"""Challenge the margin obstruction with frozen matched branches, without relifting.

One serial worker. New output only; old census files are read-only inputs.
"""
from collections import defaultdict
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import time

from scripts.residual_compression_obstruction import ROOT, OUT, load, save, check, margins
from scripts.audit_fiber_structure import row, compress, paf, kernel_pair

BASE = 'be92dfea374da4d4b621452ac9e30776ec067a36'


def profile(cs):
    return tuple(tuple(sorted(c[r::3])) for c in cs for r in range(3))


def transfer(mask, source, target):
    """Permute columns within each CRT block, preserving length-nine sums."""
    n = len(source); length = 3*n; mapping = {}
    for r in range(3):
        unused = list(range(r, n, 3))
        for j in range(r, n, 3):
            k = next(k for k in unused if source[k] == target[j])
            mapping[j] = k; unused.remove(k)
    indices = {(i % n, i % 9): i for i in range(length)}
    assert len(indices) == length
    return sum(((mask >> indices[mapping[i % n], i % 9]) & 1) << i
               for i in range(length))


def third_gauge(pair, cs):
    active = [i for i, v in enumerate(cs[0]) if abs(v) == 1]
    i0 = active[0]; i1 = next(i for i in active if (i-i0) % 3)
    orbit = [kernel_pair(pair, cs, t) for t in range(3)]
    selected = [m for m in orbit if row(m[0], 3*len(cs[0]))[i1] == -cs[0][i1]]
    assert len(selected) == 1
    return selected[0]


def describe(pair, cs):
    p = len(cs[0])//3; xs = [row(m, 9*p) for m in pair]
    assert [compress(x, 3*p) for x in xs] == [tuple(c) for c in cs]
    us = [compress(x, 9) for x in xs]
    assert sum(v*v for u in us for v in u) == 16*p+2
    assert all(a+b == -2*p for a, b in zip(paf(us[0]), paf(us[1])))
    sums = [a+b for a, b in zip(paf(xs[0]), paf(xs[1]))]
    violations = [{'shift': i+1, 'paf_sum': v} for i, v in enumerate(sums) if v != -2]
    return {'masks': pair, 'alternate_compression': us, 'full_paf_violations': violations}


def matrix_check():
    """Independent exhaustive truth table: all 512 binary 3-by-3 matrices."""
    feasible = set()
    for bits in product((0, 1), repeat=9):
        feasible.add((tuple(sum(bits[3*i:3*i+3]) for i in range(3)),
                      tuple(sum(bits[j::3]) for j in range(3))))
    count = 0
    for r in product(range(4), repeat=3):
        for c in product(range(4), repeat=3):
            assert margins(r, c) == ((r, c) in feasible)
            count += 1
    return {'matrices': 512, 'degree_pairs': count, 'feasible_degree_pairs': len(feasible)}


def frozen_digest():
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'results'],
                                    cwd=ROOT, text=True).splitlines()
    # Git comparison establishes unchanged tracked contents; hash raw local bytes too.
    changed = subprocess.check_output(['git', 'diff', '--name-only', BASE, '--', *paths],
                                      cwd=ROOT, text=True) if len(paths) < 50 else subprocess.check_output(
        ['git', 'diff', '--name-only', BASE, '--', 'results'], cwd=ROOT, text=True)
    assert not set(changed.splitlines()).intersection(paths)
    h = hashlib.sha256()
    for name in paths:
        h.update((name+' '+hashlib.sha256((ROOT/name).read_bytes()).hexdigest()+'\n').encode())
    return {'files': len(paths), 'ordered_path_sha256_digest': h.hexdigest()}


def main():
    start = time.perf_counter(); baseline = frozen_digest()
    # Bounded p7 pilot precedes the four new portfolio projection checks.
    positive = load('results/p7_positive_control/witness.json')['pair']
    pilot = check(*positive)
    save('p7_pilot.json', {'positive_case': pilot, 'estimate_seconds_10x': 5*10*pilot['seconds'],
         'workers': 1, 'memory_estimate_bytes': 200_000_000, 'storage_estimate_bytes': 2_000_000,
         'controller_limit_seconds': 120})
    assert 5*10*pilot['seconds'] < 120
    p7 = [{'id': 'positive', **pilot}]
    for b in load('results/p7_portfolio/portfolio.json')['branches']:
        if time.perf_counter()-start > 120: raise TimeoutError('Unresolved audit cap')
        p7.append({'id': b['id'], **check(*b['pair'])})
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    old = load('results/p5_classification/classification.json')
    new = load('results/residual_obstruction/census.json')['cases']
    groups = defaultdict(list)
    for c, frozen, fresh in zip(cat, old, new, strict=True):
        assert c['rank'] == frozen['rank'] == fresh['rank']
        groups[profile([c['first'], c['second']])].append(c['rank'])
    mixed = [ranks for ranks in groups.values() if
             {old[r-1]['canonical_pairs'] > 0 for r in ranks} == {False, True}]
    for ranks in groups.values():
        assert len({new[r-1]['matching_pairs'] for r in ranks}) == 1
        assert len({tuple(new[r-1]['alternate_rows']) for r in ranks}) == 1
    cs = [[cat[r-1]['first'], cat[r-1]['second']] for r in (277, 279)]
    assert cs[0][0] == cs[1][0] and profile(cs[0]) == profile(cs[1])
    assert old[276]['canonical_pairs'] == 3 and old[278]['canonical_pairs'] == 0
    positive_pair = old[276]['solutions'][0]
    false_pair = tuple(transfer(m, c, d) for m, c, d in zip(positive_pair, cs[0], cs[1]))
    positive_description = describe(positive_pair, cs[0]); false_description = describe(false_pair, cs[1])
    assert not positive_description['full_paf_violations'] and false_description['full_paf_violations']
    assert positive_description['alternate_compression'] == false_description['alternate_compression']
    gauge_positive = describe(third_gauge(positive_pair, cs[0]), cs[0])
    gauge_false = describe(third_gauge(false_pair, cs[1]), cs[1])
    assert gauge_false['full_paf_violations'] and not gauge_positive['full_paf_violations']
    save('counterexample.json', {'positive_rank': 277, 'empty_rank': 279,
         'fixed_compressions': cs, 'shared_profile': profile(cs[0]),
         'positive': positive_description, 'false_positive': false_description,
         'third_gauge_positive': gauge_positive, 'third_gauge_false_positive': gauge_false,
         'alternate_matching_pairs': new[276]['matching_pairs'],
         'claim_refuted': 'Simultaneous binary feasibility plus all length-nine compressed LP equations implies liftability.'})
    assert baseline == frozen_digest()
    save('audit.json', {'complete': True, 'base_commit': BASE, 'frozen_results': baseline,
         'frozen_results_unchanged': True, 'p5_cases': len(new),
         'p5_empty_cases': sum(r['canonical_pairs'] == 0 for r in old),
         'p5_rejections': sum(r['empty_relaxation'] for r in new),
         'p7_cases': p7, 'profiles': len(groups), 'mixed_profile_groups': mixed,
         'matrix_truth_table': matrix_check(), 'seconds': time.perf_counter()-start,
         'python': platform.python_version(), 'platform': platform.platform(),
         'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope': 'Exact projection relaxation and counterexample audit; no new binary census or external replication.'})
    print(json.dumps({'p7_rejected': sum(r['empty_relaxation'] for r in p7), 'profiles': len(groups),
          'mixed_profiles': len(mixed), 'baseline': baseline, 'seconds': time.perf_counter()-start}))


if __name__ == '__main__': main()
