# Direction selection

Status: revised 2026-09-29 UTC after completing the prescribed p=5 census.
All 1,164 intermediate translation orbits are resolved: 704 liftable and 460
empty, with every multiplicity preserved. See `p5_classification.md` and
`../paper/manuscript.tex`. The independent enumeration and symmetry-transfer
audit passed. This restricted census is not a new LP(45) existence result or
a first length-45 classification; Fletcher--Gysin--Seberry already reported
an exhaustive classification in 2001. Novelty of this artifact remains open.

Earlier direction assessment after implementing the exact ternary phase
formulation and comparing bounded p=5/p=7 binary lifting. Prioritize
finite-domain propagation on phase differences and weighted PAF sums, with
the binary and phase PB models as exact references. No p=37 solver run has
been started.

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

## Primary: cross-term-aware uncompression with an exact PB reference

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
3. **Pipeline complete, search benchmark negative:** RoundingSat and VeriPB
   interoperate with exact recorded proof sizes, time, and memory, but neither
   unfixed LP(27) model was solved within the tested bounds;
4. **Complete for fixed-witness validation:** the published structured LP(45)
   passes both models and VeriPB, while the four-facet XOR gadgets are exact
   and individually irredundant; the source's successive q-uncompression is
   now the preferred encoding experiment;
5. request approval with measured solver/proof estimates before any LP(333)
   run.

The staged route now has a non-enumerative p=37 first-stage OPB with 49,506
variables and 147,538 records. For any valid intermediate branch, an exact
projection theorem reduces the final PAF key to shifts `1..N-1`; at length 333
this gives 73,926 variables and 293,372 records instead of 111,222 and
442,612. Exhaustive p=3 and p=5 checks show that the projected and full keys
return identical solution counts, and a p=5 witness certificate passes
VeriPB. However, the p=5 projected open solver still times out in ten seconds,
and a p=37 branch retains `3^167` paired preimages. See
`projected_uncompression.md`.

The next gate has now been completed: four anchor-triple inequalities give
an exact factor-nine first-stage translation reduction, exhaustively audited
at p=3 and p=5. All six p=5 first-stage PB searches succeeded, but all six p=7
searches timed out at ten seconds; canonicalization slowed every paired p=5
comparison. Four projected canonical p=5 binary-lift probes also timed out.
On the known SAT rank-1 branch, the complete exact PAF join recovered 27
pairs in 7.75 seconds while PB timed out. See `intermediate_scaling.md` for
the proofs, complete timings, certificates, and limitations.

The subsequent implementation exposed the exact weighted ternary
phase-difference interactions, preserving cross terms and layer carries.
It passes 196,830 direct PAF checks over the fixed p=3 branch's row preimages
and reproduces the p=5 rank-1 count of 27. The phase PB model has 432
variables and 1,249 records at that p=5 branch, compared with 1,350 and
5,088 in the binary projected model. A seeded heuristic acquired an exact,
VeriPB-certified p=7 intermediate branch in 3.87 seconds.

All twelve ten-second p=5/p=7 binary-lift probes, comparing both encodings
at three restart settings, still time out. The incremental phase join beats
an independent packed join on the same canonical p=5 domain (0.96 versus
1.81 seconds), but the p=7 join reaches its 250,000-signature cap before
streaming partner rows. See `ternary_phase.md` for exact counts, proof,
certificates, measurements, and the lack of a p=7 liftability conclusion.

Next implement finite-domain propagation over the ternary phase differences,
cycle consistency, and weighted PAF sums. Check the known p=3/p=5 counts and
an exhaustively empty p=5 branch before using the saved p=7 branch. Preserve
all cross terms: the interaction graph is complete within each row, so a
small separator cannot be assumed. Keep both PB models as correctness and
certificate references. These results do not justify a p=37 run.

The honest prior is that this fails too. Passing every compressed necessary
condition does not imply a binary preimage exists, and the source states the
universal uncompression claim as a conjecture. A negative result would still
be publishable if it carries a checkable proof.

## Follow-up result: phase propagation (2026-09-29 UTC)

The proposed difference/cycle/PAF solver and a row-conditioned variant are
implemented and audited; see `phase_propagation.md`. The latter reproduces
every solution on all 1,164 p=5 branches using 79 direct representatives and
proved bijections, but takes 3.56 times the join's summed recorded case time.
Controlled ablations reduce nodes without improving elapsed time. Standalone
difference search times out on p=5 controls, and the bounded p=7 experiments
remain unresolved. Thus this implementation does not displace the join or
justify scaling. Derive and validate a stronger safe single-row filter before
another scaling experiment. Keep the PB baseline for certificates and avoid
p=37 search. The literature convention conversion yields 63 classes within
our subset; matching the historical representative list remains outstanding.

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
