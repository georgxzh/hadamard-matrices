# Hadamard Matrices

Rigorous, reproducible computational research toward the FrontierMath open
problem of constructing a Hadamard matrix of order 668.

> **Research status (2026-07-25): unsolved.** This repository does not contain
> a Hadamard matrix of order 668. A candidate counts as a solution only after
> two independent exact verifiers establish
> \(H H^{\mathsf T}=668I_{668}\) for the complete \(668\times668\) ±1 matrix.

## Current milestone

The low-risk foundations, order-428 warm-up, and exact Legendre core are complete:

- a mathematical primer and an explicitly qualified literature map;
- a source ledger that separates peer-reviewed results, preprints, software,
  and exploratory reports;
- two independent exact CSV verifiers;
- tests on Sylvester and Paley constructions, corrupted matrices, malformed
  inputs, and an approximately orthogonal near miss;
- an exact reconstruction of the Kharaghani--Tayfeh-Rezaie order-428 result
  from its printed `TT(36)` source sequences;
- a frozen `results/H428.csv` accepted by both independent exact verifiers;
- exact periodic autocorrelation, negative-support SDS, and cyclotomic PSD
  certificates for binary Legendre pairs;
- generic compression plus exact length-333 output paths of lengths 3, 9,
  and 37;
- published LP(3), LP(5), LP(7), and LP(27) source reproductions, yielding
  H(8), H(12), H(16), and H(56), each accepted by both exact verifiers;
- an independent derivation and proof of the structured `pq^2` compressed pair,
  replacing a blocked publisher artifact, plus an exhaustive factor-9
  uncompression at `p=3` recovering 7,614 canonical matches (77,274 ordered
  pairs with multiplicity) and a second, distinct dual-verified H(56);
- a deterministic exact pseudo-Boolean uncompression model, exhaustively
  validated on all 7,614 p=3 canonical matches, with an exact LP(333) model
  size and certificate plan but no solver search;
- a proved translation-canonical OPB variant reducing ordered prescribed
  uncompressions by an exact factor of 81, again exhaustively validated at
  p=3;
- a versioned audit of the current common-multiplier artifacts, locally
  reproducing 15 of 25 reported exclusions and recording the ten-case full
  proof gap;
- a phase-ordered plan and source-backed derivation for the remaining work.

No expensive computation has been started. The largest run to date enumerated
1,778,112 candidates on one core in 8.5 seconds.

The reproduced order-428 candidate has SHA-256
`c00e3f86da7acdab1123fb9d2ed5fc887d5b86dd786662ab37e46a3072cc7869`.
See [research/order428_reproduction.md](research/order428_reproduction.md)
for the paper-to-code audit. This does not solve order 668.

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
[research/source_ledger.md](research/source_ledger.md). The exact framework is
derived in [research/legendre_framework.md](research/legendre_framework.md) and
the structured `pq^2` route in
[research/pq2_derivation.md](research/pq2_derivation.md). The current direction
is recorded in
[research/direction_selection.md](research/direction_selection.md).
The exact OPB derivation and resource audit are in
[research/pb_uncompression_model.md](research/pb_uncompression_model.md).
The common-multiplier artifact boundary is documented in
[research/multiplier_artifact_audit.md](research/multiplier_artifact_audit.md).

### Why order 668 is still open

The `pq^2` route prescribes an exact 37-entry compressed pair whose binary
preimages, if any, would be length-333 Legendre pairs and hence H(668). That
compressed pair is now derived and certified here. Recovering a preimage by
enumeration would require scanning about `2.4e71` candidates per row — roughly
fifty orders of magnitude beyond reach. The obstruction is mathematical, not
computational; see [research/pq2_derivation.md](research/pq2_derivation.md)
section 5.

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
