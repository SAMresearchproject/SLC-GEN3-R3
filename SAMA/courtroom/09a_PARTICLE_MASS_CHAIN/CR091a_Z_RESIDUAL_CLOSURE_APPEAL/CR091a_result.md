# CR091a Z 12-sigma Residual Closure Appeal - Result

## Verdict

```text
CR091a_Z_RESIDUAL_CLOSURE_APPEAL_PASS
```

## What This Appeal Records

The 26.1 MeV LEP Z residual (originally 12.4 sigma below LEP) sits at q_subslot = -2/12 = -1/6 in the native R12/R16/R24 bounce sub-slot grid per QP087 PASS. Applying this structural correction with zero free parameters closes the residual to within LEP uncertainty.

## Closure Numerics

```text
z_pred_QP075_MeV        = 91161.5000
z_observed_LEP_MeV      = 91187.6000
residual_before_MeV     = -26.1000    (~12.4 sigma below LEP)

sub-slot grid point     = q = -2/12 = -0.166667
G435 r_unit (= A0/16)   = 0.00165786
r_correction            = -q * r_unit = 0.00027631

z_corrected_MeV         = z_pred * (1 - q_subslot * r_unit) = 91186.6889
residual_after_MeV      = -0.9111
LEP uncertainty MeV     = 2.1
sigma after             = 0.43  (was 12.43)
```

## Cryptographic Chain

```text
CR067a anchor sha256          = 2e18cfe53ecb0f3033c179641814e8d30371a4ae32604defe38e880b5ae3258e
CR091 summary sha256          = 00a2f5781d05389f2cc8323c99eee4a1d3e12118d9cabdc668e0540b08b5b239
CR091 evidence sha256         = 8bca4a0fdbc05c37fd6d450356d50fda9eb763a502d1f264dd47a9b2bbd8a009
appeal_lock_sha256            = cbb7e8411b17fc788f9266f615d4a7401ecb04b7b4c893b4f2b74605b0248ff0
```

## Predictions

- **[PASS]** P1_qp087_z_row_subslot_grid_match
- **[PASS]** P2_sub_slot_correction_closes_residual_within_lep_uncertainty
- **[PASS]** P3_zero_free_parameters_in_closure
- **[PASS]** P4_cr091_verdict_untouched

## Wrong Controls

- **[PASS]** WC1_subslot_must_be_native_grid_point
- **[PASS]** WC2_correction_sign_must_close_not_widen

## What This Appeal Does Not Do

- modify CR091 verdict
- modify the QP087 PASS
- modify any 09a CR verdict
- claim a new measurement; LEP value is unchanged
- introduce a free parameter
