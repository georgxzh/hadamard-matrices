"""Bounded saved-evidence audit; no new phase assignments or census."""
import argparse
import hashlib
import json
from fractions import Fraction
import time

from scripts.primitive_local_audit import ROOT, load, red, valuation
from scripts.residue_formula import tensor_coefficients
from scripts.event_compression_products import (models, indicator, expand_value,
    contract, form_value, conditional_response, independent_factor_map,
    product_expectation, local_dipole, q_of, carry_feedback)
from src.legendre import _reduce_mod_monic

BASE = 'f1499ee7c5f726e34d1c74c644b40b1187ef6771'
OUT = ROOT/'results/event_compression'


def rational(x):
    if isinstance(x,Fraction):
        return {'numerator':x.numerator,'denominator':x.denominator}
    raise TypeError(type(x))


def save(name, value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True,default=rational)+'\n',
                          encoding='utf8',newline='\n')


def main():
    p = argparse.ArgumentParser(); p.add_argument('stage',choices=['pilot','audit'])
    args = p.parse_args(); start = time.perf_counter()
    cat = load('results/p5_branch_portfolio/canonical_branches.json')
    old = load('results/compression_residue/audit.json')
    if args.stage == 'audit':
        assert load('results/event_compression/pilot.json')['estimate_seconds_5x'] < 120
    model_records = []; point_records = []; mean_records = []; independent_records = []
    checks = 0; carry_checks = 0; modular_counter = None
    for rank, pair in ((277,(1,2)),(279,(2,3))):
        c = cat[rank-1]; cs = [c['first'],c['second']]
        m, selectors, forms = models(cs,pair)
        contracted = [[contract(f,e) for f in forms] for e in selectors]
        model_records.append({'rank':rank,'pair':pair,'rows':cs,
            'selectors':selectors,'G_forms':forms,'contracted_forms':contracted,
            'products':len(selectors)*len(forms),'core_products':18})
        records = [h for h in old['saved_records_checked'] if h['rank'] == rank]
        design = next(d for d in old['barycenters'] if d['rank'] == rank)
        # Use only saved evidence, including the saved 27-point designs.
        if args.stage == 'pilot':
            records = records[:1]
        else:
            records += design['witnesses']
        sums = [[0]*3 for _ in selectors]
        for record_index,h in enumerate(records):
            assert time.perf_counter()-start < 120
            phases = h['phases']; g = h['G'][:3]
            assert [form_value(f,phases) for f in forms] == g
            assert h['in_domain'] == all(x % 9 == 0 for a in tensor_coefficients(h['balance']) for x in a)
            values = []
            for i,e in enumerate(selectors):
                y = indicator(e['event'],phases)
                vals = [expand_value(e,f,phases) for f in forms]
                assert vals == [y*v for v in g]
                assert vals == [y*form_value(f,phases) for f in contracted[i]]
                for coordinate in (0,2):
                    for gt in g:
                        diff = carry_feedback(h['Q'][coordinate],gt,y)
                        if gt % 3 == 0:
                            assert diff == (y*(gt//3)) % 3
                        if not any(g):
                            assert diff == 0
                        carry_checks += 1
                        if (h['masks'][0] == 31210651353580 and e['core'] and
                            coordinate == 0 and gt == 6 and y):
                            modular_counter = {'masks':h['masks'],'event':e,'Q_0':h['Q'][0],
                                'G_1':gt,'Y':y,'Y_G_mod3':(y*gt)%3,'carry_difference_mod3':diff,
                                'qualification':'Shifted carry is not J outside exact compression.'}
                values.append(vals); checks += 3
            is_design = record_index >= sum(hh['rank'] == rank for hh in old['saved_records_checked'])
            if is_design:
                for i in range(len(selectors)):
                    sums[i] = [a+b for a,b in zip(sums[i],values[i])]
            point_records.append({'rank':rank,'masks':h['masks'],'saved_design_member':is_design,
                'G':g,'Q':h['Q'],'J':h['J'],'in_domain':h['in_domain'],
                'equal_cancelling_phases': phases[12+m['active'][1].index(pair[0])] == phases[12+m['active'][1].index(pair[1])],
                'products':values,'nonzero_products':sum(v != 0 for row in values for v in row)})
        if args.stage == 'audit':
            mean_records.append({'rank':rank,'sample_size':27,'product_sums':sums,
                'nonzero_product_means':sum(x != 0 for row in sums for x in row),
                'core_nonzero_product_means':sum(x != 0 for e,row in zip(selectors,sums) if e['core'] for x in row)})
        # Independent model is not the 27-point code: it has nineteen independent
        # scalar factors. Evaluate its moments by rank, not phase enumeration.
        mapping,n = independent_factor_map(cs,pair)
        for i,e in enumerate(selectors[:3] if args.stage == 'pilot' else selectors):
            assert time.perf_counter()-start < 120
            response = conditional_response(cs,pair,e['positions'][1],e['phase_difference'])
            mean = [product_expectation(e,f,mapping,n) for f in forms]
            assert mean == [x/3 for x in response['G']]
            independent_records.append({'rank':rank,'selector_index':i,'event':e,
                'independent_factors':n,'E_YG':mean,'conditional_G':response['G'],
                'conditional_Q':response['Q'],
                'scope':'Exact rational moments of a relaxation distribution; no 9O membership asserted.'})
    elapsed = time.perf_counter()-start
    if args.stage == 'pilot':
        out = {'seconds':elapsed,'saved_records':len(point_records),'products_checked':checks,
            'expectation_rows':len(independent_records),'estimate_seconds_5x':elapsed*31*5,
            'cap_seconds':120,'workers':1,'memory_estimate_bytes':150_000_000,
            'storage_estimate_bytes':3_000_000}
        save('pilot.json',out);print(out);return
    blind = []; support_table = []
    for n in (5,14,23,32,41):
        b = local_dipole(n); s = red(b)
        r = list(_reduce_mod_monic(s,[1]*5)); r += [0]*(4-len(r))
        assert all(sum(b[t::9]) == 0 for t in range(9))
        assert (not any(s)) == (n == 23)
        blind.append({'n':n,'B_local':b,'Q_local':q_of(b),'primitive_coefficients':s,
                      'valuation_pi':valuation(s),'reduction_mod_pi':[v % 3 for v in r],
                      'is_full_domain_term':all(v % 9 == 0 for v in s)})
    for rank,pair in ((277,(1,2)),(279,(2,3))):
        c = cat[rank-1]; u,v = pair
        for k,sign in enumerate(c['second']):
            if abs(sign) != 1 or k in pair:
                continue
            for d in range(3):
                n = (k-u+15*d) % 45
                if n % 9 == 5:
                    support_table.append({'rank':rank,'third_position':k,'difference':d,
                        'n':n,'weight':c['second'][u]*sign,'primitive_cross_term_zero':n == 23})
    strong = next(h for h in old['saved_records_checked'] if h['masks'][0] == 442312790436)
    active_d = [i for i,c in enumerate(cat[278]['second']) if abs(c) == 1]
    local_phases = [strong['phases'][12+active_d.index(i)] for i in (2,3,4)]
    assert local_phases == [0,0,2]
    local = local_dipole(32,-1); local_s = red(local)
    remainder = [a-b for a,b in zip(strong['norm_defect'],local_s)]
    assert valuation(local_s) == valuation(remainder) == 0
    decomposition = {'masks':strong['masks'],'positions':[2,3,4],'local_phases':local_phases,
        'n':32,'weight':-1,'local_G':[sum(local[t::9]) for t in range(9)],
        'local_Q':q_of(local),'local_primitive_coefficients':local_s,
        'remaining_primitive_coefficients':remainder,'local_valuation':0,'remaining_valuation':0,
        'full_norm_defect':strong['norm_defect'],'full_J':strong['J'],
        'qualification':'Neither summand has an individual S/9 residue; the full sum does.'}
    save('model.json',{'base_commit':BASE,'branches':model_records,
        'family_selected_before_audit':'Six core selectors / 18 products; full star 54 selectors / 162 products per branch.'})
    out = {'base_commit':BASE,'saved_points':point_records,'saved_design_means':mean_records,
        'independent_model_moments':independent_records,'compression_invisible_dipoles':blind,
        'indexed_midpoint_supports':support_table,'strong_witness_decomposition':decomposition,
        'seconds':time.perf_counter()-start,'workers':1,'caps_hit':False,
        'products_checked':checks,'carry_identity_checks':carry_checks,
        'modular_product_counterexample':modular_counter,'new_phase_assignments_generated':0,
        'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (
            'scripts/event_compression_products.py','scripts/audit_event_compression.py',
            'results/compression_residue/audit.json','results/p5_branch_portfolio/canonical_branches.json')}}
    save('audit.json',out)
    print({'seconds':out['seconds'],'saved_points':len(point_records),'products_checked':checks})
    for r in point_records:
        if not r['saved_design_member']:
            print({k:r[k] for k in ('rank','masks','G','J','equal_cancelling_phases','nonzero_products')})
    print([{k:r[k] for k in ('rank','sample_size','nonzero_product_means','core_nonzero_product_means')} for r in mean_records])
    for r in independent_records:
        if r['event']['core']:
            print({'rank':r['rank'],'positions':r['event']['positions'],'d':r['event']['phase_difference'],
                   'conditional_G':r['conditional_G'],'conditional_Q':r['conditional_Q']})
    print([{'n':r['n'],'Q':r['Q_local'],'valuation':r['valuation_pi']} for r in blind])


if __name__ == '__main__':
    main()
