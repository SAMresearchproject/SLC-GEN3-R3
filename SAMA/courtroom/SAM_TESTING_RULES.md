# SAM Testing Rules

## NEON RULE: No More Tests Of Tests Without Permission

Confirmation runs, double checks, audits, referee passes, hostile reviews,
red-team reviews, reruns whose purpose is to validate a prior result, and tests
whose main target is another test/result are strictly forbidden unless all of
the following happen before the run:

1. The run is explicitly named as a confirmation, double check, audit, referee
   pass, hostile review, red-team review, or result-validation run.
2. The reason for looking at old work is stated plainly.
3. The user explicitly grants permission for that confirmation/audit work.

Reason is not permission. Documentation is not permission. If the proposed run
is an audit, verification, retest, double check, rerun-to-validate, referee
pass, hostile review, red-team review, or any other test whose target is an old
test/result, the run must stop before execution and the user must be told that
classification.

Default rule:

```text
Do not test tests.
Do not test prior results.
Do not spend a gate asking whether the last gate was valid.
Use prior tests as inputs and build the next piece of machinery.
```

Multiple hostile audits have been done and will continue to be done under the direction of the user/developer Sean Brady. The roadmap is PROGRESS NOT AUDIT.

This rule exists because the existing test stack has already been double
checked and audited many times, including hostile review passes. Further work
should be constructive by default.

## What Counts As Progress

A new test or gate should produce at least one of the following:

```text
new equation
new coefficient
new operator
new selector that fills a blank
new numerical prediction
new falsifiable comparison
new artifact that directly advances a branch
```

## Allowed Without Special Permission

Using previous tests as evidence, inputs, frozen source rows, or branch context
is allowed. The boundary is purpose:

```text
Allowed: use prior result X to build new result Y.
Forbidden without permission: run a gate whose main purpose is to validate X.
```

## Required Pre-Run Declaration

Before running any new gate, complete the mandatory preflight in
`SAM_TEST_PREFLIGHT.md`.

Every proposed test must be classified as one of:

```text
CONSTRUCTIVE_NEW_WORK
CONFIRMATION_OR_AUDIT_REQUIRES_PERMISSION
```

If the second class applies, stop. Provide either:

```text
redirect = the constructive new-work route instead
```

or:

```text
reason = why old work must be checked again
```

Then ask for explicit user permission before running it.

The only passing permission status for that class is:

```text
permission status = GRANTED_BY_USER: <explicit user approval>
```

Until that approval exists, use:

```text
permission status = BLOCKED_PENDING_USER_APPROVAL
```

Do not infer approval from a generic "proceed" unless the immediately preceding
agent message clearly identified the run as an audit/verification/retest/
double-check and asked for permission to run that class of work.

## Preflight Enforcement

Testing rules are part of preflight. No SAM test, gate, campaign run, or
result-producing script should run until the preflight class is stated.

For Codex or any other tool-using agent, this also gates tool use around SAM
work. No shell search, `apply_patch`, script execution, artifact generation, or
repo mutation is allowed before a task-specific Courtroom V4.2 preflight-only
report exists and the user explicitly approves continuing for that exact task.

The approval is single-use and task-specific. It cannot be reused for later
turns, adjacent tasks, follow-up campaigns, reruns, audits, or artifact work.

Required preflight file:

```text
SAM_TEST_PREFLIGHT.md
```

Required execution path:

```text
python tools/run_sam_test.py --task "<exact task name>" --script <script.py>
```

Direct execution of SAM result-producing Python scripts is blocked by the
per-script preflight guard unless the runner has approved the preflight.

Repository files can enforce the runner path. Mechanical blocking of raw agent
tools such as shell, search, or `apply_patch` must be installed in the outer
harness/system-instruction layer that controls tool availability, the user must be notified of any changes.
