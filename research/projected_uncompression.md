# Non-enumerative first stage and exact factor-three projection

Status: derived, implemented, and validated 2026-09-27. The p=37 first-stage
model was generated and measured but **not solved**. No LP(333) or order-668
search was started.

## 1. Literature and novelty boundary

The successive `q`-uncompression architecture comes from
`kotsireas2025compression`, and the prescribed `pq^2` route from
`kotsireas2027pq2`. Contemporary exact-search work also uses autocorrelation
vectors as meet-in-the-middle keys and compression along divisor chains
(`lebedev2026quaternary`), but that source concerns quaternary pairs and was
audited here from its arXiv abstract only. It is methodological context, not
evidence for a binary LP(333).

The projection theorem below is derived directly from the standard exact PAF
compression identity already implemented in this repository. A broader
novelty claim would require a dedicated literature comparison before
publication.

## 2. Exact projection theorem

Let binary rows `x,y` have length `3N`, where `N` is odd, and let their
factor-three compressions be a fixed valid intermediate pair `C,D` of length
`N`. Define combined autocorrelations

```text
F(t) = PAF_x(t) + PAF_y(t),
G(r) = PAF_C(r) + PAF_D(r).
```

Compression gives, exactly,

```text
G(r) = F(r) + F(r+N) + F(r+2N).
```

For a valid factor-three intermediate pair, `G(r)=-6` for every nonzero
`r modulo N`. Suppose only

```text
F(r) = -2,  r=1,...,N-1
```

is enforced. PAF symmetry gives `F(r+2N)=F(N-r)=-2`, so the compression
identity forces `F(r+N)=-2`. These equations cover all shifts except `N` and
`2N`. At zero,

```text
G(0) = F(0) + F(N) + F(2N) = (6N-4),
F(0) = 6N,  and  F(N)=F(2N),
```

hence `F(N)=F(2N)=-2`. Therefore shifts `1..N-1` are necessary and
sufficient for the complete final Legendre equations within a fixed valid
factor-three branch.

This reduces the exact join key from `(3N-1)/2` to `N-1` coordinates. It is
not a heuristic or modular filter; no solution is added or removed.

## 3. Implemented exact models

`src.uncompress.search_factor_three_uncompressions` uses the projected PAF
key and still checks every shift on returned witnesses.
`UncompressionPBModel(..., factor_three_projection=True)` emits XOR variables
and correlation equations only for shifts `1..N-1`. Construction is rejected
unless the supplied compressed rows pass every exact factor-three intermediate
condition.

At p=3, the full and projected joins agree exactly: 6,561 and 729 row
candidates, 243 distinct stored vectors, 45 matched streamed rows, and 135
ordered LP(27) pairs. At the rank-1 p=5 branch, the projected 14-coordinate
key recovers the same exact count of 27 ordered LP(45) pairs as the full
22-coordinate key. The measured projected join took 6.27 seconds in the frozen
run; the earlier full-key run took 7.77 seconds on the same machine, but this
single comparison is only an observed runtime, not an asymptotic claim.

The p=5 projected OPB has 1,350 variables and 5,084 records, versus 2,070
variables and 7,952 records for the generic full-shift model. A complete
witness certificate is accepted by VeriPB 3.0.2. A separate ten-second
RoundingSat open-search probe still returned `TIMELIMIT`; its roughly 23 MB
incomplete proof remains ignored scratch data and is not evidence.

## 4. Non-enumerative p=37 first stage

The exact two-bit intermediate model was instantiated directly at p=37. It
represents every length-111 pair above the prescribed length-37 rows without
enumerating residue triples:

| quantity | p=37 first-stage value |
|---|---:|
| base entry bits | 444 |
| square-XOR auxiliaries | 222 |
| shifted-product auxiliaries | 48,840 |
| total variables | 49,506 |
| OPB records | 147,538 |
| normalized inequalities | 147,668 |
| scratch OPB bytes | 4,538,361 |

The deterministic scratch OPB SHA-256 is
`475713cbd08c927e5b3373cd0e7b41d9be09d350ab02140f418a9df052454d7e`.
It was generated only to audit formulation size. No solver was invoked on it.

If a valid length-111 branch is later obtained, the projected length-333
second-stage dimensions are:

| model | variables | OPB records | normalized inequalities |
|---|---:|---:|---:|
| generic full shifts | 111,222 | 442,612 | 443,000 |
| exact projected shifts | 73,926 | 293,372 | 293,704 |

The projection removes 37,296 variables and 149,240 OPB records.

## 5. Remaining exponential obstruction

Every p=37 intermediate pair has exactly

```text
(9p+1)/2 = 167
```

magnitude-one entries across its two rows. Consequently its Cartesian binary
preimage product is always `3^167`. Even the best balanced split requires
about `3^83 + 3^84`, approximately `1.6e40`, row candidates for the current
explicit signature join. The projected key lowers work per candidate and
model size, but does not make enumeration remotely feasible.

The local PAF contributions form a dense quadratic three-state constraint
system on the minority-layer choices. A naive split of those choices does not
produce an additive meet-in-the-middle key: cross-half products remain for
essentially every shift. Any claimed `3^(k/2)` method must explicitly encode
or eliminate those cross terms rather than ignoring them.

## 6. Recommendation

Use the 49,506-variable first-stage OPB as the non-enumerative reference, but
do not launch it at p=37 yet. First add and prove intermediate translation
canonicalization, test the first-stage solver at p=5 and p=7 with short proof
budgets, and investigate a ternary/minority-layer encoding that exposes more
propagation than the generic two-bit product model. For the second stage, use
the projected 110-shift formulation once a branch exists. A p=37 run still
requires a separate resource estimate and approval.

Reproduction command:

```powershell
python -m scripts.build_projected_uncompression `
  --solver tmp\tools\roundingsat\roundingsat.exe `
  --verifier tmp\tools\veripb-3.0.2\bin\veripb.exe `
  --probe-seconds 10
```
