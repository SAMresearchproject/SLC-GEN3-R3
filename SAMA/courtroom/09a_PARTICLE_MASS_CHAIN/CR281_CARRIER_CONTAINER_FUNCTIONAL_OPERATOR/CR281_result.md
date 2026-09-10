# CR281 Carrier/Container Functional Operator -- Result

```text
scientific_verdict = PASS
execution_status = CLEAN
precommit_sha256 = a31ed176acf9ec2272873c64c64e29c24f387ada879c7aa3e4f5d1923e5f50f3
free_parameters_introduced = 0
external_observational_inputs_used = false
isotope_stability_used_as_operator_input = false
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
```

## Core Rule

`F_cc(A)` classifies each source-supported atom from exact address `A=h^a*d^b`, mirror seating, bow release, and ledger closure:

```text
TERMINAL_CLOSURE iff A = L = h*d^4 = R^2*d^2/S = 162.
FIXED_POINT iff (a,b)=(2,1) or a=0 and b>=3.
OUTPUT iff a=1 and 1<=b<=3, or (a,b)=(0,2).
OUT_OF_TARGET_DOMAIN otherwise.
```

This uses no isotope stability, half-life, abundance, decay mode, or observed-stability field.

## Exact Constants

```json
{
  "L": 162,
  "L_equals_R_sq_d_sq_over_S": true,
  "M": 126,
  "M_retained_fraction": "7/8",
  "R": 12,
  "R_sq": 144,
  "S": 8,
  "Theta": 18,
  "Theta_lift_fee": "81/4",
  "Theta_release_fraction": "1/8",
  "d": 3,
  "h": 2
}
```

## Target Roles

| atom | value | address | actual | expected | match |
|---|---:|---|---|---|---|
| m_3 | 6 | (1,1) | OUTPUT | OUTPUT | True |
| D^2 | 9 | (0,2) | OUTPUT | OUTPUT | True |
| Theta | 18 | (1,2) | OUTPUT | OUTPUT | True |
| hV | 54 | (1,3) | OUTPUT | OUTPUT | True |
| R | 12 | (2,1) | FIXED_POINT | FIXED_POINT | True |
| V | 27 | (0,3) | FIXED_POINT | FIXED_POINT | True |
| F | 81 | (0,4) | FIXED_POINT | FIXED_POINT | True |
| L | 162 | (1,4) | TERMINAL_CLOSURE | TERMINAL_CLOSURE | True |

## No-Lift / No-Fee Status of 18

Theta = 18 = h*d^2 = R^2/S is the single released bow quantum. Its retained-lift fee would be 18*(1+18/144)=81/4=20.25, which is not a seated target row; CR233 gives M_rest(Theta)=18-18=0. The operator therefore returns OUTPUT, not FIXED_POINT, because Theta is released traffic rather than boundary-seated local matter.

## Held-Out Structural Classifications

| item | value | actual | expected | match |
|---|---:|---|---|---|
| M | 126 | RETAINED_SCRATCH | RETAINED_SCRATCH | True |
| R^2 | 144 | DOMAIN_TOTAL | DOMAIN_TOTAL | True |
| S | 8 | DOMAIN_MULTIPLICITY | DOMAIN_MULTIPLICITY | True |
| h^4 | 16 | OUT_OF_SOURCE_ATOM_SET | OUT_OF_SOURCE_ATOM_SET | True |

## Wrong Controls

| control | broke | best/matches |
|---|---:|---|
| WC1_RAW_NUMERIC_ORDERING | True | not_applicable_monotone_sequence_test |
| WC2_PARITY_ONLY | True | 5 |
| WC3_PURE_POWER_VS_MIXED_POWER_ONLY | True | 5 |
| WC4_UNRESTRICTED_GRADE_PROMOTES_16 | True | n/a |
| WC5_SWAPPED_PRIMITIVE_ADDRESSES | True | 1 |
| WC6_INVERT_OUTPUT_FIXED_LABELS | True | 1 |

## Source Quality and Boundary Notes

- CR262 display-cell inconsistencies are preserved; the runner does not use isotope stability as an operator input.
- CR270 remains BOUNDARY-grade mechanism support. CR281 passes as a functional classification operator, not as a full dynamical derivation of all nuclear behavior.
- A broad source-location command printed language-tree path/snippet hits before precommit; those hits were quarantined and are not inputs or evidence.

## Validation

```text
source_hashes_ok = True
forbidden_source_paths_opened = False
target_roles_all_match = True
wrong_controls_broke_count = 6
heldout_match_count = 4
firewall_fields_false = True
queue_maintenance_performed_by_research_agent = false
```
