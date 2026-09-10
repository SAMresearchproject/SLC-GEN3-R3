import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR013_declared_premises.json"


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def write_csv(path, rows):
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_hashes(paths):
    lines = []
    for path in sorted(paths, key=lambda p: str(p).lower()):
        if path.name == "HASHES.txt":
            continue
        lines.append(f"{sha256(path)}  {path.relative_to(REPO) if path.is_relative_to(REPO) else path}")
    (ROOT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rms(values):
    values = list(values)
    return math.sqrt(sum(v * v for v in values) / len(values))


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    sam = premises["sam_inputs"]
    source_path = Path(premises["source_artifact_used_as_data_rows"])
    R = sam["R"]
    D = sam["D"]
    A0 = 1.0 / (math.pi * R)
    c = sam["c_km_s"]

    with source_path.open("r", encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle))

    def A_los(z):
        return A0 * R * (1.0 - (1.0 + z) ** (-D))

    def mu_native(mu_obs, A):
        return mu_obs + 5.0 * math.log10(1.0 - A)

    computed = []
    A_values = [float(row["A_los"]) for row in source_rows]
    median_A = sorted(A_values)[len(A_values) // 2]
    max_A_error = max_c_error = max_distance_error = max_mu_error = 0.0
    for row in source_rows:
        z = float(row["z"])
        mu_obs = float(row["mu_obs"])
        readout = float(row["observed_distance_mpc"])
        A = A_los(z)
        native = readout * (1.0 - A)
        c_eff = c * (1.0 - A)
        mu_n = mu_native(mu_obs, A)
        max_A_error = max(max_A_error, abs(A - float(row["A_los"])))
        max_c_error = max(max_c_error, abs(c_eff - float(row["c_eff_km_s"])))
        max_distance_error = max(max_distance_error, abs(native - float(row["native_distance_mpc"])))
        max_mu_error = max(max_mu_error, abs(mu_n - float(row["mu_native_speed_lane"])))
        computed.append({"z": z, "A_los": A, "weight": float(row["weight"])})

    def wrong_distance(readout, z, mode):
        if mode == "no_shrink":
            return readout
        if mode == "half_A":
            return readout * (1.0 - 0.5 * A_los(z))
        if mode == "constant_median_A":
            return readout * (1.0 - median_A)
        if mode == "D2_power":
            return readout * (1.0 - (1.0 / math.pi) * (1.0 - (1.0 + z) ** -2.0))
        if mode == "linear_z_clipped":
            return readout * (1.0 - min(1.0 / math.pi, z / (1.0 + z)))
        raise ValueError(mode)

    candidate_rows = [
        {
            "candidate": "primary_SN_A_los_ledger",
            "rows": len(source_rows),
            "rms_distance_error_mpc": 0.0,
            "max_distance_error_mpc": max_distance_error,
            "matches_packet": max_distance_error <= 1e-9,
        }
    ]
    for mode in premises["wrong_controls"]:
        errors = []
        for row in source_rows:
            z = float(row["z"])
            readout = float(row["observed_distance_mpc"])
            target = float(row["native_distance_mpc"])
            errors.append(wrong_distance(readout, z, mode) - target)
        candidate_rows.append(
            {
                "candidate": mode,
                "rows": len(source_rows),
                "rms_distance_error_mpc": rms(errors),
                "max_distance_error_mpc": max(abs(v) for v in errors),
                "matches_packet": rms(errors) <= 1e-9,
            }
        )

    low_z = [row["A_los"] for row in computed if row["z"] <= 0.01]
    high_z = [row["A_los"] for row in computed if row["z"] >= 1.0]
    low_z_mean_A = sum(low_z) / len(low_z)
    high_z_mean_A = sum(high_z) / len(high_z)
    wrong_full_count = sum(1 for row in candidate_rows[1:] if row["matches_packet"])
    pass_conditions = {
        "no_older_test_verdicts_used": not premises["older_test_verdicts_used_as_computed_inputs"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "sn_source_rows_present": len(source_rows) >= 1000,
        "bao_inputs_not_loaded": "bao" not in source_path.name.lower(),
        "A_los_row_identity": max_A_error <= 1e-12,
        "c_eff_row_identity": max_c_error <= 1e-9,
        "native_distance_row_identity": max_distance_error <= 1e-9,
        "native_mu_row_identity": max_mu_error <= 1e-9,
        "low_z_shrink_near_zero": low_z_mean_A < 0.01,
        "high_z_shrink_larger_than_low_z": high_z_mean_A > low_z_mean_A,
        "wrong_controls_do_not_match_packet": wrong_full_count == 0,
    }
    verdict_pass = all(pass_conditions.values())
    verdict = "CR013_PASS_SN_LUMINOSITY_LEDGER_SHRINKAGE" if verdict_pass else "CR013_FAIL_SN_LUMINOSITY_LEDGER_SHRINKAGE"

    write_csv(ROOT / "CR013_candidate_rows.csv", candidate_rows)
    write_csv(
        ROOT / "CR013_input_manifest.csv",
        [
            {"input": str(source_path), "role": "source_data_rows", "used_as_computed_input": True},
            {"input": "CR013_declared_premises.json", "role": "declared_formula_controls", "used_as_computed_input": True},
            {"input": "CR013_PRECOMMIT.md", "role": "sealed_pre_run_prediction", "used_as_computed_input": False},
            {"input": "CR013_runner.py", "role": "calculation_script", "used_as_computed_input": True},
        ],
    )
    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS" if verdict_pass else "FAIL",
        "triage_bin": "A" if verdict_pass else "C",
        "claim_tier": "PASS_SN_LUMINOSITY_LEDGER" if verdict_pass else "FAILED_SN_LUMINOSITY_LEDGER",
        "source_rows": len(source_rows),
        "max_A_error": max_A_error,
        "max_c_error_km_s": max_c_error,
        "max_distance_error_mpc": max_distance_error,
        "max_mu_error": max_mu_error,
        "low_z_mean_A": low_z_mean_A,
        "high_z_mean_A": high_z_mean_A,
        "wrong_control_full_packet_count": wrong_full_count,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
    }
    (ROOT / "CR013_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# CR013 SN Luminosity Ledger Shrinkage",
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
        f"scientific_verdict = {summary['scientific_verdict']}",
        f"triage_bin = {summary['triage_bin']}",
        f"claim_tier = {summary['claim_tier']}",
        "```",
        "",
        "## Row Identity Packet",
        "",
        "```text",
        f"rows = {len(source_rows)}",
        f"max_A_error = {max_A_error:.3e}",
        f"max_distance_error_mpc = {max_distance_error:.3e}",
        f"low_z_mean_A = {low_z_mean_A:.12f}",
        f"high_z_mean_A = {high_z_mean_A:.12f}",
        "```",
        "",
        "## Pass Conditions",
        "",
        "| condition | pass |",
        "|---|---:|",
    ]
    for key, value in pass_conditions.items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(["", "## Rule-9 Line", "", "```text", premises["rule_9_falsification"], "```", ""])
    (ROOT / "CR013_result.md").write_text("\n".join(lines), encoding="utf-8")

    write_hashes(
        [
            ROOT / "CR013_declared_premises.json",
            ROOT / "CR013_PRECOMMIT.md",
            ROOT / "CR013_runner.py",
            ROOT / "CR013_candidate_rows.csv",
            ROOT / "CR013_input_manifest.csv",
            ROOT / "CR013_result.md",
            ROOT / "CR013_summary.json",
            source_path,
        ]
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

