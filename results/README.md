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
metadata. No solver search was run.

`multiplier_audit/` records the exact external commit, certificate hashes,
locally reproduced fixed-symmetry exclusions, release-archive checksum, and
the cases whose full DRAT/MITM evidence was not rerun.

No order-668 candidate is present. A near miss, compressed object, modular
matrix, or heuristic optimum must not be named `H668.csv`.
