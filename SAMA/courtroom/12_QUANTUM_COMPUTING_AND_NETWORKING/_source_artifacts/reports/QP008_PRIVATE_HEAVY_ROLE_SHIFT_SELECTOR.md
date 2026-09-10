# QP008 - Private Heavy Role Shift Selector

Location: `D:\quantum_phase`

## Verdict

`QP008_PRIVATE_HEAVY_ROLE_SHIFT_SELECTOR_BUILT`

QP008 selects the A-share contact surface for each P1/P2 phase-role class and
emits the nearest native integer-shift mass readout. It does not use observed
composite masses.

## Main Read

Selected rows: `4`

Selected pairs:

```text
b<->c, b<->s, b<->t, c<->s
```

## Selected Readouts

| Rank | Pair | Selected surface | Seed role | Shift | Selected mass MeV |
| ---: | --- | --- | --- | ---: | ---: |
| 1 | b<->c | INTERACTION_COORDINATE_SURFACE | charged_kaon_D_b_square | 1 | 3950.10153486 |
| 2 | b<->s | CLOSURE_COMPLEMENT_SURFACE | neutral_kaon_color_complement | -4 | 3978.71874985 |
| 3 | b<->t | INTERACTION_COORDINATE_SURFACE | charged_kaon_D_b_square | -1 | 15800.4061394 |
| 4 | c<->s | CLOSURE_COMPLEMENT_SURFACE | charged_kaon_D_b_square | 3 | 987.525383715 |

## Counts

```text
candidate trials read = 12
selected rows = 4
role counts = {'DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR': 2, 'NEUTRAL_BINARY_MIXING_ROLE_OPERATOR': 1, 'TRANSITION_COLOR_COUPLED_ROLE_OPERATOR': 1}
selected integer shift counts = {'1': 1, '-4': 1, '-1': 1, '3': 1}
```

## Next Frontier

`QP009_PRIVATE_HEAVY_COMPOSITE_EXTERNAL_COMPARISON_SEALED_OPTION`

At this point there are two clean options: seal the private prediction table,
or run an external comparison only on the secure machine.

Generated at UTC: `2026-06-07T02:41:37.659854+00:00`
