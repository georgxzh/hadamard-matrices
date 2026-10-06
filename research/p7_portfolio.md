# Systematic bounded p=7 portfolio

Study date: 2026-10-06. No p=37 search. Results are generated from completed
records in `../results/p7_portfolio/`; stopped records retain null exact counts.

## Candidate contribution and source access

The candidate contribution is a proved rational rectangle exclusion for
partial minority-layer assignments, coupled to an exact restricted branch
classification and controlled evidence. PSD exclusion, correlation matching,
compression and recursive lifting are established (`fletcher2001`,
`djokovic2015compression`, `kotsireas2025compression`,
`lumsden2025periodic`, `bright2019complexgolay`). Our specialization is an
independent implementation whose priority remains unresolved. Native execution
is engineering, and no new exponential complexity bound is claimed.

For `perera2025fast`, the indexed publisher introduction and Section 3/4
previews identify Bluestein/FFTW structured Fourier evaluation. Direct HTML
returned 403; the full factorization and numerical/search conventions were
not accessible. This addresses Fourier evaluation cost, while our prefixes
exclude candidate subtrees. Their interaction and superiority require the
complete algorithm and comparable domains; no head-to-head claim is made.

For `kotsireas2027pq2`, the indexed primary abstract mentions compression,
decimations, cosets and SDS, but full HTML/PDF retrieval failed despite an
open-access label. Primary institution/preprint searches did not recover a
complete manuscript. Its phase/search details therefore remain unaudited.
The accessible ISSAC predecessor, Section 4.1, already specifies two q-lifts;
its conjectural trace/linear-complexity discard is not used here. The
literature access record distinguishes read sections from inaccessible text;
it cannot support a first-method claim.

## Starting evidence

Starting commit: `03876f3747a7f1505dd84d128ef4dbade115ab67` on
`agent/order-428-reproduction`. The four manifests' 5,081 entries were
checked before extension. The spectral consistency audit was rerun, matching
all 1,164 frozen p=5 mask lists, 2,976 canonical pairs, all coefficient
certificates, and the saved empty p=7 evidence. The refreshed audit is
recorded separately; original frozen files remain byte-identical. This is
a consistency/witness audit, not a fresh exhaustive p=5 enumeration. The
native executable remains the preceding audited SHA-256, and the new timing
harness is checked byte-for-byte against its frozen wrapper at capped inputs.

## Selection, verification and bias

For ordered target patterns (12,20),(13,19),(14,18),(15,17),(16,16), run four
fixed seeds each, `20261006+100*pattern_index+offset`, with 200,000 iterations
and a 20-second wall guard per attempt. Annealing is the previous exact
incremental integer-PAF acquisition with an added *heuristic* active-count
penalty. This penalty does not prune a lift: it only proposes intermediates.
Every accepted intermediate is independently re-evaluated for all length-21
compressed PAF constants, prescribed length-seven compression, row sums and
the existing first-stage OPB constraints before admission.

Canonicalize independent shifts by seven using the proved existing gauge,
deduplicate **ordered** translation classes, then choose the minimum pair
SHA-256 per acquired ordered pattern. Pair hashes use compact JSON of the
two rows. Add the previously resolved empty intermediate as a mandatory
control. This freezes the portfolio **before** any lift pilot or timing.
There is no reversal, row-exchange or decimation quotient in these counts.
Binary first-active minority layers are fixed to zero independently; ordered
fixed-intermediate lift counts are nine times canonical pair counts.

The 20 attempts found verified candidates only at (14,18),(15,17),(16,16).
The portfolio contains four classes including the (15,17) control. Failure
to acquire (12,20) or (13,19) is unresolved and does not exclude their
existence. This is targeted annealing, not a uniform or exhaustive sample.
Success probability and first-hit stopping bias the pool. Minimum-hash
selection does not remove this bias. Equal budgets retain both balanced
tables and larger asymmetric streaming domains instead of conditioning on
lift success or short timings. All branches have combined active count 32,
so the anchor-zero pair domain has 3^30 tuples, but individual row costs vary.

## Resource gates and timing protocol

Use one worker and serial trials; no concurrent repository experiment runs
during the timing batches. Each native configuration has an 80-second cap,
two-billion-node cap per row, 15-million stored-mask cap and 100,000-solution
cap. All stops remain unresolved. The supported largest stored domain is
3^15=14,348,907 masks. Conservative table capacity plus reallocation/wrapper
allowance gives 1.68 GB, below the 10-GB limit. Expected evidence is 30 MB;
the conservative storage allowance is 1 GB including capped solution lists
and aggregate records. No proof logs grow without a bound.

The first 400,000-node row probes omit joins and underestimate unfiltered
timing. A supplementary pilot therefore exercises real key generation under
250,000 stored masks/one million nodes. Its tenfold extrapolations cover
early prefixes only and are not proven time bounds. Every class remains in
the experiment even when its estimate exceeds the trial budget. Four classes
times three modes times 80 seconds give a 960-second worst engine sum per
batch, with a 1,500-second controller guard below the 30-minute run limit.
The independent all-shift auditor receives its own pilot before larger checks.

Three replicate batches use shuffled order with seeds 20261006, 20261007,
20261008. The native implementation, exact input, traversal, multiplicity
buckets and PAF verification are identical across modes 0/1/2. Modes 1/2
share bound maintenance, while mode 0 disables that work along with the
spectral tests. The leaf/prefix comparison isolates prefix testing.
No PB, translation or update speedup is
credited to this ablation. Native engine time excludes its preparation;
the harness separately records Python setup, native process wall time,
native wall minus engine, exact witness validation and total wrapper time.
Coefficient warmup is measured separately outside the engines. Native
process residual includes process startup and native pre/post work, not a
pure setup measurement. Wrapper time is measured before the final JSON
rewrite. OS load and frequency are uncontrolled; deterministic repeats
measure timing variability, not independent solution samples.

## Exactness and independent checks

No new search pruning is introduced; the spectral soundness, coefficient
error bound, complete cross terms and projected PAF theorem are unchanged.
Exhausted rows must satisfy visited leaves plus safely excluded completion
mass equals 3^(k-1); exact leaf keys keep every mask and repeated signature.
Completed variants and trials must have identical **full solution lists**,
including zero counts. Witnesses get full PAF, negative-support SDS,
compression and anchor checks in Python. Stopped runs retain verified lower
bounds, never substituted for exact counts or timing completions.

The independent binary-column auditor uses all 31 PAF shifts, an intersection
identity rather than the join's XOR identity, sorted fingerprints with full
key equality and no spectral/projected filter. Every class gets a bounded
180-second attempt after its pilot. Full independent completion requires
both complete row domains and exact-list agreement. The input and compiler
are shared; this is not an external replication or formal UNSAT certificate.

## Reproduction

Run these separately from the root with the recorded existing native
toolchain. The acquisition/selection precedes pilots and lift trials.

```powershell
.venv/Scripts/python.exe -m scripts.p7_study acquire
.venv/Scripts/python.exe -m scripts.build_p7_study
.venv/Scripts/python.exe -m scripts.p7_study pilot
.venv/Scripts/python.exe -m scripts.p7_join_pilot
.venv/Scripts/python.exe -m scripts.p7_study trial --trial 0
.venv/Scripts/python.exe -m scripts.p7_study trial --trial 1
.venv/Scripts/python.exe -m scripts.p7_study trial --trial 2
.venv/Scripts/python.exe -m scripts.p7_study independent-pilot
.venv/Scripts/python.exe -m scripts.p7_study independent
.venv/Scripts/python.exe -m scripts.check_p7_invariants
.venv/Scripts/python.exe -m scripts.p7_study audit
.venv/Scripts/python.exe -m pytest tests/test_p7_study.py -q --basetemp=tmp/pytest_p7_protocol
.venv/Scripts/python.exe -m scripts.update_paper_results
.venv/Scripts/python.exe -m scripts.verify_spectral_paper
```

Completed tables, publication assessment and hashes are incorporated below
from the audited summary. No conclusion covers unacquired intermediates.

## Completed outcome and publication decision

All 36 native trials exhaust with identical empty lists. The serial batches
took 171.50, 166.72 and 160.38 seconds. No native timing trial reached a cap.
Engine medians (ranges), seconds:

| Class | Off | Leaf spectral | Prefix spectral |
|---|---:|---:|---:|
| Prior control (15,17) | 24.197 (22.056–28.649) | 3.751 (3.744–3.754) | 2.685 (2.420–4.038) |
| New (14,18) | 68.352 (68.192–69.726) | 9.612 (9.238–9.795) | 6.031 (5.213–7.285) |
| New (15,17) | 22.940 (22.681–24.229) | 3.969 (3.783–4.117) | 2.445 (2.418–3.143) |
| New (16,16) | 14.113 (13.841–14.858) | 2.536 (2.233–2.666) | 2.723 (1.718–3.952) |

The balanced case's prefix median regresses despite reducing nodes; ranges
overlap substantially. Prefix/leaf is not a uniform performance ranking.
Both spectral variants have lower medians than the matched off mode in all
four cases. This is not an estimate of general p=7 scaling or a literature baseline.

Full independent PAF enumeration exhausts every class: prior control in
43.76 seconds, new (14,18) in 84.90, new (15,17) in 36.26, and balanced
(16,16) in 18.98. Both row domains are completely enumerated in each check.
All return **zero canonical and ordered lifts**. No binary witness exists in
these records; verified intermediate witnesses are a different object.
There is no formal UNSAT certificate, nor a claim about all p=7 classes.

The largest native trial peak is **744.39 MB** and the study package is about
**1.46 MB**. Additional checks reproduce the selection, deterministic row
counters, equal leaf/prefix survivor counts, exact coverage and resource
limits. Five new protocol tests passed in 1.59 seconds before timing. Both
binaries rebuilt to the original audited hashes after timing. The old test
counts remain historical; a new full-suite pass is not claimed.

Prefer a **restricted census/reproducibility paper with proved specializations**.
The full p=5 restricted census and this small conditional p=7 study are
completed evidence. A methods-priority/performance paper would need the full
fast-spectral and pq-squared algorithms, comparable external baselines,
broader independent classes and a verified positive p=7 control. Even the
restricted artifact's novelty remains unresolved pending historical-list
comparison and external replication. This is a draft direction, not a
claim of submission readiness or a new existence result.

The balanced regression justifies a future safe prefix-cadence/frequency-order
ablation; skipping a necessary test weakens pruning without deleting lifts.
First obtain a positive control and broaden predetermined strata, including
opposite row orientations and unresolved acquisition patterns, with new
bounded pilots. No p=37 search follows.

The frozen portfolio SHA-256 is
`89ddeb0ec8a73747779b6f12886caa663a42b51e2ffb1939c8bf353f77ef1b49`;
the study manifest is
`40fe52a4f632660d5e786ffb23cc50b0cdff464e0aecf0b2b8cd29fa5724e8a7`.
The manifest pins all 159 evidence/source entries. The supplementary paper
manifest also pins this note, the timing harness parity tests, build and
invariant-check scripts, renderer and publication assessment.
