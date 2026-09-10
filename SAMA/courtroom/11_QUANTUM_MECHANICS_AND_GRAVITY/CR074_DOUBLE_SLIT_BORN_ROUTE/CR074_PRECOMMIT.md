# CR074 Double Slit / Born Route - Precommit

```text
document_id:    CR074_PRECOMMIT
branch:         11_QUANTUM_MECHANICS_AND_GRAVITY
cr_slot:        CR074
sealed_before:  CR074 runner exists and CR074 result exists
seal_anchor:    SEALED_QUANTUM_MECHANICS_AND_GRAVITY_SCOPE_APPROACH_2026_06_13
                (sha256: f80c93f67da67a5c9286aafe845316ee6fa3a614439c4e9e120abb9c3a9207dc)
manifest:       11_QUANTUM_MECHANICS_AND_GRAVITY/SOURCE_MANIFEST.csv (sealed by CR073)
date_local:     2026-06-13
```

## Rule

```text
Verify that the Born rule is reproduced in SAM substrate language as
route weighting over unresolved exposure:
    probability  ~  |amplitude|^2  ~  route_weight
and that the Born rule emerges from substrate route counting, not from
an external probability postulate.
Theorem-grade structural reproduction; no per-row K1.
```

## Question

```text
Does QP014 (Born rule route weight bridge) reproduce the Born rule as
route weighting such that:
  (a) "Born rule" / |amplitude|^2 / route_weight identity patterns are
      present in source documentation,
  (b) qp014 free_parameters_introduced = 0,
  (c) no engine-surface fit loop targets observed probabilities,
  (d) double-slit / interference test artifact present (any G/QGA test
      with Born or interference reference)?
```

## Declared Premises

```text
P1. Load-bearing sources (hash-locked):
      C:\VS\quantum_phase\src\qp014_*.py
      C:\VS\quantum_phase\artifacts\qp014\qp014_summary.json
      C:\VS\quantum_phase\docs\reports\QP014_*.md
      SAMs_TOE 05_quantum_phase/README.md (Born route documentation)

P2. Identity patterns:
      Born rule:   "Born rule"  OR  "|amplitude|" with "^2" / "squared"
                                OR  "|psi|^2"
      route weight: "route weight" OR "route weighting"
                                OR "route interference"
      bridge:      QP014 title literal "Born rule route weight bridge"

P3. QP014 free_parameters_introduced = 0.

P4. No engine-surface fit loop on observed probability.

P5. Cross-cite: G421 (Born rule public bridge test) present (already
    verified by CR073 phase 7; rolled forward here).

P6. Manifest seal intact (rolled forward from CR073).
```

## Outcome Taxonomy

```text
PASS_SCOPED_STRUCTURAL_BORN_ROUTE:
  - All identity patterns matched; qp014 zero free params;
    G421 present; engine-surface clean; wrong controls trip.

BOUNDARY:
  - Patterns partial (e.g., "Born" present but |amplitude|^2 absent).

FAIL:
  - Engine-surface probability fit detected.
  - qp014 free_parameters_introduced > 0.

DIAGNOSTIC:
  - Manifest seal mismatch.
  - QP014 source unreadable.
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM reproduces the Born
rule as route weighting over unresolved exposure without an external
probability postulate or fit-to-observation loop.
```

## Expected Artifacts

```text
CR074_PRECOMMIT.md
CR074_DOUBLE_SLIT_BORN_ROUTE.py
CR074_input_manifest.csv
CR074_born_identity_check.json
CR074_route_weight_check.json
CR074_qp014_disclosure_check.json
CR074_engine_surface_fit_scan.csv
CR074_public_bridge_cite_check.csv
CR074_manifest_seal_check.json
CR074_wrong_controls.csv
CR074_summary.json
CR074_result.md
HASHES.txt
```

## Wrong Controls (declared)

```text
WC1: simulated fit loop targeting observed probability -> FAIL
WC2: qp014 free_parameters_introduced=1                -> FAIL
WC3: absent Born identity pattern                       -> DIAGNOSTIC
WC4: absent route-weight pattern                        -> BOUNDARY
WC5: corrupt manifest seal                              -> DIAGNOSTIC
WC6: Born pattern in a "we do NOT use" comment context  -> presence
     recorded; fit-scan separate (phase isolation)
```

## Sealed Premise Set

```text
P1-P6 sealed at CR074_PRECOMMIT write time.
```
