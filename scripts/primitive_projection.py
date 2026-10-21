"""Exact primitive-frequency projection; no phase search or new obstruction."""
from scripts.primitive_local_audit import red,mul,conj


def ramanujan_9p(d,p):
    return 9*p*int(d%(9*p)==0)-3*p*int(d%(3*p)==0)-9*int(d%9==0)+3*int(d%3==0)


def projection(b,p):
    if len(b)!=9*p or any(sum(b[r::3*p]) for r in range(3*p)):
        raise ValueError('exact first homogeneous compression required')
    g=[sum(b[t::9]) for t in range(9)]
    e=[p*x-g[s%9] for s,x in enumerate(b)]
    minima=[min(b[r::3*p]) for r in range(3*p)]
    positive=[x-minima[s%(3*p)] for s,x in enumerate(b)]
    w=p*sum(x*x for x in b)-sum(x*x for x in g)
    assert all(x>=0 for x in positive)
    assert all(min(positive[r::3*p])==0 for r in range(3*p))
    assert all(sum(e[r::3*p])==0 for r in range(3*p))
    assert all(sum(e[t::9])==0 for t in range(9))
    assert sum(x*x for x in e)==p*w and w>=0
    return {'B':b,'G':g,'E':e,'minimum_by_triple':minima,'R':positive,'W':w,
            'nine_periodic':all(b[s]==b[s%9] for s in range(9*p)),
            'R_is_sum_of_p_cycles':all(positive[s]==positive[s%9] for s in range(9*p))}


def check45(b):
    out=projection(b,5);s=red(b)
    assert red(out['R'])==s and red(out['E'])==[5*x for x in s]
    n=mul(s,conj(s))
    trace=sum(x*ramanujan_9p(i,5) for i,x in enumerate(n))
    assert trace==9*out['W']
    assert (not any(s))==out['nine_periodic']==out['R_is_sum_of_p_cycles']==(out['W']==0)
    if not any(out['G']):assert (not any(s))==(not any(b))
    return {**out,'S':s,'full_9O':all(x%9==0 for x in s),'trace_norm':trace}
