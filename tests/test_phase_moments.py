from itertools import combinations
from random import Random
from scripts.phase_moment_obstruction import load,model,quadratic_values,rref,recover
from scripts.study_phase_moments import prepare
from scripts.audit_fiber_structure import row,compress,paf
from scripts.audit_residual_obstruction import third_gauge
from scripts.factor_phase_moment_defect import monic_divide
from src.ternary_phase import PhaseRow


def test_moment_system_equivalent_to_all_shift_paf_modulo_twelve():
    rng=Random(20261013)
    for rank in (277,279):
        m,_=prepare(rank);sources=[PhaseRow(c) for c in m['compressed']]
        for _ in range(100):
            x=[rng.randrange(3) for _ in range(m['size'])]
            linear=all((sum(a*b for a,b in zip(e[:-1],x))-e[-1])%3==0 for e in m['linear'][:m['n']-1])
            modular=linear and not any(quadratic_values(m,x))
            k=len(m['active'][0]);xs=[sources[0].decode(x[:k]),sources[1].decode(x[k:])]
            expected=all((a+b+2)%12==0 for a,b in zip(paf(xs[0]),paf(xs[1])))
            assert modular==expected


def test_every_saved_modular_witness_by_independent_tuple_paf():
    for rank,count in ((277,734),(279,740)):
        data=load(f'results/phase_moments/rank_{rank}.json');m,r=prepare(rank)
        assert data['range_complete'] and data['range_end']==3**13
        hits=data['modular_solutions'];assert len(hits)==count
        assert len({h['free_index'] for h in hits})==count
        for h in hits:
            xs=[row(mask,45) for mask in h['masks']]
            assert [compress(x,15) for x in xs]==[tuple(c) for c in m['compressed']]
            x=[v for source,binary in zip(map(PhaseRow,m['compressed']),xs) for v in source.encode(binary)]
            assert x==h['phases'] and not any(quadratic_values(m,x))
            assert all(x[i]==0 for i in m['gauges'])
            assert recover(r,[x[i] for i in r['free']],m['size'])==x
            values=[a+b for a,b in zip(paf(xs[0]),paf(xs[1]))]
            assert all((v+2)%12==0 for v in values)
            assert [(v+2)//12 for v in values[:22]]==h['paf_defect_divided_by_12']


def test_combined_relaxation_counterexample_and_carry_holonomy():
    record=load('results/phase_moments/refinement_challenge.json');h=record['witness']
    m,_=prepare(279);x=h['phases'];xs=[row(mask,45) for mask in h['masks']]
    assert h['masks']==[22964264347100,2872821395978]
    assert list(third_gauge(h['masks'],m['compressed']))==h['masks']
    us=[compress(binary,9) for binary in xs]
    assert sum(v*v for u in us for v in u)==82
    assert all(a+b==-10 for a,b in zip(paf(us[0]),paf(us[1])))
    assert paf(xs[0])[4]+paf(xs[1])[4]==10
    assert not any(quadratic_values(m,x))
    # First three active residues form a directed cycle with one boundary wrap.
    cycle=((0,1,0),(1,2,0),(2,0,1))
    assert sum((x[v]-x[u]-carry)%3 for u,v,carry in cycle)%3==2
    assert sum((x[v]-x[u])%3 for u,v,carry in cycle)%3==0


def test_frozen_positive_orbit_and_no_four_shift_explanation():
    cat=load('results/p5_branch_portfolio/canonical_branches.json')[276]
    old=load('results/p5_classification/classification.json')[276]['solutions']
    expected={third_gauge(pair,[cat['first'],cat['second']]) for pair in old}
    assert expected=={tuple(p) for p in load('results/phase_moments/rank_277.json')['diagnostic']['exact_pairs']}
    hits=load('results/phase_moments/rank_279.json')['modular_solutions']
    masks=[sum(1<<i for i,h in enumerate(hits) if h['paf_defect_divided_by_12'][s]==0) for s in range(22)]
    for shifts in combinations(range(22),4):
        remaining=(1<<len(hits))-1
        for s in shifts:remaining &= masks[s]
        assert remaining
    assert not any(not any(h['paf_defect_divided_by_12']) for h in hits)


def test_integer_defect_factorization():
    f=load('results/phase_moments/defect_factorization.json')
    q,r=monic_divide(f['normalized_defect_coefficients'],f['divisor_coefficients'])
    assert q==f['quotient_coefficients'] and not any(r)
    reconstructed=[0]*45
    for i,a in enumerate(q):
        for j,b in enumerate(f['divisor_coefficients']):reconstructed[i+j]+=a*b
    assert reconstructed==f['normalized_defect_coefficients']
    assert any(q) and len(q)==24
