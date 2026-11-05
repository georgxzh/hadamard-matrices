# Compression-preserving exchanges and local correlation rigidity

Research round: October 16, 2026. Base
`9ed23ba6252ddfec41a79b6eff5af93f7ef10c6c`, branch
`agent/order-428-reproduction`. Initial tree clean; no child AGENTS.md or
CLAUDE.md found. The star-cut, compression/residue, residue/carry and preceding
phase notes, their implementations, the existing phase propagator, and frozen
witnesses were read. No old artifact is edited. The manuscript remains unchanged.

**Outcome:** the proposed invariance is proved, in the stronger form of a
uniform two-position correlation-rigidity theorem for length 9p. This is
a mathematical mechanism beyond the finite audit, not an empty-fiber theorem.
The bounded audit finds no nontrivial in-domain neighbor at any of the three
origins, so the tested graph components are singleton vertices. Originality
of the rigidity specialization remains unresolved; the narrower publication
assessment is retained.

## 1. Selection and proof before the pilot

The bounded family is exactly the user's family. For each of the three saved
origins, inspect the 66 pairs of active C positions and 55 pairs of active D
positions, 121 total. Retain pairs in one row with equal index modulo three
and equal sign; exchange landing labels, recovering phases; reject any move
changing gauge coordinates 0,1,12. Count equal-label exchanges as no-ops, not
as new neighbors. The pilot checks at most one nontrivial permitted exchange
per origin. The final audit checks only remaining one-exchange neighbors,
reusing the pilot endpoints. No path exploration or second-step moves.

**Selected candidate:** if both endpoints of such an exchange satisfy the
full condition S in 9O, their J=(S/9) mod pi values agree. This might yield a
constant residue on a connected component of a charge-preserving phase graph.
It cannot explain the whole empty fiber without a proof that the relevant
components and charge patterns are covered and that their constants are nonzero.
The proposed invariant is not assumed to follow from charge preservation alone.

For i=r+3m_i and j=r+3m_j, c_i=c_j=c in {+1,-1}, set

    q_i=L_i=(m_i+5a_i) mod3, q_j=L_j=(m_j+5a_j) mod3.
    a_i'=2(q_j-m_i) mod3, a_j'=2(q_i-m_j) mod3.                (1)

The inverse of five modulo three is two. Other phases remain fixed. For
every integer charge coordinate M_(r,q), the old contribution from these
positions is c([q_i=q]+[q_j=q]); the new contribution is the same two summands
in reverse order. Thus every M is preserved **in Z**. In particular,
X_(r+3q)=beta_r-2M_(r,q) is unchanged coordinate by coordinate in each row.
All length-nine PAFs and energies are therefore unchanged in Z. The fixed
length-15 intermediates also remain unchanged. A nontrivial exchange involving
a fixed gauge position changes its landing label and hence its phase, so is
excluded; an equal-label exchange is simply a no-op. This proof retains the
actual m offsets, signs and positions and applies to all permitted moves.

## 2. Indexed factorization and exact change of norm

Use gamma=zeta^36, t=zeta^5, omega=t^3=zeta^15. Then zeta=gamma*t^2.
For i=r+3m_i,

    zeta^i*omega^a_i = gamma^i*t^(2r)*omega^(2L_i),

since 2i+3a_i=2r+3(2m_i+a_i), and 2L_i=2m_i+a_i modulo three.
Consequently the exact exchange in the affected active row sum is

    Delta F = c*t^(2r)*(gamma^i-gamma^j)
                            *(omega^(2q_j)-omega^(2q_i)).    (2)

Equivalently, for j-i=3d,

    Delta F=c*zeta^i*(1-zeta^(18d))
                            *(omega^(a_j-d)-omega^a_i).      (3)

The integer offsets in (1)--(3) precede exponent reduction. Both factors
retain the indexed information that a signed charge alone forgets. A
nontrivial exchange has Delta F!=0: 1<=d<=4, so the first difference is a
nonzero fifth-root difference; the second is a nonzero third-root difference.
In fact its pi valuation is exactly three, since the first factor is a unit
at pi and a nonzero third-root difference has valuation three. This does
not assert any particular valuation of the norm difference.

With F the old affected-row sum, ordinary norm expansion gives

    Delta S=Delta F*bar(F)+F*bar(Delta F)+Delta F*bar(Delta F). (4)

The other row does not change. This identity is standard, not a proposed
contribution. Integral-basis coefficients of (4) must all be divisible by
nine before any quotient is formed. Formula (2), direct endpoint subtraction,
and (4) supply independent checks in the bounded audit.

For a more informative criterion, put D_s=B_s'-B_s. Directly in the existing
signed phase events, for s=r+15*l, j0=(k+r) mod15, h=floor((k+r)/15),

    D_s=sum_(affected directed active edges k->j0) c_k*c_j0
       ([a_j0'-a_k'-h-l=0 mod3]-[a_j0-a_k-h-l=0 mod3]).       (5)

The fixed target cancels. For r!=0 there are at most four affected directed
edges: incoming and outgoing edges at each changed position. Count an edge
incident to both positions only once. Every summand has absolute value at
most one, so

    |D_s|<=4.                                               (6)

At shifts 0,15,30 the autocorrelations are phase independent and D_s=0.
Both compression maps of D vanish exactly: length 15 by the fixed
intermediates, length nine by the identical compressed rows. Also
Delta S=sum_s D_s*zeta^s. Applying the compression-domain lemma to **D** gives

    Delta S in 9O iff D_r=D_(r+15)=D_(r+30) mod9 for all r.   (7)

This application does not require G=0 at either endpoint: their difference
has zero G. In particular it remains valid for the J0=0 origin that fails
exact compression. It does not make that origin a conditional solution.

If Delta S is in 9O, division in the integral basis gives

    Delta J_k = (sum_(s in I_4)D_s-sum_(s in I_k)D_s)/3 mod3, (8)

where I_0=(30,35,40), I_1=(21,26,31), I_2=(12,17,22),
I_3=(3,8,13), I_4=(4,39,44). The inherited residue derivation is linear
on this compression kernel and justifies divisibility of the numerator by
three on (7). Equation (8) is the quotient of the **difference**, not an
assertion that either endpoint is itself in 9O. To call it J'-J we require
both endpoint domains independently. No reduction mod3 precedes division.

## 3. General local rigidity theorem

**Theorem.** Let p>3 be prime and fix valid factor-three intermediates of
length 3p with entries in {+1,-1,+3,-3}. Consider two phase assignments
differing at at most two active positions in total, and suppose their
combined length-nine compressed PAFs and energies agree exactly. Put
S=F_C bar(F_C)+F_D bar(F_D)-(9p+1)/2, and define S' similarly. Then

    S'-S in 9Z[zeta]  iff  B'=B  iff  S'=S.                  (9)

In particular, if both S and S' belong to 9O, every combined correlation
balance is unchanged, hence J'=J. For an exchange in a single row, the
individual affected-row PAF is unchanged as well.

Proof. Let N=3p and D=B'-B. The same directed-edge count as (5) gives
|D_s|<=4, including when one position changes in each row. At shifts 0,N,2N
the difference is zero. The two homogeneous compression maps vanish by
hypothesis. To verify (7) for general p rather than assume it, choose a
tensor basis gamma^r*t^v (r<p-1,v<6), gamma of order p and t of order nine.
The CRT reindexes D as H_(r,e); for v<6 and j=6+(v mod3), set
T_r=H_(r,v)-H_(r,j), for all p rows. The integral coefficients are T_r-T_(p-1).
The length-nine compression of D makes sum_r T_r=0. If Delta S is divisible
by nine, all T_r are equal mod9; p is invertible mod9, so all are zero mod9.
Conversely, their being zero implies coefficient divisibility. Under the
CRT these are precisely equality modulo nine of D_s,D_(s+N),D_(s+2N).
All three lie in [-4,4]; their pairwise differences lie in [-8,8], whose
only multiple of nine is zero. Thus they are equal as integers. Their exact
sum is zero from the length-N compression, so each is zero. This proves
Delta S in 9O implies B'=B. The remaining implications follow from
Delta S=sum D_s zeta^s, with equality implying divisibility. QED.

The argument is not exhaustive phase evaluation. Its mechanism is the gap
between a modulus of nine and the maximum eight-unit difference between
two layer changes. More generally it applies whenever each three-layer
set of D values has diameter less than nine, regardless of how many phases
changed. The uniform two-position bound is a convenient sufficient condition.
For three changed positions the crude bound is six, so the same argument
does not prove rigidity. No sharpness or sufficiency of three-position moves
is claimed, and none is explored computationally in this round.

There is nevertheless a useful necessary pattern for that next case. With
at most three changed active phases, |D_s|<=6. Under (7) and the exact
triple sum zero, each entry is divisible by three. A nonzero layer triple
in [-6,6] whose entries agree modulo nine must therefore be a permutation
of (6,-3,-3) or (-6,3,3). To attain magnitude six, a shift must have exactly
six distinct affected active directed edges, and all six signed indicator
differences must contribute the same plus or minus one. Any overlap or
missing edge reduces the possible magnitude below six. Thus a structural
proof excluding those saturated six-edge configurations would extend local
rigidity to three-position trades. This is a necessary pattern theorem,
not an assertion that such a trade is realizable. It uses no additional
phase assignments or higher valuation condition.

For the user's exchanges, the theorem proves the invariance candidate,
indeed the stronger equality of all correlations. It requires neither an
equal-phase cancelling edge nor a special sign/support pattern beyond the
stated minority-phase setup and exact preservation of compressed PAF/energy.
Gauge restrictions only select a subset of moves; they do not weaken the proof.

An immediate consequence is a distance bound: two assignments with the same
compressed PAF/energy data, both in 9O, and different combined correlation
vectors must differ at **at least three active phase positions**. The result
concerns arbitrary defects, including nonzero S, so is not a restatement of
the Legendre equation S=0.

### An explicit support hypothesis excluding a nontrivial domain edge

For a candidate pair i,j, suppose there is a nonzero base shift r for which
exactly one directed active edge in the affected row is incident to {i,j}.
Then no nontrivial exchange of these positions can have both endpoints in
9O. Indeed, the two phase increments are opposite nonzero residues. An edge
with one changed endpoint changes colour; an edge with both endpoints does
too, since its difference changes by plus or minus twice a nonzero residue.
Thus the single affected edge changes the three-layer vector D_(r+N*l)
by a permutation of (-1,0,1), up to an overall sign. This violates (7).
The statement depends only on indexed support, same-sign exchange eligibility,
and distinct landing labels; it covers a class of supports at any p>3.

Example: in the common C row, exchange positions 2 and 5. At base shift six,
2->8, 5->11 and 11->2 are absent because 8 and 11 are forced columns.
The sole affected active edge is 14->5, with weight +1 and boundary carry
one. At the strong 279 origin the exchange changes (a_2,a_5)=(0,0) to (2,1).
The edge's old colour is one and its new colour two, giving
(D_6,D_21,D_36)=(0,-1,1). This provides a short explanation of that move's
failure to stay in 9O, but not of the emptiness of the branch. The same
support obstruction also occurs in positive branch 277, so it is not a
branch-separating hypothesis. Ten of the 26 audited moves have this support
certificate; the others are not claimed to satisfy it.

## 4. Connectivity and what the theorem does not prove

Define N_(row,r,sign,q) to count the positive and negative landing labels
separately. The exchanges preserve every N, not just M=N_+-N_-. On the
unrestricted phase space with fixed gauge values, all assignments with the
same N are connected: subtract the fixed-position counts, then within each
row/residue/sign group match the multiset of labels on free positions by
transpositions. A misplaced label can be exchanged with a position carrying
its desired label; repeating terminates. Equation (1) recovers unique phases.
This is a proof of connectivity **before** restricting to S in 9O.

That connectivity proof supplies no path remaining in 9O. In the graph
induced by the full domain, the theorem makes B (and S and J) constant on
each connected component. Different B values cannot be joined by permitted
domain-preserving exchanges. Merely walking through a point outside 9O
invalidates the invariance argument.

Even the unrestricted N-fibers need not cover an entire signed-charge fiber
as one connected set. For example, one free positive and one free negative
position in the same residue class may both have label 0 or both label 1.
Their signed contribution M is zero in either case, but their separate N
vectors differ. No same-sign label exchange connects the two N patterns.
This is a generic charge example, not a claimed full-domain branch witness.

Thus the theorem does not say that the residue of the strong 279 witness
is shared by its whole signed-charge fiber, let alone all exact compressed
rows in branch 279. To deduce emptiness one would need a structural
classification of all relevant domain components/charge patterns with a
nonzero invariant on every component, or another global obstruction. No
such coverage or classification is asserted.

## 5. Bounded audit and active challenges

The three origins and every permitted neighbor are independently decoded
into binary rows. Direct binary compression and PAFs check the charge and
event implementations. Each endpoint's 24 integral coefficients and tensor
coefficients independently determine its full-domain flag. The difference
test (7) is cross-checked, not substituted for an endpoint check. Both indexed
factorizations, direct Delta F, norm expansion, event differences and direct
binary PAF differences agree. The gauge and the four-edge bound are checked.

|origin masks|sign/residue rejection|gauge rejection|no-op|nontrivial neighbors|neighbors in 9O|
|---|---:|---:|---:|---:|---:|
|(22487656929184,11681458143385), 277|104|1|9|7|0|
|(442312790436,2830005805622), 279|104|4|4|9|0|
|(31210651353580,20580563788346), 279|104|2|5|10|0|

There are 363 distinct raw pairs and 26 distinct nontrivial endpoints. The
three pilot endpoints are reused in the final evidence, not expanded again.
The audit's lack of a counterexample would by itself be vacuous evidence for
invariance on nontrivial in-domain edges: no such edge was found. Section 3's
general proof is what establishes the invariant. With every permitted
one-step move exhausted, each of these three origins is isolated in the
specified induced 9O exchange graph (ignoring no-op loops). This is a local
finite fact, not a claim to classify all of that graph's other components.

The third origin has J=(0,0,1,1) and G=(0,6,-3); every neighbor has those same
nonzero compression balances. It is used only as a 9O origin with failed
compression, never as a conditional solution. The first two origins have
exact compression and J respectively (0,0,0,0) and (1,0,2,2). Their neighbors
preserve exact compression but fail the full domain, and are assigned J=null.

For example, the first C(2,5) neighbor of the strong 279 witness has masks
(446608806272,2830005805622). It has the same integer compressed rows, but
the constant coefficient of Delta S is 2. Since the origin is in 9O, that
endpoint is outside 9O. It is a counterexample to *compression alone implies
full-domain preservation*, not to the candidate conditional invariance.
The first nonzero Delta S coefficients for the first positive-277 and
J0=0-origin neighbors are respectively 1 and -4, also excluding 9O directly.

To challenge an overextension of the bound, the tests use one explicit
abstract symmetric integer D array. In tensor coordinates, put (-6,3,3)
at e=(0,3,6) in rows 1,4 and its negative in rows 2,3; all other entries are
zero. Both compression maps vanish and Delta S is a nonzero member of 9O.
Its layer diameter is nine and max |D_s| is six. Thus the small-diameter
hypothesis is essential to the lattice argument. This is **not** a phase
witness or a three-position exchange; it establishes no sharpness claim
for realizable phase moves. No additional phase assignments were generated.

## 6. Primary literature and originality

Accessible primary texts checked October 16, 2026:

* Djokovic and Kotsireas, [Compression of Periodic Complementary Sequences
  and Applications](https://arxiv.org/html/1302.0571), Section 2's norm and
  involution, and Section 5, Theorem 3, equations (18)--(19) and proof.
  This is the standard exact compression framework. The norm expansion
  and preservation of compressed PAFs are not new principles.
* Turner, Kotsireas, Bulutoglu and Geyer,
  [Legendre pair of length 77 using complementary binary matrices with fixed
  marginals](https://arxiv.org/pdf/2101.10918), Theorem 2.1, printed p.4;
  simultaneous-decompression constraints (8), pp.6--7; Theorem 3.4 and
  Corollary 3.5 with proof, pp.11--12; Section 4 opening, p.12. These give
  the fixed-marginal and primitive-frequency precedents. The read results
  do not provide the specific two-active-position/9O rigidity statement.
  This limited comparison is not a proof of its novelty.
* Ellison, Jouve and Stone, [Switching checkerboards in (0,1)-matrices](https://blogs.univ-tlse2.fr/jouve/files/2023/10/published-paper.pdf),
  Linear Algebra and its Applications 680 (2024), Section 1, printed p.276:
  switches preserve row/column sums; their Theorem 1 credits Ryser (1957)
  for connectivity at fixed marginals. A landing-label assignment is a
  one-hot matrix within each row/residue/sign group; our transposition is
  this familiar switching operation. Fixed-marginal connectivity supplies
  no connectivity after adding the arithmetic restriction. The original
  Ryser article was not read here; the accessible primary research paper
  establishes the provenance of the comparison, not a new connectivity claim.

The publisher URL for [On properties of Legendre pairs under compression](https://doi.org/10.1145/3747199.3747549)
again returned HTTP 403 on direct opening. Search-index text exposed an
introduction and references to later sections; these were not treated as
access to the complete algorithms or a sufficient basis for priority claims.
The earlier full-algorithm and other publication-audit gaps remain unresolved.

The specific candidate contribution from this round is the uniform local
rigidity theorem (9), its minimum-three-position consequence, and the
single-affected-edge support criterion. Their ingredients are elementary
compression arithmetic and a bounded signed-event count. They are proved
statements about a class of lengths and supports, not finite separations,
but whether the specialization is original or substantial enough for a
research paper remains unresolved. There is still no explanatory theorem
for an entire empty conditional fiber. Retain the narrower reproducibility/
software assessment; do not infer submission readiness or any priority
regarding the reported order-668 construction.

## 7. Direction and reproduction

**Continue the mathematical direction narrowly, not a two-position walk.**
There is now a provable restriction on how the full-domain phase space can
change its correlations. A walk using these exchanges cannot alter S or J
while staying in 9O, and the three audited origins are isolated. The concrete
next target is an analytic classification of charge-preserving trades that
can change B while remaining in 9O: they must change at least three active
positions and produce a layer difference of diameter at least nine. For
three positions, first determine whether the saturated six-edge patterns
just proved necessary are compatible with the indexed signs and phase
differences. Determine this before proposing computation. These conditions
are necessary, not sufficient. No such
larger moves or multistep paths were run in this round.

An empty-fiber explanation would additionally need component/charge-pattern
coverage and a nonzero invariant on every relevant component. Without that,
the strong witness's J=(1,0,2,2) cannot be exported to the rest of branch 279.

```powershell
.venv/Scripts/python.exe -m scripts.audit_phase_exchange pilot
.venv/Scripts/python.exe -m scripts.audit_phase_exchange audit
.venv/Scripts/python.exe -m pytest tests/test_phase_exchange.py -q -p no:cacheprovider --basetemp=tmp/pytest_phase_exchange
.venv/Scripts/python.exe -m scripts.package_phase_exchange
```

The pilot evaluated three nontrivial endpoints in 0.0207 seconds and
projected 12.55 seconds for the maximum raw-pair budget with a fivefold
margin. The final audit took 0.0581 seconds, including checks on 23 further
endpoints and reuse of three pilot records. One worker, 120-second internal
cap, estimated 150 MB memory and 1 MB new storage; estimates are not peak
measurements. No cap was hit. No completed census was rerun. Four focused
tests cover independent factorizations, the actual endpoint domains, the
single-edge criterion, and the necessity of the lattice bound.

The package pins new notes, code, tests and evidence. It verifies all 6,764
inherited result files, all five paper files, earlier manifests and the
inherited raw-byte aggregate, preserving the two pinned CRLF exceptions.
The manuscript hash remains
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.
The manuscript was neither edited nor compiled; no PDF/layout claim is made.
