# Carry-aware phase moments: a necessary condition that does not explain emptiness

Research round: October 13, 2026. Base commit
`5fbcfcee28b7e429ed20732baff2b942b047c7e7`, branch
`agent/order-428-reproduction`. The initial tree was clean; no child agent
instructions were found. All 6,723 baseline result files and all paper files
are unchanged. New evidence is confined to `results/phase_moments/`.

**Research outcome:** no useful original empty-fiber theorem or substantive
breakthrough was obtained. We proved the candidate's necessity, its exact
scope, and its invariance under the kernel action; explicit counterexamples
prevent it from explaining rank 279. The algebra and the finite enumeration
below are distinct evidence levels. Enumeration confirms the old empty result
incidentally; it does not constitute the sought explanatory contradiction.
The narrower paper assessment is retained and the manuscript was not edited
or recompiled during this exploratory round.

## 1. Inspection and selection

Read the phase, propagation, spectral, conditional-fiber, and residual-margin
notes and their implementations, together with the frozen census and source
ledger. In particular, `src/phase_propagation.py` already has shared ternary
edge differences, exact triangle supports, weighted signed PAF intervals,
and a conditioned partner search. Anchor triangles already ensure global
realizability. `src/ternary_phase.py` already retains every layer carry and
cross term. Reintroducing these as a new method would be unjustified.

The selected precise candidate is **infeasibility of the carry-aware first
and second signed phase moments over F_3, after the third gauge**. The first
moments are linear; the second are quadratic. Gaussian elimination can expose
an arithmetic contradiction without traversing every phase assignment. Unlike
the preceding margin profile, their coefficients depend on cyclic column order.
This is a candidate tool, not a presumed original theorem.

Ranks 277 (positive) and 279 (empty) have the same first row, active counts
(12,11), and identical margin profiles. Their three gauges leave 20 phase
coordinates. The new first moments contribute seven independent equations,
leaving 13 free coordinates in each branch. Thus the candidate does preserve
additional indexed information, but a rank reduction alone says nothing about
emptiness or originality.

## 2. Definitions and exact signed equations

Let N be odd and fix valid factor-three intermediate rows C,D of length N:
entries are in {±1,±3}, row sums are one, their combined squared energy is
6N-4, and their combined PAF is -6 at every nonzero shift. A binary lift has
length L=3N. For either row set b_i=sign(C_i), epsilon_i=1 if |C_i|=1 and
zero otherwise, and d_i=-2 b_i epsilon_i. At each active position the minority
layer is a_i in F_3. Then

`x[i+kN] = b_i + d_i [k=a_i]`.

For 1<=r<N define j=(i+r) mod N and h=floor((i+r)/N). Each directed active
edge i->j has weight w=b_i b_j and adjusted difference

`g = a_j-a_i-h in F_3`.

Sum over the active edges in both rows and define the integer signed histograms

`E_(r,ell) = sum(w [g=ell])`, ell=0,1,2,

and the phase-independent integer

`K_r = sum(3*b_i*b_j + d_i*b_j + b_i*d_j)` over both rows and all i.

Direct expansion of the three layer products gives

`PAF_x(r+ell*N)+PAF_y(r+ell*N) = K_r+4*E_(r,ell)`.                 (1)

This is the existing exact phase formula in directed-edge notation. Every
binary row has PAF congruent to its odd length modulo four: the number of
mismatches under a cyclic shift is even. Consequently K_r is congruent to
-2 modulo four and `t_r=(-2-K_r)/4` is an integer. The compressed PAF identity
gives `3*K_r+4*W_r=-6`, where `W_r=sum(w)=sum_ell E_(r,ell)`.
It follows that

`W_r=3*t_r`.                                                    (2)

Exact Legendre lifting requires the three integer equations E_(r,ell)=t_r.

## 3. Proven moment criterion and what it actually says

**Proposition 1 (necessity and exact modular scope).** Every Legendre lift
satisfies, for 1<=r<N,

`sum(w*g)=0 in F_3`,                                            (3)

`sum(w*g^2)=2*t_r in F_3`.                                      (4)

Conversely, for any binary preimage of these fixed valid intermediates,
(3) and (4) for all r are equivalent to the full set of congruences

`PAF_x(s)+PAF_y(s) = -2 mod 12`, 1<=s<3N.                       (5)

**Proof.** The first moment is E_1+2E_2 modulo three and the second is
E_1+E_2 modulo three. When all E_ell=t_r these have the stated values.
Conversely (3) implies E_1=E_2; (4) then implies E_1=E_2=t_r modulo three.
Equation (2) gives E_0=t_r modulo three as well. Equation (1) is now exactly
the equivalence with (5) at shifts not divisible by N. At shift N or 2N,
the pair PAF equals `(sum(C_i^2+D_i^2)-6N)/2=-2` independently of phases.
This covers every nonzero shift. QED.

The first moment expands to the linear equation

`sum(w*(a_j-a_i)) = sum(w*h) mod 3`.                            (6)

The right side must not be discarded. The second moment is a polynomial of
degree at most two in the vertex phases. Using vertex phases enforces all
ordinary difference-cycle constraints exactly; it is not a relaxation of
cycle realizability. The relaxation is reducing the signed integer balances
modulo three. Defects `E_(r,ell)-t_r=3*k_(r,ell)` are allowed, with
`k_(r,0)+k_(r,1)+k_(r,2)=0` by (2). Full lifting demands every k vanish.

**Proposition 2 (carries, cycles, and the free action).** Ordinary phase
differences sum to zero around every directed cycle. The adjusted differences
g sum to minus the total boundary carry modulo three. If 3 divides N,
(3)--(4) are invariant under independent layer translations and common
kernel decimations; hence their infeasibility is a sound obstruction on the
residual quotient as well.

**Proof.** Telescope the vertex phases around a cycle. For example an increasing
three-vertex cycle returning across the boundary has carry sum one, so its
adjusted differences sum to -1, not zero. Layer translations add a common
constant to each row's phases and leave differences unchanged. Under the
common multiplier 1+tN, phases change by `a_i -> a_i-t*i`. Because 3|N,
the adjusted difference on every shift-r edge changes by the same -tr.
Thus the three signed histogram entries are cyclically permuted. The condition
that they all equal t_r modulo three is invariant. Alternatively the first
moment changes by -tr*W_r=0, and the second changes by
`-2tr*M_1+(tr)^2*W_r=0` on (3). QED.

The third gauge fixes the first active phase in each row and the first
row's first active phase at a different index modulo three to zero.
The prior free-action argument justifies this for the frozen domain.
No additional symmetry is divided out in the new counts.

These propositions are elementary consequences of the existing exact signed
equations and finite-field arithmetic. They do not establish publication
priority or provide a new general classification theorem.

## 4. Counterexamples and complete diagnostic exploration

The initial bounded pilot found a modular witness for rank 279 after 988
assignments (and one for 277 after 667), so no contradiction can be derived
from (3)--(4) and cycle consistency alone. The first empty-branch witness has
negative-support masks `(5449388123528,9478070979302)`. It is already in the
third gauge. Its PAF sum at shift two is -14 rather than -2, although every
shift agrees modulo twelve. Masks encode `x_i=1-2*((mask>>i)&1)`.

To learn what was missing, a separately gated run enumerated the new modular
residual space, reusing its 10,000-point pilots. It did not rerun the old
binary row join or any frozen census command.

| Fixed branch | Independent first moments | Rank including gauges | Free coordinates | Modular assignments | Exact pairs in this gauge |
|---|---:|---:|---:|---:|---:|
| 277 | 7 | 10 | 13 | 734 | 1 |
| 279 | 7 | 10 | 13 | 740 | 0 |

All 3^13=1,594,323 linear-system assignments were visited for each branch.
Full integer PAF was evaluated only on the modular survivors. The exact
rank-277 pair is the frozen kernel orbit representative; the rank-279 result
agrees with its already known emptiness. This agreement is **a finite search
diagnostic**, not an explanatory theorem and not external replication.

Every subset of at most four nonredundant exact shifts has a witness among
the 740 modular assignments of rank 279. A greedy intersection of shifts
8,2,16,3,4,21,1,5,7,12,6 becomes empty. Thus the smallest such diagnostic
intersection has size between five and eleven; eleven is not claimed minimal.
This rules out a one-to-four-shift explanation *within this modular diagnostic*
but proves no general lower bound for other proof systems or domains.

## 5. Combining with the previous relaxation also fails

A justified strengthening is to demand the exact length-nine complementary
compression of the same binary preimages, in addition to (3)--(4). A bounded
challenge stopped at the eleventh modular witness; full intersection counting
was unnecessary because the stronger proposed obstruction already fails.

The rank-279 binary pair

`(22964264347100,2872821395978)`

has third-gauged phase arrays

`a=(0,0,0,1,0,1,0,2,0,0,0,2)`,
`b=(0,1,2,0,0,0,1,2,0,0,1)`.

It has exactly the frozen rank-279 length-15 compression. Its length-nine
compressions are

`U=(3,1,-1,-1,-3,3,-3,1,1)`,
`V=(-1,1,1,-5,-1,3,1,1,1)`.

Their combined energy is 82 and every nonzero combined PAF equals -10.
Thus the earlier binary-margin conditions hold with actual simultaneous
preimages, not just a feasibility test. All moment congruences and all phase
cycles with correct carries hold. Nevertheless, in nonredundant shifts its
full PAF sum equals 10 at 5,7,17, equals -14 at 8,13,20, and equals -2 at
the other sixteen shifts. Its defect is nonzero with three positive and three
negative entries, each of magnitude twelve. This is an explicit counterexample
to sufficiency of the combined tests, after removing the free action.

No valid logical consequence of those tests alone can exclude this point.
An empty-fiber explanation must retain additional integer correlation
information. This does not say that every empty branch passes the combined
test, or that all other order-sensitive obstructions are ineffective.

## 6. General structural interpretation of the surviving defect

Here let p>3 be prime, L=9p, N=3p, and assume both the length-N and
length-nine compressions have the required complementary PAFs. Define
the integer correlation-defect polynomial

`Delta(z)=sum_(s=0)^(L-1) e_s z^s`,

where e_0=0 and `e_s=PAF_x(s)+PAF_y(s)+2` for s!=0. This subtracts the
target group-ring norm `2(L+1)-2*(1+z+...+z^(L-1))`.

**Proposition 3 (standard cyclotomic reduction, specialized).**

`Delta(z) = H(z)*R(z)`,
`H(z)=(z^(3p)-1)*(1+z^3+z^6)=(z^(9p)-1)/Phi_(9p)(z)`,

for an integer polynomial R of degree less than phi(9p)=6(p-1). If the
moment congruences also hold, R=12Q for an integer polynomial Q. If Q is
nonzero, every primitive 9p-th-root frequency has a nonzero pair-PSD defect;
all nonprimitive frequencies have the correct values.

**Proof.** Compression of the PAF defect is zero, so Delta is divisible by
both z^(3p)-1 and z^9-1. Their monic gcd is z^3-1. Their monic lcm is H;
integer divisibility follows by the monic factors (or Gauss's lemma).
For prime p>3, these factors account for every cyclotomic factor of
z^(9p)-1 except Phi_(9p), proving the expression for H and the degree bound.
If all e_s are divisible by twelve, apply the same argument to Delta/12.
At a primitive root zeta, H(zeta)!=0 and a nonzero rational polynomial Q
of degree below phi(9p) cannot vanish, by the minimal polynomial of zeta.
The norm/PAF Fourier identity identifies Delta(zeta) as the PSD defect.
At other roots H vanishes; at frequency zero the correct PSD sum is two,
while the other target sums are 2L+2. QED.

For the explicit counterexample, integer long division gives

`Q(z)=-z^5-z^7+2z^8+z^10-z^11+z^13-z^14-2z^16+z^17+z^19`.

The coefficients and zero remainder are recorded independently. Thus the
stronger false positive hides its entire error at the primitive length-45
frequencies. This explains the information left unchecked, not why the true
fiber is empty. The reduction to one Galois orbit is established methodology:
Turner et al. Theorem 3.4 and Corollary 3.5 are direct precedents. No original
cyclotomic or spectral principle is claimed.

## 7. Validation, further challenges, and boundaries of generalization

All 2,979 frozen positive pairs (2,976 at p=5 and three at p=7) pass the
moment equations after the third gauge. All 1,169 frozen branches have
consistent first-moment systems: rank seven before gauges in all 1,164 p=5
branches, and rank ten in each of the five p=7 branches. We have not proved
that this rank or consistency pattern is universal; it is an observation on
this frozen domain, not a conjecture assumed by the implementation.

One empty branch from each of the 18 previously established mixed-profile
groups was challenged with at most 10,000 linear-system assignments. All 18
produced modular counterexamples, after 20 to 3,652 tests. This extends the
failure of the moment-only obstruction beyond rank 279. It does not count
their modular solutions or evaluate the combined test on all those branches.
For p=7 the all-positive audit and first-moment rank check are complete;
the quadratic residual spaces of the four empty branches were not exhausted.

Omitting carries from (6) rejects every one of the 2,979 true saved positive
pairs. Requiring adjusted differences themselves to sum to zero around a
winding cycle is also false: their sum is minus the carry count. Both tempting
strengthenings would therefore be unsound, not useful obstructions.

Five focused tests passed in 1.49 s. They check the equivalence of moments
and all-shift PAF congruences on deterministic random phase assignments;
validate all 1,474 saved modular witnesses with independent tuple PAFs;
check the stronger explicit counterexample and cycle law; recover the frozen
positive orbit and verify every four-shift intersection; and multiply out
the integer defect factorization. These tests do not replace the proofs or
provide independent external replication. Existing core implementations and
old experiment records were not modified.

## 8. Primary literature and access record

Accessed on October 13, 2026. Only the indicated portions are claimed read.
No authors were contacted.

* Djokovic and Kotsireas, [primary preprint](https://arxiv.org/html/1302.0571),
  Section 2, Lemma 1/equation (4), and Section 5, Theorem 3/equations
  (18)--(19): group-ring norms and the exact compression identity. These
  are established inputs to the derivation, not new contributions.
* Kotsireas and Koutschan,
  [primary preprint v3](https://arxiv.org/html/2101.03116), Section 2,
  Lemma 1/Corollary 1, Section 3 Proposition 1, and opening of Section 4:
  exact special-frequency conditions, compression, and subsequent full PSD
  filtering. These do not establish sufficiency for fixed lifting fibers.
  The PDF endpoint failed; the full HTML was accessible and used.
* Turner et al., [primary preprint](https://arxiv.org/pdf/2101.10918),
  Theorem 3.4 and Corollary 3.5, PDF pages 11--12: rational PSD equalities
  propagate through Galois conjugates, and divisor-frequency testing is
  sufficient. This is the relevant precedent for the primitive reduction.
* Gobin, [institutional thesis](https://mspace.lib.umanitoba.ca/bitstreams/e3f73833-0322-4661-b9ef-f91d46391501/download),
  *Boolean Complementary Pairs* (2023), definition on printed pp.1--2,
  Lemma 5.1.2 pp.63--64, conclusion p.139, and reference [4] p.143.
  Modular reduction of complementary-pair identities is an explicit prior
  technique. The thesis discusses aperiodic pairs and cites Craigen's
  *Complementary pairs modulo 3*, unpublished manuscript (2019).
  That manuscript was not obtained; its contents or applicability to this
  periodic conditional problem have not been verified. The whole thesis
  was not read. A targeted title search returned the thesis, not that manuscript.
* The ISSAC 2025 [publisher DOI](https://doi.org/10.1145/3747199.3747549)
  exposed indexed primary text for Section 2 (F_2 trace/linear complexity),
  but direct opening failed. No additional full-text algorithm comparison
  is claimed. The earlier fast-spectral and pq^2 access gaps remain.

Queries covered Legendre-pair congruences, ternary phase differences,
characteristic-three lifting, and modular complementary pairs. A search
result pointing to this repository was not treated as independent evidence.
Absence of an exact match in these searches establishes no originality.
The carry-aware moment specialization's priority remains unresolved, and
the standard algebra plus its demonstrated insufficiency supports no new
research-paper claim.

## 9. Commands, resource gates, and reproducibility

Run from the repository root in a disposable checkout; these commands write
only the new study's files. They do not run any old packager.

```powershell
.venv/Scripts/python.exe -m scripts.phase_moment_obstruction pilot
.venv/Scripts/python.exe -m scripts.study_phase_moments pilot
.venv/Scripts/python.exe -m scripts.study_phase_moments complete
.venv/Scripts/python.exe -m scripts.audit_phase_moments pilot
.venv/Scripts/python.exe -m scripts.audit_phase_moments complete
.venv/Scripts/python.exe -m scripts.challenge_phase_moment_refinement
.venv/Scripts/python.exe -m scripts.factor_phase_moment_defect
.venv/Scripts/python.exe -m pytest tests/test_phase_moments.py -q -p no:cacheprovider --basetemp=tmp/pytest_phase_moments
.venv/Scripts/python.exe -m scripts.package_phase_moments
```

The initial capped pilot took 0.081 s. The 10,000-point-per-branch enumeration
pilots forecast 148.19 s with a factor-three margin; their records were reused.
The complete subsequent run took 79.04 s, with a 1,200 s guard. Per-branch
enumeration times including pilots were 40.82 and 38.43 s. The 25-case validation
pilot forecast 25.50 s with a tenfold margin; the full read-only audit took
15.83 s under a 300 s guard and reused its pilot. A 25-witness refinement
pilot took 0.0048 s; the saved challenge stops at the eleventh witness.

Each process uses one worker. Planned memory was at most 200 MB per process
and storage at most 10 MB for the largest stage; these are estimates, not
measured peak memory. Result storage before final metadata is about 1.92 MB.
All substantive runs completed under their guards. Bounded challenges stop
on witnesses and claim feasibility only, not completeness. No timed-out or
capped run is treated as empty. Python printed a launcher-location diagnostic
but all reported completed commands exited zero. The manifest records source
hashes and evidence sizes; the audit pins the raw baseline path/hash digest
and unchanged manuscript hash. No external replication is claimed.

## 10. Strongest next mathematical target and stopping decision

For a primitive 45th root zeta and omega=zeta^15, the baseline and monochromatic
column contributions vanish. Define

`F_C = sum_(i active) C_i*zeta^i*omega^(a_i)` and similarly F_D.

The exact joint norm requirement is

`F_C*conjugate(F_C)+F_D*conjugate(F_D)=23`.                       (7)

This follows from X(zeta)=-2F_C, Y(zeta)=-2F_D and the required PSD sum 92.
After the two exact compressions, it is the remaining primitive condition;
the single-orbit formulation itself is known and is not a breakthrough.

The strongest justified next target is a **short conditional arithmetic
obstruction to (7) for the indexed supports of rank 279**, while retaining
rank 277. Possible tools to assess, not assumed results, are a higher
3-adic norm obstruction or a bounded-degree identity/inequality in signed
cycle counts that forces the primitive defect Q to be nonzero. Such an
obstruction should depend on structural hypotheses on the indexed signs
and ideally apply to a family. Simply evaluating (7) on every phase tuple,
running the existing PSD filter, or encoding all exact PAF equations again
would remain exhaustive search or an existing formulation.

At present there is no such invariant, proof, or substantiated family-level
conjecture. The finite rank pattern and sparse-defect structure are leads,
not theorems outside their stated domains. We stop this focused round because
the selected candidate and its natural compression refinement have explicit
counterexamples, not because documentation or a solver status achieved the
primary goal. No manuscript update is justified. The research goal remains open.
