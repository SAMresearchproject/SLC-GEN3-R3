# CR253 — Particle Promoter (80-Row Stable Matter Set)

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Sealed by:** Sean Brady, 2026-06-28
**Upstream concern:** the QP098 / QP106 stability filter, surfaced and
verified in the QP night session 2026-06-27, identifies an **80-row
stable matter set** structurally distinct from CR219's 126-row
matter-allowed export. CR253 promotes this 80-row set to CR-class
discipline so downstream particle-identity work in branch 09a can
consume it as a sealed surface.

**Stewardship:**
`d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

Does the QP098 stability filter, applied to the
corrected 299-row QP093A catalog (post-A_FIELD_CARRIER removal at
QP104), produce **exactly 80 rows** decomposing as **48 stable_matter
+ 32 antimatter_conjugate**, with full conjugate-parity closure on
the charged sub-grid and substrate-natural exception accounting on
the Majorana-style matter-only rows?

The promoter rule (locked):

```text
stable(r) = (I_T(r) == 0)
        AND (h_T(r) in {0, 1})
        AND (q(r)  in {0, 1, 2, 3, 4, 6, 8, 9, 12})
        AND (bin(r) in {stable_matter_rows, antimatter_conjugate_rows})

I_T(r)  = tensor-port closure defect under QP097 T13 lane structure
            with bigrade-multiplicity grammar
h_T(r)  = closure_depth column from the catalog
q(r)    = q_abs column from the catalog
bin(r)  = bin column from the catalog
```

T13 lane structure:
`{1, 1, 2, 3, 4, 6, 8, 8, 9, 9, 12, 18, 81}`

Connection rule (from QP097, used by I_T computation):
row `r` connects to lane value `v_j` iff
`(v_j | q AND q > 0)` OR `(v_j | p_i for some partition component p_i)`
OR `(v_j == 1 AND q == 0)` OR `(v_j == 18 AND (18 in p OR q == 18))`.

## Source boundary

```text
input catalog : 09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/
                CR253_input_catalog_299.csv
input hash    : 33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c
input lineage : corrected QP093A v3 from QP104, originally derived from
                qp093a_candidate_catalog.csv (QP093A enumerator) with
                13 T13 carrier+lifted rows added (QP101B) and the
                erroneous A_FIELD_CARRIER row (QP093A-0305) removed
                per QP102/QP103 (ledger-closure self-reference proof)
```

## Expected output

| quantity | expected |
| --- | ---: |
| total promoted rows | **80** |
| stable_matter_rows bin | 48 |
| antimatter_conjugate_rows bin | 32 |
| every antimatter row has matter conjugate partner | 32 / 32 |
| matter rows without antimatter mirror (Majorana exceptions) | 16 |
|   ↳ neutral_higher_partition (matter only) | 14 |
|   ↳ neutrino_like (p=1, q=0, matter only) | 2 |
| charged sub-grid (7p × 2sign × 2depth × 2sides) | 56 quark-like |
| lepton sub-grid (1p × 2sign × 2depth × 2sides) | 8 |
| TOTAL charged: | 64 |
| TOTAL neutral matter-only: | 16 |

## Class-by-class breakdown (substrate-natural taxonomy)

| identity rule | matter | anti | total |
| --- | ---: | ---: | ---: |
| electron_like_minus (p=1, q=1, neg, d=0) | 1 | 1 | 2 |
| positron_substrate_slot (p=1, q=1, pos, d=0) | 1 | 1 | 2 |
| heavier_charged_lepton_minus (p=1, q=1, neg, d=1) | 1 | 1 | 2 |
| heavier_positron_substrate_slot (p=1, q=1, pos, d=1) | 1 | 1 | 2 |
| neutrino_like (p=1, q=0) | 2 | 0 | 2 |
| quark_like_charged (p ∈ {2,3,4,6,8,9,12}, q=p) | 28 | 28 | 56 |
| neutral_higher_partition (p ∈ {2,3,4,6,8,9,12}, q=0) | 14 | 0 | 14 |
| **TOTAL** | **48** | **32** | **80** |

## Wrong controls

W1. **Bin-rule relaxation**: include `bound_composite_rows` in `B_allowed`.
    Expected: row count rises sharply (composites would flood in).

W2. **Depth-rule relaxation**: include `h_T = 2`. Expected: 80 + 34 =
    114 rows (the QP110-verified set).

W3. **Charge-rule relaxation**: drop the q ∈ bigrade requirement.
    Expected: small additional rows (q ∈ {5, 7, 10, 11}) appear.

W4. **Tensor-defect relaxation**: include `I_T > 0`. Expected: rows
    with non-zero closure defects appear; under QP097/QP098 these
    were the boundary rows.

W5. **Random bin permutation**: shuffle bin labels across the 299-row
    catalog, re-apply the promoter. Expected: 80-row count is NOT
    reproduced; the 48/32 split is destroyed.

For each wrong-control, record the row count produced and compare to
the canonical 80.

## Verdict tree

```text
PASS:
  (1) exactly 80 rows promoted
  (2) 48 / 32 matter / anti split exact
  (3) every antimatter row has a matter conjugate partner (via
      route_combination 'anti(X)' lookup; 32/32)
  (4) class-by-class breakdown matches the table above exactly
  (5) wrong-controls W1, W2, W3, W4 each produce row counts strictly
      DIFFERENT from 80 (rule sensitivity confirmed)
  (6) W5 random permutation reproduces 80 in < 5% of 1000 trials

BOUNDARY:
  any single PASS condition fails by ±2 rows or less, with
  structural attribution

FAIL:
  any single PASS condition fails by more than ±2 rows, OR
  the conjugate-parity closure is broken
```

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR253_input_catalog_299.csv | `33abc9e19f008c7c8082fbc628dc0f46786820ba7682905419a2929c8ada5b7c` |
| upstream QP104 corrected catalog | same as above (this CR consumes the QP104 output verbatim) |
| upstream QP106 80-row signatures (reference) | `c8a398a3160045e3c4f1b692da12ef99b87d86e0873491d5e96867007aca53f1` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |

The runner SHA-256 will be sealed in HASHES.txt before execution per
hostile-environment protocol.

## What this CR does NOT do

- It does NOT re-verify the T13 partition sum = 162 (documented at
  Section 4.3 + QP102).
- It does NOT re-derive c_+ = 5/4 or c_- = 3/2 (QP108 / QP112).
- It does NOT generate qA values from the substrate laws (QP108-QP110
  cover that; downstream CRs may consume those laws).
- It does NOT classify rows by named particle (electron, muon,
  proton, ...); the 7 substrate-natural classes above are
  partition+charge+depth+sign+bin signatures, not PDG names.

It promotes the 80-row stable matter surface so downstream branch-09a
work has a sealed CR-class artifact to reference instead of the QP
exploration output.

## Out of scope

- composite-row layer (h_T = 3) — separate CR family
- carrier / lifted T13 rows — those are infrastructure, not matter
- Standard Model PDG assignment — downstream concern
- Parent-repo derivation entry — separate handoff after this CR seals
