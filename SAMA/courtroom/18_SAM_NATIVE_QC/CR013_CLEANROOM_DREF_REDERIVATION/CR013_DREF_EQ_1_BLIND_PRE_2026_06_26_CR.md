# CR013 d_ref = 1 Blind Pre-2026-06-26 CR

**Prepared:** 2026-07-03  
**Task preflight:** `artifacts/preflight_filled/PREFLIGHT_20260703_121748_no_script.md`  
**Preflight class:** `CONSTRUCTIVE_NEW_WORK`  
**Object under review:** `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_DREF_EQ_1_SOURCE_BOUNDED_DERIVATION.md`  
**Blind boundary:** no source/context evidence created or changed on or after 2026-06-26 admitted.  

## Boundary

This CR treats the target derivation as the object under review. It does not
admit nearby post-cutoff support files as source evidence.

The historical source snapshot used for source evidence is:

```text
commit = 0cc5212671c7d69e20fa1c6159ff056e3bfbbbc1
commit_date = 2026-06-25 21:36:14 -0500
subject = 062526
cutoff = before 2026-06-26 00:00:00 -0500
```

The following current/untracked files are explicitly nonadmitted as source
evidence for this blind CR:

```text
18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_DREF_EQ_1_PRIOR_TESTING_SUPPORT.md
18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_APPEAL_PRE_2026_06_26_EVIDENCE_SCAN.md
18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_COLLAPSE_CONDITION_CANDIDATE_SWEEP.md
18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_COLLAPSE_CONDITION_CANDIDATE_SWEEP_ADDENDUM.md
18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_COLLAPSE_CONDITION_CANDIDATE_SWEEP_QP_STAM.md
```

## Admitted Source Set

All admitted source references below are from commit
`0cc5212671c7d69e20fa1c6159ff056e3bfbbbc1`.

```text
18_SAM_NATIVE_QC/LCQC006_NETWORKING_AND_RING_TOPOLOGY/LCQC006_NETWORKING_AND_RING_TOPOLOGY_v2.md
18_SAM_NATIVE_QC/CR002_T2_PRESCREENING_AND_K1_ENVELOPE/CR002_PRECOMMIT.md
18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_PRECOMMIT.md
18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_result.md
18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_summary.json
18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_distance_sweep.csv
18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_wrong_controls.csv
18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/HASHES.txt
18_SAM_NATIVE_QC/SLC_UNITS_AND_NORMALIZATION.md
18_SAM_NATIVE_QC/SLC_STATUS_MATRIX.csv
18_SAM_NATIVE_QC/SLC_ARCHITECTURE_REBASE_AND_COMPLETION_CAMPAIGN.md
```

CR004 artifact hashes from the pre-cutoff `HASHES.txt`:

```text
CR004_PRECOMMIT.md       5d565d113f6f8897d8173f99d54aebeaf3e933655b85ee2d4f88f1ab3e6e833c
CR004_result.md          5d5d1153d8b1b9074b13274a474fabca6ac14f57abbfd445eb9b5b093f6df33e
CR004_summary.json       50729c67edecb00f646739513fe9f42e180487acb1b49f5439f721a4bed30ada
CR004_distance_sweep.csv fd83413915fbc2acd61d1ddd4ae657a1419681891a32a385c09ca80bb687f197
CR004_wrong_controls.csv 285a1317ed3c236be3c9667e6f07f6970cb77818a36c5758956d701abd4dc4e5
CR004_runner.py          3a25c2ffb8e5b47ccfec4fcb9ab83ffed6d6bba466bba10c40defe435b825cbe
```

## Question

Can the target derivation's claim

```text
d_ref_norm = 1
```

be supported from pre-2026-06-26 sources only, and does the source set support
any absolute SI value for `d_ref`?

## Findings

### F1 - Normalized `d_ref = 1` is source-supported

CR004_PRECOMMIT declares the locked distance-dependent budget rule:

```text
site Y receives A-shift contribution = (1/N_max) * (d_ref / d(X, Y))
where d_ref = unit spacing (chosen = 1)
      d(X, Y) = distance between sites X and Y (in d_ref units)
      d(X, X) = d_ref
```

This directly supports the target derivation's normalized conclusion:

```text
d_ref_norm = 1
```

The status is not an independently discovered meter-scale constant. It is the
declared CR004/SLC normalized unit-spacing convention used by the simulator
and by the CR004 precommit.

### F2 - The ratio reduction is valid under the admitted convention

LCQC006 v2 gives the substrate-field continuity form:

```text
A_field at site j from source-pressure at site i
  = A_0 * (d_ref / d(i, j))
```

CR002 also carries the same candidate kernel form:

```text
A(r) = A_0 * d_ref/r
```

Once CR004 fixes `d_ref` as the unit spacing and measures `d(X, Y)` in
`d_ref` units, the target derivation's normalized ratio step is valid:

```text
d_ref / d_abs(X, Y)
  = L_ref / (delta(X, Y) * L_ref)
  = 1 / delta(X, Y)
```

This is a normalization result: the absolute reference length cancels from the
dimensionless simulator law.

### F3 - CR004 supports the operational 1/r kernel, not 1/d^2

CR004_result records PASS across the six-distance sweep
`d = 1, 2, 6, 12, 100, 10000`, with budget consumption matching the typed
LCQC006 v2 `1/r` A-kernel prediction. The pre-cutoff `CR004_distance_sweep.csv`
shows all six rows passing for both `cumA_A` and `cumA_B`.

CR004_wrong_controls records WC-3 as PASS:

```text
runner uses 1/r kernel (NOT 1/d^2)
matches_correct = true
matches_wrong = false
```

Therefore the target's use of the inverse-distance law is supported by the
pre-cutoff source set.

### F4 - The d = 1 equal-budget row is supported

The target derivation states that, at `delta = 1`,

```text
3 + 2/d = 2 + 3/d = 5
cumA_A = cumA_B = 5 * S^2 / N_max
```

CR004_distance_sweep at `d = 1.0` records equal predicted and observed values:

```text
predicted_cumA_A = observed_cumA_A = 0.005219206680584551
predicted_cumA_B = observed_cumA_B = 0.005219206680584551
correlation_AB = (1, 1)
```

That row supports the target derivation's unit-spacing budget equality.

### F5 - Absolute SI length is not source-supported

SLC_UNITS_AND_NORMALIZATION quarantines physical distance and coupling
magnitude:

```text
coupling strength J(r): shape only (1/r); no magnitude
distance r: declared in CR004 simulator only as logical
LCQC018 derives physical magnitude
```

SLC_STATUS_MATRIX likewise records:

```text
CR004 confirms 1/r budget rule at simulator level
do not call CR004 a physical 1/r measurement
physical magnitude of the 1/r coupling: OPEN
do not quote a physical 1/r coupling strength
```

SLC_ARCHITECTURE_REBASE_AND_COMPLETION_CAMPAIGN also marks CR004 as an
internal software result, not physical validation, and says the direct physical
magnitude of the `1/r` coupling is not established.

Therefore the target derivation correctly refuses to derive:

```text
d_ref_abs in SI meters
```

## Companion Source-Boundary Correction

The target derivation initially said its input boundary was:

```text
CR013_DREF_EQ_1_PRIOR_TESTING_SUPPORT.md only, after preflight.
```

For a blind pre-2026-06-26 CR, that support note is nonadmitted because it is a
current untracked post-cutoff file. The derivation's mathematical conclusion
survives, and the source-boundary statement has been corrected in the target
file so it no longer cites the post-cutoff support note as admitted evidence.

Applied replacement:

```text
Input boundary: pre-2026-06-26 sources only, using git snapshot
0cc5212671c7d69e20fa1c6159ff056e3bfbbbc1. The post-cutoff CR013 support note
is excluded from source evidence for the blind CR.
```

## Verdict

```text
CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR_VERDICT:
  PASS_NORMALIZED_DREF_EQ_1_AS_CR004_UNIT_SPACING_CONVENTION
  PASS_1_OVER_R_OPERATIONAL_KERNEL_SUPPORTED_BY_PRE_CUTOFF_CR004
  PASS_D_EQ_1_EQUAL_BUDGET_ROW_SUPPORTED
  PASS_ABSOLUTE_SI_DREF_NOT_DERIVED
  PASS_SOURCE_BOUNDARY_CORRECTED_TO_PRE_CUTOFF_SNAPSHOT
```

Plain readout:

The derivation is good if stated as a normalized SLC/CR004 unit-spacing
derivation. Pre-cutoff sources support `d_ref_norm = 1`, support the operational
`1/r` coupling shape, and support the `d = 1` equal-budget row. They do not
support any absolute SI length for `d_ref`. The source-boundary hygiene cleanup
has been applied to the target derivation: the post-cutoff support note is
excluded from the blind source set.
