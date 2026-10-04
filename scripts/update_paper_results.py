"""Insert audited result tables/hashes into the standalone manuscript.

Does not run experiments or a TeX compiler. Refuses incomplete evidence.
"""
import json
import re
from pathlib import Path
from statistics import median

from scripts.classify_p5_lifts import ROOT, digest, save


def main():
    census=json.loads((ROOT/'results/p5_classification/metadata.json').read_text())
    audit=json.loads((ROOT/'results/p5_classification/audit.json').read_text())
    controls=json.loads((ROOT/'results/phase_controls/metadata.json').read_text())
    control_audit=json.loads((ROOT/'results/phase_controls/audit.json').read_text())
    isolated=json.loads((ROOT/'results/phase_controls/isolated_joins.json').read_text())
    propagation=json.loads((ROOT/'results/phase_propagation/metadata.json').read_text())
    propagation_audit=json.loads((ROOT/'results/phase_propagation/audit.json').read_text())
    assert propagation['complete'] and propagation_audit['status']=='passed'
    assert propagation_audit['manifest_sha256']==digest(ROOT/'results/phase_propagation/manifest.json')
    spectral_audit=json.loads((ROOT/'results/spectral_join/audit.json').read_text())
    assert spectral_audit['status']=='passed'
    assert spectral_audit['manifest_sha256']==digest(ROOT/'results/spectral_join/manifest.json')
    assert census['complete'] and audit['status']==control_audit['status']=='passed'
    assert audit['classification_sha256']==digest(ROOT/'results/p5_classification/classification.json')
    assert control_audit['metadata_sha256']==digest(ROOT/'results/phase_controls/metadata.json')
    assert isolated['source_sha256']==digest(ROOT/'scripts/benchmark_phase_isolated_joins.py')
    assert isolated['implementation_sha256']==digest(ROOT/'scripts/benchmark_phase_controls.py')
    table=[r'\begin{center}',r'\begin{tabular}{llrr}',r'\toprule',
           r'Branch / gauge & PAF evaluation & Median (s) & Range (s)\\',r'\midrule']
    for name in ('p5_rank1','p5_rank3'):
        for canonical in (0,1):
            for incremental in (0,1):
                r=isolated['summary'][f'{name}_canonical{canonical}_incremental{incremental}']
                table.append(f"{name.replace('p5_rank','Rank ')} / {'on' if canonical else 'off'} & "
                    f"{'incremental' if incremental else 'recompute'} & {r['median_seconds']:.3f} & "
                    f"{r['min_seconds']:.3f}--{r['max_seconds']:.3f}"+r'\\')
    table += [r'\bottomrule',r'\end{tabular}',r'\end{center}']
    section=r'''The controlled join comparison holds Gray traversal, mask maintenance,
projected coordinates, byte keys, multiplicity buckets, and stream hashing
fixed. Only the translation gauge and PAF evaluator change. Three repeats
per configuration run in a deterministic shuffled order. Ordered stream
hashes agree between the incremental and recomputed evaluators. Rank 1 gives
27 ordered lifts and rank 3 gives zero in every trial. A separate timing
batch ran with no concurrent repository computations; background OS load and
CPU frequency were not controlled. Its medians and ranges are:
'''+ '\n'.join(table)+r'''
The gauge reduces the two-row candidate scan exactly threefold,
from 708,588 to 236,196, while the pair-orbit reduction is ninefold.
With the gauge on, incremental updates improve the median by factors 1.10
and 1.07 on ranks 1 and 3; the timing ranges overlap. This is materially
less than the earlier single-trial comparison using different traversals.
There is no robust large update-only speedup claim.

The aligned PB comparison uses the same intermediate branches, projected
shifts, and binary lexicographic anchor gauges in both encodings. It uses
RoundingSat with LP reasoning disabled, restart multiplier 100, a ten-second
internal limit, proof logging, and a fifteen-second external timeout.
Three shuffled-order repetitions are timing replicates of deterministic
search, not independent random seeds. The results are:
\begin{center}
\begin{tabular}{lll}
\toprule
Branch & Binary PB & Phase PB\\\midrule
'''
    for branch,title in [('p3','$p=3$ known'),('p5_rank1','$p=5$ rank 1'),('p7','$p=7$ saved')]:
        values=[]
        for encoding in ('binary','phase'):
            records=[r['run'] for k,r in controls['solver_controls'].items() if k.startswith(branch+'_'+encoding+'_')]
            statuses={r['reported_status'] for r in records}
            assert len(records)==3 and len(statuses)==1
            status='SAT' if statuses=={'SATISFIABLE'} else 'timeout'
            values.append(f"3/3 {status}; {median(r['elapsed_seconds'] for r in records):.3f} s")
        section+=title+' & '+' & '.join(values)+r'\\'+'\n'
    section+=r'''\bottomrule
\end{tabular}
\end{center}
Each SAT result passed exact witness checks, full VeriPB proof verification,
and compact certificate verification. Timeouts remain unresolved in solver
records. The earlier 13.84-second census audit overlapped part of this PB
batch, so these wall times have that additional limitation. It cannot alter
the exact outcomes or justify ranking censored searches. The phase encoding
wins the tiny positive control, while both encodings fail the tested larger
budgets. Complete p=5 enumeration remains the stronger demonstrated route
for this restricted task, not a demonstrated scalable algorithm.

The artifact audit checked 139 hashes, regenerated 35 OPB files byte-for-byte,
and reverified 19 SAT proofs/certificates. All 156 repository tests passed
using an in-repository temporary directory. The first test attempt encountered
a system-temporary-directory permission error; that run is not counted as a
passing verification. The control batch took 253.16 seconds on one worker,
with a 39.04 MB Python-process peak and 206.90 MB of proof logs.
'''
    section+=f"The separate join batch took {isolated['elapsed_seconds']:.2f} seconds; "
    section+=f"its measured process peak was {isolated['peak_working_set_bytes']/1e6:.2f} MB.\n"
    artifacts=['results/intermediate_scaling/metadata.json','results/ternary_phase/metadata.json',
               'results/p5_branch_portfolio/canonical_branches.json',
               'results/p5_classification/classification.json','results/p5_classification/audit.json',
               'results/p5_classification/manifest.json','results/phase_controls/metadata.json',
               'results/phase_controls/isolated_joins.json','results/phase_controls/audit.json',
               'scripts/classify_p5_lifts.py','src/ternary_phase.py',
               'results/phase_propagation/metadata.json','results/phase_propagation/controls.json',
               'results/phase_propagation/census_validation.json',
               'results/phase_propagation/equivalence_crosswalk.json',
               'results/phase_propagation/audit.json','results/phase_propagation/manifest.json']
    artifacts += ['results/spectral_join/pilot.json','results/spectral_join/metadata.json',
                  'results/spectral_join/controls.json','results/spectral_join/p7_metadata.json',
                  'results/spectral_join/coefficients_63.json','results/spectral_join/full_paf_p7.json',
                  'results/spectral_join/independent_audit.json','results/spectral_join/audit.json',
                  'results/spectral_join/manifest.json']
    hashes=r'''The following SHA-256 values pin the principal evidence. The census
manifest also pins every branch record and symmetry map. The supplementary
\path{paper/artifact_manifest.json} pins the manuscript, scripts, tests,
and supporting records; it is regenerated only after the paper is updated.
\begin{description}
'''
    for path in artifacts:
        hashes+=r'\item[\normalfont\footnotesize\path{'+path+r'}] \hfill\break'+'\n'
        hashes+=r'{\footnotesize\texttt{'+digest(ROOT/path)+'}}\n'
    hashes+=r'\end{description}'
    paper=ROOT/'paper/manuscript.tex'; text=paper.read_text()
    from scripts.render_spectral_results import render
    for name,replacement in [('CONTROL_RESULTS',section),('SPECTRAL_RESULTS',render()),('ARTIFACT_HASHES',hashes)]:
        pattern=f'% {name}_BEGIN\n.*?% {name}_END'
        text,count=re.subn(pattern,lambda _:f'% {name}_BEGIN\n{replacement}\n% {name}_END',text,flags=re.S)
        assert count==1
    paper.write_text(text,encoding='utf-8',newline='\n')
    paths=[paper,Path(__file__),ROOT/'tests/test_p5_classification.py',
           ROOT/'scripts/audit_p5_classification.py',ROOT/'scripts/audit_ternary_phase.py',
           ROOT/'scripts/benchmark_phase_controls.py',ROOT/'scripts/benchmark_phase_isolated_joins.py',
           ROOT/'research/p5_classification.md',ROOT/'research/phase_controls.md',
           ROOT/'research/source_ledger.md',ROOT/'references/references.bib']
    paths.extend(ROOT/p for p in ('src/phase_propagation.py','scripts/benchmark_phase_propagation.py',
                                'scripts/crosswalk_p5_equivalence.py','scripts/audit_phase_propagation.py',
                                'tests/test_phase_propagation.py','tests/test_p5_equivalence.py',
                                'research/phase_propagation.md','research/direction_selection.md'))
    paths.extend(ROOT/p for p in ('src/spectral_join.cpp','src/spectral_join.py','src/full_paf_audit.cpp',
             'scripts/benchmark_spectral_join.py','scripts/audit_saved_p7.py','scripts/audit_spectral_join.py',
             'scripts/render_spectral_results.py','scripts/verify_spectral_paper.py',
             'tests/test_spectral_join.py','research/spectral_join.md','.gitattributes'))
    paths.extend(ROOT/p for p in artifacts)
    save(ROOT/'paper/artifact_manifest.json',{'algorithm':'sha256','files':[
        {'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(set(paths))]})
    print('Updated paper result blocks and artifact manifest.')


if __name__=='__main__': main()
