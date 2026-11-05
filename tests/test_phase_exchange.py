from scripts.primitive_local_audit import load, red
from scripts.compression_residue import restricted_domain, folded_balances
from scripts.residue_formula import tensor_coefficients
from scripts.phase_exchange import delta_factor, delta_factor_offset, norm_change, sub


def test_frozen_origin_domains_and_bounded_inventory():
    a=load('results/phase_exchange/audit.json')
    assert a['raw_pairs_total']==363 and a['evaluated_nontrivial_neighbors']==26
    assert [x['neighbors'] for x in a['summary']]==[7,9,10]
    assert not any(x['neighbors_in_full_domain'] for x in a['summary'])
    assert a['pilot_neighbors_reused']==3 and a['neighbor_depth']==1
    assert [x['J'] for x in a['origins']]==[[0,0,0,0],[1,0,2,2],[0,0,1,1]]
    assert [any(x['G']) for x in a['origins']]==[False,False,True]
    assert all(x['full_domain'] for x in a['origins'])
    for inv in a['inventories']:
        assert len(inv['pairs'])==sum(inv['counts'].values())==121


def test_indexed_factorization_and_integer_changes_on_permitted_neighbors():
    a=load('results/phase_exchange/audit.json')
    for x in a['checks']:
        old=next(o for o in a['origins'] if o['masks']==x['origin_masks'])
        new=x['endpoint']; move=x['move']; row=old['rows'][move['side']]
        assert delta_factor(row,move)==delta_factor_offset(row,move)==x['delta_F']
        assert norm_change(old['F'][move['side']],x['delta_F'])==sub(new['S'],old['S'])==x['delta_S']
        assert old['charges']==new['charges'] and old['G']==new['G']
        assert sum(u!=v for u,v in zip(old['phases'],new['phases']))==2
        assert all(new['phases'][i]==0 for i in (0,1,12))
        assert max(x['affected_edge_counts'])<=4 and max(map(abs,x['delta_B']))<=4
        assert not restricted_domain(x['delta_B'])
        assert x['delta_J'] is None  # Never divide a non-domain difference.


def test_private_edge_structural_obstruction():
    a=load('results/phase_exchange/audit.json')
    counts=[]
    for origin in a['origins']:
        private=0
        for x in a['checks']:
            if x['origin_masks']!=origin['masks']:continue
            shifts=[r for r in range(1,15) if x['affected_edge_counts'][r]==1]
            private+=bool(shifts)
            for r in shifts:
                assert sorted(x['delta_B'][r::15])==[-1,0,1]
        counts.append(private)
    assert counts==[3,3,4]


def test_lattice_bound_is_a_real_hypothesis():
    # An abstract symmetric integer defect difference, NOT a phase witness.
    # Tensor rows 1,4 carry (-6,3,3); rows 2,3 carry the negative.
    d=[]
    for s in range(45):
        r,e=s%5,2*s%9
        v={0:-6,3:3,6:3}.get(e,0)
        d.append(v if r in (1,4) else -v if r in (2,3) else 0)
    assert all(d[s]==d[-s%45] for s in range(45))
    assert all(sum(d[r::15])==0 for r in range(15))
    assert not any(folded_balances(d))
    assert restricted_domain(d) and any(red(d))
    assert all(x%9==0 for row in tensor_coefficients(d) for x in row)
    assert max(map(abs,d))==6 and max(max(d[r::15])-min(d[r::15]) for r in range(15))==9
