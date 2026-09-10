# LC09 - Quantum Pair-Write / Born-Rule Lane Replay

Result: **LC09_PASS_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY_FROM_LOCKED_PRIMITIVE_STACK**

Question: with the locked primitive stack promoted in LC01, does the quantum pair-write / Born-rule lane replay without normalization patch, threshold swap, final-outcome leakage, or route-identity collapse?

Verdict: yes. LC09 replays the live Branch 11 and quantum_phase surfaces through protected-route thresholds, Born-style route weights, pair-write probabilities, ledger commit, stable-mode selection, and the network Born surface while preserving the CR076 boundary and the missing-live-QN019/QN020 provenance boundary.

Locked stack used:
- R = 12
- D = 3
- A_side = 1/(2R) = 0.041666666666666664
- A_share = 1/R = 0.08333333333333333

Core replay numbers:
- QP014 route-weight rows = 49; probability-surface rows = 7
- QP014 max open normalization error = 1.1102230246251565e-16
- QP014 max closed probability error = 0.0
- QP015 bridge rows = 1176; sample summary rows = 42
- QP015 primary pair probability sum = 1.0
- QP016 stable/boundary/transient counts = 1/1/26
- QN005 network rows = 49; multi-node rows = 84; forbidden fields used = False
- live QN019/QN020 executed artifact files found = 0/0

Trap controls rejected:
- Normalization patch rejected: QP014 row weights normalize natively, and closed windows carry zero probability.
- Pair-factor deletion rejected: LC09 recomputes QP015 self/mixed pair probabilities from QP014 route probabilities.
- Final-outcome leakage rejected: QN005 surfaces report no forbidden final ledger fields.
- Threshold swap rejected: A_side and A_share derive from LC01 R=12.
- CR076 overpromotion rejected: explicit integral form remains open, so CR076 stays BOUNDARY.
- Stale QN019/QN020 provenance rejected: absent live executed folders are recorded as a boundary, not used as proof.

Checks: 96/96 PASS
Wrong controls: 9/9 rejected

Primary artifacts:
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_branch11_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_replay_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_formula_manifest.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_quantum_replay_metrics.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_qp014_probability_recompute.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_qp015_pair_probability_recompute.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_claim_boundaries.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_checks.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_sources_hashes.csv`
- `16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_summary.json`
