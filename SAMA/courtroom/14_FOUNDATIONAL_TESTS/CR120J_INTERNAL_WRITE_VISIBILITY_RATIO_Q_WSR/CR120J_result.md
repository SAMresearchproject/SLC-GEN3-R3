# CR120J Internal Write-Visibility Ratio q_WSR

record_id: `CR120J_INTERNAL_WRITE_VISIBILITY_RATIO_Q_WSR`
result_class: `MATHEMATICAL_RESEARCH_BOUNDARY`
scientific_pass_claimed: `false`
disposition: `RESEARCH_BOUNDARY_INTERNAL_WRITE_VISIBILITY_RATIO_Q_WSR_DEFINED_ON_ELIGIBLE_NONZERO_BUDGET_HISTORIES_EXACT_CALIBRATION_COLLISION_SCALE_AND_HELDOUT_AUDITS_PASS_PHYSICAL_MAPPING_OPEN`

## Direct result

The adjusted internal statistic executes exactly as a partial typed ratio:

```text
q_WSR = A_H/(A_H+B_H) only when A_H+B_H > 0

empty history                 NULL_HISTORY       q=null
nonempty perfect cancellation CANCELED_NONEMPTY  q=null
eligible nonzero budget       DEFINED            0 <= q <= 1
```

`A_H` is the current full-probe state budget. `B_H` is the accumulated typed
residue budget. Their relative unit scale is not fitted: both inherit the
standard exact norm isometrically from the common constructed `Q^81` input
fixture. The raw state and residue types remain distinct.

`q_WSR` is therefore a current write-visibility ratio, not a conserved share of
total history. The pathwise diagnostics `C_H` and `T_H` expose coherent
accumulation and cancellation separately.

## Exact calibration

```text
[]          NULL_HISTORY       q=null
[e1]        DEFINED            q=1
[e2]        DEFINED            q=1
[e0+e1]     DEFINED            q=1/2
[e0]        DEFINED            q=0
```

The required collision is preserved: `[e1]` and `[e2]` have equal `q_WSR=1`
but unequal full-probe states. Equal q does not mean equal record.

## Held-out results

```text
[e1,e1]             A=4 B=0  q=1
[e1,-e1]            A=0 B=0  CANCELED_NONEMPTY q=null
[e0+2e1]            A=4 B=1  q=4/5
[e0+e1,-e0]         A=1 B=2  q=1/3
[e0+e1,-e1]         A=0 B=1  q=0
[e0+e1,e2]          A=2 B=1  q=2/3
[e2,e0+e1]          A=2 B=1  q=2/3
```

The last pair has the same snapshot and ratio but different write order. The
ratio remains a lossy summary, not the reel or transcript.

## Scale, probe, delay, and erasure controls

The frozen mixed write `[e0+e1]` changes under illicit relative-scale choices:

```text
s_K=1/2  q=1/5
s_K=1    q=1/2  authoritative isometric lock
s_K=2    q=4/5
```

This confirms that scale matters and must not be retuned. The incomplete probe
control hides `e2`, producing an invalid zero denominator for `[e2]` and changing
`[e0+e2]` from `q=1/2` to an apparent `q=0`; both reduced-probe outputs are
rejected.

Sixteen identity delays preserve the state and give `rho_16=1`. This is exact
fixture persistence, not physical time evidence.

```text
exact inverse        CANCELED_NONEMPTY q=null; scar ratio 0
sham                 q=1; scar ratio 1
summary-only erase   q ineligible; scar ratio 2
overwrite            q=1; scar ratio 2
```

`q_WSR` is not an erasure detector; scar response remains separate.

## Bounded representation audit

`Q_ID`, `Q_12`, `Q_123`, `Q_SIGN_13`, and `Q_FAR` preserve every calibration
and held-out status and value under covariant probe transport. `Q_MIX_X1`
changes the raw X1-only value from `q=0` to `q=1` while failing X1 preservation
and `Pi80` commutation, so it is rejected without projector, probe, or scale
repair.

This finite result is not general basis invariance.

## Authority boundary

`q_WSR` is a constructed `InternalWriteVisibilityRatio`, not an installed SAM
operator, physical observable, closure field, or empirical parameter.

- No clock, GPS, supernova, thermodynamic, cosmological, particle, redshift,
  locality, or physical-time data entered the definition or run.
- `P80_PARTICLE_FACE_CONTENT` remains `STRUCTURAL_ONLY` and unpopulated.
- The language and registries are unchanged.

The CR120 frontier remains:

```text
PROPAGATE_CLOSURE       MISSING
LEDGER_SITE             MISSING
ADJACENT                MISSING
ADJACENT_LEDGER_STATE   MISSING
```
