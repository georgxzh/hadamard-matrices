# Mathematical primer

Last audited: 2026-07-25

## 1. The object

An order-\(n\) **Hadamard matrix** is a matrix

\[
H\in\{-1,1\}^{n\times n}
\quad\text{such that}\quad
HH^{\mathsf T}=nI_n.
\]

The \((i,j)\)-entry of \(HH^{\mathsf T}\) is the ordinary integer dot
product of rows \(i\) and \(j\). Thus the definition says:

- each row has squared length \(n\); and
- every two distinct rows are orthogonal.

Because the entries are already constrained to ±1, the diagonal equation is
automatic after the shape and entry checks. The off-diagonal equations are
the substantive verification task. This project nevertheless checks both.

## 2. Why the order is usually divisible by four

**Proven fact.** If an order-\(n\) Hadamard matrix exists and \(n>2\), then
\(4\mid n\).

**Proof.** Negating columns preserves all row inner products, so normalize the
first row to all \(+1\). Every other row is orthogonal to it and therefore has
equally many \(+1\)'s and \(-1\)'s; hence \(n\) is even. Permute columns so the
second row is

\[
(1,\ldots,1,-1,\ldots,-1),
\]

with \(n/2\) entries of each sign. For a third row, let \(a\) be the number of
\(+1\)'s in the first half. Orthogonality to the first row forces the second
half to contain \(n/2-a\) plus signs. Orthogonality to the second row gives

\[
(2a-n/2)-\bigl(2(n/2-a)-n/2\bigr)=4a-n=0.
\]

Therefore \(n=4a\). ∎

The **Hadamard conjecture** asserts the converse for positive multiples of
four. It remains a conjecture.

## 3. Equivalence and normalization

These operations preserve the Hadamard property:

1. permuting rows;
2. permuting columns;
3. negating a row;
4. negating a column.

Consequently every Hadamard matrix is equivalent to a **normalized** one whose
first row and first column are all \(+1\). Equivalent matrices are different
CSV files but not essentially different designs under this equivalence.

Normalization is useful for search-space reduction, but every symmetry
reduction used in a search must be proved to preserve at least one
representative of every desired equivalence class.

## 4. Two reproducible small constructions

### 4.1 Sylvester construction

Starting with \(H_1=[1]\), define

\[
H_{2n}=
\begin{pmatrix}
H_n&H_n\\
H_n&-H_n
\end{pmatrix}.
\]

Direct block multiplication proves
\(H_{2n}H_{2n}^{\mathsf T}=2nI_{2n}\) whenever
\(H_nH_n^{\mathsf T}=nI_n\). This gives every power-of-two order. The test
suite reproduces orders \(1,2,4,8,16,32\).

### 4.2 Paley type I

For a prime power \(q\equiv3\pmod4\), Paley's quadratic-character
construction gives an order-\(q+1\) Hadamard matrix. The test suite implements
the prime cases \(q=3,11,19\), producing orders \(4,12,20\). This is a genuine
construction from quadratic residues, not stored matrix data.

## 5. Sequence language

For a real sequence \(a=(a_0,\ldots,a_{L-1})\), with indices modulo \(L\),
define the periodic autocorrelation

\[
\operatorname{PAF}_a(s)
=\sum_{j=0}^{L-1}a_j a_{j+s}.
\]

For \(a,b\in\{\pm1\}^L\) and odd \(L\), a standard definition of a
**Legendre pair** is

\[
\operatorname{PAF}_a(s)+\operatorname{PAF}_b(s)=-2
\quad (s\not\equiv0\pmod L).
\]

At shift zero the sum is \(2L\). Summing all shifts shows that

\[
\left(\sum_j a_j\right)^2+\left(\sum_j b_j\right)^2=2,
\]

so the two row sums are each ±1. Independent negation can normalize both to
\(+1\).

The discrete Fourier transform converts periodic autocorrelation into power
spectral density (finite Wiener–Khinchin):

\[
\operatorname{PSD}_a(k)=|\operatorname{DFT}_a(k)|^2.
\]

For a Legendre pair, the nonzero-frequency constraint becomes

\[
\operatorname{PSD}_a(k)+\operatorname{PSD}_b(k)=2L+2.
\]

PSD is valuable as a necessary search constraint, but numerical evaluation of
algebraic Fourier values is not an exact certificate unless accompanied by
proved error bounds or an exact algebraic representation.

## 6. Why length 333 matters

**Published implication, not yet independently derived in this repository.**
Fletcher, Gysin, and Seberry (2001) show that a binary Legendre pair of odd
length \(L\) yields a Hadamard matrix of order \(2L+2\). Therefore

\[
L=333 \Longrightarrow 2L+2=668.
\]

The converse is not known and must not be assumed: an order-668 Hadamard
matrix need not arise from a Legendre pair. Phase 4 will derive the array,
indexing, and sign conventions independently and test them on smaller cases.

After normalizing the row sums, the negative supports of a length-333 pair
have the supplementary-difference-set parameters

\[
\operatorname{SDS}(333;166,166;165).
\]

This supplies an exact combinatorial encoding: every nonzero group element
must occur exactly 165 times among the ordered within-block differences.

## 7. Compression

If \(L=dm\), one common convention compresses a length-\(L\) sequence to
length \(d\):

\[
\widetilde a_j=\sum_{t=0}^{m-1}a_{j+td}.
\]

Each compressed entry is an integer congruent to \(m\pmod2\) in
\([-m,m]\). Compression preserves exact aggregated autocorrelation and samples
of the exact Fourier data. These constraints can drastically prune a search,
but a feasible compressed pair need not uncompress to binary sequences.

Because \(333=3^2\cdot37\), the natural lengths mentioned in the literature
include 3-, 9-, and 37-coordinate compressed objects. Authors sometimes name
compression by the number of terms combined and sometimes by the output
length; every implementation in this repository will state both.

## 8. Other construction families

- **Williamson type:** four suitably symmetric commuting ±1 matrices
  \(A,B,C,D\) satisfying
  \(AA^{\mathsf T}+BB^{\mathsf T}+CC^{\mathsf T}+DD^{\mathsf T}=4tI_t\)
  feed a block array of order \(4t\). For order 668, \(t=167\).
- **Goethals–Seidel:** four circulant blocks satisfying the same sum-of-Gram
  identity feed a less restrictive block array, often obtained from four
  supplementary difference sets in a group of order \(t\).
- **Supplementary difference sets:** translate periodic autocorrelation into
  exact difference multiplicities in a finite group.
- **Cocyclic constructions:** encode entries with a group 2-cocycle; cocyclic
  Hadamard matrices correspond to particular relative difference sets.
- **Turyn/base/T-sequence constructions:** the published order-428 result
  starts from a Turyn-type sequence \(TT(36)\), produces base sequences of
  lengths \(71,71,36,36\), and then a Hadamard matrix of order 428.

These descriptions identify constraint families, not evidence that any one of
them reaches 668.

## 9. Exact verification standard

A final candidate is accepted only if both implementations:

1. parse exactly 668 rows and 668 columns;
2. accept only literal integer values \(1\) and \(-1\);
3. compute every relevant Gram entry with integer arithmetic;
4. obtain diagonal 668 and every off-diagonal zero;
5. record the candidate and report SHA-256 hashes.

Low loss, approximate orthogonality, modular orthogonality, or a valid
compressed object is not a solution.

## 10. Current status

**Source-backed status as of 2026-07-25.** Epoch AI labels order 668 unsolved.
Cati and Pasechnik's construction database leaves it absent, a 2025 paper
constructs only a 64-modular matrix at this order, and the 2026-07-22 preprint
by Ramos, Hulak, and de Queiroz explicitly says the unrestricted order-668
problem remains open.

This is strong current evidence, not a proof that no unpublished construction
exists. The status must be checked again before any public solution claim.
