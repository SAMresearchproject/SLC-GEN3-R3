# CR069 Observed Roster Comparison (K1 Anchor)

## Verdict

```text
CR069_PASS_SCOPED_K1_ROSTER_LEVEL_OBSERVED_ROSTER_COMPARISON
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_SCOPED_K1_ROSTER_LEVEL
triage_bin = A
```

## Headline Result

```text
Z = 1..96    :  162 / 162  exact ZNA matches  (rate = 1.0)
Z = 1..82    :  136 / 136  (lead-and-below band)
Z = 83..96   :   26 /  26  (actinide-contact band through curium)
Z = 97..118  :  0 / 38  (frontier band, deferred to CR071)

Per the seal: Z=97..118 is a STRUCTURED MISS BAND, not a scattered
failure.  It is recorded here but sealed at CR071 as a pre-registered
prediction map.
```

## Reason

```text
Z=1..96 = 162/162 (100%); Z=97..118 = 0/38 deferred to CR071; IAEA anchor sha 8aee5dc4... verified
```

## Phase Summary

```text
Phase 1 manifest seal + hash       verified=155
Phase 2 QP061 artifacts            hash_match=6/6
Phase 3 band partition             bands_extracted=5
Phase 4 Z=1..96 K1 PASS check      k1_pass=True
Phase 5 Z=97..118 deferred         deferred_to_cr071=True
Phase 6 element coverage           coverage_rate=0.8135593220338984
Phase 7 IAEA anchor roll-forward   status=iaea_anchor_verified
Phase 8 wrong controls             passed=6/6
```

## IAEA External Anchor

```text
authority    = IAEA LiveChart of Nuclides
endpoint     = https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=all
local sha256 = 8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
declared sha = 8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
status       = iaea_anchor_verified
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's sealed-hash-guarded
QP061 isotope prediction manifest contacts the IAEA LiveChart ground-
state roster exactly 162/162 times across Z=1..96, with 0/38 in the
Z=97..118 frontier band reserved as a structured miss to be sealed
at CR071.
```

## Artifacts

- `CR069_input_manifest.csv`
- `CR069_qp061_artifact_check.csv`
- `CR069_band_partition_verification.csv`
- `CR069_z_001_096_pass_summary.json`
- `CR069_z_097_118_deferred_summary.json`
- `CR069_element_coverage_check.json`
- `CR069_iaea_anchor_roll_forward.json`
- `CR069_wrong_controls.csv`
- `CR069_manifest_seal_check.json`
- `CR069_summary.json`
- `HASHES.txt`
