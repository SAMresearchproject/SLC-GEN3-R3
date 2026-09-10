# LC10 - Quantum Information Thresholds Replay

Result: **LC10_PASS_QUANTUM_INFORMATION_THRESHOLDS_REPLAY_FROM_LOCKED_PRIMITIVE_STACK**

Question: with the locked primitive stack promoted in LC01, do the quantum information thresholds replay without threshold swap, hardware-threshold substitution, or Born-measurement overclaim?

Verdict: yes. LC10 replays the threshold stack from R=12, D=3, and alpha_H=2: A_side=1/24, A_share=1/12, the q=0 Paul Revere letter increment 1/16, loaded probabilities (4/17, 9/17, 4/17), and the multi-letter capacity ceiling 1/8. The known hardware-table regrades are preserved as boundaries and are not load-bearing.

Locked threshold stack:
- A_side = 1/24 = 0.041666666666666664
- A_share = 1/12 = 0.08333333333333333
- letter increment = 1/16
- loaded weights = (1/4, 9/16, 1/4) with sum 17/16
- loaded probabilities = (4/17, 9/17, 4/17) with sum 1
- capacity ceiling = 2^-D = 1/8

Core replay numbers:
- CR060a alphabet rows = 300; promoted symbols = 300
- CR061a ideal candidates = 2
- CR066a ratio P_b/P_a = 9/4; P_b-P_a = 5/17
- CR067a capacity rows = 20; N=8 fraction of channel = 99.609375%
- CR068a A_leak at alarm = 0.041919263144548635 (< A_share 0.08333333333333333)
- CR063a status = CR063a_HARDWARE_TRANSLATION_V1_REFUTED_BY_TRANSMON_T2_CONTACT_RESCUED_BY_CR064a_V1_1
- CR064a status = CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1_BOUNDARY_PENDING_CITATION_VERIFICATION_AND_GATE_RATE_ARTIFACT_DISCLOSURE
- CR069a violations = 1; verified rows = 0

Trap controls rejected:
- Threshold swap rejected: A_side and A_share are R-derived and cannot be replaced by hardware fault-tolerance/T2 thresholds.
- Born-rule modification rejected: 17/16 is a surface-debit loaded-weight sum; measurement probabilities still sum to one.
- Mini 1:2:1 packet rejected: CR066b preserves the center-only bridge lift.
- Linear/parallel/full-unity capacity controls rejected: CR067a locks geometric scaling to the 1/8 ceiling.
- Hardware overpromotion rejected: CR063a/CR064a/CR069a are boundary records, not threshold proofs.

Checks: 116/116 PASS
Wrong controls: 10/10 rejected

Primary artifacts:
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_branch12_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_branch12a_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_threshold_manifest.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_formula_manifest.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_information_recompute.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_capacity_recompute.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_claim_boundaries.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_checks.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_sources_hashes.csv`
- `16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_summary.json`
