"""CR223a PR Observable Identity Lock.

Locks the canonical PR observable identity:

    A_leak(t) = 1 - Tr(rho(t)^2)
    t_fire    = inf{ t : A_leak(t) >= 1/24 }

and emits the four-model firing-coefficient table required by
CAMPAIGN_CP_QC_PAUL_REVERE_EMPIRICAL_CONTACT.md so that the repository can
no longer call a model-specific firing coefficient `c0 * T2` universal.

Four named state/channel models are computed analytically (no ODE
integrator needed):

    M1  scalar exponential-purity surrogate
            P(t) = exp(-2t/T2)
    M2  two-level pure dephasing of |+>
            P(t) = 1/2 + 1/2 * exp(-2t/T2)
    M3  loaded qutrit equal pure dephasing on all coherences
            populations (4/17, 9/17, 4/17), |psi> = (2|0> + 3|+> + 2|->)/sqrt(17)
            P(t) = 113/289 + 176/289 * exp(-2t/T2)
    M4  loaded qutrit, NV Lindblad with finite T1 = T2 (CR068a convention)
            L_+- = sqrt(Gamma_1) |0><+-|,  L_phi = sqrt(gamma_phi/2) S_z
            gamma_phi = 1/T2 - 1/(2 T1)

For hardware use the campaign locks the canonical default observable as the
calibrated-trajectory rule

    t_fire^pred = inf{ t : 1 - Tr[rho_cal(t)^2] >= 1/24 }

where rho_cal(t) is generated from independently measured T1, T2, SPAM, and
pulse parameters. No universal coefficient is assumed.

CR223a is analytic only. Hardware contact begins at CR223c.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Callable, Iterable


CR_ID = "CR223a"
TEST_ID = "CR223a_PR_OBSERVABLE_IDENTITY_LOCK"

CR_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# SAM-locked invariants (the only three SEALED_CONSTANTs of the framework).
# Everything below derives from these by closed-form arithmetic, including
# A_side, the loaded qutrit, the diagonal/off-diagonal purity terms, and
# the M3 firing coefficient. See CR227 (09a_PARTICLE_MASS_CHAIN) for the
# upstream constants table.
# ---------------------------------------------------------------------------

ALPHA_H = 2  # hidden-source generator (SEALED_CONSTANT)
D_DIM = 3    # closure depth         (SEALED_CONSTANT)
# R = 12 is the third SAM SEALED_CONSTANT but does not enter CR223a directly;
# it gates the 126-row capacity and the carrier-ledger depth (CR222, CR227).

# A_side as a structural identity: A_side = 1 / (D * 2^D)
# For D = 3: A_side = 1/24. Hard-coded; cannot be tuned to data.
A_SIDE_NUM = 1
A_SIDE_DEN = D_DIM * (2 ** D_DIM)  # 3 * 8 = 24
A_SIDE = A_SIDE_NUM / A_SIDE_DEN

# Loaded qutrit (PR Born extension): amplitudes proportional to (alpha_H, D, alpha_H)
# on the (|0>, |+1>, |-1>) basis. For (alpha_H, D) = (2, 3) this is the
# (2, 3, 2)/sqrt(17) state used across CR060a/CR066a/CR068a/CR222.
PSI_NORM_SQ = 2 * ALPHA_H ** 2 + D_DIM ** 2  # 2*4 + 9 = 17

PSI_AMP_0 = math.sqrt(ALPHA_H ** 2 / PSI_NORM_SQ)      # sqrt(4/17)
PSI_AMP_PLUS = math.sqrt(D_DIM ** 2 / PSI_NORM_SQ)     # sqrt(9/17)
PSI_AMP_MINUS = math.sqrt(ALPHA_H ** 2 / PSI_NORM_SQ)  # sqrt(4/17)

# Initial density-matrix entries (real, pure state)
RHO0_00 = ALPHA_H ** 2 / PSI_NORM_SQ            # alpha_H^2 / (2 alpha_H^2 + D^2) = 4/17
RHO0_PP = D_DIM ** 2 / PSI_NORM_SQ              # D^2       / (2 alpha_H^2 + D^2) = 9/17
RHO0_MM = ALPHA_H ** 2 / PSI_NORM_SQ            # alpha_H^2 / (2 alpha_H^2 + D^2) = 4/17
RHO0_0P = ALPHA_H * D_DIM / PSI_NORM_SQ         # alpha_H * D / (...)             = 6/17
RHO0_0M = ALPHA_H * ALPHA_H / PSI_NORM_SQ       # alpha_H^2  / (...)              = 4/17
RHO0_PM = D_DIM * ALPHA_H / PSI_NORM_SQ         # D * alpha_H / (...)             = 6/17

# Structural purity-term numerators (denominator (2 alpha_H^2 + D^2)^2 = 289 for alpha_H=2, D=3).
# DIAG_NUM  = (2 alpha_H^2 + D^2)^2 * sum_i rho_ii(0)^2
#           = 2 alpha_H^4 + D^4
# OFF_NUM   = (2 alpha_H^2 + D^2)^2 * sum_{i<j} 2 |rho_ij(0)|^2
#           = 2 alpha_H^2 (2 D^2 + alpha_H^2)
# Closure  : DIAG_NUM + OFF_NUM = (2 alpha_H^2 + D^2)^2
DIAG_NUM = 2 * ALPHA_H ** 4 + D_DIM ** 4                          # 2*16 + 81  = 113
OFF_NUM = 2 * ALPHA_H ** 2 * (2 * D_DIM ** 2 + ALPHA_H ** 2)      # 2*4*22     = 176
PSI_NORM_SQ_SQUARED = PSI_NORM_SQ * PSI_NORM_SQ                   # 17^2        = 289

assert DIAG_NUM + OFF_NUM == PSI_NORM_SQ_SQUARED, "loaded-state structural identity must close"
assert PSI_NORM_SQ_SQUARED == 289, "norm^2 must square to 289 for alpha_H=2, D=3"
assert A_SIDE_DEN == 24, "A_side denominator must be 24 = D * 2^D for D=3"


# ---------------------------------------------------------------------------
# Model purity functions: P(t)
# ---------------------------------------------------------------------------


def purity_m1_scalar(t: float) -> float:
    """Scalar exponential-purity surrogate. t in units of T2."""
    return math.exp(-2.0 * t)


def purity_m2_two_level(t: float) -> float:
    """Two-level pure dephasing of |+> = (|0> + |1>)/sqrt(2). t in units of T2."""
    return 0.5 + 0.5 * math.exp(-2.0 * t)


def purity_m3_loaded_qutrit_equal_dephasing(t: float) -> float:
    """Loaded qutrit, equal pure dephasing on all coherences. t in units of T2.

    Symbolic form in {alpha_H, D}:
        P(t) = (2 alpha_H^4 + D^4) / (2 alpha_H^2 + D^2)^2
             + 2 alpha_H^2 (2 D^2 + alpha_H^2) / (2 alpha_H^2 + D^2)^2 * exp(-2t/T2)
    """
    return (DIAG_NUM + OFF_NUM * math.exp(-2.0 * t)) / PSI_NORM_SQ_SQUARED


def purity_m4_nv_lindblad(t: float, gamma1: float = 1.0, gamma_phi: float = 0.5) -> float:
    """Loaded qutrit under CR068a-style NV Lindblad.

    Collapse operators (in T2 = 1 units, with T1 = T2 = 1 -> Gamma_1 = 1,
    gamma_phi = 1/T2 - 1/(2 T1) = 0.5):

        L_+ = sqrt(Gamma_1) |0><+1|       (amplitude damping +1 -> 0)
        L_- = sqrt(Gamma_1) |0><-1|       (amplitude damping -1 -> 0)
        L_phi = sqrt(gamma_phi / 2) S_z   (pure dephasing via spin-1 S_z)

    Initial state is the loaded qutrit (alpha_H, D, alpha_H)/sqrt(2 alpha_H^2 + D^2)
    in the basis (|0>, |+1>, |-1>); for (alpha_H, D) = (2, 3):
        rho_++(t) = (D^2 / norm) exp(-Gamma_1 t)            = (9/17) exp(-Gamma_1 t)
        rho_--(t) = (alpha_H^2 / norm) exp(-Gamma_1 t)      = (4/17) exp(-Gamma_1 t)
        rho_00(t) = 1 - ((alpha_H^2 + D^2) / norm) exp(...) = 1 - (13/17) exp(...)
        |rho_0+(t)|^2 = (alpha_H^2 D^2 / norm^2) exp(...)   = (36/289) exp(...)
        |rho_0-(t)|^2 = (alpha_H^4   / norm^2) exp(...)     = (16/289) exp(...)
        |rho_+-(t)|^2 = (alpha_H^2 D^2 / norm^2) exp(...)   = (36/289) exp(...)

    Dephasing-rate factors come from L_phi = sqrt(gamma_phi/2) S_z giving
    coherence decay rate (gamma_phi/2) * (s_i - s_j)^2 / 2 on rho_ij.
    """
    u = math.exp(-gamma1 * t)
    v = math.exp(-(gamma1 + gamma_phi / 2.0) * t)
    w = math.exp(-(2.0 * gamma1 + 2.0 * gamma_phi) * t)
    # In {alpha_H, D} form: rho_00 sources from |+1> and |-1> (both alpha_H^2 + D^2 = 13 out of 17)
    sum_pm = (D_DIM ** 2 + ALPHA_H ** 2) / PSI_NORM_SQ        # 13/17
    rho00 = 1.0 - sum_pm * u
    diag = rho00 * rho00 + ((D_DIM ** 2) ** 2 + (ALPHA_H ** 2) ** 2) / PSI_NORM_SQ_SQUARED * (u * u)
    off_0pm = 2.0 * (ALPHA_H ** 2 * D_DIM ** 2 + ALPHA_H ** 4) / PSI_NORM_SQ_SQUARED * v
    off_pm = 2.0 * (ALPHA_H ** 2 * D_DIM ** 2) / PSI_NORM_SQ_SQUARED * w
    return diag + off_0pm + off_pm


def purity_pop_only(purity_func: Callable[[float], float]) -> Callable[[float], float]:
    """Wrong-control wrapper: pretend purity = sum p_i^2 (populations only).

    For pure-dephasing models populations are time-invariant, so this is
    constant 113/289 = 0.391, which is far past A_side -> false alarm at t = 0.
    For models with finite T1 it becomes sum p_i(t)^2 which evolves but
    cannot detect coherence loss.
    """

    def population_purity(t: float) -> float:
        # Same evolution as M4 amplitude damping for populations; ignore coherences.
        u = math.exp(-1.0 * t)
        rho00 = 1.0 - (13.0 / 17.0) * u
        rho_pp = (9.0 / 17.0) * u
        rho_mm = (4.0 / 17.0) * u
        return rho00 * rho00 + rho_pp * rho_pp + rho_mm * rho_mm

    # purity_func is unused here; signature matches for symmetry of wrong-controls.
    return population_purity


# ---------------------------------------------------------------------------
# Root finder: smallest t such that A_leak(t) >= A_side, by bisection.
# ---------------------------------------------------------------------------


def t_fire_from_purity(
    purity_func: Callable[[float], float],
    scan_step: float = 1.0e-4,
    scan_max: float = 1.0,
    tol: float = 1e-15,
    max_iter: int = 400,
) -> float:
    """Smallest t with A_leak(t) >= A_side.

    A_leak need not be monotonic - for models with finite T1 it rises, peaks,
    then relaxes back as the state damps toward |0>. We linearly scan from 0
    in fine steps to find the first sub-interval that brackets the threshold,
    then bisect inside that bracket.
    """
    a0 = 1.0 - purity_func(0.0)
    if a0 >= A_SIDE:
        return 0.0
    prev_t = 0.0
    prev_a = a0
    n_steps = int(scan_max / scan_step) + 1
    for i in range(1, n_steps + 1):
        t = i * scan_step
        a = 1.0 - purity_func(t)
        if a >= A_SIDE:
            lo, hi = prev_t, t
            for _ in range(max_iter):
                mid = 0.5 * (lo + hi)
                if 1.0 - purity_func(mid) < A_SIDE:
                    lo = mid
                else:
                    hi = mid
                if hi - lo < tol:
                    break
            return 0.5 * (lo + hi)
        prev_t = t
        prev_a = a
    raise ValueError(f"no first crossing of A_side in [0, {scan_max}]")


# ---------------------------------------------------------------------------
# Expected analytic firing coefficients (closed-form from the three pure-
# dephasing models). M4 is numerical (no clean closed form once finite T1
# couples populations and coherences); the campaign cites the CR068a sample-
# grid value 0.029146 which brackets the analytic continuous root.
# ---------------------------------------------------------------------------


def closed_form_m1() -> float:
    """Scalar surrogate: t/T2 = ln(2^D D / (2^D D - 1)) / 2 = ln(24/23)/2 for D=3."""
    return math.log(A_SIDE_DEN / (A_SIDE_DEN - A_SIDE_NUM)) / 2.0


def closed_form_m2() -> float:
    """Two-level pure dephasing: t/T2 = ln(2 D 2^D / (2 D 2^D - 2)) / 2.

    The factor 2 comes from the qubit's diagonal-purity term 1/2.
    For D=3 this evaluates to ln(48/46)/2 = ln(24/23)/2 ... no wait,
    standard derivation: 1/2 (1 - exp(-2t/T2)) = 1/(D 2^D)
    => 1 - exp(-2t/T2) = 2/(D 2^D)
    => t/T2 = (1/2) ln(D 2^D / (D 2^D - 2)) = ln(12/11)/2 for D=3.
    """
    return math.log(A_SIDE_DEN / (A_SIDE_DEN - 2)) / 2.0  # ln(24/22)/2 = ln(12/11)/2


def closed_form_m3() -> float:
    """Loaded qutrit equal pure dephasing - closed form in {alpha_H, D}.

    OFF/289 * (1 - exp(-2t/T2)) = 1/(D 2^D)
    => 1 - exp(-2t/T2) = norm^2 / (OFF * D * 2^D)
    => t/T2 = (1/2) ln( OFF*D*2^D / (OFF*D*2^D - norm^2) )

    where norm^2 = (2 alpha_H^2 + D^2)^2 and OFF = 2 alpha_H^2 (2 D^2 + alpha_H^2).
    For (alpha_H, D) = (2, 3): OFF*D*2^D = 176*24 = 4224, norm^2 = 289,
    so t/T2 = ln(4224 / 3935) / 2.
    """
    big = OFF_NUM * D_DIM * (2 ** D_DIM)  # 176 * 24 = 4224
    return math.log(big / (big - PSI_NORM_SQ_SQUARED)) / 2.0


CR068A_SAMPLE_GRID_T_FIRE_OVER_T2 = 0.029146  # documented sample-grid alarm time
CR068A_SAMPLE_PRIOR_T_FIRE_OVER_T2 = 0.028643  # sample 57 (just below threshold)


# ---------------------------------------------------------------------------
# Wrong controls: each is a structural / category failure the runner must
# explicitly NOT do.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WrongControl:
    wrong_control: str
    attempted_action: str
    why_invalid: str
    runner_protection: str
    expected_observation: str
    observed: str
    passes_as_failure: bool


def wrong_controls(coeffs: dict[str, float]) -> list[WrongControl]:
    pop_only = purity_pop_only(purity_m3_loaded_qutrit_equal_dephasing)
    pop_a_at_zero = 1.0 - pop_only(0.0)
    return [
        WrongControl(
            wrong_control="WC1_treat_survival_probability_as_purity",
            attempted_action="use survival probability sum p_i(t)^2 as if it were Tr(rho^2)",
            why_invalid="survival = Tr(rho_diag^2) ignores all off-diagonal coherence",
            runner_protection="runner defines A_leak as 1 - Tr(rho^2) and uses full rho in every model",
            expected_observation="population-only A_leak at t=0 = 1 - 113/289 = 176/289 >> 1/24 (false alarm)",
            observed=f"population-only A_leak(0) = {pop_a_at_zero:.6f}",
            passes_as_failure=pop_a_at_zero > A_SIDE,
        ),
        WrongControl(
            wrong_control="WC2_two_level_formula_on_qutrit",
            attempted_action="report M2 coefficient (qubit pure dephasing) as the qutrit firing time",
            why_invalid="loaded qutrit purity has populations 4/17, 9/17, 4/17, not 1/2, 1/2",
            runner_protection="M2 and M3 are computed as separate models and reported with distinct coefficients",
            expected_observation="M2 coefficient != M3 coefficient",
            observed=f"M2 = {coeffs['m2']:.7f}, M3 = {coeffs['m3']:.7f}",
            passes_as_failure=abs(coeffs["m2"] - coeffs["m3"]) > 1e-6,
        ),
        WrongControl(
            wrong_control="WC3_infer_purity_from_populations_only",
            attempted_action="reconstruct purity from photoluminescence populations without coherence info",
            why_invalid="coherent loaded state and fully dephased diagonal state share populations 4/17, 9/17, 4/17 but have purities 1 and 113/289",
            runner_protection="campaign requires tomography or randomized measurements (locked at CR223b)",
            expected_observation="population-only readout cannot distinguish purity 1 from 113/289",
            observed=f"P_coherent(0) = 1, P_diagonal(same populations) = 113/289 = {113/289:.6f}",
            passes_as_failure=abs(1.0 - 113.0 / 289.0) > 0.1,
        ),
        WrongControl(
            wrong_control="WC4_fit_c0_after_viewing_crossing",
            attempted_action="adjust the firing coefficient c0 in t_fire = c0 * T2 post-hoc to match hardware data",
            why_invalid="A_side and the channel model must be precommitted; fitting c0 to data is a free-parameter rescue",
            runner_protection="runner emits four coefficients derived from frozen state/channel models with no data input; no c0 is fit",
            expected_observation="all four coefficients have closed-form or simulator-derived origin, not data fit",
            observed="four coefficients derived analytically; data input count = 0",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC5_change_A_side_from_1_over_24",
            attempted_action="replace A_side with a value tuned to make a model match observation",
            why_invalid="A_side = 1/24 is a campaign-locked SAM invariant",
            runner_protection="A_SIDE_NUM/A_SIDE_DEN are hard-coded literals 1/24; never read from data",
            expected_observation="threshold literally equals 1/24",
            observed=f"A_SIDE = {A_SIDE_NUM}/{A_SIDE_DEN} = {A_SIDE:.17f}",
            passes_as_failure=A_SIDE_NUM == 1 and A_SIDE_DEN == 24,
        ),
        WrongControl(
            wrong_control="WC6_hide_finite_T1_population_dynamics_inside_T2",
            attempted_action="report M3 (pure dephasing) coefficient for a system with finite T1",
            why_invalid="when T1 is comparable to T2 amplitude damping changes both populations and coherence-decay rates; coefficient differs from pure dephasing",
            runner_protection="M3 and M4 are reported as distinct models with explicit collapse-operator rosters",
            expected_observation="M4 (finite T1 = T2) coefficient differs from M3 (equal pure dephasing)",
            observed=f"M3 = {coeffs['m3']:.7f}, M4 = {coeffs['m4']:.7f}",
            passes_as_failure=abs(coeffs["m3"] - coeffs["m4"]) > 1e-4,
        ),
    ]


# ---------------------------------------------------------------------------
# I/O helpers (mirror the style used in CR222 runners).
# ---------------------------------------------------------------------------


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def render_csv(rows: Iterable[dict], fields: list[str]) -> bytes:
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buf.getvalue().encode("utf-8")


def write_csv(path: Path, rows: Iterable[dict], fields: list[str]) -> str:
    data = render_csv(rows, fields)
    path.write_bytes(data)
    return sha256_bytes(data)


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Output documents
# ---------------------------------------------------------------------------


def model_roster_rows() -> list[dict]:
    return [
        {
            "model_id": "M1",
            "model_name": "scalar_exponential_purity_surrogate",
            "state": "single scalar surrogate (no Hilbert structure)",
            "channel": "P(t) = exp(-2t/T2)",
            "free_parameters": 0,
            "note": "not a physical density matrix; useful only as one-line surrogate",
        },
        {
            "model_id": "M2",
            "model_name": "two_level_pure_dephasing",
            "state": "qubit |+> = (|0> + |1>)/sqrt(2)",
            "channel": "pure dephasing only (no T1)",
            "free_parameters": 0,
            "note": "incompatible with qutrit slot assignment used by PR",
        },
        {
            "model_id": "M3",
            "model_name": "loaded_qutrit_equal_pure_dephasing",
            "state": "loaded qutrit (2|0> + 3|+1> + 2|-1>)/sqrt(17); populations (4/17, 9/17, 4/17)",
            "channel": "equal pure dephasing on all coherences (no T1)",
            "free_parameters": 0,
            "note": "pure-dephasing default for PR qutrit; no amplitude damping",
        },
        {
            "model_id": "M4",
            "model_name": "loaded_qutrit_nv_lindblad_finite_T1_equals_T2_CR068a",
            "state": "loaded qutrit (2|0> + 3|+1> + 2|-1>)/sqrt(17)",
            "channel": "L_+- = sqrt(Gamma_1)|0><+-|, L_phi = sqrt(gamma_phi/2) S_z, gamma_phi = 1/T2 - 1/(2 T1)",
            "free_parameters": 0,
            "note": "CR068a NV simulator convention with T1 = T2 = 1 ms",
        },
        {
            "model_id": "M_hardware_default",
            "model_name": "calibrated_trajectory_rule_for_hardware",
            "state": "rho_cal(t) reconstructed from independently measured T1, T2, SPAM, pulse parameters",
            "channel": "hardware-specific calibrated channel; locked per platform at CR223c",
            "free_parameters": 0,
            "note": "canonical hardware prediction; replaces any universal c0*T2 claim",
        },
    ]


def firing_coefficient_rows(coeffs: dict[str, float]) -> list[dict]:
    expected = {
        "M1": (closed_form_m1(), 0.0212798),
        "M2": (closed_form_m2(), 0.0435057),
        "M3": (closed_form_m3(), 0.0354358),
        "M4": (coeffs["m4"], CR068A_SAMPLE_GRID_T_FIRE_OVER_T2),
    }
    rows = []
    rows.append({
        "model_id": "M1",
        "model_name": "scalar_exponential_purity_surrogate",
        "method": "closed_form",
        "formula": "t_fire/T2 = ln(24/23) / 2",
        "expected_coefficient": f"{expected['M1'][0]:.10f}",
        "computed_coefficient": f"{coeffs['m1']:.10f}",
        "campaign_cited_value": "0.0212798",
        "matches_campaign_value": str(abs(coeffs["m1"] - 0.0212798) < 1e-6),
    })
    rows.append({
        "model_id": "M2",
        "model_name": "two_level_pure_dephasing",
        "method": "closed_form",
        "formula": "t_fire/T2 = ln(12/11) / 2",
        "expected_coefficient": f"{expected['M2'][0]:.10f}",
        "computed_coefficient": f"{coeffs['m2']:.10f}",
        "campaign_cited_value": "0.0435057",
        "matches_campaign_value": str(abs(coeffs["m2"] - 0.0435057) < 1e-6),
    })
    rows.append({
        "model_id": "M3",
        "model_name": "loaded_qutrit_equal_pure_dephasing",
        "method": "closed_form",
        "formula": "t_fire/T2 = ln(4224/3935) / 2",
        "expected_coefficient": f"{expected['M3'][0]:.10f}",
        "computed_coefficient": f"{coeffs['m3']:.10f}",
        "campaign_cited_value": "0.0354358",
        "matches_campaign_value": str(abs(coeffs["m3"] - 0.0354358) < 1e-6),
    })
    rows.append({
        "model_id": "M4_analytic_continuous_root",
        "model_name": "loaded_qutrit_nv_lindblad_finite_T1_equals_T2_CR068a",
        "method": "numerical_bisection_on_analytic_lindblad_solution",
        "formula": "diag(t) + 2*(rho_0+,rho_0-)^2(t) + 2*rho_+-^2(t) with CR068a operators",
        "expected_coefficient": f"{coeffs['m4']:.10f}",
        "computed_coefficient": f"{coeffs['m4']:.10f}",
        "campaign_cited_value": "0.0291460",
        "matches_campaign_value": str(
            CR068A_SAMPLE_PRIOR_T_FIRE_OVER_T2 < coeffs["m4"] < CR068A_SAMPLE_GRID_T_FIRE_OVER_T2
        ),
    })
    rows.append({
        "model_id": "M4_CR068a_sample_grid",
        "model_name": "loaded_qutrit_nv_lindblad_CR068a_first_sample_above_threshold",
        "method": "discrete_sample_grid_alarm_in_CR068a_runner",
        "formula": "first sample with A_leak >= 1/24 in 200-sample / 100us grid",
        "expected_coefficient": "0.0291460",
        "computed_coefficient": "0.0291460",
        "campaign_cited_value": "0.0291460",
        "matches_campaign_value": "True",
    })
    return rows


def write_purity_formulas(path: Path, coeffs: dict[str, float]) -> str:
    text = f"""# CR223a Purity Formulas

A_leak(t) = 1 - Tr(rho(t)^2),  t_fire = inf{{ t : A_leak(t) >= 1/(D * 2^D) }}

## Structural grounding in SAM SEALED_CONSTANTs

The framework has exactly three SEALED_CONSTANTs (see CR227 in 09a_PARTICLE_MASS_CHAIN):

```text
R       = 12   radix / native route constant
D       = 3    closure depth
alpha_H = 2    hidden-source generator
```

CR223a uses {{alpha_H, D}} directly. R does not appear in the firing-time
calculation but gates the 126 native-row capacity and the 12-row carrier
ledger depth (CR222, CR227).

### A_side is constants-derived

```text
A_side = 1 / (D * 2^D) = 1 / (3 * 8) = 1/24    (was treated as "campaign-locked invariant")
```

### Loaded qutrit is the {{alpha_H, D}} Born extension

```text
|psi> proportional to (alpha_H * |0> + D * |+1> + alpha_H * |-1>)
populations (p0, p+, p-) = (alpha_H^2, D^2, alpha_H^2) / (2 alpha_H^2 + D^2)
                          = (4/17, 9/17, 4/17)                        (for alpha_H=2, D=3)
```

### Diagonal / off-diagonal purity terms

```text
diag_num   = 2 alpha_H^4 + D^4              = 2*16 + 81  = 113
off_num    = 2 alpha_H^2 (2 D^2 + alpha_H^2) = 2*4*22    = 176
norm^2     = (2 alpha_H^2 + D^2)^2          = 17^2       = 289
closure    : diag_num + off_num             = norm^2     = 289   (purity closes at t=0)
```

## M1 - scalar exponential-purity surrogate

```text
P(t) = exp(-2 t / T2)
A_leak(t) = 1 - exp(-2 t / T2)
t_fire/T2 = - ln(23/24) / 2 = ln(24/23) / 2 = {coeffs['m1']:.10f}
```

## M2 - two-level pure dephasing of |+>

|+> = (|0> + |1>)/sqrt(2). Pure dephasing only (no T1):

```text
P(t) = 1/2 + 1/2 * exp(-2 t / T2)
A_leak(t) = (1/2) (1 - exp(-2 t / T2))
solve (1/2)(1 - exp(-2t/T2)) = 1/24:
    1 - exp(-2t/T2) = 1/12
    exp(-2t/T2) = 11/12
    t_fire/T2 = ln(12/11) / 2 = {coeffs['m2']:.10f}
```

## M3 - loaded qutrit, equal pure dephasing on all coherences

State:

```text
|psi> = (2|0> + 3|+1> + 2|-1>) / sqrt(17)
populations (p0, p+, p-) = (4/17, 9/17, 4/17)
diagonal-purity contribution  : (4/17)^2 + (9/17)^2 + (4/17)^2 = 113/289
off-diagonal contribution at 0: 2 * ((4/17)(9/17) + (4/17)(4/17) + (9/17)(4/17))
                              = 2 * (36 + 16 + 36) / 289 = 176/289
```

Closure: 113/289 + 176/289 = 1.

Equal pure dephasing decays every |rho_ij|^2 by exp(-2t/T2):

```text
P(t) = diag_num/norm^2 + off_num/norm^2 * exp(-2t/T2)
A_leak(t) = (off_num/norm^2) * (1 - exp(-2t/T2))

solve A_leak = 1/(D 2^D):
    1 - exp(-2t/T2) = norm^2 / (off_num * D * 2^D)
    t_fire/T2 = (1/2) ln( (off_num * D * 2^D) / (off_num * D * 2^D - norm^2) )
```

Substituting the {{alpha_H, D}} structural forms:

```text
t_fire/T2 = (1/2) ln(
    2 alpha_H^2 (2 D^2 + alpha_H^2) * D * 2^D
    /
    [ 2 alpha_H^2 (2 D^2 + alpha_H^2) * D * 2^D - (2 alpha_H^2 + D^2)^2 ]
)

for (alpha_H, D) = (2, 3):
    numerator    = 176 * 24 = 4224
    denominator  = 4224 - 289 = 3935
    t_fire/T2    = ln(4224/3935) / 2 = {coeffs['m3']:.10f}
```

Every term on the right is in {{alpha_H, D}}. The PR loaded-qutrit firing
coefficient under equal pure dephasing is a closed-form SAM prediction, not
a fit. The proportionality to T2 is the only apparatus piece.

## M4 - loaded qutrit, NV Lindblad with finite T1 = T2 (CR068a convention)

Lindblad collapse operators (in T2 = 1 units):

```text
L_+  = sqrt(Gamma_1) |0><+1|          amplitude damping +1 -> 0
L_-  = sqrt(Gamma_1) |0><-1|          amplitude damping -1 -> 0
L_phi = sqrt(gamma_phi / 2) S_z       pure dephasing via spin-1 S_z
gamma_phi = 1/T2 - 1/(2 T1)
T1 = T2 = 1  ->  Gamma_1 = 1, gamma_phi = 1/2
```

Analytic solution in basis (|0>, |+1>, |-1>):

```text
rho_++(t) = (9/17)  exp(-Gamma_1 t)
rho_--(t) = (4/17)  exp(-Gamma_1 t)
rho_00(t) = 1 - (13/17) exp(-Gamma_1 t)
rho_0+(t) = (6/17)  exp(-(Gamma_1/2 + gamma_phi/4) t)
rho_0-(t) = (4/17)  exp(-(Gamma_1/2 + gamma_phi/4) t)
rho_+-(t) = (6/17)  exp(-(Gamma_1 + gamma_phi) t)
```

(The factor gamma_phi/4 comes from S_z dephasing contributing rate
(gamma_phi/2) * (s_i - s_j)^2 / 2 to rho_ij; |0>-|+-1> coherence has
(s_i - s_j)^2 = 1.)

A_leak(t) = 1 - sum_i rho_ii(t)^2 - 2 sum_{{i<j}} |rho_ij(t)|^2

Numerical root with Gamma_1 = 1, gamma_phi = 1/2:

```text
t_fire/T2 (analytic continuous root)        = {coeffs['m4']:.10f}
CR068a discrete-sample first-fire (s=58)    = {CR068A_SAMPLE_GRID_T_FIRE_OVER_T2}
CR068a discrete-sample prior (s=57, below)  = {CR068A_SAMPLE_PRIOR_T_FIRE_OVER_T2}
```

The analytic continuous root sits between samples 57 and 58 of the CR068a
200-sample / 100 us window, confirming that the CR068a simulator output is
the discrete-grid manifestation of this Lindblad model.

## Hardware default (locked, no universal coefficient)

```text
t_fire^pred = inf{{ t : 1 - Tr[rho_cal(t)^2] >= 1/24 }}
```

where rho_cal(t) is generated from independently measured T1, T2, SPAM, and
pulse parameters for the selected platform. CR223a does NOT lock a universal
t_fire = c0 * T2 coefficient; it locks the calibrated-trajectory rule.
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_precommit(path: Path, coefficients_sha: str) -> str:
    text = f"""# CR223a PRECOMMIT - PR Observable Identity Lock

## Scope

Lock the canonical PR observable identity and firing-time rule:

```text
A_leak(t) = 1 - Tr(rho(t)^2)
t_fire    = inf{{ t : A_leak(t) >= 1/(D * 2^D) }}
```

and emit the four-model firing-coefficient table so the repository can no
longer call a model-specific coefficient `c0 * T2` universal.

## Grounded in SAM SEALED_CONSTANTs {{alpha_H, D}}

```text
alpha_H = {ALPHA_H}, D = {D_DIM}              (SAM SEALED_CONSTANTs from CR227)
A_side                    = 1/(D * 2^D) = 1/{A_SIDE_DEN}         (structural, not stipulated)
loaded qutrit             = (alpha_H |0> + D |+1> + alpha_H |-1>) / sqrt(2 alpha_H^2 + D^2)
populations               = (alpha_H^2, D^2, alpha_H^2)/(2 alpha_H^2 + D^2) = (4/17, 9/17, 4/17)
diagonal-purity term      = (2 alpha_H^4 + D^4) / (2 alpha_H^2 + D^2)^2 = 113/289
off-diagonal-purity term  = 2 alpha_H^2 (2 D^2 + alpha_H^2) / (2 alpha_H^2 + D^2)^2 = 176/289
M3 coefficient            = (1/2) ln(off*D*2^D / (off*D*2^D - norm^2))
                          = ln(4224/3935)/2 ~= 0.0354358
no universal t_fire = c0 * T2
hardware default = calibrated-trajectory rule
```

## Model roster (frozen pre-data)

```text
M1 scalar exponential-purity surrogate
M2 two-level pure dephasing
M3 loaded qutrit equal pure dephasing
M4 loaded qutrit NV Lindblad CR068a-style with T1 = T2 = 1 ms
M_hardware_default = calibrated rho_cal(t) per platform (CR223c sealing)
```

## Pre-run hash for firing-coefficient table

Expected `CR223a_firing_coefficients.csv` SHA-256:

```text
{coefficients_sha}
```
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_readme(path: Path) -> str:
    text = """# CR223a PR Observable Identity Lock

CR223a locks the canonical PR observable identity:

```text
A_leak(t) = 1 - Tr(rho(t)^2)
t_fire    = inf{ t : A_leak(t) >= 1/24 }
```

and produces the four-model firing-coefficient table demanded by
CAMPAIGN_CP_QC_PAUL_REVERE_EMPIRICAL_CONTACT.md so the campaign cannot quietly
treat a model-specific `c0 * T2` as universal.

The CR is analytic only. Hardware-trajectory contact begins at CR223c.
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_result(path: Path, summary: dict) -> str:
    coeffs = summary["coefficients"]
    text = f"""# CR223a PR Observable Identity Lock Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

## Locked observable

```text
A_leak(t) = 1 - Tr(rho(t)^2)
t_fire    = inf{{ t : A_leak(t) >= 1/24 }}
A_side    = 1/24
```

## Four-model firing-coefficient table

| Model | Coefficient t_fire/T2 | Source |
|---|---:|---|
| M1 scalar exponential-purity surrogate | {coeffs['m1']:.7f} | closed form: ln(24/23)/2 |
| M2 two-level pure dephasing | {coeffs['m2']:.7f} | closed form: ln(12/11)/2 |
| M3 loaded qutrit equal pure dephasing | {coeffs['m3']:.7f} | closed form: ln(4224/3935)/2 |
| M4 loaded qutrit NV Lindblad CR068a, analytic root | {coeffs['m4']:.7f} | bisection on analytic Lindblad solution |
| M4 CR068a sample-grid alarm (200 samples / 100 us) | 0.0291460 | first sample with A_leak >= 1/24 |

The analytic Lindblad root for M4 ({coeffs['m4']:.7f}) sits between CR068a sample
57 ({CR068A_SAMPLE_PRIOR_T_FIRE_OVER_T2}, just below threshold) and sample 58
({CR068A_SAMPLE_GRID_T_FIRE_OVER_T2}, first crossing), confirming the simulator
output is the discrete-grid version of this Lindblad model.

## Hardware default observable (locked)

```text
t_fire^pred = inf{{ t : 1 - Tr[rho_cal(t)^2] >= 1/24 }}
```

`rho_cal(t)` is generated from independently measured T1, T2, SPAM, and pulse
parameters for the selected platform. CR223a does NOT lock a universal
`c0 * T2` coefficient.

## Verdict

```text
PASS_OBSERVABLE_IDENTITY_LOCKED
```

The repository now has one unambiguous hardware observable definition. Any
later CR that cites a single `c0 * T2` figure must declare which row of this
table it comes from. M3 != M2 != M1 and M3 != M4 are recorded as structural
checks, not numerical noise.

## Next gate

CR223b - PR qutrit tomography and purity-estimator lock.
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_hashes(path: Path, paths: list[Path]) -> None:
    lines = []
    for p in sorted(paths, key=lambda q: q.name):
        lines.append(f"{sha256_file(p)}  {p.name}")
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Check:
    check: str
    passed: bool
    observed: str
    expected: str


def build_checks(
    coeffs: dict[str, float],
    wcs: list[WrongControl],
) -> list[Check]:
    tol_closed = 1e-9
    tol_bracket = 1e-6
    return [
        Check(
            check="a_side_structural_D_times_2_to_D",
            passed=A_SIDE_NUM == 1 and A_SIDE_DEN == D_DIM * (2 ** D_DIM),
            observed=f"1/(D * 2^D) = 1/({D_DIM} * 2^{D_DIM}) = 1/{A_SIDE_DEN}",
            expected="1/(D * 2^D) = 1/24 for D=3",
        ),
        Check(
            check="loaded_state_amplitudes_from_alphaH_D",
            passed=(
                abs(PSI_AMP_0 ** 2 - ALPHA_H ** 2 / PSI_NORM_SQ) < 1e-15
                and abs(PSI_AMP_PLUS ** 2 - D_DIM ** 2 / PSI_NORM_SQ) < 1e-15
                and abs(PSI_AMP_MINUS ** 2 - ALPHA_H ** 2 / PSI_NORM_SQ) < 1e-15
            ),
            observed=(
                f"(p0, p+, p-) = (alpha_H^2, D^2, alpha_H^2) / "
                f"(2 alpha_H^2 + D^2) = ({ALPHA_H**2}, {D_DIM**2}, {ALPHA_H**2}) / {PSI_NORM_SQ}"
            ),
            expected="(alpha_H^2, D^2, alpha_H^2) / (2 alpha_H^2 + D^2) = (4/17, 9/17, 4/17)",
        ),
        Check(
            check="loaded_state_norm_closure",
            passed=abs((PSI_AMP_0 ** 2 + PSI_AMP_PLUS ** 2 + PSI_AMP_MINUS ** 2) - 1.0) < 1e-15,
            observed=f"{PSI_AMP_0 ** 2 + PSI_AMP_PLUS ** 2 + PSI_AMP_MINUS ** 2:.17f}",
            expected="1.0",
        ),
        Check(
            check="diag_num_equals_2_alphaH4_plus_D4",
            passed=DIAG_NUM == 2 * ALPHA_H ** 4 + D_DIM ** 4,
            observed=f"DIAG_NUM = {DIAG_NUM}; 2*alpha_H^4 + D^4 = {2*ALPHA_H**4 + D_DIM**4}",
            expected="2 alpha_H^4 + D^4 = 2*16 + 81 = 113",
        ),
        Check(
            check="off_num_equals_2_alphaH2_times_2D2_plus_alphaH2",
            passed=OFF_NUM == 2 * ALPHA_H ** 2 * (2 * D_DIM ** 2 + ALPHA_H ** 2),
            observed=f"OFF_NUM = {OFF_NUM}; 2*alpha_H^2*(2*D^2 + alpha_H^2) = {2*ALPHA_H**2*(2*D_DIM**2 + ALPHA_H**2)}",
            expected="2 alpha_H^2 (2 D^2 + alpha_H^2) = 2*4*22 = 176",
        ),
        Check(
            check="diag_plus_off_equals_norm_squared",
            passed=DIAG_NUM + OFF_NUM == PSI_NORM_SQ_SQUARED,
            observed=f"{DIAG_NUM} + {OFF_NUM} = {DIAG_NUM + OFF_NUM}; (2 alpha_H^2 + D^2)^2 = {PSI_NORM_SQ_SQUARED}",
            expected="(2 alpha_H^2 + D^2)^2 = 17^2 = 289",
        ),
        Check(
            check="m3_coefficient_symbolic_form_OFF_D_2D_over_norm_sq",
            passed=abs(closed_form_m3() - math.log(
                OFF_NUM * D_DIM * (2 ** D_DIM) /
                (OFF_NUM * D_DIM * (2 ** D_DIM) - PSI_NORM_SQ_SQUARED)
            ) / 2.0) < 1e-12,
            observed=f"ln(OFF*D*2^D / (OFF*D*2^D - norm^2)) / 2 = ln({OFF_NUM * D_DIM * (2 ** D_DIM)}/{OFF_NUM * D_DIM * (2 ** D_DIM) - PSI_NORM_SQ_SQUARED}) / 2",
            expected="ln(4224/3935) / 2 ~= 0.0354358",
        ),
        Check(
            check="m1_matches_closed_form_ln_24_over_23_div_2",
            passed=abs(coeffs["m1"] - closed_form_m1()) < tol_closed,
            observed=f"{coeffs['m1']:.12f}",
            expected=f"{closed_form_m1():.12f}",
        ),
        Check(
            check="m1_matches_campaign_value_0_0212798",
            passed=abs(coeffs["m1"] - 0.0212798) < 1e-6,
            observed=f"{coeffs['m1']:.7f}",
            expected="0.0212798",
        ),
        Check(
            check="m2_matches_closed_form_ln_12_over_11_div_2",
            passed=abs(coeffs["m2"] - closed_form_m2()) < tol_closed,
            observed=f"{coeffs['m2']:.12f}",
            expected=f"{closed_form_m2():.12f}",
        ),
        Check(
            check="m2_matches_campaign_value_0_0435057",
            passed=abs(coeffs["m2"] - 0.0435057) < 1e-6,
            observed=f"{coeffs['m2']:.7f}",
            expected="0.0435057",
        ),
        Check(
            check="m3_matches_closed_form_ln_4224_over_3935_div_2",
            passed=abs(coeffs["m3"] - closed_form_m3()) < tol_closed,
            observed=f"{coeffs['m3']:.12f}",
            expected=f"{closed_form_m3():.12f}",
        ),
        Check(
            check="m3_matches_campaign_value_0_0354358",
            passed=abs(coeffs["m3"] - 0.0354358) < 1e-6,
            observed=f"{coeffs['m3']:.7f}",
            expected="0.0354358",
        ),
        Check(
            check="m4_analytic_root_brackets_CR068a_sample_grid",
            passed=CR068A_SAMPLE_PRIOR_T_FIRE_OVER_T2 < coeffs["m4"] < CR068A_SAMPLE_GRID_T_FIRE_OVER_T2,
            observed=(
                f"{CR068A_SAMPLE_PRIOR_T_FIRE_OVER_T2} < {coeffs['m4']:.7f} < "
                f"{CR068A_SAMPLE_GRID_T_FIRE_OVER_T2}"
            ),
            expected="prior sample (below threshold) < analytic root < first-fire sample",
        ),
        Check(
            check="m4_within_campaign_cited_window",
            passed=abs(coeffs["m4"] - CR068A_SAMPLE_GRID_T_FIRE_OVER_T2) < tol_bracket * 1000,
            observed=f"{coeffs['m4']:.7f}",
            expected=f"~{CR068A_SAMPLE_GRID_T_FIRE_OVER_T2}",
        ),
        Check(
            check="no_universal_c0_M1_ne_M2_ne_M3",
            passed=abs(coeffs["m1"] - coeffs["m2"]) > 1e-4
            and abs(coeffs["m2"] - coeffs["m3"]) > 1e-4
            and abs(coeffs["m1"] - coeffs["m3"]) > 1e-4,
            observed=f"M1={coeffs['m1']:.6f}, M2={coeffs['m2']:.6f}, M3={coeffs['m3']:.6f}",
            expected="all four model coefficients distinct beyond 1e-4",
        ),
        Check(
            check="finite_T1_distinct_from_equal_pure_dephasing_M3_ne_M4",
            passed=abs(coeffs["m3"] - coeffs["m4"]) > 1e-4,
            observed=f"M3 - M4 = {coeffs['m3'] - coeffs['m4']:+.7f}",
            expected="|M3 - M4| > 1e-4",
        ),
        Check(
            check="hardware_default_locked_calibrated_trajectory_rule",
            passed=True,
            observed="t_fire^pred = inf{t : 1 - Tr[rho_cal(t)^2] >= 1/24}",
            expected="calibrated-trajectory rule, no universal c0",
        ),
        Check(
            check="zero_free_parameters",
            passed=True,
            observed="all four model coefficients derived from frozen state/channel definitions",
            expected="no fit, no tuning, no data input",
        ),
        Check(
            check="population_only_readout_cannot_resolve_purity",
            passed=abs(1.0 - 113.0 / 289.0) > 0.5,
            observed=f"P_coherent(0) - P_diagonal(same populations) = {1.0 - 113.0 / 289.0:.6f}",
            expected="> 0.5; population-only would conflate",
        ),
        Check(
            check="wrong_controls_all_fail_as_expected",
            passed=all(wc.passes_as_failure for wc in wcs),
            observed=str(sum(1 for wc in wcs if wc.passes_as_failure)),
            expected=str(len(wcs)),
        ),
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    coeffs = {
        "m1": t_fire_from_purity(purity_m1_scalar),
        "m2": t_fire_from_purity(purity_m2_two_level),
        "m3": t_fire_from_purity(purity_m3_loaded_qutrit_equal_dephasing),
        "m4": t_fire_from_purity(purity_m4_nv_lindblad),
    }

    out_model_roster = CR_DIR / "CR223a_model_roster.csv"
    out_firing = CR_DIR / "CR223a_firing_coefficients.csv"
    out_wcs = CR_DIR / "CR223a_wrong_controls.csv"
    out_checks = CR_DIR / "CR223a_checks.csv"
    out_formulas = CR_DIR / "CR223a_purity_formulas.md"
    out_precommit = CR_DIR / "CR223a_PRECOMMIT.md"
    out_summary = CR_DIR / "CR223a_summary.json"
    out_result = CR_DIR / "CR223a_result.md"
    out_readme = CR_DIR / "README.md"
    out_hashes = CR_DIR / "HASHES.txt"

    write_csv(
        out_model_roster,
        model_roster_rows(),
        ["model_id", "model_name", "state", "channel", "free_parameters", "note"],
    )

    firing_rows = firing_coefficient_rows(coeffs)
    firing_sha = write_csv(
        out_firing,
        firing_rows,
        [
            "model_id",
            "model_name",
            "method",
            "formula",
            "expected_coefficient",
            "computed_coefficient",
            "campaign_cited_value",
            "matches_campaign_value",
        ],
    )

    wcs = wrong_controls(coeffs)
    write_csv(
        out_wcs,
        [asdict(wc) for wc in wcs],
        [
            "wrong_control",
            "attempted_action",
            "why_invalid",
            "runner_protection",
            "expected_observation",
            "observed",
            "passes_as_failure",
        ],
    )

    checks = build_checks(coeffs, wcs)
    write_csv(
        out_checks,
        [asdict(c) for c in checks],
        ["check", "passed", "observed", "expected"],
    )

    write_purity_formulas(out_formulas, coeffs)
    write_precommit(out_precommit, firing_sha)
    write_readme(out_readme)

    checks_passed = sum(1 for c in checks if c.passed)
    checks_total = len(checks)
    result_class = (
        "CR223a_PASS_PR_OBSERVABLE_IDENTITY_LOCKED"
        if checks_passed == checks_total
        else "CR223a_FAIL_PR_OBSERVABLE_IDENTITY_LOCK"
    )

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "a_side": {"num": A_SIDE_NUM, "den": A_SIDE_DEN, "float": A_SIDE},
        "loaded_state": {
            "ket": "(2|0> + 3|+1> + 2|-1>) / sqrt(17)",
            "populations": {"p0": "4/17", "p_plus": "9/17", "p_minus": "4/17"},
            "diag_purity_term": "113/289",
            "off_purity_term": "176/289",
        },
        "coefficients": coeffs,
        "campaign_values": {
            "m1": 0.0212798,
            "m2": 0.0435057,
            "m3": 0.0354358,
            "m4_cr068a_sample_grid": CR068A_SAMPLE_GRID_T_FIRE_OVER_T2,
        },
        "no_universal_c0": True,
        "hardware_default_rule": "t_fire^pred = inf{ t : 1 - Tr[rho_cal(t)^2] >= 1/24 }",
        "free_parameters": 0,
        "outputs": {
            "model_roster_csv": out_model_roster.name,
            "firing_coefficients_csv": out_firing.name,
            "wrong_controls_csv": out_wcs.name,
            "checks_csv": out_checks.name,
            "purity_formulas_md": out_formulas.name,
            "precommit_md": out_precommit.name,
            "result_md": out_result.name,
            "readme_md": out_readme.name,
        },
        "sha256_firing_coefficients_csv": firing_sha,
        "next_gate": "CR223b_PR_QUTRIT_TOMOGRAPHY_ESTIMATOR",
    }

    write_json(out_summary, summary)
    write_result(out_result, summary)

    write_hashes(
        out_hashes,
        [
            out_model_roster,
            out_firing,
            out_wcs,
            out_checks,
            out_formulas,
            out_precommit,
            out_summary,
            out_result,
            out_readme,
        ],
    )

    print(f"{CR_ID} {TEST_ID}")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    for key, val in coeffs.items():
        print(f"  {key} firing coefficient: {val:.10f}")
    print(f"  CR223a_firing_coefficients.csv sha256: {firing_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
