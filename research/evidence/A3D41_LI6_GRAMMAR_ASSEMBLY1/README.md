# Li-6 construction grammar, retained circulation and hidden support

The Li-6 trial selects two of five motif assemblies. Each three-owner
circulation assembly narrows the previous 256 contact histories to 64;
the hidden-nine depth-loop response selects the same sixteen histories in
both. That set is unchanged across six center placements and all 128 rho
settings. **The test result suggests strong contact with the concept.**

Scope: finite isotope-specific grammar assembly, retained circulation
distinction, and exact candidate source-action selection. Direction: Sean
Brady. Technical mapping, implementation and derivation: Codex.

The eight support tensors remain ingredients. The catalog's one-body routes,
two-owner writes, three-owner constructions and carrier context determine
how those ingredients can be assembled on this Li-6 geometry. The tested
circulation response adds information beyond the net current at each object.

## What was constructed

The six one-body addresses keep their partition, depth, route and conjugation.
The existing center inventory remains one hidden nine, one road, one color
owner and one weak vector. The graph has nine relations, four core triangles
and one new depth square. A motif cover assigns each relation once: either
nine pair motifs, or one three-owner motif and six remaining pair motifs.
There are five covers. The separated mask removes the two depth joins.

The complete 321-row catalog is retained and typed in the source manifest and
geometry. The candidate constituent-partition projection selects pair row
QP093A-0235 and triad row QP093A-0115. Endpoint species, source role and depth
remain separate fields. Unused scalar and rejected-control rows do not become
isotope constituents. The full source selection and fixed candidate operators
are in [TECHNICAL_MAP.md](TECHNICAL_MAP.md).

## Exact result

Connected native-direction results using catalog observed-channel coefficients:

| Motif cover | Three-owner objects | Minimum without hidden-loop response | Histories | Minimum with hidden-loop response | Histories |
|---|---|---:|---:|---:|---:|
| COVER_00 | Pair motifs only | 86 | 256 | 1385/16 | 16 |
| COVER_01 | P00, N00, P01 | 177/2 | 64 | 363/4 | 64 |
| COVER_02 | P00, N00, N01 | 177/2 | 64 | 363/4 | 64 |
| COVER_03 | P00, P01, N01 | 91/2 | 64 | **737/16** | **16** |
| COVER_04 | N00, P01, N01 | 91/2 | 64 | **737/16** | **16** |

Each favored cover uses one triad and six pair motifs, while retaining the
center support inventory. Both favored covers attain `737/16 = 46.0625` in
candidate source-action units. The native channel selects the same two covers
and same sixteen histories at `969/16`. All ties are retained. The hidden
response refines the histories; the circulation triad selects the motif covers.

The endpoint-only triad comparison favors the pair-only cover. Switching to
the retained circulation changes that assembly preference. The site-incidence
rank is five; cycle rank is four; together they recover all nine edge currents.
An explicit same-site-current/different-circulation witness is retained.
The exact explanation of the sixteen states is in [DERIVATION.md](DERIVATION.md).

The calculation retains 245,760 minimum cases and 119 distinct minimizing
sets, across both direction maps, four reference masks, two source channels,
two triad receivers, five covers, hidden response on/off, six placements and
128 rho settings. Every native/phase-erased matched case has a different
minimum set. All source addresses remain recoverable through the inverse
maps and packed state sets. Separated-to-connected differences are retained
exactly in the same arrays and [REFERENCE_EXAMPLES.json](REFERENCE_EXAMPLES.json).

## Hardware and installation

The actual installed CE run evaluates **5,563,227 new primitive response
values** in **1.645563 seconds**. H14F uses fourteen direct-form workers;
Ryzen uses sixteen workers with independent expansions; the actual Radeon
780M contracts the exact integer features. Every value agrees across all
three calculations. Calibration compares workgroups 64 and 128; 128 is used
for both full batches. T500 stores the operands and results with independent
readback. The completed phase census is reused.

The two batches contain 5,143 center feature rows and 41,245 grammar feature
rows. Their inverse maps cover 2,097,152 state/reference rows. Factoring the
batches avoids materializing their large Cartesian product. The exact minimum
analysis takes 8.437689 seconds. All **216 result checks** pass, including
200 comparisons with an unfiltered exact integer calculation. An additional
**13 installation checks** pass, including 64 readout points checked against
the hardware results, CLI/Python agreement, and stale or malformed plan
rejection. The sixteen-state analytic derivation is also checked directly.

The current Li-6 head is
[`CURRENT_REVISION/domains/ATOM3D/LI6_CURRENT.json`](../../../CURRENT_REVISION/domains/ATOM3D/LI6_CURRENT.json).
From the repository root:

```sh
./CE-run --domain ATOM3D --operation LI6_GRAMMAR \
  --payload CURRENT_REVISION/domains/ATOM3D/li6_grammar_source/FULL_PLAN.json
./CE-run --domain ATOM3D --operation LI6_GRAMMAR_READOUT \
  --payload CURRENT_REVISION/domains/ATOM3D/li6_grammar_source/READOUT_EXAMPLE_PLAN.json
```

`READOUT_COVER04_PLAN.json` addresses the other tied cover. Both examples use
state 14336; they are source readouts. Python consumers use
`CURRENT_REVISION.domains.ATOM3D.li6_grammar.build_readout_plan` and `readout`.
The head records both covers and all sixteen histories. Earlier Li-6 stages
are explicitly named completed operations. The ordinary A3D41 contact default
continues to use its installed R2 packet.

The initial sandbox-denied calibration attempt is preserved under
`calibration_runs/`; approved remote calibration and full execution pass.
[CONTROL_CLARIFICATION.md](CONTROL_CLARIFICATION.md) records the inherited
TMR1 coordinate-covariance check separately from new scalar circulation
rotation invariance. No source operators were changed in that clarification.

## Continuation and evidence

The useful next route is to carry the signed site **and cycle** coordinates
into the physical tensor readouts on this sixteen-history family. It retains
internal distinctions that endpoint currents alone erase and reduces the
active history set sixteenfold. Two motif covers and six center placements
remain; spin, magnetic and quadrupole operators can act on that explicit
family. Physical coefficients and the MeV conversion remain unassigned.
The source value 46.0625 is not a measured binding energy. H000971's tested
unit source-to-MeV transfer retains its recorded falsification.

- [Exact result](RESULT.json), [result checks](VALIDATION.json),
  [installation checks](INSTALLATION_CHECKS.json), [hardware receipt](FULL_CLI.json)
- [Source manifest](SOURCE_MANIFEST.json), [geometry](GEOMETRY.json),
  [contract](CONTRACT.json), [minimum metadata](MINIMUM_METADATA.json)
- [Exact selected states](SELECTION_DERIVATION.json),
  [current readout](READOUT_CLI.json), [circulation witness](CIRCULATION_WITNESS.json)
- Final installation, T500 custody and completion are recorded in
  `FINAL_CHECKS.json`, `CUSTODY_RECEIPT.json` and `COMPLETION.json`.
