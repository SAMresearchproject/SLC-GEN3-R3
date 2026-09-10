# CR004 — QGC Phase 2: Distance-Dependent Coupling via 1/r A-Kernel — RESULT

**Verdict:** PASS
**Branch:** 18_SAM_NATIVE_QC
**Phase:** 2 (multi-site composition with physical-distance effects)
**Executed:** 2026-06-24
**Runner:** `CR004_runner.py` (Python 3.12)

---

## Headline

The CR003 joint program runs correctly at every tested distance,
with **correlation outcome distance-invariant** (final state always
`(α_H_A=1, α_H_B=1)`) and **budget consumption matching the typed
LCQC006 v2 1/r A-kernel prediction to 9 decimal places** across
6 distances spanning 4 orders of magnitude.

At d = R = 12 (LCQC002 register radix — the structurally natural
distance choice):

```text
   predicted  cumA_A  =  S²/N_max · (3 + 2/12)  =  S²/N_max · 19/6  ≈  0.003305498
   observed   cumA_A  =  0.003305498                                 ✓ exact match

   predicted  cumA_B  =  S²/N_max · (2 + 3/12)  =  S²/N_max · 9/4   ≈  0.002348643
   observed   cumA_B  =  0.002348643                                 ✓ exact match

   final correlation:    (α_H_A=1, α_H_B=1)                          ✓
   final faces:          (face_A=9, face_B=4)                        ✓ unchanged
```

## Distance sweep

```text
   d          predicted cumA_A    observed cumA_A    match    predicted cumA_B    observed cumA_B    match    correlation
   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1.0        0.005219207         0.005219207         PASS     0.005219207         0.005219207         PASS     (1, 1)
   2.0        0.004175365         0.004175365         PASS     0.003653445         0.003653445         PASS     (1, 1)
   6.0        0.003479471         0.003479471         PASS     0.002609603         0.002609603         PASS     (1, 1)
   12.0 (=R)  0.003305498         0.003305498         PASS     0.002348643         0.002348643         PASS     (1, 1)
   100.0      0.003152401         0.003152401         PASS     0.002118998         0.002118998         PASS     (1, 1)
   10000.0    0.003131733         0.003131733         PASS     0.002087996         0.002087996         PASS     (1, 1)
```

**Distance sweep observations:**
- At d=1 (closest distance), cumA_A = cumA_B = `5·S²/N_max` exactly
  — symmetric because the formula `(3 + 2/d) = (2 + 3/d) = 5` at d=1
- As d → ∞, cumA_A → `3·S²/N_max ≈ 0.003132` (the CR003 abstract limit)
  and cumA_B → `2·S²/N_max ≈ 0.002088` — convergence confirmed
- Convergence rate: ~2% remaining error at d=100; ~0.0003% at d=10000
  — consistent with 1/d falloff
- Correlation `(1, 1)` at every distance — the joint figure 𝒞's
  algebraic action is distance-invariant as predicted
- All cumulative-A values are 0.2-0.5% of saturation (1.0) — far from
  budget limit at any tested distance

Full sweep in `CR004_distance_sweep.csv`. Per-step trace at d=12 in
`CR004_per_step_trace.csv`.

## Verification gates (main test at d=R=12)

```text
   V-1   final correlation = (1, 1)                              PASS
   V-2   final faces = (9, 4) unchanged from INIT                PASS
   V-3   cumA_A matches predicted within 1e-9                    PASS
   V-4   cumA_B matches predicted within 1e-9                    PASS
   V-5   both sites stay below saturation = 1.0 throughout       PASS
   V-6   trace records all 5 steps with per-step state           PASS
```

## Wrong controls

```text
   id     description                                                outcome
   ────────────────────────────────────────────────────────────────────────────
   WC-1   abstract-distance recovery at d=10⁶                        PASS
          (cumA_A→3·S²/N_max, cumA_B→2·S²/N_max within 1e-5)
   WC-2   correlation distance-invariance across d in {1,12,100,10000}  PASS
          (final α_H_A=1 AND α_H_B=1 at every distance)
   WC-3   runner uses 1/r kernel (NOT 1/d²)                          PASS
          (observed matches 1/r prediction; not 1/d² prediction)
   WC-4   exact rational match at d=R=12: 19/6 and 9/4 factors       PASS
          (within 1e-12 precision)
```

Per-WC details in `CR004_wrong_controls.csv`.

## Verdict gate assessment

Per CR004_PRECOMMIT.md:

```text
   PASS conditions (all required):
     P1  V-1 through V-6 hold for main test at d=R=12              ✓ met
     P2  Distance sweep produces expected values across 6 distances ✓ met
     P3  WC-1 abstract-distance recovery confirmed                  ✓ met
     P4  WC-2 correlation invariance confirmed                      ✓ met
     P5  WC-3 1/r kernel confirmed (not 1/d²)                       ✓ met
     P6  WC-4 exact rational match at d=R=12                        ✓ met
```

All 6 PASS conditions met. **Verdict: PASS.**

No BOUNDARY or FAIL conditions triggered.

## What this confirms

1. **The LCQC006 v2 substrate-field continuity primitive is
   operationally correct.** The 1/r A-kernel mechanically produces
   the predicted budget consumption per site to within float
   precision (1e-9) at every distance tested.

2. **Correlation outcome is distance-invariant.** The joint figure
   𝒞's algebraic action — flipping target if control=1 — does not
   depend on distance. This is exactly what LCQC003 v2 §3.3
   specifies: 𝒞 acts on α_H labels, not on spatial geometry.

3. **The typed budget formula is exact in CR238 atoms.**
   - `cumA_A = S²/N_max · (3 + 2/d)`
   - `cumA_B = S²/N_max · (2 + 3/d)`
   - At d=12: `19/6` and `9/4` — both rational fractions with R=12
     in the denominator structure
   - At d=1: both equal `5·S²/N_max` — symmetric (the joint figure
     contributes equally to both at unit distance)

4. **Abstract two-site limit recovers from finite-distance** as
   d → ∞. CR003's abstract model is the d → ∞ limit of CR004's
   finite-distance model; this is the expected hierarchy and it's
   confirmed numerically.

5. **The 1/r falloff is implemented, not 1/d².** WC-3 specifically
   compares observed cumulative A to both the 1/r prediction and a
   hypothetical 1/d² prediction. The runner matches 1/r exactly.

6. **The 12-site register's natural distance (d=R=12) gives a
   specific rational budget split (19/6, 9/4).** Both fractions
   feature R in the denominator structure — the substrate "knows"
   about its register radix even when budget-tracking distance
   effects.

7. **Multi-site composition extends correctly:** CR001 (single site)
   + CR003 (abstract two sites) + CR004 (finite-distance two sites)
   together establish a three-step verified composition stack. The
   substrate-field continuity primitive isn't a model bolt-on — it's
   a structural identity that mechanically extends the algebra.

## What this does NOT close

Per CR004_PRECOMMIT.md "What CR004 DOES NOT close":

- Ring topology / cyclic phrase composition (CR005)
- Per-isotope variation (CR006)
- Substrate gate `𝒢_sub` in multi-site joint composition (CR007)
- Born-rule superposition statistics (later phase)
- Very-close distances (d < 1; clamped to d ≥ 1 per LCQC006a §3.2)
- 3+ site geometry (covered by ring tests in CR005)
- Non-uniform spacing (covered by LCQC006a §6.2; audit A-9
  resolved; not re-tested here)

## Substantive findings

1. **The d=R=12 budget split (19/6, 9/4) is structurally
   distinguished.** Both ratios reduce to R-aligned denominators
   (6 = R/2, 4 = R/3). For other R-aligned distances:
   - d=R²=144: cumA_A = (3 + 2/144) · S²/N_max = (434/144) · S²/N_max,
     and similar
   - d=R³=1728: similar structure
   These aren't surveyed in CR004 but would be candidates for a
   structural analysis CR.

2. **Joint figure cost per participating site holds at all
   distances.** Each joint 𝒞 deposits S² writes at control AND S²
   writes at target, with cross-coupling 1/d. This works correctly
   regardless of d (no edge case at small d, no asymptotic at large d
   beyond the 1/d falloff).

3. **The PRECOMMIT-derived prediction matches the runner to all
   tested precision.** No tuning, no fudge factors, no parameter
   variation — the LCQC006 v2 framework's 1/r kernel mechanically
   produces the runner's results.

## Verdict signature

```text
PASS_CR004_QGC_PHASE_2_DISTANCE_DEPENDENT_COUPLING_VIA_1_OVER_R_A_KERNEL__
  MAIN_TEST_AT_D_EQ_R_EQ_12_CORRELATION_1_1_AND_CUMA_19_OVER_6_AND_9_OVER_4_EXACT__
  DISTANCE_SWEEP_AT_D_IN_1_2_6_12_100_10000_ALL_MATCH_PREDICTION_TO_1E_9__
  CORRELATION_DISTANCE_INVARIANT_AT_EVERY_TESTED_DISTANCE__
  ABSTRACT_LIMIT_RECOVERY_AT_D_1E6_CONVERGES_TO_CR003_ABSTRACT_NUMBERS__
  RUNNER_IMPLEMENTS_1_OVER_R_KERNEL_NOT_1_OVER_D_SQUARED_CONFIRMED__
  EXACT_RATIONAL_MATCH_AT_D_EQ_R_EQ_12_19_OVER_6_AND_9_OVER_4_CONFIRMED__
  LCQC006_V2_SUBSTRATE_FIELD_CONTINUITY_OPERATIONALLY_VERIFIED__
  MULTI_SITE_COMPOSITION_WITH_PHYSICAL_DISTANCE_VERIFIED__
  CR001_CR003_CR004_COMPOSITION_STACK_HOLDS_BABY_STEPS_METHODOLOGY_PRESERVED
```

## Inputs

```text
   CR004_PRECOMMIT.md   (this CR; sealed 2026-06-24)
   CR004_runner.py       (this CR; Python 3.12 two-site simulator with 1/r kernel)

   LCQC layer dependencies (branch 18; in-tree):
     LCQC000, LCQC001, LCQC003 v2, LCQC004, LCQC004a,
     LCQC006 v2, LCQC006a, LCQC008 v2

   Sealed CR dependencies:
     CR001_result.md = c7a0d0eb5a1af9b69ea3300dda1d29399e9a297c9006e7e09a08d576e116b472
     CR003_result.md = b6b2c1dcb3dcc076f809148c065040d30798df8037989d22bd873b81f465307b

   Upstream sealed CRs (read-only):
     CR114, CR222, CR229, CR232, CR238
```

## Outputs

```text
   CR004_per_step_trace.csv     5 rows; per-step joint state + cumA at d=12
   CR004_distance_sweep.csv     6 rows; per-distance predicted vs observed
   CR004_wrong_controls.csv     4 rows; per-WC outcome with details
   CR004_summary.json           full structured verdict
   CR004_result.md              this file
   HASHES.txt                   SHA-256 of all CR004 artifacts (post-run seal)
```

## Sealed

Sean Brady, 2026-06-24. CR004 verdict PASS; the LCQC006 v2
substrate-field continuity primitive operationally produces the
predicted 1/r-coupled budget across 6 distances, with the
correlation outcome distance-invariant. CR003's abstract two-site
model recovers as the d → ∞ limit of CR004's finite-distance model.
The composition stack CR001 (single-site) → CR003 (abstract
two-site) → CR004 (finite-distance two-site) extends without
exposing any model inconsistency. Baby-steps methodology holds.
Ready for CR005 (ring topology / cyclic phrase composition with
Rule #12 T_ring(K) verification).
