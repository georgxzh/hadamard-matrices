"""Tests for the exact factor-three branch model."""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path

import pytest

from src.legendre import (
    compress,
    decode_signs,
    published_structured_legendre_pair_45,
    structured_compressed_pair,
)
from src.staged_uncompression import (
    FactorThreeBranch,
    IntermediatePBModel,
    canonical_intermediate_translation,
    canonical_intermediate_residue_translation,
    enumerate_intermediate_pairs,
    intermediate_signature,
    intermediate_uncompression_count,
    iter_intermediate_rows,
    search_intermediate_pairs,
)
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
    projected = branch.model(projected_correlations=True)
    assert projected.correlation_shifts == tuple(range(1, 3 * prime))
    assert projected.first_failed_constraint(first, second) is None

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


def test_intermediate_model_has_derived_exact_counts() -> None:
    p3 = IntermediatePBModel(*structured_compressed_pair(3, 3))
    assert vars(p3.stats) == {
        "prescribed_length": 3,
        "intermediate_length": 9,
        "base_variables": 36,
        "square_xor_variables": 18,
        "product_variables": 288,
        "variables": 342,
        "square_xor_inequalities": 72,
        "product_inequalities": 864,
        "compression_equalities": 6,
        "zero_shift_equalities": 1,
        "correlation_equalities": 4,
        "symmetry_inequalities": 0,
        "constraint_records": 947,
        "normalized_inequalities": 958,
    }
    assert sum(1 for _ in p3.iter_constraints()) == p3.stats.constraint_records

    p5 = IntermediatePBModel(*structured_compressed_pair(5, 3))
    assert p5.stats.intermediate_length == 15
    assert p5.stats.base_variables == 60
    assert p5.stats.square_xor_variables == 30
    assert p5.stats.product_variables == 840
    assert p5.stats.variables == 930
    assert p5.stats.square_xor_inequalities == 120
    assert p5.stats.product_inequalities == 2_520
    assert p5.stats.constraint_records == 2_658
    assert p5.stats.normalized_inequalities == 2_676


def test_projected_branch_models_have_derived_exact_counts() -> None:
    for prime, factory, expected in (
        (3, _lp27, (486, 432, 1_754, 1_780)),
        (5, published_structured_legendre_pair_45, (1_350, 1_260, 5_084, 5_128)),
    ):
        first, second = factory()
        prescribed = structured_compressed_pair(prime, 3)
        intermediate = compress(first, 3 * prime), compress(second, 3 * prime)
        model = FactorThreeBranch(*prescribed, *intermediate).model(
            projected_correlations=True
        )
        assert (
            model.stats.variables,
            model.stats.xor_variables,
            model.stats.constraint_records,
            model.stats.normalized_inequalities,
        ) == expected
        assert sum(1 for _ in model.iter_constraints()) == model.stats.constraint_records
        assert model.first_failed_constraint(first, second) is None


@pytest.mark.parametrize(
    ("prime", "factory"),
    [(3, _lp27), (5, published_structured_legendre_pair_45)],
)
def test_known_intermediate_pair_is_an_exact_model_witness(prime: int, factory) -> None:
    binary_first, binary_second = factory()
    prescribed = structured_compressed_pair(prime, 3)
    intermediate = (
        compress(binary_first, 3 * prime),
        compress(binary_second, 3 * prime),
    )
    model = IntermediatePBModel(*prescribed)
    constraints = tuple(model.iter_constraints())
    assert model.first_failed_constraint(*intermediate, constraints=constraints) is None
    broken = (intermediate[0][:-1] + (-intermediate[0][-1],), intermediate[1])
    assert model.first_failed_constraint(*broken, constraints=constraints) is not None


def test_intermediate_row_enumeration_is_exact_and_deterministic() -> None:
    first, second = structured_compressed_pair(3, 3)
    assert intermediate_uncompression_count(first) == 1_200
    assert intermediate_uncompression_count(second) == 1_200
    rows = tuple(iter_intermediate_rows(first))
    assert len(rows) == 1_200
    assert len(set(rows)) == 1_200
    assert all(compress(row, 3) == first for row in rows)
    assert rows == tuple(iter_intermediate_rows(first))
    assert (
        intermediate_uncompression_count(structured_compressed_pair(5, 3)[0])
        == 120_000
    )


def test_p3_intermediate_search_is_exhaustive_and_model_checked() -> None:
    prescribed = structured_compressed_pair(3, 3)
    search = search_intermediate_pairs(*prescribed)
    assert search.first_candidates == 1_200
    assert search.second_candidates == 1_200
    assert search.first_signatures == 282
    assert search.second_signatures == 282
    assert search.signature_matches == 25
    assert search.ordered_pairs == 792
    assert len(search.representative_pairs) == 25
    model = IntermediatePBModel(*prescribed)
    assert all(
        model.first_failed_constraint(*pair) is None
        for pair in search.representative_pairs
    )


def test_published_p5_intermediate_signature_has_an_exact_complement() -> None:
    first, second = published_structured_legendre_pair_45()
    prescribed = structured_compressed_pair(5, 3)
    intermediate = compress(first, 15), compress(second, 15)
    target = (86, *([-6] * 7))
    assert tuple(
        left + right
        for left, right in zip(
            intermediate_signature(intermediate[0]),
            intermediate_signature(intermediate[1]),
            strict=True,
        )
    ) == target
    assert IntermediatePBModel(*prescribed).first_failed_constraint(*intermediate) is None


def test_p5_intermediate_search_recovers_the_published_branch() -> None:
    prescribed = structured_compressed_pair(5, 3)
    search = search_intermediate_pairs(*prescribed)
    assert search.first_candidates == 120_000
    assert search.second_candidates == 120_000
    assert search.first_signatures == 18_348
    assert search.second_signatures == 18_348
    assert search.signature_matches == 208
    assert search.ordered_pairs == 10_476

    first, second = published_structured_legendre_pair_45()
    published_intermediate = compress(first, 15), compress(second, 15)
    assert published_intermediate in search.representative_pairs


def test_complete_p5_pairs_split_into_free_translation_orbits() -> None:
    prescribed = structured_compressed_pair(5, 3)
    pairs = enumerate_intermediate_pairs(*prescribed)
    canonical = enumerate_intermediate_pairs(*prescribed, canonical_translations=True)
    assert len(pairs) == 10_476
    assert len(canonical) == 1_164
    assert len(pairs) == 9 * len(canonical)
    model = IntermediatePBModel(*prescribed, canonical_translations=True)
    anchored = Counter(model.canonicalize_pair(*pair) for pair in pairs)
    assert len(anchored) == 1_164
    assert set(anchored.values()) == {9}
    symmetry = tuple(model.iter_symmetry_constraints())
    for pair in pairs:
        assignment = {
            model.bit_variable(r, i, bit): (((3 - value) // 2) >> bit) & 1
            for r, row in enumerate(pair) for i, value in enumerate(row)
            for bit in (0, 1)
        }
        assert all(c.satisfied_by(assignment) for c in symmetry) == (pair in anchored)
    assert Counter(
        tuple(sum(abs(value) == 1 for value in row) for row in pair)
        for pair in pairs
    ) == {
        (9, 14): 162,
        (10, 13): 1_620,
        (11, 12): 3_456,
        (12, 11): 3_456,
        (13, 10): 1_620,
        (14, 9): 162,
    }

    ranked = sorted(
        canonical,
        key=lambda pair: (
            sum(uncompression_count(row, 3) for row in pair),
            max(uncompression_count(row, 3) for row in pair),
            pair,
        ),
    )
    first, second = ranked[0]
    assert (uncompression_count(first, 3), uncompression_count(second, 3)) == (
        177_147,
        531_441,
    )
    assert canonical_intermediate_translation(first, 5) == (first, 0)
    assert canonical_intermediate_translation(second, 5) == (second, 0)
    assert compress(first, 5) == prescribed[0]
    assert compress(second, 5) == prescribed[1]
    assert IntermediatePBModel(*prescribed).first_failed_constraint(first, second) is None


def test_intermediate_enumeration_rejects_an_accidental_p37_run() -> None:
    prescribed = structured_compressed_pair(37, 3)
    with pytest.raises(ValueError, match="exceeds the explicit per-side cap"):
        search_intermediate_pairs(*prescribed)
    with pytest.raises(ValueError, match="exceeds the explicit per-side cap"):
        enumerate_intermediate_pairs(*prescribed)


def test_anchor_inequalities_exhaustively_select_one_rotation() -> None:
    # Include tied minima and both target signs; inequalities must resolve ties.
    for target in (-1, 1):
        model = IntermediatePBModel(*structured_compressed_pair(3, 3),
                                    canonical_translations=True)
        constraints = tuple(model.iter_symmetry_constraints())[:2]
        for triple in product((-3, -1, 1, 3), repeat=3):
            if sum(triple) != target:
                continue
            accepted = []
            for k in range(3):
                rotated = triple[k:] + triple[:k]
                row = tuple(rotated[i // 3] if i % 3 == 0 else 1 for i in range(9))
                assignment = {
                    model.bit_variable(0, 3 * i, bit): (((3 - v) // 2) >> bit) & 1
                    for i, v in enumerate(rotated) for bit in (0, 1)
                }
                if all(c.satisfied_by(assignment) for c in constraints):
                    accepted.append(rotated)
                canonical, _ = canonical_intermediate_residue_translation(row, 3, 0)
                assert canonical[::3] == min(triple[j:] + triple[:j] for j in range(3))
            assert accepted == [min(triple[j:] + triple[:j] for j in range(3))]


def test_p3_canonical_model_is_sound_complete_on_all_translation_orbits(tmp_path) -> None:
    prescribed = structured_compressed_pair(3, 3)
    model = IntermediatePBModel(*prescribed, canonical_translations=True)
    pairs = enumerate_intermediate_pairs(*prescribed)
    constraints = tuple(model.iter_constraints())
    accepted = {pair for pair in pairs
                if model.first_failed_constraint(*pair, constraints=constraints) is None}
    assert len(accepted) == 88
    assert accepted == {model.canonicalize_pair(*pair) for pair in pairs}
    assert model.stats.variables == 342
    assert model.stats.constraint_records == 951 == len(constraints)
    assert model.stats.normalized_inequalities == 962
    artifact = model.write_opb(tmp_path / "canonical.opb")
    assert "#constraint= 951 #equal= 11" in artifact.path.read_text().splitlines()[0]


def test_intermediate_anchor_validation() -> None:
    with pytest.raises(ValueError, match="sum to"):
        canonical_intermediate_residue_translation((1,) * 9, 3, 0)
    with pytest.raises(ValueError, match="invalid canonical residue"):
        canonical_intermediate_residue_translation((1,) * 9, 3, 3)
    with pytest.raises(ValueError, match="requires a canonical"):
        IntermediatePBModel(*structured_compressed_pair(3, 3)).canonicalize_pair((), ())
