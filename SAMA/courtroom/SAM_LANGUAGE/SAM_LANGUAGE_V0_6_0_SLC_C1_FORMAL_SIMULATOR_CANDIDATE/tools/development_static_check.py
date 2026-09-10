"""Static pre-seal check for the v0.6 executable and one-shot runner."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


CANDIDATE = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    python_files = sorted(
        path
        for path in CANDIDATE.rglob("*.py")
        if "__pycache__" not in path.parts and ".egg-info" not in path.as_posix()
    )
    compile_failures: list[dict[str, str]] = []
    for path in python_files:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except Exception as exc:
            compile_failures.append(
                {
                    "path": path.relative_to(CANDIDATE).as_posix(),
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            )

    runner = load_module(
        "v06_acceptance_static",
        CANDIDATE / "tools/run_v06_slc_c1_acceptance.py",
    )
    sealer = load_module(
        "v06_sealer_static",
        CANDIDATE / "tools/seal_v06_slc_c1_executable.py",
    )
    runner_snapshot = runner.candidate_code_snapshot()
    sealer_snapshot = sealer.executable_snapshot()
    required = {
        "V0_5_PARENT_BASELINE.json",
        "build_v06_slc_c1_precommit.py",
        "tools/run_v06_slc_c1_acceptance.py",
        "tools/clean_wheel_probe.py",
    }
    immutable_markers = (
        "V0_6_SLC_C1_EXECUTABLE_HASHES.json",
        "V0_6_SLC_C1_EXECUTABLE_SEAL.txt",
        "V0_6_SLC_C1_ACCEPTANCE_RESULT.json",
        "V0_6_SLC_C1_ACCEPTANCE_FAILURE.json",
        "V0_6_SLC_C1_RELEASE_MANIFEST.json",
    )
    checks = {
        "all_python_compiles": not compile_failures,
        "snapshot_algorithms_match": runner_snapshot == sealer_snapshot,
        "required_custody_files_present": required.issubset(runner_snapshot),
        "predecessor_census_available": "native_decomposition_census"
        in json.loads(
            (
                CANDIDATE.parent
                / "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/SLCX003_CONTRACT.json"
            ).read_text(encoding="utf-8")
        ),
        "one_shot_markers_absent": not any(
            (CANDIDATE / name).exists() for name in immutable_markers
        ),
    }
    payload = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "python_files": len(python_files),
        "snapshot_files": len(runner_snapshot),
        "compile_failures": compile_failures,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
