# First-stage translation canonicalization and bounded solver scaling

Status: completed 2026-09-28 UTC (2026-09-27 Toronto). The canonicalization is
proved and exhaustively checked at p=3 and p=5. All six p=5 first-stage PB
searches succeed; all six p=7 first-stage searches hit their ten-second
limits. Four p=5 second-stage probes also time out. No p=37 search was run.

## Exact first-stage symmetry

Let C be a length-3p intermediate row whose compression is A. Translations
by 0, p, and 2p preserve A and every periodic autocorrelation. Choose the
first residue r with A[r] in {-1,1}; the structured prescribed rows always
have such a residue, namely r=0. The anchor triple

```
(C[r], C[r+p], C[r+2p])
```

cannot be constant, since its sum is +/-1, which is not divisible by three.
A nonconstant triple has three distinct cyclic rotations, even when two
entries coincide. Selecting its lexicographically least rotation therefore
selects exactly one of C's three translations. Independent row translations
act freely on ordered pairs, giving an exact factor-nine reduction. They
preserve all intermediate equations and preserve binary-lift existence:
translating a length-9p binary row by the same multiple of p translates its
length-3p compression correspondingly.

In the existing encoding n_i=u_i+2v_i=(3-C_i)/2, minimizing the triple of C
entries is maximizing the triple of n digits. Put

```
W = 16 n_r + 4 n_(r+p) + n_(r+2p).
```

Since each digit is in {0,1,2,3}, base-four numeric ordering equals
lexicographic ordering. Require W to be at least the two rotated codes.
After collecting coefficients these are, per row,

```
15 n_r - 12 n_(r+p) - 3 n_(r+2p) >= 0,
12 n_r +  3 n_(r+p) - 15 n_(r+2p) >= 0.
```

Expanding n into u,v gives four inequalities for the pair, no new variables,
and coefficients of magnitude at most 30, independent of p. The constructor
rejects canonicalization if either prescribed row lacks a +/-1 anchor.

The API is `IntermediatePBModel(..., canonical_translations=True)`, with
`canonicalize_pair` for translating witnesses and
`iter_symmetry_constraints` for independent audits. The existing catalog
function `canonical_intermediate_translation` still minimizes the entire
row. The new anchor convention can select a different representative of the
same orbit; catalog IDs must not be compared by raw tuple equality across
the two conventions.

| p | variables, either variant | unbroken records | canonical records |
|---:|---:|---:|---:|
| 3 | 342 | 947 | 951 |
| 5 | 930 | 2,658 | 2,662 |
| 7 | 1,806 | 5,233 | 5,237 |

The exhaustive audit maps all 792 p=3 pairs to 88 representatives and all
10,476 p=5 pairs to 1,164 representatives, each with exactly nine preimages.
Every canonical pair passes the entire OPB model. Tests also compare direct
inequality acceptance against orbit membership for every p=5 pair, and cover
every +/-1 anchor triple including repeated entries. Known canonical p=3
and p=5 witnesses have independently accepted VeriPB certificates.

## Bounded experiment

RoundingSat binary SHA-256 and VeriPB binary SHA-256, commands, model hashes,
proof hashes, witness files, timings, and sampled solver peak working sets
are frozen in `results/intermediate_scaling/metadata.json`. Runs were
sequential, on one solver core, with LP disabled and proof logging enabled.
Each search had a ten-second internal budget and a fifteen-second external
watchdog. Internal timeouts returned after about 11.05 seconds of wall time.

This solver exposes no random-seed flag. Restart multipliers 50, 100, and
200 provide a small deterministic sensitivity comparison, not independent
randomized trials or an exhaustive tuning exercise. All base entries are
free except for the stated compression and symmetry equations.

| p | restart multiplier | unbroken result / wall seconds | canonical result / wall seconds |
|---:|---:|---|---|
| 3 | 100 | SAT / 0.061 | SAT / 0.061 |
| 5 | 50 | SAT / 1.491 | SAT / 1.837 |
| 5 | 100 | SAT / 2.483 | SAT / 3.405 |
| 5 | 200 | SAT / 0.596 | SAT / 1.385 |
| 7 | 50 | TIMELIMIT / 11.043 | TIMELIMIT / 11.047 |
| 7 | 100 | TIMELIMIT / 11.047 | TIMELIMIT / 11.042 |
| 7 | 200 | TIMELIMIT / 11.067 | TIMELIMIT / 11.053 |

All eight successful search traces pass VeriPB. Actual solver assignments
are checked against every OPB record including auxiliary variables; decoded
rows independently pass the full compressed PAF and prescribed-compression
checks. Compact assignment certificates are retained in versioned results
and also pass VeriPB. Larger search traces remain in ignored scratch storage
with their hashes recorded. VeriPB reports the existing version-2 unchecked
deletion warning; only SAT conclusions backed by full exact assignments are
accepted. No timeout is an UNSAT result.

The first three distinct p=5 translation orbits discovered in the prescribed
run order were tested for binary lifts, using both projected correlations
and binary translation constraints. Their row-preimage counts were:

| selected branch | first row | second row | PB result |
|---:|---:|---:|---|
| 1 | 177,147 | 531,441 | TIMELIMIT |
| 2 | 59,049 | 1,594,323 | TIMELIMIT |
| 3 | 177,147 | 531,441 | TIMELIMIT |

These are search-selected branches, not a representative statistical sample.
Their liftability remains undetermined by these probes. No p=7 second-stage
probe was possible because the bounded first stage produced no branch.

As a controlled comparison, the earlier catalog's rank-1 p=5 branch was run
through the canonical projected PB model and the exact projected PAF join.
PB returned TIMELIMIT in 11.049 seconds. The join exhaustively scanned
531,441 and 177,147 rows, recovered exactly 27 ordered pairs, and checked a
returned witness at every PAF shift, in 7.745979 seconds. This join retains
all within-row cross terms; it is still exponential enumeration.

Total experiment wall time was 150.309042 seconds. The largest sampled
solver working set was 18,231,296 bytes; this is not a measurement of the
Python join's peak memory or the whole pipeline. Search proof files total
227,640,019 bytes. The frozen result package is about 2.31 MB. No broad
hardware-independent speed claim follows from these single-machine timings.

## Decision and next bounded milestone

**Prioritize a specialized ternary formulation retaining cross terms, and
keep PB as the exact reference and certificate backend. Do not advance to
p=37 on this evidence.** Canonicalization is correct and cheap to encode,
but it slowed all three measured p=5 first-stage searches and did not bridge
the p=7 gap. The known SAT p=5 lift still defeats the generic projected PB
search within this budget, while its exact signature join completes.

This is evidence against scaling this particular generic PB configuration
directly. It is not evidence that every PB solver or encoding fails, nor a
measured win for an as-yet unimplemented decomposition.

A concrete cross-term-aware next model follows from the minority-layer
description. For a fixed intermediate row C of length N, write

```
x_(i+kN) = b_i + d_i [k = a_i],    k in Z/3Z.
```

For |C_i|=1, take b_i=C_i, d_i=-2b_i and a ternary phase a_i. For |C_i|=3,
take b_i=C_i/3 and d_i=0 (its phase is irrelevant). For shift s=r+ell*N,
0<=r<N, put j=(i+r) mod N and h=ell+floor((i+r)/N). Summing over the three
layers gives the exact contribution

```
3 b_i b_j + d_i b_j + b_i d_j
    + d_i d_j [a_j - a_i = h mod 3].
```

Thus each PAF is a constant plus weighted ternary phase-difference tests.
The carry term in h and every interaction between phase groups must remain.
Independent row translations permit fixing one active phase per row. A
naive additive split into two halves would drop the final interaction term
and is invalid.

The next implementation gate should verify this tensor/phase formulation
against direct PAF evaluation for all p=3 preimages, reproduce the p=5 rank-1
count of 27, and compare it with the retained PB models under equal short
budgets. Only measured progress at both p=5 and p=7 should motivate larger
resource proposals. The present work implements the symmetry and bounded
benchmark. Follow-up: `ternary_phase.md` now records the exact phase model,
incremental join, certified p=7 intermediate branch, and bounded lift
comparison. Finite-domain phase propagation is the next research task.

Reproduction:

```powershell
python -m scripts.benchmark_intermediate_scaling `
  --solver tmp/tools/roundingsat/roundingsat.exe `
  --verifier tmp/tools/veripb-3.0.2/bin/veripb.exe `
  --search-seconds 10
```
