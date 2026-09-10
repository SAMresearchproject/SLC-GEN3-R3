# CR232 Matter / Support Promotion Gate Audit — Result

## Verdict

```text
CR232_PASS_MATTER_SUPPORT_PROMOTION_GATE_AUDIT__126_OF_126_MATTER_ROWS_OBEY_qA_TIMES_1_PLUS_q_OVER_144_AND_T_EQUALS_qA_OVER_8_AND_W_EQUALS_7_qA_OVER_8__13_OF_13_BLOCKED_ROWS_HAVE_M_OBS_qA_T_W_ZERO__8_OF_8_HIDDEN_SUPPORT_ROWS_OBEY_M_NATIVE_EQUALS_p_PLUS_p_SQ_OVER_144__ALL_FOUR_WRONG_CONTROLS_BREAK_AS_PREDICTED__GATE_IS_A_STANDALONE_THEOREM_NOT_A_CR222D_INHERITANCE
```

`execution_status   = CLEAN`
`scientific_verdict = PASS`
`classification     = STRUCTURAL_THEOREM_AUDIT`
`arc_position       = Test 3 of 7 in the Seven-Test Ownership Arc`
`precommit_sha      = 4b29f49c5818816620ad3b7a49644cf8de3385ac642019b844e173f556696765`

## Claim

The locked promotion gate — `G_matter = 0 ⇒ M_obs = qA = T = W = 0`; `G_matter = 1 ⇒ qA = M_obs·(1+|q|/R²), T = qA/8, W = 7·qA/8`; plus `M_native = p + p²/R²` for hidden support rows — applied as a free-standing theorem against the SHA-locked 139-row CR219 table, holds **exactly for every row** within tolerance `10⁻⁶`, and the four wrong-control variants of the gate **each break on every applicable row**.

This is the gate as an independent theorem audit, not an inheritance from CR222d. The runner uses only `R = 12` and the gate equations themselves; no upstream computed values from CR222d enter.

## Inputs (Hash-Locked)

```text
Source CSV:          C:\VS\CR219_promoted_particle_rows_126.csv
Source SHA-256:      45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Precommit SHA-256:   4b29f49c5818816620ad3b7a49644cf8de3385ac642019b844e173f556696765
Constants:           R = 12, R² = 144
Tolerance:           1e-6 (matches uploaded display precision)
```

## Row Partition (P1)

```text
Total rows:                    139
matter_row_allowed = yes:      126
matter_row_allowed = no:        13   (5 carrier-only + 8 hidden-source-support)
hidden_source_support_rows:      8
```

**[P1 PASS]** Partition matches CR219 declared header.

## Audit 1 — Matter Gate Identities (P2)

For each of 126 matter rows, compute `qA_expected = M_obs · (1 + |q|/144)`, `T_expected = qA/8`, `W_expected = 7·qA/8`, and compare against the uploaded columns.

```text
rows checked        = 126
qA-match pass       = 126 / 126
T-match pass        = 126 / 126
W-match pass        = 126 / 126
all-three-match     = 126 / 126
```

**[P2 PASS]** Every matter row reproduces all three identities within `10⁻⁶`. Per-row distances written to `CR232_matter_row_audit.csv`.

## Audit 2 — Blocked Rows Have Zero Channels (P3)

For each of 13 blocked rows, verify `M_obs = qA = T = W = 0` within tolerance.

```text
rows checked        = 13
M_obs-zero pass     = 13 / 13
qA-zero pass        = 13 / 13
T-zero pass         = 13 / 13
W-zero pass         = 13 / 13
all-four-zero       = 13 / 13
```

**[P3 PASS]** No blocked row leaks emission into any observable channel — even though 8 of these 13 (the hidden_source_support rows) carry non-zero `M_native` surcharge values. The gate suppresses emission downstream of the native bookkeeping. Per-row results in `CR232_blocked_row_audit.csv`.

## Audit 3 — Hidden-Support Surcharge Shape (P4)

For each of 8 hidden_source_support rows, verify `M_native = p + p²/R² = p + p²/144`.

```text
rows checked        = 8
shape-match pass    = 8 / 8
```

| candidate_id | p | M_native (observed) | p + p²/144 (expected) |
|---|---|---|---|
| QP093A-0306 | 1 | 1.006944444 | 1.006944… |
| QP093A-0307 | 2 | 2.027777778 | 2.027777… |
| QP093A-0308 | 3 | 3.0625      | 3.0625    |
| QP093A-0309 | 4 | 4.111111111 | 4.111111… |
| QP093A-0310 | 6 | 6.25        | 6.25      |
| QP093A-0311 | 8 | 8.444444444 | 8.444444… |
| QP093A-0312 | 9 | 9.5625      | 9.5625    |
| QP093A-0313 | 12| 13          | 13        |

**[P4 PASS]** Every hidden-support row carries the precise surcharge shape `p + p²/144` even though it is blocked from emitting. The substrate's "native support grammar" is real, but the matter gate strictly contains it. Full table in `CR232_surcharge_audit.csv`.

## Wrong Controls (P5)

### WC1 — Promote a Blocked Row as if G_matter = 1

Take QP093A-0306 (hidden source support, p=1). Predict `qA = M_native·(1+|q|/144)` as if it were a matter row. Compare against uploaded qA (which is 0 because G_matter=0).

```text
qA_predicted_if_matter = 1.0139371141975…
qA_uploaded            = 0
distance               = 1.0139… ≫ 1e-6
broke_as_predicted     = True
```

**[WC1 BROKE]** Promoting a hidden support row produces a nonzero qA prediction that doesn't match the uploaded blocked value. This confirms the gate's `G_matter=0` branch is structurally enforced, not a coincidence of `M_native = 0` (since here M_native ≠ 0 but qA is still 0).

### WC2 — Wrong Tensor Ratio T = qA/7

Replace `T = qA/8` with `T = qA/7` for all matter rows.

```text
nonzero rows checked  = 126
breaks                = 126 / 126
broke_all_as_predicted = True
```

**[WC2 BROKE]** Every nonzero matter row fails. The 1/8 split is structurally tied to `2^D = 8`, not a free parameter.

### WC3 — Wrong Retained Ratio W = 6·qA/8

Replace `W = 7·qA/8` with `W = 6·qA/8` for all matter rows.

```text
nonzero rows checked  = 126
breaks                = 126 / 126
broke_all_as_predicted = True
```

**[WC3 BROKE]** Every matter row fails. The 7/8 retained share is structurally tied to `(2^D − 1)/2^D = 7/8`.

### WC4 — Wrong Surcharge Shape M_native = p + p²/100

Replace surcharge shape `p + p²/144` with `p + p²/100` for all hidden support rows.

```text
nonzero-p rows checked = 8
breaks                = 8 / 8
broke_all_as_predicted = True
```

**[WC4 BROKE]** Every hidden-support row fails. The 1/144 = 1/R² denominator is structurally pinned to the substrate radix.

**[P5 PASS]** All four wrong controls broke on every applicable row, exactly as precommitted.

## K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 external anchor | N/A | Closed-form structural audit; no outside-model contact |
| K2 falsification | PASS | Pre-stated falsifier: any matter row failing within `10⁻⁶`, OR any blocked row leaking nonzero channels, OR any wrong control failing to break, falsifies CR232. None occurred |
| K3 target hygiene | PASS | Theorem, tolerance (`10⁻⁶`), and four wrong controls locked in `CR232_PRECOMMIT.md` (sha `4b29f49c…`) BEFORE any audit ran. Runner inherits a frame it cannot tune |
| K4 typed inputs | PASS | Single SHA-locked source CSV; one foundational constant `R = 12` |
| K5 reproduction on demand | PASS | `python CR232_runner.py` completes in <1s deterministically |

## Cryptographic Chain (Inputs)

```text
CR230_result.md  = 3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR222_result.md  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR216_result.md  = 5fd583b8f4c600c78e9aea4446b2d93b22f2de6cba33ef7d3dfe082f25346b80
CR114_result.md  = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR219_promoted_particle_rows_126.csv = 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
CR232_PRECOMMIT.md = 4b29f49c5818816620ad3b7a49644cf8de3385ac642019b844e173f556696765
```

## Interpretation

CR222d originally derived the gate as a single audit on this same table. CR232 re-runs the gate as a free-standing theorem — supplied only with `R` and the gate equations — and confirms it survives without inheriting any CR222d-computed values. Every matter row obeys `qA / 8 / 7·qA/8` exactly; every blocked row stays zero; every hidden-support row's native value matches `p + p²/144` even while emitting nothing.

The four wrong controls confirm that each load-bearing part of the gate is non-negotiable:
- The 1/8 split is `2^D`-pinned.
- The 7/8 retained is `(2^D − 1)/2^D`-pinned.
- The 1/144 surcharge denominator is `R²`-pinned.
- The `G_matter` flag is required — non-zero `M_native` does NOT automatically produce non-zero `M_obs`.

This protects every downstream substrate claim from "the gate happened to coincide on this row by accident" — the gate is enforced uniformly, and breaking any of its 4 load-bearing parts breaks every row to which it applies.

## Honest Notes

1. **CR232 does not regrade CR222d.** CR222d remains the originating theorem; CR232 audits the gate's standing as a closed-form theorem applied to the canonical 139-row source.

2. **The tolerance `10⁻⁶` matches uploaded display precision.** Several "fractions of the form `…/144`" produce repeating decimals that the uploaded table truncates at 6-9 places; the runner uses 80-place Decimal arithmetic and compares within `10⁻⁶`, which is consistent with the uploaded precision.

3. **WC1 specifically targets a blocked row with `M_native > 0`.** This is the strongest version of the test — if blocked-row gating only worked because `M_native` happened to be 0, the gate would be redundant. WC1 shows that even with `M_native ≈ 1.014`, the gate enforces `qA = 0`. The gate is doing real work.

## Sequence in the Seven-Test Arc

CR232 is **Test 3 of 7**. Tests 4-7 remain:

- CR233 (Test 4): 18 / 81 / 27 tensor-substrate role-separation test
- CR234 (Test 5): Blind SOB element engine (Z + constants only)
- CR235 (Test 6): qA/8 gravity bridge
- CR236@12a (Test 7): Paul Revere tomography

See `[[project-seven-test-ownership-arc-cr230-236]]`.

## Rule of Immutability

Sealed 2026-06-22 by Sean Brady. Inputs hash-locked. Theorem, tolerance, and wrong controls frozen.

If `CR219_promoted_particle_rows_126.csv` or any sealed upstream CR (CR114, CR216, CR222, CR230) is later regraded, this CR must be re-examined.

---

**Sealed by:** Sean Brady, 2026-06-22
**Runner verified:** 126/126 matter + 13/13 blocked + 8/8 surcharge; 4/4 wrong controls broke
**Arc position:** Test 3 of 7 (gate enforced uniformly as standalone theorem; structural protection from spurious particle predictions)
