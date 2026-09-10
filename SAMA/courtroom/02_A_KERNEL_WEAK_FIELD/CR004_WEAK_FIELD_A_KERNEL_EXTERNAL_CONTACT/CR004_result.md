# CR004 Weak-Field A-Kernel External Contact

## Verdict

```text
CR004_PASS_SCOPED_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SCOPED_WEAK_FIELD
```

## Branch Claim Tested

```text
A(r) = r_s/r = 2GM/(c^2 r)
Phi = -c^2 A/2
g = (c^2/2) |dA/dr|
v_escape = c sqrt(A)
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| external_data_required | true |
| free_parameters_introduced_zero | true |
| trace_ascii_clean | true |
| sam_packet_passes_all_bodies | true |
| wrong_controls_do_not_match_full_packet | true |

## External Anchor Rows

| body | candidate | g | v_escape | full_packet |
|---|---|---:|---:|---:|
| Earth | sam_A_kernel | 9.82025048706 | 11186.1356914 | true |
| Moon | sam_A_kernel | 1.62490442956 | 2376.17716339 | true |
| Sun | sam_A_kernel | 274.200111695 | 617674.700317 | true |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's weak-field A-kernel A(r)=r_s/r carries the correct factor, radial power, potential lane, acceleration lane, and escape-speed lane against external weak-field anchors.
```

## Courtroom Reading

CR004 gives the weak-field A-kernel an external-contact PASS in a
scoped local weak-field lane. It does not claim GPS, Shapiro delay,
strong-field closure, or full GR; those remain separate branches.
