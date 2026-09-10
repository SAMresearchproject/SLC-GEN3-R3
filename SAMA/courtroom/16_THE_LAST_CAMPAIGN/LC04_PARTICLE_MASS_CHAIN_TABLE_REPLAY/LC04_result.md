# LC04 - Particle Mass-Chain Table Replay

Result: **LC04_PASS_PARTICLE_MASS_CHAIN_TABLE_REPLAY_FROM_LOCKED_PRIMITIVE_STACK**

Question: with the locked primitive stack promoted in LC01, does the particle mass-chain/table branch replay without formula mutation, constant mutation, target substitution, row deletion, or retroactive relabeling?

Verdict: yes. The base 35-row chain, CR119 finite particle vault, and CR128-CR134 generator suite replay from the locked primitive stack while preserving their source caveats.

Locked stack used:
- alpha_H = 2
- R = 12
- D = 3
- split fraction = 1/8
- surface debit = 3/4

Replay count:
- Checks: 65/65 PASS
- Replay layers: 13/13 PASS
- Wrong controls: 11/11 rejected
- CR119 particle table: 321 rows exported against summary count 321

Critical boundaries preserved:
- Known labels and observed masses are reveal-only, not construction inputs.
- qA and surface debit are grammar/debit terms, not direct mass values.
- Tensor carrier M=18 remains a carrier/support row, not matter.
- CR128-CR134 generator laws remain in-sample generator consistency unless separately marked forward-blind.
- Periodic/isotope replay is deferred to LC05.

Primary artifacts:
- `16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_particle_replay_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_generator_suite_register.csv`
- `16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_claim_boundaries.csv`
- `16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_checks.csv`
- `16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_sources_hashes.csv`
- `16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_summary.json`
