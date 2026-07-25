# Order-428 reproduction plan

Status: planned; no order-428 matrix has yet been generated.

## Published route

Kharaghani and Tayfeh-Rezaie report a Turyn-type sequence \(TT(36)\), i.e.
four binary sequences of lengths \(36,36,36,35\). Their construction produces
base sequences with lengths \(71,71,36,36\), then T-sequences and an
order-428 Hadamard matrix. Numerically,

\[
428=4(71+36)=4\cdot107.
\]

## Reproduction protocol

1. Obtain and archive bibliographic metadata plus a lawful full text.
2. Independently transcribe every displayed source sequence twice. Compare the
   transcriptions by hash/diff before using either.
3. Implement nonperiodic autocorrelation and the exact \(TT(36)\) defining
   equations.
4. Verify the published quadruple before applying any transformation.
5. Implement the paper's \(TT(36)\to BS(71,71,36,36)\) map with explicit
   zero-based indexing and polynomial-coefficient conventions.
6. Verify the base-sequence norm identity exactly.
7. Implement each subsequent T-sequence / block-array transformation as a
   separately tested pure function.
8. Test every map first on the smallest published examples for which hand
   calculation is possible.
9. Construct `results/H428.csv` from source objects, never by downloading a
   finished 428 CSV.
10. Verify with both repository verifiers using `--order 428`, record hashes,
    and compare invariants with any published construction data.

## Ambiguities to resolve from the full paper

- whether sequence displays list coefficients from low to high degree;
- which autocorrelation convention (zero padding versus cyclic) applies at
  each stage;
- the reversal-matrix orientation in the final block array;
- signs and row/column order of the base-to-T transformation;
- whether the final 428 construction uses additional Williamson-type data.

None will be guessed silently. Each resolved convention will be documented
with a small exact test.

## Acceptance criteria

The reproduction is complete only when:

- the source sequence constraints pass exactly;
- each intermediate construction identity passes exactly;
- both independent verifiers accept the generated 428 CSV;
- a clean rerun produces the same candidate SHA-256; and
- the paper-to-code mapping is documented sufficiently for a third party.

## Resource estimate

Verifying a supplied \(TT(36)\) and constructing order 428 should be small
(one core, minutes, negligible storage). Searching anew for \(TT(36)\) is not
part of the reproduction plan and would require a separate estimate.
