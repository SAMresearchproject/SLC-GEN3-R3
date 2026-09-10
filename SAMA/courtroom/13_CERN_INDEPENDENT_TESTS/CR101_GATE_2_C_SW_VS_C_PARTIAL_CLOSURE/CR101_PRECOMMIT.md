# CR101 GATE_2_C_SW_VS_C_PARTIAL_CLOSURE

## Test Class

```text
FIRST_GATE_PARTIAL_CLOSURE_TEST_AGAINST_CERN_CLASS_DATA
```

## Preflight

```text
CR100 sealed the SW open question and named three open gates:
  GATE_1 N_SW[u_H] functional
  GATE_2 c_SW relation to c
  GATE_3 K(A_H) substrate tension

CR101 is the first partial-closure attempt. It targets GATE_2.

SAM commits, sha256-sealed at runner time, to GATE_2 candidate #1:

      c_SW = c (identity)

This is the simplest candidate from the CR100 sealed enumeration. SAM
locks the commitment BEFORE the anchor envelope is opened, and the
runner then compares SAM's locked commitment against published CERN-
class bounds on substrate propagation speed = c.

This CR does NOT claim definitive GATE_2 closure. CERN's distance scale
(O(10) km between CNGS and Gran Sasso, O(km) at LHC) is intrinsically
weaker than astrophysical Lorentz-invariance tests (GRB photon
dispersion at Gpc distances reaches 1e-15 - 1e-18 precision). What
CR101 does is record, on the public sealed record, that SAM's c_SW = c
commitment is consistent with the strongest CERN-class data available.

If CERN later publishes a tighter bound (e.g., MoEDAL-MAPP timing,
LHCb forward physics dedicated analysis, or a CNGS-class successor),
an appeal row updates the bound.

If a future ATLAS / CMS / LHCb publication shows c_v != c at
measurement-level precision, GATE_2 candidate #1 is disfavored and
CR101a records the constraint.
```

## Question

Is SAM's locked commitment c_SW = c consistent with the strongest
published CERN-class bounds on substrate propagation speed equaling c?

## SAM Commitment (Locked Before Anchor Open)

```text
GATE_2 candidate selected: c_SW = c (identity)

Reading: in our 3D resolved ledger, light propagates at c; SW echoes
on the 2D boundary support propagate at the same speed; substrate
propagation speed equals the SR-relativistic limit.

This is the simplest of the three GATE_2 candidates enumerated in
CR100's sealed open-gate set:
  (a) c_SW = c                                              <- SELECTED
  (b) c_SW = c * dimensionless_substrate_factor             <- not selected
  (c) c_SW related to c via converter triad in A0 / R / D   <- not selected
```

## Anchor Envelope Composition (Locked At Curator Seal Time)

```text
LIVE ANCHORS (CERN-class, used for residual test):

  A1  ICARUS 2012 neutrino time-of-flight
      (v_v - c) / c = (0.4 +/- 2.8) x 10^-6 at ~17 GeV, 730 km
      arXiv:1208.2629 [VERIFY_PRECOMMIT]

  A2  OPERA 2012 corrected neutrino time-of-flight
      (v_v - c) / c = (2.7 +/- 3.1) x 10^-6 at ~17 GeV, 730 km
      arXiv:1212.1276 [VERIFY_PRECOMMIT]

  A3  BOREXINO 2012 neutrino time-of-flight (LNGS, CNGS-fed)
      (v_v - c) / c = (2.7 +/- 1.9) x 10^-6 at ~17 GeV, 730 km
      arXiv:1207.6860 [VERIFY_PRECOMMIT]

  A4  LVD 2012 neutrino time-of-flight (LNGS, CNGS-fed)
      (v_v - c) / c = (0.3 +/- 3.3) x 10^-6 at ~17 GeV, 730 km
      arXiv:1208.1392 [VERIFY_PRECOMMIT]

HONEST NEGATIVES (must be rejected at Gate A or Gate R):

  HN1  OPERA 2011 original neutrino time-of-flight (CLASS_A withdrawn)
       (v_v - c) / c = (2.48 +/- 0.28(stat) +/- 0.30(sys)) x 10^-5 at ~17 GeV
       arXiv:1109.4897 [VERIFY_PRECOMMIT]
       FIBER CONNECTOR ANOMALY identified 2012; result formally withdrawn
       Test: this row must be REJECTED at Gate A (withdrawn anchor class)

  HN2  Tevatron / Fermilab timing measurements miscoded as CERN
       Synthetic; tests Gate A rejection of non-CERN sources

  HN3  Astrophysical Fermi-LAT GRB 090510 photon-dispersion bound
       (Vasileiou et al., 2013) (v_g - c)/c < 10^-15 at GRB energies
       This is the STRONGEST bound available but is NOT CERN
       Test: this row must be REJECTED at Gate A (non-CERN source)
       Recorded as informational context, not as live anchor

CROSS-SOURCE CHECK (Pillar 3):
  ICARUS, OPERA-corrected, BOREXINO, and LVD are four INDEPENDENT
  CERN-fed measurements of the same observable. The SAM commitment
  (c_SW = c, i.e. (v_v - c)/c = 0) must be consistent with all four
  within their stated uncertainties.
```

## Observation Band

```text
The CR101 observation band is the QUADRATURE-COMBINED 1-sigma envelope
of the four live anchors at the time of seal:

  band_centered_on_zero_pm = max(
      |A1 mean| + 1*sigma_A1,
      |A2 mean| + 1*sigma_A2,
      |A3 mean| + 1*sigma_A3,
      |A4 mean| + 1*sigma_A4
  )

  numerically at seal: max(0.4+2.8, 2.7+3.1, 2.7+1.9, 0.3+3.3) x 10^-6
                     = 5.8 x 10^-6

  band = +/- 5.8 x 10^-6  (i.e., (v_v - c)/c within +/- 5.8e-6)

SAM's commitment c_SW = c <=> (v_v - c)/c = 0 falls strictly within
this band by construction. The test is whether each individual CERN
measurement places SAM's commitment inside its own quoted uncertainty
band.

Each live anchor's row label:
  AGREEMENT_WITHIN_ANCHOR_1_SIGMA      if |0 - mean| <= 1*sigma_combined
  AGREEMENT_WITHIN_ANCHOR_2_SIGMA      if |0 - mean| <= 2*sigma_combined
  AGREEMENT_OUTSIDE_ANCHOR_2_SIGMA     otherwise
```

## Pass Conditions (Reporting Completion)

CR101 is complete when:

- `CR101_predictions.csv` contains SAM's locked commitment c_SW = c
  expressed as the prediction (v_v - c)/c = 0 with zero free
  parameters.
- `CR101_prediction_commit.json` records sha256 + utc of the
  prediction file BEFORE envelope is opened.
- `CR101_cern_anchor_envelope.json` and sibling sha256 file lock the
  four live anchors and three honest-negative anchors.
- `CR101_evidence_rows.csv` carries one row per live anchor with
  blindness fields and the row label above; honest-negative rows
  carry the rejection gate.
- `CR101_summary.json` records per-anchor agreement, the cross-source
  status, and the partial-closure verdict.
- `CR101_result.md` cites BLINDNESS_PROTOCOL.md and CR100's GATE_2
  enumeration; the result is presented as PARTIAL closure, not
  definitive closure.

## Possible Outcomes

```text
PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_WITH_CERN_BOUNDS
    all four live anchors find (v_v - c)/c = 0 within their 1-sigma
    bands; the CERN-class precision floor on c_SW = c is locked at
    O(10^-6).

PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_2_SIGMA_ONLY
    if any anchor's mean shifts to 2-sigma; recorded honestly without
    SAM commitment change.

GATE_2_IDENTITY_DISFAVORED_BY_CERN_DATA
    if any live anchor measures (v_v - c)/c > 0 at >= 3-sigma; SAM's
    c_SW = c is challenged at CERN precision; reopen for candidate
    (b) or (c). CR100's open-gate enumeration is not modified;
    CR101 records the disfavoring result.

The outcome at seal time is determined by the cited anchor central
values and uncertainties as recorded in the envelope.
```

## Wrong Controls (Discipline Checks)

- HN1 OPERA 2011 original (CLASS_A withdrawn) must fail at Gate A
  admissibility (withdrawn anchor class) BEFORE residual is computed.
  If it passes admissibility, the runner emits a protocol violation.
- HN2 synthetic Tevatron-coded timing must fail at Gate A
  (experiment not on CERN allow-list).
- HN3 Fermi-LAT GRB bound is recorded as informational context but
  must fail Gate A as a CERN anchor (non-CERN source). It is the
  strongest bound on c_g = c but it is NOT a CERN result.
- Any evidence row missing `prediction_commit_sha256` or
  `anchor_envelope_sha256` falls to DIAGNOSTIC.

## Why This Could Build From The Ground Up

```text
GATE_2 partial closure at CERN precision (1e-6) is the first
foundation stone. If c_SW = c at this precision, then:

  - SR/QFT recovery on the substrate is structurally permitted
  - SW echoes propagating at c support the photon = standing-echo
    reading natively
  - 09a's particle ledger interpretation as pair-closed standing
    echoes inherits the c-propagation foundation
  - CR098's SAM-X candidates and SUK055 composite coordinates can
    use c as the propagation constant without ambiguity
  - The 11_QM_AND_GRAVITY action-phase identity (CR073) is
    dimensionally compatible with c_SW = c

If a stronger non-CERN bound (Fermi 1e-15, IceCube 1e-18) closes
GATE_2 more tightly in a future branch (14_FOUNDATIONAL_TESTS or
similar that allows non-CERN data), the foundation extends further.

CR101's job is to lay the first CERN-precision stone of this
foundation under blindness discipline.
```

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could have falsified SAM's GATE_2 candidate #1 if any of the
four live CERN-class neutrino time-of-flight measurements had
reported (v_v - c)/c > 0 at >= 3-sigma after the corrected 2012
analyses. They did not. SAM's c_SW = c commitment is consistent with
the CERN-class precision floor.

This CR does NOT falsify SAM's substrate primitive. It records a
partial-closure consistency on one of three GATE_2 candidates at
CERN-class precision. Astrophysical bounds remain the stronger probe
and live outside the 13 branch's CERN-restricted scope.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
