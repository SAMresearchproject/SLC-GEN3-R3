# Exactly three GW-COM follow-up tests

The owner authorizes three bounded experiments: continuous-source Gaussian noise/SNR, physical scaling/detectability, and natural-carrier false positives. The [contract](CONTRACT.json) fixes every case before execution. There are no adaptive extensions or receiver changes.

The [completed report](REPORT.md) records 4/6 noisy-message recoveries, 0/6 matched-control statistical false positives, both physical scalings and 0/2 natural-nuisance packet false positives. All original results in GW_COM_CONTINUOUS1 remain frozen.

Run from the repository root, using a new output name if explicitly authorized to rerun:

```bash
.venv-r3/bin/python CURRENT_REVISION/engines/SLC/gen3/resources.py run -- .venv-r3/bin/python SAM_REVIEW/campaigns/GW_COM_THREE_TESTS1/run.py --run run001
```

The `run001` directory is exclusive and cannot be overwritten by the runner. Its `code/` and `METHOD.json` preserve the source, runtime, contract and curve snapshot. Records retain the waveform, fit alternatives, signed residuals, symbolizations, individual controls and gated hypotheses. `verify.py` checks saved arithmetic and custody without running new scientific cases.

The detector input is [Advanced LIGO design ASD T1800044-v5](https://dcc.ligo.org/public/0149/T1800044/005/aLIGODesign.txt), retrieved 2026-09-17, stored under `sources/`. It is a design reference, not present measured detector performance. Source physics uses [LIGO/Virgo's binary quadrupole derivation](https://dcc.ligo.org/public/0126/P1600161/013/BBHBasicsANDPFullAuth.pdf). The two natural nuisances are explicitly defined approximations in the contract; no message is injected into them.
