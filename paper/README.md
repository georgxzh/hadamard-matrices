# Research-paper draft

`manuscript.tex` is a standalone LaTeX source for the built-in Codex editor.
It includes its bibliography, proved mathematical setup, the completed
restricted p=5 census, controlled benchmarks, reproducible commands and
artifact hashes. It distinguishes established results, independent
reproductions and unresolved novelty questions. Order 668 is motivation;
there is no proximity claim and no p=37 search.

The complete length-45 classification already reported by Fletcher, Gysin
and Seberry (2001) is explicitly credited. This draft concerns a fixed
compression family and does not establish new LP(45) existence or a first
length-45 classification.

`artifact_manifest.json` pins the source and evidence. To refresh completed
result blocks after rerunning the corresponding audits:

```powershell
.venv/Scripts/python.exe -m scripts.update_paper_results
```

The source remains in the native editor. Earlier compilation attempts failed
with missing platform directories or `setup refresh had errors`. The built-in
desktop compiler succeeded on October 11, 2026. **Visual PDF layout remains
unverified**. No terminal TeX installation was added. The current result and
saved-source hash are in `../results/publication_gap_audit/latex_status.json`.

The October 10 publication-gap audit is in
`../research/publication_gap_audit.md`. Publisher/author/repository searches
did not recover full fast-spectral/pq² algorithms or the historical complete
length-45 list; priority and the historical crosswalk remain unresolved.
The positive p=7 control is complete: three anchor-fixed pairs, 27 ordered
fixed-intermediate lifts. All four negative p=7 classes are exhausted.

New Clang/MSVC replication and the branch/class incidence artifact are kept
separately under `../results/publication_gap_audit/`. This is local toolchain
replication, not independent external replication. The strongest candidate
is a conditional census and reproducibility/software contribution, with no
claim of first classification, algorithmic priority, or submission readiness.
Authorship, archival release, external replication and visual PDF layout review
remain gates alongside the literature gaps.

After a completed new replication, use
`python -m scripts.render_publication_gap` to refresh its manuscript section
and supplementary manifests. The older updater handles historical blocks;
run the new renderer afterward if using it. Neither renderer compiles TeX.
