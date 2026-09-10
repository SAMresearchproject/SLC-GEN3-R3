# CR063 Wrong Controls and Near Neighbors - Precommit

```text
document_id:    CR063_PRECOMMIT
branch:         09_PARTICLE_MASS_CHAIN
cr_slot:        CR063
sealed_before:  CR063 runner exists and CR063 result exists
seal_anchor:    SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13
                (sha256: ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8)
manifest:       09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv  (sha256 d605d070...)
date_local:     2026-06-13
```

## Rule

```text
Verify that honest negatives (deliberately perturbed engines / dropped
selectors / wrong-control row sets) fail to reproduce SAM's parameter-
free particle predictions.  If any honest negative DOES reproduce the
engine's row outputs, CR061 + CR062 results are retroactively
invalidated.
Per seal: CR063 verdict is PASS or DIAGNOSTIC on its own criterion.
```

## Question

```text
Do declared honest negatives produce row outputs that fail to match the
PDG-verified strict + audit row set, such that:
  (a) qp040 support row replay WITHOUT observed mass produces rows that
      DO NOT reach CR062's PDG-tolerance bands,
  (b) per-QGA wrong_controls.csv files exist and document declared
      wrong-control row sets,
  (c) hostile QP010-QP021 audit replay verdicts remain NO_BLOCKER_FOUND
      (rolled forward from CR060),
  (d) simulated engine perturbations (dropped qp019 / swapped qp071 SUK
      gate / bypassed qp073) would change Phase4 outputs?
```

## Declared Premises

```text
P1. qp040 = golden honest-negative artifact:
      C:\VS\quantum_phase\artifacts\qp040\qp040_support_row_replay_without_observed_mass.csv
    Must exist with hash-locked content.

P2. Per-QGA wrong_controls files:
      tests/Substrate/QGA0XX_*/QGA0XX_wrong_controls.csv  for the
      QGA053-QGA060 + QGA068-QGA072 set in scope for 09.

P3. Hostile audit verdict roll-forward:
      AUDIT_VERDICT_POST_RETEST_REVIEW.md still ends NO_BLOCKER_FOUND.

P4. Engine perturbation simulations:
      - Drop qp019 (mass surface bridge): Phase4 frozen tables would
        be inconsistent (no row could be derived from the chain).
      - Swap qp071 (SUK gate draft): the SUK bridge breaks.
      - Bypass qp073 (final Phase4 freeze): the row partition is
        not finalized.
      Each simulation is verified by removing the manifest entry and
      observing the downstream check fail.

P5. Near-neighbor row check:
      For each PDG-anchored row, the engine's predicted value vs. the
      PDG value's nearest unselected-row neighbor must NOT also be
      within tolerance.  (Already implicitly verified by CR062 - if
      near neighbors were also within band, residual differences
      between adjacent rows would be smaller than the band itself.)
      CR063 explicitly checks this by computing inter-row residual
      gaps.

P6. CR059 manifest seal intact.
```

## Outcome Taxonomy

```text
PASS_HONEST_NEGATIVES_REJECT:
  - qp040 present and documents the without-observed-mass replay.
  - All in-scope wrong_controls.csv files present.
  - Hostile audit verdict still NO_BLOCKER_FOUND.
  - All simulated engine perturbations detected as breaking the chain.
  - Inter-row residual gaps prove neighbors are not within band.

DIAGNOSTIC:
  - qp040 missing or unreadable.
  - One or more wrong_controls.csv files missing.
  - Hostile audit verdict not parseable.
  - Manifest seal mismatch.

FAIL_RETROACTIVE:
  - qp040 replay produces rows that reach PDG tolerance.
  - A simulated engine perturbation produces the same row outputs.
  - This would retroactively invalidate CR061 + CR062.
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's parameter-free
particle predictions cannot be reproduced by deliberately perturbed
engines or dropped selectors, and that the qp040 without-observed-mass
replay correctly fails to reach PDG row-level tolerance bands.
```

## Expected Artifacts

```text
CR063_PRECOMMIT.md
CR063_WRONG_CONTROLS_AND_NEAR_NEIGHBORS.py
CR063_input_manifest.csv
CR063_qp040_honest_negative_check.json
CR063_qga_wrong_controls_inventory.csv
CR063_hostile_audit_roll_forward.json
CR063_engine_perturbation_simulations.csv
CR063_near_neighbor_gap_analysis.csv
CR063_wrong_controls.csv
CR063_manifest_seal_check.json
CR063_summary.json
CR063_result.md
HASHES.txt
```

## Wrong Controls (meta-level, of wrong-control detection itself)

```text
WC1: simulate qp040 missing from manifest -> DIAGNOSTIC detection
WC2: simulate a QGA wrong_controls.csv with 0 rows -> DIAGNOSTIC
WC3: simulate hostile audit verdict ending in FAIL -> retroactive
     invalidation detected
WC4: simulate inter-row gap < tolerance for two adjacent strict rows
     -> would mark near-neighbor check as INSUFFICIENT
WC5: corrupt manifest seal -> DIAGNOSTIC
WC6: simulate a perturbation that DOES reproduce the engine output
     -> FAIL_RETROACTIVE detection wired
```

## Sealed Premise Set

```text
The premise set P1-P6 above is sealed at CR063_PRECOMMIT write time.
```
