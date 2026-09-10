# Courtroom Cross-Branch Phase 2 Export Claim

**Sealed at UTC**: `2026-06-14T03:11:03Z`  
**Certificate sha256**: `5023841154959148aab6574358be3bd24eeab58f585736b2c28cc387e1cb2f35`  
**Composite Phase 2 sha256**: `282bed22adc035e1d524e71db98e29c40b8394eaa7392cd0fbf7e834aeaf60eb`  
**Scope status**: PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF

## What This Certificate Binds

Three Courtroom branches each carry an immutable Phase 1 verdict and a sealed Phase 2 verdict.  CR113 binds the three Phase 2 verdicts into one composite sha256 so a single export hash proves the joint Phase 2 state.

| Branch | Phase 1 verdict (unmodified) | Phase 2 verdict (certified) |
|---|---|---|
| 09a_PARTICLE_MASS_CHAIN | CR064a `a2af5df2dd3a...` | CR069a `6a4d7d7dfdbf...` |
| 14_FOUNDATIONAL_TESTS | CR106 `09eb6ae0055e...` | CR112 `632917ff7fcf...` |
| 13_CERN_INDEPENDENT_TESTS | CR098 reg `6884850496ee...` | CR098a commit `f5ea66c9ffb0...` |

## Joint Phase 2 Verdict Reading

- **09a**: Higgs ZZ4l observables within 2 sigma at ATLAS/CMS combined; Z LEP 12-sigma residual closed structurally at q_subslot = -1/6 (12.4 sigma -> 0.43 sigma); 9/8 reciprocal control verified across full u/d/s/c/b/t lineage. Zero free parameters across Phase 1 + Phase 2.
- **14**: SPARC, Planck 2018, and PBH constraint envelopes sealed as public reference anchors; three-mode Earth/Galaxy/PBH structural compatibility closed by a single per-body A-field rule; cosmic baryon Omega_b target frozen at Planck 0.02237 +/- 0.00015 for future appeal. Zero free parameters across cosmology layer.
- **13**: Forward-blind registry now spans particle scale (CR098, 24 predictions) and cosmology scale (CR098a, 5 predictions) with explicit falsification criteria for every cosmology-scale entry. Particle-scale registry unmodified.

## What The Certificate Proves

- the three Phase 2 verdicts (09a, 14, 13) were sealed before this certificate
- the four upstream Phase 2 artifact sha256s reproduce the composite sha256 deterministically
- any future modification to a sealed Phase 2 verdict invalidates this certificate
- Phase 1 chain of custody (CR064a, CR106, CR098) is recorded but unmodified

## What The Certificate Does NOT Prove

- the SAM physics framework is correct (the certificate is about provenance, not physics)
- any quantitative match between SAM predictions and external data beyond what each underlying CR claims
- curator sign-off (still PROVISIONAL until human curator signs)

## Cryptographic Chain (Phase 2 primary objects)

```text
CR069a 09a Phase 2 verdict          = 6a4d7d7dfdbf0fbf5f717a11390700ed66424e330f75f0307a9985e3beff4055
CR112  14  Phase 2 verdict          = 632917ff7fcf9573e6b016103993fb739fdbcbae6aca1c8d6709202c583a7889
CR098a prediction commit lock       = f5ea66c9ffb02ef60d5b8fa99ba5e7eb1674b9042099b67e7b3fb90e79145dfe
CR098a Phase 2 registry CSV         = e867f2ba8e4e4aed27ed517dbe812d0cb0f9e72b3b6baaca73e876a5a1287986
composite Phase 2 sha256            = 282bed22adc035e1d524e71db98e29c40b8394eaa7392cd0fbf7e834aeaf60eb
```

## Chain of Custody (Phase 1, unmodified)

```text
CR064a 09a Phase 1 summary          = a2af5df2dd3ac83cd131bb8a09913d806d0ba57db70942f53b232a892f0173e6
CR106  14  Phase 1 verdict          = 09eb6ae0055ebe5e53db9c2dc3df205c0613c4af5671341b7d5b4e7e07aa0ea6
CR098  13  particle-scale registry  = 6884850496ee233ed799c886dc114c70e9930b9a6c9b9c7d5df867064751fb1e
BLINDNESS_PROTOCOL.md               = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## Immutability

CR113 modifies zero branch artifacts.  Every hash quoted above is computed from a file that was on disk BEFORE this CR ran.  Future reveals (SPARC vs G732c, Omega_b derivation) will appeal against the predictions registered in CR098a via NEW CRs; the registry CSV and this certificate are never modified inline.
