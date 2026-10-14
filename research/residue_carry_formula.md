# An explicit signed-balance and degree-six formula for the next residue

Research round: October 14, 2026. Base commit
`d441e0d8bfe6052c6574ca3702f1b3d40129ff7e`, branch
`agent/order-428-reproduction`. The initial tree was clean; no child agent
instruction files were found. The two preceding mathematical notes, exact
phase equations, phase propagator, integral spectral implementation, and
frozen witness records were inspected. No completed census was rerun.

**Outcome.** The formula deliverable is proved, through two exact routes.
For a valid length-15 intermediate pair and S in 9Z[zeta], four small signed
histogram differences determine J. They admit explicit polynomials over F_3
of total degree at most six in the original ternary phases. The degree bound
generalizes to length 9p, p>3 prime, independently of p. This is mathematical
progress beyond evaluating saved solutions. The carry-polynomial mechanism
has direct primary precedents; originality of this lifting specialization is
not established. A proposed single-coordinate obstruction fails, and no
structural proof of branch-279 nonvanishing has been obtained. The manuscript
remains unchanged, and the narrower publication assessment is retained.

## 1. Domain, indices, and the exact integer balances

Let C,D be valid factor-three compressed Legendre intermediates of length 15:
entries in {+1,-1,+3,-3}, row sums one, combined energy 86, and combined PAF
-6 off zero. There are 23 active entries in total. Keep every active position
and its sign. Set b_i=sign(C_i), d_i=-2b_i on active positions and zero
otherwise. A phase a_i in {0,1,2} gives

`x[i+15*k] = b_i + d_i*[k=a_i]`.

Use the analogous notation for D. Phases are listed by increasing active
index, with the first two C phases and first D phase fixed to zero on branches
277 and 279. The free-action justification is inherited; the formula itself
does not require this gauge. The exact rows and active supports remain those
printed in `primitive_local_obstruction.md`, Section 1.

For 1<=r<15 and j=(i+r) mod 15 let h=floor((i+r)/15), an **integer** boundary
carry. Define, summing directed active edges in both rows,

`E_(r,l) = sum b_i*b_j*[a_j-a_i-h = l (mod 3)]`, 0<=l<3,

`K_r = sum_(both rows, all i) (3b_i*b_j+d_i*b_j+b_i*d_j)`,

`t_r = (-2-K_r)/4`.

The exact existing phase identity is

`PAF_x(r+15l)+PAF_y(r+15l)+2 = 4*(E_(r,l)-t_r)`.

Set B_0=B_15=B_30=0 and B_(r+15l)=E_(r,l)-t_r. Then B_s is an integer,

`B_s=B_(45-s)`, and `sum_(l=0)^2 B_(r+15l)=0` for every r modulo 15. (1)

In particular, `sum_(s=r mod 5) B_s=0` for every r modulo five. These are exact
integer equalities, not congruences. The previous phase moments are equivalent
to every B_s being divisible by three. On that additional domain write

`k_s=B_s/3=(PAF_x(s)+PAF_y(s)+2)/12` for s!=0; k_0=0.            (2)

Let zeta be primitive of order 45, omega=zeta^15, pi=1-zeta^5,
and O=Z[zeta]. With the user-specified active signed sums F_C,F_D put

`S=F_C*conjugate(F_C)+F_D*conjugate(F_D)-23`.

At a primitive frequency x(zeta)=-2F_C and y(zeta)=-2F_D. Consequently

`S = sum_(s=0)^44 B_s*zeta^s`.                                 (3)

This uses the exact PAF/norm identity and the vanishing of the target's
nonconstant geometric sum. It is not an assertion of polynomial equality
away from the primitive roots.

## 2. First route: the standard integral cyclotomic basis

Write uniquely S=sum_(j=0)^23 s_j*zeta^j, s_j integers. This is the existing
baseline route. Explicitly, if R_j(n) is the coefficient of z^j in
`z^(n mod 45) mod Phi_45(z)`, then

`s_j = sum_(rows) sum_(i != k active) C_i*C_k * R_j(i-k+15(a_i-a_k))`. (4)

The 23 diagonal terms cancel the target. All exponent differences in (4) are
computed as integers before reduction; negative differences are allowed.
The modulus is

`Phi_45(z)=z^24-z^21+z^15-z^12+z^9-z^3+1`.

**Exactly here divisibility by nine enters:** S belongs to 9O if and only if
every s_j is divisible by nine, since these powers are an integral basis.
Only after verifying this do we form q_j=s_j/9 in Z. Reduction modulo pi
sends zeta to a primitive fifth root alpha over F_3. Thus

`J_r = (sum_(j=r mod 5) s_j - sum_(j=4 mod 5) s_j)/9 mod 3`,
`J = J_0+J_1*alpha+J_2*alpha^2+J_3*alpha^3`, 0<=r<4.            (5)

This coefficient-reduction formula is a baseline, not the main explanatory
result. Reducing s_j modulo three before dividing would erase the needed
information. The implementation rejects division outside 9O.

## 3. Second route: three-shift slices of signed balances

Put gamma=zeta^36 and t=zeta^5. Then gamma has order five, t order nine,
and zeta=gamma*t^2 because 36+10=46=1 mod 45. The elements

`gamma^r*t^v`, 0<=r<4, 0<=v<6,

form an integral basis of O. Indeed they span a ring containing zeta, and
the two monic relations Phi_5(gamma)=0 and Phi_9(t)=t^6+t^3+1=0 reduce
it to 24 generators. Their independence follows from [Q(zeta):Q]=24.
Thus this basis and the standard basis in Section 2 are related integrally
in both directions. Modulo pi, t=1 and gamma=alpha.

Arrange the integer balances in a 5 by 9 array

`H_(r,e)=sum_(s mod 5=r, 2s mod 9=e) B_s`.

The index map is a bijection on 0,...,44, so each cell contains one B_s.
Let D_(r,e)=H_(r,e)-H_(4,e), r<4. Eliminating gamma^4, then eliminating
t^6,t^7,t^8 with Phi_9, gives the exact tensor-basis coefficients

`A_(r,v)=D_(r,v)-D_(r,6+(v mod 3))`, 0<=v<6.                    (6)

These 24 integers are all divisible by nine if and only if S is in 9O.
On that domain evaluation of the quotient at t=1 gives

`J_r = (sum_(e=0)^8 D_(r,e) - 3*sum_(e=6)^8 D_(r,e))/9 mod 3`. (7)

The first sum is **zero as an integer**, by (1). Define

`I_r={s: s mod 5=r and s mod 9 in {3,4,8}}`,
`U_r=sum_(s in I_r) B_s`, `Q_r=U_4-U_r`.

Here {3,4,8} is the inverse image of {6,7,8} under multiplication by two
modulo nine. Explicitly,

| r | I_r |
|---|---|
|0|30,35,40|
|1|21,26,31|
|2|12,17,22|
|3|3,8,13|
|4|4,39,44|

**Theorem 1 (signed-balance residue formula).** For any binary preimage of
a valid length-15 intermediate pair, if S is in 9O, then every Q_r is divisible
by three and

`J_r = Q_r/3 mod 3`, 0<=r<4.                                   (8)

**Proof.** Equations (6)--(7) were exact integral basis reduction before any
division. Summing (6) over v gives 3Q_r. Since each A_(r,v) is divisible by
nine, so is 3Q_r, proving the asserted integer divisibility. Dividing the
sum of the A coefficients by nine gives Q_r/3, as claimed. QED.

This proves agreement of the routes: both divide the *same algebraic integer*
S by nine in an integral basis, then apply the well-defined ring map
O -> O/(pi). Equality (3) connects the original signed phase norm to the
histogram route. No cancellation or division in F_3 was used to justify (8).

With the moment conditions, (8) becomes especially sparse. Define
`A=k_1+k_4+k_6`, using the nonredundant shifts 1,...,22. Then

```
J_0 = A-k_5-k_10
J_1 = A-k_14-k_19-k_21
J_2 = A-k_12-k_17-k_22
J_3 = A-k_3-k_8-k_13                         (all in F_3).       (9)
```

This uses k_(45-s)=k_s and k_15=k_30=0. Importantly, the moments alone do
not make (9) the residue J: S in 9O remains a necessary domain assumption.
Equation (9) otherwise defines an extension with no such interpretation.
The theorem does not require the alternate length-nine compression.

## 4. An actual polynomial over F_3: retaining the signed carries

The rational expression Q_r/3 is quadratic in Boolean phase-event variables,
but its coefficients cannot be reduced modulo three. We now eliminate that
denominator **without** pretending it is invertible.

For a fixed coordinate expand Q_r exactly using its six signed shift slices:

`Q_r = c_r + sum_e epsilon_e*Y_e`, epsilon_e in {+1,-1},          (10)

where the event e is a directed same-row active pair i->j from one chosen
shift s=r'+15l. Its Boolean value and sign are

`Y_e=[a_j-a_i-h-l=0 (mod 3)]`, `epsilon_e=sigma*b_i*b_j`.

Here sigma=+1 on I_4 and -1 on I_r, and
`c_r=-sum_(s in I_4) t_(s mod 15)+sum_(s in I_r) t_(s mod 15)`;
shifts 0,15,30 contribute zero and are omitted. Repeated events may be kept
as separate labeled terms. No independence of their Boolean values is assumed.

In the polynomial ring over F_3 in all the phase variables and T, truncated
modulo T^4, define for each event

`y_e=1-(phase_j-phase_i-h-l)^2` in F_3,

which evaluates to its integer indicator Y_e. Define the explicit polynomial

`P_r = [T^3] (sum_(j=0)^3 binom(c_r,j)*T^j)`
`             * product_(epsilon=+1) (1+y_e*T)`
`             * product_(epsilon=-1) (1-y_e*T+y_e*T^2-y_e*T^3)`. (11)

The binomial coefficients of the **fixed integer constant** c_r are evaluated
in Z before reducing modulo three, including when c_r is negative. Equation
(11) has no variable denominators in F_3.

**Theorem 2 (uniform degree bound).** P_r is a polynomial of total degree at
most six in the original ternary phase coordinates. For every phase assignment
it equals `floor(Q_r/3) mod 3`. On S in 9O it equals J_r.

**Proof.** For any integer n=3q+d, 0<=d<3 (also when n<0), in the formal power
series ring over F_3,

`(1+T)^n=(1+T^3)^q*(1+T)^d`.

Its coefficient of T^3 is q modulo three. Negative powers are legitimate
formal series since the constant coefficient is one; truncation at degree
three suffices. Thus binom(n,3)=floor(n/3) mod 3, and in particular
binom(3q,3)=q mod 3. For a Boolean Y,

`(1+T)^(+Y)=1+YT`,
`(1+T)^(-Y)=1+Y*(-T+T^2-T^3) mod T^4`.

Consequently (11), evaluated on phases, is exactly the coefficient of T^3 in
(1+T)^Q_r. Each nonconstant factor contains at least one T and one y_e. A
term contributing to T^3 therefore contains at most three y_e factors,
each quadratic in phases. This proves degree <=6, regardless of the number
of edges. Equation (8) proves the final assertion on its stated domain. QED.

An alternative formulation keeps integer carry variables q_r and equations
`3q_r=Q_r`, then sets J_r=q_r mod 3. Those are valid quadratic integer
constraints, but (11) is stronger as a representation result: it gives a
genuine bounded-degree polynomial over F_3 with no auxiliary variables.

This explains additional interactions: each Q_r counts signed phase events
at selected indexed separations, retaining their boundary carries. Extracting
its next ternary digit couples up to three such events, potentially on six
different vertices and on both rows. They need not form a graph cycle.
This is arithmetic coupling of norm summands, not a new cross-correlation
between the binary rows. Pure cycle identities remain automatically satisfied
by the globally assigned phases.

The degree bound is not merely an interpolation bound depending on the
number of variables. A bounded challenge found a nonzero sixth mixed finite
difference for P_2 of branch 279 on the full gauged phase cube. At the saved
base assignment, vary phase indices (2,7,8,10,21,22) independently over {0,1};
the alternating sum of the 64 values is 2 in F_3. Every polynomial of total
degree <6 has zero such difference, since each monomial misses one of the six
variables. The full arithmetic certificate is saved and independently tested.
Thus this specified extension has minimum total degree six on the full gauged
cube. This proves **nothing** about the minimum degree of a polynomial that
agrees with J only on the much smaller domain S in 9O.

## 5. Two independent coordinates and a length-9p generalization

Since S is real, S/9 is fixed by conjugation. On O/(pi), conjugation sends
alpha to alpha^-1=alpha^4=alpha^9. Comparing the four basis coefficients
therefore gives

`J_1=0`, `J_2=J_3`.

Equivalently J lies in the subfield F_9 of F_81 and has the form
`J=u+v*(alpha^2+alpha^3)` with u,v in F_3. If eta=alpha^2+alpha^3 then
eta^2+eta+2=0. This is a conjugation consequence, not a nonvanishing argument.
The equations concern the domain; the polynomial extensions need not obey
them outside it. Requiring J=0 is weaker than requiring S=0 as an algebraic
condition (for example S=27 has zero residue but is not zero). That example
is not claimed to be the norm defect of an allowed branch assignment.

**Theorem 3 (generalization with explicit hypotheses).** Let p>3 be prime,
L=9p, and C,D valid factor-three intermediates of length 3p. Define S with
target (9p+1)/2, and assume S in 9Z[zeta_L]. Let beta be the inverse of p
modulo nine and set

`I_r={0<=s<L: s=r mod p, (beta*s mod 9) in {6,7,8}}`, 0<=r<p.

With B_s=(PAF_x(s)+PAF_y(s)+2)/4 off zero and B_0=0, put
`Q_r=sum_(s in I_(p-1)) B_s-sum_(s in I_r) B_s`.
Then in `F_3[alpha]/Phi_p(alpha)`, the coefficient of alpha^r in the residue
of S/9 modulo 1-zeta_L^p is Q_r/3 mod 3, for 0<=r<p-1. Each coefficient
has a phase polynomial of degree at most six as in (11).

**Proof.** Set t=zeta_L^p and gamma=zeta_L^(9a), where 9a=1 mod p.
Then zeta_L=gamma*t^beta. The integral basis gamma^r*t^v, r<p-1, v<6,
has 6(p-1)=phi(9p) elements. Repeat (6)--(8) using
H_(r,e)=sum_(s=r mod p, beta*s=e mod 9) B_s and eliminate gamma^(p-1).
The length-3p compression makes each row sum of H exactly zero. Phi_9 is
unchanged, so the factor of three and the same signed carry formula result.
The phase-event indicators remain quadratic and the degree bound is unchanged.
QED.

For general p this residue algebra can be a product of fields; 1-zeta_L^p
need not generate a prime. No assertion that it is always F_(3^(p-1)) is made.
Projection to an irreducible factor gives the corresponding prime residue.
A test at p=7 uses B(z)=3z^j(z^21-1)^2, for which S=-9omega*zeta^j and
the nonzero residue is -alpha^j. These are synthetic signed balance tests,
not binary Legendre solutions or a new p=7 census.

## 6. Validation and failed simplifications

Three independently formulated computations agree: direct multiplication of
F_C,F_D reduced in the standard basis (frozen evidence), the signed histogram
formula in the tensor basis, and the carry polynomial (11). Every monomial
of degrees 0 through 44 also passed the exact integral change-of-basis test.
The new formula was checked on all 1,474 previously saved moment assignments,
not by generating new phase assignments or rerunning the census. Only six
of those lie in its modulo-nine domain:

| Branch; masks | Q | J coordinates |
|---|---|---|
|277; 22487656929184, 11681458143385|(0,0,0,0)|(0,0,0,0)|
|277; 18570512807384, 19927795344025|(0,0,-6,3)|(0,0,1,1)|
|279; 31210651353580, 20580563788346|(0,0,-6,3)|(0,0,1,1)|
|279; 416258831260, 11737627988606|(3,9,3,3)|(1,0,1,1)|
|279; 428621558224, 824046633594|(6,9,9,9)|(2,0,0,0)|
|279; 442312790436, 2830005805622|(3,9,6,-3)|(1,0,2,2)|

For the user-specified last witness, k_3=2, k_6=k_9=1,
k_12=k_18=-1, k_21=-2, with all other nonredundant k zero. Equation (9)
immediately gives J=1+2alpha^2+2alpha^3. Both its compressions remain exact.
The frozen positive gives zero throughout.

All 2,976 frozen p=5 positives were covered after the third gauge, checking
992 distinct pairs with the new formula; each has J=0. Sixty deterministic
random phase assignments outside the moment domain verified the exact norm
and histogram identities; all sixty were correctly rejected from the S in
9O domain. They test the arithmetic, not emptiness. No p=7 phase search ran.

Several simplifications are refuted or ruled out:

* All six displayed Q vectors are zero modulo three, yet their J values
  differ. Keeping only those reduced balances loses the carry.
* Replacing zeta by a fifth root in the integer defect polynomial *before*
  division gives zero by compression for every assignment. It would wrongly
  return zero on the last witness. There is no characteristic-zero ring map
  Z[zeta_45] -> Z[alpha_5] taking zeta to alpha; the missing factor three
  appears precisely in Phi_9(1)=3.
* Individual B_s need not be divisible by nine. For the last witness B_3=6;
  it is the integral-basis coefficients of S, not each raw correlation
  coefficient, whose divisibility by nine defines the domain.
* The earlier witness (22964264347100,2872821395978), of valuation ten,
  has polynomial-extension value (2,0,2,2). It is outside 9O; that value is
  not J. An extension that happens to look real is still no domain proof.
* Degree-two reasoning from the original norm does not automatically survive
  digit extraction. The specified extension has degree exactly six on the
  full gauged cube. No minimal-degree claim on the conditional domain follows.

## 7. One precise structural claim, its counterexample, and the remaining target

After deriving the formula, we selected the following stronger, inexpensive
claim: **the indexed signs of branch 279, together with the phase moments and
S in 9O, force the constant coordinate J_0 to be nonzero.** This would imply
J!=0 without needing the other coordinate or the alternate compression.
In the moment notation it asserts

`k_1+k_4+k_6-k_5-k_10 != 0 mod 3`.                             (12)

We sought a counterexample before attempting a proof. The saved allowed
third-gauged assignment (31210651353580,20580563788346) has Q_0=0 and
J=alpha^2+alpha^3. It refutes (12) while satisfying both the moments and
S in 9O. Its alternate length-nine PAF sums are
(14,-22,-10,-22,-22,-10,-22,14), so it does not refute the strengthening
that additionally uses the exact length-nine compression.

An explicit general sufficient support/sign hypothesis can be stated: if
the signed events forced by a support pattern and phase constraints bound
some Q_r in an integer interval containing no multiple of nine, then on
the domain 3|Q_r, J_r cannot vanish. For example, forcing 1<=Q_r<=8 makes
Q_r equal 3 or 6 there. This is a valid elementary conditional theorem, not
a claim of a new method. The unconditioned event bounds for branch 279 are
[-42,43], [-53,53], [-51,54], [-51,54]; each includes zero and many multiples
of nine. The actual counterexample shows that support/sign counts plus the
moments and 9O domain cannot supply this desired constant-coordinate bound.
Any useful generalization would need additional indexed balance hypotheses,
not just the common margin profiles: branch 277 has the same profiles and a
true solution with J=0.

No structural contradiction follows in this round. With the exact length-nine
compression added, the saved list has one branch-279 modulo-nine point, but
identifying that point is an exhaustive-list fact and is not our proof of a
formula or an explanatory theorem. We did not use it to assert a symbolic
identity, uniqueness theorem, or publication-ready nonvanishing result.

**Strongest next target:** use the two degree-six coordinates P_0,P_2 jointly
with the exact length-nine signed balances to prove a support-dependent
identity excluding their common zero on the 9O domain. The formula makes
that algebraic target explicit; it does not prove such an identity exists.
A promising result would identify a small set of mixed signed edge products
forced by an explicit class of indexed supports and prove that their carry
cannot cancel. A solver result or the observed value (1,2) of the sole saved
survivor would not suffice. Pure cycle consistency adds nothing to the actual
global phase witnesses.

## 8. Primary precedents and originality assessment

Checked October 14, 2026. The relevant new primary source was accessible in
full: Kaji, Maeno, Nuida, and Numata,
[Polynomial Expressions of Carries in p-ary Arithmetics](https://arxiv.org/pdf/1506.02742),
v3 (2016). Read Section 1.1/Theorem 1 (printed p.2), Section 2 Propositions
1--2 (pp.3--4), and Section 3.1 Proposition 3, Theorem 3 with its proof, and
Remark 1 (pp.5--6). Their addition-carry polynomial has degree at most p^i;
their proof extracts the digit with a binomial coefficient using Lucas'
theorem, and Remark 1 gives the generating-function version. This is a direct
precedent for our degree-three carry step. The signed Boolean presentation
and the six-degree composition do not create a new carry principle. The
preprint's first-page priority notice concerns its multiplication Theorem 2;
we do not transfer that notice into a claim about the addition result.

Granville's [institutional PDF](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/granville.pdf)
was retrieved, but its extracted text was fragmented and it was not relied
upon for a detailed theorem comparison. No claim to have read a usable full
proof there is made. The Kaji et al. proof supplies the needed accessible
primary comparison. Standard compression, norm, and Galois precedents remain
the ones recorded in the preceding notes, including Turner et al. Theorem
3.4 and Corollary 3.5; none is presented here as new.

The precise candidate contribution is the explicit three-shift signed-balance
formula, its careful division domain, and the resulting uniform degree-six
phase representation for length 9p. These are proved mathematical statements,
not merely observations about six solutions. Their ingredients are elementary
and closely related to known carry arithmetic. Whether the specialization is
new or useful enough for publication remains unresolved. It does not yet
explain any empty conditional fiber. The earlier unavailable full algorithms,
historical representative list, and external-replication gaps remain open.
No authors were contacted, and no manuscript change or submission-readiness
claim is warranted from this round alone.

## 9. Reproducibility and resource record

```powershell
.venv/Scripts/python.exe -m scripts.audit_residue_formula pilot
.venv/Scripts/python.exe -m scripts.audit_residue_formula audit
.venv/Scripts/python.exe -m scripts.challenge_residue_formula
.venv/Scripts/python.exe -m pytest tests/test_residue_formula.py -q -p no:cacheprovider --basetemp=tmp/pytest_residue_formula
.venv/Scripts/python.exe -m scripts.package_residue_formula
```

New output is confined to `results/residue_formula/`. All inherited artifacts
and the manuscript are preserved. Input/source SHA-256 hashes are in the new
audit, with integrity and test records and a final manifest. The package
verifies both preceding frozen aggregates/manifests and the current Git base.
The manuscript hash remains
`69e6f7555d5872d78924b60b56dfb494bd3c4c17f8d15899c492089ccc0536a6`.

The 50-record pilot took 0.073 seconds and estimated 10.76 seconds for the
saved-record audit with a fivefold margin. A separate 25-pair positive pilot
gated the remaining formula checks. The final combined audit took 4.61 seconds
on one worker; the bounded degree challenge found its certificate on the
third of at most twenty attempted cubes (192 polynomial evaluations). It did
not enumerate the phase space. Final code added validation of the fixed
intermediate pair, so the new formula audit was repeated after that change;
no inherited census or local-arithmetic audit was rerun. The run limit was
120 seconds, with conservative estimates of 150 MB memory and 2 MB storage;
memory was estimated, not measured. No cap was hit. All runs stayed within
four cores, thirty minutes per run, and 10 GB. The known Python launcher
location diagnostic appeared, but successful runs exited zero.
