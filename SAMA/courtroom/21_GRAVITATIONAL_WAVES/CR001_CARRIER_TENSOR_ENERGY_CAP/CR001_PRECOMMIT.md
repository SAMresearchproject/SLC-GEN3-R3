# CR001 — Carrier-Tensor Energy Cap

**Branch:** 21_GRAVITATIONAL_WAVES
**Mode:** EXPLORATORY (first lock on a new hypothesis; light precommit)
**Sealed by:** Sean Brady, 2026-06-28
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Idea under test

The SAM carrier-tensor framing of gravitational waves
([GW_SUBSTRATE_FRAMING.md](../GW_SUBSTRATE_FRAMING.md)) predicts a
substrate-derived hard cap on the fraction of merger mass-energy
that can be radiated as a Θ-wave:

```text
  E_GW / (M_total · c²)   ≤   Θ / R²   =   18 / 144   =   1 / 8   =   12.5%
```

The cap is the tensor share of the closed ledger
(CR229@09a inclusion-exclusion identity). Carriers above this
fraction can't escape — they'd exceed the Home's allowed Θ
allocation and stay bound.

**This is exploratory.** The framing might be wrong. The first
test is the strongest possible falsifier: any single LIGO/Virgo
confirmed event with E_GW/M_total·c² > 1/8 kills the framing.

## Question

For every confirmed binary-merger gravitational wave event with
published M_total (source-frame total mass) and E_rad (radiated
energy in M_⊙c² units), does

```text
  f_rad  =  E_rad / M_total   ≤   1/8 = 0.125
```

hold across the GWTC catalog?

## Data discipline

This is the **exploratory** first lock. The runner uses a curated
representative event set hardcoded as in-code literals, with each
value cited to its LIGO/Virgo publication. **No full-catalog
download in CR001.**

If CR001 PASSes, **CR001b** would extend to the full GWTC-3 confident
event list with the JSON download from `https://gwosc.org/`. If CR001
FAILs on any single event, the framing is killed and no extension is
warranted.

### Cited event set

15 representative confirmed events spanning GWTC-1, GWTC-2.1, and
GWTC-3, chosen to cover:
- the lowest radiated fraction (BNS GW170817)
- the highest mass (GW190521 IMBH-class)
- the asymmetric mass ratio (GW190412)
- the mass-gap event (GW190814)
- the NSBH case (GW200115)
- representative BBH from each observing run

All values cited from the GWTC-1 (Abbott et al. 2019), GWTC-2.1
(Abbott et al. 2021), and GWTC-3 (Abbott et al. 2023) catalog
papers and individual event discovery papers. Numerical values
hardcoded in the runner with comment-cited references.

## Cap formula

```text
  cap_substrate  =  Theta / R²  =  18 / 144  =  1/8
  Theta          =  alpha_H · D²  =  2 · 9 = 18      [CR229]
  R              =  alpha_H² · D  =  4 · 3 = 12       [CR258]
  R²             =  144
```

No fitted parameter. No catalog calibration. Pure substrate atom.

## Verdict tree (exploratory; minimal gate stacking)

```text
PASS:
  every event in the curated set has f_rad <= 1/8
  -> framing survives first test; CR001b extends to full catalog

BOUNDARY:
  one event within 0.5% of cap (0.1244 to 0.1250)
  -> framing survives but tightly; flag for CR001b scrutiny

FAIL:
  any event has f_rad > 1/8
  -> framing killed; document which event and by how much
```

## What this CR seals

Either:
- **PASS** — the substrate cap Θ/R² = 1/8 is consistent with the
  LIGO/Virgo confirmed event radiated-fraction spectrum on the
  representative set. The carrier-tensor framing survives first
  contact with data.
- **FAIL** — at least one confirmed event radiates more than 1/8
  of total mass-energy. The carrier-tensor framing's hard cap
  prediction is falsified. Subsequent CRs in the queue stay
  unsealed pending a re-framing.

## Honest framing notes

- **GR's hard limit** from numerical relativity for binary BH
  mergers is roughly 11–12% (Hemberger et al. 2013 give up to
  ~12.27% for extremally aligned-spin equal-mass). SAM's 1/8 =
  12.5% is right at that boundary. A PASS does not strongly
  discriminate SAM from GR's hard limit — both bound the same
  region. This is acknowledged in the result interpretation,
  not gated.
- **The cap is the headline test, not the only test.** If CR001
  PASSes, CR002 (binary-only emission requirement) and CR003
  (ringdown frequency in substrate units) become the next
  discriminating tests.

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR229@09a inclusion-exclusion identity | per [HASHES.txt](../../09a_PARTICLE_MASS_CHAIN/CR229_CARRIER_TENSOR_INCLUSION_EXCLUSION_IDENTITY/HASHES.txt) |
| CR258@09a primitive closure audit | `942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7` |
| branch README.md | `1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595` |
| branch GW_SUBSTRATE_FRAMING.md | `a19afc01a749e925d6e1e4f70321217dcaca95fd5981a68e0e52ebdfcb2ed941` |
| branch CR_QUEUE.md | `ef6f85bc02a1dd2a9fc62f4d14da865079f0705f25e73eeb815d1d6b6b810c66` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
