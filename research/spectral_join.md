# Certified spectral joining: resolved saved p=7 branch

Status: completed and audited, 2026-10-04 UTC. No p=37 search.

The new exact implementation directly reproduces **all 1,164 p=5 branches**
and every binary mask in the frozen census. All three native modes exhaust
the saved p=7 intermediate pair with **zero binary lifts**. An independent
binary-column enumerator, checking all 31 nonredundant PAF shifts, also
exhausts the branch and returns zero. This resolves that intermediate pair,
not other p=7 branches, all LP(63), or order 668.

## Bottleneck and selected change

The audited row-conditioned propagation builds the smaller row table before
searching partners; its p=7 probe stopped at 250,000 candidates before that
search began. Partner-signature bitsets reduced p=5 nodes but increased time.
The replacement applies a cheap necessary **single-row PSD bound** before
materializing the table, with bounds on partial ternary assignments. A compact
native join retains every surviving mask and checks complete integer keys.
Matched native modes isolate spectral filtering; comparisons to the Python
join also change execution language, traversal and PAF evaluation.

Mode 0 disables spectral exclusions; mode 1 tests complete rows; mode 2 tests
prefixes and complete rows. All modes fix each row's first active minority
phase to zero. They keep the existing factor-nine relation between canonical
and ordered fixed-intermediate lifts. There is no row exchange or additional
decimation quotient in these counts.

## Safe exclusion proof and cross terms

Let L=3N, and write a row as a repeated sign baseline plus the minority-layer
contribution at each active residue: x[i+kN]=b[i]+d[i] [a[i]=k], where
d[i]=-2b[i]. Forced residues have d[i]=0. Its Fourier sum is exactly the
baseline Fourier sum plus the phase contributions. This is a parameterization
of the entire binary row, including all layer positions and carries.

At a nonzero frequency f, a binary Legendre pair satisfies
PSD_x(f)+PSD_y(f)=2L+2. Hence each row individually has PSD at most 2L+2.
This exclusion principle is established in `fletcher2001`, Section 5.1.

The coefficient generator uses scale S=2^20 and exact rational intervals
enclosing cosine and sine with error at most one integer unit. Machin's
identity, 32/31-term alternating arctangent sums and outward rounding give
pi bounds. After argument normalization to [0,pi], monotonicity and cosine
partial sums through indices 21/20 enclose each value. The generator checks
each enclosure within the chosen integer coefficient plus/minus one unit;
the rational bounds are saved in `coefficients_27/45/63.json`.

For a phase prefix, sum the fixed contributions and each unassigned phase's
coordinate-wise minimum/maximum over its three possible layers. These give
a rectangle enclosing every completed approximate Fourier sum. The real
and imaginary extremes need not be attainable together: this only enlarges
the rectangle. Inflate both coordinate intervals by L, since the error of
the final binary sum is bounded by sum |x_i|=L in each coordinate. The tighter
L error is valid despite the baseline-plus-minority representation: its sum
is exactly the same integer-coefficient sum of the completed binary row.

If r and t are the distances of the inflated real and imaginary intervals
from zero, exclude a prefix only when

`r*r + t*t > S*S*(2*L+2)`.

Every completion's scaled PSD is at least the left side, contradicting the
necessary upper bound. Equality is retained. There are no floating-point
pruning decisions. Squaring the full Fourier sum contains **all** cross terms;
the rectangle relaxes their interactions, and exact PAF equations retain
them at matching. Only nonzero frequencies not divisible by three are
tested; omitting frequencies weakens exclusion and cannot remove a lift.
N is restricted to 9,15,21, so squared bounds fit signed 64-bit arithmetic
and binary support masks fit unsigned 64-bit arithmetic.

Every excluded prefix represents exactly 3^q completions for q remaining
phases. Exhausted rows require `leaves + excluded_completions = 3^(k-1)`.
The table stores an entry for **every mask**, including all repeated PAF
signatures. Hash collisions require full-key equality. Every matching bucket
entry is visited and checked at all nonredundant PAF shifts. The projected
PAF theorem proves sufficiency of shifts 1 through N-1 for this intermediate
pair; the Python wrapper additionally checks row sums, compression, full
PAFs and negative-support SDS identities for every emitted pair.
Time, node, table and solution caps return null exact counts with separate
lower bounds. A stopped search is never reported empty.

## Primary literature and claim limits

`fletcher2001`, Sections 5.1 and 5.3, already uses PSD exclusion followed by
matching. `lumsden2025periodic`, Sections 2, 3.4 and 4, explicitly gives PSD
filters, all equal-signature bucket combinations, multilevel compression
and recursive uncompression. `bright2019complexgolay`, Sections 3.3 and 3.5,
uses partial-correlation conflicts and FFT spectral filtering with an explicit
numeric tolerance, precomputed contributions and frequency ordering in the
complex aperiodic setting. It is a methodological precedent, not an LP(63)
classification. These primary sections were read for this milestone.

The periodic binary rectangle bound with rational coefficient certificates is
a proved specialization independently implemented here. Its priority is
**unresolved**. No new PSD criterion, first matching algorithm, new length,
general complexity improvement, or state-of-the-art timing is claimed. Full
comparisons with `perera2025fast` and `kotsireas2027pq2` remain missing. The
historical complete LP(45) representative list has still not been obtained;
our 63 subset equivalence classes are not the literature's 3,058-class census.

## Pilot gates and completed measurements

Limits were four cores, 1,800 seconds per command and 10 GB. No run exceeded
them. The frozen pilot used three workers and 12 p=5 ranks, sampling every
active-count stratum, plus 200,000-node p=7 row probes. Its 5.63 seconds
included compilation. It estimated 324.73 seconds and 277.05 MB for the p=5
batch, 64.15 seconds per p=7 method with a tenfold timing margin, a 1.2-GB
p=7 memory envelope, and 20 MB storage. Prefix probes are deterministic,
not a proven runtime bound. The eventual evidence exceeds that storage
estimate because every native input was preserved, but remains far below
10 GB: the final spectral package occupies 29.65 MB. Frozen process peaks
exclude unrelated processes and kernel memory.

The p=5 batch took **63.90 seconds**, reusing 12 direct pilot cases. Both
modes 0 and 2 directly enumerate every branch, with no symmetry transfers.
Exact lists agree with the independent prior census: ordered count histogram
0:460, 27:464, 54:192, 81:48, totaling 2,976 canonical and 26,784 ordered
lifts of the fixed intermediate catalogue. The further intermediate
translation factor remains nine, giving 241,056 for the prescribed domain.
The conservative sum of wrapper/native worker peaks was 139.54 MB, obtained
by summing process maxima rather than observing simultaneous system usage.

A separate one-worker batch uses three deterministic shuffled replicates,
seed 20261004, with no concurrent repository experiment. Medians in seconds:

| Control | Existing Python join | Native off | Native leaf | Native prefix |
|---|---:|---:|---:|---:|
| p=3, 135 ordered lifts | .0110 | .0012 | .0012 | .0015 |
| p=5 rank 1, 27 | 1.6556 | .0335 | .0342 | .0316 |
| p=5 rank 3, 0 | 1.5332 | .0387 | .0262 | .0257 |
| p=5 rank 1133, 54 | 10.9219 | .1782 | .1587 | .1143 |

Native engine times exclude setup and process startup; wrapper times are
also recorded. The Python/native speed difference is confounded by the
implementation changes. The native comparison isolates spectral testing.
Prefix tests slow the tiny p=3 control. Ranges overlap at ranks 1 and 3;
rank 1133 ranges are disjoint (.164-.179 versus .073-.130 seconds). Three
replicates, one machine and uncontrolled OS load do not support broad claims.
The previous translation/incremental-PAF/phase-PB ablations remain separate
frozen experiments; none of their effects are credited to this spectral test.

The saved p=7 pair has 15 and 17 active residues, with anchor-zero row
domains **3^14=4,782,969** and **3^16=43,046,721**. All native modes exhaust
both domains or safely exclude their prefixes, returning zero lifts:

| Method | Engine seconds | Stored masks | Native peak MB |
|---|---:|---:|---:|
| No spectral filter | 26.135 | 4,782,969 | 375.66 |
| Leaf filter | 4.186 | 38,907 | 8.91 |
| Prefix filter | 2.635 | 38,907 | 8.91 |

Leaf and prefix modes retain the same 38,907/28,134 rows. Prefix pruning
accounts for 3,126,363 and 36,148,041 completions. Recorded nodes are
3,745,765 and 22,979,722, with 840,571/8,421,135 prefix conflicts. Table
capacity falls from 369.10 MB to 2.88 MB. The observed 9.9x engine speedup
is one branch with one trial per mode in fixed order (2,1,0). It does not
establish scaling on other branches. No binary witness exists for this pair;
the earlier verified intermediate witness remains valid and is not a lift.

## Independent exact check

`full_paf_audit.cpp` enumerates Cartesian binary column patterns with the
same anchor convention, independently of phase formulas and spectral bounds.
It evaluates all 31 shifts with the negative-support intersection identity
`L-4*weight+4*intersection`, rather than the new search's XOR/popcount PAF.
Sorted fingerprints require full-vector equality; repeated keys keep every
mask. Positive/empty p=5 controls match exact mask lists and counts 27/0.

Its 200,000-row pilot estimated 169.56 seconds, 406.11 MB and 1 MB storage
before the full audit. The full saved p=7 check enumerates both complete row
domains in **54.75 seconds**, with a **140.52-MB** native peak, and returns
zero. The auditor shares compiler and input with the main search; it is an
independent implementation, not an external replication or a formal UNSAT
certificate. Computational nonexistence is supported by both exhausted
enumerators, complete coverage and proved necessary exclusions.

## Reproduction and evidence

Use the repository root and the recorded Python environment; run commands
separately. The launcher uses installed MSYS2 GNU C++ 15.2.0 at
`C:/msys64/ucrt64/bin/g++.exe`, with
`-std=c++17 -O3 -mpopcnt -static -Wl,--no-insert-timestamp -lpsapi`.
It targets Windows x86 with popcount support; porting is untested. Generated
executables live in ignored `tmp/`. Coefficients are regenerated rationally.

```powershell
.venv/Scripts/python.exe -m scripts.benchmark_spectral_join pilot --workers 3
.venv/Scripts/python.exe -m scripts.benchmark_spectral_join full --workers 3
.venv/Scripts/python.exe -m scripts.benchmark_spectral_join controls
.venv/Scripts/python.exe -m scripts.benchmark_spectral_join p7
.venv/Scripts/python.exe -m scripts.audit_saved_p7
.venv/Scripts/python.exe -m scripts.audit_spectral_join
.venv/Scripts/python.exe -m pytest tests/test_spectral_join.py tests/test_phase_propagation.py tests/test_p5_equivalence.py tests/test_ternary_phase.py tests/test_p5_classification.py -q --basetemp=tmp/pytest_spectral_final
.venv/Scripts/python.exe -m scripts.update_paper_results
.venv/Scripts/python.exe -m scripts.verify_spectral_paper
```

The spectral manifest has 4,806 SHA-256 entries. The audit checks frozen
inputs, provenance, coefficients, full p=5 solution sets, each witness's
exact PAF/SDS/compression, multiplicities and p=7 coverage. It does not itself
rerun the complete searches; the commands above do. Key frozen hashes:

- Native search source: `f55675cd7c9b190410d671a8ef521b109438291dea534000765a64f0c238a5d3`.
- Native executable: `3bc0a21d0e69ede1ea4d9eaa7966b2cef6ac3c220335642c892c3d1a4163c328`.
- Prior p=5 census: `8cf7c10075511c30a765c4bb36aa37924a6af8e835cd86f2ef82a98ff7bfe1ea`.
- Independent p=7 result: `87c2d69fa4ae97fce25ceb447c0db2cbef8fafc8e3fd36149a35c9920f1c89e5`.
- Spectral manifest: `39e56606c32b603d74e983471ebc4d98dea9d361b8ffaf570d7738e5c863d682`.

## Next justified experiment

Use this validated filter on a **bounded portfolio of other verified p=7
intermediate translation classes**, initially balancing active counts, with
a new acquisition/runtime/storage pilot and exact per-branch records. Do not
infer that this empty pair represents others or that it disproves the full
structured p=7 prescription. Enumeration is still exponential. Continue to
retain PB as a certificate reference; do not start p=37 searches from this
single-branch result.
