# LP(27) proof-backend benchmark

Status: completed 2026-09-27 for the small LP(27) gate only. No LP(333)
solver run was made, and no order-668 result is claimed.

## Toolchain and format audit

The benchmark uses RoundingSat commit `d4edbf7` and VeriPB 3.0.2, the release
used in the SAT Competition 2026. The executables have SHA-256 values

```text
RoundingSat  12a98e4ca9e91cd0fe344e88760fe0eaced3c1e4cf377b5134379ef4fec9fedf
VeriPB       c3e3d547112c5cf0f9bf610438bb0b629a8699b85dcaa337ed0af55978bad676
```

The current RoundingSat proof logger requires the otherwise optional OPB
header fields `#equal` and `intsize`. The model writer now emits these fields,
with `#equal` equal to the number of equality records and `intsize=4`; this
does not alter any mathematical constraint. RoundingSat then expands each
equality into two inequalities, exactly matching the recorded normalized
constraint count. The toolchain choice and certificate workflow follow
`koops2025prooflogging` and the official software documentation
`roundingsat2026`, `veripb2026`.

## Exact certificate pipeline

For each of the unbroken and translation-canonical models, the tracked LP(27)
witness was checked in three independent ways before certificate generation:

1. exact Legendre PAF identities and prescribed length-three compression;
2. every record of the Python OPB model;
3. a complete VeriPB SAT certificate assigning all 756 variables, including
   the uniquely determined XOR auxiliaries.

VeriPB reported `VERIFIED SATISFIABLE` for both certificates. As a separate
interoperability check, a scratch OPB fixed all 756 variables to that exact
assignment; RoundingSat emitted its own proof log, which VeriPB also accepted.
The fixed instances are deliberately not presented as search results: their
only purpose is to test parsing, proof production, and proof checking end to
end.

| case | direct VeriPB wall / peak | fixed RoundingSat wall / peak | fixed-proof VeriPB wall / peak |
|---|---:|---:|---:|
| unbroken | 0.093 s / 8.34 MB | 0.070 s / 6.10 MB | 0.038 s / 8.89 MB |
| translation-canonical | 0.040 s / 8.43 MB | 0.063 s / 6.07 MB | 0.040 s / 8.99 MB |

The timings are single observations for pipeline validation, not comparative
performance claims. Complete commands, byte counts, hashes, exit codes, and
peak working sets are in `results/pb_backend_benchmark/metadata.json`.

## Bounded open-search observations

Two reproducible one-core probes used `--lp=0`, proof logging, and a ten-second
internal limit. Both returned `TIMELIMIT`:

| model | wall time | peak working set | incomplete proof size |
|---|---:|---:|---:|
| unbroken | 11.046 s | 12.57 MB | 19,414,411 bytes |
| translation-canonical | 11.056 s | 12.61 MB | 21,760,828 bytes |

These are failed search attempts, not certificates. An earlier default
LP-enabled unbroken run also timed out after 120 seconds and produced an
incomplete 158,697,560-byte proof (SHA-256
`07d5a9169c3ee29449fb23f5ad0aeb0fcd46002d96318a048de6e9cec9923c47`).
An LP-disabled canonical probe timed out after 60 seconds. The short probes do
not show a performance benefit from translation canonicalization; they are far
too small to support an asymptotic conclusion.

## Decision

The certificate pipeline gate is complete: the model format, RoundingSat
proof logger, and VeriPB checker interoperate, and exact memory/proof-size
measurements are available. The search-performance gate is not passed.
RoundingSat did not recover a known LP(27) witness under the tested bounded
open configurations, so extrapolating this encoding directly to LP(333) would
be unjustified.

The bounded p=5 fixed-witness validation is now complete; see
`p5_validation.md`. The next safe milestone is an exact implementation of the
paper's two-stage `q=3` uncompression model. No LP(333) solver run should be
requested until a backend solves an unfixed smaller instance and its
certificate verifies.

Reproduction command:

```powershell
python -m scripts.benchmark_pb_backend `
  --solver tmp\tools\roundingsat\roundingsat.exe `
  --verifier tmp\tools\veripb-3.0.2\bin\veripb.exe `
  --probe-seconds 10
```
