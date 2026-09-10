# CR108 Planck Omega_b Cosmological Anchor Intake - Result

## Verdict

```text
CR108_PLANCK_OMEGA_B_INTAKE_PASS
```

## What This CR Intakes

Public Planck 2018 cosmological parameters (Planck Collaboration 2020, A&A 641 A6, arXiv:1807.06209).  Sealed as a Courtroom anchor against which CR111 will appeal the cosmic baryon Omega_b closure.

**This CR reveals no match.**  Match reveal is deferred to CR111.

## Planck 2018 Reference (baseline LCDM TT,TE,EE+lowE+lensing)

| parameter | value | uncertainty | role |
|---|---|---|---|
| Omega_b_h2 | 0.02237 | 0.00015 | PRIMARY anchor for CR111 cosmic baryon closure appeal |
| Omega_c_h2 | 0.12 | 0.0012 | secondary - cold component reference for cumulative-A reading |
| H0_km_s_Mpc | 67.36 | 0.54 | Hubble constant from same dataset |
| Omega_b | 0.0493 | 0.00057 | baryon density parameter (Omega_b h^2 / h^2) |
| n_s | 0.9649 | 0.0042 | scalar spectral index |
| sigma_8 | 0.8111 | 0.006 | matter power normalization |

## Cryptographic Chain

```text
CR107 SPARC anchor                  = 937ee99e4605dff30ee0fac1ef12ad2e3bfd2091e4ca296c83a1afa77259388c
CR106 14 branch verdict             = 09eb6ae0055ebe5e53db9c2dc3df205c0613c4af5671341b7d5b4e7e07aa0ea6
BLINDNESS_PROTOCOL.md               = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR108 Planck anchor sha256          = 736ac1405394b787d86db26f785458266f069472953abee97c39aa69d5a6ade5
```

## Predictions

- **[PASS]** P1_planck_2018_reference_sealed
- **[PASS]** P2_upstream_cr107_anchor_present
- **[PASS]** P3_cr106_branch_verdict_present
- **[PASS]** P4_blindness_protocol_present
- **[PASS]** P5_zero_free_parameters_at_intake
- **[PASS]** P6_no_match_revealed_yet

## Wrong Controls

- **[PASS]** WC1_no_sam_prediction_value_substituted_for_planck_reference
- **[PASS]** WC2_no_prior_CR_verdict_modified
- **[PASS]** WC3_anchor_file_sealed_with_sha256_sibling

## Next CRs

- **CR109** intakes microlensing PBH abundance constraints.
- **CR110** opens the three-mode Earth/Galaxy/PBH closure appeal.
- **CR111** opens the cosmic baryon Omega_b closure appeal against this Planck anchor.
