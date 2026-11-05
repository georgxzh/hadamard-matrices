"""Exact minority-layer phases, cross-term PAF joins, and a compact PB model.

A magnitude-one compressed entry has one minority sign in three layers.
Its layer is a ternary phase. PAFs depend on phase differences, including
the carry when a shift crosses the compressed row boundary.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from time import perf_counter
from typing import Iterator, Mapping, Sequence

from src.legendre import check_compressed_legendre_constants, check_legendre_pair, compress
from src.pb_model import OPBArtifact, PBConstraint
from src.uncompress import paf_signature_at_shifts


class PhaseRow:
    """A bijective ternary parameterization of one factor-three preimage."""

    def __init__(self, compressed: Sequence[int]):
        self.compressed = tuple(compressed)
        if not self.compressed or any(c not in {-3, -1, 1, 3} for c in self.compressed):
            raise ValueError("compressed row must be nonempty with entries in {-3,-1,1,3}")
        self.length = len(self.compressed)
        self.active = tuple(i for i, c in enumerate(self.compressed) if abs(c) == 1)
        self._indices = {position: index for index, position in enumerate(self.active)}
        self.base = tuple(1 if c > 0 else -1 for c in self.compressed)
        self.delta = tuple(-2 * b if abs(c) == 1 else 0
                           for b, c in zip(self.base, self.compressed, strict=True))

    def _validate_phases(self, phases: Sequence[int]) -> tuple[int, ...]:
        phases = tuple(phases)
        if len(phases) != len(self.active) or any(a not in {0, 1, 2} for a in phases):
            raise ValueError("one phase in {0,1,2} is required per active residue")
        return phases

    def decode(self, phases: Sequence[int]) -> tuple[int, ...]:
        phases = self._validate_phases(phases)
        return tuple(
            self.base[i] + (self.delta[i] if i in self._indices and
                           k == phases[self._indices[i]] else 0)
            for k in range(3) for i in range(self.length)
        )

    def encode(self, binary: Sequence[int]) -> tuple[int, ...]:
        binary = tuple(binary)
        if len(binary) != 3 * self.length or any(x not in {-1, 1} for x in binary):
            raise ValueError("binary preimage has wrong length or entries")
        if compress(binary, self.length) != self.compressed:
            raise ValueError("binary preimage has wrong compression")
        return tuple(next(k for k in range(3) if binary[i + k * self.length] != self.base[i])
                     for i in self.active)

    def canonical_phases(self, phases: Sequence[int]) -> tuple[int, ...]:
        phases = self._validate_phases(phases)
        return tuple((a - phases[0]) % 3 for a in phases) if phases else ()

    def paf_terms(self, shift: int) -> tuple[int, tuple[tuple[int, int, int, int], ...]]:
        """Return constant and (u,v,h,weight) terms [a_v-a_u=h mod 3].

        This also handles zero shifts and multiples of N exactly. Orienting
        every edge u<v makes the layer carry and sign convention explicit.
        """
        shift %= 3 * self.length
        ell, r = divmod(shift, self.length)
        constant = 0
        terms: dict[tuple[int, int, int], int] = defaultdict(int)
        for i in range(self.length):
            carry, j = divmod(i + r, self.length)
            h = (ell + carry) % 3
            b, d = self.base, self.delta
            constant += 3 * b[i] * b[j] + d[i] * b[j] + b[i] * d[j]
            if not d[i] or not d[j]:
                continue
            if i == j:
                constant += d[i] * d[j] * (h == 0)
                continue
            u, v = self._indices[i], self._indices[j]
            if u > v:
                u, v, h = v, u, (-h) % 3
            terms[u, v, h] += d[i] * d[j]
        return constant, tuple((*key, weight) for key, weight in sorted(terms.items()) if weight)

    def paf(self, phases: Sequence[int], shift: int) -> int:
        phases = self._validate_phases(phases)
        constant, terms = self.paf_terms(shift)
        return constant + sum(weight for u, v, h, weight in terms
                              if (phases[v] - phases[u]) % 3 == h)

    @property
    def canonical_count(self) -> int:
        return 3 ** max(0, len(self.active) - 1)

    def iter_projected_signatures(self) -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
        """Enumerate anchor-zero phases with an exact incremental PAF vector.

        Ternary reflected Gray order changes one phase at a time. All edges
        incident to that phase are updated, including edges across any split.
        This is still exponential enumeration, with no square-root claim.
        """
        n, k = self.length, len(self.active)
        phases = [0] * k
        signature = [self.paf_terms(s)[0] for s in range(1, n)]
        adjacent = [[] for _ in range(k)]
        for u, v in combinations(range(k), 2):
            distance = self.active[v] - self.active[u]
            weight = self.delta[self.active[u]] * self.delta[self.active[v]]
            signature[distance - 1] += weight  # All initial differences are zero.
            edge = (u, v, distance - 1, n - distance - 1, weight)
            adjacent[u].append(edge)
            adjacent[v].append(edge)
        directions = [1] * k
        while True:
            yield tuple(phases), tuple(signature)
            index = k - 1
            while index >= 1 and not 0 <= phases[index] + directions[index] <= 2:
                directions[index] = -directions[index]
                index -= 1
            if index < 1:
                return
            for u, v, forward, reverse, weight in adjacent[index]:
                difference = (phases[v] - phases[u]) % 3
                if difference != 1:
                    signature[forward if difference == 0 else reverse] -= weight
            phases[index] += directions[index]
            for u, v, forward, reverse, weight in adjacent[index]:
                difference = (phases[v] - phases[u]) % 3
                if difference != 1:
                    signature[forward if difference == 0 else reverse] += weight

    def iter_packed_signatures(self) -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
        """Independent bit-packed baseline on exactly the same anchor-zero set."""
        n = self.length
        fixed = sum(1 << (i + k*n) for i, c in enumerate(self.compressed)
                    if c == -3 for k in range(3))
        masks = []
        for i in self.active:
            full = sum(1 << (i + k*n) for k in range(3))
            masks.append(tuple((1 << (i + a*n)) if self.compressed[i] == 1
                               else full ^ (1 << (i + a*n)) for a in range(3)))
        choices = [(0,)] + [range(3)] * (len(self.active)-1) if self.active else []
        for phases in product(*choices):
            mask = fixed
            for index, phase in enumerate(phases):
                mask |= masks[index][phase]
            yield phases, paf_signature_at_shifts(mask, 3*n, tuple(range(1, n)))


@dataclass(frozen=True)
class PhasePBStats:
    phase_variables: int
    difference_variables: int
    variables: int
    phase_equalities: int
    difference_equalities: int
    channel_inequalities: int
    gauge_equalities: int
    correlation_equalities: int
    constraint_records: int
    normalized_inequalities: int


class TernaryPhasePBModel:
    """One-hot phases and shared one-hot differences for all active pairs.

    Exactly nine implications per edge channel endpoint phases to a single
    difference. Every correlation retains its full set of cross terms.
    """

    def __init__(self, first: Sequence[int], second: Sequence[int], *, canonical: bool = True):
        self.rows = (PhaseRow(first), PhaseRow(second))
        if len(first) != len(second) or len(first) % 2 != 1:
            raise ValueError("intermediate rows must have the same positive odd length")
        check = check_compressed_legendre_constants(first, second, 3)
        if not check.ok:
            raise ValueError(f"invalid factor-three branch: {check.message}")
        self.canonical = canonical
        self.length = 3 * len(first)
        self.compressed_length = len(first)
        self.first_compressed, self.second_compressed = tuple(first), tuple(second)
        self._phases = {}
        self._differences = {}
        variable = 1
        for row, source in enumerate(self.rows):
            for index in range(len(source.active)):
                for phase in range(3):
                    self._phases[row, index, phase] = variable
                    variable += 1
        for row, source in enumerate(self.rows):
            for u, v in combinations(range(len(source.active)), 2):
                for h in range(3):
                    self._differences[row, u, v, h] = variable
                    variable += 1

    @property
    def stats(self) -> PhasePBStats:
        phases, differences = len(self._phases), len(self._differences)
        gauge = sum(bool(row.active) for row in self.rows) if self.canonical else 0
        correlations = self.compressed_length - 1
        equalities = phases // 3 + differences // 3 + gauge + correlations
        channels = 3 * differences
        return PhasePBStats(phases, differences, phases + differences, phases // 3,
                            differences // 3, channels, gauge, correlations,
                            equalities + channels, 2 * equalities + channels)

    def phase_variable(self, row: int, index: int, phase: int) -> int:
        return self._phases[row, index, phase]

    def difference_variable(self, row: int, u: int, v: int, h: int) -> int:
        return self._differences[row, u, v, h]

    def iter_constraints(self) -> Iterator[PBConstraint]:
        for row, source in enumerate(self.rows):
            for index in range(len(source.active)):
                yield PBConstraint(tuple((1, self.phase_variable(row, index, a)) for a in range(3)), "=", 1)
            if self.canonical and source.active:
                yield PBConstraint(((1, self.phase_variable(row, 0, 0)),), "=", 1)
            for u, v in combinations(range(len(source.active)), 2):
                yield PBConstraint(tuple((1, self.difference_variable(row, u, v, h))
                                         for h in range(3)), "=", 1)
                for a in range(3):
                    for b in range(3):
                        yield PBConstraint(((-1, self.phase_variable(row, u, a)),
                                            (-1, self.phase_variable(row, v, b)),
                                            (1, self.difference_variable(row, u, v, (b-a) % 3))), ">=", -1)
        for shift in range(1, self.compressed_length):
            constant = 0
            coefficients = []
            for row, source in enumerate(self.rows):
                offset, terms = source.paf_terms(shift)
                constant += offset
                coefficients.extend((weight // 4, self.difference_variable(row, u, v, h))
                                    for u, v, h, weight in terms)
            if (-2 - constant) % 4:
                raise AssertionError("phase PAF target must be divisible by four")
            # Nonempty for the structured branches; represent a constant-only
            # equation with a canceling phase pair if a general branch needs it.
            if not coefficients:
                coefficients = [(1, 1), (-1, 1)]
            yield PBConstraint(tuple(coefficients), "=", (-2 - constant) // 4)

    def canonicalize_pair(self, first: Sequence[int], second: Sequence[int]):
        return tuple(row.decode(row.canonical_phases(row.encode(binary)))
                     for row, binary in zip(self.rows, (first, second), strict=True))

    def assignment_for_pair(self, first: Sequence[int], second: Sequence[int]) -> dict[int, int]:
        phases = tuple(row.encode(binary) for row, binary in zip(self.rows, (first, second), strict=True))
        assignment = {variable: int(phases[row][i] == a)
                      for (row, i, a), variable in self._phases.items()}
        assignment.update({variable: int((phases[row][v] - phases[row][u]) % 3 == h)
                           for (row, u, v, h), variable in self._differences.items()})
        return assignment

    def pair_from_assignment(self, assignment: Mapping[int, int]):
        if set(assignment) != set(range(1, self.stats.variables + 1)):
            raise ValueError("expected a complete assignment")
        if any(not c.satisfied_by(assignment) for c in self.iter_constraints()):
            raise ValueError("assignment fails the phase OPB")
        pair = tuple(row.decode(tuple(next(a for a in range(3)
                                          if assignment[self.phase_variable(r, i, a)])
                                      for i in range(len(row.active))))
                     for r, row in enumerate(self.rows))
        if not check_legendre_pair(*pair).ok:
            raise AssertionError("phase OPB witness failed full exact PAF")
        return pair

    def first_failed_constraint(self, first, second, *, constraints=None):
        assignment = self.assignment_for_pair(first, second)
        for index, constraint in enumerate(self.iter_constraints() if constraints is None else constraints):
            if not constraint.satisfied_by(assignment):
                return index
        return None

    def write_opb(self, path: Path) -> OPBArtifact:
        path.parent.mkdir(parents=True, exist_ok=True)
        stats = self.stats
        equalities = stats.normalized_inequalities - stats.constraint_records
        with path.open("w", encoding="ascii", newline="\n") as stream:
            stream.write(f"* #variable= {stats.variables} #constraint= {stats.constraint_records} "
                         f"#equal= {equalities} intsize= 4\n")
            stream.write("* ternary phases and exact shared phase differences; anchor phase zero\n")
            for constraint in self.iter_constraints():
                stream.write(constraint.to_opb())
        data = path.read_bytes()
        return OPBArtifact(path, len(data), sha256(data).hexdigest())


@dataclass(frozen=True)
class PhaseSearch:
    complete: bool
    stop_reason: str
    elapsed_seconds: float
    stored_candidates: int
    streamed_candidates: int
    stored_signatures: int
    canonical_pairs: int
    ordered_pairs: int
    solutions: tuple


def search_phase_uncompressions(first: Sequence[int], second: Sequence[int], *,
                                time_limit: float | None = None,
                                max_candidates_per_side: int = 1_000_000,
                                max_stored_signatures: int = 250_000,
                                collect: int = 1,
                                evaluation: str = "incremental") -> PhaseSearch:
    """Exact Gray-update join, with explicit partial-result semantics and caps.

    Count multiplicities in anchor-zero representatives; ordered counts are
    multiplied by the exact independent translation orbit size. Partial
    counts are lower bounds, never nonexistence certificates.
    """
    model = TernaryPhasePBModel(first, second)
    if max_candidates_per_side <= 0 or max_stored_signatures <= 0 or collect < 0:
        raise ValueError("positive resource caps and nonnegative collect required")
    if time_limit is not None and time_limit <= 0:
        raise ValueError("time limit must be positive")
    if evaluation not in {"incremental", "packed"}:
        raise ValueError("evaluation must be incremental or packed")
    rows = model.rows
    stored = min(range(2), key=lambda r: rows[r].canonical_count)
    streamed = 1 - stored
    start = perf_counter()
    table = {}
    counts = [0, 0]
    pairs = 0
    solutions = []
    orbit_size = (3 if rows[0].active else 1) * (3 if rows[1].active else 1)

    def finish(complete, reason):
        return PhaseSearch(complete, reason, perf_counter() - start, counts[stored],
                           counts[streamed], len(table), pairs, orbit_size * pairs, tuple(solutions))

    for side in (stored, streamed):
        candidates = (rows[side].iter_projected_signatures() if evaluation == "incremental"
                      else rows[side].iter_packed_signatures())
        for phases, signature in candidates:
            if counts[side] >= max_candidates_per_side:
                return finish(False, "candidate_limit")
            if time_limit is not None and perf_counter() - start >= time_limit:
                return finish(False, "time_limit")
            counts[side] += 1
            if side == stored:
                if signature in table:
                    multiplicity, representative = table[signature]
                    table[signature] = multiplicity + 1, representative
                else:
                    if len(table) >= max_stored_signatures:
                        return finish(False, "signature_limit")
                    table[signature] = 1, phases
            else:
                match = table.get(tuple(-2 - value for value in signature))
                if match:
                    multiplicity, other = match
                    pairs += multiplicity
                    if len(solutions) < collect:
                        phase_pair = (other, phases) if stored == 0 else (phases, other)
                        pair = tuple(row.decode(a) for row, a in zip(rows, phase_pair, strict=True))
                        if not check_legendre_pair(*pair).ok:
                            raise AssertionError("phase join failed full exact PAF")
                        solutions.append(pair)
    return finish(True, "exhausted")
