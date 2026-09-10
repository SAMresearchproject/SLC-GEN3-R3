# Test 8 — Input Schema

## external_nuclide_table.csv

Required columns:

| column | type | notes |
|---|---|---|
| Z | int | proton number |
| N | int | neutron number |
| A | int | mass number; `A = Z + N` if missing |
| symbol | string | element symbol |
| half_life | string | free text from upstream source |
| half_life_sec | float or "inf" | seconds; `inf` for stable |
| is_stable | bool | true/false |
| isomer_flag | string | empty if unknown |
| isomer_status_unknown | bool | true when isomer state not separated |
| source | string | upstream provenance tag |

Alias normalization (applied before scoring):

```text
z -> Z, n -> N, a -> A, mass_number -> A, element -> symbol
half_life_seconds -> half_life_sec, stable -> is_stable, isomer -> isomer_flag
```

A row failing parse is not silently discarded; it is flagged.

Ground-state vs isomer:
- Where source distinguishes, ground states preferred.
- Where source does not distinguish (QP061 case), `isomer_status_unknown=true` on every row.

See `external_nuclide_table_SOURCE.txt` for upstream lineage and SHA chain.
