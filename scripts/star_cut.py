"""Signed support cuts, before any division by nine. No phase search."""
from scripts.primitive_local_audit import red
from scripts.event_compression_products import indicator
from src.legendre import _reduce_mod_monic


def residue(polynomial, prime=5):
    """Reduction in F3[x]/Phi_p(x), not division by 9 or a J residue."""
    a = list(_reduce_mod_monic(polynomial, [1]*prime))
    return [(a[i] if i < len(a) else 0) % 3 for i in range(prime-1)]


def signed_counts(row, subset=None, prime=5):
    active = [i for i,c in enumerate(row) if abs(c) == 1]
    indices = active if subset is None else list(subset)
    assert set(indices) <= set(active)
    out = [0]*prime
    for i in indices:
        out[i % prime] += row[i]
    return out


def support_cut(row, subset, prime=5):
    """Integer signed difference counts; no phases or modular averaging."""
    active = [i for i,c in enumerate(row) if abs(c) == 1]
    subset = set(subset)
    assert subset <= set(active)
    w = [0]*prime
    for i in sorted(subset):
        for j in active:
            if j not in subset:
                w[(j-i) % prime] += row[i]*row[j]
                w[(i-j) % prime] += row[i]*row[j]
    return w


def cut_polynomial(row, phases, subset):
    """Exact length-45 cross terms, with integer differences before wrap."""
    active = [i for i,c in enumerate(row) if abs(c) == 1]
    assert len(phases) == len(active)
    phase = dict(zip(active,phases)); subset = set(subset)
    assert subset <= set(active)
    out = [0]*45
    for i in sorted(subset):
        for j in active:
            if j not in subset:
                n = j-i+15*(phase[j]-phase[i])
                out[n % 45] += row[i]*row[j]
                out[-n % 45] += row[i]*row[j]
    return out


def event_cut(selectors, phases):
    """Same cut from original carry-aware Y events, including reverse shifts."""
    out = [0]*45
    for e in selectors:
        w = e['weight']*indicator(e['event'],phases)
        out[e['shift']] += w
        out[-e['shift'] % 45] += w
    return out


def folded(a):
    return [sum(a[t::9]) for t in range(9)]


def cut_norm(row, phases, subset):
    return red(cut_polynomial(row,phases,subset))
