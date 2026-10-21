# Primitive projection: a global identity and a research-program stop rule

Research date: October 20, 2026. Verified before beginning: local HEAD and
origin/agent/order-428-reproduction both equal
`44f0f1786c5a23f4231e2dcebea04acf1cce4fcb`; initial tree clean.
No project AGENTS.md or CLAUDE.md found. Read the latest global-charge note,
three-position proof, compression/residue and carry proofs, primitive-local
and phase-moment records, conditional-fiber theorem, phase propagation,
exact arithmetic implementation and frozen controls. No inherited artifact
or manuscript change is permitted in this round.

**Outcome:** no substantive original breakthrough. The strongest completed
formula is the exact primitive trace/projection identity (2), with a complete
kernel description (6). These are specializations of established Fourier
and cyclotomic theory. The selected prime-cycle mechanism collapses to the
original lifting equations; its hoped-for support-specific exclusion was
not proved. A precise relaxation counterexample and the pure-product
obstruction explain two failed shortcuts. Recommend stopping incremental
branch-279 obstruction work and changing the construction strategy, not
upgrading the manuscript or manufacturing a new theorem claim.

## 1. Critical assessment and three candidates, before computation

The strongest established pieces are: the exact carry-sensitive residue
formula on full 9O; the homogeneous compression/divisibility equivalence;
the support-and-charge local rigidity theorem; and global compression-profile
transport with its universal norm-preservation criterion. The prime-kernel
orbit count is useful but its central obstruction has a close antecedent.
None characterizes all primitive norms over every attainable signed charge.
That is the bottleneck, not another phase symmetry or compression identity.

Known dead ends have precise scopes. Identical margins cannot separate
277/279. Their entire attainable compressed PAF sets agree. Unconditional
affine intervals contain zero by a genuine-phase barycenter. Moment and
mod-nine conditions admit actual strong false positives. Local two/three
position rigidity does not connect a restricted fiber. Fixed-charge
transport can leave 9O. Increasing those move sizes or valuation thresholds
without a new global lemma has no credible explanatory bridge.

Three genuinely different candidate mechanisms were considered:

**A. A global primitive-energy lower bound.** For every gauged allocation
of branch 279 with exact G=0 and full S in 9O, prove W>0, where
W=p*sum_s B_s^2-sum_t G_t^2. Hypotheses retain the entire indexed phase
model; on these hypotheses W>0 would rule out an exact lift. Mechanism:
an exact relative-frequency projection followed by a support-dependent
sum-of-squares lower bound. The positive 277 has W=0 and must be admitted.
The strongest obstacle is that compression-identical assignments can
have different primitive defects, while the known support bounds and
local rigidity provide no strictly positive term on all charge classes.
The missing lemma is a nonzero indexed square forced on every such 279
allocation. Merely proving W>=0 is not progress toward that lemma. It is
not selected for an optimization or search: no credible strict bound has
emerged from the existing equations.

**B. A prime-cycle obstruction after removing signed cancellation.** For
each layer triple subtract its integer minimum, obtaining R>=0 with a
zero in every triple. An exact lift would make R vanish at a primitive
9p-th root. The proposed global mechanism is to use the indexed signs to
exclude the necessary p-cycle decomposition, uniformly for branch 279,
while allowing the positive 277. Lam--Leung supplies the decomposition
theorem, not the support-specific exclusion. The strongest known warning
is that the positive control has R=0: a universal argument that simply
forbids all cycles would also need to exclude this zero case using indexed
realizability. The decisive missing lemma is an exclusion of the required
cycle capacities for all allowed phase allocations, independent of solving
B=0. This is selected for analytic scrutiny: it has a complete global
classification theorem behind it and a short route to determining whether
that theorem actually supplies new information. No novelty is presumed.

**C. A CRT product lifting construction.** For coprime odd m,n>1 (here
m=p,n=9), seek binary A,C of length m and B,D of length n such that
x(r,t)=A(r)B(t), y(r,t)=C(r)D(t) is a Legendre pair with the requested
compressions. A proof would supply an explicit lifting procedure for a
structured family rather than explain an arbitrary empty branch.
Factorization of PAFs is the proposed mechanism. The mandatory obstruction
is a shift along only one CRT coordinate: its combined PAF is a multiple
of n and cannot equal -2. Section 5 proves this immediately. There is no
missing lemma that can repair this literal ansatz. A nonseparable switching
construction is a different problem; no expansion to it is silently made.
Known Golay/quaternary product constructions cannot be imported as binary
odd-length Legendre constructions without proving the changed equations.

B has the most credible finite analytic investigation, although its
potential significance depends entirely on a noncircular support lemma.
A would be consequential if its strict inequality were proved, but the
formula alone does not justify substantial computation. C is rejected
algebraically. All selection and proofs below precede the bounded audit.

## 2. Exact variables and the global projection formula

Let p>3 be prime, N=3p, L=9p. Use a binary preimage of valid fixed factor-three
intermediates, phases in {0,1,2}, with the original three gauges. The exact
indexed phase formula is retained: for s=r+N*l, j=(i+r) modN and
h=floor((i+r)/N),

    B_s=sum_(both rows, active directed edges) c_i*c_j
                [a_j-a_i-h-l=0 mod3] - t_r.

The constants t_r are the existing integer targets; B_0=B_N=B_(2N)=0.
Thus B_s=(PAF_x(s)+PAF_y(s)+2)/4 off zero, B is symmetric, and
sum_(l=0)^2 B_(r+Nl)=0. Put G_t=sum_(k=0)^(p-1) B_(t+9k).
Exact second compression means G=0 in Z, including energy. Set

    S=sum_s B_s*zeta^s,
    E_s=p*B_s-G_(s mod9),
    W=p*sum_s B_s^2-sum_(t=0)^8 G_t^2.                     (1)

For actual phases S is precisely F_C*bar(F_C)+F_D*bar(F_D)-(9p+1)/2.
The following statements hold more generally for any real integer array
B with its first homogeneous compression zero; they do not assert that
every such array is realizable by phases.

**Proposition (exact primitive projection).**

    sum_(s=r modN) E_s=0,       sum_(s=t mod9) E_s=0,
    E(zeta)=p*S,
    sum_s E_s^2=p*W,
    Tr_(Q(zeta)/Q)(S*bar(S))=9*W.                          (2)

In particular W>=0 and W=0 iff S=0. On G=0 this becomes
W=p*sum B_s^2. This is a global identity, but not the strict lower bound A.

Proof. For the nine-folding, sum(pB-G)=pG-pG=0. The three G entries at
t,t+N,t+2N sum all B entries in one residue modulo three, which is zero
by the first compression. This proves the other folding. The polynomial
with coefficients G_(s mod9) vanishes at zeta by the p-cycle geometric
sum. Expanding the square uses sum_s B_s G_(s mod9)=sum_t G_t^2 and
sum_s G_(s mod9)^2=p*sum_t G_t^2, giving the third identity.

For the trace use the Ramanujan coefficient

    c_(9p)(d)=9p*[9p|d]-3p*[3p|d]-9*[9|d]+3*[3|d].       (3)

Indeed c_p(d)=p*[p|d]-1 and c_9(d)=9*[9|d]-3*[3|d], and their product
is c_(9p)(d). Expanding Tr(S*bar(S))=sum_(s,t)B_s B_t c_(9p)(s-t),
the first term is 9p sum B_s^2, the second and fourth vanish by the
homogeneous first compression, and the third is -9 sum G_t^2. This proves
the trace identity. A nonzero algebraic number has positive sum of squared
absolute values over embeddings, so W=0 iff S=0. Equivalently this follows
from the tensor-basis proof in Section 3. All divisions in (1)--(3) are
exact identities, not modular approximations.

No replacement of full 9O is made: it is checked independently in the
integral cyclotomic basis. The statement W>=0 holds outside that domain
too. On G=0 the inherited triple-congruence test is equivalent to full
9O; without G=0 it is not used. In particular a trace congruence alone
does not test full coefficient divisibility or permit forming J.

## 3. Selected cycle route: complete elimination exposes circularity

Define m_r=min(B_r,B_(r+N),B_(r+2N)) in Z and

    R_s=B_s-m_(s modN).                                    (4)

Then R>=0, each N-layer triple has a zero, and R(zeta)=S because the
subtracted part is a sum of exact three-cycles. The p=5 indexing, phases,
signs and carries are those in Section 2; (4) changes coefficients, not
the phases or their gauge. It does not turn R into another phase assignment.

Lam--Leung's Theorem 3.1 and Corollary 3.4 imply that a nonnegative
vanishing sum at order 9p is a nonnegative integer sum of rotated three-
and p-cycles. The prime-power reduction must be included; applying only
the square-free formula at order 3p would miss rotations. Since every
three-cycle support in R has a zero, none can occur with positive weight
in such a decomposition. The remaining p-cycles are exactly the residue
classes modulo nine. Consequently

    S=0 implies R_s=u_(s mod9) for nonnegative integers u_t. (5)

The first compression gives
m_r=-(u_t+u_(t+N)+u_(t+2N))/3; the right side depends only on r mod3.
Hence B_s itself is nine-periodic. Conversely any nine-periodic B vanishes
at zeta by geometric summation. Thus, on the first compression kernel,

    S=0  iff B is nine-periodic  iff p*B_s=G_(s mod9).       (6)

This also proves W=0 iff S=0 directly from (2). There is a second exact
proof with no positivity theorem: in the p-by-nine CRT tensor array H,
S=0 means H_(a,e)-H_(a,e+3) is independent of a (with the appropriate
three exponent representatives). Therefore any two rows differ by a
constant on each three-layer set. Each row's layer sum is zero, so that
constant is zero over Z. All rows agree, which is nine-periodicity.
This is the same integral tensor mechanism already used in the residue work.

If G=0 as well, (6) says B=0. The hoped-for new cycle-capacity obstruction
has therefore reduced EXACTLY to the old lifting equations. It supplies
no support-specific impossibility, no branch distinction, and no constructive
procedure. Checking a decomposition after evaluating phases is just another
way to test S=0. We stop this route here rather than report the resulting
separation of saved witnesses as a theorem explaining emptiness.

The unproved missing statement for 279 would still be: its indexed signed
events cannot realize B=0 under the gauges. A purported "cycle capacity"
lemma that merely asserts this has changed the notation, not solved it.
The color of an edge (which row and indexed endpoints produced it) is
absent from Lam--Leung's coefficient decomposition. A new colored-cycle
theorem could in principle help, but no such theorem or credible support
lemma follows from the decomposition we have proved.

## 4. Explicit counterexample to the tempting shortcut

The statement "a nonnegative vanishing R with a zero in every three-cycle
must be zero" is false. For every prime p>3 take the nine-periodic integer
array with period

    b=(0,2,-1,0,-1,-1,0,-1,2).                             (7)

It is symmetric, has B_0=B_N=B_(2N)=0, and every N-layer triple sums to
zero. Its primitive value S is zero, so it is in full 9O. But G=p*b is
nonzero. Normalization (4) gives R=3 on residues 1 and 8 modulo nine and
zero elsewhere: exactly three copies of each of two p-cycles, with no
three-cycle present. This is an INTEGER CORRELATION RELAXATION, not a
binary phase witness; no gauge or support realization is claimed. It
refutes the shortcut even with the first compression and symmetry retained,
and shows why exact second compression cannot be omitted. Requiring G=0
removes it only by returning to B=0 through (6), not by a new obstruction.

## 5. The construction alternative is blocked in its literal form

Suppose x(r,t)=A_r B_t and y(r,t)=C_r D_t are binary rows on C_m x C_n,
where m,n are odd and greater than one. At a shift (h,0) with h!=0,

    PAF_x(h,0)+PAF_y(h,0)=n*(PAF_A(h)+PAF_C(h)).             (8)

The left side would be -2 for a Legendre pair, impossible since n does
not divide two. Thus no binary Legendre pair is a pair of pure CRT-product
rows at these lengths. This is a one-line standard product-PAF obstruction,
not a new construction or a theorem excluding either actual branch: neither
branch is assumed to force this ansatz. Allowing switching blocks or sums
of products changes the ansatz and requires new binary and PAF proofs.
The positive solution is a mandatory warning against treating a failed
product ansatz as a nonexistence theorem for the ambient length.

## 6. Predeclared validation boundary

No new phase assignment will be generated. Pilot: recheck the frozen
positive endpoint and formulas (1)--(4). Final audit: the seven saved
compression/residue witnesses plus the one previously saved transported
positive, reusing the pilot; then the single explicit array (7). At most
eight saved phase records and one relaxation. Check exact norm reduction,
the trace via independent multiplication in Z[zeta], E's two foldings,
and nonnegative normalization. Read the 54 saved mean-zero members only
to retain their actual domain labels; no regeneration or search. One
worker, 120-second cap, estimates 200 MB memory and 2 MB storage.

## 7. Completed checks and domain challenges

The pilot checked one saved endpoint in 0.02206 seconds, projecting 0.99278
seconds for the full bounded audit with a fivefold margin. The audit took
0.01889 seconds, reusing that endpoint. No phase assignment was generated.
Each saved endpoint was independently decoded and checked against its
frozen masks and integral S; the PAF/event array, both compressions, tensor
coefficients and standard-basis norm agree. The trace in (2) was checked
by independent multiplication S*bar(S) in Z[zeta], then taking the trace
of its integral coefficients, rather than merely recomputing W.

| Branch, first mask | G0,G1,G2 | Full 9O | J | W |
|---|---|---|---|---:|
| 277, 22487656929184 | 0,0,0 | yes | (0,0,0,0) | 0 |
| 277, 18570512807384 | 0,6,-3 | yes | (0,0,1,1) | 432 |
| 279, 31210651353580 | 0,6,-3 | yes | (0,0,1,1) | 432 |
| 279, 416258831260 | 6,0,0 | yes | (1,0,1,1) | 486 |
| 279, 428621558224 | 0,3,3 | yes | (2,0,0,0) | 972 |
| 279, 442312790436 | 0,0,0 | yes | (1,0,2,2) | 1080 |
| 279, 22964264347100 | 0,0,0 | no | undefined | 540 |
| 279, 22487656929184, transported | 0,0,0 | no | undefined | 360 |

The transported record has second mask 9405125214970; all other second
masks are pinned in the audit and inherited evidence. The strong false
positive has trace 9720=9*1080: the identity is satisfied, but no argument
has shown that W must stay positive for every admissible 279 assignment.
The positive control has W=0. These observations are checks of the formula,
not a new separation theorem.

The transported positive has S_0=-1 and trace 3240 divisible by 81. Thus
even the necessary trace divisibility from S in 9O does not recover that
full domain, despite both exact compressions. The saved Q-divisible outsider
also has trace divisible by 81 while outside 9O. The J0=0 source is in 9O
but fails exact compression; its W is 432, so a zero residue coordinate
does not force vanishing primitive energy. No quotient J is formed at an
out-of-domain endpoint.

The explicit array (7) passes S=0 and first compression but fails second
compression. It remains an integer relaxation, not a phase witness.
The 54 previously saved mean-zero design members were only read: none
passes exact G=0 or full 9O. Their zero mean does not give W=0 pointwise;
the quadratic expression cannot be evaluated at the mean as a replacement
for evaluating genuine assignments. No new fractional or modular object is
labelled an exact lift.

Four focused tests passed in 0.12 seconds. Tests cover saved arithmetic,
the nonnegative-cycle shortcut counterexample, trace-domain failure, and
the required first-compression guard. Additional checks at p=7 and p=11
use only the explicit integer arrays (2,-1,-1) on one layer triple and
the periodic array (7), not binary or phase searches. They validate scaling;
the proofs, not these finite tests, establish generality.

## 8. Primary literature, checked early and against the surviving result

* Lam and Leung, [On vanishing sums of roots of unity](https://arxiv.org/pdf/math/9511209),
  arXiv v1: Theorem 2.2 and tensor proof, PDF pp.4--5; Theorem 3.1 and proof,
  PDF pp.6--7; Theorem 3.3, its proof, and Corollary 3.4, PDF pp.7--8.
  These were read before the pilot and revisited for (5)--(6). The p-cycle
  decomposition is established, including the reduction from prime powers
  to square-free order with rotated cosets. Their text traces the two-prime
  result to de Bruijn. No original de Bruijn text was read here.
* Ramanujan, [On certain trigonometrical sums and their applications in the
  theory of numbers](https://ramanujan.sirinudi.org/Volumes/published/ram21.pdf),
  1918 paper, accessible re-typeset primary text: Section 1 and Section 2,
  equations (2.3), (2.5)--(2.7), PDF pp.1--3. These give the primitive-root
  sum and divisor/Mobius formula behind (3). This was checked against the
  exact surviving trace identity, not used as evidence that the specialization
  is original. Fourier energy projection and its positivity are standard.
* Turner, Kotsireas, Bulutoglu and Geyer, [Legendre pair of length 77 using
  complementary binary matrices with fixed marginals](https://arxiv.org/pdf/2101.10918),
  Section 3, printed pp.10--12: primitive-frequency remainder after exact
  compressions, Theorem 3.4 and Corollary 3.5. This was checked early and
  again against (6). It already establishes that the remaining primitive
  test completes lifting once the other frequency conditions are known.
  This round does not claim a new necessary-and-sufficient lifting criterion.

The search also found a publisher record for
[On the search of binary Legendre pairs of length pq2](https://www.sciencedirect.com/science/article/pii/S0747717126000544).
Direct opening returned HTTP 403. No full algorithm was read or inferred
from search-index text. An author-hosted quaternary-construction PDF URL
returned 404; it was not relied on for a binary construction or a claim
about its proof. The elementary product failure (8) is proved here directly.
Earlier full fast-spectral/pq-squared algorithm, historical-list, and
external-replication limitations remain. No author contact occurred.

Correctness, originality, significance, and readiness are separate:

* Correctness: (2), (6), and (8) have complete proofs and bounded arithmetic
  checks. The proposed strict inequality A and indexed cycle exclusion B
  remain unproved; no solver result fills that gap.
* Originality: the completed formulas specialize established cyclotomic,
  Fourier, and product-PAF facts. No useful original theorem was established.
* Significance: the identities expose why the selected global reformulation
  is circular, but resolve no entire conditional fiber and provide no new
  construction. They are not the requested substantive breakthrough.
* Publication: retain the narrower reproducibility/software assessment.
  There is no basis for research-submission consolidation or readiness.
  This conclusion is independent of priority for constructing order 668.

## 9. Concrete decision and reproducibility

**Stop this sequence of branch-279 local/filter reformulations.** No promising
global mechanism survived this round. Do not interpret that as a theorem
that no obstruction exists; it is a research allocation decision based on
proved information loss, available counterexamples, and the circularity
of the selected decomposition.

The substantive pivot is construction-first work on a deliberately structured
family of intermediates, rather than fixing an arbitrary census branch
and hoping local arithmetic will explain it. The next proposal should be
an explicit NONSEPARABLE binary composition or switching ansatz, with a
symbolic proof of the off-axis PAF equations and its resulting indexed
compressions before any search. Equation (8) gives a concrete rejection
test: pure products cannot work. Established difference-set/complementary
sequence constructions must be checked before pursuing an ansatz, and an
alphabet or cyclic-group change cannot be hidden. No such new construction
is asserted here; the current census should serve as controls, not be rerun.
This is a change of mathematical problem structure, not an instruction to
expand to four-position trades or launch an open-ended search.

Commands:

```powershell
.venv/Scripts/python.exe -m scripts.audit_primitive_projection pilot
.venv/Scripts/python.exe -m scripts.audit_primitive_projection audit
.venv/Scripts/python.exe -m pytest tests/test_primitive_projection.py -q -p no:cacheprovider --basetemp=tmp/pytest_primitive_projection
.venv/Scripts/python.exe -m scripts.package_primitive_projection
```

One worker, 120-second internal cap, conservative estimates of 200 MB memory
and 2 MB new storage (not measured peaks); no cap reached. Eight saved
phase records, one new explicit integer relaxation, zero new phase
assignments, zero census or move-graph runs. The new manifest pins notes,
code, tests and evidence with SHA-256. The integrity record verifies all
6,779 inherited result files and all five paper files, previous manifests,
the prior raw-byte aggregate, and the two preserved CRLF exceptions.
The manuscript SHA-256 is unchanged:
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.
No manuscript editing/compilation, external replication claim, p=37 search,
or communication to another person occurred.
