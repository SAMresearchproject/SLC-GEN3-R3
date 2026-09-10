# CR067 Periodic Structure Derivation - Precommit

```text
document_id:    CR067_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR067
sealed_before:  CR067 runner exists and CR067 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv
                manifest sha256: cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
date_local:     2026-06-13
```

## Rule

```text
Verify that the periodic structure emerges from native role/operator
structure (QP049-QP054) as a downstream consequence of 09's frozen
mass surface, without consuming any IAEA roster value as a construction
input.  Verify Phase5 isotope tables (phase5_*) reproduce byte-equivalent
to their declared hashes.  Verify cross-branch shared inputs qp050 +
qp052 match between 09 and 10 manifests.  Verify no QP049-QP060
construction step reads the IAEA LiveChart roster before QP061.
```

## Question

```text
Can the periodic structure be shown to derive structurally such that:
  (a) the QP049-QP054 construction chain declares an unbroken
      next_frontier graph,
  (b) Phase5 isotope tables (seed identity, symmetric seed mass,
      neutron-excess binding-depth, numeric DeltaN, isotope neighbor
      ladder, roster stability lanes) reproduce byte-equivalent to
      hashes recorded in 09's manifest (cross-branch),
  (c) the cross-branch shared inputs qp050 and qp052 carry the same
      sha256 in 09's manifest and 10's manifest,
  (d) no QP049-QP060 source code reads the IAEA LiveChart roster as
      a construction input (only QP061 may do so),
  (e) the QP061 sealed prediction manifest's content was finalized
      before any external roster comparison?
```

## Declared Premises

```text
P1. Vault construction chain bridge:
      qp049 seed identity
      qp050 symmetric seed mass  (cross-branch shared with 09)
      qp051 neutron-excess binding-depth lane
      qp052 numeric DeltaN binding mass  (cross-branch shared with 09)
      qp053 roster stability lane
      qp054 isotope neighbor ladder
      qp055 Phase 5 isotope freeze
      qp056 residual stability / decay pressure
      qp057 decay direction chain
      qp058 pressure freeze
      qp059 visual package
      qp060 sealed comparison protocol
      Each declares next_frontier toward the chain successor.

P2. Phase5 isotope tables (load-bearing reproduction surface):
      phase4_tables/phase5_isotope_seed_identity_v1.csv
      phase4_tables/phase5_symmetric_isotope_seed_mass_v1.csv
      phase4_tables/phase5_neutron_excess_binding_depth_lanes_v1.csv
      phase4_tables/phase5_numeric_deltaN_binding_mass_v1.csv
      phase4_tables/phase5_isotope_roster_stability_lanes_v1.csv
      phase4_tables/phase5_isotope_neighbor_ladder_v1.csv
      phase4_tables/phase5_freeze_summary.json
      phase4_tables/phase5_freeze_summary.csv
      phase4_tables/phase5_sealed_prediction_manifest.csv
      phase4_tables/phase5_sealed_hash_manifest.csv
      These live in C:\VS\quantum_phase\phase4_tables\ and are hash-locked
      in 09's manifest (cross-branch dependency).

P3. Cross-branch shared inputs:
      qp050 + qp052 source/artifact files appear in both 09's and 10's
      manifests.  Their sha256 hashes must match across both manifests.

P4. Roster non-contact:
      QP049-QP060 source code (qpNNN_*.py) must NOT contain
      engine-surface (non-comment, non-string-literal) references to
      IAEA LiveChart roster file paths.
      Comments/docstrings that mention IAEA as the future external
      anchor are allowed.

P5. Sealed prediction manifest hash guard:
      QP060's sealed_comparison_protocol output records the prediction
      manifest sha256.  QP061's sealed_hash_guard_pass field confirms
      that the predictions used in the comparison match this pre-sealed
      sha256.  CR067 verifies this seal is byte-equivalent.

P6. Cross-branch manifest hash:
      10's SOURCE_MANIFEST.csv carries the 09 manifest sha256 as
      cross_branch_dependency.  CR067 verifies 09's manifest hash
      matches what's recorded.
```

## Outcome Taxonomy

```text
PASS_SCOPED_STRUCTURAL:
  - All manifest hashes verify.
  - QP049-QP060 next_frontier graph is unbroken.
  - Phase5 isotope tables hash-locked through 09's cross-branch manifest.
  - qp050 + qp052 cross-branch hashes match.
  - No IAEA roster engine-surface reference in QP049-QP060 source code.
  - QP060 prediction manifest sha256 = QP061 sealed_prediction_hash_actual.

BOUNDARY:
  - PASS_SCOPED_STRUCTURAL conditions hold structurally but one or more
    Phase5 tables are not exhaustively listed in CR067's expected set
    (proposal-class fallback).  Expected default if any soft anomaly.

FAIL:
  - Any required artifact hash fails verification.
  - Any QP049-QP060 source contains an engine-surface IAEA roster read.
  - qp050 or qp052 cross-branch hash mismatch.
  - QP060/QP061 sealed prediction hash mismatch (manifest mutated).

DIAGNOSTIC:
  - Manifest seal missing or sha mismatch.
  - Summary.json files unreadable.
  - Cross-branch dependency hash missing or wrong shape.
```

## Rule-9 Line

```text
This test could have falsified: the claim that the periodic structure
of the isotope vault emerges from QP049-QP054 native construction
without consuming any IAEA roster value as a construction input, and
that the construction-to-comparison boundary (QP060 -> QP061) is
hash-guarded byte-equivalent through the sealed prediction manifest.
```

## Expected Artifacts

```text
CR067_PRECOMMIT.md
CR067_PERIODIC_STRUCTURE_DERIVATION.py
CR067_input_manifest.csv
CR067_vault_chain_bridge_graph.csv
CR067_phase5_tables_check.csv
CR067_cross_branch_shared_inputs.csv
CR067_roster_non_contact_scan.csv
CR067_sealed_prediction_hash_guard.json
CR067_wrong_derivations.csv
CR067_manifest_seal_check.json
CR067_summary.json
CR067_result.md
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: simulate a Phase5 isotope table hash mismatch  -> FAIL
WC2: simulate an IAEA roster path read in qp053 (engine surface)  -> FAIL
WC3: simulate a broken vault-chain next_frontier link  -> FAIL
WC4: simulate qp050 cross-branch hash divergence (09 vs 10)  -> FAIL
WC5: corrupt CR065 manifest seal  -> DIAGNOSTIC
WC6: simulate a QP060/QP061 sealed prediction hash mismatch
     (would indicate prediction manifest mutated post-sealing)  -> FAIL
```

## Sealed Premise Set

```text
The premise set P1-P6 above is sealed at CR067_PRECOMMIT write time.
```
