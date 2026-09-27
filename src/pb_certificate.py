"""Exact SAT certificates and fixed-witness OPB instances."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping, Sequence

from src.pb_model import UncompressionPBModel


_HEADER = re.compile(
    r"\* #variable= (?P<variables>\d+) #constraint= (?P<constraints>\d+) "
    r"#equal= (?P<equalities>\d+) intsize= (?P<intsize>\d+)"
)


def assignment_literals(assignment: Mapping[int, int], variables: int) -> str:
    """Render a complete binary assignment as VeriPB literals."""

    expected = set(range(1, variables + 1))
    if set(assignment) != expected:
        raise ValueError("assignment keys must be exactly 1..variables")
    if any(value not in {0, 1} for value in assignment.values()):
        raise ValueError("assignment values must be binary")
    return " ".join(
        f"x{variable}" if assignment[variable] else f"~x{variable}"
        for variable in range(1, variables + 1)
    )


def write_veripb_sat_certificate(
    model: UncompressionPBModel,
    first: Sequence[int],
    second: Sequence[int],
    path: Path,
) -> None:
    """Write a VeriPB 2.0 SAT certificate after exact model validation."""

    failure = model.first_failed_constraint(first, second)
    if failure is not None:
        raise ValueError(f"pair violates OPB record {failure}")
    assignment = model.assignment_for_pair(first, second)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "pseudo-Boolean proof version 2.0\n"
        f"f {model.stats.normalized_inequalities}\n"
        f"sol {assignment_literals(assignment, model.stats.variables)}\n"
        "output NONE\n"
        "conclusion SAT\n"
        "end pseudo-Boolean proof\n",
        encoding="ascii",
        newline="\n",
    )


def write_fixed_assignment_opb(
    source: Path,
    assignment: Mapping[int, int],
    destination: Path,
) -> None:
    """Append exact unit constraints fixing all variables in an OPB instance."""

    lines = source.read_text(encoding="ascii").splitlines()
    if not lines:
        raise ValueError("source OPB is empty")
    match = _HEADER.fullmatch(lines[0])
    if match is None:
        raise ValueError("source OPB lacks the proof-compatible extended header")
    variables = int(match.group("variables"))
    assignment_literals(assignment, variables)
    constraints = int(match.group("constraints")) + variables
    lines[0] = (
        f"* #variable= {variables} #constraint= {constraints} "
        f"#equal= {match.group('equalities')} intsize= {match.group('intsize')}"
    )
    lines.append("* exact fixed assignment for proof-pipeline validation")
    lines.extend(
        f"+1 x{variable} >= 1 ;" if assignment[variable] else f"-1 x{variable} >= 0 ;"
        for variable in range(1, variables + 1)
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
