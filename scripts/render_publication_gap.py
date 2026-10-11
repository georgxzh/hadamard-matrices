"""Update only the publication-gap block and supplementary paper manifest.

Frozen experiment files, code, and earlier generated result blocks are untouched.
Call again after writing compiler/test status to refresh the new evidence manifest.
"""
import re
from pathlib import Path
from scripts.publication_gap_replication import ROOT, OUT, load, save, sha

def main():
    a=load('results/publication_gap_audit/replication_audit.json')
    p5=load('results/publication_gap_audit/p5_summary.json')
    p7=load('results/publication_gap_audit/p7_summary.json')
    assert a['status']=='passed' and p5['complete'] and p7['complete']
    text=r'''\section{Publication-gap audit and revised contribution}\label{sec:gap}
This October 10, 2026 audit starts from commit
\path{e76084054f594f2af89831cc377d88994ba7b4e6} on
\path{agent/order-428-reproduction}. All 5,330 pre-existing manifest entries
matched before editing. The frozen census, four empty $p=7$ classes, positive
control, source files and provenance records are preserved byte for byte.
The new evidence is in \path{results/publication_gap_audit/}; the complete
access ledger and reproduction procedure are in
\path{research/publication_gap_audit.md}.

\paragraph{What could be original.}
The strongest defensible candidate is an auditable conditional lifting
dataset and software workflow: every binary solution fiber over the 1,164
prescribed intermediate translation classes at $p=5$, with exact
multiplicities, explicit symmetry maps, and incidence with the 63 classes
under the published equivalence; five individually exhausted $p=7$ fibers
provide four negative cases and one published positive control. The rational
spectral enclosures and exact matching are useful checked specializations.
Neither their priority nor the dataset's first-publication status is
established. These are candidate artifact contributions, not a new existence
result, a first classification, or a new general search principle.

\paragraph{Access boundary and comparison.}
Fresh publisher HTML and PDF requests for \cite{perera,pq2} returned HTTP 403.
Public OpenAlex records listed only the publisher DOI for each, with no PDF
location. The fast-spectral institutional record linked only its DOI.
Exact-title, author, arXiv and institutional-repository searches located no
accessible complete algorithm. The Cantabria repository was robots-restricted
through the web service. The open-access label on \cite{pq2} did not provide
full-text access in this session. No authors were contacted. Full algorithms,
code and numerical conventions in these two papers remain unread; abstract
claims are not used to fill those gaps or infer performance superiority.

\begin{longtable}{p{.20\linewidth}p{.49\linewidth}p{.22\linewidth}}
\toprule
Axis & Present implementation & Full \cite{perera,pq2} comparison\\\midrule
\endhead
Domain & Fixed prescription; all $p=5$ intermediate classes, five selected
$p=7$ fibers & Unknown beyond headline abstract scope\\
Symmetry & Two free translation gauges; proved 79-case transfer, also
directly checked over all 1,164 classes & Unresolved\\
Pruning & Necessary rational PSD enclosures and exact PAF; no conjectural
trace or complexity exclusions & Unresolved\\
Matching & All masks retained, full-key equality on hash collisions,
all matching bucket combinations & Unresolved\\
Lifting & $p\to3p\to9p$ with complete minority-phase parameterization & Unresolved\\
Numerics & Integer acceptance keys; outward error bounds; strict rejection
retains threshold equality & Unresolved\\
\bottomrule
\end{longtable}

Accessible text still establishes substantial prior overlap. The indexed
primary Section 4.1 of \cite{issac} gives the complete listed sequence of
intermediate generation, decimation reduction, conjectural trace/complexity
discard and binary lifting; its C source was offered on request. We do not
adopt the conjectural discard or infer undocumented bucket counts. Appendix A's
displayed DFT helper uses \texttt{evalf}; a search-wide numerical error bound
was not supplied in the accessible sections. This is a predecessor comparison,
not a reading of the later $pq^2$ algorithm.
In \cite[Section 3.4, Algorithm 1]{lumsden}, every equal-signature bucket
combination is retained; Sections 4.1--4.2, Theorem 3 and Algorithms 2--3
give multilevel compression and recursive preimages. Section 3.4 explicitly
rounds PSD values to nearest integers and checks matches. That text addresses
false positives, but supplies no rigorous rounding bound excluding missed
matches. We do not assert an observed failure. Exact integer PAF keys avoid
this issue in our implementation. The periodic Golay domain is distinct;
its equivalence and timing results are not binary Legendre baselines.

\paragraph{Historical data and conditional branch structure.}
Both the journal and author copies of \cite{fletcher} were obtained.
Printed p.\ 83, below Table 3, offers the complete lists on request;
the author version's PDF p.\ 8 says the same and describes compatible
decimation-class records. The public copies contain samples, not all 3,058
representatives. Author publication/library pages and targeted searches did
not recover the full list. Thus no historical record-by-record crosswalk is
claimed, and our 63 local labels are not historical record identifiers.

An exact reorganization of the frozen solutions gives the following new
incidence summary; no new binary solutions were generated for this table.
\begin{center}
\begin{tabular}{rr}\toprule
Distinct LP classes reached by one intermediate class & Intermediate classes\\\midrule
0 & 460\\ 1 & 496\\ 2 & 160\\ 3 & 48\\\bottomrule
\end{tabular}
\end{center}
There are 960 nonzero intermediate/LP-class incidences: 928 contain three
phase-gauged solutions, and 32 contain six. Of the 63 LP classes, 57 meet
16 intermediate classes each and six meet eight each. The exact incidence
matrix, local canonical masks and multiplicities are retained in
\path{conditional_incidence.json}. This records failed intermediates,
fiber sizes and the distribution of equivalent lifts across branches.
A global count alone does not display this information, but a complete
historical representative list with exact orbit expansion and compression
could recover it. It is a refinement of established classification data,
not logically new existence information. Whether that refinement was
previously computed or published remains unresolved.

The pending crosswalk must preserve the historical encoding and record IDs,
decode any compatible-decimation-class format, validate PAFs, normalize row
sums and canonicalize under the actual Section 5.4 operations. It must then
compare keys and expand the relevant orbits to recover the prescribed fibers.
Count agreement alone cannot identify representatives or certify the list.

\paragraph{Fresh second-toolchain replication.}
The unchanged \path{src/full_paf_audit.cpp} was compiled with Clang 22.1.8,
Microsoft STL 14.44.35207, \texttt{lld-link}, and \texttt{libcmt}, separately
from GCC 15.2.0/MinGW/libstdc++. The compiler required \texttt{-include string}
because the original source relied on a transitive header include. This
compiler flag preserves the frozen source. The compiler driver record pins
headers, target, linker, flags and executable hash.
This is a separate local compiler/STL/runtime execution of the existing
independent full-PAF implementation. It is not a third newly written
enumerator, a different machine, or external independent replication.
The Python runtime and input catalogue are shared. First-stage catalogue
completeness retains its previous audit; it was not independently rederived.

The six-stratum $p=5$ pilot projected 577.31 seconds with a twofold margin.
Capped $p=7$ prefixes gave tenfold-margin estimates of 196.76--919.48 seconds,
omitting large-table sort/lookup costs; these are not completion guarantees.
The admitted trial used one worker, 240-second native and 250-second hard
per-case caps, a 1,500-second controller guard, a 2-GB memory allowance and
100-MB output allowance. The conservative table allocation was 805,306,368
bytes. Stopped pilots remained unresolved, never empty.
'''
    text+=f'''
All 1,164 $p=5$ branches were directly exhausted in {p5['elapsed_seconds']:.2f}
seconds, matching every one of the 2,976 canonical mask pairs and the count
histogram $(460,464,192,48)$ for ordered counts $(0,27,54,81)$.
All five $p=7$ classes were directly exhausted in {p7['elapsed_seconds']:.2f}
seconds, with the same four empty lists and the same three positive
anchor-fixed pairs (27 ordered fixed-intermediate lifts). No full trial hit
a cap. Maximum native peak working sets were
{p5['max_peak_working_set_bytes']/1e6:.2f} MB and
{p7['max_peak_working_set_bytes']/1e6:.2f} MB respectively (decimal MB).
The read-only audit compared all exact lists and coverage counters and
checked all 2,979 reported pairs by full integer PAF and compression.
It verified preservation of {a['frozen_result_files_unchanged']:,} frozen result files.
'''
    text+=r'''
Each command below is a separate bounded stage, run serially from the root:
\begin{verbatim}
.venv/Scripts/python.exe -m scripts.publication_gap_replication baseline
.venv/Scripts/python.exe -m scripts.publication_gap_replication build
.venv/Scripts/python.exe -m scripts.publication_gap_replication pilot
.venv/Scripts/python.exe -m scripts.publication_gap_replication p5
.venv/Scripts/python.exe -m scripts.publication_gap_replication p7
.venv/Scripts/python.exe -m scripts.publication_gap_replication audit
.venv/Scripts/python.exe -m scripts.publication_gap_incidence
\end{verbatim}
For external replication, use a fresh checkout/output location, record the
environment and any launcher adaptations, rerun pilots under the same limits,
and compare full solution sets rather than counts alone. The research note
specifies Linux build adaptations and warns that the native Windows memory
counter is unmeasured on other systems. No Linux run is claimed.

\paragraph{Revised submission assessment.}
The evidence supports developing a narrow reproducibility/software paper
centered on conditional fibers and auditable exact computation. A novel
methods or general classification research-paper claim is not supported.
Submission remains gated by the full algorithm/priority comparison,
historical-list crosswalk, external replication and archival release,
authorship/expository review, and visual PDF layout review. The built-in
compiler succeeded on October 11; visual layout inspection remains pending.
No standalone formal exhaustion certificate is available. Broader
predetermined $p=7$ strata are needed for statistical/scaling claims, not
as a substitute for these evidence gaps. More optimization is not the next
priority. No $p=37$ search follows from this assessment.

\paragraph{New evidence hashes.}
The supplementary manifest \path{results/publication_gap_audit/manifest.json}
pins all new records and scripts; \path{paper/artifact_manifest.json} pins
the saved manuscript and that manifest. SHA-256 identifies evidence, not
mathematical exhaustion. Principal hashes follow.
\begin{description}
'''
    for name in ('build.json','resource_plan.json','p5_summary.json','p7_summary.json',
                 'replication_audit.json','conditional_incidence.json','access_probes.json'):
        text+=r'\item[\normalfont\footnotesize\path{'+name+r'}] \hfill\break'+'\n'
        text+=r'{\footnotesize\texttt{'+sha(OUT/name)+'}}\n'
    text+=r'\end{description}'+'\n'
    paper=ROOT/'paper/manuscript.tex'; source=paper.read_text()
    source=source.replace(r'\date{October 9, 2026}',r'\date{October 10, 2026}')
    source=source.replace('memory measurements; porting and hardware comparisons remain untested.',
                          'memory measurements; the second local Clang build is audited in\nSection~\\ref{sec:gap}; other operating systems and hardware remain untested.')
    begin='% PUBLICATION_GAP_BEGIN'; end='% PUBLICATION_GAP_END'
    block=begin+'\n'+text+end+'\n\n'
    if begin in source: source=re.sub(begin+r'\n.*?'+end+r'\n\n',lambda _:block,source,flags=re.S)
    else: source=source.replace(r'\section{Reproduction and outstanding work}',block+r'\section{Reproduction and outstanding work}')
    paper.write_text(source,encoding='utf8',newline='\n')
    paths=[p for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json']
    paths += [ROOT/'research/publication_gap_audit.md']
    paths += list((ROOT/'scripts').glob('*publication_gap*.py'))
    save(OUT/'manifest.json', {'algorithm':'sha256','files':[{'path':p.relative_to(ROOT).as_posix(),
         'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(paths)]})
    old=load('paper/artifact_manifest.json')
    mapped={e['path']:e for e in old['files']}
    for p in [paper,OUT/'manifest.json',*paths]:
        name=p.relative_to(ROOT).as_posix()
        mapped[name]={'path':name,'bytes':p.stat().st_size,'sha256':sha(p)}
    save(ROOT/'paper/artifact_manifest.json',{'algorithm':'sha256','files':[mapped[k] for k in sorted(mapped)]})
    print('Updated publication-gap section and supplementary manifests.')

if __name__=='__main__': main()
