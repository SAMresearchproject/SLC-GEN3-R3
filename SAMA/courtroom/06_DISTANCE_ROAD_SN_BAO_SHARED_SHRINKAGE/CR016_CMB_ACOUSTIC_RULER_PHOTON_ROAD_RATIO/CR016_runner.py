import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
REPO = BRANCH.parent
PREMISES_PATH = ROOT / "CR016_declared_premises.json"


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def write_csv(path, rows):
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_hashes(paths):
    lines = []
    for path in sorted(paths, key=lambda p: str(p).lower()):
        if path.name == "HASHES.txt":
            continue
        lines.append(f"{sha256(path)}  {path.relative_to(REPO)}")
    (ROOT / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def theta100(ruler_mpc, road_mpc):
    return 100.0 * ruler_mpc / road_mpc


def main():
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    sam = premises["sam_inputs"]
    ref = premises["external_reference_downstream_only"]
    r_star = sam["r_star_mpc"]
    road = sam["D_M_photon_road_mpc"]
    r_drag = sam["r_drag_mpc"]
    wrong_road = sam["wrong_H0_denominator_mpc"]
    planck = ref["Planck_theta100"]
    pass_window = ref["pass_window_abs_percent"]
    primary = theta100(r_star, road)
    primary_residual_pct = 100.0 * (primary - planck) / planck

    specs = [
        ("primary_acoustic_write_over_photon_road", r_star, road),
        ("use_drag_ruler", r_drag, road),
        ("wrong_H0_denominator", r_star, wrong_road),
        ("invert_ratio", road, r_star),
        ("half_ruler", 0.5 * r_star, road),
        ("drag_ruler_and_wrong_H0", r_drag, wrong_road),
    ]
    candidate_rows = []
    for label, ruler, denom in specs:
        value = theta100(ruler, denom)
        residual_pct = 100.0 * (value - planck) / planck
        candidate_rows.append(
            {
                "candidate": label,
                "ruler_mpc": ruler,
                "road_mpc": denom,
                "theta100": value,
                "planck_reference_theta100": planck,
                "residual_pct": residual_pct,
                "matches_packet": abs(value - primary) <= 1e-12,
            }
        )

    wrong_full_count = sum(1 for row in candidate_rows[1:] if row["matches_packet"])
    pass_conditions = {
        "no_older_test_verdicts_used": not premises["older_test_verdicts_used_as_computed_inputs"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "ratio_identity": abs(primary - 1.038976065435997) <= 1e-12,
        "planck_target_not_formula_source": not premises["frozen_predictions"]["target_data_used_to_choose_formula"],
        "theta_reference_residual_within_half_percent": abs(primary_residual_pct) <= pass_window,
        "wrong_controls_do_not_match_packet": wrong_full_count == 0,
    }
    verdict_pass = all(pass_conditions.values())
    verdict = "CR016_PASS_CMB_ACOUSTIC_RULER_PHOTON_ROAD_RATIO" if verdict_pass else "CR016_FAIL_CMB_ACOUSTIC_RULER_PHOTON_ROAD_RATIO"

    write_csv(ROOT / "CR016_candidate_rows.csv", candidate_rows)
    write_csv(
        ROOT / "CR016_input_manifest.csv",
        [
            {"input": "CR016_declared_premises.json", "role": "declared_formula_controls", "used_as_computed_input": True},
            {"input": "CR016_PRECOMMIT.md", "role": "sealed_pre_run_prediction", "used_as_computed_input": False},
            {"input": "CR016_runner.py", "role": "calculation_script", "used_as_computed_input": True},
            {"input": "Planck theta100 reference", "role": "downstream_external_anchor_only", "used_as_formula_source": False},
        ],
    )
    summary = {
        "test_id": premises["test_id"],
        "verdict": verdict,
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS" if verdict_pass else "FAIL",
        "triage_bin": "A" if verdict_pass else "C",
        "claim_tier": "PASS_CMB_ACOUSTIC_RATIO" if verdict_pass else "FAILED_CMB_ACOUSTIC_RATIO",
        "theta100": primary,
        "planck_reference_theta100": planck,
        "residual_pct": primary_residual_pct,
        "wrong_control_full_packet_count": wrong_full_count,
        "pass_conditions": pass_conditions,
        "rule_9_falsification": premises["rule_9_falsification"],
    }
    (ROOT / "CR016_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# CR016 CMB Acoustic Ruler Photon-Road Ratio",
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
        "## Ratio Packet",
        "",
        "```text",
        f"theta100 = {primary:.15f}",
        f"residual_pct = {primary_residual_pct:.6f}",
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
    (ROOT / "CR016_result.md").write_text("\n".join(lines), encoding="utf-8")

    write_hashes(
        [
            ROOT / "CR016_declared_premises.json",
            ROOT / "CR016_PRECOMMIT.md",
            ROOT / "CR016_runner.py",
            ROOT / "CR016_candidate_rows.csv",
            ROOT / "CR016_input_manifest.csv",
            ROOT / "CR016_result.md",
            ROOT / "CR016_summary.json",
        ]
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
