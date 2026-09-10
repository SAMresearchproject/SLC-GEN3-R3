# CR071 Superheavy Miss-Band Target Map

## PERMANENT Verdict (Never Overwritten)

```text
CR071_BOUNDARY_PRE_REGISTERED_PREDICTION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY_PRE_REGISTERED_PREDICTION
triage_bin = B
permanent_record = True
```

## What This CR Seals

```text
Z = 97..118 frontier band: 38 pre-registered ZNA rows
Source: qp068 high_z_neutron_rich_island_prediction_table.csv
Pre-registered: 2026-06-13 (before any post-2026-06-13 IAEA release)
Disclosure: external_data_used=false, free_parameters_introduced=0
```

## Reason

```text
Z=97..118 frontier band sealed: 22 qp068 island ZNA rows + 38 broader-band sealed rows; permanent verdict (never overwritten); appeals via M3 channel
```

## Phase Summary

```text
Phase 1 manifest seal + hash    verified=155
Phase 2 qp068 artifacts         5/5 hash_match
Phase 3 row count               island_rows=22  broader_band=38
Phase 4 qp068 disclosure        status=disclosure_clean
Phase 5 frontier map seal       sealed=True
Phase 6 wrong controls          passed=6/6
```

## Appeal Channel

The verdict CR071_BOUNDARY_PRE_REGISTERED_PREDICTION is PERMANENT.
Future IAEA observations in Z=97..118 enter via M3 appeal channel:

  APPEAL_FRONTIER_HIT  - predicted ZNA matches a new observation
  APPEAL_FRONTIER_MISS - new observation does not match any predicted ZNA

CR071 itself is never overwritten.  See
`CR071_appeal_channel_documentation.md` for invocation format.

## Rule-9 Line

```text
This test could have falsified the claim that SAM's Z=97..118 frontier
prediction is pre-registered, structured, hash-sealed before any
post-2026-06-13 IAEA observation, and consists of 38 specific ZNA
coordinates predicted from native structure rather than back-fit to
known absences.
```

## Artifacts

- `CR071_input_manifest.csv`
- `CR071_qp068_artifact_check.csv`
- `CR071_frontier_prediction_count_check.json`
- `CR071_pre_registered_frontier_map.json`     (SEALED PREDICTION RECORD)
- `CR071_pre_registered_frontier_map.sha256.txt`
- `CR071_appeal_channel_documentation.md`
- `CR071_wrong_controls.csv`
- `CR071_manifest_seal_check.json`
- `CR071_summary.json`
- `HASHES.txt`
