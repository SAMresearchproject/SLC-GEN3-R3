# CR226 Vaulted SOB Card Generation, Freeze, Reveal

Result: **CR226_PASS_VAULTED_CONSTANTS_ONLY_SOB_CARD_GENERATION__PREDICTIONS_SEALED__126_NATIVE_CARDS_FROZEN__126_REVEAL_CARDS_GENERATED__CLOCK_MATCH_126_OF_126**

## Direct Answer

The vault run generated the 126 SOB card predictions from SAM constants only,
sealed them, froze the prediction hash root, then opened reveal sources and
generated 126 revealed cards.

## Prediction Formula

```text
R = 12
D = 3
alpha_H = 2
split = 8
capacity = 126
kappa_floor = 7117/768
clock_stable(Z) = Z <= 83 and Z not in {43,61}
frontier(Z) = Z > 118
```

Prediction counts:

```text
stable     = 81
radioactive = 37
frontier   = 8
```

## Seals

```text
prediction_merkle_root = e436cf01bacc542bad5403d605c0eea9c964c2c645d97574f378a360fa061897
prediction_file_count  = 255
reveal_merkle_root     = f02f2253378f291fec25d6b31807fa554bbb03934b19497197b08468087253a6
reveal_file_count      = 254
```

The reveal seal links back to the prediction root:

```text
e436cf01bacc542bad5403d605c0eea9c964c2c645d97574f378a360fa061897
```

## Cards

- Native prediction PNG cards: 126
- Native prediction SVG cards: 126
- Revealed PNG cards: 126
- Revealed SVG cards: 126

Gold reveal check:

```text
SOB79
Z=79, N=118, A=197
P=79p+118n+79e
quark=276u+315d+79e
clock=stable
reveal=Au Gold
matter=Matter 196.967
```

## Security Boundary

Prediction artifacts were written, hashed, zipped, and frozen before reveal
sources were read. Downstream names, symbols, measured isotope masses, and
HH001/CLOCK labels are reveal/comparator fields only.

## Artifacts

- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/vault/01_prediction_seal/CR226_predictions_constants_only_126.csv`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/vault/01_prediction_seal/CR226_prediction_seal.json`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/vault/02_freeze/CR226_FREEZE_LEDGER.json`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/vault/03_reveal/CR226_reveal_comparison_126.csv`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/vault/03_reveal/CR226_reveal_seal.json`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/vault/01_prediction_seal/cards_native_png/SOB079_native.png`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/vault/03_reveal/cards_revealed_png/SOB079_revealed_Gold.png`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/CR226_checks.csv`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/CR226_summary.json`
- `09a_PARTICLE_MASS_CHAIN/CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL/HASHES.txt`
