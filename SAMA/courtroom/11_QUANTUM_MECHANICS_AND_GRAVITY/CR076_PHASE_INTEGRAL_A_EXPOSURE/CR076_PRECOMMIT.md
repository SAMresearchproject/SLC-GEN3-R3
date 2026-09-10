# CR076 Phase Integral / A Exposure - Precommit

```text
document_id:    CR076_PRECOMMIT
branch:         11_QUANTUM_MECHANICS_AND_GRAVITY
cr_slot:        CR076
seal_anchor:    SEALED_QUANTUM_MECHANICS_AND_GRAVITY_SCOPE_APPROACH_2026_06_13
                (sha256: f80c93f67da67a5c9286aafe845316ee6fa3a614439c4e9e120abb9c3a9207dc)
date_local:     2026-06-13
```

## Rule

Verify the phase integral / A exposure chain reproduces in SAM
substrate-count form:
- A exposure accumulates per substrate-time tick into A_route
- phase functional integrates A exposure to yield Delta_phi
- no engine-surface fit loop on observed A exposure / phase

## Question

Does QP001 (phase functional bridge) plus G406/G286-class substrate-
count tests reproduce the phase integral / A exposure chain?

## Premises

```text
P1. Sources: qp001 (already CR073), SAMs_TOE 05 README,
    G286-class free-particle action substrate-count test.
P2. Patterns:
      A exposure: "A_exposure" / "A exposure"
      A route accumulation: "A_route" / "A route"
      phase functional: "phase functional"
      integral form: "integral A" / "int A" / "phase integral"
P3. qp001 free_parameters_introduced = 0 (rolled forward from CR073).
P4. No engine-surface fit on A exposure.
P5. G286-class test present.
P6. Manifest seal intact.
```

## Outcome

```text
PASS_SCOPED_STRUCTURAL_PHASE_INTEGRAL: all patterns matched.
BOUNDARY: partial pattern coverage.
FAIL: engine fit or non-zero free params.
DIAGNOSTIC: seal mismatch.
```

## Rule-9

This test could have falsified the claim that SAM's A_exposure +
A_route + phase functional reproduces the phase integral form
Δφ = ∫A ds / ℏ in substrate-count language with zero free parameters.

## Expected Artifacts

CR076_PRECOMMIT.md, CR076_PHASE_INTEGRAL_A_EXPOSURE.py,
CR076_input_manifest.csv, CR076_a_exposure_check.json,
CR076_a_route_check.json, CR076_phase_functional_check.json,
CR076_integral_form_check.json, CR076_engine_surface_fit_scan.csv,
CR076_manifest_seal_check.json, CR076_wrong_controls.csv,
CR076_summary.json, CR076_result.md, HASHES.txt
