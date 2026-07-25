# Hadamard Matrices

Rigorous, reproducible computational research toward the FrontierMath open
problem of constructing a Hadamard matrix of order 668.

> **Research status (2026-07-25): unsolved.** This repository does not contain
> a Hadamard matrix of order 668. A candidate counts as a solution only after
> two independent exact verifiers establish
> \(H H^{\mathsf T}=668I_{668}\) for the complete \(668\times668\) ±1 matrix.

## Current milestone

The repository starts with the low-risk foundations required before any open
search:

- a mathematical primer and an explicitly qualified literature map;
- a source ledger that separates peer-reviewed results, preprints, software,
  and exploratory reports;
- two independent exact CSV verifiers;
- tests on Sylvester and Paley constructions, corrupted matrices, malformed
  inputs, and an approximately orthogonal near miss;
- a concrete plan for reconstructing the published order-428 result.

No expensive computation has been started.

## Exact verification

The default expected order is 668:

```powershell
python -m src.verify_matrix path\to\candidate.csv --report results\verification.txt
python -m src.verify_matrix_independent path\to\candidate.csv --report results\verification-independent.txt
```

The reference verifier uses direct Python-integer row inner products. The
independent verifier separately parses the file, bit-packs each row, and uses
exact Hamming distances. Reports include the candidate SHA-256; an adjacent
`.sha256` sidecar hashes both the candidate and the completed report.

For small test matrices, pass `--order N`.

## Development

Python 3.10 or newer is required.

```powershell
python -m pip install -e ".[test]"
python -m pytest
```

## Research rules

- Proven facts, reproduced results, computational observations, heuristics,
  conjectures, and failed attempts are labeled separately.
- Floating-point agreement is never accepted as proof of orthogonality.
- Published construction data are reconstructed where feasible, not merely
  downloaded and relabeled.
- Any run expected to exceed four CPU cores, 30 minutes, or 10 GB requires
  approval first.

See [research/primer.md](research/primer.md),
[research/literature_map.md](research/literature_map.md), and
[research/source_ledger.md](research/source_ledger.md).

## Repository layout

```text
src/          exact reference implementations
tests/        deterministic tests and known small constructions
research/     derivations, audits, decisions, and experiment log
references/   BibTeX source ledger
results/      frozen candidates and verification packages
scripts/      reproducible experiment entry points
```

## License

Code is released under the MIT License. Research notes cite their sources; the
rights in cited papers and external construction data remain with their owners.
