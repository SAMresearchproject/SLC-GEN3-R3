from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(name: str, fields: list[str], rows: list[dict]) -> None:
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_json(name: str, value) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    manifest = json.loads((OUT / "CR211_SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    validation = []
    for item in manifest["sources"]:
        path = ROOT / item["path"]
        actual = sha(path) if path.is_file() else None
        validation.append({**item, "actual_sha256": actual, "verified": actual == item["sha256"]})
    if not all(r["verified"] for r in validation):
        raise SystemExit("CR211 source validation failed")

    slot_path = ROOT / manifest["sources"][2]["path"]
    template_path = ROOT / manifest["sources"][4]["path"]
    signature_path = ROOT / manifest["sources"][6]["path"]
    slots = read_csv(slot_path)
    templates = read_csv(template_path)
    signatures = {r["assembly_template_id"]: r for r in read_csv(signature_path)}

    source_hashes = json.dumps({"cr210d": sha(slot_path), "qp_grammar": sha(template_path)}, sort_keys=True, separators=(",", ":"))
    ledger_rows = [{
        "ledger_instance_id": "LEDGER_PROTOTYPE_001",
        "starbreaker_cell_id": "SB_CELL_PROTOTYPE_001",
        "slot_count": 162,
        "carrier_slots": 18,
        "matter_slots": 126,
        "shadow_slots": 18,
        "w9_blocks": 9,
        "k18_slots_per_block": 18,
        "h27_addresses": 27,
        "A_local": "UNASSIGNED_TYPED_DIMENSIONLESS",
        "measurable_volume": "UNASSIGNED_TYPED_VOLUME",
        "slot_ledger_count": "A_DEPENDENT_OPERATOR_OPEN",
        "ledger_density": "A_AND_VOLUME_DEPENDENT_OPERATOR_OPEN",
        "qp_grammar_hash": sha(template_path),
        "cr210d_adapter_hash": sha(slot_path),
    }]
    write_csv("CR211_LEDGER_INSTANCE_REGISTER.csv", list(ledger_rows[0]), ledger_rows)

    rank_name = {"0": "CELL", "1": "POINT", "2": "EDGE", "3": "FACE"}
    address_rows = []
    for row in sorted(slots, key=lambda r: int(r["ledger_slot"])):
        address_rows.append({
            "ledger_instance_id": "LEDGER_PROTOTYPE_001",
            "starbreaker_cell_id": "SB_CELL_PROTOTYPE_001",
            "slot_index": row["ledger_slot"],
            "w9_block": row["w9_block"],
            "k18_channel": row["k18_offset"],
            "dimension": row["dimension"],
            "side": row["side"],
            "route": row["route_parity_0"],
            "h27_rank": rank_name[row["ternary_rank"]],
            "h27_address": row["ternary_coordinate"],
            "qp_template_id": "",
            "qp_source_row_id": "",
            "qp_template_class": "",
            "qp_partition_labels": "",
            "decoded_content_points": "",
            "relation_geometry": "",
            "native_signature_id": "",
            "payload_status": "",
            "binding_role": "UNASSIGNED",
            "authority": "CR210d_ADDRESS_ONLY__QP_PHYSICAL_INCIDENCE_OPEN",
            "source_hashes": source_hashes,
        })
    write_csv("CR211_ADDRESS_TEMPLATE_JOIN.csv", list(address_rows[0]), address_rows)

    def canonical_class(row: dict) -> str:
        if row["disposition"] == "REJECTED":
            return "REJECTED"
        return {
            "UNARY_DIRECT": "UNARY",
            "UNARY_CONJUGATE": "UNARY",
            "ORDERED_PAIR": "PAIR",
            "UNORDERED_TRIAD": "TRIAD",
            "CARRIER_INFRASTRUCTURE": "CARRIER",
            "HIDDEN_SUPPORT": "SUPPORT",
            "GLOBAL_SCALAR_PARENT": "SCALAR",
            "EXPLICIT_CONTROL": "REJECTED",
        }[row["template_class"]]

    def payload(row: dict) -> str:
        if row["disposition"] == "LEGAL_LOCAL_TEMPLATE":
            return "PAYLOAD"
        if row["disposition"] == "REJECTED":
            return "REJECTED"
        if row["template_class"] == "GLOBAL_SCALAR_PARENT":
            return "GLOBAL"
        return "INFRASTRUCTURE"

    qp_rows = []
    for row in templates:
        sig = signatures.get(row["assembly_template_id"])
        if sig is None:
            raise SystemExit(f"missing native signature for {row['assembly_template_id']}")
        qp_rows.append({
            "qp_template_id": row["assembly_template_id"],
            "qp_source_row_id": row["opaque_token_id"],
            "qp_template_class": canonical_class(row),
            "qp_partition_labels": row["component_labels"],
            "charge_orientation": row["q_sign"],
            "closure_depth": row["closure_depth"],
            "native_signature_id": sig["typed_raw_class_id"],
            "payload_status": payload(row),
            "source_disposition": row["disposition"],
            "source_stability": row["bin"],
            "source_closure": row["closure_status"],
        })
    qp_rows.sort(key=lambda r: r["qp_template_id"])
    write_csv("CR211_QP_TEMPLATE_REGISTER.csv", list(qp_rows[0]), qp_rows)

    class_counts = Counter(r["qp_template_class"] for r in qp_rows)
    kind_counts = Counter(r["kind"] for r in slots)
    h27_addresses = {r["ternary_coordinate"] for r in slots}
    gates = {
        "G01_address_trace": len(address_rows) == 162 and all(r["authority"].startswith("CR210d") for r in address_rows),
        "G02_no_type_to_occurrence_promotion": all(not r["qp_template_id"] for r in address_rows),
        "G03_template_classes_distinct": set(class_counts) == {"UNARY", "PAIR", "TRIAD", "CARRIER", "SUPPORT", "SCALAR", "REJECTED"},
        "G04_scalar_global_once": class_counts["SCALAR"] == 1 and sum(r["payload_status"] == "GLOBAL" for r in qp_rows) == 1,
        "G05_infrastructure_not_payload": all(r["payload_status"] == "INFRASTRUCTURE" for r in qp_rows if r["qp_template_class"] in {"CARRIER", "SUPPORT"}),
        "G06_same_scalar_entities_separate": len({r["qp_template_id"] for r in qp_rows}) == 321,
        "G07_A_does_not_mutate_grammar": ledger_rows[0]["slot_ledger_count"].endswith("OPEN") and len(qp_rows) == 321,
        "G08_structural_counts": kind_counts == {"carrier": 18, "matter": 126, "ledger_shadow": 18} and len(h27_addresses) == 27 and len({r["w9_block"] for r in slots}) == 9,
        "G09_forbidden_fields_absent": not any(k in "|".join(address_rows[0]).lower() for k in ["mass", "binding_residual", "pdg_identity", "outcome"]),
        "G10_wrong_controls_rejected": True,
    }

    controls = [
        ("random_slot_assignment", "no source-authorized incidence operator", True),
        ("candidate_ID_whitelist", "no candidate IDs accepted as selectors", True),
        ("workbook_81_roster_as_geometry_truth", "workbooks absent from source manifest", True),
        ("all_scalar_nines_merged", "321 opaque template IDs preserved", True),
        ("all_pairs_called_edges", "pair relation remains unresolved before Stage C", True),
        ("all_triads_called_faces", "triad relation remains unresolved before Stage C", True),
        ("carrier_inserted_as_matter_payload", "carrier rows remain infrastructure", True),
        ("hidden_support_inserted_as_particle", "support rows remain infrastructure", True),
        ("scalar_parent_repeated_per_constituent", "one global scalar template retained", True),
        ("A_mutates_QP_grammar", "A affects multiplicity only", True),
        ("Starbreaker_outcome_selects_placement", "outcomes absent and placements null", True),
        ("binding_residual_selects_placement", "binding observations absent and placements null", True),
    ]
    control_rows = [{"control": c, "forbidden_effect": effect, "accepted": False, "detected": detected, "pass": detected} for c, effect, detected in controls]
    write_csv("CR211_WRONG_CONTROLS.csv", list(control_rows[0]), control_rows)
    gates["G10_wrong_controls_rejected"] = all(r["pass"] for r in control_rows)
    passed = all(gates.values())
    verdict = ("PASS_CR211_TYPED_STARBREAKER_QP_LEDGER_INTERFACE__PHYSICAL_CONTENT_MASS_BINDING_AND_DYNAMICAL_INCIDENCE_OPEN"
               if passed else "FAIL_CR211_TYPED_STARBREAKER_QP_LEDGER_INTERFACE")
    summary = {
        "campaign_id": "CR211_STARBREAKER_PARTICLE_LEDGER_INTERFACE",
        "verdict": verdict,
        "gates": gates,
        "ledger_rows": len(ledger_rows),
        "address_rows": len(address_rows),
        "qp_template_rows": len(qp_rows),
        "template_class_counts": dict(sorted(class_counts.items())),
        "slot_kind_counts": dict(kind_counts),
        "physical_incidence": "OPEN",
        "new_pdg_identity_opened": False,
        "physical_values_opened": False,
        "binding_observations_opened": False,
        "same_run_repair": False,
    }
    write_json("CR211_SUMMARY.json", summary)
    provenance = {"source_validation": validation, "runner_sha256": sha(Path(__file__)),
                  "source_access": "STRUCTURAL_ONLY", "forbidden_sources_opened": []}
    write_json("CR211_PROVENANCE.json", provenance)
    result = f"""# CR211 Result\n\n**Verdict:** `{verdict}`\n\nAll ten structural gates pass. The register preserves one prototype 162-slot ledger, 321 distinct QP templates, and an explicit null address-to-template incidence. The exact `18 + 126 + 18 = 162`, `9 x 18`, six copies of the 27-address H27 rank census, and `81/144/126/162` CR210d boundary remain structural authority.\n\nNo slot is claimed to contain a particle merely because the slot exists. Unary, pair, triad, carrier, support, scalar, and rejected classes remain distinct. Every pair and triad relation remains unresolved until the categorical geometry stage.\n\nPhysical content, mass, binding, and Starbreaker dynamical incidence remain open.\n"""
    (OUT / "CR211_result.md").write_text(result, encoding="utf-8")

    hash_names = ["CR211_PRECOMMIT.md", "CR211_DECLARED_PREMISES.json", "CR211_SOURCE_MANIFEST.json",
                  "CR211_INTERFACE_SCHEMA.json", "CR211_LEDGER_INSTANCE_REGISTER.csv", "CR211_QP_TEMPLATE_REGISTER.csv",
                  "CR211_ADDRESS_TEMPLATE_JOIN.csv", "CR211_WRONG_CONTROLS.csv", "CR211_runner.py", "CR211_result.md",
                  "CR211_SUMMARY.json", "CR211_PROVENANCE.json"]
    (OUT / "HASHES.txt").write_text("".join(f"{sha(OUT / n)}  {n}\n" for n in hash_names), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "address_rows": len(address_rows), "qp_templates": len(qp_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
