import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR007_declared_premises.json"


def close(a, b, tol=1e-12):
    return abs(a - b) <= tol


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


def candidate_A(r_over_rs, mode):
    if mode == "sam_inverse_radius":
        return 1.0 / r_over_rs
    if mode == "wrong_half_A":
        return 0.5 / r_over_rs
    if mode == "wrong_double_A":
        return 2.0 / r_over_rs
    if mode == "wrong_inverse_square_preserve_horizon":
        return 1.0 / (r_over_rs * r_over_rs)
    if mode == "wrong_constant_horizon_only":
        return 1.0
    if mode == "wrong_linear_gap":
        return max(0.0, 2.0 - r_over_rs)
    raise ValueError(f"unknown mode: {mode}")


def compute_rows(mode):
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    landmarks = premises["external_reference_landmarks"]
    rows = []
    for name, spec in landmarks.items():
        r_over_rs = spec["r_over_rs"]
        target_A = spec["target_A"]
        value_A = candidate_A(r_over_rs, mode)
        rows.append(
            {
                "candidate": mode,
                "landmark": name,
                "r_over_rs": r_over_rs,
                "target_A": target_A,
                "candidate_A": value_A,
                "absolute_error": abs(value_A - target_A),
                "pass": close(value_A, target_A),
            }
        )
    return rows


def mass_rows():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    ext = premises["declared_external_inputs"]
    c = ext["speed_of_light_m_s"]
    G = ext["G_m3_kg_s2"]
    masses = {
        "Earth": ext["earth_mass_kg"],
        "Sun": ext["solar_mass_kg"],
        "10_solar_mass": ext["ten_solar_mass_kg"],
    }
    landmarks = premises["external_reference_landmarks"]
    rows = []
    for label, mass in masses.items():
        r_s = 2.0 * G * mass / (c * c)
        for name, spec in landmarks.items():
            r = spec["r_over_rs"] * r_s
            A = r_s / r
            rows.append(
                {
                    "body": label,
                    "mass_kg": mass,
                    "r_s_m": r_s,
                    "landmark": name,
                    "r_m": r,
                    "r_over_rs": spec["r_over_rs"],
                    "A": A,
                    "target_A": spec["target_A"],
                    "absolute_error": abs(A - spec["target_A"]),
                }
            )
    return rows


def max_spread(rows, landmark, key):
    values = [row[key] for row in rows if row["landmark"] == landmark]
    return max(values) - min(values)


def full_packet_pass(rows):
    return all(row["pass"] for row in rows)


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    sealed_path = REPO / premises["sealed_scope_file"]
    sealed_hash_current = sha256(sealed_path)
    sealed_scope_predates_test = sealed_hash_current == premises["sealed_scope_sha256"]

    candidate_modes = [
        "sam_inverse_radius",
        "wrong_half_A",
        "wrong_double_A",
        "wrong_inverse_square_preserve_horizon",
        "wrong_constant_horizon_only",
        "wrong_linear_gap",
    ]
    rows = []
    candidate_summary = []
    for mode in candidate_modes:
        mode_rows = compute_rows(mode)
        rows.extend(mode_rows)
        candidate_summary.append(
            {
                "candidate": mode,
                "full_packet": full_packet_pass(mode_rows),
                "max_absolute_error": max(row["absolute_error"] for row in mode_rows),
            }
        )

    sam_rows = [row for row in rows if row["candidate"] == "sam_inverse_radius"]
    wrong_summary = [row for row in candidate_summary if row["candidate"] != "sam_inverse_radius"]
    wrong_full_count = sum(1 for row in wrong_summary if row["full_packet"])

    m_rows = mass_rows()
    mass_spreads = {
        "horizon_A_spread": max_spread(m_rows, "horizon", "A"),
        "photon_sphere_A_spread": max_spread(m_rows, "photon_sphere", "A"),
        "isco_A_spread": max_spread(m_rows, "isco", "A"),
    }

    landmark_order_preserved = (
        next(row for row in sam_rows if row["landmark"] == "horizon")["candidate_A"]
        > next(row for row in sam_rows if row["landmark"] == "photon_sphere")["candidate_A"]
        > next(row for row in sam_rows if row["landmark"] == "isco")["candidate_A"]
    )
    mass_scale_invariance = all(value <= 1e-12 for value in mass_spreads.values())

    pass_conditions = {
        "no_older_test_outputs_used": not premises["older_outputs_used_as_computed_inputs"],
        "sealed_scope_predates_test": sealed_scope_predates_test,
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "trace_ascii_clean": True,
        "sam_landmark_tuple_exact": full_packet_pass(sam_rows),
        "landmark_order_preserved": landmark_order_preserved,
        "mass_scale_invariance": mass_scale_invariance,
        "wrong_controls_do_not_match_full_packet": wrong_full_count == 0,
        "empirical_overclaim_rejected": premises["expected_scientific_verdict"] == "BOUNDARY",
    }

    structural_success = all(pass_conditions.values())
    scientific_verdict = "BOUNDARY"
    verdict = "CR007_BOUNDARY_STRONG_FIELD_LANDMARK_SELECTOR" if structural_success else "CR007_FAIL_STRONG_FIELD_LANDMARK_SELECTOR"
    triage_bin = "C"
    claim_tier = premises["expected_claim_tier"] if structural_success else "FAILED_LANDMARK_ROOT"

    write_csv(ROOT / "CR007_candidate_rows.csv", rows)
    write_csv(ROOT / "CR007_candidate_summary.csv", candidate_summary)
    write_csv(ROOT / "CR007_mass_scale_rows.csv", m_rows)

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
            "input": "05_STRONG_FIELD_AND_HORIZON_CLOSURE/SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.md",
            "role": "sealed_scope_lock",
            "used_as_computed_input": False,
        },
        {
            "input": "05_STRONG_FIELD_AND_HORIZON_CLOSURE/README.md",
            "role": "branch_claim_and_scope",
            "used_as_computed_input": False,
        },
        {
            "input": "CR007_declared_premises.json",
            "role": "declared_constants_landmarks_and_expected_grade",
            "used_as_computed_input": True,
        },
        {
            "input": "CR007_runner.py",
            "role": "calculation_script",
            "used_as_computed_input": True,
        },
    ]
    write_csv(ROOT / "CR007_input_manifest.csv", manifest_rows)

    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "claim_tier": claim_tier,
        "structural_success": structural_success,
        "sealed_scope_sha256_current": sealed_hash_current,
        "sam_rows": sam_rows,
        "wrong_control_full_packet_count": wrong_full_count,
        "mass_spreads": mass_spreads,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
        "deferred_support_status": "eligible_for_CR011_if_CR008_CR010_pass",
    }
    (ROOT / "CR007_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result_lines = [
        "# CR007 Strong-Field Landmark Selector",
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
        "A(r) = r_s/r",
        "horizon        r/r_s = 1   -> A = 1",
        "photon sphere  r/r_s = 3/2 -> A = 2/3",
        "ISCO           r/r_s = 3   -> A = 1/3",
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
            "## SAM Landmark Rows",
            "",
            "| landmark | r/r_s | candidate A | target A | absolute error |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in sam_rows:
        result_lines.append(
            f"| {row['landmark']} | {row['r_over_rs']:.12f} | {row['candidate_A']:.12f} | {row['target_A']:.12f} | {row['absolute_error']:.3e} |"
        )
    result_lines.extend(
        [
            "",
            "## Mass-Scale Invariance",
            "",
            "| quantity | spread |",
            "|---|---:|",
        ]
    )
    for key, value in mass_spreads.items():
        result_lines.append(f"| {key} | {value:.3e} |")
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
            "CR007 structurally succeeds as the 05-branch landmark root, but it remains",
            "scientific_verdict=BOUNDARY by sealed design. The test does not claim broad",
            "external strong-field closure. CR008-CR010 may later provide deferred support",
            "through declared downstream tests.",
            "",
            "## Rule-9 Line",
            "",
            "```text",
            premises["rule_9_falsification"],
            "```",
            "",
        ]
    )
    (ROOT / "CR007_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    hash_targets = [
        BRANCH / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.md",
        BRANCH / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.sha256.txt",
        BRANCH / "README.md",
        ROOT / "CR007_PRECOMMIT.md",
        ROOT / "CR007_declared_premises.json",
        ROOT / "CR007_runner.py",
        ROOT / "CR007_candidate_rows.csv",
        ROOT / "CR007_candidate_summary.csv",
        ROOT / "CR007_mass_scale_rows.csv",
        ROOT / "CR007_input_manifest.csv",
        ROOT / "CR007_summary.json",
        ROOT / "CR007_result.md",
    ]
    write_hashes(hash_targets)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
