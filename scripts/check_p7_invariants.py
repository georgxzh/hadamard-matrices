"""Additional frozen protocol, selection, survivor-count and resource checks."""
import json
import random
from pathlib import Path
from scripts.p7_study import (OUT,ROOT,PATTERNS,branches,canonical,identifier,digest,save)


def main():
    read=lambda name:json.loads((OUT/name).read_text())
    selected=branches(); acquisition=read('acquisition.json'); source=digest(ROOT/'scripts/p7_study.py')
    assert acquisition['source_sha256']==read('portfolio.json')['source_sha256']==source
    assert len(selected)==len({b['sha256'] for b in selected})==4
    pool={identifier(canonical(r['pair'])):canonical(r['pair']) for r in acquisition['records'] if r['pair'] is not None}
    for b in selected:
        assert b['pair']==[list(r) for r in canonical(b['pair'])]
        assert identifier(b['pair'])==b['sha256']
        if b['id']=='control':
            assert b['pair']==json.loads((ROOT/'results/spectral_join/p7_metadata.json').read_text())['pair']
        else:
            eligible=[key for key,pair in pool.items() if [sum(abs(v)==1 for v in row) for row in pair]==b['active_counts']]
            assert b['sha256']==min(eligible)
    compared=0; peaks=[]; engine_caps=0
    for t in range(3):
        trial=read(f'trial_{t}.json'); assert trial['script_sha256']==source
        assert trial['seed']==20261006+t and trial['elapsed_seconds']<1500 and trial['workers']==1
        expected=[(b['id'],mode) for b in selected for mode in (0,1,2)]
        random.Random(20261006+t).shuffle(expected)
        assert trial['order']==[list(job) for job in expected]
        assert trial['completed_jobs']==trial['scheduled']==len(trial['records'])==12
        assert trial['portfolio_sha256']==digest(OUT/'portfolio.json')
        for aggregate in trial['records']:
            r=read(f"trials/{aggregate['id']}_m{aggregate['mode']}_t{t}.json")
            assert r==aggregate['result']
            assert r['seconds_limit']==80 and r['elapsed_seconds']<81 and r['wrapper_elapsed_seconds']<1800
            assert r['node_limit']==2_000_000_000 and r['stored_candidate_limit']==15_000_000
            peaks.append(r['peak_working_set_bytes']); engine_caps+=not r['complete']
    for b in selected:
        variants={m:[read(f"trials/{b['id']}_m{m}_t{t}.json") for t in range(3)] for m in (0,1,2)}
        for m,records in variants.items():
            assert all(r['complete'] for r in records)
            projection=lambda r:[{k:v for k,v in row.items() if k!='elapsed_seconds'} for row in r['rows']]
            assert all(projection(r)==projection(records[0]) for r in records)
        off,leaf,prefix=[variants[m][0] for m in (0,1,2)]
        for i in (0,1):
            assert off['rows'][i]['accepted']==off['rows'][i]['leaves']==b['row_domains'][i]
            assert leaf['rows'][i]['accepted']==prefix['rows'][i]['accepted']
            assert prefix['rows'][i]['nodes']<=leaf['rows'][i]['nodes']
        compared+=1
    for path in (OUT/'pilot').glob('*.json'):
        r=json.loads(path.read_text())
        if not r['complete']: assert r['canonical_pairs'] is None and r['ordered_pairs'] is None
    independent=read('independent.json'); assert independent['elapsed_seconds']<1500
    estimates=read('independent_pilot.json')['estimates']
    assert max(v['estimated_memory_bytes'] for v in estimates)<8_000_000_000
    assert max(peaks)<read('pilot.json')['memory_envelope_bytes']<8_000_000_000
    storage=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()); assert storage<1_000_000_000
    save(OUT/'invariants.json',{'status':'passed','classes_checked':compared,'trials_checked':36,
        'survivor_counts_leaf_prefix_equal':True,'deterministic_row_counters':True,
        'selection_reproduced':True,'native_trial_stops':engine_caps,'native_peak_bytes':max(peaks),
        'storage_bytes_before_final_manifests':storage,'source_sha256':digest(Path(__file__)),
        'limits':'One worker; measured batch times <1500 seconds; native memory within pilot envelope; evidence <1GB.'})
    print(read('invariants.json'))


if __name__=='__main__': main()
