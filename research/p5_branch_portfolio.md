# Complete p=5 branch profile and bounded second-stage portfolio

Status: completed 2026-09-27. This is a deterministic small-parameter
experiment for the successive-q route in `kotsireas2025compression`. It is
not an LP(333) experiment and has no implication that order 668 is solved.

## Exact branch invariant and ranking

Every compatible p=5 intermediate pair `(C,D)` has 23 entries of magnitude
one across its two length-15 rows. A factor-three binary preimage has three
choices above an entry `+/-1` and one choice above `+/-3`. Therefore, if the
two rows contain `k` and `23-k` magnitude-one entries, their individual
preimage counts are `3^k` and `3^(23-k)`. The Cartesian product is always
`3^23`; only the number of row candidates scanned and the signature-table
memory change with the split.

The complete 10,476-pair first-stage output has this exact distribution:

| split | ordered branches | scans per exhaustive row join |
|---:|---:|---:|
| 9+14 | 162 | 4,802,652 |
| 10+13 | 1,620 | 1,653,372 |
| 11+12 | 3,456 | 708,588 |
| 12+11 | 3,456 | 708,588 |
| 13+10 | 1,620 | 1,653,372 |
| 14+9 | 162 | 4,802,652 |

Independent translations of each intermediate row by `0`, `p`, or `2p`
preserve its second compression and PAF. Residue zero compresses to one, so
its three entries cannot be constant; the action is free in both rows. The
10,476 ordered branches consequently split into exactly 1,164 orbits of size
nine. `results/p5_branch_portfolio/canonical_branches.json` freezes every
lexicographically canonical representative.

Branches are ranked by total row scans, then maximum and minimum row count,
then the two rows lexicographically. This is an exact cost measure for the
repository's signature-join implementation, not a claim about general SAT
hardness. The published intermediate branch has split 10+13 and rank 771.

## Three-branch exhaustive portfolio

The smaller preimage row is stored as the PAF-signature table to control
memory. Each ranked branch requires 177,147 plus 531,441 row candidates.

| rank | complete result | wall time | distinct stored signatures | ordered LP(45) pairs |
|---:|---|---:|---:|---:|
| 1 | SAT | 7.771051 s | 59,001 | 27 |
| 2 | SAT | 8.648980 s | 59,001 | 27 |
| 3 | no pair in branch | 7.816479 s | 58,935 | 0 |

The first two results are exhaustive counts, not early exits. The third is a
branch-level negative computational result: every binary preimage on both
sides was included in the exact integer PAF join. It is not a global LP(45)
nonexistence statement, and it currently has no standalone machine-checkable
UNSAT proof. A ten-second RoundingSat proof-producing probe of rank 3 returned
`TIMELIMIT`; its incomplete scratch proof is not retained as evidence.

The first recovered pair independently passes every PAF shift, the SDS check,
all cyclotomic PSD constraints, both compression stages, and every fixed-branch
OPB record. VeriPB 3.0.2 accepts its complete SAT certificate. The resulting
H(92) has SHA-256
`a2081037642e242729aebec4a94529f400dc49b326f69f6b74c0521b9ae33389` and
passes both independent exact matrix verifiers.

## Interpretation

The ordering succeeds at its limited goal: a fully exhaustive p=5 branch
search finds witnesses not copied from the published rows, whereas the earlier
generic proof-producing search timed out on the less balanced published
branch. No inequivalence or novelty claim is made for these witnesses. The
result does not establish that scan balance predicts solver hardness beyond
this enumerator, nor does three branches estimate the satisfiable fraction of
all 1,164 orbits.

For p=37, direct intermediate generation and per-branch binary enumeration
remain exponential. The next useful milestone is therefore mathematical:
derive first-stage constraints that avoid materializing all residue triples,
and investigate stronger exact second-stage projections or meet-in-the-middle
keys. Any LP(333) run still requires a separate resource proposal and user
approval.

Reproduction command:

```powershell
python -m scripts.benchmark_p5_branch_portfolio `
  --verifier tmp\tools\veripb-3.0.2\bin\veripb.exe `
  --portfolio-size 3
```
