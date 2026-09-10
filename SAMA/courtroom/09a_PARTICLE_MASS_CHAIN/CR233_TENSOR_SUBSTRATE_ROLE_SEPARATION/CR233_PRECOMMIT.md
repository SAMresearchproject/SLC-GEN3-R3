# CR233 18 / 81 / 27 Tensor-Substrate Role-Separation Test — Precommit

**Date:** 2026-06-22
**Classification:** STRUCTURAL_ROLE_SEPARATION (direct CR229 extension)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 ("test 4 please")
**Source:** `C:\Users\drwho\OneDrive\Desktop\Tests.docx` Test 4 ("18 / 81 / 27 tensor-substrate role-separation")
**Part of:** Seven-test ownership arc (CR230-CR236)
**Arc position:** Test 4 of 7
**Status:** PRECOMMITTED before runner execution.

## Scope

Test that the four structural numbers `{18, 81, 27, 162}` from CR230 / CR229 play **distinct** structural roles in the substrate ledger. Each number has a locked identity and a locked behavior. If any of the four can be interchanged — if 18 behaves like a normal particle, if 81 (one-side) and 0303 (mirror) collapse, if 27 takes 18's tensor role — the interpretation fails.

Per Sean's locked rule: `18 = R²/2^D = α_H · D²` (tensor); `M_rest(18) = 18 − 18 = 0` (no rest-mass channel, because 18 IS the tensor that gets subtracted).

## Roles Under Test (Locked)

```text
ROLE 1   Tensor bridge        =  18      =  α_H · D²     =  R² / 2^D
ROLE 2   Carrier-response face=  81      =  D^(D+1)      =  per_side_unique + tensor = 63 + 18
ROLE 3   Record mirror (0303) =  81      =  D^(D+1)      (on the OTHER side of the closed ledger)
ROLE 4   Resolved 3D write    =  27      =  D³           =  (one_side · 4) / R
COMPOSITION  Closed ledger     =  162    =  R² · 9/8    =  ROLE 2 + ROLE 3
CROSS-IDENTITY                 18²       =  324          =  R · 27   (12 · 27 = 18²)
WRITE-RATE FROM LEDGER         2·162/R   =  27           (writes the ledger at D³)
REST CHANNEL FOR TENSOR        M_rest(18) = 18 − 18 = 0  (tensor has no rest signature)
```

## Row-Table Anchors (from CR219, hash-locked)

The four structural numbers occupy specific rows in the canonical 139-row table:

```text
ROLE 1 row:  QP093A-0300  partition_signature = 18   bin = carrier_only_rows    blocked (matter_row_allowed=no)
ROLE 3 row:  QP093A-0303  partition_signature = 81   bin = carrier_only_rows    blocked (mirror duplicate)
ROLE 2 sum:  twelve support-roster rows                partition_signature sum = 81
ROLE 4:      not a row; emerges from one_side · 4 / R = 81·4/12 = 27 (write-rate identity)
```

The role-separation predicate: each role must satisfy its identity AND its row-table position consistently. ROLE 1 and ROLE 3 share `bin = carrier_only_rows` and both blocked, but their partition_signatures differ (18 vs 81) and their structural identities differ (`α_H·D²` vs `D^(D+1)`). ROLE 2 is the sum of 12 distinct rows, not a single row. ROLE 4 is a derived scalar identity.

## Inputs (Hash-Locked at Execution)

```text
Source CSV:     C:\VS\CR219_promoted_particle_rows_126.csv
Source SHA-256: 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Constants:      R = 12, D = 3, alpha_H = 2
```

## Pass Condition (Precommitted)

```text
PASS  iff  ALL of the following hold:

  (1)  ROLE 1 identity: 18 = alpha_H · D² = R² / 2^D            (exact)
  (2)  ROLE 2 identity: 81 = D^(D+1) = per_side + tensor         (exact)
  (3)  ROLE 3 identity: 81 = D^(D+1)                              (exact)
  (4)  ROLE 4 identity: 27 = D³ = one_side · 4 / R                (exact)
  (5)  Closed ledger composition: 162 = 81 + 81 = R² · 9/8       (exact)
  (6)  Cross identity: 18² = R · 27 = 324                         (exact)
  (7)  Tensor rest-mass: M_rest(18) = 18 − 18 = 0                 (exact)
  (8)  Row anchor for ROLE 1: QP093A-0300 has partition_signature 18, bin carrier_only_rows, blocked
  (9)  Row anchor for ROLE 3: QP093A-0303 has partition_signature 81, bin carrier_only_rows, blocked
  (10) Row anchor for ROLE 2: 12 support-roster rows' partition_signature values sum to 81
  (11) All four wrong controls break role-interchange as predicted

FAIL otherwise.
```

## Wrong Controls (Precommitted)

- **WC1 — Swap 18 ↔ 27:** Try `27 = α_H · D²` (substitute 27 into the tensor identity). `2 · 9 = 18 ≠ 27`. Expected: BREAK.

- **WC2 — Swap 18 ↔ 81 (tensor ↔ mirror):** Try `81 = R²/2^D` and `18 = D^(D+1)`. `R²/2^D = 18 ≠ 81`. `D^(D+1) = 81 ≠ 18`. Expected: BREAK both directions.

- **WC3 — Collapse ROLE 2 into ROLE 3 (treat one-side as the mirror, no separate sides):** Then closed ledger becomes `81 + 0 = 81 ≠ 162`. Expected: BREAK (also already shown in CR230 WC3, restated here for cross-identity confirmation).

- **WC4 — Wrong write-cell identity: 27 ≠ D³ alternative.** Try `27 = D² · α_H` = `9 · 2 = 18 ≠ 27`. Or try `27 = R²/2^D · α_H/D` = `18 · 2/3 = 12 ≠ 27`. Expected: BREAK.

- **WC5 — Wrong cross-identity: 18² ≠ R · 27 alternative.** Try `18² = R² · D = 144 · 3 = 432 ≠ 324`. Expected: BREAK.

- **WC6 — Non-zero rest mass for tensor:** Try `M_rest(18) = 18 − 9 = 9 ≠ 0`. Expected: BREAK (no half-tensor in the substrate).

## Precommitted Predictions

- **P1:** ROLE 1 identity 18 = α_H·D² = R²/2^D holds exactly.
- **P2:** ROLE 2 identity 81 = D^(D+1) and per_side+tensor = 63+18 = 81 hold exactly.
- **P3:** ROLE 3 identity 81 = D^(D+1) holds exactly; row QP093A-0303 has partition_signature 81 and is in carrier_only_rows blocked bin.
- **P4:** ROLE 4 identity 27 = D³ = one_side·4/R holds exactly.
- **P5:** Closed ledger 162 = 81+81 = R²·9/8 holds exactly.
- **P6:** Cross identity 18² = R·27 = 324 holds exactly.
- **P7:** Tensor rest-mass: M_rest(18) = 18 − 18 = 0 holds exactly.
- **P8:** Row anchor ROLE 1: QP093A-0300 partition_signature = 18, blocked, carrier_only_rows.
- **P9:** Row anchor ROLE 3: QP093A-0303 partition_signature = 81, blocked, carrier_only_rows.
- **P10:** Row anchor ROLE 2: 12 support-roster partition_signature values sum to 81.
- **P11:** WC1-WC6 each break the role-interchange or alternative identity as predicted.

## K-Gate Audit (Precommitted Pre-Execution)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | N/A — structural role-separation; no outside-model contact |
| K2 | Falsification | Any of P1-P10 failing exact equality falsifies; any WC failing to break falsifies the test design |
| K3 | Target hygiene | Roles, identities, row anchors, wrong controls all locked here BEFORE the runner reads any data |
| K4 | Typed inputs | Three foundational constants (R, D, α_H) + SHA-locked CR219 source |
| K5 | Reproduction on demand | `python CR233_runner.py` reproduces every identity and every row check |

## Falsifier

If any role identity fails exact equality, or any row anchor is mis-located in the CR219 table, or any wrong control fails to break the interchange attempt, CR233 fails.

## Upstream Sources (Hash-Locked)

```text
CR230_result.md  = 3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR229_result.md  = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR222_result.md  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR216_result.md  = 5fd583b8f4c600c78e9aea4446b2d93b22f2de6cba33ef7d3dfe082f25346b80
CR114_result.md  = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR219_promoted_particle_rows_126.csv = 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
```

## Sequence Reminder

CR233 is **Test 4 of 7** in the Seven-Test Ownership Arc. Tests 5-7 remain:

- CR234 (Test 5): Blind SOB element engine (Z + constants only)
- CR235 (Test 6): qA/8 gravity bridge
- CR236@12a (Test 7): Paul Revere tomography

See `[[project-seven-test-ownership-arc-cr230-236]]`.
