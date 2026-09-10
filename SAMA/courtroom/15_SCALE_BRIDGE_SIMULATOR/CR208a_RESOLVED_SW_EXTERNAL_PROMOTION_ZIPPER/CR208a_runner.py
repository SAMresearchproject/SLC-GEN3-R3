import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


SAM_SIM = Path(r"C:\VS\sam_sim\artifacts")
G756 = SAM_SIM / "G756c_SIMULATOR_CLOSED_LOOP_STABILITY_TEST"
CR208_SUMMARY = BRANCH / "CR208_WRONG_CONTROL_ZIPPER_AND_BRANCH_VERDICT" / "CR208_summary.json"


def _sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def _read_hash_lines(path):
    lines = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        raw = raw.lstrip("\ufeff").strip()
        if raw and not raw.startswith("#"):
            lines.append(raw)
    return lines


def _extract_trace_hashes(g756_summary):
    return {
        item["trace"]: item["sha256"].lower()
        for item in g756_summary.get("trace_hashes", [])
    }


def _fingerprint(payload):
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evaluate(sources):
    cr204 = sources["cr204_summary"]
    cr204a = sources["cr204a_summary"]
    cr207 = sources["cr207_summary"]
    cr207a = sources["cr207a_summary"]
    cr208 = sources["cr208_summary"]
    g756 = sources["g756_summary"]
    metadata_hash_lines = _read_hash_lines(ROOT.parent / "CR204a_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION" / "CR204a_metadata_manifest.csv.sha256.txt")
    trace_hashes = _extract_trace_hashes(g756)
    cr204a_sources = {a["source_id"]: a["sha256"] for a in cr204a.get("source_artifacts", [])}
    cr207a_sources = {a["source_id"]: a["sha256"] for a in cr207a.get("source_artifacts", [])}
    source_artifacts = sources.get("__source_artifacts__", {})
    wrong_control_counts = {
        row["key"]: row["value"]
        for row in cr208.get("evidence_rows", [])
        if row["key"] in {"total_controls", "controls_passed", "controls_fired_or_degraded", "honest_diagnostics", "failed_controls"}
    }
    zipper_payload = {
        "ladder": {
            "CR204": cr204["scientific_verdict"],
            "CR204a": cr204a["scientific_verdict"],
            "CR207": cr207["scientific_verdict"],
            "CR207a": cr207a["scientific_verdict"],
        },
        "metadata_manifest_sha256": cr204a_sources.get("metadata_manifest"),
        "wrong_control_counts": wrong_control_counts,
        "trace_hashes": trace_hashes,
        "chain_fingerprint": next(
            row["value"] for row in cr207a["evidence_rows"]
            if row["key"] == "chain_fingerprint_sha256"
        ),
    }
    zipper_fingerprint = _fingerprint(zipper_payload)
    conditions = {
        "cr204_remains_boundary": cr204["scientific_verdict"] == "BOUNDARY",
        "cr204a_external_topology_pass": cr204a["scientific_verdict"] == "PASS",
        "cr207_remains_boundary": cr207["scientific_verdict"] == "BOUNDARY",
        "cr207a_external_chain_pass": cr207a["scientific_verdict"] == "PASS",
        "cr204a_manifest_hash_preserved": cr204a_sources.get("metadata_manifest") == "332599bd79e84ef74918561c296a7cc9783a0078c68c44b89881883e3a062235",
        "cr204a_manifest_hash_sibling_present": len(metadata_hash_lines) == 1 and metadata_hash_lines[0].startswith("332599bd79e84ef74918561c296a7cc9783a0078c68c44b89881883e3a062235"),
        "cr208_wrong_controls_preserved": wrong_control_counts.get("total_controls") == 43 and wrong_control_counts.get("failed_controls") == 0,
        "g756_replay_trace_hashes_present": len(trace_hashes) == 5,
        "cr207a_chain_fingerprint_present": "chain_fingerprint_sha256" in {r["key"] for r in cr207a["evidence_rows"]},
        "no_free_parameters": all(
            s.get("pass_conditions", {}).get("no_free_parameters", True) is True
            for s in [cr204, cr204a, cr207, cr207a, cr208]
        ),
    }
    evidence = [
        {"key": "claim_ladder", "value": "CR204 BOUNDARY; CR204a PASS; CR207 BOUNDARY; CR207a PASS", "note": "original boundaries preserved"},
        {"key": "scoped_pass", "value": "external resolved-parent topology bridge established", "note": "CR208a scoped verdict"},
        {"key": "remaining_boundary", "value": "full particle-sector / electroweak theorem closure remains open", "note": "not claimed by zipper"},
        {"key": "metadata_manifest_sha256", "value": cr204a_sources.get("metadata_manifest"), "note": "CR204a allowed-import manifest"},
        {"key": "wrong_control_report", "value": f"{wrong_control_counts.get('controls_passed')}/{wrong_control_counts.get('total_controls')} passed; {wrong_control_counts.get('failed_controls')} failed", "note": "from CR208"},
        {"key": "wrong_control_report_sha256", "value": _sha256(CR208_SUMMARY), "note": "CR208_summary.json"},
        {"key": "replay_trace_hash_count", "value": len(trace_hashes), "note": "from G756 closed-loop summary"},
        {"key": "replay_trace_hashes", "value": "; ".join(f"{k}={v}" for k, v in sorted(trace_hashes.items())), "note": "from G756 closed-loop summary"},
        {"key": "cr207a_chain_fingerprint", "value": zipper_payload["chain_fingerprint"], "note": "external-chain replay fingerprint"},
        {"key": "cr208a_zipper_fingerprint", "value": zipper_fingerprint, "note": "this zipper payload fingerprint"},
    ]
    return {
        "result_class": "CR208a_PASS_EXTERNAL_RESOLVED_PARENT_TOPOLOGY_BRIDGE_ESTABLISHED__BOUNDARY_FULL_EW_THEOREM_OPEN",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "RESOLVED_SW_EXTERNAL_PROMOTION_ZIPPER",
        "question": "Can the resolved-SW external topology promotion ladder be zipped while preserving original boundary verdicts?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that the simulator's resolved-SW grammar has a clean external topology promotion path while preserving original boundary verdicts, metadata hashes, wrong-control evidence, and replay traces.",
        "notes": [
            "CR204 and CR207 remain BOUNDARY.",
            "CR204a and CR207a are the promotion artifacts that pass.",
            "The scoped pass is topology-bridge establishment; full particle-sector/electroweak theorem closure remains open.",
        ],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR208a",
            "title": "Resolved-SW External Promotion Zipper",
            "source_paths": {
                "cr204_summary": {"path": BRANCH / "CR204_RESOLVED_SW_PARENT_RECONSTRUCTION" / "CR204_summary.json", "role": "internal_resolved_parent_boundary"},
                "cr204a_summary": {"path": BRANCH / "CR204a_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION" / "CR204a_summary.json", "role": "external_topology_promotion"},
                "cr207_summary": {"path": BRANCH / "CR207_CLOSED_LOOP_STABILITY" / "CR207_summary.json", "role": "internal_replay_boundary"},
                "cr207a_summary": {"path": BRANCH / "CR207a_EXTERNAL_CHAIN_REPLAY_STABILITY" / "CR207a_summary.json", "role": "external_chain_promotion"},
                "cr208_summary": {"path": CR208_SUMMARY, "role": "wrong_control_report"},
                "g756_summary": {"path": G756 / "G756c_summary.json", "role": "replay_trace_hashes"},
                "cr204a_metadata_manifest": {"path": BRANCH / "CR204a_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION" / "CR204a_metadata_manifest.csv", "role": "metadata_manifest_hash_target"},
                "cr204a_metadata_manifest_hash": {"path": BRANCH / "CR204a_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION" / "CR204a_metadata_manifest.csv.sha256.txt", "role": "metadata_manifest_hash_sibling"},
            },
        },
        evaluate,
    )
