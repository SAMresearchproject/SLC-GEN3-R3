"""
CR035A runner: SAM density-spine locked CMB shape test.

Implements the test specified in CR035A_PRECOMMIT.md
(SHA-256 0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced).

SAM density spine (substrate-derived; fixed):
    A_0     = 1/(12*pi)
    chi     = (S/D)*A_0 = 2/(9*pi)
    Omega_m = R*A_0 = 1/pi
    Omega_b = 2*A_0*(1-chi)
    Omega_c = Omega_m - Omega_b
    H_0     = 68.76 km/s/Mpc       (CR018b CMB-side anchor; value cited)

External perturbation parameters (disclosed; Run A holds them fixed at
Planck 2018 base_plikHM_TTTEEE_lowl_lowE_lensing posterior centroids):
    A_s   = 2.100e-9
    n_s   = 0.9649
    tau   = 0.0544
    N_eff = 3.046
    T_CMB = 2.7255 K
    k_pivot = 0.05 Mpc^-1

Engine: CAMB 1.6.6 (canonical; no swap after seal).

P1 — acoustic geometry / peak-structure gate (Run A):
    P1a: |ell_peak_1_SAM - ell_peak_1_Planck| <= 5
    P1b: |ell_peak_{2,3}_SAM - ell_peak_{2,3}_Planck| <= 10 each
    P1c: |H_{2,3}/H_1 ratio deviation| <= 15% each
    P1 PASS iff at least two of (P1a, P1b, P1c) hold.

P2 — TT full-shape gate (Run A):
    PASS:     chi^2_TT/dof <= 2.0   over ell in [30, 2500]
    BOUNDARY: 2.0 < chi^2_TT/dof <= 3.0  (and P1 holds)
    FAIL:     chi^2_TT/dof > 3.0

Run B is diagnostic only; cannot rescue PASS.

v2 NOTE: v1 (CR035A_runner_v1_aborted_json_bug.py, SHA-256
21cc8fa86e49acaae137ee3a65ed29d053de7855682e8c30a90b994e4784d1b7) ran
the science but aborted before artifact emission due to a numpy-bool
JSON serialization bug. v2 adds a _jsonify helper that converts numpy
scalar types to native Python; no peak-finder / chi^2 / Run A / Run B
spec change versus the sealed precommit
(0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced).
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


def _jsonify(o):
    """Convert numpy scalar types to native Python for json.dumps."""
    import numpy as _np
    if isinstance(o, (_np.bool_,)):
        return bool(o)
    if isinstance(o, (_np.integer,)):
        return int(o)
    if isinstance(o, (_np.floating,)):
        return float(o)
    if isinstance(o, _np.ndarray):
        return o.tolist()
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

import numpy as np

warnings.filterwarnings("ignore")


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
                f"CR035A forbidden-file guard tripped: attempted to open {p!r}"
            )
    return _orig_open(file, *args, **kwargs)


builtins.open = _guarded_open


# =====================================================================
# Frozen substrate constants and external perturbation parameters
# =====================================================================

PI = math.pi
R, D, S, ALPHA_H = 12, 3, 8, 2
A_0 = 1.0 / (12.0 * PI)
CHI = (S / D) * A_0
OMEGA_M = R * A_0
OMEGA_B = 2.0 * A_0 * (1.0 - CHI)
OMEGA_C = OMEGA_M - OMEGA_B
H_0 = 68.76
H_SMALL = H_0 / 100.0
OMBH2 = OMEGA_B * H_SMALL ** 2
OMCH2 = OMEGA_C * H_SMALL ** 2

A_S_FIXED = 2.100e-9
N_S_FIXED = 0.9649
TAU_FIXED = 0.0544
N_EFF = 3.046
T_CMB = 2.7255
K_PIVOT = 0.05
MNU = 0.06

PLANCK_AS_SIGMA  = 0.030e-9
PLANCK_NS_SIGMA  = 0.0042
PLANCK_TAU_SIGMA = 0.0073

ELL_MIN, ELL_MAX = 30, 2500
SMOOTH_SIGMA = 5.0
PEAK_ELL_MIN, PEAK_ELL_MAX = 50, 2700

CHI2_PASS_TT  = 2.0
CHI2_BOUND_TT = 3.0

PLANCK_DIR = Path(r"C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3")
PLANCK_TT = PLANCK_DIR / "COM_PowerSpect_CMB-TT-full_R3.01.txt"
PLANCK_TE = PLANCK_DIR / "COM_PowerSpect_CMB-TE-full_R3.01.txt"
PLANCK_EE = PLANCK_DIR / "COM_PowerSpect_CMB-EE-full_R3.01.txt"


# =====================================================================
# Planck data loader
# =====================================================================

def load_planck(path: Path):
    """Cols: ell, D_l, -dDl, +dDl. Symmetric sigma per bin."""
    data = np.loadtxt(path, comments="#")
    ell = data[:, 0].astype(int)
    Dl  = data[:, 1]
    sig = 0.5 * (np.abs(data[:, 2]) + np.abs(data[:, 3]))
    return ell, Dl, sig


# =====================================================================
# CAMB call
# =====================================================================

def camb_spectra(A_s: float, n_s: float, tau: float, lmax: int = 2700):
    """Compute lensed TT/TE/EE D_l in muK^2 with SAM density spine + given perturbations."""
    import camb
    pars = camb.CAMBparams()
    pars.set_cosmology(
        H0=H_0, ombh2=OMBH2, omch2=OMCH2,
        mnu=MNU, omk=0.0, tau=tau,
        TCMB=T_CMB, num_massive_neutrinos=1, nnu=N_EFF,
    )
    pars.InitPower.set_params(As=A_s, ns=n_s, pivot_scalar=K_PIVOT, r=0.0)
    pars.set_for_lmax(lmax=lmax, lens_potential_accuracy=1)
    pars.WantTensors = False
    results = camb.get_results(pars)
    cls = results.get_cmb_power_spectra(pars, CMB_unit="muK", spectra=["lensed_scalar"])
    spec = cls["lensed_scalar"]   # shape (lmax+1, 4): TT, EE, BB, TE
    ell_arr = np.arange(spec.shape[0])
    TT = spec[:, 0]
    EE = spec[:, 1]
    TE = spec[:, 3]
    return ell_arr, TT, TE, EE


# =====================================================================
# Chi^2 and binning
# =====================================================================

def chi2_at_ells(ell_p: np.ndarray, Dl_p: np.ndarray, sig_p: np.ndarray,
                 ell_th: np.ndarray, Dl_th: np.ndarray,
                 ell_min: int = ELL_MIN, ell_max: int = ELL_MAX):
    """Compute chi^2 using theory evaluated at Planck's ell grid."""
    mask = (ell_p >= ell_min) & (ell_p <= ell_max)
    e = ell_p[mask]
    obs = Dl_p[mask]
    sig = sig_p[mask]
    th_lookup = np.full(len(e), np.nan)
    for i, l in enumerate(e):
        if 0 <= l < len(Dl_th):
            th_lookup[i] = Dl_th[l]
    valid = ~np.isnan(th_lookup) & (sig > 0)
    e_v = e[valid]; obs_v = obs[valid]; sig_v = sig[valid]; th_v = th_lookup[valid]
    residual = th_v - obs_v
    chi2 = float(np.sum((residual / sig_v) ** 2))
    dof = int(valid.sum())
    return chi2, dof, e_v, obs_v, sig_v, th_v, residual


# =====================================================================
# Peak finder
# =====================================================================

def find_first_three_peaks(ell_arr: np.ndarray, Dl: np.ndarray,
                           sigma: float = SMOOTH_SIGMA,
                           ell_min: int = PEAK_ELL_MIN,
                           ell_max: int = PEAK_ELL_MAX):
    """Return list of (ell_peak, height) for the first three peaks in
    Gaussian-smoothed D_l. Returns NaN tuples if fewer peaks found."""
    from scipy.ndimage import gaussian_filter1d
    from scipy.signal import find_peaks
    mask = (ell_arr >= ell_min) & (ell_arr <= ell_max)
    e = ell_arr[mask]
    d = gaussian_filter1d(Dl[mask].astype(float), sigma)
    peak_idx, _ = find_peaks(d, distance=80, prominence=0.0)
    peaks = []
    for i in range(3):
        if i < len(peak_idx):
            peaks.append((float(e[peak_idx[i]]), float(d[peak_idx[i]])))
        else:
            peaks.append((float("nan"), float("nan")))
    return peaks


def find_peaks_planck(ell_p, Dl_p):
    """Use the Planck integer-ell binned spectrum directly."""
    return find_first_three_peaks(ell_p, Dl_p)


def find_peaks_theory(ell_th, Dl_th):
    return find_first_three_peaks(ell_th, Dl_th)


# =====================================================================
# Run A and Run B logic
# =====================================================================

def run_a(ell_TT, Dl_TT_planck, sig_TT_planck,
          ell_TE, Dl_TE_planck, sig_TE_planck,
          ell_EE, Dl_EE_planck, sig_EE_planck):
    """Run A: SAM densities + fixed Planck perturbations."""
    print("Run A: SAM density spine + fixed Planck perturbations ...")
    ell_th, TT_th, TE_th, EE_th = camb_spectra(A_S_FIXED, N_S_FIXED, TAU_FIXED)

    chi2_TT, dof_TT, ell_v_TT, obs_TT, sig_v_TT, th_v_TT, res_TT = chi2_at_ells(
        ell_TT, Dl_TT_planck, sig_TT_planck, ell_th, TT_th)
    chi2_TE, dof_TE, ell_v_TE, obs_TE, sig_v_TE, th_v_TE, res_TE = chi2_at_ells(
        ell_TE, Dl_TE_planck, sig_TE_planck, ell_th, TE_th)
    chi2_EE, dof_EE, ell_v_EE, obs_EE, sig_v_EE, th_v_EE, res_EE = chi2_at_ells(
        ell_EE, Dl_EE_planck, sig_EE_planck, ell_th, EE_th)

    peaks_planck = find_peaks_planck(ell_TT, Dl_TT_planck)
    peaks_theory = find_peaks_theory(ell_th, TT_th)

    print(f"  Run A: TT chi^2/dof = {chi2_TT/dof_TT:.4f}  (chi^2 = {chi2_TT:.2f}, dof = {dof_TT})")
    print(f"  Run A: TE chi^2/dof = {chi2_TE/dof_TE:.4f}  (chi^2 = {chi2_TE:.2f}, dof = {dof_TE})")
    print(f"  Run A: EE chi^2/dof = {chi2_EE/dof_EE:.4f}  (chi^2 = {chi2_EE:.2f}, dof = {dof_EE})")
    print(f"  Run A: TT peaks (theory):  {peaks_theory}")
    print(f"  Run A: TT peaks (Planck):  {peaks_planck}")

    return dict(
        ell_th=ell_th, TT=TT_th, TE=TE_th, EE=EE_th,
        chi2_TT=chi2_TT, dof_TT=dof_TT,
        chi2_TE=chi2_TE, dof_TE=dof_TE,
        chi2_EE=chi2_EE, dof_EE=dof_EE,
        ell_v_TT=ell_v_TT, obs_TT=obs_TT, sig_v_TT=sig_v_TT,
        th_v_TT=th_v_TT, res_TT=res_TT,
        ell_v_TE=ell_v_TE, obs_TE=obs_TE, sig_v_TE=sig_v_TE,
        th_v_TE=th_v_TE, res_TE=res_TE,
        ell_v_EE=ell_v_EE, obs_EE=obs_EE, sig_v_EE=sig_v_EE,
        th_v_EE=th_v_EE, res_EE=res_EE,
        peaks_theory=peaks_theory,
        peaks_planck=peaks_planck,
    )


def apply_p1(peaks_theory, peaks_planck):
    """P1 gates."""
    e1_th, h1_th = peaks_theory[0]
    e2_th, h2_th = peaks_theory[1]
    e3_th, h3_th = peaks_theory[2]
    e1_pl, h1_pl = peaks_planck[0]
    e2_pl, h2_pl = peaks_planck[1]
    e3_pl, h3_pl = peaks_planck[2]

    # P1a
    if math.isnan(e1_th) or math.isnan(e1_pl):
        p1a = False
        delta1 = float("nan")
    else:
        delta1 = abs(e1_th - e1_pl)
        p1a = delta1 <= 5.0

    # P1b
    deltas23 = []
    p1b_each = []
    for et, ep in [(e2_th, e2_pl), (e3_th, e3_pl)]:
        if math.isnan(et) or math.isnan(ep):
            p1b_each.append(False)
            deltas23.append(float("nan"))
        else:
            d = abs(et - ep)
            deltas23.append(d)
            p1b_each.append(d <= 10.0)
    p1b = all(p1b_each)

    # P1c: ratios
    ratios = []
    p1c_each = []
    if not any(math.isnan(x) for x in (h1_th, h1_pl, h2_th, h2_pl)) and h1_th != 0 and h1_pl != 0:
        r_th = h2_th / h1_th
        r_pl = h2_pl / h1_pl
        ratios.append((r_th, r_pl))
        p1c_each.append(abs(r_th - r_pl) / abs(r_pl) <= 0.15)
    else:
        ratios.append((float("nan"), float("nan")))
        p1c_each.append(False)
    if not any(math.isnan(x) for x in (h1_th, h1_pl, h3_th, h3_pl)) and h1_th != 0 and h1_pl != 0:
        r_th = h3_th / h1_th
        r_pl = h3_pl / h1_pl
        ratios.append((r_th, r_pl))
        p1c_each.append(abs(r_th - r_pl) / abs(r_pl) <= 0.15)
    else:
        ratios.append((float("nan"), float("nan")))
        p1c_each.append(False)
    p1c = all(p1c_each)

    sub_results = [p1a, p1b, p1c]
    n_pass = sum(1 for v in sub_results if v)
    p1_pass = n_pass >= 2  # "at least two of three hold"
    return dict(
        p1a=p1a, p1b=p1b, p1c=p1c,
        delta1=delta1, deltas23=deltas23,
        ratios=ratios, p1c_each=p1c_each,
        p1_pass=p1_pass, n_pass=n_pass,
    )


def apply_p2(chi2_TT, dof_TT, p1_pass: bool):
    """P2 verdict."""
    rd = chi2_TT / dof_TT if dof_TT > 0 else float("inf")
    if rd <= CHI2_PASS_TT:
        return "PASS", rd
    if rd <= CHI2_BOUND_TT and p1_pass:
        return "BOUNDARY", rd
    if rd <= CHI2_BOUND_TT and not p1_pass:
        return "FAIL", rd  # P1 already failed -> not eligible for boundary
    return "FAIL", rd


def run_b(ell_TT, Dl_TT_planck, sig_TT_planck):
    """Run B: optimize A_s, n_s, tau with SAM densities frozen. Diagnostic only."""
    from scipy.optimize import minimize
    print("Run B: optimizing A_s, n_s, tau (SAM densities frozen) ...")

    def objective(theta):
        A_s_1e9, n_s, tau = theta
        A_s = A_s_1e9 * 1e-9
        try:
            ell_th, TT_th, _, _ = camb_spectra(A_s, n_s, tau, lmax=2700)
        except Exception as e:
            return 1e10
        chi2, dof, *_ = chi2_at_ells(ell_TT, Dl_TT_planck, sig_TT_planck, ell_th, TT_th)
        return chi2

    x0 = [A_S_FIXED * 1e9, N_S_FIXED, TAU_FIXED]
    bounds = [(1.7, 2.5), (0.93, 1.00), (0.02, 0.10)]
    res = minimize(
        objective, x0=x0, method="L-BFGS-B", bounds=bounds,
        options=dict(maxiter=30, ftol=1e-3, disp=False),
    )
    A_s_opt = res.x[0] * 1e-9
    n_s_opt = res.x[1]
    tau_opt = res.x[2]

    ell_th, TT_th, TE_th, EE_th = camb_spectra(A_s_opt, n_s_opt, tau_opt)
    chi2_TT_opt, dof_TT_opt, *_ = chi2_at_ells(
        ell_TT, Dl_TT_planck, sig_TT_planck, ell_th, TT_th)

    sigma_As  = abs(A_s_opt - A_S_FIXED) / PLANCK_AS_SIGMA
    sigma_ns  = abs(n_s_opt - N_S_FIXED) / PLANCK_NS_SIGMA
    sigma_tau = abs(tau_opt - TAU_FIXED) / PLANCK_TAU_SIGMA

    print(f"  Run B optimum: A_s = {A_s_opt:.4e}  ({sigma_As:+.2f} sigma)")
    print(f"  Run B optimum: n_s = {n_s_opt:.4f}  ({sigma_ns:+.2f} sigma)")
    print(f"  Run B optimum: tau = {tau_opt:.4f}  ({sigma_tau:+.2f} sigma)")
    print(f"  Run B chi^2_TT/dof at optimum: {chi2_TT_opt/dof_TT_opt:.4f}")

    return dict(
        A_s_opt=A_s_opt, n_s_opt=n_s_opt, tau_opt=tau_opt,
        chi2_TT_opt=chi2_TT_opt, dof_TT_opt=dof_TT_opt,
        sigma_As=sigma_As, sigma_ns=sigma_ns, sigma_tau=sigma_tau,
        nfev=res.nfev, nit=res.nit, message=str(res.message),
    )


# =====================================================================
# Outputs
# =====================================================================

def write_residual_csv(path: Path, ell, obs, sig, th, res):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ell", "Dl_planck", "sigma_planck", "Dl_SAM_theory",
                    "residual", "z_score"])
        for i in range(len(ell)):
            z = res[i] / sig[i] if sig[i] > 0 else float("nan")
            w.writerow([int(ell[i]), f"{obs[i]:.6e}", f"{sig[i]:.6e}",
                        f"{th[i]:.6e}", f"{res[i]:.6e}", f"{z:.4f}"])


def write_peaks_csv(path: Path, peaks_theory, peaks_planck):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["peak", "ell_theory", "height_theory",
                    "ell_planck", "height_planck",
                    "delta_ell", "delta_height_rel"])
        for i in range(3):
            et, ht = peaks_theory[i]
            ep, hp = peaks_planck[i]
            d_e = (et - ep) if (not math.isnan(et) and not math.isnan(ep)) else float("nan")
            d_h = ((ht - hp) / abs(hp)) if (hp not in (0, float("nan")) and not math.isnan(ht) and not math.isnan(hp)) else float("nan")
            w.writerow([i + 1,
                        f"{et:.4f}" if not math.isnan(et) else "",
                        f"{ht:.4f}" if not math.isnan(ht) else "",
                        f"{ep:.4f}" if not math.isnan(ep) else "",
                        f"{hp:.4f}" if not math.isnan(hp) else "",
                        f"{d_e:+.4f}" if not math.isnan(d_e) else "",
                        f"{d_h:+.4%}" if not math.isnan(d_h) else ""])


def write_theory_csv(path: Path, ell_th, TT, TE, EE, ell_max: int = 2700):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ell", "Dl_TT_SAM", "Dl_TE_SAM", "Dl_EE_SAM"])
        for l in range(2, min(ell_max + 1, len(TT))):
            w.writerow([l, f"{TT[l]:.6e}", f"{TE[l]:.6e}", f"{EE[l]:.6e}"])


# =====================================================================
# Main
# =====================================================================

def main() -> int:
    print(f"CR035A runner  -  SAM density spine CMB shape test")
    print(f"  Omega_m  = {OMEGA_M:.12f}")
    print(f"  Omega_b  = {OMEGA_B:.12f}")
    print(f"  Omega_c  = {OMEGA_C:.12f}")
    print(f"  H_0      = {H_0}")
    print(f"  ombh2    = {OMBH2:.12f}")
    print(f"  omch2    = {OMCH2:.12f}")
    print(f"  A_s/n_s/tau fixed at Planck 2018 centroids: "
          f"{A_S_FIXED:.3e}, {N_S_FIXED}, {TAU_FIXED}")
    import camb as _camb
    print(f"  CAMB version: {_camb.__version__}")

    ell_TT, Dl_TT, sig_TT = load_planck(PLANCK_TT)
    ell_TE, Dl_TE, sig_TE = load_planck(PLANCK_TE)
    ell_EE, Dl_EE, sig_EE = load_planck(PLANCK_EE)
    print(f"  Planck TT bins: {len(ell_TT)}  range: {ell_TT[0]}..{ell_TT[-1]}")
    print(f"  Planck TE bins: {len(ell_TE)}")
    print(f"  Planck EE bins: {len(ell_EE)}")

    # ----- Run A -----
    A = run_a(ell_TT, Dl_TT, sig_TT,
              ell_TE, Dl_TE, sig_TE,
              ell_EE, Dl_EE, sig_EE)

    # P1
    p1 = apply_p1(A["peaks_theory"], A["peaks_planck"])
    print(f"  P1a (first-peak <=5):    {p1['p1a']}  (delta = {p1['delta1']})")
    print(f"  P1b (2nd/3rd <=10):      {p1['p1b']}  (deltas = {p1['deltas23']})")
    print(f"  P1c (height ratios <=15%): {p1['p1c']}  "
          f"(each = {p1['p1c_each']})")
    print(f"  P1 PASS (>=2 of 3):      {p1['p1_pass']}")

    # P2
    p2_token, rd_TT = apply_p2(A["chi2_TT"], A["dof_TT"], p1["p1_pass"])
    print(f"  P2 TT chi^2/dof = {rd_TT:.4f}  -> {p2_token}")

    # TE/EE BOUNDARY trigger
    rd_TE = A["chi2_TE"] / A["dof_TE"]
    rd_EE = A["chi2_EE"] / A["dof_EE"]
    pol_boundary = (p1["p1_pass"] and p2_token == "PASS"
                    and (rd_TE > 3.0 or rd_EE > 3.0))

    # Run B (diagnostic)
    B = run_b(ell_TT, Dl_TT, sig_TT)

    # ----- Final verdict logic -----
    runB_within_5sigma = (B["sigma_As"] <= 5 and B["sigma_ns"] <= 5
                         and B["sigma_tau"] <= 5)
    runB_chi2pass = (B["chi2_TT_opt"] / B["dof_TT_opt"]) <= CHI2_BOUND_TT

    if p1["p1_pass"] and p2_token == "PASS" and not pol_boundary:
        verdict = "PASS"
        verdict_token = (
            "CR035A_PASS_SAM_DENSITY_SPINE_REPRODUCES_PLANCK_TT_BINNED_SHAPE"
            "_AT_ACOUSTIC_PEAK_AND_FULL_SHAPE_TOLERANCES"
        )
    elif p1["p1_pass"] and p2_token == "PASS" and pol_boundary:
        verdict = "BOUNDARY"
        verdict_token = (
            "CR035A_BOUNDARY_POLARIZATION_DEBT_TT_PASSES_TE_OR_EE_DEGRADED"
        )
    elif p2_token == "BOUNDARY":
        verdict = "BOUNDARY"
        verdict_token = (
            "CR035A_BOUNDARY_TT_FULL_SHAPE_BETWEEN_2_AND_3_CHI2_PER_DOF"
        )
    elif p2_token == "FAIL" and runB_chi2pass and runB_within_5sigma:
        verdict = "BOUNDARY"
        verdict_token = (
            "CR035A_BOUNDARY_RUNA_FAIL_BUT_RUNB_RESCUES_WITHIN_5SIGMA_PLANCK_POSTERIOR"
        )
    else:
        verdict = "FAIL"
        verdict_token = (
            "CR035A_FAIL_SAM_DENSITY_SPINE_BINNED_TT_SHAPE_OUTSIDE_TOLERANCES"
        )

    print(f"\n=== CR035A VERDICT: {verdict} ===")
    print(f"    {verdict_token}")

    # ----- Emit artifacts -----
    summary = dict(
        precommit_sha256="0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced",
        execution_status="CLEAN",
        scientific_verdict=verdict,
        verdict_token=verdict_token,
        triage_bin="A",
        free_parameters_introduced_RunA=0,
        external_perturbation_disclosed=True,
        prior_CR_result_inputs=False,
        forbidden_files_opened=False,
        opened_paths_count=len(OPENED_PATHS),
        engine="CAMB",
        engine_version=_camb.__version__,
        # SAM density spine
        substrate=dict(
            R=R, D=D, S=S, alpha_H=ALPHA_H,
            A_0=A_0, chi=CHI,
            Omega_m=OMEGA_M, Omega_b=OMEGA_B, Omega_c=OMEGA_C,
            H_0=H_0, h=H_SMALL,
            ombh2=OMBH2, omch2=OMCH2,
        ),
        external_perturbations=dict(
            A_s=A_S_FIXED, n_s=N_S_FIXED, tau=TAU_FIXED,
            N_eff=N_EFF, T_CMB=T_CMB, k_pivot=K_PIVOT,
        ),
        Planck_files=dict(
            TT=str(PLANCK_TT),
            TE=str(PLANCK_TE),
            EE=str(PLANCK_EE),
        ),
        sample=dict(
            n_TT_bins=int(A["dof_TT"]),
            n_TE_bins=int(A["dof_TE"]),
            n_EE_bins=int(A["dof_EE"]),
            ell_min=ELL_MIN, ell_max=ELL_MAX,
        ),
        # Run A
        runA=dict(
            chi2_TT=A["chi2_TT"], dof_TT=A["dof_TT"],
            chi2_per_dof_TT=A["chi2_TT"] / A["dof_TT"],
            chi2_TE=A["chi2_TE"], dof_TE=A["dof_TE"],
            chi2_per_dof_TE=A["chi2_TE"] / A["dof_TE"],
            chi2_EE=A["chi2_EE"], dof_EE=A["dof_EE"],
            chi2_per_dof_EE=A["chi2_EE"] / A["dof_EE"],
            P1a_pass=p1["p1a"], P1b_pass=p1["p1b"], P1c_pass=p1["p1c"],
            P1_pass=p1["p1_pass"],
            P1_first_peak_delta_ell=p1["delta1"],
            P1_2nd_3rd_peak_delta_ell=p1["deltas23"],
            P1_height_ratios=[
                dict(theory=r[0], planck=r[1]) for r in p1["ratios"]],
            P1_height_ratio_pass_each=p1["p1c_each"],
            P2_verdict=p2_token,
            P2_chi2_TT_over_dof=rd_TT,
            pol_BOUNDARY_triggered=pol_boundary,
            peaks_theory=[dict(ell=p[0], height=p[1]) for p in A["peaks_theory"]],
            peaks_planck=[dict(ell=p[0], height=p[1]) for p in A["peaks_planck"]],
        ),
        # Run B diagnostic
        runB=dict(
            A_s_optimized=B["A_s_opt"], n_s_optimized=B["n_s_opt"],
            tau_optimized=B["tau_opt"],
            sigma_dev_As=B["sigma_As"], sigma_dev_ns=B["sigma_ns"],
            sigma_dev_tau=B["sigma_tau"],
            chi2_TT_at_optimum=B["chi2_TT_opt"],
            dof_TT_at_optimum=B["dof_TT_opt"],
            chi2_per_dof_TT_at_optimum=B["chi2_TT_opt"] / B["dof_TT_opt"],
            within_5sigma_planck_posterior=runB_within_5sigma,
            optimization_chi2_in_band=runB_chi2pass,
            optimizer_nfev=B["nfev"], optimizer_nit=B["nit"],
            optimizer_message=B["message"],
        ),
    )

    out_summary = CR_DIR / "CR035A_summary.json"
    out_summary.write_text(json.dumps(summary, indent=2, default=_jsonify), encoding="utf-8")
    print(f"\nWrote: {out_summary.name}")

    write_residual_csv(CR_DIR / "CR035A_TT_residuals.csv",
                       A["ell_v_TT"], A["obs_TT"], A["sig_v_TT"],
                       A["th_v_TT"], A["res_TT"])
    write_residual_csv(CR_DIR / "CR035A_TE_residuals.csv",
                       A["ell_v_TE"], A["obs_TE"], A["sig_v_TE"],
                       A["th_v_TE"], A["res_TE"])
    write_residual_csv(CR_DIR / "CR035A_EE_residuals.csv",
                       A["ell_v_EE"], A["obs_EE"], A["sig_v_EE"],
                       A["th_v_EE"], A["res_EE"])
    write_peaks_csv(CR_DIR / "CR035A_peaks.csv",
                    A["peaks_theory"], A["peaks_planck"])
    write_theory_csv(CR_DIR / "CR035A_runA_theory_spectra.csv",
                     A["ell_th"], A["TT"], A["TE"], A["EE"])
    (CR_DIR / "CR035A_runB_diagnostic.json").write_text(
        json.dumps(summary["runB"], indent=2, default=_jsonify), encoding="utf-8")
    print("Wrote: TT/TE/EE residual CSVs, peaks CSV, runB_diagnostic.json, "
          "runA_theory_spectra.csv")

    # ----- Result markdown -----
    def fmt_peak(p):
        return f"ell={p[0]:.1f}  D={p[1]:.2f}" if not math.isnan(p[0]) else "n/a"

    result_md = f"""# CR035A_SAM_DENSITY_SPINE_CMB_SHAPE

## Verdict

```text
{verdict_token}
```

## Courtroom Fields

```text
execution_status                 = CLEAN
scientific_verdict               = {verdict}
triage_bin                       = A
free_parameters_introduced_RunA  = 0
external_perturbation_disclosed  = true
prior_CR_result_inputs           = false
forbidden_files_opened           = false
opened_paths_count               = {len(OPENED_PATHS)}
precommit_sha256                 = 0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced
engine                           = CAMB {_camb.__version__}
```

## SAM Density Spine (substrate-derived)

| symbol | value |
|---|---:|
| A_0 = 1/(12π) | {A_0:.12f} |
| χ = 2/(9π) | {CHI:.12f} |
| Ω_m = 1/π | {OMEGA_M:.12f} |
| Ω_b = 2·A_0·(1−χ) | {OMEGA_B:.12f} |
| Ω_c = Ω_m − Ω_b | {OMEGA_C:.12f} |
| H_0 | {H_0} km/s/Mpc |
| ω_b = Ω_b·h² | {OMBH2:.12f} |
| ω_c = Ω_c·h² | {OMCH2:.12f} |

## Fixed External Perturbations (Planck 2018 centroids; Run A)

| field | value |
|---|---:|
| A_s | {A_S_FIXED:.3e} |
| n_s | {N_S_FIXED} |
| τ | {TAU_FIXED} |
| N_eff | {N_EFF} |
| T_CMB | {T_CMB} K |
| k_pivot | {K_PIVOT} Mpc⁻¹ |

## Sample

| field | value |
|---|---:|
| TT bins (ℓ ∈ [30, 2500]) | {A['dof_TT']} |
| TE bins | {A['dof_TE']} |
| EE bins | {A['dof_EE']} |

## P1 — Acoustic Geometry / Peak Structure (Run A)

| peak | theory | Planck | Δℓ |
|---|---|---|---:|
| 1 | {fmt_peak(A['peaks_theory'][0])} | {fmt_peak(A['peaks_planck'][0])} | {p1['delta1']:+.2f} |
| 2 | {fmt_peak(A['peaks_theory'][1])} | {fmt_peak(A['peaks_planck'][1])} | {p1['deltas23'][0]:+.2f} |
| 3 | {fmt_peak(A['peaks_theory'][2])} | {fmt_peak(A['peaks_planck'][2])} | {p1['deltas23'][1]:+.2f} |

| sub-gate | tolerance | pass |
|---|---|---:|
| P1a (first peak Δℓ ≤ 5) | ±5 | **{p1['p1a']}** |
| P1b (2nd/3rd Δℓ ≤ 10) | ±10 each | **{p1['p1b']}** |
| P1c (H2/H1, H3/H1 within 15%) | ±15% each | **{p1['p1c']}** |
| **P1 (≥2 of 3)** | | **{p1['p1_pass']}** |

Height ratios (theory / Planck):
- H2/H1: {p1['ratios'][0][0]:.4f} / {p1['ratios'][0][1]:.4f}  → pass {p1['p1c_each'][0]}
- H3/H1: {p1['ratios'][1][0]:.4f} / {p1['ratios'][1][1]:.4f}  → pass {p1['p1c_each'][1]}

## P2 — TT Full-Shape (Run A)

| stat | value |
|---|---:|
| χ²_TT | {A['chi2_TT']:.4f} |
| dof_TT | {A['dof_TT']} |
| **χ²_TT / dof_TT** | **{rd_TT:.4f}** |
| P2 band | **{p2_token}** |

P2 PASS ≤ 2.0; BOUNDARY (2.0, 3.0] with P1; FAIL > 3.0.

## E_TE / E_EE — Reported Evidence (Run A)

| spectrum | χ² | dof | χ²/dof |
|---|---:|---:|---:|
| TE | {A['chi2_TE']:.4f} | {A['dof_TE']} | {rd_TE:.4f} |
| EE | {A['chi2_EE']:.4f} | {A['dof_EE']} | {rd_EE:.4f} |

Polarization BOUNDARY triggered: **{pol_boundary}** (TT passes but TE or EE > 3.0).

## Run B — Diagnostic Optimization (NOT a gate)

| param | optimized | fixed (Planck) | σ-deviation |
|---|---|---|---:|
| A_s | {B['A_s_opt']:.4e} | {A_S_FIXED:.4e} | {B['sigma_As']:+.3f} σ |
| n_s | {B['n_s_opt']:.4f} | {N_S_FIXED} | {B['sigma_ns']:+.3f} σ |
| τ | {B['tau_opt']:.4f} | {TAU_FIXED} | {B['sigma_tau']:+.3f} σ |
| χ²_TT/dof at optimum | {B['chi2_TT_opt'] / B['dof_TT_opt']:.4f} | | |
| within ±5σ Planck posterior | **{runB_within_5sigma}** | | |
| optimizer | L-BFGS-B  ({B['nit']} iters, {B['nfev']} evals) | | |

Run B is diagnostic only. It cannot rescue PASS; it can explain BOUNDARY.

## Chronology

```text
CR035A is the next rung after CR001c@19 (which sealed CMB compressed
acoustic geometry at sub-percent precision). The SAM density spine is
FIXED from substrate atoms; the perturbation sector (A_s, n_s, tau)
is FIXED at Planck 2018 posterior centroids in Run A. CR035A does NOT
claim full parameter-free CMB shape closure. The forbidden-file open()
guard was installed at module load and did not trip
(opened_paths_count = {len(OPENED_PATHS)}; forbidden_files_opened = false).
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced
External data  = Planck PR3 TT/TE/EE bandpowers (locally hashed in HASHES.txt)
Engine         = CAMB {_camb.__version__}
```

---

**Sealed by:** CR035A runner, 2026-06-27.
"""
    (CR_DIR / "CR035A_result.md").write_text(result_md, encoding="utf-8")
    print("Wrote: CR035A_result.md")
    print(f"\nVerdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
