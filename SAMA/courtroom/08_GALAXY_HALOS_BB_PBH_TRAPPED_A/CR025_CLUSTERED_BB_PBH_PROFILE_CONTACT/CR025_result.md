# CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT

## Verdict

```text
CR025_PASS_CLUSTERED_BB_PBH_PROFILE_CONTACT_RADIAL_LAW_OPEN
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SCOPED_CLUSTERED_HALO_PROFILE_CONTACT
```

## Question

```text
Does the clustered BB-PBH/trapped-A halo profile contact strongly improve the real SPARC rotation-curve fit while preserving the native radial-law debt?
```

## Pass Conditions

| condition | pass |
|---|---:|
| realistic_clustered_halo_profile_passed | true |
| real_sparc_sample_fit | true |
| clustered_profile_improves_baryon_only | true |
| halo_requires_clustered_overdensity | true |
| native_radial_selector_debt_preserved | true |
| wrong_controls_rejected_upstream | true |
| free_parameters_introduced_zero | true |

## Evidence Rows

| item | value | pass |
|---|---:|---:|
| galaxies_fit | 175 | true |
| median_baryon_rms_kms | 40.95236813050122 | true |
| median_halo_rms_kms | 3.625430524040301 | true |
| median_chi2_improvement_factor | 150.7662388291606 | true |
| median_halo_overdensity_vs_cosmic_dm_mean | 79090.03192365015 | true |
| selector_open | native radial organization law / mass function / concentration relation | true |

## Wrong Controls

```text
wrong_control_full_packet_count = 0
```

## Scope

CR025 is a scoped external-contact test. It records clustered profile compatibility and explicitly keeps native radial organization / mass function / concentration as open selectors.

## Rule-9 Line

```text
This test could have falsified: the claim that a clustered BB-PBH/trapped-A halo profile can carry the real SPARC rotation residual far better than baryons alone.
```
