# Independent derivation of the structured pq^2 compressed pair

Status: derivation complete and proved; retrieval gap closed; factor-9
uncompression reproduced at `p=3`; the `p=37, q=3` route is certified as a
valid compressed pair but is **not** computationally reachable by direct
enumeration.

This note removes the blocking dependency recorded in `length333_audit.md`,
where the newer `kotsireas2027pq2` source sequences could not be retrieved
because the publisher embeds them in a dynamic figure, blocks the direct PDF
with HTTP 403, and gates browser access behind a CAPTCHA.

**The sequences do not need to be retrieved. They are determined by a formula,
and the formula's defining property is provable in a few lines.** Everything
below is derived in this repository and covered by tests; no publisher
artifact is used.

## 1. The prescribed rows

For odd primes `p` and `q`, let `chi` be the quadratic character (Legendre
symbol) modulo `p`. Define length-`p` integer rows

```text
A_0 = 1,   A_j =  q * chi(j)   for j = 1..p-1
B_0 = 1,   B_j = -q * chi(j)   for j = 1..p-1
```

The claim is that `(A, B)` has every exact property required of the
factor-`q^2` compression of a binary Legendre pair of length `L = p*q^2`.

Implemented as `src.legendre.structured_compressed_pair`.

## 2. Proof of the compressed Legendre conditions

Write `m = q^2` for the aggregation factor and `L = p*m`.

### 2.1 Entry range and parity

Each entry is `1` or `±q`. Both are odd, and `q <= q^2 = m` for `q >= 1`, so
every entry lies in `[-m, m]` with parity `m`. This is exactly the range and
parity invariant that any factor-`m` compression of a `±1` sequence must obey.

### 2.2 Row sums

The quadratic character sums to zero over a complete residue system, because
the nonzero residues split evenly into `(p-1)/2` squares and `(p-1)/2`
non-squares. Hence

```text
sum(A) = 1 + q * sum_{j=1}^{p-1} chi(j) = 1 + 0 = 1
```

and likewise `sum(B) = 1`. A normalized Legendre pair has both row sums `+1`,
and compression preserves the row sum, so this is the required value.

### 2.3 The autocorrelation constants

This is the substantive step. Fix a shift `s` with `s != 0 (mod p)`.

Split each autocorrelation into the terms that touch index `0` and the rest.
Since `A_0 = B_0 = 1` and `A_j = -B_j` for `j != 0`:

```text
PAF_A(s) = A_0*A_s + A_{-s}*A_0 + sum_{j != 0, -s} A_j*A_{j+s}
         =  q*chi(s) + q*chi(-s) + q^2 * sum_{j != 0, -s} chi(j)*chi(j+s)

PAF_B(s) = B_0*B_s + B_{-s}*B_0 + sum_{j != 0, -s} B_j*B_{j+s}
         = -q*chi(s) - q*chi(-s) + q^2 * sum_{j != 0, -s} chi(j)*chi(j+s)
```

The sign flip on the off-zero entries is squared away in the quadratic terms
but survives in the terms that are linear in `A_0 = B_0 = 1`. **Those linear
terms therefore cancel when the two are added**, leaving

```text
PAF_A(s) + PAF_B(s) = 2*q^2 * sum_{j != 0, -s} chi(j)*chi(j+s).
```

The excluded indices contribute nothing anyway, because `chi(0) = 0`, so the
sum may be taken over all of `Z/pZ`. That is the classical **Jacobsthal sum**,
and for `s != 0` it equals `-1`:

```text
sum_{j in Z/pZ} chi(j)*chi(j+s) = -1     (s != 0 mod p).
```

Hence for every nonzero shift

```text
PAF_A(s) + PAF_B(s) = -2*q^2 = -2*m,
```

which is precisely the compressed constant required of a Legendre pair.

At shift zero, `PAF_A(0) = PAF_B(0) = 1 + q^2*(p-1)`, so

```text
PAF_A(0) + PAF_B(0) = 2 + 2*q^2*(p-1) = 2*L - 2*(m-1).
```

Again exactly the required constant. ∎

The Jacobsthal identity is not assumed: `jacobsthal_shifted_character_sum`
computes it directly, and tests confirm it returns `-1` at every nonzero shift
for `p in {3,5,7,11,13,37}`.

### 2.4 The Fourier form

Compression by residue classes samples the transform,
`DFT_compressed(k) = DFT_original(k*m)`, so a compressed Legendre pair must
satisfy `PSD_A(k) + PSD_B(k) = 2L + 2` at every nonzero frequency.
`check_compressed_legendre_psd` verifies this in cyclotomic integer
arithmetic. It holds for every case tested. At `p=37, q=3` the constant is
`2*333 + 2 = 668` — the target order itself.

## 3. Independent confirmation against the prior audit

`length333_audit.md` tabulated the output-length-37 constants as `650` at
shift zero and `-18` at nonzero shifts, computed from the Legendre definition
without reference to this formula. The derived pair `A(37,3), B(37,3)`
reproduces both exactly. Two independent routes agree, and the agreement is
locked in by
`test_prescribed_pair_at_p37_q3_matches_the_audited_length333_constants`.

## 4. Reproduced uncompression at p=3, q=3

**Reproduced computation.** The complete factor-9 uncompression of
`A(3,3) = (1, 3, -3)` and `B(3,3) = (1, -3, 3)` was enumerated exhaustively.

| quantity | value |
|---|---:|
| uncompressions per row | 889,056 |
| distinct PAF signatures on the B side | 88,821 |
| binary Legendre pairs recovered | 7,614 |
| wall time (one core) | 8.5 s |

The recovered LP(27) passes the all-shift PAF check, the
`SDS(27; 13, 13; 12)` check, and the exact cyclotomic PSD check, and yields an
H(56) accepted by both independent exact verifiers.

This is a genuinely **different** LP(27) from the Fletcher–Gysin–Seberry
Table 4 pair already in the repository: the 2001 pair compresses to
`(1, 1, -1)` and `(-3, 5, -1)`, a different compressed class from the
prescribed `(1, 3, -3)` and `(1, -3, 3)`. The two H(56) artifacts have
different SHA-256 hashes.

The uncompression mechanism reported in the source is therefore reproduced
rather than merely cited, using sequences derived here from first principles.

## 5. Why this does not reach 333

A compressed row with entries `A_j` admits exactly

```text
prod_j C(m, (m - A_j)/2)
```

binary uncompressions. For the prescribed rows at `q=3` every entry is `1` or
`±3`, giving `C(9,4) = 126` for the single entry `1` and `C(9,3) = C(9,6) = 84`
for each of the other `p-1` entries:

| p | L = 9p | uncompressions of one row | log10 |
|---:|---:|---:|---:|
| 3 | 27 | 889,056 | 5.9 |
| 5 | 45 | 6.27e9 | 9.8 |
| 7 | 63 | 4.43e13 | 13.6 |
| 11 | 99 | 2.20e21 | 21.3 |
| 13 | 117 | 1.55e25 | 25.2 |
| **37** | **333** | **2.37e71** | **71.4** |

The count is `126 * 84^(p-1)`, so it grows by a factor of `84` per unit
increase in `p`. At `p=37` one side of the search has about `10^71.4`
candidates. Enumerating that at an optimistic `10^9` candidates per second
would take on the order of `10^62` seconds; the universe is about `10^17.6`
seconds old.

**Direct enumeration of this route is not merely expensive; it is impossible
by many orders of magnitude.** No constant-factor engineering, parallelism, or
hardware change affects this conclusion. The `p=5` case at `6.3e9` already
exceeds the repository's four-core / thirty-minute / ten-gigabyte approval
gate, and `p=7` at `4.4e13` is out of reach for this project.

This is the honest reason the `p=37, q=3` row is stated as a conjecture in the
source and why the case remains open. The compressed object is certified valid;
finding a binary preimage is the entire difficulty, and it is unsolved.

## 6. What is and is not established

**Proved here.** For all odd primes `p, q`, the rows `A(p,q), B(p,q)` satisfy
every necessary condition on a factor-`q^2` compressed binary Legendre pair:
range, parity, row sums, all `p` autocorrelation constants, and all nonzero
exact PSD sums.

**Reproduced here.** At `p=3, q=3` the prescribed pair does uncompress; 7,614
binary Legendre pairs of length 27 exist above it, and one yields a
dual-verified H(56).

**Not established.** That `A(37,3), B(37,3)` has any binary uncompression.
Passing every compressed necessary condition does not imply a binary preimage
exists — a feasible compressed object need not uncompress, and the universal
uncompression statement is explicitly a conjecture in the source. Nothing here
constructs an LP(333) or an H(668), and nothing here is evidence that one
exists.

**Consequence for direction.** The primary route recorded in
`direction_selection.md` is now unblocked at the level of *data and
validation* and closed at the level of *direct search*. Any continuation must
attack the uncompression as a constraint-satisfaction problem with strong
propagation — the repository's stated backup direction — rather than by
enumeration. The `10^71.4` figure is the benchmark any such method must beat.
