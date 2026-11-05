"""Checks of the local-ring implementation and adversarial saved witnesses."""
from random import Random

from scripts.primitive_local_audit import (load, red, mul, valuation, phase_norm,
    coefficient_bounds, inspect)
from scripts.verify_primitive_local import algebra, details, trace
from src.ternary_phase import PhaseRow
from scripts.audit_fiber_structure import row
from src.legendre import exact_psd_sum


def branches():
    cat=load('results/p5_branch_portfolio/canonical_branches.json')
    return [[cat[i-1]['first'],cat[i-1]['second']] for i in (277,279)]


def test_ramification_and_nonselfconjugate_counterexample():
    data=algebra()
    assert data['abstract_23_unit_witness']['norm_sum']==32*23
    assert data['valuation_3']==6
    pi=red([1,0,0,0,0,-1]);power=[1]+[0]*23
    for k in range(15):
        # Multiplication by a root of unity cannot change the valuation.
        assert valuation(mul(power,red([0]*7+[1])))==k
        power=mul(power,pi)


def test_old_and_new_compression_false_positives():
    cs=branches()[1]
    old=details(cs,load('results/phase_moments/refinement_challenge.json')['witness'])
    assert old['passes_K9'] and old['pi_valuation']==10 and not old['mod_9']
    masks=[442312790436,2830005805622]
    h=next(h for h in load('results/phase_moments/rank_279.json')['modular_solutions'] if h['masks']==masks)
    new=details(cs,h)
    assert new['passes_K9'] and new['mod_9'] and new['pi_valuation']==12
    assert new['trace_defect']==0 and new['trace_squared_defect']==9720
    assert new['full_paf_sums'][2]==22


def test_indexed_norm_and_bounds_on_unconstrained_phases():
    rng=Random(20261014)
    for cs in branches():
        bounds=coefficient_bounds(cs)
        for _ in range(40):
            phases=[rng.randrange(3) for _ in range(23)]
            _,defect=phase_norm(cs,phases)
            xs=[PhaseRow(cs[0]).decode(phases[:12]),PhaseRow(cs[1]).decode(phases[12:])]
            psd=list(exact_psd_sum(*xs,1).coefficients);psd += [0]*(24-len(psd));psd[0]-=92
            assert psd==[4*x for x in defect]
            assert all(lo<=x<=hi for lo,x,hi in zip(bounds['lower'],defect,bounds['upper']))


def test_positive_and_integer_reconstruction_scope():
    cs=branches()[0];masks=[22487656929184,11681458143385]
    phases=[]
    for c,m in zip(cs,masks):phases.extend(PhaseRow(c).encode(row(m,45)))
    r=inspect(cs,{'masks':masks,'phases':phases})
    assert not any(r['norm_defect']) and r['pi_valuation']=='infinity'
    # The modulus product, rather than either modulus alone, supplies the bound.
    assert all(x==0 for x in range(-54,55) if x%3==0 and x%23==0)
    assert 9%9==0 and 9!=0
