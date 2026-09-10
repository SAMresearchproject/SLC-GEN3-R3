# CR006 Optical Clock Height Holdout Endpoint A-Kernel

## Canonical Identity

```text
scientific_branch = 03_CLOCKS_AND_GPS
branch_local_identifier = CR006
trailer = OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL
canonical_path = 03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL
```

## Primary Verdict

```text
PASS_OPTICAL_CLOCK_ENDPOINT_HOLDOUT
```

## Selected Experiment

```text
Bothwell et al., "Resolving the gravitational redshift across a millimetre-scale atomic sample", Nature 602, 420-424 (2022), DOI 10.1038/s41586-021-04349-7.
clock_species = 87Sr
apparatus = vertical one-dimensional optical lattice clock
```

Eligibility: primary peer-reviewed optical-clock gravitational-redshift measurement; independent millimetre geometry and local gravitational acceleration are available; the final fractional frequency gradient and uncertainty are reported; the experiment was not found in the prior active SAM exclusion list.

## Source Hashes

```text
primary_source_sha256 = 7D4376361233F17082814D99CC46CD3263C9FEBFDBF273BB9BFBE9699723E2B3
target_identity_lock_sha256 = A6CEDD37FF8130B346F83E2524E06DA2F73D7330920C5E208A69F5B30B0CD795
geometry_lock_sha256 = CD63702E222E869688A36B42C0B6AEF2F99ACE1732CEF0A26EF608B5D1A66919
precommit_sha256 = 73AE63A764F9B70EBAF865BC16EBE0A11F24C57C45571008811292AB50B8C953
runner_sha256 = 47E29CB7FD36E935DD858E7FD099C35284241DCC5EE852505F9DBB4EDA74F308
```

## Earth And Geometry Inputs

| quantity | value | unit |
|---|---:|---|
| c | 2.997924580000000000E+8 | m/s |
| mu_earth | 3.986004418000000000E+14 | m^3/s^2 |
| local g | 9.796000000000000000E+0 | m/s^2 |
| height step | 1.000000000000000000E-3 | m |
| r_lower | 6.378880989854540619E+6 | m |
| r_upper | 6.378880990854540619E+6 | m |

## SAM Prediction

| quantity | value |
|---|---:|
| r_s | 8.870056078235341431E-3 |
| A_lower | 1.390534812037245386E-9 |
| A_upper | 1.390534811819254987E-9 |
| weak_fractional_shift_per_mm | 1.089951994739255776E-19 |
| exact_fractional_shift_per_mm | 1.089951996254871970E-19 |
| exact_minus_weak | 1.515616194182489015E-28 |
| observed_upper_minus_lower_per_mm | 9.800000000000000000E-20 |
| observed_sigma_per_mm | 2.300000000000000000E-20 |
| standardized_residual_z | 4.780521370557475412E-1 |

## Wrong Controls

| control | status | prediction | z | note |
|---|---|---:|---:|---|
| WC1 | FAIL_CHANNEL_AND_MAGNITUDE | 1.326291192432461142E-2 | 5.766483276671159548E+17 | Uncanceled A0/2 local term is not an endpoint clock observable. |
| WC2 | FAIL_MATERIAL | 2.179903989478511552E-19 | 5.216973714685353567E+0 | Doubles the canonical endpoint coefficient. |
| WC3 | FAIL_MATERIAL | 3.031232384031144335E-28 | -4.260869427394587635E+0 | Force-like radial dependence erases the endpoint clock scale. |
| WC4 | FAIL_SIGN | -1.089951994739255776E-19 | -8.999791018203464510E+0 | Sign is opposite the frozen upper-minus-lower observable. |
| WC5 | FAIL_CHANNEL_UNITS | 4.638324864187361865E-21 | n/a | A road time integral in seconds is not a fractional endpoint clock shift. |
| WC6 | FAIL_FREE_PARAMETER | 9.800000000000000000E-20 | 0.000000000000000000E+18 | Would require fitted k = 0.89912216751751613761569454109049465778776664079315258129288386756155850185527242. |
| WC7 | DIAGNOSTIC_LIMIT_MATCH | 1.089951994910124616E-19 | 4.780521377986555191E-1 | Near-surface limit agrees and does not replace the radial A-kernel route. |

## Free Parameters

```text
free_parameters_introduced = 0
```

## External Anchors And Comparators

```text
external_anchors = c, mu_earth, local g, height step
external_comparators = final reported fractional frequency gradient, reported total uncertainty
```

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

## Rule-9 Falsification Sentence

This test would falsify the scoped SAM endpoint-clock claim if the frozen no-fit A-kernel prediction disagreed with the independently selected optical-clock measurement beyond the precommitted tolerance, returned the wrong sign, required a local A0 contribution, or required a fitted normalization.

## Scope Statement

This is a weak-field recovery test and internal/external consistency check of the SAM endpoint clock channel. It is not, by itself, a unique discriminator against general relativity in the weak field.
