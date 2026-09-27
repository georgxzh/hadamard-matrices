"""Validate and benchmark fixed intermediate branches at p=3 and p=5.

Each branch fixes the first 3-compression (length ``9p`` to ``3p``), while
leaving every final binary variable free.  The script emits exact OPB models,
checks known-witness certificates, and performs bounded proof-logging searches.
It never constructs or solves an LP(333) model.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import platform
import re
import shutil
import subprocess
import time
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence

from src.legendre import (
    check_legendre_pair,
    check_legendre_psd_constraints,
    check_negative_support_sds,
    compress,
    decode_signs,
    published_structured_legendre_pair_45,
    structured_compressed_pair,
)
from src.pb_certificate import write_veripb_sat_certificate
from src.pb_model import UncompressionPBModel
from src.staged_uncompression import FactorThreeBranch
from src.symmetry import canonical_residue_translation
from src.uncompress import uncompression_count


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "staged_uncompression"
DEFAULT_SCRATCH = REPOSITORY_ROOT / "tmp" / "staged_uncompression"


class _ProcessMemoryCounters(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
    ]


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


def _artifact(path: Path, *, tracked: bool) -> dict[str, object]:
    return {
        "path": _recorded_path(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "tracked": tracked,
    }


def _peak_working_set(process: subprocess.Popen[bytes]) -> int | None:
    if platform.system() != "Windows" or not hasattr(process, "_handle"):
        return None
    counters = _ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    success = psapi.GetProcessMemoryInfo(
        wintypes.HANDLE(process._handle),  # type: ignore[attr-defined]
        ctypes.byref(counters),
        counters.cb,
    )
    return int(counters.PeakWorkingSetSize) if success else None


def _run(command: Sequence[str], output: Path, *, timeout: float) -> dict[str, object]:
    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    externally_timed_out = False
    peak = 0
    with output.open("wb") as stream:
        process = subprocess.Popen(
            list(command),
            cwd=REPOSITORY_ROOT,
            stdout=stream,
            stderr=subprocess.STDOUT,
        )
        while process.poll() is None:
            sample = _peak_working_set(process)
            if sample is not None:
                peak = max(peak, sample)
            if time.perf_counter() - started > timeout:
                externally_timed_out = True
                process.kill()
                break
            time.sleep(0.01)
        process.wait()
    text = output.read_text(encoding="utf-8", errors="replace")
    output.write_text(text, encoding="utf-8", newline="\n")
    status_match = re.search(r"(?m)^s ([A-Z]+)$", text)
    return {
        "command": [str(part) for part in command],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "exit_code": process.returncode,
        "externally_timed_out": externally_timed_out,
        "reported_status": status_match.group(1) if status_match else None,
        "peak_working_set_bytes": peak or None,
        "stdout": _artifact(output, tracked=True),
    }


def _normalize_proof(path: Path) -> None:
    lines = path.read_text(encoding="ascii").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="ascii",
        newline="\n",
    )


def _assignment_from_solver_output(text: str, variables: int) -> dict[int, int]:
    assignment: dict[int, int] = {}
    for line in text.splitlines():
        if not line.startswith("v "):
            continue
        for literal in line.split()[1:]:
            match = re.fullmatch(r"(-?)x(\d+)", literal)
            if match is None:
                raise ValueError(f"invalid solver assignment literal: {literal}")
            variable = int(match.group(2))
            assignment[variable] = int(not match.group(1))
    expected = set(range(1, variables + 1))
    if set(assignment) != expected:
        raise ValueError("solver did not emit a complete assignment")
    return assignment


def _rows_from_assignment(
    model: UncompressionPBModel, assignment: Mapping[int, int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    rows = []
    for row in (0, 1):
        start = row * model.length + 1
        rows.append(
            tuple(-1 if assignment[start + index] else 1 for index in range(model.length))
        )
    return rows[0], rows[1]


def _signs(sequence: Sequence[int]) -> str:
    return "".join("+" if value == 1 else "-" for value in sequence)


def _known_pair(prime: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if prime == 5:
        return published_structured_legendre_pair_45()
    if prime != 3:
        raise ValueError("this bounded benchmark supports only p=3 and p=5")
    record = json.loads(
        (REPOSITORY_ROOT / "results" / "pb_uncompression" / "lp27_witness.json").read_text(
            encoding="utf-8"
        )
    )
    return decode_signs(record["first"]), decode_signs(record["second"])


def _verify_certificate(
    verifier: Path,
    opb: Path,
    proof: Path,
    output: Path,
) -> dict[str, object]:
    check = _run(
        [str(verifier), "--stats", str(opb), str(proof)],
        output,
        timeout=120,
    )
    text = output.read_text(encoding="utf-8")
    if check["exit_code"] != 0 or "s VERIFIED SATISFIABLE" not in text:
        raise RuntimeError(f"VeriPB rejected {proof.name}")
    return check


def benchmark(
    solver: Path,
    verifier: Path,
    output_directory: Path = DEFAULT_OUTPUT,
    scratch_directory: Path = DEFAULT_SCRATCH,
    search_seconds: int = 10,
) -> dict[str, object]:
    """Validate known branches and run bounded final-binary searches."""

    if not 0 < search_seconds < 30:
        raise ValueError("search_seconds must be between 1 and 29")
    solver = solver.resolve()
    verifier = verifier.resolve()
    if not solver.is_file() or not verifier.is_file():
        raise FileNotFoundError("solver and verifier must name executable files")
    output_directory.mkdir(parents=True, exist_ok=True)
    scratch_directory.mkdir(parents=True, exist_ok=True)

    results: dict[str, object] = {}
    for prime in (3, 5):
        first, second = _known_pair(prime)
        prescribed = structured_compressed_pair(prime, 3)
        intermediate = (compress(first, 3 * prime), compress(second, 3 * prime))
        branch = FactorThreeBranch(*prescribed, *intermediate)
        residues = branch.canonical_residues
        case_results: dict[str, object] = {
            "intermediate_first": list(intermediate[0]),
            "intermediate_second": list(intermediate[1]),
            "canonical_residues": list(residues),
            "row_preimage_counts": [
                str(uncompression_count(intermediate[0], 3)),
                str(uncompression_count(intermediate[1], 3)),
            ],
        }
        for canonical in (False, True):
            label = "canonical" if canonical else "unbroken"
            model = branch.model(canonical_translations=canonical)
            if canonical:
                row_first, first_offset = canonical_residue_translation(
                    first, 3 * prime, residues[0]
                )
                row_second, second_offset = canonical_residue_translation(
                    second, 3 * prime, residues[1]
                )
                offsets = [first_offset, second_offset]
            else:
                row_first, row_second = first, second
                offsets = [0, 0]
            if model.first_failed_constraint(row_first, row_second) is not None:
                raise RuntimeError(f"known p={prime} witness failed the {label} model")

            prefix = f"p{prime}_{label}"
            opb = output_directory / f"{prefix}.opb"
            opb_artifact = model.write_opb(opb)
            known_proof = output_directory / f"{prefix}_known_witness.pbp"
            write_veripb_sat_certificate(model, row_first, row_second, known_proof)
            known_check = _verify_certificate(
                verifier,
                opb,
                known_proof,
                output_directory / f"{prefix}_known_witness_veripb.txt",
            )

            scratch_proof = scratch_directory / f"{prefix}_search.pbp"
            search_stdout = output_directory / f"{prefix}_search.txt"
            search = _run(
                [
                    str(solver),
                    "--print-sol=1",
                    "--verbosity=1",
                    "--lp=0",
                    f"--proof-log={scratch_proof}",
                    f"--time-limit={search_seconds}",
                    str(opb),
                ],
                search_stdout,
                timeout=search_seconds + 20,
            )
            search_result: dict[str, object] = {"run": search}
            if search["reported_status"] == "SATISFIABLE":
                assignment = _assignment_from_solver_output(
                    search_stdout.read_text(encoding="utf-8"), model.stats.variables
                )
                solved_first, solved_second = _rows_from_assignment(model, assignment)
                if model.first_failed_constraint(solved_first, solved_second) is not None:
                    raise RuntimeError(f"solver p={prime} {label} rows fail their OPB model")
                if not check_legendre_pair(solved_first, solved_second).ok:
                    raise RuntimeError(f"solver p={prime} {label} rows fail exact PAF")
                if not check_negative_support_sds(solved_first, solved_second).ok:
                    raise RuntimeError(f"solver p={prime} {label} rows fail exact SDS")
                if not check_legendre_psd_constraints(solved_first, solved_second):
                    raise RuntimeError(f"solver p={prime} {label} rows fail exact PSD")
                if compress(solved_first, 3 * prime) != intermediate[0] or compress(
                    solved_second, 3 * prime
                ) != intermediate[1]:
                    raise RuntimeError(f"solver p={prime} {label} rows have wrong branch")
                _normalize_proof(scratch_proof)
                tracked_proof = output_directory / f"{prefix}_search.pbp"
                shutil.copyfile(scratch_proof, tracked_proof)
                proof_check = _verify_certificate(
                    verifier,
                    opb,
                    tracked_proof,
                    output_directory / f"{prefix}_search_veripb.txt",
                )
                witness_path = output_directory / f"{prefix}_solver_witness.json"
                witness_path.write_text(
                    json.dumps(
                        {
                            "first": _signs(solved_first),
                            "second": _signs(solved_second),
                            "legendre_paf": True,
                            "negative_support_sds": True,
                            "cyclotomic_psd": True,
                            "intermediate_first": list(intermediate[0]),
                            "intermediate_second": list(intermediate[1]),
                        },
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
                search_result.update(
                    {
                        "exact_independent_checks": True,
                        "proof": _artifact(tracked_proof, tracked=True),
                        "proof_verification": proof_check,
                        "witness": _artifact(witness_path, tracked=True),
                    }
                )
            else:
                search_result["incomplete_proof"] = _artifact(
                    scratch_proof, tracked=False
                )

            case_results[label] = {
                "stats": vars(model.stats),
                "opb": {
                    "path": _recorded_path(opb_artifact.path),
                    "bytes": opb_artifact.bytes,
                    "sha256": opb_artifact.sha256,
                    "tracked": True,
                },
                "known_witness_offsets": offsets,
                "known_witness_certificate": _artifact(known_proof, tracked=True),
                "known_witness_verification": known_check,
                "bounded_search": search_result,
            }
        results[f"p{prime}"] = case_results

    metadata: dict[str, object] = {
        "status": (
            "fixed intermediate-branch validation and bounded p=3/p=5 searches; "
            "no LP(333) model or order-668 result"
        ),
        "architecture": (
            "length 9p binary rows -> factor-3 intermediate rows of length 3p "
            "-> prescribed factor-3 rows of length p"
        ),
        "source_basis": "successive q-uncompression in kotsireas2025compression",
        "search_seconds_each": search_seconds,
        "cpu_cores_used_per_process": 1,
        "random_seed": None,
        "solver": _artifact(solver, tracked=False),
        "roundingsat_reported_commit": "d4edbf7",
        "verifier": _artifact(verifier, tracked=False),
        "verifier_version": "VeriPB 3.0.2",
        "cases": results,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "command": (
            "python -m scripts.benchmark_staged_uncompression --solver "
            "tmp/tools/roundingsat/roundingsat.exe --verifier "
            "tmp/tools/veripb-3.0.2/bin/veripb.exe --search-seconds 10"
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
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scratch-directory", type=Path, default=DEFAULT_SCRATCH)
    parser.add_argument("--search-seconds", type=int, default=10)
    args = parser.parse_args()
    metadata = benchmark(
        args.solver,
        args.verifier,
        args.output_directory.resolve(),
        args.scratch_directory.resolve(),
        args.search_seconds,
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
