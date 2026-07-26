# Direction selection

Status: revised 2026-07-26 after the pq^2 retrieval gap was closed by
independent derivation. No expensive run authorized.

Order 428 and the exact Legendre core are reproduced. The structured pq^2
compressed pair is now derived, proved, and reproduced at `p=3`.

## What changed

The previous primary direction was gated on retrieving publisher data that was
inaccessible. That gate is gone: `A(p,q)` and `B(p,q)` are determined by the
quadratic-character formula, and their compressed-Legendre property is proved
via the Jacobsthal sum in `pq2_derivation.md`. The factor-9 uncompression is
reproduced end to end at `p=3, q=3`, yielding an LP(27) and a dual-verified
H(56) from sequences derived rather than transcribed.

The same work also settles the route's feasibility, negatively. One row of
`A(37,3)` admits `126 * 84^36 ~ 2.4e71` binary uncompressions. Direct
enumeration is impossible by roughly fifty orders of magnitude, and no
engineering effort changes that.

**Prescribed factor-9 uncompression at `p=37, q=3` is therefore retained as
the mathematical target and abandoned as a search method.**

## Primary: constraint-propagation uncompression

Encode "binary uncompression of `A(37,3), B(37,3)`" as an exact
pseudo-Boolean/SAT problem — 666 variables, 37 exact cardinality constraints
per row, and the 332 combined PAF equations — and rely on propagation and
learned clauses rather than enumeration. The compressed rows are now known
exactly, so the model is fully specified.

Gates before any run:

1. build the model and validate it end to end at `p=3` against the 7,614
   known solutions, then at `p=5` against ground truth if reachable;
2. derive and add every proved symmetry break (translation, reversal, row
   swap, independent negation), documented separately;
3. estimate variables, clauses, memory, and certificate format;
4. request approval with that estimate before running.

The honest prior is that this fails too. Passing every compressed necessary
condition does not imply a binary preimage exists, and the source states the
universal uncompression claim as a conjecture. A negative result would still
be publishable if it carries a checkable proof.

## Backup: audited compressed classes

Independently check the reported 9-compressed counts and the common-multiplier
certificates, then run the same exact encoding over unrestricted compressed
classes rather than the single prescribed one. Slower to set up, but it does
not stake everything on one conjectural compressed pair.

## Deprioritized

- direct enumeration of any uncompression at `p >= 7`;
- common fixed multipliers of order at least nine, subject to certificate audit;
- stochastic order-333 searches without an exact finishing stage;
- treating the 64-modular order-668 matrix, approximate PSDs, or compressed
  rows as a solution.

Full evidence labels, parameter constraints, gaps, and gates are recorded in
`length333_audit.md` and `pq2_derivation.md`.
