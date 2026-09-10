# CR003 — QGC Phase 2: Joint Figure 𝒞 Correlation End-to-End — RESULT

**Verdict:** PASS
**Branch:** 18_SAM_NATIVE_QC
**Phase:** 2 (first multi-site / joint composition test)
**Executed:** 2026-06-24
**Runner:** `CR003_runner.py` (Python 3.12)

---

## Headline

The QGC's joint figure `𝒞` from LCQC003 v2 §3.3 composes correctly
with the binary flip `B` and PUBLISH primitives on two abstract
sites. The locked program

```text
   INIT site_A (face=9, α_H=0, resolved)
   INIT site_B (face=4, α_H=0, resolved)
   → B(A) → 𝒞(A→B) → PUBLISH(A) → PUBLISH(B)
```

produces the correlated output **(α_H_A=1, α_H_B=1)**, with all 5
per-step states matching the locked expected state exactly. Per-site
budget consumption is exactly the predicted `3·S² = 192` writes at
site_A and `2·S² = 128` writes at site_B (0.31% and 0.21% of N_max
respectively). All 4 wrong controls produce their predicted broken
outputs.

## Main program — per-step trace

```text
   step    op             face_A  α_H_A  status_A    wA       face_B  α_H_B  status_B    wB
   ──────────────────────────────────────────────────────────────────────────────────────────
   0       INIT             9       0    resolved      0         4       0    resolved      0
   1       B-A              9       1    resolved     64         4       0    resolved      0
   2       𝒞(A→B)           9       1    resolved    128         4       1    resolved     64
   3       PUBLISH(A)       9       1    resolved    192         4       1    resolved     64
   4       PUBLISH(B)       9       1    resolved    192         4       1    resolved    128
```

The joint figure step (step 2) is where correlation is created:
control α_H_A=1 from step 1 triggers `𝒞` to apply B to target site_B,
flipping α_H_B from 0 to 1. After step 2, the two sites are
correlated (both at α_H=1).

Full trace in `CR003_per_step_trace.csv`.

## Verification gates

```text
   V-1   all per-step (face, α_H, status, budget) match locked   PASS
   V-2   budget stayed under N_max throughout                    PASS
   V-3   final correlation (α_H_A=1, α_H_B=1)                    PASS
   V-4   final faces unchanged from INIT                         PASS
   V-5   final cumulative writes match (3·S² for A, 2·S² for B)  PASS
```

## Wrong controls

```text
   id     description                                         predicted     observed     verdict
   ───────────────────────────────────────────────────────────────────────────────────────────────
   WC-1   skip B on control (no flip; α_H_A stays 0)          (0, 0)        (0, 0)        PASS
   WC-2   B(A) AFTER 𝒞 (𝒞 reads α_H=0 before flip)            (1, 0)        (1, 0)        PASS
   WC-3   swap control/target (𝒞 with control=B, target=A)    (1, 0)        (1, 0)        PASS
   WC-4   apply 𝒞 twice (𝒞² = identity on joint state)        (1, 0)        (1, 0)        PASS
```

Per-WC details in `CR003_wrong_controls.csv`.

## Verdict gate assessment

Per CR003_PRECOMMIT.md:

```text
   PASS conditions (all required):
     P1  V-1 through V-5 hold for main program                  ✓ met
     P2  Each WC produces predicted broken output                ✓ met
     P3  Per-step trace CSV produced (5 rows)                    ✓ met
     P4  Wrong control CSV produced (4 WC outcomes)              ✓ met
     P5  Cumulative budget per site matches predicted exactly    ✓ met
     P6  No exceptions during execution                          ✓ met
```

All 6 PASS conditions met. **Verdict: PASS.**

No BOUNDARY or FAIL conditions triggered.

## What this confirms

1. **Joint figure 𝒞 composes correctly** with B and PUBLISH at the
   abstract two-site level. Control-conditional flip works as
   specified.
2. **𝒞 reads the control's label at fire time** (WC-2 confirms: B
   applied AFTER 𝒞 doesn't affect what 𝒞 saw earlier — the
   composition is temporally ordered as expected).
3. **𝒞 is asymmetric in control/target roles** (WC-3 confirms:
   swapping control and target gives a different result because the
   control's label is what determines the flip; sites are not
   interchangeable).
4. **𝒞² = identity on joint state when control is fixed** (WC-4
   confirms: two consecutive 𝒞 applications with the same control
   value return the target to its original state — involution
   property holds at the joint-state level).
5. **Joint figure cost = S² writes per participating site** (per
   LCQC004a structural choice + CR003 implementation): the joint
   figure consumes gate-equivalent budget at BOTH the control and
   target sites, as specified in PRECOMMIT §3.
6. **Per-site coherence budget remains independent in the abstract
   model**: site_A and site_B each have their own N_max ceiling; the
   joint figure consumes S² of each site's budget, not a shared budget.
7. **Face indices are preserved by 𝒞** (the joint figure acts only on
   α_H labels, never on face indices — V-4 confirms).
8. **LCQC003 v2 algebra extends to multi-site correctly**: the
   unconditional group structure + joint partial algebra composition
   works as the layer specifies.

## What this does NOT close

Per CR003_PRECOMMIT.md "What CR003 DOES NOT close":

- Physical distance effects between sites (LCQC006 v2 1/r A-kernel
  cross-coupling) — abstract sites have no spatial-distance behavior
- Born-rule superposition statistics (deterministic-prep states only)
- Ring topology / cyclic-phrase composition (no playhead)
- Per-isotope variation (balanced anchor implicit)
- Substrate gate `𝒢_sub` in joint composition (single-site `𝒢_sub`
  verified in CR001; multi-site `𝒢_sub` is a separate test)
- External-benchmark comparison (out of scope by R-3 discipline)

These are each candidates for subsequent CRs (CR004, CR005, ...) as
the operational stack scales one dimension at a time per the
baby-steps methodology.

## Substantive findings

1. **The joint figure cost model holds in operation.** PRECOMMIT
   stipulated `𝒞` costs S² writes at EACH participating site (control
   and target). The runner implemented this and the budget accounting
   matched predicted values to the bit. The joint-figure-as-multi-site-
   gate framework is consistent.

2. **CR001 + CR003 together establish:** single-site composition
   works (CR001 covered 𝒢_sub², B², MEASURE) AND two-site joint
   composition works (CR003 covers 𝒞 with B and PUBLISH). The
   operational stack composes for both single-site and abstract
   two-site programs.

3. **What's not yet operationally tested** that COULD reveal issues
   in subsequent CRs: physical-distance budget interaction (CR004
   candidate), ring topology / playhead composition (CR005), per-
   isotope coherence scaling (CR006), substrate gate `𝒢_sub` in
   joint composition (CR007).

## Verdict signature

```text
PASS_CR003_QGC_PHASE_2_JOINT_FIGURE_C_CORRELATION_END_TO_END__
  MAIN_PROGRAM_INIT_A_INIT_B_B_A_C_A_B_PUBLISH_A_PUBLISH_B_RETURNS_ALPHA_H_A_1_ALPHA_H_B_1__
  CORRELATION_CREATED_BY_JOINT_FIGURE_C_AT_STEP_2_AS_PREDICTED__
  ALL_5_PER_STEP_STATES_MATCH_LOCKED_EXPECTED_EXACTLY__
  PER_SITE_BUDGET_CONSUMPTION_MATCHES_PREDICTED_3_S_SQUARED_AT_A_AND_2_S_SQUARED_AT_B__
  ALL_4_WRONG_CONTROLS_PRODUCE_PREDICTED_BROKEN_OUTPUTS__
  WC1_SKIP_B_CONTROL_NO_CORRELATION__
  WC2_B_AFTER_C_TEMPORAL_ORDER_PRESERVED__
  WC3_SWAP_CONTROL_TARGET_ASYMMETRY_CONFIRMED__
  WC4_C_TWICE_INVOLUTION_ON_JOINT_STATE__
  LCQC003_V2_JOINT_PARTIAL_ALGEBRA_OPERATIONAL_FOUNDATION_VERIFIED__
  MULTI_SITE_COMPOSITION_FRAMEWORK_EXTENDS_FROM_CR001_SINGLE_SITE__
  PHASE_2_FIRST_MULTI_SITE_TEST_PASS_BABY_STEPS_METHODOLOGY_HOLDS
```

## Inputs

```text
   CR003_PRECOMMIT.md   (this CR; sealed 2026-06-24)
   CR003_runner.py       (this CR; Python 3.12 two-site abstract simulator)

   LCQC layer dependencies (branch 18; in-tree):
     LCQC000, LCQC001, LCQC003 v2, LCQC004, LCQC004a, LCQC008 v2

   Sealed CR dependency:
     CR001_result.md  =  c7a0d0eb5a1af9b69ea3300dda1d29399e9a297c9006e7e09a08d576e116b472

   Upstream sealed CRs (read-only):
     CR114, CR222, CR229, CR232, CR238
```

## Outputs

```text
   CR003_per_step_trace.csv     5 rows; main program per-step joint state
   CR003_wrong_controls.csv     4 rows; per-WC outcome
   CR003_summary.json           full structured verdict
   CR003_result.md              this file
   HASHES.txt                   SHA-256 of all CR003 artifacts (post-run seal)
```

## Sealed

Sean Brady, 2026-06-24. CR003 verdict PASS; the joint figure `𝒞`
composes correctly with B and PUBLISH at the abstract two-site level.
LCQC003 v2's joint partial-algebra extends operationally from single-
site (CR001) to two-site (CR003) without exposing any composition
issue. Baby-steps methodology holds: one new primitive per CR,
verified before the next dimension is added. Ready for CR004 (the
next baby step — probably physical-distance effects via LCQC006 v2
1/r kernel between two sites).
