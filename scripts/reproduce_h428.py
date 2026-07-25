"""Deterministically reconstruct and exactly verify the published H(428)."""

from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

from src.order428 import (
    base_to_t_sequences,
    check_base_sequences,
    check_t_sequences,
    check_turyn_type,
    published_tt36,
    t_sequences_to_hadamard,
    turyn_type_to_base,
)
from src.verify_matrix import sha256_file
from src.verify_matrix import verify as verify_direct
from src.verify_matrix import write_report as write_direct_report
from src.verify_matrix_independent import verify as verify_independent
from src.verify_matrix_independent import write_report as write_independent_report


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "H428.csv"


def write_csv(matrix: list[list[int]], path: Path) -> None:
    """Write the complete matrix in a canonical CSV representation."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerows(matrix)


def reproduce(output: Path = DEFAULT_OUTPUT) -> dict[str, object]:
    """Run every exact stage, write H428, and invoke both final verifiers."""

    started = perf_counter()
    tt = published_tt36()
    tt_check = check_turyn_type(tt)
    if not tt_check.ok:
        raise RuntimeError(tt_check.message)

    base = turyn_type_to_base(tt)
    base_check = check_base_sequences(base)
    if not base_check.ok:
        raise RuntimeError(base_check.message)

    t_sequences = base_to_t_sequences(base)
    t_check = check_t_sequences(t_sequences)
    if not t_check.ok:
        raise RuntimeError(t_check.message)

    matrix = t_sequences_to_hadamard(t_sequences)
    write_csv(matrix, output)

    direct = verify_direct(output, order=428)
    independent = verify_independent(output, order=428)
    direct_report = output.with_name("H428_verification.txt")
    independent_report = output.with_name("H428_verification_independent.txt")
    direct_report_hash = write_direct_report(direct, direct_report)
    independent_report_hash = write_independent_report(independent, independent_report)
    if not direct.ok or not independent.ok:
        raise RuntimeError(
            f"final verification failed: direct={direct.message}; independent={independent.message}"
        )

    elapsed = perf_counter() - started
    metadata: dict[str, object] = {
        "construction": "Kharaghani--Tayfeh-Rezaie TT(36) -> BS(71,71,36,36) -> T(107) -> GS H(428)",
        "deterministic": True,
        "random_seed": None,
        "indexing": "zero-based; published signs read left-to-right",
        "correlation": "exact nonperiodic integer autocorrelation",
        "source_sequence_lengths": [len(sequence) for sequence in tt],
        "source_sequence_sums": [sum(sequence) for sequence in tt],
        "base_sequence_lengths": [len(sequence) for sequence in base],
        "t_sequence_lengths": [len(sequence) for sequence in t_sequences],
        "matrix_shape": [len(matrix), len(matrix[0])],
        "candidate_sha256": sha256_file(output),
        "direct_report_sha256": direct_report_hash,
        "independent_report_sha256": independent_report_hash,
        "elapsed_seconds_this_run": round(elapsed, 6),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "logical_cpu_count": __import__("os").cpu_count(),
        "cpu_cores_used": 1,
        "peak_memory": "not measured; matrix is 428 x 428 Python integers",
        "storage_bytes": sum(
            path.stat().st_size
            for path in (
                output,
                direct_report,
                independent_report,
                direct_report.with_name(direct_report.name + ".sha256"),
                independent_report.with_name(independent_report.name + ".sha256"),
            )
        ),
        "command": "python -m scripts.reproduce_h428",
    }
    metadata_path = output.with_name("H428_metadata.json")
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    metadata = reproduce(args.output.resolve())
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
