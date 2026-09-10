# CR218 Hidden Source Bigrade Derivation

## Task

Test whether the sealed 8-row hidden_source_support_rows partition set
`{1, 2, 3, 4, 6, 8, 9, 12}` is exactly reproduced by a single rule on a
single primitive set:

```
enumerate p = alpha_H^a * D^b for a, b in {0, 1, 2, ...}
include p iff lift(p) = p^2 / R^2 <= 1
equivalently:  include p iff p <= R
```

with `alpha_H = 2`, `D = 3`, `R = 12`, `R^2 = 144`.

This converts the set `{1, 2, 3, 4, 6, 8, 9, 12}` from an enumerator
output to a *derived* output of two sealed primitives and one bound rule.

## Origin

CR217 established that the lift formula `m(p) = p + p^2/R^2` fires exactly
on the hidden_source bin. The open lead from CR217 was whether the
hidden_source partition set is derived or hand-picked. CR218 tests
SeanBrady's hypothesis that the set is exactly the bigrade-lattice
elements `{2^a * 3^b : a, b >= 0, p <= R}`.

## Classification

Combinatorial closure test. CR218 enumerates a finite set deterministically
from sealed primitives and compares to a sealed observation. There is no
fitting, no free parameter, no tolerance.

## Inputs (hash-verified at runtime)

- `09a_PARTICLE_MASS_CHAIN/CR214_CR119_PARTICLE_COMPLEMENT_PATTERN_AUDIT/CR214_particle_complement_195.csv`
  sha256 `e41016b5b6b2a4ce68bdb0cbeb1cb8502d40dac34867de690177f6f92f443545`
- `09a_PARTICLE_MASS_CHAIN/CR216_CARRIER_DUPLICATE_RETIREMENT/CR216_particle_complement_194_active.csv`
  sha256 `01e780c0fbb315d0aaf93cc6b060ffc4c9cfd0da29ab7155b4da8ca40d444179`
- `09a_PARTICLE_MASS_CHAIN/CR217_DEDUP_STRUCTURAL_IDENTITY_AUDIT/CR217_summary.json`
  sha256 `375e458b34e215b5ff500e9da3305286df8b9634dcc5388ed018ba762a8ee06d`
- `02_A_KERNEL_WEAK_FIELD/README.md`
  sha256 `317081ed0425f71cf885bf024aadae1ee4ab8abb7a217cec8b6de419f84cc6cc`
  (carries `alpha_H = 2` at derivation grade)

## Sealed Primitives Carried In

- `alpha_H = 2` (sealed in `02_A_KERNEL_WEAK_FIELD/README.md` and propagated
  through generator outputs G219, G305, G312 and CR142 runner; cited at
  derivation grade from PR Sec 2.3).
- `D = 3` (closure_depth on every carrier and hidden_source row).
- `R = 12`, `R^2 = 144` (used in CR213, CR214, CR217, SAMs_TOE glossary).

These are not derived inside CR218. They are inputs.

## Pass Conditions

### Main rule (the hypothesis under test)

- The predicted set
  `P_main = { 2^a * 3^b : a, b in Z_{>=0} AND 2^a * 3^b <= R }`
  equals `{1, 2, 3, 4, 6, 8, 9, 12}` exactly.
- The observed set
  `P_obs = sealed partition_signature values from CR214's
   hidden_source_support_rows bin`
  equals `{1, 2, 3, 4, 6, 8, 9, 12}` exactly.
- `P_main == P_obs` (set equality: no extras in P_main, no omissions from P_main).

### Wrong controls (all must fail set-equality, i.e. all must differ from P_obs)

- `WC1: P = { 2^a * 3^b : p <= R^2 = 144 }` must have 23 elements and
  differ from P_obs. Specifically the elements `{16, 18, 24, 27, 32, 36,
  48, 54, 64, 72, 81, 96, 108, 128, 144}` must be present in WC1 and
  absent from P_obs.
- `WC2: P = { p in Z_{>0} : p <= R }` must have 12 elements and differ
  from P_obs. Specifically `{5, 7, 10, 11}` must be present in WC2 and
  absent from P_obs.
- `WC3: P = { 2^a * 3^b : p < R }` (strict, lift < 1 not lift <= 1) must
  have 7 elements and differ from P_obs. Specifically `{12}` must be
  present in P_obs and absent from WC3.

If any wrong control accidentally matches P_obs, the main rule loses its
discriminating power. CR218 fails in that case.

## Non-Promotion Rule

- CR218 establishes that the hidden_source partition set is set-theoretically
  equivalent to a bigrade-lattice rule. It does not derive *why* the
  upstream enumerator (CR119 / LC04 generator suite) chose the bigrade
  lattice or the `p <= R` bound. Those are separate questions.
- The match with `lift <= 1` as the bound is recorded as a backed
  observation linking CR217's lift formula to this derivation. It is not
  promoted to a claim that "lift bound *causes* the set boundary"; only
  that the boundary and the lift unity-line coincide on the sealed data.

## Outputs

- `CR218_runner.py`
- `CR218_declared_premises.json`
- `CR218_input_manifest.csv`
- `CR218_bigrade_enumeration.csv`     (the full a,b -> p table up to R^2)
- `CR218_set_comparison.csv`          (P_main vs P_obs side by side)
- `CR218_wrong_controls.csv`          (WC1, WC2, WC3 with pass/fail)
- `CR218_summary.json`
- `CR218_result.md`
- `HASHES.txt`
