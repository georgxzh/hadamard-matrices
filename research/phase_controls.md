# Controlled ternary-phase benchmarks

Completed 2026-09-29 UTC. Exact counts are the primary result; timings are
local measurements, not state-of-the-art claims. No p=37 search was run.

## Separating the effects

`benchmark_phase_controls.py` uses the same reflected ternary Gray order,
mask updates, 14 projected PAF coordinates, byte keys, multiplicity buckets,
and stream hashing in all four join configurations. It changes only the
translation gauge and whether PAF is updated from incident edges or
recomputed by popcount. Stream digests match exactly between evaluation
methods. This removes the different candidate generators used in the earlier
`ternary_phase` comparison.

The translation gauge reduces the two-row scan from 708,588 to 236,196
candidates on each tested branch: exactly a factor of three. Its effect on
the solution-pair orbit count is a factor of nine. Rank 1 has 27 ordered
lifts (three canonical); rank 3 has zero in every configuration.

Three deterministic, shuffled-order repetitions were made. A separate join
run without other concurrent repository computations is the main timing
artifact, `results/phase_controls/isolated_joins.json`. OS/background load
and CPU frequency were not controlled. The original records are retained in
`metadata.json`; a 13.84-second classification audit overlapped part of that
run's solver phase. The separate join trial was added to reduce timing
ambiguity, not to discard an unfavorable outcome.

| Branch | Translation gauge | PAF method | Median seconds | Range |
|---|---|---|---:|---:|
| rank 1 | off | recompute | 5.737 | 5.387–7.314 |
| rank 1 | off | incremental | 5.706 | 5.186–7.161 |
| rank 1 | on | recompute | 1.879 | 1.807–2.590 |
| rank 1 | on | incremental | 1.709 | 1.697–1.778 |
| rank 3 | off | recompute | 5.903 | 5.450–10.115 |
| rank 3 | off | incremental | 5.192 | 5.172–5.859 |
| rank 3 | on | recompute | 1.839 | 1.803–2.499 |
| rank 3 | on | incremental | 1.717 | 1.657–1.806 |

With the gauge on, the median recompute/incremental ratios are 1.10 and
1.07. Ranges overlap. Earlier single-trial figures (0.96 versus 1.81 seconds)
do not isolate the update effect and must not be cited as its robust speedup.

## Phase PB versus binary PB

The binary model fixes the least negative-bit anchor word, selecting minority
layer 2 for anchor +1 and layer 0 for anchor −1. `AlignedPhaseModel` applies
exactly this gauge to phase PB, without changing the original phase model
or its saved artifacts. Exhaustive translation tests on known p=3/p=5 lifts
verify that both gauges select exactly the same row pair.

Both models use the same branch and projected shifts. RoundingSat runs with
`--lp=0 --print-sol=1 --verbosity=1 --luby-mult=100 --time-limit=10`, proof
logging, and a 15-second external timeout. Each pairing is repeated three
times in shuffled order. These are deterministic timing repeats, not three
independent seeds. Internal ten-second limits take approximately 11.1 seconds
wall time on these runs.

| Branch | Binary outcome / median seconds | Phase outcome / median seconds |
|---|---|---|
| p=3 known | 3/3 SAT; 1.659 | 3/3 SAT; 0.165 |
| p=5 rank 1 | 3/3 timeout; 11.087 | 3/3 timeout; 11.087 |
| p=7 saved branch | 3/3 timeout; 11.088 | 3/3 timeout; 11.074 |

Every p=3 SAT witness passes exact PAF/SDS/PSD checks, VeriPB's full search
proof check, and its compact witness certificate check. All timeouts remain
unresolved in solver records, including the independently known SAT p=5
branch. The saved p=7 branch's binary liftability remains unknown.

The phase encoding is smaller and wins the tiny positive control. Censored
p=5/p=7 results cannot establish a winner by time to completion. Complete
p=5 enumeration is useful within the tested domain; it is still exponential
and does not validate a p=37 plan. Potential phase propagation remains future
work, not an implemented scaling result.

## Audit, resources and reproduction

The initial control batch took 253.164 seconds, one solver at a time; the
Python process peaked at 39.04 MB and additional proof logs occupied
206.90 MB. Each join trial has a one-minute cap. The 24-trial separate run
therefore has a worst-case search budget below 30 minutes. Measured timing
and memory are in `isolated_joins.json`.

`audit_ternary_phase.py` verified 139 artifact hashes across the earlier
ternary experiment and the controlled PB runs; regenerated 35 OPB models
byte-for-byte; and reverified 19 SAT proof logs/certificates. It does not
reclassify timeouts as UNSAT. Tests passed: 156 total, including independent
coverage, gauge and inverse-map checks. The initial default pytest temporary
directory was inaccessible; rerunning with an in-repository `--basetemp`
resolved that environment issue.

```powershell
.venv/Scripts/python.exe -m scripts.benchmark_phase_controls
.venv/Scripts/python.exe -m scripts.benchmark_phase_isolated_joins
.venv/Scripts/python.exe -m scripts.audit_ternary_phase
.venv/Scripts/python.exe -m pytest -q --basetemp=tmp/pytest_paper
```

Avoid running other repository computations concurrently with the isolated
timing command. Executable hashes and complete commands are in `metadata.json`;
the paper's artifact manifest pins the finalized evidence. The fixed ternary
controls are p=3, p=5 and p=7 only.
