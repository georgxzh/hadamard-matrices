"""Profile p=5 intermediate branches and exhaustively search a small portfolio.

The script enumerates every compatible length-15 intermediate pair, reduces
the free independent translations, ranks branches by exact factor-three
binary-row scan cost, and exhaustively searches the first three orbit
representatives. It never builds or solves an LP(333) instance.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from src.legendre import (
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    legendre_pair_to_hadamard,
    published_structured_legendre_pair_45,
    structured_compressed_pair,
)
from src.pb_certificate import write_veripb_sat_certificate
from src.staged_uncompression import (
    FactorThreeBranch,
    canonical_intermediate_translation,
    enumerate_intermediate_pairs,
)
from src.uncompress import search_uncompressions, uncompression_count
from src.verify_matrix import verify as verify_direct
from src.verify_matrix import write_report as write_direct_report
from src.verify_matrix_independent import verify as verify_independent
from src.verify_matrix_independent import write_report as write_independent_report


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "p5_branch_portfolio"


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


def _artifact(path: Path, *, tracked: bool = True) -> dict[str, object]:
    return {
        "path": _recorded_path(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "tracked": tracked,
    }


def _write_csv(matrix: list[list[int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerows(matrix)


def _signs(sequence: Sequence[int]) -> str:
    return "".join("+" if value == 1 else "-" for value in sequence)


def _canonical_pair(
    pair: tuple[tuple[int, ...], tuple[int, ...]], p: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return (
        canonical_intermediate_translation(pair[0], p)[0],
        canonical_intermediate_translation(pair[1], p)[0],
    )


def _branch_key(
    pair: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[object, ...]:
    counts = tuple(uncompression_count(row, 3) for row in pair)
    return sum(counts), max(counts), min(counts), pair


def _search_branch(
    pair: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[
    dict[str, object],
    tuple[tuple[int, ...], tuple[int, ...]] | None,
]:
    """Search with the smaller row as the stored signature table."""

    first_count, second_count = (uncompression_count(row, 3) for row in pair)
    started = time.perf_counter()
    if first_count <= second_count:
        raw = search_uncompressions(pair[1], pair[0], 3, collect=1)
        witness = (
            (raw.solutions[0][1], raw.solutions[0][0]) if raw.solutions else None
        )
        orientation = "second row streamed; first row stored"
    else:
        raw = search_uncompressions(pair[0], pair[1], 3, collect=1)
        witness = raw.solutions[0] if raw.solutions else None
        orientation = "first row streamed; second row stored"
    return {
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "first_candidates": first_count,
        "second_candidates": second_count,
        "total_candidate_rows_scanned": first_count + second_count,
        "stored_signature_vectors": raw.distinct_second_vectors,
        "matched_streamed_rows": raw.matched_first_candidates,
        "ordered_pairs_found": raw.ordered_pairs_found,
        "complete": True,
        "orientation": orientation,
    }, witness


def _verify_certificate(
    verifier: Path, opb: Path, proof: Path, output: Path
) -> dict[str, object]:
    started = time.perf_counter()
    completed = subprocess.run(
        [str(verifier), "--stats", str(opb), str(proof)],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        timeout=120,
        check=False,
    )
    text = (completed.stdout + completed.stderr).decode("utf-8", errors="replace")
    output.write_text(text, encoding="utf-8", newline="\n")
    if completed.returncode != 0 or "s VERIFIED SATISFIABLE" not in text:
        raise RuntimeError("VeriPB rejected the selected-branch witness")
    return {
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "exit_code": completed.returncode,
        "status": "VERIFIED SATISFIABLE",
        "stdout": _artifact(output),
    }


def benchmark(
    verifier: Path,
    output_directory: Path = DEFAULT_OUTPUT,
    portfolio_size: int = 3,
) -> dict[str, object]:
    """Run the deterministic complete p=5 branch profile and portfolio."""

    if not 1 <= portfolio_size <= 3:
        raise ValueError("portfolio size must be between one and three")
    verifier = verifier.resolve()
    if not verifier.is_file():
        raise FileNotFoundError(verifier)
    output_directory.mkdir(parents=True, exist_ok=True)
    started_utc = datetime.now(timezone.utc)
    started = time.perf_counter()

    prescribed = structured_compressed_pair(5, 3)
    profile_started = time.perf_counter()
    ordered_pairs = enumerate_intermediate_pairs(*prescribed)
    orbit_counts = Counter(_canonical_pair(pair, 5) for pair in ordered_pairs)
    if set(orbit_counts.values()) != {9}:
        raise RuntimeError("intermediate translation action was not free of size nine")
    canonical_pairs = sorted(orbit_counts, key=_branch_key)
    profile_seconds = time.perf_counter() - profile_started

    split_histogram = Counter(
        tuple(sum(abs(value) == 1 for value in row) for row in pair)
        for pair in ordered_pairs
    )
    if {sum(split) for split in split_histogram} != {23}:
        raise RuntimeError("combined magnitude-one count is not invariant")
    if len(ordered_pairs) != 10_476 or len(canonical_pairs) != 1_164:
        raise RuntimeError("p=5 branch counts changed unexpectedly")

    published_binary = published_structured_legendre_pair_45()
    published_intermediate = (
        compress(published_binary[0], 15),
        compress(published_binary[1], 15),
    )
    published_canonical = _canonical_pair(published_intermediate, 5)
    published_rank = canonical_pairs.index(published_canonical) + 1

    catalog = []
    for rank, pair in enumerate(canonical_pairs, 1):
        counts = tuple(uncompression_count(row, 3) for row in pair)
        catalog.append(
            {
                "rank": rank,
                "first": list(pair[0]),
                "second": list(pair[1]),
                "magnitude_one_counts": [
                    sum(abs(value) == 1 for value in pair[0]),
                    sum(abs(value) == 1 for value in pair[1]),
                ],
                "binary_preimage_counts": list(counts),
                "candidate_rows_scanned": sum(counts),
            }
        )
    catalog_path = output_directory / "canonical_branches.json"
    catalog_path.write_text(
        json.dumps(catalog, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    portfolio = []
    selected_witness: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    selected_branch: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    for rank, pair in enumerate(canonical_pairs[:portfolio_size], 1):
        search, witness = _search_branch(pair)
        if witness is not None:
            if not check_legendre_pair(*witness).ok:
                raise RuntimeError(f"rank-{rank} witness failed exact PAF")
            if not check_negative_support_sds(*witness).ok:
                raise RuntimeError(f"rank-{rank} witness failed exact SDS")
            if not check_legendre_psd_constraints(*witness):
                raise RuntimeError(f"rank-{rank} witness failed exact PSD")
            if compress(witness[0], 15) != pair[0] or compress(
                witness[1], 15
            ) != pair[1]:
                raise RuntimeError(f"rank-{rank} witness has the wrong intermediate branch")
            if selected_witness is None:
                selected_witness = witness
                selected_branch = pair
        portfolio.append(
            {
                "rank": rank,
                "branch_first": list(pair[0]),
                "branch_second": list(pair[1]),
                "search": search,
                "result": "SAT" if witness is not None else "UNSAT_BY_EXHAUSTIVE_JOIN",
                "witness_first": _signs(witness[0]) if witness else None,
                "witness_second": _signs(witness[1]) if witness else None,
            }
        )

    if selected_witness is None or selected_branch is None:
        raise RuntimeError("portfolio did not recover a binary Legendre pair")
    branch = FactorThreeBranch(*prescribed, *selected_branch)
    model = branch.model()
    if model.first_failed_constraint(*selected_witness) is not None:
        raise RuntimeError("selected witness failed its branch OPB")
    opb = model.write_opb(output_directory / "selected_branch.opb")
    proof = output_directory / "selected_branch_witness.pbp"
    write_veripb_sat_certificate(model, *selected_witness, proof)
    proof_check = _verify_certificate(
        verifier,
        opb.path,
        proof,
        output_directory / "selected_branch_witness_veripb.txt",
    )

    witness_path = output_directory / "lp45_witness.json"
    witness_path.write_text(
        json.dumps(
            {
                "source": "deterministic exhaustive p=5 branch portfolio",
                "first": _signs(selected_witness[0]),
                "second": _signs(selected_witness[1]),
                "intermediate_first": list(selected_branch[0]),
                "intermediate_second": list(selected_branch[1]),
                "prescribed_first": list(prescribed[0]),
                "prescribed_second": list(prescribed[1]),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    matrix = legendre_pair_to_hadamard(*selected_witness)
    candidate = output_directory / "H92.csv"
    _write_csv(matrix, candidate)
    direct = verify_direct(candidate, order=92)
    independent = verify_independent(candidate, order=92)
    if not direct.ok or not independent.ok:
        raise RuntimeError("portfolio H(92) failed an exact verifier")
    direct_report = output_directory / "H92_verification.txt"
    independent_report = output_directory / "H92_verification_independent.txt"
    direct_report_hash = write_direct_report(direct, direct_report)
    independent_report_hash = write_independent_report(independent, independent_report)

    metadata: dict[str, object] = {
        "status": (
            f"complete p=5 branch profile and {portfolio_size}-branch exhaustive "
            "portfolio; no LP(333) run and no order-668 result"
        ),
        "source_basis": "successive q-uncompression in kotsireas2025compression",
        "deterministic": True,
        "random_seed": None,
        "parameters": {"p": 5, "q": 3, "binary_length": 45},
        "branch_profile": {
            "ordered_intermediate_pairs": len(ordered_pairs),
            "independent_translation_orbits": len(canonical_pairs),
            "orbit_size": 9,
            "magnitude_one_total": 23,
            "ordered_split_histogram": {
                f"{left}+{right}": count
                for (left, right), count in sorted(split_histogram.items())
            },
            "minimum_candidate_rows_scanned": catalog[0][
                "candidate_rows_scanned"
            ],
            "published_branch_rank": published_rank,
            "elapsed_seconds": round(profile_seconds, 6),
            "catalog": _artifact(catalog_path),
        },
        "ranking": (
            "ascending total candidate-row scans, maximum row count, minimum row count, "
            "then lexicographic branch rows"
        ),
        "portfolio": portfolio,
        "selected_witness": _artifact(witness_path),
        "selected_branch_model": {
            "stats": vars(model.stats),
            "opb": {
                "path": _recorded_path(opb.path),
                "bytes": opb.bytes,
                "sha256": opb.sha256,
                "tracked": True,
            },
            "certificate": _artifact(proof),
            "veripb": proof_check,
        },
        "hadamard": {
            "order": 92,
            "candidate": _artifact(candidate),
            "candidate_sha256": direct.candidate_sha256,
            "direct_verifier": True,
            "independent_bitpacked_verifier": True,
            "direct_report_sha256": direct_report_hash,
            "independent_report_sha256": independent_report_hash,
        },
        "verifier": _artifact(verifier, tracked=False),
        "verifier_version": "VeriPB 3.0.2",
        "started_utc": started_utc.isoformat(),
        "elapsed_seconds_this_run": round(time.perf_counter() - started, 6),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "logical_cpu_count": os.cpu_count(),
        "cpu_cores_used": 1,
        "peak_memory": "not instrumented; smaller preimage row stored as signature table",
        "command": (
            "python -m scripts.benchmark_p5_branch_portfolio --verifier "
            "tmp/tools/veripb-3.0.2/bin/veripb.exe --portfolio-size 3"
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
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--portfolio-size", type=int, default=3)
    args = parser.parse_args()
    result = benchmark(
        args.verifier,
        args.output_directory.resolve(),
        args.portfolio_size,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
