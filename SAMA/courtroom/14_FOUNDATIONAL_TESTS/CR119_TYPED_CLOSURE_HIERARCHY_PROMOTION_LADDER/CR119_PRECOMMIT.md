# CR119 Precommit -- Typed Closure Hierarchy and Promotion Ladder

record_id: `CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER`
task: `SAM_PROSPECTIVE_CR_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER_5_5_XHIGH`
classification: `STRUCTURAL_INTEGRATION_CR`
preflight_report: `artifacts/preflight_filled/PREFLIGHT_20260712_035641_no_script.md`

## Campaign Metadata

```text
prior_CR_result_inputs = true
prospective_holdout_eligible = false
language_or_meta_language_test = false
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
```

## Target Hierarchy

```text
h = 2
D = 3
R = 12
S = 8
X = 1
W = 9
Theta = 18
V = 27
F = 81
P = 80 [inherit CR283]
M = 126
N = 144
L = 162
```

## Exact Paths To Test

```text
X = D^(D-1) - S
W = S + X = D^2
Theta = h*W = R^2/S
V = D*W = D^3
F = D*V = W^2 = D^4
N = R^2 = S*Theta
M = N - Theta = (S-1)*Theta
L = h*F = W*Theta = N*(W/S)
P = F - X = S*(W+1) [conditional]
```

## Frozen Controls

Reject:

```text
PROMOTE_VOLUME(S8, D3) -> 24
operator insertion as a ledger row
A_OPERATOR == B_CONTACT_OPERATOR
B_CONTACT_OPERATOR == X1_AXIS_SELF_CHANNEL
scalar-only deduplication
automatic promotion of the P80/F81 edge beyond CR283
Higgs input into this hierarchy
```

## Required Outputs

The runner must generate `CR119_typed_hierarchy.json` and `CR119_LANGUAGE_HANDOFF_CONTRACT.json`, plus the required register, DAG, proof, model comparison, validation, provenance, and hash artifacts.

## Firewall

No SAM Language v0.3 path, registered contract, candidate implementation, expected output, holdout queue, forecast gate, or language regression is an input to this CR.
