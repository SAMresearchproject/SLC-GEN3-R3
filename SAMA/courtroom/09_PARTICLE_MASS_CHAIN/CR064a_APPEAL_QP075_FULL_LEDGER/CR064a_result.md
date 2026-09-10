# CR064a Appeal - QP075 Full Ledger Extension

## Verdict

```text
CR064a_APPEAL_PASS_K1_EXTENSION_TO_QP075_FULL_LEDGER_WITH_OPERATOR_BACKBONE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = APPEAL_PASS_K1_EXTENSION_TO_QP075_FULL_LEDGER_WITH_OPERATOR_BACKBONE
triage_bin = A
appeal_type = content_addition_M3_channel
```

## Reason

```text
35-row QP075 campaign closure + 26-row operator backbone; 0 free parameters across both surfaces; bridge integrity clean (orphan_ops=0 informational only)
```

## What This Appeal Records

```text
CR062 scope (immutable):   15 rows (12 PDG point-residual + 3 neutrino
                                    boundary) from 15-row gauge-bosons CSV
CR064a appeal scope:       35 rows (32 PDG-anchored + 3 lattice-anchored)
                           paired with 26-row operator backbone
Free parameters total:     0  (across campaign closure + operator inventory)
Immutability:              CR062 + CR064 files unchanged
```

## Headline Aggregate

```text
PDG-strict      32 rows within 1.0%
PDG-audit       0 rows within 2.0%
Lattice         3 rows within 5.0%
Operators       26 in inventory, all with 0 free params
Bridge          orphan_campaign_rows=0  orphan_operators=0
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

## Honest Process Note

CR062 used `phase4_parameter_free_particle_table_with_gauge_bosons.csv`
(15 rows: 12 PDG point-residual + 3 neutrino boundary).  At CR062
execution time, QP062-QP075 had already produced a 35-row campaign
closure surface and 26-row operator backbone.  CR064a now records
that broader contact as a content-addition appeal under the seal's M3
channel.

Per courtroom rule, CR062 result and CR064 branch verdict files are
preserved as recorded.  CR064a writes only its own outputs.

This is not pretty.  It is not deleting files either.

## Artifacts

- `CR064a_input_manifest.csv`
- `CR064a_campaign_closure_ledger.csv`
- `CR064a_role_operator_inventory.csv`
- `CR064a_bridge_integrity_check.csv`
- `CR064a_strict_summary.json`
- `CR064a_audit_summary.json`
- `CR064a_lattice_boundary_summary.json`
- `CR064a_free_parameters_check.json`
- `CR064a_immutability_check.json`
- `CR064a_wrong_controls.csv`
- `CR064a_manifest_seal_check.json`
- `CR064a_summary.json`
- `CR064a_revised_strongest_claim.md`
- `HASHES.txt`
