"""Exact witness checks for both stages of the bounded benchmark."""

import pytest

from scripts.benchmark_intermediate_scaling import _validated_pair
from src.legendre import compress, published_structured_legendre_pair_45, structured_compressed_pair
from src.staged_uncompression import FactorThreeBranch, IntermediatePBModel
from src.symmetry import canonical_residue_translation


@pytest.mark.parametrize("canonical", [False, True])
def test_solver_witness_validation_and_corrupt_auxiliaries(canonical):
    binary = published_structured_legendre_pair_45()
    prescribed = structured_compressed_pair(5, 3)
    intermediate = tuple(compress(row, 15) for row in binary)
    first_model = IntermediatePBModel(*prescribed, canonical_translations=canonical)
    pair = first_model.canonicalize_pair(*intermediate) if canonical else intermediate
    assignment = first_model.assignment_for_pair(*pair)
    assert _validated_pair(first_model, assignment) == pair
    assignment[first_model.square_variable(0, 0)] ^= 1
    with pytest.raises(ValueError, match="fails OPB"):
        _validated_pair(first_model, assignment)

    branch = FactorThreeBranch(*prescribed, *intermediate)
    model = branch.model(canonical_translations=canonical, projected_correlations=True)
    if canonical:
        binary = tuple(canonical_residue_translation(row, 15, residue)[0]
                       for row, residue in zip(binary, branch.canonical_residues, strict=True))
    assignment = model.assignment_for_pair(*binary)
    assert _validated_pair(model, assignment) == binary
    assignment[2 * model.length + 1] ^= 1
    with pytest.raises(ValueError, match="fails OPB"):
        _validated_pair(model, assignment)
