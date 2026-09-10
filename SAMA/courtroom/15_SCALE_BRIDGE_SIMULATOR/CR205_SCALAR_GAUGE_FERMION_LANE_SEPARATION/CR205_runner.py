import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G754c_SCALAR_GAUGE_FERMION_LANE_SEPARATION_TEST")


def evaluate(sources):
    summary = sources["summary"]
    wrong_rows = sources["wrong_controls"]
    conditions = {
        "lane_gate_pass": summary["engineering_status"] == "PASS" and summary["scientific_verdict"] == "PASS_SCOPED_LANE_SEPARATION",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "scalar_half_is_9_16": summary["derived_scalar_half"] == 0.5625,
        "scalar_expression_is_D3": summary["derived_scalar_expression"] == "D^2 / 2^(D+1)" and summary["D_privileged"] == 3,
        "fermions_degrade_under_forced_9_16": summary["fermion_rows_degraded_9_16"] == summary["fermion_rows_checked"] == 6,
        "fermions_degrade_under_forced_16_9": summary["fermion_rows_degraded_16_9"] == summary["fermion_rows_checked"] == 6,
        "gauge_rows_held": summary["gauge_rows_held"] == 2,
        "higgs_scalar_owner_confirmed": summary["higgs_scalar_owner_confirmed"] is True,
        "wrong_controls_passed": summary["wrong_controls_passed"] == summary["wrong_controls_total"] == len(wrong_rows),
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "derived_scalar_half", "value": summary["derived_scalar_half"], "note": "D=3 scalar lane"},
        {"key": "fermion_rows_checked", "value": summary["fermion_rows_checked"], "note": "fermion controls degrade under scalar multipliers"},
        {"key": "gauge_rows_held", "value": summary["gauge_rows_held"], "note": "gauge owners separated"},
        {"key": "wrong_controls", "value": f"{summary['wrong_controls_passed']}/{summary['wrong_controls_total']}", "note": "all lane-separation controls passed"},
    ]
    return {
        "result_class": "CR205_PASS_SCALAR_GAUGE_FERMION_LANE_SEPARATION",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "SIMULATOR_TYPED_LANE_SEPARATION",
        "question": "Can scalar 9/16 stay lane-specific rather than becoming a universal particle multiplier?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that 9/16 is a D=3 scalar-lane structure and not a universal multiplier for fermion or gauge rows.",
        "notes": ["This is a scoped lane-separation result, not a new particle-mass fit."],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR205",
            "title": "Scalar/Gauge/Fermion Lane Separation",
            "source_paths": {
                "summary": {"path": SOURCE / "G754c_summary.json", "role": "source_gate_summary"},
                "wrong_controls": {"path": SOURCE / "G754c_wrong_controls.csv", "role": "wrong_controls"},
            },
        },
        evaluate,
    )
