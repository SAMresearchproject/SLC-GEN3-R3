# CR102 GATE_2_C_SW_VS_C_ASTROPHYSICAL_CLOSURE

## Test Class

```text
ASTROPHYSICAL_PRECISION_PARTIAL_CLOSURE_OF_GATE_2
```

## Preflight

```text
CR101 (in 13) reported PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_
2_SIGMA_ONLY at CERN-class precision O(1e-6). Three of four CNGS-fed
neutrino time-of-flight measurements landed SAM's c_SW = c commitment
within 1 sigma; BOREXINO landed it at 1.42 sigma. The CERN-only
restriction was the binding constraint on the precision.

CR102 lifts the CERN restriction (14 branch admits any peer-reviewed
publication as a live anchor) and tests the same SAM commitment
c_SW = c against the strongest astrophysical bounds:

  - Fermi-LAT GRB 090510 photon-dispersion bound
  - IceCube astrophysical neutrino LIV bound
  - MAGIC PKS 1222+216 / Mrk 421 photon timing
  - HESS PKS 2155-304 photon timing
  - Crab pulsar TeV-gamma timing (HESS / MAGIC / VERITAS)

These bounds reach 1e-15 to 1e-18 precision - 9 to 12 orders of
magnitude tighter than CERN-class.

SAM's commitment is unchanged from CR101: c_SW = c (identity), the
simplest candidate from CR100's sealed open-gate enumeration. The
prediction is hashed and committed BEFORE the anchor envelope is
opened, exactly as in CR101.
```

## Question

Is SAM's locked commitment c_SW = c consistent with the strongest
published astrophysical bounds on photon and neutrino propagation
speed equaling c?

## SAM Commitment (Locked Before Anchor Open)

```text
GATE_2 candidate: c_SW = c (identity)
Expressed as testable prediction: (v_substrate - c) / c = 0
Free parameters introduced: 0
Upstream CR100 question lock sha256:
  fb310a23497308e9b0b92c23974cb08a230c7a8779c36aabd94feb628e145867
Identical commitment to CR101 (CERN-class run).
```

## Anchor Envelope Composition

```text
LIVE ANCHORS (peer-reviewed, used for residual test):

  A1  Fermi-LAT GRB 090510 photon-dispersion bound
      effective constraint: (v_g - c)/c at GRB-photon energies
      precision ~ 1e-15 (linear LIV, Vasileiou et al. 2013)
      arXiv:1305.3463 [VERIFY_PRECOMMIT]

  A2  IceCube astrophysical neutrino LIV bound
      effective constraint: (v_v - c)/c at TeV-PeV neutrino energies
      precision ~ 1e-18 (Amelino-Camelia et al. analyses; recent
      IceCube collaboration constraints)
      arXiv:1709.03434 [VERIFY_PRECOMMIT]

  A3  MAGIC PKS 1222+216 / Mrk 421 photon timing
      effective constraint: (v_g - c)/c at TeV-gamma energies
      precision ~ 1e-11
      arXiv:1106.1410 [VERIFY_PRECOMMIT]

  A4  HESS PKS 2155-304 photon timing
      effective constraint: (v_g - c)/c at TeV-gamma energies
      precision ~ 1e-11
      arXiv:1101.3650 [VERIFY_PRECOMMIT]

  A5  Crab pulsar TeV-gamma timing (HESS / MAGIC / VERITAS combined)
      effective constraint: (v_g - c)/c at TeV-gamma energies
      precision ~ 1e-12
      arXiv:1707.04249 [VERIFY_PRECOMMIT]

HONEST NEGATIVES (Pillar 4 discipline):

  HN1  OPERA 2011 original (CLASS_A withdrawn, fiber connector artefact)
       must be rejected at Gate A (withdrawn anchor class)
       arXiv:1109.4897 v1

  HN2  Hypothetical preprint claim without journal reference (CLASS_X
       unpublished/non-peer-reviewed)
       must be rejected at Gate A (unpublished anchor class)

  HN3  Synthetic CLASS_G perturbation (Fermi-LAT central value shifted
       by 3x its own precision)
       must be rejected at Gate R (residual outside band)
```

## Observation Bands

For each live anchor, the "uncertainty" is the published precision of
the bound on (v - c)/c. SAM's commitment of exactly 0 falls inside
this precision by construction unless the published bound's central
value (not its uncertainty) is non-zero.

In standard practice for these astrophysical bounds:

```text
- Fermi-LAT GRB 090510 reports a bound consistent with 0, with
  precision ~1e-15
- IceCube reports a bound consistent with 0, with precision ~1e-18
- MAGIC / HESS report bounds consistent with 0, precision ~1e-10 to 1e-11
- Crab timing reports a bound consistent with 0, precision ~1e-12
```

Each anchor row is labeled by sigma-distance of SAM's c_SW = c
commitment from the published central value (which is 0 for null
bounds, or non-zero if a deviation was detected).

## Pass Conditions (Reporting Completion)

CR102 is complete when:

- predictions, prediction_commit, envelope, evidence rows, summary,
  and result are written
- envelope sha256 sibling exists and matches at runner time
- temporal ordering: prediction_commit_utc precedes
  anchor_envelope_open_utc
- evidence rows carry blindness sha256 + utc fields
- honest-negative rows are rejected at their declared gate

## Possible Outcomes

```text
PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_ASTROPHYSICAL_PRECISION
    all five live anchors find SAM's 0 within their published 1-sigma
    band; the precision floor on c_SW = c is lifted to the tightest
    live anchor (~1e-18 from IceCube)

GATE_2_IDENTITY_DISFAVORED_AT_ASTROPHYSICAL_PRECISION
    any live anchor with central value >= 3 sigma from 0; SAM's c_SW = c
    challenged at astrophysical precision

PARTIAL_CLOSURE_AT_TIGHTER_THAN_CERN_BUT_NOT_TIGHTEST
    intermediate result; some live anchors pass at 1 sigma, others at
    2 sigma; the precision floor is improved from CERN's 1e-6 but not
    to the tightest available bound
```

## Wrong Controls (Discipline Checks)

- HN1 (OPERA 2011 withdrawn) must fail at Gate A admissibility BEFORE
  residual is computed
- HN2 (unpublished preprint) must fail at Gate A
- HN3 (synthetic CLASS_G perturbation) must fail at Gate R residual
- Temporal ordering violation -> DIAGNOSTIC

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could have disfavored SAM's GATE_2 candidate #1 at
astrophysical precision if any of the five live photon/neutrino LIV
bounds had reported a non-zero (v - c)/c at >= 3 sigma. None of them
has, to the precision of the cited publications.

If c_SW = c holds at IceCube precision of ~1e-18, the substrate
propagation constant is locked at c to 18 orders of magnitude. The
partition algebra carriers, the standing-echo particle reading, and
the action-phase identity all inherit this anchor at world-best
precision.

This is the ground stone. CR102's job is to test it at the strongest
available precision.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
