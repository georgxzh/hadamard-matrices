"""Closed signed occupancy counts and indexed transport; no phase search."""
from math import factorial


def occupancy_count(positive, negative, residual):
    if sum(residual) != positive-negative or sum(map(abs,residual)) > positive+negative:
        return 0
    k=(positive+negative-sum(map(abs,residual)))//2
    total=0
    for k0 in range(k+1):
        for k1 in range(k-k0+1):
            ks=(k0,k1,k-k0-k1); denominator=1
            for r,j in zip(residual,ks):
                denominator*=factorial(max(r,0)+j)*factorial(max(-r,0)+j)
            total+=factorial(positive)*factorial(negative)//denominator
    return total


def fiber_count(cs,charges,pins=(0,1,12)):
    """All gauged assignments at M, not full-9O or Legendre solutions."""
    offset=0; count=1; groups=[]
    for side,row in enumerate(cs):
        active=[i for i,c in enumerate(row) if abs(c)==1]
        index={i:offset+j for j,i in enumerate(active)}
        for r in range(3):
            fixed=[0]*3;pos=neg=0
            for i in active:
                if i%3!=r:continue
                if index[i] in pins:fixed[(i//3)%3]+=row[i]
                elif row[i]==1:pos+=1
                else:neg+=1
            m=charges[side]['charges'][r]
            residual=[a-b for a,b in zip(m,fixed)]
            n=occupancy_count(pos,neg,residual);count*=n
            groups.append({'side':side,'residue':r,'positive_free':pos,'negative_free':neg,
                           'fixed_charge':fixed,'residual':residual,'count':n})
        offset+=len(active)
    return {'count':count,'groups':groups,'scope':'All gauge-respecting assignments at M; no primitive-domain filtering.'}


def transport(source,target,phases):
    assert source[0]==target[0] and len(source[0])==15
    old=source[1];new=target[1]
    active_old=[i for i,c in enumerate(old) if abs(c)==1]
    active_new=[i for i,c in enumerate(new) if abs(c)==1]
    offset=sum(abs(c)==1 for c in source[0]); indices={i:offset+j for j,i in enumerate(active_old)}
    mapped={};records=[]
    for r in range(3):
        assert sum(1 if old[i]>0 else -1 for i in range(r,15,3))==sum(1 if new[i]>0 else -1 for i in range(r,15,3))
        for sign in (-1,1):
            aa=[i for i in active_old if i%3==r and old[i]==sign]
            bb=[i for i in active_new if i%3==r and new[i]==sign]
            assert len(aa)==len(bb)
            for i,j in zip(aa,bb):
                nu=(2*(i//3-j//3))%3
                d=j-i+15*nu;assert d%9==0
                mapped[j]=(phases[indices[i]]+nu)%3
                records.append({'old':i,'new':j,'sign':sign,'nu':nu,'integer_displacement':d,'k_mod5':(d//9)%5})
    before=list(phases[:offset])+[mapped[j] for j in active_new]
    anchor=before[offset]
    after=list(before[:offset])+[(a-anchor)%3 for a in before[offset:]]
    assert all(after[j]==0 for j in (0,1,12))
    return {'phases':after,'before_anchor_normalization':before,'anchor_subtracted':anchor,
            'compressed_row_shift_mod9':(-15*anchor)%9,'mapping':sorted(records,key=lambda x:x['old'])}


def row_paf(row):
    return [sum(row[i]*row[(i+s)%len(row)] for i in range(len(row))) for s in range(len(row))]
