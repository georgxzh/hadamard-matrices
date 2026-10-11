"""Serial, separately compiled full-PAF replication; never writes frozen evidence.

Run baseline, build, pilot, p5, p7, audit separately. Each run has a 1500 s
controller guard; each native job has a 240 s cap and 250 s hard timeout.
The frozen enumerator is reused, not represented as a third implementation.
"""
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/publication_gap_audit'
TMP = ROOT / 'tmp/publication_gap_audit'
EXE = TMP / 'full_paf_clang.exe'
COMPILER = Path('C:/Program Files/LLVM/bin/clang++.exe')
BASE = 'e76084054f594f2af89831cc377d88994ba7b4e6'
MANIFESTS = ['paper/artifact_manifest.json'] + [
    f'results/{n}/manifest.json' for n in ('p5_classification', 'phase_propagation',
    'spectral_join', 'p7_portfolio', 'p7_positive_control')]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(p):
    return json.loads((ROOT / p).read_text())

def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf8', newline='\n')

def baseline():
    entries = []
    for name in MANIFESTS:
        m = load(name)
        for e in m['files']:
            p = ROOT / e['path']
            assert sha(p) == e['sha256'] and p.stat().st_size == e['bytes'], e['path']
        entries.append({'path': name, 'sha256': sha(ROOT/name), 'entries': len(m['files'])})
    tracked = subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'results'], cwd=ROOT, text=True).splitlines()
    snapshot = [{'path': p, 'sha256': sha(ROOT/p)} for p in tracked]
    save(OUT/'baseline.json', {'requested_commit': BASE, 'head': subprocess.check_output(
        ['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(), 'manifests': entries,
        'manifest_entries_checked': sum(e['entries'] for e in entries), 'frozen_results': snapshot,
        'scope': 'Read-only digest verification, not a fresh exhaustion.'})
    print('Baseline hashes verified', sum(e['entries'] for e in entries), flush=True)

def build():
    TMP.mkdir(parents=True, exist_ok=True)
    command = [str(COMPILER), 'src/full_paf_audit.cpp', '-include', 'string',
               '-std=c++17', '-O3', '-mpopcnt', '-o', str(EXE), '-lpsapi']
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert run.returncode == 0, run.stderr
    detail = subprocess.run(command+['-###'], cwd=ROOT, capture_output=True, text=True, timeout=30)
    save(OUT/'build.json', {'command': command, 'compiler_version': subprocess.check_output(
        [str(COMPILER),'--version'], text=True), 'driver_details': detail.stderr,
        'compiler_sha256': sha(COMPILER), 'executable_sha256': sha(EXE),
        'source_sha256': sha(ROOT/'src/full_paf_audit.cpp'), 'harness_sha256': sha(__file__),
        'python': sys.version, 'platform': platform.platform(),
        'portability_issue': 'Without -include string, MSVC headers report missing std::stoull, stod and to_string. Frozen source unchanged.',
        'independence': 'Clang/MSVC STL and libcmt versus GCC/libstdc++/MinGW; same Windows host, input catalogue, and existing full-PAF source. Not external replication.',
        'wsl_probe': 'wsl --list --quiet: Wsl/E_ACCESSDENIED in sandbox; no claim that WSL is absent.'})

def cases():
    catalog = load('results/p5_branch_portfolio/canonical_branches.json')
    reference = load('results/p5_classification/classification.json')
    p5 = [{'id': f'p5_{e["rank"]:04d}', 'pair': [e['first'],e['second']],
           'solutions': r['solutions']} for e,r in zip(catalog,reference,strict=True)]
    p7 = [{'id': 'p7_'+e['id'], 'pair': e['pair'], 'solutions': []}
          for e in load('results/p7_portfolio/portfolio.json')['branches']]
    p7.append({'id':'p7_positive','pair':load('results/p7_positive_control/witness.json')['pair'],
               'solutions':load('results/p7_positive_control/solutions.json')['canonical_masks']})
    return p5,p7

def domains(case):
    return [3**(sum(abs(v)==1 for v in row)-1) for row in case['pair']]

def run_case(case, folder, cap=150_000_000, seconds=240):
    # These admitted finite domains fit <1 GB for the table; no broad search accepted.
    ds = domains(case)
    assert max(ds) <= 150_000_000 and min(ds) <= 14_348_907
    assert sha(EXE) == load('results/publication_gap_audit/build.json')['executable_sha256']
    inp = TMP/(case['id']+'.txt')
    inp.write_text(str(len(case['pair'][0]))+'\n'+'\n'.join(' '.join(map(str,r)) for r in case['pair'])+'\n')
    output = OUT/folder/(case['id']+'.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [str(EXE),str(inp),str(output),str(cap),str(seconds),'full-key']
    start = time.perf_counter()
    try:
        subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True, timeout=seconds+10)
        r = json.loads(output.read_text())
    except subprocess.TimeoutExpired:
        r = {'complete':False,'stop_reason':'wrapper_timeout','solutions':[], 'canonical_pairs':None,'ordered_pairs':None}
    r.update(id=case['id'], wrapper_seconds=time.perf_counter()-start, command=command,
             input_sha256=sha(inp), executable_sha256=sha(EXE), pair=case['pair'])
    if r['complete']:
        assert r['enumerated'] == r['expected'] == ds
        assert r['solutions'] == sorted(case['solutions']), case['id']
        assert r['canonical_pairs'] == len(case['solutions']) and r['ordered_pairs'] == 9*len(case['solutions'])
        r['exact_set_matches_frozen'] = True
    else:
        assert r['canonical_pairs'] is None and r['ordered_pairs'] is None
        r['exact_set_matches_frozen'] = None
    save(output,r)
    return r

def pilot():
    start=time.perf_counter(); p5,p7=cases(); strata={}
    for c in p5: strata.setdefault(tuple(domains(c)), c)
    records=[run_case(c,'pilot',seconds=60) for c in strata.values()]
    assert all(r['complete'] for r in records)
    rates={tuple(r['expected']):r['wrapper_seconds'] for r in records}
    p5_estimate=2*sum(rates[tuple(domains(c))] for c in p5)
    # Exercise both stored and streaming paths at p7 scale on smaller p5 cases,
    # plus bounded p7 row-prefix probes. Prefix-only estimates are not time bounds.
    probes=[run_case(c,'pilot',cap=100_000,seconds=15) for c in p7]
    estimates={r['id']:10*r['wrapper_seconds']*sum(domains(c))/max(1,sum(r['enumerated']))
               for r,c in zip(probes,p7,strict=True)}
    table_bound=3*16*(1 << (min(max(min(domains(c)) for c in p7),14_348_907)-1).bit_length())
    save(OUT/'resource_plan.json', {'pilot_seconds':time.perf_counter()-start,
        'p5_strata':len(strata), 'p5_estimated_seconds_with_2x_margin':p5_estimate,
        'p7_prefix_estimates_with_10x_margin':estimates,
        'p7_estimate_limitation':'Prefixes omit large-table sorting and streaming lookup; estimates are not guaranteed bounds. Serial capped trials only.',
        'serial_workers':1, 'controller_guard_seconds':1500, 'native_seconds_per_case':240,
        'hard_timeout_seconds_per_case':250, 'p7_worst_hard_timeout_sum_seconds':1250,
        'table_allocation_conservative_bytes':table_bound,
        'memory_allowance_bytes':2_000_000_000, 'storage_allowance_bytes':100_000_000,
        'p5_pilot_max_peak_bytes':max(r['peak_working_set_bytes'] for r in records),
        'p7_pilot_max_peak_bytes':max(r['peak_working_set_bytes'] for r in probes)})
    print(json.dumps(load('results/publication_gap_audit/resource_plan.json')),flush=True)

def full(which):
    plan=load('results/publication_gap_audit/resource_plan.json')
    assert plan['memory_allowance_bytes'] < 10_000_000_000
    if which=='p5': assert plan['p5_estimated_seconds_with_2x_margin']<1500
    selected=cases()[0 if which=='p5' else 1]; start=time.perf_counter(); records=[]
    for c in selected:
        if time.perf_counter()-start>1240: break  # reserve one full hard timeout
        records.append(run_case(c,which))
        if len(records)%100==0 or which=='p7': print(which,len(records),round(time.perf_counter()-start,2),flush=True)
    save(OUT/(which+'_summary.json'), {'complete':len(records)==len(selected) and all(r['complete'] for r in records),
        'requested_cases':len(selected),'attempted_cases':len(records), 'elapsed_seconds':time.perf_counter()-start,
        'completed_cases':sum(r['complete'] for r in records),
        'canonical_pairs':sum(r['canonical_pairs'] or 0 for r in records),
        'count_interpretation':'Sum is a lower bound unless complete=true; caps/timeouts unresolved.',
        'max_peak_working_set_bytes':max(r.get('peak_working_set_bytes',0) for r in records),
        'ordered_count_histogram':dict(Counter(r['ordered_pairs'] for r in records if r['complete']))})
    print(load('results/publication_gap_audit/'+which+'_summary.json'),flush=True)

def audit():
    for e in load('results/publication_gap_audit/baseline.json')['frozen_results']:
        assert sha(ROOT/e['path'])==e['sha256'],e['path']
    checked=0
    for group,cs in zip(('p5','p7'),cases(),strict=True):
        for c in cs:
            r=load('results/publication_gap_audit/'+group+'/'+c['id']+'.json')
            assert r['complete'] and r['solutions']==sorted(c['solutions'])
            assert r['enumerated']==r['expected']==domains(c)
            for masks in r['solutions']:
                n=len(c['pair'][0]); length=3*n
                rows=[[1-2*((m>>i)&1) for i in range(length)] for m in masks]
                assert all(sum(row)==1 for row in rows)
                assert [[sum(row[i+k*n] for k in range(3)) for i in range(n)] for row in rows]==c['pair']
                assert all(sum(sum(row[i]*row[(i+s)%length] for i in range(length)) for row in rows)==-2 for s in range(1,length))
                checked+=1
    save(OUT/'replication_audit.json', {'status':'passed','direct_p5_branches':1164,'direct_p7_branches':5,
         'exact_mask_sets_equal':True,'pairs_checked_by_definition':checked,
         'frozen_result_files_unchanged':len(load('results/publication_gap_audit/baseline.json')['frozen_results']),
         'scope':'Second local compiler/STL/runtime with existing independent full-PAF source, same host and frozen inputs; not external replication or a formal certificate.'})
    print('Replication audit passed',checked,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('stage',choices=['baseline','build','pilot','p5','p7','audit'])
    stage=parser.parse_args().stage
    if stage in ('p5','p7'): full(stage)
    else: globals()[stage]()
