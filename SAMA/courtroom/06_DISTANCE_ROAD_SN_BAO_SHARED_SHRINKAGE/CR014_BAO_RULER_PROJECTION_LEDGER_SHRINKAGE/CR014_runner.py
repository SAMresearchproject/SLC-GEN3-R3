import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR014_declared_premises.json"


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
        try:
            label = path.relative_to(REPO)
        except ValueError:
            label = path
        lines.append(f"{sha256(path)}  {label}")
    (ROOT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def close(a, b, tol=1e-12):
    return abs(a - b) <= tol


def rms(values):
    values = list(values)
    return math.sqrt(sum(v * v for v in values) / len(values))


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    source_path = Path(premises["source_artifact_used_as_data_rows"])
    sam = premises["sam_inputs"]
    R = sam["R"]
    D = sam["D"]
    A0 = 1.0 / (math.pi * R)
    omega_b = sam["Omega_b"]
    omega_pbh = sam["Omega_BB_PBH_trapped"]
    w = (D / R) * (omega_b / omega_pbh)
    with source_path.open("r", encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["model"] == "PRIMARY_G716C_A_SHELL_SELECTOR"]

    def declared_symbol_value(symbol):
        symbol = symbol.strip()
        if symbol == "0":
            return 0.0
        if symbol == "-w":
            return -w
        if symbol == "+w":
            return w
        if symbol == "-2w":
            return -2.0 * w
        if symbol == "-A0":
            return -A0
        return float(symbol)

    def window_for(row, mode):
        declared = float(row["window_value"])
        if mode == "primary":
            return declared
        if mode == "no_window":
            return 0.0
        if mode == "half_window":
            return 0.5 * declared
        if mode == "sign_flipped_window":
            return -declared
        if mode == "all_minus_w":
            return -w
        if mode == "phi_power_window":
            return math.copysign(abs(declared) ** R, declared)
        raise ValueError(mode)

    def score(mode):
        predicted_non_fap = {}
        predicted_rows = []
        for row in rows:
            key = (row["tracer"], row["z"])
            obs = row["observable"]
            win = window_for(row, mode)
            if obs != "F_AP_DM_over_DH":
                predicted = float(row["base_predicted"]) * (1.0 + win)
                predicted_non_fap[(key, obs)] = predicted
            else:
                predicted = None
            predicted_rows.append((row, win, predicted))
        out = []
        pulls = []
        for row, win, predicted in predicted_rows:
            key = (row["tracer"], row["z"])
            if row["observable"] == "F_AP_DM_over_DH":
                dm = predicted_non_fap.get((key, "DM_over_rd"))
                dh = predicted_non_fap.get((key, "DH_over_rd"))
                predicted = dm / dh if dm is not None and dh is not None else float(row["base_predicted"])
            observed = float(row["observed"])
            sigma = float(row["sigma"])
            pull = (predicted - observed) / sigma
            pulls.append(pull)
            out.append(
                {
                    "tracer": row["tracer"],
                    "z": float(row["z"]),
                    "observable": row["observable"],
                    "window_symbol": row["window_symbol"],
                    "window_value": win,
                    "predicted_recomputed": predicted,
                    "windowed_predicted_source": float(row["windowed_predicted"]),
                    "prediction_error": predicted - float(row["windowed_predicted"]),
                    "pull_recomputed": pull,
                    "abs_pull_recomputed": abs(pull),
                }
            )
        return out, {
            "candidate": mode,
            "rows": len(out),
            "rms_pull": rms(pulls),
            "max_abs_pull": max(abs(p) for p in pulls),
            "rows_over_3sigma": sum(1 for p in pulls if abs(p) > 3.0),
            "max_prediction_error": max(abs(row["prediction_error"]) for row in out),
        }

    primary_rows, primary_score = score("primary")
    candidate_rows = [primary_score | {"matches_packet": primary_score["max_prediction_error"] <= 1e-9}]
    for mode in premises["wrong_controls"]:
        _, score_row = score(mode)
        score_row["matches_packet"] = score_row["max_prediction_error"] <= 1e-9
        candidate_rows.append(score_row)

    non_fap_keys = {(row["tracer"], row["z"], row["observable"]) for row in primary_rows if row["observable"] != "F_AP_DM_over_DH"}
    f_ap_rows = [row for row in primary_rows if row["observable"] == "F_AP_DM_over_DH"]
    f_ap_derived = all(
        (row["tracer"], row["z"], "DM_over_rd") in non_fap_keys and (row["tracer"], row["z"], "DH_over_rd") in non_fap_keys
        for row in f_ap_rows
    )
    wrong_full_count = sum(1 for row in candidate_rows[1:] if row["matches_packet"])
    pass_conditions = {
        "no_older_test_verdicts_used": not premises["older_test_verdicts_used_as_computed_inputs"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "bao_source_rows_present": len(rows) >= 10,
        "sn_inputs_not_loaded": "sn" not in source_path.name.lower(),
        "window_values_follow_declared_symbols": all(close(declared_symbol_value(row["window_symbol"]), float(row["window_value"])) for row in rows),
        "bao_windowed_prediction_identity": primary_score["max_prediction_error"] <= 1e-9,
        "f_ap_derived_from_dm_dh_rows": f_ap_derived,
        "all_primary_rows_under_3sigma": primary_score["rows_over_3sigma"] == 0,
        "wrong_controls_do_not_match_packet": wrong_full_count == 0,
    }
    verdict_pass = all(pass_conditions.values())
    verdict = "CR014_PASS_BAO_RULER_PROJECTION_LEDGER_SHRINKAGE" if verdict_pass else "CR014_FAIL_BAO_RULER_PROJECTION_LEDGER_SHRINKAGE"

    write_csv(ROOT / "CR014_candidate_rows.csv", candidate_rows)
    write_csv(ROOT / "CR014_recomputed_bao_rows.csv", primary_rows)
    write_csv(
        ROOT / "CR014_input_manifest.csv",
        [
            {"input": str(source_path), "role": "source_data_rows", "used_as_computed_input": True},
            {"input": "CR014_declared_premises.json", "role": "declared_formula_controls", "used_as_computed_input": True},
            {"input": "CR014_PRECOMMIT.md", "role": "sealed_pre_run_prediction", "used_as_computed_input": False},
            {"input": "CR014_runner.py", "role": "calculation_script", "used_as_computed_input": True},
        ],
    )
    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS" if verdict_pass else "FAIL",
        "triage_bin": "A" if verdict_pass else "C",
        "claim_tier": "PASS_BAO_RULER_PROJECTION_LEDGER" if verdict_pass else "FAILED_BAO_RULER_PROJECTION_LEDGER",
        "source_rows": len(rows),
        "w": w,
        "primary_score": primary_score,
        "wrong_control_full_packet_count": wrong_full_count,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
    }
    (ROOT / "CR014_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# CR014 BAO Ruler Projection Ledger Shrinkage",
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
        "## BAO Packet",
        "",
        "```text",
        f"rows = {len(rows)}",
        f"w = {w:.16f}",
        f"max_prediction_error = {primary_score['max_prediction_error']:.3e}",
        f"rms_pull = {primary_score['rms_pull']:.12f}",
        f"rows_over_3sigma = {primary_score['rows_over_3sigma']}",
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
    (ROOT / "CR014_result.md").write_text("\n".join(lines), encoding="utf-8")

    write_hashes(
        [
            ROOT / "CR014_declared_premises.json",
            ROOT / "CR014_PRECOMMIT.md",
            ROOT / "CR014_runner.py",
            ROOT / "CR014_candidate_rows.csv",
            ROOT / "CR014_recomputed_bao_rows.csv",
            ROOT / "CR014_input_manifest.csv",
            ROOT / "CR014_result.md",
            ROOT / "CR014_summary.json",
            source_path,
        ]
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
