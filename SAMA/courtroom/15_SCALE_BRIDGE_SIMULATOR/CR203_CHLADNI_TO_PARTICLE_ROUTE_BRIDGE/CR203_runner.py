import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G752c_CHLADNI_TO_PARTICLE_ROUTE_CLOSURE_BRIDGE")


def evaluate(sources):
    summary = sources["summary"]
    boundary_rows = sources["boundary_records"]
    wrong_rows = sources["wrong_controls"]
    qp091_rows = [r for r in boundary_rows if "qp091" in r.get("live_surface", "").lower()]
    promoted_particles = [r for r in boundary_rows if r.get("promotion_status") == "PROMOTED_PARTICLE"]
    route_candidate_rows = [r for r in boundary_rows if r.get("promotion_status") == "ROUTE_CANDIDATE_ONLY"]
    conditions = {
        "chladni_gate_pass": summary["engineering_status"] == "PASS" and summary["scientific_verdict"] == "PASS",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "qp091_live_surface": summary["qp091_result_class"] == "PASS_QP091_HIGGS_ZZ4L_OBSERVABLE_PREDICTION_FROZEN",
        "no_direct_qp075_live_inputs": summary["direct_qp075_live_inputs"] == 0,
        "lab_plate_all_pass": summary["lab_plate_all_pass"] is True,
        "boundary_records_present": summary["boundary_records"] == len(boundary_rows) == 12,
        "all_records_link_qp091": len(qp091_rows) == len(boundary_rows),
        "no_particle_promotion": len(promoted_particles) == 0,
        "route_candidate_rows_scoped": len(route_candidate_rows) == summary["boundary_selector_only_rows"],
        "wrong_controls_rejected": summary["wrong_controls_rejected"] == summary["wrong_controls_total"] == len(wrong_rows),
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "live_surface", "value": summary["live_surface"], "note": "fresh QP091 surface"},
        {"key": "lab_plate_campaign", "value": summary["lab_plate_campaign"], "note": "lab plate path"},
        {"key": "direct_qp075_live_inputs", "value": summary["direct_qp075_live_inputs"], "note": "stale direct inputs rejected"},
        {"key": "wrong_controls", "value": f"{summary['wrong_controls_rejected']}/{summary['wrong_controls_total']}", "note": "all Chladni controls rejected"},
    ]
    return {
        "result_class": "CR203_PASS_CHLADNI_TO_PARTICLE_ROUTE_BRIDGE_QP091_FRESH",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "SIMULATOR_CHLADNI_ROUTE_BRIDGE",
        "question": "Can the Chladni plate support boundary routes without becoming a stale particle selector?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that the Chladni bridge uses the QP091 live surface and lab plate only as boundary-route support, not stale QP075 or toy plate direct promotion.",
        "notes": ["The route bridge stays scoped to boundary/mode support."],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR203",
            "title": "Chladni-To-Particle Route Bridge",
            "source_paths": {
                "summary": {"path": SOURCE / "G752c_summary.json", "role": "source_gate_summary"},
                "boundary_records": {"path": SOURCE / "G752c_boundary_mode_records.csv", "role": "boundary_mode_records"},
                "wrong_controls": {"path": SOURCE / "G752c_wrong_controls.csv", "role": "wrong_controls"},
            },
        },
        evaluate,
    )
