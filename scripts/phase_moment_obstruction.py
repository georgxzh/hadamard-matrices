"""Exploratory exact carry-sensitive moment equations over F_3.

Separate output from every frozen study; no binary re-enumeration.
"""
from pathlib import Path
from itertools import product
import hashlib
import json
import time
import argparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/phase_moments'


def load(name): return json.loads((ROOT/name).read_text())


def save(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf8', newline='\n')


def model(cs):
    n = len(cs[0]); active = [[i for i,c in enumerate(row) if abs(c)==1] for row in cs]
    offsets = [0, len(active[0])]; size = sum(map(len,active)); linear=[]; quadratic=[]
    for shift in range(1,n):
        constant=0; edges=[]
        for side,c in enumerate(cs):
            lookup={i:offsets[side]+k for k,i in enumerate(active[side])}
            signs=[1 if v>0 else -1 for v in c]
            for i in range(n):
                carry,j=divmod(i+shift,n)
                bi,bj=signs[i],signs[j]
                di=-2*bi if i in lookup else 0; dj=-2*bj if j in lookup else 0
                constant += 3*bi*bj+di*bj+bi*dj
                if di and dj: edges.append((lookup[i],lookup[j],carry,bi*bj))
        assert (-2-constant)%4==0
        target=(-2-constant)//4
        assert sum(e[3] for e in edges)==3*target
        equation=[0]*(size+1)
        for u,v,h,w in edges:
            equation[u]-=w; equation[v]+=w; equation[-1]+=w*h
        linear.append([v%3 for v in equation])
        quadratic.append({'shift':shift,'edges':edges,'target':2*target%3})
    # Independent layer translations and the third kernel gauge.
    second=next(k for k,i in enumerate(active[0]) if (i-active[0][0])%3)
    gauges=[0,second,offsets[1]]
    for index in gauges:
        eq=[0]*(size+1);eq[index]=1;linear.append(eq)
    return {'size':size,'n':n,'active':active,'gauges':gauges,'linear':linear,'quadratic':quadratic}


def rref(equations,size):
    a=[r.copy() for r in equations]; pivots=[]; k=0
    for j in range(size):
        found=next((i for i in range(k,len(a)) if a[i][j]%3),None)
        if found is None:continue
        a[k],a[found]=a[found],a[k]
        a[k]=[(v*pow(a[k][j],-1,3))%3 for v in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                c=a[i][j];a[i]=[(x-c*y)%3 for x,y in zip(a[i],a[k])]
        pivots.append(j);k+=1
    consistent=not any(not any(r[:size]) and r[-1] for r in a)
    return {'consistent':consistent,'rank':len(pivots),'pivots':pivots,
            'free':[i for i in range(size) if i not in pivots],'equations':a[:k]}


def recover(reduced,values,size):
    x=[0]*size
    for i,v in zip(reduced['free'],values):x[i]=v
    for p,e in zip(reduced['pivots'],reduced['equations']):
        x[p]=(e[-1]-sum(e[i]*x[i] for i in reduced['free']))%3
    return x


def quadratic_values(m,x):
    return [(sum(w*((x[v]-x[u]-h)%3)**2 for u,v,h,w in q['edges'])-q['target'])%3
            for q in m['quadratic']]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['pilot']);args=parser.parse_args()
    start=time.perf_counter();cat=load('results/p5_branch_portfolio/canonical_branches.json');out=[]
    for rank in (277,279):
        c=cat[rank-1];m=model([c['first'],c['second']]);r=rref(m['linear'],m['size'])
        example=None;tested=0
        if r['consistent']:
            for values in product(range(3),repeat=len(r['free'])):
                if tested==10000 or time.perf_counter()-start>10:break
                x=recover(r,values,m['size']);tested+=1
                if not any(quadratic_values(m,x)):example=x;break
        out.append({'rank':rank,'model':m,'linear_reduction':r,'bounded_assignments_tested':tested,
                    'modular_witness':example,'complete_modular_search':tested==3**len(r['free'])})
    save('pilot.json',{'cases':out,'seconds':time.perf_counter()-start,'workers':1,
         'time_cap_seconds':10,'assignment_cap_per_branch':10000,'memory_estimate_bytes':100_000_000,
         'storage_estimate_bytes':1_000_000,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print([{k:v for k,v in c.items() if k not in ('model','linear_reduction')} | {'linear_rank':c['linear_reduction']['rank'],'free_variables':len(c['linear_reduction']['free'])} for c in out])


if __name__=='__main__':main()
