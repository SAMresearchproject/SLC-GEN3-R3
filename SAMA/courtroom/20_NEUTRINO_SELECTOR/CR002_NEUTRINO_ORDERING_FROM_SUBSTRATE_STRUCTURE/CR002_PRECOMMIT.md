# CR002@20_NEUTRINO_ORDERING_FROM_SUBSTRATE_STRUCTURE Precommit

**Sealed by:** Sean Brady, 2026-06-26.
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
**Volume I seal:** `ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b`
**Upstream:** CR001@20 (substrate ratios sealed)

## Verdict Ladder

```text
PASS:
  The substrate-derived ordering matches the global-fit preferred
  ordering.

FAIL:
  Substrate-derived ordering disagrees with the global-fit preference
  at the present significance.
```

## Test Type

```text
Structural-identity CR. Reads CR001@20's sealed substrate ratios and
extracts the mass-ordering prediction.
```

## Question

```text
Does the substrate reading {1, sqrt(alpha_H), alpha_H * D} for the
three neutrino mass eigenstates produce normal ordering, in agreement
with the joint oscillation+cosmology global-fit preference for normal
ordering at ~2-2.5 sigma (PDG 2024)?
```

## Substrate Inputs (sealed; zero fit)

```text
From CR001@20:
  r_1 = 1
  r_2 = sqrt(alpha_H) = sqrt(2) = 1.4142135624
  r_3 = alpha_H * D = 6

base_eV > 0 (sealed from CR001@20 = 0.0084768593 eV)
```

## P1 — Normal Ordering by Substrate Construction (load-bearing)

```text
Normal ordering is defined as m_3 > m_2 > m_1 (the third mass
eigenstate is the heaviest).

From the sealed substrate ratios with base_eV > 0:

  m_3 = base_eV * 6
  m_2 = base_eV * sqrt(2) ~= base_eV * 1.414
  m_1 = base_eV * 1

Since 6 > sqrt(2) > 1, we have m_3 > m_2 > m_1.

Pass: ordering is normal (m_3 > m_2 > m_1).
Falsifier: any ordering other than normal (impossible given the sealed
substrate ratios and base_eV > 0).

This is structurally forced. CR002@20 documents the forcing.
```

## Reported Evidence

```text
E1: Global-fit preference
    PDG 2024: normal ordering preferred at ~2-2.5 sigma over inverted
    by joint oscillation + cosmology data.
    SAM: normal ordering by substrate construction (zero significance
    over inverted because inverted is structurally excluded).

E2: Cosmological preference
    Planck 2018 + DESI 2024 Sigma m_nu upper bounds are tighter for
    inverted ordering (which would require larger Sigma m_nu by ~30%
    relative to normal). Inverted ordering would push Sigma m_nu
    closer to or above the cosmological bound.
    SAM's normal ordering with Sigma m_nu = 71.33 meV (CR001@20)
    is consistent with cosmology.

E3: Pathway to falsification
    The substrate prediction would be falsified only if:
    (a) future precision oscillation measurements decisively favor
        inverted ordering at >5 sigma, OR
    (b) cosmological measurements decisively constrain Sigma m_nu
        below the SAM prediction (~0.07 eV), which would force
        revision of the substrate reading.
    Neither is currently the case.
```

## Rule-9 Line

```text
This test could falsify the claim that SAM's substrate reading
{1, sqrt(alpha_H), alpha_H * D} forces normal ordering of the
neutrino mass eigenstates.

It did not falsify it. The substrate ratios are sealed in CR001@20;
the ordering 1 < sqrt(2) < 6 forces normal ordering m_3 > m_2 > m_1
trivially under positive base_eV.
```

## Manuscript Headline (conditional on PASS)

```text
SAM forces normal ordering of the neutrino mass eigenstates by
substrate construction. The sealed substrate ratios r_1 = 1,
r_2 = sqrt(alpha_H) = sqrt(2), r_3 = alpha_H * D = 6 satisfy
r_3 > r_2 > r_1, so under positive eV anchor the masses obey
m_3 > m_2 > m_1 — the normal ordering.

The global-fit preference (PDG 2024) for normal ordering at ~2-2.5
sigma over inverted is in agreement with SAM. The substrate prediction
is structurally definite, not statistical.
```
