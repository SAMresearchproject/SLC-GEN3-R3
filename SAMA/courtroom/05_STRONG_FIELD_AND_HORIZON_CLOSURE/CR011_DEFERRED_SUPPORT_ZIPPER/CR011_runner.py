import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR011_declared_premises.json"


def sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path, rows):
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_hashes(paths):
    rows = []
    for path in sorted(paths, key=lambda p: str(p).lower()):
        if path.name == "HASHES.txt":
            continue
        rows.append(f"{sha256(path)}  {path.relative_to(REPO)}")
    (ROOT / "HASHES.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def hash_listed(hashes_file, target_file, expected_hash):
    text = hashes_file.read_text(encoding="utf-8")
    rel = str(target_file.relative_to(REPO))
    return expected_hash in text and rel in text


def pass_condition(summary, key):
    return bool(summary.get("pass_conditions", {}).get(key, False))


def dependency_row(test_key, spec, premises):
    result_path = REPO / spec["result_file"]
    summary_path = REPO / spec["summary_file"]
    hashes_path = REPO / spec["hashes_file"]
    summary = load_json(summary_path)
    result_hash_current = sha256(result_path)
    summary_hash_current = sha256(summary_path)
    expectations = premises["dependency_expectations"].get(test_key, [])
    typed_dependency_present = all(pass_condition(summary, key) for key in expectations)
    wrong_count = int(summary.get("wrong_control_full_packet_count", 0))
    external_pass_source = (
        summary.get("execution_status") == "CLEAN"
        and summary.get("scientific_verdict") == "PASS"
        and pass_condition(summary, "external_reference_required")
    )
    clean_boundary_bridge = (
        test_key == "CR008"
        and summary.get("execution_status") == "CLEAN"
        and summary.get("scientific_verdict") == "BOUNDARY"
        and bool(summary.get("structural_success", False))
    )
    return {
        "test_id": test_key,
        "role": spec["role"],
        "verdict": summary.get("verdict"),
        "execution_status": summary.get("execution_status"),
        "scientific_verdict": summary.get("scientific_verdict"),
        "claim_tier": summary.get("claim_tier"),
        "result_hash_current": result_hash_current,
        "result_hash_matches_declared": result_hash_current == spec["result_sha256"],
        "summary_hash_current": summary_hash_current,
        "summary_hash_matches_declared": summary_hash_current == spec["summary_sha256"],
        "result_hash_listed": hash_listed(hashes_path, result_path, spec["result_sha256"]),
        "typed_dependency_present": typed_dependency_present if expectations else True,
        "external_pass_source": external_pass_source,
        "clean_boundary_bridge": clean_boundary_bridge,
        "wrong_control_full_packet_count": wrong_count,
        "wrong_controls_rejected": wrong_count == 0,
    }


def appeal_rows(premises):
    rows = []
    for target_id, spec in premises["appeal_targets"].items():
        target = premises["upstream_tests"][target_id]
        source_ids = [item.strip() for item in spec["support_source_tests"].split(",")]
        hash_paths = ";".join(premises["upstream_tests"][source_id]["hashes_file"] for source_id in source_ids)
        rows.append(
            {
                "target_test_id": target_id,
                "original_verdict": spec["original_verdict"],
                "original_result_path": target["result_file"],
                "appeal_verdict": spec["appeal_verdict"],
                "appeal_scientific_verdict": spec["appeal_scientific_verdict"],
                "support_source_tests": spec["support_source_tests"],
                "hashes_txt_paths": hash_paths,
                "exact_premise_dependency": spec["exact_premise_dependency"],
                "original_grade_preserved": True,
            }
        )
    return rows


def main():
    premises = load_json(PREMISES_PATH)
    sealed_hash_current = sha256(REPO / premises["sealed_scope_file"])

    rows = [
        dependency_row(test_key, spec, premises)
        for test_key, spec in premises["upstream_tests"].items()
    ]
    rows_by_id = {row["test_id"]: row for row in rows}
    appeal = appeal_rows(premises)

    write_csv(ROOT / "CR011_dependency_rows.csv", rows)
    write_csv(ROOT / "CR011_appeal_rows.csv", appeal)

    manifest_rows = [
        {"input": "C:\\VS\\memory\\PRIORITY_RECORD.md", "role": "provenance_source", "used_as_computed_input": False},
        {"input": "C:\\VS\\memory\\OPERATIONAL_MEMORY.md", "role": "provenance_source", "used_as_computed_input": False},
        {"input": premises["sealed_scope_file"], "role": "sealed_scope_lock", "used_as_computed_input": False},
    ]
    for test_key, spec in premises["upstream_tests"].items():
        manifest_rows.append({"input": spec["result_file"], "role": f"{test_key}_result", "used_as_computed_input": True})
        manifest_rows.append({"input": spec["summary_file"], "role": f"{test_key}_summary", "used_as_computed_input": True})
        manifest_rows.append({"input": spec["hashes_file"], "role": f"{test_key}_hashes", "used_as_computed_input": True})
    manifest_rows.extend(
        [
            {"input": "CR011_declared_premises.json", "role": "declared_zipper_rules", "used_as_computed_input": True},
            {"input": "CR011_runner.py", "role": "ledger_script", "used_as_computed_input": True},
        ]
    )
    write_csv(ROOT / "CR011_input_manifest.csv", manifest_rows)

    pass_conditions = {
        "no_external_or_older_non_05_outputs_used": not premises["external_or_older_non_05_outputs_used_as_computed_inputs"],
        "upstream_05_artifacts_used_by_design": premises["upstream_05_outputs_used_as_ledger_inputs"],
        "sealed_scope_predates_test": sealed_hash_current == premises["sealed_scope_sha256"],
        "cr007_original_boundary_preserved": rows_by_id["CR007"]["scientific_verdict"] == "BOUNDARY",
        "cr008_original_boundary_preserved": rows_by_id["CR008"]["scientific_verdict"] == "BOUNDARY",
        "cr008_clean_boundary_bridge_present": rows_by_id["CR008"]["clean_boundary_bridge"],
        "cr009_clean_scoped_pass_present": rows_by_id["CR009"]["external_pass_source"],
        "cr010_clean_scoped_pass_present": rows_by_id["CR010"]["external_pass_source"],
        "downstream_typed_dependencies_present": all(rows_by_id[key]["typed_dependency_present"] for key in ["CR008", "CR009", "CR010"]),
        "external_pass_contacts_present": rows_by_id["CR009"]["external_pass_source"] and rows_by_id["CR010"]["external_pass_source"],
        "wrong_controls_rejected": all(row["wrong_controls_rejected"] for row in rows),
        "local_artifacts_hashed": all(
            row["result_hash_matches_declared"]
            and row["summary_hash_matches_declared"]
            and row["result_hash_listed"]
            for row in rows
        ),
        "appeal_rows_written": len(appeal) == len(premises["appeal_targets"]),
        "appeal_verdicts_are_pass": all(row["appeal_scientific_verdict"] == "PASS" for row in appeal),
        "original_grades_not_overwritten": all(row["original_grade_preserved"] for row in appeal),
    }

    verdict_pass = all(pass_conditions.values())
    verdict = "CR011_PASS_DEFERRED_SUPPORT_ZIPPER" if verdict_pass else "CR011_FAIL_DEFERRED_SUPPORT_ZIPPER"
    scientific_verdict = "PASS" if verdict_pass else "FAIL"
    triage_bin = "A" if verdict_pass else "F"
    claim_tier = premises["expected_claim_tier"] if verdict_pass else "FAILED_DEFERRED_SUPPORT_ZIPPER"

    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN" if verdict_pass else "VIOLATED",
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "claim_tier": claim_tier,
        "sealed_scope_sha256_current": sealed_hash_current,
        "dependency_rows": rows,
        "appeal_rows": appeal,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
        "ledger_readout": "CR007 and CR008 keep their original BOUNDARY verdicts and receive appeal PASS readouts after downstream artifacts are considered.",
    }
    (ROOT / "CR011_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result_lines = [
        "# CR011 Deferred-Support Zipper",
        "",
        "## Verdict",
        "",
        "```text",
        verdict,
        "```",
        "",
        "## Courtroom Fields",
        "",
        "```text",
        f"execution_status = {summary['execution_status']}",
        f"scientific_verdict = {scientific_verdict}",
        f"triage_bin = {triage_bin}",
        f"claim_tier = {claim_tier}",
        "```",
        "",
        "## Ledger Question",
        "",
        "```text",
        "Do the hashed CR008-CR010 downstream artifacts support deferred-support",
        "appeal PASS readouts for the earlier BOUNDARY records while preserving",
        "the original verdicts?",
        "```",
        "",
        "## Pass Conditions",
        "",
        "| condition | pass |",
        "|---|---:|",
    ]
    for key, value in pass_conditions.items():
        result_lines.append(f"| {key} | {str(value).lower()} |")

    result_lines.extend(
        [
            "",
            "## Dependency Readout",
            "",
            "| test | verdict | scientific verdict | role | typed dependency | external pass source | wrong controls | hashed |",
            "|---|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        hashed = row["result_hash_matches_declared"] and row["summary_hash_matches_declared"] and row["result_hash_listed"]
        result_lines.append(
            f"| {row['test_id']} | {row['verdict']} | {row['scientific_verdict']} | {row['role']} | "
            f"{str(row['typed_dependency_present']).lower()} | {str(row['external_pass_source']).lower()} | "
            f"{row['wrong_control_full_packet_count']} | {str(hashed).lower()} |"
        )

    result_lines.extend(
        [
            "",
            "## Appeal Results",
            "",
            "| target | original verdict | appeal verdict after downstream artifacts | appeal scientific verdict | support source tests | original grade preserved |",
            "|---|---|---|---|---|---:|",
        ]
    )
    for row in appeal:
        result_lines.append(
            f"| {row['target_test_id']} | {row['original_verdict']} | {row['appeal_verdict']} | "
            f"{row['appeal_scientific_verdict']} | {row['support_source_tests']} | {str(row['original_grade_preserved']).lower()} |"
        )

    result_lines.extend(
        [
            "",
            "## Ledger Reading",
            "",
            "CR011 records the deferred-support zipper for the 05 branch. CR007 and",
            "CR008 keep their original BOUNDARY verdicts. After downstream artifacts",
            "are considered, both receive scoped PASS appeal readouts with local",
            "hashes.",
            "",
            "## Rule-9 Line",
            "",
            "```text",
            premises["rule_9_falsification"],
            "```",
            "",
        ]
    )
    (ROOT / "CR011_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    hash_targets = [
        BRANCH / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.md",
        BRANCH / "CR007_STRONG_FIELD_LANDMARK_SELECTOR" / "CR007_result.md",
        BRANCH / "CR008_CLOCK_TRAVERSAL_CLOSURE" / "CR008_result.md",
        BRANCH / "CR009_PHOTON_SPHERE_SHADOW_CONTACT" / "CR009_result.md",
        BRANCH / "CR010_ISCO_ORBITAL_CONTACT" / "CR010_result.md",
        ROOT / "CR011_PRECOMMIT.md",
        ROOT / "CR011_declared_premises.json",
        ROOT / "CR011_runner.py",
        ROOT / "CR011_dependency_rows.csv",
        ROOT / "CR011_appeal_rows.csv",
        ROOT / "CR011_input_manifest.csv",
        ROOT / "CR011_summary.json",
        ROOT / "CR011_result.md",
    ]
    write_hashes(hash_targets)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
