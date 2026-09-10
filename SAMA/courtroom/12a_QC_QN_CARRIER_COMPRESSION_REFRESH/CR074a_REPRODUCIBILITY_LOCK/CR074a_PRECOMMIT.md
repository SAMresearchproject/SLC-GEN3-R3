# CR074a - Reproducibility Lock - PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-21
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR074a/6)
**Test class:** REPRODUCIBILITY_LOCK_CR070a_TO_CR073a_PACK_AND_HASH_VERIFY
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` at repository root.

---

## Scope

CR074a is the **engineering CR** that locks the CR070a-CR073a runner
chain for partner-lab reproduction. It:

1. Walks each CR directory (CR070a, CR071a, CR072a, CR073a), verifies
   all expected artifacts present, recomputes file hashes, and
   verifies each hash against the corresponding CR's HASHES.txt
   entry.
2. Captures the ACTUAL Python and package versions used during the
   campaign run (not what was declared in per-CR requirements.txt
   files — see Discipline Drift Finding below).
3. Emits the three reproducibility-minimum files per the locked
   campaign decision: consolidated requirements.txt with pinned
   ACTUAL versions, .python-version pin, seeds.json documenting
   stochastic-step seeds (or noting their absence).
4. Bundles all artifacts plus STEWARDSHIP.md plus reproducibility-
   minimum files plus a CAMPAIGN_RERUN.md into a single
   CAMPAIGN_REPRODUCIBILITY_PACK.zip.
5. Runs predictions and wrong controls; reports pass/fail honestly.

CR074a does NOT add new physics. It locks what we have for external
rerun.

## Discipline drift finding (honest up front)

During CR070a, CR072a, and CR073a preparation, the per-CR
requirements.txt files pinned numpy==1.26.4 and matplotlib==3.8.4.
The ACTUAL versions installed during execution were:

```text
Python:     3.12.10  (declared per-CR: not specified)
numpy:      2.4.4    (declared per-CR: 1.26.4)  -- DRIFT
matplotlib: 3.10.9   (declared per-CR: 3.8.4)   -- DRIFT
```

The per-CR pins were aspirational, written before checking the
actual installed environment. The campaign's locked decision (per
campaign doc, 2026-06-20) requires "pinned exact versions for
reproducibility — pip install -r requirements.txt at the pinned
commit hash."

CR074a treats this as a CAUGHT discipline drift: the reproducibility
pack will use the ACTUAL versions used (2.4.4, 3.10.9, Python 3.12.10)
so a partner lab reproducing the run gets byte-identical results.
The per-CR requirements.txt pins are flagged as stale-but-locked-
historical (changing them would require new CRs).

This is exactly the kind of finding the reproducibility CR exists to
catch. Reporting it openly per the campaign's "max testing, failures
included" discipline.

## Stochastic-step inventory (seeds.json content)

Walked CR070a_runner.py, CR071a_runner.py, CR072a_runner.py,
CR073a_runner.py. **Result: no stochastic operations.** All runners
are deterministic from input CSV through numpy/matplotlib output
(Decimal arithmetic in qp094a-style; standard plot generation;
deterministic dict ordering).

seeds.json will document this finding: "no stochastic steps;
deterministic from input CSV."

## Inputs

```text
CR070a (full directory)              - 11 artifacts, HASHES.txt sealed
CR071a (full directory)              - 11 artifacts, HASHES.txt sealed
CR072a (full directory)              - 11 artifacts, HASHES.txt sealed
CR073a (full directory)              - 11 artifacts, HASHES.txt sealed
STEWARDSHIP.md (repo root)           - verbatim inclusion in pack
Actual installed Python + deps       - captured at pack-build time
```

Foundation primitives (unchanged):

```text
R       = 12
D       = 3
alpha_H = 2
```

## The reproducibility pack contents (locked structure)

```text
CAMPAIGN_REPRODUCIBILITY_PACK.zip
├── STEWARDSHIP.md
├── CAMPAIGN_RERUN.md
├── CAMPAIGN_PAUL_REVERE_FIELD_COMPARISON.md   (campaign scope doc)
├── requirements.txt                            (pinned ACTUAL versions)
├── .python-version                             (3.12.10)
├── seeds.json                                  (no stochastic steps)
├── PACK_MANIFEST.csv                           (every file + sha256)
├── CR070a_EXPANDED_NV_DIAMOND_T2_CONTACT_TABLE/
│       └── (11 files: PRECOMMIT, declared_premises, runner, table,
│            outputs, README, requirements, HASHES.txt)
├── CR071a_PHOTONIC_PR_LETTER_FRAMEWORK_MAPPING/
│       └── (11 files)
├── CR072a_PHOTONIC_EMPIRICAL_CONTACT_TABLE/
│       └── (11 files)
└── CR073a_CROSS_PLATFORM_PR_LETTER_SCALING_TEST/
        └── (11 files)
```

## Predictions

- **P1_all_CR_directories_present_with_expected_artifacts**
  Each of CR070a/CR071a/CR072a/CR073a has 11 expected files (PRECOMMIT,
  declared_premises, runner, input table, outputs, README,
  requirements, HASHES.txt). Missing any file fails P1.

- **P2_every_artifact_hash_matches_HASHES_txt_entry**
  For every file listed in each CR's HASHES.txt, recompute SHA-256 and
  verify match. Mismatch on any file fails P2.

- **P3_pinned_requirements_use_equals_equals**
  Consolidated requirements.txt uses `==` exact-version pins, not `>=`
  or `~=`. Verified by parsing the file.

- **P4_python_version_pin_is_exact**
  .python-version is a complete `MAJOR.MINOR.PATCH` triple
  (e.g., 3.12.10), not a partial pin (3.12) or range.

- **P5_seeds_json_documents_all_stochastic_steps**
  seeds.json explicitly notes "no stochastic steps; deterministic"
  for this campaign (verified by walking each runner for
  random/numpy.random/secrets calls — none present).

- **P6_CAMPAIGN_RERUN_md_exists_and_self_contained**
  CAMPAIGN_RERUN.md exists in pack root and documents: how to set up
  Python venv at pinned version, how to install pinned requirements,
  how to rerun each CR runner in order, how to verify pack hashes
  match, how to interpret X-of-Y outcome counts.

- **P7_STEWARDSHIP_md_included_verbatim**
  STEWARDSHIP.md from `C:\VS\The_Courtroom\STEWARDSHIP.md` included
  verbatim (byte-identical) in pack root.

- **P8_pack_does_not_include_external_non_citation_data**
  No external data files in the pack beyond what each CR runner
  produced or referenced via citation. Verified by manifest review.

- **P9_pack_is_single_file_emission**
  CAMPAIGN_REPRODUCIBILITY_PACK.zip is one file. Pack hash recorded
  in HASHES.txt.

- **P10_discipline_drift_finding_documented**
  CR074a output explicitly names the per-CR requirements.txt pin
  vs actual-version drift (numpy 1.26.4 declared, 2.4.4 actual;
  matplotlib 3.8.4 declared, 3.10.9 actual) and resolves it in
  the pack-level requirements.txt by pinning actual versions.

- **P11_protocol_completes_end_to_end**
  Runner completes hash verification, file collection, pack
  emission, summary writing without runtime error.

## Wrong controls

- **WC1_requirements_with_loose_pin_rejected**
  Synthetic test: requirements.txt with `numpy>=1.0` is rejected by
  the parser (P3 would catch this in real input).

- **WC2_missing_CR_artifact_detected**
  Synthetic test: walking a CR directory with a missing PRECOMMIT.md
  causes P1 to fail with the missing-file flagged.

- **WC3_hash_mismatch_in_pack_vs_HASHES_txt_detected**
  Synthetic test: if a file's actual SHA-256 differs from its
  recorded value in HASHES.txt, P2 fails with the row flagged.

- **WC4_missing_STEWARDSHIP_md_rejected**
  Synthetic test: if STEWARDSHIP.md is not found at
  `C:\VS\The_Courtroom\STEWARDSHIP.md`, P7 fails and the pack is
  not emitted.

- **WC5_no_Docker_requirement**
  Pack does not contain Dockerfile, docker-compose.yml, or any
  containerization spec. Verified by manifest content.

- **WC6_runner_does_not_modify_upstream_artifacts**
  CR070a-CR073a files are read-only during pack-building; checked
  by re-verifying CR070a-CR073a HASHES.txt files after pack-build
  completes.

- **WC7_no_free_parameters**
  Pack-build logic has no fitted constants. Pin values come from
  the actual installed environment.

- **WC8_pack_does_not_include_partner_lab_claims**
  Pack does not contain any text or artifact claiming partner-lab
  verification, hardware demonstration, or commercial protocol.
  Verified by manifest content scan.

- **WC9_per_CR_pin_drift_is_caught_not_silently_corrected**
  The per-CR requirements.txt files (with numpy==1.26.4) are LEFT
  AS THEY ARE in the pack — not silently rewritten. The pack-level
  requirements.txt is what governs the rerun; the per-CR ones are
  preserved as historical artifacts. P10 documents this.

## Outputs

```text
CR074a_pack_manifest.csv                 - every file + sha256 + role
CR074a_per_CR_hash_verify.csv            - hash verification per CR file
CR074a_discipline_drift_log.csv          - the requirements.txt drift finding
requirements.txt                         - consolidated, pinned, ACTUAL versions
.python-version                          - 3.12.10
seeds.json                               - no stochastic steps
CAMPAIGN_RERUN.md                        - rerun procedure
CAMPAIGN_REPRODUCIBILITY_PACK.zip        - single-file pack
CR074a_runner.py                         - the pack builder
CR074a_summary.json                      - pass/fail per prediction and WC
CR074a_result.md                         - human-readable
HASHES.txt
```

## Falsifiers

- A partner lab installing the pinned requirements at the pinned
  Python version and running each CR runner in order produces DIFFERENT
  hashes than the pack records. This would mean the
  reproducibility-minimum spec is incomplete (e.g., missing a
  platform-specific dependency).
- Any file's recorded HASHES.txt value disagreeing with its
  current SHA-256 means the upstream CR seal was tampered with;
  CR074a halts the pack build.

## Free parameters

```text
free_parameters = 0
```

## Honest expected outcome

CR074a is expected to PASS structurally on all 11 predictions and
all 9 wrong controls. The discipline drift finding (per-CR
requirements.txt pins vs actual versions) is documented as a
CAUGHT discipline issue, not a failure — the pack-level
requirements.txt resolves the drift by pinning to ACTUAL versions
used, and the per-CR pins are preserved as historical artifacts.

## Stewardship

Per `STEWARDSHIP.md`. Any commercial value flowing from this work
or its derivatives is subject to the stewardship intent: revenue
funds humanitarian causes.

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before runner execution.
Modifications to predictions, wrong controls, or scope after runner
output require a new CR.
