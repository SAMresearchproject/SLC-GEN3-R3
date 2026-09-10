# CR003@20_PMNS_MIXING_BOUNDARY_CHAPTER

**Type:** BOUNDARY CHAPTER (no derivation gates; PDG values quoted as
the remaining open work to derive from substrate).

**Sealed by:** Sean Brady, 2026-06-26.
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
**Volume I seal:** `ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b`

## Status

```text
SAM derivation of the PMNS mixing matrix is OPEN as of 2026-06-26.

CR001@20 sealed the three neutrino mass eigenstates from substrate ratios.
CR002@20 sealed the normal ordering from substrate construction.
CR003@20 marks the mixing structure as a remaining boundary in Vol II.

The PMNS mixing angles theta_12, theta_23, theta_13 and the CP-violating
phase delta_CP are not yet derived from substrate identities. The
substrate has the apparatus (carrier-tensor lanes, R-aligned bigrade
alphabet, second-layer inverse decomposition Phi(Z,N)) that could
plausibly carry the mixing structure, but the specific reading is
open work.
```

## PDG 2024 Reference Values (quoted as remaining work)

```text
sin^2(theta_12) = 0.307 +/- 0.013        theta_12 = 33.65 deg
sin^2(theta_23) = 0.451 +/- 0.020 (NO)   theta_23 = 42.18 deg
sin^2(theta_13) = 0.0220 +/- 0.0007      theta_13 =  8.53 deg
delta_CP        = 197 +/- 24 deg (NO)
```

The mixing angles are constrained by oscillation experiments
(Super-Kamiokande, T2K, NOvA, KamLAND, Daya Bay, RENO, IceCube,
KM3NeT). The CP-violating phase delta_CP is the least precisely
measured; current 1-sigma uncertainty is ~30 degrees.

## Substrate-Side Candidates for Future Derivation

```text
The PMNS matrix has three mixing angles and one CP phase (for Dirac
neutrinos; two additional Majorana phases for Majorana neutrinos).
The substrate apparatus that could carry the mixing structure includes:

1. The carrier-tensor lanes [1, 1, 2, 3, 4, 6, 8, 8, 9, 9, 12, 18, 81].
   The 13 distinct lane widths might map onto the mixing-angle structure
   via a typed reading.

2. The bigrade alphabet {1, 2, 3, 4, 6, 8, 9, 12} from CR217. The
   {1, 8, 9} overlap with named carriers (Theta = 18 = 1+8+9) might
   carry mixing structure.

3. The connection-fee formula (R + q + D) / R applied to the three
   mass eigenstates with appropriate q-readings might produce mixing
   angles.

4. The second-layer inverse decomposition Phi(Z, N) = Z*phi_balanced +
   (N-Z)*phi_excess from CR247 produced exact 6/6 identities on 69
   N >= Z rows. A similar decomposition applied to neutrino flavor
   states might produce the mixing structure.

5. The asymmetry-term identity (Q_mass - Q_sub)^2 / Q_mass from CR245
   has theorem-grade derivation depth; an analog might apply to
   neutrino-sector asymmetry.

None of these candidates is sealed for the mixing structure as of
2026-06-26. CR003@20 documents the boundary; subsequent CRs in this
branch or a successor branch will attempt the derivation.
```

## What CR001@20 + CR002@20 + CR003@20 Establish Together

```text
Volume II ships with:
  - Substrate-derived neutrino mass spectrum (CR001@20 PASS)
  - Substrate-derived normal ordering (CR002@20 PASS)
  - PMNS mixing as documented boundary chapter (CR003@20)

That is more than the Standard Model offers: SM derives zero of the
three neutrino mass values, the ordering, the Sigma m_nu, the
splittings, or the mixing structure. SAM derives the three masses,
the ordering, the Sigma m_nu, the splittings ratio to 3.26%, and
documents the mixing as open work for a future CR.

The honest position for Volume II is: SAM landed the mass spectrum
and ordering; SAM is still working on mixing.
```

## Used in E5 of CR001@20

```text
The PDG mixing values were used in CR001@20 E5 (effective beta-decay
mass m_beta computation) as external inputs, not as load-bearing
gates. m_beta = 12.20 meV, factor 36.9 below the KATRIN bound. That
computation does not change CR001@20's PASS verdict; it is reported
evidence only.
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
