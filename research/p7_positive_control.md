# Published positive LP(63) control and publication assessment

Date: 2026-10-09. Baseline: `69aa1ae2634a27f1468bf7279222b288a10a0471`
on `agent/order-428-reproduction`. The initial read-only audit verified all
5,258 entries in the five existing manifests. The census and four empty
p=7 classes were not rerun or changed. Both frozen native executables match
their recorded hashes. No p=37 search was started.

## Primary witness and conventions

Kotsireas, Gómez and Gómez-Pérez, *On properties of Legendre pairs under
compression*, ISSAC 2025, pp. 79–86,
[DOI](https://doi.org/10.1145/3747199.3747549), Section 5.3.3, prints `a63`
and `b63`. A targeted primary-publisher indexed-HTML search for the DOI,
`63` and `sequences` returned this numerical block. Direct publisher fetch
returned 403. The numerical transcription, source locator and full
verification vectors are preserved in `results/p7_positive_control/witness.json`.
Trace representations and linear complexity were not independently checked.

We use the signs as printed, with the first printed element indexed zero.
Both row sums are 1. Standalone integer nested loops verify all 62 nonzero
PAF sums equal -2, with zero-shift sum 126. Independently, both negative
supports have size 31 and their combined directed difference counts equal
30 for every nonzero residue. These checks do not use projected PAFs,
phase formulas, or floating-point spectra. The 9-compression is exactly
`[1,3,3,-3,3,-3,-3]`, `[1,-3,-3,3,-3,3,3]`: **this witness belongs to the
prescribed p=7 family**, not merely an unrelated engine-validation domain.
Its existence is a published result, independently reproduced here.

For each row, choose the lexicographically smallest length-21 compression
among translations by 0, 7 and 14. The selected translations are 0 and 14.
Next shift each binary row by 21 so its first active minority phase is zero.
Thus our recovered representative is
`a'[j]=a63[(j+21)%63]`, `b'[j]=b63[(j+35)%63]`.
The corresponding negative masks are
`7677489779817452654`, `5050907891639286294`.
The branch is different from each of the four frozen empty classes.

Translation preserves the full PAF because changing summation index in
`sum x[j+t]x[j+s+t]` gives the original sum. Translation by 21 cyclically
subtracts one from all minority phases while fixing the intermediate row.
For a nonconstant column this action has no fixed binary row, so each
anchor-fixed row represents exactly three rows, independently on the two
sides. Translation by 7 at the intermediate stage preserves length-7
compression. These are the existing gauges applied to a published witness;
no new pruning rule, cross-term approximation or additional quotient is used.

## Pilots, completed experiments and exact solution sets

The intermediate active pattern is (16,16): 3^15 = 14,348,907 candidates
per anchor-fixed row. First 400,000-node probes, then real bounded
hash-table pilots, precede complete attempts. The real pilots estimate
30.68, 31.65 and 21.95 seconds with a 10x empirical extrapolation margin
for modes 0, 1 and 2. Their caps are **unresolved pilot outcomes**, not
branch counts. The no-table probe severely understates mode-0 table cost;
the second pilot is necessary. These are not proven runtime bounds.
The allocation/reallocation envelope is 1,676,395,008 bytes and storage
allowance 100 MB. Complete trials have 180-second, 2-billion-node per-row,
14,348,907 stored-mask and 100,000-solution caps; one worker only.

Three serial shuffled batches (seeds 20261009, 20261010, 20261011) ran
without concurrent experiments. They take 22.31, 20.75 and 19.26 seconds.
All nine trials exhaust and return **3 anchor-fixed pairs / 27 ordered
fixed-intermediate lifts**, including the known pair. Complete canonical
sets are identical bytewise as parsed integer lists. Engine median (range):

| Mode | Engine seconds | Wrapper median seconds | Largest native peak |
|---|---:|---:|---:|
| Unfiltered | 15.298 (14.060–15.825) | 15.364 | 744.65 MB |
| Leaf spectral | 2.477 (2.259–3.582) | 2.520 | 8.81 MB |
| Prefix spectral | 2.212 (1.730–2.591) | 2.256 | 8.81 MB |

Setup, process-minus-engine, output verification, and wrapper times are
recorded separately in every trial; coefficient warm-up precedes timing.
Background OS load and processor frequency were not controlled. Leaf and
prefix ranges overlap, so their median ordering is not a robust universal
claim. Modes use the exact same frozen binary and projected matching key.
Leaf/prefix retain 35,223 / 34,746 row masks respectively. Prefix excludes
10,821,357 / 10,850,193 completion masses before leaves. Exact coverage is
`leaves + excluded_completions = 14,348,907` on both sides. Multiplicity
buckets retain every mask, including repeated keys; no deduplication of
inequivalent or equivalent witnesses is applied.

A separate 200,000-candidate full-PAF pilot estimates 92.39 seconds with
10x margin and a 1,118,330,048-byte envelope. Only after all native sets
agree do we run its 180-second complete attempt, with a known three-pair
output bound. The independent binary-column enumerator exhausts both row
domains in **23.16 seconds**, peak **274.91 MB**, and returns the same
three canonical pairs and count 27. It uses all 31 nonredundant PAF shifts,
support intersections and full-key collision checks, without the spectral
or projected pruning. Compiler/input are shared; this is independent
implementation evidence, not external replication or a formal proof log.

All emitted pairs were additionally checked by standalone nested loops at
all 62 nonzero shifts and via SDS. `solutions.json` expands the complete
canonical set into all 27 distinct ordered mask pairs for this fixed
intermediate. It does not quotient reversal, exchange or decimation, or
purport to list all pairs in the prescribed family. The published positive
class is selected for validation, not as an unbiased sample. It does not
alter the selection rule or conclusions of the frozen four-class portfolio.

## Lawful primary-literature comparison and access limits

| Dimension | Our audited fixed-branch join | Fast spectral paper | pq² paper |
|---|---|---|---|
| Domain | Prescribed length 9p; native implementation only L=27,45,63 | Publisher abstract: arbitrary odd sequence length | Publisher abstract: length pq² and fixed partial sums |
| Symmetry | Ordered rows; independent intermediate shifts by p and phase anchors | Exact quotient/conventions not audited | Abstract mentions decimations/cosets; exact quotient not audited |
| Pruning | Necessary PSD ceiling; certified partial-phase rectangles | Abstract: matrix spectra/Gershgorin and FFT-like DFT computation; full pruning loop unknown | Abstract: compression/SDS improvements; full pruning rules unknown |
| Matching | Exact projected PAF vectors, all mask multiplicities, full collision check | Full matching algorithm inaccessible | Full matching algorithm inaccessible |
| Lifting | Bijective factor-three minority phases, all cross terms/carries retained | Full lifting procedure inaccessible | Full lifting procedure inaccessible |
| Numerical safeguards | Rational coefficient enclosures, inflated integer rectangles, strict rejection, final integer PAF checks | Error bounds/tolerances and exact acceptance not audited | Arithmetic and verification safeguards not audited |

Fast spectral reference:
[Perera–Kotsireas, LAA 721 (2025), 149–171](https://doi.org/10.1016/j.laa.2025.01.010).
The publisher abstract and author institution's
[publication record](https://portfolio.erau.edu/en/publications/a-low-complexity-algorithm-to-search-for-legendre-pairs/)
were inspected. The institutional page links only the DOI. No full algorithm
or code was obtained. The claimed speedup in its abstract is not a matched
benchmark against our conditional enumeration, so we do not compare ratios.

pq² reference:
[Kotsireas et al., JSC 138 (2027), 102606, online July 2026](https://doi.org/10.1016/j.jsc.2026.102606).
The indexed primary publisher abstract was inspected; direct HTML/PDF
attempts failed. Targeted author, URJC/Cantabria repository and preprint/code
searches located no usable full copy; this does not prove no copy exists.
Cantabria repository browsing was blocked by robots.txt.

Public OpenAlex metadata returns only the publisher DOI location for each
paper (closed for fast spectral, open for pq², neither with a PDF URL).
Crossref exposes official publisher text-mining links. Unauthenticated
publisher API GETs succeed in the default view but contain only `coredata`:
**no algorithm body**. Requesting the official `FULL` view returns HTTP 401
for both papers, and access attempts stop there.
For pq², the returned publisher license is CC BY 4.0; this license does not
make its full algorithms accessible in this session. Metadata receipts and
payload hashes are preserved separately. No paywall/access-control workaround
or author messaging was used. The access matrix records unknowns rather than
claiming those procedures were absent. Full priority comparison remains open.

Compression/successive lifting are established in ISSAC 2025 and
Đoković–Kotsireas (2015); PSD exclusion/matching precede us in
Fletcher–Gysin–Seberry (2001). Golay literature supplies additional matching,
lifting and floating-point safeguard precedents, in different sequence
domains. The rational prefix-phase rectangle is a potentially useful
specialization, **not a demonstrated first method**. This milestone adds
an exact conditional list and a positive reproduction, not a new length or
a stronger search algorithm.

## Strongest defensible contribution and submission gaps

Prefer a **restricted census and reproducibility paper**: the complete
1,164-class p=5 census under explicit multiplicities, the four fixed empty
p=7 classes, and this complete positive fixed branch, tied to exact proofs,
independent enumerators and a controlled filter ablation. The candidate
computational contribution is the auditable conditional census artifact;
its priority remains unresolved. A methods-priority or competitive-speed
paper is not supported by the present comparison. The positive-control gap
is closed, but publication readiness is not established.

Submission gates, in priority order:

1. Obtain and audit both full algorithms/code lawfully; map exact domains,
   symmetries, bucket multiplicities, lifting and numeric safeguards before
   any priority or performance claim.
2. Compare the restricted length-45 classes with the historical complete
   representative list (3,058 global classes reported in 2001); establish
   whether the conditional artifact supplies information absent there.
3. External independent replication with a second environment/compiler and
   stable archival release. Hashes alone do not certify exhaustion.
4. Broader predetermined p=7 sampling only if a scope/utility argument
   requires it; five classes, one selected positive, do not classify p=7.
5. Confirm authorship, sharpen exposition, and obtain verified TeX compilation
   and visual layout. There is no formal enumeration proof certificate.

Additional optimization is not the highest-value next milestone. No
extrapolation to p=37 or claim of proximity to order 668 follows.

## Reproduction

The frozen native binaries are byte-identical to the baseline. Rebuild using
`src.spectral_join.build_native()` and the command/flags in
`scripts/build_p7_study.py` if required, without overwriting old study metadata.
For fresh controls, use a separate in-repository output directory. On this
machine the old `.venv` launcher reports a missing base executable; the
bundled Python 3.12.14 was used, and native hashes did not change.

```powershell
$positivePython = 'C:/Users/georg/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:HADAMARD_POSITIVE_OUT = 'tmp/p7_positive_replication'
& $positivePython -m scripts.p7_positive_control setup
& $positivePython -m scripts.p7_positive_control pilot
& $positivePython -m scripts.p7_positive_control join-pilot
& $positivePython -m scripts.p7_positive_control trial 0
& $positivePython -m scripts.p7_positive_control trial 1
& $positivePython -m scripts.p7_positive_control trial 2
& $positivePython -m scripts.p7_positive_control independent-pilot
& $positivePython -m scripts.p7_positive_control independent
& $positivePython -m scripts.p7_positive_control audit
Remove-Item Env:HADAMARD_POSITIVE_OUT
```

Do not run timing experiments concurrently. Read the pilot before extending
caps. The independent stage refuses if native sets have not all exhausted
and matched. Archived initial/timing protocol snapshots retain the actual
source hashes used before later audit/reproduction refinements. Use the
current script for fresh outputs. Lawful metadata queries are reproduced by
`python -m scripts.probe_p7_literature` (network access required; no experiment).
The study manifest and manuscript hash ledger pin the full evidence package.
