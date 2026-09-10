# QC005 - Material / Isotope Support Filter

## Result

```text
QC005_MATERIAL_ISOTOPE_SUPPORT_FILTER_SELECTED
```

## Main Readout

```text
support_filters = 6
selected_filters = 5
excluded_filters = 1
check_passes = 8/8
wrong_control_passes = 5/5
free_parameters_introduced = 0
```

## Support Filters

| filter_id | filter_name | support_role | native_readout | qc_use | status |
| --- | --- | --- | --- | --- | --- |
| QC005-FILTER-01 | low_A_contact_stable_isotope_band | stable material platform band | exact_match_rate=1.0; matched_primary=96 | apparatus support and shielding candidate band | SELECTED |
| QC005-FILTER-02 | controlled_charged_response_templates | charged-envelope response model | charged resonance families supply response templates, not carrier identity | model charged envelope response without promoting it to carrier | SELECTED |
| QC005-FILTER-03 | stable_many_SW_composite_platform | many-SW composite support | first_reorganization_ratio=0.08333333333333333 | prefer coherent shared-closure support over open-tail material lanes | SELECTED |
| QC005-FILTER-04 | quantum_spaghettification_avoidance_band | avoid extended A-road shear failure | full_contact_failure_ratio=1.0 | prevent support geometry from forcing carrier/envelope desync | SELECTED |
| QC005-FILTER-05 | superheavy_open_tail_exclusion | exclude unresolved heavy-tail support lane | exact_match_rate=0.0; no_observed_rows=38 | do not use open-tail rows as baseline coherence support | EXCLUDED_FOR_PHASE1_QC_SUPPORT |
| QC005-FILTER-06 | paul_revere_protocol_compatibility | material must preserve letter-safe readout | support cannot open final-answer channel before selected write | material support must not defeat QC004 readout firewall | SELECTED |

## Lane Scorecard

| lane | supports_carrier | supports_envelope | supports_sensor | phase1_qc_decision |
| --- | --- | --- | --- | --- |
| low_A_contact_stable_isotope_band | True | False | False | USE_AS_SUPPORT_FILTER |
| controlled_charged_response_templates | False | True | False | USE_AS_SUPPORT_FILTER |
| stable_many_SW_composite_platform | True | False | True | USE_AS_SUPPORT_FILTER |
| quantum_spaghettification_avoidance_band | False | False | True | USE_AS_SUPPORT_FILTER |
| superheavy_open_tail_exclusion | False | False | False | DO_NOT_USE_AS_BASELINE |
| paul_revere_protocol_compatibility | True | True | True | USE_AS_SUPPORT_FILTER |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QC005_CHECK_01 | QC004 dependency is selected | True | QC004_PAUL_REVERE_READOUT_PROTOCOL_SELECTED |
| QC005_CHECK_02 | QP061 sealed prediction manifest was not mutated | True | False |
| QC005_CHECK_03 | phase5 Z<=96 exact match band is complete | True | 1.0 |
| QC005_CHECK_04 | superheavy open tail is excluded from baseline support | True | 1 |
| QC005_CHECK_05 | support filters cover material/envelope/sensor/firewall roles | True | 5 |
| QC005_CHECK_06 | lane scorecard includes carrier, envelope, and sensor supports | True | 6 |
| QC005_CHECK_07 | application rules are all selected | True | 5 |
| QC005_CHECK_08 | no external quantum hardware data introduced | True | repo sealed isotope data only |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QC005_WC_01 | superheavy open tail accepted as baseline support | False | False | True |
| QC005_WC_02 | charged response template promoted to protected carrier | False | False | True |
| QC005_WC_03 | support filter omits QC004 firewall compatibility | False | False | True |
| QC005_WC_04 | material support lane omits many-SW composite support | False | False | True |
| QC005_WC_05 | unsupported filter status appears | False | False | True |

## Next Frontier

```text
QC_CAMPAIGN_PHASE1_COMPLETE_READY_FOR_REVIEW
```
