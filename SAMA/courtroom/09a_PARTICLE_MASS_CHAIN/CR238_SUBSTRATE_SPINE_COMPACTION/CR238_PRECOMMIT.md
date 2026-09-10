# CR238 Substrate Spine Compaction + Primitive Typing Audit — Precommit

**Date:** 2026-06-23
**Classification:** STRUCTURAL_REDUCTION_AND_TYPING_AUDIT (downstream unification of CR114 / CR217 / CR221 / CR222 / CR229 / CR232 / CR233)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-23 ("Lets see what happens", confirming the foundational framing "ℱ and S are foundational substrate atoms; D and αH are the dimensional and binary readouts extracted from them")
**Source documents:**
  - `c:/VS/quantum_phase/reduction.pdf` (typed substrate spine, sha `bc2c011f61e9f53e3f917a45dfdbd22762020bf2edb7f1cd94bbce7c20c5eb4d`)
  - `c:/VS/quantum_phase/reduction.docx` (Word source, sha `a9fcfaabef3a2b4d70e3cf4dfdcc63cbfd9587377a731356be7b9e1d3994bd7f`)
  - `c:/VS/quantum_phase/update.md` (earlier compaction note, sha `6af870c9b2f6fd2f45186dbb9e3133dbd3262e422b441e72633ce940c0ee6199`)
**Status:** PRECOMMITTED before runner execution.

## Scope

> **CR238 does not modify upstream CRs. It re-expresses them in typed form.**
> CR238 is not "moving the target." It reduces the number of primitives needed to emit the same sealed stack of CR114 / CR217 / CR221 / CR222 / CR229 / CR232 / CR233 results — bit-identically.

Reduce the substrate spine from an opaque inventory of structural constants `{R, A_0, R², ℒ, M, Θ, S, κ_floor, g_n, …}` to two foundational atoms `{ℱ, S}` plus one structural constant `α_H = 2` and one dimensional bridge `μ_Q`. Every other quantity must derive from these by a typed expression with no raw literal injection.

Then audit the derivation by verifying:

1. Every previously-sealed structural identity (CR114 cycle budget, CR217+CR222 closed ledger, CR229 inclusion-exclusion, CR232 matter gate, CR233 role separation) is reproduced bit-identically from the typed spine.
2. The numerically-frozen kernel constants (CR221 `κ_floor = 7117/768` and `g_n = 1/64`) are reproduced bit-identically by the typed kernel formulas.
3. The two structural axioms that the typed spine carries — face axiom `ℱ = D^(D+1)` and radix-closure axiom `ℱ = (S+1)·D²` — agree at exactly one positive-integer dimension, **D = 3**, which (with S held foundational at S = 8) forces `ℱ = 81` as the canonical substrate.

The reduction is a unification CR.

## Foundational Declaration

```text
Foundational atoms        :  ℱ  (substrate response face)
                             S  (release-share split)
Structural constant       :  α_H = ℒ / ℱ = 2   (binary readout: face count = two-sidedness)
Dimensional bridge        :  μ_Q                (kg/Q unit; the only kg-scale primitive)

Canonical realized values :  ℱ = 81, S = 8     ⇒ D = 3, α_H = 2
```

## Typed Spine (Locked)

```text
ℒ  =  α_H · ℱ           closed two-sided event        = 2 · 81  = 162
D  =  √(ℱ / (S + 1))    dimensional readout           = √(81/9) = 3
𝒱  =  ℱ / D             resolved cubic write cell     = 81/3    = 27   (equivalently 𝒱 = √(ℱ·(S+1)))
Θ  =  α_H · D²          tensor bridge                 = 2·9     = 18   (equivalently Θ = ℒ/(S+1) = 162/9 = 18)
R  =  α_H · ℒ / 𝒱       radix                         = 4D      = 12
M  =  ℒ − 2Θ            matter capacity               = 162−36  = 126
A_0     =  𝒱 / (π · α_H · ℒ)        minimum substrate share quantum   = 1/(12π)
A_share =  𝒱 / (α_H · ℒ)            share threshold                   = 1/12
A_side  =  𝒱 / (2 · α_H · ℒ)        per-face share                    = 1/24

Element engine:
  N(Z)    =  Z + ⌊(Z/R) · ⌊(Z−1)/R⌋⌋                   floor-form neutron rule
  κ       =  (R − 1)(ℱ·S − 1) / (D · α_H^S)            typed kernel coefficient   = 7117/768
  g       =  1 / S²                                     typed neutron unit         = 1/64
  G(Z,N)  =  Z · κ + (N − Z) · g                       carrier kernel
  Q(Z,N)  =  S · G(Z,N) = (S−1) · G + G                completed source write

Mass / gravity:
  m_i = m_g = μ_Q · Q(P)                               structural identity
  A_P(r)    =  2 · G_N · μ_Q · Q(P) / (c² · r)         exterior accumulation field
```

### Wall Version (one-glance summary)

```text
ℱ, S, α_H   →   D, ℒ, 𝒱, Θ, R, R², M, A_0, κ, g

with   ℱ = 81,   S = 8,   α_H = 2

emitting:
  D = 3,   ℒ = 162,   𝒱 = 27,   Θ = 18,   R = 12,
  R² = 144,   M = 126,   A_0 = 1/(12π)

typed kernel:
  κ  =  (R − 1)(ℱ·S − 1) / (D · α_H^S)   =   7117/768
  g  =  1/S²                              =   1/64
```

## Inputs (Hash-Locked at Execution)

```text
Source CSV         :  C:\VS\CR219_promoted_particle_rows_126.csv
Source SHA-256     :  45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Foundational atoms :  ℱ = 81, S = 8
Structural const   :  α_H = 2
```

No other inputs. The typed runner must produce every quantity below from `{ℱ, S, α_H, R(derived), D(derived)}` and a SHA-locked read of CR219 for the 126 matter-row gate check.

## Predictions (Precommitted)

### Block A — Typed structural identities (derive from {ℱ, S, α_H} alone)

- **P1** — Two-sidedness: `α_H = ℒ / ℱ = 2`.
- **P2** — Closed two-sided event: `ℒ = α_H · ℱ = 2 · 81 = 162`.
- **P3** — Dimensional readout: `D = √(ℱ / (S+1)) = √(81/9) = 3` (positive integer).
- **P4** — Cubic write cell: `𝒱 = ℱ / D = 81/3 = 27`; and equivalently `𝒱 = √(ℱ · (S+1)) = √729 = 27`.
- **P5** — Tensor bridge: `Θ = α_H · D² = 2 · 9 = 18`; and equivalently `Θ = ℒ / (S+1) = 162/9 = 18`.
- **P6** — Radix: `R = α_H · ℒ / 𝒱 = 4D = 12`.
- **P7** — Matter capacity: `M = ℒ − 2Θ = 162 − 36 = 126`; equivalently `M = R² − Θ = 144 − 18 = 126`. The matter capacity is what remains of the closed event after both tensor bridges (or equivalently, of the cycle budget after one bridge).
- **P8** — Closed ledger identity (rewrite of CR217 + CR229): `ℒ = M + 2Θ` ⇒ `162 = 126 + 18 + 18`. Each bridge counts once per face.
- **P9** — Cycle-budget identity (rewrite of CR114): `R² = ℒ − Θ` ⇒ `144 = 162 − 18`. The cycle budget (R² = 144) is the closed event minus one tensor bridge — the per-cycle write ceiling. **Distinct from matter capacity** (M = 126); in this branch `M ≠ R²`. The role separation is: `ℒ = 162` (closed two-sided event), `R² = 144` (cycle budget), `M = 126` (matter capacity), `Θ = 18` (tensor bridge).
- **P10** — Share split: `S = R² / Θ = (ℒ − Θ) / Θ = 144/18 = 8`. The 1/8 split is forced, not chosen.
- **P11** — Minimum substrate share: `A_0 = 𝒱 / (π · α_H · ℒ) = 1/(12π)`; `A_share = 1/12`; `A_side = 1/24`. One ratio, three readouts.

### Block B — Element-kernel bit-identical match against CR221 (the load-bearing test)

- **P12** — Typed κ reproduces CR221 frozen kappa_floor exactly:
  ```text
  κ_typed  =  (R − 1)(ℱ·S − 1) / (D · α_H^S)
           =  11 · (81 · 8 − 1) / (3 · 2^8)
           =  11 · 647 / (3 · 256)
           =  7117 / 768
           =  9.266927083333… (repeating)
  CR221    :  kappa_floor = 7117/768 = 9.266927083333… ✓ bit-identical
  ```
- **P13** — Typed g reproduces CR221 frozen neutron_G_unit exactly:
  ```text
  g_typed  =  1 / S²  =  1/64  =  0.015625
  CR221    :  neutron_G_unit = 0.015625 ✓ bit-identical
  ```
- **P14** — Internal-consistency identity (two routes to the same fraction):
  ```text
  S · (R − 1) · (ℱ · S − 1)  =  (proton_qA + electron_qA + neutron_qA) · α_H^S · D
  8 · 11 · 647               =  (charged_pair_qA + 1/8) · 256 · 3
  56936                      =  (7117/96) · 768  =  56936  ✓
  ```
  The typed reduction and CR221's component-decomposition derive the same fraction by two structurally distinct routes; they must agree, and they do.

### Block C — Sample regrade of CR232 matter gate from typed kernel

- **P15** — Q(Z,N) = S · G(Z,N) reproduces the uploaded q_A column on every matter row in the SHA-locked CR219 source, within tolerance 1e-6.
  - Matter rows checked: 126 / 126 expected exact (already shown in CR232 at numerical-kernel level; CR238 verifies it also holds at typed-kernel level with κ and g substituted by their typed forms).
- **P16** — Blocked rows: `G_matter = 0 ⇒ M_obs = qA = T = W = 0` holds for all 13 blocked rows (5 carrier-only + 8 hidden-source-support). Typed reduction does not weaken the gate.
- **P17** — Hidden-support surcharge `M_native = p + p²/R² = p + p²/144` reproduces on all 8 hidden-support rows. `R² = 144` enters here as the typed `R²`, not a literal.

### Block D — Sample regrade of CR233 role identities from typed primitives

- **P18** — ROLE 1 (tensor bridge): `Θ = 18 = α_H · D²` ⇒ derives from typed primitives, no literal injection.
- **P19** — ROLE 2 (carrier-response face one-side): `ℱ = 81` is THE foundational atom, by declaration.
- **P20** — ROLE 3 (record mirror): the mirror face has size `ℱ = 81` (the other face in the two-sided event ℒ = 2ℱ).
- **P21** — ROLE 4 (3D write cell): `𝒱 = ℱ / D = 27`.
- **P22** — Cross identity (CR233): `Θ² = R · 𝒱` ⇒ `18² = 12 · 27 = 324`. In typed form:

  ```text
  (α_H · D²)²  =  (α_H · ℒ / 𝒱) · 𝒱
  α_H² · D^4   =  α_H · ℒ                  (1)

  Since ℒ = α_H · ℱ, substitute into (1):
  α_H² · D^4   =  α_H · (α_H · ℱ)
  α_H² · D^4   =  α_H² · ℱ

  Cancel α_H² (≠ 0):
  D^4          =  ℱ                         (2)
  ```

  At D = 3: `D^4 = 3^4 = 81 = ℱ` ✓. The cross identity reduces, after typed substitution, to the face axiom `ℱ = D^(D+1)` specialized at D=3 (where D+1 = 4).

### Block E — Substrate uniqueness (the deep prediction)

The typed spine carries two structural axioms:

```text
Face axiom            :  ℱ  =  D^(D+1)         (CR222 / CR233 ROLE 2 derivation)
Radix-closure axiom   :  ℱ  =  (S+1) · D²      (equivalent to R² = ℒ − Θ with
                                                R = 4D, ℒ = α_H·ℱ = 2ℱ, Θ = α_H · D² = 2D²;
                                                the (S+1) factor exposes that what would
                                                otherwise be hard-coded as "9" is structurally
                                                S+1 at canonical S = 8)
```

Equality of the two axioms requires:

```text
D^(D+1)  =  (S+1) · D²
D^(D−1)  =  S + 1
```

S is held foundational (Sean's framing: S is a substrate atom, not a derived closure of D). At canonical `S = 8`, the equality reduces to `D^(D−1) = 9`. Scan over positive integers D ∈ {1, …, 12}:

```text
D =  1 :  D^(D−1) = 1^0    = 1.        1 ≠ 9.       DISAGREE
D =  2 :  D^(D−1) = 2^1    = 2.        2 ≠ 9.       DISAGREE
D =  3 :  D^(D−1) = 3^2    = 9.        9 = 9.       AGREE  ← canonical
D =  4 :  D^(D−1) = 4^3    = 64.       64 ≠ 9.      DISAGREE
D =  5 :  D^(D−1) = 5^4    = 625.      625 ≠ 9.     DISAGREE
D =  6 :  D^(D−1) = 6^5    = 7776.     7776 ≠ 9.    DISAGREE
D =  7 :  D^(D−1) = 7^6    = 117649.   117649 ≠ 9.  DISAGREE
... (grows monotonically; no integer D > 3 makes D^(D−1) = 9)
```

`D^(D−1)` is monotonically non-decreasing for D ≥ 1 and strictly increasing for D ≥ 2, so D = 3 is the **unique** positive integer solution.

Selection chain (S-foundational form, consistent with the file):

```text
S = 8   ⇒   D^(D−1) = 9   ⇒   D = 3   ⇒   ℱ = D^(D+1) = 3^4 = 81
```

- **P23** — D = 3 is the unique positive integer dimension D ∈ {1, …, 12} satisfying `D^(D−1) = S + 1` at canonical `S = 8`. The canonical dimensional readout is structurally selected by the substrate atoms `{ℱ_axiom, S}`, not chosen.
- **P24** — At D = 3, the face axiom delivers `ℱ = D^(D+1) = 81`. With S = 8 held foundational, the canonical substrate is `{ℱ = 81, S = 8}` with readouts `{D = 3, α_H = 2}`.

Note (framing hygiene): the file treats `S = 8` as a foundational atom throughout. The alternative framing `S = D² − 1` (with D foundational instead of S) is not used here; it is mentioned only as a "stronger form" of the uniqueness statement, not as the operative framing. Wrong controls that vary S (WC2, WC3) are valid because S is foundational. Wrong controls that vary D directly (WC1 via ℱ perturbation, WC9 via D=4 substrate attempt) test the radix-closure axiom by holding S fixed and checking that no other D satisfies both axioms.

### Block F — Primitive typing audit (the literal-injection sentinel)

- **P25** — Across the CR238 runner code, every appearance of any value in `{81, 162, 27, 144, 126, 18, 8, 1/12, 1/64, 7117/768}` must be sourced from a typed expression on `{ℱ, S, α_H}` (or downstream typed primitives derived from them).

  **Allowed exception — single input declaration.** The foundational atoms may appear as literals in exactly one place: the input declaration block

  ```text
  ℱ = 81,   S = 8,   α_H = 2
  ```

  This single declaration is the runner's input boundary. The literal-scan audit must:
  (a) confirm exactly one such declaration exists,
  (b) record it as the input source rather than flagging it as an injection, and
  (c) verify that every other appearance of `{81, 162, 27, 144, 126, 18, 8, 1/12, 1/64, 7117/768}` in the runner is a typed expression derived from `{ℱ, S, α_H}`.

  Any line outside the input declaration that introduces one of these values as a raw literal must be flagged in `CR238_literal_scan.csv` with reason and either justified (e.g., test-equality assertion comparing typed value against expected) or fixed.

## Wrong Controls (Precommitted)

- **WC1 — Face perturbation, split locked.** Set `ℱ → 80` with `S = 8`. Then `D = √(80/9) ≈ 2.981`, non-integer; `R = 4D ≈ 11.92`, non-integer; `κ = (R−1)(80·8−1)/(D·α_H^S)` breaks bit-identical match with CR221's `7117/768`. Expected: ALL TYPED IDENTITIES BREAK; geometric integers lost.

- **WC2 — Split perturbation, face locked.** Set `ℱ = 81` with `S → 7`. Then `D = √(81/8) ≈ 3.182`, non-integer; `Θ = α_H·D² ≈ 20.25`; `R = 4D ≈ 12.73`; `κ = (11)(81·7−1)/(3.182·2^7) = 11·566/407.3 ≈ 15.29`, no longer `7117/768`. Expected: BREAK.

- **WC3 — Split overshoot.** Set `ℱ = 81` with `S → 9`. Then `D = √(81/10) ≈ 2.846`, non-integer; identities break. Expected: BREAK.

- **WC4 — α_H ≠ 2 (binary readout violated).** Force `α_H = 3` at fixed `{ℱ=81, S=8}`. Then `Θ = 3·9 = 27`; `R = α_H·ℒ/𝒱 = 3·162/27 = 18 ≠ 4D = 12`; `S = (ℒ−Θ)/Θ = 135/27 = 5 ≠ 8`. Internal inconsistency: declared S=8 contradicts derived S=5. Expected: SYSTEM SELF-CONTRADICTS.

- **WC5 — κ exponent variation (literal vs typed test).** At canonical `{ℱ=81, S=8, α_H=2, D=3}`, replace exponent S in `α_H^S` with `S−1 = 7` and `S+1 = 9`. Numerator unchanged (still ℱ·S−1 = 647). Denominator changes to `2^7·3 = 384` and `2^9·3 = 1536`. Then κ becomes `7117/384 ≈ 18.53` and `7117/1536 ≈ 4.63` respectively, neither matching CR221's `7117/768`. Expected: BREAK both directions.

- **WC6 — g exponent variation.** Replace `g = 1/S²` with `g = 1/S` (one power lower). Then `g = 1/8 = 0.125 ≠ 0.015625`. CR221's `neutron_G_unit` match breaks; CR064a residual range on every neutron-excess row (Z ≥ 2 with N > Z) blows up. Expected: BREAK.

- **WC7 — N(Z) form swap.** Replace floor form `N(Z) = Z + ⌊(Z/R)·⌊(Z−1)/R⌋⌋` with mod form `N(Z) = Z + (Z/R)·((Z−1) mod R)`. At Z = 2: floor gives N=2 (matches He-4); mod gives N = 2 + 1/6 ≈ 2.167 (non-integer, fails to match). Expected: BREAK at any Z with `(Z−1) mod R ≠ 0` that is not also a radix multiple.

- **WC8 — Raw-literal injection sentinel.** Take one site in the runner that currently uses a typed expression for a value in `{81, 162, 27, 144, 126, 18, 8, 1/64, 7117/768}` and replace it with the literal integer or fraction. Downstream arithmetic still passes (same numerical value), but `CR238_literal_scan.csv` must flag the injection. Expected: ARITHMETIC PASSES, AUDIT FLAGS. This tests the typing audit's discriminating power, not the spine's arithmetic.

- **WC9 — Uniqueness control (D = 4 substrate attempt).** Try `D = 4` with `ℱ` chosen to satisfy the face axiom (`ℱ = D^(D+1) = 4^5 = 1024`) and check whether the radix-closure axiom can also be satisfied with the same `ℱ` at canonical `S = 8`. Radix-closure demands `ℱ = (S+1)·D² = 9·16 = 144 ≠ 1024`. Equivalently, `D^(D−1) = 4^3 = 64 ≠ 9 = S+1`. Expected: AXIOMS DISAGREE; D = 4 substrate is structurally inconsistent at S = 8 (no shared `ℱ` makes both axioms hold).

## Pass Condition

```text
PASS iff:

  Block A (P1–P10)    :  hold as exact rationals
  Block A (P11)       :  holds as an exact symbolic π-normalized identity
                         (A_0 = 1/(12π) is not rational; A_share = 1/12 and A_side = 1/24 are)
  Block B (P12–P14)   :  typed κ = 7117/768 and typed g = 1/64 match CR221 bit-identically;
                         the two-route equality 56936 = 56936 holds
  Block C (P15–P17)   :  CR232 matter gate, blocked rows, hidden-support surcharge all
                         reproduced from the typed kernel on the SHA-locked CR219 source
                         (tolerance 1e-6, matching CR232's display precision)
  Block D (P18–P22)   :  CR233 role identities all derive from typed primitives
  Block E (P23–P24)   :  face + radix-closure axioms agree only at D = 3 among positive integers
                         in scan range D ∈ {1, …, 12}; canonical {ℱ=81, S=8} pinned at D=3
  Block F (P25)       :  CR238_literal_scan.csv contains no unjustified raw-literal injections;
                         each flagged literal is either an equality-assertion comparand or fixed

AND

  All nine wrong controls (WC1–WC9) break exactly as predicted, with WC8 the discriminator
  test (arithmetic passes, audit flags injection).

FAIL otherwise.
```

## K-Gate Audit (Precommitted Pre-Execution)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | N/A — internal substrate reduction; no outside-model contact |
| K2 | Falsification | Any P1–P25 failing as stated; any WC1–WC9 failing to break in the stated direction; any literal injection that audit fails to flag |
| K3 | Target hygiene | Foundational atoms, typed spine, predictions, wrong controls, pass condition, and literal-scan auditing protocol all locked here BEFORE the runner reads CR219 or computes any kernel value |
| K4 | Typed inputs | Two foundational atoms (ℱ, S), one structural constant (α_H), SHA-locked CR219 source. No other free integer or rational enters the runner |
| K5 | Reproduction on demand | `python CR238_runner.py` recomputes every typed identity, every CR221/CR232/CR233 cross-check, every wrong control, and the literal-scan audit in deterministic fashion |

## Falsifiers (Made Explicit)

- **F1**: Any of `{ℒ, D, 𝒱, Θ, R, M, A_0, A_share, A_side, κ, g}` failing to derive bit-identically from `{ℱ, S, α_H}` by the typed expressions in §"Typed Spine."
- **F2**: Typed `κ ≠ 7117/768` or typed `g ≠ 1/64`. (CR221 frozen values are the load-bearing match.)
- **F3**: The two-route identity `S · (R−1) · (ℱ·S − 1) = (proton_qA + electron_qA + neutron_qA) · α_H^S · D` failing as an exact rational equality.
- **F4**: Any CR232 matter row (any of the 126) failing `Q(Z,N) = S · G(Z,N)` with typed κ and typed g, within tolerance 1e-6.
- **F5**: Any positive integer D in {1, …, 12} other than 3 satisfying `D^(D−1) = S + 1` at canonical `S = 8` (equivalently, simultaneously satisfying the face axiom `ℱ = D^(D+1)` and the radix-closure axiom `ℱ = (S+1)·D²` with S held at its foundational value 8).
- **F6**: The literal-scan audit failing to flag the WC8 raw-literal injection.
- **F7**: Any wrong control (WC1–WC7, WC9) failing to break in the precommitted direction.

## Upstream Sources (Hash-Locked)

```text
CR114_result.md (capacity R² + split-loss identity)              =  f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R²·9/8 closed ledger identity)            =  635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR221_result.md (kappa_floor = 7117/768; neutron_G_unit = 1/64)  =  2fc932adda9df4e3002b6a996d321a072a009722801099747fae552c393fbeef
CR222_result.md (carrier ledger 12+1 closed sum)                 =  b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity)                   =  ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR230_result.md (raw generator test)                             =  3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR232_result.md (matter-support promotion gate audit)            =  f7840628755b0e4551c3e4e0d989a8f90c2acea9aae90ef2e3070af75f712e25
CR233_result.md (18/81/27 tensor-substrate role separation)      =  55e0c81a8c417fb79f377f5913035d65a917ada0cca80e5cc9cdf8851fd55895
CR219_promoted_particle_rows_126.csv                             =  45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f

Source proposal documents (Sean Brady's reduction):
reduction.pdf  =  bc2c011f61e9f53e3f917a45dfdbd22762020bf2edb7f1cd94bbce7c20c5eb4d
reduction.docx =  a9fcfaabef3a2b4d70e3cf4dfdcc63cbfd9587377a731356be7b9e1d3994bd7f
update.md      =  6af870c9b2f6fd2f45186dbb9e3133dbd3262e422b441e72633ce940c0ee6199
```

All upstream CRs are read-only. CR238 does not modify any prior result. If any upstream CR is later regraded, CR238 must be re-examined.

## Sequence Position

CR238 is **not** part of the Seven-Test Ownership Arc (CR230–CR236). It is a downstream structural-unification CR that follows the arc's substrate-side conclusions (CR229 inclusion-exclusion, CR232 matter gate, CR233 role separation) and the CR221 kappa derivation, and compacts them into a typed spine with two foundational atoms.

Relation to surrounding work:
- **Upstream (read-only inputs):** CR114, CR217, CR221, CR222, CR229, CR230, CR232, CR233.
- **Does NOT regrade:** any of the above. It re-expresses them in typed form.
- **Enables (if CR238 passes):** a Particles_Carriers manuscript spine in 14 lines, two foundational atoms, one structural constant, one dimensional bridge. The "wall version" of SAM.

## What CR238 Does

1. Declares `{ℱ, S}` as the only dimensionless foundational atoms (with `α_H = 2` as the binary readout, i.e., a structural constant of two-sidedness).
2. Specifies the typed spine derivations for every previously-named structural scalar.
3. Verifies the typed kernel reproduces CR221's frozen κ_floor and g_n bit-identically.
4. Re-derives the CR229, CR232, CR233 identities from the typed primitives.
5. Asserts and tests that D = 3 is the **unique** positive integer dimension where the face axiom and radix-closure axiom coincide, structurally selecting the canonical substrate.
6. Provides a literal-scan audit that flags any raw-literal injection in code (testing the typing, not the arithmetic).

## What CR238 Does NOT Do

- Does NOT modify any upstream sealed CR.
- Does NOT introduce new free parameters.
- Does NOT claim that the typed spine is preferred over any other internally-consistent representation; it claims that the typed spine and the prior representations agree bit-identically on every measured quantity, with the typed spine using strictly fewer foundational atoms.
- Does NOT extend to the QC line (QC001–QC006B+) — that's a separate downstream restatement.
- Does NOT touch the m_i = m_g = μ_Q · Q(P) measured-mass equality at the numerical scale (μ_Q is left as an unfit dimensional bridge; CR238 only states the structural identity, not the numerical value of μ_Q).

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady (foundational framing locked: "ℱ and S are foundational substrate atoms; D and αH are the dimensional and binary readouts extracted from them").

Inputs hash-locked. The typed spine, predictions P1–P25, wrong controls WC1–WC9, pass condition, K-gates, and falsifiers F1–F7 are frozen before runner execution.

If any sealed upstream CR (CR114, CR217, CR221, CR222, CR229, CR230, CR232, CR233) is later regraded such that its frozen numerical value changes, CR238 must be re-examined and its bit-identical-match predictions re-verified.

---

**Precommit drafted by:** Claude (Opus 4.7, 1M context), at Sean's direction
**Sealed by:** Sean Brady, 2026-06-23 [pending Sean's seal]
**Arc relation:** Downstream unification, not arc-internal
**Foundational atom count:** 2 dimensionless (ℱ, S) + 1 structural constant (α_H = 2) + 1 dimensional bridge (μ_Q)
