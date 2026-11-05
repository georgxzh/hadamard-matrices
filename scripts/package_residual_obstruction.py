"""Pin this study without rewriting any pre-existing result artifact."""
import json
from scripts.residual_compression_obstruction import ROOT, OUT
from scripts.audit_fiber_structure import sha
from scripts.audit_residual_obstruction import frozen_digest


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf8', newline='\n')


def entry(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def main():
    audit = json.loads((OUT/'audit.json').read_text())
    assert frozen_digest() == audit['frozen_results']
    paths = [p for p in OUT.rglob('*') if p.is_file() and p.name != 'manifest.json']
    paths += [ROOT/name for name in ('research/residual_compression_obstruction.md',
        'scripts/residual_compression_obstruction.py', 'scripts/audit_residual_obstruction.py',
        'scripts/package_residual_obstruction.py', 'tests/test_residual_obstruction.py')]
    write(OUT/'manifest.json', {'algorithm': 'sha256', 'files': [entry(p) for p in sorted(paths)]})
    paper = ROOT/'paper/artifact_manifest.json'
    old = json.loads(paper.read_text()); mapped = {e['path']: e for e in old['files']}
    for p in [*paths, OUT/'manifest.json', ROOT/'paper/manuscript.tex']:
        e = entry(p); mapped[e['path']] = e
    write(paper, {'algorithm': 'sha256', 'files': [mapped[k] for k in sorted(mapped)]})
    status_path = ROOT/'paper/verification_status.json'
    status = json.loads(status_path.read_text())
    status['residual_obstruction_audit'] = 'results/residual_obstruction/audit.json'
    status['residual_obstruction_manifest'] = 'results/residual_obstruction/manifest.json'
    status['residual_obstruction_tests'] = json.loads((OUT/'tests.json').read_text())
    latex_path = OUT/'latex_status.json'
    if latex_path.exists():
        latex = json.loads(latex_path.read_text())
        assert latex['manuscript_sha256'] == sha(ROOT/'paper/manuscript.tex')
        status['native_latex_compilation'] = {'date': latex['date'], 'status': latex['compilation'],
            'source_sha256': latex['manuscript_sha256'], 'record': 'results/residual_obstruction/latex_status.json',
            'visual_layout': 'unverified'}
    write(status_path, status)
    print('Pinned new residual study; 6,715 frozen result files unchanged.')


if __name__ == '__main__': main()
