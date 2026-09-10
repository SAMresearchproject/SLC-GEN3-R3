# CR031_X_RADIAL_LAW_POPULATION_TEST

## Verdict

```text
CR031_BOUNDARY_X_RADIAL_LAW_SIGNAL_CONFIRMED_NEGATIVE_CONTROLS_BELOW_95_PCT_THRESHOLD
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
claim_tier = SUBSTRATE_RADIAL_LAW_SIGNAL_CONFIRMED__NEGATIVE_CONTROL_KILL_THRESHOLD_OPEN
free_parameters_introduced = 0
precommit_sha256 = 01797081265fdc072b233dfed413c38374a8a27f4ef6c02bcf1740623ea42b05
```

## Question

```text
Does X(r) = V_dark^2(r) / V_bar^2(r), computed at every measured SPARC radius
across all 175 galaxies and binned in r/R_outer, rise monotonically from a
baryon-dominated inner regime to a bound-halo plateau matching the sealed
CR025 reference, with cross-galaxy convergence at the outer edge, under
canonical Lelli mass-to-light ratios and zero per-galaxy fitting?
```

## Sealed Predictions — Canonical Upsilon = 0.5

| prediction | result | evidence | pass |
|---|---|---|---:|
| P1 monotonic rise | endpoint_diff = +1.971, Spearman = +1.000, adjacent rises = 4/4 | bin_medians: 1.151, 1.727, 2.422, 2.683, 3.122 | true |
| P2 outer plateau in [2.5, 4.5] and < 4.56 cosmic cap | outer median = 3.122 | within [2.5, 4.5] and below 4.5594 cap | true |
| P3 cross-galaxy convergence | spread_endpoint_diff = -0.218, adjacent decreases = 4/4 | log10_X spread: 0.614, 0.448, 0.435, 0.404, 0.396 | true |

## Wrong Controls

### Soft controls (must hold under WC1, WC2)

| control | description | P1 holds | P3 holds | pass |
|---|---|---:|---:|---:|
| WC1 | Upsilon_disk = 0.3 | true | true | true |
| WC2 | Upsilon_disk = 0.7 | true | true | true |

### Hard kill controls (P1/P3 must fail in >= 95% of trials)

| control | description | n_trials | fail_fraction | threshold | pass |
|---|---|---:|---:|---:|---:|
| WC3 | within-galaxy shuffle of (V_obs, V_gas, V_disk, V_bul) across R | 1000 | 0.839 | 0.95 | false |
| WC4 | galaxy-randomized rho = uniform(0,1) replacement | 1000 | 0.808 | 0.95 | false |

## Pass Conditions

| condition | pass |
|---|---:|
| P1_canonical | true |
| P2_canonical | true |
| P3_canonical | true |
| WC1_P1 | true |
| WC1_P3 | true |
| WC2_P1 | true |
| WC2_P3 | true |
| WC3_kill (>= 95% of trials destroy P1) | false |
| WC4_kill (>= 95% of trials destroy P3) | false |

## Evidence Rows

| item | value |
|---|---:|
| n_galaxies_loaded | 175 |
| n_radial_points_loaded | 3391 |
| canonical_median_X_bin_0.0-0.2 | 1.1513 |
| canonical_median_X_bin_0.2-0.4 | 1.7271 |
| canonical_median_X_bin_0.4-0.6 | 2.4224 |
| canonical_median_X_bin_0.6-0.8 | 2.6832 |
| canonical_median_X_bin_0.8-1.0 | 3.1225 |
| canonical_log10X_spread_bin_0.0-0.2 | 0.6137 |
| canonical_log10X_spread_bin_0.2-0.4 | 0.4477 |
| canonical_log10X_spread_bin_0.4-0.6 | 0.4347 |
| canonical_log10X_spread_bin_0.6-0.8 | 0.4042 |
| canonical_log10X_spread_bin_0.8-1.0 | 0.3960 |
| canonical_nonpos_X_count_bin_0.0-0.2 | 173 |
| canonical_nonpos_X_count_bin_0.2-0.4 | 22 |
| canonical_nonpos_X_count_bin_0.4-0.6 | 8 |
| canonical_nonpos_X_count_bin_0.6-0.8 | 6 |
| canonical_nonpos_X_count_bin_0.8-1.0 | 5 |
| P1_endpoint_diff | 1.9712 |
| P1_spearman | 1.0000 |
| P1_adjacent_rises_of_4 | 4 |
| P2_outer_median | 3.1225 |
| P3_spread_endpoint_diff | -0.2177 |
| P3_adjacent_decreases_of_4 | 4 |
| WC1_P1_passed | true |
| WC2_P1_passed | true |
| WC3_P1_fail_fraction | 0.839 |
| WC4_P3_fail_fraction | 0.808 |
| WC3_kill_threshold | 0.95 |
| WC4_kill_threshold | 0.95 |

## Reference Comparison

```text
inner-bin median X      = 1.151    vs   ~1.0 N=Z baryon reference (CR240)
outer-bin median X      = 3.122    vs   3.18 CR025 sealed SPARC outer median
                                    vs   5.36 CR023 sealed cosmic Omega_PBH/Omega_b
cosmic-X separation     = 3.122 / 5.364 = 0.582 (bound-halo strictly below cosmic)
```

## Scope

```text
CR031 is a sealed test of the substrate-derived X = Q_sub/Q_matter framing
applied as a radial-organization law to the SPARC galaxy rotation curve
population. The canonical analysis confirms P1 (monotonic rise), P2 (outer
plateau matching the CR025 sealed value), and P3 (cross-galaxy convergence
at the outer edge). The mass-to-light bracket controls WC1 and WC2 confirm
that the signal is not an artifact of the canonical Lelli Upsilon choice.

The hard kill controls WC3 and WC4 fail their 95-percent fail-fraction
threshold (observed 83.9 percent and 80.8 percent respectively). The
verdict is therefore BOUNDARY rather than PASS.
```

## Rule-9 Line

```text
This test could have falsified the claim that X(r) rises monotonically with
radius across the 175-galaxy SPARC population to a bound-halo plateau matching
the CR025 sealed reference, with cross-galaxy convergence at the outer edge,
under canonical Lelli mass-to-light ratios. The canonical, Upsilon-bracket
contents of that claim are confirmed. The 95-percent negative-control kill
threshold on within-galaxy shuffle and galaxy-randomized rho was not met.
```

## Connection to CR029

```text
CR029 isolated branch 08's remaining debt as the native radial organization
law / mass function / concentration relation. CR031 tests the radial
organization piece. The canonical signal confirms the radial-organization
structure substrate-derivedly without per-galaxy fitting; the BOUNDARY
verdict reflects the kill-threshold gap and does not retire CR029.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon          = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
Precommit             = 01797081265fdc072b233dfed413c38374a8a27f4ef6c02bcf1740623ea42b05
```

---

**Sealed by:** Sean Brady, 2026-06-26.
