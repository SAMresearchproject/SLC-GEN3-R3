import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G757c_FULL_SCALE_BRIDGE_WRONG_CONTROLS_ZIPPER")


def evaluate(sources):
    summary = sources["summary"]
    matrix = sources["control_matrix"]
    claim = sources["strongest_claim"]
    negatives = sources["honest_negatives"]
    family_counts = summary["family_counts"]
    families_complete = all(v["passed"] == v["total"] for v in family_counts.values())
    fired_count = sum(1 for r in matrix if str(r.get("control_fired_or_degraded", "")).lower() == "true")
    diagnostic_count = sum(1 for r in matrix if str(r.get("honest_diagnostic", "")).lower() == "true")
    conditions = {
        "zipper_gate_pass": summary["engineering_status"] == "PASS" and summary["scientific_verdict"] == "PASS_WRONG_CONTROL_ZIPPER",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_courtroom_export_performed_upstream": summary["courtroom_files_opened"] is False,
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "all_controls_passed": summary["controls_passed"] == summary["total_controls"] == len(matrix) == 43,
        "controls_fire_or_degrade": summary["controls_fired_or_degraded"] == fired_count == 42,
        "honest_diagnostic_preserved": summary["honest_diagnostics"] == diagnostic_count == 1,
        "failed_controls_zero": summary["failed_controls"] == 0,
        "families_complete": families_complete,
        "claim_file_contains_scale_bridge": "Typed route support" in claim,
        "honest_negatives_file_present": len(negatives.strip()) > 0,
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "total_controls", "value": summary["total_controls"], "note": "wrong-control zipper size"},
        {"key": "controls_passed", "value": summary["controls_passed"], "note": "all controls passed"},
        {"key": "controls_fired_or_degraded", "value": summary["controls_fired_or_degraded"], "note": "controls actually broke/degraded the wrong route"},
        {"key": "honest_diagnostics", "value": summary["honest_diagnostics"], "note": "diagnostic retained, not hidden"},
        {"key": "failed_controls", "value": summary["failed_controls"], "note": "must be zero"},
    ]
    return {
        "result_class": "CR208_PASS_SCALE_BRIDGE_SIMULATOR_WRONG_CONTROL_ZIPPER",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "SIMULATOR_BRANCH_VERDICT",
        "question": "Does the scale bridge survive the full wrong-control zipper without overwriting individual gate verdicts?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that the scale bridge survived a full wrong-control zipper with 43/43 controls passed, no failed controls, and individual gate verdicts preserved.",
        "notes": [
            "CR204 and CR207 remain BOUNDARY by design while CR208 records the branch-level wrong-control PASS.",
            "The branch strongest claim is imported from G757c and hash-anchored here.",
        ],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR208",
            "title": "Wrong-Control Zipper And Branch Verdict",
            "source_paths": {
                "summary": {"path": SOURCE / "G757c_summary.json", "role": "source_gate_summary"},
                "control_matrix": {"path": SOURCE / "G757c_control_fire_matrix.csv", "role": "full_wrong_control_matrix"},
                "strongest_claim": {"path": SOURCE / "G757c_strongest_surviving_claim.md", "role": "strongest_surviving_claim"},
                "honest_negatives": {"path": SOURCE / "G757c_honest_negatives.md", "role": "honest_negatives"},
            },
        },
        evaluate,
    )
