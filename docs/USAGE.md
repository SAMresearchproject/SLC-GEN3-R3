# Using the standalone engine

Run commands from the repository directory after installing requirements.txt in
your Python environment. Python 3.11+ is required; Python 3.12 and NumPy 1.26.4
are the checked combination for this release.

```sh
python -m slc_gen2_r4 info
python -m slc_gen2_r4 verify
python -m slc_gen2_r4 run GEN2_SIGNED_LOG examples/signed.json
python -m slc_gen2_r4 run GEN2_RUN examples/word.json --receipts runs
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
from slc_gen2_r4 import open_runtime

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
from slc_gen2_r4 import open_runtime

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
multi-host deployments. All operation payloads keep the original R4 schemas;
the portable wrapper does not translate floating approximations into exact data.
