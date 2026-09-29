"""Validate exact ternary phases and run small bounded solver comparisons."""

from __future__ import annotations

import argparse
import json
import math
import platform
import random
import sys
import time
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

from scripts.benchmark_intermediate_scaling import _validated_pair
from scripts.benchmark_staged_uncompression import (
    REPOSITORY_ROOT, _artifact, _assignment_from_solver_output, _known_pair,
    _run, _verify_certificate,
)
from src.legendre import (
    check_legendre_pair, check_legendre_psd_constraints, check_negative_support_sds,
    compress, periodic_autocorrelation, structured_compressed_pair,
)
from src.pb_certificate import write_veripb_sat_certificate
from src.staged_uncompression import FactorThreeBranch, IntermediatePBModel
from src.ternary_phase import PhaseRow, TernaryPhasePBModel, search_phase_uncompressions
from src.uncompress import iter_uncompression_masks, mask_to_sequence


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def find_intermediate(prime: int, *, seed: int, seconds: float, max_iterations: int = 200_000):
    """Bounded heuristic branch acquisition; only exact zero energy is accepted.

    Moves preserve every prescribed residue sum. Incremental integer PAF
    updates include quadratic delta products. No optimality/UNSAT claim.
    """
    if prime not in (3, 5, 7) or not 0 < seconds <= 20 or max_iterations <= 0:
        raise ValueError("branch acquisition is bounded to p=3,5,7 and <=20 seconds")
    rng = random.Random(seed)
    prescribed = structured_compressed_pair(prime, 3)
    n = 3 * prime
    options = [[tuple(t for t in product((-3, -1, 1, 3), repeat=3) if sum(t) == target)
                for target in row] for row in prescribed]
    targets = [6*n-4] + [-6] * (n//2)
    started = time.perf_counter()
    best = None
    pair = None
    iterations = 0
    for iteration in range(max_iterations):
        if iteration % 128 == 0 and time.perf_counter() - started >= seconds:
            break
        if iteration % 4000 == 0:
            rows = [[0] * n for _ in range(2)]
            for r in range(2):
                for residue in range(prime):
                    for k, value in enumerate(rng.choice(options[r][residue])):
                        rows[r][residue+k*prime] = value
            residual = [(sum(periodic_autocorrelation(row, s) for row in rows) - target)//4
                        for s, target in enumerate(targets)]
            energy = sum(v*v for v in residual)
        r, residue = rng.randrange(2), rng.randrange(prime)
        replacement = rng.choice(options[r][residue])
        row = rows[r]
        delta = {residue+k*prime: v-row[residue+k*prime]
                 for k, v in enumerate(replacement) if v != row[residue+k*prime]}
        change = [sum(d * (row[(i+s) % n] + row[(i-s) % n] + delta.get((i+s) % n, 0))
                      for i, d in delta.items()) // 4 for s in range(n//2+1)]
        candidate = [a+b for a, b in zip(residual, change, strict=True)]
        new_energy = sum(v*v for v in candidate)
        temperature = 25 * (0.02 ** ((iteration % 4000) / 3999))
        if new_energy <= energy or rng.random() < math.exp((energy-new_energy)/temperature):
            for i, d in delta.items():
                row[i] += d
            residual, energy = candidate, new_energy
        iterations = iteration + 1
        best = energy if best is None else min(best, energy)
        if energy == 0:
            # Never trust the incremental objective as the certificate.
            FactorThreeBranch(*prescribed, *rows)
            model = IntermediatePBModel(*prescribed, canonical_translations=True)
            pair = model.canonicalize_pair(*rows)
            if model.first_failed_constraint(*pair) is not None:
                raise AssertionError("heuristic candidate fails exact OPB")
            break
    return {
        "prime": prime, "seed": seed, "time_limit": seconds,
        "max_iterations": max_iterations, "iterations": iterations,
        "best_energy": best, "elapsed_seconds": time.perf_counter() - started,
        "status": "exact_branch_found" if pair else "budget_exhausted",
        "pair": pair,
    }


def solve(model, label, solver, verifier, output, scratch, seconds, restart=100):
    opb = output / f"{label}.opb"
    model.write_opb(opb)
    proof = scratch / f"{label}.pbp"
    stdout = output / f"{label}_solver.txt"
    record = {
        "stats": vars(model.stats), "opb": _artifact(opb, tracked=True),
        "run": _run([str(solver), "--lp=0", "--print-sol=1", "--verbosity=1",
                     f"--luby-mult={restart}", f"--time-limit={seconds}",
                     f"--proof-log={proof}", str(opb)], stdout, timeout=seconds+5),
    }
    record["search_proof"] = _artifact(proof, tracked=False) if proof.exists() else None
    status = record["run"]["reported_status"]
    if status == "SATISFIABLE":
        assignment = _assignment_from_solver_output(stdout.read_text(), model.stats.variables)
        pair = (model.pair_from_assignment(assignment) if isinstance(model, TernaryPhasePBModel)
                else _validated_pair(model, assignment))
        if not (check_legendre_pair(*pair).ok and check_negative_support_sds(*pair).ok
                and check_legendre_psd_constraints(*pair)):
            raise AssertionError("solver witness fails independent exact checks")
        record["proof_verification"] = _verify_certificate(verifier, opb, proof,
                                                           output / f"{label}_search_veripb.txt")
        cert = output / f"{label}_witness.pbp"
        write_veripb_sat_certificate(model, *pair, cert)
        record["certificate_verification"] = _verify_certificate(verifier, opb, cert,
                                                                 output / f"{label}_witness_veripb.txt")
        record["certificate"] = _artifact(cert, tracked=True)
        witness = output / f"{label}_witness.json"
        save(witness, {"first": pair[0], "second": pair[1], "paf_sds_psd_verified": True})
        record["witness"] = _artifact(witness, tracked=True)
    elif status == "UNSATISFIABLE":
        # Record but do not promote a raw solver status to a mathematical claim.
        record["unsat_claim_accepted"] = False
    elif status != "TIMELIMIT" and not record["run"]["externally_timed_out"]:
        raise RuntimeError(f"{label}: solver failed")
    print(f"{label}: {status}, {record['run']['elapsed_seconds']:.3f}s", flush=True)
    return record


def run_packed_controls(metadata, output):
    """Separate symmetry savings from the cost of updating phase cross terms."""
    start = time.perf_counter()
    known = _known_pair(3)
    catalog = json.loads((REPOSITORY_ROOT / "results/p5_branch_portfolio/canonical_branches.json").read_text())
    branches = {
        "p3": tuple(compress(row, 9) for row in known),
        "p5_rank1": tuple(tuple(catalog[0][key]) for key in ("first", "second")),
    }
    controls = {}
    for label, pair in branches.items():
        controls[label] = {}
        for evaluation in ("incremental", "packed"):
            result = search_phase_uncompressions(*pair, evaluation=evaluation, time_limit=20)
            if not result.complete or result.ordered_pairs != (135 if label == "p3" else 27):
                raise AssertionError("same-domain control failed exact known count")
            controls[label][evaluation] = vars(result)
            print(f"{label} {evaluation} control: {result.elapsed_seconds:.3f}s", flush=True)
    metadata["same_domain_controls"] = {
        "results": controls, "elapsed_seconds": time.perf_counter()-start,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "same anchor-zero assignments; Gray incremental vs packed exact PAF",
    }
    save(output / "metadata.json", metadata)


def benchmark(solver, verifier, output, scratch, seconds=10):
    if not 1 <= seconds <= 20:
        raise ValueError("search seconds must be 1..20")
    solver, verifier = solver.resolve(), verifier.resolve()
    if not solver.is_file() or not verifier.is_file():
        raise FileNotFoundError("solver and verifier executables required")
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    metadata = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "python": sys.version,
        "solver": _artifact(solver, tracked=False), "verifier": _artifact(verifier, tracked=False),
        "search_seconds": seconds, "solver_cores": 1, "parallel_processes": 1,
        "status": "bounded exact ternary formulation validation; no p=37 run",
        "command": "python -m scripts.benchmark_ternary_phase --solver tmp/tools/roundingsat/roundingsat.exe "
                   f"--verifier tmp/tools/veripb-3.0.2/bin/veripb.exe --search-seconds {seconds}",
        "validation": {}, "branch_acquisition": [], "models": {}, "phase_joins": {},
    }
    def checkpoint():
        metadata["elapsed_seconds"] = time.perf_counter()-start
        save(output / "metadata.json", metadata)

    known = _known_pair(3)
    intermediate3 = tuple(compress(row, 9) for row in known)
    verified = 0
    for compressed in intermediate3:
        row = PhaseRow(compressed)
        terms = [row.paf_terms(s) for s in range(3*row.length)]
        for mask in iter_uncompression_masks(compressed, 3):
            binary = mask_to_sequence(mask, 3*row.length)
            phases = row.encode(binary)
            if row.decode(phases) != binary:
                raise AssertionError("phase map is not a bijection")
            for s, (constant, edges) in enumerate(terms):
                value = constant + sum(w for u, v, h, w in edges if (phases[v]-phases[u]) % 3 == h)
                if value != periodic_autocorrelation(binary, s):
                    raise AssertionError("phase formula loses a cross term or layer carry")
            verified += 1
    metadata["validation"]["p3_all_preimages"] = {"rows": verified, "shifts_each": 27,
                                                   "exact_checks": verified*27}
    catalog = json.loads((REPOSITORY_ROOT / "results/p5_branch_portfolio/canonical_branches.json").read_text())
    intermediate5 = tuple(tuple(catalog[0][key]) for key in ("first", "second"))
    branches = {"p3": intermediate3, "p5_rank1": intermediate5}
    for label, pair in branches.items():
        result = search_phase_uncompressions(*pair, time_limit=20)
        expected = 135 if label == "p3" else 27
        if not result.complete or result.ordered_pairs != expected:
            raise AssertionError(f"{label}: exact phase join failed the known count gate")
        metadata["phase_joins"][label] = vars(result)
        # A compact phase certificate checks the formulation before open search.
        model = TernaryPhasePBModel(*pair)
        opb = output / f"{label}_known_phase.opb"
        model.write_opb(opb)
        cert = output / f"{label}_known_phase.pbp"
        write_veripb_sat_certificate(model, *result.solutions[0], cert)
        metadata["validation"][label] = {
            "opb": _artifact(opb, tracked=True), "certificate": _artifact(cert, tracked=True),
            "verification": _verify_certificate(verifier, opb, cert, output / f"{label}_known_phase_veripb.txt"),
        }
        print(f"{label}: exact phase join {result.ordered_pairs} pairs in {result.elapsed_seconds:.3f}s", flush=True)
        checkpoint()

    # The previous first stage did not yield p=7. A small reproducible heuristic
    # can acquire a necessary-condition branch, with exact acceptance afterward.
    for seed in (20260928, 20260929, 20260930):
        acquired = find_intermediate(7, seed=seed, seconds=10)
        metadata["branch_acquisition"].append(acquired)
        print(f"p7 seed {seed}: {acquired['status']}, best energy {acquired['best_energy']}", flush=True)
        if acquired["pair"]:
            branches["p7"] = acquired["pair"]
            model = IntermediatePBModel(*structured_compressed_pair(7, 3), canonical_translations=True)
            opb = output / "p7_intermediate.opb"
            model.write_opb(opb)
            cert = output / "p7_intermediate.pbp"
            write_veripb_sat_certificate(model, *acquired["pair"], cert)
            metadata["validation"]["p7_intermediate"] = {
                "opb": _artifact(opb, tracked=True), "certificate": _artifact(cert, tracked=True),
                "verification": _verify_certificate(verifier, opb, cert, output / "p7_intermediate_veripb.txt"),
            }
            break
        checkpoint()
    for label, pair in branches.items():
        p = len(pair[0]) // 3
        branch = FactorThreeBranch(*structured_compressed_pair(p, 3), *pair)
        for restart in ((100,) if p == 3 else (50, 100, 200)):
            for encoding in ("binary", "phase"):
                model = (branch.model(canonical_translations=True, projected_correlations=True)
                         if encoding == "binary" else TernaryPhasePBModel(*pair))
                key = f"{label}_{encoding}_r{restart}"
                metadata["models"][key] = solve(model, key, solver, verifier, output, scratch, seconds, restart)
                checkpoint()
        if p == 7:
            result = search_phase_uncompressions(*pair, time_limit=seconds,
                                                  max_candidates_per_side=1_000_000,
                                                  max_stored_signatures=250_000)
            metadata["phase_joins"][label] = vars(result)
            checkpoint()
    run_packed_controls(metadata, output)
    metadata["completed_utc"] = datetime.now(timezone.utc).isoformat()
    checkpoint()
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, default=REPOSITORY_ROOT / "results/ternary_phase")
    parser.add_argument("--scratch-directory", type=Path, default=REPOSITORY_ROOT / "tmp/ternary_phase")
    parser.add_argument("--search-seconds", type=int, default=10)
    parser.add_argument("--packed-controls-only", action="store_true",
                        help="append the equal-domain controls to an existing benchmark")
    args = parser.parse_args()
    if args.packed_controls_only:
        output = args.output_directory.resolve()
        run_packed_controls(json.loads((output / "metadata.json").read_text()), output)
    else:
        benchmark(args.solver, args.verifier, args.output_directory.resolve(), args.scratch_directory.resolve(), args.search_seconds)


if __name__ == "__main__":
    main()
