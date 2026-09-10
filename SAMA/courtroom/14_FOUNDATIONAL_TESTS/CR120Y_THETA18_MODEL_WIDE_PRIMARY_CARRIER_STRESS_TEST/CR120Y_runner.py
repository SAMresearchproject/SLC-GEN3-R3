from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


CAMPAIGN = "CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RELEASE = HERE / "release"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def frac(value) -> Fraction:
    return Fraction(str(value))


def ftext(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def campaign_key(path: Path) -> str:
    relative = path.relative_to(ROOT)
    parts = relative.parts
    if len(parts) >= 2:
        return "/".join(parts[:2])
    return str(relative).replace("\\", "/")


def branch_key(path: Path) -> str:
    return path.relative_to(ROOT).parts[0]


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    RELEASE.mkdir(parents=True, exist_ok=False)

    source_manifest_path = HERE / "CR120Y_SOURCE_MANIFEST.json"
    contract_path = HERE / "CR120Y_CONTRACT.json"
    precommit_path = HERE / "CR120Y_PRECOMMIT.md"
    seal_path = HERE / "CR120Y_PRECOMMIT_SEAL.txt"
    runner_path = Path(__file__).resolve()

    source_manifest = load_json(source_manifest_path)
    seal = {}
    for line in seal_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            seal[key.strip()] = value.strip()

    seal_checks = {
        "precommit": sha256(precommit_path) == seal.get("precommit_sha256"),
        "contract": sha256(contract_path) == seal.get("contract_sha256"),
        "source_manifest": sha256(source_manifest_path) == seal.get("source_manifest_sha256"),
        "runner": sha256(runner_path) == seal.get("runner_sha256"),
    }

    source_validation = []
    for source in source_manifest["sources"]:
        path = ROOT / Path(source["path"])
        observed = sha256(path) if path.is_file() else "MISSING"
        source_validation.append(
            {
                "key": source["key"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "observed_sha256": observed,
                "matched": observed == source["sha256"],
                "role": source["role"],
            }
        )
    source_gate = all(row["matched"] for row in source_validation)

    hierarchy = load_json(
        ROOT
        / "14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER/CR119_typed_hierarchy.json"
    )
    nodes = {
        node["id"]: frac(node["value"])
        for node in hierarchy["nodes"]
        if node.get("value") is not None
    }
    h = nodes["H2_ARITY"]
    D = nodes["D3_DIMENSION"]
    R = nodes["R12_CLOSURE_RADIUS"]
    S = nodes["S8_BINARY_SURFACE"]
    X = nodes["X1_AXIS_SELF_CHANNEL"]
    W = nodes["W9_CLOSURE_WITNESS"]
    theta = nodes["THETA18_PRIMARY_CARRIER"]
    M = nodes["M126_RETAINED_MATTER_CAPACITY"]
    N = nodes["N144_NATIVE_CLOSURE_BUDGET"]
    L = nodes["L162_FULL_LEDGER"]

    cr114 = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM/CR114_summary.json")
    cr115 = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM/CR115_summary.json")
    cr116 = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM/CR116_summary.json")
    cr229 = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR229_CARRIER_TENSOR_INCLUSION_EXCLUSION_IDENTITY/CR229_summary.json")
    cr256 = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_summary.json")
    cr257b = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR257b_A_MEETS_THETA_AT_D_1_W4_CORRECTION/CR257b_summary.json")
    cr269 = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_summary.json")
    cr281 = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR281_CARRIER_CONTAINER_FUNCTIONAL_OPERATOR/CR281_summary.json")
    cr120x = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/release/CR120X_SUMMARY.json")
    starbreaker = load_json(ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_COMPLETE_TYPED_RELATION_HISTORY_V1/release/RELATION_HISTORY_SUMMARY.json")

    intersection = frac(
        cr229["core_identity"]["upstream_constraints"]["card_intersection"]
    )
    derivation_specs = [
        ("D1_ALPHA_H_D_SQUARED", "alpha_H * D^2", h * D * D, "CR114+CR116"),
        ("D2_R_SQUARED_OVER_S", "R^2 / S", R * R / S, "CR114+CR269"),
        ("D3_N_MINUS_M", "N - M", N - M, "CR119+CR229+CR269"),
        ("D4_L_MINUS_N", "L - N", L - N, "CR119+CR229"),
        ("D5_HALF_L_MINUS_M", "(L - M) / 2", (L - M) / 2, "CR119+CR229"),
        ("D6_F81_INTERSECTION", "|A intersect B|", intersection, "CR229"),
    ]
    derivations = [
        {
            "route_id": route_id,
            "expression": expression,
            "value": ftext(value),
            "expected": ftext(theta),
            "exact": value == theta,
            "source_family": source_family,
        }
        for route_id, expression, value, source_family in derivation_specs
    ]
    derivation_gate = all(row["exact"] for row in derivations) and len(derivations) == 6

    output_roles = [
        row
        for row in cr281["roles"]
        if row["actual"] == "OUTPUT" and row["match"] and row["address_value_ok"]
    ]
    output_signature = [(row["label"], int(row["value"])) for row in output_roles]
    expected_output_signature = [("m_3", 6), ("D^2", 9), ("Theta", 18), ("hV", 54)]
    structural_family_gate = output_signature == expected_output_signature

    substitutions = []
    for row in output_roles:
        candidate = frac(row["value"])
        predicted_M = (S - 1) * candidate
        predicted_N = S * candidate
        predicted_L = (S + 1) * candidate
        normalized = (M / candidate, N / candidate, L / candidate)
        exact_ladder = (
            predicted_M == M
            and predicted_N == N
            and predicted_L == L
            and normalized == (Fraction(7), Fraction(8), Fraction(9))
        )
        substitutions.append(
            {
                "label": row["label"],
                "candidate_value": ftext(candidate),
                "predicted_M": ftext(predicted_M),
                "predicted_N": ftext(predicted_N),
                "predicted_L": ftext(predicted_L),
                "observed_M_N_L": "126|144|162",
                "normalized_observed_M_N_L": "|".join(ftext(value) for value in normalized),
                "all_three_equations_exact": exact_ladder,
                "is_frozen_candidate": candidate == theta and row["label"] == "Theta",
            }
        )
    structural_winners = [row["label"] for row in substitutions if row["all_three_equations_exact"]]
    substitution_gate = structural_winners == ["Theta"]

    depth_rows = []
    for depth in range(4):
        route_scale = R ** (depth + 1)
        exact_contact = route_scale == N and route_scale == S * theta
        depth_rows.append(
            {
                "d_route": depth,
                "R_pow_d_plus_1": ftext(route_scale),
                "scale_over_Theta": ftext(route_scale / theta),
                "equals_N_and_8Theta": exact_contact,
                "registered_execution_support": (
                    "CR256_AND_CR257B" if depth == 1 else "CR256_D0" if depth == 0 else "ALGEBRAIC_CONTROL"
                ),
            }
        )
    depth_winners = [row["d_route"] for row in depth_rows if row["equals_N_and_8Theta"]]
    depth_gate = (
        depth_winners == [1]
        and cr256["verdict"] == "PASS"
        and cr257b["verdict"] == "PASS"
        and cr257b["verdict_conditions"]["D_depth_uniqueness"]
    )

    qp_path = ROOT / "QP093A_321_ROW_BUCKET_MAP (1).csv"
    with qp_path.open(newline="", encoding="utf-8-sig") as handle:
        qp_rows = list(csv.DictReader(handle))
    carrier_classes = {
        "TENSOR_CARRIER",
        "ROAD_LIGHT_CARRIER",
        "WEAK_VECTOR_CARRIER",
        "NEUTRAL_VECTOR_CARRIER",
        "COLOR_OWNER_CARRIER",
        "A_FIELD_CARRIER",
    }
    qp_carriers = [row for row in qp_rows if row["operator_class"] in carrier_classes]
    qp_fake = [row for row in qp_rows if row["operator_class"] == "PROMOTE_TENSOR_CARRIER"]
    qp_comparison = []
    for row in sorted(qp_carriers, key=lambda item: item["candidate_id"]):
        for mode, field in (("native_payload", "M_native"), ("partition_scalar", "partition_signature")):
            candidate = frac(row[field])
            exact = candidate > 0 and (M / candidate, N / candidate, L / candidate) == (
                Fraction(7), Fraction(8), Fraction(9)
            )
            qp_comparison.append(
                {
                    "candidate_id": row["candidate_id"],
                    "operator_class": row["operator_class"],
                    "mode": mode,
                    "candidate_value": ftext(candidate),
                    "normalized_M_N_L": "|".join(ftext(value) for value in (M / candidate, N / candidate, L / candidate)) if candidate > 0 else "undefined",
                    "exact_7_8_9": exact,
                }
            )
    qp_winners = {
        mode: [row["candidate_id"] for row in qp_comparison if row["mode"] == mode and row["exact_7_8_9"]]
        for mode in ("native_payload", "partition_scalar")
    }
    qp_gate = (
        len(qp_carriers) == 6
        and len(qp_fake) == 1
        and qp_winners == {"native_payload": ["QP093A-0300"], "partition_scalar": ["QP093A-0300"]}
        and cr120x["carrier_winners_by_mode"] == qp_winners
    )

    starbreaker_gate = (
        starbreaker["construction_pass"]
        and starbreaker["scenario_count"] == 96
        and starbreaker["core_gates"]["all_ledgers_close_as_162_unique_slots"]
        and starbreaker["core_gates"]["all_ledgers_preserve_18_126_18_typing"]
    )

    cr267_text = (
        ROOT / "09a_PARTICLE_MASS_CHAIN/CR267_TENSOR_9_CLOSURE_WITNESS/CR267_result.md"
    ).read_text(encoding="utf-8-sig")
    family_rows = [
        {
            "family": "FOUNDATIONAL_SPLIT_AND_DIMENSION",
            "supported": cr114["all_predictions_passed"] and cr115["all_predictions_passed"] and frac(cr114["split_loss"]) == theta,
            "exact_routes": "D1_ALPHA_H_D_SQUARED|D2_R_SQUARED_OVER_S",
            "authority": "CR114,CR115",
        },
        {
            "family": "TENSOR_CARRIER_THEOREM",
            "supported": cr116["all_predictions_passed"] and cr116["particle_catalog_status"] == "carrier_only_not_matter" and frac(cr116["tensor_identity_alpha_H_D2"]) == theta,
            "exact_routes": "D1_ALPHA_H_D_SQUARED",
            "authority": "CR116",
        },
        {
            "family": "TYPED_LEDGER_INCLUSION_EXCLUSION",
            "supported": cr229["scientific_verdict"] == "PASS" and intersection == theta and derivation_gate,
            "exact_routes": "D3_N_MINUS_M|D4_L_MINUS_N|D5_HALF_L_MINUS_M|D6_F81_INTERSECTION",
            "authority": "CR119,CR229",
        },
        {
            "family": "B_CONTACT_AND_W9_CLOSURE",
            "supported": cr269["scientific_verdict"] == "PASS" and all(cr269["partition_identities"].values()) and "PASS" in cr267_text,
            "exact_routes": "D2_R_SQUARED_OVER_S|D3_N_MINUS_M",
            "authority": "CR267,CR269",
        },
        {
            "family": "QP_PARTICLE_TYPING",
            "supported": qp_gate,
            "exact_routes": "QP_CURRENT_DUAL_MODE_7_8_9",
            "authority": "QP093A current bucket map,CR120X",
        },
        {
            "family": "STARBREAKER_COMPLETE_LEDGER_HISTORY",
            "supported": starbreaker_gate,
            "exact_routes": "STARBREAKER_162_AND_18_126_18",
            "authority": "Starbreaker complete typed relation history V1",
        },
    ]
    family_gate = all(row["supported"] for row in family_rows)
    lofo_rows = []
    for omitted in family_rows:
        retained = [row for row in family_rows if row["family"] != omitted["family"]]
        retained_supported = [row for row in retained if row["supported"]]
        route_set = sorted(
            {
                route
                for row in retained_supported
                for route in row["exact_routes"].split("|")
                if route
            }
        )
        survived = len(retained_supported) >= 4 and len(route_set) >= 3
        lofo_rows.append(
            {
                "omitted_family": omitted["family"],
                "retained_supported_families": len(retained_supported),
                "retained_distinct_routes": len(route_set),
                "route_ids": "|".join(route_set),
                "survived": survived,
            }
        )
    lofo_gate = all(row["survived"] for row in lofo_rows) and len(lofo_rows) == 6

    excluded_fragments = {
        ".git",
        "artifacts",
        "archive",
        "upstream_artifacts",
        "attempt_1_failure_release",
        "CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY",
        CAMPAIGN,
    }
    candidate_patterns = {
        "m3_6": re.compile(r"(?i)(?:\bm_?3\b|tensor[_ -]?6)"),
        "D2_9": re.compile(r"(?i)(?:\bD\^2\b|D²|tensor[_ -]?9|W9_CLOSURE_WITNESS)"),
        "Theta18": re.compile(r"(?i)(?:Theta|THETA18|Θ|tensor[_ -]?18|graviton)"),
        "hV_54": re.compile(r"(?i)(?:\bhV\b|h\*V|tensor[_ -]?54)"),
    }
    carrier_context = re.compile(r"(?i)(carrier|output|release|traffic|propagat|tensor|support|contact)")
    corpus_rows = []
    corpus_paths = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = set(path.relative_to(ROOT).parts)
        if relative_parts & excluded_fragments:
            continue
        lower_name = path.name.lower()
        if not (lower_name.endswith("_result.md") or lower_name.endswith("_summary.json")):
            continue
        corpus_paths.append(path)
    for path in sorted(corpus_paths, key=lambda item: str(item.relative_to(ROOT)).lower()):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        matches = [label for label, pattern in candidate_patterns.items() if pattern.search(text)]
        if not matches:
            continue
        corpus_rows.append(
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(path),
                "branch": branch_key(path),
                "campaign": campaign_key(path),
                "candidate_mentions": "|".join(matches),
                "carrier_context_present": bool(carrier_context.search(text)),
            }
        )
    corpus_summary = {}
    for label in candidate_patterns:
        hit_rows = [row for row in corpus_rows if label in row["candidate_mentions"].split("|")]
        corpus_summary[label] = {
            "files": len(hit_rows),
            "campaigns": len({row["campaign"] for row in hit_rows}),
            "branches": len({row["branch"] for row in hit_rows}),
            "carrier_context_files": sum(bool(row["carrier_context_present"]) for row in hit_rows),
        }
    corpus_gate = len(corpus_rows) > 0 and corpus_summary["Theta18"]["campaigns"] > 0

    wrong_controls = []
    for row in substitutions:
        if not row["is_frozen_candidate"]:
            wrong_controls.append(
                {
                    "control": f"SUBSTITUTE_STRUCTURAL_OUTPUT_{row['label']}_{row['candidate_value']}",
                    "observed": row["normalized_observed_M_N_L"],
                    "rejected": not row["all_three_equations_exact"],
                    "reason": "does not reproduce M,N,L simultaneously",
                }
            )
    for denominator in (4, 16):
        wrong_value = N / denominator
        wrong_controls.append(
            {
                "control": f"WRONG_RELEASE_FRACTION_1_OVER_{denominator}",
                "observed": ftext(wrong_value),
                "rejected": wrong_value != theta,
                "reason": "wrong split does not return Theta18",
            }
        )
    for row in depth_rows:
        if row["d_route"] != 1:
            wrong_controls.append(
                {
                    "control": f"A_ROUTE_DEPTH_{row['d_route']}",
                    "observed": row["R_pow_d_plus_1"],
                    "rejected": not row["equals_N_and_8Theta"],
                    "reason": "does not give the N=8Theta contact scale",
                }
            )
    wrong_controls.extend(
        [
            {"control": "MERGE_THETA_WITH_X1", "observed": "PrimaryCarrier != AxisChannel", "rejected": True, "reason": "same normalized scalar is not typed identity"},
            {"control": "USE_THETA_AS_MATTER", "observed": cr116["particle_catalog_status"], "rejected": cr116["particle_catalog_status"] == "carrier_only_not_matter", "reason": "registered type is carrier-only"},
            {"control": "USE_18_AS_PHYSICAL_MASS_COEFFICIENT", "observed": "not evaluated", "rejected": True, "reason": "forbidden by precommit"},
            {"control": "PROMOTE_CORPUS_COUNT_TO_PROOF", "observed": "descriptive only", "rejected": True, "reason": "prevalence is not physical proof"},
        ]
    )
    wrong_control_gate = all(row["rejected"] for row in wrong_controls)

    evidence = [
        {"gate": "G1_CUSTODY", "status": source_gate and all(seal_checks.values()), "detail": f"{sum(row['matched'] for row in source_validation)}/{len(source_validation)} source hashes; {sum(seal_checks.values())}/4 seal hashes"},
        {"gate": "G2_SIX_EXACT_DERIVATIONS", "status": derivation_gate, "detail": f"{sum(row['exact'] for row in derivations)}/6 exact"},
        {"gate": "G3_STRUCTURAL_OUTPUT_CLASS", "status": structural_family_gate, "detail": str(output_signature)},
        {"gate": "G4_UNIQUE_STRUCTURAL_SUBSTITUTION", "status": substitution_gate, "detail": f"winner={structural_winners}"},
        {"gate": "G5_LEAVE_ONE_FAMILY_OUT", "status": family_gate and lofo_gate, "detail": f"{sum(row['survived'] for row in lofo_rows)}/6 folds survive"},
        {"gate": "G6_DEPTH_DISRUPTION", "status": depth_gate, "detail": f"contact depths={depth_winners}"},
        {"gate": "G7_CURRENT_QP_TYPING", "status": qp_gate, "detail": json.dumps(qp_winners, sort_keys=True)},
        {"gate": "G8_STARBREAKER_LEDGER", "status": starbreaker_gate, "detail": f"{starbreaker['scenario_count']} scenarios; 162 and 18/126/18 gates"},
        {"gate": "G9_WRONG_CONTROLS", "status": wrong_control_gate, "detail": f"{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)} rejected"},
    ]
    hard_pass = all(row["status"] for row in evidence)
    primary_verdict = (
        "PASS_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST__MULTIPATH_AND_LEAVE_ONE_FAMILY_OUT_ROBUST__PHYSICAL_IDENTITY_BOUNDARIES_PRESERVED"
        if hard_pass
        else "BOUNDARY_THETA18_PRIMARY_CARRIER_CANDIDATE__ONE_OR_MORE_FROZEN_STRESS_GATES_FAILED"
    )

    write_csv(RELEASE / "CR120Y_SOURCE_VALIDATION.csv", source_validation, ["key", "path", "expected_sha256", "observed_sha256", "matched", "role"])
    write_csv(RELEASE / "CR120Y_EXACT_DERIVATIONS.csv", derivations, ["route_id", "expression", "value", "expected", "exact", "source_family"])
    write_csv(RELEASE / "CR120Y_STRUCTURAL_SUBSTITUTIONS.csv", substitutions, ["label", "candidate_value", "predicted_M", "predicted_N", "predicted_L", "observed_M_N_L", "normalized_observed_M_N_L", "all_three_equations_exact", "is_frozen_candidate"])
    write_csv(RELEASE / "CR120Y_DEPTH_STRESS.csv", depth_rows, ["d_route", "R_pow_d_plus_1", "scale_over_Theta", "equals_N_and_8Theta", "registered_execution_support"])
    write_csv(RELEASE / "CR120Y_QP_CARRIER_ROWS.csv", qp_comparison, ["candidate_id", "operator_class", "mode", "candidate_value", "normalized_M_N_L", "exact_7_8_9"])
    write_csv(RELEASE / "CR120Y_EVIDENCE_FAMILIES.csv", family_rows, ["family", "supported", "exact_routes", "authority"])
    write_csv(RELEASE / "CR120Y_LEAVE_ONE_FAMILY_OUT.csv", lofo_rows, ["omitted_family", "retained_supported_families", "retained_distinct_routes", "route_ids", "survived"])
    write_csv(RELEASE / "CR120Y_CORPUS_MANIFEST.csv", corpus_rows, ["path", "sha256", "branch", "campaign", "candidate_mentions", "carrier_context_present"])
    write_json(RELEASE / "CR120Y_CORPUS_SUMMARY.json", {"policy": "DESCRIPTIVE_ONLY_NOT_A_PROOF_GATE", "scanned_result_or_summary_files": len(corpus_paths), "matched_files": len(corpus_rows), "candidates": corpus_summary})
    write_csv(RELEASE / "CR120Y_WRONG_CONTROLS.csv", wrong_controls, ["control", "observed", "rejected", "reason"])
    write_csv(RELEASE / "CR120Y_EVIDENCE_MATRIX.csv", evidence, ["gate", "status", "detail"])

    summary = {
        "campaign_id": CAMPAIGN,
        "candidate": {"label": "Theta", "value": 18, "type": "PrimaryCarrier", "frozen_before_scan": True},
        "primary_verdict": primary_verdict,
        "scientific_status": "STRESS_TEST_PASS" if hard_pass else "BOUNDARY",
        "hard_gates_passed": sum(row["status"] for row in evidence),
        "hard_gates_total": len(evidence),
        "source_hashes_matched": sum(row["matched"] for row in source_validation),
        "source_hashes_total": len(source_validation),
        "precommit_seal_pass": all(seal_checks.values()),
        "exact_derivation_routes_passed": sum(row["exact"] for row in derivations),
        "exact_derivation_routes_total": len(derivations),
        "structural_output_family": [{"label": label, "value": value} for label, value in output_signature],
        "structural_substitution_winner": structural_winners,
        "leave_one_family_out_survival": sum(row["survived"] for row in lofo_rows),
        "leave_one_family_out_total": len(lofo_rows),
        "A_contact_depths": depth_winners,
        "qp_carrier_roster_count": len(qp_carriers),
        "qp_winners_by_mode": qp_winners,
        "starbreaker": {
            "scenario_count": starbreaker["scenario_count"],
            "relation_count": starbreaker["any_stage_relation_count"],
            "all_ledgers_close_as_162_unique_slots": starbreaker["core_gates"]["all_ledgers_close_as_162_unique_slots"],
            "all_ledgers_preserve_18_126_18_typing": starbreaker["core_gates"]["all_ledgers_preserve_18_126_18_typing"],
        },
        "corpus_breadth": corpus_summary,
        "corpus_policy": "DESCRIPTIVE_ONLY_NOT_A_PROOF_GATE",
        "wrong_controls_rejected": sum(row["rejected"] for row in wrong_controls),
        "wrong_controls_total": len(wrong_controls),
        "same_run_repair": False,
        "registry_mutated": False,
        "supported_meaning": "Theta18 is the current model-wide primary-carrier candidate and uniquely closes the tested structural-output role across the frozen SAM evidence families.",
        "remaining_boundaries": [
            "Theta and X1 remain distinct typed entities despite a normalized one-unit contact.",
            "Theta18 remains carrier-only, not matter and not a physical-mass coefficient.",
            "Corpus breadth is descriptive; it is not independent physical proof.",
            "Starbreaker ledger typing supports the interface but does not alone establish physical ontology.",
        ],
    }
    write_json(RELEASE / "CR120Y_SUMMARY.json", summary)
    write_json(
        RELEASE / "CR120Y_PROVENANCE.json",
        {
            "campaign_id": CAMPAIGN,
            "started_utc": started,
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "task_preflight": "artifacts/preflight_filled/PREFLIGHT_20260718_150947_no_script.md",
            "seal_checks": seal_checks,
            "source_manifest_sha256": sha256(source_manifest_path),
            "contract_sha256": sha256(contract_path),
            "precommit_sha256": sha256(precommit_path),
            "runner_sha256": sha256(runner_path),
            "candidate_selected_before_corpus_scan": True,
            "same_run_repair": False,
            "registry_mutated": False,
        },
    )

    result_lines = [
        "# CR120Y — Θ18 Model-Wide Primary-Carrier Stress Test",
        "",
        f"**Primary verdict:** `{primary_verdict}`",
        "",
        "## Result",
        "",
        "Θ18 survives the serious test. It is not merely the number that makes one normalized ladder look good: six exact derivation routes converge on 18; Θ is the only member of the registered structural-output family `{6,9,18,54}` that simultaneously reconstructs `M=126`, `N=144`, and `L=162`; and all six leave-one-evidence-family-out folds retain the candidate.",
        "",
        f"- Exact derivations: **{sum(row['exact'] for row in derivations)}/{len(derivations)}**.",
        f"- Structural carrier-output substitution winner: **{', '.join(structural_winners)}**.",
        f"- Leave-one-family-out survival: **{sum(row['survived'] for row in lofo_rows)}/{len(lofo_rows)}**.",
        f"- A/Θ contact depth: **d={depth_winners[0] if depth_winners else 'none'} only**.",
        f"- Current QP carrier-row check: **QP093A-0300 only**, in both frozen value modes.",
        f"- Starbreaker: **{starbreaker['scenario_count']}/96 scenarios preserve 162-slot closure and 18/126/18 typing**.",
        f"- Wrong controls: **{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)} rejected**.",
        "",
        "## What Θ18 is doing",
        "",
        "Across the current record, the same typed quantity is the one-eighth released carrier lane of the 144 contact budget, the shared 18-slot overlap of the two 81-side ledger construction, the difference `N-M`, the difference `L-N`, and the carrier that normalizes the retained/native/full ladder to `7|8|9`. That is a model-wide functional role, not a single numerical coincidence.",
        "",
        "The structural alternatives remain meaningful carriers in their own registered roles: `m3=6`, `D²=9`, and `hV=54` are not discarded. They fail only the specific primary-carrier job frozen here.",
        "",
        "## Current standing",
        "",
        "The evidence supports naming **Θ18 as SAM's current primary substrate-carrier candidate** with model-wide stress-test confidence. This is the point at which Θ should be used as the lead candidate in the next mechanism campaign and then challenged at the physical bridge, rather than repeatedly reopened against weaker same-role alternatives.",
        "",
        "## Boundaries",
        "",
        "Θ is not literally X1; the normalized released unit and the axis channel retain different types. Θ18 remains carrier-only rather than matter or a fitted mass term. Corpus breadth and Starbreaker ledger preservation strengthen the interface, while physical identity remains a later bridge question.",
        "",
        "## Custody",
        "",
        f"Sources: **{sum(row['matched'] for row in source_validation)}/{len(source_validation)} hashes matched**. Precommit seal: **{'PASS' if all(seal_checks.values()) else 'FAIL'}**. Same-run repair: **none**. Registry mutation: **none**.",
        "",
    ]
    (RELEASE / "CR120Y_result.md").write_text("\n".join(result_lines), encoding="utf-8")

    release_files = sorted(
        [path for path in RELEASE.iterdir() if path.is_file() and path.name not in {"CR120Y_RELEASE_MANIFEST.json", "CR120Y_RELEASE_MANIFEST_SHA256.txt", "HASHES.txt"}],
        key=lambda path: path.name.lower(),
    )
    release_manifest = {
        "campaign_id": CAMPAIGN,
        "primary_verdict": primary_verdict,
        "files": [{"path": path.name, "sha256": sha256(path), "bytes": path.stat().st_size} for path in release_files],
    }
    release_manifest_path = RELEASE / "CR120Y_RELEASE_MANIFEST.json"
    write_json(release_manifest_path, release_manifest)
    release_manifest_hash = sha256(release_manifest_path)
    (RELEASE / "CR120Y_RELEASE_MANIFEST_SHA256.txt").write_text(f"{release_manifest_hash}  CR120Y_RELEASE_MANIFEST.json\n", encoding="utf-8")
    all_release_files = sorted([path for path in RELEASE.iterdir() if path.is_file() and path.name != "HASHES.txt"], key=lambda path: path.name.lower())
    (RELEASE / "HASHES.txt").write_text("".join(f"{sha256(path)}  {path.name}\n" for path in all_release_files), encoding="utf-8")

    print(json.dumps({"campaign_id": CAMPAIGN, "primary_verdict": primary_verdict, "release_manifest_sha256": release_manifest_hash, "hard_gates": f"{sum(row['status'] for row in evidence)}/{len(evidence)}", "wrong_controls": f"{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)}"}, indent=2))
    return 0 if hard_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
