from scripts.residual_compression_obstruction import load, rows, margins
from scripts.audit_residual_obstruction import matrix_check, transfer, third_gauge, describe
from scripts.audit_fiber_structure import row, compress, kernel_pair


def test_margin_criterion_against_all_small_matrices():
    assert matrix_check() == {'matrices': 512, 'degree_pairs': 4096, 'feasible_degree_pairs': 328}
    assert not margins([4, 0, 0], [1, 1, 1])
    assert not margins([2, 2, 0], [3, 1, 0])  # Equal totals are insufficient.


def test_matched_branches_have_identical_exact_projection_domains():
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    for side in ('first', 'second'):
        assert set(rows(cat[276][side])) == set(rows(cat[278][side]))


def test_counterexample_survives_every_kernel_element_and_third_gauge():
    record = load('results/residual_obstruction/counterexample.json')
    cs, ds = record['fixed_compressions']
    positive = record['positive']['masks']
    false = tuple(transfer(m, c, d) for m, c, d in zip(positive, cs, ds))
    assert list(false) == record['false_positive']['masks']
    assert [compress(row(m, 45), 9) for m in false] == [compress(row(m, 45), 9) for m in positive]
    for t in range(3):
        assert describe(kernel_pair(false, ds, t), ds)['full_paf_violations']
        assert not describe(kernel_pair(positive, cs, t), cs)['full_paf_violations']
    gauged = describe(third_gauge(false, ds), ds)
    assert list(gauged['masks']) == record['third_gauge_false_positive']['masks']
    assert gauged['full_paf_violations'][0] == {'shift': 2, 'paf_sum': -6}


def test_every_saved_projection_witness_has_exact_compatible_margins_and_paf():
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    records = load('results/residual_obstruction/census.json')['cases']
    cases = [([c['first'], c['second']], r) for c, r in zip(cat, records, strict=True)]
    p7 = load('results/residual_obstruction/audit.json')['p7_cases']
    cases += [(load('results/p7_positive_control/witness.json')['pair'], p7[0])]
    cases += [(b['pair'], r) for b, r in zip(load('results/p7_portfolio/portfolio.json')['branches'], p7[1:], strict=True)]
    for cs, result in cases:
        p = len(cs[0])//3; us = result['example']
        assert us is not None
        for c, u in zip(cs, us):
            assert sum(c) == sum(u) == 1
            for residue in range(3):
                assert margins([(p-v)//2 for v in u[residue::3]], [(3-v)//2 for v in c[residue::3]])
        assert sum(v*v for u in us for v in u) == 16*p+2
        for s in range(1, 9):
            assert sum(u[i]*u[(i+s)%9] for u in us for i in range(9)) == -2*p
