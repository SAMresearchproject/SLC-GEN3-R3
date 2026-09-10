# CR009 Connection-Fee K1 Reveal — Result

**Verdict:** `FAIL`
**Started:** 2026-06-24T22:57:09+00:00
**Completed:** 2026-06-24T22:57:09+00:00
**Catalog sha256:** `3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6`

## Cohort metrics (mean-based)
- Derivation set (n_conn=2, q∈{1..4}): n=67, mean(abs_rel_delta)=0.37733062781945417642079206630979612844740411628571222156742593949826109383746782
- Extension set (n_conn=2, other q): n=53, mean(abs_rel_delta)=1.8066440972188217476459064077173715761263452868554848109847657979818936492971741
- Pair cohort (n_conn=1): n=65, mean(actual_ratio)=0.98756868131868131868131868131868131868131868131868131868131868131868131868131866, drift_from_1=0.01243131868131868131868131868131868131868131868131868131868131868131868131868134
- Single-atom (n_conn=0): n=136, integrity_violations=42

## Classification distribution
- Derivation: {'systematic_miss': 49, 'exact_match': 18}
- Extension (n_conn=2): {'systematic_miss': 47, 'exact_match': 6}
- Pair (n_conn=1): {'systematic_miss': 9, 'approximate_match': 54, 'close_match': 2}

## Pass conditions
- P1_verifications: True
- P2_derivation_mean: False
- P3_extension_mean: False
- P4_pair_mean: False
- P5_single_atom_integrity: False
- P6_wrong_controls: True

## FAIL conditions triggered
- F1_derivation_drift: TRIGGERED
- F2_extension_no_extension: TRIGGERED
- F3_pair_principle_false: TRIGGERED
- F4_single_atom_broken: TRIGGERED

## Wrong controls
- WC-1_R_perturb_10: passed=True
- WC-2_D_perturb_2: passed=True
- WC-3_offset_q_only: passed=True
- WC-4_offset_q_plus_R: passed=True
- WC-5_pair_mean: passed=False
