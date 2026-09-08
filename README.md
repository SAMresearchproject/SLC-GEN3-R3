# SLC-GEN2-R4

**Substrate Ledger Computer — exact arithmetic, retained histories, and
target-directed observation policies. Research use only.**

R4 computes with native SAM/SLC source states and signed Write histories. It
retains exact rational and formal-log values, contribution identities,
alternative histories and all maximizing ties. It can summarize and compose
paths, restore checkpoints, and choose observations for a declared target using
exact weighted information and adaptive policies of up to two readings.

Sean Brady is the originator and conceptual director. OpenAI ChatGPT and Codex
are credited as AI research collaborators. See [NOTICE.md](NOTICE.md).

## Run the research engine

Use Python 3.11 or later. The release was checked on Python 3.12 with NumPy
1.26.4. From the repository directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-tested.txt
python -m slc_gen2_r4 verify
python -m slc_gen2_r4 run GEN2_RUN examples/word.json --output word-result.json
```

The example has action trace `6,8,10,8,6,10,6,4,2,4,4,2,4`, barrier `4`, and
maximizing occurrences `state:2` and `state:5`. The output retains the entire
history and its exact summaries. Each CLI calculation saves input, output and
SHA-256 custody records under `runs/`; failed calls retain a failure record.
Choose a new output filename for each run: existing output files are not overwritten.

```python
from slc_gen2_r4 import open_runtime

with open_runtime() as slc:
    result = slc.execute("GEN2_RUN", {
        "initial": [0, 0, 0],
        "program": ["W1+", "W1-"],
    })
    print(result["barrier"])
```

See [usage and exact inputs](docs/USAGE.md),
[release scope](docs/DISTRIBUTION_SCOPE.md) and
[mathematical definitions](docs/MATHEMATICAL_INTERFACE.md).

## Capabilities

| Capability | Retained behavior |
|---|---|
| Signed exact arithmetic | Rational values, prime-coefficient logs, cancellation contribution history and typed references |
| Native forward and inverse histories | Original states, Write order, compatible alternatives and declared original targets |
| Path summaries | Exact U, D, V, N and M, every maximizing occurrence, append and adjacent-chunk composition |
| Observation selection | Declared positive rational weights, exact target entropy/information, explicit report resolutions and ties |
| Adaptive policies | Horizons 0–2, conditional choices, STOP and original-target custody |
| Construction boundaries | Information on linked finite assembly histories with a separately declared measure |
| Sphere and motion | Inherited source-defined fixed-sphere/log/phase records and signed golden packet schedules |
| Checkpoints | Source-bound reconstruction of arithmetic, history, motion, inverse and policy state |

The portable interface exports the computational engine. Deployment-specific
tau and multi-host hardware operations require their separate application and
infrastructure bindings; the preserved source and exact boundary are documented
in [distribution scope](docs/DISTRIBUTION_SCOPE.md). The N72 source attachment
retains its explicit Linux CPU/compiler profile and is not run by the quick start.

## Reproduce the release checks

```sh
python -m unittest discover -s tests -v
```

The suite compares the portable package with 35 frozen installed R4 integration
fixtures and the owner-specified 12-event/nonuniform-weight test. It also launches
separate producer/consumer processes for checkpoint continuation. The larger
upstream installation record is preserved as provenance, with the distinction
between upstream qualification and this export's checks kept explicit.

All upstream computational bytes and required sealed foundation files have
source hashes in [SOURCE_MANIFEST.json](provenance/SOURCE_MANIFEST.json).
The portable launcher is separately identified; it does not replace the native
arithmetic or policy-selection implementation.

## Copyright, research permission and stewardship

**Copyright © 2026 Sean Brady. All rights reserved, subject to
[LICENSE.md](LICENSE.md) and independently applicable licences.**

You may run, inspect and privately modify this release for noncommercial
research, and publish research findings with attribution. Commercial use,
commercial R&D, products and paid services require separate written permission.
This is source-available research software, not an open-source licence.

The [stewardship declaration](STEWARDSHIP.md) preserves the existing commitment
that at least 90% of the defined net commercialization proceeds received by
SAM Research Project LC or a successor are intended for public-benefit purposes.
Commercial permission and operative stewardship agreements are separate from
the research-use grant.

For ownership, AI assistance, registration and contributor rights, see the
[rights guide](legal/RIGHTS_AND_COPYRIGHT.md),
[contribution process](CONTRIBUTING.md), and
[dependency notices](THIRD_PARTY_NOTICES.md).
