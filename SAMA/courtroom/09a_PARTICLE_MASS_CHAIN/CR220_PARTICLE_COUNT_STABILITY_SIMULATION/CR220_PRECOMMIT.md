# CR220 Precommit - Particle Count Stability Simulation

## Task

Run a particle-count simulation centered on:

```text
P -> G(P) -> GR(P)
```

and test what can be produced toward stable element rows.

## Source Boundary

- CR119 periodic rows are the locked 126-row native element-family surface.
- CR119 matter rows provide the SAM-native proton, neutron, and electron
  component selectors used by QP094A.
- QP094A source rules provide the native capacity, shell capacity, radix
  coordinates, isotope ladder, and `qA`/tensor split formula.
- CR219/roworderv1 and CR218 provide the row-order/bigrade address skeleton
  `{1,2,3,4,6,8,9,12}`.
- CR211/HH001 CLOCK is a reference comparator only. It is not a construction
  input for any native selector.

## Planned Outputs

- `CR220_component_selector.csv`
- `CR220_simulated_element_primary_rows_126.csv`
- `CR220_simulated_isotope_ladder_rows_214.csv`
- `CR220_selector_scores.csv`
- `CR220_threshold_search.csv`
- `CR220_particle_count_threshold_candidates_83.csv`
- `CR220_input_manifest.csv`
- `CR220_checks.csv`
- `CR220_summary.json`
- `CR220_result.md`
- `HASHES.txt`

## Pass Conditions

- 126 primary element-family rows are emitted from native capacity.
- 214 isotope-ladder rows are emitted from the QP094A ladder rule.
- Computed `GR(P)` matches CR119 `qA_total_primary` for all 126 rows.
- Computed `G(P)` matches CR119 `tensor_carrier_support_primary` for all 126
  rows.
- Computed `7G(P)` matches CR119 `retained_write_support_primary` for all 126
  rows.
- HH001 CLOCK labels are used only for scoring selectors, never for native row
  construction.
- Any selector that requires downstream reference holes is marked as
  reference-patched, not SAM-native.

