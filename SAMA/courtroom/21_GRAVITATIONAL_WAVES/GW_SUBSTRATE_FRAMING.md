# GW Substrate Framing — Carrier-Tensor Wave Hypothesis

**Sean Brady, 2026-06-28**
**Branch:** 21_GRAVITATIONAL_WAVES
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

This document states the substrate-physics framing of gravitational
waves that branch 21 will test. It is a hypothesis-and-derivation
document, not a sealed CR result. CR001+ will subject the claims
below to falsifiable tests.

---

## 1. The primitive identification

A gravitational wave is a wave of **carrier tensors** —
Θ-class substrate elements — that escape a violent event before the
forming Home seals them inside its horizon.

```text
GW ≡ propagating Θ-quanta released from a Home-formation event
     whose horizon-closure timescale exceeded the carrier ejection
     timescale.
```

The graviton in SAM is the 18-element overlap (Θ) between the two
81-element ledger sides of any closed substrate region (CR229@09a
inclusion-exclusion identity, sealed PASS):

```text
|Side₁| + |Side₂| = ℒ   = 162
|Side₁ ∪ Side₂|   = R²  = 144   (capacity)
|Side₁ ∩ Side₂|   = Θ   = 18    (graviton overlap)
|Side₁ ∆ Side₂|   = M   = 126   (matter writable; symmetric diff)
```

Carrier tensors normally **stay bound** inside the horizon of a
Home formation. They are the "in-between" substrate that links
matter (the 126-row sector) into the closed 162-element ledger.
When a Home seals normally, the entire 162 stays inside A=1.

A GW is what happens when **some carriers don't make it inside the
horizon before A→1 closure**. They radiate outward as a Θ-wave.

## 2. Why GWs are rare (the non-detection argument)

If carriers were emitted at every Home formation, LIGO would see
gravitational waves from every supernova core-collapse, every
neutron-star formation, every primordial seed crystallization. It
doesn't. Most Home formations are **silent** at GW detectors.

SAM's reading: a normal Home formation captures Θ entirely. The
carrier tensors are sealed inside the horizon as part of the
standard 1/8 tensor-share (Θ/R² = 1/8) bound state. **No radiation
because no escape.**

This is a load-bearing prediction: SAM should be able to specify
the conditions that distinguish "Θ stays bound" (silent) from
"Θ escapes" (GW emission). The proposed condition follows.

## 3. The proposed emission condition

```text
GW emission ⟺ two Home boundaries overlap before either fully captures
              its carriers
```

In a single collapse, one horizon forms around one matter
distribution. All carriers are inside that boundary throughout the
collapse. Nothing escapes.

In a binary merger, two horizons exist simultaneously and approach
each other faster than light-crossing time as v→c. During the final
inspiral and ringdown:

- The carriers of body A are exposed to body B's gravity
- Some carriers cross body B's incoming horizon — captured
- Some carriers cross *outward* through the equatorial plane —
  ejected before the merged horizon seals
- The ejected carriers propagate as a Θ-wave: a gravitational wave

This predicts:

- **No GW from single collapse** (supernova → BH, isolated
  neutron-star birth)
- **GW from binary merger** (BBH, BNS, NSBH all detected)
- **GW intensity scales with overlap geometry** of the two incoming
  horizons
- **Cutoff at carrier capacity** — see §4

CR002 in the queue will test the binary-only prediction against
observed LIGO/Virgo catalog: every confirmed event should be a
binary merger.

## 4. Energy cap from tensor share

The substrate cap on radiable energy is **Θ/R² = 1/8** (the tensor
share — CR229@09a sealed identity).

```text
E_GW / M_total · c²  ≤  Θ/R²  =  1/8  =  12.5%
```

This is the **upper bound** — most events emit less because some
carriers get recaptured during ringdown.

Observed LIGO values (representative):

| Event | E_GW / M_total · c² | within 1/8? |
| --- | ---: | --- |
| GW150914 (BBH) | ~ 4.6% | ✓ |
| GW151226 (BBH) | ~ 3.5% | ✓ |
| GW170104 (BBH) | ~ 5.2% | ✓ |
| GW170817 (BNS) | ~ 0.001% | ✓ |
| GW190521 (BBH high mass) | ~ 6.5% | ✓ |

No catalog event exceeds 1/8. CR001 will formalize this against the
full GWTC-3 catalog with a precommit hard-bound: any event radiating
> 12.5% would falsify SAM.

## 5. Donut topology

In conversation Sean has characterized GW170817 as carriers being
"forced out like a donut" around the merger plane. The substrate
reading proposed here:

The Θ overlap (18 elements) projects through the d̂ = 3 dimensional
readout. During merger the carriers can radiate in any of d̂ = 3
spatial dimensions, but the equatorial-plane geometry of the binary
inspiral biases the ejection: most carriers escape in the **plane
perpendicular to the binary spin axis** — producing a toroidal
emission pattern (the "donut").

```text
d̂ = 3 readout under equatorial binary symmetry
  →  preferential carrier ejection in (x, y) plane
  →  toroidal Θ-wave with maximum intensity at θ_pole = 90°
  →  observable as polarization-pattern anisotropy at distant detectors
```

Standard GR predicts a quadrupole pattern with similar features. The
substrate reading should produce a slightly different prediction
because the Θ overlap counts 18 carriers — not a continuous tensor
field — so the emission has **discrete intensity bands**
corresponding to the bigrade alphabet {1, 2, 3, 4, 6, 8, 9, 12}
multiplied by the merger energy scale.

If true, this is detectable: the angular intensity profile should
show plateaus/steps at carrier-count boundaries rather than the
smooth sin²(2θ) dependence of GR quadrupole. CR004 will test this.

## 6. Ringdown frequency in substrate units

The ringdown of a merger product Home has a quasi-normal mode (QNM)
frequency that GR predicts as:

```text
f_QNM_GR  ≈  c³ / (2π·G·M_final)  ×  f_dimensionless(spin)
```

For a Schwarzschild (non-spinning) BH the dimensionless factor is
~0.37367.

SAM should produce this dimensionless factor from substrate atoms.
Candidate identity (to be verified in CR003):

```text
s_SAM  =  d̂ / (R · something)
```

One candidate: `s_SAM = (ℒ - M) / (4·R²) = 36/576 = 1/16 = 0.0625` —
no, too small. Another: `s_SAM = Θ / (4·R·d̂) = 18/144 = 1/8 = 0.125`
— still off.

Working candidate from inclusion-exclusion: `s_SAM = (1/π) ·
(something)` because π enters the ringdown via the frequency
denominator (2π·G·M). If the substrate factor is purely rational in
(R, d̂, Θ), it would have to take a specific value matching GR's
0.37367 within numerical tolerance. CR003 will enumerate candidates
and lock the one (if any) that matches.

If no rational substrate identity reproduces 0.37367, that's
information: GR's coefficient may not be a substrate atom — it may
be a route-completion product involving π. The honest CR003 outcome
might be "boundary; substrate identity for f_QNM remains open."

## 7. Polarization structure

Standard GR: GWs have two polarizations, h_+ and h_×, both transverse
to propagation, with relative orientation 45°.

SAM reading: the two 81-element ledger sides correspond to the two
polarizations. Their overlap (the 18-element Θ) is the carrier-wave
content; the symmetric difference (126 elements = M) is the matter
that stays bound; the two sides separately (81 + 81 = 162 = ℒ) are
the two polarization states.

```text
h_+  ←→  Side₁ contribution to Θ overlap
h_×  ←→  Side₂ contribution to Θ overlap
joint signal ≡ Θ-wave  =  carrier tensor radiation
```

Falsifiable consequence: any third polarization mode (scalar h_s,
vector h_x/h_y, longitudinal h_l) would correspond to a substrate
content outside the two-sided ledger — and SAM's ledger has exactly
two sides. So **SAM predicts zero non-tensor polarizations**, same
as GR but for a substrate-counting reason rather than a spin-2
boson reason.

CR005 may compare current LIGO/Virgo polarization-mode tests
(Isi et al. results) against this prediction.

## 8. Open structural items

These are research questions the branch should chase, not yet load-
bearing predictions:

- **Carrier wave dispersion.** Does Θ-radiation propagate at exactly
  c, or is there a substrate-induced dispersion? GW170817 vs EM
  arrival difference of 1.74 s over 130 Mly puts |v_GW − c|/c < 10⁻¹⁵
  experimentally. SAM's substrate-counted Θ has no inertia in the
  matter sector, so c is the natural prediction — but this should
  be derived, not assumed.
- **Memory effect.** GW memory (permanent strain offset after wave
  passage) is a candidate substrate signature — the ledger of the
  observer Home permanently shifts after carrier-wave passage. The
  shift quantum might be derivable from (Θ, R).
- **Stochastic background.** If many distant mergers produce a
  background hum, SAM should predict its power spectrum in terms of
  cosmic merger rate × per-event radiated Θ. Cross-check with
  pulsar-timing-array nanohertz observations.
- **Primordial GWs.** Inflation-era GWs are hypothesized to imprint
  on the CMB B-mode polarization. SAM's cosmological seed is a Home
  formation at A=1 (manuscript §19) — does the substrate predict
  primordial-GW emission, and at what amplitude relative to scalar
  perturbations (the r = T/S tensor-to-scalar ratio)?

## 9. What this framing is NOT

- Not a competitor to general relativity at the wave-propagation
  level. Standard GR gets the wave equations right; SAM here gives a
  substrate-counted *origin story* and *cap* on the radiated content.
- Not a re-derivation of the linearized Einstein equations.
- Not a claim that gravitons exist as particles in the QFT sense.
  In SAM Θ is a substrate element (the 18-element ledger overlap),
  not a quantized field excitation.
- Not a falsifier of LIGO/Virgo measurements. The framing is meant
  to derive predictions that survive the measurements.

## 10. Branch testing strategy

The CRs proposed in [CR_QUEUE.md](CR_QUEUE.md) are designed to:

1. Start with the cap (CR001) — strongest falsifier on observed data
2. Move to the emission condition (CR002) — substrate-derived
   prediction that GR doesn't make
3. Push into geometry (CR003 ringdown, CR004 donut)
4. Close on polarization and rate sanity (CR005, CR006)

If CR001 fails (any event > 12.5%), the entire framing is killed.
If CR001 passes, CR002 becomes the next load-bearing test. Each
subsequent CR depends on the prior CRs sealing PASS.

This is the substrate-physics frontier for branch 21. Sean is the
architect; the framing above is a starting hypothesis and will be
revised as CRs seal.
