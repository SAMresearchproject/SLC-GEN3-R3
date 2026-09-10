# CR223d PR Real-Time Warning Contact Result

**Result class:** `CR223d_REALTIME_WARNING_VALIDATED_IN_SIMULATION`
**Checks:** 13/13

## Alarm performance (test, N=100 trials)

- TP / TN / FP / FN (per-sample) = 609 / 299 / 18 / 74
- TPR (per-sample) = 0.8917  (above-threshold samples caught)
- TNR (per-sample) = 0.9432  (below-threshold samples correctly silent)
- false-alarm rate = 0.0568  (target <= 0.1)
- miss rate        = 0.1083  (target <= 0.15)
- latency mean     = 0.70 intervals
- latency max      = 3 intervals  (target <= 3)

## Sensor calibration (frozen on train)

P(A_leak >= 1/24 | S(t)) = sigmoid((S - mu) / scale)
mu = 0.255371, scale = 0.003042
train label prevalence = 0.691

## Packet-integrity audit

| Audit | Expected | Observed | Passed |
|---|---|---|:---:|
| valid_packet_162_allows_emission | alarms fire on above-threshold samples | TP_samples=609, FN_samples=74 | True |
| corrupt_packet_161_blocks_emission | 0 fires across 30 trials | 0 fires | True |
| corrupt_packet_163_blocks_emission | 0 fires across 30 trials | 0 fires | True |
| G_protocol_0_blocks_emission | 0 fires across 30 trials | 0 fires | True |

## Verdict

```text
CR223d_REALTIME_WARNING_VALIDATED_IN_SIMULATION
```

A held-out sensor proxy emitted a real-time Paul Revere warning consistent
with tomography on a noise-augmented NV qutrit simulator. All five gate-
blocking wrong controls (corrupt checksum 161, corrupt checksum 163,
G_protocol=0, shuffled sensor stream, future-info leakage) confirm the
warning is gated correctly.

Simulator-validated, partner-lab confirmation pending.

## Next gate

CR223e - PR QC operational benefit (intervention vs budget-matched controls).
