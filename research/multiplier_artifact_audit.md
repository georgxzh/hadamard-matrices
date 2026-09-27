# Length-333 common-multiplier artifact audit

Status: current repository and release audited 2026-08-20. Lightweight exact
claims partially reproduced; the full DRAT bundle was integrity-checked but
not executed. This concerns fixed common-multiplier symmetry only and does not
resolve unrestricted LP(333) or H(668).

## 1. Versioned sources

The paper `ramos2026multipliers` is arXiv v1, submitted 2026-07-22. It proves
that a common fixed multiplier group has order at most 6, classifies 30
mod-3-compatible subgroups, excludes 21 (all 19 of order at least 9), and
leaves nine groups of order at most 6 undecided.

The associated artifact `ramos2026artifacts` has continued after v1. The
audited public `main` commit is

```text
691398b7634140269874a45024ed3041036cda9c
```

dated 2026-08-10. Its machine-readable `master_status.json` has SHA-256
`5b2db85501dbb15b7c2eb73125cc9a88a034ac900d2b83019972efade54dcfe2`
and reports:

- 25 of 30 common-multiplier families impossible;
- open IDs `0,1,3,4,5`, of orders 1, 2, 3, 3, 3;
- no found family;
- every common-multiplier family of order at least 4 excluded.

This stronger 25/30 statement is a **post-v1 artifact result**, not a theorem
stated in arXiv v1. Current GitHub CI for the audited commit passed, but CI is
supporting evidence rather than a substitute for the local checks below.

## 2. Locally reproduced exact checks

The repository was shallow-cloned at the exact commit above. Python-only
checks used Python 3.14.6; the supplemental symbolic scripts used the source's
pinned NumPy 2.5.1 and SymPy 1.14.0 in an isolated scratch environment.

### Subgroup classification and elementary obstructions

- exact subgroup regeneration returned 30 subgroups in the order-108 mod-3
  kernel;
- full mod-37 reduction excluded IDs `25,26,27,29`;
- exact row-sum/mod-24 conditions excluded IDs `16,17,18,24`;
- the regenerated JSON and certificate files were byte-identical to Git
  (the external clone remained clean).

### Standalone analytic verifiers

- ID 12: analytic single-shift contradiction and an independent exhaustive
  compressed decision both passed; certificate SHA-256
  `c8dc8aefbc814026f3feacd6bdf30a94c3def307871e4fe51302e0e5887696fa`;
- generalized value-set 9-compression: IDs `6,8,12` passed exact exhaustive
  checks (2,428,992; 148,428; and 5,292 compressed sequences respectively);
- ID 2: shift-111 fibre obstruction passed, certificate SHA-256
  `2dd738d38804db6719b78b974837cbb9cad77e0be71600e7bc42788410910249`;
- ID 7: shift-111 orbit obstruction passed, certificate SHA-256
  `b8b5f9f44ffa945d949ae07afadcc79a73c8b46c83034dbe516c7dc5c9038597`;
- IDs 9 and 10: CRT mod-8 obstruction passed, certificate SHA-256
  `d2eedb8a1fb79f7a8d129b38fd255725609a045481f508dbb9437d329e2494f1`;
- the exact order-4 Hadamard positive control passed.

Together these local runs reproduce the exclusions of exactly 15 IDs:

```text
2, 6, 7, 8, 9, 10, 12, 16, 17, 18, 24, 25, 26, 27, 29.
```

### Supplemental compression theorem

All five symbolic/checking scripts passed. In particular they reproduced the
four L=333 full-image exclusions, the real-quadratic census of 139 forbidden
fixed-symmetry classes among 428 cases, the finite imaginary-quadratic census
of zero infeasible cases among 797, and all 44 numeric/attribution assertions.
These are fixed-symmetry results, not length nonexistence claims.

## 3. Release bundle and remaining gap

GitHub release `v1.0.0` and Zenodo DOI `10.5281/zenodo.21498698` identify the
proof archive

```text
proof-artifacts-v1.0.0.tar.zst
```

with size 198,965,505 bytes. The downloaded file exactly matched both the
release digest and checksum sidecar:

```text
49cc367a1cee8da1e10d662c68150eb6ae9b66a0ad21d80b4594d3a0a0749957
```

The archive was **not extracted and its DRAT proofs were not run**. The source
does not give a sufficiently tight expanded-storage and verifier-runtime bound
to establish in advance that the full check stays below this project's
10-GB/30-minute approval gate. Hash agreement proves artifact integrity, not
the mathematical verdicts inside.

The ten locally unreproduced exclusions are IDs

```text
11, 13, 14, 15, 19, 20, 21, 22, 23, 28.
```

They rely on the stored CP-SAT/proof-carrying or meet-in-the-middle records.
Their current artifact status was inspected, but their full enumerations and
proof traces were not independently rerun in this audit.

## 4. Strict interpretation

**Reproduced fact:** the 15 IDs listed above are excluded by locally rerun
exact arithmetic/census checks at the audited commit.

**Current artifact claim:** 25/30 are impossible and the five open families
have multiplier order at most 3.

**Not established by this audit:** that every archived DRAT proof passes a
fresh local checker, that the five open families contain a Legendre pair, or
that unrestricted LP(333) is impossible.

The current result makes a common fixed multiplier of order at least 4 a poor
search hypothesis, subject to the ten-case full-proof audit gap. It says
nothing about unrestricted pairs, different multiplier groups for the two
rows, or affine multiplier-plus-translation actions.

## 5. Commands executed

From an ignored scratch clone at the audited commit:

```powershell
python lp333\code\classify.py
python lp333\code\obstructions.py
python lp333\code\necessary_conditions.py
python lp333\id12_phase2\code\standalone_verifier.py
python lp333\id12_phase2\code\general_verifier.py
python lp333\id2_congruence_kernel\code\standalone_verifier.py
python lp333\id7_single_shift\code\standalone_verifier.py
python lp333\id9_id10_mod8\code\standalone_verifier.py
python scripts\verify_hadamard_csv.py --order 4 artifacts\hadamard4.csv
```

The five `compression_theorem/scripts/` Python entry points from its
`run_all.sh` were executed with Python 3.14.6, NumPy 2.5.1, and SymPy 1.14.0:
`verify_core.py`, `norm_form_obstruction.py`, `l333_consequences.py`,
`families.py`, and `check_note_claims.py`.

Release integrity was checked with:

```powershell
gh release download v1.0.0 --repo Arthur742Ramos/hadamard-668-multiplier-obstructions --pattern 'proof-artifacts-v1.0.0.tar.zst*'
Get-FileHash -Algorithm SHA256 proof-artifacts-v1.0.0.tar.zst
```
