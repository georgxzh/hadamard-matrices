"""Render completed positive-control evidence without rerunning experiments."""
import json
from scripts.classify_p5_lifts import ROOT


def render():
    out=ROOT/'results/p7_positive_control'
    read=lambda name:json.loads((out/name).read_text())
    s=read('summary.json'); w=read('witness.json'); audit=read('audit.json')
    assert s['complete'] and s['prescribed_family'] and s['canonical_pairs']==3 and s['ordered_pairs']==27
    text=r'''\subsection{Published positive $p=7$ control (October 9, 2026)}
The previous portfolio and its assessment above are frozen historical evidence.
The next control is deliberately selected from a published positive example,
not from the heuristic pool: Section 5.3.3 of \cite{issac} prints two length-63
rows. The primary publisher's indexed HTML supplied the numerical block;
direct retrieval returned HTTP 403. \path{results/p7_positive_control/witness.json}
pins its locator, transcription, signs and verification vectors. We use the
first printed element as index zero. Standalone nested integer loops verify
all 62 nonzero PAF sums are $-2$, both row sums are 1, and the combined
negative-support difference counts are 30 (each block has size 31).
The printed pair has exactly the prescribed length-seven compression
\[
(1,3,3,-3,3,-3,-3),\qquad(1,-3,-3,3,-3,3,3).
\]
It therefore validates the prescribed family, beyond merely testing an
unrelated domain. Its existence is established literature, independently
reproduced here; trace and linear-complexity assertions are not reverified.

\paragraph{Normalization and count convention.}
The length-21 rows are minimized independently among shifts $0,7,14$;
the chosen shifts are 0 and 14. In each binary row the first active minority
phase is then moved to zero by a further shift of 21. With the convention
$x'[j]=x[(j+t)\bmod63]$, the recovered primary representative has total
shifts 21 and 35 and negative masks
\[
7677489779817452654,\qquad 5050907891639286294.
\]
The resulting intermediate is
\begin{align*}
C={}&(-1,-1,-1,-1,1,-3,-1,-1,3,1,1,\\
 &\hspace{1em}1,-1,-1,3,1,3,-3,1,1,-1),\\
D={}&(-1,-3,1,1,-3,3,3,1,1,-3,1,\\
 &\hspace{1em}-1,-1,-1,1,-1,-1,1,1,1,1).
\end{align*}
This translation class differs from the four frozen empty classes.

\begin{proposition}
This normalization preserves every PAF equation, and each anchor-fixed
pair above $(C,D)$ represents exactly nine ordered fixed-intermediate lifts.
\end{proposition}
\begin{proof}
For any cyclic shift $t$, replacing the summation index $j$ by $j+t$ in
$\sum_jx[j+t]x[j+s+t]$ preserves $\PAF_x(s)$. A shift by 7 at length 21
preserves length-seven compression. A binary shift by 21 preserves $(C,D)$
and subtracts one from each minority phase modulo 3. Since each row has
active residues, neither nontrivial such shift fixes it. Each independent
row action is free of size three; their product has size nine. This is the
existing gauge applied to a known witness and introduces no pruning rule
or additional exchange, reversal or decimation quotient.
\end{proof}

\paragraph{Resource gates and controlled recovery.}
Both rows have 16 active entries, giving $3^{15}=14,348,907$ anchor-fixed
candidates each. The 400,000-node probes omit table work; in particular
their mode-zero estimate understates the join cost. Real capped table
pilots preceded full attempts, with 10-fold empirical timing extrapolations
of 30.68, 31.65 and 21.95 seconds for off, leaf and prefix modes.
These pilot caps remain unresolved, not exact branch outcomes.
The conservative allocation/reallocation envelope is 1.676 GB and the
storage allowance 100 MB. Full attempts use one worker, a 180-second time
cap, two billion nodes per row, 14,348,907 stored masks and 100,000 solutions.
Three serial batches shuffle the three modes with seeds 20261009--20261011.
The native implementation and compiler binary hashes match the frozen
baseline; only the control harness is new. The old virtual-environment
launcher could not find its base executable, so the bundled Python 3.12.14
was used. Timing phases are measured separately; no concurrent experiment
ran, while background OS load and clock frequency were not controlled.

\begin{center}
\begin{tabular}{lrrr}
\toprule
Mode & Engine median (s) & Range (s) & Wrapper median (s)\\\midrule
'''
    for row in s['native_summary']:
        low,high=row['engine_range_seconds']
        text+=['Off','Leaf spectral','Prefix spectral'][row['mode']]+f" & {row['median_engine_seconds']:.3f} & {low:.3f}--{high:.3f} & {row['median_wrapper_seconds']:.3f}"+r'\\'+'\n'
    text+=r'''\bottomrule
\end{tabular}
\end{center}
All nine trials exhaust to identical complete lists containing the published
control: three anchor-fixed pairs and 27 ordered lifts of this fixed
intermediate. \path{solutions.json} expands and verifies all 27 distinct
ordered masks; repeated PAF keys retain every mask in the native table.
This is a conditional count, not a count of the entire prescribed family.
Leaf/prefix timing ranges overlap, so their median order supports no
universal ranking. Median setup costs are 0.006--0.007 seconds; native
process time minus engine time is 0.031--0.051 seconds; witness validation
adds approximately 0.003 seconds. Exact per-run phases are retained.
Leaf and prefix modes retain 35,223 and 34,746 masks on the two sides.
Prefix mode excludes 10,821,357 and 10,850,193 completion masses before
leaves. Every exhausted row satisfies its exact coverage identity.
'''
    text+=f"The three batch walls are {', '.join(f'{x:.2f}' for x in s['batch_walls'])} seconds. The largest native process peak is {max(x['peak_working_set_bytes'] for x in s['native_summary'])/1e6:.2f} MB.\n"
    text+=r'''
The independent full-PAF pilot enumerates 200,000 candidates and estimates
92.39 seconds with a tenfold margin and a 1.118 GB envelope. After all
native sets agree, the unchanged binary-column enumerator exhausts both
full row domains using all 31 nonredundant PAF shifts and support-intersection
keys, with no spectral or projected filter.
'''
    text+=f"It returns the same three pairs and ordered count 27 in {s['independent_engine_seconds']:.2f} seconds, with peak {s['independent_peak_bytes']/1e6:.2f} MB.\n"
    text+=r'''Standalone definition/SDS checks additionally verify every emitted
pair at all 62 nonzero shifts, including the 27 expanded ordered pairs.
This is independent implementation evidence, sharing input and compiler,
not external replication or a formal exhaustion certificate. The four old
empty classes and all frozen census/source manifests remain byte-identical;
the baseline read-only audit checked 5,258 manifest entries without rerunning
the censuses. The new complete list closes the positive-control gap but
does not create an unbiased five-class sample or a global $p=7$ census.

\paragraph{Full-algorithm access and revised publication assessment.}
The primary abstract of \cite{perera} describes arbitrary odd-length DFT
computation using matrix spectra and an FFT-like algorithm; \cite{pq2}
describes fixed partial sums at length $pq^2$ with decimation, coset and SDS
techniques. Neither full algorithm was retrieved. Publisher HTML/PDF,
author/institutional records, targeted repository/preprint/code searches,
and public Crossref/OpenAlex location discovery were checked lawfully.
The institutional record for \cite{perera} links only the DOI; metadata
lists only publisher locations for both papers. The advertised publisher
API returns only core metadata in its default view and HTTP 401 for FULL
view. The $pq^2$ paper is marked CC BY 4.0, but its algorithm body remains
inaccessible in this session. Failed discovery does not prove no copy exists.
\path{literature_access.json} records the limits; no missing procedure is
assumed absent and no paywall workaround or author messaging is used.

\begin{longtable}{p{.18\linewidth}p{.33\linewidth}p{.38\linewidth}}
\toprule
Dimension & This audited implementation & Limits of primary comparison\\\midrule
\endhead
Domain & Fixed prescribed branch at $L=27,45,63$. & Fast spectral abstract:
odd lengths; $pq^2$ abstract: fixed partial sums. Exact domains unaudited.\\
Symmetry & Ordered rows; intermediate translations and free phase anchors. &
Fast spectral quotient unknown; $pq^2$ mentions decimation/cosets, exact
quotient and multiplicities unknown.\\
Pruning & Necessary PSD ceiling, rational partial rectangles, strict rejection. &
Fast spectral matrix/DFT framework known from abstract; detailed search
tests in both algorithms unknown.\\
Matching & Exact projected PAF keys, complete buckets, full collision checks. &
Both full matching algorithms inaccessible.\\
Lifting & Bijective ternary columns with every cross term and carry. &
Both full lifting procedures inaccessible; compression is established.\\
Numerical safety & Certified integer coefficients and final integer PAFs. &
Error bounds, tolerances and acceptance checks of both algorithms unaudited.\\
\bottomrule
\end{longtable}

The strongest defensible contribution remains a restricted census and
reproducibility artifact: the complete 1,164-class $p=5$ census, four
conditional empty $p=7$ classes and one complete positive fixed branch,
with explicit multiplicities, proved specializations and controlled filter
ablation. Compression, PSD exclusion, matching and published LP(63)
existence are established; their reproduction here is not a new existence
result. Priority of the rational prefix rectangle and conditional census
artifact remains unresolved. A competitive methods or first-method paper
is not supported. Before submission, obtain full primary algorithms and
code, compare the historical complete length-45 lists, secure external
replication and an archival release, confirm authorship and verify PDF
compilation/layout. Broader predetermined $p=7$ sampling may be needed
depending on the chosen scope. Evidence gaps take priority over further
optimization; no extrapolation to $p=37$ or proximity to order 668 follows.

\paragraph{Reproduction.}
Use the frozen executable hashes; the current harness allows a fresh output
directory inside the repository. Python 3.12.14 was used in this milestone.
\begin{verbatim}
# PowerShell: set to the bundled or an equivalent Python executable.
$positivePython = 'python'
$env:HADAMARD_POSITIVE_OUT = 'tmp/p7_positive_replication'
& $positivePython -m scripts.p7_positive_control setup
& $positivePython -m scripts.p7_positive_control pilot
& $positivePython -m scripts.p7_positive_control join-pilot
& $positivePython -m scripts.p7_positive_control trial 0
& $positivePython -m scripts.p7_positive_control trial 1
& $positivePython -m scripts.p7_positive_control trial 2
& $positivePython -m scripts.p7_positive_control independent-pilot
& $positivePython -m scripts.p7_positive_control independent
& $positivePython -m scripts.p7_positive_control audit
Remove-Item Env:HADAMARD_POSITIVE_OUT
\end{verbatim}
The initial and timing protocol snapshots preserve the actual source hashes
used before later audit refinements. Fresh runs use the current script;
their caps remain unresolved if exhaustion fails. See
\path{research/p7_positive_control.md} for exact runtime/build paths and the
lawful metadata probe command. The positive-control manifest pins all
inputs, complete sets, pilot limits, timing phases and literature receipts.
'''
    return text
