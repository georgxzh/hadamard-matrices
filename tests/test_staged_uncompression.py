"""Tests for the exact factor-three branch model."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.legendre import (
    compress,
    decode_signs,
    published_structured_legendre_pair_45,
    structured_compressed_pair,
)
from src.staged_uncompression import FactorThreeBranch
from src.symmetry import canonical_residue_translation, least_cyclic_period, residue_bits
from src.uncompress import uncompression_count


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _lp27() -> tuple[tuple[int, ...], tuple[int, ...]]:
    record = json.loads(
        (REPOSITORY_ROOT / "results" / "pb_uncompression" / "lp27_witness.json").read_text(
            encoding="utf-8"
        )
    )
    return decode_signs(record["first"]), decode_signs(record["second"])


@pytest.mark.parametrize(
    ("prime", "factory", "expected_counts"),
    [
        (3, _lp27, (6_561, 729)),
        (5, published_structured_legendre_pair_45, (59_049, 1_594_323)),
    ],
)
def test_factor_three_branch_accepts_known_witnesses(
    prime: int, factory, expected_counts: tuple[int, int]
) -> None:
    first, second = factory()
    prescribed = structured_compressed_pair(prime, 3)
    intermediate = (compress(first, 3 * prime), compress(second, 3 * prime))
    branch = FactorThreeBranch(*prescribed, *intermediate)
    assert branch.final_length == 9 * prime
    assert tuple(uncompression_count(row, 3) for row in intermediate) == expected_counts
    assert branch.model().first_failed_constraint(first, second) is None

    residues = branch.canonical_residues
    canonical_first, _ = canonical_residue_translation(first, 3 * prime, residues[0])
    canonical_second, _ = canonical_residue_translation(second, 3 * prime, residues[1])
    assert branch.model(canonical_translations=True).first_failed_constraint(
        canonical_first, canonical_second
    ) is None
    assert all(
        least_cyclic_period(residue_bits(row, 3 * prime, residue)) == 3
        for row, residue in zip((first, second), residues, strict=True)
    )


def test_factor_three_branch_rejects_an_invalid_intermediate_pair() -> None:
    first, second = published_structured_legendre_pair_45()
    prescribed = structured_compressed_pair(5, 3)
    intermediate_first = list(compress(first, 15))
    intermediate_second = compress(second, 15)
    intermediate_first[0] += 2
    with pytest.raises(ValueError, match="wrong second compression"):
        FactorThreeBranch(
            *prescribed,
            intermediate_first,
            intermediate_second,
        )
