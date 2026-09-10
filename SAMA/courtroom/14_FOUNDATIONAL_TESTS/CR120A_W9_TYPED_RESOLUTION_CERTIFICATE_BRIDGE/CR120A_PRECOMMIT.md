# CR120A Precommit

record_id: `CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE`
task: `Continue 8 + 1 closure witness bridge research from attached working note`
classification: `CONSTRUCTIVE_NEW_WORK`

## Question frozen before execution

Does the active SAM Language contract already establish a typed transition from
the unresolved `S8_BINARY_SURFACE` to the resolved
`W9_CLOSURE_WITNESS`, with `RESOLVE` as the gate,
`B_CONTACT_OPERATOR` as the contact operator, and
`X1_AXIS_SELF_CHANNEL` as a required independently typed input?

## Precommitted interpretation

```text
S8_BINARY_SURFACE : BinarySurface, Layer1StructuralCapacity
  -- RESOLVE(..., B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL) -->
W9_CLOSURE_WITNESS : ClosureWitness, Layer2Resolution
```

`W9_CLOSURE_WITNESS` is treated as the certificate emitted by the typed
resolution gate. The bridge is the registered `RESOLVE` operation; the result
is not reduced to scalar arithmetic `8 + 1 = 9`.

## Gates

1. The canonical three-argument `RESOLVE` expression must type-check and return
   `W9_CLOSURE_WITNESS` with semantic type `ClosureWitness`.
2. `PROMOTE_VOLUME` must accept the returned witness and produce
   `V27_VOLUME_CONTAINER`.
3. Direct promotion of `S8_BINARY_SURFACE` must reject because `BinarySurface`
   is not `ClosureWitness`.
4. Omitting `X1_AXIS_SELF_CHANNEL` must reject on `RESOLVE` arity.
5. Substituting `B_CONTACT_OPERATOR` for the axis input must reject on type.
6. Substituting `X1_AXIS_SELF_CHANNEL` for the contact input must reject on
   type.
7. Same-scalar entities `W9_CLOSURE_WITNESS` and `CARRIER9` must remain
   distinct; scalar equality must not merge their types or identities.
8. The CR120 frontier must remain unchanged: `PROPAGATE_CLOSURE`,
   `LEDGER_SITE`, `ADJACENT`, and `ADJACENT_LEDGER_STATE` remain missing.
9. No raw traceback may reach the generated result artifacts.

## Precommitted verdict logic

If all gates pass, the result is:

`PASS_TYPED_UNRESOLVED_TO_RESOLVED_GATE_BRIDGE_BOUNDARY_X1_INFORMATIONAL_INDEPENDENCE_OPEN`

This PASS means only that the active language enforces the typed gate and emits
the registered resolved closure witness. It does **not** establish that `X1`
carries independently variable information, that `W9` contains a recoverable
preimage/filling/correction payload, or that closure propagates to an adjacent
ledger site.

The preserved secondary boundary is:

`BOUNDARY_W9_CERTIFICATE_CONTENT_AND_X1_INDEPENDENCE_NOT_ESTABLISHED`

## Frozen sources

```text
aa0d61ece36d5c4621b7a54e0a810bc2ab2dbaf55ff5939bb651592085924f64  C:/Users/drwho/.codex/attachments/0592a489-6c9c-47ae-be29-df7752a1862c/pasted-text.txt
ad197382fb2594d32afa56ec936371bf093aa373656088792705343239359228  14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER/CR119_typed_hierarchy.json
93a8919058cd7e5c5b82a67ff73b907c4a87de58cf9aa95ebcc5f0bfde8f597e  14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER/CR119_OPERATOR_SIGNATURES.json
098c88a2275a359e6a9305836bb79baac306b1562dea117c1ecd2509f5b034e3  09a_PARTICLE_MASS_CHAIN/CR267_TENSOR_9_CLOSURE_WITNESS/CR267_result.md
beb5effdf9c3d0a0050e686f9a716f6f547c54dcc6e54efa878f685b0fdf1beb  09a_PARTICLE_MASS_CHAIN/CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT/CR282_APPEAL_result.md
be0217b92f2c49839dd32fb43ae985c34ee80de07873881d3d1078084b7270cb  09a_PARTICLE_MASS_CHAIN/CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT/CR282_APPEAL_summary.json
d40d2766b3166f9572c695fd68f7f4718e99e4c3db7c2e698baf60d5cdb195c1  SAM_LANGUAGE_V0_4_1_CANDIDATE/src/sam_language_v0_4/runtime.py
09ddbf4dd2647249404b3b9bbc8a01625ad181e848cc592fc98119c5b05de1b9  SAM_LANGUAGE_V0_4_1_CANDIDATE/V0_4_1_ENTITY_REGISTRY.json
5e7866eb0c8789c4d8fe321dd6ac131a8aff57429b58684bcd2507c03152a212  SAM_LANGUAGE_V0_4_1_CANDIDATE/V0_4_1_OPERATOR_REGISTRY.json
a725c1d267fb70f3f71f7a7e45965f1534c19582a339f9ded8814539e1ef36d5  SAM_LANGUAGE_V0_4_1_CANDIDATE/V0_4_1_REGRESSION_SUMMARY.json
75b2b02261e014985c2df378a1cb17c6766e90240c69924ae8d27aad5d842a8f  14_FOUNDATIONAL_TESTS/CR120_LOCAL_CLOSURE_PROPAGATION_ADJACENT_LEDGER_SITE/CR120_result.md
```

## Hard stop

Stop after one validated CR120A candidate. Do not add missing CR120 operators,
entities, relations, or science.
