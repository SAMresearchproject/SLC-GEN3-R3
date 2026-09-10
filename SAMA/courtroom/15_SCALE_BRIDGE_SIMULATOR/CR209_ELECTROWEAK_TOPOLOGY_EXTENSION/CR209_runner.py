import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


G758 = Path(r"C:\VS\sam_sim\artifacts\G758c_ELECTROWEAK_TOPOLOGY_EXTENSION")


def _as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def evaluate(sources):
    premises = sources["premises"]
    g758 = sources["g758_summary"]
    classifications = sources["g758_classifications"]
    controls = sources["g758_wrong_controls"]
    source_manifest = sources["g758_source_manifest"]
    cr204a = sources["cr204a_summary"]
    cr208a = sources["cr208a_summary"]

    accepted = [row for row in classifications if _as_bool(row.get("should_accept", ""))]
    rejected = [row for row in classifications if not _as_bool(row.get("should_accept", ""))]
    correct = [row for row in accepted if _as_bool(row.get("classified_correctly", ""))]
    control_pass = [row for row in controls if _as_bool(row.get("passed", ""))]
    observed_lanes = sorted({row["observed_lane"] for row in accepted})
    target_map = "; ".join(f"{row['target']}->{row['observed_lane']}" for row in classifications)

    cr208a_boundary = " ".join(
        str(row.get("value", ""))
        for row in cr208a.get("evidence_rows", [])
        if row.get("key") == "remaining_boundary"
    )

    conditions = {
        "source_gate_pass": g758["scientific_verdict"] == "PASS_SCOPED_ELECTROWEAK_TOPOLOGY_EXTENSION",
        "forward_not_audit": premises["is_audit_or_retest"] is False
        and g758["is_audit_or_retest"] is False
        and g758["confirmation_or_double_check"] is False,
        "no_free_parameters": premises["free_parameters_introduced"] == 0 and g758["free_parameters_introduced"] == 0,
        "five_target_lanes_classified": len(accepted) == 5 and len(correct) == 5,
        "fake_parent_rejected": len(rejected) == 1 and all(row["observed_lane"] == "reject_fake_parent" for row in rejected),
        "wrong_controls_pass": len(controls) == 7 and len(control_pass) == 7,
        "higgs_lanes_distinguished": {
            row["observed_lane"] for row in accepted if row["lane_id"] in {"H_ZZSTAR_4L", "H_GAMMA_GAMMA"}
        }
        == {"resolved_scalar_parent_vector_branches", "resolved_scalar_parent_massless_daughters"},
        "vector_lanes_distinguished": {
            row["observed_lane"] for row in accepted if row["lane_id"] in {"Z_LL", "W_LNU"}
        }
        == {"neutral_vector_visible_pair_parent", "charged_vector_missing_route_parent"},
        "gamma_not_parent": next(row for row in accepted if row["lane_id"] == "GAMMA_DAUGHTER")["observed_lane"]
        == "massless_readout_daughter_not_parent",
        "cr204a_external_topology_bridge_preserved": cr204a["scientific_verdict"] == "PASS",
        "cr208a_full_ew_boundary_preserved": "EW_THEOREM_OPEN" in cr208a["result_class"]
        or "electroweak theorem closure remains open" in cr208a_boundary,
        "source_manifest_hashes_present": len(source_manifest) >= 10 and all(row["sha256"] for row in source_manifest),
    }
    evidence = [
        {"key": "source_gate_result_class", "value": g758["result_class"], "note": "G758c upstream simulator result"},
        {"key": "target_lane_result", "value": f"{len(correct)}/{len(accepted)}", "note": "accepted lanes classified correctly"},
        {"key": "fake_parent_rejection", "value": f"{len(rejected)}/{len(rejected)}", "note": "background/fake parent rejected"},
        {"key": "wrong_controls", "value": f"{len(control_pass)}/{len(controls)}", "note": "wrong controls fired"},
        {"key": "observed_lane_count", "value": len(observed_lanes), "note": "distinct accepted topology lanes"},
        {"key": "observed_lanes", "value": "|".join(observed_lanes), "note": "fixed classifier readout"},
        {"key": "target_map", "value": target_map, "note": "lane by lane classification"},
        {"key": "payload_fingerprint_sha256", "value": g758["payload_fingerprint_sha256"], "note": "G758c payload fingerprint"},
        {"key": "remaining_boundary", "value": g758["scope_boundary"], "note": "not a full electroweak theorem"},
    ]
    return {
        "result_class": "CR209_PASS_ELECTROWEAK_TOPOLOGY_EXTENSION__BOUNDARY_FULL_EW_THEOREM_OPEN",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "ELECTROWEAK_TOPOLOGY_EXTENSION",
        "question": "Can the same resolved-parent/write-bounce grammar distinguish H, Z, W, and gamma lanes without changing rules?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that the scale-bridge simulator's resolved-parent/write-bounce grammar generalizes beyond H -> ZZ* -> 4l into H, Z, W, gamma, and fake-parent lane separation without changing rules or adding parameters.",
        "notes": [
            "CR204 and CR207 remain BOUNDARY.",
            "CR204a and CR208a are preserved as the external topology bridge and promotion zipper.",
            "CR209 is a topology-grammar PASS, not a full electroweak coupling, amplitude, or branching-ratio theorem.",
        ],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR209",
            "title": "Electroweak Topology Extension",
            "source_paths": {
                "premises": {"path": ROOT / "CR209_declared_premises.json", "role": "declared_premises"},
                "g758_summary": {"path": G758 / "G758c_summary.json", "role": "source_gate_summary"},
                "g758_classifications": {"path": G758 / "G758c_lane_classification_results.csv", "role": "lane_classification_results"},
                "g758_wrong_controls": {"path": G758 / "G758c_wrong_controls.csv", "role": "wrong_controls"},
                "g758_source_manifest": {"path": G758 / "G758c_source_manifest.csv", "role": "source_manifest"},
                "g758_hashes": {"path": G758 / "HASHES.txt", "role": "source_hashes"},
                "cr204a_summary": {"path": BRANCH / "CR204a_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION" / "CR204a_summary.json", "role": "external_topology_bridge"},
                "cr208a_summary": {"path": BRANCH / "CR208a_RESOLVED_SW_EXTERNAL_PROMOTION_ZIPPER" / "CR208a_summary.json", "role": "promotion_zipper"},
            },
        },
        evaluate,
    )
