# CR284 Implementation Correction Record

## Initial Run

The first Courtroom execution on `2026-07-15T03:01:17Z` returned:

```text
CR284_FAIL_CAMPAIGN_INTAKE_CONTRACT
checks = 31/32
sources = 18/18
```

The only failed check was `C27`, which verifies that the water-stewardship
record does not invent an operative legal instrument.

## Cause

The required sentence was present in the frozen stewardship file, but a Markdown
line break fell between `itself` and `select`. The runner searched the raw text
for the sentence as one continuous string and therefore returned false.

## Correction

The runner now normalizes whitespace before performing that exact content
check. No contract file, source hash, scientific condition, species roster,
wrong control, campaign stage, claim boundary, or expected verdict was changed.

## Status Meaning

This was an implementation-string defect, not a failed desalination hypothesis
and not a scientific appeal. The first failure is preserved here rather than
silently erased by the corrected execution.
