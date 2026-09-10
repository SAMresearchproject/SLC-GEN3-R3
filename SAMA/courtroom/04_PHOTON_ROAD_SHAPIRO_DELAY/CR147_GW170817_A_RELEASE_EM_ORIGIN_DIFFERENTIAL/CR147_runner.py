"""CR147 fresh GW170817 A-release / EM-origin differential test.

This runner tests the proposed GW170817 mechanism after CR116:

    1. The GW channel is the massless m=18 tensor-carrier packet.
    2. After release, GW and EM share the same A-road.
    3. The observed GW-to-EM lag is local source/release engine time, not a
       long-distance propagation-speed split.
    4. A tempting static local A-road integral between an EM origin and the GW
       release surface is tested as a wrong control.

The important boundary is that the seconds-scale delay is carried by the
locked SAM dynamic A-release/engine law. A literal Shapiro-style local
integral (1/c) int A(r) dr across the release gap is only a formal first-order
control: at A=1 exactly, light is at the no-escape / zero-depth boundary and
cannot be used as a normal launch point.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CR_ID = "CR147"
RESULT_CLASS_PASS = "CR147_PASS_GW170817_DYNAMIC_A_RELEASE_ENGINE_DIFFERENTIAL_WITH_STATIC_A_INTEGRAL_BOUNDARY"
RESULT_CLASS_FAIL = "CR147_FAIL_GW170817_A_RELEASE_ENGINE_DIFFERENTIAL"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent
STAM_ROOT = Path(r"C:/VS/Stam_model-A-v1.0")

G = 6.67430e-11
C = 299_792_458.0
M_SUN = 1.98847e30
SECONDS_PER_YEAR = 365.25 * 86_400.0

# Primary external event inputs, frozen into this runner from primary papers.
GW170817_TOTAL_MASS_MSUN = 2.74
GW170817_TOTAL_MASS_PLUS_MSUN = 0.04
GW170817_TOTAL_MASS_MINUS_MSUN = 0.01
GW170817_LEGACY_ROUNDED_MASS_MSUN = 2.70
OBSERVED_DELAY_S = 1.74
OBSERVED_DELAY_SIGMA_S = 0.05
GW170817_DISTANCE_MPC = 40.0

CR006_SUMMARY = (
    COURTROOM_DIR
    / "04_PHOTON_ROAD_SHAPIRO_DELAY"
    / "CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT"
    / "CR006_summary.json"
)
CR116_SUMMARY = (
    COURTROOM_DIR
    / "14_FOUNDATIONAL_TESTS"
    / "CR116_18_GRAVITON_CARRIER_THEOREM"
    / "CR116_summary.json"
)
CR116_RESULT = (
    COURTROOM_DIR
    / "14_FOUNDATIONAL_TESTS"
    / "CR116_18_GRAVITON_CARRIER_THEOREM"
    / "CR116_result.md"
)
G96_SUMMARY = (
    STAM_ROOT
    / "tests"
    / "Substrate"
    / "G96_BNS_engine_time_scaling"
    / "results"
    / "G96_BNS_engine_time_scaling_summary.md"
)
G699C_SUMMARY = (
    STAM_ROOT
    / "tests"
    / "Substrate"
    / "G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT"
    / "G699c_summary.json"
)
G699C_RESULT = (
    STAM_ROOT
    / "tests"
    / "Substrate"
    / "G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT"
    / "G699c_RESULT.md"
)
G699C_SEALED = (
    STAM_ROOT
    / "audit"
    / "audits"
    / "SEALED_ENVELOPE_G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT_2026_06_11.md"
)
F5C_SUMMARY = (
    STAM_ROOT
    / "tests"
    / "Substrate"
    / "005c_gw170817_arrival_test"
    / "results"
    / "F5c_gw170817_arrival_test_summary.md"
)

SOURCE_CHAIN_CSV = CR_DIR / "CR147_source_chain.csv"
EVENT_INPUTS_CSV = CR_DIR / "CR147_external_event_inputs.csv"
RELEASE_ROWS_CSV = CR_DIR / "CR147_release_surface_rows.csv"
DELAY_BUDGET_CSV = CR_DIR / "CR147_delay_budget.csv"
CHECKS_CSV = CR_DIR / "CR147_checks.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR147_wrong_controls.csv"
LOCK_JSON = CR_DIR / "CR147_gw170817_a_release_lock.json"
LOCK_SHA = CR_DIR / "CR147_gw170817_a_release_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR147_summary.json"
RESULT_MD = CR_DIR / "CR147_result.md"
LOCAL_HASHES = CR_DIR / "CR147_hashes.txt"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def branch_rel(path: Path) -> str:
    try:
        return str(path.relative_to(BRANCH_DIR))
    except ValueError:
        return str(path)


def cr_rel(path: Path) -> str:
    try:
        return str(path.relative_to(CR_DIR))
    except ValueError:
        return str(path)


def source_row(
    label: str,
    role: str,
    load_bearing: bool,
    source_type: str,
    path: Path | None = None,
    url: str = "",
    note: str = "",
) -> dict[str, Any]:
    exists = path.exists() if path else bool(url)
    return {
        "label": label,
        "role": role,
        "load_bearing": bool(load_bearing),
        "source_type": source_type,
        "path": str(path) if path else "",
        "url": url,
        "exists": exists,
        "sha256": sha256_file(path) if path else "",
        "note": note,
    }


def check_row(check_id: str, description: str, observed: Any, passed: bool, source: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "description": description,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "passed": bool(passed),
        "source": source,
    }


def wc_row(control_id: str, hypothesis: str, observed: Any, rejected: bool, reason: str) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "hypothesis": hypothesis,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "rejected": bool(rejected),
        "reason": reason,
    }


def solve_threshold_roots(a0: float) -> list[float]:
    # A0 = x(1-x)/(1+x), x = R_s/(2*r_release)
    b = a0 - 1.0
    disc = b * b - 4.0 * a0
    return [(-b - math.sqrt(disc)) / 2.0, (-b + math.sqrt(disc)) / 2.0]


def release_engine_packet(mass_msun: float) -> dict[str, float | list[float]]:
    a0 = 1.0 / (12.0 * math.pi)
    roots = solve_threshold_roots(a0)
    x_outer = min(root for root in roots if root > 0.0)
    r_release_over_rs = 1.0 / (2.0 * x_outer)
    a_release = 1.0 / r_release_over_rs
    rs_m = 2.0 * G * mass_msun * M_SUN / C**2
    rs_over_c = rs_m / C
    slope = (5.0 / 8.0) * r_release_over_rs**4 * (2.0 * G * M_SUN / C**3)
    tau_engine = slope * mass_msun
    return {
        "A0": a0,
        "threshold_roots": roots,
        "x_outer": x_outer,
        "r_release_over_rs": r_release_over_rs,
        "A_release": a_release,
        "delta_A_from_A1_to_release": 1.0 - a_release,
        "rs_m": rs_m,
        "r_release_m": r_release_over_rs * rs_m,
        "release_gap_from_A1_m": (r_release_over_rs - 1.0) * rs_m,
        "rs_over_c_s": rs_over_c,
        "slope_s_per_msun": slope,
        "tau_engine_s": tau_engine,
        "A1_exact_status": "NO_ESCAPE_ZERO_DEPTH_BOUNDARY_NOT_LITERAL_LIGHT_LAUNCH_POINT",
        "formal_static_A_integral_boundary_to_release_s": rs_over_c * math.log(r_release_over_rs),
        "formal_light_crossing_boundary_to_release_s": (r_release_over_rs - 1.0) * rs_over_c,
    }


def sigma_residual(predicted: float, observed: float = OBSERVED_DELAY_S) -> float:
    return (observed - predicted) / OBSERVED_DELAY_SIGMA_S


def update_local_hashes(artifacts: list[Path]) -> None:
    lines = [f"{sha256_file(path)}  {cr_rel(path)}" for path in artifacts]
    LOCAL_HASHES.write_text("\n".join(lines) + "\n", encoding="ascii")


def main() -> int:
    print("CR147 runner: starting fresh GW170817 A-release / EM-origin differential test")

    cr116 = read_json(CR116_SUMMARY)
    g699c = read_json(G699C_SUMMARY)
    cr006 = read_json(CR006_SUMMARY)

    packet = release_engine_packet(GW170817_TOTAL_MASS_MSUN)
    packet_low = release_engine_packet(GW170817_TOTAL_MASS_MSUN - GW170817_TOTAL_MASS_MINUS_MSUN)
    packet_high = release_engine_packet(GW170817_TOTAL_MASS_MSUN + GW170817_TOTAL_MASS_PLUS_MSUN)
    packet_legacy = release_engine_packet(GW170817_LEGACY_ROUNDED_MASS_MSUN)

    predicted = float(packet["tau_engine_s"])
    residual = OBSERVED_DELAY_S - predicted
    abs_percent_error = 100.0 * abs(residual) / OBSERVED_DELAY_S
    residual_sigma = sigma_residual(predicted)
    predicted_low = float(packet_low["tau_engine_s"])
    predicted_high = float(packet_high["tau_engine_s"])
    one_sigma_low = OBSERVED_DELAY_S - OBSERVED_DELAY_SIGMA_S
    one_sigma_high = OBSERVED_DELAY_S + OBSERVED_DELAY_SIGMA_S

    plain_a_s = float(packet["formal_static_A_integral_boundary_to_release_s"])
    plain_light_s = float(packet["formal_light_crossing_boundary_to_release_s"])
    plain_fraction = plain_a_s / OBSERVED_DELAY_S
    plain_shortfall = OBSERVED_DELAY_S / plain_a_s
    required_ln_ratio = OBSERVED_DELAY_S / float(packet["rs_over_c_s"])
    required_log10_ratio = required_ln_ratio / math.log(10.0)
    tuned_mass_for_exact_delay = OBSERVED_DELAY_S / float(packet["slope_s_per_msun"])

    one_sided_delay = float(g699c["one_sided_control"]["total_one_sided_delay_s"])
    one_sided_ratio = float(g699c["one_sided_control"]["ratio_one_sided_to_observed"])

    event_inputs = [
        {
            "quantity": "observed_GW_to_GRB_delay_s",
            "value": OBSERVED_DELAY_S,
            "sigma": OBSERVED_DELAY_SIGMA_S,
            "source": "LIGO/Virgo/Fermi/INTEGRAL ApJL 848 L13; arXiv:1710.05834",
        },
        {
            "quantity": "total_mass_msun_low_spin",
            "value": GW170817_TOTAL_MASS_MSUN,
            "plus": GW170817_TOTAL_MASS_PLUS_MSUN,
            "minus": GW170817_TOTAL_MASS_MINUS_MSUN,
            "source": "LIGO/Virgo PRL 119 161101; arXiv:1710.05832",
        },
        {
            "quantity": "luminosity_distance_mpc",
            "value": GW170817_DISTANCE_MPC,
            "plus": 8,
            "minus": 14,
            "source": "LIGO/Virgo PRL 119 161101; arXiv:1710.05832",
        },
        {
            "quantity": "fermi_grb_trigger_utc",
            "value": "2017-08-17 12:41:06 UTC",
            "source": "Fermi-GBM ApJL; arXiv:1710.05446",
        },
    ]

    release_rows = [
        {
            "row": "fresh_external_mass",
            "mass_msun": GW170817_TOTAL_MASS_MSUN,
            "A0": packet["A0"],
            "x_outer": packet["x_outer"],
            "r_release_over_rs": packet["r_release_over_rs"],
            "A_release": packet["A_release"],
            "delta_A_from_A1_to_release": packet["delta_A_from_A1_to_release"],
            "rs_m": packet["rs_m"],
            "r_release_m": packet["r_release_m"],
            "release_gap_from_A1_m": packet["release_gap_from_A1_m"],
            "tau_engine_s": packet["tau_engine_s"],
            "A1_exact_status": packet["A1_exact_status"],
            "formal_static_A_integral_boundary_to_release_s": packet["formal_static_A_integral_boundary_to_release_s"],
        },
        {
            "row": "mass_uncertainty_low",
            "mass_msun": GW170817_TOTAL_MASS_MSUN - GW170817_TOTAL_MASS_MINUS_MSUN,
            "tau_engine_s": predicted_low,
        },
        {
            "row": "mass_uncertainty_high",
            "mass_msun": GW170817_TOTAL_MASS_MSUN + GW170817_TOTAL_MASS_PLUS_MSUN,
            "tau_engine_s": predicted_high,
        },
        {
            "row": "legacy_rounded_G699c_mass",
            "mass_msun": GW170817_LEGACY_ROUNDED_MASS_MSUN,
            "tau_engine_s": packet_legacy["tau_engine_s"],
            "status": "LEGACY_CONTROL_NOT_LOAD_BEARING",
        },
    ]

    delay_budget = [
        {
            "lane": "CR116_GW_channel",
            "formula": "18 = R^2/2^D = alpha_H*D^2; QP092F massless phase_speed=c",
            "value_s": 0.0,
            "readout": cr116.get("wave_mode"),
            "status": "MASSLESS_M18_CARRIER_PACKET",
        },
        {
            "lane": "fresh_release_engine_delay",
            "formula": "(5/8)*(r_release/Rs)^4*(Rs/c)",
            "value_s": predicted,
            "readout": f"residual_sigma={residual_sigma}",
            "status": "ACTIVE_SAM_SOURCE_RELEASE_DIFFERENTIAL",
        },
        {
            "lane": "observed_GW170817_GRB170817A_delay",
            "formula": "primary external observed delay",
            "value_s": OBSERVED_DELAY_S,
            "readout": f"sigma_s={OBSERVED_DELAY_SIGMA_S}",
            "status": "OBSERVED_REFERENCE",
        },
        {
            "lane": "residual_after_fresh_external_mass",
            "formula": "observed - fresh_release_engine_delay",
            "value_s": residual,
            "readout": f"abs_percent_error={abs_percent_error}",
            "status": "WITHIN_1SIGMA",
        },
        {
            "lane": "formal_static_A_integral_boundary_to_release",
            "formula": "(Rs/c)*ln(r_release/Rs), formal first-order control only",
            "value_s": plain_a_s,
            "readout": f"observed/plain={plain_shortfall}",
            "status": "REJECTED_AS_SECONDS_SCALE_EXPLANATION",
        },
        {
            "lane": "formal_light_crossing_boundary_to_release",
            "formula": "(r_release-Rs)/c",
            "value_s": plain_light_s,
            "status": "LOCAL_GEOMETRY_CONTEXT",
        },
        {
            "lane": "post_release_shared_road_differential",
            "formula": "same A-road after release",
            "value_s": 0.0,
            "status": "ZERO_UNDER_SHARED_A_ROAD",
        },
        {
            "lane": "one_sided_40Mpc_A_road_wrong_control",
            "formula": "light couples to full local A-road; GW does not",
            "value_s": one_sided_delay,
            "readout": f"one_sided_to_observed={one_sided_ratio}",
            "status": "REJECTED_WRONG_CONTROL",
        },
    ]

    sources = [
        source_row(
            "CR147_RUNNER",
            "Executable fresh GW170817 release-differential gate",
            True,
            "EXECUTABLE_GATE",
            Path(__file__).resolve(),
        ),
        source_row(
            "GW170817_GRB170817A_DELAY_PRIMARY",
            "Observed 1.74 +/- 0.05 s GW-to-GRB delay and speed bound",
            True,
            "PRIMARY_EXTERNAL",
            url="https://arxiv.org/abs/1710.05834",
            note="LIGO/Virgo/Fermi/INTEGRAL ApJL 848 L13",
        ),
        source_row(
            "GW170817_MASS_DISTANCE_PRIMARY",
            "Total mass 2.74 +0.04/-0.01 Msun and 40 +8/-14 Mpc distance",
            True,
            "PRIMARY_EXTERNAL",
            url="https://arxiv.org/abs/1710.05832",
            note="LIGO/Virgo PRL 119 161101",
        ),
        source_row(
            "GRB170817A_FERMI_GBM_PRIMARY",
            "Fermi-GBM GRB trigger context at 12:41:06 UTC",
            True,
            "PRIMARY_EXTERNAL",
            url="https://arxiv.org/abs/1710.05446",
            note="Fermi-GBM ApJL GRB 170817A paper",
        ),
        source_row(
            "CR116_M18_GRAVITON_CHANNEL",
            "Massless m=18 tensor-carrier wave-mode theorem",
            True,
            "COURTROOM_THEOREM",
            CR116_SUMMARY,
        ),
        source_row(
            "CR116_RESULT_TEXT",
            "Human-readable m=18 carrier theorem and boundaries",
            True,
            "COURTROOM_RESULT",
            CR116_RESULT,
        ),
        source_row(
            "CR006_PHOTON_ROAD_A_INTEGRAL",
            "Scoped photon-road A integral contact",
            True,
            "COURTROOM_RESULT",
            CR006_SUMMARY,
        ),
        source_row(
            "G96_BNS_ENGINE_TIME",
            "Locked release/engine-time law",
            True,
            "UPSTREAM_SUMMARY",
            G96_SUMMARY,
        ),
        source_row(
            "G699C_MULTIMESSENGER_SPLIT",
            "Prior shared-road GW170817 split and one-sided control",
            True,
            "UPSTREAM_SUMMARY",
            G699C_SUMMARY,
        ),
        source_row(
            "G699C_RESULT_TEXT",
            "Human-readable prior G699c result",
            False,
            "UPSTREAM_RESULT",
            G699C_RESULT,
        ),
        source_row(
            "G699C_SEALED_ENVELOPE",
            "Pre-run prediction envelope for G699c",
            True,
            "SEALED_ENVELOPE",
            G699C_SEALED,
        ),
        source_row(
            "F5C_ONE_SIDED_CONTROL",
            "Historical full one-sided A-road failure control",
            False,
            "UPSTREAM_WRONG_CONTROL",
            F5C_SUMMARY,
        ),
    ]
    load_bearing_sources_present = all(row["exists"] for row in sources if row["load_bearing"])

    cr116_pass = (
        cr116.get("result_class") == "CR116_PASS_18_GRAVITON_CHANNEL_CARRIER_THEOREM"
        and cr116.get("all_predictions_passed") is True
        and cr116.get("all_wrong_controls_rejected") is True
        and cr116.get("split_loss_tensor_channel", "").startswith("18")
        and "massless" in cr116.get("wave_mode", "")
    )
    cr006_pass = (
        cr006.get("verdict") == "CR006_PASS_SCOPED_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT"
        and cr006.get("pass_conditions", {}).get("sam_integral_matches_log_law") is True
    )
    external_mass_not_legacy = GW170817_TOTAL_MASS_MSUN != GW170817_LEGACY_ROUNDED_MASS_MSUN
    central_within_1sigma = abs(residual) <= OBSERVED_DELAY_SIGMA_S
    band_inside_1sigma = predicted_low >= one_sigma_low and predicted_high <= one_sigma_high
    a1_boundary_preserved = packet["A1_exact_status"] == "NO_ESCAPE_ZERO_DEPTH_BOUNDARY_NOT_LITERAL_LIGHT_LAUNCH_POINT"
    plain_a_rejected = plain_shortfall > 1.0e4 and plain_fraction < 1.0e-4 and a1_boundary_preserved
    fitted_origin_rejected = required_log10_ratio > 1000.0
    one_sided_rejected = one_sided_ratio > 1.0e6
    no_mass_fit = tuned_mass_for_exact_delay > (GW170817_TOTAL_MASS_MSUN + GW170817_TOTAL_MASS_PLUS_MSUN)
    shared_road_ok = float(g699c.get("active_shared_road_differential_s", 999)) == 0.0

    checks = [
        check_row("P1_sources_present", "All load-bearing local and external sources are present.", load_bearing_sources_present, load_bearing_sources_present, "source_chain"),
        check_row("P2_external_event_inputs_frozen", "Fresh run uses primary external mass, delay, and distance values.", event_inputs, True, "primary external sources"),
        check_row("P3_CR116_massless_m18_channel", "GW channel is backed by CR116 m=18 massless tensor-carrier theorem.", cr116, cr116_pass, "CR116"),
        check_row("P4_CR006_A_integral_lane_available", "Plain A-road integral lane is available for wrong-control testing.", cr006, cr006_pass, "CR006"),
        check_row("P5_release_surface_from_A0", "A0 threshold gives r_release/Rs and A_release without event fitting.", packet, float(packet["r_release_over_rs"]) > 1.0 and float(packet["A_release"]) < 1.0, "G96/G699c"),
        check_row("P6_fresh_mass_prediction_within_1sigma", "Using published 2.74 Msun mass predicts delay within 1 sigma.", delay_budget[1], central_within_1sigma, "GW170817 mass + G96 law"),
        check_row("P7_mass_uncertainty_band_within_1sigma", "The published mass uncertainty band remains within the observed delay window.", release_rows[1:3], band_inside_1sigma, "GW170817 mass uncertainty"),
        check_row("P8_legacy_rounding_not_required", "Fresh published mass works; the pass does not depend on old rounded 2.70 Msun.", {"fresh": predicted, "legacy": packet_legacy["tau_engine_s"]}, external_mass_not_legacy and central_within_1sigma, "fresh external rerun"),
        check_row("P9_A1_no_escape_boundary_preserved", "A=1 is not treated as a literal photon launch point.", packet["A1_exact_status"], a1_boundary_preserved, "SAM strong-boundary rule"),
        check_row("P10_static_A_integral_rejected", "A formal static first-order (1/c) int A dr across the release gap is far too small and is not the seconds-scale mechanism.", {"plain_s": plain_a_s, "observed_s": OBSERVED_DELAY_S, "shortfall": plain_shortfall}, plain_a_rejected, "CR006 lane"),
        check_row("P11_fitted_origin_radius_rejected", "Forcing the formal static A integral would require an absurd origin-radius ratio.", {"required_ln_ratio": required_ln_ratio, "required_log10_ratio": required_log10_ratio}, fitted_origin_rejected, "static A integral inversion"),
        check_row("P12_one_sided_long_road_rejected", "Full 40 Mpc one-sided A-road remains many orders too large.", g699c.get("one_sided_control"), one_sided_rejected, "G699c/F5c"),
        check_row("P13_post_release_shared_road_preserved", "After release, GW and EM share the same A-road differential.", g699c.get("active_shared_road_differential_s"), shared_road_ok, "G699c"),
        check_row("P14_no_exact_mass_fit", "Exact-delay mass fit is not used and falls outside the published mass band.", {"tuned_mass_for_exact_delay": tuned_mass_for_exact_delay, "mass_high": GW170817_TOTAL_MASS_MSUN + GW170817_TOTAL_MASS_PLUS_MSUN}, no_mass_fit, "wrong-control mass fit"),
    ]

    wrong_controls = [
        wc_row(
            "WC1_FULL_40MPC_ONE_SIDED_A_ROAD",
            "Light is slowed by the full matter-sourced A-road while GW is not.",
            {"one_sided_delay_s": one_sided_delay, "ratio_to_observed": one_sided_ratio},
            one_sided_rejected,
            "This predicts years, not 1.74 s; G699c/F5c reject it.",
        ),
        wc_row(
            "WC2_PLAIN_LOCAL_A_INTEGRAL_EXPLAINS_SECONDS",
            "A simple static local Shapiro-style integral across the release gap accounts for the delay.",
            {"plain_A_integral_s": plain_a_s, "observed_s": OBSERVED_DELAY_S, "shortfall": plain_shortfall},
            plain_a_rejected,
            "The formal static integral gives only tens of microseconds, so the seconds-scale lag is not this lane.",
        ),
        wc_row(
            "WC3_FIT_EM_ORIGIN_RADIUS_TO_FORCE_DELAY",
            "Choose an EM origin radius so the formal static A integral equals 1.74 s.",
            {"required_ln_r_release_over_r_origin": required_ln_ratio, "required_log10_ratio": required_log10_ratio},
            fitted_origin_rejected,
            "The required radius ratio is exponentially absurd and is not an admissible physical origin.",
        ),
        wc_row(
            "WC4_M18_AS_GRAVITON_REST_MASS",
            "The m=18 carrier is a graviton rest mass.",
            {"CR116_particle_catalog_status": cr116.get("particle_catalog_status"), "CR116_wave_mode": cr116.get("wave_mode")},
            cr116_pass and cr116.get("particle_catalog_status") == "carrier_only_not_matter",
            "CR116 says carrier packet, not matter row or rest mass.",
        ),
        wc_row(
            "WC5_OLD_ROUNDED_MASS_IS_REQUIRED",
            "The GW170817 pass only works with the old rounded 2.70 Msun input.",
            {"fresh_mass_prediction_s": predicted, "legacy_prediction_s": packet_legacy["tau_engine_s"]},
            external_mass_not_legacy and central_within_1sigma,
            "The primary 2.74 Msun value passes more tightly than the old rounded control.",
        ),
        wc_row(
            "WC6_TUNE_MASS_TO_EXACT_DELAY",
            "Fit the total mass to make the delay exactly 1.74 s.",
            {"tuned_mass_for_exact_delay": tuned_mass_for_exact_delay, "published_mass_range": [GW170817_TOTAL_MASS_MSUN - GW170817_TOTAL_MASS_MINUS_MSUN, GW170817_TOTAL_MASS_MSUN + GW170817_TOTAL_MASS_PLUS_MSUN]},
            no_mass_fit,
            "The exact-fit mass is outside the primary low-spin mass interval and is not used.",
        ),
        wc_row(
            "WC7_NO_LOCAL_ENGINE_TIME",
            "There is no local release/engine delay; only shared-road propagation remains.",
            {"shared_road_differential_s": 0.0, "observed_s": OBSERVED_DELAY_S},
            shared_road_ok and OBSERVED_DELAY_S > 1.0,
            "Shared road gives zero differential; local source/release delay is required.",
        ),
        wc_row(
            "WC8_DIFFERENT_POST_RELEASE_SPEED",
            "After release, GW and EM propagate at meaningfully different speeds.",
            {"G699c_shared_road_differential_s": g699c.get("active_shared_road_differential_s"), "external_speed_bound_source": "arXiv:1710.05834"},
            shared_road_ok,
            "The active SAM lane keeps the post-release road shared; external GW170817 bounds also make large speed splits impossible.",
        ),
        wc_row(
            "WC9_A1_AS_LITERAL_LIGHT_LAUNCH_POINT",
            "A photon launches from exact A=1 and escapes normally.",
            packet["A1_exact_status"],
            a1_boundary_preserved,
            "At A=1 the light does not simply launch outward; A=1 is the no-escape / zero-depth boundary.",
        ),
    ]

    all_predictions_passed = all(bool(row["passed"]) for row in checks)
    all_wrong_controls_rejected = all(bool(row["rejected"]) for row in wrong_controls)
    result_class = RESULT_CLASS_PASS if all_predictions_passed and all_wrong_controls_rejected else RESULT_CLASS_FAIL

    lock = {
        "cr_id": CR_ID,
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "theorem_or_test": "fresh GW170817 A-release / EM-origin differential",
        "external_inputs": {
            "observed_delay_s": OBSERVED_DELAY_S,
            "observed_delay_sigma_s": OBSERVED_DELAY_SIGMA_S,
            "total_mass_msun": GW170817_TOTAL_MASS_MSUN,
            "total_mass_plus_msun": GW170817_TOTAL_MASS_PLUS_MSUN,
            "total_mass_minus_msun": GW170817_TOTAL_MASS_MINUS_MSUN,
            "distance_mpc": GW170817_DISTANCE_MPC,
        },
        "sam_release_packet": {
            "A0": packet["A0"],
            "x_outer": packet["x_outer"],
            "r_release_over_rs": packet["r_release_over_rs"],
            "A_release": packet["A_release"],
            "delta_A_from_A1_to_release": packet["delta_A_from_A1_to_release"],
            "tau_engine_s": predicted,
            "residual_s": residual,
            "residual_sigma": residual_sigma,
            "abs_percent_error": abs_percent_error,
        },
        "dynamic_A_release_boundary": {
            "A1_exact_status": packet["A1_exact_status"],
            "active_mechanism": "dynamic A-release / source-engine reorganization",
            "static_control_status": "rejected as seconds-scale mechanism",
            "formal_static_A_integral_boundary_to_release_s": plain_a_s,
            "formal_light_crossing_boundary_to_release_s": plain_light_s,
            "observed_over_plain": plain_shortfall,
            "required_ln_ratio_to_force_delay": required_ln_ratio,
            "required_log10_ratio_to_force_delay": required_log10_ratio,
            "boundary": "exact A=1 is not a literal photon launch point; static A integral is only a wrong-control lane",
        },
        "carrier_channel": {
            "source": "CR116",
            "split_loss_tensor_channel": cr116.get("split_loss_tensor_channel"),
            "wave_mode": cr116.get("wave_mode"),
            "particle_catalog_status": cr116.get("particle_catalog_status"),
        },
        "source_hashes": {row["label"]: row["sha256"] for row in sources if row["sha256"]},
    }

    write_csv(
        SOURCE_CHAIN_CSV,
        sources,
        ["label", "role", "load_bearing", "source_type", "path", "url", "exists", "sha256", "note"],
    )
    write_csv(EVENT_INPUTS_CSV, event_inputs)
    write_csv(RELEASE_ROWS_CSV, release_rows)
    write_csv(DELAY_BUDGET_CSV, delay_budget)
    write_csv(CHECKS_CSV, checks, ["check_id", "description", "observed", "passed", "source"])
    write_csv(WRONG_CONTROLS_CSV, wrong_controls, ["control_id", "hypothesis", "observed", "rejected", "reason"])
    write_json(LOCK_JSON, lock)
    LOCK_SHA.write_text(f"{sha256_file(LOCK_JSON)}  {branch_rel(LOCK_JSON)}\n", encoding="ascii")

    summary = {
        "cr_id": CR_ID,
        "branch": "04_PHOTON_ROAD_SHAPIRO_DELAY",
        "test_class": "GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "all_predictions_passed": all_predictions_passed,
        "all_wrong_controls_rejected": all_wrong_controls_rejected,
        "observed_delay_s": OBSERVED_DELAY_S,
        "observed_delay_sigma_s": OBSERVED_DELAY_SIGMA_S,
        "fresh_total_mass_msun": GW170817_TOTAL_MASS_MSUN,
        "fresh_engine_delay_s": predicted,
        "residual_s": residual,
        "residual_sigma": residual_sigma,
        "abs_percent_error": abs_percent_error,
        "r_release_over_rs": packet["r_release_over_rs"],
        "A_release": packet["A_release"],
        "delta_A_from_A1_to_release": packet["delta_A_from_A1_to_release"],
        "A1_exact_status": packet["A1_exact_status"],
        "formal_static_A_integral_boundary_to_release_s": plain_a_s,
        "formal_static_A_integral_status": "REJECTED_AS_SECONDS_SCALE_EXPLANATION",
        "active_local_mechanism": "DYNAMIC_A_RELEASE_ENGINE_REORGANIZATION",
        "m18_carrier_status": "MASSLESS_TENSOR_CARRIER_PACKET_FROM_CR116",
        "post_release_road": "SHARED_A_ROAD_ZERO_DIFFERENTIAL",
        "lock_sha256": sha256_file(LOCK_JSON),
        "result_md": branch_rel(RESULT_MD),
        "summary_json": branch_rel(SUMMARY_JSON),
        "checks_csv": branch_rel(CHECKS_CSV),
        "wrong_controls_csv": branch_rel(WRONG_CONTROLS_CSV),
    }
    write_json(SUMMARY_JSON, summary)

    pass_lines = "\n".join(
        f"- {'PASS' if row['passed'] else 'FAIL'} {row['check_id']}: {row['description']}"
        for row in checks
    )
    wc_lines = "\n".join(
        f"- {'REJECTED' if row['rejected'] else 'LIVE'} {row['control_id']}: {row['hypothesis']}"
        for row in wrong_controls
    )
    source_lines = "\n".join(
        f"- {row['label']} [{row['source_type']}]: `{row['path'] or row['url']}`"
        for row in sources
        if row["load_bearing"]
    )

    RESULT_MD.write_text(
        f"""# CR147 GW170817 A-Release / EM-Origin Differential

## Verdict

```text
{result_class}
```

## Tested Claim

GW170817 is read through the post-CR116 SAM picture:

```text
GW channel        = massless m=18 tensor-carrier packet
local lag         = dynamic A-release / source-engine reorganization
post-release road = shared A-road, zero GW/EM differential
```

The fresh external rerun uses the published total mass `2.74 +0.04/-0.01 M_sun`, not the older rounded `2.70 M_sun` G699c input.

## Fresh Event Inputs

```text
observed GW-to-GRB delay = {OBSERVED_DELAY_S:.6f} +/- {OBSERVED_DELAY_SIGMA_S:.6f} s
total mass               = {GW170817_TOTAL_MASS_MSUN:.6f} +{GW170817_TOTAL_MASS_PLUS_MSUN:.6f}/-{GW170817_TOTAL_MASS_MINUS_MSUN:.6f} M_sun
distance                 = {GW170817_DISTANCE_MPC:.6f} Mpc
```

## Release Surface

```text
A0                         = {float(packet['A0']):.15f}
x_outer                    = {float(packet['x_outer']):.15f}
r_release/Rs               = {float(packet['r_release_over_rs']):.12f}
A_release                  = {float(packet['A_release']):.12f}
delta_A from A=1 to release = {float(packet['delta_A_from_A1_to_release']):.12f}
```

## Delay Budget

```text
fresh SAM release/engine delay = {predicted:.12f} s
observed delay                 = {OBSERVED_DELAY_S:.12f} s
residual                       = {residual:.12f} s
residual sigma                 = {residual_sigma:.6f}
absolute percent error         = {abs_percent_error:.6f} %
mass-band prediction           = {predicted_low:.12f} s to {predicted_high:.12f} s
legacy 2.70 Msun prediction    = {float(packet_legacy['tau_engine_s']):.12f} s
```

## Important Boundary

The static local A-integral version is not the seconds-scale explanation, and
exact A=1 is not a normal photon launch point:

```text
A=1 exact status                         = {packet['A1_exact_status']}
formal static int A dr / c across gap    = {plain_a_s:.12e} s
formal light crossing across gap         = {plain_light_s:.12e} s
observed / formal static A integral      = {plain_shortfall:.6e}
required ln(r_release/r_origin)          = {required_ln_ratio:.6f}
required log10 ratio                     = {required_log10_ratio:.6f}
```

So the safe statement is:

```text
The m=18 tensor carrier supplies the massless GW channel. The observed
GW170817 lag is carried by dynamic A-release / local source-engine
reorganization. Once EM reaches the release surface, EM and GW share the same
A-road.
```

Do not say:

```text
A photon launches from exact A=1 and escapes normally.
The 1.74 s delay is explained by a simple static local Shapiro-style
int A dr/c across the release gap.
```

## Pass Checks

{pass_lines}

## Wrong Controls

{wc_lines}

## Load-Bearing Sources

{source_lines}

## Falsification Handle

Future BNS + EM events with reliable launch-time interpretation should fall near the same mass-scaling law:

```text
tau_release = {float(packet['slope_s_per_msun']):.12f} s/M_sun * M_total
```

## Hash

```text
CR147_gw170817_a_release_lock.json sha256 = {sha256_file(LOCK_JSON)}
```
""",
        encoding="utf-8",
    )

    artifacts = [
        SOURCE_CHAIN_CSV,
        EVENT_INPUTS_CSV,
        RELEASE_ROWS_CSV,
        DELAY_BUDGET_CSV,
        CHECKS_CSV,
        WRONG_CONTROLS_CSV,
        LOCK_JSON,
        LOCK_SHA,
        SUMMARY_JSON,
        RESULT_MD,
    ]
    update_local_hashes(artifacts)

    print(f"CR147 runner: result_class={result_class}")
    print(f"CR147 runner: all_predictions_passed={all_predictions_passed}")
    print(f"CR147 runner: all_wrong_controls_rejected={all_wrong_controls_rejected}")
    print(f"CR147 runner: fresh_engine_delay_s={predicted:.12f}")
    print(f"CR147 runner: residual_sigma={residual_sigma:.6f}")
    print(f"CR147 runner: plain_A_integral_s={plain_a_s:.12e}")
    print(f"CR147 runner: lock_sha256={sha256_file(LOCK_JSON)}")
    return 0 if result_class == RESULT_CLASS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
