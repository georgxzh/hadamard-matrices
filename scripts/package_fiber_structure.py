"""Pin the mathematical follow-up without rewriting any frozen result manifest."""
import json
from scripts.audit_fiber_structure import ROOT, OUT, sha


def entry(p):
    return {'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}


def write(p,v):
    p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')


def main():
    paths=[p for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json']
    paths += [ROOT/n for n in ('research/conditional_fiber_theorem.md',
        'scripts/audit_fiber_structure.py','scripts/package_fiber_structure.py',
        'tests/test_fiber_structure.py')]
    write(OUT/'manifest.json',{'algorithm':'sha256','files':[entry(p) for p in sorted(paths)]})
    paper=ROOT/'paper/artifact_manifest.json'
    old=json.loads(paper.read_text());mapped={e['path']:e for e in old['files']}
    for p in [*paths, OUT/'manifest.json', ROOT/'paper/manuscript.tex']:
        e=entry(p);mapped[e['path']]=e
    write(paper,{'algorithm':'sha256','files':[mapped[k] for k in sorted(mapped)]})
    compiler=OUT/'latex_status.json'
    if compiler.exists():
        status_path=ROOT/'paper/verification_status.json'
        status=json.loads(status_path.read_text());latex=json.loads(compiler.read_text())
        assert latex['manuscript_sha256']==sha(ROOT/'paper/manuscript.tex')
        status['native_latex_compilation']={'date':latex['date'],
            'status':latex['compilation'],'source_sha256':latex['manuscript_sha256'],
            'record':'results/fiber_structure/latex_status.json','visual_layout':'unverified'}
        status['fiber_structure_audit']='results/fiber_structure/audit.json'
        status['fiber_structure_manifest']='results/fiber_structure/manifest.json'
        write(status_path,status)
    print('Pinned mathematical follow-up; frozen result manifests unchanged.')


if __name__=='__main__':main()
