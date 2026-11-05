"""Bounded exact local arithmetic on saved phase witnesses; no lift search.

All polynomials are low-degree-first. New output only in primitive_local/.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from src.legendre import cyclotomic_polynomial, _reduce_mod_monic, exact_psd_sum
from src.ternary_phase import PhaseRow
from scripts.audit_fiber_structure import row, cases
from scripts.audit_residual_obstruction import third_gauge

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/primitive_local'
PHI = cyclotomic_polynomial(45)


def load(name):
    return json.loads((ROOT / name).read_text())


def save(name, obj):
    OUT.mkdir(exist_ok=True, parents=True)
    (OUT/name).write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n', encoding='utf8', newline='\n')


def red(a):
    reduced = list(_reduce_mod_monic(a, PHI))
    return reduced + [0] * (24-len(reduced))


POW = [red([0]*i+[1]) for i in range(45)]


def mul(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return red(c)


def conj(a):
    return [sum(x*POW[(-i)%45][k] for i,x in enumerate(a)) for k in range(24)]


INV_PI_NUM = [sum((8-j)*POW[(5*j)%45][k] for j in range(8)) for k in range(24)]


def valuation(a):
    if not any(a):
        return 'infinity'
    v = 0
    while True:
        divided = mul(a, INV_PI_NUM)
        if any(x%9 for x in divided):
            return v
        a = [x//9 for x in divided]
        v += 1
        assert v < 100


def phase_norm(cs, phases):
    offset = 0
    fs = []
    for c in cs:
        active = [i for i,x in enumerate(c) if abs(x)==1]
        f = [0]*24
        for j,i in enumerate(active):
            for k,x in enumerate(POW[i+15*phases[offset+j]]):
                f[k] += c[i]*x
        offset += len(active)
        fs.append(f)
    assert offset == len(phases)
    norms = [mul(f,conj(f)) for f in fs]
    defect = [sum(x) for x in zip(*norms)]
    defect[0] -= 23
    return fs, defect


def coefficient_bounds(cs):
    """Triangle bounds for each coefficient, relaxing edge compatibility only."""
    lower = [0]*24
    upper = [0]*24
    lower[0] = upper[0] = sum(abs(x)==1 for c in cs for x in c)-23
    for c in cs:
        active = [i for i,x in enumerate(c) if abs(x)==1]
        for ii,i in enumerate(active):
            for j in active[ii+1:]:
                options = [[c[i]*c[j]*(POW[(j-i+15*h)%45][k]+POW[(i-j-15*h)%45][k])
                            for k in range(24)] for h in range(3)]
                for k in range(24):
                    lower[k] += min(x[k] for x in options)
                    upper[k] += max(x[k] for x in options)
    return {'lower':lower, 'upper':upper, 'max_absolute':max(map(abs,lower+upper))}


def inspect(cs, h):
    fs, defect = phase_norm(cs, h['phases'])
    # Independent existing spectral calculation uses complete binary PAFs.
    psd = list(exact_psd_sum(*(row(x,45) for x in h['masks']),1).coefficients)
    psd += [0]*(24-len(psd)); psd[0] -= 92
    assert psd == [4*x for x in defect]
    offset=0
    for c,mask in zip(cs,h['masks']):
        phases = PhaseRow(c).encode(row(mask,45))
        assert list(phases)==h['phases'][offset:offset+len(phases)]
        offset += len(phases)
    assert tuple(h['masks']) == third_gauge(h['masks'],cs)
    return {'source_free_index':h.get('free_index'),
            'masks':h['masks'], 'phases':h['phases'], 'F':fs, 'norm_defect':defect,
            'pi_valuation':valuation(defect),
            'mod_3':all(x%3==0 for x in defect),
            'mod_9':all(x%9==0 for x in defect),
            'mod_23':all(x%23==0 for x in defect)}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=['pilot','audit'])
    args=parser.parse_args(); start=time.perf_counter()
    if args.stage=='audit':
        pilot=load('results/primitive_local/pilot.json')
        assert pilot['estimated_audit_seconds_10x'] < 120
        assert pilot['memory_estimate_bytes'] < 10_000_000_000
    catalogue=load('results/p5_branch_portfolio/canonical_branches.json')
    results=[]
    for rank in (277,279):
        c=catalogue[rank-1];cs=[c['first'],c['second']]
        hits=load('results/phase_moments/rank_'+str(rank)+'.json')['modular_solutions']
        if args.stage=='pilot': hits=hits[:25]
        records=[]
        for h in hits:
            assert time.perf_counter()-start < 120
            records.append(inspect(cs,h))
        results.append({'rank':rank,'tested':len(records),'bounds':coefficient_bounds(cs),
                        'valuation_histogram':dict(Counter(str(x['pi_valuation']) for x in records)),
                        'mod_3_count':sum(x['mod_3'] for x in records),
                        'mod_9_count':sum(x['mod_9'] for x in records),
                        'mod_23_count':sum(x['mod_23'] for x in records),
                        'records':records})
    c=catalogue[278];false=inspect([c['first'],c['second']],load('results/phase_moments/refinement_challenge.json')['witness'])
    out={'stage':args.stage,'workers':1,'seconds':time.perf_counter()-start,
         'cases':results,'saved_false_positive':false,'phi45':PHI,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
             'results/p5_branch_portfolio/canonical_branches.json',
             'results/phase_moments/rank_277.json','results/phase_moments/rank_279.json',
             'results/phase_moments/refinement_challenge.json')},
         'time_cap_seconds':120,'memory_estimate_bytes':100_000_000,'storage_estimate_bytes':5_000_000}
    if args.stage=='pilot':
        out['estimated_audit_seconds_10x']=out['seconds']*1474/50*10
    save(args.stage+'.json',out)
    print({k:v for k,v in out.items() if k not in ('cases','saved_false_positive')})
    print([{k:v for k,v in r.items() if k not in ('records','bounds')}|{'bound':r['bounds']['max_absolute']} for r in results])
    print({'false':false})


if __name__=='__main__':main()
