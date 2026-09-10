# SAM on Earth — Frame Reference v1.0 (REDACTED for CR013 DERIVER context)

**Sean Brady** · SAM Research Project LC · Frame reference draft: 2026-07-02
Repository record: `C:\VS\The_Courtroom`
License: Proprietary, all rights reserved; see `LICENSE.md`.

**Status:** DRAFT v1.0. This document is a foundational reference, not a derivation and not a CR. It consolidates the Earth-frame tie-downs already earned in Volume I §2 and pre-existing STAM v1.0 test code, and it establishes the SI-unit lock every downstream laboratory-scale SAM prediction cites.

---

## 0. Purpose

Every laboratory-scale SAM prediction needs to answer one question before anything else: *is my prediction in SI meters, seconds, and kilograms, or is it in "SAM units" that require rescaling to reach the lab?* Volume I §4 says c is the substrate's tooth-rate and that "measurable distance" changes cosmologically; it does not spell out what that means at laboratory scale. This reference does.

**Claim of this document (single sentence):** at Earth-surface conditions (A ≤ 1.4 × 10⁻⁹), SAM predictions in SI meters are indistinguishable from SAM predictions in "SAM units" to better than 10⁻⁹, and every downstream laboratory CR states its numbers in SI units without rescaling.

That is not a new derivation. It is the honest reading of Vol I §2 (weak-field kernel), Vol I §4 (invariant c and cosmological road integrals), and CODATA/SI (definitional c since 1983), together with the empirical confirmation the STAM Model-A GPS test already produced. This document assembles those pieces into one citable handle so future lab CRs can lock the frame in a single line of provenance.

**What this document is NOT.** It is not a rederivation of Vol I. It is not a proposal for new physics. It is not a claim that SI is "correct" — SI is the operational unit system the lab measures in, and Vol I §4 already recovered every relevant Earth-scale observable in that same operational frame. This document formalizes that operational fact as a locked reference.

---

## 1. The Earth Frame — SI units, no rescaling

**SI** = *Système International d'unités* — the International System of Units. It is the standard scientific unit system used globally since 1960 (metre, kilogram, second, ampere, kelvin, mole, candela and their combinations). Since 1983 the metre is defined via a fixed value of the speed of light in vacuum, and since 2019 all seven SI base units are defined through fixed values of seven fundamental constants (c, h, e, k, N_A, ΔνCs, K_cd). "SI meters" and "SI seconds" in this document mean the same units every laboratory in the world measures with; no conversion factor separates them from the meters and seconds of any physical instrument.

The lab-scale SAM operational frame carries these definitions verbatim from the international standards, hash-locked below:

```text
c        =  299_792_458           m/s   (SI, defined exactly since 1983)
G        =  6.67430e-11           m³·kg⁻¹·s⁻²   (CODATA 2018)
ℏ        =  1.054571817e-34       J·s   (SI, defined exactly since 2019)
u        =  1.66053906660e-27     kg    (CODATA 2018 unified atomic mass unit)
m_e      =  9.1093837015e-31      kg    (CODATA 2018 electron mass)
m_p      =  1.67262192369e-27     kg    (CODATA 2018 proton mass)
1 u in MeV/c²  =  931.49410242    MeV/c² (CODATA)
GM_Earth =  3.986004418e14        m³/s²  (WGS84 geocentric gravitational constant)
R_Earth  =  6_378_137.0           m      (WGS84 equatorial radius)
U₀/c²    =  6.969290134e-10       (dimensionless; effective geoid potential magnitude
                                    per unit c²; used in GPS relativity treatments)
```

**Read rule.** Any downstream SAM lab CR that predicts a numeric outcome in meters, seconds, kilograms, hertz, joules, or their combinations reads its constants from this table.

---

## 2. The A-budget at laboratory scale

The accumulation kernel A(r) = r_s/r = 2GM/(c²r) evaluated at Earth surface and points of interest for laboratory experiments:

```text
A₀ (cosmic [REDACTED], SAM)    =  1/(12π)              =  2.6526e-2   (dimensionless)
Galactic potential at Sun      ≈  10⁻⁶                                  (order estimate)
Solar potential at 1 AU        ≈  1.97e-8                              (2GM_Sun/(c²·1 AU))
Earth potential at surface     ≈  1.39e-9                              (2GM_Earth/(c²·R_Earth))
Effective geoid (U₀/c²)·2      ≈  1.39e-9                              (used in GPS treatments)
```

**Load-bearing observations:**

1. **The Earth-surface A is one part in 10⁹.**
2. **The A gradient over apparatus-scale altitudes is one part in 10¹⁵ per meter.**
3. **The cosmic [REDACTED] A₀ = 1/(12π) never enters a local measurement**, per Vol I §2's proof that a value common to two clocks cancels in their comparison and a value with no slope contributes exactly zero force.

---

## 3. The SI unit lock (the sentence)

**"The SI meter is realized through locally measured c, fixed at 299,792,458 m/s exactly since 1983. Any SAM prediction at Earth surface expressed in SI units is expressed in SAM units to better than 10⁻⁹. Any uniform substrate rescale of lengths cancels in the dimensionless ratio d_ref/d on which SAM's laboratory coupling laws depend; residual local-well gradients (≤ 10⁻⁶ from galactic, ≤ 10⁻⁸ from solar, ≤ 10⁻⁹ from Earth-surface potential) sit more than four orders below any downstream ×3 tolerance and are recorded here as negligible."**

This is the sentence downstream lab CRs cite verbatim when they need the frame lock in a single line.

**What the sentence excludes:** the sentence does *not* say c is a fundamental constant of nature (SAM says c is the tooth-rate of the substrate). It does *not* say SI meters are the "true" length (SAM has no such notion). It says only that Earth-frame SI meters are the operational unit system in which SAM's laboratory predictions are expressed, and that any substrate-native length rescale cancels in the ratios SAM's coupling laws actually depend on. That is a much narrower and much stronger claim than an ontological one.

---

## 4. Earned confirmations from Volume I §2 (cited, not rederived)

Vol I §2 already recovered four Earth-scale observables from the same kernel with the same SI-frame reading, and each of those is an existing K1-anchor confirmation that the frame lock works in practice. Cited here as the empirical backing for §3:

| observable | SAM reading | agreement with observation | Vol I §2 reference |
|---|---|---|---|
| Weak-field gravity g at Earth surface | −GM/r² from ∇A · c²/2 | recovers Newtonian gravity exactly | §2 "gravity is the slope of the hill" |
| GPS clock rate at orbit vs geoid | dτ/dt = √(1−A) → 38 μs/day gain at GPS altitude | parts-in-10⁹ agreement engineered around | §2 "a clock is the altitude"; STAM Model-A §6 |
| Shapiro delay at solar limb (Cassini) | Δt_A = (1/c) ∫ A ds | parts-in-10⁵ agreement with radar | §2 "light is the road across the hill" |
| Light bending at solar limb | 1.751″ from line integral of A | 1919 Eddington confirmation onward | §2 "bending starlight at 1.751 arcseconds" |

Every entry above uses the SI-frame reading of c, G, M, r that this reference locks. None required a substrate rescaling to reach the observed number.

---

## 5. STAM Model-A GPS test — an existing empirical implementation

The STAM v1.0 test suite already implements the Earth-frame reading of the SAM kernel numerically.

Excerpt (constants and kernel):

```python
C = 299_792_458.0
MU_EARTH = 3.986004418e14
R_EARTH = 6_378_137.0
GPS_RADIUS = 26_560_000.0
U0_OVER_C2 = 6.969290134e-10

def accumulation_spherical(r_m: float) -> float:
    return 2.0 * MU_EARTH / (C**2 * r_m)
```

The weak-field clock mapping `dτ/dt ≈ 1 − A/2` is applied at GPS orbit against the effective geoid, added to the kinematic circular-orbit correction `−v²/(2c²)`, and returns the standard 38-microsecond-per-day satellite gain that GPS clocks are factory-detuned to compensate.

This is not new physics. It is the observation that the SAM kernel `A(r) = 2GM/(c²r)` read in SI reproduces the engineered GPS relativistic correction to the precision GPS is engineered around. It stands as the earned empirical basis for §3's SI unit lock.

---

## 6. The ceiling on cosmological-style corrections in the lab

Vol I §4 introduces `c_eff = c(1 − A_los)` as the read of measurable distance along cosmological sightlines where the line integral of A accumulates over gigaparsecs. That reading is load-bearing for the distance/BAO/supernova work Vol I §4 depends on. It is also, at Earth surface, arithmetically negligible.

**The laboratory-scale calculation:**

For a line-of-sight path of length ℓ at Earth surface, `A_los = ⟨A⟩ · ℓ / ℓ_scale` where ⟨A⟩ ≈ 1.4 × 10⁻⁹. Along any laboratory-scale path (ℓ ≤ few m), the line-integrated A is at most 1.7 × 10⁻⁹ m of A-per-meter — a dimensionless correction to `c_eff` at the 10⁻⁹ level.

**Consequence:** `c_eff` at laboratory scale differs from the SI-defined c by parts in 10⁹. Any SAM prediction stated in SI at laboratory scale carries an intrinsic frame uncertainty of ≤ 10⁻⁹ from the cosmological-style correction.

**Downstream language.** Lab CRs may state numerical predictions in SI without carrying a `c_eff` correction term.

---

## 7. What this reference does for downstream CRs

Any laboratory-scale SAM CR that cites `SAM_ON_EARTH_v1.md` inherits:

1. **The SI constants table (§1)** — no need to restate CODATA values.
2. **The A-budget at laboratory scale (§2)** — no need to recompute Earth-surface A.
3. **The SI unit lock (§3)** — one-sentence verbatim citation closing the "SAM units vs SI units" escape hatch.
4. **The Vol I §2 empirical backing (§4)** — reference for why the frame lock is not a bare assertion.
5. **The STAM Model-A worked example (§5)** — numerical implementation available.
6. **The ceiling on c_eff-style corrections (§6)** — explicit ledger entry for the omission of cosmological correction terms in lab predictions.

---

## 9. Provenance

| artifact | reference |
|---|---|
| Vol I | [SAM_VOLUME_I_SUBSTRATE.md](SAM_VOLUME_I_SUBSTRATE.md) |
| Vol I §2 A-kernel weak-field kernel derivation | Vol I §2 |
| Vol I §4 c_eff and cosmological line integrals | Vol I §4 |
| CODATA 2018 fundamental constants | NIST Constants |
| SI Brochure (definitional c since 1983; kg, s, m definitions) | BIPM SI Brochure |
| WGS84 Earth reference (R_Earth, GM_Earth, U₀/c²) | US Department of Defense WGS84 (1984, updated 2004) |
