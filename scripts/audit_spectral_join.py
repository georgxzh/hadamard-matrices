"""Audit exact coverage, all census solutions, coefficients, and p=7 result."""
import json
import time
from pathlib import Path

from scripts.classify_p5_lifts import ROOT,CATALOG,digest,save
from scripts.benchmark_spectral_join import OUTPUT,REFERENCE,verify_provenance
from src.spectral_join import coefficients
from src.legendre import check_legendre_pair,check_negative_support_sds,compress


def check_result(result,pair):
    n=len(pair[0]); length=3*n
    if result['complete']:
        assert result['stop_reason']=='exhausted'
        assert result['canonical_pairs']==result['canonical_lower_bound']==len(result['solutions'])
        assert result['ordered_pairs']==9*len(result['solutions'])
        for row in result['rows']:
            assert row['complete'] and row['leaves']+row['excluded_completions']==row['expected']
            assert row['accepted']+row['full_rejections']==row['leaves']
    else:
        assert result['canonical_pairs'] is None and result['ordered_pairs'] is None
    for side,row in enumerate(result['rows']):
        if row['expected']:
            assert row['expected']==3**(sum(abs(v)==1 for v in pair[side])-1)
    for masks in result['solutions']:
        rows=[tuple(1-2*((m>>i)&1) for i in range(length)) for m in masks]
        assert check_legendre_pair(*rows).ok and check_negative_support_sds(*rows).ok
        assert tuple(compress(rows[0],n))==tuple(pair[0]) and tuple(compress(rows[1],n))==tuple(pair[1])


def main():
    start=time.perf_counter(); read=lambda name:json.loads((OUTPUT/name).read_text())
    pilot=read('pilot.json'); metadata=read('metadata.json'); controls=read('controls.json'); p7=read('p7_metadata.json')
    for record in (pilot,metadata,controls,p7): verify_provenance(record)
    for length in (27,45,63): assert read(f'coefficients_{length}.json')==coefficients(length)
    assert metadata['complete'] and metadata['direct_cases']==1164
    reference=json.loads(REFERENCE.read_text()); catalog=json.loads(CATALOG.read_text()); checked=0
    for entry,expected in zip(catalog,reference,strict=True):
        rank=entry['rank']; pair=(entry['first'],entry['second'])
        folder='pilot' if rank in pilot['selected_ranks'] else 'branches'
        for mode in (0,2):
            r=read(f'{folder}/rank_{rank:04d}_mode{mode}.json'); check_result(r,pair)
            assert r['complete'] and r['solutions']==expected['solutions']
            assert r['ordered_pairs']==expected['ordered_pairs']
        checked+=len(expected['solutions'])
    assert checked==2976
    for name,r in controls['records'].items():
        if '_modepython_' in name: assert r['complete']; continue
        if name.startswith('p5_'):
            rank=int(name.split('_')[1].removeprefix('rank')); e=catalog[rank-1]
            check_result(r,(e['first'],e['second'])); assert r['solutions']==reference[rank-1]['solutions']
    for mode,r in p7['results'].items():
        check_result(r,p7['pair']); assert r['complete'] and r['canonical_pairs']==0
    assert p7['results']['1']['rows'][0]['accepted']==p7['results']['2']['rows'][0]['accepted']==38907
    assert p7['results']['1']['rows'][1]['accepted']==p7['results']['2']['rows'][1]['accepted']==28134
    independent=read('independent_audit.json'); full=read('full_paf_p7.json')
    assert independent['status']=='passed' and full['complete'] and full['ordered_pairs']==0
    assert full['enumerated']==full['expected']==[4782969,43046721]
    assert independent['source_sha256']==digest(ROOT/'src/full_paf_audit.cpp')
    assert independent['script_sha256']==digest(ROOT/'scripts/audit_saved_p7.py')
    assert independent['result_sha256']==digest(OUTPUT/'full_paf_p7.json')
    assert independent['controls']==[27,0]
    files=[p for p in OUTPUT.rglob('*') if p.is_file() and p.name not in ('manifest.json','audit.json')]
    files += [ROOT/p for p in ('src/spectral_join.cpp','src/spectral_join.py','src/full_paf_audit.cpp',
                'scripts/benchmark_spectral_join.py','scripts/audit_saved_p7.py','scripts/audit_spectral_join.py',
                'tests/test_spectral_join.py','src/ternary_phase.py','src/legendre.py','.gitattributes')]
    files += [REFERENCE,CATALOG]
    save(OUTPUT/'manifest.json',{'algorithm':'sha256','files':[
         {'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(files)]})
    save(OUTPUT/'audit.json',{'status':'passed','p5_branches':1164,'p5_canonical_pairs':checked,
           'p7_ordered_pairs':0,'independent_p7_result':'exhausted_full_PAF_no_lifts',
           'elapsed_seconds':time.perf_counter()-start,'manifest_entries':len(files),
           'manifest_sha256':digest(OUTPUT/'manifest.json'),
           'limitation':'Frozen evidence consistency and exact witness checks, not a new enumeration or formal proof certificate.'})
    print(read('audit.json'))


if __name__=='__main__': main()
