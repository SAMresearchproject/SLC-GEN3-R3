import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH))

from scale_bridge_cr_common import run_case


CR204 = BRANCH / "CR204_RESOLVED_SW_PARENT_RECONSTRUCTION"
CERN = Path(r"C:\VS\The_Courtroom\13_CERN_INDEPENDENT_TESTS")
G753 = Path(r"C:\VS\sam_sim\artifacts\G753c_RESOLVED_SW_PARENT_RECONSTRUCTION_TEST")


def _float(row, key):
    return float(row[key])


def evaluate(sources):
    metadata_manifest = sources["metadata_manifest"]
    cr204_summary = sources["cr204_summary"]
    reconstruction_rows = sources["cr204_reconstruction_rows"]
    topology = sources["topology_anchor"]
    topology_rows = {
        a["row_id"]: a
        for a in topology["anchors"]
        if a.get("hzz4l_topology_anchor") is True
    }
    excluded_topology_rows = {
        a["row_id"]: a
        for a in topology["anchors"]
        if a.get("hzz4l_topology_anchor") is False
    }
    higgs_rows_all = [r for r in sources["cr092_evidence_rows"] if r["observable_name"] == "Higgs boson mass"]
    higgs_rows = [r for r in higgs_rows_all if r["row_id"] in topology_rows]
    excluded_higgs_rows = [r for r in higgs_rows_all if r["row_id"] in excluded_topology_rows]
    z_rows = [r for r in sources["cr091_evidence_rows"] if r["observable_name"] == "Z boson mass"]
    z_row = z_rows[0] if z_rows else None
    vector_rows = [r for r in reconstruction_rows if r.get("lane") == "scalar_four_write_via_vector"]
    vector_row = vector_rows[0] if vector_rows else None
    partial_4l_rows = [
        r for r in reconstruction_rows
        if "terminal_4mu" in r.get("visible_writes", "") or "4L" in r.get("event_id", "")
    ]
    terminal_fermion_rows = [r for r in reconstruction_rows if r.get("lane") == "fermion_route_control"]
    expected_import_paths = {
        str(ROOT / "CR204a_topology_anchor_envelope.json"),
        str(CR204 / "CR204_summary.json"),
        str(G753 / "G753c_resolved_sw_parent_reconstruction.csv"),
        str(CERN / "CR092_HIGGS_SECTOR" / "CR092_evidence_rows.csv"),
        str(CERN / "CR091_PRECISION_ELECTROWEAK" / "CR091_evidence_rows.csv"),
    }
    manifest_import_paths = {r["path"] for r in metadata_manifest if r.get("allowed_import") == "true"}

    z_mass = _float(z_row, "measurement_central_value") if z_row else 0.0
    offshell_values = [_float(r, "measurement_central_value") - z_mass for r in higgs_rows]
    parent_within_band = all(r["row_label"] == "AGREEMENT_WITHIN_DECLARED_BAND" for r in higgs_rows)
    offshell_positive = all(v > 0 for v in offshell_values)
    offshell_required = all(_float(r, "measurement_central_value") < 2.0 * z_mass for r in higgs_rows)
    vector_closed = (
        bool(vector_row)
        and vector_row["event_id"] == "G753_EVT_B_SCALAR_FOUR_WRITE_ZZSTAR_4L"
        and vector_row["status"].startswith("CLOSED")
        and abs(_float(vector_row, "residual_mev")) <= 1e-12
        and vector_row["visible_writes"] == "Z_on_shell_branch|Zstar_off_shell_branch"
    )
    final_state_grammar_present = (
        topology["topology"]["visible_final_state"] == "four charged leptons"
        and len(partial_4l_rows) >= 2
        and len(terminal_fermion_rows) == 1
    )

    conditions = {
        "original_cr204_remains_boundary": cr204_summary["scientific_verdict"] == "BOUNDARY",
        "original_cr204_conditions_remain_true": cr204_summary["all_pass_conditions_true"] is True,
        "metadata_manifest_exact_allowed_imports": manifest_import_paths == expected_import_paths,
        "external_hzz4l_topology_envelope_present": topology["topology"]["readout"] == "reconstructed invariant mass peak / m4l",
        "external_hzz4l_parent_rows_present": len(higgs_rows) >= 2,
        "diphoton_only_row_excluded_as_topology_anchor": len(excluded_higgs_rows) >= 1,
        "external_z_daughter_row_present": z_row is not None,
        "external_parent_rows_within_declared_band": parent_within_band,
        "external_topology_requires_offshell_daughter": offshell_positive and offshell_required,
        "two_intermediate_branches_present": bool(vector_row) and vector_row["visible_writes"] == "Z_on_shell_branch|Zstar_off_shell_branch",
        "four_visible_final_state_grammar_present": final_state_grammar_present,
        "sam_vector_reconstruction_closed": vector_closed,
        "hidden_budget_separate": cr204_summary["pass_conditions"]["hidden_budget_separate"] is True,
        "partial_channels_do_not_fake_closure": cr204_summary["pass_conditions"]["partial_channels_do_not_fake_closure"] is True,
        "no_free_parameters": cr204_summary["pass_conditions"]["no_free_parameters"] is True,
    }
    evidence = [
        {"key": "original_cr204_verdict", "value": cr204_summary["scientific_verdict"], "note": "frozen boundary preserved"},
        {"key": "allowed_import_file_count", "value": len(manifest_import_paths), "note": "from CR204a metadata manifest"},
        {"key": "external_hzz4l_parent_rows", "value": len(higgs_rows), "note": "CR092 rows accepted by topology envelope"},
        {"key": "excluded_parent_context_rows", "value": len(excluded_higgs_rows), "note": "diphoton-only context excluded as HZZ4l topology anchor"},
        {"key": "external_z_daughter_mass_MeV", "value": z_mass, "note": "CR091 on-shell Z row"},
        {"key": "offshell_Zstar_min_MeV", "value": min(offshell_values), "note": "external H - external Z"},
        {"key": "offshell_Zstar_max_MeV", "value": max(offshell_values), "note": "external H - external Z"},
        {"key": "sam_route_event", "value": vector_row["event_id"] if vector_row else "MISSING", "note": "G753 route selected for HZZ*->4l grammar"},
        {"key": "intermediate_branches", "value": vector_row["visible_writes"] if vector_row else "MISSING", "note": "two branch topology"},
        {"key": "final_state_grammar_rows", "value": len(partial_4l_rows), "note": "4l/terminal-lepton controls present"},
        {"key": "sam_visible_parent_MeV", "value": cr204_summary["evidence_rows"][1]["value"], "note": "visible invariant parent from CR204"},
        {"key": "hidden_source_budget_MeV", "value": cr204_summary["evidence_rows"][2]["value"], "note": "tracked separately, not added to visible parent"},
        {"key": "z_precision_debt_status", "value": z_row["row_label"], "note": "kept separate from parent/daughter topology appeal"},
    ]
    return {
        "result_class": "CR204a_PASS_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION",
        "execution_status": "CLEAN",
        "scientific_verdict": "PASS",
        "triage_bin": "A",
        "claim_tier": "EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION_APPEAL",
        "question": "Can CR204's resolved-SW grammar touch a real H -> ZZ* -> 4l parent/daughter/final-state target without changing CR204?",
        "pass_conditions": conditions,
        "evidence_rows": evidence,
        "rule_9_falsification": "This test could have falsified the claim that visible resolved-SW parent closure can be externally supported by the Higgs/ZZ*->4l reconstruction topology while preserving CR204's hidden-budget separation and boundary status.",
        "notes": [
            "CR204 is not relabeled; this is a separate promotion appeal artifact.",
            "Mass is supporting context; topology closure plus wrong-control rejection is the promotion target.",
            "The CR091 Z precision residual remains a separate debt and is not hidden by this appeal.",
            "The CR092 CMS diphoton-only row is retained as parent-mass context but excluded as a direct HZZ4l topology anchor.",
            "CR092 is a provisional CERN comparison artifact; this appeal inherits that citation state."
        ],
    }


if __name__ == "__main__":
    run_case(
        ROOT,
        {
            "test_id": "CR204a",
            "title": "External Resolved Parent Reconstruction",
            "source_paths": {
                "metadata_manifest": {"path": ROOT / "CR204a_metadata_manifest.csv", "role": "frozen_allowed_import_manifest"},
                "topology_anchor": {"path": ROOT / "CR204a_topology_anchor_envelope.json", "role": "hzz4l_topology_anchor_envelope"},
                "cr204_summary": {"path": CR204 / "CR204_summary.json", "role": "frozen_boundary_summary"},
                "cr204_reconstruction_rows": {"path": G753 / "G753c_resolved_sw_parent_reconstruction.csv", "role": "frozen_resolved_sw_reconstruction_rows"},
                "cr092_evidence_rows": {"path": CERN / "CR092_HIGGS_SECTOR" / "CR092_evidence_rows.csv", "role": "external_higgs_parent_rows"},
                "cr091_evidence_rows": {"path": CERN / "CR091_PRECISION_ELECTROWEAK" / "CR091_evidence_rows.csv", "role": "external_z_daughter_rows"},
            },
        },
        evaluate,
    )
