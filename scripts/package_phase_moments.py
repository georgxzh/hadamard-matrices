"""Package exploratory evidence only; preserve the paper and all old artifacts."""
from pathlib import Path
import hashlib
from scripts.phase_moment_obstruction import ROOT,OUT,load,save
from scripts.audit_phase_moments import digest


def main():
    assert digest()==load('results/phase_moments/audit.json')['baseline']
    paths=[p for p in OUT.iterdir() if p.is_file() and p.name!='manifest.json']
    paths += [ROOT/name for name in ('research/phase_moment_obstruction.md',
        'scripts/phase_moment_obstruction.py','scripts/study_phase_moments.py',
        'scripts/audit_phase_moments.py','scripts/challenge_phase_moment_refinement.py',
        'scripts/factor_phase_moment_defect.py','scripts/package_phase_moments.py',
        'tests/test_phase_moments.py')]
    entries=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,
              'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]
    save('manifest.json',{'algorithm':'sha256','files':entries})
    print({'files_pinned':len(entries),'frozen_files_preserved':6723,'paper_unchanged':True})


if __name__=='__main__':main()
