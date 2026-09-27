"""Tests for exact pseudo-Boolean SAT certificate helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.pb_certificate import (
    assignment_literals,
    write_fixed_assignment_opb,
    write_veripb_sat_certificate,
)
from src.pb_model import UncompressionPBModel


def test_assignment_literals_requires_and_renders_a_complete_assignment() -> None:
    assert assignment_literals({1: 1, 2: 0}, 2) == "x1 ~x2"
    with pytest.raises(ValueError, match="exactly"):
        assignment_literals({1: 1}, 2)
    with pytest.raises(ValueError, match="binary"):
        assignment_literals({1: 1, 2: 2}, 2)


def test_sat_certificate_and_fixed_instance_are_exact(tmp_path: Path) -> None:
    model = UncompressionPBModel((1,), (1,), 1)
    first = (1,)
    second = (1,)
    source = tmp_path / "base.opb"
    certificate = tmp_path / "sat.pbp"
    fixed = tmp_path / "fixed.opb"
    model.write_opb(source)
    write_veripb_sat_certificate(model, first, second, certificate)
    assignment = model.assignment_for_pair(first, second)
    write_fixed_assignment_opb(source, assignment, fixed)

    assert certificate.read_text(encoding="ascii").splitlines() == [
        "pseudo-Boolean proof version 2.0",
        "f 4",
        "sol ~x1 ~x2",
        "output NONE",
        "conclusion SAT",
        "end pseudo-Boolean proof",
    ]
    fixed_lines = fixed.read_text(encoding="ascii").splitlines()
    assert fixed_lines[0] == "* #variable= 2 #constraint= 4 #equal= 2 intsize= 4"
    assert fixed_lines[-2:] == ["-1 x1 >= 0 ;", "-1 x2 >= 0 ;"]


def test_sat_certificate_rejects_a_nonmodel_pair(tmp_path: Path) -> None:
    model = UncompressionPBModel((1,), (1,), 1)
    with pytest.raises(ValueError, match="violates"):
        write_veripb_sat_certificate(model, (-1,), (1,), tmp_path / "bad.pbp")
