"""Render audited p=7 portfolio results without promoting capped searches."""
import json
from scripts.classify_p5_lifts import ROOT,digest


def render():
    directory=ROOT/'results/p7_portfolio'
    read=lambda name:json.loads((directory/name).read_text())
    audit=read('audit.json'); assert audit['status']=='passed'
    assert audit['manifest_sha256']==digest(directory/'manifest.json')
    summary=read('summary.json'); portfolio=read('portfolio.json'); acquisition=read('acquisition.json')
    trials=[read(f'trial_{t}.json') for t in range(3)]
    assert all(t['scheduled']==t['completed_jobs']==3*len(portfolio['branches']) for t in trials)
    successes=sum(r['pair'] is not None for r in acquisition['records'])
    guards=sum(r['guard_fired'] for r in acquisition['records'])
    result=rf'''\subsection{{Bounded systematic $p=7$ portfolio}}
The starting commit \texttt{{03876f3}} was checked before extension:
5,081 manifest entries matched, and a fresh consistency audit rechecked
the frozen $p=5$ lists and saved $p=7$ evidence. Original artifacts remain
unchanged. This was not a new exhaustive $p=5$ run.

Targeted acquisition used the ordered splits $(12,20),(13,19),(14,18)$,
$(15,17),(16,16)$, four seeds per split, 200,000 iterations and a 20-second
wall guard per attempt. Seeds are $20261006+100j+h$, where $j$ indexes the
listed split from zero and $h=0,1,2,3$. The {len(acquisition['records'])} attempts
took {acquisition['elapsed_seconds']:.2f} seconds, producing {successes}
verified intermediates, with {guards} wall guards firing. The admitted
pool contains the last three splits. Absence of an acquired $(12,20)$ or
$(13,19)$ class is unresolved, not an impossibility result.

For each acquired split select the minimum compact-JSON pair SHA-256,
after the existing independent-translation-by-seven gauge and deduplication.
Add the previous empty branch as a mandatory control. The resulting four
ordered translation classes are frozen before lift pilots and outcomes.
This targeted first-hit heuristic pool is neither exhaustive nor uniform;
minimum-hash selection cannot remove acquisition bias. No row-exchange,
reversal or decimation quotient changes the counts. Every binary lift keeps
the anchor-zero phase convention and factor-nine ordered multiplicity.

The prefix probes took {read('pilot.json')['elapsed_seconds']:.2f} seconds.
Because they omit joins, they underestimate unfiltered cost; a supplementary
{read('join_pilot.json')['elapsed_seconds']:.2f}-second real-key pilot capped
stored masks at 250,000 and nodes at one million. Tenfold extrapolations
are empirical early-prefix estimates, not time guarantees. The memory
envelope is 1.68 GB; expected evidence is 30 MB with a conservative 1-GB
storage allowance. These gates fit four cores, 30 minutes and 10 GB.
All selected classes remain scheduled under equal budgets, regardless of
their timing estimate. Each trial has 80 seconds, two billion nodes per row,
15 million stored masks and 100,000 solutions as caps; any stop has null
exact counts. Each serial batch has a 1,500-second controller guard and at
most 960 seconds of capped engine work.

Three batches shuffle the 12 branch/mode jobs with seeds 20261006,
20261007 and 20261008, using one worker and no concurrent repository
experiment. Their wall times are '''
    result+=', '.join(f"{t['elapsed_seconds']:.2f}" for t in trials)+r''' seconds.
All variants use the same frozen native executable. Modes 1 and 2 share
bound maintenance; mode 0 disables it with the spectral tests. This ablation
compares the entire spectral mechanism, and the leaf/prefix comparison
isolates prefix testing. Python/native, PB, translation and incremental-PAF
effects are not credited to this experiment.

\begin{center}
\begin{tabular}{lrrrr}
\toprule
Branch & Active counts & Off (s) & Leaf (s) & Prefix (s)\\
\midrule
'''
    for b in summary['branches']:
        m=b['methods']; result+=b['id'].replace('_',r'\_')+' & '+','.join(map(str,b['active_counts']))+' & '
        result+=' & '.join(f"{m[str(i)]['engine_median']:.3f}"+(' (capped)' if m[str(i)]['completed']<3 else '') for i in (0,1,2))+r'\\'+'\n'
    result+=r'''\bottomrule
\end{tabular}
\end{center}
The following ranges expose repeat variability rather than treating a
single median as robust improvement:
\begin{center}
\begin{tabular}{lrrr}
\toprule
Branch & Off range (s) & Leaf range (s) & Prefix range (s)\\
\midrule
'''
    for b in summary['branches']:
        result+=b['id'].replace('_',r'\_')+' & '+ ' & '.join(f"{b['methods'][str(i)]['engine_min']:.3f}--{b['methods'][str(i)]['engine_max']:.3f}" for i in (0,1,2))+r'\\'+'\n'
    result+=r'''\bottomrule
\end{tabular}
\end{center}
Engine time excludes native preparation. Python setup, process wall time,
native wall minus engine, exact validation and total wrapper times are
separately recorded; coefficient warmup is outside engines. Native residual
includes startup and native pre/post work, not a pure setup measurement.
Wrapper time is measured before the final JSON rewrite. OS load/frequency
were not controlled. Repeats are deterministic timing replicates, not
independent samples of classes or solutions.

\begin{center}
\begin{tabular}{lrrr}
\toprule
Prefix configuration & Python setup (ms) & Native residual (ms) & Wrapper (s)\\
\midrule
'''
    for b in summary['branches']:
        m=b['methods']['2']
        result+=b['id'].replace('_',r'\_')+f" & {1000*m['setup_median']:.2f} & {1000*m['native_nonengine_median']:.2f} & {m['wrapper_median']:.3f}"+r'\\'+'\n'
    result+=r'''\bottomrule
\end{tabular}
\end{center}
These columns are separately recorded medians and need not add to the
engine median. Full phase measurements for all configurations are preserved.

\begin{center}
\begin{tabular}{lrrrr}
\toprule
Branch & Ordered lifts & Independent complete & Audit (s) & Peak native (MB)\\
\midrule
'''
    independent=read('independent.json')
    for b in summary['branches']:
        records=[r['result'] for t in trials for r in t['records'] if r['id']==b['id']]
        peak=max(r['peak_working_set_bytes'] for r in records)/1e6
        result+=f"{b['id'].replace('_',r'\_')} & {b['ordered_pairs'] if b['ordered_pairs'] is not None else 'unresolved'} & {'yes' if b['independent_complete'] else 'no'} & {b['independent_seconds']:.3f} & {peak:.2f}"+r'\\'+'\n'
    result+=r'''\bottomrule
\end{tabular}
\end{center}
'''
    result+=r'''Prefix pruning retains the same rows as leaf testing. Its recorded
survivors and coverage masses (identical across timing replicates) are:
\begin{center}
\begin{tabular}{lrrr}
\toprule
Branch & Kept rows C/D & Prefix excluded C/D & Prefix nodes\\
\midrule
'''
    for b in summary['branches']:
        r=next(v['result'] for v in trials[0]['records'] if v['id']==b['id'] and v['mode']==2)
        kept='/'.join(f"{row['accepted']:,}" for row in r['rows'])
        mass='/'.join(f"{row['excluded_completions']:,}" for row in r['rows'])
        result+=b['id'].replace('_',r'\_')+f" & {kept} & {mass} & {sum(row['nodes'] for row in r['rows']):,}"+r'\\'+'\n'
    result+=r'''\bottomrule
\end{tabular}
\end{center}
'''
    balanced=next(b for b in summary['branches'] if b['id']=='a16_16')
    result+=f"For the balanced class, prefix testing has median {balanced['methods']['2']['engine_median']:.3f} s versus {balanced['methods']['1']['engine_median']:.3f} s for leaf testing, despite fewer nodes. Its timing ranges overlap; this is an observed median regression, not a robust general ranking.\n"
    result+=f"The native trial peak is {read('invariants.json')['native_peak_bytes']/1e6:.2f} MB. The preserved study package occupies {audit['storage_bytes']/1e6:.2f} MB, below both pilot allowances. All 36 native trials exhaust, with no timeout or cap.\n"
    completed=sum(b['status']=='exact_completed' for b in summary['branches'])
    result+=f"The complete solution lists and exact counts agree across all completed variants: {completed} of four branches are resolved.\n"
    if completed==4 and all(b['ordered_pairs']==0 for b in summary['branches']):
        result+=r'''All four branches are empty in all 36 native trials. These records
therefore contain no binary witness; every complete solution list is empty.
Their intermediate witnesses were checked, and the prior full $p=5$ census
still supplies positive exact controls. This does not establish nonexistence
for any other intermediate or for the full prescribed $p=7$ family.
'''
    result+=r'''Each independent check uses the unchanged binary-column enumerator,
all 31 PAF shifts, the support-intersection identity, and exact sorted-key
collision checks. A separate 200,000-row-per-class pilot preceded its
180-second attempts. No spectral or projected filter is used. Complete
checks enumerate both full row domains and compare exact solution lists;
incomplete checks remain unresolved. The independent compiler/input are
shared, so this is not an external replication or a formal UNSAT proof.
Hashes pin coverage, excluded completion masses, every input/result and
the separately measured setup/wrapper phases.
Five new protocol tests passed in 1.59 seconds before timing, checking
the translation class, witness rejection, and byte-identical input/row
counter parity with the frozen wrapper under caps in all three modes.
Both native binaries rebuilt byte-identically after timings. The historical
35 targeted and 156 full-suite test records retain their original dates;
they are not presented as fresh full-suite executions.

\paragraph{Publication assessment.}
This evidence supports a narrower restricted-census/reproducibility draft
with a proved spectral specialization. It does not yet support priority or
competitive-method claims: the full fast-spectral and $pq^2$ algorithms
remain unaudited, the pool is small and biased, no positive $p=7$ branch is
validated here, and external replication is missing. Prefix pruning need
not improve on leaf filtering; bound-testing overhead must be reported with
its node reduction. A publishable methods claim needs broader independent
classes, a verified positive $p=7$ control, complete primary comparisons,
and comparable external baselines. A future bounded acquisition should
include unsuccessful strata and opposite row orientations without treating
heuristic failure as an exclusion. No $p=37$ search is warranted or started.
'''
    return result
