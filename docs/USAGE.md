# Using SLC-GEN3-R3

Run commands from the repository directory after installing requirements.txt in
your Python environment. Python 3.11+ is required; Python 3.12 and NumPy 1.26.4
are the checked combination for this release.

```sh
python -m slc_gen3_r3 info
python -m slc_gen3_r3 verify
python -m slc_gen3_r3 run GEN2_SIGNED_LOG examples/signed.json
python -m slc_gen3_r3 run GEN2_RUN examples/word.json --receipts runs
```

The CLI returns the unmodified operation result as JSON. Each run has a unique
directory with INPUT.json, OUTPUT.json and RECEIPT.json. A failed operation has
FAILED.json. Receipts identify the operation, release generation, exact input
and output digests and source-manifest digest. They are local execution records;
they are not an external digital signature or hardware attestation.

## Python and checkpoints

Keep one context open for related operations:

```python
import json
from slc_gen3_r3 import open_runtime

with open_runtime() as slc:
    native = slc.execute("GEN2_RUN", {
        "initial": [0, 0, 0], "program": ["W1+", "W1-"]})
    history = native["motion"]["roles"][0]["history_summary"]
    restored = slc.execute("GEN2_HISTORY_SUMMARY_APPEND", {
        "checkpoint": history["checkpoint"], "points": [], "edges": []})
    assert restored == history
```

Persist the entire checkpoint object, including body and sha256. Resume in a
fresh context/process using the relevant operation. Do not retain only a hash
or presentation summary. GEN2_HISTORY_SUMMARY_APPEND accepts only newly appended
points and their connecting edges; empty lists request semantic restoration.
For adjacent source-bound chunks use `slc.compose(left_checkpoint,right_checkpoint)`.
The helper invokes the preserved installed composition implementation.

## Declared target and exact weighted observations

```python
from slc_gen3_r3 import open_runtime

with open_runtime() as slc:
    inverse = slc.execute("GEN2_INVERSE_OPEN", {
        "blocks": [[1, 2, 3]],
        "mode": "ABSOLUTE", "observations": [None, None],
        "event_labels": ["W1+"],
        "initial_states": [[t, 0, 0] for t in range(4)],
        "target": {"kind": "BARRIER"}})
    masses = ["1/8", "2/8", "3/8", "2/8"]
    weights = {m["record_id"]: masses[m["initial"][0]] for m in inverse["members"]}
    choices = [{"label": "SCALE", "event": None,
        "readout": {"kind": "SCALE", "role": "J4_0.endpoint_a", "scope": "ENDPOINT"},
        "report": {"kind": "ABOVE_SAME_BELOW", "reference": 1}}]
    policy = slc.execute("GEN2_OBSERVATION_POLICY_PLAN", {
        "checkpoint": inverse["checkpoint"], "weights": weights,
        "choices": choices, "horizon": 2})
```

The complete three-channel PARITY/PAIR/SCALE case is in
tests/fixtures/owner_channels.json and tests/test_release.py. The fixtures
preserve actual candidate record IDs, report encodings, all alternatives and
the exact policy DAG. The selected policy for that case is PAIR followed by
STOP on both branches, with expected reads 1.

APPLY requires an actual observed report, or the explicit missing-report form
allowed by the interface. Candidate predictions are possible answers, not an
instruction to invent a measurement. Planning alone does not apply a report.

## Operation families

| Family | Entry points |
|---|---|
| Native histories | GEN2_COMPILE, GEN2_RUN, GEN2_DECODE, GEN2_RESUME, T18_WORD |
| Exact arithmetic | GEN2_HD, GEN2_HD_PRIMITIVES, GEN2_FORMAL_LOG, GEN2_SIGNED_LOG, GEN2_SIGNED_LOG_RESUME |
| Summaries | GEN2_HISTORY_SUMMARY, GEN2_HISTORY_SUMMARY_APPEND, `slc.compose` |
| Inverse and observations | GEN2_INVERSE_OPEN, GEN2_INVERSE_RESUME, GEN2_OBSERVATION_PLAN, GEN2_OBSERVATION_APPLY |
| Adaptive policies | GEN2_OBSERVATION_POLICY_PLAN, GEN2_OBSERVATION_POLICY_APPLY, GEN2_OBSERVATION_POLICY_RESUME |
| Motion | GEN2_RUN with motion payload, GEN2_MOTION_RESUME |
| Boundaries | GEN2_BOUNDARY_OPEN, GEN2_BOUNDARY_INFORMATION, GEN2_BOUNDARY_CONDITION, GEN2_BOUNDARY_APPEND, GEN2_BOUNDARY_RESUME |
| Constructions/readouts | GEN2_CONSTRUCTION_COMPILE, GEN2_CONSTRUCTION_CHANGE, GEN2_LI6_CONSTRUCTION, GEN2_LI6_SITE_CYCLE, GEN2_READOUT, GEN2_READOUT_INVERSE |
| Encounters and custody | GEN2_ENCOUNTER, GEN2_ENCOUNTER_INVERSE, GEN2_CUSTODY |
| Work counters | GEN2_REUSE_STATS |

See DISTRIBUTION_SCOPE.md for the N72 hardware profile and separate tau and
multi-host deployments. Inherited GEN2 operation payloads retain their source schemas;
the portable wrapper does not translate floating approximations into exact data.

## R3 execution and durable continuation

`GEN3_EXECUTE` accepts the native `initial` and `program` fields. Omitting
`initial` continues the runtime's saved state and contract. The first call
requires an explicit initial state. Results include an `r3` account and retained
history in addition to inherited native fields.

```python
from slc_gen3_r3 import open_runtime

with open_runtime(state_dir="runs/r3-state") as slc:
    slc.execute("GEN3_EXECUTE", {"initial": [0, 0, 0], "program": ["W1+"]})
with open_runtime(state_dir="runs/r3-state") as slc:
    continued = slc.execute("GEN3_EXECUTE", {"program": ["W7-"]})
    status = slc.execute("GEN3_STATUS", {})
```

Use `--state-dir PATH` with the CLI to attach the same durable store. Successful
changing calls persist state automatically; `GEN3_CHECKPOINT` explicitly emits
the authenticated root. Only one writer may open a state directory at a time.
The locally generated custody key belongs to that store and is not release data.

`GEN3_LOG_OPEN` takes `account`, `quantity`, `source_binding`, `points`, `edges`.
`quantity` is a descriptor such as `{"kind":"SOURCE_ACTION","units":{},"scope":"HISTORY"}`; `source_binding` identifies the declared source.
Points have unique `id`, full `state`, exact `action` and optional availability
`status`; edges have `id`, adjacent `before`/`after` IDs and explicit `event`.
`GEN3_LOG_APPEND` takes `account` and new connecting `points`/`edges`.
`GEN3_READOUT` and `GEN3_HISTORY_EXPORT` take `{"account":"name"}`.
`GEN3_LOG_COMPOSE` takes a new `account` plus adjacent `left`/`right` accounts.
`GEN3_LOG_IMPORT` applies source admission to the supplied complete history.

`GEN3_MEMORY_NODE` exposes an acquired node. `GEN3_MEMORY_START` takes `memory`,
a new `encounter`, and optional `node`. `GEN3_MEMORY_APPLY` requires `encounter`,
an actual `observation`, and source `evidence`.

The installed acquired relation and observation seeds are included. Remote
replication and project-specific CE services require separate deployment.
