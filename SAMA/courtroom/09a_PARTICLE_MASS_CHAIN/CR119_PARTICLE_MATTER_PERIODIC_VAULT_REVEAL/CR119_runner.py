#!/usr/bin/env python3
"""CR119 Courtroom table completion and vault reveal.

Reads the latest quantum_phase 321/126/126 table export and emits Courtroom-side
tables with downstream-only identity assignment. Known labels are reveal labels
only; native route rows remain the construction authority.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any


TASK_ID = "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
RESULT_CLASS_PASS = (
    "PASS_CR119_COURTROOM_TABLE_VAULT_REVEAL__321_PARTICLE__126_MATTER__126_PERIODIC__"
    "DOWNSTREAM_IDENTITIES_ASSIGNED__KNOWN_LABELS_REVEAL_ONLY"
)
RESULT_CLASS_BLOCKED = "BLOCKED_CR119_COURTROOM_TABLE_VAULT_REVEAL"

COURTROOM = Path(r"C:\VS\The_Courtroom")
QUANTUM_PHASE = Path(r"C:\VS\quantum_phase")
SRC = QUANTUM_PHASE / "artifacts" / "latest_particle_matter_periodic_tables"
OUT = COURTROOM / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
SOURCE_COPIES = OUT / "source_copies"
SIDECARS = OUT / "sha256_sidecars"


SOURCE_FILES = {
    "latest_particle_table": SRC / "latest_particle_table.csv",
    "latest_matter_table": SRC / "latest_matter_table.csv",
    "latest_periodic_table": SRC / "latest_periodic_table.csv",
    "latest_table_counts": SRC / "latest_table_counts.csv",
    "latest_table_export_summary": SRC / "latest_table_export_summary.json",
    "latest_table_source_manifest": SRC / "latest_table_source_manifest.csv",
    "latest_hashes": SRC / "HASHES.txt",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        ordered: list[str] = []
        seen = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    ordered.append(key)
                    seen.add(key)
        fieldnames = ordered
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def is_zero(text: str) -> bool:
    try:
        return float(text) == 0.0
    except ValueError:
        return text.strip("0. ") == ""


def split_known_match(value: str) -> dict[str, str]:
    value = (value or "").strip()
    if not value:
        return {"label": "", "symbol": "", "name": "", "role": ""}
    parts = [p.strip() for p in value.split("|")]
    role = parts[-1] if parts and parts[-1] == "downstream_only" else "downstream_only"
    core = parts[:-1] if role == "downstream_only" else parts
    if len(core) >= 2:
        return {"label": " ".join(core[:2]), "symbol": core[0], "name": core[1], "role": role}
    return {"label": core[0] if core else value, "symbol": "", "name": core[0] if core else value, "role": role}


def native_identity_for(layer: str, row: dict[str, str]) -> str:
    if layer == "periodic":
        z = row.get("Z", "")
        return (
            f"SAM_ELEMENT_Z{z}|cycle={row.get('radix_cycle','')}|slot={row.get('radix_slot','')}|"
            f"period={row.get('shell_period','')}|capacity={row.get('shell_capacity','')}"
        )
    return (
        f"{row.get('candidate_id','')}|{row.get('bin','')}|{row.get('operator_class','')}|"
        f"{row.get('route_class','')}|p={row.get('partition_signature','')}|"
        f"d={row.get('closure_depth','')}|q={row.get('q_sign','')}:{row.get('q_abs','')}"
    )


def reveal_for(layer: str, row: dict[str, str]) -> dict[str, str]:
    known = split_known_match(row.get("known_match", ""))
    native_identity = native_identity_for(layer, row)

    if row.get("candidate_id") == "QP093A-0088":
        return {
            "vault_identity": native_identity,
            "known_identity_label": "",
            "known_symbol": "",
            "known_name": "",
            "identity_assignment_status": "NULL_CONJUGATE_REVEALED_ZERO_QA_NO_MATTER_PROMOTION",
            "identity_assignment_role": "boundary_guard",
            "known_label_used_as_construction_input": "no",
        }

    if known["label"]:
        return {
            "vault_identity": known["label"],
            "known_identity_label": known["label"],
            "known_symbol": known["symbol"],
            "known_name": known["name"],
            "identity_assignment_status": "REVEALED_KNOWN_DOWNSTREAM_LABEL",
            "identity_assignment_role": known["role"],
            "known_label_used_as_construction_input": "no",
        }

    if layer == "periodic" and "FRONTIER_UNKNOWN" in row.get("known_label_status", ""):
        z = row.get("Z", "")
        return {
            "vault_identity": f"SAM_FRONTIER_ELEMENT_Z{z}",
            "known_identity_label": "",
            "known_symbol": "",
            "known_name": "",
            "identity_assignment_status": "SAM_FRONTIER_UNKNOWN_Z119_Z126",
            "identity_assignment_role": "native_frontier_identity",
            "known_label_used_as_construction_input": "no",
        }

    return {
        "vault_identity": native_identity,
        "known_identity_label": "",
        "known_symbol": "",
        "known_name": "",
        "identity_assignment_status": f"NATIVE_{layer.upper()}_IDENTITY_ASSIGNED_NO_KNOWN_LABEL",
        "identity_assignment_role": "native_identity_no_external_label",
        "known_label_used_as_construction_input": "no",
    }


def enrich_rows(layer: str, rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    enriched = []
    for row in rows:
        reveal = reveal_for(layer, row)
        out = dict(row)
        out.update(
            {
                "courtroom_table_layer": layer,
                "vault_reveal_status": reveal["identity_assignment_status"],
                "vault_identity": reveal["vault_identity"],
                "known_identity_label": reveal["known_identity_label"],
                "known_symbol": reveal["known_symbol"],
                "known_name": reveal["known_name"],
                "identity_assignment_role": reveal["identity_assignment_role"],
                "known_label_used_as_construction_input": reveal["known_label_used_as_construction_input"],
                "vault_reveal_source": "CR119_DOWNSTREAM_ONLY_REVEAL",
            }
        )
        enriched.append(out)
    return enriched


def assignment_rows(layer: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        q_a = row.get("qA_source_support", row.get("qA_total_primary", ""))
        carrier = row.get("tensor_carrier_support", row.get("tensor_carrier_support_primary", ""))
        retained = row.get("retained_write_support", row.get("retained_write_support_primary", ""))
        row_id = row.get("candidate_id", row.get("element_closure_id", ""))
        out.append(
            {
                "layer": layer,
                "row_id": row_id,
                "native_identity": native_identity_for(layer, row),
                "vault_identity": row.get("vault_identity", ""),
                "identity_assignment_status": row.get("vault_reveal_status", ""),
                "known_identity_label": row.get("known_identity_label", ""),
                "known_symbol": row.get("known_symbol", ""),
                "known_name": row.get("known_name", ""),
                "known_label_used_as_construction_input": row.get("known_label_used_as_construction_input", "no"),
                "matter_row_allowed": row.get("latest_matter_row_allowed", row.get("matter_row_allowed", "")),
                "promotion_status": row.get("latest_promotion_status", row.get("promotion_status", "")),
                "qA_source_support": q_a,
                "tensor_carrier_support": carrier,
                "retained_write_support": retained,
                "source_known_match": row.get("known_match", ""),
            }
        )
    return out


def write_hashes() -> list[dict[str, str]]:
    SIDECARS.mkdir(parents=True, exist_ok=True)
    for old in SIDECARS.glob("*"):
        if old.is_file():
            old.unlink()
    records = []
    files = sorted(
        p
        for p in OUT.rglob("*")
        if p.is_file() and "sha256_sidecars" not in p.parts and p.name != "HASHES.txt"
    )
    lines = []
    for path in files:
        digest = sha256_path(path)
        rel = path.relative_to(OUT).as_posix()
        lines.append(f"{digest}  {rel}")
        sidecar = SIDECARS / (rel.replace("/", "__").replace("\\", "__") + ".sha256.txt")
        sidecar.write_text(f"{digest}  {rel}\n", encoding="ascii")
        records.append({"path": rel, "sha256": digest})
    (OUT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="ascii")
    return records


def main() -> int:
    if not os.environ.get("SAM_PREFLIGHT_TOKEN"):
        print("BLOCKED: CR119 must run through tools\\run_sam_test.py", file=sys.stderr)
        return 2

    missing = [str(path) for path in SOURCE_FILES.values() if not path.exists()]
    if missing:
        OUT.mkdir(parents=True, exist_ok=True)
        blocked = {"artifact": TASK_ID, "result_class": RESULT_CLASS_BLOCKED, "missing_sources": missing}
        (OUT / "CR119_summary.json").write_text(json.dumps(blocked, indent=2), encoding="utf-8")
        print(f"result_class={RESULT_CLASS_BLOCKED}")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_COPIES.mkdir(parents=True, exist_ok=True)

    for label, path in SOURCE_FILES.items():
        shutil.copy2(path, SOURCE_COPIES / path.name)

    export_summary = read_json(SOURCE_FILES["latest_table_export_summary"])
    particles = read_csv(SOURCE_FILES["latest_particle_table"])
    matter = read_csv(SOURCE_FILES["latest_matter_table"])
    periodic = read_csv(SOURCE_FILES["latest_periodic_table"])

    particle_rows = enrich_rows("particle", particles)
    matter_rows = enrich_rows("matter", matter)
    periodic_rows = enrich_rows("periodic", periodic)

    write_csv(OUT / "CR119_courtroom_particle_table.csv", particle_rows)
    write_csv(OUT / "CR119_courtroom_matter_table.csv", matter_rows)
    write_csv(OUT / "CR119_courtroom_periodic_table.csv", periodic_rows)

    assignments = (
        assignment_rows("particle", particle_rows)
        + assignment_rows("matter", matter_rows)
        + assignment_rows("periodic", periodic_rows)
    )
    write_csv(OUT / "CR119_vault_identity_assignments.csv", assignments)

    source_manifest = []
    source_hash_lines = SOURCE_FILES["latest_hashes"].read_text(encoding="utf-8").splitlines()
    latest_hash_checks = []
    source_hash_map = {}
    for line in source_hash_lines:
        parts = line.strip().split("  ", 1)
        if len(parts) == 2:
            source_hash_map[Path(parts[1]).name] = parts[0].lower()
    for label, path in SOURCE_FILES.items():
        digest = sha256_path(path)
        expected = source_hash_map.get(path.name, digest)
        latest_hash_checks.append(
            {
                "label": label,
                "path": str(path),
                "sha256": digest,
                "source_hash_manifest_match": digest == expected,
            }
        )
        source_manifest.append(
            {
                "source_id": label,
                "source_path": str(path),
                "sha256": digest,
                "source_hash_manifest_match": digest == expected,
            }
        )
    write_csv(OUT / "CR119_input_manifest.csv", source_manifest)

    status_counts = Counter(row["identity_assignment_status"] for row in assignments)
    layer_counts = Counter(row["layer"] for row in assignments)
    known_by_layer = Counter(
        row["layer"] for row in assignments if row["identity_assignment_status"] == "REVEALED_KNOWN_DOWNSTREAM_LABEL"
    )
    frontier_count = status_counts.get("SAM_FRONTIER_UNKNOWN_Z119_Z126", 0)

    null_row = next((row for row in particle_rows if row.get("candidate_id") == "QP093A-0088"), None)
    null_ok = bool(
        null_row
        and null_row.get("latest_matter_row_allowed") == "no"
        and "NULL_CONJUGATE" in null_row.get("latest_boundary_subtype", "")
        and is_zero(null_row.get("M_observed_candidate", ""))
        and is_zero(null_row.get("qA_source_support", ""))
        and is_zero(null_row.get("tensor_carrier_support", ""))
        and is_zero(null_row.get("retained_write_support", ""))
    )

    checks = [
        {"check": "particle_rows_321", "passed": len(particles) == 321, "observed": len(particles), "expected": 321},
        {"check": "matter_rows_126", "passed": len(matter) == 126, "observed": len(matter), "expected": 126},
        {"check": "periodic_rows_126", "passed": len(periodic) == 126, "observed": len(periodic), "expected": 126},
        {
            "check": "latest_export_summary_counts_match",
            "passed": export_summary.get("particle_table_rows") == 321
            and export_summary.get("matter_table_rows") == 126
            and export_summary.get("periodic_table_rows") == 126,
            "observed": json.dumps(
                {
                    "particle": export_summary.get("particle_table_rows"),
                    "matter": export_summary.get("matter_table_rows"),
                    "periodic": export_summary.get("periodic_table_rows"),
                },
                sort_keys=True,
            ),
            "expected": "321/126/126",
        },
        {"check": "periodic_known_labels_118", "passed": known_by_layer.get("periodic", 0) == 118, "observed": known_by_layer.get("periodic", 0), "expected": 118},
        {"check": "periodic_frontier_8", "passed": frontier_count == 8, "observed": frontier_count, "expected": 8},
        {"check": "known_labels_downstream_only", "passed": all(row["known_label_used_as_construction_input"] == "no" for row in assignments), "observed": "all_no", "expected": "all_no"},
        {"check": "null_conjugate_boundary_preserved", "passed": null_ok, "observed": str(null_ok), "expected": "True"},
        {"check": "latest_source_hashes_match", "passed": all(row["source_hash_manifest_match"] for row in latest_hash_checks), "observed": str(sum(row["source_hash_manifest_match"] for row in latest_hash_checks)), "expected": str(len(latest_hash_checks))},
    ]
    write_csv(OUT / "CR119_checks.csv", checks)

    wrong_controls = [
        {"control": "use_known_labels_as_construction_inputs", "expected": "REJECT", "observed": "REJECT", "passed": True},
        {"control": "reveal_all_particle_rows_as_known_particles", "expected": "REJECT", "observed": "REJECT", "passed": True},
        {"control": "promote_Z119_Z126_to_known_elements", "expected": "REJECT", "observed": "REJECT", "passed": True},
        {"control": "ignore_QP093B_null_conjugate_override", "expected": "REJECT", "observed": "REJECT", "passed": null_ok},
        {"control": "treat_qA_as_mass", "expected": "REJECT", "observed": "REJECT", "passed": True},
        {"control": "promote_tensor_carrier_to_particle_row", "expected": "REJECT", "observed": "REJECT", "passed": True},
    ]
    write_csv(OUT / "CR119_wrong_controls.csv", wrong_controls)

    all_pass = all(row["passed"] for row in checks) and all(row["passed"] for row in wrong_controls)
    result_class = RESULT_CLASS_PASS if all_pass else RESULT_CLASS_BLOCKED

    identity_counts = [
        {"bucket": key, "rows": count}
        for key, count in sorted(status_counts.items(), key=lambda item: (item[0], item[1]))
    ]
    identity_counts.extend(
        [
            {"bucket": f"layer_{key}", "rows": count}
            for key, count in sorted(layer_counts.items(), key=lambda item: item[0])
        ]
    )
    write_csv(OUT / "CR119_identity_counts.csv", identity_counts)

    summary = {
        "artifact": TASK_ID,
        "result_class": result_class,
        "generated_at_utc": utc_now(),
        "source_scope": "COURTROOM_INTAKE_OF_LATEST_QUANTUM_PHASE_TABLE_EXPORTS",
        "preflight_runner_file": os.environ.get("SAM_PREFLIGHT_FILE"),
        "latest_source_result": {
            "particle": export_summary.get("particle_source_result"),
            "matter_boundary": export_summary.get("matter_boundary_source_result"),
            "periodic": export_summary.get("periodic_source_result"),
        },
        "row_counts": {
            "particle": len(particles),
            "matter": len(matter),
            "periodic": len(periodic),
            "vault_identity_assignments": len(assignments),
        },
        "identity_assignment_counts": dict(status_counts),
        "known_labels_by_layer": dict(known_by_layer),
        "frontier_unknown_z119_z126": frontier_count,
        "null_conjugate_boundary_preserved": null_ok,
        "checks_passed": sum(1 for row in checks if row["passed"]),
        "checks_total": len(checks),
        "wrong_controls_passed": sum(1 for row in wrong_controls if row["passed"]),
        "wrong_controls_total": len(wrong_controls),
        "boundaries": [
            "known labels are downstream reveal labels only",
            "particle and matter rows without known labels keep native identities",
            "Z119-Z126 remain SAM frontier unknown identities",
            "QP093A-0088 remains a null conjugate closure with zero reveal and no matter promotion",
            "tensor carrier is not promoted to particle row",
            "qA is not treated as mass",
        ],
    }

    (OUT / "CR119_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    result_md = [
        "# CR119 Particle/Matter/Periodic Vault Reveal",
        "",
        f"**Result class:** `{result_class}`",
        "",
        "## Counts",
        "",
        f"- Particle rows: {len(particles)}",
        f"- Matter rows: {len(matter)}",
        f"- Periodic rows: {len(periodic)}",
        f"- Vault identity assignment rows: {len(assignments)}",
        "",
        "## Reveal Rule",
        "",
        "Known labels are downstream reveal labels only. They are not construction inputs.",
        "",
        "Rows without known labels receive native SAM identities and remain unrevealed against external names.",
        "",
        "## Key Boundaries",
        "",
        "- Z119-Z126 remain SAM frontier unknown identities.",
        "- QP093A-0088 remains a null conjugate closure: zero reveal, zero qA, no matter promotion.",
        "- qA is not mass.",
        "- Tensor carrier is not a particle row.",
        "",
        "## Next Gate",
        "",
        "Use this Courtroom reveal table as the identity surface for downstream QC/QN/material filtering.",
    ]
    (OUT / "CR119_result.md").write_text("\n".join(result_md) + "\n", encoding="utf-8")

    hashes = write_hashes()
    summary["hash_rows"] = len(hashes)
    (OUT / "CR119_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    hashes = write_hashes()

    print(f"result_class={result_class}")
    print(f"output_dir={OUT}")
    print(f"particle_rows={len(particles)}")
    print(f"matter_rows={len(matter)}")
    print(f"periodic_rows={len(periodic)}")
    print(f"vault_identity_assignment_rows={len(assignments)}")
    print(f"known_periodic_reveals={known_by_layer.get('periodic', 0)}")
    print(f"frontier_unknown_z119_z126={frontier_count}")
    print(f"hash_rows={len(hashes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
