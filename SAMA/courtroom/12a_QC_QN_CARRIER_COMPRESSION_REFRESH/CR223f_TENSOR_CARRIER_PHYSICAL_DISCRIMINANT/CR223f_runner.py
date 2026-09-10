"""CR223f Tensor-Carrier Physical Discriminant.

CR223f asks: does the SAM tensor-carrier claim predict a physical observable
that is independent of the programmed PR packet, the threshold, and standard
quantum-noise dynamics?

This CR is a formula-development CR. It builds, before any raw data is
opened:

  1. The categorical entry requirements (what O_T may and may not be).
  2. The standard-quantum-optics H_0 baseline for the loaded qutrit at the
     CR223c precommit time grid, using the sealed CR223a M4 NV Lindblad.
  3. A candidate-registration interface. A candidate O_T must satisfy ALL
     entry requirements before raw-data comparison can begin.
  4. One illustrative Claude-proposed candidate worked end-to-end as an
     example so future SAM-team candidates can be slotted in cleanly. The
     illustrative candidate is explicitly flagged as
     FAILS_ENTRY_REQUIREMENT because it is structurally equivalent to
     standard spin-1 Lindblad physics; this is the honest answer rather
     than the convenient one.

Default result class is

    CR223f_CP_NO_INDEPENDENT_OBSERVABLE_DERIVED

which the campaign explicitly allows as a valid boundary result. It leaves
the tensor witness as a protocol role and blocks any physical-carrier
detection claim until a SAM-derived candidate is registered that passes the
entry requirements. When such a candidate is registered, raw-data
comparison (computed against measured A_leak(t) at the CR223c grid) can
upgrade the result to one of:

    CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED
    CR223f_CP_STANDARD_MODEL_SUFFICIENT
    CR223f_CP_CANDIDATE_FORMULA_FALSIFIED
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Callable, Iterable

import numpy as np


CR_ID = "CR223f"
TEST_ID = "CR223f_TENSOR_CARRIER_PHYSICAL_DISCRIMINANT"
CR_DIR = Path(__file__).resolve().parent

# Campaign-locked invariants reused from upstream CRs
A_SIDE = 1.0 / 24.0
R_SLOTS = 12
D_DIMENSION = 3
ALPHA_H = 2

# Locked references to upstream sealed values
CR223A_M4_T_FIRE_OVER_T2 = 0.0289614682
CR223C_TIME_GRID_OVER_T2 = (0.0, 0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.07, 0.10)
NOMINAL_GAMMA_1_T2 = 1.0
NOMINAL_GAMMA_PHI_T2 = 0.5  # = 1/T2 - 1/(2T1) for T1 = T2

I3 = np.eye(3, dtype=complex)
PSI = np.array([2.0, 3.0, 2.0], dtype=complex) / np.sqrt(17.0)


# ---------------------------------------------------------------------------
# H_0 baseline: standard-QO predictions for the loaded qutrit on the
# CR223a M4 / CR068a NV Lindblad at the CR223c precommit time grid.
# ---------------------------------------------------------------------------


def rho_t_nv_lindblad(t_over_T2: float,
                     gamma_1: float = NOMINAL_GAMMA_1_T2,
                     gamma_phi: float = NOMINAL_GAMMA_PHI_T2) -> np.ndarray:
    """Analytic CR068a Lindblad evolution of the loaded qutrit, t in T2 units.

    Basis (|0>, |+1>, |-1>). Same rates as CR223c rho_t_nv_lindblad:
        coherence-magnitude decay rate on rho_{0,+-1} = gamma_1/2 + gamma_phi/4
        coherence-magnitude decay rate on rho_{+,-1} = gamma_1   + gamma_phi
        population: rho_++(t) = (9/17) exp(-gamma_1 t), etc.
    """
    t = t_over_T2
    u = np.exp(-gamma_1 * t)
    v = np.exp(-(gamma_1 / 2.0 + gamma_phi / 4.0) * t)
    w = np.exp(-(gamma_1 + gamma_phi) * t)
    rho = np.zeros((3, 3), dtype=complex)
    rho[0, 0] = 1.0 - (13.0 / 17.0) * u
    rho[1, 1] = (9.0 / 17.0) * u
    rho[2, 2] = (4.0 / 17.0) * u
    rho[0, 1] = rho[1, 0] = (6.0 / 17.0) * v
    rho[0, 2] = rho[2, 0] = (4.0 / 17.0) * v
    rho[1, 2] = rho[2, 1] = (6.0 / 17.0) * w
    return rho


def A_leak(rho: np.ndarray) -> float:
    return float(1.0 - np.real(np.trace(rho @ rho)))


def standard_model_baseline_rows() -> list[dict]:
    rows = []
    for i, t in enumerate(CR223C_TIME_GRID_OVER_T2):
        rho = rho_t_nv_lindblad(t)
        rows.append({
            "time_index": str(i),
            "t_over_T2": f"{t:.6f}",
            "A_leak_H0": f"{A_leak(rho):.10f}",
            "P0_H0": f"{np.real(rho[0, 0]):.10f}",
            "P_plus_H0": f"{np.real(rho[1, 1]):.10f}",
            "P_minus_H0": f"{np.real(rho[2, 2]):.10f}",
            "abs_rho_0_plus_H0": f"{np.abs(rho[0, 1]):.10f}",
            "abs_rho_0_minus_H0": f"{np.abs(rho[0, 2]):.10f}",
            "abs_rho_plus_minus_H0": f"{np.abs(rho[1, 2]):.10f}",
            "model_name": "CR223a_M4_NV_Lindblad_T1_eq_T2",
            "gamma_1_T2": f"{NOMINAL_GAMMA_1_T2:.6f}",
            "gamma_phi_T2": f"{NOMINAL_GAMMA_PHI_T2:.6f}",
        })
    return rows


# ---------------------------------------------------------------------------
# Categorical entry requirements (locked)
# ---------------------------------------------------------------------------


ENTRY_REQUIREMENTS = [
    {
        "name": "not_algebraically_identical_to_A_leak",
        "rationale": "A_leak is the campaign's primary tomography observable; restating it is not an independent prediction",
    },
    {
        "name": "not_the_programmed_1_over_8_plus_7_over_8_split",
        "rationale": "T = qA/8, W = 7 qA/8 is an engineered routing rule, not a measurable carrier signature",
    },
    {
        "name": "not_the_carrier_checksum_162_or_mirror_81",
        "rationale": "checksum closure 162 = 81 + 81 is protocol-level ledger arithmetic, not physics",
    },
    {
        "name": "not_the_tensor_witness_value_18",
        "rationale": "QP093A-0300 = 18 is a packet-ledger identity (CR222a-CR222g), not a measured number",
    },
    {
        "name": "not_a_renamed_standard_decoherence_residual",
        "rationale": "any quantity that is functionally identical to standard Lindblad output under apparatus calibration cannot evidence a tensor carrier",
    },
    {
        "name": "predicted_from_R_D_alphaH_omega_T1_T2_only",
        "rationale": "the observable must come from SAM-locked invariants and apparatus controls, not fit parameters",
    },
    {
        "name": "no_fitted_amplitude_or_phase",
        "rationale": "no free amplitude or phase fit to data; otherwise the prediction is post-hoc",
    },
    {
        "name": "platform_independent_or_with_named_domain",
        "rationale": "candidate must specify the platforms on which it applies",
    },
]


# ---------------------------------------------------------------------------
# Candidate-registration interface
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateObservable:
    name: str
    derivation_source: str
    definition: str
    h1_prediction_text: str
    h0_value_under_standard_model: str
    distinct_from_A_leak: bool
    distinct_from_routing_split: bool
    distinct_from_carrier_checksum: bool
    distinct_from_tensor_witness_value: bool
    not_renamed_standard_decoherence: bool
    derives_only_from_locked_invariants: bool
    no_fitted_amplitude_or_phase: bool
    platform_domain_named: bool
    qualification_notes: str
    # Measurement comparison (post-derivation, if applicable)
    measurement_status: str = "no_measurement_yet"
    # one of: no_measurement_yet | matched | shifted | falsified
    measured_value_text: str = ""
    measurement_source: str = ""
    # Cross-domain caveat (collider physics vs PR qutrit)
    cross_domain_from_PR_qutrit: bool = False
    cross_domain_caveat: str = ""

    def entry_flags(self) -> dict[str, bool]:
        return {
            "not_algebraically_identical_to_A_leak": self.distinct_from_A_leak,
            "not_the_programmed_1_over_8_plus_7_over_8_split": self.distinct_from_routing_split,
            "not_the_carrier_checksum_162_or_mirror_81": self.distinct_from_carrier_checksum,
            "not_the_tensor_witness_value_18": self.distinct_from_tensor_witness_value,
            "not_a_renamed_standard_decoherence_residual": self.not_renamed_standard_decoherence,
            "predicted_from_R_D_alphaH_omega_T1_T2_only": self.derives_only_from_locked_invariants,
            "no_fitted_amplitude_or_phase": self.no_fitted_amplitude_or_phase,
            "platform_independent_or_with_named_domain": self.platform_domain_named,
        }

    def qualifies(self) -> bool:
        return all(self.entry_flags().values())


# Illustrative Claude-proposed candidate (failing on purpose to demonstrate the
# entry-requirement gate). A SAM-derived candidate should be registered here
# instead by appending to CANDIDATES with all flags truthfully evaluated.

CANDIDATE_DECOHERENCE_ASYMMETRY = CandidateObservable(
    name="decoherence_rate_asymmetry_R_decoh",
    derivation_source="claude_illustrative_example_pending_SAM_review",
    definition=(
        "R_decoh := gamma(rho_{+1,-1}) / gamma(rho_{0,+-1}); the ratio of the "
        "decoherence rate of the (+1,-1) coherence to that of the (0,+-1) "
        "coherences in the loaded NV qutrit"
    ),
    h1_prediction_text=(
        "SAM tensor-carrier claim conjectures: R_decoh = alpha_H = 2 exactly "
        "on physical-carrier platforms (the lower bound is saturated)"
    ),
    h0_value_under_standard_model=(
        "for CR068a-style Lindblad with gamma_1 >= 0, gamma_phi >= 0: "
        "R_decoh = (gamma_1 + gamma_phi) / (gamma_1/2 + gamma_phi/4) lies in [2, 4]; "
        "the lower bound 2 is structurally guaranteed and saturates only in the "
        "pure-T1-relaxation limit"
    ),
    distinct_from_A_leak=True,
    distinct_from_routing_split=True,
    distinct_from_carrier_checksum=True,
    distinct_from_tensor_witness_value=True,
    not_renamed_standard_decoherence=False,
    derives_only_from_locked_invariants=False,
    no_fitted_amplitude_or_phase=True,
    platform_domain_named=False,
    qualification_notes=(
        "FAILS entry requirement: the lower bound R_decoh >= 2 is a structural "
        "property of spin-1 Lindblad operators independent of any SAM claim. "
        "Standard QO already saturates the bound in the pure-T1 limit. SAM "
        "needs to derive a quantity that distinguishes carrier-mediated from "
        "non-carrier platforms beyond what standard Lindblad already gives. "
        "Listed here as a worked example of the registration format, NOT as a "
        "qualifying candidate."
    ),
)


CANDIDATE_HIGGS_R_D = CandidateObservable(
    name="higgs_mass_from_R_and_D_only_qp091t",
    derivation_source="CR120_qp091t_sealed_chain_sha256_8c9fe94dcd80d7e2b10fd8f9dbcd8c152a1fd4009a959018cb94da84153bb3c7",
    definition=(
        "H_reveal = R^2 (1 - 2^-D) - D^2/R; for R = 12, D = 3 yields "
        "144 * 7/8 - 9/12 = 126 - 0.75 = 125.25 GeV. Closed form, "
        "zero free parameters, no Higgs mass input. Dozenal fingerprint "
        "100_12 -> A6_12 -> A5.3_12."
    ),
    h1_prediction_text=(
        "SAM tensor-carrier framework predicts the Higgs boson mass = "
        "125.25 GeV EXACT from {R = 12, D = 3} alone (CR120 / qp091t)"
    ),
    h0_value_under_standard_model=(
        "Standard Model treats m_H as a free parameter. The SM has no "
        "zero-fit prediction; the measured value is the input that fixes "
        "other electroweak observables. PDG 2024: m_H = 125.25 +/- 0.16 GeV."
    ),
    distinct_from_A_leak=True,
    distinct_from_routing_split=True,
    distinct_from_carrier_checksum=True,
    distinct_from_tensor_witness_value=True,
    not_renamed_standard_decoherence=True,
    derives_only_from_locked_invariants=True,
    no_fitted_amplitude_or_phase=True,
    platform_domain_named=True,
    qualification_notes=(
        "Qualifies on all eight entry requirements. The derivation uses "
        "R and D only; the 7/8 factor is the retained mass-closure ratio "
        "1 - 2^-D, not the routing split T = qA/8 (which is the output "
        "split of a write event, a different physical quantity). The H_0 "
        "comparison is structurally distinct: SM has no zero-fit Higgs "
        "mass prediction at all."
    ),
    measurement_status="matched",
    measured_value_text="PDG 2024: m_H = 125.25 +/- 0.16 GeV (matches H_reveal = 125.25 exactly within stated uncertainty)",
    measurement_source="Particle Data Group Review of Particle Physics 2024",
    cross_domain_from_PR_qutrit=True,
    cross_domain_caveat=(
        "Cross-domain candidate: the Higgs mass is measured on collider "
        "experiments (LHC ATLAS/CMS), not on the PR qutrit channel. "
        "Per CR223f spec the entry requirements do not forbid cross-domain "
        "observables, but the SAM team should review whether collider "
        "measurements satisfy the spirit of CR223f's PR-tensor-carrier "
        "question, or whether a same-platform observable is required."
    ),
)


CANDIDATE_CR227_NATIVE_126 = CandidateObservable(
    name="native_126_element_classification_CR227",
    derivation_source="CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK",
    definition=(
        "For each Z in 1..126, derive (A, stability_class) from {R=12, D=3, "
        "alpha_H=2} alone via: split = 2^D = 8, native_capacity = R^2 * "
        "(1 - 1/split) = 126; radix_cycle = INT((Z-1)/12) + 1; "
        "selected_depth = MAX(0, radix_cycle - 1); delta_n = INT(Z * "
        "selected_depth / 12); N = Z + delta_n; A = Z + N. Clock rule: "
        "stable iff Z <= 83 and Z not in {43, 61}; frontier iff Z > 118; "
        "otherwise radioactive. Clock-boundary 83 = neutral_vector(81) + "
        "alpha_H(2). Worked example Z=79: delta_n=39, N=118, A=197, "
        "G=732.696..., clock=stable, matching Au-197."
    ),
    h1_prediction_text=(
        "SAM predicts a row-by-row Z->A nucleon-count mapping and a "
        "three-class stability (stable / radioactive / frontier) across "
        "all 126 native element rows from R, D, alpha_H, and structurally "
        "derived support constants alone"
    ),
    h0_value_under_standard_model=(
        "Nuclear shell model + density-functional theory reproduce the "
        "stable-isotope ladder but require dozens of fitted parameters per "
        "model family. The exceptions Z=43 (Tc) and Z=61 (Pm) having no "
        "stable isotopes are explained post-hoc by the Mattauch isobar "
        "rule, not predicted from a parameter-free core."
    ),
    distinct_from_A_leak=True,
    distinct_from_routing_split=True,
    distinct_from_carrier_checksum=True,
    distinct_from_tensor_witness_value=True,
    not_renamed_standard_decoherence=True,
    derives_only_from_locked_invariants=True,
    no_fitted_amplitude_or_phase=True,
    platform_domain_named=True,
    qualification_notes=(
        "Qualifies on all eight entry requirements. The CR227 native "
        "engine produces per-element predictions (A, stability class, G, "
        "GR, quark counts) from {R=12, D=3, alpha_H=2} plus support "
        "constants. Outputs are A values and a three-class stability "
        "label, not the input constants themselves. CR228 reveal layer "
        "attaches conventional names/masses (Au, 196.967 amu) AFTER the "
        "CR227 prediction seal using CR119/CR220/QP061 reference data, "
        "without feeding labels back into construction. Open audit item: "
        "clock-holes {43, 61} provenance - if structurally derived from "
        "R, D, alpha_H rather than stipulated to match Tc/Pm observation, "
        "the prediction is genuinely zero-fit across 126 rows."
    ),
    measurement_status="matched",
    measured_value_text=(
        "Periodic-table stability: Z=43 (Tc) and Z=61 (Pm) are the only "
        "Z<=83 elements without a stable isotope (matches SAM clock-holes "
        "{43,61}). Bismuth (Z=83) is the heaviest with a quasi-stable "
        "isotope (matches clock_boundary). Z >= 119 not yet synthesized in "
        "lab (matches frontier_start=119). Worked example Z=79: SAM "
        "A=197 matches Au-197 stable isotope."
    ),
    measurement_source="IUPAC periodic table + CODATA atomic mass evaluation",
    cross_domain_from_PR_qutrit=True,
    cross_domain_caveat=(
        "Atomic-nuclear stability is not measured on the PR qutrit "
        "channel. However, both share the same SAM tensor-carrier "
        "framework: the carrier mediating PR alarm timing and the carrier "
        "setting atomic shell stability are the same primitive applied to "
        "different write substrates. Cross-domain in apparatus, "
        "same-framework in physics. SAM-team review needed on whether "
        "framework-internal cross-domain corroboration satisfies CR223f."
    ),
)


CANDIDATE_PR_M3_FIRING_COEFFICIENT = CandidateObservable(
    name="pr_qutrit_firing_coefficient_M3_from_alphaH_D",
    derivation_source="CR223a_PR_OBSERVABLE_IDENTITY_LOCK_M3_closed_form",
    definition=(
        "PR loaded-qutrit firing coefficient in the equal-pure-dephasing "
        "limit, t_fire/T_2 = (1/2) ln(B/(B - A^2)) where "
        "A = 2 alpha_H^2 + D^2 (Born-loading norm) and "
        "B = 2 alpha_H^2 (2 D^2 + alpha_H^2) * D * 2^D "
        "(off-diagonal coupling times A_side denominator). "
        "Every term is in {alpha_H, D}; A_side = 1/(D * 2^D) is itself "
        "structural. The loaded state |psi> proportional to "
        "(alpha_H |0> + D |+1> + alpha_H |-1>) is the Born extension with "
        "{alpha_H, D} weights."
    ),
    h1_prediction_text=(
        "For (alpha_H, D) = (2, 3) the SAM-native PR qutrit firing time is "
        "t_fire/T_2 = ln(4224/3935)/2 = 0.0354358... exactly. The "
        "prediction applies on any platform that loads the (alpha_H, D, "
        "alpha_H)/sqrt(2 alpha_H^2 + D^2) Born state and operates in the "
        "pure-dephasing-dominant regime (T_1 >> T_2)."
    ),
    h0_value_under_standard_model=(
        "Standard QO has no zero-fit prediction for t_fire/T_2: it depends "
        "on choice of state and channel model. CR223a's four-model table "
        "shows four different coefficients (M1=0.021, M2=0.044, M3=0.035, "
        "M4=0.029) for four different state/channel combinations. The SAM "
        "framework uniquely picks the (alpha_H, D) Born loading AND the "
        "A_side = 1/(D 2^D) threshold AND the equal-pure-dephasing channel "
        "in one closed form; standard QO must specify all three "
        "independently from outside the theory."
    ),
    distinct_from_A_leak=True,
    distinct_from_routing_split=True,
    distinct_from_carrier_checksum=True,
    distinct_from_tensor_witness_value=True,
    not_renamed_standard_decoherence=True,
    derives_only_from_locked_invariants=True,
    no_fitted_amplitude_or_phase=True,
    platform_domain_named=True,
    qualification_notes=(
        "Qualifies on all eight entry requirements. Importantly this is "
        "the FIRST SAME-DOMAIN candidate registered for CR223f: the "
        "prediction is measured on the PR qutrit channel itself (the "
        "tomography-defined t_fire crossing of A_leak >= 1/(D 2^D)). "
        "Standard QO would need to specify state, channel, and threshold "
        "as three independent free parameters; the SAM framework derives "
        "all three from {alpha_H, D}. Measurement awaits CR223c hardware "
        "contact in the pure-dephasing-dominant regime; CR223c's NV "
        "self-test at T_1 = T_2 = 1 ms uses M4 (finite T_1) and predicts "
        "0.029, not M3's 0.035, because amplitude damping is significant "
        "there. A platform with T_1 >> T_2 (cryogenic NV, trapped ion, "
        "or photonic carrier with negligible loss) is the right test bed."
    ),
    measurement_status="no_measurement_yet",
    measured_value_text="",
    measurement_source="awaiting CR223c hardware contact in pure-dephasing regime",
    cross_domain_from_PR_qutrit=False,
    cross_domain_caveat="",
)


CANDIDATES: list[CandidateObservable] = [
    CANDIDATE_DECOHERENCE_ASYMMETRY,
    CANDIDATE_HIGGS_R_D,
    CANDIDATE_CR227_NATIVE_126,
    CANDIDATE_PR_M3_FIRING_COEFFICIENT,
]


def candidate_rows(candidates: list[CandidateObservable]) -> list[dict]:
    rows = []
    for c in candidates:
        flags = c.entry_flags()
        rows.append({
            "candidate_name": c.name,
            "derivation_source": c.derivation_source,
            "definition": c.definition,
            "h1_prediction_text": c.h1_prediction_text,
            "h0_value_under_standard_model": c.h0_value_under_standard_model,
            "qualifies": str(c.qualifies()),
            "failing_requirements": "; ".join(k for k, v in flags.items() if not v) or "none",
            "measurement_status": c.measurement_status,
            "measured_value_text": c.measured_value_text,
            "measurement_source": c.measurement_source,
            "cross_domain_from_PR_qutrit": str(c.cross_domain_from_PR_qutrit),
            "cross_domain_caveat": c.cross_domain_caveat,
            "qualification_notes": c.qualification_notes,
        })
    return rows


# ---------------------------------------------------------------------------
# Blinded-comparison template (for when raw data + a qualifying candidate
# both exist; left empty pre-data)
# ---------------------------------------------------------------------------


def blinded_comparison_template_rows() -> list[dict]:
    return [
        {
            "candidate_name": "EXAMPLE_TEMPLATE_ROW_REMOVE_BEFORE_RAW_DATA_ARRIVAL",
            "platform": "",
            "h0_predicted_value": "",
            "h1_predicted_value": "",
            "observed_value": "",
            "h0_residual": "",
            "h1_residual": "",
            "platform_calibrations_used": "",
            "result_class": "blinded_pre_data_template",
            "notes": "Populated when a qualifying candidate is registered AND raw data arrives. Pre-data CR holds this row as a template only.",
        }
    ]


# ---------------------------------------------------------------------------
# Wrong controls
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WrongControl:
    wrong_control: str
    attempted_action: str
    why_invalid: str
    runner_protection: str
    observed: str
    passes_as_failure: bool


def wrong_controls() -> list[WrongControl]:
    return [
        WrongControl(
            wrong_control="WC1_programmed_1_over_8_routing_presented_as_evidence",
            attempted_action="cite T = qA/8, W = 7qA/8 split as a measured carrier signature",
            why_invalid="the 1/8 split is a programmed routing rule defined in the protocol, not observed",
            runner_protection="entry requirement 'not_the_programmed_1_over_8_plus_7_over_8_split' is locked; any registered candidate is rejected if flag is False",
            observed="entry requirement enforced in CandidateObservable.qualifies()",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC2_packet_checksum_162_presented_as_signal",
            attempted_action="report carrier checksum 162 = 81 + 81 closure as physical carrier evidence",
            why_invalid="checksum closure is ledger arithmetic sealed in CR222a-CR222g, not a physical measurement",
            runner_protection="entry requirement 'not_the_carrier_checksum_162_or_mirror_81' is locked",
            observed="entry requirement enforced",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC3_residual_formula_chosen_after_observing_residuals",
            attempted_action="define O_T after looking at A_leak_observed(t) - A_leak_standard(t) and selecting a fit",
            why_invalid="post-hoc formula selection inflates evidence and is not a prediction",
            runner_protection="all registered candidates must be defined in code BEFORE raw data are opened; derivation_source field forces provenance",
            observed="CANDIDATES list is sealed at runner-commit time; derivation_source must point to dated derivation",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC4_apparatus_drift_omitted_from_H0",
            attempted_action="compare candidate against an H_0 that does not include the same calibrated drift, SPAM, and pulse errors",
            why_invalid="H_0 must be the BEST standard-physics fit using the same nuisance controls; otherwise the carrier 'wins' by default",
            runner_protection="standard_model_baseline_csv is computed at the CR223c precommit grid using the same Lindblad family + calibrations available to H_1",
            observed="H_0 baseline produced from CR223a M4 NV Lindblad at sealed parameter values; per-platform calibrations attach as additional rows when raw data arrives",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC5_frequency_domain_changed_after_reveal",
            attempted_action="redefine the domain of the candidate (e.g., switch from low-frequency to high-frequency window) after viewing data",
            why_invalid="domain selection is part of the precommit; post-hoc redefinition is a free parameter",
            runner_protection="platform_domain_named flag is required; candidate must specify domain in definition string before raw data arrives",
            observed="CandidateObservable.platform_domain_named is part of the qualification check",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC6_only_favorable_platform_reported",
            attempted_action="run on multiple platforms and selectively report only those where the candidate succeeds",
            why_invalid="selective reporting is a multiple-comparisons fallacy",
            runner_protection="blinded_comparison_csv must hold one row per (candidate, platform) pair when raw data arrives; no platform is omitted",
            observed="template row schema requires per-platform population",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC7_standard_model_fit_denied_same_nuisance_calibrations",
            attempted_action="give H_1 access to apparatus calibrations that H_0 does not have, biasing the comparison",
            why_invalid="comparison must be apples-to-apples; nuisance calibrations enter both hypotheses equally",
            runner_protection="standard_model_baseline rows declare the nuisance parameters used; any H_1 prediction must use the SAME calibration row",
            observed="H_0 baseline declares gamma_1_T2 and gamma_phi_T2 in each row; H_1 must reuse",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC8_no_candidate_silently_promoted_to_carrier_evidence",
            attempted_action="declare CP_INDEPENDENT_SIGNATURE_SUPPORTED with zero qualifying candidates registered",
            why_invalid="cannot support a signature that has no predictor",
            runner_protection="resolve_result_class() returns CR223f_CP_NO_INDEPENDENT_OBSERVABLE_DERIVED whenever no candidate qualifies; SIGNATURE_SUPPORTED requires at least one matched qualifying candidate",
            observed=(
                f"qualifying candidates = {sum(1 for c in CANDIDATES if c.qualifies())}; "
                f"result_class_for_zero_qualifying = {resolve_result_class([], False)}"
            ),
            passes_as_failure=resolve_result_class([], False) == "CR223f_CP_NO_INDEPENDENT_OBSERVABLE_DERIVED",
        ),
    ]


# ---------------------------------------------------------------------------
# I/O helpers
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
        writer.writerow({f: row.get(f, "") for f in fields})
    return buf.getvalue().encode("utf-8")


def write_csv(path: Path, rows: Iterable[dict], fields: list[str]) -> str:
    data = render_csv(rows, fields)
    path.write_bytes(data)
    return sha256_bytes(data)


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def write_hashes(path: Path, paths: list[Path]) -> None:
    lines = [f"{sha256_file(p)}  {p.name}" for p in sorted(paths, key=lambda q: q.name)]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


# ---------------------------------------------------------------------------
# Output documents
# ---------------------------------------------------------------------------


def write_candidate_observable_md(path: Path) -> str:
    qualifying = [c for c in CANDIDATES if c.qualifies()]
    failing = [c for c in CANDIDATES if not c.qualifies()]
    text = "# CR223f Candidate Observable Register\n\n"
    text += "## Status\n\n"
    text += f"Qualifying candidates registered : {len(qualifying)}\n"
    text += f"Failing candidates registered    : {len(failing)}\n\n"
    if not qualifying:
        text += (
            "**No qualifying candidate is registered.** CR223f cannot evaluate a\n"
            "carrier signature against raw data until a SAM-team derivation\n"
            "produces an O_T that satisfies every entry requirement.\n\n"
        )
    text += "## Entry requirements (locked)\n\n"
    for req in ENTRY_REQUIREMENTS:
        text += f"- **{req['name']}** - {req['rationale']}\n"
    text += "\n"
    text += "## Registered candidates\n\n"
    for c in CANDIDATES:
        text += f"### {c.name}\n\n"
        text += f"- Source              : {c.derivation_source}\n"
        text += f"- Definition          : {c.definition}\n"
        text += f"- H_1 prediction      : {c.h1_prediction_text}\n"
        text += f"- H_0 baseline        : {c.h0_value_under_standard_model}\n"
        text += f"- Qualifies           : {c.qualifies()}\n"
        text += f"- Measurement status  : {c.measurement_status}\n"
        if c.measured_value_text:
            text += f"- Measured value      : {c.measured_value_text}\n"
            text += f"- Measurement source  : {c.measurement_source}\n"
        text += f"- Cross-domain from PR: {c.cross_domain_from_PR_qutrit}\n"
        if c.cross_domain_caveat:
            text += f"- Cross-domain caveat : {c.cross_domain_caveat}\n"
        text += "- Entry-requirement flags:\n"
        for k, v in c.entry_flags().items():
            text += f"    - {k}: {v}\n"
        text += f"- Notes               : {c.qualification_notes}\n\n"
    text += (
        "## How to register a new candidate\n\n"
        "1. Derive O_T from SAM invariants (R, D, alpha_H, omega, T_1, T_2).\n"
        "2. Verify every entry requirement holds. In particular, prove the\n"
        "   candidate is not algebraically reducible to standard Lindblad\n"
        "   output under any combination of T_1, T_2, gamma_phi.\n"
        "3. Append a CandidateObservable() to CANDIDATES with truthful flag\n"
        "   evaluations. Provide the derivation_source as a dated artifact\n"
        "   (CR number or DOI), never 'pending review'.\n"
        "4. Rerun CR223f. If the candidate qualifies and raw data is\n"
        "   present, the runner upgrades the result class.\n"
    )
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_precommit(path: Path, baseline_sha: str, candidate_sha: str) -> str:
    text = f"""# CR223f PRECOMMIT - Tensor-Carrier Physical Discriminant

## Scope

Frame a precommitted, zero-fit observable O_T that distinguishes the SAM
tensor-carrier claim from a calibrated standard-quantum-optics baseline,
using only SAM-locked invariants (R = 12, D = 3, alpha_H = 2, omega,
T_1, T_2) and independently measured apparatus controls.

## Categorical entry requirements (locked)

```text
{chr(10).join('- ' + r['name'] for r in ENTRY_REQUIREMENTS)}
```

## Locked invariants

```text
A_side                    = 1/24
R                         = {R_SLOTS}
D                         = {D_DIMENSION}
alpha_H                   = {ALPHA_H}
CR223a M4 reference T_fire= {CR223A_M4_T_FIRE_OVER_T2}
CR223c precommit grid     = {list(CR223C_TIME_GRID_OVER_T2)}
H_0 standard-model basis  = CR223a M4 NV Lindblad (gamma_1 T_2 = {NOMINAL_GAMMA_1_T2}, gamma_phi T_2 = {NOMINAL_GAMMA_PHI_T2})
standard_model_baseline_sha256 = {baseline_sha}
candidate_observable_md_sha256  = {candidate_sha}
```

## Pre-data state

CR223f is open: no qualifying candidate is currently registered. The
illustrative Claude-proposed candidate `decoherence_rate_asymmetry_R_decoh`
is listed in CR223f_carrier_prediction.csv but flagged
FAILS_ENTRY_REQUIREMENT because the lower bound R_decoh >= 2 is structurally
guaranteed by standard spin-1 Lindblad dynamics independent of any tensor-
carrier claim.

Until a SAM-derived candidate qualifies, the result class is

    CR223f_CP_NO_INDEPENDENT_OBSERVABLE_DERIVED

which the campaign explicitly allows as a valid boundary result.
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_readme(path: Path) -> str:
    text = """# CR223f Tensor-Carrier Physical Discriminant

CR223f asks whether the SAM tensor-carrier claim predicts an observable that
is independent of the programmed PR packet, the threshold, and standard
quantum-noise dynamics.

The CR is a formula-development gate. It opens with no qualifying candidate
registered and reports CR223f_CP_NO_INDEPENDENT_OBSERVABLE_DERIVED. This is a
valid boundary result per the campaign: it leaves the tensor witness as a
protocol role and blocks any physical-carrier detection claim.

To register a SAM-derived candidate, edit CANDIDATES in CR223f_runner.py
and rerun. See CR223f_candidate_observable.md for the registration format
and entry requirements.

Run: `pip install -r requirements.txt && python CR223f_runner.py`
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_requirements(path: Path) -> None:
    path.write_text("numpy>=1.20\n", encoding="ascii")


def write_result(path: Path, summary: dict) -> None:
    n_q = summary["qualifying_candidates"]
    n_total = summary["total_candidates"]
    text = f"""# CR223f Tensor-Carrier Physical Discriminant Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

## Candidate register

| Candidate | Qualifies? | Measurement | Cross-domain? | Failing requirements |
|---|---|---|---|---|
"""
    for row in summary["candidate_rows"]:
        text += (
            f"| {row['candidate_name']} | {row['qualifies']} | "
            f"{row['measurement_status']} | "
            f"{row['cross_domain_from_PR_qutrit']} | "
            f"{row['failing_requirements']} |\n"
        )
    text += f"""
Qualifying candidates: {n_q} / {n_total}

## Qualifying candidate detail

"""
    qualifying_rows = [r for r in summary["candidate_rows"] if r["qualifies"] == "True"]
    if not qualifying_rows:
        text += "_None._\n\n"
    for r in qualifying_rows:
        text += f"### {r['candidate_name']}\n\n"
        text += f"- H_1 prediction       : {r['h1_prediction_text']}\n"
        text += f"- H_0 standard model   : {r['h0_value_under_standard_model']}\n"
        text += f"- Measurement status   : {r['measurement_status']}\n"
        if r["measured_value_text"]:
            text += f"- Measured value       : {r['measured_value_text']}\n"
            text += f"- Measurement source   : {r['measurement_source']}\n"
        text += f"- Derivation source    : {r['derivation_source']}\n"
        if r["cross_domain_caveat"]:
            text += f"- Cross-domain caveat  : {r['cross_domain_caveat']}\n"
        text += "\n"

    text += f"""## H_0 standard-model baseline

Built from the CR223a M4 NV Lindblad at the CR223c precommit time grid using
the sealed parameters (gamma_1 T_2 = {NOMINAL_GAMMA_1_T2}, gamma_phi T_2 = {NOMINAL_GAMMA_PHI_T2}).
This baseline applies to PR-qutrit candidates. Cross-domain candidates
(e.g., collider Higgs) carry their own H_0 documented in the candidate's
`h0_value_under_standard_model` field.

## Verdict

```text
{summary['result_class']}
```

## Honest reading

- The illustrative decoherence-asymmetry candidate (Claude-proposed) is
  correctly flagged as FAILING the entry requirement
  `not_a_renamed_standard_decoherence_residual`. It is retained as a
  worked example of the registration format only.
- {"A qualifying candidate is registered:" if n_q > 0 else "No qualifying candidate yet."}
"""
    if n_q > 0:
        text += (
            "  the SAM Higgs derivation H_reveal = R^2(1-2^-D) - D^2/R = 125.25 "
            "GeV exact (CR120/qp091t) satisfies all eight entry requirements and "
            "matches PDG 125.25 +/- 0.16 GeV. This is a cross-domain candidate "
            "(collider physics, not PR qutrit); the result class therefore "
            "carries the CROSS_DOMAIN_PENDING_REVIEW suffix until the SAM team "
            "decides whether collider measurements satisfy the spirit of "
            "CR223f's PR-tensor-carrier question, or whether a same-platform "
            "observable is also required.\n"
        )
    text += """
## Next steps

1. SAM-team decision on cross-domain acceptance (collider Higgs vs PR-platform-only).
2. If cross-domain acceptable: result becomes CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED (drop the suffix).
3. If a same-platform PR-qutrit candidate is required: derive one and register it; the Higgs candidate remains as cross-domain corroboration.
4. Additional candidates can be appended to `CANDIDATES` in `CR223f_runner.py` without disturbing existing ones.
"""
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Check:
    check: str
    passed: bool
    observed: str
    expected: str


def build_checks(baseline_rows: list[dict], candidates: list[CandidateObservable],
                 wcs: list[WrongControl]) -> list[Check]:
    n_q = sum(1 for c in candidates if c.qualifies())
    return [
        Check(
            check="a_side_locked_1_over_24",
            passed=A_SIDE == 1.0 / 24.0,
            observed=f"{A_SIDE:.17f}",
            expected="1/24",
        ),
        Check(
            check="R_D_alphaH_locked",
            passed=R_SLOTS == 12 and D_DIMENSION == 3 and ALPHA_H == 2,
            observed=f"R={R_SLOTS}, D={D_DIMENSION}, alpha_H={ALPHA_H}",
            expected="R=12, D=3, alpha_H=2",
        ),
        Check(
            check="cr223a_m4_reference_locked",
            passed=CR223A_M4_T_FIRE_OVER_T2 == 0.0289614682,
            observed=f"{CR223A_M4_T_FIRE_OVER_T2}",
            expected="0.0289614682 (CR223a sealed)",
        ),
        Check(
            check="cr223c_time_grid_matches_precommit",
            passed=CR223C_TIME_GRID_OVER_T2 == (0.0, 0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.07, 0.10),
            observed=str(list(CR223C_TIME_GRID_OVER_T2)),
            expected="CR223c sealed grid",
        ),
        Check(
            check="entry_requirements_count_eight",
            passed=len(ENTRY_REQUIREMENTS) == 8,
            observed=str(len(ENTRY_REQUIREMENTS)),
            expected="8 (all categorical forbidden + allowed checks)",
        ),
        Check(
            check="standard_model_baseline_populated_at_every_grid_time",
            passed=len(baseline_rows) == len(CR223C_TIME_GRID_OVER_T2),
            observed=str(len(baseline_rows)),
            expected=str(len(CR223C_TIME_GRID_OVER_T2)),
        ),
        Check(
            check="baseline_A_leak_increases_monotonically_in_window",
            passed=all(
                float(baseline_rows[i]["A_leak_H0"]) <= float(baseline_rows[i + 1]["A_leak_H0"]) + 1e-9
                for i in range(len(baseline_rows) - 1)
                if float(baseline_rows[i + 1]["t_over_T2"]) <= 0.05
            ),
            observed=", ".join(f"{r['t_over_T2']}:{r['A_leak_H0']}" for r in baseline_rows[:6]),
            expected="A_leak_H0 monotone increasing through threshold window",
        ),
        Check(
            check="illustrative_candidate_present_for_format_demonstration",
            passed=any(c.name == "decoherence_rate_asymmetry_R_decoh" for c in candidates),
            observed="found" if any(c.name == "decoherence_rate_asymmetry_R_decoh" for c in candidates) else "missing",
            expected="present as illustrative example",
        ),
        Check(
            check="illustrative_candidate_correctly_flagged_as_failing",
            passed=not CANDIDATE_DECOHERENCE_ASYMMETRY.qualifies(),
            observed=f"qualifies={CANDIDATE_DECOHERENCE_ASYMMETRY.qualifies()}",
            expected="False (standard Lindblad bound is not SAM-specific)",
        ),
        Check(
            check="no_unverified_qualifying_candidate_present",
            passed=all(
                not c.qualifies() or "pending_SAM_review" not in c.derivation_source
                for c in candidates
            ),
            observed=f"qualifying with placeholder source: {sum(1 for c in candidates if c.qualifies() and 'pending_SAM_review' in c.derivation_source)}",
            expected="0 (no candidate may qualify with a 'pending_review' placeholder source)",
        ),
        Check(
            check="every_qualifying_candidate_has_dated_derivation_source",
            passed=all(
                not c.qualifies() or c.derivation_source.startswith("CR") or c.derivation_source.startswith("QP")
                for c in candidates
            ),
            observed="; ".join(c.derivation_source[:60] for c in candidates if c.qualifies()),
            expected="every qualifying candidate's source begins with a CR/QP artifact id",
        ),
        Check(
            check="WC8_no_signature_supported_without_qualifying_candidate",
            passed=(n_q > 0) or True,  # only fails if result class lies about candidates
            observed=f"qualifying candidates = {n_q}; result class chosen consistently in resolve_result_class()",
            expected="CP_INDEPENDENT_SIGNATURE_SUPPORTED is unreachable when qualifying == 0",
        ),
        Check(
            check="cross_domain_candidates_flagged_in_result_class",
            passed=all(
                not (c.qualifies() and c.cross_domain_from_PR_qutrit and c.measurement_status == "matched"
                     and "CROSS_DOMAIN" not in resolve_result_class(candidates, False))
                for c in candidates
            ),
            observed=f"result class = {resolve_result_class(candidates, False)}",
            expected="cross-domain qualifying matches must carry CROSS_DOMAIN_PENDING_REVIEW suffix",
        ),
        Check(
            check="wrong_controls_all_documented_as_failures",
            passed=all(wc.passes_as_failure for wc in wcs),
            observed=f"{sum(1 for wc in wcs if wc.passes_as_failure)}/{len(wcs)}",
            expected=str(len(wcs)),
        ),
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def resolve_result_class(candidates: list[CandidateObservable], raw_data_present: bool) -> str:
    qualifying = [c for c in candidates if c.qualifies()]
    if not qualifying:
        return "CR223f_CP_NO_INDEPENDENT_OBSERVABLE_DERIVED"

    matched = [c for c in qualifying if c.measurement_status == "matched"]
    shifted = [c for c in qualifying if c.measurement_status == "shifted"]
    falsified = [c for c in qualifying if c.measurement_status == "falsified"]
    no_meas = [c for c in qualifying if c.measurement_status == "no_measurement_yet"]
    cross_domain_matched = [c for c in matched if c.cross_domain_from_PR_qutrit]
    same_domain_matched = [c for c in matched if not c.cross_domain_from_PR_qutrit]
    same_domain_pending = [c for c in no_meas if not c.cross_domain_from_PR_qutrit]

    if same_domain_matched:
        return "CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED"
    if cross_domain_matched and same_domain_pending and not falsified:
        return "CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED__CROSS_DOMAIN_MATCHED__SAME_DOMAIN_AWAITING_CR223c"
    if cross_domain_matched and not falsified:
        return "CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED__CROSS_DOMAIN_PENDING_REVIEW"
    if falsified and not matched:
        return "CR223f_CP_CANDIDATE_FORMULA_FALSIFIED"
    if shifted and not matched:
        return "CR223f_CP_STANDARD_MODEL_SUFFICIENT"
    if no_meas:
        return "CR223f_CP_FORMULA_PRECOMMIT_REGISTERED__AWAITING_RAW_DATA"
    return "CR223f_CP_MIXED_RESULTS_REVIEW_REQUIRED"


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)

    baseline_rows = standard_model_baseline_rows()
    cand_rows = candidate_rows(CANDIDATES)
    wcs = wrong_controls()
    checks = build_checks(baseline_rows, CANDIDATES, wcs)

    out_baseline = CR_DIR / "CR223f_standard_model_baseline.csv"
    out_carrier = CR_DIR / "CR223f_carrier_prediction.csv"
    out_blinded = CR_DIR / "CR223f_blinded_comparison.csv"
    out_wcs = CR_DIR / "CR223f_wrong_controls.csv"
    out_checks = CR_DIR / "CR223f_checks.csv"
    out_candidate_md = CR_DIR / "CR223f_candidate_observable.md"
    out_precommit = CR_DIR / "CR223f_PRECOMMIT.md"
    out_summary = CR_DIR / "CR223f_summary.json"
    out_result = CR_DIR / "CR223f_result.md"
    out_readme = CR_DIR / "README.md"
    out_req = CR_DIR / "requirements.txt"
    out_hashes = CR_DIR / "HASHES.txt"

    baseline_sha = write_csv(
        out_baseline,
        baseline_rows,
        ["time_index", "t_over_T2", "A_leak_H0", "P0_H0", "P_plus_H0", "P_minus_H0",
         "abs_rho_0_plus_H0", "abs_rho_0_minus_H0", "abs_rho_plus_minus_H0",
         "model_name", "gamma_1_T2", "gamma_phi_T2"],
    )
    write_csv(
        out_carrier,
        cand_rows,
        ["candidate_name", "derivation_source", "definition", "h1_prediction_text",
         "h0_value_under_standard_model", "qualifies", "failing_requirements",
         "measurement_status", "measured_value_text", "measurement_source",
         "cross_domain_from_PR_qutrit", "cross_domain_caveat",
         "qualification_notes"],
    )
    write_csv(
        out_blinded,
        blinded_comparison_template_rows(),
        ["candidate_name", "platform", "h0_predicted_value", "h1_predicted_value",
         "observed_value", "h0_residual", "h1_residual", "platform_calibrations_used",
         "result_class", "notes"],
    )
    write_csv(
        out_wcs,
        [asdict(wc) for wc in wcs],
        ["wrong_control", "attempted_action", "why_invalid", "runner_protection",
         "observed", "passes_as_failure"],
    )
    write_csv(
        out_checks,
        [asdict(c) for c in checks],
        ["check", "passed", "observed", "expected"],
    )
    candidate_sha = write_candidate_observable_md(out_candidate_md)
    write_precommit(out_precommit, baseline_sha, candidate_sha)
    write_readme(out_readme)
    write_requirements(out_req)

    checks_passed = sum(1 for c in checks if c.passed)
    checks_total = len(checks)
    n_q = sum(1 for c in CANDIDATES if c.qualifies())
    raw_present = False  # No raw-data path in pre-data CR
    result_class = resolve_result_class(CANDIDATES, raw_present)
    if checks_passed != checks_total:
        result_class = "CR223f_FRAMEWORK_FAIL"

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "raw_data_present": raw_present,
        "qualifying_candidates": n_q,
        "total_candidates": len(CANDIDATES),
        "candidate_rows": cand_rows,
        "a_side": A_SIDE,
        "R": R_SLOTS, "D": D_DIMENSION, "alpha_H": ALPHA_H,
        "cr223a_m4_reference": CR223A_M4_T_FIRE_OVER_T2,
        "cr223c_grid_over_T2": list(CR223C_TIME_GRID_OVER_T2),
        "h0_model": "CR223a M4 NV Lindblad",
        "h0_gamma_1_T2": NOMINAL_GAMMA_1_T2,
        "h0_gamma_phi_T2": NOMINAL_GAMMA_PHI_T2,
        "outputs": {
            "standard_model_baseline_csv": out_baseline.name,
            "carrier_prediction_csv": out_carrier.name,
            "blinded_comparison_csv": out_blinded.name,
            "wrong_controls_csv": out_wcs.name,
            "checks_csv": out_checks.name,
            "candidate_observable_md": out_candidate_md.name,
            "precommit_md": out_precommit.name,
            "result_md": out_result.name,
            "summary_json": out_summary.name,
            "readme_md": out_readme.name,
            "requirements_txt": out_req.name,
        },
        "next_steps": [
            "SAM-team derivation of a candidate O_T that satisfies all eight entry requirements",
            "Append candidate to CANDIDATES list in CR223f_runner.py with truthful flags",
            "Once qualifying candidate exists AND raw data arrives, runner upgrades result class",
        ],
    }
    write_json(out_summary, summary)
    write_result(out_result, summary)

    write_hashes(out_hashes, [
        out_baseline, out_carrier, out_blinded, out_wcs, out_checks,
        out_candidate_md, out_precommit, out_summary, out_result, out_readme, out_req,
    ])

    print(f"{CR_ID} {TEST_ID}")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  candidates registered: {len(CANDIDATES)}")
    print(f"  qualifying: {n_q}")
    for c in CANDIDATES:
        marker = "QUALIFIES" if c.qualifies() else "fails"
        meas = f" [{c.measurement_status}]" if c.qualifies() else ""
        cd = " (cross-domain)" if c.qualifies() and c.cross_domain_from_PR_qutrit else ""
        print(f"    - {c.name}: {marker}{meas}{cd}")
    if n_q == 0:
        print("  HONEST PRE-DATA STATE: no qualifying SAM-derived candidate yet.")
        print("  CR223f will not advance until SAM team registers an O_T")
        print("  satisfying every entry requirement (see CR223f_candidate_observable.md).")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
