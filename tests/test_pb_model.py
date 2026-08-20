"""Tests for the exact pseudo-Boolean uncompression encoding."""

from __future__ import annotations

from src.legendre import structured_compressed_pair
from src.pb_model import PBConstraint, UncompressionPBModel
from src.uncompress import search_uncompressions


def test_pb_constraint_serialization_and_exact_evaluation() -> None:
    constraint = PBConstraint(((1, 1), (-1, 2), (1, 3)), ">=", 0)
    assert constraint.to_opb() == "+1 x1 -1 x2 +1 x3 >= 0 ;\n"
    assert constraint.satisfied_by({1: 1, 2: 0, 3: 0})
    assert not constraint.satisfied_by({1: 0, 2: 1, 3: 0})


def test_p3_model_has_the_derived_exact_counts() -> None:
    first, second = structured_compressed_pair(3, 3)
    model = UncompressionPBModel(first, second, 9)
    assert model.stats.uncompressed_length == 27
    assert model.stats.base_variables == 54
    assert model.stats.xor_variables == 702
    assert model.stats.variables == 756
    assert model.stats.xor_inequalities == 2808
    assert model.stats.compression_equalities == 6
    assert model.stats.correlation_equalities == 13
    assert model.stats.constraint_records == 2827
    assert model.stats.normalized_inequalities == 2846
    assert sum(1 for _ in model.iter_constraints()) == model.stats.constraint_records


def test_p37_model_has_the_derived_exact_counts() -> None:
    first, second = structured_compressed_pair(37, 3)
    model = UncompressionPBModel(first, second, 9)
    assert model.stats.uncompressed_length == 333
    assert model.stats.base_variables == 666
    assert model.stats.xor_variables == 110_556
    assert model.stats.variables == 111_222
    assert model.stats.xor_inequalities == 442_224
    assert model.stats.compression_equalities == 74
    assert model.stats.correlation_equalities == 166
    assert model.stats.constraint_records == 442_464
    assert model.stats.normalized_inequalities == 442_704


def test_recovered_lp27_is_a_model_witness_and_a_perturbation_is_not() -> None:
    first, second = structured_compressed_pair(3, 3)
    search = search_uncompressions(first, second, 9, collect=1)
    left, right = search.solutions[0]
    model = UncompressionPBModel(first, second, 9)
    constraints = tuple(model.iter_constraints())
    assert model.first_failed_constraint(left, right, constraints=constraints) is None

    broken = (-left[0], *left[1:])
    assert model.first_failed_constraint(broken, right, constraints=constraints) is not None


def test_written_opb_header_and_hash_are_deterministic(tmp_path) -> None:
    model = UncompressionPBModel((1,), (1,), 1)
    first = model.write_opb(tmp_path / "first.opb")
    second = model.write_opb(tmp_path / "second.opb")
    assert first.sha256 == second.sha256
    assert first.bytes == second.bytes
    text = first.path.read_text(encoding="ascii")
    assert text.startswith("* #variable= 2 #constraint= 2\n")
    assert sum(line.endswith(" ;") for line in text.splitlines()) == 2
