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
byte size, and SHA-256. It also builds the translation-canonical variants,
normalizes every p=3 match, and verifies the exact factor-81 ordered-pair
reduction. It does not invoke a solver.

```powershell
python -m scripts.build_uncompression_opb
```

`benchmark_pb_backend.py` validates the complete LP(27) certificate pipeline
with RoundingSat and VeriPB, then runs short one-core proof-logging probes on
both unfixed models. It never runs LP(333).

```powershell
python -m scripts.benchmark_pb_backend --solver path\to\roundingsat.exe --verifier path\to\veripb.exe --probe-seconds 10
```

`validate_p5_uncompression.py` reproduces the published structured LP(45),
checks its two successive 3-compressions, validates both p=5 OPB models with
VeriPB, and dual-verifies the resulting H(92). It supplies the known witness;
it does not run an open search.

```powershell
python -m scripts.validate_p5_uncompression --verifier path\to\veripb.exe
```

`benchmark_staged_uncompression.py` validates fixed length-`3p` intermediate
branches at p=3 and p=5, then runs bounded proof-producing searches over the
final binary rows. It never builds or solves LP(333).

```powershell
python -m scripts.benchmark_staged_uncompression --solver path\to\roundingsat.exe --verifier path\to\veripb.exe --search-seconds 10
```

`build_intermediate_stage.py` exhaustively generates the first-stage
length-`3p` intermediate pairs at p=3 and p=5, writes the independent exact
OPB formulation, and checks known-branch certificates with VeriPB. It uses one
core and never builds or solves LP(333).

```powershell
python -m scripts.build_intermediate_stage --verifier path\to\veripb.exe
```

`benchmark_p5_branch_portfolio.py` reduces all 10,476 p=5 intermediate pairs
to their 1,164 independent-translation orbits, ranks them by exact binary-row
scan cost, and exhaustively searches the first three branches. It also emits a
VeriPB-checked SAT certificate and dual-verifies the recovered H(92).

```powershell
python -m scripts.benchmark_p5_branch_portfolio --verifier path\to\veripb.exe --portfolio-size 3
```

`build_projected_uncompression.py` writes the non-enumerative p=37
first-stage OPB to ignored scratch storage, validates the sufficient
factor-three projected PAF key at p=3 and p=5, checks a projected p=5 SAT
certificate, and runs a bounded solver probe. It never solves an LP(333)
model.

```powershell
python -m scripts.build_projected_uncompression --solver path\to\roundingsat.exe --verifier path\to\veripb.exe --probe-seconds 10
```

No open-search script targeting order 668 is present. Direct enumeration at
`p=37, q=3` would require about `2.4e71` candidates per row; see
`research/pq2_derivation.md`.
