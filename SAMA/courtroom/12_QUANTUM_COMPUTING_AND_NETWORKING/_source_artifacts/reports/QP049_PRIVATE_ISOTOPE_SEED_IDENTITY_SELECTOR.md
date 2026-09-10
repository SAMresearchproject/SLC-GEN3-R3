# QP049 - Private Isotope Seed Identity Selector

## Preflight

```text
test_id = QP049
test_name = PRIVATE_ISOTOPE_SEED_IDENTITY_SELECTOR
test_type = FORWARD_MODEL_BUILD
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
if_audit_or_retest_reason = NOT_APPLICABLE
permission_required_before_run = false
public_repo_write = false
external_data_used = false
free_parameters_introduced = 0
```

## Result

```text
QP049_ISOTOPE_SEED_IDENTITY_SELECTED_ALL_ELEMENTS
```

QP049 selects a seed identity for the isotope layer before attempting isotope
mass/readout:

```text
Z = 1      -> proton/deuteron seed
Z = 2      -> alpha closure seed
even Z > 2 -> alpha-stack seed
odd Z > 1  -> alpha-stack plus one residual charge lane
```

## Seed Family Summary

| seed family | rows | alpha units | residual values |
| --- | ---: | --- | --- |
| EVEN_Z_ALPHA_STACK_SEED | 58 | 2..59 | 0 |
| HELIUM_ALPHA_CLOSURE_SEED | 1 | 1..1 | 0 |
| HYDROGEN_PROTON_DEUTERON_SEED | 1 | 0..0 | 1 |
| ODD_Z_ALPHA_STACK_PLUS_RESIDUAL_SEED | 58 | 1..58 | 1 |

## Radix Cycle Summary

| radix cycle | Z range | rows | alpha units | odd residual rows |
| ---: | --- | ---: | --- | ---: |
| 1 | 1..12 | 12 | 0..6 | 6 |
| 2 | 13..24 | 12 | 6..12 | 6 |
| 3 | 25..36 | 12 | 12..18 | 6 |
| 4 | 37..48 | 12 | 18..24 | 6 |
| 5 | 49..60 | 12 | 24..30 | 6 |
| 6 | 61..72 | 12 | 30..36 | 6 |
| 7 | 73..84 | 12 | 36..42 | 6 |
| 8 | 85..96 | 12 | 42..48 | 6 |
| 9 | 97..108 | 12 | 48..54 | 6 |
| 10 | 109..118 | 10 | 54..59 | 5 |

## Bridge Usage

| bridge | symbol | constituents | QP049 usage |
| --- | --- | --- | --- |
| proton_neutron | p/n | p;n | base nucleon seed pair |
| deuteron | D | proton;neutron | hydrogen isotope residual bridge |
| alpha_particle | alpha | proton;proton;neutron;neutron | alpha-stack seed unit |

## Key Fields

```text
element_rows = 118
seed_identity_rows = 118
seed_family_count = 4
radix_cycles = 10
mass_readout_rows_emitted = 0
observed_isotope_masses_used = false
free_parameters_introduced = 0
next_frontier = QP050_PRIVATE_SYMMETRIC_ISOTOPE_SEED_MASS_READOUT
```

## Interpretation

This is a real compression step. The isotope table no longer starts from 118
unstructured blanks. Every element now has a SAM-native seed identity built from
the proton/neutron, deuteron, and alpha bridges. The remaining missing selector
is narrower:

```text
seed identity + A-road band -> symmetric seed mass -> neutron-excess / binding-depth readout
```
