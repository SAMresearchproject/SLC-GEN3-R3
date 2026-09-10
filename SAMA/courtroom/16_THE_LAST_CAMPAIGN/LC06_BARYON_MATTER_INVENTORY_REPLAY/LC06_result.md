# LC06 - Baryon And Matter Inventory Replay

Result: **LC06_PASS_BARYON_AND_MATTER_INVENTORY_REPLAY_FROM_LOCKED_PRIMITIVE_STACK**

Question: with the locked primitive stack promoted in LC01, do the baryon split and matter inventory replay without carrier/matter mixing, target substitution, row deletion, or retroactive relabeling?

Verdict: yes. CR018/CR019 replay the baryon and effective-matter inventory from the locked stack, and CR119 preserves a 126-row matter table while rejecting tensor-carrier promotion and the QP093A-0088 null-conjugate trap.

Locked stack used:
- alpha_H = 2
- R = 12
- D = 3
- carrier side = 1/8
- retained side = 7/8

Baryon replay:
- A0 = 0.026525823848649222628147293895
- mu_H = 2.666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666667
- chi = 0.07073553026306459367505945038666666666666666666666666666666666666666666666666666666666666666666666668
- Omega_b = 0.04929901126610075001763238544901754615806281489273864388786666666666666666666666666666666666666666666
- Omega_m_eff = 0.3137609155690572
- Omega_BB_PBH_trapped = 0.26446190430295646
- Omega_substrate_vacuum = 0.6862390844309427

Matter inventory replay:
- Checks: 58/58 PASS
- Matter rows: 126/126
- Stable single-write rows: 63/63
- Bound composite rows: 63/63
- Antimatter rows included: 0
- qA split max Decimal error: 1E-96
- M_observed identity max Decimal error: 0.00
- Wrong controls: 10/10 rejected

Critical boundaries preserved:
- Tensor carrier M=18 remains carrier-only, not matter/rest mass.
- QP093A-0088 remains the null conjugate boundary row: M_native=18, S_debit=18, M_observed=0, qA=0, no matter promotion.
- qA source support is routed through carrier compression and ledger/A readout, not direct mass.
- CR023 remains BOUNDARY_PASS: full CMB, recombination, perturbation, TT/TE/EE, Planck likelihood, and distance-triad closure remain open.
- Governance CR114 is retroactive bridge provenance for CR111, not a fresh forward-blind claim.

Primary artifacts:
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_replay_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_baryon_cosmology_replay.csv`
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_matter_inventory_invariants.csv`
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_claim_boundaries.csv`
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_checks.csv`
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_sources_hashes.csv`
- `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_summary.json`
