# Conditional fibers: a prime-kernel divisibility theorem

October 11, 2026. Starting commit: `0c23a7e2989ba863e33817a49b6b934c526598ea`,
branch `agent/order-428-reproduction`. HEAD matched and the working tree was
clean before this investigation. No child-project agent instruction file was
found. All existing result artifacts, including the local Clang/MSVC replication,
are frozen. New records live only in `results/fiber_structure/`.

## Outcome and selection of the question

**Proved:** if an odd prime q divides an odd integer N, every fixed length-N
compression fiber of normalized binary Legendre pairs of length qN has ordered
size divisible by q³. After independent translations by N, its size is divisible
by q. Every intersection with a class under common decimation, independent shifts
and reversals, and row exchange has the same divisibility. For q=3 this explains
the factor 27 in the completed census and the factor three in every nonzero
branch/class entry. A third explicit phase gauge selects one member of each
27-element orbit.

This is a general statement, not an extrapolation from 1,164 branches. However,
the central multiplier obstruction has a close, explicit primary antecedent,
including a stated general prime-square version. Another cited archive is
reported to cover affine symmetries. Our count and gauge conclusions are modest
consequences of that obstruction and standard group actions. **A substantive
original theorem sufficient to upgrade the submission assessment has not been
established.** The narrower reproducibility/software assessment remains.

The candidate ranking supporting selection of the multiplicity question is:

| Rank | Candidate | Significance if resolved | Proof prospects | Prior-art risk / decision |
|---|---|---|---|---|
| 1 | Explain the extra factor three within each fixed fiber and incidence entry | General structural constraint beyond the computed lengths | High: explicit congruence-kernel action and energy bound | High, now confirmed for the underlying obstruction; selected and proved with attribution |
| 2 | Characterize which admissible intermediate pairs have no lifts | Stronger: explains 460 p=5 and four p=7 empty fibers | Low in this investigation; phases interact across every active pair | Compression/PSD obstructions established; no new necessary-and-sufficient criterion obtained |
| 3 | Predict all residual branch/class multiplicities and incidence degrees | Moderate if a structural characterization replaces enumeration | Moderate for accounting, low for predicting stabilizers | Orbit–stabilizer itself is standard; universal one-orbit claim is false |
| 4 | Describe all fibers by complementary signature buckets | Exact but primarily a formulation | Immediate | Already compression and all-bucket matching; not a new theorem target |

The selected question is: *what forces multiplicity beyond the two known
translation gauges, and precisely what does that force about class incidence?*
It does not promise a new empty-branch test or global existence information.

## Domain, conventions, and elementary preliminaries

Let q be an odd prime, N an odd positive multiple of q, and L=qN. Coordinates
are in Z/L. Rows are binary, their sums are +1, and the pair is ordered. Set

\[
 C_i=\sum_{k=0}^{q-1}x_{i+kN},\qquad
 D_i=\sum_{k=0}^{q-1}y_{i+kN}\quad(0\le i<N).
\]

Fix the **indexed, ordered** pair (C,D). Let F(C,D) contain all binary pairs
with these compressions and PAF_x(s)+PAF_y(s)=-2 for every nonzero s. No row
exchange, reversal or decimation is divided out in F. Each compressed entry is
an odd integer between -q and q. A *monochromatic column* has all q signs equal,
equivalently its compressed entry has absolute value q. Write μ_x and μ_y for
their counts. The standard compression identity gives

\[
 E:=\sum_i(C_i^2+D_i^2)=2qN-2(q-1).
 \tag{1}
\]

**Lemma 1 (monochromatic budget, a compression consequence).**

\[
 \mu_x+\mu_y\le\frac{2(N-1)}{q+1}.
 \tag{2}
\]

Proof. Every column has squared sum at least one; a monochromatic column
contributes q² instead. Thus E≥2N+(q²-1)(μ_x+μ_y). Substitute (1) and divide
by q²-1. For q=3 equality holds because every other column has squared sum one.
This lemma is routine energy accounting, not a claimed discovery.

An integer row of sum one has no nonidentity cyclic translation stabilizer:
a translation with orbit size d>1 partitions its positions into cycles of size
d, so its sum would be divisible by d. This applies to both binary and compressed
rows and justifies all translation factors without assuming genericity.

## The obstruction and complete proof of the selected result

Define M_a x by (M_a x)_j=x_{(1+aN)j}, for a∈Z/q. Because q divides N,
N² is a multiple of qN, and

\[
 (1+aN)(1+bN)\equiv1+(a+b)N\pmod{qN}.
\]

These are q distinct units, forming the kernel K of reduction from units
modulo qN to units modulo N. On the column indexed by i, M_a acts on layer k
as k↦k+ai. It fixes the indexed compression. Let T_b x have coordinates
(T_b x)_j=x_{j+bN}. The two actions commute.

**Lemma 2 (no nontrivial affine kernel multiplier in a row).** No row in a
binary Legendre pair has

\[
 x_{(1+aN)j+bN}=x_j\quad\text{for every }j,
 \qquad a\ne0\pmod q.
 \tag{3}
\]

Proof. On column i this permutation is k↦k+ai+b. For every i except those
in the single residue class -b/a modulo q, it is a q-cycle, since q is prime.
Invariance forces at least N-N/q monochromatic columns in this one row.
But

\[
 \frac{N(q-1)}q>\frac{2(N-1)}{q+1},
\]

because after multiplication by q(q+1) the difference is
N(q²-2q-1)+2q>0 for q≥3. This contradicts (2), even with no monochromatic
columns in the other row. This proves the obstruction for either row separately.
For an arbitrary affine translation t, compression of the fixed-row relation
would make C invariant under translation t modulo N. Its sum is one, so
t≡0 modulo N, reducing to (3). Alternatively (3) is conjugate to untranslated
kernel invariance by a coordinate shift solving ac≡b modulo q.

The untranslated obstruction and general prime-square assertion are explicit
antecedents described below. The extension to affine shifts is also reported
there; this proof is included for a self-contained, directly auditable deduction.

**Theorem 3 (fixed-fiber divisibility).** On F(C,D), the group

\[
 G=\{(x,y)\mapsto(T_bM_ax,T_cM_ay):a,b,c\in\mathbb Z/q\}
       \cong(\mathbb Z/q)^3
 \tag{4}
\]

acts freely. Consequently |F(C,D)|=q³r for an integer r≥0. Independent layer
translations H={(a,b,c):a=0} have q²-element orbits. K acts freely on F/H,
which has qr elements. For any global equivalence class E under the published
operations (common units, independent cyclic shifts/reversals, row exchange),
|F∩E| is divisible by q³ and |(F∩E)/H| is divisible by q.

Proof. The column formulas establish compression preservation and commutation;
the q³ coordinate actions are distinct. Each T leaves its row PAF unchanged,
and common M_a sends the pair PAF at shift s to its PAF at (1+aN)s. Hence G
preserves F. If a≠0 fixed a pair, it would fix each row as in (3), impossible.
If a=0, sum-one translation freeness forces b=c=0. Thus the action is free.
Every orbit has q³ members by orbit–stabilizer. If an element of K fixed an
H-orbit it would yield a nonidentity stabilizer in G, so its quotient action
is free. Finally every G operation is among the stated equivalences, so F∩E
is a union of G-orbits. This proves all count claims, including zero fibers.

No primeness assumption on N/q, quadratic-character prescription, or unequal
row assumption is needed. This includes N divisible by q². The theorem requires
odd prime q and odd N, binary rows and the Legendre equations. Composite q is
not covered by the q-cycle argument. For q∤N the claimed order-q kernel is
unavailable. Counts modulo larger equivalence groups need not be multiples of
q³: stabilizers outside G may occur, and G is not asserted normal in that group.

## Exact ternary gauge and what matching does not preserve

For q=3 write a_i∈Z/3 for the minority layer at an active column |C_i|=1.
Every row of an admissible intermediate pair has active columns in at least
two residue classes modulo three: otherwise it would have at least 2N/3
monochromatic columns, violating (2). This conclusion already follows from
the compressed energy equation, even if the fiber is empty.

Choose the first active index i0 of the first row and the first active i1 with
i1≠i0 modulo three. Retain the old phase-zero anchors in both rows. Applying
M_t and restoring those two anchors changes first-row phases to

\[
 a'_i=a_i-t(i-i_0)\pmod3.
 \tag{5}
\]

Exactly one t makes a'_(i1)=0. Therefore fixing these **three** phases selects
exactly one pair per G-orbit. Restoring all 27 ordered pairs is bijective.
The existing enumerators still use only two anchors; their outputs and counts
are unchanged. This is a proved optional gauge, not a measured optimization.

The elementary matching identity |F/H|=Σ_v A_v B_(-2-v), with complete row
signature bucket multiplicities A_v,B_v, remains valid. It is not a new
counting theorem. Kernel decimation generally **permutes PAF coordinates**;
it does not fix a signature or justify dividing each bucket by three. In all
2,979 saved pairs tested, the first-row full PAF signature changes under the
generator. Collisions must still be resolved by full-key equality, and every
member of each matching bucket must be retained. Independent decimation of
both rows cannot simply replace the common action: relative alignments matter.

## Counterexamples, finite evidence, and limits

The read-only action audit checks all 1,164 p=5 branches, the four empty p=7
branches and the positive control, including all 2,979 saved phase-gauged pairs.
It verifies integer PAF/compression, orbit closure and size three, the one-row
freeness strengthening, the third gauge, and unchanged local equivalence labels
inside each orbit. It yields 992 p=5 kernel orbits and one positive p=7 orbit.
The four empty cases remain empty by their earlier exhaustive evidence; the
new symmetry theorem does not explain why those admissible branches are empty.

The stronger conjecture that every nonzero branch/class entry is a *single*
kernel orbit is false. The frozen data give 928 entries with one orbit and 32
with two. Rank 129, local class 60, is the first counterexample; `audit.json`
stores both triples of exact mask pairs. Similarly, the observed incidence
degrees eight and sixteen are finite observations; no general degree formula
with known stabilizers has been proved. A symmetry action predicts divisibility,
not those particular degrees or an upper bound of 81 ordered lifts.

Tiny independent full checks used 3 normalized rows at length 3 and 126 at
length 9. Length 3 compressed to N=1 has one fiber of size nine, disproving
the q³ conclusion if q|N is omitted. Length 9 compressed to N=3 has 18 nonempty
fibers of size 54, totaling 972 ordered pairs. This is finite corroboration,
not a proof at other lengths. Without the Legendre hypothesis, C=D=(1,3,-3)
at N=3 has nine binary preimage pairs and invariant rows: each row has three
choices only in column zero. Its energy is 38, inconsistent with the required
14, so it is not a counterexample to the theorem.

An additional single-row check assigns signs on every affine coordinate orbit
for (q,N)=(3,3),(5,5), with every a≠0,b. It tests 192 and 10,240 assignments;
the minimum normalized-row energies are 19 and 101. Even adding the partner
lower bounds 3 and 5 exceeds the necessary pair energies 14 and 42. These
small finite checks test the affine argument; no length-25 LP search was run.

The proof and new action audit use integer arithmetic only. They do not use
DFT values, numerical enclosures, floating-point tolerances, or the projected
PAF sufficiency theorem. The old census completeness continues to rely on its
audited enumeration coverage and exact matching; the spectral variants rely
additionally on their rational coefficient bounds. Their completed full-PAF
Clang/MSVC reproduction remains local, not external independent replication.

## Primary literature and priority boundary

The precise access ledger is `results/fiber_structure/literature.json`.

* Turner–Kotsireas–Bulutoglu–Geyer, [author preprint](https://arxiv.org/pdf/2101.10918),
  Section 2, Theorem 2.3 and Corollaries 2.4–2.5, preprint pp. 5–6, count
  duplicate decompressions using multiplier groups. Section 3, Theorem 3.2,
  pp. 8–9, treats simultaneous compressions. Their stated coprime-factor
  hypotheses do not directly cover q|N, but group-action fiber counting is an
  established method. The full PDF and these statements/proofs were read.
* [Issue #2, July 24, 2026](https://github.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/issues/2),
  by the account `byclaude`, attributes the work to Claude with Patrick White.
  Its claim/proof paragraphs give the one-row ternary obstruction, and its
  final mathematical paragraph explicitly states the general odd-prime-square
  obstruction. This is a primary public research communication, not a
  peer-reviewed article. It decisively prevents a first-obstruction claim here.
* The project’s [ID-2 report](https://github.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/blob/main/lp333/id2_congruence_kernel/report.md),
  “Theorem,” “Proof,” and “Provenance and independent corroboration,” incorporates
  that argument; [PR #5](https://github.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/pull/5)
  records its merge on August 10. The report also credits Benedek “Ben” Blackthorn
  with a broader prime-square theorem including affine symmetries and a Lean 4
  formalization, citing [Zenodo 21779001](https://doi.org/10.5281/zenodo.21779001).
  The report was read; the Zenodo DOI, landing page and API were inaccessible
  through the web tool. The archive and Lean proof were **not** read or checked.
* Ramos–Hulak–de Queiroz, [arXiv v1](https://arxiv.org/html/2607.20765v1),
  Sections 2.1–2.2 (Lemma 2.4, Definition 2.6) distinguish compression and
  untranslated common multipliers. The v1 classification predates the incorporated
  ID-2 obstruction. Its accessible relevant sections are background, not evidence
  that the later repository result was absent. No computation at its target
  length was performed in this investigation.

The October 10 access findings for fast-spectral/pq² and the complete historical
length-45 list remain unresolved and frozen. They were not inferred from
abstracts, and no contact was made. The order of this investigation matters:
the kernel/count argument was developed locally, then the focused literature
search located the direct antecedent. That is an independent derivation with
subsequent attribution, not independent publication priority. The conditional
q³ statement and explicit ternary gauge are useful specializations/corollaries;
their own priority is unresolved, and no originality claim is made.

## Reproduction, resource gate, and research assessment

Run separately from the repository root in a fresh output location:

```powershell
.venv/Scripts/python.exe -m scripts.audit_fiber_structure baseline
.venv/Scripts/python.exe -m scripts.audit_fiber_structure pilot
.venv/Scripts/python.exe -m scripts.audit_fiber_structure audit
.venv/Scripts/python.exe -m pytest tests/test_fiber_structure.py -q --basetemp=tmp/pytest_fiber_structure
```

The bounded 26-case pilot took 0.136 seconds; its tenfold extrapolation was
61.00 seconds. Before the full action audit the budget was one worker, 120
seconds, 200 MB estimated memory and 2 MB estimated output. The actual audit
completed in 7.23 seconds. These are validation timings, not speed comparisons.
No caps or timeouts occurred and no old enumerations were repeated. Runtime,
script hash, individual orbits, small experiments, and baseline digest are saved.
The manifest pins the research note, new script/tests, source ledger and output;
the paper manifest separately pins the updated manuscript. Hashes do not certify
the general proof. No proof assistant or external mathematical referee checked it.

The central artifact remains the complete conditional census and auditable
software. This investigation adds an attributed general divisibility theorem,
a correct optional gauge, and a concrete refutation of uniform single-orbit
incidence. It strengthens explanation, but the result is not a new existence,
classification, asymptotic complexity or empty-fiber theorem. Submission readiness
is unchanged. Outstanding gates include full algorithm/priority comparison,
historical crosswalk, external replication, archival release, authorship and
exposition, and visual PDF layout review. Final compilation status is recorded
separately for the final saved source; a prior successful compile does not
validate later edits.

The most promising next mathematical question is whether one can characterize
or obstruct the **residual** fibers after the free kernel action is removed,
using exact phase-difference cycles and signed correlation constraints. Such a
criterion must distinguish nonempty and empty intermediates satisfying the same
energy equations, and must outperform a restatement of the full phase search.
This remains a bounded research question, not a conjectured universal liftability
or a promised new algorithm. No p=37 search or proximity claim is made.
