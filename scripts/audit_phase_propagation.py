"""Audit frozen propagation results, exact census agreement, and subset labels."""
import json
import time
from pathlib import Path

from scripts.classify_p5_lifts import ROOT,digest,save,symmetry_partition,CATALOG,transfer_masks
from scripts.crosswalk_p5_equivalence import canonical_pair
from src.legendre import check_legendre_pair,check_negative_support_sds


def main():
    start=time.perf_counter(); directory=ROOT/'results/phase_propagation'
    read=lambda name:json.loads((directory/name).read_text())
    metadata=read('metadata.json'); pilot=read('pilot.json'); controls=read('controls.json')
    reference=ROOT/'results/p5_classification/classification.json'
    census=json.loads(reference.read_text()); catalog=json.loads(CATALOG.read_text())
    groups,mappings=symmetry_partition(catalog)
    for record in (metadata,pilot,controls):
        assert record['source_sha256']==digest(ROOT/'src/phase_propagation.py')
        assert record['runner_sha256']==digest(ROOT/'scripts/benchmark_phase_propagation.py')
    assert metadata['complete'] and pilot['all_complete']
    assert metadata['reference_sha256']==pilot['reference_sha256']==digest(reference)
    assert metadata['validation_sha256']==digest(directory/'census_validation.json')
    direct={r:read(f'representatives/branch_{r:04d}.json') for r in groups}
    for rank,r in direct.items():
        p=r['propagation']; expected=census[rank-1]
        assert p['complete'] and p['stop_reason']=='exhausted'
        assert p['ordered_pairs']==expected['ordered_pairs']==r['join_baseline']['ordered_pairs']
        assert r['join_baseline']['complete'] and p['solutions']==expected['solutions']
        assert p['canonical_pairs']==len(p['solutions'])==p['canonical_lower_bound']
    validation=read('census_validation.json'); checked=0
    for expected,result in zip(census,validation,strict=True):
        rank=expected['rank']; mapping=mappings[rank]; entry=catalog[rank-1]
        assert result['rank']==rank and result['status']=='exact_match'
        assert result['ordered_pairs']==expected['ordered_pairs']
        pair=tuple(tuple(entry[k]) for k in ('first','second'))
        masks=sorted(transfer_masks(m,mapping['operation'],pair)
                     for m in direct[mapping['representative_rank']]['propagation']['solutions'])
        assert [list(m) for m in masks]==expected['solutions']
        checked+=len(masks)
    for name,r in controls['results'].items():
        if r['complete']:
            assert r['stop_reason']=='exhausted'
            assert r['ordered_pairs']==9*len(r['solutions'])
            if name.startswith('p5_'):
                rank=int(name.split('_')[1].replace('rank',''))
                assert r['solutions']==census[rank-1]['solutions']
        else:
            assert r['ordered_pairs'] is None and r['canonical_pairs'] is None
            assert r['stop_reason'] in ('time_limit','node_limit','stored_candidate_limit')
        for pair in r['solutions']:
            length=27 if name.startswith('p3_') else 63 if name.startswith('p7_') else 45
            rows=[tuple(1-2*((m >> i)&1) for i in range(length)) for m in pair]
            assert check_legendre_pair(*rows).ok and check_negative_support_sds(*rows).ok
    crosswalk=read('equivalence_crosswalk.json')
    assert crosswalk['script_sha256']==digest(ROOT/'scripts/crosswalk_p5_equivalence.py')
    assert crosswalk['source_sha256']==digest(reference)
    seen=set(); labels=set()
    for group in crosswalk['classes']:
        label=tuple(group['representative_masks']); assert label not in labels; labels.add(label)
        assert group['phase_gauged_members']==len(group['members'])
        assert group['prescribed_ordered_members']==81*len(group['members'])
        for member in group['members']:
            key=(member['rank'],tuple(member['masks'])); assert key not in seen; seen.add(key)
            assert canonical_pair(key[1],45)==label
    assert seen=={(r['rank'],tuple(m)) for r in census for m in r['solutions']}
    assert len(labels)==crosswalk['class_count']==63 and checked==2976
    files=list(directory.glob('*.json'))+list((directory/'pilot').glob('*.json'))+list((directory/'representatives').glob('*.json'))
    files=[p for p in files if p.name not in ('audit.json','manifest.json')]
    files += [ROOT/p for p in ('src/phase_propagation.py','scripts/benchmark_phase_propagation.py',
                              'scripts/crosswalk_p5_equivalence.py','scripts/audit_phase_propagation.py',
                              'tests/test_phase_propagation.py','tests/test_p5_equivalence.py',
                              'src/ternary_phase.py','src/legendre.py','scripts/classify_p5_lifts.py')]
    files += [reference,CATALOG]
    save(directory/'manifest.json',{'algorithm':'sha256','files':[
        {'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(files)]})
    save(directory/'audit.json',{'status':'passed','branches':1164,'direct_cases':79,
                                'canonical_solutions':checked,'equivalence_classes':len(labels),
                                'elapsed_seconds':time.perf_counter()-start,
                                'manifest_sha256':digest(directory/'manifest.json'),
                                'limitation':'Frozen-result consistency audit; fresh exhaustion is the pilot/full command, not this audit.'})
    print(read('audit.json'))


if __name__=='__main__': main()
