# Experiment log

No open-search experiments have been run.

## EXP-428-001: published construction reproduction

- Status: reproduction; PASS
- UTC start and end: initial audit began 2026-07-25; final deterministic
  rerun completed before 2026-07-25T17:58:11.406Z (exact start timestamp was
  not captured)
- Objective: reconstruct the published order-428 matrix from its `TT(36)`
  source sequences
- Mathematical constraints: exact Turyn-type, base-sequence, T-sequence, and
  full Hadamard Gram identities
- Configuration file: none; fixed source data in `src/order428.py`
- Random seed: not applicable; deterministic
- Git commit: working tree on branch `agent/order-428-reproduction`; final
  commit recorded by repository history
- Hardware and software: Windows 11, AMD64 Family 25 Model 117, Python 3.14.6
- CPU cores / peak memory / storage: one core / not instrumented / under
  0.5 MB frozen package
- Complete output: `results/H428.csv`,
  `results/H428_metadata.json`, and both verification reports/sidecars
- Exact checker: `src.verify_matrix` and the separately parsed,
  bit-packed `src.verify_matrix_independent`
- Result: PASS/PASS; candidate SHA-256
  `c00e3f86da7acdab1123fb9d2ed5fc887d5b86dd786662ab37e46a3072cc7869`
- Interpretation: successful independent computational reproduction of the
  published existence result at order 428
- Limitations / failed cases: not a result at order 668; the original
  publisher-era matrix file was not recovered. Initial pytest setup failed
  because the system temp directory was inaccessible; repository-local
  `--basetemp` resolved it.
- Reproduction command: `python -m scripts.reproduce_h428`
- Recorded wall time: 3.126743 seconds for generation and both verifiers

## EXP-LP-001: exact framework and published small pairs

- Status: reproduction; PASS
- UTC start and end: literature audit and implementation on 2026-07-25;
  deterministic artifact rerun started 2026-07-25T23:12:50.174573Z and
  completed 0.112203 seconds later
- Objective: implement the exact binary Legendre-pair, SDS, cyclotomic PSD,
  compression, and bordered-Hadamard pipeline and reproduce published pairs
- Primary sources: `fletcher2001`, `djokovic2015compression`, and
  `kotsireas2021mod3`, audited from complete PDFs; structured-example context
  from the accessible publisher text of `kotsireas2027pq2`
- Mathematical constraints: every nonzero PAF shift; negative-support ordered
  differences; every nonzero cyclotomic PSD sum; generic compression PAF
  identities; exact 3/9/37 paths; complete final Hadamard Gram identities
- Configuration file: none; fixed source signs in `src/legendre.py`
- Random seed: not applicable; deterministic
- Git commit: working tree on branch `agent/order-428-reproduction`; final
  commit recorded by repository history
- Hardware and software: Windows 11, AMD64 Family 25 Model 117, Python 3.14.6
- CPU cores / peak memory / storage: one core / not instrumented; largest
  matrix 56 by 56 / small CSV and text package under `results/legendre_examples`
- Complete output: `results/legendre_examples/metadata.json`, H8/H12/H16/H56
  CSVs, and both verifier reports and sidecars for every matrix
- Exact checker: `src.legendre`, `src.verify_matrix`, and separately parsed,
  bit-packed `src.verify_matrix_independent`
- Result: LP(3), LP(5), LP(7), and LP(27) PASS all exact source constraints;
  H8, H12, H16, and H56 PASS/PASS. Candidate hashes are in metadata.
- Interpretation: successful reconstruction of the source sequences and the
  `LP(n) -> H(2n+2)` theorem, including a length divisible by 3 and the
  parameter 27=3*3^2
- Limitations / failed cases: no LP(333) search was run and no order-668 result
  is claimed. The newer structured LP(27) data remain unreproduced because the
  publisher embeds signs in a dynamic figure, blocks the direct PDF, and does
  not fully specify the trace convention in searchable text. An initial trace
  interpretation was rejected when it failed to return base-field bits.
- Reproduction command: `python -m scripts.reproduce_legendre_examples`

## Entry template

- Experiment ID:
- Status: exploratory / exhaustive / reproduction
- UTC start and end:
- Objective:
- Mathematical constraints:
- Configuration file:
- Random seed:
- Git commit:
- Hardware and software:
- CPU cores / peak memory / storage:
- Complete output:
- Exact checker:
- Result:
- Interpretation:
- Limitations / failed cases:
- Reproduction command:

Verifier unit tests are software validation and are recorded in commit/CI
history rather than as research experiments.
