# CR060 Selector Provenance and Forbidden Targets - Precommit

```text
document_id:    CR060_PRECOMMIT
branch:         09_PARTICLE_MASS_CHAIN
cr_slot:        CR060
sealed_before:  CR060 runner exists and CR060 result exists
seal_anchor:    SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13
                (sha256: ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8)
manifest:       09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv  (locked by CR059)
                manifest sha256: d605d070281119f2c874112de0be1be06d6ab4ad5ef8b914e459420c8148f22a
date_local:     2026-06-13
```

## Rule

```text
Verify that every selector in the particle mass chain has a provenance
trace independent of any externally measured particle mass value, fitted
Yukawa coupling, or post-observation calibration loop.
Walk the QP arm dependency chain (QP004 -> QP018 -> QP019 -> QP021 ->
QP023 -> QP037 -> QP040 -> QP050 -> QP052 -> QP062..QP075) and verify
each test's declared self-disclosure fields.
Replay the hostile QP010-QP021 audit and verify the RT_QP019 mass
surface replay result.
Cite QGA032 source_provenance_board.csv and QGA033 witness_board.csv as
the upstream provenance discipline boards.
```

## Question

```text
Can every selector in the particle mass chain be shown to:
  (a) declare its construction-input set with no external particle mass
      value, no fitted Yukawa table, no calibration loop, and no
      target-driven optimizer,
  (b) survive the hostile QP010-QP021 audit and RT_QP019 mass surface
      replay,
  (c) trace its selector lineage back to declared SAM-native quantities
      through the QGA032/QGA033 provenance boards, and
  (d) pass each test's own per-test self-disclosure (every qpNNN_summary
      .json reports external_data_used=false, observed_*_used=false,
      and free_parameters_introduced=0)?
```

## Declared Premises

```text
P1. Selector chain (QP arm):
      qp004 phase-to-role bridge
      qp018 role-bridge to particle slot selector
      qp019 particle slot to native mass surface bridge
      qp020 QP-to-particle bridge readiness package
      qp021 charged particle mass bridge
      qp023 derived particle table freeze
      qp037 particle identity closure freeze
      qp040 support row replay (without observed mass)
      qp050 symmetric isotope seed mass (shared input)
      qp052 numeric DeltaN binding mass (shared input)
      qp062 full lattice meson binding readout selector
      qp063 phase4 freeze refresh
      qp064 gauge boson surface extension
      qp065 same-flavor quarkonium frontier coordinates
      qp066 phase4 final freeze with parent linkage
      qp067 heavy composite role-operator enumerator
      qp069 heavy role-operator group invariant search
      qp070 heavy role-operator structural reading proposal
      qp071 heavy composite derivation rule + SUK gate draft
      qp072 heavy composite fill pass
      qp073 phase4 final freeze post-SUK-HCO
      qp074 doubly-heavy BC baryon structural reading proposal
      qp075 campaign closure summary table

P2. Per-test self-disclosure check:
      Each qpNNN_summary.json shall report:
        external_data_used               = false
        observed_particle_masses_used    = false   (when applicable)
        observed_quarkonium_masses_used  = false   (when applicable)
        free_parameters_introduced       = 0
      Exception: qpNNN_summary.json may carry "REVEAL_ONLY" residual
      scoring fields - these are post-derivation comparators, not
      construction inputs, and are explicitly allowed by the seal.

P3. Provenance boards:
      tests/Substrate/QGA032_SW_ACTION_DENSITY_OR_1_OVER_A0_SQUARED_SELECTOR/
        QGA032_source_provenance_board.csv
      tests/Substrate/QGA033_FACTOR_PROVENANCE_OR_SW_ACTION_DENSITY_SOURCE_AUDIT/
        QGA033_witness_board.csv
      Each row in these boards declares a source's status and evidence.
      CR060 must read both and verify no row carries an "ACTIVE_PROOF" or
      "PROMOTED" tag for any retired/quarantined/spreadsheet source.

P4. Hostile audit gate:
      audits/private_hostile_qp010_qp021/
      Must contain:
        results/ markdown files reporting per-QP retest verdicts
        retest_runs/RT_QP019_MASS_SURFACE_REPLAY/ replay results
      CR060 must verify each results/*.md ends in a PASS verdict (or
      explicitly states the failure mode if any).

P5. Forbidden selector patterns (engine surface, code tokens only):
      - any selector that imports a measured mass value as construction input
      - any selector with scipy.optimize / curve_fit / least_squares /
        minimize against an observed quantity
      - any selector that walks the Forbidden Route per DIRECTIVE_INDEX:
        known SM/GR/LCDM result -> fit residual -> retrofitted explanation
      - any selector that consumes a PDG / AME2020 / NIST mass roster
        value (PDG mentions inside REVEAL_ONLY / residual_scoring blocks
        are documentation; the seal allows comparator-only references)

P6. QGA057 / SUK018 audit-strictness gate:
      tests/Substrate/QGA057_TOP_AUDIT_STRICTNESS_RESOLUTION_SELECTOR/
      Result must classify the m_t row as audit-grade with the 1/alpha_em
      lift documented per PRIORITY_RECORD.

P7. The CR059 manifest seal is the only allowed input registry:
      09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv.sha256.txt must exist
      and match the on-disk SOURCE_MANIFEST.csv. CR060 reads only
      artifacts listed there.
```

## Outcome Taxonomy

```text
PASS:
  - Every qpNNN_summary.json reports external_data_used=false (where
    declared) and free_parameters_introduced=0.
  - Hostile audit results all PASS (or explicitly documented otherwise
    without contradicting the engine's per-test disclosure).
  - Provenance boards have no row promoting a quarantined/retired
    source to proof.
  - No engine-surface (code-token) match for any forbidden selector
    pattern.
  - The CR059 manifest seal is intact.

BOUNDARY:
  - All PASS conditions hold structurally.  This is the expected default
    verdict for CR060.  The K1 external anchor is still at CR062.

FAIL:
  - Any qpNNN_summary.json reports external_data_used=true or
    free_parameters_introduced>0 without an explicit reveal-only or
    pre-declared exception.
  - Any forbidden selector pattern is found in an engine code token.
  - The hostile audit reports a failure that contradicts the per-test
    disclosure.
  - A provenance board row promotes a quarantined source to proof.

DIAGNOSTIC:
  - A qpNNN_summary.json is missing or malformed.
  - The provenance boards or hostile audit artifacts are incomplete.
  - The CR059 manifest seal is missing or its sha mismatches the on-disk
    manifest.
```

## Rule-9 Line

```text
This test could have falsified: the claim that every selector in the
particle mass chain has a provenance trace independent of measured
particle masses, fitted Yukawa couplings, and post-observation
calibration loops, and that the hostile QP010-QP021 audit confirms
this independence.
```

## Expected Artifacts

```text
CR060_PRECOMMIT.md
CR060_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS.py
CR060_input_manifest.csv             (subset of SOURCE_MANIFEST.csv read)
CR060_qp_self_disclosure_check.csv   (per qpNNN: declared fields / verdict)
CR060_provenance_board_check.csv     (per QGA032/QGA033 row: status verdict)
CR060_hostile_audit_replay_check.csv (per audit results/*.md: verdict)
CR060_forbidden_selector_scan.csv    (engine-surface code-token matches)
CR060_manifest_seal_check.json       (verifies CR059 seal still intact)
CR060_wrong_controls.csv             (declared adverse injections)
CR060_summary.json
CR060_result.md
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: inject a fabricated qpNNN_summary.json declaring
     external_data_used=true and observed_particle_masses_used=true
     -> expected: FAIL on P2

WC2: inject a synthetic engine .py code token containing
     scipy.optimize.curve_fit against an observed mass
     -> expected: FAIL on P5

WC3: inject a provenance board row tagging a retired-spreadsheet source
     with status ACTIVE_PROOF
     -> expected: FAIL on P3

WC4: inject a hostile audit result file ending in FAIL
     -> expected: FAIL on P4

WC5: corrupt one byte of SOURCE_MANIFEST.csv so the CR059 seal mismatches
     -> expected: DIAGNOSTIC on P7

WC6: inject a qp077 (non-existent) summary that walks Forbidden Route
     (Yukawa coupling table imported as selector input)
     -> expected: FAIL on P5
```

## Sealed Premise Set

```text
The premise set P1-P7 above is sealed at CR060_PRECOMMIT write time.
No CR060 runner may add or alter a premise.  If a premise needs
revision after CR060 runs, the revision belongs to an appeal CR per the
Appeal Channel section of the 09 seal.
```
