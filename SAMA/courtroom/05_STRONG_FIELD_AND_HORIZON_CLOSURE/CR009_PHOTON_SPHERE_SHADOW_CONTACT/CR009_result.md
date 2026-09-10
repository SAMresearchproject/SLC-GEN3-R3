# CR009 Photon Sphere Shadow Contact

## Verdict

```text
CR009_PASS_SCOPED_PHOTON_SPHERE_SHADOW_CONTACT
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SCOPED_PHOTON_SPHERE_SHADOW_INVARIANT
```

## Branch Claim Tested

```text
CR007 typed premise: photon sphere A=2/3 at r/r_s=3/2
CR008 typed boundary: A=1 closure, not A=2/3
b/r_s = x/sqrt(1 - 1/x)
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| sealed_scope_predates_test | true |
| cr007_typed_premise_present | true |
| cr008_typed_boundary_present | true |
| external_reference_required | true |
| free_parameters_introduced_zero | true |
| trace_ascii_clean | true |
| sam_photon_sphere_x_exact | true |
| sam_photon_sphere_A_exact | true |
| sam_shadow_bcrit_exact | true |
| sam_shadow_diameter_exact | true |
| sam_minimum_is_local | true |
| wrong_controls_do_not_match_full_packet | true |
| eht_image_overclaim_rejected | true |

## SAM Photon/Shadow Packet

| quantity | value | target |
|---|---:|---:|
| x_photon = r/r_s | 1.500000000000 | 1.500000000000 |
| A_photon | 0.666666666667 | 0.666666666667 |
| bcrit/r_s | 2.598076211353 | 2.598076211353 |
| shadow diameter/r_s | 5.196152422707 | 5.196152422707 |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Grade Reading

CR009 gives the 05 branch its first scoped photon-sphere/shadow external
reference contact. It does not claim full EHT image modeling, Kerr shadow
modeling, accretion physics, full strong-field metric closure, or full GR.

## Rule-9 Line

```text
This test could have falsified the claim that the CR007 A=2/3 photon-sphere landmark carries the standard Schwarzschild photon critical-impact/shadow invariant b_crit/r_s=3*sqrt(3)/2, rather than being only an internal A-label or a horizon-preserving but shadow-wrong construction.
```
