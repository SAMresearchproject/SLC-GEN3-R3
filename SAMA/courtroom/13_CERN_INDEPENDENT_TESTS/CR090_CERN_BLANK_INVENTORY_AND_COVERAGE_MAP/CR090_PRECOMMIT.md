# CR090 CERN_BLANK_INVENTORY_AND_COVERAGE_MAP

## Test Class

```text
INVENTORY_AND_COVERAGE_MAP (no anchor test in this CR; anchor tests
begin at CR091)
```

## Preflight

```text
CR090 is the inventory CR. It enumerates the universe of CERN-published
independent measurements the 13 branch could anchor against, classifies
each candidate by the SAM closure-surface row or role-operator it
exposes, and assigns each candidate to a target CR (CR091..CR095) or
to the CR096 honest-negative rejection set.

CR090 does NOT load anchor values. It declares which candidates will be
loaded later by which CR, with the publication reference and the
expected SAM prediction source.

The candidate anchor inventory CSV is the artifact CR090 emits and the
artifact CR091..CR095 read to build their per-CR anchor envelopes.
```

## Question

Has the 13 branch enumerated a comprehensive, citation-complete
inventory of CERN-published independent measurements that:

```text
1. spans the five anchor-class CRs (CR091 EW, CR092 Higgs, CR093 heavy
   flavour, CR094 exotic spectroscopy, CR095 lepton universality)
2. lists at least two independent CERN measurements per observable
   wherever multiple CERN experiments published (for Pillar 3 cross-
   source defense)
3. names the SAM prediction source for each candidate (09a row id,
   QP075 role operator, V4.1 closure_campaign id, etc.)
4. lists the wrong-controls set (withdrawn / Tevatron / B-factory /
   Fermilab / PDG-average / perturbed) destined for CR096
5. carries publication date in every row, so Pillar 2 temporal
   ordering checks have a fixed reference
```

## Pass Conditions

- `CR090_candidate_anchor_inventory.csv` exists in the CR090 folder
  and contains, per candidate row:
  - candidate_id, observable_name, experiment, publication_reference,
    publication_date_utc, anchor_class, target_cr,
    measurement_central_value (optional at CR090, mandatory at the
    target CR's envelope), stat_uncertainty, sys_uncertainty, units,
    sam_prediction_source (09a row id or QP075 operator id),
    cross_source_status (SINGLE | MULTI-COUNTERPART_LISTED),
    citation_verification_status (PENDING | VERIFIED_BY_CURATOR),
    honest_negative_class (NULL for live candidates; CLASS_A..G for
    CR096 rows).
- The inventory has at minimum N >= 5 live candidates per CR091..CR095
  target_cr (so each target CR can carry a credible anchor table).
- The inventory has at minimum N >= 7 honest-negative candidates
  (one per CR096 class A..G).
- Every live candidate row has a non-empty `sam_prediction_source`
  field referencing a load-bearing 09a CR or QP075 artifact.
- Every honest-negative row has a non-empty `honest_negative_class`
  field naming the class A..G.
- `CR090_coverage_map.md` exists and groups candidates by anchor_class,
  noting which observable has multi-experiment coverage (Pillar 3 use)
  and which is single-experiment-only.
- `CR090_summary.json` exists with counts: live_candidates_total,
  live_candidates_per_target_cr, honest_negative_candidates_total,
  honest_negative_candidates_per_class, observables_with_multi_experiment_cover,
  observables_with_single_experiment_only.

## Wrong Controls (Inventory Discipline Checks)

These check that the CR090 inventory itself is well-formed. None of
them gates the 09a verdict; they gate the inventory CSV. CR090 does
not open any anchor envelope and does not compute any residual.

- A candidate row whose `sam_prediction_source` does not resolve to a
  load-bearing 09a CR or QP075 artifact must fail
  `prediction_source_resolution_check` and be rejected from the
  inventory.
- A candidate row whose `publication_reference` is empty or whose
  `publication_date_utc` is missing must fail
  `cern_anchor_citation_completeness` and be rejected from the
  inventory.
- A candidate row marked as `target_cr = CR091..CR095` whose
  `honest_negative_class` is non-empty must fail
  `inventory_class_consistency_check` and be re-classified or
  rejected.
- A wrong-control row marked as `target_cr = CR096` whose
  `honest_negative_class` is empty must fail
  `wrong_control_class_assignment_check` and be re-classified or
  rejected.
- An anchor whose experiment is not in the allowed CERN list and is
  coded as `target_cr = CR091..CR095` must fail
  `experiment_admissibility_check` (e.g., a CDF, Belle, KamLAND, or
  Fermilab row miscoded as live). It belongs in CR096 class B/C/D/E
  for Gate A rejection.

Per the BLINDNESS_PROTOCOL `09a Immutability Rule`, none of these
inventory checks can modify 09a's prediction surface. They protect
the 13-branch inventory CSV; they do not put 09a on trial.

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = PENDING_HASH_AT_RUNNER_TIME
```

CR090 does not open anchor envelopes. The procedural-blindness step
order (Pillar 2) does not apply to this CR. But CR090 must reference
the protocol so that the inventory it builds is shaped to support
Pillars 1-4 in CR091..CR096.

## Rule-9 Line

```text
This test could have falsified the 13 branch coverage strategy - the
inventory CR that feeds CR091..CR096 - if the inventory was sparse
(fewer than ~5 live candidates per anchor-class CR), if multi-
experiment cross-source coverage was missing for any observable known
to have multiple CERN measurements, if any candidate named a
sam_prediction_source that does not resolve to a load-bearing
09a / QP075 artifact, if the honest-negative set did not cover all
seven CR096 classes A-G, or if the Gate A vs Gate R assignment per
class was inconsistent with the BLINDNESS_PROTOCOL two-gate rule.

This test does NOT falsify 09a. 09a stands as exemplary regardless of
the inventory's shape. CR090 protects the 13-branch inventory only.
```

## Cross-CR Links

```text
upstream  CR089 CERN_ALLOWED_INPUTS_AND_SOURCE_LOCK
forward   CR091..CR095 (each reads CR090 inventory to build its anchor
                         envelope; live candidates with matching target_cr)
forward   CR096 (reads CR090 inventory honest-negative rows)
forward   CR097 13 branch verdict zipper
```
