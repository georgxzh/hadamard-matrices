# Order-428 literature audit and exact reproduction

Status: **reproduced and independently verified on 2026-07-25**.

This is a reproduction of Kharaghani and Tayfeh-Rezaie's published
construction, not a new existence result. The complete generated matrix is
`results/H428.csv`.

## Primary-source audit

The audited source is `kharaghani2005`:

- author-hosted PDF:
  <https://www.cs.uleth.ca/~hadi/research/h428.pdf>;
- local audit copy SHA-256:
  `1d6d5c0cf25d16db9e451b016ab2724fe974b079fe6c9a4f5d7a43967c855bd2`;
- journal metadata: *Journal of Combinatorial Designs* 13 (2005), 435-440,
  DOI `10.1002/jcd.20043`;
- PDF creation date shown by metadata: 2004-06-29;
- pages audited: all 7;
- visual checks: the formula page (PDF page 2) and printed-sequence page
  (PDF page 5) were rendered with Poppler and inspected at original
  resolution.

The paper's own link to a precomputed matrix is obsolete. It was neither
needed nor used. The matrix here is regenerated from the four printed source
sequences.

As a separate transcription cross-check, SageMath's current
`sage.combinat.t_sequences` source stores the same `TT(36)` as the hexadecimal
string

```text
060989975b685d8fc80750b21c0212eceb26
```

Decoding that string by SageMath's documented bit convention produces the
same four arrays as the visual paper transcription. SageMath is a software
cross-check; the paper remains the primary source.

## Exact definitions and indexing

All code uses zero-based array indices. Signs on the printed page are read
left-to-right as coefficients \(a_0,a_1,\ldots\). Reversing the display is
irrelevant to the standalone autocorrelation equations but would change the
block matrix, so this convention is explicit.

For a finite sequence \(A=(a_0,\ldots,a_{r-1})\), the paper uses the
nonperiodic autocorrelation

\[
N_A(s)=\sum_{i=0}^{r-1-s} a_i a_{i+s}
\quad (0\le s<r),
\]

and \(N_A(s)=0\) when \(s\ge r\). This is zero padding, not cyclic
autocorrelation.

A Turyn-type quadruple \(TT(n)\) has binary sequence lengths
\((n,n,n,n-1)\) and satisfies

\[
N_X(s)+N_Y(s)+2N_Z(s)+2N_W(s)=0
\quad (s\ge1).
\]

The exact source signs transcribed from page 5 are:

```text
X + + + - - - - + + - + - + - - - - - + + + + - + + - + + + + - - - - + -
Y + - + + + + + - - + - + - - + - - + + - - + + + + - + + + + - - - + + -
Z + - + + + + + - + - - + + + + - + + + - + + - - + + + - + - - + - - - +
W + + + - + - - - - - + + - - + - + + + - - + - + - + + + - + + + + - +
```

Their lengths are \((36,36,36,35)\), their sums are \((0,6,8,5)\), and all
35 exact Turyn-type equations pass.

## Paper-to-code maps

Theorem 1 gives base sequences

\[
A=Z;W,\quad B=Z;-W,\quad C=X,\quad D=Y,
\]

with lengths \((71,71,36,36)\). The implementation checks

\[
N_A(s)+N_B(s)+N_C(s)+N_D(s)=0
\]

at all 70 positive shifts before continuing.

The base-to-T map is

\[
\begin{aligned}
T_1&=(A+B)/2;0_{36}, &T_2&=(A-B)/2;0_{36},\\
T_3&=0_{71};(C+D)/2, &T_4&=0_{71};(C-D)/2.
\end{aligned}
\]

Each \(T_i\) has length 107. At each coordinate exactly one of the four
entries is nonzero, and the sum of their four nonperiodic autocorrelations
vanishes at all 106 positive shifts.

The four binary first rows used for circulants are

\[
\begin{aligned}
A_1&=T_1+T_2+T_3+T_4,\\
A_2&=-T_1+T_2+T_3-T_4,\\
A_3&=-T_1-T_2+T_3+T_4,\\
A_4&=-T_1+T_2-T_3+T_4.
\end{aligned}
\]

If \(R\) is the 107 by 107 back-diagonal identity, the final block array is

\[
\begin{bmatrix}
A_1&A_2R&A_3R&A_4R\\
-A_2R&A_1&A_4^{\mathsf T}R&-A_3^{\mathsf T}R\\
-A_3R&-A_4^{\mathsf T}R&A_1&A_2^{\mathsf T}R\\
-A_4R&A_3^{\mathsf T}R&-A_2^{\mathsf T}R&A_1
\end{bmatrix}.
\]

`src/order428.py` implements each arrow as a pure, exact-integer function.
Rows of a circulant are successive right shifts. Right multiplication by
\(R\) reverses columns.

## Independent validation

Before the full case, the same pipeline is tested on the published `TT(4)`
example and produces an exact order-44 Hadamard matrix.

For the full case:

- candidate SHA-256:
  `c00e3f86da7acdab1123fb9d2ed5fc887d5b86dd786662ab37e46a3072cc7869`;
- dimensions: \(428\times428\);
- alphabet: all 183,184 cells are exactly `1` or `-1`;
- direct verifier: PASS, all Python-integer row inner products checked;
- independent verifier: PASS, separately parsed bit-packed rows and exact
  Hamming distances checked;
- direct report SHA-256:
  `751c2fb0e3b4de1652cd3d4bca7fa1c8c6db21077986aadeecfb5f41e4c6ab9c`;
- independent report SHA-256:
  `f8557e714a8a24b58d8d5038dcd272f118f84e20c4c7a9bc7b0282452e7cb666`.

Thus \(H H^{\mathsf T}=428I_{428}\) exactly. This establishes only the
published order-428 result and says nothing about existence at order 668.

## Reproduction command

```powershell
python -m scripts.reproduce_h428
python -m pytest --basetemp .pytest-tmp\h428-run
```

The reproduction is deterministic and has no random seed. On the recorded
Windows 11 / AMD64 machine with Python 3.14.6, the final rerun used one core
and took 3.13 seconds wall time. Peak memory was not instrumented; the frozen result
package is under 0.5 MB. Exact per-run environment details are in
`results/H428_metadata.json`.

## Classification of claims

- **Proven in the cited paper:** the displayed sequence transformations map a
  valid `TT(36)` to an order-428 Hadamard matrix.
- **Reproduced here:** the printed sequences meet every defining equation;
  every intermediate invariant passes; the generated full CSV passes two
  independent exact verifiers.
- **Computational observation:** this implementation completes in seconds on
  the recorded machine.
- **Uncertainty:** the obsolete publisher-era electronic matrix may be a
  differently normalized but equivalent representative. It has not been
  recovered or compared, and that comparison is unnecessary for existence.
- **Failed attempts:** the first pytest invocation used an inaccessible
  system temporary directory; rerunning with a repository-local `--basetemp`
  resolved this environmental issue. No mathematical or search failure
  occurred.

## Implementation plan after this milestone

Proceed to the Legendre-pair framework in the phase order recorded in
`research/legendre_framework_plan.md`. Do not launch a `TT(56)` or `LP(333)`
search until the exact framework and smaller literature examples are
reproduced.
