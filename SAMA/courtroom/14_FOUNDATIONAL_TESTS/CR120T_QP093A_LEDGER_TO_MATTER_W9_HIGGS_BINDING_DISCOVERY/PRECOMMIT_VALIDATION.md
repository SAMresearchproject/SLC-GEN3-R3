# CR120T Frozen Validation Precommit

Task: `Execute SAM_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY.md exactly as written`

Classification: constructive discovery followed by one frozen validation.

This document freezes the validation design after discovery and before any
CR261 test observation or CR277 extended observation is scored against a new
candidate. There will be no scientific repair, refit, exception addition, or
replacement candidate after this validation begins.

## Frozen discovery inputs

| File | SHA256 |
|---|---|
| `SOURCE_MANIFEST.json` | `b1eee6ab1603c7a3ed5995afb5e1b3061b17f1c8aafce11d7db0f675a7769451` |
| `runner_discovery.py` | `323de8fcb7d1e7e7d8d0b9db8f1b7767905a27ebc0ba43d09a76ac9f6cbade30` |
| `DISCOVERY_REPORT.json` | `e600a27831fe2b82ad5ece146cc353a16eb586cf11809eb4cc363e6b3cd99811` |
| `F81_CANDIDATE_RULES.json` | `c6b16102993898762c2ba12a9e33340a2e30c744f6a5e85f513c6a613f2867dd` |
| `BINDING_DISCOVERY_RESULTS.csv` | `76cb63f3175866a8aca1dd2999a4e9aa538e83f6db0916bf059959b0f02be5e8` |
| `BINDING_BASELINE.json` | `192096bd5e7354c243f015ea73d34fa26361852b14d7e8020e238ae6dfef2a06` |
| `BINDING_FEATURE_DEFINITIONS.json` | `89463644403a43ff733548a522456f1c0aeba9054db2323f2f1b2e9b4315bb68` |
| `freeze_candidates.py` | `fe67a9730226504293133bf6f3bf6ee50bb1386fed8326156b28a6987f914d01` |
| `F81_FROZEN_RULE_CONTRACT.json` | `c209c1250c51a1f54f68724396b6826247bf4d8aafd9bb36fd35ee6efc7f9877` |
| `BINDING_FROZEN_CANDIDATE.json` | `8194cff8f6c70b1e0f4ff3fb3b9dbe6b68a28adb3761fb8c2f10a9b6e4023b47` |

The source manifest in turn freezes the CR261, CR274, CR277, QP093A, workbook,
and typed-hierarchy source hashes. Any mismatch is a hard stop.

## F81 candidate under validation

The only rule to be validated is
`CR120T_F81_FROZEN_SOURCE_TYPED_RULE_V1`, containing the exact depth-5 tree
copied from `F81_TREE_DEPTH_5`.

Its permitted selection fields are:

`bin`, `operator_class`, `route_class`, `q_sign`, `closure_status`,
`stability_status`, `matter_row_allowed`, `same_role`, `p`, and `g`.

The runner must apply the frozen tree to the 126-row `count=1` saved-table lane
from the first updated workbook before it computes or reports the selected
count or selected `M_native` sum. The second workbook and its current-membership
column are forbidden validation inputs. Candidate IDs, row numbers, target count
81, target sum 12,600, `M_native`, and all other value columns are forbidden
selection inputs.

This candidate was trained against current membership during discovery. It is
therefore not an independent proof of the supplied 81-row roster even if it
matches it. Discovery already recorded a post-rule readout of 84 rows, so the
candidate enters validation as a partial structural rule, not as an exact F81
operator. No three-row exception patch is permitted.

### F81 validation gates

- `V_F81_0_HASH`: all frozen inputs and source hashes match.
- `V_F81_1_FIREWALL`: the selector reads only permitted source fields; the
  second workbook, current membership, IDs, targets, and value fields are not
  used.
- `V_F81_2_SHUFFLE`: row-order shuffling leaves the selected source-row set
  unchanged.
- `V_F81_3_VALUE_BLIND`: hiding/replacing `M_native` leaves selection unchanged.
- `V_F81_4_CONJUGATE`: the rule's selection is conjugate symmetric wherever a
  supplied charged/anti-charged pair exists.
- `V_F81_5_EXACT`: after selection, and only as a readout, the rule selects
  exactly 81 rows with `M_native` sum exactly 12,600.
- `V_F81_6_TYPED_CONTROLS`: arithmetic `p6+p3=p9` is not accepted as the same
  typed mechanism as source-declared S8 plus X1 to W9; role swaps, a missing
  conjugate, and a duplicated witness are detected as invalid ledger packets.

F81 status is `PASS_EXACT` only if all gates including `V_F81_5_EXACT` pass.
It is `PARTIAL_SOURCE_TYPED_RULE` if firewall/invariance gates pass but the exact
gate does not. It is `FAIL_RULE` if firewall or invariance fails.

## Binding candidate under validation

The frozen accounting cleanup is:

- neutral W9 witness local count = 0;
- QP093A-0066 Theta local fee = 0;
- QP093A-0299 repeated constituent count = 0.

This cleanup is required to be numerically identical to CR274 because those
quantities were not CR274 binding inputs.

The only numerical candidate is
`CR120T_BINDING_FROZEN_SURFACE_EXCESS_V1`:

`B_candidate = B_CR274 - gamma_82pre*op_82pre + gamma_surface*abs(N-Z)/A^(1/3)`

with frozen training-only `gamma_surface = 0.09121089246081573`. It replaces
the one-parameter `op_82pre` operator, so the free-parameter delta is zero.
Neither this coefficient nor any formula term may be changed after holdout
opening.

### Binding validation sequence and gates

1. Reproduce frozen CR274 predictions and the 55-row combined RMS from the
   source coefficients before scoring B3.
2. Reproduce the frozen CR277 table predictions to its published rounding
   tolerance and its published baseline metrics before scoring B3.
3. Score the immutable B3 candidate on the CR261 20-row test lane.
4. Score it on CR277 observed rows and separately on extended-only observed
   rows not in the original CR261 55-row roster.
5. Record light, mid, heavy, anchor, original-test, extended-only, whole-set,
   and frontier readouts. Do not refit or repair.

- `V_BIND_0_BASELINE`: CR274 combined 55-row RMS agrees with
  `2.716039627696933` within `1e-9`; CR277 recomputed predictions agree with its
  stored table within `5e-5 MeV`; recomputed CR277 baseline RMS agrees with
  `6.672483508062074` within `1e-6` using the stored rounded table.
- `V_BIND_1_FIREWALL`: gamma/formula hashes match the frozen contract; no test
  or extended observation was used in discovery; no repair is made.
- `V_BIND_2_TEST`: candidate CR261 test RMS is strictly lower than frozen CR274
  CR261 test RMS.
- `V_BIND_3_EXTENSION`: candidate extended-only RMS is no more than 2 percent
  above the frozen CR277 extended-only RMS.
- `V_BIND_4_WHOLE`: candidate 118-row observed RMS is no more than 2 percent
  above the frozen CR277 whole-observed RMS.
- `V_BIND_5_ANCHORS`: every O-16, Fe-56, Au-197, and Pb-208 candidate absolute
  residual is at most 10 MeV.
- `V_BIND_6_COMPLEXITY`: free-parameter delta remains zero; no per-isotope,
  per-family-validation, or target-specific parameter exists.
- `V_BIND_7_TYPED_ACCOUNTING`: W9 witness, Theta carrier, and Higgs global
  reveal remain non-repeated zero-fee accounting roles.

Binding status is `PASS_BINDING_IMPROVEMENT` only if every binding gate passes.
If the test improves but an extension/whole tolerance fails, status is
`BOUNDARY_TRAIN_TO_EXTENSION_TRANSFER`. Otherwise status is
`NO_FROZEN_BINDING_IMPROVEMENT`. Metrics remain reportable in every case.

## Frozen wrong controls

The validation will explicitly reject or flag:

1. removing every scalar-9 row;
2. treating every `p=9` row as W9;
3. treating `p6+p3=p9` as the source-typed S8+X1 mechanism;
4. counting W9 as an extra constituent;
5. repeating QP093A-0066 once per isotope;
6. repeating QP093A-0299 once per isotope;
7. using 126, 144, 162, 12,600, or 16,200 as fitted coefficients;
8. using target total as a selector;
9. using an ID whitelist or row-number list;
10. zeroing QP093A-0299 `M_native` without source authority;
11. assigning a local Theta fee;
12. treating qA as binding energy;
13. validation-family fitting;
14. same-run repair;
15. inferring physical identity from equal scalars;
16. treating a literal spreadsheet grid as proof of ontology.

## Verdict tree

The primary verdict reports components separately:

- accounting ladder;
- same-role row arithmetic;
- source-typed 8+1 to 9 interpretation;
- QP093A-0066 role;
- QP093A-0299 role and source discrepancy;
- F81 frozen rule status;
- binding frozen candidate status;
- wrong-control integrity.

`PASS_DISCOVERY_AND_VALIDATION` requires exact accounting, typed-source closure,
exact F81 validation, and binding improvement. A partial F81 rule or a binding
boundary produces `BOUNDARY_DISCOVERY_SUPPORTED_PROJECTION_OR_BINDING_OPEN`,
not a manufactured pass. A hash/firewall breach produces `FAIL_INTEGRITY`.

