"""Exact coordinate symmetries for cyclic Legendre-pair searches."""

from __future__ import annotations

from math import gcd
from typing import Sequence


IntegerSequence = tuple[int, ...]


def _validate_sign_sequence(sequence: Sequence[int]) -> IntegerSequence:
    result = tuple(sequence)
    if not result:
        raise ValueError("sequence must be nonempty")
    if any(value not in {-1, 1} for value in result):
        raise ValueError("sequence entries must be -1 or +1")
    return result


def cyclic_translate(sequence: Sequence[int], offset: int) -> IntegerSequence:
    """Return ``translated[i] = sequence[i + offset]`` with cyclic indices."""

    source = _validate_sign_sequence(sequence)
    length = len(source)
    return tuple(source[(index + offset) % length] for index in range(length))


def reverse_cyclic(sequence: Sequence[int]) -> IntegerSequence:
    """Return the index-negated row ``reversed[i] = sequence[-i]``."""

    source = _validate_sign_sequence(sequence)
    length = len(source)
    return tuple(source[-index % length] for index in range(length))


def multiplier_permute(sequence: Sequence[int], multiplier: int) -> IntegerSequence:
    """Return ``permuted[i] = sequence[multiplier*i]`` for a unit multiplier."""

    source = _validate_sign_sequence(sequence)
    length = len(source)
    if gcd(multiplier, length) != 1:
        raise ValueError(f"multiplier {multiplier} is not a unit modulo {length}")
    return tuple(source[(multiplier * index) % length] for index in range(length))


def residue_zero_bits(sequence: Sequence[int], compressed_length: int) -> tuple[int, ...]:
    """Return the negative-sign bits in residue class zero of a compression."""

    source = _validate_sign_sequence(sequence)
    if compressed_length <= 0 or len(source) % compressed_length:
        raise ValueError("compressed length must be a positive divisor of the row length")
    factor = len(source) // compressed_length
    return tuple(int(source[step * compressed_length] == -1) for step in range(factor))


def least_cyclic_period(values: Sequence[int]) -> int:
    """Return the least positive cyclic period of a nonempty finite word."""

    word = tuple(values)
    if not word:
        raise ValueError("word must be nonempty")
    for period in range(1, len(word) + 1):
        if len(word) % period == 0 and all(
            word[index] == word[index % period] for index in range(len(word))
        ):
            return period
    raise AssertionError("the full word must always be a period")


def canonical_residue_translation(
    sequence: Sequence[int], compressed_length: int
) -> tuple[IntegerSequence, int]:
    """Choose the least residue-zero bit rotation under translations by ``d``.

    The returned offset is a multiple of ``compressed_length``.  Ties are
    resolved by the least nonnegative offset; for the structured factor-nine
    target the residue-zero word has four negative bits and hence period nine,
    so the minimizing offset is unique.
    """

    source = _validate_sign_sequence(sequence)
    bits = residue_zero_bits(source, compressed_length)
    rotations = [bits[step:] + bits[:step] for step in range(len(bits))]
    best_step = min(range(len(bits)), key=lambda step: (rotations[step], step))
    offset = best_step * compressed_length
    return cyclic_translate(source, offset), offset
