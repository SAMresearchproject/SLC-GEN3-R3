# CR207a External Chain Replay Stability

## Verdict

```text
CR207a_PASS_EXTERNAL_CHAIN_REPLAY_STABILITY
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = EXTERNAL_CHAIN_REPLAY_STABILITY_APPEAL
```

## Question

Can the full simulator chain reach an external-facing readout while preserving frozen lane rules and boundary labels?

## Pass Conditions

| condition | pass |
|---|---:|
| original_cr204_and_cr207_remain_boundary | true |
| all_chain_case_conditions_true | true |
| no_free_parameters_any_chain_case | true |
| external_facing_endpoint_passes | true |
| wrong_controls_and_expected_breaks_preserved | true |
| source_artifact_hashes_present | true |
| chain_fingerprint_emitted | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| chain_cases | CR201,CR202,CR203,CR204,CR204a,CR205,CR207,CR208 | frozen summaries loaded |
| original_CR204_verdict | BOUNDARY | not relabeled |
| original_CR207_verdict | BOUNDARY | not relabeled |
| external_endpoint | CR204a_PASS_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION | external-facing Higgs/ZZ* endpoint |
| source_artifact_hash_count | 27 | hashes carried through chain summaries |
| chain_fingerprint_sha256 | f72e4a1fe7e300b920e62f32aeb7c25ba94a6acac77ceca69db959e0970336d8 | result classes plus source hashes |

## Rule-9 Line

```text
This test could have falsified the claim that the scale-bridge simulator can replay from source grammar to an external-facing resolved-parent readout while preserving all frozen lane rules and boundary labels.
```

## Notes

- CR207 is not relabeled; this is a separate promotion appeal artifact.
- The chain endpoint is CR204a, which carries the external Higgs/ZZ* parent-daughter contact.
- The chain fingerprint binds result classes and imported source hashes.
