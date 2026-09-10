# CR098 CERN_GAPS_FORWARD_BLIND_PREDICTIONS

## Test Class

```text
FORWARD_BLIND_PREDICTION_REGISTRY_AGAINST_UNRESOLVED_CERN_GAPS
```

## Preflight

```text
This CR is qualitatively different from CR091..CR096.

CR091..CR096 compared 09a's locked predictions against CERN values
that were already public when 09a was sealed. That is rigorous as
audit but not forward-blind: both datasets existed before the
comparison.

CR098 commits SAM forward predictions for observables that CERN has
NOT YET PUBLISHED, sha256-locks them with a utc commitment timestamp,
and waits. When CERN publishes a measurement on any of the registered
gaps, an APPEAL_NEW_CERN_MEASUREMENT row updates the registry. The
sealed prediction is never modified.

The registry covers two upstream SAM frontier sources:

  closure_campaign03  SAM_UNKNOWN_NATIVE_PARTICLES
                      12 SAM-X candidates (SAM-X-001..SAM-X-012)
                      novel native-sector predictions with explicit
                      partition-algebra mass formulas

  SUK055              SAM_UNIFICATION_KERNEL_GATE composite lane
                      12 heavy q-anti-q pair mass coordinates
                      (b<->c, b<->d, b<->s, b<->t, b<->u, c<->d,
                       c<->s, c<->t, c<->u, d<->t, s<->t, t<->u)

The 12th SAM-X row (SAM-X-012) is a NEGATIVE forward prediction:
SAM says no particle exists at partition (7,5) because both parts
sit at radix walls {5, 7, 10, 11}. If a CERN search finds such a
state at that structural shape, SAM is broken.
```

## Question

For each forward-blind row in the registry, given SAM's locked
prediction and the named CERN experimental program, what happens
when CERN publishes a result that addresses the prediction?

This CR does not answer that question today. It locks the
prediction. The answer comes later, from CERN, on CERN's timeline.

## Pass Conditions (Sealing Completion)

CR098 is complete when:

- `CR098_forward_blind_prediction_registry.csv` exists with one row
  per candidate, all required fields populated.
- `CR098_forward_blind_prediction_registry.csv.sha256.txt` sibling
  exists and seals the registry.
- `CR098_predictions.csv` carries the raw upstream cite values from
  the two source files, hashed via `CR098_prediction_commit.json`.
- `CR098_summary.json` records: total candidates, candidates per
  source family, candidates per search-status class, the sha256
  registry seal hash, and the prediction commitment utc.
- `CR098_result.md` cites BLINDNESS_PROTOCOL.md and is structured
  as a forward-blind prediction registry, not as a comparison report.

## What CR098 Records Per Row

```text
candidate_id                          (SAM-X-001..012 or COMPOSITE-PAIR-<a>-<b>)
source_family                         (SAM_X | SUK055_COMPOSITE)
structural_reading                    (partition / a-slice / pair)
predicted_mass_MeV
predicted_charge_Q                    (rational; may be "undetermined")
mass_formula                          (m_P * A_0^x * alpha_em^y * lift / div)
why_not_in_SM                         (specific structural distinction)
upstream_source_file                  (citable SAM artifact path)
upstream_source_sha256                (PENDING until upstream sealed)
prediction_commit_sha256              (sha256 of CR098_predictions.csv)
prediction_commit_utc                 (commitment timestamp)
prediction_status                     (FORWARD_BLIND_UNMEASURED |
                                       FORWARD_BLIND_SEARCH_ACTIVE |
                                       FORWARD_BLIND_NO_SEARCH_DEFINED |
                                       FORBIDDEN_PARTITION_NEGATIVE_PREDICTION)
suggested_CERN_search_program         (best-fit experimental program;
                                       may be empty for low-energy
                                       candidates where no CERN program
                                       currently covers the band)
mass_band_in_search_program           (what mass / energy range the
                                       suggested program already covers)
appeal_row_added_when_published       (NOT_YET; placeholder for
                                       APPEAL_NEW_CERN_MEASUREMENT)
```

## Wrong Controls (Discipline Checks)

- A registry row missing `mass_formula` falls to DIAGNOSTIC.
- A registry row missing `prediction_commit_sha256` or
  `prediction_commit_utc` falls to DIAGNOSTIC.
- An attempt to modify any candidate's predicted_mass_MeV after the
  registry sha256 sibling is written is a protocol violation.
- A "search program" claim must be either a real CERN program
  (ATLAS / CMS / LHCb / ALICE / MoEDAL / FASER / FASERnu / SND@LHC /
  NA62 / NA64 / OSQAR / IAXO etc.) or explicitly "NO_CURRENT_CERN_PROGRAM"
  for candidates outside CERN-accessible bands.

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

The procedural blindness here is asymmetric to CR091..CR096: the
"anchor envelope" doesn't exist yet because CERN hasn't published.
The prediction commit hash and the utc timestamp ARE the blindness
proof - they are the cryptographic record that SAM committed BEFORE
CERN published, and the registry sha256 sibling locks the commitment.

## Rule-9 Line

```text
This CR could have falsified the 13-branch forward-blind discipline
if SAM had no upstream-cited numeric predictions for the candidates,
if the registry was sealed without a sha256 sibling, if any candidate
row was modified after seal, or if a CERN measurement was loaded into
the registry on the prediction side instead of on a later appeal row.

CR098 puts SAM on the line for predictions CERN has not made yet.
That is the whole point.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
- BLINDNESS_PROTOCOL sha256 sibling: NOT YET WRITTEN
- Seal sha256 sibling: NOT YET WRITTEN
- Registry sha256 sibling: WRITTEN BY RUNNER AT EXECUTION TIME
- Upstream source sha256 fields: PENDING_PRECOMMIT_VERIFICATION
```
