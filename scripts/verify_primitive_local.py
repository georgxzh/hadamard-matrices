"""Independent PAF challenges, algebra identities, and frozen positive audit.

No phase assignments are generated; all inputs are frozen witnesses.
"""
import hashlib
import platform
import subprocess
import time
from math import gcd

from scripts.primitive_local_audit import (ROOT, PHI, POW, INV_PI_NUM, load, save,
    red, mul, conj, valuation, phase_norm, inspect, coefficient_bounds)
from scripts.audit_fiber_structure import row, compress, paf, cases
from scripts.audit_residual_obstruction import third_gauge
from scripts.phase_moment_obstruction import model, quadratic_values
from src.ternary_phase import PhaseRow
from src.legendre import _reduce_mod_monic

BASE='beac2a4ca80d8087b01780f677596d60717e178a'


def trace(a):
    total=[0]*24
    for u in range(45):
        if gcd(u,45)==1:
            for i,x in enumerate(a):
                for k,y in enumerate(POW[(u*i)%45]): total[k]+=x*y
    assert not any(total[1:])
    return total[0]


def details(cs,h):
    r=inspect(cs,h)
    xs=[row(x,45) for x in r['masks']]
    m=model(cs)
    assert not any(quadratic_values(m,r['phases']))
    assert all((sum(a*b for a,b in zip(eq[:-1],r['phases']))-eq[-1])%3==0 for eq in m['linear'])
    alt=[compress(x,9) for x in xs]
    r['alternate_compressions']=alt
    r['alternate_energy']=sum(x*x for c in alt for x in c)
    r['alternate_paf_sums']=[a+b for a,b in zip(*map(paf,alt))]
    r['passes_K9']=r['alternate_energy']==82 and r['alternate_paf_sums']==[-10]*8
    r['full_paf_sums']=[a+b for a,b in zip(*map(paf,xs))]
    assert all((x+2)%12==0 for x in r['full_paf_sums'])
    r['trace_defect']=trace(r['norm_defect'])
    r['trace_squared_defect']=trace(mul(r['norm_defect'],r['norm_defect']))
    return r


def frozen_digest():
    # Match every inherited hash from the preceding round, including its new files.
    from scripts.audit_phase_moments import digest
    assert digest()==load('results/phase_moments/audit.json')['baseline']
    for e in load('results/phase_moments/manifest.json')['files']:
        assert hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256']
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'results'],text=True,cwd=ROOT).splitlines()
    changed=subprocess.check_output(['git','diff','--name-only',BASE,'--','results','paper'],text=True,cwd=ROOT).splitlines()
    assert not set(paths).intersection(changed) and not any(p.startswith('paper/') for p in changed)
    h=hashlib.sha256()
    for name in paths:h.update((name+' '+hashlib.sha256((ROOT/name).read_bytes()).hexdigest()+'\n').encode())
    return {'files':len(paths),'ordered_path_sha256_digest':h.hexdigest(),
            'manuscript_sha256':hashlib.sha256((ROOT/'paper/manuscript.tex').read_bytes()).hexdigest()}


def algebra():
    pi=red([1,0,0,0,0,-1])
    assert mul(pi,INV_PI_NUM)==[9]+[0]*23
    assert valuation([3]+[0]*23)==6
    assert valuation([9]+[0]*23)==12
    assert valuation(pi)==1
    f=[1]*5
    power=[1]
    for _ in range(6):
        prod=[0]*(len(power)+4)
        for i,x in enumerate(power):
            for j,y in enumerate(f):prod[i+j]+=x*y
        power=prod
    assert all((x-y)%3==0 for x,y in zip(PHI,power))
    T=[0]*45
    for i in (3,6,12,24):T[i]=1
    for i in (21,33,39,42):T[i]=-1
    T=red(T)
    assert conj(T)==[-x for x in T]
    assert mul(T,T)==[-15]+[0]*23
    G=[7*x for x in T]
    assert mul(G,conj(G))==[735]+[0]*23
    assert all((x-y)%23==0 for x,y in zip(mul(G,G),[1]+[0]*23))
    orbit=[pow(23,i,45) for i in range(12)]
    assert len(set(orbit))==12 and 44 not in orbit and pow(23,12,45)==1
    return {'pi_inverse_numerator':INV_PI_NUM,'valuation_3':6,'valuation_9':12,
            'phi45_mod3_equals_phi5_power6':True,'frobenius_23_orbit':orbit,
            'abstract_23_unit_witness':{'F':[1],'G':G,'T':T,'norm_sum':736,
                'scope':'Unrestricted residue ring only; NOT an allowed branch phase witness.'}}


def positive_record(c,pair):
    pair=third_gauge(pair,c['rows'])
    phases=[]
    for cs,mask in zip(c['rows'],pair):phases.extend(PhaseRow(cs).encode(row(mask,45)))
    r=inspect(c['rows'],{'masks':list(pair),'phases':phases})
    assert not any(r['norm_defect'])
    return pair


def main():
    start=time.perf_counter();baseline=frozen_digest()
    identities=algebra()
    cat=load('results/p5_branch_portfolio/canonical_branches.json')
    local=load('results/primitive_local/audit.json')
    survivors=[]
    for entry in local['cases']:
        c=cat[entry['rank']-1];cs=[c['first'],c['second']]
        # Residue modulo the unique prime above 3 is phase independent.
        for compressed in cs:
            f=[x if abs(x)==1 else 0 for x in compressed]
            reduced=list(_reduce_mod_monic(f,[1]*5));reduced += [0]*(4-len(reduced));reduced[0]-=1
            assert all(x%3==0 for x in reduced)
        bounds=coefficient_bounds(cs)
        assert bounds['max_absolute']<69
        for r in entry['records']:
            assert all(lo<=x<=hi for lo,x,hi in zip(bounds['lower'],r['norm_defect'],bounds['upper']))
            assert all(x%3==0 for x in r['norm_defect'])
            assert r['mod_23']==(not any(r['norm_defect']))
            if r['mod_9']:survivors.append({'rank':entry['rank'],**details(cs,dict(r,free_index=r['source_free_index']))})
    false=next(r for r in survivors if r['rank']==279 and r['passes_K9'])
    assert false['pi_valuation']==12 and false['trace_defect']==0
    assert false['trace_squared_defect']>0
    original=details([cat[278]['first'],cat[278]['second']],load('results/phase_moments/refinement_challenge.json')['witness'])
    assert original['passes_K9'] and original['pi_valuation']==10 and not original['mod_9']
    all_pairs=[(c,p) for c in cases() if 'rank' in c for p in c['solutions']]
    pilot_start=time.perf_counter();checked=set()
    for c,p in all_pairs[:25]:checked.add((c['rank'],positive_record(c,p)))
    pilot_seconds=time.perf_counter()-pilot_start
    estimate=pilot_seconds*len(all_pairs)/25*5
    save('positive_pilot.json',{'pairs':25,'seconds':pilot_seconds,'estimate_seconds_5x':estimate,
         'workers':1,'memory_estimate_bytes':100_000_000,'storage_estimate_bytes':2_000_000,'cap_seconds':120})
    assert estimate<120
    for c,p in all_pairs[25:]:
        assert time.perf_counter()-start<120
        pair=third_gauge(p,c['rows']);key=(c['rank'],pair)
        if key not in checked:checked.add((c['rank'],positive_record(c,p)))
    assert baseline==frozen_digest()
    out={'base_commit':BASE,'baseline':baseline,'algebra':identities,
         'mod_9_survivors':survivors,'mod_9_and_compression_false_positive':false,
         'original_false_positive':original,'frozen_p5_positive_pairs_covered':len(all_pairs),
         'distinct_third_gauge_pairs_checked':len(checked),
         'p7_scope':'Frozen artifacts preserved; no p7 computations in this length-45 audit.',
         'positive_pilot_reused':True,'seconds':time.perf_counter()-start,'workers':1,
         'python':platform.python_version(),'platform':platform.platform(),
         'script_sha256':hashlib.sha256((ROOT/'scripts/verify_primitive_local.py').read_bytes()).hexdigest(),
         'manuscript_action':'Unchanged; neither edited nor compiled.',
         'research_goal_achieved':False,'caps_hit':False}
    save('verification.json',out)
    print({k:v for k,v in out.items() if k not in ('algebra','mod_9_survivors','original_false_positive','mod_9_and_compression_false_positive')})
    print({'new_false_positive':false})


if __name__=='__main__':main()
