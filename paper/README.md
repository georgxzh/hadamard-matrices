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

The source was requested in the native editor. Three native compilation
attempts returned `Unable to find standard directories for platform`, an
environment error before source diagnostics. Consequently **PDF compilation
and visual layout are unverified**. No terminal TeX installation was added.
The source and editor request were preserved. The final build-status record
documents this limitation separately from successful computational audits.

Outstanding scholarly work: compare the later pq² and fast spectral
algorithms in full, obtain/crosswalk earlier length-45 representatives under
matching conventions, and seek independent external replication. The p=7
saved branch is still unresolved. Authorship is intentionally left pending.
