from scripts.primitive_local_audit import load, red, mul, conj
from scripts.star_cut import residue, signed_counts, support_cut


def test_cut_formula_from_two_independent_routes():
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    for rank,pair in ((277,(1,2)),(279,(2,3))):
        row = cat[rank-1]['second']
        a = red(signed_counts(row)); h = red(signed_counts(row,pair))
        r = [x-y for x,y in zip(a,h)]
        cross = [x+y for x,y in zip(mul(h,conj(r)),mul(conj(h),r))]
        w = support_cut(row,pair)
        assert residue(cross) == residue(w)
        assert any(residue(w))
        # The zero test in F3[x]/Phi_p is equal coefficients, not zero sum.
        assert sum(w) == 0
        assert not all((x-w[-1])%3 == 0 for x in w)


def test_saved_full_domain_counterexamples_to_local_division():
    rows = {x['masks'][0]:x for x in load('results/star_cut/audit.json')['saved_points']
            if not x['saved_design_member']}
    for mask,j in ((22487656929184,[0,0,0,0]),(442312790436,[1,0,2,2])):
        x = rows[mask]
        assert x['full_domain'] and x['exact_compression'] and x['J'] == j
        assert not x['star_in_9O'] and any(x['star_mod_pi'])
        assert x['remaining_mod_pi'] == [(-c)%3 for c in x['star_mod_pi']]
        assert x['remaining_G'] == [-v for v in x['star_G']]
    assert rows[22487656929184]['pair_phase_difference'] != 0
    assert rows[442312790436]['pair_phase_difference'] == 0


def test_quadratic_aggregation_loses_exact_compression_information():
    audit = load('results/star_cut/audit.json')
    x = next(x for x in audit['saved_points'] if x['masks'][0] == 31210651353580)
    assert x['full_domain'] and not x['exact_compression']
    assert x['J'] == [0,0,1,1] and x['star_G_times_G'] == [0,0,0]
    old = load('results/event_compression/audit.json')
    y = next(x for x in old['saved_points'] if x['masks'][0] == 31210651353580)
    assert y['nonzero_products'] == 36
    for mean in audit['saved_design_quadratic_sums']:
        assert mean['sum_HG'] == [a+b for a,b in zip(mean['sum_H_squared'],mean['sum_HR'])]
        assert all(v > 0 for v in mean['sum_HG'])


def test_full_domain_not_replaced_by_products_or_q_divisibility():
    rows = load('results/star_cut/audit.json')['saved_points']
    outside = next(x for x in rows if x['masks'][0] == 22964264347100)
    assert outside['exact_compression'] and not outside['full_domain']
    assert outside['J'] is None and outside['star_G_times_G'] == [0,0,0]
