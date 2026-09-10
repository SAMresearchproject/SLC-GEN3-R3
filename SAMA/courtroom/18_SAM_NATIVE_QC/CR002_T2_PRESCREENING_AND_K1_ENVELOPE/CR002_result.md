# CR002 — QGC T2 Prescreening + K1-Frozen Hardware Envelope — RESULT

**Verdict:** BOUNDARY (B2 — top/bottom rankings agree; 2 pair swaps in middle; B's ranking 100% robust)
**Branch:** 18_SAM_NATIVE_QC
**Phase:** 1A preliminary
**Executed:** 2026-06-24
**Runner:** `CR002_runner.py` (Python 3.12)

---

## 100% Disclaimer (preserved verbatim from PRECOMMIT)

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

## Headline

Component B's computational ranking matches Component A's theoretical
ranking at the **top** (mass-density modulation #1) and **bottom**
(spontaneous baseline reference); it disagrees in the **middle** with
two adjacent pair swaps:

```text
   Position    A's theoretical              B's computational
   ──────────────────────────────────────────────────────────────────
   #1          mass_density_modulation_BEC  mass_density_modulation_BEC  ✓
   #2          MEMS_pressure                EM_laser_focal               ← swap
   #3          EM_laser_focal               MEMS_pressure                ← swap
   #4          acoustic_phonon              charge_pulse_low_field       ← swap
   #5          charge_pulse_low_field       acoustic_phonon              ← swap
   #6 (REF)    spontaneous_baseline         spontaneous_baseline         ✓
```

B's ranking is **100% robust** under pathway-directness parameter
variation across [0.25×, 4.0×] of baseline (1000 samples). Full
ranking matches baseline in 100% of variation samples.

## Baseline coupling scores (Component B output)

```text
   candidate                          score (log10)      notes
   ─────────────────────────────────────────────────────────────────────
   mass_density_modulation_BEC         -2.37             trap site
   EM_laser_focal                      -2.91             focal volume
   MEMS_pressure                       -3.47             mechanical
   charge_pulse_low_field              -6.92             low E field
   acoustic_phonon                    -12.00             piezo lattice
   spontaneous_baseline               -20.30             reference
```

The score is the log10 product of (stress-energy magnitude × spatial
localization × temporal localization × pathway-directness baseline).
Full per-sample data in `CR002_candidate_scores.csv`.

## Verdict assessment

```text
   verification gate                            outcome
   ─────────────────────────────────────────────────────────
   V-1   A's ranking defensible from SAM        PASS
   V-2   B's ranking matches A's at baseline    FAIL (2 pair swaps)
   V-3   B's ranking robust ≥80% under variation PASS (100%)
   V-4   K1-frozen predictions committed         PASS (6 predictions in PRECOMMIT §C)
   V-5   Disclaimer preserved verbatim           PASS (above)
   V-6   No empirical-validation overreach       PASS

   Position differences:    4
   Inferred pair swaps:     2
   Top candidate matches:   YES (mass_density_modulation_BEC)
   Bottom reference matches: YES (spontaneous_baseline)
```

Per the PRECOMMIT verdict gates:
- P1-P3 not met (V-2 fails)
- BOUNDARY-B1 not applicable (V-3 passes)
- **BOUNDARY-B2 applies**: top/bottom right + 2 pair swaps in middle +
  robust ranking + disclaimer preserved → "internal consistency partial"
- F1-F5 not met (top and bottom match; not "substantially different")

**Verdict: BOUNDARY-B2.**

## Honest reading of the swap

The two pair swaps are NOT random — they reveal a structural
disagreement between A's intuition and B's mechanical computation:

### Swap #1: EM_laser (#2 in B) vs MEMS (#2 in A)

A's reasoning weighted **pathway-directness** heavily (direct
mass-density modulation > stress-energy via EM field). B's
mechanical multiplication of factors gives EM_laser a higher score
because its **excellent spatial localization (diffraction-limited
focus, 0.9) and excellent temporal localization (femtosecond pulse
possible, 0.95)** compensate for lower pathway-directness (0.45 vs
MEMS's 0.85).

Interpretation: if SAM's substrate coupling is even modestly
responsive to EM stress-energy, the precision-temporal-spatial
qualities of laser pulses make them competitive with mechanical
mass-density modulation. The "MEMS > EM_laser" intuition from A
assumes pathway-directness dominates by more than the model's
parameter range allows.

### Swap #2: charge_pulse (#4 in B) vs acoustic_phonon (#4 in A)

A's reasoning put acoustic_phonon above charge_pulse on the basis
that mechanical perturbations have a more direct pathway. B's
mechanical computation gives charge_pulse a higher score because
acoustic_phonon's stress-energy magnitude is so small (10^-10
relative to background) that even with better pathway-directness
(0.2 vs 0.15), the overall product is worse.

Interpretation: acoustic phonons may actually be a weaker trigger
than expected because the stress-energy they perturb is dominated
by their tiny per-atom mode energy. Charge pulses, even via
indirect EM stress-energy coupling, mobilize larger absolute
energy magnitudes.

## What this means for the K1-frozen envelope

The PRECOMMIT §C K1 predictions remain LOCKED as committed. **Per
discipline, we do NOT modify K1 predictions after running the test
that informs them.** That said, the BOUNDARY result suggests the K1
predictions may benefit from a follow-up CR (CR003 candidate) that:

- Reframes K1-PREDICTION-1 to include EM_laser_focal as a co-equal
  candidate with mass-density and MEMS (i.e., the prediction should
  not have ranked EM-via-laser lower than MEMS)
- Adds a K1 prediction specifically about whether pathway-directness
  dominates spatial/temporal localization in determining trigger
  effectiveness — this would be tested by comparing MEMS vs
  EM_laser performance in hardware
- Acknowledges that acoustic_phonon may be a weaker candidate than
  initially ranked, because of stress-energy magnitude smallness

These are POTENTIAL revisions for a future CR. They are NOT
retrofitted onto CR002's locked PRECOMMIT.

## What CR002 confirms

- The TOP candidate (mass-density modulation / BEC) is robust to the
  pathway-directness parameter — both A and B agree it should be the
  strongest trigger
- The BOTTOM reference (spontaneous baseline) is the correct
  reference — no trigger gives the smallest signal as expected
- Robustness across parameter variation is 100% — B's ranking is
  insensitive to the pathway-directness assumption within the tested
  range
- The internal consistency check has identified WHERE A's intuition
  and B's computation disagree, which is more useful than blind PASS

## What CR002 does NOT confirm

- That mass-density modulation actually works as a trigger in
  hardware (Phase 1A T2 is the test)
- That any specific quantitative score corresponds to physical
  signal magnitude
- That the pathway-directness parameter range tested covers the
  actual physical truth
- That the rankings predicted here will hold under conditions not
  modeled (e.g., specific isotope choices, specific geometries,
  non-uniform site environments)

The 6 K1-frozen predictions in PRECOMMIT §C remain the deliverable
for hardware-reveal testing. The CR002 BOUNDARY informs the
predictions' framing but does not validate them.

## Substantive findings to carry forward

1. **EM_laser_focal should be tested in parallel with MEMS and
   mass-density modulation** in Phase 1A T2, not after them. The
   computational model says it's competitive with MEMS.

2. **Pathway-directness vs precision-localization is a substantive
   parameter** that hardware T2 can resolve. The hardware test will
   reveal which factor dominates in actual substrate coupling.

3. **Acoustic phonon may be deprioritized** in Phase 1A T2 ordering
   because of stress-energy magnitude smallness. Still worth testing
   for completeness but not first.

4. **The pathway-directness parameter has 100% robust ranking
   within tested range** — this is the most useful technical finding.
   It means SAM's predictions for these candidates are not sensitive
   to small-to-moderate variations in the unknown pathway parameter.
   Larger variations (outside [0.25×, 4×]) might change rankings but
   would require SAM-silent assumptions that exceed plausible
   physics-intuition bounds.

## Verdict signature

```text
BOUNDARY_CR002_QGC_T2_PRESCREENING_K1_FROZEN_ENVELOPE_PARTIAL_INTERNAL_CONSISTENCY__
  COMPONENT_A_THEORETICAL_RANKING_AND_COMPONENT_B_COMPUTATIONAL_RANKING_DIFFER_AT_TWO_PAIR_SWAPS__
  TOP_CANDIDATE_MASS_DENSITY_BEC_AGREES__
  BOTTOM_REFERENCE_SPONTANEOUS_BASELINE_AGREES__
  MIDDLE_POSITIONS_2_3_AND_4_5_SWAPPED__
  EM_LASER_FOCAL_RANKS_ABOVE_MEMS_IN_COMPUTATIONAL_MODEL__
  CHARGE_PULSE_RANKS_ABOVE_ACOUSTIC_PHONON_IN_COMPUTATIONAL_MODEL__
  100_PERCENT_RANKING_ROBUST_UNDER_PATHWAY_PARAMETER_VARIATION_0_25X_TO_4X__
  K1_FROZEN_HARDWARE_ENVELOPE_PRESERVED_NO_POST_HOC_MODIFICATION__
  DISCLAIMER_VERBATIM_PRESERVED__
  NO_EMPIRICAL_SAM_VALIDATION_CLAIMED__
  CR002_CONFIRMS_INTERNAL_CONSISTENCY_PARTIAL_FLAGGED_FOR_FOLLOWUP_CR003_CANDIDATE
```

## Inputs

```text
   CR002_PRECOMMIT.md (this CR; sealed by Sean Brady 2026-06-24)
   CR002_runner.py     (this CR; Python 3.12 computational model)

   LCQC layer dependencies (branch 18; in-tree):
     LCQC000, LCQC001, LCQC003 v2, LCQC004, LCQC004a, LCQC005,
     LCQC006 v2, LCQC008 v2
   QGC_HARDWARE_SKETCH.md (branch 18)

   Upstream sealed CRs (read-only):
     CR114, CR222, CR229, CR232, CR238
```

## Outputs

```text
   CR002_candidate_scores.csv   1000-sample per-candidate scores under
                                  pathway-multiplier variation
   CR002_summary.json           structured verdict + verification gates
   CR002_result.md              this file
   HASHES.txt                   SHA-256 of all CR002 artifacts (post-run seal)
```

## Sealed

Sean Brady, 2026-06-24. CR002 verdict BOUNDARY-B2; internal-consistency
test of SAM's hardware predictions completed. Top and bottom rankings
agree between theoretical (A) and computational (B); middle has 2 pair
swaps revealing where A's intuition under-weighted spatial/temporal
localization. K1-frozen envelope locked in PRECOMMIT §C, preserved
without post-hoc modification. Audit queue updated with A-15 for actual
hardware T2 test. Phase 2 operation work proceeds with these findings
in view; Phase 1A hardware T2 (when committed) reveals against the
locked K1 envelope.
