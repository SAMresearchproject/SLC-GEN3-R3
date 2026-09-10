# CR120P Result

## Verdict

`PASS_BINDING_IMPROVEMENT_POTENTIAL_CONFIRMED`

**Direct answer: yes.** The specific `[p=9,g=0]` value removal has a source-backed mechanism with the potential to improve binding construction by preventing an exact dependent linear `M_native` contribution from being counted again as independent inventory.

## Decisive readout

- The frozen relation is exactly `[p=9,g=0] = [p=8,g=0] + [p=1,g=0]` for five rows.
- All five rows retain exact additivity, zero residual, passing type checks, and the executed W8/X1/W9 provenance.
- Their exact `M_native` sum is `50.625`.
- The 100-row workbook already implements the complete removal: `100` rows, `sum(M_native) = 16200`, zero retained candidate rows, and all 10 parent rows retained.
- Therefore the 100-row/16,200 assembly is `YES_POTENTIAL` for binding improvement through duplicate-inventory prevention and isolation of any separately modeled interaction/residual contribution.

## 81-row assembly

- As saved, the 81-row workbook has `sum(M_native) = 12600` and retains four charged `[p=9,g=0]` values totaling `49.5`; the neutral fifth row is already absent.
- Those four retained values are sign-balanced: positive `2` rows / `24.75` and negative `2` rows / `24.75`.
- Specifically removing those remaining four values produces `sum(M_native) = 12550.5` while retaining all 10 W8/X1 parent rows. That transformed assembly is also `YES_POTENTIAL` under the same duplicate-prevention mechanism.
- The saved 12,600 roster itself is `NO_SAME_MECHANISM_AS_SAVED` because its four charged `[p=9,g=0]` values are still present.

The broader 100-to-81 contraction is separately exact: the 100-only packet removes `28` rows totaling `13693.5`, including `12` positive rows / `6732` and `12` negative rows / `6732`. The 81-only packet inserts `9` rows totaling `10093.5`, giving the net `-3600` change. That signed contraction is not relabeled as the five-row removal.

## Binding boundary

The repo already contains isotope-varying binding datasets, a frozen holdout surface, signed binding operators, an observed 126-element panel, and CR276 role rows for all five candidates. That is enough to establish a real testable improvement mechanism.

It is **not yet a measured reduction in binding residuals**. No frozen per-isotope occupancy/multiplicity map currently joins the five particle rows to each isotope. Also, the global totals `16200`, `12600`, `50.625`, or `3600` used alone are exact scalar multiples of CR242's intercept and cannot add independent predictive information. The measurement step is a separately precommitted per-isotope feature test against the frozen holdout/observed panels.

## Controls

- All spreadsheet arithmetic used `M_native` sums, never means.
- No any-depth p9 deletion was used.
- No identity or provenance row was erased.
- No binding coefficient, isotope, holdout split, operator, or threshold was tuned.
- The 81-row sheet was not misreported as already implementing the complete five-row removal.
