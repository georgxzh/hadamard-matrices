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
`p=3, q=3`, recovering 7,614 canonical matches (77,274 ordered pairs after
including second-signature multiplicity) and a dual-verified H(56).

**Feasibility — resolved negatively.** One row of `A(37,3)` admits
`126 * 84^36 ~ 2.4e71` binary uncompressions. Direct enumeration is impossible
by about fifty orders of magnitude. The route survives only as a
constraint-satisfaction problem, not as a search over candidates. See
`pq2_derivation.md` section 5.

**Exact constraint model — complete 2026-08-20.** The unbroken OPB encoding
has 111,222 variables and 442,464 constraint records. It was exhaustively
validated against all 7,614 canonical p=3 matches. The generated LP(333) input
is 15,681,010 bytes with SHA-256
`60d5eb303c36fb1dee95e40ffb82b858a64c737c704be18e59d0764726f23405`.
No solver was run. Soundness, completeness, counts, and certificate policy are
proved and recorded in `pb_uncompression_model.md`.

**Translation symmetry — complete 2026-08-25.** Independent translations of
the two rows by multiples of 37 form a free order-81 action because each
residue-zero word has four negatives and full period nine. Sixteen exact OPB
inequalities select the least cyclic residue-zero word in each row. The
canonical model has 442,480 records, unchanged variable count, and was
validated on every p=3 canonical match. Reversal and multiplier actions are
proved but intentionally remain unencoded pending a combined canonicalization
proof.

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

**Paper scope.** ArXiv v1 proves that if both rows are fixed by the same
subgroup of `(Z/333Z)^*`, its order is at most six. It classifies 30 subgroups,
excludes 21 (all 19 of order at least nine), and leaves nine low-order groups.

**Post-v1 artifact state — partially reproduced.** The current
`ramos2026artifacts` repository reports 25/30 impossible and open IDs
`0,1,3,4,5`, all of order at most three. At commit `691398b`, this project
locally reran exact checks excluding these 15 IDs:
`2,6,7,8,9,10,12,16,17,18,24,25,26,27,29`. The v1.0.0 proof archive's
198,965,505-byte download matches its
published SHA-256, but it was not extracted or executed. The ten remaining
machine exclusions are therefore artifact claims inspected but not locally
reproduced. See `multiplier_artifact_audit.md`.

**Strict consequence.** Common fixed multiplier order at least four is a bad
search hypothesis according to the current artifact classification; the
paper-alone bound remains order at most six. Neither result excludes
unrestricted pairs, different multiplier groups for the two rows, or affine
multiplier-with-translation actions.

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
The compressed rows, exact identities, direct-enumeration bound, unbroken OPB
model, small-case validation, and certificate policy are complete. Proceed
through the remaining gates:

1. **Complete for translations:** the free order-81 action is encoded and
   exhaustively validated; reversal and multiplier actions are documented but
   not yet combined into a canonical encoding;
2. benchmark proof-logging PB backends on LP(27), including proof-check time
   and memory;
3. decide whether a bounded p=5 validation can stay within the approval gate;
4. request approval with measured resources before any LP(333) solver run.

This is a research hypothesis, not evidence that the conjectured
uncompression exists at 333.

### Backup: exact pseudo-Boolean/SAT search on audited compressed classes

Finish the ten-case common-multiplier proof audit when its resources are
bounded, and independently check the prior 9-compressed count. Reuse the exact
cardinality/cyclic-correlation encoding over unrestricted compressed classes.
If using common multipliers, the current artifact leaves only IDs
`0,1,3,4,5`; retain an unrestricted path so that fixed-symmetry assumptions
are not mistaken for the full problem. Prefer proof-producing tooling or a
complete witness that the independent Python checkers can validate.

This backup is less structurally elegant and likely larger, but it offers
stronger certificate discipline and a controlled way to reuse audited
compressed candidate sets.

### Deprioritized

- common fixed multipliers of order at least four under the current artifact
  classification, with the ten full machine-proof cases still marked pending;
- stochastic order-333 searches without an exact finishing/certificate stage;
- treating the 64-modular order-668 matrix, approximate PSDs, or compressed
  rows as a solution;
- broad GS/SDS(167), Williamson(167), TT(56), or cocyclic searches until their
  feasibility and cost are compared against the two Legendre routes above.

## Next milestone

The structured rows, direct-enumeration cost, exact OPB model, small-case
validation, input-size measurement, and certificate policy are complete. What
remains, in order:

1. bound or obtain approval for the full common-multiplier DRAT/MITM audit of
   the ten locally unreproduced exclusions;
2. locate and audit the inputs behind the reported 12,017,243 9-compressed
   configurations;
3. benchmark a proof-logging backend on both unbroken and translation-
   canonical LP(27) models before proposing any larger solver run.

No expensive computation is authorized by this recommendation.
