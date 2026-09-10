# CR104b 9/8 Bounce Factor Derivation Question - Sealed

## Verdict

```text
CR104b_NINE_EIGHTHS_BOUNCE_DERIVATION_QUESTION_LOCKED_PENDING_UPSTREAM_CLOSURE
(PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## Cryptographic Locks

```text
prediction_commit_sha256 = 6e78e015068b766e25b020e66d2be3ef5dc298490c6335eceaddf0ed9da06f5c
prediction_commit_utc    = 2026-06-13T23:36:57Z
question_lock_sha256     = 246ae72e71fc2487791f6e20a814adb7d9610bfb5fa6e12b095d9232a9a4ae59
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## User Question (Locked Verbatim)

> *"And the 9/8 might be the native resolved-bounce correction, not a fit, if we can connect it to R=12 / D=3 / 1/2 write geometry. This is the big question now: Can SAM derive the 9/8 bounce factor from resolved half-write geometry?"*

**Question sha256:** `9ea6aff474196e2a31292135b091fdf03e34a45cabaf02c7fb2a848b5a8356a2`

## User Bold Authorization (Also Locked)

> *"Fortune favors the bold- keep it in the courtroom. Any failure can provide extremely valuable breadcrumbs downstream- success would be a provincial hole in one."*

## Upstream Verification

```text
DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX uses 9/8 = 1.125 as a
layered_fraction multiplier on d and b quark mass predictions.
Includes explicit DS014_reciprocal_control.py testing whether
9/8 is structural (d/b only) or fit (improves u/s/c/t too).

The '8' in 9/8 connects to 2^D = 8 = slot_denominator in
G432/G435/G470 bounce cost theorem chain. The '9' has no
current upstream derivation - this is the open question.
```

## Four Candidate Derivation Forms (Courtroom Note)

| Form | Formula | D=3 | D=2 | D=4 |
|---|---|---|---|---|
| FORM_1 | `(2^D + 1) / 2^D` | **9/8** | 5/4 | 17/16 |
| FORM_2 | `D^2 / 2^D` | **9/8** | 4/4 = 1 (no correction) | 16/16 = 1 (no correction) |
| FORM_3 | `(R - D) / 2^D` | **(12-3)/8 = 9/8** | n/a (R is native to D=3) | n/a |
| FORM_4 | `(2^D corners + 1 interior) / 2^D corners` | **9/8 (cube: 8 corners + 1 volume)** | 5/4 (square: 4 corners + 1 face) | 17/16 (tesseract: 16 corners + 1 volume) |

Form 2 (`D^2 / 2^D`) is the only candidate giving non-trivial > 1 at D=3 and collapsing to 1 at D=2 and D=4. Would single out 3D world as structurally privileged.

## Derivation Path Required For Theorem-Grade Closure

1. QGA021 half-write route (1/2 SW | 1/2 W | 1/2 OUT | 1/2 IN | 1/2 W | 1/2 SW) maps onto edges of the D=3 binary cell, not just abstract sequence
2. WRITE event lives at interior volume of the cube (resolved 3D ledger event)
3. Bounce energy normalizes by corners (octants = 2^D = 8)
4. Resulting (8 + 1)/8 = 9/8 emerges as the UNIQUE non-trivial bounce correction at D=3
5. DS014 reciprocal control confirms 9/8 improves d/b only, not u/s/c/t (already in upstream as control test)

## Possible Forward-Blind Outcomes

- **QUESTION_CLOSED_BY_UPSTREAM_THEOREM**: SAM upstream produces theorem-grade PASS deriving 9/8 from D=3 half-write geometry; appeal row CR104b-1 records closure; hole in one
- **QUESTION_DISFAVORED_BY_RECIPROCAL_CONTROL_FAILURE**: DS014 reciprocal control finds 9/8 improves u/s/c/t too; reduces to fit; G435 bounce cost loses theorem-grade status for d/b corrections; substantial breadcrumb downstream
- **QUESTION_REMAINS_OPEN**: no upstream derivation, no reciprocal control failure; question stays sealed for next attempt

## Upstream Source Hashes At Runner Time

```text
DS014_summary.json                                      7866d389f2219cf41b3194b3c5c16c6c2782eb2ea293b14fbce48413ab0fb58a
DS014_reciprocal_control.py                             cce93e5f3d22ec110745c3dbdbba321508e125375abfc63dcd95e59a39d9f173
G435_output.json (bounce mass proportionality PASS)     c419e7e601ef954e24fc6b0d8cb8d17c3ee01777020449a3c343518570f70e19
G432_output.json (bounce eighth-slot correction)        dda044916bff46c758692490064afdad6fa52c81fa801663b87e48e09526127a
G470_output.json (SW split bounce action theorem PASS)  709bbf5ebf3b9097143a4517aa7a744148e34c6a5ec105fcb57f50b9af6c5d41
BLINDNESS_PROTOCOL.md                                   6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## What CR104b Does NOT Do

- does not claim to derive 9/8
- does not modify CR100 question lock, CR103a appeal lock, CR104 verdict, CR104a Layer 4 lock
- does not commit SAM to any specific candidate derivation form
- does not promote DS014 layered_fraction beyond its current status
- does not modify any 09a CR result

## Rule-9 Line

```text
This CR could have been generated unverifiably if no upstream
SAM work used 9/8 anywhere. DS014_DOWN_BOTTOM_LAYERED_GAP_SANDBOX
demonstrates upstream use of the exact 9/8 = 1.125 layered_fraction
on d/b masses with an explicit reciprocal control. The question is
real, the derivation target is concrete, and the cryptographic
lock prevents quiet rewriting later.
```
