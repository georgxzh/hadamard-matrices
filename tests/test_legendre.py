"""Exact regression tests for the binary Legendre-pair framework."""

from __future__ import annotations

import csv
from math import cos, pi, sin
from pathlib import Path

import pytest

from src.legendre import (
    ExactCyclotomicValue,
    check_compression_paf_identity,
    check_legendre_compression_constants,
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    cyclic_convolution,
    cyclotomic_polynomial,
    decode_signs,
    difference_multiplicities,
    evaluate_cyclotomic,
    exact_psd,
    exact_psd_at_third_root,
    exact_psd_sum,
    legendre_pair_to_hadamard,
    normalize_legendre_pair,
    periodic_autocorrelation,
    periodic_autocorrelations,
    published_legendre_pair_3,
    published_legendre_pair_5,
    published_legendre_pair_7,
    published_legendre_pair_27,
)
from src.verify_matrix import verify as verify_direct
from src.verify_matrix_independent import verify as verify_independent


def _write_matrix(path: Path, matrix: list[list[int]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerows(matrix)


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [
        ((1, -1, 1), (3, -1, -1)),
        ((2, -1, 3, 0), (14, -5, 12, -5)),
    ],
)
def test_periodic_autocorrelation_all_shifts(
    sequence: tuple[int, ...], expected: tuple[int, ...]
) -> None:
    assert periodic_autocorrelations(sequence) == expected
    assert tuple(periodic_autocorrelation(sequence, shift) for shift in range(len(sequence))) == expected
    assert periodic_autocorrelation(sequence, -1) == expected[-1]


def test_cyclic_convolution_uses_zero_based_modular_indices() -> None:
    assert cyclic_convolution((1, 2, 3), (4, 5, 6)) == (31, 31, 28)
    with pytest.raises(ValueError, match="length mismatch"):
        cyclic_convolution((1,), (1, 2))


@pytest.mark.parametrize(
    "factory",
    [
        published_legendre_pair_3,
        published_legendre_pair_5,
        published_legendre_pair_7,
        published_legendre_pair_27,
    ],
)
def test_published_pairs_satisfy_paf_psd_and_sds(factory) -> None:
    first, second = factory()
    check = check_legendre_pair(first, second)
    assert check.ok
    assert check.checked_shifts == len(first) - 1
    assert check_legendre_psd_constraints(first, second)
    assert check_negative_support_sds(first, second).ok
    assert exact_psd_sum(first, second, 0).integer_value == 2


def test_corruption_fails_exact_paf_psd_and_sds() -> None:
    first, second = published_legendre_pair_7()
    corrupted = list(first)
    corrupted[2] *= -1
    paf_check = check_legendre_pair(corrupted, second)
    assert not paf_check.ok
    assert paf_check.failure_shift is not None
    assert not check_legendre_psd_constraints(corrupted, second)
    assert not check_negative_support_sds(corrupted, second).ok


def test_independent_row_negation_normalizes_without_changing_paf() -> None:
    first, second = published_legendre_pair_5()
    normalized = normalize_legendre_pair(tuple(-value for value in first), second)
    assert normalized == (first, second)
    assert check_legendre_pair(*normalized).ok


@pytest.mark.parametrize(
    ("factory", "order"),
    [
        (published_legendre_pair_3, 8),
        (published_legendre_pair_5, 12),
        (published_legendre_pair_7, 16),
        (published_legendre_pair_27, 56),
    ],
)
def test_published_pairs_construct_dual_verified_hadamard_matrices(
    factory, order: int, tmp_path: Path
) -> None:
    matrix = legendre_pair_to_hadamard(*factory())
    assert len(matrix) == order
    assert all(len(row) == order for row in matrix)
    candidate = tmp_path / f"H{order}.csv"
    _write_matrix(candidate, matrix)
    assert verify_direct(candidate, order=order).ok
    assert verify_independent(candidate, order=order).ok


def test_negative_support_difference_parameters_are_exact() -> None:
    first, second = published_legendre_pair_7()
    check = check_negative_support_sds(first, second)
    assert check.block_sizes == (3, 3)
    assert check.lambda_value == 2
    assert difference_multiplicities((1, 3), 5) == (2, 0, 1, 1, 0)


@pytest.mark.parametrize(
    ("order", "expected"),
    [
        (1, (-1, 1)),
        (2, (1, 1)),
        (3, (1, 1, 1)),
        (4, (1, 0, 1)),
        (9, (1, 0, 0, 1, 0, 0, 1)),
        (37, tuple([1] * 37)),
    ],
)
def test_cyclotomic_polynomials(order: int, expected: tuple[int, ...]) -> None:
    assert cyclotomic_polynomial(order) == expected


def test_exact_psd_representation_and_numeric_diagnostic_agree() -> None:
    sequence = decode_signs("++-+-")
    at_zero = exact_psd(sequence, 0)
    assert at_zero == ExactCyclotomicValue(1, (1,))
    at_one = exact_psd(sequence, 1)
    assert at_one.order == 5
    direct = abs(
        sum(
            value
            * complex(
                cos(2 * pi * index / 5),
                sin(2 * pi * index / 5),
            )
            for index, value in enumerate(sequence)
        )
    ) ** 2
    assert evaluate_cyclotomic(at_one).real == pytest.approx(direct, abs=1e-10)


def test_exact_third_root_psd_identity() -> None:
    sequence = published_legendre_pair_3()[0]
    assert exact_psd_at_third_root(sequence) == 4
    exact = exact_psd(sequence, 1)
    assert exact.is_integer
    assert exact.integer_value == 4


def test_generic_compression_identity_and_binary_range() -> None:
    sequence = tuple(1 if (index * index + 3 * index + 1) % 7 < 3 else -1 for index in range(45))
    for output_length in (3, 5, 9, 15):
        compressed = compress(sequence, output_length)
        factor = len(sequence) // output_length
        assert all(-factor <= value <= factor and value % 2 == factor % 2 for value in compressed)
        assert sum(compressed) == sum(sequence)
        assert check_compression_paf_identity(sequence, output_length)


def test_length_333_compressions_and_composition_are_exact() -> None:
    sequence = tuple(1 if (index * index + 5 * index + 2) % 11 < 5 else -1 for index in range(333))
    compression_3 = compress(sequence, 3)
    compression_9 = compress(sequence, 9)
    compression_37 = compress(sequence, 37)
    assert tuple(map(len, (compression_3, compression_9, compression_37))) == (3, 9, 37)
    assert compression_3 == compress(compression_9, 3)
    for output_length in (3, 9, 37):
        assert check_compression_paf_identity(sequence, output_length)
        for frequency in range(1, output_length):
            original_frequency = frequency * (333 // output_length)
            assert exact_psd(sequence, original_frequency) == exact_psd(
                compress(sequence, output_length), frequency
            )


@pytest.mark.parametrize(
    "factory",
    [published_legendre_pair_3, published_legendre_pair_5],
)
def test_legendre_compression_constants(factory) -> None:
    first, second = factory()
    assert check_legendre_compression_constants(first, second, 1)
    assert check_legendre_compression_constants(first, second, len(first))


def test_published_length_27_pair_has_exact_3_and_9_compressions() -> None:
    first, second = published_legendre_pair_27()
    assert compress(first, 3) == (1, 1, -1)
    assert compress(second, 3) == (-3, 5, -1)
    assert compress(first, 9) == (-1, 1, 1, 3, 1, -3, -1, -1, 1)
    assert compress(second, 9) == (-1, -1, 1, -1, 3, -1, -1, 3, -1)
    assert check_legendre_compression_constants(first, second, 3)
    assert check_legendre_compression_constants(first, second, 9)
    assert exact_psd_at_third_root(compress(first, 3)) == 4
    assert exact_psd_at_third_root(compress(second, 3)) == 52
    assert exact_psd_sum(first, second, 9).integer_value == 56


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="expected -1 or 1"):
        check_legendre_pair((1, 0, -1), (1, 1, -1))
    with pytest.raises(ValueError, match="does not divide"):
        compress((1, -1, 1), 2)
    with pytest.raises(ValueError, match="repeated"):
        difference_multiplicities((1, 1), 3)
