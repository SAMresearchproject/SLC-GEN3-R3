# CR107 SPARC Galaxy Rotation Curve Reference Intake - Result

## Verdict

```text
CR107_SPARC_REFERENCE_INTAKE_PASS
```

## What This CR Intakes

Public SPARC database reference parameters (Lelli, McGaugh, Schombert 2016, AJ 152 157, arXiv:1606.09251).  Sealed as a Courtroom anchor against which CR110 will appeal the three-mode Earth/Galaxy/PBH A-field closure using the upstream G732c PASS (native R12 cored halo law) and CR104a forward-blind prediction PRED_1.

**This CR reveals no match.**  Match reveal is deferred to CR110.

## SPARC Public Reference

```text
galaxies (full)         = 175
galaxies (quality)      = 153
morphology range        = S0 to Irr
stellar mass log10 M_sun = [7.0, 11.5]
V_rot range km/s        = [20.0, 350.0]
rotation method         = HI 21-cm + Halpha
photometry              = Spitzer 3.6 micron (stellar mass tracer)
```

## Cryptographic Chain

```text
CR104a appeal lock                  = 090c9e450a38741499cbda2adaf0ea6a8aeb2296bf7ec78265c13bfcdd26e850
CR106 14 branch verdict             = 09eb6ae0055ebe5e53db9c2dc3df205c0613c4af5671341b7d5b4e7e07aa0ea6
BLINDNESS_PROTOCOL.md               = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR107 SPARC anchor sha256           = 937ee99e4605dff30ee0fac1ef12ad2e3bfd2091e4ca296c83a1afa77259388c
```

## Predictions

- **[PASS]** P1_sparc_public_reference_sealed
- **[PASS]** P2_upstream_cr104a_lock_present
- **[PASS]** P3_cr106_branch_verdict_present
- **[PASS]** P4_blindness_protocol_present
- **[PASS]** P5_zero_free_parameters_at_intake
- **[PASS]** P6_no_match_revealed_yet

## Wrong Controls

- **[PASS]** WC1_no_sam_prediction_value_substituted_for_reference
- **[PASS]** WC2_no_prior_CR_verdict_modified
- **[PASS]** WC3_anchor_file_sealed_with_sha256_sibling

## Next CRs

- **CR108** intakes Planck 2018 Omega_b cosmological anchor.
- **CR109** intakes microlensing PBH abundance constraints.
- **CR110** opens the three-mode Earth/Galaxy/PBH closure appeal using CR107/CR108/CR109 anchors.
- **CR111** opens the cosmic baryon Omega_b closure appeal.
