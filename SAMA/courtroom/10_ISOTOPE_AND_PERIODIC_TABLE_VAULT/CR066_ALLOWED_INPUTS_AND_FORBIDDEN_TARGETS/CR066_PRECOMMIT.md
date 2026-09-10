# CR066 Allowed Inputs and Forbidden Targets - Precommit

```text
document_id:    CR066_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR066
sealed_before:  CR066 runner exists and CR066 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv  (locked by CR065)
                manifest sha256: cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
date_local:     2026-06-13
```

## Rule

```text
Verify that no QP isotope vault construction step consumes an externally
measured isotope value, an external authority roster value, or any
post-observation calibration source as a construction input.
Verify that QP049-QP060 (the vault construction chain) each declare
external_data_used=false in their summary.json, and that QP061 is the
only QP test that explicitly admits external data (the IAEA LiveChart
roster) and uses it only as a post-construction comparator.
Verify QP068 (high-Z miss structure analysis) self-discloses no
construction-input consumption.
```

## Question

```text
Can the QP isotope vault input boundary be verified such that:
  (a) QP049-QP060 each declare external_data_used=false,
      observed_isotope_masses_used=false, observed_decay_modes_used=false,
      observed_half_lives_used=false, observed_abundances_used=false,
      and free_parameters_introduced=0 in their respective summary.json,
  (b) QP061 admits external IAEA data only as a comparator AFTER its
      construction surface is fixed (sealed comparison protocol),
  (c) QP068 (high-Z miss structure analysis) consumes only QP049-QP060
      outputs and no observed superheavy isotope value,
  (d) No engine-surface code token consumes AME2020, NIST, IUPAC, or
      any other external roster value as a construction input,
  (e) The CR065 manifest seal is intact and the vault's input boundary
      can be re-verified against the locked manifest?
```

## Declared Premises

```text
P1. Vault construction chain (QP049-QP060):
      qp049 isotope seed identity
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
      qp060 sealed comparison protocol  (pre-comparison state)

P2. Vault external-anchor step:
      qp061 IAEA LiveChart comparison
      This is the ONLY QP test in scope that admits external data.
      qp061 must use the external data only as a post-construction
      comparator (verified via qp061_summary.json fields:
      external_data_used=true AND the construction surface inherited
      from qp060 sealed protocol).

P3. Vault frontier prediction step:
      qp068 high-Z sealed miss structure readout
      Must declare external_data_used=false and consume only QP049-QP060
      outputs.  No observed superheavy isotope value may enter the
      prediction-table construction.

P4. Per-test self-disclosure required fields:
      external_data_used                  (boolean)
      observed_isotope_masses_used        (boolean)
      observed_decay_modes_used           (boolean)
      observed_half_lives_used            (boolean)
      observed_abundances_used            (boolean)
      free_parameters_introduced          (integer)

P5. Forbidden construction-input classes:
      - AME2020 mass column read as construction input
      - NIST nuclide chart read as predictor seed
      - IUPAC element name registry read as anything other than
        post-derivation naming
      - any post-observation calibration loop using IAEA / AME / NIST
        roster values
      - any selector whose parameters are tuned to match an observed
        isotope mass

P6. Sealed comparison protocol (qp060):
      qp060_summary.json must declare:
        external_data_used               = false
        observed_isotope_masses_used     = false
        free_parameters_introduced       = 0
        next_frontier                    = explicit reference to qp061
                                           as the external-data step
      The transition from qp060 to qp061 must be the ONLY point in the
      vault chain where external data enters, and must be declared in
      qp060's next_frontier field.

P7. Cross-branch boundary:
      qp050 and qp052 are shared with 09. CR066 may consume them as
      shared mass-surface inputs. CR066 may NOT consume 09's particle
      row partition (G616c strict/audit rows are 09's territory).

P8. Manifest seal:
      10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv.sha256.txt
      must exist and match the on-disk SOURCE_MANIFEST.csv hash
      cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2.
```

## Outcome Taxonomy

```text
PASS:
  - QP049-QP060 each declare external_data_used=false and
    free_parameters_introduced=0 in their summary.json.
  - QP060 explicitly names qp061 as the external-data step.
  - QP061 admits external data only as a post-construction comparator.
  - QP068 declares external_data_used=false and consumes only QP049-QP060
    outputs.
  - No engine-surface code token in QP049-QP060 or QP068 reads AME2020,
    NIST, or IUPAC values as construction inputs.
  - CR065 manifest seal intact.

BOUNDARY:
  - All PASS conditions hold structurally.  Expected default verdict
    for CR066. K1 external anchor is at CR069.

FAIL:
  - Any qpNNN_summary.json among QP049-QP060 or QP068 reports
    external_data_used=true (only QP061 may).
  - Any free_parameters_introduced > 0 in QP049-QP060 or QP068.
  - Engine-surface code token consumes AME2020/NIST/IUPAC as construction
    input.
  - QP060 does not name qp061 as the next_frontier external-data step.

DIAGNOSTIC:
  - A qpNNN_summary.json is missing or malformed.
  - CR065 manifest seal missing or sha mismatch.
  - Required self-disclosure field absent from any qpNNN_summary.json.
```

## Rule-9 Line

```text
This test could have falsified: the claim that the QP isotope vault
construction chain (QP049-QP060 + QP068) consumes no externally
measured isotope value, no external authority roster value, and no
post-observation calibration source as a construction input, and that
the only point of external-data admission is QP061 as a post-
construction comparator.
```

## Expected Artifacts

```text
CR066_PRECOMMIT.md
CR066_ALLOWED_INPUTS_AND_FORBIDDEN_TARGETS.py
CR066_input_manifest.csv
CR066_qp_self_disclosure_check.csv   (per qpNNN: declared fields / verdict)
CR066_qp060_boundary_check.json      (sealed comparison protocol verification)
CR066_qp061_comparator_role_check.json (qp061 is comparator-only verification)
CR066_forbidden_input_scan.csv       (engine-surface code-token matches)
CR066_manifest_seal_check.json
CR066_wrong_controls.csv
CR066_summary.json
CR066_result.md
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: inject a fabricated qpNNN_summary.json (for QP049-QP060) declaring
     external_data_used=true and observed_isotope_masses_used=true
     -> expected: FAIL on P1/P4

WC2: inject a synthetic engine .py code token containing
     ame2020_table.read_csv() as a construction input
     -> expected: FAIL on P5

WC3: inject a qp060_summary.json missing the next_frontier reference to
     qp061
     -> expected: FAIL on P6

WC4: inject a qp068_summary.json declaring external_data_used=true
     -> expected: FAIL on P3

WC5: corrupt one byte of SOURCE_MANIFEST.csv so the CR065 seal mismatches
     -> expected: DIAGNOSTIC on P8

WC6: inject a free_parameters_introduced=1 value into a vault-chain
     summary.json
     -> expected: FAIL on P4
```

## Sealed Premise Set

```text
The premise set P1-P8 above is sealed at CR066_PRECOMMIT write time.
No CR066 runner may add or alter a premise.  If a premise needs
revision after CR066 runs, the revision belongs to an appeal CR per the
Appeal Channel section of the 10 seal.
```
