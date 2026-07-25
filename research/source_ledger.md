# Source ledger

Last audited: 2026-07-25

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
| `fletcher2001` | P | metadata/open access link | LP(\(L\)) → HM(\(2L+2\)) | derivation pending |
| `georgiou2002` | P | repository metadata/abstract | multipliers and SDS formulation | pending |
| `djokovic2015compression` | P | arXiv abstract | exact compression identities | implementation pending |
| `kotsireas2021mod3` | P | arXiv abstract | length divisible by 3 constraints | pending |
| `kotsireas2027pq2` | P, online 2026 | substantial publisher text | structured \(pq^2\) uncompression route | small cases pending |
| `kotsireas2025compression` | P | metadata | newer compression properties | full-text audit pending |
| `cati2024database` | PP/software | arXiv and Sage docs | construction coverage/database | executable audit pending |
| `eliahou2025modular` | P | open PDF text | modular near-result at 668 | pending |
| `chojecki2026status` | R | full PDF indexed | previous computational approach | claims not reproduced |
| `ramos2026multipliers` | PP | arXiv abstract and HTML | latest exact common-multiplier obstruction | analytic/certificate audit pending |
| `djokovic2009sds` | P/PP | arXiv abstract | SDS and Williamson alternatives | pending |
| `djokovic2018gs` | P/PP | arXiv abstract | GS difference-family constraints | pending |
| `deLauneyFlannery2000` | P | publisher abstract | cocyclic/RDS equivalence | pending |

## Current-open-status audit

Evidence checked on 2026-07-25:

1. Epoch AI currently labels the order-668 task “Unsolved.”
2. The 2024 construction database covers known constructions through 1208
   and does not supply order 668.
3. Eliahou's 2025 result is explicitly only modulo 64.
4. Kotsireas et al.'s online-2026 \(pq^2\) paper treats the \(p=37,q=3\)
   row as a conjectural route/future case, not a constructed LP(333).
5. Ramos–Hulak–de Queiroz, submitted 2026-07-22, explicitly state that their
   common-multiplier restrictions leave unrestricted LP(333) and HM(668)
   open.

**Conclusion:** order 668 remains open in the current sources audited. This is
a literature-status conclusion, not a mathematical nonexistence theorem.

## Order-428 source artifact

The author-hosted `kharaghani2005` PDF was accessed on 2026-07-25 at
<https://www.cs.uleth.ca/~hadi/research/h428.pdf>. Its SHA-256 is
`1d6d5c0cf25d16db9e451b016ab2724fe974b079fe6c9a4f5d7a43967c855bd2`.
The audited copy is research input and is not redistributed in this
repository. The exact transcription and complete audit are in
`order428_reproduction.md`.

## Retrieval gaps

- Retrieve and inspect the proof/certificate artifacts for
  `ramos2026multipliers`.
- Locate code and complete outputs underlying `chojecki2026status`.
- Check SageMath's exact reason/dispatch trace for nonconstruction at 668.
- Search citation indexes again before any major experiment or public claim.

## Citation discipline

Every substantive research note must cite a key present in the BibTeX file.
When a statement was seen only in an abstract, that limitation is stated.
Computational claims enter this ledger only with configuration, code commit,
complete output, and an exact checker.
