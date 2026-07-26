# Audit report

Status: Phase 5 has not started.

## Findings already requiring care

1. **Implication versus equivalence.** LP(333) implies HM(668), but an
   arbitrary HM(668) need not yield LP(333). Search reports sometimes use
   “equivalently” informally; this repository will not.
2. **Compression naming.** Sources vary between naming by aggregation factor
   and output length. Every implementation will specify both.
3. **Modular versus integer orthogonality.** A 64-modular matrix of order 668
   is published, but it is not an integer Hadamard matrix.
4. **Common fixed multipliers are narrow.** The 2026 obstruction covers a
   shared fixed subgroup, not multiplier-with-translation or unrestricted
   pairs.
5. **Conjectural \(pq^2\) row.** The published table identifies \(p=37,q=3\)
   as a route to LP(333); it does not report constructing that row. As of
   2026-07-26 this repository derives and certifies the compressed pair
   \(A(37,3),B(37,3)\) independently, but certification is of *necessary*
   conditions only. No binary uncompression at \(p=37\) is known, and direct
   enumeration would need about \(2.4\times10^{71}\) candidates per row.
   A certified compressed object must never be reported as progress toward a
   matrix.
6. **Approximate PSD.** A small floating-point objective is not exact
   autocorrelation and cannot certify a pair.

All previous computational claims remain “not reproduced” until their code,
inputs, outputs, and exact checks have been inspected.
