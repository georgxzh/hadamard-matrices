"""Bounded challenge of moments plus the preceding simultaneous compression.

Stop at an explicit false positive: full intersection counting is unnecessary.
"""
from pathlib import Path
import hashlib
import time
from scripts.phase_moment_obstruction import ROOT,load,save
from scripts.audit_fiber_structure import row,compress,paf


def main():
    start=time.perf_counter();seen=0;witness=None
    for h in load('results/phase_moments/rank_279.json')['modular_solutions'][:25]:
        seen+=1;xs=[row(m,45) for m in h['masks']];us=[compress(x,9) for x in xs]
        if sum(v*v for u in us for v in u)!=82:continue
        if not all(a+b==-10 for a,b in zip(paf(us[0]),paf(us[1]))):continue
        sums=[a+b for a,b in zip(paf(xs[0]),paf(xs[1]))]
        assert all((v+2)%12==0 for v in sums) and any(v!=-2 for v in sums)
        witness={**h,'alternate_compressions':us,'full_paf_sums':sums,
                 'first_failed_shift':next(i+1 for i,v in enumerate(sums) if v!=-2)}
        break
    save('refinement_challenge.json',{'rank':279,'tested':seen,'cap':25,
         'outcome':'explicit_false_positive' if witness else 'unresolved_bounded_challenge',
         'witness':witness,'seconds':time.perf_counter()-start,
         'scope':'Moments modulo three, actual global phases and carries, and exact alternate length-nine PAF/energy conditions together.',
         'preliminary_pilot':{'cases':25,'seconds':0.0047722999879624695,
             'estimated_all_1474_seconds_10x':2.814455598290078,
             'decision':'A counterexample already exists; no full intersection census is needed.'},
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print({'tested':seen,'witness':witness})


if __name__=='__main__':main()
