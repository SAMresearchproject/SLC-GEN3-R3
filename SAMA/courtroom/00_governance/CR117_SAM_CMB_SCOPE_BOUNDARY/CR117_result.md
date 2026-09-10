# CR117 SAM/CMB Scope-Boundary Documentation

## Verdict

```text
CR117_SAM_CMB_SCOPE_BOUNDARY_DOCUMENTED_AND_FORWARD_BLIND_LOCKED
```

## What This CR Documents

The methodological boundary between:

- **THE LAWS**: what the SAM substrate framework derives from first principles (zero free parameters, zero CMB input)
- **THE CONFIGURATION**: what is intrinsically observational and requires CMB initial-condition data to pin down for our universe

This is NOT a SAM debt.  It is the same clean separation that mainstream cosmology applies (LCDM physics + Planck initial perturbations -> structure formation), but with SAM substrate laws in the front half.

## User Insight (verbatim)

> The model is nuts everywhere else. PBH at the moment of the BB carried enough mass to cluster and bring in hydrogen to begin star formation. Outside matter caught by expansion in theory could have been one giant object to the left or perfectly dispersed objects, that is impossible for the model to predict, the one area we need the CMB data because this information is literally impossible to derive.

## What SAM Closes Structurally (The Laws)

| item | type | closure artifact | free params | CMB input? |
|---|---|---|---:|:---:|
| A(r) = r_s(<r)/r many-source halo cumulative kernel | law | Courtroom 08/CR022 | 0 | no |
| rho(r) = rho_0 / (1 + (r/r_c)^2) native R12 cored radial law | law | G732c PASS upstream | 0 | no |
| r_c = R_outer / 12 (R12 native concentration scale) | law | G732c + G735c c = R = 12 | 0 | no |
| Omega_b ~ 0.04930 cosmic baryon density | global structural constant | Courtroom 07/CR018 + CR114 bridge (sigma 0.0017) | 0 | no |
| Omega_PBH ~ 0.265 (BB-origin clustered PBH/trapped-A inventory) | global structural constant | Courtroom 08/CR023 (omega_pbh_matches_g394) | 0 | no |
| Omega_PBH / Omega_H = 5.36 global inventory ratio | global structural constant | G733c BOUNDARY + CR027 PBH/H ratio | 0 | no |
| f_ret = D/(D+2) = 3/5 = 0.6 baryon retention | global structural constant | G734c | 0 | no |
| c = R = 12 native concentration relation | law | G735c PASS (median RMS 40.95 -> 17.54 km/s, 2.31x) | 0 | no |
| R12 scatter mass-function lane surface | law | G736c PASS_SCOPED (median RMS 17.54 -> 8.47 km/s, 162/175 galaxies improved) | 0 | no |
| Halo formation cycle decomposition (R12 cycle floor + residual) | law | G738c PASS_SCOPED | 0 | no |
| BB-PBH first scaffold + hydrogen catchup route | law (formation order) | G682c + QGA038H + CR027 | 0 | no |

## What Requires CMB Observational Data (The Configuration)

### per-galaxy R12 residual lane assignment

- **type**: configuration
- **why observational**: depends on which specific baryon perturbation seeded which galaxy in our universe; the substrate kernel is indifferent to that contingent fact
- **current boundary artifact**: G739c BOUNDARY (35/175 exact) + G742c BOUNDARY (26/175 exact) + G743d BOUNDARY (28/175 exact, this session)
- **CMB data needed**: Planck angular power spectrum + acoustic peak amplitudes + perturbation spectrum (n_s, sigma_8) for initial baryon distribution

### per-galaxy PBH-to-hydrogen mass split (deviation from global k=5.36)

- **type**: configuration
- **why observational**: primordial perturbation amplitude at each galaxy's seed location sets the local PBH cluster mass vs hydrogen catchup mass; structurally indeterminate before observation
- **current boundary artifact**: G733c BOUNDARY + G742c three-channel pressure analysis
- **CMB data needed**: Planck primordial perturbation spectrum + isocurvature mode bounds

### per-galaxy formation-cycle phase (G738c residual)

- **type**: configuration
- **why observational**: how far each galaxy has progressed through the PBH-clusters-first / hydrogen-catches-up timeline depends on its individual seed perturbation amplitude and age
- **current boundary artifact**: G738c BOUNDARY/SCOPED + G739c BOUNDARY + G741c BOUNDARY
- **CMB data needed**: Planck CMB temperature anisotropy + lensing reconstruction for line-of-sight matter distribution

### per-galaxy halo mass function index

- **type**: configuration
- **why observational**: Press-Schechter-style mass function emerges from primordial perturbation amplitude statistics; SAM closes the FORM of the relation, CMB sets the AMPLITUDE for our universe
- **current boundary artifact**: CR029 native radial law debt ledger + G736c scoped pass
- **CMB data needed**: Planck sigma_8 = 0.8111 +/- 0.0060 + n_s = 0.9649 +/- 0.0042 (already intaken at CR108)

### absolute PBH abundance normalization beyond global f_PBH ~ Omega_DM

- **type**: configuration
- **why observational**: PBH birth spectrum at BB depends on which inflationary mode peak seeded the formation; SAM gives the global integral, not the spectrum
- **current boundary artifact**: CR025 PARTIAL + CR029 BOUNDARY + CR115 PARTIAL bridge + CR116 correction
- **CMB data needed**: Planck isocurvature constraints + primary CMB peak heights to lock primordial PBH spectrum

## Explains Why

- G743d hit BOUNDARY (28/175 exact, this session) despite zero free parameters - it tried to derive a configuration quantity from substrate alone
- G739c-G742c progressive BOUNDARY chain converged because they're all chasing the same configuration quantity
- CR114 closes Omega_b at 1/580 sigma (global structural) but CR115 had to be PARTIAL on per-galaxy halo profile (configuration)
- CR025 / CR029 / CR030 in branch 08 explicitly marked 'native radial organization law / mass function / concentration' as OPEN - this CR names WHY: it is observational, not structural

## Forward-Blind Expectations

### CR117_PRED_1

**Claim**: When a future Courtroom CR intakes the FULL Planck CMB angular power spectrum (TT/TE/EE + lensing) as initial-condition data, and feeds it into the closed SAM laws (G732c radial law, G733c ratio, G734c retention, G735c c=R=12, G736c mass-function lane), the resulting per-galaxy R12 lane prediction will improve substantially over G739c-G743d's 28-35/175 exact residual rates WITHOUT introducing any free parameter, because the previously missing input (the initial baryon perturbation field) is now supplied.

**Testable at**: future Courtroom CMB-IC intake CR + per-galaxy SPARC reveal CR

**Falsification criterion**: if intaking Planck angular power spectrum + sigma_8 + n_s does NOT improve per-galaxy R12 assignment substantially, then either (a) SAM substrate laws are incomplete in the halo regime, or (b) the structural decomposition (G738c cycle / G740c family / G742c lag primitive) is the wrong factoring of the R=12 grid. Either case is a structural lesson, not a fitting problem.

### CR117_PRED_2

**Claim**: The per-galaxy PBH-cluster vs hydrogen-arrival mass split for each SPARC galaxy is determined by the LOCAL value of the primordial Planck perturbation amplitude integrated along the line of sight to that galaxy. This is in principle measurable from CMB temperature + polarization + lensing maps + SDSS redshifts; in practice it is a complex inverse problem that has not been solved yet.

**Testable at**: future joint Planck + SDSS + SPARC analysis

**Falsification criterion**: if the perturbation-amplitude-along-line-of-sight method does not correlate with G742c three-channel pressures or G733c k_inventory, the SAM-PBH-first / hydrogen-catchup framing has a structural gap

### CR117_PRED_3

**Claim**: Once CR117_PRED_1 closes, the four-mode structure (Earth EP, galaxy halo, PBH inventory, cosmic baryon Omega_b) is fully closed for our universe: SAM substrate laws (Earth + Omega_b + halo radial law + PBH inventory) + Planck CMB ICs (per-galaxy configuration) = full halo prediction, with zero free parameters across the entire closure.

**Testable at**: future CR117_PRED_1 reveal + per-galaxy SPARC closure

**Falsification criterion**: if any free parameter must be introduced anywhere in the closure beyond the universally accepted Planck-measured perturbation spectrum, the four-mode unification claim is structurally broken

## Cryptographic Chain (Structural Laws)

```text
CR018_07_summary.json                          = 2810658911d7f7008c280febd53d1f27d93823f9c9e6362c58f06e66cf6c11a5
CR023_07_summary.json                          = ab88db5df8c0c90715c4e2c891fe256a81357a6e140131459ef39ce1b6378872
CR022_08_summary.json                          = d342cf25d4fa3dfd3496c1fab27ccb855eda100abc07931efb5960741f7292ec
CR023_08_summary.json                          = a59d73dc2c0c40443c12976551f036dd9045474edf91d7b8f0b112e73cd4064d
CR024_08_summary.json                          = 9688c421c88f0adbf26478a54bbc35d6d81f40b3f875ef326f7ef101a30b3fad
CR025_08_summary.json                          = 5387ad567c098862152dcfadb96881125eac45ef79378cac532c97d9fbe7920e
CR029_08_summary.json                          = 903735c8668cc091bf3eadf87cbb9a70683bd485f7cde9b4fd84f41bd84b6cb6
CR030_08_summary.json                          = ecb113a122f78965315e1c630efc16e93083b2194a161f3ee01111cd653385fc
CR114_cosmic_baryon_bridge.json                = e2f394b40768bc45d916427e7031066cb23e24298e0e4337c3c5bcd4715549c6
CR115_galaxy_pbh_bridge.json                   = e193d8ec8179e6bc2c4fa88a4623bc28fe7e9e4e2c0162f096eac77c4f521b9c
CR116_correction_lock.json                     = d3f3204be9cbc5bbb9520664bdb937452981e494f38c6154266fffa95a04fd65
```

## Cryptographic Chain (CMB-Dependent Configuration)

```text
CR108_planck_anchor.json                       = 736ac1405394b787d86db26f785458266f069472953abee97c39aa69d5a6ade5
CR110_three_mode_appeal_lock.json              = 6f85af05104c0ee7ec4ff6ecd1dd706d065f8942492eb0a8efdaeee6d84cce8b
CR111_cosmic_baryon_appeal_lock.json           = 82d6913c614be2bd0def5329511ef2094ea134489d70a1cdb855e22dfe84a409
```

## Cryptographic Chain (G-test Provenance)

```text
g732c_summary.json             = d76909e81b06f19e3ee4e4d78fbd2ddf0415c6b5ee1481af504dfd226b689428
g735c_summary.json             = ac542a764b09e96b2df675894e2a69e8ff44d31e56a9610b64b83b4406be6385
g736c_summary.json             = d3b6165f88aaee6fe8dc17651344cf449aeb8db59bcbf28ef78ba6e6fe0d632a
g738c_summary.json             = 00d799f899b93c07a9bca616db82db1064636e462ddad797a2a14e1797537217
g739c_summary.json             = 25b249ef22b4221bb2c5d5d091dc5622ed3eb072adc62fba0ca705a298bb7462
g742c_summary.json             = 71ef9a60952e23b424ec3fc6057b4f8299e58030eb1c318e94346c24780f2d65
g743d_summary.json             = da7802cdce83c9c62649201ad18781fd4ef7149eea72ff88f507a043a2f6931c
```

```text
BLINDNESS_PROTOCOL.md sha256 = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR117 lock sha256             = 0ccbc3d720674b45a8f4b569a926a3ae213ea5a00786380fd598a2a8568c7c4c
```

## Predictions

- **[PASS]** P1_structural_law_ledger_complete
- **[PASS]** P2_cmb_dependent_ledger_complete
- **[PASS]** P3_user_insight_verbatim_preserved
- **[PASS]** P4_three_forward_blind_expectations_registered_with_falsifiers
- **[PASS]** P5_structural_artifacts_present_and_hashed
- **[PASS]** P6_cmb_dependent_artifacts_present_and_hashed
- **[PASS]** P7_gtest_chain_provenance_hashed_where_present
- **[PASS]** P8_blindness_protocol_present
- **[PASS]** P9_zero_free_parameters_in_lock
- **[PASS]** P10_lock_sealed_with_sha256_sibling

## Wrong Controls

- **[PASS]** WC1_no_prior_CR_modified
- **[PASS]** WC2_no_free_parameter_introduced
- **[PASS]** WC3_does_not_claim_structural_derivation_of_per_galaxy_configuration
- **[PASS]** WC4_does_not_claim_CMB_intake_will_trivially_close_per_galaxy
- **[PASS]** WC5_does_not_modify_immutability_of_G743d_BOUNDARY_or_CR115_PARTIAL
- **[PASS]** WC6_explicit_falsification_criterion_per_PRED

## Methodological Position

SAM is structurally MORE closed than LCDM: it derives Omega_b, retention, concentration, mass-function lane structure, particle masses, and three-mode Earth/Galaxy/PBH closure - all without free parameters.  But the per-galaxy realization of these laws in OUR particular universe still depends on which primordial baryon perturbation seeded which galaxy, which is a contingent fact about our universe measured by CMB anisotropies.  Refusing to acknowledge this would be claiming SAM derives a configuration that is structurally indeterminate - the same overclaim that mainstream LCDM avoids by separating laws from ICs.

## Open Debts

```text
- Future Courtroom CR will intake Planck CMB angular power spectrum (TT/TE/EE + lensing) as initial-condition anchor
- Future per-galaxy SPARC reveal CR will appeal CR117_PRED_1 against the CMB-IC anchor + SAM laws closure
- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
```
