# CR001 Foundation Selector Recertification

## Verdict

```text
CR001_BOUNDARY_STRUCTURAL_PACKET_RECERTIFIED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
```

## Source Hygiene

```text
uses_older_g_tests = false
older_test_reference_hits = 0
```

## Selected Packet

```text
exchange_count = 2
identity_support_dimension = 3
compact_phase_cycle = 6.283185307179586
floor = 0.026525823848649224
floor_inverse = 37.69911184307752
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_g_test_inputs_read | True |
| unique_exchange_selector | True |
| unique_identity_dimension_selector | True |
| unique_compact_phase_cycle_selector | True |
| floor_finite_positive | True |
| wrong_controls_do_not_match_full_packet | True |

## Wrong Controls

```text
wrong_controls_same_full_packet = False
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's foundation packet is selected by minimal exchange, stable identity support, and primitive compact phase composition rather than by inherited older result labels.
```

## Courtroom Reading

CR001 is a clean structural recertification. It does not by itself
supply downstream empirical evidence, so its scientific verdict is
BOUNDARY rather than empirical PASS. It can support the case summary's
internal structural PASS language as a recertified foundation packet.

## Artifacts

- `A0-a_h-D\CR001_foundation_selector_recertification\CR001_summary.json`
- `A0-a_h-D\CR001_foundation_selector_recertification\CR001_candidate_rows.csv`
- `A0-a_h-D\CR001_foundation_selector_recertification\CR001_wrong_controls.csv`
- `A0-a_h-D\CR001_foundation_selector_recertification\CR001_input_manifest.csv`
