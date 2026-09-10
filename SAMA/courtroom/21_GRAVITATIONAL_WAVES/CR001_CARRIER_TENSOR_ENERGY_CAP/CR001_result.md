# CR001 — Carrier-Tensor Energy Cap — RESULT

```text
verdict           : PASS
mode              : EXPLORATORY (first-contact lock)
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : 1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805
runner_hash       : 4a6a27f6544eacf943a0cfa94ea41c23627622d95ae482b336c334264588d6ee
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

The SAM substrate cap `E_GW / (M_total · c²) ≤ Θ/R² = 1/8 = 12.5%`
is **consistent with every event in the curated GWTC representative
set**. No event radiates more than the cap. The carrier-tensor
framing survives first contact with LIGO/Virgo data.

```text
substrate cap                = 0.12500   (= Θ/R² = 18/144 = 1/8)
max observed f_rad           = 0.05978   (GW170729, GWTC-1 BBH)
headroom to cap              = 0.06522   (52% of the cap unused)
events tested                = 16
within cap                   = 16  (PASS)
exceeded cap                 = 0
near boundary (within 0.5%)  = 0
```

## Per-event readout

All values source-frame; E_rad in M_⊙·c² units.

| event | class | M_total (M_⊙) | E_rad (M_⊙) | f_rad | within cap? |
| --- | --- | ---: | ---: | ---: | :---: |
| GW150914 | BBH | 65.30 | 3.100 | 0.04747 | ✓ |
| GW151012 | BBH | 37.20 | 1.600 | 0.04301 | ✓ |
| GW151226 | BBH | 21.50 | 1.000 | 0.04651 | ✓ |
| GW170104 | BBH | 49.10 | 2.200 | 0.04481 | ✓ |
| GW170608 | BBH | 18.60 | 0.850 | 0.04570 | ✓ |
| **GW170729** | **BBH** | **80.30** | **4.800** | **0.05978** | **✓ (max)** |
| GW170809 | BBH | 56.40 | 2.700 | 0.04787 | ✓ |
| GW170814 | BBH | 53.20 | 2.700 | 0.05075 | ✓ |
| GW170817 | BNS | 2.74 | 0.025 | 0.00912 | ✓ |
| GW170818 | BBH | 62.50 | 2.700 | 0.04320 | ✓ |
| GW170823 | BBH | 68.90 | 3.300 | 0.04790 | ✓ |
| GW190412 | BBH-asym | 37.30 | 1.700 | 0.04558 | ✓ |
| GW190425 | BNS | 3.40 | 0.010 | 0.00294 | ✓ |
| GW190521 | BBH-IMBH | 150.00 | 7.600 | 0.05067 | ✓ |
| GW190814 | NSBH? | 25.80 | 0.800 | 0.03101 | ✓ |
| GW200115 | NSBH | 6.60 | 0.025 | 0.00379 | ✓ |

## Substrate cap derivation (sealed atoms)

```text
alpha_H = 2                        (CR258 primitive)
D       = 3                        (CR258 primitive)
R       = alpha_H^2 · D = 12       (route radix)
R^2     = 144                      (writable capacity)
Theta   = alpha_H · D^2 = 18       (carrier tensor / graviton overlap)
cap     = Theta / R^2  = 18/144 = 1/8 = 0.125
```

Zero fitted parameters. No catalog calibration.

## What we learned

1. **The framing is alive.** All 16 representative events sit
   below the cap. No falsifying outlier.
2. **The cap is loose at current sensitivity.** Max observed
   `f_rad = 0.0598` uses less than half the substrate budget
   (52% headroom). CR001 alone cannot strongly distinguish SAM
   from a hypothetical "any cap ≥ 6%" framing.
3. **The cap landed near GR's hard limit.** Numerical-relativity
   binary-BH simulations cap radiated fraction at roughly 11–12%
   for extremally aligned-spin equal-mass mergers (Hemberger et
   al. 2013). SAM's 12.5% is right at that boundary — slightly
   looser. A PASS on observed events is consistent with both
   theories; discriminating tests live in CR002+ of the queue.

The exploratory framing was: "there is an idea, it might be wrong."
First-contact result: the idea is **not yet wrong**. That earns it
the next CR (CR002 binary-only emission requirement) and an
extension to the full GWTC-3 catalog under CR001b.

## What this CR does NOT seal

Per branch discipline, this exploratory CR is one piece of evidence,
not a closed proof:

- CR001 tested a representative 16-event subset, not the full
  GWTC-3 confident catalog (~90+ events as of 2026-06). CR001b
  follow-up extends to the full catalog from `gwosc.org`.
- Posterior-distribution coverage: the precommit uses median
  source-frame values from catalog papers. Per-event posteriors
  may have tails above the cap at low credibility.
- The substrate cap derivation assumes the inclusion-exclusion
  identity CR229@09a applies uniformly to merger products. That's
  the framing under test in the broader branch — not separately
  audited here.

## What this CR opens

- **CR001b** — full GWTC-3 confident-event catalog extension.
  Pure catalog widening; no framing change.
- **CR002** — binary-only emission requirement. Pure catalog
  classification check; first test that discriminates SAM from
  GR-equivalent at the *emission-mechanism* level (GR doesn't
  prohibit non-binary GW emission; SAM's framing does).
- **CR003** — ringdown frequency in substrate units. First test
  that discriminates at the *substrate-derivation* level.

## Source citations

All event values from LIGO/Virgo published catalog and discovery
papers, cited in CR001_runner.py per-row comments:

- Abbott et al. 2016 PRL 116 061102 (GW150914)
- Abbott et al. 2017 PRL 119 161101 (GW170817 BNS)
- Abbott et al. 2019 Phys. Rev. X 9 031040 (GWTC-1)
- Abbott et al. 2020 PRL 125 101102 (GW190521)
- Abbott et al. 2020 ApJL 896 L44 (GW190814)
- Abbott et al. 2020 PRD 102 043015 (GW190412)
- Abbott et al. 2020 ApJL 892 L3 (GW190425)
- Abbott et al. 2021 ApJL 915 L5 (GW200115)
- Abbott et al. 2021 Phys. Rev. X 11 021053 (GWTC-2)
- Abbott et al. 2023 Phys. Rev. X 13 041039 (GWTC-3)
- Abbott et al. 2024 Phys. Rev. D 109 022001 (GWTC-2.1)

Numerical relativity hard-limit reference:
- Hemberger et al. 2013 Phys. Rev. D 88 064014 (max radiated fraction
  for binary BH ~12.27% at extremal aligned spin)

## Provenance hash chain

```text
precommit          : 1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805
runner             : 4a6a27f6544eacf943a0cfa94ea41c23627622d95ae482b336c334264588d6ee
upstream (CR229@09a inclusion-exclusion identity)
upstream (CR258@09a primitive closure audit) : 942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7
branch README                                : 1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595
branch GW_SUBSTRATE_FRAMING                  : a19afc01a749e925d6e1e4f70321217dcaca95fd5981a68e0e52ebdfcb2ed941
branch CR_QUEUE                              : ef6f85bc02a1dd2a9fc62f4d14da865079f0705f25e73eeb815d1d6b6b810c66
stewardship                                  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR001 PASS (EXPLORATORY).** SAM's substrate cap on
gravitational-wave radiated mass-energy (Θ/R² = 1/8) is consistent
with the curated representative LIGO/Virgo confirmed-event set; all
16 events sit at or below 6% radiated fraction, well within the 12.5%
cap. The framing survives first contact; the next discriminating
tests (CR002 binary-only emission, CR003 ringdown frequency in
substrate units) are now unblocked.

`CARRIER_TENSOR_CAP_THETA_OVER_R_SQ_EQUALS_ONE_EIGHTH_HOLDS_16_OF_16_LIGO_VIRGO_CONFIRMED_EVENTS_MAX_OBSERVED_0.0598_GW170729_PASS_EXPLORATORY`
