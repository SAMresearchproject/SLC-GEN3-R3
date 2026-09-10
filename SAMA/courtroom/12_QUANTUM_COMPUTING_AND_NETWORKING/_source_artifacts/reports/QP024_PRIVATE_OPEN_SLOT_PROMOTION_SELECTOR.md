# QP024 - Private Open Slot Promotion Selector

## Result

```text
QP024_OPEN_SLOT_FRONTIER_RANKED_NO_NATIVE_PROMOTION
```

QP024 starts from QP023's held-open particle slots and applies the native
thresholds already used by QP016:

```text
A_SIDE = 0.041666666666666664
A_SHARE = 0.08333333333333333
```

## Lane Frontier

| derived replay lane | open slots | promotes now | top frontier pair | top fraction of A_SIDE | top gap to A_SIDE |
| --- | ---: | ---: | --- | ---: | ---: |
| DERIVED_CHARGED_CARRIER_LANE | 4 | 0 | c<->d | 0.34658246814480004 | 0.027225730493966663 |
| DERIVED_STABLE_ANCHOR_LANE | 4 | 0 | c<->t | 0.6997888706064 | 0.012508797058066665 |

## Top Open Frontiers

| pair | derived lane | native strength | fraction of A_SIDE | class |
| --- | --- | ---: | ---: | --- |
| c<->t | DERIVED_STABLE_ANCHOR_LANE | 0.0291578696086 | 0.6997888706064 | TOP_OPEN_FRONTIER_BELOW_A_SIDE |
| c<->d | DERIVED_CHARGED_CARRIER_LANE | 0.0144409361727 | 0.34658246814480004 | TOP_OPEN_FRONTIER_BELOW_A_SIDE |

## Interpretation

No held-open slot crosses the native `A_SIDE` boundary in QP024. The result is
still useful: it ranks the next open fronts without changing frozen QP023
surface claims.

The strongest two frontiers are:

```text
stable lane  = c<->t
charged lane = c<->d
```

## Next Frontier

```text
QP025_PRIVATE_SUB_A_SIDE_REINFORCEMENT_SELECTOR
```
