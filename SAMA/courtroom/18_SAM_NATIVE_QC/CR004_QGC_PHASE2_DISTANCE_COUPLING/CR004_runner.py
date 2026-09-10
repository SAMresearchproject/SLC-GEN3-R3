"""
CR004 — QGC Phase 2: Distance-Dependent Coupling via 1/r A-Kernel

Same joint program from CR003 with two sites at finite distance d.
Each figure deposits A-shift at the originating site (full S²/N_max)
AND at the other site (S²/(N_max · d)) per LCQC006 v2 / LCQC006a §3.2.

Verifies:
  - Final correlation (1, 1) is distance-invariant
  - Cumulative A per site matches the typed budget formula
    cumA_A = S²/N_max · (3 + 2/d), cumA_B = S²/N_max · (2 + 3/d)
  - Convergence to CR003 abstract limit as d → ∞
  - 1/r kernel (NOT 1/d²)
"""

import csv
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple


# ── Locked substrate atoms ──────────────────────────────────────────

S = 8
S_SQUARED = S * S          # = 64
N_MAX = 61_312
PER_WRITE_AT_SELF = 1.0 / N_MAX       # normalized contribution at write site
# Per-write at distance d: PER_WRITE_AT_SELF / d


# ── Single-site state (continuous cumulative_A) ─────────────────────

@dataclass
class State:
    face_index: int
    alpha_h_label: Any
    status: str
    cumulative_A: float   # continuous; saturation at 1.0

    def copy(self) -> 'State':
        return State(
            face_index=self.face_index,
            alpha_h_label=self.alpha_h_label,
            status=self.status,
            cumulative_A=self.cumulative_A,
        )


@dataclass
class JointState:
    site_A: State
    site_B: State
    distance: float

    def copy(self) -> 'JointState':
        return JointState(
            site_A=self.site_A.copy(),
            site_B=self.site_B.copy(),
            distance=self.distance,
        )

    def as_row(self, step: int, op: str) -> Dict[str, Any]:
        return {
            'step': step,
            'op': op,
            'distance': self.distance,
            'face_A': self.site_A.face_index,
            'alpha_h_A': self.site_A.alpha_h_label,
            'status_A': self.site_A.status,
            'cumA_A': self.site_A.cumulative_A,
            'face_B': self.site_B.face_index,
            'alpha_h_B': self.site_B.alpha_h_label,
            'status_B': self.site_B.status,
            'cumA_B': self.site_B.cumulative_A,
        }


# ── Budget accounting helpers ───────────────────────────────────────

def deposit_writes_at_site(joint: JointState, site_label: str,
                           writes: int) -> None:
    """Add `writes` substrate writes worth of A-shift at site_label.
    Also deposits cross-coupled shift at the OTHER site per 1/d kernel.
    """
    contrib_self = writes * PER_WRITE_AT_SELF
    contrib_cross = writes * PER_WRITE_AT_SELF / joint.distance

    if site_label == 'A':
        joint.site_A.cumulative_A += contrib_self
        joint.site_B.cumulative_A += contrib_cross
    elif site_label == 'B':
        joint.site_A.cumulative_A += contrib_cross
        joint.site_B.cumulative_A += contrib_self
    else:
        raise ValueError(f'unknown site {site_label!r}')


# ── LCQC003 v2 figure primitives (with distance-aware budget) ───────

def apply_binary_flip(joint: JointState, site: str) -> JointState:
    """B figure at given site: flip α_H label; S² writes at that site."""
    new = joint.copy()
    state = new.site_A if site == 'A' else new.site_B
    if state.status == 'resolved':
        state.alpha_h_label = 1 - state.alpha_h_label
    deposit_writes_at_site(new, site, S_SQUARED)
    return new


def apply_substrate_gate(joint: JointState, site: str) -> JointState:
    """𝒢_sub at given site: face 9↔12 swap; S² writes at that site."""
    new = joint.copy()
    state = new.site_A if site == 'A' else new.site_B
    if state.face_index == 9:
        state.face_index = 12
    elif state.face_index == 12:
        state.face_index = 9
    deposit_writes_at_site(new, site, S_SQUARED)
    return new


def apply_joint_C(joint: JointState, control: str, target: str) -> JointState:
    """𝒞 joint figure: S² writes at control + S² writes at target.
    Both sites incur their own gate-equivalent + cross-coupling from the other.
    """
    if control == target:
        raise ValueError('𝒞 requires distinct control and target')
    new = joint.copy()
    control_state = new.site_A if control == 'A' else new.site_B
    if control_state.status != 'resolved':
        raise ValueError(f'𝒞 requires resolved control')

    # Deposit S² writes at control AND S² writes at target
    deposit_writes_at_site(new, control, S_SQUARED)
    deposit_writes_at_site(new, target, S_SQUARED)

    # Apply target flip if control label = 1
    if control_state.alpha_h_label == 1:
        target_state = new.site_A if target == 'A' else new.site_B
        if target_state.status == 'resolved':
            target_state.alpha_h_label = 1 - target_state.alpha_h_label

    return new


def apply_publish(joint: JointState, site: str,
                  deterministic_result: Optional[int] = None) -> JointState:
    """PUBLISH at given site: S² writes at that site; resolves α_H if unresolved."""
    new = joint.copy()
    state = new.site_A if site == 'A' else new.site_B
    if state.status == 'unresolved':
        if deterministic_result is None:
            raise ValueError('PUBLISH on unresolved requires deterministic_result')
        state.alpha_h_label = deterministic_result
        state.status = 'resolved'
    deposit_writes_at_site(new, site, S_SQUARED)
    return new


# ── Program executor ────────────────────────────────────────────────

def execute_program(initial: JointState, ops: List[Tuple[str, ...]]) -> Tuple[JointState, List[Dict[str, Any]]]:
    trace: List[Dict[str, Any]] = []
    state = initial.copy()
    trace.append(state.as_row(0, 'INIT'))
    for step, op in enumerate(ops, start=1):
        op_name = op[0]
        if op_name == 'B':
            state = apply_binary_flip(state, op[1])
        elif op_name == 'G_sub':
            state = apply_substrate_gate(state, op[1])
        elif op_name == 'C':
            state = apply_joint_C(state, op[1], op[2])
        elif op_name == 'PUBLISH':
            state = apply_publish(state, op[1])
        else:
            raise ValueError(f'unknown op {op_name!r}')
        trace.append(state.as_row(step, '-'.join(str(x) for x in op)))
    return state, trace


# ── Main program ────────────────────────────────────────────────────

def make_initial(distance: float) -> JointState:
    return JointState(
        site_A=State(face_index=9, alpha_h_label=0, status='resolved',
                     cumulative_A=0.0),
        site_B=State(face_index=4, alpha_h_label=0, status='resolved',
                     cumulative_A=0.0),
        distance=distance,
    )


MAIN_PROGRAM = [
    ('B', 'A'),
    ('C', 'A', 'B'),
    ('PUBLISH', 'A'),
    ('PUBLISH', 'B'),
]


def predicted_cumA(distance: float) -> Tuple[float, float]:
    """Predicted (cumA_A, cumA_B) from LCQC006 v2 1/r formula."""
    cumA_A = (S_SQUARED / N_MAX) * (3.0 + 2.0 / distance)
    cumA_B = (S_SQUARED / N_MAX) * (2.0 + 3.0 / distance)
    return cumA_A, cumA_B


# ── Main test verification ──────────────────────────────────────────

def run_main_test(distance: float = 12.0, tolerance: float = 1e-9) -> Dict[str, Any]:
    final, trace = execute_program(make_initial(distance), MAIN_PROGRAM)
    pred_A, pred_B = predicted_cumA(distance)

    v1_corr = (final.site_A.alpha_h_label == 1
               and final.site_B.alpha_h_label == 1)
    v2_face = (final.site_A.face_index == 9
               and final.site_B.face_index == 4)
    v3_cumA_A = abs(final.site_A.cumulative_A - pred_A) < tolerance
    v4_cumA_B = abs(final.site_B.cumulative_A - pred_B) < tolerance
    v5_below_sat = (final.site_A.cumulative_A < 1.0
                    and final.site_B.cumulative_A < 1.0)
    v6_trace_complete = len(trace) == len(MAIN_PROGRAM) + 1

    return {
        'distance': distance,
        'trace': trace,
        'final_state': {
            'site_A': asdict(final.site_A),
            'site_B': asdict(final.site_B),
        },
        'predicted_cumA_A': pred_A,
        'predicted_cumA_B': pred_B,
        'observed_cumA_A': final.site_A.cumulative_A,
        'observed_cumA_B': final.site_B.cumulative_A,
        'V-1_correlation_eq_1_1': v1_corr,
        'V-2_faces_unchanged': v2_face,
        'V-3_cumA_A_matches_prediction': v3_cumA_A,
        'V-4_cumA_B_matches_prediction': v4_cumA_B,
        'V-5_below_saturation': v5_below_sat,
        'V-6_trace_complete': v6_trace_complete,
        'main_test_pass': (v1_corr and v2_face and v3_cumA_A and v4_cumA_B
                           and v5_below_sat and v6_trace_complete),
    }


# ── Distance sweep ──────────────────────────────────────────────────

DISTANCES = [1.0, 2.0, 6.0, 12.0, 100.0, 10000.0]


def run_distance_sweep(tolerance: float = 1e-9) -> List[Dict[str, Any]]:
    rows = []
    for d in DISTANCES:
        final, _ = execute_program(make_initial(d), MAIN_PROGRAM)
        pred_A, pred_B = predicted_cumA(d)
        corr_ok = (final.site_A.alpha_h_label == 1
                   and final.site_B.alpha_h_label == 1)
        cumA_A_ok = abs(final.site_A.cumulative_A - pred_A) < tolerance
        cumA_B_ok = abs(final.site_B.cumulative_A - pred_B) < tolerance
        rows.append({
            'distance': d,
            'predicted_cumA_A': pred_A,
            'observed_cumA_A': final.site_A.cumulative_A,
            'cumA_A_match': cumA_A_ok,
            'predicted_cumA_B': pred_B,
            'observed_cumA_B': final.site_B.cumulative_A,
            'cumA_B_match': cumA_B_ok,
            'correlation_AB': (final.site_A.alpha_h_label,
                               final.site_B.alpha_h_label),
            'correlation_eq_1_1': corr_ok,
        })
    return rows


# ── Wrong controls ──────────────────────────────────────────────────

def run_wrong_controls() -> List[Dict[str, Any]]:
    results = []

    # WC-1: abstract-distance limit recovery at d = 1e6
    d_huge = 1.0e6
    final, _ = execute_program(make_initial(d_huge), MAIN_PROGRAM)
    abstract_A = 3.0 * S_SQUARED / N_MAX
    abstract_B = 2.0 * S_SQUARED / N_MAX
    wc1_A_close = abs(final.site_A.cumulative_A - abstract_A) < 1e-5
    wc1_B_close = abs(final.site_B.cumulative_A - abstract_B) < 1e-5
    results.append({
        'id': 'WC-1',
        'description': 'abstract-distance recovery at d=1e6',
        'predicted_cumA_A_abstract': abstract_A,
        'observed_cumA_A': final.site_A.cumulative_A,
        'predicted_cumA_B_abstract': abstract_B,
        'observed_cumA_B': final.site_B.cumulative_A,
        'wc_pass': wc1_A_close and wc1_B_close,
    })

    # WC-2: correlation distance-invariance across multiple distances
    test_distances = [1.0, 12.0, 100.0, 10000.0]
    corrs = []
    for d in test_distances:
        final, _ = execute_program(make_initial(d), MAIN_PROGRAM)
        corrs.append((d, final.site_A.alpha_h_label,
                      final.site_B.alpha_h_label))
    all_corr_ok = all(c[1] == 1 and c[2] == 1 for c in corrs)
    results.append({
        'id': 'WC-2',
        'description': 'correlation distance-invariance across d in {1, 12, 100, 10000}',
        'correlations_per_distance': corrs,
        'wc_pass': all_corr_ok,
    })

    # WC-3: confirm 1/r NOT 1/d² (at d=12, compare to wrong-prediction)
    d_test = 12.0
    final, _ = execute_program(make_initial(d_test), MAIN_PROGRAM)
    correct_A, correct_B = predicted_cumA(d_test)
    # Wrong prediction under 1/d² would use 144 instead of 12
    wrong_A = (S_SQUARED / N_MAX) * (3.0 + 2.0 / (d_test ** 2))
    wrong_B = (S_SQUARED / N_MAX) * (2.0 + 3.0 / (d_test ** 2))
    matches_correct = (abs(final.site_A.cumulative_A - correct_A) < 1e-9
                       and abs(final.site_B.cumulative_A - correct_B) < 1e-9)
    matches_wrong = (abs(final.site_A.cumulative_A - wrong_A) < 1e-9
                     and abs(final.site_B.cumulative_A - wrong_B) < 1e-9)
    results.append({
        'id': 'WC-3',
        'description': 'runner uses 1/r kernel (NOT 1/d^2)',
        'observed_cumA_A': final.site_A.cumulative_A,
        'correct_1_over_r_prediction_A': correct_A,
        'wrong_1_over_d_squared_prediction_A': wrong_A,
        'matches_correct': matches_correct,
        'matches_wrong': matches_wrong,
        'wc_pass': matches_correct and not matches_wrong,
    })

    # WC-4: exact rational match at d=R=12
    # cumA_A = S²/N_max · (3 + 2/12) = S²/N_max · 19/6
    # cumA_B = S²/N_max · (2 + 3/12) = S²/N_max · 9/4
    expected_A = (S_SQUARED / N_MAX) * (19.0 / 6.0)
    expected_B = (S_SQUARED / N_MAX) * (9.0 / 4.0)
    final, _ = execute_program(make_initial(12.0), MAIN_PROGRAM)
    wc4_A_match = abs(final.site_A.cumulative_A - expected_A) < 1e-12
    wc4_B_match = abs(final.site_B.cumulative_A - expected_B) < 1e-12
    results.append({
        'id': 'WC-4',
        'description': 'exact rational match at d=R=12 (19/6 and 9/4 factors)',
        'expected_cumA_A_19_over_6': expected_A,
        'observed_cumA_A': final.site_A.cumulative_A,
        'expected_cumA_B_9_over_4': expected_B,
        'observed_cumA_B': final.site_B.cumulative_A,
        'wc_pass': wc4_A_match and wc4_B_match,
    })

    return results


# ── Output writers ──────────────────────────────────────────────────

def write_per_step_csv(trace: List[Dict[str, Any]], path: str) -> None:
    fieldnames = ['step', 'op', 'distance', 'face_A', 'alpha_h_A',
                  'status_A', 'cumA_A', 'face_B', 'alpha_h_B',
                  'status_B', 'cumA_B']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trace)


def write_sweep_csv(rows: List[Dict[str, Any]], path: str) -> None:
    fieldnames = ['distance', 'predicted_cumA_A', 'observed_cumA_A',
                  'cumA_A_match', 'predicted_cumA_B', 'observed_cumA_B',
                  'cumA_B_match', 'correlation_AB', 'correlation_eq_1_1']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})


def write_wc_csv(rows: List[Dict[str, Any]], path: str) -> None:
    # Flatten for CSV
    fieldnames = ['id', 'description', 'wc_pass', 'detail']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            detail = {k: v for k, v in row.items()
                      if k not in ('id', 'description', 'wc_pass')}
            writer.writerow({
                'id': row['id'],
                'description': row['description'],
                'wc_pass': row.get('wc_pass', False),
                'detail': json.dumps(detail, default=str),
            })


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    print('CR004 — QGC Phase 2: Distance-Dependent Coupling via 1/r A-Kernel')
    print('=' * 70)
    print()

    # Main test at d=R=12
    print('Main test (d = R = 12):')
    print('-' * 70)
    main_result = run_main_test(distance=12.0)
    print(f"  predicted cumA_A: {main_result['predicted_cumA_A']:.9f}")
    print(f"  observed  cumA_A: {main_result['observed_cumA_A']:.9f}")
    print(f"  predicted cumA_B: {main_result['predicted_cumA_B']:.9f}")
    print(f"  observed  cumA_B: {main_result['observed_cumA_B']:.9f}")
    print(f"  final correlation: (α_H_A={main_result['final_state']['site_A']['alpha_h_label']}, "
          f"α_H_B={main_result['final_state']['site_B']['alpha_h_label']})")
    print(f"  final faces:        (face_A={main_result['final_state']['site_A']['face_index']}, "
          f"face_B={main_result['final_state']['site_B']['face_index']})")
    print()
    for k in ['V-1_correlation_eq_1_1', 'V-2_faces_unchanged',
              'V-3_cumA_A_matches_prediction', 'V-4_cumA_B_matches_prediction',
              'V-5_below_saturation', 'V-6_trace_complete']:
        print(f"  {k:<48} {'PASS' if main_result[k] else 'FAIL'}")
    main_pass = main_result['main_test_pass']
    print()
    print(f"  MAIN TEST: {'PASS' if main_pass else 'FAIL'}")
    print()

    # Distance sweep
    print('Distance sweep:')
    print('-' * 70)
    sweep_rows = run_distance_sweep()
    print(f"{'d':<10} {'pred_A':<14} {'obs_A':<14} {'A_match':<8} "
          f"{'pred_B':<14} {'obs_B':<14} {'B_match':<8} {'corr':<10}")
    for row in sweep_rows:
        print(f"{row['distance']:<10.1f} {row['predicted_cumA_A']:<14.9f} "
              f"{row['observed_cumA_A']:<14.9f} "
              f"{'PASS' if row['cumA_A_match'] else 'FAIL':<8} "
              f"{row['predicted_cumA_B']:<14.9f} "
              f"{row['observed_cumA_B']:<14.9f} "
              f"{'PASS' if row['cumA_B_match'] else 'FAIL':<8} "
              f"{row['correlation_AB']}")
    sweep_all_pass = all(r['cumA_A_match'] and r['cumA_B_match']
                         and r['correlation_eq_1_1'] for r in sweep_rows)
    print()
    print(f"  DISTANCE SWEEP: {'PASS' if sweep_all_pass else 'FAIL'}")
    print()

    # Wrong controls
    print('Wrong controls:')
    print('-' * 70)
    wc_results = run_wrong_controls()
    for wc in wc_results:
        status = 'PASS' if wc.get('wc_pass', False) else 'FAIL'
        print(f"  {wc['id']:<6} {wc['description']:<55} {status}")
    all_wc_pass = all(wc.get('wc_pass', False) for wc in wc_results)
    print()
    print(f"  ALL WRONG CONTROLS: {'PASS' if all_wc_pass else 'FAIL'}")
    print()

    # Verdict
    print('=' * 70)
    if main_pass and sweep_all_pass and all_wc_pass:
        verdict = 'PASS'
    elif main_pass and (not sweep_all_pass or not all_wc_pass):
        verdict = 'BOUNDARY'
    else:
        verdict = 'FAIL'
    print(f'CR004 VERDICT: {verdict}')
    print()

    # Write outputs
    write_per_step_csv(main_result['trace'],
                       os.path.join(folder, 'CR004_per_step_trace.csv'))
    write_sweep_csv(sweep_rows,
                    os.path.join(folder, 'CR004_distance_sweep.csv'))
    write_wc_csv(wc_results,
                 os.path.join(folder, 'CR004_wrong_controls.csv'))

    summary = {
        'cr_id': 'CR004',
        'branch': '18_SAM_NATIVE_QC',
        'title': 'QGC Phase 2: Distance-Dependent Coupling via 1/r A-Kernel',
        'verdict': verdict,
        'main_test': {
            'distance': main_result['distance'],
            'predicted_cumA_A': main_result['predicted_cumA_A'],
            'observed_cumA_A': main_result['observed_cumA_A'],
            'predicted_cumA_B': main_result['predicted_cumA_B'],
            'observed_cumA_B': main_result['observed_cumA_B'],
            'final_state': main_result['final_state'],
            'verification_gates': {
                k: main_result[k] for k in [
                    'V-1_correlation_eq_1_1', 'V-2_faces_unchanged',
                    'V-3_cumA_A_matches_prediction',
                    'V-4_cumA_B_matches_prediction',
                    'V-5_below_saturation', 'V-6_trace_complete',
                ]
            },
            'main_test_pass': main_pass,
        },
        'distance_sweep': {
            'rows': sweep_rows,
            'all_pass': sweep_all_pass,
        },
        'wrong_controls': {
            'results': wc_results,
            'all_pass': all_wc_pass,
        },
        'substrate_atoms_used': {
            'S_squared': S_SQUARED, 'N_max': N_MAX,
            'per_write_at_self': PER_WRITE_AT_SELF,
        },
    }
    with open(os.path.join(folder, 'CR004_summary.json'), 'w',
              encoding='utf-8') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f'Per-step trace : CR004_per_step_trace.csv')
    print(f'Distance sweep : CR004_distance_sweep.csv')
    print(f'Wrong controls : CR004_wrong_controls.csv')
    print(f'Summary JSON   : CR004_summary.json')


if __name__ == '__main__':
    main()
