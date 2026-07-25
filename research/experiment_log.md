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
