"""Repeat the join factorial without concurrent repository computations.

Retains the earlier benchmark records; produces a separate timing artifact.
One process, 24 trials, each capped at 60 seconds (under 30 minutes total).
"""
import json
import platform
import random
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

from scripts.benchmark_phase_controls import join_control, OUTPUT
from scripts.classify_p5_lifts import CATALOG, ROOT, save, digest, peak_memory


def main():
    started=time.perf_counter()
    catalog=json.loads(CATALOG.read_text())
    branches={f'p5_rank{rank}':tuple(tuple(catalog[rank-1][k]) for k in ('first','second')) for rank in (1,3)}
    rng=random.Random(20260930); records=[]
    for repetition in range(3):
        jobs=[(name,c,i) for name in branches for c in (False,True) for i in (False,True)]
        rng.shuffle(jobs)
        for name,canonical,incremental in jobs:
            result=join_control(branches[name],canonical,incremental)
            assert result['ordered_pairs']==(27 if name=='p5_rank1' else 0)
            records.append({'branch':name,'repeat':repetition,**result})
            print(f'{name} canonical={canonical} incremental={incremental}: {result["seconds"]:.3f}s',flush=True)
    for name in branches:
        for canonical in (False,True):
            assert len({tuple(r['ordered_stream_sha256']) for r in records if r['branch']==name and r['canonical']==canonical})==1
    summary={f'{name}_canonical{int(c)}_incremental{int(i)}':{
        'median_seconds':statistics.median(values),'min_seconds':min(values),'max_seconds':max(values)}
        for name in branches for c in (False,True) for i in (False,True)
        for values in [[r['seconds'] for r in records if r['branch']==name and r['canonical']==c and r['incremental']==i]]}
    result={'completed_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-started,
            'workers':1,'repeats':3,'python':platform.python_version(),'platform':platform.platform(),
            'source_sha256':digest(Path(__file__)),
            'implementation_sha256':digest(ROOT/'scripts/benchmark_phase_controls.py'),
            'peak_working_set_bytes':peak_memory(),'results':records,'summary':summary,
            'timing_scope':'No other repository experiment was run concurrently. OS/background load and CPU frequency were not controlled.',
            'earlier_run':'metadata.json retains preliminary factorial and PB runs; a 13.84s classification audit overlapped part of its solver phase.'}
    save(OUTPUT/'isolated_joins.json',result)
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__': main()
