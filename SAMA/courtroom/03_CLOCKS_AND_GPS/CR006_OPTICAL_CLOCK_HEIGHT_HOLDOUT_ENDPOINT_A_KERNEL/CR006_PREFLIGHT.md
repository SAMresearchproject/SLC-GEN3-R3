# CR006 Preflight: Optical Clock Height Holdout Endpoint A-Kernel

## CR Identity

```text
scientific_branch = 03_CLOCKS_AND_GPS
branch_local_identifier = CR006
trailer = OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL
canonical_path = 03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL
bare_cr_number_global_uniqueness_required = false
destination_existed_before_creation = false
```

## Scientific Question

Can the SAM endpoint clock readout from:

```text
A(r) = r_s/r = 2GM/(c^2 r)
```

recover an independent optical-clock gravitational-redshift height measurement with A0 canceled as a common floor, no fitted normalization, and all mandatory wrong controls rejected?

## Source Authority

Internal authority is the active A-kernel and clock/GPS Courtroom chain:

```text
02_A_KERNEL_WEAK_FIELD
03_CLOCKS_AND_GPS
A0-a_h-D
```

External authority is the selected primary peer-reviewed paper:

```text
Bothwell et al., "Resolving the gravitational redshift across a millimetre-scale atomic sample", Nature 602, 420-424 (2022), DOI 10.1038/s41586-021-04349-7.
```

## Selected External Experiment

```text
clock_species = 87Sr
apparatus = vertical one-dimensional optical lattice clock
observable = fractional frequency gradient across a millimetre-scale atomic sample
primary_comparator = final corrected frequency gradient, revealed after target and geometry locks
```

The canonical CR006 observable is:

```text
Delta_nu/nu = upper clock minus lower clock per 1 mm upward separation
```

## Output Type

```text
new_scientific_courtroom_record = true
language_test = false
forecast = false
queue_maintenance = false
```

## Units

All dimensional calculations use SI units. Fractional frequency shifts are dimensionless per 1 mm height step.

## Free Parameters

```text
free_parameters_introduced = 0
```

The local gravitational acceleration and height scale are external geometry inputs, not SAM fit parameters.

## External Anchors

```text
c
Earth gravitational parameter mu = GM
local laboratory gravitational acceleration from the selected paper
height step = 1 mm
```

## External Comparator

The selected paper's final corrected fractional frequency gradient with total uncertainty is the external comparator. It is not a derivation input.

## Forbidden Inputs

No SAM Language v0.3 candidate, contract, forecast gate, prospective queue maintenance artifact, or frozen executable language artifact is an input to this CR.

## Wrong Controls

Mandatory wrong controls:

```text
WC1 add the floor locally
WC2 remove the half factor
WC3 use 1/r^2 as the clock field
WC4 reverse endpoint order
WC5 use photon-road integration
WC6 free clock normalization
WC7 Newtonian near-surface approximation diagnostic
```

## Permitted Verdicts

```text
PASS_OPTICAL_CLOCK_ENDPOINT_HOLDOUT
BOUNDARY_PUBLIC_GEOMETRY_OR_UNCERTAINTY
FAIL_OPTICAL_CLOCK_ENDPOINT_HOLDOUT
INVALID_SOURCE_OR_TARGET_REUSE
INVALID_FIREWALL_EXPOSURE
```

## Rule-9 Falsification Condition

This test would falsify the scoped SAM endpoint-clock claim if the frozen no-fit A-kernel prediction disagreed with the independently selected optical-clock measurement beyond the precommitted tolerance, returned the wrong sign, required a local A0 contribution, or required a fitted normalization.

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

