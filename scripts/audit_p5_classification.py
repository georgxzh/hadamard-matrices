"""Read-only exact audit, with a small hashed report written after success.

Regenerates the intermediate catalogue; checks all representative evidence;
independently inverts every recorded lift permutation; expands all translations
and checks uniqueness. Does not trust a timeout or status string as exhaustion.
"""
from __future__ import annotations

import csv
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from scripts.classify_p5_lifts import ROOT, CATALOG, OUTPUT, digest, save, binary, peak_memory
from src.legendre import (compress, check_legendre_pair, check_negative_support_sds,
                          structured_compressed_pair, published_structured_legendre_pair_45)
from src.staged_uncompression import enumerate_intermediate_pairs


def canonical_mask(row, compressed):
    n = len(compressed)
    anchor = next(i for i,c in enumerate(compressed) if abs(c)==1)
    minority = next(k for k in range(3) if row[anchor+k*n] == -compressed[anchor])
    row = tuple(row[(i+minority*n) % (3*n)] for i in range(3*n))
    return sum(1 << i for i,v in enumerate(row) if v == -1)


def invert_solution(masks, operation, source_pair):
    """Separate tuple implementation of the inverse recorded permutation."""
    restored=[]
    for mask,sign,offset in zip(masks, operation['signs'], operation['offsets'], strict=True):
        row = binary(mask)
        source=[None]*45
        for i,value in enumerate(row): source[(sign*operation['u']*(i+offset))%45]=value
        assert None not in source
        restored.append(tuple(source))
    if operation['swap']: restored.reverse()
    return tuple(canonical_mask(row,c) for row,c in zip(restored,source_pair,strict=True))


def audit():
    started=time.perf_counter()
    metadata=json.loads((OUTPUT/'metadata.json').read_text())
    assert metadata['complete']
    for field,path in [('catalog_sha256',CATALOG),('source_sha256',ROOT/'scripts/classify_p5_lifts.py'),
                       ('phase_source_sha256',ROOT/'src/ternary_phase.py'),
                       ('classification_sha256',OUTPUT/'classification.json'),
                       ('symmetry_maps_sha256',OUTPUT/'symmetry_maps.json')]:
        assert metadata[field]==digest(path), (field,'hash mismatch')
    catalog=json.loads(CATALOG.read_text())
    prescribed=structured_compressed_pair(5,3)
    raw=enumerate_intermediate_pairs(*prescribed)
    regenerated={tuple(min(tuple(row[(i+t)%15] for i in range(15)) for t in (0,5,10))
                       for row in pair) for pair in raw}
    key=lambda pair:(sum(3**sum(abs(c)==1 for c in row) for row in pair),
                     max(3**sum(abs(c)==1 for c in row) for row in pair),
                     min(3**sum(abs(c)==1 for c in row) for row in pair),pair)
    ranked=sorted(regenerated,key=key)
    assert len(set(raw))==len(raw)==10476 and len(ranked)==1164
    assert ranked==[tuple(tuple(e[k]) for k in ('first','second')) for e in catalog]
    assert [e['rank'] for e in catalog]==list(range(1,1165))
    records={}
    for path in (OUTPUT/'representatives').glob('branch_*.json'):
        record=json.loads(path.read_text()); rank=record['rank']; records[rank]=record
        pair=ranked[rank-1]
        assert pair==tuple(tuple(record[k]) for k in ('first','second'))
        left,right=record['phase'],record['independent_full_paf']
        assert left['complete'] and right['complete'] and record['status'] in ('sat','verified_empty')
        expected=[3**(sum(abs(c)==1 for c in row)-1) for row in pair]
        for item in (left,right):
            assert item['counts']==item['expected_counts']==expected
            assert len(item['solutions'])==item['canonical_pairs']
            assert 9*len(item['solutions'])==item['ordered_pairs']
        for field in ('counts','projected_histogram_sha256','solutions','canonical_pairs','ordered_pairs'):
            assert left[field]==right[field]
        assert record['ordered_pairs']==left['ordered_pairs']
        assert (record['status']=='verified_empty')==(left['ordered_pairs']==0)
    assert len(records)==79
    branches=json.loads((OUTPUT/'classification.json').read_text())
    maps=json.loads((OUTPUT/'symmetry_maps.json').read_text())
    assert [b['rank'] for b in branches]==list(range(1,1165))
    expanded=set(); canonical_total=0; positive_checks=0; pilot_crosschecks=0
    mask45=(1<<45)-1
    rotate=lambda m,s:((m>>s)|(m<<(45-s))) & mask45
    for branch,pair in zip(branches,ranked,strict=True):
        rank=branch['rank']; rep=branch['representative_rank']; operation=branch['operation']
        assert maps[str(rank)]=={'representative_rank':rep,'operation':operation}
        source_pair=ranked[rep-1]
        assert branch['representative_sha256']==digest(OUTPUT/'representatives'/f'branch_{rep:04d}.json')
        assert branch['status']==records[rep]['status']
        assert branch['ordered_pairs']==records[rep]['ordered_pairs']==9*len(branch['solutions'])
        assert branch['canonical_pairs']==len(branch['solutions'])
        restored=sorted(invert_solution(m,operation,source_pair) for m in branch['solutions'])
        assert [list(m) for m in restored]==records[rep]['phase']['solutions']
        # Check the branch permutation directly on integer intermediate rows.
        original=source_pair[::-1] if operation['swap'] else source_pair
        image=tuple(tuple(row[(sign*operation['u']*(i+t))%15] for i in range(15))
                    for row,sign,t in zip(original,operation['signs'],operation['offsets'],strict=True))
        assert image==pair
        pilot=OUTPUT/'pilot'/f'branch_{rank:04d}.json'
        if pilot.exists():
            direct=json.loads(pilot.read_text())
            assert direct['phase']['solutions']==branch['solutions']
            pilot_crosschecks+=1
        for masks in branch['solutions']:
            rows=tuple(binary(m) for m in masks)
            assert tuple(compress(row,15) for row in rows)==pair
            assert check_legendre_pair(*rows).ok and check_negative_support_sds(*rows).ok
            assert tuple(canonical_mask(row,c) for row,c in zip(rows,pair))==tuple(masks)
            canonical_total+=1; positive_checks+=1
            for s in range(0,45,5):
                a=rotate(masks[0],s)
                for t in range(0,45,5):
                    expanded.add((a,rotate(masks[1],t)))
        if time.perf_counter()-started>600: raise TimeoutError('ten-minute audit cap')
    assert len(expanded)==81*canonical_total==241056
    assert sum(b['ordered_pairs'] for b in branches)==26784
    # Published positive control, canonicalized to the catalogue independently.
    published=published_structured_legendre_pair_45()
    known_rows=[]; known_intermediate=[]
    for row in published:
        c=compress(row,15)
        t=min((0,5,10),key=lambda t:tuple(c[(i+t)%15] for i in range(15)))
        shifted=tuple(row[(i+t)%45] for i in range(45))
        known_rows.append(shifted); known_intermediate.append(compress(shifted,15))
    assert ranked.index(tuple(known_intermediate))+1==771
    known_masks=[canonical_mask(row,c) for row,c in zip(known_rows,known_intermediate)]
    assert known_masks in branches[770]['solutions']
    assert {r:branches[r-1]['ordered_pairs'] for r in (1,2,3,771)}=={1:27,2:27,3:0,771:54}
    # Compact branch-level table is convenient for independent downstream work.
    with (OUTPUT/'branch_counts.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(['rank','representative_rank','status','canonical_pairs','ordered_pairs'])
        writer.writerows([b[k] for k in ('rank','representative_rank','status','canonical_pairs','ordered_pairs')] for b in branches)
    report={'status':'passed','completed_utc':datetime.now(timezone.utc).isoformat(),
            'elapsed_seconds':time.perf_counter()-started,'peak_working_set_bytes':peak_memory(),
            'catalog_regenerated':True,'raw_intermediates':len(raw),'catalog_orbits':len(ranked),
            'representatives_audited':len(records),'pilot_direct_comparisons':pilot_crosschecks,
            'canonical_solutions_direct_paf_sds_compression_checked':positive_checks,
            'unique_ordered_prescribed_binary_pairs_after_translation_expansion':len(expanded),
            'published_rank771_witness_present':True,'status_counts':dict(Counter(b['status'] for b in branches)),
            'ordered_solution_histogram':dict(Counter(b['ordered_pairs'] for b in branches)),
            'classification_sha256':digest(OUTPUT/'classification.json'),
            'source_sha256':digest(Path(__file__)),
            'limitations':'Audit reads representative exhaustion records; does not perform a third exhaustive binary enumeration. No formal UNSAT proof.'}
    save(OUTPUT/'audit.json',report)
    files=[CATALOG,ROOT/'scripts/classify_p5_lifts.py',ROOT/'src/ternary_phase.py',Path(__file__),
           ROOT/'src/staged_uncompression.py',ROOT/'src/legendre.py']
    files.extend(p for p in OUTPUT.rglob('*') if p.is_file() and p.name!='manifest.json')
    save(OUTPUT/'manifest.json',{'algorithm':'sha256','files':[{'path':p.relative_to(ROOT).as_posix(),
         'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(set(files))]})
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__': audit()
