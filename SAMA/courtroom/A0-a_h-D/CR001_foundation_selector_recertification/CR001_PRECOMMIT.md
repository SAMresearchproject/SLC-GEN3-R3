# CR001 Foundation Selector Recertification - Precommit

## Rule

```text
Do not read older G-test outputs.
Do not import older G-test result files as computation inputs.
Use only declared selector premises and current Courtroom standard.
```

## Question

```text
Can the foundation selector recover one minimal exchange count, one stable
identity-support dimension, and one compact-cycle floor from declared premises
without using older test outputs?
```

## Declared Selector Premises

```text
P1. A resolved exchange surface must support a nontrivial fixed-point-free
    exchange/involution.
P2. The selected exchange count is the minimal count satisfying P1.
P3. Persistent identity requires a closed response carrier with twist/link
    stability.
P4. Closed-loop identity must have enough ambient freedom for over/under twist,
    but not enough extra freedom to untie the carrier.
P5. The compact phase cycle is the primitive positive unitary phase return.
P6. The floor is the inverse product of the primitive phase cycle, selected
    exchange count, and selected identity-support dimension.
```

## Outcome Taxonomy

```text
PASS:
  Each selector returns exactly one value, wrong controls do not return the same
  full packet, and the composed floor is finite and positive.

BOUNDARY:
  The selectors return a unique packet, but the result remains structural rather
  than empirical because no downstream external measurement is tested.

FAIL:
  Any primary selector returns no value, more than one value, or a wrong control
  returns the same full packet.

DIAGNOSTIC:
  The run reads older G-test outputs, the source hygiene scan fails, or the
  computation cannot produce a complete packet.
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's foundation packet is
selected by minimal exchange, stable identity support, and primitive compact
phase composition rather than by inherited older result labels.
```

## Expected Artifacts

```text
CR001_result.md
CR001_summary.json
CR001_candidate_rows.csv
CR001_wrong_controls.csv
CR001_input_manifest.csv
```
