"""Build and validate exact OPB models for structured Legendre uncompression.

The length-27 model is exhaustively cross-checked against all 7,614 canonical
matches produced by the repository's p=3 factor-nine enumerator.  The
length-333 model is written only to ignored scratch storage so that its exact
byte size and SHA-256 can be recorded without committing a large generated
file.  No solver or order-333 search is run.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from src.legendre import structured_compressed_pair
from src.pb_model import OPBArtifact, UncompressionPBModel
from src.uncompress import search_uncompressions


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "pb_uncompression"
DEFAULT_SCRATCH = REPOSITORY_ROOT / "tmp" / "pb_models"
CANONICAL_P3_MATCHES = 7_614


def _artifact_record(artifact: OPBArtifact, *, tracked: bool) -> dict[str, object]:
    try:
        path = artifact.path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        path = str(artifact.path)
    return {
        "path": path,
        "bytes": artifact.bytes,
        "mib": round(artifact.bytes / 2**20, 3),
        "sha256": artifact.sha256,
        "tracked": tracked,
    }


def _signs(sequence: tuple[int, ...]) -> str:
    return "".join("+" if value == 1 else "-" for value in sequence)


def build(
    output_directory: Path = DEFAULT_OUTPUT,
    scratch_directory: Path = DEFAULT_SCRATCH,
) -> dict[str, object]:
    """Build both models and validate the small one without invoking a solver."""

    started_at = datetime.now(timezone.utc)
    started = perf_counter()
    output_directory.mkdir(parents=True, exist_ok=True)
    scratch_directory.mkdir(parents=True, exist_ok=True)

    small_first, small_second = structured_compressed_pair(3, 3)
    small_model = UncompressionPBModel(small_first, small_second, 9)
    small_artifact = small_model.write_opb(output_directory / "lp27_structured.opb")
    constraints = tuple(small_model.iter_constraints())

    enumeration_started = perf_counter()
    search = search_uncompressions(
        small_first,
        small_second,
        9,
        collect=CANONICAL_P3_MATCHES,
    )
    enumeration_seconds = perf_counter() - enumeration_started
    if search.matched_first_candidates != CANONICAL_P3_MATCHES:
        raise RuntimeError(
            f"p=3 enumerator returned {search.matched_first_candidates} canonical matches; "
            f"expected {CANONICAL_P3_MATCHES}"
        )
    if len(search.solutions) != CANONICAL_P3_MATCHES:
        raise RuntimeError("not every canonical p=3 match was materialized")

    validation_started = perf_counter()
    for match_index, (first, second) in enumerate(search.solutions):
        failure = small_model.first_failed_constraint(first, second, constraints=constraints)
        if failure is not None:
            raise RuntimeError(
                f"canonical p=3 match {match_index} violates OPB record {failure}"
            )
    validation_seconds = perf_counter() - validation_started

    witness_first, witness_second = search.solutions[0]
    witness = {
        "status": "exact satisfying base assignment; XOR auxiliaries are uniquely derived",
        "first": _signs(witness_first),
        "second": _signs(witness_second),
        "negative_positions_first_zero_based": [
            index for index, value in enumerate(witness_first) if value == -1
        ],
        "negative_positions_second_zero_based": [
            index for index, value in enumerate(witness_second) if value == -1
        ],
        "model_sha256": small_artifact.sha256,
    }
    (output_directory / "lp27_witness.json").write_text(
        json.dumps(witness, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    large_first, large_second = structured_compressed_pair(37, 3)
    large_model = UncompressionPBModel(large_first, large_second, 9)
    large_started = perf_counter()
    large_artifact = large_model.write_opb(scratch_directory / "lp333_structured.opb")
    large_write_seconds = perf_counter() - large_started

    metadata: dict[str, object] = {
        "status": (
            "exact model construction and small-case validation only; no LP(333) "
            "search and no order-668 result"
        ),
        "deterministic": True,
        "random_seed": None,
        "binary_convention": "x_i=1 exactly when sequence sign i is -1",
        "indexing": "zero-based sequence positions; shifts 1..floor(L/2)",
        "model": (
            "compression cardinalities plus exact XOR disagreement variables; "
            "for each shift sum(disagreements in both rows)=L+1"
        ),
        "symmetry_breaking": "none; this is the unbroken reference model",
        "lp27": {
            "compressed_first": list(small_first),
            "compressed_second": list(small_second),
            "stats": asdict(small_model.stats),
            "opb": _artifact_record(small_artifact, tracked=True),
            "enumerator_semantics": (
                "one second-row representative is stored per PAF signature; "
                "7,614 is the number of matching first-row candidates, not a "
                "multiplicity-weighted count of all ordered pairs"
            ),
            "canonical_matches_exhaustively_checked": len(search.solutions),
            "ordered_pairs_represented": search.ordered_pairs_found,
            "enumeration_seconds": round(enumeration_seconds, 6),
            "constraint_validation_seconds": round(validation_seconds, 6),
            "witness": "results/pb_uncompression/lp27_witness.json",
        },
        "lp333": {
            "compressed_first": list(large_first),
            "compressed_second": list(large_second),
            "stats": asdict(large_model.stats),
            "opb": _artifact_record(large_artifact, tracked=False),
            "write_seconds": round(large_write_seconds, 6),
            "search_run": False,
            "xor_to_cnf_clause_count": large_model.stats.xor_inequalities,
            "remaining_cnf_clause_count": (
                "encoder-dependent: 74 compression and 166 correlation "
                "equalities are retained natively in OPB"
            ),
            "memory_statement": (
                "the recorded OPB byte size is an exact input-file measure, not "
                "a solver-memory forecast; solver memory is backend-dependent"
            ),
            "certificate_plan": (
                "require a solver witness checked by src.legendre for SAT; for "
                "UNSAT require a VeriPB-checkable proof plus the exact OPB SHA-256"
            ),
        },
        "started_utc": started_at.isoformat(),
        "elapsed_seconds_this_run": round(perf_counter() - started, 6),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "logical_cpu_count": os.cpu_count(),
        "cpu_cores_used": 1,
        "peak_memory": "not instrumented",
        "command": "python -m scripts.build_uncompression_opb",
    }
    (output_directory / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scratch-directory", type=Path, default=DEFAULT_SCRATCH)
    args = parser.parse_args()
    metadata = build(args.output_directory.resolve(), args.scratch_directory.resolve())
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
