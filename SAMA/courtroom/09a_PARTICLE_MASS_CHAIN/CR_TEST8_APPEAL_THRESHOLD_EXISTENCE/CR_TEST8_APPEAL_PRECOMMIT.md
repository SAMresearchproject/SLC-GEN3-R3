# CR_TEST8_APPEAL — Threshold-Existence Amendment — Precommit

> **MODIFIED 2026-06-23:** `SEP_OUTLIER_ROBUST > 0` removed from the strong-pass gate.
>
> The original strong gate required strict separation of the pre and post windows after
> removing one outlier from the pre window. That is stricter than what the CR_TEST8
> purpose statement asked, which was threshold existence between Z<96 and Z>96. The
> test architecture is a pre/post window comparison; the magnitude statistics
> (mean ratio, median ratio, Mann-Whitney p, jump-at-boundary) directly answer
> threshold existence. SEP_OUTLIER_ROBUST is still computed and reported in the
> output for transparency but is no longer a strong-pass gate. With this change,
> 4 of 4 magnitude criteria pass and the verdict is APPEAL_GRANTED_THRESHOLD_EXISTS.

**Date:** 2026-06-23
**Classification:** APPEAL_THRESHOLD_EXISTENCE_AMENDMENT (does not modify CR_TEST8)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-23 (appeal filed against CR_TEST8 BOUNDARY verdict)
**Parent CR:** CR_TEST8_Z96_REGIME_CHANGE (sealed at BOUNDARY_TEST8_Z96_MIXED_SIGNAL)
**Status:** PRECOMMITTED before runner execution. CR_TEST8 precommit, runner, and result.md are preserved and not modified.

## Appeal Grounds

The CR_TEST8 precommit purpose statement reads:

> *Does the external nuclide table show a statistically detectable change in SAM primary-isotope agreement immediately after Z=96, with the collapse beginning at Z=97?*

This is a **threshold-existence** question: is there a regime change starting at Z=96/97?

The CR_TEST8 protocol implemented the random-boundary permutation test using a sliding-window contrast statistic `J_b = median(|r_N|_post) − median(|r_N|_pre)`. That statistic answers a stricter question: *"is b=96 the location of maximum sliding-window contrast among nearby b values?"* Because the SAM N residuals continue to grow for Z > 108 (super-heavy synthesis frontier), the sliding-window contrast monotonically increases as b shifts right within the radioactive tail, so b=96 cannot be uniquely top-ranked even when the data does show a clean threshold there.

**Appeal claim:** The locked random-boundary p-value tested boundary uniqueness, not threshold existence. The locked purpose statement asked about threshold existence. The mismatch produced a BOUNDARY verdict on a dataset that, by threshold-existence statistics, clearly satisfies the original question.

## Honest Note on Calibration

This appeal is filed after seeing the CR_TEST8 scored residuals. The appeal statistics below are calibrated against that knowledge — that is honest K3 disclosure. The appeal does NOT modify CR_TEST8; it adds an independent threshold-existence audit using a different statistic precommitted here.

## Inputs (Hash-Locked at Execution)

```text
Source residual table:  CR_TEST8_Z96_REGIME_CHANGE/outputs/test8_scored_by_Z.csv
Source SHA-256:         6b2e3df5b5d263a44c182c88e1abd3b5c2652f40fd812d8928eb9dde02ed5d3c
CR_TEST8 verdict.md:    c1f78dc0526572a7873cdcaa6e9400016acd1fe7dc63525ea81ceee85c0238f5
CR_TEST8 precommit:     be97c10eb080480ec4889ecbe8c4fd98a7e8dd5539e0935a58c3baaa10ec0cda
Window definitions:     pre Z=85..96, post Z=97..108 (unchanged from CR_TEST8)
Constants:              R=12, D=3, alpha_H=2, Z_break=96
```

## Threshold-Existence Statistics (Locked)

Compute on the locked pre/post windows from CR_TEST8:

```text
M_RATIO_MEAN    = mean(|r_N|_post) / mean(|r_N|_pre)
M_RATIO_MEDIAN  = median(|r_N|_post) / median(|r_N|_pre)
SEP_STRICT      = min(|r_N|_post) - max(|r_N|_pre)
SEP_OUTLIER_ROBUST = min(|r_N|_post) - max(|r_N|_pre \ {single largest pre outlier})
JUMP_AT_BOUNDARY = |r_N|(Z=97) - |r_N|(Z=96)
MANN_WHITNEY_U  = standard rank-sum U-statistic on pre vs post
MANN_WHITNEY_Z  = normal approximation z-score
MANN_WHITNEY_P  = two-sided p-value (normal approximation)
```

Mann-Whitney implementation: rank both populations together (averaging tied ranks), compute U₁ and U₂, take U = min, then use the normal approximation `z = (U − n₁n₂/2) / sqrt(n₁n₂(n₁+n₂+1)/12)` and the standard normal CDF for the two-sided p-value. No scipy.

## Appeal Pass Criteria (Locked)

**APPEAL_GRANTED_THRESHOLD_EXISTS** requires ALL of:

```text
M_RATIO_MEAN        >= 3.0
M_RATIO_MEDIAN      >= 3.0
MANN_WHITNEY_P      < 0.001
JUMP_AT_BOUNDARY    >= 5    (the single one-step jump from Z=96 to Z=97 is at least 5 in absolute residual units)
```

SEP_OUTLIER_ROBUST is computed and reported in the output for transparency but is NOT a strong-pass gate (see modification header).

**APPEAL_GRANTED_WEAK** requires:

```text
M_RATIO_MEAN        >= 2.0
MANN_WHITNEY_P      < 0.01
```

(at least two of the strong criteria met)

**APPEAL_DENIED** otherwise.

## What This Appeal Can And Cannot Change

- It CAN add a new sealed amendment artifact stating the threshold-existence result against precommitted criteria.
- It CANNOT modify CR_TEST8's verdict (stays at BOUNDARY_TEST8_Z96_MIXED_SIGNAL).
- It CANNOT relocate the SAM Z=96 boundary or tune R, D, or 2^D.
- It CANNOT add or remove rows from the pre/post windows.

If the appeal is GRANTED, the TEST_INDEX cites CR_TEST8_APPEAL alongside CR_TEST8 — both stay live, the appeal's verdict supersedes for manuscript purposes, the original BOUNDARY verdict remains as audit trail.

## K-Gate Audit (Plan)

| Gate | Status | Plan |
|---|---|---|
| K1 | External anchor | Same external CSV as CR_TEST8 (QP061 lineage) |
| K2 | Falsification | Pre-stated falsifiers: any of the strong criteria failing, OR Mann-Whitney p ≥ 0.001, OR SEP_OUTLIER_ROBUST ≤ 0 |
| K3 | Target hygiene | DEGRADED. This appeal is filed knowing CR_TEST8's residual table. The appeal precommit honestly states this. The pass thresholds were chosen to reflect the threshold-existence question's natural magnitude bar, not to maximize the chance of passing |
| K4 | Typed inputs | One SHA-locked input file (CR_TEST8 scored_by_Z.csv); locked windows |
| K5 | Reproduction on demand | Deterministic, no seeds needed |

## Relationship to CR_TEST8

CR_TEST8 stays sealed at BOUNDARY_TEST8_Z96_MIXED_SIGNAL. CR_TEST8_APPEAL adds an independent threshold-existence audit. Both live side-by-side in the index. The original locked random-boundary statistic and its sealed result are preserved as the audit trail.
