# QP061 - Private Approved Sealed Isotope Comparison

## Result

```text
QP061_SEALED_ISOTOPE_COMPARISON_COMPLETED
```

## External Source

```text
source = IAEA LiveChart of Nuclides ground_states all
url = https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=all
sha256 = 8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
retrieved_utc = 2026-06-08T22:49:23.035093+00:00
normalized_rows = 3383
```

## Sealed Guard

```text
sealed_hash_guard_pass = true
prediction_manifest_mutated = false
free_parameters_introduced = 0
sealed_prediction_hash_actual = 19781d97b1008b3b1a1d030c64f37ab8ad7e55b7127cc75b72a0ab2792f697c3
```

## Roster Match

```text
sealed_prediction_rows = 200
exact_ZNA_matches = 162
exact_ZNA_match_rate = 0.810000
symbol_A_matches = 162
symbol_A_match_rate = 0.810000
primary_rows = 118
primary_exact_matches = 96
primary_exact_match_rate = 0.813559
neighbor_rows = 82
neighbor_exact_matches = 66
neighbor_exact_match_rate = 0.804878
elements_with_any_exact_match = 96
element_exact_coverage_rate = 0.813559
```

## Banded Readout

```text
Z_001_096_rows = 162
Z_001_096_exact_matches = 162
Z_001_096_exact_match_rate = 1.000000
Z_097_118_rows = 38
Z_097_118_exact_matches = 0
Z_097_118_exact_match_rate = 0.000000
```

## Pressure And Decay Readout

```text
pressure_alignment_counts = {'MATCH': 95, 'MISMATCH': 67, 'NO_OBSERVED_ROW': 38}
decay_alignment_counts = {'MATCH': 47, 'MISMATCH': 115, 'NO_OBSERVED_ROW': 38}
```

## Interpretation

QP061 opens the vault against IAEA LiveChart ground-state data. The sealed
prediction manifest remains unchanged. The first scoring lane is exact Z/N/A
roster presence; pressure, decay, and mass residual readouts are recorded as
declared comparison lanes, not as refits.

The result is now empirical contact. Hits and misses both stay downstream of
the frozen QP060 manifest.
