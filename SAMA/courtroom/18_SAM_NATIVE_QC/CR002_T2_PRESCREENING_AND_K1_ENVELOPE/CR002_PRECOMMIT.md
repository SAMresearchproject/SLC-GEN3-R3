# CR002 — QGC T2 Prescreening + K1-Frozen Hardware Envelope

**Branch:** 18_SAM_NATIVE_QC
**Phase:** 1A preliminary (preceding hardware T2)
**Sealed by:** Sean Brady, 2026-06-24
**Companion to:** [QGC_HARDWARE_SKETCH.md](../QGC_HARDWARE_SKETCH.md) §3 T2

---

## 100% Disclaimer — read first

```text
   ┌─────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │  WHAT CR002 IS:                                                  │
   │                                                                  │
   │  An internal-consistency test of SAM's hardware predictions     │
   │  about candidate trigger mechanisms for substrate writes.       │
   │  Three components run together:                                  │
   │                                                                  │
   │    A. Theoretical candidate screening — paper analysis ranking  │
   │       each candidate by SAM-derived substrate-coupling pathway. │
   │                                                                  │
   │    B. Computational substrate-response model — software         │
   │       simulation that mechanically computes a coupling score    │
   │       per candidate under explicit parameter assumptions.       │
   │                                                                  │
   │    C. K1-frozen prediction envelope — locked predictions about  │
   │       what hardware T2 should observe, committed BEFORE any     │
   │       hardware run, for future K1-disciplined reveal.           │
   │                                                                  │
   │  WHAT CR002 IS NOT:                                              │
   │                                                                  │
   │  * NOT empirical validation of SAM. No hardware was run.        │
   │  * NOT a measurement of the substrate field. No physical        │
   │       coupling was tested.                                       │
   │  * NOT a confirmation that any specific trigger mechanism       │
   │       works. The rankings are model-based predictions.          │
   │  * NOT a substitute for hardware T2. The actual T2 test         │
   │       remains audit-queue item A-15 (added).                    │
   │                                                                  │
   │  The model in component B is parameterized with explicit        │
   │  assumptions about candidate coupling pathways. SAM is partly   │
   │  silent on these — what the substrate's trigger primitive       │
   │  actually is at the engineering layer is OPEN. The model        │
   │  encodes physics-intuition extrapolation from SAM's typed       │
   │  structural pieces, not pure SAM derivation. Variation across   │
   │  plausible parameter ranges is performed to assess robustness.  │
   │                                                                  │
   │  PASS / FAIL in CR002 means:                                     │
   │  * the SAM-derived theoretical ranking (A) and the              │
   │    computational model ranking (B) are internally consistent    │
   │    with each other under the model's stated assumptions.        │
   │                                                                  │
   │  PASS / FAIL does NOT mean:                                      │
   │  * the rankings reflect actual physical reality. Reality is     │
   │    measured in hardware; CR002 only confirms SAM's predictions  │
   │    are self-consistent in software.                             │
   │                                                                  │
   └─────────────────────────────────────────────────────────────────┘
```

This disclaimer is mandatory framing for any downstream citation of
CR002 results. Citing CR002 as evidence of empirical SAM validation
is a misuse.

## Question

```text
   Within the SAM framework as specified by LCQC000-LCQC008 v2 + the
   sealed CR238 + CR222d/CR232 + CR244 layers, do the candidate
   trigger mechanisms from QGC_HARDWARE_SKETCH §2 admit a coherent
   ranking by predicted substrate-coupling pathway strength? Does the
   computational model's ranking agree with the theoretical analysis's
   ranking, and is the agreement robust to plausible variation in the
   parameterized coupling pathway?
```

## Locked substrate atoms (read-only from CR238)

```text
   A_0 = 1/(12π)         per-write A-contribution at write site
   A(r) = A_0 · d_ref/r  per-write A-contribution at distance r
   κ = 7117/768          mass channel coefficient
   g = 1/64              gravitational channel coefficient
   Q_sub = S·[Zκ + (N-Z)·g]   per-isotope substrate coupling
   S = 8, α_H = 2, R = 12, D = 3
   N_max = 16πR⁴/17 ≈ 61,312    per-site coherence ceiling
```

## Component A — Theoretical candidate screening

The SAM substrate-coupling pathway for any trigger mechanism passes
through stress-energy perturbation at the target site. Per CR238 the
A-kernel responds to mass-energy distribution; per the GR-consistent
SAM framework, ANY stress-energy modulation contributes to substrate
field activity. The trigger mechanism's substrate-coupling strength
scales as:

```text
   coupling_strength  ∝  stress_energy_perturbation
                       × spatial_localization_at_site
                       × temporal_localization_per_event
                       × pathway_directness_to_substrate
```

Per-candidate theoretical analysis:

```text
candidate            stress-energy    spatial    temporal    pathway     ranking
                     magnitude        local.     local.      directness  expected
                     (rel. to bg)
─────────────────────────────────────────────────────────────────────────────────
spontaneous          0 (reference)    site-wide  continuous  baseline    REF
mass-density mod     direct mass      excellent  medium      HIGH        #1
  (BEC, cooled atoms)  modulation     (trap)
MEMS pressure        direct density   good       medium      HIGH        #2
  (mechanical)         modulation     (MEMS)
EM-laser focal       stress-energy    excellent  excellent   MEDIUM      #3
  (high-intensity)     via EM field   (μm focus) (fs pulse)
acoustic phonon      stress-energy    poor       poor        LOW         #4
  (piezo)              via lattice    (propag.)  (cw mode)
charge-pulse         stress-energy    good       excellent   LOW-ind.    #5
  (low-field EM)       via EM field   (electrode)(ns pulse)  (very weak)
```

**A's predicted ranking (locked):** mass-density > MEMS > EM-laser > acoustic > charge-pulse > spontaneous

**Where SAM is silent (explicit):** the trigger mechanism IS the
architect-substrate coupling primitive. SAM specifies that substrate
writes happen as the universe's foundational events; SAM does NOT
specify the mechanical pathway by which an external perturbation
modulates this rate. The pathway-directness scoring above is
physics-intuition: stress-energy that directly modulates mass-energy
density is presumed to couple more directly to the substrate than
stress-energy mediated through EM fields. This is an extrapolation
from SAM's typed pieces, not a sealed derivation.

## Component B — Computational substrate-response model (the test)

The runner `CR002_runner.py` mechanically computes a coupling score
per candidate using the per-candidate parameters above, plus a
parameterized **pathway-directness factor** that captures the
SAM-silent unknown. The model:

1. Compute base score = stress_energy × spatial × temporal × pathway
2. Vary pathway parameter across plausible range [0.25×, 4×] of
   baseline value
3. Compute ranking under each parameter variation
4. Report: whether ranking is robust (same order regardless of
   variation) or fragile (order changes with parameter)

**B's ranking is robust iff** the same ordering is produced across
all parameter variations.

## Component C — K1-Frozen Hardware Envelope

Predictions LOCKED HERE, committed before any hardware T2, for
future K1-disciplined reveal when Phase 1A hardware is built and
run. Each prediction is paired with a falsifier — what observation
would contradict SAM.

```text
   K1-PREDICTION-1   Trigger mechanism ranking (qualitative)
       PREDICTED:    First successful trigger mechanism in T2 will be
                     mass-density modulation (BEC / cooled atom) OR
                     direct mechanical (MEMS) — not charge-pulse alone.
       FALSIFIER:    If charge-pulse alone produces detectable signal
                     while mass-density and MEMS do not, the SAM
                     coupling-pathway scoring is wrong; pathway-
                     directness from stress-energy to substrate is
                     not as A predicts.

   K1-PREDICTION-2   Temperature flatness of trigger response
       PREDICTED:    For ANY mechanism that produces detectable signal,
                     the signal magnitude at 4K and 295K should differ
                     by less than 20% (excluding obvious thermal
                     equipment effects that can be controlled for).
       FALSIFIER:    If signal magnitude varies by > 50% across 4K →
                     295K (after controlling for equipment thermal
                     drift), Rule #7 (temperature-flat coherence) is
                     wrong and SAM's hardware foundation needs revision.

   K1-PREDICTION-3   1/r A-kernel coupling falloff
       PREDICTED:    Cross-site signal at distance d should fall as
                     1/d (within measurement error) across at least
                     one decade of distance variation.
       FALSIFIER:    If coupling falls exponentially, as 1/d², or
                     follows any law inconsistent with A-kernel 1/r,
                     CR238 A-kernel needs revision at the QGC-relevant
                     length scale.

   K1-PREDICTION-4   Per-isotope coherence scaling
       PREDICTED:    Saturation behavior at site filled with U-238
                     should plateau at ≈1.29× the saturation count
                     for C-12 anchor (within measurement error).
                     Site filled with H-1 should plateau at ≈0.50×
                     the C-12 count.
       FALSIFIER:    If per-isotope multipliers do NOT follow the
                     LCQC005 R_sub predictions (N=Z balanced anchor
                     reference, N>Z memory > 1, N<Z network < 1
                     monotonically), the substrate coupling formula
                     Q_sub = S·[Zκ + (N-Z)·g] is wrong at
                     hardware-relevant scales.

   K1-PREDICTION-5   N_max saturation magnitude
       PREDICTED:    Saturation plateau for the balanced-anchor site
                     occurs at ≈61,312 events per coherence cycle
                     (within 10%, modulo measurement / detector
                     efficiency calibration).
       FALSIFIER:    If saturation plateau is substantially different
                     (>2× off), the N_max = 16πR⁴/17 derivation in
                     LCQC004 is wrong at hardware scale.

   K1-PREDICTION-6   Substrate-write event distinction from
                     conventional matter signals
       PREDICTED:    Triggered substrate-write events should produce
                     detector signals that DO NOT correlate with
                     conventional EM crosstalk, phonon energy
                     deposition, or thermal events at the trigger.
                     Discrimination must be possible via at least one
                     of: temperature signature, magnetic-field
                     dependence, time-resolved kinetics.
       FALSIFIER:    If signal is indistinguishable from conventional
                     matter physics under all available discrimination
                     methods, the QGC's claim of substrate-native
                     events cannot be supported by this apparatus
                     class and needs different instrumentation.
```

These 6 K1-frozen predictions are the explicit hardware-test
envelope. Future Phase 1A hardware results reveal against this
envelope. PASS/FAIL on each is determined by the hardware
measurement, not by CR002 (which only confirms that the SAM
framework predicts them self-consistently).

## Locked verification (the CR002 test)

```text
V-1   A's theoretical ranking (mass-density > MEMS > EM-laser >
      acoustic > charge-pulse > spontaneous-as-reference) is
      defensible from the SAM-typed framework as analyzed in §A.
V-2   B's computational model produces a ranking at the baseline
      pathway parameter that matches A's ranking exactly.
V-3   B's ranking is ROBUST to pathway-parameter variation across
      [0.25×, 4×] of baseline — the same ranking emerges for at
      least 80% of parameter samples in the variation range.
V-4   All 6 K1-frozen predictions in §C are explicitly committed
      with paired falsifiers.
V-5   The disclaimer block at the top of this PRECOMMIT is
      preserved verbatim in the result.md.
V-6   No claim of empirical SAM validation appears in any CR002
      artifact.
```

## Verdict gates

```text
PASS conditions (all required):
  P1  V-1 through V-6 all hold
  P2  B's ranking matches A's at baseline pathway parameters
  P3  B's ranking is robust under parameter variation (80%+ samples)
  P4  Disclaimer block preserved verbatim in result
  P5  No empirical-validation overreach in any CR002 output

BOUNDARY conditions:
  B1  A and B rankings agree at baseline but B is fragile
      (rankings flip for >20% of parameter samples)
  B2  A and B differ in 1-2 positions (e.g., MEMS and EM-laser swap)
      — internal consistency partial

FAIL conditions:
  F1  A and B produce substantially different rankings at baseline
  F2  Disclaimer block missing or weakened in result
  F3  Any claim of empirical SAM validation appears
  F4  K1-frozen predictions weakened or hedged in §C
  F5  Runner crashes / produces no ranking
```

Expected outcome: **PASS** with rankings agreeing under baseline and
robust to plausible variation. PASS would confirm SAM's hardware
predictions are internally self-consistent for the candidate
trigger mechanisms specified. PASS does NOT confirm any of the
mechanisms actually work in hardware.

## What CR002 DOES NOT close

- Does NOT close audit-queue A-15 (actual hardware T2). CR002 is
  prescreening; A-15 is the empirical test that comes later.
- Does NOT specify the substrate write trigger mechanism in any
  sealed structural sense. The mechanism remains the engineering
  unknown identified in the hardware sketch.
- Does NOT compare to external physics models for PASS/FAIL. The
  test is purely internal to SAM. R-3 discipline preserved.
- Does NOT predict ω_op (operation rate / event timescale). That
  remains engineering-determined per the hardware sketch.
- Does NOT close any LCQC layer open follow-up. CR002 is a
  prescreening artifact, not a structural derivation.

## Outputs

```text
   CR002_PRECOMMIT.md           this file
   CR002_runner.py              Python runner executing component B
   CR002_candidate_scores.csv   per-candidate score per parameter
                                variation sample
   CR002_summary.json           verdict + ranking stability assessment
   CR002_result.md              verdict markdown with disclaimer
                                preserved verbatim
   HASHES.txt                   SHA-256 of all CR002 artifacts
```

## Cryptographic chain (inputs)

```text
   LCQC000_NATIVE_QC_CHARTER.md                  (branch 18)
   LCQC001_NATIVE_STATE_ONTOLOGY.md              (branch 18)
   LCQC003_TRANSITIONS_AND_GATES_v2.md           (branch 18)
   LCQC004_COHERENCE_FLOOR.md                     (branch 18)
   LCQC004a_SUBSTRATE_ERROR_BUDGET_INVARIANT.md  (branch 18)
   LCQC005_MATERIALS_PALETTE.md                   (branch 18)
   LCQC006_NETWORKING_AND_RING_TOPOLOGY_v2.md     (branch 18)
   LCQC008_NATIVE_MEASUREMENT_OPERATION_v2.md     (branch 18)
   QGC_HARDWARE_SKETCH.md                         (branch 18)

   Upstream sealed CRs (read-only):
   CR114, CR222, CR229, CR232, CR238
```

## Falsifiers (for CR002 itself)

```text
F-RANKING   A and B rankings disagree at baseline parameters: the
            theoretical analysis (A) and computational model (B)
            don't converge under SAM's framework — possible
            interpretation issue in one or the other.

F-ROBUSTNESS  B's ranking flips under modest parameter variation:
              the pathway-directness assumption is doing too much
              load-bearing work; the rankings are not derived from
              SAM but from the speculative parameter choice.

F-DISCLAIMER  Disclaimer is weakened or missing in any artifact: the
              test was misframed as empirical validation. Whole CR002
              becomes a methodological error per repo discipline
              (see [feedback_no_outside_model_comparison]).
```

## Sealed

Sean Brady, 2026-06-24. Disclaimer, substrate atoms, theoretical
analysis components, computational model parameters, K1-frozen
hardware envelope, verification gates, verdict thresholds,
falsifiers all locked above the line.
