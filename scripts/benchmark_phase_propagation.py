"""Pilot, gated complete p=5 comparison, and bounded p=7 propagation probes."""
import argparse
import json
import platform
import time
from collections import Counter,defaultdict
from concurrent.futures import ProcessPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path

from scripts.classify_p5_lifts import ROOT,CATALOG,digest,save,peak_memory,symmetry_partition,transfer_masks
from scripts.benchmark_staged_uncompression import _known_pair
from src.legendre import compress,check_legendre_pair,check_negative_support_sds
from src.phase_propagation import PhasePropagationModel,search_conditioned
from src.ternary_phase import search_phase_uncompressions

OUTPUT=ROOT/'results/phase_propagation'
REFERENCE=ROOT/'results/p5_classification/classification.json'


def case(entry,directory):
    pair=(entry['first'],entry['second']); started=time.perf_counter()
    propagated=search_conditioned(*pair,seconds=90)
    baseline=search_phase_uncompressions(*pair,time_limit=30,max_candidates_per_side=2_000_000,
                                        max_stored_signatures=250_000,collect=0)
    expected=json.loads(REFERENCE.read_text())[entry['rank']-1]
    if propagated['complete']:
        assert propagated['ordered_pairs']==expected['ordered_pairs']
        assert [list(m) for m in propagated['solutions']]==expected['solutions']
    else:
        assert all(list(m) in expected['solutions'] for m in propagated['solutions'])
    if baseline.complete: assert baseline.ordered_pairs==expected['ordered_pairs']
    record={'rank':entry['rank'],'split':sorted(entry['magnitude_one_counts']),
            'propagation':propagated,'join_baseline':vars(baseline),
            'matches_reference':propagated['complete'],
            'elapsed_seconds':time.perf_counter()-started,'peak_working_set_bytes':peak_memory()}
    save(Path(directory)/f"branch_{entry['rank']:04d}.json",record)
    return record


def pilot(workers):
    started=time.perf_counter(); catalog=json.loads(CATALOG.read_text())
    groups,_=symmetry_partition(catalog); strata=defaultdict(list)
    for rank in groups: strata[tuple(sorted(catalog[rank-1]['magnitude_one_counts']))].append(rank)
    selected={1,3,771}
    for ranks in strata.values(): selected.update((ranks[0],ranks[len(ranks)//2],ranks[-1]))
    records=[]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for future in as_completed([pool.submit(case,catalog[r-1],OUTPUT/'pilot') for r in sorted(selected)]):
            r=future.result(); records.append(r)
            print(f"pilot {r['rank']}: complete={r['matches_reference']}, {r['elapsed_seconds']:.2f}s",flush=True)
    measured={tuple(r['split']):max(s['elapsed_seconds'] for s in records if s['split']==r['split']) for r in records}
    estimate=1.5*sum(len(ranks)*measured[split] for split,ranks in strata.items())/workers
    metadata={'completed_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-started,
              'workers':workers,'selected_ranks':sorted(selected),'all_complete':all(r['matches_reference'] for r in records),
              'estimated_full_seconds_with_margin':estimate,
              'estimated_peak_worker_memory_bytes_with_margin':1.5*workers*max(r['peak_working_set_bytes'] for r in records),
              'estimated_storage_bytes':10_000_000,'source_sha256':digest(ROOT/'src/phase_propagation.py'),
              'runner_sha256':digest(Path(__file__)),'reference_sha256':digest(REFERENCE),
              'strata':[{'split':split,'representatives':len(ranks),'max_case_seconds':measured[split]} for split,ranks in strata.items()]}
    save(OUTPUT/'pilot.json',metadata); print(json.dumps(metadata,indent=2),flush=True)


def full(workers):
    catalog=json.loads(CATALOG.read_text()); pilot_data=json.loads((OUTPUT/'pilot.json').read_text())
    assert pilot_data['all_complete'] and pilot_data['source_sha256']==digest(ROOT/'src/phase_propagation.py')
    assert pilot_data['reference_sha256']==digest(REFERENCE)
    estimate=pilot_data['estimated_full_seconds_with_margin']*pilot_data['workers']/workers
    memory=pilot_data['estimated_peak_worker_memory_bytes_with_margin']*workers/pilot_data['workers']
    if estimate>1450 or memory>8_000_000_000:
        raise RuntimeError('estimated run exceeds conservative resource envelope; approval required')
    print(f'Resource gate: {estimate:.1f}s, {memory/1e6:.1f}MB, {workers} workers',flush=True)
    groups,mappings=symmetry_partition(catalog); started=time.perf_counter(); records={}
    for rank in groups:
        path=OUTPUT/'pilot'/f'branch_{rank:04d}.json'
        if path.exists(): records[rank]=json.loads(path.read_text())
    with ProcessPoolExecutor(max_workers=workers) as pool:
        jobs=[pool.submit(case,catalog[rank-1],OUTPUT/'representatives') for rank in groups if rank not in records]
        try:
            for future in as_completed(jobs,timeout=1490):
                record=future.result(); records[record['rank']]=record
                print(f"branch {record['rank']}: {record['matches_reference']}; {len(records)}/79",flush=True)
        except TimeoutError:
            for future in jobs: future.cancel()
    for rank,record in records.items(): save(OUTPUT/'representatives'/f'branch_{rank:04d}.json',record)
    reference=json.loads(REFERENCE.read_text()); validation=[]
    for entry in catalog:
        rank=entry['rank']; mapping=mappings[rank]; direct=records.get(mapping['representative_rank'])
        result={'rank':rank,'representative_rank':mapping['representative_rank'],'status':'unresolved'}
        if direct and direct['propagation']['complete']:
            pair=tuple(tuple(entry[k]) for k in ('first','second'))
            solutions=sorted(transfer_masks(m,mapping['operation'],pair) for m in direct['propagation']['solutions'])
            assert [list(m) for m in solutions]==reference[rank-1]['solutions']
            result.update(status='exact_match',ordered_pairs=9*len(solutions),canonical_pairs=len(solutions))
        validation.append(result)
    save(OUTPUT/'census_validation.json',validation)
    complete=all(r['status']=='exact_match' for r in validation)
    metadata={'complete':complete,'completed_utc':datetime.now(timezone.utc).isoformat(),
              'elapsed_seconds':time.perf_counter()-started,'workers':workers,
              'status_counts':dict(Counter(r['status'] for r in validation)),
              'source_sha256':digest(ROOT/'src/phase_propagation.py'),'runner_sha256':digest(Path(__file__)),
              'reference_sha256':digest(REFERENCE),'validation_sha256':digest(OUTPUT/'census_validation.json'),
              'ordered_pair_histogram':dict(Counter(r['ordered_pairs'] for r in validation if r['status']=='exact_match')),
              'direct_cases':len(records),'direct_propagation_seconds_sum':sum(r['propagation']['elapsed_seconds'] for r in records.values()),
              'direct_join_seconds_sum':sum(r['join_baseline']['elapsed_seconds'] for r in records.values()),
              'peak_worker_bytes':max(r['peak_working_set_bytes'] for r in records.values()),
              'python':platform.python_version(),'platform':platform.platform(),
              'limitation':'79 direct re-enumerations plus proved bijections cover 1164 orbits; both methods share PhaseRow formula, census binary enumerator is independent.'}
    save(OUTPUT/'metadata.json',metadata); print(json.dumps(metadata,indent=2),flush=True)


def controls():
    started=time.perf_counter(); catalog=json.loads(CATALOG.read_text())
    p3=tuple(compress(row,9) for row in _known_pair(3))
    data=json.loads((ROOT/'results/ternary_phase/metadata.json').read_text())
    p7=tuple(tuple(row) for row in data['branch_acquisition'][0]['pair'])
    records={}
    for name,pair in [('p3',p3),('p5_rank1',(catalog[0]['first'],catalog[0]['second'])),
                      ('p5_rank3',(catalog[2]['first'],catalog[2]['second']))]:
        for mode in ('anchor','all'):
            result=PhasePropagationModel(*pair,cycle_mode=mode).search(seconds=10)
            records[f'{name}_difference_{mode}']=result
            print(f'{name} differences {mode}: {result["stop_reason"]}',flush=True)
        for filtering,folded in ((False,False),(False,True),(True,False),(True,True)):
            result=search_conditioned(*pair,seconds=60,partner_filter=filtering,folded_bounds=folded)
            if result['complete']: assert result['ordered_pairs']==(135 if name=='p3' else 27 if name=='p5_rank1' else 0)
            records[f'{name}_conditioned_filter{int(filtering)}_fold{int(folded)}']=result
            print(f'{name} conditioned {filtering}/{folded}: {result["stop_reason"]} {result["elapsed_seconds"]:.2f}s',flush=True)
    # Both p=7 probes stay within small, explicit time/storage budgets.
    records['p7_difference_all']=PhasePropagationModel(*p7).search(seconds=30)
    records['p7_conditioned']=search_conditioned(*p7,seconds=30,max_stored_candidates=250_000)
    metadata={'completed_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-started,
              'workers':1,'results':records,'source_sha256':digest(ROOT/'src/phase_propagation.py'),
              'runner_sha256':digest(Path(__file__)),'peak_working_set_bytes':peak_memory(),
              'limitations':'Single-trial mechanism ablations, no distributional speed claim. p7 caps cannot establish nonexistence.'}
    save(OUTPUT/'controls.json',metadata)
    print({k:(v['complete'],v['stop_reason'],v['elapsed_seconds']) for k,v in records.items()},flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('pilot','full','controls'))
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args()
    if not 1<=args.workers<=4: raise ValueError('one to four workers')
    if args.mode=='pilot': pilot(args.workers)
    elif args.mode=='full': full(args.workers)
    else: controls()


if __name__=='__main__': main()
