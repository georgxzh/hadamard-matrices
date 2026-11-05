"""Read-only validation against frozen positives and bounded further challenges."""
from collections import Counter
from itertools import product
from pathlib import Path
import argparse
import hashlib
import platform
import subprocess
import time
from scripts.phase_moment_obstruction import ROOT,OUT,load,save,model,rref,recover,quadratic_values
from scripts.study_phase_moments import satisfies,describe
from scripts.audit_fiber_structure import cases,row
from scripts.audit_residual_obstruction import third_gauge
from src.ternary_phase import PhaseRow

BASE='5fbcfcee28b7e429ed20732baff2b942b047c7e7'


def digest():
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'results'],cwd=ROOT,text=True).splitlines()
    changed=subprocess.check_output(['git','diff','--name-only',BASE,'--','results','paper'],cwd=ROOT,text=True).splitlines()
    assert not set(changed).intersection(paths) and not any(p.startswith('paper/') for p in changed)
    h=hashlib.sha256()
    for name in paths:h.update((name+' '+hashlib.sha256((ROOT/name).read_bytes()).hexdigest()+'\n').encode())
    return {'files':len(paths),'ordered_path_sha256_digest':h.hexdigest(),
            'manuscript_sha256':hashlib.sha256((ROOT/'paper/manuscript.tex').read_bytes()).hexdigest()}


def check_case(c):
    m=model(c['rows']);r=rref(m['linear'],m['size']);raw_rank=rref(m['linear'][:m['n']-1],m['size'])
    wrong_carry=0;example=None
    rows=[PhaseRow(cs) for cs in c['rows']]
    for pair in c['solutions']:
        pair=third_gauge(pair,c['rows']);x=[]
        for mask,source in zip(pair,rows):x.extend(source.encode(row(mask,3*m['n'])))
        assert all((sum(a*b for a,b in zip(eq[:-1],x))-eq[-1])%3==0 for eq in m['linear'])
        assert not any(quadratic_values(m,x))
        # Challenge the tempting, but false, omission of boundary carries.
        wrong=[q['shift'] for q in m['quadratic'] if sum(w*(x[v]-x[u]) for u,v,h,w in q['edges'])%3]
        if wrong:wrong_carry+=1;example=example or {'masks':pair,'phases':x,'failing_shifts_without_carries':wrong}
    return {'id':c['id'],'phase_variables':m['size'],'linear_rank_before_gauges':raw_rank['rank'],
            'linear_consistent':r['consistent'],'rank_with_gauges':r['rank'],'free_variables':len(r['free']),
            'frozen_positive_pairs_checked':len(c['solutions']),'wrong_carry_rejected_pairs':wrong_carry,
            'wrong_carry_counterexample':example}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['pilot','complete']);a=parser.parse_args()
    start=time.perf_counter();all_cases=list(cases());out=[]
    if a.stage=='pilot':
        for c in all_cases[:25]:out.append(check_case(c))
        elapsed=time.perf_counter()-start
        save('audit_pilot.json',{'cases':out,'seconds':elapsed,'estimate_seconds_10x':elapsed*len(all_cases)/25*10,
             'workers':1,'memory_estimate_bytes':200_000_000,'storage_estimate_bytes':5_000_000,'limit_seconds':300})
        print({'seconds':elapsed,'estimate_seconds_10x':elapsed*len(all_cases)/25*10});return
    baseline=digest();pilot=load('results/phase_moments/audit_pilot.json');assert pilot['estimate_seconds_10x']<300
    out=pilot['cases'].copy()
    for c in all_cases[len(out):]:
        if time.perf_counter()-start>300:raise TimeoutError('Unresolved audit cap')
        out.append(check_case(c))
    # One empty branch per previously established mixed-profile group.
    groups=load('results/residual_obstruction/audit.json')['mixed_profile_groups']
    cat=load('results/p5_branch_portfolio/canonical_branches.json');old=load('results/p5_classification/classification.json')
    challenges=[]
    for group in groups:
        rank=next(r for r in group if old[r-1]['canonical_pairs']==0)
        c=cat[rank-1];m=model([c['first'],c['second']]);m['compressed']=[c['first'],c['second']]
        r=rref(m['linear'],m['size']);witness=None;tested=0
        if r['consistent']:
            for values in product(range(3),repeat=len(r['free'])):
                if tested==10000 or time.perf_counter()-start>300:break
                tested+=1;x=recover(r,values,m['size'])
                if satisfies(m,x):witness=describe(m,x);break
        challenges.append({'rank':rank,'tested':tested,'modular_witness':witness,
             'outcome':'feasible_relaxation' if witness else 'unresolved_bounded_search',
             'exact_zero_claimed':False})
    assert digest()==baseline
    save('audit.json',{'complete_frozen_validation':True,'base_commit':BASE,'baseline':baseline,
         'frozen_results_and_paper_unchanged':True,'cases':out,'pilot_reused':True,
         'positive_pairs_checked':sum(r['frozen_positive_pairs_checked'] for r in out),
         'linear_inconsistent_branches':[r['id'] for r in out if not r['linear_consistent']],
         'rank_histogram':dict(Counter((str(r['linear_rank_before_gauges']) for r in out))),
         'wrong_carry_rejections':sum(r['wrong_carry_rejected_pairs'] for r in out),
         'matched_empty_challenges':challenges,'seconds':time.perf_counter()-start,
         'python':platform.python_version(),'platform':platform.platform(),
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print({'positive_pairs':sum(r['frozen_positive_pairs_checked'] for r in out),
           'inconsistent':sum(not r['linear_consistent'] for r in out),
           'further_witnesses':sum(bool(c['modular_witness']) for c in challenges),
           'wrong_carry_rejections':sum(r['wrong_carry_rejected_pairs'] for r in out),
           'seconds':time.perf_counter()-start,'baseline':baseline})


if __name__=='__main__':main()
