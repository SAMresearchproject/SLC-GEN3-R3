# QP026 - Private Stable Lane Residual Closure Selector

## Result

```text
QP026_STABLE_RESIDUAL_TIGHT_NATIVE_CONTACT
```

QP026 compares the QP025 stable residual gap to a sealed family of native terms
from `A0`, `A_SIDE`, `A_SHARE`, `R`, `D`, and `alpha_H`.

## Stable Residual Target

```text
stable_open_gap_to_A_SIDE = 0.0013323515711069628
```

## Top Native Contacts

| rank | candidate | value | fraction of gap closed | relative delta | class |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | A0_over_R_plus_2_pow_D | 0.0013262911924324613 | 0.9954513667368844 | 0.004548633263115618 | TIGHT_NATIVE_RESIDUAL_CONTACT |
| 2 | A0_over_R_plus_D_sq | 0.0012631344689832964 | 0.9480489207017946 | 0.05195107929820542 | NEAR_NATIVE_RESIDUAL_CONTACT |
| 3 | A0_over_R_plus_alpha_H_times_D | 0.0014736568804805126 | 1.1060570741520939 | 0.10605707415209376 | NON_CONTACT_CANDIDATE |
| 4 | A_SIDE_over_R_times_D | 0.0011574074074074073 | 0.8686951946518096 | 0.13130480534819042 | NON_CONTACT_CANDIDATE |
| 5 | A0_over_R_times_alpha_H | 0.0011052426603603844 | 0.8295428056140703 | 0.17045719438592968 | NON_CONTACT_CANDIDATE |
| 6 | A0_over_R_plus_alpha_H_sq | 0.0016578639905405765 | 1.2443142084211054 | 0.2443142084211054 | NON_CONTACT_CANDIDATE |
| 7 | A_SHARE_over_R_times_alpha_H_sq | 0.001736111111111111 | 1.3030427919777143 | 0.3030427919777144 | NON_CONTACT_CANDIDATE |
| 8 | A_SIDE_over_R_times_alpha_H | 0.001736111111111111 | 1.3030427919777143 | 0.3030427919777144 | NON_CONTACT_CANDIDATE |

## Key Fields

```text
best_candidate = A0_over_R_plus_2_pow_D
best_candidate_value = 0.0013262911924324613
best_fraction_of_gap_closed = 0.9954513667368844
residual_after_best_candidate = 6.060378674501484e-06
best_contact_class = TIGHT_NATIVE_RESIDUAL_CONTACT
```

## Interpretation

The best sealed native term is:

```text
A0 / (R + 2^D)
```

It closes about 99.545 percent of the QP025 stable residual gap but does not
exactly close it. The remaining residual is small enough to justify a targeted
route-exposure crumb selector as the next forward gate.

## Next Frontier

```text
QP027_PRIVATE_ROUTE_EXPOSURE_RESIDUAL_CRUMB_SELECTOR
```
