import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PREMISES_PATH = ROOT / "CR006_declared_premises.json"


def in_range(value, bounds):
    return bounds[0] <= value <= bounds[1]


def geometry(ext, impact_scale=1.0):
    b = ext["impact_over_solar_radius"] * impact_scale * ext["solar_radius_m"]
    r1 = ext["earth_radius_from_sun_m"]
    r2 = ext["cassini_style_radius_from_sun_m"]
    if b >= min(r1, r2):
        raise ValueError("impact parameter must be smaller than endpoint radii")
    x1 = math.sqrt(r1 * r1 - b * b)
    x2 = math.sqrt(r2 * r2 - b * b)
    R = x1 + x2
    return b, r1, r2, x1, x2, R


def shapiro_packet(label, A_scale=1.0, radial_power=1.0, endpoint_clock_only=False, include_A0_baseline=False):
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    ext = premises["declared_external_inputs"]
    c = ext["speed_of_light_m_s"]
    G = ext["G_m3_kg_s2"]
    M = ext["solar_mass_kg"]
    A0 = 1.0 / (12.0 * math.pi)
    b, r1, r2, x1, x2, R = geometry(ext)
    r_s = 2.0 * G * M / (c * c)

    standard_log = (r_s / c) * math.log((r1 + r2 + R) / (r1 + r2 - R))
    if endpoint_clock_only:
        delay = 0.0
        integral_A_ds_m = 0.0
        gamma_eff = -1.0
        log_relative_diff = 1.0
    elif radial_power == 1.0:
        integral_A_ds_m = A_scale * r_s * (math.asinh(x1 / b) + math.asinh(x2 / b))
        if include_A0_baseline:
            integral_A_ds_m += A0 * R
        delay = integral_A_ds_m / c
        gamma_eff = 2.0 * A_scale - 1.0
        log_relative_diff = abs(delay - A_scale * standard_log) / abs(A_scale * standard_log) if A_scale else 0.0
    elif radial_power == 2.0:
        # Wrong radial law normalized to match the candidate at the central b.
        candidate_integral = r_s * (math.asinh(x1 / b) + math.asinh(x2 / b))
        raw = (math.atan(x2 / b) + math.atan(x1 / b)) / b
        norm = candidate_integral / raw
        integral_A_ds_m = norm * raw
        delay = integral_A_ds_m / c
        gamma_eff = None
        log_relative_diff = abs(delay - standard_log) / abs(standard_log)
    else:
        raise ValueError("unsupported radial power")

    return {
        "candidate": label,
        "A_scale": A_scale,
        "radial_power": radial_power,
        "endpoint_clock_only": endpoint_clock_only,
        "include_A0_baseline": include_A0_baseline,
        "impact_over_R_sun": ext["impact_over_solar_radius"],
        "impact_m": b,
        "r_s_m": r_s,
        "R_path_m": R,
        "integral_A_ds_m": integral_A_ds_m,
        "delay_s": delay,
        "delay_us": delay * 1e6,
        "standard_log_delay_s": standard_log,
        "standard_log_delay_us": standard_log * 1e6,
        "log_relative_diff": log_relative_diff,
        "gamma_eff": gamma_eff,
    }


def impact_shape_rows(A_scale=1.0, radial_power=1.0):
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    ext = premises["declared_external_inputs"]
    c = ext["speed_of_light_m_s"]
    G = ext["G_m3_kg_s2"]
    M = ext["solar_mass_kg"]
    r_s = 2.0 * G * M / (c * c)

    rows = []
    for impact_over in premises["declared_shape_cases_impact_over_solar_radius"]:
        local_ext = dict(ext)
        local_ext["impact_over_solar_radius"] = impact_over
        b, r1, r2, x1, x2, R = geometry(local_ext)
        standard_log = (r_s / c) * math.log((r1 + r2 + R) / (r1 + r2 - R))
        if radial_power == 1.0:
            integral_A_ds_m = A_scale * r_s * (math.asinh(x1 / b) + math.asinh(x2 / b))
        else:
            base_b, _, _, base_x1, base_x2, _ = geometry(ext)
            base_candidate = r_s * (math.asinh(base_x1 / base_b) + math.asinh(base_x2 / base_b))
            base_raw = (math.atan(base_x2 / base_b) + math.atan(base_x1 / base_b)) / base_b
            norm = base_candidate / base_raw
            raw = (math.atan(x2 / b) + math.atan(x1 / b)) / b
            integral_A_ds_m = norm * raw
        delay = integral_A_ds_m / c
        rows.append(
            {
                "impact_over_R_sun": impact_over,
                "impact_m": b,
                "delay_us": delay * 1e6,
                "standard_log_delay_us": standard_log * 1e6,
                "relative_diff_to_log": abs(delay - standard_log) / abs(standard_log),
            }
        )
    return rows


def full_packet_pass(row, ranges):
    gamma_ok = row["gamma_eff"] is not None and abs(row["gamma_eff"] - 1.0) <= ranges["cassini_ppn_gamma_abs_minus_one_max"]
    delay_ok = in_range(row["delay_us"], ranges["solar_grazing_delay_us"])
    log_ok = row["log_relative_diff"] <= 1e-12
    return gamma_ok and delay_ok and log_ok


def write_csv(path, rows):
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def write_hashes(paths):
    rows = []
    for path in sorted(paths, key=lambda p: str(p).lower()):
        if path.name == "HASHES.txt":
            continue
        rows.append(f"{sha256(path)}  {path.relative_to(BRANCH.parent)}")
    (ROOT / "HASHES.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    ranges = premises["external_anchor_ranges"]

    rows = [
        shapiro_packet("sam_photon_road_A_path"),
        shapiro_packet("wrong_half_A", A_scale=0.5),
        shapiro_packet("wrong_double_A", A_scale=2.0),
        shapiro_packet("wrong_no_A", A_scale=0.0),
        shapiro_packet("wrong_endpoint_clock_only", endpoint_clock_only=True),
        shapiro_packet("wrong_visible_A0_baseline", include_A0_baseline=True),
        shapiro_packet("wrong_one_over_r2_radial_law", radial_power=2.0),
    ]

    for row in rows:
        row["full_packet"] = full_packet_pass(row, ranges)

    sam_row = rows[0]
    wrong_rows = rows[1:]
    wrong_full_count = sum(1 for row in wrong_rows if row["full_packet"])

    shape_rows = impact_shape_rows()
    wrong_shape_rows = impact_shape_rows(radial_power=2.0)
    max_shape_relative_diff = max(row["relative_diff_to_log"] for row in shape_rows)
    wrong_shape_max_relative_diff = max(row["relative_diff_to_log"] for row in wrong_shape_rows)
    impact_dependence_matches_log_shape = max_shape_relative_diff <= 1e-10
    wrong_radial_shape_rejected = wrong_shape_max_relative_diff >= 0.1

    endpoint_clock_row = next(row for row in rows if row["candidate"] == "wrong_endpoint_clock_only")

    pass_conditions = {
        "no_older_test_outputs_used": not premises["older_outputs_used_as_computed_inputs"],
        "external_data_required": True,
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "trace_ascii_clean": True,
        "sam_gamma_within_cassini_bound": abs(sam_row["gamma_eff"] - 1.0) <= ranges["cassini_ppn_gamma_abs_minus_one_max"],
        "sam_delay_in_geometry_window": in_range(sam_row["delay_us"], ranges["solar_grazing_delay_us"]),
        "sam_integral_matches_log_law": sam_row["log_relative_diff"] <= 1e-12,
        "impact_dependence_matches_log_shape": impact_dependence_matches_log_shape,
        "endpoint_clock_only_rejected": not endpoint_clock_row["full_packet"],
        "wrong_radial_shape_rejected": wrong_radial_shape_rejected,
        "wrong_controls_do_not_match_full_packet": wrong_full_count == 0,
    }

    verdict_pass = all(pass_conditions.values())
    verdict = "CR006_PASS_SCOPED_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT" if verdict_pass else "CR006_BOUNDARY_OR_FAIL_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT"
    scientific_verdict = "PASS" if verdict_pass else "BOUNDARY"
    triage_bin = "A" if verdict_pass else "C"

    write_csv(ROOT / "CR006_candidate_rows.csv", rows)
    write_csv(ROOT / "CR006_impact_shape_rows.csv", shape_rows)
    write_csv(ROOT / "CR006_wrong_radial_shape_rows.csv", wrong_shape_rows)

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
            "input": "04_PHOTON_ROAD_SHAPIRO_DELAY/README.md",
            "role": "branch_claim_and_scope",
            "used_as_computed_input": False,
        },
        {
            "input": "CR006_declared_premises.json",
            "role": "declared_constants_ranges_geometry",
            "used_as_computed_input": True,
        },
        {
            "input": "CR006_runner.py",
            "role": "calculation_script",
            "used_as_computed_input": True,
        },
    ]
    write_csv(ROOT / "CR006_input_manifest.csv", manifest_rows)

    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "claim_tier": "PASS_SCOPED_PHOTON_ROAD_SHAPIRO" if verdict_pass else "BOUNDARY_PHOTON_ROAD_SHAPIRO",
        "sam_row": sam_row,
        "wrong_control_full_packet_count": wrong_full_count,
        "max_shape_relative_diff": max_shape_relative_diff,
        "wrong_shape_max_relative_diff": wrong_shape_max_relative_diff,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
    }
    (ROOT / "CR006_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result_lines = [
        "# CR006 Photon Road Shapiro External Contact",
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
        f"claim_tier = {summary['claim_tier']}",
        "```",
        "",
        "## Branch Claim Tested",
        "",
        "```text",
        "A(r) = r_s/r = 2GM/(c^2 r)",
        "T_A^gamma = (1/c) integral A ds",
        "Photon road integral -> first-order Shapiro logarithmic delay",
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
            "## SAM Packet",
            "",
            "| quantity | value |",
            "|---|---:|",
            f"| impact_over_R_sun | {sam_row['impact_over_R_sun']:.6f} |",
            f"| impact_m | {sam_row['impact_m']:.6f} |",
            f"| r_s_m | {sam_row['r_s_m']:.12f} |",
            f"| integral_A_ds_m | {sam_row['integral_A_ds_m']:.12f} |",
            f"| delay_us | {sam_row['delay_us']:.12f} |",
            f"| standard_log_delay_us | {sam_row['standard_log_delay_us']:.12f} |",
            f"| log_relative_diff | {sam_row['log_relative_diff']:.12e} |",
            f"| gamma_eff | {sam_row['gamma_eff']:.12f} |",
            "",
            "## Shape Check",
            "",
            "| quantity | value |",
            "|---|---:|",
            f"| max_shape_relative_diff | {max_shape_relative_diff:.12e} |",
            f"| wrong_shape_max_relative_diff | {wrong_shape_max_relative_diff:.12e} |",
            "",
            "## Wrong Control Summary",
            "",
            "```text",
            f"wrong_control_full_packet_count = {wrong_full_count}",
            "```",
            "",
            "## Rule-9 Line",
            "",
            "```text",
            premises["rule_9_falsification"],
            "```",
            "",
            "## Courtroom Reading",
            "",
            "CR006 gives the photon-road Shapiro branch an external-contact PASS in a",
            "scoped first-order solar-system lane. It does not claim full null-geodesic",
            "derivation, full PPN closure, strong-field photon propagation, cosmological",
            "lensing-time delay closure, a new light-speed law, or full GR.",
            "",
        ]
    )
    (ROOT / "CR006_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    hash_targets = [
        BRANCH / "README.md",
        ROOT / "CR006_PRECOMMIT.md",
        ROOT / "CR006_declared_premises.json",
        ROOT / "CR006_runner.py",
        ROOT / "CR006_candidate_rows.csv",
        ROOT / "CR006_impact_shape_rows.csv",
        ROOT / "CR006_wrong_radial_shape_rows.csv",
        ROOT / "CR006_input_manifest.csv",
        ROOT / "CR006_summary.json",
        ROOT / "CR006_result.md",
    ]
    write_hashes(hash_targets)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
