"""
CR037A runner: SAM perturbation-sector selector.

Implements the test specified in CR037A_PRECOMMIT.md
(SHA-256 1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78).

Candidate substrate identities under test:
  n_s_SAM = 1 - chi/2 = 1 - 1/(9*pi)
  A_s_SAM = eta_SAM * sqrt(R) = 7 * sqrt(R) / (4 * (12*pi)^6)
  tau_SAM = 2 * A_0 = 1/(6*pi)

Gates (per-parameter):
  PASS     |sigma_dev| <= 1.0
  BOUNDARY 1.0 < |sigma_dev| <= 2.0
  FAIL     |sigma_dev| >  2.0

Overall:
  PASS      iff all three parameters are PASS
  BOUNDARY  iff at least one is BOUNDARY and none is FAIL
  FAIL      iff any is FAIL

Reported flags (NOT gates):
  STRONG_CONTACT_X if |sigma_dev_X| <= 0.5
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
    # CR035A family
    re.compile(r"CR035A_(summary|result|evidence|runner|PRECOMMIT|TT|TE|EE|peaks|runA|runB).*", re.IGNORECASE),
    # CR035A2 family
    re.compile(r"CR035A2_(summary|result|evidence|runner|PRECOMMIT|TT|TE|EE|peaks|runA|runB).*", re.IGNORECASE),
    # CR036 family
    re.compile(r"CR036_(summary|result|evidence|runner|PRECOMMIT|substrate_atoms).*", re.IGNORECASE),
    # CR036B family
    re.compile(r"CR036B_(summary|result|evidence|runner|PRECOMMIT|TT|TE|EE|peaks|runA|runB).*", re.IGNORECASE),
    # Planck spectra / chains / posteriors
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
                f"CR037A forbidden-file guard tripped: attempted to open {p!r}"
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
THETA   = 18
M_CAP   = 126
F_CAR   = 81
L       = 162
V       = 27

A_0 = 1.0 / (12.0 * PI)
CHI = (S / D) * A_0


# =====================================================================
# Frozen external references (numeric constants; runner does NOT open files)
# =====================================================================

A_S_REF   = 2.100e-9
SIGMA_AS  = 0.030e-9
N_S_REF   = 0.9649
SIGMA_NS  = 0.0042
TAU_REF   = 0.0544
SIGMA_TAU = 0.0073


# =====================================================================
# Eta identity (re-derived from substrate atoms in-runner)
# =====================================================================

def eta_sam_from_atoms() -> float:
    """eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V)."""
    exponent = L // V                            # 162/27 = 6 (exact integer)
    assert L % V == 0
    coef = M_CAP / (ALPHA_H * ALPHA_H * THETA)   # 126/72 = 7/4
    return coef * (A_0 ** exponent)


def eta_sam_compact() -> float:
    """eta_SAM = 7 / (4 * (12*pi)^6)."""
    return 7.0 / (4.0 * (12.0 * PI) ** 6)


# =====================================================================
# Perturbation identities (two paths each for E3 machine-precision check)
# =====================================================================

def n_s_sam_path_a() -> float:
    return 1.0 - CHI / 2.0


def n_s_sam_path_b() -> float:
    return 1.0 - 1.0 / (9.0 * PI)


def A_s_sam_path_a(eta: float) -> float:
    return eta * math.sqrt(R)


def A_s_sam_path_b() -> float:
    return 7.0 * math.sqrt(R) / (4.0 * (12.0 * PI) ** 6)


def tau_sam_path_a() -> float:
    return 2.0 * A_0


def tau_sam_path_b() -> float:
    return 1.0 / (6.0 * PI)


# =====================================================================
# Bands and verdict combination
# =====================================================================

def band(sigma_dev: float) -> str:
    a = abs(sigma_dev)
    if a <= 1.0:
        return "PASS"
    if a <= 2.0:
        return "BOUNDARY"
    return "FAIL"


def combine_verdict(*bands) -> str:
    if "FAIL" in bands:
        return "FAIL"
    if "BOUNDARY" in bands:
        return "BOUNDARY"
    return "PASS"


# =====================================================================
# Wrong-control comparators for A_s (E1)
# =====================================================================

def wrong_controls_for_As(eta: float) -> list[tuple[str, float, float]]:
    """Return list of (label, value, sigma_dev_vs_A_s_ref)."""
    comparators = [
        ("eta_SAM (bare)",        eta),
        ("eta * sqrt(R) [chosen]", eta * math.sqrt(R)),
        ("eta * sqrt(S)",         eta * math.sqrt(S)),
        ("eta * sqrt(R/2)",       eta * math.sqrt(R / 2)),
        ("eta * sqrt(Theta)",     eta * math.sqrt(THETA)),
        ("eta * D",               eta * D),
        ("eta * pi",              eta * PI),
    ]
    return [(lbl, v, (v - A_S_REF) / SIGMA_AS) for lbl, v in comparators]


# =====================================================================
# Output writers
# =====================================================================

def write_evidence_csv(path: Path, eta_a, eta_b, ns_a, ns_b, As_a, As_b,
                       tau_a, tau_b, A_s_sam, n_s_sam, tau_sam,
                       sigma_devs, bands_per_param, strong_contact, wrongs,
                       tau_alt, sigma_dev_tau_alt):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["field", "value", "units", "notes"])
        w.writerow(["R", R, "", "radix"])
        w.writerow(["D", D, "", "dimension"])
        w.writerow(["S", S, "", "split inventory"])
        w.writerow(["alpha_H", ALPHA_H, "", "binary readout"])
        w.writerow(["Theta", THETA, "", "tensor bridge"])
        w.writerow(["M", M_CAP, "", "matter capacity"])
        w.writerow(["L", L, "", "closed ledger"])
        w.writerow(["V", V, "", "resolved write cell"])
        w.writerow(["A_0", f"{A_0:.20e}", "", "1/(12*pi)"])
        w.writerow(["chi", f"{CHI:.20e}", "", "2/(9*pi)"])
        w.writerow(["eta_SAM Path A (atoms)", f"{eta_a:.20e}", "", "(M/(alpha^2*Theta))*A_0^(L/V)"])
        w.writerow(["eta_SAM Path B (compact)", f"{eta_b:.20e}", "", "7/(4*(12pi)^6)"])
        w.writerow(["|eta A - eta B| / eta A", f"{abs(eta_a-eta_b)/eta_a:.3e}", "", "machine-precision check"])
        w.writerow(["n_s_SAM Path A", f"{ns_a:.20e}", "", "1 - chi/2"])
        w.writerow(["n_s_SAM Path B", f"{ns_b:.20e}", "", "1 - 1/(9*pi)"])
        w.writerow(["A_s_SAM Path A", f"{As_a:.20e}", "", "eta_SAM * sqrt(R)"])
        w.writerow(["A_s_SAM Path B", f"{As_b:.20e}", "", "7*sqrt(R)/(4*(12pi)^6)"])
        w.writerow(["tau_SAM Path A", f"{tau_a:.20e}", "", "2*A_0"])
        w.writerow(["tau_SAM Path B", f"{tau_b:.20e}", "", "1/(6*pi)"])
        w.writerow(["A_s_SAM canonical", f"{A_s_sam:.20e}", "", "Path A"])
        w.writerow(["n_s_SAM canonical", f"{n_s_sam:.20e}", "", "Path A"])
        w.writerow(["tau_SAM canonical", f"{tau_sam:.20e}", "", "Path A"])
        w.writerow(["A_s_reference", f"{A_S_REF:.6e}", "", "Planck 2018"])
        w.writerow(["sigma_As", f"{SIGMA_AS:.6e}", "", "Planck 2018"])
        w.writerow(["n_s_reference", N_S_REF, "", "Planck 2018"])
        w.writerow(["sigma_ns", SIGMA_NS, "", "Planck 2018"])
        w.writerow(["tau_reference", TAU_REF, "", "Planck 2018"])
        w.writerow(["sigma_tau", SIGMA_TAU, "", "Planck 2018"])
        w.writerow(["sigma_dev_As", f"{sigma_devs['As']:+.6f}", "", f"band={bands_per_param['As']}"])
        w.writerow(["sigma_dev_ns", f"{sigma_devs['ns']:+.6f}", "", f"band={bands_per_param['ns']}"])
        w.writerow(["sigma_dev_tau", f"{sigma_devs['tau']:+.6f}", "", f"band={bands_per_param['tau']}"])
        w.writerow(["STRONG_CONTACT_AS", strong_contact["As"], "", "|sigma_dev| <= 0.5"])
        w.writerow(["STRONG_CONTACT_NS", strong_contact["ns"], "", "|sigma_dev| <= 0.5"])
        w.writerow(["STRONG_CONTACT_TAU", strong_contact["tau"], "", "|sigma_dev| <= 0.5"])
        # Wrong-controls for A_s
        for lbl, val, dev in wrongs:
            w.writerow([f"A_s WC: {lbl}", f"{val:.6e}", "", f"sigma_dev = {dev:+.4f}"])
        # Self-lifted tau alternative
        w.writerow(["tau_alt = 2*A_0*(1+A_0)", f"{tau_alt:.12f}", "",
                    f"sigma_dev = {sigma_dev_tau_alt:+.4f} (reported only)"])


# =====================================================================
# Main
# =====================================================================

def main() -> int:
    print("CR037A runner  -  SAM perturbation-sector selector")
    print()

    # eta_SAM (two paths)
    eta_a = eta_sam_from_atoms()
    eta_b = eta_sam_compact()
    eta_rel = abs(eta_a - eta_b) / eta_a
    eta_SAM = eta_a   # canonical

    # n_s_SAM
    ns_a = n_s_sam_path_a()
    ns_b = n_s_sam_path_b()
    ns_rel = abs(ns_a - ns_b) / abs(ns_a)
    n_s_sam = ns_a

    # A_s_SAM
    As_a = A_s_sam_path_a(eta_SAM)
    As_b = A_s_sam_path_b()
    As_rel = abs(As_a - As_b) / As_a
    A_s_sam = As_a

    # tau_SAM
    tau_a = tau_sam_path_a()
    tau_b = tau_sam_path_b()
    tau_rel = abs(tau_a - tau_b) / tau_a
    tau_sam = tau_a

    print(f"  eta_SAM Path A    = {eta_a:.15e}")
    print(f"  eta_SAM Path B    = {eta_b:.15e}")
    print(f"  |rel diff|        = {eta_rel:.3e}")
    print()
    print(f"  n_s_SAM Path A    = {ns_a:.15e}")
    print(f"  n_s_SAM Path B    = {ns_b:.15e}")
    print(f"  |rel diff|        = {ns_rel:.3e}")
    print()
    print(f"  A_s_SAM Path A    = {As_a:.15e}")
    print(f"  A_s_SAM Path B    = {As_b:.15e}")
    print(f"  |rel diff|        = {As_rel:.3e}")
    print()
    print(f"  tau_SAM Path A    = {tau_a:.15e}")
    print(f"  tau_SAM Path B    = {tau_b:.15e}")
    print(f"  |rel diff|        = {tau_rel:.3e}")
    print()

    # sigma deviations
    sigma_dev_As  = (A_s_sam  - A_S_REF) / SIGMA_AS
    sigma_dev_ns  = (n_s_sam  - N_S_REF) / SIGMA_NS
    sigma_dev_tau = (tau_sam  - TAU_REF) / SIGMA_TAU
    sigma_devs = dict(As=sigma_dev_As, ns=sigma_dev_ns, tau=sigma_dev_tau)

    p1_band = band(sigma_dev_As)
    p2_band = band(sigma_dev_ns)
    p3_band = band(sigma_dev_tau)
    bands_per_param = dict(As=p1_band, ns=p2_band, tau=p3_band)

    strong_contact = dict(
        As=(abs(sigma_dev_As)  <= 0.5),
        ns=(abs(sigma_dev_ns)  <= 0.5),
        tau=(abs(sigma_dev_tau) <= 0.5),
    )

    print(f"  Frozen references:")
    print(f"    A_s_ref = {A_S_REF:.3e} +/- {SIGMA_AS:.3e}")
    print(f"    n_s_ref = {N_S_REF}        +/- {SIGMA_NS}")
    print(f"    tau_ref = {TAU_REF}        +/- {SIGMA_TAU}")
    print()
    print(f"  A_s_SAM  = {A_s_sam:.10e}  sigma_dev = {sigma_dev_As:+.4f}  -> {p1_band}  "
          f"STRONG={strong_contact['As']}")
    print(f"  n_s_SAM  = {n_s_sam:.10f}        sigma_dev = {sigma_dev_ns:+.4f}  -> {p2_band}  "
          f"STRONG={strong_contact['ns']}")
    print(f"  tau_SAM  = {tau_sam:.10f}        sigma_dev = {sigma_dev_tau:+.4f}  -> {p3_band}  "
          f"STRONG={strong_contact['tau']}")
    print()

    # E1 wrong-controls for A_s
    wrongs = wrong_controls_for_As(eta_SAM)
    print("  E1 wrong-control comparators for A_s (smaller |sigma_dev| is better):")
    for lbl, val, dev in wrongs:
        marker = "  <-- CANONICAL" if "[chosen]" in lbl else ""
        print(f"    {lbl:<32s} value = {val:.4e}  sigma_dev = {dev:+.4f}{marker}")
    print()

    # E2 self-lifted tau alternative
    tau_alt = 2.0 * A_0 * (1.0 + A_0)
    sigma_dev_tau_alt = (tau_alt - TAU_REF) / SIGMA_TAU
    print(f"  E2 self-lifted tau alternative (reported only):")
    print(f"    tau_alt = 2*A_0*(1+A_0) = {tau_alt:.12f}  sigma_dev = {sigma_dev_tau_alt:+.4f}")
    print()

    # Verdict
    verdict = combine_verdict(p1_band, p2_band, p3_band)
    if verdict == "PASS":
        verdict_token = (
            "CR037A_PASS_SAM_PERTURBATION_TRIPLET_WITHIN_1SIGMA_PLANCK_POSTERIOR"
        )
    elif verdict == "BOUNDARY":
        verdict_token = (
            "CR037A_BOUNDARY_AT_LEAST_ONE_PARAMETER_BETWEEN_1_AND_2_SIGMA"
        )
    else:
        verdict_token = (
            "CR037A_FAIL_AT_LEAST_ONE_PARAMETER_BEYOND_2_SIGMA"
        )

    print(f"  P1 (A_s) = {p1_band}")
    print(f"  P2 (n_s) = {p2_band}")
    print(f"  P3 (tau) = {p3_band}")
    print(f"\n=== CR037A VERDICT: {verdict} ===")
    print(f"    {verdict_token}")

    # ----- Emit artifacts -----
    summary = dict(
        precommit_sha256="1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78",
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
        substrate=dict(R=R, D=D, S=S, alpha_H=ALPHA_H, Theta=THETA,
                       M=M_CAP, L=L, V=V, A_0=A_0, chi=CHI),
        eta=dict(eta_SAM_path_A=eta_a, eta_SAM_path_B=eta_b,
                 machine_precision_rel_diff=eta_rel),
        identities=dict(
            n_s_SAM_path_A=ns_a, n_s_SAM_path_B=ns_b,
            n_s_SAM=n_s_sam, n_s_path_rel_diff=ns_rel,
            A_s_SAM_path_A=As_a, A_s_SAM_path_B=As_b,
            A_s_SAM=A_s_sam, A_s_path_rel_diff=As_rel,
            tau_SAM_path_A=tau_a, tau_SAM_path_B=tau_b,
            tau_SAM=tau_sam, tau_path_rel_diff=tau_rel,
        ),
        references=dict(
            A_s_reference=A_S_REF, sigma_As=SIGMA_AS,
            n_s_reference=N_S_REF, sigma_ns=SIGMA_NS,
            tau_reference=TAU_REF, sigma_tau=SIGMA_TAU,
        ),
        sigma_deviations=dict(
            sigma_dev_As=sigma_dev_As,
            sigma_dev_ns=sigma_dev_ns,
            sigma_dev_tau=sigma_dev_tau,
        ),
        gates=dict(P1=p1_band, P2=p2_band, P3=p3_band),
        strong_contact=strong_contact,
        E1_wrong_controls_for_As=[
            dict(label=lbl, value=v, sigma_dev=dev) for lbl, v, dev in wrongs
        ],
        E2_tau_alternative=dict(
            tau_alt_formula="2*A_0*(1+A_0)",
            tau_alt_value=tau_alt,
            sigma_dev_tau_alt=sigma_dev_tau_alt,
            note="Reported only; canonical CR037A tau is 2*A_0 = 1/(6*pi).",
        ),
    )

    out_summary = CR_DIR / "CR037A_summary.json"
    out_summary.write_text(json.dumps(summary, indent=2, default=_jsonify),
                           encoding="utf-8")

    write_evidence_csv(CR_DIR / "CR037A_evidence_rows.csv",
                       eta_a, eta_b, ns_a, ns_b, As_a, As_b, tau_a, tau_b,
                       A_s_sam, n_s_sam, tau_sam,
                       sigma_devs, bands_per_param, strong_contact, wrongs,
                       tau_alt, sigma_dev_tau_alt)

    # Result markdown
    result_md = f"""# CR037A_SAM_PERTURBATION_SELECTOR

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
precommit_sha256             = 1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78
```

## Substrate Identities Under Test

| parameter | identity | SAM value |
|---|---|---:|
| A_s | η_SAM · √R = 7·√R / (4·(12π)⁶) | {A_s_sam:.10e} |
| n_s | 1 − χ/2 = 1 − 1/(9π) | {n_s_sam:.10f} |
| τ | 2·A_0 = 1/(6π) | {tau_sam:.10f} |

η_SAM verified from substrate atoms (Path A vs Path B agree to {eta_rel:.2e}).

## Frozen Planck References (in-code; NOT file-read)

| field | value |
|---|---:|
| A_s_reference | {A_S_REF:.3e} ± {SIGMA_AS:.3e} |
| n_s_reference | {N_S_REF} ± {SIGMA_NS} |
| τ_reference | {TAU_REF} ± {SIGMA_TAU} |

## P1, P2, P3 — Selector Gates

| param | SAM value | σ_dev | band | STRONG_CONTACT |
|---|---:|---:|---|---:|
| **A_s** (P1) | {A_s_sam:.10e} | **{sigma_dev_As:+.4f}** | **{p1_band}** | {strong_contact['As']} |
| **n_s** (P2) | {n_s_sam:.10f} | **{sigma_dev_ns:+.4f}** | **{p2_band}** | {strong_contact['ns']} |
| **τ** (P3) | {tau_sam:.10f} | **{sigma_dev_tau:+.4f}** | **{p3_band}** | {strong_contact['tau']} |

Bands: PASS ≤ 1.0σ; BOUNDARY (1.0σ, 2.0σ]; FAIL > 2.0σ.
STRONG_CONTACT_X: |σ_dev| ≤ 0.5.

## E1 — Wrong-Control Comparators for A_s

| comparator | value | σ_dev vs A_s_ref |
|---|---:|---:|
"""
    for lbl, val, dev in wrongs:
        marker = "  ← canonical" if "[chosen]" in lbl else ""
        result_md += f"| {lbl}{marker} | {val:.4e} | {dev:+.4f} |\n"
    result_md += f"""
The canonical A_s_SAM = η·√R earns its place if its |σ_dev| is the
smallest of the set (or tied for smallest). Reported as evidence.

## E2 — Self-Lifted τ Alternative (reported only)

```text
tau_alt = 2 * A_0 * (1 + A_0) = {tau_alt:.12f}
sigma_dev_tau_alt = {sigma_dev_tau_alt:+.4f}
```

Canonical CR037A τ is 2·A_0 = 1/(6π); the self-lifted form is reported
for completeness and is NOT used in the P3 gate.

## E3 — Algebraic Two-Path Checks (machine precision)

| identity | Path A − Path B (relative) |
|---|---:|
| η_SAM | {eta_rel:.3e} |
| n_s,SAM | {ns_rel:.3e} |
| A_s,SAM | {As_rel:.3e} |
| τ_SAM | {tau_rel:.3e} |

## Chronology

```text
CR037A is the selector test for the SAM perturbation triplet. It does
NOT consult any CMB spectrum, likelihood, chain, or posterior table at
runtime. It computes three closed-form substrate values and compares
them to frozen Planck 2018 posterior centroids declared as numeric
constants in the precommit. If CR037A PASSes, CR037B follows: the
CR036B pipeline with these three SAM values replacing the Planck-
centroid perturbation inputs.

The runner did not open any CR036, CR036B, CR035A, or CR035A2 file at
runtime; the forbidden-file guard did not trip (opened_paths_count =
{len(OPENED_PATHS)}; forbidden_files_opened = false).
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78
eta_SAM source = CR036 sealed PASS (precommit 345a1a8d...; eta_SAM verified in CR037A runner from atoms)
```

---

**Sealed by:** CR037A runner, 2026-06-27.
"""
    (CR_DIR / "CR037A_result.md").write_text(result_md, encoding="utf-8")
    print(f"\nWrote artifacts to {CR_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
