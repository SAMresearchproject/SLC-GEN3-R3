# CR222j PR Self-Correction Triad Carrier Result

**Result class:** `CR222j_PASS_PR_SELF_CORRECTION_TRIAD_CARRIER__0115_PLUS_0301_WITH_0225_FOLLOWUP`

**Checks:** 24/24

**CR222j_self_correction_roster.csv SHA-256:** `1c977f579cc6908f2fcdd42ba78dbeb24df0c26f4c52a1d05a415de91009e5e9`

## Verdict

CR222j locks the self-correction upgrade:

```text
QP093A-0115 + QP093A-0301
= three-owner correction particle + road-light correction carrier
```

The correction theorem is:

```text
three-owner logical state -> detect owner disagreement -> carrier removes error entropy -> return to closed three-owner state
```

The PR warning no longer means ordinary decoherence. It means:

```text
A_leak < 1/24  => correction operating normally
A_leak >= 1/24 => correction capacity exceeded; emit warning
```

Rows locked:

```text
QP093A-0115: color_triad[1+1+1], qA/T/W = 72.5 / 9.0625 / 63.4375
QP093A-0301: ROAD_LIGHT_CARRIER,p=1, syndrome and entropy-removal route
QP093A-0300: tensor witness/floor, not correction actuator
QP093A-0225: strong p=8 follow-up, qA/T/W = 4088 / 511 / 3577
QP093A-0235: two-owner detection-only control
```
