from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent

EXPECTED_INPUT_HASHES = {
    "F81_CANDIDATE_RULES.json": "c6b16102993898762c2ba12a9e33340a2e30c744f6a5e85f513c6a613f2867dd",
    "F81_CANDIDATE_RULE_SCORECARD.csv": "5645382edcfd0eae7a82eabe93be0144ec4d07da2376fd94a35dae6ae592bf0e",
    "BINDING_DISCOVERY_RESULTS.csv": "76cb63f3175866a8aca1dd2999a4e9aa538e83f6db0916bf059959b0f02be5e8",
    "BINDING_BASELINE.json": "192096bd5e7354c243f015ea73d34fa26361852b14d7e8020e238ae6dfef2a06",
    "BINDING_FEATURE_DEFINITIONS.json": "89463644403a43ff733548a522456f1c0aeba9054db2323f2f1b2e9b4315bb68",
    "DISCOVERY_REPORT.json": "e600a27831fe2b82ad5ece146cc353a16eb586cf11809eb4cc363e6b3cd99811",
    "SOURCE_MANIFEST.json": "b1eee6ab1603c7a3ed5995afb5e1b3061b17f1c8aafce11d7db0f675a7769451",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(name: str):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def write_json(name: str, payload: dict) -> None:
    (HERE / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    actual_hashes = {name: sha256(HERE / name) for name in EXPECTED_INPUT_HASHES}
    if actual_hashes != EXPECTED_INPUT_HASHES:
        raise RuntimeError(
            "Discovery inputs do not match the reviewed freeze boundary: "
            + json.dumps(actual_hashes, sort_keys=True)
        )

    f81_candidates = load_json("F81_CANDIDATE_RULES.json")
    recommended = f81_candidates["recommended_for_freeze_review"]
    if recommended != "F81_TREE_DEPTH_5":
        raise RuntimeError(f"Unexpected recommended F81 rule: {recommended}")
    f81_rule = next(r for r in f81_candidates["rules"] if r["rule_id"] == recommended)
    score = f81_rule["score"]
    if score["uses_candidate_ids"] or score["uses_M_native"] or score["uses_target_count_or_sum"]:
        raise RuntimeError("F81 recommendation violates the validation firewall")
    if score["exceptions"] != 3 or score["selected_rows_reported_after_rule"] != 84:
        raise RuntimeError("F81 recommendation no longer matches the reviewed discovery result")

    f81_contract = {
        "contract_id": "CR120T_F81_FROZEN_SOURCE_TYPED_RULE_V1",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_at_freeze": "PARTIAL_STRUCTURAL_CANDIDATE_NOT_AN_EXACT_F81_OPERATOR",
        "selection_domain": f81_candidates["domain"],
        "domain_rows_at_discovery": f81_candidates["domain_rows"],
        "candidate": f81_rule,
        "selection_inputs_allowed": f81_rule["allowed_features"],
        "selection_inputs_forbidden": [
            "current_membership",
            "candidate_id_or_row_number",
            "target_count_81",
            "target_sum_12600",
            "M_native_or_any_value_column",
            "observed_binding_residuals",
        ],
        "validation_protocol": {
            "apply_rule_before_revealing_selected_count_or_M_native_sum": True,
            "no_exception_patch": True,
            "no_same_run_repair": True,
            "shuffle_invariance_required": True,
            "typed_wrong_controls_required": [
                "p6_plus_p3_arithmetic_control",
                "role_swap_control",
                "missing_conjugate_control",
                "duplicated_witness_control",
            ],
        },
        "discovery_boundary": {
            "membership_was_used_to_train_candidate": True,
            "rule_is_not_independent_evidence_for_the_81_row_roster": True,
            "discovery_exceptions_are_recorded_but_must_not_be_used_as_a_whitelist": score[
                "exception_ids_discovery_only"
            ],
            "post_rule_discovery_readout": {
                "selected_rows": score["selected_rows_reported_after_rule"],
                "selected_M_native_sum": score["selected_M_native_sum_reported_after_rule"],
            },
        },
        "frozen_input_sha256": actual_hashes,
    }
    write_json("F81_FROZEN_RULE_CONTRACT.json", f81_contract)

    with (HERE / "BINDING_DISCOVERY_RESULTS.csv").open(
        newline="", encoding="utf-8-sig"
    ) as handle:
        binding_rows = list(csv.DictReader(handle))
    b3 = next(r for r in binding_rows if r["candidate_id"] == "B3_SURFACE_EXCESS_REPLACES_82")
    if b3["eligible"] != "True" or b3["discovery_status"] != "TRAIN_ONLY_CANDIDATE":
        raise RuntimeError("B3 is not eligible at the reviewed freeze boundary")
    if int(b3["free_parameter_delta"]) != 0:
        raise RuntimeError("B3 changed the free-parameter count")

    baseline = load_json("BINDING_BASELINE.json")
    definitions = load_json("BINDING_FEATURE_DEFINITIONS.json")
    if baseline["candidate_selection_rows"] != 35:
        raise RuntimeError("Binding discovery lane is not the frozen 35-row training lane")
    if baseline["test_observations_scored"] or baseline["extended_observations_scored"]:
        raise RuntimeError("Held-out observations were opened before freeze")

    binding_contract = {
        "contract_id": "CR120T_BINDING_FROZEN_SURFACE_EXCESS_V1",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_at_freeze": "TRAIN_SELECTED_CANDIDATE_REQUIRING_FROZEN_VALIDATION",
        "baseline": {
            "model": "CR274 frozen combined model",
            "beta_K": baseline["controlling_CR274"]["beta_K"],
            "operators": baseline["controlling_CR274"]["operators"],
            "train_metrics": baseline["train_metrics_frozen_CR274"],
            "source_sha256": EXPECTED_INPUT_HASHES["BINDING_BASELINE.json"],
        },
        "accounting_invariants": {
            "candidate_id": "B1_TYPED_ZERO_FEE_CLEANUP",
            "neutral_W9_witness_local_count": 0,
            "QP093A_0066_Theta_local_fee": 0,
            "QP093A_0299_repeated_constituent_count": 0,
            "expected_numeric_effect_relative_to_CR274": 0,
        },
        "candidate": {
            "candidate_id": b3["candidate_id"],
            "formula": "B_candidate = B_CR274 - gamma_82pre*op_82pre + gamma_surface*abs(N-Z)/A^(1/3)",
            "removed_operator": b3["removed_operator"],
            "removed_operator_gamma": baseline["controlling_CR274"]["operators"][
                b3["removed_operator"]
            ]["gamma"],
            "added_feature": b3["formula"],
            "gamma_surface": float(b3["gamma"]),
            "free_parameter_delta": int(b3["free_parameter_delta"]),
            "selection_basis": "lowest eligible non-baseline RMS on the original 35-row training lane with zero free-parameter delta",
            "train_metrics": {
                "n": int(b3["n"]),
                "RMS_MeV": float(b3["RMS_MeV"]),
                "mean_residual_MeV": float(b3["mean_residual_MeV"]),
                "MAE_MeV": float(b3["MAE_MeV"]),
                "within_5": int(b3["within_5"]),
                "within_8": int(b3["within_8"]),
                "max_abs_MeV": float(b3["max_abs_MeV"]),
            },
        },
        "forbidden_fitted_coefficients": definitions["forbidden_fitted_coefficients"],
        "validation_firewall": {
            "candidate_formula_and_gamma_are_immutable": True,
            "held_out_lane": "CR261 rows marked test (20)",
            "extended_lane": "CR277 observed rows not in the original CR261 55-row roster",
            "no_observed_binding_residual_used_for_selection_or_repair": True,
            "no_same_run_repair": True,
            "no_per_isotope_or_target_specific_parameters": True,
        },
        "frozen_input_sha256": actual_hashes,
    }
    write_json("BINDING_FROZEN_CANDIDATE.json", binding_contract)

    print("F81 candidate frozen: F81_TREE_DEPTH_5 (partial; 84 rows in discovery)")
    print("Binding candidate frozen: B3_SURFACE_EXCESS_REPLACES_82")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
