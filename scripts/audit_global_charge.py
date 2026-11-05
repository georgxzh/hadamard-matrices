"""Seven predeclared deterministic transports of saved witnesses, no search."""
import argparse
import hashlib
import json
import time
from scripts.primitive_local_audit import ROOT,load,phase_norm,POW,mul
from scripts.audit_phase_exchange import endpoint
from scripts.residue_formula import build_model
from scripts.compression_residue import compressed_charges,restricted_domain
from scripts.phase_exchange import sub,norm_change
from scripts.three_phase_trades import thin_hypotheses
from scripts.global_charge import transport,fiber_count,row_paf

BASE='2b7e9c712c23cf859e1bd54146f8a39bc2424724'
OUT=ROOT/'results/global_charge'


def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')


def check(saved,cat):
    rank=saved['rank'];other=279 if rank==277 else 277
    c=cat[rank-1];cs=[c['first'],c['second']]
    d=cat[other-1];ds=[d['first'],d['second']]
    old=endpoint(cs,build_model(cs),saved['phases'])
    assert old['S']==saved['norm_defect'] and old['masks']==saved['masks']
    assert old['G']==saved['G'] and old['full_domain']==saved['in_domain']
    tr=transport(cs,ds,old['phases'])
    new=endpoint(ds,build_model(ds),tr['phases'])
    before=compressed_charges(ds,tr['before_anchor_normalization'])
    assert before==old['charges']
    for a,b in zip(old['charges'],new['charges']):
        assert row_paf(a['row'])==row_paf(b['row'])
        assert [sum(v*v for v in m) for m in a['charges']]==[sum(v*v for v in m) for m in b['charges']]
    assert old['G']==new['G']
    fs,_=phase_norm(ds,tr['before_anchor_normalization'])
    predicted=[0]*24
    active=[i for i,c in enumerate(cs[1]) if abs(c)==1]
    index={i:12+j for j,i in enumerate(active)}
    for entry in tr['mapping']:
        i=entry['old'];k=entry['k_mod5'];a=old['phases'][index[i]]
        term=mul(POW[(i+15*a)%45],POW[9*k])
        predicted=[x+entry['sign']*y for x,y in zip(predicted,term)]
    assert predicted==fs[1]
    assert mul(POW[(-15*tr['anchor_subtracted'])%45],predicted)==new['F'][1]
    assert norm_change(old['F'][1],sub(predicted,old['F'][1]))==sub(new['S'],old['S'])
    for ep in (old,new):
        if not any(ep['G']):assert restricted_domain(ep['B'])==ep['full_domain']
    # Inverse transport returns the old gauged assignment, not merely its PAF.
    back=transport(ds,cs,tr['phases'])
    assert back['phases']==old['phases']
    counts=[fiber_count(rows,ep['charges']) for rows,ep in ((cs,old),(ds,new))]
    assert all(x['count']>0 for x in counts)
    return {'source_rank':rank,'target_rank':other,'source':old,'target':new,'transport':tr,
            'charge_fiber_counts':counts,
            'source_hypotheses':[thin_hypotheses(r,m['charges']) for r,m in zip(cs,old['charges'])],
            'target_hypotheses':[thin_hypotheses(r,m['charges']) for r,m in zip(ds,new['charges'])]}


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('pilot','audit'));stage=p.parse_args().stage
    start=time.perf_counter();old=load('results/compression_residue/audit.json')
    cat=load('results/p5_branch_portfolio/canonical_branches.json')
    pilot=load('results/global_charge/pilot.json') if stage=='audit' else None
    if pilot:assert pilot['projected_seconds_5x']<120
    checks=[]
    for saved in old['saved_records_checked'][:1] if stage=='pilot' else old['saved_records_checked']:
        assert time.perf_counter()-start<120
        prior=[] if pilot is None else [x for x in pilot['checks'] if x['source']['masks']==saved['masks']]
        checks.append(prior[0] if prior else check(saved,cat))
    relax=[]
    for b in old['barycenters']:
        assert all(not any(v) for v in b['sums'].values())
        assert all(not w['exact_length_nine'] and not w['in_domain'] for w in b['witnesses'])
        relax.append({'rank':b['rank'],'saved_members':len(b['witnesses']),'exact_compression_members':0,
                      'full_9O_members':0,'mean_B_G_Q_S_zero':True,'scope':'Saved convex mean only; not a conditional witness.'})
    elapsed=time.perf_counter()-start
    out={'base_commit':BASE,'stage':stage,'checks':checks,'saved_relaxations':relax,'seconds':elapsed,
         'workers':1,'cap_seconds':120,'caps_hit':False,'search_performed':False,
         'new_assignments_total':len(checks),'pilot_reused':1 if pilot else 0,
         'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (
             'scripts/global_charge.py','scripts/audit_global_charge.py',
             'results/compression_residue/audit.json','results/p5_branch_portfolio/canonical_branches.json')}}
    if stage=='pilot':out.update({'projected_seconds_5x':elapsed*7*5,'estimated_memory_bytes':200_000_000,'estimated_storage_bytes':2_000_000})
    save(stage+'.json',out)
    print({'seconds':elapsed,'records':len(checks),'projection':out.get('projected_seconds_5x')})
    for c in checks:
        print({'rank':c['source_rank'],'old':c['source']['masks'],'new':c['target']['masks'],
               'G':c['target']['G'][:3],'new_9O':c['target']['full_domain'],'new_J':c['target']['J'],
               'new_S_constant':c['target']['S'][0],'counts':[x['count'] for x in c['charge_fiber_counts']]})


if __name__=='__main__':main()
