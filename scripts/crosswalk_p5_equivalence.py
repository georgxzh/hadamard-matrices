"""Convert the restricted census to FGS (2001), Section 5.4 equivalence.

This computes labels for our subset; it does not retrieve or match the old list.
"""
import json
import time
from collections import Counter, defaultdict
from functools import lru_cache
from math import gcd
from pathlib import Path

from scripts.classify_p5_lifts import ROOT, digest, save, peak_memory
from src.legendre import check_legendre_pair, check_negative_support_sds


def bracelet(mask, length):
    full=(1 << length)-1
    reverse=sum(((mask >> i)&1) << ((-i)%length) for i in range(length))
    best=mask
    for value in (mask,reverse):
        for _ in range(length):
            best=min(best,value)
            value=((value << 1)&full)|(value >> (length-1))
    return best


@lru_cache(maxsize=100_000)
def decimated_bracelet(mask, unit, length):
    return bracelet(sum(((mask >> ((unit*i)%length))&1) << i for i in range(length)),length)


def canonical_pair(pair, length):
    # First taking bracelets changes no subsequent common-decimation orbit.
    a,b=(bracelet(m,length) for m in pair)
    return min(tuple(sorted((decimated_bracelet(a,u,length),decimated_bracelet(b,u,length))))
               for u in range(1,length) if gcd(u,length)==1)


def main():
    start=time.perf_counter(); source=ROOT/'results/p5_classification/classification.json'
    records=json.loads(source.read_text()); samples=[(r['rank'],tuple(m)) for r in records for m in r['solutions']]
    # Bounded pilot and conservative memory/storage estimates precede the scan.
    for _,pair in samples[:30]: canonical_pair(pair,45)
    pilot=time.perf_counter()-start
    estimate=2*pilot*len(samples)/30
    if estimate>1200 or peak_memory()>1_000_000_000:
        raise RuntimeError('crosswalk pilot exceeds conservative resource gate')
    groups=defaultdict(list)
    for rank,pair in samples:
        if time.perf_counter()-start>1500: raise TimeoutError('crosswalk run budget')
        key=canonical_pair(pair,45)
        groups[key].append({'rank':rank,'masks':pair})
    classes=[]
    for key,members in sorted(groups.items()):
        rows=[tuple(1-2*((m >> i)&1) for i in range(45)) for m in key]
        assert check_legendre_pair(*rows).ok and check_negative_support_sds(*rows).ok
        classes.append({'representative_masks':key,'phase_gauged_members':len(members),
                        'prescribed_ordered_members':81*len(members),'members':members})
    output=ROOT/'results/phase_propagation/equivalence_crosswalk.json'
    save(output,{'complete':True,'classes':classes,'class_count':len(classes),
                 'phase_gauged_pairs':len(samples),'prescribed_ordered_pairs':81*len(samples),
                 'class_intersection_histogram':dict(Counter(len(v) for v in groups.values())),
                 'pilot_seconds':pilot,'estimated_seconds_with_margin':estimate,
                 'estimated_storage_bytes':2_000_000,'memory_gate_bytes':1_000_000_000,
                 'elapsed_seconds':time.perf_counter()-start,'peak_working_set_bytes':peak_memory(),
                 'source_sha256':digest(source),'script_sha256':digest(Path(__file__)),
                 'convention':'row exchange, independent cyclic shifts and reversals, common units modulo 45; row sums +1',
                 'limitation':'Restricted subset only. Historical list of 3058 representatives not obtained; no record-by-record crosswalk claimed.'})
    print({k:v for k,v in json.loads(output.read_text()).items() if k!='classes'})


if __name__=='__main__': main()
