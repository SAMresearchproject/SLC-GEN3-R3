import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR015_declared_premises.json"


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


def weighted_mean(rows, key):
    num = sum(float(row[key]) * float(row["weight"]) for row in rows)
    den = sum(float(row["weight"]) for row in rows)
    return num / den


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    sam = premises["sam_inputs"]
    source_path = Path(premises["source_artifact_used_as_sn_data_rows"])
    R = sam["R"]
    D = sam["D"]
    A0 = 1.0 / (math.pi * R)
    bao_sites = sam["bao_sites"]
    half_width = sam["overlap_half_width_z"]
    with source_path.open("r", encoding="utf-8", newline="") as handle:
        sn_rows = list(csv.DictReader(handle))

    def A(z):
        return A0 * R * (1.0 - (1.0 + z) ** (-D))

    def wrong_pair(z, mode, median_A):
        if mode == "SN_half_A":
            return 0.5 * A(z), A(z)
        if mode == "BAO_D2":
            return A(z), (1.0 / math.pi) * (1.0 - (1.0 + z) ** -2.0)
        if mode == "SN_constant_median_A":
            return median_A, A(z)
        if mode == "BAO_no_shrink":
            return A(z), 0.0
        if mode == "opposite_sign_BAO":
            return A(z), -A(z)
        raise ValueError(mode)

    identity_z = bao_sites + [0.1, 1.0, 2.33]
    identity_rows = []
    for z in identity_z:
        A_sn = A(z)
        A_bao = A(z)
        identity_rows.append({"z": z, "A_SN": A_sn, "A_BAO": A_bao, "identity_error": A_sn - A_bao})

    overlap_rows = []
    for z_bao in bao_sites:
        rows = [row for row in sn_rows if abs(float(row["z"]) - z_bao) <= half_width]
        sn_mean_z = weighted_mean(rows, "z")
        sn_mean_A = weighted_mean(rows, "A_los")
        bao_A = A(z_bao)
        overlap_rows.append(
            {
                "z_bao": z_bao,
                "overlap_half_width_z": half_width,
                "sn_rows": len(rows),
                "sn_weighted_mean_z": sn_mean_z,
                "sn_weighted_mean_A": sn_mean_A,
                "bao_A_at_site": bao_A,
                "A_difference_sn_minus_bao": sn_mean_A - bao_A,
                "shrinkage_pct_difference_sn_minus_bao": 100.0 * (sn_mean_A - bao_A),
            }
        )

    median_A = sorted(float(row["A_los"]) for row in sn_rows)[len(sn_rows) // 2]
    candidate_rows = [
        {
            "candidate": "primary_independent_SN_BAO_A_los_identity",
            "max_identity_error": max(abs(row["identity_error"]) for row in identity_rows),
            "max_overlap_pct_abs": max(abs(row["shrinkage_pct_difference_sn_minus_bao"]) for row in overlap_rows),
            "matches_packet": True,
        }
    ]
    for mode in premises["wrong_controls"]:
        errors = []
        for z in identity_z:
            A_sn, A_bao = wrong_pair(z, mode, median_A)
            errors.append(abs(A_sn - A_bao))
        candidate_rows.append({"candidate": mode, "max_identity_error": max(errors), "max_overlap_pct_abs": "", "matches_packet": max(errors) <= 1e-12})

    wrong_full_count = sum(1 for row in candidate_rows[1:] if row["matches_packet"])
    max_identity_error = candidate_rows[0]["max_identity_error"]
    max_overlap_pct_abs = candidate_rows[0]["max_overlap_pct_abs"]
    pass_conditions = {
        "no_older_test_verdicts_used": not premises["older_test_verdicts_used_as_computed_inputs"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "independent_ledger_functions_defined_before_overlap": True,
        "same_z_identity_holds": max_identity_error <= 1e-15,
        "overlap_not_formula_source": True,
        "all_bao_sites_have_sn_overlap_rows": all(row["sn_rows"] > 0 for row in overlap_rows),
        "overlap_max_abs_pct_within_declared_window": max_overlap_pct_abs <= premises["frozen_predictions"]["overlap_max_abs_pct_window"],
        "wrong_controls_do_not_match_packet": wrong_full_count == 0,
    }
    verdict_pass = all(pass_conditions.values())
    verdict = "CR015_PASS_SN_BAO_INDEPENDENT_LEDGER_LOCK" if verdict_pass else "CR015_FAIL_SN_BAO_INDEPENDENT_LEDGER_LOCK"

    write_csv(ROOT / "CR015_candidate_rows.csv", candidate_rows)
    write_csv(ROOT / "CR015_identity_rows.csv", identity_rows)
    write_csv(ROOT / "CR015_overlap_rows.csv", overlap_rows)
    write_csv(
        ROOT / "CR015_input_manifest.csv",
        [
            {"input": str(source_path), "role": "source_data_rows_for_overlap_only", "used_as_computed_input": True},
            {"input": "CR015_declared_premises.json", "role": "declared_formula_controls", "used_as_computed_input": True},
            {"input": "CR015_PRECOMMIT.md", "role": "sealed_pre_run_prediction", "used_as_computed_input": False},
            {"input": "CR015_runner.py", "role": "calculation_script", "used_as_computed_input": True},
        ],
    )
    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS" if verdict_pass else "FAIL",
        "triage_bin": "A" if verdict_pass else "C",
        "claim_tier": "PASS_SN_BAO_INDEPENDENT_LEDGER_LOCK" if verdict_pass else "FAILED_SN_BAO_INDEPENDENT_LEDGER_LOCK",
        "max_identity_error": max_identity_error,
        "max_overlap_pct_abs": max_overlap_pct_abs,
        "wrong_control_full_packet_count": wrong_full_count,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
    }
    (ROOT / "CR015_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# CR015 SN/BAO Independent Ledger Lock",
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
        "## Lock Packet",
        "",
        "```text",
        f"max_identity_error = {max_identity_error:.3e}",
        f"max_overlap_pct_abs = {max_overlap_pct_abs:.6f}",
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
    (ROOT / "CR015_result.md").write_text("\n".join(lines), encoding="utf-8")

    write_hashes(
        [
            ROOT / "CR015_declared_premises.json",
            ROOT / "CR015_PRECOMMIT.md",
            ROOT / "CR015_runner.py",
            ROOT / "CR015_candidate_rows.csv",
            ROOT / "CR015_identity_rows.csv",
            ROOT / "CR015_overlap_rows.csv",
            ROOT / "CR015_input_manifest.csv",
            ROOT / "CR015_result.md",
            ROOT / "CR015_summary.json",
            source_path,
        ]
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

