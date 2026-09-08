# R4 information across construction boundaries

This adapter reuses the installed linked-record entropy implementation and the
active runtime's exact FormalLogElement. It registers variable maps on complete
source-bound finite assembly/history rosters. Source-account amounts,
multiplicities and response coefficients retain their construction meanings;
they do not become statistical weights.

## Public operations

The runtime facade calls `boundary_information.dispatch(operation, payload,
runtime)`. No separate logarithm runtime is opened.

| Operation | Payload and result |
|---|---|
| GEN2_BOUNDARY_OPEN | `source`, explicit `measure`; returns every admitted linked member, exact masses/probabilities, variable registry and sealed checkpoint |
| GEN2_BOUNDARY_INFORMATION | `checkpoint`, nonempty `left` and `right` variable-name lists, optional `given`; returns H(left), H(right), H(joint), H(left\|right), MI and I(left;right\|given), with linked partitions |
| GEN2_BOUNDARY_CONDITION | `checkpoint`, `reports` mapping registered exterior variables to supplied exact values; retains every compatible member and its original mass |
| GEN2_BOUNDARY_APPEND | `checkpoint`, `event`; extends all surviving native histories, preserving original identities/targets and weights |
| GEN2_BOUNDARY_RESUME | `checkpoint`; verifies binding, complete original relation, measure and ordered journal, then restores the same result |

Information units are nats. Joint tuples use the same complete relation and
measure. Conditional gain is H(left\|given) minus H(left\|given,right); separate
readings' information is never added as if they were independent. Interior
history targets contain actual source state/program associations; bookkeeping
record IDs never enter the variable maps. Undefined variables and an empty
relation are represented explicitly, not converted into a zero-valued reading.

`measure` is exactly `{"kind":"UNIFORM"}` or
`{"kind":"WEIGHTS","values":[...]}`. Positive rational values cover the full
source roster in deterministic order. Conditioning preserves those masses and
renormalizes by the surviving total; it never replaces them with uniform mass.

## Registered source rosters

`NATIVE` supplies a native `contract` and a nonempty `histories` list. Every
history has `initial`, `program`, and optional complete `states`. The compiler
validates each native transition, and supplied states must match it exactly.
The declared list is the complete finite experimental source domain. Duplicate
source histories are rejected. A missing contract selects the ordinary native
source. The joint state coordinates of a multi-receiver source already enforce
its shared coordinates.

`NATIVE_JOIN` supplies components with distinct `component_id`, native `source`,
strictly increasing `ticks`, `clock_id`, and `clock_unit`, plus explicit `joins`.
Each join is `{"left":[component,coordinate],"right":[component,coordinate]}`.
Shared coordinates require the same complete aligned clock and agree at every
tick. The resulting relation retains each compatible combination and its local
source/history witnesses. An empty joins list explicitly declares unrestricted
composition. Local probability distributions are never multiplied; the caller
declares one measure on the resulting assembly relation.

`CONSTRUCTION` supplies the existing typed construction `source` and a nonempty
`alternatives` list of `values` and optional activation `context`. Source forms
are compiled once per distinct context. Per-instance/action responses and total
exterior accounts remain separate variables. Inventory belongs to the instance,
so a hidden-support instance can supply both center and depth-loop responses
without a second copy of its amount.

`LI6` supplies a nonempty `alternatives` list. Each item has either an eighteen-bit
`state` or nine native `phases`, and optional existing cover/placement/rho/mask/
hidden-loop/receiver settings. Exact compiled forms are reused per setting.
Exterior signed site/cycle readings are calculated on the declared masked native
edge currents. The original construction alternative and every action response
remain linked to those readings.

`ENCOUNTER` supplies the existing calibrated transfer `source` and a nonempty
`alternatives` list of full `emissions`. Existing source/receiver ports, emission
ticks, observation windows, orientations and coefficients define the joint map.
No additional maintained-state transition is inferred from an arrival frame.

Native variable defaults include original `INTERIOR_HISTORY`, appended
`CURRENT_HISTORY`, current `INTERIOR_STATE`, `SOURCE_ACTION`, each receiver's
component state and separate signed/occupancy exterior readings. Equal-width
ports also register their exact exterior sum. Construction variables retain
interior configurations, source inventory, component action responses and total
exterior accounts. Li6 additionally registers `EXTERIOR:SITES` and
`EXTERIOR:CYCLES`; encounters expose each calibrated receiver/tick frame.

Every registered variable carries the shared quantity descriptor with source,
role, component, scope and declared units. Numerical channels normalize exact
rationals before partitioning. History/configuration labels keep their types.
Conditioning accepts only registered exterior channels and supplied readings.
It cannot condition on an interior identifier or replace a missing report with
zero. General report bins and missing-probe semantics belong to the shared R4
observation adapter.

## Incremental work and custody

Native APPEND takes one event label admitted on every retained history. Joined
APPEND takes `{"events":{component:event,...},"tick":new_tick}`: one declared
native event per component, an advancing clock tick, and agreement of every
shared boundary coordinate. It extends only the new endpoints; original
histories and mass lineage remain intact. Atomic validation prevents a failed
joint append from partially updating a session.

The checkpoint includes the full source recipe, original/current rows, original/
current weights, quantity registry and ordered condition/append journal. Its
binding covers source/quantity/entropy/compiler/assembly modules, native source
calibrations and the exact logarithm source. Fresh semantic restoration rebuilds
the declared relation and replays its journal. Validated complete checkpoints,
source relations and exact partitions are reused in bounded 128-entry caches;
keys retain source bindings, full histories, variables and weights.

Computational counters are available through `reuse_stats(reset=False)` and the
parent's `GEN2_REUSE_STATS` operation. No timing or cache counters enter the
mathematical result, source identity, or checkpoint seal. Ordinary construction,
site/cycle, readout and encounter calls automatically add a top-level `boundary`
registration while preserving every predecessor result field. A deterministic
ordinary call reports `COMPLETE_RELATION_AND_MEASURE_REQUIRED` rather than
inventing a probability distribution over unprovided alternatives.

## Focused evidence

The focused script is `tests_boundary.py`; named attempt folders preserve results
and failures. Run001 passed 25 checks. Run002 passed 29 checks after adding joined
incremental append, fresh semantic restoration and hidden-response information.
The disjoint four-history source has aggregate exterior information
`(3/2)ln(2)` and retains two owner arrangements under its middle report. Separate
ports supply the remaining `(1/2)ln(2)`. The shared-coordinate source admits two
combinations and returns `ln(2)` between its component states. Selected Li6
site/cycle and calibrated encounter readings resolve their supplied native
alternatives. No native run/forward operation is reexecuted by the adapter.

An initial multiline-with syntax error in the test harness was corrected before
run001; it did not execute a scientific test. The implementation's source-bound
tests produced no failed mathematical result.
