# CR285 Coefficient-Free Compatibility Operator

## Purpose

Freeze how future typed species constructions will be compared with passive
gate constructions before any measured membrane or hydration result is opened.

## Typed Graphs

Future CR286 species candidates and CR285 gate candidates must each provide:

```text
node inventory
typed contact/edge inventory
boundary or port inventory
support requirements
source provenance for every graph item
```

CR285 supplies the gate side. The species side remains deliberately absent.

## Validity Gate

A comparison is invalid if it requires:

- a node or contact type absent from its frozen source grammar;
- an unresolved hidden-row-to-face or carrier-row-to-vertex assignment;
- measured hydrated radius, dehydration energy, flux, rejection, or
  selectivity to construct either graph;
- a physical-unit interpretation of QP numeric fields;
- acoustic or Starbreaker variables.

Invalid comparisons are not given a large penalty and retained. They are
rejected before ranking.

## Comparison Vector

For valid typed graphs, define:

```text
K = (
  invalid_type_matches,
  broken_species_contacts,
  added_support_contacts,
  remaining_graph_edits
)
```

The vector is compared lexicographically. No weighted sum is permitted.

- `invalid_type_matches` must be zero for a valid row.
- `broken_species_contacts` counts source contacts that cannot remain through
  the proposed gate mapping.
- `added_support_contacts` counts new support contacts required by the mapping.
- `remaining_graph_edits` counts other typed node/contact additions, removals,
  or reassignments after the first two categories are accounted for.

Equal vectors remain tied. Candidate IDs stabilize file order only and do not
choose a physical winner.

## Physical Reveal Boundary

The comparison vector is a topology hypothesis. A later reveal must test
whether its ordering predicts conventional quantities such as coordination
change, maximum cross-section, de-coordination barrier, permeability, and
selectivity. CR285 assigns no scale or coefficient connecting graph edits to
those quantities.
