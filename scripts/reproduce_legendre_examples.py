"""Reproduce published small Legendre pairs and dual-verify their matrices."""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Callable

from src.legendre import (
    check_legendre_compression_constants,
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    legendre_pair_to_hadamard,
    periodic_autocorrelation,
    published_legendre_pair_3,
    published_legendre_pair_5,
    published_legendre_pair_7,
    published_legendre_pair_27,
)
from src.verify_matrix import verify as verify_direct
from src.verify_matrix import write_report as write_direct_report
from src.verify_matrix_independent import verify as verify_independent
from src.verify_matrix_independent import write_report as write_independent_report


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "legendre_examples"
PairFactory = Callable[[], tuple[tuple[int, ...], tuple[int, ...]]]
EXAMPLES: tuple[tuple[int, PairFactory], ...] = (
    (3, published_legendre_pair_3),
    (5, published_legendre_pair_5),
    (7, published_legendre_pair_7),
    (27, published_legendre_pair_27),
)


def _signs(sequence: tuple[int, ...]) -> str:
    return "".join("+" if value == 1 else "-" for value in sequence)


def _write_csv(matrix: list[list[int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerows(matrix)


def reproduce(output_directory: Path = DEFAULT_OUTPUT) -> dict[str, object]:
    """Write and exactly verify H(8), H(12), H(16), and H(56)."""

    started_at = datetime.now(timezone.utc)
    started = perf_counter()
    output_directory.mkdir(parents=True, exist_ok=True)
    examples: list[dict[str, object]] = []

    for length, factory in EXAMPLES:
        first, second = factory()
        paf_check = check_legendre_pair(first, second)
        sds_check = check_negative_support_sds(first, second)
        if not paf_check.ok or not sds_check.ok or not check_legendre_psd_constraints(first, second):
            raise RuntimeError(f"published LP({length}) failed an exact source-sequence check")

        order = 2 * length + 2
        matrix = legendre_pair_to_hadamard(first, second)
        candidate = output_directory / f"H{order}.csv"
        _write_csv(matrix, candidate)
        direct = verify_direct(candidate, order=order)
        independent = verify_independent(candidate, order=order)
        direct_report = output_directory / f"H{order}_verification.txt"
        independent_report = output_directory / f"H{order}_verification_independent.txt"
        direct_report_hash = write_direct_report(direct, direct_report)
        independent_report_hash = write_independent_report(independent, independent_report)
        if not direct.ok or not independent.ok:
            raise RuntimeError(
                f"H({order}) verification failed: direct={direct.message}; "
                f"independent={independent.message}"
            )

        compression_outputs: dict[str, object] = {}
        for output_length in (3, 9):
            if length % output_length == 0:
                if not check_legendre_compression_constants(first, second, output_length):
                    raise RuntimeError(f"LP({length}) compression to {output_length} failed")
                compression_outputs[str(output_length)] = {
                    "factor": length // output_length,
                    "first": list(compress(first, output_length)),
                    "second": list(compress(second, output_length)),
                }

        examples.append(
            {
                "length": length,
                "source": "Fletcher--Gysin--Seberry (2001), Table 4",
                "first": _signs(first),
                "second": _signs(second),
                "row_sums": [sum(first), sum(second)],
                "combined_paf": [
                    periodic_autocorrelation(first, shift)
                    + periodic_autocorrelation(second, shift)
                    for shift in range(length)
                ],
                "sds_parameters": [
                    length,
                    sds_check.block_sizes[0],
                    sds_check.block_sizes[1],
                    sds_check.lambda_value,
                ],
                "compressions": compression_outputs,
                "matrix_order": order,
                "candidate": candidate.relative_to(REPOSITORY_ROOT).as_posix(),
                "candidate_sha256": direct.candidate_sha256,
                "direct_report_sha256": direct_report_hash,
                "independent_report_sha256": independent_report_hash,
                "dual_exact_verification": True,
            }
        )

    metadata: dict[str, object] = {
        "status": "published small-example reproduction; not an order-668 result",
        "deterministic": True,
        "random_seed": None,
        "indexing": "zero-based; PAF shift i -> i+s mod length",
        "dft_sign": "positive exp(2*pi*i/n); PSD certified in cyclotomic integer arithmetic",
        "compression": "length d*m to d by a[j+r*d], r=0..m-1",
        "source_pdf_sha256": "4d0bc39f392a24dfb0bec3a0f17961eab4dfffe85956a1204016110d029c82b5",
        "started_utc": started_at.isoformat(),
        "elapsed_seconds_this_run": round(perf_counter() - started, 6),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "logical_cpu_count": os.cpu_count(),
        "cpu_cores_used": 1,
        "peak_memory": "not instrumented; largest matrix is 56 x 56",
        "command": "python -m scripts.reproduce_legendre_examples",
        "examples": examples,
    }
    metadata_path = output_directory / "metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    metadata = reproduce(args.output_directory.resolve())
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
