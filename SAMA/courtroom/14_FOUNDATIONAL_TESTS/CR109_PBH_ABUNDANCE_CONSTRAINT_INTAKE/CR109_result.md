# CR109 PBH Abundance Constraint Intake - Result

## Verdict

```text
CR109_PBH_ABUNDANCE_INTAKE_PASS
```

## What This CR Intakes

Public Primordial Black Hole f_PBH = Omega_PBH/Omega_DM constraint envelope from leading microlensing + dynamical surveys (EROS-2, OGLE, Subaru HSC, Kepler, Segue 1).  Sealed as a Courtroom anchor against which CR110 will appeal the three-mode Earth/Galaxy/PBH closure using the CR104a Layer 4 cumulative-A dark matter reading.

**This CR reveals no match.**  Match reveal is deferred to CR110.

## PBH Constraint Envelope

| mass window M_sun | f_PBH upper limit | method | source |
|---|---|---|---|
| 1e-11 to 1e-9 | 1e-02 | femtolensing of GRBs / asteroid-mass PBH bound | Barnacka+ 2012 PRD 86 043001 (envelope) |
| 1e-8 to 1e-6 | 1e-01 | Subaru HSC microlensing of M31 | Niikura+ 2019 Nature Astron 3 524 |
| 1e-6 to 1e-3 | 1e-01 | Kepler stellar microlensing | Griest+ 2014 ApJ 786 158 |
| 1e-3 to 1.0 | 1e-01 | EROS-2 + OGLE LMC/SMC microlensing | Tisserand+ 2007 A&A 469 387; Wyrzykowski+ 2011 MNRAS 416 2949 |
| 1.0 to 1e2 | 1e-01 | EROS-2 + OGLE long-event tails | Tisserand+ 2007 A&A 469 387 (envelope) |
| 1e2 to 1e3 | 1e-02 | Segue 1 dynamical heating / wide binary stability | Brandt 2016 ApJ 824 L31 |

## Cryptographic Chain

```text
CR108 Planck anchor                 = 736ac1405394b787d86db26f785458266f069472953abee97c39aa69d5a6ade5
CR107 SPARC anchor                  = 937ee99e4605dff30ee0fac1ef12ad2e3bfd2091e4ca296c83a1afa77259388c
CR104a appeal lock                  = 090c9e450a38741499cbda2adaf0ea6a8aeb2296bf7ec78265c13bfcdd26e850
BLINDNESS_PROTOCOL.md               = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR109 PBH anchor sha256             = 8594e7025ffe9b92bd3592bf80195385347059b66973a51e3b6e128c760ace86
```

## Predictions

- **[PASS]** P1_pbh_constraint_envelope_sealed
- **[PASS]** P2_upstream_cr108_anchor_present
- **[PASS]** P3_upstream_cr107_anchor_present
- **[PASS]** P4_upstream_cr104a_lock_present
- **[PASS]** P5_blindness_protocol_present
- **[PASS]** P6_zero_free_parameters_at_intake
- **[PASS]** P7_no_match_revealed_yet

## Wrong Controls

- **[PASS]** WC1_no_sam_prediction_substituted_for_pbh_envelope
- **[PASS]** WC2_no_prior_CR_verdict_modified
- **[PASS]** WC3_anchor_file_sealed_with_sha256_sibling

## Next CRs

- **CR110** opens the three-mode Earth/Galaxy/PBH closure appeal using CR107/CR108/CR109 anchors.
- **CR111** opens the cosmic baryon Omega_b closure appeal.
