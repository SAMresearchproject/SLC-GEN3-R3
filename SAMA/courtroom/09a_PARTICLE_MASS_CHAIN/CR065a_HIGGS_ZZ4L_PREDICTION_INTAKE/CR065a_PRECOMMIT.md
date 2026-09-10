# CR065a HIGGS_ZZ4L_PREDICTION_INTAKE

## Test Class

```text
COURTROOM_INTAKE_OF_QP084_THROUGH_QP091_FORWARD_FROZEN_PREDICTIONS
no external CERN decay data opened in this CR
```

## Preflight

```text
Upstream quantum_phase has completed the QP084 -> QP091 chain
(8 sequential FORWARD passes), producing a frozen prediction freeze
for the Higgs H -> ZZ* -> 4l channel with zero free parameters
introduced anywhere in the chain.

CR065a brings the FROZEN predictions into the Courtroom 09a branch
as a continuation of the 35-row particle mass chain export.  It
does NOT open the CERN reveal targets (m4l distribution, m12/m34,
four-lepton angles) - that is the role of CR066a.

Held downstream anchors in QP090/QP091: H006 and H007 (the H -> ZZ*
signal strengths from CR098 forward-blind registry).  These are
explicitly NOT targeted in CR065a or CR066a; QP091 already
acknowledged that signal strength is the weakest of the four
candidate reveals.  The strongest three (m4l, m12/m34, angular) are
the CR066a target list.
```

## Question

Does the upstream QP084 -> QP091 chain provide a self-consistent,
zero-free-parameter, target-blind freeze for the H -> ZZ* -> 4l
observable set ready for CERN reveal?

## Pass Conditions

```text
P1  QP084 through QP091 each report passed=true in their summary.json
P2  every QP test in the chain reports free_parameters_introduced=0
P3  every QP test in the chain reports external_decay_data_used=false
    (or external_reference_used=false for the pre-QP085 lift selector)
P4  QP091 frozen observables present and reproducible:
      H_visible_parent_ledger_MeV     = 125219.0
      H_source_hidden_budget_MeV       = 125419.11694535677
      Z_visible_branch_MeV             = 91161.5
      two_on_shell_Z_deficit_visible   = 57104.0 MeV (forbidden)
      Zstar_ceiling_visible            = 34057.5 MeV
      4l thresholds                    = 4e 2.044, 2e2mu 212.4, 4mu 422.7 MeV
      hidden_source_budget_fraction     = 0.001595... (0.16%)
P5  the QP091 reveal map (qp092 reveal map) names the four reveal
    targets, with three flagged HELD_NOT_OPENED:
      REVEAL_02 m4l distribution
      REVEAL_03 m12/m34 or Z/Z* branch distributions
      REVEAL_04 four-lepton angular correlations
    plus the held signal strength (REVEAL_01) recorded but NOT targeted
P6  no external CERN four-lepton measurement is opened in this CR
```

## Wrong Controls

```text
WC1  any QP in the chain with passed=false aborts the intake
WC2  any QP with free_parameters_introduced > 0 fails P2
WC3  any QP that opened external decay/angular data before the QP091
     freeze (i.e. before the reveal map is opened) fails P3 and the
     chain loses target-blind status
WC4  any modification of the QP091 frozen predictions inside the
     Courtroom intake is a protocol violation
WC5  opening REVEAL_02/03/04 inside CR065a (rather than CR066a) is
     a scope violation
```

## Branch Continuation Rule

```text
09a current chain: CR059a -> CR060a -> CR061a -> CR062a -> CR063a
                    -> CR064a (branch verdict)
CR065a extends 09a: takes the upstream QP084-QP091 chain (which
                    extends QP075 with a structural H -> ZZ* -> 4l
                    derivation) and intakes the prediction freeze.
The 09a CR064a branch verdict remains immutable.  CR065a is a
continuation in the same 09a branch, citing CR064a as upstream
courtroom anchor.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
