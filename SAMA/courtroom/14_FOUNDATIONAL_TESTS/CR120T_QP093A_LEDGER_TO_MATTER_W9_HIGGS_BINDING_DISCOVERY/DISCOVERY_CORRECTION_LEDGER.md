# CR120T Discovery Correction Ledger

## Localized domain correction before freeze

The first discovery execution completed its mechanical gates, but the manual
freeze review found that F81 tree discovery had used every canonical-matched
row on the workbook's `Particle Stability Blocks` sheet. That sheet contains
313 candidate occurrences, of which 126 carry the workbook's explicit
`count=1` saved-table flag. The candidate feature join reduced the mistaken
domain to 299 canonical rows instead of the required 126 saved-table rows.

No validation data had been opened and no candidate had been frozen.

The runner was corrected to:

1. restrict F81 discovery to `count=1` rows;
2. require exactly 126 feature rows at gate D5; and
3. report both total candidate occurrences and saved-count rows in workbook
   inventory.

The discovery precommit, source manifest, workbooks, CR120R, and CR120S were
not changed. The corrected runner must be executed through the same Courtroom
task gate before any freeze decision.
