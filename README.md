# Hadamard Matrices

Rigorous, reproducible computational research toward the FrontierMath open
problem of constructing a Hadamard matrix of order 668.

> **Research status (2026-10-04 UTC): unsolved.** This repository does not contain
> a Hadamard matrix of order 668. A candidate counts as a solution only after
> two independent exact verifiers establish
> \(H H^{\mathsf T}=668I_{668}\) for the complete \(668\times668\) ±1 matrix.

## Current milestone

The complete prescribed p=5 lift census is now audited: all **1,164**
intermediate translation orbits are resolved, with **704 liftable** and
**460 empty** branches. Exact counts, multiplicities, symmetry maps and
independent checks are in [research/p5_classification.md](research/p5_classification.md).
The research draft is [paper/manuscript.tex](paper/manuscript.tex), with
primary-literature comparisons and explicit unresolved novelty questions.
Length-45 classification already exists in the literature; this is a
restricted reproducible census. No p=37 search was performed.

The new phase-propagation search also reproduces every branch and solution
in that census, but its row-conditioned variant is slower than the existing
join in the recorded comparison. The restricted solutions occupy **63**
classes under the published length-45 equivalence convention. Details and
bounded p=7 outcomes are in [research/phase_propagation.md](research/phase_propagation.md).

The certified spectral join now directly reproduces all 1,164 p=5 branches
and exhausts the **saved p=7 intermediate pair with zero binary lifts**.
An independent full-PAF enumeration confirms this restricted nonexistence
result. On that one branch, prefix filtering takes 2.64 seconds versus
26.13 seconds for the matched native unfiltered join; these are single-run
engine timings, not a general scaling claim. Proofs, primary precedents,
bounded pilots and reproducible evidence are in
[research/spectral_join.md](research/spectral_join.md). Other p=7 branches
remain unclassified. The next experiment is a bounded p=7 branch portfolio.

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
- an end-to-end LP(27) RoundingSat/VeriPB certificate benchmark: four SAT
  certificates verify, while bounded unfixed searches time out and therefore
  do not justify an LP(333) run;
- a primary-source reproduction of the structured LP(45), its successive
  3-compressions, both p=5 OPB models, and a dual-verified H(92);
- an exact conditional two-stage q=3 model: proof-producing staged searches
  solve both p=3 variants in under one second, while bounded p=5 searches
  time out and remain an explicit gap;
- an exact first-stage q=3 model and exhaustive generator: p=3 has 792 and
  p=5 has 10,476 ordered compatible intermediate pairs; the published p=5
  branch is recovered and both known-branch certificates pass VeriPB;
- a complete p=5 branch profile reducing those pairs to 1,164 translation
  orbits, plus a three-branch exhaustive portfolio yielding exact solution
  counts 27, 27, and 0 and a distinct dual-verified H(92) artifact;
- a non-enumerative p=37 first-stage OPB and an exact factor-three projection
  theorem reducing a future fixed-branch length-333 model to 73,926 variables
  and 293,372 records, validated exhaustively at p=3 and p=5;
- proved first-stage translation canonicalization with an exact factor-nine
  reduction, plus bounded p=5/p=7 scaling: all six p=5 first-stage searches
  succeed, all six p=7 searches time out, and the p=5 binary-lift comparison
  favors investigating a specialized cross-term-aware formulation;
- an exact ternary phase formulation and incremental PAF join, reproducing
  the p=3/p=5 counts and reducing fixed-branch PB model sizes; a seeded p=7
  intermediate branch passes VeriPB, but all bounded p=5/p=7 binary-lift
  probes still time out, motivating finite-domain phase propagation;
- a versioned audit of the current common-multiplier artifacts, locally
  reproducing 15 of 25 reported exclusions and recording the ten-case full
  proof gap;
- a phase-ordered plan and source-backed derivation for the remaining work.

The census used a bounded 21-branch pilot followed by 79 direct symmetry
representatives on three workers. The reduced run took 6.58 minutes and
stayed within the repository's resource limits. It preserves an exact result
for every one of the 1,164 original catalogue branches.

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
The proof-backend benchmark and its negative search result are in
[research/pb_backend_benchmark.md](research/pb_backend_benchmark.md).
The bounded p=5 witness and encoding audit are in
[research/p5_validation.md](research/p5_validation.md).
The successive-q branch model and proof benchmark are in
[research/staged_uncompression.md](research/staged_uncompression.md).
The complete small-case first-stage derivation and enumeration are in
[research/intermediate_stage.md](research/intermediate_stage.md).
The exact p=5 branch ranking and bounded second-stage portfolio are in
[research/p5_branch_portfolio.md](research/p5_branch_portfolio.md).
The p=37 first-stage model and sufficient projected PAF key are derived in
[research/projected_uncompression.md](research/projected_uncompression.md).
The canonicalization proof, bounded scaling results, and next solver decision
are in [research/intermediate_scaling.md](research/intermediate_scaling.md).
The implemented ternary model, exact join, and saved p=7 branch are described
in [research/ternary_phase.md](research/ternary_phase.md).
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
