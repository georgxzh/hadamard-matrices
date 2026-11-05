"""Exact noncoprime simultaneous-compression relaxation, separate from frozen runs."""
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import time

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/residual_obstruction'

def load(p): return json.loads((ROOT/p).read_text())
def save(name,v):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')

def margins(rows,cols):
    """Gale-Ryser, using negative-support counts, no numerical tolerances."""
    r=sorted(rows,reverse=True)
    return (all(0<=x<=len(cols) for x in r) and
            all(0<=x<=len(rows) for x in cols) and sum(r)==sum(cols) and
            all(sum(r[:k])<=sum(min(k,c) for c in cols) for k in range(1,len(r)+1)))

def options(c):
    # L=9p, fixed compression to 3p, alternate to 9; gcd=3 for p != 3.
    p=len(c)//3
    assert p in (5,7)
    blocks=[]
    for r in range(3):
        cols=[(3-c[i])//2 for i in range(r,len(c),3)]
        values=[]
        for u in product(range(-p,p+1,2),repeat=3):
            if margins([(p-v)//2 for v in u],cols):values.append(u)
        blocks.append(values)
    return blocks

def rows(c):
    p=len(c)//3
    for blocks in product(*options(c)):
        u=tuple(blocks[i%3][i//3] for i in range(9))
        energy=sum(v*v for v in u)
        if energy>16*p-7:continue # partner length-nine energy >= 9
        key=(energy,)+tuple(sum(u[i]*u[(i+s)%9] for i in range(9)) for s in range(1,5))
        yield key,u

def check(c,d):
    p=len(c)//3;start=time.perf_counter();table=defaultdict(list);counts=[0,0];matched=0;example=None
    for key,u in rows(c):table[key].append(u);counts[0]+=1
    for key,v in rows(d):
        counts[1]+=1
        target=(16*p+2-key[0],)+tuple(-2*p-x for x in key[1:])
        hits=table.get(target,[]);matched+=len(hits)
        if hits and example is None:example=[hits[0],v]
    return {'alternate_rows':counts,'matching_pairs':matched,'example':example,
            'empty_relaxation':matched==0,'seconds':time.perf_counter()-start}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['pilot','census']);a=parser.parse_args()
    cat=load('results/p5_branch_portfolio/canonical_branches.json');old=load('results/p5_classification/classification.json')
    start=time.perf_counter();output=[]
    indices=[0,2] if a.stage=='pilot' else range(len(cat))
    if a.stage=='census':
        pilot=load('results/residual_obstruction/pilot.json');assert pilot['estimated_full_seconds']<1200
    for i in indices:
        if time.perf_counter()-start>1200:raise TimeoutError('Unresolved: controller cap')
        result=check(cat[i]['first'],cat[i]['second'])
        result.update(rank=i+1,frozen_count=old[i]['canonical_pairs'])
        assert not result['empty_relaxation'] or result['frozen_count']==0
        output.append(result)
    elapsed=time.perf_counter()-start
    value={'complete':True,'cases':output,'seconds':elapsed,'worker_count':1,
           'estimated_memory_bytes':200_000_000,'estimated_output_bytes':2_000_000,
           'controller_limit_seconds':1200,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if a.stage=='pilot':value['estimated_full_seconds']=elapsed*len(cat)/len(output)*3
    save(a.stage+'.json',value)
    print(value if a.stage=='pilot' else {'cases':len(output),'rejected':sum(r['empty_relaxation'] for r in output),'seconds':elapsed})

if __name__=='__main__':main()
