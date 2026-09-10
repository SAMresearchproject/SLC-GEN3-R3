# CR280 Precommit: CR253 Stable-Matter Surface Semantic Clarification

record_id: CR280
record_name: CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION
campaign: SAM_COURTROOM_THREE_RECORD_PROMOTION_CAMPAIGN_5_5_XHIGH
destination: 09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION
precommit_written_before_runner: true

## Objective

Clarify and seal what CR253 produces:

```text
QP093A finite candidate catalog
-> CR253 compatibility/promoter rules
-> 80-row structurally stable matter surface
-> controlled naming and deterministic placeholder addressing
```

This record must not claim that every promoted row is an experimentally
identified, independently real, permanently stable particle.

## Required Semantic Type

```text
TensorCompatibleStableMatterSurface
StructurallyStableMatterRow
```

The explicit distinction is:

```text
StructurallyStableMatterRow != ExperimentallyIdentifiedParticle
```

The unqualified type `StablePhysicalParticle` is forbidden for CR253 rows.

## Permitted Source Set

| source | role | sha256 |
| --- | --- | --- |
| QP093A source | enumerator source | c6010a34c94fac0012e45e84df232fbb86d6ebec3f19d48632e8e793795f45b3 |
| QP093A result | finite catalog result | 504d2fb5152072248faf7f96e2bbbfa5d033d289e30bc21829af293b29215af5 |
| QP093A summary | enumerator summary | 0fab75381e2c27a8c98456016fd3f15781dbd338d11398788235d01f92333891 |
| QP104 corrected 299 catalog | corrected QP093A output | 33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c |
| CR119 summary | QP093A boundary and row discipline | 1eb2ba0c12d2079fc395cfa28e41693e9525af3cd394f8c9caa0f4393e0bcb53 |
| CR253 summary | promoter census | 06a023d5bd231ffdc2e441044936191c48fd861a9f56007e3408401934ad9aa0 |
| CR253 result | promoter boundary language | fd944b04ae0701d1c1bbf25eb7860f808a3eb83f7e94d050c8b6858b5c0861e5 |
| CR253 promoted rows | row source | 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b |
| CR254 summary | charged matter law | ac5cb2bc8d884fab0d10e55c81db6fa9401b01779bd710d1d43d7e26367d3074 |
| CR255 summary | neutral matter law | f9d2c88b2d78e76f56bbea71340ac1a5e94a3cefb75aba84c6cde017d9e25da9 |
| CR256 summary | antimatter conjugate law | 721a64f48b4977d736a4e362f4091857fd8628c4808444ce78d3159b8a7f630b |
| CR257 summary | depth-one compact form, context only | db5b8ff0010a6984d82893e4c392320829f1408a20e02bde1376ecabe1768788 |
| SAM Volume II draft | 80-row surface naming discipline | 7b6b266c85735c56cfe27d4f49ad7121e0b77eb13c2f010acfcd2aca7927d471 |

## Locked Replay Invariants

The runner must verify exactly:

```text
total promoted rows = 80
matter rows         = 48
antimatter rows     = 32
conjugate parity    = 32/32 source-defined exact count
row laws            = CR254 32/32, CR255 16/16, CR256 32/32
```

CR253 original verdict must remain:

```text
BOUNDARY
```

and the boundary reason must be preserved: W3 and W4 were insensitive because
the upstream bin plus h_T filters subsumed those controls; the core 80-row
promoter finding itself remains exact.

## Naming Discipline

Only rows meeting a source-authorized exact naming rule may receive a
conventional particle name.

Every other promoted row receives a deterministic placeholder:

```text
SAM[row=<row_id>,p=<partition_signature>,sign=<q_sign>,depth=<closure_depth>,class=<identity_rule>]
```

This placeholder must be:

- deterministic;
- collision-free;
- reversible to the source row;
- free of unsupported PDG names;
- free of implied mass or lifetime claims;
- stable across reruns.

Allowed status labels are restricted to source-supported strengths:

```text
EXACT_CONTACT
SECTOR_HINT
MIRROR
NEUTRAL_ANCHOR
SUBSTRATE_CANDIDATE
INDEPENDENT_EXISTENCE_UNRESOLVED
```

Do not invent categories to fill fields.

## Guards

Reject:

1. naming every promoted row as a known particle;
2. treating tensor compatibility as proof of experimental existence;
3. treating a placeholder as a PDG identity;
4. using PDG membership to decide promotion;
5. changing the 80/48/32 census;
6. applying the Be-8 nuclear stability cipher as the CR253 row selector.

## Verdict Tree

Return exactly one primary verdict:

```text
PASS_CR253_SEMANTIC_CLARIFICATION
BOUNDARY_CR253_NAMING_CONTRACT_INCOMPLETE
FAIL_CR253_REPLAY_OR_CENSUS
INVALID_CR253_SOURCE_CHAIN
```

PASS requires:

- every required source exists and hashes to the precommitted value;
- source CR253 summary reports n_promoted=80, n_matter=48, n_anti=32;
- source CR253 verdict BOUNDARY is preserved;
- CR254/CR255/CR256 report PASS and exact sector closures;
- every emitted row has a placeholder identifier reversible to row_id;
- conventional_name is populated only for source-authorized exact contacts;
- row type is StructurallyStableMatterRow, not StablePhysicalParticle;
- all six guards reject the forbidden moves.

If sources are missing or hash-invalid, return INVALID_CR253_SOURCE_CHAIN. If
the census or replay fails, return FAIL_CR253_REPLAY_OR_CENSUS. If the source
data cannot support the naming contract, return
BOUNDARY_CR253_NAMING_CONTRACT_INCOMPLETE without changing CR253.
