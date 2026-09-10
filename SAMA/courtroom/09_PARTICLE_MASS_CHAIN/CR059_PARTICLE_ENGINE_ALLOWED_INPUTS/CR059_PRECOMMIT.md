# CR059 Particle Engine Allowed Inputs - Precommit

```text
document_id:    CR059_PRECOMMIT
branch:         09_PARTICLE_MASS_CHAIN
cr_slot:        CR059
sealed_before:  CR059 runner exists and CR059 result exists
seal_anchor:    SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13
                (sha256: ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8)
manifest:       09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv  (572 entries)
date_local:     2026-06-13
```

## Rule

```text
Do not consume any externally measured particle mass value, Yukawa coupling
table, or post-observation calibration source as a construction input.
Use only the SAM-native closed-form input set declared below.
Use only artifacts whose sha256 was captured in SOURCE_MANIFEST.csv before
CR059 runs.
Treat measured-mass references as post-derivation comparators only, never
as construction inputs.
```

## Question

```text
Can the particle engine input boundary be declared and locked such that:
  (a) the allowed input set is exactly the SAM-native closed-form constants,
  (b) every source artifact consumed by the engine is recorded in
      SOURCE_MANIFEST.csv with a captured sha256,
  (c) no forbidden input class appears anywhere in the declared engine
      surface, and
  (d) the declaration is independently verifiable by re-running this CR
      against the same manifest?
```

## Declared Premises

```text
P1. Allowed-input set (closed form):
      A_0          = 1/(12*pi)
      alpha_em     = (alpha_em as fixed structural input per PRIORITY_RECORD)
      D            = 3                  (derived inside SAM at theorem grade)
      alpha_H      = 2                  (derived at structural-argument grade)
      R            = 12                 (alpha_H^2 * D)
      S            = 1 - A_0 - alpha_em (G505 screen theorem)
      m_P          = (Planck mass anchor as fixed structural input)
      tier_n       = the layered set {alpha_H^i * D^j} per G544b

P2. Engine scope marker:
      QGA060 (= SUK021) PARTICLE_ENGINE_COMPLETION_SURFACE is the canonical
      scope marker for what counts as "the engine."
      qp020 PRIVATE_QP_TO_PARTICLE_BRIDGE_READINESS_PACKAGE is the QP arm
      readiness declaration.

P3. Source artifact hygiene:
      Every artifact consumed by the engine is listed in
      09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv with:
        - item_id
        - sha256 captured before CR059 runs
        - source_repo and source_commit
        - target_cr declaration

P4. Forbidden input classes (mass-side):
      - PDG-listed mass values
      - AME2020 mass column
      - NIST particle / nuclide mass values
      - any post-observation calibration loop output
      - any selector whose construction reads a measured mass
      - any Yukawa coupling table (from fits, RG running, or measurement)
      - any CKM/PMNS matrix element used as construction input
      - any post-2026-06-13 measurement used to backfit the engine

P5. Forbidden input classes (route-side):
      - DS-tier / decontamination-vestibule / playground artifacts
      - FRZ_* freeze-queue entries that have not been promoted
      - any artifact not appearing in SOURCE_MANIFEST.csv

P6. Memory-layer rule:
      Lab-tier memory references (PRIORITY_RECORD, PASS_LOG, FAILURE_LOG,
      DIRECTIVE_INDEX, OPERATIONAL_MEMORY) are allowed as provenance
      pointers. Discovery-tier entries within those files (DS*, DCH_*,
      FRZ_*) are not allowed as construction inputs even when cited.

P7. Cross-branch boundary:
      The 09 branch must not consume any artifact whose target_cr in
      SOURCE_MANIFEST.csv points only at the 10 branch.
      The 10 branch's CR065-CR072 deliverables are out of scope.
```

## Outcome Taxonomy

```text
PASS:
  - SOURCE_MANIFEST.csv is complete and every entry has a verifiable
    sha256.
  - The declared P1 input set matches what the QP arm + SUK/QGA arm
    actually consumed.
  - No row in SOURCE_MANIFEST.csv falls into a P4 or P5 forbidden class.
  - Cross-branch boundary P7 holds.
  - SOURCE_MANIFEST.csv sha256 is captured into CR059_summary.json and
    promoted to the manifest's sibling .sha256.txt at CR059 execution.

BOUNDARY:
  - All PASS conditions hold structurally, but CR059 does not by itself
    contact any external mass roster. The K1 anchor lights up at CR062.
  - This is the expected default verdict for CR059.

FAIL:
  - Any row in SOURCE_MANIFEST.csv falls into a P4 or P5 forbidden class.
  - The declared P1 input set is contradicted by the actual engine
    surface (e.g., a measured mass value reaches a construction step).
  - The cross-branch boundary P7 is violated.

DIAGNOSTIC:
  - SOURCE_MANIFEST.csv is incomplete (engine consumes an artifact not
    listed in the manifest).
  - sha256 mismatch between SOURCE_MANIFEST.csv and on-disk file.
  - source_commit in SOURCE_MANIFEST.csv does not match current
    source repo HEAD without an explicit pin note.
  - Test cannot produce a complete allowed-input verification.
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's particle engine
input boundary excludes externally measured particle mass values,
Yukawa coupling tables, and post-observation calibration sources, and
that every artifact consumed by the engine is independently hash-
locked through SOURCE_MANIFEST.csv.
```

## Forbidden Route Cross-Reference

CR059 inherits the DIRECTIVE_INDEX Forbidden Route rule verbatim:

```text
known SM mass roster value
-> retrofit STAM derivation step
-> retrofitted STAM explanation
```

Any candidate input that walks this route is reported as a P4 violation
and triggers FAIL.

CR059 also inherits the DIRECTIVE_INDEX drift guard:

```text
Residuals are fields, not verdict criteria.
```

A residual against an observed mass value is NOT a CR059 input. It is
post-derivation comparator data and belongs to CR062 row-by-row ledger.

## Expected Artifacts

```text
CR059_PRECOMMIT.md                  (this file)
CR059_PARTICLE_ENGINE_ALLOWED_INPUTS.py   (runner script)
CR059_input_manifest.csv            (subset of SOURCE_MANIFEST.csv that
                                     CR059 actually reads)
CR059_allowed_input_check.csv       (per P1 entry: declared / found /
                                     status)
CR059_forbidden_input_scan.csv      (per P4 / P5 class: scan result /
                                     match count / verdict)
CR059_cross_branch_check.csv        (per P7: artifact / target_cr /
                                     status)
CR059_memory_layer_audit.csv        (per memory file: lab-tier rule
                                     hits / DS-tier hits / verdict)
CR059_source_manifest_hash.json     (sha256 of SOURCE_MANIFEST.csv at
                                     time of CR059 run)
CR059_wrong_controls.csv            (declared wrong inputs - measured
                                     mass injection, Yukawa-table
                                     injection, DS-tier injection -
                                     must all fail to pass the gate)
CR059_summary.json                  (machine-readable verdict)
CR059_result.md                     (human-readable verdict)
HASHES.txt                          (sha256 of all CR059 output files)
```

## Wrong Controls (declared in advance)

CR059's wrong-control set must include at least these injections, and
each must trigger a FAIL outcome when CR059 runs against the injected
manifest:

```text
WC1: inject a row into SOURCE_MANIFEST.csv that references a PDG mass
     value file as construction input  -> expected: FAIL on P4
WC2: inject a Yukawa coupling table reference as construction input
     -> expected: FAIL on P4
WC3: inject a DS-tier discovery brief as a target_cr=CR061 input
     -> expected: FAIL on P5
WC4: corrupt one sha256 in SOURCE_MANIFEST.csv so on-disk hash differs
     -> expected: DIAGNOSTIC on hash mismatch
WC5: inject a 10-branch-only artifact (a QP049-only file) as a CR061
     input  -> expected: FAIL on P7
WC6: inject a freeze-queue entry (FRZ_DS002_*) as a construction input
     -> expected: FAIL on P5
```

All six WC inputs must produce the declared adverse verdict. If any
wrong control passes, CR059's own verdict downgrades to DIAGNOSTIC and
the test is rerun.

## Hash Anchor Statement

```text
SOURCE_MANIFEST.csv was built before CR059 runs.
The manifest's sha256 will be captured by CR059 into
  CR059_source_manifest_hash.json
and promoted to
  09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv.sha256.txt
at CR059 execution. Once promoted, no CR after CR059 may consume any
artifact whose sha256 is not in the locked manifest.
```

## Sealed Premise Set

```text
The premise set P1-P7 above is sealed at CR059_PRECOMMIT write time.
No CR059 runner may add or alter a premise. If a premise needs revision
after CR059 runs, the revision belongs to an appeal CR per the Appeal
Channel section of the 09 seal.
```
