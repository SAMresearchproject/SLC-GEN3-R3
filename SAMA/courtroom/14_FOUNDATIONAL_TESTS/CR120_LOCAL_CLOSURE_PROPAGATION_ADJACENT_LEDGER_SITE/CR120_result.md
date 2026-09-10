# CR120 Result

record_id: `CR120_LOCAL_CLOSURE_PROPAGATION_ADJACENT_LEDGER_SITE`
sealed_utc: `2026-07-12T10:25:30Z`
scientific_result_status: `BOUNDARY`
primary_verdict: `BOUNDARY_CLOSURE_HIERARCHY_PASS_ADJACENCY_OR_LOCALITY_UNSOURCED`
secondary_boundary: `BOUNDARY_THETA_CONTACT_PROPAGATION_CANDIDATE_CONSERVATION_RULE_OPEN`

## Question

Test whether the sealed closure hierarchy can be written, transmitted, or propagated from one completed ledger state into an adjacent unresolved ledger state.

The scoped target is site-local, not a global replay:

```text
L162_FULL_LEDGER@site_i
  with THETA18_PRIMARY_CARRIER, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL
  -> W9_CLOSURE_WITNESS@site_j
  -> V27_VOLUME_CONTAINER@site_j
  -> F81_COMPLETED_FACE@site_j
  -> L162_FULL_LEDGER@site_j
```

## Replayed Sealed Prefix

The v0.4.1 engine replays the active hierarchy exactly:

```text
S8 --B through X1--> W9
W9 * D3 -> V27
V27 * D3 -> F81
F81 * H2 -> L162
```

Result:

```text
entity: L162_FULL_LEDGER
value: 162
type: FullLedger
authority: ACTIVE
```

Exact arithmetic passed:

```text
W = 8 + 1 = 9
V = 9 * 3 = 27
F = 27 * 3 = 81
L = 81 * 2 = 162
Theta = 2 * 9 = 18
N = 8 * 18 = 144
```

## Boundary Found

The new propagation edge is not authorized by the active language or sealed hierarchy. The live v0.4.1 CLI reports:

```text
UnknownOperatorError: No registered operator named PROPAGATE_CLOSURE
UnknownEntityError: No registered entity named ADJACENT_LEDGER_STATE
```

No sourced `LEDGER_SITE` type or `ADJACENT` relation was found in the scoped active chain. Therefore this CR cannot promote local closure propagation as an active physical operator.

## Preserved Boundaries

```text
B_CONTACT_OPERATOR acts_through X1_AXIS_SELF_CHANNEL : PASS
A_OPERATOR relation_to_B                              : OPEN
P80_PARTICLE_FACE_CONTENT authority                   : STRUCTURAL_ONLY
```

The result does not insert A, B, X1, P80, or the closure address as a ledger row.

## Model Comparison

```text
W9 witness propagation        : OPEN
Theta18 carrier propagation   : BOUNDARY, conservation/accounting rule open
B/contact disturbance         : OPEN
global L162 replay            : REJECTED
A-operator insertion          : REJECTED
same-site identity replay     : REJECTED
```

## Verdict

`BOUNDARY_CLOSURE_HIERARCHY_PASS_ADJACENCY_OR_LOCALITY_UNSOURCED`

The hierarchy itself is executable and preserved. The local-propagation claim stops at the missing site and operator contract: `PROPAGATE_CLOSURE`, `LEDGER_SITE`, `ADJACENT_LEDGER_STATE`, and `ADJACENT` must be sourced before v0.4.1 can execute this as anything more than a boundary witness.

## Handoff

Generated for the next CR:

```text
CR120_LANGUAGE_HANDOFF_CONTRACT.json
CR120_VALIDATION_REPORT.json
CR120_SOURCE_MANIFEST.json
CR120_WRONG_CONTROLS.json
CR120_MODEL_COMPARISON.json
```
