# CR226 Precommit - Vaulted SOB Card Generation, Freeze, Reveal

## Task

Run the constants-only SOB card engine as securely as possible:

1. generate the 126 native card predictions with no card/reveal inputs,
2. seal prediction rows and native card images with hashes,
3. freeze the prediction vault,
4. only then read downstream reveal/comparator sources,
5. generate revealed cards and comparison ledgers,
6. hash the whole vault chain.

## Construction Inputs

The prediction layer is constructed from declared SAM constants only:

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8
capacity = R^2 * (1 - 2^-D) = 126
shell_n_path = [1, alpha_H, D, R/D, R/D, D, alpha_H, alpha_H]
kappa_floor = 7117/768
neutron_G_unit = 1/64
clock_stable(Z) = Z <= 83 and Z not in {43,61}
frontier(Z) = Z > capacity - split = 118
```

No known element names, symbols, measured masses, public cards, or CLOCK labels
may be read before the prediction seal is written and hashed.

## Reveal-Only Sources

After the prediction freeze, these sources may be opened:

- `CR119_courtroom_periodic_table.csv` for downstream symbol/name labels.
- `CR220_simulated_element_primary_rows_126.csv` for HH001/CLOCK comparator.
- `C:\VS\quantum_phase\artifacts\qp061\qp061_observed_roster_normalized.csv`
  for downstream isotope atomic-mass reveal when available.

Reveal sources are not construction inputs.

## Expected Outputs

- `vault/01_prediction_seal/CR226_predictions_constants_only_126.csv`
- `vault/01_prediction_seal/CR226_prediction_card_payloads.jsonl`
- `vault/01_prediction_seal/cards_native_png/*.png`
- `vault/01_prediction_seal/cards_native_svg/*.svg`
- `vault/01_prediction_seal/CR226_prediction_hash_manifest.csv`
- `vault/01_prediction_seal/CR226_prediction_seal.json`
- `vault/02_freeze/CR226_FREEZE_LEDGER.json`
- `vault/03_reveal/CR226_reveal_comparison_126.csv`
- `vault/03_reveal/cards_revealed_png/*.png`
- `vault/03_reveal/cards_revealed_svg/*.svg`
- `vault/03_reveal/CR226_reveal_hash_manifest.csv`
- `vault/03_reveal/CR226_reveal_seal.json`
- `CR226_checks.csv`
- `CR226_summary.json`
- `CR226_result.md`
- `HASHES.txt`

