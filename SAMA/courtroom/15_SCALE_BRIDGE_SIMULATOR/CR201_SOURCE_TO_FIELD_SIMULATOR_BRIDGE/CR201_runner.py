import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G750c_SOURCE_TO_FIELD_SIMULATOR_BRIDGE")


def evaluate(sources):
    summary = sources["summary"]
    qa_rows = sources["qa_ledger"]
    particle_rows = sources["particle_ledger"]
    wrong_rows = sources["wrong_controls"]

    qa_rule_rows = [r for r in qa_rows if r.get("rule") == "q_A = m * (1 + r_bounce)"]
    conditions = {
        "source_gate_pass": summary["engineering_status"] == "PASS" and summary["scientific_verdict"] == "PASS",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "particle_rows_imported": summary["particle_rows_imported"] == 26 and len(particle_rows) >= 26,
        "qa_source_rows_emitted": summary["source_rows_emitted"] == 7 and len(qa_rows) == 7,
        "qa_source_formula_exact": summary["max_source_formula_relative_error"] == 0.0 and len(qa_rule_rows) == len(qa_rows),
        "source_bridge_within_tolerance": summary["ratio_spread_fractional"] <= summary["source_bridge_tolerance"],
        "composite_binding_within_tolerance": summary["max_composite_relative_error"] <= summary["composite_tolerance"],
        "wrong_controls_passed": summary["wrong_controls_passed"] == summary["wrong_controls_total"] == len(wrong_rows),
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "particle_rows_imported", "value": summary["particle_rows_imported"], "note": "QP075 particle rows imported by G750c"},
        {"key": "source_rows_emitted", "value": summary["source_rows_emitted"], "note": "active q_A source rows"},
        {"key": "ratio_spread_fractional", "value": summary["ratio_spread_fractional"], "note": "must be within declared tolerance"},
        {"key": "wrong_controls", "value": f"{summary['wrong_controls_passed']}/{summary['wrong_controls_total']}", "note": "all source-strength controls labeled"},
    ]
    return {
        "result_class": "CR201_PASS_SOURCE_TO_FIELD_SIMULATOR_BRIDGE",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "SIMULATOR_SOURCE_TO_FIELD_BRIDGE",
        "question": "Can the source ledger feed field inventory without changing q_A grammar or adding a parameter?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that q_A = m * (1 + r_bounce) can bridge particle source rows into field inventory rows with zero new parameters and with the declared wrong controls rejected.",
        "notes": ["Courtroom export reads frozen G750c artifacts and does not overwrite the G750c verdict."],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR201",
            "title": "Source-To-Field Simulator Bridge",
            "source_paths": {
                "summary": {"path": SOURCE / "G750c_summary.json", "role": "source_gate_summary"},
                "qa_ledger": {"path": SOURCE / "G750c_qA_source_ledger.csv", "role": "qA_source_rows"},
                "particle_ledger": {"path": SOURCE / "G750c_particle_route_ledger.csv", "role": "particle_route_rows"},
                "wrong_controls": {"path": SOURCE / "G750c_wrong_controls.csv", "role": "wrong_controls"},
            },
        },
        evaluate,
    )
