"""Freeze the complete v0.6 SLC C1 executable before acceptance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CANDIDATE = Path(__file__).resolve().parents[1]
HASHES_PATH = CANDIDATE / "V0_6_SLC_C1_EXECUTABLE_HASHES.json"
SEAL_PATH = CANDIDATE / "V0_6_SLC_C1_EXECUTABLE_SEAL.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def aggregate(entries: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, file_hash in sorted(entries.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def executable_snapshot() -> dict[str, str]:
    files: list[Path] = []
    for name in ("src", "tests", "tools", "registry", "examples"):
        base = CANDIDATE / name
        files.extend(path for path in base.rglob("*") if path.is_file())
    for name in (
        "pyproject.toml",
        "README.md",
        "CHANGELOG.md",
        "V0_6_SLC_C1_CONTRACT.json",
        "V0_6_SLC_C1_PRECOMMIT.md",
        "V0_6_SLC_C1_PRECOMMIT_SEAL.json",
        "V0_6_SLC_C1_SOURCE_MANIFEST.json",
        "V0_5_PARENT_BASELINE.json",
        "build_v06_slc_c1_precommit.py",
    ):
        files.append(CANDIDATE / name)
    return {
        path.relative_to(CANDIDATE).as_posix(): sha256(path)
        for path in sorted(set(files))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
        and ".egg-info" not in path.as_posix()
    }


def main() -> int:
    immutable_markers = (
        HASHES_PATH,
        SEAL_PATH,
        CANDIDATE / "V0_6_SLC_C1_ACCEPTANCE_RESULT.json",
        CANDIDATE / "V0_6_SLC_C1_ACCEPTANCE_FAILURE.json",
        CANDIDATE / "V0_6_SLC_C1_RELEASE_MANIFEST.json",
    )
    existing = [path.name for path in immutable_markers if path.exists()]
    if existing:
        raise RuntimeError(
            "executable seal is single-use and cannot overwrite existing markers: "
            + ", ".join(existing)
        )
    files = executable_snapshot()
    candidate_hash = aggregate(files)
    payload = {
        "algorithm": "sha256(relative_posix_path + NUL + file_sha256 + LF)",
        "campaign_id": "SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE",
        "candidate_code_hash": candidate_hash,
        "file_count": len(files),
        "files": files,
        "runner_sha256": files["tools/run_v06_slc_c1_acceptance.py"],
        "precommit_seal_sha256": files["V0_6_SLC_C1_PRECOMMIT_SEAL.json"],
    }
    HASHES_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    SEAL_PATH.write_text(candidate_hash + "\n", encoding="utf-8")
    print(json.dumps({"candidate_code_hash": candidate_hash, "file_count": len(files)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
