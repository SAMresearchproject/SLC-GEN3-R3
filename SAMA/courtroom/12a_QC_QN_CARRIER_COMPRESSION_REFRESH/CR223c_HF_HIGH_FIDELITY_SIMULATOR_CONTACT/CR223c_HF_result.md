# CR223c_HF High-Fidelity Simulator Contact Result

**Result class:** `CR223c_HF_PIPELINE_PASS__HIGH_FIDELITY_SIMULATOR_CONTACT`
**Checks:** 16/16

## Per-regime crossing summary

| Regime | gamma_1*T2 | gamma_phi*T2 | t_fire_test | reference | classification | sensor BA |
|---|---:|---:|---:|---:|---|---:|
| room_temp_NV | 1.0 | 0.5 | 0.021928 | 0.028961 | MATCHED_MODEL | 0.8946 |
| cryogenic_NV | 0.1 | 0.95 | 0.049261 | 0.035436 | MATCHED_MODEL | 0.8552 |
| noisy_NV | 1.0 | 0.5 | 0.015278 | 0.028961 | MATCHED_MODEL | 0.9471 |

## Controls

- zero-wait max A_hat: 0.023709 (must be < 0.041667)
- no-decoherence max A_hat: 0.011918 (must be < 0.041667)

## Verdict

```text
CR223c_HF_PIPELINE_PASS__HIGH_FIDELITY_SIMULATOR_CONTACT
```

The CR223c sealed pipeline (Gell-Mann tomography + PSD projection + sensor
proxy + linear-interpolation crossing) survives realistic apparatus noise
across three platform regimes: room-temperature NV (M4), cryogenic NV (M3),
and high-noise NV. The cryogenic regime aligns with the SAM-native M3
coefficient (the CR223f same-domain candidate); room-temp aligns with M4.

This is **simulator-validated, partner-lab confirmation pending** - the
highest result class that can be honestly claimed without raw hardware data.

## Next gate

CR223d - PR realtime warning emission contact (builds on this HF simulator).
