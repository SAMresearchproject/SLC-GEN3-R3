# CR064a Appeal - QP075 Full Ledger Extension - Precommit

```text
document_id:    CR064a_PRECOMMIT
branch:         09_PARTICLE_MASS_CHAIN
cr_slot:        CR064a  (appeal appendix to CR064 branch verdict)
sealed_before:  CR064a runner exists and CR064a result exists
seal_anchor:    SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13
                (sha256: ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8)
manifest:       09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv  (sha256 d605d070...)
date_local:     2026-06-13
appeal_basis:   seal Appeal Channel M3 - content addition
```

## What This Appeal Is, And What It Is Not

```text
What this appeal IS:
  CR062 scored 12 PDG point-residual rows plus 3 neutrino upper-bound
  boundary rows, drawn from
    phase4_parameter_free_particle_table_with_gauge_bosons.csv (15-row
    elementary + electroweak surface).
  At CR062 execution time, the QP062-QP075 composite extension was already
  complete, producing a 35-row campaign closure surface in
    artifacts/qp075/qp075_campaign_closure_summary_table.csv
  and a 26-row role-operator inventory in
    artifacts/qp075/qp075_role_operator_closure_table.csv
  CR062 did not consume those larger surfaces.  CR064a now records the
  K1 contact against the QP075 35-row surface as a content addition to
  the branch.

What this appeal IS NOT:
  CR064a does NOT modify CR062_result.md, CR062_summary.json, or any
  CR062 output file.  CR062's verdict
    PASS_SCOPED_K1_ROW_LEVEL
  stands as recorded, on its declared 15-row scope.
  CR064a does NOT modify CR064 branch-verdict files.  CR064's verdict
    PASS_SCOPED_09_BRANCH_K1_VERIFIED
  stands as recorded.
  CR064a does NOT delete or rename any existing CR artifact.
  CR064a does NOT claim CR062 was wrong on its declared scope.  It
  claims the declared scope was narrower than the available source
  surface at the time.

Courtroom plain language:
  This is not pretty.  It is not deleting files either.
```

## Rule

```text
Read the QP075 campaign closure surface (35 rows) and role-operator
inventory (26 operators) as the appeal source.  Apply grade partition
per row's reference_label:

  PDG-anchored rows (32 of 35):
    strict tolerance  = 1.0%   (matches CR062 elementary band)
    audit tolerance   = 2.0%
  Lattice-anchored rows (3 of 35: Xi_bc, Omega_bcs, Omega_bbc):
    boundary tolerance = 5.0%  (proposal-class lattice comparison)

Verify the role-operator backbone:
  Every campaign-closure row's role_operator_or_ladder field maps to
  either "V4.1 ladder" or one of the 26 named role operators in
  qp075_role_operator_closure_table.csv.
  Every named operator carries 0 free_parameters_used.
  Every campaign row carries 0 free_parameters_used.
```

## Question

```text
Does the QP075 35-row campaign closure surface, paired with the 26-row
role-operator backbone, contact PDG (for the 32 PDG-anchored rows) and
lattice references (for the 3 doubly/multi-heavy BC baryon rows)
within declared per-grade tolerances, with 0 free parameters across
every row and operator?
```

## Declared Premises

```text
P1. Source files (already hash-locked in 09 SOURCE_MANIFEST.csv via CR059):
      artifacts/qp075/qp075_campaign_closure_summary_table.csv
      artifacts/qp075/qp075_role_operator_closure_table.csv

P2. Row partition by reference_label:
      label contains "PDG"     -> PDG-anchored row
      label contains "lattice" -> lattice-anchored row
      else                     -> DIAGNOSTIC (unrecognized authority)

P3. Per-grade tolerance bands:
      PDG strict     residual| <= 1.0%
      PDG audit      residual| <= 2.0%   (carrier_or_symbol-level
                                          audit-grade markers if any)
      Lattice        residual| <= 5.0%   (proposal-class)

P4. Per-row verdict logic uses the residual_percent column directly
    from the source files (this is the upstream-computed value).
    CR064a does NOT recompute residuals from predicted_MeV /
    reference_MeV - it reads the audit-trail value the campaign sealed.

P5. Role-operator backbone verification:
      For each campaign-row whose role_operator_or_ladder is NOT
      "V4.1 ladder", the value must appear in the
      qp075_role_operator_closure_table.csv role_operator column.
      Orphan campaign-row entries (referencing a non-existent operator)
      are FAIL.
      Orphan operators (named in inventory but absent from campaign-row
      assignments) are DIAGNOSTIC.

P6. Zero free parameters check:
      free_parameters_used column must equal 0 across all 35 campaign
      rows AND all 26 operator inventory rows.  Any non-zero value
      anywhere is FAIL.

P7. CR062 and CR064 result files remain immutable.  CR064a writes only
    its own result.md + ledger CSV + appeal summary + HASHES.txt.
    No file under CR062_* or CR064_* directories is touched.

P8. CR065 manifest seal intact (rolled forward from CR059).
```

## Outcome Taxonomy

```text
APPEAL_PASS_K1_EXTENSION_TO_QP075_FULL_LEDGER_WITH_OPERATOR_BACKBONE:
  - All 32 PDG-anchored rows within their grade tolerance.
  - All 3 lattice-anchored rows within boundary tolerance 5.0%.
  - 0 free parameters across all 35 + 26 rows.
  - Role-operator bridge: no orphan campaign-rows; no orphan operators.
  - Records K1 surface extension from 15-row CR062 scope to 35-row
    QP075 scope without modifying CR062 or CR064.

BOUNDARY_PARTIAL_K1_EXTENSION:
  - All PDG-anchored rows pass, but one or more lattice rows exceed
    5.0% boundary tolerance (would extend with a wider lattice band
    declaration in a future appeal).

FAIL_APPEAL:
  - Any PDG-anchored row exceeds its grade tolerance (would
    retroactively raise concern about CR062's strict subset too).
  - Free parameters > 0 anywhere.
  - Orphan campaign-row referencing a non-existent operator.

DIAGNOSTIC:
  - Manifest seal mismatch.
  - Source file missing or unreadable.
  - Reference_label unrecognized authority.
  - Predicted/reference/residual columns missing or non-numeric.
```

## Rule-9 Line

```text
This test could have falsified the claim that the QP075-extended
35-row campaign closure surface, paired with the 26-row role-operator
backbone, contacts PDG (32 rows) and lattice (3 rows) references
within declared per-grade tolerances and zero free parameters,
without modifying CR062's earlier 15-row K1 PASS or CR064's branch
verdict.
```

## Forbidden Language

```text
"CR062 was wrong"
"CR062 missed rows"
"CR062 is superseded"
"The 09 branch verdict from CR064 is invalid"
"CR064 should be re-run"

These statements are forbidden per courtroom rule.  CR062 and CR064
recorded what they recorded on their declared scopes.  CR064a records
a broader scope as a content addition.
```

## Allowed Language

```text
"CR062 K1 scope was 15 rows from the gauge-bosons CSV; QP075 closure
 surface is 35 rows; CR064a records the 20-row composite extension."
"For the new repo export, the canonical K1 row table is QP075
 35-row campaign closure paired with the 26-row operator inventory."
"CR062 verdict PASS_SCOPED_K1_ROW_LEVEL stands on its declared scope."
"CR064 verdict PASS_SCOPED_09_BRANCH_K1_VERIFIED stands."
"CR064a records APPEAL_PASS_K1_EXTENSION_TO_QP075_FULL_LEDGER
 WITH_OPERATOR_BACKBONE as a content-addition appeal."
```

## Expected Artifacts

```text
CR064a_PRECOMMIT.md
CR064a_APPEAL_QP075_FULL_LEDGER.py
CR064a_input_manifest.csv
CR064a_campaign_closure_ledger.csv     (35 rows + per-row verdict)
CR064a_role_operator_inventory.csv     (26 operators + verdict)
CR064a_bridge_integrity_check.csv      (operator <-> campaign row map)
CR064a_strict_summary.json
CR064a_audit_summary.json
CR064a_lattice_boundary_summary.json
CR064a_free_parameters_check.json
CR064a_immutability_check.json         (verifies CR062 + CR064 untouched)
CR064a_wrong_controls.csv
CR064a_manifest_seal_check.json
CR064a_summary.json
CR064a_result.md
CR064a_revised_strongest_claim.md      (for new repo export; does NOT
                                        replace CR064_branch_strongest_claim.md)
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: perturb one PDG-anchored row's residual to +2.0% (above strict band)
     -> FAIL_APPEAL detection wired
WC2: inject a campaign row with role_operator_or_ladder = "phantom_operator"
     -> orphan campaign-row detection wired
WC3: inject an operator in the 26-row table that no campaign row references
     -> orphan operator detection wired
WC4: inject free_parameters_used = 1 in any row
     -> FAIL_APPEAL on P6
WC5: corrupt SOURCE_MANIFEST.csv seal
     -> DIAGNOSTIC
WC6: simulate CR062 result file modification (forbidden per P7)
     -> immutability check trips
```

## Sealed Premise Set

```text
P1-P8 sealed at CR064a_PRECOMMIT write time.
```
