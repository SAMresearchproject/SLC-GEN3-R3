# SAM Test Preflight — V4.2 Locked Root

**Status:** AUTHORITATIVE ROOT PREFLIGHT  
**Purpose:** Prevent preflight diversion, stale-data runs, accidental audits, radix mistakes, and script construction before repo/context search.  
**Install target:** `C:\VS\The_Courtroom\SAM_TEST_PREFLIGHT.md` or the single path passed to `tools/run_sam_test.py --preflight`.  
**This file supersedes:** older loose preflights, templates, duplicate preflight files, copied preflight fragments, and agent-created substitute checklists.

---

## 0. Non-Negotiable Root Rule

There is only one active preflight root for a SAM result-producing run: **this file**.

An agent may read templates, historical rules, or branch-specific notes as supporting context, but it may not divert the run to a second preflight, alternate checklist, stale template, or self-made abbreviated gate.

For Codex or any other tool-using agent, the preflight lock begins before
ordinary tool use. For a SAM/Courtroom task, no shell search, `apply_patch`,
script execution, artifact generation, or repo mutation may occur until a
task-specific `tools/run_sam_test.py --preflight-only` report has been produced
for that same task.

After that report exists, explicit user approval is required only when the
preflight classification is audit/retest/double-check/confirmation/
verification/replay/rerun-to-validate prior SAM results.

Audit/retest approval is single-use and task-specific. It does not carry to
later turns, nearby branches, follow-up scripts, generated artifacts, audits, or
reruns.

If the preflight classification is constructive new work or manuscript/reference
context, the agent is allowed to work inside the preflighted task without asking
for a separate approval. Allowed post-preflight actions include task-scoped
read-only orientation, repository search, source/PDF inspection, focused file
edits, correction ledgers, and hygiene checks. The preflight does not allow a
changed objective, a branch switch, a new result-producing script, a rerun, or a
disguised audit.

Clear same-task assent after an audit/retest classification notice counts as
approval. The user does not need to use one exact approval word.

If another preflight-like file is found, classify it as:

```text
secondary_preflight_detected = true
secondary_preflight_path = <path>
secondary_preflight_status = SUPPORTING_CONTEXT_ONLY
root_preflight_wins = true
conflict_rule = use this V4.2 locked root; if the secondary file is stricter, copy the stricter clause into the filled decision block and report it
```

If an agent cannot establish which file is authoritative, stop before script construction.

---

## 1. Required V4.2 Source Documents

Before constructing any result-producing script, the agent must locate and read the current SAM source documents.

Required documents:

```text
MASTER_FORMULA_REQUIRED = C:\VS\The_Courtroom\SAM_NATIVE_MASTER_FORMULA_V4_2.md
ACTION_ENGINE_REQUIRED  = C:\VS\The_Courtroom\SAM_NATIVE_ACTION_ENGINE_V4_2.md
TESTING_RULES_REQUIRED  = C:\VS\The_Courtroom\SAM_TESTING_RULES.md
PREFLIGHT_ROOT_REQUIRED = C:\VS\The_Courtroom\SAM_TEST_PREFLIGHT.md
```

If V4.2 files are not present, stop with:

```text
preflight_status = BLOCKED_MISSING_V4_2_SOURCE_DOCS
missing_docs = <list>
allowed_action = locate/create/promote V4.2 source docs before running a SAM result script
```

V4.1 files may be read only as historical fallback context. They are not authoritative for a V4.2 run unless the user explicitly downgrades the run to V4.1.

---

## 2. Native SAM Radix Gate

SAM uses native duodecimal write accounting.

```text
R = 12_dec = 10_doz
R = 2 * alpha_H * D
alpha_H = 2
D = 3
A_share = 1/R = 1/12_dec = 1/10_doz
A_side = 1/(2R) = 1/24_dec = 1/20_doz
A0 = 1/(pi R) = 1/(12*pi)
```

Before interpreting any digit string, residual, fraction packet, route index, ledger digit, write cost, bounce cost, half-side, side/share packet, or route-pressure residue, the agent must declare radix handling.

Allowed radix basis values:

```text
PHYSICAL_DECIMAL_UNIT
SAM_NATIVE_R12_LEDGER
MIXED_WITH_EXPLICIT_CONVERSION
NOT_APPLICABLE
```

Rules:

```text
1. Decimal physical units remain decimal unless explicitly converted: MeV, GeV, meters, seconds, kg, Hz, external probabilities, detector counts.
2. SAM ledger/write-grammar digit strings are native R=12 unless explicitly declared otherwise.
3. Base-10 rendering of a SAM ledger string is display, not authority.
4. Conversions between R=12 and decimal must be emitted as auditable rows.
5. Reductions by alpha_H, D, alpha_H*D, R, 2R, or powers of R must be preserved and reported.
6. Half-ledger denominators such as 2R^n are not disposable noise unless a wrong control shows they are accidental.
7. Fractional subchannels must be located as radix shares whenever applicable:
   1/2 = 6/12 = 6_doz
   1/3 = 4/12 = 4_doz
   2/3 = 8/12 = 8_doz
   1/4 = 3/12 = 3_doz
   1/6 = 2/12 = 2_doz
```

Required radix block:

```text
radix basis =
radix interpretation =
R12 values used =
decimal values used =
conversion rows emitted = yes/no/not_applicable
wrong radix control required = yes/no
wrong radix control status =
```

---

## 3. Mandatory Repository Search Before Script Construction

Before writing or modifying a result-producing script, the agent must search the live repository and artifact roots for task-related keywords.

Required roots:

```text
ROOT_A = C:\VS\The_Courtroom
ROOT_B = C:\VS\quantum_phase\artifacts
```

If either root is unavailable, the agent must report it and search the nearest available equivalent working root. Do not silently continue.

```text
root_A_status = FOUND/MISSING
root_B_status = FOUND/MISSING
fallback_roots = <list or NONE>
```

### 3.1 Keyword Construction

The keyword list must be created from the user task before script construction.

Include, when present:

```text
1. test id or campaign id, e.g. QP091J, CR209, G744c
2. branch name, e.g. HZZ4l, particle_completion, write_closure, scale_bridge
3. core symbols, e.g. A0, A_share, A_side, R, alpha_H, D, qA, bounce, half-bounce
4. route terms, e.g. SW, WRITE, OUTSIDE, INSIDE, ledger_guard, degeneracy, projection
5. particle/event names, e.g. H, Z, Zstar, 4e, 2e2mu, 4mu
6. artifact names, e.g. HASHES.txt, manifest, ledger, result, summary
7. user-specified names or labels
```

### 3.2 Required Search Commands

Use `rg` if available. Equivalent search is allowed only if `rg` is missing.

PowerShell examples:

```powershell
rg -n -i -S "<keyword>" "C:\VS\The_Courtroom" "C:\VS\quantum_phase\artifacts"
rg -n -i -S "result_class|passed|execution_status|wrong_controls|boundary|pressure_class|hash|manifest" "C:\VS\The_Courtroom" "C:\VS\quantum_phase\artifacts"
rg -n -i -S "SAM_NATIVE_MASTER_FORMULA_V4_2|SAM_NATIVE_ACTION_ENGINE_V4_2|R = 12|10_doz|duodecimal|A_share|A_side" "C:\VS\The_Courtroom" "C:\VS\quantum_phase\artifacts"
```

Required search ledger:

```text
SEARCH LEDGER
search_required = yes
search_completed = yes/no
search_roots =
keywords =
commands_or_tool =
files_hit_count =
most_relevant_hits =
stale_or_conflicting_hits =
missing_expected_hits =
search_notes =
```

No script construction may begin until `search_completed = yes` or the run is explicitly blocked.

---

## 4. Latest-Data Gate

The agent must use the most up-to-date relevant data available in the searched roots.

Required latest-data checks:

```text
1. locate newest matching manifests, HASHES, result JSON/MD/TXT/CSV files, ledgers, summary files, and branch docs
2. record file modified timestamps
3. prefer highest explicit version number, then newest modified timestamp, then closest branch/test id match
4. reject stale copies unless deliberately selected as historical input
5. report conflicts between same-named files or version branches
```

Required latest-data block:

```text
LATEST DATA GATE
latest_data_checked = yes/no
version_priority = explicit_version > modified_time > branch_match
latest_master_formula =
latest_action_engine =
latest_testing_rules =
latest_branch_artifacts =
latest_hash_manifest =
stale_files_rejected =
conflicts_found =
conflict_resolution =
```

If the latest available source conflicts with a stale source, the agent must use the latest source unless the user explicitly asks for historical replay.

---

## 5. Last-Test Lookback Gate

Before proposing the next test, the agent must inspect the latest relevant prior result so it does not accidentally run a double-check, audit, replay, or retest.

Look for:

```text
result_class
passed
execution_status
external_sources
external_values
native_chain_tuned
external_values_used_as_generation_inputs
checks
wrong_controls
boundary
pressure_class
hash_manifest_rows
open_debts
next_gate
```

Required lookback block:

```text
LAST-TEST LOOKBACK
lookback_required = yes
lookback_completed = yes/no
last_relevant_test_id =
last_relevant_result_file =
last_result_class =
last_passed =
last_boundary =
last_open_debts =
last_next_gate_hint =
proposed_next_test =
relationship_to_last_test = NEW_CONSTRUCTIVE_STEP / USES_LAST_AS_INPUT / AUDIT_OR_RETEST / UNKNOWN
relationship_to_manuscript = MANUSCRIPT_OR_REFERENCE_WORK / NOT_APPLICABLE
```

If `relationship_to_last_test = AUDIT_OR_RETEST`, the run is blocked unless Section 6 is satisfied.

---

## 6. Audit / Retest / Double-Check Blocker

Default roadmap:

```text
PROGRESS_NOT_AUDIT
```

A run is **not** allowed by default if its main purpose is any of:

```text
confirmation run
double-check
audit
referee pass
hostile review
red-team review
rerun to validate a prior result
test whose main target is another test/result
replay whose main purpose is proving an already claimed result again
```

If the agent believes an audit/retest is necessary, it must stop and inform the user before running anything.

Required user-facing notice:

```text
This proposed run is a <audit/retest/double-check/verification/replay> of prior work, not constructive new work.
Reason old work must be inspected: <reason>
Constructive alternative if not approved: <new-work redirect>
Permission status: BLOCKED_PENDING_USER_APPROVAL
```

Only explicit approval after that notice can unlock the run:

```text
permission status = GRANTED_BY_USER: <quote or short note of explicit approval>
```

A generic “proceed” does not count unless the immediately preceding agent message identified the run as audit/retest/double-check/verification and asked for approval.

Manuscript/reference correction work is not automatically an audit. Looking up
the provenance of a formula, checking arithmetic used in prose, inserting a
section/page correction, or tying a manuscript sentence back to an earlier test
is constructive context work unless the main target is to re-run, re-grade,
audit, or validate a prior SAM result.

---

## 7. Constructive Work Requirement

A constructive SAM run must produce at least one of:

```text
new equation
new coefficient
new operator
new selector that fills a blank
new numerical prediction
new falsifiable comparison
new artifact that directly advances a branch
```

Required constructive block:

```text
CONSTRUCTIVE TARGET
class = CONSTRUCTIVE_NEW_WORK or CONFIRMATION_OR_AUDIT_REQUIRES_PERMISSION
target =
expected new output =
uses prior results as = INPUTS / EVIDENCE / CONTEXT_ONLY / TEST_TARGET
produces = new_equation/new_coefficient/new_operator/new_selector/new_prediction/new_comparison/new_artifact
```

If no constructive output can be stated, do not run. Reframe first.

---

## 8. Pattern, Relationship, and Breadcrumb Examination

After repository search and before script construction, the agent must examine the latest relevant artifacts for non-obvious structure.

This is not an audit. It is discovery/context extraction for the next constructive step.

Required examination lenses:

```text
1. native R=12 reductions and denominator patterns
2. alpha_H, D, alpha_H*D, R, 2R, R^n, 2R^n appearances
3. A0, A_share, A_side, pi*A0, 1/pi relationships
4. half-slot / six-slot chain:
   1/2 SW | 1/2 WRITE | 1/2 OUTSIDE | 1/2 INSIDE | 1/2 WRITE | 1/2 SW
5. degeneracy/projection operators, e.g. P_category ∝ raw_pressure * degeneracy
6. same-flavor / mixed-channel symmetry or antisymmetry
7. sign flips under label swaps
8. boundary rows, pressure flags, and open debts
9. failed wrong controls that reveal selector shape
10. stale rounding, CSV conversion, and display-vs-authority mismatches
```

Required breadcrumb block:

```text
PATTERN / BREADCRUMB SCAN
scan_completed = yes/no
patterns_found =
relationships_found =
breadcrumbs_for_next_test =
radix_sensitive_values =
rounding_or_format_risks =
recommended_constructive_next_step =
```

If no pattern is found, write `patterns_found = NONE_FOUND_AFTER_SEARCH`, not a blank field.

---

## 9. Script-Construction Gate

For agent-driven SAM work, script construction is not the only gated action.
Repository search, code edits, patch application, result-script execution, and
artifact work are also gated until the filled preflight-only report exists and
any required audit/retest approval has been granted for the exact task.

A result-producing script may be constructed only after Sections 1–8 pass or the run is explicitly blocked.

Every result-producing script must include or emit:

```text
preflight_root = SAM_TEST_PREFLIGHT_V4_2_LOCKED
preflight_file_path = <path>
master_formula_doc = SAM_NATIVE_MASTER_FORMULA_V4_2.md
native_action_engine_doc = SAM_NATIVE_ACTION_ENGINE_V4_2.md
radix_R = 12_dec = 10_doz
source_search_completed = yes
latest_data_checked = yes
last_test_lookback_completed = yes
constructive_classification = <classification>
permission_status = <status>
```

The script must abort if:

```text
1. preflight root is missing
2. V4.2 source docs are missing
3. repo/artifact search was skipped
4. latest-data gate was skipped
5. last-test lookback was skipped
6. audit/retest permission is required but absent
7. radix basis is blank
```

Allowed hygiene checks after edits:

```text
git diff --check
syntax checks
file-existence checks
if rerunning a newly created script only to emit its own artifacts is deemed helpful provide reasoning to the user and request rerun.
```

Hygiene checks may not relitigate old SAM results.

### 9.1 Post-Preflight Scope and Anti-Circling Guard

After the filled preflight for the exact task, the agent must keep a short
working boundary. If the task is audit/retest-class, this boundary opens only
after explicit same-task approval:

```text
preflighted_task =
preflighted_output =
allowed_context_pass = task-scoped source/repo/PDF inspection only
task_drift_rule = new objective, branch, result script, or validation target requires fresh preflight
```

The agent must avoid circling:

```text
1. Make one focused orientation pass before acting.
2. Do not repeat the same search or re-read cycle unless new evidence changes the target.
3. If the same blocker appears twice, stop looping.
4. When blocked, summarize the blocker, files checked, and the single next decision needed.
5. Prefer producing the requested correction/artifact over expanding the task.
```

---

## 10. Filled Decision Block — Required Before Every SAM Result Run

Paste and fill this block before running any SAM test, gate, campaign, or result-producing script.

```text
SAM V4.2 LOCKED PREFLIGHT DECISION
preflight_root = SAM_TEST_PREFLIGHT_V4_2_LOCKED
preflight_file_path =
secondary_preflight_detected =
secondary_preflight_path =
secondary_preflight_status =

REQUIRED DOCS
master_formula_required = C:\VS\The_Courtroom\SAM_NATIVE_MASTER_FORMULA_V4_2.md
master_formula_status = FOUND / MISSING / HISTORICAL_FALLBACK_ONLY
action_engine_required = C:\VS\The_Courtroom\SAM_NATIVE_ACTION_ENGINE_V4_2.md
action_engine_status = FOUND / MISSING / HISTORICAL_FALLBACK_ONLY
testing_rules_status = FOUND / MISSING

SEARCH LEDGER
search_required = yes
search_completed = yes/no
search_roots = C:\VS\The_Courtroom ; C:\VS\quantum_phase\artifacts
keywords =
commands_or_tool =
files_hit_count =
most_relevant_hits =
stale_or_conflicting_hits =
missing_expected_hits =

LATEST DATA GATE
latest_data_checked = yes/no
latest_master_formula =
latest_action_engine =
latest_testing_rules =
latest_branch_artifacts =
latest_hash_manifest =
stale_files_rejected =
conflicts_found =
conflict_resolution =

LAST-TEST LOOKBACK
lookback_required = yes
lookback_completed = yes/no
last_relevant_test_id =
last_relevant_result_file =
last_result_class =
last_passed =
last_boundary =
last_open_debts =
last_next_gate_hint =
proposed_next_test =
relationship_to_last_test = NEW_CONSTRUCTIVE_STEP / USES_LAST_AS_INPUT / AUDIT_OR_RETEST / UNKNOWN

PRE-FLIGHT TEST CLASSIFICATION
class = CONSTRUCTIVE_NEW_WORK / CONFIRMATION_OR_AUDIT_REQUIRES_PERMISSION
target =
expected new output =
uses prior results as = INPUTS / EVIDENCE / CONTEXT_ONLY / TEST_TARGET
tests prior tests/results = yes/no
if yes, reason =
if yes, constructive redirect =
permission status = NOT_REQUIRED / BLOCKED_PENDING_USER_APPROVAL / GRANTED_BY_USER: <explicit approval>

POST-PREFLIGHT SCOPE / AUDIT-APPROVAL GUARD
preflighted_scope =
allowed_after_preflight_if_permission_not_required =
audit_approval_rule =
task_drift_rule =
circling_guard =

RADIX GATE
radix basis = PHYSICAL_DECIMAL_UNIT / SAM_NATIVE_R12_LEDGER / MIXED_WITH_EXPLICIT_CONVERSION / NOT_APPLICABLE
radix interpretation =
R12 values used =
decimal values used =
conversion rows emitted = yes/no/not_applicable
wrong radix control required = yes/no
wrong radix control status =

PATTERN / BREADCRUMB SCAN
scan_completed = yes/no
patterns_found =
relationships_found =
breadcrumbs_for_next_test =
radix_sensitive_values =
rounding_or_format_risks =
recommended_constructive_next_step =

SCRIPT CONSTRUCTION DECISION
script_allowed = yes/no
if no, block_reason =
if yes, script_path =
expected_artifacts =
```

---

## 11. Agent Instruction Summary

Use this exact order:

```text
1. First executable action: run tools/run_sam_test.py --task "<exact task>" --preflight-only.
2. Read the filled preflight report.
3. If the report classifies the task as audit/retest/double-check/confirmation/verification/replay/rerun-to-validate prior results, stop for explicit same-task approval.
4. If approval is not required, or after audit approval is granted, keep work inside the preflighted task and make one focused orientation pass.
5. Load this V4.2 locked preflight root.
6. Locate required V4.2 master formula and action engine docs.
7. Derive task keywords.
8. Search C:\VS\The_Courtroom and C:\VS\quantum_phase\artifacts before constructing code.
9. Identify latest relevant artifacts and reject stale copies.
10. Look back at the last relevant test/result.
11. Decide whether the next run is constructive, manuscript/reference context, or an audit/retest.
12. If audit/retest, stop and ask the user with a reason and constructive redirect.
13. Declare radix handling; SAM ledger strings are R=12 by default.
14. Examine patterns, relationships, and breadcrumbs.
15. Only then construct the script.
```

If any step is skipped, the run is invalid.
