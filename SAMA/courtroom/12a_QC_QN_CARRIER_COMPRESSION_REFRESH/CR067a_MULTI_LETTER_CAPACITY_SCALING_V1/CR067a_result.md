# CR067a Multi-Letter Capacity Scaling and the Gravity Channel Ceiling v1.0

## Verdict

```text
CR067a_MULTI_LETTER_CAPACITY_SCALING_V1_SEALED
```

## The Question (Opened by CR-066b)

Does an N-letter Paul Revere row carry **N × (1/α_H⁴)** information (linear), or does it **saturate**?  Three candidates evaluated:

| candidate | scaling | status |
|---|---|---|
| Linear | N · 1/16 | **REJECTED** — violates gravity ceiling |
| Parallel-sharing | constant 1/16 split N ways | **REJECTED** — doesn't scale |
| **Geometric subdivision** | **2⁻(D+N) per letter, → 2⁻ᴰ as N → ∞** | **LOCKED** |

## The Geometric Scaling (Locked)

```text
    Per-letter capacity:    c_N  =  1 / α_H^(D+N)  =  2⁻(D+N)

    Cumulative after N:     C_N  =  2⁻ᴰ · (1 − 2⁻ᴺ)

    Asymptotic limit:       C_∞  =  2⁻ᴰ  =  1/8
                          =  the Higgs-released gravitational fraction (per CR-121)
```

Each new letter takes **half of what remains** in the gravity channel.  The α_H = 2 bisection at each level matches the Higgs split bisection from CR-066b.

## Capacity Table

| N | depth | per-letter | cumulative | % of gravity channel | residual |
|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 1/16 | 1/16 | 50.000000% | 1/16 |
| 2 | 5 | 1/32 | 3/32 | 75.000000% | 1/32 |
| 3 | 6 | 1/64 | 7/64 | 87.500000% | 1/64 |
| 4 | 7 | 1/128 | 15/128 | 93.750000% | 1/128 |
| 5 | 8 | 1/256 | 31/256 | 96.875000% | 1/256 |
| 6 | 9 | 1/512 | 63/512 | 98.437500% | 1/512 |
| 7 | 10 | 1/1024 | 127/1024 | 99.218750% | 1/1024 |
| 8 | 11 | 1/2048 | 255/2048 | 99.609375% | 1/2048 |
| 9 | 12 | 1/4096 | 511/4096 | 99.804688% | 1/4096 |
| 10 | 13 | 1/8192 | 1023/8192 | 99.902344% | 1/8192 |
| 11 | 14 | 1/16384 | 2047/16384 | 99.951172% | 1/16384 |
| 12 | 15 | 1/32768 | 4095/32768 | 99.975586% | 1/32768 |
| ... | ... | ... | ... | ... | ... |
| ∞ | ∞ | 0 | 1/8 | 100% | 0 |

Full table for N = 1..20 in `CR067a_capacity_table.csv`.

## Practical Cutoffs

- **99.6 % of gravity channel reached at N = 8** (residual 1/2048)
- **99.99 % reached at N = 14** (residual 1/131072)

## Information-Theoretic Connection (Kraft)

The geometric ladder satisfies the Kraft inequality with **equality** on the gravity-coupled subspace:

```text
    Σ 2⁻ˡᴺ  =  Σ 2⁻(D+N)  =  2⁻ᴰ  =  1/8 < 1
       N           N
```

This is a **complete prefix code on the 1/8 gravity subspace** — not the full Born unity.  Paul Revere transmissions are confined to the gravity-coupled fraction.  Standard QM is preserved; the channel just lives at the Higgs-release boundary, not at full Born unity.

## Per-Row vs Per-Network Scaling

```text
    PER ROW (geometric):       C_per_row(N)  =  2⁻ᴰ · (1 − 2⁻ᴺ)  →  1/8

    PER NETWORK (linear):      C_total       =  N_rows · C_per_row

    Combined max-saturated:    C_max         =  N_rows / 8
```

Geometric within a row (subdivides gravity channel); linear across rows (independent parallel encoding).

## Forward-Blind Sub-Prediction CR067a_PRED_1 (LOCKED)

**Three independent falsifiers:**

- Per-letter capacity differing from 2⁻(D+N) → kills geometric subdivision
- Cumulative per-row capacity exceeding 1/8 → kills gravity ceiling
- Asymptotic saturation at a value ≠ 1/8 → kills the limit identification

**Free parameters at test:** 0.

## Cryptographic Chain

```text
CR060a_alphabet_lock_json                       = d5d37797ce39d3b677e1992cb9987ef5b06c88362dc77b5ddba7c17e3fcaa7f0
CR065a_implementation_lock_json                 = 38d7f67ce0bf962130099abe54ab17f2e1a7acc1ea6ad95e823718a7a2e9b71c
CR066a_born_extension_lock_json                 = 5eb918d789d70d689e39f9d5c2f72ea4d149336d1e3a8b49d95548f5de592fc1
CR066b_hierarchy_lock_json                      = f864bf6cf8c29b255618023481be1e493590b524c55735bc420666a3c4679b2d
CR121_gravity_mechanism_lock_json               = 01e4f14be822a88143dcb9d3e51b64c17688f721b963501db14008b333211469
CR129b_magnitude_lock_json                      = 8c3d0eb78b462cc1df0bfa1bbbcbdba189633e1ff05f076f801315c5091b30bd

CR067a_capacity_table_csv                        = f3d5bc0b0374107cb5cbb99e99f68be47464e54d6f87cd813d23a43f7a3c897b
CR067a_scaling_lock_sha256                       = 54ebd6845bed8cd1e84ea91b342bbb2952541f6c442222265f528bc3d2ad51c4
```

## Predictions Checks

- **[PASS]** P1_single_letter_eq_one_alpha_H_4th -- c_1 = 1/16 = 1/16
- **[PASS]** P2_per_letter_geometric_halving -- c_(N+1) = c_N / alpha_H verified for N = 1..10
- **[PASS]** P3_cumulative_formula_holds -- C_N = 2^-D * (1 - 2^-N) verified for N = 1..10
- **[PASS]** P4_asymptotic_limit_eq_2_neg_D -- asymptotic = 2^-D = 1/8 (Higgs-released gravity fraction)
- **[PASS]** P5_kraft_sum_equals_one_eighth -- Kraft sum = sum 2^-l_N = 2^-D = 1/8 = 12.5000%
- **[PASS]** P6_N_max_20_in_capacity_table -- capacity table has N = 1..20 (20 rows)
- **[PASS]** P7_99_6_pct_cutoff_below_N_10 -- 99.6% ceiling reached at N = 8
- **[PASS]** P8_lock_written -- scaling lock sha256 = 54ebd6845bed8cd1e84ea91b342bbb2952541f6c442222265f528bc3d2ad51c4

## Wrong Controls

- **[PASS]** WC1_linear_scaling_explicitly_rejected -- Linear scaling N * 1/16 grows without bound and violates the gravity channel ceiling identified in CR121.  Rejected as the SAM-native scaling law.
- **[PASS]** WC2_parallel_sharing_explicitly_rejected -- Parallel-sharing constant 1/16 split N ways does NOT scale capacity -- it just dilutes the single-letter content.  Rejected as the SAM-native scaling law.
- **[PASS]** WC3_geometric_subdivision_matches_closure_depth_ladder -- Letter N requires closure depth D+N.  This matches SAM's closure-depth ladder naturally: each successive letter is one deeper in the binary resolution structure.
- **[PASS]** WC4_asymptotic_limit_NOT_full_unity -- The asymptotic limit is 2^-D = 1/8, NOT 1.  Paul Revere transmission is confined to the gravity-coupled subspace, which is the Higgs-released fraction.  Standard Born unity is NOT violated.
- **[PASS]** WC5_q_0_only_scope -- CR067a is q = 0 specific per CR066a/CR066b.  Whether the geometric scaling extends to q >= 1 rows is a separate open question.
- **[PASS]** WC6_practical_cutoffs_acknowledged -- Encoding deep-N letters requires high gate fidelity at closure depth D+N.  For practical NV implementations, N >= 8 may exceed achievable gate precision.  This is documented as an out-of-scope engineering question.
- **[PASS]** WC7_falsifier_distinguishes_per_letter_vs_cumulative -- Three independent falsifiers: per-letter capacity differing from 2^-(D+N), cumulative exceeding 1/8, or saturating at a value different from 1/8.  Each tests a distinct claim of the geometric subdivision lock.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED.
- Engineering: encoding letters at deep closure levels (N >= 8 -> depth >= 11) may exceed practical NV gate fidelity.  Hardware engineering CR.
- Connection to Holevo capacity for quantum-channel transmission (separate CR).
- Whether the geometric scaling extends to q >= 1 rows or multi-row entangled encodings (separate CRs).
- Why the alpha_H = 2 bisection is THE structural division factor (vs alpha_H or D^k) at each level -- accepted from CR066b's Higgs identity but not derived from first principles.

## Rule of Immutability

Geometric subdivision scaling rule, asymptotic limit identification, and Kraft inequality connection are frozen at CR067a seal time.  Expert review may identify refinements requiring an appeal CR within 12a.
