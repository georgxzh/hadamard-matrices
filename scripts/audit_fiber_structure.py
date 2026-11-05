"""Read-only structural audit of frozen lifts; tiny independent counterchecks.

Stages: baseline, pilot, audit. One worker, 120 s guard, no spectral arithmetic.
Outputs are new; this does not repeat either completed lifting census.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/fiber_structure'
BASE = '0c23a7e2989ba863e33817a49b6b934c526598ea'


def load(name):
    return json.loads((ROOT / name).read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n',
                            encoding='utf8', newline='\n')


def frozen_digest():
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE,
                                     'results'], cwd=ROOT, text=True).splitlines()
    h = hashlib.sha256()
    for name in paths:
        h.update((name+' '+sha(ROOT/name)+'\n').encode())
    return {'files': len(paths), 'ordered_path_sha256_digest': h.hexdigest()}


def row(mask, length):
    return tuple(1-2*((mask >> i)&1) for i in range(length))


def compress(x, n):
    return tuple(sum(x[i::n]) for i in range(n))


def paf(x):
    return tuple(sum(a*x[(i+s)%len(x)] for i,a in enumerate(x))
                 for s in range(1, len(x)))


def affine(mask, length, unit=1, offset=0):
    return sum(((mask >> ((unit*i+offset)%length))&1) << i for i in range(length))


def phase_gauge(mask, c):
    n = len(c)
    i = next(i for i,v in enumerate(c) if abs(v)==1)
    x = row(mask, 3*n)
    minority = -c[i]
    a = next(k for k in range(3) if x[i+k*n]==minority)
    return affine(mask, 3*n, offset=a*n)


def kernel_pair(pair, cs, t):
    n = len(cs[0])
    return tuple(phase_gauge(affine(m, 3*n, 1+t*n), c) for m,c in zip(pair,cs))


def cases():
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    for c,r in zip(cat,load('results/p5_classification/classification.json'),strict=True):
        yield {'id': 'p5_'+str(r['rank']), 'rank': r['rank'],
               'rows': [c['first'],c['second']], 'solutions': r['solutions']}
    for b in load('results/p7_portfolio/portfolio.json')['branches']:
        yield {'id': 'p7_'+b['id'], 'rows': b['pair'], 'solutions': []}
    yield {'id': 'p7_positive', 'rows': load('results/p7_positive_control/witness.json')['pair'],
           'solutions': load('results/p7_positive_control/solutions.json')['canonical_masks']}


def check_case(c):
    cs = c['rows']; n = len(cs[0]); masks = {tuple(m) for m in c['solutions']}
    assert sum(v*v for r in cs for v in r)==6*n-4
    for r in cs:
        assert sum(r)==1
        assert len({i%3 for i,v in enumerate(r) if abs(v)==1})>=2
    orbits = set(); signature_changes = 0
    for pair in sorted(masks):
        xs = [row(m,3*n) for m in pair]
        assert all(compress(x,n)==tuple(r) for x,r in zip(xs,cs))
        assert all(a+b==-2 for a,b in zip(paf(xs[0]),paf(xs[1])))
        orbit = tuple(sorted(kernel_pair(pair,cs,t) for t in range(3)))
        assert len(set(orbit))==3 and set(orbit)<=masks
        assert kernel_pair(kernel_pair(pair,cs,1),cs,2)==pair
        # Stronger one-row freeness, and the explicit third phase gauge.
        for side in range(2): assert len({m[side] for m in orbit})==3
        active = [i for i,v in enumerate(cs[0]) if abs(v)==1]
        i0 = active[0]; i1 = next(i for i in active if (i-i0)%3)
        selected = [m for m in orbit if row(m[0],3*n)[i1]==-cs[0][i1]]
        assert len(selected)==1
        signature_changes += paf(xs[0])!=paf(row(kernel_pair(pair,cs,1)[0],3*n))
        orbits.add(orbit)
    assert 3*len(orbits)==len(masks)
    return {'id':c['id'], 'phase_pairs':len(masks), 'ordered_pairs':9*len(masks),
            'kernel_orbits':[list(o) for o in sorted(orbits)],
            'first_row_signature_changes':signature_changes}


def tiny_census(length, n):
    rows = [tuple(-1 if i in neg else 1 for i in range(length))
            for neg in map(set,combinations(range(length),(length-1)//2))]
    buckets = defaultdict(list)
    for x in rows: buckets[paf(x)].append(x)
    counts = Counter()
    for x in rows:
        for y in buckets.get(tuple(-2-v for v in paf(x)),[]):
            counts[(compress(x,n),compress(y,n))] += 1
    return {'length':length,'compressed_length':n,'row_domain':len(rows),
            'ordered_pairs':sum(counts.values()), 'nonempty_fibers':len(counts),
            'fiber_histogram':dict(Counter(counts.values())),
            'minimum_example':{'rows':min(counts,key=counts.get), 'count':min(counts.values())}}


def affine_cycles(q, n, a, b):
    length=q*n; unseen=set(range(length)); cycles=[]
    while unseen:
        start=min(unseen); current=start; cycle=[]
        while current in unseen:
            unseen.remove(current);cycle.append(current)
            current=((1+a*n)*current+b*n)%length
        assert current==start
        cycles.append(cycle)
    return cycles


def fixed_row_check(q, n):
    # Enumerate signs on affine coordinate orbits, not length-q*n LP pairs.
    tested=normalized=0; minima=[]
    for a in range(1,q):
        for b in range(q):
            cycles=affine_cycles(q,n,a,b); best=None
            assert len(cycles)<=9
            for signs in product((-1,1),repeat=len(cycles)):
                tested+=1
                if sum(s*len(c) for s,c in zip(signs,cycles))!=1: continue
                normalized+=1; x=[0]*(q*n)
                for s,c in zip(signs,cycles):
                    for i in c:x[i]=s
                c=compress(x,n); energy=sum(v*v for v in c)
                best=energy if best is None else min(best,energy)
                assert energy+n > 2*q*n-2*(q-1)
            minima.append(best)
    return {'q':q,'n':n,'affine_maps':q*(q-1),'sign_assignments':tested,
            'normalized_rows':normalized,'minimum_row_energy':min(v for v in minima if v is not None),
            'partner_energy_lower_bound':n,'pair_energy_required':2*q*n-2*(q-1)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['baseline','pilot','audit'])
    stage=parser.parse_args().stage; start=time.perf_counter()
    if stage=='baseline':
        save('baseline.json',{'base_commit':BASE, 'frozen_results':frozen_digest(),
             'old_paper_manifest_sha256':sha(ROOT/'paper/artifact_manifest.json'),
             'old_publication_manifest_sha256':sha(ROOT/'results/publication_gap_audit/manifest.json')})
        return
    all_cases=list(cases())
    if stage=='pilot':
        chosen=[c for c in all_cases if c['solutions']][:25]+all_cases[-1:]
        for c in chosen:check_case(c)
        tiny=[tiny_census(3,1),tiny_census(9,3)]
        fixed=[fixed_row_check(3,3),fixed_row_check(5,5)]
        elapsed=time.perf_counter()-start
        estimate=10*elapsed*len(all_cases)/len(chosen)
        save('pilot.json',{'completed':True,'cases':len(chosen),'elapsed_seconds':elapsed,
             'estimate_seconds_with_10x_margin':estimate,'serial_workers':1,
             'memory_estimate_bytes':200_000_000,'output_estimate_bytes':2_000_000,
             'timeout_seconds':120,'tiny_censuses':tiny,'fixed_row_checks':fixed,
             'scope':'Action checks on existing solutions; at most 126 rows in tiny LP census, 20*512 sign assignments in q=5 affine check.'})
        if estimate>120:raise RuntimeError('Pilot exceeds planned gate')
        return
    pilot=load('results/fiber_structure/pilot.json');assert pilot['estimate_seconds_with_10x_margin']<=120
    results=[]
    for c in all_cases:
        if time.perf_counter()-start>120:raise TimeoutError('Unresolved structural audit')
        results.append(check_case(c))
    lookup={}
    for index,c in enumerate(load('results/phase_propagation/equivalence_crosswalk.json')['classes'],1):
        for m in c['members']:lookup[(m['rank'],tuple(m['masks']))]=index
    entries=Counter(); example=None
    for c,r in zip(all_cases,results):
        if 'rank' not in c:continue
        for orbit in r['kernel_orbits']:
            labels={lookup[(c['rank'],tuple(m))] for m in orbit};assert len(labels)==1
            entries[(c['rank'],labels.pop())]+=1
    for (rank,label),count in sorted(entries.items()):
        if count>1:
            rr=next(r for c,r in zip(all_cases,results) if c.get('rank')==rank)
            example={'rank':rank,'class_id':label,'kernel_orbits':[o for o in rr['kernel_orbits'] if lookup[(rank,tuple(o[0]))]==label]}
            break
    assert Counter(entries.values())==Counter({1:928,2:32})
    assert frozen_digest()==load('results/fiber_structure/baseline.json')['frozen_results']
    save('audit.json',{'complete':True,'cases':results,'branches':len(results),
         'phase_pairs_checked':sum(r['phase_pairs'] for r in results),
         'kernel_orbits':sum(len(r['kernel_orbits']) for r in results),
         'incidence_orbit_histogram':dict(Counter(entries.values())),
         'counterexample_to_one_orbit_per_incidence':example,
         'signature_changes':sum(r['first_row_signature_changes'] for r in results),
         'frozen_results_unchanged':True,'elapsed_seconds':time.perf_counter()-start,
         'python':platform.python_version(),'platform':platform.platform(),
         'script_sha256':sha(Path(__file__)),
         'scope':'Finite integer action/compression/PAF validation, not a new lifting exhaustion, external replication, or general proof.'})
    print({k:v for k,v in load('results/fiber_structure/audit.json').items() if k not in ('cases','counterexample_to_one_orbit_per_incidence')})


if __name__=='__main__':main()
