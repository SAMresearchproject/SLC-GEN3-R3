# SAM/Courtroom Harness Preflight Gate

Install the following rule in the outer Codex harness, system instruction, or
tool-availability layer. Repository files cannot themselves prevent raw agent
tools from being called.

```text
For any task involving SAM, Courtroom, The_Courtroom, quantum_phase artifacts,
SAM theory artifacts, SAM scripts, SAM tests, SAM campaigns, SAM result files,
or SAM repository mutation:

1. Withhold shell, apply_patch, script execution, artifact generation, search,
   and repo-mutation tools until the agent has run exactly one task-specific
   Courtroom V4.2 preflight-only command:

   python tools\run_sam_test.py --task "<exact task name>" --preflight-only

2. The preflight-only command is the only permitted first executable action for
   that task.

3. After the filled preflight report is produced, require explicit user approval
   only if the preflight classification is audit/retest/double-check/
   confirmation/verification/replay/rerun-to-validate prior SAM results.
   Approval is single-use and task-specific. Clear same-task assent after the
   audit/retest notice counts; do not require one magic approval word.

4. If the preflight classification is constructive new work or manuscript/
   reference context, release task-scoped tools after preflight without a
   separate user approval stop.

5. If the task is an audit, retest, double-check, confirmation, verification,
   replay, or rerun-to-validate prior work, require the agent to state that
   classification and request explicit approval before any execution beyond
   preflight-only.

6. Do not reuse audit approval for a later turn, a different task, a nearby
   branch, a follow-up script, a generated artifact, a rerun, or an audit.

7. After preflight, allow only task-scoped tools. Any SAM result-producing script
   must run through:

   python tools\run_sam_test.py --task "<exact task name>" --script <script.py>

   If the script is audit-class, it must include --audit-approved after same-task
   approval.

8. After preflight, allow the agent to perform task-scoped orientation and work:
   repo search, source/PDF inspection, focused patching, correction ledgers, and
   hygiene checks. Require a fresh preflight if the objective, branch, requested
   output, or result-producing script changes.

9. Manuscript/reference correction work is constructive context work unless its
   primary target is re-running, auditing, or validating prior SAM results.
   Finding provenance for a formula or citation is not by itself an audit.

10. Enforce an anti-circling guard: one focused orientation pass, no repeated
   searches without new evidence, and a stop-and-summarize response if the same
   blocker repeats twice.

11. If the preflight root, required V4.2 docs, radix declaration, search ledger,
   latest-data gate, or last-test lookback is missing, fail closed and keep
   tool access withheld.
```

Repository-side coverage:

```text
AGENTS.md                  agent operating rule
SAM_TEST_PREFLIGHT.md      authoritative V4.2 preflight root
SAM_TESTING_RULES.md       test-classification and audit blocker
tools/run_sam_test.py      script-path enforcement
```

Boundary:

```text
The repository can enforce scripts run through tools/run_sam_test.py.
Only the outer harness can mechanically block raw shell/apply_patch/search tools.
```
