"""CR011 runner — verify §1.3 numerical claim d_ref_base = R × λ_spaghettio.

Structural-foundation CR: no measurement, no fit, no external data. The runner
verifies:
  G3 — arithmetic reproduction of the derived value from sealed upstream
  Consistency checks against CR266 seven-atom identities
  Informational compute of S1 v2 H_pred at bench distance 0.15 m
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> dict:
    results: dict = {}

    # ---------- CR266 seven-atom identities (integer arithmetic) ----------
    h_hat = 2
    d_hat = 3
    S = h_hat**d_hat            # 8
    R = h_hat**2 * d_hat        # 12
    V = d_hat**3                # 27
    F = d_hat**4                # 81
    Theta = h_hat * d_hat**2    # 18
    L_curly = h_hat * d_hat**4  # 162
    M = (S - 1) * Theta         # 126

    identities = {
        "S = h^d": (S, 8),
        "R = h^2 * d": (R, 12),
        "V = d^3": (V, 27),
        "F = d^4": (F, 81),
        "Theta = h * d^2": (Theta, 18),
        "L = h * d^4": (L_curly, 162),
        "M = (S-1) * Theta": (M, 126),
        "R^2 = M + Theta (CR229 identity)": (R**2, M + Theta),
        "R^2 numeric": (R**2, 144),
    }
    for label, (got, want) in identities.items():
        assert got == want, f"{label}: got {got}, want {want}"
    results["cr266_atom_identities"] = "PASS (9/9)"

    # ---------- CR010 §1.2 numerical claim: λ_spaghettio ----------
    # ħc = 197.3269804 MeV·fm (NIST CODATA)
    # m_3 = 50.9 meV/c² (CR001@20 spectrum from Δm²_31)
    hc_MeV_fm = 197.3269804
    m3_meV = 50.9

    # λ_C = ħc / (mc²). With ħc in MeV·fm and mc² in MeV:
    # λ_C [fm] = ħc [MeV·fm] / mc² [MeV]
    # m3 in MeV: 50.9e-9
    lambda_C_fm = hc_MeV_fm / (m3_meV * 1e-9)
    lambda_spaghettio_um = lambda_C_fm / 1e9  # fm to μm

    expected_um = 3.877
    delta = abs(lambda_spaghettio_um - expected_um)
    assert delta < 0.01, f"λ_spaghettio: got {lambda_spaghettio_um:.4f} μm, want ~{expected_um} μm"
    results["cr010_lambda_spaghettio_um"] = round(lambda_spaghettio_um, 4)
    results["cr010_lambda_spaghettio_check"] = "PASS"

    # ---------- CR011 §1.3 numerical claim: d_ref_base ----------
    d_ref_base_um = R * lambda_spaghettio_um
    expected_46 = 46.5
    delta2 = abs(d_ref_base_um - expected_46)
    assert delta2 < 0.2, f"d_ref_base: got {d_ref_base_um:.4f} μm, want ~46.5 μm"
    results["cr011_d_ref_base_um"] = round(d_ref_base_um, 4)
    results["cr011_d_ref_base_check"] = "PASS"

    # ---------- Informational: S1 v2 H_pred at bench distance ----------
    # A₀ = 1/(12π) per Vol I §7 (sealed)
    A_0 = 1.0 / (12.0 * math.pi)
    d_bench_m = 0.15  # bench distance
    d_ref_base_m = d_ref_base_um * 1e-6

    # H_pred = A₀ · d_ref / d
    H_pred = A_0 * d_ref_base_m / d_bench_m
    floor = 7.4e-6  # CR-NSC-01 §7 overnight sensitivity floor
    ratio_to_floor = H_pred / floor

    results["informational_A_0"] = A_0
    results["informational_bench_distance_m"] = d_bench_m
    results["informational_H_pred_at_0.15m"] = f"{H_pred:.4e}"
    results["informational_CR_NSC_01_floor"] = f"{floor:.4e}"
    results["informational_H_pred_over_floor"] = round(ratio_to_floor, 3)
    results["informational_landing_at_n_0"] = (
        "F-iii marginal (~1.1x floor)" if 1.0 < ratio_to_floor < 2.0
        else "F-ii (below floor)" if ratio_to_floor < 1.0
        else "F-iii solid (>2x floor)"
    )

    # ---------- Alternative candidates for information ----------
    results["alt_candidate_a_loop_scale_um"] = round(lambda_spaghettio_um, 4)
    results["alt_candidate_a_H_pred"] = f"{A_0 * lambda_spaghettio_um * 1e-6 / d_bench_m:.4e}"
    results["alt_candidate_a_status"] = "INCONSISTENT with CR010 §1.5 elsewhere-propagation"

    d_ref_alt_R2_um = R**2 * lambda_spaghettio_um
    results["alt_candidate_c_R2_scale_um"] = round(d_ref_alt_R2_um, 4)
    results["alt_candidate_c_H_pred"] = f"{A_0 * d_ref_alt_R2_um * 1e-6 / d_bench_m:.4e}"
    results["alt_candidate_c_status"] = "RULED OUT by Vol II §11C A-operator domain rule (stable charged matter only)"

    # ---------- Overall verdict ----------
    results["verdict"] = "PASS"
    results["verdict_signature"] = (
        "CR011_PASS_LOOP_POP_BOUNCE_INTERSECT_COUPLING_MECHANISM_"
        "d_ref_base_EQUALS_R_TIMES_LAMBDA_SPAGHETTIO_EQUALS_"
        "12_TIMES_3.877_MICRO_METER_EQUALS_46.53_MICRO_METER_"
        "MECHANISM_FORCED_FROM_CR010_1.5_ENDPOINT_PROPAGATION_"
        "PLUS_CR266_R_12_MIRROR_LINEAR_EXTENT_"
        "PLUS_CR010_1.2_PER_ADDRESS_SCALE_"
        "NO_FREE_PARAMETERS_NO_BENCH_TARGET_REFERENCE"
    )

    return results


if __name__ == "__main__":
    results = main()
    out_path = Path(__file__).parent / "CR011_summary.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("=" * 70)
    print("CR011 — Loop Pop-Bounce-Intersect Coupling Mechanism — RUNNER")
    print("=" * 70)
    for k, v in results.items():
        print(f"  {k}: {v}")
    print("=" * 70)
