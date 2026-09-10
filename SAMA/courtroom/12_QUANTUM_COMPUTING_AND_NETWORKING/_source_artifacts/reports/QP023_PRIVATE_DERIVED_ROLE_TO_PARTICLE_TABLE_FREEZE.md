# QP023 - Private Derived Role To Particle Table Freeze

## Result

```text
QP023_DERIVED_PARTICLE_TABLE_FREEZE_BUILT
```

QP023 freezes the particle-table surface carried by QP022-derived topology. It
uses QP022D selected stable, boundary, and charged carrier lanes, then carries
downstream QP018/QP019/QP021 slot and mass-surface results into one table.

## Lane Counts

| derived replay lane | slot rows | frozen mass surfaces | open slots | frozen pairs |
| --- | ---: | ---: | ---: | --- |
| DERIVED_BOUNDARY_REORGANIZATION_LANE | 1 | 1 | 0 | c<->s |
| DERIVED_CHARGED_CARRIER_LANE | 6 | 2 | 4 | b<->c;b<->t |
| DERIVED_STABLE_ANCHOR_LANE | 5 | 1 | 4 | b<->s |

## Frozen Mass Surfaces

| pair | derived lane | selected mass readout MeV | freeze class |
| --- | --- | ---: | --- |
| c<->s | DERIVED_BOUNDARY_REORGANIZATION_LANE | 987.525383715 | BOUNDARY_REORGANIZATION_MASS_SURFACE_FROZEN |
| b<->c | DERIVED_CHARGED_CARRIER_LANE | 3950.10153486 | CHARGED_CARRIER_MASS_SURFACE_FROZEN |
| b<->t | DERIVED_CHARGED_CARRIER_LANE | 15800.4061394 | CHARGED_CARRIER_MASS_SURFACE_FROZEN |
| b<->s | DERIVED_STABLE_ANCHOR_LANE | 3978.71874985 | STABLE_ANCHOR_MASS_SURFACE_FROZEN |

## Key Fields

```text
particle_table_rows = 12
frozen_mass_surfaces = 4
open_slots = 8
legacy_role_operator_column_used_for_selection = False
selector_used_qp004_labels = False
```

## Interpretation

The derived QP022 topology now carries four frozen private particle mass
surfaces:

```text
stable anchor: b<->s
boundary reorganization: c<->s
charged carriers: b<->c, b<->t
```

The remaining rows stay visible as open scaffolds rather than being thrown away.

## Next Frontier

```text
QP024_PRIVATE_OPEN_SLOT_PROMOTION_SELECTOR
```
