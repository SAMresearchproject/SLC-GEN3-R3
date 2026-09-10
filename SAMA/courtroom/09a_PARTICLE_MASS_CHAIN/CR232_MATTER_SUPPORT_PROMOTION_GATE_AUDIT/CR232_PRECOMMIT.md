# CR232 Matter / Support Promotion Gate Audit — Precommit

**Date:** 2026-06-22
**Classification:** STRUCTURAL_THEOREM_AUDIT (closed-form gate equations applied to every row)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 ("test 3 please")
**Source:** `C:\Users\drwho\OneDrive\Desktop\Tests.docx` Test 3 ("Matter/Support Promotion Gate Audit")
**Part of:** Seven-test ownership arc (CR230-CR236)
**Arc position:** Test 3 of 7 — promote the locked CR222d gate from a single theorem into a full-table standalone audit.
**Status:** PRECOMMITTED before runner execution.

## Scope

Run the locked promotion gate as a standalone audit over all 139 rows of the canonical CR219 table. Independently verify (a) every blocked row stays blocked, (b) every matter row obeys the `qA/8 / 7qA/8` split exactly, and (c) hidden support rows carry the surcharge shape `M_native = p + p²/R²` but emit nothing.

This is **not** a regrade of CR222d. CR222d originated the gate. CR232 audits the gate as a free-standing theorem applied to the same 139-row source, using only `R` and the gate equations as inputs — without trusting the upstream CR222d derivation.

## Theorem Under Audit (Locked)

```text
G_matter = 0  ⇒  M_obs = qA = T = W = 0
G_matter = 1  ⇒  qA  = M_obs · (1 + |q|/R²)
                 T   = qA / 8
                 W   = 7 · qA / 8
```

Plus the support-surcharge shape, declared but blocked:

```text
For hidden_source_support_rows (G_matter = 0):
  M_native = p + p² / R²        (still blocked from emitting; M_obs = 0)
```

Numerical tolerance: `|observed − expected| ≤ 10⁻⁶` (display precision of the uploaded table).

## Inputs (Hash-Locked at Execution)

```text
Source CSV:        C:\VS\CR219_promoted_particle_rows_126.csv
Source SHA-256:    45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Constants:         R = 12  (R² = 144)
Tolerance:         1e-6
```

## Pass Condition (Precommitted)

```text
PASS  iff
  (1)  Every G_matter=1 row reproduces qA = M_obs·(1+|q|/144) within tolerance
  (2)  Every G_matter=1 row reproduces T  = qA/8     within tolerance
  (3)  Every G_matter=1 row reproduces W  = 7·qA/8   within tolerance
  (4)  Every G_matter=0 row has M_obs = qA = T = W = 0 (within tolerance)
  (5)  Every hidden_source_support row reproduces M_native = p + p²/R² within tolerance
  (6)  All four wrong controls (below) break the closure as predicted

FAIL otherwise.
```

## Wrong Controls (Precommitted)

- **WC1 — Promote one blocked row:** Pick a hidden_source_support row (e.g., QP093A-0306, p=1). Compute qA = M_native·(1+|q|/144) as if G_matter were 1. The resulting qA value MUST NOT equal the uploaded qA (which is 0); WC1 expected to break.

- **WC2 — Wrong tensor ratio:** For all matter rows, replace T = qA/8 with T' = qA/7. Compare T' against uploaded tensor_carrier_support. WC2 expected to break — the 7-split signature is structurally tied to D, not editorial.

- **WC3 — Wrong retained ratio:** For all matter rows, replace W = 7·qA/8 with W' = 6·qA/8. Compare W' against uploaded retained_write_support. WC3 expected to break.

- **WC4 — Wrong surcharge shape:** For all hidden_source_support rows, replace M_native = p + p²/144 with M_native' = p + p²/100. Compare M_native' against uploaded M_native. WC4 expected to break for every row with p > 0.

## Precommitted Predictions

- **P1:** 139 rows parsed; 126 matter, 13 blocked (5 carrier-only + 8 hidden-source-support).
- **P2:** All 126 matter rows pass the three matter-gate identities (qA, T, W) within `1e-6`.
- **P3:** All 13 blocked rows pass the four-channels-zero requirement.
- **P4:** All 8 hidden_source_support rows pass the surcharge shape `M_native = p + p²/R²`.
- **P5:** WC1, WC2, WC3, WC4 each break the closure.
- **P6:** Result tables CSVs written per category (matter pass list, blocked verification, surcharge shape).
- **P7:** Per-row tolerance distances recorded and reported in summary.

## K-Gate Audit (Precommitted Pre-Execution)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | N/A — this is a closed-form structural audit; no outside-model contact |
| K2 | Falsification | Any matter row failing qA/8/7·qA/8 within `1e-6` falsifies the gate; any blocked row leaking non-zero channels falsifies the gate; any wrong control failing to break falsifies the test design |
| K3 | Target hygiene | Theorem, tolerance, and wrong controls are locked here BEFORE any audit row reads. The runner inherits a frame it cannot tune |
| K4 | Typed inputs | Single canonical CSV (sha-locked); single foundational constant R=12 |
| K5 | Reproduction on demand | `python CR232_runner.py` reproduces every row and every wrong-control verdict |

## Falsifier

If any single row fails its expected gate behavior within tolerance, this CR fails. If every wrong control passes (i.e., does NOT break the closure), the test design is unsound and the verdict is FAIL even if the main checks pass.

## Upstream Sources (Hash-Locked)

```text
CR230_result.md  = 3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR222_result.md  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR222d_result.md = (referenced — the originating gate theorem; CR232 audits it independently)
CR216_result.md  = 5fd583b8f4c600c78e9aea4446b2d93b22f2de6cba33ef7d3dfe082f25346b80
CR114_result.md  = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
Source CSV (CR219_promoted_particle_rows_126.csv) = 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
```

## Honest Note

The precommit transcribes Sean's locked Test 3 spec from `Tests.docx`. The gate equations are quoted verbatim. The tolerance was chosen to match the uploaded table's display precision (CR222d uses the same `1e-6`). Wrong controls are constructed to test each load-bearing edge of the gate; if any of them inadvertently passes, that itself is a structural finding.

## Sequence Reminder

CR232 is **Test 3 of 7** in the Seven-Test Ownership Arc. Tests 4-7 remain:

- CR233 (Test 4): 18/81/27 tensor-substrate role-separation test
- CR234 (Test 5): Blind SOB element engine (Z-only input)
- CR235 (Test 6): qA/8 gravity bridge
- CR236@12a (Test 7): Paul Revere tomography

See `[[project-seven-test-ownership-arc-cr230-236]]`.
