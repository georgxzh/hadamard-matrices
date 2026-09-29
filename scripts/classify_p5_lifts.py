"""Pilot and independently verify all prescribed p=5 intermediate branches.

Four workers at most, a 27-minute full-run wall cap, and resumable per-branch
records. An incomplete branch is always unresolved. The second enumerator
uses binary residue masks and all 22 nonredundant PAF shifts, independently
of the phase identity and the projected-key theorem.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import platform
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from itertools import combinations, product
from math import gcd
from pathlib import Path

from scripts.benchmark_staged_uncompression import _ProcessMemoryCounters
from src.legendre import check_legendre_pair, check_negative_support_sds, compress, structured_compressed_pair
from src.staged_uncompression import FactorThreeBranch, canonical_intermediate_translation
from src.ternary_phase import PhaseRow

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "results/p5_branch_portfolio/canonical_branches.json"
OUTPUT = ROOT / "results/p5_classification"


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n", encoding="utf-8", newline="\n")


def peak_memory():
    if platform.system() != "Windows":
        return None
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    counters = _ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    ok = psapi.GetProcessMemoryInfo(ctypes.c_void_p(kernel.GetCurrentProcess()),
                                    ctypes.byref(counters), counters.cb)
    return int(counters.PeakWorkingSetSize) if ok else None


def independent_masks(compressed, canonical=True):
    """Cartesian product of binary residue patterns; no PhaseRow dependency."""
    n = len(compressed)
    anchor = next(i for i, value in enumerate(compressed) if abs(value) == 1)
    classes = []
    for i, value in enumerate(compressed):
        choices = list(combinations(range(3), (3-value)//2))
        if canonical and i == anchor:
            # Minority layer zero, for either sign of the compressed entry.
            choices = [choice for choice in choices if ((0 in choice) == (value == 1))]
        classes.append(tuple(sum(1 << (i+k*n) for k in choice) for choice in choices))
    for parts in product(*classes):
        mask = 0
        for part in parts:
            mask |= part
        yield mask


def packed_key(mask, length=45, shifts=22):
    full = (1 << length)-1
    return bytes(2*length - 2*(mask ^ (((mask >> s) | (mask << (length-s))) & full)).bit_count()
                 for s in range(1, shifts+1))


def binary(mask, length=45):
    return tuple(1-2*((mask >> i) & 1) for i in range(length))


def phase_mask(row, phases):
    return sum(1 << i for i, value in enumerate(row.decode(phases)) if value == -1)


def histogram_hash(histogram):
    h = hashlib.sha256()
    for key, count in sorted(histogram.items()):
        h.update(key)
        h.update(count.to_bytes(8, "little"))
    return h.hexdigest()


def enumerate_branch(pair, method, *, deadline, canonical=True, projected=False):
    """Return complete multiplicity counts, row digests and every matched mask pair."""
    active = [sum(abs(c)==1 for c in row) for row in pair]
    expected = [3**(k-int(canonical)) for k in active]
    stored = min(range(2), key=lambda r: expected[r])
    phases = [PhaseRow(row) for row in pair] if method == "phase" else None
    count = [0, 0]
    histograms = [Counter(), Counter()]
    table = defaultdict(list)
    matches = []
    start = time.perf_counter()
    for side in (stored, 1-stored):
        if method == "phase":
            if not canonical:
                raise ValueError("phase iterator uses the proved translation gauge")
            candidates = ((bytes(v+45 for v in signature), a)
                          for a, signature in phases[side].iter_projected_signatures())
        else:
            shifts = 14 if projected else 22
            candidates = ((packed_key(mask, shifts=shifts), mask)
                          for mask in independent_masks(pair[side], canonical=canonical))
        for key, representative in candidates:
            count[side] += 1
            if count[side] % 1024 == 0 and time.perf_counter() >= deadline:
                return {"complete": False, "reason": "time_limit", "counts": count}
            histograms[side][key[:14]] += 1
            if side == stored:
                table[key].append(representative)
            elif all(v <= 88 for v in key):
                for other in table.get(bytes(88-v for v in key), ()):
                    values = [None, None]
                    values[stored], values[side] = other, representative
                    masks = tuple(phase_mask(phases[r], values[r]) if method == "phase"
                                  else values[r] for r in range(2))
                    matches.append(masks)
    if count != expected:
        raise AssertionError(f"incomplete enumerator {count} != {expected}")
    if len(set(matches)) != len(matches):
        raise AssertionError("duplicate ordered binary pair")
    return {
        "complete": True, "elapsed_seconds": time.perf_counter()-start,
        "counts": count, "expected_counts": expected,
        "stored_signatures": len(table),
        "projected_histogram_sha256": [histogram_hash(h) for h in histograms],
        "canonical_pairs": len(matches),
        "ordered_pairs": len(matches)*(9 if canonical else 1),
        "solutions": sorted(matches),
    }


def classify(entry, directory, seconds=120):
    start = time.perf_counter()
    pair = tuple(tuple(entry[k]) for k in ("first", "second"))
    FactorThreeBranch(*structured_compressed_pair(5,3), *pair)
    deadline = start+seconds
    phase = enumerate_branch(pair, "phase", deadline=deadline)
    full = enumerate_branch(pair, "packed", deadline=deadline)
    record = {
        "rank": entry["rank"], "first": pair[0], "second": pair[1],
        "magnitude_one_counts": entry["magnitude_one_counts"],
        "phase": phase, "independent_full_paf": full,
        "status": "unresolved", "elapsed_seconds": time.perf_counter()-start,
        "peak_worker_working_set_bytes": peak_memory(),
    }
    if phase["complete"] and full["complete"]:
        for key in ("counts", "projected_histogram_sha256", "solutions", "ordered_pairs"):
            if phase[key] != full[key]:
                raise AssertionError(f"independent enumerators disagree at rank {entry['rank']}: {key}")
        for masks in phase["solutions"]:
            rows = tuple(binary(mask) for mask in masks)
            if not check_legendre_pair(*rows).ok or not check_negative_support_sds(*rows).ok:
                raise AssertionError("matched pair fails direct PAF or SDS")
            if tuple(compress(row,15) for row in rows) != pair:
                raise AssertionError("wrong branch")
        record.update(status="sat" if phase["ordered_pairs"] else "verified_empty",
                      canonical_pairs=phase["canonical_pairs"],
                      ordered_pairs=phase["ordered_pairs"],
                      all_solutions_direct_paf_sds_checked=True)
    path = Path(directory) / f"branch_{entry['rank']:04d}.json"
    save(path, record)
    return record


def pilot(workers=4):
    catalog = json.loads(CATALOG.read_text())
    strata = defaultdict(list)
    for e in catalog:
        strata[tuple(e["magnitude_one_counts"])].append(e)
    ranks = {1,2,3,771}
    for entries in strata.values():
        ranks.update(entries[index]["rank"] for index in (0,len(entries)//2,-1))
    selected = [e for e in catalog if e["rank"] in ranks]
    start = time.perf_counter()
    records=[]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        jobs=[executor.submit(classify,e,OUTPUT/"pilot") for e in selected]
        for job in as_completed(jobs):
            r=job.result(); records.append(r)
            print(f"pilot rank {r['rank']}: {r['status']} in {r['elapsed_seconds']:.2f}s",flush=True)
    elapsed=time.perf_counter()-start
    estimates=[]
    for split, entries in strata.items():
        measured=[r["elapsed_seconds"] for r in records if tuple(r["magnitude_one_counts"])==split]
        estimates.append({"split":split,"branches":len(entries),"sample_seconds":measured,
                          "estimated_worker_seconds":len(entries)*max(measured)})
    estimate=sum(e["estimated_worker_seconds"] for e in estimates)/workers
    metadata={"mode":"pilot","workers":workers,"elapsed_seconds":elapsed,
              "selected_ranks":sorted(ranks),"strata":estimates,
              "estimated_full_wall_seconds_conservative":1.20*estimate,
              "estimated_peak_memory_bytes":workers*max(r["peak_worker_working_set_bytes"] or 0 for r in records),
              "estimated_record_storage_bytes":sum(p.stat().st_size for p in (OUTPUT/"pilot").glob('*.json'))/len(records)*1164,
              "all_pilot_branches_verified":all(r["status"]!="unresolved" for r in records),
              "catalog_sha256":digest(CATALOG),"completed_utc":datetime.now(timezone.utc).isoformat()}
    save(OUTPUT/"pilot.json",metadata)
    print(json.dumps(metadata,indent=2),flush=True)


def symmetry_partition(catalog):
    """Bijections of lift sets, without identifying catalog row labels/counts.

    Independent reversals, simultaneous decimation, and a row swap exactly
    when chi_5(u)=-1 preserve the prescribed ordered pair. All units mod 15
    used here are also units mod 45. Offsets are applied after decimation.
    """
    lookup={(tuple(e['first']),tuple(e['second'])):e['rank'] for e in catalog}
    assigned={}
    groups={}
    for entry in catalog:
        rank=entry['rank']
        if rank in assigned: continue
        pair=tuple(tuple(entry[k]) for k in ('first','second'))
        targets={}
        for u in range(15):
            if gcd(u,15)!=1: continue
            swap=u%5 in (2,3)
            rows=pair[::-1] if swap else pair
            for signs in product((-1,1),repeat=2):
                images=[]; offsets=[]
                for row,sign in zip(rows,signs,strict=True):
                    mapped=tuple(row[(sign*u*i)%15] for i in range(15))
                    normalized,offset=canonical_intermediate_translation(mapped,5)
                    images.append(normalized); offsets.append(offset)
                target=lookup[tuple(images)]
                targets.setdefault(target,{'u':u,'swap':swap,'signs':signs,'offsets':offsets})
        if min(targets)!=rank or any(t in assigned for t in targets):
            raise AssertionError('symmetry maps do not form a disjoint closed partition')
        groups[rank]=sorted(targets)
        for target,operation in targets.items():
            assigned[target]={'representative_rank':rank,'operation':operation}
    if len(assigned)!=1164 or len(groups)!=79:
        raise AssertionError('unexpected p5 symmetry partition')
    return groups,assigned


def transfer_masks(masks, operation, target_pair):
    """Apply the recorded permutation at length 45 and restore phase-zero gauges."""
    source=masks[::-1] if operation['swap'] else masks
    result=[]
    for mask,sign,offset,compressed in zip(source,operation['signs'],operation['offsets'],target_pair,strict=True):
        moved=sum(((mask >> ((sign*operation['u']*(i+offset))%45)) & 1) << i for i in range(45))
        anchor=next(i for i,c in enumerate(compressed) if abs(c)==1)
        minority=next(k for k in range(3) if ((moved >> (anchor+15*k)) & 1)==(compressed[anchor]==1))
        shift=15*minority
        moved=((moved >> shift) | (moved << (45-shift))) & ((1<<45)-1)
        result.append(moved)
    return tuple(result)


def full_run(workers=3):
    catalog=json.loads(CATALOG.read_text())
    pilot_data=json.loads((OUTPUT/'pilot.json').read_text())
    if not pilot_data['all_pilot_branches_verified'] or pilot_data['catalog_sha256']!=digest(CATALOG):
        raise RuntimeError('a complete matching pilot is required')
    groups,assigned=symmetry_partition(catalog)
    costs={tuple(s['split']):max(s['sample_seconds']) for s in pilot_data['strata']}
    estimate=1.5*sum(costs[tuple(catalog[r-1]['magnitude_one_counts'])] for r in groups)/workers
    memory=pilot_data['estimated_peak_memory_bytes']/pilot_data['workers']*workers*1.5
    proposal={'representatives':len(groups),'catalog_branches':len(catalog),'workers':workers,
              'estimated_wall_seconds_with_50_percent_margin':estimate,
              'estimated_peak_worker_memory_bytes_with_50_percent_margin':memory,
              'estimated_storage_bytes':pilot_data['estimated_record_storage_bytes']*4,
              'hard_wall_seconds':1620,'per_branch_seconds':120,
              'proof':'independent reversals; common unit decimation; nonsquare swap; explicit bijections',
              'group_size_histogram':dict(Counter(map(len,groups.values())))}
    save(OUTPUT/'resource_plan.json',proposal)
    if estimate>1500 or memory>8_000_000_000 or proposal['estimated_storage_bytes']>8_000_000_000:
        raise RuntimeError('full-run estimate exceeds conservative resource envelope; approval required')
    print('Resource plan: '+json.dumps(proposal),flush=True)
    save(OUTPUT/'symmetry_maps.json',assigned)
    started=time.perf_counter()
    records={}
    # Reuse independently checked pilot representatives only; no pilot timeouts.
    for rank in groups:
        path=OUTPUT/'pilot'/f'branch_{rank:04d}.json'
        if path.exists():
            record=json.loads(path.read_text())
            if record['status']!='unresolved': records[rank]=record
    pending=[catalog[rank-1] for rank in groups if rank not in records]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        jobs={executor.submit(classify,e,OUTPUT/'representatives'):e['rank'] for e in pending}
        try:
            for job in as_completed(jobs,timeout=1620-130):
                r=job.result(); records[r['rank']]=r
                print(f"representative {r['rank']}: {r['status']}; {len(records)}/79",flush=True)
        except TimeoutError:
            for job in jobs: job.cancel()
            # Running jobs have their own <=120s deadline. Pending branches
            # remain unresolved, with no empty result inferred.
    for rank,record in records.items(): save(OUTPUT/'representatives'/f'branch_{rank:04d}.json',record)
    branches=[]
    for entry in catalog:
        rank=entry['rank']; mapping=assigned[rank]; representative=records.get(mapping['representative_rank'])
        result={'rank':rank,**mapping,'status':'unresolved'}
        if representative and representative['status']!='unresolved':
            target=tuple(tuple(entry[k]) for k in ('first','second'))
            solutions=sorted(transfer_masks(m,mapping['operation'],target) for m in representative['phase']['solutions'])
            if len(set(solutions))!=len(solutions): raise AssertionError('noninjective solution transfer')
            for masks in solutions:
                rows=tuple(binary(m) for m in masks)
                if tuple(compress(row,15) for row in rows)!=target or not check_legendre_pair(*rows).ok or not check_negative_support_sds(*rows).ok:
                    raise AssertionError('transferred solution fails independent exact checks')
            result.update(status=representative['status'],canonical_pairs=len(solutions),
                          ordered_pairs=9*len(solutions),solutions=solutions,
                          representative_sha256=digest(OUTPUT/'representatives'/f"branch_{mapping['representative_rank']:04d}.json"))
            original=OUTPUT/'pilot'/f'branch_{rank:04d}.json'
            if original.exists():
                check=json.loads(original.read_text())
                if check['status']!='unresolved' and check['phase']['solutions']!=[list(m) for m in solutions]:
                    raise AssertionError('symmetry transfer disagrees with directly enumerated pilot')
        branches.append(result)
    save(OUTPUT/'classification.json',branches)
    completed=all(r['status']!='unresolved' for r in branches)
    metadata={'completed_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-started,
              'complete':completed,'resource_plan':proposal,'catalog_sha256':digest(CATALOG),
              'source_sha256':digest(Path(__file__)),'phase_source_sha256':digest(ROOT/'src/ternary_phase.py'),
              'classification_sha256':digest(OUTPUT/'classification.json'),'symmetry_maps_sha256':digest(OUTPUT/'symmetry_maps.json'),
              'status_counts':dict(Counter(r['status'] for r in branches)),
              'ordered_solution_histogram':dict(Counter(r['ordered_pairs'] for r in branches if 'ordered_pairs' in r)),
              'sum_ordered_pairs_over_translation_representatives':sum(r.get('ordered_pairs',0) for r in branches),
              'sum_ordered_pairs_over_all_10476_intermediates':9*sum(r.get('ordered_pairs',0) for r in branches),
              'known_rank_counts':{r:branches[r-1].get('ordered_pairs') for r in (1,2,3,771)},
              'workers':workers,'python':platform.python_version(),'platform':platform.platform(),
              'negative_evidence':'two independent exhaustive enumerations plus proved explicit symmetry bijections; no standalone PB UNSAT proof'}
    save(OUTPUT/'metadata.json',metadata)
    print(json.dumps(metadata,indent=2),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot",action="store_true")
    parser.add_argument("--workers",type=int,default=4)
    parser.add_argument("--full",action="store_true")
    args=parser.parse_args()
    if not 1<=args.workers<=4: raise ValueError("one to four workers required")
    if args.pilot: pilot(args.workers)
    elif args.full: full_run(args.workers)
    else: raise ValueError("run the pilot first")


if __name__=="__main__":
    main()
