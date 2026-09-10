# CR004 — SAM vs GR / Standard Discrimination Map

**Branch:** 21_GRAVITATIONAL_WAVES
**Mode:** EXPLORATORY (synthesis CR; cataloging existing sealed predictions)
**Sealed by:** Sean Brady, 2026-06-29
**Upstream:** CR001 PASS, CR002 PASS, CR003 PASS, CR003b STRONG_PASS
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Purpose

Catalog every substrate-derived numerical prediction that has been
sealed in the courtroom (GW branch and cross-domain), and tabulate
against the corresponding GR / Planck / PDG / catalog value. For each
row compute:

- the gap between SAM's closed-form value and the standard value
- the current measurement σ
- the future-detector σ projected to resolve the gap
- a testability score (`gap / future_σ`) that ranks rows by
  discrimination potential

Output: a ranked map identifying which substrate predictions are
already discriminating, which are queued for next-generation
detectors, and which are below any plausible measurement floor.

The top-ranked rows become the SAM-1919 candidate set — substrate
predictions waiting for sharper measurement to decide.

## What CR004 does NOT do

- Does not commit any prediction as "exact" — that derivation step
  is CR005.
- Does not run any new test against external data — uses sealed
  values from prior CRs and published standard values.
- Does not interpret rankings as proof — the testability score is
  a planning tool, not a verdict.

## Sources for SAM values (sealed)

All SAM values are pulled by hash from sealed courtroom artifacts:

| Domain | Source CRs | Hash provenance |
| --- | --- | --- |
| GW radiation cap (1/8) | CR001@21 | precommit `1e37ca0a…` |
| GW fundamental QNM | CR003@21 | precommit `ec90b992…` |
| GW higher-mode QNMs | CR003b@21 | precommit `9ed16b1e…` |
| Cosmology densities (Ω_m, Ω_b, Ω_c, Ω_Λ) | CR018@07, CR019@07, CR002@19 | sealed in master sheet |
| η_SAM, H_0_SAM | CR036@19 | precommit `345a1a8d…` |
| Perturbation triplet (A_s, n_s, τ) | CR037A@19 | precommit `1b7da85b…` |
| Higgs mass (125.25 GeV) | CR120b@09a + foundation | per master sheet |
| Proton mass (937.96 MeV) | CR009@18 | per master sheet |
| Halo asymptote X_∞ = 10/π | CR025/CR031b@08 | per master sheet |
| Neutrino selector (35 split ratio; Σm_ν 71.3 meV) | CR001@20 | precommit `8e6cb197…` |
| CMB compressed geometry (θ_*, ℓ_A, r_d) | CR019@06 | per master sheet |

## Sources for standard values (published)

| Reference | Use |
| --- | --- |
| Berti, Cardoso, Starinets 2009 (Living Rev Rel 12, 2) | Schwarzschild QNM dimensionless frequencies |
| Hemberger et al. 2013 (PRD 88, 064014) | binary-BH max radiated fraction NR limit |
| Planck 2018 base-ΛCDM TT,TE,EE+lowE+lensing (Aghanim et al. 2020) | Ω_m, Ω_b·h², H_0, A_s, n_s, τ |
| SH0ES (Riess et al. 2022) | H_0 distance-ladder anchor |
| PDG 2024 | Higgs mass, proton mass |
| SPARC galaxy rotation curves (Lelli et al. 2016) | halo asymptote X observed |
| NuFit 5.2 / PDG 2024 | neutrino splitting ratios, Σm_ν Planck bound |

## Sources for future-detector σ projections

| Instrument | Mission profile | Projected precision | Source |
| --- | --- | --- | --- |
| LISA | space; SMBH ringdowns | ~0.1% ω_R, ~0.5% ω_I at SNR > 1000 | Berti et al. 2016 Class. Quant. Grav. 33, 174002 |
| Einstein Telescope (ET) | ground; stellar-mass BBH/BNS | ~1% on QNM real, ~3% on damping | Maggiore et al. 2020 JCAP 03, 050 |
| Cosmic Explorer (CE) | ground; stellar-mass BBH/BNS | similar ET scale | Reitze et al. 2019 |
| CMB-S4 | ground CMB | Σm_ν σ ~30 meV | Abazajian et al. 2019 |
| DUNE | long-baseline ν | Δm²_31/Δm²_21 σ ~0.5% | DUNE TDR 2020 |
| Hyper-Kamiokande | ν oscillation | similar to DUNE | Abe et al. 2018 |
| ATLAS/CMS HL-LHC | LHC upgrade | Higgs mass σ ~50 MeV (~0.04%) | ATLAS/CMS HL-LHC projections 2019 |

## Testability score (closed-form)

For each row:

```text
gap_pct         = 100 · |SAM − standard| / standard
score_current   = gap_pct / current_σ_pct           (testable now if score > 3)
score_future    = gap_pct / future_σ_pct            (discriminating with future detector if score > 3)
status:
   ALREADY DISCRIMINATING : score_current > 3      (gap exceeds current σ)
   ALREADY TESTED, PASS   : score_current < 1 and gap matches  ← SAM is consistent with current data
   FUTURE-TESTABLE        : score_current < 1 and score_future > 3
   BELOW MEASUREMENT FLOOR: score_future < 1 even with best projected detector
```

## Verdict

CR004 produces a ranked table; the "verdict" is the table itself.
For workflow continuity:

```text
PASS: table is generated cleanly with all gates evaluated and rows
      ranked by testability. CR004 is a synthesis CR — output is
      the map, not a binary outcome.

FAIL: any row's SAM value contradicts a SEALED CR (data
      pull-through bug). Stop and audit.
```

## What CR004 opens

- **CR005**: substrate-physics derivation of the top-ranked
  FUTURE-TESTABLE prediction (likely Schwarzschild fundamental QNM
  ω_R·M = 3/8). Moves it from "substrate atom that hits within 0.36%"
  to "substrate-physics consequence." Required before any prediction
  can be formally locked as SAM's commitment.
- **CR006**: formal forecast lock for the LISA-era discrimination,
  with explicit σ thresholds and verdict criteria for the eventual
  measurement.
- **CR007+**: parallel CR per testable row in the ranked map.

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR001@21 | `1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805` |
| CR002@21 | `a42873eb1d3f68064c2d2540f93d6cc9f68f24c830daa36922240cab42733e18` |
| CR003@21 | `ec90b9924a12ae760bd3cefb550ad602be442114b8a26c36b0fb9c37f5998cd3` |
| CR003b@21 | `9ed16b1ebc02c8765db9ff3c307bf71380928ffb7954cb0bfb300a972d2703c5` |
| branch README | `1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595` |
| stewardship | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
