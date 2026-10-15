"""Exact length-nine balances and an analytic affine-certificate limitation.

No census, solver, or independent phase-space search. Existing artifacts are
read only. The barycenter is NOT a conditional lifting solution.
"""
from itertools import product

from scripts.residue_formula import tensor_coefficients


def folded_balances(b):
    return [sum(b[r::9]) for r in range(9)]


def compressed_charges(cs, phases):
    """Signed minority charges; the original index and layer carry are retained."""
    offset = 0
    out = []
    for c in cs:
        beta = [sum(1 if c[i] > 0 else -1 for i in range(r, 15, 3)) for r in range(3)]
        charges = [[0]*3 for _ in range(3)]
        for i, sign in enumerate(c):
            if abs(sign) == 1:
                q = (i//3 + 5*phases[offset]) % 3
                charges[i % 3][q] += sign
                offset += 1
        row = [beta[r]-2*charges[r][q] for q in range(3) for r in range(3)]
        out.append({'beta': beta, 'charges': charges, 'row': row})
    assert offset == len(phases)
    return out


def charge_paf(charges, shift):
    """Expand all integer terms, including the residue-three boundary carry."""
    total = 0
    for record in charges:
        beta, m = record['beta'], record['charges']
        for r in range(3):
            h, rp = divmod(r+shift, 3)
            for q in range(3):
                qp = (q+h) % 3
                total += (beta[r]*beta[rp] - 2*beta[r]*m[rp][qp]
                          - 2*beta[rp]*m[r][q] + 4*m[r][q]*m[rp][qp])
    return total


def restricted_domain(b):
    """Equivalent full-9O test ONLY under both exact compression hypotheses."""
    if len(b) != 45 or any(sum(b[r::15]) for r in range(15)):
        raise ValueError('exact length-15 balances required')
    if any(folded_balances(b)):
        raise ValueError('exact length-nine balances required')
    congruent = all((b[r]-b[r+15]) % 9 == 0 and (b[r]-b[r+30]) % 9 == 0
                    for r in range(15))
    full = all(a % 9 == 0 for row in tensor_coefficients(b) for a in row)
    assert congruent == full
    if full:
        assert all(x % 3 == 0 for x in b)
    return full


def cancelling_barycenter(cs, opposite_positions):
    """27 genuine gauged assignments; their mean B is zero, not their B's.

    C has fixed adjacent equal-sign anchors (0,1). D has an opposite-weight
    adjacent active edge. All other within-row differences are uniform.
    Projective directions in F3^3 supply pairwise independent phases.
    """
    active = [[i for i, c in enumerate(row) if abs(c) == 1] for row in cs]
    assert active[0][:2] == [0, 1]
    u, v = opposite_positions
    assert v-u == 1 and u in active[1] and v in active[1]
    assert cs[0][0]*cs[0][1] == -cs[1][u]*cs[1][v]
    directions = [d for d in product(range(3), repeat=3)
                  if any(d) and next(x for x in d if x) == 1]
    maps = []
    for side, positions in enumerate(active):
        fixed = set(positions[:2] if side == 0 else positions[:1])
        if side == 1 and (u in fixed or v in fixed):
            fixed.update((u, v))
        mapping, labels = {}, {}
        for i in positions:
            if i in fixed:
                mapping[i] = (0, 0, 0)
            else:
                key = u if side == 1 and i in (u, v) else i
                if key not in labels:
                    labels[key] = directions[len(labels)]
                mapping[i] = labels[key]
        maps.append(mapping)
    phases = [[sum(x*y for x, y in zip(maps[side][i], seed)) % 3
               for side in range(2) for i in active[side]]
              for seed in product(range(3), repeat=3)]
    assert all(x[0] == x[1] == x[len(active[0])] == 0 for x in phases)
    return {'opposite_positions': [u, v],
            'directions_by_active_index': [[list(maps[s][i]) for i in active[s]] for s in range(2)],
            'phases': phases}
