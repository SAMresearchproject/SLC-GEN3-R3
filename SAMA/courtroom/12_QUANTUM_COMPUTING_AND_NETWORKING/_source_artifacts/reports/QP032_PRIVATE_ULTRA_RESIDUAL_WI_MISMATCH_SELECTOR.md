# QP032 - Private Ultra Residual W/I Mismatch Selector

## Result

```text
QP032_ULTRA_RESIDUAL_SELECTED_AS_WI_MISMATCH_BOUNDARY
```

QP032 classifies the QP031 ultra residual under the Phase 3 W/I closure frame.

## W/I Closure Readout

| quantity | value | meaning |
| --- | ---: | --- |
| W_target | 0.041666666666666664 | A_SIDE half-write target |
| I_return | 0.04166664049775131 | stable lane after boundary floor plus allowed route crumbs |
| W_minus_I_mismatch | 2.6168915354118916e-08 | remaining mismatch before exact W/I closure |
| minimum_whole_route_exposure | 4.125668022876614e-08 | smallest whole route quantum available to additive continuation |
| top_slot_gap_after_boundary_floor | 0.011182505865634202 | best single-slot gap after boundary floor |

## Role Scores

| rank | candidate role | score | decision | reason |
| ---: | --- | ---: | --- | --- |
| 1 | WI_RETURN_MISMATCH_BOUNDARY | 6 | SELECT_PRIMARY_ROLE | W_target minus I_return equals recorded ultra residual; mismatch is below whole route-exposure floor; no single slot promotes under boundary floor; no prefix promotes under allowed route crumbs |
| 2 | ADDITIVE_ROUTE_CONTINUATION | 0 | BLOCK | mismatch is smaller than the smallest whole route exposure |
| 3 | NUMERICAL_ROUNDING_ONLY | 0 | BLOCK | mismatch is small but above pure numerical-rounding cutoff |
| 4 | SINGLE_SLOT_PROMOTION_DEFICIT | 0 | BLOCK | top open-slot gap is far larger than the ultra residual; slot promotion did not occur in QP031 |

## Interpretation

The ultra residual is exactly the remaining difference between the half-write
target and the information-return support after the boundary floor and allowed
route crumbs. It is below the smallest whole route-exposure quantum, so QP032
blocks ordinary additive continuation. The next move is W/I self-support at the
slot level, not another threshold push.

## Next Frontier

```text
QP033_PRIVATE_SLOT_WI_SELF_SUPPORT_TABLE
```
