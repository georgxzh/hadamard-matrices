# Direction selection

Status: revised 2026-08-25 after a free translation action was proved,
encoded, and exhaustively validated at p=3. No expensive run authorized.

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

The exact pseudo-Boolean reference model is now implemented. Its 666 base
variables expand to 111,222 variables after exact XOR linearization, with
442,464 OPB records. The deterministic 14.955-MiB model has a frozen SHA-256
and a VeriPB-oriented certificate plan. It contains no unproved symmetry
break. See `pb_uncompression_model.md`.

Gates before any run:

1. **Complete:** validate the exact model at `p=3`; all 7,614 canonical
   matches passed, representing 77,274 ordered pairs with multiplicity;
2. **Complete for translations:** independent translations by 37 give a free
   order-81 action on ordered pairs; the canonical OPB adds 16 inequalities
   and was exhaustively validated. Reversal and multiplier actions are proved
   but remain unencoded pending a combined canonicalization proof;
3. benchmark proof-logging PB backends on LP(27), measuring verifier time and
   memory; do not assume a solver's UNSAT output is a certificate;
4. decide whether a bounded p=5 validation can fit the approval gate;
5. request approval with measured solver/proof estimates before any LP(333)
   run.

The honest prior is that this fails too. Passing every compressed necessary
condition does not imply a binary preimage exists, and the source states the
universal uncompression claim as a conjecture. A negative result would still
be publishable if it carries a checkable proof.

## Backup: audited compressed classes

The common-multiplier artifact audit locally reproduced 15 of 25 exclusions;
the current classification leaves only IDs `0,1,3,4,5`, all of order at most
three. Finish the ten-case full-proof audit when its resources are bounded,
and independently check the reported 9-compressed counts. Then reuse the
audited exact encoding over unrestricted compressed classes rather than the
single prescribed one. Prefer proof-producing tooling or a complete witness
checked by the independent Python pipeline. Retain an unrestricted path so
any common-multiplier hypothesis is not mistaken for the full problem.

## Deprioritized

- direct enumeration of any uncompression at `p >= 7`;
- common fixed multipliers of order at least four under the current artifact
  classification (ten machine exclusions still await a full local proof run);
- stochastic order-333 searches without an exact finishing stage;
- treating the 64-modular order-668 matrix, approximate PSDs, or compressed
  rows as a solution.

Full evidence labels, parameter constraints, gaps, and gates are recorded in
`length333_audit.md` and `pq2_derivation.md`.
