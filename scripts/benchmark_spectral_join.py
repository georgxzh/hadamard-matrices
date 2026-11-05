"""Gated direct p=5 validation, isolated controls, and saved-branch p=7 search."""
import argparse
import json
import platform
import random
import subprocess
import time
from collections import Counter,defaultdict
from concurrent.futures import ProcessPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
from statistics import median

from scripts.classify_p5_lifts import ROOT,CATALOG,digest,save,peak_memory
from scripts.benchmark_staged_uncompression import _known_pair
from src.legendre import compress
from src.spectral_join import build_native,coefficients,search,NATIVE,COMPILER,FLAGS
from src.ternary_phase import search_phase_uncompressions

OUTPUT=ROOT/'results/spectral_join'
REFERENCE=ROOT/'results/p5_classification/classification.json'


def provenance():
    return {'implementation_sha256':digest(ROOT/'src/spectral_join.cpp'),
            'wrapper_sha256':digest(ROOT/'src/spectral_join.py'),
            'runner_sha256':digest(Path(__file__)), 'native_sha256':digest(NATIVE),
            'reference_sha256':digest(REFERENCE),'catalog_sha256':digest(CATALOG)}


def verify_provenance(record):
    for key,value in provenance().items(): assert record[key]==value,key


def p7_pair():
    return json.loads((ROOT/'results/ternary_phase/metadata.json').read_text())['branch_acquisition'][0]['pair']


def case(entry,directory,modes=(0,2)):
    start=time.perf_counter(); records={}
    expected=json.loads(REFERENCE.read_text())[entry['rank']-1]
    for mode in modes:
        r=search(entry['first'],entry['second'],Path(directory)/f"rank_{entry['rank']:04d}_mode{mode}.json",mode=mode)
        assert r['complete'] and r['ordered_pairs']==expected['ordered_pairs']
        assert r['solutions']==expected['solutions']
        records[str(mode)]=r
    return {'rank':entry['rank'],'split':sorted(entry['magnitude_one_counts']),
            'elapsed_seconds':time.perf_counter()-start,'methods':records,
            'python_peak_bytes':peak_memory()}


def pilot(workers):
    start=time.perf_counter(); command=build_native(); catalog=json.loads(CATALOG.read_text())
    strata=defaultdict(list)
    for r in catalog: strata[tuple(sorted(r['magnitude_one_counts']))].append(r['rank'])
    selected={1,3,771,1133}
    for ranks in strata.values(): selected.update((ranks[0],ranks[len(ranks)//2],ranks[-1]))
    records=[]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for f in as_completed([pool.submit(case,catalog[r-1],OUTPUT/'pilot',(0,1,2)) for r in sorted(selected)]):
            r=f.result(); records.append(r); save(OUTPUT/'pilot'/f"case_{r['rank']:04d}.json",r)
            print(f"pilot p5 rank {r['rank']}: {r['elapsed_seconds']:.3f}s",flush=True)
    # Whole-wrapper measurements include Python validation, I/O, and startup.
    estimate=2*sum(len(ranks)*max(r['elapsed_seconds'] for r in records if tuple(r['split'])==split)
                   for split,ranks in strata.items())/workers
    probes={}
    for mode in range(3):
        r=search(*p7_pair(),OUTPUT/'pilot'/f'p7_probe_mode{mode}.json',mode=mode,probe=True,node_limit=200_000,seconds=10)
        probes[str(mode)]=r
    # Bound work by the unpruned tree; apply 10x timing margin for table costs
    # and different prefixes. This remains an empirical estimate, not a bound.
    p7_estimate=max(sum(1.5*row['expected']*row['elapsed_seconds']/max(1,row['nodes']) for row in r['rows'])
                    for r in probes.values())*10
    memory=2*workers*max(r['python_peak_bytes']+v['peak_working_set_bytes']
                        for r in records for v in r['methods'].values())
    result={'completed_utc':datetime.now(timezone.utc).isoformat(),'workers':workers,
            'elapsed_seconds':time.perf_counter()-start,'selected_ranks':sorted(selected),
            'estimated_p5_full_seconds_with_margin':estimate,
            'estimated_p5_worker_memory_bytes_with_margin':memory,
            'estimated_p7_seconds_per_method_with_margin':p7_estimate,
            'p7_memory_envelope_bytes':1_200_000_000,'estimated_storage_bytes':20_000_000,
            'build_command':command,'compiler_sha256':digest(COMPILER),
            'compiler_version':subprocess.run([str(COMPILER),'--version'],capture_output=True,text=True).stdout.splitlines()[0],
            'python':platform.python_version(),'platform':platform.platform(),**provenance(),
            'limits':{'cores':4,'seconds_per_run':1800,'bytes':10_000_000_000},
            'p7_estimate_limitation':'Deterministic early-prefix probes, no random sampling; includes a 10x margin but does not prove future runtime.'}
    save(OUTPUT/'pilot.json',result)
    for length in (27,45,63): save(OUTPUT/f'coefficients_{length}.json',coefficients(length))
    print(json.dumps(result,indent=2),flush=True)


def full(workers):
    pilot=json.loads((OUTPUT/'pilot.json').read_text()); verify_provenance(pilot)
    estimate=pilot['estimated_p5_full_seconds_with_margin']*pilot['workers']/workers
    memory=pilot['estimated_p5_worker_memory_bytes_with_margin']*workers/pilot['workers']
    if estimate>1400 or memory>8_000_000_000: raise RuntimeError('resource gate requires approval')
    start=time.perf_counter(); catalog=json.loads(CATALOG.read_text()); records={}
    for r in pilot['selected_ranks']:
        records[r]=json.loads((OUTPUT/'pilot'/f'case_{r:04d}.json').read_text())
    with ProcessPoolExecutor(max_workers=workers) as pool:
        jobs=[pool.submit(case,e,OUTPUT/'branches') for e in catalog if e['rank'] not in records]
        try:
            for future in as_completed(jobs,timeout=1450):
                r=future.result(); records[r['rank']]=r
                if len(records)%100==0: print(f'p5 complete {len(records)}/1164',flush=True)
        except TimeoutError:
            for future in jobs: future.cancel()
            save(OUTPUT/'incomplete_full.json',{'complete':False,'status':'unresolved',
                 'completed_ranks':sorted(records),'elapsed_seconds':time.perf_counter()-start,**provenance()})
            return
    # No symmetry reuse: directly enumerate each catalogue branch in both modes.
    ordered=[records[r] for r in range(1,1165)]
    save(OUTPUT/'census_validation.json',[{'rank':r['rank'],'status':'exact_match',
            'canonical_pairs':r['methods']['2']['canonical_pairs'],'ordered_pairs':r['methods']['2']['ordered_pairs'],
            'baseline_solutions_match':r['methods']['0']['solutions']==r['methods']['2']['solutions']} for r in ordered])
    result={'complete':True,'direct_cases':1164,'elapsed_seconds':time.perf_counter()-start,'workers':workers,
            'pilot_cases_reused':len(pilot['selected_ranks']),
            'ordered_pair_histogram':dict(Counter(r['methods']['2']['ordered_pairs'] for r in ordered)),
            'canonical_pairs':sum(r['methods']['2']['canonical_pairs'] for r in ordered),
            'engine_seconds_sum':{str(m):sum(r['methods'][str(m)]['elapsed_seconds'] for r in ordered) for m in (0,2)},
            'peak_worker_bytes':max(v['peak_working_set_bytes'] for r in ordered for v in r['methods'].values()),
            'python_plus_native_worker_bound_bytes':workers*max(r['python_peak_bytes']+v['peak_working_set_bytes']
                                         for r in ordered for v in r['methods'].values()),
            'validation_sha256':digest(OUTPUT/'census_validation.json'),**provenance(),
            'limitation':'Native baseline and spectral search share binary-mask PAF code; independent frozen census additionally uses phase enumeration.'}
    save(OUTPUT/'metadata.json',result); print(json.dumps(result,indent=2),flush=True)


def controls():
    start=time.perf_counter(); catalog=json.loads(CATALOG.read_text()); records={}
    cases={'p3':tuple(compress(x,9) for x in _known_pair(3))}
    cases.update({f'p5_rank{r}':(catalog[r-1]['first'],catalog[r-1]['second']) for r in (1,3,1133)})
    for length in (27,45): coefficients(length)
    jobs=[(name,mode,trial) for name in cases for mode in ('python',0,1,2) for trial in range(3)]
    random.Random(20261004).shuffle(jobs)
    for name,mode,trial in jobs:
        if time.perf_counter()-start>1400:
            save(OUTPUT/'incomplete_controls.json',{'status':'unresolved','records':records,**provenance()})
            return
        pair=cases[name]; key=f'{name}_mode{mode}_trial{trial}'
        if mode=='python':
            r=vars(search_phase_uncompressions(*pair,time_limit=60,max_candidates_per_side=2_000_000,
                                               max_stored_signatures=250_000,collect=1))
        else: r=search(*pair,OUTPUT/'controls'/f'{key}.json',mode=mode)
        assert r['complete'] and r['ordered_pairs']==({'p3':135,'p5_rank1':27,'p5_rank3':0,'p5_rank1133':54}[name])
        records[key]=r; print(f'{key}: {r["elapsed_seconds"]:.4f}s',flush=True)
    summary={}
    for name in cases:
        for mode in ('python',0,1,2):
            values=[records[f'{name}_mode{mode}_trial{t}']['elapsed_seconds'] for t in range(3)]
            summary[f'{name}_mode{mode}']={'median_seconds':median(values),'min_seconds':min(values),'max_seconds':max(values)}
    save(OUTPUT/'controls.json',{'elapsed_seconds':time.perf_counter()-start,'workers':1,'seed':20261004,
            'records':records,'summary':summary,**provenance(),
            'limitation':'Three shuffled timing replicates of deterministic searches. Native engine time excludes process startup/setup; wrapper time is separately recorded. Python vs native confounds implementation and traversal; native mode ablation isolates spectral pruning.'})


def p7():
    pilot=json.loads((OUTPUT/'pilot.json').read_text()); verify_provenance(pilot)
    assert json.loads((OUTPUT/'metadata.json').read_text())['complete']
    estimate=pilot['estimated_p7_seconds_per_method_with_margin']
    # Each method is a separate bounded run, one process. Even if the estimate
    # is optimistic, no internal search exceeds 25 minutes.
    if estimate>1400: raise RuntimeError('pilot requires approval or a smaller experiment')
    results={}; pair=p7_pair()
    for mode in (2,1,0):
        r=search(*pair,OUTPUT/f'p7_mode{mode}.json',mode=mode,seconds=min(450,max(120,3*estimate)))
        results[str(mode)]=r
        print(f'p7 mode {mode}: {r["complete"]} {r["stop_reason"]}, {r["elapsed_seconds"]:.3f}s, {r["ordered_pairs"]} pairs',flush=True)
    completed=[r for r in results.values() if r['complete']]
    if completed:
        assert all(r['solutions']==completed[0]['solutions'] for r in completed)
        for r in results.values(): assert all(m in completed[0]['solutions'] for m in r['solutions'])
    save(OUTPUT/'p7_metadata.json',{'pair':pair,'results':results,'estimate_seconds_per_method':estimate,
                'workers':1,'branch_source_sha256':digest(ROOT/'results/ternary_phase/metadata.json'),**provenance(),
                'status':'exact_completed' if completed else 'unresolved',
                'completed_utc':datetime.now(timezone.utc).isoformat(),
                'limitation':'One saved intermediate branch only; completion does not classify all length-63 pairs.'})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('pilot','full','controls','p7'))
    parser.add_argument('--workers',type=int,default=3); args=parser.parse_args()
    if not 1<=args.workers<=4: raise ValueError('one to four workers')
    if args.mode=='pilot': pilot(args.workers)
    elif args.mode=='full': full(args.workers)
    elif args.mode=='controls': controls()
    else: p7()


if __name__=='__main__': main()
