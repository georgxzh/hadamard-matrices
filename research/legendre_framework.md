# Exact Legendre-pair framework

Status: implemented and reproduced on 2026-07-25. This note records exact
mathematics and verified small examples; it does **not** report an LP(333) or
an order-668 Hadamard matrix.

Bibliographic keys refer to `references/references.bib`.

## Primary-source audit

Three complete primary-source PDFs were read, formula pages were rendered and
visually checked, and the following local research-input hashes were recorded.
The PDFs are not redistributed in this repository.

| Key | Pages/formulas used | SHA-256 |
|---|---|---|
| `fletcher2001` | Definition 1, Wiener--Khinchin discussion, Lemma 1, Theorem 3 and its displayed bordered array, Table 4 | `4d0bc39f392a24dfb0bec3a0f17961eab4dfffe85956a1204016110d029c82b5` |
| `djokovic2015compression` | Definition 3, equation (18), Theorem 3 and equations (19) | `a05f33d2d901e70440e17acb2a21988ab07ccda52b31dbc3398546a32a69bffb` |
| `kotsireas2021mod3` | LP/PSD definitions, Corollary 1 and equations (7)--(8) | `4e9cc7adcdb9f57cdf16b53a511ebafac63f780bacbe05b5ea9cf73a52648f5` |

The online-2026 `kotsireas2027pq2` publisher text was also audited for the
structured compression theorem and reported parameters. Its LP(27) signs are
embedded only as a dynamic figure, the direct PDF endpoint returned HTTP 403,
and browser access presented a CAPTCHA. The searchable trace formula does not
state enough of its trace convention to justify an independent reconstruction.
No signs from that figure were guessed or admitted as data.

## Fixed conventions

For an integer sequence `a=(a_0,...,a_{n-1})`, all indices are zero-based and

\[
  \operatorname{PAF}_a(s)=\sum_{i=0}^{n-1}a_i a_{i+s\bmod n}.
\]

The DFT convention is
\(\widehat a(k)=\sum_i a_i\exp(2\pi i k i/n)\), and
`PSD(a,k)=|widehat a(k)|^2`. Reversing the DFT sign does not change PSD, but the
sign is fixed here to make exact cyclotomic representations reproducible.
A binary Legendre pair has entries in `{+1,-1}`, odd common length `n`, row
sums of absolute value one, and

\[
  \operatorname{PAF}_a(s)+\operatorname{PAF}_b(s)=-2
  \quad(1\le s<n).
\]

Independent whole-row negation normalizes both row sums to `+1` without
changing PAF or PSD. No cyclic shift or reversal is silently applied.

## LP(n) to H(2n+2)

Let `A` and `B` be the right-shift circulants whose first rows are `a` and
`b`. The PAF equations give the exact matrix identity

\[
 AA^{\mathsf T}+BB^{\mathsf T}=(2n+2)I_n-2J_n.
\]

Theorem 3 of `fletcher2001`, checked against the rendered displayed array, is
implemented literally as

\[
H=\begin{bmatrix}
-1&-1&\mathbf1^T&\mathbf1^T\\
-1& 1&\mathbf1^T&-\mathbf1^T\\
\mathbf1&\mathbf1&A&B\\
\mathbf1&-\mathbf1&B^T&-A^T
\end{bmatrix}.
\]

The row sums `+1` make every border/block cross term vanish. The displayed
circulant identity makes both diagonal block Gram matrices `(2n+2)I`, and the
off-diagonal block Gram terms cancel because circulants commute. Thus
`H H^T=(2n+2)I` over the integers. The implementation still sends every
constructed full matrix through both independent repository verifiers.

## Supplementary difference sets

For a normalized binary row let `X={i:a_i=-1}`. Then `|X|=(n-1)/2`. If
`N_X(s)` is the number of ordered pairs `(x,y)` in `X^2` with
`x-y=s mod n`, direct expansion gives

\[
  \operatorname{PAF}_a(s)=n-4|X|+4N_X(s).
\]

Consequently the two negative supports form an SDS with parameters

\[
 (n;(n-1)/2,(n-1)/2;(n-3)/2).
\]

`check_negative_support_sds` is an independent exact check of these ordered
difference multiplicities; it does not call the PAF checker.

## Exact PSD certificates

Wiener--Khinchin gives

\[
 \operatorname{PSD}(a,k)=\sum_s \operatorname{PAF}_a(s)\zeta_n^{ks}.
\]

The code never accepts a floating-point value. It finds the order `q` of
`zeta_n^k`, folds exponents to `Z[x]`, and reduces the PAF polynomial modulo
the exactly generated cyclotomic polynomial `Phi_q(x)`. The resulting
`ExactCyclotomicValue` is a canonical element of `Z[x]/Phi_q(x)`. For a
Legendre pair and nonzero `k`, the combined value reduces to the rational
integer `2n+2`. Numerical evaluation exists only as a test diagnostic.

At a primitive third root the exact specialization for a three-entry
compression `(x_0,x_1,x_2)` is

\[
 |x_0+x_1\omega+x_2\omega^2|^2
 =\frac{3\sum_i x_i^2-(\sum_i x_i)^2}{2}.
\]

For normalized LP length `n=3m`, equation (8) of `kotsireas2021mod3` follows:
the six compressed squares sum to `4m+2`.

## Compression

Following Definition 3 of `djokovic2015compression`, a length `n=d m`
sequence is compressed to length `d` by

\[
 a^{(d)}_j=\sum_{r=0}^{m-1}a_{j+r d}.
\]

For a binary input, each entry lies in `{-m,-m+2,...,m}` and the row sum is
preserved. The exact identity checked at every output shift is

\[
 \operatorname{PAF}_{a^{(d)}}(k)
 =\sum_{r=0}^{m-1}\operatorname{PAF}_a(k+r d).
\]

For a Legendre pair the compressed combined PAF is

\[
 \begin{cases}
  2n-2(m-1),&k=0,\\
  -2m,&1\le k<d.
 \end{cases}
\]

The compressed DFT at frequency `t` is the original DFT at frequency `m t`,
so their exact cyclotomic PSD values agree.

For length 333 the implemented specializations are:

| output length `d` | factor `m` | combined PAF at zero | nonzero combined PAF |
|---:|---:|---:|---:|
| 3 | 111 | 446 | -222 |
| 9 | 37 | 594 | -74 |
| 37 | 9 | 650 | -18 |

Direct compression to length 3 is tested against length 9 followed by length
3. The deterministic length-333 tests also compare every sampled original PSD
with the corresponding compressed exact cyclotomic value. These are necessary
constraints only; a compressed candidate is not a binary uncompression.

## Published reproductions

Table 4 of `fletcher2001` was reconstructed at lengths 3, 5, 7, and 27.
Every source pair passed all-shift PAF, SDS, and exact PSD checks. The complete
bordered matrices passed both independent exact verifiers.

| LP | matrix | candidate SHA-256 |
|---:|---:|---|
| 3 | H(8) | `43d3038cde23ed4ec1459d4111e4692295ec4613185ded3f45db587b9dc8421d` |
| 5 | H(12) | `77b8a4c0d2ab12f7fa147d68071e29639892c032567cc326373e90b4bf6e558e` |
| 7 | H(16) | `fdb5ecc0a2ef69b0551371948c425d054960c60b7f34c65b1a79670dcc6f679c` |
| 27 | H(56) | `53369c062e6dd6ef5f9b9039e2e4106b221d24958464f92f42d7278e293c29ab` |

The LP(27) OCR layer omitted four printed glyphs. The 600-dpi rendered row was
segmented into 27 connected glyph components per sequence and classified by
glyph height; the recovered strings are

```text
+++++-+-+-++++--++---+-----
++-++--++--+-++++---+-+--+-
```

The resulting exact invariants are row sums `(1,1)`, SDS parameters
`(27;13,13;12)`, combined PAF `[54,-2,...,-2]`, 3-compressions
`(1,1,-1)` and `(-3,5,-1)`, and 9-compressions recorded in
`results/legendre_examples/metadata.json`. At the third root the two PSDs are
4 and 52, summing to 56. These redundant checks make an unnoticed glyph error
very unlikely.

This Table-4 LP(27) is a published pair at the parameter `27=3*3^2`, but it is
not the structured LP(27) claimed in `kotsireas2027pq2`: its 9-compressions do
not equal that paper's prescribed `A(3,3),B(3,3)`. Reproduction of the newer
structured example therefore remains open pending reliable figure data or a
fully specified trace convention.

## Reproduction

```powershell
python -m scripts.reproduce_legendre_examples
python -m pytest
```

The script records source signs, PAFs, SDS parameters, compressions, candidate
and report hashes, timestamps, runtime, Python/platform data, and the explicit
one-core/no-seed configuration in `results/legendre_examples/metadata.json`.
