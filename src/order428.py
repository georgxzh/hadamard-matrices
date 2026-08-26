"""Exact Kharaghani--Tayfeh-Rezaie construction of order 428.

The construction is implemented as a sequence of independently checkable
maps:

    TT(n) -> BS(2n-1, 2n-1, n, n) -> T(3n-1) -> H(12n-4).

All indexing is zero-based.  Sequence entries are coefficients in display
order, and every correlation in the first three stages is nonperiodic (zero
outside the listed coefficient range).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


BinarySequence = tuple[int, ...]
TernarySequence = tuple[int, ...]
IntegerMatrix = list[list[int]]


@dataclass(frozen=True)
class CorrelationCheck:
    """Exact result of a complementary-sequence constraint check."""

    ok: bool
    checked_shifts: int
    failure_shift: int | None = None
    failure_value: int | None = None
    message: str = ""


def _as_tuple(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(int(value) for value in values)


def _require_alphabet(sequence: Sequence[int], alphabet: set[int], name: str) -> None:
    for index, value in enumerate(sequence):
        if value not in alphabet:
            raise ValueError(f"{name}[{index}]={value}; expected one of {sorted(alphabet)}")


def nonperiodic_autocorrelation(sequence: Sequence[int], shift: int) -> int:
    """Return ``sum_i sequence[i] * sequence[i+shift]`` with zero padding."""

    if shift < 0:
        raise ValueError("shift must be nonnegative")
    if shift >= len(sequence):
        return 0
    return sum(sequence[index] * sequence[index + shift] for index in range(len(sequence) - shift))


def _complementary_check(
    sequences: Sequence[Sequence[int]],
    weights: Sequence[int],
    maximum_shift: int,
) -> CorrelationCheck:
    for shift in range(1, maximum_shift + 1):
        value = sum(
            weight * nonperiodic_autocorrelation(sequence, shift)
            for sequence, weight in zip(sequences, weights, strict=True)
        )
        if value != 0:
            return CorrelationCheck(
                False,
                shift,
                failure_shift=shift,
                failure_value=value,
                message=f"weighted nonperiodic autocorrelation is {value} at shift {shift}",
            )
    return CorrelationCheck(True, maximum_shift, message=f"all shifts 1..{maximum_shift} vanish exactly")


def check_turyn_type(sequences: Sequence[Sequence[int]]) -> CorrelationCheck:
    """Check the exact ``TT(n)`` definition used in the order-428 paper."""

    if len(sequences) != 4:
        raise ValueError(f"expected four Turyn-type sequences, got {len(sequences)}")
    x, y, z, w = sequences
    n = len(x)
    if n == 0 or (len(y), len(z), len(w)) != (n, n, n - 1):
        raise ValueError(
            f"expected lengths (n,n,n,n-1), got {(len(x), len(y), len(z), len(w))}"
        )
    for name, sequence in zip(("X", "Y", "Z", "W"), sequences, strict=True):
        _require_alphabet(sequence, {-1, 1}, name)
    return _complementary_check(sequences, (1, 1, 2, 2), n - 1)


def turyn_type_to_base(sequences: Sequence[Sequence[int]]) -> tuple[BinarySequence, ...]:
    """Apply Theorem 1 of Kharaghani--Tayfeh-Rezaie exactly."""

    check = check_turyn_type(sequences)
    if not check.ok:
        raise ValueError(f"invalid Turyn-type input: {check.message}")
    x, y, z, w = map(_as_tuple, sequences)
    return z + w, z + tuple(-value for value in w), x, y


def check_base_sequences(sequences: Sequence[Sequence[int]]) -> CorrelationCheck:
    """Check ``BS(n+p,n+p,n,n)`` using exact nonperiodic correlations."""

    if len(sequences) != 4:
        raise ValueError(f"expected four base sequences, got {len(sequences)}")
    a, b, c, d = sequences
    if len(a) == 0 or len(a) != len(b) or len(c) != len(d) or len(a) < len(c):
        raise ValueError(
            "expected base-sequence lengths (n+p,n+p,n,n), got "
            f"{(len(a), len(b), len(c), len(d))}"
        )
    for name, sequence in zip(("A", "B", "C", "D"), sequences, strict=True):
        _require_alphabet(sequence, {-1, 1}, name)
    return _complementary_check(sequences, (1, 1, 1, 1), len(a) - 1)


def base_to_t_sequences(sequences: Sequence[Sequence[int]]) -> tuple[TernarySequence, ...]:
    """Map base sequences to four T-sequences as displayed in the paper."""

    check = check_base_sequences(sequences)
    if not check.ok:
        raise ValueError(f"invalid base-sequence input: {check.message}")
    a, b, c, d = map(_as_tuple, sequences)
    n = len(c)
    zero_n = (0,) * n
    zero_long = (0,) * len(a)
    t1 = tuple((left + right) // 2 for left, right in zip(a, b, strict=True)) + zero_n
    t2 = tuple((left - right) // 2 for left, right in zip(a, b, strict=True)) + zero_n
    t3 = zero_long + tuple((left + right) // 2 for left, right in zip(c, d, strict=True))
    t4 = zero_long + tuple((left - right) // 2 for left, right in zip(c, d, strict=True))
    result = t1, t2, t3, t4
    t_check = check_t_sequences(result)
    if not t_check.ok:
        raise AssertionError(f"base-to-T theorem failed: {t_check.message}")
    return result


def check_t_sequences(sequences: Sequence[Sequence[int]]) -> CorrelationCheck:
    """Check equal lengths, disjoint support, and exact complementarity."""

    if len(sequences) != 4:
        raise ValueError(f"expected four T-sequences, got {len(sequences)}")
    length = len(sequences[0])
    if length == 0 or any(len(sequence) != length for sequence in sequences):
        raise ValueError(f"expected four nonempty equal lengths, got {tuple(map(len, sequences))}")
    for sequence_index, sequence in enumerate(sequences, start=1):
        _require_alphabet(sequence, {-1, 0, 1}, f"T{sequence_index}")
    for index, column in enumerate(zip(*sequences, strict=True)):
        support_size = sum(value != 0 for value in column)
        if support_size != 1:
            return CorrelationCheck(
                False,
                0,
                message=f"coordinate {index} has support size {support_size}; expected 1",
            )
    return _complementary_check(sequences, (1, 1, 1, 1), length - 1)


def circulant(first_row: Sequence[int]) -> IntegerMatrix:
    """Return the circulant whose row ``i`` is a right shift by ``i``."""

    row = list(first_row)
    if not row:
        raise ValueError("a circulant must be nonempty")
    size = len(row)
    return [[row[(column - line) % size] for column in range(size)] for line in range(size)]


def _transpose(matrix: IntegerMatrix) -> IntegerMatrix:
    return [list(column) for column in zip(*matrix, strict=True)]


def _times_reversal(matrix: IntegerMatrix) -> IntegerMatrix:
    """Right-multiply a matrix by the back-diagonal identity."""

    return [list(reversed(row)) for row in matrix]


def _scale(matrix: IntegerMatrix, scalar: int) -> IntegerMatrix:
    return [[scalar * value for value in row] for row in matrix]


def _join_block_rows(block_rows: Sequence[Sequence[IntegerMatrix]]) -> IntegerMatrix:
    block_size = len(block_rows[0][0])
    result: IntegerMatrix = []
    for block_row in block_rows:
        if len(block_row) != 4:
            raise ValueError("the Goethals--Seidel array requires four block columns")
        for local_row in range(block_size):
            result.append(
                [value for block in block_row for value in block[local_row]]
            )
    return result


def t_sequences_to_hadamard(sequences: Sequence[Sequence[int]]) -> IntegerMatrix:
    """Construct the paper's exact Goethals--Seidel array of order ``4m``."""

    check = check_t_sequences(sequences)
    if not check.ok:
        raise ValueError(f"invalid T-sequence input: {check.message}")
    t1, t2, t3, t4 = map(_as_tuple, sequences)
    first_rows = (
        tuple(a + b + c + d for a, b, c, d in zip(t1, t2, t3, t4, strict=True)),
        tuple(-a + b + c - d for a, b, c, d in zip(t1, t2, t3, t4, strict=True)),
        tuple(-a - b + c + d for a, b, c, d in zip(t1, t2, t3, t4, strict=True)),
        tuple(-a + b - c + d for a, b, c, d in zip(t1, t2, t3, t4, strict=True)),
    )
    for index, row in enumerate(first_rows, start=1):
        _require_alphabet(row, {-1, 1}, f"circulant first row A{index}")
    a1, a2, a3, a4 = map(circulant, first_rows)
    a2r = _times_reversal(a2)
    a3r = _times_reversal(a3)
    a4r = _times_reversal(a4)
    a2tr = _times_reversal(_transpose(a2))
    a3tr = _times_reversal(_transpose(a3))
    a4tr = _times_reversal(_transpose(a4))
    return _join_block_rows(
        (
            (a1, a2r, a3r, a4r),
            (_scale(a2r, -1), a1, a4tr, _scale(a3tr, -1)),
            (_scale(a3r, -1), _scale(a4tr, -1), a1, a2tr),
            (_scale(a4r, -1), a3tr, _scale(a2tr, -1), a1),
        )
    )


def hadamard_from_turyn_type(sequences: Sequence[Sequence[int]]) -> IntegerMatrix:
    """Run the complete exact construction pipeline."""

    return t_sequences_to_hadamard(base_to_t_sequences(turyn_type_to_base(sequences)))


def _decode_signs(display: str) -> BinarySequence:
    tokens = display.split()
    invalid = [token for token in tokens if token not in {"+", "-"}]
    if invalid:
        raise ValueError(f"invalid sign tokens: {invalid}")
    return tuple(1 if token == "+" else -1 for token in tokens)


def published_tt36() -> tuple[BinarySequence, ...]:
    """Return the four sequences printed in KTR 2005, page 5.

    The transcription was checked against the paper's rendered page and the
    independent hexadecimal encoding currently shipped by SageMath.
    """

    x = _decode_signs(
        "+ + + - - - - + + - + - + - - - - - + + + + - + + - + + + + - - - - + -"
    )
    y = _decode_signs(
        "+ - + + + + + - - + - + - - + - - + + - - + + + + - + + + + - - - + + -"
    )
    z = _decode_signs(
        "+ - + + + + + - + - - + + + + - + + + - + + - - + + + - + - - + - - - +"
    )
    w = _decode_signs(
        "+ + + - + - - - - - + + - - + - + + + - - + - + - + + + - + + + + - +"
    )
    return x, y, z, w


def published_tt4() -> tuple[BinarySequence, ...]:
    """Small published TT(4) example used as a hand-checkable regression."""

    return (
        (1, 1, 1, 1),
        (1, 1, -1, 1),
        (1, 1, -1, -1),
        (1, -1, 1),
    )
