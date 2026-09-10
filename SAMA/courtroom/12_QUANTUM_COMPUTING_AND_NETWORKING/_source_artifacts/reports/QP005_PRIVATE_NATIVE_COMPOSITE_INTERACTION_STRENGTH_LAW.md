# QP005 - Private Native Composite Interaction Strength Law

Location: `D:\quantum_phase`

## Verdict

`QP005_PRIVATE_NATIVE_COMPOSITE_INTERACTION_STRENGTH_LAW_BUILT`

QP005 turns the QP004 role-operator bridge into a dimensionless native
interaction-strength coordinate.

```text
native_interaction_strength = phase_role_strength * 4*m_a*m_b/(m_a+m_b)^2
```

The pair-balance term is the no-parameter symmetric closure coordinate. It is
equal to `1 - mass_asymmetry^2`, so it measures how well two transported
response packets can close together rather than how heavy the pair is.

## Main Read

The strongest private heavy-composite closure in the SUK055 target set is
`b<->c` with native strength
`0.717139946489`.

## Ranked Strength Table

| Rank | Pair | Phase role operator | Native strength | Closure class |
| ---: | --- | --- | ---: | --- |
| 1 | b<->c | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | 0.717139946489 | WRITE_MIDPOINT_BALANCED_CLOSURE |
| 2 | c<->s | TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | 0.252472987837 | A_SHARE_SCALE_ASYMMETRIC_CLOSURE |
| 3 | b<->t | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | 0.0923016101689 | A_SHARE_SCALE_ASYMMETRIC_CLOSURE |
| 4 | b<->s | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | 0.0849597126971 | A_SHARE_SCALE_ASYMMETRIC_CLOSURE |
| 5 | c<->t | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | 0.0291578696086 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |
| 6 | c<->d | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | 0.0144409361727 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |
| 7 | c<->u | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | 0.00669113159829 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |
| 8 | b<->d | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | 0.00443564972461 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |
| 9 | s<->t | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | 0.00214652742778 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |
| 10 | b<->u | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | 0.0020496727624 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |
| 11 | d<->t | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | 0.000107602567305 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |
| 12 | t<->u | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | 4.96641640597e-05 | SUB_A_SHARE_ASYMMETRIC_CLOSURE |

## Counts

```text
rows = 12
closure class counts = {'WRITE_MIDPOINT_BALANCED_CLOSURE': 1, 'A_SHARE_SCALE_ASYMMETRIC_CLOSURE': 3, 'SUB_A_SHARE_ASYMMETRIC_CLOSURE': 8}
role operator counts = {'DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR': 6, 'TRANSITION_COLOR_COUPLED_ROLE_OPERATOR': 1, 'NEUTRAL_BINARY_MIXING_ROLE_OPERATOR': 5}
max balance identity abs residual = 2.22044604925e-16
```

## Next Frontier

`QP006_PRIVATE_HEAVY_COMPOSITE_SLOT_PRIORITY_TABLE`

QP006 should turn this into a private blank-slot priority table before any
external observed-mass comparison.

Generated at UTC: `2026-06-07T02:34:51.872450+00:00`
