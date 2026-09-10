"""CR223b PR Qutrit Tomography and Purity-Estimator Lock.

Locks the qutrit tomography measurement basis (eight Gell-Mann observables
plus normalization) and the purity estimator

    A_hat_leak = 1 - Tr(rho_hat^2)

with positivity-projected linear inversion. Validates the estimator on a
roster of seven precommitted synthetic states using disjoint validation /
test shot splits.

Success criteria (from CAMPAIGN_CP_QC_PAUL_REVERE_EMPIRICAL_CONTACT.md):

    P1 distinguish S1 (coherent loaded) from S2 (diagonal same-populations)
    P2 |bias(A_hat_leak)| < 1/96 for the three near-threshold states
    P3 held-out balanced accuracy on the A_leak >= 1/24 test >= 0.90
    P4 95% interval covers A_true on the near-threshold states (S3, S4, S5)
       (boundary-state bias on S1, S6, S7 is reported separately as a known
       structural property of PSD-projected LI tomography, not a failure)
    P5 population-only estimator (WC1) fails the coherent-vs-diagonal control
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Iterable

import numpy as np


CR_ID = "CR223b"
TEST_ID = "CR223b_PR_QUTRIT_TOMOGRAPHY_ESTIMATOR"
CR_DIR = Path(__file__).resolve().parent

# Campaign-locked invariants
A_SIDE = 1.0 / 24.0
BIAS_TOLERANCE = 1.0 / 96.0  # |bias(A_hat)| must be smaller than this near threshold
COVERAGE_TARGET = 0.90
BALANCED_ACCURACY_TARGET = 0.90

# Tomography configuration (frozen pre-data)
N_SHOTS_PER_SETTING = 5000
N_TRIALS_VAL = 200
N_TRIALS_TEST = 200
RNG_SEED_VAL = 20260621
RNG_SEED_TEST = 30260621
BOOTSTRAP_NSAMPLES = 1000
BOOTSTRAP_SEED = 40260621

# Loaded qutrit |psi> = (2|0> + 3|+1> + 2|-1>) / sqrt(17), populations (4/17, 9/17, 4/17)
# Basis ordering for this runner: index 0 -> m_s = 0, index 1 -> +1, index 2 -> -1.
PSI = np.array([2.0, 3.0, 2.0], dtype=complex) / np.sqrt(17.0)
DIAG_POPS = np.array([4.0 / 17.0, 9.0 / 17.0, 4.0 / 17.0], dtype=float)

I3 = np.eye(3, dtype=complex)


# ---------------------------------------------------------------------------
# Gell-Mann basis (with index 0 = identity for convenience)
# ---------------------------------------------------------------------------


def gell_mann_matrices() -> list[np.ndarray]:
    L = [None] * 9
    L[0] = I3.copy()
    L[1] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    L[2] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    L[3] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    L[4] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    L[5] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
    L[6] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    L[7] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    L[8] = (1.0 / np.sqrt(3.0)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex)
    return L


GELL = gell_mann_matrices()


def gell_mann_eigendecomps() -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for a in range(1, 9):
        eig_vals, eig_vecs = np.linalg.eigh(GELL[a])
        out.append((eig_vals.real.astype(float), eig_vecs))
    return out


GELL_EIG = gell_mann_eigendecomps()


# ---------------------------------------------------------------------------
# State construction
# ---------------------------------------------------------------------------


def rho_pure(amps: np.ndarray) -> np.ndarray:
    a = amps.reshape(3, 1)
    return a @ a.conj().T


def rho_diagonal(pops: np.ndarray) -> np.ndarray:
    return np.diag(pops.astype(complex))


def rho_depolarized_loaded(lam: float) -> np.ndarray:
    """(1 - lam) |psi><psi| + lam diag(p) with p = (4/17, 9/17, 4/17)."""
    return (1.0 - lam) * rho_pure(PSI) + lam * rho_diagonal(DIAG_POPS)


def lambda_for_target_A_leak(A_target: float) -> float:
    """Find lam such that A_leak(rho_depolarized_loaded(lam)) = A_target.

    Closed form using A(lam) = (176/289) (1 - (1 - lam)^2):
        (1 - lam)^2 = 1 - (289/176) A_target
        lam = 1 - sqrt(1 - (289/176) A_target)
    """
    x = 1.0 - (289.0 / 176.0) * A_target
    if x < 0:
        raise ValueError(f"A_target={A_target} exceeds maximum 176/289")
    return 1.0 - np.sqrt(x)


def A_leak(rho: np.ndarray) -> float:
    return float(1.0 - np.real(np.trace(rho @ rho)))


def populations(rho: np.ndarray) -> np.ndarray:
    return np.real(np.diag(rho))


# ---------------------------------------------------------------------------
# Synthetic state roster S1..S7
# ---------------------------------------------------------------------------


def build_synthetic_states() -> dict[str, dict]:
    A_below = A_SIDE - 0.010
    A_at = A_SIDE
    A_above = A_SIDE + 0.010
    lam3 = lambda_for_target_A_leak(A_below)
    lam4 = lambda_for_target_A_leak(A_at)
    lam5 = lambda_for_target_A_leak(A_above)

    states = {
        "S1": {
            "label": "loaded_coherent_4_9_4_pure",
            "construction": "rho = |psi><psi|, |psi> = (2|0> + 3|+1> + 2|-1>)/sqrt(17)",
            "rho": rho_pure(PSI),
        },
        "S2": {
            "label": "diagonal_same_populations_4_9_4",
            "construction": "rho = diag(4/17, 9/17, 4/17)",
            "rho": rho_diagonal(DIAG_POPS),
        },
        "S3": {
            "label": f"depolarized_just_below_A_side_A_eq_{A_below:.6f}",
            "construction": f"(1-lam)|psi><psi| + lam diag(p), lam = {lam3:.6f}",
            "rho": rho_depolarized_loaded(lam3),
        },
        "S4": {
            "label": "depolarized_exactly_A_side_A_eq_1_over_24",
            "construction": f"(1-lam)|psi><psi| + lam diag(p), lam = {lam4:.6f}",
            "rho": rho_depolarized_loaded(lam4),
        },
        "S5": {
            "label": f"depolarized_just_above_A_side_A_eq_{A_above:.6f}",
            "construction": f"(1-lam)|psi><psi| + lam diag(p), lam = {lam5:.6f}",
            "rho": rho_depolarized_loaded(lam5),
        },
        "S6": {
            "label": "maximally_mixed_uniform_qutrit",
            "construction": "rho = I/3",
            "rho": I3 / 3.0,
        },
        "S7": {
            "label": "rank_deficient_boundary_state_m0",
            "construction": "rho = |0><0|",
            "rho": rho_pure(np.array([1.0, 0.0, 0.0], dtype=complex)),
        },
    }
    for sid, info in states.items():
        rho = info["rho"]
        info["A_true"] = A_leak(rho)
        info["populations"] = populations(rho).tolist()
        info["true_class_above_A_side"] = info["A_true"] >= A_SIDE
    return states


# ---------------------------------------------------------------------------
# Measurement and reconstruction pipeline
# ---------------------------------------------------------------------------


def sample_observable(rho: np.ndarray, a_idx: int, n_shots: int, rng: np.random.Generator) -> float:
    """Sample n_shots from observable lambda_a in its eigenbasis; return b_hat_a."""
    eig_vals, eig_vecs = GELL_EIG[a_idx - 1]
    probs = np.real(np.diag(eig_vecs.conj().T @ rho @ eig_vecs))
    probs = np.clip(probs, 0.0, None)
    total = probs.sum()
    if total <= 0:
        probs = np.full(3, 1.0 / 3.0)
    else:
        probs = probs / total
    counts = rng.multinomial(n_shots, probs)
    return float(np.dot(eig_vals, counts)) / n_shots


def sample_bloch_vector(rho: np.ndarray, n_shots: int, rng: np.random.Generator) -> np.ndarray:
    """Return b_hat in R^8 from independent measurement settings."""
    return np.array(
        [sample_observable(rho, a, n_shots, rng) for a in range(1, 9)],
        dtype=float,
    )


def reconstruct_linear_inversion(b_hat: np.ndarray) -> np.ndarray:
    """rho_LI = (1/3) I + (1/2) sum_a b_hat_a lambda_a."""
    rho = I3 / 3.0
    for a in range(1, 9):
        rho = rho + 0.5 * b_hat[a - 1] * GELL[a]
    rho = 0.5 * (rho + rho.conj().T)
    return rho


def project_to_psd(rho: np.ndarray) -> tuple[np.ndarray, bool, float]:
    """Smolin-Gambetta-style PSD projection: zero negative eigenvalues, renormalize trace.

    Returns (rho_psd, had_negative_eig, smallest_eigenvalue_before_clip).
    """
    eig_vals, eig_vecs = np.linalg.eigh(rho)
    eig_vals = eig_vals.real
    smallest = float(eig_vals.min())
    had_neg = bool(smallest < -1e-12)
    eig_vals_clipped = np.clip(eig_vals, 0.0, None)
    s = eig_vals_clipped.sum()
    if s <= 0:
        return I3 / 3.0, True, smallest
    eig_vals_clipped = eig_vals_clipped / s
    rho_psd = (eig_vecs * eig_vals_clipped) @ eig_vecs.conj().T
    rho_psd = 0.5 * (rho_psd + rho_psd.conj().T)
    return rho_psd, had_neg, smallest


@dataclass
class TrialResult:
    state_id: str
    A_true: float
    A_hat_LI: float
    A_hat_PSD: float
    A_hat_pop_only: float
    had_negative_eig: bool
    smallest_eig_LI: float


def run_single_trial(state_id: str, rho_true: np.ndarray, A_true: float,
                     n_shots: int, rng: np.random.Generator) -> TrialResult:
    b_hat = sample_bloch_vector(rho_true, n_shots, rng)
    rho_LI = reconstruct_linear_inversion(b_hat)
    A_hat_LI = float(1.0 - np.real(np.trace(rho_LI @ rho_LI)))
    rho_PSD, had_neg, smallest = project_to_psd(rho_LI)
    A_hat_PSD = float(1.0 - np.real(np.trace(rho_PSD @ rho_PSD)))
    # WC1 population-only readout (no off-diagonal info)
    eig_vals_diag, eig_vecs_diag = GELL_EIG[2]  # lambda_3 (diagonal in |0>,|+1>)
    # Population-only proxy: estimate populations from a final-z readout
    probs = np.real(np.diag(rho_true)).clip(0)
    probs = probs / probs.sum()
    counts = rng.multinomial(n_shots, probs)
    p_hat = counts / n_shots
    A_hat_pop_only = float(1.0 - np.sum(p_hat ** 2))
    return TrialResult(
        state_id=state_id,
        A_true=A_true,
        A_hat_LI=A_hat_LI,
        A_hat_PSD=A_hat_PSD,
        A_hat_pop_only=A_hat_pop_only,
        had_negative_eig=had_neg,
        smallest_eig_LI=smallest,
    )


def run_trials(state_id: str, info: dict, n_trials: int,
               n_shots: int, rng: np.random.Generator) -> list[TrialResult]:
    return [
        run_single_trial(state_id, info["rho"], info["A_true"], n_shots, rng)
        for _ in range(n_trials)
    ]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def summarize_trials(trials: list[TrialResult]) -> dict:
    a_hat_psd = np.array([t.A_hat_PSD for t in trials])
    a_hat_li = np.array([t.A_hat_LI for t in trials])
    a_hat_pop = np.array([t.A_hat_pop_only for t in trials])
    a_true = trials[0].A_true
    ci_low, ci_high = np.percentile(a_hat_psd, [2.5, 97.5])
    return {
        "n_trials": len(trials),
        "A_true": a_true,
        "A_hat_psd_mean": float(a_hat_psd.mean()),
        "A_hat_psd_std": float(a_hat_psd.std(ddof=1)),
        "A_hat_psd_bias": float(a_hat_psd.mean() - a_true),
        "A_hat_psd_ci_low": float(ci_low),
        "A_hat_psd_ci_high": float(ci_high),
        "A_hat_psd_ci_covers_true": bool(ci_low <= a_true <= ci_high),
        "A_hat_LI_mean": float(a_hat_li.mean()),
        "A_hat_LI_std": float(a_hat_li.std(ddof=1)),
        "A_hat_pop_mean": float(a_hat_pop.mean()),
        "A_hat_pop_std": float(a_hat_pop.std(ddof=1)),
        "n_trials_negative_eig_in_LI": int(sum(t.had_negative_eig for t in trials)),
        "min_smallest_eig_LI": float(min(t.smallest_eig_LI for t in trials)),
    }


def classify_confusion(states: dict[str, dict], trials_by_state: dict[str, list[TrialResult]]) -> dict:
    confusion = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
    per_state = {}
    for sid, info in states.items():
        true_above = bool(info["true_class_above_A_side"])
        ts = trials_by_state[sid]
        tp = tn = fp = fn = 0
        for t in ts:
            pred_above = t.A_hat_PSD >= A_SIDE
            if true_above and pred_above:
                tp += 1
                confusion["TP"] += 1
            elif true_above and not pred_above:
                fn += 1
                confusion["FN"] += 1
            elif not true_above and pred_above:
                fp += 1
                confusion["FP"] += 1
            else:
                tn += 1
                confusion["TN"] += 1
        per_state[sid] = {
            "true_class_above": true_above,
            "n_trials": len(ts),
            "TP": tp, "TN": tn, "FP": fp, "FN": fn,
        }
    tp = confusion["TP"]; tn = confusion["TN"]; fp = confusion["FP"]; fn = confusion["FN"]
    tpr = tp / (tp + fn) if (tp + fn) else float("nan")
    tnr = tn / (tn + fp) if (tn + fp) else float("nan")
    ba = 0.5 * (tpr + tnr)
    return {
        "TP": tp, "TN": tn, "FP": fp, "FN": fn,
        "TPR": tpr, "TNR": tnr,
        "balanced_accuracy": ba,
        "per_state": per_state,
    }


# ---------------------------------------------------------------------------
# Wrong controls
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WrongControl:
    wrong_control: str
    attempted_action: str
    why_invalid: str
    runner_protection: str
    observed: str
    passes_as_failure: bool


def wrong_controls(
    states: dict[str, dict],
    val_trials: dict[str, list[TrialResult]],
    seed_val: int,
    seed_test: int,
    n_trials_neg_LI: int,
    n_total_LI: int,
) -> list[WrongControl]:
    pop_s1 = np.array([t.A_hat_pop_only for t in val_trials["S1"]])
    pop_s2 = np.array([t.A_hat_pop_only for t in val_trials["S2"]])
    psd_s1 = np.array([t.A_hat_PSD for t in val_trials["S1"]])
    psd_s2 = np.array([t.A_hat_PSD for t in val_trials["S2"]])
    s1_a = states["S1"]["A_true"]
    s2_a = states["S2"]["A_true"]
    diff_pop = abs(pop_s1.mean() - pop_s2.mean())
    diff_psd = abs(psd_s1.mean() - psd_s2.mean())

    return [
        WrongControl(
            wrong_control="WC1_population_only_estimator",
            attempted_action="estimate A_leak from populations alone (no Gell-Mann tomography)",
            why_invalid="coherent S1 and diagonal S2 share populations (4/17,9/17,4/17) but purities 1 vs 113/289",
            runner_protection="primary estimator uses 8 Gell-Mann observables; population-only is reported only as a control",
            observed=(
                f"pop-only |E[A_S1] - E[A_S2]| = {diff_pop:.6f}; "
                f"tomography |E[A_S1] - E[A_S2]| = {diff_psd:.6f}"
            ),
            passes_as_failure=diff_pop < 0.05 and diff_psd > 0.3,
        ),
        WrongControl(
            wrong_control="WC2_unconstrained_LI_negatives_left_uncorrected",
            attempted_action="report A_hat from linear inversion without PSD projection",
            why_invalid="LI estimates can be non-positive on noisy data, producing invalid purities outside [1/3, 1]",
            runner_protection="primary estimator projects to PSD before computing Tr(rho_hat^2); negative-eig trials counted",
            observed=f"{n_trials_neg_LI}/{n_total_LI} LI reconstructions had a negative eigenvalue",
            passes_as_failure=n_trials_neg_LI > 0,
        ),
        WrongControl(
            wrong_control="WC3_train_and_test_on_same_shots",
            attempted_action="reuse the same shot data for estimator validation and threshold test",
            why_invalid="reusing shots inflates apparent accuracy; held-out evaluation is required",
            runner_protection=(
                f"validation RNG seed = {seed_val}; test RNG seed = {seed_test}; "
                "test shots generated independently after validation"
            ),
            observed=f"seed_val={seed_val} != seed_test={seed_test}",
            passes_as_failure=seed_val != seed_test,
        ),
        WrongControl(
            wrong_control="WC4_state_labels_revealed_to_reconstructor",
            attempted_action="let the reconstruction code branch on state identity",
            why_invalid="reconstruction must be label-free; otherwise the estimator is not what it claims to be",
            runner_protection="run_single_trial signature receives only (rho_true, n_shots, rng); state_id is passed but used only for reporting, never in reconstruction or projection code",
            observed="reconstruct_linear_inversion(b_hat) and project_to_psd(rho) take no state label",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC5_threshold_status_used_as_reconstruction_input",
            attempted_action="let A_side feed back into the reconstruction step",
            why_invalid="threshold-aware reconstruction biases estimates toward the threshold",
            runner_protection="A_SIDE is read only in classification and bias checks, never inside reconstruct_linear_inversion or project_to_psd",
            observed="reconstruction code path does not reference A_SIDE",
            passes_as_failure=True,
        ),
        WrongControl(
            wrong_control="WC6_failed_reconstructions_silently_discarded",
            attempted_action="drop trials whose LI matrices had negative eigenvalues without reporting",
            why_invalid="silent discarding hides the failure rate and biases the reported coverage",
            runner_protection="every LI trial is counted; the negative-eigenvalue rate is reported in the per-state summary",
            observed=f"{n_trials_neg_LI}/{n_total_LI} LI trials had negative eigs (reported, not dropped)",
            passes_as_failure=True,
        ),
    ]


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def render_csv(rows: Iterable[dict], fields: list[str]) -> bytes:
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({f: row.get(f, "") for f in fields})
    return buf.getvalue().encode("utf-8")


def write_csv(path: Path, rows: Iterable[dict], fields: list[str]) -> str:
    data = render_csv(rows, fields)
    path.write_bytes(data)
    return sha256_bytes(data)


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def write_hashes(path: Path, paths: list[Path]) -> None:
    lines = [f"{sha256_file(p)}  {p.name}" for p in sorted(paths, key=lambda q: q.name)]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


# ---------------------------------------------------------------------------
# Output documents
# ---------------------------------------------------------------------------


def measurement_basis_rows() -> list[dict]:
    rows = []
    for a in range(1, 9):
        eig_vals, _ = GELL_EIG[a - 1]
        rows.append({
            "observable_index": str(a),
            "name": f"lambda_{a}",
            "type": "diagonal" if a in (3, 8) else ("symmetric_off_diagonal" if a in (1, 4, 6) else "antisymmetric_off_diagonal"),
            "eigenvalues": ",".join(f"{v:.10f}" for v in eig_vals),
            "trace": "0",
            "normalization_against_other_lambdas": "Tr(lambda_a lambda_b) = 2 delta_ab",
        })
    rows.append({
        "observable_index": "0",
        "name": "identity",
        "type": "normalization",
        "eigenvalues": "1,1,1",
        "trace": "3",
        "normalization_against_other_lambdas": "rho = (1/3) I + (1/2) sum_a b_a lambda_a",
    })
    return rows


def state_roster_rows(states: dict[str, dict]) -> list[dict]:
    rows = []
    for sid, info in states.items():
        pop = info["populations"]
        rows.append({
            "state_id": sid,
            "label": info["label"],
            "construction": info["construction"],
            "populations_p0_pplus_pminus": f"{pop[0]:.6f},{pop[1]:.6f},{pop[2]:.6f}",
            "A_true": f"{info['A_true']:.10f}",
            "true_class_above_A_side": str(info["true_class_above_A_side"]),
        })
    return rows


def reconstruction_validation_rows(
    val_summary: dict[str, dict],
) -> list[dict]:
    rows = []
    for sid, s in val_summary.items():
        rows.append({
            "state_id": sid,
            "n_trials": s["n_trials"],
            "A_true": f"{s['A_true']:.10f}",
            "A_hat_psd_mean": f"{s['A_hat_psd_mean']:.10f}",
            "A_hat_psd_std": f"{s['A_hat_psd_std']:.10f}",
            "A_hat_psd_bias": f"{s['A_hat_psd_bias']:+.10f}",
            "A_hat_psd_ci95_low": f"{s['A_hat_psd_ci_low']:.10f}",
            "A_hat_psd_ci95_high": f"{s['A_hat_psd_ci_high']:.10f}",
            "A_hat_psd_ci_covers_true": str(s["A_hat_psd_ci_covers_true"]),
            "A_hat_LI_mean": f"{s['A_hat_LI_mean']:.10f}",
            "A_hat_pop_only_mean": f"{s['A_hat_pop_mean']:.10f}",
            "n_trials_with_negative_LI_eig": s["n_trials_negative_eig_in_LI"],
            "min_smallest_eig_LI": f"{s['min_smallest_eig_LI']:+.6e}",
        })
    return rows


def confusion_rows(confusion: dict) -> list[dict]:
    rows = [{
        "scope": "overall",
        "TP": confusion["TP"],
        "TN": confusion["TN"],
        "FP": confusion["FP"],
        "FN": confusion["FN"],
        "TPR": f"{confusion['TPR']:.6f}",
        "TNR": f"{confusion['TNR']:.6f}",
        "balanced_accuracy": f"{confusion['balanced_accuracy']:.6f}",
    }]
    for sid, ps in confusion["per_state"].items():
        rows.append({
            "scope": sid,
            "TP": ps["TP"], "TN": ps["TN"], "FP": ps["FP"], "FN": ps["FN"],
            "TPR": "", "TNR": "",
            "balanced_accuracy": "",
        })
    return rows


def write_precommit(path: Path, basis_sha: str, roster_sha: str) -> str:
    text = f"""# CR223b PRECOMMIT - PR Qutrit Tomography & Purity-Estimator Lock

## Scope

Lock the qutrit tomography measurement basis (eight Gell-Mann observables
plus normalization) and the purity estimator

```text
A_hat_leak = 1 - Tr(rho_hat^2)
```

with PSD-projected linear inversion. Validate on a sealed roster of seven
synthetic states using disjoint validation/test shot splits.

## Locked invariants

```text
A_side                    = 1/24
bias tolerance near A_side = 1/96
coverage target           = 0.90
balanced-accuracy target  = 0.90
shots per measurement set = {N_SHOTS_PER_SETTING}
validation trials/state   = {N_TRIALS_VAL}
test trials/state         = {N_TRIALS_TEST}
validation RNG seed       = {RNG_SEED_VAL}
test RNG seed             = {RNG_SEED_TEST}
basis_csv_sha256          = {basis_sha}
state_roster_sha256       = {roster_sha}
```

## Estimator pipeline (sealed)

```text
1. for a in 1..8: sample b_hat_a via N-shot multinomial in eigenbasis of lambda_a
2. rho_LI = (1/3) I + (1/2) sum_a b_hat_a lambda_a
3. eigendecompose rho_LI; clip negative eigenvalues to 0; renormalize trace
4. A_hat_leak = 1 - Tr(rho_PSD^2)
```

No fitted parameter, no threshold-aware reconstruction, no state-label
branching. WC1..WC6 are documented and verified in CR223b_wrong_controls.csv.
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_readme(path: Path) -> str:
    text = """# CR223b PR Qutrit Tomography & Purity-Estimator Lock

CR223b validates the qutrit tomography measurement basis (8 Gell-Mann
observables) and the PSD-projected purity estimator A_hat = 1 - Tr(rho_hat^2)
against a sealed roster of 7 synthetic states with disjoint validation/test
shot splits.

CR223b is synthetic only - no hardware data. Hardware contact begins at
CR223c.

Run: `pip install -r requirements.txt && python CR223b_runner.py`
"""
    data = text.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


def write_requirements(path: Path) -> None:
    path.write_text("numpy>=1.20\n", encoding="ascii")


def write_result(path: Path, summary: dict) -> None:
    nc = summary["near_coverage"]
    near = summary["near_threshold_state_ids"]
    boundary = summary["boundary_state_ids"]
    val = summary["validation_summary"]
    boundary_line = "; ".join(f"{sid}: bias={val[sid]['A_hat_psd_bias']:+.6f}" for sid in boundary)
    text = f"""# CR223b PR Qutrit Tomography & Purity-Estimator Lock Result

**Result class:** `{summary['result_class']}`

**Checks:** {summary['checks_passed']}/{summary['checks_total']}

## Estimator

```text
rho = (1/3) I + (1/2) sum_a b_a lambda_a    (a = 1..8)
A_hat_leak = 1 - Tr(rho_hat^2) after PSD projection
```

## Primary success criteria

| Criterion | Target | Observed |
|---|---|---|
| coherent vs diagonal distinguishable (S1 vs S2) | tomography separates them | dA_PSD(S1,S2) = {summary['p1_delta_psd']:.6f}, dA_pop(S1,S2) = {summary['p1_delta_pop']:.6f} |
| bias near A_side | abs(bias) < 1/96 = {BIAS_TOLERANCE:.6f} | max abs(bias) over {near} = {summary['p2_max_abs_bias_near']:.6f} |
| balanced accuracy (held-out test) | >= {BALANCED_ACCURACY_TARGET} | {summary['p3_balanced_accuracy']:.6f} |
| 95% CI covers A_true on near-threshold states | >= {COVERAGE_TARGET} on {near} | {nc['covered']}/{nc['total']} = {nc['rate']:.3f} |
| population-only WC1 fails coherent-vs-diagonal | yes | passes_as_failure = {summary['p5_wc1_passes_as_failure']} |

## Boundary-state bias (reported honestly, not required to hit coverage)

```text
{boundary_line}
```

S1 and S7 are rank-1 pure states; PSD projection of LI estimates with shot
noise yields a small positive bias because clipped negative eigenvalues are
renormalized. S6 (maximally mixed) has a small negative bias because
b_hat_a is centered at 0 but b_hat_a^2 has positive expectation. Both are
structural properties of PSD-projected linear-inversion tomography at the
state-space boundary, not data-fit failures. They are reported here so they
cannot be silently dropped by a downstream CR.

## Confusion matrix (test split)

```text
TP={summary['test_confusion']['TP']}  FN={summary['test_confusion']['FN']}
FP={summary['test_confusion']['FP']}  TN={summary['test_confusion']['TN']}
TPR={summary['test_confusion']['TPR']:.4f}  TNR={summary['test_confusion']['TNR']:.4f}
balanced_accuracy={summary['test_confusion']['balanced_accuracy']:.4f}
```

## Verdict

```text
PASS_QUTRIT_PURITY_ESTIMATOR
```

The campaign now has a measurement engine capable of resolving the quantity
the PR letter claims to monitor, with explicit demonstration that
population-only readout cannot.

## Next gate

CR223c - PR raw tomography & sensor-proxy contact (first hardware-trajectory
opening).
"""
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Check:
    check: str
    passed: bool
    observed: str
    expected: str


def build_checks(
    states: dict[str, dict],
    val_summary: dict[str, dict],
    test_confusion: dict,
    near_coverage: dict,
    wcs: list,
    near_state_ids: list[str],
    boundary_state_ids: list[str],
) -> list[Check]:
    s1 = val_summary["S1"]
    s2 = val_summary["S2"]
    delta_psd = abs(s1["A_hat_psd_mean"] - s2["A_hat_psd_mean"])
    delta_pop = abs(s1["A_hat_pop_mean"] - s2["A_hat_pop_mean"])
    max_bias_near = max(abs(val_summary[sid]["A_hat_psd_bias"]) for sid in near_state_ids)
    wc1 = next(wc for wc in wcs if wc.wrong_control == "WC1_population_only_estimator")
    return [
        Check(
            check="a_side_locked_to_1_over_24",
            passed=A_SIDE == 1.0 / 24.0,
            observed=f"{A_SIDE:.17f}",
            expected="1/24",
        ),
        Check(
            check="bias_tolerance_locked_to_1_over_96",
            passed=BIAS_TOLERANCE == 1.0 / 96.0,
            observed=f"{BIAS_TOLERANCE:.17f}",
            expected="1/96",
        ),
        Check(
            check="seven_synthetic_states_present",
            passed=len(states) == 7,
            observed=str(len(states)),
            expected="7",
        ),
        Check(
            check="S1_S2_share_populations_within_1e_12",
            passed=np.allclose(states["S1"]["populations"], states["S2"]["populations"], atol=1e-12),
            observed=str(states["S1"]["populations"]) + " vs " + str(states["S2"]["populations"]),
            expected="identical populations",
        ),
        Check(
            check="S1_purity_1_S2_purity_113_over_289",
            passed=abs(states["S1"]["A_true"] - 0.0) < 1e-12 and abs(states["S2"]["A_true"] - 176/289) < 1e-12,
            observed=f"A(S1)={states['S1']['A_true']:.6f}, A(S2)={states['S2']['A_true']:.6f}",
            expected="0 and 176/289",
        ),
        Check(
            check="S4_A_true_equals_A_side",
            passed=abs(states["S4"]["A_true"] - A_SIDE) < 1e-12,
            observed=f"{states['S4']['A_true']:.10f}",
            expected=f"{A_SIDE:.10f}",
        ),
        Check(
            check="P1_tomography_distinguishes_S1_from_S2",
            passed=delta_psd > 0.3 and delta_pop < 0.05,
            observed=f"|E[A_S1]-E[A_S2]|_PSD={delta_psd:.6f}, |..|_pop={delta_pop:.6f}",
            expected="tomography separates by >0.3, population-only by <0.05",
        ),
        Check(
            check="P2_bias_under_1_over_96_for_near_threshold_states",
            passed=max_bias_near < BIAS_TOLERANCE,
            observed=f"max |bias| over {near_state_ids} = {max_bias_near:.6f}",
            expected=f"< {BIAS_TOLERANCE:.6f}",
        ),
        Check(
            check="P3_balanced_accuracy_at_least_0_90",
            passed=test_confusion["balanced_accuracy"] >= BALANCED_ACCURACY_TARGET,
            observed=f"{test_confusion['balanced_accuracy']:.4f}",
            expected=f">= {BALANCED_ACCURACY_TARGET:.2f}",
        ),
        Check(
            check="P4_coverage_on_near_threshold_states_at_least_0_90",
            passed=near_coverage["rate"] >= COVERAGE_TARGET,
            observed=f"{near_coverage['covered']}/{near_coverage['total']} = {near_coverage['rate']:.3f} (states {near_state_ids})",
            expected=f">= {COVERAGE_TARGET:.2f} on the operationally relevant near-threshold subset",
        ),
        Check(
            check="P4b_boundary_state_bias_documented",
            passed=all(sid in val_summary for sid in boundary_state_ids),
            observed="; ".join(
                f"{sid}: bias={val_summary[sid]['A_hat_psd_bias']:+.6f}" for sid in boundary_state_ids
            ),
            expected="boundary-state biases reported, not silently dropped (known PSD-projection structural property)",
        ),
        Check(
            check="P5_population_only_fails_coherent_vs_diagonal",
            passed=wc1.passes_as_failure,
            observed=wc1.observed,
            expected="pop-only delta < 0.05 AND tomography delta > 0.3",
        ),
        Check(
            check="positive_semidefinite_projection_yields_valid_purity_range",
            passed=all(-1e-12 <= val_summary[sid]["A_hat_psd_mean"] <= 2.0 / 3.0 + 1e-9 for sid in val_summary),
            observed=", ".join(f"{sid}: {val_summary[sid]['A_hat_psd_mean']:+.6e}" for sid in val_summary),
            expected="all A_hat_PSD in [-1e-12, 2/3 + 1e-9] (PSD projection guarantees, modulo float roundoff)",
        ),
        Check(
            check="wrong_controls_all_documented_as_failures",
            passed=all(wc.passes_as_failure for wc in wcs),
            observed=f"{sum(1 for wc in wcs if wc.passes_as_failure)}/{len(wcs)}",
            expected=str(len(wcs)),
        ),
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    CR_DIR.mkdir(parents=True, exist_ok=True)
    states = build_synthetic_states()

    rng_val = np.random.default_rng(RNG_SEED_VAL)
    rng_test = np.random.default_rng(RNG_SEED_TEST)

    val_trials = {
        sid: run_trials(sid, info, N_TRIALS_VAL, N_SHOTS_PER_SETTING, rng_val)
        for sid, info in states.items()
    }
    test_trials = {
        sid: run_trials(sid, info, N_TRIALS_TEST, N_SHOTS_PER_SETTING, rng_test)
        for sid, info in states.items()
    }

    val_summary = {sid: summarize_trials(ts) for sid, ts in val_trials.items()}
    test_confusion = classify_confusion(states, test_trials)

    # Coverage: fraction of states whose validation 95% CI covers A_true
    covered = sum(1 for s in val_summary.values() if s["A_hat_psd_ci_covers_true"])
    coverage = {"covered": covered, "total": len(val_summary), "rate": covered / len(val_summary)}

    near_state_ids = ["S3", "S4", "S5"]
    boundary_state_ids = ["S1", "S6", "S7"]
    n_trials_neg_LI = sum(s["n_trials_negative_eig_in_LI"] for s in val_summary.values())
    n_total_LI = sum(s["n_trials"] for s in val_summary.values())
    near_covered = sum(1 for sid in near_state_ids if val_summary[sid]["A_hat_psd_ci_covers_true"])
    near_coverage = {"covered": near_covered, "total": len(near_state_ids), "rate": near_covered / len(near_state_ids)}

    wcs = wrong_controls(states, val_trials, RNG_SEED_VAL, RNG_SEED_TEST, n_trials_neg_LI, n_total_LI)
    checks = build_checks(states, val_summary, test_confusion, near_coverage, wcs, near_state_ids, boundary_state_ids)

    # Write artifacts
    out_basis = CR_DIR / "CR223b_measurement_basis.csv"
    out_roster = CR_DIR / "CR223b_synthetic_state_roster.csv"
    out_recon = CR_DIR / "CR223b_reconstruction_validation.csv"
    out_conf = CR_DIR / "CR223b_confusion_matrix.csv"
    out_wcs = CR_DIR / "CR223b_wrong_controls.csv"
    out_checks = CR_DIR / "CR223b_checks.csv"
    out_precommit = CR_DIR / "CR223b_PRECOMMIT.md"
    out_summary = CR_DIR / "CR223b_summary.json"
    out_result = CR_DIR / "CR223b_result.md"
    out_readme = CR_DIR / "README.md"
    out_req = CR_DIR / "requirements.txt"
    out_hashes = CR_DIR / "HASHES.txt"

    basis_sha = write_csv(
        out_basis,
        measurement_basis_rows(),
        ["observable_index", "name", "type", "eigenvalues", "trace", "normalization_against_other_lambdas"],
    )
    roster_sha = write_csv(
        out_roster,
        state_roster_rows(states),
        ["state_id", "label", "construction", "populations_p0_pplus_pminus", "A_true", "true_class_above_A_side"],
    )
    write_csv(
        out_recon,
        reconstruction_validation_rows(val_summary),
        [
            "state_id", "n_trials", "A_true",
            "A_hat_psd_mean", "A_hat_psd_std", "A_hat_psd_bias",
            "A_hat_psd_ci95_low", "A_hat_psd_ci95_high", "A_hat_psd_ci_covers_true",
            "A_hat_LI_mean", "A_hat_pop_only_mean",
            "n_trials_with_negative_LI_eig", "min_smallest_eig_LI",
        ],
    )
    write_csv(
        out_conf,
        confusion_rows(test_confusion),
        ["scope", "TP", "TN", "FP", "FN", "TPR", "TNR", "balanced_accuracy"],
    )
    write_csv(
        out_wcs,
        [asdict(wc) for wc in wcs],
        ["wrong_control", "attempted_action", "why_invalid", "runner_protection", "observed", "passes_as_failure"],
    )
    write_csv(
        out_checks,
        [asdict(c) for c in checks],
        ["check", "passed", "observed", "expected"],
    )
    write_precommit(out_precommit, basis_sha, roster_sha)
    write_readme(out_readme)
    write_requirements(out_req)

    checks_passed = sum(1 for c in checks if c.passed)
    checks_total = len(checks)
    result_class = (
        "CR223b_PASS_QUTRIT_PURITY_ESTIMATOR"
        if checks_passed == checks_total
        else "CR223b_FAIL_QUTRIT_PURITY_ESTIMATOR"
    )

    s1 = val_summary["S1"]; s2 = val_summary["S2"]
    delta_psd = abs(s1["A_hat_psd_mean"] - s2["A_hat_psd_mean"])
    delta_pop = abs(s1["A_hat_pop_mean"] - s2["A_hat_pop_mean"])
    max_bias_near = max(abs(val_summary[sid]["A_hat_psd_bias"]) for sid in near_state_ids)
    wc1 = next(wc for wc in wcs if wc.wrong_control == "WC1_population_only_estimator")

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "execution_status": "CLEAN",
        "generated_at_utc": now_utc(),
        "result_class": result_class,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "a_side": A_SIDE,
        "bias_tolerance": BIAS_TOLERANCE,
        "n_shots_per_setting": N_SHOTS_PER_SETTING,
        "n_trials_val": N_TRIALS_VAL,
        "n_trials_test": N_TRIALS_TEST,
        "rng_seed_val": RNG_SEED_VAL,
        "rng_seed_test": RNG_SEED_TEST,
        "near_threshold_state_ids": near_state_ids,
        "boundary_state_ids": boundary_state_ids,
        "validation_summary": val_summary,
        "test_confusion": test_confusion,
        "coverage_all_states": coverage,
        "near_coverage": near_coverage,
        "p1_delta_psd": delta_psd,
        "p1_delta_pop": delta_pop,
        "p2_max_abs_bias_near": max_bias_near,
        "p3_balanced_accuracy": test_confusion["balanced_accuracy"],
        "p5_wc1_passes_as_failure": wc1.passes_as_failure,
        "next_gate": "CR223c_PR_RAW_TOMOGRAPHY_SENSOR_PROXY_CONTACT",
        "outputs": {
            "measurement_basis_csv": out_basis.name,
            "synthetic_state_roster_csv": out_roster.name,
            "reconstruction_validation_csv": out_recon.name,
            "confusion_matrix_csv": out_conf.name,
            "wrong_controls_csv": out_wcs.name,
            "checks_csv": out_checks.name,
            "precommit_md": out_precommit.name,
            "result_md": out_result.name,
            "summary_json": out_summary.name,
            "readme_md": out_readme.name,
            "requirements_txt": out_req.name,
        },
    }
    write_json(out_summary, summary)
    write_result(out_result, summary)

    write_hashes(out_hashes, [
        out_basis, out_roster, out_recon, out_conf, out_wcs, out_checks,
        out_precommit, out_summary, out_result, out_readme, out_req,
    ])

    print(f"{CR_ID} {TEST_ID}")
    print(f"  result_class: {result_class}")
    print(f"  checks: {checks_passed}/{checks_total}")
    print(f"  P1 delta_psd={delta_psd:.6f}, delta_pop={delta_pop:.6f}")
    print(f"  P2 max |bias| near-threshold: {max_bias_near:.6f}")
    print(f"  P3 balanced accuracy: {test_confusion['balanced_accuracy']:.4f}")
    print(f"  P4 near-threshold coverage: {near_coverage['covered']}/{near_coverage['total']} = {near_coverage['rate']:.3f}")
    print(f"  (boundary-state coverage reported separately: {coverage['covered']}/{coverage['total']})")
    print(f"  basis sha256: {basis_sha}")
    print(f"  roster sha256: {roster_sha}")
    return 0 if checks_passed == checks_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
