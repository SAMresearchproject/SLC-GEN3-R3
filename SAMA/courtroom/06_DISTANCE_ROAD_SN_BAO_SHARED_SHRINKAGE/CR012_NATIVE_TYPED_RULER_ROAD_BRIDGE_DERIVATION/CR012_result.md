# CR012 Native Typed Ruler-Road Bridge Derivation

## Verdict

```text
CR012_PASS_NATIVE_TYPED_RULER_ROAD_BRIDGE_DERIVATION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_NATIVE_TYPED_BRIDGE
```

## Derived Packet

```text
A0 = 0.026525823848649
A_inf = 0.318309886183791
w = 0.0466031311731253
r_drag_mpc = 150.921864015187
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_verdicts_used | true |
| free_parameters_introduced_zero | true |
| A0_identity | true |
| w_identity | true |
| r_drag_identity | true |
| projection_operator_identity | true |
| phi_and_phi_R_roles_separated | true |
| wrong_controls_do_not_match_packet | true |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Rule-9 Line

```text
This test could have falsified the claim that the same native typed grammar derives the r_drag bridge, the settled projection operator, and the phi/phi^R lane split without selecting from SN, BAO, or CMB target data.
```
