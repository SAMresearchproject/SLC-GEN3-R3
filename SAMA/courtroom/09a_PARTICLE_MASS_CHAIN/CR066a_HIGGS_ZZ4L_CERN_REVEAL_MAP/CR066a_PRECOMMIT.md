# CR066a HIGGS_ZZ4L_CERN_REVEAL_MAP

## Test Class

```text
COURTROOM_CERN_REVEAL_OF_QP091_FROZEN_H_TO_ZZSTAR_4L_PREDICTIONS
opens three reveal targets carefully; explicitly holds signal strength
```

## Preflight

```text
CR065a intaken the QP084 -> QP091 frozen prediction set with zero
free parameters and no external CERN decay data opened.  CR065a is
locked at sha256 + utc.

CR066a opens the QP091 reveal map AT THE THREE STRONGEST TARGETS
ONLY:

  REVEAL_02  m4l distribution / Higgs mass reconstruction
             -> tests visible parent closure at the peak
  REVEAL_03  m12/m34 or Z/Z* branch distributions
             -> tests native off-shell ceiling
  REVEAL_04  four-lepton angular correlations
             -> tests structured hidden-bounce/orientation handle

The fourth reveal target is intentionally NOT opened:

  REVEAL_01  H006/H007 signal strength    HELD_NOT_OPENED_IN_CR066a

User direction (verbatim, in conversation 2026-06-14):
  "The best target is not just signal strength, it is m4l, m12/m34
   or Z/Z* branch distributions, and four-lepton angular correlations."

Signal strength rate is a single number that hides the structural
information SAM's freeze actually predicts.  Structural distributions
expose whether QP091's freeze closes properly or not.
```

## What CR066a Compares

For each reveal target:

```text
m4l peak
  SAM prediction:  H_visible_parent_ledger = 125219.0 MeV
  Anchor set:      ATLAS Run-2 H -> ZZ* -> 4l m_H measurement
                   CMS  Run-2 H -> ZZ* -> 4l m_H measurement
                   ATLAS+CMS Run-1 combination
  Test:            Is SAM's 125.219 GeV inside the per-experiment
                   1-sigma envelope?

m12 / m34 split
  SAM prediction:  one on-shell Z (m_Z visible = 91.1615 GeV)
                   plus one off-shell Z* with ceiling = 34.0575 GeV
                   two on-shell Z forbidden (deficit 57.104 GeV)
  Anchor set:      ATLAS H -> 4l m12/m34 dual-mass distribution
                   CMS H -> 4l m12/m34 dual-mass distribution
  Test:            Is m_12 peak near 91 GeV?
                   Is m_34 spectrum bounded above by ~34 GeV?
                   Are double-on-shell events absent below 182 GeV?

Four-lepton angular
  SAM prediction:  angles carry STRUCTURED branch / orientation
                   information; hidden bounce is NOT random missing
                   energy.  (qualitative at QP091; QP093+ will emit
                   quantitative angular distributions)
  Anchor set:      ATLAS H -> 4l angular analyses (Run-1 + Run-2)
                   CMS H -> 4l angular / spin-parity analyses
  Test:            Are observed angles non-flat and consistent with
                   a structured (non-random-missing-energy) source?
                   This is a STRUCTURAL CONSISTENCY check; the
                   QUANTITATIVE angular prediction is downstream
                   work that CR066a does not pre-empt.
```

## Pass Conditions

```text
P1  m4l peak: SAM 125.219 GeV inside the 1-sigma band of at least
    two of the three live anchors (ATLAS, CMS, combined)
P2  m12 peak at the Z visible mass: SAM 91.16 GeV inside the live
    anchor central-value band within sigma
P3  m34 ceiling: SAM 34.06 GeV consistent with the published m34
    endpoint within experimental resolution (~ few GeV)
P4  no on-shell Z+Z events observed below 182 GeV (trivially true
    kinematically; recorded as forbidden-row PASS)
P5  four-lepton angular distributions are not flat (structural-
    consistency only at this CR; quantitative comparison deferred)
P6  REVEAL_01 (signal strength) explicitly held NOT_OPENED
P7  no free parameters introduced in the comparison
```

## Wrong Controls

```text
WC1  CDF-like Tevatron 4l search must fail admissibility
     (Tevatron not the LHC H -> ZZ* -> 4l target)
WC2  unpublished claim without journal reference must fail
     admissibility
WC3  synthetic perturbation of the m_H value by 5 sigma must fail
     the m4l peak test (resolution proof)
WC4  signal strength rate fold-in must remain explicitly NOT used
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
