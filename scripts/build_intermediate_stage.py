"""Build and verify exact first-stage q=3 intermediate artifacts.

The bounded computation exhaustively enumerates the length-3p intermediate
rows at p=3 and p=5, joins their exact PAF signatures, emits OPB models, and
checks the known branch certificates with VeriPB.  It does not create or solve
an LP(333) instance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from src.legendre import (
    compress,
    decode_signs,
    published_structured_legendre_pair_45,
    structured_compressed_pair,
)
from src.pb_certificate import write_veripb_sat_certificate
from src.staged_uncompression import (
    IntermediatePBModel,
    intermediate_signature,
    search_intermediate_pairs,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "intermediate_stage"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _recorded_path(path: Path) -> str:
    try:
        return path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        return str(path)


def _artifact(path: Path) -> dict[str, object]:
    return {
        "path": _recorded_path(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _known_pair(prime: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if prime == 5:
        return published_structured_legendre_pair_45()
    if prime != 3:
        raise ValueError("artifact builder supports only p=3 and p=5")
    record = json.loads(
        (REPOSITORY_ROOT / "results" / "pb_uncompression" / "lp27_witness.json").read_text(
            encoding="utf-8"
        )
    )
    return decode_signs(record["first"]), decode_signs(record["second"])


def _verify(verifier: Path, opb: Path, proof: Path, output: Path) -> dict[str, object]:
    started = time.perf_counter()
    completed = subprocess.run(
        [str(verifier), "--stats", str(opb), str(proof)],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        timeout=120,
        check=False,
    )
    text = (completed.stdout + completed.stderr).decode("utf-8", errors="replace")
    output.write_text(text, encoding="utf-8", newline="\n")
    if completed.returncode != 0 or "s VERIFIED SATISFIABLE" not in text:
        raise RuntimeError(f"VeriPB rejected {proof.name}")
    return {
        "command": [str(verifier), "--stats", _recorded_path(opb), _recorded_path(proof)],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "exit_code": completed.returncode,
        "status": "VERIFIED SATISFIABLE",
        "stdout": _artifact(output),
    }


def _row(row: Sequence[int]) -> list[int]:
    return [int(value) for value in row]


def build(verifier: Path, output_directory: Path = DEFAULT_OUTPUT) -> dict[str, object]:
    """Build deterministic models/certificates and measured enumeration metadata."""

    verifier = verifier.resolve()
    if not verifier.is_file():
        raise FileNotFoundError(verifier)
    output_directory.mkdir(parents=True, exist_ok=True)
    cases: dict[str, object] = {}
    for prime in (3, 5):
        prescribed = structured_compressed_pair(prime, 3)
        binary = _known_pair(prime)
        intermediate = compress(binary[0], 3 * prime), compress(binary[1], 3 * prime)
        model = IntermediatePBModel(*prescribed)
        if model.first_failed_constraint(*intermediate) is not None:
            raise RuntimeError(f"known p={prime} intermediate branch failed its exact model")

        tracemalloc.start()
        started = time.perf_counter()
        search = search_intermediate_pairs(*prescribed)
        enumeration_seconds = time.perf_counter() - started
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        if not all(
            model.first_failed_constraint(*pair) is None
            for pair in search.representative_pairs
        ):
            raise RuntimeError(f"p={prime} enumeration emitted an invalid representative")
        known_recovered = intermediate in search.representative_pairs
        known_signatures = (
            intermediate_signature(intermediate[0]),
            intermediate_signature(intermediate[1]),
        )
        target = (6 * model.length - 4, *([-6] * model.half_shifts))
        if tuple(
            left + right for left, right in zip(*known_signatures, strict=True)
        ) != target:
            raise RuntimeError(f"p={prime} known signatures are not complementary")

        opb = output_directory / f"p{prime}_intermediate.opb"
        opb_artifact = model.write_opb(opb)
        proof = output_directory / f"p{prime}_known_branch.pbp"
        write_veripb_sat_certificate(model, *intermediate, proof)
        verification = _verify(
            verifier,
            opb,
            proof,
            output_directory / f"p{prime}_known_branch_veripb.txt",
        )
        cases[f"p{prime}"] = {
            "prescribed_first": _row(prescribed[0]),
            "prescribed_second": _row(prescribed[1]),
            "known_intermediate_first": _row(intermediate[0]),
            "known_intermediate_second": _row(intermediate[1]),
            "known_signature_first": _row(known_signatures[0]),
            "known_signature_second": _row(known_signatures[1]),
            "known_branch_recovered_as_stored_representative": known_recovered,
            "search": {
                "first_candidates": search.first_candidates,
                "second_candidates": search.second_candidates,
                "first_signatures": search.first_signatures,
                "second_signatures": search.second_signatures,
                "signature_matches": search.signature_matches,
                "ordered_pairs": search.ordered_pairs,
                "stored_representatives": len(search.representative_pairs),
                "elapsed_seconds": round(enumeration_seconds, 6),
                "tracemalloc_peak_bytes": peak_bytes,
            },
            "model_stats": vars(model.stats),
            "opb": {
                "path": _recorded_path(opb_artifact.path),
                "bytes": opb_artifact.bytes,
                "sha256": opb_artifact.sha256,
            },
            "known_branch_certificate": _artifact(proof),
            "verification": verification,
        }

    metadata: dict[str, object] = {
        "status": (
            "exhaustive p=3/p=5 intermediate-stage enumeration and known-branch "
            "certificate verification; no LP(333) model and no order-668 result"
        ),
        "source_basis": "successive q-uncompression in kotsireas2025compression",
        "algorithm": (
            "enumerate all {-3,-1,1,3} residue triples and hash-join exact "
            "nonredundant PAF signatures"
        ),
        "cpu_cores_used": 1,
        "random_seed": None,
        "cases": cases,
        "verifier": _artifact(verifier),
        "verifier_version": "VeriPB 3.0.2",
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "command": (
            "python -m scripts.build_intermediate_stage --verifier "
            "tmp/tools/veripb-3.0.2/bin/veripb.exe"
        ),
    }
    (output_directory / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    metadata = build(args.verifier, args.output_directory.resolve())
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
