# Complete prescribed p=5 lift census

Completed and audited 2026-09-29 UTC. This classifies binary lifts of every
one of the 1,164 translation representatives in
`results/p5_branch_portfolio/canonical_branches.json`. It does not classify
all LP(45)s or Hadamard matrices, and makes no progress claim for order 668.

## Counts and conventions

The prescribed pair is `(1,3,-3,-3,3)`, `(1,-3,3,3,-3)`. Intermediate rows
have length 15 and entries ±1, ±3; binary rows have length 45 and row sum 1.
The catalogue uses the lexicographically least entire intermediate row under
translations by 5. Binary enumeration fixes the first magnitude-one residue's
minority layer to zero, independently in each row. These two conventions are
distinct from the first-stage PB anchor-triple convention and the binary PB
negative-bit convention.

| Ordered binary lifts of the fixed intermediate pair | Phase-gauged lifts | Catalogue branches |
|---:|---:|---:|
| 0 | 0 | 460 |
| 27 | 3 | 464 |
| 54 | 6 | 192 |
| 81 | 9 | 48 |

All 1,164 branches are resolved: 704 SAT and 460 verified empty. No timeout
was assigned count zero. There are 2,976 phase-gauged lifts; multiplying each
by 9 gives 26,784 ordered pairs over catalogue representatives. Restoring
the 9 intermediate translations gives **241,056** distinct ordered indexed
binary pairs with the prescribed length-five compression. These are not
counts modulo arbitrary reversal, decimation, exchange, or matrix equivalence.

## Pilot and resources

The stratified pilot covered 21 branches and all six active-count strata,
including ranks 1, 2, 3 and the published branch 771. Both exhaustive
enumerators completed each case. It took 205.248 seconds on four workers;
the conservative direct 1,164-case estimate was 6,513.693 seconds (108.56
minutes). That run would exceed the repository's 30-minute limit and was
not started.

Exact symmetries instead partition the catalogue into 79 classes: 67 of
size 16, 11 of size 8, and one of size 4. The reduced three-worker proposal
estimated 763.185 seconds, 1.426 GB of worker memory, and 8.73 MB of output,
including a 50% time/memory margin. The full runner has a 27-minute wall
budget and 120-second per-branch deadlines. No approval threshold was crossed.

The reduced run took 394.574 seconds, reusing seven verified pilot
representatives. Maximum recorded worker peak: 317,227,008 bytes; three
times this is 951,681,024 bytes, a conservative sum of worker peaks, not a
simultaneous whole-system measurement. Result records, audit and manifest
occupy approximately 1.14 MB. Fresh reproduction needs both pilot and full
run (about ten minutes combined at these observed rates).

## Why the 79-case reduction preserves exact counts

Use a common unit `u` modulo 15, independent signs `epsilon` for reversal,
and exchange the rows precisely when `u mod 5` is a nonsquare (2 or 3).
Because `chi_5(-1)=1`, this preserves the ordered prescribed pair. Independent
reversal leaves real PAF unchanged, and common decimation permutes shifts.
Normalize each resulting intermediate row by a recorded offset `t` in
`{0,5,10}`. On binary rows the explicit permutation is
`x'[i] = x[epsilon*u*(i+t) mod 45]`, after the same exchange.
All selected units modulo 15 are units modulo 45. This invertible permutation
commutes with compression. Restoring phase-zero gauges therefore induces
a bijection of lift sets modulo the free binary translations by 15.

Every target retains its own operation, representative evidence hash, count,
and full canonical solution list. The class sizes are not used as a uniform
factor. The audit separately implements the inverse permutation on tuples.
Tests also invert arbitrary non-Legendre preimages for every target.

## Independent checks and trust boundary

Each representative is exhausted twice:

1. Ternary reflected Gray order, incremental PAF, 14 projected shifts.
2. Independent Cartesian products of binary residue masks, direct popcount
   PAF, all 22 nonredundant shifts; no phase formula or projected theorem is
   used to accept a match.

The programs compare row coverage, projected-signature histograms with
multiplicity, every matching binary mask pair, and exact counts. All 2,976
transferred solutions pass full direct integer PAF, SDS and compression
checks. The separate audit regenerates all 10,476 intermediates, reproduces
the ranked catalogue, checks all 79 representative records, compares every
one of the 21 pilot branches, inverts all transfers and expands translations
to verify uniqueness of all 241,056 pairs. It took 13.843 seconds.

Known counts are reproduced: ranks 1 and 2 each have 27 ordered lifts;
rank 3 has none; published rank 771 has 54 and includes the published
structured LP(45) after normalization.

This is exact computational exhaustion checked by two implementations, plus
proved symmetry bijections. Empty branches have no standalone VeriPB UNSAT
certificate. The audit reads exhaustion records rather than running a third
enumerator. Both enumerators share the catalogue and some final check
routines; independent external replication remains desirable. File hashes
identify evidence and do not themselves establish exhaustion.

## Reproduction and artifacts

```powershell
.venv/Scripts/python.exe -m scripts.classify_p5_lifts --pilot --workers 4
.venv/Scripts/python.exe -m scripts.classify_p5_lifts --full --workers 3
.venv/Scripts/python.exe -m scripts.audit_p5_classification
```

`results/p5_classification/branch_counts.csv` has a count for every branch.
`classification.json` retains all solutions and transfer operations;
`representatives/` retains both exhaustive enumerations' evidence;
`pilot/`, `pilot.json`, `resource_plan.json`, `audit.json`, and `manifest.json`
record the gate, checks and hashes. Classification SHA-256:
`8cf7c10075511c30a765c4bb36aa37924a6af8e835cd86f2ef82a98ff7bfe1ea`.

## Primary-literature comparison

`fletcher2001`, Section 5.4 and Table 3, already reports exhaustive searches
through length 47, including **3,058 inequivalent LP(45)s** under row
exchange, independent cyclic shifts/reversals and common decimation. Our
restricted ordered count is not directly comparable; a crosswalk to their
underlying representatives has not been performed. No first length-45
classification is claimed.

`kotsireas2025compression`, Theorem 3.2 and Section 4, already gives this
character prescription and successive q-lifting. `kotsireas2023mod5`, Section
2 and Table 2, already lists the magnitude pattern `(1,3,3,3,3)` at length
45, alongside other families. Compression and symmetry principles are
established (`djokovic2015compression`, `turner2022decimation`). The
restricted branch-by-branch artifact may be useful, but its novelty is
unresolved, especially against the later `kotsireas2027pq2` full text.
