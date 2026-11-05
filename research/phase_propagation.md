# Exact phase propagation: validation and limits

This milestone implements two exact searches in `src/phase_propagation.py`:

1. Ternary edge differences, exact triangle supports, and weighted PAF
   interval propagation. Anchor triangles alone ensure global realization;
   all triangles provide redundant local propagation.
2. A row-conditioned search: exhaust the smaller row, preserve every phase
   tuple in each signature bucket, then propagate partial phases of the
   partner row against exact partner-signature bitsets and optional folded
   PAF bounds. All cross terms are retained. This is not a partition of the
   complete interaction graph within a row.

The manuscript proves that each filter preserves every feasible assignment.
Complete traversal counts all phase-gauged solutions; timeout, node limit,
or storage cap yields a lower bound with exact counts explicitly null.

## Pilot and complete p=5 check

The 11-case stratified pilot completed in 67.00 seconds on three workers.
Its conservative full-run estimate was 484.14 seconds, 420.82 MB of worker
memory, and 10 MB of storage. This fits four cores, 30 minutes/run, and 10 GB.
The complete comparison reused those cases and finished in 268.73 seconds.
For a fresh reproduction, add pilot time. The largest recorded worker peak
was 98.56 MB; three times that peak is a conservative 295.69 MB worker-sum
bound, not a simultaneous total-system measurement.

All 79 representative cases completed, and the proved transformations
recover **exact solution-list agreement for every one of 1,164 branches**.
The count distribution is unchanged: 460 empty, 464 with 27 ordered lifts,
192 with 54, and 48 with 81. There are 2,976 phase-gauged pairs in total.
Both new searches share the phase formula with the older phase join; the
existing census additionally uses an independent binary-mask enumerator.
No new independent implementation of the symmetry-transfer proof is claimed.

The sum of recorded propagation times over representatives is 755.60 seconds,
versus 212.18 seconds for the existing join, a ratio of 3.56. These are
per-case wall times under three-worker concurrency, with propagation run
before the join; they are not CPU times or an isolated randomized benchmark.
They establish no speed improvement for this implementation. The join counts
all matches without retaining their masks; propagation retains its small
solution lists. Both preserve signature multiplicity.

## Literature and equivalence conversion

`fletcher2001` already reports a complete length-45 classification of 3,058
classes. Our restricted solutions occupy **63 classes** under its Section
5.4 operations: independent shifts/reversals, common decimation, and row
exchange. Of those classes, 61 contain 48 phase-gauged records in our subset
and two contain 24. Multiplying each intersection by 81 restores prescribed
ordered pairs: 61 × 3,888 + 2 × 1,944 = 241,056. These are not unrestricted
orbit sizes. The crosswalk has full per-solution labels, but the old list
has not been obtained, so no historical record-by-record match is claimed.

The conversion took 1.39 seconds and peaked at 41.46 MB. A 30-pair pilot
estimated 5.11 seconds with margin. A separate tuple oracle checks all
1,024 length-five binary mask pairs and 29 sampled length-45 pairs.

`lumsden2025periodic` Sections 3.4–5 provide explicit precedents for matching,
bucket multiplicities, multilevel compression, recursive uncompression,
and equivalence filtering. `kotsireas2025compression` already specifies
successive lifts; its conjectural trace filter is not used here. The exact
combination of difference and partner-support filters may be a useful
specialization, but novelty remains unresolved. Full-text comparisons with
`kotsireas2027pq2` and `perera2025fast` remain missing. See `source_ledger.md`.

## Isolated ablations and p=7

The one-worker control batch took 114.65 seconds and peaked at 182.44 MB.
Single trials hold the row domain and leaf lookup fixed:

| Branch | Partner filter | Folded bounds | Nodes | Lookup leaves | Seconds |
|---|---|---|---:|---:|---:|
| rank 1 | off | off | 263668 | 167877 | 3.990 |
| rank 1 | off | on | 262579 | 163608 | 4.072 |
| rank 1 | on | off | 148315 | 3 | 7.665 |
| rank 1 | on | on | 114763 | 3 | 8.688 |
| rank 3 | off | off | 265345 | 169034 | 2.416 |
| rank 3 | off | on | 265162 | 165432 | 3.110 |
| rank 3 | on | off | 153769 | 0 | 5.709 |
| rank 3 | on | on | 115366 | 0 | 6.129 |

All variants return 27 ordered lifts at rank 1 and zero at rank 3. Lookup
leaves are not solutions. Stronger pruning costs more wall time here; these
single trials establish no timing distribution. No other repository
experiment ran concurrently, although document/file work and OS load remain.

Both standalone triangle modes exhaust p=3 and return all 135 ordered lifts
in about 0.49 seconds. Each times out at ten seconds on both p=5 controls.
The p=7 standalone search times out at 30 seconds, and its row-conditioned
variant hits 250,000 stored candidates at 1.74 seconds before searching the
partner. **The saved p=7 branch remains unresolved.** No stopped run records
an exact zero. Frozen-result auditing passed all 1,164 branches, 2,976
solutions, and 63 subset equivalence labels in 1.33 seconds.

The new artifact package is about 0.71 MB. The phase join remains the best
demonstrated method here. Before more scaling, any stronger safe single-row
filter needs a mathematical derivation, exact p=5 validation, and a matched
bounded p=7 comparison. PB is still a certificate/reference route; its prior
ten-second timeouts do not rank uncensored completion times. No p=37 run is
justified by these results.

## Reproduce

Run separately from the repository root:

```powershell
.venv/Scripts/python.exe -m scripts.benchmark_phase_propagation pilot --workers 3
.venv/Scripts/python.exe -m scripts.benchmark_phase_propagation full --workers 3
.venv/Scripts/python.exe -m scripts.benchmark_phase_propagation controls
.venv/Scripts/python.exe -m scripts.crosswalk_p5_equivalence
.venv/Scripts/python.exe -m scripts.audit_phase_propagation
.venv/Scripts/python.exe -m pytest tests/test_phase_propagation.py tests/test_p5_equivalence.py -q --basetemp=tmp/pytest_phase_final
.venv/Scripts/python.exe -m scripts.update_paper_results
```

`results/phase_propagation/manifest.json` pins code, tests, input census,
and every pilot, representative, control, and equivalence record. The audit
checks frozen-result consistency; re-enumeration requires the pilot/full
commands. The prior binary census supplies the independent exact check.
No p=37 search is included.
