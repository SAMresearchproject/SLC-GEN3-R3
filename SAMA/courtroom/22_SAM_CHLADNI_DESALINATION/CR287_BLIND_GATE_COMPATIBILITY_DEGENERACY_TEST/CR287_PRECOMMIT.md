# CR287 Precommit - Blind Gate Compatibility and Degeneracy Test

Record ID: `CR287_BLIND_GATE_COMPATIBILITY_DEGENERACY_TEST`

## Question

Does the coefficient-free CR285 compatibility operator produce any species or
gate ordering when the sealed CR286 observation-blind primary graphs are
mapped to the complete 960-gate passive membrane catalog?

## Frozen Inputs

CR287 may use only:

- the nine CR286 `OCT6_PRIMARY` species graphs;
- their six signed-axis envelope ports;
- the 960 CR285 directed gates;
- each gate's signed-axis vertices on its entry and complementary exit faces;
- the CR285 lexicographic compatibility vector;
- frozen IDs and provenance for stable output order only.

No measured molecular or membrane value is allowed.

## Typed Interface Rule

For a directed gate `g`, normalize the suffix of each vertex ID in the union
of `entry_vertices` and `exit_vertices`:

```text
P_g = {-x, +x, -y, +y, -z, +z}
```

For a CR286 primary species graph `s`:

```text
P_s = {-x, +x, -y, +y, -z, +z}
```

`HYDRATION_WATER` envelope ports and gate signed-axis vertex ports meet only
through equality in this abstract signed-axis boundary namespace. This is a
topology comparison, not a physical water-wall interaction claim.

The mapping is admissible only when `P_s = P_g` with six unique labels and all
species core contacts remain unchanged.

## Frozen Compatibility Vector

Use the CR285 vector without weights:

```text
K = (
  invalid_type_matches,
  broken_species_contacts,
  added_support_contacts,
  remaining_graph_edits
)
```

For an admissible exact boundary identification, the precommitted vector is:

```text
K = (0, 0, 0, 0)
```

Equal vectors remain tied. IDs stabilize file order only.

## Control Admissibility

- `TET4_EVEN_CONTROL` and `TET4_ODD_CONTROL` use a face-state bit namespace,
  not the signed-axis vertex namespace. They are rejected before ranking.
- `CORE_ONLY_CONTROL` has no boundary ports. It is rejected before ranking.
- Invalid controls receive no large penalty and cannot become pseudo-ranks.

## Precommitted Inventory

```text
species primary graphs               = 9
directed gates                       = 960
all graph x gate combinations        = 34,560
primary admissible mappings          = 8,640
control mappings rejected            = 25,920
distinct primary K vectors           = 1
species rank groups                  = 1
gate rank groups                     = 1
selectivity predictions              = 0
physical pore or material promotions = 0
```

Every one of the 960 directed gates is expected to expose the same normalized
six-port set. Triad signature and `source_matter_row_allowed` remain source
metadata; neither may select a species or break a tie.

## Boundary Rule

If all 8,640 primary comparisons collapse to one vector, CR287 records a
scientific `BOUNDARY`, not a selectivity PASS. The construction remains a
valid passive topology grammar, but it supplies no blind species or gate
ordering at this resolution.

## Explicitly Excluded

- hydrated or bare radius;
- preferred coordination or hydration number;
- hydration, de-coordination, or transport energy;
- charge density, bond lengths, bond angles, or partial charges;
- measured or simulated flux, rejection, permeability, or selectivity;
- an element-to-QP-triad selector;
- atomic-number, mass, row order, or candidate-ID tie breakers;
- using `source_matter_row_allowed` as a membrane ranking;
- physical size, material, wall chemistry, or functionalization;
- acoustic or Starbreaker variables;
- weighted scores or species-specific rescue rules.

## Pass and Boundary Conditions

Execution closes only if:

- every contract and source hash verifies;
- all 9 primary graphs and all 960 gates are complete;
- every gate normalizes to exactly the six signed-axis ports;
- all 8,640 primary mappings are admissible and have `K=(0,0,0,0)`;
- all 25,920 control mappings are rejected for the frozen type reason;
- all species and gates remain in one tied class;
- reverse gate pairs remain tied;
- no target, ranking, physical unit, or selectivity claim enters output;
- all wrong controls are rejected.

The scientific verdict is `BOUNDARY` when this expected collapse occurs.

## Rule-9 Line

This test could falsify the blind compatibility construction through missing
ports, non-complementary gate coverage, broken graph contacts, asymmetric
reverse mappings, source drift, target leakage, a hidden selector, a
species-specific rescue, or suppression of a complete tie.

## Expected Result Class

```text
CR287_BOUNDARY_BLIND_COMPATIBILITY_COLLAPSES_TO_ONE_ZERO_EDIT_CLASS__8640_PRIMARY_MAPPINGS__NO_SPECIES_OR_GATE_RANKING
```
