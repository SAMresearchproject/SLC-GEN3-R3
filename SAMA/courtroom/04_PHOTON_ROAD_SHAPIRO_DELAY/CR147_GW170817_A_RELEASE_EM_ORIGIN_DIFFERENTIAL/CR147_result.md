# CR147 GW170817 A-Release / EM-Origin Differential

## Verdict

```text
CR147_PASS_GW170817_DYNAMIC_A_RELEASE_ENGINE_DIFFERENTIAL_WITH_STATIC_A_INTEGRAL_BOUNDARY
```

## Tested Claim

GW170817 is read through the post-CR116 SAM picture:

```text
GW channel        = massless m=18 tensor-carrier packet
local lag         = dynamic A-release / source-engine reorganization
post-release road = shared A-road, zero GW/EM differential
```

The fresh external rerun uses the published total mass `2.74 +0.04/-0.01 M_sun`, not the older rounded `2.70 M_sun` G699c input.

## Fresh Event Inputs

```text
observed GW-to-GRB delay = 1.740000 +/- 0.050000 s
total mass               = 2.740000 +0.040000/-0.010000 M_sun
distance                 = 40.000000 Mpc
```

## Release Surface

```text
A0                         = 0.026525823848649
x_outer                    = 0.028057277031262
r_release/Rs               = 17.820688709132
A_release                  = 0.056114554063
delta_A from A=1 to release = 0.943885445937
```

## Delay Budget

```text
fresh SAM release/engine delay = 1.701457752729 s
observed delay                 = 1.740000000000 s
residual                       = 0.038542247271 s
residual sigma                 = 0.770845
absolute percent error         = 2.215072 %
mass-band prediction           = 1.695248052902 s to 1.726296552039 s
legacy 2.70 Msun prediction    = 1.676618953419 s
```

## Important Boundary

The static local A-integral version is not the seconds-scale explanation, and
exact A=1 is not a normal photon launch point:

```text
A=1 exact status                         = NO_ESCAPE_ZERO_DEPTH_BOUNDARY_NOT_LITERAL_LIGHT_LAUNCH_POINT
formal static int A dr / c across gap    = 7.774813823799e-05 s
formal light crossing across gap         = 4.540325513158e-04 s
observed / formal static A integral      = 2.237996e+04
required ln(r_release/r_origin)          = 64462.334846
required log10 ratio                     = 27995.636314
```

So the safe statement is:

```text
The m=18 tensor carrier supplies the massless GW channel. The observed
GW170817 lag is carried by dynamic A-release / local source-engine
reorganization. Once EM reaches the release surface, EM and GW share the same
A-road.
```

Do not say:

```text
A photon launches from exact A=1 and escapes normally.
The 1.74 s delay is explained by a simple static local Shapiro-style
int A dr/c across the release gap.
```

## Pass Checks

- PASS P1_sources_present: All load-bearing local and external sources are present.
- PASS P2_external_event_inputs_frozen: Fresh run uses primary external mass, delay, and distance values.
- PASS P3_CR116_massless_m18_channel: GW channel is backed by CR116 m=18 massless tensor-carrier theorem.
- PASS P4_CR006_A_integral_lane_available: Plain A-road integral lane is available for wrong-control testing.
- PASS P5_release_surface_from_A0: A0 threshold gives r_release/Rs and A_release without event fitting.
- PASS P6_fresh_mass_prediction_within_1sigma: Using published 2.74 Msun mass predicts delay within 1 sigma.
- PASS P7_mass_uncertainty_band_within_1sigma: The published mass uncertainty band remains within the observed delay window.
- PASS P8_legacy_rounding_not_required: Fresh published mass works; the pass does not depend on old rounded 2.70 Msun.
- PASS P9_A1_no_escape_boundary_preserved: A=1 is not treated as a literal photon launch point.
- PASS P10_static_A_integral_rejected: A formal static first-order (1/c) int A dr across the release gap is far too small and is not the seconds-scale mechanism.
- PASS P11_fitted_origin_radius_rejected: Forcing the formal static A integral would require an absurd origin-radius ratio.
- PASS P12_one_sided_long_road_rejected: Full 40 Mpc one-sided A-road remains many orders too large.
- PASS P13_post_release_shared_road_preserved: After release, GW and EM share the same A-road differential.
- PASS P14_no_exact_mass_fit: Exact-delay mass fit is not used and falls outside the published mass band.

## Wrong Controls

- REJECTED WC1_FULL_40MPC_ONE_SIDED_A_ROAD: Light is slowed by the full matter-sourced A-road while GW is not.
- REJECTED WC2_PLAIN_LOCAL_A_INTEGRAL_EXPLAINS_SECONDS: A simple static local Shapiro-style integral across the release gap accounts for the delay.
- REJECTED WC3_FIT_EM_ORIGIN_RADIUS_TO_FORCE_DELAY: Choose an EM origin radius so the formal static A integral equals 1.74 s.
- REJECTED WC4_M18_AS_GRAVITON_REST_MASS: The m=18 carrier is a graviton rest mass.
- REJECTED WC5_OLD_ROUNDED_MASS_IS_REQUIRED: The GW170817 pass only works with the old rounded 2.70 Msun input.
- REJECTED WC6_TUNE_MASS_TO_EXACT_DELAY: Fit the total mass to make the delay exactly 1.74 s.
- REJECTED WC7_NO_LOCAL_ENGINE_TIME: There is no local release/engine delay; only shared-road propagation remains.
- REJECTED WC8_DIFFERENT_POST_RELEASE_SPEED: After release, GW and EM propagate at meaningfully different speeds.
- REJECTED WC9_A1_AS_LITERAL_LIGHT_LAUNCH_POINT: A photon launches from exact A=1 and escapes normally.

## Load-Bearing Sources

- CR147_RUNNER [EXECUTABLE_GATE]: `C:\VS\The_Courtroom\04_PHOTON_ROAD_SHAPIRO_DELAY\CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL\CR147_runner.py`
- GW170817_GRB170817A_DELAY_PRIMARY [PRIMARY_EXTERNAL]: `https://arxiv.org/abs/1710.05834`
- GW170817_MASS_DISTANCE_PRIMARY [PRIMARY_EXTERNAL]: `https://arxiv.org/abs/1710.05832`
- GRB170817A_FERMI_GBM_PRIMARY [PRIMARY_EXTERNAL]: `https://arxiv.org/abs/1710.05446`
- CR116_M18_GRAVITON_CHANNEL [COURTROOM_THEOREM]: `C:\VS\The_Courtroom\14_FOUNDATIONAL_TESTS\CR116_18_GRAVITON_CARRIER_THEOREM\CR116_summary.json`
- CR116_RESULT_TEXT [COURTROOM_RESULT]: `C:\VS\The_Courtroom\14_FOUNDATIONAL_TESTS\CR116_18_GRAVITON_CARRIER_THEOREM\CR116_result.md`
- CR006_PHOTON_ROAD_A_INTEGRAL [COURTROOM_RESULT]: `C:\VS\The_Courtroom\04_PHOTON_ROAD_SHAPIRO_DELAY\CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT\CR006_summary.json`
- G96_BNS_ENGINE_TIME [UPSTREAM_SUMMARY]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G96_BNS_engine_time_scaling\results\G96_BNS_engine_time_scaling_summary.md`
- G699C_MULTIMESSENGER_SPLIT [UPSTREAM_SUMMARY]: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT\G699c_summary.json`
- G699C_SEALED_ENVELOPE [SEALED_ENVELOPE]: `C:\VS\Stam_model-A-v1.0\audit\audits\SEALED_ENVELOPE_G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT_2026_06_11.md`

## Falsification Handle

Future BNS + EM events with reliable launch-time interpretation should fall near the same mass-scaling law:

```text
tau_release = 0.620969982748 s/M_sun * M_total
```

## Hash

```text
CR147_gw170817_a_release_lock.json sha256 = 57a114bca6a45fbe30962983c9f6383babc721b33e20d20d683b0221cf3d8317
```
