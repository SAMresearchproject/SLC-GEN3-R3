# CR091 PRECISION_ELECTROWEAK

## Test Class

```text
OBSERVATIONAL_COMPARISON_OF_LOCKED_09A_PREDICTIONS_AGAINST_CERN_PRECISION_EW_ANCHORS
```

## Preflight

```text
13 is observational. 09a's locked predictions for W boson mass, Z boson
mass, top quark mass, and sin^2 theta_W are read verbatim from
09a/CR062a_evidence_rows.csv and from the QP075 closure tables cited
through 09a. They are not modified, re-fit, or re-tuned. They are
compared to the CERN-published independent measurements drawn from
CR090_candidate_anchor_inventory.csv under the four-pillar blindness
protocol.

This precommit declares the per-row observation bands. Bands are
guidance for reporting, not gates that can falsify 09a. Per the
09a Immutability Rule, 09a stands regardless of where each residual
lands.
```

## Question

For the precision-electroweak observables (W mass, Z mass, top mass)
where 09a/QP075 emits a numeric prediction, how does that prediction
compare to each cited CERN-published independent measurement under
blindness discipline?

For observables (sin^2 theta_W effective leptonic, W width) where the
09a evidence row does not carry a direct numeric prediction and the
QP075 role operator is not visible to this CR at runner time, the
row is labeled INFORMATION_INSUFFICIENT_AT_THIS_CR and deferred.

## Anchor Rows Considered

```text
EW001 ATLAS  W boson mass
EW002 CMS    W boson mass
EW003 LHCb   W boson mass
EW004 LEP    Z boson mass (CERN host laboratory legacy)
EW007 ATLAS  top quark mass
EW008 CMS    top quark mass
EW009 ATLAS  sin^2 theta_W effective    INFORMATION_INSUFFICIENT_AT_THIS_CR
EW010 CMS    sin^2 theta_W effective    INFORMATION_INSUFFICIENT_AT_THIS_CR
EW011 LHCb   sin^2 theta_W effective    INFORMATION_INSUFFICIENT_AT_THIS_CR
EW005 ATLAS  W width                    INFORMATION_INSUFFICIENT_AT_THIS_CR
EW006 LEP    W width                    INFORMATION_INSUFFICIENT_AT_THIS_CR
```

## Observation Bands (Guidance, Not Gate)

Computed per BLINDNESS_PROTOCOL Observation-Band Guidance rule:
band >= max(inter-experiment disagreement, largest stat unc, largest sys unc)

```text
W boson mass         band = 25 MeV    (~0.031% of central; driven by LHCb sys 22 MeV
                                        and ATLAS-LHCb disagreement 12.5 MeV)
Z boson mass         band =  5 MeV    (~0.005% of central; single experiment LEP,
                                        2.1 MeV total unc; floor 5 MeV)
top quark mass       band = 1000 MeV  (~0.580% of central; driven by ATLAS-CMS
                                        disagreement 920 MeV)
Higgs is in CR092, not CR091.
```

Observation bands wider than the BLINDNESS_PROTOCOL guidance minimum
are permitted; narrower are flagged with the design-error note for the
curator. Bands are not adjusted to fit observed residuals.

## Pass Conditions (Reporting Completion, Not Pass/Fail Gate)

CR091 is complete when:

- `CR091_predictions.csv` exists and is hashed BEFORE the anchor envelope
  is opened.
- `CR091_prediction_commit.json` records the prediction file sha256 and
  the prediction_commit_utc timestamp.
- `CR091_cern_anchor_envelope.json` exists with sealed values, and the
  `CR091_cern_anchor_envelope.json.sha256.txt` sibling matches at
  runner time.
- `CR091_evidence_rows.csv` carries one row per anchor candidate with
  the schema fields named in BLINDNESS_PROTOCOL: row_id,
  observable_name, experiment, publication_reference,
  publication_date_utc, measurement_central_value, stat_uncertainty,
  sys_uncertainty, units, sam_prediction_value, sam_prediction_source,
  prediction_commit_sha256, prediction_commit_utc,
  anchor_envelope_sha256, anchor_envelope_open_utc, residual_value,
  residual_percent, observation_band_value, cross_source_status,
  row_label.
- `CR091_summary.json` records the per-band agreement counts and the
  observation-band values used.
- `CR091_result.md` cites BLINDNESS_PROTOCOL.md and reports the
  comparison as observational data, not as a verdict on 09a.

## Wrong Controls (Discipline Checks)

- Any evidence row where `prediction_commit_utc` does not precede
  `anchor_envelope_open_utc` falls to DIAGNOSTIC and emits
  `BLINDNESS_VIOLATION_DETECTED`.
- Any evidence row missing `prediction_commit_sha256` or
  `anchor_envelope_sha256` falls to DIAGNOSTIC.
- Any attempt to modify a 09a CR result file from within this runner
  is a protocol violation. The runner reads 09a files read-only.

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could have falsified the 13 branch plumbing - the procedural
blindness pipeline that hashes 09a predictions before opening any
CERN anchor envelope, and the reporting of per-row residuals as
observational data - if the runner opened the envelope before the
prediction commit was written, if any 09a prediction was modified,
or if any sha256 or utc field was missing from the evidence rows.

This CR does NOT falsify 09a. 09a's exemplary verdict is preserved
regardless of how the residuals land.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
- BLINDNESS_PROTOCOL sha256 sibling: NOT YET WRITTEN
- Seal sha256 sibling: NOT YET WRITTEN
- CR090 citation_verification_status: PENDING across all rows
- Anchor envelope citations: PENDING_PRECOMMIT_VERIFICATION
```

This CR091 draft demonstrates the procedure end-to-end and reports the
provisional comparison. It cannot claim sealed-scope verdict until the
curator promotes the seal sha256 sibling, the BLINDNESS_PROTOCOL sha256,
and the EW001..EW011 citation verification status.
