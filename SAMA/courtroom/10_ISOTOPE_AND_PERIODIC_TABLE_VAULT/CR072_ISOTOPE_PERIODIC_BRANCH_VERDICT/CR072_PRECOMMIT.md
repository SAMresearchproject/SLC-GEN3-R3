# CR072 Isotope/Periodic Branch Verdict (Zipper) - Precommit

```text
document_id:    CR072_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR072
sealed_before:  CR072 runner exists and CR072 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv
                manifest sha256: cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
date_local:     2026-06-13
```

## Rule

```text
Zipper for the 10 branch.  Reads CR065-CR071 results and emits:
  1. branch-level verdict
  2. deferred-support appeal upgrade for CR066 (BOUNDARY -> APPEAL_PASS
     supported by CR067-CR070 downstream contact)
  3. strongest export claim for the new repo
  4. CR071 permanent record reference (the frontier seal is permanent
     regardless of this zipper)
CR072 does NOT modify any earlier CR result file.
```

## Question

```text
Given:
  CR065 PASS
  CR066 BOUNDARY
  CR067 PASS_SCOPED_STRUCTURAL
  CR068 PASS_SCOPED_STRUCTURAL
  CR069 PASS_SCOPED_K1_ROSTER_LEVEL
  CR070 PASS_ALL_THREE_SUB_LANES
  CR071 BOUNDARY_PRE_REGISTERED_PREDICTION (permanent)
what is the 10 branch verdict?
```

## Declared Premises

```text
P1. Prior CR chain (read-only).
P2. Anti-circularity rule (same as 05/CR064).
P3. Allowed appeal: CR066 BOUNDARY -> APPEAL_PASS supported by CR067+CR068+CR069+CR070.
P4. CR065 PASS does not need an appeal (already PASS).
P5. CR071 BOUNDARY_PRE_REGISTERED_PREDICTION is PERMANENT.  CR072 cites
    it but does NOT upgrade or alter it.  Future appeals through M3
    channel (APPEAL_FRONTIER_HIT / APPEAL_FRONTIER_MISS).
P6. Original CR result files immutable.  Appeals recorded in
    CR072_appeal_pass_ledger.csv.
P7. CR065 manifest seal intact.
```

## Outcome Taxonomy

```text
PASS_SCOPED_10_BRANCH_K1_VERIFIED_WITH_FRONTIER_SEAL:
  - CR065 PASS; CR067-CR070 all PASS-tier; CR071 sealed.
  - CR066 appeal recorded.
  - Manifest seal intact.

BOUNDARY_10_BRANCH:
  - One or more prior CRs at DIAGNOSTIC.

FAIL_10_BRANCH:
  - CR069 FAIL (K1 roster miss).
  - Per seal: CR069 Z=97..118 deferral does NOT count as FAIL.

DIAGNOSTIC:
  - Prior CR summary missing or unreadable.
```

## Rule-9 Line

```text
This test could have falsified the claim that the 10 branch produces
a coherent PASS-tier chain ending in K1 IAEA roster contact (162/162
Z=1..96) plus a permanently-sealed Z=97..118 frontier prediction map.
```

## Expected Artifacts

```text
CR072_PRECOMMIT.md
CR072_ISOTOPE_PERIODIC_BRANCH_VERDICT.py
CR072_input_manifest.csv
CR072_prior_cr_results_ledger.csv
CR072_appeal_pass_ledger.csv
CR072_branch_strongest_claim.md
CR072_frontier_seal_reference.json    (cites CR071 permanent record)
CR072_wrong_controls.csv
CR072_manifest_seal_check.json
CR072_summary.json
CR072_result.md
HASHES.txt
```

## Wrong Controls

```text
WC1: simulate CR069 FAIL on Z=1..96 -> FAIL_10_BRANCH
WC2: simulate CR071 modification attempt -> forbidden, detection wired
WC3: simulate CR066 appeal overwriting original -> forbidden
WC4: corrupt manifest seal -> DIAGNOSTIC
WC5: simulate missing prior summary -> DIAGNOSTIC
WC6: simulate Z=97..118 deferral counted as FAIL -> forbidden interpretation
```

## Sealed Premise Set

```text
P1-P7 sealed at CR072_PRECOMMIT write time.
```
