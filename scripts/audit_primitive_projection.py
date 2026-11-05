"""Eight saved phase records and one explicit integer relaxation; no search."""
import argparse
import hashlib
import json
import time
from scripts.primitive_local_audit import ROOT,load
from scripts.audit_phase_exchange import endpoint
from scripts.residue_formula import build_model
from scripts.compression_residue import restricted_domain
from scripts.primitive_projection import check45

BASE='44f0f1786c5a23f4231e2dcebea04acf1cce4fcb'
OUT=ROOT/'results/primitive_projection'


def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')


def check(rank,phases,cat,expected):
    c=cat[rank-1];ep=endpoint([c['first'],c['second']],build_model([c['first'],c['second']]),phases)
    assert all(phases[i]==0 for i in (0,1,12))
    assert ep['masks']==expected['masks'] and ep['S']==expected['S']
    result=check45(ep['B'])
    assert result['S']==ep['S'] and result['G']==ep['G'] and result['full_9O']==ep['full_domain']
    if not any(ep['G']):assert restricted_domain(ep['B'])==ep['full_domain']
    return {'rank':rank,'endpoint':ep,'projection':result,'scope':'Actual saved gauged assignment; endpoint domain flags apply.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('pilot','audit'));stage=parser.parse_args().stage
    start=time.perf_counter();cat=load('results/p5_branch_portfolio/canonical_branches.json')
    saved=load('results/compression_residue/audit.json')
    requests=[(x['rank'],x['phases'],{'masks':x['masks'],'S':x['norm_defect']}) for x in saved['saved_records_checked']]
    transported=load('results/global_charge/audit.json')['checks'][0]['target']
    requests.append((279,transported['phases'],transported))
    pilot=load('results/primitive_projection/pilot.json') if stage=='audit' else None
    if pilot:assert pilot['projected_seconds_5x']<120
    checks=[]
    for rank,phases,expected in requests[:1] if stage=='pilot' else requests:
        assert time.perf_counter()-start<120
        prior=[] if pilot is None else [x for x in pilot['checks'] if x['endpoint']['masks']==expected['masks']]
        checks.append(prior[0] if prior else check(rank,phases,cat,expected))
    out={'base_commit':BASE,'stage':stage,'checks':checks,'new_phase_assignments':0,
         'workers':1,'cap_seconds':120,'caps_hit':False,'pilot_reused':1 if pilot else 0}
    if stage=='audit':
        b=[(0,2,-1,0,-1,-1,0,-1,2)[s%9] for s in range(45)]
        toy=check45(b);assert toy['W']==0 and any(toy['G']) and any(toy['R'])
        out['integer_relaxation']={'scope':'Not a phase witness; no binary/support realization claimed.',**toy}
        out['saved_barycenters']=[{'rank':d['rank'],'members':len(d['witnesses']),
            'exact_compression_members':d['exact_compression_members'],'full_9O_members':d['full_9O_members'],
            'scope':'Saved zero mean; none is a conditional solution.'} for d in saved['barycenters']]
        assert all(x['exact_compression_members']==x['full_9O_members']==0 for x in out['saved_barycenters'])
    out['seconds']=time.perf_counter()-start
    if stage=='pilot':out.update({'projected_seconds_5x':out['seconds']*9*5,
                                 'estimated_memory_bytes':200_000_000,'estimated_storage_bytes':2_000_000})
    out['source_hashes']={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (
        'scripts/primitive_projection.py','scripts/audit_primitive_projection.py',
        'results/compression_residue/audit.json','results/global_charge/audit.json')}
    save(stage+'.json',out)
    print({'seconds':out['seconds'],'records':len(checks),'projection':out.get('projected_seconds_5x')})
    for c in checks:print({'mask':c['endpoint']['masks'][0],'G':c['endpoint']['G'][:3],
        'in_9O':c['endpoint']['full_domain'],'J':c['endpoint']['J'],'W':c['projection']['W'],
        'trace':c['projection']['trace_norm']})


if __name__=='__main__':main()
