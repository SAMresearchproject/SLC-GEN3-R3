# CR029b — Native Radial-Law Debt Ledger Formal Update

**Branch:** 08_GALAXY_HALOS_BB_PBH_TRAPPED_A
**Classification:** LEDGER_UPDATE_CR (formal update of CR029 BOUNDARY ledger)
**Supersedes for downstream citation:** CR029 (CR029 itself is preserved bit-for-bit)
**Sealed by:** Sean Brady, 2026-06-29
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Test Type

```text
Ledger-update CR. Re-reads only frozen sealed summary.json files from
already-sealed CRs (CR029, CR031b, CR032, CR033) and applies the verdict
logic declared below. No new measurement or fit. No catalog data read.
The forbidden-file open() guard installed at runner startup will trip
if any non-whitelisted file is opened.

This is the formal update CR029 explicitly named as pending in its own
result and in the branch README ("CR029 remains preserved as the original
BOUNDARY debt ledger until a formal CR029 appeal/update is sealed").
```

## Question

```text
After CR031b, CR032, and CR033 have sealed downstream of CR029, which of
the four debt items CR029 isolated as open ("native radial organization
law", "mass function", "concentration relation", "X_inf identity") are
closed at the population level, and which remain explicitly open?
```

## CR029's Open List (from CR029 result.md, line 44)

```text
debt declared: "native radial organization law / mass function /
                concentration relation"
plus the implicit X_inf identity referenced by CR029's downstream chain.
```

## Downstream Closures Under Test (frozen sealed summaries)

```text
1. CR031b@08 (sealed PASS, 2026-06-26)
   - claim: X(r) = V_dark^2 / V_bar^2 rises monotonically across SPARC,
     reaches outer plateau at the CR025 reference X_inf = 3.18, and
     beats null distribution at exact permutation p < 0.001 on both
     within-galaxy shuffle (WC3) and galaxy-randomized normalization
     (WC4) nulls.
   - free_parameters_introduced = 0
   - closes: "native radial organization law" at population level

2. CR032@08 (sealed PASS, 2026-06-26)
   - claim: M_halo(<R_outer) = R_outer * X_inf * V_bar^2 / G with
     X_inf = 3.18 sealed and zero per-galaxy fitting reproduces SPARC
     measured halo mass at median 0.9983 (|median log10| = 0.00073;
     68x under 0.05 threshold).
   - additionally reports c_SAM concentration distribution (median 1.063)
     as a substrate-native concentration scale without NFW fit.
   - free_parameters_introduced = 0
   - closes: "mass function" placement at population median AND provides
     a parameter-free concentration scale (concentration item provided,
     not closed by selector formula)

3. CR033@08 (sealed PASS, 2026-06-27)
   - claim: X_inf,SAM = (R - h_hat) * Omega_m = 10/pi = 3.1831 reproduces
     raw-SPARC outer-radius halo-mass population median to within +/- 12%
     (actual: |median log10| = 0.000311, ~160x under threshold).
   - retrospective substrate-identification; forbidden-file guard did
     not trip.
   - free_parameters_introduced = 0
   - closes: "X_inf identity" at the substrate-derivation level
     (retrospective on SPARC; prospective owed to CR034)
```

## Verdict Logic

```text
For each of the four debt items declared by CR029, mark closure status
strictly from the frozen sealed summary.json files of the three CRs
above (no narrative interpretation, no new data):

  radial_organization_law_closed_at_population_level :=
      (cr031b.scientific_verdict == "PASS"
       AND cr031b.p_value_wc3 < 0.01
       AND cr031b.p_value_wc4 < 0.01
       AND cr031b.free_parameters_introduced == 0)

  mass_function_placement_closed_at_median :=
      (cr032.scientific_verdict == "PASS"
       AND cr032.median_linear_ratio in [0.891, 1.122]
       AND cr032.free_parameters_introduced == 0
       AND cr032.per_galaxy_fitting == false)

  x_inf_identity_closed_retrospectively :=
      (cr033.scientific_verdict == "PASS"
       AND abs(cr033.median_log10_ratio) <= 0.05
       AND cr033.empirical_X_inf_input == false
       AND cr033.free_parameters_introduced == 0
       AND cr033.forbidden_files_opened == false)

  concentration_provided := cr032 reports c_SAM distribution.

The concentration RELATION (a closed-form selector formula tying
concentration to substrate atoms galaxy by galaxy without R_outer being
read per galaxy) is NOT closed; CR032 provides a c_SAM distribution
that uses R_outer as a measured input.
```

## Sealed PASS Gates

```text
PASS (formal update):
  G1. radial_organization_law_closed_at_population_level == True
  G2. mass_function_placement_closed_at_median            == True
  G3. x_inf_identity_closed_retrospectively               == True
  G4. open items honestly itemized in result.md and NOT promoted to
      closed by this ledger update.
  G5. precommit hash verified at runner load.
  G6. forbidden_file_open guard not tripped.

BOUNDARY:
  Any one of G1, G2, G3 evaluates False under its own sealed-summary
  check (would mean the ledger update is premature relative to actual
  downstream evidence).

FAIL:
  Hash mismatch, forbidden-file guard trips, or runner spec error
  (e.g. cited sealed value cannot be reproduced from the summary.json).
```

## Open Items After This Update (must appear in result.md verbatim)

```text
O1. Per-galaxy scatter of the CR032 mass-placement result remains
    ~0.38 dex (E1 of CR032). Closed is the POPULATION median, NOT a
    per-galaxy mass prediction. No claim is made on the
    radial-acceleration relation (RAR-grade tightness).

O2. Prospective confirmation of X_inf = 10/pi against a rotation-curve
    catalog SAM has never seen (THINGS or LITTLE THINGS) is registered
    as CR034@08 and NOT YET RUN. Until CR034 is sealed, the X_inf
    identity is closed retrospectively on SPARC, not prospectively.

O3. The closed-form concentration-selector formula (c as a function of
    substrate atoms alone, with no per-galaxy R_outer read) remains
    open. CR032 provides a c_SAM distribution that USES R_outer per
    galaxy; the parameter-free 1/12 in r_c = R_outer/12 is structurally
    motivated but does not yet remove the per-galaxy R_outer column.

O4. Cross-catalog universality of the X(r) population law (CR031b is
    SPARC-only) is owed to CR034 alongside O2.
```

## Pre-Registered Frozen Inputs

| field | path |
| --- | --- |
| cr029_summary | `08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER\CR029_summary.json` (or the result.md fallback if summary absent) |
| cr031b_summary | `08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL\CR031b_summary.json` |
| cr032_summary | `08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION\CR032_summary.json` |
| cr033_summary | `08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY\CR033_summary.json` |

The runner whitelists exactly these four read paths plus this precommit
file and the runner source. Any other open() call trips the forbidden-
file guard and forces FAIL.

## Rule-9 Line

```text
This test could have falsified the claim that CR029's four declared
open items are now closed at the population level by the sealed
downstream CRs CR031b, CR032, and CR033 — by any one of those CRs not
satisfying the closure predicate declared above when read from its own
frozen sealed summary.
```

## What This CR Seals

A formal update to the radial-law debt ledger: three of the four CR029
open items are closed at the population level by sealed downstream CRs
with zero free parameters in each; the remaining open items (per-galaxy
scatter, prospective non-SPARC catalog, closed-form concentration
selector) are itemized so the branch can carry its open work honestly
into Volume I and the patent register.

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR029@08 (preserved BOUNDARY) | per `BRANCH_HASHES.txt` |
| CR031b@08 (sealed PASS) | precommit `52e724ab54c7254716553408744871004219d399f90a2fdbef7769b40a0ad20c` |
| CR032@08 (sealed PASS) | precommit `a0af5e891c5e8f2448e26ead9c9aa80686529f3eb8328db2e7c2b615d898533e` |
| CR033@08 (sealed PASS) | precommit `fac85ca9decf0c724591bd95bf083630c49f95624c00cff5820b67824e1cf810` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
