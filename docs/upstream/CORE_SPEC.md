# R4 shared quantities, signed values and logarithmic histories

This implementation extends the installed R3 source and retains its R2/R3
native fields, role definitions, source accounts, formal-log algebra and full
ordered histories. The new summaries appear automatically on ordinary native
motion and the existing CE packet history attachments.

## Shared quantity meanings

`quantities.normalize_descriptor(raw=None)` produces `GEN2_QUANTITY_V1` with
`kind`, exact `units` exponent map, `normalization`, `reference_state`, `frame`,
`scope`, `sign_convention`, `source`, `component` and `role`. Omission selects the
registered dimensionless signed-rational scalar. Floating operands are rejected.
`normalize_exact_value` is for rational numerical values; it does not reinterpret
bookkeeping labels or formal information logs as numbers.

`compatible_add` compares kind, units, frame, scope, reference and normalization
meaning. Different contributing source/component owners do not block compatible
unnormalized addition. A normalized common account is explicit through an
`account` or `source_account` field in normalization; otherwise the source,
component and role remain part of normalized compatibility. Signed, nonnegative
and positive *value* conventions share real-value arithmetic. Logarithmic and
phase conventions remain separate.

`add_descriptor` retains composed source ownership. `product_descriptor`
combines exact unit exponents, including subtraction under division.
`require_log_reference` requires a compatible positive reference for dimensional
logs. `source_quantity` registers native action, scale/log-scale, information and
phase/lift kinds with the native contract, role and original reference account.
`bind_formal_log` retains the exact bound source hash while the foundation's
temporary extraction is live.

## Signed arithmetic with contribution custody

`signed_log.dispatch(operation, payload, foundation)` supports:

- `GEN2_SIGNED_LOG`: `{nodes, result_id?}`.
- `GEN2_SIGNED_LOG_RESUME`: `{checkpoint, append_nodes?, result_id?}`.

A leaf is `{id, op:"VALUE", value, quantity?, reference?, source?}`. A reference
is `{value, quantity}` with strictly positive exact value. A binary node is
`{id, op:"ADD"|"SUBTRACT"|"MULTIPLY"|"DIVIDE", left, right}`. Every operand names
an earlier retained node. Repeated use creates repeated operand edges, so
`x-x` retains both occurrences rather than dropping their source contributions.

The bound `HDSignature` is the represented signed rational value. The separate
`FormalLogElement` records its logarithmic magnitude. Addition and subtraction
compute exact rational values, then regenerate HD/log coordinates. Products and
quotients use the native HD operations. Nonzero +1 and -1 have log magnitude zero
and retain distinct signs. ZERO has no finite logarithm. Division by zero returns
`DIVISION_BY_ZERO`; later dependent nodes retain `DEPENDENCY_UNDEFINED` and all
operand references.

Leaf values honor declared positive/nonnegative constraints. Subtraction returns
a signed-value convention; other operations preserve the guarantees of their
operand conventions. A dimensional value without its reference remains an exact
value with `log_status:REFERENCE_REQUIRED`. Additive references compare their
exact reference value and compatible meanings, allowing distinct provenance
owners of the same declared reference.
Products and quotients compose their effective references: a dimensionless
operand without an explicit reference uses exact reference 1, so multiplying
energy 6 with reference 2 by scalar 2 gives value 12, reference 2 and ln(6).
An unreferenced dimensional operand supplies no implicit reference. When both
dimensionless operands use reference 1 implicitly, their result retains the
ordinary implicit-reference representation.

The checkpoint retains normalized input nodes, evaluated nodes, root selection
and source/code bindings. Append evaluates only new nodes and reuses prior
results. A fresh-process checkpoint undergoes semantic verification once; cached
identical canonical checkpoint bodies reuse that verification. Altered/resealed
values, quantity meanings or graph associations are rejected.

## Owner-defined history summary

`history_summary.dispatch(operation, payload, foundation)` supports:

- `GEN2_HISTORY_SUMMARY`: `{quantity, source_binding, points, edges}`.
- `GEN2_HISTORY_SUMMARY_APPEND`: `{checkpoint, points, edges}`.

A point is `{id, state, action, status?}`. The full source state and occurrence
identity remain explicit. A directed edge is `{id, before, after, event}` and
must connect its actual adjacent point IDs. No connection is inferred from two
action numbers alone. `source_binding` labels the declared input/source contract.
Append supplies only new points and one connecting edge for each new point.

For positive source actions, the exact summaries are

`delta_ell = ln(E_after/E_before)`;
`U = sum max(0,delta_ell)`;
`D = sum max(0,-delta_ell)`;
`V = U+D`;
`net = U-D = ln(E_end/E_initial)`;
`M = max_t ln(E_t/E_initial)`.

The initial point participates in M. Every edge increment, contributing edge ID
and maximizing point tie remains present. Each result describes the original
action quantity and its separate normalized `summary_quantity`. Missing,
unavailable, undefined and observed nonpositive actions retain their records.
Such gaps make the whole-history summary `UNDEFINED_GAPS`; contiguous positive
segments retain their own complete summaries. The code creates no crossing edge
by skipping a missing/nonpositive point.

`compose(left_checkpoint, right_checkpoint, foundation)` requires one quantity
and source account and the identical boundary occurrence/state/action. It uses
`U_AB=U_A+U_B`, `D_AB=D_A+D_B`, `V_AB=V_A+V_B`, and
`M_AB=max(M_A, net_A+M_B)`. It retains the original A baseline, shifts B's local
excursion exactly, merges all maximum ties, and counts the shared point once.
Positive segments are composed explicitly when a larger trace contains gaps.

## Automatic motion and incremental reuse

Each ordinary motion role includes `history_summary`, bound to its own contact
triple and original source state. Existing packet annotations call the same
pure motion helper, so complete CE source histories receive the same summaries.
Nine-coordinate phase-only histories retain their existing type and do not
receive an invented source-action summary.

Generated motion appends only new native observations, contacts, directions,
source/role records and summary edges. It retains earlier records and their
original action baselines. The new suffix includes one shared boundary for
phase/log validation; accumulated lifts and logarithmic scales are then
expressed against the original history. An unchanged cached motion checkpoint
reuses prior semantic verification. Fresh-process restoration validates the
retained source history before continuing with new Writes.

`reuse_stats(reset=False)` on signed_log, history_summary and motion returns
independent process counters. Reset clears counters, not mathematical caches.
Counters distinguish new work, reused prior nodes/edges/states and fresh
checkpoint revalidation. They do not enter mathematical checkpoint identity.
Complete checkpoint serialization still carries the complete preserved history.

## Focused evidence and preservation

`core_tests/run_core.py` checks native closure, a new ln(5) value, signed unit
and zero distinctions, positive-value constraints, compatible references from
different components, explicit division-by-zero status, rise/fall identities,
append/composition equality, invalid source/checkpoint admission and actual
incremental continuation. Each attempt preserves its result or failure record.

The first direct test-script launch lacked the repository root in `sys.path`;
`core_tests/IMPORT_FAILURE.json` preserves that runner fault. No tests executed
before its correction and no candidate source change was required. A subsequent
focused run passed 29 checks and produced installed operation fixtures plus
separate signed/history fresh-resume request and expected-result pairs.

A read-only review identified a checkpoint admission asymmetry before
qualification: a resealed history checkpoint could bypass source-binding/value-
convention admission. A shared `_admit_source` now applies the same admission
at initial summary and restore; focused guards cover both altered forms.

The final reference-propagation correction preserves its executed pre-fix
example and both source versions under `core_tests/reference_propagation_fix1/`.
Before correction, referenced energy times a dimensionless scalar returned the
right value but lost its usable reference. The corrected multiply/divide checks
cover both operand orders and preservation of the missing dimensional reference
status. The final focused run
`core_tests/run_20260907T082513646857Z/RESULT.json` passes 34 checks and supplies
refreshed installation and signed/history restart fixtures bound to final code.
