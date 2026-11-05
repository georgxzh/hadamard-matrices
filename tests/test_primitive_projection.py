import pytest
from scripts.primitive_local_audit import load
from scripts.primitive_projection import projection,check45


def test_saved_trace_identity_and_gauges():
    a=load('results/primitive_projection/audit.json')
    assert len(a['checks'])==8 and a['new_phase_assignments']==0 and a['pilot_reused']==1
    for c in a['checks']:
        ep=c['endpoint'];p=c['projection']
        assert all(ep['phases'][i]==0 for i in (0,1,12))
        assert p['S']==ep['S'] and p['full_9O']==ep['full_domain']
        assert p['trace_norm']==9*p['W']
        assert p['W']==5*sum(x*x for x in ep['B'])-sum(x*x for x in ep['G'])
    assert [c['projection']['W'] for c in a['checks']]==[0,432,432,486,972,1080,540,360]


def test_nonnegative_cycle_shortcut_has_exact_counterexample():
    p=load('results/primitive_projection/audit.json')['integer_relaxation']
    assert not any(p['S']) and p['full_9O'] and p['W']==0
    assert any(p['G']) and any(p['B'])
    assert p['R']==[3 if s%9 in (1,8) else 0 for s in range(45)]
    assert all(min(p['R'][r::15])==0 for r in range(15))
    assert p['B'][0]==p['B'][15]==p['B'][30]==0
    assert all(p['B'][s]==p['B'][-s%45] for s in range(45))


def test_trace_congruence_does_not_test_full_domain():
    c=load('results/primitive_projection/audit.json')['checks'][-1]
    assert c['endpoint']['masks']==[22487656929184,9405125214970]
    assert not any(c['endpoint']['G'])
    assert c['projection']['trace_norm']%81==0
    assert not c['endpoint']['full_domain'] and c['endpoint']['J'] is None
    assert c['endpoint']['S'][0]==-1


def test_projection_at_other_small_primes_and_missing_hypothesis():
    # Explicit integer arrays only; no binary or phase search at other lengths.
    for p in (5,7,11):
        b=[0]*(9*p);b[0]=2;b[3*p]=b[6*p]=-1
        out=projection(b,p)
        assert out['W']==6*(p-1)
        assert sum(x*x for x in out['E'])==p*out['W']
        periodic=[(0,2,-1,0,-1,-1,0,-1,2)[i%9] for i in range(9*p)]
        assert projection(periodic,p)['W']==0
    invalid=[0]*45;invalid[0]=1
    with pytest.raises(ValueError):check45(invalid)
