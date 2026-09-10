# TEST 8 — Z=96 Regime-Change / N-Z Stability Collapse Test — PRECOMMIT

**Date:** 2026-06-22
**Classification:** STRUCTURAL_BOUNDARY_DETECTION (external nuclide table comparison)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 (full Test 8 spec issued)
**Status:** PRECOMMITTED before runner execution.

## Purpose

Test whether SAM predicts a real structural regime change at:

```text
Z_break = R * 2^D = 12 * 8 = 96
```

The test question is: does the external nuclide table show a statistically detectable change in SAM primary-isotope agreement immediately after Z=96, with the collapse beginning at Z=97?

The SAM neutron rule is NOT to be tuned after seeing external data. The boundary is locked: `Z_break = 96`, `Z_first_post = 97`.

## Native SAM Constants (Locked)

```text
alpha_H = 2
D       = 3
R       = 12
SPLIT   = 2^D = 8
Z_break = R * SPLIT = 96
Z_pre   = 85..96   (one radix cycle ending at the boundary)
Z_post  = 97..108  (one radix cycle starting at the boundary + 1)
```

## SAM Neutron Rule (Locked)

For every `Z = 1..126`:

```text
radix_cycle(Z)    = floor((Z - 1) / R) + 1
selected_depth(Z) = max(0, radix_cycle - 1)
delta_N(Z)        = floor(Z * selected_depth / R)
N_SAM(Z)          = Z + delta_N(Z)
A_SAM(Z)          = Z + N_SAM(Z)
```

## Required Audit Rows (Locked)

```text
Z=84:  cycle=7,  depth=6, delta_N=42, N=126, A=210
Z=96:  cycle=8,  depth=7, delta_N=56, N=152, A=248
Z=97:  cycle=9,  depth=8, delta_N=64, N=161, A=258
Z=108: cycle=9,  depth=8, delta_N=72, N=180, A=288
Z=118: cycle=10, depth=9, delta_N=88, N=206, A=324
Z=119: cycle=10, depth=9, delta_N=89, N=208, A=327
Z=120: cycle=10, depth=9, delta_N=90, N=210, A=330
Z=121: cycle=11, depth=10, delta_N=100, N=221, A=342
```

Boundary jumps:
```text
N_SAM(97) - N_SAM(96) = 161 - 152 = 9
A_SAM(97) - A_SAM(96) = 258 - 248 = 10
```

If any audit row fails: `FAIL_TEST8_SAM_GENERATOR`.

## External Input Schema

`inputs/external_nuclide_table.csv` minimum columns:

```text
Z, N, A, symbol, half_life, half_life_sec, is_stable, isomer_flag, source
```

Alias normalization allowed:
```text
z->Z, n->N, a->A, mass_number->A, element->symbol,
half_life_seconds->half_life_sec, stable->is_stable, isomer->isomer_flag
```

If `A` is missing, compute `A = Z + N`. If `half_life_sec` is missing but `is_stable=true`, set `half_life_sec = inf`. Ground states preferred; if isomer status unknown, keep the row and mark `isomer_status_unknown=true`. Do not silently discard.

## External Anchor Construction (Locked)

**Lane A — longest-lived ground-state anchor:**
For each Z, select the known isotope with the largest `half_life_sec` among ground-state rows. Tied stable rows flagged with `stable_tie=true`.

```text
Z, anchor_N_longest, anchor_A_longest, anchor_half_life_sec, anchor_symbol, stable_tie, anchor_valid
```

**Lane B — nearest known isotope to SAM primary:**

```text
nearest_known_delta_N(Z) = min over known N of |N_known - N_SAM(Z)|
nearest_known_N, nearest_known_A, nearest_known_delta_N, nearest_known_half_life_sec
```

**Lane C — exact SAM isotope known:**

```text
sam_primary_known, sam_primary_half_life_sec, sam_primary_source
```

## Scoring by Z

Per-row residuals:
```text
N_residual = N_anchor - N_SAM
A_residual = A_anchor - A_SAM
abs_N_residual = |N_residual|
exact_N_match = (N_anchor == N_SAM)
near2 = (|N_anchor - N_SAM| <= 2)
near5 = (|N_anchor - N_SAM| <= 5)
```

## Primary Window Statistics (Locked)

```text
J_96 = median(|r_N|_post) - median(|r_N|_pre)
C_96 = near2_rate_pre - near2_rate_post
K_96 = sam_primary_known_rate_pre - sam_primary_known_rate_post
```

## Primary Pass Criteria (Locked)

**PASS_TEST8_Z96_STRONG_REGIME_CHANGE** requires ALL of:
```text
pre_count >= 10
post_count >= 10
J_96 >= 5
post_median_abs_N_residual_anchor >= 2 * max(pre_median_abs_N_residual_anchor, 1)
C_96 >= 0.50
K_96 >= 0.50
p_random_boundary <= 0.001
```

**PASS_TEST8_Z96_BOUNDARY_SIGNAL** requires ALL of:
```text
pre_count >= 10
post_count >= 10
J_96 >= 3
C_96 >= 0.30
p_random_boundary <= 0.01
```

**BOUNDARY_TEST8_Z96_MIXED_SIGNAL**: positive signal but fails collapse or random-boundary.

**FAIL_TEST8_Z96_NO_REGIME_CHANGE**: J_96 <= 0 or fails controls.

## Random Boundary Control (Locked)

```text
b in [84, 112]
N_RANDOM_BOUNDARIES = 10000
seed = 20260621
For each b: pre window = Z=b-11..b; post window = Z=b+1..b+12
Skip if any window has fewer than 8 externally scored rows
J_b = median(|r_N|_post,b) - median(|r_N|_pre,b)
p_random = (1 + #{J_b >= J_96}) / (1 + N_valid)
```

## Changepoint Scan (Locked)

```text
b = 84..112
For each b: compute J_b, C_b, K_b
is_SAM_boundary = (b == 96)
Cycle boundaries: 12, 24, 36, 48, 60, 72, 84, 96, 108, 120
Relevant cycle boundaries in scan: 84, 96, 108
Report ranks honestly; DO NOT MOVE the SAM boundary.
```

## Wrong Controls (Locked)

- **A** R=10, D=3 → Z_break_control = 80
- **B** R=11, D=3 → Z_break_control = 88
- **C** R=13, D=3 → Z_break_control = 104
- **D** R=12, D=2 → SPLIT=4, Z_break_control = 48
- **E** R=12, D=4 → SPLIT=16, Z_break_control = 192 (out of range; `CONTROL_OUT_OF_RANGE_FAIL`)
- **F** Shuffled anchor_N_longest, seed 20260621
- **G** Smooth null: least-squares quadratic `N_smooth(Z) = a + bZ + cZ^2` — used as null comparison only, no special Z=96 boundary

A control degrades if:
```text
J_control < J_96  OR  p_control > 0.01
```

At least **5 of 7** controls must degrade for the main result to pass.

## Internal Checks JSON (Locked)

All must be true before any pass verdict:

```text
constants_locked
Z_break_equals_96
first_post_boundary_Z_equals_97
SAM_prediction_rows_equal_126
audit_Z84_passed
audit_Z96_passed
audit_Z97_passed
audit_Z108_passed
audit_Z118_passed
audit_Z119_passed
audit_Z120_passed
audit_Z121_passed
external_table_loaded
external_anchor_rows_created
primary_pre_window_count_at_least_10
primary_post_window_count_at_least_10
random_boundary_controls_completed
changepoint_scan_completed
wrong_controls_completed
no_boundary_relocation
no_post_reveal_tuning
```

## Allowed Verdicts

```text
PASS_TEST8_Z96_STRONG_REGIME_CHANGE
PASS_TEST8_Z96_BOUNDARY_SIGNAL
BOUNDARY_TEST8_Z96_MIXED_SIGNAL
FAIL_TEST8_Z96_NO_REGIME_CHANGE
FAIL_TEST8_INPUT_SCHEMA
FAIL_TEST8_SAM_GENERATOR
FAIL_TEST8_EXTERNAL_DATA_INSUFFICIENT
FAIL_TEST8_CONTROLS_NOT_DEGRADED
FAIL_TEST8_BOUNDARY_RELOCATED
FAIL_TEST8_POST_REVEAL_TUNING
```

## Allowed / Disallowed Claims

**If strong pass:** SAM's locked Z=96 boundary shows a statistically significant external regime-change signal: the one-cycle window after Z=96 exhibits a sharp collapse in agreement with external isotope anchors compared with the window before Z=96, and the effect survives random-boundary and wrong-control tests.

**If moderate pass:** SAM's locked Z=96 boundary shows an external boundary signal in isotope-anchor residuals, but the result should be treated as a scoped nuclear-frontier signal pending replication with NUBASE/AME and alternate anchor definitions.

**If boundary/mixed:** The Z=96 boundary remains structurally interesting but is not yet externally confirmed by this scoring lane.

**Disallowed:**
- "Observation confirms SAM because Z=96 looks important."
- "The Z=96 boundary proves the substrate."
- "The agent may move the boundary to the best-scoring Z value."

The boundary is locked before scoring. If another Z scores better, report that.

## Agent Warnings (Locked)

```text
Do not change R, D, 2^D, or Z_break after seeing external data.
Do not choose a different isotope anchor because it improves the result.
Do not choose a different tolerance after scoring.
Do not hide stable-tie rows.
Do not report a clean hit if random-boundary controls do not degrade.
Do not call this a discovery test unless the boundary survives controls.
```

## K-Gate Audit (Plan)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | External NUBASE-style nuclide table is the anchor; QP061 observed roster (sealed source); compared by ratios/residuals, no model fitting allowed |
| K2 | Falsification | Pre-stated failure modes: J_96 ≤ 0, p_random_boundary > 0.01, fewer than 5/7 controls degraded |
| K3 | Target hygiene | Z_break, windows, statistics, pass criteria, random-boundary seed, control parameters all locked here BEFORE the runner reads external data |
| K4 | Typed inputs | Constants R/D/alpha_H; external nuclide table SHA-locked; controls use constant-substituted formulas only |
| K5 | Reproduction on demand | Deterministic + seeded controls (random boundaries, shuffled anchor: seed 20260621) |
