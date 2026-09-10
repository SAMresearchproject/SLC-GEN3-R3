# CR064 Particle Mass Chain Branch Verdict (Zipper) - Precommit

```text
document_id:    CR064_PRECOMMIT
branch:         09_PARTICLE_MASS_CHAIN
cr_slot:        CR064
sealed_before:  CR064 runner exists and CR064 result exists
seal_anchor:    SEALED_PARTICLE_MASS_CHAIN_SCOPE_APPROACH_2026_06_13
                (sha256: ab7cdebb8a2c56f98a1e242967b30fbb05d1fb4ec40719061e779608e87e50c8)
manifest:       09_PARTICLE_MASS_CHAIN/SOURCE_MANIFEST.csv  (sha256 d605d070...)
date_local:     2026-06-13
```

## Rule

```text
This CR is a zipper, not a new physics test.  It reads CR059-CR063
results and emits:
  1. branch-level verdict aggregating the chain
  2. deferred-support appeal upgrades for CR059 + CR060 (BOUNDARY ->
     APPEAL_PASS based on downstream CR061+CR062+CR063 contact)
  3. strongest export claim for SAMs_TOE / new repo
CR064 does NOT modify any earlier CR result file.  Original BOUNDARY
records remain immutable; appeals are recorded in CR064's own outputs.
```

## Question

```text
Given CR059 (BOUNDARY), CR060 (BOUNDARY), CR061 (PASS_SCOPED_STRUCTURAL),
CR062 (PASS_SCOPED_K1_ROW_LEVEL), CR063 (PASS_HONEST_NEGATIVES_REJECT),
what is the 09 branch verdict and what deferred-support upgrades
are permitted for CR059 and CR060?
```

## Declared Premises

```text
P1. Chain of prior CR results (read-only):
      CR059 BOUNDARY  (particle engine input boundary verified clean)
      CR060 BOUNDARY  (selector provenance + forbidden targets clean)
      CR061 PASS_SCOPED_STRUCTURAL  (mass chain reproduction verified)
      CR062 PASS_SCOPED_K1_ROW_LEVEL  (PDG 2024 row-by-row contact)
      CR063 PASS_HONEST_NEGATIVES_REJECT  (honest negatives validated)

P2. Anti-circularity rule (from 05 seal):
      Downstream tests may support upstream structure only if all are true:
        downstream declared upstream premise before running,
        downstream contains at least one external anchor,
        downstream has wrong controls that can fail the same external anchor,
        downstream result is locally artifacted and hashed,
        upstream grade is APPENDED, not overwritten.

P3. Allowed deferred-support upgrades:
      CR059 BOUNDARY -> APPEAL_PASS supported by CR061 + CR062 + CR063
      CR060 BOUNDARY -> APPEAL_PASS supported by CR061 + CR062 + CR063

P4. Original CR result files are IMMUTABLE.  CR064 records appeals in
    CR064_appeal_pass_ledger.csv, not by editing CR059 or CR060.

P5. Source manifest sealed by CR059 must still match.
```

## Outcome Taxonomy

```text
PASS_SCOPED_09_BRANCH_K1_VERIFIED:
  - CR061-CR063 all PASS-tier.
  - CR059 + CR060 deferred-support appeals recorded.
  - Manifest seal intact.

BOUNDARY_09_BRANCH:
  - One or more prior CRs at DIAGNOSTIC.

FAIL_09_BRANCH:
  - CR062 FAIL (K1 anchor violation) or CR063 FAIL_RETROACTIVE.
  - Any forbidden language used (e.g., implying upstream CRs were
    independently proven by downstream).

DIAGNOSTIC:
  - A prior CR result file is missing or unreadable.
```

## Rule-9 Line

```text
This test could have falsified the claim that the 09 branch produces
a coherent PASS-tier chain ending in K1 PDG row-by-row contact, with
deferred-support appeals correctly applied to CR059 + CR060 per the
anti-circularity rule.
```

## Expected Artifacts

```text
CR064_PRECOMMIT.md
CR064_PARTICLE_MASS_CHAIN_BRANCH_VERDICT.py
CR064_input_manifest.csv
CR064_prior_cr_results_ledger.csv         (read-only roll-up)
CR064_appeal_pass_ledger.csv              (deferred-support upgrades)
CR064_branch_strongest_claim.md           (export claim text)
CR064_wrong_controls.csv
CR064_manifest_seal_check.json
CR064_summary.json
CR064_result.md
HASHES.txt
```

## Wrong Controls

```text
WC1: simulate CR062 verdict = FAIL_ROW_LEVEL -> CR064 must FAIL_09_BRANCH
WC2: simulate CR063 verdict = FAIL_RETROACTIVE -> CR064 must FAIL_09_BRANCH
WC3: simulate appeal language overwriting CR059 result -> forbidden,
     detection wired
WC4: corrupt manifest seal -> DIAGNOSTIC
WC5: simulate a missing prior CR summary -> DIAGNOSTIC
WC6: simulate forbidden language ("downstream proves upstream") -> detect
```

## Sealed Premise Set

```text
P1-P5 sealed at CR064_PRECOMMIT write time.
```
