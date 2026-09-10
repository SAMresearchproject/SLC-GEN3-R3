# CR214 CR119 Particle Complement Pattern Audit

Result: **CR214_PASS_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT__195_COMPLEMENT_ROWS_ACCOUNTED__MATTER_GATE_SPLIT_126_PLUS_195__OPEN_COUNT_LEADS_NOT_PROMOTED**

## Direct Answer

The 195 rows are the particle-table complement left after the CR119 matter gate selects 126 rows.
They are not one undifferentiated residue class.

## Count Spine

- Particle rows: 321
- Matter rows: 126
- Periodic rows: 126
- Particle-minus-matter complement: 195

## Matter Table Split

- bound_composite_rows: 63
- stable_matter_rows: 63

## Complement Split

- antimatter_conjugate_rows: 42
- bound_composite_rows: 106
- carrier_only_rows: 6
- hidden_source_support_rows: 8
- rejected_fake_closures: 8
- unstable_resonance_rows: 25

## Gate Readout

- REJECT_BIN_antimatter_conjugate_rows: 41
- REJECT_NOT_MATTER_ALLOWED: 36
- REJECT_STABILITY_SELECTOR_OPEN_OR_HEAVY: 118

## Pattern Leads

- BACKED: 321 = 126 selected matter rows + 195 complement rows.
- BACKED: the 126 matter rows split 63 stable single-write and 63 bound-composite rows.
- BACKED: the 195 complement is structured by the matter gate, not by periodic membership.
- OPEN: 118 stability-open/heavy complement rows equals 118 downstream known-Z rows, but CR214 records only a count match.
- OPEN: eight-row guard packets echo the Z119-Z126 frontier count, but CR214 records only a count match.

## Artifacts

- `CR214_particle_complement_195.csv`
- `CR214_all_particle_gate_reasons.csv`
- `CR214_complement_bin_summary.csv`
- `CR214_complement_gate_summary_195.csv`
- `CR214_pattern_leads.csv`
- `CR214_summary.json`
