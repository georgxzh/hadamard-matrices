from itertools import product
from random import Random
import pytest

from scripts.primitive_local_audit import load, red
from scripts.compression_residue import (folded_balances, restricted_domain,
    cancelling_barycenter)
from scripts.residue_formula import build_model, histograms


def test_full_domain_equivalence_on_integer_compression_lattice():
    # Random integer rectangular moves preserve BOTH exact compression maps.
    # Check against the independent standard cyclotomic reduction, not A alone.
    rng = Random(20261015)
    saw = set()
    for scale in (1, 3, 9):
        for _ in range(30):
            h = [[0]*9 for _ in range(5)]
            for _ in range(20):
                r, t = rng.sample(range(5), 2)
                e = rng.randrange(9); f = (e+3) % 9
                n = scale*rng.randrange(-3, 4)
                h[r][e] += n; h[r][f] -= n
                h[t][e] -= n; h[t][f] += n
            b = [h[s % 5][2*s % 9] for s in range(45)]
            assert not any(folded_balances(b))
            actual = all(x % 9 == 0 for x in red(b))
            assert restricted_domain(b) == actual
            saw.add(actual)
    assert saw == {False, True}


def test_saved_domain_and_modular_compression_counterexamples():
    saved = load('results/residue_formula/audit.json')['mod_nine_records']
    h = next(h for h in saved if h['masks'][0] == 31210651353580)
    assert h['J'] == [0, 0, 1, 1]
    assert all(x % 3 == 0 for x in folded_balances(h['balance']))
    with pytest.raises(ValueError, match='length-nine'):
        restricted_domain(h['balance'])
    cat = load('results/p5_branch_portfolio/canonical_branches.json')[278]
    m = build_model([cat['first'], cat['second']])
    outside = load('results/primitive_local/audit.json')['saved_false_positive']
    b = histograms(m, outside['phases'])
    assert not any(folded_balances(b))
    assert not restricted_domain(b)


def test_barycenter_uses_real_phases_and_exact_uniform_differences():
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    for rank, opposite in ((277, (1, 2)), (279, (2, 3))):
        c = cat[rank-1]; cs = [c['first'], c['second']]
        design = cancelling_barycenter(cs, opposite)
        phases = design['phases']; m = build_model(cs)
        assert len(phases) == 27
        sums = [0]*45
        for x in phases:
            assert x[0] == x[1] == x[12] == 0
            for s, b in enumerate(histograms(m, x)):
                sums[s] += b
        assert sums == [0]*45
        for side, positions in enumerate(m['active']):
            offset = 0 if side == 0 else 12
            forced = (0, 1) if side == 0 else opposite
            for u, v in product(range(len(positions)), repeat=2):
                if u >= v:
                    continue
                counts = [sum((x[offset+v]-x[offset+u]) % 3 == d for x in phases)
                          for d in range(3)]
                assert counts == ([27, 0, 0] if (positions[u], positions[v]) == forced
                                  else [9, 9, 9])


def test_saved_new_audit_cross_checks_and_no_conditional_design_members():
    audit = load('results/compression_residue/audit.json')
    assert len(audit['saved_records_checked']) == 7
    for d in audit['barycenters']:
        assert d['exact_compression_members'] == d['full_9O_members'] == 0
        assert all(not any(v) for v in d['sums'].values())
    strong = next(r for r in audit['saved_records_checked'] if r['masks'][0] == 442312790436)
    assert strong['G'] == [0]*9 and strong['J'] == [1, 0, 2, 2]
    assert strong['compression_paf_with_energy'] == [82]+[-10]*8
