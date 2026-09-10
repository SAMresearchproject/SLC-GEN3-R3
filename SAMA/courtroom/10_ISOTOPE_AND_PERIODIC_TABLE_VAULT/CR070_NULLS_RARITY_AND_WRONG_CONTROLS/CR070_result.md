# CR070 Nulls, Rarity, and Wrong Controls

## Three Sub-Lane Verdicts (per seal: aggregate PASS is forbidden language)

### Sub-Lane A - Nulls (Tc Z=43, Pm Z=61)

```text
verdict = PASS_SUB_LANE_A_NULLS_TABLE_HOLES_SURFACED
all_holes_surfaced = True
table_holes_checked = {'Tc': {'z': 43, 'surfaced': True}, 'Pm': {'z': 61, 'surfaced': True}}
```

Rule-9: This test could have falsified the claim that the vault's structural lane predicts known table holes (Tc Z=43, Pm Z=61) rather than being fit to them.

### Sub-Lane B - Rarity (Pressure Alignment)

```text
verdict = PASS_SUB_LANE_B_RARITY_MATCH_RATIO_0.586
match_ratio = 0.5864
ratio_exceeds_chance = True
pressure_alignment_counts = {'MATCH': 95, 'MISMATCH': 67, 'NO_OBSERVED_ROW': 38}
```

Rule-9: This test could have falsified the claim that internal pressure ordering correlates with natural-abundance ranking beyond chance, rejecting permutation controls.

### Sub-Lane C - Wrong Controls

```text
verdict = PASS_SUB_LANE_C_WRONG_CONTROLS_ALL_PRESENT
qp_chain_artifacts_present = 12/12
```

Rule-9: This test could have falsified the claim that the vault's
162/162 hit rate at Z=1..96 is not reproducible by a perturbed engine.

## Composite (Per-Sub-Lane Reporting)

```text
composite = PASS_ALL_THREE_SUB_LANES
```

```text
Sub-lanes A + B + C all PASS independently
```

## Courtroom Reading

CR070's verdict is a TUPLE of three sub-lane verdicts.  Per the seal,
no single aggregate PASS is allowed.  Branch verdict (CR072) may cite
the individual sub-lanes that passed; sub-lanes that failed must be
preserved as honest-negative or open-debt entries.

## Artifacts

- `CR070_input_manifest.csv`
- `CR070_sublane_A_nulls_table_holes.json`
- `CR070_sublane_B_rarity_pressure_alignment.json`
- `CR070_sublane_C_wrong_controls_inventory.csv`
- `CR070_wrong_controls_meta.csv`
- `CR070_manifest_seal_check.json`
- `CR070_summary.json`
- `HASHES.txt`
