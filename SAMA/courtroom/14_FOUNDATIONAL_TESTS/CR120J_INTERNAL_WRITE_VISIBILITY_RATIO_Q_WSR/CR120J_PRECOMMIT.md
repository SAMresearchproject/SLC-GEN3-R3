# CR120J Precommit

record_id: `CR120J_INTERNAL_WRITE_VISIBILITY_RATIO_Q_WSR`
task: `Adjust and run the internal q_WSR candidate`
classification: `CONSTRUCTIVE_NEW_WORK / MATHEMATICAL_RESEARCH_BOUNDARY`
scientific_pass_claimed: `false`
proposal_source_sha256: `e58516c2f9151412be41635ea3ab09a0e5ee984b83f75a0799a8cb46b622aa01`

## Question frozen before execution

Can the CR120I exact-rational write fixture support one bounded, partial,
dimensionless internal write-visibility ratio `q_WSR` that:

1. keeps state, residue, probe, and history types distinct;
2. locks its relative normalization without observational tuning;
3. distinguishes defined, empty, and perfectly canceled histories;
4. records deliberate scalar collisions rather than hiding them;
5. survives the frozen complete-probe, delay, erasure, and finite-symmetry
   controls; and
6. remains internal-only, with no clock, supernova, thermodynamic, particle,
   locality, or physical-time interpretation?

`q_WSR` means `InternalWriteVisibilityRatio`. It is not named a general
closure scalar and is not a complete state, record, reel, memory magnitude, or
history decoder.

## Frozen fixture and types

Use the sealed CR120I construction exactly:

```text
U = Q^81 WriteInput
S = Q^81 HomeSnapshotState
K = separately tagged copy of span(e0) WriteResidue
P81 = ordered coordinate probes p0,...,p80
Y = Q RationalReadout
S_ref = 0
x = e0
Pi80 = diag(0,1,...,1)
W(S_n,u_n) = (S_n + Pi80*u_n, tag_K((I-Pi80)*u_n))
R(S,p_i) = S dot e_i
```

The standard exact inner product on `Q^81` is frozen for this constructed
fixture only.

## Isometric scale lock

Freeze the residue tag as an isometry inherited from the common input space:

```text
||tag_K((I-Pi80)u)||_K^2 = ||(I-Pi80)u||_U^2
sum_(p in P81) R(S,p)^2 = ||S||_S^2
s_Y = 1 basis readout unit
s_K = 1 basis residue unit
```

The state and residue remain different semantic types. Only their separately
normalized, dimensionless budgets may be added. No raw cross-type vector or
scalar equality is authorized.

Freeze relative-scale perturbations as wrong controls on the one-write mixed
history `[e0+e1]`:

```text
s_K=1/2 -> q=1/5
s_K=1   -> q=1/2  authoritative fixture lock
s_K=2   -> q=4/5
```

These controls must demonstrate that scale choice matters and that the
authoritative internal candidate uses the precommitted isometric lock only.

## Frozen budgets and eligibility

For an ordered history `H=[u_1,...,u_m]`, construct `S_H` by repeated `W` and
freeze:

```text
A_H = ||S_H-S_ref||_S^2 / s_Y^2
B_H = sum_n ||kappa_n||_K^2 / s_K^2
C_H = sum_n ||Pi80*u_n||_U^2
T_H = sum_n ||u_n||_U^2
```

Require the pathwise accounting diagnostic:

```text
T_H = C_H + B_H     under the authoritative unit-scale lock
```

`A_H` is the visible current-snapshot budget. `B_H` is the accumulated residue
budget. `C_H` and `T_H` diagnose coherent accumulation and cancellation.
Because `A_H` contains cross terms while `B_H` is pathwise, `q_WSR` is not a
conserved share of total history.

Freeze the partial statistic:

```text
if m=0:
    status = NULL_HISTORY
    q_WSR = null

if m>0 and A_H+B_H=0:
    status = CANCELED_NONEMPTY
    q_WSR = null

if A_H+B_H>0:
    status = DEFINED
    q_WSR = A_H/(A_H+B_H)
```

Every defined value must lie in `[0,1]` exactly. `q_WSR=0` is reserved for a
defined history with no visible current-state budget and a positive residue
budget. It does not mean no write, no information, or no conservation.

## Frozen calibration suite

```text
H_EMPTY=[]
  A=0 B=0 C=0 T=0 status=NULL_HISTORY q=null

H_E1=[e1]
  A=1 B=0 C=1 T=1 status=DEFINED q=1

H_E2=[e2]
  A=1 B=0 C=1 T=1 status=DEFINED q=1

H_MIX=[e0+e1]
  A=1 B=1 C=1 T=2 status=DEFINED q=1/2

H_X1=[e0]
  A=0 B=1 C=0 T=1 status=DEFINED q=0
```

The `H_E1/H_E2` equality is a required collision: equal `q_WSR`, unequal
full-probe states.

## Frozen supplied-history controls

```text
H_TERMINAL_A=[e1,e2]
  A=2 B=0 C=2 T=2 q=1

H_TERMINAL_B=[e2,e2]
  A=4 B=0 C=2 T=2 q=1
```

They share terminal input and `q_WSR` but have unequal full-probe states.

```text
H_ORDER_A=[e1,e2]
H_ORDER_B=[e2,e1]
```

They have equal states, budgets, and `q_WSR`, while their ordered histories
remain different. Neither the snapshot nor `q_WSR` is an ordered transcript.

After 16 identity delays on `H_E1`, require unchanged state, `A`, `q_WSR`, and
delay-retention ratio `rho_16=1`.

## Frozen erasure controls

```text
H_INVERSE=[e1,-e1]
  A=0 B=0 C=2 T=2
  status=CANCELED_NONEMPTY q=null
  scar ratio chi=0

SHAM after [e1]
  state=e1 q remains 1 chi=1

SUMMARY_ONLY_ERASE after [e1]
  state=e1-e2, restored scalar summary, chi=2
  q_WSR eligibility=INELIGIBLE_NON_WRITE_OPERATION

OVERWRITE=[e1,e2]
  state=e1+e2 q=1 chi=2
```

`q_WSR` is not an erasure detector. Scar response remains a separate
diagnostic.

## Frozen held-out rational suite

Freeze before execution:

```text
H_REPEAT=[e1,e1]
  A=4 B=0 C=2 T=2 status=DEFINED q=1

H_CANCEL=[e1,-e1]
  A=0 B=0 C=2 T=2 status=CANCELED_NONEMPTY q=null

H_MIXED_4_1=[e0+2e1]
  A=4 B=1 C=4 T=5 status=DEFINED q=4/5

H_RESIDUE_ACCUM=[e0+e1,-e0]
  A=1 B=2 C=1 T=3 status=DEFINED q=1/3

H_STATE_CANCEL_WITH_RESIDUE=[e0+e1,-e1]
  A=0 B=1 C=2 T=3 status=DEFINED q=0

H_ORDER_MIX_A=[e0+e1,e2]
H_ORDER_MIX_B=[e2,e0+e1]
  A=2 B=1 C=2 T=3 status=DEFINED q=2/3
  equal snapshots and q; different ordered histories
```

The held-out suite must be evaluated without changing formulas, probes,
reference, scales, projector, or null statuses.

## Probe controls

`P81` is the authoritative complete fixture probe family. Freeze the incomplete
family `{p1}` as a wrong control:

```text
[e2] under P81    -> A=1 B=0 q=1
[e2] under {p1}   -> apparent A=0 B=0; invalid zero denominator

[e0+e2] under P81  -> A=1 B=1 q=1/2
[e0+e2] under {p1} -> apparent A=0 B=1 q=0
```

The reduced-probe results must be marked `INCOMPLETE_PROBE_CONTROL`, never
accepted as authoritative `q_WSR` values.

## Bounded representation controls

Reuse the five precommitted CR120I admissible signed permutations:

```text
Q_ID, Q_12, Q_123, Q_SIGN_13, Q_FAR
```

Transform inputs, states, and probes covariantly. Each must preserve `A`, `B`,
`q_WSR` status, and defined value for every calibration and held-out history.

`Q_MIX_X1` remains inadmissible. On `[e0]`, the untransformed candidate has
`q_WSR=0`; the raw X1-mixed calculation gives `q=1`, while also failing X1
preservation and `Pi80` commutation. Record the change and reject the
transformation. Do not retune `Pi80`, probes, or scales.

This finite audit does not establish general basis invariance, a canonical
representation, or a physical decoder.

## Precommitted gates

1. Every frozen source hash must match before calculation.
2. CR120I types, write rule, probes, erasure states, and transformation family
   must match their sealed artifacts.
3. The isometric state/readout and residue-tag locks must hold exactly.
4. Every write must close its typed state and residue accounting exactly.
5. Every history must satisfy `T_H=C_H+B_H` exactly.
6. Calibration statuses, budgets, and `q_WSR` targets must match exactly.
7. Empty and canceled nonempty histories must remain separate typed nulls.
8. All defined `q_WSR` values must lie in `[0,1]`.
9. Scale perturbations must produce `1/5`, `1/2`, and `4/5` exactly without
   changing the authoritative lock.
10. Supplied collisions and order/terminal-input boundaries must remain
    visible.
11. Delay and erasure controls must match their frozen values while keeping
    scar response separate from `q_WSR`.
12. Every held-out rational target must match without retuning.
13. Reduced probes must produce the frozen wrong-control failures.
14. Five admissible transformations must preserve `q_WSR`; `Q_MIX_X1` must
    fail without repair.
15. No installed registry entry may be interpreted as `q_WSR`, its metrics,
    scales, state mutation, or physical mapping.
16. `P80_PARTICLE_FACE_CONTENT` remains `STRUCTURAL_ONLY` and unpopulated.
17. No clock, GPS, supernova, thermodynamic, cosmological, particle, redshift,
    locality, propagation, or physical-time data enter the candidate.
18. The CR120 frontier remains missing and unused.

## Precommitted disposition

If every exact gate and wrong control behaves as frozen, record:

`RESEARCH_BOUNDARY_INTERNAL_WRITE_VISIBILITY_RATIO_Q_WSR_DEFINED_ON_ELIGIBLE_NONZERO_BUDGET_HISTORIES_EXACT_CALIBRATION_COLLISION_SCALE_AND_HELDOUT_AUDITS_PASS_PHYSICAL_MAPPING_OPEN`

This is not a scientific PASS and does not authorize empirical exposure.

## Frozen sources

```text
e58516c2f9151412be41635ea3ab09a0e5ee984b83f75a0799a8cb46b622aa01  C:/Users/drwho/.codex/attachments/6054da11-70a1-4550-a751-1143cefd878f/pasted-text.txt
06c4f480052285a5b1f932b76a6936efae12208a3d27a15f19366c47819964d2  14_FOUNDATIONAL_TESTS/CR120G_INTERNAL_SPLIT_RESIDUE_MIRROR_ODD_X1_COMPLEMENT/CR120G_CANDIDATE_MANIFEST.json
60ce5fcb59d820e6f65957734174fc7922cf0754dbc13f6fdb0e4b2b62bb62a3  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_CANDIDATE_MANIFEST.json
dbbbb24ef23fef4cc4f633f0b6ee6f4f10bbf45bd79442437063ea669acbad21  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_TYPE_SYSTEM.json
4b19cd16b8ef08f7b03e03b92e528a47a00f858d285c6b4b065921daa7fe9286  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_WRITE_EXECUTION.json
8787298fddc86fc08ebc6fc1b6777b8221f273a3e4040eb82d5ee0938420e4d6  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_RECORD_EQUIVALENCE.json
32c492ba65b67d05a0655c1f934d63627a1a633ba6d0bc26b2432f2203f3e65e  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_PERSISTENCE_ERASURE.json
2bc86f544abbc25c5764e787ff93968f6c2cf5f8b135b75d3567f57853ea9ec2  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_REPRESENTATION_FAMILY.json
2cc46939d662f337568eec8813f6be2e1cf119eb1967e214e6a3131b65c85a72  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_AUTHORITY_BOUNDARY.json
f47eacaec6ef91fcbdc2004368d9531e0ef99237893bb3a0c3b6a80448566ad7  14_FOUNDATIONAL_TESTS/CR120I_TYPED_SUBSTRATE_LEDGER_WRITE_STATE_READ_DISCRIMINATION/CR120I_summary.json
09ddbf4dd2647249404b3b9bbc8a01625ad181e848cc592fc98119c5b05de1b9  SAM_LANGUAGE_V0_4_2_CANDIDATE/V0_4_1_ENTITY_REGISTRY.json
873f36e77b97e1e04f8d272af9f15e174ccf2605bec3fe7443be60bdf276935d  SAM_LANGUAGE_V0_4_2_CANDIDATE/V0_4_OPERATOR_REGISTRY.json
75b2b02261e014985c2df378a1cb17c6766e90240c69924ae8d27aad5d842a8f  14_FOUNDATIONAL_TESTS/CR120_LOCAL_CLOSURE_PROPAGATION_ADJACENT_LEDGER_SITE/CR120_result.md
```

## Hard stop

Stop after one sealed CR120J candidate. Do not expose `q_WSR` to any physical
packet or observation, mutate the language or registry, populate P80, or infer
any missing CR120 relation.
