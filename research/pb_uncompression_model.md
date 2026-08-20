# Exact pseudo-Boolean uncompression model

Status: implemented and validated 2026-08-20. This is a model-construction
milestone, not an LP(333) search and not an order-668 result.

## 1. Variables and conventions

Let the prescribed compressed rows have length `d`, compression factor `m`,
and uncompressed length `L=dm`. Sequence positions and residue classes are
zero-based. For each row, `x_i=1` exactly when the sign at position `i` is
`-1`.

For each row, shift `s=1,...,floor(L/2)`, and position `i`, an auxiliary
variable `z_(s,i)` is constrained to equal

```text
x_i XOR x_((i+s) mod L).
```

The four exact binary inequalities are

```text
 x_i + x_j - z >=  0
-x_i - x_j - z >= -2
 x_i - x_j + z >=  0
-x_i + x_j + z >=  0.
```

They are the four facets of the binary XOR relation. No floating-point
quantity occurs.

## 2. Exact constraints

If a compressed entry is `C_r`, its residue class must contain exactly

```text
(m-C_r)/2
```

negative signs. This gives one cardinality equality for every residue class
of each row.

At shift `s`, let `D_A(s)` and `D_B(s)` be the sums of the corresponding XOR
variables. Since `PAF_X(s)=L-2D_X(s)`, the Legendre equation

```text
PAF_A(s) + PAF_B(s) = -2
```

is exactly equivalent to

```text
D_A(s) + D_B(s) = L+1.
```

Only shifts through `floor(L/2)` are needed because periodic
autocorrelation is symmetric under `s -> L-s`.

**Soundness.** Any satisfying assignment gives two binary rows with exactly
the prescribed residue-class sums and combined PAF `-2` at every nonzero
shift, hence a binary Legendre pair above the prescribed compression.

**Completeness.** Any such Legendre pair determines the base variables and
uniquely determines every XOR auxiliary, satisfying every model record.

The implementation is `src/pb_model.py`; the deterministic builder is
`scripts/build_uncompression_opb.py`.

## 3. Exact model sizes

| quantity | LP(27), `d=3,m=9` | LP(333), `d=37,m=9` |
|---|---:|---:|
| base variables | 54 | 666 |
| XOR variables | 702 | 110,556 |
| total variables | 756 | 111,222 |
| XOR inequalities | 2,808 | 442,224 |
| compression equalities | 6 | 74 |
| correlation equalities | 13 | 166 |
| OPB constraint records | 2,827 | 442,464 |
| inequalities after splitting equalities | 2,846 | 442,704 |

The generated LP(333) OPB is exactly 15,681,010 bytes (14.955 MiB), SHA-256
`60d5eb303c36fb1dee95e40ffb82b858a64c737c704be18e59d0764726f23405`.
It is reproducible scratch output under `tmp/pb_models/`, not a tracked
15-MiB source artifact. The compact tracked LP(27) model has SHA-256
`3fa0c938127f82f1c977a8a01f2d1b281b68b288b923e230e46d8c5200dad1d7`.

The 442,224 XOR inequalities translate directly to 442,224 ternary CNF
clauses. A total CNF clause count is deliberately not asserted: it depends on
the chosen encodings for 74 compression and 166 long correlation equalities.
The exact OPB input size is likewise not a solver-memory forecast.

## 4. Exhaustive small-case validation

The factor-nine p=3 enumerator scans all 889,056 preimages on each side. It
stores one representative per second-row PAF signature and finds 7,614 first
rows whose complementary signature is present. These 7,614 **canonical
matches** were all materialized and checked against all 2,827 OPB records.
Every one passed. Including signature multiplicities, the same exhaustive
enumeration represents exactly 77,274 ordered Legendre pairs.

The distinction corrects earlier wording that called 7,614 the total number
of binary pairs. It is a canonical-match count; 77,274 is the exact ordered
pair count for this fixed compressed class.

The recorded one-core run took 21.88 seconds: 8.50 seconds for exhaustive
enumeration, 11.92 seconds for all model checks, and 1.41 seconds to stream the
LP(333) model. Full metadata and a satisfying LP(27) base assignment are under
`results/pb_uncompression/`.

## 5. Certificate and search policy

No symmetry break is present. This unbroken model is the reference against
which any later optimized model must be proved equisatisfiable.

For a satisfiable result, retain the solver assignment and check the two base
rows with the independent exact Legendre/SDS/PSD pipeline before constructing
and dual-verifying H(668). For an unsatisfiable result, require the exact OPB
hash and a proof accepted by VeriPB, whose official documentation identifies
OPB as its standard input and supports SAT/UNSAT certificates
`veripb2026`. A solver status line without a checked proof is not accepted.

No LP(333) solver run is authorized by this milestone. Backend selection,
proof logging, solver-memory measurement, and any proved symmetry constraints
must be completed before requesting approval for a bounded run.
