# CR281 Precommit: Cosmic-Budget Typed-Readout Promotion

record_id: CR281
record_name: COSMIC_BUDGET_TYPED_READOUT_PROMOTION
campaign: SAM_COURTROOM_THREE_RECORD_PROMOTION_CAMPAIGN_5_5_XHIGH
destination: 07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION
precommit_written_before_runner: true

## Objective

Promote the complete typed cosmic-budget readout from A0 through Omega_b and
Omega_m, and where sealed through eta, omega_b, h^2, and H0.

This record uses Volume I as conceptual map and traces the equations to sealed
Courtroom authority. It does not begin a CMB-spectrum campaign and does not use
Planck or any observational comparator to choose or normalize the SAM result.

## Permitted Source Set

| source | role | sha256 |
| --- | --- | --- |
| SAM_VOLUME_I_SUBSTRATE.md | conceptual cosmic-budget map | 88d8ef28863be32326264456ed3af24830cfbc633a25a157556c4b872b0122d3 |
| SAM_VOLUME_I_GLOSSARY.md | typed glossary | 68714376542f773fe917b86d926128ac65a7ccd3f7ff9512f89f5ecfe1c2831f |
| VOLUME_I_APPENDIX_AND_GLOSSARY.md | formula quick reference | a1ce9da214e5ce0d60ede81d818a12c8d94be1a81a33dc5fd4b5b7da6ef69884 |
| CR003@19 summary | A0 horizon projection | 860ff846ac0dc786176cbb1becb821bb10bfdf971682b6b638b5e095ad8ba9b5 |
| CR003@19 result | A0 identity prose | eb81ee8d9f8d395ad982133fe622fa0204109d10b2af688e41d44b748e07ad35 |
| CR018@07 summary | A0, chi, Omega_b | a1d598841ecb06f8ea59f744c8f29e85ccdee32a6454fb5ee590c98ff545cc19 |
| CR018@07 result | baryon inventory result | 9f84c09f44488ee86f1d55dcb54e9f25a05f97f3bcfcc458cd60948eae517b56 |
| CR019@07 summary | directional refinement | c2dad0a4a45c9739962ccc106bec43343ee02bd82c58b1ed1818d105bef77ad3 |
| CR019@07 result | refinement result prose | c000c57841687a0f39d8303a164658def99da72acd6af1b5bf675599fc96b2f4 |
| CR114 summary | cosmic baryon bridge | f503032f082938ddadc75f69783104af80d08cf078fa64e42d29dc177886f978 |
| CR114 cosmic bridge | retroactive bridge lock | e2f394b40768bc45d916427e7031066cb23e24298e0e4337c3c5bcd4715549c6 |
| CR117 summary | CMB scope boundary | b625af5a9ad7f56fbcf975aad5caddd23efcfc7f2e93ca39f7b37fb8a2e3faae |
| CR117 result | law/configuration boundary | 19e18898de5f0f1305a8417b8fcea8afa6c50f93b12a1e4a5288ba3570cfccf8 |
| CR036@19 summary | eta, K, h^2, H0 cascade | 97f3b07bba6e842a8474b62d5ab3b99fdcc8a3261536086d402c51b73ddae3af |
| CR036@19 result | physical-density provenance | fe1c9ee9c6a4ccf3c6f3d7d6e68ca34f93620c2650811f6b519ce636e1c247a6 |
| CR036@19 evidence rows | dimensional constants/K rows | 03dd23411e8ccd07aadb612a2810931bf5130490de5b6669c9e58cf0f8c4aed6 |

## Structural Inventory Contract

Freeze and verify:

```text
A0 = 1/(pi*R)
chi = (S/D) * A0
Omega_b = alpha_H * A0 * (1 - chi)
Omega_m = R * A0 = 1/pi
Omega_c = Omega_m - Omega_b
Omega_Lambda = 1 - Omega_m
```

Use:

```text
R = 12
D = 3
S = 8
alpha_H = 2
Theta = 18
M = 126
```

The directional refinement is separate:

```text
Omega_m_eff = R*A0 - 2*A0*(chi + D*chi^2)
```

Do not replace the clean Omega_m = 1/pi spine with Omega_m_eff.

## Physical-Density Contract

Where sealed source authority supports it, verify:

```text
eta = (M/(alpha_H^2*Theta)) * A0^6
omega_b = Omega_b*h^2 = eta / K(T_CMB)
h^2 = omega_b / Omega_b
H0 = 100*h km/s/Mpc
```

K source:

```text
CR036@19 computes K_eta_to_omega_b from FIRAS T_CMB=2.7255 K,
CODATA/SI constants, blackbody photon density, H_100, rho_crit(h=1),
and proton mass. K is not fitted to Planck.
```

The runner must identify SAM outputs and external comparators separately.

## Required Typed Outputs

```text
SubstrateFloor[A0]
HorizonQuotient[chi]
BaryonInventoryFraction[Omega_b]
MatterInventoryFraction[Omega_m]
DarkInventoryFraction[Omega_c]
SubstrateVacuumFraction[Omega_Lambda]
EffectiveMatterFraction[Omega_m_eff]
BaryonPhotonRatio[eta]
PhysicalBaryonDensity[omega_b = Omega_b*h^2]
ReducedHubbleParameterSquared[h^2]
HubbleReadout[H0]
```

## Wrong Controls

The runner must preserve these controls:

1. Set A0 = 0.
2. Remove the (1 - chi) factor from Omega_b.
3. Replace R or D with a noncanonical control.
4. Use Omega_m_eff in place of the clean Omega_m spine.
5. Use the Planck omega_b comparator as an input.
6. Replace sourced K(T_CMB) with an unsourced normalization.
7. Confuse Omega_b with omega_b = Omega_b*h^2.

## Verdict Tree

Return one primary verdict:

```text
PASS_COSMIC_BUDGET_TYPED_READOUT
BOUNDARY_PHYSICAL_DENSITY_SOURCE_INCOMPLETE
FAIL_COSMIC_BUDGET_IDENTITY
INVALID_COSMIC_BUDGET_PROVENANCE
```

Optional sub-verdicts:

```text
STRUCTURAL_INVENTORY_PASS
PHYSICAL_DENSITY_PASS
HUBBLE_CASCADE_PASS
DIRECTIONAL_REFINEMENT_PASS
```

PASS requires:

- every required source exists and hashes to the precommitted value;
- structural inventory identities match CR003/CR018/Volume I;
- Omega_m stays the clean 1/pi spine;
- Omega_m_eff is emitted only as a directional refinement;
- eta, omega_b, h^2, and H0 match CR036 within numerical tolerance;
- Planck and other observational values appear only as comparators;
- all wrong controls reject their forbidden moves.
