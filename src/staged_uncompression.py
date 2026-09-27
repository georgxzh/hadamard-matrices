"""Exact factor-three branch model for successive q-uncompression.

For ``q=3``, a length-``9p`` binary pair may first be 3-compressed to an
integer pair of length ``3p`` and then 3-compressed again to the prescribed
length-``p`` pair.  This module validates a fixed intermediate branch and
builds its exact binary second-stage OPB model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from src.legendre import check_compressed_legendre_constants, compress
from src.pb_model import UncompressionPBModel


IntegerSequence = tuple[int, ...]


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

    def model(self, *, canonical_translations: bool = False) -> UncompressionPBModel:
        """Return the exact binary uncompression model for this fixed branch."""

        return UncompressionPBModel(
            self.intermediate_first,
            self.intermediate_second,
            3,
            canonical_translations=canonical_translations,
            canonical_residues=(self.canonical_residues if canonical_translations else None),
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
            raise ValueError(f"intermediate pair violates compressed PAF constants: {check.message}")
