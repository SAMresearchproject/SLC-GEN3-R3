# CR003 A-Kernel Typed Readout Recertification

## Verdict

```text
CR003_BOUNDARY_A_KERNEL_TYPED_READOUT_RECERTIFIED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
```

## Selected Kernel

```text
A(r) = r_s/r
r_s = 2GM/c^2
selected_candidate = correct_A
```

## Computed Sample

```text
r_s = 0.0088701028718461
A = 1.3922622621010988e-09
Phi_from_A = -62565145.91115995
Phi_Newton = -62565145.91115994
weak_clock_exact = 0.9999999993038688
weak_clock_first_order = 0.9999999993038688
many_source_A = 2.297220655470099e-09
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| trace_ascii_clean | true |
| selected_unique_correct_A | true |
| wrong_controls_do_not_match_full_packet | true |
| potential_identity_closes | true |
| horizon_identity_closes | true |
| many_source_identity_closes | true |

## Candidate Controls

| candidate | full_packet | selector_score |
|---|---:|---:|
| correct_A | true | 5 |
| half_A | false | 2 |
| inverse_square_A | false | 1 |
| potential_doubled | false | 3 |
| horizon_shifted | false | 4 |
| clock_linear | false | 4 |

## Rule-9 Line

```text
This test could have falsified: the claim that A(r)=r_s/r uniquely supplies the native typed weak-field readout packet for horizon, potential, force, clock, and many-source accumulation lanes.
```

## Courtroom Reading

CR003 recertifies the A-kernel as a native typed readout packet.
It does not use older G-test outputs as inputs. It remains BOUNDARY
until external-data branches such as GPS, Shapiro, weak-field,
SN/BAO, or CMB attach observed data.
