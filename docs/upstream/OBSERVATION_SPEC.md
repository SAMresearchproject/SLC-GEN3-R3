# R4 exact reports and adaptive observation policies

This candidate extends the R2/R3 complete linked inverse relation. Every member keeps its original program, ordered states, contact profile, barrier, positive endpoint-action ratio, target and source identity. Probe programs and states append separately. Identifiers remain association keys; the scorer partitions the declared target and actual returned report.

## Source quantities and report resolutions

The existing typed readout descriptor remains `{kind, role|roles, scope}`. Its quantity metadata is supplied separately through `GEN2_QUANTITY_V1`: source, component/role, units, normalization account, reference, frame, scope and sign convention. The original initial-state reference is symbolic metadata; an unknown candidate initial state is never appended to its observed value. Native receiver quantities distinguish ABSOLUTE frames from DELTA edges and sign reports from receiver amounts.

A choice may additionally declare `report`:

* `{"kind":"EXACT"}` returns the existing exact native/typed value.
* `{"kind":"ABOVE_SAME_BELOW","reference":1}` returns exactly `ABOVE`, `SAME` or `BELOW`. The reference is an exact rational, or an exact formal logarithm for a log channel. A zero rational reference is permitted for a log channel. No floating decision is used.
* `{"kind":"BINS","boundaries":[...],"closed":"LEFT"|"RIGHT"}` declares strictly increasing exact rational boundaries and all bins, including both exterior intervals. LEFT assigns equality to the bin on the right: index is the number of boundaries less than or equal to the value. RIGHT assigns equality to the bin on the left: index counts boundaries strictly below the value. The returned value is a zero-based integer bin index.

A coarse rule applies to an endpoint scalar; it never silently picks a component of a vector or a history. Log comparisons use the bound installed formal-log algebra; bins with rational cuts apply directly to rational-valued channels. The report wrapper is `{schema: GEN2_REPORTED_OBSERVATION_V1, channel, report, value}`. APPLY also accepts the raw actual report value and canonicalizes it to that wrapper.

All declared motion channels retain EXACT resolution. Registered INITIAL_ACTION SCALE channels additionally declare ABOVE/SAME/BELOW relative to one; LOG_SCALE declares the same comparison relative to zero. These are native normalization references, so an ordinary automatic request uses them without another flag. Explicit source profiles may declare `observation_reports: [{readout, reports:[...]}]`, including bins. `GEN2_INVERSE_OPEN.available_readouts` restricts source channels; `available_reports: [{readout, report}]` further restricts source resolutions. Neither whitelist invents a channel or a resolution. Undeclared explicit reports are rejected.

## Target and single-observation selection

Targets STATE, BARRIER and ACTION_RATIO keep their original R2 meaning. `{"kind":"HISTORY"}` targets the complete original source contract, ordered native program and ordered states. It does not target an opaque record identifier, and appending probes never changes it.

Automatic `GEN2_OBSERVATION_PLAN` maximizes exact target mutual information on the same positive record weights. Among all information maximizers it minimizes returned report entropy, then the realized report alphabet size, scalar payload width and original roster order. All information-maximizing labels remain in the result. Entropy and alphabet count concern the actual supplied report, not a hidden exact value behind it. Explicit R2/R3 rosters with no `report` field keep their original information, scalar-width and roster-order rule. An explicit reported roster uses the new detail rule.

APPLY requires an actual observation, including an observed scalar or bin value zero. `report_status: "MISSING"` is the distinct explicit alternative, and cannot be combined with `observation`. For an admitted probe, MISSING appends that native event and its predicted linked states to every complete candidate member, retains all candidates and their weights, and records the missing report. It performs no conditioning on the unavailable report. Ordinary omission remains an error. A source-unavailable probe does not become available through MISSING.

## Two-step adaptive policy

Public operations are `GEN2_OBSERVATION_POLICY_PLAN`, `GEN2_OBSERVATION_POLICY_APPLY` and `GEN2_OBSERVATION_POLICY_RESUME`.

PLAN accepts `{checkpoint, horizon?:2, choices?:[...], weights?:{record_id:positive_exact_mass}}`. The R4 finite release accepts horizons zero, one and two. An omitted roster uses the current source-declared automatic roster. STOP is a reserved terminal action. An explicit policy request defaults to horizon two; ordinary observation PLAN retains its one-observation API.

At each node the policy evaluates STOP and every choice admitted for the entire current conditional relation. It retains every report branch with its exact positive probability and all matching linked histories. The child sees conditional weights and original targets after the first native action. Zero immediate information does not exclude a first action: its children can provide information. STOP leaves all candidates intact and is selected when no further report improves the ordered objective. Once a branch has one original target class, an exact dominance certificate records zero target information for every available choice, nonnegative transcript entropy, alphabet size at least one and at least one read for every non-STOP choice. All available information-tied labels remain present, while their unnecessary future report branches are not materialized. A caller may still explicitly apply any available nonselected choice.

For a first report R and the adaptively selected second report S, the exact target information is `I(T;R) + sum_r P(r) I(T;S|R=r)`. Transcript entropy uses the parallel chain rule `H(R) + sum_r P(r) H(S|R=r)`. STOP has zero additional information and entropy, one empty transcript symbol, and zero read/Write/payload cost.

Among all target-information maximizers, policy selection minimizes transcript entropy, transcript alphabet size, expected read count, expected native Write count, expected scalar payload, then stable roster order. Conditional choices are allowed to differ between branches. All information ties and final detail/cost ties are retained. These objectives apply to the declared finite roster and horizon.

APPLY accepts `{policy_checkpoint, choice_label?:selected, observation:<actual>}` or explicit MISSING. STOP accepts no report. Every actual nonterminal application also seals an ordinary one-step decision plan with all alternatives, scores and weights into the ordinary session. Policy continuation retains the full preceding policy and actual report, the current ordinary checkpoint, the remaining horizon, the exact current measure and the complete next policy DAG. Missing reports preserve the interaction and calculate the next policy on the unfiltered extended relation.

RESUME accepts only `{policy_checkpoint}` and checks integrity, source and code binding, complete ordinary-session replay, all saved policy alternatives and chain rules, and the exact linkage from preceding policy through the actual report. The source contract is at `policy_checkpoint.body.session_checkpoint.body.contract`; `observation_policy.resolve_contract(operation,payload)` provides this route to the global facade. Resume mathematical output equals the saved result exactly.

## Incremental reuse and evidence

Prediction reuse keys source/code bytes, complete original/current native histories, target, readout and future event semantics. Policy DAG reuse additionally keys the exact conditional weights, original question, roster and remaining horizon. Receiver-equivalent histories retain their different ordered programs and states. Distinct labels and alternatives remain in the decision record even when computation is shared. Past report-envelope spelling is not a future native state; its complete custody remains in the enclosing session and policy chain.

Source-profile reuse keys the full normalized source contract plus hashes of the profile, calibration and relevant code; file signatures trigger a source-identity refresh when bytes may have changed. A bounded cache stores complete policy trees as immutable exact JSON bytes. Every returned tree is an isolated decoded copy, so caller mutation cannot alter cached evidence. Node retention is cleared between completed builds above its threshold; an in-progress complete tree is never truncated.

`reuse_stats(reset=False)` exposes execution counters separately. Counters never enter mathematical outputs, checkpoints, source identities or selection. Warm and fresh replay therefore have identical mathematical serialization. Focused test runs preserve source bindings, snapshots, failures, corrections, installation fixtures and a separate checkpoint-resumption package.
