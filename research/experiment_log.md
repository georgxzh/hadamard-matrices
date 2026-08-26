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

## EXP-PQ2-001: derived pq^2 pair and exhaustive factor-9 uncompression at p=3

- Status: derivation plus exhaustive enumeration; PASS
- UTC start and end: started 2026-07-26T02:29:34.572335Z, completed 8.559629
  seconds later
- Objective: remove the `kotsireas2027pq2` retrieval gap by deriving the
  prescribed compressed rows from the quadratic-character formula, prove their
  compressed-Legendre property, and exhaustively uncompress the smallest case
- Mathematical constraints: entry range and parity for factor `q^2`; both row
  sums `+1`; all `p` combined compressed PAF constants; all nonzero compressed
  PSD sums in exact cyclotomic arithmetic; Jacobsthal sum `-1` at every nonzero
  shift; all-shift PAF, SDS, and PSD checks on the recovered length-27 pair;
  complete H(56) Gram identities
- Primary sources: none required for the sequences. The rows are derived, not
  transcribed; `kotsireas2027pq2` is cited for the route only. Its embedded
  data remain unretrieved and are no longer needed.
- Configuration file: none; rows generated by
  `src.legendre.structured_compressed_pair`
- Random seed: not applicable; deterministic exhaustive enumeration
- Git commit: working tree on branch `agent/order-428-reproduction`; final
  commit recorded by repository history
- Hardware and software: Windows 11, AMD64 Family 25 Model 117, Python 3.14.6
- CPU cores / peak memory / storage: one core / not instrumented, one PAF-vector
  table of 88,821 entries / small CSV and text package under
  `results/pq2_uncompression`
- Complete output: `results/pq2_uncompression/metadata.json`, `H56.csv`, and
  both verifier reports and sidecars
- Exact checker: `src.legendre`, `src.uncompress`, `src.verify_matrix`, and the
  separately parsed, bit-packed `src.verify_matrix_independent`. The bit-packed
  PAF fast path is never trusted alone; every reported pair is re-checked with
  `check_legendre_pair`.
- Result: the derived pair passes every exact condition for
  `p in {3,5,7,11,13,37}` with `q=3` and `p in {5,7}` with `q=5`. At `p=3,q=3`,
  both 889,056-candidate sides were enumerated in full. There are 7,614
  canonical matching first rows and 77,274 ordered Legendre pairs after
  including second-signature multiplicity. The resulting
  H(56) is PASS/PASS with SHA-256
  `19b53864d3428d934d3330ca0a328c29c9b57f9e447268f575930fee777d896a`.
- Interpretation: the structured uncompression mechanism is reproduced from
  independently derived sequences. The recovered LP(27) is distinct from the
  Fletcher--Gysin--Seberry Table 4 pair, which lies in a different compressed
  class; the two H(56) artifacts differ (published-route SHA-256
  `53369c062e6dd6ef5f9b9039e2e4106b221d24958464f92f42d7278e293c29ab`). The
  derived `A(37,3),B(37,3)` independently reproduce the previously tabulated
  length-333 constants 650 and -18.
- Limitations / failed cases: no LP(333) and no order-668 result is claimed.
  Only `p=3` was enumerated. Direct enumeration at `p=37,q=3` requires about
  `2.4e71` candidates per row and is impossible; `p=5` at `6.3e9` already
  exceeds the approval gate and was not run. Satisfying every compressed
  necessary condition does not imply a binary uncompression exists.
- Reproduction command: `python -m scripts.reproduce_pq2_uncompression`

## EXP-PB-001: exact OPB uncompression model and exhaustive small-case check

- Status: exact model construction and validation; PASS
- UTC start and end: 2026-08-20T18:16:04.781103Z; completed 21.880116 seconds
  later
- Objective: encode binary uncompression of the structured compressed pair as
  exact pseudo-Boolean constraints and measure the LP(333) reference input
- Mathematical constraints: every residue-class cardinality; exact XOR at
  every position and nonredundant shift; combined disagreement count `L+1`,
  equivalent to combined PAF `-2`
- Configuration file: none; deterministic `A(p,3),B(p,3)` for p=3 and p=37
- Random seed: not applicable
- Git commit: working tree on branch `agent/order-428-reproduction`; final
  commit recorded by repository history
- Hardware and software: Windows 11, AMD64 Family 25 Model 117, Python 3.14.6
- CPU cores / peak memory / storage: one core / not instrumented / LP(333)
  scratch OPB 15,681,010 bytes
- Complete output: `results/pb_uncompression/metadata.json`, tracked LP(27)
  OPB, and exact satisfying base witness; LP(333) OPB is reproducible ignored
  scratch output with hash recorded in metadata
- Exact checker: `src.pb_model.PBConstraint.satisfied_by`, independently fed
  the canonical pairs produced by `src.uncompress`
- Result: all 7,614 canonical p=3 matches satisfy all 2,827 model records;
  those matches represent 77,274 ordered pairs. LP(333) has 111,222 variables,
  442,464 OPB records, size 15,681,010 bytes, and SHA-256
  `60d5eb303c36fb1dee95e40ffb82b858a64c737c704be18e59d0764726f23405`.
- Interpretation: the prescribed length-333 uncompression problem now has a
  deterministic, sound, complete, proof-oriented exact reference encoding
- Limitations / failed cases: no solver was run; no LP(333) or H(668) is
  claimed; solver memory and clauses for long equalities are backend-dependent;
  this experiment's reference model is deliberately unbroken
- Reproduction command: `python -m scripts.build_uncompression_opb`

## EXP-SYM-001: free translation canonicalization

- Status: exact derivation and exhaustive small-case validation; PASS
- UTC start and end: started 2026-08-26T02:50:15.508795Z; completed 60.989648
  seconds later
- Objective: remove the independent translations by multiples of the
  compressed length without excluding any prescribed Legendre pair
- Mathematical constraints: translations preserve every compression class
  and each row's PAF; residue-zero negative-bit words are constrained to their
  least cyclic rotation by exact binary positional inequalities
- Configuration: factor nine, compressed lengths 3 and 37; no random choices
- Random seed: not applicable
- Git commit: working tree on branch `agent/order-428-reproduction`; final
  commit recorded by repository history
- Hardware and software: Windows 11, AMD64 Family 25 Model 117, Python 3.14.6
- CPU cores / peak memory / storage: one core / not instrumented / canonical
  LP(333) scratch OPB 15,682,450 bytes
- Complete output: `results/pb_uncompression/metadata.json`, tracked canonical
  LP(27) OPB, and reproducible ignored LP(333) canonical OPB
- Exact checker: all generated constraints evaluated by `src.pb_model`; PAF,
  compression, reversal, and multiplier actions independently checked in
  `tests/test_symmetry.py`
- Result: 16 inequalities and no variables added; all 7,614 canonical p=3
  matches normalize to satisfying assignments; 77,274 ordered pairs split
  into exactly 954 free translation orbits of size 81. Canonical LP(333)
  SHA-256 is
  `b59bf0499931c3d751e41a15cd59631da86ab0e3b2dbd2718b016693fe680cea`.
- Interpretation: the prescribed LP(333) search now has a proved
  equisatisfiable translation-canonical model
- Limitations / failed cases: reversal and common multiplier actions are
  proved but not encoded because their interaction requires a separate
  canonicalization proof; no solver was run and no H(668) is claimed
- Reproduction command: `python -m scripts.build_uncompression_opb`

## EXP-MULT-001: current common-multiplier artifact audit

- Status: partial independent reproduction; PASS for the stated 15-family
  subset, full 25-family claim not completely rerun
- UTC start and end: 2026-08-20; exact start/end timestamps were not captured
- Objective: audit the current primary artifact behind
  `ramos2026multipliers`, reproduce its lightweight exact obstructions, and
  establish the remaining proof gap
- Mathematical constraints: subgroup classification in the mod-3 kernel;
  mod-37 full-image obstruction; row-sum congruences; value-set
  9-compression; shift-111 fibre/orbit bounds; CRT mod-8 obstruction
- Configuration: external public commit
  `691398b7634140269874a45024ed3041036cda9c`; release v1.0.0
- Random seed: not applicable; all rerun checks deterministic
- Git commit: working tree on branch `agent/order-428-reproduction`; final
  commit recorded by repository history
- Hardware and software: Windows 11; Python 3.14.6; NumPy 2.5.1; SymPy 1.14.0
- CPU cores / peak memory / storage: at most three cores / not instrumented /
  145,723,878-byte scratch clone+environment plus 198,965,602-byte release
  download and checksum sidecar
- Complete output: `results/multiplier_audit/metadata.json`; detailed commands,
  hashes, claims, and limitations in `multiplier_artifact_audit.md`
- Exact checker: source repository's standalone arithmetic verifiers,
  regenerated classification/necessary-condition scripts, and supplemental
  symbolic claim checkers
- Result: locally reproduced impossible IDs
  `2,6,7,8,9,10,12,16,17,18,24,25,26,27,29`; current artifact reports 25/30
  impossible and open IDs `0,1,3,4,5`
- Release integrity: 198,965,505-byte proof archive SHA-256 verified as
  `49cc367a1cee8da1e10d662c68150eb6ae9b66a0ad21d80b4594d3a0a0749957`
- Interpretation: common multiplier order at least four is excluded by the
  current artifact classification, but only 15 exclusions were independently
  rerun here
- Limitations / failed cases: archive not extracted; DRAT/MITM/CP-SAT evidence
  for IDs `11,13,14,15,19,20,21,22,23,28` not locally rerun because expanded
  storage and verifier runtime were not bounded tightly enough in advance;
  no conclusion about unrestricted LP(333) or H(668)
- Reproduction commands: enumerated in `multiplier_artifact_audit.md`; all
  executed against the exact external commit above

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
