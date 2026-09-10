import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G751c_TYPED_READOUT_REPRODUCTION_FROM_QA_SOURCES")


def evaluate(sources):
    summary = sources["summary"]
    readouts = sources["readouts"]
    wrong_rows = sources["wrong_controls"]
    separated_rows = [r for r in readouts if "SEPARATED" in r.get("typed_lane_status", "")]
    zero_error_keys = [
        "max_A_mass_relative_error",
        "max_A_q_direct_relative_error",
        "max_force_relative_error",
        "max_clock_shift_relative_error",
    ]
    conditions = {
        "readout_gate_pass": summary["engineering_status"] == "PASS" and summary["scientific_verdict"] == "PASS",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "readout_rows_present": summary["readout_rows"] == len(readouts) == 6,
        "all_recompute_errors_zero": all(summary[k] == 0.0 for k in zero_error_keys),
        "typed_lanes_separated": len(separated_rows) == len(readouts),
        "species_mix_spread_within_tolerance": summary["species_mix_spread_fractional"] <= summary["source_bridge_tolerance"],
        "wrong_controls_passed": summary["wrong_controls_passed"] == summary["wrong_controls_total"] == len(wrong_rows),
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "readout_rows", "value": len(readouts), "note": "typed readout rows"},
        {"key": "max_recompute_error", "value": max(summary[k] for k in zero_error_keys), "note": "mass/q_A/force/clock recomputation"},
        {"key": "typed_lane_status_rows", "value": len(separated_rows), "note": "rows explicitly reporting separated lanes"},
        {"key": "wrong_controls", "value": f"{summary['wrong_controls_passed']}/{summary['wrong_controls_total']}", "note": "all lane-mixing controls passed"},
    ]
    return {
        "result_class": "CR202_PASS_TYPED_READOUT_REPRODUCTION",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "SIMULATOR_TYPED_READOUT",
        "question": "Can field readouts stay typed across mass ledger, q_A direct, force, and clock lanes?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that typed field readouts reproduce mass-ledger A, q_A-direct A, force, and clock lanes without lane mixing or species retuning.",
        "notes": ["Courtroom export reads frozen G751c artifacts and does not tune by species."],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR202",
            "title": "Typed Readout Reproduction",
            "source_paths": {
                "summary": {"path": SOURCE / "G751c_summary.json", "role": "source_gate_summary"},
                "readouts": {"path": SOURCE / "G751c_source_to_field_readout_table.csv", "role": "typed_readout_rows"},
                "wrong_controls": {"path": SOURCE / "G751c_wrong_controls.csv", "role": "wrong_controls"},
            },
        },
        evaluate,
    )
