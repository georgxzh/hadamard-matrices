# Signed triangle trades and a three-active-position charge obstruction

October 17, 2026. Base `f92a7b3740e4b301a9574b8ae7e61fd9c0dd7bac`,
branch `agent/order-428-reproduction`. Initial tree clean; no child agent
instruction files found. Read the previous exchange-rigidity, compression/
residue and carry notes, exact phase/event implementation, phase propagation,
and frozen evidence. New work is separate; the manuscript is unchanged.

**Outcome.** The two-position proof survives scrutiny. All three-position
charge trades are signed directed triangles. A proved support-and-charge
obstruction excludes their necessary six-edge saturation under the explicit
hypotheses in Section 4. This is a general conditional rigidity mechanism,
not an explanation of the entire empty branch 279. The bounded audit found
14 permitted neighbors, all outside 9O. Originality remains unestablished.

Throughout, p is a prime greater than three, N=3p, zeta is primitive of
order 9p, omega=zeta^N, and O=Z[zeta]. Active positions have fixed signs
c_i in {+1,-1}; inactive intermediate entries are +3 or -3. The primitive
norm defect is S=F_C*bar(F_C)+F_D*bar(F_D)-(9p+1)/2. For p=5 this is the
previous S with constant 23. At nonzero shifts B_s=(PAF_C(s)+PAF_D(s)+2)/4;
only differences D=B'-B are needed here. The shift-zero difference is zero.
All uses of (1) require both exact homogeneous compression equations, not
merely preservation of a modular marginal.

## 1. Independent scrutiny of the preceding proof

No correction to the two-position theorem was found. Its hypotheses matter:
fixed factor-three intermediates, active signs of magnitude one, odd N=3p,
and equality of the full integer compressed PAF/energy data. At a fixed
nonzero base difference r, a changed vertex affects only its incoming and
outgoing directed edge. The union for two vertices has at most four edges;
an edge with both endpoints changed is counted once. Each signed indicator
difference is in {-1,0,1}. Shifts 0,N,2N are phase independent. Thus the
four-edge bound is valid; it does not require unchanged edge differences
between the two moved vertices.

For D=B'-B, fixed intermediates give sum_(l=0)^2 D_(r+Nl)=0. Equal compressed
PAFs and energy give sum_(s=t mod9)D_s=0. These are homogeneous equations
even if neither endpoint meets the Legendre compression target. The tensor
basis argument applies to D, not to an endpoint with failed compression.
The integral basis is justified by writing zeta=gamma^a*t^b for coprime
orders p and nine: the (p-1)*6 products gamma^u*t^v span integrally by the
two monic cyclotomic relations and are independent by the field degree.
The coefficient differences T_u-T_(p-1) are zero mod9 iff all p T_u agree
mod9; their zero sum and gcd(p,9)=1 make all zero mod9. Consequently

    Delta S in 9O iff D_r=D_(r+N)=D_(r+2N) mod9.              (1)

Together with |D_s|<=4 and the exact triple sum this proves D=0. Neither
Q-divisibility nor compression modulo three is a substitute. All of these
hypotheses were present in the earlier theorem; this section makes the
integral-basis and difference-domain steps explicit before building on it.

## 2. Complete classification before computation

Write i=r+3m_i, L_i=m_i+p*a_i mod3, with p=5 for the audit. Each changed
phase has a nonzero landing increment because p is invertible modulo three.
For an active sign c_i=+1 orient an arc L_i->L_i'; for c_i=-1 orient it
L_i'->L_i. Integer charge preservation is exactly zero net incidence at
each of the three landing labels, separately for each (row,r) group.

A single loop-free arc cannot balance. Thus exactly three changes cannot
be split between groups (a split leaves a singleton). All three lie in
one row and one residue class. A balanced directed multigraph with three
loop-free arcs is a directed triangle: follow an arc until a cycle closes;
a two-cycle would leave an unbalanced singleton, so the cycle has length
three and uses all arcs. This proves the classification without a sign
restriction or enumeration.

There is epsilon in {+1,-1} and a bijection i->t_i from the changed triple
P to {0,1,2} such that

    L_i = t_i + (1-c_i)*epsilon/2,
    L_i'= t_i + (1+c_i)*epsilon/2,
    delta_i=a_i'-a_i=p^(-1)*c_i*epsilon mod3.                 (2)

Here (1+-c_i)/2 is an integer 0 or 1, not modular division of a charge.
The converse follows by summing the three directed triangle arcs. Formula
(2) covers all eight sign patterns. Equal signs give the familiar label
three-cycle. A representative mixed pattern (+,+,-) has old labels (0,1,0)
and new labels (1,2,2); its two positive/negative histograms change separately
although their signed difference stays fixed. Global sign reversal,
permutation of the three positions, and reversal of epsilon describe all
mixed types. Mixed trades must not be discarded as non-permutations.

No changed position can be a gauge position: every delta_i is nonzero.
The gauges at concatenated active-phase indices 0,1,12 are retained by excluding triples
meeting them. Groups spanning rows or residues are analytically impossible,
which justifies auditing only within-row triples and then filtering residues.

For completeness let beta_r be the sum of the fixed column signs in one
residue class, including the signs of inactive columns. The exact length-nine
compressed row is X_(r+3q)=beta_r-2M_(r,q). Thus preservation of every integer
M preserves the compressed row itself, not just its PAF or energy. Fixed
factor-three intermediates preserve the other compression. This supplies
both homogeneous equations needed for (1) for every trade considered here,
including those starting at the failed-compression origin.

## 3. Exact indexed equations and saturation

Let N=3p, s=r+N*l, y=(x+r) modN, h=floor((x+r)/N), and
theta_xy=a_y-a_x-h mod3. Put delta_x=0 off P. The exact equation, for either
the equal-sign or mixed-sign triangle type, is

    D_s=sum_(directed active edges incident to P) c_x*c_y
          ([theta_xy+delta_y-delta_x=l]-[theta_xy=l]).        (3)

All h and l are the existing integer boundary/layer carries. For an internal
edge, delta_y-delta_x=p^(-1)*epsilon*(c_y-c_x): zero for equal signs,
nonzero for opposite signs. For an external edge the increments are
-p^(-1)c_x epsilon outward and +p^(-1)c_y epsilon inward. Thus (3) explicitly
handles both trade types; internal cancellations are not counted as six
independent edges. There are at most six distinct affected edges and |D_s|<=6.

The norm change is checked independently using

    Delta F=sum_(i in P)c_i*zeta^i*omega^a_i*(omega^delta_i-1),
    Delta S=Delta F*bar(F)+F*bar(Delta F)+Delta F*bar(Delta F). (4)

For length45 the equivalent landing-coordinate expression is

    Delta F=t^(2r0)*sum_(i in P)c_i*gamma^i
                          *(omega^(2L_i')-omega^(2L_i)),

gamma=zeta^36, t=zeta^5, r0=i mod3. These are exact integral expressions;
the generic norm expansion is established algebra, not a novelty claim.

If both endpoints are in 9O, (1) applies. The triple sum forces 3|D_s, and
the only nonzero triples in [-6,6] congruent mod9 with sum zero are
permutations of (6,-3,-3) and (-6,3,3). Hence different correlations require
some D_s=6*sigma, sigma in {+1,-1}. Exactly six distinct edges must contribute
sigma. This confirms, rather than weakens, the preceding saturation claim.
It is necessary only; the six equations at one shift are not sufficient for
full 9O. No higher valuation threshold is introduced.

For any affected edge put w=c_x*c_y and d=delta_y-delta_x. Saturation requires
d!=0 and the following indexed old-colour equation:

    theta_xy = l - ((1+sigma*w)/2)*d mod3.                   (5)

If sigma*w=+1, the new indicator is one and the old zero. If sigma*w=-1,
the old is one and the new zero. This proves (5) in both directions.
Equations (2),(3),(5) retain phase offsets and signs; they do not introduce
new phase-cycle constraints already handled by the propagator.

## 4. Selected structural candidate: a sparse residue class with uneven charges

The following is the precise candidate selected before the pilot. In the
affected row suppose:

* a residue class b mod3 has exactly three active positions;
* its signed charge vector M_b is not balanced: its squared norm exceeds
  e_b=3 when all three signs agree, or e_b=1 when they are mixed;
* for the changed triple P, every nonzero base shift divisible by three
  has at most five distinct affected active directed edges.

Then an exact-charge-preserving three-position trade with both endpoints
in 9O must preserve all correlations. The last condition is an explicit
indexed-support test independent of phases. A sufficient uniform hypothesis
is at most five active positions in each residue class of that row. It is
automatic at p=5. The weaker support test can be used at other lengths;
no assertion that all length9p supports satisfy it is made.

Here is the short contradiction. For a signed triangle with tails t=0,1,2,
any vector of the form

    V_q=sum_t s_t*[q=t+H+epsilon*(1+sigma*s_t)/2]             (6)

is (1,1,1), (-1,-1,-1), a positive unit vector or a negative unit vector,
according as the three signs are all positive, all negative, two positive
or one positive. To prove this start with the all-positive/all-negative
case, where the labels are a permutation. Changing one sign removes its
old contribution and inserts its negative at a different label, leaving
one signed unit in the mixed case. The same argument works for either
sigma and epsilon and every H. Thus its energy is exactly e_b.

If P lies in the three-active-position class b, (2) makes its original
charge vector a vector (6), contradicting the uneven-charge hypothesis.
If P lies elsewhere, a saturated shift divisible by three is excluded by
the support hypothesis. At any other shift, the three outgoing neighbors
P+r and three incoming neighbors P-r lie in the two other residue classes;
one of them is class b. Saturation requires all three neighbors active,
so they exhaust that class.

Let r0 be the residue of P and r_plus/minus=(r0+-s) mod3 in {0,1,2}.
At an outward/inward neighboring position y, (5) says that y is aligned
with the new landing position of x if sigma*c_x*c_y=+1, and with the old
one otherwise. Since its phase is unchanged, reducing that exact alignment
modulo nine gives

    L_y=t_x+H_plus/minus+epsilon*(1+sigma*c_y)/2 mod3,
    H_plus/minus=(r0+-s-r_plus/minus)/3 in Z.                 (7)

The integer H includes all boundary and layer offsets; negative values are
allowed. The t_x run through all three labels. Equation (7) makes the full
charge vector of class b a vector (6), again contradicting its unevenness.
This excludes every possible saturated shift, so (1)--(3) force D=0. QED.

For the sufficient five-active-position hypothesis, six distinct affected
edges at a shift divisible by three would require P+r disjoint from P and
contained in the same active residue class. Those two sets alone require
six active positions. Thus the hypothesis indeed excludes such saturation.

This is a support-and-charge mechanism, not just the abstract local distance
bound: it rules out saturation using the signed charge distribution in an
entire residue class. It applies to all assignments with these fixed indexed
intermediates and charges, not merely the three audited origins. It applies
with all sign patterns and all permitted gauge choices.

## 5. Planned bounded challenges and limits

Use only the three previous origins. There are binom(12,3)+binom(11,3)=385
within-row triples per origin, each with eight nonzero increments, at most
9240 candidates in total before filtering. A pilot evaluates at most one
charge-preserving gauged neighbor per origin; its endpoints are reused in
the final audit. No multistep paths or completed census are allowed.
Full endpoint divisibility is tested independently in integral and tensor
bases. The J0=0 origin keeps its failed compression label.

The structural hypothesis must be checked, not presumed, at each origin.
Its failure is not itself a counterexample to the theorem. A blanket claim
of rigidity without the uneven-charge hypothesis is separate and will be
challenged by the permitted neighbors. An entire-fiber emptiness or
connectivity conclusion is not implied by the candidate.

## 6. Completed bounded challenges

The pilot preceded endpoint auditing. Its three endpoints were reused;
only eleven further endpoints were evaluated. Filtering all 9,240 raw
candidates verified that the integer charge test agrees with the signed-flow
classification, retaining all sign patterns. There was no multistep search.

| Origin | Raw candidates | Charge changes | Gauge violations | Permitted | Mixed / equal sign | New endpoint in 9O |
|---|---:|---:|---:|---:|---:|---:|
| positive 277 | 3080 | 3074 | 2 | 4 | 4 / 0 | 0 |
| strong 279 | 3080 | 3066 | 10 | 4 | 4 / 0 | 0 |
| J0=0 origin 279 | 3080 | 3071 | 3 | 6 | 4 / 2 | 0 |

The origins, respectively, are
`(22487656929184,11681458143385)`,
`(442312790436,2830005805622)`, and
`(31210651353580,20580563788346)`.
Their saved J values (0,0,0,0), (1,0,2,2), (0,0,1,1) were independently
rechecked. Every origin is in full 9O; only the first two meet the exact
length-nine target. The third has G=(0,6,-3,0,-3,-3,0,-3,6), and each of
its trades preserves that failure. No new endpoint has an assigned J:
division by nine there would be invalid. None of the fourteen moves even
has a saturated shift. These are actual gauged phase assignments, not
fractional or moment witnesses.

For each endpoint the audit checks the integral cyclotomic norm, tensor
coordinates, direct binary decoding, both compressions, exact PAFs, (3),
both expressions for Delta F, and (4). Full divisibility is checked at each
endpoint independently, then compared with (1) on the homogeneous difference.

Here are the structural hypotheses, not just pass/fail labels:

| Origin | C class r=2, signs +++: M, energy | D class r=1, signs -++: M, energy |
|---|---|---|
| positive 277 | (0,2,1), 5>3 | (-1,0,2), 5>1 |
| strong 279 | (2,1,0), 5>3 | (0,2,-1), 5>1 |
| J0=0 origin | (1,1,1), 3=3 | (0,1,0), 1=1 |

C's class consists of positions (2,5,14). The D classes are (1,7,13)
for 277 and (4,7,13) for 279. Active group sizes are (5,4,3) for C and
(4,3,4) for D. Both rows at the first two origins meet the theorem's uniform
hypotheses. Neither row at the third does. Its six failures to remain in
9O do not prove that the unevenness hypothesis can be dropped. The abstract
six-edge lattice example from the preceding note remains a relaxation,
not a realizable phase counterexample. No further assignments were generated.

**Explicit failed simplifications.** Starting at the positive origin, change
C positions (3,6,12), with signs (-1,+1,-1), from labels (1,0,0) to (2,2,1).
The triangle has epsilon=-1 and tails (2,0,1). The new mask pair is
`(22410481731560,11681458143385)`. Its exact charges and compressed rows are
unchanged, while the constant coefficient of S is 1. Hence it is outside
9O. This one saved counterexample refutes both proposed shortcuts:
"every three-position charge trade is a same-sign label permutation" and
"preserving charges preserves the full arithmetic domain". It does not
refute the conditional rigidity theorem. The failure is specifically that
signed marginal preservation allows opposite signs to move differently and
does not control the indexed primitive norm. There is no observed in-domain
counterexample, and no claim of unrestricted three-position rigidity.

## 7. Generality and consequence for conditional lifting

Classification (2), equations (3)--(5), and the saturation necessity apply
at every length 9p with p prime greater than three and the stated homogeneous
compression hypotheses. The proof in Section 4 also applies at those lengths
when its explicit support-and-charge conditions hold. The at-most-five
condition is only a convenient sufficient condition; it is automatic at
p=5 but not at larger p. No larger-p example was audited. The weaker
per-trade incidence bound in Section 4 is the actual needed condition.

There is a consequence stronger than a count of excluded neighbors. Fix
intermediates and signed charges. If both rows satisfy the uniform structural
hypotheses, form a graph of the actual gauged assignments in full 9O, with
edges the charge-preserving two- or three-position trades. Every connected
component has each row's entire cyclic PAF fixed, hence S and J fixed.
Indeed, charge balance forces each such move into one row and one residue
class; the other row is unchanged, so D=0 also fixes the affected row's PAF.
The two-position theorem and Section 4 apply to every edge. Induction on a
finite path proves the component assertion without assuming connectivity.
In the usual terminology these components stay inside pairs of cyclic
homometry classes. This says neither that components exhaust a homometry
class nor that equal autocorrelations imply equal phases or trivial symmetry.

In particular a full-domain move changing a correlation needs at least four
changed phases in such a fixed-charge class. The mechanism is the uneven
three-position charge vector forbidding six aligned events, rather than the
distance bound by itself. It uses a full integer charge hypothesis that is
constant throughout that class. Both controls meet it, so it does not separate
positive from empty branches. The strong origin's nonzero J cannot be
exported to every component or to other charge vectors of branch 279.
No entire-fiber emptiness theorem or connectivity statement has been proved.

## 8. Primary literature, access, and originality

Accessible primary sections checked October 17, 2026:

* Djokovic and Kotsireas, [Compression of Periodic Complementary Sequences
  and Applications](https://arxiv.org/html/1302.0571), Section 2 (norm and
  involution); Section 5, Definition 3, Theorem 3, equations (18)--(19) and
  proof. This supplies the standard exact compression setting. Compression
  preservation and the generic norm expansion are established tools.
* Turner, Kotsireas, Bulutoglu and Geyer, [Legendre pair of length 77 using
  complementary binary matrices with fixed marginals](https://arxiv.org/pdf/2101.10918),
  Theorem 2.1, printed p.4; Section 3's fixed-marginal setting; Theorem 3.4
  and Corollary 3.5, printed pp.11--12. These are precedents for the
  simultaneous-compression and primitive-frequency framework; these read
  results do not establish our particular signed-triangle obstruction.
* Ellison, Jouve and Stone, [Switching checkerboards in (0,1)-matrices](https://blogs.univ-tlse2.fr/jouve/files/2023/10/published-paper.pdf),
  Linear Algebra and its Applications 680 (2024), 274--292, Section 1,
  printed p.276, Theorem 1. Fixed-marginal switching and its connectivity
  precedent are known. That theorem credits Ryser; the original Ryser text
  was not read here. Neither a signed marginal nor the additional 9O
  restriction is covered by simply invoking this connectivity statement.
* Adrian Dobra, [Dynamic Markov Bases](https://arxiv.org/pdf/1103.4891),
  Section 1, printed p.2, and Section 3, printed pp.4--5, especially (6).
  The relevant issue is connection of the reference fiber by the chosen
  moves. Finding marginal-preserving moves alone does not prove this. Only
  these relevant portions were read, not a complete audit of its algorithms.
* Uwe Grimm and Michael Baake, [Homometric Point Sets and Inverse Problems](https://sfb701.math.uni-bielefeld.de/preprints/sfb08073.pdf),
  arXiv:0808.0094v1, Section 2, printed p.2, finite weighted-difference
  definition and example (1); Section 2.1, printed pp.2--3, covariogram
  equations (3)--(4). Homometry is the established ambiguity of recovering
  configurations from autocorrelation. Their Euclidean/infinite setting
  is not itself a theorem about these finite cyclic arithmetic fibers.

The limited read sections establish precedents, not an exhaustive novelty
search. No exact match for the support-and-charge saturation obstruction
was established in them; that absence does not establish originality.
Earlier unavailable full fast-spectral/pq-squared algorithms, the historical
representative-list gap, and external-replication gaps remain unresolved.
No new full publisher access was obtained for those sources this round;
their missing details were not inferred from abstracts or search snippets.
No authors were contacted.

The strongest defensible candidate contribution is now the signed-triangle
classification coupled to the **uneven three-position charge obstruction
to primitive-domain correlation changes**, with its homometry-component
consequence. The cycle classification and fixed-marginal ingredients are
elementary and familiar; only the specific arithmetic/indexed combination
is a candidate for originality. It is a proved local mechanism for a class
of supports, beyond a finite audit, but its significance and priority remain
unsettled. There is still no global explanation of an empty conditional
fiber. Retain the narrower reproducibility/software assessment, not research
submission readiness. This assessment is independent of priority for the
reported order-668 construction.

## 9. Next target and reproducible provenance

**Pursue a global theorem next, not paper consolidation or automatic expansion
to four-position searches.** The concrete missing step is structural coverage:
characterize the signed-charge vectors compatible with the exact compression
targets and full 9O, and the possible cyclic homometry classes over them.
A useful next lemma would constrain those classes' primitive norm or J
without enumerating all phases. One nonzero-J representative cannot certify
an unproved connected component, much less every charge class. If that
coverage cannot be obtained, pivot away from increasing local move size;
the present local rigidity already explains why a small-move walk loses
access to different correlations. No global connectivity is conjectured as
a consequence of this round.

Commands, in execution order (the package verifies inherited data and writes
only the new round's integrity/manifest files):

```powershell
.venv/Scripts/python.exe -m scripts.audit_three_phase_trades pilot
.venv/Scripts/python.exe -m scripts.audit_three_phase_trades audit
.venv/Scripts/python.exe -m pytest tests/test_three_phase_trades.py -q -p no:cacheprovider --basetemp=tmp/pytest_three_phase_trades
.venv/Scripts/python.exe -m scripts.package_three_phase_trades
```

Pilot: three endpoints in 0.0472 seconds; fivefold projected full endpoint
audit 1.1013 seconds. Final audit: 0.0536 seconds, fourteen unique endpoint
records including reuse of the three pilot endpoints. One worker and a
120-second internal cap; preflight estimates 200 MB memory and 2 MB new
storage, not measured peaks. No cap was hit. No completed census was rerun.
Four focused tests passed in 0.28 seconds. They check domains, exact
factorizations, all-sign retention, the explicit failed simplification, and
the 96 abstract sign/offset cases of (6); those abstract cases are not extra
branch phase assignments. This is local verification, not external replication.

`results/three_phase_trades/manifest.json` pins SHA-256 hashes for all new
notes, code, tests and evidence. `integrity.json` verifies all 6,769 inherited
result files, all five paper files, the preceding manifests and inherited
raw-byte aggregate, preserving the two previously recorded CRLF exceptions.
The manuscript SHA-256 remains
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.
All frozen p=5 and p=7 evidence is preserved. The manuscript was neither
edited nor compiled; no new PDF/layout claim is made.
