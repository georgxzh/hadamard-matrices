# Length-333 computational audit and direction decision

Status: phase-level audit complete on 2026-07-25; external search artifacts and
certificates listed below remain unavailable. No length-333 enumeration or
stochastic search was run in this repository.

This note distinguishes theorem, reproduced computation, reported computation,
heuristic evidence, and open cases. Bibliographic keys refer to
`references/references.bib`.

## Exact target and implemented constraints

A normalized binary LP(333) consists of two 333-entry sign rows with sums
`+1` and combined nonzero PAF `-2`. Equivalently, the two negative supports
would be an SDS with parameters `(333;166,166;165)`. Such a pair would yield a
complete H(668) by the exactly reproduced bordered construction. The converse
is not asserted.

**Reproduced computation.** `src/legendre.py` now checks the all-shift PAF and
SDS systems, represents every PSD exactly modulo the appropriate cyclotomic
polynomial, and implements output lengths 3, 9, and 37. Deterministic synthetic
length-333 tests establish the compression and sampled-PSD plumbing, not the
existence of an LP(333).

The exact compressed combined PAF constants are:

| output length | factor | shift zero | nonzero shift |
|---:|---:|---:|---:|
| 3 | 111 | 446 | -222 |
| 9 | 37 | 594 | -74 |
| 37 | 9 | 650 | -18 |

At output length 3, normalized rows are odd-entry triples with individual sums
one and the six squares must sum to 446. This is a necessary condition from
`kotsireas2021mod3`, now independently reproduced in exact arithmetic.

## Structured q-squared uncompression

**Theorem and reported computation (`kotsireas2027pq2`).** For odd primes
`p,q`, the paper proves that the length-`p` rows

```text
A(p,q) = [1, q*chi(1), ..., q*chi(p-1)]
B(p,q) = [1,-q*chi(1), ...,-q*chi(p-1)]
```

have the exact necessary properties for a factor-`q^2` compressed Legendre
pair. It reports successful uncompressions at LP(27), LP(45), LP(63), and
LP(75). The universal uncompression statement is explicitly a conjecture.
For `p=37,q=3`, the prescribed output-length-37 rows are therefore a candidate
route to LP(333), not a construction of LP(333).

**Reproduced computation.** The independent 2001 Table-4 LP(27) and its H(56)
are reproduced, including factor-9 compression. Its compressed rows differ
from the newer prescribed `A(3,3),B(3,3)`, so it does not validate the newer
uncompression mechanism.

**Retrieval gap — closed 2026-07-26.** The newer source sequences are embedded
as dynamic figures; the direct PDF is HTTP-403 blocked and publisher browser
access presents a CAPTCHA. Retrieval is no longer required: the rows are
determined by the quadratic-character formula, and their compressed-Legendre
property is proved from the Jacobsthal sum in `pq2_derivation.md`. The derived
`A(37,3), B(37,3)` reproduce the `650` and `-18` constants tabulated above by
an independent route. The factor-9 uncompression is reproduced end to end at
`p=3, q=3`, recovering 7,614 binary LP(27) solutions and a dual-verified
H(56).

**Feasibility — resolved negatively.** One row of `A(37,3)` admits
`126 * 84^36 ~ 2.4e71` binary uncompressions. Direct enumeration is impossible
by about fifty orders of magnitude. The route survives only as a
constraint-satisfaction problem, not as a search over candidates. See
`pq2_derivation.md` section 5.

## Previously reported length-333 searches

### Nine-compressed enumeration -- `chojecki2026status`

**Reported computation, not reproduced.** The technical report states that
12,017,243 PSD-compatible 9-compressed column configurations were obtained.
The repository has not located the complete candidate files, generator code,
configuration, or an independently checkable count certificate. The number is
therefore a search-space observation, not an accepted exhaustive result here.

### Thirty-seven-compressed annealing -- `chojecki2026status`

**Heuristic observation, not a solution.** The report describes simulated
annealing reaching an L1 PSD deviation of 236. The objective is nonzero, the
rows are not a complete LP(333), and no H(668) follows. This is weak evidence
about one heuristic landscape only; it is neither a lower bound nor an
infeasibility result.

### Common multipliers -- `ramos2026multipliers`

**Theorem/preprint scope.** If both rows are fixed by the same subgroup of
`(Z/333Z)^*`, the subgroup order is at most six. The paper reports that a
mod-3 reduction leaves 30 subgroups, excludes 21 (including all 19 of order at
least nine), and leaves nine low-order subgroups undecided.

**Artifact gap.** The preprint describes pseudo-Boolean cases, DRAT proofs,
and arithmetic certificates, but the artifact URLs and certificate bundle
were not recovered from the available record. Analytic arguments and every
machine certificate still require an independent repository-level audit.

**Strict consequence.** A common fixed multiplier of order at least nine is a
bad search direction. The result does not exclude unrestricted pairs,
different multiplier groups for the two rows, or multiplier actions composed
with translation.

## Constraint inventory before any search

Every accepted search path must preserve:

1. two 333-bit rows, each normalized to sum `+1`;
2. all 332 combined PAF equations, checked over integers;
3. SDS parameters `(333;166,166;165)` as an independent representation;
4. exact nonzero PSD sum 668 in cyclotomic arithmetic;
5. output-length 3/9/37 parity, range, row-sum, PAF, and sampled-PSD identities;
6. only proven symmetry breaking, with translations, reversals, row swaps,
   and independent row negations documented separately;
7. a complete 668-by-668 CSV and PASS/PASS from both exact verifiers before
   any solution claim.

Compressed feasibility, modular orthogonality, an FFT tolerance, a small
objective, or a solver model without a checked witness is not sufficient.

## Recommendation

### Primary: prescribed factor-9 uncompression at p=37, q=3

Use the exact output-length-37 pair `A(37,3),B(37,3)` from the proved
compression theorem as a deliberately narrow hypothesis. This has the best
current balance of mathematical structure and direct relevance to 333.
Proceed through gates:

1. obtain and reproduce the newer structured LP(27), LP(45), and LP(63)
   source data and prescribed compressions;
2. translate the published Maple checks into the exact repository API;
3. derive orbit, parity, PAF, and exact cyclotomic PSD constraints for all
   binary uncompressions of `A(37,3),B(37,3)`;
4. estimate variables, candidate counts, memory, and certificate format;
5. request approval before any run expected to exceed four cores, 30 minutes,
   or 10 GB.

This is a research hypothesis, not evidence that the conjectured
uncompression exists at 333.

### Backup: exact pseudo-Boolean/SAT search on audited compressed classes

After independently checking the prior 9-compressed counts and multiplier
certificates, encode binary uncompression with exact cardinality and cyclic
correlation constraints. Prefer proof-producing pseudo-Boolean/SAT tooling or
a complete witness that the independent Python checkers can validate. Use
only the nine surviving common-multiplier cases or separately proved
row-specific/translation symmetries; retain an unrestricted compressed-class
path so the symmetry hypothesis is not mistaken for the full problem.

This backup is less structurally elegant and likely larger, but it offers
stronger certificate discipline and a controlled way to reuse audited
compressed candidate sets.

### Deprioritized

- common fixed multipliers of order at least nine, subject to certificate audit;
- stochastic order-333 searches without an exact finishing/certificate stage;
- treating the 64-modular order-668 matrix, approximate PSDs, or compressed
  rows as a solution;
- broad GS/SDS(167), Williamson(167), TT(56), or cocyclic searches until their
  feasibility and cost are compared against the two Legendre routes above.

## Next milestone

Superseded in part on 2026-07-26. The structured q-squared pairs no longer
require artifact recovery; they are derived and proved in `pq2_derivation.md`,
and their direct-enumeration cost is settled. What remains:

1. build the exact pseudo-Boolean/SAT uncompression model for
   `A(37,3), B(37,3)`, validated at `p=3` against the 7,614 known solutions;
2. independently audit the reported 9-compressed count and the
   common-multiplier certificates;
3. produce a variable, clause, memory, and certificate estimate.

No expensive computation is authorized by this recommendation.
