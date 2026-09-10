# CR148 Precommit - Binary Pulsar Shapiro Road Holdout

Precommit sealed UTC: 2026-07-11T17:28:47Z

## Test Identity

```text
top-level branch: 04_PHOTON_ROAD_SHAPIRO_DELAY
branch-local CR: CR148
unique trailer: BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT
full CR key: 04_PHOTON_ROAD_SHAPIRO_DELAY / CR148 / BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT
research model requested: GPT-5.5 Extra High
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
```

## Scientific Question

Does the source-derived SAM photon-road readout

```text
A(r) = r_s/r = 2GM_c/(c^2 r)
Delta t_A(phi) = (1/c) [ integral_Gamma(phi) A ds - integral_Gamma(ref) A ds ]
```

reproduce the orbital-phase-dependent Shapiro delay of PSR J0737-3039A/B with
zero fitted SAM parameters?

The target is the variable road delay produced by the companion B accumulation
field for pulses from pulsar A.

## Selected System

```text
selected_system = PSR J0737-3039A/B
source_paper = Kramer et al., Tests of general relativity from timing the double pulsar
source_data_version = arXiv astro-ph/0609417 v1 source package with Science 314:97-102 journal reference
target_readout_type = Shapiro shape parameter s = sin(i), plus reported SAM range coefficient r = GM_B/c^3
free_parameters_allowed = 0
```

Branch 04 prior-use exclusion was checked only against existing Branch 04 CR006
and CR147 files. No selected-system hit was found.

## External Anchors

Locked in `BINARY_PULSAR_INPUTS_LOCKED.json` before target reveal:

```text
P_b = 0.10225156248 day
e = 0.0877775
x_A = 1.415032 light-second
x_B = 1.5161 light-second
omega_A = 87.0331 deg
T_0 = 53155.9074280 MJD
dot_omega_A = 16.89947 deg/yr
mass_function_A = 0.29096571 M_sun
mass_function_B = 0.3579 M_sun
mass_ratio R = m_A/m_B = 1.0714
M_total = 2.58708 M_sun
m_A = 1.3381 M_sun
m_B = 1.2489 M_sun
T_sun = GM_sun/c^3 = 4.925490947 microseconds
```

Input roles are recorded as `EXTERNAL_DIMENSIONAL_ANCHOR`,
`EXTERNAL_GEOMETRY_ANCHOR`, `DERIVATION_INPUT`, or
`OBSERVATIONAL_COMPARATOR_WITHHELD` in the lock file.

## Withheld Comparator Fields

```text
shapiro_shape_s_observed
shapiro_shape_observed_over_expected_ratio
published_uncertainty_for_primary_shape_comparator
```

These fields must be opened only after this precommit and the runner are sealed.

## Canonical Equations

```text
A_c(r) = 2 G M_c / (c^2 r)
T_A = (1/c) integral A_c(r) ds
T_sun = G M_sun / c^3
r_SAM = T_sun * m_B
f_A = 4 pi^2 x_A^3 / (T_sun P_b^2)
s_SAM = [ f_A M_total^2 / m_B^3 ]^(1/3)
q(E) = 1 - e cos(E) - s [ sin(omega)(cos(E)-e) + sqrt(1-e^2) cos(omega) sin(E) ]
Delta_S(E) = -2 r_SAM ln(q(E))
Delta t_A(E) = Delta_S(E) - Delta_S(E_ref)
E_ref = 0
```

The coefficient `2GM_c/c^3` from the SAM line integral is the source timing
convention coefficient `2r`; therefore `r_SAM = GM_c/c^3`.

## Locked Pre-Reveal SAM Readout

```text
P_b_seconds = 8834.534998272
mass_function_A_from_xA_Pb_Tsun = 0.290965571533945
s_SAM_from_published_mass_function_A_M_total_mB = 0.999906773574375
s_SAM_from_xA_Pb_M_total_mB = 0.999906614960991
r_SAM = 6.1514456437083 microseconds
delay_curve_peak_to_peak_before_baseline_subtraction = 123.083708040909 microseconds
```

Primary prediction uses the source table mass function for the comparator:

```text
s_SAM = 0.999906773574375
r_SAM = 6.1514456437083 microseconds
```

## Integration Geometry

Use the Damour-Deruelle eccentric-binary Shapiro convention derived from the
point-source photon-road integral. The direct numerical road check integrates
the source field along the observer ray and compares the reference-subtracted
dimensionless integral to `ln(q_ref/q)`.

Numerical agreement tolerance:

```text
max |numerical_integral_difference - analytic_log_difference| <= 2e-8
```

## Baseline Convention

The additive timing constant is removed exactly once by subtracting the
precommitted reference phase:

```text
E_ref = 0
Delta t_A(E) = Delta_S(E) - Delta_S(E_ref)
```

No post-reveal fitted baseline is allowed.

## Exact Output Fields

```text
selected_system
source_paper
source_hashes_ok
target_source_hash_ok
s_SAM
r_SAM_microseconds
primary_comparator_name
primary_observed_value
primary_observed_sigma
primary_standardized_residual_z
primary_verdict
scientific_result_status
sealed_utc
free_parameters_introduced
wrong_controls_sensitive_count
target_locked_before_reveal
precommit_sealed_before_runner
runner_sealed_before_target_reveal
hashes_verified
firewall_fields
```

## Grading Rule

Use the independent-uncertainty gate. If the source table gives an
observed-to-expected Shapiro-shape ratio, the canonical SAM ratio is 1 and

```text
z = (1 - ratio_obs) / sigma_ratio
PASS iff |z| <= 1.96
```

If the ratio is unavailable, compare the source's observed Shapiro shape:

```text
z = (s_SAM - s_obs) / sigma_s
PASS iff |z| <= 1.96
```

If the selected source does not provide enough public uncertainty information,
return:

```text
BOUNDARY_PUBLIC_GEOMETRY_OR_COVARIANCE_INSUFFICIENT
```

## PASS Conditions

```text
source_hashes_ok = true
target_source_hash_ok = true
precommit_sealed_before_runner = true
runner_sealed_before_target_reveal = true
target_locked_before_reveal = true
free_parameters_introduced = 0
canonical prediction uses A(r)=2GM_c/(c^2 r)
primary |z| <= 1.96
at least four wrong controls sensitive
json_parse_ok = true
hashes_verified = true
existing_artifacts_modified = false
forbidden_source_paths_opened = false
firewall_fields_false = true
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

Primary PASS verdict:

```text
PASS_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT
```

## FAIL Conditions

```text
source and target hashes are valid
all seal/reveal order checks pass
free parameters introduced = 0
wrong controls sensitivity gate passes
primary |z| > 1.96
```

Primary FAIL verdict:

```text
FAIL_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT
```

## BOUNDARY Conditions

```text
BOUNDARY_INDEPENDENT_INPUTS_INSUFFICIENT
BOUNDARY_PUBLIC_GEOMETRY_OR_COVARIANCE_INSUFFICIENT
BOUNDARY_CONTROL_SENSITIVITY_INSUFFICIENT
```

## Invalid Conditions

```text
INVALID_SOURCE_CHAIN
INVALID_TARGET_REVEAL_ORDER
INVALID_FIREWALL
```

Invalid records do not receive an allowed `scientific_result_status`.

## Wrong Controls

Precommitted controls, all run from the same locked inputs:

```text
WC1_ENDPOINT_ONLY_SUBSTITUTION
WC2_WRONG_RADIAL_POWER
WC3_MISSING_SOURCE_RADIUS_FACTOR
WC4_A0_TREATED_AS_LOCAL_ROAD_SOURCE
WC5_NO_NEAR_SOURCE_ENHANCEMENT
WC6_WRONG_INCLINATION_ORIENTATION
WC7_FREE_AMPLITUDE_RESCUE
```

Pre-reveal sensitivity gate:

```text
WC1 sensitive: endpoint field substitution loses the logarithmic orbital shape
WC2 sensitive: 1/r^2 integrand loses DD logarithmic conjunction morphology
WC3 sensitive: coefficient is half amplitude, delta ratio 0.5
WC4 sensitive: A0 as a local source creates an illegal path-length term
WC5 sensitive: constant mean field has zero conjunction logarithmic shape
WC6 sensitive: complementary inclination gives s = 0.0136544556860983
WC7 sensitive as prohibition: any post-reveal amplitude fit is disallowed
sensitive_controls_before_reveal = 6 plus 1 prohibited-rescue control
```

The control definitions must not change after target reveal.

## Forbidden Files

Do not inspect, search, list, hash, summarize, or open paths matching:

```text
SAM_LANGUAGE*
*V0_3_GENERALIZATION*
*PROSPECTIVE_HOLDOUT*
*FORECAST_GATE*
*LANGUAGE_CONTRACT*
```

Do not run repository-root recursive searches. Do not run queue maintenance.
Do not generate a forecast.

## Rule 9 Falsification Sentence

This test could falsify the claim that SAM's photon-road source lift
`A(r)=2GM_c/(c^2 r)` and differential photon-road integral reproduce a
binary-pulsar Shapiro shape readout from independently locked orbital and
mass-geometry anchors with zero fitted parameters.

