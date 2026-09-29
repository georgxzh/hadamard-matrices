"""Bounded p=5/p=7 first-stage and conditional binary-lift PB experiments.

Run sequentially with proof logging, LP disabled, and three restart settings.
No p=37 search, no exhaustive p=7 enumeration, no timeout-as-UNSAT claims.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from scripts.benchmark_staged_uncompression import (
    REPOSITORY_ROOT, _artifact, _assignment_from_solver_output, _known_pair,
    _rows_from_assignment, _run, _verify_certificate,
)
from src.legendre import (
    check_legendre_pair, check_legendre_psd_constraints,
    check_negative_support_sds, compress, structured_compressed_pair,
)
from src.pb_certificate import write_veripb_sat_certificate
from src.staged_uncompression import (
    FactorThreeBranch, IntermediatePBModel, enumerate_intermediate_pairs,
)
from src.uncompress import search_factor_three_uncompressions, uncompression_count


def _save(path: Path, record: object) -> None:
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8", newline="\n")


def _validated_pair(model, assignment):
    """Validate actual auxiliary bits and independently check decoded rows."""
    if any(not c.satisfied_by(assignment) for c in model.iter_constraints()):
        raise ValueError("solver assignment fails OPB")
    if isinstance(model, IntermediatePBModel):
        pair = tuple(tuple(3 - 2 * (assignment[model.bit_variable(r, i, 0)] +
                                    2 * assignment[model.bit_variable(r, i, 1)])
                           for i in range(model.length)) for r in (0, 1))
        FactorThreeBranch(model.prescribed_first, model.prescribed_second, *pair)
    else:
        pair = _rows_from_assignment(model, assignment)
        if not (check_legendre_pair(*pair).ok and
                check_negative_support_sds(*pair).ok and
                check_legendre_psd_constraints(*pair)):
            raise ValueError("binary witness fails independent exact checks")
        if tuple(compress(row, model.compressed_length) for row in pair) != (
            model.first_compressed, model.second_compressed
        ):
            raise ValueError("binary witness has wrong compression")
    if model.first_failed_constraint(*pair) is not None:
        raise ValueError("reconstructed assignment fails OPB")
    return pair


def _search(model, prefix, solver, verifier, output, scratch, seconds, restart):
    opb = output / f"{prefix}.opb"
    model.write_opb(opb)
    proof = scratch / f"{prefix}.pbp"
    stdout = output / f"{prefix}_solver.txt"
    run = _run([
        str(solver), "--print-sol=1", "--verbosity=1", "--lp=0",
        f"--luby-mult={restart}", f"--proof-log={proof}",
        f"--time-limit={seconds}", str(opb),
    ], stdout, timeout=seconds + 5)
    record = {"run": run, "model_stats": vars(model.stats),
              "opb": _artifact(opb, tracked=True),
              "search_proof": _artifact(proof, tracked=False) if proof.exists() else None,
              "search_proof_verified": False,
              "restart_multiplier": restart}
    status = run["reported_status"]
    pair = None
    if status == "SATISFIABLE":
        assignment = _assignment_from_solver_output(stdout.read_text(), model.stats.variables)
        pair = _validated_pair(model, assignment)
        record["search_proof_verification"] = _verify_certificate(
            verifier, opb, proof, output / f"{prefix}_search_veripb.txt")
        record["search_proof_verified"] = True
        # Retain a small, independently checkable SAT certificate; search traces
        # can be large and remain in scratch with their exact hashes recorded.
        certificate = output / f"{prefix}_witness.pbp"
        write_veripb_sat_certificate(model, *pair, certificate)
        record["certificate_verification"] = _verify_certificate(
            verifier, opb, certificate, output / f"{prefix}_witness_veripb.txt")
        record["certificate"] = _artifact(certificate, tracked=True)
        witness = output / f"{prefix}_witness.json"
        _save(witness, {"first": pair[0], "second": pair[1],
                        "exact_opb_and_mathematical_checks": True})
        record["witness"] = _artifact(witness, tracked=True)
    elif status == "UNSATISFIABLE":
        # A raw UNSAT status is not an accepted claim without verification.
        record["unsat_claim_accepted"] = False
        raise RuntimeError(f"{prefix}: unexpected UNSAT; requires separate proof audit")
    elif status != "TIMELIMIT" and not run["externally_timed_out"]:
        raise RuntimeError(f"{prefix}: solver error: {run}")
    print(f"{prefix}: {status}, {run['elapsed_seconds']:.3f}s", flush=True)
    return record, pair


def benchmark(solver: Path, verifier: Path, output: Path, scratch: Path,
              seconds: int = 10) -> dict:
    if not 1 <= seconds <= 20:
        raise ValueError("search budget must be 1..20 seconds")
    solver, verifier = solver.resolve(), verifier.resolve()
    if not solver.is_file() or not verifier.is_file():
        raise FileNotFoundError("solver and verifier executables are required")
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    metadata = {
        "status": "bounded first-stage and conditional second-stage experiment; no p=37 solve",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "solver": _artifact(solver, tracked=False),
        "verifier": _artifact(verifier, tracked=False),
        "python": sys.version, "platform": platform.platform(),
        "cores_per_process": 1, "parallel_processes": 1,
        "search_seconds_each": seconds, "random_seed": None,
        "restart_multipliers": [50, 100, 200],
        "design": "paired restart sensitivity runs; deterministic settings, not random seeds",
        "canonicalization": "least anchor triple, distinct from full-row catalog lex order",
        "validation": {}, "first_stage": {}, "second_stage": {},
        "command": "python -m scripts.benchmark_intermediate_scaling --solver "
                   "tmp/tools/roundingsat/roundingsat.exe --verifier "
                   f"tmp/tools/veripb-3.0.2/bin/veripb.exe --search-seconds {seconds}",
    }
    def checkpoint():
        metadata["elapsed_seconds"] = round(time.perf_counter() - start, 6)
        _save(output / "metadata.json", metadata)

    for p, expected in ((3, 792), (5, 10476)):
        t = time.perf_counter()
        prescribed = structured_compressed_pair(p, 3)
        pairs = enumerate_intermediate_pairs(*prescribed)
        canonical = IntermediatePBModel(*prescribed, canonical_translations=True)
        orbits = Counter(canonical.canonicalize_pair(*pair) for pair in pairs)
        assert len(pairs) == expected and len(orbits) * 9 == expected
        assert set(orbits.values()) == {9}
        constraints = tuple(canonical.iter_constraints())
        for pair in orbits:
            if canonical.first_failed_constraint(*pair, constraints=constraints) is not None:
                raise RuntimeError("canonicalization lost a valid intermediate orbit")
        binary = _known_pair(p)
        known = canonical.canonicalize_pair(*(compress(row, 3 * p) for row in binary))
        opb = output / f"p{p}_known_canonical.opb"
        canonical.write_opb(opb)
        cert = output / f"p{p}_known_canonical.pbp"
        write_veripb_sat_certificate(canonical, *known, cert)
        verification = _verify_certificate(verifier, opb, cert,
                                           output / f"p{p}_known_canonical_veripb.txt")
        metadata["validation"][f"p{p}"] = {
            "ordered_pairs": len(pairs), "canonical_pairs": len(orbits),
            "orbit_size": 9, "all_canonical_pairs_pass_full_opb": True,
            "elapsed_seconds": round(time.perf_counter() - t, 6),
            "known_certificate": _artifact(cert, tracked=True),
            "known_opb": _artifact(opb, tracked=True), "verification": verification,
        }
        print(f"p{p}: validated {len(orbits)} complete canonical orbits", flush=True)
        checkpoint()

    # Positive search controls, with no fixed entries.
    for canonical in (False, True):
        label = "canonical" if canonical else "unbroken"
        model = IntermediatePBModel(*structured_compressed_pair(3, 3),
                                    canonical_translations=canonical)
        key = f"p3_{label}_r100"
        record, _ = _search(model, key, solver, verifier, output, scratch, seconds, 100)
        metadata["first_stage"][key] = record
        checkpoint()

    branches = {}
    for p in (5, 7):
        prescribed = structured_compressed_pair(p, 3)
        canonical_model = IntermediatePBModel(*prescribed, canonical_translations=True)
        for restart in (50, 100, 200):
            for canonical in (False, True):
                label = "canonical" if canonical else "unbroken"
                key = f"p{p}_{label}_r{restart}"
                model = IntermediatePBModel(*prescribed, canonical_translations=canonical)
                record, pair = _search(model, key, solver, verifier, output, scratch,
                                       seconds, restart)
                metadata["first_stage"][key] = record
                if pair is not None:
                    anchored = canonical_model.canonicalize_pair(*pair)
                    # At most three distinct branches per p, first discovered order.
                    selected = branches.setdefault(p, [])
                    if anchored not in [entry[1] for entry in selected] and len(selected) < 3:
                        selected.append((key, anchored))
                checkpoint()

    for p, selected in branches.items():
        for index, (source, pair) in enumerate(selected, 1):
            branch = FactorThreeBranch(*structured_compressed_pair(p, 3), *pair)
            model = branch.model(canonical_translations=True, projected_correlations=True)
            key = f"p{p}_branch{index}_projected_canonical"
            record, _ = _search(model, key, solver, verifier, output, scratch, seconds, 100)
            record.update({"first_stage_source": source, "intermediate_pair": pair,
                           "row_preimage_counts": [uncompression_count(row, 3) for row in pair]})
            metadata["second_stage"][key] = record
            checkpoint()

    # Same known SAT branch for the generic PB / exact specialized join comparison.
    catalog = json.loads((REPOSITORY_ROOT / "results/p5_branch_portfolio/canonical_branches.json").read_text())
    pair = tuple(tuple(catalog[0][key]) for key in ("first", "second"))
    branch = FactorThreeBranch(*structured_compressed_pair(5, 3), *pair)
    record, _ = _search(branch.model(canonical_translations=True, projected_correlations=True),
                        "p5_rank1_projected_canonical", solver, verifier, output, scratch, seconds, 100)
    metadata["second_stage"]["p5_rank1_projected_canonical"] = record
    t = time.perf_counter()
    # Store the smaller side, streaming the larger side.
    search = search_factor_three_uncompressions(pair[1], pair[0], collect=1)
    assert search.ordered_pairs_found == 27 and search.solutions
    metadata["p5_exact_join_baseline"] = {
        "branch": "p5 rank 1", "intermediate_pair": pair,
        "elapsed_seconds": round(time.perf_counter() - t, 6),
        "first_candidates": search.first_candidates,
        "second_candidates": search.second_candidates,
        "ordered_pairs": search.ordered_pairs_found,
        "note": "complete projected PAF join retaining all cross terms; exponential row enumeration",
    }
    metadata["completed_utc"] = datetime.now(timezone.utc).isoformat()
    checkpoint()
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path,
                        default=REPOSITORY_ROOT / "results/intermediate_scaling")
    parser.add_argument("--scratch-directory", type=Path,
                        default=REPOSITORY_ROOT / "tmp/intermediate_scaling")
    parser.add_argument("--search-seconds", type=int, default=10)
    args = parser.parse_args()
    benchmark(args.solver, args.verifier, args.output_directory.resolve(),
              args.scratch_directory.resolve(), args.search_seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
