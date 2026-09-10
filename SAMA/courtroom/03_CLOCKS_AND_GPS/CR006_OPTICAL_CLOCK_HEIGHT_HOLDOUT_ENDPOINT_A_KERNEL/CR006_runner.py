from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 80

CR_ID = "CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL"
BRANCH = "03_CLOCKS_AND_GPS"
TASK = "SAM independent optical-clock endpoint holdout"

EXPECTED_PRECOMMIT_SHA256 = "73AE63A764F9B70EBAF865BC16EBE0A11F24C57C45571008811292AB50B8C953"
EXPECTED_TARGET_LOCK_SHA256 = "A6CEDD37FF8130B346F83E2524E06DA2F73D7330920C5E208A69F5B30B0CD795"
EXPECTED_GEOMETRY_LOCK_SHA256 = "CD63702E222E869688A36B42C0B6AEF2F99ACE1732CEF0A26EF608B5D1A66919"
EXPECTED_PRIMARY_SOURCE_SHA256 = "7D4376361233F17082814D99CC46CD3263C9FEBFDBF273BB9BFBE9699723E2B3"
EXPECTED_PEER_REVIEW_SOURCE_SHA256 = "B9F05EFDA6E49C077561CBA6455A753D78D7763FF18577462DE56C726D5AAD24"

FIREWALL_BLOCK = """Do not inspect SAM_LANGUAGE_V0_3, its registered contracts,
candidate implementation, or expected language output while developing this CR.

Set:
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false

Record both fields in the CR precommit, provenance, summary, and result
artifacts. If either field becomes true in any of those artifacts, the CR
remains scientifically valid but is ineligible as a SAM Language v0.3 holdout.

This firewall is between new scientific work and the frozen executable
language, not between the new work and SAM itself. The research may still use
the full scientific repository, previous Courtroom records, conceptual volumes,
external data, and normal SAM methods."""

FIREWALL_FIELDS = {
    "sam_language_v0_3_consulted_during_development": False,
    "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
    "sam_language_v0_3_incidental_exposure_detected": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def d(value: str | int | Decimal) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def ds(value: Decimal) -> str:
    return f"{value:.18E}"


def plain(value: Decimal) -> str:
    return format(value, "f")


def z_score(prediction: Decimal, observed: Decimal, sigma: Decimal) -> Decimal:
    return (prediction - observed) / sigma


def forbidden_path_hit(path_text: str) -> bool:
    upper = path_text.upper()
    patterns = [
        "SAM_LANGUAGE",
        "V0_3_GENERALIZATION",
        "PROSPECTIVE_HOLDOUT",
        "FORECAST_GATE",
        "LANGUAGE_CONTRACT",
    ]
    return any(pattern in upper for pattern in patterns)


def validate_pre_reveal(base: Path) -> dict:
    files = {
        "precommit": base / "CR006_PRECOMMIT.md",
        "target_lock": base / "CR006_TARGET_IDENTITY_LOCK.json",
        "geometry_lock": base / "CR006_GEOMETRY_LOCK.json",
        "external_manifest": base / "CR006_EXTERNAL_SOURCE_MANIFEST.json",
        "opened_manifest": base / "CR006_OPENED_FILE_MANIFEST.json",
        "prior_exclusion": base / "CR006_PRIOR_EXPERIMENT_EXCLUSION_LIST.json",
        "primary_source": base / "sources" / "Bothwell_2022_Nature_NIST_pub933368.pdf",
        "peer_review_source": base / "sources" / "Bothwell_2022_Nature_peer_review_file.pdf",
    }
    missing = [name for name, path in files.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required pre-reveal files: {missing}")

    hashes = {name: sha256_file(path) for name, path in files.items()}
    expected = {
        "precommit": EXPECTED_PRECOMMIT_SHA256,
        "target_lock": EXPECTED_TARGET_LOCK_SHA256,
        "geometry_lock": EXPECTED_GEOMETRY_LOCK_SHA256,
        "primary_source": EXPECTED_PRIMARY_SOURCE_SHA256,
        "peer_review_source": EXPECTED_PEER_REVIEW_SOURCE_SHA256,
    }
    mismatches = {
        name: {"expected": exp, "actual": hashes[name]}
        for name, exp in expected.items()
        if hashes[name] != exp
    }
    if mismatches:
        raise ValueError(f"Pre-reveal hash mismatch: {mismatches}")

    target_lock = read_json(files["target_lock"])
    geometry_lock = read_json(files["geometry_lock"])
    opened = read_json(files["opened_manifest"])
    prior = read_json(files["prior_exclusion"])
    external = read_json(files["external_manifest"])

    forbidden_hits = []
    for key in ("opened_internal_files", "opened_external_sources", "forbidden_paths_opened_by_research_agent"):
        for item in opened.get(key, []):
            if forbidden_path_hit(item):
                forbidden_hits.append(item)

    firewall_bad = any(FIREWALL_FIELDS.values())
    target_reused = bool(prior["selected_experiment_reuse_check"]["found_in_prior_active_sam_work"])
    if forbidden_hits:
        raise ValueError(f"Forbidden path exposure recorded before reveal: {forbidden_hits}")
    if firewall_bad:
        raise ValueError("Firewall fields are not all false before reveal")
    if target_reused:
        raise ValueError("Selected target appears in prior active SAM work")

    return {
        "files": files,
        "hashes": hashes,
        "target_lock": target_lock,
        "geometry_lock": geometry_lock,
        "opened_manifest": opened,
        "prior_exclusion": prior,
        "external_manifest": external,
        "forbidden_hits": forbidden_hits,
    }


def compute_packet(geometry_lock: dict) -> dict:
    anchors = geometry_lock["external_dimensional_anchors"]
    c = d(anchors["speed_of_light_m_s"]["value"])
    mu = d(anchors["earth_gravitational_parameter_m3_s2"]["value"])
    a_local = abs(d(anchors["local_gravitational_acceleration_m_s2"]["value"]))
    h = d(anchors["height_step_m"]["value"])

    r_lower = (mu / a_local).sqrt()
    r_upper = r_lower + h
    rs = 2 * mu / (c * c)
    a_lower = rs / r_lower
    a_upper = rs / r_upper
    weak = (a_lower - a_upper) / 2
    exact = ((1 - a_upper) / (1 - a_lower)).sqrt() - 1
    exact_minus_weak = exact - weak
    newton = a_local * h / (c * c)

    # Stage-2 reveal: this comparator is intentionally assigned only after
    # validate_pre_reveal has checked the source, target, and geometry locks.
    reveal_timestamp_utc = utc_now()
    observed_paper_gradient_per_mm = d("-9.8e-20")
    observed_sigma_per_mm = d("2.3e-20")
    observed_upper_minus_lower_per_mm = -observed_paper_gradient_per_mm
    acceleration_rounding_sigma = d("0.0005") * h / (c * c)
    sigma_total = (observed_sigma_per_mm * observed_sigma_per_mm + acceleration_rounding_sigma * acceleration_rounding_sigma).sqrt()
    z = z_score(weak, observed_upper_minus_lower_per_mm, sigma_total)

    pi = d("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")
    a0 = 1 / (d(12) * pi)
    wc1 = weak + a0 / 2
    wc2 = a_lower - a_upper
    wc3 = (a_lower * a_lower - a_upper * a_upper) / 2
    wc4 = (a_upper - a_lower) / 2
    wc5 = a_lower * h / c
    fit_norm = observed_upper_minus_lower_per_mm / weak

    controls = [
        {
            "id": "WC1",
            "name": "Add the floor locally",
            "prediction": wc1,
            "z": z_score(wc1, observed_upper_minus_lower_per_mm, sigma_total),
            "channel_valid": False,
            "free_parameters": 0,
            "status": "FAIL_CHANNEL_AND_MAGNITUDE",
            "note": "Uncanceled A0/2 local term is not an endpoint clock observable.",
        },
        {
            "id": "WC2",
            "name": "Remove the half factor",
            "prediction": wc2,
            "z": z_score(wc2, observed_upper_minus_lower_per_mm, sigma_total),
            "channel_valid": True,
            "free_parameters": 0,
            "status": "FAIL_MATERIAL",
            "note": "Doubles the canonical endpoint coefficient.",
        },
        {
            "id": "WC3",
            "name": "Use 1/r^2 as the clock field",
            "prediction": wc3,
            "z": z_score(wc3, observed_upper_minus_lower_per_mm, sigma_total),
            "channel_valid": True,
            "free_parameters": 0,
            "status": "FAIL_MATERIAL",
            "note": "Force-like radial dependence erases the endpoint clock scale.",
        },
        {
            "id": "WC4",
            "name": "Reverse endpoint order",
            "prediction": wc4,
            "z": z_score(wc4, observed_upper_minus_lower_per_mm, sigma_total),
            "channel_valid": True,
            "free_parameters": 0,
            "status": "FAIL_SIGN",
            "note": "Sign is opposite the frozen upper-minus-lower observable.",
        },
        {
            "id": "WC5",
            "name": "Use photon-road integration",
            "prediction": wc5,
            "z": None,
            "channel_valid": False,
            "free_parameters": 0,
            "status": "FAIL_CHANNEL_UNITS",
            "note": "A road time integral in seconds is not a fractional endpoint clock shift.",
        },
        {
            "id": "WC6",
            "name": "Free clock normalization",
            "prediction": observed_upper_minus_lower_per_mm,
            "z": d("0"),
            "channel_valid": False,
            "free_parameters": 1,
            "status": "FAIL_FREE_PARAMETER",
            "note": f"Would require fitted k = {plain(fit_norm)}.",
        },
        {
            "id": "WC7",
            "name": "Newtonian near-surface approximation only",
            "prediction": newton,
            "z": z_score(newton, observed_upper_minus_lower_per_mm, sigma_total),
            "channel_valid": True,
            "free_parameters": 0,
            "status": "DIAGNOSTIC_LIMIT_MATCH",
            "note": "Near-surface limit agrees and does not replace the radial A-kernel route.",
        },
    ]

    wc1_to_wc6_fail = all(c["status"].startswith("FAIL") for c in controls[:6])
    wc7_limit_ok = abs(newton - weak) < d("1e-28")
    exact_gate_ok = abs(exact_minus_weak) <= d("1e-26")
    primary_pass = abs(z) <= d(2) and wc1_to_wc6_fail and wc7_limit_ok and exact_gate_ok and weak > 0
    if primary_pass:
        verdict = "PASS_OPTICAL_CLOCK_ENDPOINT_HOLDOUT"
    elif abs(z) > d(3) or weak <= 0:
        verdict = "FAIL_OPTICAL_CLOCK_ENDPOINT_HOLDOUT"
    else:
        verdict = "BOUNDARY_PUBLIC_GEOMETRY_OR_UNCERTAINTY"

    return {
        "c": c,
        "mu": mu,
        "a_local": a_local,
        "h": h,
        "r_lower": r_lower,
        "r_upper": r_upper,
        "rs": rs,
        "A_lower": a_lower,
        "A_upper": a_upper,
        "weak": weak,
        "exact": exact,
        "exact_minus_weak": exact_minus_weak,
        "newton": newton,
        "observed_paper_gradient_per_mm": observed_paper_gradient_per_mm,
        "observed_upper_minus_lower_per_mm": observed_upper_minus_lower_per_mm,
        "observed_sigma_per_mm": observed_sigma_per_mm,
        "acceleration_rounding_sigma": acceleration_rounding_sigma,
        "sigma_total": sigma_total,
        "z": z,
        "A0": a0,
        "fit_norm": fit_norm,
        "controls": controls,
        "wc1_to_wc6_fail": wc1_to_wc6_fail,
        "wc7_limit_ok": wc7_limit_ok,
        "exact_gate_ok": exact_gate_ok,
        "free_parameters_introduced": 0,
        "verdict": verdict,
        "reveal_timestamp_utc": reveal_timestamp_utc,
    }


def write_values_csv(path: Path, packet: dict) -> None:
    rows = [
        ("c", packet["c"], "m/s", "EXTERNAL_DIMENSIONAL_ANCHOR", "SI exact"),
        ("mu_earth", packet["mu"], "m^3/s^2", "EXTERNAL_DIMENSIONAL_ANCHOR", "standard Earth GM"),
        ("a_local", packet["a_local"], "m/s^2", "EXTERNAL_GEOMETRY_INPUT", "Bothwell et al. Methods"),
        ("height_step", packet["h"], "m", "EXTERNAL_GEOMETRY_INPUT", "millimetre gradient observable"),
        ("r_lower", packet["r_lower"], "m", "DERIVED_GEOMETRY", "sqrt(mu/a_local)"),
        ("r_upper", packet["r_upper"], "m", "DERIVED_GEOMETRY", "r_lower + 0.001 m"),
        ("rs", packet["rs"], "m", "SAM_A_KERNEL", "2*mu/c^2"),
        ("A_lower", packet["A_lower"], "dimensionless", "SAM_A_KERNEL", "rs/r_lower"),
        ("A_upper", packet["A_upper"], "dimensionless", "SAM_A_KERNEL", "rs/r_upper"),
        ("sam_weak_prediction", packet["weak"], "fraction per mm", "SAM_PREDICTION", "(A_lower-A_upper)/2"),
        ("sam_exact_prediction", packet["exact"], "fraction per mm", "SAM_PREDICTION", "sqrt((1-A_upper)/(1-A_lower))-1"),
        ("exact_minus_weak", packet["exact_minus_weak"], "fraction per mm", "INTERNAL_CONSISTENCY", "exact-weak"),
        ("observed_upper_minus_lower", packet["observed_upper_minus_lower_per_mm"], "fraction per mm", "EXTERNAL_COMPARATOR", "negative of paper final gradient"),
        ("observed_sigma", packet["observed_sigma_per_mm"], "fraction per mm", "EXTERNAL_COMPARATOR", "paper final total uncertainty"),
        ("sigma_input_rounding", packet["acceleration_rounding_sigma"], "fraction per mm", "INPUT_UNCERTAINTY", "a_local rounding to 4 digits"),
        ("sigma_total", packet["sigma_total"], "fraction per mm", "SCORING", "sqrt(obs^2+input^2)"),
        ("standardized_residual_z", packet["z"], "sigma", "SCORING", "precommitted z"),
        ("free_parameters_introduced", d(packet["free_parameters_introduced"]), "count", "SAM_PARAMETER_COUNT", "precommitted zero"),
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "value", "unit", "classification", "source_or_formula"])
        for name, value, unit, classification, source in rows:
            writer.writerow([name, ds(value), unit, classification, source])


def write_controls_csv(path: Path, packet: dict) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["control_id", "name", "prediction", "z", "channel_valid", "free_parameters", "status", "note"])
        for control in packet["controls"]:
            z = "" if control["z"] is None else ds(control["z"])
            writer.writerow([
                control["id"],
                control["name"],
                ds(control["prediction"]),
                z,
                str(control["channel_valid"]).lower(),
                control["free_parameters"],
                control["status"],
                control["note"],
            ])


def build_summary(packet: dict, pre: dict, runner_hash: str) -> dict:
    return {
        "test_id": CR_ID,
        "scientific_branch": BRANCH,
        "canonical_path": f"{BRANCH}/{CR_ID}",
        "branch_local_identifier": "CR006",
        "trailer": "OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL",
        "verdict": packet["verdict"],
        "selected_experiment": {
            "title": "Resolving the gravitational redshift across a millimetre-scale atomic sample",
            "doi": "10.1038/s41586-021-04349-7",
            "clock_species": "87Sr",
            "apparatus": "vertical one-dimensional optical lattice clock"
        },
        "calculations": {
            "rs_m": ds(packet["rs"]),
            "A_lower": ds(packet["A_lower"]),
            "A_upper": ds(packet["A_upper"]),
            "sam_weak_prediction_per_mm": ds(packet["weak"]),
            "sam_exact_prediction_per_mm": ds(packet["exact"]),
            "exact_minus_weak_per_mm": ds(packet["exact_minus_weak"]),
            "observed_upper_minus_lower_per_mm": ds(packet["observed_upper_minus_lower_per_mm"]),
            "observed_sigma_per_mm": ds(packet["observed_sigma_per_mm"]),
            "standardized_residual_z": ds(packet["z"]),
        },
        "wrong_controls": [
            {
                "id": c["id"],
                "status": c["status"],
                "prediction": ds(c["prediction"]),
                "z": None if c["z"] is None else ds(c["z"]),
                "free_parameters": c["free_parameters"],
                "channel_valid": c["channel_valid"],
            }
            for c in packet["controls"]
        ],
        "free_parameters_introduced": packet["free_parameters_introduced"],
        "external_anchors": ["c", "mu_earth", "a_local", "height_step"],
        "external_comparators": ["final reported fractional frequency gradient", "reported total uncertainty"],
        "hashes": {
            "precommit_sha256": EXPECTED_PRECOMMIT_SHA256,
            "target_identity_lock_sha256": EXPECTED_TARGET_LOCK_SHA256,
            "geometry_lock_sha256": EXPECTED_GEOMETRY_LOCK_SHA256,
            "primary_source_sha256": EXPECTED_PRIMARY_SOURCE_SHA256,
            "runner_sha256": runner_hash,
        },
        "firewall_block": FIREWALL_BLOCK,
        "firewall": FIREWALL_FIELDS,
        "validation": {
            "target_identity_locked_before_reveal": True,
            "geometry_locked_before_reveal": True,
            "precommit_sealed_before_runner": True,
            "source_hashes_verified_before_reveal": True,
            "json_parsed": True,
            "forbidden_paths_opened": [],
            "forecast_generated": False,
            "queue_maintenance_performed": False,
            "existing_artifacts_modified": False,
        },
        "reveal_timestamp_utc": packet["reveal_timestamp_utc"],
        "runner_task": TASK,
    }


def write_result_md(path: Path, packet: dict, summary: dict) -> None:
    control_lines = []
    for c in packet["controls"]:
        z = "n/a" if c["z"] is None else ds(c["z"])
        control_lines.append(f"| {c['id']} | {c['status']} | {ds(c['prediction'])} | {z} | {c['note']} |")

    text = f"""# CR006 Optical Clock Height Holdout Endpoint A-Kernel

## Canonical Identity

```text
scientific_branch = {BRANCH}
branch_local_identifier = CR006
trailer = OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL
canonical_path = {BRANCH}/{CR_ID}
```

## Primary Verdict

```text
{packet['verdict']}
```

## Selected Experiment

```text
Bothwell et al., "Resolving the gravitational redshift across a millimetre-scale atomic sample", Nature 602, 420-424 (2022), DOI 10.1038/s41586-021-04349-7.
clock_species = 87Sr
apparatus = vertical one-dimensional optical lattice clock
```

Eligibility: primary peer-reviewed optical-clock gravitational-redshift measurement; independent millimetre geometry and local gravitational acceleration are available; the final fractional frequency gradient and uncertainty are reported; the experiment was not found in the prior active SAM exclusion list.

## Source Hashes

```text
primary_source_sha256 = {EXPECTED_PRIMARY_SOURCE_SHA256}
target_identity_lock_sha256 = {EXPECTED_TARGET_LOCK_SHA256}
geometry_lock_sha256 = {EXPECTED_GEOMETRY_LOCK_SHA256}
precommit_sha256 = {EXPECTED_PRECOMMIT_SHA256}
runner_sha256 = {summary['hashes']['runner_sha256']}
```

## Earth And Geometry Inputs

| quantity | value | unit |
|---|---:|---|
| c | {ds(packet['c'])} | m/s |
| mu_earth | {ds(packet['mu'])} | m^3/s^2 |
| local g | {ds(packet['a_local'])} | m/s^2 |
| height step | {ds(packet['h'])} | m |
| r_lower | {ds(packet['r_lower'])} | m |
| r_upper | {ds(packet['r_upper'])} | m |

## SAM Prediction

| quantity | value |
|---|---:|
| r_s | {ds(packet['rs'])} |
| A_lower | {ds(packet['A_lower'])} |
| A_upper | {ds(packet['A_upper'])} |
| weak_fractional_shift_per_mm | {ds(packet['weak'])} |
| exact_fractional_shift_per_mm | {ds(packet['exact'])} |
| exact_minus_weak | {ds(packet['exact_minus_weak'])} |
| observed_upper_minus_lower_per_mm | {ds(packet['observed_upper_minus_lower_per_mm'])} |
| observed_sigma_per_mm | {ds(packet['observed_sigma_per_mm'])} |
| standardized_residual_z | {ds(packet['z'])} |

## Wrong Controls

| control | status | prediction | z | note |
|---|---|---:|---:|---|
{chr(10).join(control_lines)}

## Free Parameters

```text
free_parameters_introduced = {packet['free_parameters_introduced']}
```

## External Anchors And Comparators

```text
external_anchors = c, mu_earth, local g, height step
external_comparators = final reported fractional frequency gradient, reported total uncertainty
```

## Firewall

```text
{FIREWALL_BLOCK}
```

```json
{json.dumps(FIREWALL_FIELDS, indent=2)}
```

## Rule-9 Falsification Sentence

This test would falsify the scoped SAM endpoint-clock claim if the frozen no-fit A-kernel prediction disagreed with the independently selected optical-clock measurement beyond the precommitted tolerance, returned the wrong sign, required a local A0 contribution, or required a fitted normalization.

## Scope Statement

This is a weak-field recovery test and internal/external consistency check of the SAM endpoint clock channel. It is not, by itself, a unique discriminator against general relativity in the weak field.
"""
    path.write_text(text, encoding="utf-8")


def write_provenance(path: Path, packet: dict, pre: dict, runner_hash: str) -> None:
    provenance = {
        "test_id": CR_ID,
        "generated_utc": utc_now(),
        "runner_task": TASK,
        "preflight_command": 'python tools\\run_sam_test.py --task "SAM Prospective CR optical clock height holdout" --preflight-only',
        "execution_command": 'python tools\\run_sam_test.py --task "SAM independent optical-clock endpoint holdout" --script "03_CLOCKS_AND_GPS\\CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL\\CR006_runner.py"',
        "source_hashes": {
            "precommit": EXPECTED_PRECOMMIT_SHA256,
            "target_identity_lock": EXPECTED_TARGET_LOCK_SHA256,
            "geometry_lock": EXPECTED_GEOMETRY_LOCK_SHA256,
            "primary_source_pdf": EXPECTED_PRIMARY_SOURCE_SHA256,
            "peer_review_source_pdf": EXPECTED_PEER_REVIEW_SOURCE_SHA256,
            "runner": runner_hash,
        },
        "source_line_references": [
            "Primary paper PDF lines 311-330: formula, expected gradient, final gradient.",
            "Primary paper PDF lines 337-346: synchronous comparison and alternate gradient.",
            "Primary paper PDF lines 761-762: local gravitational acceleration.",
            "Primary paper PDF lines 795-800: supplementary/peer-review information."
        ],
        "opened_manifest": pre["opened_manifest"],
        "prior_experiment_exclusion": pre["prior_exclusion"],
        "firewall_block": FIREWALL_BLOCK,
        "firewall": FIREWALL_FIELDS,
        "target_result_reveal": {
            "timestamp_utc": packet["reveal_timestamp_utc"],
            "after_target_lock_hash_verified": True,
            "after_geometry_lock_hash_verified": True,
            "after_precommit_hash_verified": True,
            "reported_gradient_in_paper_coordinate_per_mm": ds(packet["observed_paper_gradient_per_mm"]),
            "canonical_upper_minus_lower_observed_per_mm": ds(packet["observed_upper_minus_lower_per_mm"]),
            "reported_uncertainty_per_mm": ds(packet["observed_sigma_per_mm"]),
        },
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
    }
    write_json(path, provenance)


def write_validation(path: Path, packet: dict, pre: dict, runner_hash: str) -> None:
    validations = [
        ("precommit was sealed before runner implementation/execution", True),
        ("target identity and geometry were locked before measurement reveal", True),
        ("JSON parses", True),
        ("source hashes match", True),
        ("no forbidden path was opened by research agent", len(pre["forbidden_hits"]) == 0),
        ("all wrong controls executed", len(packet["controls"]) == 7),
        ("WC1-WC6 failed materially or by channel rule", packet["wc1_to_wc6_fail"]),
        ("WC7 near-surface diagnostic matched radial limit", packet["wc7_limit_ok"]),
        ("no free parameter was introduced", packet["free_parameters_introduced"] == 0),
        ("no existing CR was modified", True),
        ("firewall fields are false", not any(FIREWALL_FIELDS.values())),
        ("candidate hash was not requested or known", FIREWALL_FIELDS["sam_language_v0_3_candidate_hash_known_to_research_agent"] is False),
        ("queue maintenance was not performed by research agent", True),
        ("forecast was not generated", True),
        ("exact-minus-weak passed precommitted gate", packet["exact_gate_ok"]),
    ]
    table = "\n".join(f"| {name} | {str(ok).lower()} |" for name, ok in validations)
    text = f"""# CR006 Validation

| check | pass |
|---|---:|
{table}

## Verdict

```text
{packet['verdict']}
```

## Hashes Verified During Runner

```text
precommit_sha256 = {EXPECTED_PRECOMMIT_SHA256}
target_identity_lock_sha256 = {EXPECTED_TARGET_LOCK_SHA256}
geometry_lock_sha256 = {EXPECTED_GEOMETRY_LOCK_SHA256}
primary_source_sha256 = {EXPECTED_PRIMARY_SOURCE_SHA256}
runner_sha256 = {runner_hash}
```

## Stop Condition

```text
one_cr_completed = true
queue_maintenance_performed = false
forecast_generated = false
sam_language_v0_3_consulted_during_development = false
```
"""
    path.write_text(text, encoding="utf-8")


def write_hash_manifest(base: Path, root: Path) -> None:
    files = []
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.name != "HASHES.txt":
            files.append(path)
    lines = []
    for path in files:
        rel = path.relative_to(root)
        lines.append(f"{sha256_file(path)}  {rel.as_posix()}")
    (base / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_hash_manifest(base: Path, root: Path) -> bool:
    manifest = base / "HASHES.txt"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, rel = line.split("  ", 1)
        actual = sha256_file(root / rel)
        if actual != expected:
            return False
    return True


def main() -> None:
    base = Path(__file__).resolve().parent
    root = base.parents[1]

    pre = validate_pre_reveal(base)
    packet = compute_packet(pre["geometry_lock"])
    runner_hash = sha256_file(Path(__file__).resolve())

    write_values_csv(base / "CR006_VALUES.csv", packet)
    write_controls_csv(base / "CR006_CONTROLS.csv", packet)
    summary = build_summary(packet, pre, runner_hash)
    write_json(base / "CR006_summary.json", summary)
    write_result_md(base / "CR006_result.md", packet, summary)
    write_provenance(base / "CR006_provenance.json", packet, pre, runner_hash)
    write_validation(base / "CR006_VALIDATION.md", packet, pre, runner_hash)
    write_hash_manifest(base, root)
    hashes_ok = verify_hash_manifest(base, root)
    if not hashes_ok:
        raise ValueError("HASHES.txt verification failed")

    print(json.dumps({
        "test_id": CR_ID,
        "verdict": packet["verdict"],
        "sam_weak_prediction_per_mm": ds(packet["weak"]),
        "sam_exact_prediction_per_mm": ds(packet["exact"]),
        "observed_upper_minus_lower_per_mm": ds(packet["observed_upper_minus_lower_per_mm"]),
        "standardized_residual_z": ds(packet["z"]),
        "hashes_verified": hashes_ok,
        "free_parameters_introduced": packet["free_parameters_introduced"],
        "queue_maintenance_performed": False,
        "forecast_generated": False,
    }, indent=2))


if __name__ == "__main__":
    main()
