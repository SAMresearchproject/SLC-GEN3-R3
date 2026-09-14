# SLC-GEN3-R3

**Substrate Ledger Computer: exact execution, acquired memory, and retained history.**

This is the public-facing SLC repository of the SAM Research Project. It brings
together the runnable portable SLC-GEN3-R3 implementation, current architecture,
research papers, computational findings, and supporting SAM source material.

**Research update: 14 September 2026.** The global engine is SLC-GEN3-R3 with
SLC-GEN3-CEV1-R3. The GEN3-RXT native deployment connects exact C++/GMP research,
CUDA construction and acquired source models. Its latest RH work develops exact
signed transport and a conditional route to RH; the uniform arithmetic estimate
remains open. Mersenne work includes native certificate validation, GPU factor
search and source/action learning.

Sean Brady is the originator and conceptual director. OpenAI ChatGPT and Codex
are AI research collaborators and co-authors. See [NOTICE.md](NOTICE.md).

| Start here | What you will find |
|---|---|
| [SLC architecture](docs/ARCHITECTURE.md) | Exact state, source learning, logarithmic accounts, observations and recovery |
| [GEN3-RXT](docs/GEN3_RXT.md) | Native CPU/GPU research and the relationship to the portable package |
| [Riemann Hypothesis research](research/rh/README.md) | Latest paper, exact identities, computational results and the remaining uniform estimate |
| [Mersenne / MP research](research/mersenne/README.md) | Certificate work, factor-search coverage, learned choices and paused campaign status |
| [All research areas](docs/RESEARCH.md) | RH, MP, Starbreaker, ATOM3D/Li-6, tau and clock/history work |
| [Current project status](docs/PROJECT_STATUS.md) | Dated engine and research status, with source provenance |
| [SAMA](SAMA/README.md) | Four supporting volumes, explanations, tests and historical source data |

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


## How SLC works

SLC keeps the state of an execution together with the source relations it has
acquired, actual observation encounters and complete ordered histories. Known
source relations can be reused; new admitted support becomes part of the same
machine. A durable authenticated root retains execution, knowledge and accounts
for continuation in another process.

Exact logarithmic accounts retain U (rises), D (fall magnitudes), V = U + D,
net L = U − D, and M with every maximizing occurrence. Exact ratio arguments
retain cancellation and composition without replacing source history with a
floating-point summary. Signed values, zero values and missing inputs have
explicit handling. Inherited GEN2 names remain supported compatibility calls.

The installed build is `GEN3-UNIFIED-EXECUTION1-20260910`, generation
`GEN3-UNIFIED-EXECUTION1-20260910-G2`. The portable binding remains
`SLC-GEN3-R3-RESEARCH-20260910-1`. This update adds current research and public
documentation; the included mathematical Python sources match the current
upstream sources checked for this update. [Distribution scope](docs/DISTRIBUTION_SCOPE.md)
identifies which domain and GPU deployments are separate.

## Riemann Hypothesis work

The September 14 paper develops an exact transport law for the original
stopped Möbius-source energy:

```text
Q(2s, 2t) = Q(s, t) + E(s, t) + R(s, t),    R(s, t) ≤ 3.
```

It gives a conditional SAM-to-RH implication from a uniform subpower bound on
the signed excess E, and a sufficient smaller-source transfer threshold that
approaches the quadratic exponent. Complete excess scans retain **12,836
prefixes at scales 32, 512, 4096 and 8192**. The largest observed excess is
0.520439137454. The candidate ceiling one survives this tested scope; the
half-ceiling has 13 counterexamples. These finite results and the remaining
uniform arithmetic estimate are recorded separately.

Read the [RH overview](research/rh/README.md), the [version 2 paper](research/rh/paper.md)
or its [ten-page PDF](research/rh/paper.pdf). The overview includes the source
certificates, failed fitted forecasts, selection audit, companion derivations
and downloadable exact scale-8192 data.

## Mersenne and MP work

The native MP domain validates certificates, reuses checked references and
performs exact batched factor elimination. The MP-B300 successor combines
native proof validation with GPU factor search and acquired source/action costs.
Its final documented campaign snapshot records **148,914,569,216 GPU lanes,
151 GPU batches and 150 proof-learning cycles**. A checked M1279 proof reduction
retains 163 powers rather than 277; the final quiet-context comparison selected
the original CPU route after measuring it. MP-B300 is paused by its owner.

[MP results and scope](research/mersenne/README.md) distinguish full native
validation, cached reuse, native factor checks and GPU-only no-factor coverage.
No new frontier Mersenne-prime certification is reported here.

## Evidence and supporting project material

Upstream R3 qualification records 617 core checks, 191 memory-admission checks
and 75 installed-adoption checks. The distributed fixture agrees on 8,123,904
exact values across i9, Ryzen and 780M execution, with T500 readback and recovery.
These are identified upstream workloads; public-package checks are recorded
separately in [update validation](provenance/PUBLIC_UPDATE_VALIDATION.json).

The [SAMA collection](SAMA/README.md) retains 81 chapters, 23 branches,
1,246 test identities and 5,340 copied Courtroom source files across
[Volume I](SAMA/vol_i/README.md), [Volume II](SAMA/vol_ii/README.md),
[Volume III](SAMA/vol_iii/README.md) and [Volume IV](SAMA/vol_iv/README.md).
Its original source records and licences remain intact. Dated historical
statements are read alongside this repository's current status pages.

## Check the package

```sh
python -m unittest discover -s tests -v
python SAMA/tools/check_structure.py
```

The current research [source index](research/SOURCE_INDEX.md) and
[hashed manifest](provenance/RESEARCH_UPDATE_20260914.json) identify the material
added in this update.

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
