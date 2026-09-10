# CR072 Isotope/Periodic Branch Verdict (Zipper)

## Verdict

```text
CR072_PASS_SCOPED_10_BRANCH_K1_VERIFIED_WITH_FRONTIER_SEAL
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_SCOPED_10_BRANCH_K1_VERIFIED_WITH_FRONTIER_SEAL
triage_bin = A
```

## Reason

```text
CR067-CR070 all PASS-tier; CR065 PASS; CR071 BOUNDARY_PRE_REGISTERED_PREDICTION sealed permanent; CR066 deferred-support appeal recorded
```

## Prior CR Chain (Read-Only)

| CR | Role | Original Verdict |
|---|---|---|
| CR065 | vault_protocol_and_hash_chain | PASS |
| CR066 | allowed_inputs_and_forbidden_targets | BOUNDARY |
| CR067 | periodic_structure_derivation | PASS_SCOPED_STRUCTURAL |
| CR068 | isotope_manifest_reproduction | PASS_SCOPED_STRUCTURAL |
| CR069 | observed_roster_comparison_k1 | PASS_SCOPED_K1_ROSTER_LEVEL |
| CR070 | nulls_rarity_wrong_controls | PASS_ALL_THREE_SUB_LANES |
| CR071 | superheavy_miss_band_target_map_PERMANENT | BOUNDARY_PRE_REGISTERED_PREDICTION |

## Deferred-Support Appeal Ledger

Original CR result files are NOT modified.  Appeals recorded here:

| Upstream CR | Original | Appeal | Supporting CRs |
|---|---|---|---|
| CR066 | BOUNDARY | APPEAL_PASS_DEFERRED_SUPPORT | CR067;CR068;CR069;CR070 |


## CR071 Permanent Frontier Seal

```text
CR071 verdict   = BOUNDARY_PRE_REGISTERED_PREDICTION  (permanent)
sealed file     = CR071_pre_registered_frontier_map.json
sha256          = 636b4df597f80118c8da5e615aedeb95eb4f53cd1edf7e7ab2dac2b81a3bb626
modification    = FORBIDDEN_NEVER_OVERWRITTEN
appeal channel  = APPEAL_FRONTIER_HIT, APPEAL_FRONTIER_MISS
```

CR072 cites CR071's seal; CR072 does NOT modify it.

## Rule-9 Line

```text
This test could have falsified the claim that the 10 branch produces
a coherent PASS-tier chain ending in K1 IAEA roster contact (162/162
Z=1..96) plus a permanently-sealed Z=97..118 frontier prediction map.
```

## Branch Strongest Export Claim

See `CR072_branch_strongest_claim.md`.

## Branch Status

```text
10_BRANCH_COMPLETE
```

## Artifacts

- `CR072_input_manifest.csv`
- `CR072_prior_cr_results_ledger.csv`
- `CR072_appeal_pass_ledger.csv`
- `CR072_branch_strongest_claim.md`
- `CR072_frontier_seal_reference.json`
- `CR072_wrong_controls.csv`
- `CR072_manifest_seal_check.json`
- `CR072_summary.json`
- `HASHES.txt`
