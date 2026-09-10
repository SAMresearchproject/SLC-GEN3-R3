# CR120D Runtime Contract Result

record_id: `CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE`
sealed_utc: `2026-07-13T18:30:27Z`
result_class: `RUNTIME_CONTRACT_BOUNDARY`
scientific_pass_claimed: `false`
disposition: `RUNTIME_BOUNDARY_X1_STATIC_DERIVED_CONTENT_NO_INDEPENDENT_INTERVENTION_SURFACE_W9_TYPED_ROUTE_CERTIFICATE_ONLY`

## Direct answer

X1 has **static registered content**, but the installed runtime does **not**
represent independently perturbable X1 content.

```text
entity                 X1_AXIS_SELF_CHANNEL
scalar                 1
type                   AxisChannel
roles                  axis_self_coupling, axis_fee
origin                 D^(D-1)-S and axis self-coupling
canonical AxisChannels 1
entity representation  immutable
intervention syntax    absent
```

Therefore X1 is mathematically and semantically distinct, but there is no
runtime operation for preparing `x0`, preparing `x1`, resetting X1, or changing
X1 while S8 and B remain fixed. Physical perturbability is unresolved; it is
not physically falsified.

## What RESOLVE actually does

The current implementation:

1. resolves the three named inputs;
2. checks that their types are exactly
   `(BinarySurface, ContactOperator, AxisChannel)`;
3. checks authority;
4. selects the operator signature's fixed result entity,
   `W9_CLOSURE_WITNESS`.

It does not read the arguments' scalar values, metadata, or contextual roles to
compute an outcome. The installed RESOLVE output alphabet is therefore the
singleton `{W9_CLOSURE_WITNESS}`, with zero bits of input-dependent variation.
That zero-bit statement applies only to the present fixed-result runtime. The
scalar value `9` is not an information-capacity measure.

## What W9 certifies exactly

### W9 entity itself

```text
entity_id          W9_CLOSURE_WITNESS
scalar_value       9
semantic_type      ClosureWitness
authority          ACTIVE
contextual_role    resolved_closure_witness
metadata           empty
provenance         CR119 typed hierarchy and handoff contract
```

### Complete execution record

The surrounding execution packet additionally records:

```text
operator           RESOLVE
inputs             S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL
result             W9_CLOSURE_WITNESS
typed-plan trace   present
source trace       present
warnings           present as a field
```

So the strongest exact certificate is:

> The active runtime accepted the registered typed RESOLVE route and returned
> its registered resolved-closure-witness entity, with trace and provenance.

## What W9 does not currently certify

No current W9 field carries:

- a measured closure Boolean or independently defined closure predicate;
- a parity bit or sector label;
- a residual, uncertainty, soundness, or completeness value;
- an X1 intervention identifier;
- a fault location, input preimage, repair, or correction;
- measurement backaction.

The name and contextual role encode the contract's semantic assertion. They do
not yet provide a dynamic measurement certificate or empirical proof that an
input state closed.

## Consequence for the parity candidate

The CR120C parity model remains mechanically coherent research, but the active
runtime cannot yet express its decisive experiment. It needs at minimum:

1. two sourced admissible X1 settings;
2. an invariant-preserving intervention contract;
3. an input-dependent W9 outcome schema;
4. a sourced proposition mapping each outcome to what it certifies;
5. independent soundness/completeness challenges.

The CR120 frontier remains unchanged.
