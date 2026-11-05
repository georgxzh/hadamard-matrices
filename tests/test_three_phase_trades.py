from itertools import product
from scripts.primitive_local_audit import load
from scripts.three_phase_trades import flow_type,delta_f,landing_delta_f
from scripts.phase_exchange import sub,norm_change
from scripts.compression_residue import restricted_domain


def test_complete_budget_and_all_sign_patterns_retained():
    a=load('results/three_phase_trades/audit.json')
    assert a['raw_candidates_total']==9240 and a['neighbor_depth']==1
    assert a['new_distinct_neighbors_evaluated']==14 and a['pilot_endpoints_reused']==3
    assert [x['neighbors'] for x in a['summary']]==[4,4,6]
    assert all(x['in_domain']==0 for x in a['summary'])
    assert [x['permitted_types'].get('mixed_sign',0) for x in a['inventories']]==[4,4,4]
    for x in a['inventories']:
        assert sum(x['status_counts'].values())==x['raw_candidates']==385*8
    assert flow_type([1,1,-1],[0,1,0],[1,2,2])=={'epsilon':1,'tails':[0,1,2],'type':'mixed_sign'}


def test_balanced_flank_identity_all_96_abstract_cases():
    # Sign/label algebra only, not extra branch assignments or trade neighbors.
    for signs in product((-1,1),repeat=3):
        for epsilon,sigma,h in product((-1,1),(-1,1),range(3)):
            v=[0]*3
            for t,c in enumerate(signs):v[(t+h+epsilon*((1+sigma*c)//2))%3]+=c
            assert sum(v)==sum(signs)
            assert sum(x*x for x in v)==(3 if len(set(signs))==1 else 1)


def test_endpoints_integer_factorizations_and_failed_simplification():
    a=load('results/three_phase_trades/audit.json')
    for x in a['checks']:
        old=next(o for o in a['origins'] if o['masks']==x['origin_masks']);new=x['endpoint'];m=x['move']
        assert old['full_domain'] and not new['full_domain'] and new['J'] is None
        assert old['charges']==new['charges'] and old['G']==new['G']
        assert len({i%3 for i in m['positions']})==1
        assert all(new['phases'][i]==0 for i in (0,1,12))
        row=old['rows'][m['side']]
        assert delta_f(row,old['phases'],m)==landing_delta_f(row,m)==x['delta_F']
        assert norm_change(old['F'][m['side']],x['delta_F'])==sub(new['S'],old['S'])==x['delta_S']
        assert max(map(abs,x['delta_B']))<=6 and not restricted_domain(x['delta_B'])
    x=next(x for x in a['checks'] if x['endpoint']['masks'][0]==22410481731560)
    assert x['origin_masks']==[22487656929184,11681458143385]
    assert x['move']['old_labels']==[1,0,0] and x['move']['new_labels']==[2,2,1]
    assert sorted(x['move']['old_labels'])!=sorted(x['move']['new_labels'])
    assert x['endpoint']['S'][0]==1


def test_structural_hypotheses_are_not_exported_to_failed_compression_origin():
    a=load('results/three_phase_trades/audit.json')
    assert [[h['uniform_structural_hypothesis'] for h in o['hypotheses']] for o in a['origins']]==[
        [True,True],[True,True],[False,False]]
    assert [any(o['G']) for o in a['origins']]==[False,False,True]
    assert a['origins'][2]['J']==[0,0,1,1]
    assert all(x['endpoint']['G']==a['origins'][2]['G'] for x in a['checks'] if x['origin_masks']==a['origins'][2]['masks'])
