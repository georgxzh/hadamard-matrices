# Literature map

Last audited: 2026-07-25

This is a working constraint map, not a claim of exhaustive coverage.
Bibliographic keys refer to `references/references.bib`.

## Status sources

### Epoch AI open-problem page — `epoch2026`

- **Exact claim:** asks for an order-668 Hadamard matrix, labels the problem
  unsolved, and identifies order 428 as the previous smallest unknown order.
- **Role:** benchmark statement, not primary mathematical literature.
- **Code/data:** none.
- **Implication:** defines the deliverable: a complete CSV matrix.
- **Uncertainty:** a web page is not a proof of current nonexistence; it is
  corroborated below.

### Construction database — `cati2024database`

- **Exact claim:** supplies SageMath constructions for all known Hadamard and
  skew-Hadamard orders through 1208 and updated tables beyond that range.
- **Family:** many families, encoded as executable SageMath constructions.
- **Parameters for 668:** the database documents 668 among the missing known
  orders; no construction is implemented.
- **Code/data:** SageMath's
  `sage.combinat.matrices.hadamard_matrix` is executable and independently
  testable.
- **Reproducibility:** high for implemented orders; the paper itself reports
  finding and fixing a literature error at skew order 292, which motivates
  implementation-level audits.
- **Implication:** use Sage as a comparison implementation for known small
  orders and construction plumbing, never as proof for 668.

### 64-modular order 668 — `eliahou2025modular`

- **Exact claim:** constructs \(H\in\{\pm1\}^{668\times668}\) with
  \(HH^{\mathsf T}\equiv668I\pmod{64}\).
- **Family:** modular Hadamard construction.
- **Parameters for 668:** directly at 668, but only modulo 64.
- **Code/data:** the article is open access; construction data availability
  still needs a file-level audit.
- **Reproducibility:** mathematical construction appears explicit; not yet
  reproduced here.
- **Implication:** possibly useful residue structure or initialization.
- **Critical limitation:** modular orthogonality is strictly weaker than
  integer orthogonality and is not a FrontierMath solution.

## Order-428 warm-up

### Kharaghani–Tayfeh-Rezaie — `kharaghani2005`

- **Exact claim:** four Turyn-type sequences of lengths \(36,36,36,35\) give
  base sequences of lengths \(71,71,36,36\), new T-sequences, and an
  order-428 Hadamard matrix.
- **Family:** Turyn-type sequences → base sequences → T-sequences /
  Goethals–Seidel-related construction.
- **Parameter identity:** \(428=4(71+36)=4\cdot107\).
- **Code/data:** the author-hosted full article provides all four source
  sequences and every map needed to regenerate the matrix. SageMath's current
  T-sequence module independently stores the same source data in hexadecimal.
- **Reproducibility:** complete. The full paper was audited, its sequence page
  visually transcribed and checked against SageMath's independent encoding,
  every intermediate equation passed, and the generated complete matrix
  passed both exact repository verifiers.
- **Resolved conventions:** signs are read left-to-right with zero-based
  indices; correlations before the circulant stage are nonperiodic; circulant
  rows are right shifts; right multiplication by the back-diagonal identity
  reverses columns. See `order428_reproduction.md`.
- **Implication for 668:** later work on Turyn-type sequences states that a
  \(TT(56)\) would yield order 668 because
  \(668=4((2\cdot56-1)+56)=4(111+56)\). Existence of \(TT(56)\) is not known
  from the audited sources.

## Legendre-pair route

### Fletcher–Gysin–Seberry — `fletcher2001`

- **Exact claim relevant here:** a generalized/binary Legendre pair of odd
  length \(L\) yields a Hadamard matrix of order \(2L+2\).
- **Family:** periodic autocorrelation / DFT and a structured block
  construction.
- **Parameters for 668:** \(L=333\).
- **Code/data:** open article; no modern reference implementation located.
- **Reproducibility:** the implication is source-backed but not yet
  independently reconstructed here.
- **Constraint extracted:** for all nonzero shifts,
  \(\operatorname{PAF}_a(s)+\operatorname{PAF}_b(s)=-2\); equivalently for
  nonzero frequencies the PSD sum is \(2L+2=668\).
- **Important logic:** LP(333) implies HM(668); it is not equivalent to the
  existence of an arbitrary HM(668).

### Compression — `djokovic2015compression`

- **Exact claim:** compression of periodic complementary sequences remains
  complementary and provides smaller necessary systems.
- **Parameters for 333:** divisors \(3,9,37,111\) induce useful compressed
  lengths and aggregation factors.
- **Code/data:** formulas are explicit; no canonical package required.
- **Reproducibility:** suitable for an exact reference implementation.
- **Constraint extracted:** compressed entries have exact parity/range and
  compressed PAF is the sum of original PAF values in congruence classes.
- **Gap:** compression feasibility is necessary, not generally sufficient for
  binary uncompression.

### Lengths divisible by 3 — `kotsireas2021mod3`

- **Exact claim:** determines the possible special DFT/PSD values for Legendre
  pairs with length divisible by 3 and constructs several previously open
  lengths.
- **Parameters for 333:** directly applicable because \(3\mid333\).
- **Code/data:** arXiv text is available; associated code/data audit pending.
- **Constraint extracted:** special-frequency values can be handled through
  integer/number-theoretic conditions rather than approximate complex FFTs.

### \(pq^2\) uncompression — `kotsireas2027pq2`

- **Exact proved/computational content:** proposes a structured
  \(q^2\)-compression family and reports constructed/verified LP(27), LP(45),
  LP(63), and LP(75).
- **Conjecture (not a result):** every odd-prime pair \(p,q\) admits the stated
  uncompression to LP(\(pq^2\)).
- **Parameters for 333:** \(p=37,q=3\), so the conjecture would produce
  LP(333), hence HM(668).
- **Code/data:** Maple listings are included; article says other data are
  available on request.
- **Reproducibility:** smaller reported pairs should be reconstructed before
  trying \(p=37\).
- **Critical distinction:** the table's 333 row is a proposed route, not a
  constructed LP(333).

### 2026 computational status report — `chojecki2026status`

- **Reported observations:** 12,017,243 PSD-compatible 9-compressed column
  configurations; simulated annealing on a 37-compressed system reached an
  \(L_1\) PSD deviation of 236, not zero.
- **Type:** independent technical report, not a peer-reviewed proof.
- **Code/data:** availability and completeness need auditing.
- **Reproducibility:** not yet reproduced.
- **Implication:** identifies a search bottleneck and candidate macro-cases.
- **Caution:** the report calls the Hadamard problem “equivalent” to LP(333);
  the implication needed for construction is valid, but the converse is not.
  The near-zero objective is explicitly not a solution.

### Common-multiplier obstruction — `ramos2026multipliers`

- **Exact theorem:** if both sequences of a length-333 Legendre pair are fixed
  by the same subgroup
  \(H\le(\mathbb Z/333\mathbb Z)^\times\), then \(|H|\le6\).
- **Case ledger:** after a mod-3 reduction, 30 subgroups remain; 21 are
  excluded, including all 19 of order at least 9. Nine subgroups of orders at
  most 6 remain undecided by the paper.
- **Methods:** exact value-set compression, sum-of-two-squares obstruction,
  row-sum congruences, meet-in-the-middle enumeration, pseudo-Boolean systems,
  DRAT proofs, and arithmetic certificates.
- **Parameters:** exactly length 333.
- **Code/data:** the preprint states that solver cases have independently
  checkable certificates; artifact URLs were not visible on the arXiv record
  and must be obtained/audited.
- **Reproducibility:** analytic arguments can be rederived; certificate cases
  need artifact retrieval and independent checking.
- **Implication:** do not spend resources searching fixed common multipliers
  of order at least 9.
- **Strict scope:** says nothing about unrestricted pairs, separate multiplier
  groups, or multiplier-with-translation symmetry. It leaves HM(668) open.

## Alternative construction families

### Goethals–Seidel / supplementary difference sets

The block condition is

\[
AA^{\mathsf T}+BB^{\mathsf T}+CC^{\mathsf T}+DD^{\mathsf T}=4tI_t.
\]

For four cyclic blocks at order 668, \(t=167\). If negative supports
\(X_i\subseteq\mathbb Z_{167}\) have sizes \(k_i\), the SDS equations require
one common difference multiplicity \(\lambda\) and
\(\sum_i k_i=\lambda+167\). These are exact integer constraints suitable for
code. The modern surveys `djokovic2009sds` and `djokovic2018gs` provide
examples and warn that published classifications can contain errors.

### Williamson type

Williamson matrices impose symmetry and pairwise commutation in addition to
the four-Gram identity. Order 668 requires four blocks of order 167. The
prime block size is mathematically clean but the audited construction
databases do not currently supply the needed quadruple. Exhaustive feasibility
at 167 has not been established here.

### Cocyclic

`deLauneyFlannery2000` proves an equivalence between cocyclic Hadamard
matrices of order \(4t\) and normal relative difference sets with parameters
\((4t,2,4t,2t)\). At \(4t=668\), this gives exact group/cohomology constraints.
No theorem located in this initial audit constructs the required relative
difference set at 668. Group enumeration and cohomology would need a separate
feasibility study before search.

## Initial comparison

| Route | Exact target object | Main benefit | Main current barrier |
|---|---|---|---|
| LP(333) | two 333-bit sequences | strongest recent theory and compression | unrestricted uncompression remains open |
| TT(56) | four sequences of lengths 56,56,56,55 | mirrors successful order 428 | existence/search status unclear |
| GS/SDS(167) | four subsets/circulants | direct order \(4\cdot167\) array | enormous unstructured search |
| Williamson(167) | four symmetric circulants | strong algebraic reduction | restrictive and no known quadruple |
| cocyclic(668) | cocycle / relative difference set | group-theoretic structure | candidate groups and cohomology not audited |

Order 428 is now reproduced. The next research phase is the exact
Legendre-pair core and compression framework, followed by the small \(pq^2\)
Legendre examples before selecting a high-cost route.
