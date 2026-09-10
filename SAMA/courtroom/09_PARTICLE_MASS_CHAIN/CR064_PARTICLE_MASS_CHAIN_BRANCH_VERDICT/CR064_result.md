# CR064 Particle Mass Chain Branch Verdict (Zipper)

## Verdict

```text
CR064_PASS_SCOPED_09_BRANCH_K1_VERIFIED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_SCOPED_09_BRANCH_K1_VERIFIED
triage_bin = A
```

## Reason

```text
CR061+CR062+CR063 all PASS-tier; CR059+CR060 deferred-support appeals recorded
```

## Prior CR Chain (Read-Only)

| CR | Role | Original Verdict |
|---|---|---|
| CR059 | input_boundary | BOUNDARY |
| CR060 | selector_provenance | BOUNDARY |
| CR061 | mass_chain_reproduction | PASS_SCOPED_STRUCTURAL |
| CR062 | k1_row_by_row_ledger | PASS_SCOPED_K1_ROW_LEVEL |
| CR063 | honest_negatives | PASS_HONEST_NEGATIVES_REJECT |

## Deferred-Support Appeal Ledger

Original CR result files are NOT modified.  Appeals recorded here:

| Upstream CR | Original | Appeal | Supporting CRs |
|---|---|---|---|
| CR059 | BOUNDARY | APPEAL_PASS_DEFERRED_SUPPORT | CR061;CR062;CR063 |
| CR060 | BOUNDARY | APPEAL_PASS_DEFERRED_SUPPORT | CR061;CR062;CR063 |


## Rule-9 Line

```text
This test could have falsified the claim that the 09 branch produces
a coherent PASS-tier chain ending in K1 PDG row-by-row contact, with
deferred-support appeals correctly applied to CR059 + CR060 per the
anti-circularity rule.
```

## Branch Strongest Export Claim

See `CR064_branch_strongest_claim.md`.

## Branch Status

```text
09_BRANCH_COMPLETE
```

## Artifacts

- `CR064_input_manifest.csv`
- `CR064_prior_cr_results_ledger.csv`
- `CR064_appeal_pass_ledger.csv`
- `CR064_branch_strongest_claim.md`
- `CR064_wrong_controls.csv`
- `CR064_manifest_seal_check.json`
- `CR064_summary.json`
- `HASHES.txt`
