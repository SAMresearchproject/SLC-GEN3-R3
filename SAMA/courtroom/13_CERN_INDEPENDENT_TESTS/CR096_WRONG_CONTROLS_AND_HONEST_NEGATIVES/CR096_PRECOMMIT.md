# CR096 WRONG_CONTROLS_AND_HONEST_NEGATIVES

## Test Class

```text
ADMISSIBILITY_AND_RESIDUAL_RESOLUTION_PROOF
(Gate A and Gate R per BLINDNESS_PROTOCOL Pillar 4)
```

## Preflight

```text
CR096 demonstrates that the 13 branch's two-gate honest-negative
discipline rejects wrong-controls on the correct mechanism:
  - Classes A-F: rejected at Gate A (admissibility) BEFORE residual
                 is computed, because the experiment is not on the
                 CERN allow-list or the row is withdrawn / PDG-average.
  - Class G:     synthetic perturbation passes admissibility (real
                 CERN experiment, real publication) but fails Gate R
                 because the central value is shifted to lie outside
                 the per-CR observation band.

This CR provides the resolution proof. It does NOT compute residuals
for classes A-F (admissibility rejects first). It records what the
residual WOULD have been as informational only.
```

## Anchor Rows Considered (provisional slice)

```text
HN001 CDF II W boson mass (CLASS_B Tevatron)         Gate A
HN005 PDG world-average W boson mass (CLASS_F)        Gate A
HN006 Withdrawn early-Run-1 ATLAS Higgs (CLASS_A)     Gate A
HN007 Perturbed CMS Higgs mass synthetic (CLASS_G)    Gate R
```

## Observation Band Used For Gate R (CLASS_G)

```text
Observable: Higgs boson mass
Per-CR band (CR092): 300 MeV
CLASS_G perturbation sizing: max(3 * band, 10 * stat, floor)
                            = max(900, 1400, 50) MeV = 1400 MeV
CLASS_G value:   125380 + 1400 = 126780 MeV
Expected: AGREEMENT_OUTSIDE_DECLARED_BAND (Gate R bites by design)
```

## CERN Allow-List

```text
admissible_experiments = { ATLAS, CMS, LHCb, ALICE, ALPHA, BASE, ASACUSA, AEgIS }
admissible_anchor_classes_LEP_legacy_CERN = { LEP combined (legacy CERN) }

NOT admissible (Gate A REJECTS):
  CDF, D0           (Tevatron / Fermilab)
  Belle, BaBar, Belle II  (B-factories / KEK / SLAC)
  Fermilab Muon g-2
  KamLAND, Super-Kamiokande, IceCube, Daya Bay  (non-CERN neutrino)
  PDG world average  (not an individual measurement)
  Withdrawn / superseded CERN measurement
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
