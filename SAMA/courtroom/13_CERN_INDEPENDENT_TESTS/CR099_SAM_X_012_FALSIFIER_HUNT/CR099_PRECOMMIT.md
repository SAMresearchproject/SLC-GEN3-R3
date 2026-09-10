# CR099 SAM_X_012_FALSIFIER_HUNT

## Test Class

```text
FORWARD_BLIND_FALSIFIER_HUNT_FOR_NEGATIVE_PREDICTION_SAM_X_012
```

## Preflight

```text
CR098 sealed 24 forward-blind SAM predictions. One of them (SAM-X-012)
is qualitatively different from the other 23: it is a NEGATIVE
prediction. SAM commits, on the record, that no particle exists at
partition (7,5) because both parts sit on radix walls {5,7,10,11}
that are not in the partition algebra {alpha_H^i * D^j : product <= R}
= {1, 2, 3, 4, 6, 8, 9, 12}.

A negative prediction is the strongest kind of test because it has a
clean falsifier: find one and SAM is broken. The point of this CR is
to make the falsifier as concrete as possible so an experimentalist
(at MoEDAL, CMS, LHCb, or ATLAS) can know what to look for.

This is a hunt to break SAM. If we find a (7,5)-shape particle, the
partition-algebra commitment in PR section 2.4 falls, the 09a
verdict's structural foundation is at risk, and SAM goes back to the
shop for repair. That outcome is fine - the whole point of the
courtroom is to make failure visible, not to hide it.
```

## Question

Given SAM-X-012's structural prediction (partition (7,5) is FORBIDDEN
in the partition algebra), what would a (7,5)-shape particle look
like to a CERN detector, and which CERN program is best positioned
to find or exclude it?

## Decoded Falsifier Signature

```text
Charge candidate set (from partition algebra extrapolation):
  Q in { -7/12, -5/12, +5/12, +7/12, -1/6, +1/6 }
  numerically: Q in { -0.5833, -0.4167, +0.4167, +0.5833, -0.1667, +0.1667 }

  These are NON-SM rational charges. The SM rational-charge set is
  {0, +/-1/3, +/-2/3, +/-1}. SAM-X-006 and SAM-X-007 already extend
  this to -2/3-with-negative-winding and -3/4. SAM-X-012's would-be
  charges sit OUTSIDE both sets.

Mass range candidate:
  ~1 MeV to ~few GeV
  Reason: SAM-X-006 ((8,4) layered, a=4 PROPAGATION default) is
  1.025 MeV, SAM-X-007 ((9,3)) is 1.537 MeV, SAM-X-008 ((6,4,2)) is
  228 MeV. A (7,5) at the same a=4 PROPAGATION default would land
  somewhere in this bracket. Without a layered-set lift assigned
  (the partition is forbidden), the exact mass is not derivable -
  but the search band is structurally bounded.

Spin / quantum number expectation:
  half-integer winding plausible (SAM-X-006 and -007 both
  alpha_H_half spin); but spin is not the load-bearing signature.
  Charge plus mass is enough to falsify.
```

## Primary CERN Probe

```text
MoEDAL (Monopole and Exotics Detector at the LHC)
Location: LHC Interaction Point 8 (shared cavern with LHCb)
Run: Run 1 + Run 2 + Run 3 (ongoing as of 2026)
Sensitivity: any non-SM electric charge via (Z/beta)^2 ionization
              signature in Nuclear Track Detectors (NTDs)

Published MoEDAL searches relevant to SAM-X-012:
  - magnetic monopole searches (Run-1 + Run-2)
  - milli-charged particle search
  - fractionally charged particle limits at Q=1/3, 2/3

What MoEDAL has NOT yet published (as of CR099 commitment utc):
  - dedicated limit at Q = +/- 7/12 (~0.58)
  - dedicated limit at Q = +/- 5/12 (~0.42)
  - dedicated limit at Q = +/- 1/6 (~0.17)
  - across the 1 MeV - few GeV mass range

That gap is exactly where SAM-X-012 lives. A MoEDAL re-analysis of
existing Run-1+Run-2 NTD data at the specific (Q, M) coordinates
above would constitute a real falsifier test.
```

## Secondary CERN Probes

```text
CMS / ATLAS heavy stable charged particle (HSCP) searches:
  Sensitivity: charges Q != 1 with anomalous dE/dx signature
  Mass reach: typically tens of GeV and above for HSCP class;
              SAM-X-012's expected mass (1 MeV - few GeV) is below
              the standard HSCP analysis threshold but could be
              probed by dedicated low-mass extensions.

LHCb fractional-charge tracking:
  Sensitivity: charge anomalies in dE/dx in the VELO + IT trackers
  Mass reach: GeV-scale exotic states
  Has reported limits on doubly-charged scalar bosons; not yet at
  the specific Q = +/- 5/12 or 7/12 wedge.

MoEDAL-MAPP (extension for Run-3):
  Adds scintillator + active calorimeter; sensitivity extends to
  longer-lived neutral and charged exotics. Currently commissioning.
  This is the strongest near-term probe of SAM-X-012's mass band.
```

## Falsifier Criteria

```text
SAM-X-012 is FALSIFIED if a CERN experiment publishes (with full
analysis chain and citation) a particle observation with:

  CRITERION A   - charge Q in { -7/12, -5/12, +5/12, +7/12, -1/6, +1/6 }
                  AT measurement-level precision, AND
  CRITERION B   - mass M in [1 MeV, ~10 GeV] band, AND
  CRITERION C   - identified as a primary carrier (not a composite,
                  bound state, or threshold artefact)

If all three criteria are met, SAM-X-012 has been broken. CR099 will
record this on the appeal row, the residual will be 'SAM_BROKEN',
and SAM goes to the shop.

SAM-X-012 remains UNFALSIFIED if:
  - MoEDAL Run-3 / MoEDAL-MAPP completes data-taking and publishes
    NULL results at Q = +/- 7/12, +/- 5/12, +/- 1/6 in the 1 MeV -
    10 GeV mass range.
  - Or no CERN experiment ever publishes a candidate observation
    matching all three criteria.

Either outcome (falsification OR continued null result) is
informative. CR099 records the result honestly when it comes.
```

## Pass Conditions (Sealing Completion)

CR099 is complete when:

- `CR099_falsifier_signature.json` is written and sealed with sha256.
- `CR099_falsifier_signature.json.sha256.txt` sibling exists.
- `CR099_predictions.csv` carries the candidate-charge set and the
  expected mass band as the prediction commitment.
- `CR099_prediction_commit.json` records the sha256 and utc.
- `CR099_summary.json` and `CR099_result.md` are written and cite
  BLINDNESS_PROTOCOL.md.

The runner does NOT compute residuals because there is no CERN
measurement to compare against today. The cryptographic seal IS
the test - it locks the falsifier criteria so that any future CERN
observation can be checked against the pre-committed signature.

## Wrong Controls (Discipline Checks)

- A change to the candidate charge set after seal is a protocol
  violation.
- A change to the expected mass band after seal is a protocol
  violation.
- Reframing the criteria after CERN publishes (motivated cherry-
  picking) is a protocol violation.

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could have falsified the 13-branch falsifier-hunt discipline
if the (7,5) partition were decoded into observables that do not
match SAM's own algebra, if the candidate charge set were padded
to be unfalsifiable, if the mass band were widened to swallow any
result, or if no CERN program were identified as the probe.

When CERN publishes a result matching the sealed criteria, CR099
will record SAM_X_012_FALSIFIED. When CERN publishes a null result
covering the band, CR099 will record SAM_X_012_HOLDS_UNDER_NEGATIVE_CONFIRMATION.
Either way it is on the public record, with the commitment timestamp
proving SAM committed first.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF - falsifier signature
will be sealed by the runner at execution time.
```
