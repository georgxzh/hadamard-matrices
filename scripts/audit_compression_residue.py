"""Bounded proof cross-checks and saved-witness challenges, one worker."""
import argparse
import hashlib
import json
import time

from scripts.primitive_local_audit import ROOT, load, phase_norm
from scripts.residue_formula import build_model, formula
from scripts.compression_residue import (folded_balances, compressed_charges,
    charge_paf, restricted_domain, cancelling_barycenter)
from scripts.audit_fiber_structure import compress, paf
from src.ternary_phase import PhaseRow

BASE = 'aff70e5307492a65b61fddfabed92634edb6788f'
OUT = ROOT/'results/compression_residue'


def save(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n',
                          encoding='utf8', newline='\n')


def check(cs, phases):
    m = build_model(cs)
    _, s = phase_norm(cs, phases)
    f = formula(m, phases, s)
    b = f['balance']; g = folded_balances(b)
    assert g[0]+2*g[3] == 0 and g[1]+g[2]+g[4] == 0
    assert all(g[r] == g[9-r] for r in range(1, 9))
    assert g[0] == 2*(b[9]+b[18])
    assert g[1] == sum(b[i] for i in (1, 8, 10, 17, 19))
    assert g[2] == sum(b[i] for i in (2, 7, 11, 16, 20))
    assert sum(f['Q']) == 5*sum(b[i] for i in (1, 4, 6))+g[0]//2+g[2]
    charges = compressed_charges(cs, phases)
    p9 = [charge_paf(charges, shift) for shift in range(9)]
    offset = 0
    decoded = []
    masks = []
    for side, c in enumerate(cs):
        row = PhaseRow(c)
        x = row.decode(phases[offset:offset+len(row.active)])
        offset += len(row.active)
        masks.append(sum(1 << i for i, v in enumerate(x) if v == -1))
        decoded.append(compress(x, 9))
        assert list(decoded[-1]) == charges[side]['row']
    direct = [sum(v*v for x in decoded for v in x)] + [sum(v) for v in zip(*map(paf, decoded))]
    assert direct == p9
    assert p9 == [82+4*g[0]] + [-10+4*g[r] for r in range(1, 9)]
    exact = not any(g)
    if exact:
        assert restricted_domain(b) == f['in_domain']
        if f['in_domain']:
            a = sum(b[i]//3 for i in (1, 4, 6))
            assert f['J'][2] == (f['J'][0]+a) % 3
    return {**f, 'phases': phases, 'masks': masks, 'norm_defect': s,
            'compression_charges': charges, 'compression_paf_with_energy': p9,
            'G': g, 'exact_length_nine': exact,
            'triple_congruences_mod9': all((b[r]-b[r+15]) % 9 == 0 and
                (b[r]-b[r+30]) % 9 == 0 for r in range(15)),
            'moments': all(x % 3 == 0 for x in b)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['pilot', 'audit'])
    args = parser.parse_args()
    start = time.perf_counter()
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    saved = load('results/residue_formula/audit.json')['mod_nine_records']
    old = load('results/primitive_local/audit.json')['saved_false_positive']
    saved = saved + [{'rank': 279, **old}]
    if args.stage == 'audit':
        assert load('results/compression_residue/pilot.json')['estimate_seconds_5x'] < 60
    records = []
    for h in saved[:3] if args.stage == 'pilot' else saved:
        c = cat[h['rank']-1]
        r = check([c['first'], c['second']], h['phases'])
        assert r['masks'] == h['masks']
        records.append({'rank': h['rank'], **r})
        assert time.perf_counter()-start < 60
    if args.stage == 'pilot':
        seconds = time.perf_counter()-start
        out = {'records': len(records), 'seconds': seconds,
               'estimate_seconds_5x': seconds*61/len(records)*5,
               'workers': 1, 'cap_seconds': 60, 'memory_estimate_bytes': 100_000_000,
               'storage_estimate_bytes': 1_000_000}
        save('pilot.json', out); print(out); return
    # Saved counterexamples were evaluated first. This fixed 27-point design
    # then verifies the analytic barycenter; it is not a lifting search.
    designs = []
    for rank, opposite in ((277, (1, 2)), (279, (2, 3))):
        c = cat[rank-1]; cs = [c['first'], c['second']]
        design = cancelling_barycenter(cs, opposite)
        witnesses = []
        for phases in design['phases']:
            assert time.perf_counter()-start < 60
            witnesses.append(check(cs, phases))
        sums = {key: [sum(w[key][i] for w in witnesses) for i in range(n)]
                for key, n in (('balance',45), ('G',9), ('Q',4), ('norm_defect',24))}
        assert all(not any(v) for v in sums.values())
        designs.append({'rank': rank, **design, 'witnesses': witnesses, 'sums': sums,
                        'exact_compression_members': sum(w['exact_length_nine'] for w in witnesses),
                        'full_9O_members': sum(w['in_domain'] for w in witnesses),
                        'scope': 'Convex barycenter only; no pointwise conditional solution asserted.'})
    out = {'base_commit': BASE, 'saved_records_checked': records, 'barycenters': designs,
           'seconds': time.perf_counter()-start, 'workers': 1, 'caps_hit': False,
           'source_hashes': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in (
               'scripts/compression_residue.py', 'scripts/audit_compression_residue.py',
               'results/residue_formula/audit.json', 'results/primitive_local/audit.json',
               'results/p5_branch_portfolio/canonical_branches.json')}}
    save('audit.json', out)
    print({'seconds': out['seconds'], 'saved_checks': len(records), 'new_design_checks': 54})
    for r in records:
        print({k: r[k] for k in ('rank','masks','G','Q','J','exact_length_nine','triple_congruences_mod9')})
    for d in designs:
        print({k: d[k] for k in ('rank','sums','exact_compression_members','full_9O_members')})


if __name__ == '__main__':
    main()
