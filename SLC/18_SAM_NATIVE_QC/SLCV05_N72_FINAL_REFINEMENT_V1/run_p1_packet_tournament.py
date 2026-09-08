#!/usr/bin/env python3
"""Test exact singleton-root kernels under different queue packet sizes."""

from __future__ import annotations

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


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_scheduler_tournament as base  # noqa: E402
from native_arithmetic_p1 import NativeArithmeticP1  # noqa: E402


SCHEMA = "SLCV05_N72_FINAL_REFINEMENT_P1_PACKET_TOURNAMENT_V1"
TRIAL_SCHEMA = "SLCV05_N72_FINAL_REFINEMENT_P1_PACKET_TRIAL_V1"
WORK = HERE / "work" / "P1_PACKET_TOURNAMENT"
TRIAL_ROOT = WORK / "trials"
NATIVE_LIBRARY = WORK / "native" / "libslcv05_n72_refined_p1.so"
NATIVE_RECEIPT = WORK / "NATIVE_BUILD_RECEIPT.json"
MANIFEST_PATH = WORK / "SOURCE_MANIFEST.json"
RESULT_PATH = HERE / "release" / "P1_PACKET_TOURNAMENT_RESULT.json"
RESULT_MD = HERE / "release" / "P1_PACKET_TOURNAMENT_RESULT.md"
CROSSED_RESULT = (
    HERE / "release" / "CROSSED_SCHEDULER_TOURNAMENT_RESULT.json"
)
CPU_IDS = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19]
PACKET_SIZES = [1, 4, 2, 8, 16]


def build_native() -> dict[str, Any]:
    NATIVE_LIBRARY.parent.mkdir(parents=True, exist_ok=False)
    command = [
        "gcc",
        "-O3",
        "-march=native",
        "-std=c11",
        "-fPIC",
        "-shared",
        str(HERE / "refined_native_p1.c"),
        "-o",
        str(NATIVE_LIBRARY),
    ]
    started = time.perf_counter()
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True
    )
    compiler = subprocess.run(
        ["gcc", "--version"], check=True, capture_output=True, text=True
    ).stdout.splitlines()[0]
    receipt = base.sealed(
        {
            "schema": "SLCV05_N72_REFINED_P1_NATIVE_BUILD_V1",
            "campaign_id": base.CAMPAIGN_ID,
            "command": command,
            "compiler": compiler,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "build_seconds": time.perf_counter() - started,
            "source_sha256": base.sha256_file(HERE / "refined_native_p1.c"),
            "included_source_sha256": base.sha256_file(
                HERE / "refined_native.c"
            ),
            "library_bytes": NATIVE_LIBRARY.stat().st_size,
            "library_sha256": base.sha256_file(NATIVE_LIBRARY),
            "specialization": "EXACT_SINGLETON_ROOT_P1_PLUS_INHERITED_P4",
        },
        "receipt_sha256",
    )
    base.atomic_json(NATIVE_RECEIPT, receipt)
    return receipt


def source_manifest() -> dict[str, Any]:
    paths = [
        Path(__file__).resolve(),
        HERE / "refined_native_p1.c",
        HERE / "native_arithmetic_p1.py",
        HERE / "refined_native.c",
        HERE / "native_arithmetic.py",
        HERE / "refined_kernel.py",
        HERE / "run_scheduler_tournament.py",
        CROSSED_RESULT,
        base.H14D_PLAN,
        base.INSTANCE_PATH,
        base.ENGINE_PATH,
        base.H14E_RESULT,
    ]
    rows = []
    for path in paths:
        resolved = path.resolve()
        rows.append(
            {
                "path": str(resolved.relative_to(base.REPO_ROOT)),
                "bytes": resolved.stat().st_size,
                "sha256": base.sha256_file(resolved),
            }
        )
    return base.sealed(
        {
            "schema": "SLCV05_N72_P1_PACKET_SOURCE_MANIFEST_V1",
            "campaign_id": base.CAMPAIGN_ID,
            "sources": rows,
        },
        "manifest_sha256",
    )


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
            (
                base.PER_WORKER_ADDRESS_SPACE_BYTES,
                base.PER_WORKER_ADDRESS_SPACE_BYTES,
            ),
        )
        os.sched_setaffinity(0, {cpu_id})
        engine = base.load_engine(
            base.ENGINE_PATH, f"p1_packet_engine_{node_id}_{os.getpid()}"
        )
        local_instance = engine._local_instance(
            instance, engine.factor_ownership(instance)
        )
        cache = base.open_cache_file(Path(cache_path), cache_descriptor)
        native = NativeArithmeticP1(Path(native_library))
        native.self_test([int(value) for value in plan["primes"]])
        policy = base.KernelPolicy(
            policy_id="NATIVE_FUSED_EXACT_P1_C64K_REUSE",
            chunk_cap=65536,
            inplace_products=False,
            reusable_product_buffers=True,
            reusable_one_index=False,
            reusable_take_buffer=False,
            native_fused=True,
        )
        order = [int(value) for value in plan["conditional_order"]]
        ports = [int(value) for value in plan["port_order"]]
        result_queue.put(
            {
                "kind": "READY",
                "node_id": node_id,
                "pid": os.getpid(),
                "observed_affinity": sorted(os.sched_getaffinity(0)),
                "maximum_rss_bytes": base.maximum_rss_bytes(),
            }
        )
        while True:
            task = task_queue.get()
            if task is None:
                break
            prime = int(task["prime"])
            packet_start = int(task["root_start"])
            packet_stop = int(task["root_stop"])
            evaluations = [[] for _ in range(16)]
            structural = None
            started_wall = time.perf_counter()
            started_cpu = time.process_time()
            for root in range(packet_start, packet_stop):
                points = engine._zeta_points(
                    prime, int(plan["y_ntt_length"]), root, root + 1
                )
                terminal, observed_structural = (
                    base.retained_port_root_batch_refined(
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
                )
                if structural is None:
                    structural = observed_structural
                elif structural != observed_structural:
                    raise RuntimeError("P1 structural metrics changed in packet")
                for state in range(16):
                    evaluations[state].append(int(terminal[state, 0]))
            result_queue.put(
                {
                    "kind": "DONE",
                    "node_id": node_id,
                    "task_index": int(task["task_index"]),
                    "root_start": packet_start,
                    "root_stop": packet_stop,
                    "evaluations": evaluations,
                    "evaluation_sha256": base.canonical_sha256(evaluations),
                    "structural_metrics": {
                        key: int(value) for key, value in structural.items()
                    },
                    "wall_seconds": time.perf_counter() - started_wall,
                    "process_cpu_seconds": time.process_time() - started_cpu,
                    "maximum_rss_bytes": base.maximum_rss_bytes(),
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
    packet_size: int,
    instance: Mapping[str, Any],
    plan: Mapping[str, Any],
    prime: int,
    cache_path: Path,
    descriptor: Mapping[str, Any],
    expected_sha256: str,
) -> dict[str, Any]:
    if base.ROOT_COUNT % packet_size:
        raise RuntimeError("packet size does not divide root count")
    memory_before = base.meminfo()
    if memory_before["MemAvailable"] < base.MINIMUM_AVAILABLE_MEMORY_BYTES:
        raise RuntimeError("8 GiB reserve unavailable")
    context = mp.get_context("spawn")
    task_queue = context.Queue()
    result_queue = context.Queue()
    node_ids = [f"N{index:02d}" for index in range(len(CPU_IDS))]
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
                descriptor,
                str(NATIVE_LIBRARY),
            ),
            name=f"SLCV05-P1-{trial_id}-{node_id}",
        )
        for node_id, cpu_id in zip(node_ids, CPU_IDS)
    }
    pool_started = time.perf_counter()
    for process in processes.values():
        process.start()
    readiness: dict[str, dict[str, Any]] = {}
    pids: dict[str, int] = {}
    minimum_available = memory_before["MemAvailable"]
    peak_rss = 0
    peak_pss = 0

    def sample_memory() -> None:
        nonlocal minimum_available, peak_rss, peak_pss
        rollups = [base.pid_rollup(pid) for pid in pids.values()]
        peak_rss = max(peak_rss, sum(row.get("Rss", 0) for row in rollups))
        peak_pss = max(peak_pss, sum(row.get("Pss", 0) for row in rollups))
        minimum_available = min(
            minimum_available, base.meminfo()["MemAvailable"]
        )
        if minimum_available < base.MINIMUM_AVAILABLE_MEMORY_BYTES:
            raise RuntimeError("P1 packet trial crossed 8 GiB reserve")

    packet_count = base.ROOT_COUNT // packet_size
    records: dict[int, dict[str, Any]] = {}
    try:
        while len(readiness) < len(node_ids):
            message = result_queue.get(timeout=120)
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')} startup: {message.get('error')}\n"
                    f"{message.get('traceback')}"
                )
            if message.get("kind") != "READY":
                raise RuntimeError("unexpected P1 startup message")
            node_id = str(message["node_id"])
            expected_cpu = CPU_IDS[node_ids.index(node_id)]
            if message["observed_affinity"] != [expected_cpu]:
                raise RuntimeError("P1 affinity changed")
            readiness[node_id] = dict(message)
            pids[node_id] = int(message["pid"])
        startup_seconds = time.perf_counter() - pool_started
        sample_memory()
        for task_index, root_start in enumerate(
            range(0, base.ROOT_COUNT, packet_size)
        ):
            task_queue.put(
                {
                    "task_index": task_index,
                    "prime": prime,
                    "root_start": root_start,
                    "root_stop": root_start + packet_size,
                }
            )
        kernel_started = time.perf_counter()
        last_sample = 0.0
        while len(records) < packet_count:
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
                    raise RuntimeError("P1 worker exited")
                continue
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')}: {message.get('error')}\n"
                    f"{message.get('traceback')}"
                )
            if message.get("kind") != "DONE":
                raise RuntimeError("unexpected P1 task message")
            task_index = int(message["task_index"])
            if task_index in records:
                raise RuntimeError("duplicate P1 packet")
            records[task_index] = dict(message)
            if len(records) % max(1, packet_count // 4) == 0:
                print(
                    json.dumps(
                        {
                            "event": "P1_PACKET_PROGRESS",
                            "trial_id": trial_id,
                            "completed": len(records),
                            "packet_count": packet_count,
                            "elapsed_seconds": time.perf_counter()
                            - kernel_started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
        kernel_wall = time.perf_counter() - kernel_started
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
    ordered = [records[index] for index in range(packet_count)]
    evaluations = [[0] * base.ROOT_COUNT for _ in range(16)]
    for task_index, row in enumerate(ordered):
        start = task_index * packet_size
        if int(row["root_start"]) != start:
            raise RuntimeError("P1 packet roots changed")
        for state in range(16):
            evaluations[state][start : start + packet_size] = [
                int(value) for value in row["evaluations"][state]
            ]
    evaluation_sha256 = base.canonical_sha256(evaluations)
    if evaluation_sha256 != expected_sha256:
        raise RuntimeError("P1 complete prime differs from H14E")
    structural = ordered[0]["structural_metrics"]
    if any(row["structural_metrics"] != structural for row in ordered[1:]):
        raise RuntimeError("P1 structural metrics changed across packets")
    task_counts = {node_id: 0 for node_id in node_ids}
    for row in ordered:
        task_counts[str(row["node_id"])] += 1
    result = base.sealed(
        {
            "schema": TRIAL_SCHEMA,
            "campaign_id": base.CAMPAIGN_ID,
            "trial_id": trial_id,
            "profile_id": f"H14_P1_PACKET{packet_size}",
            "prime": prime,
            "singleton_root_batch_size": 1,
            "queue_packet_size": packet_size,
            "packet_count": packet_count,
            "worker_count": len(CPU_IDS),
            "requested_cpu_ids": CPU_IDS,
            "startup_seconds": startup_seconds,
            "kernel_wall_seconds": kernel_wall,
            "roots_per_second": base.ROOT_COUNT / kernel_wall,
            "sum_packet_wall_seconds": sum(
                float(row["wall_seconds"]) for row in ordered
            ),
            "sum_packet_cpu_seconds": sum(
                float(row["process_cpu_seconds"]) for row in ordered
            ),
            "task_count_by_node": task_counts,
            "all_workers_active": all(value > 0 for value in task_counts.values()),
            "minimum_available_memory_bytes": minimum_available,
            "peak_aggregate_worker_rss_bytes": peak_rss,
            "peak_aggregate_worker_pss_bytes": peak_pss,
            "system_reserve_maintained": minimum_available
            >= base.MINIMUM_AVAILABLE_MEMORY_BYTES,
            "structural_metrics": structural,
            "evaluation_sha256": evaluation_sha256,
            "expected_h14e_evaluation_sha256": expected_sha256,
            "exact_equality_with_h14e": True,
            "evaluations": evaluations,
            "ordered_packet_roster": [
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
    base.atomic_json(TRIAL_ROOT / f"{trial_id}.json", result)
    print(
        json.dumps(
            {
                "event": "P1_PACKET_COMPLETE",
                "trial_id": trial_id,
                "packet_size": packet_size,
                "kernel_wall_seconds": kernel_wall,
                "roots_per_second": base.ROOT_COUNT / kernel_wall,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return result


def render(result: Mapping[str, Any]) -> str:
    selection = result["selection"]
    return "\n".join(
        [
            "# N72 P1 queue-packet tournament",
            "",
            f"- Status: `{result['execution_status']}`",
            f"- Classification: **{result['result_classification']}**",
            f"- Exact complete-prime trials: `{result['trial_count']}`",
            f"- Selected queue packet: `{selection['queue_packet_size']}`",
            f"- Selected median wall: `{selection['median_wall_seconds']:.9f}` seconds",
            f"- H14E/selected ratio: `{result['comparison']['h14e_over_selected_ratio']:.6f}`",
            f"- Prior H14/B1 over selected ratio: `{result['comparison']['prior_h14_b1_over_selected_ratio']:.6f}`",
            f"- Result SHA-256: `{result['result_sha256']}`",
            "",
        ]
    )


def main() -> int:
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError(f"{key} must equal 1")
    if WORK.exists() or RESULT_PATH.exists() or RESULT_MD.exists():
        raise RuntimeError("P1 packet artifacts already exist")
    WORK.mkdir(parents=True, exist_ok=False)
    TRIAL_ROOT.mkdir(parents=True, exist_ok=False)
    manifest = source_manifest()
    base.atomic_json(MANIFEST_PATH, manifest)
    native_receipt = build_native()
    crossed = base.load_json(CROSSED_RESULT)
    base.validate_seal(crossed, "result_sha256")
    if crossed.get("execution_status") != "COMPLETED":
        raise RuntimeError("crossed scheduler authority changed")
    plan = base.load_json(base.H14D_PLAN)
    instance = base.load_json(base.INSTANCE_PATH)
    base.validate_seal(plan, "plan_sha256")
    engine = base.load_engine(base.ENGINE_PATH, "p1_packet_parent_engine")
    engine.validate_n72_instance(instance)
    local_instance = engine._local_instance(
        instance, engine.factor_ownership(instance)
    )
    descriptor = base.compile_descriptor(
        engine,
        local_instance,
        plan["conditional_order"],
        plan["port_order"],
    )
    prime = int(plan["primes"][0])
    expected_sha256 = str(
        base.load_json(base.H14E_RESULT)["prime_lanes"][0][
            "evaluation_sha256"
        ]
    )
    temporary_root = Path(
        tempfile.mkdtemp(prefix="slcv05_p1_packet_cache_", dir="/tmp")
    )
    cache_path = temporary_root / "projection_cache.bin"
    cache_removed = False
    trials: list[dict[str, Any]] = []
    try:
        build_receipt = base.build_cache_file(cache_path, descriptor)
        if base.sha256_file(cache_path) != build_receipt["cache_sha256"]:
            raise RuntimeError("P1 cache hash changed")
        os.chmod(cache_path, 0o444)
        for index, packet_size in enumerate(PACKET_SIZES):
            trials.append(
                run_trial(
                    trial_id=f"P1_INITIAL_{index:02d}_PACKET{packet_size}",
                    packet_size=packet_size,
                    instance=instance,
                    plan=plan,
                    prime=prime,
                    cache_path=cache_path,
                    descriptor=descriptor,
                    expected_sha256=expected_sha256,
                )
            )
        ranked = sorted(trials, key=lambda row: float(row["kernel_wall_seconds"]))
        finalist_packets = [
            int(ranked[0]["queue_packet_size"]),
            int(ranked[1]["queue_packet_size"]),
        ]
        for index, packet_size in enumerate(
            [
                finalist_packets[0],
                finalist_packets[1],
                finalist_packets[1],
                finalist_packets[0],
            ]
        ):
            trials.append(
                run_trial(
                    trial_id=f"P1_CONFIRM_{index:02d}_PACKET{packet_size}",
                    packet_size=packet_size,
                    instance=instance,
                    plan=plan,
                    prime=prime,
                    cache_path=cache_path,
                    descriptor=descriptor,
                    expected_sha256=expected_sha256,
                )
            )
    finally:
        if cache_path.exists():
            cache_path.chmod(0o644)
            cache_path.unlink()
        if temporary_root.exists():
            shutil.rmtree(temporary_root)
        cache_removed = not cache_path.exists() and not temporary_root.exists()
    observations: dict[int, list[float]] = {}
    for trial in trials:
        observations.setdefault(int(trial["queue_packet_size"]), []).append(
            float(trial["kernel_wall_seconds"])
        )
    finalist_statistics = []
    for packet_size in finalist_packets:
        values = observations[packet_size]
        finalist_statistics.append(
            {
                "queue_packet_size": packet_size,
                "wall_seconds": values,
                "median_wall_seconds": sorted(values)[1],
            }
        )
    finalist_statistics.sort(key=lambda row: row["median_wall_seconds"])
    winner = finalist_statistics[0]
    selected_wall = float(winner["median_wall_seconds"])
    prior_wall = float(crossed["selection"]["median_wall_seconds"])
    h14e_wall = float(
        crossed["comparison"]["h14e_complete_prime_wall_seconds"]
    )
    selection = {
        "profile_id": f"H14_P1_PACKET{winner['queue_packet_size']}",
        "cpu_ids": CPU_IDS,
        "worker_count": len(CPU_IDS),
        "singleton_root_batch_size": 1,
        "queue_packet_size": int(winner["queue_packet_size"]),
        "chunk_cap": 65536,
        "native_policy_id": "NATIVE_FUSED_EXACT_P1_C64K_REUSE",
        "median_wall_seconds": selected_wall,
        "observed_wall_seconds": winner["wall_seconds"],
        "selection_rule": "LOWER_MEDIAN_OF_THREE_EXACT_P1_PACKET_TRIALS",
    }
    checks = {
        "all_trials_exact": all(
            trial["exact_equality_with_h14e"] for trial in trials
        ),
        "all_workers_active": all(trial["all_workers_active"] for trial in trials),
        "all_reserves_maintained": all(
            trial["system_reserve_maintained"] for trial in trials
        ),
        "nine_complete_prime_trials": len(trials) == 9,
        "two_finalists_repeated_three_times": all(
            len(observations[packet]) == 3 for packet in finalist_packets
        ),
        "p1_selected_below_prior_h14_b1": selected_wall < prior_wall,
        "cache_removed": cache_removed,
    }
    if not all(checks.values()):
        failures = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"P1 packet checks failed: {failures}")
    result = base.sealed(
        {
            "schema": SCHEMA,
            "campaign_id": base.CAMPAIGN_ID,
            "execution_status": "COMPLETED",
            "result_classification": "The test result suggests strong contact with the concept.",
            "release_promoted": False,
            "crossed_result_sha256": crossed["result_sha256"],
            "manifest": manifest,
            "native_build": native_receipt,
            "initial_packet_order": PACKET_SIZES,
            "finalist_packets": finalist_packets,
            "finalist_statistics": finalist_statistics,
            "selection": selection,
            "trial_count": len(trials),
            "comparison": {
                "h14e_complete_prime_wall_seconds": h14e_wall,
                "prior_h14_b1_median_wall_seconds": prior_wall,
                "selected_median_wall_seconds": selected_wall,
                "h14e_over_selected_ratio": h14e_wall / selected_wall,
                "prior_h14_b1_over_selected_ratio": prior_wall / selected_wall,
                "wall_reduction_from_h14e_percent": 100.0
                * (h14e_wall - selected_wall)
                / h14e_wall,
            },
            "trial_roster": [
                {
                    "trial_id": trial["trial_id"],
                    "queue_packet_size": trial["queue_packet_size"],
                    "path": str(
                        (TRIAL_ROOT / f"{trial['trial_id']}.json").relative_to(
                            base.REPO_ROOT
                        )
                    ),
                    "trial_sha256": trial["trial_sha256"],
                    "kernel_wall_seconds": trial["kernel_wall_seconds"],
                    "minimum_available_memory_bytes": trial[
                        "minimum_available_memory_bytes"
                    ],
                    "evaluation_sha256": trial["evaluation_sha256"],
                }
                for trial in trials
            ],
            "checks": checks,
            "all_checks_passed": True,
        },
        "result_sha256",
    )
    base.atomic_json(RESULT_PATH, result)
    RESULT_MD.write_text(render(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "event": "P1_PACKET_TOURNAMENT_COMPLETE",
                "selection": selection,
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
