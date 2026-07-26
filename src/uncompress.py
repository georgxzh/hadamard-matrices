"""Exact binary uncompression of a prescribed compressed Legendre pair.

Given compressed rows ``A`` and ``B`` of length ``d`` and an aggregation
factor ``m``, a binary uncompression is a pair of sequences in
``{-1,1}**(d*m)`` whose residue-class sums reproduce ``A`` and ``B``.  The
pair is accepted only when it satisfies the binary Legendre-pair equations at
every nonzero shift.

The enumeration is exact.  Sequences are bit-packed, with bit ``i`` set when
entry ``i`` is ``-1``, and periodic autocorrelation is evaluated as

``PAF(s) = L - 2 * popcount(x XOR rotate(x, s))``,

which is integer arithmetic throughout; no floating-point Fourier value is
used at any stage.  Because ``PAF(s) == PAF(L-s)``, only shifts
``1..L//2`` are stored, and two uncompressions pair up exactly when their
stored vectors sum entrywise to ``-2``.

The cost is combinatorial: one row admits
``prod_j C(m, (m - A_j)//2)`` uncompressions.  Call
:func:`uncompression_count` before enumerating anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import comb
from typing import Iterator, Sequence

from src.legendre import check_legendre_pair


IntegerSequence = tuple[int, ...]


@dataclass(frozen=True)
class UncompressionSearch:
    """Summary of one exact uncompression search."""

    output_length: int
    factor: int
    uncompressed_length: int
    first_candidates: int
    second_candidates: int
    distinct_second_vectors: int
    pairs_found: int
    solutions: tuple[tuple[IntegerSequence, IntegerSequence], ...]


def _class_negative_count(target: int, factor: int) -> int:
    """Return how many ``-1`` entries a residue class with the given sum has."""

    if (factor - target) % 2:
        raise ValueError(f"compressed entry {target} has wrong parity for factor {factor}")
    negatives = (factor - target) // 2
    if not 0 <= negatives <= factor:
        raise ValueError(f"compressed entry {target} is out of range for factor {factor}")
    return negatives


def uncompression_count(compressed: Sequence[int], factor: int) -> int:
    """Return the exact number of binary uncompressions of one compressed row."""

    if factor <= 0:
        raise ValueError("factor must be positive")
    total = 1
    for target in compressed:
        total *= comb(factor, _class_negative_count(target, factor))
    return total


def iter_uncompression_masks(compressed: Sequence[int], factor: int) -> Iterator[int]:
    """Yield every binary uncompression of one compressed row as a bitmask.

    Bit ``i`` of the yielded mask is set exactly when entry ``i`` is ``-1``.
    Residue class ``j`` occupies positions ``j, j+d, ..., j+(m-1)d``.
    """

    output_length = len(compressed)
    if output_length == 0:
        raise ValueError("compressed row must be nonempty")
    per_class: list[list[int]] = []
    for index, target in enumerate(compressed):
        positions = [index + step * output_length for step in range(factor)]
        negatives = _class_negative_count(target, factor)
        per_class.append(
            [
                sum(1 << positions[slot] for slot in choice)
                for choice in combinations(range(factor), negatives)
            ]
        )
    for parts in product(*per_class):
        mask = 0
        for part in parts:
            mask |= part
        yield mask


def mask_to_sequence(mask: int, length: int) -> IntegerSequence:
    """Convert a bitmask back to a ``{-1,1}`` sequence."""

    return tuple(-1 if (mask >> index) & 1 else 1 for index in range(length))


def paf_signature(mask: int, length: int) -> IntegerSequence:
    """Return exact PAF values at shifts ``1..length//2`` for a packed sequence.

    ``PAF(s) = length - 2 * popcount(x XOR rotate(x, s))`` counts sign
    disagreements exactly.  Shifts above ``length//2`` are omitted because
    ``PAF(s) == PAF(length - s)``.
    """

    full = (1 << length) - 1
    signature = []
    for shift in range(1, length // 2 + 1):
        rotated = ((mask >> shift) | (mask << (length - shift))) & full
        signature.append(length - 2 * (mask ^ rotated).bit_count())
    return tuple(signature)


def search_uncompressions(
    first: Sequence[int],
    second: Sequence[int],
    factor: int,
    *,
    limit: int | None = None,
    collect: int = 1,
) -> UncompressionSearch:
    """Enumerate binary uncompressions and return exactly verified pairs.

    ``limit`` optionally caps the number of candidates scanned on each side so
    that callers can probe cost before committing.  ``collect`` bounds how many
    solution pairs are materialised as sequences; the count of matches is
    reported in full regardless.

    Every returned pair is re-checked with :func:`check_legendre_pair`, so the
    bit-packed fast path can never by itself admit a wrong answer.
    """

    if len(first) != len(second):
        raise ValueError(f"length mismatch: {len(first)} != {len(second)}")
    if collect < 0:
        raise ValueError("collect must be non-negative")
    output_length = len(first)
    length = output_length * factor

    table: dict[IntegerSequence, int] = {}
    second_scanned = 0
    for mask in iter_uncompression_masks(second, factor):
        if limit is not None and second_scanned >= limit:
            break
        second_scanned += 1
        table.setdefault(paf_signature(mask, length), mask)

    solutions: list[tuple[IntegerSequence, IntegerSequence]] = []
    pairs_found = 0
    first_scanned = 0
    for mask in iter_uncompression_masks(first, factor):
        if limit is not None and first_scanned >= limit:
            break
        first_scanned += 1
        wanted = tuple(-2 - value for value in paf_signature(mask, length))
        partner = table.get(wanted)
        if partner is None:
            continue
        pairs_found += 1
        if len(solutions) < collect:
            left = mask_to_sequence(mask, length)
            right = mask_to_sequence(partner, length)
            check = check_legendre_pair(left, right)
            if not check.ok:
                raise AssertionError(
                    f"bit-packed match failed the exact Legendre check: {check.message}"
                )
            solutions.append((left, right))

    return UncompressionSearch(
        output_length=output_length,
        factor=factor,
        uncompressed_length=length,
        first_candidates=first_scanned,
        second_candidates=second_scanned,
        distinct_second_vectors=len(table),
        pairs_found=pairs_found,
        solutions=tuple(solutions),
    )
