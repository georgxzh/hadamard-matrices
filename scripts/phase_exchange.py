"""Landing-label exchanges and exact norm differences, with no search engine."""
from itertools import combinations

from scripts.primitive_local_audit import POW, mul, conj


def add(*args):
    return [sum(xs) for xs in zip(*args)]


def sub(a,b):
    return [x-y for x,y in zip(a,b)]


def exchanges(cs, phases, fixed=(0,1,12)):
    """Exactly 121 raw pairs for the two prescribed rows; no second-step moves."""
    offset = 0
    for side,row in enumerate(cs):
        active = [i for i,c in enumerate(row) if abs(c) == 1]
        index = {i:offset+k for k,i in enumerate(active)}
        for i,j in combinations(active,2):
            move = {'side':side,'positions':[i,j],'phase_indices':[index[i],index[j]]}
            if i%3 != j%3 or row[i] != row[j]:
                yield {**move,'status':'residue_or_sign_mismatch'}; continue
            u,v = index[i],index[j]
            qi,qj = (i//3+5*phases[u])%3, (j//3+5*phases[v])%3
            new = list(phases)
            new[u],new[v] = 2*(qj-i//3)%3, 2*(qi-j//3)%3
            move.update({'labels':[qi,qj],'old_phases':[phases[u],phases[v]],
                         'new_phases':[new[u],new[v]]})
            if any(new[k] != phases[k] for k in fixed):
                yield {**move,'status':'gauge_violation'}; continue
            if new == list(phases):
                yield {**move,'status':'noop'}; continue
            yield {**move,'status':'permitted','phases':new}
        offset += len(active)


def delta_factor(row, move):
    i,j = move['positions']; qi,qj = move['labels']
    # gamma=zeta^36, t=zeta^5, omega=zeta^15. Integers before exponent wrap.
    out = mul(POW[(10*(i%3))%45],sub(POW[(36*i)%45],POW[(36*j)%45]))
    out = mul(out,sub(POW[(30*qj)%45],POW[(30*qi)%45]))
    return [row[i]*x for x in out]


def delta_factor_offset(row, move):
    i,j = move['positions']; a,b = move['old_phases']; d=(j-i)//3
    out = mul(POW[i],sub(POW[0],POW[(18*d)%45]))
    out = mul(out,sub(POW[(15*(b-d))%45],POW[15*a]))
    return [row[i]*x for x in out]


def norm_change(f, delta):
    return add(mul(delta,conj(f)),mul(f,conj(delta)),mul(delta,conj(delta)))


def affected_delta(model, old, new):
    changed = {i for i,(a,b) in enumerate(zip(old,new)) if a != b}
    counts = []; difference = []
    for edges in model['edges']:
        relevant = [(w,u,v,h) for w,u,v,h in edges if u in changed or v in changed]
        counts.append(len(relevant))
        difference.append(sum(w*(int((new[v]-new[u]-h)%3 == 0)
                                 -int((old[v]-old[u]-h)%3 == 0)) for w,u,v,h in relevant))
    return difference,counts
