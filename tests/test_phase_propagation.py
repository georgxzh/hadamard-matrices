"""Soundness/coverage checks independent of the propagation implementation."""
import json
from itertools import product

import pytest

from scripts.benchmark_staged_uncompression import _known_pair
from scripts.classify_p5_lifts import independent_masks, packed_key
from src.legendre import compress
from src.phase_propagation import PhasePropagationModel, search_conditioned, triangle_support


def p3_pair():
    return tuple(compress(row,9) for row in _known_pair(3))


def exact_masks(pair):
    length=3*len(pair[0]); table={}; found=[]
    for m in independent_masks(pair[0]): table.setdefault(packed_key(m,length,length//2),[]).append(m)
    for m in independent_masks(pair[1]):
        key=packed_key(m,length,length//2)
        if all(v<=2*length-2 for v in key):
            found.extend((other,m) for other in table.get(bytes(2*length-2-v for v in key),()))
    return sorted(found)


def test_triangle_support_exhaustively():
    for x,y,z in product(range(8),repeat=3):
        witnesses=[t for t in product(range(3),repeat=3)
                   if all(d & (1 << v) for d,v in zip((x,y,z),t)) and (t[0]+t[1]-t[2])%3==0]
        expected=tuple(sum(1 << v for v in {t[i] for t in witnesses}) for i in range(3))
        assert triangle_support(x,y,z)==expected


@pytest.mark.parametrize('mode',['anchor','all'])
def test_difference_solver_reproduces_every_p3_lift(mode):
    pair=p3_pair(); result=PhasePropagationModel(*pair,cycle_mode=mode).search(seconds=30)
    assert result['complete'] and result['ordered_pairs']==135
    assert result['solutions']==exact_masks(pair)


@pytest.mark.parametrize('partner_filter',[False,True])
@pytest.mark.parametrize('folded_bounds',[False,True])
def test_conditioned_solver_variants_reproduce_every_p3_lift(partner_filter,folded_bounds):
    pair=p3_pair()
    result=search_conditioned(*pair,partner_filter=partner_filter,folded_bounds=folded_bounds)
    assert result['complete'] and result['ordered_pairs']==135
    assert result['solutions']==exact_masks(pair)


def test_all_p5_known_solutions_survive_domain_propagation():
    catalog=json.loads(open('results/p5_branch_portfolio/canonical_branches.json').read())
    census=json.loads(open('results/p5_classification/classification.json').read())
    checked=0
    for entry,branch in zip(catalog,census):
        if not branch['solutions']: continue
        model=PhasePropagationModel(entry['first'],entry['second'])
        for masks in branch['solutions']:
            phases=[row.encode(tuple(1-2*((mask>>i)&1) for i in range(45))) for row,mask in zip(model.rows,masks)]
            actual=[(phases[r][v]-phases[r][u])%3 for r,u,v in model.edges]
            # Mixed singleton/two-value/full domains, all containing this witness.
            domains=[(1 << value) | (0 if i%3==0 else (1 << ((value+1)%3)) if i%3==1 else 7)
                     for i,value in enumerate(actual)]
            assert model.propagate(domains)
            assert all(d & (1 << v) for d,v in zip(domains,actual))
            checked+=1
    assert checked==2976


def test_limits_never_report_exact_zero():
    result=PhasePropagationModel(*p3_pair()).search(max_nodes=1)
    assert not result['complete'] and result['ordered_pairs'] is None
    result=search_conditioned(*p3_pair(),max_stored_candidates=1)
    assert not result['complete'] and result['ordered_pairs'] is None
    result=search_conditioned(*p3_pair(),max_nodes=1)
    assert not result['complete'] and result['ordered_pairs'] is None


def test_cycle_realization_on_arbitrary_phases():
    model=PhasePropagationModel(*p3_pair(),paf_bounds=False)
    phases=[tuple(i*i%3 for i in range(len(row.active))) for row in model.rows]
    domains=[7]*len(model.edges)
    for edge,(r,u,v) in enumerate(model.edges):
        if u==0: domains[edge]=1 << phases[r][v]
    assert model.propagate(domains)
    assert domains==[1 << ((phases[r][v]-phases[r][u])%3) for r,u,v in model.edges]
