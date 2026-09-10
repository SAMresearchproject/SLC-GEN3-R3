# LC07 - SN/BAO Distance Road Replay

Result: **LC07_PASS_SN_BAO_DISTANCE_ROAD_REPLAY_FROM_LOCKED_PRIMITIVE_STACK**

Question: with the locked primitive stack promoted in LC01, does the SN/BAO distance road replay without D refit, bin cherry-pick, target substitution, or formula mutation?

Verdict: yes. LC07 replays branch 06 from the locked stack at D=3, recomputes the SN row identities and BAO window/projection rows, preserves the independent-ledger overlap as a witness only, and keeps CMB modal/polarization closure open.

Locked stack used:
- R = 12
- D = 3
- A0 = 1/(12*pi) = 0.026525823848649222628147293895
- A_inf = A0*R = 0.3183098861837907

Core replay numbers:
- w = 0.0466031311731253
- r_drag = 150.92186401518705 Mpc
- SN rows = 1701; max_mu_error = 7.105427357601002e-15
- BAO rows = 19; rms_pull = 0.8269872776835621; rows_over_3sigma = 0
- SN/BAO same-z identity error = 0.0
- SN/BAO max overlap pct abs = 0.24000025506268896
- theta100 = 1.038976065435997; residual_pct = -0.2030501266944362

Trap controls rejected:
- D refit rejected: LC01/CR115 lock D=3; SN D2_power and BAO_D2 controls fail.
- Bin cherry-pick rejected: all 1701 SN rows and all 19 BAO rows are replayed.
- Target substitution rejected: Planck theta and observed SN/BAO values are downstream comparisons, not formula sources.
- Shared-data leak rejected: SN and BAO ledgers are built separately before overlap is checked.
- Overlap overclaim rejected: 0.240000255% is a local overlap witness, not a global all-z residual.

Checks: 113/113 PASS
Wrong controls: 10/10 rejected

Primary artifacts:
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_replay_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_formula_manifest.csv`
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_distance_replay_metrics.csv`
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_claim_boundaries.csv`
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_checks.csv`
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_sources_hashes.csv`
- `16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_summary.json`
