"""Build the p=37 first-stage model and validate projected second-stage keys.

This script does not solve either length-333 model. It writes the exact p=37
first-stage OPB to ignored scratch storage, records its hash and dimensions,
validates the factor-three PAF projection at p=3 and p=5, and performs one
bounded p=5 solver probe.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from src.legendre import (
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    decode_signs,
    structured_compressed_pair,
)
from src.pb_certificate import write_veripb_sat_certificate
from src.pb_model import factor_three_projected_model_stats
from src.staged_uncompression import FactorThreeBranch, IntermediatePBModel
from src.uncompress import (
    UncompressionSearch,
    search_factor_three_uncompressions,
    uncompression_count,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "projected_uncompression"
DEFAULT_SCRATCH = REPOSITORY_ROOT / "tmp" / "projected_uncompression"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _recorded_path(path: Path) -> str:
    try:
        return path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        return str(path)


def _artifact(path: Path, *, tracked: bool) -> dict[str, object]:
    return {
        "path": _recorded_path(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "tracked": tracked,
    }


def _signs(sequence: Sequence[int]) -> str:
    return "".join("+" if value == 1 else "-" for value in sequence)


def _run(command: Sequence[str], output: Path, *, timeout: float) -> dict[str, object]:
    started = time.perf_counter()
    completed = subprocess.run(
        list(command),
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    text = (completed.stdout + completed.stderr).decode("utf-8", errors="replace")
    output.write_text(text, encoding="utf-8", newline="\n")
    status_match = re.search(r"(?m)^s ([A-Z]+(?: [A-Z]+)*)\r?$", text)
    return {
        "command": [str(part) for part in command],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "exit_code": completed.returncode,
        "reported_status": status_match.group(1) if status_match else None,
        "stdout": _artifact(output, tracked=True),
    }


def _known_lp27() -> tuple[tuple[int, ...], tuple[int, ...]]:
    record = json.loads(
        (REPOSITORY_ROOT / "results" / "pb_uncompression" / "lp27_witness.json").read_text(
            encoding="utf-8"
        )
    )
    return decode_signs(record["first"]), decode_signs(record["second"])


def _projected_search(
    branch: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[
    UncompressionSearch,
    tuple[tuple[int, ...], tuple[int, ...]],
    float,
    str,
]:
    first_count, second_count = (uncompression_count(row, 3) for row in branch)
    started = time.perf_counter()
    if first_count <= second_count:
        search = search_factor_three_uncompressions(branch[1], branch[0], collect=1)
        witness = search.solutions[0][1], search.solutions[0][0]
        orientation = "second row streamed; first row stored"
    else:
        search = search_factor_three_uncompressions(branch[0], branch[1], collect=1)
        witness = search.solutions[0]
        orientation = "first row streamed; second row stored"
    return search, witness, time.perf_counter() - started, orientation


def build(
    solver: Path,
    verifier: Path,
    output_directory: Path = DEFAULT_OUTPUT,
    scratch_directory: Path = DEFAULT_SCRATCH,
    probe_seconds: int = 10,
) -> dict[str, object]:
    """Build exact artifacts and run only small validation/probe computations."""

    if not 0 < probe_seconds < 30:
        raise ValueError("probe seconds must be between 1 and 29")
    solver = solver.resolve()
    verifier = verifier.resolve()
    if not solver.is_file() or not verifier.is_file():
        raise FileNotFoundError("solver and verifier must be executable files")
    output_directory.mkdir(parents=True, exist_ok=True)
    scratch_directory.mkdir(parents=True, exist_ok=True)
    started_utc = datetime.now(timezone.utc)
    started = time.perf_counter()

    prescribed37 = structured_compressed_pair(37, 3)
    first_stage = IntermediatePBModel(*prescribed37)
    first_stage_artifact = first_stage.write_opb(
        scratch_directory / "p37_first_stage.opb"
    )

    projected333 = factor_three_projected_model_stats(111)
    full333 = {
        "compressed_length": 111,
        "factor": 3,
        "uncompressed_length": 333,
        "base_variables": 666,
        "xor_variables": 110_556,
        "variables": 111_222,
        "xor_inequalities": 442_224,
        "compression_equalities": 222,
        "correlation_equalities": 166,
        "symmetry_inequalities": 0,
        "constraint_records": 442_612,
        "normalized_inequalities": 443_000,
    }

    lp27 = _known_lp27()
    intermediate27 = compress(lp27[0], 9), compress(lp27[1], 9)
    search27 = search_factor_three_uncompressions(*intermediate27, collect=1)
    if search27.ordered_pairs_found != 135 or not search27.solutions:
        raise RuntimeError("projected p=3 validation count changed")

    catalog = json.loads(
        (
            REPOSITORY_ROOT
            / "results"
            / "p5_branch_portfolio"
            / "canonical_branches.json"
        ).read_text(encoding="utf-8")
    )
    rank1 = tuple(catalog[0][key] for key in ("first", "second"))
    branch45 = tuple(tuple(row) for row in rank1)
    search45, witness45, search45_seconds, orientation = _projected_search(branch45)
    if search45.ordered_pairs_found != 27:
        raise RuntimeError("projected p=5 join disagrees with the complete full-key count")
    if not check_legendre_pair(*witness45).ok:
        raise RuntimeError("projected p=5 witness failed full exact PAF")
    if not check_negative_support_sds(*witness45).ok:
        raise RuntimeError("projected p=5 witness failed exact SDS")
    if not check_legendre_psd_constraints(*witness45):
        raise RuntimeError("projected p=5 witness failed exact PSD")
    if compress(witness45[0], 15) != branch45[0] or compress(
        witness45[1], 15
    ) != branch45[1]:
        raise RuntimeError("projected p=5 witness has the wrong fixed branch")

    prescribed5 = structured_compressed_pair(5, 3)
    projected_model = FactorThreeBranch(*prescribed5, *branch45).model(
        projected_correlations=True
    )
    if projected_model.first_failed_constraint(*witness45) is not None:
        raise RuntimeError("p=5 witness failed the projected OPB model")
    projected_opb = projected_model.write_opb(
        output_directory / "p5_rank1_projected.opb"
    )
    certificate = output_directory / "p5_rank1_witness.pbp"
    write_veripb_sat_certificate(projected_model, *witness45, certificate)
    verifier_output = output_directory / "p5_rank1_witness_veripb.txt"
    verification = _run(
        [str(verifier), "--stats", str(projected_opb.path), str(certificate)],
        verifier_output,
        timeout=120,
    )
    if verification["exit_code"] != 0 or "VERIFIED SATISFIABLE" not in verifier_output.read_text(
        encoding="utf-8"
    ):
        raise RuntimeError("VeriPB rejected the projected p=5 certificate")

    proof = scratch_directory / "p5_rank1_projected_search.pbp"
    solver_probe = _run(
        [
            str(solver),
            "--print-sol=1",
            "--verbosity=1",
            "--lp=0",
            f"--proof-log={proof}",
            f"--time-limit={probe_seconds}",
            str(projected_opb.path),
        ],
        output_directory / "p5_rank1_solver_probe.txt",
        timeout=probe_seconds + 20,
    )
    solver_probe["proof_log"] = _artifact(proof, tracked=False)
    solver_probe["proof_complete"] = solver_probe["reported_status"] in {
        "SATISFIABLE",
        "UNSATISFIABLE",
    }

    witness_path = output_directory / "p5_rank1_witness.json"
    witness_path.write_text(
        json.dumps(
            {
                "first": _signs(witness45[0]),
                "second": _signs(witness45[1]),
                "intermediate_first": list(branch45[0]),
                "intermediate_second": list(branch45[1]),
                "full_legendre_check": True,
                "negative_support_sds": True,
                "cyclotomic_psd": True,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    metadata: dict[str, object] = {
        "status": (
            "non-enumerative p=37 first-stage model plus exact projected "
            "second-stage validation; no LP(333) solve and no order-668 result"
        ),
        "projection_theorem": (
            "for a fixed valid factor-three intermediate pair of odd length N, "
            "final PAF equations at shifts 1..N-1 imply every omitted shift"
        ),
        "p37_first_stage": {
            "solved": False,
            "stats": vars(first_stage.stats),
            "opb": {
                "path": _recorded_path(first_stage_artifact.path),
                "bytes": first_stage_artifact.bytes,
                "sha256": first_stage_artifact.sha256,
                "tracked": False,
            },
        },
        "p37_fixed_branch_second_stage_dimensions": {
            "full": full333,
            "projected": vars(projected333),
            "variable_reduction": full333["variables"] - projected333.variables,
            "record_reduction": (
                full333["constraint_records"] - projected333.constraint_records
            ),
            "requires_valid_intermediate_branch": True,
        },
        "p3_validation": {
            "first_candidates": search27.first_candidates,
            "second_candidates": search27.second_candidates,
            "distinct_second_vectors": search27.distinct_second_vectors,
            "matched_first_candidates": search27.matched_first_candidates,
            "ordered_pairs_found": search27.ordered_pairs_found,
            "agrees_with_full_key_search": True,
        },
        "p5_validation": {
            "branch_rank": 1,
            "signature_coordinates": 14,
            "full_key_coordinates": 22,
            "orientation": orientation,
            "elapsed_seconds": round(search45_seconds, 6),
            "first_candidates": uncompression_count(branch45[0], 3),
            "second_candidates": uncompression_count(branch45[1], 3),
            "distinct_stored_vectors": search45.distinct_second_vectors,
            "matched_streamed_rows": search45.matched_first_candidates,
            "ordered_pairs_found": search45.ordered_pairs_found,
            "agrees_with_full_key_search": True,
            "witness": _artifact(witness_path, tracked=True),
            "model_stats": vars(projected_model.stats),
            "opb": {
                "path": _recorded_path(projected_opb.path),
                "bytes": projected_opb.bytes,
                "sha256": projected_opb.sha256,
                "tracked": True,
            },
            "certificate": _artifact(certificate, tracked=True),
            "veripb": verification,
            "bounded_solver_probe": solver_probe,
        },
        "solver": _artifact(solver, tracked=False),
        "solver_reported_commit": "d4edbf7",
        "verifier": _artifact(verifier, tracked=False),
        "verifier_version": "VeriPB 3.0.2",
        "random_seed": None,
        "cpu_cores_used": 1,
        "started_utc": started_utc.isoformat(),
        "elapsed_seconds_this_run": round(time.perf_counter() - started, 6),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "logical_cpu_count": os.cpu_count(),
        "command": (
            "python -m scripts.build_projected_uncompression --solver "
            "tmp/tools/roundingsat/roundingsat.exe --verifier "
            "tmp/tools/veripb-3.0.2/bin/veripb.exe --probe-seconds 10"
        ),
    }
    (output_directory / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scratch-directory", type=Path, default=DEFAULT_SCRATCH)
    parser.add_argument("--probe-seconds", type=int, default=10)
    args = parser.parse_args()
    metadata = build(
        args.solver,
        args.verifier,
        args.output_directory.resolve(),
        args.scratch_directory.resolve(),
        args.probe_seconds,
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
