"""Preserve inherited artifacts and pin only this round's additions."""
import hashlib
import platform
import subprocess
import time

from scripts.primitive_local_audit import ROOT, load
from scripts.audit_compression_residue import BASE, OUT, save


def main():
    start = time.perf_counter()
    tracked = set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],
                                         cwd=ROOT, text=True).splitlines())
    changed = set(subprocess.check_output(['git','diff','--name-only',BASE],
                                         cwd=ROOT, text=True).splitlines())
    assert not tracked.intersection(changed), 'an inherited tracked file changed'
    for name in ('primitive_local','residue_formula'):
        for entry in load('results/'+name+'/manifest.json')['files']:
            assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest() == entry['sha256']
    inherited = load('results/residue_formula/integrity.json')
    inherited_paths = subprocess.check_output(['git','ls-tree','-r','--name-only',
        inherited['base_commit'],'results'], cwd=ROOT, text=True).splitlines()
    inherited_hash = hashlib.sha256()
    for path in inherited_paths:
        inherited_hash.update((path+' '+hashlib.sha256((ROOT/path).read_bytes()).hexdigest()+'\n').encode())
    assert len(inherited_paths) == inherited['baseline']['files']
    assert inherited_hash.hexdigest() == inherited['baseline']['ordered_path_sha256_digest']
    lines = subprocess.check_output(['git','ls-tree','-r',BASE,'results','paper'],
                                    cwd=ROOT, text=True).splitlines()
    aggregate = hashlib.sha256(); count = 0; paper = 0; total_bytes = 0
    legacy_crlf = []
    proc = subprocess.Popen(['git','cat-file','--batch'], cwd=ROOT,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for line in lines:
            assert time.perf_counter()-start < 120
            header, path = line.split('\t',1)
            oid = header.split()[2]
            proc.stdin.write((oid+'\n').encode()); proc.stdin.flush()
            fields = proc.stdout.readline().split()
            assert fields[0].decode() == oid and fields[1] == b'blob'
            size = int(fields[2]); blob = proc.stdout.read(size)
            assert len(blob) == size and proc.stdout.read(1) == b'\n'
            expected = hashlib.sha256(blob).hexdigest()
            local = (ROOT/path).read_bytes()
            actual = hashlib.sha256(local).hexdigest()
            if actual != expected:
                # Do not rewrite legacy artifacts. Their raw bytes were just
                # checked against the inherited frozen aggregate above.
                assert path in inherited_paths and local.replace(b'\r\n',b'\n') == blob, path
                legacy_crlf.append({'path': path, 'local_sha256': actual,
                                    'git_lf_sha256': expected})
            total_bytes += size
            if path.startswith('results/'):
                count += 1
                aggregate.update((path+' '+actual+'\n').encode())
            else:
                paper += 1
        proc.stdin.close()
        assert proc.wait(timeout=5) == 0
    finally:
        if proc.poll() is None:
            proc.kill(); proc.wait()
        proc.stdout.close()
    assert count == 6748
    baseline = {'result_files': count, 'paper_files': paper, 'total_bytes': total_bytes,
                'result_ordered_path_sha256_digest': aggregate.hexdigest(),
                'manuscript_sha256': hashlib.sha256((ROOT/'paper/manuscript.tex').read_bytes()).hexdigest()}
    save('integrity.json', {'base_commit': BASE, 'baseline': baseline,
         'inherited_raw_aggregate_matches_frozen_record': True,
         'git_blobs_match_except_preserved_legacy_crlf': legacy_crlf,
         'no_inherited_tracked_file_changed': True,
         'preceding_manifests_checked': ['primitive_local','residue_formula'],
         'manuscript_edited_or_compiled': False, 'explanatory_empty_fiber_theorem_proved': False,
         'originality_established': False, 'python': platform.python_version(),
         'platform': platform.platform(), 'seconds': time.perf_counter()-start,
         'workers': 1, 'cap_seconds': 120, 'caps_hit': False,
         'memory_estimate_bytes': 100_000_000})
    files = [p for p in OUT.iterdir() if p.is_file() and p.name != 'manifest.json']
    files += [ROOT/p for p in ('research/compression_residue_coupling.md',
        'scripts/compression_residue.py','scripts/audit_compression_residue.py',
        'scripts/package_compression_residue.py','tests/test_compression_residue.py')]
    entries = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
    save('manifest.json', {'base_commit': BASE, 'algorithm': 'sha256', 'files': entries})
    print({'baseline': baseline, 'new_files_pinned': len(entries),
           'new_bytes': sum(e['bytes'] for e in entries), 'seconds': time.perf_counter()-start})


if __name__ == '__main__':
    main()
