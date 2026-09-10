# CR013 d_ref = 1 Prior-Testing Support Note

**Prepared:** 2026-07-03  
**Task preflight:** `artifacts/preflight_filled/PREFLIGHT_20260703_121118_no_script.md`  
**Scope:** documentation of prior support for `d_ref = 1` as the inherited SLC unit-spacing normalization.  
**Status:** SUPPORTS NORMALIZATION; DOES NOT DERIVE AN ABSOLUTE SI LENGTH.

## Bottom line

The pre-2026-06-26 SLC record supports `d_ref = 1` as the unit-spacing
normalization used in the distance-coupling tests and inherited by the SLC
networking layer.

This note does not claim that `d_ref = 1` was derived from substrate atoms as
an absolute SI length. The support is narrower and cleaner:

```text
d_ref = unit spacing (chosen = 1)
d(X, Y) measured in d_ref units
d(X, X) = d_ref
```

That normalization was then used in CR004's tested 1/r A-kernel, where the
`d=1` row, the `d=R=12` row, the distance sweep, and the wrong controls all
passed against the precommitted formula.

## Evidence chain

### 1. Historical assignment: d_ref is unit spacing, chosen as 1

Source: `C:\VS\chat_history\Chat5-QGC_Subtrate_Shape.md`

Relevant lines:

- line 9585: `site Y receives A-shift contribution = (1/N_max) * (d_ref / d(X, Y))`
- line 9587: `where d_ref = unit spacing (chosen = 1)`
- line 9588: `d(X, Y) = distance between sites X and Y (in d_ref units)`
- line 9589: `d(X, X) = d_ref (self-reference; LCQC006a self_distance choice)`

Role: CHAT-tier historical source. This is the direct origin found for the
`chosen = 1` assignment. It is a stipulation/normalization, not a derivation.

### 2. Courtroom CR004 precommit inherited the same normalization

Source: `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_PRECOMMIT.md`

Relevant lines:

- line 71: `site Y receives A-shift contribution = (1/N_max) * (d_ref / d(X, Y))`
- line 73: `where d_ref = unit spacing (chosen = 1)`
- line 74: `d(X, Y) = distance between sites X and Y (in d_ref units)`
- line 75: `d(X, X) = d_ref (self-reference; LCQC006a self_distance choice)`
- lines 245-247: sub-spacing distances below `d_ref` are out of scope and would require separate A-kernel typing.

Role: PRECOMMIT-tier source. CR004 turns the Chat5 normalization into the
precommitted testing basis for the distance-dependent SLC A-kernel.

### 3. CR004 PASS tested the normalized distance kernel, including d = 1

Source: `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_result.md`

Relevant result lines:

- line 3: CR004 verdict is `PASS`.
- lines 14-17: budget consumption matches the typed LCQC006 v2 1/r A-kernel prediction across 6 distances.
- lines 19-27: main test at `d = R = 12` matches predicted `cumA_A` and `cumA_B` exactly.
- lines 38-43: distance sweep rows at `d = 1, 2, 6, 12, 100, 10000` all PASS.
- lines 47-48: at `d = 1`, `cumA_A = cumA_B = 5*S^2/N_max` exactly because `(3 + 2/d) = (2 + 3/d) = 5`.
- lines 77-83: wrong controls PASS, including WC-3 verifying 1/r rather than 1/d^2.
- lines 94-103: all six PASS conditions are met.
- lines 132-134: observed cumulative A matches 1/r exactly and not the 1/d^2 alternative.
- lines 229-233: sealed PASS statement records predicted 1/r-coupled budget across 6 distances.

Role: RESULT-tier support. CR004 does not derive `d_ref`; it tests the
distance kernel after distances have been normalized in `d_ref` units. The
successful `d=1` row is therefore direct test support for the unit-spacing
normalization being operationally coherent.

### 4. CR004 structured artifacts preserve the same result

Sources:

- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_distance_sweep.csv`
- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_wrong_controls.csv`
- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_summary.json`

Observed support:

- `CR004_distance_sweep.csv` records all tested distances as passing:
  `1.0`, `2.0`, `6.0`, `12.0`, `100.0`, `10000.0`.
- The `d=1.0` row has predicted and observed `cumA_A` both equal to
  `0.005219206680584551`, predicted and observed `cumA_B` both equal to the
  same value, and final correlation `(1, 1)`.
- `CR004_wrong_controls.csv` records WC-3 as PASS: the runner matches the
  1/r prediction and does not match the 1/d^2 prediction.
- `CR004_summary.json` records `verdict = PASS`, `main_test_pass = true`,
  `distance_sweep.all_pass = true`, and `wrong_controls.all_pass = true`.

Role: machine-readable result support for the CR004 verdict.

### 5. LCQC006 inherited the tested coupling form

Sources:

- `18_SAM_NATIVE_QC/LCQC006_NETWORKING_AND_RING_TOPOLOGY/LCQC006_NETWORKING_AND_RING_TOPOLOGY.md`
- `18_SAM_NATIVE_QC/LCQC006_NETWORKING_AND_RING_TOPOLOGY/LCQC006_NETWORKING_AND_RING_TOPOLOGY_v2.md`

Relevant lines in v1:

- lines 63-68: `A_field at site j = A_0 * (d_ref / d(i, j))`, with `d_ref` defined as the per-write reference distance.
- lines 89-90: coupling strength scales as `A_0 * d_ref / d` per substrate write.

Relevant lines in v2:

- lines 51-56: same `A_0 * (d_ref / d(i, j))` form and per-write reference-distance definition.
- lines 82-83: same 1/r site-to-site scaling.

Role: layer-inheritance support. LCQC006 carries the normalized CR004 coupling
form into the networking/ring-topology layer.

### 6. SLC simulator uses normalized distance coordinates

Sources:

- `18_SAM_NATIVE_QC/SLC_substrate_ledger_simulator/slc_ledger/topology.py`
- `18_SAM_NATIVE_QC/SLC_substrate_ledger_simulator/slc_ledger/experiments.py`
- `18_SAM_NATIVE_QC/SLC_substrate_ledger_simulator/example_outputs/coupling_model_sweep.csv`

Relevant code:

- `topology.py` lines 161-165: builds a coordinate distance matrix.
- `topology.py` lines 178-191: `inverse_distance` is implemented as `strength / distances`.
- `experiments.py` lines 96-125: the coupling sweep samples target faces by normalized distance.
- `coupling_model_sweep.csv` rows include distance values `1.0`, `2.0`, `3.0`, `4.0`, and `4.031128874149275`, with inverse-distance outputs recorded separately from grid, inverse-square, and exponential controls.

Role: simulator-consistency support. The simulator does not name a `d_ref`
variable. Instead, it operates in normalized coordinate distances, consistent
with the prior `d_ref = unit spacing = 1` convention.

## What is supported

The prior testing supports the following statement:

```text
For the SLC distance-coupling tests and simulator-normalized coordinates,
d_ref = 1 is the inherited unit-spacing normalization. Distances d are read in
d_ref units. Under that convention, CR004's 1/r A-kernel passes the main test,
the d=1 unit-distance row, the six-distance sweep, and the 1/r-vs-1/d^2 wrong
control.
```

## What is not supported

This evidence does not support any of the following stronger claims:

- `d_ref = 1` is derived from substrate atoms as an absolute SI length.
- `d_ref = 1 meter`.
- `d_ref = 1 Planck length`.
- The CR010/CR011 post-2026-06-26 loop-scale derivation is pre-2026-06-26 evidence.
- A post-hoc derivation sweep has closed the absolute `d_ref` question.

## Citation hierarchy

```text
RESULT-tier:
  CR004_result.md
  CR004_distance_sweep.csv
  CR004_wrong_controls.csv
  CR004_summary.json

PRECOMMIT-tier:
  CR004_PRECOMMIT.md

LAYER-INHERITANCE:
  LCQC006_NETWORKING_AND_RING_TOPOLOGY.md
  LCQC006_NETWORKING_AND_RING_TOPOLOGY_v2.md

SIMULATOR-CONSISTENCY:
  SLC_substrate_ledger_simulator/slc_ledger/topology.py
  SLC_substrate_ledger_simulator/slc_ledger/experiments.py
  SLC_substrate_ledger_simulator/example_outputs/coupling_model_sweep.csv

CHAT-tier origin:
  C:\VS\chat_history\Chat5-QGC_Subtrate_Shape.md
  C:\VS\chat_history\Chat4-CR238.md
```

## Recommended use

Use this note to support wording such as:

```text
The SLC simulator and CR004 distance-coupling tests use the inherited
unit-spacing convention d_ref = 1. This convention is explicitly present in
the pre-6/26 SLC record and is operationally supported by the CR004 PASS
distance sweep and wrong controls. Its status remains normalization support,
not a derivation of an absolute SI d_ref.
```

Do not cite this note as an absolute-length derivation.
