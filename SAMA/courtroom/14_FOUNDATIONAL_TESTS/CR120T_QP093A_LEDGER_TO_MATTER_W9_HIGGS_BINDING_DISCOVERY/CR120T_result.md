# CR120T Result

Primary verdict: **BOUNDARY_DISCOVERY_SUPPORTED_PROJECTION_OR_BINDING_OPEN**

## Component verdicts

| Component | Verdict |
|---|---|
| Accounting ladder | `PASS_EXACT` |
| Same-role arithmetic | `PASS_ARITHMETIC_NOT_UNIQUE` |
| Canonical 8+1 to 9 | `PASS_SOURCE_TYPED` |
| QP093A-0066 | `PASS_CLOSURE_BUDGET_UNIT_CELL_WITH_CAUSAL_BOUNDARY` |
| QP093A-0299 | `PASS_HIGGS_REVEAL_PARENT_CANONICAL_126000` |
| F81 projection | `PARTIAL_SOURCE_TYPED_RULE` |
| Binding candidate | `NO_FROZEN_BINDING_IMPROVEMENT` |
| Wrong controls | `PASS_ALL_REJECTED_OR_DETECTED` |

## Source lineage and discovery posture

The original QP093A first output contained 321 rows. CR219's 126-row matter surface, CR253's 80-row shallow single-write surface, and the human-reviewed updated workbooks are separate looks at that source, not successive versions of one authoritative roster. The approved CR253 audit found that its minimal selector was only the pre-existing matter/antimatter bin plus depth 0 or 1; its charge and tensor-defect conditions were redundant. CR253 is therefore retained as a comparison surface, not used as ground truth for CR120T.

The 105-row expansion, five-row p=9,g=0 packet, 100-row closure, and proposed 81-row symmetric roster are treated as discovery observations. Their exact totals may guide candidate formation in discovery; they are prohibited as selectors or fitted coefficients during frozen validation.

## Exact ledger meanings

- `16,200 / 100 = 162 = L` is supported as an exact full-ledger accounting closure after the five p=9,g=0 packet occurrences are removed from the 105-row lane. It is not a binding-energy term, a fitted coefficient, or a mass subtraction.
- `12,600` is the exact `M_native` sum of the supplied 81-row roster and also equals `100M = 100*126`. The row count and the multiplier play different roles; this equality alone is not an F81 selector.
- The entire ladder reproduces exactly: `100L=16,200`, `100N=14,400`, `100M=12,600`, `L=N+Theta`, `M=N-Theta`, and `N=Theta+M`, with `L=162`, `N=144`, `Theta=18`, and `M=126`.

## Canonical 8 + 1 -> 9 interpretation

The canonical hierarchy privileges `S8_BINARY_SURFACE + X1_AXIS_SELF_CHANNEL -> W9_CLOSURE_WITNESS`: an unresolved binary surface plus an independent axis self-channel resolves to the closure witness. Scalar QP coordinates, carriers, supports, and typed hierarchy nodes remain distinct occurrences. At the QP row level, `p8+p1=p9` closes `M_native` at every available same-role depth, but `p6+p3=p9` does too. Arithmetic is therefore not unique; the source types, not scalar addition alone, privilege 8+1. Support column closure is neutral-lane specific because charged qA is nonlinear.

## Row dossiers

- **QP093A-0066:** the neutral `p=8,g=2` row is a row-local closure-budget unit cell: `144 = 18 + 126`, or `N = Theta + M`. Together with its neutral `p=1,g=2` and `p=9,g=2` neighbors it also closes `18+144=162`. Its absence from the supplied 81-row roster is real, but the available evidence does not uniquely decide between template/global-accounting exclusion and manual target-aware omission.
- **QP093A-0299:** the canonical source row controls at `M_native=126000`, followed by `126000-750=125250`, `125250/8=15656.25`, and `7*125250/8=109593.75`. Workbook 2's zero has no sealed source authorization. This row is a separate closed scalar-loop Higgs reveal parent, not the same object as QP093A-0066 and not a repeated per-isotope constituent.

## Frozen F81 validation

The best ID-free, value-blind source-field rule selected **84 rows** with post-selection `M_native=14077.125`. It was shuffle invariant, value blind, and conjugate symmetric, but it did not reproduce 81/12,600. The exact F81 operator therefore remains open: **PARTIAL_SOURCE_TYPED_RULE**. No three-row exception patch was added.

The five p=9,g=0 rows are supported as a global accounting packet for the 105-to-100 closure. The supplied F81 roster instead retains the four charged/conjugate occurrences and excludes the neutral occurrence, supporting a role-sensitive neutral W9 row witness as a candidate interpretation, not yet a finished projection law.

## Frozen binding validation

CR274 and CR277 baselines were reproduced first. B3 replaced the one-row `op_82pre` operator with the training-frozen geometry feature `abs(N-Z)/A^(1/3)` and added no free parameter.

| Lane | CR274 RMS MeV | B3 RMS MeV | Delta |
|---|---:|---:|---:|
| CR261 20-row held-out test | 3.017113068 | 4.071613571 | +1.054500503 |
| CR277 78-row extended-only | 7.974144225 | 8.067445504 | +0.093301279 |
| CR277 118-row observed | 6.672483502 | 6.828884165 | +0.156400663 |

Binding verdict: **NO_FROZEN_BINDING_IMPROVEMENT**. The exact accounting cleanup remains valid even if the numerical binding transfer does not promote.

## Remaining boundaries

- No finished source-registered F81 projection operator was found; the frozen best candidate is partial and cannot be patched from the known three exceptions.
- Exact scalar coincidences do not establish physical identity or a binding coefficient.
- QP093A-0066 exclusion causality remains unresolved.
- QP093A-0299's workbook-2 zero is rejected as an unauthorized overlay; the canonical 126000 row controls.
- Binding promotion is governed by the frozen holdout and extension gates only; no same-run repair was attempted.
