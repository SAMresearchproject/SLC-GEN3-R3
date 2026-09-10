# QP041C - Private Meson Binding Readout Selector

## Preflight

```text
test_id = QP041C
test_name = PRIVATE_MESON_BINDING_READOUT_SELECTOR
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
QP041C_MESON_BINDING_READOUT_COORDINATES_SELECTED
```

QP041C emits SAM-native binding/readout coordinates:

```text
M_readout = M_role * R_bind(q,D)
```

Observed meson masses are not used.

## Binding Readout Rows

| scaffold | pair | role coordinate / MeV | q | native readout / MeV | status |
| --- | --- | ---: | ---: | ---: | --- |
| b_anti_c | b<->c | 3915.55786767 | 4 | 3889.7630751340125 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| c_anti_b | b<->c | 3915.55786767 | 4 | 3889.7630751340125 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| c_anti_s | c<->s | 346.105609494 | 0 | 346.105609494 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| s_anti_c | c<->s | 346.105609494 | 0 | 346.105609494 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| b_anti_t | b<->t | 16332.3044371 | 4 | 16224.710980732496 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| t_anti_b | b<->t | 16332.3044371 | 4 | 16224.710980732496 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| b_anti_s | b<->s | 363.179072431 | -7 | 367.4432691828114 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| s_anti_b | b<->s | 363.179072431 | -7 | 367.4432691828114 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| c_anti_t | c<->t | 5074.66763704 | -7 | 5134.250864425712 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |
| t_anti_c | c<->t | 5074.66763704 | -7 | 5134.250864425712 | FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE |

## Residue Selector

| selector class | source family | q | R_bind | selector rule |
| --- | --- | ---: | ---: | --- |
| DUAL_POLARITY_CHARGED_Q_ANTI_Q_RESIDUE | charged_pion_family | 4 | 0.9934122305408968 | dual-polarity charged role selects q=4 from charged pion family |
| TRANSITION_COLOR_Q_ANTI_Q_RESIDUE | charged_kaon_family | 0 | 1.0 | transition color-coupled role selects q=0 from charged kaon family |
| MIXED_NEUTRAL_Q_ANTI_Q_RESIDUE | neutral_kaon_family | -7 | 1.0117413063568566 | neutral binary mixing selects q=-7 from neutral kaon family |

## Boundary Delta

| boundary group | before | after | note |
| --- | ---: | ---: | --- |
| FILLED_ROLE_SCALE_BINDING_READOUT_OPEN | 8 | 0 | QP041C applies native residue selector to QP041B role-scale rows |
| CANDIDATE_RETURN_CHANNEL_BINDING_SELECTOR_NEEDED | 2 | 0 | QP041C applies mixed-neutral residue to QP039 return-channel rows |
| FILLED_NATIVE_MESON_BINDING_READOUT_COORDINATE | 0 | 10 | native binding/readout coordinates emitted without observed meson masses |

## Key Fields

```text
binding_readout_rows = 10
high_priority_role_rows_consumed = 8
return_channel_rows_consumed = 2
observed_meson_masses_used = False
free_parameters_introduced = 0
next_frontier = QP043_PRIVATE_UNKNOWN_MODE_CARRIER_ASSIGNMENT
```

## Interpretation

The high-priority meson queue now has native binding/readout coordinates. QP041C
also consumes the two `c<->t` return-channel rows because QP039 selected that
bridge and the phase role selects the mixed-neutral residue class.
