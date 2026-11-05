"""Bounded pilot and one-step all-sign triple audit of three saved origins."""
import argparse
from collections import Counter
import hashlib
import json
import time

from scripts.primitive_local_audit import ROOT,load
from scripts.residue_formula import build_model,residue_basis
from scripts.compression_residue import restricted_domain,folded_balances
from scripts.audit_phase_exchange import endpoint
from scripts.phase_exchange import sub,norm_change,affected_delta
from scripts.three_phase_trades import candidates,thin_hypotheses,delta_f,landing_delta_f

BASE='f92a7b3740e4b301a9574b8ae7e61fd9c0dd7bac'
OUT=ROOT/'results/three_phase_trades'


def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')


def check(cs,model,old,move):
    new=endpoint(cs,model,move['phases'])
    assert all(new['phases'][k]==0 for k in (0,1,12))
    assert sum(a!=b for a,b in zip(old['phases'],new['phases']))==3
    assert old['charges']==new['charges'] and old['G']==new['G']
    df=delta_f(cs[move['side']],old['phases'],move)
    assert df==landing_delta_f(cs[move['side']],move)==sub(new['F'][move['side']],old['F'][move['side']])
    ds=sub(new['S'],old['S']);assert ds==norm_change(old['F'][move['side']],df)
    d,counts=affected_delta(model,old['phases'],new['phases'])
    assert d==sub(new['B'],old['B']) and max(counts)<=6 and max(map(abs,d))<=6
    assert not any(folded_balances(d)) and all(sum(d[r::15])==0 for r in range(15))
    dom=all(x%9==0 for x in ds);assert restricted_domain(d)==dom
    assert old['full_domain'] and new['full_domain']==dom
    saturation=[]
    increments={u:v for u,v in zip(move['phase_indices'],move['increments'])}
    for s,value in enumerate(d):
        if abs(value)!=6:continue
        sigma=value//6;edges=[]
        for w,u,v,h in model['edges'][s]:
            if u not in increments and v not in increments:continue
            step=(increments.get(v,0)-increments.get(u,0))%3
            theta=(old['phases'][v]-old['phases'][u]-h)%3
            assert step and theta==(-((1+sigma*w)//2)*step)%3
            term=w*(int((new['phases'][v]-new['phases'][u]-h)%3==0)-int(theta==0))
            assert term==sigma
            edges.append({'weight':w,'from_phase_index':u,'to_phase_index':v,'carry_plus_layer':h,
                          'old_colour_relative_to_layer':theta,'increment':step})
        assert len(edges)==6
        saturation.append({'shift':s,'sign':sigma,'edges':edges})
    if dom:
        for r in range(15):
            triple=sorted(d[r::15]);assert triple in ([0,0,0],[-6,3,3],[-3,-3,6])
        if any(d):assert saturation
    hypothesis=thin_hypotheses(cs[move['side']],old['charges'][move['side']]['charges'])
    if hypothesis['uniform_structural_hypothesis']:
        assert not saturation
        if dom:assert not any(d)
    return {'origin_masks':old['masks'],'move':move,'endpoint':new,'delta_F':df,'delta_S':ds,'delta_B':d,
            'affected_edge_counts':counts,'saturated_shifts':saturation,'delta_in_9O':dom,
            'delta_J':residue_basis(ds) if dom else None,'hypothesis':hypothesis}


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['pilot','audit'])
    stage=p.parse_args().stage;start=time.perf_counter()
    frozen=load('results/phase_exchange/audit.json')['origins']
    pilot=load('results/three_phase_trades/pilot.json') if stage=='audit' else None
    if pilot:assert pilot['projected_seconds_5x']<120
    origins=[];checks=[];inventories=[]
    for saved in frozen:
        cs=saved['rows'];model=build_model(cs);old=endpoint(cs,model,saved['phases'])
        assert old['S']==saved['S'] and old['masks']==saved['masks'] and old['full_domain']
        hypotheses=[thin_hypotheses(row,c['charges']) for row,c in zip(cs,old['charges'])]
        origins.append({'rank':saved['rank'],'rows':cs,'hypotheses':hypotheses,**old})
        status=Counter();types=Counter();eligible=[];raw=0
        for move in candidates(cs,old['phases']):
            raw+=1;status[move['status']]+=1
            if move['status']=='permitted':eligible.append(move);types[move['flow']['type']]+=1
        assert raw==3080
        inventories.append({'origin_masks':old['masks'],'position_triples':385,'increment_patterns':8,
            'raw_candidates':raw,'status_counts':dict(status),'permitted_types':dict(types),
            'permitted_moves':eligible})
        selected=eligible[:1] if stage=='pilot' else eligible
        for move in selected:
            assert time.perf_counter()-start<120
            prior=[] if pilot is None else [x for x in pilot['checks'] if x['origin_masks']==old['masks'] and x['move']==move]
            checks.append(prior[0] if prior else check(cs,model,old,move))
    elapsed=time.perf_counter()-start
    out={'base_commit':BASE,'stage':stage,'origins':origins,'inventories':inventories,'checks':checks,
         'raw_candidates_total':9240,'neighbor_depth':1,'multi_step_search':False,'seconds':elapsed,
         'workers':1,'cap_seconds':120,'caps_hit':False,'new_distinct_neighbors_evaluated':len(checks),
         'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (
             'scripts/three_phase_trades.py','scripts/audit_three_phase_trades.py','results/phase_exchange/audit.json')}}
    if stage=='pilot':
        kept=sum(i['status_counts'].get('permitted',0) for i in inventories)
        out.update({'projected_seconds_5x':elapsed*max(1,kept/len(checks))*5,
                    'estimated_memory_bytes':200_000_000,'estimated_storage_bytes':2_000_000})
    else:
        out['pilot_endpoints_reused']=len(pilot['checks'])
        out['summary']=[{'origin_masks':o['masks'],
            'neighbors':sum(x['origin_masks']==o['masks'] for x in checks),
            'in_domain':sum(x['origin_masks']==o['masks'] and x['endpoint']['full_domain'] for x in checks),
            'correlation_changing_in_domain':sum(x['origin_masks']==o['masks'] and x['endpoint']['full_domain'] and any(x['delta_B']) for x in checks),
            'moves_with_saturation':sum(x['origin_masks']==o['masks'] and bool(x['saturated_shifts']) for x in checks)} for o in origins]
        out['blanket_rigidity_counterexamples']=[{'origin_masks':x['origin_masks'],'move':x['move'],'endpoint_masks':x['endpoint']['masks'],
           'J':x['endpoint']['J'],'delta_J':x['delta_J'],'G':x['endpoint']['G'],'hypothesis':x['hypothesis']}
           for x in checks if x['endpoint']['full_domain'] and any(x['delta_B'])]
    save(stage+'.json',out)
    print({'seconds':elapsed,'neighbors':len(checks),'summary':out.get('summary'),
           'projection':out.get('projected_seconds_5x')})
    print([{'mask':o['masks'][0],'hypotheses':o['hypotheses']} for o in origins])


if __name__=='__main__':main()
