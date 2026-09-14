[SAM](../../README.md) · [Volume II](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Typed Matter Surfaces and Row Grammar

## ATOM3D: contact, grammar and signed decoding — 14 September 2026

A3D41-T18-CONTACT-R2 uses SLC-GEN3-R3; A3D41-RXT-R3 supplies the joint native successor. Ordinary contact retains four minima and 113,664 agreeing readouts. Li-6 grammar retains both selected covers and every tie across six placements and 128 rho settings. Two Write responses and a signed N01 bit recover all 192 tested configurations. The test result suggests strong contact with the concept. The separate distinct-selector and physical-coefficient/MeV work remain owner-paused.

[Current derivations, code and results](../../../research/atom3d/README.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Opening question

> When SAM reports 35, 80, 100, 126, 139 or 321 rows, what exactly has been
> counted, and how can a row move between typed surfaces without its address,
> role or evidence being silently rewritten?

## Conceptual abstract

A row count is never a complete particle statement. SAM maintains several
finite surfaces because each answers a different executable question: the
compact base mass chain, the full candidate catalog, the admitted matter
inventory, the lift-channel table, the stable tensor-compatible surface, the
periodic surface and the computation basis. Their counts may coincide or
overlap, but their row predicates and meanings do not.

The row itself is also typed. A finite identity is the combination of a source
table, its schema, a typed address and the operator acting on it. Partition,
charge, sign, depth, bin and conventional label are fields inside that
contract; no one field reconstructs the row. Known names and measured masses
arrive downstream as reveals or comparators.

The 80-row surface provides the clearest worked example. CR253 begins with the
larger catalog and applies a promoter. It returns exactly 80 rows, split as
\(48+32\) matter/antimatter and \(64+16\) charged/neutral. Two planned binary
controls are redundant because the bin and depth filters already subsume
them. That preserved boundary does not change the 80 rows; it simplifies the
minimal sufficient promoter. CR280 then corrects the semantic label from an
unqualified physical-particle reading to `StructurallyStableMatterRow` on a
`TensorCompatibleStableMatterSurface`.

## 1. A row is a typed record

### 1.1 Minimal identity contract

Represent a source row schematically as

\[
r=(\mathsf{source},\mathsf{schema},\mathsf{id},p,q,s,d,h_T,I_T,
\mathsf{bin},\mathsf{operator},\ldots).
\]

Not every schema uses every displayed field, but row identity requires at
least the first four layers:

\[
\boxed{
\text{row identity}
=\text{source table}
+\text{row schema}
+\text{typed address}
+\text{acting operator}}
\]

The fields then carry schema-specific meaning:

| Field | Typical role | Boundary |
|---|---|---|
| \(p\) | partition address | A scalar partition does not define a row. |
| \(q\) | charge or role coordinate | Its sign and magnitude are schema-bound. |
| \(s\) | sign lane | Not an identity independent of \((p,d,\mathsf{operator})\). |
| \(d\) | closure depth | Not the spatial support dimension unless explicitly stated. |
| \(h_T\) | tensor/bigrade depth field | Used by a promoter only in its declared schema. |
| \(I_T\) | incidence or obstruction field | Can be redundant after upstream filters. |
| bin | catalog classification | Load-bearing for some projections, not a universal ontology. |
| operator | row law or transform | A non-row operator acts on rows without joining the count. |
| conventional label | downstream reveal | Never a native construction input. |
| measured mass | downstream comparator | Never substituted for \(q_A\) or debit. |

### 1.2 Construction before reveal

The permitted order is

```text
native source row
  -> schema parse
  -> typed address
  -> native operator
  -> gate/promoter/filter
  -> reversible SAM identity
  -> authorized conventional label or measured comparator, if available.
```

Reversing the last arrow contaminates the construction: a familiar label or
mass value could then select the row it was supposed to test. LC04 preserves
the correct direction across the 35-row chain, 321-row vault and generator
suite.

## 2. What a surface is

### 2.1 Surface as a typed projection

Let \(\mathcal C\) be a source catalog. A finite surface is a typed projection

\[
\mathcal S_P=\{r\in\mathcal C:P(r)=1\},
\]

where \(P\) is the source-defined predicate and the result retains its own
schema. Two surfaces can use the same catalog while asking different
questions:

\[
P_1\ne P_2
\quad\Longrightarrow\quad
\mathcal S_{P_1}\text{ and }\mathcal S_{P_2}
\text{ are differently typed even if }|\mathcal S_{P_1}|=|\mathcal S_{P_2}|.
\]

Likewise, one surface may be a subset or projection of another without
replacing it.

### 2.2 The census firewall

| Surface | Rows | Executable question | What the count does not mean |
|---|---:|---|---|
| connector alphabet | 8 values | Which diagonal partition values are admitted as connectors? | eight particles |
| base mass closure | 35 | Which compact base prediction-chain rows close? | the full catalog |
| lift table | 139, 138 evaluable | Which typed lift channel applies to each promoted/carrier row? | 139 matter particles |
| finite catalog | 321 | Which candidates, composites, carriers, supports and rejections occupy the full typed vault? | 321 experimentally identified particles |
| matter inventory | 126 | Which stable single and bound writes pass that inventory gate? | the 126-row periodic table |
| tensor-compatible surface | 80 | Which shallow structurally stable matter/antimatter rows pass the promoter? | 80 named observed particles |
| periodic surface | 126 | Which one-per-\(Z\) native element-family rows form the periodic table? | the 126-row matter inventory |
| computation basis | 100 | Which source grammar rows remain after executable pruning? | a new physical census |

The firewall has two directions. A larger count does not supersede a smaller
surface, and a later computational pruning does not edit a frozen physical
table.

## 3. The 321-row catalog lineage

### 3.1 Historical reveal

CR119 records three visible counts:

\[
321\ \text{particle-catalog rows},
\qquad
126\ \text{matter rows},
\qquad
126\ \text{periodic rows}.
\]

It also records 573 vault identity-assignment rows. These figures occupy
different schemas even inside one result. CR119's key boundaries are already
explicit: labels are reveal-only, Z119–Z126 remain frontier identities,
`QP093A-0088` is a null conjugate with no matter promotion, \(q_A\) is not
mass, and the tensor carrier is not a particle row.

### 3.2 Spine refresh and bit-identical custody

CR252 rebuilds the 321-row catalog from its source and compares it to the
frozen baseline:

\[
N_{\rm baseline}=321,
\qquad
N_{\rm regen}=321,
\]

with identical SHA-256

```text
3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6.
```

All 321 rows are classified as unchanged and present in both versions. The
schema-bin distribution is

| 321-schema bin | Rows |
|---|---:|
| stable matter | 63 |
| unstable resonance | 25 |
| antimatter conjugate | 42 |
| bound composite | 169 |
| carrier-only | 6 |
| hidden source support | 8 |
| rejected fake closure | 8 |

The census closes arithmetically:

\[
63+25+42+169+6+8+8=321.
\]

The labels belong to the 321-row schema. CR252 also records a broader
`matter_rows(v2)=286` predicate in its own table. That broad field is not
silently substituted for the 126-row LC06 inventory or for the 80-row
promoted surface; predicate and schema travel with every count.

### 3.3 Why the refresh is a correction rather than a new census

The historical CR119 reveal remains provenance. CR252 is the current catalog
spine because it certifies deterministic, bit-identical reconstruction, complete
classification and carrier non-promotion. The correction is authority and
typing, not a replacement of 321 by a new number.

## 4. The 126-row matter inventory

LC06 replays a different surface:

\[
126=63\ \text{stable single writes}+63\ \text{bound composites}.
\]

That table includes zero antimatter rows. It explicitly excludes carrier
promotion and preserves the null-conjugate boundary

\[
18-18=0\quad\Longrightarrow\quad M_{\rm obs}=q_A=0.
\]

The count 126 also appears as the retained capacity
\(M=7R^2/8\) and as the periodic-surface cardinality. The structural relation
is part of SAM, but each occurrence retains its type:

```text
126 retained capacity != 126 inventory rows != 126 periodic rows.
```

## 5. Row types, structural maps and count firewalls

### 5.1 Deriving the 80-row promoter

#### 5.1.1 Full pre-registered predicate

CR253 begins with a source catalog and a four-part promoter using:

- a permitted catalog bin;
- \(h_T\in\{0,1\}\);
- \(q\) in the bigrade alphabet; and
- \(I_T=0\).

Writing the conditions as \((B,H,Q,I)\), the planned predicate is

\[
P_{\rm full}(r)=B(r)\land H(r)\land Q(r)\land I(r).
\]

Its execution returns exactly

\[
80=48\ \text{matter}+32\ \text{antimatter},
\]

and independently

\[
80=64\ \text{charged}+16\ \text{neutral}.
\]

The finer decomposition is

\[
80=32\ \text{charged matter}
+16\ \text{neutral matter}
+32\ \text{charged antimatter}.
\]

Conjugate parity closes on 32/32 scoped pairs, all seven planned row classes
match, and no row remains unclassified.

#### 5.1.2 Control-driven minimization

The controls reveal which predicate components are load-bearing:

| Control | Resulting rows | Reading |
|---|---:|---|
| include bound composites in allowed bin | 116 | bin boundary is sensitive |
| allow \(h_T=2\) | 105 | shallow-depth boundary is sensitive |
| relax \(q\) to every integer 0–12 | 80 | no newly eligible rows after bin and \(h_T\) |
| allow \(I_T>0\) | 80 | incidence condition already implied on survivors |
| permute bins, 1000 trials | exact 80 in 0/1000 | real bin assignment is load-bearing; \(p<0.001\) |

The last two binary controls do not change the output because upstream filters
subsume them. Formally, on this fixed catalog,

\[
B\land H\Longrightarrow Q\land I.
\]

Therefore

\[
P_{\rm full}
=(B\land H\land Q\land I)
\equiv(B\land H)
=P_{\rm min}
\]

on the catalog domain. The minimal sufficient promoter is

\[
\boxed{
P_{80}(r)=
[\mathsf{bin}(r)\in\{\mathsf{stable\ matter},
\mathsf{antimatter\ conjugate}\}]
\land[h_T(r)\in\{0,1\}].}
\]

The source records a `BOUNDARY` verdict because the pre-registered tree
required all four binary controls to be individually sensitive. The content
of the surface remains exact; the preserved boundary is that the original
four filters were not independent.

#### 5.1.3 Semantic correction

An exact structural promoter does not establish that every output row is an
experimentally identified particle. CR280 installs the current type:

```text
TensorCompatibleStableMatterSurface
  row subtype: StructurallyStableMatterRow
  not equal to: ExperimentallyIdentifiedParticle.
```

It replays all 80 rows, preserves the \(48/32\) split and 32/32 conjugate
parity, retains CR253's `BOUNDARY`, and emits a conventional name only where a
source authorizes exact contact. Other rows receive deterministic reversible
SAM identifiers.

This is a semantic correction, not a roster change:

\[
\mathcal S_{80}^{\rm before}
=\mathcal S_{80}^{\rm after}
\quad\text{as row IDs},
\]

while

\[
\mathsf{type}_{\rm after}
=\mathsf{StructurallyStableMatterRow}
\]

removes an unsupported observed-particle reading.

### 5.2 Row-type controls and independent restarts

#### 5.2.1 QP034: support does not promote identity

QP034's strong support lanes yield no fixed-point promotions. The result is a
general row-grammar guard: a high support score, route fraction or matching
scalar is evidence within a lane, not a row identity constructor.

#### 5.2.2 QP093A: the bucket map organizes; it does not authorize stale prose

The QP093A artifact supplies the structural bucket map used by the catalog
lineage. A bucket assignment is a typed organizational field. It does not
authorize importing claims from an older `SAM_321` manuscript or relabeling a
candidate as a known particle.

#### 5.2.3 QP106: independent 80-row restart

QP106 loads 299 source rows and extracts 80 stable rows with zero carrier rows
in the set, zero unmatched antimatter partners and zero rule gaps. Its identity
counts recover the same matter/antimatter structure, including 16 matter rows
without mirrors—the two neutrino-like and fourteen neutral higher-partition
rows. The restart corroborates the surface while preserving its structural,
not experimentally named, type.

#### 5.2.4 LC04 and LC06: locked replay at two scales

LC04 replays 65/65 checks, 13/13 layers and 11/11 wrong controls across the
35-row base chain, CR119 vault and generator suite. It explicitly preserves
known labels and masses as reveal-only, \(q_A\) and debit as non-mass channels,
\(\Theta18\) as carrier and the generator laws as in-sample consistency unless
separately forward-blind.

LC06 independently replays the 126-row inventory. Together they show why one
successful replay cannot merge the base, full-catalog and matter-inventory
surfaces.

### 5.3 The lift and computation boundaries

#### 5.3.1 139-row lift table

The lift table contains 126 promoted rows plus 13 carrier/tensor rows. Of its
139 rows, 138 have a defined normalized lift \(Y=X/K\); the massless photon
road has \(K=X=0\), so \(Y\) is undefined rather than failed. This is a
channel table, not a 139-particle census. The full class-specific lift
derivations belong to the downstream lift document.

#### 5.3.2 N100 is a computation basis

The current executable basis has 100 rows after five \(p{:}9\) removals. That
selection is applied at the computation interface:

\[
\mathcal G_{100}=\Pi_{\rm executable}(\mathcal G_{\rm source}).
\]

It does not mutate any frozen source surface:

\[
\mathcal S_{35},\mathcal S_{80},\mathcal S_{126},
\mathcal S_{139},\mathcal S_{321}
\quad\text{remain unchanged}.
\]

The G1 compiler audit confirms 100/100 unique source keys and a 72-row exact
aggregate-incidence partial domain. It also finds zero source-authorized
elementwise mappings from N100 rows to the 81 semantic F81 sites. The contact
lane is therefore not executed, and the exact status remains
`PARTIAL_DOMAIN__ELEMENTWISE_F81_JOIN_OPEN`.

This is the correct open boundary: a compiler can preserve source types and
still lack one required join key.

## 6. Catalog and surface correction chain

The registered correction route is chronological and typed:

```text
CR119 historical reveal
  -> CR252 deterministic 321-row spine refresh
  -> CR253 exact 80-row projection with redundant-control boundary
  -> CR280 semantic correction to StructurallyStableMatterRow.
```

CR252 changes neither row count nor source content: its regenerated table is
bit-identical to the 321-row baseline. CR253 then asks a narrower projection
question and returns 80 rows; its two redundant binary controls simplify the
promoter but do not alter the roster. CR280 finally corrects the interpretation
of that frozen roster without renaming it as an observed-particle census.
Thus each correction changes exactly one layer—current custody, projection
logic, then semantic type—while preserving all predecessor artifacts.

## 7. Worked cross-surface examples

### 7.1 Carrier row

The \(\Theta18\) row participates in carrier and lift-support tables, but it is
excluded from the 126-row matter inventory and the 80-row promoted matter
surface. Its repeated appearance across source tables records a shared role,
not multiple particle identities.

### 7.2 Null-conjugate row

`QP093A-0088` exists in the full catalog and carries a native value, but its
debit leaves \(M_{\rm obs}=q_A=0\). It remains a boundary row rather than an
admitted matter row. Deleting it would make the catalog cleaner only by
erasing the reason the gate is typed.

### 7.3 One row, later projection

A structurally stable row may appear in the 321 catalog, survive the 80-row
promoter, and later be serialized into a computation basis. Those are three
records of one source lineage under three predicates. The later projection
does not retroactively turn the original catalog bin into a computation type.

## 8. Locked table and inventory replays

LC04 replays the 35-row base chain, the current 321-row export and the scoped
generator register with 65/65 checks and 13/13 replay layers passing; all
11 wrong controls reject. LC06 separately replays the 126-row inventory as
63 single plus 63 bound writes, with no carrier or antimatter promotion. These
are complementary retests. LC04 protects the grammar and reveal boundary;
LC06 protects matter admission and the null-conjugate witness. Neither replay
converts one surface into the other.

## 9. Established result and exact boundaries

The source chain establishes:

1. Row identity is source + schema + typed address + operator.
2. The 35-, 80-, 100-, 126-, 139- and 321-row surfaces answer different
   questions and cannot be treated as competing counts of one particle type.
3. CR252 deterministically preserves the current 321-row catalog and its
   seven exact schema-bin counts.
4. LC06 preserves a differently typed 126-row inventory of 63 single and 63
   bound writes.
5. CR253 preserves an exact 80-row structural surface and derives the minimal
   sufficient promoter from its controls.
6. CR280 types those rows as structurally stable tensor-compatible matter,
   not an observed-particle list.
7. N100 pruning leaves physical source tables unchanged, and the elementwise
   N100-to-F81 join remains open.

No project-wide result classification is assigned because the registered
evidence routes have `result_classification: null`. Source verdict/status
fields remain visible in the test index.

## 10. Deviations, wrong controls and corrections

| Deviation | Preserved evidence | Correction |
|---|---|---|
| “321 particles” becomes 321 experimentally named objects | CR119 says labels are reveal-only | Retain catalog bins and reversible native IDs. |
| Historical CR119 alone is treated as current catalog authority | CR252 rebuild is bit-identical and complete | Use CR252 for current census; preserve CR119 as lineage. |
| All planned promoter clauses are declared independently necessary | W3 and W4 return the same 80 | Reduce to bin + \(h_T\) on this catalog; preserve CR253 boundary. |
| Tensor compatibility becomes experimental existence | CR280 guards reject the inference | Use `StructurallyStableMatterRow`. |
| 126 inventory equals 126 periodic surface | LC06 defines 63+63 inventory | Carry separate schemas despite equal counts. |
| N100 deletions rewrite physical catalogs | G1 keeps source keys and source tables typed | Treat pruning as computation-only projection. |
| Missing F81 join is filled from geometry or outcome | G1 records no source-native elementwise key | Keep the elementwise compiler lane open. |

## 11. Related SAMA documents and forward handoff

`SAMA-D000025` supplies the connector/carrier/container distinctions that
prevent non-row infrastructure from entering a census. This chapter turns
that distinction into a reusable row and surface contract.

`SAMA-D000027` receives:

```text
current full catalog = 321 typed rows with seven exact bins
base mass chain       = 35 rows, a separate compact closure
labels/masses         = downstream reveals and comparators
generator output      != stability promotion
N100                  = computation projection, not census revision.
```

The next chapter can therefore develop the finite generator laws without
confusing a generated candidate, admitted matter row, carrier or known
particle.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| [`CR:CR119@09a`](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) | Historical 321/126/126 vault reveal | `CLEAN`; source verdict `PASS` | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL) |
| [`CR:CR252@09a`](../../tests/courtroom/09a-particle-mass-chain-cr252-particle-catalog-spine-refresh/README.md) | Current bit-identical 321-row correction | Source verdict `PASS` | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH) |
| [`CR:CR253@09a`](../../tests/courtroom/09a-particle-mass-chain-cr253-particle-promoter-80-row/README.md) | Exact 80-row promoter and control-derived minimization | `BOUNDARY`; core 80-row finding exact | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW) |
| [`CR:CR280@09a`](../../tests/courtroom/09a-particle-mass-chain-cr280-cr253-stable-matter-surface-semantic-clarification/README.md) | Semantic correction to structural matter rows | `PASS_CR253_SEMANTIC_CLARIFICATION` | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION) |
| [`QP:QP034`](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | Support-versus-identity boundary | `QP034_LANE_SUPPORT_PARTICLE_IDENTITY_SEPARATED` | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP034_PRIVATE_LANE_SUPPORT_VS_PARTICLE_IDENTITY_SEPARATOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| [`QP:QP093A`](../../tests/courtroom/workbench-misc/README.md) | Structural bucket map | Source artifact recorded | [result](../../courtroom/Workbench-misc/QP093A_321_ROW_STRUCTURAL_INTERPRETATION.md) | [folder](../../courtroom/Workbench-misc) |
| `QP:QP106@SAM-ARCHIVE` | Independent 80-row restart | Source artifact records 80 extracted, zero carriers and zero rule gaps | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/quantum_phase_QP_tests/qp106_80_row_matter_sector_restart/qp106_summary.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/quantum_phase_QP_tests/qp106_80_row_matter_sector_restart) |
| `G:G1@SAM-RESEARCH` | N100 serialization and open elementwise F81 join | `PARTIAL_DOMAIN__ELEMENTWISE_F81_JOIN_OPEN` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/2b45b6edf1fb80b70c0193f63e3d32dd218967d6/SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_H14F_EXACT_N100_PARTICLE_SPIN_G1_V1/G1_SOURCE_NATIVE_COMPILER_AUDIT.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/tree/2b45b6edf1fb80b70c0193f63e3d32dd218967d6/SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_H14F_EXACT_N100_PARTICLE_SPIN_G1_V1) |
| [`LC:LC04`](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | Locked 35/321/generator-table replay | `LC04_PASS_PARTICLE_MASS_CHAIN_TABLE_REPLAY_FROM_LOCKED_PRIMITIVE_STACK` | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY) |
| [`LC:LC06`](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | Locked 126-row inventory replay | `LC06_PASS_BARYON_AND_MATTER_INVENTORY_REPLAY_FROM_LOCKED_PRIMITIVE_STACK` | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000139-R001` | Typed particle-row identity contract. |
| `SAMA-C000140-R001` | Census firewall across finite surfaces. |
| `SAMA-C000141-R001` | Current 321-row catalog and exact bins. |
| `SAMA-C000142-R001` | 126-row 63+63 matter inventory. |
| `SAMA-C000143-R001` | Structural type and exact decomposition of the 80-row surface. |
| `SAMA-C000144-R001` | Downstream reveal boundary for labels and masses. |
| `SAMA-C000145-R001` | N100 pruning/physical-table firewall. |
| `SAMA-C000182-R001` | 80+1 cardinality boundary for the non-row closure address. |

## External references

No external bibliographic source is used directly. All counts, controls and
boundaries are routed through registered source artifacts.

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`QP:QP034`](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All package files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All package files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All package files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) | [All 107 files](../../tests/courtroom/12-quantum-computing-and-networking-source-artifacts/README.md) |
| [`QP:QP093A`](../../tests/courtroom/workbench-misc/README.md) | [All package files](../../tests/courtroom/workbench-misc/README.md) | [All package files](../../tests/courtroom/workbench-misc/README.md) | [All files](../../tests/courtroom/workbench-misc/README.md) | [All package files](../../tests/courtroom/workbench-misc/README.md) | [All 7 files](../../tests/courtroom/workbench-misc/README.md) |
| [`CR:CR119@09a`](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) | [All package files](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) | [CR119_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_runner.py) | [CR119_wrong_controls.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_wrong_controls.csv)<br>[CR119_wrong_controls.csv.sha256.txt](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/sha256_sidecars/CR119_wrong_controls.csv.sha256.txt) | [CR119_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_result.md)<br>[CR119_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_summary.json)<br>[CR119_result.md.sha256.txt](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/sha256_sidecars/CR119_result.md.sha256.txt)<br>[CR119_summary.json.sha256.txt](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/sha256_sidecars/CR119_summary.json.sha256.txt) | [All 36 files](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) |
| [`CR:CR252@09a`](../../tests/courtroom/09a-particle-mass-chain-cr252-particle-catalog-spine-refresh/README.md) | [CR252_PRECOMMIT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_PRECOMMIT.md)<br>[CR252_PRECOMMIT_AMENDMENT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_PRECOMMIT_AMENDMENT.md) | [CR252_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_runner.py) | [CR252_wrong_controls.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_wrong_controls.csv)<br>[CR252_wrong_controls_FIRSTRUN_FAIL_spec_error.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_wrong_controls_FIRSTRUN_FAIL_spec_error.csv) | [CR252_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_result.md)<br>[CR252_result_FIRSTRUN_FAIL_spec_error.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_result_FIRSTRUN_FAIL_spec_error.md)<br>[CR252_spine_input_audit.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_spine_input_audit.csv)<br>[CR252_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_summary.json)<br>[CR252_summary_FIRSTRUN_FAIL_spec_error.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_summary_FIRSTRUN_FAIL_spec_error.json) | [All 20 files](../../tests/courtroom/09a-particle-mass-chain-cr252-particle-catalog-spine-refresh/README.md) |
| [`CR:CR253@09a`](../../tests/courtroom/09a-particle-mass-chain-cr253-particle-promoter-80-row/README.md) | [CR253_PRECOMMIT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_PRECOMMIT.md) | [CR253_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_runner.py) | [CR253_wrong_controls.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_wrong_controls.csv) | [CR253_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_result.md)<br>[CR253_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_summary.json) | [All 8 files](../../tests/courtroom/09a-particle-mass-chain-cr253-particle-promoter-80-row/README.md) |
| [`CR:CR280@09a`](../../tests/courtroom/09a-particle-mass-chain-cr280-cr253-stable-matter-surface-semantic-clarification/README.md) | [CR280_PRECOMMIT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_PRECOMMIT.md)<br>[CR280_row_contract.schema.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_row_contract.schema.json) | [CR280_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_runner.py) | [CR280_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_runner.py)<br>[CR280_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_result.md)<br>[CR280_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_summary.json) | [CR280_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_result.md)<br>[CR280_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION/CR280_summary.json) | [All 9 files](../../tests/courtroom/09a-particle-mass-chain-cr280-cr253-stable-matter-surface-semantic-clarification/README.md) |
| [`LC:LC04`](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | [LC04_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_wrong_controls.csv) | [LC04_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_result.md)<br>[LC04_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_summary.json) | [All 9 files](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) |
| [`LC:LC06`](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) | [LC06_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_wrong_controls.csv) | [LC06_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md)<br>[LC06_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_summary.json) | [All 10 files](../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000026`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/TYPED_MATTER_SURFACES_AND_ROW_GRAMMAR.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol II | SAMA-D000026 | Particle Grammar | Typed Matter Surfaces, Row Classes and Count Firewalls |

| Document field | Value |
|---|---|
| Purpose | Present finite matter surfaces and row classes without collapsing their types into competing particle counts. |
| Prerequisite documents | `SAMA-D000025` |
| Used by | `SAMA-D000027`; generated from the document catalog |

</details>
