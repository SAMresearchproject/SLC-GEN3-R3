# CR219 Promoted Particle Rows Export

## Task

Export the formal CR119 matter-gated particle surface as a standalone CSV of
the 126 promoted particle rows.

## Source Boundary

- `09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_courtroom_matter_table.csv`
- `09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_courtroom_particle_table.csv`
- `09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/source_copies/latest_table_counts.csv`
- `09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/source_copies/latest_table_export_summary.json`

## Export Rule

The promoted-particle export is the CR119 matter table exactly as the
matter-gated 126-row surface.

Do not define the export by filtering the 321-row particle table on
`matter_row_allowed` or `latest_matter_row_allowed`; those flags include
open/heavy reveal candidates outside the formal CR119 126-row matter table.

## Expected Checks

- Export row count is exactly 126.
- Candidate IDs are unique.
- All exported rows have `matter_row_allowed=yes`.
- All exported rows have `latest_matter_row_allowed=yes`.
- Matter gate split is `63 PASS_STABLE_SINGLE_WRITE_MATTER` and
  `63 PASS_BOUND_COMPOSITE_MATTER`.
- Bin split is `63 stable_matter_rows` and `63 bound_composite_rows`.
- Exported candidate IDs are a subset of the CR119 321-row particle table.
- Known labels, where present, remain downstream reveal labels only and are
  not construction inputs.
