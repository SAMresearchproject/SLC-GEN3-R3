# SAM Master Formula Sheet — Primitives, Constants, Full Derivation DAG

**Sean Brady, 2026-06-28**
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

This is the master derivation reference. Companion to the quick-reference
[SAM_CHEAT_SHEET_2026_06_28.md](SAM_CHEAT_SHEET_2026_06_28.md). The cheat sheet
is a surface; this sheet shows the closed-form identity for every sealed
quantity, **what each identity depends on**, and the CR that locks it.

---

## 1. Primitive Basis

```text
                    ĥ   ⊥   d̂   ⊥   π
```

| Axis | Symbol | Value | Role |
| --- | --- | ---: | --- |
| binary readout | ĥ ≡ α_H | 2 | rational sector |
| dimensional readout | d̂ ≡ D | 3 | rational sector |
| route completion | π | π | accumulation axis |

**Closure selector** (Volume I §4.1, locked by CR238@09a as unique
small-integer solution):

```text
        d̂^(d̂ − 1) = ĥ^d̂ + 1
        3^2        = 2^3 + 1     →  (ĥ, d̂) = (2, 3)
```

CR258@09a primitive-closure audit (`942b42dd…`) verifies that every named
SAM quantity reduces to `f(ĥ, d̂) · π^k` for `k ∈ {0, ±1}`.

---

## 2. Layer 1 — Rational Substrate Atoms (no π)

All from {ĥ, d̂} alone:

| Atom | Closed form | Value | Role |
| --- | --- | ---: | --- |
| split inventory | S = ĥ^d̂ | 8 | binary face states |
| dim square | d̂² | 9 | dimensional bridge |
| write cell | 𝒱 = d̂^d̂ | 27 | resolved cell |
| carrier face | ℱ = d̂^(d̂+1) | 81 | per-side capacity |
| route radix | R = ĥ²·d̂ | 12 | radix |
| writable capacity | R² = ĥ⁴·d̂² | 144 | union of two sides |
| tensor bridge | Θ = ĥ·d̂² = R²/S | 18 | overlap (graviton) |
| closed ledger | ℒ = ĥ·ℱ | 162 | both sides total |
| matter capacity | M = R² − Θ = ĥ·d̂²·(ĥ³−1) | 126 | symmetric difference |
| symmetric debit | 2Θ = ℒ − M | 36 | overlap doubled |

**Inclusion-exclusion identity** (CR229@09a sealed):

```text
  |Side₁| + |Side₂| = ℒ   = 162
  |Side₁ ∪ Side₂|  = R²  = 144   (capacity)
  |Side₁ ∩ Side₂|  = Θ   = 18    (graviton overlap)
  |Side₁ ∆ Side₂|  = M   = 126   (matter writable)
  ℒ − M             = 2Θ  = 36
  M/R² = 7/8       (retained share)
  Θ/R² = 1/8 = ĥ^(−d̂)  (tensor share)
```

**Four-way 6-identity** (CR036@19 load-bearing for η_SAM exponent):

```text
  6 = ĥ·d̂ = R/2 = Θ/d̂ = ℒ/𝒱
        2·3   12/2   18/3   162/27
```

This is the closed-ledger → write-cell reducer. Used as the **exponent** in
A_0^6 in the η_SAM closed form (§5.1).

---

## 3. Layer 2 — Rational Ratios and Shares

| Constant | Closed form | Value | First use |
| --- | --- | ---: | --- |
| positive charge coef | c₊ = 1 + 1/ĥ² | 5/4 | CR254 matter charged |
| negative charge coef | c₋ = 1 + 1/ĥ | 3/2 | CR254 matter charged |
| tensor share | ĥ^(−d̂) = Θ/R² | 1/8 | CR255 matter neutral |
| retained share | 1 − ĥ^(−d̂) = M/R² | 7/8 | CR255, CR255 holdout |
| neg A-conjugate base | c₊/c₋ | 5/6 | CR256 antimatter |
| pos A-conjugate base | c₋/c₊ | 6/5 | CR256 antimatter |
| bigrade alphabet | {ĥ^a·d̂^b : (ĥ^a·d̂^b)² ≤ R²} | {1,2,3,4,6,8,9,12} | promoter q-set |
| bigrade sum | d̂²·(ĥ+d̂) = 45 | 45 | CR218 hidden source |
| lifted connector | L_p = p + p²/R² | L_6 = 25/4 | binding closure |

**Connector-12 closure:** `L_12 = 12 + 144/R² = 13` (R+1 collapse).
**Forbidden local fee:** `L_18 = 20.25` (excluded as connector).

---

## 4. Layer 3 — Accumulation (π enters)

Accumulation atoms are rational-times-π^k for k ∈ {0, ±1}:

| Quantity | Closed form | Value | First use |
| --- | --- | ---: | --- |
| floor | A_0 = 𝒱/(π·ĥ·ℒ) = 1/(π·R) | 1/(12π) ≈ 0.02653 | CR001@A0a |
| route share | A_share = π·A_0 = 1/R | 1/12 | distance road |
| side share | A_side = A_share/2 | 1/24 | half-side |
| matter density | Ω_m = R·A_0 = ĥ/(2π) | 1/π ≈ 0.31831 | CR018@07, CR019@07 |
| baryon mix | χ = (S/d̂)·A_0 | 2/(9π) ≈ 0.07074 | CR018@07 |
| baryon density | Ω_b = 2·A_0·(1−χ) | ≈ 0.04930 | CR018@07 |
| cold-DM density | Ω_c = Ω_m − Ω_b | ≈ 0.26901 | CR036B@19 |
| dark-energy density | Ω_Λ = (π−1)/π | ≈ 0.68169 | CR002@19 (fate) |
| halo asymptote | X_∞ = (R−ĥ)·Ω_m | 10/π ≈ 3.1831 | CR025/CR031b@08 |

**Dual form for A_0:** the cancellation `𝒱/(π·ĥ·ℒ) = (ℒ/6)/(π·ĥ·ℒ) =
1/(6·π·ĥ) = 1/(12π)` is the load-bearing route-completion identity.

---

## 5. The η_SAM → H_0 → Perturbation → CMB Chain (CR036/CR037A/CR037B)

This is the parameter-free CMB closure. Every input is a substrate atom
or a declared dimensional anchor (T_CMB FIRAS + CODATA/SI constants).

### 5.1 η_SAM identity (CR036@19, PASS)

```text
  η_SAM = (M / (ĥ² · Θ)) · A_0^(ℒ/𝒱)
        = (126 / (4 · 18)) · (1/(12π))^6
        = (7/4) · (1/(12π))^6
        = 7 / (4·(12π)^6)
        ≈ 6.0961 × 10⁻¹⁰         (−0.37% vs Planck 6.119e-10)
```

Atoms used: M=126, ĥ=2, Θ=18 → ratio 7/4. Exponent ℒ/𝒱 = 162/27 = 6
(four-way identity §2). No fitted exponent.

### 5.2 Dimensional bridge (CR036@19, declared, not fitted)

Declared non-fitted anchors (NOT prior CR results):

```text
  T_CMB = 2.7255 K              (FIRAS thermal anchor)
  c     = 299 792 458 m/s        (SI exact)
  h     = 6.626 070 15 × 10⁻³⁴ J·s   (SI exact since 2019)
  ℏ     = h/(2π)                 (in-runner derivation)
  k_B   = 1.380 649 × 10⁻²³ J/K  (SI exact)
  G     = 6.674 30 × 10⁻¹¹ m³/(kg·s²)  (CODATA 2018)
  Mpc   = 3.085 677 5815 × 10²² m
  m_b   = m_p = 1.672 621 924 × 10⁻²⁷ kg  (CODATA 2018)
```

In-runner conversion `K_η→ω_b` (first-principles, **not** hardcoded):

```text
  n_γ           = (2·ζ(3)/π²) · (k_B·T_CMB/(ℏ·c))³    (Planck blackbody)
  ρ_crit(h=1)   = 3·(100 km/s/Mpc)² / (8π·G)
  K_η→ω_b       = ρ_crit(h=1) / (m_b · n_γ)            (~2.735e-8)
```

### 5.3 H_0,SAM cascade (CR036@19, PASS)

```text
  ω_b,SAM = η_SAM / K_η→ω_b
  h_SAM²  = ω_b,SAM / Ω_b,SAM        with Ω_b,SAM = 2·A_0·(1−χ)
  H_0,SAM = 100 · h_SAM
          ≈ 67.2504 km/s/Mpc          (−0.16% vs Planck 67.36)
```

### 5.4 Perturbation triplet (CR037A@19, PASS, STRONG_CONTACT)

```text
  A_s,SAM = η_SAM · √R = (7/4)·(12π)⁻⁶·√12
                       ≈ 2.1117473568 × 10⁻⁹
  n_s,SAM = 1 − χ/2     = 1 − 1/(9π)
                       ≈ 0.9646322349
  τ_SAM   = 2·A_0       = 1/(6π)
                       ≈ 0.0530516477
```

All three land inside the Planck posterior at ≤ 0.5σ STRONG_CONTACT.

### 5.5 Parameter-free CMB shape (CR037B@19, PASS)

With **only** the SAM cascade above (densities + H_0 + A_s + n_s + τ)
plus the disclosed ancillary inputs (T_CMB FIRAS, N_eff=3.046,
k_pivot=0.05 Mpc⁻¹, m_ν,sum=0.06 eV Planck-baseline) fed into CAMB 1.6.6:

| Spectrum | χ²/dof | Verdict |
| --- | ---: | --- |
| TT | 1.0339 | PASS |
| TE | 1.0454 | reported |
| EE | 1.0430 | reported |

Peak deltas (theory − Planck): Δℓ₁ = 1, Δℓ₂ = 15, Δℓ₃ = 2.

**Free parameters introduced: 0. No optimizer.**

### 5.6 z_eq cascade (CR036 E5)

```text
  z_eq + 1 = ω_m,SAM / (ω_γ · (1 + 0.2271·N_eff))
  ω_γ      computed in-runner from T_CMB blackbody
```

---

## 6. Distance-Road Chain (06_DISTANCE_ROAD_*)

### 6.1 Native ruler-road kernel (CR012@06, PASS)

```text
  A_los(z) = (1/π) · (1 − (1+z)^(−d̂))        [shrinkage kernel]
  A_los,max = 1/π                              [z → ∞ saturation]
```

### 6.2 Pure SN distance (CR013@06, CR018b@06, PASS)

```text
  μ_native(z) = μ_obs(z) + 5·log₁₀(1 − A_los(z))
```

- 1701 Pantheon rows; no offset fit, no host-mass correction.
- CR018b at H_0=73.04 (SH0ES): weighted residual −0.00907 mag.

### 6.3 BAO (CR014@06, CR018b@06, PASS)

```text
  w        = (d̂/R) · (Ω_b/Ω_PBH/A)
  r_drag   = r_*·(1 + w)
  r_d,SAM ≈ 147.769 Mpc                       (+0.461% vs Planck 147.09)
  DESI DR1: χ²/n ≤ 2.5 over 12 distance ratios
```

### 6.4 CMB compressed (CR019@07, CR016@06, PASS)

```text
  100·θ_*  = r_s(z_*)/D_M(z_*) = 1.04740     (+0.605% vs Planck 1.04110)
  ℓ_A      = π/θ_* = 299.942                 (−0.602% vs 301.760)
  r_d      = 147.769 Mpc                     (+0.461% vs 147.090)
```

### 6.5 Big Bang acoustic / thermal clock (CR001c@19, CR019@07)

CR019 compressed clock products:

```text
  z_eq = 3596.43      z_* = 1091.22       z_d = 1023.34
  r_s(z_*) = 141.778 Mpc                  D_M(z_*) = 13 536.18 Mpc
```

Peebles three-level recombination + corrected Thomson optical-depth
integrand `1/(a·H)` (CR001c@19 PASS, reproduces Planck acoustic geometry
within 5%).

### 6.6 Fate identity (CR002@19, PASS)

```text
  Ω_Λ = (π − 1)/π
  H_∞,native  = H_0 · √((π−1)/π)
  H_∞,readout = H_0 · [(π−1)/π]^(3/2) ≈ 38.70 km/s/Mpc   at H_0 = 68.76
```

---

## 7. Local Gravity Chain (02–05)

### 7.1 A-kernel (CR003@02, weak-field PASS via CR004; strong-field
CR007/CR008 BOUNDARY; CR009/CR010 contact via CR011 zipper)

```text
  A(r) = r_s/r           r_s = 2GM/c²
  Φ    = −GM/r           (weak-field limit)
```

### 7.2 Horizon landmarks (CR007–CR011@05)

```text
  Horizon         A(r_s)       = 1
  Photon sphere   A(1.5·r_s)   = 2/3
  ISCO            A(3·r_s)     = 1/3
```

### 7.3 Horizon → cosmic projection (CR003@19, PASS)

```text
  A_0 = A_horizon / (4π·d̂) = 1/(12π) = 1/(π·R)
```

Local A=1 closure and cosmic A_0 are the same identity at different scales
(SAM Homes: every A=1 full-local-closure is one substrate primitive; no
hierarchical "universe contains BHs" framing).

### 7.4 Distance-road bridge (CR012@06)

A_0, w, r_drag frozen from CR001@A0a + CR003@02. No SN/BAO/CMB target
selection at lock time.

---

## 8. Matter Sector (09a_PARTICLE_MASS_CHAIN, particle-side)

### 8.1 Particle promoter (CR253@09a, BOUNDARY — core PASS, W3/W4 subsumption)

```text
  promoted(r) ⟺ bin(r) ∈ {stable_matter, antimatter_conjugate}
              AND h_T(r) ∈ {0, 1}
  → 80 rows = 48 matter + 32 antimatter (from 299-row QP093A catalog)
```

### 8.2 Compact matter laws (CR254/CR255/CR256/CR257)

| Sector | Rows | Closed form | CR |
| --- | ---: | --- | --- |
| matter charged | 32 | `qA = R^d · c_s · p · (1 + p/R²)`, c_s=c₊ or c₋ | CR254 PASS |
| matter neutral | 16 | `qA = (p/8)·R^d`, 1/8 = Θ/R² | CR255 PASS |
| anti charged | 32 | `qA_anti = qA_matter · A_conj` | CR256 PASS |
| d=1 reduction (anti, neg) | — | `R·(5/4)·p·(1+p/R²)²` | CR257 |
| d=1 reduction (anti, pos) | — | `R·(3/2)·p·(1−p²/R⁴)` | CR257 |

A-conjugate operator:

```text
  A_conj(neg, p, d) = (5/6) · (1 + p/R^(d+1))
  A_conj(pos, p, d) = (6/5) · (1 − p/R^(d+1))
```

**Hard-zero falsifier (CR256):** `qA_anti(pos, p=12, d=0) = 0` exactly.
Confirmed at row QP093A-0088.

### 8.3 Higgs reveal (CR120b@09a + foundation, PASS)

```text
  H_reveal = R²·(1 − 2^(−d̂)) − d̂²/R
           = 144·(7/8) − 9/12
           = 126 − 0.75
           = 125.25 GeV          (PDG 2024: 125.20 ± 0.11 GeV — inside 1σ)
```

Capacity 126 = M (CR114@14 binary face-state split); surface debit
d̂²/R = 3/4 (foundation algebra). Zero free parameters.

### 8.4 Proton mass (CR009@18, PASS)

**Connection-fee K1 reveal**:

```text
  M_obs / M_native = 1 + offset(q)/R          [triadic, n_conn = 2]
  offset(q)        = q + d̂ = q + 3
  pair (n_conn=1)  offset = 0                 [first-connection free]
```

- 31/31 derivation rows exact match.
- 6/6 extension blind prediction (q ∈ {5,6,7,9}) exact.
- Proton: PDG 938.272 MeV → SAM 937.96 MeV, **Δ = 0.03%**.

---

## 9. Nuclear Sector (09a — κ, channel split, binding)

### 9.1 κ derivation (CR221@09a, PASS — bit-identical re-derived in CR238@09a)

```text
  κ_floor = (q_Ap + q_Ae + q_An)/8
          = (145/2 + 145/96 + 1/8)/8
          = 7117/768
  g       = 1/S² = 1/64
  G(P)    = Z·κ_floor + (N−Z)/64
  GR(P)   = 8·G(P)
```

Component writes only; **no PDG mass inputs**. CR238 typed re-derivation:

```text
  κ = (R−1)·(ℱ·S − 1) / (d̂·ĥ^S)
    = 11·647 / (3·256)
    = 7117/768                  (bit-identical to CR221)
```

### 9.2 Typed channel split (CR238/CR240@09a, PASS)

```text
  Q_mass = 4·A·κ
  Q_sub  = S·(Z·κ + (N−Z)·g)
  dQ     = Q_mass − Q_sub
         = (N−Z) · (4κ − S·g)
         = (N−Z) · 7093/192
```

### 9.3 Binding asymmetry-term identity (CR245@09a Stage 1, BOUNDARY)

```text
  (Q_mass − Q_sub)² / Q_mass ≡ (N−Z)²/A · 7093²/(192·7117)
```

Theorem-grade structural derivation; Stage 1 closed exact on 71 rows.
Other 4 Bethe-Weizsäcker shapes remain phenomenological.

### 9.4 Second-layer SOB inverse (CR247@09a, STRONG_PASS)

```text
  Φ(Z,N)   = Z·φ_balanced + (N−Z)·φ_excess        N ≥ Z
  φ_balanced = (u=3, d=3, e=1, Q_mass=8κ, Q_sub=8κ, dQ=0)
  φ_excess   = (u=1, d=2, e=0, Q_mass=4κ, Q_sub=1/8, dQ=4κ−1/8)
```

Reproduces SOB target exact on 69/69 rows under `Fraction` arithmetic;
dQ identity (N−Z)·7093/192 confirmed exact.

### 9.5 Binding closure (full BW with substrate-derived coefficients)

```text
  B_u⁽⁰⁾ = S·A
         − (Θ−1)·A^(2/3)
         − (d̂²/R)·Z(Z−1)/A^(1/3)
         − ĥ·(R−1)·(N−Z)²/A
         + (S−1)·δ/√A
         − L_6·Λ

         = 8·A − 17·A^(2/3) − (3/4)·Z(Z−1)/A^(1/3)
                            − 22·(N−Z)²/A + 7·δ/√A − (25/4)·Λ
```

---

## 10. Galaxy Halo Chain (08_GALAXY_HALOS_*)

### 10.1 Radial halo law (CR025/CR031b@08, PASS, p = 0.000999)

```text
  X(r) = V_dark²(r) / V_bar²(r)
```

Monotonic rise from baryon-dominated inner to bound-halo plateau across
175 SPARC galaxies / 3391 points.

### 10.2 Asymptote identity (CR025@08, sealed; CR031b@08 confirmed)

```text
  X_∞,SAM = (R − ĥ) · Ω_m = 10/π ≈ 3.1831
```

### 10.3 Per-galaxy halo mass (CR032@08, PASS; CR033@08 follow-up)

```text
  M_halo(<R_outer) = R_outer · X_∞ · V_bar²(R_outer) / G
```

Median ratio (population): CR032 = 0.9983 on 173 SPARC galaxies;
CR033 = 0.9993. Zero per-galaxy free parameters.

### 10.4 Native halo concentration / classes

```text
  c_SAM = 1 / ρ_{1/2}        median 1.063
```

6 classes across 175 galaxies: 94 late-saturating, 58 early-saturating,
15 rising-edge, 3 intermediate, 3 baryon-dominated inner-closure, 2
disturbed/non-closed.

---

## 11. Neutrino Selector (20_NEUTRINO_SELECTOR/CR001, PASS)

### 11.1 Splittings ratio

```text
  ratio_selector = ((ĥ·d̂)² − 1) / (ĥ − 1)
                 = (36 − 1) / (2 − 1)
                 = 35                          (measured: 33.895, +3.26%)
```

### 11.2 Mass pattern

```text
  m₁ : m₂ : m₃ = 1 : √ĥ : (ĥ·d̂)
              = 1 : √2 : 6
```

With Δm²₃₁ = 2.515×10⁻³ eV² anchor:

```text
  m₁ = 8.477 meV    m₂ = 11.988 meV    m₃ = 50.861 meV
  Σm_ν = 71.326 meV               (40.56% below Planck 120 meV bound)
```

---

## 12. Periodic Table / Isotope Vault (CR119@09a, CR065–CR072@10)

```text
  Z ─→ (N_SOB, A_SOB) ─→ P = Z·p + N·n + Z·e
       ─→ (G_sub, Q_sub, Q_mass, χ) ─→ SOB workbook lanes
```

CR119@09a generates the 299-row QP093A vault that is the input catalog
for CR253–CR258. Sealed: 2026-06-15, PASS.

Carrier T13 multiset (CR238 spine, CR229 closure):

```text
  T13 = {1, 1, 2, 3, 4, 6, 8, 8, 9, 9, 12, 18, 81}
  Σ T13 = 162 = ℒ                       (partition sum = closed ledger)
  Σ (non-Z lanes) = 81 = ℱ              (carrier face)
  fold: 114 + 12 = 126 = M              (substrate-closed + non-Z)
```

---

## 13. Full Derivation DAG

```text
                  ĥ = 2          d̂ = 3          π
                     \              |             /
                      \             |            /
                       \____________|___________/
                                    |
                       Rational atoms (S, ℱ, 𝒱, R, R², Θ, ℒ, M)
                                    |
              ┌─────────────────────┼─────────────────────┐
              |                     |                     |
     Layer-2 ratios         Layer-3 accumulation     Closure axiom
     (c₊, c₋, 1/8,          (A_0, A_share,           d̂^(d̂−1) = ĥ^d̂ + 1
      5/6, 6/5,             A_side, Ω_m, χ,          (locks ĥ=2, d̂=3
      bigrade)              Ω_b, Ω_c, Ω_Λ, X_∞)      uniquely)
              |                     |                     |
              |                     |                     |
              ↓                     ↓                     ↓
       09a matter laws        Distance-road           CR258 audit
       (CR254/CR255/          (CR012-CR017,           (36 quantities
        CR256/CR257)          CR018b/CR019)            reduce, all)
              |                     |
              |                     ├──→ CR018@07 (Ω_b derivation)
              |                     ├──→ CR019@07 (Ω_m refinement)
              |                     └──→ CR036@19 (η_SAM, H_0_SAM)
              |                                |
              |                                ├──→ CR037A (A_s, n_s, τ)
              |                                |        ↓
              |                                └──→ CR037B parameter-free
              |                                     CMB shape (PASS, χ²/dof = 1.034)
              |
              ├──→ CR114@14 binary face-state split (capacity 126)
              ├──→ CR221@09a (κ_floor = 7117/768) ──→ CR238@09a (typed spine)
              |                                            |
              |                                            ├──→ CR240@09a (Q_mass = 4Aκ)
              |                                            ├──→ CR243/244@09a (typing)
              |                                            ├──→ CR245@09a (binding stage 1)
              |                                            └──→ CR247@09a (Φ inverse)
              |
              ├──→ CR229@09a inclusion-exclusion identity
              |    (substrate = closed ledger 162; capacity 144;
              |     matter 126; graviton 18)
              |
              ├──→ CR009@18 connection-fee (proton 0.03%)
              |    [(R+q+D)/R triadic; first-connection-free pair]
              |
              ├──→ CR120b@09a Higgs reveal (126 − 0.75 = 125.25 GeV)
              |
              ├──→ CR003@02 A-kernel ──→ CR009/CR010@05 horizon landmarks
              |    [A(r) = r_s/r;  photon sphere A=2/3;  ISCO A=1/3]
              |    ──→ CR003@19 horizon → cosmic projection A_0 = A_horizon/(4πd̂)
              |
              ├──→ CR025/CR031b@08 X(r) law; X_∞ = 10/π
              |    ──→ CR032/CR033@08 per-galaxy halo mass
              |
              ├──→ CR001@20 neutrino selector (ratio 35; Σmν = 71.3 meV)
              |
              └──→ CR002@19 fate identity (H_∞,readout = H_0·[(π−1)/π]^(3/2))
```

---

## 14. The Dimensional Bridge — When π and Atoms Meet Measured Units

Substrate atoms are dimensionless. Carrying them to SI requires a
**declared, non-fitted** anchor set (CR036@19, CR005@03/CR005@18):

| Anchor | Value | Source | Purpose |
| --- | --- | --- | --- |
| T_CMB | 2.7255 K | FIRAS | thermal anchor (η → ω_b) |
| c | 299 792 458 m/s | SI exact | length-time |
| h | 6.626 070 15 × 10⁻³⁴ J·s | SI exact | energy-frequency |
| k_B | 1.380 649 × 10⁻²³ J/K | SI exact | thermal energy |
| G | 6.674 30 × 10⁻¹¹ m³/(kg·s²) | CODATA 2018 | Friedmann critical density |
| Mpc | 3.085 677 5815 × 10²² m | parsec | cosmological length |
| m_p | 1.672 621 924 × 10⁻²⁷ kg | CODATA 2018 | baryon mass |
| N_eff | 3.046 | standard radiation | z_eq cascade |

These never enter as fitted parameters. They are the unit-bridge from
substrate counts to laboratory measurements.

---

## 15. Provenance Hash Chain

| Artifact | SHA-256 |
| --- | --- |
| Stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
| CR258 sealed audit (primitive closure) | `942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7` |
| SAM_UNIFICATION_NOTE_2026_06_28.md | `8c7029c607b7a1c6acf5741517e8811fab62a574e6f79bc9278c2ee3989bda28` |
| SAM_PRIMITIVE_BASIS_2026_06_28.md | (companion) |
| SAM_VOLUME_II_1_MATTER_UPDATE_2026_06_28.md | `0279ea3028da9785fcf22146f53a255cb0bfb68eccebc4c2f26ac0c5957a5da2` |
| CR037B precommit | `5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b` |
| CR037A precommit | `1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78` |
| CR036 precommit | `345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2` |

Per-CR HASHES.txt sidecars live in each CR folder.

---

## 16. What "Zero Free Parameters" Means Here

Across every chain above, the count of fitted parameters is:

| Chain | Free parameters fitted |
| --- | ---: |
| Compact matter laws (CR254/255/256/257) | 0 |
| Particle promoter (CR253) | 0 |
| Higgs reveal (CR120b) | 0 |
| Proton mass (CR009@18) | 0 |
| κ derivation (CR221/238) | 0 |
| Binding asymmetry term (CR245) | 0 |
| SOB inverse Φ(Z,N) (CR247) | 0 |
| Distance road (CR012-CR017) | 0 |
| Ω_b, Ω_m, A_0 (CR018/019/036) | 0 |
| η_SAM (CR036) | 0 |
| H_0,SAM (CR036) | 0 |
| Perturbation triplet A_s, n_s, τ (CR037A) | 0 |
| Parameter-free CMB shape (CR037B) | 0 |
| Galaxy X(r), X_∞, halo mass (CR025-CR033) | 0 |
| Neutrino selector (CR001@20) | 0 |
| Fate identity (CR002@19) | 0 |

The declared dimensional anchors (T_CMB, c, h, k_B, G, Mpc, m_p,
N_eff) are unit-bridge inputs, not fitted parameters.

---

```text
                    ĥ   ⊥   d̂   ⊥   π
```
