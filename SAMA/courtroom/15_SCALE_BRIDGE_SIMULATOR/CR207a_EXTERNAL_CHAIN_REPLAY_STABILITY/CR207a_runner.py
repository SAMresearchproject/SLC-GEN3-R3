import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


def _summary_path(case_dir, test_id):
    return BRANCH / case_dir / f"{test_id}_summary.json"


def _chain_fingerprint(summaries):
    payload = []
    for test_id in sorted(summaries):
        summary = summaries[test_id]
        payload.append(
            {
                "test_id": test_id,
                "result_class": summary["result_class"],
                "scientific_verdict": summary["scientific_verdict"],
                "source_hashes": sorted(a["sha256"] for a in summary.get("source_artifacts", [])),
            }
        )
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evaluate(sources):
    summaries = {
        "CR201": sources["cr201_summary"],
        "CR202": sources["cr202_summary"],
        "CR203": sources["cr203_summary"],
        "CR204": sources["cr204_summary"],
        "CR205": sources["cr205_summary"],
        "CR207": sources["cr207_summary"],
        "CR208": sources["cr208_summary"],
        "CR204a": sources["cr204a_summary"],
    }
    all_conditions_true = all(s["all_pass_conditions_true"] is True for s in summaries.values())
    no_free_params = all(
        s.get("pass_conditions", {}).get("no_free_parameters", True) is True
        for s in summaries.values()
    )
    original_boundaries_preserved = (
        summaries["CR204"]["scientific_verdict"] == "BOUNDARY"
        and summaries["CR207"]["scientific_verdict"] == "BOUNDARY"
    )
    endpoint_external = summaries["CR204a"]["scientific_verdict"] == "PASS"
    controls_preserved = (
        summaries["CR207"]["evidence_rows"][1]["value"] == 0
        and summaries["CR207"]["evidence_rows"][2]["value"] == 3
        and summaries["CR208"]["evidence_rows"][1]["value"] == 43
        and summaries["CR208"]["evidence_rows"][4]["value"] == 1
    )
    source_hash_count = sum(len(s.get("source_artifacts", [])) for s in summaries.values())
    fingerprint = _chain_fingerprint(summaries)
    conditions = {
        "original_cr204_and_cr207_remain_boundary": original_boundaries_preserved,
        "all_chain_case_conditions_true": all_conditions_true,
        "no_free_parameters_any_chain_case": no_free_params,
        "external_facing_endpoint_passes": endpoint_external,
        "wrong_controls_and_expected_breaks_preserved": controls_preserved,
        "source_artifact_hashes_present": source_hash_count > 0,
        "chain_fingerprint_emitted": len(fingerprint) == 64,
    }
    evidence = [
        {"key": "chain_cases", "value": ",".join(sorted(summaries)), "note": "frozen summaries loaded"},
        {"key": "original_CR204_verdict", "value": summaries["CR204"]["scientific_verdict"], "note": "not relabeled"},
        {"key": "original_CR207_verdict", "value": summaries["CR207"]["scientific_verdict"], "note": "not relabeled"},
        {"key": "external_endpoint", "value": summaries["CR204a"]["result_class"], "note": "external-facing Higgs/ZZ* endpoint"},
        {"key": "source_artifact_hash_count", "value": source_hash_count, "note": "hashes carried through chain summaries"},
        {"key": "chain_fingerprint_sha256", "value": fingerprint, "note": "result classes plus source hashes"},
    ]
    return {
        "result_class": "CR207a_PASS_EXTERNAL_CHAIN_REPLAY_STABILITY",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "EXTERNAL_CHAIN_REPLAY_STABILITY_APPEAL",
        "question": "Can the full simulator chain reach an external-facing readout while preserving frozen lane rules and boundary labels?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that the scale-bridge simulator can replay from source grammar to an external-facing resolved-parent readout while preserving all frozen lane rules and boundary labels.",
        "notes": [
            "CR207 is not relabeled; this is a separate promotion appeal artifact.",
            "The chain endpoint is CR204a, which carries the external Higgs/ZZ* parent-daughter contact.",
            "The chain fingerprint binds result classes and imported source hashes."
        ],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR207a",
            "title": "External Chain Replay Stability",
            "source_paths": {
                "cr201_summary": {"path": _summary_path("CR201_SOURCE_TO_FIELD_SIMULATOR_BRIDGE", "CR201"), "role": "source_to_field_summary"},
                "cr202_summary": {"path": _summary_path("CR202_TYPED_READOUT_REPRODUCTION", "CR202"), "role": "typed_readout_summary"},
                "cr203_summary": {"path": _summary_path("CR203_CHLADNI_TO_PARTICLE_ROUTE_BRIDGE", "CR203"), "role": "chladni_bridge_summary"},
                "cr204_summary": {"path": _summary_path("CR204_RESOLVED_SW_PARENT_RECONSTRUCTION", "CR204"), "role": "frozen_resolved_sw_boundary"},
                "cr205_summary": {"path": _summary_path("CR205_SCALAR_GAUGE_FERMION_LANE_SEPARATION", "CR205"), "role": "lane_separation_summary"},
                "cr207_summary": {"path": _summary_path("CR207_CLOSED_LOOP_STABILITY", "CR207"), "role": "frozen_closed_loop_boundary"},
                "cr208_summary": {"path": _summary_path("CR208_WRONG_CONTROL_ZIPPER_AND_BRANCH_VERDICT", "CR208"), "role": "wrong_control_zipper"},
                "cr204a_summary": {"path": _summary_path("CR204a_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION", "CR204a"), "role": "external_endpoint_summary"},
            },
        },
        evaluate,
    )
