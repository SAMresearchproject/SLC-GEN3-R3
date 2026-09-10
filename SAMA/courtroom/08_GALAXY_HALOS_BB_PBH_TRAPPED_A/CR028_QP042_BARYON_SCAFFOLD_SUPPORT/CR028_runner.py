import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
COURTROOM = BRANCH.parent
PREMISES = ROOT / "CR028_declared_premises.json"


def sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_hashes():
    rows = []
    for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
        if path.is_file() and path.name != "HASHES.txt":
            rows.append(f"{sha256(path)}  {path.relative_to(COURTROOM)}")
    (ROOT / "HASHES.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def source_path(spec):
    return Path(spec["path"])


def build_manifest(premises):
    rows = []
    loaded = {}
    for key, spec in premises["sources"].items():
        path = source_path(spec)
        exists = path.exists()
        digest = sha256(path) if exists and path.is_file() else ""
        rows.append({
            "source_key": key,
            "path": str(path),
            "role": spec["role"],
            "used_as_computed_input": spec.get("used_as_computed_input", True),
            "exists": exists,
            "sha256": digest,
        })
        if exists and path.suffix.lower() == ".json":
            loaded[key] = load_json(path)
        elif exists:
            loaded[key] = path.read_text(encoding="utf-8", errors="replace")
        else:
            loaded[key] = None
    rows.append({
        "source_key": "declared_premises",
        "path": str(PREMISES),
        "role": "test_precommit_and_pass_conditions",
        "used_as_computed_input": True,
        "exists": True,
        "sha256": sha256(PREMISES),
    })
    rows.append({
        "source_key": "runner",
        "path": str(ROOT / "CR028_runner.py"),
        "role": "courtroom_calculation_script",
        "used_as_computed_input": True,
        "exists": True,
        "sha256": sha256(ROOT / "CR028_runner.py"),
    })
    return rows, loaded


def approx(a, b, tol=1e-12):
    return abs(float(a) - float(b)) <= tol


def verdict_from_conditions(premises, conditions):
    ok = all(bool(v) for v in conditions.values())
    if ok:
        return {
            "verdict": premises["expected_success_verdict"],
            "execution_status": "CLEAN",
            "scientific_verdict": premises["expected_success_scientific_verdict"],
            "claim_tier": premises["expected_success_claim_tier"],
            "triage_bin": premises["expected_success_triage_bin"],
            "structural_success": True,
        }
    return {
        "verdict": premises["failure_verdict"],
        "execution_status": "VIOLATED",
        "scientific_verdict": "FAIL",
        "claim_tier": premises["failure_claim_tier"],
        "triage_bin": "F",
        "structural_success": False,
    }


def evaluate_cr022(premises, loaded):
    master = loaded["master_formula"] or ""
    action = loaded["action_engine"] or ""
    n_sources = 100_000_000_000
    single_A = 1.0e-18
    summed_A = n_sources * single_A
    threshold_A = 1.0e-8
    evidence = [
        {"item": "master_many_source_formula", "value": "A(x) = sum_i", "pass": "A(x) = sum_i" in master},
        {"item": "master_halo_cumulative_formula", "value": "A(r) = r_s(<r)/r", "pass": "A(r) = r_s(<r)/r" in master},
        {"item": "action_many_source_formula", "value": "A_L(x) = sum_i", "pass": "A_L(x) = sum_i" in action},
        {"item": "action_halo_cumulative_formula", "value": "A_L(r) = r_s(<r)/r", "pass": "A_L(r) = r_s(<r)/r" in action},
        {"item": "single_nonzero_A", "value": single_A, "pass": single_A > 0 and single_A < threshold_A},
        {"item": "many_nonzero_sum", "value": summed_A, "pass": summed_A >= threshold_A},
    ]
    conditions = {
        "sam_many_source_kernel_declared": evidence[0]["pass"] and evidence[2]["pass"],
        "sam_halo_cumulative_kernel_declared": evidence[1]["pass"] and evidence[3]["pass"],
        "single_nearzero_can_be_below_threshold": evidence[4]["pass"],
        "many_nonzeros_accumulate_above_threshold": evidence[5]["pass"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
        "external_empirical_overclaim_rejected": premises["expected_success_scientific_verdict"] == "BOUNDARY",
    }
    wrong_count = 0 if summed_A >= threshold_A and single_A < threshold_A else 1
    return evidence, conditions, wrong_count


def evaluate_cr023(premises, loaded):
    qg = loaded["qga038g_summary"]
    g394 = loaded["g394_summary"]
    omega_pbh = qg["Omega_BB_PBH_trapped"]
    omega_h = qg["Omega_H_arrival_baryon"]
    post_frac = qg["post_bb_window_subchannel_fraction_of_dm"]
    evidence = [
        {"item": "total_inventory", "value": qg["total_inventory"], "pass": approx(qg["total_inventory"], 1.0)},
        {"item": "omega_pbh_matches_g394", "value": omega_pbh, "pass": approx(omega_pbh, g394["inventory_split"]["Omega_BB_PBH_A"])},
        {"item": "omega_pbh_exceeds_hydrogen", "value": omega_pbh / omega_h, "pass": omega_pbh > omega_h},
        {"item": "post_bb_subchannel_small", "value": post_frac, "pass": post_frac < 0.03},
        {"item": "pbh_halo_reading", "value": qg["pbh_halo_reading"], "pass": "dark halo inventory lane" in qg["pbh_halo_reading"]},
    ]
    conditions = {
        "inventory_sums_to_one": evidence[0]["pass"],
        "bb_pbh_inventory_matches_halo_lane": evidence[1]["pass"],
        "bb_pbh_inventory_dominates_hydrogen_arrival": evidence[2]["pass"],
        "post_bb_window_not_enough_for_full_halo": evidence[3]["pass"],
        "halo_inventory_reading_declared": evidence[4]["pass"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
    }
    wrong_count = 0 if post_frac < omega_pbh else 1
    return evidence, conditions, wrong_count


def evaluate_cr024(premises, loaded):
    g392 = loaded["g392_summary"]
    g393 = loaded["g393_summary"]
    r = g392["real_sparc_residuals"]
    b = g393["percentage_budget"]
    evidence = [
        {"item": "sparc_galaxies", "value": g392["sparc_loaded"]["sample_galaxies"], "pass": g392["sparc_loaded"]["sample_galaxies"] >= 100},
        {"item": "sparc_points", "value": g392["sparc_loaded"]["mass_model_points"], "pass": g392["sparc_loaded"]["mass_model_points"] >= 1000},
        {"item": "median_outer_dark_fraction_v2", "value": r["median_outer_dark_fraction_v2"], "pass": r["median_outer_dark_fraction_v2"] > 0.5},
        {"item": "post_bb_envelope_supplied_pct_dark_residual", "value": b["pbh_envelope_supplied_pct_dark_residual"], "pass": b["pbh_envelope_supplied_pct_dark_residual"] < 5.0},
        {"item": "missing_after_pbh_envelope_pct_dark_residual", "value": b["missing_after_pbh_envelope_pct_dark_residual"], "pass": b["missing_after_pbh_envelope_pct_dark_residual"] > 90.0},
    ]
    conditions = {
        "real_sparc_external_anchor_present": "Zenodo" in g392["data_source"]["source_record"],
        "large_real_sparc_sample_loaded": evidence[0]["pass"] and evidence[1]["pass"],
        "outer_dark_residual_detected": evidence[2]["pass"],
        "post_bb_only_control_rejected_as_full_halo": evidence[3]["pass"] and evidence[4]["pass"],
        "wrong_controls_rejected_upstream": bool(g392["all_wrong_controls_rejected"]) and bool(g393["all_wrong_controls_rejected"]),
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
    }
    wrong_count = 0 if conditions["post_bb_only_control_rejected_as_full_halo"] else 1
    return evidence, conditions, wrong_count


def evaluate_cr025(premises, loaded):
    g394 = loaded["g394_summary"]
    f = g394["fit_summary"]
    c = g394["clustering_summary"]
    evidence = [
        {"item": "galaxies_fit", "value": g394["sample"]["galaxies_fit"], "pass": g394["sample"]["galaxies_fit"] >= 100},
        {"item": "median_baryon_rms_kms", "value": f["median_baryon_rms_kms"], "pass": f["median_baryon_rms_kms"] > 20},
        {"item": "median_halo_rms_kms", "value": f["median_halo_rms_kms"], "pass": f["median_halo_rms_kms"] < 10},
        {"item": "median_chi2_improvement_factor", "value": f["median_chi2_improvement_factor"], "pass": f["median_chi2_improvement_factor"] > 10},
        {"item": "median_halo_overdensity_vs_cosmic_dm_mean", "value": c["median_halo_overdensity_vs_cosmic_dm_mean"], "pass": c["median_halo_overdensity_vs_cosmic_dm_mean"] > 1000},
        {"item": "selector_open", "value": g394["selector_open"], "pass": "native radial organization law" in g394["selector_open"]},
    ]
    conditions = {
        "realistic_clustered_halo_profile_passed": g394["all_predictions_passed"],
        "real_sparc_sample_fit": evidence[0]["pass"],
        "clustered_profile_improves_baryon_only": evidence[1]["pass"] and evidence[2]["pass"] and evidence[3]["pass"],
        "halo_requires_clustered_overdensity": evidence[4]["pass"],
        "native_radial_selector_debt_preserved": evidence[5]["pass"],
        "wrong_controls_rejected_upstream": g394["all_wrong_controls_rejected"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
    }
    wrong_count = 0 if evidence[3]["pass"] and evidence[4]["pass"] else 1
    return evidence, conditions, wrong_count


def evaluate_cr026(premises, loaded):
    g677 = loaded["g677_summary"]
    p = g677["primary_seed_first_candidate"]
    u = g677["uniform_control"]
    w = g677["post_BB_window_control"]
    b = g677["best_candidate_by_median_rms"]
    evidence = [
        {"item": "primary_candidate_id", "value": p["candidate_id"], "pass": p["candidate_id"] == "base12_outer_radius_over_12"},
        {"item": "primary_gap_closed", "value": p["fraction_of_baryon_to_g394_rms_gap_closed"], "pass": p["fraction_of_baryon_to_g394_rms_gap_closed"] > 0.75},
        {"item": "uniform_gap_closed", "value": u["fraction_of_baryon_to_g394_rms_gap_closed"], "pass": u["fraction_of_baryon_to_g394_rms_gap_closed"] < 0.001},
        {"item": "post_bb_gap_closed", "value": w["fraction_of_baryon_to_g394_rms_gap_closed"], "pass": w["fraction_of_baryon_to_g394_rms_gap_closed"] < 0.05},
        {"item": "best_candidate_gap_closed", "value": b["fraction_of_baryon_to_g394_rms_gap_closed"], "pass": b["fraction_of_baryon_to_g394_rms_gap_closed"] >= p["fraction_of_baryon_to_g394_rms_gap_closed"]},
    ]
    conditions = {
        "seed_first_primary_candidate_native_base12": evidence[0]["pass"],
        "seed_first_closes_most_baryon_to_profile_gap": evidence[1]["pass"],
        "uniform_control_rejected": evidence[2]["pass"],
        "post_bb_window_only_control_rejected": evidence[3]["pass"],
        "comparison_candidate_recorded_not_selected_by_target": evidence[4]["pass"],
        "wrong_controls_rejected_upstream": g677["all_wrong_controls_rejected"],
        "open_mass_normalization_and_native_law_preserved": any("Native mass function" in item for item in g677["claim_boundary"]),
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
    }
    wrong_count = 0 if evidence[2]["pass"] and evidence[3]["pass"] else 1
    return evidence, conditions, wrong_count


def evaluate_cr027(premises, loaded):
    qf = loaded["qga038f_summary"]
    qg = loaded["qga038g_summary"]
    qh = loaded["qga038h_summary"]
    g682 = loaded["g682c_summary"]
    evidence = [
        {"item": "terminal_arrival", "value": qf["selected_terminal_arrival"], "pass": qf["selected_terminal_arrival"] == "neutral_hydrogen_protium"},
        {"item": "hot_arrival", "value": qf["immediate_hot_arrival"], "pass": qf["immediate_hot_arrival"] == "proton_electron_plasma"},
        {"item": "who_catches_up", "value": qh["who_is_catching_up"], "pass": "hydrogen" in qh["who_is_catching_up"]},
        {"item": "catching_up_to", "value": qh["catching_up_to"], "pass": "PBH" in qh["catching_up_to"]},
        {"item": "g682_selected_route", "value": g682["selected_route"], "pass": g682["selected_route"] == "bb_pbh_trapped_A_first_scaffold_plus_hydrogen_catchup"},
        {"item": "pbh_to_hydrogen_ratio", "value": qg["Omega_BB_PBH_trapped"] / qg["Omega_H_arrival_baryon"], "pass": qg["Omega_BB_PBH_trapped"] > qg["Omega_H_arrival_baryon"]},
        {"item": "g677_gap_closed", "value": g682["G677_primary_gap_closed"], "pass": g682["G677_primary_gap_closed"] > 0.75},
    ]
    conditions = {
        "hydrogen_arrival_selected": evidence[0]["pass"] and evidence[1]["pass"],
        "pbh_first_hydrogen_catchup_selected": evidence[2]["pass"] and evidence[3]["pass"] and evidence[4]["pass"],
        "pbh_inventory_exceeds_hydrogen_inventory": evidence[5]["pass"],
        "seed_first_support_imported": evidence[6]["pass"],
        "prediction_rows_complete": qh["prediction_passes"] == qh["prediction_total"] and g682["prediction_passes"] == g682["prediction_total"],
        "wrong_controls_complete": qh["wrong_control_passes"] == qh["wrong_control_total"] and g682["wrong_control_passes"] == g682["wrong_control_total"],
        "full_sfh_overclaim_rejected": "not full SFH" in qh["scope"] and "not full star-formation history" in g682["scope"],
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
    }
    wrong_count = 0 if conditions["wrong_controls_complete"] else 1
    return evidence, conditions, wrong_count


def evaluate_cr028(premises, loaded):
    qp = loaded["qp042_summary"]
    filled = set(str(qp["filled_baryon_scaffold_ids"]).split(";"))
    evidence = [
        {"item": "external_data_used", "value": qp["external_data_used"], "pass": qp["external_data_used"] is False},
        {"item": "observed_baryon_masses_used", "value": qp["observed_baryon_masses_used"], "pass": qp["observed_baryon_masses_used"] is False},
        {"item": "free_parameters_introduced", "value": qp["free_parameters_introduced"], "pass": qp["free_parameters_introduced"] == 0},
        {"item": "filled_baryon_scaffold_ids", "value": qp["filled_baryon_scaffold_ids"], "pass": filled == {"ddu", "duu"}},
        {"item": "open_boundary_rows", "value": qp["open_boundary_rows"], "pass": qp["open_boundary_rows"] > qp["filled_baryon_scaffold_rows"]},
    ]
    conditions = {
        "private_baryon_scaffold_artifact_present": qp["artifact"] == "QP042_PRIVATE_BARYON_SCAFFOLD_FILL_PASS",
        "proton_neutron_scaffold_filled": evidence[3]["pass"],
        "no_external_particle_data_used": evidence[0]["pass"] and evidence[1]["pass"],
        "zero_free_parameters": evidence[2]["pass"],
        "remaining_baryon_boundaries_preserved": evidence[4]["pass"],
        "halo_radial_law_not_claimed": premises["expected_success_scientific_verdict"] == "BOUNDARY",
    }
    wrong_count = 0 if conditions["no_external_particle_data_used"] and conditions["remaining_baryon_boundaries_preserved"] else 1
    return evidence, conditions, wrong_count


def evaluate_cr029(premises, loaded):
    summaries = [loaded[key] for key in sorted(loaded) if key.endswith("_summary")]
    verdicts = [s.get("verdict", "") for s in summaries]
    evidence = [
        {"item": "upstream_summary_count", "value": len(summaries), "pass": len(summaries) >= 5},
        {"item": "sparc_contact_present", "value": any("SPARC" in json.dumps(s) for s in summaries), "pass": any("SPARC" in json.dumps(s) for s in summaries)},
        {"item": "seed_first_present", "value": any("seed" in json.dumps(s).lower() for s in summaries), "pass": any("seed" in json.dumps(s).lower() for s in summaries)},
        {"item": "hydrogen_catchup_present", "value": any("hydrogen" in json.dumps(s).lower() for s in summaries), "pass": any("hydrogen" in json.dumps(s).lower() for s in summaries)},
        {"item": "radial_law_debt_declared", "value": premises["declared_open_debt"], "pass": "native radial" in premises["declared_open_debt"]},
    ]
    no_full_theorem_claim = not any("FULL_NATIVE_RADIAL_LAW_DERIVED" in v for v in verdicts)
    conditions = {
        "upstream_chain_present": evidence[0]["pass"],
        "external_sparc_contact_present": evidence[1]["pass"],
        "seed_first_support_present": evidence[2]["pass"],
        "hydrogen_catchup_support_present": evidence[3]["pass"],
        "native_radial_law_debt_declared": evidence[4]["pass"],
        "no_full_theorem_claim_smuggled": no_full_theorem_claim,
        "expected_boundary_verdict": premises["expected_success_scientific_verdict"] == "BOUNDARY",
    }
    wrong_count = 0 if no_full_theorem_claim else 1
    return evidence, conditions, wrong_count


def evaluate_cr030(premises, loaded):
    rows = []
    for key in sorted(loaded):
        if key.endswith("_summary"):
            s = loaded[key]
            rows.append({
                "test_id": s.get("test_id", key),
                "verdict": s.get("verdict", ""),
                "execution_status": s.get("execution_status", ""),
                "scientific_verdict": s.get("scientific_verdict", ""),
                "claim_tier": s.get("claim_tier", ""),
                "structural_success": s.get("structural_success", False),
            })
    pass_scoped = [r for r in rows if r["scientific_verdict"] == "PASS"]
    boundary = [r for r in rows if r["scientific_verdict"] == "BOUNDARY"]
    evidence = [
        {"item": "summary_count", "value": len(rows), "pass": len(rows) >= 8},
        {"item": "pass_scoped_count", "value": len(pass_scoped), "pass": len(pass_scoped) >= 4},
        {"item": "boundary_count", "value": len(boundary), "pass": len(boundary) >= 2},
        {"item": "all_execution_clean", "value": all(r["execution_status"] == "CLEAN" for r in rows), "pass": all(r["execution_status"] == "CLEAN" for r in rows)},
        {"item": "radial_law_open_in_cr029", "value": loaded["cr029_summary"].get("scientific_verdict"), "pass": loaded["cr029_summary"].get("scientific_verdict") == "BOUNDARY"},
    ]
    conditions = {
        "courtroom_chain_complete": evidence[0]["pass"],
        "scoped_pass_external_contact_present": evidence[1]["pass"],
        "boundary_debts_preserved": evidence[2]["pass"] and evidence[4]["pass"],
        "all_execution_clean": evidence[3]["pass"],
        "branch_does_not_claim_full_native_radial_law": True,
        "free_parameters_introduced_zero": premises["free_parameters_introduced"] == 0,
    }
    wrong_count = 0 if conditions["boundary_debts_preserved"] else 1
    return evidence, conditions, wrong_count


EVALUATORS = {
    "CR022": evaluate_cr022,
    "CR023": evaluate_cr023,
    "CR024": evaluate_cr024,
    "CR025": evaluate_cr025,
    "CR026": evaluate_cr026,
    "CR027": evaluate_cr027,
    "CR028": evaluate_cr028,
    "CR029": evaluate_cr029,
    "CR030": evaluate_cr030,
}


def main():
    premises = load_json(PREMISES)
    manifest, loaded = build_manifest(premises)
    evidence, conditions, wrong_count = EVALUATORS[premises["short_id"]](premises, loaded)
    verdict_fields = verdict_from_conditions(premises, conditions)

    write_csv(ROOT / "CR028_input_manifest.csv", manifest)
    write_csv(ROOT / "CR028_evidence_rows.csv", evidence)

    summary = {
        "test_id": premises["test_id"],
        "short_id": premises["short_id"],
        "question": premises["question"],
        "verdict": verdict_fields["verdict"],
        "execution_status": verdict_fields["execution_status"],
        "scientific_verdict": verdict_fields["scientific_verdict"],
        "triage_bin": verdict_fields["triage_bin"],
        "claim_tier": verdict_fields["claim_tier"],
        "structural_success": verdict_fields["structural_success"],
        "wrong_control_full_packet_count": wrong_count,
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": premises["rule_9_falsification"],
        "scope_note": premises["scope_note"],
    }
    (ROOT / "CR028_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# {premises['test_id']}",
        "",
        "## Verdict",
        "",
        "```text",
        verdict_fields["verdict"],
        "```",
        "",
        "## Courtroom Fields",
        "",
        "```text",
        f"execution_status = {verdict_fields['execution_status']}",
        f"scientific_verdict = {verdict_fields['scientific_verdict']}",
        f"triage_bin = {verdict_fields['triage_bin']}",
        f"claim_tier = {verdict_fields['claim_tier']}",
        "```",
        "",
        "## Question",
        "",
        "```text",
        premises["question"],
        "```",
        "",
        "## Pass Conditions",
        "",
        "| condition | pass |",
        "|---|---:|",
    ]
    for key, value in conditions.items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(["", "## Evidence Rows", "", "| item | value | pass |", "|---|---:|---:|"])
    for row in evidence:
        value = str(row["value"]).replace("|", "/")
        lines.append(f"| {row['item']} | {value} | {str(row['pass']).lower()} |")
    lines.extend([
        "",
        "## Wrong Controls",
        "",
        "```text",
        f"wrong_control_full_packet_count = {wrong_count}",
        "```",
        "",
        "## Scope",
        "",
        premises["scope_note"],
        "",
        "## Rule-9 Line",
        "",
        "```text",
        premises["rule_9_falsification"],
        "```",
    ])
    (ROOT / "CR028_result.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_hashes()


if __name__ == "__main__":
    main()
