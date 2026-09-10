# CR022 (08 Branch) — Appeal Upgrade Annotation

**Date sealed:** 2026-06-22
**Mechanism:** Courtroom Deferred-Support Appeal Rule (README.md, "Deferred-Support Appeal Rule")
**Annotation type:** Appended upgrade. Original CR022 BOUNDARY verdict is NOT erased.

## Original Branch Verdict (Preserved, Immutable)

```text
CR022_BOUNDARY_NATIVE_A_MANY_NONZERO_ACCUMULATION_ROOT
```

Original `CR022_result.md` sha256: `edd16d621fb17a5a7a2f04640d33ec09f800bae008f834956867ae63412370f3`

CR022 was sealed BOUNDARY because it is a structural-root test: the SAM V4.1 kernel was shown to admit many nonzero A contributions accumulating into a measurable halo-scale field, but the test itself had no standalone external contact. The BOUNDARY verdict was correct at the time of sealing.

## Premise Dependency

CR022 establishes the typed premise:

> Many nonzero A contributions accumulate into a measurable halo-scale field; a single 1e-18 contribution is below threshold, but many such contributions sum to ~1e-7 above threshold.

This premise becomes the typed input for every downstream halo-physics test in branch 08 and several cross-branch consumers. When those downstream tests achieve PASS using the premise, the original BOUNDARY can be appeal-upgraded under the Deferred-Support Appeal Rule.

## Downstream PASS Evidence

| Test ID | Branch | result.md sha256 | How it uses CR022's cumulative-A premise |
|---|---|---|---|
| CR024 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `8e9c97a2a9d23802a699198f2086c4655e69a4825299e8c69dea52340360a637` | Real SPARC 175-galaxy 76% outer dark residual measured; post-BB-only envelope supplies only 2.6% — establishes that cumulative-A (not any single-source) is required for halo closure |
| CR025 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `4846b72cb901fe862029fb663db2e42b9f3f885c2a5a6f94ef09d538529b33e5` | Clustered BB-PBH/trapped-A halo profile improves SPARC rotation-curve fit by factor 150.8× using cumulative-A summed contributions |
| CR026 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `65c17e77f8701c213f5af959092832fffda0d676a9cb33893552a73737a23ac8` | Base-12 outer-radius-over-12 seed-first clustering closes 81.9% baryon-to-profile gap; uniform A wrong control fails (3.85e-5), post-BB-only wrong control fails (0.0245) |
| CR027 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `42d6a2274d5b5a50ec807831791c61b5f926e83b6ffc520ec837a2557213f59f` | Hydrogen catchup first-star scaffold uses cumulative BB-PBH+trapped-A as the foundational scaffold (PBH:H ratio = 5.36) |
| CR030 | 08_GALAXY_HALOS_BB_PBH_TRAPPED_A | `9b6bf0056e59fe8e11d38a777ddc4b95202a533bf7583fa0c3fff92c99206b4a` | Branch 08 verdict zipper integrates cumulative-A across 4 PASS + 4 BOUNDARY tests |
| CR110 | 14_FOUNDATIONAL_TESTS | `6b63bacc9a2d7cf2afcc2f01149b0699a756b8da7249984bca00a57367c9e835` | Three-mode closure (Earth/Galaxy/PBH) explicitly built on per-body A + cumulative-A premise; zero new free parameters |
| CR116 | 00_governance | `d3f3204be9cbc5bbb9520664bdb937452981e494f38c6154266fffa95a04fd65` | Halo composition correction explicitly built on cumulative-A + clustered BB-PBH; supersedes CR110_PRED_2 reading |
| LC08 | 16_THE_LAST_CAMPAIGN | `51bc67735a8c45941f1493441b5e5c274419c963c07685fccb8b26c1ae6f8684` | 166/166 consistency checks pass under LC01-locked primitive stack; cumulative-A reproduces all downstream halo readouts with no mutation |

HASHES.txt files in the corresponding canonical_path folders carry the artifact-level integrity records.

## Appended Upgrade Verdict

```text
CR022@08_APPEAL_PASS_DEFERRED_SUPPORT__CUMULATIVE_A_PREMISE_VALIDATED_BY_DOWNSTREAM_PASS_CHAIN__NATIVE_RADIAL_LAW_DEBT_NOT_ADDRESSED_BY_THIS_UPGRADE
```

## Scope of This Upgrade (Honest Boundaries)

```text
upgrades         : the cumulative-A premise (many-nonzero accumulation into measurable halo field)
                   is validated by the downstream PASS chain listed above.

does NOT upgrade : the native radial law open debt (CR029@08), which LC08 explicitly preserves
                   ("native radial law open"). r(rho) form, concentration relation, and mass function
                   remain open by design.

does NOT erase   : the original CR022_BOUNDARY_NATIVE_A_MANY_NONZERO_ACCUMULATION_ROOT verdict.
                   That verdict remains the historical record. This annotation appends.

reversibility    : if any cited downstream PASS is later regraded BOUNDARY/FAIL/REFUTED, this
                   appeal annotation must be retracted or scoped.
```

## Provenance

Recorded during the 2026-06-22 `TEST_INDEX.csv` build pass per Sean Brady's directive to "use the index to see if we can honestly upgrade anything." The index resolved every cited downstream test to a current LIVE PASS row before this annotation was written. See `TEST_INDEX.csv` row `CR022,08_GALAXY_HALOS_BB_PBH_TRAPPED_A,APPEAL_UPGRADED,BOUNDARY,...`.
