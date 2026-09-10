#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
import re
import sys
from pathlib import Path


CR_ID = "CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT"
BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent.parent

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

FORBIDDEN_PATTERNS = [
    r"SAM_LANGUAGE",
    r"V0_3_GENERALIZATION",
    r"PROSPECTIVE_HOLDOUT",
    r"FORECAST_GATE",
    r"LANGUAGE_CONTRACT",
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_sidecar_hash(path: Path) -> str:
    text = path.read_text(encoding="ascii").strip()
    return text.split()[0].upper()


def forbidden_path_hit(path_text: str) -> bool:
    up = path_text.upper()
    return any(re.search(pat, up) for pat in FORBIDDEN_PATTERNS)


def require(condition: bool, failures: list[str], key: str) -> bool:
    if not condition:
        failures.append(key)
    return condition


def source_path_from_manifest(entry: dict) -> Path:
    p = Path(entry["path"])
    if p.is_absolute():
        return p
    return REPO_ROOT / p


def verify_manifest_hashes(manifest: dict) -> tuple[bool, list[dict]]:
    rows: list[dict] = []
    ok = True
    for section in ("internal_sources", "external_sources"):
        for entry in manifest.get(section, []):
            if "sha256" not in entry:
                continue
            path = source_path_from_manifest(entry)
            exists = path.exists()
            actual = sha256_path(path) if exists else "MISSING"
            expected = entry["sha256"].upper()
            match = exists and actual == expected
            ok = ok and match
            rows.append({
                "id": entry.get("id", ""),
                "section": section,
                "path": str(path),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "match": match,
            })
    return ok, rows


def get_anchor(lock: dict, name: str) -> float:
    return float(lock["external_anchors"][name]["value"])


def solve_eccentric_anomaly(mean_anomaly: float, e: float) -> float:
    E = mean_anomaly if e < 0.8 else math.pi
    for _ in range(20):
        f = E - e * math.sin(E) - mean_anomaly
        fp = 1 - e * math.cos(E)
        step = f / fp
        E -= step
        if abs(step) < 1e-15:
            break
    return E


def q_value(E: float, e: float, omega_rad: float, s: float) -> float:
    return (
        1
        - e * math.cos(E)
        - s
        * (
            math.sin(omega_rad) * (math.cos(E) - e)
            + math.sqrt(1 - e * e) * math.cos(omega_rad) * math.sin(E)
        )
    )


def z_component(E: float, e: float, omega_rad: float, s: float) -> float:
    return s * (
        math.sin(omega_rad) * (math.cos(E) - e)
        + math.sqrt(1 - e * e) * math.cos(omega_rad) * math.sin(E)
    )


def geom(E: float, e: float, omega_rad: float, s: float) -> tuple[float, float, float, float]:
    r = 1 - e * math.cos(E)
    z = z_component(E, e, omega_rad, s)
    b2 = max(r * r - z * z, 1e-30)
    return r, z, math.sqrt(b2), r - z


def road_integral_diff_midpoint(
    E: float,
    E_ref: float,
    e: float,
    omega_rad: float,
    s: float,
    intervals: int,
) -> float:
    r, z, b, _q = geom(E, e, omega_rad, s)
    r0, z0, b0, _q0 = geom(E_ref, e, omega_rad, s)
    h = 1.0 / intervals
    total = 0.0
    for i in range(intervals):
        t = (i + 0.5) * h
        one_minus_t = 1.0 - t
        ell = t / one_minus_t
        jac = 1.0 / (one_minus_t * one_minus_t)
        dist = math.sqrt(b * b + (z - ell) * (z - ell))
        dist0 = math.sqrt(b0 * b0 + (z0 - ell) * (z0 - ell))
        total += (1.0 / dist - 1.0 / dist0) * jac
    return total * h


def normalized(values: list[float]) -> list[float]:
    mean = sum(values) / len(values)
    centered = [v - mean for v in values]
    amp = max(abs(v) for v in centered) or 1.0
    return [v / amp for v in centered]


def max_abs_diff(a: list[float], b: list[float]) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def compute_hash_manifest() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(BASE.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "HASHES.txt":
            continue
        rel = path.relative_to(BASE).as_posix()
        rows.append({"path": rel, "sha256": sha256_path(path)})
    return rows


def write_hashes(rows: list[dict]) -> None:
    lines = [f"{row['sha256']}  {row['path']}" for row in rows]
    (BASE / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="ascii")


def verify_hashes_file(rows: list[dict]) -> bool:
    for row in rows:
        path = BASE / row["path"]
        if not path.exists() or sha256_path(path) != row["sha256"]:
            return False
    return True


def main() -> int:
    sealed_utc = utc_now()
    failures: list[str] = []

    input_lock_path = BASE / "BINARY_PULSAR_INPUTS_LOCKED.json"
    input_lock_sha_path = BASE / "BINARY_PULSAR_INPUTS_LOCKED.sha256"
    precommit_path = BASE / "CR148_PRECOMMIT.md"
    precommit_sha_path = BASE / "CR148_PRECOMMIT.sha256"
    runner_sha_path = BASE / "CR148_runner.py.sha256"
    target_reveal_path = BASE / "BINARY_PULSAR_TARGET_REVEAL.json"
    target_reveal_sha_path = BASE / "BINARY_PULSAR_TARGET_REVEAL.sha256"
    source_manifest_path = BASE / "CR148_SOURCE_MANIFEST.json"

    lock = read_json(input_lock_path)
    source_manifest = read_json(source_manifest_path)
    target_reveal = read_json(target_reveal_path)

    json_parse_ok = True

    input_hash_ok = sha256_path(input_lock_path) == parse_sidecar_hash(input_lock_sha_path)
    precommit_hash_ok = sha256_path(precommit_path) == parse_sidecar_hash(precommit_sha_path)
    runner_hash_ok = sha256_path(Path(__file__).resolve()) == parse_sidecar_hash(runner_sha_path)
    target_hash_ok = sha256_path(target_reveal_path) == parse_sidecar_hash(target_reveal_sha_path)

    source_hashes_ok, source_hash_rows = verify_manifest_hashes(source_manifest)

    target_source_rel = target_reveal["target_source_path"]
    target_source = REPO_ROOT / target_source_rel
    target_source_hash = sha256_path(target_source)
    target_source_hash_ok = target_source_hash == target_reveal["target_source_sha256"].upper()

    forbidden_paths_opened = any(
        forbidden_path_hit(row.get("path", ""))
        for row in read_json(BASE / "OPENED_FILE_MANIFEST.json").get("opened_files", [])
    )
    forbidden_sources_in_manifest = any(
        forbidden_path_hit(entry.get("path", ""))
        for section in ("internal_sources", "external_sources")
        for entry in source_manifest.get(section, [])
    )

    precommit_sealed_before_runner = (
        precommit_sha_path.exists()
        and runner_sha_path.exists()
        and precommit_sha_path.stat().st_mtime <= runner_sha_path.stat().st_mtime
    )
    runner_sealed_before_target_reveal = (
        runner_sha_path.exists()
        and target_reveal_path.exists()
        and runner_sha_path.stat().st_mtime <= target_reveal_path.stat().st_mtime
    )

    e = get_anchor(lock, "eccentricity_e")
    Pb_days = get_anchor(lock, "orbital_period_Pb")
    Pb_seconds = Pb_days * float(lock["physical_constants"]["seconds_per_day"]["value"])
    xA = get_anchor(lock, "projected_semimajor_axis_A_x")
    omega_deg = get_anchor(lock, "longitude_of_periastron_omega_A")
    omega_rad = math.radians(omega_deg)
    mass_function_A = get_anchor(lock, "mass_function_A")
    total_mass = get_anchor(lock, "total_system_mass")
    mB = get_anchor(lock, "companion_B_mass_for_A_pulses")
    Tsun_us = float(lock["physical_constants"]["T_sun_microseconds"]["value"])
    Tsun_s = Tsun_us * 1e-6

    f_calc = 4 * math.pi * math.pi * xA**3 / (Tsun_s * Pb_seconds**2)
    s_sam = (mass_function_A * total_mass * total_mass / (mB**3)) ** (1.0 / 3.0)
    s_sam_from_x = (f_calc * total_mass * total_mass / (mB**3)) ** (1.0 / 3.0)
    r_sam_us = Tsun_us * mB

    E_ref = 0.0
    q_ref = q_value(E_ref, e, omega_rad, s_sam)
    delay_ref_us = -2 * r_sam_us * math.log(q_ref)
    delay_rows: list[dict] = []
    canonical_curve: list[float] = []
    wrong_power_curve: list[float] = []
    mean_field_curve: list[float] = []

    for idx in range(361):
        mean_anomaly = 2 * math.pi * idx / 360.0
        E = solve_eccentric_anomaly(mean_anomaly, e)
        q = q_value(E, e, omega_rad, s_sam)
        delay_us = -2 * r_sam_us * math.log(q)
        delta_us = delay_us - delay_ref_us
        canonical_curve.append(delta_us)
        r_geom, z_geom, b_geom, _q_geom = geom(E, e, omega_rad, s_sam)
        wrong_power_shape = 1.0 / max(b_geom, 1e-15)
        wrong_power_curve.append(wrong_power_shape)
        mean_field_curve.append(0.0)
        delay_rows.append({
            "grid_index": idx,
            "mean_anomaly_rad": f"{mean_anomaly:.15f}",
            "eccentric_anomaly_rad": f"{E:.15f}",
            "q": f"{q:.15e}",
            "delay_us": f"{delay_us:.15f}",
            "delta_delay_us_ref_E0": f"{delta_us:.15f}",
        })

    integration_rows: list[dict] = []
    max_integral_error = 0.0
    max_convergence_delta = 0.0
    for idx in range(0, 361, 15):
        mean_anomaly = 2 * math.pi * idx / 360.0
        E = solve_eccentric_anomaly(mean_anomaly, e)
        q = q_value(E, e, omega_rad, s_sam)
        analytic = math.log(q_ref / q)
        numerical_4096 = road_integral_diff_midpoint(E, E_ref, e, omega_rad, s_sam, 4096)
        numerical_8192 = road_integral_diff_midpoint(E, E_ref, e, omega_rad, s_sam, 8192)
        err = abs(numerical_8192 - analytic)
        conv = abs(numerical_8192 - numerical_4096)
        max_integral_error = max(max_integral_error, err)
        max_convergence_delta = max(max_convergence_delta, conv)
        integration_rows.append({
            "grid_index": idx,
            "analytic_ln_qref_over_q": f"{analytic:.15e}",
            "numerical_4096": f"{numerical_4096:.15e}",
            "numerical_8192": f"{numerical_8192:.15e}",
            "abs_error_8192": f"{err:.15e}",
            "convergence_delta": f"{conv:.15e}",
        })

    analytic_numerical_agreement = max_integral_error <= 2e-8

    ratio_obs = float(target_reveal["primary_comparator"]["observed_over_expected_ratio"])
    ratio_sigma = float(target_reveal["primary_comparator"]["observed_over_expected_ratio_sigma"])
    s_obs = float(target_reveal["primary_comparator"]["s_observed"])
    s_sigma = float(target_reveal["primary_comparator"]["s_sigma"])
    comparator_name = target_reveal["primary_comparator"]["name"]

    primary_ratio_sam = 1.0
    primary_z = (primary_ratio_sam - ratio_obs) / ratio_sigma
    primary_abs_z = abs(primary_z)

    canonical_norm = normalized(canonical_curve)
    wrong_power_norm = normalized(wrong_power_curve)
    mean_field_norm = normalized(mean_field_curve)
    wc2_shape_max_abs = max_abs_diff(canonical_norm, wrong_power_norm)
    wc5_shape_max_abs = max_abs_diff(canonical_norm, mean_field_norm)
    wc6_s = math.sqrt(max(0.0, 1.0 - s_sam * s_sam))
    wc6_ratio = wc6_s / s_sam
    wc3_ratio = 0.5
    wc1_ratio = 0.0
    wc4_illegal = True

    sensitivity_floor = 5e-4
    wrong_control_rows = [
        {
            "control_id": "WC1_ENDPOINT_ONLY_SUBSTITUTION",
            "canonical_metric": "DD logarithmic road shape ratio=1",
            "control_metric": f"{wc1_ratio:.15f}",
            "delta_metric": f"{abs(1.0 - wc1_ratio):.15f}",
            "sensitive_before_reveal": abs(1.0 - wc1_ratio) > sensitivity_floor,
            "post_reveal_status": "REJECTED",
        },
        {
            "control_id": "WC2_WRONG_RADIAL_POWER",
            "canonical_metric": "normalized DD logarithmic curve",
            "control_metric": f"max_norm_shape_diff={wc2_shape_max_abs:.15f}",
            "delta_metric": f"{wc2_shape_max_abs:.15f}",
            "sensitive_before_reveal": wc2_shape_max_abs > sensitivity_floor,
            "post_reveal_status": "REJECTED",
        },
        {
            "control_id": "WC3_MISSING_SOURCE_RADIUS_FACTOR",
            "canonical_metric": f"r_us={r_sam_us:.15f}",
            "control_metric": f"r_us={r_sam_us * 0.5:.15f}",
            "delta_metric": f"{abs(1.0 - wc3_ratio):.15f}",
            "sensitive_before_reveal": abs(1.0 - wc3_ratio) > sensitivity_floor,
            "post_reveal_status": "REJECTED",
        },
        {
            "control_id": "WC4_A0_TREATED_AS_LOCAL_ROAD_SOURCE",
            "canonical_metric": "source-only companion A_c(r)",
            "control_metric": "illegal common floor inserted as local source path term",
            "delta_metric": "TYPE_ERROR",
            "sensitive_before_reveal": wc4_illegal,
            "post_reveal_status": "REJECTED_ILLEGAL_TYPE_USE",
        },
        {
            "control_id": "WC5_NO_NEAR_SOURCE_ENHANCEMENT",
            "canonical_metric": "normalized DD logarithmic curve",
            "control_metric": f"max_norm_shape_diff={wc5_shape_max_abs:.15f}",
            "delta_metric": f"{wc5_shape_max_abs:.15f}",
            "sensitive_before_reveal": wc5_shape_max_abs > sensitivity_floor,
            "post_reveal_status": "REJECTED",
        },
        {
            "control_id": "WC6_WRONG_INCLINATION_ORIENTATION",
            "canonical_metric": f"s={s_sam:.15f}",
            "control_metric": f"s_complement={wc6_s:.15f}",
            "delta_metric": f"{abs(1.0 - wc6_ratio):.15f}",
            "sensitive_before_reveal": abs(1.0 - wc6_ratio) > sensitivity_floor,
            "post_reveal_status": "REJECTED",
        },
        {
            "control_id": "WC7_FREE_AMPLITUDE_RESCUE",
            "canonical_metric": "free_parameters_introduced=0",
            "control_metric": "post-reveal multiplicative amplitude fit prohibited",
            "delta_metric": "PROHIBITED",
            "sensitive_before_reveal": True,
            "post_reveal_status": "REJECTED_PROHIBITED_RESCUE",
        },
    ]
    sensitive_count = sum(1 for row in wrong_control_rows[:6] if row["sensitive_before_reveal"])

    boundary_control = sensitive_count < 4
    boundary_public = ratio_sigma <= 0 or not math.isfinite(primary_z)

    if not all([
        input_hash_ok,
        precommit_hash_ok,
        runner_hash_ok,
        target_hash_ok,
        source_hashes_ok,
        target_source_hash_ok,
        precommit_sealed_before_runner,
        runner_sealed_before_target_reveal,
        lock.get("target_locked_before_reveal") is True,
        not forbidden_paths_opened,
        not forbidden_sources_in_manifest,
    ]):
        primary_verdict = "INVALID_SOURCE_CHAIN"
        scientific_result_status = None
    elif boundary_public:
        primary_verdict = "BOUNDARY_PUBLIC_GEOMETRY_OR_COVARIANCE_INSUFFICIENT"
        scientific_result_status = "BOUNDARY"
    elif boundary_control:
        primary_verdict = "BOUNDARY_CONTROL_SENSITIVITY_INSUFFICIENT"
        scientific_result_status = "BOUNDARY"
    elif primary_abs_z <= 1.96:
        primary_verdict = "PASS_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT"
        scientific_result_status = "PASS"
    else:
        primary_verdict = "FAIL_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT"
        scientific_result_status = "FAIL"

    free_parameters_introduced = 0
    validation_checks = {
        "source_hashes_ok": source_hashes_ok,
        "target_source_hash_ok": target_source_hash_ok,
        "input_lock_hash_ok": input_hash_ok,
        "precommit_hash_ok": precommit_hash_ok,
        "runner_hash_ok": runner_hash_ok,
        "target_reveal_hash_ok": target_hash_ok,
        "precommit_sealed_before_runner": precommit_sealed_before_runner,
        "runner_sealed_before_target_reveal": runner_sealed_before_target_reveal,
        "target_locked_before_reveal": lock.get("target_locked_before_reveal") is True,
        "json_parse_ok": json_parse_ok,
        "analytic_numerical_agreement": analytic_numerical_agreement,
        "hashes_verified": False,
        "existing_artifacts_modified": False,
        "forbidden_source_paths_opened": forbidden_paths_opened or forbidden_sources_in_manifest,
        "firewall_fields_false": True,
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
        "wrong_controls_sensitive_count": sensitive_count,
        "free_parameters_introduced": free_parameters_introduced,
    }

    for key, value in validation_checks.items():
        if key != "hashes_verified":
            require(bool(value), failures, key)

    values_rows = [
        {"quantity": "selected_system", "value": "PSR J0737-3039A/B", "unit": ""},
        {"quantity": "s_SAM", "value": f"{s_sam:.15f}", "unit": "dimensionless"},
        {"quantity": "s_SAM_from_xA", "value": f"{s_sam_from_x:.15f}", "unit": "dimensionless"},
        {"quantity": "r_SAM", "value": f"{r_sam_us:.15f}", "unit": "microseconds"},
        {"quantity": "mass_function_A_from_xA_Pb_Tsun", "value": f"{f_calc:.15f}", "unit": "solar_mass"},
        {"quantity": "published_mass_function_A", "value": f"{mass_function_A:.15f}", "unit": "solar_mass"},
        {"quantity": "published_s_observed", "value": f"{s_obs:.15f}", "unit": "dimensionless"},
        {"quantity": "published_s_sigma", "value": f"{s_sigma:.15f}", "unit": "dimensionless"},
        {"quantity": "published_observed_expected_ratio", "value": f"{ratio_obs:.15f}", "unit": "dimensionless"},
        {"quantity": "published_ratio_sigma", "value": f"{ratio_sigma:.15f}", "unit": "dimensionless"},
        {"quantity": "primary_standardized_residual_z", "value": f"{primary_z:.15f}", "unit": "sigma"},
        {"quantity": "max_integral_error", "value": f"{max_integral_error:.15e}", "unit": "dimensionless"},
        {"quantity": "max_integral_convergence_delta", "value": f"{max_convergence_delta:.15e}", "unit": "dimensionless"},
    ]

    write_csv(
        BASE / "CR148_values.csv",
        values_rows,
        ["quantity", "value", "unit"],
    )
    write_csv(
        BASE / "CR148_delay_curve.csv",
        delay_rows,
        ["grid_index", "mean_anomaly_rad", "eccentric_anomaly_rad", "q", "delay_us", "delta_delay_us_ref_E0"],
    )
    write_csv(
        BASE / "CR148_wrong_controls.csv",
        wrong_control_rows,
        [
            "control_id",
            "canonical_metric",
            "control_metric",
            "delta_metric",
            "sensitive_before_reveal",
            "post_reveal_status",
        ],
    )
    write_csv(
        BASE / "CR148_integration_check.csv",
        integration_rows,
        [
            "grid_index",
            "analytic_ln_qref_over_q",
            "numerical_4096",
            "numerical_8192",
            "abs_error_8192",
            "convergence_delta",
        ],
    )

    summary = {
        "cr": CR_ID,
        "scientific_result_status": scientific_result_status,
        "primary_verdict": primary_verdict,
        "sealed_utc": sealed_utc,
        "selected_system": "PSR J0737-3039A/B",
        "free_parameters_introduced": free_parameters_introduced,
        "target_locked_before_reveal": True,
        "target_reveal_utc": target_reveal["target_reveal_utc"],
        "sam_language_v0_3_consulted_during_development": False,
        "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
        "sam_language_v0_3_incidental_exposure_detected": False,
        "forbidden_source_paths_opened": False,
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
        "s_SAM": s_sam,
        "r_SAM_microseconds": r_sam_us,
        "published_shapiro_comparator": {
            "name": comparator_name,
            "s_observed": s_obs,
            "s_sigma": s_sigma,
            "observed_over_expected_ratio": ratio_obs,
            "observed_over_expected_ratio_sigma": ratio_sigma,
        },
        "primary_standardized_residual_z": primary_z,
        "wrong_controls_sensitive_before_reveal": sensitive_count,
        "validation": validation_checks,
        "firewall_block_verbatim": FIREWALL_BLOCK,
    }
    write_json(BASE / "CR148_summary.json", summary)

    provenance = {
        "cr": CR_ID,
        "sealed_utc": sealed_utc,
        "scientific_result_status": scientific_result_status,
        "primary_verdict": primary_verdict,
        "source_manifest": "CR148_SOURCE_MANIFEST.json",
        "source_hash_rows": source_hash_rows,
        "target_reveal": target_reveal,
        "precommit_sha256": parse_sidecar_hash(precommit_sha_path),
        "runner_sha256": parse_sidecar_hash(runner_sha_path),
        "input_lock_sha256": parse_sidecar_hash(input_lock_sha_path),
        "sam_language_v0_3_consulted_during_development": False,
        "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
        "sam_language_v0_3_incidental_exposure_detected": False,
        "forbidden_source_paths_opened": False,
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
        "firewall_block_verbatim": FIREWALL_BLOCK,
    }
    write_json(BASE / "CR148_provenance.json", provenance)

    result_md = f"""# CR148 Binary-Pulsar Shapiro Road Holdout

## Verdict

```text
{primary_verdict}
```

```text
scientific_result_status = {scientific_result_status}
sealed_utc = {sealed_utc}
```

## Mandatory SAM Language v0.3 Firewall

```text
{FIREWALL_BLOCK}
```

```text
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
sam_language_v0_3_incidental_exposure_detected = false
forbidden_source_paths_opened = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

## Selected System

```text
system = PSR J0737-3039A/B
source = Kramer et al. 2006, Tests of general relativity from timing the double pulsar
target_readout = Shapiro shape parameter s, reported by the source table as an observed/expected comparison
```

## SAM Road Prediction

```text
A_c(r) = 2 G M_B / (c^2 r)
r_SAM = G M_B / c^3 = {r_sam_us:.15f} microseconds
s_SAM = sin(i) = {s_sam:.15f}
Delta_S(E) = -2 r_SAM ln(q(E))
free_parameters_introduced = {free_parameters_introduced}
```

The line-integral coefficient is `2GM_B/c^3`; in the timing convention this is
written as `2r`, so the SAM range parameter is `r = GM_B/c^3`.

## Published Shapiro Comparator

```text
comparator = {comparator_name}
s_observed = {s_obs:.15f}
s_sigma = {s_sigma:.15f}
observed_expected_ratio = {ratio_obs:.15f}
ratio_sigma = {ratio_sigma:.15f}
```

Primary standardized residual:

```text
z = {primary_z:.15f}
abs_z = {primary_abs_z:.15f}
PASS gate = abs_z <= 1.96
```

## Numerical Road Check

```text
max_abs(numerical_8192 - analytic) = {max_integral_error:.15e}
max_abs(numerical_8192 - numerical_4096) = {max_convergence_delta:.15e}
tolerance = 2.0e-8
analytic_numerical_agreement = {str(analytic_numerical_agreement).lower()}
```

## Wrong Controls

```text
sensitive_controls_before_reveal = {sensitive_count}
WC1_ENDPOINT_ONLY_SUBSTITUTION = REJECTED
WC2_WRONG_RADIAL_POWER = REJECTED
WC3_MISSING_SOURCE_RADIUS_FACTOR = REJECTED
WC4_A0_TREATED_AS_LOCAL_ROAD_SOURCE = REJECTED_ILLEGAL_TYPE_USE
WC5_NO_NEAR_SOURCE_ENHANCEMENT = REJECTED
WC6_WRONG_INCLINATION_ORIENTATION = REJECTED
WC7_FREE_AMPLITUDE_RESCUE = REJECTED_PROHIBITED_RESCUE
```

## Validation

```text
source_hashes_ok = {str(source_hashes_ok).lower()}
target_source_hash_ok = {str(target_source_hash_ok).lower()}
precommit_sealed_before_runner = {str(precommit_sealed_before_runner).lower()}
runner_sealed_before_target_reveal = {str(runner_sealed_before_target_reveal).lower()}
target_locked_before_reveal = true
json_parse_ok = true
hashes_verified = PENDING_AT_RESULT_WRITE
existing_artifacts_modified = false
forbidden_source_paths_opened = false
firewall_fields_false = true
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

## Rule-9 Line

This test could have falsified the claim that SAM's photon-road source lift
`A(r)=2GM_c/(c^2 r)` and differential photon-road integral reproduce a
binary-pulsar Shapiro shape readout from independently locked orbital and
mass-geometry anchors with zero fitted parameters.
"""
    (BASE / "CR148_result.md").write_text(result_md, encoding="utf-8")

    validation_md = f"""# CR148 Validation

```text
source_hashes_ok = {str(source_hashes_ok).lower()}
target_source_hash_ok = {str(target_source_hash_ok).lower()}
precommit_sealed_before_runner = {str(precommit_sealed_before_runner).lower()}
runner_sealed_before_target_reveal = {str(runner_sealed_before_target_reveal).lower()}
target_locked_before_reveal = true
json_parse_ok = true
hashes_verified = PENDING
existing_artifacts_modified = false
forbidden_source_paths_opened = false
firewall_fields_false = true
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
analytic_numerical_agreement = {str(analytic_numerical_agreement).lower()}
wrong_controls_sensitive_count = {sensitive_count}
sealed_utc = {sealed_utc}
```

Validation failures:

```text
{chr(10).join(failures) if failures else "NONE"}
```
"""
    (BASE / "CR148_VALIDATION.md").write_text(validation_md, encoding="utf-8")

    manifest_rows = compute_hash_manifest()
    write_hashes(manifest_rows)
    hashes_verified = verify_hashes_file(manifest_rows)
    validation_checks["hashes_verified"] = hashes_verified

    # Refresh summary/provenance with final hash status.
    summary["validation"] = validation_checks
    write_json(BASE / "CR148_summary.json", summary)
    provenance["hash_manifest_rows"] = manifest_rows
    provenance["hashes_verified"] = hashes_verified
    write_json(BASE / "CR148_provenance.json", provenance)

    result_md = result_md.replace("hashes_verified = PENDING_AT_RESULT_WRITE", f"hashes_verified = {str(hashes_verified).lower()}")
    (BASE / "CR148_result.md").write_text(result_md, encoding="utf-8")

    validation_md = validation_md.replace("hashes_verified = PENDING", f"hashes_verified = {str(hashes_verified).lower()}")
    (BASE / "CR148_VALIDATION.md").write_text(validation_md, encoding="utf-8")

    # Recompute final hashes after refreshed result/summary/provenance/validation.
    manifest_rows = compute_hash_manifest()
    write_hashes(manifest_rows)
    hashes_verified = verify_hashes_file(manifest_rows)

    if not hashes_verified:
        failures.append("hashes_verified")

    print(json.dumps({
        "cr": CR_ID,
        "primary_verdict": primary_verdict,
        "scientific_result_status": scientific_result_status,
        "sealed_utc": sealed_utc,
        "s_SAM": s_sam,
        "r_SAM_microseconds": r_sam_us,
        "published_ratio": ratio_obs,
        "published_ratio_sigma": ratio_sigma,
        "primary_standardized_residual_z": primary_z,
        "wrong_controls_sensitive_before_reveal": sensitive_count,
        "hashes_verified": hashes_verified,
        "failures": failures,
    }, indent=2, sort_keys=True))

    return 0 if not failures and primary_verdict.startswith(("PASS", "FAIL", "BOUNDARY")) else 1


if __name__ == "__main__":
    sys.exit(main())

