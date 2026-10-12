# A simultaneous-compression obstruction and its information loss

Date: 2026-10-12. Starting commit: `be92dfea374da4d4b621452ac9e30776ec067a36`.
All 6,715 tracked result files at that commit are preserved. This investigation
does not repeat the binary lifting census. Its negative result leaves the
reproducibility/software assessment unchanged.

## Selected target and outcome

The target was an exact obstruction based on a second compression after the
free prime-kernel action is removed. For length 9p, combine the prescribed
length-3p intermediate with a length-nine compression, using exact binary
matrix margins to require simultaneous realizability. This is more informative
than checking compatible sums alone, yet much smaller than the binary phase
domain. First pilots used active-count-matched p=5 ranks 1 (positive) and 3
(empty). The stronger diagnostic pair selected below is ranks 277 and 279:
they have identical first rows and identical residue-wise column multisets.

The necessary obstruction and its invariance have complete elementary proofs
below. Its proposed usefulness for these empty fibers is refuted: it rejects
none of the 460 frozen empty p=5 branches or four completed empty p=7 branches.
The exact margin profile cannot distinguish the selected empty branch from a
positive branch, even when all alternate compressed PAF equations are imposed.
**No new symbolic proof of emptiness of branch 279 is claimed.** Its emptiness
remains the established frozen enumeration result. What is proved here is the
soundness and precise information-loss boundary of this chosen relaxation.

## Exact simultaneous binary feasibility

Let p be odd, gcd(p,3)=1, L=9p, N=3p. Write K_m x for compression to length m:
`(K_m x)[i] = sum(x[i+k*m], k=0,...,L/m-1)`. Fix C in {-3,-1,1,3}^N
and U in {-p,-p+2,...,p}^9. For r=0,1,2 set

* column degrees `S_a = (3-C[r+3a])/2`, a=0,...,p-1;
* row degrees `R_b = (p-U[r+3b])/2`, b=0,1,2.

**Proposition 1.** A binary sign vector x with K_N x=C and K_9 x=U exists
if and only if, in every residue r, these nonnegative integer degrees satisfy
R_b<=p, S_a<=3, equal totals, and

`sum(R_sorted[:k]) <= sum(min(k,S_a), a=0,...,p-1)`, k=1,2,3,

where R_sorted is nonincreasing. These are the classical binary margin
(Gale–Ryser) inequalities, applied separately to three blocks.

**Proof.** The two congruences j=r+3a (mod 3p), j=r+3b (mod 9) specify
exactly one j (mod 9p): after removing r and dividing by 3 the remaining
moduli p and 3 are coprime. The indicators of x_j=-1 therefore form three
independent 3-by-p zero-one matrices, with the displayed column and row sums.
Necessity of each inequality follows because k rows contain at most min(k,S_a)
ones in column a.

For sufficiency, for each block build a directed network from a source to
row b with capacity R_b, from every row to every column with capacity 1,
and from column a to the sink with capacity S_a. Put T=sum(R_b)=sum(S_a).
A cut with rows A and columns B on the source side has capacity

`T - sum(R_b,b in A) + |A|*(p-|B|) + sum(S_a,a in B)`.

Minimizing over B gives `T-sum(R_b,b in A)+sum(min(|A|,S_a),a)`.
The largest row sum for |A|=k is the sum of the k largest R_b. Thus every
cut has capacity at least T exactly when the displayed inequalities hold.
For completeness, start at zero flow and augment on a residual source-sink
path by its smallest residual capacity. Capacities and flows remain integers;
each augmentation increases the flow by at least one and the total is bounded
by T. If augmentation stops below T, the residual-reachable vertices define
a cut whose capacity equals the flow, contradicting the cut bound. A flow
of value T therefore exists. Its unit-capacity row-column entries give the
required zero-one matrix. The CRT then reconstructs x uniquely from the three
matrices. This proves both directions without a floating-point assumption. QED.

This is a standard integral-flow argument, not a new margin theorem.

## The obstruction and the quotient

Define M(C) as the set of U passing Proposition 1. For fixed normalized
intermediates C,D define E(C,D) to consist of (U,V) in M(C) x M(D) with

`sum(U_i^2+V_i^2)=16p+2`,

`PAF_U(s)+PAF_V(s)=-2p` for s=1,...,8.

**Proposition 2.** E(C,D) empty implies the conditional Legendre fiber is
empty. This statement is invariant under the independent N-translations and
common congruence-kernel multipliers `u=1+tN`, t in Z/3Z.

**Proof.** Every genuine binary lift (x,y) gives compatible U=K_9 x,V=K_9 y.
For every s, expansion of the sums gives the exact identity

`PAF_(K_9 x)(s) = sum(PAF_x(s+9h), h=0,...,p-1)`.

For s=1,...,8 all p original shifts are nonzero, giving -2p after adding
the two rows. For s=0 the zero-shift contribution is 2L and the other p-1
contributions are -2, giving 2L-2(p-1)=16p+2. Hence every lift maps into E.
Rows retain sum one. Also `K_m(x_(u*j+v))[i]=(K_m x)[u*i+v mod m]`
for a unit u and either divisor m=N,9. Taking v=aN or bN keeps the fixed
intermediate, while on the length-nine rows these are independent cyclic
shifts and a common unit decimation. These preserve the alternate equations;
actual binary preimages establish preservation of margin feasibility.
Thus the necessary condition remains valid on the kernel quotient. QED.

Quotienting does not turn a nonempty relaxation into an empty one. The prior
free-action theorem concerns actual Legendre fibers; it does not justify
dividing counts of compressed pairs by 27. All projection counts here are
ordered length-nine pairs, counted once per pair, not binary lifts or orbits.

## A complete information-loss proof and counterexample

Define the profile P(C,D) to be the six labeled multisets
`{C[r+3a]:a=0,...,p-1}` and `{D[r+3a]:a=0,...,p-1}`, r=0,1,2.

**Proposition 3.** Equal profiles imply exactly equal E sets, not merely
equal cardinalities. No decision rule using only this profile (or E itself)
can distinguish an empty and a positive branch with equal profiles.

**Proof.** A permutation of columns of each CRT block changes their labels
but neither the permitted row margins nor their ordered length-nine row
labels. Alternatively, each right-hand side in Proposition 1 depends only
on the column multiset. Consequently M(C)=M(C') and M(D)=M(D') for equal
profiles. The extra energy and PAF conditions depend only on U,V, so E is
identical. A rule receiving identical data has identical output. QED.

The frozen rank-277 positive and rank-279 empty branches have active counts
(12,11), the same first row, and the same profile. Both have 3,267 and 2,592
candidate alternate rows after the safe individual energy bound, with exactly
2,943 ordered alternate matching pairs. The positive branch has three
anchor-fixed solutions (27 ordered lifts, one residual kernel orbit); the
empty one has zero. Their exact intermediate arrays and masks are in
`results/residual_obstruction/counterexample.json`.

In bit convention `x_i=1-2*((mask>>i)&1)`, a genuine rank-277 pair is
`(5988272173974,31425271139033)`. Permuting the second row's CRT columns
within residues gives the rank-279 binary preimage
`(5988272173974,31468172020371)`. Both have identical alternate compressions

`U=(-1,1,-1,1,-3,1,-1,1,3)`,
`V=(-3,3,1,-1,1,5,-1,-3,-1)`.

These satisfy every alternate equation and both binary margin conditions.
The transferred pair fails the full length-45 equation already at shift 3,
where the PAF sum is 2 instead of -2. After imposing the previously proved
third gauge, it becomes `(22487656929184,9405125214970)`; its shift-2 PAF
sum is -6. Its alternate compressions still coincide with those of the
third-gauged positive witness. Direct checks cover all three kernel elements.
The explicit failed pair alone refutes sufficiency for that pair; the frozen
zero census is additionally required to refute existential branch liftability.

The 1,164 intermediates have 668 distinct labeled profiles, of which 18 mix
positive and empty branches. This number of profiles has no connection to a
Hadamard order. A nonlinear classifier or additional inequalities computed
solely from these same profiles cannot repair the loss of cyclic column order.
This does not rule out order-sensitive constraints on the actual matrices,
or methods using retained phases, correlations, or different joint data.

## Exact bounded computation and reproduction

The implementation enumerates all feasible ordered U triples in each residue,
then matches integer keys (energy,PAF(1),...,PAF(4)). Symmetry PAF(s)=PAF(9-s)
justifies four shifts. Since every alternate coordinate is odd, a partner has
energy at least nine; dropping rows of energy greater than 16p-7 is sound.
There are no spectral tolerances, randomized filters, or caps on solutions.

The p=5 two-case pilot took 0.0926 s, projecting 161.70 s with a factor-three
margin. The full new projection run took 73.16 s, one worker, with a 1,200 s
controller guard; it rejected zero of 1,164 branches. The p=7 positive pilot
took 0.421 s, with a tenfold five-case estimate of 21.04 s against a 120 s
guard. Its result was reused alongside four portfolio checks; the complete
follow-up audit, including frozen-file hashing, took 14.04 s. Both pilots
budgeted 200 MB memory and 2 MB output; these are estimates, not measured
peak memory. No resource limit or timeout was reached. No binaries were
recompiled and no claim of independent external replication is made.

| p=7 class | Alternate matching pairs | Frozen anchor-fixed lifts |
|---|---:|---:|
| positive | 10,476 | 3 |
| control | 10,755 | 0 |
| a14_18 | 11,925 | 0 |
| a15_17 | 11,943 | 0 |
| a16_16 | 12,006 | 0 |

Reproduce in a disposable checkout (commands overwrite only this new study's
outputs); do not rerun the old result packagers over the preserved artifacts:

```powershell
.venv/Scripts/python.exe -m scripts.residual_compression_obstruction pilot
.venv/Scripts/python.exe -m scripts.residual_compression_obstruction census
.venv/Scripts/python.exe -m scripts.audit_residual_obstruction
.venv/Scripts/python.exe -m pytest tests/test_residual_obstruction.py -q --basetemp=tmp/pytest_residual_obstruction
```

Four tests passed in 0.25 s; the only pytest warning concerned its cache
directory. Python also printed a launcher-location diagnostic but exited
successfully. Independent validation enumerated all 512 binary 3-by-3
matrices and checked the criterion against all 4,096 possible degree pairs.
Tests compare exact alternate row sets for 277/279, verify the transferred
counterexample and all kernel elements, and check every saved alternate
witness at all eight shifts. These finite checks support the implementation;
the preceding proofs do not rely on test coverage.

## Sources, limits, and contribution assessment

Primary full text accessed lawfully on 2026-10-12:

* Turner et al., [author preprint](https://arxiv.org/pdf/2101.10918), Section 3,
  Definition 3.1 (PDF page 6), equations (8),(9) (PDF page 7), Theorem 3.2
  (PDF pages 8–9), and fixed-marginal binary matrix discussion (PDF page 9).
  The stated CRT factors there are pairwise coprime. The present decomposition
  by the common residue handles lengths 3p and 9, whose gcd is 3. This is
  a standard block application, not evidence of a new simultaneous-lifting
  principle. Their decimation multiplicity formula is not used to count E.
* David Gale, [publisher full text](https://msp.org/pjm/1957/7-2/pjm-v7-n2-p04-p.pdf),
  *A theorem on flows in networks*, Pacific J. Math. 7 (1957), 1073–1082:
  feasibility theorem p.1075, minimum-cut theorem and proof pp.1076–1077,
  integer-valued remark p.1078. These provide the classical flow background.

Focused searches for noncoprime Legendre compression did not establish
priority for the specialization or this finite counterexample. A secondary
author-hosted margin survey URL (`https://dept.math.lsa.umich.edu/~barvinok/zeroone.pdf`)
returned an internal access error; it was not read or used. Earlier full-text
and historical-list gaps remain as recorded in the publication audit; no
new access to those missing sources is claimed and nobody was contacted.

The completed contribution here is an attributed exact relaxation, a full
invariance and information-loss proof, and a reproducible negative case study.
It is not a useful new empty-fiber theorem for the frozen domain, a complete
residual characterization, or a new existence/classification result. The
strongest defensible candidate remains conditional branch incidence with
auditable software and replication artifacts. A narrow reproducibility/software
paper remains the appropriate development path, without submission readiness.
An order-sensitive obstruction would need genuinely additional data and its
own counterexample testing and proof. Full algorithm/priority comparison,
historical representative crosswalk, external replication, archival release,
authorship/expository review and visual PDF review remain submission gates.
