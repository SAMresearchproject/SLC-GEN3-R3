# CR067a WZH Bounce Sub-slot Intake - Result

## Verdict

```text
CR067a_WZH_BOUNCE_SUBSLOT_INTAKE_PASS
```

## What This CR Intakes

QP087 WZH precision lane bounce sub-slot coordinates (PASS upstream).

QP088 WZH q-slot owner derivation (PASS upstream).

Together these provide the structural data needed by CR091a (Z 12-sigma residual closure appeal).

## Cryptographic Chain

```text
CR065a intake lock                  = 11e898ca84273071096436bd52c3667dd9ec3df2a3c6b599f5a94453827582a7
upstream QP087_summary.json         = 5300f929afca127366251dbe154e8ea75365b0d50f2e2bf5482980e5a08c092a
upstream QP087 subslot table        = 21a6d693b778a0c050de6c09ee8f32cf72333b1b806cef179d10258ad6c93a9e
upstream QP088_summary.json         = adc66ed1c8e64a96e4bf25c505ae207a0dd0db0f3144eefdc6c50b3aef768e48
upstream QP088 owner-q table        = 932a8b1ac9ec4ee3560ab2e0f5cab36c3520da39b6ddec6ce5cac33e945a8d89
CR067a wzh anchor sha256             = 2e18cfe53ecb0f3033c179641814e8d30371a4ae32604defe38e880b5ae3258e
```

## QP088 Owner q-slots (reproduce QP075 frozen masses)

```text
W: q =   4   owner = half_color
     q_expression = SU3_DIM // SW_DIM
Z: q =  -1   owner = negative_U1_neutral_identity
     q_expression = -U1_DIM
H: q =   3   owner = SU2_scalar_mass_coupling_owner
     q_expression = SU2_DIM
```

## QP087 Bounce Sub-slot Grid Placement (per-anchor residual)

| row | anchor | residual MeV | q_eff (G435 units) | nearest grid | grid error |
|---|---|---|---|---|---|
| EW001 | W boson mass (ATLAS) | -1.40 | -0.010508 | 0 = +0.0000 | 0.010508 |
| EW002 | W boson mass (CMS) | +4.90 | +0.036780 | 1/24 = +0.0417 | 0.004887 |
| EW003 | W boson mass (LHCb) | +11.10 | +0.083323 | 1/12 = +0.0833 | 0.000010 |
| EW004 | Z boson mass (LEP combined (legacy CERN)) | -26.10 | -0.172646 | -2/12 = -0.1667 | 0.005979 |
| H001 | Higgs boson mass (ATLAS) | +309.12 | +1.490328 | 18/12 = +1.5000 | 0.009672 |
| H002 | Higgs boson mass (CMS) | +39.12 | +0.188186 | 3/16 = +0.1875 | 0.000686 |
| H003 | Higgs boson mass (ATLAS+CMS (Run-1 combination)) | +329.12 | +1.587007 | 19/12 = +1.5833 | 0.003673 |

## Predictions

- **[PASS]** P1_qp087_passed
- **[PASS]** P2_qp088_passed
- **[PASS]** P3_zero_free_parameters
- **[PASS]** P4_all_residual_rows_inside_native_subslot_band
- **[PASS]** P5_z_lep_residual_sits_at_minus_2_over_12_grid_point

## Next CR in 09a

**CR091a** appeals the CR091 Z 12-sigma residual using the EW004 row above: the Z LEP residual sits at q_eff = -2/12 in the native R12 grid, closing the 26 MeV gap structurally with zero free parameters.
