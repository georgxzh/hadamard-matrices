"""Independent exact checks of the phase encoding, carry, and cross terms."""

from itertools import product

import pytest

from scripts.benchmark_staged_uncompression import _known_pair
from scripts.benchmark_ternary_phase import find_intermediate
from src.legendre import compress, periodic_autocorrelation, structured_compressed_pair
from src.staged_uncompression import FactorThreeBranch
from src.ternary_phase import PhaseRow, TernaryPhasePBModel, search_phase_uncompressions
from src.uncompress import iter_uncompression_masks, mask_to_sequence


def _branch(p):
    binary = _known_pair(p)
    intermediate = tuple(compress(row, 3*p) for row in binary)
    return binary, intermediate


def test_phase_formula_for_every_p3_preimage_and_every_shift():
    _, intermediate = _branch(3)
    total = 0
    for compressed in intermediate:
        row = PhaseRow(compressed)
        terms = [row.paf_terms(s) for s in range(3*row.length)]
        seen = set()
        for mask in iter_uncompression_masks(compressed, 3):
            binary = mask_to_sequence(mask, 3*row.length)
            phases = row.encode(binary)
            assert row.decode(phases) == binary
            seen.add(phases)
            for s, (constant, edges) in enumerate(terms):
                value = constant + sum(w for u, v, h, w in edges
                                       if (phases[v]-phases[u]) % 3 == h)
                assert value == periodic_autocorrelation(binary, s)
            total += 1
        assert len(seen) == 3 ** len(row.active)
    assert total == 7290


def test_gray_updates_preserve_every_projected_cross_term():
    _, intermediate = _branch(3)
    for compressed in intermediate:
        row = PhaseRow(compressed)
        seen = set()
        previous = None
        for phases, signature in row.iter_projected_signatures():
            assert phases[0] == 0
            assert signature == tuple(periodic_autocorrelation(row.decode(phases), s)
                                      for s in range(1, row.length))
            if previous is not None:
                assert sum(a != b for a, b in zip(phases, previous)) == 1
            previous = phases
            seen.add(phases)
        assert len(seen) == row.canonical_count
        assert dict(row.iter_projected_signatures()) == dict(row.iter_packed_signatures())


@pytest.mark.parametrize("p", [3, 5])
@pytest.mark.parametrize("canonical", [False, True])
def test_phase_pb_witness_and_stats(p, canonical, tmp_path):
    binary, intermediate = _branch(p)
    model = TernaryPhasePBModel(*intermediate, canonical=canonical)
    if canonical:
        binary = model.canonicalize_pair(*binary)
    assert model.first_failed_constraint(*binary) is None
    assignment = model.assignment_for_pair(*binary)
    assert model.pair_from_assignment(assignment) == binary
    constraints = tuple(model.iter_constraints())
    assert len(constraints) == model.stats.constraint_records
    assert sum(1 + (c.relation == "=") for c in constraints) == model.stats.normalized_inequalities
    assert max(v for c in constraints for _, v in c.terms) == model.stats.variables
    artifact = model.write_opb(tmp_path / "phase.opb")
    assert artifact.bytes == artifact.path.stat().st_size
    assignment[model.difference_variable(0, 0, 1, 0)] ^= 1
    with pytest.raises(ValueError, match="fails the phase OPB"):
        model.pair_from_assignment(assignment)


def test_channel_gadget_truth_table():
    _, intermediate = _branch(3)
    model = TernaryPhasePBModel(*intermediate, canonical=False)
    variables = {model.phase_variable(0, i, a) for i in (0, 1) for a in range(3)}
    variables.update(model.difference_variable(0, 0, 1, h) for h in range(3))
    constraints = [c for c in model.iter_constraints()
                   if {v for _, v in c.terms} <= variables]
    # All nine-bit assignments: exactly nine satisfy the complete gadget.
    accepted = 0
    for bits in product((0, 1), repeat=9):
        assignment = dict(zip(sorted(variables), bits))
        if all(c.satisfied_by(assignment) for c in constraints):
            phases = [next(a for a in range(3) if assignment[model.phase_variable(0, i, a)])
                      for i in (0, 1)]
            assert assignment[model.difference_variable(0, 0, 1, (phases[1]-phases[0]) % 3)]
            accepted += 1
    assert accepted == 9


def test_exact_phase_join_count_and_partial_semantics():
    _, intermediate = _branch(3)
    result = search_phase_uncompressions(*intermediate)
    assert result.complete and result.stop_reason == "exhausted"
    assert result.canonical_pairs == 15
    assert result.ordered_pairs == 135
    assert (result.stored_candidates, result.streamed_candidates) == (243, 2187)
    assert result.solutions
    packed = search_phase_uncompressions(*intermediate, evaluation="packed")
    assert packed.complete and packed.ordered_pairs == result.ordered_pairs
    for kwargs, reason in (({"max_candidates_per_side": 1}, "candidate_limit"),
                           ({"max_stored_signatures": 1}, "signature_limit"),
                           ({"time_limit": 1e-9}, "time_limit")):
        partial = search_phase_uncompressions(*intermediate, **kwargs)
        assert not partial.complete and partial.stop_reason == reason


def test_phase_validation_and_constant_residues():
    row = PhaseRow((3, -3, 3))
    assert row.encode(row.decode(())) == ()
    assert list(row.iter_projected_signatures()) == [((), (row.paf((), 1), row.paf((), 2)))]
    with pytest.raises(ValueError):
        PhaseRow((0, 1))
    with pytest.raises(ValueError):
        row.decode((0,))
    with pytest.raises(ValueError, match="wrong compression"):
        row.encode((1,) * 9)
    _, intermediate = _branch(3)
    broken = list(intermediate[0])
    broken[0] = -broken[0]
    with pytest.raises(ValueError, match="invalid factor-three"):
        TernaryPhasePBModel(broken, intermediate[1])


def test_seeded_branch_acquisition_accepts_only_exact_intermediates():
    result = find_intermediate(3, seed=20260928, seconds=2, max_iterations=2000)
    assert result["status"] == "exact_branch_found"
    branch = FactorThreeBranch(*structured_compressed_pair(3, 3), *result["pair"])
    assert branch.final_length == 27
    assert result["iterations"] <= 2000
    with pytest.raises(ValueError, match="bounded"):
        find_intermediate(37, seed=0, seconds=1)


def test_phase_join_rejects_invalid_resource_controls():
    _, intermediate = _branch(3)
    for options in ({"max_candidates_per_side": 0}, {"max_stored_signatures": 0},
                    {"time_limit": 0}, {"collect": -1}, {"evaluation": "approximate"}):
        with pytest.raises(ValueError):
            search_phase_uncompressions(*intermediate, **options)
