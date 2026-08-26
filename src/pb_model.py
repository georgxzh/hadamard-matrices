"""Exact pseudo-Boolean model for prescribed Legendre-pair uncompression.

The binary variable for a sequence position is one exactly when the sign at
that position is ``-1``.  Compression is therefore an exact cardinality
condition.  For every nonredundant cyclic shift, auxiliary variables encode
the XOR (sign disagreement) at each position.  The Legendre PAF equation

``PAF_A(s) + PAF_B(s) = -2``

is equivalent to saying that the two rows have ``length + 1`` disagreements
in total at shift ``s``.  All coefficients and right-hand sides are integers.

The generated OPB uses only equality and greater-than-or-equal constraints.
It is intentionally an unbroken reference model: no symmetry restriction is
included unless it has separately been proved to preserve the prescribed
compressed rows.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence


IntegerSequence = tuple[int, ...]


@dataclass(frozen=True)
class PBConstraint:
    """One sparse pseudo-Boolean constraint."""

    terms: tuple[tuple[int, int], ...]
    relation: str
    rhs: int

    def __post_init__(self) -> None:
        if self.relation not in {">=", "="}:
            raise ValueError(f"unsupported relation: {self.relation}")
        if not self.terms:
            raise ValueError("a constraint must contain at least one term")
        if any(coefficient == 0 or variable <= 0 for coefficient, variable in self.terms):
            raise ValueError("constraint coefficients must be nonzero and variables positive")

    def satisfied_by(self, assignment: Mapping[int, int]) -> bool:
        """Evaluate the constraint exactly on a complete binary assignment."""

        total = 0
        for coefficient, variable in self.terms:
            value = assignment.get(variable)
            if value not in {0, 1}:
                raise ValueError(f"variable x{variable} is not assigned a binary value")
            total += coefficient * value
        return total >= self.rhs if self.relation == ">=" else total == self.rhs

    def to_opb(self) -> str:
        """Serialize using the standard numbered-variable OPB syntax."""

        left = " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in self.terms)
        return f"{left} {self.relation} {self.rhs} ;\n"


@dataclass(frozen=True)
class PBModelStats:
    """Exact structural counts for an uncompression model."""

    compressed_length: int
    factor: int
    uncompressed_length: int
    base_variables: int
    xor_variables: int
    variables: int
    xor_inequalities: int
    compression_equalities: int
    correlation_equalities: int
    symmetry_inequalities: int
    constraint_records: int
    normalized_inequalities: int


@dataclass(frozen=True)
class OPBArtifact:
    """Hash and size of a deterministically written model."""

    path: Path
    bytes: int
    sha256: str


class UncompressionPBModel:
    """Exact OPB encoding of binary preimages of two compressed rows."""

    def __init__(
        self,
        first_compressed: Sequence[int],
        second_compressed: Sequence[int],
        factor: int,
        *,
        canonical_translations: bool = False,
    ) -> None:
        self.first_compressed = tuple(first_compressed)
        self.second_compressed = tuple(second_compressed)
        self.factor = factor
        self.canonical_translations = canonical_translations
        if not self.first_compressed:
            raise ValueError("compressed rows must be nonempty")
        if len(self.first_compressed) != len(self.second_compressed):
            raise ValueError("compressed rows must have equal length")
        if factor <= 0:
            raise ValueError("factor must be positive")
        for target in (*self.first_compressed, *self.second_compressed):
            self._negative_count(target)

    @property
    def compressed_length(self) -> int:
        return len(self.first_compressed)

    @property
    def length(self) -> int:
        return self.compressed_length * self.factor

    @property
    def half_shifts(self) -> int:
        return self.length // 2

    @property
    def stats(self) -> PBModelStats:
        base = 2 * self.length
        xor = 2 * self.half_shifts * self.length
        xor_inequalities = 4 * xor
        compression_equalities = 2 * self.compressed_length
        correlation_equalities = self.half_shifts
        symmetry_inequalities = 2 * (self.factor - 1) if self.canonical_translations else 0
        equalities = compression_equalities + correlation_equalities
        return PBModelStats(
            compressed_length=self.compressed_length,
            factor=self.factor,
            uncompressed_length=self.length,
            base_variables=base,
            xor_variables=xor,
            variables=base + xor,
            xor_inequalities=xor_inequalities,
            compression_equalities=compression_equalities,
            correlation_equalities=correlation_equalities,
            symmetry_inequalities=symmetry_inequalities,
            constraint_records=xor_inequalities + equalities + symmetry_inequalities,
            normalized_inequalities=(
                xor_inequalities + 2 * equalities + symmetry_inequalities
            ),
        )

    def _negative_count(self, target: int) -> int:
        if (self.factor - target) % 2:
            raise ValueError(
                f"compressed entry {target} has wrong parity for factor {self.factor}"
            )
        result = (self.factor - target) // 2
        if not 0 <= result <= self.factor:
            raise ValueError(
                f"compressed entry {target} is out of range for factor {self.factor}"
            )
        return result

    def first_variable(self, index: int) -> int:
        return self._position_variable(0, index)

    def second_variable(self, index: int) -> int:
        return self._position_variable(1, index)

    def _position_variable(self, row: int, index: int) -> int:
        if row not in {0, 1} or not 0 <= index < self.length:
            raise IndexError("invalid row or sequence index")
        return 1 + row * self.length + index

    def xor_variable(self, row: int, shift: int, index: int) -> int:
        if row not in {0, 1}:
            raise IndexError("row must be zero or one")
        if not 1 <= shift <= self.half_shifts:
            raise IndexError("shift is outside the nonredundant range")
        if not 0 <= index < self.length:
            raise IndexError("sequence index is outside the row")
        offset = row * self.half_shifts * self.length
        offset += (shift - 1) * self.length + index
        return 2 * self.length + 1 + offset

    def iter_constraints(self) -> Iterator[PBConstraint]:
        """Yield every model constraint in deterministic order."""

        d = self.compressed_length
        for row, compressed in enumerate((self.first_compressed, self.second_compressed)):
            for residue, target in enumerate(compressed):
                variables = tuple(
                    (1, self._position_variable(row, residue + step * d))
                    for step in range(self.factor)
                )
                yield PBConstraint(variables, "=", self._negative_count(target))

        if self.canonical_translations:
            # Translation by k*d rotates every residue class by k and leaves
            # each row's PAF unchanged.  Compare the negative-sign bit word in
            # residue class zero with each of its nontrivial rotations.  Binary
            # positional weights encode exact lexicographic minimality.
            weights = tuple(1 << (self.factor - 1 - step) for step in range(self.factor))
            for row in (0, 1):
                for rotation in range(1, self.factor):
                    coefficients: dict[int, int] = {}
                    for step, weight in enumerate(weights):
                        original = self._position_variable(
                            row, step * self.compressed_length
                        )
                        rotated = self._position_variable(
                            row,
                            ((step + rotation) % self.factor) * self.compressed_length,
                        )
                        coefficients[rotated] = coefficients.get(rotated, 0) + weight
                        coefficients[original] = coefficients.get(original, 0) - weight
                    terms = tuple(
                        (coefficient, variable)
                        for variable, coefficient in sorted(coefficients.items())
                        if coefficient
                    )
                    yield PBConstraint(terms, ">=", 0)

        for row in (0, 1):
            for shift in range(1, self.half_shifts + 1):
                for index in range(self.length):
                    left = self._position_variable(row, index)
                    right = self._position_variable(row, (index + shift) % self.length)
                    xor = self.xor_variable(row, shift, index)
                    # xor == left XOR right, as the four facets of its exact
                    # binary convex hull.
                    yield PBConstraint(((1, left), (1, right), (-1, xor)), ">=", 0)
                    yield PBConstraint(((-1, left), (-1, right), (-1, xor)), ">=", -2)
                    yield PBConstraint(((1, left), (-1, right), (1, xor)), ">=", 0)
                    yield PBConstraint(((-1, left), (1, right), (1, xor)), ">=", 0)

        for shift in range(1, self.half_shifts + 1):
            variables = tuple(
                (1, self.xor_variable(row, shift, index))
                for row in (0, 1)
                for index in range(self.length)
            )
            yield PBConstraint(variables, "=", self.length + 1)

    def assignment_for_pair(
        self, first: Sequence[int], second: Sequence[int]
    ) -> dict[int, int]:
        """Return the unique complete assignment induced by two sign rows."""

        rows = (tuple(first), tuple(second))
        if any(len(row) != self.length for row in rows):
            raise ValueError(f"both rows must have length {self.length}")
        if any(value not in {-1, 1} for row in rows for value in row):
            raise ValueError("sequence entries must be -1 or +1")

        assignment: dict[int, int] = {}
        for row_index, row in enumerate(rows):
            for index, sign in enumerate(row):
                assignment[self._position_variable(row_index, index)] = int(sign == -1)
            for shift in range(1, self.half_shifts + 1):
                for index, sign in enumerate(row):
                    assignment[self.xor_variable(row_index, shift, index)] = int(
                        sign != row[(index + shift) % self.length]
                    )
        return assignment

    def first_failed_constraint(
        self,
        first: Sequence[int],
        second: Sequence[int],
        *,
        constraints: Iterable[PBConstraint] | None = None,
    ) -> int | None:
        """Return the zero-based index of the first violated record, if any."""

        assignment = self.assignment_for_pair(first, second)
        source = self.iter_constraints() if constraints is None else constraints
        for index, constraint in enumerate(source):
            if not constraint.satisfied_by(assignment):
                return index
        return None

    def write_opb(self, path: Path) -> OPBArtifact:
        """Stream a deterministic OPB file and return its exact hash and size."""

        path.parent.mkdir(parents=True, exist_ok=True)
        stats = self.stats
        with path.open("w", encoding="ascii", newline="\n") as stream:
            stream.write(
                f"* #variable= {stats.variables} #constraint= {stats.constraint_records}\n"
            )
            stream.write("* x1..xL: first row; x(L+1)..x(2L): second row\n")
            stream.write("* remaining variables: row-major XORs by row, shift, position\n")
            if self.canonical_translations:
                stream.write("* translation canonicalization: enabled\n")
            for constraint in self.iter_constraints():
                stream.write(constraint.to_opb())

        digest = sha256()
        size = 0
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(block)
                digest.update(block)
        return OPBArtifact(path=path, bytes=size, sha256=digest.hexdigest())
