# CR223f PRECOMMIT - Tensor-Carrier Physical Discriminant

## Scope

Frame a precommitted, zero-fit observable O_T that distinguishes the SAM
tensor-carrier claim from a calibrated standard-quantum-optics baseline,
using only SAM-locked invariants (R = 12, D = 3, alpha_H = 2, omega,
T_1, T_2) and independently measured apparatus controls.

## Categorical entry requirements (locked)

```text
- not_algebraically_identical_to_A_leak
- not_the_programmed_1_over_8_plus_7_over_8_split
- not_the_carrier_checksum_162_or_mirror_81
- not_the_tensor_witness_value_18
- not_a_renamed_standard_decoherence_residual
- predicted_from_R_D_alphaH_omega_T1_T2_only
- no_fitted_amplitude_or_phase
- platform_independent_or_with_named_domain
```

## Locked invariants

```text
A_side                    = 1/24
R                         = 12
D                         = 3
alpha_H                   = 2
CR223a M4 reference T_fire= 0.0289614682
CR223c precommit grid     = [0.0, 0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.07, 0.1]
H_0 standard-model basis  = CR223a M4 NV Lindblad (gamma_1 T_2 = 1.0, gamma_phi T_2 = 0.5)
standard_model_baseline_sha256 = c2010c47f0add5a1884ceaabcf9cc7c59a8830832b1a46d9ab4b6ae72680d62d
candidate_observable_md_sha256  = c140a09d83c4fd6ea834eddec3c39765429e3a4b6488a448ec0085a438ff559d
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
