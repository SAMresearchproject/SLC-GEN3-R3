# CR228 Precommit - Reveal-Layer SOB Formula Workbook

## Task

Create the companion workbook to CR227: keep the 126 SOB rows formula-derived
from SAM constants, then populate post-seal reveal fields for symbols, names,
isotope anchors, CLOCK comparator labels, and measured isotope mass where the
reveal source has it.

## Boundary

CR227 remains the no-free-input prediction workbook. CR228 is a reveal-layer
workbook:

- prediction rows are still formulas from constants,
- reveal source rows are post-seal values,
- revealed card rows use lookup formulas to join prediction fields to reveal
  fields,
- reveal fields are not construction inputs for the native SOB rows.

## Reveal Sources

- `CR119_courtroom_periodic_table.csv`: downstream symbol/name labels.
- `CR220_simulated_element_primary_rows_126.csv`: HH001/CLOCK comparator labels.
- `C:\VS\quantum_phase\artifacts\qp061\qp061_observed_roster_normalized.csv`:
  isotope atomic mass reveal when available.
- `CR227_no_free_input_sob_formula_workbook.xlsx`: prediction workbook hash
  reference only.

## Expected Outputs

- `CR228_reveal_layer_sob_formula_workbook.xlsx`
- `CR228_formula_map.csv`
- `CR228_input_manifest.csv`
- `CR228_checks.csv`
- `CR228_summary.json`
- `CR228_result.md`
- `HASHES.txt`

