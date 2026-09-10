# CR004 — QGC Phase 2: Distance-Dependent Coupling via 1/r A-Kernel

**Branch:** 18_SAM_NATIVE_QC
**Phase:** 2 (multi-site composition with physical-distance effects)
**Sealed by:** Sean Brady, 2026-06-24

---

## Question

Does the joint program from CR003 produce the same correlated output
when the two sites are at finite physical distance d, with budget
consumption tracking the LCQC006 v2 substrate-field continuity 1/r
A-kernel? Specifically:

```text
   Does the program

      INIT site_A (face=9, α_H=0, resolved) at position 0
      INIT site_B (face=4, α_H=0, resolved) at position d
      → B(A) → 𝒞(A→B) → PUBLISH(A) → PUBLISH(B)

   produce:
     (1) the same correlated final state (α_H_A=1, α_H_B=1) at every
         distance d (correlation is distance-invariant)
     (2) per-site cumulative-A budget that matches the typed formula
         derived from LCQC006 v2's 1/r kernel:
             cumulative_A(site_A) ∝ 3·S² + 2·S²/d
             cumulative_A(site_B) ∝ 2·S² + 3·S²/d
     (3) convergence to CR003's abstract-distance result as d → ∞
```

This is CR003 with physical distance added back — testing whether the
abstract two-site model used in CR003 generalizes correctly to
realistic site geometry with substrate-field cross-coupling.

## Honest framing

CR004 verifies **distance-dependent budget consumption** matches
LCQC006 v2's typed 1/r A-kernel prediction, while confirming the
**algebraic correlation outcome is distance-invariant** (the joint
figure 𝒞 produces its predicted joint state regardless of d).

What CR004 deliberately DOES NOT test (deferred to subsequent CRs):

- Ring topology composition / cyclic playhead (CR005)
- Per-isotope variation (CR006)
- Substrate gate `𝒢_sub` in multi-site joint composition (CR007)
- Born-rule superposition statistics (later phase)
- Non-uniform spacing (covered by LCQC006a §4 / audit A-9
  resolution; not re-tested here)

## Locked substrate atoms (read-only)

```text
   S² = 64                       writes per figure (LCQC004a)
   N_max = 61,312                per-site coherence ceiling (LCQC004)
   A_0 = 1/(12π) ≈ 0.02653       per-write A-contribution at write site
                                  (CR238)
   1/(N_max · d) = per-write A-contribution at distance d
                   in normalized "saturation = 1.0" units
                   (LCQC006a §3.2)
```

## Locked distance-dependent budget formula

For each substrate write event at site X (with cost = 1 substrate
write, normalized contribution = 1/N_max at the write site):

```text
   site Y receives A-shift contribution = (1/N_max) · (d_ref / d(X, Y))

   where d_ref = unit spacing (chosen = 1)
         d(X, Y) = distance between sites X and Y (in d_ref units)
         d(X, X) = d_ref (self-reference; LCQC006a self_distance choice)
```

For a single-site figure at site X (cost = S² writes):
```text
   ΔcumA at X     =  S² / N_max
   ΔcumA at Y≠X   =  S² / (N_max · d(X, Y))
```

For the joint figure 𝒞 at sites (control, target) — both incur S²
writes per LCQC004a's joint-figure-cost-per-participating-site choice:
```text
   ΔcumA at control  =  S²/N_max (own writes) + S²/(N_max · d) (target's writes)
                     =  S²/N_max · (1 + 1/d)
   ΔcumA at target   =  S²/N_max · (1 + 1/d)        (symmetric)
```

For our 7-op main program at distance d between site_A and site_B:

```text
   site_A cumulative_A     site_B cumulative_A
   =  (S²/N_max) · BUDGET_A   (S²/N_max) · BUDGET_B

   where:
     BUDGET_A = 3 + 2/d        (3 own-site figures + 2 cross-coupled from B)
     BUDGET_B = 2 + 3/d        (2 own-site figures + 3 cross-coupled from A)
```

Breakdown:
```text
   site_A: B(A) at A (own)            +S²/N_max
           𝒞 at A (own)               +S²/N_max
           𝒞 at B (cross)             +S²/(N_max · d)
           PUBLISH(A) at A (own)      +S²/N_max
           PUBLISH(B) at B (cross)    +S²/(N_max · d)
           ────────────────────────────
           total                       S²/N_max · (3 + 2/d)

   site_B: B(A) at A (cross)          +S²/(N_max · d)
           𝒞 at A (cross)             +S²/(N_max · d)
           𝒞 at B (own)               +S²/N_max
           PUBLISH(A) at A (cross)    +S²/(N_max · d)
           PUBLISH(B) at B (own)      +S²/N_max
           ────────────────────────────
           total                       S²/N_max · (2 + 3/d)
```

## Locked program (main test at d = R = 12)

The MAIN test runs the same CR003 program but at distance d = R = 12
(the LCQC002 register radix — a structurally natural distance choice).

```text
   step    op                           predicted ΔcumA_A    predicted ΔcumA_B
   ──────────────────────────────────────────────────────────────────────────
   0       INIT_A (face=9, α_H=0)        —                    —
   0       INIT_B (face=4, α_H=0)        —                    —
   1       B(A)                          S²/N_max             S²/(N_max·12)
   2       𝒞(A → B)                      S²/N_max + S²/(N_max·12)  ... same
   3       PUBLISH(A)                    S²/N_max             S²/(N_max·12)
   4       PUBLISH(B)                    S²/(N_max·12)        S²/N_max
   ──────────────────────────────────────────────────────────────────────────
   FINAL   cumulative_A_A = S²/N_max · (3 + 2/12) ≈ 0.003304
           cumulative_A_B = S²/N_max · (2 + 3/12) ≈ 0.002351
           correlation:    (α_H_A=1, α_H_B=1)
           faces:          (face_A=9, face_B=4) unchanged
```

## Locked verification (main test at d=12)

```text
V-1   Final correlation is (α_H_A=1, α_H_B=1)
V-2   Final faces are (face_A=9, face_B=4) — unchanged from INIT
V-3   Cumulative A at site_A matches predicted value within 1e-9
       (3.167 · S²/N_max ≈ 3.30396e-3)
V-4   Cumulative A at site_B matches predicted value within 1e-9
       (2.25  · S²/N_max ≈ 2.34896e-3)
V-5   Cumulative A at both sites stays < 1.0 (saturation = 1.0)
       throughout execution
V-6   Per-step trace records the predicted ΔcumA values for both sites
       at every step
```

## Locked distance sweep

The runner additionally executes the same program at multiple
distances and verifies the predicted scaling:

```text
   d (spacing units)    expected cumA_A          expected cumA_B
   ──────────────────────────────────────────────────────────────
        1               5 · S²/N_max ≈ 0.00522    5 · S²/N_max ≈ 0.00522
        2               4 · S²/N_max ≈ 0.00418    3.5 · S²/N_max ≈ 0.00366
        6               3.333 · S²/N_max ≈ 0.00348  2.5 · S²/N_max ≈ 0.00261
       12 (= R)         3.167 · S²/N_max ≈ 0.00330  2.25 · S²/N_max ≈ 0.00235
      100               3.02 · S²/N_max ≈ 0.00315   2.03 · S²/N_max ≈ 0.00212
    10000               ≈ 3.0 · S²/N_max ≈ 0.00313  ≈ 2.0 · S²/N_max ≈ 0.00209
```

Distance sweep convergence check: at large d, cumA_A → 3·S²/N_max
and cumA_B → 2·S²/N_max (the CR003 abstract-distance numbers).

## Wrong controls

```text
WC-1   (abstract-distance limit recovery) Run with d = 1,000,000
       (effectively infinite). Expected: cumA_A and cumA_B converge
       to CR003's abstract numbers (3·S²/N_max and 2·S²/N_max)
       within 1e-5.

WC-2   (correlation distance-invariance) Run main program at d=1,
       d=12, d=100, d=10000. Expected: final correlation is
       (1, 1) at every distance — outcome does NOT depend on d.

WC-3   (wrong distance law — 1/d² instead of 1/d) Hypothetical
       computation: if the kernel were 1/d² instead of 1/d, at d=12,
       cross-coupling per write would be 1/(N_max · 144) instead of
       1/(N_max · 12). Expected:
       cumA_A_wrong = S²/N_max · (3 + 2/144) ≈ 0.00316
       cumA_B_wrong = S²/N_max · (2 + 3/144) ≈ 0.00211
       Compare runner's actual output (using correct 1/r) to the
       wrong-prediction values — runner should match 1/r prediction,
       NOT the 1/d² prediction.

WC-4   (specific d=R=12 prediction lock-in) At d=R=12 specifically:
       cumA_A should equal S²/N_max · (3 + 1/6) = S²/N_max · 19/6
       cumA_B should equal S²/N_max · (2 + 1/4) = S²/N_max · 9/4
       Verify exact rational match (within float precision).
```

## Verdict gates

```text
PASS conditions (all required):
  P1  V-1 through V-6 hold for main test at d=R=12
  P2  Distance sweep produces expected cumA_A and cumA_B values
      across all 6 distances (relative error < 1e-9)
  P3  WC-1 confirms abstract-distance recovery (cumA converges to
      CR003 numbers within 1e-5 at d=10⁶)
  P4  WC-2 confirms correlation is distance-invariant at all
      tested distances
  P5  WC-3 confirms runner uses 1/r kernel (NOT 1/d²) — match the
      1/r prediction, NOT the 1/d² wrong-prediction
  P6  WC-4 confirms exact rational match at d=R=12

BOUNDARY conditions:
  B1  Main test passes but distance sweep has 1-2 distance points
      with deviations > 1e-9 (possible float-precision artifact)
  B2  WC-1 abstract recovery fails (cumA doesn't quite converge):
      possible normalization issue
  B3  Correlation invariance partial (1 of 4 distances gives
      different outcome): unexpected interaction

FAIL conditions:
  F1  Main test correlation wrong (not (1, 1)) at d=R=12
  F2  Distance sweep shows systematic deviation from 1/r prediction
  F3  WC-3 shows runner matches 1/d² instead of 1/r kernel
  F4  WC-4 specific-d=12 prediction lock-in fails
  F5  Runner crashes
```

Expected outcome: **PASS**. The LCQC006 v2 1/r A-kernel framework
mechanically produces the predicted budget formulas; running the same
algebraic program at varied distances should match exactly.

## What CR004 DOES NOT close

- Does NOT test ring topology / cyclic phrase (CR005)
- Does NOT test per-isotope variation (CR006)
- Does NOT test substrate gate `𝒢_sub` in joint composition (CR007)
- Does NOT test very-close distances (d < 1) — clamping to d ≥ 1
  per LCQC006a §3.2 self-distance choice. Sub-spacing distances
  would require typing the A-kernel behavior below d_ref.
- Does NOT test 3+ site geometry (full ring tests come in CR005)
- Does NOT test asymmetric coupling (uniform spacing assumption
  per LCQC006a P-RING-A; audit A-9 resolved)

## Outputs

```text
   CR004_PRECOMMIT.md             this file
   CR004_runner.py                Python runner with 1/r cross-coupling
   CR004_per_step_trace.csv       per-step joint state + cumulative_A
                                    at both sites at d=R=12
   CR004_distance_sweep.csv       cumA_A and cumA_B at each tested
                                    distance with predicted-vs-observed
   CR004_wrong_controls.csv       per-WC outcome
   CR004_summary.json             verdict + verification
   CR004_result.md                verdict markdown
   HASHES.txt                     SHA-256 of all CR004 artifacts
```

## Cryptographic chain (inputs)

```text
   LCQC000_NATIVE_QC_CHARTER.md                  (branch 18)
   LCQC001_NATIVE_STATE_ONTOLOGY.md              (branch 18)
   LCQC003_TRANSITIONS_AND_GATES_v2.md           (branch 18)
   LCQC004_COHERENCE_FLOOR.md                     (branch 18)
   LCQC004a_SUBSTRATE_ERROR_BUDGET_INVARIANT.md  (branch 18)
   LCQC006_NETWORKING_AND_RING_TOPOLOGY_v2.md     (branch 18)
   LCQC006a_RING_AMPLIFICATION_UNDER_THE_HOOD.md  (branch 18)
   LCQC008_NATIVE_MEASUREMENT_OPERATION_v2.md     (branch 18)
   CR003_result.md =  b6b2c1dcb3dcc076f809148c065040d30798df8037989d22bd873b81f465307b
   CR001_result.md =  c7a0d0eb5a1af9b69ea3300dda1d29399e9a297c9006e7e09a08d576e116b472

   Upstream sealed CRs (read-only):
   CR114, CR222, CR229, CR232, CR238
```

## Falsifiers

```text
F-CORR-D  Correlation differs from (1,1) at some distance d:
          the joint figure 𝒞 is somehow distance-dependent in its
          algebraic action (it should NOT be).

F-1OVERR  Budget formula deviates from S²/N_max · (3 + 2/d) and
          S²/N_max · (2 + 3/d): the 1/r kernel implementation is
          incorrect.

F-ABSTRACT  At very large d, cumA does not converge to abstract
          CR003 limits: the cross-coupling formula is wrong.

F-D2-MATCH  WC-3 reveals runner matches 1/d² rather than 1/r: the
          A-kernel falloff is implemented incorrectly.
```

## Sealed

Sean Brady, 2026-06-24. Substrate atoms, distance-dependent budget
formula, main test specification at d=R=12, distance sweep table,
verification gates, wrong controls, verdict thresholds, falsifiers
all locked above the line.
