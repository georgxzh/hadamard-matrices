# Global charge coverage and the missing primitive information

Research round: October 20, 2026. Base
`2b7e9c712c23cf859e1bd54146f8a39bc2424724`, branch
`agent/order-428-reproduction`. Initial tree clean. No project AGENTS.md or
CLAUDE.md found. Read the three-phase theorem, preceding compression/residue,
carry and star-cut notes, phase propagation, exact endpoint implementation,
and frozen witnesses. No manuscript or inherited evidence is edited.

**Outcome:** a global limitation theorem, not an empty-fiber theorem. Complete
signed-charge realizability is characterized by (1)--(3); the two branches
have identical attainable compressed PAF data by explicit transport for all
assignments. Universal preservation of the primitive row norm under that
transport is possible exactly for a common cyclic displacement, which these
D supports forbid. This identifies a precise information loss. It does not
characterize the image after imposing full 9O, establish originality, or
upgrade the narrower publication assessment.

## 1. Audit and selection before new phase computation

The previous three-position proof remains valid: the signed triangle
classification, six distinct edge bound, integer homogeneous compression
lemma, and the two flank alignment equations retain their hypotheses.
Its three-active-position support and the five-active-position bound are
fixed by the intermediates. Its *uneven charge* hypothesis is not: it is
E_b=sum_q M_(b,q)^2>3 for three equal signs, or >1 for mixed signs. This
condition is constant only after a particular charge vector has been fixed.
Full 9O is a separate endpoint hypothesis, not a consequence of these data.

Reading the seven saved records already refutes an attempted global coverage
lemma: exact compression does NOT force unevenness in both rows. The saved
279 witness (22964264347100,2872821395978) has exact compression, C thin
charge (2,0,1), and D thin charge (0,1,0). It is outside 9O. Therefore it
refutes only the compression-only implication, not the same implication
with full 9O added. The latter is open; no coverage is inferred from the
two saved exact-compression/full-domain origins.
This does not settle whether C's thin class alone must be uneven under
exact compression. That narrower implication is also left unresolved;
the exceptional D class is enough to refute coverage of both row hypotheses.

**Selected global candidate (limitation theorem).** For every third-gauged
assignment on either branch 277 or 279, there is a third-gauged assignment
on the other branch with the same individual length-nine compressed PAFs,
energies, and thin-class charge energies. Hence their entire attainable
sets of those data agree, also after imposing the exact compression target.
The stronger unanchored statement preserves the complete charge vectors.
This is a statement over all assignments, not an enumeration of charge
vectors. It does NOT assert transport preserves 9O or exact lifting.

Mechanism: sign/residue-preserving transport of landing labels, with the
single D anchor restored by a whole-row phase shift. The C row and its two
gauges are unchanged. A closed integer feasibility/count formula below gives
coverage of all charge vectors, including exceptional classes. This route
can settle the scope of compression-only coverage globally; it cannot by
itself settle the remaining primitive-domain restriction.

Falsification test: construct that transport on the saved positive, strong
279, J0=0, and other saved records, and compare integer compressed data and
independently computed full S. One deterministic map per direction, no
search over maps. A pilot transports only the positive; at most seven
new assignments total, reusing the pilot. One worker, 120-second cap;
preflight estimates 200 MB memory and 2 MB storage. No move graph, census,
four-position trades, or adaptive expansion is authorized by this plan.

The missing lemma is NOT fixed-marginal connectivity. It is a restriction on
which indexed allocations at each feasible M satisfy full 9O and which
primitive defects they attain. Even if unevenness held on all those
allocations, local constancy on components would not make their constants
equal or nonzero. The norm-transfer theorem below identifies the information
erased by charge transport. It is not a rewriting of S=0: it characterizes
when a fixed transport preserves a row norm for *every* phase assignment.

## 2. Complete integer charge feasibility, with fixed gauges

Let N=3p, length 9p, p>3 prime, i=r+3m_i and
L_i=m_i+p*a_i mod3. All phases are ternary. Fix any collection of phases
(including the three actual gauges). In each (row,r) group subtract the
fixed signed contributions f_q from proposed M_q and write R_q=M_q-f_q.
Let P and Q be the numbers of remaining positive and negative active signs.
Then M is realizable, with these gauges, if and only if

    sum_q R_q=P-Q,                 sum_q |R_q| <= P+Q.       (1)

Proof. If U_q,V_q are the positive/negative occupancies, then U-V=R,
sum U=P, sum V=Q. Necessarily (1) holds. Conversely put

    U_q=max(R_q,0)+k_q,   V_q=max(-R_q,0)+k_q,
    sum k_q=K=(P+Q-sum |R_q|)/2,       k_q>=0.               (2)

K is a nonnegative integer: |R_q|=R_q mod2 and the first equation in (1)
give parity. Any distribution of K among the three labels supplies U,V.
Assign these labels to the distinct signed positions and recover
a_i=p^(-1)(L_i-m_i) mod3. Thus no indexed position or integer offset is
dropped; the inverse exists since p is coprime to three. Different groups
are independent at this feasibility stage.

The exact number of gauged assignments in one group is the closed formula

    H_(P,Q)(R) = sum_(k0+k1+k2=K) P! Q! /
      product_q ((max(R_q,0)+k_q)! (max(-R_q,0)+k_q)!).      (3)

It is zero when (1) fails. Multiplying (3) over all six groups counts the
entire fixed-charge phase fiber, NOT the subset in 9O or the exact lifts.
This is an elementary signed occupancy/multinomial formula, not a new
general counting principle or a hidden phase census.

Let beta_r be the sum of the column signs, including inactive columns.
The exact compressed row is X_(r+3q)=beta_r-2M_(r,q). For t, put
r'=(r+t) mod3 and h=floor((r+t)/3) in Z. Its PAF is exactly

    sum_(r,q) (beta_r-2M_(r,q)) (beta_r'-2M_(r',q+h)).       (4)

Equations (1),(4) are therefore a complete characterization of attainable
length-nine compressed rows and their PAFs at fixed intermediates/gauges.
For our branches the combined targets are 82 at zero and -10 otherwise.
No full-9O claim is part of this characterization. Marginals constrain
charges nontrivially; the statement is not that they are unconstrained.

## 3. Global transport theorem

Suppose two indexed rows have equal beta_r and equal counts of positive
and negative active signs separately in every residue r mod3. Choose any
bijection phi between their active positions preserving r and sign. Define

    L'_(phi(i))=L_i,
    a'_(phi(i))=a_i+nu_i mod3,
    nu_i=p^(-1)(m_i-m_(phi(i))) mod3.                        (5)

It preserves every integer M and the compressed row by (4). This is a
bijection before gauges, with the inverse induced by phi^(-1). If a row
has one fixed anchor, subtract its new anchor phase k from every phase of
that row. This sets that anchor to zero; all landing labels shift by -p*k,
so the compressed row is cyclically shifted by -3p*k modulo nine. Its PAF
and each charge-class energy are unchanged. Conversely the same construction
works in the opposite direction. We assert equality of attainable sets,
not a bijection between all fixed-gauge charge fibers with identical M.
With multiple pinned phases the normalization step is not generally valid;
the theorem requires their preservation by (5), or leaves that row unchanged.

For 277 and 279, C is identical and stays fixed. In D the per-residue
(positive,negative,beta) triples are (1,3,-3), (2,1,1), (3,1,3) in both.
Take the increasing-order matching within each sign/residue group:

    source D277 i:  1  2  3  5  6  7  9 11 12 13 14
    target D279 j:  4  2  0 11  3  7  6  5 12 13 14.        (6)

Use its inverse in the other direction, then restore the sole D anchor.
The C gauges (concatenated active indices 0,1) and D gauge (index12) are
all retained. Thus (5) proves the selected candidate for EVERY assignment,
and not just the saved witnesses. Imposing (4)'s exact target or an arbitrary
predicate of the individual compressed PAFs and thin-class energies leaves
the equality of attainable sets intact. Exact compression cannot distinguish
these indexed branches at that level of information.

Consequently any obstruction expressed only through those shared profiles
and compressed data which excludes *all* compression-admissible 279
assignments would also exclude the transported frozen positive data.
Such an obstruction cannot be a necessary condition for exact lifting.
This limitation does not apply to a condition using the indexed primitive
norm to restrict the set of admissible charges first.

## 4. What is lost: universal norm-preservation criterion

Put eta=zeta^9 (order p). Choose integer representatives for nu_i in (5).
The integer

    d_i=phi(i)-i+N*nu_i

is divisible by nine, by the defining congruence; let k_i=d_i/9 mod p.
Before the harmless anchor normalization, the affected row satisfies

    F'=sum_i c_i*zeta^i*omega^a_i * eta^k_i,
    Delta F=sum_i c_i*zeta^i*omega^a_i*(eta^k_i-1).           (7)

Every carry is included in the integer d_i before division. Reducing a
phase representative changes d_i by 9p, so eta^k_i is well defined.
The row's exact norm difference is

    sum_(i!=j)c_i*c_j*zeta^(i-j)*omega^(a_i-a_j)
                                      *(eta^(k_i-k_j)-1).  (8)

Anchor normalization multiplies F' by a third root, leaving this norm
unchanged. Formula (8) exhibits precisely the pairwise indexed differences
forgotten by M, with no division of S or weakening of its domain.

**Theorem.** With at least two active positions and at most one pinned
phase, (5) preserves the row norm for every allowed phase assignment if
and only if all k_i are equal modulo p.

Proof. Sufficiency is a common unit factor in (7). For necessity regard
(8) as a complex-valued function on the ternary phase cube, fixing one
anchor to zero if desired. The characters omega^(a_i-a_j), i!=j, are
pairwise distinct: with one anchor they have exponent vectors e_i-e_j,
e_i, or -e_j in F3^(n-1). None coincide, including when n=2 since +1 != -1
in F3. Finite-character orthogonality therefore forces every coefficient
of an identically zero function (8) to vanish. Its prefactor is nonzero,
so eta^(k_i-k_j)=1 for every i,j. QED. No phase evaluation is part of this
proof. More than one pinned phase could merge characters and is excluded.

For (6), the old positions 1 and 2 have k_1=2 and k_2=0 modulo five.
Their signed edge supplies a nonzero coefficient proportional to
eta^2-1 in (8). Thus this transport is not universally norm preserving,
despite universal exact charge preservation before normalization. In fact
no residue/sign matching of these D rows can be universally norm preserving:
constant k would require the active signed support to be a cyclic translate
by 9k mod15. Their inactive positions of residue two are both {8}; this
forces that translate to be zero mod15. Their active supports then differ
(position 0 is inactive only in 277), a contradiction.

This is a general algebraic limitation on compression-preserving transport,
not a statement that every assignment changes norm, nor that it changes J,
nor that norm changes cannot be multiples of nine. A conditional identity
on G=0 and 9O would need additional information and is not disproved by
character independence on the larger cube.

## 5. Bounded validation and final assessment

The single-positive pilot took 0.01996 seconds and projected 0.69852 seconds
for seven transports with a fivefold margin. The audit took 0.05163 seconds,
reusing the pilot endpoint and constructing just six more. These are direct
transports between branches, not moves within a branch or multistep paths.
No search over maps, charges, phases, or graph components was performed.

Each source is independently rechecked against its saved masks, S, G and
domain. Each target is independently decoded to binary rows, compressed,
and checked using its integer norm coefficients and the integral tensor
basis. Exact formula (7), norm expansion and reverse transport are checked.
Only when G=0 is the inherited equivalence

    S in 9O iff B_r=B_(r+15)=B_(r+30) mod9 for every r       (9)

invoked, with the other exact compression supplied by valid intermediates.
This equivalence follows by coefficient comparison in the integral
fifth-root/ninth-root tensor basis and the homogeneous compression sums,
as proved in `compression_residue_coupling.md`, Proposition 1. It is not
used on an endpoint with failed exact compression. No Q test or expectation
is substituted. The coefficient S_0 below is in the standard integral
basis 1,zeta,...,zeta^23.

| Source branch, first mask | Source G0,G1,G2 | Source full 9O / J | Target second mask | Target S_0 |
|---|---|---|---|---:|
| 277, 22487656929184 | 0,0,0 | yes / (0,0,0,0) | 9405125214970 | -1 |
| 277, 18570512807384 | 0,6,-3 | yes / (0,0,1,1) | 18269935608570 | -5 |
| 279, 31210651353580 | 0,6,-3 | yes / (0,0,1,1) | 20511827012217 | -1 |
| 279, 416258831260 | 6,0,0 | yes / (1,0,1,1) | 11780645031997 | -2 |
| 279, 428621558224 | 0,3,3 | yes / (2,0,0,0) | 2404597219929 | 2 |
| 279, 442312790436 | 0,0,0 | yes / (1,0,2,2) | 11681324191889 | 12 |
| 279, 22964264347100 | 0,0,0 | no / undefined | 20022552265305 | -2 |

Targets use the other branch, retain the first mask, and have exactly the
same G as the source. Every displayed target S_0 is nonzero modulo nine,
so every target is outside full 9O and has J undefined. In particular the
new branch-279 pair `(22487656929184,9405125214970)` has both exact
compressions and the same individual compressed PAFs as the positive
solution, yet S_0=-1. It is an explicit counterexample to extending the
transport theorem to preservation of primitive divisibility or exact lifts.
Its failing hypothesis is the common-displacement criterion in Section 4,
not a lost gauge or an approximate compression check.

The saved J0=0 source and its image fail exact compression. The strong 279
source has G=0 and full 9O; its image preserves G but not the primitive
domain. The earlier outsider has G=0, Q divisible by three, and balanced
D thin charges, but no J. All these roles remain distinct. The 54 saved
mean-zero construction members were read, not regenerated: none has G=0
or full 9O, while their saved B,G,Q,S sums vanish. They remain relaxation
witnesses only; no conditional conclusion is drawn from their mean.

Formula (3), without generating those fibers, gives 864 gauged assignments
at the positive source's exact M and 360 at its normalized target's M.
At the strong 279 source and its target it gives 810 and 4860. These are
counts BEFORE primitive-domain filtering. They do not count exact lifts,
prove multiple autocorrelation classes, or imply connectivity. The differing
counts are consistent with the transport theorem: normalization can send
one fixed-M fiber to more than one cyclic orientation of target M. It is
not asserted to be a bijection of those particular fixed-M fibers.

Four tests passed in 0.18 seconds. Besides the recorded endpoint/domain
checks, an independent Laurent-coefficient dynamic program verifies (3)
for abstract P,Q from zero through four, including impossible residuals.
This is small occupancy algebra, not additional branch assignments.
Character exponent vectors for 2 through 12 active positions are checked
for distinctness, supporting but not replacing the general proof.

## 6. Exactly what global coverage has and has not been obtained

For a branch b, let A_b be the signed-charge vectors realizable with its
gauges and satisfying all exact length-nine target equations. Equations
(1)--(4) characterize A_b completely without phase enumeration. The
transport theorem identifies the whole image of A_277 and A_279 in
individual compressed PAFs and thin-class energies (indeed, charges modulo
the allowed D label rotation). This is genuine universal coverage of the
compression projection, not just evidence from seven records.

Let A_b^9 be the subcollection admitting at least one allocation with full
S in 9O. No characterization of A_b^9 is proved. In particular the following
possible coverage lemma remains OPEN, not supported merely by the saved
origins: every allocation with G=0 and full 9O has uneven thin charges in
both rows. The saved outsider refutes that statement without 9O; the J0=0
witness refutes it without G=0. Neither refutes their conjunction. We did
not search for an actual counterexample to the conjunction beyond saved
evidence, and do not claim it true.

Even this lemma, if proved, would give only uniform local rigidity. It
would not prove that every homometry class over A_279^9 has nonzero J, or
exclude an exact lift. The missing all-class primitive restriction is the
central research gap. Equality of attainable compressed PAF sets is not
equality of attainable length-45 PAF sets; the universal norm-transfer
criterion explains why such an inference is invalid.

Sections 2--4 generalize to length 9p, p>3 prime, with the stated matching
profiles and gauge restrictions. The counting/transport parts actually
require only gcd(p,3)=1; primality is used for the present primitive-field
setting and order-p factor notation. No other length was searched. The
character argument applies to any nonzero signed coefficients and at most
one pinned phase in the affected row. It is not a claim about arbitrary
maps, sign-changing permutations, conjugating maps, or identities valid
only on a conditioned subvariety.

## 7. Primary literature and originality

Accessible primary portions read October 20, 2026:

* Djokovic and Kotsireas, [Compression of Periodic Complementary Sequences
  and Applications](https://arxiv.org/html/1302.0571), Section 5, Definition 3,
  equations (18)--(19), Theorem 3 and its proof. The exact PAF folding in
  (4) is established compression theory. Our occupancy coordinates do not
  make it new.
* Turner, Kotsireas, Bulutoglu and Geyer, [Legendre pair of length 77 using
  complementary binary matrices with fixed marginals](https://arxiv.org/pdf/2101.10918),
  Section 3, printed pp.9--10 (binary matrices with fixed marginals and
  Theorem 3.3); pp.10--12 (remaining primitive frequencies, Theorem 3.4,
  Corollary 3.5 and proofs). Their framework already separates simultaneous
  compression from the remaining primitive-frequency condition. These
  portions, rather than an asserted complete algorithm audit, support our
  comparison. The signed occupancy formula is elementary multinomial
  bookkeeping within this established setting.
* Adrian Dobra, [Dynamic Markov Bases](https://arxiv.org/pdf/1103.4891),
  Section 1, printed p.2, definition of moves and the requirement that a
  Markov basis still connect the reference set. No connectivity claim here
  follows from exhibiting local moves; additional arithmetic conditioning
  changes the set to be connected. The original Diaconis--Sturmfels text
  cited there was not read this round.
* Grimm and Baake, [Homometric Point Sets and Inverse Problems](https://sfb701.math.uni-bielefeld.de/preprints/sfb08073.pdf),
  Section 2, printed p.2, weighted-difference definition and finite example
  (1). Autocorrelation ambiguity is established. Their Euclidean point-set
  framework is not itself a classification of these finite cyclic lifting
  fibers, and equality after compression is weaker than full homometry.

Finite-character orthogonality, multinomial counting, norm expansions and
compression are standard ingredients; no originality is claimed for them.
The candidate contribution is their precise use to prove complete charge
projection coverage, branch indistinguishability at that projection, and
the common-displacement criterion for norm-preserving transport. These
are proved specializations with a practical limitation consequence, but
neither originality nor sufficient mathematical significance for a research
paper is established by the sources checked. The limited comparison is not
an exhaustive priority search. Earlier inaccessible full fast-spectral and
pq-squared algorithm details, historical representative-list access, and
external replication gaps remain unresolved. Those texts were not newly
obtained or inferred from abstracts in this round. No authors were contacted.

Retain the narrower reproducibility/software assessment. A global
empty-fiber theorem remains missing. The present advance is an explanation
of why a whole class of proposed explanations loses necessary information,
not achievement of the original empty-fiber goal or submission readiness.
This assessment is independent of order-668 construction priority.

## 8. Decision, commands, and preservation

**Pivot away from compression-only charge exclusions and incremental local
move exploration.** They have reached a proved limitation for these two
branches. Do not spend the next round classifying more moves, enumerating
charge fibers, or assuming that charge feasibility describes A_b^9.

A justified continuation would require a new indexed primitive lemma:
control the coefficients in (8), with their nonconstant fifth-root factors,
on *all* allocations satisfying G=0 and full 9O. A concrete falsification
benchmark is that it must accept the positive source, distinguish its
compression-identical transported target, and still address the strong
279 source which passes 9O. No such conditional identity is proved or
proposed as already sufficient here. Without an analytic candidate meeting
that benchmark, stop this branch-specific route rather than commission
another bounded separation experiment. Do not consolidate a research
submission on these local/limitation results alone.

```powershell
.venv/Scripts/python.exe -m scripts.audit_global_charge pilot
.venv/Scripts/python.exe -m scripts.audit_global_charge audit
.venv/Scripts/python.exe -m pytest tests/test_global_charge.py -q -p no:cacheprovider --basetemp=tmp/pytest_global_charge
.venv/Scripts/python.exe -m scripts.package_global_charge
```

One worker, internal 120-second cap, estimated 200 MB memory and 2 MB
storage; these are conservative preflight estimates, not measured peaks.
No cap was reached. Only seven deterministic target assignments were
constructed, with the pilot reused. No census or move graph was run.
`results/global_charge/manifest.json` pins new code, notes, tests and evidence
with SHA-256. The integrity package checks all 6,774 inherited result files,
all five paper files, previous manifests and the preceding raw-byte aggregate,
preserving the two recorded legacy CRLF exceptions. The manuscript hash is
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.
It was neither edited nor compiled. All frozen p=5/p=7 evidence is preserved;
no new independent-external-replication or PDF-layout claim is made.
