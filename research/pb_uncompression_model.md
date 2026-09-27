# Exact pseudo-Boolean uncompression model

Status: implemented and validated 2026-08-20; proof-compatible header audited
2026-09-27. This is a model-construction milestone, not an LP(333) search and
not an order-668 result.

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

The generated LP(333) OPB is exactly 15,681,033 bytes (14.955 MiB), SHA-256
`2c1fab74f89ac9d19ed01d8380732049d8f22d0f72d7d5446249ddfacb9915f7`.
It is reproducible scratch output under `tmp/pb_models/`, not a tracked
15-MiB source artifact. The compact tracked LP(27) model has SHA-256
`071752e9e5d2f5ff9f7f669d8dd03bfc6d9452ced13a930cc24f39ad1fd92a08`.
These hashes include the proof-compatible `#equal` and `intsize` header
fields required by the current RoundingSat proof logger.

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

### Fixed-witness p=5 validation

The structured LP(45) printed in `kotsireas2025compression` supplies an
independent larger regression case. Its known witness passes all 7,952
unbroken records; after independent row-translation normalization it passes
all 7,968 canonical records. Complete assignments for both 2,070-variable
models are accepted by VeriPB 3.0.2. This is not an open search: a row still
has 6,273,179,136 possible preimages of the prescribed compression.

At p=5, 1,980 of 2,070 variables and 7,920 of 7,952 records belong to the XOR
layer. Exhaustive binary truth tables confirm that the four inequalities for
each local XOR are exact and individually irredundant. The next encoding
experiment therefore follows the source's two successive q-uncompressions
rather than deleting a facet. See `p5_validation.md`.

## 5. Proved coordinate symmetries

Let `T_k x` denote translation by `k*d` positions. For each row separately,

```text
PAF_(T_k x)(s) = PAF_x(s)
```

by reindexing the PAF sum. Translation by `k*d` also permutes the `m`
positions within every compression residue class, so it leaves every
compressed entry unchanged. The two rows may therefore be translated
independently, giving an exact `C_m x C_m` action on prescribed
uncompressions.

For each row, form the factor-length negative-sign bit word in residue class
zero. The translation-canonical OPB requires this word to be no greater than
any cyclic rotation, using binary positional weights. At factor nine this
adds eight inequalities per row and no variables.

For the structured rows, compressed entry zero is `1`, so the nine-position
word has exactly four negative bits. A word of length nine with period one or
three has a number of negative bits divisible by nine or three. Four is
neither, so the word has full period nine. Thus each row action is free and
the ordered-pair search space is reduced by exactly `9*9=81`.

The canonical LP(333) variant has 111,222 variables and 442,480 OPB records.
Its deterministic scratch artifact is 15,682,473 bytes, SHA-256
`d8276301c0182363f8a798c5ccdcfa661fdbf48824b968ebd5a7264d2260ec15`.
The canonical constraints are unchanged; only the proof-compatible header
changes this artifact's historical hash.

Three additional actions are proved and tested but not yet encoded:

1. independent reversal of either row, because `p=37` has
   `chi(-1)=1`, each prescribed compressed row is reversal-invariant, and a
   row's PAF is unchanged by reversal;
2. a common coordinate multiplier `h` with `chi(h mod 37)=1`, which preserves
   both compressed rows and permutes the shift equations simultaneously;
3. a common nonsquare multiplier followed by row swap, which exchanges the
   two prescribed compressed rows and restores their order.

A general multiplier cannot be applied independently to the two rows because
it sends their PAF values to potentially different shifts. Row swap alone,
or row negation, also fails to preserve the ordered prescribed compression.
These boundaries are explicit to prevent invalid symmetry breaking.

## 6. Exhaustive symmetry validation

All 7,614 p=3 canonical matches were independently translated into the new
normal form and checked against all 2,843 canonical OPB records. Every match
passed. They collapse to 846 normalized pairs because the enumerator stores
only one second-row representative per PAF signature.

For the complete ordered-pair count, the free `C_9 x C_9` action partitions
77,274 pairs into exactly

```text
77,274 / 81 = 954
```

translation orbits. This is an exact group-action count, not a heuristic
estimate.

The tracked canonical LP(27) OPB is 88,555 bytes with SHA-256
`6395e52bd04102237c2e9ba46ec5d4077dab2adc067943991faefd73919ae9c6`.
The complete rerun took 60.99 seconds on one core, including enumeration,
validation against both models, and streaming both LP(333) variants.

## 7. Certificate and search policy

The unbroken model remains the reference against which the translation-
canonical model is proved equisatisfiable. The encoded inequalities implement
only the independently proved translation action; the other coordinate
symmetries above remain unencoded until their interaction has an equally
explicit canonicalization proof.

For a satisfiable result, retain the solver assignment and check the two base
rows with the independent exact Legendre/SDS/PSD pipeline before constructing
and dual-verifying H(668). For an unsatisfiable result, require the exact OPB
hash and a proof accepted by VeriPB, whose official documentation identifies
OPB as its standard input and supports SAT/UNSAT certificates
`veripb2026`. A solver status line without a checked proof is not accepted.

The LP(27) RoundingSat/VeriPB pipeline is now checked end to end, but bounded
unfixed runs did not recover the known witness. See `pb_backend_benchmark.md`.
No LP(333) solver run is authorized until a backend solves an unfixed smaller
instance and its certificate verifies.
