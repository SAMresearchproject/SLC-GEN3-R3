# CR252 Recheck Derivations

For every spine-input audit row marked `requires_recheck` in
`CR252_spine_input_audit.csv`, walk through the post-CR238 derivation
that determines whether the qp093a value is structurally consistent
with the current spine.

The validation criterion is **operational, not theoretical**: if the
qp093a value were structurally wrong post-CR238, the regen would
produce shifted M_native values at the rows that use it. The
row-delta step (CR252_row_delta.csv) tests this directly. This file
documents the proposed reading; row-delta confirms or refutes it.

---

## L328 — axis_factor in `native_single_mass()`

**qp093a value (line 328):**

```
axis_factor = {"plus": Decimal("1.25"), "minus": Decimal("1.5"), "neutral": Decimal("0.125")}
return p * axis_factor * (R ** generation_depth)
```

**Recheck against CR243 typed mass-lift channels.**

Per [project_typed_channel_table_closure_cr243_244], CR243 typed the
substrate mass-lift Y(P) = X/K closed across all 138 substrate-ledger
rows via seven typed forms. The substrate atoms are unchanged; what
CR243 added is the **typed channel** decomposition that classifies
which form a row's lift takes.

The qp093a axis_factor values in CR238-atom rationals:

- `plus = 1.25 = 5/4`
- `minus = 1.5 = 3/2 = D/α_H`
- `neutral = 0.125 = 1/8 = 1/S`

The `neutral = 1/S` ratio is structurally clean (one CR238 atom).
The `minus = D/α_H` ratio is structurally clean (two CR238 atoms).
The `plus = 5/4` ratio uses 5 — which is α_H + D, NOT a single
CR238 atom — flagged as the form most likely to shift if CR243's
typed channel form differs.

**Convergence reading:** if regen produces identical M_native for
single-axis rows (generation_depth ∈ {0,1,2}, axis ∈ {plus, minus,
neutral}), the L328 audit converges to `match` for qp093a's scope.
If single-axis rows shift, this section gets amended with the
specific CR243 derivation needed (and the named attribution gets
recorded in row_delta.csv).

---

## L434 — pair_m_native formula in pair enumeration

**qp093a value (line 434):**

```
m_native = (a * b * R) + (abs(q_value) * D)
```

**Recheck against CR244 unequal-pair typed forms.**

Per [project_typed_channel_table_closure_cr243_244]: "unequal-pair
lane uses R^4 denominator + OCTET-trigger (a=9 or b=9) correction
D^2/R."

The qp093a pair formula uses **R** (not R^4) and adds **|q|·D**
without an OCTET trigger. Two possibilities:

(1) CR244's R^4 denominator and OCTET correction apply to a
    **different scope** than qp093a's catalog enumeration. qp093a's
    pair channel may be the integer-mass shape from before the
    typed-form refinement, and CR244 may have refined a different
    cohort.

(2) CR244's typed form replaces qp093a's pair formula, in which
    case pair rows in regen would shift relative to the 2026-06-15
    baseline. If they don't shift, qp093a's formula is the
    integer-mass projection and CR244's typed form lives in a
    distinct downstream layer.

**Convergence reading:** if regen produces identical M_native for
pair rows (the bound_composite + unstable_resonance pair branches),
the L434 audit converges to `match` for qp093a's scope. If pair
rows shift, this section is amended with the CR244 derivation
walk and the named attribution gets recorded.

---

**Next:** the runner produces the row-delta. If single-axis rows
or pair rows show drift, this file is amended with the specific
named-CR attribution per row.
