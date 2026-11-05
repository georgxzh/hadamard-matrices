"""Deterministic stratified p=7 portfolio; bounded serial experimental stages.

Native implementation is frozen. Selection precedes lift timings/outcomes.
Each subcommand is a separate <=30-minute run; no p=37 domain accepted.
"""
import argparse
import hashlib
import json
import math
import os
import platform
import random
import subprocess
import time
from collections import Counter
from itertools import product
from pathlib import Path
from statistics import median

from scripts.classify_p5_lifts import ROOT,digest,save
from src.legendre import (compress,periodic_autocorrelation,structured_compressed_pair,
                          check_legendre_pair,check_negative_support_sds)
from src.staged_uncompression import FactorThreeBranch,IntermediatePBModel
from src.spectral_join import search,coefficients,NATIVE,COMPILER,FLAGS
from src.ternary_phase import TernaryPhasePBModel

OUT=ROOT/'results/p7_portfolio'
PATTERNS=((12,20),(13,19),(14,18),(15,17),(16,16))
EXE=ROOT/'tmp/full_paf_audit.exe'


def identifier(pair):
    return hashlib.sha256(json.dumps(pair,separators=(',',':')).encode()).hexdigest()


def canonical(pair):
    prescribed=structured_compressed_pair(7,3)
    FactorThreeBranch(*prescribed,*pair)
    model=IntermediatePBModel(*prescribed,canonical_translations=True)
    pair=model.canonicalize_pair(*pair)
    assert model.first_failed_constraint(*pair) is None
    return pair


def acquire_one(target,seed,iterations=200_000,seconds=20):
    rng=random.Random(seed); prescribed=structured_compressed_pair(7,3); n=21
    options=[[tuple(t for t in product((-3,-1,1,3),repeat=3) if sum(t)==value)
              for value in row] for row in prescribed]
    targets=[122]+[-6]*10; start=time.perf_counter(); best=None; found=None
    for iteration in range(iterations):
        if iteration%128==0 and time.perf_counter()-start>=seconds: break
        if iteration%4000==0:
            rows=[[0]*n for _ in range(2)]
            for side in range(2):
                for residue in range(7):
                    for k,value in enumerate(rng.choice(options[side][residue])): rows[side][residue+k*7]=value
            residual=[(sum(periodic_autocorrelation(row,s) for row in rows)-t)//4 for s,t in enumerate(targets)]
            active=[sum(abs(v)==1 for v in row) for row in rows]
            energy=sum(v*v for v in residual)+4*sum((a-b)**2 for a,b in zip(active,target))
        side,residue=rng.randrange(2),rng.randrange(7); replacement=rng.choice(options[side][residue]); row=rows[side]
        delta={residue+k*7:v-row[residue+k*7] for k,v in enumerate(replacement) if v!=row[residue+k*7]}
        change=[sum(d*(row[(i+s)%n]+row[(i-s)%n]+delta.get((i+s)%n,0)) for i,d in delta.items())//4 for s in range(11)]
        candidate=[a+b for a,b in zip(residual,change)]; counts=active.copy()
        counts[side]+=sum((abs(row[i]+d)==1)-(abs(row[i])==1) for i,d in delta.items())
        value=sum(v*v for v in candidate)+4*sum((a-b)**2 for a,b in zip(counts,target))
        temperature=25*(.02**((iteration%4000)/3999))
        if value<=energy or rng.random()<math.exp((energy-value)/temperature):
            for i,d in delta.items(): row[i]+=d
            residual,active,energy=candidate,counts,value
        best=energy if best is None else min(best,energy)
        if energy==0:
            found=canonical(rows); assert tuple(active)==target; break
    return {'target':target,'seed':seed,'iteration_limit':iterations,'seconds_limit':seconds,
            'iterations':iteration+1,'best_energy':best,'elapsed_seconds':time.perf_counter()-start,
            'status':'verified_intermediate' if found else 'acquisition_unresolved','pair':found,
            'guard_fired':found is None and iteration+1<iterations}


def acquisition():
    start=time.perf_counter(); OUT.mkdir(exist_ok=True); records=[]
    for index,target in enumerate(PATTERNS):
        for offset in range(4):
            r=acquire_one(target,20261006+100*index+offset); records.append(r)
            save(OUT/'acquisition.json',{'records':records,'complete':False})
            print(target,offset,r['status'],r['iterations'],flush=True)
    candidates={}
    for r in records:
        if r['pair'] is not None: candidates[identifier(r['pair'])]=r['pair']
    control=canonical(json.loads((ROOT/'results/spectral_join/p7_metadata.json').read_text())['pair'])
    chosen=[{'id':'control','sha256':identifier(control),'pair':control,'selection':'previous empty control'}]
    for target in PATTERNS:
        matches=sorted((key,pair) for key,pair in candidates.items()
                       if tuple(sum(abs(v)==1 for v in row) for row in pair)==target and pair!=control)
        if matches:
            key,pair=matches[0]; chosen.append({'id':f'a{target[0]}_{target[1]}','sha256':key,'pair':pair,
                                             'selection':'minimum pair SHA256 among fixed-seed successes in stratum'})
    for r in chosen:
        r['active_counts']=[sum(abs(v)==1 for v in row) for row in r['pair']]
        r['row_domains']=[3**(k-1) for k in r['active_counts']]
    save(OUT/'acquisition.json',{'records':records,'complete':True,'elapsed_seconds':time.perf_counter()-start,
         'source_sha256':digest(Path(__file__)),'patterns':PATTERNS,'seeds_per_pattern':4,
         'bias':'Fixed-seed targeted annealing successes, not all classes or a random sample; wall guard may censor acquisition.'})
    save(OUT/'portfolio.json',{'branches':chosen,'rule':'one minimum-SHA class per acquired ordered active pattern plus prior control; fixed before lift pilot',
         'absent_patterns':[p for p in PATTERNS if list(p) not in [r['active_counts'] for r in chosen]],
         'distinct_translation_classes':len({r['sha256'] for r in chosen}),
         'symmetry':'Ordered rows, independent shifts by 7 canonicalized; binary anchor-zero gauge, ordered lift multiplier 9.',
         'selection_before_lift_search':True,'source_sha256':digest(Path(__file__))})
    print([(r['id'],r['active_counts']) for r in chosen],flush=True)


def branches(): return json.loads((OUT/'portfolio.json').read_text())['branches']


def provenance():
    original=json.loads((ROOT/'results/spectral_join/pilot.json').read_text())
    for key,path in (('native_sha256',NATIVE),('implementation_sha256',ROOT/'src/spectral_join.cpp'),
                     ('wrapper_sha256',ROOT/'src/spectral_join.py')): assert original[key]==digest(path)
    return {'script_sha256':digest(Path(__file__)),'native_sha256':digest(NATIVE),
            'portfolio_sha256':digest(OUT/'portfolio.json'),'python':platform.python_version(),
            'platform':platform.platform(),'compiler_sha256':digest(COMPILER),'flags':FLAGS}


def pilot():
    start=time.perf_counter(); coefficients(63); rows=[]
    for branch in branches():
        for mode in (0,1,2):
            r=search(*branch['pair'],OUT/'pilot'/f"{branch['id']}_m{mode}.json",mode=mode,
                     probe=True,node_limit=400_000,seconds=10)
            estimate=10*sum(1.5*s['expected']*s['elapsed_seconds']/max(1,s['nodes']) for s in r['rows'])
            rows.append({'id':branch['id'],'mode':mode,'estimate_seconds_10x':estimate})
    # Worst supported balanced table: 2^24 allocated entries (40 bytes) plus heads,
    # with an additional doubling allowance for vector reallocation and wrappers.
    maximum=min(max(min(b['row_domains']) for b in branches()),15_000_000)
    capacity=1<<(maximum-1).bit_length(); memory=2*(40*capacity+4*capacity)+200_000_000
    record={'elapsed_seconds':time.perf_counter()-start,'estimates':rows,'timing_margin':10,
            'memory_envelope_bytes':memory,'estimated_storage_bytes':30_000_000,
            'seconds_per_trial':80,'table_cap':15_000_000,'node_cap':2_000_000_000,'solution_cap':100_000,
            'max_trial_batch_seconds':1500,'workers':1,'limits':{'cores':4,'seconds':1800,'bytes':10_000_000_000},
            'limitation':'Early-prefix probes, empirical timing estimates; full-domain memory bound includes table capacity/reallocation, not a whole-system measurement.',
            **provenance()}
    assert memory<8_000_000_000
    save(OUT/'pilot.json',record); print(json.dumps(record,indent=2),flush=True)


def trial(number):
    p=json.loads((OUT/'pilot.json').read_text()); assert p['script_sha256']==digest(Path(__file__))
    assert p['portfolio_sha256']==digest(OUT/'portfolio.json'); assert p['memory_envelope_bytes']<8_000_000_000
    assert number in (0,1,2); warm_start=time.perf_counter(); coefficients(63)
    warm_seconds=time.perf_counter()-warm_start # setup outside timed engines
    jobs=[(b,m) for b in branches() for m in (0,1,2)]
    random.Random(20261006+number).shuffle(jobs); start=time.perf_counter(); records=[]
    for b,m in jobs:
        if time.perf_counter()-start+95>1500: break
        r=timed_search(b['pair'],OUT/'trials'/f"{b['id']}_m{m}_t{number}.json",m,p)
        records.append({'id':b['id'],'mode':m,'result':r})
        print(number,b['id'],m,r['complete'],r['elapsed_seconds'],r['ordered_pairs'],flush=True)
    save(OUT/f'trial_{number}.json',{'trial':number,'seed':20261006+number,'scheduled':len(jobs),
         'completed_jobs':len(records),'elapsed_seconds':time.perf_counter()-start,'workers':1,
         'records':records,'coefficient_warmup_seconds':warm_seconds,
         'order':[(b['id'],m) for b,m in jobs],**provenance()})


def verify_masks(pair,masks):
    rows=[tuple(1-2*((m>>i)&1) for i in range(63)) for m in masks]
    assert check_legendre_pair(*rows).ok and check_negative_support_sds(*rows).ok
    assert [compress(row,21) for row in rows]==[tuple(row) for row in pair]
    for side,row in enumerate(pair):
        anchor=next(i for i,c in enumerate(row) if abs(c)==1)
        assert rows[side][anchor]!= (1 if row[anchor]>0 else -1)


def timed_search(pair,path,mode,limits):
    """Same frozen native input and exact checks, separately measured phases."""
    start=time.perf_counter(); model=TernaryPhasePBModel(*pair); n=model.compressed_length
    assert n==21 and mode in (0,1,2); data=coefficients(63); path=Path(path); path.parent.mkdir(exist_ok=True)
    lines=[f'{n} {data["scale"]} {len(data["frequencies"])}']
    lines+=[' '.join(map(str,row)) for row in pair]
    lines+=[' '.join(map(str,row)) for key in ('cosine','sine') for row in data[key]]
    lines+=[f'{mode} 0 {limits["seconds_per_trial"]} {limits["node_cap"]} {limits["table_cap"]} {limits["solution_cap"]}']
    inp=path.with_suffix('.input.txt'); inp.write_text('\n'.join(lines)+'\n',encoding='ascii',newline='\n')
    setup=time.perf_counter()-start; command=[str(NATIVE),str(inp),str(path)]; native_start=time.perf_counter()
    run=subprocess.run(command,capture_output=True,text=True,timeout=limits['seconds_per_trial']+15)
    native_wall=time.perf_counter()-native_start
    if run.returncode: raise RuntimeError(run.stderr)
    r=json.loads(path.read_text()); validation_start=time.perf_counter()
    for masks in r['solutions']: verify_masks(pair,masks)
    validation=time.perf_counter()-validation_start
    r.update(command=command,python_setup_seconds=setup,native_process_wall_seconds=native_wall,
             native_nonengine_seconds=native_wall-r['elapsed_seconds'],validation_seconds=validation,
             wrapper_elapsed_seconds=time.perf_counter()-start)
    save(path,r); return r


def independent_pilot():
    coefficients(63); start=time.perf_counter(); estimates=[]
    for b in branches():
        # Independent full-key generation pilot; sorting/streaming cost gets 10x margin.
        r=independent_run(b,'pilot',200_000,10)
        estimate=10*r['elapsed_seconds']*sum(b['row_domains'])/max(1,sum(r['enumerated']))
        memory=4*16*min(b['row_domains'])+200_000_000
        estimates.append({'id':b['id'],'estimated_seconds_10x':estimate,'estimated_memory_bytes':memory})
    save(OUT/'independent_pilot.json',{'estimates':estimates,'elapsed_seconds':time.perf_counter()-start,
          'binary_sha256':digest(EXE),'source_sha256':digest(ROOT/'src/full_paf_audit.cpp'),
          'limitation':'Stored-row prefix, unknown streaming/sorting costs covered empirically, not a proven time bound.',**provenance()})


def independent_run(branch,label,cap,seconds):
    directory=OUT/'independent'; directory.mkdir(exist_ok=True)
    path=directory/f"{branch['id']}_{label}.json"; inp=path.with_suffix('.input.txt')
    inp.write_text('21\n'+'\n'.join(' '.join(map(str,row)) for row in branch['pair'])+'\n',newline='\n')
    command=[str(EXE),str(inp),str(path),str(cap),str(seconds),'full-key']; start=time.perf_counter()
    r=subprocess.run(command,capture_output=True,text=True,timeout=seconds+15)
    if r.returncode: raise RuntimeError(r.stderr)
    value=json.loads(path.read_text()); value.update(command=command,wrapper_elapsed_seconds=time.perf_counter()-start)
    save(path,value); return value


def independent():
    p=json.loads((OUT/'independent_pilot.json').read_text()); start=time.perf_counter(); results=[]
    assert p['binary_sha256']==digest(EXE)
    for b in branches():
        estimate=next(v for v in p['estimates'] if v['id']==b['id'])
        if estimate['estimated_memory_bytes']>8_000_000_000: raise RuntimeError('approval required')
        # Every acquired stratum gets an independent bounded check, including hard cases.
        if time.perf_counter()-start+195>1500: break
        r=independent_run(b,'full',2_000_000_000,180); results.append({'id':b['id'],'result':r})
        print('independent',b['id'],r['complete'],r['ordered_pairs'],r['elapsed_seconds'],flush=True)
    save(OUT/'independent.json',{'results':results,'elapsed_seconds':time.perf_counter()-start,
         'binary_sha256':digest(EXE),'source_sha256':digest(ROOT/'src/full_paf_audit.cpp'),**provenance()})


def audit():
    start=time.perf_counter(); catalog=branches(); summaries=[]; witness_checks=0
    for b in catalog:
        assert identifier(canonical(b['pair']))==b['sha256']
        variants={}; completed=[]
        for mode in (0,1,2):
            values=[]
            for trial_no in range(3):
                r=json.loads((OUT/'trials'/f"{b['id']}_m{mode}_t{trial_no}.json").read_text()); values.append(r)
                if r['complete']:
                    assert r['stop_reason']=='exhausted'; assert r['canonical_pairs']==len(r['solutions'])
                    assert r['ordered_pairs']==9*len(r['solutions']); completed.append(r)
                    for s,expected in zip(r['rows'],b['row_domains']):
                        assert s['complete'] and s['expected']==expected
                        assert s['leaves']+s['excluded_completions']==expected
                        assert s['accepted']+s['full_rejections']==s['leaves']
                else: assert r['canonical_pairs'] is None and r['ordered_pairs'] is None
                assert r['solutions']==sorted(r['solutions']) and len({tuple(v) for v in r['solutions']})==len(r['solutions'])
                for masks in r['solutions']:
                    verify_masks(b['pair'],masks)
                    witness_checks+=1
            variants[str(mode)]={'completed':sum(r['complete'] for r in values),'trials':len(values),
                 'engine_median':median(r['elapsed_seconds'] for r in values),
                 'engine_min':min(r['elapsed_seconds'] for r in values),'engine_max':max(r['elapsed_seconds'] for r in values),
                 'wrapper_median':median(r['wrapper_elapsed_seconds'] for r in values),
                 'setup_median':median(r['python_setup_seconds'] for r in values),
                 'validation_median':median(r['validation_seconds'] for r in values),
                 'native_nonengine_median':median(r['native_nonengine_seconds'] for r in values),
                 'peak_native_bytes':max(r['peak_working_set_bytes'] for r in values),
                 'statuses':Counter(r['stop_reason'] for r in values)}
        if completed:
            assert all(r['solutions']==completed[0]['solutions'] for r in completed)
            complete_masks={tuple(v) for v in completed[0]['solutions']}
            for mode in (0,1,2):
                for t in range(3):
                    r=json.loads((OUT/'trials'/f"{b['id']}_m{mode}_t{t}.json").read_text())
                    assert {tuple(v) for v in r['solutions']}<=complete_masks
        independent=json.loads((OUT/'independent'/f"{b['id']}_full.json").read_text())
        if independent['complete']:
            assert independent['expected']==independent['enumerated']==b['row_domains']
            assert independent['solutions']==completed[0]['solutions'] and independent['ordered_pairs']==completed[0]['ordered_pairs']
        summaries.append({'id':b['id'],'active_counts':b['active_counts'],'methods':variants,
                'status':'exact_completed' if completed else 'unresolved',
                'canonical_pairs':completed[0]['canonical_pairs'] if completed else None,
                'ordered_pairs':completed[0]['ordered_pairs'] if completed else None,
                'solutions':completed[0]['solutions'] if completed else None,
                'independent_complete':independent['complete'],'independent_seconds':independent['elapsed_seconds']})
    save(OUT/'summary.json',{'branches':summaries,'witness_checks_with_repeats':witness_checks,
          'scope':'Frozen deterministic heuristic portfolio only; no census or sampling inference.',**provenance()})
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name not in ('manifest.json','audit.json')]
    files+=[ROOT/p for p in ('scripts/p7_study.py','src/spectral_join.cpp','src/spectral_join.py','src/full_paf_audit.cpp',
                            'scripts/benchmark_ternary_phase.py','src/staged_uncompression.py','src/legendre.py','src/ternary_phase.py')]
    save(OUT/'manifest.json',{'algorithm':'sha256','files':[{'path':p.relative_to(ROOT).as_posix(),
           'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(files)]})
    save(OUT/'audit.json',{'status':'passed','elapsed_seconds':time.perf_counter()-start,
         'branches':len(catalog),'manifest_entries':len(files),'manifest_sha256':digest(OUT/'manifest.json'),
         'completed_branches':sum(r['status']=='exact_completed' for r in summaries),
         'independent_completed':sum(r['independent_complete'] for r in summaries),
         'storage_bytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),
         'limitation':'Input/full-witness/frozen-result/coverage audit, not a formal exhaustion certificate.'})
    print(json.loads((OUT/'audit.json').read_text()),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('stage',choices=('acquire','pilot','trial','independent-pilot','independent','audit'))
    parser.add_argument('--trial',type=int); args=parser.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.stage=='acquire': acquisition()
    elif args.stage=='pilot': pilot()
    elif args.stage=='trial': trial(args.trial)
    elif args.stage=='independent-pilot': independent_pilot()
    elif args.stage=='independent': independent()
    else: audit()


if __name__=='__main__': main()
