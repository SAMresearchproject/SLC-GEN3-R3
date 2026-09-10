"""Seal the v0.5 + SLCX002/SLCX003 sources for the SAM Language v0.6 C1 build.

This builder is intentionally precommit-only. It verifies and records immutable
inputs, then emits the source manifest, human-readable precommit, and seal. It
does not scaffold implementation files, execute acceptance tests, or mutate any
predecessor.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
CAMPAIGN_ID = "SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE"
PREFLIGHT_STEM = "PREFLIGHT_20260718_173728_no_script"
CONTRACT_PATH = OUT / "V0_6_SLC_C1_CONTRACT.json"
BUILDER_PATH = Path(__file__).resolve()

PARENT = ROOT / "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE"
PARENT_HASHES = PARENT / "V0_5_EXECUTABLE_HASHES.json"
PARENT_SEAL = PARENT / "V0_5_EXECUTABLE_SEAL.txt"

SLCX002 = ROOT / "18_SAM_NATIVE_QC" / "SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY"
SLCX003 = ROOT / "18_SAM_NATIVE_QC" / "SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY"

ANCHOR_SOURCES = [
    f"artifacts/preflight_filled/{PREFLIGHT_STEM}.md",
    f"artifacts/preflight_filled/{PREFLIGHT_STEM}.json",
    "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE/V0_5_EXECUTABLE_HASHES.json",
    "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE/V0_5_EXECUTABLE_SEAL.txt",
    "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE/V0_5_RELEASE_MANIFEST.json",
    "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE/V0_5_RELEASE_READINESS.md",
    "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE/V0_5_REGRESSION_SUMMARY.json",
    "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE/HASHES.txt",
    "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY/SLCX002_SOURCE_MANIFEST.json",
    "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY/SLCX002_CONTRACT.json",
    "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY/SLCX002_PRECOMMIT.md",
    "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY/SLCX002_PRECOMMIT_SEAL.json",
    "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY/release/SLCX002_RELEASE_MANIFEST.csv",
    "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY/release/SLCX002_RELEASE_MANIFEST_SHA256.txt",
    "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/SLCX003_SOURCE_MANIFEST.json",
    "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/SLCX003_CONTRACT.json",
    "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/SLCX003_PRECOMMIT.md",
    "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/SLCX003_PRECOMMIT_SEAL.json",
    "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/release/SLCX003_RELEASE_MANIFEST.csv",
    "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY/release/SLCX003_RELEASE_MANIFEST_SHA256.txt",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def aggregate(entries: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, file_hash in sorted(entries.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def source_row(path: Path, authority: str, expected: str | None = None) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    observed = sha256(path)
    if expected is not None and observed != expected:
        raise RuntimeError(
            f"Source custody mismatch for {relative(path)}: expected {expected}, observed {observed}"
        )
    return {
        "authority": authority,
        "bytes": path.stat().st_size,
        "path": relative(path),
        "sha256": observed,
    }


def add_row(rows: dict[str, dict[str, Any]], row: dict[str, Any]) -> None:
    prior = rows.get(row["path"])
    if prior is not None and prior["sha256"] != row["sha256"]:
        raise RuntimeError(f"Conflicting custody rows for {row['path']}")
    if prior is None:
        rows[row["path"]] = row


def load_contract() -> dict[str, Any]:
    payload = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if payload.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("Contract campaign_id mismatch")
    return payload


def verify_parent(contract: dict[str, Any], rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    declaration = contract["lineage"]["sam_language_v0_5"]
    payload = json.loads(PARENT_HASHES.read_text(encoding="utf-8"))
    expected_code_hash = declaration["expected_executable_hash"]
    if payload.get("candidate_code_hash") != expected_code_hash:
        raise RuntimeError("v0.5 executable-hash record disagrees with the frozen contract")
    if PARENT_SEAL.read_text(encoding="utf-8").strip() != expected_code_hash:
        raise RuntimeError("v0.5 executable seal disagrees with the frozen contract")
    files = payload.get("files", {})
    if len(files) != declaration["expected_executable_file_count"]:
        raise RuntimeError("v0.5 executable file-count mismatch")
    if aggregate(files) != expected_code_hash:
        raise RuntimeError("v0.5 aggregate executable hash does not reconstruct")
    for rel, expected in sorted(files.items()):
        add_row(rows, source_row(PARENT / rel, "IMMUTABLE_SAM_LANGUAGE_V0_5_PARENT", expected))

    release = json.loads((PARENT / "V0_5_RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
    if release.get("candidate_code_hash") != expected_code_hash:
        raise RuntimeError("v0.5 release manifest does not name the frozen parent hash")
    return {
        "candidate_code_hash": expected_code_hash,
        "executable_files_verified": len(files),
        "release_primary_verdict": release.get("primary_verdict"),
    }


def expected_manifest_hash(path: Path) -> str:
    fields = path.read_text(encoding="utf-8").strip().split()
    if not fields or len(fields[0]) != 64:
        raise RuntimeError(f"Malformed release-manifest hash record: {path}")
    return fields[0].lower()


def verify_release(
    campaign_dir: Path,
    prefix: str,
    expected_release_hash: str,
    authority: str,
    rows: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    release = campaign_dir / "release"
    manifest = release / f"{prefix}_RELEASE_MANIFEST.csv"
    hash_record = release / f"{prefix}_RELEASE_MANIFEST_SHA256.txt"
    declared = expected_manifest_hash(hash_record)
    observed = sha256(manifest)
    if declared != expected_release_hash or observed != expected_release_hash:
        raise RuntimeError(
            f"{prefix} release manifest mismatch: contract={expected_release_hash}, "
            f"declared={declared}, observed={observed}"
        )

    verified = 0
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        for item in csv.DictReader(handle):
            artifact = release / item["file"]
            row = source_row(artifact, authority, item["sha256"].lower())
            if int(item["bytes"]) != row["bytes"]:
                raise RuntimeError(f"Byte-count custody mismatch for {relative(artifact)}")
            add_row(rows, row)
            verified += 1
    return {
        "artifacts_verified": verified,
        "release_manifest_sha256": observed,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    contract = load_contract()
    rows: dict[str, dict[str, Any]] = {}

    parent = verify_parent(contract, rows)
    slcx002 = verify_release(
        SLCX002,
        "SLCX002",
        contract["lineage"]["slcx002"]["expected_release_manifest_sha256"],
        "FROZEN_SLCX002_REAL_TWO_OPERATION_SOURCE",
        rows,
    )
    slcx003 = verify_release(
        SLCX003,
        "SLCX003",
        contract["lineage"]["slcx003"]["expected_release_manifest_sha256"],
        "FROZEN_SLCX003_12_LEBIT_FORMAL_ORACLE",
        rows,
    )

    for rel in ANCHOR_SOURCES:
        add_row(rows, source_row(ROOT / rel, "LINEAGE_AND_PREFLIGHT_ANCHOR"))
    add_row(rows, source_row(CONTRACT_PATH, "FROZEN_V0_6_C1_CONTRACT"))
    add_row(rows, source_row(BUILDER_PATH, "PRECOMMIT_BUILDER"))

    ordered_rows = [rows[key] for key in sorted(rows)]
    manifest_payload = {
        "campaign_id": CAMPAIGN_ID,
        "deterministic_manifest": True,
        "lineage_verification": {
            "sam_language_v0_5": parent,
            "slcx002": slcx002,
            "slcx003": slcx003,
        },
        "preflight_stem": PREFLIGHT_STEM,
        "source_count": len(ordered_rows),
        "sources": ordered_rows,
    }
    manifest_path = OUT / "V0_6_SLC_C1_SOURCE_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    contract_hash = sha256(CONTRACT_PATH)
    builder_hash = sha256(BUILDER_PATH)
    manifest_hash = sha256(manifest_path)
    precommit_path = OUT / "V0_6_SLC_C1_PRECOMMIT.md"
    precommit_path.write_text(
        "# SAM Language v0.6 SLC C1 Formal Simulator Precommit\n\n"
        "Status: **SOURCE AND SEMANTIC CONTRACT SEALED BEFORE IMPLEMENTATION ACCEPTANCE**\n\n"
        "## Constructive target\n\n"
        "Build one exact 12-lebit SLC C1 state engine directly inside the successor "
        "SAM Language runtime. The v0.5 grammar remains the immutable parent. The "
        "SLCX002 real two-operation result and SLCX003 complete register lift are "
        "the executable-oracle sources; neither predecessor may be rewritten.\n\n"
        "## Frozen kernel\n\n"
        "The kernel stores sparse signed integer coefficients over a single exact "
        "power of sqrt(2), reduces them canonically, and proves normalization with "
        "integer arithmetic. SLC_L0 is address bit 0. B, PREPARE_REQUEST, and "
        "X1_RESPONSE have the exact meanings fixed in the contract. No sampling, "
        "physical edge graph, phase operator, or fitted cost enters the state engine.\n\n"
        "State identity and route history are deliberately separate. State hashes "
        "cover only the reduced exact vector. History hashes cover the ordered, "
        "tamper-evident transition receipts. Therefore star and chain histories may "
        "share a terminal state hash while retaining distinct history hashes.\n\n"
        "## Acceptance\n\n"
        "The sealed campaign requires parent preservation; a single language path; "
        "formal-profile isolation; all 132 ordered placements and 4096 basis inputs; "
        "1,081,344 classical schedule cases; 528 sign-gauge placements; 66 forest "
        "induction cases; 31,572 native decomposition assignments; 204 peel/restore "
        "cases; deterministic CLI/API parity; tamper detection; inherited regression; "
        "clean-wheel execution; and every frozen wrong control. No same-run repair is allowed.\n\n"
        "## Preserved frontier\n\n"
        "A pass promotes an exact real-sector SLC C1 simulator candidate. Complex "
        "phase semantics, measurement/publication, physical connectivity, coupling "
        "magnitude, and hardware realization remain separate work.\n\n"
        f"- v0.5 parent executable hash: `{parent['candidate_code_hash']}`\n"
        f"- SLCX002 release manifest hash: `{slcx002['release_manifest_sha256']}`\n"
        f"- SLCX003 release manifest hash: `{slcx003['release_manifest_sha256']}`\n"
        f"- Frozen source count: `{len(ordered_rows)}`\n"
        f"- Contract SHA-256: `{contract_hash}`\n"
        f"- Builder SHA-256: `{builder_hash}`\n"
        f"- Source manifest SHA-256: `{manifest_hash}`\n",
        encoding="utf-8",
    )

    seal = {
        "builder_sha256": builder_hash,
        "campaign_id": CAMPAIGN_ID,
        "contract_sha256": contract_hash,
        "precommit_sha256": sha256(precommit_path),
        "sam_language_v0_5_executable_hash": parent["candidate_code_hash"],
        "slcx002_release_manifest_sha256": slcx002["release_manifest_sha256"],
        "slcx003_release_manifest_sha256": slcx003["release_manifest_sha256"],
        "source_manifest_sha256": manifest_hash,
    }
    seal["seal_sha256"] = canonical_sha256(seal)
    seal_path = OUT / "V0_6_SLC_C1_PRECOMMIT_SEAL.json"
    seal_path.write_text(json.dumps(seal, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(seal, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
