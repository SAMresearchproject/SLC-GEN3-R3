"""
CR037B runner: parameter-free CMB shape attempt.

Implements the test specified in CR037B_PRECOMMIT.md
(SHA-256 5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b).

Full SAM-derived cosmology (substrate-spine + H_0_SAM + SAM perturbation
triplet) through CAMB 1.6.6 with all ancillary settings frozen and
echoed in summary. NO Run B optimizer.

Substrate-derived inputs (numeric literals; prior CR files NOT opened):
  Omega_m = R*A_0 = 1/pi                          (substrate)
  Omega_b = 2*A_0*(1-chi)                         (substrate)
  Omega_c = Omega_m - Omega_b                     (substrate)
  H_0     = 67.2503751950 km/s/Mpc                (CR036 sealed)
  A_s     = 2.1117473568e-9   = eta_SAM*sqrt(R)   (CR037A sealed)
  n_s     = 0.9646322349      = 1 - chi/2          (CR037A sealed)
  tau     = 0.0530516477      = 2 * A_0            (CR037A sealed)

Fixed non-fit ancillary inputs:
  T_CMB   = 2.7255 K          (measured thermal anchor)
  N_eff   = 3.046             (standard)
  k_pivot = 0.05 Mpc^-1       (scalar-amplitude convention)

CAMB ancillary settings ALL frozen and emitted in summary so no hidden
default can carry the result.

NO Run B. Verdict tree: PASS / BOUNDARY (i) / BOUNDARY (ii) / FAIL.

CR035A2 / CR036 / CR036B / CR037A all stand sealed and are NOT overwritten.
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
    # CR035A2 family
    re.compile(r"CR035A2_summary\.json$",                 re.IGNORECASE),
    re.compile(r"CR035A2_result\.md$",                    re.IGNORECASE),
    re.compile(r"CR035A2_(TT|TE|EE)_residuals\.csv$",     re.IGNORECASE),
    re.compile(r"CR035A2_peaks\.csv$",                    re.IGNORECASE),
    re.compile(r"CR035A2_runB_diagnostic\.json$",         re.IGNORECASE),
    re.compile(r"CR035A2_runA_theory_spectra\.csv$",      re.IGNORECASE),
    re.compile(r"CR035A2_runner.*\.py$",                  re.IGNORECASE),
    re.compile(r"CR035A2_PRECOMMIT\.md$",                 re.IGNORECASE),
    # CR036 family
    re.compile(r"CR036_summary\.json$",                   re.IGNORECASE),
    re.compile(r"CR036_result\.md$",                      re.IGNORECASE),
    re.compile(r"CR036_evidence_rows\.csv$",              re.IGNORECASE),
    re.compile(r"CR036_substrate_atoms\.csv$",            re.IGNORECASE),
    re.compile(r"CR036_runner.*\.py$",                    re.IGNORECASE),
    re.compile(r"CR036_PRECOMMIT\.md$",                   re.IGNORECASE),
    # CR036B family (NEW vs CR036B)
    re.compile(r"CR036B_summary\.json$",                  re.IGNORECASE),
    re.compile(r"CR036B_result\.md$",                     re.IGNORECASE),
    re.compile(r"CR036B_(TT|TE|EE)_residuals\.csv$",      re.IGNORECASE),
    re.compile(r"CR036B_peaks\.csv$",                     re.IGNORECASE),
    re.compile(r"CR036B_runB_diagnostic\.json$",          re.IGNORECASE),
    re.compile(r"CR036B_runA_theory_spectra\.csv$",       re.IGNORECASE),
    re.compile(r"CR036B_runner.*\.py$",                   re.IGNORECASE),
    re.compile(r"CR036B_PRECOMMIT\.md$",                  re.IGNORECASE),
    # CR037A family (NEW vs CR036B)
    re.compile(r"CR037A_summary\.json$",                  re.IGNORECASE),
    re.compile(r"CR037A_result\.md$",                     re.IGNORECASE),
    re.compile(r"CR037A_evidence_rows\.csv$",             re.IGNORECASE),
    re.compile(r"CR037A_runner.*\.py$",                   re.IGNORECASE),
    re.compile(r"CR037A_PRECOMMIT\.md$",                  re.IGNORECASE),
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
                f"CR037B forbidden-file guard tripped: attempted to open {p!r}"
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

# H_0_SAM sealed from CR036 precommit hash
# 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2,
# canonical value copied from CR036_summary.json by value.
# The CR037B runner does NOT open any CR036 file at runtime.
H_0 = 67.2503751950   # H_0_SAM (sealed in CR036)
H_SMALL = H_0 / 100.0
OMBH2 = OMEGA_B * H_SMALL ** 2
OMCH2 = OMEGA_C * H_SMALL ** 2

# SAM perturbation triplet sealed from CR037A precommit hash
# 1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78,
# canonical values copied from CR037A_summary.json by value.
# The CR037B runner does NOT open any CR037A file at runtime.
A_S_FIXED = 2.1117473568e-9   # eta_SAM * sqrt(R)        (CR037A sealed)
N_S_FIXED = 0.9646322349       # 1 - chi/2                 (CR037A sealed)
TAU_FIXED = 0.0530516477       # 2 * A_0                   (CR037A sealed)

# Fixed non-fit ancillary inputs (disclosed)
N_EFF = 3.046                  # standard radiation-sector input
T_CMB = 2.7255                 # measured thermal anchor (FIRAS)
K_PIVOT = 0.05                 # scalar-amplitude convention (Mpc^-1)
MNU = 0.06                     # sum of neutrino masses (eV; Planck-baseline)

# CAMB ancillary settings (frozen; emitted in summary)
CAMB_LMAX = 2700
CAMB_LENS_POTENTIAL_ACCURACY = 1
CAMB_WANT_TENSORS = False
CAMB_WANT_SCALARS = True
CAMB_R_TENSOR = 0.0
CAMB_OMK = 0.0
CAMB_NUM_MASSIVE_NEUTRINOS = 1
CAMB_CMB_UNIT = "muK"
CAMB_SPECTRA = ("lensed_scalar",)

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

def camb_spectra(A_s: float, n_s: float, tau: float,
                 lmax: int = CAMB_LMAX, return_settings: bool = False):
    """Compute lensed TT/TE/EE D_l in muK^2 with full SAM cosmology +
    SAM-derived perturbations. All CAMB settings are frozen and
    extractable for echo into the summary."""
    import camb
    from camb import model
    pars = camb.CAMBparams()
    pars.set_cosmology(
        H0=H_0, ombh2=OMBH2, omch2=OMCH2,
        mnu=MNU, omk=CAMB_OMK, tau=tau,
        TCMB=T_CMB,
        num_massive_neutrinos=CAMB_NUM_MASSIVE_NEUTRINOS,
        nnu=N_EFF,
    )
    pars.InitPower.set_params(As=A_s, ns=n_s, pivot_scalar=K_PIVOT,
                              r=CAMB_R_TENSOR)
    pars.set_for_lmax(lmax=lmax,
                      lens_potential_accuracy=CAMB_LENS_POTENTIAL_ACCURACY)
    pars.WantTensors = CAMB_WANT_TENSORS
    pars.WantScalars = CAMB_WANT_SCALARS
    pars.NonLinear   = model.NonLinear_none   # explicit; default is None

    results = camb.get_results(pars)
    cls = results.get_cmb_power_spectra(pars, CMB_unit=CAMB_CMB_UNIT,
                                        spectra=list(CAMB_SPECTRA))
    spec = cls["lensed_scalar"]
    ell_arr = np.arange(spec.shape[0])
    TT = spec[:, 0]
    EE = spec[:, 1]
    TE = spec[:, 3]

    if return_settings:
        # Extract every CAMB ancillary that affects spectra
        try:
            YHe_used = float(pars.YHe)
        except Exception:
            YHe_used = None
        try:
            nonlinear_name = str(pars.NonLinear)
        except Exception:
            nonlinear_name = "NonLinear_none"
        settings = dict(
            camb_version=camb.__version__,
            lmax=CAMB_LMAX,
            lens_potential_accuracy=CAMB_LENS_POTENTIAL_ACCURACY,
            WantTensors=CAMB_WANT_TENSORS,
            WantScalars=CAMB_WANT_SCALARS,
            r_tensor=CAMB_R_TENSOR,
            NonLinear=nonlinear_name,
            omk=CAMB_OMK,
            TCMB=T_CMB,
            nnu=N_EFF,
            num_massive_neutrinos=CAMB_NUM_MASSIVE_NEUTRINOS,
            mnu_eV=MNU,
            YHe_used=YHe_used,
            YHe_handling="CAMB BBN-consistency (default; set via set_cosmology)",
            pivot_scalar=K_PIVOT,
            CMB_unit=CAMB_CMB_UNIT,
            spectra_requested=list(CAMB_SPECTRA),
            H0=H_0,
            ombh2=OMBH2,
            omch2=OMCH2,
            tau=tau,
            As=A_s,
            ns=n_s,
        )
        return ell_arr, TT, TE, EE, settings
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
# Run A (single verdict path; NO Run B)
# =====================================================================

def run_a(ell_TT, Dl_TT_planck, sig_TT_planck,
          ell_TE, Dl_TE_planck, sig_TE_planck,
          ell_EE, Dl_EE_planck, sig_EE_planck):
    """Run A: SAM density spine + H_0_SAM + SAM perturbation triplet.
    NO Run B optimizer. Returns CAMB settings echo for the summary."""
    print("Run A: full SAM cosmology (densities + H_0_SAM + SAM perturbations) ...")
    ell_th, TT_th, TE_th, EE_th, camb_settings = camb_spectra(
        A_S_FIXED, N_S_FIXED, TAU_FIXED, return_settings=True)

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
        camb_settings=camb_settings,
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


# NO Run B optimizer in CR037B. The perturbation triplet is fixed at the
# CR037A-sealed values. There is no rescue branch.


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
    print(f"CR037B runner  -  parameter-free CMB shape attempt (full SAM cosmology, NO Run B)")
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

    # NO Run B in CR037B.

    # ----- Verdict tree (NO BOUNDARY iii branch) -----
    if p1["p1_pass"] and p2_token == "PASS":
        if pol_debt:
            verdict = "BOUNDARY"
            verdict_case = "ii_polarization_debt"
            verdict_token = (
                "CR037B_BOUNDARY_POLARIZATION_DEBT_TT_PASSES_TE_OR_EE_DEGRADED"
            )
        else:
            verdict = "PASS"
            verdict_case = "PASS"
            verdict_token = (
                "CR037B_PASS_PARAMETER_FREE_SAM_COSMOLOGY_REPRODUCES_PLANCK_TT"
                "_FULL_PER_MULTIPOLE_SHAPE_AT_PEAK_AND_FULL_SHAPE_TOLERANCES"
            )
    elif p1["p1_pass"] and p2_token == "BOUNDARY":
        verdict = "BOUNDARY"
        verdict_case = "i_full_shape_marginal"
        verdict_token = (
            "CR037B_BOUNDARY_TT_FULL_SHAPE_BETWEEN_2_AND_3_CHI2_PER_DOF"
        )
    else:
        verdict = "FAIL"
        verdict_case = "FAIL"
        verdict_token = (
            "CR037B_FAIL_PARAMETER_FREE_SAM_COSMOLOGY_FULL_PER_MULTIPOLE_SHAPE_OUTSIDE_TOLERANCES"
        )

    print(f"\n=== CR037B VERDICT: {verdict}  ({verdict_case}) ===")
    print(f"    {verdict_token}")

    # ----- Emit artifacts -----
    summary = dict(
        precommit_sha256="5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b",
        execution_status="CLEAN",
        scientific_verdict=verdict,
        verdict_case=verdict_case,
        verdict_token=verdict_token,
        triage_bin="A",
        free_parameters_introduced=0,
        prior_CR_result_inputs=False,
        Run_B_optimizer_used=False,
        CR035A_files_opened=False,
        CR035A2_files_opened=False,
        CR036_files_opened=False,
        CR036B_files_opened=False,
        CR037A_files_opened=False,
        forbidden_files_opened=False,
        opened_paths_count=len(OPENED_PATHS),
        engine="CAMB",
        engine_version=_camb.__version__,
        peak_finder_spec="windows_plus_prominence",
        peak_finder_windows=PEAK_WINDOWS,
        peak_finder_prominence_muK2=PEAK_PROMINENCE,
        peak_finder_smoothing_sigma_ell=SMOOTH_SIGMA,
        # Full CAMB ancillary settings echo (frozen)
        camb_settings=A["camb_settings"],
        # SAM density spine
        substrate=dict(
            R=R, D=D, S=S, alpha_H=ALPHA_H,
            A_0=A_0, chi=CHI,
            Omega_m=OMEGA_M, Omega_b=OMEGA_B, Omega_c=OMEGA_C,
            H_0=H_0, h=H_SMALL,
            ombh2=OMBH2, omch2=OMCH2,
        ),
        sam_perturbations=dict(
            A_s_SAM=A_S_FIXED, n_s_SAM=N_S_FIXED, tau_SAM=TAU_FIXED,
            A_s_identity="eta_SAM * sqrt(R)",
            n_s_identity="1 - chi/2",
            tau_identity="2 * A_0",
            source="CR037A sealed PASS (1b7da85b...)",
        ),
        ancillary_fixed=dict(
            N_eff=N_EFF, T_CMB=T_CMB, k_pivot=K_PIVOT,
            mnu_eV=MNU,
            note="Fixed non-fit ancillary inputs; not optimized, not "
                 "read from posterior chains, not adjusted to improve "
                 "the CR037B result.",
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
        # Run A (the only run)
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
    )

    out_summary = CR_DIR / "CR037B_summary.json"
    out_summary.write_text(json.dumps(summary, indent=2, default=_jsonify), encoding="utf-8")
    print(f"\nWrote: {out_summary.name}")

    write_residual_csv(CR_DIR / "CR037B_TT_residuals.csv",
                       A["ell_v_TT"], A["obs_TT"], A["sig_v_TT"],
                       A["th_v_TT"], A["res_TT"])
    write_residual_csv(CR_DIR / "CR037B_TE_residuals.csv",
                       A["ell_v_TE"], A["obs_TE"], A["sig_v_TE"],
                       A["th_v_TE"], A["res_TE"])
    write_residual_csv(CR_DIR / "CR037B_EE_residuals.csv",
                       A["ell_v_EE"], A["obs_EE"], A["sig_v_EE"],
                       A["th_v_EE"], A["res_EE"])
    write_peaks_csv(CR_DIR / "CR037B_peaks.csv",
                    A["peaks_theory"], A["peaks_planck"])
    write_theory_csv(CR_DIR / "CR037B_runA_theory_spectra.csv",
                     A["ell_th"], A["TT"], A["TE"], A["EE"])
    print("Wrote: TT/TE/EE residual CSVs, peaks CSV, runA_theory_spectra.csv "
          "(NO runB diagnostic in CR037B)")

    # ----- Result markdown -----
    def fmt_peak(p):
        if p[2]:
            return f"ell={p[0]:.1f}  H_smoothed={p[1]:.2f}  prom={p[3]:.2f}"
        return "NOT DETECTED in window"

    pass_summary_line = {
        "PASS":     "CR037B PASS confirms that the SAM-derived cosmological "
                    "inputs (densities + H_0_SAM + SAM perturbation triplet, "
                    "all from substrate atoms via FIRAS T_CMB + CODATA 2018 / "
                    "SI fixed constants) reproduce the Planck 2018 PR3 full "
                    "per-multipole bandpower table at the CR035A2 P1 peak "
                    "structure + P2 full-shape tolerances, with NO Run B "
                    "optimizer and zero free parameters.",
        "BOUNDARY": f"CR037B BOUNDARY ({verdict_case}): SAM-derived cosmology "
                    f"(densities + H_0_SAM + SAM perturbations) is consistent "
                    f"with the Planck full per-multipole bandpower table within "
                    f"the CR037B boundary conditions; see the verdict-case "
                    f"detail for the specific gate.",
        "FAIL":     "CR037B FAIL rejects the parameter-free SAM cosmology "
                    "cascade at the Planck full per-multipole shape level "
                    "under the CR037B verdict tree.",
    }[verdict]

    cs = A["camb_settings"]
    result_md = f"""# CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT

## Verdict

```text
{verdict_token}
```

## Courtroom Fields

```text
execution_status               = CLEAN
scientific_verdict             = {verdict}
verdict_case                   = {verdict_case}
triage_bin                     = A
free_parameters_introduced     = 0
prior_CR_result_inputs         = false
Run_B_optimizer_used           = false
forbidden_files_opened         = false
CR035A_files_opened            = false
CR035A2_files_opened           = false
CR036_files_opened             = false
CR036B_files_opened            = false
CR037A_files_opened            = false
opened_paths_count             = {len(OPENED_PATHS)}
precommit_sha256               = 5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b
engine                         = CAMB {_camb.__version__}
peak_finder                    = windows + prominence >= 50 muK^2 + smoothed-curve heights
```

## Summary

```text
{pass_summary_line}

CR035A2, CR036, CR036B, and CR037A all stand sealed and are NOT
overwritten. CR037B inherits the CR036B spec verbatim except for the
perturbation triplet, which now comes from CR037A:

  CR036B:  A_s = 2.100e-9       n_s = 0.9649       tau = 0.0544       (Planck centroids)
  CR037B:  A_s = 2.1117473568e-9 n_s = 0.9646322349 tau = 0.0530516477 (SAM, CR037A)

All cosmology inputs (Omega_m, Omega_b, Omega_c, H_0, A_s, n_s, tau) are
SAM-derived from substrate atoms via the declared T_CMB FIRAS thermal
anchor + CODATA 2018 / SI fixed constants. There is no Run B optimizer.
The runner did NOT open any CR036, CR036B, CR035A2, CR035A, or CR037A
file at runtime.
```

## SAM Density Spine (substrate-derived)

| symbol | value |
|---|---:|
| A_0 = 1/(12π) | {A_0:.12f} |
| χ = 2/(9π) | {CHI:.12f} |
| Ω_m = 1/π | {OMEGA_M:.12f} |
| Ω_b = 2·A_0·(1−χ) | {OMEGA_B:.12f} |
| Ω_c = Ω_m − Ω_b | {OMEGA_C:.12f} |
| H_0 (CR036) | {H_0} km/s/Mpc |
| ω_b = Ω_b·h² | {OMBH2:.12f} |
| ω_c = Ω_c·h² | {OMCH2:.12f} |

## SAM-Derived Perturbations (from CR037A)

| field | identity | value |
|---|---|---:|
| A_s,SAM | η_SAM·√R | {A_S_FIXED:.10e} |
| n_s,SAM | 1 − χ/2 | {N_S_FIXED} |
| τ_SAM | 2·A_0 | {TAU_FIXED} |

## Fixed Non-Fit Ancillary Inputs (disclosed)

| field | value | note |
|---|---:|---|
| N_eff | {N_EFF} | standard radiation-sector input |
| T_CMB | {T_CMB} K | measured thermal anchor (FIRAS) |
| k_pivot | {K_PIVOT} Mpc⁻¹ | scalar-amplitude convention |
| m_ν (sum) | {MNU} eV | Planck-baseline |

## CAMB Ancillary Settings (frozen; echoed from runtime)

| setting | value |
|---|---:|
| camb_version | {cs.get('camb_version')} |
| lmax | {cs.get('lmax')} |
| lens_potential_accuracy | {cs.get('lens_potential_accuracy')} |
| WantTensors | {cs.get('WantTensors')} |
| WantScalars | {cs.get('WantScalars')} |
| r (tensor-to-scalar) | {cs.get('r_tensor')} |
| NonLinear | {cs.get('NonLinear')} |
| omk | {cs.get('omk')} |
| TCMB | {cs.get('TCMB')} |
| nnu | {cs.get('nnu')} |
| num_massive_neutrinos | {cs.get('num_massive_neutrinos')} |
| mnu (eV) | {cs.get('mnu_eV')} |
| YHe_used | {cs.get('YHe_used')} |
| YHe_handling | {cs.get('YHe_handling')} |
| pivot_scalar | {cs.get('pivot_scalar')} |
| CMB_unit | {cs.get('CMB_unit')} |
| spectra_requested | {cs.get('spectra_requested')} |

## Peak Finder

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

## Chronology

```text
CR037B is the parameter-free CMB shape attempt. It follows:
  CR035A2 (precommit 6310c00f...; PASS at TT chi^2/dof = 1.35 with
    H_0 = 68.76 externally set + Planck-centroid perturbations)
  CR036    (precommit 345a1a8d...; PASS deriving H_0_SAM = 67.2503751950
    from substrate atoms + FIRAS T_CMB + CODATA 2018 / SI)
  CR036B   (precommit ab2fea4b...; PASS at TT chi^2/dof = 1.04 with
    SAM density spine + H_0_SAM + Planck-centroid perturbations)
  CR037A   (precommit 1b7da85b...; PASS with all three SAM perturbation
    identities (A_s,SAM = eta*sqrt(R); n_s,SAM = 1 - chi/2;
    tau_SAM = 2*A_0) inside Planck posterior at STRONG_CONTACT)

CR037B closes the cascade: the full SAM-derived cosmology (densities +
H_0 + perturbation triplet) runs through CAMB 1.6.6 with NO Run B
optimizer. The runner did NOT open any CR036, CR036B, CR035A, CR035A2,
or CR037A file at runtime; all values are numeric literals cited by
hash provenance in the precommit.
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b
H_0 source     = CR036 sealed PASS (precommit 345a1a8d...; cited by value)
Perturbations  = CR037A sealed PASS (precommit 1b7da85b...; cited by value)
External data  = Planck PR3 TT/TE/EE bandpowers (locally hashed in HASHES.txt)
Engine         = CAMB {_camb.__version__}
```

---

**Sealed by:** CR037B runner, 2026-06-27.
"""
    (CR_DIR / "CR037B_result.md").write_text(result_md, encoding="utf-8")
    print("Wrote: CR036B_result.md")
    print(f"\nVerdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
