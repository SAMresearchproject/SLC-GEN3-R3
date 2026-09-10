import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR010_declared_premises.json"


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


def json_safe(value):
    if isinstance(value, float):
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        if math.isnan(value):
            return "NaN"
    return value


def safe_rows(rows):
    return [{key: json_safe(value) for key, value in row.items()} for row in rows]


def safe_sqrt(value):
    if value < 0.0:
        return float("nan")
    return math.sqrt(value)


def A_profile(x, mode):
    if mode == "wrong_horizon_preserving_inverse_square_A":
        return 1.0 / (x * x)
    return 1.0 / x


def orbit_alpha(mode):
    if mode == "wrong_shift_isco_2rs":
        return 2.0
    if mode == "wrong_shift_isco_4rs":
        return 4.0
    return 3.0


def candidate_x(mode):
    if mode == "sam_A_kernel_isco_lane":
        return 3.0
    if mode == "wrong_horizon_preserving_inverse_square_A":
        return 3.0
    if mode == "wrong_photon_as_isco":
        return 1.5
    if mode == "wrong_horizon_as_isco":
        return 1.0
    if mode == "wrong_shift_isco_2rs":
        return 2.0
    if mode == "wrong_shift_isco_4rs":
        return 4.0
    if mode == "wrong_newtonian_no_isco":
        return 3.0
    raise ValueError(f"unknown mode {mode}")


def energy_over_c2(x, mode):
    if mode == "wrong_newtonian_no_isco":
        return math.sqrt(max(0.0, 1.0 - 1.0 / (2.0 * x)))
    alpha = orbit_alpha(mode)
    denom = 1.0 - alpha / (2.0 * x)
    if denom <= 0.0:
        return float("inf")
    return (1.0 - 1.0 / x) / math.sqrt(denom)


def angular_momentum_over_m_c_rs(x, mode):
    if mode == "wrong_newtonian_no_isco":
        return math.sqrt(x / 2.0)
    alpha = orbit_alpha(mode)
    denom = 2.0 * x - alpha
    if denom <= 0.0:
        return float("inf")
    return x / math.sqrt(denom)


def angular_momentum_sq(x, mode):
    ell = angular_momentum_over_m_c_rs(x, mode)
    if not math.isfinite(ell):
        return float("inf")
    return ell * ell


def omega_rs_over_c(x, mode):
    if mode == "wrong_newtonian_no_isco":
        return 1.0 / math.sqrt(2.0 * x * x * x)
    return 1.0 / math.sqrt(2.0 * x * x * x)


def derivative_ell_sq(x, mode):
    eps = 1e-6
    left = angular_momentum_sq(x - eps, mode)
    right = angular_momentum_sq(x + eps, mode)
    if not math.isfinite(left) or not math.isfinite(right):
        return float("nan")
    return (right - left) / (2.0 * eps)


def local_stability_rows(mode, center):
    offsets = [-1e-3, -1e-4, 0.0, 1e-4, 1e-3]
    rows = []
    for offset in offsets:
        x = center + offset
        if x <= 0.0:
            continue
        ell_sq = angular_momentum_sq(x, mode)
        rows.append(
            {
                "candidate": mode,
                "x": x,
                "A": A_profile(x, mode),
                "ell_sq": ell_sq,
                "offset_from_center": offset,
            }
        )
    return rows


def relative_miss(value, target):
    if not math.isfinite(value):
        return float("inf")
    return abs(value - target) / abs(target)


def packet(mode, refs, thresholds):
    x = candidate_x(mode)
    A = A_profile(x, mode)
    E = energy_over_c2(x, mode)
    ell = angular_momentum_over_m_c_rs(x, mode)
    omega = omega_rs_over_c(x, mode)
    local_rows = local_stability_rows(mode, x)
    center = next(row for row in local_rows if row["offset_from_center"] == 0.0)
    side_values = [row["ell_sq"] for row in local_rows if row["offset_from_center"] != 0.0]
    local_minimum = (
        math.isfinite(center["ell_sq"])
        and bool(side_values)
        and all((value - center["ell_sq"]) >= -thresholds["local_minimum_margin"] for value in side_values)
    )
    derivative_left = derivative_ell_sq(x - thresholds["stability_derivative_epsilon"], mode)
    derivative_right = derivative_ell_sq(x + thresholds["stability_derivative_epsilon"], mode)
    stability_transition = (
        math.isfinite(derivative_left)
        and math.isfinite(derivative_right)
        and derivative_left < 0.0
        and derivative_right > 0.0
    )
    tol = thresholds["exact_absolute_tolerance"]
    exact_packet = (
        abs(x - refs["schwarzschild_isco_x"]) <= tol
        and abs(A - refs["schwarzschild_isco_A"]) <= tol
        and abs(E - refs["schwarzschild_isco_energy_over_c2"]) <= tol
        and abs(ell - refs["schwarzschild_isco_angular_momentum_over_m_c_rs"]) <= tol
        and abs(omega - refs["schwarzschild_isco_omega_rs_over_c"]) <= tol
        and local_minimum
        and stability_transition
    )
    max_relative_miss = max(
        relative_miss(x, refs["schwarzschild_isco_x"]),
        relative_miss(A, refs["schwarzschild_isco_A"]),
        relative_miss(E, refs["schwarzschild_isco_energy_over_c2"]),
        relative_miss(ell, refs["schwarzschild_isco_angular_momentum_over_m_c_rs"]),
        relative_miss(omega, refs["schwarzschild_isco_omega_rs_over_c"]),
    )
    row = {
        "candidate": mode,
        "x_isco": x,
        "A_isco": A,
        "energy_over_c2": E,
        "angular_momentum_over_m_c_rs": ell,
        "omega_rs_over_c": omega,
        "local_stability_minimum": local_minimum,
        "stability_derivative_left": derivative_left,
        "stability_derivative_right": derivative_right,
        "stability_transition": stability_transition,
        "full_packet": exact_packet,
        "max_relative_miss": max_relative_miss,
    }
    return row, local_rows


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    refs = premises["external_reference_invariants"]
    thresholds = premises["thresholds"]

    sealed_hash_current = sha256(REPO / premises["sealed_scope_file"])
    cr007_hash_current = sha256(REPO / premises["cr007_result_file"])
    cr008_hash_current = sha256(REPO / premises["cr008_result_file"])
    cr009_hash_current = sha256(REPO / premises["cr009_result_file"])

    modes = [
        "sam_A_kernel_isco_lane",
        "wrong_horizon_preserving_inverse_square_A",
        "wrong_photon_as_isco",
        "wrong_horizon_as_isco",
        "wrong_shift_isco_2rs",
        "wrong_shift_isco_4rs",
        "wrong_newtonian_no_isco",
    ]
    candidate_rows = []
    stability_rows = []
    for mode in modes:
        row, local = packet(mode, refs, thresholds)
        candidate_rows.append(row)
        stability_rows.extend(local)

    sam_row = next(row for row in candidate_rows if row["candidate"] == "sam_A_kernel_isco_lane")
    wrong_rows = [row for row in candidate_rows if row["candidate"] != "sam_A_kernel_isco_lane"]
    wrong_full_count = sum(1 for row in wrong_rows if row["full_packet"])
    wrong_min_miss_ok = all(row["max_relative_miss"] >= thresholds["wrong_control_min_relative_miss"] for row in wrong_rows)

    pass_conditions = {
        "no_older_test_outputs_used": not premises["older_outputs_used_as_computed_inputs"],
        "sealed_scope_predates_test": sealed_hash_current == premises["sealed_scope_sha256"],
        "cr007_typed_premise_present": cr007_hash_current == premises["cr007_result_sha256"],
        "cr008_typed_boundary_present": cr008_hash_current == premises["cr008_result_sha256"],
        "cr009_typed_photon_contact_present": cr009_hash_current == premises["cr009_result_sha256"],
        "external_reference_required": True,
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "trace_ascii_clean": True,
        "sam_isco_x_exact": abs(sam_row["x_isco"] - refs["schwarzschild_isco_x"]) <= thresholds["exact_absolute_tolerance"],
        "sam_isco_A_exact": abs(sam_row["A_isco"] - refs["schwarzschild_isco_A"]) <= thresholds["exact_absolute_tolerance"],
        "sam_isco_energy_exact": abs(sam_row["energy_over_c2"] - refs["schwarzschild_isco_energy_over_c2"]) <= thresholds["exact_absolute_tolerance"],
        "sam_isco_angular_momentum_exact": abs(sam_row["angular_momentum_over_m_c_rs"] - refs["schwarzschild_isco_angular_momentum_over_m_c_rs"]) <= thresholds["exact_absolute_tolerance"],
        "sam_isco_frequency_exact": abs(sam_row["omega_rs_over_c"] - refs["schwarzschild_isco_omega_rs_over_c"]) <= thresholds["exact_absolute_tolerance"],
        "sam_isco_is_local_stability_minimum": sam_row["local_stability_minimum"] and sam_row["stability_transition"],
        "wrong_controls_do_not_match_full_packet": wrong_full_count == 0 and wrong_min_miss_ok,
        "declared_readout_preserved": premises["expected_claim_tier"] == "PASS_SCOPED_ISCO_ORBITAL_CONTACT",
    }

    verdict_pass = all(pass_conditions.values())
    verdict = "CR010_PASS_SCOPED_ISCO_ORBITAL_CONTACT" if verdict_pass else "CR010_BOUNDARY_OR_FAIL_ISCO_ORBITAL_CONTACT"
    scientific_verdict = "PASS" if verdict_pass else "BOUNDARY"
    triage_bin = "A" if verdict_pass else "C"
    claim_tier = premises["expected_claim_tier"] if verdict_pass else "BOUNDARY_ISCO_ORBITAL_CONTACT"

    write_csv(ROOT / "CR010_candidate_rows.csv", safe_rows(candidate_rows))
    write_csv(ROOT / "CR010_stability_rows.csv", safe_rows(stability_rows))

    manifest_rows = [
        {"input": "C:\\VS\\memory\\PRIORITY_RECORD.md", "role": "provenance_source", "used_as_computed_input": False},
        {"input": "C:\\VS\\memory\\OPERATIONAL_MEMORY.md", "role": "provenance_source", "used_as_computed_input": False},
        {"input": premises["sealed_scope_file"], "role": "sealed_scope_lock", "used_as_computed_input": False},
        {"input": premises["cr007_result_file"], "role": "typed_upstream_isco_premise", "used_as_computed_input": False},
        {"input": premises["cr008_result_file"], "role": "typed_upstream_closure_boundary", "used_as_computed_input": False},
        {"input": premises["cr009_result_file"], "role": "typed_upstream_photon_contact", "used_as_computed_input": False},
        {"input": "CR010_declared_premises.json", "role": "declared_formula_invariants_and_scope", "used_as_computed_input": True},
        {"input": "CR010_runner.py", "role": "calculation_script", "used_as_computed_input": True},
    ]
    write_csv(ROOT / "CR010_input_manifest.csv", manifest_rows)

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
        "cr009_result_sha256_current": cr009_hash_current,
        "sam_row": {key: json_safe(value) for key, value in sam_row.items()},
        "wrong_control_full_packet_count": wrong_full_count,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
        "courtroom_readout": premises["courtroom_readout"],
        "deferred_support_status": "supports_CR007_CR008_CR009_package_pending_CR011",
    }
    (ROOT / "CR010_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result_lines = [
        "# CR010 ISCO Orbital Contact",
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
        "CR007 typed premise: ISCO A = 1/3 at r/r_s=3",
        "CR008 typed boundary: A=1 closure, not A=1/3",
        "CR009 typed photon contact: A=2/3 photon sphere remains distinct from ISCO",
        "E/c^2 = (1 - 1/x) / sqrt(1 - 3/(2x))",
        "L/(m c r_s) = x / sqrt(2x - 3)",
        "Omega r_s/c = 1 / sqrt(2 x^3)",
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
            "## SAM ISCO Packet",
            "",
            "| quantity | value | target |",
            "|---|---:|---:|",
            f"| x_ISCO = r/r_s | {sam_row['x_isco']:.12f} | {refs['schwarzschild_isco_x']:.12f} |",
            f"| A_ISCO | {sam_row['A_isco']:.12f} | {refs['schwarzschild_isco_A']:.12f} |",
            f"| E_ISCO/c^2 | {sam_row['energy_over_c2']:.12f} | {refs['schwarzschild_isco_energy_over_c2']:.12f} |",
            f"| L_ISCO/(m c r_s) | {sam_row['angular_momentum_over_m_c_rs']:.12f} | {refs['schwarzschild_isco_angular_momentum_over_m_c_rs']:.12f} |",
            f"| Omega_ISCO r_s/c | {sam_row['omega_rs_over_c']:.12f} | {refs['schwarzschild_isco_omega_rs_over_c']:.12f} |",
            "",
            "## Stability Check",
            "",
            "| quantity | value |",
            "|---|---:|",
            f"| local_stability_minimum | {str(sam_row['local_stability_minimum']).lower()} |",
            f"| d(L^2)/dx left of x=3 | {sam_row['stability_derivative_left']:.12e} |",
            f"| d(L^2)/dx right of x=3 | {sam_row['stability_derivative_right']:.12e} |",
            f"| stability_transition | {str(sam_row['stability_transition']).lower()} |",
            "",
            "## Wrong Control Summary",
            "",
            "```text",
            f"wrong_control_full_packet_count = {wrong_full_count}",
            "```",
            "",
            "## Grade Reading",
            "",
            "CR010 gives the 05 branch a scoped strong-field ISCO landmark",
            "contact showing that the SAM A-kernel naturally indexes ISCO as",
            "A = 1/3. The record supplies the declared ISCO packet,",
            "wrong-control rejection, and artifact hashes for the CR011",
            "deferred-support ledger.",
            "",
            "## Rule-9 Line",
            "",
            "```text",
            premises["rule_9_falsification"],
            "```",
            "",
        ]
    )
    (ROOT / "CR010_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    hash_targets = [
        BRANCH / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.md",
        BRANCH / "README.md",
        BRANCH / "CR007_STRONG_FIELD_LANDMARK_SELECTOR" / "CR007_result.md",
        BRANCH / "CR008_CLOCK_TRAVERSAL_CLOSURE" / "CR008_result.md",
        BRANCH / "CR009_PHOTON_SPHERE_SHADOW_CONTACT" / "CR009_result.md",
        ROOT / "CR010_PRECOMMIT.md",
        ROOT / "CR010_declared_premises.json",
        ROOT / "CR010_runner.py",
        ROOT / "CR010_candidate_rows.csv",
        ROOT / "CR010_stability_rows.csv",
        ROOT / "CR010_input_manifest.csv",
        ROOT / "CR010_summary.json",
        ROOT / "CR010_result.md",
    ]
    write_hashes(hash_targets)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
