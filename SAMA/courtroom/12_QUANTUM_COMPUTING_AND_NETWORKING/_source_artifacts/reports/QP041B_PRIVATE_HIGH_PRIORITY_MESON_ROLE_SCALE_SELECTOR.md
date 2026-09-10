# QP041B - Private High-Priority Meson Role-Scale Selector

## Preflight

```text
test_id = QP041B
test_name = PRIVATE_HIGH_PRIORITY_MESON_ROLE_SCALE_SELECTOR
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
QP041B_HIGH_PRIORITY_MESON_ROLE_SCALE_COORDINATES_SELECTED
```

QP041B selects native role-scale coordinates for high-priority meson scaffolds
using the QP005 interaction mass coordinate:

```text
M_role = native_interaction_strength * (m_a + m_b)
```

This is not a final bound-meson mass claim. It fills the role-scale layer and
hands final binding/readout to QP041C.

## Filled Role-Scale Rows

| scaffold | pair | role coordinate / MeV | role operator | status |
| --- | --- | ---: | --- | --- |
| b_anti_c | b<->c | 3915.55786767 | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | FILLED_NATIVE_MESON_ROLE_SCALE_LOCK |
| c_anti_b | b<->c | 3915.55786767 | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | FILLED_NATIVE_MESON_ROLE_SCALE_LOCK |
| c_anti_s | c<->s | 346.105609494 | TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |
| s_anti_c | c<->s | 346.105609494 | TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |
| b_anti_t | b<->t | 16332.3044371 | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |
| t_anti_b | b<->t | 16332.3044371 | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |
| b_anti_s | b<->s | 363.179072431 | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |
| s_anti_b | b<->s | 363.179072431 | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |

## Pair Selector Table

| pair | priority | native strength | interaction coordinate / MeV | status |
| --- | --- | ---: | ---: | --- |
| b<->c | P1_ROLE_LOCK_FIRST | 0.717139946489 | 3915.55786767 | FILLED_NATIVE_MESON_ROLE_SCALE_LOCK |
| c<->s | P2_A_SHARE_ROLE_CANDIDATE | 0.252472987837 | 346.105609494 | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |
| b<->t | P2_A_SHARE_ROLE_CANDIDATE | 0.0923016101689 | 16332.3044371 | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |
| b<->s | P2_A_SHARE_ROLE_CANDIDATE | 0.0849597126971 | 363.179072431 | FILLED_NATIVE_MESON_A_SHARE_ROLE_SCALE_COORDINATE |

## Boundary Delta

| boundary group | before | after | note |
| --- | ---: | ---: | --- |
| CANDIDATE_MESON_READOUT_ROLE_SCALE_SELECTOR_NEEDED | 8 | 0 | QP041B fills role-scale coordinates for the high-priority meson queue |
| FILLED_ROLE_SCALE_BINDING_READOUT_OPEN | 0 | 8 | rows now carry native role coordinate but still need final binding/readout selector |
| CANDIDATE_RETURN_CHANNEL_BINDING_SELECTOR_NEEDED | 2 | 2 | QP041B does not touch c<->t return-channel binding rows |

## Key Fields

```text
high_priority_pairs = 4
filled_role_scale_pairs = 4
filled_role_scale_rows = 8
final_bound_mass_rows_emitted = 0
observed_meson_masses_used = False
free_parameters_introduced = 0
next_frontier = QP041C_PRIVATE_MESON_BINDING_READOUT_SELECTOR
```

## Interpretation

QP041B advances the meson table one layer deeper. The eight high-priority
candidate scaffolds are no longer generic blanks; they now carry native role
coordinates and wait only for the final binding/readout selector.
