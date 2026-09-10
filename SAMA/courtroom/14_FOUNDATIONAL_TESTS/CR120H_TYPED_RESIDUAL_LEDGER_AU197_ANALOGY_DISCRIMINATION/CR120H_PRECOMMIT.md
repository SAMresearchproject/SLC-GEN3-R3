# CR120H Precommit

record_id: `CR120H_TYPED_RESIDUAL_LEDGER_AU197_ANALOGY_DISCRIMINATION`
task: `next up`
classification: `CONSTRUCTIVE_NEW_WORK / MATHEMATICAL_RESEARCH_BOUNDARY`
scientific_pass_claimed: `false`
proposal_source_sha256: `12f010fc058bd2109dda8ccf3b05ef495939601c174fd801dc9ba2a549ecafb0`

## Question frozen before execution

Determine whether the constructed CR120G closure split and the frozen Au-197
binding packet share a reusable typed accounting shape without identifying
their quantities, operators, units, residuals, or mechanisms.

This is the next staged proposal test after CR120G. It does not rerun CR120G,
refit the nuclear surface, define the proposed response scalar `q`, or test any
clock or supernova coupling.

## Generic accounting shape

Freeze the five-slot schema:

```text
base + operator_adjustment = program_final
reference - program_final = post_program_residual
```

Each slot retains its domain-specific type, unit, provenance, and authority.
A shared equation shape is not entity identity, operator identity, physical
coupling, or evidence of a common mechanism.

The word `debit` is not precommitted as a universal sign. The installed CR277
surface uses:

```text
B_u_final = B_u_base + op_contribution
```

A negative contribution acts debit-like, a positive contribution acts
credit-like, and a zero contribution is a null operator slot.

## Frozen CR120G projection into the schema

Use only the already sealed constructed split:

```text
parent = e0 + e1 + e2
left   = e0
right  = e1
kappa  = e2
I(v)   = sum of coordinates
```

Freeze this schema projection:

```text
base                    I(left)+I(right) = 2
operator_adjustment     I(kappa)         = 1
program_final           base+adjustment = 3
reference               I(parent)        = 3
post_program_residual   reference-final  = 0
```

Types remain distinct:

```text
ConstructedDaughterSubtotalCount
ConstructedSplitResidueCount
ConstructedReconstructedParentCount
ConstructedParentInvariantCount
ConstructedClosureReconciliationCount
```

`kappa` is a constructed split residue. It is not the installed
`B_CONTACT_OPERATOR`, a nuclear operator contribution, a nuclear residual, or a
carrier.

## Frozen Au-197 projection into the schema

Use the sealed V4.2 packet values exactly as decimal MeV quantities:

```text
base                    B_u_base                 27.421477 MeV
operator_adjustment     op_contribution           0.000000 MeV
program_final           B_u_final                27.421477 MeV
reference               B_u_obs                  31.139752 MeV
post_program_residual   B_u_obs - B_u_final       3.718275 MeV
```

Types remain distinct:

```text
NuclearBindingBaseMeV
NuclearOperatorContributionMeV
NuclearBindingPredictionMeV
NuclearBindingObservationMeV
NuclearPostPredictionResidualMeV
```

Au-197 has an exactly zero operator contribution. It can exercise the generic
accounting schema but cannot test whether a nonzero operator adjustment behaves
like the CR120G residue.

The underlying CR277 table is a sign/control surface only. For every row with
the necessary fields, require within `0.000002 MeV`, the tolerance implied by
six-decimal serialized inputs:

```text
B_u_final = B_u_base + op_contribution
residual_MeV = B_u_final - B_u_obs
```

Require the table to contain positive, negative, and zero operator
contributions. No fit, row selection by performance, or parameter change is
allowed.

## Precommitted discriminations

1. The five-slot equation shape must close on both frozen projections.
2. Slot order and residual sign must remain explicit.
3. The two projections must retain different types, units, provenance, and
   authority.
4. CR120G `kappa` maps only to the generic adjustment slot; it does not map to
   the Au-197 quantity as an entity.
5. Au-197 `op_contribution=0` requires the operator-effect readout `NULL`.
6. Au-197's `3.718275 MeV` is a post-program observation residual, not its
   operator contribution.
7. The CR277 table must verify the installed plus-sign contribution rule across
   positive, negative, and zero contribution rows.
8. No scalar normalization, unit stripping, or fitted scale factor may be used
   to force the closure and nuclear values to coincide.
9. `P80_PARTICLE_FACE_CONTENT` remains `STRUCTURAL_ONLY` and unpopulated.
10. The CR120 frontier remains missing and unused.

## Frozen wrong controls

```text
WC1  omit CR120G kappa
     expected: reconstructed value 2; reconciliation residual 1

WC2  treat Au-197 post-program residual as operator contribution
     expected: reject; wrong slot, wrong provenance, and 3.718275 != 0

WC3  replace installed CR277 plus rule with base - op_contribution
     expected: reject on nonzero-contribution rows

WC4  force a nonzero operator on Au-197
     expected: reject using frozen DRIVE_002 wrong-control record

WC5  use B_u_obs as the program generator
     expected: reject as frozen target leakage

WC6  identify CR120G kappa with nuclear operator contribution
     expected: reject by domain, type, unit, provenance, and value

WC7  identify CR120G reconciliation residual with the Au-197 residual
     expected: reject by domain, type, unit, provenance, and value
```

## Authority boundary

The candidate may establish only a shared abstract accounting shape. It must
not establish:

- a closure-to-binding operator;
- identity between `B_CONTACT_OPERATOR` and any CR277 operator;
- identity between constructed `kappa` and a nuclear contribution or residual;
- a physical mapping from F81/X1/P80 to Au-197;
- a response scalar `q`;
- a clock, location, redshift, or supernova coupling;
- a particle interpretation of P80; or
- any missing CR120 relation.

The frontier remains:

```text
PROPAGATE_CLOSURE       MISSING
LEDGER_SITE             MISSING
ADJACENT                MISSING
ADJACENT_LEDGER_STATE   MISSING
```

## Precommitted disposition

If all schema gates and wrong controls behave as frozen, record:

`RESEARCH_BOUNDARY_TYPED_LEDGER_SHAPE_SHARED_AU197_OPERATOR_SLOT_NULL_CLOSURE_NUCLEAR_IDENTITY_REJECTED_MECHANISM_MAPPING_OPEN`

This is not a scientific PASS. It establishes a reusable typed accounting
interface and a decisive Au-197 null boundary only.

## Frozen sources

```text
12f010fc058bd2109dda8ccf3b05ef495939601c174fd801dc9ba2a549ecafb0  C:/Users/drwho/.codex/attachments/46816fc7-3e0f-4f35-a705-72aa2857cec0/pasted-text.txt
06c4f480052285a5b1f932b76a6936efae12208a3d27a15f19366c47819964d2  14_FOUNDATIONAL_TESTS/CR120G_INTERNAL_SPLIT_RESIDUE_MIRROR_ODD_X1_COMPLEMENT/CR120G_CANDIDATE_MANIFEST.json
674eb90b4622716ba54e0f1883a541d89a1794865688e944c5e3a40fc961c29f  14_FOUNDATIONAL_TESTS/CR120G_INTERNAL_SPLIT_RESIDUE_MIRROR_ODD_X1_COMPLEMENT/CR120G_MODEL_EXECUTION.json
bad00364dbd2af0fb4db455a13a1fbba0c18a0e51508d79eac5ad2fccee00bae  14_FOUNDATIONAL_TESTS/CR120G_INTERNAL_SPLIT_RESIDUE_MIRROR_ODD_X1_COMPLEMENT/CR120G_ROLE_DISCRIMINATION.json
6eab2b1b3612774a9c540e9ed8407c2299f4a3b3666b614f9f0860c07ef27263  14_FOUNDATIONAL_TESTS/CR120G_INTERNAL_SPLIT_RESIDUE_MIRROR_ODD_X1_COMPLEMENT/CR120G_summary.json
cdfe69d3e4974d2009901bdfdc689e203489c714f49ea633c74463d242212042  SAM_NATIVE_V4_2_DRIVES/DRIVE_002_AU197_BINDING_BU_PACKET/DRIVE_002_AU197_BINDING_BU_RESULT.md
649305dbe5bf8748ff02603431bdc32fddf04ae6af87481308662cb5a1cb05ed  SAM_NATIVE_V4_2_DRIVES/DRIVE_002_AU197_BINDING_BU_PACKET/DRIVE_002_AU197_BINDING_BU_RESULT.json
75137d3ae74c02d332b744bb037fd825b2ebd51f3d56a4b04e939198ed588258  SAM_NATIVE_V4_2_DRIVES/DRIVE_002_AU197_BINDING_BU_PACKET/DRIVE_002_AU197_BU_PACKET.csv
8d5fff8e6b934c131487bbac2ef2d82289999356953a380d97717445c4ea23ba  SAM_NATIVE_V4_2_DRIVES/DRIVE_002_AU197_BINDING_BU_PACKET/DRIVE_002_WRONG_CONTROLS.csv
568217613ac1fb638745a33e05d174009038d2fdf0041f968f5ff46a029dd384  SAM_NATIVE_V4_2_DRIVES/DRIVE_002_AU197_BINDING_BU_PACKET/DRIVE_002_SOURCE_MANIFEST.json
65fd9d8267cc3eaa4fc268df0cb941790be37777048a1a9bdf435b01c1802ac1  09a_PARTICLE_MASS_CHAIN/CR277_ONE_HUNDRED_TWENTY_SIX_ELEMENT_TABLE_AND_SOB_FRONTIER_LOCKS/CR277_element_table.csv
72fc859df41b277226a5693620ceb711de5b6fd107a8408f5a90ef8eab9dc63c  SAM_LANGUAGE_V0_4_2_CANDIDATE/contracts/CR119_LANGUAGE_HANDOFF_CONTRACT.json
09ddbf4dd2647249404b3b9bbc8a01625ad181e848cc592fc98119c5b05de1b9  SAM_LANGUAGE_V0_4_2_CANDIDATE/V0_4_1_ENTITY_REGISTRY.json
873f36e77b97e1e04f8d272af9f15e174ccf2605bec3fe7443be60bdf276935d  SAM_LANGUAGE_V0_4_2_CANDIDATE/V0_4_OPERATOR_REGISTRY.json
75b2b02261e014985c2df378a1cb17c6766e90240c69924ae8d27aad5d842a8f  14_FOUNDATIONAL_TESTS/CR120_LOCAL_CLOSURE_PROPAGATION_ADJACENT_LEDGER_SITE/CR120_result.md
```

## Hard stop

Stop after one sealed CR120H candidate. Do not define `q`, inspect clock or
supernova observations, add language operators, mutate a registry, populate
P80, assign particle identities, or infer any missing CR120 relation.
