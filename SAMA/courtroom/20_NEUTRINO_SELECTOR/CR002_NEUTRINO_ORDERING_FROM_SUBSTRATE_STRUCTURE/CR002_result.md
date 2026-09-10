# CR002@20_NEUTRINO_ORDERING_FROM_SUBSTRATE_STRUCTURE

## Verdict

```text
CR002@20_PASS_NORMAL_ORDERING_FORCED_BY_SUBSTRATE_RATIOS_1_SQRT2_6
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SUBSTRATE_STRUCTURAL_FORCING_OF_NORMAL_ORDERING
free_parameters_introduced = 0
precommit_sha256 = 076979401c06c7af8d979549ccc26f7838d6a91c5eb5047858639a57d035d72a
```

## Headline

```text
SAM forces normal ordering of the neutrino mass eigenstates by
substrate construction.

The sealed substrate ratios (CR001@20):

  r_1 = 1
  r_2 = sqrt(alpha_H) = sqrt(2)
  r_3 = alpha_H * D = 6

satisfy r_3 > r_2 > r_1. Under positive eV anchor (base_eV > 0,
sealed in CR001@20 as 0.0084768593 eV), the masses obey

  m_3 > m_2 > m_1

which is the definition of normal ordering. Inverted ordering is
structurally excluded.

PDG 2024 global-fit preference for normal ordering at ~2-2.5 sigma
is in agreement with SAM's structurally-forced normal ordering.
```

## Substrate Inputs (sealed from CR001@20)

```text
r_1 = 1.0000000000
r_2 = 1.4142135624
r_3 = 6.0000000000
base_eV = 0.0084768593 eV
```

## P1 — Normal Ordering by Substrate Construction — PASS

| field | value |
|---|---:|
| m_3 (heaviest) | 50.861 meV |
| m_2 (middle) | 11.988 meV |
| m_1 (lightest) | 8.477 meV |
| m_3 > m_2 ? | true |
| m_2 > m_1 ? | true |
| ordering | normal |
| **pass** | **true** |

## Reported Evidence

### E1 — Global-Fit Preference

```text
PDG 2024: normal ordering preferred at ~2-2.5 sigma over inverted by
joint oscillation + cosmology data.
SAM: normal ordering by substrate construction (structurally forced;
no significance over inverted because inverted is structurally
excluded under the sealed substrate reading).
```

### E2 — Cosmological Preference

```text
Inverted ordering would require Sigma m_nu ~ 0.10 eV (m_1 ~ m_2 ~
sqrt(Delta m^2_31) ~ 50 meV each, m_3 small), pushing close to or
above the Planck cosmological bound 0.12 eV.

SAM's normal ordering with Sigma m_nu = 0.0713 eV (CR001@20) is
comfortably consistent with cosmology.
```

### E3 — Falsifiability

```text
The substrate prediction would be falsified by:
  (a) future precision oscillation measurements decisively favoring
      inverted ordering at >5 sigma, OR
  (b) cosmological measurements decisively constraining Sigma m_nu
      below the SAM prediction ~0.07 eV.
Neither is currently the case.
```

## Pass Conditions

| condition | pass |
|---|---:|
| ordering_normal_by_substrate_construction | true |

## Rule-9 Line

```text
This test could falsify the claim that SAM's substrate reading
{1, sqrt(alpha_H), alpha_H * D} forces normal ordering of the
neutrino mass eigenstates.

It did not falsify it. The substrate ratios are sealed in CR001@20;
the ordering 1 < sqrt(2) < 6 trivially forces normal ordering
m_3 > m_2 > m_1 under positive base_eV.
```

## Provenance Chain

```text
Stewardship                = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Volume I (manuscript)      = ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b
CR001@20 precommit         = 8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77
CR002@20 precommit         = 076979401c06c7af8d979549ccc26f7838d6a91c5eb5047858639a57d035d72a
```

---

**Sealed by:** Sean Brady, 2026-06-26.
