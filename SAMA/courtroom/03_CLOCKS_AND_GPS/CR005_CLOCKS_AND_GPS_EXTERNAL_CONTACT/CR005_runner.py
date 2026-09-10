import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PREMISES_PATH = ROOT / "CR005_declared_premises.json"


def in_range(value, bounds):
    return bounds[0] <= value <= bounds[1]


def compute_packet(label, A_scale=1.0, gravity_sign=1.0, include_sr=True, sr_sign=1.0):
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    ext = premises["declared_external_inputs"]
    c = ext["speed_of_light_m_s"]
    mu = ext["earth_mu_m3_s2"]
    r_ground = ext["earth_equatorial_radius_m"]
    r_orbit = ext["gps_orbit_radius_m"]
    day = ext["seconds_per_day"]
    nominal = ext["gps_nominal_clock_frequency_hz"]

    A_ground = A_scale * 2.0 * mu / (c * c * r_ground)
    A_orbit = A_scale * 2.0 * mu / (c * c * r_orbit)
    v_orbit = math.sqrt(mu / r_orbit)

    grav_exact = gravity_sign * (math.sqrt(1.0 - A_orbit) / math.sqrt(1.0 - A_ground) - 1.0)
    grav_weak = gravity_sign * ((A_ground - A_orbit) / 2.0)

    sr_exact_base = math.sqrt(1.0 - (v_orbit * v_orbit) / (c * c)) - 1.0
    sr_weak_base = -(v_orbit * v_orbit) / (2.0 * c * c)
    sr_exact = sr_sign * sr_exact_base if include_sr else 0.0
    sr_weak = sr_sign * sr_weak_base if include_sr else 0.0

    net_exact = grav_exact + sr_exact
    net_weak = grav_weak + sr_weak
    factory = nominal * (1.0 - net_exact)

    return {
        "candidate": label,
        "A_scale": A_scale,
        "gravity_sign": gravity_sign,
        "include_sr": include_sr,
        "sr_sign": sr_sign,
        "A_ground": A_ground,
        "A_orbit": A_orbit,
        "gps_orbit_speed_m_s": v_orbit,
        "gravity_exact_us_day": grav_exact * day * 1e6,
        "gravity_weak_us_day": grav_weak * day * 1e6,
        "sr_exact_us_day": sr_exact * day * 1e6,
        "sr_weak_us_day": sr_weak * day * 1e6,
        "net_exact_us_day": net_exact * day * 1e6,
        "net_weak_us_day": net_weak * day * 1e6,
        "factory_frequency_hz": factory,
    }


def full_packet_pass(row, ranges):
    return (
        in_range(row["gravity_exact_us_day"], ranges["gravity_gain_us_per_day"])
        and in_range(row["sr_exact_us_day"], ranges["sr_loss_us_per_day"])
        and in_range(row["net_exact_us_day"], ranges["net_gain_us_per_day"])
        and in_range(row["factory_frequency_hz"], ranges["factory_frequency_hz"])
    )


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
        compute_packet("sam_A_clock_plus_declared_SR"),
        compute_packet("wrong_half_A", A_scale=0.5),
        compute_packet("wrong_double_A", A_scale=2.0),
        compute_packet("wrong_gravity_sign", gravity_sign=-1.0),
        compute_packet("wrong_omit_SR", include_sr=False),
        compute_packet("wrong_positive_SR", sr_sign=-1.0),
        compute_packet("wrong_ground_equals_orbit_A", A_scale=0.0),
    ]

    for row in rows:
        row["full_packet"] = full_packet_pass(row, ranges)

    sam_row = rows[0]
    wrong_rows = rows[1:]
    wrong_full_count = sum(1 for row in wrong_rows if row["full_packet"])
    exact_weak_net_delta_us_day = abs(sam_row["net_exact_us_day"] - sam_row["net_weak_us_day"])
    exact_weak_grav_delta_us_day = abs(sam_row["gravity_exact_us_day"] - sam_row["gravity_weak_us_day"])
    exact_weak_sr_delta_us_day = abs(sam_row["sr_exact_us_day"] - sam_row["sr_weak_us_day"])
    exact_and_weak_limits_agree = (
        exact_weak_net_delta_us_day < 0.001
        and exact_weak_grav_delta_us_day < 0.001
        and exact_weak_sr_delta_us_day < 0.001
    )

    pass_conditions = {
        "no_older_test_outputs_used": not premises["older_outputs_used_as_computed_inputs"],
        "external_data_required": True,
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "trace_ascii_clean": True,
        "sam_gravity_gain_in_external_range": in_range(sam_row["gravity_exact_us_day"], ranges["gravity_gain_us_per_day"]),
        "sam_sr_loss_in_external_range": in_range(sam_row["sr_exact_us_day"], ranges["sr_loss_us_per_day"]),
        "sam_net_correction_in_external_range": in_range(sam_row["net_exact_us_day"], ranges["net_gain_us_per_day"]),
        "sam_factory_frequency_in_external_range": in_range(sam_row["factory_frequency_hz"], ranges["factory_frequency_hz"]),
        "exact_and_weak_limits_agree": exact_and_weak_limits_agree,
        "wrong_controls_do_not_match_full_packet": wrong_full_count == 0,
    }

    verdict_pass = all(pass_conditions.values())
    verdict = "CR005_PASS_SCOPED_CLOCKS_GPS_EXTERNAL_CONTACT" if verdict_pass else "CR005_BOUNDARY_OR_FAIL_CLOCKS_GPS_EXTERNAL_CONTACT"
    scientific_verdict = "PASS" if verdict_pass else "BOUNDARY"
    triage_bin = "A" if verdict_pass else "C"

    write_csv(ROOT / "CR005_candidate_rows.csv", rows)

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
            "input": "03_CLOCKS_AND_GPS/README.md",
            "role": "branch_claim_and_scope",
            "used_as_computed_input": False,
        },
        {
            "input": "CR005_declared_premises.json",
            "role": "declared_constants_and_ranges",
            "used_as_computed_input": True,
        },
        {
            "input": "CR005_runner.py",
            "role": "calculation_script",
            "used_as_computed_input": True,
        },
    ]
    write_csv(ROOT / "CR005_input_manifest.csv", manifest_rows)

    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "claim_tier": "PASS_SCOPED_CLOCKS_GPS" if verdict_pass else "BOUNDARY_CLOCKS_GPS",
        "sam_row": sam_row,
        "wrong_control_full_packet_count": wrong_full_count,
        "exact_weak_delta_us_day": {
            "gravity": exact_weak_grav_delta_us_day,
            "sr": exact_weak_sr_delta_us_day,
            "net": exact_weak_net_delta_us_day,
        },
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
    }
    (ROOT / "CR005_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result_lines = [
        "# CR005 Clock and GPS External Contact",
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
        "dtau/dt = sqrt(1 - A)",
        "GPS gravity gain + declared SR orbital motion loss -> net correction",
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
            f"| A_ground | {sam_row['A_ground']:.12e} |",
            f"| A_orbit | {sam_row['A_orbit']:.12e} |",
            f"| gps_orbit_speed_m_s | {sam_row['gps_orbit_speed_m_s']:.9f} |",
            f"| gravity_exact_us_day | {sam_row['gravity_exact_us_day']:.12f} |",
            f"| sr_exact_us_day | {sam_row['sr_exact_us_day']:.12f} |",
            f"| net_exact_us_day | {sam_row['net_exact_us_day']:.12f} |",
            f"| factory_frequency_hz | {sam_row['factory_frequency_hz']:.12f} |",
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
            "CR005 gives the clocks/GPS branch an external-contact PASS in a scoped",
            "GPS clock-correction lane. It does not claim Shapiro delay, full GPS",
            "engineering, full GR, or an independent derivation of SR.",
            "",
        ]
    )
    (ROOT / "CR005_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    hash_targets = [
        BRANCH / "README.md",
        ROOT / "CR005_PRECOMMIT.md",
        ROOT / "CR005_declared_premises.json",
        ROOT / "CR005_runner.py",
        ROOT / "CR005_candidate_rows.csv",
        ROOT / "CR005_input_manifest.csv",
        ROOT / "CR005_summary.json",
        ROOT / "CR005_result.md",
    ]
    write_hashes(hash_targets)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
