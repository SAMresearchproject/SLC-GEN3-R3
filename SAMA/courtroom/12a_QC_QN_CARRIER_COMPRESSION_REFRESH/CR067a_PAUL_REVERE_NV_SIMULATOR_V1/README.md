# CR067a — Paul Revere NV-Center Simulator V1.0

**Copyright (c) 2026 Sean Brady. ALL RIGHTS RESERVED.**

Private research record. No license is granted for use, copying, modification, distribution, or commercialization. Any future commercialization is subject to the stewardship intent in `STEWARDSHIP.md` at the repository root.

---

## What this is

A classical software simulation of the Paul Revere protocol (CR065a) running on a faithful physics model of the NV⁻ ³A₂ ground-state triplet (nitrogen-vacancy center in diamond, neutrally charged variant). The simulator:

- Loads the SAM-native qutrit state with normalized amplitudes √(4/17), √(9/17), √(4/17) on the (|m_s = 0⟩, |m_s = +1⟩, |m_s = -1⟩) sublevels
- Evolves under the NV zero-field-splitting Hamiltonian with Lindblad-form T1/T2 decoherence
- Applies the letter-preserving drift gate that corrects envelope drift without disturbing carrier or sensor populations
- Demonstrates the refusal stack (no-cloning, premature-commit refusal)
- Evaluates 10 predictions and 7 wrong controls declared in `CR067a_PRECOMMIT.md`
- Emits a results CSV, a summary JSON, an evolution plot, and a human-readable result markdown

## Slot architecture

| slot | physical sublevel | role | structural weight | normalized probability |
|---|---|---|---|---|
| a — carrier | m_s = 0 | route identity, protected pre-commit | 1/4 | 4/17 |
| b — envelope | m_s = +1 | letter content, 9/8 surcharge | 9/16 | 9/17 |
| c — sensor | m_s = -1 | boundary stress readout | 1/4 | 4/17 |

The structural slot weights (1/4, 9/16, 1/4) sum to 17/16 = 1 + 1/α_H⁴ = (Born unity) + (letter increment). Renormalized for the qutrit, they give the probabilities (4/17, 9/17, 4/17).

## Files

| file | purpose |
|---|---|
| `CR067a_PRECOMMIT.md` | structural declaration, frozen before runner execution |
| `CR067a_declared_premises.json` | typed inputs from upstream hash-locked CRs |
| `paul_revere_nv_simulator_v1.py` | the runner |
| `requirements.txt` | Python dependencies |
| `README.md` | this file |
| **after first run:** | |
| `CR067a_results.csv` | row per protocol stage |
| `CR067a_summary.json` | pass/fail per prediction and wrong control |
| `CR067a_evolution_plot.png` | population vs time |
| `CR067a_result.md` | human-readable result |
| `HASHES.txt` | sha256 of all artifacts (to be written after runner) |

## How to run

Tested with Python 3.10+. From this directory:

```bash
pip install -r requirements.txt
python paul_revere_nv_simulator_v1.py
```

That's it. The runner prints progress, writes the four output artifacts next to itself, and exits with code 0 on success. The evolution plot is rendered headlessly (no display required) so it works in any environment.

## What it validates

- Protocol math closes on a faithful NV-physics simulator
- CR065a hardware spec specifications are implementable
- CR066a Born extension + letter increment is internally consistent
- Refusal stack mechanics are correctly specified
- Lindblad decoherence is properly applied (purity decreases monotonically)
- Unitary evolution is recovered in the no-decoherence limit

## What it does NOT validate

- That real NV hardware will reproduce the predicted behavior (requires Stage 2: empirical T2 contact against published NV measurements)
- That the T2_grav floor formula CR064a v1.1 (`T2_grav = 16πR⁴/(17ω_drive)`) matches empirical data (requires partner-lab Stage 4 measurement)
- Any patentable claim on its own (the patentable claims are the protocol architecture itself, in CR065a)
- Quantum advantage over existing platforms

## Stewardship

Per `STEWARDSHIP.md` at the repository root: if commercialization of this work generates revenue, that revenue is intended to fund humanitarian causes — housing, addiction recovery, charitable medical support, education and opportunity access, community charities, and environmental prosperity. Profit and care are not in tension in this design; profit is the *vector* by which care happens.

## Upstream dependencies

```text
A0-a_h-D                          foundation (R, D, α_H, A_0)
CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1
CR061a_SELECTION_LOCK
CR065a_PAUL_REVERE_IMPLEMENTATION_SPEC_V1
CR066a_BORN_EXTENSION_AND_LETTER_INCREMENT_V1
CR121_SAM_GRAVITY_MECHANISM_INTAKE
CR129b_MAGNITUDE_LOCK
```

All upstream artifacts are hash-locked and referenced by sha256 in `CR067a_declared_premises.json`. The runner is read-only with respect to all upstream artifacts.

## Contact

`sbnvh@missouri.edu`

Repository: `github.com/iwtbotiwtwot/The_Courtroom` (private)
