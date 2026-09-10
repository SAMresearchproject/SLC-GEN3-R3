# CR101 GATE_2 c_SW vs c Partial Closure - Result

## Verdict

```text
CR101_PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_2_SIGMA_ONLY (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## SAM Commitment (Locked Before Anchor Open)

```text
GATE_2 candidate selected (from CR100 sealed enumeration):
  c_SW = c (identity)

Expressed as testable prediction: (v_substrate - c) / c = 0
Free parameters introduced: 0
Upstream CR100 question lock sha256: fb310a23497308e9b0b92c23974cb08a230c7a8779c36aabd94feb628e145867
```

## Blindness Proof

```text
prediction_commit_sha256 = a0a46b4a79dfd043f3e6f3b5fd66941582328f526b75eda3b7d1a0bbfaea178b
prediction_commit_utc    = 2026-06-13T22:06:53Z
anchor_envelope_sha256   = b38b02157862564e3e8597e3c11404fca925c8bfaf59411075ab87ad5e970972
anchor_envelope_open_utc = 2026-06-13T22:06:53Z
temporal_ordering        = OK
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## Live CERN-Class Anchors (Pillar 3 Cross-Source)

| Row | Experiment | (v-c)/c +/- combined sigma | Distance to 0 (in sigma) | Label |
|---|---|---|---|---|
| A1 | ICARUS | +4.00e-07 +/- 2.80e-06 | 0.14 sigma | AGREEMENT_WITHIN_ANCHOR_1_SIGMA |
| A2 | OPERA | +2.70e-06 +/- 3.10e-06 | 0.87 sigma | AGREEMENT_WITHIN_ANCHOR_1_SIGMA |
| A3 | BOREXINO | +2.70e-06 +/- 1.90e-06 | 1.42 sigma | AGREEMENT_WITHIN_ANCHOR_2_SIGMA |
| A4 | LVD | +3.00e-07 +/- 3.30e-06 | 0.09 sigma | AGREEMENT_WITHIN_ANCHOR_1_SIGMA |

## Honest-Negative Rejection Proof (Pillar 4)

| Row | Class | Experiment | Declared gate | Actual gate | Label |
|---|---|---|---|---|---|
| HN1 | CLASS_A | OPERA (2011 original, WITHDRAWN) | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN2 | CLASS_B | Fermilab synthetic Tevatron-coded | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN3 | CLASS_E | Fermi-LAT GRB 090510 | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY |

## What This Test Means

```text
SAM's c_SW = c commitment is consistent with CERN-class bounds at
2-sigma only for one or more live anchors. The closure is weaker
than 1-sigma identity. Recorded honestly without changing SAM's
commitment.

Stronger bounds exist OUTSIDE the 13 branch scope:
  Fermi-LAT GRB 090510 (Vasileiou et al. 2013):     1e-15 precision
  IceCube neutrino LIV constraints:                  1e-18 precision
These are not CERN; they were excluded from live anchors at Gate A.
A future 14_FOUNDATIONAL_TESTS branch could admit them as live anchors.
```

## How Progress On GATE_2 Is Tracked

```text
CR101a appeal rows record:
  - new CERN-class measurements at tighter precision
  - non-CERN measurements admitted in a future 14_ branch
  - any future result that disfavors c_SW = c

Original CR101 verdict is NEVER modified.
Original CR100 GATE_2 enumeration is NEVER modified.
```

## What CR101 Does Not Claim

- definitive closure of GATE_2 (would require lab measurement of substrate propagation speed)
- c_SW = c to better than CERN precision (astrophysical bounds reach 1e-15 - 1e-18 but are outside the 13 branch scope)
- exclusion of GATE_2 candidates (b) or (c) - they remain in the CR100 sealed enumeration
- any modification of CR100's sealed open-gate list - CR101 is a probe, not a rewrite

## Rule-9 Line

```text
This CR could have falsified SAM's GATE_2 candidate #1 if any of
the four live CERN-class neutrino time-of-flight measurements had
reported (v_v - c)/c at >= 3-sigma after the corrected 2012 analyses.

This is the first foundation stone. If c_SW = c holds at CERN
precision, the partition algebra inherits c as the propagation
constant, the standing-echo reading of particles inherits c, and
the action-phase identity in 11_QM_AND_GRAVITY inherits c.
If we build from the ground up, this is the ground.
```
