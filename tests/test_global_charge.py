from collections import Counter
from itertools import product
from scripts.global_charge import occupancy_count,row_paf,transport
from scripts.primitive_local_audit import load


def test_closed_count_against_independent_laurent_coefficient_dp():
    # Abstract occupancy algebra; no branch phase assignments generated.
    for p,q in product(range(5),repeat=2):
        counts=Counter({(0,0,0):1})
        for sign in [1]*p+[-1]*q:
            nxt=Counter()
            for r,n in counts.items():
                for label in range(3):
                    rr=list(r);rr[label]+=sign;nxt[tuple(rr)]+=n
            counts=nxt
        assert sum(counts.values())==3**(p+q)
        for r in product(range(-q,p+1),repeat=3):
            assert occupancy_count(p,q,r)==counts[r]


def test_characters_remain_distinct_with_one_pin():
    for n in range(2,13):
        chars=[]
        for i in range(n):
            for j in range(n):
                if i==j:continue
                v=[0]*(n-1)
                if i:v[i-1]+=1
                if j:v[j-1]-=1
                chars.append(tuple(x%3 for x in v))
        assert len(set(chars))==n*(n-1)
        assert (0,)*(n-1) not in chars


def test_saved_domain_counterexamples_and_global_transport_checks():
    a=load('results/global_charge/audit.json')
    assert a['new_assignments_total']==7 and a['pilot_reused']==1 and not a['search_performed']
    cat=load('results/p5_branch_portfolio/canonical_branches.json')
    for c in a['checks']:
        old,new=c['source'],c['target']
        assert old['G']==new['G'] and not new['full_domain'] and new['J'] is None
        assert new['S'][0]%9!=0
        assert [row_paf(x['row']) for x in old['charges']]==[row_paf(x['row']) for x in new['charges']]
        assert all(new['phases'][i]==0 for i in (0,1,12))
        cs=cat[c['source_rank']-1];ds=cat[c['target_rank']-1]
        back=transport([ds['first'],ds['second']],[cs['first'],cs['second']],new['phases'])
        assert back['phases']==old['phases']
    first=a['checks'][0]
    assert not any(first['source']['S']) and not any(first['target']['G'])
    assert first['target']['masks']==[22487656929184,9405125214970]
    assert first['target']['S'][0]==-1
    outsider=a['checks'][-1]['source']
    assert not any(outsider['G']) and not outsider['full_domain']
    assert outsider['charges'][1]['charges'][1]==[0,1,0]
    assert all(b['exact_compression_members']==b['full_9O_members']==0 for b in a['saved_relaxations'])


def test_mapping_obstruction_and_exceptional_class_counts():
    a=load('results/global_charge/audit.json')
    m={x['old']:x for x in a['checks'][0]['transport']['mapping']}
    assert (m[1]['new'],m[1]['k_mod5'])==(4,2)
    assert (m[2]['new'],m[2]['k_mod5'])==(2,0)
    assert [x['count'] for x in a['checks'][0]['charge_fiber_counts']]==[864,360]
    assert not a['checks'][-1]['source_hypotheses'][1]['uniform_structural_hypothesis']
    assert a['checks'][2]['source']['J']==[0,0,1,1]
    assert a['checks'][2]['source']['G'][:3]==[0,6,-3]
