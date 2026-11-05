"""Bounded validation of the proved formula; no census or lifting search."""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path
from random import Random
import time

from scripts.residue_formula import build_model, formula, carry_polynomial, histograms
from scripts.primitive_local_audit import ROOT, load, phase_norm
from scripts.audit_fiber_structure import cases,row
from scripts.audit_residual_obstruction import third_gauge
from src.ternary_phase import PhaseRow

OUT=ROOT/'results/residue_formula'


def save(name,obj):
    OUT.mkdir(exist_ok=True,parents=True)
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')


def check(rank,m,record):
    r=formula(m,record['phases'],record['norm_defect'])
    if r['in_domain']:
        return {'rank':rank,'masks':record['masks'],'phases':record['phases'],
                'Q':r['Q'],'J':r['J'],'balance':r['balance'],'tensor':r['tensor']}
    return None


def degree_challenge(m,seconds=15,attempts=20):
    """A bounded finite-difference certificate on the full gauged phase cube.

    It says nothing about minimum polynomial degree on the conditional domain.
    """
    rng=Random(20261014);start=time.perf_counter();tested=0
    gauge=(0,1,12);available=[i for i in range(m['size']) if i not in gauge]
    for attempt in range(attempts):
        if time.perf_counter()-start>seconds:
            return {'outcome':'unresolved_cap','attempts':tested,'seconds':time.perf_counter()-start}
        base=[rng.randrange(3) for _ in range(m['size'])]
        for i in gauge:base[i]=0
        selected=sorted(rng.sample(available,6));coordinate=attempt%4
        values=[];difference=0
        for bits in product(range(2),repeat=6):
            x=base.copy()
            for i,b in zip(selected,bits):x[i]=b
            v=carry_polynomial(m['coordinates'][coordinate],x)
            values.append(v);difference+=(-1)**(6-sum(bits))*v
        tested+=1
        if difference%3:
            return {'outcome':'degree_six_certificate','attempts':tested,'base':base,
                    'phase_indices':selected,'coordinate':coordinate,'values_lexicographic':values,
                    'alternating_sum_mod3':difference%3,'seconds':time.perf_counter()-start,
                    'scope':'Degree of the specified polynomial extension on the full gauged cube, not of J on S in 9O.'}
    return {'outcome':'unresolved_no_certificate','attempts':tested,'seconds':time.perf_counter()-start}


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['pilot','audit']);args=p.parse_args()
    start=time.perf_counter();cat=load('results/p5_branch_portfolio/canonical_branches.json')
    source=load('results/primitive_local/audit.json');survivors=[];count=0;bounds={}
    if args.stage=='audit':
        pilot=load('results/residue_formula/pilot.json')
        assert pilot['estimate_seconds_5x']<120
    for c in source['cases']:
        branch=cat[c['rank']-1];m=build_model([branch['first'],branch['second']])
        bounds[str(c['rank'])]=[{'constant':constant,'positive_events':sum(w>0 for w,_,_,_ in es),
            'negative_events':sum(w<0 for w,_,_,_ in es),
            'lower':constant-sum(w<0 for w,_,_,_ in es),
            'upper':constant+sum(w>0 for w,_,_,_ in es)} for constant,es in m['coordinates']]
        records=c['records'][:25] if args.stage=='pilot' else c['records']
        for h in records:
            assert time.perf_counter()-start<120
            result=check(c['rank'],m,h);count+=1
            if result:survivors.append(result)
    elapsed=time.perf_counter()-start
    if args.stage=='pilot':
        save('pilot.json',{'records':count,'seconds':elapsed,'estimate_seconds_5x':elapsed*1474/count*5,
            'workers':1,'memory_estimate_bytes':150_000_000,'storage_estimate_bytes':2_000_000,'cap_seconds':120})
        print({'pilot_records':count,'seconds':elapsed,'estimate_seconds_5x':elapsed*1474/count*5});return
    # Challenge the formulas outside the moment and divisibility domains.
    rng=Random(45);random_checks=0;domain_rejections=0
    for rank in (277,279):
        c=cat[rank-1];cs=[c['first'],c['second']];m=build_model(cs)
        for _ in range(30):
            x=[rng.randrange(3) for _ in range(m['size'])]
            _,s=phase_norm(cs,x);r=formula(m,x,s)
            domain_rejections+=not r['in_domain'];random_checks+=1
    # New formula audit on frozen positives, quotient duplicates removed.
    positives=[(c,pair) for c in cases() if 'rank' in c for pair in c['solutions']]
    seen=set();models={};pilot_start=time.perf_counter()
    for index,(c,pair) in enumerate(positives):
        assert time.perf_counter()-start<120
        pair=third_gauge(pair,c['rows']);key=(c['rank'],pair)
        if key not in seen:
            m=models.setdefault(c['rank'],build_model(c['rows']))
            x=[]
            for cs,mask in zip(c['rows'],pair):x.extend(PhaseRow(cs).encode(row(mask,45)))
            r=formula(m,x,[0]*24);assert r['J']==[0]*4
            seen.add(key)
        if index==24:
            pe=time.perf_counter()-pilot_start;estimate=pe*len(positives)/25*5
            save('positive_pilot.json',{'pairs':25,'seconds':pe,'estimate_seconds_5x':estimate,
                'cap_seconds':120,'workers':1,'memory_estimate_bytes':150_000_000,'storage_estimate_bytes':2_000_000})
            assert estimate<120
    c=cat[278];m=build_model([c['first'],c['second']]);degree=degree_challenge(m)
    out={'base_commit':'d441e0d8bfe6052c6574ca3702f1b3d40129ff7e','saved_records_checked':count,
         'mod_nine_records':survivors,'integer_event_bounds':bounds,'random_outside_checks':random_checks,
         'outside_domain_rejections':domain_rejections,'frozen_positive_pairs_covered':len(positives),
         'distinct_third_gauge_positives':len(seen),'degree_challenge':degree,
         'seconds':time.perf_counter()-start,'workers':1,'caps_hit':degree['outcome']=='unresolved_cap',
         'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (
             'scripts/residue_formula.py','scripts/audit_residue_formula.py',
             'results/primitive_local/audit.json','results/p5_classification/classification.json')}}
    save('audit.json',out)
    print({k:v for k,v in out.items() if k not in ('mod_nine_records','integer_event_bounds','source_hashes')})
    print('coordinate bounds:',bounds)


if __name__=='__main__':main()
