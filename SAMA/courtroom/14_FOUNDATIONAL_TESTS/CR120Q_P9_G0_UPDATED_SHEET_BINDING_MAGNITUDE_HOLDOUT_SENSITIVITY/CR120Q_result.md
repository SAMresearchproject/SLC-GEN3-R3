# CR120Q Result

## Verdict

`PASS_NO_MEASURED_BINDING_MAGNITUDE_IMPROVEMENT`

## Direct answer

No. The new whole-sheet sums were run, but neither specifically p9,g0-corrected sum materially lowered untouched holdout binding residual magnitudes under the direct predeclared surfaces.

## Holdout readout (MeV)

| surface | scenario | RMS | MAE | delta RMS vs M=126 | delta MAE vs M=126 | direction | material |
|---|---|---:|---:|---:|---:|---|---|
| `FROZEN_COEFFICIENT_TRANSFER` | `BASELINE_REGISTERED_M126` | 3.358328783 | 2.698229204 | 0.000000000 | 0.000000000 | `BASELINE` | `false` |
| `FROZEN_COEFFICIENT_TRANSFER` | `SHEET81_AS_SAVED_12600` | 756.306993997 | 721.671077268 | -752.948665214 | -718.972848064 | `WORSE` | `false` |
| `FROZEN_COEFFICIENT_TRANSFER` | `SHEET81_P9G0_REMOVED_12550P5` | 756.276833856 | 721.642296810 | -752.918505074 | -718.944067606 | `WORSE` | `false` |
| `FROZEN_COEFFICIENT_TRANSFER` | `SHEET100_P9G0_REMOVED_16200` | 758.006319929 | 723.292667103 | -754.647991147 | -720.594437899 | `WORSE` | `false` |
| `TRAIN_ONLY_REFIT` | `BASELINE_REGISTERED_M126` | 3.358328783 | 2.698229204 | 0.000000000 | 0.000000000 | `BASELINE` | `false` |
| `TRAIN_ONLY_REFIT` | `SHEET81_AS_SAVED_12600` | 3.358328783 | 2.698229204 | 0.000000000 | 0.000000000 | `UNCHANGED` | `false` |
| `TRAIN_ONLY_REFIT` | `SHEET81_P9G0_REMOVED_12550P5` | 3.358328783 | 2.698229204 | 0.000000000 | 0.000000000 | `UNCHANGED` | `false` |
| `TRAIN_ONLY_REFIT` | `SHEET100_P9G0_REMOVED_16200` | 3.358328783 | 2.698229204 | 0.000000000 | 0.000000000 | `UNCHANGED` | `false` |
| `FIXED_ZERO_FREE_SURFACE` | `BASELINE_REGISTERED_M126` | 59.602456485 | 56.753723515 | 0.000000000 | 0.000000000 | `BASELINE` | `false` |
| `FIXED_ZERO_FREE_SURFACE` | `SHEET81_AS_SAVED_12600` | 165.710329947 | 161.868595427 | -106.107873462 | -105.114871912 | `WORSE` | `false` |
| `FIXED_ZERO_FREE_SURFACE` | `SHEET81_P9G0_REMOVED_12550P5` | 165.705862834 | 161.864287889 | -106.103406349 | -105.110564375 | `WORSE` | `false` |
| `FIXED_ZERO_FREE_SURFACE` | `SHEET100_P9G0_REMOVED_16200` | 165.962032933 | 162.111296876 | -106.359576448 | -105.357573361 | `WORSE` | `false` |

## Source and split checks

- Live 100-row sum reconstructed exactly: `16200`.
- Live 81-row as-saved sum reconstructed exactly: `12600`.
- Specific remaining p9,g0 removal from the 81-row sheet: `12600 - 49.5 = 12550.5`.
- All arithmetic used whole-roster sums; no mean was used.
- Frozen split: `49` training rows and `20` untouched holdout rows; holdout fit rows: `0`.
- CR242 baseline reproduction: `PASS`.

## Interpretation

Surface A answers direct substitution with the original CR242 coefficients held fixed. Surface B answers whether training-only coefficient refitting extracts any new predictive shape. Surface C challenges the fixed zero-free magnitude formula. The global sums were also tested as additive features and rejected because each is an exact scalar multiple of the intercept.

This result measures numerical holdout response only. It does not install the sums as a new registered M value or create the still-missing isotope-to-QP093A occupancy map.
