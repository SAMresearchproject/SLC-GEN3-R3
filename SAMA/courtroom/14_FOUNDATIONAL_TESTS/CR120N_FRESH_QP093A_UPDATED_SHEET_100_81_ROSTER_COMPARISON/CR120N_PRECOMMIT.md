# CR120N Fresh QP093A Updated-Sheet 100/81 Roster Comparison — Precommit

record_id: `CR120N_FRESH_QP093A_UPDATED_SHEET_100_81_ROSTER_COMPARISON`

task: `Run fresh QP093A updated-sheet comparison for 100-row 16200 and 81-row 12600 rosters`

run_class: `CONSTRUCTIVE_NEW_WORK`

source_manifest_sha256: `4d92d00ac5653f1bf3e0d1e2202a221323ce8229abec8ad4292cabb62c6f71ff`

## Primary evidence

The two current workbooks are the primary evidence:

```text
C:\Users\drwho\OneDrive\Desktop\Updated Particle Rows.xlsx
C:\Users\drwho\OneDrive\Desktop\Updated Particle Rows2.xlsx
```

QP093A is used only to reconcile canonical candidate identity, bin, route, and
stored exact decimals. No prior CR supplies either roster or either total.

Both workbooks must be read directly from their XLSX ZIP/XML packages. No
formula, macro, generated code, or workbook calculation is executed.

## Frozen roster definitions

### Fresh 100-row roster

From `Updated Particle Rows.xlsx`, read `Particle Stability Blocks` and the
saved `tblStableMatter` data rows. Reconcile candidate ids against the frozen
QP093A lane:

```text
canonical lane = stable_matter_rows + antimatter_conjugate_rows
```

The lane must contain 105 unique rows totaling `16250.625`. Exclude the five
visible `p=9,g=0` rows at workbook rows 35–39:

```text
QP093A-0019
QP093A-0020
QP093A-0021
QP093A-0085
QP093A-0086
```

They must total `50.625`. The resulting workbook-derived roster must contain
100 unique rows totaling `16200` exactly.

The exclusion is user-proposed and known before execution. Its arithmetic is
not blind evidence and it does not delete or mutate the workbook or QP093A.

### Fresh 81-row roster

From `Updated Particle Rows2.xlsx`, read `M_native 12600 - 81 Rows` directly.
The sheet must contain 81 unique candidate ids totaling `12600` exactly. Its
cached checks must remain:

```text
ROWS(A2:A82)  -> 81
SUM(O2:O82)   -> 12600
AF3-12600     -> 0
```

The last formula makes the total target-aware. It is not a blind discovery.

## Sum-first claim

The claim is about the sums, not the row means.

With CR269's frozen `Theta=18`, `M=126`, and `R^2=144`, define:

```text
L_minus = 12600 = 100 * 126 = 100 * 7 Theta
L_mid   = 14400 = 100 * 144 = 100 * 8 Theta
L_plus  = 16200 = 100 * 162 = 100 * 9 Theta

L_plus - L_minus = 3600 = 2 * 100 * Theta
(L_minus + L_plus) / 2 = L_mid
```

`L_mid` is derived, not a third observed roster.

The 81-row roster cardinality is a distinct typed quantity. It is not the
denominator, multiplier, or normalization used to obtain `126`. Row means may
be emitted only as a wrong-normalization guard and must not be promoted as the
test signal.

## Direct sheet-to-sheet reconciliation

The run must reproduce these exact set facts from the two workbooks:

```text
shared ids                      72    sum 2506.5
100-roster only ids             28    sum 13693.5
81-roster only ids               9    sum 10093.5
same-id M_native mismatches       0
net row change                  -19
net sum change                -3600
```

The 81-row roster is not a subset of the 100-row roster.

The 28 removed-side rows and 9 inserted-side rows must remain explicit. The
runner must identify the 24-row conjugate-balanced block inside the 28-row
100-only packet and the five user-reclassified heavy rows inside the 9-row
81-only packet.

## Canonical authority boundary

Workbook labels are research overlays. In particular, these five ids remain
canonically `unstable_resonance_rows` with
`UNSTABLE_HEAVY_WRITE_CANDIDATE`:

```text
QP093A-0065
QP093A-0067
QP093A-0068
QP093A-0070
QP093A-0071
```

Their workbook inclusion may be analyzed but may not mutate QP093A or install
physical/canonical stability authority.

## Known-number disclosure

All headline counts and sums were known before execution. The result is a
reproduction, reconciliation, typed-composition, and selection-authority
test—not an independent numerical prediction.

## Wrong controls

The runner must reject:

1. analyzing row means instead of the frozen sums;
2. treating 81 as the multiplier or denominator that creates 126;
3. claiming the 81-row roster is a subset of the 100-row roster;
4. hiding the 28 removals or 9 insertions;
5. using a prior CR instead of extracting the current 100-row workbook roster;
6. deleting or merging p=9 identities;
7. promoting the five user-reclassified heavy rows to canonical stability;
8. calling 14400 an observed roster;
9. calling the known 100×162 or 81/12600 targets blind;
10. treating exact sum arithmetic as selection authority or physical mapping;
11. mutating either workbook, QP093A, CR269, or any registry;
12. executing workbook formulas, macros, or generated code;
13. hiding exact set differences or decimal residuals;
14. importing external physics to choose the rosters.

## Expected disposition

If every source, roster, sum, identity, set, mirror, and wrong-control gate
passes:

`PASS_STRUCTURAL_FRESH_QP093A_UPDATED_SHEET_SUMS_12600_14400_16200_EXACT_7_8_9_THETA_MIRROR_SELECTION_AUTHORITY_OPEN`

with:

```text
mathematical_verdict      PASS
result_class              STRUCTURAL_RESEARCH_BOUNDARY
scientific_pass_claimed   false
physical_mapping          OPEN_NOT_INSTALLED
roster_authority          USER_RESEARCH_OVERLAY_ONLY
selection_authority       OPEN_NOT_INSTALLED
```

## Required outputs

- `CR120N_ROSTER100_RAW.csv`
- `CR120N_ROSTER81_RAW.csv`
- `CR120N_ROSTER_COMPARISON.csv`
- `CR120N_WORKBOOK_EXTRACTION.json`
- `CR120N_SET_RECONCILIATION.json`
- `CR120N_SUM_MIRROR.json`
- `CR120N_SELECTION_AUTHORITY.json`
- `CR120N_WRONG_CONTROLS.json`
- `CR120N_VALIDATION_REPORT.json`
- `CR120N_summary.json`
- `CR120N_result.md`
- `COMMAND_LOG.txt`
- candidate manifest, candidate hash, and `HASHES.txt`

## Hard boundaries

- Preserve the two workbook rosters as raw evidence.
- Keep raw extraction separate from processed reconciliation.
- Do not substitute CR120K, CR120L, or CR120M for either workbook.
- Do not turn cardinality 81 into multiplicity 100.
- Do not replace a sum claim with a mean claim.
- Do not promote structural exactness to physical inventory authority.
