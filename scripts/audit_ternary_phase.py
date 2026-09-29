"""Verify saved ternary/control artifacts, regenerate OPBs, rerun certificates."""
from __future__ import annotations

import json
import time
from pathlib import Path

from scripts.classify_p5_lifts import ROOT, digest, save
from scripts.benchmark_phase_controls import AlignedPhaseModel
from scripts.benchmark_staged_uncompression import _known_pair, _verify_certificate
from src.legendre import compress, structured_compressed_pair
from src.staged_uncompression import FactorThreeBranch, IntermediatePBModel
from src.ternary_phase import TernaryPhasePBModel


def artifact_records(value):
    if isinstance(value,dict):
        if 'path' in value and 'sha256' in value: yield value
        for child in value.values(): yield from artifact_records(child)
    elif isinstance(value,list):
        for child in value: yield from artifact_records(child)


def audit():
    started=time.perf_counter()
    output=ROOT/'results/phase_controls'
    old=json.loads((ROOT/'results/ternary_phase/metadata.json').read_text())
    controls=json.loads((output/'metadata.json').read_text())
    assert 'completed_utc' in controls
    assert controls['source_sha256']==digest(ROOT/'scripts/benchmark_phase_controls.py')
    records=list(artifact_records(old))+list(artifact_records(controls))
    unique={r['path']:r for r in records}
    for record in unique.values():
        path=ROOT/record['path']
        assert path.is_file() and digest(path)==record['sha256'],record['path']
        assert path.stat().st_size==record['bytes']
    catalog=json.loads((ROOT/'results/p5_branch_portfolio/canonical_branches.json').read_text())
    branches={'p3':tuple(compress(row,9) for row in _known_pair(3)),
              'p5_rank1':tuple(tuple(catalog[0][k]) for k in ('first','second')),
              'p7':tuple(tuple(row) for row in old['branch_acquisition'][0]['pair'])}
    scratch=ROOT/'tmp/audit_phase'; scratch.mkdir(parents=True,exist_ok=True)
    verifier=ROOT/'tmp/tools/veripb-3.0.2/bin/veripb.exe'
    regenerated=[]; verified=[]
    for dataset,models,aligned in [(ROOT/'results/ternary_phase',old['models'],False),
                                    (output,controls['solver_controls'],True)]:
        for label,record in models.items():
            name=next(name for name in branches if label.startswith(name+'_'))
            pair=branches[name]; p=len(pair[0])//3
            model=(FactorThreeBranch(*structured_compressed_pair(p,3),*pair).model(
                canonical_translations=True,projected_correlations=True) if '_binary_' in label else
                (AlignedPhaseModel(*pair) if aligned else TernaryPhasePBModel(*pair)))
            generated=scratch/f'{label}.opb'; model.write_opb(generated)
            opb=ROOT/record['opb']['path']
            assert digest(generated)==digest(opb)
            assert vars(model.stats)==record['stats']
            regenerated.append(record['opb']['path'])
            if record['run']['reported_status']=='SATISFIABLE':
                for field in ('certificate','search_proof'):
                    proof=ROOT/record[field]['path']
                    result=_verify_certificate(verifier,opb,proof,scratch/f'{label}_{field}_veripb.txt')
                    assert result['exit_code']==0
                    verified.append(record[field]['path'])
            else:
                assert record['run']['reported_status']=='TIMELIMIT' or record['run']['externally_timed_out']
    for name,record in old['validation'].items():
        if 'opb' not in record: continue
        if name=='p7_intermediate':
            model=IntermediatePBModel(*structured_compressed_pair(7,3),canonical_translations=True)
        else: model=TernaryPhasePBModel(*branches[name])
        generated=scratch/f'{name}_known.opb'; model.write_opb(generated)
        opb=ROOT/record['opb']['path']; proof=ROOT/record['certificate']['path']
        assert digest(generated)==digest(opb)
        regenerated.append(record['opb']['path'])
        assert _verify_certificate(verifier,opb,proof,scratch/f'{name}_known_veripb.txt')['exit_code']==0
        verified.append(record['certificate']['path'])
    report={'status':'passed','elapsed_seconds':time.perf_counter()-started,
            'artifact_hashes_checked':len(unique),'opbs_regenerated':len(regenerated),
            'sat_certificates_and_logs_reverified':len(verified),
            'metadata_sha256':digest(output/'metadata.json'),
            'prior_ternary_metadata_sha256':digest(ROOT/'results/ternary_phase/metadata.json'),
            'audit_source_sha256':digest(Path(__file__)),
            'regenerated_models':regenerated,'verified_proofs':verified,
            'limitation':'Timeout logs are preserved unresolved; certificates establish SAT witnesses, not exhaustive counts.'}
    save(output/'audit.json',report)
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__': audit()
