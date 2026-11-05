"""Verify inherited evidence and pin this round's new files only."""
import hashlib
import platform
import subprocess

from scripts.primitive_local_audit import ROOT,load
from scripts.verify_primitive_local import frozen_digest
from scripts.audit_residue_formula import OUT,save

BASE='d441e0d8bfe6052c6574ca3702f1b3d40129ff7e'


def main():
    assert frozen_digest()==load('results/primitive_local/verification.json')['baseline']
    for e in load('results/primitive_local/manifest.json')['files']:
        assert hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256']
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'results'],cwd=ROOT,text=True).splitlines()
    changed=subprocess.check_output(['git','diff','--name-only',BASE,'--','results','paper'],cwd=ROOT,text=True).splitlines()
    assert not set(changed).intersection(paths) and not any(p.startswith('paper/') for p in changed)
    h=hashlib.sha256()
    for name in paths:h.update((name+' '+hashlib.sha256((ROOT/name).read_bytes()).hexdigest()+'\n').encode())
    baseline={'files':len(paths),'ordered_path_sha256_digest':h.hexdigest(),
        'manuscript_sha256':hashlib.sha256((ROOT/'paper/manuscript.tex').read_bytes()).hexdigest()}
    save('integrity.json',{'base_commit':BASE,'baseline':baseline,'all_frozen_artifacts_preserved':True,
        'manuscript_edited_or_compiled':False,'python':platform.python_version(),'platform':platform.platform(),
        'formula_deliverable_proved':True,'explanatory_empty_fiber_theorem_proved':False,
        'originality_established':False,'mathematical_advance_beyond_saved_point_evaluation':True})
    files=[p for p in OUT.iterdir() if p.is_file() and p.name!='manifest.json']
    files += [ROOT/p for p in ('research/residue_carry_formula.md','scripts/residue_formula.py',
        'scripts/audit_residue_formula.py','scripts/challenge_residue_formula.py',
        'scripts/package_residue_formula.py','tests/test_residue_formula.py')]
    entries=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,
        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
    save('manifest.json',{'base_commit':BASE,'algorithm':'sha256','files':entries})
    print({'baseline':baseline,'files_pinned':len(entries),'new_bytes':sum(e['bytes'] for e in entries)})


if __name__=='__main__':main()
