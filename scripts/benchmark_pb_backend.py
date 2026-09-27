"""Benchmark the LP(27) RoundingSat/VeriPB certificate pipeline.

This script never runs LP(333).  It checks deterministic SAT certificates for
the known LP(27) witness, exercises solver-generated proof logging on an exact
fixed-witness copy, and performs short bounded open-search probes on both the
unbroken and translation-canonical models.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import platform
import re
import subprocess
import time
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from src.legendre import check_legendre_pair, compress, structured_compressed_pair
from src.pb_certificate import write_fixed_assignment_opb, write_veripb_sat_certificate
from src.pb_model import UncompressionPBModel
from src.symmetry import canonical_residue_translation


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "pb_backend_benchmark"
DEFAULT_SCRATCH = REPOSITORY_ROOT / "tmp" / "pb_backend_benchmark"


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
    started = perf_started = time.perf_counter()
    timed_out = False
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
            if time.perf_counter() - perf_started > timeout:
                timed_out = True
                process.kill()
                break
            time.sleep(0.01)
        process.wait()
        sample = _peak_working_set(process)
        if sample is not None:
            peak = max(peak, sample)
    text = output.read_text(encoding="utf-8", errors="replace")
    output.write_text(text, encoding="utf-8", newline="\n")
    status_match = re.search(r"(?m)^s ([A-Z]+)$", text)
    return {
        "command": [str(part) for part in command],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "exit_code": process.returncode,
        "externally_timed_out": timed_out,
        "reported_status": status_match.group(1) if status_match else None,
        "peak_working_set_bytes": peak or None,
        "stdout": {
            "path": output.relative_to(REPOSITORY_ROOT).as_posix(),
            "bytes": output.stat().st_size,
            "sha256": _sha256(output),
        },
    }


def _signs(value: str) -> tuple[int, ...]:
    if not value or any(character not in "+-" for character in value):
        raise ValueError("witness strings must contain only + and -")
    return tuple(1 if character == "+" else -1 for character in value)


def _artifact(path: Path, *, tracked: bool) -> dict[str, object]:
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


def _normalize_proof(path: Path) -> None:
    """Canonicalize solver text without changing proof commands."""

    lines = path.read_text(encoding="ascii").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="ascii",
        newline="\n",
    )


def benchmark(
    solver: Path,
    verifier: Path,
    output_directory: Path = DEFAULT_OUTPUT,
    scratch_directory: Path = DEFAULT_SCRATCH,
    probe_seconds: int = 10,
) -> dict[str, object]:
    """Run bounded LP(27) certificate and search-pipeline benchmarks."""

    if probe_seconds <= 0:
        raise ValueError("probe_seconds must be positive")
    solver = solver.resolve()
    verifier = verifier.resolve()
    if not solver.is_file() or not verifier.is_file():
        raise FileNotFoundError("solver and verifier paths must name executable files")
    output_directory.mkdir(parents=True, exist_ok=True)
    scratch_directory.mkdir(parents=True, exist_ok=True)

    witness_record = json.loads(
        (REPOSITORY_ROOT / "results" / "pb_uncompression" / "lp27_witness.json").read_text(
            encoding="utf-8"
        )
    )
    first = _signs(witness_record["first"])
    second = _signs(witness_record["second"])
    compressed_first, compressed_second = structured_compressed_pair(3, 3)
    if not check_legendre_pair(first, second).ok:
        raise RuntimeError("tracked LP(27) witness failed the independent Legendre checker")
    if compress(first, 3) != compressed_first or compress(second, 3) != compressed_second:
        raise RuntimeError("tracked LP(27) witness has the wrong prescribed compression")

    cases = {
        "unbroken": (
            UncompressionPBModel(compressed_first, compressed_second, 9),
            first,
            second,
            REPOSITORY_ROOT / "results" / "pb_uncompression" / "lp27_structured.opb",
        ),
        "translation_canonical": (
            UncompressionPBModel(
                compressed_first,
                compressed_second,
                9,
                canonical_translations=True,
            ),
            canonical_residue_translation(first, 3)[0],
            canonical_residue_translation(second, 3)[0],
            REPOSITORY_ROOT
            / "results"
            / "pb_uncompression"
            / "lp27_structured_translation_canonical.opb",
        ),
    }

    results: dict[str, object] = {}
    for name, (model, row_first, row_second, opb) in cases.items():
        certificate = output_directory / f"{name}_known_witness.pbp"
        write_veripb_sat_certificate(model, row_first, row_second, certificate)
        direct_check = _run(
            [str(verifier), "--stats", str(opb), str(certificate)],
            output_directory / f"{name}_known_witness_veripb.txt",
            timeout=120,
        )
        if direct_check["exit_code"] != 0:
            raise RuntimeError(f"VeriPB rejected the deterministic {name} SAT certificate")

        assignment = model.assignment_for_pair(row_first, row_second)
        fixed_opb = scratch_directory / f"{name}_fixed.opb"
        fixed_proof = output_directory / f"{name}_roundingsat_fixed.pbp"
        write_fixed_assignment_opb(opb, assignment, fixed_opb)
        fixed_run = _run(
            [
                str(solver),
                "--print-sol=1",
                "--verbosity=1",
                "--lp=0",
                f"--proof-log={fixed_proof}",
                "--time-limit=120",
                str(fixed_opb),
            ],
            output_directory / f"{name}_roundingsat_fixed.txt",
            timeout=150,
        )
        if fixed_run["reported_status"] != "SATISFIABLE" or not fixed_proof.is_file():
            raise RuntimeError(f"RoundingSat failed the fixed-witness {name} pipeline")
        _normalize_proof(fixed_proof)
        fixed_check = _run(
            [str(verifier), "--stats", str(fixed_opb), str(fixed_proof)],
            output_directory / f"{name}_roundingsat_fixed_veripb.txt",
            timeout=120,
        )
        if fixed_check["exit_code"] != 0:
            raise RuntimeError(f"VeriPB rejected RoundingSat's fixed-witness {name} proof")

        probe_proof = scratch_directory / f"{name}_open_probe.pbp"
        probe = _run(
            [
                str(solver),
                "--print-sol=1",
                "--verbosity=1",
                "--lp=0",
                f"--proof-log={probe_proof}",
                f"--time-limit={probe_seconds}",
                str(opb),
            ],
            output_directory / f"{name}_open_probe.txt",
            timeout=probe_seconds + 30,
        )
        results[name] = {
            "opb": _artifact(opb, tracked=True),
            "known_witness_exact_checks": {
                "legendre_pair": True,
                "prescribed_compression": True,
                "all_opb_records": True,
            },
            "known_witness_certificate": _artifact(certificate, tracked=True),
            "known_witness_veripb": direct_check,
            "fixed_witness_roundingsat": fixed_run,
            "fixed_witness_proof": _artifact(fixed_proof, tracked=True),
            "fixed_witness_veripb": fixed_check,
            "open_search_probe": probe,
            "open_search_probe_proof": _artifact(probe_proof, tracked=False),
        }

    metadata: dict[str, object] = {
        "status": (
            "LP(27) certificate-pipeline benchmark only; bounded open probes are "
            "not evidence about LP(333) or order 668"
        ),
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "probe_seconds_each": probe_seconds,
        "cpu_cores_used_per_process": 1,
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported by platform.processor()",
        "solver": _artifact(solver, tracked=False),
        "verifier": _artifact(verifier, tracked=False),
        "verifier_version": "VeriPB 3.0.2",
        "roundingsat_reported_commit": "d4edbf7",
        "cases": results,
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
    parser.add_argument("--probe-seconds", type=int, default=10)
    args = parser.parse_args()
    metadata = benchmark(
        args.solver,
        args.verifier,
        args.output_directory.resolve(),
        args.scratch_directory.resolve(),
        args.probe_seconds,
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
