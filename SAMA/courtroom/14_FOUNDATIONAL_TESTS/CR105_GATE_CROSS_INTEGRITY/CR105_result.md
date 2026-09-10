# CR105 Gate-Cross Integrity - Result

## Verdict

```text
CR105_GATE_CROSS_INTEGRITY_PASS (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## SAM Joint Commitment (Locked Before Anchor Open)

```text
GATE_2:  c_SW = c           (locally for A < 11/12)
GATE_3:  K(A_H) self-correct (K * r_bounce * m = const, A < 11/12)

Joint deviation from (SR + EP) = 0 for A < 11/12
Free parameters: 0
Upstream CR102 envelope sha256: 594f7e88d5d00c8974eca72ce29264084a4f5cb8a4f4aceb1f391ac456358029
Upstream CR104 envelope sha256: 91d425b692d9477af5b1c98dbb5893d178758376adc5a40a5d38757eb8fb6d9d
```

## Blindness Proof

```text
prediction_commit_sha256 = 93b3a2b55af5ae59b06d7e5838902cd4914366ff619941994365b8b00607fba4
prediction_commit_utc    = 2026-06-13T23:11:59Z
anchor_envelope_sha256   = dabdc50b4d78347fe80c9c5df55195dd4d9e88ffdff55e02c3533208655f3f85
anchor_envelope_open_utc = 2026-06-13T23:11:59Z
temporal_ordering        = OK
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## Joint Anchors (Each Tests BOTH Gates Simultaneously)

| Row | Experiment | A | Sigma | Label |
|---|---|---|---|---|
| J1 | Al+ optical clock NIST 2010 | 1e-15 | 0.00 | JOINT_AGREEMENT_WITHIN_1_SIGMA |
| J2 | LIGO+Virgo+Fermi GW170817 | 1e-03 | 0.00 | JOINT_AGREEMENT_WITHIN_1_SIGMA |
| J3 | PSR B1913+16 Hulse-Taylor | 4e-01 | 0.00 | JOINT_AGREEMENT_WITHIN_1_SIGMA |
| J4 | PSR J0740+6620 NICER | 4e-01 | 0.00 | JOINT_AGREEMENT_WITHIN_1_SIGMA |

## Honest Negatives

| Row | Class | Anchor | Declared | Actual | Label |
|---|---|---|---|---|---|
| HN1 | CLASS_A | Withdrawn joint EP+SR claim | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN2 | CLASS_X_UNPUBLISHED | Unpublished joint claim | GATE_A_ADMISSIBILITY | GATE_A_ADMISSIBILITY | REJECTED_AT_GATE_A_ADMISSIBILITY |
| HN3 | CLASS_G | LIGO+Virgo+Fermi (synthetic CLASS_G perturbation) | GATE_R_RESIDUAL | GATE_R_RESIDUAL | REJECTED_AT_GATE_R_RESIDUAL |

Correctly gated: 3/3

## What This Test Means

```text
Both partial closures (GATE_2 c_SW = c at 1e-18; GATE_3 K(A_H)
self-correction at 1e-19) hold simultaneously in every joint
anchor. The two gates form a coherent substrate-foundation
reading in the regime A < 11/12.

Joint anchors span:
  Al+ optical clock (A ~ 1e-15) - low gravity precision floor
  GW170817 (A ~ 1e-3) - cosmological photon+gravity propagation
  PSR B1913+16 (A ~ 0.4) - NS binary GW emission
  PSR J0740+6620 NICER (A ~ 0.42) - NS surface rest mass

No contradiction detected. CR102 and CR104 verdicts interlock.
```

## Rule-9 Line

```text
This CR could have flagged contradiction between SAM's two partial
closures if any joint anchor showed measurements one gate would
predict differently from the other. None did. The two gates form a
coherent substrate-foundation reading at A < 11/12.
```
