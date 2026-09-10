# CR103 GATE_1 N_SW Multiplicity Scaling - Result

## Verdict

```text
CR103_CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## SAM Commitment (Locked Before Anchor Open)

```text
GATE_1 candidate: paired source/recoil count (#4 from CR100 enumeration)
Reading: simplest (one source-recoil pair = one produced particle;
          total pairs linear in collision available energy)
Predicted scaling: N_ch(s) = K * s^(alpha_SAM/2)
alpha_SAM = 1.0
Free parameters in exponent: 0
Free parameters in normalization: 1 (anchored at lowest sqrt(s))
Upstream CR100 question lock sha256: fb310a23497308e9b0b92c23974cb08a230c7a8779c36aabd94feb628e145867
```

## Blindness Proof

```text
prediction_commit_sha256 = 509ac7b6cfbc80daff75160985ac97bc8c4b81f6e5cfa2513dee17875cb39926
prediction_commit_utc    = 2026-06-13T22:28:23Z
anchor_envelope_sha256   = 305d694e3a5f06b0b649947da89dc0187c034e17dc8f33100ebf2434040d5b80
anchor_envelope_open_utc = 2026-06-13T22:28:23Z
temporal_ordering        = OK
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## Per-Anchor Prediction vs Measurement

| Row | Experiment | sqrt(s) TeV | Measured | SAM predicted | Residual | %  | Sigma | Label |
|---|---|---|---|---|---|---|---|---|
| A1 | ATLAS | 0.9 | 3.81 +/- 0.15 | 3.81 | +0.00 | +0.0% | 0.0 | NORMALIZATION_ANCHOR_BY_CONSTRUCTION |
| A2 | ATLAS | 7.0 | 5.83 +/- 0.23 | 10.63 | +4.80 | +82.3% | 20.8 | AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA |
| A3 | ATLAS | 13.0 | 6.42 +/- 0.16 | 14.48 | +8.06 | +125.5% | 50.3 | AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA |
| A4 | CMS | 7.0 | 5.78 +/- 0.23 | 10.63 | +4.85 | +83.8% | 21.0 | AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA |
| A5 | CMS | 13.0 | 5.49 +/- 0.17 | 14.48 | +8.99 | +163.8% | 52.8 | AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA |
| A6 | ALICE | 7.0 | 6.00 +/- 0.20 | 10.63 | +4.63 | +77.1% | 23.1 | AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA |
| A7 | ALICE | 13.0 | 6.46 +/- 0.39 | 14.48 | +8.02 | +124.2% | 20.6 | AGREEMENT_OUTSIDE_ANCHOR_3_SIGMA |

## Cross-Source Observed Scaling Exponents

| Low anchor | High anchor | alpha_obs |
|---|---|---|
| ATLAS at 0.9 TeV (A1) | ATLAS at 7.0 TeV (A2) | 0.207 |
| ATLAS at 0.9 TeV (A1) | CMS at 7.0 TeV (A4) | 0.203 |
| ATLAS at 0.9 TeV (A1) | ALICE at 7.0 TeV (A6) | 0.221 |
| ATLAS at 0.9 TeV (A1) | ATLAS at 13.0 TeV (A3) | 0.195 |
| ATLAS at 0.9 TeV (A1) | CMS at 13.0 TeV (A5) | 0.137 |
| ATLAS at 0.9 TeV (A1) | ALICE at 13.0 TeV (A7) | 0.198 |
| ATLAS at 7.0 TeV (A2) | ATLAS at 13.0 TeV (A3) | 0.156 |
| ATLAS at 7.0 TeV (A2) | CMS at 13.0 TeV (A5) | -0.097 |
| ATLAS at 7.0 TeV (A2) | ALICE at 13.0 TeV (A7) | 0.166 |
| CMS at 7.0 TeV (A4) | ATLAS at 13.0 TeV (A3) | 0.170 |
| CMS at 7.0 TeV (A4) | CMS at 13.0 TeV (A5) | -0.083 |
| CMS at 7.0 TeV (A4) | ALICE at 13.0 TeV (A7) | 0.180 |
| ALICE at 7.0 TeV (A6) | ATLAS at 13.0 TeV (A3) | 0.109 |
| ALICE at 7.0 TeV (A6) | CMS at 13.0 TeV (A5) | -0.143 |
| ALICE at 7.0 TeV (A6) | ALICE at 13.0 TeV (A7) | 0.119 |

**Median alpha_obs:** `0.166` if cross-source pairs available.

## Exponent Comparison

```text
SAM alpha_SAM (simple reading)   = 1.000
median alpha_obs (LHC data)      = 0.166
difference alpha_SAM - alpha_obs = +0.834
```

## Honest-Negative Resolution Proof

| Row | Class | Anchor | Declared gate | Actual gate | Label |
|---|---|---|---|---|---|
| HN1 | CLASS_A | ATLAS (withdrawn early multiplicity measurement) | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN2 | CLASS_X_UNPUBLISHED | Unpublished multiplicity claim (no journal reference) | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN3 | CLASS_G | ATLAS (synthetic CLASS_G perturbation of 13 TeV value) | GATE_R_RESIDUAL | GATE_R_RESIDUAL | REJECTED_AT_GATE_R_RESIDUAL |

Honest-negatives correctly gated: 3 / 3

## What This Test Means

```text
LHC pp data scales much more slowly with collision energy than
SAM's simplest reading of GATE_1 candidate #4 predicts. The naive
linear-in-energy mapping from 'paired source/recoil count' to
'particle multiplicity' is firmly disfavored at LHC precision.

This does NOT close GATE_1 against candidate #4 entirely - it
closes the SIMPLEST READING of that candidate. A non-trivial
N_SW -> multiplicity mapping where each particle uses many SWs
(more SWs per particle at higher energy) could in principle
reproduce the observed s^0.11 scaling.

The other three candidates (local echo intensity, signed contact
count, closed-loop intersection count) remain in CR100's sealed
enumeration. CR103 has narrowed the closure space by one
specific reading.

Upstream consequence: SAM needs a multi-SW-per-particle scaling
law to make any of the four N_SW candidates reproduce the
observed slow multiplicity growth.
```

## Rule-9 Line

```text
This CR tested ONE specific reading of ONE specific candidate
(candidate #4 simplest reading). It does not falsify GATE_1
candidate #4 in general; it does not exclude candidates 1-3;
it does not modify CR100's sealed open-gate enumeration.

What it does: narrow the closure space by recording on the
public sealed record that one specific naive reading does not
match world-class LHC multiplicity measurements. That is real
progress toward GATE_1 closure - even when the news is bad,
the bad news points SAM to where the next derivation must do
more work.
```
