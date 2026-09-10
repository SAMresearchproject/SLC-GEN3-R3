# LC05 - Periodic/Isotope Vault Replay

Result: **LC05_PASS_PERIODIC_ISOTOPE_VAULT_REPLAY_FROM_LOCKED_PRIMITIVE_STACK**

Question: with the locked primitive stack promoted in LC01, does the periodic/isotope vault replay without periodic-label backfill, row deletion, constant mutation, or frontier relabeling?

Verdict: yes. CR119/QP094A exports a 126-row native element-family table with downstream-only known labels, while the older branch-10 isotope vault keeps its scoped K1 roster pass and permanent frontier seal.

Locked stack used:
- alpha_H = 2
- R = 12
- D = 3
- split fraction = 1/8
- retained side = 7/8
- carrier side = 1/8

Replay count:
- Checks: 56/56 PASS
- CR119/QP094A periodic rows: 126/126
- Known downstream labels: 118/118
- Frontier unknown native identities: 8/8
- Known labels used as construction inputs: {'no': 126}
- qA split max Decimal error: 1E-96 (tolerance 1E-90)
- Branch-10 scoped K1 comparison: 162/162 for Z=1..96
- CR071 frontier seal: island rows 22, broader band rows 38
- Wrong controls: 10/10 rejected

Critical boundaries preserved:
- Known periodic labels and IAEA roster values are downstream comparator/reveal data, not generator inputs.
- Z119-Z126 remain native frontier identities, not promoted known elements.
- Z97-Z118 in the older branch remains a permanent CR071 frontier prediction boundary, not a failure or overwrite target.
- qA support columns are split by 1/8 and 7/8; qA is not element or isotope mass.
- Full nuclear shell-model, binding-energy, half-life, decay-channel, and synthesis-pathway derivations are not claimed here.

Primary artifacts:
- `16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_replay_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_periodic_table_invariants.csv`
- `16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_claim_boundaries.csv`
- `16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_checks.csv`
- `16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_sources_hashes.csv`
- `16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_summary.json`
