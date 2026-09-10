# CR021 Planck-Lite CMB Density and BBN Contact

## Verdict

```text
CR021_BOUNDARY_PASS_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT
```

## Key Packet

```text
G381 primary_high_l_delta_chi2_per_point = 0.0008836165765404745
G381 wrong_control_high_l_delta_chi2_per_point = 1.472411841957094
G396 omega_b_h2_primary = 0.022368783502886305
G396 eta10_primary = 6.126809801440558
```

## Scope Boundary

```text
Planck-lite / BBN contact only; no full Planck likelihood, recombination, perturbation, TT/TE/EE theorem-grade closure.
```

## Pass Conditions

| condition | pass |
|---|---:|
| G379_card_frozen | true |
| G380_smoke_passed | true |
| G381_planck_lite_passed | true |
| G381_primary_better_than_wrong_control | true |
| G382_residuals_passed | true |
| G383_wrong_controls_passed | true |
| G384_claim_lock_passed | true |
| G396_bbn_scoped_passed | true |
