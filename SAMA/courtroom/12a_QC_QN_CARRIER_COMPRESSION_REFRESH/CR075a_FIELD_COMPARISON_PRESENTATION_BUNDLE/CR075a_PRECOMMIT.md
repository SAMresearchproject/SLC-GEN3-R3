# CR075a - Field Comparison Presentation Bundle - PRECOMMIT

**Status:** PRECOMMIT (frozen before runner executes)
**Date:** 2026-06-21
**Branch:** 12a_QC_QN_CARRIER_COMPRESSION_REFRESH
**Campaign:** PAUL_REVERE_FIELD_COMPARISON (CR075a/6)
**Test class:** FIELD_COMPARISON_PRESENTATION_BUNDLE_MARKDOWN_AND_PDF
**Author:** Sean Brady

---

## Copyright

Copyright (c) 2026 Sean Brady. **ALL RIGHTS RESERVED.**

Private research record. No license granted. See `STEWARDSHIP.md` at repository root.

---

## Scope

CR075a is the presentation/handoff CR for the Paul Revere Field Comparison
Campaign. It compresses CR070a-CR074a into one reviewer-facing bundle:

1. Markdown source document.
2. PDF distribution document.
3. Check table, summary JSON, human result, and HASHES.txt.

The bundle must be readable by a partner-lab contact, scientific reviewer, or
potential supporter in under one working day. It must present every failure and
boundary honestly.

CR075a does not add new physics and does not re-run CR070a-CR074a. It consumes
their sealed summaries and result files as inputs.

## Inputs

```text
CR070a_summary.json and result.md
CR071a_summary.json and result.md
CR072a_summary.json and result.md
CR073a_summary.json and result.md
CR074a_summary.json and result.md
CAMPAIGN_PAUL_REVERE_FIELD_COMPARISON.md
Paul_Revere_Next_Steps.md
STEWARDSHIP.md
09a CR220-CR228 result/summary surfaces as connection context only
```

## Required presentation content

The bundle must:

- open with `STEWARDSHIP.md` verbatim as front matter;
- summarize the PR letter framework without requiring the reader to accept SAM
  as a theory of everything before reading;
- summarize CR070a-CR074a with result-class strings and honest X-of-Y counts;
- show all failures and PROVISIONAL tags visibly;
- name the CR073a textbook 1/e mismatch and partner-lab measured `A_leak(t)`
  path;
- name bus-factor-1 risk explicitly;
- name the partner-lab verification path explicitly;
- include a clear ask for the next external engagement;
- avoid hardware-demonstration, partner-lab-agreement, or commercial-deployment
  claims;
- include the 09a connection notes only as regime/provenance/methodology
  context, not as direct quantum-hardware validation;
- deliver both markdown source and PDF distribution, with the PDF at or below
  30 pages.

## Predictions

- **P1_markdown_source_emitted**
  `CR075a_paul_revere_field_comparison_bundle.md` exists and is non-empty.

- **P2_pdf_distribution_emitted_and_under_30_pages**
  `CR075a_paul_revere_field_comparison_bundle.pdf` exists and the runner's page
  count is `<= 30`.

- **P3_stewardship_front_matter_verbatim**
  The markdown source begins with byte-identical `STEWARDSHIP.md` content.

- **P4_all_CR070a_to_CR074a_result_classes_visible**
  All five sealed result-class strings appear in the markdown source.

- **P5_failures_and_provisional_status_visible**
  The bundle visibly names CR070a violations, CR073a 0/14 load-bearing breach,
  PROVISIONAL citation status, and the CR074a requirements drift finding.

- **P6_bus_factor_1_named**
  The bundle explicitly names the one-author / bus-factor-1 risk.

- **P7_partner_lab_verification_path_named**
  The bundle explicitly names citation verification and measured `A_leak(t)` /
  `t_fire` hardware measurement as the external gates.

- **P8_clear_ask_present**
  The bundle closes with a concrete next action for an engaged reviewer.

- **P9_scope_boundaries_present**
  The bundle explicitly says it is not a hardware demonstration, partner-lab
  agreement, commercial deployment, or external validation claim.

- **P10_formula_surface_visible**
  The bundle exposes `A_side = 1/24`, `A_share = 1/12`,
  `c0_SAM = -0.5 * ln(23/24)`, `t_fire = coherence_time * c0_SAM`, and the
  textbook proxy `coherence_time * 0.5`.

- **P11_09a_connection_notes_present_with_boundary**
  The bundle includes CR220-CR228 connection notes and explicitly states they
  are regime/provenance/methodology context, not direct PR hardware validation.

- **P12_protocol_completes_end_to_end**
  The runner completes artifact generation, checks, summary, result, and hashes.

## Wrong controls

- **WC1_missing_stewardship_would_fail**
  The runner verifies the source starts with STEWARDSHIP content; removing it
  would fail P3.

- **WC2_missing_result_class_would_fail**
  The runner checks all five result classes; omitting one would fail P4.

- **WC3_hidden_failure_would_fail**
  The runner scans for the required failure/provisional phrases; hiding one
  would fail P5.

- **WC4_page_limit_enforced**
  The PDF page count is measured by the runner; exceeding 30 pages would fail P2.

- **WC5_scope_overclaim_rejected**
  The runner requires explicit boundary text rejecting hardware/partner/
  commercial claims.

- **WC6_formula_appendix_required**
  Omitting the formula surface would fail P10.

- **WC7_09a_overreach_guard**
  The runner requires boundary text saying 09a is connection context only, not
  direct PR hardware validation.

- **WC8_no_free_parameters**
  CR075a introduces no fitted constants or tuned thresholds.

## Outputs

```text
CR075a_paul_revere_field_comparison_bundle.md
CR075a_paul_revere_field_comparison_bundle.pdf
CR075a_checks.csv
CR075a_summary.json
CR075a_result.md
CR075a_runner.py
CR075a_declared_premises.json
README.md
HASHES.txt
```

## Free parameters

```text
free_parameters = 0
```

## Pre-execution seal

This PRECOMMIT.md is hash-sealed before runner execution. Modifications to
predictions, wrong controls, or scope after runner output require a new CR.
