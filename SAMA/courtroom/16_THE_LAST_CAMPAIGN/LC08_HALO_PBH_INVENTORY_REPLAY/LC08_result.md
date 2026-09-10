# LC08 - Halo/PBH Inventory Replay

Result: **LC08_PASS_HALO_PBH_INVENTORY_REPLAY_FROM_LOCKED_PRIMITIVE_STACK**

Question: with the locked primitive stack promoted in LC01, does the halo/PBH inventory branch replay without promoting a successful config into a primitive law?

Verdict: yes. LC08 replays branch 08 as a scoped halo/PBH inventory support chain: cumulative nonzero A plus clustered BB-origin PBH/trapped-A carries the halo lane, post-BB/window PBH remains a small rejected full-halo control, hydrogen catches up inside the PBH/trapped-A scaffold, and the native radial law remains open.

Locked stack used:
- R = 12
- D = 3
- A0 = 1/(12*pi) = 0.026525823848649222628147293895

Core replay numbers:
- Omega_BB_PBH_trapped = 0.26446190430295646
- Omega_H_arrival_baryon = 0.049299011266100756
- total inventory = 1.0
- PBH/H ratio = 5.364446416084761
- SPARC galaxies = 175; mass-model points = 3391
- median outer dark fraction v2 = 0.760699023482704
- post-BB envelope supplied pct of dark residual = 2.576714268055339
- missing after post-BB envelope pct of dark residual = 97.42328573194466
- clustered profile median RMS = 3.625430524040301 km/s vs baryon RMS = 40.95236813050122 km/s
- clustered profile chi2 improvement = 150.7662388291606
- seed-first native R/12 gap closed = 0.8191375474184742
- uniform-control gap closed = 3.8495994978147876e-05
- post-BB-only-control gap closed = 0.02448481593940179

Trap controls rejected:
- Config-as-law rejected: R/6 is the best-RMS comparison row but is not promoted to primitive law.
- Smooth/uniform PBH conflation rejected: uniform gap closed is near zero; clustered-PBH-aware microlensing remains open.
- Post-BB-only-as-full-halo rejected: post-BB/window PBH supplies only 2.576714% of the dark residual.
- Full radial-law overclaim rejected: native radial organization, mass function, and concentration remain open.
- Stale governance wording rejected: CR116 supersedes the older CR115 bridge interpretation without modifying it.

Checks: 166/166 PASS
Wrong controls: 11/11 rejected

Primary artifacts:
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_replay_layers.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_formula_manifest.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_halo_replay_metrics.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_seed_candidate_rows.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_wrong_controls.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_claim_boundaries.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_checks.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_sources_hashes.csv`
- `16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_summary.json`
