# CR282 Appeal -- CR267/CR269 Provenance Second Verdict -- Precommit

record_id: `CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT`
parent_record: `CR282_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD`
preflight_report: `artifacts/preflight_filled/PREFLIGHT_20260712_022143_no_script.md`
classification: `APPEAL_CURRENT_STATUS_ARTIFACT`
permission_status: `USER_REQUESTED_APPEAL_DOCUMENTATION_AND_SECOND_VERDICT`

## Parent Preservation

CR282 remains sealed as originally produced:

- `scientific_result_status = BOUNDARY`
- `primary_verdict = BOUNDARY_A_OPERATOR_ROW_TRACE_PASS_AXIS_SELF_WELD_OPEN`
- historical row trace: `PASS`
- direct A-through-X1 axis-self weld: `OPEN`

This appeal does not modify CR282. The original boundary/failure is kept on record as a correct result for the narrow claim it tested.

## Appeal Ground

After reviewing CR282, the new appeal ground is that CR269 should not be treated only as a competing alternative. CR269 is also positive provenance for the contact/write side of the closure structure because it seals:

```text
B : R^2 -> (M, Theta_out)
R^2 = S * Theta = 8 * 18 = 144
Theta_out / R^2 = 1/8
```

CR269 explicitly identifies its `1/8` release fraction with CR267's axis-fee fraction. CR267 already seals:

```text
9 = (mirror + axis)^2 = 4 + 4 + 1 = 8 + 1
+1 = axis self-coupling / axis fee
```

Therefore the appeal tests whether the current status should be refined from a single open A-axis weld to a typed split:

```text
B/contact -> X1 axis-fee -> W9 : source-supported PASS
A_OPERATOR -> B/contact       : OPEN
A_OPERATOR -> X1 directly     : OPEN under CR282's original narrow claim
```

CR256 remains source provenance that A is a non-row substrate operator over the ledger. It does not by itself identify A with B/contact.

## Locked Source Set

The locked source manifest is `CR282_APPEAL_SOURCE_MANIFEST.json`.

## Verdict Rule

If all gates in `CR282_APPEAL_VERDICT_RULES.json` pass, the second verdict is:

```text
APPEAL_GRANTED_SCOPE_REFINED_CONTACT_AXIS_FEE_BRIDGE_PASS_A_TO_CONTACT_WELD_OPEN
```

with `scientific_result_status = APPEAL_GRANTED_IN_PART`.

If any source hash, parent preservation check, CR267 closure witness check, CR269 contact/axis-fee check, or scope-separation check fails, the appeal is denied or remains boundary.

## Boundaries

- Do not overwrite CR282.
- Do not change ledger counts.
- Do not turn non-row A into a row.
- Do not merge A, B, X1, C1, or P1 by scalar value.
- Do not inspect or modify SAM Language.
- Do not run queue maintenance.
- Do not generate forecasts.
