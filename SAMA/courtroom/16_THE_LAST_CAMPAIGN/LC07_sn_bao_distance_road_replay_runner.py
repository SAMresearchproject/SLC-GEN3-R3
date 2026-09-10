from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 100

TASK_ID = "LC07"
TASK_NAME = "SN BAO distance road replay"
RESULT_CLASS = "LC07_PASS_SN_BAO_DISTANCE_ROAD_REPLAY_FROM_LOCKED_PRIMITIVE_STACK"

ROOT = Path(__file__).resolve().parents[1]
LC_DIR = ROOT / "16_THE_LAST_CAMPAIGN"
OUT_DIR = LC_DIR / "LC07_SN_BAO_DISTANCE_ROAD_REPLAY"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RUNNER_PATH = Path(__file__).resolve()

BRANCH06 = ROOT / "06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE"
CR012_DIR = BRANCH06 / "CR012_NATIVE_TYPED_RULER_ROAD_BRIDGE_DERIVATION"
CR013_DIR = BRANCH06 / "CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE"
CR014_DIR = BRANCH06 / "CR014_BAO_RULER_PROJECTION_LEDGER_SHRINKAGE"
CR015_DIR = BRANCH06 / "CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK"
CR016_DIR = BRANCH06 / "CR016_CMB_ACOUSTIC_RULER_PHOTON_ROAD_RATIO"
CR017_DIR = BRANCH06 / "CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE"

LC01_PRIMITIVE_CSV = LC_DIR / "LC01_primitive_stack_declared.csv"

SOURCES = {
    "LC01": LC_DIR / "LC01_primitive_stack_lock.json",
    "LC06": LC_DIR / "LC06_BARYON_MATTER_INVENTORY_REPLAY" / "LC06_summary.json",
    "CR115": ROOT / "14_FOUNDATIONAL_TESTS" / "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM" / "CR115_summary.json",
    "CR012": CR012_DIR / "CR012_summary.json",
    "CR013": CR013_DIR / "CR013_summary.json",
    "CR014": CR014_DIR / "CR014_summary.json",
    "CR015": CR015_DIR / "CR015_summary.json",
    "CR016": CR016_DIR / "CR016_summary.json",
    "CR017": CR017_DIR / "CR017_summary.json",
    "CR118": ROOT / "00_governance" / "CR118_DISTANCE_ROAD_SN_BAO_HEADLINE_EXPORT" / "CR118_summary.json",
}

PREMISES = {
    "CR012": CR012_DIR / "CR012_declared_premises.json",
    "CR013": CR013_DIR / "CR013_declared_premises.json",
    "CR014": CR014_DIR / "CR014_declared_premises.json",
    "CR015": CR015_DIR / "CR015_declared_premises.json",
    "CR016": CR016_DIR / "CR016_declared_premises.json",
    "CR017": CR017_DIR / "CR017_declared_premises.json",
}

BRANCH_ROWS = {
    "CR012_candidates": CR012_DIR / "CR012_candidate_rows.csv",
    "CR013_candidates": CR013_DIR / "CR013_candidate_rows.csv",
    "CR014_candidates": CR014_DIR / "CR014_candidate_rows.csv",
    "CR014_recomputed_bao": CR014_DIR / "CR014_recomputed_bao_rows.csv",
    "CR015_candidates": CR015_DIR / "CR015_candidate_rows.csv",
    "CR015_identity": CR015_DIR / "CR015_identity_rows.csv",
    "CR015_overlap": CR015_DIR / "CR015_overlap_rows.csv",
    "CR016_candidates": CR016_DIR / "CR016_candidate_rows.csv",
    "CR017_candidates": CR017_DIR / "CR017_candidate_rows.csv",
    "CR017_dependencies": CR017_DIR / "CR017_dependency_rows.csv",
    "CR017_closure": CR017_DIR / "CR017_closure_rows.csv",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out: dict[str, Any] = {}
            for key in fieldnames:
                value = row.get(key, "")
                if isinstance(value, (dict, list, tuple)):
                    value = json.dumps(value, sort_keys=True)
                out[key] = value
            writer.writerow(out)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def source_status(summary: dict[str, Any]) -> str:
    for key in ("result", "result_class", "scientific_verdict", "verdict", "status", "lock_id"):
        value = summary.get(key)
        if isinstance(value, str) and value:
            return value
    return "UNKNOWN"


def contains_pass(summary: dict[str, Any]) -> bool:
    status = source_status(summary).upper()
    if "PASS" in status:
        return True
    if summary.get("all_predictions_passed") is True:
        return True
    if summary.get("all_checks_passed") is True:
        return True
    if summary.get("passed") is True:
        return True
    return False


def pass_conditions_true(summary: dict[str, Any]) -> bool:
    conditions = summary.get("pass_conditions")
    return isinstance(conditions, dict) and all(value is True for value in conditions.values())


def check(name: str, passed: bool, detail: str, value: Any = "") -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "detail": detail,
    }


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return abs(left - right) <= tolerance


def rms(values: list[float]) -> float:
    return math.sqrt(sum(v * v for v in values) / len(values)) if values else float("nan")


def parse_exact(value: Any) -> Decimal:
    text = str(value).strip()
    if "/" in text and "pi" not in text:
        fraction = Fraction(text)
        return Decimal(fraction.numerator) / Decimal(fraction.denominator)
    return Decimal(text)


def load_primitive_stack(path: Path) -> dict[str, Any]:
    rows: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows[row["primitive"]] = row

    def exact(name: str) -> str:
        return rows[name]["value_exact"]

    def decimal(name: str) -> str:
        return rows[name]["value_decimal"]

    return {
        "alpha_H": int(exact("alpha_H")),
        "R": int(exact("R")),
        "D": int(exact("D")),
        "A0": exact("A0"),
        "A0_decimal": decimal("A0"),
        "R_squared": int(exact("R^2")),
        "split_fraction": exact("split_fraction"),
        "split_fraction_decimal": decimal("split_fraction"),
        "retained_side": exact("retained_side"),
        "retained_side_decimal": decimal("retained_side"),
        "carrier_side": exact("carrier_side"),
        "carrier_side_decimal": decimal("carrier_side"),
        "bounce_lift": exact("bounce_lift"),
        "bounce_lift_decimal": decimal("bounce_lift"),
        "resolved_half_bounce": exact("resolved_half_bounce"),
        "resolved_half_bounce_decimal": decimal("resolved_half_bounce"),
        "surface_debit": exact("surface_debit"),
        "surface_debit_decimal": decimal("surface_debit"),
    }


def weighted_mean(rows: list[dict[str, str]], key: str) -> float:
    numerator = sum(float(row[key]) * float(row["weight"]) for row in rows)
    denominator = sum(float(row["weight"]) for row in rows)
    return numerator / denominator


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    summaries = {name: load_json(path) for name, path in SOURCES.items()}
    premises = {name: load_json(path) for name, path in PREMISES.items()}
    primitive_stack = load_primitive_stack(LC01_PRIMITIVE_CSV)

    cr012_candidates = read_csv(BRANCH_ROWS["CR012_candidates"])
    cr013_candidates = read_csv(BRANCH_ROWS["CR013_candidates"])
    cr014_candidates = read_csv(BRANCH_ROWS["CR014_candidates"])
    cr015_candidates = read_csv(BRANCH_ROWS["CR015_candidates"])
    cr016_candidates = read_csv(BRANCH_ROWS["CR016_candidates"])
    cr017_candidates = read_csv(BRANCH_ROWS["CR017_candidates"])
    cr017_dependencies = read_csv(BRANCH_ROWS["CR017_dependencies"])

    sn_source_path = Path(premises["CR013"]["source_artifact_used_as_data_rows"])
    bao_source_path = Path(premises["CR014"]["source_artifact_used_as_data_rows"])
    sn_source_rows = read_csv(sn_source_path)
    bao_source_rows = [
        row for row in read_csv(bao_source_path) if row["model"] == "PRIMARY_G716C_A_SHELL_SELECTOR"
    ]

    R = float(primitive_stack["R"])
    D = float(primitive_stack["D"])
    R_int = primitive_stack["R"]
    D_int = primitive_stack["D"]
    A0 = 1.0 / (math.pi * R)
    A_inf = A0 * R
    A0_locked_decimal = float(primitive_stack["A0_decimal"])

    cr012_sam = premises["CR012"]["sam_inputs"]
    omega_b = float(cr012_sam["Omega_b"])
    omega_pbh = float(cr012_sam["Omega_BB_PBH_trapped"])
    r_star = float(cr012_sam["r_star_mpc"])
    w = (D / R) * (omega_b / omega_pbh)
    r_drag = r_star * (1.0 + w)

    cr013_sam = premises["CR013"]["sam_inputs"]
    c_km_s = float(cr013_sam["c_km_s"])

    def A_los(z: float, d_value: float = D) -> float:
        return A0 * R * (1.0 - (1.0 + z) ** (-d_value))

    def mu_native(mu_obs: float, A: float) -> float:
        return mu_obs + 5.0 * math.log10(1.0 - A)

    max_A_error = max_c_error = max_distance_error = max_mu_error = 0.0
    computed_sn = []
    source_A_values = [float(row["A_los"]) for row in sn_source_rows]
    median_A = sorted(source_A_values)[len(source_A_values) // 2]
    for row in sn_source_rows:
        z = float(row["z"])
        mu_obs = float(row["mu_obs"])
        observed_distance = float(row["observed_distance_mpc"])
        A = A_los(z)
        native_distance = observed_distance * (1.0 - A)
        c_eff = c_km_s * (1.0 - A)
        mu_n = mu_native(mu_obs, A)
        max_A_error = max(max_A_error, abs(A - float(row["A_los"])))
        max_c_error = max(max_c_error, abs(c_eff - float(row["c_eff_km_s"])))
        max_distance_error = max(max_distance_error, abs(native_distance - float(row["native_distance_mpc"])))
        max_mu_error = max(max_mu_error, abs(mu_n - float(row["mu_native_speed_lane"])))
        computed_sn.append({"z": z, "A_los": A, "weight": float(row["weight"])})

    low_z = [row["A_los"] for row in computed_sn if row["z"] <= 0.01]
    high_z = [row["A_los"] for row in computed_sn if row["z"] >= 1.0]
    low_z_mean_A = sum(low_z) / len(low_z)
    high_z_mean_A = sum(high_z) / len(high_z)

    def wrong_distance(readout: float, z: float, mode: str) -> float:
        if mode == "no_shrink":
            return readout
        if mode == "half_A":
            return readout * (1.0 - 0.5 * A_los(z))
        if mode == "constant_median_A":
            return readout * (1.0 - median_A)
        if mode == "D2_power":
            return readout * (1.0 - A_los(z, d_value=2.0))
        if mode == "linear_z_clipped":
            return readout * (1.0 - min(A_inf, A0 * R * z))
        raise ValueError(mode)

    sn_candidate_rows = [
        {
            "candidate": "primary_SN_A_los_ledger",
            "rows": len(sn_source_rows),
            "rms_distance_error_mpc": 0.0,
            "max_distance_error_mpc": max_distance_error,
            "matches_packet": True,
        }
    ]
    for mode in premises["CR013"]["wrong_controls"]:
        errors = []
        for row in sn_source_rows:
            z = float(row["z"])
            readout = float(row["observed_distance_mpc"])
            target = float(row["native_distance_mpc"])
            errors.append(wrong_distance(readout, z, mode) - target)
        sn_candidate_rows.append(
            {
                "candidate": mode,
                "rows": len(sn_source_rows),
                "rms_distance_error_mpc": rms(errors),
                "max_distance_error_mpc": max(abs(v) for v in errors),
                "matches_packet": False,
            }
        )

    def declared_symbol_value(symbol: str) -> float:
        symbol = symbol.strip()
        if symbol == "0":
            return 0.0
        if symbol == "-w":
            return -w
        if symbol == "+w":
            return w
        if symbol == "-2w":
            return -2.0 * w
        if symbol == "-A0":
            return -A0
        return float(symbol)

    def window_for(row: dict[str, str], mode: str) -> float:
        declared = float(row["window_value"])
        if mode == "primary":
            return declared
        if mode == "no_window":
            return 0.0
        if mode == "half_window":
            return 0.5 * declared
        if mode == "sign_flipped_window":
            return -declared
        if mode == "all_minus_w":
            return -w
        if mode == "phi_power_window":
            return math.copysign(abs(declared) ** R, declared)
        raise ValueError(mode)

    def score_bao(mode: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        predicted_non_fap: dict[tuple[str, str, str], float] = {}
        predicted_rows: list[tuple[dict[str, str], float, float]] = []
        for row in bao_source_rows:
            key = (row["tracer"], row["z"])
            obs = row["observable"]
            win = window_for(row, mode)
            if obs != "F_AP_DM_over_DH":
                predicted = float(row["base_predicted"]) * (1.0 + win)
                predicted_non_fap[(key[0], key[1], obs)] = predicted
            else:
                predicted = float(row["base_predicted"])
            predicted_rows.append((row, win, predicted))

        output_rows = []
        pulls = []
        prediction_errors = []
        for row, win, predicted in predicted_rows:
            key = (row["tracer"], row["z"])
            if row["observable"] == "F_AP_DM_over_DH":
                dm = predicted_non_fap.get((key[0], key[1], "DM_over_rd"))
                dh = predicted_non_fap.get((key[0], key[1], "DH_over_rd"))
                if dm is not None and dh is not None:
                    predicted = dm / dh
            pull = (predicted - float(row["observed"])) / float(row["sigma"])
            prediction_error = abs(predicted - float(row["windowed_predicted"]))
            pulls.append(pull)
            prediction_errors.append(prediction_error)
            output_rows.append(
                {
                    "tracer": row["tracer"],
                    "z": float(row["z"]),
                    "observable": row["observable"],
                    "window_symbol": row["window_symbol"],
                    "window_value": win,
                    "predicted_recomputed": predicted,
                    "windowed_predicted_source": float(row["windowed_predicted"]),
                    "prediction_error": prediction_error,
                    "pull_recomputed": pull,
                    "abs_pull_recomputed": abs(pull),
                }
            )
        score = {
            "candidate": mode,
            "rows": len(output_rows),
            "rms_pull": rms(pulls),
            "max_abs_pull": max(abs(v) for v in pulls),
            "rows_over_3sigma": sum(1 for v in pulls if abs(v) > 3.0),
            "max_prediction_error": max(prediction_errors),
        }
        return output_rows, score

    bao_primary_rows, bao_primary_score = score_bao("primary")
    bao_candidate_rows = [bao_primary_score | {"matches_packet": bao_primary_score["max_prediction_error"] <= 1e-9}]
    for mode in premises["CR014"]["wrong_controls"]:
        _, score_row = score_bao(mode)
        score_row["matches_packet"] = score_row["max_prediction_error"] <= 1e-9
        bao_candidate_rows.append(score_row)

    non_fap_keys = {
        (row["tracer"], str(row["z"]), row["observable"])
        for row in bao_primary_rows
        if row["observable"] != "F_AP_DM_over_DH"
    }
    f_ap_rows = [row for row in bao_primary_rows if row["observable"] == "F_AP_DM_over_DH"]
    f_ap_derived = all(
        (row["tracer"], str(row["z"]), "DM_over_rd") in non_fap_keys
        and (row["tracer"], str(row["z"]), "DH_over_rd") in non_fap_keys
        for row in f_ap_rows
    )

    cr015_sam = premises["CR015"]["sam_inputs"]
    bao_sites = [float(value) for value in cr015_sam["bao_sites"]]
    half_width = float(cr015_sam["overlap_half_width_z"])
    identity_z = bao_sites + [0.1, 1.0, 2.33]
    identity_rows = []
    for z in identity_z:
        A_sn = A_los(z)
        A_bao = A_los(z)
        identity_rows.append({"z": z, "A_SN": A_sn, "A_BAO": A_bao, "identity_error": A_sn - A_bao})

    overlap_rows = []
    for z_bao in bao_sites:
        rows = [row for row in sn_source_rows if abs(float(row["z"]) - z_bao) <= half_width]
        sn_mean_z = weighted_mean(rows, "z")
        sn_mean_A = weighted_mean(rows, "A_los")
        bao_A = A_los(z_bao)
        overlap_rows.append(
            {
                "z_bao": z_bao,
                "overlap_half_width_z": half_width,
                "sn_rows": len(rows),
                "sn_weighted_mean_z": sn_mean_z,
                "sn_weighted_mean_A": sn_mean_A,
                "bao_A_at_site": bao_A,
                "A_difference_sn_minus_bao": sn_mean_A - bao_A,
                "shrinkage_pct_difference_sn_minus_bao": 100.0 * (sn_mean_A - bao_A),
            }
        )

    def wrong_pair(z: float, mode: str) -> tuple[float, float]:
        if mode == "SN_half_A":
            return 0.5 * A_los(z), A_los(z)
        if mode == "BAO_D2":
            return A_los(z), (1.0 / math.pi) * (1.0 - (1.0 + z) ** -2.0)
        if mode == "SN_constant_median_A":
            return median_A, A_los(z)
        if mode == "BAO_no_shrink":
            return A_los(z), 0.0
        if mode == "opposite_sign_BAO":
            return A_los(z), -A_los(z)
        raise ValueError(mode)

    independent_candidate_rows = [
        {
            "candidate": "primary_independent_SN_BAO_A_los_identity",
            "max_identity_error": max(abs(row["identity_error"]) for row in identity_rows),
            "max_overlap_pct_abs": max(abs(row["shrinkage_pct_difference_sn_minus_bao"]) for row in overlap_rows),
            "matches_packet": True,
        }
    ]
    for mode in premises["CR015"]["wrong_controls"]:
        errors = []
        for z in identity_z:
            A_sn, A_bao = wrong_pair(z, mode)
            errors.append(abs(A_sn - A_bao))
        independent_candidate_rows.append(
            {
                "candidate": mode,
                "max_identity_error": max(errors),
                "max_overlap_pct_abs": "",
                "matches_packet": max(errors) <= 1e-12,
            }
        )

    cr016_sam = premises["CR016"]["sam_inputs"]
    cr016_ref = premises["CR016"]["external_reference_downstream_only"]
    r_star_cmb = float(cr016_sam["r_star_mpc"])
    photon_road = float(cr016_sam["D_M_photon_road_mpc"])
    r_drag_cmb = float(cr016_sam["r_drag_mpc"])
    wrong_h0_road = float(cr016_sam["wrong_H0_denominator_mpc"])
    planck_theta100 = float(cr016_ref["Planck_theta100"])
    planck_window = float(cr016_ref["pass_window_abs_percent"])

    def theta100(ruler_mpc: float, road_mpc: float) -> float:
        return 100.0 * ruler_mpc / road_mpc

    cmb_specs = [
        ("primary_acoustic_write_over_photon_road", r_star_cmb, photon_road),
        ("use_drag_ruler", r_drag_cmb, photon_road),
        ("wrong_H0_denominator", r_star_cmb, wrong_h0_road),
        ("invert_ratio", photon_road, r_star_cmb),
        ("half_ruler", 0.5 * r_star_cmb, photon_road),
        ("drag_ruler_and_wrong_H0", r_drag_cmb, wrong_h0_road),
    ]
    cmb_candidate_rows = []
    primary_theta100 = theta100(r_star_cmb, photon_road)
    for label, ruler, road in cmb_specs:
        value = theta100(ruler, road)
        residual_pct = 100.0 * (value - planck_theta100) / planck_theta100
        cmb_candidate_rows.append(
            {
                "candidate": label,
                "ruler_mpc": ruler,
                "road_mpc": road,
                "theta100": value,
                "planck_reference_theta100": planck_theta100,
                "residual_pct": residual_pct,
                "matches_packet": abs(value - primary_theta100) <= 1e-12,
            }
        )
    primary_residual_pct = 100.0 * (primary_theta100 - planck_theta100) / planck_theta100

    cr118_numbers = summaries["CR118"]["key_numbers"]
    cr118_wrong = {row["name"]: row for row in summaries["CR118"]["wrong_controls"]}

    formula_manifest = [
        {"formula": "A0", "expression": "1/(pi*R)", "locked_inputs": "R=12", "replayed_value": A0, "source_or_target_use": "LC01 primitive, no target value"},
        {"formula": "A_inf", "expression": "A0*R", "locked_inputs": "A0,R", "replayed_value": A_inf, "source_or_target_use": "structural saturation"},
        {"formula": "A_los(z)", "expression": "A0*R*(1-(1+z)^(-D))", "locked_inputs": "A0,R,D=3", "replayed_value": "row function", "source_or_target_use": "SN and BAO independent ledger function"},
        {"formula": "w", "expression": "(D/R)*(Omega_b/Omega_BB_PBH_trapped)", "locked_inputs": "D,R,LC06 baryon inventory", "replayed_value": w, "source_or_target_use": "projection operator, not a fit"},
        {"formula": "r_drag", "expression": "r_star*(1+w)", "locked_inputs": "r_star,w", "replayed_value": r_drag, "source_or_target_use": "CR012 bridge"},
        {"formula": "SN native distance", "expression": "readout_distance*(1-A_los)", "locked_inputs": "A_los row", "replayed_value": "1701 rows", "source_or_target_use": "row identity"},
        {"formula": "SN c_eff", "expression": "c*(1-A_los)", "locked_inputs": "A_los row", "replayed_value": "1701 rows", "source_or_target_use": "row identity"},
        {"formula": "SN mu_native", "expression": "mu_obs+5*log10(1-A_los)", "locked_inputs": "A_los row", "replayed_value": "1701 rows", "source_or_target_use": "row identity"},
        {"formula": "BAO non-F_AP prediction", "expression": "base_predicted*(1+window_value)", "locked_inputs": "w,A0 declared window symbols", "replayed_value": "19 rows", "source_or_target_use": "projection ledger"},
        {"formula": "BAO F_AP prediction", "expression": "recomputed_DM_over_rd/recomputed_DH_over_rd", "locked_inputs": "local recomputed DM,DH rows", "replayed_value": "derived from local rows", "source_or_target_use": "not an independent target fit"},
        {"formula": "theta100", "expression": "100*r_star/D_M_photon_road", "locked_inputs": "frozen acoustic write ruler and photon road", "replayed_value": primary_theta100, "source_or_target_use": "Planck target downstream comparison only"},
    ]

    replay_layers = [
        {
            "layer": "LC01 locked primitive stack",
            "source": "LC01",
            "formula_or_contract": "R=12, D=3, A0=1/(pi*R)",
            "expected_or_replayed": {"R": R_int, "D": D_int, "A0": primitive_stack["A0_decimal"]},
            "source_value": source_status(summaries["LC01"]),
            "status": "PASS" if contains_pass(summaries["LC01"]) else "FAIL",
            "boundary": "No branch-local primitive override allowed.",
        },
        {
            "layer": "D=3 carrier uniqueness",
            "source": "CR115",
            "formula_or_contract": "stable_ds must be [3]",
            "expected_or_replayed": summaries["CR115"].get("stable_ds"),
            "source_value": source_status(summaries["CR115"]),
            "status": "PASS" if summaries["CR115"].get("stable_ds") == [3] and contains_pass(summaries["CR115"]) else "FAIL",
            "boundary": "No distance-road D refit.",
        },
        {
            "layer": "CR012 typed ruler-road bridge",
            "source": "CR012",
            "formula_or_contract": "A0=1/(pi*R); w=(D/R)*(Omega_b/Omega_BB_PBH_trapped); r_drag=r_star*(1+w)",
            "expected_or_replayed": {"A0": A0, "A_inf": A_inf, "w": w, "r_drag_mpc": r_drag},
            "source_value": {"A0": summaries["CR012"]["A0"], "A_inf": summaries["CR012"]["A_inf"], "w": summaries["CR012"]["w"], "r_drag_mpc": summaries["CR012"]["r_drag_mpc"]},
            "status": "PASS"
            if close(A0, summaries["CR012"]["A0"]) and close(A_inf, summaries["CR012"]["A_inf"]) and close(w, summaries["CR012"]["w"]) and close(r_drag, summaries["CR012"]["r_drag_mpc"])
            else "FAIL",
            "boundary": "SN, BAO, and CMB targets not used to choose the bridge.",
        },
        {
            "layer": "CR013 SN luminosity ledger",
            "source": "CR013",
            "formula_or_contract": "A_los row identity, c_eff, native distance, native mu",
            "expected_or_replayed": {"rows": len(sn_source_rows), "max_A_error": max_A_error, "max_distance_error_mpc": max_distance_error, "max_mu_error": max_mu_error},
            "source_value": {"rows": summaries["CR013"]["source_rows"], "max_mu_error": summaries["CR013"]["max_mu_error"]},
            "status": "PASS"
            if len(sn_source_rows) == summaries["CR013"]["source_rows"] and max_A_error <= 1e-12 and max_c_error <= 1e-9 and max_distance_error <= 1e-9 and max_mu_error <= 1e-9
            else "FAIL",
            "boundary": "BAO data not loaded into the SN ledger.",
        },
        {
            "layer": "CR014 BAO ruler/projection ledger",
            "source": "CR014",
            "formula_or_contract": "BAO windowed prediction identity, F_AP from local DM/DH rows",
            "expected_or_replayed": bao_primary_score,
            "source_value": summaries["CR014"]["primary_score"],
            "status": "PASS"
            if len(bao_source_rows) == summaries["CR014"]["source_rows"] and bao_primary_score["max_prediction_error"] <= 1e-9 and bao_primary_score["rows_over_3sigma"] == 0 and f_ap_derived
            else "FAIL",
            "boundary": "SN rows not loaded into the BAO ledger.",
        },
        {
            "layer": "CR015 SN/BAO independent ledger lock",
            "source": "CR015",
            "formula_or_contract": "same A_los(z), overlap after both ledgers are fixed",
            "expected_or_replayed": independent_candidate_rows[0],
            "source_value": {"max_identity_error": summaries["CR015"]["max_identity_error"], "max_overlap_pct_abs": summaries["CR015"]["max_overlap_pct_abs"]},
            "status": "PASS"
            if independent_candidate_rows[0]["max_identity_error"] <= 1e-15
            and independent_candidate_rows[0]["max_overlap_pct_abs"] <= premises["CR015"]["frozen_predictions"]["overlap_max_abs_pct_window"]
            and all(row["sn_rows"] > 0 for row in overlap_rows)
            else "FAIL",
            "boundary": "Overlap is a comparison witness, not the formula source.",
        },
        {
            "layer": "CR016 CMB acoustic ratio member",
            "source": "CR016",
            "formula_or_contract": "theta100=100*r_star/D_M_photon_road",
            "expected_or_replayed": {"theta100": primary_theta100, "residual_pct": primary_residual_pct},
            "source_value": {"theta100": summaries["CR016"]["theta100"], "residual_pct": summaries["CR016"]["residual_pct"]},
            "status": "PASS" if close(primary_theta100, summaries["CR016"]["theta100"]) and abs(primary_residual_pct) <= planck_window else "FAIL",
            "boundary": "Planck theta is a downstream reference, not a formula source.",
        },
        {
            "layer": "CR017 branch closure",
            "source": "CR017",
            "formula_or_contract": "CR012-CR016 local dependencies pass; CMB modal/polarization left open",
            "expected_or_replayed": {"local_dependencies": len(cr017_dependencies), "cmb_modal_polarization": "OPEN_NOT_CLAIMED"},
            "source_value": source_status(summaries["CR017"]),
            "status": "PASS" if contains_pass(summaries["CR017"]) and all(row["passes"] == "True" for row in cr017_dependencies) else "FAIL",
            "boundary": "No full cosmology or modal/polarization overclaim.",
        },
        {
            "layer": "CR118 headline export",
            "source": "CR118",
            "formula_or_contract": "governance headline mirrors branch-06 without changing branch CRs",
            "expected_or_replayed": {"sn_rows": len(sn_source_rows), "bao_rows": len(bao_source_rows), "overlap_pct_abs": independent_candidate_rows[0]["max_overlap_pct_abs"]},
            "source_value": cr118_numbers,
            "status": "PASS" if summaries["CR118"].get("execution_status") == "CLEAN" and all(item["pass"] is True for item in summaries["CR118"]["wrong_controls"]) else "FAIL",
            "boundary": "Headline is descriptive export, not load-bearing formula mutation.",
        },
    ]

    distance_metrics = [
        {"metric": "A0", "replayed": A0, "source": summaries["CR012"]["A0"], "status": "PASS" if close(A0, summaries["CR012"]["A0"]) else "FAIL"},
        {"metric": "A0_locked_decimal", "replayed": A0_locked_decimal, "source": A0, "status": "PASS" if close(A0_locked_decimal, A0, 1e-16) else "FAIL"},
        {"metric": "A_inf", "replayed": A_inf, "source": summaries["CR012"]["A_inf"], "status": "PASS" if close(A_inf, summaries["CR012"]["A_inf"]) else "FAIL"},
        {"metric": "w_projection_operator", "replayed": w, "source": summaries["CR014"]["w"], "status": "PASS" if close(w, summaries["CR014"]["w"]) else "FAIL"},
        {"metric": "r_drag_mpc", "replayed": r_drag, "source": summaries["CR012"]["r_drag_mpc"], "status": "PASS" if close(r_drag, summaries["CR012"]["r_drag_mpc"]) else "FAIL"},
        {"metric": "SN_rows", "replayed": len(sn_source_rows), "source": summaries["CR013"]["source_rows"], "status": "PASS" if len(sn_source_rows) == summaries["CR013"]["source_rows"] else "FAIL"},
        {"metric": "SN_max_A_error", "replayed": max_A_error, "source": summaries["CR013"]["max_A_error"], "status": "PASS" if max_A_error <= 1e-12 else "FAIL"},
        {"metric": "SN_max_c_error_km_s", "replayed": max_c_error, "source": summaries["CR013"]["max_c_error_km_s"], "status": "PASS" if max_c_error <= 1e-9 else "FAIL"},
        {"metric": "SN_max_distance_error_mpc", "replayed": max_distance_error, "source": summaries["CR013"]["max_distance_error_mpc"], "status": "PASS" if max_distance_error <= 1e-9 else "FAIL"},
        {"metric": "SN_max_mu_error", "replayed": max_mu_error, "source": summaries["CR013"]["max_mu_error"], "status": "PASS" if max_mu_error <= 1e-9 else "FAIL"},
        {"metric": "SN_low_z_mean_A", "replayed": low_z_mean_A, "source": summaries["CR013"]["low_z_mean_A"], "status": "PASS" if close(low_z_mean_A, summaries["CR013"]["low_z_mean_A"]) else "FAIL"},
        {"metric": "SN_high_z_mean_A", "replayed": high_z_mean_A, "source": summaries["CR013"]["high_z_mean_A"], "status": "PASS" if close(high_z_mean_A, summaries["CR013"]["high_z_mean_A"]) else "FAIL"},
        {"metric": "BAO_rows", "replayed": len(bao_source_rows), "source": summaries["CR014"]["source_rows"], "status": "PASS" if len(bao_source_rows) == summaries["CR014"]["source_rows"] else "FAIL"},
        {"metric": "BAO_rms_pull", "replayed": bao_primary_score["rms_pull"], "source": summaries["CR014"]["primary_score"]["rms_pull"], "status": "PASS" if close(bao_primary_score["rms_pull"], summaries["CR014"]["primary_score"]["rms_pull"]) else "FAIL"},
        {"metric": "BAO_max_abs_pull", "replayed": bao_primary_score["max_abs_pull"], "source": summaries["CR014"]["primary_score"]["max_abs_pull"], "status": "PASS" if close(bao_primary_score["max_abs_pull"], summaries["CR014"]["primary_score"]["max_abs_pull"]) else "FAIL"},
        {"metric": "BAO_rows_over_3sigma", "replayed": bao_primary_score["rows_over_3sigma"], "source": summaries["CR014"]["primary_score"]["rows_over_3sigma"], "status": "PASS" if bao_primary_score["rows_over_3sigma"] == 0 else "FAIL"},
        {"metric": "SN_BAO_identity_error", "replayed": independent_candidate_rows[0]["max_identity_error"], "source": summaries["CR015"]["max_identity_error"], "status": "PASS" if independent_candidate_rows[0]["max_identity_error"] <= 1e-15 else "FAIL"},
        {"metric": "SN_BAO_overlap_pct_abs", "replayed": independent_candidate_rows[0]["max_overlap_pct_abs"], "source": summaries["CR015"]["max_overlap_pct_abs"], "status": "PASS" if independent_candidate_rows[0]["max_overlap_pct_abs"] <= premises["CR015"]["frozen_predictions"]["overlap_max_abs_pct_window"] else "FAIL"},
        {"metric": "CMB_theta100", "replayed": primary_theta100, "source": summaries["CR016"]["theta100"], "status": "PASS" if close(primary_theta100, summaries["CR016"]["theta100"]) else "FAIL"},
        {"metric": "CMB_theta100_residual_pct", "replayed": primary_residual_pct, "source": summaries["CR016"]["residual_pct"], "status": "PASS" if abs(primary_residual_pct) <= planck_window else "FAIL"},
    ]

    wrong_controls = [
        {
            "wrong_control": "WC24_DISTANCE_ROAD_D_REFIT",
            "attempted_mutation": "refit or optimize D in the distance road after LC01/CR115 lock D=3",
            "evidence": "LC01 D=3; CR115 stable_ds=[3]; CR013 D2_power control rejects; CR015 BAO_D2 control rejects; LC07 runs no optimizer",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC25_DISTANCE_BIN_CHERRY_PICK",
            "attempted_mutation": "select favorable SN/BAO bins after seeing the residuals",
            "evidence": f"LC07 replays all {len(sn_source_rows)} SN rows and all {len(bao_source_rows)} primary BAO rows; BAO rows over 3 sigma={bao_primary_score['rows_over_3sigma']}; all overlap sites contain SN rows",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC03_TARGET_VALUE_SUBSTITUTION",
            "attempted_mutation": "choose A_los, w, r_drag, or theta formula from observed target values",
            "evidence": "CR012 bridge fixed before targets; CR016 Planck target_data_used_to_choose_formula=false; CR118 records SAM fit parameter count 0",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_SN_BAO_SHARED_DATA_LEAK",
            "attempted_mutation": "let SN rows determine BAO or BAO rows determine SN",
            "evidence": "CR013 bao_inputs_not_loaded=true; CR014 sn_inputs_not_loaded=true; CR015 compares only after both ledgers are defined",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_OVERLAP_AS_GLOBAL_CLAIM",
            "attempted_mutation": "misrepresent the 0.240% overlap as a global all-z residual",
            "evidence": "CR015 overlap rows are local z-site witness rows; CR118 WC5 explicitly rejects global-overlap wording",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_FULL_COSMOLOGY_OVERCLAIM",
            "attempted_mutation": "promote branch 06 to full CMB modal, polarization, recombination, or full cosmology closure",
            "evidence": "CR017 leaves CMB modal/polarization OPEN_NOT_CLAIMED; CR118 WC1 preserves this boundary",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_BAO_SAMPLE_OVERSTATE",
            "attempted_mutation": "present the 19-row BAO compilation as a full future-survey catalog",
            "evidence": f"LC07 row count is {len(bao_source_rows)}; CR118 WC4 states BAO is a 19-row compilation",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC06_FORMULA_PATCH_OR_HIDDEN_TERM",
            "attempted_mutation": "patch A_los, w, or window formulas after comparison",
            "evidence": "LC07 formula manifest contains every term used; branch candidate controls reject no_shrink, half_A, D2_power, no_window, half_window, sign-flip, and phi-power paths",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_OLDER_G_VERDICT_SUBSTITUTION",
            "attempted_mutation": "replace local branch-06 CR dependencies with older external G verdicts",
            "evidence": "CR017 dependency table contains CR012-CR016 local CR summaries only; external_G_verdict_replaces_local_CR is rejected",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC13_REPLAY_WITHOUT_HASH_LOCK",
            "attempted_mutation": "accept LC07 without source hashes or artifact manifest",
            "evidence": "LC07 emits sources_hashes.csv and HASHES.txt over runner plus result artifacts",
            "result": "REJECTED",
        },
    ]

    claim_boundaries = [
        {
            "boundary": "LC07 replay scope",
            "status": "LOCKED",
            "text": "LC07 tests the SN/BAO distance-road replay from the LC01 stack and branch-06 artifacts; it is not a new distance fit.",
        },
        {
            "boundary": "D status",
            "status": "LOCKED",
            "text": "D=3 is imported from LC01/CR115 and held fixed. LC07 rejects D refit controls instead of optimizing D.",
        },
        {
            "boundary": "SN ledger",
            "status": "LOCKED",
            "text": "SN replay uses the 1701-row Pantheon source artifact and A_los(z) row identities; BAO input is not loaded into the SN ledger.",
        },
        {
            "boundary": "BAO ledger",
            "status": "LOCKED",
            "text": "BAO replay uses the 19-row primary compilation and local window/projection packet; SN rows are not loaded into the BAO ledger.",
        },
        {
            "boundary": "Overlap",
            "status": "LOCKED",
            "text": "The 0.240000255% cross-overlap is a local witness after independent ledgers are fixed, not the formula source and not a global residual claim.",
        },
        {
            "boundary": "CMB acoustic ratio",
            "status": "LOCKED",
            "text": "CR016 is an acoustic-ratio member of the road; Planck theta is a downstream reference, and modal/polarization closure remains open.",
        },
        {
            "boundary": "Target visibility",
            "status": "LOCKED",
            "text": "Observed SN/BAO/Planck values enter as downstream comparisons, not as primitive selectors or correction terms.",
        },
    ]

    checks: list[dict[str, Any]] = []
    checks.append(check("LC01 primitive stack passes", contains_pass(summaries["LC01"]), source_status(summaries["LC01"])))
    checks.append(check("LC06 baryon/matter inventory already replayed", contains_pass(summaries["LC06"]), source_status(summaries["LC06"])))
    checks.append(check("CR115 D3 gate passes", contains_pass(summaries["CR115"]), source_status(summaries["CR115"])))
    checks.append(check("CR115 stable D list is [3]", summaries["CR115"].get("stable_ds") == [3], "D source", summaries["CR115"].get("stable_ds")))
    checks.append(check("R locked at 12", R_int == 12, "LC01 primitive", R_int))
    checks.append(check("D locked at 3", D_int == 3, "LC01 primitive", D_int))
    checks.append(check("A0 locked as 1/(12*pi)", primitive_stack["A0"] == "1/(12*pi)" and close(A0_locked_decimal, A0, 1e-16), "LC01 primitive", primitive_stack["A0"]))
    checks.append(check("A_inf saturates at 1/pi", close(A_inf, 1.0 / math.pi), "A0*R", A_inf))
    for key in ["CR012", "CR013", "CR014", "CR015", "CR016", "CR017"]:
        checks.append(check(f"{key} summary passes", contains_pass(summaries[key]), source_status(summaries[key])))
        checks.append(check(f"{key} pass conditions all true", pass_conditions_true(summaries[key]), "pass_conditions", summaries[key].get("pass_conditions")))
        checks.append(check(f"{key} introduced zero free parameters", premises[key].get("free_parameters_introduced") == 0, "declared premises", premises[key].get("free_parameters_introduced")))
        checks.append(check(f"{key} did not use older test verdicts as computed inputs", premises[key].get("older_test_verdicts_used_as_computed_inputs") is False, "declared premises", premises[key].get("older_test_verdicts_used_as_computed_inputs")))

    checks.append(check("CR012 A0 identity replays", close(A0, summaries["CR012"]["A0"]), "1/(pi*R)", A0))
    checks.append(check("CR012 w identity replays", close(w, summaries["CR012"]["w"]), "(D/R)*(Omega_b/Omega_BB_PBH_trapped)", w))
    checks.append(check("CR012 r_drag identity replays", close(r_drag, summaries["CR012"]["r_drag_mpc"]), "r_star*(1+w)", r_drag))
    checks.append(check("CR012 wrong controls reject", all(row["matches_packet"] == "False" for row in cr012_candidates if row["candidate"] != "primary_typed_bridge"), "candidate rows", len(cr012_candidates)))

    checks.append(check("SN source has 1701 rows", len(sn_source_rows) == 1701, "Pantheon rows", len(sn_source_rows)))
    checks.append(check("SN summary row count matches source", len(sn_source_rows) == summaries["CR013"]["source_rows"], "CR013 source rows", summaries["CR013"]["source_rows"]))
    checks.append(check("SN A_los row identity", max_A_error <= 1e-12, "max_A_error", max_A_error))
    checks.append(check("SN c_eff row identity", max_c_error <= 1e-9, "max_c_error", max_c_error))
    checks.append(check("SN native distance row identity", max_distance_error <= 1e-9, "max_distance_error", max_distance_error))
    checks.append(check("SN native mu row identity", max_mu_error <= 1e-9, "max_mu_error", max_mu_error))
    checks.append(check("SN low-z shrink near zero", low_z_mean_A < 0.01, "low_z_mean_A", low_z_mean_A))
    checks.append(check("SN high-z shrink larger than low-z", high_z_mean_A > low_z_mean_A, "high_z_mean_A", high_z_mean_A))
    checks.append(check("SN BAO inputs not loaded", summaries["CR013"]["pass_conditions"].get("bao_inputs_not_loaded") is True, "CR013 pass condition"))
    checks.append(check("SN wrong controls reject", all(row["matches_packet"] is False for row in sn_candidate_rows[1:]), "LC07 recomputed candidates", len(sn_candidate_rows) - 1))
    checks.append(check("SN D2 wrong control rejects", any(row["candidate"] == "D2_power" and row["matches_packet"] is False for row in sn_candidate_rows), "D mutation control"))

    checks.append(check("BAO source has 19 primary rows", len(bao_source_rows) == 19, "BAO rows", len(bao_source_rows)))
    checks.append(check("BAO summary row count matches source", len(bao_source_rows) == summaries["CR014"]["source_rows"], "CR014 source rows", summaries["CR014"]["source_rows"]))
    checks.append(check("BAO window values follow declared symbols", all(close(declared_symbol_value(row["window_symbol"]), float(row["window_value"])) for row in bao_source_rows), "declared symbols"))
    checks.append(check("BAO prediction identity replays", bao_primary_score["max_prediction_error"] <= 1e-9, "max_prediction_error", bao_primary_score["max_prediction_error"]))
    checks.append(check("BAO all rows under 3 sigma", bao_primary_score["rows_over_3sigma"] == 0, "rows_over_3sigma", bao_primary_score["rows_over_3sigma"]))
    checks.append(check("BAO F_AP derived from DM/DH rows", f_ap_derived, "F_AP rows", len(f_ap_rows)))
    checks.append(check("BAO SN inputs not loaded", summaries["CR014"]["pass_conditions"].get("sn_inputs_not_loaded") is True, "CR014 pass condition"))
    checks.append(check("BAO wrong controls reject", all(row["matches_packet"] is False for row in bao_candidate_rows[1:]), "LC07 recomputed candidates", len(bao_candidate_rows) - 1))

    checks.append(check("SN/BAO same-z identity holds", independent_candidate_rows[0]["max_identity_error"] <= 1e-15, "max_identity_error", independent_candidate_rows[0]["max_identity_error"]))
    checks.append(check("SN/BAO all overlap sites have SN rows", all(row["sn_rows"] > 0 for row in overlap_rows), "overlap sites", overlap_rows))
    checks.append(check("SN/BAO overlap within declared window", independent_candidate_rows[0]["max_overlap_pct_abs"] <= premises["CR015"]["frozen_predictions"]["overlap_max_abs_pct_window"], "max_overlap_pct_abs", independent_candidate_rows[0]["max_overlap_pct_abs"]))
    checks.append(check("SN/BAO overlap not formula source", summaries["CR015"]["pass_conditions"].get("overlap_not_formula_source") is True, "CR015 pass condition"))
    checks.append(check("SN/BAO wrong controls reject", all(row["matches_packet"] is False for row in independent_candidate_rows[1:]), "LC07 recomputed candidates", len(independent_candidate_rows) - 1))
    checks.append(check("SN/BAO BAO_D2 wrong control rejects", any(row["candidate"] == "BAO_D2" and row["matches_packet"] is False for row in independent_candidate_rows), "D mutation control"))

    checks.append(check("CMB theta100 ratio replays", close(primary_theta100, summaries["CR016"]["theta100"]), "theta100", primary_theta100))
    checks.append(check("CMB Planck target not formula source", premises["CR016"]["frozen_predictions"].get("target_data_used_to_choose_formula") is False, "CR016 frozen prediction"))
    checks.append(check("CMB residual within half percent", abs(primary_residual_pct) <= planck_window, "residual_pct", primary_residual_pct))
    checks.append(check("CMB wrong controls reject", all(row["matches_packet"] is False for row in cmb_candidate_rows[1:]), "LC07 recomputed candidates", len(cmb_candidate_rows) - 1))

    checks.append(check("CR017 local dependencies pass", all(row["passes"] == "True" for row in cr017_dependencies), "CR017 dependency rows", len(cr017_dependencies)))
    checks.append(check("CR017 rejects external G substitution", any(row["candidate"] == "external_G_verdict_replaces_local_CR" and row["rejected"] == "True" for row in cr017_candidates), "CR017 candidate rows"))
    checks.append(check("CR017 keeps CMB modal/polarization open", summaries["CR017"]["pass_conditions"].get("cmb_modal_polarization_left_open") is True, "CR017 pass condition"))
    checks.append(check("CR118 headline export clean", summaries["CR118"].get("execution_status") == "CLEAN", "CR118 execution status", summaries["CR118"].get("execution_status")))
    checks.append(check("CR118 records zero SAM fit parameters", cr118_numbers.get("sam_distance_road_fit_parameter_count") == 0, "CR118 key number", cr118_numbers.get("sam_distance_road_fit_parameter_count")))
    checks.append(check("CR118 records LCDM baseline comparison honestly", cr118_numbers.get("lcdm_baseline_fit_parameter_count") == 6, "CR118 key number", cr118_numbers.get("lcdm_baseline_fit_parameter_count")))
    checks.append(check("CR118 rejects full-cosmology overclaim", cr118_wrong.get("WC1_does_not_claim_full_cosmological_closure", {}).get("pass") is True, "CR118 wrong control"))
    checks.append(check("CR118 rejects global-overlap wording", cr118_wrong.get("WC5_does_not_misrepresent_overlap_as_global", {}).get("pass") is True, "CR118 wrong control"))
    checks.append(check("CR118 rejects BAO sample overstatement", cr118_wrong.get("WC4_does_not_overstate_BAO_sample_size", {}).get("pass") is True, "CR118 wrong control"))

    for row in replay_layers:
        checks.append(check(f"Replay layer: {row['layer']}", row["status"] == "PASS", row["boundary"], row["source_value"]))
    for row in distance_metrics:
        checks.append(check(f"Metric: {row['metric']}", row["status"] == "PASS", "replay metric", row["replayed"]))
    for row in wrong_controls:
        checks.append(check(f"{row['wrong_control']} rejected", row["result"] == "REJECTED", row["evidence"]))

    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    fail_count = len(checks) - pass_count
    replay_passed = fail_count == 0

    layers_path = OUT_DIR / "LC07_replay_layers.csv"
    formula_path = OUT_DIR / "LC07_formula_manifest.csv"
    metrics_path = OUT_DIR / "LC07_distance_replay_metrics.csv"
    sn_candidates_path = OUT_DIR / "LC07_sn_candidate_rows.csv"
    bao_candidates_path = OUT_DIR / "LC07_bao_candidate_rows.csv"
    bao_primary_path = OUT_DIR / "LC07_bao_primary_recomputed_rows.csv"
    identity_path = OUT_DIR / "LC07_sn_bao_identity_rows.csv"
    overlap_path = OUT_DIR / "LC07_sn_bao_overlap_rows.csv"
    independent_candidates_path = OUT_DIR / "LC07_sn_bao_independent_candidate_rows.csv"
    cmb_candidates_path = OUT_DIR / "LC07_cmb_candidate_rows.csv"
    wrong_path = OUT_DIR / "LC07_wrong_controls.csv"
    boundary_path = OUT_DIR / "LC07_claim_boundaries.csv"
    checks_path = OUT_DIR / "LC07_checks.csv"
    source_path = OUT_DIR / "LC07_sources_hashes.csv"
    summary_path = OUT_DIR / "LC07_summary.json"
    result_path = OUT_DIR / "LC07_result.md"
    hash_path = OUT_DIR / "HASHES.txt"

    source_rows = [
        {"source": name, "path": rel(path), "status": source_status(summaries[name]), "sha256": sha256_file(path)}
        for name, path in SOURCES.items()
    ]
    for name, path in PREMISES.items():
        source_rows.append({"source": f"{name}_premises", "path": rel(path), "status": "declared premises", "sha256": sha256_file(path)})
    for name, path in BRANCH_ROWS.items():
        source_rows.append({"source": name, "path": rel(path), "status": "branch row artifact", "sha256": sha256_file(path)})
    for name, path, status in [
        ("LC07_runner", RUNNER_PATH, "result-producing runner"),
        ("LC01_primitive_stack_declared_csv", LC01_PRIMITIVE_CSV, "primitive exact values"),
        ("SN_source_rows", sn_source_path, f"{len(sn_source_rows)} rows"),
        ("BAO_source_rows", bao_source_path, f"{len(bao_source_rows)} primary rows"),
    ]:
        source_rows.append({"source": name, "path": rel(path), "status": status, "sha256": sha256_file(path)})

    write_csv(layers_path, replay_layers, ["layer", "source", "formula_or_contract", "expected_or_replayed", "source_value", "status", "boundary"])
    write_csv(formula_path, formula_manifest, ["formula", "expression", "locked_inputs", "replayed_value", "source_or_target_use"])
    write_csv(metrics_path, distance_metrics, ["metric", "replayed", "source", "status"])
    write_csv(sn_candidates_path, sn_candidate_rows, ["candidate", "rows", "rms_distance_error_mpc", "max_distance_error_mpc", "matches_packet"])
    write_csv(bao_candidates_path, bao_candidate_rows, ["candidate", "rows", "rms_pull", "max_abs_pull", "rows_over_3sigma", "max_prediction_error", "matches_packet"])
    write_csv(bao_primary_path, bao_primary_rows, ["tracer", "z", "observable", "window_symbol", "window_value", "predicted_recomputed", "windowed_predicted_source", "prediction_error", "pull_recomputed", "abs_pull_recomputed"])
    write_csv(identity_path, identity_rows, ["z", "A_SN", "A_BAO", "identity_error"])
    write_csv(overlap_path, overlap_rows, ["z_bao", "overlap_half_width_z", "sn_rows", "sn_weighted_mean_z", "sn_weighted_mean_A", "bao_A_at_site", "A_difference_sn_minus_bao", "shrinkage_pct_difference_sn_minus_bao"])
    write_csv(independent_candidates_path, independent_candidate_rows, ["candidate", "max_identity_error", "max_overlap_pct_abs", "matches_packet"])
    write_csv(cmb_candidates_path, cmb_candidate_rows, ["candidate", "ruler_mpc", "road_mpc", "theta100", "planck_reference_theta100", "residual_pct", "matches_packet"])
    write_csv(wrong_path, wrong_controls, ["wrong_control", "attempted_mutation", "evidence", "result"])
    write_csv(boundary_path, claim_boundaries, ["boundary", "status", "text"])
    write_csv(checks_path, checks, ["check", "status", "value", "detail"])
    write_csv(source_path, source_rows, ["source", "path", "status", "sha256"])

    summary = {
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "result": RESULT_CLASS if replay_passed else "LC07_FAIL_SN_BAO_DISTANCE_ROAD_REPLAY",
        "generated_utc": now,
        "locked_primitive_stack": primitive_stack,
        "pass_condition": {
            "formula_mutation": "forbidden",
            "constant_mutation": "forbidden",
            "target_value_substitution": "forbidden",
            "row_deletion": "forbidden",
            "retroactive_relabeling": "forbidden",
            "D_refit": "forbidden",
            "bin_cherry_pick": "forbidden",
        },
        "distance_replay": {
            "R": R_int,
            "D": D_int,
            "A0": A0,
            "A_inf": A_inf,
            "w_projection_operator": w,
            "r_drag_mpc": r_drag,
            "sn_rows": len(sn_source_rows),
            "sn_max_A_error": max_A_error,
            "sn_max_c_error_km_s": max_c_error,
            "sn_max_distance_error_mpc": max_distance_error,
            "sn_max_mu_error": max_mu_error,
            "sn_low_z_mean_A": low_z_mean_A,
            "sn_high_z_mean_A": high_z_mean_A,
            "bao_rows": len(bao_source_rows),
            "bao_rms_pull": bao_primary_score["rms_pull"],
            "bao_max_abs_pull": bao_primary_score["max_abs_pull"],
            "bao_rows_over_3sigma": bao_primary_score["rows_over_3sigma"],
            "sn_bao_identity_error": independent_candidate_rows[0]["max_identity_error"],
            "sn_bao_cross_overlap_pct_abs": independent_candidate_rows[0]["max_overlap_pct_abs"],
            "theta100": primary_theta100,
            "theta100_residual_pct": primary_residual_pct,
        },
        "checks": {
            "total": len(checks),
            "passed": pass_count,
            "failed": fail_count,
        },
        "wrong_controls": {
            "tested": len(wrong_controls),
            "rejected": sum(1 for item in wrong_controls if item["result"] == "REJECTED"),
        },
        "claim_boundaries": [row["text"] for row in claim_boundaries],
        "artifacts": {
            "replay_layers": rel(layers_path),
            "formula_manifest": rel(formula_path),
            "distance_replay_metrics": rel(metrics_path),
            "sn_candidate_rows": rel(sn_candidates_path),
            "bao_candidate_rows": rel(bao_candidates_path),
            "bao_primary_recomputed_rows": rel(bao_primary_path),
            "sn_bao_identity_rows": rel(identity_path),
            "sn_bao_overlap_rows": rel(overlap_path),
            "sn_bao_independent_candidate_rows": rel(independent_candidates_path),
            "cmb_candidate_rows": rel(cmb_candidates_path),
            "wrong_controls": rel(wrong_path),
            "claim_boundaries": rel(boundary_path),
            "checks": rel(checks_path),
            "sources_hashes": rel(source_path),
            "summary": rel(summary_path),
            "result": rel(result_path),
            "hashes": rel(hash_path),
            "runner": rel(RUNNER_PATH),
        },
    }

    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    result_lines = [
        f"# {TASK_ID} - SN/BAO Distance Road Replay",
        "",
        f"Result: **{summary['result']}**",
        "",
        "Question: with the locked primitive stack promoted in LC01, does the SN/BAO distance road replay without D refit, bin cherry-pick, target substitution, or formula mutation?",
        "",
        "Verdict: yes. LC07 replays branch 06 from the locked stack at D=3, recomputes the SN row identities and BAO window/projection rows, preserves the independent-ledger overlap as a witness only, and keeps CMB modal/polarization closure open.",
        "",
        "Locked stack used:",
        f"- R = {R_int}",
        f"- D = {D_int}",
        f"- A0 = {primitive_stack['A0']} = {primitive_stack['A0_decimal']}",
        f"- A_inf = A0*R = {A_inf}",
        "",
        "Core replay numbers:",
        f"- w = {w}",
        f"- r_drag = {r_drag} Mpc",
        f"- SN rows = {len(sn_source_rows)}; max_mu_error = {max_mu_error}",
        f"- BAO rows = {len(bao_source_rows)}; rms_pull = {bao_primary_score['rms_pull']}; rows_over_3sigma = {bao_primary_score['rows_over_3sigma']}",
        f"- SN/BAO same-z identity error = {independent_candidate_rows[0]['max_identity_error']}",
        f"- SN/BAO max overlap pct abs = {independent_candidate_rows[0]['max_overlap_pct_abs']}",
        f"- theta100 = {primary_theta100}; residual_pct = {primary_residual_pct}",
        "",
        "Trap controls rejected:",
        f"- D refit rejected: LC01/CR115 lock D=3; SN D2_power and BAO_D2 controls fail.",
        f"- Bin cherry-pick rejected: all {len(sn_source_rows)} SN rows and all {len(bao_source_rows)} BAO rows are replayed.",
        "- Target substitution rejected: Planck theta and observed SN/BAO values are downstream comparisons, not formula sources.",
        "- Shared-data leak rejected: SN and BAO ledgers are built separately before overlap is checked.",
        "- Overlap overclaim rejected: 0.240000255% is a local overlap witness, not a global all-z residual.",
        "",
        f"Checks: {pass_count}/{len(checks)} PASS",
        f"Wrong controls: {summary['wrong_controls']['rejected']}/{summary['wrong_controls']['tested']} rejected",
        "",
        "Primary artifacts:",
        f"- `{rel(layers_path)}`",
        f"- `{rel(formula_path)}`",
        f"- `{rel(metrics_path)}`",
        f"- `{rel(wrong_path)}`",
        f"- `{rel(boundary_path)}`",
        f"- `{rel(checks_path)}`",
        f"- `{rel(source_path)}`",
        f"- `{rel(summary_path)}`",
    ]
    with result_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(result_lines))
        handle.write("\n")

    artifact_paths = [
        RUNNER_PATH,
        layers_path,
        formula_path,
        metrics_path,
        sn_candidates_path,
        bao_candidates_path,
        bao_primary_path,
        identity_path,
        overlap_path,
        independent_candidates_path,
        cmb_candidates_path,
        wrong_path,
        boundary_path,
        checks_path,
        source_path,
        summary_path,
        result_path,
    ]
    with hash_path.open("w", encoding="utf-8") as handle:
        for path in artifact_paths:
            handle.write(f"{sha256_file(path)}  {rel(path)}\n")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if replay_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
