"""Pilot then independent unfiltered full-PAF audit of the saved p=7 branch."""
import json
import os
import subprocess
from pathlib import Path

from scripts.classify_p5_lifts import ROOT,digest,save
from scripts.benchmark_spectral_join import OUTPUT,p7_pair
from src.spectral_join import COMPILER,FLAGS

EXE=ROOT/'tmp/full_paf_audit.exe'


def run(pair,name,cap,seconds):
    output=OUTPUT/f'{name}.json'; source=output.with_suffix('.input.txt')
    source.write_text(str(len(pair[0]))+'\n'+'\n'.join(' '.join(map(str,r)) for r in pair)+'\n',encoding='ascii',newline='\n')
    command=[str(EXE),str(source),str(output),str(cap),str(seconds),'full-key']
    r=subprocess.run(command,capture_output=True,text=True,timeout=seconds+15)
    if r.returncode: raise RuntimeError(r.stderr)
    data=json.loads(output.read_text()); data['command']=command; save(output,data)
    return data


def main():
    command=[str(COMPILER),str(ROOT/'src/full_paf_audit.cpp'),'-o',str(EXE),*FLAGS]
    environment=os.environ.copy(); environment['PATH']=str(COMPILER.parent)+os.pathsep+environment.get('PATH','')
    r=subprocess.run(command,capture_output=True,text=True,env=environment,timeout=120)
    if r.returncode: raise RuntimeError(r.stderr)
    # Independent known positive/empty controls before the larger audit.
    catalog=json.loads((ROOT/'results/p5_branch_portfolio/canonical_branches.json').read_text())
    controls=[]
    for rank in (1,3):
        e=catalog[rank-1]; data=run((e['first'],e['second']),f'full_paf_control_rank{rank}',2_000_000,30)
        expected=json.loads((ROOT/'results/p5_classification/classification.json').read_text())[rank-1]
        assert data['complete'] and data['solutions']==expected['solutions']; controls.append(data)
    # Stored-row and streaming probes estimate per-candidate cost separately.
    pair=p7_pair(); a=run(pair,'full_paf_pilot',200_000,10)
    # Streaming full keys + binary search can cost more than table generation.
    estimate=10*a['elapsed_seconds']*sum(a['expected'])/max(1,sum(a['enumerated']))
    memory_estimate=4*16*min(a['expected'])+100_000_000
    pilot={'estimated_seconds_with_margin':estimate,'estimated_memory_bytes':memory_estimate,
           'estimated_storage_bytes':1_000_000,'pilot_seconds':a['elapsed_seconds'],
           'limitation':'Stored-row prefix only; 10x runtime margin includes unknown streaming cost.',
           'build_command':command,'source_sha256':digest(ROOT/'src/full_paf_audit.cpp'),'binary_sha256':digest(EXE)}
    save(OUTPUT/'full_paf_pilot_metadata.json',pilot)
    if estimate>1300 or memory_estimate>8_000_000_000: raise RuntimeError('pilot resource gate requires approval')
    data=run(pair,'full_paf_p7',50_000_000,min(1400,max(120,3*estimate)))
    reference=json.loads((OUTPUT/'p7_mode0.json').read_text())
    if data['complete']:
        assert reference['complete'] and data['solutions']==reference['solutions']
        assert data['ordered_pairs']==reference['ordered_pairs']
    save(OUTPUT/'independent_audit.json',{'status':'passed' if data['complete'] else 'unresolved',
         'result_sha256':digest(OUTPUT/'full_paf_p7.json'),'source_sha256':digest(ROOT/'src/full_paf_audit.cpp'),
         'script_sha256':digest(Path(__file__)),'binary_sha256':digest(EXE),
         'ordered_pairs':data['ordered_pairs'],'controls':[r['ordered_pairs'] for r in controls],
         'limitation':'Independent enumeration and full-PAF lookup; shared input and compiler, no formal exhaustion certificate.'})
    print(pilot); print({k:v for k,v in data.items() if k not in ('command','solutions')},flush=True)


if __name__=='__main__': main()
