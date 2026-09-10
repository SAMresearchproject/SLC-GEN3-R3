# QP025 - Private Sub-A-Side Reinforcement Selector

## Result

```text
QP025_STABLE_OPEN_REINFORCEMENT_NEAR_A_SIDE
```

QP025 asks whether held-open slots can accumulate coherently inside each derived
lane.

## Lane Reinforcement

| derived replay lane | open slots | open native sum | open fraction of A_SIDE | open gap to A_SIDE | open class | carrier support |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| DERIVED_BOUNDARY_REORGANIZATION_LANE | 0 | 0 | 0.0 | 0.041666666666666664 | OPEN_REINFORCEMENT_SUB_A_SIDE | FROZEN_ONLY_NO_OPEN_REINFORCEMENT |
| DERIVED_CHARGED_CARRIER_LANE | 4 | 0.018744738930185 | 0.44987373432444 | 0.022921927736481666 | OPEN_REINFORCEMENT_SUB_A_SIDE | CARRIER_ASSISTED_REINFORCEMENT_SURFACE |
| DERIVED_STABLE_ANCHOR_LANE | 4 | 0.0403343150955597 | 0.9680235622934329 | 0.0013323515711069628 | OPEN_REINFORCEMENT_NEAR_A_SIDE | CARRIER_ASSISTED_REINFORCEMENT_SURFACE |

## Key Fields

```text
A_SIDE = 0.041666666666666664
A_SHARE = 0.08333333333333333
stable_open_fraction_of_A_SIDE = 0.9680235622934329
stable_open_gap_to_A_SIDE = 0.0013323515711069628
charged_open_fraction_of_A_SIDE = 0.44987373432444
charged_open_gap_to_A_SIDE = 0.022921927736481666
open_lanes_crossing_A_SIDE = 0
carrier_assisted_lanes = 2
```

## Interpretation

Open-only reinforcement does not cross `A_SIDE`, but the stable open lane is a
near-boundary reservoir: its held-open rows reach roughly 96.8 percent of
`A_SIDE`.

That makes the next question sharply local: what supplies the small remaining
stable-lane closure gap without changing the already frozen QP023 rows?

## Next Frontier

```text
QP026_PRIVATE_STABLE_LANE_RESIDUAL_CLOSURE_SELECTOR
```
