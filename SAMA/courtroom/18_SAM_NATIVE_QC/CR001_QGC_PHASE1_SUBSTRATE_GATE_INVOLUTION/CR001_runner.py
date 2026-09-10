"""
CR001 — QGC Phase 1: Substrate Gate Involution End-to-End

Executes the locked program from CR001_PRECOMMIT.md against a
substrate-write simulation implementing LCQC003 gate algebra +
LCQC008 measurement, and verifies the end-to-end composition matches
the locked per-step expected state.

Also runs 5 wrong controls and verifies each produces its predicted
broken output.
"""

import csv
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


# ── Locked substrate atoms (read-only from CR238 / LCQC000-008) ──────

R = 12
D = 3
S = 8                       # = α_H ** D
ALPHA_H = 2
S_SQUARED = S * S           # = 64; LCQC004a gate-size
N_MAX = 61_312              # LCQC004 locked Substrate Coherence Ceiling

RESIDUAL_PAIR = (9, 12)     # LCQC002 / LCQC003 §4.6 residual pair


# ── LCQC001 state object ─────────────────────────────────────────────

@dataclass
class State:
    face_index: int            # 1..81 (CR114 ledger face position)
    alpha_h_label: Any         # 0, 1, or '?' (unresolved)
    status: str                # 'resolved' or 'unresolved'
    cumulative_writes: int     # substrate-write budget consumed

    def copy(self) -> 'State':
        return State(
            face_index=self.face_index,
            alpha_h_label=self.alpha_h_label,
            status=self.status,
            cumulative_writes=self.cumulative_writes,
        )

    def as_row(self, step: int, op: str) -> Dict[str, Any]:
        return {
            'step': step,
            'op': op,
            'face_index': self.face_index,
            'alpha_h_label': self.alpha_h_label,
            'status': self.status,
            'cumulative_writes': self.cumulative_writes,
        }


# ── LCQC003 gate primitives ──────────────────────────────────────────

def apply_identity(state: State) -> State:
    new = state.copy()
    new.cumulative_writes += S_SQUARED
    return new


def apply_binary_flip(state: State) -> State:
    """LCQC003 §2 Question 2: binary flip B.

    Flips alpha_H label 0 ↔ 1 for resolved state; identity on unresolved.
    """
    new = state.copy()
    if state.status == 'resolved':
        new.alpha_h_label = 1 - state.alpha_h_label
    # else: unresolved — leave label as '?'
    new.cumulative_writes += S_SQUARED
    return new


def apply_substrate_gate(state: State) -> State:
    """LCQC003 §4.6: substrate gate 𝒢_sub.

    Swaps face_index 9 ↔ 12; identity on all other faces.
    Does NOT affect alpha_H label or status.
    """
    new = state.copy()
    if state.face_index == 9:
        new.face_index = 12
    elif state.face_index == 12:
        new.face_index = 9
    # else: identity on non-residual-pair faces
    new.cumulative_writes += S_SQUARED
    return new


def apply_measure(state: State, deterministic_result: Optional[int] = None) -> State:
    """LCQC008: measurement = G_matter promotion event.

    Resolves unresolved alpha_H label to a definite value.
    Idempotent on already-resolved states.
    deterministic_result: for unresolved superposition states, the runner
       provides the expected resolved value (Born-rule outside CR001 scope).
       For resolved states, this argument is ignored.
    """
    new = state.copy()
    if state.status == 'unresolved':
        if deterministic_result is None:
            raise ValueError(
                'CR001 expects resolved input or explicit deterministic_result '
                'for MEASURE; Born-rule statistics out of scope'
            )
        new.alpha_h_label = deterministic_result
        new.status = 'resolved'
    # else: idempotent
    new.cumulative_writes += S_SQUARED
    return new


# ── Program executor ─────────────────────────────────────────────────

def execute_program(initial: State, ops: List[str]) -> (State, List[Dict[str, Any]]):
    """Execute a program (list of operation names) against an initial state.

    Returns (final_state, trace_rows).
    """
    trace: List[Dict[str, Any]] = []
    state = initial.copy()
    trace.append(state.as_row(0, 'INIT'))
    for step, op in enumerate(ops, start=1):
        if op == 'G_sub':
            state = apply_substrate_gate(state)
        elif op == 'B':
            state = apply_binary_flip(state)
        elif op == 'I':
            state = apply_identity(state)
        elif op == 'MEASURE':
            state = apply_measure(state)
        else:
            raise ValueError(f'unknown op: {op!r}')
        trace.append(state.as_row(step, op))
    return state, trace


# ── Main program (from CR001_PRECOMMIT.md §"Locked program") ────────

MAIN_PROGRAM = ['G_sub', 'B', 'G_sub', 'B', 'MEASURE']

MAIN_INITIAL = State(face_index=9, alpha_h_label=0, status='resolved',
                     cumulative_writes=0)

MAIN_EXPECTED_PER_STEP = [
    # step, face, alpha_h, status, budget
    (0, 9, 0, 'resolved', 0),
    (1, 12, 0, 'resolved', S_SQUARED),
    (2, 12, 1, 'resolved', 2 * S_SQUARED),
    (3, 9, 1, 'resolved', 3 * S_SQUARED),
    (4, 9, 0, 'resolved', 4 * S_SQUARED),
    (5, 9, 0, 'resolved', 5 * S_SQUARED),
]


# ── Wrong controls ───────────────────────────────────────────────────

WRONG_CONTROLS = [
    {
        'id': 'WC-1',
        'description': 'drop one 𝒢_sub (omit step 3)',
        'initial': State(9, 0, 'resolved', 0),
        'ops': ['G_sub', 'B', 'B', 'MEASURE'],
        'expected_final_face': 12,
        'expected_final_alpha_h': 0,
        'expected_break_field': 'face_index',
    },
    {
        'id': 'WC-2',
        'description': 'extra 𝒢_sub (3 swaps total)',
        'initial': State(9, 0, 'resolved', 0),
        'ops': ['G_sub', 'B', 'G_sub', 'B', 'G_sub', 'MEASURE'],
        'expected_final_face': 12,
        'expected_final_alpha_h': 0,
        'expected_break_field': 'face_index',
    },
    {
        'id': 'WC-3',
        'description': 'non-residual face (init face=4)',
        'initial': State(4, 0, 'resolved', 0),
        'ops': ['G_sub', 'B', 'G_sub', 'B', 'MEASURE'],
        'expected_final_face': 4,
        'expected_final_alpha_h': 0,
        'expected_break_field': 'face_index',
    },
    {
        'id': 'WC-4',
        'description': 'measure-first (before any gates)',
        'initial': State(9, 0, 'resolved', 0),
        'ops': ['MEASURE', 'G_sub', 'B', 'G_sub', 'B'],
        'expected_final_face': 9,
        'expected_final_alpha_h': 0,
        'expected_break_field': '(none-but-MEASURE-out-of-order)',
    },
    {
        'id': 'WC-5',
        'description': 'drop second B (omit step 4)',
        'initial': State(9, 0, 'resolved', 0),
        'ops': ['G_sub', 'B', 'G_sub', 'MEASURE'],
        'expected_final_face': 9,
        'expected_final_alpha_h': 1,
        'expected_break_field': 'alpha_h_label',
    },
]


# ── Main + verification ──────────────────────────────────────────────

def run_main_program() -> Dict[str, Any]:
    final, trace = execute_program(MAIN_INITIAL, MAIN_PROGRAM)

    # V-1, V-2: check each per-step state matches expected
    per_step_checks = []
    for (exp_step, exp_face, exp_alpha, exp_status, exp_budget), row in zip(
            MAIN_EXPECTED_PER_STEP, trace):
        ok = (
            row['step'] == exp_step
            and row['face_index'] == exp_face
            and row['alpha_h_label'] == exp_alpha
            and row['status'] == exp_status
            and row['cumulative_writes'] == exp_budget
        )
        per_step_checks.append({
            'step': exp_step,
            'expected_face': exp_face,
            'observed_face': row['face_index'],
            'expected_alpha_h': exp_alpha,
            'observed_alpha_h': row['alpha_h_label'],
            'expected_status': exp_status,
            'observed_status': row['status'],
            'expected_budget': exp_budget,
            'observed_budget': row['cumulative_writes'],
            'match': ok,
        })

    # V-3: final budget = 5 * S²
    budget_ok = final.cumulative_writes == 5 * S_SQUARED

    # V-4: budget remained under N_max throughout
    budget_ceiling_ok = all(
        row['cumulative_writes'] <= N_MAX for row in trace
    )

    # V-5: final measured alpha_h = 0
    final_alpha_ok = final.alpha_h_label == 0

    # V-6: final face = 9 (involution)
    final_face_ok = final.face_index == 9

    all_per_step_ok = all(c['match'] for c in per_step_checks)

    return {
        'trace': trace,
        'per_step_checks': per_step_checks,
        'final_state': asdict(final),
        'V-1_V-2_all_per_step_match': all_per_step_ok,
        'V-3_final_budget_eq_5_S_squared': budget_ok,
        'V-4_budget_under_N_max': budget_ceiling_ok,
        'V-5_final_alpha_h_eq_0': final_alpha_ok,
        'V-6_final_face_eq_9': final_face_ok,
        'main_program_pass': (
            all_per_step_ok and budget_ok and budget_ceiling_ok
            and final_alpha_ok and final_face_ok
        ),
    }


def run_wrong_controls() -> List[Dict[str, Any]]:
    results = []
    for wc in WRONG_CONTROLS:
        try:
            final, trace = execute_program(wc['initial'], wc['ops'])
            face_match = final.face_index == wc['expected_final_face']
            alpha_match = final.alpha_h_label == wc['expected_final_alpha_h']
            # WC passes if the predicted broken output is observed
            wc_pass = face_match and alpha_match
            results.append({
                'id': wc['id'],
                'description': wc['description'],
                'expected_final_face': wc['expected_final_face'],
                'observed_final_face': final.face_index,
                'expected_final_alpha_h': wc['expected_final_alpha_h'],
                'observed_final_alpha_h': final.alpha_h_label,
                'expected_break_field': wc['expected_break_field'],
                'wc_pass': wc_pass,
                'budget_consumed': final.cumulative_writes,
            })
        except Exception as e:
            results.append({
                'id': wc['id'],
                'description': wc['description'],
                'error': str(e),
                'wc_pass': False,
            })
    return results


# ── Output writers ───────────────────────────────────────────────────

def write_per_step_csv(trace: List[Dict[str, Any]], path: str) -> None:
    fieldnames = ['step', 'op', 'face_index', 'alpha_h_label', 'status',
                  'cumulative_writes']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trace)


def write_wrong_controls_csv(rows: List[Dict[str, Any]], path: str) -> None:
    fieldnames = ['id', 'description', 'expected_final_face',
                  'observed_final_face', 'expected_final_alpha_h',
                  'observed_final_alpha_h', 'expected_break_field',
                  'wc_pass', 'budget_consumed']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    print('CR001 — QGC Phase 1: Substrate Gate Involution End-to-End')
    print('=' * 60)
    print()

    # Main program
    main_result = run_main_program()

    print('Main program per-step trace:')
    print('-' * 60)
    print(f"{'step':<4} {'op':<10} {'face':<5} {'α_H':<4} {'status':<12} {'budget':>8}")
    for row in main_result['trace']:
        print(f"{row['step']:<4} {row['op']:<10} {row['face_index']:<5} "
              f"{str(row['alpha_h_label']):<4} {row['status']:<12} "
              f"{row['cumulative_writes']:>8}")

    print()
    print('Verification gates:')
    for k in ['V-1_V-2_all_per_step_match', 'V-3_final_budget_eq_5_S_squared',
              'V-4_budget_under_N_max', 'V-5_final_alpha_h_eq_0',
              'V-6_final_face_eq_9']:
        print(f'  {k:<45} {"PASS" if main_result[k] else "FAIL"}')
    main_pass = main_result['main_program_pass']
    print()
    print(f'  MAIN PROGRAM: {"PASS" if main_pass else "FAIL"}')

    # Wrong controls
    print()
    print('Wrong controls:')
    print('-' * 60)
    wc_results = run_wrong_controls()
    for wc in wc_results:
        if 'error' in wc:
            print(f"  {wc['id']:<6} {wc['description']:<45} "
                  f"ERROR: {wc['error']}")
        else:
            status = 'PASS' if wc['wc_pass'] else 'FAIL'
            print(f"  {wc['id']:<6} {wc['description']:<45} {status}")
            print(f"         observed face={wc['observed_final_face']} "
                  f"(expected {wc['expected_final_face']}), "
                  f"α_H={wc['observed_final_alpha_h']} "
                  f"(expected {wc['expected_final_alpha_h']})")

    all_wc_pass = all(wc.get('wc_pass', False) for wc in wc_results)
    print()
    print(f'  ALL WRONG CONTROLS: {"PASS" if all_wc_pass else "FAIL"}')

    # Verdict
    print()
    print('=' * 60)
    if main_pass and all_wc_pass:
        verdict = 'PASS'
    elif main_pass and not all_wc_pass:
        verdict = 'BOUNDARY'
    else:
        verdict = 'FAIL'
    print(f'CR001 VERDICT: {verdict}')
    print()

    # Write CSV outputs
    write_per_step_csv(main_result['trace'],
                       os.path.join(folder, 'CR001_per_step_trace.csv'))
    write_wrong_controls_csv(wc_results,
                             os.path.join(folder, 'CR001_wrong_controls.csv'))

    # Write summary.json
    summary = {
        'cr_id': 'CR001',
        'branch': '18_SAM_NATIVE_QC',
        'title': 'QGC Phase 1: Substrate Gate Involution End-to-End',
        'verdict': verdict,
        'main_program': {
            'program_ops': MAIN_PROGRAM,
            'initial_state': asdict(MAIN_INITIAL),
            'final_state': main_result['final_state'],
            'budget_consumed': main_result['final_state']['cumulative_writes'],
            'budget_ceiling_n_max': N_MAX,
            'budget_utilization_pct': round(
                100 * main_result['final_state']['cumulative_writes'] / N_MAX, 6),
            'verification_gates': {
                k: main_result[k] for k in [
                    'V-1_V-2_all_per_step_match',
                    'V-3_final_budget_eq_5_S_squared',
                    'V-4_budget_under_N_max',
                    'V-5_final_alpha_h_eq_0',
                    'V-6_final_face_eq_9',
                ]
            },
            'main_program_pass': main_pass,
        },
        'wrong_controls': {
            'results': wc_results,
            'all_pass': all_wc_pass,
        },
        'substrate_atoms_used': {
            'R': R, 'D': D, 'S': S, 'alpha_H': ALPHA_H,
            'S_squared': S_SQUARED, 'N_max': N_MAX,
            'residual_pair': list(RESIDUAL_PAIR),
        },
    }
    with open(os.path.join(folder, 'CR001_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f'Per-step trace : CR001_per_step_trace.csv')
    print(f'Wrong controls : CR001_wrong_controls.csv')
    print(f'Summary JSON   : CR001_summary.json')


if __name__ == '__main__':
    main()
