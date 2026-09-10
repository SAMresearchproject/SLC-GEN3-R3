# CR238 Substrate Spine Compaction + Primitive Typing Audit — Result

## Verdict

```text
CR238_PASS_SUBSTRATE_SPINE_COMPACTION_AND_PRIMITIVE_TYPING_AUDIT__FOUNDATIONAL_ATOMS_F_AND_S_ONLY__D_AND_ALPHA_H_ARE_READOUTS__TYPED_KAPPA_EQUALS_7117_OVER_768_BIT_IDENTICAL_TO_CR221__TYPED_g_EQUALS_1_OVER_64_BIT_IDENTICAL_TO_CR221__126_OF_126_MATTER_ROWS_PLUS_13_OF_13_BLOCKED_ROWS_PLUS_8_OF_8_HIDDEN_SUPPORT_ROWS_REGRADED_FROM_TYPED_KERNEL__D_EQUALS_3_UNIQUE_INTEGER_SOLUTION_OF_FACE_AND_RADIX_CLOSURE_AXIOMS__ZERO_RAW_LITERAL_INJECTIONS_IN_RUNNER__ALL_NINE_WRONG_CONTROLS_BROKE_AS_PREDICTED
```

`execution_status   = CLEAN`
`scientific_verdict = PASS`
`classification     = STRUCTURAL_REDUCTION_AND_TYPING_AUDIT (downstream unification of CR114 / CR217 / CR221 / CR222 / CR229 / CR232 / CR233)`
`precommit_sha      = 5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293`

## Claim

The substrate spine reduces to two foundational dimensionless atoms `{ℱ, S}` plus one structural constant `α_H = 2` (the binary readout, equal to `ℒ/ℱ`) plus one dimensional bridge `μ_Q`. Every other structural quantity — `D`, `ℒ`, `𝒱`, `Θ`, `R`, `R²`, `M`, `A_0`, `A_share`, `A_side`, `κ`, `g` — derives from these by a typed expression with no raw literal injection.

The typed kernel `κ = (R−1)(ℱ·S − 1) / (D · α_H^S)` reproduces CR221's frozen `kappa_floor = 7117/768` bit-identically. The typed neutron unit `g = 1/S²` reproduces CR221's frozen `neutron_G_unit = 1/64` bit-identically. The CR232 matter gate, blocked-row zeroing, and hidden-support surcharge all regrade cleanly from the typed kernel on the SHA-locked CR219 source.

The substrate dimension `D = 3` is the **unique positive integer** in the scan range `D ∈ {1, …, 12}` satisfying `D^(D−1) = S + 1` at canonical `S = 8` — equivalently, the only D at which the face axiom `ℱ = D^(D+1)` and the radix-closure axiom `ℱ = (S+1)·D²` agree. The canonical substrate `{ℱ = 81, S = 8}` is structurally selected, not chosen.

## Inputs (Hash-Locked)

```text
Precommit SHA-256:  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR219 CSV SHA-256:  45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Foundational atoms: ℱ = 81, S = 8
Structural const:   α_H = 2
```

## Block A — Typed Structural Identities (P1–P11)

```text
checks_pass : 31 / 31
rationals   : exact (P1–P10)
A_0         : exact symbolic π-normalized identity (P11)
```

Every typed derivation in the spine produced exact equality, evaluated as sympy `Rational` for P1–P10 and as a symbolic identity for the π-bearing `A_0 = V / (π · α_H · ℒ) = 1/(12π)`. Both `A_share = 1/12` and `A_side = 1/24` are exact rationals.

Per-check breakdown in `CR238_block_a_checks.csv`.

## Block B — Element-Kernel Bit-Identical Match Against CR221 (the load-bearing test)

| Prediction | Typed value | CR221 frozen | Match |
|---|---|---|---|
| P12 — `κ = (R−1)(ℱ·S − 1) / (D · α_H^S)` | `7117/768` | `7117/768` | **bit-identical** |
| P13 — `g = 1/S²` | `1/64` | `1/64` | **bit-identical** |
| P14 — two-route consistency `S·(R−1)·(ℱ·S−1) = (q_A_p + q_A_e + q_A_n)·α_H^S·D` | `56936 = 56936` | exact rational equality | PASS |

This is the load-bearing test. The typed reduction and CR221's component-by-component derivation arrive at `κ_floor = 7117/768` by structurally distinct routes, and they agree as exact rationals.

Per-check breakdown in `CR238_block_b_checks.csv`.

## Block C — CR232 Matter Gate Regrade from Typed Kernel

| Audit | Rows | Pass | Fail |
|---|---:|---:|---:|
| P15 — Matter gate `qA = M_obs·(1 + \|q\|/R²)`, `T = qA/S`, `W = (S−1)·qA/S` | 126 | 126 | 0 |
| P16 — Blocked rows have `M_obs = qA = T = W = 0` | 13 | 13 | 0 |
| P17 — Hidden-support surcharge `M_native = p + p²/R²` | 8 | 8 | 0 |

Every matter row reproduced the uploaded `qA_source_support`, `tensor_carrier_support`, and `retained_write_support` columns within tolerance `10⁻⁶` using the typed `R² = 144` and typed `S = 8` from the spine derivation. No literal `144` or `8` was used in the gate logic; both entered as typed primitives.

Per-row results in `CR238_matter_row_audit.csv`, `CR238_blocked_row_audit.csv`, `CR238_surcharge_audit.csv`.

## Block D — CR233 Role Identities From Typed Primitives

```text
checks_pass : 9 / 9
ROLE 1 (Θ = 18 = α_H · D²)   : derives from typed primitives
ROLE 2 (ℱ = 81)               : foundational atom by declaration
ROLE 3 (mirror face = ℱ = 81) : derives from ℒ − ℱ = ℱ
ROLE 4 (𝒱 = 27 = ℱ/D)         : derives from typed primitives
Cross identity (Θ² = R · 𝒱)   : verified, and reduces under typed substitution to D^4 = ℱ
```

Per-check breakdown in `CR238_block_d_checks.csv`.

## Block E — Substrate Uniqueness Scan

```text
P23 — agreeing positive integers D in [1, 12]:  [3]      (unique)
P24 — at D = 3, face axiom delivers ℱ = D^(D+1) = 3^4 = 81
```

Full scan table (`D^(D−1)` vs `S + 1 = 9` at canonical `S = 8`):

| D | D^(D−1) | S+1 | face_axiom_ℱ = D^(D+1) | radix_closure_ℱ = (S+1)·D² | agree |
|---:|---:|---:|---:|---:|---|
| 1 | 1 | 9 | 1 | 9 | no |
| 2 | 2 | 9 | 8 | 36 | no |
| 3 | 9 | 9 | 81 | 81 | **YES** |
| 4 | 64 | 9 | 1024 | 144 | no |
| 5 | 625 | 9 | 15625 | 225 | no |
| 6 | 7776 | 9 | 279936 | 324 | no |
| 7 | 117649 | 9 | 823543 | 441 | no |
| ... (monotonically diverging beyond D=3) |

`D^(D−1)` is monotonically non-decreasing for D ≥ 1 and strictly increasing for D ≥ 2, so D = 3 is the unique positive integer solution. Full scan in `CR238_uniqueness_scan.csv`.

The canonical substrate `{ℱ = 81, S = 8}` is structurally selected by the two axioms `{face, radix-closure}` rather than chosen. The dimensional readout `D = 3` and binary readout `α_H = 2` are forced.

## Block F — Primitive Typing Audit (Literal Scan)

```text
input_boundary  :  2    (the runner's single allowed input-declaration block)
allowed_section : 10    (scanner-configuration data list)
comparand       : 16    (test-assertion comparands)
injection       :  0    (raw-literal injections in functional code)
```

Zero unjustified raw-literal injections were detected in the runner's functional code. Every appearance of `{81, 18, 27, 126, 144, 162, 324, 647, 768, 7117, 64}` and the fractions `{1/12, 1/64, 7117/768}` was either:

- In the locked input declaration block (`ℱ = 81, S = 8, α_H = 2`), or
- In the scanner's own configuration list (`FORBIDDEN_INTEGER_LITERALS`), explicitly marked as an allowed section, or
- A comparand in a test-equality assertion (`assert kappa == sp.Rational(7117, 768)` style).

Per-occurrence categorization in `CR238_literal_scan.csv`. Detection uses Python's `tokenize` module (NUMBER tokens only — string literals, comments, and docstrings are skipped naturally) plus an explicit pass for fraction patterns `NUMBER '/' NUMBER`.

## Wrong Controls

All nine wrong controls broke exactly as the precommit predicted.

| WC | Description | Predicted | Observed |
|---|---|---|---|
| WC1 | ℱ → 80 face perturbation (S=8 locked) | BREAK | BREAK (D non-integer; κ ≠ 7117/768) |
| WC2 | ℱ=81, S → 7 split perturbation | BREAK | BREAK (D non-integer; κ ≠ 7117/768) |
| WC3 | ℱ=81, S → 9 split overshoot | BREAK | BREAK (D non-integer; κ ≠ 7117/768) |
| WC4 | α_H → 3 (binary readout violated) at ℒ=162 sealed | SELF-CONTRADICT | SELF-CONTRADICT (α_H_decl=3 ≠ α_H_derived=2; S_decl=8 ≠ S_derived=5) |
| WC5 | κ exponent α_H^(S±1) | BREAK both | BREAK both (κ ≠ 7117/768 for S−1 and S+1) |
| WC6 | g = 1/S instead of 1/S² | BREAK | BREAK (g = 1/8 ≠ 1/64) |
| WC7 | N(Z) mod form vs floor form | BREAK at non-radix Z | BREAK at Z = 2 (mod gives 13/6, floor gives 2) |
| WC8 | Raw-literal injection sentinel | ARITHMETIC PASSES, AUDIT FLAGS | AUDIT flagged the injection (1 hit on `7117/768`) |
| WC9 | D = 4 substrate attempt at S=8 | AXIOMS DISAGREE | AXIOMS DISAGREE (face=1024, radix=144) |

Full per-WC details in `CR238_wrong_controls.csv`.

## K-Gate Audit (Post-Execution)

| Gate | Status | Evidence |
|---|---|---|
| K1 | N/A | Internal substrate reduction; no outside-model contact |
| K2 | PASS | Pre-stated falsifiers (any P1–P25 failing, any WC failing to break, any literal injection that audit misses) — none occurred |
| K3 | PASS | Foundational atoms, typed spine, predictions, wrong controls, pass condition, and literal-scan protocol all locked in `CR238_PRECOMMIT.md` (sha `5e9161…`) BEFORE the runner read CR219 or derived any kernel value |
| K4 | PASS | Two foundational dimensionless atoms `{ℱ, S}` + one structural constant `α_H` + SHA-locked CR219 source. No other free integer or rational entered the runner |
| K5 | PASS | `python CR238_runner.py` deterministically recomputes every typed identity, every CR221/CR232/CR233 cross-check, every wrong control, and the literal-scan audit |

## Cryptographic Chain (Inputs)

```text
CR114_result.md (capacity R² + split-loss)                =  f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R²·9/8 closed ledger)              =  635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR221_result.md (kappa_floor = 7117/768; g_n = 1/64)      =  2fc932adda9df4e3002b6a996d321a072a009722801099747fae552c393fbeef
CR222_result.md (carrier ledger 12+1 closed sum)          =  b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity)            =  ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR230_result.md (raw generator test)                      =  3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR232_result.md (matter-support promotion gate)           =  f7840628755b0e4551c3e4e0d989a8f90c2acea9aae90ef2e3070af75f712e25
CR233_result.md (18/81/27 tensor-substrate roles)         =  55e0c81a8c417fb79f377f5913035d65a917ada0cca80e5cc9cdf8851fd55895
CR219_promoted_particle_rows_126.csv                      =  45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
CR238_PRECOMMIT.md                                        =  5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293

Source proposal documents (Sean Brady's reduction):
reduction.pdf                                             =  bc2c011f61e9f53e3f917a45dfdbd22762020bf2edb7f1cd94bbce7c20c5eb4d
reduction.docx                                            =  a9fcfaabef3a2b4d70e3cf4dfdcc63cbfd9587377a731356be7b9e1d3994bd7f
update.md                                                 =  6af870c9b2f6fd2f45186dbb9e3133dbd3262e422b441e72633ce940c0ee6199
```

## What CR238 Does

1. Declares `{ℱ, S}` as the only foundational dimensionless substrate atoms.
2. Derives `α_H = ℒ/ℱ = 2` (binary readout) and `D = √(ℱ/(S+1)) = 3` (dimensional readout) from `{ℱ, S}` plus the structural definitions in the typed spine.
3. Reproduces the CR221 frozen kernel constants `κ_floor = 7117/768` and `g_n = 1/64` bit-identically from the typed formulas.
4. Re-derives the CR114 cycle-budget identity (`R² = ℒ − Θ = 144`), CR217+CR229 closed-ledger identity (`ℒ = M + 2Θ`), CR232 matter gate (`qA = M_obs·(1+|q|/R²), T = qA/S, W = (S−1)·qA/S`), CR233 role identities, and the 1/8 split (`S = (ℒ−Θ)/Θ`) from typed primitives.
5. Asserts and verifies that D = 3 is the unique positive integer in [1, 12] satisfying the face and radix-closure axioms simultaneously.
6. Audits its own runner code via a tokenize-based literal scan and flags zero injection of substrate-primitive raw literals outside the locked input boundary.

## What CR238 Does NOT Do

- Does NOT modify any upstream sealed CR. CR114, CR217, CR221, CR222, CR229, CR230, CR232, CR233 remain frozen.
- Does NOT introduce new free parameters; foundational atom count is 2 dimensionless + 1 structural constant + 1 dimensional bridge.
- Does NOT claim the typed spine is preferred over any other internally-consistent representation; it claims that the typed spine and the prior representations agree bit-identically on every measured quantity.
- Does NOT extend to the QC line (QC001–QC006B+). A separate downstream restatement would carry the typed spine into the quantum-phase tests.
- Does NOT touch the numerical value of `μ_Q`. The kg-scale dimensional bridge is left unfit; CR238 only states the structural identity `m_i = m_g = μ_Q · Q`.

## Manuscript Implications

CR238 enables the following manuscript-grade restatements (subject to Sean's drafting choices):

1. **§0 substrate framing:** "The substrate has two foundational atoms `{ℱ, S}` whose dimensional and binary readouts `{D, α_H}` are derived: `D = √(ℱ/(S+1))`, `α_H = ℒ/ℱ`. At the canonical substrate `{ℱ = 81, S = 8}`, the readouts are `{D = 3, α_H = 2}`, and the structural identities `ℒ = α_H·ℱ = 162`, `𝒱 = ℱ/D = 27`, `Θ = α_H·D² = 18`, `R = α_H·ℒ/𝒱 = 12`, `R² = ℒ − Θ = 144`, `M = ℒ − 2Θ = 126`, `A_0 = 𝒱/(π·α_H·ℒ) = 1/(12π)` all derive without further input."

2. **§n element kernel:** "The carrier kernel coefficient is the closed-form expression `κ = (R−1)(ℱ·S − 1)/(D·α_H^S) = 7117/768`, and the neutron carrier unit is `g = 1/S² = 1/64`. Both reproduce CR221's frozen values bit-identically — the SOB element engine has no free parameters in its kernel coefficients."

3. **§n+1 substrate uniqueness:** "The substrate dimension D = 3 is the unique positive integer satisfying `D^(D−1) = S + 1` at canonical S = 8; equivalently, the only positive-integer dimension at which the face axiom `ℱ = D^(D+1)` and the radix-closure axiom `ℱ = (S+1)·D²` simultaneously hold. The canonical substrate is structurally selected."

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Inputs hash-locked. The typed spine, predictions P1–P25, wrong controls WC1–WC9, pass condition, K-gates, and falsifiers F1–F7 are frozen.

If any sealed upstream CR (CR114, CR217, CR221, CR222, CR229, CR230, CR232, CR233) is later regraded such that its frozen numerical value changes, CR238 must be re-examined and its bit-identical-match predictions re-verified.

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** Block A 31/31; Block B 3/3; Block C 126/126 + 13/13 + 8/8; Block D 9/9; Block E unique D = [3]; Block F injections = 0; Wrong controls 9/9 broke as predicted
**Foundational atom count:** 2 dimensionless (ℱ, S) + 1 structural constant (α_H = 2) + 1 dimensional bridge (μ_Q)
**Arc relation:** Downstream unification, not arc-internal
