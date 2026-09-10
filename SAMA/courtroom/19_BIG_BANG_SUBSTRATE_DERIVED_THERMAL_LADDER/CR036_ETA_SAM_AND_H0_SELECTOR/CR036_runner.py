"""
CR036 runner: eta_SAM and H_0_SAM selector.

Implements the test specified in CR036_PRECOMMIT.md
(SHA-256 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2).

Substrate identity under test:
  eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V)
          = 7 / (4 * (12*pi)^6)
          = 6.09608952448e-10   (expected)

Cascade:
  K_eta_to_omega_b = (3 H_100^2 / (8 pi G)) / (m_p * n_gamma(T_CMB))
                     (derived in-runner from c, h, k_B, G, T_CMB, m_p, Mpc)
  omega_b,SAM = eta_SAM / K_eta_to_omega_b
  Omega_b,SAM = 2 * A_0 * (1 - chi)
  h_SAM^2     = omega_b,SAM / Omega_b,SAM
  H_0,SAM     = 100 * h_SAM   km/s/Mpc
              = 67.25037526   (expected)

P1 (load-bearing): |eta_dev_pct| vs eta_reference 6.119e-10
                   PASS <= 1.0, BOUNDARY <= 2.0, FAIL > 2.0
                   STRONG_CONTACT_ETA if <= 0.5

P2 (load-bearing): |H0_dev_pct| vs H_0_reference 67.36 km/s/Mpc
                   PASS <= 1.0, BOUNDARY <= 2.0, FAIL > 2.0

I1 (implementation integrity, NOT a science gate):
  Path A (substrate-atom form) vs Path B (compact 7/(4*(12pi)^6))
  must agree to < 1e-12 relative.

E1-E5: reported evidence; not gated.
"""

from __future__ import annotations

import builtins
import csv
import json
import math
import os
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")


def _jsonify(o):
    """Native types only — no numpy in this runner."""
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


# =====================================================================
# Strict input discipline: forbidden-file open() guard
# =====================================================================

CR_DIR = Path(__file__).resolve().parent

FORBIDDEN_PATTERNS = [
    re.compile(r"CR00[12]b?_(summary|result|evidence).*", re.IGNORECASE),
    re.compile(r"CR00[123]_(summary|result|evidence).*",  re.IGNORECASE),
    re.compile(r"CR018b?_(summary|result|evidence).*",    re.IGNORECASE),
    re.compile(r"CR019_(summary|result|evidence).*",      re.IGNORECASE),
    re.compile(r"CR025_(summary|result|evidence).*",      re.IGNORECASE),
    re.compile(r"CR031b?_(summary|result|evidence).*",    re.IGNORECASE),
    re.compile(r"CR032_(summary|result|evidence).*",      re.IGNORECASE),
    re.compile(r"CR033_(summary|result|evidence).*",      re.IGNORECASE),
    re.compile(r"CR205.*",                                re.IGNORECASE),
    re.compile(r"CR035A2?_summary\.json$",                re.IGNORECASE),
    re.compile(r"CR035A2?_result\.md$",                   re.IGNORECASE),
    re.compile(r"CR035A2?_(TT|TE|EE)_residuals\.csv$",    re.IGNORECASE),
    re.compile(r"CR035A2?_peaks\.csv$",                   re.IGNORECASE),
    re.compile(r"CR035A2?_runB_diagnostic\.json$",        re.IGNORECASE),
    re.compile(r"CR035A2?_runA_theory_spectra\.csv$",     re.IGNORECASE),
    re.compile(r"CR035A2?_runner.*\.py$",                 re.IGNORECASE),
    re.compile(r"COM_PowerSpect_CMB.*",                   re.IGNORECASE),
    re.compile(r".*plikHM.*",                             re.IGNORECASE),
    re.compile(r".*posterior.*\.txt$",                    re.IGNORECASE),
    re.compile(r".*chain.*\.txt$",                        re.IGNORECASE),
]

OPENED_PATHS: list[str] = []
_orig_open = builtins.open


def _guarded_open(file, *args, **kwargs):
    p = os.fspath(file) if not isinstance(file, int) else str(file)
    OPENED_PATHS.append(p)
    base = os.path.basename(p)
    for pat in FORBIDDEN_PATTERNS:
        if pat.search(base):
            raise RuntimeError(
                f"CR036 forbidden-file guard tripped: attempted to open {p!r}"
            )
    return _orig_open(file, *args, **kwargs)


builtins.open = _guarded_open


# =====================================================================
# Frozen substrate atoms (integers / closed forms)
# =====================================================================

PI = math.pi
R       = 12
D       = 3
S       = 8
ALPHA_H = 2
THETA   = 18              # alpha_H * D^2
M_CAP   = 126             # R^2 - Theta
F_CAR   = 81              # D^(D+1)
L       = 162             # alpha_H * F
V       = 27              # D^3
A_0     = 1.0 / (12.0 * PI)
CHI     = (S / D) * A_0

OMEGA_B_SAM = 2.0 * A_0 * (1.0 - CHI)
OMEGA_M_SAM = R * A_0
OMEGA_C_SAM = OMEGA_M_SAM - OMEGA_B_SAM


# =====================================================================
# Dimensional bridge (CODATA 2018 / SI fixed; in-code numeric literals)
# =====================================================================

C_M_S      = 299792458.0              # m/s, SI exact
H_J_S      = 6.62607015e-34           # J*s, SI exact (2019)
HBAR_J_S   = H_J_S / (2.0 * PI)       # COMPUTED IN-RUNNER
K_B_J_K    = 1.380649e-23             # J/K, SI exact (2019)
G_MKS      = 6.67430e-11              # m^3/(kg*s^2), CODATA 2018
MPC_M      = 3.0856775815e22          # m, parsec-based
M_P_KG     = 1.67262192369e-27        # kg, CODATA 2018
T_CMB_K    = 2.7255                   # K, FIRAS

ZETA_3     = 1.2020569031595942853997381  # Apery's constant

N_EFF      = 3.046                    # standard

# Frozen external references (numeric constants; runner does NOT open files)
ETA_REFERENCE        = 6.119e-10
ETA_BBN_CONSENSUS    = 6.10e-10
H_0_REFERENCE_KMS_MPC = 67.36


# =====================================================================
# eta_SAM identity (Path A and Path B for I1)
# =====================================================================

def eta_sam_path_a() -> float:
    """Path A: substrate-atom form (M / (alpha_H^2 * Theta)) * A_0^(L/V)."""
    exponent = L // V                  # 162 / 27 = 6 (exact integer)
    assert L % V == 0, "L/V must be an integer reducer"
    coef = M_CAP / (ALPHA_H * ALPHA_H * THETA)
    return coef * (A_0 ** exponent)


def eta_sam_path_b() -> float:
    """Path B: compact algebraic form 7 / (4 * (12*pi)^6)."""
    return 7.0 / (4.0 * (12.0 * PI) ** 6)


# =====================================================================
# In-runner eta -> omega_b conversion
# =====================================================================

def derive_K_eta_to_omega_b():
    """Compute K such that eta = K * omega_b, from first principles."""
    # Photon number density at T_CMB (Planck blackbody)
    # n_gamma = (2 * zeta(3) / pi^2) * (k_B T / (hbar c))^3
    kT = K_B_J_K * T_CMB_K
    inv_lambda = kT / (HBAR_J_S * C_M_S)           # m^-1
    n_gamma = (2.0 * ZETA_3 / PI ** 2) * inv_lambda ** 3   # m^-3

    # Critical density at h = 1
    # H_100 = 100 km/s/Mpc converted to s^-1
    H_100 = 100.0 * 1000.0 / MPC_M                 # s^-1
    rho_crit_h1 = 3.0 * H_100 ** 2 / (8.0 * PI * G_MKS)   # kg/m^3

    # Baryon number density per omega_b at h=1
    n_b_per_omega_b = rho_crit_h1 / M_P_KG         # m^-3 per omega_b

    # K such that eta = K * omega_b
    K = n_b_per_omega_b / n_gamma                  # dimensionless / omega_b

    return dict(
        n_gamma_per_m3=n_gamma,
        H_100_per_s=H_100,
        rho_crit_h1_kg_per_m3=rho_crit_h1,
        n_b_per_omega_b_per_m3=n_b_per_omega_b,
        K_eta_to_omega_b=K,
    )


# =====================================================================
# Verdict bands
# =====================================================================

def band(dev_pct: float, pass_thresh: float = 1.0,
         boundary_thresh: float = 2.0) -> str:
    a = abs(dev_pct)
    if a <= pass_thresh:
        return "PASS"
    if a <= boundary_thresh:
        return "BOUNDARY"
    return "FAIL"


def combine_verdict(p1: str, p2: str) -> str:
    if "FAIL" in (p1, p2):
        return "FAIL"
    if "BOUNDARY" in (p1, p2):
        return "BOUNDARY"
    return "PASS"


# =====================================================================
# Output writers
# =====================================================================

def write_evidence_csv(path: Path, conv: dict, eta_A: float, eta_B: float,
                       omega_b_sam: float, h_sam: float, H0_sam: float,
                       z_eq_sam: float):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["field", "value", "units", "notes"])
        # Substrate atoms
        w.writerow(["R", R, "", "radix"])
        w.writerow(["D", D, "", "dimension"])
        w.writerow(["S", S, "", "split inventory"])
        w.writerow(["alpha_H", ALPHA_H, "", "binary readout"])
        w.writerow(["Theta", THETA, "", "tensor bridge alpha_H*D^2"])
        w.writerow(["M", M_CAP, "", "matter capacity R^2-Theta"])
        w.writerow(["F", F_CAR, "", "carrier face D^(D+1)"])
        w.writerow(["L", L, "", "closed ledger alpha_H*F"])
        w.writerow(["V", V, "", "resolved write cell D^3"])
        w.writerow(["L_over_V", L // V, "", "ledger-to-write-cell reducer"])
        w.writerow(["A_0", f"{A_0:.20e}", "", "= 1/(12*pi) = V/(pi*alpha_H*L)"])
        w.writerow(["chi", f"{CHI:.20e}", "", "= (S/D)*A_0 = 2/(9*pi)"])
        w.writerow(["Omega_b_SAM", f"{OMEGA_B_SAM:.20e}", "",
                    "= 2*A_0*(1-chi)"])
        w.writerow(["Omega_m_SAM", f"{OMEGA_M_SAM:.20e}", "", "= R*A_0 = 1/pi"])
        w.writerow(["Omega_c_SAM", f"{OMEGA_C_SAM:.20e}", "",
                    "= Omega_m - Omega_b"])
        # Dimensional bridge
        w.writerow(["c", C_M_S, "m/s", "SI exact"])
        w.writerow(["h_Planck", H_J_S, "J*s", "SI exact 2019"])
        w.writerow(["hbar (computed)", f"{HBAR_J_S:.20e}", "J*s",
                    "= h/(2*pi)"])
        w.writerow(["k_B", K_B_J_K, "J/K", "SI exact 2019"])
        w.writerow(["G", G_MKS, "m^3/(kg*s^2)", "CODATA 2018"])
        w.writerow(["Mpc", MPC_M, "m", "parsec-based"])
        w.writerow(["m_p", M_P_KG, "kg", "CODATA 2018"])
        w.writerow(["T_CMB", T_CMB_K, "K", "FIRAS"])
        w.writerow(["N_eff", N_EFF, "", "standard"])
        # Computed intermediates
        w.writerow(["n_gamma", f"{conv['n_gamma_per_m3']:.10e}", "1/m^3",
                    "Planck blackbody at T_CMB"])
        w.writerow(["H_100", f"{conv['H_100_per_s']:.10e}", "1/s",
                    "100 km/s/Mpc in SI"])
        w.writerow(["rho_crit_h1", f"{conv['rho_crit_h1_kg_per_m3']:.10e}",
                    "kg/m^3", "Friedmann at h=1"])
        w.writerow(["n_b_per_omega_b", f"{conv['n_b_per_omega_b_per_m3']:.10e}",
                    "1/m^3", "rho_crit_h1 / m_p"])
        w.writerow(["K_eta_to_omega_b (computed)",
                    f"{conv['K_eta_to_omega_b']:.15e}", "",
                    "eta = K * omega_b"])
        w.writerow(["K standard literature", "2.735e-8", "",
                    "comparison only"])
        # eta_SAM (Path A and B)
        w.writerow(["eta_SAM Path A", f"{eta_A:.15e}", "",
                    "(M/(alpha_H^2*Theta)) * A_0^(L/V)"])
        w.writerow(["eta_SAM Path B", f"{eta_B:.15e}", "",
                    "7 / (4*(12*pi)^6)"])
        # Cascade products
        w.writerow(["omega_b_SAM", f"{omega_b_sam:.15e}", "",
                    "eta_SAM / K_eta_to_omega_b"])
        w.writerow(["h_SAM", f"{h_sam:.15e}", "",
                    "sqrt(omega_b_SAM / Omega_b_SAM)"])
        w.writerow(["H_0_SAM", f"{H0_sam:.15e}", "km/s/Mpc", "= 100 * h_SAM"])
        # z_eq cascade (E5)
        w.writerow(["z_eq_SAM", f"{z_eq_sam:.10e}", "",
                    "Omega_m * h^2 / (omega_gamma*(1+0.2271*N_eff)) - 1"])
        # External anchors (cited; never read from file)
        w.writerow(["eta_reference", f"{ETA_REFERENCE:.6e}", "",
                    "Planck 2018 CMB-side"])
        w.writerow(["eta_BBN_consensus", f"{ETA_BBN_CONSENSUS:.6e}", "",
                    "E1 reporting only"])
        w.writerow(["H_0_reference", H_0_REFERENCE_KMS_MPC, "km/s/Mpc",
                    "Planck 2018 TT,TE,EE+lowE+lensing central"])


def write_substrate_atoms_csv(path: Path):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["symbol", "value", "definition"])
        w.writerow(["R",       R,       "radix"])
        w.writerow(["D",       D,       "dimension"])
        w.writerow(["S",       S,       "split inventory = 2^D"])
        w.writerow(["alpha_H", ALPHA_H, "binary readout"])
        w.writerow(["Theta",   THETA,   "tensor bridge alpha_H*D^2"])
        w.writerow(["F",       F_CAR,   "carrier face D^(D+1)"])
        w.writerow(["L",       L,       "closed ledger alpha_H*F"])
        w.writerow(["V",       V,       "resolved write cell D^3"])
        w.writerow(["M",       M_CAP,   "matter capacity R^2-Theta"])
        w.writerow(["L/V",     L // V,  "ledger-to-write-cell reducer = 6"])
        w.writerow(["A_0",     A_0,     "1/(12*pi) = V/(pi*alpha_H*L)"])
        w.writerow(["chi",     CHI,     "(S/D)*A_0 = 2/(9*pi)"])


# =====================================================================
# Main
# =====================================================================

def main() -> int:
    print("CR036 runner  -  eta_SAM and H_0,SAM selector")
    print()

    # eta_SAM via Path A (substrate atom form)
    eta_A = eta_sam_path_a()
    # eta_SAM via Path B (compact algebraic form)
    eta_B = eta_sam_path_b()

    # I1 implementation integrity
    i1_rel_diff = abs(eta_A - eta_B) / eta_A
    i1_ok = i1_rel_diff < 1e-12
    eta_SAM = eta_A   # Path A canonical

    print(f"  eta_SAM Path A  = {eta_A:.15e}")
    print(f"  eta_SAM Path B  = {eta_B:.15e}")
    print(f"  I1 |rel diff|   = {i1_rel_diff:.3e}  (OK if < 1e-12)")
    print()

    # In-runner conversion K
    conv = derive_K_eta_to_omega_b()
    K = conv["K_eta_to_omega_b"]
    K_std = 2.735e-8
    K_dev_pct = 100.0 * (K - K_std) / K_std

    print(f"  n_gamma         = {conv['n_gamma_per_m3']:.10e}  m^-3")
    print(f"  H_100           = {conv['H_100_per_s']:.10e}  s^-1")
    print(f"  rho_crit_h1     = {conv['rho_crit_h1_kg_per_m3']:.10e}  kg/m^3")
    print(f"  K (computed)    = {K:.15e}")
    print(f"  K (standard)    = {K_std:.6e}")
    print(f"  K dev vs std    = {K_dev_pct:+.4f} %")
    print()

    # Cascade
    omega_b_sam = eta_SAM / K
    h_sam_sq = omega_b_sam / OMEGA_B_SAM
    h_sam = math.sqrt(h_sam_sq)
    H0_sam = 100.0 * h_sam

    print(f"  omega_b_SAM     = {omega_b_sam:.15e}")
    print(f"  Omega_b_SAM     = {OMEGA_B_SAM:.15e}")
    print(f"  h_SAM           = {h_sam:.15e}")
    print(f"  H_0,SAM         = {H0_sam:.10f}  km/s/Mpc")
    print()

    # z_eq cascade (E5)
    # omega_gamma = (8 pi G / 3) * rho_gamma / H_100^2
    # rho_gamma = (pi^2 / 15) * (k_B T)^4 / (hbar c)^3
    rho_gamma = (PI ** 2 / 15.0) * (K_B_J_K * T_CMB_K) ** 4 / (HBAR_J_S * C_M_S) ** 3
    omega_gamma = (8.0 * PI * G_MKS / 3.0) * rho_gamma / conv["H_100_per_s"] ** 2
    omega_r = omega_gamma * (1.0 + 0.2271 * N_EFF)
    omega_m_sam = OMEGA_M_SAM * h_sam_sq
    z_eq_sam = omega_m_sam / omega_r - 1.0

    print(f"  omega_gamma     = {omega_gamma:.10e}")
    print(f"  omega_r (with N_eff={N_EFF}) = {omega_r:.10e}")
    print(f"  omega_m_SAM     = {omega_m_sam:.10e}")
    print(f"  z_eq_SAM        = {z_eq_sam:.4f}")
    print()

    # P1 — eta vs reference
    eta_dev_pct = 100.0 * (eta_SAM - ETA_REFERENCE) / ETA_REFERENCE
    p1 = band(eta_dev_pct, 1.0, 2.0)
    eta_dev_bbn_pct = 100.0 * (eta_SAM - ETA_BBN_CONSENSUS) / ETA_BBN_CONSENSUS
    strong_contact = abs(eta_dev_pct) <= 0.5 or abs(eta_dev_bbn_pct) <= 0.5

    print(f"  eta_reference   = {ETA_REFERENCE:.6e}")
    print(f"  eta_dev_pct     = {eta_dev_pct:+.6f} %  ({p1})")
    print(f"  eta_BBN         = {ETA_BBN_CONSENSUS:.6e}")
    print(f"  eta_dev_BBN_pct = {eta_dev_bbn_pct:+.6f} %")
    print(f"  STRONG_CONTACT_ETA = {strong_contact}")
    print()

    # P2 — H_0 vs reference
    H0_dev_pct = 100.0 * (H0_sam - H_0_REFERENCE_KMS_MPC) / H_0_REFERENCE_KMS_MPC
    p2 = band(H0_dev_pct, 1.0, 2.0)
    print(f"  H_0_reference   = {H_0_REFERENCE_KMS_MPC} km/s/Mpc")
    print(f"  H0_dev_pct      = {H0_dev_pct:+.6f} %  ({p2})")
    print()

    # E3 — six-way identification of L/V
    six_id_alpha_D   = (ALPHA_H * D == 6)
    six_id_R_over_2  = (R // 2 == 6) and (R % 2 == 0)
    six_id_theta_D   = (THETA % D == 0) and (THETA // D == 6)
    six_id_L_over_V  = (L % V == 0) and (L // V == 6)
    six_all = (six_id_alpha_D and six_id_R_over_2 and six_id_theta_D
               and six_id_L_over_V)

    # E4 — A_0 dual form
    A0_dual = V / (PI * ALPHA_H * L)
    A0_canon = 1.0 / (12.0 * PI)
    A0_dual_ok = abs(A0_dual - A0_canon) / A0_canon < 1e-15

    # Overall verdict
    verdict = combine_verdict(p1, p2)
    if verdict == "PASS":
        verdict_token = (
            "CR036_PASS_SUBSTRATE_DERIVED_ETA_AND_H0_BOTH_WITHIN_1PCT_OF_PLANCK_CMB_SIDE"
        )
    elif verdict == "BOUNDARY":
        verdict_token = (
            "CR036_BOUNDARY_AT_LEAST_ONE_GATE_IN_1_TO_2_PCT_BAND"
        )
    else:
        verdict_token = (
            "CR036_FAIL_AT_LEAST_ONE_GATE_OUTSIDE_2PCT_BAND"
        )

    print(f"  P1 (eta)        = {p1}")
    print(f"  P2 (H_0)        = {p2}")
    print(f"  I1 (impl)       = {'OK' if i1_ok else 'FLOATING_POINT_DRIFT'}")
    print(f"\n=== CR036 VERDICT: {verdict} ===")
    print(f"    {verdict_token}")

    # ----- Emit artifacts -----
    summary = dict(
        precommit_sha256="345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2",
        execution_status="CLEAN",
        scientific_verdict=verdict,
        verdict_token=verdict_token,
        triage_bin="A",
        free_parameters_introduced=0,
        prior_CR_result_inputs=False,
        CMB_spectrum_inputs=False,
        posterior_table_inputs=False,
        forbidden_files_opened=False,
        opened_paths_count=len(OPENED_PATHS),
        implementation_integrity=("OK" if i1_ok else "FLOATING_POINT_DRIFT"),
        # Substrate spine
        substrate=dict(
            R=R, D=D, S=S, alpha_H=ALPHA_H, Theta=THETA, M=M_CAP, F=F_CAR,
            L=L, V=V, L_over_V=L // V, A_0=A_0, chi=CHI,
            Omega_m_SAM=OMEGA_M_SAM, Omega_b_SAM=OMEGA_B_SAM,
            Omega_c_SAM=OMEGA_C_SAM,
        ),
        dimensional_bridge=dict(
            c_m_s=C_M_S, h_J_s=H_J_S, hbar_J_s=HBAR_J_S, k_B_J_K=K_B_J_K,
            G=G_MKS, Mpc_m=MPC_M, m_p_kg=M_P_KG, T_CMB_K=T_CMB_K,
            N_eff=N_EFF, zeta_3=ZETA_3,
        ),
        eta=dict(
            eta_SAM_path_A=eta_A,
            eta_SAM_path_B=eta_B,
            eta_SAM=eta_SAM,
            eta_reference=ETA_REFERENCE,
            eta_BBN_consensus=ETA_BBN_CONSENSUS,
            eta_dev_pct=eta_dev_pct,
            eta_dev_BBN_pct=eta_dev_bbn_pct,
            STRONG_CONTACT_ETA=strong_contact,
        ),
        conversion=dict(
            n_gamma_per_m3=conv["n_gamma_per_m3"],
            H_100_per_s=conv["H_100_per_s"],
            rho_crit_h1_kg_per_m3=conv["rho_crit_h1_kg_per_m3"],
            K_eta_to_omega_b=K,
            K_standard_literature=K_std,
            K_dev_pct=K_dev_pct,
        ),
        H0_cascade=dict(
            omega_b_SAM=omega_b_sam,
            h_SAM=h_sam,
            H_0_SAM=H0_sam,
            H_0_reference=H_0_REFERENCE_KMS_MPC,
            H0_dev_pct=H0_dev_pct,
        ),
        z_eq=dict(
            omega_gamma=omega_gamma, omega_r=omega_r,
            omega_m_SAM=omega_m_sam, z_eq_SAM=z_eq_sam,
        ),
        gates=dict(P1=p1, P2=p2, I1=("OK" if i1_ok else "FAIL"),
                   I1_rel_diff=i1_rel_diff),
        E3_six_identification=dict(
            alpha_H_times_D=six_id_alpha_D, R_over_2=six_id_R_over_2,
            Theta_over_D=six_id_theta_D, L_over_V=six_id_L_over_V,
            all_four_equal=six_all,
        ),
        E4_A0_dual_form=dict(
            A_0_via_V_over_piAH_L=A0_dual,
            A_0_canonical=A0_canon,
            agreement_ok=A0_dual_ok,
        ),
    )

    out_summary = CR_DIR / "CR036_summary.json"
    out_summary.write_text(json.dumps(summary, indent=2, default=_jsonify),
                            encoding="utf-8")
    write_evidence_csv(CR_DIR / "CR036_evidence_rows.csv", conv, eta_A, eta_B,
                       omega_b_sam, h_sam, H0_sam, z_eq_sam)
    write_substrate_atoms_csv(CR_DIR / "CR036_substrate_atoms.csv")

    # Result markdown
    result_md = f"""# CR036_ETA_SAM_AND_H0_SELECTOR

## Verdict

```text
{verdict_token}
```

## Courtroom Fields

```text
execution_status             = CLEAN
scientific_verdict           = {verdict}
triage_bin                   = A
free_parameters_introduced   = 0
prior_CR_result_inputs       = false
CMB_spectrum_inputs          = false
posterior_table_inputs       = false
forbidden_files_opened       = false
opened_paths_count           = {len(OPENED_PATHS)}
implementation_integrity     = {'OK' if i1_ok else 'FLOATING_POINT_DRIFT'}
precommit_sha256             = 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2
```

## Substrate Identity Under Test

| symbol | value |
|---|---:|
| M / (α_H² · Θ) | 126 / (4·18) = **7/4** |
| L / V | 162 / 27 = **6** |
| A_0 = V / (π·α_H·L) | {A_0:.15e} |
| **η_SAM = (7/4)·A_0^6** | **{eta_SAM:.15e}** |

## Six-Way Identification of L/V (E3)

| identification | value | match |
|---|---:|---:|
| α_H · D | {ALPHA_H * D} | {six_id_alpha_D} |
| R / 2 | {R // 2} | {six_id_R_over_2} |
| Θ / D | {THETA // D} | {six_id_theta_D} |
| **L / V** | **{L // V}** | **{six_id_L_over_V}** |
| all four equal | | **{six_all}** |

## I1 — Implementation Integrity (NOT a science gate)

| | value |
|---|---:|
| Path A: (M/(α_H²·Θ))·A_0^(L/V) | {eta_A:.15e} |
| Path B: 7/(4·(12π)^6) | {eta_B:.15e} |
| relative difference | {i1_rel_diff:.3e} |
| **implementation_integrity** | **{'OK' if i1_ok else 'FLOATING_POINT_DRIFT'}** |

## Dimensional Bridge (declared; in-runner literals)

| symbol | value | source |
|---|---:|---|
| c | {C_M_S} m/s | SI exact |
| h | {H_J_S:.10e} J·s | SI exact (2019) |
| ℏ = h/(2π) | {HBAR_J_S:.10e} J·s | **computed in-runner** |
| k_B | {K_B_J_K:.10e} J/K | SI exact (2019) |
| G | {G_MKS:.5e} m³/(kg·s²) | CODATA 2018 |
| Mpc | {MPC_M:.10e} m | parsec-based |
| m_p | {M_P_KG:.10e} kg | CODATA 2018 |
| T_CMB | {T_CMB_K} K | FIRAS |
| N_eff | {N_EFF} | standard |

## In-Runner Conversion (NOT hardcoded)

| quantity | value | notes |
|---|---:|---|
| n_γ (blackbody at T_CMB) | {conv['n_gamma_per_m3']:.10e} m⁻³ | (2·ζ(3)/π²)·(k_B·T_CMB/(ℏc))³ |
| H_100 in s⁻¹ | {conv['H_100_per_s']:.10e} s⁻¹ | 100 km/s/Mpc converted |
| ρ_crit at h=1 | {conv['rho_crit_h1_kg_per_m3']:.10e} kg/m³ | 3·H_100²/(8πG) |
| **K (η = K·ω_b) computed** | **{K:.15e}** | first-principles |
| K standard literature (compare) | 2.735×10⁻⁸ | reported only |
| K deviation vs standard | {K_dev_pct:+.4f} % | sensitivity evidence |

## P1 — η_SAM vs Planck-side reference

| field | value |
|---|---:|
| η_SAM | {eta_SAM:.15e} |
| η_reference (Planck) | {ETA_REFERENCE:.6e} |
| **η deviation** | **{eta_dev_pct:+.6f} %** |
| **P1 band** | **{p1}** |
| η_BBN consensus (E-only) | {ETA_BBN_CONSENSUS:.6e} |
| η dev vs BBN | {eta_dev_bbn_pct:+.6f} % |
| **STRONG_CONTACT_ETA** | **{strong_contact}** |

## P2 — H_0,SAM cascade vs Planck-side reference

| step | value |
|---|---:|
| ω_b,SAM = η_SAM / K | {omega_b_sam:.15e} |
| Ω_b,SAM = 2·A_0·(1−χ) | {OMEGA_B_SAM:.15e} |
| h²_SAM = ω_b / Ω_b | {h_sam_sq:.15e} |
| h_SAM | {h_sam:.15e} |
| **H_0,SAM** | **{H0_sam:.10f} km/s/Mpc** |
| H_0 reference (Planck) | {H_0_REFERENCE_KMS_MPC} km/s/Mpc |
| **H_0 deviation** | **{H0_dev_pct:+.6f} %** |
| **P2 band** | **{p2}** |

## E5 — z_eq cascade (reported only)

| field | value |
|---|---:|
| ω_γ from T_CMB | {omega_gamma:.10e} |
| ω_r with N_eff=3.046 | {omega_r:.10e} |
| ω_m,SAM = Ω_m·h² | {omega_m_sam:.10e} |
| z_eq,SAM | {z_eq_sam:.4f} |
| z_eq Planck (cited; not read) | 3387 ± 20 | |

## Chronology

```text
CR036 is a retrospective substrate-identification CR. It derives eta_SAM
and H_0,SAM from substrate atoms + FIRAS thermal anchor + CODATA 2018 /
SI fixed constants, with zero free parameters and zero CMB-spectrum
input. The runner did not open any Planck spectrum, posterior table,
prior CR result file, or CR035A/CR035A2 artifact. The forbidden-file
open() guard installed at module load did not trip (opened_paths_count
= {len(OPENED_PATHS)}; forbidden_files_opened = false).
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2
Dimensional bridge = T_CMB (FIRAS) + CODATA 2018 / SI fixed constants
External references (numeric, NOT files) = eta_ref 6.119e-10; H_0_ref 67.36
```

---

**Sealed by:** CR036 runner, 2026-06-27.
"""
    (CR_DIR / "CR036_result.md").write_text(result_md, encoding="utf-8")
    print(f"\nWrote artifacts to {CR_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
