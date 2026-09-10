# QP036 - Private Local Information-Return Correction Selector

## Result

```text
QP036_LOCAL_RETURN_CORRECTION_CONTACT_SELECTED
```

QP036 asks whether the QP035 missing local information-return correction is
already present in the native QP/SAM surfaces.

## Selected Candidate

```text
candidate = residual_stack_minus_R_neutral_route_reservation
formula = residual_after_floor * R*(D + alpha_H) - minimum_route_exposure * R
value = 0.00036312764030734386
target = 0.0003631206076198587
abs_delta = 7.032687485153139e-09
delta_in_ultra_units = 0.2687420319102455
```

## Top Candidate Rows

| rank | candidate | value | abs delta | ultra units | class | provenance rank |
| ---: | --- | ---: | ---: | ---: | --- | ---: |
| 1 | residual_stack_minus_R_neutral_route_reservation | 0.00036312764030734386 | 7.032687485153139e-09 | 0.2687420319102455 | ULTRA_CONTACT_SELECTED | 6 |
| 2 | A0_over_R_sq_over_alpha_H_plus_one | 0.0003633674499814962 | 2.4684236163749875e-07 | 9.432655434786541 | TIGHT_LOCAL_RETURN_CONTACT | 2 |
| 3 | residual_after_floor_times_R_times_D_plus_alpha_H | 0.00036362272047008905 | 5.021128502303435e-07 | 19.187377215896426 | TIGHT_LOCAL_RETURN_CONTACT | 5 |
| 4 | route_crumb_sum_times_R_times_D_plus_alpha_H | 0.00036205258554899083 | 1.0680220708678763e-06 | 40.812622778413036 | TIGHT_LOCAL_RETURN_CONTACT | 5 |
| 5 | two_A0_over_R_sq | 0.00036841422012012814 | 5.293612500269435e-06 | 202.2862785345146 | NEAR_LOCAL_RETURN_CONTACT | 2 |
| 6 | route_bundle_QUBIT-BN-001;QUBIT-TM-001;QUBIT-TP-001 | 0.00035583520008721284 | 7.285407532645863e-06 | 278.39929298021747 | NEAR_LOCAL_RETURN_CONTACT | 4 |
| 7 | route_bundle_QUBIT-CL-001;QUBIT-TM-001;QUBIT-TP-001 | 0.00030163786872645156 | 6.148273889340714e-05 | 2349.4569056997593 | NO_LOCAL_RETURN_CONTACT | 4 |
| 8 | route_bundle_QUBIT-UNK-001;QUBIT-TM-001;QUBIT-TP-001 | 0.00029875559605196716 | 6.436501156789154e-05 | 2459.597988563965 | NO_LOCAL_RETURN_CONTACT | 4 |

## Top Slot Applications

| rank | slot | candidate | corrected W/I delta | ultra units | class |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | c<->t | residual_stack_minus_R_neutral_route_reservation | 1.9136227868965777e-08 | 0.7312579680897545 | LOCAL_RETURN_FIXED_POINT_CONTACT |
| 2 | c<->u | A0_over_R_times_alpha_H | 2.669057835272444e-08 | 1.0199344524427687 | LOCAL_RETURN_HELD_OPEN |
| 3 | c<->t | A0_over_R_sq_over_alpha_H_plus_one | 2.2067344628337983e-07 | 8.432655434786541 | LOCAL_RETURN_HELD_OPEN |
| 4 | c<->t | residual_after_floor_times_R_times_D_plus_alpha_H | 4.7594393487622455e-07 | 18.187377215896426 | LOCAL_RETURN_HELD_OPEN |
| 5 | c<->t | route_crumb_sum_times_R_times_D_plus_alpha_H | 1.0941909862219952e-06 | 41.812622778413036 | LOCAL_RETURN_HELD_OPEN |
| 6 | t<->u | A0_over_R_plus_2_pow_D | 1.6405095065723675e-06 | 62.689243492629345 | LOCAL_RETURN_HELD_OPEN |
| 7 | c<->d | route_bundle_QUBIT-CL-001;QUBIT-TM-001;QUBIT-TP-001 | 2.87934607599231e-06 | 110.02924794661422 | LOCAL_RETURN_HELD_OPEN |
| 8 | c<->t | two_A0_over_R_sq | 5.267443584915316e-06 | 201.2862785345146 | LOCAL_RETURN_HELD_OPEN |

## Interpretation

The local-return correction is selected as a native residual-chain return with
one full neutral route reservation. Applied to the strongest W/I slot, it
reduces the corrected W/I delta below the QP032 ultra residual.

## Next Frontier

```text
QP037_PRIVATE_PARTICLE_IDENTITY_CLOSURE_FREEZE
```
