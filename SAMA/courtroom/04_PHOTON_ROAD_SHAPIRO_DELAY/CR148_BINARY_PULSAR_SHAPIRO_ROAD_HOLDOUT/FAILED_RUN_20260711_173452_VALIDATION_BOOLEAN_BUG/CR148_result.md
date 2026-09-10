# CR148 Binary-Pulsar Shapiro Road Holdout

## Verdict

```text
PASS_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT
```

```text
scientific_result_status = PASS
sealed_utc = 2026-07-11T17:34:52Z
```

## Mandatory SAM Language v0.3 Firewall

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

```text
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
sam_language_v0_3_incidental_exposure_detected = false
forbidden_source_paths_opened = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

## Selected System

```text
system = PSR J0737-3039A/B
source = Kramer et al. 2006, Tests of general relativity from timing the double pulsar
target_readout = Shapiro shape parameter s, reported by the source table as an observed/expected comparison
```

## SAM Road Prediction

```text
A_c(r) = 2 G M_B / (c^2 r)
r_SAM = G M_B / c^3 = 6.151445643708300 microseconds
s_SAM = sin(i) = 0.999906773574375
Delta_S(E) = -2 r_SAM ln(q(E))
free_parameters_introduced = 0
```

The line-integral coefficient is `2GM_B/c^3`; in the timing convention this is
written as `2r`, so the SAM range parameter is `r = GM_B/c^3`.

## Published Shapiro Comparator

```text
comparator = Kramer2006 Table 2 Shapiro shape s observed/expected ratio
s_observed = 0.999740000000000
s_sigma = 0.000390000000000
observed_expected_ratio = 0.999870000000000
ratio_sigma = 0.000500000000000
```

Primary standardized residual:

```text
z = 0.259999999999927
abs_z = 0.259999999999927
PASS gate = abs_z <= 1.96
```

## Numerical Road Check

```text
max_abs(numerical_8192 - analytic) = 3.770677103887010e-09
max_abs(numerical_8192 - numerical_4096) = 1.131203575255313e-08
tolerance = 2.0e-8
analytic_numerical_agreement = true
```

## Wrong Controls

```text
sensitive_controls_before_reveal = 6
WC1_ENDPOINT_ONLY_SUBSTITUTION = REJECTED
WC2_WRONG_RADIAL_POWER = REJECTED
WC3_MISSING_SOURCE_RADIUS_FACTOR = REJECTED
WC4_A0_TREATED_AS_LOCAL_ROAD_SOURCE = REJECTED_ILLEGAL_TYPE_USE
WC5_NO_NEAR_SOURCE_ENHANCEMENT = REJECTED
WC6_WRONG_INCLINATION_ORIENTATION = REJECTED
WC7_FREE_AMPLITUDE_RESCUE = REJECTED_PROHIBITED_RESCUE
```

## Validation

```text
source_hashes_ok = true
target_source_hash_ok = true
precommit_sealed_before_runner = true
runner_sealed_before_target_reveal = true
target_locked_before_reveal = true
json_parse_ok = true
hashes_verified = true
existing_artifacts_modified = false
forbidden_source_paths_opened = false
firewall_fields_false = true
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

## Rule-9 Line

This test could have falsified the claim that SAM's photon-road source lift
`A(r)=2GM_c/(c^2 r)` and differential photon-road integral reproduce a
binary-pulsar Shapiro shape readout from independently locked orbital and
mass-geometry anchors with zero fitted parameters.
