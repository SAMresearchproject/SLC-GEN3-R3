# SLC-GEN3-R3

**Substrate Ledger Computer — computing with exact logarithmic state and retained history.**

SLC-GEN3-R3 executes native SAM source programs, acquires reusable source relations,
and retains execution state, learned support, complete histories and exact
logarithmic accounts in one runtime. A durable checkpoint keeps these together
for continuation in a fresh process.

Sean Brady is the originator and conceptual director. OpenAI ChatGPT and Codex
are credited as AI research collaborators. See [NOTICE.md](NOTICE.md).

## Run SLC-GEN3-R3

Use Linux and Python 3.11 or later. The release checks use Python 3.12.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-tested.txt
python -m slc_gen3_r3 verify
python -m slc_gen3_r3 run GEN3_EXECUTE examples/r3-word.json --state-dir runs/my-state --output first.json
python -m slc_gen3_r3 run GEN3_EXECUTE examples/r3-continue.json --state-dir runs/my-state --output continued.json
```

The second process restores the first process's state and continues its Writes.
Choose new output filenames for subsequent runs. Each call retains input,
output and SHA-256 receipts under `runs/`; failures retain their own records.

```python
from slc_gen3_r3 import open_runtime

with open_runtime(state_dir="runs/python-state") as slc:
    result = slc.execute("GEN3_EXECUTE", {
        "initial": [0, 0, 0], "program": ["W1+", "W7-"]})
    print(result["r3"])
    checkpoint = slc.execute("GEN3_CHECKPOINT", {})
```

[Usage and operation inputs](docs/USAGE.md) · [Distribution scope](docs/DISTRIBUTION_SCOPE.md)
· [Mathematical interface](docs/MATHEMATICAL_INTERFACE.md)
· [Current project status](docs/PROJECT_STATUS.md)

## What R3 retains

| Capability | Behavior |
|---|---|
| Execution and acquired support | Known source relations execute directly; new support is acquired during native execution. |
| Exact logarithmic accounts | U accumulates rises, D fall magnitudes, V = U + D, and net L = U − D. M retains every maximizing occurrence relative to the original reference. |
| Complete source history | Signed state, phase, barriers, events and explicit gaps remain available alongside summaries. |
| Incremental composition | Append new source history and compose adjacent accounts while retaining source custody. |
| Actual observation encounters | Apply supplied observations to acquired branches, retaining complete alternatives and choice ties. |
| Durable state | Restore execution state, acquired knowledge and accounts from one authenticated root. |
| Inherited operations | GEN2 operation names remain supported by the R3 runtime. `slc_gen2_r4` remains a compatibility entry point. |

The upstream source is **SLC-GEN3-R3**, build
`GEN3-UNIFIED-EXECUTION1-20260910`, generation
`GEN3-UNIFIED-EXECUTION1-20260910-G2`. The portable export has its own release
binding, documented in [source provenance](provenance/SOURCE_MANIFEST.json).

## SAM project background and research data

The [SAMA collection](SAMA/README.md) supplies the broader project's explanations,
derivations, tests and data alongside this SLC implementation.

| Research volume | Contents |
|---|---|
| [Volume I](SAMA/vol_i/README.md) | Substrate, accumulation, gravity, clocks and cosmology |
| [Volume II](SAMA/vol_ii/README.md) | Matter, particles, nuclei, binding and carriers |
| [Volume III](SAMA/vol_iii/README.md) | SAM language, SLC, Writes, history and applications |
| [Volume IV](SAMA/vol_iv/README.md) | Riemann Hypothesis research, results and corrections |

The collection includes 81 chapters, 23 branches, 1,246 test identities and
[5,340 copied Courtroom source files](SAMA/courtroom/). Its
[source manifest](SAMA/maintenance/COURTROOM_MIRROR.json) preserves the originating
file identities. [Research methods](SAMA/methodology/README.md) explain the
project's procedures. [Current status](docs/PROJECT_STATUS.md) dates the latest
engine and research information; earlier source records retain their original results.

## Check the release

```sh
python -m unittest discover -s tests -v
python SAMA/tools/check_structure.py
```

[Export validation](provenance/EXPORT_VALIDATION.json) records this distribution's
checks. Earlier qualification records remain identified as upstream provenance.

## Copyright, research permission and stewardship

**Copyright © 2026 Sean Brady.** The SLC software is source-available under
[LICENSE.md](LICENSE.md). It permits noncommercial research; commercial use,
commercial R&D, products and paid services require separate written permission.

The SAMA collection retains its [own licences](SAMA/LICENSE.md),
[notices](SAMA/NOTICE.md) and [stewardship](SAMA/STEWARDSHIP.md), including the
originating terms of copied Courtroom files. Its inclusion does not replace
those grants with the SLC research-use licence.

See [SLC stewardship](STEWARDSHIP.md), [rights guide](legal/RIGHTS_AND_COPYRIGHT.md),
[contribution process](CONTRIBUTING.md) and [dependency notices](THIRD_PARTY_NOTICES.md).
