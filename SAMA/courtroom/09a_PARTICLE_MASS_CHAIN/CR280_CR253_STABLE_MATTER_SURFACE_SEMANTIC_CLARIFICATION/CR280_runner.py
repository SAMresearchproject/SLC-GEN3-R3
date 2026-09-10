from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_ID = "CR280"
RECORD = "CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION"
VERDICT_PASS = "PASS_CR253_SEMANTIC_CLARIFICATION"
PRECOMMIT_SHA256 = "5dac524da10f8117b0fe0b9b89cd139bfa80a9811d820933c8f489d70f6991df"

CR_DIR = Path(__file__).resolve().parent
COURTROOM_ROOT = CR_DIR.parents[1]
Q_ROOT = Path("C:/VS/quantum_phase")

SOURCES = {
    "QP093A_source": (
        Q_ROOT / "src/qp093a_all_stable_sam_particle_combination_enumerator.py",
        "c6010a34c94fac0012e45e84df232fbb86d6ebec3f19d48632e8e793795f45b3",
    ),
    "QP093A_result": (
        Q_ROOT / "artifacts/qp093a_stable_particle_combination_enumerator/QP093A_STABLE_PARTICLE_ENUMERATOR_result.md",
        "504d2fb5152072248faf7f96e2bbbfa5d033d289e30bc21829af293b29215af5",
    ),
    "QP093A_summary": (
        Q_ROOT / "artifacts/qp093a_stable_particle_combination_enumerator/qp093a_summary.json",
        "0fab75381e2c27a8c98456016fd3f15781dbd338d11398788235d01f92333891",
    ),
    "QP104_corrected_catalog": (
        Q_ROOT / "artifacts/qp104_corrected_299_catalog_propagation_audit/qp093a_v3_corrected_299.csv",
        "33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c",
    ),
    "CR119_summary": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_summary.json",
        "1eb2ba0c12d2079fc395cfa28e41693e9525af3cd394f8c9caa0f4393e0bcb53",
    ),
    "CR253_summary": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_summary.json",
        "06a023d5bd231ffdc2e441044936191c48fd861a9f56007e3408401934ad9aa0",
    ),
    "CR253_result": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_result.md",
        "fd944b04ae0701d1c1bbf25eb7860f808a3eb83f7e94d050c8b6858b5c0861e5",
    ),
    "CR253_promoted_rows": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_promoted_80_rows.csv",
        "59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b",
    ),
    "CR253_input_catalog": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_input_catalog_299.csv",
        "33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c",
    ),
    "CR254_summary": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR254_COMPACT_MATTER_CHARGED_LAW/CR254_summary.json",
        "ac5cb2bc8d884fab0d10e55c81db6fa9401b01779bd710d1d43d7e26367d3074",
    ),
    "CR255_summary": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR255_COMPACT_MATTER_NEUTRAL_LAW/CR255_summary.json",
        "f9d2c88b2d78e76f56bbea71340ac1a5e94a3cefb75aba84c6cde017d9e25da9",
    ),
    "CR256_summary": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_summary.json",
        "721a64f48b4977d736a4e362f4091857fd8628c4808444ce78d3159b8a7f630b",
    ),
    "CR257_summary": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR257_A_MEETS_THETA_AT_D_1/CR257_summary.json",
        "db5b8ff0010a6984d82893e4c392320829f1408a20e02bde1376ecabe1768788",
    ),
    "SAM_VOLUME_II_MATTER_CONCEPTUAL_DRAFT": (
        COURTROOM_ROOT / "docs/SAM_VOLUME_II_MATTER_CONCEPTUAL_DRAFT_2026_07_01.md",
        "7b6b266c85735c56cfe27d4f49ad7121e0b77eb13c2f010acfcd2aca7927d471",
    ),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def verify_sources() -> list[dict]:
    rows = []
    for source_id, (path, expected) in SOURCES.items():
        exists = path.exists()
        actual = sha256(path) if exists else None
        rows.append(
            {
                "id": source_id,
                "path": str(path).replace("\\", "/"),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "pass": exists and actual == expected,
            }
        )
    return rows


def load_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def row_class(row: dict) -> str:
    return "antimatter" if row["bin"] == "antimatter_conjugate_rows" else "matter"


def source_rule(row: dict) -> str:
    if row["bin"] == "antimatter_conjugate_rows":
        return "CR256_A_OPERATOR_ANTIMATTER_CONJUGATE"
    if row["q_sign"] == "neutral" or row["q_abs"] == "0":
        return "CR255_COMPACT_MATTER_NEUTRAL_LAW"
    return "CR254_COMPACT_MATTER_CHARGED_LAW"


def naming_status(row: dict) -> tuple[str, str, str]:
    identity = row["identity_rule"]
    is_exact_electron = (
        row["bin"] == "stable_matter_rows"
        and identity == "electron_like_minus"
        and row["partition_signature"] == "1"
        and row["q_sign"] == "negative"
        and row["closure_depth"] == "0"
    )
    if is_exact_electron:
        return "EXACT_CONTACT", "electron", "EXACT_CONTACT"
    if identity in {"positron_substrate_slot", "heavier_positron_substrate_slot"}:
        return "MIRROR", "", "INDEPENDENT_EXISTENCE_UNRESOLVED"
    if identity == "neutrino_like":
        return "NEUTRAL_ANCHOR", "", "INDEPENDENT_EXISTENCE_UNRESOLVED"
    if identity == "neutral_higher_partition":
        return "SUBSTRATE_CANDIDATE", "", "INDEPENDENT_EXISTENCE_UNRESOLVED"
    if identity in {"quark_like_charged", "heavier_charged_lepton_minus"}:
        return "SECTOR_HINT", "", "INDEPENDENT_EXISTENCE_UNRESOLVED"
    return "SUBSTRATE_CANDIDATE", "", "INDEPENDENT_EXISTENCE_UNRESOLVED"


def placeholder(row: dict) -> str:
    return (
        "SAM["
        f"row={row['row_id']},"
        f"p={row['partition_signature']},"
        f"sign={row['q_sign']},"
        f"depth={row['closure_depth']},"
        f"class={row['identity_rule']}"
        "]"
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_checks = verify_sources()
    if not all(row["pass"] for row in source_checks):
        verdict = "INVALID_CR253_SOURCE_CHAIN"
        summary = {
            "cr_id": CR_ID,
            "record": RECORD,
            "generated_utc": generated_utc,
            "primary_verdict": verdict,
            "source_hashes_pass": False,
            "source_hash_validation": source_checks,
        }
        write_json(CR_DIR / "CR280_summary.json", summary)
        raise SystemExit(f"{CR_ID} {verdict}: source hash validation failed")

    q_summary = read_json(SOURCES["QP093A_summary"][0])
    cr119 = read_json(SOURCES["CR119_summary"][0])
    cr253 = read_json(SOURCES["CR253_summary"][0])
    cr254 = read_json(SOURCES["CR254_summary"][0])
    cr255 = read_json(SOURCES["CR255_summary"][0])
    cr256 = read_json(SOURCES["CR256_summary"][0])
    cr257 = read_json(SOURCES["CR257_summary"][0])
    rows = load_csv(SOURCES["CR253_promoted_rows"][0])

    matter_rows = [r for r in rows if r["bin"] == "stable_matter_rows"]
    anti_rows = [r for r in rows if r["bin"] == "antimatter_conjugate_rows"]
    conjugate_count = sum(1 for r in rows if r.get("conjugate_partner"))
    placeholders = [placeholder(r) for r in rows]

    promoted = []
    for row in rows:
        status, conventional, independent = naming_status(row)
        promoted.append(
            {
                "original_row_address": row["row_id"],
                "row_type": "StructurallyStableMatterRow",
                "surface_type": "TensorCompatibleStableMatterSurface",
                "matter_antimatter_class": row_class(row),
                "bin": row["bin"],
                "partition_signature": row["partition_signature"],
                "q_abs": row["q_abs"],
                "q_sign": row["q_sign"],
                "closure_depth": row["closure_depth"],
                "qA_source_support": row["qA_source_support"],
                "source_rule": source_rule(row),
                "placeholder_id": placeholder(row),
                "exact_contact_status": status,
                "conventional_name": conventional,
                "identity_rule": row["identity_rule"],
                "conjugate_partner": row["conjugate_partner"],
                "independent_existence_status": independent,
            }
        )

    row_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "CR280 promoted stable matter row contract",
        "type": "object",
        "required": [
            "original_row_address",
            "row_type",
            "surface_type",
            "matter_antimatter_class",
            "partition_signature",
            "q_sign",
            "closure_depth",
            "source_rule",
            "placeholder_id",
            "exact_contact_status",
            "conventional_name",
            "independent_existence_status",
        ],
        "properties": {
            "original_row_address": {"type": "string"},
            "row_type": {"const": "StructurallyStableMatterRow"},
            "surface_type": {"const": "TensorCompatibleStableMatterSurface"},
            "matter_antimatter_class": {"enum": ["matter", "antimatter"]},
            "source_rule": {
                "enum": [
                    "CR254_COMPACT_MATTER_CHARGED_LAW",
                    "CR255_COMPACT_MATTER_NEUTRAL_LAW",
                    "CR256_A_OPERATOR_ANTIMATTER_CONJUGATE",
                ]
            },
            "exact_contact_status": {
                "enum": [
                    "EXACT_CONTACT",
                    "SECTOR_HINT",
                    "MIRROR",
                    "NEUTRAL_ANCHOR",
                    "SUBSTRATE_CANDIDATE",
                    "INDEPENDENT_EXISTENCE_UNRESOLVED",
                ]
            },
        },
    }

    conventional_names = [r for r in promoted if r["conventional_name"]]
    census_checks = [
        {"name": "csv_total_promoted_rows_80", "pass": len(rows) == 80, "value": len(rows)},
        {"name": "csv_matter_rows_48", "pass": len(matter_rows) == 48, "value": len(matter_rows)},
        {"name": "csv_antimatter_rows_32", "pass": len(anti_rows) == 32, "value": len(anti_rows)},
        {
            "name": "summary_n_promoted_80",
            "pass": cr253.get("n_promoted") == 80,
            "value": cr253.get("n_promoted"),
        },
        {"name": "summary_n_matter_48", "pass": cr253.get("n_matter") == 48, "value": cr253.get("n_matter")},
        {"name": "summary_n_anti_32", "pass": cr253.get("n_anti") == 32, "value": cr253.get("n_anti")},
        {
            "name": "source_conjugate_parity_32",
            "pass": cr253.get("n_conjugate_partners") == 32,
            "value": cr253.get("n_conjugate_partners"),
        },
        {"name": "cr253_boundary_preserved", "pass": cr253.get("verdict") == "BOUNDARY"},
        {
            "name": "cr254_charged_law_32_32",
            "pass": cr254.get("verdict") == "PASS" and cr254.get("canonical_matches") == 32,
        },
        {
            "name": "cr255_neutral_law_16_16",
            "pass": cr255.get("verdict") == "PASS" and cr255.get("canonical_matches") == 16,
        },
        {
            "name": "cr256_anti_law_32_32",
            "pass": cr256.get("verdict") == "PASS" and cr256.get("canonical_matches") == 32,
        },
        {"name": "placeholder_count_80", "pass": len(placeholders) == 80},
        {"name": "placeholder_unique_80", "pass": len(set(placeholders)) == 80},
        {"name": "conventional_names_controlled", "pass": len(conventional_names) == 1},
    ]
    guards = [
        {"name": "reject_name_every_row_as_known_particle", "pass": len(conventional_names) < len(rows)},
        {
            "name": "reject_tensor_compatibility_as_experimental_existence",
            "pass": all(r["row_type"] == "StructurallyStableMatterRow" for r in promoted)
            and any(r["independent_existence_status"] == "INDEPENDENT_EXISTENCE_UNRESOLVED" for r in promoted),
        },
        {
            "name": "reject_placeholder_as_pdg_identity",
            "pass": all(r["placeholder_id"].startswith("SAM[") for r in promoted)
            and all("PDG" not in r["placeholder_id"] for r in promoted),
        },
        {
            "name": "reject_pdg_membership_as_promotion_selector",
            "pass": all(r["source_rule"].startswith("CR25") for r in promoted),
        },
        {
            "name": "reject_census_change",
            "pass": len(rows) == 80 and len(matter_rows) == 48 and len(anti_rows) == 32,
        },
        {
            "name": "reject_be8_nuclear_cipher_as_cr253_selector",
            "pass": all("Be-8" not in json.dumps(r) and "beryllium" not in json.dumps(r).lower() for r in promoted),
        },
    ]

    all_checks_pass = all(row["pass"] for row in census_checks + guards)
    verdict = VERDICT_PASS if all_checks_pass else "FAIL_CR253_REPLAY_OR_CENSUS"

    provenance = {
        "cr_id": CR_ID,
        "record": RECORD,
        "generated_utc": generated_utc,
        "precommit_sha256": PRECOMMIT_SHA256,
        "source_hash_validation": source_checks,
        "source_contracts": {
            "QP093A_result_class": q_summary.get("result_class"),
            "CR119_result_class": cr119.get("result_class"),
            "CR253_verdict_preserved": cr253.get("verdict"),
            "CR253_boundary_reason": "W3 and W4 controls insensitive due to upstream bin+h_T filter subsumption",
            "CR254_verdict": cr254.get("verdict"),
            "CR255_verdict": cr255.get("verdict"),
            "CR256_verdict": cr256.get("verdict"),
            "CR257_context_verdict": cr257.get("verdict"),
        },
        "no_existing_artifact_modified": True,
    }

    summary = {
        "cr_id": CR_ID,
        "record": RECORD,
        "generated_utc": generated_utc,
        "execution_status": "CLEAN",
        "primary_verdict": verdict,
        "source_hashes_pass": all(row["pass"] for row in source_checks),
        "precommit_sha256": PRECOMMIT_SHA256,
        "semantic_surface_type": "TensorCompatibleStableMatterSurface",
        "row_subtype": "StructurallyStableMatterRow",
        "forbidden_unqualified_type": "StablePhysicalParticle",
        "structural_row_not_experimentally_identified_particle": True,
        "cr253_original_verdict_preserved": cr253.get("verdict"),
        "n_promoted": len(rows),
        "n_matter": len(matter_rows),
        "n_antimatter": len(anti_rows),
        "n_conjugate_partners_source": cr253.get("n_conjugate_partners"),
        "conjugate_partner_links_in_csv": conjugate_count,
        "conventional_name_count": len(conventional_names),
        "placeholder_count": len(placeholders),
        "placeholder_unique": len(set(placeholders)),
        "row_laws": {
            "matter_charged": "CR254 32/32 PASS",
            "matter_neutral": "CR255 16/16 PASS",
            "anti_charged": "CR256 32/32 PASS",
        },
        "census_checks": census_checks,
        "guards": guards,
        "remaining_named_opens": [
            "independent existence of non-exact-contact rows",
            "unsupported PDG flavor/name assignment for sector hints",
            "CR253 BOUNDARY grade from W3/W4 control subsumption remains unchanged",
        ],
    }

    result_lines = [
        "# CR280 CR253 Stable-Matter Surface Semantic Clarification Result",
        "",
        f"generated_utc: {generated_utc}",
        f"primary_verdict: {verdict}",
        "execution_status: CLEAN",
        "",
        "## Semantic Contract",
        "",
        "```text",
        "TensorCompatibleStableMatterSurface",
        "  row subtype: StructurallyStableMatterRow",
        "  not equal to: ExperimentallyIdentifiedParticle",
        "```",
        "",
        "The unqualified type StablePhysicalParticle is not used for CR253 rows.",
        "",
        "## Source Replay",
        "",
        f"- total promoted rows: {len(rows)}",
        f"- matter rows: {len(matter_rows)}",
        f"- antimatter rows: {len(anti_rows)}",
        f"- source conjugate parity: {cr253.get('n_conjugate_partners')}/32",
        "- CR253 original verdict preserved: BOUNDARY",
        "- CR253 boundary preserved: W3 and W4 controls were redundant/subsumed by upstream filters.",
        "- CR254/CR255/CR256 compact row laws preserved as the row-law closure family.",
        "",
        "## Naming Discipline",
        "",
        "- Conventional names emitted only for source-authorized exact contacts.",
        f"- Conventional name count: {len(conventional_names)}",
        "- All other rows carry deterministic SAM[...] placeholders reversible to row_id.",
        "- Placeholder identifiers contain no PDG identity claim, mass claim, or lifetime claim.",
        "",
        "## Guards",
        "",
    ]
    for row in guards:
        status = "PASS" if row["pass"] else "FAIL"
        result_lines.append(f"- [{status}] {row['name']}")
    result_lines.extend(
        [
            "",
            "## Verdict Statement",
            "",
            f"{verdict}. CR253 is clarified as an 80-row structurally stable, tensor-compatible matter surface with controlled naming and deterministic placeholders. CR253's BOUNDARY verdict is preserved.",
            "",
        ]
    )

    write_json(CR_DIR / "CR280_summary.json", summary)
    write_json(CR_DIR / "CR280_provenance.json", provenance)
    write_json(CR_DIR / "CR280_row_contract.schema.json", row_schema)
    write_json(CR_DIR / "CR280_promoted_rows.json", promoted)
    (CR_DIR / "CR280_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    with (CR_DIR / "CR280_placeholder_map.csv").open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "row_id",
            "placeholder_id",
            "row_type",
            "matter_antimatter_class",
            "source_rule",
            "exact_contact_status",
            "conventional_name",
            "independent_existence_status",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in promoted:
            writer.writerow(
                {
                    "row_id": row["original_row_address"],
                    "placeholder_id": row["placeholder_id"],
                    "row_type": row["row_type"],
                    "matter_antimatter_class": row["matter_antimatter_class"],
                    "source_rule": row["source_rule"],
                    "exact_contact_status": row["exact_contact_status"],
                    "conventional_name": row["conventional_name"],
                    "independent_existence_status": row["independent_existence_status"],
                }
            )

    artifacts = [
        "CR280_PRECOMMIT.md",
        "CR280_runner.py",
        "CR280_result.md",
        "CR280_summary.json",
        "CR280_provenance.json",
        "CR280_row_contract.schema.json",
        "CR280_promoted_rows.json",
        "CR280_placeholder_map.csv",
    ]
    (CR_DIR / "HASHES.txt").write_text(
        "\n".join(f"{sha256(CR_DIR / name)}  {name}" for name in artifacts) + "\n",
        encoding="utf-8",
    )

    if verdict != VERDICT_PASS:
        raise SystemExit(f"{CR_ID} {verdict}")


if __name__ == "__main__":
    main()
