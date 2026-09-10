# CR062 Row-by-Row Particle Ledger - Precommit

```text
document_id:    CR062_PRECOMMIT
branch:         09_PARTICLE_MASS_CHAIN
cr_slot:        CR062
sealed_before:  CR062 runner exists and CR062 result exists
seal_anchor:    SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13
                (sha256: ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8)
manifest:       09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv
                manifest sha256: d605d070281119f2c874112de0be1be06d6ab4ad5ef8b914e459420c8148f22a
date_local:     2026-06-13
```

## Rule

```text
Verify per-row that SAM's parameter-free particle predictions contact
PDG 2024 observed masses within their declared tolerance band.  Use
the row-partition declared by the frozen tables:
  STRICT_PARAMETER_FREE rows: residual must be < 1%
  AUDIT_GRADE_PARAMETER_FREE rows: residual must be < 2%
  Proposal / boundary rows: no residual check, BOUNDARY only
PDG values are typed inputs to CR062 declared in P1 below, sourced from
Particle Data Group 2024 review (https://pdg.lbl.gov/2024/).
Per the seal's drift guard: residuals are recorded as fields, not as
verdict criteria - the verdict is whether the row satisfies its grade
tolerance, not the absolute residual value.
```

## Question

```text
For each row in the Phase4 parameter_free_particle_table_with_gauge_bosons
freeze, does SAM's parameter-free predicted mass contact the PDG 2024
observed value within the row's grade-declared tolerance band?

  Strict rows: H, e, mu, tau, u, s, c, b, W, Z (all < 1% residual)
  Audit rows: d, t (both < 2% residual)
  Boundary rows (neutrinos): predicted within PDG upper bound

This is the K1 external anchor slot for the 09 branch.
```

## Declared Pdg 2024 Values

```text
Source: Particle Data Group 2024 review (PDG 2024)
URL: https://pdg.lbl.gov/2024/
Captured at CR062_PRECOMMIT write time.  These values are typed inputs
and become hash-locked in CR062's input manifest.

Charged leptons (pole masses):
  e          = 0.51099895 MeV       (PDG 2024)
  mu         = 105.6583755 MeV      (PDG 2024)
  tau        = 1776.86 MeV          (PDG 2024)

Quarks (MS-bar at 2 GeV unless noted):
  u          = 2.16 MeV             (PDG 2024, MS-bar 2 GeV)
  d          = 4.67 MeV             (PDG 2024, MS-bar 2 GeV)
  s          = 93.4 MeV             (PDG 2024, MS-bar 2 GeV)
  c          = 1273.0 MeV           (PDG 2024, MS-bar at m_c)
  b          = 4183.0 MeV           (PDG 2024, MS-bar at m_b)
  t          = 172690 MeV           (PDG 2024, pole mass)

Bosons (pole masses):
  H          = 125250 MeV           (PDG 2024, 125.25 GeV)
  W          = 80369.2 MeV          (PDG 2024)
  Z          = 91187.6 MeV          (PDG 2024)

Neutrinos (upper bounds; no point mass):
  nu_e       <  2.0 eV               (= 2.0e-6 MeV; KATRIN 2022 / Planck)
  nu_mu      <  0.19 MeV             (oscillation + direct bound, conservative)
  nu_tau     <  18.2 MeV             (LEP / OPAL direct bound)
```

## Declared Premises

```text
P1. PDG 2024 values (above) are typed inputs to CR062.  They are NOT
    consumed by the engine as construction inputs (CR060 verified
    selector provenance is independent).  CR062 uses them only as
    post-derivation comparators.

P2. Row partition by frozen-table grade tag:
    STRICT_PARAMETER_FREE        -> 1.0% tolerance band
    AUDIT_GRADE_PARAMETER_FREE   -> 2.0% tolerance band
    FROZEN_PARENT_ROLE_OPERATOR_PREDICTION -> 1.0% tolerance band
                                              (parent-role-operator
                                              predictions are strict-
                                              equivalent for W/Z)
    FROZEN_V4_1_STRICT_PREDICTION -> 1.0% tolerance band
    FROZEN_V4_1_AUDIT_PREDICTION  -> 2.0% tolerance band
    Neutral leptons (nu_e, nu_mu, nu_tau): BOUNDARY only
                                              (no PDG point comparison;
                                              upper-bound check only)

P3. Required source tables:
    phase4_tables/phase4_parameter_free_particle_table_with_gauge_bosons.csv
    Must be hash-locked in 09 manifest (verified by CR059 + rolled
    forward by CR062 Phase 1).

P4. Residual formula:
    residual_pct = abs(predicted_MeV - observed_MeV) / observed_MeV * 100
    For neutrinos with upper-bound observed:
      within_bound = predicted_MeV <= observed_upper_bound_MeV
      residual_pct is recorded as "WITHIN_UPPER_BOUND" if within_bound

P5. Per-row verdict logic:
    PASS_SCOPED_ROW_LEVEL:  row's residual within its grade tolerance
    BOUNDARY_ROW_LEVEL:     audit row within audit band, OR neutrino
                            within upper bound
    FAIL_ROW_LEVEL:         residual exceeds row's grade tolerance

P6. Aggregate branch verdict:
    PASS_SCOPED_K1_ROW_LEVEL: all strict rows PASS_SCOPED_ROW_LEVEL,
                              all audit rows BOUNDARY_ROW_LEVEL or
                              PASS_SCOPED_ROW_LEVEL, all boundary rows
                              BOUNDARY_ROW_LEVEL.
    BOUNDARY:                 any strict row at BOUNDARY without FAIL.
    FAIL:                     any strict OR audit row FAIL_ROW_LEVEL.
    DIAGNOSTIC:               manifest seal mismatch, frozen table
                              missing or hash mismatch, row identifier
                              column missing.

P7. Wrong controls (declared in advance):
    Engine predicted mass perturbations of declared magnitude must
    trigger FAIL_ROW_LEVEL for strict rows.  This validates the
    detection logic.
```

## Row Identity And Grade Partition

```text
Strict-grade rows (1.0% tolerance):
  H, e, mu, tau, u, s, c, b, W, Z
Audit-grade rows (2.0% tolerance):
  d, t
Boundary rows (upper-bound check only):
  nu_e, nu_mu, nu_tau
```

## Outcome Taxonomy

```text
PASS_SCOPED_K1_ROW_LEVEL:
  - Manifest hashes verify; frozen table hash-locked.
  - Every strict row contacts PDG within 1.0% tolerance.
  - Every audit row contacts PDG within 2.0% tolerance.
  - Every neutrino row sits at or below the PDG upper bound.
  - Per-row verdict table emitted with explicit grade column.

BOUNDARY:
  - Strict rows clean, audit rows clean, but one or more strict
    rows resolve to BOUNDARY_ROW_LEVEL rather than PASS_SCOPED_ROW_LEVEL
    (e.g., a strict row missing observed value entirely; partial
    contact).

FAIL:
  - Any strict row exceeds 1.0% residual against PDG.
  - Any audit row exceeds 2.0% residual.
  - Any neutrino predicted mass exceeds the documented PDG upper bound.

DIAGNOSTIC:
  - Manifest seal mismatch, frozen table missing, or required column
    absent from the frozen table.
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's parameter-free
particle predictions contact the PDG 2024 observed masses within
1.0% for strict-grade rows, within 2.0% for audit-grade rows, and
at-or-below the PDG upper bound for neutrino rows, derived from the
same engine that produced the Phase4 frozen tables under zero free
parameters.
```

## Expected Artifacts

```text
CR062_PRECOMMIT.md
CR062_ROW_BY_ROW_PARTICLE_LEDGER.py
CR062_input_manifest.csv
CR062_pdg_2024_typed_inputs.json     (PDG values pinned for this CR)
CR062_row_by_row_ledger.csv          (per-row: symbol / predicted /
                                      observed / residual_pct / grade /
                                      verdict)
CR062_strict_grade_summary.json      (strict rows aggregate)
CR062_audit_grade_summary.json       (audit rows aggregate)
CR062_boundary_grade_summary.json    (neutrino rows aggregate)
CR062_wrong_controls.csv
CR062_manifest_seal_check.json
CR062_summary.json
CR062_result.md
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: perturb the e row's predicted mass by +5% -> expected: FAIL_ROW_LEVEL
WC2: perturb the d row's predicted mass by +3% -> expected: FAIL_ROW_LEVEL
WC3: assign nu_e an upper-bound-violating predicted mass (10 eV)
     -> expected: FAIL_ROW_LEVEL
WC4: remove a strict row from the frozen table -> expected: DIAGNOSTIC
     (missing row identifier)
WC5: corrupt SOURCE_MANIFEST.csv -> expected: DIAGNOSTIC on seal mismatch
WC6: declare a 0% tolerance band for strict rows (perturbation test)
     -> expected: any actual non-zero residual triggers FAIL_ROW_LEVEL
     (validates that the tolerance logic IS doing work)
```

## Sealed Premise Set

```text
The premise set P1-P7 above is sealed at CR062_PRECOMMIT write time.
```
