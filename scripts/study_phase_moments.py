"""Bounded pilot then complete modular residual study on ranks 277 and 279.

This explores a new relaxation, not a claim of explanatory nonexistence.
"""
from itertools import product, islice, combinations
from collections import Counter
import argparse
import hashlib
import time
from scripts.phase_moment_obstruction import ROOT, OUT, load, save, model, rref, recover
from src.ternary_phase import PhaseRow


def satisfies(m,x):
    for q in m['quadratic']:
        if (sum(w*((x[v]-x[u]-h)%3)**2 for u,v,h,w in q['edges'])-q['target'])%3:
            return False
    return True


def describe(m,x):
    masks=[];offset=0
    for active in m['active']:
        # Reconstruct signs independently from the new moment formula.
        source=PhaseRow(m['compressed'][len(masks)])
        binary=source.decode(x[offset:offset+len(active)]);offset+=len(active)
        masks.append(sum(1<<i for i,v in enumerate(binary) if v==-1))
    length=3*m['n'];full=(1<<length)-1;errors=[]
    for s in range(1,length//2+1):
        value=sum(length-4*(mask.bit_count()-(mask & (((mask>>s)|(mask<<(length-s)))&full)).bit_count()) for mask in masks)
        assert (value+2)%12==0
        errors.append((value+2)//12)
    return {'phases':x,'masks':masks,'paf_defect_divided_by_12':errors}


def prepare(rank):
    c=load('results/p5_branch_portfolio/canonical_branches.json')[rank-1]
    m=model([c['first'],c['second']]);m['compressed']=[c['first'],c['second']]
    reduced=rref(m['linear'],m['size']);assert reduced['consistent']
    return m,reduced


def visit(rank,begin,end,deadline):
    m,r=prepare(rank);start=time.perf_counter();hits=[];tested=0;complete=True
    for index,values in enumerate(islice(product(range(3),repeat=len(r['free'])),begin,end),begin):
        if tested%4096==0 and time.perf_counter()>deadline:complete=False;break
        x=recover(r,values,m['size']);tested+=1
        if satisfies(m,x):hits.append({'free_index':index,**describe(m,x)})
    return {'rank':rank,'range_begin':begin,'range_end':begin+tested,'range_complete':complete,
            'linear_rank_with_gauges':r['rank'],'free_variables':len(r['free']),
            'total_linear_assignments':3**len(r['free']),'modular_solutions':hits,
            'seconds':time.perf_counter()-start}


def diagnostic(hits):
    full=(1<<len(hits))-1
    zero=[sum(1<<i for i,h in enumerate(hits) if h['paf_defect_divided_by_12'][s]==0) for s in range(22)]
    survivors=full;greedy=[]
    while survivors:
        s=min((s for s in range(22) if s not in greedy),key=lambda s:(survivors & zero[s]).bit_count(),default=None)
        if s is None or survivors & zero[s]==survivors:break
        greedy.append(s);survivors &= zero[s]
    small=None
    for k in range(1,5):
        for chosen in combinations(range(22),k):
            remaining=full
            for s in chosen:remaining &= zero[s]
            if remaining==0:small=[s+1 for s in chosen];break
        if small is not None:break
    return {'exact_pairs':[h['masks'] for h in hits if not any(h['paf_defect_divided_by_12'])],
            'defect_histogram':dict(sorted(Counter(v for h in hits for v in h['paf_defect_divided_by_12']).items())),
            'smallest_empty_shift_intersection_up_to_size_four':small,
            'greedy_shifts':[s+1 for s in greedy],'greedy_survivors':survivors.bit_count(),
            'interpretation':'Finite diagnostic on enumerated modular solutions, not an explanatory theorem or independent full census.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['pilot','complete']);a=parser.parse_args()
    start=time.perf_counter();results=[]
    if a.stage=='pilot':
        for rank in (277,279):results.append(visit(rank,0,10000,start+30))
        estimate=sum(r['seconds']*r['total_linear_assignments']/10000 for r in results)*3
        save('enumeration_pilot.json',{'cases':results,'estimate_seconds_3x':estimate,'workers':1,
             'memory_estimate_bytes':200_000_000,'storage_estimate_bytes':10_000_000,
             'time_limit_seconds':1200,'pilot_time_limit_seconds':30,
             'script_sha256':hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest()})
        print({'estimated_seconds_3x':estimate,'pilot_seconds':time.perf_counter()-start})
        return
    pilot=load('results/phase_moments/enumeration_pilot.json');assert pilot['estimate_seconds_3x']<1200
    for old in pilot['cases']:
        assert old['range_complete']
        result=visit(old['rank'],old['range_end'],old['total_linear_assignments'],start+1200)
        result['modular_solutions']=old['modular_solutions']+result['modular_solutions']
        result['range_begin']=0;result['seconds']+=old['seconds']
        if result['range_complete']:
            result['diagnostic']=diagnostic(result['modular_solutions'])
        save('rank_'+str(result['rank'])+'.json',result);results.append(result)
        print({'rank':result['rank'],'complete':result['range_complete'],'modular_solutions':len(result['modular_solutions']),
               'seconds_including_pilot':result['seconds'],'diagnostic':result.get('diagnostic')},flush=True)
    save('enumeration_summary.json',{'complete':all(r['range_complete'] for r in results),
         'cases':[{k:v for k,v in r.items() if k!='modular_solutions'}|{'modular_solution_count':len(r['modular_solutions'])} for r in results],
         'new_run_seconds':time.perf_counter()-start,'pilot_reused':True,
         'script_sha256':hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest()})


if __name__=='__main__':main()
