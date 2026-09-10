# CR219 Promoted Particle Rows Export

Result: **CR219_PASS_PROMOTED_PARTICLE_ROWS_EXPORT__126_ROWS__CR119_MATTER_GATE_SURFACE__63_STABLE_PLUS_63_BOUND**

## Direct Answer

The requested 126 promoted particle rows are exported to:

`09a_PARTICLE_MASS_CHAIN/CR219_PROMOTED_PARTICLE_ROWS_EXPORT/CR219_promoted_particle_rows_126.csv`

## Source

The export is copied from the formal CR119 matter-gated table:

`09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_courtroom_matter_table.csv`

## Checks

- Export rows: 126
- Candidate IDs: 126 unique
- Bin split: 63 `stable_matter_rows` + 63 `bound_composite_rows`
- Matter gate split: 63 `PASS_STABLE_SINGLE_WRITE_MATTER` + 63 `PASS_BOUND_COMPOSITE_MATTER`
- All exported rows have `matter_row_allowed=yes`
- All exported rows have `latest_matter_row_allowed=yes`
- Exported candidate IDs are present in the CR119 321-row particle table

## Boundary

This export uses the CR119 126-row matter table as the promoted particle
surface. It does not filter the full 321-row particle table by
`matter_row_allowed` or `latest_matter_row_allowed`, because those flags also
include open/heavy particle candidates outside the formal promoted 126.
