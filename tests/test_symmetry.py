"""Exact tests for cyclic coordinate symmetries."""

from __future__ import annotations

from src.legendre import (
    compress,
    periodic_autocorrelation,
    quadratic_character,
    structured_compressed_pair,
)
from src.symmetry import (
    canonical_residue_translation,
    cyclic_translate,
    least_cyclic_period,
    multiplier_permute,
    residue_zero_bits,
    reverse_cyclic,
)
from src.uncompress import iter_uncompression_masks, mask_to_sequence


def _first_preimage(compressed: tuple[int, ...], factor: int) -> tuple[int, ...]:
    mask = next(iter_uncompression_masks(compressed, factor))
    return mask_to_sequence(mask, len(compressed) * factor)


def test_independent_translation_by_compressed_length_preserves_row_data() -> None:
    compressed, _ = structured_compressed_pair(5, 3)
    sequence = _first_preimage(compressed, 9)
    translated = cyclic_translate(sequence, 3 * 5)
    assert compress(translated, 5) == compressed
    assert [periodic_autocorrelation(translated, shift) for shift in range(45)] == [
        periodic_autocorrelation(sequence, shift) for shift in range(45)
    ]


def test_canonical_residue_translation_is_minimal_and_idempotent() -> None:
    compressed, _ = structured_compressed_pair(5, 3)
    sequence = _first_preimage(compressed, 9)
    canonical, offset = canonical_residue_translation(sequence, 5)
    bits = residue_zero_bits(canonical, 5)
    assert offset % 5 == 0
    assert bits == min(bits[step:] + bits[:step] for step in range(9))
    assert canonical_residue_translation(canonical, 5) == (canonical, 0)
    assert compress(canonical, 5) == compressed


def test_structured_factor_nine_residue_zero_word_has_full_period() -> None:
    compressed, _ = structured_compressed_pair(37, 3)
    sequence = _first_preimage(compressed, 9)
    bits = residue_zero_bits(sequence, 37)
    assert sum(bits) == 4
    assert least_cyclic_period(bits) == 9


def test_reversal_preserves_p37_compression_and_each_paf() -> None:
    compressed, _ = structured_compressed_pair(37, 3)
    sequence = _first_preimage(compressed, 9)
    reversed_sequence = reverse_cyclic(sequence)
    assert compress(reversed_sequence, 37) == compressed
    for shift in (0, 1, 9, 37, 111, 166, 332):
        assert periodic_autocorrelation(reversed_sequence, shift) == periodic_autocorrelation(
            sequence, shift
        )


def test_quadratic_residue_multiplier_preserves_structured_compressions() -> None:
    first, second = structured_compressed_pair(37, 3)
    first_sequence = _first_preimage(first, 9)
    second_sequence = _first_preimage(second, 9)
    multiplier = 4
    assert quadratic_character(multiplier, 37) == 1
    assert compress(multiplier_permute(first_sequence, multiplier), 37) == first
    assert compress(multiplier_permute(second_sequence, multiplier), 37) == second
    for shift in (1, 9, 37, 111):
        assert periodic_autocorrelation(
            multiplier_permute(first_sequence, multiplier), shift
        ) == periodic_autocorrelation(first_sequence, multiplier * shift)


def test_nonsquare_multiplier_plus_row_swap_preserves_prescribed_order() -> None:
    first, second = structured_compressed_pair(37, 3)
    first_sequence = _first_preimage(first, 9)
    second_sequence = _first_preimage(second, 9)
    multiplier = 2
    assert quadratic_character(multiplier, 37) == -1
    transformed_first = multiplier_permute(second_sequence, multiplier)
    transformed_second = multiplier_permute(first_sequence, multiplier)
    assert compress(transformed_first, 37) == first
    assert compress(transformed_second, 37) == second
