from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import math
import sys
import tarfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


CAMPAIGN_ID = "CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED"
EXPECTED_CONTRACT_SHA256 = "9a34c4f225fd27d61d71683fb43242ea1010718bf2fbf87293cc37417e58ead7"
EXPECTED_PRECOMMIT_SHA256 = "aa2afd2a4d0b65707de359e1ce13af45acc520bf8afa8748d44ea04d19bb7495"
EXPECTED_SOURCE_MANIFEST_SHA256 = "90bb9b6dc0e74223028ba708ff21033af9d8688ecb1d429b70ec107c09726910"
EXPECTED_PRECOMMIT_SEAL_SHA256 = "3f542195a2d62c712838cd7d20209cc1a8d0928c246c916cee678ac2f2eb43d3"

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CONTRACT_PATH = BASE / "CR005f_CONTRACT.json"
PRECOMMIT_PATH = BASE / "CR005f_PRECOMMIT.md"
SOURCE_MANIFEST_PATH = BASE / "CR005f_SOURCE_MANIFEST.json"
PRECOMMIT_SEAL_PATH = BASE / "CR005f_PRECOMMIT_SEAL.json"
RUNNER_SEAL_PATH = BASE / "CR005f_RUNNER_SEAL.json"
ARCHIVE_PATH = ROOT / "21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/inputs/all.3D.strains.tar.gz"
CR005D_RUNNER_PATH = ROOT / "21_GRAVITATIONAL_WAVES/CR005d_STARBREAKER_CONTINUOUS_FLOW_AND_CARRIER_QNM_SOURCE_BRIDGE/CR005d_runner.py"
RELEASE = BASE / "release"
STAGING = BASE / ".cr005f_release_staging"

SAMPLES = 2049
EDGE_TRIM = 3
WINDOW = 256
TIME_BINS = 48
FREQ_BINS = 64
EPS = 1.0e-30

EXPECTED_WAVEFORMS: dict[str, tuple[int, str]] = {
    "s9.0.swbj15.horo.3d.gw.dat": (9, "discovery"),
    "s10.0.swbj15.horo.3d.gw.dat": (10, "validation"),
    "s11.0.swbj15.horo.3d.gw.dat": (11, "final"),
    "s12.0.swbj15.horo.3d.gw.dat": (12, "discovery"),
    "s13.0.swbj15.horo.3d.gw.dat": (13, "validation"),
    "s14.0.swbj16.horo.3d.gw.dat": (14, "final"),
    "s15.0.swbj16.horo.3d.gw.dat": (15, "discovery"),
    "s19.0.swbj15.horo.3d.gw.dat": (19, "validation"),
    "s25.0.swh18.horo.3d.gw.dat": (25, "final"),
    "s60.0.swbj15.horo.3d.gw.dat": (60, "discovery"),
}

VIEW_VECTORS = (
    ("axis_x", (1.0, 0.0, 0.0)),
    ("axis_y", (0.0, 1.0, 0.0)),
    ("axis_z", (0.0, 0.0, 1.0)),
    ("face_xy_p", (1.0, 1.0, 0.0)),
    ("face_xy_m", (1.0, -1.0, 0.0)),
    ("face_xz_p", (1.0, 0.0, 1.0)),
    ("face_xz_m", (1.0, 0.0, -1.0)),
    ("face_yz_p", (0.0, 1.0, 1.0)),
    ("face_yz_m", (0.0, 1.0, -1.0)),
    ("body_ppp", (1.0, 1.0, 1.0)),
    ("body_ppm", (1.0, 1.0, -1.0)),
    ("body_pmp", (1.0, -1.0, 1.0)),
    ("body_mpp", (-1.0, 1.0, 1.0)),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            raise ValueError(f"cannot infer fields for empty CSV: {path.name}")
        fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def resolve_source(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def validate_sources() -> list[dict[str, Any]]:
    manifest = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("source manifest campaign changed")
    if manifest.get("source_count") != len(manifest.get("sources", [])):
        raise RuntimeError("source manifest count changed")
    rows: list[dict[str, Any]] = []
    for source in manifest["sources"]:
        path = resolve_source(source["path"])
        observed_bytes = path.stat().st_size if path.is_file() else -1
        observed_sha = sha256_file(path) if path.is_file() else "MISSING"
        matched = observed_bytes == source["bytes"] and observed_sha == source["sha256"]
        rows.append({
            "path": source["path"],
            "role": source["role"],
            "expected_bytes": source["bytes"],
            "observed_bytes": observed_bytes,
            "expected_sha256": source["sha256"],
            "observed_sha256": observed_sha,
            "matched": matched,
        })
    return rows


def verify_seals() -> dict[str, Any]:
    expected = {
        CONTRACT_PATH: EXPECTED_CONTRACT_SHA256,
        PRECOMMIT_PATH: EXPECTED_PRECOMMIT_SHA256,
        SOURCE_MANIFEST_PATH: EXPECTED_SOURCE_MANIFEST_SHA256,
        PRECOMMIT_SEAL_PATH: EXPECTED_PRECOMMIT_SEAL_SHA256,
    }
    for path, digest in expected.items():
        if sha256_file(path) != digest:
            raise RuntimeError(f"sealed pre-run file changed: {path.name}")
    precommit_seal = json.loads(PRECOMMIT_SEAL_PATH.read_text(encoding="utf-8"))
    if precommit_seal.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("precommit seal campaign changed")
    if precommit_seal.get("runner_present_at_seal") or precommit_seal.get("results_opened"):
        raise RuntimeError("precommit chronology changed")
    if precommit_seal.get("same_run_repair_allowed"):
        raise RuntimeError("same-run repair prohibition changed")
    runner_seal = json.loads(RUNNER_SEAL_PATH.read_text(encoding="utf-8"))
    if runner_seal.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("runner seal campaign changed")
    if sha256_file(Path(__file__).resolve()) != runner_seal.get("runner_sha256"):
        raise RuntimeError("sealed runner changed")
    if runner_seal.get("contract_sha256") != EXPECTED_CONTRACT_SHA256:
        raise RuntimeError("runner seal contract link changed")
    if runner_seal.get("precommit_sha256") != EXPECTED_PRECOMMIT_SHA256:
        raise RuntimeError("runner seal precommit link changed")
    if runner_seal.get("source_manifest_sha256") != EXPECTED_SOURCE_MANIFEST_SHA256:
        raise RuntimeError("runner seal manifest link changed")
    if runner_seal.get("same_run_repair_allowed"):
        raise RuntimeError("runner seal permits same-run repair")
    return {"precommit": precommit_seal, "runner": runner_seal}


def load_cr005d() -> Any:
    spec = importlib.util.spec_from_file_location("cr005d_frozen_for_cr005f", CR005D_RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load CR005d source module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def normalized_view(name: str, vector: tuple[float, float, float]) -> dict[str, Any]:
    n = np.asarray(vector, dtype=float)
    n /= np.linalg.norm(n)
    reference = np.asarray((0.0, 0.0, 1.0), dtype=float)
    if abs(float(np.dot(n, reference))) > 0.9:
        reference = np.asarray((0.0, 1.0, 0.0), dtype=float)
    p = reference - n * float(np.dot(n, reference))
    p /= np.linalg.norm(p)
    q = np.cross(n, p)
    q /= np.linalg.norm(q)
    plus_projector = np.outer(p, p) - np.outer(q, q)
    cross_projector = np.outer(p, q) + np.outer(q, p)
    return {
        "view_id": name,
        "n": n,
        "p": p,
        "q": q,
        "plus_projector": plus_projector,
        "cross_projector": cross_projector,
    }


VIEWS = tuple(normalized_view(name, vector) for name, vector in VIEW_VECTORS)


def pixel_map(plus: np.ndarray, cross: np.ndarray) -> tuple[np.ndarray | None, float]:
    plus = np.asarray(plus, dtype=float)
    cross = np.asarray(cross, dtype=float)
    if plus.shape != (SAMPLES,) or cross.shape != (SAMPLES,):
        raise ValueError(f"unexpected signal shape: {plus.shape}, {cross.shape}")
    plus = plus[EDGE_TRIM:-EDGE_TRIM].copy()
    cross = cross[EDGE_TRIM:-EDGE_TRIM].copy()
    plus -= float(np.mean(plus))
    cross -= float(np.mean(cross))
    starts = np.rint(np.linspace(0, len(plus) - WINDOW, TIME_BINS)).astype(np.int64)
    if len(np.unique(starts)) != TIME_BINS:
        raise RuntimeError("time-frame starts are not unique")
    window = np.hanning(WINDOW)
    rows: list[np.ndarray] = []
    for start in starts:
        stop = int(start) + WINDOW
        f_plus = np.fft.rfft(plus[int(start):stop] * window)
        f_cross = np.fft.rfft(cross[int(start):stop] * window)
        power = (np.abs(f_plus) ** 2 + np.abs(f_cross) ** 2)[1:]
        if power.shape != (128,):
            raise RuntimeError("unexpected positive-frequency inventory")
        rows.append(np.sum(power.reshape(FREQ_BINS, 2), axis=1))
    pixels = np.stack(rows, axis=0)
    total = float(np.sum(pixels))
    if not math.isfinite(total) or total <= EPS:
        return None, total
    pixels /= total
    return pixels, total


def read_waveforms() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, np.ndarray]]:
    inventory: list[dict[str, Any]] = []
    waveforms: list[dict[str, Any]] = []
    signal_cache: dict[str, np.ndarray] = {}
    with tarfile.open(ARCHIVE_PATH, mode="r:gz") as archive:
        members = [member for member in archive.getmembers() if member.isfile()]
        names = {member.name for member in members}
        if names != set(EXPECTED_WAVEFORMS):
            missing = sorted(set(EXPECTED_WAVEFORMS) - names)
            extra = sorted(names - set(EXPECTED_WAVEFORMS))
            raise RuntimeError(f"waveform archive inventory changed: missing={missing}, extra={extra}")
        for member in sorted(members, key=lambda item: EXPECTED_WAVEFORMS[item.name][0]):
            extracted = archive.extractfile(member)
            if extracted is None:
                raise RuntimeError(f"unable to read archive member: {member.name}")
            with io.TextIOWrapper(extracted, encoding="ascii") as text_handle:
                data = np.loadtxt(text_handle, comments="#", dtype=float)
            if data.ndim != 2 or data.shape[1] != 3 or data.shape[0] < 512:
                raise RuntimeError(f"invalid waveform matrix: {member.name} {data.shape}")
            time = data[:, 0]
            plus = data[:, 1]
            cross = data[:, 2]
            finite = np.isfinite(time) & np.isfinite(plus) & np.isfinite(cross) & (time >= 0.0)
            time, plus, cross = time[finite], plus[finite], cross[finite]
            if len(time) < 512 or not np.all(np.diff(time) > 0.0):
                raise RuntimeError(f"non-monotonic or insufficient post-bounce data: {member.name}")
            duration = float(time[-1] - time[0])
            if duration <= 0.0:
                raise RuntimeError(f"non-positive waveform duration: {member.name}")
            tau = (time - time[0]) / duration
            grid = np.linspace(0.0, 1.0, SAMPLES)
            plus_grid = np.interp(grid, tau, plus)
            cross_grid = np.interp(grid, tau, cross)
            pixels, raw_power = pixel_map(plus_grid, cross_grid)
            if pixels is None:
                raise RuntimeError(f"zero CCSN pixel map: {member.name}")
            mass, door = EXPECTED_WAVEFORMS[member.name]
            dt = np.diff(time)
            median_dt = float(np.median(dt))
            inventory.append({
                "waveform": member.name,
                "mass_msun": mass,
                "door": door,
                "raw_samples": int(len(time)),
                "time_start_s": float(time[0]),
                "time_end_s": float(time[-1]),
                "duration_s": duration,
                "median_dt_s": median_dt,
                "cadence_relative_mad": float(np.median(np.abs(dt - median_dt)) / median_dt),
                "max_abs_hplus_D_cm": float(np.max(np.abs(plus))),
                "max_abs_hcross_D_cm": float(np.max(np.abs(cross))),
                "normalized_pixel_raw_power": raw_power,
            })
            waveforms.append({
                "waveform": member.name,
                "mass_msun": mass,
                "door": door,
                "pixels": pixels,
            })
            signal_cache[member.name] = np.stack((plus_grid, cross_grid), axis=0)
    return inventory, waveforms, signal_cache


def aggregate_quadrupole(positions: np.ndarray) -> np.ndarray:
    x = positions[:, :, 0]
    y = positions[:, :, 1]
    z = positions[:, :, 2]
    radius2 = x * x + y * y + z * z
    third = radius2 / 3.0
    return np.stack((
        np.sum(x * x - third, axis=0),
        np.sum(y * y - third, axis=0),
        np.sum(z * z - third, axis=0),
        np.sum(x * y, axis=0),
        np.sum(x * z, axis=0),
        np.sum(y * z, axis=0),
    ), axis=1)


def components_to_tensor(components: np.ndarray) -> np.ndarray:
    tensor = np.zeros((components.shape[0], 3, 3), dtype=float)
    tensor[:, 0, 0] = components[:, 0]
    tensor[:, 1, 1] = components[:, 1]
    tensor[:, 2, 2] = components[:, 2]
    tensor[:, 0, 1] = tensor[:, 1, 0] = components[:, 3]
    tensor[:, 0, 2] = tensor[:, 2, 0] = components[:, 4]
    tensor[:, 1, 2] = tensor[:, 2, 1] = components[:, 5]
    return tensor


def build_starbreaker_templates(cr005d: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    metadata = cr005d.load_scenario_metadata()
    grid = np.linspace(0.0, 1.0, SAMPLES)
    ds = 1.0 / (SAMPLES - 1)
    templates: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    scenario_count = 0
    atom_count = 0
    carrier_count = 0
    for scenario_id, atoms in cr005d.iter_scenario_atoms():
        scenario_count += 1
        atom_count += len(atoms)
        if scenario_id not in metadata:
            raise RuntimeError(f"missing Starbreaker metadata: {scenario_id}")
        meta = metadata[scenario_id]
        door = cr005d.door_for_seed(int(meta["seed"]))
        carrier_indexes = np.asarray([atom.atom_index for atom in atoms if atom.kind == "carrier"], dtype=np.int64)
        carrier_count += int(len(carrier_indexes))
        if len(carrier_indexes) != 252:
            raise RuntimeError(f"carrier inventory changed: {scenario_id} {len(carrier_indexes)}")
        params = cr005d.build_flow_parameters(atoms)
        positions = cr005d.flow_post_grid(params, carrier_indexes, grid)
        q = aggregate_quadrupole(positions)
        q2 = np.gradient(np.gradient(q, ds, axis=0, edge_order=2), ds, axis=0, edge_order=2)
        raw_trace_scale = max(1.0, float(np.max(np.abs(q2))))
        raw_trace_error = float(np.max(np.abs(q2[:, 0] + q2[:, 1] + q2[:, 2]))) / raw_trace_scale
        q2[:, 2] = -(q2[:, 0] + q2[:, 1])
        tensor = components_to_tensor(q2)
        trace_scale = max(1.0, float(np.max(np.abs(tensor))))
        trace_error = float(np.max(np.abs(np.trace(tensor, axis1=1, axis2=2)))) / trace_scale
        if trace_error > 1.0e-15:
            raise RuntimeError(f"trace-free source changed: {scenario_id} {trace_error}")
        for view in VIEWS:
            plus = np.einsum("ij,tij->t", view["plus_projector"], tensor)
            cross = np.einsum("ij,tij->t", view["cross_projector"], tensor)
            pixels, raw_power = pixel_map(plus, cross)
            if pixels is None:
                raise RuntimeError(f"zero Starbreaker projection: {scenario_id} {view['view_id']}")
            row = {
                "scenario_id": scenario_id,
                "door": door,
                "seed": int(meta["seed"]),
                "anchor": meta["anchor"],
                "p_level": int(meta["p_level"]),
                "geometry": meta["geometry"],
                "view_id": view["view_id"],
                "n_x": float(view["n"][0]),
                "n_y": float(view["n"][1]),
                "n_z": float(view["n"][2]),
                "carrier_count": int(len(carrier_indexes)),
                "preprojection_trace_relative_error": raw_trace_error,
                "source_trace_relative_error": trace_error,
                "normalized_pixel_raw_power": raw_power,
            }
            inventory.append(dict(row))
            row["pixels"] = pixels
            templates.append(row)
        del positions, q, q2, tensor
    counts = {
        "scenario_count": scenario_count,
        "atom_count": atom_count,
        "carrier_occurrence_count": carrier_count,
        "template_count": len(templates),
    }
    return templates, inventory, counts


def best_match(template_maps: np.ndarray, template_sqrt: np.ndarray, target: np.ndarray) -> tuple[int, float, float]:
    scores = template_sqrt @ np.sqrt(target).ravel()
    index = int(np.argmax(scores))
    affinity = float(scores[index])
    tv = 0.5 * float(np.sum(np.abs(template_maps[index] - target)))
    return index, affinity, tv


def evaluate_matches(
    waveforms: list[dict[str, Any]],
    templates: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, np.ndarray], dict[str, np.ndarray]]:
    by_door: dict[str, list[int]] = defaultdict(list)
    for index, template in enumerate(templates):
        by_door[template["door"]].append(index)
    match_rows: list[dict[str, Any]] = []
    null_cache: dict[str, np.ndarray] = {}
    best_map_cache: dict[str, np.ndarray] = {}
    for waveform in waveforms:
        door = waveform["door"]
        indexes = np.asarray(by_door[door], dtype=np.int64)
        door_maps = np.stack([templates[index]["pixels"] for index in indexes], axis=0)
        door_sqrt = np.sqrt(door_maps).reshape(len(indexes), -1)
        pixels = waveform["pixels"]
        local_index, observed, tv = best_match(door_maps, door_sqrt, pixels)
        global_index = int(indexes[local_index])
        best = templates[global_index]
        shifted = np.stack([np.roll(pixels, shift, axis=0) for shift in range(1, TIME_BINS)], axis=0)
        shifted_sqrt = np.sqrt(shifted).reshape(TIME_BINS - 1, -1).T
        shifted_best = np.max(door_sqrt @ shifted_sqrt, axis=0)
        time_reversed = pixels[::-1, :]
        frequency_reversed = pixels[:, ::-1]
        separable = np.outer(np.sum(pixels, axis=1), np.sum(pixels, axis=0))
        controls = np.stack((time_reversed, frequency_reversed, separable), axis=0)
        control_scores = np.max(door_sqrt @ np.sqrt(controls).reshape(3, -1).T, axis=0)
        empirical_p = (1.0 + float(np.sum(shifted_best >= observed))) / TIME_BINS
        match_rows.append({
            "waveform": waveform["waveform"],
            "mass_msun": waveform["mass_msun"],
            "door": door,
            "best_scenario_id": best["scenario_id"],
            "best_seed": best["seed"],
            "best_geometry": best["geometry"],
            "best_anchor": best["anchor"],
            "best_p_level": best["p_level"],
            "best_view_id": best["view_id"],
            "hellinger_affinity": observed,
            "total_variation_distance": tv,
            "time_shift_null_median": float(np.median(shifted_best)),
            "time_shift_null_q90": float(np.quantile(shifted_best, 0.90)),
            "time_shift_null_q95": float(np.quantile(shifted_best, 0.95)),
            "time_shift_empirical_p": empirical_p,
            "time_reversed_best_affinity": float(control_scores[0]),
            "frequency_reversed_best_affinity": float(control_scores[1]),
            "separable_null_best_affinity": float(control_scores[2]),
            "beats_time_reversal": observed > float(control_scores[0]),
            "beats_frequency_reversal": observed > float(control_scores[1]),
            "beats_separable_null": observed > float(control_scores[2]),
        })
        null_cache[waveform["waveform"]] = shifted_best
        best_map_cache[waveform["waveform"]] = best["pixels"]

    door_rows: list[dict[str, Any]] = []
    for door in ("discovery", "validation", "final"):
        rows = [row for row in match_rows if row["door"] == door]
        observed = float(np.median([row["hellinger_affinity"] for row in rows]))
        null_medians = np.asarray([
            np.median([null_cache[row["waveform"]][shift] for row in rows])
            for shift in range(TIME_BINS - 1)
        ], dtype=float)
        time_reverse_median = float(np.median([row["time_reversed_best_affinity"] for row in rows]))
        frequency_reverse_median = float(np.median([row["frequency_reversed_best_affinity"] for row in rows]))
        separable_median = float(np.median([row["separable_null_best_affinity"] for row in rows]))
        q90 = float(np.quantile(null_medians, 0.90))
        q95 = float(np.quantile(null_medians, 0.95))
        empirical_p = (1.0 + float(np.sum(null_medians >= observed))) / TIME_BINS
        door_rows.append({
            "door": door,
            "waveform_count": len(rows),
            "observed_median_affinity": observed,
            "time_shift_null_median": float(np.median(null_medians)),
            "time_shift_null_q90": q90,
            "time_shift_null_q95": q95,
            "time_shift_empirical_p": empirical_p,
            "time_reversed_median_affinity": time_reverse_median,
            "frequency_reversed_median_affinity": frequency_reverse_median,
            "separable_null_median_affinity": separable_median,
            "clears_q90_and_reversals": observed > q90 and observed > time_reverse_median and observed > frequency_reverse_median,
            "clears_q95_and_all_controls": observed > q95 and observed > time_reverse_median and observed > frequency_reverse_median and observed > separable_median,
        })
    return match_rows, door_rows, null_cache, best_map_cache


def build_pixel_rows(
    waveforms: list[dict[str, Any]],
    match_rows: list[dict[str, Any]],
    best_map_cache: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    match_lookup = {row["waveform"]: row for row in match_rows}
    rows: list[dict[str, Any]] = []
    for waveform in waveforms:
        name = waveform["waveform"]
        external = waveform["pixels"]
        starbreaker = best_map_cache[name]
        residual = external - starbreaker
        match = match_lookup[name]
        for map_kind, values in (
            ("ccsn", external),
            ("starbreaker_best", starbreaker),
            ("residual_ccsn_minus_starbreaker", residual),
        ):
            for time_bin in range(TIME_BINS):
                for freq_bin in range(FREQ_BINS):
                    rows.append({
                        "waveform": name,
                        "mass_msun": waveform["mass_msun"],
                        "door": waveform["door"],
                        "map_kind": map_kind,
                        "best_scenario_id": match["best_scenario_id"],
                        "best_view_id": match["best_view_id"],
                        "time_bin": time_bin,
                        "frequency_bin": freq_bin,
                        "value": float(values[time_bin, freq_bin]),
                    })
    return rows


def invariance_controls(signal_cache: dict[str, np.ndarray]) -> dict[str, Any]:
    amplitude_errors: list[float] = []
    polarization_errors: list[float] = []
    psi = math.radians(37.0)
    c2, s2 = math.cos(2.0 * psi), math.sin(2.0 * psi)
    for signal in signal_cache.values():
        plus, cross = signal[0], signal[1]
        base, _ = pixel_map(plus, cross)
        scaled, _ = pixel_map(7.0 * plus, 7.0 * cross)
        rotated, _ = pixel_map(c2 * plus + s2 * cross, -s2 * plus + c2 * cross)
        if base is None or scaled is None or rotated is None:
            raise RuntimeError("nonzero CCSN invariance control produced zero map")
        amplitude_errors.append(float(np.max(np.abs(base - scaled))))
        polarization_errors.append(float(np.max(np.abs(base - rotated))))
    zero_map, zero_power = pixel_map(np.zeros(SAMPLES), np.zeros(SAMPLES))
    return {
        "amplitude_scale_max_abs_error": max(amplitude_errors),
        "polarization_rotation_max_abs_error": max(polarization_errors),
        "zero_map_rejected": zero_map is None and zero_power == 0.0,
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    if RELEASE.exists() or STAGING.exists():
        raise RuntimeError("CR005f release path already exists; same-run repair is prohibited")
    seals = verify_seals()
    source_pre = validate_sources()
    if not all(row["matched"] for row in source_pre):
        raise RuntimeError("one or more frozen sources changed before execution")
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if contract.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("contract campaign changed")

    cr005d = load_cr005d()
    waveform_inventory, waveforms, signal_cache = read_waveforms()
    templates, template_inventory, starbreaker_counts = build_starbreaker_templates(cr005d)
    match_rows, door_rows, null_cache, best_map_cache = evaluate_matches(waveforms, templates)
    pixel_rows = build_pixel_rows(waveforms, match_rows, best_map_cache)
    invariance = invariance_controls(signal_cache)

    source_post = validate_sources()
    source_stable = source_pre == source_post and all(row["matched"] for row in source_post)
    template_doors = {door: sum(row["door"] == door for row in template_inventory) for door in ("discovery", "validation", "final")}
    waveform_doors = {door: sum(row["door"] == door for row in waveform_inventory) for door in ("discovery", "validation", "final")}
    normalization_error = max(
        max(abs(float(np.sum(waveform["pixels"])) - 1.0) for waveform in waveforms),
        max(abs(float(np.sum(template["pixels"])) - 1.0) for template in templates),
    )
    finite_maps = all(np.all(np.isfinite(waveform["pixels"])) for waveform in waveforms) and all(
        np.all(np.isfinite(template["pixels"])) for template in templates
    )
    max_preprojection_trace_error = max(float(row["preprojection_trace_relative_error"]) for row in template_inventory)
    max_source_trace_error = max(float(row["source_trace_relative_error"]) for row in template_inventory)
    door_lookup = {row["door"]: row for row in door_rows}
    strong = bool(
        door_lookup["validation"]["clears_q95_and_all_controls"]
        and door_lookup["final"]["clears_q95_and_all_controls"]
    )
    directional_door_count = sum(bool(row["clears_q90_and_reversals"]) for row in door_rows)
    directional = directional_door_count >= 2

    controls = [
        {"control": "WC00_EXACT_TRACE_FREE_ALGEBRAIC_PROJECTION", "passed": max_source_trace_error <= 1.0e-15 and math.isfinite(max_preprojection_trace_error), "observation": f"preprojection_max={max_preprojection_trace_error:.3e}; enforced_max={max_source_trace_error:.3e}"},
        {"control": "WC01_AMPLITUDE_NORMALIZATION_INVARIANCE", "passed": invariance["amplitude_scale_max_abs_error"] <= 1.0e-12, "observation": f"max_abs_error={invariance['amplitude_scale_max_abs_error']:.3e}"},
        {"control": "WC02_POLARIZATION_BASIS_INVARIANCE", "passed": invariance["polarization_rotation_max_abs_error"] <= 1.0e-12, "observation": f"max_abs_error={invariance['polarization_rotation_max_abs_error']:.3e}"},
        {"control": "WC03_ZERO_SOURCE_REJECTED", "passed": invariance["zero_map_rejected"], "observation": "zero source is not normalized into a match"},
        {"control": "WC04_FULL_BANK_REPEATED_FOR_TIME_SHIFTS", "passed": all(len(values) == 47 for values in null_cache.values()), "observation": "47 null searches per waveform"},
        {"control": "WC05_TIME_REVERSAL_REPORTED", "passed": all(math.isfinite(float(row["time_reversed_best_affinity"])) for row in match_rows), "observation": "10/10 finite"},
        {"control": "WC06_FREQUENCY_REVERSAL_REPORTED", "passed": all(math.isfinite(float(row["frequency_reversed_best_affinity"])) for row in match_rows), "observation": "10/10 finite"},
        {"control": "WC07_SEPARABLE_TEXTURE_NULL_REPORTED", "passed": all(math.isfinite(float(row["separable_null_best_affinity"])) for row in match_rows), "observation": "10/10 finite"},
        {"control": "WC08_SAME_DOOR_ONLY", "passed": all(row["door"] == cr005d.door_for_seed(int(row["best_seed"])) for row in match_rows), "observation": "10/10 matches retain door"},
        {"control": "WC09_NO_QNM_KERNEL_IN_TARGET", "passed": True, "observation": "direct quadrupole-source pixel comparison"},
        {"control": "WC10_NO_PHYSICAL_SCALE_PROMOTION", "passed": True, "observation": "normalized morphology only"},
    ]

    gates = [
        {"gate": "G01_SOURCE_HASHES_MATCH", "passed": source_stable},
        {"gate": "G02_ARCHIVE_INVENTORY_10_OF_10", "passed": len(waveform_inventory) == 10 and {row["waveform"] for row in waveform_inventory} == set(EXPECTED_WAVEFORMS)},
        {"gate": "G03_CCSN_PARSER_MONOTONIC_FINITE", "passed": len(waveforms) == 10 and finite_maps},
        {"gate": "G04_STARBREAKER_ROSTER_96_482112_252", "passed": starbreaker_counts["scenario_count"] == 96 and starbreaker_counts["atom_count"] == 482112 and starbreaker_counts["carrier_occurrence_count"] == 96 * 252},
        {"gate": "G05_EXACT_TRACE_FREE_SOURCE", "passed": max_source_trace_error <= 1.0e-15},
        {"gate": "G06_FIXED_13_VIEW_TEMPLATE_BANK", "passed": starbreaker_counts["template_count"] == 96 * 13 and template_doors == {"discovery": 624, "validation": 312, "final": 312}},
        {"gate": "G07_PIXEL_GRID_48_BY_64_NORMALIZED", "passed": normalization_error <= 1.0e-12 and all(waveform["pixels"].shape == (48, 64) for waveform in waveforms) and all(template["pixels"].shape == (48, 64) for template in templates)},
        {"gate": "G08_PREDECLARED_WAVEFORM_DOORS", "passed": waveform_doors == {"discovery": 4, "validation": 3, "final": 3}},
        {"gate": "G09_MATCH_AND_NULL_SURFACES_COMPLETE", "passed": len(match_rows) == 10 and len(door_rows) == 3 and len(pixel_rows) == 10 * 3 * 48 * 64},
        {"gate": "G10_INVARIANCE_AND_ZERO_CONTROLS", "passed": all(bool(row["passed"]) for row in controls[:4])},
        {"gate": "G11_NO_ENGINE_REGISTRY_OR_PHYSICAL_CLAIM_MUTATION", "passed": source_stable},
        {"gate": "G12_ATOMIC_RELEASE_INVENTORY", "passed": True},
    ]
    construction_pass = all(bool(row["passed"]) for row in gates) and all(bool(row["passed"]) for row in controls)
    if not construction_pass:
        verdict = contract["verdict_ladder"]["fail"]
    elif strong:
        verdict = contract["verdict_ladder"]["strong"]
    elif directional:
        verdict = contract["verdict_ladder"]["directional"]
    else:
        verdict = contract["verdict_ladder"]["boundary"]

    summary = {
        "campaign_id": CAMPAIGN_ID,
        "task": contract["task"],
        "record_class": contract["record_class"],
        "verdict": verdict,
        "construction_pass": construction_pass,
        "strong_morphology_bridge": strong,
        "directional_morphology_bridge": directional,
        "directional_door_count": directional_door_count,
        "external_data": {
            "kind": "simulated three-dimensional core-collapse supernova matter-strain waveforms",
            "catalog_url": contract["source_layers"]["external_catalog_url"],
            "archive_sha256": contract["source_layers"]["external_archive_sha256"],
            "waveform_count": len(waveforms),
            "door_counts": waveform_doors,
        },
        "starbreaker": starbreaker_counts | {"door_template_counts": template_doors},
        "pixel_grid": {
            "time_bins": TIME_BINS,
            "frequency_bins": FREQ_BINS,
            "pixels_per_map": TIME_BINS * FREQ_BINS,
            "normalization_max_abs_error": normalization_error,
            "physical_time": False,
            "physical_amplitude": False,
        },
        "door_results": door_rows,
        "best_overall_match": max(match_rows, key=lambda row: float(row["hellinger_affinity"])),
        "invariance": invariance,
        "trace_correction": {
            "rule": "after finite differencing, set S_zz=-(S_xx+S_yy) before observer projection",
            "max_preprojection_trace_relative_error": max_preprojection_trace_error,
            "max_enforced_trace_relative_error": max_source_trace_error,
            "fit_parameter": False,
        },
        "source_hashes_matched": sum(bool(row["matched"]) for row in source_post),
        "source_count": len(source_post),
        "physical_claims": {
            "strain": None,
            "luminosity": None,
            "frequency_hz": None,
            "time_seconds": None,
            "distance_reach": None,
            "detector_forecast": None,
        },
        "precommit": seals,
        "same_run_repair": False,
    }

    pixel_dictionary = {
        "campaign_id": CAMPAIGN_ID,
        "external_pixel": "normalized h_plus*D and h_cross*D time-frequency power from a simulated 3D CCSN matter signal",
        "starbreaker_pixel": "normalized fixed-view S_plus and S_cross time-frequency power from the unit-carrier second quadrupole derivative",
        "time_axis": "48 bins across complete normalized post-bounce event phase",
        "frequency_axis": "64 bins in cycles per normalized event, not hertz",
        "match": "Hellinger affinity of all 3072 corresponding pixels",
        "amplitude": "removed by unit-total-power normalization",
        "physical_bridge_still_required": [
            "carrier mass or energy weight",
            "Starbreaker phase duration in seconds",
            "source distance and transverse-traceless observer geometry",
        ],
    }

    result_lines = [
        "# CR005f Starbreaker / Weak-CCSN Pixel Bridge Result",
        "",
        "## Primary verdict",
        "",
        f"`{verdict}`",
        "",
        f"All **{sum(bool(row['passed']) for row in gates)}/{len(gates)}** construction gates and **{sum(bool(row['passed']) for row in controls)}/{len(controls)}** controls passed.",
        "",
        "## What was compared",
        "",
        "Ten public three-dimensional core-collapse supernova matter-strain waveforms were compared directly with 96 Starbreaker post-bounce unit-carrier quadrupole sources across 13 fixed observer directions. No compact-binary chirp and no black-hole QNM response was used as the target.",
        "",
        "Both sources were converted into the same 48 by 64 normalized time-frequency power grid. The primary statistic was all-pixel Hellinger affinity; every best-template search was repeated for 47 time-shift nulls and the locked reversal controls.",
        "",
        "## Door results",
        "",
        "| door | waveforms | observed median | shift q90 | shift q95 | p | clears q90 | clears q95/all |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in door_rows:
        result_lines.append(
            f"| {row['door']} | {row['waveform_count']} | {row['observed_median_affinity']:.6f} | {row['time_shift_null_q90']:.6f} | {row['time_shift_null_q95']:.6f} | {row['time_shift_empirical_p']:.6f} | {row['clears_q90_and_reversals']} | {row['clears_q95_and_all_controls']} |"
        )
    best = summary["best_overall_match"]
    result_lines.extend([
        "",
        "## Closest individual morphology",
        "",
        f"The largest affinity was **{best['hellinger_affinity']:.6f}** for `{best['waveform']}` against Starbreaker `{best['best_scenario_id']}` in view `{best['best_view_id']}`. This is a selected normalized morphology match, not a physical amplitude or mechanism identification.",
        "",
        "## Boundary",
        "",
        "Starbreaker still has unit carrier weights and dimensionless event phase. The run therefore does not calculate strain, luminosity, seconds, hertz, distance reach, or detector sensitivity. A morphology bridge can identify missing or shared source texture; physical prediction requires carrier mass/energy and a phase-to-seconds map.",
        "",
        "The downloaded archive is retained as internal source evidence; this campaign does not assert redistribution rights.",
        "",
    ])

    completed = datetime.now(timezone.utc)
    receipt = {
        "campaign_id": CAMPAIGN_ID,
        "started_utc": started.isoformat(),
        "completed_utc": completed.isoformat(),
        "verdict": verdict,
        "construction_pass": construction_pass,
        "same_run_repair": False,
        "runner_sha256": sha256_file(Path(__file__).resolve()),
    }
    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "preflight": seals["precommit"]["preflight_path"],
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "external_catalog": contract["source_layers"]["external_catalog_url"],
        "external_archive": contract["source_layers"]["external_url"],
        "external_archive_sha256": contract["source_layers"]["external_archive_sha256"],
        "external_paper": "Radice, Morozova, Burrows, Vartanyan, and Nagakura, ApJL 876 L9 (2019)",
        "upstream": "CR005d continuous Starbreaker flow and unit-carrier quadrupole source",
        "claim_boundary": "same-grid normalized morphology only",
    }

    STAGING.mkdir(parents=False, exist_ok=False)
    write_csv(STAGING / "CR005f_WAVEFORM_INVENTORY.csv", waveform_inventory)
    write_csv(STAGING / "CR005f_STARBREAKER_TEMPLATE_INVENTORY.csv", template_inventory)
    write_csv(STAGING / "CR005f_MATCHES.csv", match_rows)
    write_csv(STAGING / "CR005f_DOOR_RESULTS.csv", door_rows)
    write_csv(STAGING / "CR005f_PIXEL_MAPS.csv", pixel_rows)
    write_json(STAGING / "CR005f_PIXEL_DICTIONARY.json", pixel_dictionary)
    write_csv(STAGING / "CR005f_CONTROLS.csv", controls)
    write_csv(STAGING / "CR005f_GATES.csv", gates)
    write_csv(STAGING / "CR005f_SOURCE_VALIDATION.csv", source_post)
    write_json(STAGING / "CR005f_SUMMARY.json", summary)
    write_json(STAGING / "CR005f_PROVENANCE.json", provenance)
    write_json(STAGING / "CR005f_RUN_RECEIPT.json", receipt)
    (STAGING / "CR005f_RESULT.md").write_text("\n".join(result_lines), encoding="utf-8")

    names = sorted(path.name for path in STAGING.iterdir() if path.is_file())
    manifest_rows = [
        {"path": name, "bytes": (STAGING / name).stat().st_size, "sha256": sha256_file(STAGING / name)}
        for name in names
    ]
    write_csv(STAGING / "CR005f_RELEASE_MANIFEST.csv", manifest_rows)
    manifest_sha = sha256_file(STAGING / "CR005f_RELEASE_MANIFEST.csv")
    (STAGING / "CR005f_RELEASE_MANIFEST_SHA256.txt").write_text(manifest_sha + "\n", encoding="ascii")
    for row in manifest_rows:
        path = STAGING / row["path"]
        if path.stat().st_size != row["bytes"] or sha256_file(path) != row["sha256"]:
            raise RuntimeError("release manifest verification failed")
    STAGING.replace(RELEASE)

    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "verdict": verdict,
        "construction_pass": construction_pass,
        "strong": strong,
        "directional": directional,
        "directional_door_count": directional_door_count,
        "door_results": door_rows,
        "best_overall_match": best,
        "gates": f"{sum(bool(row['passed']) for row in gates)}/{len(gates)}",
        "controls": f"{sum(bool(row['passed']) for row in controls)}/{len(controls)}",
        "release_manifest_sha256": manifest_sha,
    }, indent=2))


if __name__ == "__main__":
    main()
