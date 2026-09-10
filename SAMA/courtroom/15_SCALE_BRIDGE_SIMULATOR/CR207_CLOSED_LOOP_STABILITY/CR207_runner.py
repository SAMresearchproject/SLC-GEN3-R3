import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G756c_SIMULATOR_CLOSED_LOOP_STABILITY_TEST")


def evaluate(sources):
    summary = sources["summary"]
    type_report = sources["type_report"]
    trace_hashes = summary.get("trace_hashes", [])
    conditions = {
        "engineering_gate_pass": summary["engineering_status"] == "PASS",
        "scientific_boundary_expected": summary["scientific_verdict"] == "BOUNDARY_INTERNAL_CLOSED_LOOP_STABILITY",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_courtroom_sources_opened": summary["courtroom_files_opened"] is False,
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "unexpected_type_violations_zero": summary["unexpected_type_violations"] == 0,
        "expected_controls_fire": summary["expected_control_breaks"] == 3,
        "all_run_traces_hashed": len(trace_hashes) == 5 and all(t.get("sha256") for t in trace_hashes),
        "type_report_records_zero_unexpected": len(type_report.get("unexpected_type_violations", [])) == 0
        and type_report.get("type_violation_status") == "PASS_NO_UNEXPECTED_TYPE_VIOLATIONS",
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "unexpected_type_violations", "value": summary["unexpected_type_violations"], "note": "closed-loop replay"},
        {"key": "expected_control_breaks", "value": summary["expected_control_breaks"], "note": "controls fired by design"},
        {"key": "trace_hash_count", "value": len(trace_hashes), "note": "all run traces hashed"},
        {"key": "run_steps", "value": f"{summary['run_A_steps']},{summary['run_B_steps']},{summary['run_C_steps']},{summary['run_D_steps']},{summary['run_E_steps']}", "note": "A through E loop sizes"},
    ]
    return {
        "result_class": "CR207_BOUNDARY_CLOSED_LOOP_STABILITY",
        "execution_status": "CLEAN",
        "scientific_verdict": "BOUNDARY",
        "triage_bin": "C",
        "claim_tier": "SIMULATOR_CLOSED_LOOP_STABILITY",
        "question": "Can the simulator replay the scale bridge without unexpected type violations?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that the scale bridge can be replayed as a closed loop with all run traces hashed and no unexpected type violations.",
        "notes": ["Boundary is preserved: closed-loop stability is internal simulator discipline, not standalone external validation."],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR207",
            "title": "Closed-Loop Stability",
            "source_paths": {
                "summary": {"path": SOURCE / "G756c_summary.json", "role": "source_gate_summary"},
                "type_report": {"path": SOURCE / "G756c_type_violation_report.json", "role": "type_violation_report"},
            },
        },
        evaluate,
    )
