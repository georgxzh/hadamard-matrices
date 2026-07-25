from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pytest

from src.verify_matrix import verify as verify_direct
from src.verify_matrix import write_report
from src.verify_matrix_independent import verify as verify_independent


VERIFIERS = (verify_direct, verify_independent)


def sylvester(order: int) -> list[list[int]]:
    matrix = [[1]]
    while len(matrix) < order:
        matrix = [row + row for row in matrix] + [row + [-x for x in row] for row in matrix]
    assert len(matrix) == order
    return matrix


def paley_type_i(prime: int) -> list[list[int]]:
    """Construct Paley type I of order prime + 1 for prime == 3 (mod 4)."""

    assert prime % 4 == 3
    residues = {x * x % prime for x in range(1, prime)}
    core: list[list[int]] = []
    for i in range(prime):
        row = []
        for j in range(prime):
            if i == j:
                row.append(-1)
            else:
                row.append(1 if (j - i) % prime in residues else -1)
        core.append(row)
    return [[1] * (prime + 1)] + [[1] + row for row in core]


def write_csv(path: Path, matrix: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle, lineterminator="\n").writerows(matrix)


@pytest.mark.parametrize("order", [1, 2, 4, 8, 16, 32])
@pytest.mark.parametrize("verifier", VERIFIERS)
def test_sylvester_matrices(order: int, verifier, tmp_path: Path) -> None:
    candidate = tmp_path / f"H{order}.csv"
    write_csv(candidate, sylvester(order))
    result = verifier(candidate, order)
    assert result.ok, result.message


@pytest.mark.parametrize("prime", [3, 11, 19])
@pytest.mark.parametrize("verifier", VERIFIERS)
def test_paley_matrices(prime: int, verifier, tmp_path: Path) -> None:
    matrix = paley_type_i(prime)
    candidate = tmp_path / f"H{prime + 1}.csv"
    write_csv(candidate, matrix)
    result = verifier(candidate, prime + 1)
    assert result.ok, result.message


@pytest.mark.parametrize("verifier", VERIFIERS)
def test_one_changed_entry_fails_exactly(verifier, tmp_path: Path) -> None:
    matrix = sylvester(8)
    matrix[3][5] *= -1
    candidate = tmp_path / "changed.csv"
    write_csv(candidate, matrix)
    result = verifier(candidate, 8)
    assert not result.ok
    assert "Gram entry" in result.message
    assert "expected 0" in result.message


@pytest.mark.parametrize("verifier", VERIFIERS)
def test_random_style_corruption_fails(verifier, tmp_path: Path) -> None:
    # Fixed coordinates keep this test deterministic while imitating multiple
    # random bit flips.
    matrix = sylvester(16)
    for row, column in ((1, 7), (6, 2), (13, 14)):
        matrix[row][column] *= -1
    candidate = tmp_path / "corrupt.csv"
    write_csv(candidate, matrix)
    assert not verifier(candidate, 16).ok


@pytest.mark.parametrize(
    "rows, expected_fragment",
    [
        ([[1, 1], [1]], "columns"),
        ([[1, 0], [1, -1]], "expected 1 or -1"),
        ([[1, 1]], "rows"),
        ([[1, 1], [1, -1], [1, -1]], "row"),
    ],
)
@pytest.mark.parametrize("verifier", VERIFIERS)
def test_malformed_csv(rows, expected_fragment: str, verifier, tmp_path: Path) -> None:
    candidate = tmp_path / "malformed.csv"
    write_csv(candidate, rows)
    result = verifier(candidate, 2)
    assert not result.ok
    assert expected_fragment in result.message


@pytest.mark.parametrize("verifier", VERIFIERS)
def test_non_integer_spelling_is_rejected(verifier, tmp_path: Path) -> None:
    candidate = tmp_path / "float_tokens.csv"
    write_csv(candidate, [["1.0", "1"], ["1", "-1"]])
    result = verifier(candidate, 2)
    assert not result.ok
    assert "expected 1 or -1" in result.message


@pytest.mark.parametrize("verifier", VERIFIERS)
def test_approximate_orthogonality_is_not_exact(verifier, tmp_path: Path) -> None:
    matrix = sylvester(64)
    matrix[17][23] *= -1

    # A loose floating-point-style normalized tolerance accepts this near miss:
    max_normalized_error = 0.0
    for i in range(64):
        for j in range(i):
            dot = sum(matrix[i][k] * matrix[j][k] for k in range(64))
            max_normalized_error = max(max_normalized_error, abs(dot) / 64.0)
    assert max_normalized_error <= 0.05

    candidate = tmp_path / "near_miss.csv"
    write_csv(candidate, matrix)
    assert not verifier(candidate, 64).ok


def test_report_and_hash_sidecar(tmp_path: Path) -> None:
    candidate = tmp_path / "H4.csv"
    write_csv(candidate, sylvester(4))
    result = verify_direct(candidate, 4)
    report = tmp_path / "verification.txt"
    report_hash = write_report(result, report)

    assert report_hash == hashlib.sha256(report.read_bytes()).hexdigest()
    sidecar = report.with_name(report.name + ".sha256").read_text(encoding="utf-8")
    assert result.candidate_sha256 in sidecar
    assert report_hash in sidecar
