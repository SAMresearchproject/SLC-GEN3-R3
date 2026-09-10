# QP040 - Private Native Binding Residue Operator

## Preflight

```text
test_id = QP040
test_name = PRIVATE_NATIVE_BINDING_RESIDUE_OPERATOR
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
QP040_NATIVE_BINDING_RESIDUE_OPERATOR_SELECTED
```

QP040 selects the common native binding residue operator:

```text
R_bind(q,D)=1/(1+(A0/2)*q/2^D)
```

The operator is extracted from the selected native support formulas only. No
observed composite masses are used.

## Operator Table

| composite | branch | q | R_bind | operator class | status |
| --- | --- | ---: | ---: | --- | --- |
| proton | baryon | 6 | 0.9901507879804149 | QQQ_COLOR_SINGLET_POSITIVE_Q_RETURN_SUPPRESSION | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |
| neutron | baryon | 5 | 0.9917788279726211 | QQQ_COLOR_SINGLET_POSITIVE_Q_RETURN_SUPPRESSION | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |
| charged_pion_family | meson | 4 | 0.9934122305408968 | Q_ANTI_Q_POSITIVE_Q_RETURN_SUPPRESSION | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |
| neutral_pion_family | meson | -15 | 1.0255021462062524 | Q_ANTI_Q_NEGATIVE_Q_RETURN_AMPLIFICATION | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |
| charged_kaon_family | meson | 0 | 1.0 | Q_ANTI_Q_NEUTRAL_Q_RETURN | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |
| neutral_kaon_family | meson | -7 | 1.0117413063568566 | Q_ANTI_Q_NEGATIVE_Q_RETURN_AMPLIFICATION | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |
| deuteron | nuclear_composite | -16 | 1.0272486158323275 | NUCLEAR_COMPOSITE_CLUSTER_NEGATIVE_Q_RETURN_AMPLIFICATION | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |
| alpha_particle | nuclear_composite | -12 | 1.0202981874959534 | NUCLEAR_COMPOSITE_CLUSTER_NEGATIVE_Q_RETURN_AMPLIFICATION | FILLED_NATIVE_BINDING_RESIDUE_OPERATOR |

## Native Replay Without Observed Masses

| composite | replay mass / MeV | source SAM mass / MeV | delta / MeV | status |
| --- | ---: | ---: | ---: | --- |
| proton | 938.6870753630358 | 938.687075363 | 3.581135388230905e-11 | PASS_NATIVE_FORMULA_REPLAY |
| neutron | 940.230496948323 | 940.2304969483 | 2.2964741219766438e-11 | PASS_NATIVE_FORMULA_REPLAY |
| charged_pion_family | 139.52281516835575 | 139.5228151684 | 4.425260158313904e-11 | PASS_NATIVE_FORMULA_REPLAY |
| neutral_pion_family | 135.02792005777698 | 135.0279200578 | 2.3021584638627246e-11 | PASS_NATIVE_FORMULA_REPLAY |
| charged_kaon_family | 493.7626918577156 | 493.7626918577 | 1.5575096767861396e-11 | PASS_NATIVE_FORMULA_REPLAY |
| neutral_kaon_family | 497.3398437308903 | 497.3398437309 | 9.663381206337363e-12 | PASS_NATIVE_FORMULA_REPLAY |
| deuteron | 1875.5759055320948 | 1875.575905532 | 9.481482265982777e-11 | PASS_NATIVE_FORMULA_REPLAY |
| alpha_particle | 3725.771283468602 | 3725.771283469 | 3.979039320256561e-10 | PASS_NATIVE_FORMULA_REPLAY |

## Handoff

| target | branch | input rows | status |
| --- | --- | ---: | --- |
| QP041_PRIVATE_MESON_SCAFFOLD_FILL_PASS | meson | 4 | READY_WITH_NATIVE_BINDING_RESIDUE_OPERATOR |
| QP042_PRIVATE_BARYON_SCAFFOLD_FILL_PASS | baryon | 2 | READY_WITH_NATIVE_BINDING_RESIDUE_OPERATOR |
| QP043_PRIVATE_UNKNOWN_MODE_CARRIER_ASSIGNMENT | unknown_mode | 5 | WAIT_FOR_QP041_QP042_FILL_RESULTS |

## Key Fields

```text
operator_rows = 8
support_rows_replayed = 8
replay_pass_rows = 8
observed_composite_masses_used = False
free_parameters_introduced = 0
next_frontier = QP041_PRIVATE_MESON_SCAFFOLD_FILL_PASS
```

## Interpretation

QP039 supplied the return-channel bridge. QP040 supplies the binding residue
operator that the scaffold-fill passes need:

```text
mass readout = native role scale * R_bind(q, D)
```

The next gates can now ask which meson and baryon scaffolds receive a unique
readout, instead of treating the scaffold table as decorative inventory.
