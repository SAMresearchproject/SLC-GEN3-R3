# CR106 14_BRANCH_VERDICT_ZIPPER

## Test Class

```text
BRANCH_VERDICT_ZIPPER_AND_STRONGEST_EXPORT_CLAIM
```

## Preflight

```text
CR106 is the 14 branch verdict zipper. It reads the prior CRs in this
branch (CR102, CR103, CR103a, CR104, CR105), confirms they exist as
CLEAN executions with sealed envelopes, and writes the branch's
strongest export claim into a single sha256-locked document.

CR106 does not re-run any prior CR. It checks that each prior CR has:

  - a sealed result file
  - a hashed predictions file (Pillar 2 procedural blindness applied)
  - a hashed anchor envelope (where applicable)
  - a final verdict in {PARTIAL_CLOSURE_*, DISFAVORED_*, INTEGRITY_PASS}
  - no protocol violations recorded

and then writes the branch verdict.
```

## Question

Read end-to-end, what does the 14 branch report? What is the
strongest export claim that survives every CR in the branch?

## Pass Conditions (Reporting Completion)

CR106 is complete when:

- each prior CR in the branch has its sha256 fields re-verified at
  zipper time
- the strongest export claim file is written
- the branch verdict file is written and sealed
- a single composite sha256 of all prior CR result files is recorded

## Possible Outcomes

```text
14_BRANCH_COMPLETE_FOUNDATIONAL_TESTS_PARTIAL_CLOSURE_BUNDLE
    every prior CR resolved with its declared verdict; no protocol
    violations; strongest claim exportable.

14_BRANCH_INCOMPLETE_OR_VIOLATION
    a prior CR is missing required artifacts or shows a protocol
    violation; zipper records the gap.
```

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at zipper time
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
