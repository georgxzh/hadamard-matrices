"""Exact tests for the Kharaghani--Tayfeh-Rezaie construction."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.order428 import (
    base_to_t_sequences,
    check_base_sequences,
    check_t_sequences,
    check_turyn_type,
    hadamard_from_turyn_type,
    nonperiodic_autocorrelation,
    published_tt4,
    published_tt36,
    turyn_type_to_base,
)
from src.verify_matrix import verify as verify_direct
from src.verify_matrix_independent import verify as verify_independent


def _write_matrix(path: Path, matrix: list[list[int]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerows(matrix)


def test_nonperiodic_autocorrelation_uses_zero_padding() -> None:
    sequence = (1, -1, 1)
    assert nonperiodic_autocorrelation(sequence, 0) == 3
    assert nonperiodic_autocorrelation(sequence, 1) == -2
    assert nonperiodic_autocorrelation(sequence, 2) == 1
    assert nonperiodic_autocorrelation(sequence, 3) == 0
    with pytest.raises(ValueError, match="nonnegative"):
        nonperiodic_autocorrelation(sequence, -1)


def test_published_tt36_transcription_and_all_shifts() -> None:
    sequences = published_tt36()
    assert tuple(map(len, sequences)) == (36, 36, 36, 35)
    assert tuple(map(sum, sequences)) == (0, 6, 8, 5)
    check = check_turyn_type(sequences)
    assert check.ok
    assert check.checked_shifts == 35


def test_tt36_intermediate_invariants() -> None:
    base = turyn_type_to_base(published_tt36())
    assert tuple(map(len, base)) == (71, 71, 36, 36)
    assert check_base_sequences(base).ok

    t_sequences = base_to_t_sequences(base)
    assert tuple(map(len, t_sequences)) == (107, 107, 107, 107)
    assert tuple(sum(value != 0 for value in sequence) for sequence in t_sequences) == (
        36,
        35,
        19,
        17,
    )
    assert check_t_sequences(t_sequences).ok


def test_corrupted_tt36_is_rejected_at_exact_shift() -> None:
    sequences = list(published_tt36())
    corrupted = list(sequences[0])
    corrupted[17] *= -1
    sequences[0] = tuple(corrupted)
    check = check_turyn_type(sequences)
    assert not check.ok
    assert check.failure_shift is not None
    assert check.failure_value != 0


def test_small_published_tt4_produces_exact_h44(tmp_path: Path) -> None:
    sequences = published_tt4()
    assert check_turyn_type(sequences).ok
    matrix = hadamard_from_turyn_type(sequences)
    assert len(matrix) == 44
    assert all(len(row) == 44 for row in matrix)

    candidate = tmp_path / "H44.csv"
    _write_matrix(candidate, matrix)
    assert verify_direct(candidate, order=44).ok
    assert verify_independent(candidate, order=44).ok


def test_complete_tt36_pipeline_passes_both_exact_verifiers(tmp_path: Path) -> None:
    matrix = hadamard_from_turyn_type(published_tt36())
    candidate = tmp_path / "H428.csv"
    _write_matrix(candidate, matrix)
    direct = verify_direct(candidate, order=428)
    independent = verify_independent(candidate, order=428)
    assert direct.ok, direct.message
    assert independent.ok, independent.message
    assert direct.candidate_sha256 == independent.candidate_sha256
