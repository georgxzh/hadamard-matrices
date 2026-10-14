from itertools import product
import pytest
from scripts.residue_formula import (binomial,build_model,formula,carry_polynomial,
    residue_basis,tensor_coefficients,tensor_to_standard,SETS)
from scripts.primitive_local_audit import load,POW,phase_norm
from src.legendre import cyclotomic_polynomial,_reduce_mod_monic


def test_integral_change_of_basis_on_all_monomials():
    for s in range(45):
        b=[0]*45;b[s]=1
        assert tensor_to_standard(tensor_coefficients(b))==POW[s]


def test_negative_signed_carry_and_degree_three_extraction():
    for n in range(-100,101):assert binomial(n,3)%3==(n//3)%3
    # Boolean events are realized independently as equality to the fixed anchor.
    for c in range(-4,5):
        for signs in product((-1,1),repeat=3):
            es=[(w,0,i+1,0) for i,w in enumerate(signs)]
            for ys in product(range(2),repeat=3):
                phases=[0]+[0 if y else 1 for y in ys]
                q=c+sum(w*y for w,y in zip(signs,ys))
                assert carry_polynomial((c,es),phases)==(q//3)%3


def test_saved_positive_and_counterexample():
    cat=load('results/p5_branch_portfolio/canonical_branches.json')
    rows=load('results/residue_formula/audit.json')['mod_nine_records']
    for h in rows:
        c=cat[h['rank']-1];cs=[c['first'],c['second']]
        _,s=phase_norm(cs,h['phases']);r=formula(build_model(cs),h['phases'],s)
        assert r['J']==h['J']
        assert all(x%3==0 for x in r['Q'])
        k=[x//3 for x in r['balance']]
        a=k[1]+k[4]+k[6]
        sparse=[a-k[5]-k[10],a-k[14]-k[19]-k[21],
                a-k[12]-k[17]-k[22],a-k[3]-k[8]-k[13]]
        assert r['J']==[x%3 for x in sparse]


def test_domain_and_sixth_difference_certificate():
    cat=load('results/p5_branch_portfolio/canonical_branches.json');c=cat[278]
    m=build_model([c['first'],c['second']])
    old=load('results/primitive_local/audit.json')['saved_false_positive']
    with pytest.raises(ValueError):residue_basis(old['norm_defect'])
    assert formula(m,old['phases'],old['norm_defect'])['J'] is None
    cert=load('results/residue_formula/audit.json')['degree_challenge']
    values=[];difference=0
    for bits in product(range(2),repeat=6):
        x=cert['base'].copy()
        for i,b in zip(cert['phase_indices'],bits):x[i]=b
        v=carry_polynomial(m['coordinates'][cert['coordinate']],x)
        values.append(v);difference+=(-1)**(6-sum(bits))*v
    assert values==cert['values_lexicographic'] and difference%3==2


def test_general_prime_seven_balance_identity():
    # Tests the generalized algebra on signed balance polynomials, not binary lifts.
    p=7;L=9*p;b_inv=pow(p,-1,9)
    phi=cyclotomic_polynomial(L)
    for j in range(12):
        # B=3*z^j*(z^(3p)-1)^2 gives S=-9*omega*z^j and nonzero J=-alpha^j.
        B=[0]*L;B[(j+6*p)%L]=3;B[(j+3*p)%L]=-6;B[j]=3
        S=list(_reduce_mod_monic(B,phi))
        assert all(x%9==0 for x in S)
        got=list(_reduce_mod_monic([x//9 for x in S],[1]*p));got += [0]*(p-1-len(got))
        U=[sum(B[s] for s in range(L) if s%p==r and (b_inv*s)%9>=6) for r in range(p)]
        expect=[((U[-1]-U[r])//3)%3 for r in range(p-1)]
        assert [x%3 for x in got]==expect
        assert any(expect)
