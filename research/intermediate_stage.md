# Exact first-stage q=3 intermediate generation

Status: exhaustive implementation and validation completed 2026-09-27 for
`p=3` and `p=5`. This is a small-parameter reproduction of the successive
uncompression architecture in `kotsireas2025compression`, not an LP(333) run
and not an order-668 result.

## Scope and conventions

For a binary Legendre pair of length `9p`, successive 3-compression has the
form

```text
binary rows of length 9p -> integer rows C,D of length 3p
                            -> prescribed A(p,3),B(p,3) of length p.
```

Indices and PAF shifts are zero-based. Each entry of `C,D` is in
`{-3,-1,1,3}`. A candidate intermediate pair is accepted exactly when its
second compression is the prescribed pair and

```text
PAF_C(0) + PAF_D(0) = 18p - 4,
PAF_C(s) + PAF_D(s) = -6 for every nonzero s modulo 3p.
```

Symmetry `PAF(s)=PAF(3p-s)` means shifts `0..floor(3p/2)` suffice for the
enumeration join. Every stored representative is then checked against the
complete exact model.

## Exhaustive generator

For prescribed entry `t`, the generator lists every ordered triple in
`{-3,-1,1,3}^3` summing to `t` and places it in one residue class modulo `p`.
There are 12 triples for `t=+/-1` and 10 for `t=+/-3`. Consequently each
`p=3` row has `12*10^2 = 1,200` candidates and each `p=5` row has
`12*10^4 = 120,000` candidates.

Rows are grouped by their exact nonredundant PAF signature. The two maps are
hash-joined against target `(18p-4,-6,...,-6)`. Multiplicities are retained,
so the reported ordered-pair count is exact rather than a count of signature
classes or stored representatives.

| p | rows per side | signatures per side | matching signature classes | ordered pairs |
|---:|---:|---:|---:|---:|
| 3 | 1,200 | 282 | 25 | 792 |
| 5 | 120,000 | 18,348 | 208 | 10,476 |

The `p=3` space is covered in full and regression-tested. At `p=5`, the
published length-15 intermediate rows obtained from the printed LP(45) occur
as an exact stored representative, not merely as a compatible aggregate.

## Independent exact OPB formulation

Write an intermediate entry uniquely as

```text
c_i = 3 - 2 n_i,       n_i = u_i + 2 v_i,       u_i,v_i in {0,1}.
```

The compression equations are weighted cardinalities. Let
`w_i = u_i XOR v_i`; then `w_i=1` precisely when `|c_i|=1`, and the zero-shift
condition is

```text
sum over both rows of w_i = (9p+1)/2.
```

For a nonzero shift `s`, expansion gives

```text
c_i c_(i+s) = 9 - 6(n_i+n_(i+s)) + 4 n_i n_(i+s).
```

The fixed row sums reduce the combined PAF equation to

```text
sum over both rows and all i of n_i n_(i+s) = 9(3p-1)/2.
```

All four bit products in `n_i n_(i+s)` are represented by exact three-facet
AND hulls with weights `1,2,2,4`. Exhaustive truth-table tests prove the AND
and XOR gadgets exact and each local facet individually necessary.

| p | variables | OPB records | normalized inequalities | OPB bytes |
|---:|---:|---:|---:|---:|
| 3 | 342 | 947 | 958 | 25,735 |
| 5 | 930 | 2,658 | 2,676 | 72,581 |

Known p=3 and published p=5 branches satisfy every model record. Their
complete assignment certificates are accepted by VeriPB 3.0.2. Exact hashes
and verifier transcripts are in `results/intermediate_stage/metadata.json`.

## Resource record and interpretation

The frozen run used one CPU core and no random seed. With Python `tracemalloc`
enabled, p=5 enumeration took 15.293400 seconds and peaked at 18,917,201
tracked bytes; p=3 took 0.060484 seconds and 221,393 bytes. The output package
is well below the project's compute and storage approval gates.

This completes the first-stage small-case gate. It does **not** make naive
enumeration plausible at p=37: the residue-product count remains exponential.
The 10,476 p=5 intermediate pairs are also not 10,476 binary LP(45)s; each is
only a branch for the second-stage binary uncompression, whose earlier
ten-second p=5 probes timed out even on the published branch.

## Next milestone

The complete p=5 set has now been reduced to 1,164 translation orbits and a
three-branch exhaustive portfolio finds two satisfiable branches and one
branch with no binary pair; see `p5_branch_portfolio.md`. Before any p=37
proposal, derive a non-enumerative first-stage constraint/search strategy and
stronger exact second-stage projections. No LP(333) computation is authorized
by this result.

Reproduction command:

```powershell
python -m scripts.build_intermediate_stage `
  --verifier tmp\tools\veripb-3.0.2\bin\veripb.exe
```
