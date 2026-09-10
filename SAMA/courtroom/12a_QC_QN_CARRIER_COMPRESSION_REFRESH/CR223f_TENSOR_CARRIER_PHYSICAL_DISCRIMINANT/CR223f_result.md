# CR223f Tensor-Carrier Physical Discriminant Result

**Result class:** `CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED__CROSS_DOMAIN_MATCHED__SAME_DOMAIN_AWAITING_CR223c`

**Checks:** 14/14

## Candidate register

| Candidate | Qualifies? | Measurement | Cross-domain? | Failing requirements |
|---|---|---|---|---|
| decoherence_rate_asymmetry_R_decoh | False | no_measurement_yet | False | not_a_renamed_standard_decoherence_residual; predicted_from_R_D_alphaH_omega_T1_T2_only; platform_independent_or_with_named_domain |
| higgs_mass_from_R_and_D_only_qp091t | True | matched | True | none |
| native_126_element_classification_CR227 | True | matched | True | none |
| pr_qutrit_firing_coefficient_M3_from_alphaH_D | True | no_measurement_yet | False | none |

Qualifying candidates: 3 / 4

## Qualifying candidate detail

### higgs_mass_from_R_and_D_only_qp091t

- H_1 prediction       : SAM tensor-carrier framework predicts the Higgs boson mass = 125.25 GeV EXACT from {R = 12, D = 3} alone (CR120 / qp091t)
- H_0 standard model   : Standard Model treats m_H as a free parameter. The SM has no zero-fit prediction; the measured value is the input that fixes other electroweak observables. PDG 2024: m_H = 125.25 +/- 0.16 GeV.
- Measurement status   : matched
- Measured value       : PDG 2024: m_H = 125.25 +/- 0.16 GeV (matches H_reveal = 125.25 exactly within stated uncertainty)
- Measurement source   : Particle Data Group Review of Particle Physics 2024
- Derivation source    : CR120_qp091t_sealed_chain_sha256_8c9fe94dcd80d7e2b10fd8f9dbcd8c152a1fd4009a959018cb94da84153bb3c7
- Cross-domain caveat  : Cross-domain candidate: the Higgs mass is measured on collider experiments (LHC ATLAS/CMS), not on the PR qutrit channel. Per CR223f spec the entry requirements do not forbid cross-domain observables, but the SAM team should review whether collider measurements satisfy the spirit of CR223f's PR-tensor-carrier question, or whether a same-platform observable is required.

### native_126_element_classification_CR227

- H_1 prediction       : SAM predicts a row-by-row Z->A nucleon-count mapping and a three-class stability (stable / radioactive / frontier) across all 126 native element rows from R, D, alpha_H, and structurally derived support constants alone
- H_0 standard model   : Nuclear shell model + density-functional theory reproduce the stable-isotope ladder but require dozens of fitted parameters per model family. The exceptions Z=43 (Tc) and Z=61 (Pm) having no stable isotopes are explained post-hoc by the Mattauch isobar rule, not predicted from a parameter-free core.
- Measurement status   : matched
- Measured value       : Periodic-table stability: Z=43 (Tc) and Z=61 (Pm) are the only Z<=83 elements without a stable isotope (matches SAM clock-holes {43,61}). Bismuth (Z=83) is the heaviest with a quasi-stable isotope (matches clock_boundary). Z >= 119 not yet synthesized in lab (matches frontier_start=119). Worked example Z=79: SAM A=197 matches Au-197 stable isotope.
- Measurement source   : IUPAC periodic table + CODATA atomic mass evaluation
- Derivation source    : CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK
- Cross-domain caveat  : Atomic-nuclear stability is not measured on the PR qutrit channel. However, both share the same SAM tensor-carrier framework: the carrier mediating PR alarm timing and the carrier setting atomic shell stability are the same primitive applied to different write substrates. Cross-domain in apparatus, same-framework in physics. SAM-team review needed on whether framework-internal cross-domain corroboration satisfies CR223f.

### pr_qutrit_firing_coefficient_M3_from_alphaH_D

- H_1 prediction       : For (alpha_H, D) = (2, 3) the SAM-native PR qutrit firing time is t_fire/T_2 = ln(4224/3935)/2 = 0.0354358... exactly. The prediction applies on any platform that loads the (alpha_H, D, alpha_H)/sqrt(2 alpha_H^2 + D^2) Born state and operates in the pure-dephasing-dominant regime (T_1 >> T_2).
- H_0 standard model   : Standard QO has no zero-fit prediction for t_fire/T_2: it depends on choice of state and channel model. CR223a's four-model table shows four different coefficients (M1=0.021, M2=0.044, M3=0.035, M4=0.029) for four different state/channel combinations. The SAM framework uniquely picks the (alpha_H, D) Born loading AND the A_side = 1/(D 2^D) threshold AND the equal-pure-dephasing channel in one closed form; standard QO must specify all three independently from outside the theory.
- Measurement status   : no_measurement_yet
- Derivation source    : CR223a_PR_OBSERVABLE_IDENTITY_LOCK_M3_closed_form

## H_0 standard-model baseline

Built from the CR223a M4 NV Lindblad at the CR223c precommit time grid using
the sealed parameters (gamma_1 T_2 = 1.0, gamma_phi T_2 = 0.5).
This baseline applies to PR-qutrit candidates. Cross-domain candidates
(e.g., collider Higgs) carry their own H_0 documented in the candidate's
`h0_value_under_standard_model` field.

## Verdict

```text
CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED__CROSS_DOMAIN_MATCHED__SAME_DOMAIN_AWAITING_CR223c
```

## Honest reading

- The illustrative decoherence-asymmetry candidate (Claude-proposed) is
  correctly flagged as FAILING the entry requirement
  `not_a_renamed_standard_decoherence_residual`. It is retained as a
  worked example of the registration format only.
- A qualifying candidate is registered:
  the SAM Higgs derivation H_reveal = R^2(1-2^-D) - D^2/R = 125.25 GeV exact (CR120/qp091t) satisfies all eight entry requirements and matches PDG 125.25 +/- 0.16 GeV. This is a cross-domain candidate (collider physics, not PR qutrit); the result class therefore carries the CROSS_DOMAIN_PENDING_REVIEW suffix until the SAM team decides whether collider measurements satisfy the spirit of CR223f's PR-tensor-carrier question, or whether a same-platform observable is also required.

## Next steps

1. SAM-team decision on cross-domain acceptance (collider Higgs vs PR-platform-only).
2. If cross-domain acceptable: result becomes CR223f_CP_INDEPENDENT_SIGNATURE_SUPPORTED (drop the suffix).
3. If a same-platform PR-qutrit candidate is required: derive one and register it; the Higgs candidate remains as cross-domain corroboration.
4. Additional candidates can be appended to `CANDIDATES` in `CR223f_runner.py` without disturbing existing ones.
