# CR120A Result

record_id: `CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE`
sealed_utc: `2026-07-13T17:54:26Z`
scientific_result_status: `PASS`
primary_verdict: `PASS_TYPED_UNRESOLVED_TO_RESOLVED_GATE_BRIDGE_BOUNDARY_X1_INFORMATIONAL_INDEPENDENCE_OPEN`
secondary_boundary: `BOUNDARY_W9_CERTIFICATE_CONTENT_AND_X1_INDEPENDENCE_NOT_ESTABLISHED`

## Result

The frozen runtime confirms a typed unresolved-to-resolved gate:

```text
S8_BINARY_SURFACE : BinarySurface, Layer1StructuralCapacity
  -- RESOLVE(B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL) -->
W9_CLOSURE_WITNESS : ClosureWitness, Layer2Resolution
```

The decisive bridge is `RESOLVE`. `B_CONTACT_OPERATOR` is the registered
contact operator acting through the independently typed `X1_AXIS_SELF_CHANNEL`.
`W9_CLOSURE_WITNESS` is the resolved certificate emitted by that gate.

This is stronger than the scalar observation `8 + 1 = 9`: the language rejects
omitting X1, rejects B in the AxisChannel position, rejects X1 in the
ContactOperator position, and rejects direct volume promotion from unresolved
S8. It also keeps scalar-nine `W9_CLOSURE_WITNESS` distinct from scalar-nine
`CARRIER9`.

## Exact controls

```text
canonical RESOLVE(S8, B, X1) -> W9        PASS
PROMOTE_VOLUME(W9, D3) -> V27             PASS
PROMOTE_VOLUME(S8, D3)                    TYPE_REJECT
RESOLVE(S8, B)                            ARITY_REJECT
RESOLVE(S8, B, B)                         TYPE_REJECT
RESOLVE(S8, X1, X1)                       TYPE_REJECT
W9 == CARRIER9                            AUTHORITY_REJECT
```

## Scientific boundary

Required typed participation is not yet evidence of independent information.
The present runtime returns the registered W9 entity after validating the input
types; it does not expose an independently perturbable X1 payload or a
recoverable W9 preimage/filling/correction certificate. Those remain open.

The CR120 propagation frontier is unchanged:

```text
existing hierarchy PASS
PROPAGATE_CLOSURE missing
LEDGER_SITE missing
ADJACENT missing
ADJACENT_LEDGER_STATE missing
```

No missing science was invented.

## Verdict

`PASS_TYPED_UNRESOLVED_TO_RESOLVED_GATE_BRIDGE_BOUNDARY_X1_INFORMATIONAL_INDEPENDENCE_OPEN`

The typed bridge is established. X1 informational independence, W9 certificate
content, and physical/local propagation are not established.
