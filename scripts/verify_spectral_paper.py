"""Verify frozen manifests and static TeX structure; does not compile a PDF."""
import json
import re
from scripts.classify_p5_lifts import ROOT,digest,save


def main():
    manifests=['paper/artifact_manifest.json','results/p5_classification/manifest.json',
               'results/phase_propagation/manifest.json','results/spectral_join/manifest.json',
               'results/p7_portfolio/manifest.json','results/p7_positive_control/manifest.json']
    checked=0
    for name in manifests:
        for entry in json.loads((ROOT/name).read_text())['files']:
            path=ROOT/entry['path']
            assert digest(path)==entry['sha256'],entry['path']
            assert path.stat().st_size==entry['bytes'],entry['path']
            checked+=1
    paper=ROOT/'paper/manuscript.tex'
    source=re.sub(r'(?<!\\)%[^\n]*','',paper.read_text())
    depth=0
    for brace in re.findall(r'(?<!\\)[{}]',source):
        depth+=1 if brace=='{' else -1
        assert depth>=0,'unbalanced braces'
    assert depth==0,'unbalanced braces'
    stack=[]
    for action,name in re.findall(r'\\(begin|end)\{([^}]+)\}',source):
        if action=='begin': stack.append(name)
        else: assert stack.pop()==name,'mismatched environments'
    assert not stack,'unclosed environments'
    bibliography=set(re.findall(r'\\bibitem\{([^}]+)\}',source))
    for citation in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',source):
        assert set(citation.split(','))<=bibliography,citation
    labels=set(re.findall(r'\\label\{([^}]+)\}',source))
    for reference in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',source):
        assert reference in labels,reference
    for marker in ('CONTROL_RESULTS','PROPAGATION_RESULTS','SPECTRAL_RESULTS','P7_PORTFOLIO_RESULTS','P7_POSITIVE_RESULTS','ARTIFACT_HASHES'):
        assert paper.read_text().count(f'% {marker}_BEGIN')==1
        assert paper.read_text().count(f'% {marker}_END')==1
    pilot=json.loads((ROOT/'results/spectral_join/pilot.json').read_text())
    native=ROOT/'tmp/spectral_join.exe'
    if native.exists(): assert digest(native)==pilot['native_sha256'],'rebuilt executable differs'
    independent=json.loads((ROOT/'results/spectral_join/independent_audit.json').read_text())
    binary=ROOT/'tmp/full_paf_audit.exe'
    if binary.exists(): assert digest(binary)==independent['binary_sha256'],'independent executable differs'
    for key,filename in (('manifest_sha256','manifest.json'),):
        audit=json.loads((ROOT/'results/spectral_join/audit.json').read_text())
        assert audit[key]==digest(ROOT/'results/spectral_join'/filename)
    files=[p for p in (ROOT/'results/spectral_join').rglob('*') if p.is_file()]
    storage=sum(p.stat().st_size for p in files)
    assert storage<10_000_000_000
    record=json.loads((ROOT/'paper/verification_status.json').read_text())
    record.update(manifests_checked=manifests,manifest_entries_checked=checked,
                  manuscript_sha256=digest(paper),spectral_audit='results/spectral_join/audit.json',
                  independent_p7_audit='results/spectral_join/independent_audit.json',
                  spectral_storage_bytes=storage,spectral_artifact_files=len(files),
                  static_tex_checks='balanced braces/environments; citations/references and result markers resolve; no PDF/layout check')
    record['spectral_extension_tests']={
        'command':'.venv/Scripts/python.exe -m pytest tests/test_spectral_join.py tests/test_phase_propagation.py tests/test_p5_equivalence.py tests/test_ternary_phase.py tests/test_p5_classification.py -q --basetemp=tmp/pytest_spectral_final',
        'reported_result':'35 passed in 22.29s',
        'provenance':'Completed tool output on 2026-10-04; verifier records this result and does not rerun tests'}
    record.update(p7_portfolio_audit='results/p7_portfolio/audit.json',
                  p7_portfolio_storage_bytes=sum(p.stat().st_size for p in (ROOT/'results/p7_portfolio').rglob('*') if p.is_file()))
    positive=json.loads((ROOT/'results/p7_positive_control/audit.json').read_text())
    assert positive['manifest_sha256']==digest(ROOT/'results/p7_positive_control/manifest.json')
    assert positive['summary']['complete'] and positive['summary']['canonical_pairs']==3 and positive['summary']['ordered_pairs']==27
    record.update(p7_positive_audit='results/p7_positive_control/audit.json',
                  p7_positive_storage_bytes=sum(p.stat().st_size for p in (ROOT/'results/p7_positive_control').rglob('*') if p.is_file()),
                  p7_positive_outcome='Published prescribed LP(63) reproduced; positive fixed branch independently exhausted: 3 canonical / 27 ordered lifts')
    record['p7_protocol_tests']={
        'command':'.venv/Scripts/python.exe -m pytest tests/test_p7_study.py -q --basetemp=tmp/pytest_p7_protocol',
        'reported_result':'5 passed in 1.59s',
        'provenance':'Completed tool output on 2026-10-06, before portfolio timings; verifier does not rerun tests'}
    save(ROOT/'paper/verification_status.json',record)
    print(json.dumps({'manifest_entries_checked':checked,'spectral_artifact_files':len(files),
                      'spectral_storage_bytes':storage,'static_tex_checks':'passed',
                      'manuscript_sha256':digest(paper)},indent=2))


if __name__=='__main__': main()
