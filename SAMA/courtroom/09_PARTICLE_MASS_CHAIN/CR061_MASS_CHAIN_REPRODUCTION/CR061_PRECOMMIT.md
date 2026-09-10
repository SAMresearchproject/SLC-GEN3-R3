# CR061 Mass Chain Reproduction - Precommit

```text
document_id:    CR061_PRECOMMIT
branch:         09_PARTICLE_MASS_CHAIN
cr_slot:        CR061
sealed_before:  CR061 runner exists and CR061 result exists
seal_anchor:    SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13
                (sha256: ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8)
manifest:       09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv  (locked by CR059)
                manifest sha256: d605d070281119f2c874112de0be1be06d6ab4ad5ef8b914e459420c8148f22a
date_local:     2026-06-13
```

## Rule

```text
Verify that the particle mass chain reproduces byte-equivalent across
the QP arm bridge (QP004 -> QP018 -> QP019 -> QP021 -> QP023 -> QP037 ->
QP040 -> QP050 -> QP052 -> QP062 -> QP063 -> QP064 -> QP065 -> QP066 ->
QP067 -> QP069 -> QP070 -> QP071 -> QP072 -> QP073 -> QP074 -> QP075)
and the SUK/QGA arm (SUK014/QGA053 -> SUK015/QGA054 -> SUK016/QGA055 ->
SUK017/QGA056 -> SUK018/QGA057 -> SUK019/QGA058 -> SUK020/QGA059 ->
SUK021/QGA060 + later SUKs), bridged at QP071 (SUK gate draft).
Reproduction is verified through:
  1. byte-equivalence of every artifact hash in the locked manifest
  2. each QP test declaring next_frontier to the expected successor
  3. the QP071 SUK gate draft artifact connecting QP arm to SUK campaign
  4. Phase4 frozen particle tables matching their manifest hashes
  5. G616c public consolidation cross-check
```

## Question

```text
Can the particle mass chain be shown to reproduce structurally such that:
  (a) every artifact remains byte-equivalent to its manifest-locked hash,
  (b) the QP arm declares an unbroken next_frontier graph from qp004 to qp075,
  (c) the SUK/QGA arm's strict native particle ledger (QGA055) and
      predictor surface (QGA056) artifacts are present and structurally
      linked,
  (d) QP071's parent_suk_gate_draft artifact connects the QP arm to the
      SUK kernel campaign,
  (e) the Phase4 frozen particle tables (parameter_free_particle_table,
      particle_periodic_matrix, particle_composite_freeze_v2) match their
      manifest-locked hashes,
  (f) the G616c parameter-free mass chain consolidation table is present
      and hash-locked, providing the public cross-check for the private
      QP73 frozen surface?
```

## Declared Premises

```text
P1. QP arm bridge graph:
      Each QP test in scope declares next_frontier in its summary.json.
      Walking next_frontier from qp004 must terminate at qp075 or at
      a terminal "campaign_closure" marker.
      Disconnections in the graph indicate broken reproduction.

P2. SUK/QGA arm artifacts:
      SUK015/QGA054 row mass readout, SUK016/QGA055 full strict native
      particle ledger, SUK017/QGA056 native particle ledger predictor
      surface, and SUK021/QGA060 particle engine completion surface
      must all be present with hash-locked artifacts.

P3. QP071 SUK gate bridge:
      C:\VS\quantum_phase\artifacts\qp071\parent_suk_gate_draft\
      must exist and contain a sam_mass_patch.py (or equivalent
      bridge artifact).
      QP071's summary must reference both QP arm and SUK kernel campaign
      lineage.

P4. Phase4 frozen tables (load-bearing reproduction surface):
      C:\VS\quantum_phase\phase4_tables\parameter_free_particle_table.csv
      C:\VS\quantum_phase\phase4_tables\parameter_free_particle_table_with_gauge_bosons.csv
      C:\VS\quantum_phase\phase4_tables\particle_periodic_matrix.csv
      C:\VS\quantum_phase\phase4_tables\particle_composite_freeze_v2.csv
      All must match their manifest-locked sha256.

P5. G616c public cross-check:
      C:\VS\Stam_model-A-v1.0\tests\Substrate\G616c_PARAMETER_FREE_MASS_CHAIN_CONSOLIDATION
      Must contain G616c_consolidation_table.csv and G616c_verdict.md
      Both must be hash-locked in the manifest.

P6. Cross-branch shared inputs:
      qp050 (symmetric isotope seed mass) and qp052 (numeric DeltaN
      binding mass) appear in BOTH the 09 and 10 manifests as shared
      inputs.  CR061 verifies their 09-side hashes; 10 verifies the
      cross-branch dependency in its own CRs.

P7. Reproduction load-bearing arm declaration:
      The declared load-bearing arm is the private QP arm at QP073/QP075.
      The public arm (G616c) is the cross-check.  Both must pass.
```

## Outcome Taxonomy

```text
PASS_SCOPED_STRUCTURAL:
  - All manifest hashes verify.
  - QP arm next_frontier graph traverses qp004 -> qp075 with no breaks.
  - SUK/QGA artifacts present and hash-locked.
  - QP071 SUK gate bridge artifact present.
  - Phase4 frozen tables hash-locked.
  - G616c public cross-check present and hash-locked.

BOUNDARY:
  - All hash-verification PASS conditions hold.
  - Bridge graph traverses but with one or more BOUNDARY-class steps
    (e.g., a proposal-class QP070 / QP074 that is documented as
    "proposal" not "freeze").  Expected default if not all phases
    reach PASS_SCOPED_STRUCTURAL.

FAIL:
  - Any required artifact hash fails verification.
  - The QP arm next_frontier graph has a hard break (a test that does
    not declare next_frontier or declares a non-existent successor).
  - QP071 SUK gate bridge missing.
  - Phase4 frozen tables missing or hash mismatch.
  - G616c cross-check missing or hash mismatch.

DIAGNOSTIC:
  - Manifest seal missing or sha mismatch.
  - Summary.json files unreadable or malformed.
  - CR runner cannot complete a phase due to environmental fault.
```

## Rule-9 Line

```text
This test could have falsified: the claim that the particle mass chain
reproduces byte-equivalent across the QP arm + SUK/QGA arm bridge,
with QP071 as the SUK gate connector, and that the public G616c
parameter-free mass chain consolidation cross-checks the private QP73
frozen surface.
```

## Expected Artifacts

```text
CR061_PRECOMMIT.md
CR061_MASS_CHAIN_REPRODUCTION.py
CR061_input_manifest.csv
CR061_qp_arm_bridge_graph.csv        (per QP test: declared next_frontier
                                      / observed successor / status)
CR061_suk_qga_arm_artifacts.csv      (per SUK/QGA test: artifact present /
                                      hash matches manifest)
CR061_qp071_suk_gate_bridge.json     (QP071 parent_suk_gate_draft
                                      verification)
CR061_phase4_freeze_check.csv        (per Phase4 table: hash match)
CR061_g616c_cross_check.json         (G616c verdict + table verification)
CR061_wrong_reproduction.csv         (declared adverse injections)
CR061_manifest_seal_check.json
CR061_summary.json
CR061_result.md
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: simulate a manifest row whose declared sha256 differs from on-disk
     (Phase4 table hash mismatch)  -> expected: FAIL on P4

WC2: simulate a missing QP071 parent_suk_gate_draft directory
     -> expected: FAIL on P3

WC3: simulate a broken next_frontier link (qp004's summary.json
     references a non-existent qp999)
     -> expected: FAIL on P1

WC4: simulate a missing G616c_consolidation_table.csv
     -> expected: FAIL on P5

WC5: corrupt SOURCE_MANIFEST.csv so the CR059 seal mismatches
     -> expected: DIAGNOSTIC on manifest seal

WC6: simulate an absent SUK/QGA arm artifact (QGA055 missing)
     -> expected: FAIL on P2
```

## Sealed Premise Set

```text
The premise set P1-P7 above is sealed at CR061_PRECOMMIT write time.
No CR061 runner may add or alter a premise.
```
