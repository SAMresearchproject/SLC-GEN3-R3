"""
CR003 — QGC Phase 2: Joint Figure 𝒞 Correlation End-to-End

Executes the locked program from CR003_PRECOMMIT.md against a two-site
abstract simulator implementing LCQC003 v2 figures (including the joint
figure 𝒞) + LCQC008 v2 publication. Verifies the joint figure produces
the predicted correlated output and that all 4 wrong controls produce
their predicted broken outputs.
"""

import csv
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple


# ── Locked substrate atoms (read-only from CR238 / LCQC004a) ─────────

S = 8
S_SQUARED = S * S  # = 64
N_MAX = 61_312


# ── Single-site state (per LCQC001) ──────────────────────────────────

@dataclass
class State:
    face_index: int
    alpha_h_label: Any            # 0, 1, or '?'
    status: str                   # 'resolved' or 'unresolved'
    cumulative_writes: int

    def copy(self) -> 'State':
        return State(
            face_index=self.face_index,
            alpha_h_label=self.alpha_h_label,
            status=self.status,
            cumulative_writes=self.cumulative_writes,
        )


# ── Joint state (per CR003 — two abstract sites) ─────────────────────

@dataclass
class JointState:
    site_A: State
    site_B: State

    def copy(self) -> 'JointState':
        return JointState(
            site_A=self.site_A.copy(),
            site_B=self.site_B.copy(),
        )

    def as_row(self, step: int, op: str) -> Dict[str, Any]:
        return {
            'step': step,
            'op': op,
            'face_A': self.site_A.face_index,
            'alpha_h_A': self.site_A.alpha_h_label,
            'status_A': self.site_A.status,
            'cum_writes_A': self.site_A.cumulative_writes,
            'face_B': self.site_B.face_index,
            'alpha_h_B': self.site_B.alpha_h_label,
            'status_B': self.site_B.status,
            'cum_writes_B': self.site_B.cumulative_writes,
        }


# ── LCQC003 v2 figure primitives ─────────────────────────────────────

def apply_binary_flip(state: State) -> State:
    """B figure: flip α_H label 0↔1 on resolved state; silent on unresolved."""
    new = state.copy()
    if state.status == 'resolved':
        new.alpha_h_label = 1 - state.alpha_h_label
    new.cumulative_writes += S_SQUARED
    return new


def apply_substrate_gate(state: State) -> State:
    """𝒢_sub figure: swap face 9↔12; identity elsewhere; label unchanged."""
    new = state.copy()
    if state.face_index == 9:
        new.face_index = 12
    elif state.face_index == 12:
        new.face_index = 9
    new.cumulative_writes += S_SQUARED
    return new


def apply_joint_C(joint: JointState, control: str, target: str) -> JointState:
    """LCQC003 v2 §3.3 joint figure 𝒞.

    𝒞 :  𝒲_c ⊗ 𝒲_t  →  𝒲_c ⊗ (B(𝒲_t) if label(𝒲_c) = 1 else 𝒲_t)

    Cost: S² writes at control + S² writes at target (each participating
    site sees gate-equivalent substrate activity per LCQC004a).
    """
    if control == target:
        raise ValueError(f'𝒞 requires distinct control and target sites; got both {control!r}')
    if control not in ('A', 'B') or target not in ('A', 'B'):
        raise ValueError(f'𝒞 sites must be A or B; got control={control!r}, target={target!r}')

    new = joint.copy()
    control_state = new.site_A if control == 'A' else new.site_B
    if control_state.status != 'resolved':
        raise ValueError(f'𝒞 requires resolved control; site_{control} is {control_state.status}')

    # Both sites incur S² writes (joint figure cost at each participating site)
    new.site_A.cumulative_writes += S_SQUARED
    new.site_B.cumulative_writes += S_SQUARED

    # If control's label is 1, apply B to target (label flip)
    if control_state.alpha_h_label == 1:
        target_state = new.site_A if target == 'A' else new.site_B
        if target_state.status == 'resolved':
            target_state.alpha_h_label = 1 - target_state.alpha_h_label

    return new


# ── LCQC008 v2 publication primitive ─────────────────────────────────

def apply_publish(state: State, deterministic_result: Optional[int] = None) -> State:
    """PUBLISH = G_matter promotion event.
    Idempotent on already-resolved states; commits unresolved to definite value.
    """
    new = state.copy()
    if state.status == 'unresolved':
        if deterministic_result is None:
            raise ValueError(
                'PUBLISH on unresolved state requires deterministic_result; '
                'Born-rule out of CR003 scope'
            )
        new.alpha_h_label = deterministic_result
        new.status = 'resolved'
    new.cumulative_writes += S_SQUARED
    return new


# ── Program executor ─────────────────────────────────────────────────

def execute_program(initial: JointState, ops: List[Tuple[str, ...]]) -> Tuple[JointState, List[Dict[str, Any]]]:
    """Execute a list of operations. Each op is a tuple naming the figure
    and its arguments, e.g., ('B', 'A'), ('C', 'A', 'B'), ('PUBLISH', 'A').
    """
    trace: List[Dict[str, Any]] = []
    state = initial.copy()
    trace.append(state.as_row(0, 'INIT'))
    for step, op in enumerate(ops, start=1):
        op_name = op[0]
        if op_name == 'B':
            site = op[1]
            if site == 'A':
                state.site_A = apply_binary_flip(state.site_A)
            elif site == 'B':
                state.site_B = apply_binary_flip(state.site_B)
            else:
                raise ValueError(f'unknown site {site!r}')
        elif op_name == 'G_sub':
            site = op[1]
            if site == 'A':
                state.site_A = apply_substrate_gate(state.site_A)
            elif site == 'B':
                state.site_B = apply_substrate_gate(state.site_B)
        elif op_name == 'C':
            control, target = op[1], op[2]
            state = apply_joint_C(state, control, target)
        elif op_name == 'PUBLISH':
            site = op[1]
            if site == 'A':
                state.site_A = apply_publish(state.site_A)
            elif site == 'B':
                state.site_B = apply_publish(state.site_B)
        else:
            raise ValueError(f'unknown op {op_name!r}')
        trace.append(state.as_row(step, '-'.join(str(x) for x in op)))
    return state, trace


# ── Main program (from CR003_PRECOMMIT.md) ──────────────────────────

def make_initial() -> JointState:
    return JointState(
        site_A=State(face_index=9, alpha_h_label=0, status='resolved',
                     cumulative_writes=0),
        site_B=State(face_index=4, alpha_h_label=0, status='resolved',
                     cumulative_writes=0),
    )


MAIN_PROGRAM = [
    ('B', 'A'),
    ('C', 'A', 'B'),
    ('PUBLISH', 'A'),
    ('PUBLISH', 'B'),
]

# Expected per-step state from PRECOMMIT
# Each tuple: (step_idx, face_A, alpha_h_A, status_A, cum_writes_A,
#                       face_B, alpha_h_B, status_B, cum_writes_B)
MAIN_EXPECTED = [
    (0, 9, 0, 'resolved', 0,       4, 0, 'resolved', 0),
    (1, 9, 1, 'resolved', S_SQUARED, 4, 0, 'resolved', 0),
    (2, 9, 1, 'resolved', 2 * S_SQUARED, 4, 1, 'resolved', S_SQUARED),
    (3, 9, 1, 'resolved', 3 * S_SQUARED, 4, 1, 'resolved', S_SQUARED),
    (4, 9, 1, 'resolved', 3 * S_SQUARED, 4, 1, 'resolved', 2 * S_SQUARED),
]


# ── Wrong controls ───────────────────────────────────────────────────

WRONG_CONTROLS = [
    {
        'id': 'WC-1',
        'description': 'skip B on control (no flip; control α_H stays 0)',
        'ops': [('C', 'A', 'B'), ('PUBLISH', 'A'), ('PUBLISH', 'B')],
        'expected_final': (9, 0, 'resolved', 4, 0, 'resolved'),
    },
    {
        'id': 'WC-2',
        'description': 'B(A) AFTER 𝒞 (𝒞 reads control α_H=0 before flip)',
        'ops': [('C', 'A', 'B'), ('B', 'A'), ('PUBLISH', 'A'), ('PUBLISH', 'B')],
        'expected_final': (9, 1, 'resolved', 4, 0, 'resolved'),
    },
    {
        'id': 'WC-3',
        'description': 'swap control/target (𝒞 with control=B, target=A)',
        'ops': [('B', 'A'), ('C', 'B', 'A'), ('PUBLISH', 'A'), ('PUBLISH', 'B')],
        'expected_final': (9, 1, 'resolved', 4, 0, 'resolved'),
    },
    {
        'id': 'WC-4',
        'description': 'apply 𝒞 twice (𝒞² = identity on joint state)',
        'ops': [('B', 'A'), ('C', 'A', 'B'), ('C', 'A', 'B'), ('PUBLISH', 'A'), ('PUBLISH', 'B')],
        'expected_final': (9, 1, 'resolved', 4, 0, 'resolved'),
    },
]


# ── Verification ─────────────────────────────────────────────────────

def run_main_program() -> Dict[str, Any]:
    final, trace = execute_program(make_initial(), MAIN_PROGRAM)

    per_step_checks = []
    for expected, row in zip(MAIN_EXPECTED, trace):
        (e_step, e_fA, e_aA, e_sA, e_wA, e_fB, e_aB, e_sB, e_wB) = expected
        ok = (
            row['step'] == e_step
            and row['face_A'] == e_fA
            and row['alpha_h_A'] == e_aA
            and row['status_A'] == e_sA
            and row['cum_writes_A'] == e_wA
            and row['face_B'] == e_fB
            and row['alpha_h_B'] == e_aB
            and row['status_B'] == e_sB
            and row['cum_writes_B'] == e_wB
        )
        per_step_checks.append({
            'step': e_step,
            'expected': expected[1:],
            'observed': (row['face_A'], row['alpha_h_A'], row['status_A'],
                         row['cum_writes_A'], row['face_B'], row['alpha_h_B'],
                         row['status_B'], row['cum_writes_B']),
            'match': ok,
        })

    all_per_step_ok = all(c['match'] for c in per_step_checks)
    budget_ok = (final.site_A.cumulative_writes == 3 * S_SQUARED
                 and final.site_B.cumulative_writes == 2 * S_SQUARED)
    budget_ceiling_ok = (final.site_A.cumulative_writes <= N_MAX
                         and final.site_B.cumulative_writes <= N_MAX)
    final_correlation_ok = (final.site_A.alpha_h_label == 1
                            and final.site_B.alpha_h_label == 1)
    final_faces_ok = (final.site_A.face_index == 9
                      and final.site_B.face_index == 4)

    return {
        'trace': trace,
        'per_step_checks': per_step_checks,
        'final_state': {
            'site_A': asdict(final.site_A),
            'site_B': asdict(final.site_B),
        },
        'V-1_all_per_step_match': all_per_step_ok,
        'V-2_budget_under_N_max': budget_ceiling_ok,
        'V-3_final_correlation_AB_eq_1_1': final_correlation_ok,
        'V-4_final_faces_unchanged': final_faces_ok,
        'V-5_final_cumulative_writes_match': budget_ok,
        'main_program_pass': (
            all_per_step_ok and budget_ceiling_ok and final_correlation_ok
            and final_faces_ok and budget_ok
        ),
    }


def run_wrong_controls() -> List[Dict[str, Any]]:
    results = []
    for wc in WRONG_CONTROLS:
        try:
            final, trace = execute_program(make_initial(), wc['ops'])
            observed = (
                final.site_A.face_index, final.site_A.alpha_h_label,
                final.site_A.status, final.site_B.face_index,
                final.site_B.alpha_h_label, final.site_B.status,
            )
            wc_pass = observed == wc['expected_final']
            results.append({
                'id': wc['id'],
                'description': wc['description'],
                'expected_final': wc['expected_final'],
                'observed_final': observed,
                'wc_pass': wc_pass,
                'cum_writes_A': final.site_A.cumulative_writes,
                'cum_writes_B': final.site_B.cumulative_writes,
            })
        except Exception as e:
            results.append({
                'id': wc['id'],
                'description': wc['description'],
                'error': str(e),
                'wc_pass': False,
            })
    return results


# ── Output ───────────────────────────────────────────────────────────

def write_per_step_csv(trace: List[Dict[str, Any]], path: str) -> None:
    fieldnames = ['step', 'op', 'face_A', 'alpha_h_A', 'status_A',
                  'cum_writes_A', 'face_B', 'alpha_h_B', 'status_B',
                  'cum_writes_B']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trace)


def write_wrong_controls_csv(rows: List[Dict[str, Any]], path: str) -> None:
    fieldnames = ['id', 'description', 'expected_final', 'observed_final',
                  'wc_pass', 'cum_writes_A', 'cum_writes_B']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    print('CR003 — QGC Phase 2: Joint Figure 𝒞 Correlation End-to-End')
    print('=' * 60)
    print()

    main_result = run_main_program()

    print('Main program per-step trace:')
    print('-' * 60)
    print(f"{'step':<4} {'op':<14}  "
          f"{'fA':>3} {'aA':>3} {'stA':<10} {'wA':>5}  "
          f"{'fB':>3} {'aB':>3} {'stB':<10} {'wB':>5}")
    for row in main_result['trace']:
        print(f"{row['step']:<4} {row['op']:<14}  "
              f"{row['face_A']:>3} {str(row['alpha_h_A']):>3} {row['status_A']:<10} {row['cum_writes_A']:>5}  "
              f"{row['face_B']:>3} {str(row['alpha_h_B']):>3} {row['status_B']:<10} {row['cum_writes_B']:>5}")

    print()
    print('Verification gates:')
    for k in ['V-1_all_per_step_match', 'V-2_budget_under_N_max',
              'V-3_final_correlation_AB_eq_1_1', 'V-4_final_faces_unchanged',
              'V-5_final_cumulative_writes_match']:
        print(f'  {k:<48} {"PASS" if main_result[k] else "FAIL"}')
    main_pass = main_result['main_program_pass']
    print()
    print(f'  MAIN PROGRAM: {"PASS" if main_pass else "FAIL"}')

    print()
    print('Wrong controls:')
    print('-' * 60)
    wc_results = run_wrong_controls()
    for wc in wc_results:
        if 'error' in wc:
            print(f"  {wc['id']:<6} {wc['description']:<55} ERROR: {wc['error']}")
        else:
            status = 'PASS' if wc['wc_pass'] else 'FAIL'
            print(f"  {wc['id']:<6} {wc['description']:<55} {status}")
            print(f"         observed final: {wc['observed_final']}")
            print(f"         expected final: {wc['expected_final']}")
    all_wc_pass = all(wc.get('wc_pass', False) for wc in wc_results)
    print()
    print(f'  ALL WRONG CONTROLS: {"PASS" if all_wc_pass else "FAIL"}')

    print()
    print('=' * 60)
    if main_pass and all_wc_pass:
        verdict = 'PASS'
    elif main_pass and not all_wc_pass:
        verdict = 'BOUNDARY'
    else:
        verdict = 'FAIL'
    print(f'CR003 VERDICT: {verdict}')
    print()

    write_per_step_csv(main_result['trace'],
                       os.path.join(folder, 'CR003_per_step_trace.csv'))
    write_wrong_controls_csv(wc_results,
                             os.path.join(folder, 'CR003_wrong_controls.csv'))

    summary = {
        'cr_id': 'CR003',
        'branch': '18_SAM_NATIVE_QC',
        'title': 'QGC Phase 2: Joint Figure 𝒞 Correlation End-to-End',
        'verdict': verdict,
        'main_program': {
            'program_ops': [list(op) for op in MAIN_PROGRAM],
            'final_state': main_result['final_state'],
            'budget_per_site': {
                'site_A_writes': main_result['final_state']['site_A']['cumulative_writes'],
                'site_B_writes': main_result['final_state']['site_B']['cumulative_writes'],
                'N_max': N_MAX,
            },
            'verification_gates': {
                k: main_result[k] for k in [
                    'V-1_all_per_step_match', 'V-2_budget_under_N_max',
                    'V-3_final_correlation_AB_eq_1_1',
                    'V-4_final_faces_unchanged',
                    'V-5_final_cumulative_writes_match',
                ]
            },
            'main_program_pass': main_pass,
        },
        'wrong_controls': {
            'results': wc_results,
            'all_pass': all_wc_pass,
        },
        'substrate_atoms_used': {
            'S': S, 'S_squared': S_SQUARED, 'N_max': N_MAX,
        },
    }
    with open(os.path.join(folder, 'CR003_summary.json'), 'w',
              encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f'Per-step trace : CR003_per_step_trace.csv')
    print(f'Wrong controls : CR003_wrong_controls.csv')
    print(f'Summary JSON   : CR003_summary.json')


if __name__ == '__main__':
    main()
