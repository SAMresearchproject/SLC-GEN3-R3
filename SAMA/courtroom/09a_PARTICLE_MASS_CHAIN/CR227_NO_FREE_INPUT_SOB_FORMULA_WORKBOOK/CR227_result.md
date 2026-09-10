# CR227 No-Free-Input SOB Formula Workbook

Result: **CR227_PASS_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK__126_ROWS__CLOCK_FORMULA_INCLUDED__FORMULA_CELLS_GT_5000__NO_REVEAL_INPUTS**

## Direct Answer

Created the no-free-input workbook:

`09a_PARTICLE_MASS_CHAIN/CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK/CR227_no_free_input_sob_formula_workbook.xlsx`

The workbook has formula-driven sheets for all 126 SOB rows and card payloads.
It includes the CR225 clock formula:

```text
stable iff Z <= 83 and Z not in {43,61}
frontier iff Z > 118
```

## Workbook

- sheets: 7
- formula cells: 5529
- SOB rows: 126
- card payload rows: 126
- prediction counts: {'stable': 81, 'radioactive': 37, 'frontier': 8}

Z79 readout:

```text
N=118
A=197
P=79p+118n+79e
quark=276u+315d+79e
G=732.696614583333333
GR=5861.572916666666667
clock=stable
```

## Boundary

No known names, symbols, measured masses, public cards, or reveal labels are
construction inputs. Reveal fields on `Card_Payloads_126` are blank.

## Artifacts

- `09a_PARTICLE_MASS_CHAIN/CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK/CR227_no_free_input_sob_formula_workbook.xlsx`
- `09a_PARTICLE_MASS_CHAIN/CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK/CR227_formula_map.csv`
- `09a_PARTICLE_MASS_CHAIN/CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK/CR227_input_manifest.csv`
- `09a_PARTICLE_MASS_CHAIN/CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK/CR227_checks.csv`
- `09a_PARTICLE_MASS_CHAIN/CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK/CR227_summary.json`
- `09a_PARTICLE_MASS_CHAIN/CR227_NO_FREE_INPUT_SOB_FORMULA_WORKBOOK/HASHES.txt`
