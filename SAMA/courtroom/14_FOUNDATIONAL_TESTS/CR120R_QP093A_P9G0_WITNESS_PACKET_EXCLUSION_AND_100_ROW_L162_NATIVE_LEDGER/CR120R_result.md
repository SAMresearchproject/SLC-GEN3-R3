# CR120R QP093A p9,g0 Witness-Packet Exclusion and 100-Row L162 Native Ledger

record_id: `CR120R_QP093A_P9G0_WITNESS_PACKET_EXCLUSION_AND_100_ROW_L162_NATIVE_LEDGER`  
execution_status: `CLEAN`  
mathematical_verdict: `PASS`  
scientific_verdict: `STRONG_STRUCTURAL_PASS`  
result_class: `STRUCTURAL_RESEARCH_BOUNDARY`  
scientific_pass_claimed: `false`

## Direct result

The PDF's hard closure finding passes every precommitted exact gate.

```text
source rows                         105
complete five-role address packets  21
address-value sum                    2889
full native inventory                130005/8 = 16250.625
excluded typed packet                p=9,g=0 (5 rows)
payload rows                          100
payload native inventory              16200
payload mean                          162 = L
single-packet L162 hits               1: [(9, 0)]
```

All 105 rows satisfy the exact packet laws. The five same-role p9,g0 rows
equal their p1,g0 plus p8,g0 parents in exact `M_native` arithmetic. Scanning
all 21 possible single-packet exclusions finds exactly one 100-row L162
closure: `(p,g)=(9,0)`.

The derived 100 payload IDs and values reconcile one-for-one with the current
`Updated Particle Rows.xlsx` extraction. All 105 source rows remain visible;
the result is a counted/not-counted overlay, not a source deletion.

## Typed controls

Scalar 9 is not treated as one untyped object. `W9_CLOSURE_WITNESS`,
`C9_CARRIER_ATOM`, and `P9_BIGRADE_PARTITION` remain distinct types.
`QP093A-0302 weak_vector_support` and `QP093A-0312 hidden_source_support[p=9]`
are not admitted to the p9,g0 payload selector. The p9 identity is not extended
to g1, g2, composite routes, or qA.

## Binding boundary

The exact 16200 result is a full-ledger conservation/accounting gate. It is
not a binding-energy term, fitted coefficient, or quantity to subtract from
nuclear mass. The binding fee question belongs to typed lift excess and
isotope geometry, outside this CR.
