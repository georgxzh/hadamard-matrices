"""Exact reference verifier for a Hadamard matrix stored as CSV.

This implementation parses the entire matrix and checks row inner products
directly with Python integers.  The independent verifier deliberately uses a
different parser and a bit-packed Hamming-distance calculation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


DEFAULT_ORDER = 668


@dataclass(frozen=True)
class VerificationResult:
    """The outcome of an exact verification."""

    ok: bool
    message: str
    candidate_sha256: str
    order: int

    def render(self, verifier: str = "direct-integer") -> str:
        status = "PASS" if self.ok else "FAIL"
        return "\n".join(
            (
                f"verifier: {verifier}",
                f"status: {status}",
                f"expected_order: {self.order}",
                f"candidate_sha256: {self.candidate_sha256}",
                f"detail: {self.message}",
                "",
            )
        )


def sha256_file(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of *path*."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _failure(path: Path, order: int, message: str) -> VerificationResult:
    try:
        candidate_hash = sha256_file(path)
    except OSError:
        candidate_hash = "unavailable"
    return VerificationResult(False, message, candidate_hash, order)


def read_matrix(path: Path, order: int = DEFAULT_ORDER) -> tuple[list[list[int]] | None, VerificationResult | None]:
    """Strictly read an ``order`` by ``order`` CSV matrix.

    Cells may contain surrounding whitespace, but after stripping must be the
    literal token ``1`` or ``-1``.  Empty rows and surplus rows are errors.
    """

    try:
        candidate_hash = sha256_file(path)
    except OSError as exc:
        return None, VerificationResult(False, f"cannot read candidate: {exc}", "unavailable", order)

    rows: list[list[int]] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, strict=True)
            for row_number, raw_row in enumerate(reader, start=1):
                if row_number > order:
                    return None, VerificationResult(
                        False,
                        f"row count exceeds {order}; first surplus row is {row_number}",
                        candidate_hash,
                        order,
                    )
                if len(raw_row) != order:
                    return None, VerificationResult(
                        False,
                        f"row {row_number} has {len(raw_row)} columns; expected {order}",
                        candidate_hash,
                        order,
                    )
                parsed: list[int] = []
                for column_number, token in enumerate(raw_row, start=1):
                    stripped = token.strip()
                    if stripped not in {"1", "-1"}:
                        return None, VerificationResult(
                            False,
                            f"entry ({row_number},{column_number}) is {token!r}; expected 1 or -1",
                            candidate_hash,
                            order,
                        )
                    parsed.append(1 if stripped == "1" else -1)
                rows.append(parsed)
    except (OSError, UnicodeError, csv.Error) as exc:
        return None, VerificationResult(False, f"CSV parse failure: {exc}", candidate_hash, order)

    if len(rows) != order:
        return None, VerificationResult(
            False,
            f"matrix has {len(rows)} rows; expected {order}",
            candidate_hash,
            order,
        )
    return rows, None


def verify(path: Path | str, order: int = DEFAULT_ORDER) -> VerificationResult:
    """Verify all entries and all entries of ``H H^T`` using Python integers."""

    candidate = Path(path)
    matrix, error = read_matrix(candidate, order)
    if error is not None:
        return error
    assert matrix is not None
    candidate_hash = sha256_file(candidate)

    for i, row_i in enumerate(matrix):
        diagonal = sum(value * value for value in row_i)
        if diagonal != order:
            return VerificationResult(
                False,
                f"Gram entry ({i + 1},{i + 1}) is {diagonal}; expected {order}",
                candidate_hash,
                order,
            )
        for j in range(i):
            row_j = matrix[j]
            inner_product = sum(a * b for a, b in zip(row_i, row_j, strict=True))
            if inner_product != 0:
                return VerificationResult(
                    False,
                    f"Gram entry ({i + 1},{j + 1}) is {inner_product}; expected 0",
                    candidate_hash,
                    order,
                )

    return VerificationResult(
        True,
        f"all {order * order} entries are ±1 and H H^T = {order} I_{order} exactly",
        candidate_hash,
        order,
    )


def write_report(result: VerificationResult, report_path: Path, verifier: str = "direct-integer") -> str:
    """Write the report and a sidecar containing hashes; return report SHA-256.

    A file cannot contain its own cryptographic hash without a circular
    definition.  Therefore the report contains the candidate hash, while the
    adjacent ``.sha256`` sidecar records hashes of both completed files.
    """

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(result.render(verifier), encoding="utf-8", newline="\n")
    report_hash = sha256_file(report_path)
    sidecar = report_path.with_name(report_path.name + ".sha256")
    sidecar.write_text(
        f"{result.candidate_sha256}  candidate\n{report_hash}  {report_path.name}\n",
        encoding="utf-8",
        newline="\n",
    )
    return report_hash


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="CSV file to verify")
    parser.add_argument("--order", type=int, default=DEFAULT_ORDER, help="expected order (default: 668)")
    parser.add_argument("--report", type=Path, help="write a verification report and SHA-256 sidecar")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.order <= 0:
        raise SystemExit("--order must be positive")
    result = verify(args.candidate, args.order)
    print(result.render(), end="")
    if args.report is not None:
        report_hash = write_report(result, args.report)
        print(f"report_sha256: {report_hash}")
        print(f"hash_sidecar: {args.report}.sha256")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
