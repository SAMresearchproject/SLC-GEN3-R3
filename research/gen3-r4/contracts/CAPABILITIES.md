# GEN3-R4 reusable native capabilities

Installed build: GEN3-SOURCEOPERATORS1-20260916. Global SLC and CE are
SLC-GEN3-R4 / SLC-GEN3-CEV1-R4. The extension uses a warm C++/GMP CPU consumer
owned by the current R4 runtime. Python provides orchestration and custody;
the native consumer performs the arithmetic, learning and inference.

## Calls

| Operation | Required payload | Result |
|---|---|---|
| GEN3_CAPABILITIES | `{}` | Operations, installed model source bindings and acquired models |
| GEN3_SIGNED_ENERGY | left/right exact vectors, a/b exact supports, source_binding | Exact signed parent energy, repayment, gain and gain features |
| GEN3_COMMON_MINIMA | states, left/right exact cost arrays, source_binding | Both complete minimum sets, their intersection, joint minimum and exact excess |
| GEN3_TREE_FIT | name, rows, source_binding | Native class-balanced CART, development-selected depth, readable rules; model saved in R4 |
| GEN3_TREE_PREDICT | name, rows, source_binding | Exact probabilities, decisions and all ranked tie groups |
| GEN3_TREE_EXPORT | name | Complete retained model record and content hash |
| GEN3_CONSTRUCTION_PLAN | family_ids, source_contract | Native original 32-feature construction and prediction with the acquired common-minimum model |

A learning row has `features` (integers), `label` (0/1), `split` (0 training,
1 development, 2 reserved test) and a source `witness`. Fit uses depth 0..3,
class-balanced exact Gini cost and development balanced accuracy, preserving
the shallower depth on a tie. Reserved test labels never enter fitting or
selection. A new fit requires a new model name; prior models remain available.
Prediction rows have `id` and integer `features`. Their source binding must
match the model's binding exactly. Exact probabilities remain rational strings.

Common-minimum inputs enumerate the entire supplied finite source roster once.
The result certifies that roster's minima/intersection, not an unstated larger
construction. Left/right supports in signed-energy calculations have their
explicit source meanings; the operation does not assign physical units.

## Domain adoption

ATOM3D supplies `ATOM3D_COMMON_MINIMA` and `ATOM3D_CONSTRUCTION_PLAN`.
Starbreaker supplies `SB_SIGNED_ENERGY` and `SB_RECEIVER_PLAN`. They use the
same global native capabilities and reject calls through the wrong domain.
The existing contact, signed decoder, J4 history and 45-policy interfaces remain.
Generic GEN3 operations remain available through the current CE domain routes.

```sh
./project start ATOM3D --objective "Use the installed acquired construction model"
```

Use the printed session path in the next command, and save this payload as
`construction.json`:

```json
{"family_ids":[0,1,7679,7680,1568135,4799999],"source_contract":"A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1"}
```

```sh
./project run SESSION --operation ATOM3D_CONSTRUCTION_PLAN --payload construction.json --purpose "Rank the supplied original construction families, retaining all ties"
```

`GEN3_CAPABILITIES` returns the exact source bindings for the installed
`A3D41_COMMON_MINIMUM` and `SB_POSITIVE_SIGNED_ENERGY_GAIN` models. These are
from the final captured R7.1 root's 20,344-byte model object. Its original
hash and source bindings are retained in MODELS.json. Inference is not a new
construction measurement; subsequent exact source computations provide outcomes.

## Persistence and migration

New models, source bindings and native computation origins share the ordinary
R4 authenticated checkpoint. The six existing core memories remain installed.
Only the explicitly recorded predecessor implementation binding is eligible
for automatic additive checkpoint migration. Its custody authentication and
complete object closure must verify. Reopening preserves its state, accounts,
knowledge and original immutable roots; the next checkpoint selects the new
implementation binding and records its predecessor. Unrecognized bindings
continue to require semantic import. Start a fresh project session after the
generation change; prior session manifests remain preserved.

This installation imports reusable capability code and two acquired domain
models. RH campaign state, pod environments and bulk training/run histories
stay in backup custody. Existing owner pauses remain in effect.

## Build provenance

The source-bound worker retains R7.1's exact signed-energy routine and native
CART fit/predict/rule routines. Its standalone CPU entry point generalizes the
complete common-minimum calculation to supplied paired finite cost tables and
uses the original construction feature mapping. The package includes source,
source identities and the compiled x86-64 CPU worker. The build uses G++ C++17,
GMP 6.3 development libraries and nlohmann-json 3.11.3 headers; qualification
and installation receipts are under GEN3_R3_CAPABILITY_UPGRADE1.

## Operator logarithms

The installed native consumer also supplies `GEN3_OPERATOR_OBSTRUCTION`, `GEN3_COMMUTING_LOG` and `GEN3_OPERATOR_EXPORT`. [Exact schemas and examples](OPERATOR_LOG.md). Operator records retain source histories and share the authenticated R4 checkpoint.

## Certified spectral logarithms — R4

Exact spectral admission, rational log enclosures, spectral profiles, refinement, signed transport logs and retained export run in the common native consumer. [Contracts](CERTIFIED_LOG.md).

## Source operators and exchange — R4

Eight exact source operations add rational/quadratic words, closure, pair relations, recurrence, creation, exchange, terminal action and checkpoint export in the common native consumer. [Contracts](SOURCE_OPERATORS.md).
