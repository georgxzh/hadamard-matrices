# Source ledger

Last audited: 2026-10-06

Labels:

- **P** — peer-reviewed primary mathematical source
- **PP** — primary preprint, not yet peer reviewed
- **S** — secondary/database/documentation source
- **R** — exploratory or status report

| Key | Type | Access checked | Exact use in this project | Reproduction state |
|---|---:|---:|---|---|
| `hadamard1893` | P | metadata | original determinant problem/background | not required |
| `sylvester1867` | P | metadata | doubling construction | reproduced in tests |
| `paley1933` | P | metadata | quadratic-residue construction | prime cases reproduced |
| `epoch2026` | S | full web page | benchmark statement and current label | checked 2026-07-25 |
| `kharaghani2005` | P | all 7 pages of author PDF; formulas and sequences visually audited | order-428 warm-up | reproduced; dual exact verification |
| `best2013turyn` | P | author PDF and arXiv record | independent TT definition/classification context | TT(36) implication checked |
| `sagemath_tsequences` | S/software | current source and documentation | independent sequence-encoding/formula cross-check | decoded TT(36) agrees |
| `fletcher2001` | P | all 12 pages of open PDF; Theorem 3 array and Table 4 visually audited | LP(\(L\)) to HM(\(2L+2\)); small source pairs | implemented; LP(3,5,7,27) and H(8,12,16,56) dual-verified |
| `georgiou2002` | P | repository metadata/abstract | multipliers and SDS formulation | pending |
| `djokovic2015compression` | P | complete arXiv PDF; Definition 3 and Theorem 3 visually audited | exact compression identities | generic and 3/9/37 paths implemented and tested |
| `kotsireas2021mod3` | P | complete arXiv PDF; Corollary 1 visually audited | length divisible by 3 exact PSD constraints | implemented; LP(27) special frequency reproduced |
| `kotsireas2027pq2` | P, online 2026 | substantial publisher text; direct PDF blocked | structured \(pq^2\) uncompression route | route cited only; compressed rows independently **derived and proved**, not retrieved; factor-9 uncompression reproduced at \(p=3\) |
| `kotsireas2025compression` | P | publisher HTML, especially Sections 4 and 5.3.2; direct PDF blocked | successive uncompression scheme and printed structured LP(45) | LP(45), both compression stages, exact first-stage models, exhaustive p=3/p=5 intermediate generation, p=5 branch portfolio, certificates, and H(92) reproductions completed |
| `lebedev2026quaternary` | PP | arXiv abstract and metadata | contemporary methodological context for exact autocorrelation-vector matching and divisor-chain compression | context only; quaternary results not used as binary evidence |
| `cati2024database` | PP/software | arXiv and Sage docs | construction coverage/database | executable audit pending |
| `eliahou2025modular` | P | open PDF text | modular near-result at 668 | pending |
| `chojecki2026status` | R | full PDF indexed | previous computational approach | claims not reproduced |
| `ramos2026multipliers` | PP | complete arXiv v1 HTML and metadata | paper's 21/30 common-multiplier exclusions | scope and formulas audited; paired artifact below |
| `ramos2026artifacts` | PP/software | current public repository at commit `691398b`; v1.0.0 release and checksum | post-v1 25/30 classification and proof-carrying evidence | 15 exclusions locally rerun; archive hash verified; ten full proof cases not rerun |
| `koops2025prooflogging` | P/software | complete open HTML and official metadata | RoundingSat/VeriPB certified PB workflow | toolchain reproduced on LP(27) |
| `roundingsat2026` | S/software | official repository, current source, README, and Windows binary | proof-producing PB backend | fixed-witness proofs verified; bounded open probes timed out |
| `veripb2026` | S/software | official 3.0.2 tagged source and documentation | OPB SAT-certificate verification | built locally; four LP(27) certificates accepted |
| `djokovic2009sds` | P/PP | arXiv abstract | SDS and Williamson alternatives | pending |
| `djokovic2018gs` | P/PP | arXiv abstract | GS difference-family constraints | pending |
| `deLauneyFlannery2000` | P | publisher abstract | cocyclic/RDS equivalence | pending |

## Current-open-status audit

Evidence checked on 2026-08-20:

1. Epoch AI currently labels the order-668 task “Unsolved.”
2. The 2024 construction database covers known constructions through 1208
   and does not supply order 668.
3. Eliahou's 2025 result is explicitly only modulo 64.
4. Kotsireas et al.'s online-2026 \(pq^2\) paper treats the \(p=37,q=3\)
   row as a conjectural route/future case, not a constructed LP(333).
5. Ramos–Hulak–de Queiroz, submitted 2026-07-22, explicitly state that their
   common-multiplier restrictions leave unrestricted LP(333) and HM(668)
   open. The audited post-v1 artifact strengthens the fixed-symmetry
   classification to 25/30 without changing that strict scope.

**Conclusion:** order 668 remains open in the current sources audited. This is
a literature-status conclusion, not a mathematical nonexistence theorem.

## Order-428 source artifact

The author-hosted `kharaghani2005` PDF was accessed on 2026-07-25 at
<https://www.cs.uleth.ca/~hadi/research/h428.pdf>. Its SHA-256 is
`1d6d5c0cf25d16db9e451b016ab2724fe974b079fe6c9a4f5d7a43967c855bd2`.
The audited copy is research input and is not redistributed in this
repository. The exact transcription and complete audit are in
`order428_reproduction.md`.

## Legendre source artifacts

The following full-text research inputs were accessed on 2026-07-25 and are
not redistributed in the repository:

- `fletcher2001`: open journal PDF, SHA-256
  `4d0bc39f392a24dfb0bec3a0f17961eab4dfffe85956a1204016110d029c82b5`;
- `djokovic2015compression`: arXiv PDF, SHA-256
  `a05f33d2d901e70440e17acb2a21988ab07ccda52b31dbc3398546a32a69bffb`;
- `kotsireas2021mod3`: arXiv PDF, SHA-256
  `4e9cc7adcdb9f57cdf16b53a511ebafac63f780bacbe05b5ea9cf73a52648f5`.

The exact derivation, indexing conventions, formula-page audit, Table-4
transcriptions, and redundant LP(27) glyph checks are in
`legendre_framework.md`. Reproduction artifacts and both independent verifier
reports are under `results/legendre_examples/`.

## Retrieval gaps

- The structured LP(45) rows are now recovered from the publisher HTML for
  `kotsireas2025compression`. The dynamic figures/direct PDF for the later
  `kotsireas2027pq2` article remain inaccessible; this does not block the
  independently proved prescribed rows in `pq2_derivation.md`.
- Extract and run the full `ramos2026artifacts` DRAT/MITM bundle only after its
  expanded storage and verifier runtime are bounded or separately approved.
- Locate code and complete outputs underlying `chojecki2026status`.
- Check SageMath's exact reason/dispatch trace for nonconstruction at 668.
- Search citation indexes again before any major experiment or public claim.
- Relevant full-text sections 4, 5 and 8 of `lebedev2026quaternary` were
  audited on 2026-09-29 UTC for correlation-vector joins, divisor chains and
  evidence levels. Its quaternary Gray map differs from our ternary traversal.
  This supplies methodological precedent, not a binary LP(333) result.

## Citation discipline

Every substantive research note must cite a key present in the BibTeX file.
When a statement was seen only in an abstract, that limitation is stated.
Computational claims enter this ledger only with configuration, code commit,
complete output, and an exact checker.

## Common-multiplier artifact

The public repository was audited at commit
`691398b7634140269874a45024ed3041036cda9c` on 2026-08-20. Its current
machine-readable classification reports 25 impossible families and open IDs
`0,1,3,4,5`. Local exact reruns reproduced 15 exclusions. The v1.0.0 archive
has 198,965,505 bytes and verified SHA-256
`49cc367a1cee8da1e10d662c68150eb6ae9b66a0ad21d80b4594d3a0a0749957`.
It was not extracted or fully checked. Exact commands, per-certificate hashes,
post-v1 distinctions, and the ten-case gap are in
`multiplier_artifact_audit.md` and `results/multiplier_audit/metadata.json`.

## Paper-draft novelty audit, 2026-09-29 UTC

- `fletcher2001`: primary journal PDF, Section 5.4/Table 3 checked again.
  Exhaustive length-45 classification already reported (3,058 inequivalent
  pairs). Our fixed-compression ordered census uses different conventions;
  conversion to the complete old representative list is still missing.
- `djokovic2015compression`: primary arXiv HTML, Theorem 3 and Section 6.
  Exact compression identities and symmetry search are established.
- `kotsireas2025compression`: indexed primary publisher text, Theorem 3.2,
  equation (5), Section 4 and the printed small examples. The prescribed
  character pair and two q-lifts are established, independently reproduced
  here. The universal uncompression claim remains conjectural.
- `kotsireas2023mod5`: primary arXiv v3, Section 2/Tables 1--2. The
  `(1,3,3,3,3)` magnitude pattern is already listed at length 45, alongside
  other families. Our exact census is confined to one ordered prescription.
- `turner2022decimation`: publisher abstract/metadata only; full theory and
  its relation to our concrete gauge still need comparison.
- `perera2025fast`: publisher abstract/metadata only. The FFT-like search
  algorithm benchmarks lengths 45 and 63. Our implementation timings are
  not a comparison against this work and do not establish state-of-the-art.
- `kotsireas2027pq2`: primary abstract/metadata checked, full algorithm and
  tables still inaccessible. This is a material gap for any phase-formulation
  or restricted-census novelty claim.

The claim-by-claim ledger and proofs are in `../paper/manuscript.tex`.

### Propagation and equivalence follow-up, 2026-09-29 UTC

- `fletcher2001`, Section 5.4/Table 3: converted all 2,976 phase-gauged
  solutions in our subset to the published operations (row exchange,
  independent cyclic shifts/reversals, common decimation). The result is
  **63 classes**: 61 with 48 records and two with 24. This is a restricted
  subset conversion, not reproduction of the complete 3,058-class count.
  The underlying historical list, stated to be available from the authors,
  has not been retrieved or matched. No author contact was initiated.
- `kotsireas2025compression`, Section 4: its trace/linear-complexity discard
  invokes Conjecture 3.5. Our complete restricted census uses no such filter.
- `lumsden2025periodic`, primary arXiv v3 Sections 3.4--5:
  <https://arxiv.org/html/2408.15611v3>. Matching retains all combinations in
  equal-signature buckets; multilevel compression, recursive uncompression,
  and equivalence filtering are explicit precedents. The authors' software
  <https://github.com/tylerlumsden/GolayPair> documents a general PAF constant,
  including -2, but has not been run or benchmarked here. Our choice of exact
  PAF coordinates does not make the generic joining method novel.
- Phase-difference triangle supports, sum intervals, and partner-signature
  bitsets now have an exact implementation and soundness argument. The
  priority of this particular combination remains unresolved. A negative
  timing result cannot establish novelty or rule out other implementations.

Full-text gaps for `kotsireas2027pq2`, `perera2025fast`, and
`turner2022decimation` remain open. No first-method or new-length claim is made.

### Certified spectral milestone, 2026-10-04 UTC

- `fletcher2001`: primary journal PDF, Sections 5.1 and 5.3 reread:
  <https://ajc.maths.uq.edu.au/pdf/23/ocr-ajc-v23-p75.pdf>.
  Single-row PSD exclusion and filtering before matching are established.
- `lumsden2025periodic`: primary arXiv v3, Sections 2 and 3.4--5 reread:
  <https://arxiv.org/html/2408.15611v3>. PSD filtering, full matching buckets,
  recursive uncompression and equivalence reduction precede this work.
- `bright2019complexgolay`: full primary author text, Sections 3.3 and 3.5:
  <https://cs.uwaterloo.ca/~cbright/reports/jsc-cgolay.pdf>, author preprint
  <https://arxiv.org/abs/1907.11981>, DOI
  <https://doi.org/10.1016/j.jsc.2019.10.013>. Partial-correlation conflicts,
  FFT-based spectral exclusion with explicit numeric tolerance, precomputed
  contributions and frequency ordering are precedents. This is a complex
  aperiodic search; no periodic binary classification is inferred from it.

The proved rational rectangle specialization and complete saved-branch p=7
result are in `spectral_join.md`. Priority of that specialization is unresolved;
native engineering speed is not a new complexity result. The full-text gaps
listed above and historical LP(45) representative-list comparison remain.

### Systematic p=7 portfolio comparison, 2026-10-06

- `perera2025fast`: indexed primary publisher introduction and Section 3/4
  previews identify Bluestein/FFTW Fourier evaluation. Direct HTML returned
  403; complete factorization, numerical safeguards and search conventions
  remain inaccessible. The author-institution page links to DOI metadata,
  not an accessible full text. No code or comparative baseline was run.
- `kotsireas2027pq2`: indexed primary publisher abstract/metadata checked;
  direct HTML/PDF retrieval still failed despite the open-access label.
  Full phase/pruning/decimation details remain unaudited. Targeted repository
  and preprint searches did not recover complete primary manuscripts.
- `kotsireas2025compression`: primary Section 4.1 reread for successive
  lifting and the explicitly conjectural trace/linear-complexity discard.
  LP(63) existence is a prior result; its printed witness was not recovered
  or added as a positive portfolio control in this milestone.

The candidate-contribution ledger and access URLs are frozen in
`../results/p7_portfolio/literature_access.json`. Priority of the rational
partial-phase specialization and the restricted-census artifact remains
unresolved. The preferred paper scope is census/reproducibility with proved
specializations, contingent on completed evidence, full comparisons and
external replication; no new existence or competitive-method claim follows.
