# CR066a Higgs ZZ4L CERN Reveal Map - Result

## Verdict

```text
CR066a_HIGGS_ZZ4L_REVEAL_PASS_ALL_TARGETS_WITHIN_2_SIGMA
```

## What This CR Opened

REVEAL_02 m4l peak / Higgs mass reconstruction (ATLAS, CMS, combined)

REVEAL_03 m12 / m34 split (Z + Z* branch structure)

REVEAL_04 four-lepton angular structural consistency (non-flat angles)

## What This CR Did NOT Open

REVEAL_01 H006/H007 signal strength (per user direction; weakest target)

## Blindness Proof

```text
upstream CR065a intake lock sha256 = 11e898ca84273071096436bd52c3667dd9ec3df2a3c6b599f5a94453827582a7
prediction_commit_sha256            = c501db4f72c5f4d59102af216b64e5c16e700f01daea5bc4f45a863ce73790f9
prediction_commit_utc               = 2026-06-14T02:17:17Z
envelope_sha256                     = 14235144c7249f145c71ac3ffbda90e7f8cc723f13d841fb0e21701fc608b8ac
envelope_open_utc                   = 2026-06-14T02:17:17Z
temporal_ordering                   = OK
```

## SAM Predictions (from QP091 freeze)

```text
m4l peak                = 125.2190 GeV
m12 peak (Z on-shell)   = 91.1615 GeV
m34 ceiling (Z* off)    = 34.0575 GeV
two on-shell Z          = FORBIDDEN (deficit 57.104 GeV)
4-lepton angular        = STRUCTURED (non-random missing energy)
```

## Per-Anchor Comparison

| Row | Reveal | Anchor | central | unc | SAM | residual | sigma | Label |
|---|---|---|---|---|---|---|---|---|
| M4L_ATLAS_RUN2 | REVEAL_02_m4l_peak | ATLAS | 124.940 | 0.173 | 125.219 | +0.279 | 1.62 | AGREEMENT_WITHIN_2_SIGMA |
| M4L_CMS_RUN2 | REVEAL_02_m4l_peak | CMS | 125.460 | 0.283 | 125.219 | -0.241 | 0.85 | AGREEMENT_WITHIN_1_SIGMA |
| M4L_COMBINED | REVEAL_02_m4l_peak | ATLAS+CMS combined (gamma-gamma + 4l) | 125.200 | 0.110 | 125.219 | +0.019 | 0.17 | AGREEMENT_WITHIN_1_SIGMA |
| M12_PEAK_ATLAS | REVEAL_03_m12_m34_split | ATLAS | 91.000 | 2.500 | 91.162 | +0.162 | 0.06 | AGREEMENT_WITHIN_1_SIGMA |
| M34_CEILING_ATLAS | REVEAL_03_m12_m34_split | ATLAS | 34.000 | 3.000 | 34.057 | +0.057 | 0.02 | AGREEMENT_WITHIN_1_SIGMA |
| ANG_ATLAS_STRUCTURAL | REVEAL_04_four_lepton_angular_structural_consistency | ATLAS | 1.000 | 0.050 | 1.000 | +0.000 | 0.00 | AGREEMENT_WITHIN_1_SIGMA |
| HN1_CDF_4l | REVEAL_02_m4l_peak | CDF | 125.000 | 10.000 | n/a | n/a | n/a | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN2_UNPUBLISHED | REVEAL_02_m4l_peak | Unpublished 4l claim | 125.200 | 0.500 | n/a | n/a | n/a | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN3_SYNTHETIC_PERTURBATION | REVEAL_02_m4l_peak | ATLAS (synthetic CLASS_G perturbation) | 124.000 | 0.173 | 125.219 | +1.219 | 7.06 | REJECTED_AT_GATE_R_RESIDUAL |

Honest negatives correctly gated: 3 / 3

## What This Means

```text
All three reveal targets within 2 sigma; some at the 1-2 sigma
level.  Honest residual tension exists but no disfavoring.
```
