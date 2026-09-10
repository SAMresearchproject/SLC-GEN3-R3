# CR023 (08 Branch) — Appeal Upgrade Annotation

**Date sealed:** 2026-06-22
**Mechanism:** Courtroom Deferred-Support Appeal Rule (README.md, "Deferred-Support Appeal Rule")
**Annotation type:** Appended upgrade. Original CR023 BOUNDARY verdict is NOT erased.

## Original Branch Verdict (Preserved, Immutable)

```text
CR023_BOUNDARY_BB_PBH_TRAPPED_A_INVENTORY_CHAIN
```

Original `CR023_result.md` sha256: `99774fdb87e35e73fd370c120190e714d976a619104aa97258b8b0eb5f4db0fa`

CR023 was sealed BOUNDARY because the inventory chain it builds (Omega_PBH = 0.2645; PBH:H ratio = 5.36; post-BB subchannel = 0.0258, insufficient alone) lacks standalone external contact at the inventory level. The BOUNDARY verdict was correct at the time of sealing.

## Premise Dependency

CR023 establishes the typed premise:

> BB-origin PBH/trapped-A inventory is preserved as the dark-halo lane while post-BB-only PBH is rejected; Omega_PBH = 0.2645 dominates baryonic hydrogen by factor 5.36.

This inventory becomes the typed input for every downstream halo-composition test in branch 08, the three-mode closure in branch 14, the cosmic baryon bridge in 00_governance, and the LC06/LC08 consistency replays.

## Downstream PASS Evidence

| Test ID | Branch | result.md sha256 | How it uses CR023's BB-PBH inventory premise |
|---|---|---|---|
| CR024 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `8e9c97a2a9d23802a699198f2086c4655e69a4825299e8c69dea52340360a637` | Real SPARC residual analysis explicitly rejects post-BB-only as full halo source; rests on CR023's BB-origin PBH+trapped-A inventory chain |
| CR025 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `4846b72cb901fe862029fb663db2e42b9f3f885c2a5a6f94ef09d538529b33e5` | Clustered BB-PBH/trapped-A halo profile fit uses CR023 BB-origin inventory; median overdensity 79090× cosmic mean |
| CR026 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `65c17e77f8701c213f5af959092832fffda0d676a9cb33893552a73737a23ac8` | Seed-first clustering selector uses CR023 BB-origin inventory; uniform and post-BB-only controls rejected |
| CR027 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `42d6a2274d5b5a50ec807831791c61b5f926e83b6ffc520ec837a2557213f59f` | Hydrogen catchup first-star scaffold uses CR023's PBH:H = 5.36 ratio as the load-bearing scaffold dimension |
| CR030 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `9b6bf0056e59fe8e11d38a777ddc4b95202a533bf7583fa0c3fff92c99206b4a` | Branch 08 verdict zipper integrates the BB-PBH inventory chain across 4 PASS + 4 BOUNDARY tests |
| CR110 | 14_FOUNDATIONAL_TESTS | `6b63bacc9a2d7cf2afcc2f01149b0699a756b8da7249984bca00a57367c9e835` | Three-mode closure derives PBH f_PBH << 1 structurally from CR023 inventory premise |
| CR114 | 00_governance | `e2f394b40768bc45d916427e7031066cb23e24298e0e4337c3c5bcd4715549c6` | Cosmic baryon bridge retroactively built on CR018@07 ↔ CR023@08 inventory chain |
| CR116 | 00_governance | `d3f3204be9cbc5bbb9520664bdb937452981e494f38c6154266fffa95a04fd65` | Halo composition correction explicitly uses CR023 inventory; user-caught misread in CR110_PRED_2 corrected |
| LC06 | 16_THE_LAST_CAMPAIGN | `bb19a31ef74c8a68627c678dfbbed8971e059f44b1a78b47f64462926b6ccaad` | 58/58 consistency checks under LC01-locked primitives; CR023 BOUNDARY_PASS preserved; baryon-split + 126-row matter inventory replayed |
| LC08 | 16_THE_LAST_CAMPAIGN | `51bc67735a8c45941f1493441b5e5c274419c963c07685fccb8b26c1ae6f8684` | 166/166 checks pass; clustered BB-PBH/trapped-A carry halo per CR023 inventory; post-BB-only envelope (2.577% of dark residual) rejected as full source |

HASHES.txt files in the corresponding canonical_path folders carry the artifact-level integrity records.

## Appended Upgrade Verdict

```text
CR023@08_APPEAL_PASS_DEFERRED_SUPPORT__BB_PBH_TRAPPED_A_INVENTORY_VALIDATED_BY_DOWNSTREAM_PASS_CHAIN__NATIVE_RADIAL_LAW_DEBT_NOT_ADDRESSED_BY_THIS_UPGRADE
```

## Scope of This Upgrade (Honest Boundaries)

```text
upgrades         : the BB-origin PBH/trapped-A inventory premise (PBH:H = 5.36 / Omega_PBH = 0.2645
                   / post-BB-only insufficient alone) is validated by the downstream PASS chain.

does NOT upgrade : the native radial law open debt (CR029@08). LC08 R/6 best-RMS is explicitly
                   NOT promoted to law. Mass function and concentration relation remain open.

does NOT upgrade : full CMB closure (CR020-CR023@07 remain BOUNDARY by design; LC06 preserves
                   "CMB / recombination / perturbation / Planck closure remain open").

does NOT erase   : the original CR023_BOUNDARY_BB_PBH_TRAPPED_A_INVENTORY_CHAIN verdict. That
                   verdict remains the historical record. This annotation appends.

reversibility    : if any cited downstream PASS is later regraded BOUNDARY/FAIL/REFUTED, this
                   appeal annotation must be retracted or scoped.
```

## Provenance

Recorded during the 2026-06-22 `TEST_INDEX.csv` build pass per Sean Brady's directive to "use the index to see if we can honestly upgrade anything." The index resolved every cited downstream test to a current LIVE PASS row before this annotation was written. See `TEST_INDEX.csv` row `CR023,08_GALAXY_HALOS_BB_PBH_TRAPPED_A,APPEAL_UPGRADED,BOUNDARY,...`.
