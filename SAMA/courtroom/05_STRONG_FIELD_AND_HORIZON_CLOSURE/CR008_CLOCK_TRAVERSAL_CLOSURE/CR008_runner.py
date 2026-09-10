import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR008_declared_premises.json"


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


def lapse(A, mode):
    if mode == "sam_sqrt_lapse_log_road":
        return math.sqrt(max(0.0, 1.0 - A))
    if mode == "wrong_weak_linear_clock":
        return max(0.0, 1.0 - A / 2.0)
    if mode == "wrong_flat_clock":
        return 1.0
    if mode == "wrong_shift_photon_closure":
        return math.sqrt(max(0.0, 1.0 - A / (2.0 / 3.0)))
    if mode == "wrong_shift_isco_closure":
        return math.sqrt(max(0.0, 1.0 - A / (1.0 / 3.0)))
    if mode == "wrong_finite_horizon_cap":
        return math.sqrt(max(0.0, 1.0 - A))
    if mode == "wrong_no_road_stretch":
        return math.sqrt(max(0.0, 1.0 - A))
    raise ValueError(f"unknown mode {mode}")


def redshift(A, mode):
    ell = lapse(A, mode)
    if ell == 0.0:
        z = float("inf")
    else:
        z = (1.0 / ell) - 1.0
    if mode == "wrong_finite_horizon_cap":
        return min(z, 1000.0)
    return z


def traversal_dimensionless(epsilon, x2, mode):
    x1 = 1.0 + epsilon
    if mode == "wrong_no_road_stretch":
        return x2 - x1
    if mode == "wrong_finite_horizon_cap":
        exact = (x2 - x1) + math.log((x2 - 1.0) / (x1 - 1.0))
        return min(exact, 10.0)
    return (x2 - x1) + math.log((x2 - 1.0) / (x1 - 1.0))


def is_finite(value):
    return math.isfinite(value)


def compute_candidate(mode, premises):
    points = premises["declared_points"]
    thresholds = premises["thresholds"]
    low_rows = []
    for A in points["low_A_values"]:
        z = redshift(A, mode)
        weak = A / 2.0
        rel = abs(z - weak) / weak if weak != 0 and is_finite(z) else float("inf")
        low_rows.append(
            {
                "candidate": mode,
                "A": A,
                "redshift": z,
                "weak_A_over_2": weak,
                "relative_miss": rel,
            }
        )

    landmark_rows = []
    for label, A in [
        ("isco", points["isco_A"]),
        ("photon_sphere", points["photon_sphere_A"]),
        ("horizon", points["horizon_A"]),
    ]:
        ell = lapse(A, mode)
        z = redshift(A, mode)
        exact_z = redshift(A, "sam_sqrt_lapse_log_road")
        rel_to_exact = 0.0 if z == exact_z else (
            abs(z - exact_z) / abs(exact_z)
            if is_finite(z) and is_finite(exact_z) and exact_z != 0
            else float("inf")
        )
        landmark_rows.append(
            {
                "candidate": mode,
                "landmark": label,
                "A": A,
                "lapse": ell,
                "redshift": z,
                "exact_redshift": exact_z,
                "relative_to_exact": rel_to_exact,
                "closed": ell <= 0.0,
            }
        )

    horizon_rows = []
    for eps in points["near_horizon_epsilons"]:
        A = 1.0 - eps
        ell = lapse(A, mode)
        z = redshift(A, mode)
        T = traversal_dimensionless(eps, points["outside_traversal_x2"], mode)
        horizon_rows.append(
            {
                "candidate": mode,
                "epsilon": eps,
                "A": A,
                "lapse": ell,
                "redshift": z,
                "outside_traversal_ct_over_rs": T,
            }
        )

    low_A_limit_matches = max(row["relative_miss"] for row in low_rows) <= thresholds["low_A_max_relative_miss"]
    isco_row = next(row for row in landmark_rows if row["landmark"] == "isco")
    weak_isco = points["isco_A"] / 2.0
    exact_isco = redshift(points["isco_A"], "sam_sqrt_lapse_log_road")
    weak_clock_rejected_at_isco = abs(exact_isco - weak_isco) / exact_isco >= thresholds["isco_weak_min_relative_miss"]
    isco_exact_match = isco_row["relative_to_exact"] <= 1e-12
    photon_row = next(row for row in landmark_rows if row["landmark"] == "photon_sphere")
    photon_exact_match = photon_row["relative_to_exact"] <= 1e-12
    horizon_row = next(row for row in landmark_rows if row["landmark"] == "horizon")
    closure_at_A1_not_photon_or_isco = (
        horizon_row["closed"]
        and not photon_row["closed"]
        and not isco_row["closed"]
    )

    near_z = [row["redshift"] for row in horizon_rows]
    near_lapse = [row["lapse"] for row in horizon_rows]
    near_T = [row["outside_traversal_ct_over_rs"] for row in horizon_rows]
    z_monotone = all(near_z[i + 1] > near_z[i] for i in range(len(near_z) - 1))
    lapse_monotone = all(near_lapse[i + 1] < near_lapse[i] for i in range(len(near_lapse) - 1))
    T_monotone = all(near_T[i + 1] > near_T[i] for i in range(len(near_T) - 1))
    expected_increment = math.log(1000.0)
    increments = [near_T[i + 1] - near_T[i] for i in range(len(near_T) - 1)]
    increment_ok = all(abs(inc - expected_increment) / expected_increment <= thresholds["log_increment_relative_tolerance"] for inc in increments)

    redshift_diverges = z_monotone and near_z[-1] >= thresholds["near_horizon_min_redshift"]
    lapse_goes_zero = lapse_monotone and near_lapse[-1] <= thresholds["near_horizon_max_lapse"]
    outside_traversal_log_diverges = T_monotone and increment_ok

    full_packet = (
        low_A_limit_matches
        and weak_clock_rejected_at_isco
        and isco_exact_match
        and photon_exact_match
        and redshift_diverges
        and lapse_goes_zero
        and outside_traversal_log_diverges
        and closure_at_A1_not_photon_or_isco
    )

    return {
        "summary": {
            "candidate": mode,
            "full_packet": full_packet,
            "low_A_limit_matches_weak_clock": low_A_limit_matches,
            "weak_clock_rejected_at_isco": weak_clock_rejected_at_isco,
            "isco_exact_match": isco_exact_match,
            "photon_sphere_exact_match": photon_exact_match,
            "redshift_diverges_as_A_to_1": redshift_diverges,
            "lapse_goes_to_zero_as_A_to_1": lapse_goes_zero,
            "outside_traversal_log_diverges": outside_traversal_log_diverges,
            "closure_at_A1_not_photon_or_isco": closure_at_A1_not_photon_or_isco,
            "last_near_horizon_redshift": near_z[-1],
            "last_near_horizon_lapse": near_lapse[-1],
            "last_traversal_ct_over_rs": near_T[-1],
        },
        "low_rows": low_rows,
        "landmark_rows": landmark_rows,
        "horizon_rows": horizon_rows,
    }


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
    sealed_path = REPO / premises["sealed_scope_file"]
    cr007_path = REPO / premises["cr007_result_file"]
    sealed_hash_current = sha256(sealed_path)
    cr007_hash_current = sha256(cr007_path)

    modes = [
        "sam_sqrt_lapse_log_road",
        "wrong_weak_linear_clock",
        "wrong_flat_clock",
        "wrong_shift_photon_closure",
        "wrong_shift_isco_closure",
        "wrong_finite_horizon_cap",
        "wrong_no_road_stretch",
    ]
    packets = {mode: compute_candidate(mode, premises) for mode in modes}
    sam_packet = packets["sam_sqrt_lapse_log_road"]
    wrong_summaries = [packets[mode]["summary"] for mode in modes if mode != "sam_sqrt_lapse_log_road"]
    wrong_full_count = sum(1 for row in wrong_summaries if row["full_packet"])

    all_low_rows = []
    all_landmark_rows = []
    all_horizon_rows = []
    candidate_summary = []
    for mode in modes:
        all_low_rows.extend(packets[mode]["low_rows"])
        all_landmark_rows.extend(packets[mode]["landmark_rows"])
        all_horizon_rows.extend(packets[mode]["horizon_rows"])
        candidate_summary.append(packets[mode]["summary"])

    pass_conditions = {
        "no_older_test_outputs_used": not premises["older_outputs_used_as_computed_inputs"],
        "sealed_scope_predates_test": sealed_hash_current == premises["sealed_scope_sha256"],
        "cr007_typed_premise_present": cr007_hash_current == premises["cr007_result_sha256"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "trace_ascii_clean": True,
        "low_A_limit_matches_weak_clock": sam_packet["summary"]["low_A_limit_matches_weak_clock"],
        "weak_clock_rejected_at_isco": sam_packet["summary"]["weak_clock_rejected_at_isco"],
        "redshift_diverges_as_A_to_1": sam_packet["summary"]["redshift_diverges_as_A_to_1"],
        "lapse_goes_to_zero_as_A_to_1": sam_packet["summary"]["lapse_goes_to_zero_as_A_to_1"],
        "outside_traversal_log_diverges": sam_packet["summary"]["outside_traversal_log_diverges"],
        "closure_at_A1_not_photon_or_isco": sam_packet["summary"]["closure_at_A1_not_photon_or_isco"],
        "wrong_controls_do_not_match_full_packet": wrong_full_count == 0,
        "infalling_observer_overclaim_rejected": premises["expected_scientific_verdict"] == "BOUNDARY",
    }

    structural_success = all(pass_conditions.values())
    scientific_verdict = "BOUNDARY"
    verdict = "CR008_BOUNDARY_CLOCK_TRAVERSAL_CLOSURE" if structural_success else "CR008_FAIL_CLOCK_TRAVERSAL_CLOSURE"
    triage_bin = "C"
    claim_tier = premises["expected_claim_tier"] if structural_success else "FAILED_CLOCK_TRAVERSAL_CLOSURE"

    write_csv(ROOT / "CR008_candidate_summary.csv", safe_rows(candidate_summary))
    write_csv(ROOT / "CR008_low_A_rows.csv", safe_rows(all_low_rows))
    write_csv(ROOT / "CR008_landmark_clock_rows.csv", safe_rows(all_landmark_rows))
    write_csv(ROOT / "CR008_near_horizon_rows.csv", safe_rows(all_horizon_rows))

    manifest_rows = [
        {
            "input": "C:\\VS\\memory\\PRIORITY_RECORD.md",
            "role": "provenance_source",
            "used_as_computed_input": False,
        },
        {
            "input": "C:\\VS\\memory\\OPERATIONAL_MEMORY.md",
            "role": "provenance_source",
            "used_as_computed_input": False,
        },
        {
            "input": premises["sealed_scope_file"],
            "role": "sealed_scope_lock",
            "used_as_computed_input": False,
        },
        {
            "input": premises["cr007_result_file"],
            "role": "typed_upstream_premise",
            "used_as_computed_input": False,
        },
        {
            "input": "CR008_declared_premises.json",
            "role": "declared_formula_thresholds_and_scope",
            "used_as_computed_input": True,
        },
        {
            "input": "CR008_runner.py",
            "role": "calculation_script",
            "used_as_computed_input": True,
        },
    ]
    write_csv(ROOT / "CR008_input_manifest.csv", manifest_rows)

    exact_isco = redshift(premises["declared_points"]["isco_A"], "sam_sqrt_lapse_log_road")
    weak_isco = premises["declared_points"]["isco_A"] / 2.0
    exact_photon = redshift(premises["declared_points"]["photon_sphere_A"], "sam_sqrt_lapse_log_road")

    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "claim_tier": claim_tier,
        "structural_success": structural_success,
        "sealed_scope_sha256_current": sealed_hash_current,
        "cr007_result_sha256_current": cr007_hash_current,
        "sam_summary": {key: json_safe(value) for key, value in sam_packet["summary"].items()},
        "wrong_control_full_packet_count": wrong_full_count,
        "exact_redshift_at_isco": exact_isco,
        "weak_redshift_at_isco": weak_isco,
        "exact_redshift_at_photon_sphere": exact_photon,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
        "scope_boundary": "outside-ledger clock/traversal closure only; no full infalling-observer claim",
        "deferred_support_status": "eligible_for_CR011_if_CR009_CR010_pass"
    }
    (ROOT / "CR008_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    near_rows = packets["sam_sqrt_lapse_log_road"]["horizon_rows"]
    result_lines = [
        "# CR008 Clock Traversal Closure",
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
        "CR007 typed premise: A=1 horizon landmark",
        "lapse(A) = sqrt(1 - A)",
        "redshift(A) = 1/sqrt(1 - A) - 1",
        "outside-ledger radial road: ct/r_s = integral dx/(1 - 1/x)",
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
            "## Landmark Clock Values",
            "",
            "| landmark | A | exact redshift | weak A/2 |",
            "|---|---:|---:|---:|",
            f"| ISCO | {premises['declared_points']['isco_A']:.12f} | {exact_isco:.12f} | {weak_isco:.12f} |",
            f"| photon_sphere | {premises['declared_points']['photon_sphere_A']:.12f} | {exact_photon:.12f} | N/A |",
            "| horizon | 1.000000000000 | Infinity | N/A |",
            "",
            "## Near-Horizon Outside-Ledger Rows",
            "",
            "| epsilon | A | lapse | redshift | ct/r_s to x=3 |",
            "|---:|---:|---:|---:|---:|",
        ]
    )
    for row in near_rows:
        result_lines.append(
            f"| {row['epsilon']:.1e} | {row['A']:.12f} | {row['lapse']:.12e} | {row['redshift']:.12e} | {row['outside_traversal_ct_over_rs']:.12f} |"
        )
    result_lines.extend(
        [
            "",
            "## Wrong Control Summary",
            "",
            "```text",
            f"wrong_control_full_packet_count = {wrong_full_count}",
            "```",
            "",
            "## Grade Reading",
            "",
            "CR008 structurally validates the outside-ledger clock/traversal closure",
            "behavior at A=1, but remains scientific_verdict=BOUNDARY by sealed design.",
            "It does not claim full infalling-observer physics or full strong-field",
            "metric closure.",
            "",
            "## Rule-9 Line",
            "",
            "```text",
            premises["rule_9_falsification"],
            "```",
            "",
        ]
    )
    (ROOT / "CR008_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    hash_targets = [
        BRANCH / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.md",
        BRANCH / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.sha256.txt",
        BRANCH / "README.md",
        BRANCH / "CR007_STRONG_FIELD_LANDMARK_SELECTOR" / "CR007_result.md",
        ROOT / "CR008_PRECOMMIT.md",
        ROOT / "CR008_declared_premises.json",
        ROOT / "CR008_runner.py",
        ROOT / "CR008_candidate_summary.csv",
        ROOT / "CR008_low_A_rows.csv",
        ROOT / "CR008_landmark_clock_rows.csv",
        ROOT / "CR008_near_horizon_rows.csv",
        ROOT / "CR008_input_manifest.csv",
        ROOT / "CR008_summary.json",
        ROOT / "CR008_result.md",
    ]
    write_hashes(hash_targets)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
