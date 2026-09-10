"""
CR035A2 runner: peak-finder + verdict-mapping audit appeal of CR035A.

Implements the test specified in CR035A2_PRECOMMIT.md
(SHA-256 6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697).

Same SAM density spine, same fixed Planck perturbations, same CAMB engine,
same Planck PR3 data files, same chi^2 / dof / tolerances / Run B bounds
as CR035A. Only the peak finder and the verdict-mapping tree change.

Changes vs CR035A:
  1. Peak finder (NEW):
       Per-peak ell windows:
         Peak 1: [150, 300]
         Peak 2: [400, 650]
         Peak 3: [700, 900]
       Minimum prominence: >= 50 muK^2.
       Heights H_i are read from the SAME sigma_ell=5 Gaussian-smoothed
       D_l curve used for peak detection.
       No peak meeting prominence inside its window -> "not detected",
       and the corresponding sub-gate FAILS.
  2. Verdict-mapping tree (NEW):
       Fully written elif tree per Verdict Ladder in precommit.
       BOUNDARY (iii) requires Run B TT/dof <= 3.0 AND TE/dof <= 5.0
       AND EE/dof <= 5.0 AND |sigma_dev| <= 5 sigma for A_s, n_s, tau.
       (Polarization sanity guard prevents TT-only rescue.)
  3. Forbidden-file guard (EXPANDED):
       Now also forbids all CR035A family files and the CR035A runners.

CR035A v2 strict FAIL stands sealed and is NOT overwritten.
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

import numpy as np

warnings.filterwarnings("ignore")


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


# =====================================================================
# Strict input discipline: forbidden-file open() guard (EXPANDED)
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
    # CR035A family
    re.compile(r"CR035A_summary\.json$",                  re.IGNORECASE),
    re.compile(r"CR035A_result\.md$",                     re.IGNORECASE),
    re.compile(r"CR035A_(TT|TE|EE)_residuals\.csv$",      re.IGNORECASE),
    re.compile(r"CR035A_peaks\.csv$",                     re.IGNORECASE),
    re.compile(r"CR035A_runB_diagnostic\.json$",          re.IGNORECASE),
    re.compile(r"CR035A_runA_theory_spectra\.csv$",       re.IGNORECASE),
    re.compile(r"CR035A_runner.*\.py$",                   re.IGNORECASE),
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
                f"CR035A2 forbidden-file guard tripped: attempted to open {p!r}"
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

# NEW peak finder spec
SMOOTH_SIGMA = 5.0
PEAK_PROMINENCE = 50.0
PEAK_WINDOWS = [(150, 300), (400, 650), (700, 900)]

CHI2_PASS_TT  = 2.0
CHI2_BOUND_TT = 3.0
CHI2_POL_DEBT_RUNA = 3.0      # polarization debt threshold in Run A
CHI2_POL_SANITY_RUNB = 5.0    # polarization sanity guard in Run B

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
# Chi^2 and binning (unchanged from CR035A)
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
# Peak finder — NEW: per-peak windows + minimum prominence
# =====================================================================

def smooth_Dl(ell_arr: np.ndarray, Dl: np.ndarray,
              sigma: float = SMOOTH_SIGMA,
              ell_lo: int = 50, ell_hi: int = 2700):
    """Return (ell_sub, D_l_smooth) on ell in [ell_lo, ell_hi]."""
    from scipy.ndimage import gaussian_filter1d
    mask = (ell_arr >= ell_lo) & (ell_arr <= ell_hi)
    e = ell_arr[mask]
    d_smooth = gaussian_filter1d(Dl[mask].astype(float), sigma)
    return e, d_smooth


def find_peaks_in_windows(ell_smooth: np.ndarray, Dl_smooth: np.ndarray,
                          windows=PEAK_WINDOWS,
                          prominence: float = PEAK_PROMINENCE):
    """For each (lo, hi) window: find peaks on smoothed curve with
    prominence >= threshold; select the single highest-prominence peak
    inside the window. Heights H_i are read from the same smoothed curve
    at the detected peak ell.
    Returns list of length len(windows); each entry is (ell_peak, H_i,
    detected_flag, prominence_value). detected_flag is False if no peak
    meeting prominence found inside the window; in that case ell_peak,
    H_i, prominence are nan.
    """
    from scipy.signal import find_peaks
    # Find ALL peaks on the smoothed curve with the prominence floor
    peak_idx, props = find_peaks(Dl_smooth, prominence=prominence)
    prominences = props["prominences"]
    peak_ells = ell_smooth[peak_idx]
    peak_heights = Dl_smooth[peak_idx]

    results = []
    for (lo, hi) in windows:
        in_window = (peak_ells >= lo) & (peak_ells <= hi)
        if not np.any(in_window):
            results.append((float("nan"), float("nan"), False, float("nan")))
            continue
        win_idx = np.where(in_window)[0]
        # Select highest-prominence peak inside window;
        # break ties by larger ell.
        best = win_idx[0]
        for ii in win_idx[1:]:
            if prominences[ii] > prominences[best]:
                best = ii
            elif prominences[ii] == prominences[best] and peak_ells[ii] > peak_ells[best]:
                best = ii
        results.append((
            float(peak_ells[best]),
            float(peak_heights[best]),    # H_i from smoothed curve
            True,
            float(prominences[best]),
        ))
    return results


# =====================================================================
# Run A and Run B
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

    # Smooth both theory and Planck on ell in [50, 2700]
    ell_th_sub, TT_th_smooth = smooth_Dl(ell_th, TT_th)
    ell_pl_sub, TT_pl_smooth = smooth_Dl(ell_TT, Dl_TT_planck)

    peaks_theory = find_peaks_in_windows(ell_th_sub, TT_th_smooth)
    peaks_planck = find_peaks_in_windows(ell_pl_sub, TT_pl_smooth)

    print(f"  Run A: TT chi^2/dof = {chi2_TT/dof_TT:.4f}  (chi^2 = {chi2_TT:.2f}, dof = {dof_TT})")
    print(f"  Run A: TE chi^2/dof = {chi2_TE/dof_TE:.4f}  (chi^2 = {chi2_TE:.2f}, dof = {dof_TE})")
    print(f"  Run A: EE chi^2/dof = {chi2_EE/dof_EE:.4f}  (chi^2 = {chi2_EE:.2f}, dof = {dof_EE})")
    print(f"  TT peaks (theory, with prominence>=50, in windows):")
    for i, p in enumerate(peaks_theory):
        if p[2]:
            print(f"    P{i+1}: ell={p[0]:.1f}  H={p[1]:.2f}  prom={p[3]:.2f}")
        else:
            print(f"    P{i+1}: NOT DETECTED in window")
    print(f"  TT peaks (Planck, with prominence>=50, in windows):")
    for i, p in enumerate(peaks_planck):
        if p[2]:
            print(f"    P{i+1}: ell={p[0]:.1f}  H={p[1]:.2f}  prom={p[3]:.2f}")
        else:
            print(f"    P{i+1}: NOT DETECTED in window")

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
    """P1 gates with corrected per-peak window + smoothed-curve heights."""
    e1_th, h1_th, det1_th, _ = peaks_theory[0]
    e2_th, h2_th, det2_th, _ = peaks_theory[1]
    e3_th, h3_th, det3_th, _ = peaks_theory[2]
    e1_pl, h1_pl, det1_pl, _ = peaks_planck[0]
    e2_pl, h2_pl, det2_pl, _ = peaks_planck[1]
    e3_pl, h3_pl, det3_pl, _ = peaks_planck[2]

    # P1a
    if det1_th and det1_pl:
        delta1 = abs(e1_th - e1_pl)
        p1a = delta1 <= 5.0
    else:
        p1a = False
        delta1 = float("nan")

    # P1b
    deltas23 = []
    p1b_each = []
    for et, ep, det_t, det_p in [
        (e2_th, e2_pl, det2_th, det2_pl),
        (e3_th, e3_pl, det3_th, det3_pl),
    ]:
        if det_t and det_p:
            d = abs(et - ep)
            deltas23.append(d)
            p1b_each.append(d <= 10.0)
        else:
            deltas23.append(float("nan"))
            p1b_each.append(False)
    p1b = all(p1b_each)

    # P1c — heights H_i from smoothed curve
    ratios = []
    p1c_each = []
    # H2/H1
    if det1_th and det2_th and det1_pl and det2_pl and h1_th != 0 and h1_pl != 0:
        r_th = h2_th / h1_th
        r_pl = h2_pl / h1_pl
        ratios.append((r_th, r_pl))
        p1c_each.append(abs(r_th - r_pl) / abs(r_pl) <= 0.15)
    else:
        ratios.append((float("nan"), float("nan")))
        p1c_each.append(False)
    # H3/H1
    if det1_th and det3_th and det1_pl and det3_pl and h1_th != 0 and h1_pl != 0:
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
    p1_pass = n_pass >= 2
    return dict(
        p1a=p1a, p1b=p1b, p1c=p1c,
        delta1=delta1, deltas23=deltas23,
        ratios=ratios, p1c_each=p1c_each,
        p1_pass=p1_pass, n_pass=n_pass,
    )


def p2_band(chi2_TT, dof_TT):
    """Return one of 'PASS' / 'BOUNDARY' / 'FAIL' for P2."""
    rd = chi2_TT / dof_TT if dof_TT > 0 else float("inf")
    if rd <= CHI2_PASS_TT:
        return "PASS", rd
    if rd <= CHI2_BOUND_TT:
        return "BOUNDARY", rd
    return "FAIL", rd


def run_b(ell_TT, Dl_TT_planck, sig_TT_planck,
          ell_TE, Dl_TE_planck, sig_TE_planck,
          ell_EE, Dl_EE_planck, sig_EE_planck):
    """Run B: optimize A_s, n_s, tau with SAM densities frozen.
    Also report TE/EE chi^2/dof at the optimum for the polarization sanity guard."""
    from scipy.optimize import minimize
    print("Run B: optimizing A_s, n_s, tau (SAM densities frozen) ...")

    def objective(theta):
        A_s_1e9, n_s, tau = theta
        A_s = A_s_1e9 * 1e-9
        try:
            ell_th, TT_th, _, _ = camb_spectra(A_s, n_s, tau, lmax=2700)
        except Exception:
            return 1e10
        chi2, dof, *_ = chi2_at_ells(ell_TT, Dl_TT_planck, sig_TT_planck, ell_th, TT_th)
        if dof == 0:
            return 1e10
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

    # Compute spectra at optimum, then TT/TE/EE chi^2 + dof
    ell_th, TT_th, TE_th, EE_th = camb_spectra(A_s_opt, n_s_opt, tau_opt)
    chi2_TT_opt, dof_TT_opt, *_ = chi2_at_ells(
        ell_TT, Dl_TT_planck, sig_TT_planck, ell_th, TT_th)
    chi2_TE_opt, dof_TE_opt, *_ = chi2_at_ells(
        ell_TE, Dl_TE_planck, sig_TE_planck, ell_th, TE_th)
    chi2_EE_opt, dof_EE_opt, *_ = chi2_at_ells(
        ell_EE, Dl_EE_planck, sig_EE_planck, ell_th, EE_th)

    sigma_As  = (A_s_opt - A_S_FIXED) / PLANCK_AS_SIGMA
    sigma_ns  = (n_s_opt - N_S_FIXED) / PLANCK_NS_SIGMA
    sigma_tau = (tau_opt - TAU_FIXED) / PLANCK_TAU_SIGMA

    print(f"  Run B optimum: A_s = {A_s_opt:.4e}  ({sigma_As:+.3f} sigma)")
    print(f"  Run B optimum: n_s = {n_s_opt:.4f}  ({sigma_ns:+.3f} sigma)")
    print(f"  Run B optimum: tau = {tau_opt:.4f}  ({sigma_tau:+.3f} sigma)")
    print(f"  Run B chi^2/dof  TT = {chi2_TT_opt/dof_TT_opt:.4f}")
    print(f"  Run B chi^2/dof  TE = {chi2_TE_opt/dof_TE_opt:.4f}")
    print(f"  Run B chi^2/dof  EE = {chi2_EE_opt/dof_EE_opt:.4f}")

    return dict(
        A_s_opt=A_s_opt, n_s_opt=n_s_opt, tau_opt=tau_opt,
        chi2_TT_opt=chi2_TT_opt, dof_TT_opt=dof_TT_opt,
        chi2_TE_opt=chi2_TE_opt, dof_TE_opt=dof_TE_opt,
        chi2_EE_opt=chi2_EE_opt, dof_EE_opt=dof_EE_opt,
        sigma_As=sigma_As, sigma_ns=sigma_ns, sigma_tau=sigma_tau,
        nfev=res.nfev, nit=res.nit, message=str(res.message),
        converged=bool(res.success),
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
        w.writerow(["peak", "window_low", "window_high",
                    "ell_theory", "H_theory_smoothed", "prom_theory", "detected_theory",
                    "ell_planck", "H_planck_smoothed", "prom_planck", "detected_planck",
                    "delta_ell", "delta_height_rel"])
        for i in range(3):
            lo, hi = PEAK_WINDOWS[i]
            et, ht, det_t, prom_t = peaks_theory[i]
            ep, hp, det_p, prom_p = peaks_planck[i]
            if det_t and det_p:
                d_e = et - ep
                d_h = (ht - hp) / abs(hp) if hp != 0 else float("nan")
            else:
                d_e = float("nan")
                d_h = float("nan")
            w.writerow([i + 1, lo, hi,
                        f"{et:.4f}" if det_t else "",
                        f"{ht:.4f}" if det_t else "",
                        f"{prom_t:.4f}" if det_t else "",
                        det_t,
                        f"{ep:.4f}" if det_p else "",
                        f"{hp:.4f}" if det_p else "",
                        f"{prom_p:.4f}" if det_p else "",
                        det_p,
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
    print(f"CR035A2 runner  -  peak-finder + verdict-mapping audit appeal of CR035A")
    print(f"  Omega_m  = {OMEGA_M:.12f}")
    print(f"  Omega_b  = {OMEGA_B:.12f}")
    print(f"  Omega_c  = {OMEGA_C:.12f}")
    print(f"  H_0      = {H_0}")
    print(f"  ombh2    = {OMBH2:.12f}")
    print(f"  omch2    = {OMCH2:.12f}")
    print(f"  A_s/n_s/tau fixed: {A_S_FIXED:.3e}, {N_S_FIXED}, {TAU_FIXED}")
    print(f"  Peak windows: {PEAK_WINDOWS}; prominence >= {PEAK_PROMINENCE} muK^2")
    import camb as _camb
    print(f"  CAMB version: {_camb.__version__}")

    ell_TT, Dl_TT, sig_TT = load_planck(PLANCK_TT)
    ell_TE, Dl_TE, sig_TE = load_planck(PLANCK_TE)
    ell_EE, Dl_EE, sig_EE = load_planck(PLANCK_EE)
    print(f"  Planck TT bins: {len(ell_TT)}  range: {ell_TT[0]}..{ell_TT[-1]}")

    # ----- Run A -----
    A = run_a(ell_TT, Dl_TT, sig_TT,
              ell_TE, Dl_TE, sig_TE,
              ell_EE, Dl_EE, sig_EE)

    # P1
    p1 = apply_p1(A["peaks_theory"], A["peaks_planck"])
    print(f"  P1a (first-peak <=5):  {p1['p1a']}  (delta = {p1['delta1']})")
    print(f"  P1b (2nd/3rd <=10):    {p1['p1b']}  (deltas = {p1['deltas23']})")
    print(f"  P1c (H ratios <=15%):  {p1['p1c']}  (each = {p1['p1c_each']})")
    print(f"  P1 PASS (>=2 of 3):    {p1['p1_pass']}")

    # P2
    p2_token, rd_TT = p2_band(A["chi2_TT"], A["dof_TT"])
    print(f"  P2 TT chi^2/dof = {rd_TT:.4f}  -> {p2_token}")

    # Polarization debt at Run A
    rd_TE = A["chi2_TE"] / A["dof_TE"]
    rd_EE = A["chi2_EE"] / A["dof_EE"]
    pol_debt = (rd_TE > CHI2_POL_DEBT_RUNA) or (rd_EE > CHI2_POL_DEBT_RUNA)

    # Run B (diagnostic)
    B = run_b(ell_TT, Dl_TT, sig_TT,
              ell_TE, Dl_TE, sig_TE,
              ell_EE, Dl_EE, sig_EE)
    rd_TT_B = B["chi2_TT_opt"] / B["dof_TT_opt"]
    rd_TE_B = B["chi2_TE_opt"] / B["dof_TE_opt"]
    rd_EE_B = B["chi2_EE_opt"] / B["dof_EE_opt"]

    # ----- Verdict tree (exactly as walked in chat) -----
    if p1["p1_pass"] and p2_token == "PASS":
        if pol_debt:
            verdict = "BOUNDARY"
            verdict_case = "ii_polarization_debt"
            verdict_token = (
                "CR035A2_BOUNDARY_POLARIZATION_DEBT_TT_PASSES_TE_OR_EE_DEGRADED"
            )
        else:
            verdict = "PASS"
            verdict_case = "PASS"
            verdict_token = (
                "CR035A2_PASS_SAM_DENSITY_SPINE_REPRODUCES_PLANCK_TT_FULL_PER_MULTIPOLE_SHAPE"
                "_AT_PEAK_AND_FULL_SHAPE_TOLERANCES"
            )
    elif p1["p1_pass"] and p2_token == "BOUNDARY":
        verdict = "BOUNDARY"
        verdict_case = "i_full_shape_marginal"
        verdict_token = (
            "CR035A2_BOUNDARY_TT_FULL_SHAPE_BETWEEN_2_AND_3_CHI2_PER_DOF"
        )
    else:
        # Run A overall not-PASS. Try BOUNDARY (iii) rescue.
        rescue = (
            B["converged"]
            and rd_TT_B <= CHI2_BOUND_TT
            and rd_TE_B <= CHI2_POL_SANITY_RUNB
            and rd_EE_B <= CHI2_POL_SANITY_RUNB
            and abs(B["sigma_As"])  <= 5.0
            and abs(B["sigma_ns"])  <= 5.0
            and abs(B["sigma_tau"]) <= 5.0
        )
        if rescue:
            verdict = "BOUNDARY"
            verdict_case = "iii_runB_rescue_within_5sigma_polarization_sane"
            verdict_token = (
                "CR035A2_BOUNDARY_RUNA_NOT_PASS_BUT_RUNB_RESCUES_WITHIN_5SIGMA_PLANCK_POSTERIOR"
                "_AND_POLARIZATION_SANE"
            )
        else:
            verdict = "FAIL"
            verdict_case = "FAIL"
            verdict_token = (
                "CR035A2_FAIL_SAM_DENSITY_SPINE_FULL_PER_MULTIPOLE_SHAPE_OUTSIDE_TOLERANCES"
            )

    print(f"\n=== CR035A2 VERDICT: {verdict}  ({verdict_case}) ===")
    print(f"    {verdict_token}")

    # ----- Emit artifacts -----
    summary = dict(
        precommit_sha256="6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697",
        execution_status="CLEAN",
        scientific_verdict=verdict,
        verdict_case=verdict_case,
        verdict_token=verdict_token,
        triage_bin="A",
        free_parameters_introduced_RunA=0,
        external_perturbation_disclosed=True,
        prior_CR_result_inputs=False,
        forbidden_files_opened=False,
        CR035A_files_opened=False,
        opened_paths_count=len(OPENED_PATHS),
        engine="CAMB",
        engine_version=_camb.__version__,
        peak_finder_spec="windows_plus_prominence",
        peak_finder_windows=PEAK_WINDOWS,
        peak_finder_prominence_muK2=PEAK_PROMINENCE,
        peak_finder_smoothing_sigma_ell=SMOOTH_SIGMA,
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
            P1_pass=p1["p1_pass"], P1_n_pass=p1["n_pass"],
            P1_first_peak_delta_ell=p1["delta1"],
            P1_2nd_3rd_peak_delta_ell=p1["deltas23"],
            P1_height_ratios=[
                dict(theory=r[0], planck=r[1]) for r in p1["ratios"]],
            P1_height_ratio_pass_each=p1["p1c_each"],
            P2_band=p2_token,
            P2_chi2_TT_over_dof=rd_TT,
            polarization_debt_runA=pol_debt,
            peaks_theory=[
                dict(window=PEAK_WINDOWS[i], ell=peaks_theory_i[0],
                     H_smoothed=peaks_theory_i[1], prominence=peaks_theory_i[3],
                     detected=peaks_theory_i[2])
                for i, peaks_theory_i in enumerate(A["peaks_theory"])
            ],
            peaks_planck=[
                dict(window=PEAK_WINDOWS[i], ell=peaks_planck_i[0],
                     H_smoothed=peaks_planck_i[1], prominence=peaks_planck_i[3],
                     detected=peaks_planck_i[2])
                for i, peaks_planck_i in enumerate(A["peaks_planck"])
            ],
        ),
        # Run B diagnostic
        runB=dict(
            A_s_optimized=B["A_s_opt"], n_s_optimized=B["n_s_opt"],
            tau_optimized=B["tau_opt"],
            sigma_dev_As=B["sigma_As"], sigma_dev_ns=B["sigma_ns"],
            sigma_dev_tau=B["sigma_tau"],
            chi2_TT_at_optimum=B["chi2_TT_opt"],
            dof_TT_at_optimum=B["dof_TT_opt"],
            chi2_per_dof_TT_at_optimum=rd_TT_B,
            chi2_TE_at_optimum=B["chi2_TE_opt"],
            dof_TE_at_optimum=B["dof_TE_opt"],
            chi2_per_dof_TE_at_optimum=rd_TE_B,
            chi2_EE_at_optimum=B["chi2_EE_opt"],
            dof_EE_at_optimum=B["dof_EE_opt"],
            chi2_per_dof_EE_at_optimum=rd_EE_B,
            within_5sigma_planck_posterior=(abs(B["sigma_As"])<=5
                                            and abs(B["sigma_ns"])<=5
                                            and abs(B["sigma_tau"])<=5),
            optimization_chi2_TT_in_band=(rd_TT_B <= CHI2_BOUND_TT),
            polarization_sanity_TE=(rd_TE_B <= CHI2_POL_SANITY_RUNB),
            polarization_sanity_EE=(rd_EE_B <= CHI2_POL_SANITY_RUNB),
            optimizer_converged=B["converged"],
            optimizer_nfev=B["nfev"], optimizer_nit=B["nit"],
            optimizer_message=B["message"],
        ),
    )

    out_summary = CR_DIR / "CR035A2_summary.json"
    out_summary.write_text(json.dumps(summary, indent=2, default=_jsonify), encoding="utf-8")
    print(f"\nWrote: {out_summary.name}")

    write_residual_csv(CR_DIR / "CR035A2_TT_residuals.csv",
                       A["ell_v_TT"], A["obs_TT"], A["sig_v_TT"],
                       A["th_v_TT"], A["res_TT"])
    write_residual_csv(CR_DIR / "CR035A2_TE_residuals.csv",
                       A["ell_v_TE"], A["obs_TE"], A["sig_v_TE"],
                       A["th_v_TE"], A["res_TE"])
    write_residual_csv(CR_DIR / "CR035A2_EE_residuals.csv",
                       A["ell_v_EE"], A["obs_EE"], A["sig_v_EE"],
                       A["th_v_EE"], A["res_EE"])
    write_peaks_csv(CR_DIR / "CR035A2_peaks.csv",
                    A["peaks_theory"], A["peaks_planck"])
    write_theory_csv(CR_DIR / "CR035A2_runA_theory_spectra.csv",
                     A["ell_th"], A["TT"], A["TE"], A["EE"])
    (CR_DIR / "CR035A2_runB_diagnostic.json").write_text(
        json.dumps(summary["runB"], indent=2, default=_jsonify), encoding="utf-8")
    print("Wrote: TT/TE/EE residual CSVs, peaks CSV, runB_diagnostic.json, "
          "runA_theory_spectra.csv")

    # ----- Result markdown -----
    def fmt_peak(p):
        if p[2]:
            return f"ell={p[0]:.1f}  H_smoothed={p[1]:.2f}  prom={p[3]:.2f}"
        return "NOT DETECTED in window"

    pass_summary_line = {
        "PASS":     "CR035A2 PASS confirms that the SAM density spine, paired "
                    "with Planck 2018 posterior-centroid perturbation parameters "
                    "and CAMB 1.6.6, reproduces the Planck 2018 PR3 full "
                    "per-multipole bandpower table at the corrected CR035A2 peak "
                    "and full-shape tolerances.",
        "BOUNDARY": f"CR035A2 BOUNDARY ({verdict_case}): SAM density spine is "
                    f"consistent with the Planck full per-multipole bandpower "
                    f"table within the predeclared CR035A2 boundary conditions; "
                    f"see the verdict-case detail for the specific gate.",
        "FAIL":     "CR035A2 FAIL rejects the SAM density spine at the full "
                    "per-multipole shape level under the corrected peak finder "
                    "and verdict tree.",
    }[verdict]

    result_md = f"""# CR035A2_PEAK_FINDER_AUDIT

## Verdict

```text
{verdict_token}
```

## Courtroom Fields

```text
execution_status                 = CLEAN
scientific_verdict               = {verdict}
verdict_case                     = {verdict_case}
triage_bin                       = A
free_parameters_introduced_RunA  = 0
external_perturbation_disclosed  = true
prior_CR_result_inputs           = false
forbidden_files_opened           = false
CR035A_files_opened              = false
opened_paths_count               = {len(OPENED_PATHS)}
precommit_sha256                 = 6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697
engine                           = CAMB {_camb.__version__}
peak_finder                      = windows + prominence >= 50 muK^2 + smoothed-curve heights
```

## Summary

```text
{pass_summary_line}

CR035A's strict FAIL token remains sealed and is not overwritten.
CR035A2 is the appeal: same SAM densities + same fixed Planck
perturbations + same CAMB engine + same Planck files + same chi^2 /
tolerances / Run B bounds. Only the peak finder (per-peak windows +
minimum prominence + smoothed-curve heights) and the verdict-mapping
tree (full BOUNDARY (iii) branch + Run B polarization sanity guard
at TE/EE chi^2/dof <= 5.0) changed.
```

## SAM Density Spine (substrate-derived; unchanged)

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

## Peak Finder (NEW spec)

| field | value |
|---|---|
| smoothing | Gaussian σ_ell = 5 |
| min prominence | 50 μK² |
| Peak 1 window | ℓ ∈ [150, 300] |
| Peak 2 window | ℓ ∈ [400, 650] |
| Peak 3 window | ℓ ∈ [700, 900] |
| height rule | H_i = D_l,smoothed at detected ℓ_peak_i |

| peak | theory | Planck |
|---|---|---|
| 1 | {fmt_peak(A['peaks_theory'][0])} | {fmt_peak(A['peaks_planck'][0])} |
| 2 | {fmt_peak(A['peaks_theory'][1])} | {fmt_peak(A['peaks_planck'][1])} |
| 3 | {fmt_peak(A['peaks_theory'][2])} | {fmt_peak(A['peaks_planck'][2])} |

## P1 — Acoustic Geometry / Peak Structure (Run A)

| sub-gate | tolerance | pass |
|---|---|---:|
| P1a (1st peak Δℓ ≤ 5) | ±5 | **{p1['p1a']}** |
| P1b (2nd/3rd Δℓ ≤ 10) | ±10 each | **{p1['p1b']}** |
| P1c (H2/H1, H3/H1 within 15%) | ±15% each | **{p1['p1c']}** |
| **P1 (≥2 of 3)** | | **{p1['p1_pass']}** |

Peak deltas: Δℓ_1 = {p1['delta1']}, Δℓ_{{2,3}} = {p1['deltas23']}.
Height ratios (theory / Planck): H2/H1 {p1['ratios'][0][0]:.4f} / {p1['ratios'][0][1]:.4f} → {p1['p1c_each'][0]};
H3/H1 {p1['ratios'][1][0]:.4f} / {p1['ratios'][1][1]:.4f} → {p1['p1c_each'][1]}.

## P2 — TT Full-Shape (Run A)

| stat | value |
|---|---:|
| χ²_TT | {A['chi2_TT']:.4f} |
| dof_TT | {A['dof_TT']} |
| **χ²_TT / dof_TT** | **{rd_TT:.4f}** |
| P2 band | **{p2_token}** |

## TE / EE — Reported (Run A)

| spectrum | χ² | dof | χ²/dof |
|---|---:|---:|---:|
| TE | {A['chi2_TE']:.4f} | {A['dof_TE']} | {rd_TE:.4f} |
| EE | {A['chi2_EE']:.4f} | {A['dof_EE']} | {rd_EE:.4f} |

Polarization debt (Run A): **{pol_debt}** (TT passes but TE or EE > 3.0 at Run A).

## Run B — Diagnostic Optimization

| param | optimized | fixed (Planck) | σ-deviation |
|---|---|---|---:|
| A_s | {B['A_s_opt']:.4e} | {A_S_FIXED:.4e} | {B['sigma_As']:+.3f} σ |
| n_s | {B['n_s_opt']:.4f} | {N_S_FIXED} | {B['sigma_ns']:+.3f} σ |
| τ | {B['tau_opt']:.4f} | {TAU_FIXED} | {B['sigma_tau']:+.3f} σ |
| χ²_TT/dof at optimum | {rd_TT_B:.4f} | (<= 3.0 for BOUNDARY iii) | |
| χ²_TE/dof at optimum | {rd_TE_B:.4f} | (<= 5.0 sanity guard) | |
| χ²_EE/dof at optimum | {rd_EE_B:.4f} | (<= 5.0 sanity guard) | |
| optimizer | L-BFGS-B  ({B['nit']} iters, {B['nfev']} evals) | | |

Run B is diagnostic only. BOUNDARY (iii) additionally requires TE/EE chi^2/dof <= 5.0 at the optimum.

## Chronology

```text
CR035A v2 strict FAIL stands sealed at 2026-06-27 (precommit
0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced).
CR035A2 is an appeal that corrects only the peak finder and the
verdict-mapping tree, with all other test inputs frozen from CR035A.
The CR035A2 runner did not open any CR035A file at runtime
(CR035A_files_opened = false; opened_paths_count = {len(OPENED_PATHS)}).
The appeal addresses the verdict token, not the underlying numerics.
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697
Appeal of      = CR035A_SAM_DENSITY_SPINE_CMB_SHAPE (FAIL, sealed)
External data  = Planck PR3 TT/TE/EE bandpowers (locally hashed in HASHES.txt)
Engine         = CAMB {_camb.__version__}
```

---

**Sealed by:** CR035A2 runner, 2026-06-27.
"""
    (CR_DIR / "CR035A2_result.md").write_text(result_md, encoding="utf-8")
    print("Wrote: CR035A2_result.md")
    print(f"\nVerdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
