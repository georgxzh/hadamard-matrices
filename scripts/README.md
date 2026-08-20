# Reproduction scripts

Each research experiment will receive a deterministic entry point here with
its configuration, seed, resource estimate, and expected output hashes.

`reproduce_h428.py` deterministically reconstructs the published order-428
matrix from source sequences, checks every intermediate exact invariant, and
runs both final matrix verifiers. Invoke it from the repository root:

```powershell
python -m scripts.reproduce_h428
```

`reproduce_legendre_examples.py` reproduces the published LP(3), LP(5), LP(7),
and LP(27) source pairs and dual-verifies H(8), H(12), H(16), and H(56).

```powershell
python -m scripts.reproduce_legendre_examples
```

`reproduce_pq2_uncompression.py` derives the structured `pq^2` compressed pairs
from the quadratic-character formula, certifies every exact necessary condition
for `p in {3,5,7,11,13,37}` at `q=3` and `p in {5,7}` at `q=5`, then exhaustively
uncompresses the `p=3, q=3` case and dual-verifies the resulting H(56). It scans
1,778,112 candidates on one core in under ten seconds.

```powershell
python -m scripts.reproduce_pq2_uncompression
```

`build_uncompression_opb.py` writes the tracked LP(27) reference OPB,
validates all 7,614 canonical p=3 matches against it, and streams the LP(333)
model to ignored scratch storage solely to record exact structural counts,
byte size, and SHA-256. It does not invoke a solver.

```powershell
python -m scripts.build_uncompression_opb
```

No open-search script targeting order 668 is present. Direct enumeration at
`p=37, q=3` would require about `2.4e71` candidates per row; see
`research/pq2_derivation.md`.
