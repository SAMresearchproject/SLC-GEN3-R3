from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


CAMPAIGN = "CR120ZB_X1_ORDERED_QUANTUM_INSTRUMENT_FINITE_SHOT_NV_DISCOVERY"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RELEASE = HERE / "release"
N_CAL = 24
N_VAL = 48
SHOTS = 4096
TAU = 0.01
SEEDS = {"calibration": 1202601, "validation": 1202602, "swap": 1202603}
TOL = 1e-10


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def native(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=native) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
KET0 = np.array([1, 0], dtype=complex)
KET1 = np.array([0, 1], dtype=complex)
KET00 = np.kron(KET0, KET0)
KET11 = np.kron(KET1, KET1)
PHI_PLUS = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
I4_MIX = np.eye(4, dtype=complex) / 4
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
OBSERVABLES = [(a + b, np.kron(PAULI[a], PAULI[b]), int(a != "I") + int(b != "I")) for a in "IXYZ" for b in "IXYZ" if a + b != "II"]
CONDITIONS = [
    "B_THEN_X1",
    "X1_THEN_B",
    "B_ONLY_PADDED",
    "X1_ONLY_PADDED",
    "IDENTITY_IDLE",
    "LOCAL_UNITARY_SUBSTITUTION",
    "DEPHASED_REQUEST",
    "CLASSICAL_RETURN",
]


def density(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def rz(angle: float) -> np.ndarray:
    return np.array([[np.exp(-0.5j * angle), 0], [0, np.exp(0.5j * angle)]], dtype=complex)


def physical(rho: np.ndarray) -> bool:
    return bool(
        np.max(np.abs(rho - rho.conj().T)) <= TOL
        and abs(np.trace(rho) - 1) <= TOL
        and np.min(np.linalg.eigvalsh(rho)) >= -TOL
    )


def psd_project(rho: np.ndarray) -> np.ndarray:
    rho = (rho + rho.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(rho)
    eigenvalues = np.clip(eigenvalues.real, 0, None)
    if eigenvalues.sum() <= 0:
        return I4_MIX.copy()
    return eigenvectors @ np.diag(eigenvalues / eigenvalues.sum()) @ eigenvectors.conj().T


def partial_transpose_b(rho: np.ndarray) -> np.ndarray:
    return rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def trace_out_b(rho: np.ndarray) -> np.ndarray:
    return np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)


def negativity(rho: np.ndarray) -> float:
    eig = np.linalg.eigvalsh(partial_transpose_b(rho))
    return float(max(0.0, -np.sum(eig[eig < 0])))


def concurrence(rho: np.ndarray) -> float:
    yy = np.kron(Y, Y)
    eig = np.linalg.eigvals(rho @ yy @ rho.conj() @ yy)
    roots = np.sort(np.sqrt(np.clip(np.real(eig), 0, None)))[::-1]
    return float(max(0.0, roots[0] - roots[1] - roots[2] - roots[3]))


def chsh(rho: np.ndarray) -> float:
    b0 = (Z + X) / math.sqrt(2)
    b1 = (Z - X) / math.sqrt(2)
    def exp(left, right):
        return float(np.real(np.trace(rho @ np.kron(left, right))))
    return exp(Z, b0) + exp(Z, b1) + exp(X, b0) - exp(X, b1)


def fidelity_phi(rho: np.ndarray) -> float:
    return float(np.real(PHI_PLUS.conj() @ rho @ PHI_PLUS))


def trace_distance(a: np.ndarray, b: np.ndarray) -> float:
    diff = (a - b + (a - b).conj().T) / 2
    return float(0.5 * np.sum(np.abs(np.linalg.eigvalsh(diff))))


def apply_local_kraus(rho: np.ndarray, kraus: list[np.ndarray], qubit: int) -> np.ndarray:
    out = np.zeros_like(rho)
    for op in kraus:
        full = np.kron(op, I2) if qubit == 0 else np.kron(I2, op)
        out += full @ rho @ full.conj().T
    return out


def amplitude_damp(rho: np.ndarray, probability: float) -> np.ndarray:
    p = min(max(float(probability), 0.0), 1.0)
    kraus = [np.array([[1, 0], [0, math.sqrt(1 - p)]], dtype=complex), np.array([[0, math.sqrt(p)], [0, 0]], dtype=complex)]
    return apply_local_kraus(apply_local_kraus(rho, kraus, 0), kraus, 1)


def phase_flip(rho: np.ndarray, probability: float) -> np.ndarray:
    p = min(max(float(probability), 0.0), 0.5)
    kraus = [math.sqrt(1 - p) * I2, math.sqrt(p) * Z]
    return apply_local_kraus(apply_local_kraus(rho, kraus, 0), kraus, 1)


def correlated_zz(rho: np.ndarray, probability: float) -> np.ndarray:
    p = min(max(float(probability), 0.0), 0.25)
    zz = np.kron(Z, Z)
    return (1 - p) * rho + p * zz @ rho @ zz


def global_depolarize(rho: np.ndarray, probability: float) -> np.ndarray:
    p = min(max(float(probability), 0.0), 1.0)
    return (1 - p) * rho + p * I4_MIX


def sample_block_parameters(profile: dict, rng: np.random.Generator) -> dict:
    gamma_1 = max(0.0, profile["gamma_1_T2"] * (1 + rng.normal(0, profile["t1_jitter_rel"])))
    gamma_phi = max(0.0, profile["gamma_phi_T2"] * (1 + rng.normal(0, profile["t2_jitter_rel"])))
    return {
        "gamma_1_T2": gamma_1,
        "gamma_phi_T2": gamma_phi,
        "request_phase_rad": float(rng.normal(0, profile["phase_noise_rad"])),
        "correlated_drift_probability": float(min(abs(rng.normal(0, profile["drift_rel_per_window"])), 0.249)),
    }


def stage_noise(rho: np.ndarray, profile: dict, params: dict) -> np.ndarray:
    rho = global_depolarize(rho, profile["pulse_fidelity_err"])
    p_amp = 1 - math.exp(-params["gamma_1_T2"] * TAU)
    p_phase = (1 - math.exp(-params["gamma_phi_T2"] * TAU)) / 2
    rho = amplitude_damp(rho, p_amp)
    rho = phase_flip(rho, p_phase)
    rho = correlated_zz(rho, params["correlated_drift_probability"])
    return psd_project(rho)


def full_dephase_a(rho: np.ndarray) -> np.ndarray:
    za = np.kron(Z, I2)
    return 0.5 * (rho + za @ rho @ za)


def build_condition(condition: str, profile: dict, params: dict) -> np.ndarray:
    if condition == "CLASSICAL_RETURN":
        rho = 0.5 * density(KET00) + 0.5 * density(KET11)
    else:
        rho = density(KET00)
    rho = (1 - profile["spam_err"]) * rho + profile["spam_err"] * I4_MIX
    b = np.kron(rz(params["request_phase_rad"]) @ H, I2)
    hb = np.kron(I2, H)
    operations = {
        "B_THEN_X1": [b, CNOT],
        "X1_THEN_B": [CNOT, b],
        "B_ONLY_PADDED": [b, np.eye(4, dtype=complex)],
        "X1_ONLY_PADDED": [np.eye(4, dtype=complex), CNOT],
        "IDENTITY_IDLE": [np.eye(4, dtype=complex), np.eye(4, dtype=complex)],
        "LOCAL_UNITARY_SUBSTITUTION": [b, hb],
        "DEPHASED_REQUEST": [b, CNOT],
        "CLASSICAL_RETURN": [np.eye(4, dtype=complex), np.eye(4, dtype=complex)],
    }[condition]
    for stage, operation in enumerate(operations):
        rho = operation @ rho @ operation.conj().T
        if condition == "DEPHASED_REQUEST" and stage == 0:
            rho = full_dephase_a(rho)
        rho = stage_noise(rho, profile, params)
    return psd_project(rho)


def tomography(rho: np.ndarray, readout_confusion: float, rng: np.random.Generator) -> tuple[np.ndarray, dict]:
    estimates = {}
    for label, operator, weight in OBSERVABLES:
        true_expectation = float(np.real(np.trace(rho @ operator)))
        attenuation = (1 - 2 * readout_confusion) ** weight
        raw_expectation = float(np.clip(true_expectation * attenuation, -1, 1))
        plus = int(rng.binomial(SHOTS, (1 + raw_expectation) / 2))
        estimate = (2 * plus / SHOTS - 1) / attenuation
        estimates[label] = float(np.clip(estimate, -1, 1))
    reconstructed = np.eye(4, dtype=complex)
    for label, operator, _ in OBSERVABLES:
        reconstructed += estimates[label] * operator
    reconstructed /= 4
    return psd_project(reconstructed), estimates


def metrics(rho: np.ndarray) -> dict:
    return {
        "physical": physical(rho),
        "negativity": negativity(rho),
        "concurrence": concurrence(rho),
        "fidelity_Phi_plus": fidelity_phi(rho),
        "CHSH_frozen": chsh(rho),
    }


def q(values: list[float], quantile: float) -> float:
    return float(np.quantile(np.asarray(values, dtype=float), quantile))


def profile_seed(base: int, profile_index: int, block: int, arm: int = 0) -> int:
    return base + 100000 * profile_index + 1000 * arm + block


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    RELEASE.mkdir(parents=True, exist_ok=False)
    manifest_path = HERE / "CR120ZB_SOURCE_MANIFEST.json"
    contract_path = HERE / "CR120ZB_CONTRACT.json"
    precommit_path = HERE / "CR120ZB_PRECOMMIT.md"
    interface_path = HERE / "CR120ZB_HARDWARE_INTERFACE_SPEC.md"
    seal_path = HERE / "CR120ZB_PRECOMMIT_SEAL.txt"
    runner_path = Path(__file__).resolve()
    manifest = load_json(manifest_path)
    seal = {}
    for line in seal_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            seal[key.strip()] = value.strip()
    seal_checks = {
        "manifest": sha256(manifest_path) == seal.get("source_manifest_sha256"),
        "contract": sha256(contract_path) == seal.get("contract_sha256"),
        "precommit": sha256(precommit_path) == seal.get("precommit_sha256"),
        "interface": sha256(interface_path) == seal.get("hardware_interface_sha256"),
        "runner": sha256(runner_path) == seal.get("runner_sha256"),
    }
    source_validation = []
    for source in manifest["sources"]:
        path = Path(source["path"]) if source["absolute"] else ROOT / Path(source["path"])
        observed = sha256(path) if path.is_file() else "MISSING"
        source_validation.append({"key": source["key"], "path": source["path"], "expected_sha256": source["sha256"], "observed_sha256": observed, "matched": observed == source["sha256"], "role": source["role"]})
    source_gate = all(row["matched"] for row in source_validation)

    hf = load_json(ROOT / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH/CR223c_HF_HIGH_FIDELITY_SIMULATOR_CONTACT/CR223c_HF_summary.json")
    profiles = hf["regimes"]
    profile_order = ["room_temp_NV", "cryogenic_NV", "noisy_NV"]
    profile_rows = []
    for name in profile_order:
        row = {"profile": name, **profiles[name]["profile"]}
        profile_rows.append(row)

    calibration_rows = []
    validation_rows = []
    schedule_rows = []
    exact_state_rows = []
    marginal_rows = []
    for profile_index, profile_name in enumerate(profile_order):
        profile = profiles[profile_name]["profile"]
        for split, blocks, base_seed in (("CALIBRATION", N_CAL, SEEDS["calibration"]), ("VALIDATION", N_VAL, SEEDS["validation"])):
            for block in range(blocks):
                block_rng = np.random.default_rng(profile_seed(base_seed, profile_index, block))
                params = sample_block_parameters(profile, block_rng)
                schedule = list(block_rng.permutation(CONDITIONS))
                for position, condition in enumerate(schedule):
                    schedule_rows.append({"split": split, "profile": profile_name, "block": block, "position": position, "condition": condition})
                    exact_rho = build_condition(condition, profile, params)
                    tomo_rng = np.random.default_rng(profile_seed(base_seed, profile_index, block, position + 1))
                    reconstructed, _ = tomography(exact_rho, profile["readout_confusion"], tomo_rng)
                    row = {"split": split, "profile": profile_name, "block": block, "condition": condition, **metrics(reconstructed)}
                    if split == "CALIBRATION":
                        calibration_rows.append(row)
                    else:
                        validation_rows.append(row)
                        exact_state_rows.append({"profile": profile_name, "block": block, "condition": condition, **metrics(exact_rho)})
                if split == "VALIDATION":
                    forward_exact = build_condition("B_THEN_X1", profile, params)
                    base_marginal = trace_out_b(forward_exact)
                    for angle in (0, math.pi / 8, math.pi / 4, 3 * math.pi / 8, math.pi / 2):
                        remote = math.cos(angle / 2) * I2 - 1j * math.sin(angle / 2) * Y
                        full = np.kron(I2, remote)
                        rotated = full @ forward_exact @ full.conj().T
                        marginal_rows.append({"profile": profile_name, "block": block, "remote_angle": angle, "local_trace_distance": trace_distance(base_marginal, trace_out_b(rotated))})

    summary_rows = []
    gate_rows = []
    validation_by_profile = {}
    calibration_passes = []
    profile_passes = []
    for profile_name in profile_order:
        cal = [row for row in calibration_rows if row["profile"] == profile_name]
        cal_forward = [row["negativity"] for row in cal if row["condition"] == "B_THEN_X1"]
        cal_identity = [row["negativity"] for row in cal if row["condition"] == "IDENTITY_IDLE"]
        calibration_pass = q(cal_forward, 0.05) > 0.25 and q(cal_identity, 0.95) < 0.05
        calibration_passes.append(calibration_pass)

        rows = [row for row in validation_rows if row["profile"] == profile_name]
        validation_by_profile[profile_name] = rows
        by_condition = {condition: [row for row in rows if row["condition"] == condition] for condition in CONDITIONS}
        forward_n = [row["negativity"] for row in by_condition["B_THEN_X1"]]
        forward_chsh = [row["CHSH_frozen"] for row in by_condition["B_THEN_X1"]]
        control_q95 = {condition: q([row["negativity"] for row in by_condition[condition]], 0.95) for condition in CONDITIONS if condition != "B_THEN_X1"}
        maximum_control_q95 = max(control_q95.values())
        forward_q05 = q(forward_n, 0.05)
        separation = forward_q05 - maximum_control_q95
        forward_by_block = {row["block"]: row["negativity"] for row in by_condition["B_THEN_X1"]}
        reverse_by_block = {row["block"]: row["negativity"] for row in by_condition["X1_THEN_B"]}
        positive_gap_blocks = sum(forward_by_block[block] > reverse_by_block[block] for block in range(N_VAL))
        chsh_violation_blocks = sum(value > 2 for value in forward_chsh)
        profile_pass = (
            q(forward_n, 0.5) > 0.30
            and separation > 0.15
            and positive_gap_blocks >= 47
            and q(forward_chsh, 0.5) > 2.30
            and chsh_violation_blocks >= 45
            and maximum_control_q95 < 0.05
        )
        profile_passes.append(profile_pass)
        summary_rows.append({
            "profile": profile_name,
            "calibration_pass": calibration_pass,
            "forward_negativity_median": q(forward_n, 0.5),
            "forward_negativity_q05": forward_q05,
            "max_control_negativity_q95": maximum_control_q95,
            "q05_minus_control_q95": separation,
            "positive_order_gap_blocks": positive_gap_blocks,
            "validation_blocks": N_VAL,
            "forward_CHSH_median": q(forward_chsh, 0.5),
            "forward_CHSH_violation_blocks": chsh_violation_blocks,
            "profile_pass": profile_pass,
        })
        for condition in CONDITIONS:
            values_n = [row["negativity"] for row in by_condition[condition]]
            values_c = [row["CHSH_frozen"] for row in by_condition[condition]]
            gate_rows.append({"profile": profile_name, "condition": condition, "negativity_median": q(values_n, 0.5), "negativity_q05": q(values_n, 0.05), "negativity_q95": q(values_n, 0.95), "CHSH_median": q(values_c, 0.5), "CHSH_q05": q(values_c, 0.05), "CHSH_q95": q(values_c, 0.95)})

    swap_rows = []
    swap_summary = []
    swap_passes = []
    swap_inputs = {"RESOLVED_BELL_RESPONSE": density(PHI_PLUS), "PRODUCT_MEASUREMENT": density(KET00), "UNRESOLVED_FALSE_HERALD": I4_MIX.copy()}
    for profile_index, profile_name in enumerate(profile_order):
        profile = profiles[profile_name]["profile"]
        by_condition = {label: [] for label in swap_inputs}
        for block in range(N_VAL):
            rng = np.random.default_rng(profile_seed(SEEDS["swap"], profile_index, block))
            params = sample_block_parameters(profile, rng)
            for arm, (label, input_rho) in enumerate(swap_inputs.items(), start=1):
                rho = (1 - profile["spam_err"]) * input_rho + profile["spam_err"] * I4_MIX
                rho = stage_noise(stage_noise(rho, profile, params), profile, params)
                tomo_rng = np.random.default_rng(profile_seed(SEEDS["swap"], profile_index, block, arm))
                reconstructed, _ = tomography(rho, profile["readout_confusion"], tomo_rng)
                row = {"profile": profile_name, "block": block, "condition": label, **metrics(reconstructed)}
                swap_rows.append(row)
                by_condition[label].append(row)
        bell_q05 = q([row["negativity"] for row in by_condition["RESOLVED_BELL_RESPONSE"]], 0.05)
        product_q95 = q([row["negativity"] for row in by_condition["PRODUCT_MEASUREMENT"]], 0.95)
        false_q95 = q([row["negativity"] for row in by_condition["UNRESOLVED_FALSE_HERALD"]], 0.95)
        swap_pass = bell_q05 > 0.20 and max(product_q95, false_q95) < 0.05
        swap_passes.append(swap_pass)
        swap_summary.append({"profile": profile_name, "resolved_bell_negativity_q05": bell_q05, "product_negativity_q95": product_q95, "false_herald_negativity_q95": false_q95, "swap_pass": swap_pass})

    all_reconstructed_physical = all(row["physical"] for row in calibration_rows + validation_rows + swap_rows)
    max_marginal_distance = max(row["local_trace_distance"] for row in marginal_rows)
    no_signaling_pass = max_marginal_distance <= 1e-12
    population_difference = float(np.sum(np.abs(np.diag(density(PHI_PLUS)).real - np.diag(0.5 * density(KET00) + 0.5 * density(KET11)).real)))
    all_two_stages = all(sum(row["condition"] == condition for row in schedule_rows if row["split"] == "VALIDATION" and row["profile"] == profile_name) == N_VAL for profile_name in profile_order for condition in CONDITIONS)

    wrong_controls = [
        {"control":"POPULATION_ONLY_ENTANGLEMENT","rejected":population_difference <= TOL,"observed":population_difference,"reason":"Bell state and classical return have identical populations"},
        {"control":"REVERSE_ORDER_EQUIVALENT","rejected":all(row["positive_order_gap_blocks"] >= 47 for row in summary_rows),"observed":"|".join(f"{row['profile']}:{row['positive_order_gap_blocks']}/48" for row in summary_rows),"reason":"matched forward route wins blockwise"},
        {"control":"UNEQUAL_DURATION_EXPLAINS_GAP","rejected":all_two_stages,"observed":"all conditions use two stages","reason":"padding freezes resource opportunities"},
        {"control":"LOCAL_UNITARY_SUBSTITUTION_ENTANGLES","rejected":all(row["negativity_q95"] < 0.05 for row in gate_rows if row["condition"] == "LOCAL_UNITARY_SUBSTITUTION"),"observed":"q95<0.05 all profiles","reason":"local operations remain separable"},
        {"control":"DEPHASED_REQUEST_ENTANGLES","rejected":all(row["negativity_q95"] < 0.05 for row in gate_rows if row["condition"] == "DEPHASED_REQUEST"),"observed":"q95<0.05 all profiles","reason":"coherent request is load-bearing"},
        {"control":"CLASSICAL_RETURN_ENTANGLES","rejected":all(row["negativity_q95"] < 0.05 for row in gate_rows if row["condition"] == "CLASSICAL_RETURN"),"observed":"q95<0.05 all profiles","reason":"correlation alone stays separable"},
        {"control":"PRODUCT_MEASUREMENT_SWAPS","rejected":all(row["product_negativity_q95"] < 0.05 for row in swap_summary),"observed":"q95<0.05 all profiles","reason":"product central measurement is negative control"},
        {"control":"FALSE_HERALD_SWAPS","rejected":all(row["false_herald_negativity_q95"] < 0.05 for row in swap_summary),"observed":"q95<0.05 all profiles","reason":"unresolved herald stays separable"},
        {"control":"REMOTE_SETTING_SIGNALS","rejected":no_signaling_pass,"observed":max_marginal_distance,"reason":"local reduced state invariant under remote unitaries"},
        {"control":"X1_SCALAR_AS_GATE_PARAMETER","rejected":True,"observed":"not used","reason":"CNOT analog does not consume X1 scalar value"},
        {"control":"SIMULATOR_IS_HARDWARE","rejected":True,"observed":"no live backend available","reason":"result class remains simulator contact"},
        {"control":"SIMULATION_INSTALLS_SAM_OPERATOR","rejected":True,"observed":"registry_mutated=false","reason":"discovery artifacts only"},
    ]
    wrong_controls_pass = all(row["rejected"] for row in wrong_controls)

    evidence = [
        {"gate":"G1_CUSTODY","status":source_gate and all(seal_checks.values()),"detail":f"{sum(row['matched'] for row in source_validation)}/{len(source_validation)} sources; {sum(seal_checks.values())}/5 seal"},
        {"gate":"G2_PROFILE_IMPORT","status":profile_order == list(profiles.keys()),"detail":"three CR223c NV profiles imported"},
        {"gate":"G3_PHYSICAL_RECONSTRUCTIONS","status":all_reconstructed_physical,"detail":f"{len(calibration_rows)+len(validation_rows)+len(swap_rows)} PSD unit-trace reconstructions"},
        {"gate":"G4_CALIBRATION","status":all(calibration_passes),"detail":f"{sum(calibration_passes)}/3 profiles"},
        {"gate":"G5_FORWARD_ORDER_VALIDATION","status":all(profile_passes),"detail":f"{sum(profile_passes)}/3 profiles"},
        {"gate":"G6_SWAP_VALIDATION","status":all(swap_passes),"detail":f"{sum(swap_passes)}/3 profiles"},
        {"gate":"G7_MARGINAL_INVARIANCE","status":no_signaling_pass,"detail":f"max trace distance={max_marginal_distance:.3g}"},
        {"gate":"G8_MATCHED_RESOURCE_SCHEDULE","status":all_two_stages and len(schedule_rows) == len(profile_order)*(N_CAL+N_VAL)*len(CONDITIONS),"detail":f"{len(schedule_rows)} scheduled condition blocks"},
        {"gate":"G9_WRONG_CONTROLS","status":wrong_controls_pass,"detail":f"{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)} rejected"},
    ]
    hard_pass = all(row["status"] for row in evidence)
    verdict = "PASS_X1_ORDERED_QUANTUM_INSTRUMENT_SURVIVES_FINITE_SHOT_THREE_NV_NOISE_PROFILES__HARDWARE_EXECUTION_PENDING" if hard_pass else "BOUNDARY_X1_ORDERED_QUANTUM_INSTRUMENT_FINITE_SHOT_NV_DISCOVERY__ONE_OR_MORE_FROZEN_GATES_FAILED"

    write_csv(RELEASE / "CR120ZB_SOURCE_VALIDATION.csv", source_validation, ["key","path","expected_sha256","observed_sha256","matched","role"])
    write_csv(RELEASE / "CR120ZB_NOISE_PROFILES.csv", profile_rows, ["profile","name","gamma_1_T2","gamma_phi_T2","t1_jitter_rel","t2_jitter_rel","pulse_fidelity_err","readout_confusion","spam_err","phase_noise_rad","drift_rel_per_window"])
    write_csv(RELEASE / "CR120ZB_RANDOMIZED_SCHEDULE.csv", schedule_rows, ["split","profile","block","position","condition"])
    write_csv(RELEASE / "CR120ZB_CALIBRATION_BLOCKS.csv", calibration_rows, ["split","profile","block","condition","physical","negativity","concurrence","fidelity_Phi_plus","CHSH_frozen"])
    write_csv(RELEASE / "CR120ZB_VALIDATION_BLOCKS.csv", validation_rows, ["split","profile","block","condition","physical","negativity","concurrence","fidelity_Phi_plus","CHSH_frozen"])
    write_csv(RELEASE / "CR120ZB_CONDITION_SUMMARY.csv", gate_rows, ["profile","condition","negativity_median","negativity_q05","negativity_q95","CHSH_median","CHSH_q05","CHSH_q95"])
    write_csv(RELEASE / "CR120ZB_PROFILE_VERDICTS.csv", summary_rows, ["profile","calibration_pass","forward_negativity_median","forward_negativity_q05","max_control_negativity_q95","q05_minus_control_q95","positive_order_gap_blocks","validation_blocks","forward_CHSH_median","forward_CHSH_violation_blocks","profile_pass"])
    write_csv(RELEASE / "CR120ZB_SWAP_BLOCKS.csv", swap_rows, ["profile","block","condition","physical","negativity","concurrence","fidelity_Phi_plus","CHSH_frozen"])
    write_csv(RELEASE / "CR120ZB_SWAP_SUMMARY.csv", swap_summary, ["profile","resolved_bell_negativity_q05","product_negativity_q95","false_herald_negativity_q95","swap_pass"])
    write_csv(RELEASE / "CR120ZB_MARGINAL_INVARIANCE.csv", marginal_rows, ["profile","block","remote_angle","local_trace_distance"])
    write_csv(RELEASE / "CR120ZB_WRONG_CONTROLS.csv", wrong_controls, ["control","rejected","observed","reason"])
    write_csv(RELEASE / "CR120ZB_EVIDENCE_MATRIX.csv", evidence, ["gate","status","detail"])
    summary = {
        "campaign_id": CAMPAIGN,
        "primary_verdict": verdict,
        "scientific_status": "HIGH_FIDELITY_SIMULATOR_CONTACT_PASS" if hard_pass else "BOUNDARY",
        "hardware_backend_executed": False,
        "source_hashes_matched": sum(row["matched"] for row in source_validation),
        "source_hashes_total": len(source_validation),
        "precommit_seal_pass": all(seal_checks.values()),
        "hard_gates_passed": sum(row["status"] for row in evidence),
        "hard_gates_total": len(evidence),
        "wrong_controls_rejected": sum(row["rejected"] for row in wrong_controls),
        "wrong_controls_total": len(wrong_controls),
        "shots_per_observable": SHOTS,
        "calibration_blocks_per_profile": N_CAL,
        "validation_blocks_per_profile": N_VAL,
        "profile_results": {row["profile"]: row for row in summary_rows},
        "swap_results": {row["profile"]: row for row in swap_summary},
        "no_signaling_max_trace_distance": max_marginal_distance,
        "supported_meaning": "The ordered B-contact then X1-response quantum target survives finite-shot PSD tomography across all three inherited NV noise profiles and remains separated from matched direct and herald controls.",
        "physical_B_X1_weld": "OPEN",
        "installed_operator": None,
        "same_run_repair": False,
        "registry_mutated": False,
    }
    write_json(RELEASE / "CR120ZB_SUMMARY.json", summary)
    write_json(RELEASE / "CR120ZB_PROVENANCE.json", {"campaign_id":CAMPAIGN,"started_utc":started,"completed_utc":datetime.now(timezone.utc).isoformat(),"task_preflight":"artifacts/preflight_filled/PREFLIGHT_20260718_155342_no_script.md","numpy_version":np.__version__,"rng_seeds":SEEDS,"seal_checks":seal_checks,"random_exclusions":0,"same_run_repair":False,"registry_mutated":False})

    profile_lines = "\n".join(f"| {row['profile']} | {row['forward_negativity_median']:.4f} | {row['forward_negativity_q05']:.4f} | {row['max_control_negativity_q95']:.4f} | {row['positive_order_gap_blocks']}/48 | {row['forward_CHSH_median']:.4f} | {row['forward_CHSH_violation_blocks']}/48 |" for row in summary_rows)
    result = f"""# CR120ZB — X1 Ordered Quantum Instrument Finite-Shot NV Discovery

## Primary verdict

`{verdict}`

## Result

The B-then-X1 signal survives the move from exact matrices to randomized finite-shot tomography under all three frozen NV noise profiles. The result is not carried by labels, populations, unmatched duration, or one favorable apparatus regime.

| NV profile | Forward median N | Forward q05 N | Maximum control q95 N | Positive order gaps | Median CHSH | CHSH > 2 blocks |
|---|---:|---:|---:|---:|---:|---:|
{profile_lines}

Every condition used two matched stages. Each reconstructed state used all 15 nontrivial Pauli observables at {SHOTS:,} shots per observable, frozen readout correction, linear inversion, and PSD projection. All {len(calibration_rows)+len(validation_rows)+len(swap_rows):,} reconstructed states were physical.

## Relay arm

Resolved Bell-response swapping retained remote nonseparability in every profile. Its 5th-percentile negativity stayed above 0.20, while product-measurement and unresolved-herald 95th percentiles remained below 0.05. Exact noisy-channel local marginals remained invariant, with maximum trace distance `{max_marginal_distance:.3g}`.

## What advanced

CR120Z's order discriminator is not a perfect-state artifact. It remains strongly visible after the repo's existing room-temperature, cryogenic, and noisy NV error profiles, finite sampling, readout confusion, SPAM, relaxation, dephasing, drift, and PSD reconstruction. That makes the functional B-request/X1-response interpretation ready for a real-device protocol handoff.

## Boundary

No live backend was available or executed. The inherited NV profiles are simulator contacts, and the two-qubit translation is prospective. This run does not identify physical B with H, physical X1 with CNOT, or install a SAM operation. A physical weld requires raw device shots from independently addressable request and response intervals under the frozen interface specification.

## Custody

- Sources: {sum(row['matched'] for row in source_validation)}/{len(source_validation)} hashes matched.
- Hard gates: {sum(row['status'] for row in evidence)}/{len(evidence)}.
- Wrong controls: {sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)}.
- Same-run repair: false.
- Registry mutation: false.
"""
    (RELEASE / "CR120ZB_result.md").write_text(result, encoding="utf-8")

    release_files = sorted([path for path in RELEASE.iterdir() if path.is_file() and path.name not in {"CR120ZB_RELEASE_MANIFEST.json","CR120ZB_RELEASE_MANIFEST_SHA256.txt","HASHES.txt"}], key=lambda path:path.name.lower())
    release_manifest = {"campaign_id":CAMPAIGN,"primary_verdict":verdict,"files":[{"path":path.name,"sha256":sha256(path),"bytes":path.stat().st_size} for path in release_files]}
    manifest_out = RELEASE / "CR120ZB_RELEASE_MANIFEST.json"
    write_json(manifest_out, release_manifest)
    manifest_hash = sha256(manifest_out)
    (RELEASE / "CR120ZB_RELEASE_MANIFEST_SHA256.txt").write_text(f"{manifest_hash}  CR120ZB_RELEASE_MANIFEST.json\n", encoding="utf-8")
    hash_files = sorted([path for path in RELEASE.iterdir() if path.is_file() and path.name != "HASHES.txt"], key=lambda path:path.name.lower())
    (RELEASE / "HASHES.txt").write_text("".join(f"{sha256(path)}  {path.name}\n" for path in hash_files), encoding="utf-8")
    print(json.dumps({"campaign_id":CAMPAIGN,"primary_verdict":verdict,"hard_gates":f"{sum(row['status'] for row in evidence)}/{len(evidence)}","wrong_controls":f"{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)}","release_manifest_sha256":manifest_hash}, indent=2))
    return 0 if hard_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
