# CR274 — Gated Nuclear-Readout Operators for CR261 Binding Closure

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** BINDING_CLOSURE_EXTENSION_CR (downstream of CR261 + CR245)
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

CR261 sealed BOUNDARY with a five-term BW fit on 55 isotopes at Lane A
train RMS 5.55 MeV — missing the ≤4 MeV gate by 1.55 MeV. The named
obstacle: the SEMF-shape terms don't capture shell + deformation +
cluster physics on the residual side, and adding those corrections by
joint refit turns CR261 into a fitted mass formula.

Can we close the CR261 gap while preserving the SAM claim — the tensor
accounting (per-particle G_p, G_e, G_n; F_conn = (N−Z)·(7093/192)) stays
sealed — by adding candidate operators that are **gated** at two layers:

  (a) each operator is fitted ONLY on its target family (feature = 0
      outside family, so non-family isotopes are structurally unchanged);
  (b) each operator must pass a family-improvement gate (mean residual
      drops > 2 MeV) to be adopted at all;

so that the extension is a per-family readout resolver on top of a
locked substrate cipher, not a re-tuning of the base fit?

## Honest Framing

K3 status: STRUCTURAL CLOSURE EXTENSION TEST (methodology as much as
numerics). Two claims are on the line:

1. **Cipher regression**: the scratchpad tensor cipher — G_p = 145/16,
   G_e = 145/768, G_n = 1/64, F_conn = Q_mass − 8·G(P) = (N−Z)·7093/192 —
   holds at Fraction equality on all 55 CR261 isotopes. This is a
   regression check on the second-set-of-eyes cipher: if any row deviates,
   the cipher does not hold at exact arithmetic and the CR fails at G0.

2. **Gated operators**: four candidate operators, each with a specific
   substrate motivation and a specific target family, must each pass a
   family-improvement gate. Adoption is per-operator; operators that
   don't improve their family are REJECTED.

The CR does not retract CR261 (which stays sealed BOUNDARY with the
same five-term BW form) and does not modify CR245 (asymmetry identity
theorem-grade). It ADDS a nuclear-readout correction layer with
transparent gate discipline.

## Locked Substrate Atoms (read-only from CR238, CR245, CR261)

```text
R = 12     D = 3     S = 8     alpha_H = 2
M = 126    L = 162   V = 27    Theta = 18
kappa = 7117/768      g = 1/64
mu_Q  = 192/7117 u
asymmetry_identity_coefficient = 7093²/(192·7117) ≈ 36.8181

Scratchpad tensor cipher (second-set-of-eyes, 2026-07-01):
  G_p = 145/16  = 9.0625
  G_e = 145/768 = 0.188802083…
  G_n = 1/64    = 0.015625

  G(P)   = Z·(G_p + G_e) + N·G_n
  Q_mass = 4·A·(7117/768)
  Q_sub  = 8·G(P)
  F_conn = Q_mass − Q_sub  =  (N − Z)·(7093/192)   (proposition to test)
```

## Locked Base Model K (from Phase 5)

```text
B_u_base(Z, N, A)
  = a·A
  − b·A^(2/3)
  − c·Z(Z−1)/A^(1/3)
  − d_locked·(N−Z)²/A               (CR245 theorem-grade, d = 7093²/(192·7117))
  − e·δ_pair(Z,N)·A^(−1/2)
  + α_quadZ·(−n_Z·(sp_Z − n_Z)/A)
  + α_quadN·(−n_N·(sp_N − n_N)/A)
  + α_cross·(−n_Z·(sp_Z − n_Z)·n_N·(sp_N − n_N)/A²)
  + α_prox·(−exp(−d_Z/3) − exp(−d_N/3))
  + α_lightodd·[A<40 and A odd]
  + α_alpha·(A/4)·[N=Z and A%4=0]
  + α_reonset·(rare-earth valence product, Z∈(50,82) AND N∈(82,126))
  + α_doubmag·[Z magic AND N magic]

where (a, b, c, e, α_i) are fitted on all 55 isotopes with d_locked
carried; MAGIC = {2, 8, 20, 28, 50, 82, 126};
n_X = X − magic_lower_of_X, sp_X = magic_upper − magic_lower,
d_X = min|X − m| over MAGIC.
```

## Locked Candidate Operators (four, each family-gated)

```text
O_82_precursor      feature = (Z−56)²·[N==82 AND Z>56]
                    family  = {isotopes with N=82 AND Z>56}
                    motive  = above-mid-shell Z valence erodes N=82 closure

O_3d_oddZ_pairing   feature = [Z odd AND 20<Z<30]
                    family  = odd-Z 3d transition metals (Mn, Co, Cu, …)
                    motive  = residual 3d-shell pairing debit not in SEMF δ

O_doubmag_saturation feature = [Z magic AND N magic AND A≥100]
                    family  = heavy doubly-magic isotopes
                    motive  = shell_prox linear form over-shoots at heavy DM

O_mid_shell_fill    feature = n_N·[28<Z≤50 AND 50<N<82]
                    family  = Z in upper 28-50 shell, N mid-shell 50-82
                    motive  = Z-shell fills while N valence still building
```

## Locked Fit Protocol

```text
Step 1: verify cipher regression on all 55 CR261 isotopes at Fraction
        precision (G0 gate).

Step 2: fit Model K (13 features) on all 55 rows with d = 7093²/(192·7117)
        locked. FREEZE the resulting coefficients as beta_K.

Step 3: for each operator O_i:
          - identify target family F_i by structural criterion (above)
          - compute γ_i = argmin over gamma of Σ_{r ∈ F_i} (residual_r − gamma · f_i(r))²
                = (Σ_{F_i} r·f_i) / (Σ_{F_i} f_i²)
            where residual_r = B_u_obs(r) − B_u_base(r; beta_K)
          - measure family_mean_improve
                = mean over F_i of ( |resid_baseline| − |resid_new| )
          - operator PASSES iff family_mean_improve > 2.0 MeV

Step 4: combine all PASSING operators. Since each feature is zero
        outside its family, they compose without interaction. No
        re-fitting of beta_K.

Step 5: compute final residuals; count |resid| ≤ 5 MeV isotopes.
```

## Sealed PASS Gates

```text
G0  Cipher regression: F_conn = Q_mass − 8·G(P) equals (N−Z)·(7093/192)
    exactly (Fraction equality) on all 55 isotopes.

G1  Base Model K fit RMS on all 55 isotopes ≤ 4.5 MeV.
    (Rationale: Phase 5 obtained 3.91; margin protects against numerical
    or fit-order sensitivity.)

G2  At least 3 of 4 candidate operators PASS the family-improvement
    gate (family mean_improve > 2 MeV).

G3  Final combined RMS across all 55 isotopes ≤ 3.5 MeV.
    (Rationale: Phase 6b obtained 2.72; margin against fit sensitivity.)

G4  Final ≥ 45/55 isotopes within |resid| ≤ 5 MeV (i.e. ≥ 81.8%).
    (Rationale: Phase 6b obtained 50/55 = 90.9%; margin protects against
    fit sensitivity.)

G5  Anchor cases remain within 10 MeV residual under the final
    combined model: O-16, Fe-56, Au-197, Pb-208 (all IN the
    55-row CR261 dataset).

G6  Precommit hash verified at runner load. All input files match locked
    SHA256s. Forbidden-file open() guard not tripped.

PASS      iff G0 AND G1 AND G2 AND G3 AND G4 AND G5 AND G6 all hold.

BOUNDARY  iff G0 AND G6 hold AND at least two of {G1, G2, G3, G4} hold,
          but not all four; OR G5 misses on one anchor by ≤ 5 MeV.

FAIL      iff G0 fails (cipher deviates) or G6 fails (whitelist/hash)
          or fewer than two of {G1, G2, G3, G4} hold.
```

## Reported Evidence (not gated)

```text
E1  Per-isotope base residuals (Model K) and final residuals (Model K
    + adopted operators), with A, Z, N, family membership flags.

E2  Fitted γ_i for each operator, family size |F_i|, family mean_improve,
    and adoption decision.

E3  Structural note on each operator's substrate motivation (which is
    NOT a gate — the operators earn adoption on family-improvement, not
    on the elegance of their motivation).

E4  Sensitivity: 5-fold CV RMS of the final combined model, reported
    as a diagnostic (NOT gated; the frozen-base composition doesn't have
    a straight CV interpretation since operators are added per-family).

E5  List of remaining outliers (|resid| > 5 MeV) with Z, N, A, and a
    short note on what structural feature they might correspond to
    (for Phase 7 candidate operators).
```

## Pre-Registered Frozen Inputs

| field | sha256 | description |
| --- | --- | --- |
| CR261_bw_fit_per_row.csv | `3212a36064244e6addc30e465af6577d68df7997715f6c68ff9bb983b0d8eef2` | 55-row CR261 fit dataset |

The runner whitelists exactly this input plus the precommit and runner
source.

## Rule-9 Line

```text
This test could have falsified the claim that the second-set-of-eyes
tensor cipher (G_p = 145/16, G_e = 145/768, G_n = 1/64) holds at exact
Fraction arithmetic on all 55 CR261 isotopes AND that four gated,
family-scoped candidate operators — layered on a frozen Model K base
— reduce the CR261 binding-closure residual below 3.5 MeV RMS while
covering ≥ 45 of 55 isotopes within 5 MeV. It could have failed by:
(i) cipher deviating on any row, (ii) base Model K exceeding 4.5 MeV
RMS, (iii) fewer than 3 operators passing family-improvement, (iv)
combined RMS exceeding 3.5 MeV, (v) fewer than 45 isotopes within
5 MeV, (vi) anchor cases failing, or (vii) whitelist/hash gate tripping.
```

## What This CR Seals

If PASS: the CR261 gap is closed at CR245-grade precision by a
gated nuclear-readout layer. The SAM tensor cipher stays sealed;
adoption of each operator is transparent, per-family, and
independently reversible; and the ratio of family-improvement to
side-effects is auditable at operator granularity.

If BOUNDARY: the methodology is validated even where some operators
don't adopt or where combined RMS falls short — future Phase 7 work
can propose additional gated operators for the remaining outliers
without retracting anything sealed here.

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR245@09a (asymmetry identity theorem-grade) | per branch HASHES |
| CR248@09a (four-particle algebraic spine BOUNDARY) | precommit `7ad11ca64fb62bfef6d6671f7bfb6defc333e6bdb720c59737c555886a648aaa` |
| CR261@09a (pair-write BW extension BOUNDARY) | precommit `5b2d07b5c1447c39c221e4a53febeff6b379acfae6788cb675970017acfe2001` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
