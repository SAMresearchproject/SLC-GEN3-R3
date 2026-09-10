# CR010 ISCO Orbital Contact

## Verdict

```text
CR010_PASS_SCOPED_ISCO_ORBITAL_CONTACT
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SCOPED_ISCO_ORBITAL_CONTACT
```

## Branch Claim Tested

```text
CR007 typed premise: ISCO A = 1/3 at r/r_s=3
CR008 typed boundary: A=1 closure, not A=1/3
CR009 typed photon contact: A=2/3 photon sphere remains distinct from ISCO
E/c^2 = (1 - 1/x) / sqrt(1 - 3/(2x))
L/(m c r_s) = x / sqrt(2x - 3)
Omega r_s/c = 1 / sqrt(2 x^3)
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| sealed_scope_predates_test | true |
| cr007_typed_premise_present | true |
| cr008_typed_boundary_present | true |
| cr009_typed_photon_contact_present | true |
| external_reference_required | true |
| free_parameters_introduced_zero | true |
| trace_ascii_clean | true |
| sam_isco_x_exact | true |
| sam_isco_A_exact | true |
| sam_isco_energy_exact | true |
| sam_isco_angular_momentum_exact | true |
| sam_isco_frequency_exact | true |
| sam_isco_is_local_stability_minimum | true |
| wrong_controls_do_not_match_full_packet | true |
| declared_readout_preserved | true |

## SAM ISCO Packet

| quantity | value | target |
|---|---:|---:|
| x_ISCO = r/r_s | 3.000000000000 | 3.000000000000 |
| A_ISCO | 0.333333333333 | 0.333333333333 |
| E_ISCO/c^2 | 0.942809041582 | 0.942809041582 |
| L_ISCO/(m c r_s) | 1.732050807569 | 1.732050807569 |
| Omega_ISCO r_s/c | 0.136082763488 | 0.136082763488 |

## Stability Check

| quantity | value |
|---|---:|
| local_stability_minimum | true |
| d(L^2)/dx left of x=3 | -6.673339658647e-04 |
| d(L^2)/dx right of x=3 | 6.660008100567e-04 |
| stability_transition | true |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Grade Reading

CR010 gives the 05 branch a scoped strong-field ISCO landmark
contact showing that the SAM A-kernel naturally indexes ISCO as
A = 1/3. The record supplies the declared ISCO packet,
wrong-control rejection, and artifact hashes for the CR011
deferred-support ledger.

## Rule-9 Line

```text
This test could have falsified the claim that the CR007 A = 1/3 ISCO landmark naturally indexes the standard strong-field timelike circular-orbit ISCO contact r/r_s=3 with E/c^2=sqrt(8/9), L/(m c r_s)=sqrt(3), and Omega r_s/c=1/sqrt(54), rather than being only an internal A-label or an orbit-wrong construction that preserves a nearby landmark.
```
