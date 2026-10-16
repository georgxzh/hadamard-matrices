# Event-conditioned compression, reflection cancellation, and integer carries

Research round: October 16, 2026. Base commit
`f1499ee7c5f726e34d1c74c644b40b1187ef6771`, branch
`agent/order-428-reproduction`. Initial tree clean; no child AGENTS.md or
CLAUDE.md found. Read the compression/residue coupling and residue-carry notes,
preceding phase-moment and primitive-local notes, phase parameterization,
existing propagation, integral spectral routines, and frozen witnesses.
No inherited file or manuscript was changed. No completed census was rerun.

**Result:** the selected products detect correlations absent from the old
mean-zero constructions, but no explanatory contradiction for branch 279
was obtained. We derive exact contraction and carry identities, and a local
reflection-cancellation formula explaining why the nearest-triangle argument
fails. The local cancellation extends to arbitrary odd compression lengths.
It does not extend to an empty-fiber theorem. The remaining conditional
nonvanishing claim and substantive originality remain open. The narrower
publication assessment is retained; the manuscript was not compiled.

## 1. Selected family and precise scope of the candidate

Use the indexed C,D rows and 23 phases from the preceding notes. Phases at
concatenated indices 0,1,12 remain fixed to zero. Signs and original positions
are unchanged. Write p,q for the adjacent cancelling D-edge: (2,3) on branch
279 and (1,2) on branch 277. We reserve u,v for J_0,J_2.

Before the pilot, select k=q+1 as the core third vertex: k=4 on 279 and k=3
on 277. For each a in {p,q} and d in {0,1,2}, select

    Y_(a,k,d) = [a_k-a_a=d mod 3].

These are six existing phase events, multiplied by G_0,G_1,G_2: **18 core
products per branch**. A predeclared comparison family uses all nine other
active D positions as k: 54 selectors and **162 products per branch**. There
is no adaptive expansion to longer paths, larger degree, or a phase search.

The candidate local mechanism is that conditioning these events makes the
opposite-edge cancellation leave an unavoidable signed compression residual,
which could then constrain the two residue coordinates. A useful proof would
need a *pointwise* bound on the remaining terms, on G=0 and S in 9O. A nonzero
conditional average would only guide that proof. We also challenge the
simplification that replacing the exact products by their residues modulo
three preserves their effect on J. Neither claim is presumed true.

All seven saved ordinary witnesses and both saved 27-point designs form the
audit input. No new branch phase assignments were generated. We do not
assume a_p=a_q for the full fiber:
that sector is examined because it is the source of the previous mean-zero
construction and occurs in the required strong false positive. The positive
277 witness is outside that sector.

## 2. Exact product expansion and event contraction

For an original directed edge i->j at shift s=r+15l retain the integer carry
h=floor((i+r)/15) and the event

    Y_f=[a_j-a_i-h-l=0 mod 3],       w_f=b_i b_j.

The integer compression form, with s=0,15,30 omitted, is

    G_t=c_t+sum_(s=t mod 9) sum_f w_f Y_f,
    c_t=-sum_(s=t mod 9) t_(s mod 15),                t=0,1,2.   (1)

Therefore the requested product is exactly

    Y_e G_t = c_t Y_e + sum_(s=t mod 9) sum_f w_f Y_e Y_f.       (2)

No sign is absorbed into the Boolean variable. Each selector's sign product,
base shift, integer carry, layer, full shift, and endpoints are saved in
`model.json`; each term of (1) retains its original full shift. To map the
ordinary difference d to the existing event, put r=(k-a) mod 15,
h=floor((a+r)/15), l=(d-h) mod 3. Only then does h+l reduce to d modulo three.
This also handles k<a. The complete expanded model consists of the saved
selectors and the three saved integer forms via (2), not a solver encoding.

**Contraction identity.** On Y_e=[a_b-a_a=d]=1, replace a_b by a_a+d.
For an event [a_j-a_i=H], let i',j' be the endpoints after that substitution,
and let delta_i,delta_j be d at a replaced endpoint and zero otherwise. Its
new equation is

    [a_j'-a_i'=H-delta_j+delta_i mod 3].                        (3)

When i'=j' this is the constant [H-delta_j+delta_i=0 mod 3]. Reversing an
edge reverses the entire adjusted difference. The identity
Y_e G_t=Y_e (G_t with substitution (3)) holds on every actual phase assignment:
it is zero on Y_e=0, and substitution is valid on Y_e=1. This proves necessity
and the expansion's exact integer scope without treating edge events as
independent variables. Coincident events satisfy Y_e^2=Y_e; incompatible
colours on the same edge have product zero. Shared-endpoint products impose
two differences, not a new triangle constraint.

Since the three colours partition one, sum_d Y_(a,k,d)G_t=G_t. On actual
phase assignments these products add no new feasible-set restriction to
G_t=0. Their value is as multipliers for a proof, or as stronger constraints
in a relaxation that records products. In particular, products involving a
D selector and a C edge are retained. They are arithmetic products of the
two rows' contributions, not an added binary cross-correlation condition.

## 3. A carry identity coupling the products to u and v

Keep S in 9O defined by **all 24** integral cyclotomic coefficients divisible
by nine. On that domain u=Q_0/3 mod 3 and v=Q_2/3 mod 3. Both exact
compressions are required before using the triple congruences of the previous
note as an equivalent domain test. Neither Q-divisibility nor product
vanishing modulo three is substituted for this domain.

For an integer q put P(q)=binom(q,3) mod 3. Generalized binomial coefficients
are evaluated in Z, including negative q. The previous carry proof gives
P(q)=floor(q/3) mod 3. In particular P(Q_0)=u and P(Q_2)=v on 9O.

**Proposition 1 (integer carry feedback).** For integers q,g and Y in {0,1},

    binom(q+Yg,3)-binom(q,3)
      =Y*(g*binom(q,2)+binom(g,2)*q+binom(g,3)).               (4)

Proof: for Y=0 both sides vanish; for Y=1 take the coefficient of T^3 in
(1+T)^q(1+T)^g. This formal power-series identity is valid for negative
integer exponents too. QED.

Apply (4) to q=Q_0 or Q_2, g=G_t and Y=Y_e. It gives an explicit identity
for modifying a residue formula by the exact compression product. On G_t=0
the modification leaves the coordinate unchanged. If only 3 divides G_t,
then (4) reduces to

    P(Q_r+Y_e G_t)-P(Q_r)=Y_e*(G_t/3) mod 3.                  (5)

Indeed G_t and binom(G_t,2) are zero modulo three, while binom(G_t,3) is
G_t/3 modulo three. The division in (5) takes place in Z. The hypothesis
3|G_t is explicit; it is true for the saved moment witnesses but is not
silently inferred from Q-divisibility. The shifted expression is a residue
representation only on the stated exact compression domain.

This also gives a genuine polynomial bound. Each event is quadratic in the
ternary phases over F3. Q_r and G_t modulo three have degree at most two;
binom(Q_r,2) and binom(G_t,2) use the invertible denominator two and have
degree at most four. The signed carry polynomial for binom(G_t,3) has degree
at most six by the preceding note. Multiplication by Y_e in (4) gives a
degree-at-most-eight representation of the feedback on the full phase cube.
This is an upper bound for this expression, not a minimum-degree result for
J on its conditional domain and not a new carry principle.

The required counterexample (31210651353580,20580563788346) makes the lost
information explicit. For e=[a_4-a_3=0], Y_e=1, G_1=6 and Q_0=0. Thus
Y_e G_1=0 modulo three, but the carry changes by binom(6,3)=2 modulo three.
Its true J_0 is zero; the shifted value is **not J** because its exact
compression fails. Keeping only the degree-four equations Y_e G_t mod 3
cannot justify this carry substitution.

A separate overly strong simplification is ruled out by existing evidence:
the specified extension P(Q_2) on branch 279 cannot be a constant-coefficient
affine combination over F3 of these degree-at-most-four products and phase
events on the entire gauged cube. The saved six-variable mixed difference
of P(Q_2) is 2, whereas every polynomial of degree at most four has zero such
difference. This reuses the existing certificate; it says nothing against
an identity restricted to the full domain or involving its carry equations.

## 4. What the products expose in the old averaging argument

On the saved 27-point designs, the sums of G and B are zero, but averages
of Y_e G_t are not. In the 18-product core there are respectively 16 and 14
nonzero means for 277 and 279. In the full 162-product star there are 142
and 134. Thus those particular designs no longer witness feasibility of the
product-moment relaxation. This is **not** a proof that the strengthened
relaxation is infeasible, nor that it explains an empty fiber.

One must distinguish these designs from the independent-factor probability
model in the previous proof. The 27-point construction has uniform pair
differences, but reuses seed directions within and between rows. It need
not preserve averages of products of two events. For example, on branch 279
the saved design has sum Y_(2,4,2)G=(12,-9,0), whereas the independent model
below gives zero for this product mean. Treating the two distributions as
interchangeable at second-event order would be incorrect.

Here is a closed formula for the independent model, with no phase enumeration.
Impose a_p=a_q, keep the gauges, and give every other unfixed phase factor an
independent uniform ternary value, sharing the one factor for p,q when they
are not anchored. There are nineteen independent factors in either branch.
For a third position k and d=a_k-a_p set w=D_p D_k and n=k-p+15d. Define
the signed array

    T_w(n;s)=w*([s=n]+[s=-n]-[s=n-1]-[s=1-n]),                (6)

with indices modulo 45. Let n_j=k-p+15j. Then

    E[B_s | a_k-a_p=d]
      =T_w(n_d;s) -(1/3)*sum_(j=0)^2 T_w(n_j;s).               (7)

Proof. The original mean of B is zero. Conditioning changes only the two
edge distributions p--k and q--k: their weights are w,-w. Every other edge
still has its original uniform difference or fixed cancelling difference.
Their deterministic contributions after conditioning are (6); subtract their
old uniform average. This proves (7). The conditioning event has probability
1/3. Fold (7) modulo nine to obtain E[G|Y_e=1], or apply the signed Q slice
functional to obtain E[Q|Y_e=1]; divide by three for E[Y_e G]. QED.

For the core k=p+2, w is +1 on 277 and -1 on 279. The following table gives
conditional (G0,G1,G2) and (Q0,Q2), divided by w:

| d | E[G|d]/w | (E[Q0|d],E[Q2|d])/w |
|---|---|---|
|0| (0,-1,1) | (-2/3,-1/3) |
|1| (0,1,-1) | (1/3,-1/3) |
|2| (0,0,0) | (1/3,2/3) |

These are exact rational expectations, **not** algebraic integers S/9 and
not values of u,v. Rank computations for at most two linear equations over
F3 independently verify (7) for every selector in the bounded star. No
3^19 enumeration is performed. The table exhibits a colour with zero
compression response in both branches, defeating the proposed uniform
nonzero-response step. The next section identifies its pointwise mechanism.

## 5. A local reflection cancellation that survives conditioning

**Proposition 2.** Suppose p,q=p+1 are active D positions of opposite signs
with equal phases, and k is a third active position. The two cross terms
joining k to p,q in the active norm have polynomial

    T_w(n;z)=w*(z^n+z^(-n)-z^(n-1)-z^(1-n))
            =w*(z-1)*z^(-n)*(z^(2n-1)-1),                  (8)

where n=k-p+15(a_k-a_p) mod 45 and w=D_p D_k. At a primitive m-th root
with odd m>1 this vanishes iff 2n=1 mod m.

Proof. Expanding the two signed norm cross terms gives the first expression.
Multiplying out the factorization gives the second. The root and z-1 are
nonzero, so vanishing is exactly z^(2n-1)=1. For odd m the solution is unique
modulo m. QED. This is the antisymmetry of an adjacent signed pair under
reflection about its midpoint, stated with exact indices.

At length nine it means n=5 mod 9. The entire folded array (6), not just
one Fourier value, then vanishes, since n and -(n-1) coincide. At length 45
only n=23 mod 45 vanishes. Thus n in {5,14,32,41} gives a cross term invisible
to every length-nine balance while remaining nonzero at primitive order 45.

For these four cases the term is a **unit at pi=1-zeta^5**, not individually
in 9O. In (8), zeta reduces to alpha of order five. For n=5,14,32,41,
neither alpha-1 nor alpha^(2n-1)-1 is zero. So its pi-valuation is zero.
This argument applies to the cross term, not the complete norm defect S.

The indexed supports yield these possible local compressed midpoints:

| branch | k | a_k-a_p | n mod 45 | w | primitive term zero? |
|---|---|---|---|---|---|
|277|3|2|32|+1|no|
|277|6|0|5|+1|no|
|277|9|1|23|+1|yes|
|277|12|2|41|-1|no|
|279|4|2|32|-1|no|
|279|7|0|5|+1|no|
|279|13|2|41|+1|no|

This is an actual indexed difference: 279 has no active third column at the
full-length midpoint k=p+23 mod 15=10, whereas 277 has the active column 9.
It is **not** an emptiness obstruction. Other edges and the other row can
cancel a nonzero cross term, and no hypothesis forcing an isolated third
term or preventing that cancellation has been proved. The table concerns
the equal-phase sector; it does not assert that the frozen positive uses it.

### The required strong false positive realizes the local blind spot

For (442312790436,2830005805622), the D phases at positions (2,3,4) are
(0,0,2). Thus n=32 and w=-1. Both connecting core events of colour two
are active. Their cross-term array has all nine folded balances zero,
while (8) is nonzero and has valuation zero. The C anchor edge cancels the
D edge (2,3) itself exactly; the k=4 cross contribution is the local
reflection cancellation above.

The local raw Q vector is (0,-1,0,1); in particular its Q0,Q2 contributions
are zero. Nevertheless the complete witness has Q=(3,9,6,-3) and
J=(1,0,2,2). Write S=T+R for this cross term and the remaining terms. The
saved exact coefficients verify v_pi(T)=v_pi(R)=0 and S in 9O. The strong
divisibility is produced by cancellation between the two summands; neither
has a separate residue (T/9) mod pi or (R/9) mod pi in O.

This refutes the local uncancellability simplification on the **full** desired
domain. It also refutes any attempt to infer equal D phases are impossible
from these compression products. It does not refute joint nonvanishing of
u,v, since this witness has nonzero J. We have not proved that the entire
162-product family is incapable of supporting a conditional proof.

## 6. Challenges, limitations and the next justified target

All saved ordinary witnesses were checked; the principal outcomes are:

| first mask; branch | G0,G1,G2 | J | nonzero star products |
|---|---|---|---|
|22487656929184; 277|0,0,0|0,0,0,0|0|
|442312790436; 279|0,0,0|1,0,2,2|0|
|31210651353580; 279|0,6,-3|0,0,1,1|36|
|22964264347100; 279|0,0,0|undefined, outside 9O|0|

The remaining three saved 9O points and all 54 saved design members are in
the audit. Direct product expansion and conditional substitution agree on
all 9,882 product evaluations. The full-domain flag is independently checked
against all tensor coefficients for each saved point. No survivor was
selected as a purported proof of nonvanishing.

The distinctions matter:

* Exact products exclude the old 27-point averages as witnesses for this
  strengthened moment relaxation. Infeasibility of that relaxation is open.
* Modulo-three products admit the J0=0 counterexample and lose the carry in
  (5). They are not substitutes for the integer products.
* The independent-factor conditional response has a local blind colour;
  it is not interchangeable with the 27-point design or a true fiber point.
* The actual strong witness retains every phase cycle, exact compression,
  and the full domain. It realizes a compression-invisible primitive cross
  term, showing why isolating one triangle cannot supply the sought residue.
* Degree-four products do not globally represent the old degree-six residue
  extension; a conditional identity using full divisibility is still possible.

What is proved beyond computational observations is (3), (4)--(5), (7), and
the reflection criterion (8) with its explicit indexed support comparison.
These are elementary algebraic refinements and a countermechanism to the
local argument, not the sought original theorem explaining an empty fiber.

The strongest next target is to **group the local dipole with specific
remaining signed edges before division by nine**. A useful lemma would make
such a grouped sum divisible by nine using the pointwise compression and
full tensor congruences, then constrain its quotient together with the other
groups. The missing information is precisely the integer cancellation
between the compression-invisible local term and the rest, including the
C-row terms in (2). The equal-phase sector and the two unequal-phase sectors
must all be covered; nothing permits reducing the fiber to the sector seen
in one saved witness. Merely increasing the product family, raising a
valuation threshold, or adding already-enforced phase cycles is not justified
by this round. No short grouped identity has yet been proved.

## 7. Primary precedents and access limits

Checked October 16, 2026. No author contact or external messaging occurred.

* Mathieu and Sinclair, [Sherali-Adams Relaxations of the Matching
  Polytope](https://people.eecs.berkeley.edu/~sinclair/sherali.pdf), accessible
  author-hosted full paper, Section 2.1 (PDF page 3), definition through
  Lemma 2.1. Read the explicit multiplication by Boolean monomials,
  multilinearization and lifted variables. Multiplying a constraint by an
  event and retaining products is established machinery. The paper's
  matching-polytope results do not establish a rank or sufficiency result
  for our ternary phase system.
* The original [Sherali--Adams 1990 publisher
  page](https://epubs.siam.org/doi/10.1137/0403036) was accessible as metadata
  and abstract. Its View PDF link redirected to the abstract/access page;
  the full original article was not read. No missing detail is inferred
  from the abstract; the accessible primary research paper above provides
  the explicit method definition used for comparison.
* Kaji, Maeno, Nuida and Numata, [Polynomial Expressions of Carries in p-ary
  Arithmetics](https://arxiv.org/pdf/1506.02742), Section 3.1, proof of
  Theorem 3 and Remark 1, printed pp.5--6. The binomial/generating-function
  carry mechanism is established. Formula (4) specializes ordinary binomial
  convolution; neither it nor its degree bound is presented as a new
  arithmetic principle.
* Djokovic and Kotsireas, [Compression of Periodic Complementary Sequences
  and Applications](https://arxiv.org/html/1302.0571), Section 2 group-ring
  norm/involution discussion and Section 5, Theorem 3 and proof. These
  supply the standard norm and compression framework for (6)--(8).

The local reflection factorization is elementary within this framework.
Whether this precise indexed application has appeared before is unresolved;
no priority claim follows from these readings. Earlier full-algorithm,
historical-list and external-replication gaps remain. There is no basis here
for upgrading the narrower publication assessment or changing the manuscript.

## 8. Reproduction and resource record

```powershell
.venv/Scripts/python.exe -m scripts.audit_event_compression pilot
.venv/Scripts/python.exe -m scripts.audit_event_compression audit
.venv/Scripts/python.exe -m pytest tests/test_event_compression.py -q -p no:cacheprovider --basetemp=tmp/pytest_event_compression
.venv/Scripts/python.exe -m scripts.package_event_compression
```

The two-record/six-expectation pilot took 0.0606 seconds and projected 9.40
seconds with a conservative fivefold margin. Audits completed in under one second:
61 saved points, 9,882 exact product checks, 19,764 carry checks, and 108
rank-based expectation checks. Five focused tests passed in 0.13 seconds.
Tests include generic small-variable identities, signed integer carry cases,
and exact root factorization; they do not generate new branch assignments.
The final audit was repeated after adding the carry and decomposition checks;
no old experiment or census was repeated. No solver was used.

One worker, a 120-second internal audit cap, estimates of 150 MB memory and
3 MB new storage; the final package is about 3.4 MB. Memory was estimated,
not measured. No cap or
timeout was hit. All runs stayed below four cores, thirty minutes per run
and 10 GB. The package verifies inherited hashes and preserves legacy CRLF
exceptions without rewriting them. New output is only in
`results/event_compression/`. The final manifest pins source, tests, notes,
model and evidence. All 6,753 baseline result files and five paper files are
preserved. The manuscript hash remains
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.
No PDF compilation or layout claim is made.
