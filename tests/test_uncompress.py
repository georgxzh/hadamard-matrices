"""Exact regression tests for the derived pq^2 pair and its uncompression."""

from __future__ import annotations

from math import comb

import pytest

from src.legendre import (
    check_compressed_legendre_constants,
    check_compressed_legendre_psd,
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    jacobsthal_shifted_character_sum,
    legendre_pair_to_hadamard,
    quadratic_character,
    structured_compressed_pair,
)
from src.uncompress import (
    iter_uncompression_masks,
    mask_to_sequence,
    paf_signature,
    search_uncompressions,
    uncompression_count,
)


PRESCRIBED = [(3, 3), (5, 3), (7, 3), (11, 3), (13, 3), (37, 3), (5, 5), (7, 5)]


def test_quadratic_character_matches_squares_modulo_seven() -> None:
    residues = {pow(value, 2, 7) for value in range(1, 7)}
    for value in range(1, 7):
        assert quadratic_character(value, 7) == (1 if value in residues else -1)
    assert quadratic_character(7, 7) == 0
    assert quadratic_character(-1, 7) == quadratic_character(6, 7)


@pytest.mark.parametrize("prime", [3, 5, 7, 11, 13, 37])
def test_character_sum_vanishes_and_jacobsthal_sum_is_minus_one(prime: int) -> None:
    assert sum(quadratic_character(value, prime) for value in range(prime)) == 0
    assert jacobsthal_shifted_character_sum(prime, 0) == prime - 1
    for shift in range(1, prime):
        assert jacobsthal_shifted_character_sum(prime, shift) == -1


@pytest.mark.parametrize("prime", [4, 9, 15, 2])
def test_quadratic_character_rejects_non_odd_primes(prime: int) -> None:
    with pytest.raises(ValueError):
        quadratic_character(1, prime)


@pytest.mark.parametrize(("prime", "root"), PRESCRIBED)
def test_prescribed_pair_satisfies_every_exact_condition(prime: int, root: int) -> None:
    first, second = structured_compressed_pair(prime, root)
    factor = root * root
    length = prime * factor

    assert len(first) == len(second) == prime
    assert first[0] == second[0] == 1
    assert all(left == -right for left, right in zip(first[1:], second[1:]))
    assert sum(first) == sum(second) == 1

    check = check_compressed_legendre_constants(first, second, factor)
    assert check.ok, check.message
    assert check.uncompressed_length == length
    assert check.zero_shift_value == 2 * length - 2 * (factor - 1)
    assert check.nonzero_shift_expected == -2 * factor
    assert check_compressed_legendre_psd(first, second, factor)


def test_prescribed_pair_at_p37_q3_matches_the_audited_length333_constants() -> None:
    """The independently tabulated output-length-37 constants are 650 and -18."""

    first, second = structured_compressed_pair(37, 3)
    check = check_compressed_legendre_constants(first, second, 9)
    assert check.ok
    assert check.uncompressed_length == 333
    assert check.zero_shift_value == 650
    assert check.nonzero_shift_expected == -18
    assert check_compressed_legendre_psd(first, second, 9)


def test_compressed_checker_rejects_perturbations() -> None:
    first, second = structured_compressed_pair(7, 3)
    broken = (first[0] + 2, first[1] - 2, *first[2:])
    assert not check_compressed_legendre_constants(broken, second, 9).ok

    out_of_range = (11, *first[1:])
    assert not check_compressed_legendre_constants(out_of_range, second, 9).ok

    wrong_parity = (2, *first[1:])
    assert not check_compressed_legendre_constants(wrong_parity, second, 9).ok


def test_uncompression_count_matches_enumeration_on_a_small_case() -> None:
    compressed = (1, 3, -3)
    assert uncompression_count(compressed, 3) == comb(3, 1) * comb(3, 0) * comb(3, 3)
    masks = list(iter_uncompression_masks(compressed, 3))
    assert len(masks) == uncompression_count(compressed, 3)
    assert len(set(masks)) == len(masks)
    for mask in masks:
        assert compress(mask_to_sequence(mask, 9), 3) == compressed


def test_paf_signature_agrees_with_direct_autocorrelation() -> None:
    from src.legendre import periodic_autocorrelation

    for mask in list(iter_uncompression_masks((1, 3, -3), 3))[:8]:
        sequence = mask_to_sequence(mask, 9)
        expected = tuple(periodic_autocorrelation(sequence, shift) for shift in range(1, 5))
        assert paf_signature(mask, 9) == expected


def test_uncompression_count_for_p37_q3_is_astronomically_large() -> None:
    first, _ = structured_compressed_pair(37, 3)
    assert uncompression_count(first, 9) > 10**70


def test_factor_nine_uncompression_at_p3_yields_a_verified_legendre_pair() -> None:
    first, second = structured_compressed_pair(3, 3)
    search = search_uncompressions(first, second, 9, collect=1)

    assert search.uncompressed_length == 27
    assert search.first_candidates == search.second_candidates == uncompression_count(first, 9)
    assert search.matched_first_candidates == 7_614
    assert search.ordered_pairs_found == 77_274
    assert search.solutions

    left, right = search.solutions[0]
    assert compress(left, 3) == first
    assert compress(right, 3) == second
    assert check_legendre_pair(left, right).ok
    assert check_negative_support_sds(left, right).ok
    assert check_legendre_psd_constraints(left, right)

    matrix = legendre_pair_to_hadamard(left, right)
    assert len(matrix) == 56
    for row_index, row in enumerate(matrix):
        assert len(row) == 56
        for column_index, other in enumerate(matrix):
            product = sum(a * b for a, b in zip(row, other))
            assert product == (56 if row_index == column_index else 0)


def test_search_limit_bounds_the_scan() -> None:
    first, second = structured_compressed_pair(3, 3)
    search = search_uncompressions(first, second, 9, limit=500, collect=0)
    assert search.first_candidates == 500
    assert search.second_candidates == 500
    assert search.solutions == ()
