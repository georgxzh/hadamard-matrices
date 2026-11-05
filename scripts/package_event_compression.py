"""Freeze additions, checking raw inherited evidence and Git provenance."""
import hashlib
import platform
import subprocess
import time

from scripts.primitive_local_audit import ROOT, load
from scripts.audit_event_compression import BASE, OUT, save


def main():
    start = time.perf_counter()
    tracked = set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],
                                          cwd=ROOT,text=True).splitlines())
    changed = set(subprocess.check_output(['git','diff','--name-only',BASE],
                                          cwd=ROOT,text=True).splitlines())
    assert not tracked.intersection(changed)
    names = ('primitive_local','residue_formula','compression_residue')
    for name in names:
        for entry in load('results/'+name+'/manifest.json')['files']:
            assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest() == entry['sha256']
    inherited = load('results/compression_residue/integrity.json')
    old_paths = set(subprocess.check_output(['git','ls-tree','-r','--name-only',
        inherited['base_commit'],'results'],cwd=ROOT,text=True).splitlines())
    legacy = {e['path']:e for e in inherited['git_blobs_match_except_preserved_legacy_crlf']}
    lines = subprocess.check_output(['git','ls-tree','-r',BASE,'results','paper'],
                                    cwd=ROOT,text=True).splitlines()
    aggregate = hashlib.sha256(); old_hash = hashlib.sha256()
    count = paper = total_bytes = 0
    proc = subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,
                            stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    try:
        for line in lines:
            assert time.perf_counter()-start < 120
            header,path = line.split('\t',1); oid = header.split()[2]
            proc.stdin.write((oid+'\n').encode()); proc.stdin.flush()
            fields = proc.stdout.readline().split()
            assert fields[0].decode() == oid and fields[1] == b'blob'
            size = int(fields[2]); blob = proc.stdout.read(size)
            assert len(blob) == size and proc.stdout.read(1) == b'\n'
            expected = hashlib.sha256(blob).hexdigest()
            local = (ROOT/path).read_bytes(); actual = hashlib.sha256(local).hexdigest()
            if actual != expected:
                assert path in legacy
                assert actual == legacy[path]['local_sha256']
                assert expected == legacy[path]['git_lf_sha256']
                assert local.replace(b'\r\n',b'\n') == blob
            total_bytes += len(local)
            if path.startswith('results/'):
                count += 1; entry = (path+' '+actual+'\n').encode()
                aggregate.update(entry)
                if path in old_paths:
                    old_hash.update(entry)
            else:
                paper += 1
        proc.stdin.close(); assert proc.wait(timeout=5) == 0
    finally:
        if proc.poll() is None:
            proc.kill(); proc.wait()
        proc.stdout.close()
    assert count == 6753 and paper == 5
    assert len(old_paths) == inherited['baseline']['result_files']
    assert old_hash.hexdigest() == inherited['baseline']['result_ordered_path_sha256_digest']
    baseline = {'result_files':count,'paper_files':paper,'raw_bytes':total_bytes,
        'result_ordered_path_sha256_digest':aggregate.hexdigest(),
        'manuscript_sha256':hashlib.sha256((ROOT/'paper/manuscript.tex').read_bytes()).hexdigest()}
    save('integrity.json',{'base_commit':BASE,'baseline':baseline,
        'preceding_manifests_checked':names,'inherited_raw_aggregate_verified':True,
        'legacy_crlf_preserved':list(legacy.values()),'all_inherited_files_preserved':True,
        'manuscript_edited_or_compiled':False,'explanatory_empty_fiber_theorem_proved':False,
        'originality_established':False,'python':platform.python_version(),
        'platform':platform.platform(),'seconds':time.perf_counter()-start,
        'workers':1,'cap_seconds':120,'caps_hit':False})
    files = [p for p in OUT.iterdir() if p.is_file() and p.name != 'manifest.json']
    files += [ROOT/p for p in ('research/event_compression_products.md',
        'scripts/event_compression_products.py','scripts/audit_event_compression.py',
        'scripts/package_event_compression.py','tests/test_event_compression.py')]
    entries = [{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,
                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
    save('manifest.json',{'base_commit':BASE,'algorithm':'sha256','files':entries})
    print({'baseline':baseline,'new_files_pinned':len(entries),
           'new_bytes':sum(e['bytes'] for e in entries),'seconds':time.perf_counter()-start})


if __name__ == '__main__':
    main()
