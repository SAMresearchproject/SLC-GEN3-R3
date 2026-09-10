# CR096 Wrong Controls / Honest Negatives - Provisional Result

## Verdict

```text
CR096_TWO_GATE_RESOLUTION_PROOF_BUILT (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## Gate Counts

```text
Gate A (admissibility) rejections : 3
Gate R (residual) rejections      : 1
Gate-declaration mismatches       : 0
```

## Blindness Proof

```text
prediction_commit_sha256 = ae7c7833d3d837f0760297f4de9fcf2937766475d05d651daccf9e1bd8940a3c
prediction_commit_utc    = 2026-06-13T21:29:08Z
anchor_envelope_sha256   = 4515d7afe9e19bc61781f2394b6b92bf346171ecc707cdcc40b9ce9bb9fafed9
anchor_envelope_open_utc = 2026-06-13T21:29:08Z
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## Per-Row Resolution

| Row | Class | Observable | Experiment | CERN value | Declared gate | Actual gate | Label | Informational residual (if Gate A blocked) |
|---|---|---|---|---|---|---|---|---|
| HN001 | CLASS_B | W boson mass | CDF | 80433.5 +/- 6.4 +/- 6.9 MeV | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY | -68.40 MeV (-0.0850%) |
| HN005 | CLASS_F | W boson mass | PDG (world average) | 80369.2 +/- 13.3 +/- 0.0 MeV | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY | -4.10 MeV (-0.0051%) |
| HN006 | CLASS_A | Higgs boson mass | ATLAS (withdrawn / superseded) | 125360.0 +/- 400.0 +/- 180.0 MeV | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY | -141.00 MeV (-0.1125%) |
| HN007 | CLASS_G | Higgs boson mass | CMS | 126780.0 +/- 140.0 +/- 0.0 MeV | GATE_R_RESIDUAL | GATE_R_RESIDUAL | REJECTED_AT_GATE_R_RESIDUAL | actual residual -1561.00 MeV (-1.2313%) |

## Why The Two-Gate Split Matters

```text
HN001 (CDF W mass) is interesting: residual against 09a is -68.4 MeV
                                   (-0.085%) - this is WITHIN the
                                   CR091 W-mass band of 25 MeV?
                                   NO: 68.4 > 25 here, but if the band
                                   were 0.5%, CDF would pass residual.
                                   Gate A catches CDF regardless,
                                   because it's Tevatron not CERN.

HN005 (PDG world-average W) is the cleanest demonstration: residual
       against 09a is -4.1 MeV (-0.005%), which would PASS any
       reasonable W-mass band. Gate R alone cannot tell PDG from
       an individual CERN measurement. Gate A rejects PDG because
       PDG is a world average, not an independent measurement.

HN007 (synthetic CLASS_G CMS Higgs +1400 MeV) is the Gate R proof:
       admissibility passes (real CMS, real publication structure),
       but the central value is shifted out of the CR092 300 MeV
       band by design.
```

## Rule-9 Reminder

```text
This CR does not falsify 09a. It demonstrates that the 13-branch
honest-negative discipline rejects wrong-controls on the correct
mechanism per class.
```
