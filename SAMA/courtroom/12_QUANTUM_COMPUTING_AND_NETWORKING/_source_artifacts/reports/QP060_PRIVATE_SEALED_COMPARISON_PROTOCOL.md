# QP060 - Private Sealed Comparison Protocol

## Result

```text
QP060_SEALED_COMPARISON_PROTOCOL_BUILT
```

## Vault Door

QP060 freezes the private Phase 5 isotope prediction bundle before observed
isotope, mass, decay, half-life, or abundance data enters the workflow.

```text
prediction_manifest_rows = 200
source_hash_rows = 8
protocol_output_hash_rows = 8
external_data_used = false
observed_isotope_masses_used = false
observed_decay_modes_used = false
observed_half_lives_used = false
free_parameters_introduced = 0
prediction_manifest_sha256 = 19781d97b1008b3b1a1d030c64f37ab8ad7e55b7127cc75b72a0ab2792f697c3
hash_manifest_sha256 = 4461edd2fea795fa84ea20c1c230005f8eaae968ed11640196850f29bc28a273
next_frontier = QP061_PRIVATE_APPROVED_SEALED_ISOTOPE_COMPARISON_REQUIRES_EXTERNAL_DATA_PREFLIGHT
```

## Sealed Inputs

| gate | artifact | sha256 prefix | path |
| --- | --- | --- | --- |
| QP052 | numeric_deltaN_binding_mass | `4b39e18f8b4f350c...` | `phase4_tables/phase5_numeric_deltaN_binding_mass_v1.csv` |
| QP054 | isotope_neighbor_ladder | `926fd481584bc5a9...` | `phase4_tables/phase5_isotope_neighbor_ladder_v1.csv` |
| QP056 | residual_stability_decay_pressure | `ba0af64bde97d848...` | `phase4_tables/phase5_residual_stability_decay_pressure_v1.csv` |
| QP057 | decay_direction_chain | `ca76bf78f235aeb8...` | `phase4_tables/phase5_decay_direction_chain_v1.csv` |
| QP059 | visual_anchor_digest | `22d6c4738033f1a4...` | `phase4_tables/phase5_visual_anchor_digest.csv` |
| QP055 | phase5_isotope_freeze_summary | `63dd48e2d4d237a6...` | `artifacts/qp055/qp055_summary.json` |
| QP058 | phase5_pressure_extension_freeze_summary | `3a1456b7e2adcf35...` | `artifacts/qp058/qp058_summary.json` |
| QP059 | phase5_visual_package_summary | `5348e929e63a88c7...` | `artifacts/qp059/qp059_summary.json` |

## Protocol Outputs

| artifact | sha256 prefix | path |
| --- | --- | --- |
| prediction_manifest | `19781d97b1008b3b...` | `artifacts/qp060/qp060_prediction_manifest.csv` |
| phase4_prediction_manifest_copy | `19781d97b1008b3b...` | `phase4_tables/phase5_sealed_prediction_manifest.csv` |
| comparison_schema | `5334a9de9616eb47...` | `artifacts/qp060/qp060_comparison_schema.csv` |
| scoring_lanes | `e59caed7fc9a59f3...` | `artifacts/qp060/qp060_scoring_lanes.csv` |
| external_data_manifest_template | `4123c53a4daf48cb...` | `artifacts/qp060/qp060_external_data_manifest_template.csv` |
| allowed_questions | `eb8f9e5aacd33f49...` | `artifacts/qp060/qp060_allowed_questions.csv` |
| next_frontier | `f80ec37c0c5bf5de...` | `artifacts/qp060/qp060_next_frontier.csv` |
| preflight | `fb2bfaa14198e3c2...` | `artifacts/qp060/qp060_preflight.md` |

## Comparison Rules

```text
1. QP061 may import external data only after a new explicit preflight.
2. QP061 may not modify QP060 prediction rows, candidate A values, or labels.
3. The first comparison lane is isotope roster presence by symbol and A.
4. Mass residuals are conditional until nuclear/atomic/mass-excess convention is declared.
5. Decay, half-life, and abundance channels are optional approved lanes, not hidden inputs.
6. No parameter refit is allowed after external data enters.
```

## Interpretation

The vault door is now built. The next move is not another internal selector.
The next move is an approved sealed comparison against external isotope data,
using this frozen manifest and hash record as the guardrail.
