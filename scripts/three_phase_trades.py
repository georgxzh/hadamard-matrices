"""All-sign, exactly-three landing-label trades. No multistep search."""
from itertools import combinations, product
from scripts.primitive_local_audit import POW, mul
from scripts.phase_exchange import sub


def flow_type(signs, old, new):
    arcs=[(a,b) if c==1 else (b,a) for c,a,b in zip(signs,old,new)]
    if any(a==b for a,b in arcs):return None
    if sorted(a for a,b in arcs)!=[0,1,2] or sorted(b for a,b in arcs)!=[0,1,2]:return None
    steps={(b-a)%3 for a,b in arcs}
    if len(steps)!=1:return None
    epsilon=next(iter(steps));epsilon=1 if epsilon==1 else -1
    return {'epsilon':epsilon,'tails':[a for a,b in arcs],
            'type':'equal_sign' if len(set(signs))==1 else 'mixed_sign'}


def candidates(cs,phases):
    offset=0
    for side,row in enumerate(cs):
        active=[i for i,c in enumerate(row) if abs(c)==1]
        index={i:offset+k for k,i in enumerate(active)}
        for positions in combinations(active,3):
            ids=[index[i] for i in positions]; signs=[row[i] for i in positions]
            old=[(i//3+5*phases[u])%3 for i,u in zip(positions,ids)]
            for increments in product((1,2),repeat=3):
                move={'side':side,'positions':list(positions),'phase_indices':ids,
                      'increments':list(increments),'signs':signs,'old_labels':old}
                new=[(q+5*d)%3 for q,d in zip(old,increments)]
                balance=[[0]*3 for _ in range(3)]
                for i,c,a,b in zip(positions,signs,old,new):
                    balance[i%3][a]-=c;balance[i%3][b]+=c
                preserved=not any(v for row0 in balance for v in row0)
                classified=None
                if len({i%3 for i in positions})==1:
                    classified=flow_type(signs,old,new)
                assert preserved == (classified is not None)
                if not preserved:
                    yield {**move,'status':'charges_change'};continue
                if any(u in (0,1,12) for u in ids):
                    yield {**move,'status':'gauge_violation'};continue
                out=list(phases)
                for u,d in zip(ids,increments):out[u]=(out[u]+d)%3
                yield {**move,'status':'permitted','new_labels':new,'flow':classified,'phases':out}
        offset+=len(active)


def thin_hypotheses(row,charges):
    groups=[[i for i,c in enumerate(row) if abs(c)==1 and i%3==r] for r in range(3)]
    records=[]
    for r,group in enumerate(groups):
        if len(group)!=3:continue
        signs=[row[i] for i in group];energy=sum(x*x for x in charges[r])
        minimum=3 if len(set(signs))==1 else 1
        records.append({'residue':r,'positions':group,'signs':signs,'charges':charges[r],
                        'energy':energy,'balanced_energy':minimum,'uneven':energy>minimum})
    sparse=all(len(g)<=5 for g in groups)
    return {'group_sizes':list(map(len,groups)),'at_most_five':sparse,'thin_groups':records,
            'uniform_structural_hypothesis':sparse and any(x['uneven'] for x in records)}


def delta_f(row,old_phases,move):
    out=[0]*24
    for i,u,d in zip(move['positions'],move['phase_indices'],move['increments']):
        part=mul(POW[(i+15*old_phases[u])%45],sub(POW[15*d],POW[0]))
        out=[x+row[i]*y for x,y in zip(out,part)]
    return out


def landing_delta_f(row,move):
    out=[0]*24;r=move['positions'][0]%3
    for i,a,b in zip(move['positions'],move['old_labels'],move['new_labels']):
        part=mul(POW[(36*i)%45],sub(POW[(30*b)%45],POW[(30*a)%45]))
        out=[x+row[i]*y for x,y in zip(out,part)]
    return mul(POW[10*r],out)
