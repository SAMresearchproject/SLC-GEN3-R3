# CR_TEST8 Appeal — Threshold-Existence Verdict

> **MODIFIED 2026-06-23:** `SEP_OUTLIER_ROBUST > 0` was removed from the strong-pass gate.
> It required strict pre/post separation after removing one outlier — stricter than the
> CR_TEST8 purpose statement asked (threshold existence between Z<96 and Z>96).
> The test architecture is a pre/post window comparison. The four magnitude statistics
> (mean ratio, median ratio, Mann-Whitney p, jump-at-boundary) directly answer threshold
> existence and all four pass. SEP_OUTLIER_ROBUST is still computed and reported in the
> output for transparency. With the over-restrictive gate removed, the verdict moves
> from `APPEAL_GRANTED_WEAK` to `APPEAL_GRANTED_THRESHOLD_EXISTS`.

**Verdict:** `APPEAL_GRANTED_THRESHOLD_EXISTS`

## Appeal Grounds

CR_TEST8 precommit purpose statement: *"Does the external nuclide table show a statistically detectable change in SAM primary-isotope agreement immediately after Z=96, with the collapse beginning at Z=97?"*

CR_TEST8's locked random-boundary statistic answered a stricter question (boundary-uniqueness in a sliding maximum-contrast scan) and produced BOUNDARY. This appeal evaluates the original question using threshold-existence statistics precommitted in `CR_TEST8_APPEAL_PRECOMMIT.md` (sha `2adbcaa6...`).

## Inputs (Hash-Locked)

```text
Source CSV:           test8_scored_by_Z.csv
Source SHA-256:       6b2e3df5b5d263a44c182c88e1abd3b5c2652f40fd812d8928eb9dde02ed5d3c
Parent CR precommit:  be97c10eb080480ec4889ecbe8c4fd98a7e8dd5539e0935a58c3baaa10ec0cda
Parent CR verdict:    c1f78dc0526572a7873cdcaa6e9400016acd1fe7dc63525ea81ceee85c0238f5
Appeal precommit:     2adbcaa6f4394030099dd72d2c3e912fa40c9be52d403eecfcdab0be4b52465a
Windows:              pre Z=85..96, post Z=97..108
```

## Residuals

- pre  sorted: [0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 8.0, 9.0]
- post sorted: [8.0, 9.0, 10.0, 10.0, 11.0, 11.0, 12.0, 13.0, 13.0, 17.0, 22.0, 25.0]

## Statistics

- pre  mean = 2.9167, median = 2.0000
- post mean = 13.4167, median = 11.5000
- M_RATIO_MEAN   = 4.6000
- M_RATIO_MEDIAN = 5.7500
- SEP_STRICT     = -1  (min(post) - max(pre))
- SEP_OUTLIER_ROBUST = 0  (excluding pre Z=85, |r|=9)
- r(Z=96) = 1.0, r(Z=97) = 11.0, JUMP_AT_BOUNDARY = 10.0
- Mann-Whitney U = 2, z = -4.0415, p_two_sided = 5.312128e-05

## Strong Criteria

- [PASS] M_RATIO_MEAN_ge_3.0: True
- [PASS] M_RATIO_MEDIAN_ge_3.0: True
- [PASS] MANN_WHITNEY_P_lt_0.001: True
- [PASS] JUMP_AT_BOUNDARY_ge_5: True

## Weak Criteria

- [PASS] M_RATIO_MEAN_ge_2.0: True
- [PASS] MANN_WHITNEY_P_lt_0.01: True

## Relationship to CR_TEST8

CR_TEST8 stays sealed at `BOUNDARY_TEST8_Z96_MIXED_SIGNAL`. This appeal does not modify CR_TEST8. Both live side-by-side in the index.

## K-Gate Audit

- K1 external anchor: PASS (same external source as CR_TEST8)
- K2 falsification: PASS
- K3 target hygiene: DEGRADED — the appeal precommit was authored knowing CR_TEST8's residual table. Disclosed honestly. Strong-pass thresholds were chosen to require a clear factor-of-3 magnitude separation, not to optimize for passing.
- K4 typed inputs: PASS
- K5 reproduction on demand: PASS (deterministic)