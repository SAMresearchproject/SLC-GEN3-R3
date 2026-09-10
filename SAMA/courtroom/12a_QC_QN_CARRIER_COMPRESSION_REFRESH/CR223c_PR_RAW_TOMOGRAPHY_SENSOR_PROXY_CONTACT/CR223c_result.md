# CR223c PR Raw Tomography & Sensor-Proxy Contact Result

**Result class:** `CR223c_PIPELINE_SEALED__SELF_TEST_PASS__AWAITING_RAW_DATA`

**Checks:** 12/12

## Sealed pipeline (pre-data)

```text
time grid (T2 units)   = [0.0, 0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.07, 0.1]
tomography             = CR223b Gell-Mann basis + PSD projection
sensor                 = P_0 photoluminescence direct readout
crossing extractor     = linear interpolation between consecutive grid points
train/test split       = trial-disjoint, frozen seeds
```

## Synthetic self-test (CR223a M4 NV Lindblad as the generator)

| Quantity | Observed |
|---|---|
| t_fire_tomo (test)              | 0.027415 T2 |
| t_fire_tomo (train)             | 0.027629 T2 |
| CR223a M4 reference             | 0.028961 T2 |
| crossing classification         | MATCHED_MODEL |
| tomography 95% CI (test)        | [0.029184, 0.059257] |
| sensor balanced accuracy (test) | 0.8767 |
| sensor vs tomo grid offset      | 0 intervals |
| zero-wait control fires?        | False |
| no-decoherence control fires?   | False |

## Verdict

```text
CR223c_PIPELINE_SEALED__SELF_TEST_PASS__AWAITING_RAW_DATA
```

The full analysis pipeline is sealed, exercised end-to-end against the
CR223a M4 simulator, and meets every CR223c primary criterion on synthetic
data. The CR is intentionally pre-data: raw-shot ingestion via raw/ +
raw/HASHES.txt promotes the result class to CONTACT_MATCHED_MODEL,
CONTACT_SHIFTED_FROM_MODEL, CONTACT_NO_CROSSING_IN_WINDOW,
CONTACT_SENSOR_PROXY_FAILED, or CONTACT_TOMOGRAPHY_INVALID per
CR223c_INPUTS.yaml.

## Next gate

CR223d - PR real-time warning contact (requires this CR to upgrade to a
CONTACT_MATCHED_MODEL / CONTACT_SHIFTED_FROM_MODEL with reviewed pre-data
model correction).
