# CR252 Particle Catalog Spine-Refresh — Result

**Verdict:** `PASS`
**Amendment:** [CR252_PRECOMMIT_AMENDMENT.md](CR252_PRECOMMIT_AMENDMENT.md) applied (V-3/F2 corrected)
**Started:** 2026-06-24T22:15:10+00:00
**Completed:** 2026-06-24T22:15:11+00:00

## Counts
- Baseline rows (2026-06-15): 321
- Regen v2 rows: 321
- Matter rows (v2): 286
- Baseline sha256: `3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6`
- v2 sha256: `3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6`
- WC-1 second-run sha256: `3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6` (deterministic: True)
- **Bit-identical to baseline:** True

## Change-class distribution
- unchanged: 321

## Presence distribution
- in_both: 321

## Verifications
- V-1_row_count_321: True
- V-2_bin_distribution: {'stable_matter_rows': 63, 'unstable_resonance_rows': 25, 'antimatter_conjugate_rows': 42, 'bound_composite_rows': 169, 'carrier_only_rows': 6, 'hidden_source_support_rows': 8, 'rejected_fake_closures': 8}
- V-3_matter_count_matches_baseline: True
- V-3_matter_count_v2: 286
- V-3_matter_count_baseline: 286
- V-4_candidate_id_stability: True
- V-5_audit_completeness: True
- V-6_recheck_derivations: True
- V-7_attribution_for_named: True
- V-8_no_unexplained: True

## Wrong controls
- WC-1 deterministic: True
- WC-2 R load-bearing (material difference): True
- WC-3 key rows:
  - QP093A-0306: present=True change_class=unchanged max_rel_delta=0
  - QP093A-0043: present=True change_class=unchanged max_rel_delta=0
  - QP093A-0313: present=True change_class=unchanged max_rel_delta=0
- WC-4 carrier non-promotion preserved: True (6 carriers, 0 promoted)

## Pass conditions
- P1_verifications: True
- P2_all_classified: True
- P3_wrong_controls: True
- P4_no_unexplained: True
- P5_no_env_drift: True
