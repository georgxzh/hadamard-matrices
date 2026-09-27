"""Reproduce the published structured LP(45) and validate the p=5 OPB model.

This is a fixed-witness validation, not an open search.  It checks the exact
two-stage compression, both OPB variants, VeriPB SAT certificates, and the
resulting H(92) with two independent exact matrix verifiers.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import tracemalloc
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from src.legendre import (
    check_legendre_compression_constants,
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    legendre_pair_to_hadamard,
    published_structured_legendre_pair_45,
    structured_compressed_pair,
)
from src.pb_certificate import write_veripb_sat_certificate
from src.pb_model import OPBArtifact, UncompressionPBModel
from src.symmetry import canonical_residue_translation
from src.uncompress import uncompression_count
from src.verify_matrix import verify as verify_direct
from src.verify_matrix import write_report as write_direct_report
from src.verify_matrix_independent import verify as verify_independent
from src.verify_matrix_independent import write_report as write_independent_report


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "p5_validation"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _artifact(path: Path, *, tracked: bool = True) -> dict[str, object]:
    try:
        recorded_path = path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        recorded_path = str(path)
    return {
        "path": recorded_path,
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "tracked": tracked,
    }


def _opb_artifact(artifact: OPBArtifact) -> dict[str, object]:
    try:
        recorded_path = artifact.path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        recorded_path = str(artifact.path)
    return {
        "path": recorded_path,
        "bytes": artifact.bytes,
        "sha256": artifact.sha256,
        "tracked": True,
    }


def _signs(sequence: tuple[int, ...]) -> str:
    return "".join("+" if value == 1 else "-" for value in sequence)


def _write_csv(matrix: list[list[int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerows(matrix)


def _run_veripb(verifier: Path, opb: Path, proof: Path, output: Path) -> dict[str, object]:
    command = [str(verifier), "--stats", str(opb), str(proof)]
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        check=False,
        timeout=120,
    )
    elapsed = time.perf_counter() - started
    combined = completed.stdout + completed.stderr
    text = combined.decode("utf-8", errors="replace")
    output.write_text(text, encoding="utf-8", newline="\n")
    if completed.returncode != 0 or "s VERIFIED SATISFIABLE" not in text:
        raise RuntimeError(f"VeriPB rejected {proof.name}; exit={completed.returncode}")
    return {
        "command": command,
        "exit_code": completed.returncode,
        "elapsed_seconds": round(elapsed, 6),
        "reported_status": "VERIFIED SATISFIABLE",
        "stdout": _artifact(output),
    }


def validate(verifier: Path, output_directory: Path = DEFAULT_OUTPUT) -> dict[str, object]:
    """Run the deterministic p=5 fixed-witness validation."""

    verifier = verifier.resolve()
    if not verifier.is_file():
        raise FileNotFoundError("--verifier must name a VeriPB executable")
    output_directory.mkdir(parents=True, exist_ok=True)
    tracemalloc.start()
    started_utc = datetime.now(timezone.utc)
    started = time.perf_counter()

    first, second = published_structured_legendre_pair_45()
    prescribed_first, prescribed_second = structured_compressed_pair(5, 3)
    intermediate_first = compress(first, 15)
    intermediate_second = compress(second, 15)
    if not check_legendre_pair(first, second).ok:
        raise RuntimeError("published LP(45) failed the exact PAF check")
    if not check_negative_support_sds(first, second).ok:
        raise RuntimeError("published LP(45) failed the exact SDS check")
    if not check_legendre_psd_constraints(first, second):
        raise RuntimeError("published LP(45) failed the exact cyclotomic PSD check")
    if not check_legendre_compression_constants(first, second, 5):
        raise RuntimeError("published LP(45) failed the direct 9-compression check")
    if not check_legendre_compression_constants(first, second, 15):
        raise RuntimeError("published LP(45) failed the first staged 3-compression check")
    if compress(intermediate_first, 5) != prescribed_first:
        raise RuntimeError("first staged row does not 3-compress to the prescribed row")
    if compress(intermediate_second, 5) != prescribed_second:
        raise RuntimeError("second staged row does not 3-compress to the prescribed row")

    model = UncompressionPBModel(prescribed_first, prescribed_second, 9)
    canonical_model = UncompressionPBModel(
        prescribed_first,
        prescribed_second,
        9,
        canonical_translations=True,
    )
    canonical_first, first_offset = canonical_residue_translation(first, 5)
    canonical_second, second_offset = canonical_residue_translation(second, 5)
    if model.first_failed_constraint(first, second) is not None:
        raise RuntimeError("published LP(45) failed the unbroken OPB model")
    if canonical_model.first_failed_constraint(canonical_first, canonical_second) is not None:
        raise RuntimeError("normalized LP(45) failed the translation-canonical OPB model")

    opb = model.write_opb(output_directory / "lp45_structured.opb")
    canonical_opb = canonical_model.write_opb(
        output_directory / "lp45_structured_translation_canonical.opb"
    )
    certificate = output_directory / "lp45_known_witness.pbp"
    canonical_certificate = output_directory / "lp45_translation_canonical_known_witness.pbp"
    write_veripb_sat_certificate(model, first, second, certificate)
    write_veripb_sat_certificate(
        canonical_model,
        canonical_first,
        canonical_second,
        canonical_certificate,
    )
    verifier_checks = {
        "unbroken": _run_veripb(
            verifier,
            opb.path,
            certificate,
            output_directory / "lp45_known_witness_veripb.txt",
        ),
        "translation_canonical": _run_veripb(
            verifier,
            canonical_opb.path,
            canonical_certificate,
            output_directory / "lp45_translation_canonical_known_witness_veripb.txt",
        ),
    }

    matrix = legendre_pair_to_hadamard(first, second)
    candidate = output_directory / "H92.csv"
    _write_csv(matrix, candidate)
    direct = verify_direct(candidate, order=92)
    independent = verify_independent(candidate, order=92)
    direct_report = output_directory / "H92_verification.txt"
    independent_report = output_directory / "H92_verification_independent.txt"
    direct_report_hash = write_direct_report(direct, direct_report)
    independent_report_hash = write_independent_report(independent, independent_report)
    if not direct.ok or not independent.ok:
        raise RuntimeError("H(92) failed an independent exact verifier")

    witness = {
        "source": "Kotsireas--Gomez--Gomez-Perez (2025), section 5.3.2",
        "source_doi": "10.1145/3747199.3747549",
        "indexing": "displayed order stored at zero-based positions 0..44",
        "first": _signs(first),
        "second": _signs(second),
        "intermediate_3_compression_first": list(intermediate_first),
        "intermediate_3_compression_second": list(intermediate_second),
        "prescribed_9_compression_first": list(prescribed_first),
        "prescribed_9_compression_second": list(prescribed_second),
        "canonical_first": _signs(canonical_first),
        "canonical_second": _signs(canonical_second),
        "canonical_offsets": [first_offset, second_offset],
    }
    witness_path = output_directory / "lp45_witness.json"
    witness_path.write_text(
        json.dumps(witness, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    metadata: dict[str, object] = {
        "status": (
            "published LP(45) fixed-witness reproduction and p=5 model validation; "
            "not an open search and not an order-668 result"
        ),
        "source": {
            "bibtex_key": "kotsireas2025compression",
            "doi": "10.1145/3747199.3747549",
            "location": "section 5.3.2, LP(3^2 * 5)",
            "accessed": "2026-09-27",
            "access": "publisher HTML; direct PDF unavailable",
        },
        "deterministic": True,
        "random_seed": None,
        "parameters": {"p": 5, "q": 3, "factor": 9, "length": 45},
        "uncompression_candidates_one_row": str(
            uncompression_count(prescribed_first, 9)
        ),
        "search_run": False,
        "exact_checks": {
            "legendre_paf": True,
            "negative_support_sds": True,
            "cyclotomic_psd": True,
            "direct_9_compression": True,
            "successive_3_compressions": True,
            "all_unbroken_opb_records": True,
            "all_translation_canonical_opb_records": True,
        },
        "staged_compression": {
            "length_45_to_15_factor": 3,
            "length_15_to_5_factor": 3,
            "intermediate_first": list(intermediate_first),
            "intermediate_second": list(intermediate_second),
        },
        "models": {
            "unbroken": {
                "stats": asdict(model.stats),
                "opb": _opb_artifact(opb),
                "certificate": _artifact(certificate),
                "veripb": verifier_checks["unbroken"],
            },
            "translation_canonical": {
                "stats": asdict(canonical_model.stats),
                "opb": _opb_artifact(canonical_opb),
                "certificate": _artifact(canonical_certificate),
                "veripb": verifier_checks["translation_canonical"],
                "normalizing_offsets": [first_offset, second_offset],
                "free_ordered_pair_reduction_factor": 81,
            },
        },
        "hadamard": {
            "order": 92,
            "candidate": _artifact(candidate),
            "direct_verifier": True,
            "independent_bitpacked_verifier": True,
            "direct_report_sha256": direct_report_hash,
            "independent_report_sha256": independent_report_hash,
        },
        "witness": _artifact(witness_path),
        "verifier": _artifact(verifier, tracked=False),
        "verifier_version": "VeriPB 3.0.2",
        "started_utc": started_utc.isoformat(),
        "elapsed_seconds_this_run": round(time.perf_counter() - started, 6),
        "python_peak_tracemalloc_bytes": peak_bytes,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "logical_cpu_count": os.cpu_count(),
        "cpu_cores_used": 1,
        "command": (
            "python -m scripts.validate_p5_uncompression --verifier "
            "tmp/tools/veripb-3.0.2/bin/veripb.exe"
        ),
    }
    metadata_path = output_directory / "metadata.json"
    metadata_path.write_text(
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
    metadata = validate(args.verifier, args.output_directory.resolve())
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
