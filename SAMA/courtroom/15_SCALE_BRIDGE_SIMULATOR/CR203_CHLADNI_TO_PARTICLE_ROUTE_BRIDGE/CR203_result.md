# CR203 Chladni-To-Particle Route Bridge

## Verdict

```text
CR203_PASS_CHLADNI_TO_PARTICLE_ROUTE_BRIDGE_QP091_FRESH
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SIMULATOR_CHLADNI_ROUTE_BRIDGE
```

## Question

Can the Chladni plate support boundary routes without becoming a stale particle selector?

## Pass Conditions

| condition | pass |
|---|---:|
| chladni_gate_pass | true |
| not_audit_or_retest | true |
| no_free_parameters | true |
| qp091_live_surface | true |
| no_direct_qp075_live_inputs | true |
| lab_plate_all_pass | true |
| boundary_records_present | true |
| all_records_link_qp091 | true |
| no_particle_promotion | true |
| route_candidate_rows_scoped | true |
| wrong_controls_rejected | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_G752c_CHLADNI_TO_PARTICLE_ROUTE_CLOSURE_BRIDGE_QP091_FRESH | source G-test result |
| live_surface | C:\VS\quantum_phase\artifacts\qp091 | fresh QP091 surface |
| lab_plate_campaign | C:\VS\Stam_model-A-v1.0\tests\Substrate\G518_G524_CHLADNI_PLATE_CAMPAIGN | lab plate path |
| direct_qp075_live_inputs | 0 | stale direct inputs rejected |
| wrong_controls | 6/6 | all Chladni controls rejected |

## Rule-9 Line

```text
This test could have falsified the claim that the Chladni bridge uses the QP091 live surface and lab plate only as boundary-route support, not stale QP075 or toy plate direct promotion.
```

## Notes

- The route bridge stays scoped to boundary/mode support.
