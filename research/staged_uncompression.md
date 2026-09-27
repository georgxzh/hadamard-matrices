# Exact successive-q uncompression branches

Status: conditional second-stage model implemented and benchmarked 2026-09-27
at p=3 and p=5. The p=3 branches solve with verified proofs; bounded p=5
searches time out. No LP(333) model or order-668 result is claimed.

## Exact decomposition

For `q=3`, let `(x,y)` be binary rows of length `9p`. First compress them by
factor three to integer rows `(C,D)` of length `3p`, then compress `(C,D)` by
factor three to the prescribed pair `(A(p,3),B(p,3))` of length `p`:

```text
{-1,+1}^{9p}  --3-compress-->  {-3,-1,1,3}^{3p}
                  --3-compress-->  prescribed integer rows of length p.
```

A valid intermediate pair must have row sums one, values in
`{-3,-1,1,3}`, combined PAF `18p-4` at shift zero, and combined PAF `-6`
at every nonzero shift. These are the exact factor-three compressed Legendre
conditions, not floating-point filters.

`src.staged_uncompression.FactorThreeBranch` checks all of these conditions
and both second compressions before constructing an OPB model. For a fixed
valid `(C,D)`, the resulting factor-three OPB is sound and complete for binary
Legendre pairs whose first compression is exactly `(C,D)`.

This scope is important: the implementation models and searches one supplied
intermediate branch. It does not yet enumerate or solve for all possible
intermediate pairs above `(A(p,3),B(p,3))`.

## Generalized translation canonicalization

The earlier factor-nine model used residue zero because its target was one.
An intermediate row can instead have residue-zero target `+3` or `-3`, making
that three-bit word constant and useless for orbit selection. The model now
accepts one canonical residue per row.

For factor three, any intermediate target `+1` or `-1` gives a three-bit word
with respectively one or two negative entries, hence full cyclic period
three. Selecting the least rotation in such a residue therefore gives a free
factor-three action per row and an exact factor-nine reduction on ordered
pairs. The p=5 branch uses residues `(1,0)`; the p=3 branch uses `(0,0)`.

## Branch sizes

| case | first-row preimages | second-row preimages | unbroken records | canonical records |
|---|---:|---:|---:|---:|
| p=3, length 27 | 6,561 | 729 | 2,839 | 2,843 |
| p=5, length 45 | 59,049 | 1,594,323 | 7,972 | 7,976 |

The original one-stage prescribed rows have 889,056 preimages per row at p=3
and 6,273,179,136 per row at p=5. Fixing a valid intermediate branch is thus a
substantial exact domain reduction even though the final-PAF XOR layer keeps
the same number of auxiliary variables.

## Proof-producing benchmark

RoundingSat commit `d4edbf7` ran with LP disabled, one core, proof logging,
and a ten-second internal limit. VeriPB 3.0.2 checked every complete proof.

| case | result | solver wall | peak working set | proof |
|---|---|---:|---:|---:|
| p=3 unbroken | SAT | 0.575 s | 7.66 MB | 1,638,002 bytes |
| p=3 canonical | SAT | 0.818 s | 7.95 MB | 2,527,594 bytes |
| p=5 unbroken | TIMELIMIT | 11.049 s | 13.65 MB | incomplete, 20,712,367 bytes |
| p=5 canonical | TIMELIMIT | 11.037 s | 13.27 MB | incomplete, 22,182,057 bytes |

Both p=3 solver assignments independently pass the complete OPB model, exact
PAF, SDS, cyclotomic PSD, and prescribed intermediate compression checks. The
solver proofs report `VERIFIED SATISFIABLE`. The incomplete p=5 proofs are
ignored scratch artifacts recorded only by byte count and SHA-256.

VeriPB warns that the RoundingSat proof-version-2 logs switch to unchecked
deletion. This benchmark makes only a SAT claim: each proof ends with a
complete assignment, VeriPB accepts that conclusion, and the repository
separately parses the solver assignment and checks all mathematical
identities. These logs are not evidence for an UNSAT-proof policy.

This is a genuine search improvement over the one-stage LP(27) benchmark,
which did not recover a known witness in ten seconds. It is not yet sufficient
at p=5, and a single fixed intermediate branch says nothing about other
branches or LP(333).

## Next milestone

Implement an exact first-stage generator/model for all length-`3p`
intermediate pairs above the prescribed length-`p` rows. First validate its
complete output at p=3, then require it to recover the published p=5 branch.
Only after both stages have independently checkable coverage and the p=5
second-stage search improves should a p=37 resource proposal be considered.

Reproduction command:

```powershell
python -m scripts.benchmark_staged_uncompression `
  --solver tmp\tools\roundingsat\roundingsat.exe `
  --verifier tmp\tools\veripb-3.0.2\bin\veripb.exe `
  --search-seconds 10
```
