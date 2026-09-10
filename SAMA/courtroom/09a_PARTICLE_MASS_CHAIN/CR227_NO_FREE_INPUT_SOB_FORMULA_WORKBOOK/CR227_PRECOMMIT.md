# CR227 Precommit - No-Free-Input SOB Formula Workbook

## Task

Create a workbook that carries the constants-only SOB formula surface for all
126 rows with no free input cells, no card lookups, and no reveal labels.

## Construction Contract

The workbook must generate rows from declared SAM constants only:

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8
capacity = R^2 * (1 - 2^-D) = 126
kappa_floor = 7117/768
neutron_G_unit = 1/64
hidden_set = {alpha_H^a * D^b <= R}
clock_boundary = D^(D+1) + alpha_H = 83
clock_holes = {hidden_sum-alpha_H, hidden_sum-alpha_H+R^2/split} = {43,61}
clock_stable(Z) = Z <= 83 and Z not in {43,61}
frontier(Z) = Z > 118
```

No known element names, symbols, measured masses, public cards, or CLOCK labels
may be used to construct workbook rows.

## Expected Workbook Sheets

- `Constants`
- `Hidden_Set`
- `SOB_126`
- `Card_Payloads_126`
- `Formula_Map`
- `Checks`

## Expected Outputs

- `CR227_no_free_input_sob_formula_workbook.xlsx`
- `CR227_formula_map.csv`
- `CR227_input_manifest.csv`
- `CR227_checks.csv`
- `CR227_summary.json`
- `CR227_result.md`
- `HASHES.txt`

