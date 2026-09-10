# CR117 Source Audit

Record: `CR117_S8_TYPED_SURFACE_CLOSURE_OCTAHEDRON_DUALITY`

Precommit sealed UTC: `2026-07-12T03:12:56Z`

## Firewall

No SAM Language, v0.3 generalization, prospective holdout, forecast gate, or language-contract files were opened or used as scientific sources for this CR. The active source chain was restricted to the campaign prompt, the preflight artifact, named prior scientific CRs, named G-test outputs, and Volume I/Section 4 context.

Metadata frozen before runner:

```text
scientific_result_status = PASS
prospective_record_class = SCIENTIFIC_TEST
language_or_meta_language_test = false
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

## Source Hierarchy

The current controlling primitive base is taken from CR258:

```text
alpha_H = 2
D = 3
S = alpha_H^D = 8
```

The new CR therefore treats the canonical mathematical object as:

```text
S_state = h^D
```

with `h = alpha_H = 2`, and then tests two independent realizations:

```text
S_cross = 2^D
S_split = R^2 / Theta
```

where:

```text
R = h^2 D
Theta = h D^2
```

This avoids circularity: `S` is not used as an input to prove itself. The CR238 `{F,S}` foundational-spine wording is preserved in the occurrence register as sealed historical language, but CR258 is later and controls the current primitive-base claim.

## Occurrence Findings

The source register identifies these active roles:

1. `BinaryClosureStateMultiplicity` - CR114, G219B, G305, G306, G307, Volume I horizon-count passages.
2. `CrossPolytopeFacetCount` - not found as an earlier active SAM source claim; introduced here as the mathematical/geometric realization to be tested.
3. `ReleaseShareMultiplicity` - CR114, CR233, CR238, CR252, Volume I, and Section 4 ledger/readout passages.
4. `Split atom` / `surface` / `row-support surface` wording - retained as aliases or scoped readouts, not treated as arbitrary-boundary mathematics.

No source found in the active chain proves that literal physical substrate atoms are octahedra. The octahedron is therefore only a candidate realization unless the runner's mathematical subtest is later joined to an independent physical-ontology source.

## Preserved Conflicts

### CR238 versus CR258 primitive direction

CR238 says the older typed spine has foundational atoms `{F,S}` and derives `D = 3` from `S + 1`. CR258 later seals the minimal sufficient primitive base `(alpha_H, D)` and derives `S = alpha_H^D = 8`. CR117 does not overwrite CR238. It records CR238 as:

```text
ACTIVE_AS_SEALED_HISTORY_SUPERSEDED_FOR_PRIMITIVE_BASE
```

and uses CR258 for the precommitted hierarchy.

### Surface language

CR114 explicitly separates the `1/8` carrier fraction from the `D^2/R` observed-surface debit. Volume I uses row-support surface language for tensor/retained shares. CR117 therefore rejects:

```text
2^3 counts every arbitrary separating surface.
```

The valid scoped statement is:

```text
Three binary directions produce eight joint closure states.
Under cube-octahedron duality, those eight states correspond to the eight triangular octahedron faces.
```

## Source-Chain Conclusion

The source audit does not force STOP 1. The apparent ontology conflict is controlled by CR258's later primitive audit and preserved as historical CR238 wording. The runner may proceed after precommit with the hierarchy:

```text
primitive inputs: h = 2, D = 3
independent constructions: h^D, 2^D, R = h^2 D, Theta = h D^2, R^2/Theta
typed equality claim: S_state = S_cross = S_split = 8
physical ontology: candidate realization only
```
