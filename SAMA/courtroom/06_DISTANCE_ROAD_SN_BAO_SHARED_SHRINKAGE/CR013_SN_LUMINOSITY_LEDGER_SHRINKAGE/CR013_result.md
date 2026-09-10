# CR013 SN Luminosity Ledger Shrinkage

## Verdict

```text
CR013_PASS_SN_LUMINOSITY_LEDGER_SHRINKAGE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SN_LUMINOSITY_LEDGER
```

## Row Identity Packet

```text
rows = 1701
max_A_error = 0.000e+00
max_distance_error_mpc = 0.000e+00
low_z_mean_A = 0.006234707158
high_z_mean_A = 0.292724398411
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_verdicts_used | true |
| free_parameters_introduced_zero | true |
| sn_source_rows_present | true |
| bao_inputs_not_loaded | true |
| A_los_row_identity | true |
| c_eff_row_identity | true |
| native_distance_row_identity | true |
| native_mu_row_identity | true |
| low_z_shrink_near_zero | true |
| high_z_shrink_larger_than_low_z | true |
| wrong_controls_do_not_match_packet | true |

## Rule-9 Line

```text
This test could have falsified the SN ledger claim if Pantheon SN rows did not recompute from A_los(z), if the luminosity-distance shrink failed row identity, if BAO inputs were needed, or if wrong controls matched the packet.
```
