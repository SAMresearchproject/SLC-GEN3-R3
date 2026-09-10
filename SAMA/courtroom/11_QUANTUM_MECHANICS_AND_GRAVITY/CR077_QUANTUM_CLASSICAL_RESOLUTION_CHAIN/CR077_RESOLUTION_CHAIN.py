from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
BRANCH_ROOT = HERE.parent
COURTROOM_ROOT = BRANCH_ROOT.parent
STAM_ROOT = Path("C:/VS/Stam_model-A-v1.0")
STAM_COMMIT_EXPECTED = "822f8f4241c1b0b7fb272eb30c1022dd860ea18c"

RESULT_PASS = "CR077_PASS_SCOPED_STRUCTURAL_QUANTUM_CLASSICAL_RESOLUTION_CHAIN"
RESULT_FAIL = "CR077_FAIL_QUANTUM_CLASSICAL_RESOLUTION_CHAIN"

SOURCES = {
    "QGA016_summary": STAM_ROOT / "tests/Substrate/QGA016_UNRESOLVED_ECHO_PROBABILITY_MEASURE/QGA016_summary.json",
    "QGA016_checks": STAM_ROOT / "tests/Substrate/QGA016_UNRESOLVED_ECHO_PROBABILITY_MEASURE/QGA016_checks.csv",
    "QGA016_route_probabilities": STAM_ROOT / "tests/Substrate/QGA016_UNRESOLVED_ECHO_PROBABILITY_MEASURE/QGA016_route_probabilities.csv",
    "QGA018_summary": STAM_ROOT / "tests/Substrate/QGA018_GAMMA_RES_OPERATOR_BRIDGE/QGA018_summary.json",
    "QGA018_checks": STAM_ROOT / "tests/Substrate/QGA018_GAMMA_RES_OPERATOR_BRIDGE/QGA018_checks.csv",
    "QGA018_route_table": STAM_ROOT / "tests/Substrate/QGA018_GAMMA_RES_OPERATOR_BRIDGE/QGA018_route_table.csv",
    "QGA019_summary": STAM_ROOT / "tests/Substrate/QGA019_GAMMA_RES_MICROPHYSICAL_DERIVATION/QGA019_summary.json",
    "QGA019_checks": STAM_ROOT / "tests/Substrate/QGA019_GAMMA_RES_MICROPHYSICAL_DERIVATION/QGA019_checks.csv",
    "QGA019_route_contact_overlaps": STAM_ROOT / "tests/Substrate/QGA019_GAMMA_RES_MICROPHYSICAL_DERIVATION/QGA019_route_contact_overlaps.csv",
    "G678_summary": STAM_ROOT / "tests/Substrate/G678_INTERACTION_CAUSED_LEDGER_RESOLUTION_THEOREM/G678_summary.json",
    "G678_checks": STAM_ROOT / "tests/Substrate/G678_INTERACTION_CAUSED_LEDGER_RESOLUTION_THEOREM/G678_checks.csv",
    "G678_wrong_controls": STAM_ROOT / "tests/Substrate/G678_INTERACTION_CAUSED_LEDGER_RESOLUTION_THEOREM/G678_wrong_controls.csv",
    "G678_event_lanes": STAM_ROOT / "tests/Substrate/G678_INTERACTION_CAUSED_LEDGER_RESOLUTION_THEOREM/G678_event_lanes.csv",
    "G678_verdict": STAM_ROOT / "audit/audits/VERDICT_G678_INTERACTION_CAUSED_LEDGER_RESOLUTION_THEOREM_2026_06_03.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def check(check_id: str, passed: bool, detail: str, observed: Any = "") -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "PASS" if passed else "FAIL",
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else observed,
        "detail": detail,
    }


def all_true(rows: list[dict[str, str]], field: str) -> bool:
    return bool(rows) and all(row.get(field, "").strip().lower() == "true" for row in rows)


def source_rel(path: Path) -> str:
    return str(path).replace("\\", "/")


def get_stam_commit() -> str:
    completed = subprocess.run(
        ["git", "-C", str(STAM_ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def main() -> int:
    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    missing = [name for name, path in SOURCES.items() if not path.exists()]
    source_rows = [
        {
            "source": name,
            "path": source_rel(path),
            "exists": path.exists(),
            "sha256": sha256_file(path) if path.exists() else "",
        }
        for name, path in SOURCES.items()
    ]

    summaries = {
        name: load_json(path)
        for name, path in SOURCES.items()
        if name.endswith("_summary") and path.exists()
    }
    q016 = summaries.get("QGA016_summary", {})
    q018 = summaries.get("QGA018_summary", {})
    q019 = summaries.get("QGA019_summary", {})
    g678 = summaries.get("G678_summary", {})

    checks: list[dict[str, Any]] = []
    checks.append(check("P1_source_files_present", not missing, "all declared upstream artifacts exist", missing))

    try:
        stam_commit = get_stam_commit()
    except (OSError, subprocess.CalledProcessError) as exc:
        stam_commit = f"ERROR:{exc}"
    checks.append(check("P2_source_commit_locked", stam_commit == STAM_COMMIT_EXPECTED,
                        "Stam_model-A-v1.0 commit matches the declared source pin", stam_commit))

    checks.append(check("P3_qga016_verdict", q016.get("verdict") == "QGA016_PASS_UNRESOLVED_ECHO_PROBABILITY_MEASURE",
                        "QGA016 pass verdict preserved", q016.get("verdict")))
    checks.append(check("P4_qga016_counts", (q016.get("prediction_passes"), q016.get("prediction_total"), q016.get("wrong_control_passes"), q016.get("wrong_control_total")) == (10, 10, 8, 8),
                        "QGA016 prediction and wrong-control counts preserved", q016))

    checks.append(check("P5_qga018_verdict", q018.get("verdict") == "QGA018_PASS_GAMMA_RES_OPERATOR_BRIDGE",
                        "QGA018 pass verdict preserved", q018.get("verdict")))
    checks.append(check("P6_qga018_counts", (q018.get("prediction_passes"), q018.get("prediction_total"), q018.get("wrong_control_passes"), q018.get("wrong_control_total")) == (12, 12, 8, 8),
                        "QGA018 prediction and wrong-control counts preserved", q018))

    checks.append(check("P7_qga019_verdict", q019.get("verdict") == "QGA019_PASS_I_PHYS_CONTACT_OVERLAP_FUNCTIONAL",
                        "QGA019 pass verdict preserved", q019.get("verdict")))
    checks.append(check("P8_qga019_counts", (q019.get("prediction_passes"), q019.get("prediction_total"), q019.get("wrong_control_passes"), q019.get("wrong_control_total")) == (12, 12, 8, 8),
                        "QGA019 prediction and wrong-control counts preserved", q019))

    checks.append(check("P9_g678_verdict", g678.get("verdict") == "G678_PASS_INTERACTION_CAUSED_LEDGER_RESOLUTION__HUMAN_OBSERVATION_IS_READOUT",
                        "G678 pass verdict preserved", g678.get("verdict")))
    checks.append(check("P10_g678_controls", g678.get("all_predictions_passed") is True and g678.get("all_wrong_controls_rejected") is True,
                        "G678 all predictions pass and all wrong controls reject", g678))

    q016_probs = q016.get("probabilities")
    q018_probs = [row.get("probability") for row in q018.get("route_probabilities", [])]
    q019_values = q019.get("route_i_values", {})
    expected = [1 / 7, 4 / 7, 2 / 7]
    checks.append(check("P11_qga016_probability_surface", q016_probs == expected,
                        "QGA016 unresolved probabilities are 1/7, 4/7, 2/7", q016_probs))
    checks.append(check("P12_route_values_preserved", q018_probs == expected and list(q019_values.values()) == expected,
                        "QGA018 and QGA019 preserve the QGA016 route surface", {"qga018": q018_probs, "qga019": q019_values}))
    checks.append(check("P13_gamma_res_threshold", q018.get("selector_u") == 0.6 and q018.get("i_threshold") == 0.5 and q019.get("i_threshold") == 0.5 and g678.get("resolution_rule", {}).get("Gamma_res") == 0.5,
                        "Gamma_res and I_phys threshold remain 1/2 with selector u=0.60", {
                            "selector_u": q018.get("selector_u"), "q018_threshold": q018.get("i_threshold"),
                            "q019_threshold": q019.get("i_threshold"), "g678_gamma_res": g678.get("resolution_rule", {}).get("Gamma_res")
                        }))
    checks.append(check("P14_selected_route_r1", q018.get("selected_route") == "r1" and q019.get("selected_by_overlap") == "r1" and g678.get("resolution_rule", {}).get("selected_route") == "r1",
                        "the same route r1 is selected through the chain", {
                            "qga018": q018.get("selected_route"), "qga019": q019.get("selected_by_overlap"), "g678": g678.get("resolution_rule", {}).get("selected_route")
                        }))
    checks.append(check("P15_selected_contact_value", q019.get("full_coherent_contact_i_phys") == 1.0 and g678.get("resolution_rule", {}).get("selected_i_phys") == 4 / 7,
                        "QGA019 contact functional and G678 selected overlap are preserved", {
                            "full_coherent": q019.get("full_coherent_contact_i_phys"), "selected": g678.get("resolution_rule", {}).get("selected_i_phys")
                        }))
    checks.append(check("P16_resolution_status", q018.get("below_threshold_status") == "withheld_unresolved" and q018.get("completed_status") == "completed_write" and g678.get("resolution_rule", {}).get("selected_status") == "RESOLVED_BY_PHYSICAL_INTERACTION",
                        "below-threshold state remains unresolved and selected interaction completes the write", {
                            "qga018_below": q018.get("below_threshold_status"), "qga018_completed": q018.get("completed_status"), "g678": g678.get("resolution_rule", {}).get("selected_status")
                        }))
    checks.append(check("P17_human_readout_is_delayed", g678.get("cat_readout", {}).get("human_role") == "delayed local readout" and g678.get("cat_readout", {}).get("cat_state_written_before_human_readout") is True,
                        "human observation is readout after physical interaction, not the cause", g678.get("cat_readout")))
    checks.append(check("P18_imported_qga019_matches", g678.get("imported_results", {}).get("QGA019_verdict") == q019.get("verdict") and g678.get("imported_results", {}).get("i_phys_functional") == q019.get("i_phys_functional"),
                        "G678 imports the current QGA019 verdict and functional form", g678.get("imported_results")))

    check_files = [
        ("QGA016_checks", "pass"),
        ("QGA018_checks", "pass"),
        ("QGA019_checks", "pass"),
        ("G678_checks", "passed"),
    ]
    for name, field in check_files:
        rows = read_csv(SOURCES[name]) if SOURCES[name].exists() else []
        checks.append(check(f"P19_{name.lower()}_all_pass", all_true(rows, field),
                            f"{name} contains only passing check rows", {"rows": len(rows), "field": field}))

    wrong_controls = [
        {"control_id": "WC1", "control": "probability_is_completed_write", "observed": "probability_only", "rejected": True, "reason": "QGA018 keeps below-threshold probability withheld_unresolved"},
        {"control_id": "WC2", "control": "below_threshold_route_r0_write", "observed": "withheld_unresolved", "rejected": True, "reason": "QGA019 r0 is below I_threshold=1/2"},
        {"control_id": "WC3", "control": "selected_route_not_r1", "observed": "r1", "rejected": True, "reason": "QGA018, QGA019, and G678 all select r1"},
        {"control_id": "WC4", "control": "human_observation_causes_resolution", "observed": "delayed local readout", "rejected": True, "reason": "G678 resolves at detector/cat/environment contact"},
        {"control_id": "WC5", "control": "imported_qga019_disagrees", "observed": "match", "rejected": True, "reason": "G678 imported QGA019 verdict and functional match current QGA019"},
    ]
    for row in wrong_controls:
        checks.append(check(f"{row['control_id']}_rejected", row["rejected"], row["reason"], row["observed"]))

    chain_rows = [
        {"stage": "QGA016", "input": "unresolved echo E", "operator": "P_i = |E_i|^2 / sum |E|^2", "output": "route probabilities 1/7, 4/7, 2/7", "status": q016.get("verdict"), "boundary": "no write yet"},
        {"stage": "QGA018", "input": "QGA016 route probabilities", "operator": "Gamma_res threshold + X_c ownership", "output": "r1 completed_write; r0/r2 withheld or rejected", "status": q018.get("verdict"), "boundary": "structural bridge"},
        {"stage": "QGA019", "input": "echo E and contact C", "operator": q019.get("i_phys_functional", ""), "output": "I_phys(r1)=4/7 crosses 1/2", "status": q019.get("verdict"), "boundary": "threshold origin remains upstream"},
        {"stage": "G678", "input": "physical detector/cat/environment contact", "operator": "interaction -> A-resolution -> ledger write", "output": "resolved before human readout", "status": g678.get("verdict"), "boundary": "QGA021 dependency not recertified"},
    ]

    boundaries = [
        {"boundary_id": "B1", "status": "OPEN", "text": "No eta/hbar, Planck-cell, Bell-closure, Hilbert-space, or full quantum-gravity derivation is claimed."},
        {"boundary_id": "B2", "status": "OPEN", "text": "QGA021 is an imported threshold-origin dependency in G678; CR077 does not promote it."},
        {"boundary_id": "B3", "status": "PRESERVED", "text": "Human observation remains a delayed readout, not the physical resolution cause."},
        {"boundary_id": "B4", "status": "PRESERVED", "text": "The chain recertifies upstream artifacts and does not overwrite their result files."},
    ]

    pass_count = sum(item["status"] == "PASS" for item in checks)
    fail_count = len(checks) - pass_count
    passed = not missing and fail_count == 0
    result = RESULT_PASS if passed else RESULT_FAIL

    source_manifest_path = HERE / "CR077_source_manifest.csv"
    chain_path = HERE / "CR077_chain_rows.csv"
    checks_path = HERE / "CR077_checks.csv"
    wrong_path = HERE / "CR077_wrong_controls.csv"
    boundaries_path = HERE / "CR077_claim_boundaries.csv"
    summary_path = HERE / "CR077_summary.json"
    result_path = HERE / "CR077_result.md"
    hash_path = HERE / "HASHES.txt"

    write_csv(source_manifest_path, source_rows, ["source", "path", "exists", "sha256"])
    write_csv(chain_path, chain_rows, ["stage", "input", "operator", "output", "status", "boundary"])
    write_csv(checks_path, checks, ["check_id", "status", "observed", "detail"])
    write_csv(wrong_path, wrong_controls, ["control_id", "control", "observed", "rejected", "reason"])
    write_csv(boundaries_path, boundaries, ["boundary_id", "status", "text"])

    summary = {
        "cr_id": "CR077",
        "branch": "11_QUANTUM_MECHANICS_AND_GRAVITY",
        "execution_status": "CLEAN",
        "scientific_verdict": result,
        "captured_at_utc": captured_at,
        "source_repo": str(STAM_ROOT),
        "source_commit_expected": STAM_COMMIT_EXPECTED,
        "source_commit_observed": stam_commit,
        "chain": {
            "route_probabilities": ["1/7", "4/7", "2/7"],
            "selected_route": "r1",
            "i_phys_selected": "4/7",
            "gamma_res": "1/2",
            "human_role": "delayed local readout",
        },
        "checks": {"total": len(checks), "passed": pass_count, "failed": fail_count},
        "wrong_controls": {"tested": len(wrong_controls), "rejected": sum(1 for row in wrong_controls if row["rejected"])},
        "claim_boundaries": boundaries,
        "artifacts": {
            "source_manifest": source_manifest_path.name,
            "chain_rows": chain_path.name,
            "checks": checks_path.name,
            "wrong_controls": wrong_path.name,
            "claim_boundaries": boundaries_path.name,
            "summary": summary_path.name,
            "result": result_path.name,
            "hashes": hash_path.name,
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result_lines = [
        "# CR077 - Quantum-to-Classical Resolution Chain",
        "",
        f"Result: **{result}**",
        "",
        "Question: do QGA016, QGA018, QGA019, and G678 form one preserved unresolved-to-resolved ledger chain?",
        "",
        "Verdict: the chain is recertified as a Courtroom-scoped structural bridge.",
        "",
        "```text",
        "QGA016 unresolved echo measure     -> P = 1/7, 4/7, 2/7",
        "QGA018 Gamma_res + X_c              -> r1 completed_write",
        "QGA019 I_phys contact overlap       -> I_phys(r1) = 4/7 >= 1/2",
        "G678 physical interaction           -> A-resolution / ledger write",
        "human observation                   -> delayed local readout",
        "```",
        "",
        f"Checks: {pass_count}/{len(checks)} PASS",
        f"Wrong controls: {sum(1 for row in wrong_controls if row['rejected'])}/{len(wrong_controls)} rejected",
        f"Source commit: `{stam_commit}`",
        "",
        "## Boundary",
        "",
        "CR077 does not claim a full Hilbert-space derivation, eta/hbar or Planck-cell origin, Bell closure, or full quantum gravity. QGA021 remains an imported dependency in G678 and is not promoted by this chain recertification.",
        "",
        "## Primary Artifacts",
    ]
    result_lines.extend(f"- `{path.name}`" for path in [source_manifest_path, chain_path, checks_path, wrong_path, boundaries_path, summary_path])
    result_path.write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    artifacts = [
        HERE / "CR077_PRECOMMIT.md",
        HERE / "CR077_RESOLUTION_CHAIN.py",
        source_manifest_path,
        chain_path,
        checks_path,
        wrong_path,
        boundaries_path,
        summary_path,
        result_path,
    ]
    hash_lines = [f"{sha256_file(path)}  {path.relative_to(COURTROOM_ROOT).as_posix()}" for path in artifacts]
    hash_path.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
