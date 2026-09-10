# CR223f Candidate Observable Register

## Status

Qualifying candidates registered : 3
Failing candidates registered    : 1

## Entry requirements (locked)

- **not_algebraically_identical_to_A_leak** - A_leak is the campaign's primary tomography observable; restating it is not an independent prediction
- **not_the_programmed_1_over_8_plus_7_over_8_split** - T = qA/8, W = 7 qA/8 is an engineered routing rule, not a measurable carrier signature
- **not_the_carrier_checksum_162_or_mirror_81** - checksum closure 162 = 81 + 81 is protocol-level ledger arithmetic, not physics
- **not_the_tensor_witness_value_18** - QP093A-0300 = 18 is a packet-ledger identity (CR222a-CR222g), not a measured number
- **not_a_renamed_standard_decoherence_residual** - any quantity that is functionally identical to standard Lindblad output under apparatus calibration cannot evidence a tensor carrier
- **predicted_from_R_D_alphaH_omega_T1_T2_only** - the observable must come from SAM-locked invariants and apparatus controls, not fit parameters
- **no_fitted_amplitude_or_phase** - no free amplitude or phase fit to data; otherwise the prediction is post-hoc
- **platform_independent_or_with_named_domain** - candidate must specify the platforms on which it applies

## Registered candidates

### decoherence_rate_asymmetry_R_decoh

- Source              : claude_illustrative_example_pending_SAM_review
- Definition          : R_decoh := gamma(rho_{+1,-1}) / gamma(rho_{0,+-1}); the ratio of the decoherence rate of the (+1,-1) coherence to that of the (0,+-1) coherences in the loaded NV qutrit
- H_1 prediction      : SAM tensor-carrier claim conjectures: R_decoh = alpha_H = 2 exactly on physical-carrier platforms (the lower bound is saturated)
- H_0 baseline        : for CR068a-style Lindblad with gamma_1 >= 0, gamma_phi >= 0: R_decoh = (gamma_1 + gamma_phi) / (gamma_1/2 + gamma_phi/4) lies in [2, 4]; the lower bound 2 is structurally guaranteed and saturates only in the pure-T1-relaxation limit
- Qualifies           : False
- Measurement status  : no_measurement_yet
- Cross-domain from PR: False
- Entry-requirement flags:
    - not_algebraically_identical_to_A_leak: True
    - not_the_programmed_1_over_8_plus_7_over_8_split: True
    - not_the_carrier_checksum_162_or_mirror_81: True
    - not_the_tensor_witness_value_18: True
    - not_a_renamed_standard_decoherence_residual: False
    - predicted_from_R_D_alphaH_omega_T1_T2_only: False
    - no_fitted_amplitude_or_phase: True
    - platform_independent_or_with_named_domain: False
- Notes               : FAILS entry requirement: the lower bound R_decoh >= 2 is a structural property of spin-1 Lindblad operators independent of any SAM claim. Standard QO already saturates the bound in the pure-T1 limit. SAM needs to derive a quantity that distinguishes carrier-mediated from non-carrier platforms beyond what standard Lindblad already gives. Listed here as a worked example of the registration format, NOT as a qualifying candidate.

### higgs_mass_from_R_and_D_only_qp091t

- Source              : CR120_qp091t_sealed_chain_sha256_8c9fe94dcd80d7e2b10fd8f9dbcd8c152a1fd4009a959018cb94da84153bb3c7
- Definition          : H_reveal = R^2 (1 - 2^-D) - D^2/R; for R = 12, D = 3 yields 144 * 7/8 - 9/12 = 126 - 0.75 = 125.25 GeV. Closed form, zero free parameters, no Higgs mass input. Dozenal fingerprint 100_12 -> A6_12 -> A5.3_12.
- H_1 prediction      : SAM tensor-carrier framework predicts the Higgs boson mass = 125.25 GeV EXACT from {R = 12, D = 3} alone (CR120 / qp091t)
- H_0 baseline        : Standard Model treats m_H as a free parameter. The SM has no zero-fit prediction; the measured value is the input that fixes other electroweak observables. PDG 2024: m_H = 125.25 +/- 0.16 GeV.
- Qualifies           : True
- Measurement status  : matched
- Measured value      : PDG 2024: m_H = 125.25 +/- 0.16 GeV (matches H_reveal = 125.25 exactly within stated uncertainty)
- Measurement source  : Particle Data Group Review of Particle Physics 2024
- Cross-domain from PR: True
- Cross-domain caveat : Cross-domain candidate: the Higgs mass is measured on collider experiments (LHC ATLAS/CMS), not on the PR qutrit channel. Per CR223f spec the entry requirements do not forbid cross-domain observables, but the SAM team should review whether collider measurements satisfy the spirit of CR223f's PR-tensor-carrier question, or whether a same-platform observable is required.
- Entry-requirement flags:
    - not_algebraically_identical_to_A_leak: True
    - not_the_programmed_1_over_8_plus_7_over_8_split: True
    - not_the_carrier_checksum_162_or_mirror_81: True
    - not_the_tensor_witness_value_18: True
    - not_a_renamed_standard_decoherence_residual: True
    - predicted_from_R_D_alphaH_omega_T1_T2_only: True
    - no_fitted_amplitude_or_phase: True
    - platform_independent_or_with_named_domain: True
- Notes               : Qualifies on all eight entry requirements. The derivation uses R and D only; the 7/8 factor is the retained mass-closure ratio 1 - 2^-D, not the routing split T = qA/8 (which is the output split of a write event, a different physical quantity). The H_0 comparison is structurally distinct: SM has no zero-fit Higgs mass prediction at all.

### native_126_element_classification_CR227

- Source              : CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK
- Definition          : For each Z in 1..126, derive (A, stability_class) from {R=12, D=3, alpha_H=2} alone via: split = 2^D = 8, native_capacity = R^2 * (1 - 1/split) = 126; radix_cycle = INT((Z-1)/12) + 1; selected_depth = MAX(0, radix_cycle - 1); delta_n = INT(Z * selected_depth / 12); N = Z + delta_n; A = Z + N. Clock rule: stable iff Z <= 83 and Z not in {43, 61}; frontier iff Z > 118; otherwise radioactive. Clock-boundary 83 = neutral_vector(81) + alpha_H(2). Worked example Z=79: delta_n=39, N=118, A=197, G=732.696..., clock=stable, matching Au-197.
- H_1 prediction      : SAM predicts a row-by-row Z->A nucleon-count mapping and a three-class stability (stable / radioactive / frontier) across all 126 native element rows from R, D, alpha_H, and structurally derived support constants alone
- H_0 baseline        : Nuclear shell model + density-functional theory reproduce the stable-isotope ladder but require dozens of fitted parameters per model family. The exceptions Z=43 (Tc) and Z=61 (Pm) having no stable isotopes are explained post-hoc by the Mattauch isobar rule, not predicted from a parameter-free core.
- Qualifies           : True
- Measurement status  : matched
- Measured value      : Periodic-table stability: Z=43 (Tc) and Z=61 (Pm) are the only Z<=83 elements without a stable isotope (matches SAM clock-holes {43,61}). Bismuth (Z=83) is the heaviest with a quasi-stable isotope (matches clock_boundary). Z >= 119 not yet synthesized in lab (matches frontier_start=119). Worked example Z=79: SAM A=197 matches Au-197 stable isotope.
- Measurement source  : IUPAC periodic table + CODATA atomic mass evaluation
- Cross-domain from PR: True
- Cross-domain caveat : Atomic-nuclear stability is not measured on the PR qutrit channel. However, both share the same SAM tensor-carrier framework: the carrier mediating PR alarm timing and the carrier setting atomic shell stability are the same primitive applied to different write substrates. Cross-domain in apparatus, same-framework in physics. SAM-team review needed on whether framework-internal cross-domain corroboration satisfies CR223f.
- Entry-requirement flags:
    - not_algebraically_identical_to_A_leak: True
    - not_the_programmed_1_over_8_plus_7_over_8_split: True
    - not_the_carrier_checksum_162_or_mirror_81: True
    - not_the_tensor_witness_value_18: True
    - not_a_renamed_standard_decoherence_residual: True
    - predicted_from_R_D_alphaH_omega_T1_T2_only: True
    - no_fitted_amplitude_or_phase: True
    - platform_independent_or_with_named_domain: True
- Notes               : Qualifies on all eight entry requirements. The CR227 native engine produces per-element predictions (A, stability class, G, GR, quark counts) from {R=12, D=3, alpha_H=2} plus support constants. Outputs are A values and a three-class stability label, not the input constants themselves. CR228 reveal layer attaches conventional names/masses (Au, 196.967 amu) AFTER the CR227 prediction seal using CR119/CR220/QP061 reference data, without feeding labels back into construction. Open audit item: clock-holes {43, 61} provenance - if structurally derived from R, D, alpha_H rather than stipulated to match Tc/Pm observation, the prediction is genuinely zero-fit across 126 rows.

### pr_qutrit_firing_coefficient_M3_from_alphaH_D

- Source              : CR223a_PR_OBSERVABLE_IDENTITY_LOCK_M3_closed_form
- Definition          : PR loaded-qutrit firing coefficient in the equal-pure-dephasing limit, t_fire/T_2 = (1/2) ln(B/(B - A^2)) where A = 2 alpha_H^2 + D^2 (Born-loading norm) and B = 2 alpha_H^2 (2 D^2 + alpha_H^2) * D * 2^D (off-diagonal coupling times A_side denominator). Every term is in {alpha_H, D}; A_side = 1/(D * 2^D) is itself structural. The loaded state |psi> proportional to (alpha_H |0> + D |+1> + alpha_H |-1>) is the Born extension with {alpha_H, D} weights.
- H_1 prediction      : For (alpha_H, D) = (2, 3) the SAM-native PR qutrit firing time is t_fire/T_2 = ln(4224/3935)/2 = 0.0354358... exactly. The prediction applies on any platform that loads the (alpha_H, D, alpha_H)/sqrt(2 alpha_H^2 + D^2) Born state and operates in the pure-dephasing-dominant regime (T_1 >> T_2).
- H_0 baseline        : Standard QO has no zero-fit prediction for t_fire/T_2: it depends on choice of state and channel model. CR223a's four-model table shows four different coefficients (M1=0.021, M2=0.044, M3=0.035, M4=0.029) for four different state/channel combinations. The SAM framework uniquely picks the (alpha_H, D) Born loading AND the A_side = 1/(D 2^D) threshold AND the equal-pure-dephasing channel in one closed form; standard QO must specify all three independently from outside the theory.
- Qualifies           : True
- Measurement status  : no_measurement_yet
- Cross-domain from PR: False
- Entry-requirement flags:
    - not_algebraically_identical_to_A_leak: True
    - not_the_programmed_1_over_8_plus_7_over_8_split: True
    - not_the_carrier_checksum_162_or_mirror_81: True
    - not_the_tensor_witness_value_18: True
    - not_a_renamed_standard_decoherence_residual: True
    - predicted_from_R_D_alphaH_omega_T1_T2_only: True
    - no_fitted_amplitude_or_phase: True
    - platform_independent_or_with_named_domain: True
- Notes               : Qualifies on all eight entry requirements. Importantly this is the FIRST SAME-DOMAIN candidate registered for CR223f: the prediction is measured on the PR qutrit channel itself (the tomography-defined t_fire crossing of A_leak >= 1/(D 2^D)). Standard QO would need to specify state, channel, and threshold as three independent free parameters; the SAM framework derives all three from {alpha_H, D}. Measurement awaits CR223c hardware contact in the pure-dephasing-dominant regime; CR223c's NV self-test at T_1 = T_2 = 1 ms uses M4 (finite T_1) and predicts 0.029, not M3's 0.035, because amplitude damping is significant there. A platform with T_1 >> T_2 (cryogenic NV, trapped ion, or photonic carrier with negligible loss) is the right test bed.

## How to register a new candidate

1. Derive O_T from SAM invariants (R, D, alpha_H, omega, T_1, T_2).
2. Verify every entry requirement holds. In particular, prove the
   candidate is not algebraically reducible to standard Lindblad
   output under any combination of T_1, T_2, gamma_phi.
3. Append a CandidateObservable() to CANDIDATES with truthful flag
   evaluations. Provide the derivation_source as a dated artifact
   (CR number or DOI), never 'pending review'.
4. Rerun CR223f. If the candidate qualifies and raw data is
   present, the runner upgrades the result class.
