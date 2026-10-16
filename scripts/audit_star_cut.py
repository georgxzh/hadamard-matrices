"""Bounded checks on inherited witnesses only; do not overwrite old artifacts."""
import argparse
import hashlib
import json
import time

from scripts.primitive_local_audit import ROOT, load, red, mul, conj, POW, phase_norm
from scripts.event_compression_products import models, indicator, form_value
from scripts.residue_formula import tensor_coefficients, residue_basis
from scripts.star_cut import residue, signed_counts, support_cut, cut_polynomial, event_cut, folded

BASE = 'ee3b93944668606a51ef3253ee101deeb5d2a96d'
OUT = ROOT/'results/star_cut'


def save(name, value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',
                          encoding='utf8',newline='\n')


def main():
    p = argparse.ArgumentParser(); p.add_argument('stage',choices=['pilot','audit'])
    stage = p.parse_args().stage; start = time.perf_counter()
    if stage == 'audit':
        assert load('results/star_cut/pilot.json')['projected_seconds_5x'] < 120
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    old = load('results/compression_residue/audit.json')
    points = []; supports = []; means = []; product_sums_checked = 0
    for rank,pair in ((277,(1,2)),(279,(2,3))):
        c = cat[rank-1]; cs = [c['first'],c['second']]
        model,selectors,forms = models(cs,pair)
        w = support_cut(cs[1],pair); rr = residue(w)
        assert rr == ([1,0,0,0] if rank == 277 else [0,0,1,1])
        # Verify the norm decomposition formula independently in the residue ring.
        a = red(signed_counts(cs[1])); h = red(signed_counts(cs[1],pair))
        expression = [x+y-2*z for x,y,z in zip(mul(h,conj(a)),mul(conj(h),a),mul(h,conj(h)))]
        assert residue(expression) == rr
        supports.append({'rank':rank,'pair':pair,'active':model['active'][1],
            'signed_counts':signed_counts(cs[1]),'pair_signed_counts':signed_counts(cs[1],pair),
            'cut_signed_difference_counts':w,'cut_residue_mod_pi':rr,
            'all_phases_nondivisible_by_pi':True,'selectors':len(selectors),'products':162})
        ordinary = [x for x in old['saved_records_checked'] if x['rank'] == rank]
        design = next(x for x in old['barycenters'] if x['rank'] == rank)['witnesses']
        selected = [(x,False) for x in ordinary]+[(x,True) for x in design]
        if stage == 'pilot':
            selected = [(ordinary[0],False)]
        hg = [0]*3; h2 = [0]*3; hr = [0]*3
        for x,is_design in selected:
            assert time.perf_counter()-start < 120
            phases = x['phases']; assert all(phases[i] == 0 for i in (0,1,12))
            b = cut_polynomial(cs[1],phases[12:],pair)
            assert b == event_cut(selectors,phases)
            t = red(b); expected = residue(t); assert expected == rr
            # Independent F_D = H + R multiplication in the full integral basis.
            fs,s = phase_norm(cs,phases)
            pos = dict(zip(model['active'][1],phases[12:])); h = [0]*24
            for i in pair:
                h = [v+cs[1][i]*z for v,z in zip(h,POW[i+15*pos[i]])]
            rem_f = [v-z for v,z in zip(fs[1],h)]
            assert t == [v+z for v,z in zip(mul(h,conj(rem_f)),mul(conj(h),rem_f))]
            assert s == x['norm_defect']
            domain = all(v % 9 == 0 for v in s)
            assert domain == x['in_domain']
            assert domain == all(v % 9 == 0 for row in tensor_coefficients(x['balance']) for v in row)
            assert (residue_basis(s) if domain else None) == x['J']
            g = x['G'][:3]; assert g == [form_value(f,phases) for f in forms]
            hs = folded(b)[:3]; remainder_g = [v-z for v,z in zip(g,hs)]
            sums = []
            for t0 in range(3):
                # Sum the preselected Y_e G_t with integer star coefficients.
                weighted = sum(e['weight']*((e['shift'] % 9 == t0)+((-e['shift']) % 9 == t0))
                    *indicator(e['event'],phases)*g[t0] for e in selectors)
                assert weighted == hs[t0]*g[t0] == hs[t0]**2+hs[t0]*remainder_g[t0]
                sums.append(weighted); product_sums_checked += 1
                if is_design:
                    hg[t0] += weighted; h2[t0] += hs[t0]**2
                    hr[t0] += hs[t0]*remainder_g[t0]
            remainder = [v-z for v,z in zip(s,t)]
            if domain:
                assert residue(remainder) == [(-v)%3 for v in rr]
            points.append({'rank':rank,'masks':x['masks'],'saved_design_member':is_design,
                'pair_phase_difference':(pos[pair[1]]-pos[pair[0]])%3,
                'full_domain':domain,'exact_compression':not any(g),'J':x['J'],
                'G':g,'star_G':hs,'remaining_G':remainder_g,'star_G_times_G':sums,
                'star_coefficients':t,'remaining_coefficients':remainder,
                'star_mod_pi':rr,'remaining_mod_pi':residue(remainder),
                'star_in_9O':all(v%9 == 0 for v in t)})
        means.append({'rank':rank,'denominator':27,'sum_HG':hg,'sum_H_squared':h2,'sum_HR':hr,
            'scope':'Saved 27-point relaxation only; not a conditional fiber witness.'})
    elapsed = time.perf_counter()-start
    if stage == 'pilot':
        result = {'seconds':elapsed,'saved_points':len(points),'projected_seconds_5x':elapsed*31*5,
            'workers':1,'cap_seconds':120,'estimated_memory_bytes':100_000_000,
            'estimated_new_storage_bytes':200_000,'estimates_not_measurements':True}
        save('pilot.json',result); print(result); return
    result = {'base_commit':BASE,'supports':supports,'saved_points':points,'saved_design_quadratic_sums':means,
        'points_checked':len(points),'weighted_product_identities_checked':product_sums_checked,
        'new_phase_assignments_generated':0,'seconds':elapsed,'workers':1,'cap_seconds':120,'caps_hit':False,
        'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (
            'scripts/star_cut.py','scripts/audit_star_cut.py','results/compression_residue/audit.json',
            'results/event_compression/audit.json','results/p5_branch_portfolio/canonical_branches.json')}}
    save('audit.json',result)
    print({'seconds':elapsed,'points':len(points),'product_sums_checked':product_sums_checked})
    print(supports); print(means)
    print([{k:v for k,v in x.items() if k in ('rank','masks','G','star_G','star_G_times_G','J','full_domain','star_mod_pi')}
           for x in points if not x['saved_design_member']])


if __name__ == '__main__':
    main()
