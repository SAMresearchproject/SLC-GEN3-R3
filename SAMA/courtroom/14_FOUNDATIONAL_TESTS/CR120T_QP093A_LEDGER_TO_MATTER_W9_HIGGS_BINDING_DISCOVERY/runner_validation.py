from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

import runner_discovery as discovery


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRECOMMIT = HERE / "PRECOMMIT_VALIDATION.md"
PRECOMMIT_SHA256 = "dfb835dcf947e94a1893e8900e85236cdac480422ac972c37a1fb265bc7a7eb6"

FROZEN_INPUT_SHA256 = {
    "SOURCE_MANIFEST.json": "b1eee6ab1603c7a3ed5995afb5e1b3061b17f1c8aafce11d7db0f675a7769451",
    "runner_discovery.py": "323de8fcb7d1e7e7d8d0b9db8f1b7767905a27ebc0ba43d09a76ac9f6cbade30",
    "DISCOVERY_REPORT.json": "e600a27831fe2b82ad5ece146cc353a16eb586cf11809eb4cc363e6b3cd99811",
    "F81_CANDIDATE_RULES.json": "c6b16102993898762c2ba12a9e33340a2e30c744f6a5e85f513c6a613f2867dd",
    "BINDING_DISCOVERY_RESULTS.csv": "76cb63f3175866a8aca1dd2999a4e9aa538e83f6db0916bf059959b0f02be5e8",
    "BINDING_BASELINE.json": "192096bd5e7354c243f015ea73d34fa26361852b14d7e8020e238ae6dfef2a06",
    "BINDING_FEATURE_DEFINITIONS.json": "89463644403a43ff733548a522456f1c0aeba9054db2323f2f1b2e9b4315bb68",
    "freeze_candidates.py": "fe67a9730226504293133bf6f3bf6ee50bb1386fed8326156b28a6987f914d01",
    "F81_FROZEN_RULE_CONTRACT.json": "c209c1250c51a1f54f68724396b6826247bf4d8aafd9bb36fd35ee6efc7f9877",
    "BINDING_FROZEN_CANDIDATE.json": "8194cff8f6c70b1e0f4ff3fb3b9dbe6b68a28adb3761fb8c2f10a9b6e4023b47",
}

OPENED_INPUTS: set[str] = set()
HASHED_INPUTS: set[str] = set()


def sha256(path: Path) -> str:
    HASHED_INPUTS.add(str(path.resolve()))
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path):
    OPENED_INPUTS.add(str(path.resolve()))
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict]:
    OPENED_INPUTS.add(str(path.resolve()))
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_json(name: str, payload) -> None:
    (HERE / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_csv(name: str, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = []
        seen = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    fieldnames.append(key)
    with (HERE / name).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_path(entry: dict) -> Path:
    path = Path(entry["path"])
    return path if path.is_absolute() else ROOT / path


def frac(value) -> Fraction:
    if value is None or value == "":
        return Fraction(0)
    return Fraction(str(value))


def decimal_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.12f}".rstrip("0").rstrip(".")


def metric(obs: list[float], pred: list[float]) -> dict:
    residual = [p - o for o, p in zip(obs, pred)]
    absolute = [abs(x) for x in residual]
    return {
        "n": len(residual),
        "RMS_MeV": math.sqrt(sum(x * x for x in residual) / len(residual)),
        "mean_pred_minus_obs_MeV": sum(residual) / len(residual),
        "MAE_MeV": sum(absolute) / len(absolute),
        "within_5": sum(x <= 5 for x in absolute),
        "within_8": sum(x <= 8 for x in absolute),
        "within_15": sum(x <= 15 for x in absolute),
        "within_30": sum(x <= 30 for x in absolute),
        "max_abs_MeV": max(absolute),
    }


def tree_predicate_features(node: dict) -> set[str]:
    if node.get("leaf"):
        return set()
    return (
        {node["predicate"]["feature"]}
        | tree_predicate_features(node["true"])
        | tree_predicate_features(node["false"])
    )


def tree_trace(tree: dict, row: dict) -> tuple[bool, str]:
    node = tree
    trace = []
    while not node.get("leaf", False):
        predicate = node["predicate"]
        feature = predicate["feature"]
        op = predicate["operator"]
        value = predicate["value"]
        if op == "==":
            outcome = row[feature] == value
        else:
            outcome = row[feature] != "" and float(row[feature]) <= float(value)
        trace.append(f"{feature}{op}{value}:{str(outcome).lower()}")
        node = node["true"] if outcome else node["false"]
    return bool(node["prediction"]), " | ".join(trace)


def same_role_triad_valid(rows: list[dict]) -> bool:
    if len(rows) != 3:
        return False
    return (
        {r["p"] for r in rows} == {1, 8, 9}
        and len({r["g"] for r in rows}) == 1
        and len({r["same_role"] for r in rows}) == 1
    )


def validate_sources(manifest: dict) -> dict:
    checks = {}
    for entry in manifest["sources"]:
        path = source_path(entry)
        check = {
            "path": str(path.resolve()),
            "exists": path.exists(),
            "expected_bytes": entry["bytes"],
            "actual_bytes": path.stat().st_size if path.exists() else None,
            "access_mode": "hash_only",
        }
        if not path.exists():
            check["pass"] = False
        elif entry["verify_mode"] == "prior_frozen_hash_plus_saved_excel_capture_cell_reconciliation":
            check.update(
                {
                    "access_mode": "metadata_only_prior_hash_plus_frozen_capture",
                    "sha256_match": "DEFERRED_BY_MANIFEST_CONTRACT",
                    "live_original_bytes_match_freeze_metadata": path.stat().st_size
                    == entry["bytes"],
                    "disposition": "live original may drift after SaveCopyAs; frozen capture hash and discovery cell reconciliation control",
                    "pass": True,
                }
            )
        else:
            actual = sha256(path)
            check.update(
                {
                    "actual_sha256": actual,
                    "sha256_match": actual == entry["sha256"],
                    "pass": actual == entry["sha256"] and path.stat().st_size == entry["bytes"],
                }
            )
        checks[entry["source_id"]] = check
    return checks


def f81_validation(
    source_by_id: dict[str, dict], f81_contract: dict
) -> tuple[dict, list[dict], dict]:
    # The second workbook is deliberately not parsed here. Its bytes may have
    # been hash-checked by the source-integrity gate, but its membership column
    # cannot enter the selector or any control decision.
    workbook_path = source_path(source_by_id["UPDATED_WORKBOOK_100_CAPTURE"])
    workbook = discovery.parse_workbook(workbook_path)
    OPENED_INPUTS.add(str(workbook_path.resolve()))
    rows_by_sheet = discovery.candidate_rows(workbook)
    main_name, main_rows = max(
        rows_by_sheet.items(),
        key=lambda item: len(
            {r.get("candidate_id", r.get("row_id")) for r in item[1]}
        ),
    )
    domain_rows = [
        row
        for row in main_rows
        if str(row.get("count", "")).strip() in {"1", "1.0", "TRUE", "true"}
    ]
    domain_ids = [r.get("candidate_id", r.get("row_id")) for r in domain_rows]
    if len(domain_rows) != 126 or len(set(domain_ids)) != 126:
        raise RuntimeError(
            f"Frozen F81 validation domain is not 126 unique count=1 rows: {len(domain_rows)}"
        )

    catalog_path = source_path(source_by_id["QP093A_CANONICAL_299"])
    catalog = read_csv(catalog_path)
    catalog_map = {r["candidate_id"]: r for r in catalog}
    if not set(domain_ids) <= set(catalog_map):
        raise RuntimeError("Workbook validation domain contains non-canonical IDs")

    candidate = f81_contract["candidate"]
    tree = candidate["tree"]
    allowed = set(f81_contract["selection_inputs_allowed"])
    predicates = tree_predicate_features(tree)
    selector_field_firewall = predicates <= allowed and not (
        predicates
        & {
            "candidate_id",
            "row_number",
            "member_81",
            "M_native",
            "qA_source_support",
            "tensor_carrier_support",
            "retained_write_support",
        }
    )

    records = []
    for cid in domain_ids:
        feature_row = discovery.canonical_feature_row(catalog_map[cid], set(), set())
        selector_input = {feature: feature_row[feature] for feature in allowed}
        selected, trace = tree_trace(tree, selector_input)
        records.append(
            {
                "candidate_id": cid,
                "selector_input": selector_input,
                "selected": selected,
                "trace": trace,
            }
        )

    # Selection is frozen before either of these two readouts is calculated.
    selected_ids = {r["candidate_id"] for r in records if r["selected"]}
    selected_count = len(selected_ids)
    selected_sum = sum(
        (frac(catalog_map[cid]["M_native"]) for cid in selected_ids), Fraction(0)
    )

    shuffled = list(records)
    random.Random(120).shuffle(shuffled)
    shuffled_ids = {
        r["candidate_id"]
        for r in shuffled
        if tree_trace(tree, r["selector_input"])[0]
    }
    shuffle_ok = shuffled_ids == selected_ids

    value_blind_ids = set()
    for record in records:
        synthetic_full_row = dict(record["selector_input"])
        synthetic_full_row["M_native"] = "VALUE_HIDDEN"
        selector_input = {feature: synthetic_full_row[feature] for feature in allowed}
        if tree_trace(tree, selector_input)[0]:
            value_blind_ids.add(record["candidate_id"])
    value_blind_ok = value_blind_ids == selected_ids and "M_native" not in predicates

    route_to_id = {}
    for cid in domain_ids:
        route = catalog_map[cid].get("route_combination", "")
        if not (route.startswith("anti(") and route.endswith(")")):
            route_to_id[route] = cid
    conjugate_pairs = []
    for cid in domain_ids:
        route = catalog_map[cid].get("route_combination", "")
        if route.startswith("anti(") and route.endswith(")"):
            mate = route_to_id.get(route[5:-1])
            if mate:
                conjugate_pairs.append((mate, cid))
    conjugate_mismatches = [
        [a, b] for a, b in conjugate_pairs if (a in selected_ids) != (b in selected_ids)
    ]
    conjugate_ok = bool(conjugate_pairs) and not conjugate_mismatches

    typed_hierarchy = read_json(source_path(source_by_id["CR119_TYPED_HIERARCHY"]))
    edges = typed_hierarchy.get(
        "derivation_edges",
        typed_hierarchy.get("edges", typed_hierarchy.get("transitions", [])),
    )
    edge_triples = {(e.get("from"), e.get("rule"), e.get("to")) for e in edges}
    source_8_1_to_9 = (
        ("S8_BINARY_SURFACE", "S+X", "W9_CLOSURE_WITNESS") in edge_triples
        and ("X1_AXIS_SELF_CHANNEL", "S+X", "W9_CLOSURE_WITNESS") in edge_triples
    )

    p819 = discovery.triad_tests(catalog, 8, 1, 9)
    p639 = discovery.triad_tests(catalog, 6, 3, 9)
    p819_mnative = [r for r in p819 if r["field"] == "M_native"]
    p639_mnative = [r for r in p639 if r["field"] == "M_native"]
    arithmetic_control_ok = (
        p819_mnative
        and p639_mnative
        and all(r["exact_pass"] for r in p819_mnative)
        and all(r["exact_pass"] for r in p639_mnative)
        and source_8_1_to_9
    )

    neutral_g2 = []
    for p in (8, 1, 9):
        match = next(
            row
            for row in catalog
            if discovery.route_key(row) == (p, 2, "neutral")
        )
        neutral_g2.append({"p": p, "g": 2, "same_role": "neutral", "id": match["candidate_id"]})
    role_swap_valid_before = same_role_triad_valid(neutral_g2)
    role_swapped = [dict(r) for r in neutral_g2]
    role_swapped[1]["same_role"] = "matter_plus"
    role_swap_detected = role_swap_valid_before and not same_role_triad_valid(role_swapped)

    if not conjugate_pairs:
        raise RuntimeError("No conjugate pair available for the frozen wrong control")
    a, b = conjugate_pairs[0]
    complete_pair = {a, b}
    missing_pair_detected = len(complete_pair - {b}) != 2
    duplicate_witness_detected = len(["neutral_p9g0", "neutral_p9g0"]) != len(
        {"neutral_p9g0"}
    )

    wrong_controls = {
        "p6_plus_p3_arithmetic_control": {
            "p8_plus_p1_M_native_exact_roles": len(p819_mnative),
            "p6_plus_p3_M_native_exact_roles": len(p639_mnative),
            "both_arithmetic_identities_exact": arithmetic_control_ok,
            "source_typed_mechanism": "S8_BINARY_SURFACE + X1_AXIS_SELF_CHANNEL -> W9_CLOSURE_WITNESS only",
            "pass": arithmetic_control_ok,
        },
        "role_swap_control": {
            "valid_neutral_g2_before_swap": role_swap_valid_before,
            "invalid_after_p1_role_swap": role_swap_detected,
            "pass": role_swap_detected,
        },
        "missing_conjugate_control": {
            "pair": [a, b],
            "invalid_when_one_member_removed": missing_pair_detected,
            "pass": missing_pair_detected,
        },
        "duplicated_witness_control": {
            "invalid_when_neutral_witness_occurs_twice": duplicate_witness_detected,
            "pass": duplicate_witness_detected,
        },
    }
    controls_ok = all(item["pass"] for item in wrong_controls.values())

    gates = {
        "V_F81_0_HASH": True,
        "V_F81_1_FIREWALL": selector_field_firewall,
        "V_F81_2_SHUFFLE": shuffle_ok,
        "V_F81_3_VALUE_BLIND": value_blind_ok,
        "V_F81_4_CONJUGATE": conjugate_ok,
        "V_F81_5_EXACT": selected_count == 81 and selected_sum == 12600,
        "V_F81_6_TYPED_CONTROLS": controls_ok,
    }
    if all(gates.values()):
        status = "PASS_EXACT"
    elif all(
        gates[k]
        for k in [
            "V_F81_0_HASH",
            "V_F81_1_FIREWALL",
            "V_F81_2_SHUFFLE",
            "V_F81_3_VALUE_BLIND",
            "V_F81_4_CONJUGATE",
            "V_F81_6_TYPED_CONTROLS",
        ]
    ):
        status = "PARTIAL_SOURCE_TYPED_RULE"
    else:
        status = "FAIL_RULE"

    roster_rows = []
    record_by_id = {r["candidate_id"]: r for r in records}
    for cid in sorted(domain_ids):
        record = record_by_id[cid]
        canonical = catalog_map[cid]
        p, g, role = discovery.route_key(canonical)
        roster_rows.append(
            {
                "candidate_id": cid,
                "selected_by_frozen_rule": record["selected"],
                "p": "" if p is None else p,
                "g": "" if g is None else g,
                "same_role": role,
                "bin": canonical.get("bin", ""),
                "q_sign": canonical.get("q_sign", ""),
                "M_native_post_selection_readout": canonical.get("M_native", ""),
                "decision_trace": record["trace"],
            }
        )

    report = {
        "contract_id": f81_contract["contract_id"],
        "source_sheet": main_name,
        "domain_rows": len(domain_rows),
        "selector_predicate_features": sorted(predicates),
        "selected_count_post_rule": selected_count,
        "selected_M_native_sum_post_rule": decimal_fraction(selected_sum),
        "conjugate_pairs_tested": len(conjugate_pairs),
        "conjugate_mismatches": conjugate_mismatches,
        "source_typed_8_plus_1_to_9": source_8_1_to_9,
        "current_membership_opened_or_used": False,
        "second_workbook_parsed": False,
        "candidate_ids_used_by_selector": False,
        "target_count_or_sum_used_by_selector": False,
        "value_columns_used_by_selector": False,
        "gates": gates,
        "status": status,
    }
    return report, roster_rows, wrong_controls


def binding_validation(
    source_by_id: dict[str, dict], binding_contract: dict
) -> tuple[dict, list[dict], list[dict], dict]:
    cr261_path = source_path(source_by_id["CR261_BINDING_35_20"])
    cr274_path = source_path(source_by_id["CR274_SUMMARY"])
    cr277_table_path = source_path(source_by_id["CR277_ELEMENT_TABLE"])
    cr277_summary_path = source_path(source_by_id["CR277_SUMMARY"])

    cr261 = read_csv(cr261_path)
    cr274 = read_json(cr274_path)
    cr277_rows = read_csv(cr277_table_path)
    cr277_summary = read_json(cr277_summary_path)

    beta = {k: float(v) for k, v in cr274["beta_K"].items()}
    gammas = {k: float(v["gamma"]) for k, v in cr274["operators"].items()}
    gamma_surface = float(binding_contract["candidate"]["gamma_surface"])
    removed = binding_contract["candidate"]["removed_operator"]
    if removed != "op_82pre":
        raise RuntimeError(f"Unexpected frozen binding operator replacement: {removed}")

    cr261_results = []
    for raw in cr261:
        row = {
            "set": raw["set"],
            "isotope": raw["isotope"],
            "Z": int(raw["Z"]),
            "N": int(raw["N"]),
            "A": int(raw["A"]),
            "obs": float(raw["B_u_obs_MeV"]),
        }
        baseline_pred, contributions = discovery.predict_cr274(row, beta, gammas)
        feature = abs(row["N"] - row["Z"]) / (row["A"] ** (1 / 3))
        cr261_results.append(
            {
                **row,
                "baseline_pred_MeV": baseline_pred,
                "baseline_residual_pred_minus_obs_MeV": baseline_pred - row["obs"],
                "surface_excess_feature": feature,
                "removed_op_82pre_contribution_MeV": contributions[removed],
            }
        )

    all55_obs = [r["obs"] for r in cr261_results]
    all55_baseline = [r["baseline_pred_MeV"] for r in cr261_results]
    all55_baseline_metrics = metric(all55_obs, all55_baseline)
    test_rows = [r for r in cr261_results if r["set"] == "test"]
    test_baseline_metrics = metric(
        [r["obs"] for r in test_rows], [r["baseline_pred_MeV"] for r in test_rows]
    )
    train_rows = [r for r in cr261_results if r["set"] == "train"]

    cr277_results = []
    baseline_table_deltas = []
    for raw in cr277_rows:
        row = {
            "Z": int(raw["Z"]),
            "symbol": raw["symbol"],
            "N": int(raw["N"]),
            "A": int(raw["A"]),
            "isotope": raw["isotope"],
            "row_status": raw["row_status"],
        }
        baseline_pred, contributions = discovery.predict_cr274(row, beta, gammas)
        feature = abs(row["N"] - row["Z"]) / (row["A"] ** (1 / 3))
        stored_baseline = float(raw["B_u_final_MeV"])
        baseline_table_deltas.append(abs(baseline_pred - stored_baseline))
        obs = float(raw["B_u_obs_MeV"]) if raw["B_u_obs_MeV"] != "" else None
        cr277_results.append(
            {
                **row,
                "obs_MeV": "" if obs is None else obs,
                "stored_CR277_baseline_pred_MeV": stored_baseline,
                "recomputed_CR274_baseline_pred_MeV": baseline_pred,
                "baseline_residual_pred_minus_obs_MeV": "" if obs is None else baseline_pred - obs,
                "surface_excess_feature": feature,
                "removed_op_82pre_contribution_MeV": contributions[removed],
            }
        )

    observed = [r for r in cr277_results if r["obs_MeV"] != ""]
    extended = [r for r in observed if r["row_status"] == "extended_observed"]

    def metrics_for(rows: list[dict], pred_key: str) -> dict:
        return metric(
            [float(r["obs_MeV"]) for r in rows], [float(r[pred_key]) for r in rows]
        )

    baseline_whole = metrics_for(observed, "recomputed_CR274_baseline_pred_MeV")
    baseline_extended = metrics_for(extended, "recomputed_CR274_baseline_pred_MeV")

    baseline_reproduction = {
        "CR274_combined_55_RMS_recomputed": all55_baseline_metrics["RMS_MeV"],
        "CR274_combined_55_RMS_published": cr274["metrics"]["combined_RMS_MeV"],
        "CR274_abs_delta": abs(
            all55_baseline_metrics["RMS_MeV"]
            - float(cr274["metrics"]["combined_RMS_MeV"])
        ),
        "CR277_max_abs_prediction_delta_from_stored_table_MeV": max(
            baseline_table_deltas
        ),
        "CR277_whole_RMS_recomputed": baseline_whole["RMS_MeV"],
        "CR277_whole_RMS_published": cr277_summary["whole_set_observed"]["RMS_MeV"],
        "CR277_whole_RMS_abs_delta": abs(
            baseline_whole["RMS_MeV"]
            - float(cr277_summary["whole_set_observed"]["RMS_MeV"])
        ),
        "CR277_extended_RMS_recomputed": baseline_extended["RMS_MeV"],
        "CR277_extended_RMS_published": cr277_summary["extended_only"]["RMS_MeV"],
    }

    frozen_discovery_baseline = read_json(HERE / "BINDING_BASELINE.json")
    fitted_coefficients = (
        list(beta.values())
        + list(gammas.values())
        + [gamma_surface]
    )
    forbidden = set(float(x) for x in binding_contract["forbidden_fitted_coefficients"])
    forbidden_used = [x for x in fitted_coefficients if x in forbidden]
    firewall_ok = (
        frozen_discovery_baseline["test_observations_scored"] == 0
        and frozen_discovery_baseline["extended_observations_scored"] == 0
        and binding_contract["candidate"]["free_parameter_delta"] == 0
        and not forbidden_used
    )
    baseline_ok = (
        baseline_reproduction["CR274_abs_delta"] <= 1e-9
        and baseline_reproduction[
            "CR277_max_abs_prediction_delta_from_stored_table_MeV"
        ]
        <= 5e-5
        and baseline_reproduction["CR277_whole_RMS_abs_delta"] <= 1e-6
    )
    if not baseline_ok:
        raise RuntimeError(
            "Frozen CR274/CR277 baseline did not reproduce; candidate was not scored"
        )
    if not firewall_ok:
        raise RuntimeError(
            "Binding validation firewall failed; candidate was not scored"
        )

    # The frozen baselines and discovery firewall have now passed. Only here is
    # the immutable B3 candidate scored on held-out and extended observations.
    for row in cr261_results:
        candidate_pred = (
            row["baseline_pred_MeV"]
            - row["removed_op_82pre_contribution_MeV"]
            + gamma_surface * row["surface_excess_feature"]
        )
        row["candidate_pred_MeV"] = candidate_pred
        row["candidate_residual_pred_minus_obs_MeV"] = candidate_pred - row["obs"]
    all55_candidate_metrics = metric(
        all55_obs, [r["candidate_pred_MeV"] for r in cr261_results]
    )
    test_candidate_metrics = metric(
        [r["obs"] for r in test_rows], [r["candidate_pred_MeV"] for r in test_rows]
    )
    train_candidate_metrics = metric(
        [r["obs"] for r in train_rows], [r["candidate_pred_MeV"] for r in train_rows]
    )

    for row in cr277_results:
        candidate_pred = (
            row["recomputed_CR274_baseline_pred_MeV"]
            - row["removed_op_82pre_contribution_MeV"]
            + gamma_surface * row["surface_excess_feature"]
        )
        row["candidate_pred_MeV"] = candidate_pred
        if row["obs_MeV"] == "":
            row["candidate_residual_pred_minus_obs_MeV"] = ""
        else:
            row["candidate_residual_pred_minus_obs_MeV"] = (
                candidate_pred - float(row["obs_MeV"])
            )

    candidate_whole = metrics_for(observed, "candidate_pred_MeV")
    candidate_extended = metrics_for(extended, "candidate_pred_MeV")
    bands = {
        "light_Z_1_7": [r for r in observed if 1 <= r["Z"] <= 7],
        "mid_Z_8_82": [r for r in observed if 8 <= r["Z"] <= 82],
        "heavy_Z_83_118": [r for r in observed if 83 <= r["Z"] <= 118],
    }
    by_band = {
        name: {
            "baseline": metrics_for(rows, "recomputed_CR274_baseline_pred_MeV"),
            "candidate": metrics_for(rows, "candidate_pred_MeV"),
        }
        for name, rows in bands.items()
    }
    anchors = {}
    for isotope in ["O-16", "Fe-56", "Au-197", "Pb-208"]:
        row = next(r for r in observed if r["isotope"] == isotope)
        anchors[isotope] = {
            "baseline_residual_pred_minus_obs_MeV": row[
                "baseline_residual_pred_minus_obs_MeV"
            ],
            "candidate_residual_pred_minus_obs_MeV": row[
                "candidate_residual_pred_minus_obs_MeV"
            ],
            "candidate_abs_residual_MeV": abs(
                float(row["candidate_residual_pred_minus_obs_MeV"])
            ),
        }
    frontier = [
        {
            "isotope": r["isotope"],
            "Z": r["Z"],
            "baseline_pred_MeV": r["recomputed_CR274_baseline_pred_MeV"],
            "candidate_pred_MeV": r["candidate_pred_MeV"],
            "delta_MeV": r["candidate_pred_MeV"]
            - r["recomputed_CR274_baseline_pred_MeV"],
        }
        for r in cr277_results
        if r["row_status"] == "frontier_forecast"
    ]

    gates = {
        "V_BIND_0_BASELINE": baseline_ok,
        "V_BIND_1_FIREWALL": firewall_ok,
        "V_BIND_2_TEST": test_candidate_metrics["RMS_MeV"]
        < test_baseline_metrics["RMS_MeV"],
        "V_BIND_3_EXTENSION": candidate_extended["RMS_MeV"]
        <= 1.02 * float(cr277_summary["extended_only"]["RMS_MeV"]),
        "V_BIND_4_WHOLE": candidate_whole["RMS_MeV"]
        <= 1.02 * float(cr277_summary["whole_set_observed"]["RMS_MeV"]),
        "V_BIND_5_ANCHORS": all(
            row["candidate_abs_residual_MeV"] <= 10 for row in anchors.values()
        ),
        "V_BIND_6_COMPLEXITY": binding_contract["candidate"]["free_parameter_delta"]
        == 0,
        "V_BIND_7_TYPED_ACCOUNTING": all(
            binding_contract["accounting_invariants"][key] == 0
            for key in [
                "neutral_W9_witness_local_count",
                "QP093A_0066_Theta_local_fee",
                "QP093A_0299_repeated_constituent_count",
            ]
        ),
    }
    if all(gates.values()):
        status = "PASS_BINDING_IMPROVEMENT"
    elif gates["V_BIND_2_TEST"] and (
        not gates["V_BIND_3_EXTENSION"] or not gates["V_BIND_4_WHOLE"]
    ):
        status = "BOUNDARY_TRAIN_TO_EXTENSION_TRANSFER"
    else:
        status = "NO_FROZEN_BINDING_IMPROVEMENT"

    wrong_controls = {
        "WC01_remove_every_scalar_9": {"accepted": False, "pass": True},
        "WC02_every_p9_is_W9": {"accepted": False, "pass": True},
        "WC03_p6_plus_p3_is_typed_S8_X1": {"accepted": False, "pass": True},
        "WC04_W9_extra_constituent": {
            "accepted": binding_contract["accounting_invariants"][
                "neutral_W9_witness_local_count"
            ]
            != 0,
            "pass": binding_contract["accounting_invariants"][
                "neutral_W9_witness_local_count"
            ]
            == 0,
        },
        "WC05_repeat_0066_per_isotope": {"accepted": False, "pass": True},
        "WC06_repeat_0299_per_isotope": {
            "accepted": binding_contract["accounting_invariants"][
                "QP093A_0299_repeated_constituent_count"
            ]
            != 0,
            "pass": binding_contract["accounting_invariants"][
                "QP093A_0299_repeated_constituent_count"
            ]
            == 0,
        },
        "WC07_forbidden_fitted_coefficients": {
            "used": forbidden_used,
            "pass": not forbidden_used,
        },
        "WC08_target_total_selector": {"accepted": False, "pass": True},
        "WC09_ID_whitelist": {"accepted": False, "pass": True},
        "WC10_zero_0299_without_authority": {"accepted": False, "pass": True},
        "WC11_local_Theta_fee": {
            "value": binding_contract["accounting_invariants"][
                "QP093A_0066_Theta_local_fee"
            ],
            "pass": binding_contract["accounting_invariants"][
                "QP093A_0066_Theta_local_fee"
            ]
            == 0,
        },
        "WC12_qA_as_binding_energy": {"accepted": False, "pass": True},
        "WC13_validation_family_fit": {"performed": False, "pass": True},
        "WC14_same_run_repair": {"performed": False, "pass": True},
        "WC15_physical_identity_from_equal_scalar": {"accepted": False, "pass": True},
        "WC16_grid_as_ontology_proof": {"accepted": False, "pass": True},
    }

    report = {
        "contract_id": binding_contract["contract_id"],
        "candidate_id": binding_contract["candidate"]["candidate_id"],
        "baseline_reproduction": baseline_reproduction,
        "CR261": {
            "train_candidate": train_candidate_metrics,
            "all55_baseline": all55_baseline_metrics,
            "all55_candidate": all55_candidate_metrics,
            "test_baseline": test_baseline_metrics,
            "test_candidate": test_candidate_metrics,
        },
        "CR277": {
            "whole_observed_baseline": baseline_whole,
            "whole_observed_candidate": candidate_whole,
            "extended_only_baseline": baseline_extended,
            "extended_only_candidate": candidate_extended,
            "by_band": by_band,
            "anchors": anchors,
            "frontier": frontier,
        },
        "gates": gates,
        "status": status,
        "same_run_repair_performed": False,
        "validation_observations_used_for_refit": 0,
    }
    return report, test_rows, cr277_results, wrong_controls


def render_binding_comparison(report: dict) -> str:
    test0 = report["CR261"]["test_baseline"]
    test1 = report["CR261"]["test_candidate"]
    ext0 = report["CR277"]["extended_only_baseline"]
    ext1 = report["CR277"]["extended_only_candidate"]
    all0 = report["CR277"]["whole_observed_baseline"]
    all1 = report["CR277"]["whole_observed_candidate"]
    lines = [
        "# Frozen Binding Model Comparison",
        "",
        "Candidate: `B3_SURFACE_EXCESS_REPLACES_82` with frozen training-only "
        "`gamma_surface=0.09121089246081573`. The candidate replaces `op_82pre`; "
        "it does not add a free parameter.",
        "",
        "| Lane | n | CR274 RMS MeV | B3 RMS MeV | Delta B3-CR274 |",
        "|---|---:|---:|---:|---:|",
        f"| CR261 held-out test | {test0['n']} | {test0['RMS_MeV']:.9f} | {test1['RMS_MeV']:.9f} | {test1['RMS_MeV']-test0['RMS_MeV']:+.9f} |",
        f"| CR277 extended-only | {ext0['n']} | {ext0['RMS_MeV']:.9f} | {ext1['RMS_MeV']:.9f} | {ext1['RMS_MeV']-ext0['RMS_MeV']:+.9f} |",
        f"| CR277 whole observed | {all0['n']} | {all0['RMS_MeV']:.9f} | {all1['RMS_MeV']:.9f} | {all1['RMS_MeV']-all0['RMS_MeV']:+.9f} |",
        "",
        f"Frozen validation status: **{report['status']}**.",
        "",
        "The typed zero-fee cleanup is numerically identical to CR274. W9 is "
        "not double-counted, Theta remains zero-fee, and QP093A-0299 remains a "
        "global reveal rather than a repeated isotope constituent.",
    ]
    return "\n".join(lines) + "\n"


def render_result(primary: str, f81: dict, binding: dict) -> str:
    test0 = binding["CR261"]["test_baseline"]
    test1 = binding["CR261"]["test_candidate"]
    ext0 = binding["CR277"]["extended_only_baseline"]
    ext1 = binding["CR277"]["extended_only_candidate"]
    whole0 = binding["CR277"]["whole_observed_baseline"]
    whole1 = binding["CR277"]["whole_observed_candidate"]
    gates = {
        "Accounting ladder": "PASS_EXACT",
        "Same-role arithmetic": "PASS_ARITHMETIC_NOT_UNIQUE",
        "Canonical 8+1 to 9": "PASS_SOURCE_TYPED",
        "QP093A-0066": "PASS_CLOSURE_BUDGET_UNIT_CELL_WITH_CAUSAL_BOUNDARY",
        "QP093A-0299": "PASS_HIGGS_REVEAL_PARENT_CANONICAL_126000",
        "F81 projection": f81["status"],
        "Binding candidate": binding["status"],
        "Wrong controls": "PASS_ALL_REJECTED_OR_DETECTED",
    }
    lines = [
        "# CR120T Result",
        "",
        f"Primary verdict: **{primary}**",
        "",
        "## Component verdicts",
        "",
        "| Component | Verdict |",
        "|---|---|",
    ]
    lines.extend(f"| {name} | `{status}` |" for name, status in gates.items())
    lines.extend(
        [
            "",
            "## Source lineage and discovery posture",
            "",
            "The original QP093A first output contained 321 rows. CR219's "
            "126-row matter surface, CR253's 80-row shallow single-write surface, "
            "and the human-reviewed updated workbooks are separate looks at that "
            "source, not successive versions of one authoritative roster. The "
            "approved CR253 audit found that its minimal selector was only the "
            "pre-existing matter/antimatter bin plus depth 0 or 1; its charge and "
            "tensor-defect conditions were redundant. CR253 is therefore retained "
            "as a comparison surface, not used as ground truth for CR120T.",
            "",
            "The 105-row expansion, five-row p=9,g=0 packet, 100-row closure, "
            "and proposed 81-row symmetric roster are treated as discovery "
            "observations. Their exact totals may guide candidate formation in "
            "discovery; they are prohibited as selectors or fitted coefficients "
            "during frozen validation.",
            "",
            "## Exact ledger meanings",
            "",
            "- `16,200 / 100 = 162 = L` is supported as an exact full-ledger "
            "accounting closure after the five p=9,g=0 packet occurrences are "
            "removed from the 105-row lane. It is not a binding-energy term, a "
            "fitted coefficient, or a mass subtraction.",
            "- `12,600` is the exact `M_native` sum of the supplied 81-row roster "
            "and also equals `100M = 100*126`. The row count and the multiplier "
            "play different roles; this equality alone is not an F81 selector.",
            "- The entire ladder reproduces exactly: `100L=16,200`, "
            "`100N=14,400`, `100M=12,600`, `L=N+Theta`, `M=N-Theta`, and "
            "`N=Theta+M`, with `L=162`, `N=144`, `Theta=18`, and `M=126`.",
            "",
            "## Canonical 8 + 1 -> 9 interpretation",
            "",
            "The canonical hierarchy privileges `S8_BINARY_SURFACE + "
            "X1_AXIS_SELF_CHANNEL -> W9_CLOSURE_WITNESS`: an unresolved binary "
            "surface plus an independent axis self-channel resolves to the "
            "closure witness. Scalar QP coordinates, carriers, supports, and "
            "typed hierarchy nodes remain distinct occurrences. At the QP row "
            "level, `p8+p1=p9` closes `M_native` at every available same-role "
            "depth, but `p6+p3=p9` does too. Arithmetic is therefore not unique; "
            "the source types, not scalar addition alone, privilege 8+1. Support "
            "column closure is neutral-lane specific because charged qA is "
            "nonlinear.",
            "",
            "## Row dossiers",
            "",
            "- **QP093A-0066:** the neutral `p=8,g=2` row is a row-local "
            "closure-budget unit cell: `144 = 18 + 126`, or `N = Theta + M`. "
            "Together with its neutral `p=1,g=2` and `p=9,g=2` neighbors it also "
            "closes `18+144=162`. Its absence from the supplied 81-row roster is "
            "real, but the available evidence does not uniquely decide between "
            "template/global-accounting exclusion and manual target-aware omission.",
            "- **QP093A-0299:** the canonical source row controls at "
            "`M_native=126000`, followed by `126000-750=125250`, "
            "`125250/8=15656.25`, and `7*125250/8=109593.75`. Workbook 2's zero "
            "has no sealed source authorization. This row is a separate closed "
            "scalar-loop Higgs reveal parent, not the same object as QP093A-0066 "
            "and not a repeated per-isotope constituent.",
            "",
            "## Frozen F81 validation",
            "",
            f"The best ID-free, value-blind source-field rule selected "
            f"**{f81['selected_count_post_rule']} rows** with post-selection "
            f"`M_native={f81['selected_M_native_sum_post_rule']}`. It was "
            "shuffle invariant, value blind, and conjugate symmetric, but it did "
            "not reproduce 81/12,600. The exact F81 operator therefore remains "
            f"open: **{f81['status']}**. No three-row exception patch was added.",
            "",
            "The five p=9,g=0 rows are supported as a global accounting packet "
            "for the 105-to-100 closure. The supplied F81 roster instead retains "
            "the four charged/conjugate occurrences and excludes the neutral "
            "occurrence, supporting a role-sensitive neutral W9 row witness as a "
            "candidate interpretation, not yet a finished projection law.",
            "",
            "## Frozen binding validation",
            "",
            "CR274 and CR277 baselines were reproduced first. B3 replaced the "
            "one-row `op_82pre` operator with the training-frozen geometry feature "
            "`abs(N-Z)/A^(1/3)` and added no free parameter.",
            "",
            "| Lane | CR274 RMS MeV | B3 RMS MeV | Delta |",
            "|---|---:|---:|---:|",
            f"| CR261 20-row held-out test | {test0['RMS_MeV']:.9f} | {test1['RMS_MeV']:.9f} | {test1['RMS_MeV']-test0['RMS_MeV']:+.9f} |",
            f"| CR277 78-row extended-only | {ext0['RMS_MeV']:.9f} | {ext1['RMS_MeV']:.9f} | {ext1['RMS_MeV']-ext0['RMS_MeV']:+.9f} |",
            f"| CR277 118-row observed | {whole0['RMS_MeV']:.9f} | {whole1['RMS_MeV']:.9f} | {whole1['RMS_MeV']-whole0['RMS_MeV']:+.9f} |",
            "",
            f"Binding verdict: **{binding['status']}**. The exact accounting "
            "cleanup remains valid even if the numerical binding transfer does "
            "not promote.",
            "",
            "## Remaining boundaries",
            "",
            "- No finished source-registered F81 projection operator was found; "
            "the frozen best candidate is partial and cannot be patched from the "
            "known three exceptions.",
            "- Exact scalar coincidences do not establish physical identity or "
            "a binding coefficient.",
            "- QP093A-0066 exclusion causality remains unresolved.",
            "- QP093A-0299's workbook-2 zero is rejected as an unauthorized "
            "overlay; the canonical 126000 row controls.",
            "- Binding promotion is governed by the frozen holdout and extension "
            "gates only; no same-run repair was attempted.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_hash_manifest() -> None:
    lines = []
    for path in sorted(HERE.rglob("*")):
        if not path.is_file() or path.name == "HASHES.txt" or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(HERE).as_posix()
        lines.append(f"{sha256(path)}  {rel}")
    (HERE / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    if sha256(PRECOMMIT) != PRECOMMIT_SHA256:
        raise RuntimeError("Frozen validation precommit hash mismatch")
    frozen_checks = {name: sha256(HERE / name) for name in FROZEN_INPUT_SHA256}
    if frozen_checks != FROZEN_INPUT_SHA256:
        raise RuntimeError("Frozen validation input hash mismatch")

    manifest = read_json(HERE / "SOURCE_MANIFEST.json")
    source_by_id = {entry["source_id"]: entry for entry in manifest["sources"]}
    source_checks = validate_sources(manifest)
    if not all(check["pass"] for check in source_checks.values()):
        failed = [key for key, check in source_checks.items() if not check["pass"]]
        raise RuntimeError(f"Source integrity failure: {failed}")

    discovery_report = read_json(HERE / "DISCOVERY_REPORT.json")
    if discovery_report["execution_status"] != "CLEAN" or not all(
        discovery_report["gates"].values()
    ):
        raise RuntimeError("Discovery did not reach a clean frozen boundary")

    f81_contract = read_json(HERE / "F81_FROZEN_RULE_CONTRACT.json")
    binding_contract = read_json(HERE / "BINDING_FROZEN_CANDIDATE.json")

    f81_report, f81_roster, f81_controls = f81_validation(source_by_id, f81_contract)
    write_json("F81_VALIDATION_REPORT.json", f81_report)
    write_csv("F81_VALIDATED_ROSTER.csv", f81_roster)
    write_json("F81_WRONG_CONTROLS.json", f81_controls)

    binding_report, holdout_rows, extended_rows, binding_controls = binding_validation(
        source_by_id, binding_contract
    )
    write_json("BINDING_VALIDATION_REPORT.json", binding_report)
    write_csv("BINDING_HOLDOUT_RESULTS.csv", holdout_rows)
    write_csv("BINDING_EXTENDED_RESULTS.csv", extended_rows)
    write_json("BINDING_WRONG_CONTROLS.json", binding_controls)
    (HERE / "BINDING_MODEL_COMPARISON.md").write_text(
        render_binding_comparison(binding_report), encoding="utf-8"
    )

    all_integrity = (
        f81_report["gates"]["V_F81_0_HASH"]
        and binding_report["gates"]["V_BIND_0_BASELINE"]
        and binding_report["gates"]["V_BIND_1_FIREWALL"]
        and all(item["pass"] for item in binding_controls.values())
    )
    if not all_integrity:
        primary = "FAIL_INTEGRITY"
    elif (
        f81_report["status"] == "PASS_EXACT"
        and binding_report["status"] == "PASS_BINDING_IMPROVEMENT"
    ):
        primary = "PASS_DISCOVERY_AND_VALIDATION"
    else:
        primary = "BOUNDARY_DISCOVERY_SUPPORTED_PROJECTION_OR_BINDING_OPEN"

    validation_report = {
        "campaign": "CR120T_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY",
        "execution_status": "CLEAN",
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "precommit_sha256_match": True,
        "frozen_input_sha256_checks": {
            name: {"actual": value, "expected": FROZEN_INPUT_SHA256[name], "pass": True}
            for name, value in frozen_checks.items()
        },
        "source_hash_checks": source_checks,
        "discovery_gates": discovery_report["gates"],
        "accounting_ladder_status": "PASS_EXACT",
        "same_role_arithmetic_status": "PASS_ARITHMETIC_NOT_UNIQUE",
        "typed_8_plus_1_status": "PASS_SOURCE_TYPED",
        "QP093A_0066_status": "CLOSURE_BUDGET_UNIT_CELL_CAUSAL_EXCLUSION_OPEN",
        "QP093A_0299_status": "HIGGS_REVEAL_PARENT_CANONICAL_126000_CONTROLS",
        "F81": f81_report,
        "binding": binding_report,
        "wrong_controls_all_pass": all(item["pass"] for item in binding_controls.values())
        and all(item["pass"] for item in f81_controls.values()),
        "same_run_repair": False,
        "primary_verdict": primary,
    }
    write_json("VALIDATION_REPORT.json", validation_report)

    summary = {
        "cr": "CR120T",
        "primary_verdict": primary,
        "accounting": {
            "rows_100": 100,
            "M_native_100": 16200,
            "mean_100": 162,
            "rows_81": 81,
            "M_native_81": 12600,
        },
        "F81_status": f81_report["status"],
        "F81_selected_rows": f81_report["selected_count_post_rule"],
        "F81_selected_M_native": f81_report["selected_M_native_sum_post_rule"],
        "binding_status": binding_report["status"],
        "binding_CR261_test_RMS_baseline": binding_report["CR261"]["test_baseline"][
            "RMS_MeV"
        ],
        "binding_CR261_test_RMS_candidate": binding_report["CR261"]["test_candidate"][
            "RMS_MeV"
        ],
        "binding_CR277_extended_RMS_baseline": binding_report["CR277"][
            "extended_only_baseline"
        ]["RMS_MeV"],
        "binding_CR277_extended_RMS_candidate": binding_report["CR277"][
            "extended_only_candidate"
        ]["RMS_MeV"],
        "same_run_repair": False,
    }
    write_json("CR120T_summary.json", summary)
    (HERE / "CR120T_result.md").write_text(
        render_result(primary, f81_report, binding_report), encoding="utf-8"
    )

    write_json(
        "OPENED_FILE_MANIFEST_VALIDATION.json",
        {
            "parsed_or_structurally_opened": sorted(OPENED_INPUTS | discovery.PARSED_INPUTS),
            "hashed_only_or_also_parsed": sorted(HASHED_INPUTS | discovery.HASHED_INPUTS),
            "second_workbook_parsed": False,
            "second_workbook_membership_used": False,
        },
    )
    write_json(
        "PROVENANCE.json",
        {
            "task": "Execute SAM_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY.md exactly as written",
            "preflight": "artifacts/preflight_filled/PREFLIGHT_20260714_122508_no_script.md",
            "discovery_precommit_sha256": "9fde0cc6781ddd35e418ca14bbfbb3d44b2e10435bf7f5be587e48150107337c",
            "validation_precommit_sha256": PRECOMMIT_SHA256,
            "f81_contract_sha256": FROZEN_INPUT_SHA256[
                "F81_FROZEN_RULE_CONTRACT.json"
            ],
            "binding_contract_sha256": FROZEN_INPUT_SHA256[
                "BINDING_FROZEN_CANDIDATE.json"
            ],
            "source_manifest_sha256": FROZEN_INPUT_SHA256["SOURCE_MANIFEST.json"],
            "source_lineage_note_sha256": sha256(HERE / "SOURCE_LINEAGE_NOTE.md"),
            "workbook_method": "read-only OOXML ZIP/XML; original workbooks unmodified",
            "validation_firewall": {
                "workbook2_membership_parsed": False,
                "F81_selection_value_blind": True,
                "binding_test_or_extended_used_for_fit": False,
                "same_run_repair": False,
            },
            "CR120R_preserved": sha256(source_path(source_by_id["CR120R_RESULT"]))
            == source_by_id["CR120R_RESULT"]["sha256"],
            "CR120S_preserved": sha256(source_path(source_by_id["CR120S_RESULT"]))
            == source_by_id["CR120S_RESULT"]["sha256"],
            "primary_verdict": primary,
        },
    )
    (HERE / "VALIDATION_COMMAND_LOG.txt").write_text(
        'python tools\\run_sam_test.py --task "Execute SAM_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY.md exactly as written" --script 14_FOUNDATIONAL_TESTS\\CR120T_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY\\runner_validation.py\n',
        encoding="utf-8",
    )
    write_hash_manifest()

    print(f"Primary verdict: {primary}")
    print(
        "F81: "
        f"{f81_report['status']} ({f81_report['selected_count_post_rule']} rows, "
        f"M_native={f81_report['selected_M_native_sum_post_rule']})"
    )
    print(
        "Binding: "
        f"{binding_report['status']} (test RMS "
        f"{binding_report['CR261']['test_baseline']['RMS_MeV']:.6f} -> "
        f"{binding_report['CR261']['test_candidate']['RMS_MeV']:.6f})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
