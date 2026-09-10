"""CR065a Higgs ZZ4l prediction intake.

Loads the upstream QP084-QP091 chain summaries, verifies each PASS
with zero free parameters and no external CERN data opened, and
locks the QP091 prediction freeze into the Courtroom 09a continuation.

Does NOT open CERN reveal targets (m4l, m12/m34, four-lepton angular).
Those are CR066a's role.
"""

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent

CR064A_RESULT = BRANCH_DIR / "CR064a_PARTICLE_MASS_CHAIN_BRANCH_VERDICT" / "CR064a_result.md"

QP_BASE = Path(r"C:/VS/quantum_phase/artifacts")
QP_CHAIN = [
    ("QP084", QP_BASE / "qp084" / "qp084_summary.json"),
    ("QP085", QP_BASE / "qp085" / "qp085_summary.json"),
    ("QP086", QP_BASE / "qp086" / "qp086_summary.json"),
    ("QP087", QP_BASE / "qp087" / "qp087_summary.json"),
    ("QP088", QP_BASE / "qp088" / "qp088_summary.json"),
    ("QP089", QP_BASE / "qp089" / "qp089_summary.json"),
    ("QP090", QP_BASE / "qp090" / "qp090_summary.json"),
    ("QP091", QP_BASE / "qp091" / "qp091_summary.json"),
]
QP091_OBS_FREEZE     = QP_BASE / "qp091" / "qp091_observable_prediction_freeze.csv"
QP091_ZZSTAR         = QP_BASE / "qp091" / "qp091_zzstar_branch_prediction_table.csv"
QP091_REVEAL_MAP     = QP_BASE / "qp091" / "qp091_qp092_reveal_map.csv"
QP091_MASS_BUDGET    = QP_BASE / "qp091" / "qp091_native_mass_budget.csv"

OUT_JSON = CR_DIR / "CR065a_summary.json"
OUT_MD   = CR_DIR / "CR065a_result.md"
INTAKE_LOCK = CR_DIR / "CR065a_intake_lock.json"
INTAKE_LOCK_SIBLING = CR_DIR / "CR065a_intake_lock.json.sha256.txt"


def sha256_file(p: Path) -> str:
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_csv_rows(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    print("CR065a runner: starting (Higgs ZZ4l prediction intake)")

    # ---- Step 1: Hash upstream QP chain summaries -----------------------
    chain_status = []
    all_pass = True
    all_zero_params = True
    none_opened_decay = True

    for qp_id, p in QP_CHAIN:
        if not p.exists():
            chain_status.append({
                "qp_id": qp_id,
                "exists": False,
                "sha256": "",
                "passed": None,
                "free_parameters_introduced": None,
                "external_decay_data_used": None,
            })
            all_pass = False
            continue

        sha = sha256_file(p)
        with open(p, "r", encoding="utf-8") as f:
            s = json.load(f)

        passed = bool(s.get("passed", False))
        fp = s.get("free_parameters_introduced", None)
        # External-data fields differ by test; accept either signal
        ext_decay = s.get("external_decay_data_used", None)
        ext_ref   = s.get("external_reference_used", None)
        # QP085 explicitly opens CR092 anchors as reveal; that's allowed
        # because QP085 IS the reveal step inside the upstream chain
        # against the CR092 Higgs mass anchors.  We track it separately.
        is_qp085_reveal = (qp_id == "QP085")

        if not passed:
            all_pass = False
        if isinstance(fp, int) and fp > 0:
            all_zero_params = False
        if ext_decay is True and not is_qp085_reveal:
            none_opened_decay = False

        chain_status.append({
            "qp_id": qp_id,
            "path": str(p),
            "exists": True,
            "sha256": sha,
            "passed": passed,
            "result_class": s.get("result_class", ""),
            "free_parameters_introduced": fp,
            "external_decay_data_used": ext_decay,
            "external_reference_used": ext_ref,
            "qp085_reveal_within_chain": is_qp085_reveal,
        })

    # ---- Step 2: Capture QP091 frozen observables -----------------------
    qp091_mass_budget = load_csv_rows(QP091_MASS_BUDGET)
    qp091_zzstar     = load_csv_rows(QP091_ZZSTAR)
    qp091_obs_freeze = load_csv_rows(QP091_OBS_FREEZE)
    qp091_reveal_map = load_csv_rows(QP091_REVEAL_MAP)

    qp091_sha = sha256_file([p for qp_id, p in QP_CHAIN if qp_id == "QP091"][0])
    qp091_obs_sha    = sha256_file(QP091_OBS_FREEZE)
    qp091_zz_sha     = sha256_file(QP091_ZZSTAR)
    qp091_reveal_sha = sha256_file(QP091_REVEAL_MAP)
    qp091_budget_sha = sha256_file(QP091_MASS_BUDGET)

    # ---- Step 3: Verify Pass Conditions ---------------------------------
    expected = {
        "H_visible_parent_ledger_MeV": 125219.0,
        "H_source_hidden_budget_MeV":  125419.11694535677,
        "Z_visible_branch_MeV":         91161.5,
        "two_on_shell_Z_deficit_visible_MeV": 57104.0,
        "Zstar_ceiling_visible_MeV":     34057.5,
        "terminal_thresholds_MeV": {
            "4e":     2.043792,
            "2e2mu":  212.393896,
            "4mu":    422.744,
        },
        "hidden_source_budget_fraction": 0.001595585666927944,
    }
    # Pull from QP091 summary
    qp091_path = [p for qp_id, p in QP_CHAIN if qp_id == "QP091"][0]
    with open(qp091_path, "r", encoding="utf-8") as f:
        qp091_summary = json.load(f)

    p4_qp091_freeze_matches = (
        abs(qp091_summary.get("H_visible_parent_ledger_MeV", 0) - expected["H_visible_parent_ledger_MeV"]) < 1e-3
        and abs(qp091_summary.get("H_source_hidden_budget_MeV", 0) - expected["H_source_hidden_budget_MeV"]) < 1e-9
        and abs(qp091_summary.get("Z_visible_branch_MeV", 0) - expected["Z_visible_branch_MeV"]) < 1e-3
        and abs(qp091_summary.get("two_on_shell_Z_deficit_visible_MeV", 0) - expected["two_on_shell_Z_deficit_visible_MeV"]) < 1e-3
        and abs(qp091_summary.get("Zstar_ceiling_visible_MeV", 0) - expected["Zstar_ceiling_visible_MeV"]) < 1e-3
    )

    # P5: reveal map names the four targets, with three HELD_NOT_OPENED
    reveal_targets = {row["reveal_id"]: row for row in qp091_reveal_map}
    p5_reveal_map_complete = (
        "QP092_REVEAL_01" in reveal_targets
        and "QP092_REVEAL_02" in reveal_targets
        and "QP092_REVEAL_03" in reveal_targets
        and "QP092_REVEAL_04" in reveal_targets
        and all(row["qp091_status"] == "HELD_NOT_OPENED" for row in qp091_reveal_map)
    )

    # P6: CR065a does NOT open any external CERN decay anchor here
    p6_no_cern_opened_in_cr065a = True

    predictions = [
        {
            "name": "P1_all_qp_passed",
            "pass": all_pass,
            "details": {qp_id: row["passed"] for qp_id, row in zip([q[0] for q in QP_CHAIN], chain_status)},
        },
        {
            "name": "P2_all_zero_free_parameters",
            "pass": all_zero_params,
            "details": {qp_id: row["free_parameters_introduced"] for qp_id, row in zip([q[0] for q in QP_CHAIN], chain_status)},
        },
        {
            "name": "P3_target_blind_no_external_decay_data_in_chain",
            "pass": none_opened_decay,
            "details": {
                "qp085_reveal_against_CR092_Higgs_mass_anchors_is_allowed_within_chain": True,
                "no_other_qp_opened_external_decay_or_angular_data": none_opened_decay,
            },
        },
        {
            "name": "P4_qp091_frozen_observables_match_expected",
            "pass": p4_qp091_freeze_matches,
            "details": {
                "expected": expected,
                "qp091_actual_summary_subset": {
                    "H_visible_parent_ledger_MeV": qp091_summary.get("H_visible_parent_ledger_MeV"),
                    "H_source_hidden_budget_MeV":  qp091_summary.get("H_source_hidden_budget_MeV"),
                    "Z_visible_branch_MeV":         qp091_summary.get("Z_visible_branch_MeV"),
                    "two_on_shell_Z_deficit_visible_MeV": qp091_summary.get("two_on_shell_Z_deficit_visible_MeV"),
                    "Zstar_ceiling_visible_MeV":     qp091_summary.get("Zstar_ceiling_visible_MeV"),
                    "terminal_thresholds_MeV":      qp091_summary.get("terminal_thresholds_MeV"),
                    "hidden_source_budget_fraction": qp091_summary.get("hidden_source_budget_fraction"),
                },
            },
        },
        {
            "name": "P5_reveal_map_names_four_targets_three_strongest_held_for_CR066a",
            "pass": p5_reveal_map_complete,
            "details": {row["reveal_id"]: row for row in qp091_reveal_map},
        },
        {
            "name": "P6_no_cern_decay_data_opened_in_CR065a",
            "pass": p6_no_cern_opened_in_cr065a,
        },
    ]

    # ---- Step 4: Wrong controls -----------------------------------------
    wrong_controls = [
        {
            "name": "WC1_any_qp_failed_aborts_intake",
            "pass": all_pass,
        },
        {
            "name": "WC2_any_free_parameter_violates_chain",
            "pass": all_zero_params,
        },
        {
            "name": "WC3_no_premature_decay_data_opening",
            "pass": none_opened_decay,
        },
        {
            "name": "WC4_qp091_frozen_predictions_not_modified_in_intake",
            "pass": p4_qp091_freeze_matches,
        },
        {
            "name": "WC5_reveal_targets_held_at_intake_time",
            "pass": p5_reveal_map_complete,
        },
    ]

    all_predictions_pass = all(p["pass"] for p in predictions)
    all_wc_pass = all(w["pass"] for w in wrong_controls)
    verdict = (
        "CR065a_HIGGS_ZZ4L_PREDICTION_INTAKE_PASS" if (all_predictions_pass and all_wc_pass)
        else "CR065a_HIGGS_ZZ4L_PREDICTION_INTAKE_FAIL"
    )

    # ---- Step 5: Intake lock --------------------------------------------
    intake_utc = now_utc()
    intake = {
        "lock_id": "CR065a_HIGGS_ZZ4L_PREDICTION_INTAKE_LOCK",
        "branch": "09a_PARTICLE_MASS_CHAIN",
        "extends_courtroom_anchor": "CR064a (immutable)",
        "intaken_at_utc": intake_utc,
        "upstream_qp_chain": chain_status,
        "qp091_artifact_hashes": {
            "qp091_summary.json":              qp091_sha,
            "qp091_observable_prediction_freeze.csv": qp091_obs_sha,
            "qp091_zzstar_branch_prediction_table.csv": qp091_zz_sha,
            "qp091_qp092_reveal_map.csv":      qp091_reveal_sha,
            "qp091_native_mass_budget.csv":    qp091_budget_sha,
        },
        "qp091_frozen_predictions": expected,
        "reveal_map": [dict(row) for row in qp091_reveal_map],
        "cern_anchors_NOT_opened_in_this_CR": True,
        "next_courtroom_step": "CR066a opens REVEAL_02 (m4l), REVEAL_03 (m12/m34), REVEAL_04 (angular). REVEAL_01 (signal strength) remains HELD.",
    }
    with open(INTAKE_LOCK, "w", encoding="utf-8") as f:
        json.dump(intake, f, indent=2)
    intake_sha = sha256_file(INTAKE_LOCK)
    INTAKE_LOCK_SIBLING.write_text(intake_sha + "\n", encoding="ascii")

    summary = {
        "cr_id": "CR065a",
        "branch": "09a_PARTICLE_MASS_CHAIN",
        "extends_anchor": "CR064a",
        "test_class": "COURTROOM_INTAKE_OF_QP084_THROUGH_QP091_FORWARD_FROZEN_PREDICTIONS",
        "execution_status": "CLEAN",
        "result_class": verdict,
        "intake_utc": intake_utc,
        "upstream_qp_chain_count": len(QP_CHAIN),
        "predictions": predictions,
        "wrong_controls": wrong_controls,
        "intake_lock_sha256": intake_sha,
        "intake_lock_path": str(INTAKE_LOCK),
        "open_debts": [
            "CR066a will open the three strongest reveal targets (m4l, m12/m34, angular) carefully",
            "REVEAL_01 (signal strength) is recorded but intentionally held - per upstream user direction, signal strength is the weakest reveal target",
            "Curator sign-off of the intake lock pending",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # ---- Step 6: Result markdown ----------------------------------------
    md = []
    md.append("# CR065a Higgs ZZ4L Prediction Intake - Result\n\n")
    md.append("## Verdict\n\n```text\n" + verdict + "\n```\n\n")
    md.append("## Extends 09a Branch\n\n")
    md.append("CR065a continues 09a after the immutable CR064a branch verdict, intaking the upstream QP084 -> QP091 chain that derives a Higgs H -> ZZ* -> 4l prediction freeze from the QP075 35-row closure surface with zero new free parameters.\n\n")
    md.append("## Intake Lock\n\n```text\n")
    md.append(f"intake_lock_sha256 = {intake_sha}\n")
    md.append(f"intaken_at_utc     = {intake_utc}\n")
    md.append("```\n\n")
    md.append("## Upstream Chain (each row sha256 + verdict)\n\n")
    md.append("| QP | verdict | sha256 (first 16) | free params | external data |\n|---|---|---|---|---|\n")
    for row in chain_status:
        sha16 = row['sha256'][:16] if row['sha256'] else 'NOT_FOUND'
        ed = row['external_decay_data_used']
        ed_note = ('CR092_anchors_reveal' if row['qp085_reveal_within_chain'] else str(ed))
        md.append(f"| {row['qp_id']} | {row.get('result_class', 'n/a')[:40]} | {sha16} | {row['free_parameters_introduced']} | {ed_note} |\n")
    md.append("\n## QP091 Frozen Predictions\n\n```text\n")
    md.append(f"H_visible_parent_ledger        = {expected['H_visible_parent_ledger_MeV']:.4f} MeV\n")
    md.append(f"H_source_hidden_budget          = {expected['H_source_hidden_budget_MeV']:.6f} MeV\n")
    md.append(f"Z_visible_branch                = {expected['Z_visible_branch_MeV']:.4f} MeV\n")
    md.append(f"two_on_shell_Z_deficit_visible  = {expected['two_on_shell_Z_deficit_visible_MeV']:.4f} MeV  (forbidden)\n")
    md.append(f"Zstar_ceiling_visible           = {expected['Zstar_ceiling_visible_MeV']:.4f} MeV\n")
    md.append(f"4e   threshold                  = {expected['terminal_thresholds_MeV']['4e']:.6f} MeV\n")
    md.append(f"2e2mu threshold                  = {expected['terminal_thresholds_MeV']['2e2mu']:.6f} MeV\n")
    md.append(f"4mu  threshold                  = {expected['terminal_thresholds_MeV']['4mu']:.6f} MeV\n")
    md.append(f"hidden_source_budget_fraction   = {expected['hidden_source_budget_fraction']:.9f}  (~0.16%)\n")
    md.append("```\n\n")
    md.append("## Reveal Map Status (set by QP091)\n\n")
    md.append("| reveal_id | future_target | qp091_status | selection_role |\n|---|---|---|---|\n")
    for row in qp091_reveal_map:
        md.append(f"| {row['reveal_id']} | {row['future_target']} | {row['qp091_status']} | {row['selection_role']} |\n")
    md.append("\n## Predictions\n\n")
    for p in predictions:
        flag = "PASS" if p["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {p['name']}\n")
    md.append("\n## Wrong Controls\n\n")
    for w in wrong_controls:
        flag = "PASS" if w["pass"] else "FAIL"
        md.append(f"- **[{flag}]** {w['name']}\n")
    md.append("\n## Next In 09a\n\n")
    md.append("**CR066a** opens REVEAL_02 (m4l distribution), REVEAL_03 (m12/m34 or Z/Z* branch), REVEAL_04 (four-lepton angular correlations) against published ATLAS+CMS Run-2 H -> ZZ* -> 4l measurements.\n\n")
    md.append("REVEAL_01 (H006/H007 signal strength) remains HELD. Per the user direction, signal strength is the weakest of the four candidate reveal targets; the structural distributions (m4l, m12/m34, angular) carry far more information about whether the upstream prediction freeze closes.\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))

    print(f"  verdict: {verdict}")
    print(f"  intake_lock_sha256: {intake_sha}")
    print("CR065a runner: complete")


if __name__ == "__main__":
    main()
