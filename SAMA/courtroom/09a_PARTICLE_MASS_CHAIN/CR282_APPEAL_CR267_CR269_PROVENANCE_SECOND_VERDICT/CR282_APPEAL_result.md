# CR282 Appeal Result

record_id: `CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT`
sealed_utc: `2026-07-12T07:24:55Z`
scientific_result_status: `APPEAL_GRANTED_IN_PART`
current_status: `APPEAL_GRANTED_SCOPE_REFINED_CONTACT_AXIS_FEE_BRIDGE_PASS_A_TO_CONTACT_WELD_OPEN`
parent_record: `CR282_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD`
parent_record_preserved: `true`

## Verdict Impact

CR282 stays on record exactly as the original boundary verdict. Its historical row-trace result remains `PASS`, and its narrow direct A-through-X1 weld remains `OPEN`.

The appeal changes the current interpretation of CR269's role. CR269 is not merely a competing contact model against CR282. In combination with CR267, it is positive provenance for a narrower closure bridge:

```text
B/contact -> X1 axis-fee -> W9
```

That bridge passes on the locked source chain because CR267 seals `9 = 8 + 1` with the `+1` as axis self-coupling / axis fee, and CR269 seals `B : R^2 -> (M, Theta_out)` with release fraction `1/8` explicitly matched to the CR267 axis-fee fraction.

## Typed Current Status

```text
historical row trace              : PASS, unchanged from CR282
non-row A operator                : PASS, preserved from CR256 and CR282
canonical non-row A ledger        : 162
retired-row restoration control   : 163
B/contact -> X1 axis-fee -> W9    : PASS on CR267 + CR269 provenance
A_OPERATOR -> B/contact           : OPEN
A_OPERATOR -> X1 directly         : OPEN under CR282's original narrow claim
```

## Source Impact

See `CR282_APPEAL_source_impact.csv` for the source-by-source appeal impact table.

## Validation

All locked source hashes matched the manifest. All appeal gates passed. Parent artifacts were not rewritten.
