# QP041 - Private Meson Scaffold Fill Pass

## Preflight

```text
test_id = QP041
test_name = PRIVATE_MESON_SCAFFOLD_FILL_PASS
test_type = FORWARD_MODEL_BUILD
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
if_audit_or_retest_reason = NOT_APPLICABLE
permission_required_before_run = false
public_repo_write = false
external_data_used = false
free_parameters_introduced = 0
```

## Result

```text
QP041_MESON_SCAFFOLD_FIRST_FILL_SELECTED
```

QP041 fills the meson scaffolds that have a selected native support family and
the QP040 binding-residue operator.

## Filled Meson Rows

| scaffold | family | symbol | SAM mass / MeV | status |
| --- | --- | --- | ---: | --- |
| d_anti_s | neutral_kaon_family | K0 / anti-K0 | 4.973398437309e+02 | FILLED_NATIVE_MESON_READOUT |
| d_anti_u | charged_pion_family | pi+ / pi- | 1.395228151684e+02 | FILLED_NATIVE_MESON_READOUT |
| s_anti_d | neutral_kaon_family | K0 / anti-K0 | 4.973398437309e+02 | FILLED_NATIVE_MESON_READOUT |
| s_anti_u | charged_kaon_family | K+ / K- | 4.937626918577e+02 | FILLED_NATIVE_MESON_READOUT |
| u_anti_d | charged_pion_family | pi+ / pi- | 1.395228151684e+02 | FILLED_NATIVE_MESON_READOUT |
| u_anti_s | charged_kaon_family | K+ / K- | 4.937626918577e+02 | FILLED_NATIVE_MESON_READOUT |
| u_anti_u | neutral_pion_family | pi0 | 1.350279200578e+02 | FILLED_NATIVE_MESON_READOUT |

## Family Map

| family | symbol | filled scaffolds | operator class |
| --- | --- | --- | --- |
| charged_pion_family | pi+ / pi- | u_anti_d;d_anti_u | Q_ANTI_Q_POSITIVE_Q_RETURN_SUPPRESSION |
| neutral_pion_family | pi0 | u_anti_u | Q_ANTI_Q_NEGATIVE_Q_RETURN_AMPLIFICATION |
| charged_kaon_family | K+ / K- | u_anti_s;s_anti_u | Q_ANTI_Q_NEUTRAL_Q_RETURN |
| neutral_kaon_family | K0 / anti-K0 | d_anti_s;s_anti_d | Q_ANTI_Q_NEGATIVE_Q_RETURN_AMPLIFICATION |

## Open Boundaries

| scaffold | charge | boundary class | selector needed |
| --- | ---: | --- | --- |
| b_anti_b | 0 | BOUNDARY_NEUTRAL_SELF_CHANNEL_SELECTOR_NEEDED | NEUTRAL_SELF_CHANNEL_ROLE_SCALE_SELECTOR |
| b_anti_c | -1 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| b_anti_d | 0 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| b_anti_s | 0 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| b_anti_t | -1 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| b_anti_u | -1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| c_anti_b | 1 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| c_anti_c | 0 | BOUNDARY_NEUTRAL_SELF_CHANNEL_SELECTOR_NEEDED | NEUTRAL_SELF_CHANNEL_ROLE_SCALE_SELECTOR |
| c_anti_d | 1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| c_anti_s | 1 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| c_anti_t | 0 | CANDIDATE_RETURN_CHANNEL_BINDING_SELECTOR_NEEDED | QP041C_RETURN_CHANNEL_BINDING_SCALE_SELECTOR |
| c_anti_u | 0 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| d_anti_b | 0 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| d_anti_c | -1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| d_anti_d | 0 | BOUNDARY_NEUTRAL_SELF_CHANNEL_SELECTOR_NEEDED | NEUTRAL_SELF_CHANNEL_ROLE_SCALE_SELECTOR |
| d_anti_t | -1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| s_anti_b | 0 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| s_anti_c | -1 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| s_anti_s | 0 | BOUNDARY_NEUTRAL_SELF_CHANNEL_SELECTOR_NEEDED | NEUTRAL_SELF_CHANNEL_ROLE_SCALE_SELECTOR |
| s_anti_t | -1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| t_anti_b | 1 | CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | QP041B_ROLE_SCALE_FOR_HIGH_PRIORITY_MESON_QUEUE |
| t_anti_c | 0 | CANDIDATE_RETURN_CHANNEL_BINDING_SELECTOR_NEEDED | QP041C_RETURN_CHANNEL_BINDING_SCALE_SELECTOR |
| t_anti_d | 1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| t_anti_s | 1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| t_anti_t | 0 | BOUNDARY_NEUTRAL_SELF_CHANNEL_SELECTOR_NEEDED | NEUTRAL_SELF_CHANNEL_ROLE_SCALE_SELECTOR |
| t_anti_u | 0 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| u_anti_b | 1 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| u_anti_c | 0 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |
| u_anti_t | 0 | BOUNDARY_LOCAL_RETURN_NOT_SELECTED | LOCAL_WI_RETURN_SELECTOR_OR_ROLE_SCALE_SELECTOR |

## Key Fields

```text
meson_scaffold_rows = 36
filled_meson_scaffold_rows = 7
candidate_meson_scaffold_rows = 10
open_boundary_rows = 29
observed_meson_masses_used = False
free_parameters_introduced = 0
next_frontier = QP042_PRIVATE_BARYON_SCAFFOLD_FILL_PASS
```

## Interpretation

The meson table now has a real first fill layer. The filled rows are not inferred
from external observed meson masses; they are Phase 4 scaffolds reached by the
selected support families and the QP040 residue operator.

Rows that remain open now name the missing selector: either a role-scale
readout selector for queued heavy mesons, a return-channel binding selector, or
a neutral self-channel selector.
