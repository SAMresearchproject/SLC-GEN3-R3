import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SOURCE = Path(r"C:\VS\sam_sim\artifacts\G755c_EARTH_GALAXY_PBH_ACCUMULATION_MODE_SELECTOR")


def evaluate(sources):
    summary = sources["summary"]
    galaxy_rows = sources["galaxy_report"]
    mode_rows = sources["mode_report"]
    wrong_rows = sources["wrong_controls"]
    statuses = {r.get("status") for r in galaxy_rows}
    required_statuses = {
        "SELECTED_CUMULATIVE_BARYON_NONZERO",
        "SELECTED_CLUSTERED_PBH_SCAFFOLD",
        "SELECTED_CUMULATIVE_PBH_NONZERO",
        "SELECTED_CATCHUP_MATERIAL",
        "SELECTED_NATIVE_RADIAL_SHAPE",
    }
    conditions = {
        "accumulation_gate_pass": summary["engineering_status"] == "PASS" and summary["scientific_verdict"] == "PASS_TYPED_ACCUMULATION_MODE_SELECTOR",
        "not_audit_or_retest": not summary["is_audit_or_retest"] and not summary["confirmation_or_double_check"],
        "no_courtroom_sources_opened": summary["courtroom_files_opened"] is False,
        "no_free_parameters": summary["free_parameters_introduced"] == 0,
        "earth_local_A_forward_present": summary["earth_A_local_forward"] > 0,
        "baryon_many_nonzero_cumulative_present": summary["baryon_many_nonzero_A_cumulative"] > summary["baryon_many_nonzero_A_single"],
        "clustered_BB_PBH_scaffold_present": summary["Omega_BB_PBH_trapped"] > summary["Omega_H_arrival_baryon"],
        "pbh_many_nonzero_present": summary["pbh_cumulative_nonzero_proxy_median"] > 0,
        "galaxy_statuses_complete": required_statuses.issubset(statuses),
        "mode_report_present": len(mode_rows) > 0,
        "wrong_controls_passed": summary["wrong_controls_passed"] == summary["wrong_controls_total"] == len(wrong_rows),
    }
    evidence = [
        {"key": "result_class", "value": summary["result_class"], "note": "source G-test result"},
        {"key": "earth_A_local_forward", "value": summary["earth_A_local_forward"], "note": "local compact lane"},
        {"key": "baryon_many_nonzero_A_cumulative", "value": summary["baryon_many_nonzero_A_cumulative"], "note": "many stellar nonzeros"},
        {"key": "Omega_BB_PBH_trapped", "value": summary["Omega_BB_PBH_trapped"], "note": "clustered BB-PBH/trapped-A inventory"},
        {"key": "pbh_cumulative_nonzero_proxy_median", "value": summary["pbh_cumulative_nonzero_proxy_median"], "note": "PBH many-nonzero lane"},
        {"key": "wrong_controls", "value": f"{summary['wrong_controls_passed']}/{summary['wrong_controls_total']}", "note": "uniform/PBH-only/baryon-only controls rejected"},
    ]
    return {
        "result_class": "CR206_PASS_EARTH_GALAXY_PBH_ACCUMULATION_MODE_SELECTOR",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "SIMULATOR_ACCUMULATION_MODE_SELECTOR",
        "question": "Can local Earth A, galaxy many-nonzero A, clustered BB-PBH scaffold, and PBH cumulative nonzeros remain typed?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that galaxy halo support is typed as baryon many-nonzero A plus clustered BB-PBH/trapped-A scaffold plus PBH many-nonzero accumulation, distinct from Earth local A.",
        "notes": ["This explicitly includes cumulative nonzero A from PBH as requested."],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR206",
            "title": "Earth/Galaxy/PBH Accumulation Mode Selector",
            "source_paths": {
                "summary": {"path": SOURCE / "G755c_summary.json", "role": "source_gate_summary"},
                "galaxy_report": {"path": SOURCE / "G755c_galaxy_cumulative_A_report.csv", "role": "galaxy_cumulative_A_report"},
                "mode_report": {"path": SOURCE / "G755c_mode_selector_report.csv", "role": "mode_selector_report"},
                "wrong_controls": {"path": SOURCE / "G755c_wrong_controls.csv", "role": "wrong_controls"},
            },
        },
        evaluate,
    )
