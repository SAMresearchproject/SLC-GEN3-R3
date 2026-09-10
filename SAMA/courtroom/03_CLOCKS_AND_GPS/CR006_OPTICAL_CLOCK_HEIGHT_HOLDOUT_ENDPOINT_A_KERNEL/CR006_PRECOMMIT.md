# CR006 Precommit: Optical Clock Height Holdout Endpoint A-Kernel

## Test ID

```text
CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL
```

## Branch

```text
03_CLOCKS_AND_GPS
```

## Test Type

```text
new_scientific_courtroom_record = true
is_audit_or_retest = false
language_test = false
forecast = false
queue_maintenance = false
```

## Target Locked Before Runner

```text
target_identity_lock = CR006_TARGET_IDENTITY_LOCK.json
geometry_lock = CR006_GEOMETRY_LOCK.json
selected_experiment = Bothwell et al. 2022 Nature optical-lattice clock millimetre-scale gravitational redshift
doi = 10.1038/s41586-021-04349-7
```

The external measured frequency gradient remains an `EXTERNAL_COMPARATOR`; it is not a calculation input for the SAM prediction.

## Canonical Calculations

Frozen formulas:

```text
rs = 2*mu_earth/c^2
A_lower = rs/r_lower
A_upper = rs/r_upper
weak_fractional_shift = (A_lower - A_upper)/2
exact_fractional_shift = sqrt((1-A_upper)/(1-A_lower)) - 1
```

Frozen geometry:

```text
c = 299792458 m/s
mu_earth = 3.986004418e14 m^3/s^2
a_local = 9.796 m/s^2
h = 0.001 m
r_lower = sqrt(mu_earth/a_local)
r_upper = r_lower + h
```

Frozen numerical prediction before measurement reveal:

```text
r_lower_m = 6378880.9898545406187519554583598443269674966815389824964319143784
r_upper_m = 6378880.9908545406187519554583598443269674966815389824964319143784
rs_m = 0.0088700560782353414310643118900272650501115344117909910700123652433993701792508065
A_lower = 1.3905348120372453859539893254694029002433348013274734942967558377530683594947568e-9
A_upper = 1.3905348118192549870061381702223276637552377655168256062899286477014232479335079e-9
weak_fractional_shift_per_mm = 1.0899519947392557762353761824404851790532394400341359502582255578062445e-19
exact_fractional_shift_per_mm = 1.089951996254871970417865197056993179381484296259050233221356e-19
exact_minus_weak_per_mm = 1.5156161941824890146165080003282448562249142829631304421937555e-28
```

## A0 Rule

The common floor is canceled before the endpoint observable is formed:

```text
A0 is not inserted as a local redshift term.
Any common A0 contribution cancels before Delta_nu/nu is calculated.
```

## External Anchors And Comparator Classification

```text
c                                      EXTERNAL_DIMENSIONAL_ANCHOR
mu_earth                               EXTERNAL_DIMENSIONAL_ANCHOR
a_local                                EXTERNAL_GEOMETRY_INPUT
h = 1 mm                               EXTERNAL_GEOMETRY_INPUT
final measured frequency gradient       EXTERNAL_COMPARATOR
reported total uncertainty              EXTERNAL_COMPARATOR
```

## Free Parameters

```text
free_parameters_introduced = 0
```

## Primary Scoring

After measurement reveal:

```text
z = (Delta_SAM - Delta_obs)/sqrt(sigma_obs^2 + sigma_input^2)
```

The acceleration rounding contribution is negligible relative to the reported measurement uncertainty and is included only as a transparent input-sigma term.

Precommitted gate:

```text
PASS: |z| <= 2 and WC1-WC6 fail materially by magnitude or channel rule; WC7 is diagnostic only.
FAIL: |z| > 3, or canonical sign/channel is wrong, or local A0/fitted normalization is required.
BOUNDARY: 2 < |z| <= 3, or public geometry is insufficient for a clean independent calculation.
```

## Exact Versus Weak Consistency

```text
max_allowed_abs_exact_minus_weak = 1e-26
```

This is an internal consistency gate only.

## Required Wrong Controls

```text
WC1 add the floor locally:
  wrong = weak_fractional_shift + A0/2
  break = uncanceled A0 local term is channel-invalid and grossly wrong in magnitude.

WC2 remove the half factor:
  wrong = A_lower - A_upper
  break = wrong coefficient must fail materially.

WC3 use 1/r^2 as the clock field:
  wrong = (A_lower^2 - A_upper^2)/2
  break = wrong field dependence must fail materially.

WC4 reverse endpoint order:
  wrong = (A_upper - A_lower)/2
  break = sign must reverse incorrectly relative to the frozen observable.

WC5 use photon-road integration:
  wrong = (1/c)*integral A ds approximated as A_lower*h/c
  break = road time integral has wrong channel/units for endpoint clock fraction.

WC6 free clock normalization:
  wrong = k*weak, with k fitted to observed after reveal
  break = rejected as one fitted free parameter even if it matches.

WC7 Newtonian near-surface approximation only:
  diagnostic = a_local*h/c^2
  break = not a wrong-physics failure; it must agree as the near-surface limit and must not replace the canonical A-kernel route.
```

## Permitted Verdicts

```text
PASS_OPTICAL_CLOCK_ENDPOINT_HOLDOUT
BOUNDARY_PUBLIC_GEOMETRY_OR_UNCERTAINTY
FAIL_OPTICAL_CLOCK_ENDPOINT_HOLDOUT
INVALID_SOURCE_OR_TARGET_REUSE
INVALID_FIREWALL_EXPOSURE
```

## Rule-9 Falsification Sentence

This test would falsify the scoped SAM endpoint-clock claim if the frozen no-fit A-kernel prediction disagreed with the independently selected optical-clock measurement beyond the precommitted tolerance, returned the wrong sign, required a local A0 contribution, or required a fitted normalization.

## Weak-Field Scope Statement

This is a weak-field recovery test and internal/external consistency check of the SAM endpoint clock channel. It is not, by itself, a unique discriminator against general relativity in the weak field.

## Firewall

```text
Do not inspect SAM_LANGUAGE_V0_3, its registered contracts,
candidate implementation, or expected language output while developing this CR.

Set:
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false

Record both fields in the CR precommit, provenance, summary, and result
artifacts. If either field becomes true in any of those artifacts, the CR
remains scientifically valid but is ineligible as a SAM Language v0.3 holdout.

This firewall is between new scientific work and the frozen executable
language, not between the new work and SAM itself. The research may still use
the full scientific repository, previous Courtroom records, conceptual volumes,
external data, and normal SAM methods.
```

```json
{
  "sam_language_v0_3_consulted_during_development": false,
  "sam_language_v0_3_candidate_hash_known_to_research_agent": false,
  "sam_language_v0_3_incidental_exposure_detected": false
}
```

