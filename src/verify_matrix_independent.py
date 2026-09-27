"""Independent exact verifier using bit-packed rows and Hamming distance.

This module does not import the reference verifier.  It has a separate strict
parser and computes

    <r_i, r_j> = n - 2 * popcount(bits(r_i) XOR bits(r_j)).

That identity is exact: the popcount is the number of coordinates on which the
two ±1 rows disagree.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


DEFAULT_ORDER = 668


@dataclass(frozen=True)
class IndependentResult:
    ok: bool
    message: str
    candidate_sha256: str
    order: int

    def render(self) -> str:
        return "\n".join(
            (
                "verifier: bitpacked-hamming",
                f"status: {'PASS' if self.ok else 'FAIL'}",
                f"expected_order: {self.order}",
                f"candidate_sha256: {self.candidate_sha256}",
                f"detail: {self.message}",
                "",
            )
        )


def _file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(131_072):
            hasher.update(block)
    return hasher.hexdigest()


def _parse_rows(path: Path, order: int) -> tuple[list[int] | None, IndependentResult | None]:
    try:
        raw = path.read_text(encoding="utf-8-sig")
        candidate_hash = _file_hash(path)
    except (OSError, UnicodeError) as exc:
        return None, IndependentResult(False, f"cannot read candidate: {exc}", "unavailable", order)

    # The accepted candidate format is intentionally simple: comma-separated
    # unquoted integers.  Reject quote characters instead of reproducing the
    # csv-module parser used by the reference implementation.
    if '"' in raw:
        return None, IndependentResult(
            False, "quote characters are not permitted by the independent strict parser", candidate_hash, order
        )
    lines = raw.splitlines()
    if len(lines) != order:
        return None, IndependentResult(
            False, f"matrix has {len(lines)} rows; expected {order}", candidate_hash, order
        )

    packed_rows: list[int] = []
    for row_index, line in enumerate(lines, start=1):
        tokens = line.split(",")
        if len(tokens) != order:
            return None, IndependentResult(
                False,
                f"row {row_index} has {len(tokens)} columns; expected {order}",
                candidate_hash,
                order,
            )
        bits = 0
        for column_index, raw_token in enumerate(tokens, start=1):
            token = raw_token.strip()
            if token == "1":
                bits |= 1 << (column_index - 1)
            elif token != "-1":
                return None, IndependentResult(
                    False,
                    f"entry ({row_index},{column_index}) is {raw_token!r}; expected 1 or -1",
                    candidate_hash,
                    order,
                )
        packed_rows.append(bits)
    return packed_rows, None


def verify(path: Path | str, order: int = DEFAULT_ORDER) -> IndependentResult:
    candidate = Path(path)
    rows, error = _parse_rows(candidate, order)
    if error is not None:
        return error
    assert rows is not None
    candidate_hash = _file_hash(candidate)

    # Every parsed row has exactly ``order`` entries in {±1}, so every diagonal
    # Gram entry is order.  Check each unordered pair for exact orthogonality.
    for i in range(order):
        for j in range(i):
            disagreements = (rows[i] ^ rows[j]).bit_count()
            inner_product = order - 2 * disagreements
            if inner_product != 0:
                return IndependentResult(
                    False,
                    f"Gram entry ({i + 1},{j + 1}) is {inner_product}; expected 0",
                    candidate_hash,
                    order,
                )

    return IndependentResult(
        True,
        f"all {order * order} entries are ±1 and H H^T = {order} I_{order} exactly",
        candidate_hash,
        order,
    )


def write_report(result: IndependentResult, path: Path) -> str:
    """Write a deterministic report and candidate/report hash sidecar."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.render(), encoding="utf-8", newline="\n")
    report_hash = _file_hash(path)
    path.with_name(path.name + ".sha256").write_text(
        f"{result.candidate_sha256}  candidate\n{report_hash}  {path.name}\n",
        encoding="utf-8",
        newline="\n",
    )
    return report_hash


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--order", type=int, default=DEFAULT_ORDER)
    parser.add_argument("--report", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.order <= 0:
        raise SystemExit("--order must be positive")
    result = verify(args.candidate, args.order)
    print(result.render(), end="")
    if args.report is not None:
        print(f"report_sha256: {write_report(result, args.report)}")
        print(f"hash_sidecar: {args.report}.sha256")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
