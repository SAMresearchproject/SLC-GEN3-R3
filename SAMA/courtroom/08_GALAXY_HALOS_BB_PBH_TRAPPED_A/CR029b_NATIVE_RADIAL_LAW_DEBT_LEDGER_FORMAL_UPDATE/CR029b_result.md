# CR029b -- Native Radial-Law Debt Ledger Formal Update -- RESULT

```text
verdict           : PASS
classification    : LEDGER_UPDATE_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-29
precommit_hash    : 04fd7e43cfade5d257af35f04ff8211c050ef72f15987b300619ee7a05986b44
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
supersedes for downstream citation : CR029 BOUNDARY (preserved bit-for-bit)
```

## Headline

After CR031b (radial organization), CR032 (per-galaxy mass placement),
and CR033 (X_inf substrate identity) sealed downstream of CR029, three
of the four open items the CR029 debt ledger isolated are now closed at
the population level with zero free parameters in each. Per-galaxy
scatter and the prospective non-SPARC catalog test (CR034) remain
explicitly open.

CR029 itself is preserved bit-for-bit. CR029b is the formal update that
should be cited downstream where the radial-law ledger is referenced.

## Gate-by-gate

| gate | claim | result |
| --- | --- | :--- |
| G1 | radial organization law closed at population level | PASS |
| G2 | mass-function placement closed at population median | PASS |
| G3 | X_inf substrate identity closed retrospectively | PASS |
| G4 | open items honestly itemized in result.md | PASS |
| G5 | precommit hash verified at runner load | PASS |
| G6 | forbidden-file open() guard not tripped | PASS |

## Sealed numbers read from frozen downstream summaries

```text
CR031b@08  verdict           : PASS
           canonical Upsilon_disk = 0.5 (canonical)
           P4 WC3 within-galaxy shuffle p-value = 0.000999  (< 0.01)
           P5 WC4 galaxy-normalized null p-value = 0.000999  (< 0.01)
           canonical endpoint_diff = +1.9712
           outer plateau median X = 3.1225

CR032@08   verdict           : PASS
           X_inf sealed       = 3.18  (from CR025; confirmed CR031b)
           median linear ratio (predicted / measured halo mass) = 0.998311
           |median log10 ratio| = 7.342827e-04
           band                 = [0.891, 1.122]
           n_in_median          = 173/175
           per-galaxy scatter   std(log10 ratio) = 0.3791 dex

CR033@08   verdict           : PASS
           X_inf_SAM formula  : (R - alpha_H) * Omega_m = 10/pi
           X_inf_SAM value    : 3.183098861837907
           |median log10 ratio| = 3.112754e-04  (threshold 0.05)
           empirical_X_inf_input    = False
           per_galaxy_fitting       = False
           prior_CR_result_inputs   = False
           forbidden_files_opened   = False
           three substrate forms (R-alpha_H), (S+alpha_H), (Theta-S) all = 10 : True
```

## What CR029 declared open

CR029 result.md, line 44, "radial_law_debt_declared":

> "native radial organization law / mass function / concentration relation"

plus the implicit X_inf identity referenced by the CR029 downstream chain.

## What is now closed (population level)

| CR029 debt item | closed by | how |
| --- | --- | --- |
| native radial organization law | CR031b@08 | X(r) monotonic rise to plateau, p < 0.001 vs two null distributions, canonical Upsilon = 0.5 |
| mass function placement | CR032@08 | M_halo(<R_outer) = R_outer X_inf V_bar^2 / G with X_inf sealed = 3.18; median linear ratio = 0.9983, 68x under 0.05 threshold |
| X_inf substrate identity | CR033@08 | (R - alpha_H) Omega_m = 10/pi reproduces raw-SPARC median to abs(med log10) = 3.1e-4; forbidden-file guard not tripped |

Three of four debt items, each at zero free parameters.

## Open Items (verbatim from CR029b precommit)

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

## Verdict statement

CR029b PASS (formal update). The four-item debt ledger isolated by
CR029 is now closed at the population level on three of four items by
sealed downstream CRs CR031b, CR032, CR033, with zero free parameters in
each. The remaining open items (per-galaxy scatter at ~0.38 dex,
CR034 prospective non-SPARC catalog test, closed-form concentration
selector, cross-catalog universality) are itemized verbatim above. The
ledger is updated; CR029 itself is preserved bit-for-bit.

CR029b is the citation target for downstream references to the
radial-law debt ledger.

`CR029b_PASS_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE_THREE_OF_FOUR_OPEN_ITEMS_CLOSED_AT_POPULATION_LEVEL_BY_CR031B_CR032_CR033_REMAINING_OPEN_PER_GALAXY_SCATTER_CR034_PROSPECTIVE_AND_CONCENTRATION_SELECTOR`
