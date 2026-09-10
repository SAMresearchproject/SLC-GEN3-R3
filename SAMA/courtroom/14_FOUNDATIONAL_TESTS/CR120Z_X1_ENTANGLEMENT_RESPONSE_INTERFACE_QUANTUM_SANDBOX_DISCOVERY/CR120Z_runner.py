from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


CAMPAIGN = "CR120Z_X1_ENTANGLEMENT_RESPONSE_INTERFACE_QUANTUM_SANDBOX_DISCOVERY"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RELEASE = HERE / "release"
TOL = 1e-10


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
CNOT = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    dtype=complex,
)
KET0 = np.array([1, 0], dtype=complex)
KET1 = np.array([0, 1], dtype=complex)
KET00 = np.kron(KET0, KET0)
PHI_PLUS = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
PHI_MINUS = np.array([1, 0, 0, -1], dtype=complex) / math.sqrt(2)
PSI_PLUS = np.array([0, 1, 1, 0], dtype=complex) / math.sqrt(2)
PSI_MINUS = np.array([0, 1, -1, 0], dtype=complex) / math.sqrt(2)


def density(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def partial_transpose_b(rho: np.ndarray) -> np.ndarray:
    return rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def trace_out_b(rho: np.ndarray) -> np.ndarray:
    return np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)


def negativity(rho: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh(partial_transpose_b(rho))
    return float(max(0.0, -np.sum(eigenvalues[eigenvalues < 0])))


def concurrence(rho: np.ndarray) -> float:
    yy = np.kron(Y, Y)
    product = rho @ yy @ rho.conj() @ yy
    eigenvalues = np.linalg.eigvals(product)
    roots = np.sqrt(np.clip(np.real(eigenvalues), 0.0, None))
    roots = np.sort(roots)[::-1]
    return float(max(0.0, roots[0] - roots[1] - roots[2] - roots[3]))


def fidelity_phi(rho: np.ndarray) -> float:
    return float(np.real(PHI_PLUS.conj() @ rho @ PHI_PLUS))


def expectation(rho: np.ndarray, left: np.ndarray, right: np.ndarray) -> float:
    return float(np.real(np.trace(rho @ np.kron(left, right))))


def chsh(rho: np.ndarray) -> float:
    b0 = (Z + X) / math.sqrt(2)
    b1 = (Z - X) / math.sqrt(2)
    return (
        expectation(rho, Z, b0)
        + expectation(rho, Z, b1)
        + expectation(rho, X, b0)
        - expectation(rho, X, b1)
    )


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    diff = (rho - sigma + (rho - sigma).conj().T) / 2
    return float(0.5 * np.sum(np.abs(np.linalg.eigvalsh(diff))))


def physical_state(rho: np.ndarray) -> bool:
    return (
        np.max(np.abs(rho - rho.conj().T)) <= TOL
        and abs(np.trace(rho) - 1) <= TOL
        and np.min(np.linalg.eigvalsh(rho)) >= -TOL
    )


def state_metrics(label: str, rho: np.ndarray, route: str) -> dict:
    return {
        "state": label,
        "route": route,
        "physical": physical_state(rho),
        "negativity": negativity(rho),
        "concurrence": concurrence(rho),
        "fidelity_Phi_plus": fidelity_phi(rho),
        "CHSH_frozen": chsh(rho),
        "CHSH_exceeds_2": chsh(rho) > 2 + TOL,
    }


def herald_remote(measurement: np.ndarray) -> tuple[np.ndarray, float]:
    four_qubit = np.kron(PHI_PLUS, PHI_PLUS).reshape(2, 2, 2, 2)
    effect = measurement.reshape(2, 2)
    remote = np.einsum("bc,abcd->ad", effect.conj(), four_qubit).reshape(4)
    probability = float(np.vdot(remote, remote).real)
    remote = remote / math.sqrt(probability)
    return density(remote), probability


def make_html(summary: dict, state_rows: list[dict], swap_rows: list[dict]) -> str:
    cards = "\n".join(
        f"<article class='card {'win' if row['state']=='B_THEN_X1' else ''}'><h3>{row['state'].replace('_',' ')}</h3><p>{row['route']}</p><dl><dt>Negativity</dt><dd>{row['negativity']:.6f}</dd><dt>Concurrence</dt><dd>{row['concurrence']:.6f}</dd><dt>CHSH</dt><dd>{row['CHSH_frozen']:.6f}</dd></dl></article>"
        for row in state_rows
    )
    swap_cards = "\n".join(
        f"<article class='card {'win' if row['condition']=='X1_BELL_RESPONSE' else ''}'><h3>{row['condition'].replace('_',' ')}</h3><dl><dt>Herald probability</dt><dd>{row['probability']:.4f}</dd><dt>Remote negativity</dt><dd>{row['negativity']:.6f}</dd><dt>Remote CHSH</dt><dd>{row['CHSH_frozen']:.6f}</dd></dl></article>"
        for row in swap_rows
    )
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>CR120Z X1 Quantum Sandbox</title>
<style>
:root{{--ink:#eaf2ff;--muted:#9eb0c9;--panel:#101b2d;--line:#28405e;--cyan:#5ee8ff;--violet:#aa7cff;--green:#70f0ad;--bg:#07101f}}*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 15% 0,#17284a 0,#07101f 45%);color:var(--ink);font-family:Inter,Segoe UI,sans-serif}}main{{max-width:1150px;margin:auto;padding:42px 24px 80px}}.eyebrow{{letter-spacing:.18em;color:var(--cyan);font-size:.78rem}}h1{{font-size:clamp(2.2rem,5vw,4.8rem);line-height:.95;margin:.4rem 0 1rem}}.lead{{max-width:780px;color:var(--muted);font-size:1.1rem}}.circuit{{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;align-items:center;gap:12px;margin:34px 0;padding:22px;background:#0b1629cc;border:1px solid var(--line);border-radius:18px}}.node{{padding:20px;text-align:center;border:1px solid var(--line);border-radius:14px;background:var(--panel)}}.node strong{{display:block;color:var(--cyan);font-size:1.25rem}}.arrow{{color:var(--violet);font-size:2rem}}section{{margin-top:38px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}.card{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px}}.card.win{{border-color:var(--green);box-shadow:0 0 28px #70f0ad22}}.card h3{{margin-top:0;font-size:1rem}}.card p{{color:var(--muted);min-height:48px}}dl{{display:grid;grid-template-columns:1fr auto;gap:7px;margin-bottom:0}}dt{{color:var(--muted)}}dd{{margin:0;font-variant-numeric:tabular-nums}}.lab{{padding:24px;background:linear-gradient(135deg,#101b2d,#15152e);border:1px solid var(--violet);border-radius:18px}}input[type=range]{{width:100%;accent-color:var(--cyan)}}.meters{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.meter{{padding:14px;background:#07101faa;border-radius:12px}}.meter b{{display:block;font-size:1.5rem;color:var(--cyan)}}footer{{margin-top:46px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:.9rem}}@media(max-width:650px){{.circuit{{grid-template-columns:1fr}}.arrow{{transform:rotate(90deg);text-align:center}}.meters{{grid-template-columns:1fr}}}}
</style></head><body><main>
<div class='eyebrow'>CR120Z · DETERMINISTIC QUANTUM SANDBOX</div><h1>B requests.<br>X1 responds.</h1>
<p class='lead'>A minimal standard quantum realization of the archived relay order. The result is an existence proof: the typed grammar can carry entanglement without turning B and X1 into the same thing.</p>
<div class='circuit'><div class='node'><strong>|00&gt;</strong>separable input</div><div class='arrow'>→</div><div class='node'><strong>B : H<sub>A</sub></strong>local coherent request</div><div class='arrow'>→</div><div class='node'><strong>X1 : CNOT</strong>joint response → |Φ+&gt;</div></div>
<section><h2>Order and direct controls</h2><div class='grid'>{cards}</div></section>
<section><h2>Entanglement-swapping arm</h2><div class='grid'>{swap_cards}</div></section>
<section class='lab'><h2>Noise visibility lab</h2><p>Move visibility <em>v</em> for ρ(v)=v|Φ+⟩⟨Φ+|+(1-v)I/4.</p><input id='v' type='range' min='0' max='1' step='0.005' value='1'><div class='meters'><div class='meter'>Visibility<b id='vv'>1.000</b></div><div class='meter'>Negativity<b id='neg'>0.500</b></div><div class='meter'>CHSH<b id='bell'>2.828</b></div></div><p id='status'></p></section>
<footer>Verdict: {summary['primary_verdict']}<br>Simulation only. No SAM registry mutation and no physical X1 identification.</footer>
<script>const v=document.querySelector('#v'),vv=document.querySelector('#vv'),n=document.querySelector('#neg'),b=document.querySelector('#bell'),s=document.querySelector('#status');function draw(){{const x=+v.value,neg=Math.max(0,(3*x-1)/4),bell=2*Math.sqrt(2)*x;vv.textContent=x.toFixed(3);n.textContent=neg.toFixed(3);b.textContent=bell.toFixed(3);s.textContent=(neg>0?'Nonseparable':'Separable')+' · '+(bell>2?'CHSH violation':'Bell-local under frozen settings');}}v.addEventListener('input',draw);draw();</script>
</main></body></html>"""


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    RELEASE.mkdir(parents=True, exist_ok=False)

    manifest_path = HERE / "CR120Z_SOURCE_MANIFEST.json"
    contract_path = HERE / "CR120Z_CONTRACT.json"
    precommit_path = HERE / "CR120Z_PRECOMMIT.md"
    seal_path = HERE / "CR120Z_PRECOMMIT_SEAL.txt"
    runner_path = Path(__file__).resolve()
    manifest = load_json(manifest_path)
    seal = {}
    for line in seal_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            seal[key.strip()] = value.strip()
    seal_checks = {
        "source_manifest": sha256(manifest_path) == seal.get("source_manifest_sha256"),
        "contract": sha256(contract_path) == seal.get("contract_sha256"),
        "precommit": sha256(precommit_path) == seal.get("precommit_sha256"),
        "runner": sha256(runner_path) == seal.get("runner_sha256"),
    }

    source_validation = []
    for source in manifest["sources"]:
        path = Path(source["path"]) if source["absolute"] else ROOT / Path(source["path"])
        observed = sha256(path) if path.is_file() else "MISSING"
        source_validation.append(
            {
                "key": source["key"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "observed_sha256": observed,
                "matched": observed == source["sha256"],
                "role": source["role"],
            }
        )
    source_gate = all(row["matched"] for row in source_validation)

    cr120v = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_summary.json")
    starbreaker = load_json(ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_SUBSTRATE_RECORD_RELAY_KINEMATICS_V1/release/SUBSTRATE_RECORD_RELAY_KINEMATICS_SUMMARY.json")
    hierarchy = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER/CR119_typed_hierarchy.json")
    nodes = {row["id"]: row for row in hierarchy["nodes"]}
    type_gate = (
        nodes["B_CONTACT_OPERATOR"]["type"] == "ContactOperator"
        and nodes["B_CONTACT_OPERATOR"]["value"] is None
        and nodes["X1_AXIS_SELF_CHANNEL"]["type"] == "AxisChannel"
        and nodes["X1_AXIS_SELF_CHANNEL"]["value"] == 1
        and cr120v["typed_B_request_X1_response"] == "SUPPORTED_AS_ARCHIVAL_HYPOTHESIS_WELD_OPEN"
        and starbreaker["relay_panel"]["overall_typed_specificity_supported"]
    )

    b_gate = np.kron(H, I2)
    state_b_only = b_gate @ KET00
    state_x1_only = CNOT @ KET00
    state_b_then_x1 = CNOT @ b_gate @ KET00
    state_x1_then_b = b_gate @ CNOT @ KET00
    rho_classical = 0.5 * density(KET00) + 0.5 * density(np.kron(KET1, KET1))
    states = {
        "INPUT": density(KET00),
        "B_ONLY": density(state_b_only),
        "X1_ONLY": density(state_x1_only),
        "B_THEN_X1": density(state_b_then_x1),
        "X1_THEN_B": density(state_x1_then_b),
        "CLASSICAL_RETURN": rho_classical,
    }
    routes = {
        "INPUT": "|00>",
        "B_ONLY": "H_A |00>",
        "X1_ONLY": "CNOT |00>",
        "B_THEN_X1": "CNOT (H_A |00>)",
        "X1_THEN_B": "H_A (CNOT |00>)",
        "CLASSICAL_RETURN": "1/2 |00><00| + 1/2 |11><11|",
    }
    state_rows = [state_metrics(label, rho, routes[label]) for label, rho in states.items()]
    state_by_label = {row["state"]: row for row in state_rows}
    all_direct_physical = all(row["physical"] for row in state_rows)

    candidate = state_by_label["B_THEN_X1"]
    control_labels = ["B_ONLY", "X1_ONLY", "X1_THEN_B", "CLASSICAL_RETURN"]
    controls_separable = all(state_by_label[label]["negativity"] <= TOL for label in control_labels)
    controls_bell_local = all(state_by_label[label]["CHSH_frozen"] <= 2 + TOL for label in control_labels)
    candidate_exact = (
        abs(candidate["negativity"] - 0.5) <= TOL
        and abs(candidate["concurrence"] - 1.0) <= TOL
        and abs(candidate["fidelity_Phi_plus"] - 1.0) <= TOL
        and abs(candidate["CHSH_frozen"] - 2 * math.sqrt(2)) <= TOL
    )
    order_gate = candidate["negativity"] > TOL and state_by_label["X1_THEN_B"]["negativity"] <= TOL

    marginal_reference = trace_out_b(states["B_THEN_X1"])
    marginal_rows = []
    for angle in (0, math.pi / 8, math.pi / 4, 3 * math.pi / 8, math.pi / 2):
        unitary_b = math.cos(angle / 2) * I2 - 1j * math.sin(angle / 2) * Y
        full = np.kron(I2, unitary_b)
        transformed = full @ states["B_THEN_X1"] @ full.conj().T
        distance = trace_distance(marginal_reference, trace_out_b(transformed))
        marginal_rows.append(
            {
                "remote_angle_rad": angle,
                "local_A_trace_distance": distance,
                "invariant_within_1e_12": distance <= 1e-12,
            }
        )
    no_signaling_gate = all(row["invariant_within_1e_12"] for row in marginal_rows)

    swap_rows = []
    bell_remote, bell_probability = herald_remote(PHI_PLUS)
    product_remote, product_probability = herald_remote(KET00)
    bell_basis = [PHI_PLUS, PHI_MINUS, PSI_PLUS, PSI_MINUS]
    unresolved = np.zeros((4, 4), dtype=complex)
    total_probability = 0.0
    for measurement in bell_basis:
        remote, probability = herald_remote(measurement)
        unresolved += probability * remote
        total_probability += probability
    unresolved /= total_probability
    swap_states = {
        "X1_BELL_RESPONSE": (bell_remote, bell_probability),
        "PRODUCT_MEASUREMENT_CONTROL": (product_remote, product_probability),
        "FALSE_UNRESOLVED_HERALD_CONTROL": (unresolved, total_probability),
    }
    for label, (rho, probability) in swap_states.items():
        row = state_metrics(label, rho, "central B-C measurement; remote A-D readout")
        row = {"condition": label, "probability": probability, **{key: value for key, value in row.items() if key not in {"state", "route"}}}
        swap_rows.append(row)
    swap_by_label = {row["condition"]: row for row in swap_rows}
    swapping_gate = (
        abs(swap_by_label["X1_BELL_RESPONSE"]["negativity"] - 0.5) <= TOL
        and abs(swap_by_label["X1_BELL_RESPONSE"]["concurrence"] - 1.0) <= TOL
        and swap_by_label["X1_BELL_RESPONSE"]["CHSH_frozen"] > 2
        and swap_by_label["PRODUCT_MEASUREMENT_CONTROL"]["negativity"] <= TOL
        and swap_by_label["FALSE_UNRESOLVED_HERALD_CONTROL"]["negativity"] <= TOL
        and all(row["physical"] for row in swap_rows)
    )

    identity4 = np.eye(4, dtype=complex) / 4
    phi_density = density(PHI_PLUS)
    noise_rows = []
    for index in range(201):
        visibility = index / 200
        rho = visibility * phi_density + (1 - visibility) * identity4
        row = {
            "visibility": visibility,
            "negativity": negativity(rho),
            "CHSH_frozen": chsh(rho),
            "nonseparable": negativity(rho) > TOL,
            "CHSH_exceeds_2": chsh(rho) > 2 + TOL,
            "physical": physical_state(rho),
        }
        noise_rows.append(row)
    first_negative = next(row["visibility"] for row in noise_rows if row["nonseparable"])
    first_chsh = next(row["visibility"] for row in noise_rows if row["CHSH_exceeds_2"])
    expected_negative_grid = next(index / 200 for index in range(201) if index / 200 > 1 / 3)
    expected_chsh_grid = next(index / 200 for index in range(201) if index / 200 > 1 / math.sqrt(2))
    noise_gate = (
        abs(first_negative - expected_negative_grid) <= TOL
        and abs(first_chsh - expected_chsh_grid) <= TOL
        and all(row["physical"] for row in noise_rows)
    )

    matrix_rows = []
    for label, rho in {**states, **{key: value[0] for key, value in swap_states.items()}}.items():
        for row_index in range(4):
            for column_index in range(4):
                matrix_rows.append(
                    {
                        "state": label,
                        "row": row_index,
                        "column": column_index,
                        "real": float(np.real(rho[row_index, column_index])),
                        "imag": float(np.imag(rho[row_index, column_index])),
                    }
                )

    type_rows = [
        {"sam_entity": "B_CONTACT_OPERATOR", "frozen_sam_type": "ContactOperator", "sandbox_analog": "local H_A request preparation", "permitted_claim": "prospective local request operation", "forbidden_conversion": "B=1/2 or B=X1"},
        {"sam_entity": "X1_AXIS_SELF_CHANNEL", "frozen_sam_type": "AxisChannel(value=1)", "sandbox_analog": "joint CNOT response interface", "permitted_claim": "prospective response transformation", "forbidden_conversion": "1 as amplitude, qubit, phase, or identity matrix"},
        {"sam_entity": "W9_CLOSURE_WITNESS", "frozen_sam_type": "ClosureWitness(value=9)", "sandbox_analog": "none", "permitted_claim": "archival downstream closure only", "forbidden_conversion": "entanglement witness or Bell flag"},
        {"sam_entity": "THETA18_PRIMARY_CARRIER", "frozen_sam_type": "PrimaryCarrier(value=18)", "sandbox_analog": "none", "permitted_claim": "separate current carrier candidate", "forbidden_conversion": "X1 identity or spare quantum resource"},
    ]

    wrong_controls = [
        {"control": "B_EQUALS_X1", "rejected": type_gate, "observed": "ContactOperator != AxisChannel", "reason": "typed entities remain distinct"},
        {"control": "X1_SCALAR_AS_AMPLITUDE", "rejected": True, "observed": "not used", "reason": "sandbox map is typed independently of scalar value"},
        {"control": "HALF_SLOTS_AS_AMPLITUDES", "rejected": True, "observed": "not used", "reason": "route weights have no Hilbert-space conversion"},
        {"control": "W9_AS_ENTANGLEMENT_WITNESS", "rejected": True, "observed": "no W9 quantum observable", "reason": "closure witness is not retyped"},
        {"control": "B_ONLY_ENTANGLES", "rejected": state_by_label["B_ONLY"]["negativity"] <= TOL, "observed": state_by_label["B_ONLY"]["negativity"], "reason": "local preparation is separable"},
        {"control": "X1_ONLY_ENTANGLES", "rejected": state_by_label["X1_ONLY"]["negativity"] <= TOL, "observed": state_by_label["X1_ONLY"]["negativity"], "reason": "response without request is separable"},
        {"control": "REVERSE_ORDER_ENTANGLES", "rejected": state_by_label["X1_THEN_B"]["negativity"] <= TOL, "observed": state_by_label["X1_THEN_B"]["negativity"], "reason": "frozen order is discriminating"},
        {"control": "CLASSICAL_CORRELATION_IS_ENTANGLEMENT", "rejected": state_by_label["CLASSICAL_RETURN"]["negativity"] <= TOL, "observed": state_by_label["CLASSICAL_RETURN"]["negativity"], "reason": "classical return is correlated but separable"},
        {"control": "PRODUCT_MEASUREMENT_SWAPS_ENTANGLEMENT", "rejected": swap_by_label["PRODUCT_MEASUREMENT_CONTROL"]["negativity"] <= TOL, "observed": swap_by_label["PRODUCT_MEASUREMENT_CONTROL"]["negativity"], "reason": "product central effect does not entangle remote pair"},
        {"control": "FALSE_HERALD_SWAPS_ENTANGLEMENT", "rejected": swap_by_label["FALSE_UNRESOLVED_HERALD_CONTROL"]["negativity"] <= TOL, "observed": swap_by_label["FALSE_UNRESOLVED_HERALD_CONTROL"]["negativity"], "reason": "unresolved outcomes erase remote entanglement"},
        {"control": "REMOTE_SETTING_SIGNALS_LOCALLY", "rejected": no_signaling_gate, "observed": max(row["local_A_trace_distance"] for row in marginal_rows), "reason": "local marginal is invariant"},
        {"control": "SIMULATION_INSTALLS_OPERATOR", "rejected": True, "observed": "registry_mutated=false", "reason": "sandbox is non-runtime"},
    ]
    wrong_control_gate = all(row["rejected"] for row in wrong_controls)

    gates = [
        {"gate": "G1_SOURCE_AND_SEAL_CUSTODY", "status": source_gate and all(seal_checks.values()), "detail": f"{sum(row['matched'] for row in source_validation)}/{len(source_validation)} sources; {sum(seal_checks.values())}/4 seal"},
        {"gate": "G2_TYPE_PRESERVATION", "status": type_gate, "detail": "B ContactOperator distinct from X1 AxisChannel; Starbreaker typed specificity retained"},
        {"gate": "G3_DENSITY_MATRIX_VALIDITY", "status": all_direct_physical and all(row["physical"] for row in swap_rows) and all(row["physical"] for row in noise_rows), "detail": "direct, swapping, and 201 noise states physical"},
        {"gate": "G4_ORDERED_NONSEPARABILITY", "status": candidate_exact and order_gate, "detail": f"N={candidate['negativity']:.12g}; C={candidate['concurrence']:.12g}; CHSH={candidate['CHSH_frozen']:.12g}"},
        {"gate": "G5_DIRECT_CONTROLS", "status": controls_separable and controls_bell_local, "detail": "B-only, X1-only, reverse, classical return separable and CHSH<=2"},
        {"gate": "G6_NO_SIGNALING_MARGINAL", "status": no_signaling_gate, "detail": f"max trace distance={max(row['local_A_trace_distance'] for row in marginal_rows):.3g}"},
        {"gate": "G7_ENTANGLEMENT_SWAPPING", "status": swapping_gate, "detail": f"Bell response N={swap_by_label['X1_BELL_RESPONSE']['negativity']:.6g}; controls N=0"},
        {"gate": "G8_NOISE_THRESHOLDS", "status": noise_gate, "detail": f"first N>0 v={first_negative}; first CHSH>2 v={first_chsh}"},
        {"gate": "G9_WRONG_CONTROLS", "status": wrong_control_gate, "detail": f"{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)} rejected"},
    ]
    hard_pass = all(row["status"] for row in gates)
    primary_verdict = (
        "PASS_X1_RESPONSE_INTERFACE_QUANTUM_CAPABLE_SANDBOX__ORDERED_B_THEN_X1_GENERATES_AND_HERALDS_NONSEPARABILITY__PHYSICAL_WELD_OPEN"
        if hard_pass
        else "BOUNDARY_X1_QUANTUM_SANDBOX__ONE_OR_MORE_FROZEN_DISCRIMINATORS_FAILED"
    )

    summary = {
        "campaign_id": CAMPAIGN,
        "primary_verdict": primary_verdict,
        "scientific_status": "CONSTRUCTIVE_SANDBOX_PASS" if hard_pass else "BOUNDARY",
        "hard_gates_passed": sum(row["status"] for row in gates),
        "hard_gates_total": len(gates),
        "source_hashes_matched": sum(row["matched"] for row in source_validation),
        "source_hashes_total": len(source_validation),
        "precommit_seal_pass": all(seal_checks.values()),
        "ordered_candidate": candidate,
        "direct_controls_separable": controls_separable,
        "reverse_order_separable": state_by_label["X1_THEN_B"]["negativity"] <= TOL,
        "no_signaling_max_trace_distance": max(row["local_A_trace_distance"] for row in marginal_rows),
        "swapping": {row["condition"]: {key: value for key, value in row.items() if key != "condition"} for row in swap_rows},
        "noise_visibility": {
            "grid_step": 0.005,
            "first_nonseparable": first_negative,
            "analytic_boundary": 1 / 3,
            "first_CHSH_violation": first_chsh,
            "analytic_CHSH_boundary": 1 / math.sqrt(2),
        },
        "wrong_controls_rejected": sum(row["rejected"] for row in wrong_controls),
        "wrong_controls_total": len(wrong_controls),
        "supported_meaning": "The typed B-contact then X1-response grammar admits a minimal standard quantum realization in which the distinct response creates or heralds nonseparability and the ordering is essential.",
        "physical_weld_status": "OPEN",
        "installed_operator": None,
        "registry_mutated": False,
        "same_run_repair": False,
    }

    write_csv(RELEASE / "CR120Z_SOURCE_VALIDATION.csv", source_validation, ["key", "path", "expected_sha256", "observed_sha256", "matched", "role"])
    write_csv(RELEASE / "CR120Z_TYPE_BRIDGE.csv", type_rows, ["sam_entity", "frozen_sam_type", "sandbox_analog", "permitted_claim", "forbidden_conversion"])
    write_csv(RELEASE / "CR120Z_DIRECT_STATE_METRICS.csv", state_rows, ["state", "route", "physical", "negativity", "concurrence", "fidelity_Phi_plus", "CHSH_frozen", "CHSH_exceeds_2"])
    write_csv(RELEASE / "CR120Z_DENSITY_MATRICES.csv", matrix_rows, ["state", "row", "column", "real", "imag"])
    write_csv(RELEASE / "CR120Z_NO_SIGNALING_MARGINALS.csv", marginal_rows, ["remote_angle_rad", "local_A_trace_distance", "invariant_within_1e_12"])
    write_csv(RELEASE / "CR120Z_SWAP_METRICS.csv", swap_rows, ["condition", "probability", "physical", "negativity", "concurrence", "fidelity_Phi_plus", "CHSH_frozen", "CHSH_exceeds_2"])
    write_csv(RELEASE / "CR120Z_NOISE_SCAN.csv", noise_rows, ["visibility", "negativity", "CHSH_frozen", "nonseparable", "CHSH_exceeds_2", "physical"])
    write_csv(RELEASE / "CR120Z_WRONG_CONTROLS.csv", wrong_controls, ["control", "rejected", "observed", "reason"])
    write_csv(RELEASE / "CR120Z_EVIDENCE_MATRIX.csv", gates, ["gate", "status", "detail"])
    write_json(RELEASE / "CR120Z_SUMMARY.json", summary)
    write_json(
        RELEASE / "CR120Z_PROVENANCE.json",
        {
            "campaign_id": CAMPAIGN,
            "started_utc": started,
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "task_preflight": "artifacts/preflight_filled/PREFLIGHT_20260718_153332_no_script.md",
            "numpy_version": np.__version__,
            "source_manifest_sha256": sha256(manifest_path),
            "contract_sha256": sha256(contract_path),
            "precommit_sha256": sha256(precommit_path),
            "runner_sha256": sha256(runner_path),
            "seal_checks": seal_checks,
            "randomness": "NONE",
            "fitting": "NONE",
            "same_run_repair": False,
            "registry_mutated": False,
        },
    )

    result = f"""# CR120Z — X1 Entanglement-Response Quantum Sandbox

## Primary verdict

`{primary_verdict}`

## The fun result

The archived relay grammar has a clean quantum realization. In the frozen minimal model, B first creates a local coherent request and X1 then supplies a distinct controlled response:

```text
|00> -- B:H_A -- X1:CNOT_A->B --> |Phi+>
```

That ordered route produces a maximally entangled state:

- negativity: `{candidate['negativity']:.12g}`
- concurrence: `{candidate['concurrence']:.12g}`
- fidelity with `|Phi+>`: `{candidate['fidelity_Phi_plus']:.12g}`
- frozen-setting CHSH: `{candidate['CHSH_frozen']:.12g}` = `2 sqrt(2)`

The ordering is load-bearing. B alone, X1 alone, X1-before-B, and the classical correlated-return state all have zero negativity. Ordinary reciprocal correlation therefore does not pass as entanglement.

## Relay extension

The same response interpretation works as a central entanglement-swapping interface. An X1-indexed Bell response on the two middle systems heralds a remote pair with negativity `{swap_by_label['X1_BELL_RESPONSE']['negativity']:.12g}` and CHSH `{swap_by_label['X1_BELL_RESPONSE']['CHSH_frozen']:.12g}`. A product central measurement and an unresolved false herald both leave the remote pair separable.

Local marginals remain invariant across every frozen remote-setting rotation; the maximum trace distance is `{max(row['local_A_trace_distance'] for row in marginal_rows):.3g}`. The quantum relay changes joint correlations without becoming a controllable signal.

## Robustness

Under depolarizing noise, the first grid point with nonzero negativity is `v={first_negative}`, immediately above the analytic boundary `1/3`. The first frozen-setting CHSH violation is `v={first_chsh}`, immediately above `1/sqrt(2)`. No parameters were fitted.

## Supported interpretation

This establishes **quantum capability of the typed grammar**: a distinct B-contact followed by an X1-response can generate or herald nonseparability, and the order matters. It gives the X1 response-interface hypothesis a concrete mathematical target for later empirical or hardware work.

## Boundary

The chosen `H` and `CNOT` maps are a prospective minimal realization, not discovered physical definitions of B or X1. X1 is not equated with entanglement, its scalar value is not used as an amplitude, W9 is not used as a Bell witness, and no SAM operator was installed.

## Custody

- Sources: `{sum(row['matched'] for row in source_validation)}/{len(source_validation)}` hashes matched.
- Seal: `{'PASS' if all(seal_checks.values()) else 'FAIL'}`.
- Hard gates: `{sum(row['status'] for row in gates)}/{len(gates)}`.
- Wrong controls: `{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)}`.
- Same-run repair: `false`.
- Registry mutation: `false`.
"""
    (RELEASE / "CR120Z_result.md").write_text(result, encoding="utf-8")
    (RELEASE / "CR120Z_QUANTUM_SANDBOX.html").write_text(make_html(summary, state_rows, swap_rows), encoding="utf-8")

    release_files = sorted(
        [path for path in RELEASE.iterdir() if path.is_file() and path.name not in {"CR120Z_RELEASE_MANIFEST.json", "CR120Z_RELEASE_MANIFEST_SHA256.txt", "HASHES.txt"}],
        key=lambda path: path.name.lower(),
    )
    release_manifest = {
        "campaign_id": CAMPAIGN,
        "primary_verdict": primary_verdict,
        "files": [{"path": path.name, "sha256": sha256(path), "bytes": path.stat().st_size} for path in release_files],
    }
    release_manifest_path = RELEASE / "CR120Z_RELEASE_MANIFEST.json"
    write_json(release_manifest_path, release_manifest)
    release_manifest_hash = sha256(release_manifest_path)
    (RELEASE / "CR120Z_RELEASE_MANIFEST_SHA256.txt").write_text(f"{release_manifest_hash}  CR120Z_RELEASE_MANIFEST.json\n", encoding="utf-8")
    hash_files = sorted([path for path in RELEASE.iterdir() if path.is_file() and path.name != "HASHES.txt"], key=lambda path: path.name.lower())
    (RELEASE / "HASHES.txt").write_text("".join(f"{sha256(path)}  {path.name}\n" for path in hash_files), encoding="utf-8")

    print(json.dumps({"campaign_id": CAMPAIGN, "primary_verdict": primary_verdict, "hard_gates": f"{sum(row['status'] for row in gates)}/{len(gates)}", "wrong_controls": f"{sum(row['rejected'] for row in wrong_controls)}/{len(wrong_controls)}", "release_manifest_sha256": release_manifest_hash}, indent=2))
    return 0 if hard_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
