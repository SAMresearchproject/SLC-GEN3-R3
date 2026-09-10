# QP014 - Private Born Rule Route-Weight Bridge

## Verdict

`QP014_PRIVATE_BORN_RULE_ROUTE_WEIGHT_BRIDGE_BUILT`

QP014 builds the first private SAM Born-style route bridge:

```text
latent_weight_i = route_capacity_prior_i * coherence_survival_i
write_weight_i = latent_weight_i * write_access_i
P_i = weight_i / sum(weight_all)
```

The probability surface exists before the final ledger outcome. Resolution does
not create the route weights; it selects which weighted surface becomes
ledger-visible.

## Main Read

```text
route priors = 7
route weight rows = 49
probability surfaces = 7
normalization failures = 0
free parameters introduced = 0
top route prior = QUBIT-NL-001 at 0.9641871075120799
```

## Route-Capacity Priors

| Rank | Qubit | Exposure Family | route capacity prior | max letter lead |
| ---: | --- | --- | ---: | ---: |
| 1 | QUBIT-NL-001 | WEAK_CONTACT_LIMITED | 0.964187107512 | 2019873.91168 |
| 2 | QUBIT-UNK-001 | PARTITION_OCCUPANCY_COUPLED | 0.025575392683 | 53577.8461036 |
| 3 | QUBIT-CL-001 | EM_CONTACT_LIMITED | 0.00896361662886 | 18777.865045 |
| 4 | QUBIT-BN-001 | WEAK_CONTACT_LIMITED | 0.000677943673128 | 1420.22303376 |
| 5 | QUBIT-TM-001 | EM_CONTACT_LIMITED | 0.000392007575228 | 821.215994504 |
| 6 | QUBIT-TP-001 | EM_CONTACT_LIMITED | 0.000202635018001 | 424.499750375 |
| 7 | QUBIT-COLOR-001 | SUPPORT_COUPLED | 1.29690974136e-06 | 2.71689398455 |

## Probability Surfaces

| Sample | open routes | top controlled route | top controlled P | P sum |
| --- | ---: | --- | ---: | ---: |
| ONE_T_SW | 7 | QUBIT-NL-001 | 0.151871184026 | 1 |
| QUARTER_A_SIDE | 7 | QUBIT-NL-001 | 0.964187107512 | 1 |
| HALF_A_SIDE | 7 | QUBIT-NL-001 | 0.964187107512 | 1 |
| A_SIDE_BOUNDARY | 7 | QUBIT-NL-001 | 0.964187107512 | 1 |
| MID_A_SIDE_TO_A_SHARE | 7 | QUBIT-NL-001 | 0.964187107512 | 1 |
| A_SHARE_BOUNDARY | 0 | QUBIT-NL-001 | 0 | 0 |
| WRITE_MIDPOINT | 0 | QUBIT-NL-001 | 0 | 0 |

## Meaning

The SAM reading is compact:

```text
probability = normalized unresolved route strength
```

There are three useful surfaces:

```text
latent surface     = which routes remain coherently available
write surface      = which available routes are close to write access
controlled surface = the write surface after QP013 A-contact suppression
```

The QP013 contact letter changes the probability surface by preserving route
coherence before the logical route identity is written.

## Outputs

```text
qp014_route_capacity_prior_table.csv
qp014_route_weight_table.csv
qp014_probability_surface_table.csv
qp014_born_bridge_schema.csv
qp014_summary.json
qp014_next_frontier.csv
```

## Next Frontier

`QP015_PRIVATE_INTERFERENCE_TO_LEDGER_COMMIT_BRIDGE`

QP015 should use QP014's route weights with QP003's interference/bounce table
to ask how two unresolved weighted routes become one committed ledger
intersection.

Generated at UTC: `2026-06-07T16:03:27.319665+00:00`
