# CR063 Wrong Controls and Near Neighbors

## Verdict

```text
CR063_PASS_HONEST_NEGATIVES_REJECT
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_HONEST_NEGATIVES_REJECT
triage_bin = A
```

## Reason

```text
qp040 present; QGA wrong-controls present; hostile audit roll-forward NO_BLOCKER_FOUND; engine perturbations detected as chain-breaking
```

## Phase Summary

```text
Phase 1 manifest seal + hash       verified=572
Phase 2 qp040 honest-negative      status=honest_negative_present_and_hash_locked  rows=8
Phase 3 QGA wrong-controls         13/13 present with rows
Phase 4 hostile audit roll-forward status=audit_roll_forward_verified
Phase 5 engine perturbations       3/3 detected as chain-breaking
Phase 6 near-neighbor gap analysis 12/12 gaps exceed 1% strict tolerance
Phase 7 meta wrong controls        passed=6/6
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's parameter-free
particle predictions cannot be reproduced by deliberately perturbed
engines or dropped selectors, and that the qp040 without-observed-mass
replay correctly fails to reach PDG row-level tolerance bands.
```

## Courtroom Reading

CR063 is the honest-negatives gate for the 09 branch.  A
PASS_HONEST_NEGATIVES_REJECT verdict means the engine cannot be
trivially reproduced by perturbations: qp040 is present and hash-locked,
each in-scope QGA carries its own declared wrong-control set, the
hostile QP010-QP021 audit replay still ends NO_BLOCKER_FOUND, and every
declared engine perturbation breaks the chain in the manifest's
downstream impact.

## Artifacts

- `CR063_input_manifest.csv`
- `CR063_qp040_honest_negative_check.json`
- `CR063_qga_wrong_controls_inventory.csv`
- `CR063_hostile_audit_roll_forward.json`
- `CR063_engine_perturbation_simulations.csv`
- `CR063_near_neighbor_gap_analysis.csv`
- `CR063_wrong_controls.csv`
- `CR063_manifest_seal_check.json`
- `CR063_summary.json`
- `HASHES.txt`
