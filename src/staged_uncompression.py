"""Exact factor-three branch model for successive q-uncompression.

For ``q=3``, a length-``9p`` binary pair may first be 3-compressed to an
integer pair of length ``3p`` and then 3-compressed again to the prescribed
length-``p`` pair.  This module validates a fixed intermediate branch and
builds its exact binary second-stage OPB model.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from src.legendre import (
    check_compressed_legendre_constants,
    compress,
    periodic_autocorrelation,
)
from src.pb_model import (
    OPBArtifact,
    PBConstraint,
    UncompressionPBModel,
    and_constraints,
    xor_constraints,
)


IntegerSequence = tuple[int, ...]
IntermediatePair = tuple[IntegerSequence, IntegerSequence]


@dataclass(frozen=True)
class IntermediatePBStats:
    """Exact structural counts for the first q=3 uncompression model."""

    prescribed_length: int
    intermediate_length: int
    base_variables: int
    square_xor_variables: int
    product_variables: int
    variables: int
    square_xor_inequalities: int
    product_inequalities: int
    compression_equalities: int
    zero_shift_equalities: int
    correlation_equalities: int
    constraint_records: int
    normalized_inequalities: int


@dataclass(frozen=True)
class IntermediateSearch:
    """Exact enumeration summary for compatible length-3p intermediate rows."""

    prescribed_length: int
    first_candidates: int
    second_candidates: int
    first_signatures: int
    second_signatures: int
    signature_matches: int
    ordered_pairs: int
    representative_pairs: tuple[IntermediatePair, ...]


def _intermediate_value(bit_low: int, bit_high: int) -> int:
    return 3 - 2 * (bit_low + 2 * bit_high)


@lru_cache(maxsize=None)
def _triples_with_sum(target: int) -> tuple[tuple[int, int, int], ...]:
    values = (-3, -1, 1, 3)
    return tuple(
        candidate for candidate in product(values, repeat=3) if sum(candidate) == target
    )


def intermediate_uncompression_count(prescribed: Sequence[int]) -> int:
    """Count exact length-3p rows whose second 3-compression is prescribed."""

    if not prescribed:
        raise ValueError("prescribed row must be nonempty")
    result = 1
    for target in prescribed:
        choices = _triples_with_sum(target)
        if not choices:
            raise ValueError(
                f"entry {target} has no three-term preimage in {{-3,-1,1,3}}"
            )
        result *= len(choices)
    return result


def iter_intermediate_rows(prescribed: Sequence[int]) -> Iterator[IntegerSequence]:
    """Yield every exact length-3p row in deterministic residue-major order."""

    targets = tuple(prescribed)
    intermediate_uncompression_count(targets)
    length = 3 * len(targets)
    for residue_choices in product(*(_triples_with_sum(target) for target in targets)):
        row = [0] * length
        for residue, choices in enumerate(residue_choices):
            for step, value in enumerate(choices):
                row[residue + step * len(targets)] = value
        yield tuple(row)


def intermediate_signature(row: Sequence[int]) -> IntegerSequence:
    """Return the nonredundant exact PAF signature, including shift zero."""

    if not row:
        raise ValueError("intermediate row must be nonempty")
    return tuple(
        periodic_autocorrelation(row, shift) for shift in range(len(row) // 2 + 1)
    )


def search_intermediate_pairs(
    prescribed_first: Sequence[int],
    prescribed_second: Sequence[int],
    *,
    max_representatives: int = 32,
    max_candidates_per_side: int | None = 1_000_000,
) -> IntermediateSearch:
    """Exhaustively join first-stage rows by complementary exact PAF signatures.

    The default cap admits the p=3 and p=5 validation cases but rejects a
    larger accidental enumeration. Passing ``None`` removes the software
    guard; it does not make a large run computationally appropriate.
    """

    first_targets = tuple(prescribed_first)
    second_targets = tuple(prescribed_second)
    if len(first_targets) != len(second_targets) or not first_targets:
        raise ValueError("prescribed rows must have the same positive length")
    if len(first_targets) % 2 == 0:
        raise ValueError("prescribed length must be odd")
    check = check_compressed_legendre_constants(first_targets, second_targets, 9)
    if not check.ok:
        raise ValueError(f"prescribed pair violates factor-nine constants: {check.message}")
    if max_representatives < 0:
        raise ValueError("max_representatives must be nonnegative")
    if max_candidates_per_side is not None and max_candidates_per_side <= 0:
        raise ValueError("candidate cap must be positive or None")
    candidate_bounds = tuple(
        intermediate_uncompression_count(row)
        for row in (first_targets, second_targets)
    )
    if max_candidates_per_side is not None and any(
        count > max_candidates_per_side for count in candidate_bounds
    ):
        raise ValueError(
            f"intermediate row count {candidate_bounds} exceeds the explicit "
            f"per-side cap {max_candidates_per_side}"
        )

    # Map each signature to an exact multiplicity and its first deterministic row.
    signature_maps: list[dict[IntegerSequence, tuple[int, IntegerSequence]]] = []
    candidate_counts: list[int] = []
    for prescribed in (first_targets, second_targets):
        counts: dict[IntegerSequence, int] = defaultdict(int)
        representatives: dict[IntegerSequence, IntegerSequence] = {}
        candidates = 0
        for row in iter_intermediate_rows(prescribed):
            candidates += 1
            signature = intermediate_signature(row)
            counts[signature] += 1
            representatives.setdefault(signature, row)
        signature_maps.append(
            {
                signature: (multiplicity, representatives[signature])
                for signature, multiplicity in counts.items()
            }
        )
        candidate_counts.append(candidates)

    length = 3 * len(first_targets)
    target = (6 * length - 4, *([-6] * (length // 2)))
    first_map, second_map = signature_maps
    matches = 0
    ordered_pairs = 0
    pairs: list[IntermediatePair] = []
    for first_signature, (first_count, first_row) in first_map.items():
        complement = tuple(
            target_value - signature_value
            for target_value, signature_value in zip(target, first_signature, strict=True)
        )
        second_record = second_map.get(complement)
        if second_record is None:
            continue
        second_count, second_row = second_record
        matches += 1
        ordered_pairs += first_count * second_count
        if len(pairs) < max_representatives:
            pairs.append((first_row, second_row))

    return IntermediateSearch(
        prescribed_length=len(first_targets),
        first_candidates=candidate_counts[0],
        second_candidates=candidate_counts[1],
        first_signatures=len(first_map),
        second_signatures=len(second_map),
        signature_matches=matches,
        ordered_pairs=ordered_pairs,
        representative_pairs=tuple(pairs),
    )


def canonical_intermediate_translation(
    row: Sequence[int], prescribed_length: int
) -> tuple[IntegerSequence, int]:
    """Choose the least of the three translations preserving 3-compression.

    The returned offset is one of ``0``, ``p``, or ``2p`` for prescribed
    length ``p``. Translation uses the same convention as
    :func:`src.symmetry.cyclic_translate`.
    """

    source = tuple(row)
    if prescribed_length <= 0 or len(source) != 3 * prescribed_length:
        raise ValueError("intermediate row must have length three times p")
    if any(value not in {-3, -1, 1, 3} for value in source):
        raise ValueError("intermediate entries must be in {-3,-1,1,3}")
    rotations = tuple(
        tuple(
            source[(index + step * prescribed_length) % len(source)]
            for index in range(len(source))
        )
        for step in range(3)
    )
    best_step = min(range(3), key=lambda step: (rotations[step], step))
    return rotations[best_step], best_step * prescribed_length


def enumerate_intermediate_pairs(
    prescribed_first: Sequence[int],
    prescribed_second: Sequence[int],
    *,
    canonical_translations: bool = False,
    max_candidates_per_side: int | None = 1_000_000,
) -> tuple[IntermediatePair, ...]:
    """Return every exact compatible intermediate pair at a tractable size.

    This materializes full signature buckets. The default cap admits p=3 and
    p=5 but rejects larger accidental runs; passing ``None`` explicitly
    removes that guard. The current research workflow uses it only for p=3
    and p=5.
    """

    first_targets = tuple(prescribed_first)
    second_targets = tuple(prescribed_second)
    if len(first_targets) != len(second_targets) or not first_targets:
        raise ValueError("prescribed rows must have the same positive length")
    if len(first_targets) % 2 == 0:
        raise ValueError("prescribed length must be odd")
    check = check_compressed_legendre_constants(first_targets, second_targets, 9)
    if not check.ok:
        raise ValueError(f"prescribed pair violates factor-nine constants: {check.message}")
    if max_candidates_per_side is not None and max_candidates_per_side <= 0:
        raise ValueError("candidate cap must be positive or None")
    candidate_bounds = tuple(
        intermediate_uncompression_count(row)
        for row in (first_targets, second_targets)
    )
    if max_candidates_per_side is not None and any(
        count > max_candidates_per_side for count in candidate_bounds
    ):
        raise ValueError(
            f"intermediate row count {candidate_bounds} exceeds the explicit "
            f"per-side cap {max_candidates_per_side}"
        )

    signature_maps: list[dict[IntegerSequence, list[IntegerSequence]]] = []
    for prescribed in (first_targets, second_targets):
        rows: dict[IntegerSequence, list[IntegerSequence]] = defaultdict(list)
        for row in iter_intermediate_rows(prescribed):
            rows[intermediate_signature(row)].append(row)
        signature_maps.append(rows)

    length = 3 * len(first_targets)
    target = (6 * length - 4, *([-6] * (length // 2)))
    pairs: list[IntermediatePair] = []
    first_map, second_map = signature_maps
    for signature, first_rows in first_map.items():
        complement = tuple(
            target_value - signature_value
            for target_value, signature_value in zip(target, signature, strict=True)
        )
        for first_row in first_rows:
            for second_row in second_map.get(complement, ()):
                pairs.append((first_row, second_row))
    if not canonical_translations:
        return tuple(pairs)

    p = len(first_targets)
    canonical = {
        (
            canonical_intermediate_translation(first, p)[0],
            canonical_intermediate_translation(second, p)[0],
        )
        for first, second in pairs
    }
    return tuple(sorted(canonical))


class IntermediatePBModel:
    """Exact OPB encoding of length-3p intermediate q=3 branches.

    Each intermediate entry is ``3 - 2*(u + 2*v)`` for binary ``u,v``.
    Auxiliary variables encode ``u XOR v`` for the square and all four bit
    products required by every nonredundant shifted product.
    """

    def __init__(
        self, prescribed_first: Sequence[int], prescribed_second: Sequence[int]
    ) -> None:
        self.prescribed_first = tuple(prescribed_first)
        self.prescribed_second = tuple(prescribed_second)
        if not self.prescribed_first or len(self.prescribed_first) != len(
            self.prescribed_second
        ):
            raise ValueError("prescribed rows must have the same positive length")
        if len(self.prescribed_first) % 2 == 0:
            raise ValueError("prescribed length must be odd")
        check = check_compressed_legendre_constants(
            self.prescribed_first, self.prescribed_second, 9
        )
        if not check.ok:
            raise ValueError(
                f"prescribed pair violates factor-nine constants: {check.message}"
            )

    @property
    def prescribed_length(self) -> int:
        return len(self.prescribed_first)

    @property
    def length(self) -> int:
        return 3 * self.prescribed_length

    @property
    def half_shifts(self) -> int:
        return self.length // 2

    @property
    def stats(self) -> IntermediatePBStats:
        base = 4 * self.length
        square = 2 * self.length
        products = 2 * self.half_shifts * self.length * 4
        square_inequalities = 4 * square
        product_inequalities = 3 * products
        compression_equalities = 2 * self.prescribed_length
        zero_equalities = 1
        correlation_equalities = self.half_shifts
        equalities = compression_equalities + zero_equalities + correlation_equalities
        return IntermediatePBStats(
            prescribed_length=self.prescribed_length,
            intermediate_length=self.length,
            base_variables=base,
            square_xor_variables=square,
            product_variables=products,
            variables=base + square + products,
            square_xor_inequalities=square_inequalities,
            product_inequalities=product_inequalities,
            compression_equalities=compression_equalities,
            zero_shift_equalities=zero_equalities,
            correlation_equalities=correlation_equalities,
            constraint_records=square_inequalities
            + product_inequalities
            + equalities,
            normalized_inequalities=square_inequalities
            + product_inequalities
            + 2 * equalities,
        )

    def bit_variable(self, row: int, index: int, bit: int) -> int:
        if row not in {0, 1} or bit not in {0, 1} or not 0 <= index < self.length:
            raise IndexError("invalid row, position, or bit")
        return 1 + row * 2 * self.length + 2 * index + bit

    def square_variable(self, row: int, index: int) -> int:
        if row not in {0, 1} or not 0 <= index < self.length:
            raise IndexError("invalid row or position")
        return 4 * self.length + 1 + row * self.length + index

    def product_variable(
        self, row: int, shift: int, index: int, left_bit: int, right_bit: int
    ) -> int:
        if row not in {0, 1} or left_bit not in {0, 1} or right_bit not in {0, 1}:
            raise IndexError("invalid row or product bit")
        if not 1 <= shift <= self.half_shifts or not 0 <= index < self.length:
            raise IndexError("invalid shift or position")
        product_index = (
            (
                (row * self.half_shifts + shift - 1) * self.length + index
            )
            * 2
            + left_bit
        ) * 2 + right_bit
        return 6 * self.length + 1 + product_index

    @staticmethod
    def _negative_units(target: int) -> int:
        if (9 - target) % 2:
            raise ValueError(f"prescribed entry {target} has wrong parity")
        result = (9 - target) // 2
        if not 0 <= result <= 9:
            raise ValueError(f"prescribed entry {target} is out of range")
        return result

    def iter_constraints(self) -> Iterator[PBConstraint]:
        d = self.prescribed_length
        for row, prescribed in enumerate(
            (self.prescribed_first, self.prescribed_second)
        ):
            for residue, target in enumerate(prescribed):
                terms = []
                for step in range(3):
                    index = residue + step * d
                    terms.append((1, self.bit_variable(row, index, 0)))
                    terms.append((2, self.bit_variable(row, index, 1)))
                yield PBConstraint(tuple(terms), "=", self._negative_units(target))

        for row in (0, 1):
            for index in range(self.length):
                yield from xor_constraints(
                    self.bit_variable(row, index, 0),
                    self.bit_variable(row, index, 1),
                    self.square_variable(row, index),
                )
        yield PBConstraint(
            tuple(
                (1, self.square_variable(row, index))
                for row in (0, 1)
                for index in range(self.length)
            ),
            "=",
            (3 * self.length + 1) // 2,
        )

        for row in (0, 1):
            for shift in range(1, self.half_shifts + 1):
                for index in range(self.length):
                    right_index = (index + shift) % self.length
                    for left_bit in (0, 1):
                        for right_bit in (0, 1):
                            yield from and_constraints(
                                self.bit_variable(row, index, left_bit),
                                self.bit_variable(row, right_index, right_bit),
                                self.product_variable(
                                    row, shift, index, left_bit, right_bit
                                ),
                            )

        product_target = 9 * (self.length - 1) // 2
        weights = ((1, 2), (2, 4))
        for shift in range(1, self.half_shifts + 1):
            yield PBConstraint(
                tuple(
                    (
                        weights[left_bit][right_bit],
                        self.product_variable(
                            row, shift, index, left_bit, right_bit
                        ),
                    )
                    for row in (0, 1)
                    for index in range(self.length)
                    for left_bit in (0, 1)
                    for right_bit in (0, 1)
                ),
                "=",
                product_target,
            )

    def assignment_for_pair(
        self, first: Sequence[int], second: Sequence[int]
    ) -> dict[int, int]:
        rows = (tuple(first), tuple(second))
        if any(len(row) != self.length for row in rows):
            raise ValueError(f"both intermediate rows must have length {self.length}")
        if any(value not in {-3, -1, 1, 3} for row in rows for value in row):
            raise ValueError("intermediate entries must be in {-3,-1,1,3}")
        assignment: dict[int, int] = {}
        bit_rows: list[list[tuple[int, int]]] = []
        for row_index, row in enumerate(rows):
            bits = []
            for index, value in enumerate(row):
                encoded = (3 - value) // 2
                low, high = encoded & 1, (encoded >> 1) & 1
                if _intermediate_value(low, high) != value:
                    raise AssertionError("intermediate bit encoding failed")
                bits.append((low, high))
                assignment[self.bit_variable(row_index, index, 0)] = low
                assignment[self.bit_variable(row_index, index, 1)] = high
                assignment[self.square_variable(row_index, index)] = low ^ high
            bit_rows.append(bits)
        for row_index, bits in enumerate(bit_rows):
            for shift in range(1, self.half_shifts + 1):
                for index, left in enumerate(bits):
                    right = bits[(index + shift) % self.length]
                    for left_bit in (0, 1):
                        for right_bit in (0, 1):
                            assignment[
                                self.product_variable(
                                    row_index, shift, index, left_bit, right_bit
                                )
                            ] = left[left_bit] & right[right_bit]
        return assignment

    def first_failed_constraint(
        self,
        first: Sequence[int],
        second: Sequence[int],
        *,
        constraints: Iterable[PBConstraint] | None = None,
    ) -> int | None:
        assignment = self.assignment_for_pair(first, second)
        source = self.iter_constraints() if constraints is None else constraints
        for index, constraint in enumerate(source):
            if not constraint.satisfied_by(assignment):
                return index
        return None

    def write_opb(self, path: Path) -> OPBArtifact:
        path.parent.mkdir(parents=True, exist_ok=True)
        stats = self.stats
        equalities = (
            stats.compression_equalities
            + stats.zero_shift_equalities
            + stats.correlation_equalities
        )
        with path.open("w", encoding="ascii", newline="\n") as stream:
            stream.write(
                f"* #variable= {stats.variables} #constraint= {stats.constraint_records} "
                f"#equal= {equalities} "
                "intsize= 4\n"
            )
            stream.write("* intermediate entry = 3 - 2*(u + 2*v)\n")
            stream.write("* auxiliaries: square XORs, then shifted bit products\n")
            for constraint in self.iter_constraints():
                stream.write(constraint.to_opb())
        digest = sha256()
        size = 0
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(block)
                digest.update(block)
        return OPBArtifact(path=path, bytes=size, sha256=digest.hexdigest())


@dataclass(frozen=True)
class FactorThreeBranch:
    """One exact length-``3p`` intermediate branch for final factor 3."""

    prescribed_first: IntegerSequence
    prescribed_second: IntegerSequence
    intermediate_first: IntegerSequence
    intermediate_second: IntegerSequence

    def __init__(
        self,
        prescribed_first: Sequence[int],
        prescribed_second: Sequence[int],
        intermediate_first: Sequence[int],
        intermediate_second: Sequence[int],
    ) -> None:
        object.__setattr__(self, "prescribed_first", tuple(prescribed_first))
        object.__setattr__(self, "prescribed_second", tuple(prescribed_second))
        object.__setattr__(self, "intermediate_first", tuple(intermediate_first))
        object.__setattr__(self, "intermediate_second", tuple(intermediate_second))
        self._validate()

    @property
    def compressed_length(self) -> int:
        return len(self.prescribed_first)

    @property
    def intermediate_length(self) -> int:
        return len(self.intermediate_first)

    @property
    def final_length(self) -> int:
        return 3 * self.intermediate_length

    @property
    def canonical_residues(self) -> tuple[int, int]:
        """Choose an aperiodic factor-three residue in each intermediate row."""

        residues = []
        for row in (self.intermediate_first, self.intermediate_second):
            residue = next((index for index, value in enumerate(row) if abs(value) == 1), None)
            if residue is None:
                raise ValueError("each intermediate row needs a +/-1 canonical residue")
            residues.append(residue)
        return residues[0], residues[1]

    def model(
        self,
        *,
        canonical_translations: bool = False,
        projected_correlations: bool = False,
    ) -> UncompressionPBModel:
        """Return the exact binary uncompression model for this fixed branch."""

        return UncompressionPBModel(
            self.intermediate_first,
            self.intermediate_second,
            3,
            canonical_translations=canonical_translations,
            canonical_residues=(self.canonical_residues if canonical_translations else None),
            factor_three_projection=projected_correlations,
        )

    def _validate(self) -> None:
        if not self.prescribed_first:
            raise ValueError("prescribed rows must be nonempty")
        if len(self.prescribed_first) != len(self.prescribed_second):
            raise ValueError("prescribed rows must have equal length")
        expected_intermediate = 3 * len(self.prescribed_first)
        if len(self.intermediate_first) != expected_intermediate or len(
            self.intermediate_second
        ) != expected_intermediate:
            raise ValueError("intermediate rows must have length three times p")
        if compress(self.intermediate_first, self.compressed_length) != self.prescribed_first:
            raise ValueError("first intermediate row has the wrong second compression")
        if compress(self.intermediate_second, self.compressed_length) != self.prescribed_second:
            raise ValueError("second intermediate row has the wrong second compression")
        check = check_compressed_legendre_constants(
            self.intermediate_first,
            self.intermediate_second,
            3,
        )
        if not check.ok:
            raise ValueError(
                "intermediate pair violates compressed PAF constants: "
                f"{check.message}"
            )
