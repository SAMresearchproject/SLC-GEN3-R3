# SAM Prospective Foundational CR
## S = 8 Typed Surface Closure, Binary-State Geometry, and Cube–Octahedron Duality
### GPT-5.5 High / Extra High Scientific Campaign

**Recommended model:** GPT-5.5 Extra High  
**Working root:** `C:\VS\The_Courtroom`  
**Suggested scientific branch:** `14_FOUNDATIONAL_TESTS`  
**Suggested trailer:** `S8_TYPED_SURFACE_CLOSURE_OCTAHEDRON_DUALITY`

This is one new foundational scientific CR.

It is not a SAM Language task.  
It is not a documentation-only harmonization.  
It is not permission to rewrite prior CRs.

Its job is to resolve the overloaded meanings of \(S=8\) by creating one typed, source-audited structural theorem.

---

# 1. The Problem

Across the repository, \(S=8\) has been described as some combination of:

```text
binary state count
binary face-state count
surface closure
release-share split
1/8 denominator
carrier multiplicity
bigrade atom
substrate surface
```

Several of these can be compatible, but they are not automatically identical definitions.

The new CR must distinguish:

1. the **canonical mathematical object**;
2. its **geometric realization**;
3. its **ledger/readout consequence**;
4. historical aliases that are compatible but imprecise;
5. statements that are too broad and must be rejected.

---

# 2. Conceptual Statement in Plain Language

SAM begins with:

```text
h = 2   the arity of distinction
D = 3   the number of spatial directions
```

Three independent binary directions produce:

\[
S_{\mathrm{state}} = h^D = 2^3 = 8
\]

joint states.

These are the eight sign combinations:

```text
(+,+,+)  (+,+,-)  (+,-,+)  (+,-,-)
(-,+,+)  (-,+,-)  (-,-,+)  (-,-,-)
```

They may also be written as the eight vertices of a cube.

The dual 3D shape is the octahedron. It has:

```text
6 vertices
12 edges
8 triangular faces
```

Each octahedral face lies in one sign octant and has an outward normal pointing toward one cube vertex. Therefore the eight binary sign states have an exact one-to-one correspondence with the eight octahedral faces.

This is the precise statement.

Do **not** claim:

> Every 3D binary classification problem has exactly eight possible separating surfaces.

That is not generally true.

The valid claim is:

> Three binary directions produce eight joint closure states. Under the cube–octahedron dual realization, those eight states correspond exactly to the eight triangular boundary faces of the octahedron.

---

# 3. Proposed Typed Semantics

The CR must keep the following objects separate until their equality is proved.

## 3.1 Binary closure-state multiplicity

\[
S_{\mathrm{state}} = h^D.
\]

At \(h=2,\ D=3\):

\[
S_{\mathrm{state}}=8.
\]

Type:

```text
BinaryClosureStateMultiplicity
```

## 3.2 Octahedral surface-face count

For the \(D\)-dimensional cross-polytope, the number of facets is:

\[
S_{\mathrm{cross}}=2^D.
\]

At \(D=3\), the cross-polytope is the regular octahedron:

\[
S_{\mathrm{oct}}=8.
\]

Type:

```text
CrossPolytopeFacetCount
```

## 3.3 Release-share multiplicity

Using the independently sourced SAM quantities:

\[
R=h^2D,
\qquad
\Theta=hD^2,
\]

define:

\[
S_{\mathrm{split}}
=
\frac{R^2}{\Theta}.
\]

At \(h=2,\ D=3\):

\[
S_{\mathrm{split}}
=
\frac{144}{18}
=
8.
\]

Type:

```text
ReleaseShareMultiplicity
```

This yields the carrier share:

\[
f_\Theta=\frac{1}{S_{\mathrm{split}}}=\frac18.
\]

## 3.4 Canonical surface object

The CR may promote a canonical typed \(S\) only if it proves:

\[
S_{\mathrm{state}}
=
S_{\mathrm{cross}}
=
S_{\mathrm{split}}
=
8
\]

from independently sourced constructions.

Recommended canonical type:

```text
S8SurfaceClosureMultiplicity
```

Recommended interpretation:

> The eight-state binary closure multiplicity, realized geometrically as the eight faces of the 3D octahedral boundary and read in the ledger as the eight-way release-share partition.

---

# 4. Cube–Octahedron Structural Closure

At \(D=3,\ h=2\), the octahedron has:

\[
V_{\mathrm{oct}}=2D=6=hD,
\]

\[
E_{\mathrm{oct}}=2D(D-1)=12=R,
\]

\[
F_{\mathrm{oct}}=2^D=8=S.
\]

Therefore:

\[
(V,E,F)_{\mathrm{oct}}
=
(hD,R,S)
=
(6,12,8).
\]

Euler closure gives:

\[
V-E+F
=
6-12+8
=
2
=
h.
\]

The dual cube has:

\[
V_{\mathrm{cube}}=2^D=8=S,
\]

\[
E_{\mathrm{cube}}=D2^{D-1}=12=R,
\]

\[
F_{\mathrm{cube}}=2D=6=hD.
\]

Thus:

\[
(V,E,F)_{\mathrm{cube}}
=
(S,R,hD)
=
(8,12,6).
\]

The duality exchanges:

\[
6 \longleftrightarrow 8
\]

while preserving:

\[
12.
\]

The CR must prove this as a combinatorial duality, not merely display matching numbers.

---

# 5. Three-Dimensional Uniqueness Tests

The CR must test whether the role alignment is special to \(D=3\).

## 5.1 Octahedral-edge/radix equality

For a \(D\)-cross-polytope:

\[
E_{\mathrm{cross}}=2D(D-1).
\]

SAM radix:

\[
R=h^2D=4D.
\]

Require:

\[
2D(D-1)=4D.
\]

For positive \(D\):

\[
D=3
\]

is the unique nondegenerate solution.

## 5.2 Cube-edge/radix equality

For a \(D\)-cube:

\[
E_{\mathrm{cube}}=D2^{D-1}.
\]

Require:

\[
D2^{D-1}=4D.
\]

For positive \(D\):

\[
D=3
\]

is the unique solution.

## 5.3 State/split equality

Require:

\[
h^D=\frac{R^2}{\Theta}.
\]

With:

\[
R=h^2D,
\qquad
\Theta=hD^2,
\]

the right side reduces to:

\[
\frac{R^2}{\Theta}=h^3.
\]

Therefore:

\[
h^D=h^3.
\]

At \(h=2\), the unique positive integer solution is:

\[
D=3.
\]

This shows that the binary state multiplicity and the release-share multiplicity coincide specifically at the canonical dimensional readout.

---

# 6. Structural Rigidity Subtest

The user’s geometric claim must be scoped precisely.

Do not claim that an octahedron is universally “stronger” than a cube under every material, wall thickness, load, and manufacturing method.

Test this narrower structural statement:

> As an equal-edge, pin-jointed 3D skeletal framework, the octahedron is internally triangulated and infinitesimally rigid, while the unbraced cube skeleton is underconstrained and permits shear modes.

## 6.1 Octahedron

```text
vertices = 6
edges = 12
3V - 6 = 12
```

The octahedron satisfies the Maxwell necessary count exactly.

Compute the generic 3D rigidity-matrix rank and require:

\[
\operatorname{rank}(R_{\mathrm{oct}})
=
3V-6
=
12.
\]

## 6.2 Cube

```text
vertices = 8
edges = 12
3V - 6 = 18
```

The unbraced cube has too few bars for generic rigidity.

Require:

\[
\operatorname{rank}(R_{\mathrm{cube}})<18.
\]

This supports:

```text
octahedron = triangulated rigid carrier framework
cube        = dual container framework requiring additional bracing
```

only as a candidate SAM geometric interpretation.

It does not prove that physical substrate atoms are literally macroscopic wireframe polyhedra.

---

# 7. Mandatory Source Audit

Before writing the precommit, inspect the active scientific source chain for every prior \(S=8\) role.

At minimum:

```text
CR114_BINARY_FACE_STATE_SPLIT_THEOREM
CR233_TENSOR_SUBSTRATE_ROLE_SEPARATION
CR238_SUBSTRATE_SPINE_COMPACTION
G219B corrected chi derivation
G305 direction-allocation theorem
CR252 particle-catalog spine references to S=8
Volume I partition-algebra and A-kernel glossary
any earlier G test explicitly defining S
```

Create:

```text
CRxxx_S8_SOURCE_OCCURRENCE_REGISTER.csv
```

Required columns:

```text
source_path
source_hash
sealed_or_unsealed
date
exact_phrase
formula
claimed_role
provisional_type
active_or_superseded
compatible_with_new_typing
conflict_reason
```

The audit must identify whether each occurrence treats \(S=8\) as:

```text
DEFINITION
DERIVED_IDENTITY
GEOMETRIC_REALIZATION
LEDGER_READOUT
ALIAS
UNSUPPORTED_INTERPRETATION
SUPERSEDED_LANGUAGE
```

Do not erase historical wording.

---

# 8. Source Hierarchy

The new CR must not create circularity by defining \(S\) simultaneously from every identity.

Recommended hierarchy:

## Level 1 — Primitive inputs

```text
h = 2
D = 3
```

or, if the active source chain treats \(D\) as a readout, use its sealed controlling source rather than silently changing the ontology.

## Level 2 — Independent constructions

```text
binary state count       h^D
cross-polytope facets    2^D
radix                    h^2 D
tensor bridge            h D^2
split multiplicity       R^2 / Theta
```

## Level 3 — Proven equality at the canonical point

```text
h^D = 2^D = R^2/Theta = 8
```

## Level 4 — Typed physical interpretation

```text
binary closure states
octahedral boundary faces
release-share multiplicity
```

The CR must state which item is the canonical definition and which are independent realizations/readouts.

If the source record cannot support one canonical direction without choosing between incompatible ontologies, return a boundary and present the exact alternatives.

---

# 9. Precommitted Predictions

At minimum, the CR must precommit:

## P1 — Binary state count

\[
|H_D|=|\{0,1\}^D|=2^D=8.
\]

## P2 — No “arbitrary boundary surface” overclaim

The runner must reject the claim that \(2^D\) counts all possible separating hyperplanes or arbitrary classification boundaries.

## P3 — Octahedron combinatorics

\[
(V,E,F)=(6,12,8).
\]

## P4 — Cube combinatorics

\[
(V,E,F)=(8,12,6).
\]

## P5 — Duality

The cube and octahedron exchange vertices and faces and preserve edges.

## P6 — Binary-state/face bijection

Construct all eight sign states and all eight octahedral triangular faces.

Map each face to the sign pattern of its outward normal.

Require a bijection:

```text
8 states
8 faces
no duplicate state
no duplicate face
complete coverage
```

## P7 — SAM atom alignment

\[
V_{\mathrm{oct}}=hD=6,
\]

\[
E_{\mathrm{oct}}=R=12,
\]

\[
F_{\mathrm{oct}}=S=8.
\]

## P8 — Euler closure

\[
V-E+F=h.
\]

## P9 — Release-share identity

\[
S_{\mathrm{split}}=R^2/\Theta=8.
\]

## P10 — Carrier fraction

\[
f_\Theta=1/S=1/8.
\]

## P11 — State/split equality uniquely selects \(D=3\)

Scan positive integer \(D\) over a precommitted range and require unique equality.

## P12 — Edge/radix equality uniquely selects \(D=3\)

Run both cube and cross-polytope edge tests.

## P13 — Octahedral skeletal rigidity

The generic rigidity-matrix rank reaches \(3V-6\).

## P14 — Cube skeletal flexibility

The unbraced cube fails the generic rigidity requirement.

## P15 — Repository role reconciliation

Every active \(S=8\) occurrence is assigned a nonconflicting type or retained as an explicit unresolved conflict.

---

# 10. Wrong Controls

## WC1 — Ternary directions

Use:

\[
3^D=27.
\]

Expected: breaks the binary-state and octahedral-face correspondence.

## WC2 — Signed axes mistaken for surface

Use:

\[
2D=6
\]

as \(S\).

Expected: identifies octahedron vertices/cube faces, not binary state multiplicity.

## WC3 — Cube faces claimed as eight

Claim the cube has eight faces.

Expected: rejected; it has six faces and eight vertices.

## WC4 — Octahedron vertices claimed as eight

Expected: rejected; it has six vertices and eight faces.

## WC5 — Arbitrary hyperplane count

Interpret \(2^D\) as the number of all linear decision boundaries.

Expected: rejected as mathematically false/unbounded.

## WC6 — One-quarter split

Use four states and \(1/4\).

Expected: breaks \(R^2/\Theta=8\).

## WC7 — Sixteen-state split

Use \(2^{D+1}=16\).

Expected: breaks \(\Theta=18\) and the dual geometry.

## WC8 — D = 4

Expected:

```text
binary states = 16
cross-polytope facets = 16
cross-polytope edges = 24
radix = 16
edge/radix role alignment fails
state/split equality fails
```

## WC9 — Unbraced cube called rigid

Expected: rejected by edge count and rigidity-matrix rank.

## WC10 — Circular definition

Set \(S=8\) as an input and then claim every equality independently derives \(S\).

Expected: provenance audit flags circularity.

## WC11 — Historical role overwrite

Replace all prior role labels with the new canonical phrase.

Expected: rejected; append-only role typing is required.

---

# 11. Permitted Verdicts

Return exactly one primary verdict:

```text
PASS_S8_TYPED_SURFACE_CLOSURE_UNIFICATION

BOUNDARY_S8_CANONICAL_DEFINITION_SOURCE_CONFLICT

BOUNDARY_OCTAHEDRON_PHYSICAL_ONTOLOGY_UNPROVEN

FAIL_S8_STRUCTURAL_IDENTITIES

INVALID_S8_SOURCE_CHAIN

INVALID_FIREWALL
```

A PASS may include the secondary scope note:

```text
MATHEMATICAL_AND_COMBINATORIAL_UNIFICATION_PASS
PHYSICAL_OCTAHEDRON_ONTOLOGY_REMAINS_CANDIDATE
```

That is likely the expected honest result.

---

# 12. Required Outputs

Create one new CR folder containing:

```text
CRxxx_SOURCE_AUDIT.md
CRxxx_S8_SOURCE_OCCURRENCE_REGISTER.csv
CRxxx_SOURCE_MANIFEST.json
CRxxx_ASSUMPTION_REGISTER.json
CRxxx_PREFLIGHT.md
CRxxx_PRECOMMIT.md
CRxxx_runner.py
CRxxx_result.md
CRxxx_summary.json
CRxxx_provenance.json
CRxxx_typed_S8_contract.json
CRxxx_binary_state_face_bijection.csv
CRxxx_cube_octahedron_counts.csv
CRxxx_dimension_uniqueness_scan.csv
CRxxx_rigidity_results.json
CRxxx_wrong_controls.csv
CRxxx_VALIDATION.md
COMMAND_LOG.txt
OPENED_FILE_MANIFEST.json
HASHES.txt
```

## Typed contract minimum schema

```json
{
  "canonical_symbol": "S",
  "canonical_value": 8,
  "canonical_type": "S8SurfaceClosureMultiplicity",
  "binary_state_type": "BinaryClosureStateMultiplicity",
  "geometric_type": "CrossPolytopeFacetCount",
  "ledger_type": "ReleaseShareMultiplicity",
  "equalities": [
    "S_state = h^D = 8",
    "S_cross = 2^D = 8",
    "S_split = R^2/Theta = 8"
  ],
  "not_claimed": [
    "number of arbitrary linear separating surfaces",
    "proof that physical substrate atoms are literally octahedra",
    "universal material-strength superiority over a cube"
  ],
  "physical_geometry_status": "CANDIDATE_REALIZATION"
}
```

---

# 13. Prospective Metadata

Include from the beginning:

```text
scientific_result_status = PASS | FAIL | BOUNDARY
sealed_utc = exact ISO-8601 UTC timestamp
prospective_record_class = "SCIENTIFIC_TEST"
language_or_meta_language_test = false
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

Because this CR is motivated partly by a release ambiguity, the prospective queue—not the research agent—must decide its holdout eligibility.

Do not make or argue the eligibility decision inside the CR.

---

# 14. Mandatory Firewall

```text
Do not inspect SAM_LANGUAGE_V0_3, its registered contracts,
candidate implementation, or expected language output while developing this CR.

Set:
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
prospective_record_class = "SCIENTIFIC_TEST"
language_or_meta_language_test = false

Record all four fields in the CR precommit, provenance, summary, and result
artifacts. If either SAM Language field becomes true, the CR remains
scientifically valid but is ineligible as a SAM Language v0.3 holdout.

This firewall is between new scientific work and the frozen executable
language, not between the new work and SAM itself. The research may still use
the full scientific repository, previous Courtroom records, conceptual volumes,
external mathematical references, and normal SAM methods.
```

Do not inspect paths matching:

```text
SAM_LANGUAGE*
*V0_3_GENERALIZATION*
*PROSPECTIVE_HOLDOUT*
*FORECAST_GATE*
*LANGUAGE_CONTRACT*
```

---

# 15. Stop Points

## STOP 1 — Source ontology

After the source audit, stop only if the active repository has incompatible foundational directions:

```text
S foundational, D derived
versus
D foundational, S derived
```

Present the two paths and recommend one without silently choosing.

## STOP 2 — Precommit

Do not implement until the canonical source hierarchy and typed meanings are frozen.

## STOP 3 — Runner

If the rigidity or geometric theorem requires a new unrecorded physical assumption, keep it as a scoped mathematical subtest.

## STOP 4 — Verdict

Do not upgrade mathematical duality into proof of literal physical substrate shape.

## STOP 5 — Validation

Stop after one validated CR. Do not modify SAM Language or run queue maintenance.

---

# 16. Copy-Paste Master Prompt

```text
Execute SAM_PROSPECTIVE_CR_S8_TYPED_SURFACE_CLOSURE_5_5_XHIGH.md exactly as written.

This is one new foundational scientific Courtroom campaign.

Use GPT-5.5 Extra High.

The goal is to resolve the overloaded meanings of S=8 through typed semantics,
not by overwriting historical wording.

Audit the active scientific source chain for every S=8 occurrence.

Keep separate until proven equal:

    S_state = h^D
    S_cross = number of cross-polytope facets
    S_split = R^2/Theta

At h=2 and D=3, test whether all equal 8.

Construct the exact bijection between the eight binary sign states and the
eight triangular faces of the octahedron.

Verify:

    octahedron (V,E,F) = (6,12,8) = (hD,R,S)
    cube       (V,E,F) = (8,12,6) = (S,R,hD)
    V-E+F = h = 2

Run the dimension-uniqueness tests and the scoped pin-jointed rigidity test.

Reject the claim that 2^3 counts every arbitrary separating surface.

Do not claim that the mathematical result proves literal physical octahedral
substrate atoms. Preserve that as a candidate realization unless the source
chain independently supports it.

Use the mandatory firewall.
Precommit before writing the runner.
Preserve source conflicts.
Record exact scientific_result_status and sealed_utc metadata.
Do not inspect or modify SAM Language.
Do not run queue maintenance.
Stop after one validated CR.
```
