"""Derive the prescribed pq^2 compressed pair and uncompress it at p=3, q=3.

The compressed rows are derived from the quadratic-character formula rather
than transcribed from the publisher's blocked figure, so this script depends on
no external artifact.  It then performs the complete factor-9 uncompression at
``p=3``, producing an LP(27) and a dual-verified H(56).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import sys
from datetime import datetime, timezone
from math import log10
from pathlib import Path
from time import perf_counter

from src.legendre import (
    check_compressed_legendre_constants,
    check_compressed_legendre_psd,
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    jacobsthal_shifted_character_sum,
    legendre_pair_to_hadamard,
    structured_compressed_pair,
)
from src.uncompress import search_uncompressions, uncompression_count
from src.verify_matrix import verify as verify_direct
from src.verify_matrix import write_report as write_direct_report
from src.verify_matrix_independent import verify as verify_independent
from src.verify_matrix_independent import write_report as write_independent_report


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "pq2_uncompression"

# Every (p, q) whose prescribed compressed pair is certified here.  Only p=3 is
# enumerated; the rest are cost-reported, since p=5 already exceeds the
# repository's four-core / thirty-minute / ten-gigabyte approval gate.
CERTIFIED = ((3, 3), (5, 3), (7, 3), (11, 3), (13, 3), (37, 3), (5, 5), (7, 5))
ENUMERATED = (3, 3)


def _signs(sequence: tuple[int, ...]) -> str:
    return "".join("+" if value == 1 else "-" for value in sequence)


def _write_csv(matrix: list[list[int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerows(matrix)


def certify_prescribed_pairs() -> list[dict[str, object]]:
    """Check every exact necessary condition on the derived compressed pairs."""

    certificates: list[dict[str, object]] = []
    for prime, root in CERTIFIED:
        first, second = structured_compressed_pair(prime, root)
        factor = root * root
        length = prime * factor
        check = check_compressed_legendre_constants(first, second, factor)
        if not check.ok:
            raise RuntimeError(f"prescribed pair p={prime}, q={root} failed: {check.message}")
        if not check_compressed_legendre_psd(first, second, factor):
            raise RuntimeError(f"prescribed pair p={prime}, q={root} failed the exact PSD test")
        jacobsthal = {
            jacobsthal_shifted_character_sum(prime, shift) for shift in range(1, prime)
        }
        if jacobsthal != {-1}:
            raise RuntimeError(f"Jacobsthal sums for p={prime} were {jacobsthal}; expected -1")
        candidates = uncompression_count(first, factor)
        certificates.append(
            {
                "p": prime,
                "q": root,
                "factor": factor,
                "uncompressed_length": length,
                "hadamard_order_if_uncompressible": 2 * length + 2,
                "first": list(first),
                "second": list(second),
                "row_sums": [sum(first), sum(second)],
                "combined_paf_zero_shift": check.zero_shift_value,
                "combined_paf_nonzero_shift": check.nonzero_shift_expected,
                "exact_psd_sum": 2 * length + 2,
                "jacobsthal_sums": sorted(jacobsthal),
                "uncompression_candidates_one_row": str(candidates),
                "uncompression_candidates_log10": round(log10(candidates), 2),
                "enumerated_here": (prime, root) == ENUMERATED,
            }
        )
    return certificates


def reproduce(output_directory: Path = DEFAULT_OUTPUT) -> dict[str, object]:
    """Certify the derived pairs and fully uncompress the p=3, q=3 case."""

    started_at = datetime.now(timezone.utc)
    started = perf_counter()
    output_directory.mkdir(parents=True, exist_ok=True)

    certificates = certify_prescribed_pairs()

    prime, root = ENUMERATED
    factor = root * root
    length = prime * factor
    order = 2 * length + 2
    first, second = structured_compressed_pair(prime, root)

    search_started = perf_counter()
    search = search_uncompressions(first, second, factor, collect=1)
    search_seconds = perf_counter() - search_started
    if not search.solutions:
        raise RuntimeError(f"no binary uncompression found at p={prime}, q={root}")

    pair_first, pair_second = search.solutions[0]
    paf_check = check_legendre_pair(pair_first, pair_second)
    sds_check = check_negative_support_sds(pair_first, pair_second)
    if not paf_check.ok or not sds_check.ok:
        raise RuntimeError("recovered pair failed an exact source-sequence check")
    if not check_legendre_psd_constraints(pair_first, pair_second):
        raise RuntimeError("recovered pair failed the exact cyclotomic PSD check")
    if compress(pair_first, prime) != first or compress(pair_second, prime) != second:
        raise RuntimeError("recovered pair does not compress to the prescribed rows")

    matrix = legendre_pair_to_hadamard(pair_first, pair_second)
    candidate = output_directory / f"H{order}.csv"
    _write_csv(matrix, candidate)
    direct = verify_direct(candidate, order=order)
    independent = verify_independent(candidate, order=order)
    direct_hash = write_direct_report(direct, output_directory / f"H{order}_verification.txt")
    independent_hash = write_independent_report(
        independent, output_directory / f"H{order}_verification_independent.txt"
    )
    if not direct.ok or not independent.ok:
        raise RuntimeError(
            f"H({order}) verification failed: direct={direct.message}; "
            f"independent={independent.message}"
        )

    metadata: dict[str, object] = {
        "status": (
            "derived-source certification plus complete factor-9 uncompression at "
            "p=3; not an order-668 result"
        ),
        "deterministic": True,
        "random_seed": None,
        "source_of_compressed_rows": (
            "derived from the quadratic-character formula and proved via the "
            "Jacobsthal sum; no publisher artifact was used"
        ),
        "indexing": "zero-based; PAF shift i -> i+s mod length",
        "compression": "length d*m to d by a[j+r*d], r=0..m-1",
        "prescribed_pair_certificates": certificates,
        "uncompression": {
            "p": prime,
            "q": root,
            "factor": factor,
            "length": length,
            "first_candidates_scanned": search.first_candidates,
            "second_candidates_scanned": search.second_candidates,
            "distinct_second_paf_vectors": search.distinct_second_vectors,
            "legendre_pairs_found": search.pairs_found,
            "search_seconds": round(search_seconds, 6),
            "recovered_first": _signs(pair_first),
            "recovered_second": _signs(pair_second),
            "sds_parameters": [
                length,
                sds_check.block_sizes[0],
                sds_check.block_sizes[1],
                sds_check.lambda_value,
            ],
            "matrix_order": order,
            "candidate": candidate.relative_to(REPOSITORY_ROOT).as_posix(),
            "candidate_sha256": direct.candidate_sha256,
            "direct_report_sha256": direct_hash,
            "independent_report_sha256": independent_hash,
            "dual_exact_verification": True,
        },
        "started_utc": started_at.isoformat(),
        "elapsed_seconds_this_run": round(perf_counter() - started, 6),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "logical_cpu_count": os.cpu_count(),
        "cpu_cores_used": 1,
        "peak_memory": "not instrumented; one PAF-vector table of about 10^5 entries",
        "command": "python -m scripts.reproduce_pq2_uncompression",
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
