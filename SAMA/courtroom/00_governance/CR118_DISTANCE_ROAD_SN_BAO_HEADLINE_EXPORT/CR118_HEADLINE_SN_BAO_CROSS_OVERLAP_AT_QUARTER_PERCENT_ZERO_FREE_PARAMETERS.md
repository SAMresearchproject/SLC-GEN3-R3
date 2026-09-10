# SAM Distance Road - Headline Export Claim

## One Line

> Two independent observational ledgers (SN luminosity, 1701 Pantheon rows; > BAO ruler projection, 19 rows) are built without sharing data AND independently > reduce to the same A_los(z) with **zero free parameters**; their cross-overlap > is **0.240%**.

## The Numbers

### Structural constants (CR012, all derived from A0 = 1/(12π))

```text
A0     = 0.026525823848649224   (= 1/(12*pi), structural)
A_inf  = 0.318309886183790691   (= 1/pi, structural)
w      = 0.046603131173125298
r_drag = 150.921864 Mpc (derived, not fit)
```

### Two independent observational lanes

| ledger | rows | source | identity error | shrinkage signature |
|---|---|---|---|---|
| **SN luminosity** (CR013) | **1701** | Pantheon | max mu error = 7.11e-15 | low-z A = 0.0062; high-z A = 0.2927 |
| **BAO ruler projection** (CR014) | **19** | BAO compilation | max prediction error = 0.0 | rms pull = 0.8270; max abs pull = 1.4298; rows over 3 sigma = **0** |

### Cross-overlap (CR015)

```text
max_overlap_pct_abs    = 0.240000    ->   0.240%
max_identity_error     = 0.0
CR013 bao_inputs_not_loaded   = True   (SN ledger does not read BAO data)
CR014 sn_inputs_not_loaded    = True   (BAO ledger does not read SN data)
CR015 independent_ledger_functions_defined_before_overlap = True
CR015 overlap_not_formula_source = True
```

### r_drag comparison to Planck 2018 baseline

```text
SAM derived r_drag      = 150.9219 Mpc  (from A0 + w, zero fit parameters, no CMB data)
Planck 2018 baseline    = 147.0500 Mpc  (from CMB fit)
delta vs Planck         = +2.6330%  (without ever touching CMB)
```

## Why This Is Structurally Stronger Than LCDM

- LCDM closes SN+BAO+CMB jointly with ~6 fit parameters (omega_b_h2, omega_c_h2, H0, tau, n_s, A_s/sigma_8); SAM distance road closes SN and BAO at the data with zero free parameters
- SAM r_drag = 150.92 Mpc is DERIVED from A0=1/(12pi) + w; Planck baseline r_drag = 147.05 Mpc differs by +2.63% without touching CMB data
- two physically distinct observation classes (Type Ia SN luminosity distance vs BAO sound-horizon ruler) agree at 0.240% on cross-overlap rows - that is a near-identity, not a fit
- the lightspeed adjustment c_eff(z) ties both ledgers to the same A_los(z); synchronization of SN and BAO is the structural signature, not an LCDM-style decorrelated parameter fit

## Honest Scope Boundaries

- CR017 explicitly notes cmb_modal_polarization_left_open - this distance road closure is BACKGROUND-level (settles A_los(z)), not CMB-perturbation-level
- BAO compilation row count is 19 (compilation-grade), not the full LSST/DESI catalog - a future high-row BAO intake would strengthen the test
- the 0.240% cross-overlap is on rows where SN and BAO share redshifts, not a global all-z statement; non-overlap z extrapolation is open
- CR117 names the CMB initial-condition handoff that completes the cosmological closure - branch 06 closes the distance road; CMB-IC intake closes the perturbation layer

## The Underlying Mechanism

Both ledgers depend on the same line-of-sight A field A_los(z) and on the same redshift-dependent effective lightspeed `c_eff(z)`.  Standard cosmology gets SN luminosity distance and BAO angular-diameter distance from background expansion via decoupled parameters; in SAM they pick up the same `c_eff(z)` and the same A_los(z), so when both are computed from sealed structural constants they end up at the same value where they share redshifts.  The 0.240% cross-overlap is the empirical signature of that synchronization.

## Connection to Other Closures on the Public Record

- **CR114** closes Omega_b at sigma = 0.0017 against Planck via the CR018 structural derivation - same A0 structural constant
- **CR117** documents the SAM/CMB scope boundary - this distance road closes background; CMB-IC carries the configuration layer
- **CR017** branch verdict explicitly leaves CMB modal/polarization open - consistent with the CR117 scope handoff

## Cryptographic Chain

```text
CR012_native_typed_ruler_road_bridge_derivation_sha256       = 29abc83488c863d2eacf7ca2595cda4f63cd5ef969eed56fcd8631ae9523517d
CR013_sn_luminosity_ledger_shrinkage_sha256                  = bffd17d22a11fcb03b0c2dd8581550d60df91c052e59e7f8023bae7d300420cc
CR014_bao_ruler_projection_ledger_shrinkage_sha256           = 78fe728d2adf4780ccf13ec1b7cd5149889f00057f7150a63cbfe1594d17b8a2
CR015_sn_bao_independent_ledger_lock_sha256                  = 584d3dad801b81bc62e84b22be6b45391c14fe238b0aa6b85b27bc85e3fb8217
CR016_cmb_acoustic_ruler_photon_road_ratio_sha256            = 4ec3d7baf0966db6daeec2da2c0a5b3393eff2165471a8941be03cb1935af5d6
CR017_distance_road_typed_bridge_closure_sha256              = b122955abcfa4cb4739f2e8846b3c51b3155d72ad9961013b113b706b782f555
CR108_planck_anchor_sha256                                   = 736ac1405394b787d86db26f785458266f069472953abee97c39aa69d5a6ade5
CR114_cosmic_baryon_bridge_sha256                            = e2f394b40768bc45d916427e7031066cb23e24298e0e4337c3c5bcd4715549c6
CR117_sam_cmb_scope_boundary_sha256                          = 0ccbc3d720674b45a8f4b569a926a3ae213ea5a00786380fd598a2a8568c7c4c
BLINDNESS_PROTOCOL_sha256                                    = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR118 headline export claim sha256                            = 05b17c8984b1546c9d301e0c89f208472cc45584660c0958b367b0b48abb848d
```

## Immutability

CR012, CR013, CR014, CR015, CR016, CR017 are all unmodified.  CR118 hashes them and presents the headline; it does not edit them.  The branch-06 verdict (CR017_PASS_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE) stands as committed.
