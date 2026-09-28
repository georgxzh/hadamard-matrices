# Published LP(45) and bounded p=5 model validation

Status: reproduced and exactly verified 2026-09-27. This is a fixed-witness
validation, not an open search and not an order-668 result.

## Primary-source audit

Section 5.3.2 of `kotsireas2025compression` prints two length-45 binary rows
and reports their 9-compression as

```text
A(5,3) = (1,  3, -3, -3,  3)
B(5,3) = (1, -3,  3,  3, -3).
```

The publisher HTML was accessible on 2026-09-27 even though the direct PDF
remained unavailable. The displayed rows were transcribed in their printed
order into `published_structured_legendre_pair_45`; repository indices are
zero-based. No OCR repair or inferred sign was needed.

The source describes the larger constructions as two successive
q-uncompressions. For this `q=3` example, the transcribed rows first
3-compress from length 45 to

```text
C = (-3,-1,-1,-3, 1, 1, 3,-1,-1,-1, 3, 1,-1, 1, 3)
D = (-1,-1,-1, 1,-1,-1,-1, 1, 1,-1, 3,-1, 3, 1,-1),
```

and `(C,D)` then 3-compresses exactly to `(A(5,3),B(5,3))`. Direct
9-compression gives the same result.

## Exact reproduction

The fixed source rows pass all of the following independently implemented
integer checks:

- all 44 nonzero combined PAF equations equal `-2`;
- `SDS(45;22,22;21)` difference multiplicities;
- all nonzero-frequency exact cyclotomic PSD sums equal `92`;
- direct factor-9 and successive factor-3 compression identities;
- every record in both p=5 OPB models;
- complete-assignment SAT certificates accepted by VeriPB 3.0.2.

The two-circulant-core construction produces `results/p5_validation/H92.csv`.
The direct integer-Gram verifier and separately parsed bit-packed verifier
both prove `H H^T = 92 I_92`. Candidate SHA-256 is
`b134f19a01280f1b7c473f1c3900d2a4bc751596ca6f4c247ddf19b68a45fd77`.

## Model scale

| quantity | unbroken | translation-canonical |
|---|---:|---:|
| base variables | 90 | 90 |
| XOR auxiliaries | 1,980 | 1,980 |
| total variables | 2,070 | 2,070 |
| XOR inequalities | 7,920 | 7,920 |
| equality records | 32 | 32 |
| symmetry inequalities | 0 | 16 |
| OPB records | 7,952 | 7,968 |
| normalized inequalities | 7,984 | 8,000 |
| OPB bytes | 252,228 | 253,540 |

Each row has exactly `6,273,179,136` binary preimages of the prescribed
compression, so no direct enumeration was attempted. Translation
canonicalization again gives an exact free factor-81 reduction. Both known
witness certificates verified in under 0.03 seconds on the recorded machine;
this measures checking a supplied solution, not finding one.

## XOR-layer audit

The p=5 counts make the bottleneck explicit: XOR auxiliaries are 95.65% of
the variables, and their inequalities are 99.60% of the unbroken OPB records.
The implementation now exposes the four-facet XOR gadget and exhaustively
checks its eight binary assignments. Removing any one of its four facets
admits a false XOR assignment. Thus no facet can be dropped from this direct
per-disagreement reification while preserving exactness.

This does not prove that all exact formulations require the same auxiliaries.
It shows only that local deletion cannot improve the present formulation. A
conditional two-stage q-uncompression branch model has now been implemented
and validated at p=3 and p=5; see `staged_uncompression.md`. It solves p=3
with checked proofs but times out at p=5. Complete p=5 first-stage generation,
branch profiling, and the exact projected PAF key are now recorded in
`intermediate_stage.md`, `p5_branch_portfolio.md`, and
`projected_uncompression.md`.

## Reproduction

```powershell
python -m scripts.validate_p5_uncompression `
  --verifier tmp\tools\veripb-3.0.2\bin\veripb.exe
```

The run used one CPU core, completed in 0.58 seconds, and reported a Python
`tracemalloc` peak of 1,478,512 bytes. Complete commands, hashes, timestamps,
tool identity, model statistics, and certificates are frozen in
`results/p5_validation/metadata.json`.
