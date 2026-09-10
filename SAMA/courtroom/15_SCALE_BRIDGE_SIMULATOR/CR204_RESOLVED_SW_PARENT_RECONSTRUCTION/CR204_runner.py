import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G753c_RESOLVED_SW_PARENT_RECONSTRUCTION_TEST")


def evaluate(sources):
    summary = sources["summary"]
    rows = sources["reconstruction_rows"]
    wrong_rows = sources["wrong_controls"]
    closed_rows = [r for r in rows if r.get("status", "").startswith("CLOSED")]
    partial_rows = [r for r in rows if r.get("status", "").startswith("PARTIAL")]
    zero_residual_closed = all(abs(float(r["residual_mev"])) <= 1e-12 for r in closed_rows)
    conditions = {
        "engineering_gate_pass": summary["engineering_status"] == "PASS",
        "scientific_boundary_expected": summary["scientific_verdict"] == "BOUNDARY_STRUCTURAL_RECONSTRUCTION",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "hidden_budget_separate": summary["hidden_source_minus_visible_budget_MeV"] > 0,
        "multiple_scalar_channels_same_parent": summary["scalar_closed_channels"] >= 2,
        "partial_channels_do_not_fake_closure": summary["partial_channels"] >= 2 and len(partial_rows) >= 2,
        "closed_rows_zero_residual": zero_residual_closed,
        "wrong_controls_passed": summary["wrong_controls_passed"] == summary["wrong_controls_total"] == len(wrong_rows),
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "visible_parent_MeV", "value": summary["parent_visible_MeV"], "note": "visible invariant parent"},
        {"key": "hidden_source_budget_MeV", "value": summary["parent_source_hidden_budget_MeV"], "note": "tracked separately"},
        {"key": "closed_rows", "value": len(closed_rows), "note": "zero-residual visible closures"},
        {"key": "wrong_controls", "value": f"{summary['wrong_controls_passed']}/{summary['wrong_controls_total']}", "note": "full-SW/direct-hidden controls rejected"},
    ]
    return {
        "result_class": "CR204_BOUNDARY_RESOLVED_SW_PARENT_RECONSTRUCTION",
        "execution_status": "CLEAN",
        "scientific_verdict": "BOUNDARY",
        "triage_bin": "C",
        "claim_tier": "SIMULATOR_RESOLVED_SW_PARENT_RECONSTRUCTION",
        "question": "Can resolved daughter-write closure reconstruct a parent while keeping full SW/source budget hidden?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that visible resolved-SW parent closure is reconstructed from daughter-write lanes while hidden/source bounce budget remains separate from visible invariant mass.",
        "notes": ["Boundary is preserved intentionally: this is structural reconstruction, not standalone external discovery."],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR204",
            "title": "Resolved-SW Parent Reconstruction",
            "source_paths": {
                "summary": {"path": SOURCE / "G753c_summary.json", "role": "source_gate_summary"},
                "reconstruction_rows": {"path": SOURCE / "G753c_resolved_sw_parent_reconstruction.csv", "role": "resolved_sw_rows"},
                "wrong_controls": {"path": SOURCE / "G753c_wrong_controls.csv", "role": "wrong_controls"},
            },
        },
        evaluate,
    )
