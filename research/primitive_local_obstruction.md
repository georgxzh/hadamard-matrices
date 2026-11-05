# Primitive-frequency local arithmetic: a failed obstruction and its limits

Research round: October 14, 2026. Base commit
`beac2a4ca80d8087b01780f677596d60717e178a`, branch
`agent/order-428-reproduction`. The initial tree was clean. No child
AGENTS.md or CLAUDE.md was found. Read the phase-moment note, the exact
cyclotomic implementation in `src/legendre.py`, the phase representation and
propagator, and the frozen branch and witness records. Existing propagation
already enforces shared differences, triangles, signed sums, and carries.

**Outcome:** the selected modulo-nine obstruction fails, even with both
compression conditions and the third gauge. A stronger explicit false positive
is given below. We proved elementary local and coefficient-bound statements;
we did **not** obtain an explanatory nonexistence theorem for branch 279 or
establish substantive originality. The narrower reproducibility/software
assessment remains appropriate. The manuscript was neither edited nor compiled.

## 1. Exact domain and selected candidate

Write O=Z[zeta], zeta a primitive 45th root, omega=zeta^15, and

`S = F_C*conjugate(F_C) + F_D*conjugate(F_D) - 23`.

The indexed intermediate rows, in zero-based order, are

```
C    = (-1,-1, 1,-1, 1, 1, 1,-3,-3, 1, 1, 3,-1, 1, 1)
D277 = (-3,-1, 1,-1,-3, 1,-1, 1, 3,-1, 3,-1, 1, 1, 1)
D279 = (-1,-3, 1,-1,-1,-1,-1, 1, 3,-3, 3, 1, 1, 1, 1)
```

Active indices are respectively

```
C:    (0,1,2,3,4,5,6,9,10,12,13,14)
D277: (1,2,3,5,6,7,9,11,12,13,14)
D279: (0,2,3,4,5,6,7,11,12,13,14)
```

Each active coefficient keeps its sign and its phase in {0,1,2}. Three gauges
fix the first two active C phases and the first active D phase to zero. These
are exactly the two layer translations and the previously proved free
prime-kernel quotient, not a new symmetry reduction. Decoding is
`x[i+15*k]=sign(C_i)-2*C_i*[k=a_i]` on active columns; forced columns are
constant. No permutations of active indices or signs are permitted.

At zeta the column-constant part vanishes, so x(zeta)=-2F_C and
y(zeta)=-2F_D. Thus 4S is the primitive pair-PSD defect. This norm reduction
and its Galois consequences are established precedents, not contributions.

**Selected candidate:** after the carry-aware moments modulo three, require
`S in 9O`, or equivalently valuation at least twelve at the prime above three.
Necessity is immediate from S=0, but sufficiency, branch separation, and a short
structural contradiction are separate questions. This condition retains all
indexed data in S; it does not replace F_C,F_D by unrestricted field elements.

## 2. What reduction at three can and cannot add

Set pi=1-zeta^5. The prime above 3 is unique, with residue field F_81,
ramification index six, and (3)=(pi)^6. Indeed

`Phi_45(z) = z^24-z^21+z^15-z^12+z^9-z^3+1`,
`Phi_45(z) mod 3 = Phi_5(z)^6`.

Phi_5 is irreducible over F_3 because 3 has order four modulo five. In the
cyclotomic integer ring this gives one prime of residue degree four. The
element 1-zeta^5 has absolute norm 3^4, so generates that prime. Equivalently,
the six conjugates of 1-t for t=zeta^5 multiply to three, and each is associated
to 1-t. We normalize v(pi)=1, hence v(3)=6 and v(1-omega)=3.

In O/(pi), zeta becomes a primitive fifth root alpha and omega becomes one.
For each of the three indexed rows above,

`sum_(i active) C_i*alpha^i = 1`.

This is checked by reducing the displayed signed polynomial modulo Phi_5 over
F_3, and is independent of every phase. Thus both F values reduce to one and
the required equation reduces to `1+1=23 mod 3`. Residue-field reduction alone
cannot distinguish the branches. Reduction modulo the rational integer three
is stronger: O/3O has nilpotents and dimension 24 over F_3. It must not be
confused with this residue field of dimension four.

**Proposition 1 (automatic valuation from the previous moments).** For a binary
preimage of a valid length-15 intermediate pair satisfying the previous moment
conditions, v(S)>=9. No length-nine compression assumption is needed.

**Proof.** Let Delta(z) be the full binary PAF defect polynomial, with zero
constant coefficient. The moments say Delta=12T for T in Z[z]. The exact
length-15 compression says z^15-1 divides Delta. Monic division therefore
gives T=(z^15-1)R with R integral. Evaluating at zeta gives
`4S=12*(omega-1)*R(zeta)`. Thus S=3*(omega-1)*R(zeta), with valuation at
least 6+3=9. QED.

The same proof applies at every prime above three for length 9p, p>3 prime,
using a valid length-3p compression, the moment congruences, and target
(9p+1)/2. The relevant valuations are still v(3)=6 and v(1-omega)=3.
This is an elementary consequence of the established compression identity;
no priority claim is made.

The selected condition S in 9O demands v(S)>=12, so it genuinely strengthens
this automatic bound. Necessity and gauge invariance are rigorous: layer
translations multiply F by units of complex norm one, and the common kernel
multiplier is a Galois automorphism. The ideals (9), (23), and the unique prime
above three are invariant under these operations.

Exact valuations were computed by integral division, with no numerical roots:

`1/pi = (sum_(j=0)^7 (8-j)*zeta^(5j))/9`.

Multiply, reduce in the degree-24 integral basis, and divide by nine only when
all coefficients are divisible. Tests verify this inverse and the valuations
of powers of pi and of three and nine.

## 3. Explicit counterexamples, including the saved stronger challenge

The previously saved branch-279 witness
`(22964264347100,2872821395978)` has v(S)=10. It passes the moments and both
compressions, but fails modulo nine. Its exact S coefficients are retained in
the new evidence, cross-checked against the existing binary PAF spectral code.
Rejecting this one point would not establish an empty-fiber theorem.

The selected obstruction fails on another **already saved** branch-279 phase
assignment (free index 950761 in `results/phase_moments/rank_279.json`):

```
masks = (442312790436,2830005805622)
a = (0,0,0,0,2,0,1,1,1,2,1,1)
b = (0,0,0,2,2,0,1,2,1,0,1)
```

Masks mean x_i=1-2*((mask>>i)&1). These are actual binary preimages of C,D279,
already in the third gauge. Their length-nine compressions are

```
U = ( 1,1,-1,-1, 1,1,-1,-3,3)
V = (-3,1,-1,-1,-3,1,-1, 3,5)
```

Their combined energy is 82 and each nonzero combined PAF is -10. All phase
moments and ordinary cycle identities hold, including the correct layer
carries in adjusted differences. Nonetheless

`S = 9*(2-z^6+2*z^9-2*z^12+z^15+z^18-3*z^21)` at z=zeta.

This nonzero reduced polynomial has v(S)=12, so passes modulo nine and fails
at the next prime-ideal level. For example its binary PAF sum at shift three
is 22 rather than -2. At nonredundant shifts the other defects occur at 6,9
(PAF 10), 12,18 (PAF -14), and 21 (PAF -26); other shifts have PAF -2.

This is a counterexample to sufficiency of **moments + both exact compressions
+ modulo-nine primitive norm + all phase cycles + the third gauge**. It is not
a Legendre pair and not a counterexample to necessity. It also proves that
no consequence of just those conditions can contradict every branch-279
assignment. This logical limitation does not depend on exhaustive evaluation.

## 4. Screening 23: failure of a divisibility shortcut, then saturation

The Frobenius orbit generated by 23 modulo 45 has length twelve and does not
contain -1: modulo five an exponent giving -1 must be 2 mod 4, whereas modulo
nine it must be 3 mod 6. Thus Phi_45 modulo 23 has two irreducible degree-twelve
factors exchanged by conjugation. The prime is not self-conjugate in this
cyclotomic field. The fact 23=3 mod 4 does **not** make a sum of two cyclotomic
complex norms anisotropic modulo 23.

An explicit check avoids relying only on terminology. Set

`T=z^3+z^6+z^12-z^21+z^24-z^33-z^39-z^42` at z=zeta.

Reduction modulo Phi_45 gives conjugate(T)=-T and T^2=-15. Hence unrestricted
field elements F=1, G=7T satisfy

`F*conjugate(F)+G*conjugate(G)=1+49*15=736=32*23`.

Both are units modulo 23 since G^2=1 there. This refutes an unrestricted
inference from norm-sum divisibility to divisibility of both summands. These
are **not** claimed to have the prescribed indexed supports or ternary phases.
They do not establish branch-279 feasibility modulo 23. Conversely,
self-conjugate single-norm theorems cannot be transferred to this sum without
additional hypotheses.

For the actual indexed phase problem, modulo 23 is already too strong to be
a coarse substitute for exact arithmetic, once the moments have been imposed.

**Proposition 2 (coefficient reconstruction, with explicit hypotheses).**
Let S=sum s_k*zeta^k, 0<=k<24. If S is in 3O and |s_k|<69 for every k, then

`S in 23O if and only if S=0`.

**Proof.** The powers 1,zeta,...,zeta^23 form an integral basis. Membership in
mO means every integer coefficient is divisible by m. Thus membership in both
3O and 23O forces each s_k to be a multiple of 69. The strict bound forces
each to vanish. The converse is immediate. QED.

Here the bound holds for **every** allowed phase assignment in either branch,
without imposing cycles, gauges, moments, or other constraints. There are
23 active entries, so the diagonal norm terms cancel the target. For each
unordered same-row pair i<j and h in {0,1,2}, reduce

`C_i*C_j*(z^(j-i+15h)+z^(-j+i-15h)) mod Phi_45`.

For each basis coefficient sum the minimum, respectively maximum, of its
three possible values over all pairs. This independent-edge relaxation gives
rigorous lower and upper bounds even though edge choices are coupled. The
maximum absolute bounds are **53 for 277 and 54 for 279**. Full 24-coordinate
bounds are saved in `audit.json`; computing them involves 121 unordered edges
per branch, not phase enumeration. The formula, displayed rows, and modulus
specify a finite arithmetic certificate for the bounds.

Moments give S in 3O by Proposition 1, so Proposition 2 applies. With both
compressions imposed, the standard Galois reduction then makes the modulo-23
test equivalent to the remaining full lifting condition. Observing that it
rejects the saved empty-branch assignments is therefore no new explanation.

The elementary generalization is: if S is in mO, gcd(m,l)=1, and every integral
basis coefficient has absolute value <m*l, testing S in lO is exact. It applies
to other signed supports when the same explicit edge-bound hypothesis holds;
no claim that it holds for all branches or lengths is made.

## 5. Small saved-space diagnostic and positive validation

No new phase space was enumerated. A 50-record pilot estimated the local audit
at 35.0 seconds with a tenfold margin; the final audit of the 1,474 previously
saved moment solutions took 2.81 seconds on one worker.

| Branch | Saved moment records | v=9 | v=10 | v=11 | v=12 | S=0 | Pass mod 9 |
|---|---:|---:|---:|---:|---:|---:|---:|
|277|734|648|78|6|1|1|2|
|279|740|666|61|9|4|0|4|

Exactly one of the four branch-279 modulo-nine records has the correct
length-nine compression PAFs: the counterexample in Section 3. These are
finite diagnostics on a frozen complete modular list. In particular, saying
that v>=13 rejects all its records is a **finite evaluation result**, not a
structural proof or a new emptiness result. We did not launch a higher-power
search, a solver, or another full lifting census.

All 2,976 frozen p=5 positive pairs were covered after the third gauge. There
are 992 distinct gauged pairs; each was checked using direct signed-polynomial
multiplication and the independent existing binary-PAF cyclotomic calculation.
Every S is zero. A 25-pair positive pilot estimated 19.3 seconds with a fivefold
margin. Verification including integrity checks took 10.89 seconds. This is
local validation with two arithmetic formulations, **not external replication**.
The p=7 artifacts were preserved but no p=7 arithmetic was run in this round.

## 6. Reassessment of traces, cycles, and the next precise target

**Proposition 3 (why the first trace adds nothing here).** If a normalized
binary length-45 pair has both required compressions, then Tr_(Q(zeta)/Q)(S)=0.

**Proof.** The two compressions fix all nonprimitive PSDs. Parseval gives total
pair PSD 45*90=4050. The zero frequency contributes two; the twenty other
nonprimitive frequencies contribute 20*92. The twenty-four primitive
frequencies therefore contribute 4050-2-20*92=24*92. Their defects are 4 times
the Galois conjugates of S, so their sum is 4 Tr(S)=0. QED.

This generalizes immediately when all nonprimitive PSDs are fixed at their
Legendre targets. It is a Parseval consequence, not a new obstruction.

With u_i=omega^(a_i), every pure cycle product of edge differences telescopes
to one. Both false positives already have globally assigned u_i. Consequently
adding more such cycle identities of any degree cannot reject these points.
A useful cycle-based argument would have to couple indexed signed correlation
balances to these identities; ordinary cycle consistency alone is exhausted.

The quartic invariant Tr(S^2), of degree at most four in u_i and their
conjugates, is positive for every nonzero S, since S is totally real. For the
new counterexample it is 9720 although Tr(S)=0. Imposing Tr(S^2)=0 is equivalent
to S=0 and by itself merely restates the exact primitive test. No structural
positive lower bound for branch 279 was proved. The general quartic expression
contains products of edges, not only single graph cycles, so calling it a
new signed-cycle obstruction would also be premature.

**Strongest next target:** on the modulo-nine domain derive, directly from
the indexed signs and exact compression balances, a short identity for

`J = (S/9) mod (pi) in F_3[alpha]/(Phi_5(alpha))`.

For the new false positive J=1+2*alpha^2+2*alpha^3, which is nonzero; for the
frozen positive it is zero. Since v(9)=12, J=0 is exactly the next condition
v(S)>=13 on this domain. The four saved branch-279 modulo-nine points have
nonzero J, but that observation is not the desired proof. A useful theorem
would give explicit structural support/sign hypotheses forcing J!=0 from
the balance equations, with a derivation valid beyond one enumerated list.
The bounds and counterexample above do not supply those hypotheses. Even
bounded-degree expressibility after division by nine must be justified:
integer carries cannot simply be discarded in a polynomial over F_3.

Thus a bounded-degree signed-balance approach is a precise research target,
not yet a proved obstruction, justified algorithm, or originality claim.

## 7. Primary literature and access limits

Accessed October 14, 2026; no authors contacted. Only the listed portions are
claimed read. Existing source gaps in the publication audit remain open.

* Keith Conrad, [Cyclotomic extensions](https://kconrad.math.uconn.edu/blurbs/galoistheory/cyclotomic.pdf),
  author-hosted full PDF, printed pp.10--11: Theorem 5.3, equation (5.1),
  Theorem 5.4 and Example 5.5. These give the prime-power Eisenstein identity,
  reduction of cyclotomic polynomials modulo a ramified prime, and degrees of
  irreducible factors via multiplicative order. Our computations at 3 and 23
  specialize these established facts. The exact polynomial and inverse checks
  are supplied independently in the code.
* Romanos D. Malikiosis, [Formal duality in finite cyclic groups](https://arxiv.org/pdf/1704.04183),
  primary preprint, Section 8, Definition 8.1, its following decomposition-group
  discussion, and Theorem 8.2 (printed p.24, PDF page index 23). This explicitly
  attributes self-conjugacy techniques to Turyn and states a single-norm
  divisibility theorem under self-conjugacy. We checked these hypotheses;
  they do not authorize the proposed two-norm shortcut at 23. The cited
  original Turyn source was not newly obtained or read this round.
* Turner et al., [Legendre pair of length 77 using complementary binary matrices with fixed marginals](https://arxiv.org/pdf/2101.10918),
  primary preprint, Theorem 3.4 and Corollary 3.5, printed pp.11--12, plus the
  paragraph immediately after the corollary. These explicitly reduce the
  remaining condition after simultaneous complementary compressions to the
  primitive PSD equation. Full relevant statements and proof were accessible.

Targeted searches for Legendre-pair modulo-nine conditions and cyclotomic
norm-sum obstructions did not provide a primary proof specific to these
conditional branches. This is not evidence of absence or priority. The full
fast-spectral and pq-squared algorithm gaps and the unpublished Craigen
modulo-three manuscript gap from earlier notes are unchanged; this round
does not claim to have read them. No novelty claim follows from this search.

## 8. Reproduction, integrity, and limits

From the repository root, Python 3.14.6 on Windows 11:

```powershell
.venv/Scripts/python.exe -m scripts.primitive_local_audit pilot
.venv/Scripts/python.exe -m scripts.primitive_local_audit audit
.venv/Scripts/python.exe -m scripts.verify_primitive_local
.venv/Scripts/python.exe -m pytest tests/test_primitive_local.py -q -p no:cacheprovider --basetemp=tmp/pytest_primitive_local
.venv/Scripts/python.exe -m scripts.package_primitive_local
```

Only the new `results/primitive_local/` directory is written. All inherited
6,734 result files and every paper file remain unchanged. The verification
checks the preceding frozen aggregate and every preceding manifest entry,
then checks Git against the specified baseline. Ordered path/content SHA-256
digest for all 6,734 baseline result files:

`707e7159bd381fff325b4946fd94998df84212d2abc14fc30220e43c878f5169`.

Unchanged manuscript SHA-256:

`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.

Input hashes, script hashes at execution, complete reduced coefficients,
valuations, survivor witnesses, resource estimates, and runtime provenance
are in the new JSON records. `manifest.json` pins the new notes, scripts,
tests, and evidence. All polynomials use ascending coefficient order. The
four tests passed in 1.27 seconds, including random unconstrained phase
cross-checks to test the formula outside the saved modular solutions.

The Python launcher emitted a location diagnostic but every reported run
completed with exit code zero. Final computational runs used one worker,
a 120-second internal audit cap, conservative 100 MB memory estimates, and
under 5 MB estimated evidence storage. Memory was estimated, not measured.
No cap or timeout was hit. No run approached the user's four-core, thirty-
minute, or 10 GB limits. Preliminary arithmetic pilots were repeated only
after the new audit code acquired input-hash provenance and valuation checks,
and to serialize the new JSON with explicit LF line endings so committed
artifact hashes remain portable across checkouts;
no inherited experiment was repeated or overwritten.

No new explanatory contradiction, structural nonvanishing theorem for J,
external replication, or substantive original contribution is established.
The narrower paper assessment and all prior submission gates are retained.
