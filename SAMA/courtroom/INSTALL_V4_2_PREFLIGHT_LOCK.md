# SAM V4.2 Preflight Lock — Install Notes

## What this fixes

The runner now hard-points to the authoritative preflight and source documents instead of allowing agents/scripts to drift into a second preflight path.

Install these files into `C:\VS\The_Courtroom`:

```text
SAM_TEST_PREFLIGHT.md
SAM_TESTING_RULES.md
SAM_NATIVE_MASTER_FORMULA_V4_2.md
SAM_NATIVE_ACTION_ENGINE_V4_2.md
tools\run_sam_test.py
```

Recommended PowerShell install from the extracted package root:

```powershell
Copy-Item .\SAM_TEST_PREFLIGHT.md C:\VS\The_Courtroom\SAM_TEST_PREFLIGHT.md -Force
Copy-Item .\SAM_TESTING_RULES.md C:\VS\The_Courtroom\SAM_TESTING_RULES.md -Force
Copy-Item .\SAM_NATIVE_MASTER_FORMULA_V4_2.md C:\VS\The_Courtroom\SAM_NATIVE_MASTER_FORMULA_V4_2.md -Force
Copy-Item .\SAM_NATIVE_ACTION_ENGINE_V4_2.md C:\VS\The_Courtroom\SAM_NATIVE_ACTION_ENGINE_V4_2.md -Force
Copy-Item .\tools\run_sam_test.py C:\VS\The_Courtroom\tools\run_sam_test.py -Force
```

Run a preflight-only check:

```powershell
cd C:\VS\The_Courtroom
python tools\run_sam_test.py --task "QP091J HZZ4l projection bridge" --preflight-only
```

Run a script:

```powershell
python tools\run_sam_test.py --task "QP091J HZZ4l projection bridge" --script tests\qp091j_projection_bridge.py
```

Audit/retest runs are blocked unless explicitly approved:

```powershell
python tools\run_sam_test.py --task "audit QP091I" --script tests\audit_qp091i.py
```

That will block. Only run after explicit user approval:

```powershell
python tools\run_sam_test.py --task "audit QP091I" --script tests\audit_qp091i.py --audit-approved "User approved this audit after classification" --audit-reason "Specific suspected stale CSV rounding path"
```

## Environment overrides

```text
SAM_COURTROOM_ROOT
SAM_ARTIFACT_ROOT
SAM_PREFLIGHT_ROOT
SAM_MASTER_FORMULA_DOC
SAM_ACTION_ENGINE_DOC
SAM_TESTING_RULES_DOC
```

Defaults:

```text
SAM_COURTROOM_ROOT     = C:\VS\The_Courtroom
SAM_ARTIFACT_ROOT      = C:\VS\quantum_phase\artifacts
SAM_PREFLIGHT_ROOT     = C:\VS\The_Courtroom\SAM_TEST_PREFLIGHT.md
SAM_MASTER_FORMULA_DOC = C:\VS\The_Courtroom\SAM_NATIVE_MASTER_FORMULA_V4_2.md
SAM_ACTION_ENGINE_DOC  = C:\VS\The_Courtroom\SAM_NATIVE_ACTION_ENGINE_V4_2.md
SAM_TESTING_RULES_DOC  = C:\VS\The_Courtroom\SAM_TESTING_RULES.md
```

## Required emitted metadata

The runner exports these environment variables to target scripts:

```text
SAM_PREFLIGHT_TOKEN
SAM_PREFLIGHT_FILE
SAM_PREFLIGHT_ROOT
SAM_PREFLIGHT_ROOT_ID
SAM_MASTER_FORMULA_DOC
SAM_ACTION_ENGINE_DOC
SAM_TESTING_RULES_DOC
SAM_RADIX_R
SAM_REPO_SEARCH_COMPLETED
SAM_LATEST_DATA_CHECKED
SAM_LAST_TEST_LOOKBACK_COMPLETED
SAM_RUNNER_VERSION
```

Target scripts can fail closed by requiring `SAM_PREFLIGHT_TOKEN` and checking the document path variables.
