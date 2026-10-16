# Signed cut formula and the limit of the cancelling-edge strategy

October 16, 2026. Requested starting point:
`f1499ee7c5f726e34d1c74c644b40b1187ef6771` on
`agent/order-428-reproduction`. The preceding product round was already
committed and pushed as `ee3b93944668606a51ef3253ee101deeb5d2a96d`.
This round preserves that descendant and does not repeat its product audit.
The initial tree was clean; no child agent instruction files were found.
Read the compression/residue, residue/carry, primitive-local, phase-moment,
and event-product notes, their implementations, phase propagation and frozen
witnesses. The existing propagator already enforces phase-cycle consistency.

**Outcome:** an explicit signed-support cut formula rules out a proposed
local division by nine, in every phase sector and for a class of indexed
supports. This explains a failure of the proof strategy, not the empty
fiber. A quadratic identity obtained from the selected event products detects
the old mean-zero constructions, but an actual saved counterexample proves
that the aggregation discards essential information. No original empty-fiber
theorem or substantive breakthrough was obtained. Pivot away from expanding
this local star without a new relation involving the remaining signed edges.
The narrower publication assessment and the manuscript are unchanged.

## 1. Bounded candidate, selected before new computation

Keep the previous family, without expansion: D-pair E={1,2} for 277 and
E={2,3} for 279, each endpoint joined to the nine remaining active D positions.
There are 18 unordered edges, 54 phase selectors and 162 products Y_e G_t,
t=0,1,2 per branch. The core third position is respectively 3 and 4. The
previous round already expanded and audited these exact products. This round
uses only two signed support calculations and 61 saved phase assignments;
there is no new phase search, solver, census, or adaptive product extension.

The next candidate was:

> On exact length-nine compression and the full S in 9O domain, the sum T_E
> of **all** cross terms between the cancelling pair and the other active D
> positions belongs to 9O, so that (T_E/9) mod pi can be handled separately.

Grouping all nine third positions was a plausible repair of the preceding
single-triangle failure: the reflection midpoint at column 9 is active in
277 but the corresponding column 10 is forced in 279. Grouping retains the
different indexed signs rather than just the common margin profile. It was
not presumed sufficient or novel. The candidate is false, including at the
strong branch-279 witness. The proof below is stronger than a finite rejection:
T_E is not even divisible by pi for **any** phases on either branch.

## 2. Exact events, products, and the retained quadratic interaction

All notation and integer targets are as in
`compression_residue_coupling.md`, Sections 1--3. For s=r+15*l, j=(i+r) mod15
and integer h=floor((i+r)/15),

    Y_(i,j,s)=[a_j-a_i-h-l=0 mod3],
    B_s=sum b_i*b_j*Y_(i,j,s)-t_r,
    G_t=sum_(s=t mod9) B_s.

The constant terms are included in G. Exact compression is G_0=G_1=G_2=0
in Z, using the already proved B symmetry and triple-sum relations. Third
gauge indices 0,1,12 remain fixed at zero. The phase arrays, supports and signs
are neither relabelled nor randomized.

For any cut E in an active row I define the group-ring polynomial

    T_E(z)=sum_(i in E,j in I\E) c_i*c_j
             (z^(j-i+15(a_j-a_i))+z^(-j+i-15(a_j-a_i))).       (1)

Exponents are calculated as integers before reducing modulo 45. Equivalently,
for each of the 54 selectors e in the selected star, use its original shift
s_e=r+15*l and weight w_e=c_i*c_j, and put

    T_E(z)=sum_e w_e*Y_e*(z^s_e+z^(-s_e)).                    (2)

Exactly one of the three colours for each edge is active; the integer h+l
is what makes (1) and (2) agree across the index boundary. Let

    H_t=sum_e w_e*([s_e=t mod9]+[-s_e=t mod9])*Y_e,
    R_t=G_t-H_t.

The reverse-shift multiplicity is retained, including its value two when
both orientations fold to the same coordinate. Multiplying the exact G_t
by H_t gives a particular, explicitly bounded sum of the selected products:

    sum_e w_e*([s_e=t]+[-s_e=t])*Y_e*G_t
       = H_t*G_t = H_t^2+H_t*R_t.                            (3)

The brackets in (3) are modulo nine. Thus every exact compression assignment
satisfies H_t^2+H_t R_t=0 in Z. Expanding G_t=c_t+sum_f w_f Y_f gives the
constant-event terms and event products with their original signed integer
coefficients. No division or reduction modulo three occurs in this identity.

This exhibits the interaction lost by unconditional averaging: the required
mixed contribution H_t R_t cancels a nonnegative square. It does **not** give
a sign bound on H_t R_t, and does not imply H_t=0. For the positive solution
H=(2,1,1), R=(-2,-1,-1); for the strong 279 witness H=(2,-3,1), R=(-2,3,-1).
Both require negative mixed products. An inequality H_t R_t>=0 would reject
the true positive solution as well as the false positive, so is unavailable.

For the two saved 27-point constructions, the sums (not averages) are

| branch | sum H_t^2 | sum H_t R_t | sum H_t G_t |
|---|---|---|---|
|277|(132,105,105)|(36,48,30)|(168,153,135)|
|279|(192,102,102)|(12,36,9)|(204,138,111)|

Divide by 27 for expectations. These are distributions on genuine gauged
phase assignments, but not distributions supported on conditional solutions.
Their zero mean B does not meet even the three consequences (3).
Infeasibility of the full strengthened moment relaxation remains unproved.

## 3. A general support-cut residue formula

**Proposition (phase-independent cut test).** For length 9p, p>3 prime, let
zeta be primitive, omega=zeta^(3p), O=Z[zeta], and pi=1-zeta^p. Let I be any
indexed active support with integer signs c_i, E any subset, and a_i any
ternary phases. Replace 15 by 3p in (1). In

    O/(pi) = F_3[alpha]/(Phi_p(alpha)),

put A=sum_(i in I)c_i alpha^i and h=sum_(i in E)c_i alpha^i. Then

    T_E mod pi = h*bar(A)+bar(h)*A-2*h*bar(h),                (4)

where bar(alpha)=alpha^(-1). Equivalently, define signed integer counts

    w_r=sum_(i in E,j in I\E)c_i*c_j
                     ([j-i=r modp]+[i-j=r modp]).

Then T_E mod pi=0 **if and only if** all p integers w_r are congruent
modulo three. If they are not, T_E is not in 9O for any phases.

Proof. Put t=zeta^p and gamma=zeta^9; choose integers a,b with 9a+pb=1,
so zeta=gamma^a*t^b. The products gamma^r*t^v, r<p-1 and v<6, span O
integrally by the two monic cyclotomic relations. Their number is
[Q(zeta):Q]=6(p-1), so they form an integral basis. Thus O has exactly the
tensor presentation Z[gamma,t]/(Phi_p(gamma),Phi_9(t)). Setting t=1 changes
Phi_9(t) to 3 and gives the displayed quotient, with alpha=gamma^a=zeta
mod pi; a is invertible modulo p. No irreducibility of Phi_p over F_3 is
needed. All omega phases reduce to one. Write F_D=F_E+F_(I\E); expanding the
cross terms and reducing gives h*(bar(A)-bar(h))+bar(h)*(A-h), proving (4).
Alternatively, reduce the exponents in (1) modulo p and collect w_r. The
degree-at-most-p-1 polynomial sum w_r*x^r vanishes modulo Phi_p over F_3
exactly when it is a scalar multiple of 1+x+...+x^(p-1), which is exactly
equality of its coefficients. Finally 9O is contained in (pi), so a nonzero
residue precludes divisibility by nine. QED.

For p=5 the quotient is the field F_81 (3 has order four modulo five), so
nonzero also gives valuation zero at the unique prime above three. For
general p the quotient can be a product of fields: the proposition asserts
nonmembership in the ideal (pi), not that every nonzero element is a unit.
It is an explicit support/sign hypothesis and applies without compression,
without an equal-phase assumption, and with or without the third gauge.
No larger-prime phase experiment was run.

For the actual indexed supports the integer calculation is particularly short:

|branch|A counts at residues 0,...,4|h counts|w counts|T_E mod pi|
|---|---|---|---|---|
|277|(1,-3,3,0,0)|(0,-1,1,0,0)|(8,-5,1,1,-5)|1|
|279|(-2,0,3,0,0)|(0,0,1,-1,0)|(2,-1,0,0,-1)|alpha^2+alpha^3|

Here A=1 in both cases. These distinct nonzero residues are an indexed
difference, but **not** a distinction in feasibility. Their integer sums
are both zero, which also shows why replacing the signed difference profile
by a total count loses the information in (4).

If S lies in 9O and S=T_E+U, then U mod pi=-(T_E mod pi). Thus neither
summand can be divided by nine individually. The obstruction to separating
the two summands holds in all three pair-phase sectors, including the
unequal sector of the frozen positive solution. Any proposed repair
T_E+sum f_(e,t)(a)*Y_e*G_t has the same value as T_E on exact compression.
Consequently such a repair alone cannot make this cut divisible by nine
on a nonempty conditional domain; additional nonvanishing signed terms
from U are essential. This is a restriction on the proposed decomposition,
not on every possible polynomial identity or conditional inequality.

## 4. Counterexamples and full-domain discipline

All 61 inherited points were checked via (1), the original event expansion
(2), and independent integral-basis multiplication of F_E and F_(I\E).
All 24 coefficients of the full S were tested for divisibility by nine and
cross-checked with the saved tensor basis. Only then was J calculated.

| masks (first, second) | exact G | S in 9O | J | H | H_t G_t |
|---|---|---|---|---|---|
|(22487656929184,11681458143385), 277|yes|yes|(0,0,0,0)|(2,1,1)|(0,0,0)|
|(442312790436,2830005805622), 279|yes|yes|(1,0,2,2)|(2,-3,1)|(0,0,0)|
|(31210651353580,20580563788346), 279|no|yes|(0,0,1,1)|(2,0,0)|(0,0,0)|
|(22964264347100,2872821395978), 279|yes|no|undefined|(2,-1,-2)|(0,0,0)|

The first two are actual conditional phase assignments; only the first is
a Legendre solution. They disprove local divisibility and any claim that
the star's nonzero residue alone obstructs a solution. The third has
G=(0,6,-3), so every aggregate in (3) is zero although 36 individual Y_e G_t
are nonzero, as already saved. Hence replacing the individual products by
three square identities is a strictly weaker test on actual assignments.
The last has all exact products zero but is outside 9O; no J is assigned.
Other saved ordinary witnesses and the 54 saved design points are retained
with their separate domain flags in `results/star_cut/audit.json`.

We do not apply the triple-balance congruence equivalence outside its
proved hypotheses: it requires both exact compression maps. We make no
replacement by Q-divisibility, modulo-three compression, mean equations,
or phase-cycle consistency. Formula (4) is a reduction **without division**;
it is not J. Knowing it does not supply the integer carries of (S/9) mod pi.

## 5. Decision, generality, and literature

The generalizable result is the support-cut formula/test (4), and the exact
quadratic consequence (3). Both are elementary consequences of group-ring
norms and multiplication of Boolean constraints. No substantive originality
is established. The reported order-668 construction changes neither this
standard nor the mathematical independence of studying conditional fibers.

Primary sources checked October 16, 2026:

* Djokovic and Kotsireas, [Compression of Periodic Complementary Sequences
  and Applications](https://arxiv.org/html/1302.0571), Section 2, group-ring
  involution and norm before Lemma 1; Section 5, Theorem 3. Accessible full
  text supplies the existing norm/compression framework, not an original
  attribution for our cut specialization.
* Mathieu and Sinclair, [Sherali-Adams Relaxations of the Matching
  Polytope](https://people.eecs.berkeley.edu/~sinclair/sherali.pdf), Section
  2.1, PDF p.3, definition before Lemma 2.1: multiplying constraints by
  Boolean monomials and multilinearizing is established. No result about
  the rank or sufficiency of this particular phase family is inferred.
* [Epoch AI, Hadamard Matrix of Order 668](https://epoch.ai/frontiermath/open-problems/hadamard),
  status and Solution update, reports the human/AI construction including
  order 668. Its About section still contains historical open-case wording;
  the explicit update is the relevant current statement. The linked
  [primary announcement](https://x.com/__alpoge__/status/2087504785952182273)
  returned HTTP 403. Its payload was not read, executed or independently
  verified here. We make no first-construction claim or inference about
  whether that construction supplies a length-333 Legendre pair.

These readings establish precedents and the reported status, not a complete
priority search for every specialized identity. Earlier inaccessible full
algorithms, historical representative-list and external-replication gaps
remain. The narrower reproducibility/software assessment is retained.

**Recommendation: pivot from local-star expansion.** The star has a fixed
nonzero residue in every phase sector, so any quotient-based proof must
account for cancellation with the remainder. The attractive three quadratic
aggregates lose exact information even on the saved J0=0 example. Neither
fact proves that the full event-product family can never help, but there is
no evidence justifying a larger blind multiplier search.

A concrete next mathematical target is a **global integer signed-charge
identity across the C and D rows**, using the exact compressed charges
M_(r,q) and their energy/cross-correlations from the compression note,
Section 1. To be useful it must constrain the mixed remainder term and the
integer Q_0,Q_2 carries on the full 9O domain, with explicit ordered
support/sign hypotheses satisfied by a class containing 279 and excluding
the positive 277 control. Require such a specific identity or bound before
further computation. A mere partition into separately divisible cuts,
positive mixed-term assumption, or phase-independent residue test is
already contradicted here. Existence of a useful global identity remains
open; no promise that this pivot succeeds is made.

## 6. Reproduction and preservation

```powershell
.venv/Scripts/python.exe -m scripts.audit_star_cut pilot
.venv/Scripts/python.exe -m scripts.audit_star_cut audit
.venv/Scripts/python.exe -m pytest tests/test_star_cut.py -q -p no:cacheprovider --basetemp=tmp/pytest_star_cut
.venv/Scripts/python.exe -m scripts.package_star_cut
```

The two-point pilot took 0.0120 s and projected 1.86 s with a fivefold margin.
The saved-evidence audit took 0.0541 s: 61 points and 183 weighted-product
identities. One worker, 120-second internal cap, estimated 100 MB memory and
200 KB new storage; these resource sizes are estimates, not peak measurements.
No cap was hit. No completed census or old audit was rerun. The initial
two-support arithmetic probe took 0.0101 s; the reproducible pilot subsumes it.
Four focused regression tests pass; their output is saved separately.

The new package verifies all 6,759 inherited result files and five paper
files, previous manifests and the inherited raw-byte aggregate. The two
pinned legacy CRLF exceptions are preserved. `manifest.json` pins the new
source, notes, tests and evidence. The manuscript hash remains
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.
It was not edited or compiled; this round makes no PDF/layout claim.
