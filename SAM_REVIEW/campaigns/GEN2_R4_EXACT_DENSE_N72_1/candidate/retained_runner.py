#!/usr/bin/env python3
"""Fresh persistent-pool three-prime N72 final-refinement confirmation."""

from __future__ import annotations

import argparse
import importlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Mapping


CAMPAIGN_ROOT = Path(__file__).resolve().parent.parent
HERE = CAMPAIGN_ROOT.parents[2] / "SLC/18_SAM_NATIVE_QC/SLCV05_N72_FINAL_REFINEMENT_V1"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_scheduler_tournament as base  # noqa: E402
import run_u32_scheduler_tournament as u32  # noqa: E402


CAMPAIGN_ID = "GEN2_R4_EXACT_DENSE_N72_1"
DISPLAY_NAME = "SLCV0.5-72 final-refinement exact U32/H14/T18"
RESULT_SCHEMA = "SLCV05_N72_FINAL_REFINEMENT_FULL_RESULT_V1"
LANE_SCHEMA = "SLCV05_N72_FINAL_REFINEMENT_PERSISTENT_PRIME_LANE_V1"
FULL_ROOT = CAMPAIGN_ROOT / "execution" / "work"
RELEASE = CAMPAIGN_ROOT / "execution" / "release"
U32_RESULT = HERE / "release/U32_SCHEDULER_TOURNAMENT_RESULT.json"
H14E_RESULT = base.H14E_RESULT
H14D_ROOT = base.QC_ROOT / "SLCV05_N72_H14D_T18_CANDIDATE"
H14D_RESULT = (
    H14D_ROOT
    / "release"
    / "SLCV0.5-72-H14D-T18_CANDIDATE_RESULT.json"
)
H14D_PLAN = base.H14D_PLAN
CPU_IDS = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19]
ROOT_COUNT = 512
CHUNK_CAP = 131072


def run_paths(run_id: str) -> dict[str, Path]:
    work = FULL_ROOT / run_id
    return {
        "work": work,
        "lanes": work / "prime_lanes",
        "plan": work / "EXECUTION_PLAN.json",
        "manifest": work / "SOURCE_MANIFEST.json",
        "native": work / "native" / f"libslcv05_u32_UNROLL_C{CHUNK_CAP}.so",
        "native_receipt": work / "NATIVE_BUILD_RECEIPT.json",
        "cache": work / "CACHE_ARTIFACT.json",
        "operator": work / "LINKED_OPERATOR.json",
        "recovery": work / "N72_RECOVERY.json",
        "completion": work / "COMPLETION.json",
        "result": RELEASE / f"FULL_N72_{run_id}_RESULT.json",
        "markdown": RELEASE / f"FULL_N72_{run_id}_RESULT.md",
    }


def build_plan(
    inherited: Mapping[str, Any],
    tournament: Mapping[str, Any],
    run_id: str,
) -> dict[str, Any]:
    unsigned = dict(inherited)
    unsigned.pop("plan_sha256", None)
    active = [
        value
        for value in unsigned["active_changes"]
        if value != "TYPED_THETA18_OVER_ACTIVE_Z4_9"
    ]
    active.extend(
        [
            "ONE_READ_ONLY_MIXED_WIDTH_TOPOLOGY_PROJECTION_CACHE",
            "EXACT_U32_REDUCED_FACTOR_AND_PRODUCT_STORAGE",
            "U64_MULTIPLY_AND_BARRETT_REDUCTION",
            "SINGLETON_ROOT_KERNEL_AND_QUEUE_PACKET",
            "PERSISTENT_THREE_PRIME_H14_POOL",
            "TYPED_THETA18_OVER_ACTIVE_Z4_9",
        ]
    )
    unsigned.update(
        {
            "schema": "SLCV05_N72_FINAL_REFINEMENT_EXECUTION_PLAN_V1",
            "campaign_id": CAMPAIGN_ID,
            "run_id": run_id,
            "display_name": DISPLAY_NAME,
            "version_label": "SLCV0.5-FINAL-REFINEMENT",
            "scheduler_profile_id": "PERSISTENT_H14_U32_P1_PACKET1_C131072",
            "root_batch_size": 1,
            "queue_packet_size": 1,
            "cluster_size": len(CPU_IDS),
            "requested_cpu_ids": CPU_IDS,
            "active_changes": active,
            "native_execution": {
                "reduced_storage_bits": 32,
                "multiplication_bits": 64,
                "chunk_cap": CHUNK_CAP,
                "compiler_flags": ["-O3", "-march=native", "-funroll-loops"],
                "selection_result_sha256": tournament["result_sha256"],
                "selection_config_id": tournament["selection"]["config_id"],
            },
            "pool_lifetime": "ONE_POOL_RETAINED_ACROSS_ALL_THREE_CRT_PRIMES",
            "full_run_freshness": "CACHE_BINARY_POOL_AND_ALL_1536_SINGLETON_TASKS_FRESH",
        }
    )
    return base.sealed(unsigned, "plan_sha256")


def source_manifest(run_id: str) -> dict[str, Any]:
    paths = [
        HERE / "README.md",
        HERE / "FINAL_REFINEMENT_CONTRACT.json",
        Path(__file__).resolve(),
        HERE / "run_u32_scheduler_tournament.py",
        HERE / "refined_kernel_u32.py",
        HERE / "native_arithmetic_u32.py",
        HERE / "refined_native_u32_p1.c",
        U32_RESULT,
        base.H14E_ROOT / "shared_projection_cache.py",
        base.ENGINE_PATH,
        base.INSTANCE_PATH,
        H14D_PLAN,
        H14D_RESULT,
        H14D_ROOT / "slcv05_h14d_runner.py",
        H14D_ROOT / "slcv05_h14d_worker.py",
        base.QC_ROOT / "SLCV05_N72_H14C_T18_CANDIDATE" / "slcv05_ir.py",
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
            "schema": "SLCV05_N72_FINAL_REFINEMENT_FULL_SOURCE_MANIFEST_V1",
            "campaign_id": CAMPAIGN_ID,
            "run_id": run_id,
            "sources": rows,
        },
        "manifest_sha256",
    )


def build_native(path: Path, run_id: str) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=False)
    command = [
        "gcc",
        "-O3",
        "-march=native",
        "-funroll-loops",
        "-std=c11",
        "-fPIC",
        "-shared",
        str(HERE / "refined_native_u32_p1.c"),
        "-o",
        str(path),
    ]
    started = time.perf_counter()
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True
    )
    return base.sealed(
        {
            "schema": "SLCV05_N72_FINAL_REFINEMENT_NATIVE_BUILD_V1",
            "campaign_id": CAMPAIGN_ID,
            "run_id": run_id,
            "command": command,
            "compiler": subprocess.run(
                ["gcc", "--version"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()[0],
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "build_seconds": time.perf_counter() - started,
            "source_sha256": base.sha256_file(
                HERE / "refined_native_u32_p1.c"
            ),
            "library_bytes": path.stat().st_size,
            "library_sha256": base.sha256_file(path),
        },
        "receipt_sha256",
    )


class PersistentPool:
    def __init__(
        self,
        *,
        instance: Mapping[str, Any],
        plan: Mapping[str, Any],
        cache_path: Path,
        descriptor: Mapping[str, Any],
        native_library: Path,
    ) -> None:
        memory = base.meminfo()
        if memory["MemAvailable"] < base.MINIMUM_AVAILABLE_MEMORY_BYTES:
            raise RuntimeError("8 GiB reserve unavailable before persistent pool")
        self.memory_before = memory["MemAvailable"]
        self.minimum_available = self.memory_before
        self.peak_rss = 0
        self.peak_pss = 0
        self.context = mp.get_context("spawn")
        self.task_queue = self.context.Queue()
        self.result_queue = self.context.Queue()
        self.node_ids = [f"N{index:02d}" for index in range(len(CPU_IDS))]
        self.processes = {
            node_id: self.context.Process(
                target=u32.worker_loop,
                args=(
                    node_id,
                    cpu_id,
                    instance,
                    plan,
                    self.task_queue,
                    self.result_queue,
                    str(cache_path),
                    descriptor,
                    str(native_library),
                ),
                name=f"SLCV05-FINAL-{plan['run_id']}-{node_id}",
            )
            for node_id, cpu_id in zip(self.node_ids, CPU_IDS)
        }
        self.readiness: dict[str, dict[str, Any]] = {}
        self.pids: dict[str, int] = {}
        started = time.perf_counter()
        for process in self.processes.values():
            process.start()
        while len(self.readiness) < len(self.node_ids):
            message = self.result_queue.get(timeout=120)
            if message.get("kind") == "ERROR":
                self.close()
                raise RuntimeError(
                    f"{message.get('node_id')} startup: {message.get('error')}\n"
                    f"{message.get('traceback')}"
                )
            if message.get("kind") != "READY":
                self.close()
                raise RuntimeError("unexpected persistent-pool startup message")
            node_id = str(message["node_id"])
            expected_cpu = CPU_IDS[self.node_ids.index(node_id)]
            if message["observed_affinity"] != [expected_cpu]:
                self.close()
                raise RuntimeError("persistent worker affinity changed")
            self.readiness[node_id] = dict(message)
            self.pids[node_id] = int(message["pid"])
        self.startup_seconds = time.perf_counter() - started
        self.sample_memory()

    def sample_memory(self) -> None:
        rollups = [base.pid_rollup(pid) for pid in self.pids.values()]
        self.peak_rss = max(
            self.peak_rss, sum(row.get("Rss", 0) for row in rollups)
        )
        self.peak_pss = max(
            self.peak_pss, sum(row.get("Pss", 0) for row in rollups)
        )
        self.minimum_available = min(
            self.minimum_available, base.meminfo()["MemAvailable"]
        )
        if self.minimum_available < base.MINIMUM_AVAILABLE_MEMORY_BYTES:
            raise RuntimeError("persistent pool crossed the 8 GiB reserve")

    def run_prime(
        self,
        *,
        prime_index: int,
        prime: int,
        expected_sha256: str,
    ) -> dict[str, Any]:
        for root in range(ROOT_COUNT):
            self.task_queue.put(
                {
                    "task_index": root,
                    "prime": prime,
                    "root_start": root,
                    "root_stop": root + 1,
                }
            )
        started = time.perf_counter()
        last_sample = 0.0
        records: dict[int, dict[str, Any]] = {}
        while len(records) < ROOT_COUNT:
            try:
                message = self.result_queue.get(timeout=0.25)
            except queue.Empty:
                message = None
            now = time.monotonic()
            if now - last_sample >= 0.75:
                self.sample_memory()
                last_sample = now
            if message is None:
                if any(
                    not process.is_alive()
                    for process in self.processes.values()
                ):
                    raise RuntimeError("persistent worker exited during prime")
                continue
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')}: {message.get('error')}\n"
                    f"{message.get('traceback')}"
                )
            if message.get("kind") != "DONE":
                raise RuntimeError("unexpected persistent-pool task message")
            task_index = int(message["task_index"])
            if task_index in records:
                raise RuntimeError("duplicate persistent singleton task")
            records[task_index] = dict(message)
            if len(records) % 128 == 0:
                print(
                    json.dumps(
                        {
                            "event": "FULL_PRIME_PROGRESS",
                            "prime": f"{prime_index + 1}/3",
                            "completed": len(records),
                            "elapsed_seconds": time.perf_counter() - started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
        kernel_wall = time.perf_counter() - started
        self.sample_memory()
        ordered = [records[index] for index in range(ROOT_COUNT)]
        evaluations = [[0] * ROOT_COUNT for _ in range(16)]
        for root, row in enumerate(ordered):
            if int(row["root_start"]) != root or int(row["root_stop"]) != root + 1:
                raise RuntimeError("persistent root roster changed")
            for state in range(16):
                evaluations[state][root] = int(row["evaluations"][state][0])
        evaluation_sha256 = base.canonical_sha256(evaluations)
        if evaluation_sha256 != expected_sha256:
            raise RuntimeError("persistent full prime differs from H14E")
        structural = ordered[0]["structural_metrics"]
        if any(row["structural_metrics"] != structural for row in ordered[1:]):
            raise RuntimeError("persistent structural metrics changed")
        task_counts = {node_id: 0 for node_id in self.node_ids}
        for row in ordered:
            task_counts[str(row["node_id"])] += 1
        return base.sealed(
            {
                "schema": LANE_SCHEMA,
                "campaign_id": CAMPAIGN_ID,
                "prime_index": prime_index,
                "prime": prime,
                "profile_id": "PERSISTENT_H14_U32_P1_PACKET1_C131072",
                "singleton_root_batch_size": 1,
                "queue_packet_size": 1,
                "task_count": ROOT_COUNT,
                "worker_count": len(CPU_IDS),
                "requested_cpu_ids": CPU_IDS,
                "kernel_wall_seconds": kernel_wall,
                "roots_per_second": ROOT_COUNT / kernel_wall,
                "sum_task_wall_seconds": sum(
                    float(row["wall_seconds"]) for row in ordered
                ),
                "sum_task_cpu_seconds": sum(
                    float(row["process_cpu_seconds"]) for row in ordered
                ),
                "task_count_by_node": task_counts,
                "all_workers_active": all(
                    value > 0 for value in task_counts.values()
                ),
                "minimum_available_memory_bytes": self.minimum_available,
                "peak_aggregate_worker_rss_bytes": self.peak_rss,
                "peak_aggregate_worker_pss_bytes": self.peak_pss,
                "system_reserve_maintained": self.minimum_available
                >= base.MINIMUM_AVAILABLE_MEMORY_BYTES,
                "structural_metrics": structural,
                "evaluation_sha256": evaluation_sha256,
                "expected_h14e_evaluation_sha256": expected_sha256,
                "exact_equality_with_h14e": True,
                "evaluations": evaluations,
                "ordered_task_roster": [
                    {
                        "task_index": int(row["task_index"]),
                        "root_start": int(row["root_start"]),
                        "root_stop": int(row["root_stop"]),
                        "node_id": str(row["node_id"]),
                        "wall_seconds": float(row["wall_seconds"]),
                        "process_cpu_seconds": float(
                            row["process_cpu_seconds"]
                        ),
                        "maximum_rss_bytes": int(row["maximum_rss_bytes"]),
                        "evaluation_sha256": str(row["evaluation_sha256"]),
                    }
                    for row in ordered
                ],
            },
            "lane_sha256",
        )

    def close(self) -> None:
        for _ in self.node_ids:
            try:
                self.task_queue.put(None)
            except BaseException:
                pass
        for process in self.processes.values():
            process.join(timeout=10)
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)


def load_h14d_module() -> Any:
    module_root = str(H14D_ROOT)
    if module_root not in sys.path:
        sys.path.insert(0, module_root)
    return importlib.import_module("slcv05_h14d_runner")


def render(result: Mapping[str, Any]) -> str:
    metrics = result["metrics"]
    comparison = result["comparison"]
    return "\n".join(
        [
            f"# {DISPLAY_NAME} — {result['run_id']}",
            "",
            f"- Status: `{result['execution_status']}`",
            f"- Classification: **{result['result_classification']}**",
            "- Fresh exact tasks: **1,536/1,536**",
            "- Pool: **14 pinned physical cores retained across 3 primes**",
            "- Kernel: **uint32 residues, uint64 products, P1/C131072**",
            f"- Dense wall: **{metrics['dense_wall_seconds']:.6f} s**",
            f"- H14E/final-refinement ratio: **{comparison['h14e_over_refinement_ratio']:.6f}**",
            "- Exact operator and all 871 coefficients equal H14E: **True**",
            f"- Minimum available memory: **{metrics['minimum_available_memory_bytes'] / (1 << 30):.3f} GiB**",
            f"- Result SHA-256: `{result['result_sha256']}`",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    run_id = str(args.run_id)
    if len(run_id) != 3 or run_id[0] != "R" or not run_id[1:].isdigit():
        raise RuntimeError("run id must have form R01")
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError(f"{key} must equal 1")
    paths = run_paths(run_id)
    if any(paths[key].exists() for key in ("work", "result", "markdown")):
        raise RuntimeError(f"full confirmation {run_id} already exists")
    paths["work"].mkdir(parents=True, exist_ok=False)
    paths["lanes"].mkdir(parents=True, exist_ok=False)
    RELEASE.mkdir(parents=True, exist_ok=True)
    total_started = time.perf_counter()
    tournament = base.load_json(U32_RESULT)
    h14e = base.load_json(H14E_RESULT)
    h14d = base.load_json(H14D_RESULT)
    inherited_plan = base.load_json(H14D_PLAN)
    base.validate_seal(tournament, "result_sha256")
    base.validate_seal(h14e, "result_sha256")
    base.validate_seal(h14d, "result_sha256")
    base.validate_seal(inherited_plan, "plan_sha256")
    if (
        tournament.get("execution_status") != "COMPLETED"
        or tournament["selection"]["config_id"] != "UNROLL_C131072"
        or not tournament.get("all_checks_passed")
    ):
        raise RuntimeError("uint32 tournament authority changed")
    instance = base.load_json(base.INSTANCE_PATH)
    engine = base.load_engine(
        base.ENGINE_PATH, f"full_refinement_parent_{run_id}"
    )
    engine.validate_n72_instance(instance)
    ownership = engine.factor_ownership(instance)
    local_instance = engine._local_instance(instance, ownership)
    plan = build_plan(inherited_plan, tournament, run_id)
    manifest = source_manifest(run_id)
    descriptor = base.compile_descriptor(
        engine,
        local_instance,
        plan["conditional_order"],
        plan["port_order"],
    )
    base.atomic_json(paths["plan"], plan)
    base.atomic_json(paths["manifest"], manifest)
    dense_started = time.perf_counter()
    native_receipt = build_native(paths["native"], run_id)
    if native_receipt["library_sha256"] != tournament["selection"][
        "library_sha256"
    ]:
        raise RuntimeError("fresh selected native binary differs from tournament")
    base.atomic_json(paths["native_receipt"], native_receipt)
    temporary_root = Path(
        tempfile.mkdtemp(prefix=f"slcv05_full_{run_id}_cache_", dir="/tmp")
    )
    cache_path = temporary_root / "projection_cache.bin"
    cache_removed = False
    pool: PersistentPool | None = None
    prime_summaries = []
    modular_coefficients = []
    exact = engine._modules()[1]
    try:
        cache_build = base.build_cache_file(cache_path, descriptor)
        if base.sha256_file(cache_path) != cache_build["cache_sha256"]:
            raise RuntimeError("full refinement cache hash changed")
        os.chmod(cache_path, 0o444)
        cache = base.open_cache_file(cache_path, descriptor)
        try:
            index_validation = base.validate_cached_indices(cache)
        finally:
            cache.close()
        cache_artifact = base.sealed(
            {
                "schema": "SLCV05_N72_FINAL_REFINEMENT_CACHE_ARTIFACT_V1",
                "campaign_id": CAMPAIGN_ID,
                "run_id": run_id,
                "descriptor": descriptor,
                "build_receipt": cache_build,
                "read_only_mode": "0444",
                "index_validation": index_validation,
                "ephemeral_path_policy": "UNIQUE_TMP_REMOVED_AFTER_PERSISTENT_POOL",
            },
            "artifact_sha256",
        )
        base.atomic_json(paths["cache"], cache_artifact)
        pool = PersistentPool(
            instance=instance,
            plan=plan,
            cache_path=cache_path,
            descriptor=descriptor,
            native_library=paths["native"],
        )
        for prime_index, raw_prime in enumerate(plan["primes"]):
            prime = int(raw_prime)
            lane = pool.run_prime(
                prime_index=prime_index,
                prime=prime,
                expected_sha256=str(
                    h14e["prime_lanes"][prime_index]["evaluation_sha256"]
                ),
            )
            lane_path = paths["lanes"] / f"prime_{prime_index:02d}.json"
            base.atomic_json(lane_path, lane)
            inverse_started = time.perf_counter()
            modular_coefficients.append(
                [
                    [
                        int(value)
                        for value in exact._inverse_ntt(
                            lane["evaluations"][state], prime
                        )
                    ]
                    for state in range(16)
                ]
            )
            inverse_seconds = time.perf_counter() - inverse_started
            prime_summaries.append(
                {
                    "prime_index": prime_index,
                    "prime": prime,
                    "path": str(lane_path.relative_to(base.REPO_ROOT)),
                    "file_sha256": base.sha256_file(lane_path),
                    "lane_sha256": lane["lane_sha256"],
                    "evaluation_sha256": lane["evaluation_sha256"],
                    "kernel_wall_seconds": lane["kernel_wall_seconds"],
                    "inverse_ntt_seconds": inverse_seconds,
                    "minimum_available_memory_bytes": lane[
                        "minimum_available_memory_bytes"
                    ],
                    "peak_aggregate_worker_rss_bytes": lane[
                        "peak_aggregate_worker_rss_bytes"
                    ],
                    "peak_aggregate_worker_pss_bytes": lane[
                        "peak_aggregate_worker_pss_bytes"
                    ],
                    "all_workers_active": lane["all_workers_active"],
                    "system_reserve_maintained": lane[
                        "system_reserve_maintained"
                    ],
                }
            )
            print(
                json.dumps(
                    {
                        "event": "FULL_PRIME_COMPLETE",
                        "prime": f"{prime_index + 1}/3",
                        "kernel_wall_seconds": lane["kernel_wall_seconds"],
                        "evaluation_sha256": lane["evaluation_sha256"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        pool_startup_seconds = pool.startup_seconds
        pool.close()
        pool = None
        primes = [int(value) for value in plan["primes"]]
        local_bound = int(engine.LOCAL_BOUND)
        expected_row_sum = 1 << (int(instance["N"]) - len(plan["port_order"]))
        w_coefficients = []
        for state in range(16):
            row = [
                int(
                    exact._crt(
                        [
                            modular_coefficients[prime_index][state][degree]
                            for prime_index in range(3)
                        ],
                        primes,
                    )
                )
                for degree in range(ROOT_COUNT)
            ]
            if any(row[local_bound + 1 :]):
                raise RuntimeError("refined operator support escaped local bound")
            active = row[: local_bound + 1]
            if any(value < 0 for value in active) or sum(active) != expected_row_sum:
                raise RuntimeError("refined operator row invariant changed")
            w_coefficients.append(active)
        glue = engine.glue_y_degrees(
            ownership["cut_edges"], plan["port_order"]
        )
        first_lane = base.load_json(base.REPO_ROOT / prime_summaries[0]["path"])
        operator = {
            "schema": "SLCX032_N72_OPERATOR_V1",
            "campaign_id": CAMPAIGN_ID,
            "run_id": run_id,
            "source_validation": engine.validate_n72_instance(instance),
            "source_instance_id": instance["instance_id"],
            "source_instance_sha256": instance["instance_sha256"],
            "port_freeze_sha256": engine.load_port_freeze()["freeze_sha256"],
            "port_order": list(plan["port_order"]),
            "cut_edges": ownership["cut_edges"],
            "orientation": [list(edge) for edge in engine.CUT_ENDPOINTS],
            "factor_ownership": ownership,
            "w_coefficients": w_coefficients,
            "w_sha256": base.canonical_sha256(w_coefficients),
            "local_y_degree": local_bound,
            "expected_row_sum": expected_row_sum,
            "row_sums": [sum(row) for row in w_coefficients],
            "glue_y_degrees": glue,
            "glue_y_degrees_sha256": base.canonical_sha256(glue),
            "metrics": {
                "y_ntt_length": ROOT_COUNT,
                "selected_primes": primes,
                "root_batch_size": 1,
                "queue_packet_size": 1,
                "conditional_induced_width": plan["conditional_induced_width"],
                "cache_descriptor_sha256": descriptor["descriptor_sha256"],
                "cache_sha256": cache_build["cache_sha256"],
                **first_lane["structural_metrics"],
            },
        }
        if operator["w_sha256"] != h14e["operator_w_sha256"]:
            raise RuntimeError("refined operator differs from H14E")
        recovery = engine.recover_n72_one_cell(operator)
        if (
            recovery["fixed_coefficient_sha256"]
            != h14e["linked_fixed_coefficient_sha256"]
        ):
            raise RuntimeError("refined fixed coefficients differ from H14E")
        base.atomic_json(paths["operator"], operator)
        base.atomic_json(paths["recovery"], recovery)
        dense_wall_seconds = time.perf_counter() - dense_started
    finally:
        if pool is not None:
            pool.close()
        if cache_path.exists():
            cache_path.chmod(0o644)
            cache_path.unlink()
        if temporary_root.exists():
            shutil.rmtree(temporary_root)
        cache_removed = not cache_path.exists() and not temporary_root.exists()

    h14d_module = load_h14d_module()
    inherited_t18, w10 = h14d_module.t18_compatibility()
    open_port, routing = h14d_module.h14.fiber_engine.build_open_port_attachment(w10)
    closed = h14d_module.h14.fiber_engine.build_closed_n72_attachment(
        operator, recovery["fixed_coefficients"], routing
    )
    t18 = base.sealed(
        {
            "schema": "SLCV05_N72_FINAL_REFINEMENT_T18_RECEIPT_V1",
            "campaign_id": CAMPAIGN_ID,
            "run_id": run_id,
            "parent_campaign_id": inherited_t18["campaign_id"],
            "parent_receipt_sha256": inherited_t18["receipt_sha256"],
            "map_sha256": inherited_t18["map_sha256"],
            "assignment_count": inherited_t18["assignment_count"],
            "all_checks_passed": inherited_t18["all_checks_passed"],
            "execution_storage_changes_t18_semantics": False,
            "fresh_open_port_routing_sha256": open_port["routing_sha256"],
            "fresh_closed_joint_tensor_sha256": closed[
                "joint_tensor_sha256"
            ],
        },
        "receipt_sha256",
    )
    minimum_available = min(
        int(row["minimum_available_memory_bytes"]) for row in prime_summaries
    )
    metrics = {
        "dense_wall_seconds": dense_wall_seconds,
        "total_runner_wall_seconds": time.perf_counter() - total_started,
        "sum_prime_kernel_wall_seconds": sum(
            float(row["kernel_wall_seconds"]) for row in prime_summaries
        ),
        "sum_inverse_ntt_seconds": sum(
            float(row["inverse_ntt_seconds"]) for row in prime_summaries
        ),
        "native_build_seconds": native_receipt["build_seconds"],
        "cache_build_seconds": cache_build["build_seconds"],
        "persistent_pool_startup_seconds": pool_startup_seconds,
        "executed_task_count": 3 * ROOT_COUNT,
        "reused_task_count": 0,
        "prime_count": 3,
        "worker_count": len(CPU_IDS),
        "root_batch_size": 1,
        "queue_packet_size": 1,
        "minimum_available_memory_bytes": minimum_available,
        "peak_aggregate_worker_rss_bytes": max(
            int(row["peak_aggregate_worker_rss_bytes"])
            for row in prime_summaries
        ),
        "peak_aggregate_worker_pss_bytes": max(
            int(row["peak_aggregate_worker_pss_bytes"])
            for row in prime_summaries
        ),
        "prime_metrics": prime_summaries,
    }
    h14e_wall = float(h14e["metrics"]["wall_seconds_this_invocation"])
    comparison = {
        "h14e_dense_wall_seconds": h14e_wall,
        "refinement_dense_wall_seconds": dense_wall_seconds,
        "wall_seconds_saved": h14e_wall - dense_wall_seconds,
        "wall_reduction_percent": 100.0
        * (h14e_wall - dense_wall_seconds)
        / h14e_wall,
        "h14e_over_refinement_ratio": h14e_wall / dense_wall_seconds,
        "under_400_seconds_observed": dense_wall_seconds < 400.0,
        "runtime_is_observation": True,
    }
    checks = {
        "fresh_1536_tasks_executed": metrics["executed_task_count"] == 1536
        and metrics["reused_task_count"] == 0,
        "one_pool_retained_across_three_primes": len(prime_summaries) == 3,
        "all_prime_tensors_equal_h14e": all(
            row["evaluation_sha256"]
            == h14e["prime_lanes"][index]["evaluation_sha256"]
            for index, row in enumerate(prime_summaries)
        ),
        "all_prime_workers_active": all(
            row["all_workers_active"] for row in prime_summaries
        ),
        "all_prime_reserves_maintained": all(
            row["system_reserve_maintained"] for row in prime_summaries
        ),
        "minimum_8_gib_reserve_kept": minimum_available
        >= base.MINIMUM_AVAILABLE_MEMORY_BYTES,
        "native_binary_matches_tournament": native_receipt["library_sha256"]
        == tournament["selection"]["library_sha256"],
        "cache_indices_prevalidated": cache_artifact["index_validation"][
            "all_zero_and_one_indices_in_factor_extent"
        ],
        "ephemeral_cache_removed": cache_removed,
        "operator_equals_h14e": operator["w_sha256"]
        == h14e["operator_w_sha256"],
        "all_871_coefficients_equal_h14e": recovery[
            "fixed_coefficient_sha256"
        ]
        == h14e["linked_fixed_coefficient_sha256"],
        "configuration_count_is_2_pow_72": recovery[
            "observed_configuration_count"
        ]
        == 1 << 72,
        "t18_compatibility_retained": t18["all_checks_passed"],
        "open_port_keeps_four_q_positions": open_port[
            "all_four_q_positions_distinct"
        ],
        "closed_scalar_marginals_equal": closed[
            "all_four_scalar_marginals_equal_hot_v0_2_2"
        ],
        "runtime_is_observation": True,
    }
    if not all(checks.values()):
        failures = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"full refinement checks failed: {failures}")
    classification = "The test result suggests strong contact with the concept."
    completion = base.sealed(
        {
            "schema": "SLCV05_N72_FINAL_REFINEMENT_COMPLETION_V1",
            "campaign_id": CAMPAIGN_ID,
            "run_id": run_id,
            "execution_status": "COMPLETED",
            "result_classification": classification,
            "release_promoted": False,
            "current_revision_installed": False,
            "plan_sha256": plan["plan_sha256"],
            "manifest_sha256": manifest["manifest_sha256"],
            "native_library_sha256": native_receipt["library_sha256"],
            "cache_descriptor_sha256": descriptor["descriptor_sha256"],
            "cache_sha256": cache_build["cache_sha256"],
            "operator_w_sha256": operator["w_sha256"],
            "fixed_coefficient_sha256": recovery[
                "fixed_coefficient_sha256"
            ],
            "executed_task_count": 1536,
            "dense_wall_seconds": dense_wall_seconds,
            "checks": checks,
        },
        "completion_sha256",
    )
    base.atomic_json(paths["completion"], completion)
    result = base.sealed(
        {
            "schema": RESULT_SCHEMA,
            "campaign_id": CAMPAIGN_ID,
            "run_id": run_id,
            "display_name": DISPLAY_NAME,
            "execution_status": "COMPLETED",
            "result_classification": classification,
            "release_promoted": False,
            "current_revision_installed": False,
            "instance_id": instance["instance_id"],
            "instance_sha256": instance["instance_sha256"],
            "configuration_count": recovery["observed_configuration_count"],
            "plan": {
                "path": str(paths["plan"].relative_to(base.REPO_ROOT)),
                "plan_sha256": plan["plan_sha256"],
            },
            "source_manifest_sha256": manifest["manifest_sha256"],
            "native": native_receipt,
            "cache": {
                "artifact_path": str(paths["cache"].relative_to(base.REPO_ROOT)),
                "artifact_sha256": cache_artifact["artifact_sha256"],
                "descriptor_sha256": descriptor["descriptor_sha256"],
                "cache_sha256": cache_build["cache_sha256"],
                "cache_bytes": cache_build["cache_bytes"],
                "entry_count": descriptor["entry_count"],
                "ephemeral_cache_removed": cache_removed,
            },
            "prime_lanes": prime_summaries,
            "prime_lane_roster_sha256": base.canonical_sha256(prime_summaries),
            "operator_path": str(paths["operator"].relative_to(base.REPO_ROOT)),
            "operator_file_sha256": base.sha256_file(paths["operator"]),
            "operator_w_sha256": operator["w_sha256"],
            "recovery_path": str(paths["recovery"].relative_to(base.REPO_ROOT)),
            "recovery_file_sha256": base.sha256_file(paths["recovery"]),
            "linked_fixed_coefficient_sha256": recovery[
                "fixed_coefficient_sha256"
            ],
            "t18_compatibility": t18,
            "open_port_attachment": open_port,
            "closed_n72_attachment": closed,
            "metrics": metrics,
            "comparison": comparison,
            "checks": checks,
            "completion_path": str(
                paths["completion"].relative_to(base.REPO_ROOT)
            ),
            "completion_file_sha256": base.sha256_file(paths["completion"]),
            "completion_sha256": completion["completion_sha256"],
        },
        "result_sha256",
    )
    base.atomic_json(paths["result"], result)
    paths["markdown"].write_text(render(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "event": "FULL_N72_REFINEMENT_COMPLETE",
                "run_id": run_id,
                "dense_wall_seconds": dense_wall_seconds,
                "h14e_over_refinement_ratio": comparison[
                    "h14e_over_refinement_ratio"
                ],
                "operator_w_sha256": operator["w_sha256"],
                "fixed_coefficient_sha256": recovery[
                    "fixed_coefficient_sha256"
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
