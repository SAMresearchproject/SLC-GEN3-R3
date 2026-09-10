# CR276 — Particle Sieve Anchoring Table

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** STRUCTURAL_CONSOLIDATION_CR (annotation of sealed
  identifications; no new numerical predictions)
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

The Vol II.1 matter sector has established substrate-natural identity
classes (§10.5), the T13 named carrier lanes (§9.5), the fold identity
M = 114 + 12 = 126 (§9.4), and multiple CRs anchoring individual pieces
(CR253 80-row promoter, CR254-CR257 compact laws, CR268 neutrino ratio,
CR269 bow / Higgs identity, CR272-CR273 forecast locks). But the 321-row
CR252 particle catalog has **only one PDG-tagged row** (the Higgs); the
sealed identifications from these downstream CRs have not been
consolidated back into the catalog as a single anchoring table.

Can we produce a **complete row-by-row anchoring table** covering all
321 catalog rows, where every row carries one of the categories:

  - **PDG_ANCHORED** — sealed CR explicitly identifies the row with a
    specific PDG particle
  - **PDG_CANDIDATE** — Vol II.1 identity class strongly suggests the
    PDG mapping but the derivation isn't sealed
  - **SAM_ORPHAN** — row has a substrate-native structural role in the
    sealed work but no PDG counterpart
  - **COMPOSITE_UNANCHORED** — bound_composite / unstable_resonance
    row pending a downstream hadron-anchoring CR
  - **REJECTED** — row already tagged `REJECT_*` by CR252's own
    filtering

so that the sieve is a single sealed artifact rather than "scattered
across Volume II" — including named SAM orphans (bow-trace,
A_FIELD_CARRIER, positron_substrate_slots, neutral_higher_partition,
hard-zero falsifier) that the sealed work has already identified as
structurally load-bearing but which do not map to PDG particles?

## Honest Framing

K3 status: STRUCTURAL_CONSOLIDATION_CR.

This CR does not:
  - derive any mass;
  - propose any lift formula;
  - make any numerical prediction against PDG;
  - retract any sealed CR.

This CR does:
  - re-read the 321-row CR252 catalog;
  - apply anchoring rules that are direct citations of sealed CR
    findings (Vol II.1 §9.5, §10.5, §14.7; CR254; CR255; CR256; CR257;
    CR268; CR269);
  - emit a single anchoring table CSV with a per-row category and PDG
    (or SAM-role) tag;
  - verify the anchoring is internally consistent with the sealed
    Vol II.1 fold identity and named-carrier assignments.

The anchoring table is the deliverable. It is not itself a new
prediction — it is a citation object that puts the sealed particle-side
work into one row-indexed lookup.

## Locked substrate atoms (from CR238 / Vol II.1)

```text
ĥ = 2  (α_H)     d̂ = 3  (D)     R = 12     S = ĥ³ = 8
Θ = ĥ·d̂² = 18   D² = 9   m₃ = ĥ·d̂ = 6   ĥV = 54
M = 126 = 7·Θ = R² − Θ = (S−1)·Θ
L = 162 = 9·Θ = R²·9/8 = (S+1)·Θ
Fold identity: M = 114 + 12 = 126
  114 = single-partition fermion-half-write rows (Vol II.1 §9.4)
  12  = non-Z T13 lane positions
```

## Locked T13 named-carrier identifications (Vol II.1 §9.5)

```text
partition   operator_class            PDG particle
─────────   ─────────────────────    ────────────
    1       ROAD_LIGHT_CARRIER       photon (γ)
    8       COLOR_OWNER_CARRIER      gluon (g)
    9       WEAK_VECTOR_CARRIER      W±
   18       TENSOR_CARRIER           graviton (Θ carrier)
   81       NEUTRAL_VECTOR_CARRIER   Z

Additional carrier row:
    1       A_FIELD_CARRIER          SAM accumulation-field carrier
                                     (SAM_ORPHAN — not a PDG particle;
                                      per Vol II.1 §7.1 GW section and
                                      Vol I §2 A-kernel derivation)
```

## Locked Vol II.1 §10.5 identity classes (80-row promoter)

```text
class                              matter  anti  total  partition | charge
────────────────────────────────   ──────  ────  ─────  ─────────────────
electron_like_minus                    1     1      2   p=1, q=1, neg, d=0
positron_substrate_slot                1     1      2   p=1, q=1, pos, d=0
heavier_charged_lepton_minus           1     1      2   p=1, q=1, neg, d=1
heavier_positron_substrate_slot        1     1      2   p=1, q=1, pos, d=1
neutrino_like                          2     0      2   p=1, q=0
quark_like_charged                    28    28     56   p ∈ {2,3,4,6,8,9,12}
neutral_higher_partition              14     0     14   p ∈ {2,3,4,6,8,9,12}
────────────────────────────────   ──────  ────  ─────
TOTAL                                 48    32     80
```

## Locked anchoring rules (citations of sealed CRs)

### Rule A — PDG_ANCHORED (sealed CR explicitly maps to PDG)

```text
A.1  Higgs H          QP093A-0299     via known_match column + CR269
                                      (M − D²/R = 125.25 GeV)
A.2  photon γ         QP093A-0301     via Vol II.1 §9.5
A.3  gluon g          QP093A-0304     via Vol II.1 §9.5
A.4  W±               QP093A-0302     via Vol II.1 §9.5
A.5  graviton Θ       QP093A-0300     via Vol II.1 §9.5
A.6  Z                QP093A-0303     via Vol II.1 §9.5
```

### Rule B — PDG_CANDIDATE (identity class suggests PDG mapping)

Vol II.1 §10.5 lays out the identity classes but explicitly names them
"substrate-natural taxonomies, not PDG-named particles". The following
mappings are consistent with the identity classes but are not sealed
CRs of their own — hence CANDIDATE not ANCHORED:

```text
B.1  electron_like_minus (matter d=0)     → e⁻ candidate
B.2  positron proper (anti of B.1)        → e⁺ candidate (via CR256 A-op)
B.3  heavier_charged_lepton_minus (d=1)   → μ⁻ candidate
B.4  μ⁺ candidate (anti of B.3)           → μ⁺ candidate (via CR256 A-op)
B.5  neutrino_like d=0 matter             → ν eigenstate m₁ candidate
                                            (per Vol II.1 §14.7 + CR268)
B.6  neutrino_like d=1 matter             → ν eigenstate m₂ candidate
B.7  (p=1, d=2, sign=neg, matter)         → τ⁻ candidate
                                            (third-generation charged lepton
                                            slot; per Vol II.1 §9.4 h_T=2 layer
                                            + CR268 three-generation spectrum)
B.8  τ⁺ candidate (anti of B.7)           → τ⁺ candidate (via CR256 A-op)
B.9  (p=1, d=2, sign=neut, matter)        → ν eigenstate m₃ candidate
                                            (heaviest neutrino per CR268
                                            m₃ = ĥ·d̂)
```

### Rule C — SAM_ORPHAN (substrate-role, no PDG counterpart)

```text
C.1  A_FIELD_CARRIER (QP093A-0305)        SAM accumulation-field carrier
                                          (Vol I §2 A-kernel; Vol II.1)
C.2  bow-fixed-point matter observable   QP093A-0023 (p=12, d=0, s=−)
                                          per CR256 orphan; matter-only
                                          because A₊(12,0) = 0
C.3  substrate-forbidden antiparticle    QP093A-0088 (p=12, d=0, anti+)
                                          qA=0 exactly per CR256
                                          hard-zero falsifier
C.4  positron_substrate_slot (matter,    Vol II.1 §10.5 explicitly
     d=0/1/2, 3 rows)                     says "NOT the positron";
                                          positive-charge substrate
                                          address per CR254 c₊ = 5/4
C.4b positron_substrate_slot conjugate   antimatter partner (sign=neg)
     (antimatter, d=0/1/2, 3 rows)        of the matter positron_substrate_
                                          slot; NOT the physical electron
                                          under CR256 A-op since matter
                                          partner isn't the physical
                                          positron
C.5  heavier_positron_substrate_slot     same reasons as C.4/C.4b at d=1
     (matter + anti, 2 rows)              — subsumed under C.4/C.4b
C.6  neutral_higher_partition (14 rows)  substrate-native neutral
                                          scalars; no PDG analog;
                                          per CR255 compact neutral law
C.7  quark_like_charged (56 rows)        substrate quark SLOT rows;
                                          per Vol II.1 §10.5 "not
                                          PDG-named"; individual quark
                                          PDG mapping deferred
```

### Rule D — COMPOSITE_UNANCHORED

```text
D.1  bin = "bound_composite_rows"        → 169 baryon / meson candidates
                                          pending downstream hadron CR
D.2  bin = "unstable_resonance_rows"     → 25 resonances; deduct the
                                          Higgs (Rule A.1) → 24 pending
D.3  bin = "hidden_source_support_rows"  → 8 lifted-connector rows
                                          per Vol II.1 §9.5 (M_native =
                                          L_p = p + p²/R²); SAM_ORPHAN
                                          category — carriers not particles
D.4  bin = "carrier_only_rows"           → already handled by Rule A
                                          (5 named T13 lanes) plus
                                          A_FIELD_CARRIER (Rule C.1)
```

Note on D.3: SOURCE_SUPPORT_PACKET rows are lifted connectors, not
particles. They will be tagged SAM_ORPHAN under Rule C (with a specific
"lifted_connector" sub-role) rather than COMPOSITE.

### Rule E — REJECTED

```text
E.1  closure_status starts with "REJECT_"   → tagged REJECTED with the
                                              specific CR252 rejection
                                              reason preserved
E.2  bin = "rejected_fake_closures"         → 8 rows, all REJECT_FAKE_*
```

## Locked classification protocol

For each of the 321 rows, apply rules in this order (first match wins):

```text
1. Row has known_match populated       → PDG_ANCHORED (Rule A.1)
2. Row matches Rule A.2 .. A.6         → PDG_ANCHORED
3. Row matches Rule C.1 .. C.5         → SAM_ORPHAN (specific slot ID)
4. Row's closure_status starts with
   "REJECT_" or bin is
   "rejected_fake_closures"            → REJECTED
5. Row matches Rule B.1 .. B.6         → PDG_CANDIDATE
6. Row matches Rule C.6 (NHP) or
   Rule C.7 (quark-slot) or Rule D.3   → SAM_ORPHAN with sub-role
7. Row's bin is "bound_composite_rows"
   or "unstable_resonance_rows"        → COMPOSITE_UNANCHORED
8. Any other row                       → UNCATEGORIZED (should be 0)
```

## Sealed PASS gates

```text
G1  All 321 rows receive exactly one category label (no
    UNCATEGORIZED rows, no double-labeling).

G2  Exactly 6 rows tagged PDG_ANCHORED corresponding to the 5 T13
    named carriers + 1 Higgs (Rule A.1 .. A.6). The candidate_ids
    match the expected list precisely.

G3  Fold identity preserved in the output:
    - fermion_half_write rows count = 114 (from Vol II.1 §9.4)
    - PDG_ANCHORED gauge boson count = 5 (photon, gluon, W, graviton, Z)
    - Higgs row count = 1
    - A_FIELD_CARRIER tagged SAM_ORPHAN = 1 row

G4  Bow-fixed-point orphan pair explicitly tagged with CR256
    reference:
      QP093A-0023 → SAM_ORPHAN, sub-role "bow_trace_matter_only"
      QP093A-0088 → SAM_ORPHAN, sub-role "hard_zero_falsifier"

G5  Vol II.1 §10.5 identity class counts preserved in the output:
      electron_like_minus total = 2 (1 matter + 1 anti)
      positron_substrate_slot total = 2
      heavier_charged_lepton_minus total = 2
      heavier_positron_substrate_slot total = 2
      neutrino_like matter = 2 (no anti; Majorana convention)
      quark_like_charged total = 56 (28 matter + 28 anti)
      neutral_higher_partition matter = 14 (no anti; Majorana convention)
    Sum = 80 = CR253 promoter row count

G6  All REJECT_* / rejected_fake_closures rows tagged REJECTED
    with the specific CR252 rejection reason preserved in the notes
    column.

G7  Precommit sha256 verified at runner load; input CR252 catalog
    hash matches; forbidden-file open() guard not tripped.

PASS      iff G1 AND G2 AND G3 AND G4 AND G5 AND G6 AND G7 all hold.

BOUNDARY  iff G1 AND G7 hold AND exactly one of {G2..G6} fails.

FAIL      iff G1 fails, G7 fails, or two or more of {G2..G6} fail.
```

## Reported evidence (not gated)

```text
E1  Row counts by category (PDG_ANCHORED, PDG_CANDIDATE,
    SAM_ORPHAN, COMPOSITE_UNANCHORED, REJECTED) — should sum to 321.

E2  For each PDG_ANCHORED row, echo the sealed CR reference and the
    substrate expression that anchors it.

E3  For each SAM_ORPHAN row, echo the substrate role and the sealed
    CR reference that identifies the role.

E4  For each PDG_CANDIDATE row, echo the Vol II.1 identity class and
    what would need to be sealed for it to be promoted to PDG_ANCHORED.

E5  COMPOSITE_UNANCHORED count broken down by bin, so the downstream
    hadron CR knows the scope of unanchored composite work.

E6  Sanity: the CR253 80-row promoter subset accounts for exactly 80
    rows in the output, distributed across the categories per Rule B
    and Rule C.
```

## Pre-registered frozen inputs

| field | sha256 | description |
| --- | --- | --- |
| CR252_particle_catalog_v2.csv | to-be-verified at runner load | 321-row full catalog |

The runner whitelists this input plus the precommit and runner source.

## Rule-9 line

```text
This test could have failed by:
  (i) categorization producing UNCATEGORIZED rows (G1);
  (ii) the T13 named carriers not being at the expected candidate_ids
       or their operator_class labels not matching Vol II.1 §9.5 (G2);
  (iii) the fold-identity counts not matching Vol II.1 §9.4 (G3);
  (iv) the bow-trace orphan pair not being present at the expected
       row ids (G4);
  (v) Vol II.1 §10.5 identity class counts not matching (G5);
  (vi) CR252's REJECT_* tags not carrying through cleanly (G6);
  (vii) hash / whitelist tripping (G7).

Any of these failures would indicate the sealed downstream CRs and
the CR252 catalog are inconsistent with each other. The PASS says
they are consistent as of this seal date.
```

## What this CR seals

If PASS: the 321-row CR252 catalog receives a single sealed
anchoring artifact — the `CR276_anchoring_table.csv` — that maps
every row to one of five categories with citations to the sealed
CR that supports the tag. Downstream work (hadron identification,
mass-lift derivation, K1 forecast locks) reads from this table.
The scattered particle-side identifications across Vol II.1 §9.5,
§10.5, §14.7 and CRs 253/254/255/256/257/268/269 become
row-indexed rather than section-indexed.

If BOUNDARY: exactly one identity check misses; the rest of the
anchoring stands and the miss becomes an appeal item.

## Provenance hash chain

| artifact | reference |
| --- | --- |
| Vol II.1 §9.5 (T13 named carriers) | `SAM_VOLUME_II_1_MATTER_UPDATE_2026_06_28.md` |
| Vol II.1 §9.4 (fold identity) | same |
| Vol II.1 §10.5 (identity classes) | same |
| Vol II.1 §14.7 (neutrino sector) | same |
| CR253@09a (80-row promoter) | per branch HASHES |
| CR254@09a (compact matter-charged law) | per branch HASHES |
| CR255@09a (compact matter-neutral law) | per branch HASHES |
| CR256@09a (A-operator hard-zero) | per branch HASHES |
| CR257b@09a (A meets Θ at d=1) | per branch HASHES |
| CR268@09a (heaviest neutrino ID) | per branch HASHES |
| CR269@09a (bow / Higgs identity) | per branch HASHES |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
