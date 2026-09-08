# SLC-GEN2-R4 cumulative usage

R4 retains the complete R2/R3 interface and adds typed signed arithmetic,
logarithmic history summaries, deterministic report resolution, adaptive
observation policies and construction-boundary information. This document
describes the implemented R4 API. Actual installed version and generation come
from [CURRENT_REVISION](../../../CURRENT_REVISION/README.md); campaign status and
installation receipts determine when R4 is active.

Detailed contracts are in [CORE_SPEC.md](CORE_SPEC.md),
[OBSERVATION_SPEC.md](OBSERVATION_SPEC.md) and
[BOUNDARY_SPEC.md](BOUNDARY_SPEC.md). The retained sphere, golden scheduling,
native inverse and domain interfaces are documented in the
[R3 guide](../SLC_GEN2_SPHERE_GOLDEN_R3_1/INTERFACE_SPEC.md).

## Current entry points and automatic behavior

For research, start the applicable managed domain and keep its session warm:

```sh
./project start ATOM3D --objective "Examine native construction boundary information"
./project status /absolute/path/printed/by/project/start
./project run /absolute/path/printed/by/project/start \
  --operation GEN2_BOUNDARY_OPEN --payload /absolute/path/to/source_payload.json \
  --purpose "Construct the declared finite weighted assembly relation"
```

Start/status/run resolve authenticated current domain, global SLC, CE and
generation records. Repeat their actual `startup_verification` announcement;
its version comes from the registry. Startup records readiness; a research
calculation is evidenced by its actual input, output and operation receipt.

| Project call name | Current routing |
|---|---|
| `ATOM3D` / `A3D` | ATOM3D; Li6 retains its task-specific authority |
| `STARBREAKER` / `SB` | STARBREAKER |
| `RH` | RH |
| `MATTER_SEARCH` | MATTER_SEARCH |
| `MP` / `MERSENNE` / `MERSENNE-PRIME` | Owner-reopened native MP research, selected through the authenticated [MP record](../../../CURRENT_REVISION/domains/MP/DOMAIN.json) |
| `TAU` | TAU project backed by ATOM3D, with tau's live authority and authenticated model pointer |

These cumulative project-call routes are installed by
[H001009](../../../SAM_HISTORY/entries/H001009_2026-09-07_PROJECT_DOMAIN_CALL_METHODOLOGY.md)
and [H001010](../../../SAM_HISTORY/entries/H001010_2026-09-07_PROJECT_ALIASES_MP_REOPEN_AND_TAU_ENTRY.md).
MP uses the shared current GEN2 consumer; its historical MPV4 services and
stopping-point records remain preserved. A project start opens the selected
research session without launching a production workload. Any subsequent
owner-closure is enforced from the current records.

```python
from SAM_PROJECT.session import DomainSession

session = DomainSession("/absolute/path/printed/by/project/start")

def run(operation, payload):
    return session.execute(operation, payload,
        purpose="Evaluate the declared R4 source and retained history")
```

The examples below use this `run` function. The library route remains
`CURRENT_REVISION.load_slc().open_runtime()` with `runtime.execute(operation,
payload)`. Current CE and domain consumers expose the same operations through
`open_ce`, `open_domain` and the managed CLI. ATOM3D also routes Li6 and tau;
STARBREAKER, MATTER_SEARCH, RH and the reopened native MP route retain their
registered source operations and current domain scope.
See the [project-session guide](../../../SAM_PROJECT/README.md) for CLI payload
and receipt handling. After an activation, start a session for the new generation
and carry forward the intended source/checkpoint explicitly. Resume an existing
session only while its recorded generation remains current.

Ordinary `GEN2_RUN` with a prescribed `program` preserves its order and adds the
applicable source-profile sphere/log/phase histories and each role's R4 history
summary. A `motion` request delegates scheduling to the registered golden policy;
there is no additional enabling flag:

```python
native = run("GEN2_RUN", {"initial": [0, 0, 0], "program": ["W1+", "W1-"]})
partial = run("GEN2_RUN", {
    "initial": [0, 0, 0], "motion": {"packets": 3}, "max_writes": 1})
continued = run("GEN2_MOTION_RESUME", {"checkpoint": partial["motion_checkpoint"]})
```

Ordinary current ATOM3D CE contact packets obtain the same summaries from their
verified source histories. Retained `T18_WORD`/`direction_fiber` supplies its
nine-coordinate phase/lift/winding annotation; a phase-only source does not
declare a contact-action account. Construction, Li6 site/cycle, readout and
encounter calls automatically add a top-level `boundary` registration. A single
deterministic construction reports `COMPLETE_RELATION_AND_MEASURE_REQUIRED` for
information calculations. Its account amounts remain construction amounts.

## Exact values and signed contributions

Numeric payloads use integers or exact rational strings such as `"9/8"`.
Quantity descriptors carry kind, units, normalization/reference, frame, scope
and sign convention. Source/component/role associations are retained; normalized
accounts require their declared common account/reference for compatibility.
Dimensional logarithms require a compatible strictly positive reference.

```python
signed = run("GEN2_SIGNED_LOG", {"nodes": [
    {"id": "eight", "op": "VALUE", "value": 8},
    {"id": "one", "op": "VALUE", "value": 1},
    {"id": "nine", "op": "ADD", "left": "eight", "right": "one"}
]})
ratio = run("GEN2_SIGNED_LOG_RESUME", {
    "checkpoint": signed["checkpoint"],
    "append_nodes": [{"id": "ratio", "op": "DIVIDE",
                      "left": "nine", "right": "eight"}]})
```

`GEN2_SIGNED_LOG` accepts `{nodes, result_id?}`. Leaves additionally accept
`quantity`, `reference: {value, quantity}` and `source`. Binary operations are
`ADD`, `SUBTRACT`, `MULTIPLY` and `DIVIDE`, with earlier node IDs as operands.
`GEN2_SIGNED_LOG_RESUME` accepts `{checkpoint, append_nodes?, result_id?}`;
checkpoint alone restores the result. Cancellation preserves both contribution
edges. ZERO, signed units, a missing dimensional reference and division by zero
retain their separate arithmetic/log statuses.

## Explicit history summaries

Automatic native histories already include summaries. To summarize a separately
declared source-action trace, supply its source binding, quantity, ordered points
and actual directed associations:

```python
prefix = run("GEN2_HISTORY_SUMMARY", {
    "quantity": {"kind": "SOURCE_ACTION", "units": {"native_action": 1},
                 "scope": "HISTORY"},
    "source_binding": "EXPLICIT_NATIVE_LOOP_6_8_6",
    "points": [{"id": "s0", "state": [0, 0, 0], "action": 6},
               {"id": "s1", "state": [1, 0, 0], "action": 8}],
    "edges": [{"id": "e0", "before": "s0", "after": "s1", "event": "W1+"}]})
loop = run("GEN2_HISTORY_SUMMARY_APPEND", {
    "checkpoint": prefix["checkpoint"],
    "points": [{"id": "s2", "state": [0, 0, 0], "action": 6}],
    "edges": [{"id": "e1", "before": "s1", "after": "s2", "event": "W1-"}]})
```

These operations require exactly the shown top-level fields. Append contains
only new points and their connecting edges. Empty `points`/`edges` performs
semantic restoration without extension. The result retains exact U, D, V, net
change and M, including all maximizing-state ties and full edge contributions.
The loop above has `U=D=M=ln(4/3)`, `V=2ln(4/3)` and zero net change.
Missing, unavailable, undefined or nonpositive points preserve gaps and separate
positive segments. Adjacent-chunk composition is the module helper
`history_summary.compose`, described in CORE_SPEC; it is not a separate public
runtime operation.

## Inverse observations and adaptive policies

`GEN2_INVERSE_OPEN` accepts `mode:"ABSOLUTE"` with `observations`, or
`mode:"DELTA"` with `deltas`, plus `target`. Optional source selection is
`contract` or native `rho`/`blocks`. Event/direction knowledge, `known_phases` or
position-specific `conditions`, and `initial_states` must state the intended
knowledge explicitly. Targets are original `STATE`, `BARRIER`, `ACTION_RATIO`
or complete `HISTORY`. Probes append history without changing that target.

For example, supplied native frames can be opened and planned directly:

```python
inverse = run("GEN2_INVERSE_OPEN", {
    "mode": "ABSOLUTE", "observations": native["observations"],
    "event_labels": ["W1+", "W1-"], "target": {"kind": "BARRIER"}})
plan = run("GEN2_OBSERVATION_PLAN", {"checkpoint": inverse["checkpoint"]})
policy = run("GEN2_OBSERVATION_POLICY_PLAN", {
    "checkpoint": inverse["checkpoint"], "horizon": 2})
```

An omitted choice roster uses available native/motion channels and registered
report resolutions. Source-normalized SCALE declares ABOVE/SAME/BELOW relative
to one; LOG_SCALE uses zero. Explicit bins require source-declared boundaries
and endpoint inclusion. `available_readouts` and `available_reports` restrict
declared channels/resolutions. They do not supply observations.

| Operation | Exact minimal payload pattern |
|---|---|
| `GEN2_OBSERVATION_PLAN` | `{checkpoint}`; optional `choices`, `weights` |
| `GEN2_OBSERVATION_APPLY` | `{checkpoint, plan: sealed_plan, choice_label, observation: actual_report}` |
| `GEN2_INVERSE_RESUME` | `{checkpoint}` |
| `GEN2_OBSERVATION_POLICY_PLAN` | `{checkpoint}`; optional `horizon` (0, 1 or 2; default 2), `choices`, `weights` |
| `GEN2_OBSERVATION_POLICY_APPLY` | `{policy_checkpoint, observation: actual_report}`; optional `choice_label` (default selected) |
| `GEN2_OBSERVATION_POLICY_RESUME` | `{policy_checkpoint}` |

Here `plan` is the returned `plan["plan"]`, and policy custody is the returned
`policy["policy_checkpoint"]`. `actual_report` comes from the declared observed
channel; candidate predictions are possible outcomes. The explicit alternative
to supplying `observation` is `report_status:"MISSING"`, which retains an admitted
interaction and every candidate without a reading constraint. These fields are
mutually exclusive. A measured zero remains an observation.

Policy APPLY permits any available choice retained in its current tree, including
an explicit `choice_label:"STOP"`; STOP takes no observation or report status.
Each actual continuation carries its previous policy, ordinary sealed plan,
original targets, surviving masses and complete histories. Exact positive
`weights` must map every current record ID to a mass. Conditioning inherits
those masses and normalizes probabilities within each branch.

Automatic one-observation selection maximizes target information, then minimizes
report entropy, reachable report count, scalar count and roster order. Explicit
inherited rosters without a report rule retain their former information/scalar/
roster rule. Policies maximize total target information, then minimize transcript
entropy, reachable transcript count, expected reads, expected native Writes,
expected scalar payload and roster order. All maximum-information ties remain
reported. A zero-gain first reading can lead to an informative second step.

## Linked construction-boundary information

Declare the complete finite assembly/history roster and its separate measure:

```python
boundary = run("GEN2_BOUNDARY_OPEN", {
    "source": {"kind": "NATIVE", "histories": [
        {"initial": [0, 0, 0], "program": []},
        {"initial": [2, 0, 0], "program": []}]},
    "measure": {"kind": "UNIFORM"}})
information = run("GEN2_BOUNDARY_INFORMATION", {
    "checkpoint": boundary["checkpoint"],
    "left": ["INTERIOR_HISTORY"], "right": ["EXTERIOR:J4_0:SIGNED"]})
```

| Operation | Exact minimal payload pattern |
|---|---|
| `GEN2_BOUNDARY_OPEN` | `{source, measure}` |
| `GEN2_BOUNDARY_INFORMATION` | `{checkpoint, left:[variable], right:[variable]}`; optional `given:[variable]` |
| `GEN2_BOUNDARY_CONDITION` | `{checkpoint, reports:{exterior_variable:actual_value}}` |
| `GEN2_BOUNDARY_APPEND` | `{checkpoint, event:"W7+"}` for a native relation |
| `GEN2_BOUNDARY_RESUME` | `{checkpoint}` |

The variable catalog supplies names and quantity meanings. All marginal, joint,
conditional and mutual information uses those maps on the same linked rows and
measure, in nats. `given` requests conditional information gain. CONDITION keeps
every compatible row and its original mass. The alternative explicit measure is
`{"kind":"WEIGHTS","values":[...]}`, with one positive rational mass per original
source row in deterministic order.

Registered sources are `NATIVE`, `NATIVE_JOIN`, `CONSTRUCTION`, `LI6` and
`ENCOUNTER`. A join declares aligned clocks and shared coordinates and preserves
every compatible component history. An explicit empty joins list declares an
unrestricted composition; component probabilities are not silently multiplied.
Joined APPEND uses `event:{events:{component_id:event_label,...}, tick:new_tick}`
and validates all shared endpoints atomically. Construction amounts and hidden
support inventory remain distinct from statistical weights. Source schemas and
the Li6/site-cycle, hidden-support and shared-coordinate examples are in
BOUNDARY_SPEC.

## Reuse, fresh validation and preserved contracts

`GEN2_REUSE_STATS` accepts `{}` or `{"reset":true}` and returns process telemetry
by module. Reset clears counters, not mathematical caches. Measure before/after
the operation of interest; keep the execution record separate from its result.

New signed nodes, summary edges and motion suffix states have their own counters;
prior-node/edge/state reuse is counted separately. Observation predictions and
policy nodes distinguish cache hits from new evaluations. Boundary counters
separate source-relation/partition builds, validated-checkpoint hits and appended
transition lookups. A fresh process must semantically validate its saved complete
checkpoint; that work is reported as checkpoint revalidation, not as a new source
interaction. Warm reuse and fresh restoration retain identical mathematical
results. Full histories still appear in the checkpoint serialization.

Cache identity includes the relevant source/code/quantity/reference bindings,
complete histories, original targets, exact masses, allowed readings and remaining
horizon. R2/R3 exact algebra, native domain operations, ordinary sphere/golden
behavior, hardware roles and checkpoint custody remain part of the cumulative
release. Timing and reuse counters never enter mathematical identities or seals.
