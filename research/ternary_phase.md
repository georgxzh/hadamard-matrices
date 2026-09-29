# Exact ternary phases and bounded p=5/p=7 lifting

Follow-up completed 2026-09-29 UTC: the full prescribed p=5 census is in
`p5_classification.md`, and controlled benchmarks are in `phase_controls.md`.
Those controls align the PB gauges and hold Gray traversal fixed when
comparing PAF updates. Their three-repeat results supersede any interpretation
of the single-trial timings below as isolated update speedups. All earlier
raw outcomes remain preserved. The paper draft is `../paper/manuscript.tex`.

Status: implemented and tested on 2026-09-29 UTC (2026-09-28 Toronto).
The exact phase representation, incremental cross-term join, and compact PB
model pass the small-case gates. A newly acquired p=7 intermediate branch
passes exact checks and VeriPB. Neither PB encoding finds a binary lift at
p=5 or p=7 within the tested limits. No p=37 search was run.

## Exact representation and proof

For a fixed factor-three intermediate row C of length N, each |C_i|=1
residue has one minority sign among three layers. Let a_i in Z/3Z be that
layer, b_i=sign(C_i), and d_i=-2b_i. For |C_i|=3 set d_i=0 and use no phase.
Then

```
x_(i+kN) = b_i + d_i [k=a_i].
```

This is a bijection between ternary assignments and binary preimages of C.
For s=r+ell*N with 0<=r<N, let j=(i+r) mod N and
h=ell+floor((i+r)/N), reduced modulo three. Summing a product over layers
gives

```
sum_k x_(i+kN) x_(j+(k+h)N)
  = 3 b_i b_j + d_i b_j + b_i d_j
    + d_i d_j [a_j-a_i=h mod 3].
```

The implementation includes the carry, all active-active terms, diagonal
terms, zero shifts, and shifts N and 2N. Orienting an edge from u to v with
u<v negates h if its endpoints are exchanged. This is exact integer
arithmetic; there is no dropped interaction between two parts of a row.

Fixing the first active phase to zero removes independent translations by N
on each row. A nonconstant binary triple has three distinct rotations, so
this action is free and the ordered-pair count is nine times the canonical
count. This phase-zero convention can differ from the existing binary
least-bit-word representative. Both select the same solution orbits; raw
representative tuples and solver timings need not coincide.

### Compact PB model

`TernaryPhasePBModel` uses three one-hot bits per active phase and three
one-hot bits for each unordered active pair's phase difference. For each
endpoint assignment a,b, the channel constraint is

```
-X_(u,a) - X_(v,b) + D_(u,v,(b-a) mod 3) >= -1.
```

Exactly-one constraints on X and D make the nine implications per edge
necessary and sufficient to encode its actual phase difference. The same
difference variables are shared across every PAF equation. All interaction
coefficients are +/-4; subtracting the constant term and dividing by four
leaves coefficients +/-1. The required projected shifts remain 1..N-1;
their sufficiency follows from the previously proved compression identity
in `projected_uncompression.md`. Hence the PB model is sound and complete
for the fixed branch, modulo the proved row translations.

| branch | binary projected variables / records | phase variables / records |
|---|---:|---:|
| p=3 reference | 486 / 1,758 | 171 / 454 |
| p=5 catalog rank 1 | 1,350 / 5,088 | 432 / 1,249 |
| acquired p=7 | 2,646 / 10,146 | 819 / 2,464 |

Both columns include translation constraints. These dimensions describe
fixed intermediate branches, not a first-stage search.

### Incremental exact join

`PhaseRow.iter_projected_signatures` traverses all anchor-zero assignments
in reflected ternary Gray order. Each transition changes one phase and
updates every incident edge in the PAF vector. For active residues i<j,
put r=j-i and delta=a_j-a_i modulo three. The edge contributes d_i*d_j at
projected shift r when delta=0, at shift N-r when delta=2, and at neither
when delta=1. This accounts for both orientations and the wrapping carry.

`search_phase_uncompressions` stores the smaller row's signatures, including
multiplicities, and streams the other row against complementary signatures.
It retains all cross terms and checks every returned witness at every final
PAF shift. It remains exponential in the number of active phases; it does
not implement a square-root split or assume that cross-half terms vanish.

Explicit time, candidate, and stored-signature limits produce
`complete=False` with a stop reason. Counts in partial searches are lower
bounds. A zero partial count is never evidence of nonexistence.

## Validation

For the fixed p=3 reference branch, all 6,561 and 729 binary row preimages
were encoded and decoded bijectively. The phase formula agrees with direct
integer autocorrelation at every one of 27 shifts: 196,830 exact checks.
Independent tests cover all 512 Boolean assignments to a channel gadget;
exactly the nine correct endpoint/difference assignments survive.

The full canonical p=3 phase join enumerates 243 stored and 2,187 streamed
rows, finding 15 canonical pairs, or 135 ordered pairs. The full p=5 rank-1
join enumerates 59,049 stored and 177,147 streamed rows, finding three
canonical pairs, or exactly 27 ordered pairs. Both agree with the older
full-row enumeration. Phase-model witness certificates for both branches
pass VeriPB 3.0.2.

Tests compare every p=3 Gray-update signature with both direct PAF evaluation
and a separately implemented bit-packed canonical enumerator. Tests also
cover invalid inputs, corrupted difference bits, counts and OPB headers,
and each partial-search stopping condition.

## Acquiring a p=7 intermediate branch

Three further canonical first-stage PB probes, each limited to twenty
seconds and using restart multipliers 50, 100, and 200, all timed out.
Their transcripts and proof hashes are in `p7_acquisition.json`.

A bounded seeded annealing search over residue triples then found a branch
after 89,695 iterations, in 3.872 seconds (rounded), with seed 20260928.
Each move preserves all prescribed residue sums. Its energy is the sum of
squared combined-PAF residuals divided by sixteen, including shift zero;
incremental updates include the quadratic delta products. Acceptance of a
branch requires zero energy followed by direct exact checks and the complete
first-stage OPB. Its SAT certificate is accepted by VeriPB.

The intermediate rows, stored exactly in `metadata.json`, have 15 and 17
active phases. This is a necessary-condition branch acquired heuristically,
not a binary LP(63), and its binary liftability remains unknown. The result
shows that this bounded heuristic can obtain an exact p=7 branch where the
tested generic PB configuration did not. One successful seed is not a
general runtime or completeness guarantee.

## Bounded comparison

The solver comparison used one process at a time, LP disabled, proof logging,
ten-second internal limits and fifteen-second external watchdogs. Restart
multipliers 50/100/200 are deterministic sensitivity probes, not random
trials. Both encodings search a fixed branch with independent translation
gauges; their representative conventions differ as noted above.

| branch | encoding | restart 50 | restart 100 | restart 200 |
|---|---|---|---|---|
| p=3 | binary projected | not run | SAT, 3.135 s | not run |
| p=3 | ternary phase | not run | SAT, 0.330 s | not run |
| p=5 rank 1 | binary projected | timeout | timeout | timeout |
| p=5 rank 1 | ternary phase | timeout | timeout | timeout |
| acquired p=7 | binary projected | timeout | timeout | timeout |
| acquired p=7 | ternary phase | timeout | timeout | timeout |

All timeouts returned after approximately 11.05--11.12 seconds of wall
time. Both SAT search traces pass VeriPB, as do separately retained compact
assignment certificates. Decoded binary witnesses pass exact PAF, SDS, and
cyclotomic PSD checks. Large traces are hashed scratch artifacts; no raw
UNSAT claim is accepted. The proof-v2 unchecked-deletion warning is limited
to SAT conclusions backed by independently checked complete assignments.

The initial p=5 phase join took 2.445 seconds. To separate translation
savings from update performance, supplemental controls ran both an
incremental phase join and a bit-packed join on exactly the same canonical
candidate sets:

| branch | incremental phase PAF | independent packed PAF | ordered count |
|---|---:|---:|---:|
| p=3 | 0.0068 s | 0.0114 s | 135 |
| p=5 rank 1 | 0.9636 s | 1.8096 s | 27 |

The same-domain p=5 measurement favors incremental updates by about 1.88x.
The difference between the initial and supplemental timings illustrates
runtime variability; these are local measurements, not asymptotic claims.
Comparison with the older 7.75-second join also includes the threefold
reduction in row enumeration from fixing translations and is not a pure
cross-term-update speedup.

At p=7 the exact join reached its 250,000 stored-signature cap in 2.001
seconds, after visiting 250,001 stored-side candidates and before streaming
any partner row. Its zero match count carries no information about binary
liftability. The smaller canonical row domain alone contains 3^14 =
4,782,969 candidates; the other contains 3^16 = 43,046,721.

The main benchmark took 148.792 seconds; the three earlier first-stage
retries took about 63.23 seconds, with the supplemental controls recorded
separately. The largest sampled solver working set in the main comparison
was 14,528,512 bytes; Python join peak memory was not measured. Scratch proof
files total 321,174,052 bytes, and retained results occupy about 2.67 MB.
Metadata records all executable hashes, model hashes, commands, timestamps,
certificate transcripts, and individual resource observations.

## Decision

Keep the phase model and incremental join as exact tools. They reduce model
size and small-case enumeration cost, and the bounded intermediate heuristic
provides a p=7 test branch. However, moving the quadratic structure into a
smaller PB model did not solve the p=5 or p=7 lift bottleneck. More explicit
row enumeration also runs into the p=7 storage bound.

The next bounded experiment should implement finite-domain propagation on
the ternary phase differences and the weighted PAF sums, retaining cycle
consistency and every cross term. Its acceptance gates should reproduce the
p=3 count of 135, the p=5 rank-1 count of 27, and a previously exhaustively
checked empty p=5 branch before trying the saved p=7 branch. Because active pairs
form a complete graph within each row, a small graph separator must not be
assumed. No evidence here justifies a p=37 run.

Reproduction:

```powershell
python -m scripts.benchmark_ternary_phase `
  --solver tmp/tools/roundingsat/roundingsat.exe `
  --verifier tmp/tools/veripb-3.0.2/bin/veripb.exe `
  --search-seconds 10
```

The optional `--packed-controls-only` appends same-domain controls to an
existing benchmark without repeating solver searches. The three preliminary
p=7 acquisition retries are separately preserved in `p7_acquisition.json`;
they used the earlier `_search` runner, the canonical first-stage model,
twenty-second limits, and restart multipliers 50/100/200, with exact commands
in that file.
