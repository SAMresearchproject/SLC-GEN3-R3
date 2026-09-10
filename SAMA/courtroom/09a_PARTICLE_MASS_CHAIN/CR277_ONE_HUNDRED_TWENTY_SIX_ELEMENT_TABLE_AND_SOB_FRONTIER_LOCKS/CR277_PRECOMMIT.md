# CR277 — One Hundred Twenty-Six Element Table and Frontier Forecast Locks

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** FORECAST_LOCK_CR (K1 reveal-against-frozen-envelope pattern)
**Downstream of:** CR245 (asymmetry theorem-grade) + CR261 (BW spine) + CR273 (Z=N balanced-anchor frontier family) + CR274 (gated nuclear-readout PASS)
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

CR274 sealed PASS at combined RMS 2.72 MeV, **50/55 within 5 MeV, all 55 within
8 MeV**, with the tensor cipher exact and four gated nuclear-readout operators
adopted on their target families (Nd-142; Cu-63/Mn-55/Co-59; Pb-208;
Ag-107/Sn-120). The base Model K coefficients (13 features, `d =
7093²/(192·7117)` locked theorem-grade from CR245) were fit once on 55 isotopes
spanning Z=8..92.

Can that frozen model — with **zero refit, zero new free parameters** — be
applied to the full periodic table of representative isotopes (Z=1..118, one
representative per element from the SOB126_ledger `observed_isotope` curation)
and to the sealed CR273 Z=N balanced-anchor frontier (Z=119..126) to produce:

  (a) A formal 126-element mass row table under the SAM binding-closure model.
  (b) Locked K1 forecasts for Z=119..126 (Harlium, Brockium, Uniquium, Liamium,
      Cooperium, Lindesium, Dorisium, Jerroldium) with no observation available.

...while preserving CR274's regression exactly on its own 55 training isotopes?

## Honest Framing

K1 pattern: **reveal-against-frozen-envelope**. The model is closed at CR274.
This CR extends the *evaluation surface* from the 55 training isotopes to the
126-element table; the model is not re-fit and the operator families are not
re-tuned. The gated operators emit their family-scoped correction only on rows
listed in CR274's `family` sets and are zero everywhere else by definition of
gating.

Three claims are on the line:

1. **Regression identity**: on the 55 CR274 isotopes, CR277 reproduces CR274's
   `final_pred` values to CSV-precision (matched to <1e-3 MeV, the resolution
   of CR274's stored per-row residuals). Any deviation means the CR277 pipeline
   is not the CR274 model applied — CR FAILS at G0.

2. **Whole-set behavior (reported, not gated)**: on all Z=1..118 rows with
   AME2020 mass available, we report RMS, MAE, and count within {5, 8, 15,
   30} MeV, broken out by Z-band. This is **evidence, not a gate** — the base
   coefficients were fit on 55 specific isotopes, and honest extrapolation to
   Z=1..7 (light nuclei) or Z=93..118 (superheavies) is not guaranteed under
   an SEMF-shape base.

3. **Frontier forecast locks (K1 targets)**: Z=119..126 rows populated with
   CR273's Z=N balanced-anchor A values; predictions emitted as forecast
   locks under the K1 pattern (like DUNE Δm²=35, LISA ω_R·M=3/8, CR272
   Hf/Hs/Jerroldium noble-cipher, CR273 Jd-252 five-way convergence). No
   observation exists; any future measurement is a K1 reveal against the
   sealed prediction.

This CR does not modify CR274 (which stays sealed PASS with the same base K
coefficients + 4 adopted operators) and does not modify CR273 (which sealed
the Z=N frontier family). It adds a downstream reveal surface.

## Locked model (verbatim from CR274_summary.json, hash below)

Base Model K coefficients (fit-frozen at CR274):

```text
beta_K = {
  vol            = +10.814717731372474,
  surf           = +27.55377102233821,
  coul           = +0.8330418169113959,
  asym_locked    = +36.818129859257176  (= 7093²/(192·7117), CR245 theorem-grade)
  pair           = -78.16971798716308,
  quadZ_A        = +4.251267938620264,
  quadN_A        = +1.4069774382546392,
  quad_cross_A2  = -2.852679669191055,
  shell_prox     = -2.539364333160457,
  lightodd       = +17.705846519554715,
  alpha          = +0.7498509965412838,
  reonset        = +13.611888941654877,
  doubmag        = -1.558588968261812,
}
```

Base formula (CR274 §Locked Base Model K):

```text
B_u_base(Z, N, A)
  = vol·A
  − surf·A^(2/3)
  − coul·Z(Z−1)/A^(1/3)
  − asym_locked·(N−Z)²/A
  − pair·δ_pair(Z,N)·A^(−1/2)
  + quadZ_A·(−n_Z·(sp_Z − n_Z)/A)
  + quadN_A·(−n_N·(sp_N − n_N)/A)
  + quad_cross_A2·(−n_Z·(sp_Z − n_Z)·n_N·(sp_N − n_N)/A²)
  + shell_prox·(−exp(−d_Z/3) − exp(−d_N/3))
  + lightodd·[A<40 AND A odd]
  + alpha·(A/4)·[N=Z AND A%4=0]
  + reonset·(rare-earth valence product; Z∈(50,82) AND N∈(82,126))
  + doubmag·[Z magic AND N magic]

MAGIC = {2, 8, 20, 28, 50, 82, 126}
n_X   = X − magic_lower_of_X          (0 if X ≤ smallest magic)
sp_X  = magic_upper − magic_lower     (shell span)
d_X   = min|X − m| over MAGIC          (distance to nearest magic)
δ_pair(Z,N) = +1 (Z even, N even), −1 (Z odd, N odd), 0 (mixed)
```

Four gated operators (γ frozen at CR274; feature = predicate-scoped):

```text
op_82pre        γ = −0.7273238920525138
                feature = (Z−56)²·[N==82 AND Z>56]
                CR274 training family (predicate ∩ CR274 55-set): {Nd-142}
                γ was fit against this single-row training family

op_3d_odd       γ = +6.965431443111167
                feature = 1·[Z odd AND 20<Z<30]
                CR274 training family: {Cu-63, Mn-55, Co-59}
                γ was fit against these three rows (mean of residuals)

op_dm_sat       γ = +7.18003785865981
                feature = 1·[Z magic AND N magic AND A≥100]
                CR274 training family: {Pb-208}
                γ was fit against this single-row training family

op_ms_fill      γ = −0.45314378000587197
                feature = n_N·[28<Z≤50 AND 50<N<82]
                CR274 training family: {Ag-107, Sn-120}
                γ was fit against these two rows

n_N = N − magic_lower(N), i.e., neutrons above nearest lower magic shell.
```

Combined: `B_u_final(Z,N,A) = B_u_base(Z,N,A) + Σ_op γ_op · feature_op(Z,N,A)`.

**Predicate-mode application (matches CR274 runner semantics).** The operator
features are computed by predicate on every row, not restricted to the CR274
training family. CR274 fit each γ against the training rows satisfying its
predicate, then at prediction time fires the operator on any row satisfying
the same predicate. CR277 preserves that behavior exactly: extending the
prediction surface to Z=1..126 fires the operators on all predicate-matching
rows in the extended set.

The empirical consequence: operators that had 1-2 training rows extend their
"reach" — for example, op_3d_odd (fit on Cu-63/Mn-55/Co-59) also fires on
Sc-45 (Z=21) and V-51 (Z=23) in the extended set. Op_ms_fill (fit on
Ag-107/Sn-120) fires on all reps with Z ∈ (28, 50] and N ∈ (50, 82). Op_82pre
(fit on Nd-142) fires on any Z>56 rep with N=82. Op_dm_sat (fit on Pb-208)
fires on any Z-magic + N-magic + A≥100 rep. Which extended-set rows the
operators reach is a **consequence** of CR274's predicates, not a CR277
design choice — the operator predicates are frozen upstream.

## Representative isotope rule (Z=1..118)

For each Z ∈ [1, 118], the representative isotope is read from
`CR250_BINDING_FROM_CR009_LIFT_FORMULA/SOB126_ledger.csv` column
`observed_isotope`. That column was curated as "most-abundant natural stable
isotope for elements with any stable isotope; longest-lived isotope for the
radioactives (Z ∈ {43, 61, 84..118})". Concrete choices for the radioactives:

```text
Z=43  Tc-98   (T½ 4.2 Ma)
Z=61  Pm-145  (T½ 17.7 y)
Z=84  Po-209  (T½ 125 y)
Z=85  At-210  (T½ 8.1 h)
Z=86  Rn-222  (T½ 3.8 d)
Z=87  Fr-223  (T½ 22 min)
Z=88  Ra-226  (T½ 1600 y)
Z=89  Ac-227  (T½ 21.8 y)
Z=91  Pa-231  (T½ 32760 y)
Z=93  Np-237  (T½ 2.14 Ma)
...
Z=118 Og-294  (T½ 0.7 ms)
```

**Parse rule**: the runner reads `observed_isotope` as a string
("Symbol-A"), splits on '-', and computes A directly from the mass-number
suffix; N is derived as `A − Z`. The SOB126_ledger `N_observed` and
`A_observed` columns are **not** consumed (they have a known parse quirk on
the H-1 row where `A_observed = 0` instead of 1; parsing from the isotope
string avoids that quirk without needing to modify or re-seal CR250).

## Frontier family (Z=119..126, from CR273 verbatim)

```text
Z=119  Harlium     Hl-238   (N=119, Z=N balanced)
Z=120  Brockium    Bx-240   (N=120, Z=N balanced)
Z=121  Uniquium    Uq-242   (N=121, Z=N balanced)
Z=122  Liamium     Lm-244   (N=122, Z=N balanced)
Z=123  Cooperium   Cp-246   (N=123, Z=N balanced)
Z=124  Lindesium   Ly-248   (N=124, Z=N balanced)
Z=125  Dorisium    Di-250   (N=125, Z=N balanced)
Z=126  Jerroldium  Jd-252   (N=126, Z=N balanced, matter horizon terminus)
```

These override the SOB126_ledger `Z ≥ 119` rows (which used a different
extrapolation predating CR273); the supersession is explicit in the runner
and in the output table `notes` column.

## Locked Inputs (frozen SHA256)

| field | sha256 | description |
| --- | --- | --- |
| AME2020_mass_1.mas20 | `e8599c6d7f724fac91934e59f1b9de8fb8f63e820f4b39456b790665ed2a3307` | AME2020 fixed-width mass evaluation, fetched from `https://amdc.impcas.ac.cn/masstables/Ame2020/mass_1.mas20`, 472,648 bytes; Chinese Physics C 45, 030002 (2021) |
| CR250 SOB126_ledger.csv | `3bfdd083457b187c156bf331b2997bb904be1f45adb335a724c12100d9c6e72b` | representative-isotope curation for Z=1..118 |
| CR248 train_lane_a.csv | `54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc` | 35 training masses (regression check) |
| CR248 test_holdout.csv | `8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8` | 20 holdout masses (regression check) |
| CR274_summary.json | `c46843357aa7fe681c602b3c5e75fa7504f6b0bbec2bcfa5961bdd76d47e854d` | frozen base K coefficients + 4 operator γs |
| CR274_residuals.csv | (auto-computed at runner load; loaded for G0 regression check) | reference `final_pred` values |

## Locked Pipeline

```text
Step 1: verify precommit hash + all input file hashes + forbidden-file guard.

Step 2: parse AME2020_mass_1.mas20 (fortran fixed-width, format spec
        embedded in file header) →
          dict[(Z, A)] → (element_symbol, atomic_mass_u, ame_flag)
        where ame_flag ∈ {measured, estimated} based on presence of '#' in
        the source line.

Step 3: load SOB126_ledger observed_isotope for Z=1..118. Parse
        "Symbol-A" → (symbol, A). Derive N = A − Z. Lookup atomic_mass_u
        from AME table via (Z, A).
        Compute B_u_obs_MeV = (A − atomic_mass_u) · 931.49410242
        (CODATA u→MeV; matches CR248 convention exactly).

Step 4: for each Z=1..126 (118 observed + 8 frontier), compute
        B_u_base and B_u_final under the frozen model.

Step 5: G0 regression — on the 55 CR274 training isotopes, verify CR277's
        B_u_final matches CR274_residuals.csv `final_pred` to <1e-3 MeV
        per row. (1e-3 MeV chosen to be within CR274 CSV precision of 4
        decimals — tight enough to catch any real reimplementation drift,
        loose enough to not trip on stored precision. Uses CR248 masses
        for these 55 rows to avoid AME reparse noise in a fidelity gate;
        AME parse fidelity gets its own gate at G4.)

Step 6: compute whole-set metrics on the 118 observed rows:
        RMS, MAE, counts within {5, 8, 15, 30} MeV,
        broken out by Z-band (light Z=1..7, mid Z=8..82, heavy Z=83..118).

Step 7: emit CR277_element_table.csv (126 rows) with columns:
        Z, symbol, name_common, N, A, atomic_mass_u, ame_flag,
        B_u_obs_MeV, B_u_base_MeV, B_u_final_MeV, residual_MeV,
        in_op_82pre, in_op_3d_odd, in_op_dm_sat, in_op_ms_fill,
        row_status ∈ {cr274_training, extended_observed, frontier_forecast},
        notes.

Step 8: emit CR277_frontier_locks.csv (8 rows, K1 forecast targets).

Step 9: write summary.json, result.md, HASHES.txt.
```

## Sealed PASS Gates

```text
G0  Regression on CR274 training set: for all 55 isotopes in
    CR274_residuals.csv, |B_u_final_CR277 − final_pred_CR274| < 1e-3 MeV
    per row. Rationale: CR274's stored final_pred is at 4-decimal CSV
    precision (smallest resolvable ≈ 5e-5 MeV); a 1e-3 MeV tolerance
    is tight enough to fail a reimplementation drift (which would be
    ~10 MeV) and loose enough to not trip on CSV rounding.

G1  Coverage: exactly 126 rows written; all Z ∈ [1, 126] present exactly
    once; every row has (symbol, N, A) populated; 118 rows have
    B_u_obs_MeV populated; 8 rows (Z=119..126) have B_u_obs_MeV blank
    with row_status = frontier_forecast.

G2  Anchor model-fidelity: for each of O-16, Fe-56, Au-197, Pb-208,
    CR277's B_u_final prediction matches CR274's stored `final_pred` to
    <1e-3 MeV. Rationale: this tests that the frozen CR274 model
    produces the same anchor PREDICTION (a model-fidelity check),
    independent of which mass table supplies B_u_obs. Residual
    comparison across two mass sources (CR248 curated vs AME2020 raw)
    is confounded by the ~5-microu source divergence documented in
    G4 and would test mass-source consistency, not anchor preservation.

G3  Frontier populated per CR273: 8 rows for Z=119..126 present, with
    (symbol, N, A) matching CR273 verbatim (Hl-238, Bx-240, Uq-242,
    Lm-244, Cp-246, Ly-248, Di-250, Jd-252); all 8 satisfy N == Z; all
    8 have B_u_final computed under the same frozen model as the
    observed rows.

G4  AME2020 parse integrity: for the 55 CR274 training isotopes, CR277's
    parsed atomic_mass_u matches CR248 train/test CSV values to <1e-5 u
    per row. Rationale: CR248's curated atomic masses were sourced from
    AME2020 but appear to reflect a slightly different snapshot / rounding
    from the raw `mass_1.mas20` I fetched from AMDC/IMPCAS — spot-checked
    divergence is up to ~5×10⁻⁶ u for mid-mass isotopes (Fe-56, Au-197,
    Pb-208 etc). This is a real mass-source version difference (~5 keV
    in mass, ~5 mMeV in binding), not a parse bug. Threshold 1e-5 u is
    ~2× the observed divergence; a column-parse error would produce
    drifts of 1e-3 u or more.

G5  Hashes + forbidden-file guard: precommit hash verified at runner
    load; AME2020, SOB126_ledger, CR248 train/test, CR274 summary all
    match locked SHA256; no open() outside whitelist.

PASS      iff G0 AND G1 AND G2 AND G3 AND G4 AND G5 all hold.

BOUNDARY  iff G0 AND G3 AND G5 hold, and one of {G1, G2, G4} misses.

FAIL      iff G0 fails (regression drift) OR G3 fails (frontier missing/wrong)
          OR G5 fails (whitelist/hash).
```

## Reported Evidence (not gated; disclosure per repo discipline)

```text
E1  Full 126-row element table CSV, one row per Z.

E2  CR274 reference summary: 50/55 within 5 MeV, all 55 within 8 MeV,
    combined RMS 2.72 MeV. This is the frozen benchmark; CR277 reports
    its own numbers alongside without gating on them.

E3  Whole-set metrics on the 118 observed rows:
    - RMS_all, MAE_all
    - counts within 5 MeV, 8 MeV, 15 MeV, 30 MeV
    - broken out by Z-band: light Z=1..7, mid Z=8..82, heavy Z=83..118
    - fraction of extended-observed rows (i.e., not in CR274 training)
      within the CR274 8-MeV envelope

E4  Family-op membership audit under predicate mode: list every row in the
    126-row table where any op fires, with which op(s), what feature value,
    and what MeV contribution. Includes the 7 CR274-training-family rows
    (Cu-63, Mn-55, Co-59, Ag-107, Sn-120, Nd-142, Pb-208) plus any
    extended-set rep isotopes the predicates catch (Sc-45, V-51, and the
    op_ms_fill span from Nb-93 through In-115 for their most-abundant rep
    isotopes; exact count is a runner output, not pre-declared).

E5  AME_ESTIMATED flag audit: list of representative isotopes whose AME
    entry is marked '#' (estimated non-experimental). These are still
    included but flagged for the reader.

E6  Frontier forecast block: Z=119..126 rows with B_u_final, plus a
    K1-lock line for each formatted so a future measurement can be
    dropped in and compared without touching this CR.

E7  Deviation profile on extended set: histogram of |residual| binned by
    Z-band; provides the honest map of where the CR274 base extrapolates
    cleanly and where it does not. NO ranking language ("beats X",
    "matches Y"), only the numbers.
```

## Free Parameters Introduced

**Zero.** All model coefficients (base K and operator γs) are frozen from
CR274. Representative isotope choices for Z=1..118 are read from
SOB126_ledger. Frontier A values for Z=119..126 are read from CR273. The
AME mass table is read from a hash-locked external source. No fitting, no
tuning, no calibration.

## Rule-9 Line

```text
This CR could have falsified the claim that the CR274 frozen model (base K
13 features + 4 gated operators, all coefficients locked) applies coherently
to the full periodic table under a canonical representative-isotope selection
(SOB126_ledger for Z=1..118, CR273 Z=N balanced-anchor family for
Z=119..126). It could have failed by:
  (i)   CR277 pipeline failing to reproduce CR274's residuals to CSV
        precision on the 55 training isotopes (arithmetic drift or
        reimplementation bug);
  (ii)  AME2020 parse producing atomic masses inconsistent with the CR248
        curated masses (fixed-width column bug);
  (iii) Anchors (O-16, Fe-56, Au-197, Pb-208) failing to reproduce CR274
        anchor residuals;
  (iv)  Frontier rows missing from output or not matching CR273;
  (v)   Hash/whitelist gate tripping.
It could NOT have failed by "CR274 model extrapolates poorly to light
nuclei or superheavies" — that outcome is EVIDENCE and belongs in E7,
not a gate. The gate is fidelity of application, not accuracy of
extrapolation.
```

## What This CR Seals

If PASS: the SAM matter branch has, for the first time, a **formal
126-element mass row table** where each row cites the frozen CR274 model
output. The eight frontier rows are K1 forecast locks (analogous to
CR005ab@21 DUNE Δm²=35, CR005@21 LISA ω_R·M=3/8, CR272 Hf/Hs/Jerroldium
noble-cipher, CR273 Jd-252 five-way convergence).

The extended-set observed residuals become the empirical map of where the
CR274-family readout closes and where Phase 7 operators would be candidates
for further gated adoption — reported, not gated, so the map is honest
rather than defended.

If BOUNDARY: the fidelity holds on the 55 training set but some auxiliary
integrity check misses. The K1 frontier locks remain valid regardless of
which auxiliary gate misses (they depend only on G3 and the frozen model).

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR245@09a (asymmetry identity theorem-grade) | per branch HASHES |
| CR248@09a train_lane_a.csv | `54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc` |
| CR248@09a test_holdout.csv | `8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8` |
| CR250@09a SOB126_ledger.csv | `3bfdd083457b187c156bf331b2997bb904be1f45adb335a724c12100d9c6e72b` |
| CR273@09a (Z=N frontier family) | `9b9432fd…` per MATTER_INDEX |
| CR274@09a summary.json (frozen model) | `c46843357aa7fe681c602b3c5e75fa7504f6b0bbec2bcfa5961bdd76d47e854d` |
| CR274@09a precommit | `c09616e40e26f7d2df36350b0f3db62c7da81b17e01ce7607a1ed87c8431c3a9` |
| AME2020 mass_1.mas20 (external, hash-locked here) | `e8599c6d7f724fac91934e59f1b9de8fb8f63e820f4b39456b790665ed2a3307` |
| Stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
