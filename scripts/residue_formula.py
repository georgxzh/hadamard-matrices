"""Exact histogram and degree-six carry formula for (S/9) mod (1-zeta^5).

No phase enumeration. Read-only imports from previous research rounds.
"""
from math import factorial
from src.legendre import _reduce_mod_monic, check_compressed_legendre_constants
from scripts.primitive_local_audit import phase_norm, POW


SETS = ((30,35,40),(21,26,31),(12,17,22),(3,8,13),(4,39,44))


def binomial(n,k):
    value=1
    for j in range(k):value*=n-j
    return value//factorial(k)


def residue_basis(coefficients):
    """Standard zeta power-basis route. Reject division outside its domain."""
    if any(x%9 for x in coefficients):raise ValueError('S is not in 9O')
    out=list(_reduce_mod_monic([x//9 for x in coefficients],[1]*5))
    return [(out[i] if i<len(out) else 0)%3 for i in range(4)]


def tensor_coefficients(polynomial):
    """Exact gamma=zeta^36, t=zeta^5 basis, gamma^r*t^v, r<4,v<6."""
    h=[[0]*9 for _ in range(5)]
    for s,b in enumerate(polynomial):h[s%5][(2*s)%9]+=b
    out=[]
    for r in range(4):
        d=[h[r][v]-h[4][v] for v in range(9)]
        out.append([d[v]-d[6+v%3] for v in range(6)])
    return out


def tensor_to_standard(tensor):
    return [sum(tensor[r][v]*POW[(36*r+5*v)%45][k]
                for r in range(4) for v in range(6)) for k in range(24)]


def build_model(cs):
    if len(cs)!=2 or any(len(c)!=15 for c in cs):raise ValueError('length-15 pair required')
    if not check_compressed_legendre_constants(*cs,3).ok:raise ValueError('invalid fixed intermediate pair')
    active=[[i for i,c in enumerate(row) if abs(c)==1] for row in cs]
    offsets=(0,len(active[0]));target=[0]*45;edges=[[] for _ in range(45)]
    for r in range(1,15):
        constant=0;terms=[]
        for side,c in enumerate(cs):
            index={i:offsets[side]+k for k,i in enumerate(active[side])}
            for i in range(15):
                h,j=divmod(i+r,15)
                bi=1 if c[i]>0 else -1;bj=1 if c[j]>0 else -1
                di=-2*bi if i in index else 0;dj=-2*bj if j in index else 0
                constant+=3*bi*bj+di*bj+bi*dj
                if di and dj:terms.append((bi*bj,index[i],index[j],h))
        assert (-2-constant)%4==0
        t=(-2-constant)//4
        assert sum(w for w,_,_,_ in terms)==3*t
        for ell in range(3):
            s=r+15*ell;target[s]=t
            edges[s]=[(w,u,v,h+ell) for w,u,v,h in terms]
    coordinates=[]
    for k in range(4):
        c=0;events=[]
        for sign,shifts in ((1,SETS[4]),(-1,SETS[k])):
            for s in shifts:
                c-=sign*target[s]
                events.extend((sign*w,u,v,h) for w,u,v,h in edges[s])
        coordinates.append((c,events))
    return {'active':active,'size':sum(map(len,active)), 'target':target,
            'edges':edges,'coordinates':coordinates}


def histograms(m,phases):
    assert len(phases)==m['size'] and all(x in (0,1,2) for x in phases)
    b=[]
    for t,events in zip(m['target'],m['edges']):
        b.append(sum(w for w,u,v,h in events if (phases[v]-phases[u]-h)%3==0)-t)
    assert b[0]==b[15]==b[30]==0
    assert all(b[s]==b[45-s] for s in range(1,45))
    assert all(sum(b[r::15])==0 for r in range(15))
    return b


def carry_polynomial(coordinate,phases):
    """Evaluate a genuine F3 polynomial, retaining terms through formal degree 3.

    Each event indicator is quadratic in phase variables; output degree <=6.
    This implementation never divides a variable value modulo three.
    """
    constant,events=coordinate
    p=[binomial(constant,k)%3 for k in range(4)]
    for sign,u,v,h in events:
        y=(1-(phases[v]-phases[u]-h)**2)%3
        factor=[1,sign*y,y if sign<0 else 0,-y if sign<0 else 0]
        p=[sum(p[j]*factor[k-j] for j in range(k+1))%3 for k in range(4)]
    return p[3]


def formula(m,phases,coefficients=None):
    b=histograms(m,phases)
    tensor=tensor_coefficients(b)
    q=[sum(b[s] for s in SETS[4])-sum(b[s] for s in SETS[k]) for k in range(4)]
    poly=[carry_polynomial(c,phases) for c in m['coordinates']]
    assert poly==[(x//3)%3 for x in q]
    in_domain=all(x%9==0 for r in tensor for x in r)
    if coefficients is not None:
        assert tensor_to_standard(tensor)==list(coefficients)
        assert in_domain==all(x%9==0 for x in coefficients)
    j=None
    if in_domain:
        assert all(x%3==0 for x in q)
        j=[(x//3)%3 for x in q]
        assert j==[sum(x//9 for x in r)%3 for r in tensor]
        assert j==poly
        if coefficients is not None:assert j==residue_basis(coefficients)
        assert j[1]==0 and j[2]==j[3]  # Real fixed subfield F9.
    return {'balance':b,'tensor':tensor,'Q':q,'polynomial_extension':poly,
            'in_domain':in_domain,'J':j}
