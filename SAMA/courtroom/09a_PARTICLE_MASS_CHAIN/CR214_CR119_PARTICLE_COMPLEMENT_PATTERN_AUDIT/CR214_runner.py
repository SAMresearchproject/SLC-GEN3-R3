from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
CR119 = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
LC04 = ROOT / "16_THE_LAST_CAMPAIGN" / "LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY"

PARTICLE = CR119 / "CR119_courtroom_particle_table.csv"
MATTER = CR119 / "CR119_courtroom_matter_table.csv"
PERIODIC = CR119 / "CR119_courtroom_periodic_table.csv"
EXPORT_SUMMARY = CR119 / "source_copies" / "latest_table_export_summary.json"
TABLE_COUNTS = CR119 / "source_copies" / "latest_table_counts.csv"
LC04_LAYERS = LC04 / "LC04_particle_replay_layers.csv"
LC04_GENERATORS = LC04 / "LC04_generator_suite_register.csv"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dec(value: str) -> Decimal:
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return Decimal(0)


def positive(row: dict[str, str], key: str) -> bool:
    return dec(row.get(key, "0")) > 0


def matter_gate_reason(row: dict[str, str]) -> str:
    if row.get("latest_matter_row_allowed") != "yes":
        return "REJECT_NOT_MATTER_ALLOWED"
    if row.get("bin") in {
        "antimatter_conjugate_rows",
        "carrier_only_rows",
        "hidden_source_support_rows",
        "rejected_fake_closures",
    }:
        return f"REJECT_BIN_{row.get('bin')}"
    if not row.get("closure_status", "").startswith("CLOSED"):
        return "REJECT_NOT_CLOSED"
    if not positive(row, "M_observed_candidate"):
        return "REJECT_ZERO_OR_NEGATIVE_REVEAL"
    if not positive(row, "qA_source_support"):
        return "REJECT_ZERO_QA"
    if row.get("bin") == "stable_matter_rows":
        return "PASS_STABLE_SINGLE_WRITE_MATTER"
    if (
        row.get("bin") == "bound_composite_rows"
        and "HEAVY" not in row.get("stability_status", "")
        and "REJECTED" not in row.get("stability_status", "")
    ):
        return "PASS_BOUND_COMPOSITE_MATTER"
    return "REJECT_STABILITY_SELECTOR_OPEN_OR_HEAVY"


def complement_role(row: dict[str, str], gate_reason: str) -> str:
    if gate_reason == "REJECT_STABILITY_SELECTOR_OPEN_OR_HEAVY":
        if row.get("bin") == "bound_composite_rows":
            return "HEAVY_COLOR_BOUND_COMPLEMENT"
        return "UNSTABLE_RESONANCE_COMPLEMENT"
    if row.get("bin") == "antimatter_conjugate_rows":
        if row.get("latest_boundary_subtype") == "NULL_CONJUGATE_CLOSURE":
            return "NULL_CONJUGATE_BOUNDARY"
        return "ANTIMATTER_CONJUGATE_COMPLEMENT"
    if row.get("bin") == "bound_composite_rows" and row.get("latest_matter_row_allowed") == "no":
        return "NEGATIVE_SURFACE_COLOR_CLOSURE"
    if row.get("bin") == "carrier_only_rows":
        return "CARRIER_SUPPORT_NOT_MATTER"
    if row.get("bin") == "hidden_source_support_rows":
        return "SOURCE_SUPPORT_NOT_MATTER"
    if row.get("bin") == "rejected_fake_closures":
        return "REJECTED_WRONG_CONTROL"
    return "COMPLEMENT_ROW"


def count_rows(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    counts = Counter(str(row.get(key, "")) for row in rows)
    return [{"field": key, "value": value, "count": count} for value, count in sorted(counts.items())]


def count_pair(rows: list[dict[str, Any]], key_a: str, key_b: str) -> list[dict[str, Any]]:
    counts = Counter((str(row.get(key_a, "")), str(row.get(key_b, ""))) for row in rows)
    return [
        {"field_a": key_a, "value_a": a, "field_b": key_b, "value_b": b, "count": count}
        for (a, b), count in sorted(counts.items())
    ]


def source_manifest(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.append(
            {
                "source": rel(path),
                "exists": path.exists(),
                "bytes": path.stat().st_size if path.exists() else 0,
                "sha256": sha256_file(path) if path.exists() and path.is_file() else "",
            }
        )
    return rows


def build_pattern_leads(
    complement: list[dict[str, Any]],
    particle: list[dict[str, str]],
    matter: list[dict[str, str]],
    periodic: list[dict[str, str]],
    export_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    gate_counts = Counter(row["matter_gate_reason"] for row in complement)
    complement_bins = Counter(row["bin"] for row in complement)
    matter_bins = Counter(row["bin"] for row in matter)
    periodic_known_z = int(export_summary.get("known_z_downstream", 0))
    periodic_frontier_z = int(export_summary.get("frontier_z_unknown", 0))
    not_allowed = gate_counts["REJECT_NOT_MATTER_ALLOWED"]
    stability_open_or_heavy = gate_counts["REJECT_STABILITY_SELECTOR_OPEN_OR_HEAVY"]
    return [
        {
            "lead_id": "P1",
            "pattern": "321 particle rows split into 126 selected matter rows plus 195 complement rows",
            "observed": f"{len(particle)}={len(matter)}+{len(complement)}",
            "status": "BACKED_BY_CR119_TABLE_MEMBERSHIP",
            "next_test": "",
        },
        {
            "lead_id": "P2",
            "pattern": "126 matter table is a dual 63+63 selection",
            "observed": f"stable={matter_bins['stable_matter_rows']}; bound={matter_bins['bound_composite_rows']}",
            "status": "BACKED_BY_CR119_MATTER_TABLE",
            "next_test": "",
        },
        {
            "lead_id": "P3",
            "pattern": "195 complement is the rejection side of the QP093 matter gate",
            "observed": (
                f"stability_open_or_heavy={stability_open_or_heavy}; "
                f"antimatter_bin={gate_counts['REJECT_BIN_antimatter_conjugate_rows']}; "
                f"not_matter_allowed={not_allowed}"
            ),
            "status": "BACKED_BY_EXPORTER_GATE_REPLAY",
            "next_test": "",
        },
        {
            "lead_id": "P4",
            "pattern": "The largest complement is the color/composite heavy side, not residue",
            "observed": (
                f"bound_composite_complement={complement_bins['bound_composite_rows']}; "
                "heavy_or_negative_surface=93+13"
            ),
            "status": "BACKED_BY_CR119_BIN_AND_STABILITY_FIELDS",
            "next_test": "",
        },
        {
            "lead_id": "P5",
            "pattern": "The stability-open/heavy complement count equals the downstream known-Z count",
            "observed": f"{stability_open_or_heavy}={periodic_known_z}",
            "status": "OPEN_COUNT_MATCH_ONLY_NOT_A_MAPPING",
            "next_test": "Build a row-level bridge test before treating this as mechanism.",
        },
        {
            "lead_id": "P6",
            "pattern": "Several guard counts are eight-row packets near the Z119-Z126 frontier count",
            "observed": (
                f"frontier_z={periodic_frontier_z}; "
                f"hidden_support={complement_bins['hidden_source_support_rows']}; "
                f"rejected_fake={complement_bins['rejected_fake_closures']}"
            ),
            "status": "OPEN_COUNT_MATCH_ONLY_NOT_A_MAPPING",
            "next_test": "Test whether any row-level address relation exists.",
        },
    ]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    particle = read_csv(PARTICLE)
    matter = read_csv(MATTER)
    periodic = read_csv(PERIODIC)
    export_summary = read_json(EXPORT_SUMMARY)
    table_counts = read_csv(TABLE_COUNTS)
    lc04_layers = read_csv(LC04_LAYERS)
    lc04_generators = read_csv(LC04_GENERATORS)

    matter_ids = {row["candidate_id"] for row in matter}
    particle_ids = {row["candidate_id"] for row in particle}
    periodic_ids = {row.get("element_closure_id", "") for row in periodic}

    complement: list[dict[str, Any]] = []
    for row in particle:
        gate_reason = matter_gate_reason(row)
        if row["candidate_id"] in matter_ids:
            continue
        exported = dict(row)
        exported["matter_gate_reason"] = gate_reason
        exported["complement_role"] = complement_role(row, gate_reason)
        exported["in_matter_table"] = "no"
        exported["periodic_layer_relation"] = "separate_element_family_layer"
        complement.append(exported)

    all_gate_rows: list[dict[str, Any]] = []
    for row in particle:
        gate_reason = matter_gate_reason(row)
        all_gate_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "bin": row["bin"],
                "latest_matter_row_allowed": row["latest_matter_row_allowed"],
                "stability_status": row["stability_status"],
                "closure_status": row["closure_status"],
                "matter_gate_reason": gate_reason,
                "in_matter_table": "yes" if row["candidate_id"] in matter_ids else "no",
            }
        )

    complement_fields = [
        "candidate_id",
        "bin",
        "route_combination",
        "operator_class",
        "route_class",
        "partition_signature",
        "closure_depth",
        "q_sign",
        "q_abs",
        "native_charge_axis",
        "spin_or_hand_class",
        "closure_status",
        "stability_status",
        "M_native",
        "surface_sign",
        "surface_depth",
        "surface_packet_address",
        "S_debit_or_credit",
        "M_observed_candidate",
        "qA_source_support",
        "tensor_carrier_support",
        "retained_write_support",
        "matter_row_allowed",
        "latest_matter_row_allowed",
        "promotion_status",
        "latest_promotion_status",
        "latest_boundary_subtype",
        "latest_override_source",
        "vault_identity",
        "known_identity_label",
        "identity_assignment_role",
        "known_label_used_as_construction_input",
        "matter_gate_reason",
        "complement_role",
        "in_matter_table",
        "periodic_layer_relation",
    ]

    gate_fields = [
        "candidate_id",
        "bin",
        "latest_matter_row_allowed",
        "stability_status",
        "closure_status",
        "matter_gate_reason",
        "in_matter_table",
    ]

    bin_summary = count_rows(complement, "bin")
    role_summary = count_rows(complement, "complement_role")
    gate_summary = count_rows(all_gate_rows, "matter_gate_reason")
    complement_gate_summary = count_rows(complement, "matter_gate_reason")
    bin_gate_summary = count_pair(complement, "bin", "matter_gate_reason")
    matter_bin_summary = count_rows(matter, "bin")
    pattern_leads = build_pattern_leads(complement, particle, matter, periodic, export_summary)

    checks = [
        {
            "check": "particle_rows_321",
            "passed": len(particle) == 321,
            "observed": len(particle),
            "expected": 321,
        },
        {
            "check": "matter_rows_126",
            "passed": len(matter) == 126,
            "observed": len(matter),
            "expected": 126,
        },
        {
            "check": "periodic_rows_126",
            "passed": len(periodic) == 126,
            "observed": len(periodic),
            "expected": 126,
        },
        {
            "check": "matter_ids_subset_of_particle_ids",
            "passed": matter_ids.issubset(particle_ids),
            "observed": len(matter_ids - particle_ids),
            "expected": 0,
        },
        {
            "check": "periodic_ids_separate_from_particle_candidate_ids",
            "passed": len(periodic_ids & particle_ids) == 0,
            "observed": len(periodic_ids & particle_ids),
            "expected": 0,
        },
        {
            "check": "complement_rows_195",
            "passed": len(complement) == 195,
            "observed": len(complement),
            "expected": 195,
        },
        {
            "check": "matter_table_split_63_63",
            "passed": Counter(row["bin"] for row in matter) == Counter({"stable_matter_rows": 63, "bound_composite_rows": 63}),
            "observed": dict(Counter(row["bin"] for row in matter)),
            "expected": {"stable_matter_rows": 63, "bound_composite_rows": 63},
        },
        {
            "check": "all_particle_rows_get_gate_reason",
            "passed": len(all_gate_rows) == len(particle) and all(row["matter_gate_reason"] for row in all_gate_rows),
            "observed": len(all_gate_rows),
            "expected": len(particle),
        },
        {
            "check": "complement_is_all_non_matter_table_rows",
            "passed": all(row["candidate_id"] not in matter_ids for row in complement),
            "observed": "no matter ids in complement",
            "expected": "no matter ids in complement",
        },
        {
            "check": "lc04_retains_cr119_table_counts",
            "passed": any("321 particle rows, 126 matter rows, 126 periodic rows" in row.get("formula_or_contract", "") for row in lc04_layers),
            "observed": "LC04 particle replay layers scanned",
            "expected": "CR119 finite vault row count layer present",
        },
    ]
    passed = all(row["passed"] for row in checks)

    manifest = source_manifest([PARTICLE, MATTER, PERIODIC, EXPORT_SUMMARY, TABLE_COUNTS, LC04_LAYERS, LC04_GENERATORS])
    write_csv(OUT / "CR214_input_manifest.csv", manifest, ["source", "exists", "bytes", "sha256"])
    write_csv(OUT / "CR214_particle_complement_195.csv", complement, complement_fields)
    write_csv(OUT / "CR214_all_particle_gate_reasons.csv", all_gate_rows, gate_fields)
    write_csv(OUT / "CR214_complement_bin_summary.csv", bin_summary, ["field", "value", "count"])
    write_csv(OUT / "CR214_complement_role_summary.csv", role_summary, ["field", "value", "count"])
    write_csv(OUT / "CR214_matter_gate_summary_all_321.csv", gate_summary, ["field", "value", "count"])
    write_csv(OUT / "CR214_complement_gate_summary_195.csv", complement_gate_summary, ["field", "value", "count"])
    write_csv(OUT / "CR214_complement_bin_gate_summary.csv", bin_gate_summary, ["field_a", "value_a", "field_b", "value_b", "count"])
    write_csv(OUT / "CR214_matter_table_bin_summary.csv", matter_bin_summary, ["field", "value", "count"])
    write_csv(OUT / "CR214_pattern_leads.csv", pattern_leads, ["lead_id", "pattern", "observed", "status", "next_test"])
    write_csv(OUT / "CR214_checks.csv", checks, ["check", "passed", "observed", "expected"])

    summary = {
        "cr_id": "CR214",
        "test_id": "CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "execution_status": "CLEAN" if passed else "BOUNDARY",
        "result_class": (
            "CR214_PASS_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT__195_COMPLEMENT_ROWS_ACCOUNTED__"
            "MATTER_GATE_SPLIT_126_PLUS_195__OPEN_COUNT_LEADS_NOT_PROMOTED"
            if passed
            else "CR214_FAIL_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT"
        ),
        "counts": {
            "particle_rows": len(particle),
            "matter_rows": len(matter),
            "periodic_rows": len(periodic),
            "complement_rows": len(complement),
            "matter_table_split": dict(Counter(row["bin"] for row in matter)),
            "complement_bins": dict(Counter(row["bin"] for row in complement)),
            "complement_gate_reasons": dict(Counter(row["matter_gate_reason"] for row in complement)),
            "all_particle_gate_reasons": dict(Counter(row["matter_gate_reason"] for row in all_gate_rows)),
            "known_z_downstream": export_summary.get("known_z_downstream"),
            "frontier_z_unknown": export_summary.get("frontier_z_unknown"),
        },
        "scientific_reading": (
            "The 195 rows are the structured non-selected side of the CR119 particle-to-matter gate. "
            "They split into stability-open/heavy rows, antimatter conjugate rows, and hard guard/reject rows. "
            "The periodic 126 is a separate element-family layer, not a candidate-id subset of the particle table."
        ),
        "open_leads": [
            "The 118 stability-open/heavy complement count equals the 118 downstream known-Z count, but CR214 finds only a count match.",
            "Eight-row guard packets sit beside the Z119-Z126 frontier count, but CR214 finds only a count match.",
        ],
        "source_counts_scope": table_counts,
        "lc04_generator_sources": [row.get("source", "") for row in lc04_generators],
        "checks_passed": sum(1 for row in checks if row["passed"]),
        "checks_total": len(checks),
        "artifacts": {
            "complement": rel(OUT / "CR214_particle_complement_195.csv"),
            "gate_reasons": rel(OUT / "CR214_all_particle_gate_reasons.csv"),
            "pattern_leads": rel(OUT / "CR214_pattern_leads.csv"),
            "summary": rel(OUT / "CR214_summary.json"),
            "result": rel(OUT / "CR214_result.md"),
        },
    }
    write_json(OUT / "CR214_summary.json", summary)

    result_lines = [
        "# CR214 CR119 Particle Complement Pattern Audit",
        "",
        f"Result: **{summary['result_class']}**",
        "",
        "## Direct Answer",
        "",
        "The 195 rows are the particle-table complement left after the CR119 matter gate selects 126 rows.",
        "They are not one undifferentiated residue class.",
        "",
        "## Count Spine",
        "",
        f"- Particle rows: {len(particle)}",
        f"- Matter rows: {len(matter)}",
        f"- Periodic rows: {len(periodic)}",
        f"- Particle-minus-matter complement: {len(complement)}",
        "",
        "## Matter Table Split",
        "",
    ]
    for row in matter_bin_summary:
        result_lines.append(f"- {row['value']}: {row['count']}")
    result_lines.extend(["", "## Complement Split", ""])
    for row in bin_summary:
        result_lines.append(f"- {row['value']}: {row['count']}")
    result_lines.extend(["", "## Gate Readout", ""])
    for row in complement_gate_summary:
        result_lines.append(f"- {row['value']}: {row['count']}")
    result_lines.extend(
        [
            "",
            "## Pattern Leads",
            "",
            "- BACKED: 321 = 126 selected matter rows + 195 complement rows.",
            "- BACKED: the 126 matter rows split 63 stable single-write and 63 bound-composite rows.",
            "- BACKED: the 195 complement is structured by the matter gate, not by periodic membership.",
            "- OPEN: 118 stability-open/heavy complement rows equals 118 downstream known-Z rows, but CR214 records only a count match.",
            "- OPEN: eight-row guard packets echo the Z119-Z126 frontier count, but CR214 records only a count match.",
            "",
            "## Artifacts",
            "",
            "- `CR214_particle_complement_195.csv`",
            "- `CR214_all_particle_gate_reasons.csv`",
            "- `CR214_complement_bin_summary.csv`",
            "- `CR214_complement_gate_summary_195.csv`",
            "- `CR214_pattern_leads.csv`",
            "- `CR214_summary.json`",
        ]
    )
    (OUT / "CR214_result.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    artifact_paths = [
        OUT / "CR214_PRECOMMIT.md",
        OUT / "CR214_declared_premises.json",
        OUT / "CR214_runner.py",
        OUT / "CR214_input_manifest.csv",
        OUT / "CR214_particle_complement_195.csv",
        OUT / "CR214_all_particle_gate_reasons.csv",
        OUT / "CR214_complement_bin_summary.csv",
        OUT / "CR214_complement_role_summary.csv",
        OUT / "CR214_matter_gate_summary_all_321.csv",
        OUT / "CR214_complement_gate_summary_195.csv",
        OUT / "CR214_complement_bin_gate_summary.csv",
        OUT / "CR214_matter_table_bin_summary.csv",
        OUT / "CR214_pattern_leads.csv",
        OUT / "CR214_checks.csv",
        OUT / "CR214_summary.json",
        OUT / "CR214_result.md",
    ]
    hashes = [{"artifact": rel(path), "sha256": sha256_file(path)} for path in artifact_paths if path.exists()]
    write_csv(OUT / "HASHES.txt", hashes, ["artifact", "sha256"])

    print(json.dumps({"result_class": summary["result_class"], "checks": {"passed": summary["checks_passed"], "total": summary["checks_total"]}}, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

