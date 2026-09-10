# CR004 — Phase 2 Distance-Dependent Coupling via 1/r A-Kernel (REDACTED for CR013 DERIVER context)

**Branch:** 18_SAM_NATIVE_QC
**Phase:** 2 (multi-site composition with physical-distance effects)
**Sealed by:** Sean Brady, 2026-06-24

---

## Question

Does the two-site joint program produce the same correlated output when the two sites are at finite physical distance d, with per-site cumulative-A budget tracking a substrate-field continuity 1/r A-kernel? Specifically:

```text
   Does the program

      INIT site_A (face=9, α_H=0, resolved) at position 0
      INIT site_B (face=4, α_H=0, resolved) at position d
      → B(A) → 𝒞(A→B) → PUBLISH(A) → PUBLISH(B)

   produce:
     (1) the same correlated final state (α_H_A=1, α_H_B=1) at every
         distance d (correlation is distance-invariant)
     (2) per-site cumulative-A budget that matches the typed formula
         derived from the 1/r kernel:
             cumulative_A(site_A) ∝ 3·S² + 2·S²/d
             cumulative_A(site_B) ∝ 2·S² + 3·S²/d
     (3) convergence to the abstract-distance result as d → ∞
```

## Locked substrate atoms (read-only)

```text
   S² = 64                       writes per figure
   [ceiling constant]            per-site coherence [REDACTED] (upstream sealed)
   A_0 = 1/(12π) ≈ 0.02653       per-write A-contribution at write site
                                  (CR238)
```

## Locked distance-dependent budget formula

For each substrate write event at site X (with cost = 1 substrate write, normalized contribution at the write site):

```text
   site Y receives A-shift contribution = A_0 · (d_ref / d(X, Y))

   where d_ref = unit spacing (kernel's characteristic length; the
                 quantity CR013 asks the DERIVER to identify)
         d(X, Y) = distance between sites X and Y (in d_ref units)
         d(X, X) = d_ref (self-reference; upstream convention)
```

For the joint figure 𝒞 at sites (control, target):
```text
   ΔcumA at control  =  A_0 · (1 + 1/d)   in unit-normalized form
   ΔcumA at target   =  A_0 · (1 + 1/d)   (symmetric)
```

## Locked program (main test at d = R = 12)

The main test runs the same two-site program at distance d = R = 12 (the register radix, a structurally natural distance choice).

```text
   FINAL   cumulative_A_A = A_0 · (3 + 2/12) ≈ 3.30396e-3
           cumulative_A_B = A_0 · (2 + 3/12) ≈ 2.34896e-3
           correlation:    (α_H_A=1, α_H_B=1)
           faces:          (face_A=9, face_B=4) unchanged
```

## Locked distance sweep

The runner additionally executes the same program at multiple distances and verifies the predicted scaling:

```text
   d              expected cumA_A               expected cumA_B
   ──────────────────────────────────────────────────────────────
        1         5 · A_0                       5 · A_0
        2         4 · A_0                       3.5 · A_0
        6         3.333 · A_0                   2.5 · A_0
       12 (= R)   3.167 · A_0                   2.25 · A_0
      100         3.02 · A_0                    2.03 · A_0
    10000         ≈ 3.0 · A_0                   ≈ 2.0 · A_0
```

Distance sweep convergence check: at large d, cumA_A → 3·A_0 and cumA_B → 2·A_0 (the abstract-distance limit).

## Wrong controls

```text
WC-1   (abstract-distance limit recovery) Run with d = 1,000,000
       (effectively infinite). Expected: cumA converges to abstract
       numbers within 1e-5.

WC-2   (correlation distance-invariance) Run main program at d=1,
       d=12, d=100, d=10000. Expected: final correlation is
       (1, 1) at every distance — outcome does NOT depend on d.

WC-3   (wrong distance law — 1/d² instead of 1/d) Hypothetical
       computation: if the kernel were 1/d² instead of 1/d, at d=12,
       cross-coupling per write would be 1/144 instead of 1/12
       (in unit-normalized form). Expected:
       cumA_A_wrong = A_0 · (3 + 2/144) ≈ 0.00316
       cumA_B_wrong = A_0 · (2 + 3/144) ≈ 0.00211
       Compare runner's actual output (using correct 1/r) to the
       wrong-prediction values — runner should match 1/r prediction,
       NOT the 1/d² prediction.

WC-4   (specific d=R=12 prediction lock-in) At d=R=12 specifically:
       cumA_A should equal A_0 · (3 + 1/6) = A_0 · 19/6
       cumA_B should equal A_0 · (2 + 1/4) = A_0 · 9/4
```

## Verdict gates

```text
PASS conditions (all required):
  P1  Main test at d=R=12 correlation is (1,1) with predicted cumA
  P2  Distance sweep matches 1/r prediction across all 6 distances
      (relative error < 1e-9)
  P3  WC-1 confirms abstract-distance recovery (cumA converges within 1e-5)
  P4  WC-2 confirms correlation is distance-invariant
  P5  WC-3 confirms runner uses 1/r kernel (NOT 1/d²)
  P6  WC-4 confirms exact rational match at d=R=12
```

Expected outcome: **PASS**. The 1/r A-kernel framework mechanically produces the predicted budget formulas; running the same algebraic program at varied distances should match exactly.

## What CR004 DOES NOT close

- Does NOT test very-close distances (d < 1) — clamping to d ≥ 1 per upstream convention. Sub-spacing distances would require typing the A-kernel behavior below d_ref.

## Sealed

Sean Brady, 2026-06-24. Substrate atoms, distance-dependent budget formula, main test at d=R=12, distance sweep table, wrong controls, verdict thresholds all locked above the line.
