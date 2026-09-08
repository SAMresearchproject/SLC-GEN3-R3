#!/usr/bin/env python3
"""Exact complete-prime scheduler tournament for N72 final refinement."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import multiprocessing as mp
import os
from pathlib import Path
import queue
import resource
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from typing import Any, Mapping

import numpy as np


HERE = Path(__file__).resolve().parent
QC_ROOT = HERE.parent
REPO_ROOT = QC_ROOT.parents[1]
H14E_ROOT = QC_ROOT / "SLCV05_N72_H14E_SHARED_PROJECTION_CACHE_V1"
if str(H14E_ROOT) not in sys.path:
    sys.path.insert(0, str(H14E_ROOT))

from shared_projection_cache import (  # noqa: E402
    build_cache_file,
    canonical_bytes,
    canonical_sha256,
    compile_descriptor,
    open_cache_file,
    sha256_file,
)

from native_arithmetic import NativeArithmetic  # noqa: E402
from refined_kernel import (  # noqa: E402
    KernelPolicy,
    retained_port_root_batch_refined,
)


CAMPAIGN_ID = "SLCV05_N72_FINAL_REFINEMENT_V1"
SCHEMA = "SLCV05_N72_FINAL_REFINEMENT_SCHEDULER_TOURNAMENT_V1"
TRIAL_SCHEMA = "SLCV05_N72_FINAL_REFINEMENT_COMPLETE_PRIME_TRIAL_V1"
ROOT_COUNT = 512
MINIMUM_AVAILABLE_MEMORY_BYTES = 8 * (1 << 30)
PER_WORKER_ADDRESS_SPACE_BYTES = 6 * (1 << 30)
EXPECTED_INSTANCE_SHA256 = (
    "396778a771378af50f7f6cbe594d93245fb0b653aef3f7a91b142c1e51fe450b"
)

WORK = HERE / "work" / "SCHEDULER_TOURNAMENT"
RELEASE = HERE / "release"
TRIAL_ROOT = WORK / "trials"
NATIVE_LIBRARY = WORK / "native" / "libslcv05_n72_refined.so"
NATIVE_RECEIPT = WORK / "NATIVE_BUILD_RECEIPT.json"
CACHE_RECEIPT = WORK / "CACHE_RECEIPT.json"
MANIFEST_PATH = WORK / "SOURCE_MANIFEST.json"
RESULT_PATH = RELEASE / "SCHEDULER_TOURNAMENT_RESULT.json"
RESULT_MD = RELEASE / "SCHEDULER_TOURNAMENT_RESULT.md"

ENGINE_PATH = (
    QC_ROOT
    / "SLCX032_EXACT_N72_SUPERCELL_N144_DAISY_CHAIN_DISCOVERY"
    / "slcx032_engine.py"
)
INSTANCE_PATH = (
    QC_ROOT
    / "SLCX025_EXACT_N72_FRUSTRATED_ISING_DOS_EXTENSION"
    / "SLCX025_N72_VAULT.json"
)
H14D_PLAN = (
    QC_ROOT
    / "SLCV05_N72_H14D_T18_CANDIDATE"
    / "work"
    / "N72_H14D_T18"
    / "EXECUTION_PLAN.json"
)
H14E_RESULT = (
    H14E_ROOT
    / "release"
    / "SLCV0.5-72-H14E-T18_CANDIDATE_RESULT.json"
)
CONTRACT = HERE / "FINAL_REFINEMENT_CONTRACT.json"

P_CPUS = [0, 2, 4, 6, 8, 10]
E2_CPUS = [16, 17]
E4_CPUS = [16, 17, 18, 19]
E6_CPUS = [14, 15, 16, 17, 18, 19]
ALL_PHYSICAL_CPUS = P_CPUS + [12, 13, 14, 15, 16, 17, 18, 19]

INITIAL_PROFILES = [
    {"profile_id": "P6_B4", "cpu_ids": P_CPUS, "root_batch_size": 4},
    {
        "profile_id": "H14_B4",
        "cpu_ids": ALL_PHYSICAL_CPUS,
        "root_batch_size": 4,
    },
    {
        "profile_id": "P6E2_B4",
        "cpu_ids": P_CPUS + E2_CPUS,
        "root_batch_size": 4,
    },
    {
        "profile_id": "H14_B2",
        "cpu_ids": ALL_PHYSICAL_CPUS,
        "root_batch_size": 2,
    },
    {
        "profile_id": "P6E4_B4",
        "cpu_ids": P_CPUS + E4_CPUS,
        "root_batch_size": 4,
    },
    {
        "profile_id": "H14_B8",
        "cpu_ids": ALL_PHYSICAL_CPUS,
        "root_batch_size": 8,
    },
    {
        "profile_id": "P6E6_B4",
        "cpu_ids": P_CPUS + E6_CPUS,
        "root_batch_size": 4,
    },
]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object at {path}")
    return value


def atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(canonical_bytes(value) + b"\n")
    os.replace(temporary, path)


def sealed(unsigned: Mapping[str, Any], key: str) -> dict[str, Any]:
    return {**unsigned, key: canonical_sha256(unsigned)}


def validate_seal(value: Mapping[str, Any], key: str) -> None:
    unsigned = dict(value)
    observed = unsigned.pop(key, None)
    if observed != canonical_sha256(unsigned):
        raise RuntimeError(f"self-seal mismatch: {key}")


def load_engine(path: Path, module_name: str) -> Any:
    if module_name in sys.modules:
        return sys.modules[module_name]
    specification = importlib.util.spec_from_file_location(module_name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load exact engine: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    return module


def meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        key, rest = line.split(":", 1)
        values[key] = int(rest.strip().split()[0]) * 1024
    return values


def maximum_rss_bytes() -> int:
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def pid_rollup(pid: int) -> dict[str, int]:
    output: dict[str, int] = {}
    try:
        lines = Path(f"/proc/{pid}/smaps_rollup").read_text(
            encoding="utf-8"
        ).splitlines()
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        return output
    for line in lines:
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        parts = rest.strip().split()
        if parts and parts[0].isdigit():
            output[key] = int(parts[0]) * 1024
    return output


def build_native_library() -> dict[str, Any]:
    NATIVE_LIBRARY.parent.mkdir(parents=True, exist_ok=False)
    command = [
        "gcc",
        "-O3",
        "-march=native",
        "-std=c11",
        "-fPIC",
        "-shared",
        str(HERE / "refined_native.c"),
        "-o",
        str(NATIVE_LIBRARY),
    ]
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    gcc_version = subprocess.run(
        ["gcc", "--version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()[0]
    receipt = sealed(
        {
            "schema": "SLCV05_N72_REFINED_NATIVE_BUILD_V1",
            "campaign_id": CAMPAIGN_ID,
            "command": command,
            "compiler": gcc_version,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "build_seconds": time.perf_counter() - started,
            "source_sha256": sha256_file(HERE / "refined_native.c"),
            "library_bytes": NATIVE_LIBRARY.stat().st_size,
            "library_sha256": sha256_file(NATIVE_LIBRARY),
            "specialization": "GENERIC_PLUS_EXACT_FOUR_ROOT_P4",
        },
        "receipt_sha256",
    )
    atomic_json(NATIVE_RECEIPT, receipt)
    return receipt


def source_manifest() -> dict[str, Any]:
    paths = [
        HERE / "README.md",
        CONTRACT,
        HERE / "refined_kernel.py",
        HERE / "native_arithmetic.py",
        HERE / "refined_native.c",
        Path(__file__).resolve(),
        H14E_ROOT / "shared_projection_cache.py",
        ENGINE_PATH,
        INSTANCE_PATH,
        H14D_PLAN,
        H14E_RESULT,
    ]
    rows = []
    for path in paths:
        resolved = path.resolve()
        rows.append(
            {
                "path": str(resolved.relative_to(REPO_ROOT)),
                "bytes": resolved.stat().st_size,
                "sha256": sha256_file(resolved),
            }
        )
    return sealed(
        {
            "schema": "SLCV05_N72_FINAL_REFINEMENT_SOURCE_MANIFEST_V1",
            "campaign_id": CAMPAIGN_ID,
            "sources": rows,
        },
        "manifest_sha256",
    )


def validate_cached_indices(cache: Any) -> dict[str, Any]:
    checked_maps = 0
    checked_entries = 0
    maximum_index = 0
    for step, raw_step in zip(cache.maps, cache.descriptor["steps"]):
        for projection, row in zip(step, raw_step["maps"]):
            if projection.size != int(row["entry_count"]):
                raise RuntimeError("cache projection extent changed")
            observed_maximum = int(projection.max(initial=0))
            one_maximum = observed_maximum | int(row["eliminated_factor_bit"])
            factor_extent = 1 << int(row["factor_scope_width"])
            if one_maximum >= factor_extent:
                raise RuntimeError("cache projection escaped factor extent")
            checked_maps += 1
            checked_entries += int(projection.size)
            maximum_index = max(maximum_index, one_maximum)
    return {
        "checked_maps": checked_maps,
        "checked_entries": checked_entries,
        "maximum_selected_index": maximum_index,
        "all_zero_and_one_indices_in_factor_extent": True,
    }


def worker_loop(
    node_id: str,
    cpu_id: int,
    instance: Mapping[str, Any],
    plan: Mapping[str, Any],
    task_queue: Any,
    result_queue: Any,
    cache_path: str,
    cache_descriptor: Mapping[str, Any],
    native_library: str,
) -> None:
    cache = None
    try:
        resource.setrlimit(
            resource.RLIMIT_AS,
            (PER_WORKER_ADDRESS_SPACE_BYTES, PER_WORKER_ADDRESS_SPACE_BYTES),
        )
        os.sched_setaffinity(0, {cpu_id})
        engine = load_engine(ENGINE_PATH, f"refinement_engine_{node_id}_{os.getpid()}")
        ownership = engine.factor_ownership(instance)
        local_instance = engine._local_instance(instance, ownership)
        order = [int(value) for value in plan["conditional_order"]]
        ports = [int(value) for value in plan["port_order"]]
        cache = open_cache_file(Path(cache_path), cache_descriptor)
        native = NativeArithmetic(Path(native_library))
        native.self_test([int(value) for value in plan["primes"]])
        result_queue.put(
            {
                "kind": "READY",
                "node_id": node_id,
                "pid": os.getpid(),
                "requested_cpu_id": cpu_id,
                "observed_affinity": sorted(os.sched_getaffinity(0)),
                "maximum_rss_bytes": maximum_rss_bytes(),
            }
        )
        while True:
            task = task_queue.get()
            if task is None:
                break
            root_start = int(task["root_start"])
            root_stop = int(task["root_stop"])
            prime = int(task["prime"])
            point_count = root_stop - root_start
            policy = KernelPolicy(
                policy_id="NATIVE_FUSED_EXACT_P4_OR_GENERIC_C64K_REUSE",
                chunk_cap=65536,
                inplace_products=False,
                reusable_product_buffers=True,
                reusable_one_index=False,
                reusable_take_buffer=False,
                native_fused=True,
            )
            points = engine._zeta_points(
                prime,
                int(plan["y_ntt_length"]),
                root_start,
                root_stop,
            )
            started_wall = time.perf_counter()
            started_cpu = time.process_time()
            terminal, structural = retained_port_root_batch_refined(
                engine,
                local_instance,
                order,
                points,
                prime,
                ports,
                cache,
                policy,
                native,
            )
            result_queue.put(
                {
                    "kind": "DONE",
                    "node_id": node_id,
                    "task_index": int(task["task_index"]),
                    "root_start": root_start,
                    "root_stop": root_stop,
                    "point_count": point_count,
                    "evaluations": terminal.tolist(),
                    "evaluation_sha256": canonical_sha256(terminal.tolist()),
                    "structural_metrics": {
                        key: int(value) for key, value in structural.items()
                    },
                    "wall_seconds": time.perf_counter() - started_wall,
                    "process_cpu_seconds": time.process_time() - started_cpu,
                    "maximum_rss_bytes": maximum_rss_bytes(),
                }
            )
    except BaseException as error:
        result_queue.put(
            {
                "kind": "ERROR",
                "node_id": node_id,
                "error": f"{type(error).__name__}: {error}",
                "traceback": traceback.format_exc(),
            }
        )
    finally:
        if cache is not None:
            cache.close()


def run_trial(
    *,
    trial_id: str,
    profile: Mapping[str, Any],
    instance: Mapping[str, Any],
    plan: Mapping[str, Any],
    prime: int,
    cache_path: Path,
    cache_descriptor: Mapping[str, Any],
    expected_evaluation_sha256: str,
) -> dict[str, Any]:
    cpu_ids = [int(value) for value in profile["cpu_ids"]]
    batch_size = int(profile["root_batch_size"])
    if ROOT_COUNT % batch_size:
        raise RuntimeError("root batch does not divide the transform")
    memory_before = meminfo()
    if memory_before["MemAvailable"] < MINIMUM_AVAILABLE_MEMORY_BYTES:
        raise RuntimeError("8 GiB system reserve is unavailable")
    context = mp.get_context("spawn")
    task_queue = context.Queue()
    result_queue = context.Queue()
    node_ids = [f"N{index:02d}" for index in range(len(cpu_ids))]
    processes = {
        node_id: context.Process(
            target=worker_loop,
            args=(
                node_id,
                cpu_id,
                instance,
                plan,
                task_queue,
                result_queue,
                str(cache_path),
                cache_descriptor,
                str(NATIVE_LIBRARY),
            ),
            name=f"SLCV05-REFINE-{trial_id}-{node_id}",
        )
        for node_id, cpu_id in zip(node_ids, cpu_ids)
    }
    pool_started = time.perf_counter()
    for process in processes.values():
        process.start()
    readiness: dict[str, dict[str, Any]] = {}
    pids: dict[str, int] = {}
    minimum_available = memory_before["MemAvailable"]
    peak_aggregate_rss = 0
    peak_aggregate_pss = 0

    def sample_memory() -> None:
        nonlocal minimum_available, peak_aggregate_rss, peak_aggregate_pss
        rollups = [pid_rollup(pid) for pid in pids.values()]
        peak_aggregate_rss = max(
            peak_aggregate_rss, sum(row.get("Rss", 0) for row in rollups)
        )
        peak_aggregate_pss = max(
            peak_aggregate_pss, sum(row.get("Pss", 0) for row in rollups)
        )
        minimum_available = min(
            minimum_available, meminfo()["MemAvailable"]
        )
        if minimum_available < MINIMUM_AVAILABLE_MEMORY_BYTES:
            raise RuntimeError("scheduler trial crossed the 8 GiB reserve")

    records: dict[int, dict[str, Any]] = {}
    task_count = ROOT_COUNT // batch_size
    try:
        while len(readiness) < len(node_ids):
            message = result_queue.get(timeout=120)
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')} startup error: "
                    f"{message.get('error')}\n{message.get('traceback')}"
                )
            if message.get("kind") != "READY":
                raise RuntimeError("unexpected scheduler startup message")
            node_id = str(message["node_id"])
            expected_cpu = cpu_ids[node_ids.index(node_id)]
            if message["observed_affinity"] != [expected_cpu]:
                raise RuntimeError("worker affinity differs from profile")
            readiness[node_id] = dict(message)
            pids[node_id] = int(message["pid"])
        startup_seconds = time.perf_counter() - pool_started
        sample_memory()
        for task_index, root_start in enumerate(
            range(0, ROOT_COUNT, batch_size)
        ):
            task_queue.put(
                {
                    "task_index": task_index,
                    "prime": prime,
                    "root_start": root_start,
                    "root_stop": root_start + batch_size,
                }
            )
        kernel_started = time.perf_counter()
        last_sample = 0.0
        while len(records) < task_count:
            try:
                message = result_queue.get(timeout=0.25)
            except queue.Empty:
                message = None
            now = time.monotonic()
            if now - last_sample >= 0.75:
                sample_memory()
                last_sample = now
            if message is None:
                if any(not process.is_alive() for process in processes.values()):
                    raise RuntimeError("worker exited during scheduler trial")
                continue
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')} error: {message.get('error')}\n"
                    f"{message.get('traceback')}"
                )
            if message.get("kind") != "DONE":
                raise RuntimeError("unexpected scheduler task message")
            task_index = int(message["task_index"])
            if task_index in records:
                raise RuntimeError("duplicate scheduler task completion")
            records[task_index] = dict(message)
            if len(records) % max(1, task_count // 4) == 0:
                print(
                    json.dumps(
                        {
                            "event": "TRIAL_PROGRESS",
                            "trial_id": trial_id,
                            "completed": len(records),
                            "task_count": task_count,
                            "elapsed_seconds": time.perf_counter()
                            - kernel_started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
        kernel_wall_seconds = time.perf_counter() - kernel_started
        sample_memory()
    finally:
        for _ in node_ids:
            try:
                task_queue.put(None)
            except BaseException:
                pass
        for process in processes.values():
            process.join(timeout=10)
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)

    ordered = [records[index] for index in range(task_count)]
    evaluations = [[0] * ROOT_COUNT for _ in range(16)]
    for task_index, row in enumerate(ordered):
        expected_start = task_index * batch_size
        if int(row["root_start"]) != expected_start:
            raise RuntimeError("ordered scheduler roots changed")
        for state in range(16):
            evaluations[state][int(row["root_start"]) : int(row["root_stop"])] = [
                int(value) for value in row["evaluations"][state]
            ]
    evaluation_sha256 = canonical_sha256(evaluations)
    if evaluation_sha256 != expected_evaluation_sha256:
        raise RuntimeError("refined complete prime differs from H14E")
    structural = ordered[0]["structural_metrics"]
    if any(row["structural_metrics"] != structural for row in ordered[1:]):
        raise RuntimeError("structural metrics changed within scheduler trial")
    task_counts = {node_id: 0 for node_id in node_ids}
    task_wall_by_node = {node_id: 0.0 for node_id in node_ids}
    for row in ordered:
        node_id = str(row["node_id"])
        task_counts[node_id] += 1
        task_wall_by_node[node_id] += float(row["wall_seconds"])
    result = sealed(
        {
            "schema": TRIAL_SCHEMA,
            "campaign_id": CAMPAIGN_ID,
            "trial_id": trial_id,
            "profile_id": str(profile["profile_id"]),
            "prime": prime,
            "root_batch_size": batch_size,
            "worker_count": len(cpu_ids),
            "requested_cpu_ids": cpu_ids,
            "task_count": task_count,
            "readiness": readiness,
            "startup_seconds": startup_seconds,
            "kernel_wall_seconds": kernel_wall_seconds,
            "roots_per_second": ROOT_COUNT / kernel_wall_seconds,
            "sum_task_wall_seconds": sum(
                float(row["wall_seconds"]) for row in ordered
            ),
            "sum_task_cpu_seconds": sum(
                float(row["process_cpu_seconds"]) for row in ordered
            ),
            "task_count_by_node": task_counts,
            "task_wall_seconds_by_node": task_wall_by_node,
            "all_workers_active": all(value > 0 for value in task_counts.values()),
            "available_memory_before_bytes": memory_before["MemAvailable"],
            "minimum_available_memory_bytes": minimum_available,
            "peak_aggregate_worker_rss_bytes": peak_aggregate_rss,
            "peak_aggregate_worker_pss_bytes": peak_aggregate_pss,
            "system_reserve_maintained": minimum_available
            >= MINIMUM_AVAILABLE_MEMORY_BYTES,
            "structural_metrics": structural,
            "evaluation_sha256": evaluation_sha256,
            "expected_h14e_evaluation_sha256": expected_evaluation_sha256,
            "exact_equality_with_h14e": True,
            "evaluations": evaluations,
            "ordered_task_roster": [
                {
                    "task_index": int(row["task_index"]),
                    "root_start": int(row["root_start"]),
                    "root_stop": int(row["root_stop"]),
                    "node_id": str(row["node_id"]),
                    "wall_seconds": float(row["wall_seconds"]),
                    "process_cpu_seconds": float(row["process_cpu_seconds"]),
                    "maximum_rss_bytes": int(row["maximum_rss_bytes"]),
                    "evaluation_sha256": str(row["evaluation_sha256"]),
                }
                for row in ordered
            ],
        },
        "trial_sha256",
    )
    atomic_json(TRIAL_ROOT / f"{trial_id}.json", result)
    print(
        json.dumps(
            {
                "event": "TRIAL_COMPLETE",
                "trial_id": trial_id,
                "profile_id": profile["profile_id"],
                "wall_seconds": kernel_wall_seconds,
                "roots_per_second": ROOT_COUNT / kernel_wall_seconds,
                "minimum_available_gib": minimum_available / (1 << 30),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return result


def render(result: Mapping[str, Any]) -> str:
    selected = result["selection"]
    lines = [
        "# N72 final-refinement scheduler tournament",
        "",
        f"- Status: `{result['execution_status']}`",
        f"- Classification: **{result['result_classification']}**",
        f"- Complete-prime trials: `{result['trial_count']}`",
        f"- All exact against H14E: `{result['checks']['all_trials_exact']}`",
        f"- Selected profile: `{selected['profile_id']}`",
        f"- Selected root batch: `{selected['root_batch_size']}`",
        f"- Selected CPUs: `{selected['cpu_ids']}`",
        f"- Selected median complete-prime wall: `{selected['median_wall_seconds']:.9f}` seconds",
        f"- H14E complete-prime wall: `{result['comparison']['h14e_complete_prime_wall_seconds']:.9f}` seconds",
        f"- H14E/selected ratio: `{result['comparison']['h14e_over_selected_ratio']:.6f}`",
        f"- Result SHA-256: `{result['result_sha256']}`",
        "",
        "The tournament changes the arithmetic implementation and execution",
        "roster only. The N72 instance, elimination order, three CRT primes,",
        "T18/q semantics, and exact integer reconstruction remain fixed.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError(f"{key} must equal 1")
    if WORK.exists() or RESULT_PATH.exists() or RESULT_MD.exists():
        raise RuntimeError("scheduler tournament artifacts already exist")
    WORK.mkdir(parents=True, exist_ok=False)
    TRIAL_ROOT.mkdir(parents=True, exist_ok=False)
    RELEASE.mkdir(parents=True, exist_ok=True)
    manifest = source_manifest()
    atomic_json(MANIFEST_PATH, manifest)
    native_receipt = build_native_library()

    contract = load_json(CONTRACT)
    plan = load_json(H14D_PLAN)
    h14e = load_json(H14E_RESULT)
    validate_seal(plan, "plan_sha256")
    validate_seal(h14e, "result_sha256")
    if (
        contract.get("schema") != "SLCV05_N72_FINAL_REFINEMENT_CONTRACT_V1"
        or h14e.get("execution_status") != "COMPLETED"
    ):
        raise RuntimeError("final-refinement authority changed")
    instance = load_json(INSTANCE_PATH)
    if instance.get("instance_sha256") != EXPECTED_INSTANCE_SHA256:
        raise RuntimeError("N72 instance changed")
    engine = load_engine(ENGINE_PATH, "refinement_tournament_parent_engine")
    engine.validate_n72_instance(instance)
    local_instance = engine._local_instance(
        instance, engine.factor_ownership(instance)
    )
    descriptor = compile_descriptor(
        engine,
        local_instance,
        plan["conditional_order"],
        plan["port_order"],
    )
    expected_evaluation_sha256 = str(
        h14e["prime_lanes"][0]["evaluation_sha256"]
    )
    prime = int(plan["primes"][0])
    temporary_root = Path(
        tempfile.mkdtemp(prefix="slcv05_refinement_cache_", dir="/tmp")
    )
    cache_path = temporary_root / "projection_cache.bin"
    cache_removed = False
    trials: list[dict[str, Any]] = []
    try:
        build_receipt = build_cache_file(cache_path, descriptor)
        if sha256_file(cache_path) != build_receipt["cache_sha256"]:
            raise RuntimeError("rebuilt projection cache hash changed")
        os.chmod(cache_path, 0o444)
        cache = open_cache_file(cache_path, descriptor)
        try:
            index_validation = validate_cached_indices(cache)
        finally:
            cache.close()
        cache_receipt = sealed(
            {
                "schema": "SLCV05_N72_FINAL_REFINEMENT_CACHE_RECEIPT_V1",
                "campaign_id": CAMPAIGN_ID,
                "descriptor_sha256": descriptor["descriptor_sha256"],
                "cache_sha256": build_receipt["cache_sha256"],
                "cache_bytes": build_receipt["cache_bytes"],
                "entry_count": descriptor["entry_count"],
                "read_only_mode": "0444",
                "index_validation": index_validation,
            },
            "receipt_sha256",
        )
        atomic_json(CACHE_RECEIPT, cache_receipt)
        for index, profile in enumerate(INITIAL_PROFILES):
            trials.append(
                run_trial(
                    trial_id=f"INITIAL_{index:02d}_{profile['profile_id']}",
                    profile=profile,
                    instance=instance,
                    plan=plan,
                    prime=prime,
                    cache_path=cache_path,
                    cache_descriptor=descriptor,
                    expected_evaluation_sha256=expected_evaluation_sha256,
                )
            )
        ranked = sorted(trials, key=lambda row: float(row["kernel_wall_seconds"]))
        finalist_ids = [str(ranked[0]["profile_id"]), str(ranked[1]["profile_id"])]
        profile_by_id = {
            str(profile["profile_id"]): profile for profile in INITIAL_PROFILES
        }
        confirmation_order = [
            finalist_ids[0],
            finalist_ids[1],
            finalist_ids[1],
            finalist_ids[0],
        ]
        for index, profile_id in enumerate(confirmation_order):
            trials.append(
                run_trial(
                    trial_id=f"CONFIRM_{index:02d}_{profile_id}",
                    profile=profile_by_id[profile_id],
                    instance=instance,
                    plan=plan,
                    prime=prime,
                    cache_path=cache_path,
                    cache_descriptor=descriptor,
                    expected_evaluation_sha256=expected_evaluation_sha256,
                )
            )
    finally:
        if cache_path.exists():
            cache_path.chmod(0o644)
            cache_path.unlink()
        if temporary_root.exists():
            shutil.rmtree(temporary_root)
        cache_removed = not cache_path.exists() and not temporary_root.exists()

    observations: dict[str, list[float]] = {}
    for trial in trials:
        observations.setdefault(str(trial["profile_id"]), []).append(
            float(trial["kernel_wall_seconds"])
        )
    finalist_statistics = []
    for profile_id in finalist_ids:
        values = sorted(observations[profile_id])
        median = values[len(values) // 2]
        finalist_statistics.append(
            {
                "profile_id": profile_id,
                "wall_seconds": observations[profile_id],
                "median_wall_seconds": median,
            }
        )
    finalist_statistics.sort(key=lambda row: row["median_wall_seconds"])
    winner_id = str(finalist_statistics[0]["profile_id"])
    winner_profile = next(
        profile for profile in INITIAL_PROFILES if profile["profile_id"] == winner_id
    )
    selected_median = float(finalist_statistics[0]["median_wall_seconds"])
    h14e_prime_wall = float(h14e["prime_lanes"][0]["kernel_wall_seconds"])
    checks = {
        "all_trials_exact": all(trial["exact_equality_with_h14e"] for trial in trials),
        "all_workers_active": all(trial["all_workers_active"] for trial in trials),
        "all_reserves_maintained": all(
            trial["system_reserve_maintained"] for trial in trials
        ),
        "eleven_complete_prime_trials": len(trials) == 11,
        "two_finalists_repeated_three_times": all(
            len(observations[profile_id]) == 3 for profile_id in finalist_ids
        ),
        "selected_below_h14e": selected_median < h14e_prime_wall,
        "cache_removed": cache_removed,
        "cache_indices_prevalidated": cache_receipt["index_validation"][
            "all_zero_and_one_indices_in_factor_extent"
        ],
    }
    if not all(checks.values()):
        failures = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"scheduler tournament checks failed: {failures}")
    selection = {
        "profile_id": winner_id,
        "cpu_ids": [int(value) for value in winner_profile["cpu_ids"]],
        "worker_count": len(winner_profile["cpu_ids"]),
        "root_batch_size": int(winner_profile["root_batch_size"]),
        "chunk_cap": 65536,
        "native_policy_id": "NATIVE_FUSED_EXACT_P4_OR_GENERIC_C64K_REUSE",
        "median_wall_seconds": selected_median,
        "observed_wall_seconds": observations[winner_id],
        "selection_rule": "LOWER_MEDIAN_OF_THREE_EXACT_COMPLETE_PRIME_RUNS",
    }
    unsigned = {
        "schema": SCHEMA,
        "campaign_id": CAMPAIGN_ID,
        "execution_status": "COMPLETED",
        "result_classification": "The test result suggests strong contact with the concept.",
        "release_promoted": False,
        "trial_count": len(trials),
        "prime": prime,
        "instance_sha256": instance["instance_sha256"],
        "manifest": manifest,
        "native_build": native_receipt,
        "cache_receipt": cache_receipt,
        "initial_profile_order": INITIAL_PROFILES,
        "finalist_ids": finalist_ids,
        "finalist_statistics": finalist_statistics,
        "selection": selection,
        "comparison": {
            "h14e_complete_prime_wall_seconds": h14e_prime_wall,
            "selected_median_wall_seconds": selected_median,
            "wall_seconds_saved": h14e_prime_wall - selected_median,
            "wall_reduction_percent": 100.0
            * (h14e_prime_wall - selected_median)
            / h14e_prime_wall,
            "h14e_over_selected_ratio": h14e_prime_wall / selected_median,
        },
        "trial_roster": [
            {
                "trial_id": trial["trial_id"],
                "profile_id": trial["profile_id"],
                "path": str(
                    (TRIAL_ROOT / f"{trial['trial_id']}.json").relative_to(
                        REPO_ROOT
                    )
                ),
                "trial_sha256": trial["trial_sha256"],
                "kernel_wall_seconds": trial["kernel_wall_seconds"],
                "roots_per_second": trial["roots_per_second"],
                "minimum_available_memory_bytes": trial[
                    "minimum_available_memory_bytes"
                ],
                "evaluation_sha256": trial["evaluation_sha256"],
            }
            for trial in trials
        ],
        "checks": checks,
        "all_checks_passed": True,
    }
    result = sealed(unsigned, "result_sha256")
    atomic_json(RESULT_PATH, result)
    RESULT_MD.write_text(render(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "event": "TOURNAMENT_COMPLETE",
                "winner": selection,
                "h14e_over_selected_ratio": result["comparison"][
                    "h14e_over_selected_ratio"
                ],
                "result_sha256": result["result_sha256"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
