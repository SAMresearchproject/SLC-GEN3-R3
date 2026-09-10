import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
COURTROOM = BRANCH.parent


SOURCES = {
    "cr051_qc_carrier": {
        "path": BRANCH / "CR051_QC_CARRIER_ENVELOPE_GATE_READOUT" / "CR051_summary.json",
        "role": "qc_carrier_envelope_gate_readout",
    },
    "cr054_qn_born": {
        "path": BRANCH / "CR054_QN_BORN_SURFACE_AND_LETTER_SAFE_CORRECTION" / "CR054_summary.json",
        "role": "qn_born_surface_letter_safe_correction",
    },
    "cr055_earth_a": {
        "path": BRANCH / "CR055_QN_EARTH_A_AND_SEALED_BENCHMARK_MANIFEST" / "CR055_summary.json",
        "role": "earth_a_deployment_benchmark_surface",
    },
    "cr058_branch": {
        "path": BRANCH / "CR058_QC_QN_BRANCH_VERDICT" / "CR058_summary.json",
        "role": "prior_qc_qn_branch_verdict",
    },
    "cr064a_particle": {
        "path": COURTROOM / "09a_PARTICLE_MASS_CHAIN" / "CR064a_PARTICLE_MASS_CHAIN_BRANCH_VERDICT" / "CR064a_summary.json",
        "role": "active_qp075_particle_mass_surface",
    },
    "cr103a_bounce_a": {
        "path": COURTROOM / "14_FOUNDATIONAL_TESTS" / "CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL" / "CR103a_summary.json",
        "role": "bounce_cost_a_dependence_structural_lock",
    },
    "cr103a_bounce_a_result": {
        "path": COURTROOM / "14_FOUNDATIONAL_TESTS" / "CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL" / "CR103a_result.md",
        "role": "bounce_cost_formula_and_user_chain",
    },
    "cr201_source_field": {
        "path": COURTROOM / "15_SCALE_BRIDGE_SIMULATOR" / "CR201_SOURCE_TO_FIELD_SIMULATOR_BRIDGE" / "CR201_summary.json",
        "role": "qA_source_to_field_bridge",
    },
    "cr209_topology": {
        "path": COURTROOM / "15_SCALE_BRIDGE_SIMULATOR" / "CR209_ELECTROWEAK_TOPOLOGY_EXTENSION" / "CR209_summary.json",
        "role": "resolved_parent_write_bounce_topology_extension",
    },
}


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def load_source(source_id, spec):
    path = spec["path"]
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        value = path.read_text(encoding="utf-8")
    manifest = {
        "source_id": source_id,
        "path": str(path),
        "role": spec["role"],
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }
    return value, manifest


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


def display_path(path):
    path = Path(path)
    try:
        return str(path.relative_to(BRANCH)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(COURTROOM)).replace("\\", "/")
        except ValueError:
            return str(path)


def write_hashes(local_paths, source_manifest):
    rows = []
    for path in sorted(set(Path(p) for p in local_paths), key=lambda p: str(p).lower()):
        if path.exists() and path.name != "HASHES.txt":
            rows.append(f"{sha256(path)}  {display_path(path)}")
    rows.append("")
    rows.append("# imported source artifacts")
    for item in source_manifest:
        rows.append(f"{item['sha256']}  {item['path']}")
    (ROOT / "HASHES.txt").write_text("\n".join(rows).rstrip() + "\n", encoding="utf-8")


def render_result(record):
    lines = [
        "# CR059 Mass/Bounce A-Source QC/QN Bridge",
        "",
        "## Verdict",
        "",
        "```text",
        record["verdict"],
        "```",
        "",
        "## Courtroom Fields",
        "",
        "```text",
        f"execution_status = {record['execution_status']}",
        f"scientific_verdict = {record['scientific_verdict']}",
        f"triage_bin = {record['triage_bin']}",
        f"claim_tier = {record['claim_tier']}",
        "```",
        "",
        "## Source Chain",
        "",
        "```text",
        record["source_chain"],
        "```",
        "",
        "## Pass Conditions",
        "",
        "| condition | pass |",
        "|---|---:|",
    ]
    for key, value in record["pass_conditions"].items():
        lines.append(f"| {key} | {str(bool(value)).lower()} |")
    lines.extend(["", "## Evidence Rows", "", "| key | value | note |", "|---|---:|---|"])
    for row in record["evidence_rows"]:
        lines.append(f"| {row['key']} | {row['value']} | {row['note']} |")
    lines.extend(["", "## Opened Protocol Work", ""])
    for item in record["opened_protocol_work"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Scope Boundaries", "", "```text"])
    lines.extend(record["scope_boundaries"])
    lines.extend(["```", "", "## Rule-9 Line", "", "```text", record["rule_9_falsification"], "```", ""])
    return "\n".join(lines)


def main():
    loaded = {}
    manifest = []
    for source_id, spec in SOURCES.items():
        loaded[source_id], row = load_source(source_id, spec)
        manifest.append(row)

    cr051 = loaded["cr051_qc_carrier"]
    cr054 = loaded["cr054_qn_born"]
    cr055 = loaded["cr055_earth_a"]
    cr058 = loaded["cr058_branch"]
    cr064a = loaded["cr064a_particle"]
    cr103a = loaded["cr103a_bounce_a"]
    cr103a_text = loaded["cr103a_bounce_a_result"]
    cr201 = loaded["cr201_source_field"]
    cr209 = loaded["cr209_topology"]

    cr064a_metrics = cr064a["metrics"]
    cr201_conditions = cr201["pass_conditions"]
    cr209_conditions = cr209["pass_conditions"]

    topology_lanes = next(
        row["value"] for row in cr209["evidence_rows"] if row["key"] == "observed_lanes"
    )
    source_rows = next(
        row["value"] for row in cr201["evidence_rows"] if row["key"] == "source_rows_emitted"
    )
    particle_rows = next(
        row["value"] for row in cr201["evidence_rows"] if row["key"] == "particle_rows_imported"
    )

    pass_conditions = {
        "prior_qc_qn_branch_boundary_pass": cr058["execution_status"] == "CLEAN"
        and cr058["scientific_verdict"] == "BOUNDARY_PASS",
        "qc_carrier_control_sensor_available": cr051["scientific_verdict"] == "PASS"
        and cr051["native_gates"] == 5
        and all(cr051.get(k) for k in ["primary_carrier", "control_envelope", "boundary_sensor"]),
        "qn_open_route_matches_primary_carrier": cr054["scientific_verdict"] == "PASS"
        and cr054["top_open_route"] == cr051["primary_carrier"],
        "earth_a_surface_available": cr055["scientific_verdict"] == "PASS"
        and cr055["earth_surface_A"] >= 0
        and cr055["benchmark_manifest_rows"] >= 8,
        "qp075_particle_surface_active": cr064a["execution_status"] == "CLEAN"
        and cr064a["scientific_verdict"] == "PASS_QP075_PARTICLE_MASS_CHAIN_BRANCH_RERUN"
        and cr064a_metrics["closure_rows"] == 35
        and cr064a_metrics["operator_rows"] == 26
        and cr064a_metrics["free_parameters_introduced"] == 0,
        "cr103a_bounce_a_lock_present": cr103a["execution_status"] == "CLEAN"
        and cr103a["result_class"] == "BOUNCE_COST_A_DEPENDENCE_STRUCTURAL_INSIGHT_LOCKED"
        and cr103a["forward_blind_predictions_count"] == 4
        and "r_bounce = (A0/2) * (q / 2^D)" in cr103a_text,
        "cr201_qA_source_bridge_exact": cr201["execution_status"] == "CLEAN"
        and cr201["scientific_verdict"] == "PASS"
        and cr201_conditions["qa_source_formula_exact"]
        and cr201_conditions["no_free_parameters"]
        and "q_A = m * (1 + r_bounce)" in cr201["rule_9_falsification"],
        "cr209_write_bounce_topology_generalizes": cr209["execution_status"] == "CLEAN"
        and cr209["scientific_verdict"] == "PASS"
        and cr209_conditions["five_target_lanes_classified"]
        and cr209_conditions["wrong_controls_pass"]
        and cr209_conditions["no_free_parameters"],
        "hardware_and_full_theory_boundaries_preserved": "not demonstrated quantum hardware"
        in cr058["scope_boundaries"]
        and any("Full electroweak theorem" in str(row["value"]) for row in cr209["evidence_rows"]),
    }

    passed = all(pass_conditions.values())
    verdict = (
        "CR059_PASS_MASS_BOUNCE_A_SOURCE_QC_QN_BRIDGE"
        if passed
        else "CR059_FAIL_MASS_BOUNCE_A_SOURCE_QC_QN_BRIDGE"
    )

    source_chain = (
        "unresolved SW -> resolved write/bounce split -> r_bounce -> "
        "q_A,i = m_i * (1 + r_bounce,i) -> particle A source -> "
        "macro A accumulation -> field-behavior protocol surface"
    )

    evidence_rows = [
        {
            "key": "source_chain",
            "value": source_chain,
            "note": "branch-12 extension chain",
        },
        {
            "key": "qc_roles",
            "value": f"carrier={cr051['primary_carrier']}; envelope={cr051['control_envelope']}; sensor={cr051['boundary_sensor']}",
            "note": "CR051 role split remains the QC carrier surface",
        },
        {
            "key": "qn_open_route",
            "value": f"{cr054['top_open_route']} @ p={cr054['top_open_probability']}",
            "note": "CR054 keeps the route open before ledger commit",
        },
        {
            "key": "particle_surface",
            "value": f"{cr064a_metrics['closure_rows']} closure rows; {cr064a_metrics['operator_rows']} role operators; 0 free parameters",
            "note": "09a/QP075 is the active downstream mass source",
        },
        {
            "key": "bounce_a_lock",
            "value": f"{cr103a['result_class']} ({cr103a['scope_status']})",
            "note": "CR103a locks the A-dependent bounce insight as a structural appeal",
        },
        {
            "key": "qA_source_bridge",
            "value": f"particle rows imported={particle_rows}; q_A source rows={source_rows}",
            "note": "CR201 verifies q_A = m * (1 + r_bounce) with zero new parameters",
        },
        {
            "key": "resolved_topology_lanes",
            "value": topology_lanes,
            "note": "CR209 preserves resolved-parent/write-bounce lane separation",
        },
    ]

    opened_protocol_work = [
        "Source-aware carrier ranking: branch-12 carrier/envelope/sensor rows can now be scored against q_A source load instead of only route grammar.",
        "A-environment protocol surfaces: Earth-A is already in CR055, and CR103a/CR201 give the bridge for high-A stress envelopes without claiming live hardware results.",
        "Paul Revere letters become source-pressure letters: boundary stress can be treated as an early q_A/contact-pressure warning before final ledger write.",
        "Benchmark manifest upgrade path: future lab handoff rows can predeclare mass row, r_bounce class, q_A source row, A environment, carrier, envelope, and sensor before outcome scoring.",
        "Resolved-event topology routing: CR209 lets QC/QN distinguish unresolved carrier preservation, resolved write, visible daughter write, hidden/source bounce budget, and fake-parent rejection as protocol classes.",
    ]

    record = {
        "test_id": "CR059_MASS_BOUNCE_A_SOURCE_QC_QN_BRIDGE",
        "verdict": verdict,
        "execution_status": "CLEAN" if passed else "VIOLATED",
        "scientific_verdict": "PASS" if passed else "FAIL",
        "triage_bin": "A" if passed else "C",
        "claim_tier": "QC_QN_SOURCE_AWARE_PROTOCOL_EXTENSION" if passed else "FAILED_QC_QN_SOURCE_AWARE_PROTOCOL_EXTENSION",
        "source_chain": source_chain,
        "pass_conditions": pass_conditions,
        "evidence_rows": evidence_rows,
        "opened_protocol_work": opened_protocol_work,
        "scope_boundaries": [
            "protocol extension only",
            "not demonstrated quantum hardware",
            "not live external network validation",
            "not full GR derivation",
            "not full electroweak theorem",
            "CR103a is a provisional structural appeal lock until curator sign-off",
        ],
        "rule_9_falsification": (
            "This test could have falsified the branch-12 source-aware extension if the "
            "QC/QN stack was not clean, if QP075 was not the active particle surface, "
            "if q_A = m * (1 + r_bounce) was not an exact source bridge, if resolved "
            "write/bounce topology did not generalize, or if the extension required a "
            "new parameter or hardware overclaim."
        ),
        "source_artifacts": manifest,
    }

    manifest_path = ROOT / "CR059_input_manifest.csv"
    evidence_path = ROOT / "CR059_evidence_rows.csv"
    summary_path = ROOT / "CR059_summary.json"
    result_path = ROOT / "CR059_result.md"

    write_csv(manifest_path, manifest)
    write_csv(evidence_path, evidence_rows)
    summary_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    result_path.write_text(render_result(record), encoding="utf-8")
    write_hashes(
        [
            ROOT / "CR059_PRECOMMIT.md",
            ROOT / "CR059_declared_premises.json",
            ROOT / "CR059_runner.py",
            manifest_path,
            evidence_path,
            summary_path,
            result_path,
        ],
        manifest,
    )
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
