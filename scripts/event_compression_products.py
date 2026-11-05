"""Exact event/compression products and signed dipole response formulas.

The probability calculations below describe a named relaxation distribution,
never membership in the conditional lifting fiber or in 9Z[zeta].
"""
from collections import defaultdict
from fractions import Fraction

from scripts.residue_formula import build_model, SETS, binomial


def models(cs, pair):
    m = build_model(cs)
    offset = len(m['active'][0]); u, v = pair
    index = {p: offset+j for j,p in enumerate(m['active'][1])}
    selectors = []
    for k in m['active'][1]:
        if k in pair:
            continue
        for endpoint in pair:
            r = (k-endpoint) % 15
            carry = (endpoint+r)//15
            for d in range(3):
                layer = (d-carry) % 3
                selectors.append({'positions': [endpoint,k], 'phase_difference': d,
                    'weight': cs[1][endpoint]*cs[1][k], 'base_shift': r,
                    'carry': carry, 'layer': layer, 'shift': r+15*layer,
                    'event': [index[endpoint],index[k],carry+layer],
                    'core': k == v+1})
    forms = []
    for t in range(3):
        shifts = list(range(t,45,9))
        forms.append({'constant': -sum(m['target'][s] for s in shifts),
                      'terms': [[w,a,b,h,s] for s in shifts for w,a,b,h in m['edges'][s]]})
    assert len(selectors) == 54 and sum(e['core'] for e in selectors) == 6
    return m, selectors, forms


def indicator(e, phases):
    a,b,h = e
    return int((phases[b]-phases[a]-h) % 3 == 0)


def expand_value(selector, form, phases):
    """c*Y_e + sum w_f*Y_e*Y_f, with INTEGER coefficients."""
    y = indicator(selector['event'], phases)
    return form['constant']*y + sum(w*y*indicator((a,b,h),phases)
                                   for w,a,b,h,_ in form['terms'])


def contract(form, selector):
    """On Y_e=1 replace a_v by a_u+d; keep signs and integer offsets first."""
    u,v,d = selector['event']
    c = form['constant']; terms = defaultdict(int)
    for w,a,b,h,_ in form['terms']:
        aa, da = (u,d) if a == v else (a,0)
        bb, db = (u,d) if b == v else (b,0)
        hh = h-db+da
        if aa == bb:
            c += w*int(hh % 3 == 0)
        else:
            if aa > bb:
                aa,bb,hh = bb,aa,-hh
            terms[aa,bb,hh % 3] += w
    return {'constant': c, 'terms': [[w,a,b,h,-1] for (a,b,h),w in sorted(terms.items()) if w]}


def form_value(form, phases):
    return form['constant']+sum(w*indicator((a,b,h),phases) for w,a,b,h,_ in form['terms'])


def local_dipole(n, weight=1, length=45):
    """Cross terms of an opposite-sign adjacent pair and a third vertex."""
    b = [0]*length
    for sign, shift in ((weight,n),(-weight,n-1)):
        b[shift % length] += sign
        b[-shift % length] += sign
    return b


def q_of(b):
    return [sum(b[s] for s in SETS[4])-sum(b[s] for s in SETS[r]) for r in range(4)]


def conditional_response(cs, pair, k, d):
    """E[B | a_k-a_u=d] in the independent opposite-edge distribution.

    This is an exact rational expectation, NOT an actual defect array.
    """
    u,v = pair
    assert v == u+1 and cs[1][u] == -cs[1][v]
    w = cs[1][u]*cs[1][k]
    arrays = [local_dipole(k-u+15*j,w) for j in range(3)]
    response = [arrays[d][s]-Fraction(sum(a[s] for a in arrays),3) for s in range(45)]
    return {'B': response, 'G': [sum(response[t::9]) for t in range(3)], 'Q': q_of(response)}


def independent_factor_map(cs, pair):
    """Scalar independent F3 factors; -1 means the fixed zero anchor."""
    active = [[i for i,c in enumerate(row) if abs(c) == 1] for row in cs]
    labels = []; next_label = 0; u,v = pair
    for side, positions in enumerate(active):
        fixed = set(positions[:2] if side == 0 else positions[:1])
        if side == 1 and fixed.intersection(pair):
            fixed.update(pair)
        shared = {}
        for i in positions:
            if i in fixed:
                labels.append(-1)
            else:
                key = u if side == 1 and i in pair else i
                if key not in shared:
                    shared[key] = next_label; next_label += 1
                labels.append(shared[key])
    return labels, next_label


def event_probability(events, mapping, n):
    """Exact probability of <=2 linear events, via rank over F3; no enumeration."""
    rows = []
    for a,b,h in events:
        row = [0]*n+[h % 3]
        if mapping[a] >= 0:
            row[mapping[a]] -= 1
        if mapping[b] >= 0:
            row[mapping[b]] += 1
        rows.append([v % 3 for v in row])
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank,len(rows)) if rows[i][col]),None)
        if pivot is None:
            continue
        rows[rank],rows[pivot] = rows[pivot],rows[rank]
        inv = pow(rows[rank][col],-1,3)
        rows[rank] = [v*inv % 3 for v in rows[rank]]
        for i in range(rank+1,len(rows)):
            scale = rows[i][col]
            rows[i] = [(x-scale*y) % 3 for x,y in zip(rows[i],rows[rank])]
        rank += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        return Fraction(0)
    return Fraction(1,3**rank)


def product_expectation(selector, form, mapping, n):
    e = selector['event']
    return (form['constant']*event_probability([e],mapping,n)
            +sum(w*event_probability([e,(a,b,h)],mapping,n) for w,a,b,h,_ in form['terms']))


def carry_feedback(q, g, y):
    """Exact integer binomial identity, reduced only after evaluating carries.

    On g=0 the carry coordinate is unchanged. If 3|g, the difference is
    y*(g//3) modulo three, not generally zero merely because y*g=0 mod 3.
    """
    assert y in (0,1)
    rhs = y*(g*binomial(q,2)+binomial(g,2)*q+binomial(g,3))
    lhs = binomial(q+y*g,3)-binomial(q,3)
    assert lhs == rhs
    return rhs % 3
