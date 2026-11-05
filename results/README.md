# Results

This directory is reserved for frozen construction outputs and exact
verification packages.

`H428.csv` is the deterministic reconstruction of the published
Kharaghani--Tayfeh-Rezaie order-428 matrix. Its verification reports and
hashes are stored alongside it; the construction is documented in
`research/order428_reproduction.md`.

`legendre_examples/` holds H(8), H(12), H(16), and H(56) built from the
published Fletcher--Gysin--Seberry Table 4 pairs.

`pq2_uncompression/` holds a second, distinct H(56) obtained by exhaustively
uncompressing the derived structured pair `A(3,3), B(3,3)`. Its LP(27) lies in
a different compressed class from the Table 4 pair, so the two H(56) files have
different hashes. The derivation is documented in
`research/pq2_derivation.md`.

`pb_uncompression/` holds the compact exact LP(27) OPB, a satisfying base
assignment, and metadata for both the exhaustive small-case validation and the
deterministically generated LP(333) model. The 15-MiB LP(333) OPB is generated
under ignored `tmp/` rather than frozen here; its exact hash and size are in
metadata. The directory also freezes the translation-canonical LP(27) OPB;
the analogous LP(333) variant is reproducible scratch output. No solver search
was run at LP(333).

`pb_backend_benchmark/` freezes complete SAT certificates and verification
logs for both LP(27) models. It also records bounded open-search timeouts;
those incomplete scratch proofs are hashed in metadata but are not tracked.

`p5_validation/` freezes the published structured LP(45), its unbroken and
translation-canonical OPB models and verified SAT certificates, and the
dual-exactly-verified H(92). This is fixed-witness validation, not search.

`staged_uncompression/` freezes conditional factor-three branch models at
p=3 and p=5. Both p=3 open searches have VeriPB-checked SAT proofs and
independently checked solver rows; bounded p=5 searches timed out, with their
incomplete proofs retained only in ignored scratch storage.

`intermediate_stage/` freezes the exact first-stage OPB models, known-branch
SAT certificates, VeriPB transcripts, and exhaustive p=3/p=5 signature-join
counts. The published p=5 intermediate branch is recovered exactly.

`p5_branch_portfolio/` freezes all 1,164 translation-canonical p=5 branches,
the three-branch exhaustive benchmark, an LP(45) recovered independently of
the printed rows, its VeriPB-checked branch certificate, and a
dual-exactly-verified H(92).

`projected_uncompression/` freezes the projected p=5 OPB, exact witness and
VeriPB certificate, bounded solver transcript, and metadata for the
non-enumerative p=37 first-stage model. The 4.5-MB p=37 OPB and incomplete
p=5 solver proof remain reproducible ignored scratch artifacts.

`intermediate_scaling/` freezes the canonical first-stage models, exhaustive
p=3/p=5 orbit audit, eight independently checked solver witnesses with compact
VeriPB certificates, six p=7 first-stage timeout transcripts, and four p=5
binary-lift timeout transcripts. Metadata records the complete search-trace
hashes in ignored scratch storage and the same-branch exact-join baseline.

`ternary_phase/` freezes binary and phase OPB comparisons, exact phase-join
counts, compact VeriPB certificates, same-domain packed/incremental controls,
and a seeded p=7 intermediate branch with its exact certificate. Preliminary
p=7 PB acquisition timeouts are recorded separately in `p7_acquisition.json`.
All bounded p=5/p=7 lift probes timed out; the p=7 join hit its storage cap
before scanning partner rows. Binary liftability of that branch is unknown.



`multiplier_audit/` records the exact external commit, certificate hashes,
locally reproduced fixed-symmetry exclusions, release-archive checksum, and
the cases whose full DRAT/MITM evidence was not rerun.

`p5_classification/` contains the complete 1,164-branch prescribed p=5 lift
census: 704 SAT, 460 verified empty, none unresolved. It includes the pilot,
resource gate, 79 dual-enumerated symmetry representatives, explicit transfer
maps, all canonical binary solutions, per-branch CSV counts, an independent
audit, and a SHA-256 manifest. Empty results are exhaustive computational
evidence with stated trust assumptions, not standalone PB UNSAT proofs.

`phase_controls/` separates translation reduction, PAF updates and encoding
effects. The PB models use aligned gauges; p=5/p=7 probes remain timeouts.
`isolated_joins.json` preserves the separate three-repeat timing experiment
without concurrent repository computations. `audit.json` records 139 hashes,
35 byte-identical regenerated models and 19 reverified SAT proofs/certificates.

The standalone draft and its evidence manifest are in `../paper/`.

No order-668 candidate is present. A near miss, compressed object, modular
matrix, or heuristic optimum must not be named `H668.csv`.
