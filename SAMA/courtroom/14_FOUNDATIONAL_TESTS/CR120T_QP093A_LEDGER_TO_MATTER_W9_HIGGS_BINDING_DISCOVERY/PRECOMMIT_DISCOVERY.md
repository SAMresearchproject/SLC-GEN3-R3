# CR120T Discovery Precommit

record_id: `CR120T_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY`
task_class: `CONSTRUCTIVE_DISCOVERY_THEN_FROZEN_VALIDATION`
controlling_brief: `SAM_QP093A_LEDGER_TO_MATTER_W9_HIGGS_BINDING_DISCOVERY.md`
preflight: `artifacts/preflight_filled/PREFLIGHT_20260714_122508_no_script.md`
existing_records_preserved: `CR120R, CR120S`
source_manifest_sha256: `b1eee6ab1603c7a3ed5995afb5e1b3061b17f1c8aafce11d7db0f675a7769451`
assumption_register_sha256: `e1c96f59b0e22cf602acd5931f85ef00cacae624afe25bfe1ef28f0f75349382`

## Discovery question

Can the two updated QP093A workbooks be reconciled to canonical source rows,
typed as a role-sensitive `S8 + X1 -> W9` ledger shadow, and used to discover
an observation-blind F81 projection candidate or a typed binding-accounting
change without using the finished totals as coefficients?

## Allowed discovery inputs

The discovery runner may open only files hash-locked in `SOURCE_MANIFEST.json`.
It may inspect both workbook memberships, their displayed/cached totals, user
annotations, and the canonical QP093A catalog. It may inspect the `train` rows
of the CR261 35/20 split for binding candidate comparison.

The workbooks are research overlays. Canonical QP identity, row values, and
source typing come from the hash-locked QP093A catalog and sealed CR records.

## Discovery-only knowledge

The following are intentionally visible during discovery and therefore cannot
validate a candidate rule:

- the current 81-row membership;
- the target count 81;
- the target total 12,600;
- the 100-row total 16,200;
- all workbook annotations and manual reclassification columns.

## Binding firewall

During discovery, candidate selection may use only CR261 rows whose frozen
`set` field is `train`. It must not parse or score `B_u_obs_MeV` for rows whose
`set` field is `test`, and it must not use CR277 extended observed residuals.

Candidate formulas may not use `126`, `144`, `162`, `12,600`, or `16,200` as
fitted coefficients. QP093A-0066 and QP093A-0299 may constrain roles and
counting only. No isotope-specific parameters, candidate-ID patches, or
same-run holdout repairs are allowed.

## Workbook audit contract

The discovery runner must record for both workbooks:

- file hash, package entries, sheet names and dimensions;
- columns, formulas and cached values, hidden rows/columns, tables, duplicate
  candidate IDs, annotations, and user-reclassification fields;
- a cell-level diff, with special dossiers for QP093A-0066 and QP093A-0299;
- the exact QP093A-0299 `M_native` values, cell addresses, literal/formula
  status, and controlling-source disposition.

The first workbook is currently open in Excel. A saved `SaveCopyAs` capture may
be used by the runner only if its logical cells reconcile to the prior frozen
source extraction. The original workbook and both sealed prior CRs must not be
modified.

## Required discovery tests

1. Reproduce `105 - five p=9,g=0 = 100`, `sum(M_native)=16,200`, and mean `162`.
2. Reproduce the explicit 81-row sheet and `sum(M_native)=12,600`.
3. Reproduce `100L`, `100N`, `100M`, `L=N+Theta`, and `M=N-Theta` exactly.
4. Build the full 100-to-81 occurrence register and role-sensitive delta.
5. Test same-role `p8+p1=p9` and control `p6+p3=p9` at every available depth
   for `M_native`, observed/qA, tensor, retained, and surface fields.
6. Separate `S8_BINARY_SURFACE`, `X1_AXIS_SELF_CHANNEL`, and
   `W9_CLOSURE_WITNESS` from QP coordinates, carriers, and supports.
7. Test global five-row packet exclusion versus neutral-W9 row witness.
8. Test QP093A-0066 as `N144 = Theta18 + M126`, its p1/p8/p9 g=2 triad,
   and all roster-exclusion hypotheses named in the controlling brief.
9. Test QP093A-0299 source conflict and exact reveal/debit/support identities.
10. Discover and score the smallest F81 candidate rules without promoting
    any rule during this run.
11. Reproduce the binding training lane and compare typed consequences B1-B5
    on training data only, including algebraic-dependence checks.

## Discovery gates

- `D0_SOURCE_HASHES`: every frozen source and snapshot hash matches.
- `D1_WORKBOOK_AUDIT`: workbook inventory, formula/cache audit, and diff emit.
- `D2_LEDGER_REPRODUCTION`: 100/16,200 and 81/12,600 reproduce exactly.
- `D3_TYPED_ROW_AUDIT`: same-role arithmetic and competing decomposition emit.
- `D4_ROW_DOSSIERS`: 0066 and 0299 source-typed dossiers emit.
- `D5_RULE_DISCOVERY`: non-whitelist candidate rules and scorecard emit.
- `D6_BINDING_DISCOVERY_FIREWALL`: only 35 training observations are scored.

Discovery succeeds when D0-D6 are complete. Scientific promotion is not a
discovery gate. Failure to find a valid F81 or binding rule is an allowed
discovery result and triggers the brief's frozen-boundary path.

## Hard stops

- Do not overwrite CR120R, CR120S, either workbook, or a canonical source.
- Do not install a SAM Language operator.
- Do not open held-out/extended binding observations during discovery.
- Do not freeze a candidate-ID whitelist or a rule mentioning 81 or 12,600.
- Do not run validation in this process.
