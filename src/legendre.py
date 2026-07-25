"""Exact arithmetic for binary Legendre pairs and their compressions.

Conventions follow Fletcher--Gysin--Seberry (2001) and
Djokovic--Kotsireas (2015):

* sequence indices and periodic shifts are zero-based;
* ``PAF_a(s) = sum_i a[i] * a[(i+s) mod n]``;
* the DFT root has positive sign, ``exp(2*pi*i/n)``;
* an ``m``-compression of a length ``n=d*m`` sequence has length ``d`` and
  entry ``j`` equal to ``sum_r a[j+r*d]``.

All acceptance checks use Python integers.  PSD values are represented in a
cyclotomic quotient ring; no floating-point Fourier value is a certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import cos, gcd, pi, sin
from typing import Iterable, Sequence

from src.order428 import circulant


IntegerSequence = tuple[int, ...]
IntegerMatrix = list[list[int]]


@dataclass(frozen=True)
class LegendreCheck:
    """Exact result of checking the binary Legendre-pair definition."""

    ok: bool
    length: int
    checked_shifts: int
    failure_shift: int | None = None
    failure_value: int | None = None
    message: str = ""


@dataclass(frozen=True)
class SDSCheck:
    """Exact result of the supplementary-difference-set check."""

    ok: bool
    length: int
    block_sizes: tuple[int, int]
    lambda_value: int
    checked_differences: int
    failure_difference: int | None = None
    failure_value: int | None = None
    message: str = ""


@dataclass(frozen=True)
class ExactCyclotomicValue:
    """An exact element of ``Z[x]/Phi_order(x)``.

    ``coefficients[i]`` is the coefficient of ``x**i`` in the unique
    representative of degree less than Euler's totient of ``order``.
    Trailing zero coefficients are omitted; the zero element is ``()``.
    """

    order: int
    coefficients: tuple[int, ...]

    @property
    def is_integer(self) -> bool:
        return len(self.coefficients) <= 1

    @property
    def integer_value(self) -> int:
        if not self.is_integer:
            raise ValueError("cyclotomic value is not a rational integer")
        return self.coefficients[0] if self.coefficients else 0


def _as_tuple(values: Iterable[int]) -> IntegerSequence:
    return tuple(int(value) for value in values)


def _require_nonempty(sequence: Sequence[int], name: str) -> None:
    if not sequence:
        raise ValueError(f"{name} must be nonempty")


def _require_binary(sequence: Sequence[int], name: str) -> None:
    _require_nonempty(sequence, name)
    for index, value in enumerate(sequence):
        if value not in {-1, 1}:
            raise ValueError(f"{name}[{index}]={value}; expected -1 or 1")


def periodic_autocorrelation(sequence: Sequence[int], shift: int) -> int:
    """Return the exact periodic autocorrelation at an arbitrary integer shift."""

    _require_nonempty(sequence, "sequence")
    length = len(sequence)
    shift %= length
    return sum(value * sequence[(index + shift) % length] for index, value in enumerate(sequence))


def periodic_autocorrelations(sequence: Sequence[int]) -> IntegerSequence:
    """Return exact PAF values at shifts ``0, ..., n-1``."""

    return tuple(periodic_autocorrelation(sequence, shift) for shift in range(len(sequence)))


def cyclic_convolution(left: Sequence[int], right: Sequence[int]) -> IntegerSequence:
    """Return exact cyclic convolution of two equal-length integer sequences."""

    _require_nonempty(left, "left")
    if len(left) != len(right):
        raise ValueError(f"length mismatch: {len(left)} != {len(right)}")
    length = len(left)
    return tuple(
        sum(left[index] * right[(output - index) % length] for index in range(length))
        for output in range(length)
    )


def check_legendre_pair(
    first: Sequence[int],
    second: Sequence[int],
    *,
    require_balanced_sums: bool = True,
) -> LegendreCheck:
    """Check the binary Legendre-pair equations at every nonzero shift."""

    _require_binary(first, "first")
    _require_binary(second, "second")
    if len(first) != len(second):
        raise ValueError(f"length mismatch: {len(first)} != {len(second)}")
    length = len(first)
    if length % 2 == 0:
        return LegendreCheck(False, length, 0, message="binary Legendre-pair length must be odd")
    if require_balanced_sums and (abs(sum(first)) != 1 or abs(sum(second)) != 1):
        return LegendreCheck(
            False,
            length,
            0,
            message=f"expected row sums of absolute value 1, got {(sum(first), sum(second))}",
        )
    for shift in range(1, length):
        value = periodic_autocorrelation(first, shift) + periodic_autocorrelation(second, shift)
        if value != -2:
            return LegendreCheck(
                False,
                length,
                shift,
                failure_shift=shift,
                failure_value=value,
                message=f"combined PAF is {value} at shift {shift}; expected -2",
            )
    return LegendreCheck(
        True,
        length,
        length - 1,
        message=f"all shifts 1..{length - 1} have combined PAF -2 exactly",
    )


def normalize_legendre_pair(
    first: Sequence[int], second: Sequence[int]
) -> tuple[IntegerSequence, IntegerSequence]:
    """Independently negate rows so that both row sums are ``+1``."""

    check = check_legendre_pair(first, second)
    if not check.ok:
        raise ValueError(f"invalid Legendre pair: {check.message}")
    normalized = []
    for sequence in (first, second):
        sign = sum(sequence)
        normalized.append(tuple(sign * value for value in sequence))
    return normalized[0], normalized[1]


def negative_support(sequence: Sequence[int]) -> tuple[int, ...]:
    """Return zero-based indices occupied by ``-1``."""

    _require_binary(sequence, "sequence")
    return tuple(index for index, value in enumerate(sequence) if value == -1)


def difference_multiplicities(support: Iterable[int], length: int) -> IntegerSequence:
    """Count ordered differences ``x-y mod length`` within one support block."""

    if length <= 0:
        raise ValueError("length must be positive")
    block = tuple(int(value) for value in support)
    if len(set(block)) != len(block):
        raise ValueError("support contains repeated indices")
    if any(value < 0 or value >= length for value in block):
        raise ValueError(f"support indices must lie in 0..{length - 1}")
    counts = [0] * length
    for left in block:
        for right in block:
            counts[(left - right) % length] += 1
    return tuple(counts)


def check_negative_support_sds(first: Sequence[int], second: Sequence[int]) -> SDSCheck:
    """Check the SDS equivalent of a normalized binary Legendre pair.

    For normalized length ``n`` sequences, both negative supports have size
    ``(n-1)/2`` and every nonzero difference occurs ``(n-3)/2`` times across
    the two blocks.
    """

    _require_binary(first, "first")
    _require_binary(second, "second")
    if len(first) != len(second):
        raise ValueError(f"length mismatch: {len(first)} != {len(second)}")
    length = len(first)
    if length % 2 == 0:
        raise ValueError("binary Legendre-pair length must be odd")
    first_support = negative_support(first)
    second_support = negative_support(second)
    expected_size = (length - 1) // 2
    lambda_value = (length - 3) // 2
    sizes = (len(first_support), len(second_support))
    if sizes != (expected_size, expected_size):
        return SDSCheck(
            False,
            length,
            sizes,
            lambda_value,
            0,
            message=f"block sizes are {sizes}; expected {(expected_size, expected_size)}",
        )
    first_counts = difference_multiplicities(first_support, length)
    second_counts = difference_multiplicities(second_support, length)
    for difference in range(1, length):
        value = first_counts[difference] + second_counts[difference]
        if value != lambda_value:
            return SDSCheck(
                False,
                length,
                sizes,
                lambda_value,
                difference,
                failure_difference=difference,
                failure_value=value,
                message=(
                    f"combined difference multiplicity is {value} at {difference}; "
                    f"expected {lambda_value}"
                ),
            )
    return SDSCheck(
        True,
        length,
        sizes,
        lambda_value,
        length - 1,
        message=f"all nonzero differences have multiplicity {lambda_value}",
    )


def legendre_pair_to_hadamard(first: Sequence[int], second: Sequence[int]) -> IntegerMatrix:
    """Construct the Fletcher--Gysin--Seberry matrix of order ``2n+2``."""

    check = check_legendre_pair(first, second)
    if not check.ok:
        raise ValueError(f"invalid Legendre pair: {check.message}")
    length = len(first)
    a = circulant(first)
    b = circulant(second)
    a_transpose = [list(column) for column in zip(*a, strict=True)]
    b_transpose = [list(column) for column in zip(*b, strict=True)]
    ones = [1] * length
    matrix: IntegerMatrix = [
        [-1, -1, *ones, *ones],
        [-1, 1, *ones, *(-value for value in ones)],
    ]
    matrix.extend([1, 1, *a[row], *b[row]] for row in range(length))
    matrix.extend(
        [1, -1, *b_transpose[row], *(-value for value in a_transpose[row])]
        for row in range(length)
    )
    return matrix


def compress(sequence: Sequence[int], output_length: int) -> IntegerSequence:
    """Compress by residue classes modulo ``output_length``.

    If the input length is ``n=d*m`` and ``output_length=d``, the returned
    entry ``j`` is ``sum(sequence[j+r*d] for r in range(m))``.
    """

    _require_nonempty(sequence, "sequence")
    if output_length <= 0:
        raise ValueError("output_length must be positive")
    if len(sequence) % output_length:
        raise ValueError(
            f"output length {output_length} does not divide input length {len(sequence)}"
        )
    factor = len(sequence) // output_length
    result = tuple(
        sum(sequence[index + repetition * output_length] for repetition in range(factor))
        for index in range(output_length)
    )
    if all(value in {-1, 1} for value in sequence):
        allowed = set(range(-factor, factor + 1, 2))
        if any(value not in allowed for value in result):
            raise AssertionError("binary compression violated its exact range/parity invariant")
    if sum(result) != sum(sequence):
        raise AssertionError("compression failed to preserve the row sum")
    return result


def compression_factor(input_length: int, output_length: int) -> int:
    """Return ``m`` for a length ``d*m`` to length ``d`` compression."""

    if input_length <= 0 or output_length <= 0 or input_length % output_length:
        raise ValueError("positive output_length must divide positive input_length")
    return input_length // output_length


def check_compression_paf_identity(
    sequence: Sequence[int], output_length: int
) -> bool:
    """Check the exact PAF compression identity at every output shift."""

    compressed = compress(sequence, output_length)
    factor = len(sequence) // output_length
    return all(
        periodic_autocorrelation(compressed, shift)
        == sum(
            periodic_autocorrelation(sequence, shift + repetition * output_length)
            for repetition in range(factor)
        )
        for shift in range(output_length)
    )


def check_legendre_compression_constants(
    first: Sequence[int], second: Sequence[int], output_length: int
) -> bool:
    """Check the compressed PAF constants implied by a Legendre pair."""

    check = check_legendre_pair(first, second)
    if not check.ok:
        raise ValueError(f"invalid Legendre pair: {check.message}")
    factor = compression_factor(len(first), output_length)
    compressed_first = compress(first, output_length)
    compressed_second = compress(second, output_length)
    expected_zero = 2 * len(first) - 2 * (factor - 1)
    for shift in range(output_length):
        value = periodic_autocorrelation(
            compressed_first, shift
        ) + periodic_autocorrelation(compressed_second, shift)
        expected = expected_zero if shift == 0 else -2 * factor
        if value != expected:
            return False
    return True


def _trim(polynomial: Sequence[int]) -> IntegerSequence:
    result = list(polynomial)
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def _polynomial_divide_exact(
    dividend: Sequence[int], monic_divisor: Sequence[int]
) -> IntegerSequence:
    divisor = _trim(monic_divisor)
    if not divisor or divisor[-1] != 1:
        raise ValueError("divisor must be a nonzero monic integer polynomial")
    remainder = list(_trim(dividend))
    quotient = [0] * max(0, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor):
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1]
        quotient[degree] = coefficient
        for index, value in enumerate(divisor):
            remainder[degree + index] -= coefficient * value
        while remainder and remainder[-1] == 0:
            remainder.pop()
    if remainder:
        raise ArithmeticError(f"non-exact polynomial division; remainder={remainder}")
    return _trim(quotient)


def _proper_divisors(number: int) -> tuple[int, ...]:
    return tuple(divisor for divisor in range(1, number) if number % divisor == 0)


@lru_cache(maxsize=None)
def cyclotomic_polynomial(order: int) -> IntegerSequence:
    """Return the integer coefficients of the monic cyclotomic polynomial."""

    if order <= 0:
        raise ValueError("cyclotomic order must be positive")
    polynomial = [-1] + [0] * (order - 1) + [1]
    for divisor in _proper_divisors(order):
        polynomial = list(_polynomial_divide_exact(polynomial, cyclotomic_polynomial(divisor)))
    return _trim(polynomial)


def _reduce_mod_monic(
    polynomial: Sequence[int], monic_modulus: Sequence[int]
) -> IntegerSequence:
    modulus = _trim(monic_modulus)
    if not modulus or modulus[-1] != 1:
        raise ValueError("modulus must be a nonzero monic polynomial")
    remainder = list(_trim(polynomial))
    while len(remainder) >= len(modulus):
        degree = len(remainder) - len(modulus)
        coefficient = remainder[-1]
        for index, value in enumerate(modulus):
            remainder[degree + index] -= coefficient * value
        while remainder and remainder[-1] == 0:
            remainder.pop()
    return _trim(remainder)


def exact_psd(sequence: Sequence[int], frequency: int) -> ExactCyclotomicValue:
    """Return ``PSD(sequence, frequency)`` exactly in a cyclotomic basis."""

    _require_nonempty(sequence, "sequence")
    length = len(sequence)
    frequency %= length
    common_divisor = gcd(length, frequency)
    order = length // common_divisor
    primitive_exponent = 0 if order == 1 else frequency // common_divisor
    folded = [0] * order
    for shift, value in enumerate(periodic_autocorrelations(sequence)):
        folded[(primitive_exponent * shift) % order] += value
    coefficients = _reduce_mod_monic(folded, cyclotomic_polynomial(order))
    return ExactCyclotomicValue(order, coefficients)


def exact_psd_sum(
    first: Sequence[int], second: Sequence[int], frequency: int
) -> ExactCyclotomicValue:
    """Return the PSD sum of two equal-length sequences exactly."""

    if len(first) != len(second):
        raise ValueError(f"length mismatch: {len(first)} != {len(second)}")
    left = exact_psd(first, frequency)
    right = exact_psd(second, frequency)
    if left.order != right.order:
        raise AssertionError("equal lengths and frequencies produced unequal cyclotomic orders")
    width = max(len(left.coefficients), len(right.coefficients))
    coefficients = tuple(
        (left.coefficients[index] if index < len(left.coefficients) else 0)
        + (right.coefficients[index] if index < len(right.coefficients) else 0)
        for index in range(width)
    )
    return ExactCyclotomicValue(left.order, _trim(coefficients))


def check_legendre_psd_constraints(first: Sequence[int], second: Sequence[int]) -> bool:
    """Check exactly that every nonzero PSD sum is ``2*n+2``."""

    if len(first) != len(second):
        raise ValueError(f"length mismatch: {len(first)} != {len(second)}")
    target = 2 * len(first) + 2
    return all(
        (value := exact_psd_sum(first, second, frequency)).is_integer
        and value.integer_value == target
        for frequency in range(1, len(first))
    )


def exact_psd_at_third_root(compressed_length_three: Sequence[int]) -> int:
    """Return the exact PSD at a primitive third root.

    For ``(x0,x1,x2)`` this is
    ``(3*sum(x_i**2) - sum(x_i)**2)/2``.
    """

    if len(compressed_length_three) != 3:
        raise ValueError("expected a length-3 compressed sequence")
    numerator = 3 * sum(value * value for value in compressed_length_three) - sum(
        compressed_length_three
    ) ** 2
    if numerator % 2:
        raise ArithmeticError("third-root PSD numerator unexpectedly odd")
    return numerator // 2


def evaluate_cyclotomic(value: ExactCyclotomicValue) -> complex:
    """Numerically evaluate an exact value for diagnostics only."""

    angle = 2 * pi / value.order
    root = complex(cos(angle), sin(angle))
    return sum(coefficient * root**power for power, coefficient in enumerate(value.coefficients))


def decode_signs(display: str) -> IntegerSequence:
    """Decode a compact ``+``/``-`` sequence used in published tables."""

    invalid = [symbol for symbol in display if symbol not in {"+", "-"}]
    if invalid:
        raise ValueError(f"invalid sign characters: {invalid}")
    if not display:
        raise ValueError("display must be nonempty")
    return tuple(1 if symbol == "+" else -1 for symbol in display)


def published_legendre_pair_3() -> tuple[IntegerSequence, IntegerSequence]:
    """Return the length-3 pair printed in Fletcher et al. (2001), Table 4."""

    return decode_signs("++-"), decode_signs("++-")


def published_legendre_pair_5() -> tuple[IntegerSequence, IntegerSequence]:
    """Return the length-5 pair printed in Fletcher et al. (2001), Table 4."""

    return decode_signs("+++--"), decode_signs("++-+-")


def published_legendre_pair_7() -> tuple[IntegerSequence, IntegerSequence]:
    """Return the length-7 pair printed in Fletcher et al. (2001), Table 4."""

    sequence = decode_signs("+++-+--")
    return sequence, sequence


def published_legendre_pair_27() -> tuple[IntegerSequence, IntegerSequence]:
    """Return the length-27 pair printed in Fletcher et al. (2001), Table 4.

    The final three signs in the first row and one sign in the second row are
    absent from the PDF's OCR text layer. They were recovered from the
    rendered glyphs and are protected by full PAF, SDS, PSD, compression, and
    Hadamard-matrix regression tests.
    """

    return (
        decode_signs("+++++-+-+-++++--++---+-----"),
        decode_signs("++-++--++--+-++++---+-+--+-"),
    )
