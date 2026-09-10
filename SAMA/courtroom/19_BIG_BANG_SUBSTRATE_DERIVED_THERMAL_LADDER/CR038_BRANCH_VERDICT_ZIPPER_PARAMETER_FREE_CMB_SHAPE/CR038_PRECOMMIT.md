# CR038 — Branch 19 Verdict Zipper: Parameter-Free CMB Shape Chain

**Branch:** 19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER
**Classification:** BRANCH_VERDICT_ZIPPER_CR (downstream of CR037C@19)
**Sealed by:** Sean Brady, 2026-06-29
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Test Type

```text
Branch verdict zipper. Reads only frozen sealed summary.json files from
the six PASS CRs that constitute the parameter-free CMB shape chain in
branch 19, plus the two preserved-FAIL audit-trail CRs that document
the chain's prior states. Applies the closure predicate declared below
and emits a citable branch-level closure record.

No new measurement. No catalog data read. No CAMB call. The forbidden-
file open() guard installed at runner startup whitelists exactly the
summaries listed below plus this precommit and the runner source.

This is the final close of the parameter-free CMB shape arc in
branch 19. CR037C placeholder named CR038 as the zipper. The branch
README's CR ladder is missing CR035A2 through CR037C; CR038 corrects
that as part of its result emission.
```

## Question

```text
Given the six sealed PASS CRs constituting the parameter-free CMB
shape chain in branch 19

  CR035A2 -- SAM density spine + H_0_external + Planck-centroid
             perturbations vs Planck PR3 full shape (PASS; peak-finder
             audit replacement for CR035A)
  CR036   -- H_0_SAM derived from substrate atoms + FIRAS T_CMB +
             CODATA / SI (PASS at 0.16% from Planck reference)
  CR036B  -- SAM density spine + H_0_SAM + Planck-centroid perturbations
             vs Planck PR3 full shape (PASS at TT chi^2/dof ~ 1.04)
  CR037A  -- SAM perturbation triplet (A_s = eta_SAM*sqrt(R);
             n_s = 1 - chi/2; tau = 2*A_0) inside Planck posterior
             at STRONG_CONTACT (PASS)
  CR037B  -- full SAM cosmology (densities + H_0 + perturbation triplet)
             vs Planck PR3 full shape, NO Run B optimizer
             (PASS at TT chi^2/dof = 1.034)
  CR037C  -- same full SAM cosmology vs ACT DR4 cleaned-CMB bandpowers
             with full 260x260 covariance and published bandpower
             window functions, yp2 fixed at 1.0, NO Run B optimizer
             (PASS at TT chi^2/dof = 1.30, full chi^2/dof = 1.12)

does the chain constitute a parameter-free CMB shape closure?
```

## Closure Predicate (applied to frozen summaries)

```text
For each CR in the chain, the closure predicate requires:

  cr.scientific_verdict == "PASS"
  AND cr.free_parameters_introduced == 0    (or _RunA variant per CR convention)
  AND cr.prior_CR_result_inputs == False
  AND cr.forbidden_files_opened == False
  AND cr.execution_status == "CLEAN"

Plus chain-level conditions:

  G_chain_substrate_invariant:
    All five PASS CRs that emit substrate{} blocks must agree on
    (Omega_m, Omega_b, Omega_c) to machine precision.

  G_chain_H0_invariant:
    CR036/CR036B/CR037B/CR037C must all use H_0 = 67.2503751950
    (from CR036 sealed) to machine precision.

  G_chain_perturbation_invariant:
    CR037A must derive (A_s, n_s, tau) from substrate identities.
    CR037B and CR037C must consume those values to machine precision
    (rel diff <= 1e-10).

  G_chain_planck_full_shape:
    CR037B TT chi^2/dof must be <= 2.0 (sealed PASS bound).

  G_chain_act_full_shape:
    CR037C TT chi^2/dof must be <= 2.0 AND full chi^2/dof must be <= 2.0
    (sealed PASS bounds).

  G_chain_independent_instrument:
    CR037C must read ACT DR4 (not Planck) external data files
    AND must not have opened any Planck data file at runtime.
```

## Sealed PASS Gates

```text
PASS (branch zipper):
  G1 each-CR predicate satisfied for CR035A2, CR036, CR036B, CR037A,
     CR037B, CR037C  (six per-CR predicates)
  G2 chain substrate invariant
  G3 chain H_0 invariant
  G4 chain perturbation invariant
  G5 CR037B Planck full-shape PASS bound
  G6 CR037C ACT full-shape PASS bound
  G7 CR037C external-instrument independence (no Planck file at
     runtime; verified via summary's "external_data_hashes" matching
     only ACT files)
  G8 precommit hash verified at runner load
  G9 forbidden-file open() guard not tripped

BOUNDARY:
  Any single G1 sub-check or G2-G7 evaluates False
  (means the zipper is premature relative to actual chain evidence).

FAIL:
  Hash mismatch, forbidden-file guard trips, or runner spec error
  (cited sealed value cannot be reproduced from the summary.json).
```

## Open Items After This Update (must appear verbatim in result.md)

```text
O1. Branch 19 also carries CR001/CR001b sealed FAIL and CR001c sealed
    PASS for substrate-DERIVED recombination physics (Saha + Peebles +
    corrected optical depth). The derived recombination gives
    100*theta_* off Planck by +1.71%, ell_A by -1.68%, r_d by -1.55%,
    z_* by -1.55% (per CR001c result). The CR037 chain uses CAMB's
    standard recombination (RECFAST default) rather than SAM-derived
    recombination, and reaches sub-percent contact via full
    Boltzmann + window functions. The structural tension between
    "SAM-derived recombination at ~1.5-1.7% from Planck" and
    "SAM-cosmology + CAMB-recombination at sub-percent from Planck and
    ACT" is named, not closed, by CR038. Substrate-derived recombination
    physics remains a multi-CR program.

O2. The CR037 chain does not include a foreground re-derivation. ACT
    DR4 cleaned-CMB bandpowers are the experiment-marginalized
    bandpowers (SZ + radio + dust + tSZxCIB already removed by the ACT
    pipeline). CR037C inherits that marginalization; SAM does not
    derive the foreground spectra independently.

O3. yp2 (polarization-efficiency calibration) is fixed at 1.0 in
    CR037C. The full-likelihood version with yp2 marginalized is
    registered as CR037D placeholder.

O4. Forward CMB experiments (SPT-3G high-ell, Simons Observatory,
    CMB-S4) are not addressed by CR038. CR037E and CR037F placeholders
    cover those when public bandpower releases are available.

O5. CR035A is preserved bit-for-bit at sealed FAIL as the audit-trail
    record of the original peak-finder spec that was corrected in
    CR035A2 (peak-finder audit). The FAIL is not retracted; it is the
    chain's documented falsification of the original P1 sub-gate spec.
```

## Pre-Registered Frozen Inputs

| field | path |
| --- | --- |
| cr035a2_summary | `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR035A2_PEAK_FINDER_AUDIT\CR035A2_summary.json` |
| cr036_summary | `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR036_ETA_SAM_AND_H0_SELECTOR\CR036_summary.json` |
| cr036b_summary | `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR036B_CMB_SHAPE_WITH_H0_SAM\CR036B_summary.json` |
| cr037a_summary | `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR037A_SAM_PERTURBATION_SELECTOR\CR037A_summary.json` |
| cr037b_summary | `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT\CR037B_summary.json` |
| cr037c_summary | `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE\CR037C_summary.json` |
| cr035a_summary (FAIL audit trail; read for verification only) | `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR035A_SAM_DENSITY_SPINE_CMB_SHAPE\CR035A_summary.json` |

The runner whitelists exactly these seven read paths plus this precommit
and the runner source. Any other open() call trips the forbidden-file
guard and forces FAIL.

## Rule-9 Line

```text
This test could have falsified the claim that the six PASS CRs
(CR035A2, CR036, CR036B, CR037A, CR037B, CR037C) constitute a
zero-free-parameter CMB shape closure in branch 19, satisfying the
chain-level invariants (substrate atoms agree, H_0 sealed value
propagates, perturbation triplet propagates, both PR3 and ACT DR4
external-data shape gates hold), by any one of those CRs not
satisfying the closure predicate declared above when read from its
own frozen sealed summary, or by any of the chain-level invariants
failing to hold across the chain.
```

## What This CR Seals

Branch 19's CMB shape arc:

```text
substrate atoms (R, D, S, alpha_H)
   --> Omega_m, Omega_b, Omega_c                    (CR018b sealed; CR036 echoed)
   --> eta_SAM via dimensional bridge               (CR036 PASS)
   --> H_0_SAM = 67.2504 km/s/Mpc                   (CR036 PASS)
   --> SAM perturbation triplet                     (CR037A PASS)
         A_s = eta_SAM * sqrt(R)
         n_s = 1 - chi/2
         tau = 2 * A_0
   --> full SAM cosmology -> CAMB -> Planck PR3      (CR037B PASS at
         TT chi^2/dof = 1.034; zero free parameters)
   --> full SAM cosmology -> CAMB -> ACT DR4         (CR037C PASS at
         TT chi^2/dof = 1.30; full chi^2/dof = 1.12;
         zero free parameters; yp2 fixed = 1.0)
```

The chain is the citation target for any external reference to "SAM
reproduces the CMB shape." CR037B is the Planck full-shape live
citation; CR037C is the external-instrument independence live citation;
CR038 is the chain closure record.

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR035A@19 (preserved FAIL audit trail) | per branch `HASHES.txt` |
| CR035A2@19 (sealed PASS) | precommit `6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697` |
| CR036@19 (sealed PASS) | precommit `345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2` |
| CR036B@19 (sealed PASS) | precommit `ab2fea4b0822412cc5ca9978bab89822ea6fccffa76f94527bff05aaa660305e` |
| CR037A@19 (sealed PASS) | precommit `1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78` |
| CR037B@19 (sealed PASS) | precommit `5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b` |
| CR037C@19 (sealed PASS) | precommit `6ab6024c6e99ae35540ba93976cda79c3b2569bc4fffcd2371e36fd6ab4bd8ca` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
