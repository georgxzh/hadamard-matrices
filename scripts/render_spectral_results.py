"""Render only completed, audited spectral results into the manuscript."""
import json
from scripts.classify_p5_lifts import ROOT


def render():
    directory=ROOT/'results/spectral_join'
    read=lambda name:json.loads((directory/name).read_text())
    pilot=read('pilot.json'); full=read('metadata.json'); controls=read('controls.json')
    p7=read('p7_metadata.json'); independent=read('full_paf_p7.json'); audit=read('audit.json')
    storage=sum(p.stat().st_size for p in directory.rglob('*') if p.is_file())
    assert full['complete'] and audit['status']=='passed' and independent['complete']
    result=rf'''\subsection{{Spectral milestone: direct census validation and one empty $p=7$ branch}}
The 12-case pilot took {pilot['elapsed_seconds']:.2f} seconds on three workers,
including native compilation and bounded $p=7$ row probes. Its estimates
were {pilot['estimated_p5_full_seconds_with_margin']:.2f} seconds and
{pilot['estimated_p5_worker_memory_bytes_with_margin']/1e6:.2f} MB for the full
$p=5$ validation, and {pilot['estimated_p7_seconds_per_method_with_margin']:.2f}
seconds per $p=7$ method with a tenfold timing margin. The $p=7$ memory
envelope was 1.2 GB; the initial storage estimate was 20 MB. These fit the
four-core, 30-minute, 10-GB limits. The deterministic early-prefix probes
are not a random sample or a proven runtime upper bound.

The full validation finished in {full['elapsed_seconds']:.2f} seconds on three
workers, reusing 12 pilot cases. Every one of the 1,164 catalogue branches
was directly enumerated by both native modes 0 and 2, with no symmetry reuse.
Exact solution lists agree with the independent frozen census: 460 empty
branches, 464 with 27 ordered lifts, 192 with 54, and 48 with 81. All 2,976
canonical mask pairs are retained. The conservative sum of Python-wrapper and
native-worker peaks is {full['python_plus_native_worker_bound_bytes']/1e6:.2f}
MB; it sums process maxima, not simultaneous whole-system measurements.

The sum of native engine times over the catalogue was
{full['engine_seconds_sum']['0']:.2f} seconds without spectral tests and
{full['engine_seconds_sum']['2']:.2f} seconds with prefix tests. These concurrent
measurements do not isolate timing effects. A separate one-worker batch
ran three shuffled replicates per configuration, with no concurrent
repository experiment. Its medians, in seconds, are:
\begin{{center}}
\begin{{tabular}}{{lrrrr}}
\toprule
Branch & Existing Python join & Native, off & Native, leaf & Native, prefix\\
\midrule
'''
    for name,title in (('p3','$p=3$'),('p5_rank1','Rank 1'),('p5_rank3','Rank 3'),('p5_rank1133','Rank 1133')):
        values=[controls['summary'][f'{name}_mode{mode}']['median_seconds'] for mode in ('python',0,1,2)]
        result+=title+' & '+' & '.join(f'{v:.4f}' for v in values)+r'\\'+'\n'
    result+=r'''\bottomrule
\end{tabular}
\end{center}
Native engine time excludes setup and process startup; wrapper wall times
are recorded separately. The Python/native comparison changes execution
language, traversal, PAF evaluation, and mask retention, so it is not an
isolated measure of spectral pruning. The native modes share traversal,
full-key lookup, mask retention, and exact verification. Prefix filtering
improves the recorded $p=5$ medians but slows the tiny $p=3$ control.
Ranges overlap on ranks 1 and 3; rank 1133 has disjoint recorded ranges
(off: 0.164--0.179 s; prefix: 0.073--0.130 s). These three deterministic
replicates are too narrow for a broad performance claim.

All three native modes exhaust the saved length-21 intermediate pair at
$p=7$ with \emph{zero} canonical and ordered binary lifts. The exact domains
have $3^{14}=4{,}782{,}969$ and $3^{16}=43{,}046{,}721$ anchor-zero rows.
The observed single-run resources are:
\begin{center}
\begin{tabular}{lrrr}
\toprule
Method & Engine seconds & Stored masks & Native peak (MB)\\
\midrule
'''
    for mode,title in (('0','Unfiltered'),('1','Leaf spectral'),('2','Prefix spectral')):
        r=p7['results'][mode]; assert r['complete'] and r['ordered_pairs']==0
        result+=f"{title} & {r['elapsed_seconds']:.3f} & {r['table_entries']:,} & {r['peak_working_set_bytes']/1e6:.2f}"+r'\\'+'\n'
    result+=r'''\bottomrule
\end{tabular}
\end{center}
Leaf and prefix tests retain the same 38,907 stored-side rows and 28,134
partner-side rows. Prefix exclusion accounts for 3,126,363 and 36,148,041
complete phase tuples respectively, before visiting leaves. The compact
table capacity falls from 369.10 MB to 2.88 MB. The prefix run is about
9.9 times faster than this matched unfiltered run; this is one branch and
one trial per method, not an estimate of general scaling. There is no
binary witness because the branch is empty. The intermediate witness and
its earlier checked constraints remain distinct from binary liftability.

An additional independent auditor enumerates Cartesian binary residue
patterns, uses the negative-support intersection PAF identity at all 31
nonredundant shifts, and sorts fingerprints with exact full-key collision
checks. It uses no spectral coefficients or projected equations. Positive
and empty $p=5$ controls reproduce 27 and zero ordered lifts. A bounded
pilot estimated 169.56 seconds and 406.11 MB; the complete $p=7$ audit
enumerates all 4,782,969 and 43,046,721 rows and again returns zero, in
54.75 seconds with a 140.52 MB native peak. This independently checks
computational nonexistence for the saved intermediate pair, conditional
on the two implementations and coverage arguments. It supplies no formal
UNSAT certificate and does not exclude other $p=7$ intermediates or any
length-63 Legendre pair in another branch.

The next justified experiment is a bounded portfolio of other verified
$p=7$ intermediate translation classes, initially with balanced active
counts, retaining exact per-branch outcomes and new pilot gates. The
single-row enumeration is still exponential, and no $p=37$ run follows
from these results. Hashes below pin the coefficient certificates, all
branch inputs/results, source, compiler configuration, and independent
audit. The larger package exceeds its 20-MB storage estimate because it
preserves each native input, while remaining far below the 10-GB limit.
All 35 targeted tests passed in 22.29 seconds, including native modes,
coefficient bounds, cap semantics, phase propagation, ternary formulation,
equivalence conventions, and prior classification checks. The historical
156-test full-suite result predates these extensions; it was not rerun here.
'''
    result+=f'The preserved spectral evidence occupies {storage/1e6:.2f} MB.\n'
    return result
