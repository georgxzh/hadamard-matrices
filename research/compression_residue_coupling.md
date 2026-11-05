# Exact compression coupling and a limitation of affine interval bounds

Research round: October 15, 2026. Base
`aff70e5307492a65b61fddfabed92634edb6788f`, branch
`agent/order-428-reproduction`. The initial tree was clean. No child AGENTS.md
or CLAUDE.md files were found. Read the residue-carry, primitive-local and
phase-moment notes, the signed-phase and propagation implementations, exact
cyclotomic arithmetic, and the frozen branch/witness evidence. In particular,
the propagator already enforces shared differences and triangle consistency.
These are not new constraints proposed in this round.

**Outcome:** no explanatory empty-fiber theorem or substantive original
breakthrough was obtained. There are two proved refinements: an exact
compression-domain equivalence retaining all of S in 9O, and an explicit
support/sign lemma ruling out the selected class of affine interval arguments.
The latter is a limitation of a proof strategy, not a proof of emptiness.
It has actual globally consistent phase assignments behind it; it is not
an infeasibility status or a new enumeration of the conditional fiber.
Originality is not established. The narrower reproducibility/software paper
assessment remains, and the manuscript was neither edited nor compiled.

## 1. Indexed variables and the exact length-nine equations

Use precisely the rows, active supports, signs, and third gauge of
`primitive_local_obstruction.md`, Section 1. For either fixed row c of length
15 write b_i=sign(c_i), d_i=-2b_i on active positions and zero otherwise.
Then x[i+15k]=b_i+d_i[k=a_i], a_i in {0,1,2}. In the concatenated list of 23
active phases, indices 0,1,12 are zero. We make no further gauge choice or
permutation of the indexed entries.

The directed events from `residue_carry_formula.md` are retained verbatim:
for s=r+15l, 1<=r<15, j=(i+r) mod 15 and h=floor((i+r)/15),

    Y_(i,j,s) = [a_j-a_i-h-l = 0 (mod 3)],
    E_s = sum_(both rows, directed active edges) b_i*b_j*Y_(i,j,s),
    B_s = E_s-t_r,                 t_r=(-2-K_r)/4.

Here K_r=sum(3b_i b_j+d_i b_j+b_i d_j) is an integer. Set B_0=B_15=B_30=0.
Exactly, B_s=(PAF_x(s)+PAF_y(s)+2)/4 off zero. Fixed valid intermediates give

    B_s=B_(45-s),       B_r+B_(r+15)+B_(r+30)=0.                 (1)

Define the nine integer folding balances

    G_t = sum_(k=0)^4 B_(t+9k),             0<=t<9.             (2)

Writing X_j=sum_(k=0)^4 x[j+9k], and similarly Y for the other row, gives

    sum_j (X_j^2+Y_j^2) = 82+4G_0,
    PAF_X(t)+PAF_Y(t)   = -10+4G_t,             1<=t<9.         (3)

Proof: expand the compressed products and collect differences modulo 45.
The result is the sum of the five original PAF values at shifts t+9k. For
t=0 the targets sum to 90-4*2=82; otherwise they sum to 5*(-2)=-10. This is
the standard compression identity, here applied to the defect balances.
Thus exact length-nine energy and PAF are equivalent to **G_t=0 in Z**.
The row sums are already one from the prescribed intermediates.

In exactly the original phase events these equations are

    G_t = -sum_(s=t mod 9) t_(s mod 15)
          +sum_(s=t mod 9) sum_(i,j active) b_i*b_j*Y_(i,j,s)=0, (4)

omitting s=0,15,30. In particular, all integer signs, h, and l remain present.
There is no reduction modulo three in (2)--(4).

Only three equations are needed. By (1),

    G_0 = 2(B_9+B_18),
    G_1 = B_1+B_8+B_10+B_17+B_19,
    G_2 = B_2+B_7+B_11+B_16+B_20,
    G_0+2G_3=0,      G_1+G_2+G_4=0,      G_t=G_(9-t).         (5)

For the fourth relation use B_3+B_12=-B_18 and B_6+B_21=-B_9;
the fifth follows by summing all B_s=0 and using symmetry. Consequently
G_0=G_1=G_2=0 is exactly equivalent to all nine equations, on (1).
Dropping the energy equation without these relations would not be justified.

### The same equations as signed minority-charge balances

This gives a second expansion that displays the indexed interactions. For
i=r+3m_i, r in {0,1,2}, put

    beta_r = sum_(i=r mod 3) b_i,
    L_i = (m_i+5a_i) mod 3,
    M_(r,q) = sum_(i active, i=r mod 3) c_i*[L_i=q].

There are five baseline contributions at each compressed coordinate, and
the minority in column i lands at i+15a_i = r+3(m_i+5a_i) mod 9. Hence

    X_(r+3q) = beta_r-2M_(r,q).                                (6)

For a shift t let r'=(r+t) mod 3 and H=floor((r+t)/3), keeping H as an
integer before reducing q+H modulo three. The combined PAF, including energy
at t=0, is the sum over both rows, r and q of

    beta_r beta_r' -2 beta_r M_(r',q+H)
    -2 beta_r' M_(r,q) +4 M_(r,q) M_(r',q+H).                 (7)

Equate this integer to 82 for t=0 and -10 otherwise. Expanding the last
product and summing q turns its indicators into
[L_j-L_i=H mod 3], equivalently
[j-i+15(a_j-a_i)=t mod 9]. Collecting these directed pairs gives (4).
This proves agreement, including diagonal terms and boundary carries.
The M variables are signed integer charges, not unsigned counts or their
residues. Their products show precisely the interactions that a relaxation
to separate phase or margin profiles would lose. At the modular level an
event indicator has a quadratic F3 representation; this does not authorize
reducing (7) before an integer division or imposing only its congruence.

## 2. Exact relations with Q_0 and Q_2

Use U_r, Q_r=U_4-U_r and the five three-shift sets from the residue note.
In nonredundant shifts,

    U_4=B_1+B_4+B_6,
    Q_0=U_4-B_5-B_10,
    Q_2=U_4-B_12-B_17-B_22.                                   (8)

The union of the five U slices is the set s mod 9 in {3,4,8}. Thus, exactly,

    sum_(r=0)^3 Q_r
      = 5U_4-(G_3+G_4+G_8)
      = 5U_4+G_0/2+G_2.                                      (9)

G_0 is even by (5); the division here is in Z. Equations (4),(8),(9) explicitly
couple the very same indexed signed events, rather than identifying only
their margin profiles. They do not by themselves force a nonzero residue.

On the full 9O domain, Q_1=0 mod 9 and Q_3=Q_2 mod 9 by conjugation.
When G=0 as well, Section 3 proves that every B_s is divisible by three.
Set k_s=B_s/3 and A=k_1+k_4+k_6. With u=Q_0/3 mod 3 and v=Q_2/3 mod 3,
division of (9) in the integers gives

    u+2v=5A mod 3,       equivalently v=u+A mod 3.             (10)

Together with (8), joint vanishing is equivalent, on this full domain, to
A=0 and k_5+k_10=0 modulo three. This is a useful coordinate identity, **not**
the desired obstruction. We do not count this reformulation as an explanation
of emptiness or assert that its right-hand side cannot vanish for branch 279.

## 3. A justified reduced form of the FULL divisibility condition

**Proposition 1.** Let an integer defect array B satisfy both exact compression
maps: sum_(s=r mod 15)B_s=0 and sum_(s=t mod 9)B_s=0. Let
S=sum B_s zeta^s. Then

    S in 9Z[zeta]  <=>
    B_r = B_(r+15) = B_(r+30) (mod 9), for every r mod 15.      (11)

Either side implies every B_s is divisible by three. This proposition does
not replace the domain by divisibility of just Q_0,...,Q_3 by three.

Proof. In the integral tensor basis of the preceding residue note write
H_(r,e)=B_s for s mod 5=r and 2s mod 9=e. For v<6 let j=6+(v mod 3) and
T_r=H_(r,v)-H_(r,j), for all five r. The exact basis coefficient is
A_(r,v)=T_r-T_4 for r<4. These 24 coefficients are divisible by nine iff S
is in 9O. The length-nine compression gives sum_r H_(r,e)=0 at every e, so
sum_r T_r=0. If A=0 mod 9, all five T_r are congruent. Since 5 is invertible
modulo nine, each T_r=0 mod 9. Conversely, that condition directly makes all
A_(r,v) zero modulo nine. This says that the three entries of H at fixed r
and fixed e mod 3 are congruent. The CRT identifies each such triple with
s=r0,r0+15,r0+30, giving (11). Their exact sum is zero by the length-15
compression; hence 3B_r=0 mod 9, proving 3 divides B_r. QED.

Thus the old moment conditions are automatic when both compressions and
the full 9O condition hold. There is no need to assume them separately on
this restricted domain. We still verify all 24 integral coefficients in
the implementation and cross-check (11), rejecting its use without the
exact compression hypotheses. Q-divisibility alone remains insufficient:
the saved witness (22964264347100,2872821395978) has both exact compressions
and Q=(-3,0,-3,6), but is outside 9O and fails (11).

The proof extends to L=9p, prime p>3, with exact compressions of lengths 3p
and nine. Use the p by nine tensor array from the residue note: sum_r T_r=0
and p invertible modulo nine replace the five-row step. The criterion is
B_s=B_(s+3p)=B_(s+6p) mod 9, and each B_s is divisible by three. This is an
elementary lattice consequence of compression, not a new norm or Galois
principle. No binary searches at other p were run.

## 4. Selected candidate: an affine interval bound, and why it fails

We selected the following precise sufficient route before generating any new
assignments. Choose integers lambda_0,lambda_2, not both zero modulo three,
and small integer multipliers mu_0,mu_1,mu_2. Form

    R=lambda_0 Q_0+lambda_2 Q_2+mu_0 G_0+mu_1 G_1+mu_2 G_2.    (12)

Seek a rigorous integer interval for R on the whole third-gauged phase cube
that contains no multiple of nine. On G=0 and the full 9O domain, J=0 implies
R=0 mod 9, so such a bound would prove the requested obstruction. Each term
in (12) is a small signed combination of exact phase events. Merging shared
events before taking bounds could in principle reveal the differing indexed
D supports of 277 and 279. This is a candidate proof strategy, not a claim
that the interval exists.

First the saved positive and five other 9O witnesses were evaluated, together
with the saved out-of-domain witness. Their outcomes are in Section 5. We
then challenged the *strategy* analytically instead of searching coefficients
or rerunning known empty fibers. The following explicit lemma defeats it,
even if its unconditional interval bounds are computed with all cycle relations.

**Proposition 2 (opposite-edge cancellation).** Suppose the fixed C anchors
are active at positions 0 and 1 with equal signs; D has active adjacent
positions j,j+1 with opposite signs. Retain the first active D anchor at zero.
For a valid intermediate pair, zero belongs to the convex hull of the full
integer B vectors of genuine third-gauged phase assignments.

Proof. Fix the two C phases to zero. Give every other active C position an
independent uniform ternary phase. In D impose a_j=a_(j+1). If one endpoint
is the fixed D anchor, set both to zero; otherwise give the shared phase an
independent uniform value. All remaining unfixed D phases are independent
uniform. Every within-row phase difference is uniform except the one fixed
C edge and the one equal-phase D edge. For those edges the difference is
zero. The two edges have identical indexed displacement and opposite sign
products. Their deviations from the uniform event probability 1/3 cancel
at every lifted shift, also for the reversed orientation with its carry.
Every other edge contributes its signed weight divided by three. Since
sum of weights at a base shift is 3t_r, the mean of E_s is t_r and the mean
of every B_s is zero. Every sample is an actual phase assignment with the
prescribed signs, supports and gauge, so its differences satisfy all cycles.
Taking expectations proves the convex-hull assertion. QED.

For 277 the cancelling D edge is (1,2), with signs (-1,+1); for 279 it is
(2,3), with signs (+1,-1). The C edge is (0,1), with signs (-1,-1). Thus
**both branches satisfy explicit hypotheses of the lemma**. It extends to
any valid length-15 intermediate pair with these anchor and edge hypotheses,
regardless of other sign counts. An analogous statement holds for a common
nonwrapping displacement d and opposite sign products, when those are the
only forced equal-phase pairs. No generality for arbitrary gauges is assumed.

It follows that the mean of R in (12) is zero for every lambda and mu.
Therefore min R <= 0 <= max R. Every enclosing interval contains the multiple
of nine zero. This rules out **all** multiplier choices for this strategy,
not merely a finite unsuccessful scan of small coefficients. There was no
reason to launch an optimization or exhaustive bound calculation.

This is deliberately a limited negative result. It does NOT exclude modular
identities, conditional bounds valid only after G=0 and S in 9O, or arguments
using products of events with those pointwise constraints. Nor does taking
the mean commute with dividing S by nine to form J on its domain. Integer
division, congruence membership and intersection with G=0 cannot be replaced
by satisfaction at the mean. In particular, the barycenter is not an allowed
conditional lifting witness. Its role is to refute the proposed unconditional
affine interval mechanism, not to refute the desired nonvanishing statement.

### A small exact realization, not a lifting enumeration

The proof only needs uniform differences, so it can be realized with 27
assignments instead of enumerating independent phases. Choose distinct
projective directions in F3^3 (first nonzero coordinate normalized to one),
and use their scalar products with a seed z in F3^3 for each unfixed phase
factor within a row. Distinct directions have a nonzero difference, making
each such difference uniform as z runs over 27 seeds. Use zero directions
for the fixed anchors, and the same direction for the selected D pair.
There are 13 directions, enough for the ten C factors and at most nine D
factors. Reuse directions between rows, since no cross-row PAF edges occur.

The new evidence lists all seeds via lexicographic order, direction maps,
phases, masks, B, G, Q, integral S, charges and domain flags for both branches.
Their B, G, Q and S sums are exactly zero. None of these 54 design members
satisfies exact length-nine compression, and none belongs to 9O. These last
counts are validation of the design's limits, not evidence of emptiness.
The mathematical explanation is the two opposite signed edges, not the list.

## 5. Saved challenges and information lost under relaxation

All six previously saved 9O witnesses were used, plus the earlier outsider.
Only the first three independent G coordinates are shown here:

| branch; first mask (second in the JSON) | (G0,G1,G2) | J=(u,0,v,v) |
|---|---|---|
|277; 22487656929184| (0,0,0) | (0,0,0,0) |
|277; 18570512807384| (0,6,-3) | (0,0,1,1) |
|279; 31210651353580| (0,6,-3) | (0,0,1,1) |
|279; 416258831260| (6,0,0) | (1,0,1,1) |
|279; 428621558224| (0,3,3) | (2,0,0,0) |
|279; 442312790436| (0,0,0) | (1,0,2,2) |
|279; 22964264347100| (0,0,0) | undefined: S not in 9O |

The required positive has zero B. The required strong false positive
(442312790436,2830005805622) has exact compressed energy 82 and all eight
compressed PAF sums -10. It still has J=1+2alpha^2+2alpha^3. Its A in (10)
is one, and v=u+A=2 as predicted.

The saved counterexample (31210651353580,20580563788346) has u=0, v=1 and
passes the FULL 9O domain. It satisfies G=0 modulo three, while its actual
compressed PAF sums are (14,-22,-10,-22,-22,-10,-22,14). Therefore replacing
exact compression by its modulo-three balance equations admits this genuine
counterexample to the single-coordinate claim u!=0. All six 9O witnesses
have G divisible by three; their differing integer G values matter. This
counterexample does not refute joint nonvanishing under exact compression.

The earlier outsider has all Q divisible by three and both exact compressions,
but no J. This directly challenges the other tempting relaxation. Conversely,
the new barycenter satisfies B=G=Q=S=0 only on average: it discards pointwise
integer information even while its samples retain all phase cycles. These
are three different losses of information and should not be conflated.

## 6. What remains open and the strongest next mathematical target

The conditional branch-279 assertion u and v not both zero remains unproved
structurally. The inherited enumeration supports separation, but it was not
rerun or used as an explanatory argument here. We did not select the one
saved exact-compression survivor as a purported proof.

The proved advance is a sharper domain description and a checkable reason
that one tempting class of small signed-balance inequalities cannot work.
It goes beyond reporting solver outcomes, but does **not** achieve the primary
research goal of a useful original empty-fiber theorem. Proposition 1 is
elementary tensor arithmetic; Proposition 2 uses a standard averaging idea.
Neither warrants changing the manuscript or publication assessment now.

The strongest justified next target is a **pointwise integer charge lemma**:
use (6)--(7), the triple congruences (11), and the fixed indexed signs to
constrain the simultaneous values of A=k1+k4+k6 and k5+k10, rather than bound
an unconditional affine combination. An argument must retain which signed
minorities occupy each residue-three layer and their original positions
modulo five. One concrete way to investigate this is to multiply a compression
balance by a selected signed phase event before collecting terms; on exact
compression Y_e*G_t=0 pointwise. These involve pairs of events and do not
follow from satisfying G_t only in expectation. Such products could expose
the absent interaction, but no particular product identity or nonvanishing
claim has been established. The mean-zero design proves that unconditioned
first-event information will not suffice for the selected interval strategy.
Adding pure cycle consistency again would address nothing missing here.

## 7. Primary literature, access limits and originality

Checked October 15, 2026. The following accessible primary portions were read:

* Djokovic and Kotsireas, [Compression of Periodic Complementary Sequences
  and Applications](https://arxiv.org/html/1302.0571), Section 5, Definition 3,
  equation (18), Theorem 3, equation (19), and its proof. These give precisely
  the PAF folding identity underlying (3). Our phase-event expansion is a
  specialization, not a new compression theorem.
* Turner et al., [Legendre pair of length 77 using complementary binary
  matrices with fixed marginals](https://arxiv.org/pdf/2101.10918), Theorem
  3.4 and proof, Corollary 3.5 and subsequent discussion, printed pp.11--12.
  Galois propagation and the remaining primitive-frequency test after
  complementary compressions are established; our domain reduction does
  not claim either principle as original.
* Kaji, Maeno, Nuida and Numata, [Polynomial Expressions of Carries in p-ary
  Arithmetics](https://arxiv.org/pdf/1506.02742), Section 3.1, Remark 1,
  printed p.6. The generating-function carry precedent from the previous
  round remains directly relevant; no new degree-six or carry principle is
  claimed in this round.
* Michel, Taubenfeld and Berman, [A Connection Between Random Variables and
  Latin k-cubes](https://faculty.runi.ac.il/gadi/MyPapers/1995MTB-random.pdf),
  author-hosted full PDF, introduction and Section 3.1, Connection Theorem
  and Lemma 1 with proof, printed pp.1--4. Small finite sample spaces and
  independence via arrays are established. Our 27-point construction has
  its own elementary linear-form proof above; no novelty claim for the
  probability-space construction follows.

A targeted search also returned the publisher listing for
[On properties of Legendre pairs under compression](https://doi.org/10.1145/3747199.3747549).
Opening it again returned HTTP 403. Search snippets were not used to infer
its full algorithms or priority. The prior unavailable full-algorithm and
historical-list gaps remain unresolved. No authors were contacted. This
search is not a proof that either specialization is absent from the literature.

## 8. Commands, provenance, resource limits and preservation

From the repository root:

```powershell
.venv/Scripts/python.exe -m scripts.audit_compression_residue pilot
.venv/Scripts/python.exe -m scripts.audit_compression_residue audit
.venv/Scripts/python.exe -m pytest tests/test_compression_residue.py -q -p no:cacheprovider --basetemp=tmp/pytest_compression_residue
.venv/Scripts/python.exe -m scripts.package_compression_residue
```

The three-record pilot took 0.03324 seconds, projecting 3.38 seconds for
61 checks with a fivefold margin. The seven saved checks and 54 fixed design
checks took 0.156 seconds on one worker. Four focused tests passed in 0.22
seconds. They include 90 synthetic integer compression-lattice checks against
the independent standard cyclotomic reduction, direct binary/compressed PAF
cross-checks in the audit, witness rejection checks, and verification that all
other within-row differences in the design are exactly uniform. None is a
new lifting census or a claim of external independent replication.

The internal audit cap was 60 seconds; conservative memory and storage
estimates were 100 MB and 1 MB. Memory is an estimate, not a measurement.
No cap was hit; the calculations used one worker and remained far below
four cores, thirty minutes per run and 10 GB. The known Python launcher
location diagnostic appeared; all reported commands exited zero.

New output is confined to `results/compression_residue/`; input hashes are in
the audit, and the final manifest pins new source, tests, notes and evidence.
The package checks preceding manifests, the previous 6,741-file raw-byte
aggregate, and Git-blob SHA-256 hashes for all 6,748 inherited result files
and all inherited paper files. A stricter initial Git-blob comparison exposed
legacy CRLF bytes in two old artifacts: the projected-uncompression solver
probe and `ternary_phase/p7_acquisition.json`. Those bytes were preserved,
not normalized: the old raw aggregate verifies them, and the package
separately records local and Git-LF hashes for these exceptions.
It also requires that no previously tracked file was changed. The unchanged
manuscript SHA-256 is
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.
No manuscript compilation was requested or performed in this exploratory
round. No claim concerning PDF layout or submission readiness is added.
