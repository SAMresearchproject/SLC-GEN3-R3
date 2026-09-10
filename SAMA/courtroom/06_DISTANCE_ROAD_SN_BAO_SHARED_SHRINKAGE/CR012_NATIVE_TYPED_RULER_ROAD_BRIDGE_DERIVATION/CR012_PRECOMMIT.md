# CR012 Precommit

## Test ID

```text
CR012_NATIVE_TYPED_RULER_ROAD_BRIDGE_DERIVATION
```

## Test Type

```text
Fresh Courtroom branch test.
Not a pointer to a G-test verdict.
G728c/G731c are provenance only.
```

## Question

```text
Can the native typed bridge derive the drag-ruler bridge, the settled
projection operator, and the phi/phi^R lane separation without selecting from
target data?
```

## Frozen Formula Set

```text
A0 = 1/(pi*R)
A_inf = A0*R
w = (D/R)*(Omega_b/Omega_BB_PBH_trapped)
r_drag = r_star*(1+w)
S_projection(phi) = 1+w*phi
burst(phi) = 1+(D/R)*phi^R
```

## Wrong Controls

```text
drop_D_over_R
use_Omega_b_over_Omega_m
use_phi_power_in_projection
half_loading
sign_flipped_loading
```

## Pass Conditions

```text
no_older_test_verdicts_used = true
free_parameters_introduced_zero = true
A0_identity = true
w_identity = true
r_drag_identity = true
projection_operator_identity = true
phi_and_phi_R_roles_separated = true
wrong_controls_do_not_match_packet = true
```

## Rule-9 Line

```text
This test could have falsified: the claim that the same native typed grammar
derives the r_drag bridge, the settled projection operator, and the phi/phi^R
lane split without selecting from SN, BAO, or CMB target data.
```

