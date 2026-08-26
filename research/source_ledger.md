# Source ledger

Last audited: 2026-08-20

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
| `kotsireas2025compression` | P | metadata | newer compression properties | full-text audit pending |
| `cati2024database` | PP/software | arXiv and Sage docs | construction coverage/database | executable audit pending |
| `eliahou2025modular` | P | open PDF text | modular near-result at 668 | pending |
| `chojecki2026status` | R | full PDF indexed | previous computational approach | claims not reproduced |
| `ramos2026multipliers` | PP | complete arXiv v1 HTML and metadata | paper's 21/30 common-multiplier exclusions | scope and formulas audited; paired artifact below |
| `ramos2026artifacts` | PP/software | current public repository at commit `691398b`; v1.0.0 release and checksum | post-v1 25/30 classification and proof-carrying evidence | 15 exclusions locally rerun; archive hash verified; ten full proof cases not rerun |
| `veripb2026` | S/software | official repository and proof-format documentation | OPB compatibility and certificate policy | format audited; solver/checker not yet installed or benchmarked |
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

- The original structured LP(27), LP(45), LP(63), and LP(75) publisher figure
  remains inaccessible, but this no longer blocks the project: the prescribed
  compressed rows were independently derived and proved in
  `pq2_derivation.md`.
- Extract and run the full `ramos2026artifacts` DRAT/MITM bundle only after its
  expanded storage and verifier runtime are bounded or separately approved.
- Locate code and complete outputs underlying `chojecki2026status`.
- Check SageMath's exact reason/dispatch trace for nonconstruction at 668.
- Search citation indexes again before any major experiment or public claim.

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
