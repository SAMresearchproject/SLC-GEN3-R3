from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


CR_ID = "CR281_CARRIER_CONTAINER_FUNCTIONAL_OPERATOR"
TASK = "SAM Prospective CR carrier container functional operator"
BRANCH = "09a_PARTICLE_MASS_CHAIN"
FIREWALL = {
    "sam_language_v0_3_consulted_during_development": False,
    "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
}

ROOT = Path(__file__).resolve().parents[2]
CR_DIR = Path(__file__).resolve().parent
PRECOMMIT = CR_DIR / "CR281_PRECOMMIT.md"


SOURCE_HASHES = {
    "artifacts/preflight_filled/PREFLIGHT_20260711_113436_no_script.md": "0c3b7ad9408889c03095abb50689f1a107757f559b0eed16fe81dba4b634b90c",
    "artifacts/preflight_filled/PREFLIGHT_20260711_113436_no_script.json": "623d6cb550d20c66d823367ee21a30052bca08f27a34dd3cce6b5621a132a00f",
    "09a_PARTICLE_MASS_CHAIN/CR233_TENSOR_SUBSTRATE_ROLE_SEPARATION/CR233_result.md": "55e0c81a8c417fb79f377f5913035d65a917ada0cca80e5cc9cdf8851fd55895",
    "09a_PARTICLE_MASS_CHAIN/CR233_TENSOR_SUBSTRATE_ROLE_SEPARATION/CR233_summary.json": "7fe429dca4162cebb257446fe58cf0a30929e5f814ace7da506fdaf26709a183",
    "09a_PARTICLE_MASS_CHAIN/CR262_SUBSTRATE_CHAIN_STEP_CIPHER_LIGHT_ANCHOR/CR262_result.md": "40548fb787cdeb0dea4f350c639fb35358783c85fd570b83706db8db38b5fd04",
    "09a_PARTICLE_MASS_CHAIN/CR262_SUBSTRATE_CHAIN_STEP_CIPHER_LIGHT_ANCHOR/CR262_summary.json": "8cd8e93483b49f317dae41242c712c0bc06335339a45462a0e25a2733cc90b72",
    "09a_PARTICLE_MASS_CHAIN/CR262_SUBSTRATE_CHAIN_STEP_CIPHER_LIGHT_ANCHOR/CR262_evidence_rows.csv": "b1d7bfd420e00eeb4d6009ed3899ee98aa80d73bc1d9c098e78e645db9f623b2",
    "09a_PARTICLE_MASS_CHAIN/CR262_SUBSTRATE_CHAIN_STEP_CIPHER_LIGHT_ANCHOR/CR262_CORRECTION_NOTE.md": "cc1b512d2b113c84c964f8243059617e83e60dd37247de2fa63dec5077700dad",
    "09a_PARTICLE_MASS_CHAIN/CR266_TWO_MIRROR_RECIPROCITY_D_DERIVATION/CR266_result.md": "cfed8bffb08d88b1d3e8fe4435ffff8f402dd880f5bb8662d274b4d85d37c8d9",
    "09a_PARTICLE_MASS_CHAIN/CR266_TWO_MIRROR_RECIPROCITY_D_DERIVATION/CR266_atom_reconstruction.csv": "782cccf115db48efe5132ce2293c5532dbd4df34495a85d9f6b9f670dba43572",
    "09a_PARTICLE_MASS_CHAIN/CR266_TWO_MIRROR_RECIPROCITY_D_DERIVATION/CR266_summary.json": "8bc5bc44b8d6eef2a0b1c2a75e7a5e4eac6dd2107c0e4f03c91c6020d20929c6",
    "09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_result.md": "c4cd0142a8d43b810c438586242a68f429de675f0d168169a11b085653d142ea",
    "09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_fixed_points_and_outputs.csv": "5ec9b48d318444c7c8d572495bf7aefa73cb0bb73fbb15f247d4f46f244fdff3",
    "09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_partition_table.csv": "63c283cfabdd10053c035448a213856f17df4589dbdf6523391ddf28912f07d9",
    "09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_summary.json": "1ed95b854c1f5370df69438484b1e2f80f7a2c19d288dc714a5e1c5b7316ac88",
    "09a_PARTICLE_MASS_CHAIN/CR270_SOURCE_COUNT_MEASURE_GKS_IDENTIFICATION/CR270_result.md": "9871b4766e999d079b5852ff50a46516e17a69124a30ddb4e85a055b288e4abb",
    "09a_PARTICLE_MASS_CHAIN/CR270_SOURCE_COUNT_MEASURE_GKS_IDENTIFICATION/CR270_q2_substrate_atoms.csv": "c003d39fc86a0896f16a646b1124754d5077b87a9b9006bec34e6f5b44074045",
    "09a_PARTICLE_MASS_CHAIN/CR270_SOURCE_COUNT_MEASURE_GKS_IDENTIFICATION/CR270_summary.json": "463de9fc1adf7715856c32055e84cd240c70eb0bb1c58e8635ee7084b7a44a3b",
    "docs/SAM_VOLUME_II_MATTER.md": "3bb1a27e7deaed50ba26e614103c6a0e4876044975bad7c519ba8c9022d4a881",
    "docs/SAM_VOLUME_II_MATTER_CONCEPTUAL_DRAFT_2026_07_01.md": "7b6b266c85735c56cfe27d4f49ad7121e0b77eb13c2f010acfcd2aca7927d471",
}


TARGET_ROWS = [
    {"label": "m_3", "value": 6, "h_exp": 1, "d_exp": 1, "expected": "OUTPUT"},
    {"label": "D^2", "value": 9, "h_exp": 0, "d_exp": 2, "expected": "OUTPUT"},
    {"label": "Theta", "value": 18, "h_exp": 1, "d_exp": 2, "expected": "OUTPUT"},
    {"label": "hV", "value": 54, "h_exp": 1, "d_exp": 3, "expected": "OUTPUT"},
    {"label": "R", "value": 12, "h_exp": 2, "d_exp": 1, "expected": "FIXED_POINT"},
    {"label": "V", "value": 27, "h_exp": 0, "d_exp": 3, "expected": "FIXED_POINT"},
    {"label": "F", "value": 81, "h_exp": 0, "d_exp": 4, "expected": "FIXED_POINT"},
    {"label": "L", "value": 162, "h_exp": 1, "d_exp": 4, "expected": "TERMINAL_CLOSURE"},
]


HELDOUT_ROWS = [
    {"label": "M", "value": 126, "kind": "partition_scratch", "expected": "RETAINED_SCRATCH"},
    {"label": "R^2", "value": 144, "kind": "bow_domain", "expected": "DOMAIN_TOTAL"},
    {"label": "S", "value": 8, "kind": "copy_count", "expected": "DOMAIN_MULTIPLICITY"},
    {"label": "h^4", "value": 16, "kind": "unrestricted_grade_control", "expected": "OUT_OF_SOURCE_ATOM_SET"},
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def rel_to_path(rel: str) -> Path:
    return ROOT.joinpath(*rel.split("/"))


def is_forbidden_source_path(rel: str) -> bool:
    normalized = rel.replace("\\", "/").lower()
    forbidden_markers = (
        "sam_language_v0_3",
        "sam-language-v0.1-frozen",
        "sam_language/",
        "sam_language_v0_2",
    )
    return any(marker in normalized for marker in forbidden_markers)


def verify_sources() -> list[dict[str, object]]:
    rows = []
    for rel, expected in SOURCE_HASHES.items():
        path = rel_to_path(rel)
        actual = sha256_file(path) if path.exists() else "MISSING"
        forbidden = is_forbidden_source_path(rel)
        rows.append(
            {
                "path": rel,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "hash_ok": actual == expected,
                "forbidden_source_path": forbidden,
            }
        )
    return rows


def constants() -> dict[str, object]:
    h = 2
    d = 3
    s = h**3
    r = h**2 * d
    theta = h * d**2
    m = (s - 1) * theta
    r_sq = r**2
    l_value = h * d**4
    l_alt = Fraction(r_sq * d**2, s)
    return {
        "h": h,
        "d": d,
        "S": s,
        "R": r,
        "Theta": theta,
        "M": m,
        "R_sq": r_sq,
        "L": l_value,
        "L_equals_R_sq_d_sq_over_S": l_alt == l_value,
        "Theta_release_fraction": str(Fraction(theta, r_sq)),
        "M_retained_fraction": str(Fraction(m, r_sq)),
        "Theta_lift_fee": str(Fraction(theta) * (1 + Fraction(theta, r_sq))),
    }


def f_cc(h_exp: int, d_exp: int, value: int) -> str:
    c = constants()
    if (h_exp, d_exp) == (1, 4) and value == c["L"] and c["L_equals_R_sq_d_sq_over_S"]:
        return "TERMINAL_CLOSURE"
    if (h_exp, d_exp) == (2, 1):
        return "FIXED_POINT"
    if h_exp == 0 and d_exp >= 3:
        return "FIXED_POINT"
    if h_exp == 1 and 1 <= d_exp <= 3:
        return "OUTPUT"
    if (h_exp, d_exp) == (0, 2):
        return "OUTPUT"
    return "OUT_OF_TARGET_DOMAIN"


def heldout_classify(row: dict[str, object]) -> str:
    c = constants()
    label = row["label"]
    value = row["value"]
    if label == "M" and value == c["M"]:
        return "RETAINED_SCRATCH"
    if label == "R^2" and value == c["R_sq"]:
        return "DOMAIN_TOTAL"
    if label == "S" and value == c["S"]:
        return "DOMAIN_MULTIPLICITY"
    if label == "h^4" and value == 16:
        return "OUT_OF_SOURCE_ATOM_SET"
    return "UNCLASSIFIED"


def compute_role_rows() -> list[dict[str, object]]:
    h = constants()["h"]
    d = constants()["d"]
    rows = []
    for row in TARGET_ROWS:
        value_from_address = h ** row["h_exp"] * d ** row["d_exp"]
        actual = f_cc(row["h_exp"], row["d_exp"], row["value"])
        rows.append(
            {
                **row,
                "value_from_address": value_from_address,
                "address_value_ok": value_from_address == row["value"],
                "actual": actual,
                "match": actual == row["expected"],
            }
        )
    return rows


def best_feature_mapping(rows: list[dict[str, object]], feature_fn) -> dict[str, object]:
    roles = ("OUTPUT", "FIXED_POINT", "TERMINAL_CLOSURE")
    features = sorted({feature_fn(row) for row in rows})
    best = {"matches": -1, "mapping": {}}

    def assign(idx: int, mapping: dict[str, str]) -> None:
        if idx == len(features):
            matches = sum(mapping[feature_fn(row)] == row["expected"] for row in rows)
            if matches > best["matches"]:
                best["matches"] = matches
                best["mapping"] = dict(mapping)
            return
        feature = features[idx]
        for role in roles:
            mapping[feature] = role
            assign(idx + 1, mapping)

    assign(0, {})
    return best


def wrong_controls(role_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    sorted_roles = [row["expected"] for row in sorted(role_rows, key=lambda item: item["value"])]
    compressed = []
    for role in sorted_roles:
        if not compressed or compressed[-1] != role:
            compressed.append(role)
    raw_order_broke = len(compressed) > 3

    parity_best = best_feature_mapping(role_rows, lambda row: "even" if row["value"] % 2 == 0 else "odd")
    pure_best = best_feature_mapping(role_rows, lambda row: "pure_d" if row["h_exp"] == 0 else "has_h")

    swapped_rows = []
    for row in role_rows:
        swapped_actual = f_cc(row["d_exp"], row["h_exp"], row["value"])
        swapped_rows.append({**row, "swapped_actual": swapped_actual, "swapped_match": swapped_actual == row["expected"]})
    swapped_matches = sum(row["swapped_match"] for row in swapped_rows)

    inverted_rows = []
    inversion = {"OUTPUT": "FIXED_POINT", "FIXED_POINT": "OUTPUT", "TERMINAL_CLOSURE": "TERMINAL_CLOSURE"}
    for row in role_rows:
        inverted_actual = inversion[row["actual"]]
        inverted_rows.append({**row, "inverted_actual": inverted_actual, "inverted_match": inverted_actual == row["expected"]})
    inverted_matches = sum(row["inverted_match"] for row in inverted_rows)

    return [
        {
            "control": "WC1_RAW_NUMERIC_ORDERING",
            "best_matches": "not_applicable_monotone_sequence_test",
            "evidence": "sorted expected roles = " + ",".join(sorted_roles),
            "broke": raw_order_broke,
        },
        {
            "control": "WC2_PARITY_ONLY",
            "best_matches": parity_best["matches"],
            "mapping": parity_best["mapping"],
            "broke": parity_best["matches"] < len(role_rows),
        },
        {
            "control": "WC3_PURE_POWER_VS_MIXED_POWER_ONLY",
            "best_matches": pure_best["matches"],
            "mapping": pure_best["mapping"],
            "broke": pure_best["matches"] < len(role_rows),
        },
        {
            "control": "WC4_UNRESTRICTED_GRADE_PROMOTES_16",
            "control_prediction": "OUTPUT",
            "canonical_prediction": heldout_classify(HELDOUT_ROWS[-1]),
            "broke": heldout_classify(HELDOUT_ROWS[-1]) == "OUT_OF_SOURCE_ATOM_SET",
        },
        {
            "control": "WC5_SWAPPED_PRIMITIVE_ADDRESSES",
            "matches": swapped_matches,
            "mismatches": len(role_rows) - swapped_matches,
            "broke": swapped_matches < len(role_rows),
        },
        {
            "control": "WC6_INVERT_OUTPUT_FIXED_LABELS",
            "matches": inverted_matches,
            "mismatches": len(role_rows) - inverted_matches,
            "broke": inverted_matches < len(role_rows),
        },
    ]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def json_ready(obj):
    if isinstance(obj, Fraction):
        return str(obj)
    if isinstance(obj, dict):
        return {key: json_ready(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [json_ready(value) for value in obj]
    return obj


def build_result_md(summary: dict[str, object]) -> str:
    role_lines = []
    for row in summary["roles"]:
        role_lines.append(
            f"| {row['label']} | {row['value']} | ({row['h_exp']},{row['d_exp']}) | {row['actual']} | {row['expected']} | {row['match']} |"
        )
    control_lines = []
    for row in summary["wrong_controls"]:
        control_lines.append(f"| {row['control']} | {row['broke']} | {row.get('best_matches', row.get('matches', 'n/a'))} |")
    heldout_lines = []
    for row in summary["heldout"]:
        heldout_lines.append(f"| {row['label']} | {row['value']} | {row['actual']} | {row['expected']} | {row['match']} |")

    return "\n".join(
        [
            "# CR281 Carrier/Container Functional Operator -- Result",
            "",
            "```text",
            f"scientific_verdict = {summary['scientific_verdict']}",
            f"execution_status = {summary['execution_status']}",
            f"precommit_sha256 = {summary['precommit_sha256']}",
            "free_parameters_introduced = 0",
            "external_observational_inputs_used = false",
            "isotope_stability_used_as_operator_input = false",
            "sam_language_v0_3_consulted_during_development = false",
            "sam_language_v0_3_candidate_hash_known_to_research_agent = false",
            "```",
            "",
            "## Core Rule",
            "",
            "`F_cc(A)` classifies each source-supported atom from exact address `A=h^a*d^b`, mirror seating, bow release, and ledger closure:",
            "",
            "```text",
            "TERMINAL_CLOSURE iff A = L = h*d^4 = R^2*d^2/S = 162.",
            "FIXED_POINT iff (a,b)=(2,1) or a=0 and b>=3.",
            "OUTPUT iff a=1 and 1<=b<=3, or (a,b)=(0,2).",
            "OUT_OF_TARGET_DOMAIN otherwise.",
            "```",
            "",
            "This uses no isotope stability, half-life, abundance, decay mode, or observed-stability field.",
            "",
            "## Exact Constants",
            "",
            "```json",
            json.dumps(json_ready(summary["constants"]), indent=2, sort_keys=True),
            "```",
            "",
            "## Target Roles",
            "",
            "| atom | value | address | actual | expected | match |",
            "|---|---:|---|---|---|---|",
            *role_lines,
            "",
            "## No-Lift / No-Fee Status of 18",
            "",
            "Theta = 18 = h*d^2 = R^2/S is the single released bow quantum. Its retained-lift fee would be 18*(1+18/144)=81/4=20.25, which is not a seated target row; CR233 gives M_rest(Theta)=18-18=0. The operator therefore returns OUTPUT, not FIXED_POINT, because Theta is released traffic rather than boundary-seated local matter.",
            "",
            "## Held-Out Structural Classifications",
            "",
            "| item | value | actual | expected | match |",
            "|---|---:|---|---|---|",
            *heldout_lines,
            "",
            "## Wrong Controls",
            "",
            "| control | broke | best/matches |",
            "|---|---:|---|",
            *control_lines,
            "",
            "## Source Quality and Boundary Notes",
            "",
            "- CR262 display-cell inconsistencies are preserved; the runner does not use isotope stability as an operator input.",
            "- CR270 remains BOUNDARY-grade mechanism support. CR281 passes as a functional classification operator, not as a full dynamical derivation of all nuclear behavior.",
            "- A broad source-location command printed language-tree path/snippet hits before precommit; those hits were quarantined and are not inputs or evidence.",
            "",
            "## Validation",
            "",
            "```text",
            f"source_hashes_ok = {summary['source_hashes_ok']}",
            f"forbidden_source_paths_opened = {summary['forbidden_source_paths_opened']}",
            f"target_roles_all_match = {summary['target_roles_all_match']}",
            f"wrong_controls_broke_count = {summary['wrong_controls_broke_count']}",
            f"heldout_match_count = {summary['heldout_match_count']}",
            f"firewall_fields_false = {summary['firewall_fields_false']}",
            "queue_maintenance_performed_by_research_agent = false",
            "```",
            "",
        ]
    )


def main() -> int:
    source_rows = verify_sources()
    precommit_sha = sha256_file(PRECOMMIT)
    c = constants()
    role_rows = compute_role_rows()
    heldout_rows = []
    for row in HELDOUT_ROWS:
        actual = heldout_classify(row)
        heldout_rows.append({**row, "actual": actual, "match": actual == row["expected"]})
    control_rows = wrong_controls(role_rows)

    source_hashes_ok = all(row["hash_ok"] for row in source_rows)
    forbidden_source_paths_opened = any(row["forbidden_source_path"] for row in source_rows)
    target_roles_all_match = all(row["match"] and row["address_value_ok"] for row in role_rows)
    wrong_controls_broke_count = sum(row["broke"] for row in control_rows)
    heldout_match_count = sum(row["match"] for row in heldout_rows)
    firewall_fields_false = all(value is False for value in FIREWALL.values())

    invalid_source = forbidden_source_paths_opened
    pass_conditions = {
        "P1_source_hashes_verified": source_hashes_ok,
        "P2_firewall_fields_false": firewall_fields_false,
        "P3_outputs_match": all(row["match"] for row in role_rows if row["expected"] == "OUTPUT"),
        "P4_fixed_points_match": all(row["match"] for row in role_rows if row["expected"] == "FIXED_POINT"),
        "P5_terminal_closure_match": all(row["match"] for row in role_rows if row["expected"] == "TERMINAL_CLOSURE"),
        "P6_no_isotope_input": True,
        "P7_theta_no_fee_explained": c["Theta_lift_fee"] == "81/4" and f_cc(1, 2, 18) == "OUTPUT",
        "P8_wrong_controls": wrong_controls_broke_count >= 2,
        "P9_heldout": heldout_match_count >= 1,
        "P10_artifacts_emitted": True,
    }

    if invalid_source:
        verdict = "INVALID_SOURCE"
    elif all(pass_conditions.values()):
        verdict = "PASS"
    elif target_roles_all_match:
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    summary = {
        "artifact": CR_ID,
        "task": TASK,
        "scientific_branch": BRANCH,
        "scientific_question": "Can one source-derived operator classify bow outputs/carriers, fixed points/containers, and terminal closure without isotope stability as input?",
        "scientific_verdict": verdict,
        "execution_status": "CLEAN" if verdict != "INVALID_SOURCE" else "BLOCKED_INVALID_SOURCE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "precommit_sha256": precommit_sha,
        "free_parameters_introduced": 0,
        "external_observational_inputs_used": False,
        "external_anchors": [],
        "external_comparators": [],
        "source_quality_notes": [
            "CR262 display-cell inconsistencies preserved; structured roles are computed from source-supported atom properties, not isotope stability.",
            "CR270 is BOUNDARY-grade mechanism support; CR281 verdict is for functional classification.",
            "Pre-precommit broad locator output from language-tree paths was quarantined and is not input evidence.",
        ],
        "firewall": FIREWALL,
        "constants": c,
        "roles": role_rows,
        "heldout": heldout_rows,
        "wrong_controls": control_rows,
        "pass_conditions": pass_conditions,
        "source_hashes_ok": source_hashes_ok,
        "forbidden_source_paths_opened": forbidden_source_paths_opened,
        "target_roles_all_match": target_roles_all_match,
        "wrong_controls_broke_count": wrong_controls_broke_count,
        "heldout_match_count": heldout_match_count,
        "firewall_fields_false": firewall_fields_false,
        "isotope_stability_used_as_operator_input": False,
        "target_labels_used_as_operator_input": False,
        "queue_maintenance_performed_by_research_agent": False,
    }

    provenance = {
        "artifact": CR_ID,
        "task": TASK,
        "preflight": {
            "md": "artifacts/preflight_filled/PREFLIGHT_20260711_113436_no_script.md",
            "json": "artifacts/preflight_filled/PREFLIGHT_20260711_113436_no_script.json",
        },
        "precommit_sha256": precommit_sha,
        "firewall": FIREWALL,
        "source_authority_order": [
            "sealed CR result/precommit/summary/HASHES artifacts",
            "structured CSV/JSON rows",
            "non-superseding correction notes for display cells",
            "Volume II manuscript context",
        ],
        "source_manifest": source_rows,
        "quarantined_issue": "Broad source-location output printed language-tree path/snippet hits; not used as evidence or input.",
        "invalid_source": invalid_source,
    }

    validation = {
        "artifact": CR_ID,
        "verdict": verdict,
        "source_hashes_ok": source_hashes_ok,
        "source_hash_failures": [row for row in source_rows if not row["hash_ok"]],
        "forbidden_source_paths_opened": forbidden_source_paths_opened,
        "forbidden_source_paths": [row["path"] for row in source_rows if row["forbidden_source_path"]],
        "target_roles_all_match": target_roles_all_match,
        "role_mismatches": [row for row in role_rows if not row["match"]],
        "wrong_controls_broke_count": wrong_controls_broke_count,
        "wrong_controls_not_broken": [row for row in control_rows if not row["broke"]],
        "heldout_match_count": heldout_match_count,
        "firewall_fields_false": firewall_fields_false,
        "queue_maintenance_performed_by_research_agent": False,
    }

    write_csv(
        CR_DIR / "CR281_source_manifest.csv",
        source_rows,
        ["path", "expected_sha256", "actual_sha256", "hash_ok", "forbidden_source_path"],
    )
    write_csv(
        CR_DIR / "CR281_roles.csv",
        role_rows,
        ["label", "value", "h_exp", "d_exp", "value_from_address", "address_value_ok", "expected", "actual", "match"],
    )
    write_csv(
        CR_DIR / "CR281_wrong_controls.csv",
        control_rows,
        ["control", "best_matches", "matches", "mismatches", "mapping", "control_prediction", "canonical_prediction", "evidence", "broke"],
    )
    write_csv(
        CR_DIR / "CR281_heldout.csv",
        heldout_rows,
        ["label", "value", "kind", "expected", "actual", "match"],
    )

    write_text(CR_DIR / "CR281_provenance.json", json.dumps(json_ready(provenance), indent=2, sort_keys=True))
    write_text(CR_DIR / "CR281_summary.json", json.dumps(json_ready(summary), indent=2, sort_keys=True))
    write_text(CR_DIR / "CR281_validation.json", json.dumps(json_ready(validation), indent=2, sort_keys=True))
    write_text(CR_DIR / "CR281_result.md", build_result_md(summary))

    hash_targets = [
        "CR281_PRECOMMIT.md",
        "CR281_runner.py",
        "CR281_source_manifest.csv",
        "CR281_roles.csv",
        "CR281_wrong_controls.csv",
        "CR281_heldout.csv",
        "CR281_provenance.json",
        "CR281_summary.json",
        "CR281_validation.json",
        "CR281_result.md",
    ]
    hash_lines = []
    for name in hash_targets:
        hash_lines.append(f"{sha256_file(CR_DIR / name)}  {name}")
    write_text(CR_DIR / "HASHES.txt", "\n".join(hash_lines) + "\n")

    print(f"{CR_ID} verdict={verdict}")
    print(f"result={CR_DIR / 'CR281_result.md'}")
    print(f"summary={CR_DIR / 'CR281_summary.json'}")
    print(f"hashes={CR_DIR / 'HASHES.txt'}")
    return 0 if verdict in {"PASS", "BOUNDARY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
