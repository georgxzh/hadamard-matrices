# Exact Legendre-pair framework: implementation plan

Status: LP-1 through LP-4 complete. The Table-4 pairs at lengths 3, 5, 7, and
27 are reproduced, and the structured `pq^2` example is no longer blocked: it
was derived and proved rather than retrieved, and uncompressed exhaustively at
`p=3` (see `pq2_derivation.md`). LP-5 is in progress; its artifact-audit item
is partly superseded and its direction decision is recorded in
`direction_selection.md`.

The target is an auditable exact framework, not an order-333 search. The
phases below are deliberately sequential.

## Phase LP-1: primary-source derivation -- complete

1. Audit the complete Fletcher-Gysin-Seberry paper and the original
   difference-set formulation.
2. Fix one zero-based convention for periodic shifts, DFT signs, support sets,
   and sequence normalization.
3. Derive on paper and in tests the implication
   `LP(L) -> H(2L+2)`, including every border sign and reversal.
4. Record which statements concern binary Legendre pairs, generalized pairs,
   or supplementary difference sets; do not silently conflate them.

Deliverable: a derivation note with a small hand-checkable example.

## Phase LP-2: exact core -- complete

Implement pure functions for:

- periodic autocorrelation (PAF) over Python integers;
- exact cyclic convolution and support-set difference multiplicities;
- the Legendre condition
  \(\operatorname{PAF}_a(s)+\operatorname{PAF}_b(s)=-2\) for every
  \(s\ne0\);
- exact special-frequency PSD values using cyclotomic/integer arithmetic;
- a numerical FFT helper only as a diagnostic, never as an acceptance test;
- construction of the full bordered block matrix;
- validation of the constructed matrix by both existing exact verifiers.

Tests must cover valid and corrupted small pairs, all shifts, normalization
equivalences, and a case that passes approximate but fails exact constraints.

## Phase LP-3: compression identities -- complete

Audit `djokovic2015compression` in full, then implement generic
\(m\)-compression where \(m\mid L\):

\[
A_j=\sum_{i\equiv j\pmod m} a_i.
\]

The API will enforce exact entry range and parity, row-sum preservation, and

\[
\operatorname{PAF}_A(s)
=\sum_{k\equiv s\pmod m}\operatorname{PAF}_a(k).
\]

Specialized, tested views are required for length 333:

| compression | output length | aggregation factor |
|---:|---:|---:|
| 3-compression | 3 | 111 |
| 9-compression | 9 | 37 |
| 37-compression | 37 | 9 |

Also test composition consistency, e.g. direct 3-compression equals
9-compression followed by 3-compression.

## Phase LP-4: published small reproductions -- complete

Reproduce at least two published Legendre pairs, including one length
divisible by 3 and one reported `pq^2` example. For each:

- reconstruct source sequences rather than accepting a final matrix;
- verify exact PAF and applicable PSD/compression identities;
- construct and dual-verify the corresponding full Hadamard matrix;
- record source data hashes and every convention.

Only after these pass should the length-333 code path be considered trusted.

## Phase LP-5: length-333 audit and direction decision -- next

1. Audit the complete artifacts and certificates behind recent
   length-333 computations.
2. Reproduce cheap counts/invariants; do not repeat large enumerations without
   an estimate and approval.
3. Build a constraint inventory for unrestricted pairs and for each surviving
   multiplier scenario.
4. Recommend:
   - **primary direction:** structured `pq^2` uncompression at
     \(333=37\cdot3^2\), if small examples reproduce;
   - **backup direction:** low-order separate-multiplier / translation
     symmetry or exact SAT/CP-SAT on compressed candidates;
   - **deprioritized direction:** common multipliers of order at least 9,
     subject to independent certificate audit.

The decision report must distinguish theorem, reproduced computation,
heuristic, conjecture, and open case. Any run expected to exceed four cores,
30 minutes, or 10 GB requires prior approval.
