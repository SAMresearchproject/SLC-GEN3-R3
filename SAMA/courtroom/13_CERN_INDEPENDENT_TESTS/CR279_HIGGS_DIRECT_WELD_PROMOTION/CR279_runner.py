from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


CR_ID = "CR279"
RECORD = "HIGGS_DIRECT_WELD_PROMOTION"
VERDICT_PASS = "PASS_HIGGS_DIRECT_WELD_PROMOTION"
PRECOMMIT_SHA256 = "3e03008ebebf1a1597646b92124b1fef4febda560cc978a874dcefe6ece23ec7"

CR_DIR = Path(__file__).resolve().parent
COURTROOM_ROOT = CR_DIR.parents[1]
G_ROOT = Path("C:/VS/Stam_model-A-v1.0/tests/Substrate")


SOURCES = {
    "G439_output": (
        G_ROOT / "G439_HEAVY_ELECTROWEAK_TOP_SLOT_SELECTOR/G439_output.json",
        "3e499706868b10d4cc4a2b7ecb7c50a494871fec94ae9efb5aed70a6e6cd72cc",
    ),
    "G439_runner_source": (
        G_ROOT / "G439_HEAVY_ELECTROWEAK_TOP_SLOT_SELECTOR/G439_HEAVY_ELECTROWEAK_TOP_SLOT_SELECTOR.py",
        "279d86de713447607e7f390857bdc3e373480b75b250ccd9287e4771c0e960b5",
    ),
    "G444_output": (
        G_ROOT / "G444_WRITE_SECTOR_Q_SLOT_DERIVATION/G444_output.json",
        "96ca5b74cdbb249e8e6128531e202e485932a70621250df3df9c69b584a7fb90",
    ),
    "G444_runner_source": (
        G_ROOT / "G444_WRITE_SECTOR_Q_SLOT_DERIVATION/G444_WRITE_SECTOR_Q_SLOT_DERIVATION.py",
        "aa702ff6a2bd4e236ccec30d12050a450f9ba69fbbedef8d32f81d9e442b7863",
    ),
    "G744c_output": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G744c_Q_A_SOURCE_STRENGTH_BRIDGE/G744c_output.json",
        "5d3ad959d780012190493e661658dc8280c981237c4b9c8adbb128900fde2c1d",
    ),
    "G744c_runner_source": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G744c_Q_A_SOURCE_STRENGTH_BRIDGE/G744c_Q_A_SOURCE_STRENGTH_BRIDGE.py",
        "055829fc7ed42296bed4adff456890fbce7f9b9a3db0b34f385a07d8ec5fcaed",
    ),
    "G745c_output": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE/G745c_output.json",
        "6957514aa88104d22fb870004b51361a1fe201fb4617beb224c01209c352ca21",
    ),
    "G745c_runner_source": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE/G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE.py",
        "e1b8559dfb06aa19f8dfa614f7d0ab205d61a4f314e8ed02106985caa12208da",
    ),
    "G748c_precommit": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G748c_HIGGS_DIRECT_WELD/G748c_PRECOMMIT.md",
        "d31e6dc0c3e5cf889947d3753af5d390e1f6b0e54f6b000753a6e214f5a4f195",
    ),
    "G748c_runner": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G748c_HIGGS_DIRECT_WELD/G748c_runner.py",
        "3520898c9abd2b5679b805378f5b07b4be86daa7878da2f49c413afa9afce3cf",
    ),
    "G748c_summary": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G748c_HIGGS_DIRECT_WELD/G748c_summary.json",
        "244d7f04ba1ec74f5ea4041d7fe1a059764f0aec6e90f63b613842965fe63270",
    ),
    "G748c_result": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G748c_HIGGS_DIRECT_WELD/G748c_result.md",
        "22ed3cf38618dca38e6ada1437fba3ba24913d90cc480bb66827388a0057a64a",
    ),
    "G748c_provenance": (
        G_ROOT / "G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G748c_HIGGS_DIRECT_WELD/G748c_provenance.json",
        "0d5ec5bb3bd5b22ad1370c3b0ad3eaa9978fae5b829f44e830c30cae8bde066d",
    ),
    "CR120_summary": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/CR120_summary.json",
        "887f9ca58dde323f1c0a53cd1c05e3f3a6be6cf1315f3b32c9419799cb726179",
    ),
    "CR120_result": (
        COURTROOM_ROOT / "09a_PARTICLE_MASS_CHAIN/CR120_QP091_HIGGS_EW_PRECISION_ITERATIVE_REFINEMENT_INTAKE/CR120_result.md",
        "5f01ecc521850597af164345d7e9d60fd6709e23bb44eb5a76823e010b170bde",
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


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_checks = verify_sources()

    if not all(row["pass"] for row in source_checks):
        verdict = "INVALID_HIGGS_PROVENANCE"
        summary = {
            "cr_id": CR_ID,
            "record": RECORD,
            "generated_utc": generated_utc,
            "primary_verdict": verdict,
            "source_hashes_pass": False,
            "source_hash_validation": source_checks,
        }
        write_json(CR_DIR / "CR279_summary.json", summary)
        raise SystemExit(f"{CR_ID} {verdict}: source hash validation failed")

    g748c = read_json(SOURCES["G748c_summary"][0])
    g748c_prov = read_json(SOURCES["G748c_provenance"][0])
    direct = g748c["direct_weld"]

    q_h = direct["q_H"]
    m_h = direct["m_H_native_MeV"]
    q_a_h = direct["q_A_H_MeV"]
    r_bounce = direct["r_bounce_H"]
    exact_r_bounce = 1.0 / (64.0 * math.pi)
    exact_ratio = 1.0 + exact_r_bounce
    actual_ratio = q_a_h / m_h

    canonical_checks = [
        {
            "name": "source_verdict_is_G748c_PASS_DIRECT_WELD",
            "pass": g748c.get("primary_verdict") == "PASS_DIRECT_WELD",
        },
        {"name": "q_H_equals_3", "pass": q_h == 3},
        {
            "name": "r_bounce_matches_1_over_64pi",
            "pass": math.isclose(r_bounce, exact_r_bounce, rel_tol=0.0, abs_tol=1e-18),
            "details": {"source": r_bounce, "computed": exact_r_bounce},
        },
        {
            "name": "q_A_ratio_matches_1_plus_1_over_64pi",
            "pass": math.isclose(actual_ratio, exact_ratio, rel_tol=0.0, abs_tol=1e-15),
            "details": {"source": actual_ratio, "computed": exact_ratio},
        },
        {"name": "measured_Higgs_mass_used_false", "pass": g748c.get("measured_Higgs_mass_used") is False},
        {
            "name": "residual_used_to_choose_candidate_false",
            "pass": g748c.get("residual_used_to_choose_candidate") is False,
        },
        {
            "name": "modified_prior_tests_or_CRs_false",
            "pass": g748c.get("modified_prior_tests_or_CRs") is False,
        },
    ]
    wrong_controls = g748c.get("wrong_controls", [])
    wrong_control_checks = [
        {"name": row["name"], "pass": bool(row.get("pass")), "details": row.get("details", {})}
        for row in wrong_controls
    ]
    all_checks_pass = all(row["pass"] for row in canonical_checks + wrong_control_checks)
    verdict = VERDICT_PASS if all_checks_pass else "FAIL_HIGGS_DIRECT_WELD_REPLAY"

    typed_contract = {
        "cr_id": CR_ID,
        "primary_verdict": verdict,
        "typed_outputs": [
            {
                "type": "ResolvedHiggsASourceOntology",
                "source": "G439 + G444 + G748c",
                "status": "resolved",
            },
            {
                "type": "HiggsQSlotRole",
                "q": 3,
                "formula": "q_H = 3",
                "source": "G439/G444",
            },
            {
                "type": "HiggsBounceRatio",
                "exact": "1/(64*pi)",
                "decimal": r_bounce,
                "source": "CR120/G744c/G748c",
            },
            {
                "type": "HiggsASourceReadout",
                "symbol": "q_A,H",
                "formula": "q_A,H = m_H_native * (1 + 1/(64*pi))",
                "m_H_native_MeV": m_h,
                "q_A_H_MeV": q_a_h,
                "mass_input_source": "G745c scalar formula output, not measured Higgs target",
            },
            {
                "type": "HiggsASourceRatio",
                "symbol": "q_A,H/m_H",
                "exact": "1 + 1/(64*pi)",
                "decimal": actual_ratio,
            },
        ],
        "registration_recommendation": "register as Higgs A-source typed promotion in SAM Language v0.3; do not use as formula search",
    }

    provenance = {
        "cr_id": CR_ID,
        "record": RECORD,
        "generated_utc": generated_utc,
        "precommit_sha256": PRECOMMIT_SHA256,
        "source_hash_validation": source_checks,
        "g748c_source_contracts": g748c_prov.get("source_contracts", []),
        "forbidden_inputs": g748c_prov.get("forbidden_inputs", {}),
        "legal_composition": g748c_prov.get("legal_composition", {}),
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
        "canonical_checks_pass": all(row["pass"] for row in canonical_checks),
        "wrong_controls_pass": all(row["pass"] for row in wrong_control_checks),
        "typed_outputs_count": len(typed_contract["typed_outputs"]),
        "measured_Higgs_mass_used": False,
        "residual_used_to_choose_candidate": False,
        "modified_prior_tests_or_CRs": False,
        "direct_weld": {
            "q_H": q_h,
            "r_bounce_H_exact": "1/(64*pi)",
            "r_bounce_H_decimal": r_bounce,
            "m_H_native_MeV": m_h,
            "q_A_H_MeV": q_a_h,
            "q_A_H_over_m_H_exact": "1 + 1/(64*pi)",
            "q_A_H_over_m_H_decimal": actual_ratio,
        },
        "canonical_checks": canonical_checks,
        "wrong_controls": wrong_control_checks,
    }

    result_lines = [
        "# CR279 Higgs Direct-Weld Promotion Result",
        "",
        f"generated_utc: {generated_utc}",
        f"primary_verdict: {verdict}",
        "execution_status: CLEAN",
        "",
        "## Typed Chain",
        "",
        "```text",
        "Resolved Higgs ontology",
        "-> q_H = 3",
        "-> r_bounce,H = 1/(64*pi)",
        "-> q_A,H = m_H_native * (1 + r_bounce,H)",
        "-> Higgs A-source readout",
        "```",
        "",
        "## Replay Values",
        "",
        f"- m_H_native_MeV: {m_h:.17g}",
        "- m_H source: G745c scalar formula output, not measured Higgs target",
        "- r_bounce,H exact: 1/(64*pi)",
        f"- r_bounce,H decimal: {r_bounce:.18f}",
        f"- q_A,H_MeV: {q_a_h:.17g}",
        "- q_A,H / m_H exact: 1 + 1/(64*pi)",
        f"- q_A,H / m_H decimal: {actual_ratio:.18f}",
        "",
        "## Wrong Controls",
        "",
    ]
    for row in wrong_control_checks:
        status = "PASS" if row["pass"] else "FAIL"
        result_lines.append(f"- [{status}] {row['name']}")
    result_lines.extend(
        [
            "",
            "## Boundaries Preserved",
            "",
            "- CR120 remains a neighboring boundary/intake record; this CR does not rewrite it.",
            "- G748c remains the source direct-weld result; this CR promotes it without mutation.",
            "- No measured Higgs target or observed residual entered the derivation path.",
            "",
            "## Verdict Statement",
            "",
            f"{verdict}. The G748c direct weld is promoted as a typed Courtroom record.",
            "",
        ]
    )

    write_json(CR_DIR / "CR279_summary.json", summary)
    write_json(CR_DIR / "CR279_provenance.json", provenance)
    write_json(CR_DIR / "CR279_typed_contract.json", typed_contract)
    (CR_DIR / "CR279_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    artifacts = [
        "CR279_PRECOMMIT.md",
        "CR279_runner.py",
        "CR279_result.md",
        "CR279_summary.json",
        "CR279_provenance.json",
        "CR279_typed_contract.json",
    ]
    hash_lines = [f"{sha256(CR_DIR / name)}  {name}" for name in artifacts]
    (CR_DIR / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    if verdict != VERDICT_PASS:
        raise SystemExit(f"{CR_ID} {verdict}")


if __name__ == "__main__":
    main()
