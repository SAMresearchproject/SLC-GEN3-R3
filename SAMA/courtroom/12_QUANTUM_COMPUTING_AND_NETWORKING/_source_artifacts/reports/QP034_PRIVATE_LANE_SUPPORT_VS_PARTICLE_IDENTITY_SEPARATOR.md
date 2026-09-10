# QP034 - Private Lane Support vs Particle Identity Separator

## Result

```text
QP034_LANE_SUPPORT_PARTICLE_IDENTITY_SEPARATED
```

QP034 separates collective lane support from localized particle identity.

## Separation Table

| lane | lane closure fraction | best slot | best slot score | best slot delta in ultra units | fixed point slots | class |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| DERIVED_STABLE_ANCHOR_LANE | 0.9999993719460315 | c<->t | 0.9880873618629215 | 13877.028207745512 | 0 | LANE_SUPPORTED_IDENTITY_HELD_OPEN_STRONG_SLOT |
| DERIVED_CHARGED_CARRIER_LANE | 0.4817047229428191 | c<->d | 0.980686698570996 | 11636.600549992367 | 0 | STRONG_SLOT_SUPPORT_WITHOUT_LANE_CLOSURE |
| DERIVED_BOUNDARY_REORGANIZATION_LANE | 0.03183098861837902 |  | 0.0 | 0.0 | 0 | NO_OPEN_SLOT_IDENTITY_SURFACE |

## Key Fields

```text
stable_lane_closure_fraction = 0.9999993719460315
stable_lane_final_gap_to_A_SIDE = 2.6168915354118916e-08
top_slot = c<->t
top_slot_WI_self_support_score = 0.9880873618629215
top_slot_delta_in_ultra_units = 13877.028207745512
fixed_point_slot_promotions = 0
```

## Interpretation

The stable lane is collectively supported to the route-floor limit, but particle
identity remains localized and requires fixed-point W/I closure. Strong slot
self-support is therefore a candidate condition, not a promotion condition by
itself.

## Next Frontier

```text
QP035_PRIVATE_HALF_WRITE_INFORMATION_FIXED_POINT_SELECTOR
```
