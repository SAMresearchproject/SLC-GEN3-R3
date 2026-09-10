# QP028 - Private Ultra Residual Floor Selector

## Result

```text
QP028_ULTRA_RESIDUAL_BELOW_ROUTE_EXPOSURE_FLOOR_BOUNDARY
```

QP028 tests whether the QP027 ultra-residual is large enough to accept another
whole QP001 route-exposure quantum.

## Floor Result

```text
ultra_residual = 2.6168915354118916e-08
minimum_route_exposure = 4.125668022876614e-08
minimum_route = QUBIT-NL-001
ultra_residual_fraction_of_minimum_route = 0.6342952270762854
below_route_exposure_floor = True
```

## Lowest Additions

| rank | route | exposure | overshoot after addition | class |
| ---: | --- | ---: | ---: | --- |
| 1 | QUBIT-NL-001 | 4.125668022876614e-08 | 1.508776487774144e-08 | WHOLE_ROUTE_EXPOSURE_OVERSHOOTS_A_SIDE |
| 2 | QUBIT-UNK-001 | 1.5553402022183398e-06 | 1.5291712868667484e-06 | WHOLE_ROUTE_EXPOSURE_OVERSHOOTS_A_SIDE |
| 3 | QUBIT-CL-001 | 4.437612876702741e-06 | 4.411443961349626e-06 | WHOLE_ROUTE_EXPOSURE_OVERSHOOTS_A_SIDE |
| 4 | QUBIT-BN-001 | 5.8634944237463996e-05 | 5.860877532210679e-05 | WHOLE_ROUTE_EXPOSURE_OVERSHOOTS_A_SIDE |
| 5 | QUBIT-TM-001 | 0.00010135211901783056 | 0.00010132595010247519 | WHOLE_ROUTE_EXPOSURE_OVERSHOOTS_A_SIDE |
| 6 | QUBIT-TP-001 | 0.00019584813683191829 | 0.00019582196791656514 | WHOLE_ROUTE_EXPOSURE_OVERSHOOTS_A_SIDE |

## Interpretation

The remaining residual is below the smallest whole QP001 route exposure. Adding
even the smallest route exposure overshoots `A_SIDE`. This is a real boundary
for the current Phase 2 particle lane: the stable chain is close, but it does
not close under whole route-exposure crumbs.

## Next Frontier

```text
STOP_PHASE2_STABLE_RESIDUAL_FLOOR_BOUNDARY
```
