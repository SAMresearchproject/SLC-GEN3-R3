#!/usr/bin/env python3
"""Approved Courtroom replay for the Starbreaker 3D external-contact chain."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
COURTROOM = ROOT.parents[1]
BASEMENT = Path(r"C:\VS\The_Basement")
SIM = BASEMENT / "15_SCALE_BRIDGE_SIMULATOR"
GEOMETRY = SIM / "STARBREAKER_3D_DENSITY_GEOMETRY"
CONTACT = SIM / "STARBREAKER_EXTERNAL_COLLAPSE_CONTACT"
PAYLOAD = ROOT / "frozen_payload"
LOG_PATH = ROOT / "CR210_replay.log"
PRECOMMIT = ROOT / "CR210_precommit_source_manifest.json"

RESULT_CLASS = (
    "CR210_PASS_SCOPED_STARBREAKER_3D_EXTERNAL_COLLAPSE_DIRECTIONAL_CONTACT__"
    "NO_PHYSICAL_PROMOTION__OPEN_TIME_RESOLVED_COLLAPSE"
)

TEST_SUITES = (
    ("starbreaker_lab", SIM / "STARBREAKER_LAB" / "tests", 8),
    ("mechanism_audit", SIM / "STARBREAKER_MECHANISM_AUDIT" / "tests", 8),
    ("cr120u_sidecar", SIM / "STARBREAKER_CR120U_INCIDENCE_SIDECAR" / "tests", 9),
    ("carrier_density_field", SIM / "STARBREAKER_CARRIER_DENSITY_FIELD" / "tests", 12),
    ("density_coupling_2d", SIM / "STARBREAKER_CARRIER_DENSITY_COUPLING" / "tests", 7),
    ("density_geometry_3d", GEOMETRY / "tests", 6),
    ("external_collapse_contact", CONTACT / "tests", 8),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV forbidden: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def append_log(label: str, command: list[str], result: subprocess.CompletedProcess[str]) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"\n===== {label} =====\n")
        handle.write("command: " + " ".join(command) + "\n")
        handle.write(f"returncode: {result.returncode}\n")
        handle.write("--- stdout ---\n")
        handle.write(result.stdout or "")
        handle.write("\n--- stderr ---\n")
        handle.write(result.stderr or "")
        handle.write("\n")


def run_command(label: str, command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    print(f"[CR210] {label}", flush=True)
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    append_log(label, command, result)
    if result.returncode != 0:
        raise RuntimeError(f"{label} failed with exit code {result.returncode}; see {LOG_PATH}")
    return result


def require_approved_preflight() -> tuple[str, str]:
    preflight_value = os.environ.get("SAM_PREFLIGHT_FILE", "")
    root_id = os.environ.get("SAM_PREFLIGHT_ROOT_ID", "")
    if not preflight_value or root_id != "SAM_TEST_PREFLIGHT_V4_2_LOCKED":
        raise RuntimeError("CR210 must run through the SAM V4.2 preflight wrapper")
    preflight = Path(preflight_value)
    text = preflight.read_text(encoding="utf-8")
    if "class = CONFIRMATION_OR_AUDIT_REQUIRES_PERMISSION" not in text:
        raise RuntimeError("CR210 replay was not classified as an audit/retest")
    if "permission status = GRANTED_BY_USER:" not in text:
        raise RuntimeError("CR210 replay lacks the task-specific approval grant")
    return str(preflight), root_id


def check_precommit(stage: str) -> list[dict[str, object]]:
    manifest = json.loads(PRECOMMIT.read_text(encoding="utf-8"))
    rows = []
    for entry in manifest["entries"]:
        path = Path(entry["path"])
        exists = path.exists()
        observed_hash = sha256(path) if exists else None
        observed_bytes = path.stat().st_size if exists else None
        rows.append(
            {
                "stage": stage,
                "role": entry["role"],
                "path": str(path),
                "expected_sha256": entry["sha256"],
                "observed_sha256": observed_hash,
                "expected_bytes": entry["bytes"],
                "observed_bytes": observed_bytes,
                "exact_match": exists
                and observed_hash == entry["sha256"]
                and observed_bytes == entry["bytes"],
            }
        )
    return rows


def copy_payload() -> list[dict[str, object]]:
    rows = []
    groups = (
        (GEOMETRY / "outputs", PAYLOAD / "starbreaker_3d_density_geometry"),
        (CONTACT / "outputs", PAYLOAD / "starbreaker_external_collapse_contact"),
    )
    for source_dir, target_dir in groups:
        target_dir.mkdir(parents=True, exist_ok=True)
        for source in sorted(source_dir.iterdir(), key=lambda item: item.name.lower()):
            if not source.is_file():
                continue
            target = target_dir / source.name
            shutil.copy2(source, target)
            if sha256(source) != sha256(target):
                raise RuntimeError(f"payload copy hash mismatch: {source}")
            rows.append(
                {
                    "file_id": f"payload_{target_dir.name}_{source.stem}",
                    "role": (
                        "presentation_only" if source.suffix.lower() == ".html" else "frozen_source_evidence"
                    ),
                    "source_path": str(source),
                    "courtroom_path": str(target),
                    "relative_path": str(target.relative_to(COURTROOM)),
                    "bytes": target.stat().st_size,
                    "sha256": sha256(target),
                }
            )
    return rows


def payload_fingerprint(rows: list[dict[str, object]]) -> str:
    payload = "\n".join(
        f"{row['relative_path']}|{row['bytes']}|{row['sha256']}" for row in rows
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    preflight_path, preflight_root_id = require_approved_preflight()
    LOG_PATH.write_text(
        "CR210 approved Starbreaker replay\n"
        f"generated_at_utc: {datetime.now(timezone.utc).isoformat()}\n"
        f"preflight: {preflight_path}\n",
        encoding="utf-8",
    )

    before = check_precommit("before_replay")
    if not all(row["exact_match"] for row in before):
        write_csv(ROOT / "CR210_replay_hash_comparison.csv", before)
        raise RuntimeError("precommit source boundary did not match before replay")

    replay_rows: list[dict[str, object]] = []
    start = datetime.now(timezone.utc)
    result = run_command(
        "full_3d_geometry_replay_1218_simulations",
        [sys.executable, str(GEOMETRY / "run_starbreaker_3d_density_geometry.py"), "--self-test"],
        GEOMETRY,
    )
    replay_rows.append(
        {
            "suite": "full_3d_geometry_replay",
            "kind": "full_result_replay",
            "expected_simulations": 1218,
            "tests_expected": 0,
            "tests_observed": 0,
            "returncode": result.returncode,
            "pass": result.returncode == 0,
        }
    )

    result = run_command(
        "external_collapse_contact_replay",
        [sys.executable, str(CONTACT / "run_starbreaker_external_collapse_contact.py"), "--self-test"],
        CONTACT,
    )
    replay_rows.append(
        {
            "suite": "external_collapse_contact_replay",
            "kind": "read_only_external_contact_replay",
            "expected_simulations": 0,
            "tests_expected": 0,
            "tests_observed": 0,
            "returncode": result.returncode,
            "pass": result.returncode == 0,
        }
    )

    total_tests = 0
    for suite, tests_dir, expected in TEST_SUITES:
        result = run_command(
            f"regression_{suite}",
            [sys.executable, "-m", "unittest", "discover", "-s", str(tests_dir), "-q"],
            BASEMENT,
        )
        output = (result.stdout or "") + "\n" + (result.stderr or "")
        match = re.search(r"Ran\s+(\d+)\s+tests?", output)
        observed = int(match.group(1)) if match else -1
        passed = result.returncode == 0 and observed == expected
        replay_rows.append(
            {
                "suite": suite,
                "kind": "regression_suite",
                "expected_simulations": 0,
                "tests_expected": expected,
                "tests_observed": observed,
                "returncode": result.returncode,
                "pass": passed,
            }
        )
        if not passed:
            raise RuntimeError(f"unexpected test count or failure in {suite}: {observed}/{expected}")
        total_tests += observed

    after = check_precommit("after_replay")
    comparison = [*before, *after]
    write_csv(ROOT / "CR210_replay_hash_comparison.csv", comparison)
    if not all(row["exact_match"] for row in after):
        raise RuntimeError("replayed output or source hash drifted from the sealed precommit")

    geometry_summary = json.loads(
        (GEOMETRY / "outputs" / "starbreaker_3d_density_geometry_summary.json").read_text(encoding="utf-8")
    )
    contact_summary = json.loads(
        (CONTACT / "outputs" / "starbreaker_external_collapse_contact_summary.json").read_text(encoding="utf-8")
    )
    payload_rows = copy_payload()
    fingerprint = payload_fingerprint(payload_rows)
    readout = {row["geometry"]: row for row in contact_summary["geometry_readout"]}

    pass_conditions = {
        "approved_audit_preflight_present": True,
        "precommit_boundary_exact_before_replay": all(row["exact_match"] for row in before),
        "full_1218_simulation_3d_replay_pass": (
            geometry_summary["status"]
            == "PASS_INTERNAL_3D_GEOMETRY_GATE__EXTERNAL_PHYSICS_VALIDATION_OPEN"
            and geometry_summary["run_counts"]["total_3d_simulations"] == 1218
            and geometry_summary["invariants"]["all_pass"]
        ),
        "external_contact_replay_pass": (
            contact_summary["status"]
            == "PASS_EXTERNAL_QUALITATIVE_DIRECTIONAL_CONTACT__NO_PHYSICAL_PROMOTION"
            and contact_summary["invariants"]["all_pass"]
        ),
        "all_58_regression_tests_pass": total_tests == 58 and all(row["pass"] for row in replay_rows),
        "all_28_precommit_entries_reproduce_exactly": (
            len(after) == 28 and all(row["exact_match"] for row in after)
        ),
        "all_42_runwise_ladders_strict": sum(
            int(row["runwise_monotonic_passes"]) for row in contact_summary["geometry_readout"]
        )
        == 42,
        "all_42_same_total_comparisons_point_inward": sum(
            int(row["same_total_direction_passes"]) for row in contact_summary["geometry_readout"]
        )
        == 42,
        "both_aligned_allocations_maximize_remnant_over_24_permutations": all(
            row["aligned_is_permutation_maximum"] and row["permutation_count"] == 24
            for row in contact_summary["geometry_readout"]
        ),
        "zero_fitted_parameters": contact_summary["run_counts"]["fitted_parameters"] == 0,
        "one_external_signature_only": contact_summary["external_signature"]["signature_id"].startswith("OO2011_"),
        "frozen_payload_copies_close": len(payload_rows) == 22,
    }
    all_pass = all(pass_conditions.values())
    if not all_pass:
        raise RuntimeError(f"CR210 pass conditions failed: {pass_conditions}")

    wrong_controls = [
        {"control": "WC_EQUATE_P_WITH_XI_2_5", "rejected": True, "reason": "p remains an internal ledger-packing index without compactness units"},
        {"control": "WC_EQUATE_REMNANT_FRACTION_WITH_BH_PROBABILITY", "rejected": True, "reason": "Starbreaker fate counts are not black-hole probabilities or masses"},
        {"control": "WC_CLAIM_FASTER_FORMATION_FROM_ENDPOINTS", "rejected": True, "reason": "the endpoint simulator has no time-to-collapse observable"},
        {"control": "WC_IMPORT_EXTERNAL_FIT_OR_THRESHOLD", "rejected": True, "reason": "zero external values or fit parameters enter Starbreaker"},
        {"control": "WC_ACCEPT_NONDETERMINISTIC_REPLAY", "rejected": True, "reason": "all 28 sealed source and output files must reproduce exact SHA-256 digests"},
        {"control": "WC_TREAT_HTML_AS_AUTHORITY", "rejected": True, "reason": "the plate is presentation-only; JSON CSV logs and hashes are authoritative"},
        {"control": "WC_OVERWRITE_BASEMENT_PROVENANCE", "rejected": True, "reason": "Courtroom stores a companion snapshot and does not replace the Basement source"},
        {"control": "WC_PROMOTE_A_PACKING_LAW_PHYSICALLY", "rejected": True, "reason": "the kinematic A proxy and physical calibration remain open"},
    ]
    write_csv(ROOT / "CR210_replay_tests.csv", replay_rows)
    write_csv(ROOT / "CR210_wrong_controls.csv", wrong_controls)

    input_rows = [
        {
            "source_id": f"sealed_{index:02d}",
            "path": row["path"],
            "role": row["role"],
            "sha256": row["observed_sha256"],
            "bytes": row["observed_bytes"],
            "used_as_computed_input": True,
        }
        for index, row in enumerate(after, start=1)
    ]
    write_csv(ROOT / "CR210_input_manifest.csv", input_rows)

    evidence = [
        {"key": "wrapped_preflight_root", "value": preflight_root_id, "note": "SAM V4.2 locked wrapper"},
        {"key": "full_3d_replay", "value": "1218/1218", "note": "two geometries, p=0..3, same-total and all 24 permutations"},
        {"key": "regression_tests", "value": f"{total_tests}/{total_tests}", "note": "full Starbreaker chain"},
        {"key": "exact_replay_hashes", "value": f"{sum(row['exact_match'] for row in after)}/{len(after)}", "note": "post-replay versus precommit"},
        {"key": "localized_remnant_ladder", "value": "|".join(f"{value:.6f}" for value in readout["localized_ledger_cells"]["mean_remnant_ladder"]), "note": "strict p=0,1,2,3 means"},
        {"key": "dispersed_remnant_ladder", "value": "|".join(f"{value:.6f}" for value in readout["dispersed_slots"]["mean_remnant_ladder"]), "note": "strict p=0,1,2,3 means"},
        {"key": "runwise_monotonic_ladders", "value": "42/42", "note": "all locked geometry anchor seed ladders"},
        {"key": "same_total_inward_wins", "value": "42/42", "note": "inward p=3 versus uniform 56-ledger controls"},
        {"key": "aligned_radial_permutation_rank", "value": "2/2 maximum of 24", "note": "both 3D geometry families"},
        {"key": "fitted_parameters", "value": 0, "note": "direction only; no external fit"},
        {"key": "payload_fingerprint_sha256", "value": fingerprint, "note": "22-file Courtroom snapshot"},
        {"key": "remaining_boundary", "value": "OPEN_TIME_RESOLVED_COLLAPSE_AND_PHYSICAL_CALIBRATION", "note": "endpoint directional contact only"},
    ]
    write_csv(ROOT / "CR210_evidence_rows.csv", evidence)

    finished = datetime.now(timezone.utc)
    summary = {
        "test_id": "CR210",
        "title": "Starbreaker 3D External Collapse Directional Contact Replay",
        "generated_at_utc": finished.isoformat(),
        "duration_seconds": (finished - start).total_seconds(),
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "result_class": RESULT_CLASS,
        "triage_bin": "A",
        "claim_tier": "SCOPED_QUALITATIVE_DIRECTIONAL_CONTACT",
        "is_audit_or_retest": True,
        "confirmation_or_double_check": True,
        "approval": "approved",
        "preflight_file": preflight_path,
        "preflight_root_id": preflight_root_id,
        "question": "Does the latest Starbreaker 3D carrier-density result replay exactly and retain no-fit qualitative contact with the frozen compactness-collapse direction?",
        "pass_conditions": pass_conditions,
        "all_pass_conditions_true": all_pass,
        "evidence_rows": evidence,
        "run_counts": {
            "full_3d_simulations": 1218,
            "regression_tests": total_tests,
            "sealed_entries_replayed": len(after),
            "frozen_payload_files": len(payload_rows),
            "new_model_parameters": 0,
            "fitted_parameters": 0,
        },
        "source_result_classes": {
            "three_dimensional": geometry_summary["status"],
            "external_contact": contact_summary["status"],
        },
        "payload_fingerprint_sha256": fingerprint,
        "payload_manifest": payload_rows,
        "preserved_boundaries": json.loads((ROOT / "CR210_declared_premises.json").read_text(encoding="utf-8"))["preserved_boundaries"],
        "rule_9_falsification": "CR210 would fail if any wrapped replay or regression failed, any sealed source/output hash drifted, either 3D mean ladder ceased to rise strictly, fewer than 90% of runwise or same-total comparisons pointed toward stronger remnant formation, either aligned allocation lost its maximum-remnant rank, or any external fit parameter entered the simulator.",
        "next_gate": "Freeze one time-resolved internal collapse observable before comparing formation-time direction; do not reopen this endpoint freeze.",
    }
    (ROOT / "CR210_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# CR210 Starbreaker 3D External Collapse Directional Contact Replay",
        "",
        "## Verdict",
        "",
        "```text",
        RESULT_CLASS,
        "```",
        "",
        "## Courtroom Fields",
        "",
        "```text",
        "execution_status = CLEAN",
        "scientific_verdict = PASS",
        "triage_bin = A",
        "claim_tier = SCOPED_QUALITATIVE_DIRECTIONAL_CONTACT",
        "audit_approval = approved",
        "```",
        "",
        "## Positive Readout",
        "",
        "The approved Courtroom replay regenerated all 1,218 three-dimensional simulations, rebuilt the no-fit external contact from those fresh outputs, and passed all 58 Starbreaker regression tests. All 28 precommitted source/output files reproduced their SHA-256 digests exactly.",
        "",
        "Both remnant ladders remain strictly ordered across p=0,1,2,3. All 42 individual ladders rise at every step, all 42 inward p=3 allocations beat their same-total uniform controls, and both aligned allocations remain the maximum-remnant arrangement among all 24 radial permutations.",
        "",
        "## Scope Boundary",
        "",
        "This is a scoped qualitative directional-contact PASS. It does not identify p with physical compactness, identify the Starbreaker remnant with a black hole, test faster formation time, solve stellar hydrodynamics or relativity, calibrate A, or physically promote the packing law.",
        "",
        "The HTML plate is frozen as presentation-only. JSON, CSV, wrapped logs, and SHA-256 records are the authority.",
        "",
        "## Rule-9 Line",
        "",
        summary["rule_9_falsification"],
        "",
        "## Next Gate",
        "",
        summary["next_gate"],
        "",
    ]
    (ROOT / "CR210_result.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"result_class": RESULT_CLASS, "all_pass": all_pass, "tests": total_tests, "payload_fingerprint_sha256": fingerprint}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
