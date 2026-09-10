# TEST 5 — BLIND SOB ELEMENT ENGINE — PRECOMMIT

**Date:** 2026-06-22
**Classification:** BLIND_GENERATE_THEN_REVEAL (the public-facing demonstration)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 (full Test 5 spec issued)
**Part of:** Seven-test ownership arc (Test 5 of 7)
**Status:** PRECOMMITTED before runner execution.

## Purpose

Build and test the no-name Substrate Order Block element engine.

The engine must generate the 126 element rows from SAM native constants only.

No element names, symbols, isotope anchors, measured masses, half-lives, abundance data, or external periodic-table information may be used before the prediction file is sealed.

The test question is:

```text
Can SAM generate the no-name element block from native constants alone, freeze it,
and only then reveal conventional element labels against it?
```

## Directory Tree (Locked)

```text
CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/
├── PRECOMMIT.md
├── run_test5_blind_sob_engine.py
├── outputs/
│   ├── test5_no_name_predictions.csv
│   ├── test5_internal_checks.json
│   ├── test5_internal_verdict.md
│   ├── test5_reveal_scored.csv              # created only after no-name hash
│   ├── test5_reveal_score_summary.json      # created only after no-name hash
│   └── test5_reveal_verdict.md              # created only after no-name hash
├── controls/
│   ├── R10_control.csv
│   ├── R11_control.csv
│   ├── R13_control.csv
│   ├── D2_control.csv
│   ├── D4_control.csv
│   ├── shuffled_Z_control.csv
│   └── random_clock_holes_control.csv
├── hashes/
│   ├── PRECOMMIT_CURRENT_HASH.txt
│   ├── run_test5_CURRENT_HASH.txt
│   ├── no_name_predictions_CURRENT_HASH.txt
│   └── reveal_outputs_CURRENT_HASH.txt
└── HASHES.txt
```

## Hard Rule — No Reveal Before Seal

The runner has two modes:

```bash
python run_test5_blind_sob_engine.py --mode generate
python run_test5_blind_sob_engine.py --mode reveal --reveal-csv path/to/reveal_reference.csv
```

The `generate` mode must not read any reveal file. The `generate` mode must not contain dictionaries of element names, symbols, measured masses, known isotopes, half-lives, or observed stability labels.

The generated file must use no-name row IDs only: `E001, E002, ..., E126`.

Only after `test5_no_name_predictions.csv` is written and hashed may the reveal mode run.

## Native Constants (Engine Inputs)

```text
alpha_H = 2
D       = 3
R       = 12
split   = 2^D = 8
R^2     = 144
Pi      = {1, 2, 3, 4, 6, 8, 9, 12}
kappa_floor = 7117/768
g_n     = 1/64
```

Derived constants:

```text
native_capacity   = R^2 * (1 - 1/split)         = 126
frontier_start    = 126 - 8 + 1                  = 119
T                 = R^2 / split                  = 18
Zc                = D^(D+1) = 3^4                = 81
H                 = 1+2+3+4+6+8+9+12             = 45
clock_boundary    = Zc + alpha_H                 = 83
clock_hole_1      = H - alpha_H                  = 43
clock_hole_2      = clock_hole_1 + T             = 61
```

## Z Range From Native Capacity

```text
Z = 1, 2, ..., 126
Row ID:  E001, E002, ..., E126
```

No hard-coded 126; capacity is generated from R and D.

## Neutron Rule

```text
radix_cycle    = floor((Z-1)/R) + 1
selected_depth = max(0, radix_cycle - 1)
delta_N        = floor(Z * selected_depth / R)
N              = Z + delta_N
A              = Z + N
```

## Particle Source Address

```text
P_{Z,N} = Zp + Nn + Ze
protons   = Z
neutrons  = N
electrons = Z
u_count   = 2Z + N
d_count   = Z + 2N
e_count   = Z
source_address_nucleon = "{Z}p + {N}n + {Z}e"
source_address_quark   = "{u}u + {d}d + {Z}e"
```

## Native Binding / Gravity Bridge

```text
G(P)            = Z * kappa_floor + (N - Z) * g_n
GR(P)           = 8 * G(P)
W(P)  retained  = 7 * G(P)
released        = G(P)
split_check     = |GR - (7G + G)|   must be < 1e-9
```

## Eight-Lane Carrier Stack

```text
lane_pG for p in {1, 2, 3, 4, 6, 8, 9, 12}
lane_8G  must equal GR(P)
lane_12G must equal R * G(P)
```

## Clock / Stability Face

```text
if Z in {43, 61}:        clock_state = "CLOCK_HOLE"
elif Z >= 119:           clock_state = "FRONTIER"
elif Z <= 83:            clock_state = "CLOCK_CLOSED"
else:                    clock_state = "RADIOACTIVE_OPEN"

Expected counts:
  81 CLOCK_CLOSED + 2 CLOCK_HOLE + 35 RADIOACTIVE_OPEN + 8 FRONTIER = 126
```

## Shell / Light Face

```text
C_n            = 2 * n^2
shell sequence = [2, 8, 18, 32, 50, 72, ...]
fill Z electrons into sequential shells
shell_capacity_vector = "2|8|18|32|50|72"
shell_fill_vector     = ...      (per row)
outer_shell_index, outer_shell_occupancy
```

## Required Audit Rows (Pre-Reveal Spot Check)

```text
E001: Z=1, N=1, A=2, u=3, d=3, e=1
E043: clock_state = CLOCK_HOLE
E061: clock_state = CLOCK_HOLE
E079: Z=79, N=118, A=197, u=276, d=315, e=79
E083: clock_state = CLOCK_CLOSED
E084: clock_state = RADIOACTIVE_OPEN
E118: clock_state = RADIOACTIVE_OPEN
E119: clock_state = FRONTIER
```

## Internal Checks (test5_internal_checks.json)

```text
row_count_is_126
native_capacity_is_126
frontier_start_is_119
clock_closed_count_is_81
clock_hole_count_is_2
radioactive_open_count_is_35
frontier_count_is_8
clock_holes_are_43_and_61
all_A_equal_Z_plus_N
all_quark_counts_match_formula
all_GR_equal_8G
all_retained_plus_released_equal_GR
all_lane8_equal_GR
all_lane12_equal_R_times_G
E079_N_A_quark_check
no_reveal_columns_present
```

Internal verdict `PASS_TEST5_INTERNAL_BLIND_SOB_ENGINE` only if all checks pass.

Failure classes:
`FAIL_TEST5_NATIVE_CAPACITY / FAIL_TEST5_ROW_COUNT / FAIL_TEST5_NEUTRON_RULE / FAIL_TEST5_SOURCE_ADDRESS / FAIL_TEST5_CLOCK_RULE / FAIL_TEST5_BINDING_SPLIT / FAIL_TEST5_LANE_STACK / FAIL_TEST5_REVEAL_LEAKAGE / FAIL_TEST5_AUDIT_ROW`.

## Hash Before Reveal

After generating the no-name outputs, sha256 them immediately and append to `HASHES.txt`. Reveal mode must refuse to run until those hashes are recorded.

## Reveal Mode

Reads an external reveal reference with columns:
`Z, symbol, name, external_anchor_A, external_anchor_N, external_stability_label, measured_mass_u`.

Joins on `Z`. Writes `outputs/test5_reveal_scored.csv`, `outputs/test5_reveal_score_summary.json`, `outputs/test5_reveal_verdict.md`.

Reveal scoring columns: `symbol, name, external_anchor_A, external_anchor_N, external_stability_label, measured_mass_u, N_match, A_match, clock_match, mass_reveal_only`.

```text
measured_mass_u is reveal-only.
Do not treat measured_mass_u as a derived SAM output.
Do not back-fit G_native to measured_mass_u.
```

## Reveal Score Summary

```json
{
  "rows_scored": 126,
  "N_match_count": "...",
  "A_match_count": "...",
  "clock_match_count": "...",
  "clock_closed_pred_count": 81,
  "clock_hole_pred_count": 2,
  "radioactive_open_pred_count": 35,
  "frontier_pred_count": 8,
  "stable_clock_holes": [43, 61],
  "measured_mass_used_as_input": false,
  "measured_mass_scored_as_derived": false
}
```

Possible reveal verdicts:
`PASS_TEST5_REVEAL_STRONG_MATCH / PASS_TEST5_REVEAL_PARTIAL_MATCH / FAIL_TEST5_REVEAL_WEAK_MATCH / FAIL_TEST5_REVEAL_INPUT_LEAK`.

## Wrong Controls

Run after the real generator. Each writes to `controls/`.

- **Control A — R = 10**: fail native capacity / row count / clock structure.
- **Control B — R = 11**: fail.
- **Control C — R = 13**: fail.
- **Control D — D = 2**: split / native capacity / clock boundary / carrier structure fail.
- **Control E — D = 4**: fail.
- **Control F — shuffled Z labels** (seed 20260621): reveal match metrics degrade.
- **Control G — random clock holes** (seed 20260621, replace {43,61} with two random <83): clock score degrades.

## Allowed Claims

If internal checks pass:

```text
SAM generated a no-name 126-row SOB element block from native constants alone,
including N, A, source address, clock state, shell face, and native binding scale.
```

If reveal scoring is strong:

```text
The sealed no-name SOB engine survived reveal against external element labels and anchor values.
```

The test MAY NOT claim:

```text
SAM derived measured atomic mass in u.
```

unless a separate native-to-physical mass conversion is added and sealed before reveal.

## Minimal Expected Headline (if successful)

```text
TEST5_PASS_BLIND_SOB_ELEMENT_ENGINE__126_ROWS__81_CLOCK_CLOSED__43_61_HOLES__NO_REVEAL_INPUTS
```

Public sentence:

```text
One integer Z enters; the no-name element block is generated, sealed,
and only then revealed against the conventional periodic table.
```

## Agent Warning

```text
Do not optimize anything after reveal.
Do not adjust the neutron rule after looking at reveal scores.
Do not rename failed reveal rows as exceptions unless an amend is created and sealed.
Do not add external data to the generator.

The test is only meaningful if the blind output is frozen before the reveal layer is attached.
```

## K-Gate Audit (Plan)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | Yes — reveal phase compares against external periodic-table reference (QP061-rooted) AFTER seal |
| K2 | Falsification | Any internal check failing falsifies; "PASS_REVEAL_STRONG" requires strong joint N+A+clock match; reveal verdict reports actual numbers honestly even if weak |
| K3 | Target hygiene | Targets locked here BEFORE the runner executes; reveal is read AFTER the no-name hash is recorded |
| K4 | Typed inputs | Native constants only for generate; external reveal CSV only for reveal phase |
| K5 | Reproduction on demand | Deterministic generate; seeded controls (F: shuffled Z seed 20260621; G: random clock holes seed 20260621) |

## Sequence in the Seven-Test Arc

Test 5 of 7. Tests 6-7 remain:
- CR235 (Test 6): qA/8 gravity bridge
- CR236@12a (Test 7): Paul Revere tomography

See `[[project-seven-test-ownership-arc-cr230-236]]`.
