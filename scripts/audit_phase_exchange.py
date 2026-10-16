"""At most one-exchange neighbors of three frozen origins; full integer checks."""
import argparse
from collections import Counter
import hashlib
import json
import time

from scripts.primitive_local_audit import ROOT, load, phase_norm, valuation, red
from scripts.residue_formula import build_model, histograms, tensor_coefficients, residue_basis, SETS
from scripts.compression_residue import compressed_charges, folded_balances, restricted_domain
from scripts.phase_exchange import exchanges, delta_factor, delta_factor_offset, norm_change, sub, affected_delta
from src.ternary_phase import PhaseRow
from src.legendre import compress

BASE = '9ed23ba6252ddfec41a79b6eff5af93f7ef10c6c'
OUT = ROOT/'results/phase_exchange'
MASKS = (22487656929184,442312790436,31210651353580)


def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')


def endpoint(cs, model, phases):
    fs,s = phase_norm(cs,phases)
    b = histograms(model,phases); tensor = tensor_coefficients(b)
    assert red(b) == s
    domain = all(x%9 == 0 for x in s)
    assert domain == all(x%9 == 0 for row in tensor for x in row)
    charges = compressed_charges(cs,phases)
    binary = []; masks = []; offset = 0
    for side,c in enumerate(cs):
        row = PhaseRow(c); n=len(row.active); x=row.decode(phases[offset:offset+n]); offset+=n
        assert list(compress(x,9)) == charges[side]['row']
        assert list(compress(x,15)) == list(c)
        binary.append(x); masks.append(sum(1<<i for i,v in enumerate(x) if v == -1))
    paf = [sum(x[i]*x[(i+s0)%45] for x in binary for i in range(45)) for s0 in range(45)]
    assert all(paf[s0]+2 == 4*b[s0] for s0 in range(1,45))
    q = [sum(b[s0] for s0 in SETS[4])-sum(b[s0] for s0 in SETS[k]) for k in range(4)]
    j = residue_basis(s) if domain else None
    if domain:
        assert all(x%3 == 0 for x in q)
        assert j == [(x//3)%3 for x in q]
    return {'phases':phases,'masks':masks,'F':fs,'S':s,'B':b,'tensor':tensor,
            'full_domain':domain,'J':j,'Q':q,'charges':charges,'G':folded_balances(b),'combined_PAF':paf}


def check_move(cs, model, origin, move):
    other = endpoint(cs,model,move['phases'])
    assert all(other['phases'][k] == 0 for k in (0,1,12))
    assert other['charges'] == origin['charges'] and other['G'] == origin['G']
    delta = delta_factor(cs[move['side']],move)
    assert delta == delta_factor_offset(cs[move['side']],move)
    assert delta == sub(other['F'][move['side']],origin['F'][move['side']])
    assert valuation(delta) == 3
    ds = sub(other['S'],origin['S'])
    assert ds == norm_change(origin['F'][move['side']],delta)
    d,counts = affected_delta(model,origin['phases'],other['phases'])
    assert d == sub(other['B'],origin['B'])
    assert max(counts) <= 4 and max(map(abs,d)) <= 4
    assert all(sum(d[r::15]) == 0 for r in range(15))
    assert not any(folded_balances(d))
    criterion = restricted_domain(d)  # Justified on the DIFFERENCE, including invalid-G origins.
    assert criterion == all(x%9 == 0 for x in ds)
    assert criterion == (not any(d)) == (not any(ds))
    dj = residue_basis(ds) if criterion else None
    dq = sub(other['Q'],origin['Q'])
    if criterion:
        assert all(x%3 == 0 for x in dq)
        assert dj == [(x//3)%3 for x in dq] == [0,0,0,0]
    assert origin['full_domain']
    assert other['full_domain'] == criterion
    if other['full_domain']:
        assert other['J'] == origin['J'] and other['combined_PAF'] == origin['combined_PAF']
    return {'origin_masks':origin['masks'],'move':move,'endpoint':other,
            'delta_F':delta,'delta_S':ds,'delta_B':d,'affected_edge_counts':counts,
            'max_abs_delta_B':max(map(abs,d)),'delta_in_9O':criterion,'delta_J':dj}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['pilot','audit'])
    stage=parser.parse_args().stage; start=time.perf_counter()
    cat=load('results/p5_branch_portfolio/canonical_branches.json')
    old=load('results/compression_residue/audit.json')
    pilot=None
    if stage == 'audit':
        pilot=load('results/phase_exchange/pilot.json')
        assert pilot['projected_seconds_5x'] < 120
    origins=[]; checks=[]; inventories=[]
    for mask in MASKS:
        saved=next(x for x in old['saved_records_checked'] if x['masks'][0] == mask)
        rank=saved['rank'];c=cat[rank-1];cs=[c['first'],c['second']];model=build_model(cs)
        origin=endpoint(cs,model,saved['phases'])
        assert origin['masks'] == saved['masks'] and origin['S'] == saved['norm_defect']
        assert origin['B'] == saved['balance'] and origin['J'] == saved['J'] and origin['full_domain']
        moves=list(exchanges(cs,origin['phases']));assert len(moves) == 121
        origins.append({'rank':rank,'rows':cs,**origin})
        inventories.append({'origin_masks':origin['masks'],'counts':dict(Counter(x['status'] for x in moves)),
                            'pairs':[{k:v for k,v in m.items() if k != 'phases'} for m in moves]})
        eligible=[m for m in moves if m['status'] == 'permitted']
        if stage == 'pilot':eligible=eligible[:1]
        for m in eligible:
            assert time.perf_counter()-start < 120
            existing=[] if pilot is None else [x for x in pilot['checks'] if x['origin_masks'][0] == mask and x['move'] == m]
            checks.append(existing[0] if existing else check_move(cs,model,origin,m))
    elapsed=time.perf_counter()-start
    out={'base_commit':BASE,'stage':stage,'origins':origins,'inventories':inventories,'checks':checks,
         'seconds':elapsed,'workers':1,'cap_seconds':120,'caps_hit':False,
         'raw_pairs_per_origin':121,'raw_pairs_total':363,'neighbor_depth':1,
         'evaluated_nontrivial_neighbors':len(checks),'multi_step_search':False,
         'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (
             'scripts/phase_exchange.py','scripts/audit_phase_exchange.py','results/compression_residue/audit.json',
             'results/p5_branch_portfolio/canonical_branches.json')}}
    if stage == 'pilot':
        out.update({'projected_seconds_5x':max(0.001,elapsed)*363*5/3,
                    'estimated_memory_bytes':150_000_000,'estimated_storage_bytes':1_000_000})
    else:
        out['pilot_neighbors_reused']=len(pilot['checks'])
        out['invariance_counterexamples']=[x['move'] for x in checks if x['endpoint']['full_domain']
             and x['endpoint']['J'] != next(o for o in origins if o['masks'] == x['origin_masks'])['J']]
        out['summary']=[{'origin_mask':m,'neighbors':sum(x['origin_masks'][0] == m for x in checks),
                        'neighbors_in_full_domain':sum(x['origin_masks'][0] == m and x['endpoint']['full_domain'] for x in checks)} for m in MASKS]
    save(stage+'.json',out)
    print({k:out[k] for k in ('stage','seconds','evaluated_nontrivial_neighbors')})
    print(out.get('summary',{'projected_seconds_5x':out.get('projected_seconds_5x')}))


if __name__ == '__main__':main()
