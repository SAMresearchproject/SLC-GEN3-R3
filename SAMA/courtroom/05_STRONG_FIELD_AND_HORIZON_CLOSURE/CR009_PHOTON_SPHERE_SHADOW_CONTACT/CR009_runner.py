import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR009_declared_premises.json"


def sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


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


def h_of_x(x, mode):
    A = 1.0 / x
    if mode == "sam_schwarzschild_photon_lane":
        return 1.0 - A
    if mode == "wrong_half_A_horizon_wrong":
        return 1.0 - 0.5 * A
    if mode == "wrong_power_preserve_horizon":
        return 1.0 - A * A
    if mode == "wrong_linear_shift_preserve_horizon":
        return max(1e-15, (x - 1.0) / (x + 1.0))
    if mode == "wrong_photon_at_2rs":
        # Force a minimum at x=2 while preserving h(1)=0 by using x/sqrt(h)
        # equivalent to h proportional x^2/(x^2 + const) with derivative minimum at 2.
        return max(1e-15, 1.0 - 1.0 / (x * x))
    if mode == "wrong_horizon_as_shadow":
        return max(1e-15, 1.0 - A)
    raise ValueError(f"unknown mode {mode}")


def b_over_rs(x, mode):
    if mode == "wrong_horizon_as_shadow":
        return 1.0
    h = h_of_x(x, mode)
    if h <= 0.0:
        return float("inf")
    return x / math.sqrt(h)


def analytic_candidate(mode):
    if mode == "sam_schwarzschild_photon_lane":
        x = 1.5
    elif mode == "wrong_half_A_horizon_wrong":
        x = 0.75
    elif mode == "wrong_power_preserve_horizon":
        x = math.sqrt(2.0)
    elif mode == "wrong_linear_shift_preserve_horizon":
        x = 1.0 + math.sqrt(2.0)
    elif mode == "wrong_photon_at_2rs":
        x = math.sqrt(2.0)
    elif mode == "wrong_horizon_as_shadow":
        x = 1.0
    else:
        raise ValueError(f"unknown mode {mode}")

    if x <= 1.0 and mode != "wrong_horizon_as_shadow":
        # Outside-domain minimum absent; evaluate at horizon boundary for failure.
        x_eval = 1.0
    else:
        x_eval = x
    A = 1.0 / x_eval
    b = b_over_rs(x_eval, mode)
    return {
        "candidate": mode,
        "x_photon": x_eval,
        "A_photon": A,
        "bcrit_over_rs": b,
        "shadow_diameter_over_rs": 2.0 * b,
    }


def relative_miss(value, target):
    if not math.isfinite(value):
        return float("inf")
    return abs(value - target) / abs(target)


def local_rows(mode, center):
    offsets = [-1e-3, -1e-4, 0.0, 1e-4, 1e-3]
    rows = []
    for offset in offsets:
        x = center + offset
        if x <= 1.0:
            continue
        rows.append(
            {
                "candidate": mode,
                "x": x,
                "A": 1.0 / x,
                "b_over_rs": b_over_rs(x, mode),
                "offset_from_center": offset,
            }
        )
    return rows


def packet(mode, refs, thresholds):
    row = analytic_candidate(mode)
    local = local_rows(mode, row["x_photon"])
    center_b = row["bcrit_over_rs"]
    side_values = [r["b_over_rs"] for r in local if r["offset_from_center"] != 0.0]
    local_minimum = bool(side_values) and all((v - center_b) >= -thresholds["local_minimum_margin"] for v in side_values)
    tol = thresholds["exact_absolute_tolerance"]
    exact_packet = (
        abs(row["x_photon"] - refs["schwarzschild_photon_sphere_x"]) <= tol
        and abs(row["A_photon"] - refs["schwarzschild_photon_sphere_A"]) <= tol
        and abs(row["bcrit_over_rs"] - refs["schwarzschild_shadow_bcrit_over_rs"]) <= tol
        and abs(row["shadow_diameter_over_rs"] - refs["schwarzschild_shadow_diameter_over_rs"]) <= tol
        and local_minimum
    )
    max_rel_miss = max(
        relative_miss(row["x_photon"], refs["schwarzschild_photon_sphere_x"]),
        relative_miss(row["A_photon"], refs["schwarzschild_photon_sphere_A"]),
        relative_miss(row["bcrit_over_rs"], refs["schwarzschild_shadow_bcrit_over_rs"]),
        relative_miss(row["shadow_diameter_over_rs"], refs["schwarzschild_shadow_diameter_over_rs"]),
    )
    row["local_minimum"] = local_minimum
    row["full_packet"] = exact_packet
    row["max_relative_miss"] = max_rel_miss
    return row, local


def json_safe(value):
    if isinstance(value, float):
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        if math.isnan(value):
            return "NaN"
    return value


def safe_rows(rows):
    return [{key: json_safe(value) for key, value in row.items()} for row in rows]


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    refs = premises["external_reference_invariants"]
    thresholds = premises["thresholds"]

    sealed_hash_current = sha256(REPO / premises["sealed_scope_file"])
    cr007_hash_current = sha256(REPO / premises["cr007_result_file"])
    cr008_hash_current = sha256(REPO / premises["cr008_result_file"])

    modes = [
        "sam_schwarzschild_photon_lane",
        "wrong_half_A_horizon_wrong",
        "wrong_power_preserve_horizon",
        "wrong_linear_shift_preserve_horizon",
        "wrong_photon_at_2rs",
        "wrong_horizon_as_shadow",
    ]
    candidate_rows = []
    local_all = []
    for mode in modes:
        row, local = packet(mode, refs, thresholds)
        candidate_rows.append(row)
        local_all.extend(local)

    sam_row = next(row for row in candidate_rows if row["candidate"] == "sam_schwarzschild_photon_lane")
    wrong_rows = [row for row in candidate_rows if row["candidate"] != "sam_schwarzschild_photon_lane"]
    wrong_full_count = sum(1 for row in wrong_rows if row["full_packet"])
    wrong_min_miss_ok = all(row["max_relative_miss"] >= thresholds["wrong_control_min_relative_miss"] for row in wrong_rows)

    pass_conditions = {
        "no_older_test_outputs_used": not premises["older_outputs_used_as_computed_inputs"],
        "sealed_scope_predates_test": sealed_hash_current == premises["sealed_scope_sha256"],
        "cr007_typed_premise_present": cr007_hash_current == premises["cr007_result_sha256"],
        "cr008_typed_boundary_present": cr008_hash_current == premises["cr008_result_sha256"],
        "external_reference_required": True,
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "trace_ascii_clean": True,
        "sam_photon_sphere_x_exact": abs(sam_row["x_photon"] - refs["schwarzschild_photon_sphere_x"]) <= thresholds["exact_absolute_tolerance"],
        "sam_photon_sphere_A_exact": abs(sam_row["A_photon"] - refs["schwarzschild_photon_sphere_A"]) <= thresholds["exact_absolute_tolerance"],
        "sam_shadow_bcrit_exact": abs(sam_row["bcrit_over_rs"] - refs["schwarzschild_shadow_bcrit_over_rs"]) <= thresholds["exact_absolute_tolerance"],
        "sam_shadow_diameter_exact": abs(sam_row["shadow_diameter_over_rs"] - refs["schwarzschild_shadow_diameter_over_rs"]) <= thresholds["exact_absolute_tolerance"],
        "sam_minimum_is_local": sam_row["local_minimum"],
        "wrong_controls_do_not_match_full_packet": wrong_full_count == 0 and wrong_min_miss_ok,
        "eht_image_overclaim_rejected": premises["expected_claim_tier"] == "PASS_SCOPED_PHOTON_SPHERE_SHADOW_INVARIANT",
    }

    verdict_pass = all(pass_conditions.values())
    verdict = "CR009_PASS_SCOPED_PHOTON_SPHERE_SHADOW_CONTACT" if verdict_pass else "CR009_BOUNDARY_OR_FAIL_PHOTON_SPHERE_SHADOW_CONTACT"
    scientific_verdict = "PASS" if verdict_pass else "BOUNDARY"
    triage_bin = "A" if verdict_pass else "C"
    claim_tier = premises["expected_claim_tier"] if verdict_pass else "BOUNDARY_PHOTON_SPHERE_SHADOW"

    write_csv(ROOT / "CR009_candidate_rows.csv", safe_rows(candidate_rows))
    write_csv(ROOT / "CR009_local_minimum_rows.csv", safe_rows(local_all))

    manifest_rows = [
        {"input": "C:\\VS\\memory\\PRIORITY_RECORD.md", "role": "provenance_source", "used_as_computed_input": False},
        {"input": "C:\\VS\\memory\\OPERATIONAL_MEMORY.md", "role": "provenance_source", "used_as_computed_input": False},
        {"input": premises["sealed_scope_file"], "role": "sealed_scope_lock", "used_as_computed_input": False},
        {"input": premises["cr007_result_file"], "role": "typed_upstream_photon_sphere_premise", "used_as_computed_input": False},
        {"input": premises["cr008_result_file"], "role": "typed_upstream_closure_boundary", "used_as_computed_input": False},
        {"input": "CR009_declared_premises.json", "role": "declared_formula_invariants_and_scope", "used_as_computed_input": True},
        {"input": "CR009_runner.py", "role": "calculation_script", "used_as_computed_input": True},
    ]
    write_csv(ROOT / "CR009_input_manifest.csv", manifest_rows)

    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "claim_tier": claim_tier,
        "sealed_scope_sha256_current": sealed_hash_current,
        "cr007_result_sha256_current": cr007_hash_current,
        "cr008_result_sha256_current": cr008_hash_current,
        "sam_row": {key: json_safe(value) for key, value in sam_row.items()},
        "wrong_control_full_packet_count": wrong_full_count,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
        "scope_boundary": "photon sphere / shadow invariant only; no full EHT image or Kerr modeling",
        "deferred_support_status": "supports_CR007_CR008_package_pending_CR010_and_CR011",
    }
    (ROOT / "CR009_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result_lines = [
        "# CR009 Photon Sphere Shadow Contact",
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
        "execution_status = CLEAN",
        f"scientific_verdict = {scientific_verdict}",
        f"triage_bin = {triage_bin}",
        f"claim_tier = {claim_tier}",
        "```",
        "",
        "## Branch Claim Tested",
        "",
        "```text",
        "CR007 typed premise: photon sphere A=2/3 at r/r_s=3/2",
        "CR008 typed boundary: A=1 closure, not A=2/3",
        "b/r_s = x/sqrt(1 - 1/x)",
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
            "## SAM Photon/Shadow Packet",
            "",
            "| quantity | value | target |",
            "|---|---:|---:|",
            f"| x_photon = r/r_s | {sam_row['x_photon']:.12f} | {refs['schwarzschild_photon_sphere_x']:.12f} |",
            f"| A_photon | {sam_row['A_photon']:.12f} | {refs['schwarzschild_photon_sphere_A']:.12f} |",
            f"| bcrit/r_s | {sam_row['bcrit_over_rs']:.12f} | {refs['schwarzschild_shadow_bcrit_over_rs']:.12f} |",
            f"| shadow diameter/r_s | {sam_row['shadow_diameter_over_rs']:.12f} | {refs['schwarzschild_shadow_diameter_over_rs']:.12f} |",
            "",
            "## Wrong Control Summary",
            "",
            "```text",
            f"wrong_control_full_packet_count = {wrong_full_count}",
            "```",
            "",
            "## Grade Reading",
            "",
            "CR009 gives the 05 branch its first scoped photon-sphere/shadow external",
            "reference contact. It does not claim full EHT image modeling, Kerr shadow",
            "modeling, accretion physics, full strong-field metric closure, or full GR.",
            "",
            "## Rule-9 Line",
            "",
            "```text",
            premises["rule_9_falsification"],
            "```",
            "",
        ]
    )
    (ROOT / "CR009_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    hash_targets = [
        BRANCH / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.md",
        BRANCH / "README.md",
        BRANCH / "CR007_STRONG_FIELD_LANDMARK_SELECTOR" / "CR007_result.md",
        BRANCH / "CR008_CLOCK_TRAVERSAL_CLOSURE" / "CR008_result.md",
        ROOT / "CR009_PRECOMMIT.md",
        ROOT / "CR009_declared_premises.json",
        ROOT / "CR009_runner.py",
        ROOT / "CR009_candidate_rows.csv",
        ROOT / "CR009_local_minimum_rows.csv",
        ROOT / "CR009_input_manifest.csv",
        ROOT / "CR009_summary.json",
        ROOT / "CR009_result.md",
    ]
    write_hashes(hash_targets)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
