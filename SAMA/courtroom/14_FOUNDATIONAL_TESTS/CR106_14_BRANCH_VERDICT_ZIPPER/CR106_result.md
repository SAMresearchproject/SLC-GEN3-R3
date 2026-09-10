# CR106 14 Branch Verdict Zipper - Result

## Verdict

```text
CR106_14_BRANCH_COMPLETE_FOUNDATIONAL_TESTS_PARTIAL_CLOSURE_BUNDLE (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## Branch Verdict Seal

```text
branch_verdict_sha256       = 09eb6ae0055ebe5e53db9c2dc3df205c0613c4af5671341b7d5b4e7e07aa0ea6
composite_summary_sha256    = dc053ec3bdc651706a0e5e69f730878225105b522c2c8194b02073d297b6b02b
sealed_at_utc               = 2026-06-13T23:13:53Z
blindness_protocol_sha256   = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## Ladder Verdicts

| CR | Status | Verdict |
|---|---|---|
| CR102 | CLEAN | PARTIAL_CLOSURE_C_SW_EQUALS_C_CONSISTENT_AT_ASTROPHYSICAL_PRECISION |
| CR103 | CLEAN | CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC |
| CR103a | CLEAN | BOUNCE_COST_A_DEPENDENCE_STRUCTURAL_INSIGHT_LOCKED |
| CR104 | CLEAN | PARTIAL_CLOSURE_K_A_H_CONSISTENT_AT_TESTED_A_RANGE_11_OVER_12_FORWARD_BLIND |
| CR105 | CLEAN | GATE_CROSS_INTEGRITY_PASS |

## Strongest Export Claim

See `CR106_14_branch_strongest_claim.md`.

## Open Debts At Zipper Time

```text
- BLINDNESS_PROTOCOL sha256 sibling pending curator sign-off
- 14 branch seal sha256 sibling pending curator sign-off
- anchor citation_verification_status PENDING across all CRs in the branch
- GATE_1 N_SW functional remains open at structural level pending upstream SAM derivation
- 11/12 spaghettification onset forward-blind unprobed by current data
- CR103b test of corrected GATE_1 structure pending upstream derivation
```

## Rule-9 Reminder

```text
This branch verdict zipper does NOT modify any prior CR result.
All five prior 14-branch CRs are sealed and immutable. The branch
verdict is the export claim that survives the sum of those CRs
plus the companion CR101 in branch 13.

Honest scope is preserved: the partial closures demonstrate
consistency with mainstream physics in tested regimes, not
unique SAM verification. The structural lock (CR103a) provides
the corrected reading; the GATE_1 simplest-reading failure (CR103)
remains on record as the most honest sharp result.
```
