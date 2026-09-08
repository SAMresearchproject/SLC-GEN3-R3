#!/usr/bin/env python3
"""Fresh exact N72 confirmation for the selected dynamic H14 profile."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import queue
import sys
import time
from typing import Any, Mapping, Sequence

import numpy as np


CAMPAIGN_ID = "SLCV05_N72_H14D_T18_CANDIDATE"
DISPLAY_NAME = "SLCV0.5-72-H14D-T18-CANDIDATE"
PROFILE_ID = "DYNAMIC_H14_B4_PINNED_PHYSICAL"
PRIME_RECEIPT_DOMAIN = "SLCV05-N72-H14D-T18-PRIME-COMPLETION-V1"
EXPECTED_OPERATOR_SHA256 = (
    "13f315ddb0f1a9f19e992f1209a2090b5a604704c48ab549aff98e89073cda50"
)
EXPECTED_FIXED_SHA256 = (
    "06c8e85ea8deca940be49190b91d8f5a028338a4b1add1c62256e22017f2c353"
)
EXPECTED_T18_MAP_SHA256 = (
    "5cd4e3001b11e8c1ecb828087aaab94bbace51c1129d5bacbd4218f95e7f9ab3"
)
EXPECTED_TUNING_RESULT_SHA256 = (
    "81a487ba9ebb3b27ddc8ebc853c1ae35b654e7e8f68d77879b6b3fe010054648"
)
EXPECTED_TUNING_VALIDATION_SHA256 = (
    "4a65401f6214d38bc7b90d29790f62fa63bc4f95b06fbe7c021863c4565b3380"
)
ROOT_BATCH_SIZE = 4
WORKER_COUNT = 14
MINIMUM_AVAILABLE_MEMORY_BYTES = 8 * (1 << 30)
PER_WORKER_ADDRESS_SPACE_BYTES = 6 * (1 << 30)

HERE = Path(__file__).resolve().parent
QC_ROOT = HERE.parent
REPO_ROOT = QC_ROOT.parents[1]
PARENT_ROOT = QC_ROOT / "SLCV40_N72_HYBRID_SCHEDULER_OPTIMIZATION"
V05_H14C_ROOT = QC_ROOT / "SLCV05_N72_H14C_T18_CANDIDATE"
TUNING_ROOT = QC_ROOT / "SLCV05_N72_T18_SCHEDULER_TUNING_V1"
CONTRACT = HERE / "H14D_CONTRACT.json"
WORK = HERE / "work" / "N72_H14D_T18"
RELEASE = HERE / "release"
PLAN_PATH = WORK / "EXECUTION_PLAN.json"
MANIFEST_PATH = WORK / "SOURCE_MANIFEST.json"
T18_PATH = WORK / "T18_COMPATIBILITY.json"
HEARTBEAT = WORK / "HEARTBEAT.json"
COMPLETION = WORK / "CANDIDATE_COMPLETION.json"
OPERATOR_PATH = WORK / "LINKED_OPERATOR.json"
RESULT_JSON = RELEASE / "SLCV0.5-72-H14D-T18_CANDIDATE_RESULT.json"
RESULT_MD = RELEASE / "SLCV0.5-72-H14D-T18_CANDIDATE_RESULT.md"
H14C_RESULT = (
    V05_H14C_ROOT
    / "release"
    / "SLCV0.5-72-H14C-T18_CANDIDATE_RESULT.json"
)
TUNING_RESULT = TUNING_ROOT / "SCHEDULER_TUNING_RESULT.json"
TUNING_VALIDATION = TUNING_ROOT / "INDEPENDENT_VALIDATION.json"

for module_root in (HERE, PARENT_ROOT, V05_H14C_ROOT):
    module_text = str(module_root)
    if module_text not in sys.path:
        sys.path.insert(0, module_text)

import slcv40_hybrid_full_runner as h14  # noqa: E402
import slcv05_h14d_worker as dynamic_worker  # noqa: E402
from slcv05_ir import (  # noqa: E402
    ASSIGNMENT_COUNT,
    build_t18_transition_maps,
    run_ir_self_checks,
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


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


def validate_seal(value: Mapping[str, Any], key: str) -> None:
    unsigned = dict(value)
    observed = unsigned.pop(key, None)
    if observed != canonical_sha256(unsigned):
        raise RuntimeError(f"self-seal mismatch for {key}")


def sealed(unsigned: Mapping[str, Any], key: str) -> dict[str, Any]:
    return {**unsigned, key: canonical_sha256(unsigned)}


def balanced_tree(
    leaves: Sequence[str],
    *,
    plan_sha256: str,
    instance_sha256: str,
    prime_index: int,
) -> tuple[list[list[str]], str]:
    current = list(leaves)
    if not current or len(current) & (len(current) - 1):
        raise RuntimeError("H14D receipt requires a power-of-two roster")
    levels = []
    depth = 0
    while len(current) > 1:
        following = [
            canonical_sha256(
                {
                    "domain": PRIME_RECEIPT_DOMAIN,
                    "campaign_id": CAMPAIGN_ID,
                    "plan_sha256": plan_sha256,
                    "instance_sha256": instance_sha256,
                    "prime_index": prime_index,
                    "depth": depth,
                    "pair_index": index // 2,
                    "left": current[index],
                    "right": current[index + 1],
                }
            )
            for index in range(0, len(current), 2)
        ]
        levels.append(following)
        current = following
        depth += 1
    return levels, current[0]


def prime_receipt(
    *,
    plan: Mapping[str, Any],
    instance: Mapping[str, Any],
    prime_index: int,
    prime: int,
    ordered: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    leaves = [str(row["record_sha256"]) for row in ordered]
    levels, root = balanced_tree(
        leaves,
        plan_sha256=str(plan["plan_sha256"]),
        instance_sha256=str(instance["instance_sha256"]),
        prime_index=prime_index,
    )
    unsigned = {
        "schema": "SLCV05_N72_H14D_T18_PRIME_COMPLETION_RECEIPT_V1",
        "domain": PRIME_RECEIPT_DOMAIN,
        "campaign_id": CAMPAIGN_ID,
        "profile_id": PROFILE_ID,
        "plan_sha256": plan["plan_sha256"],
        "instance_sha256": instance["instance_sha256"],
        "prime_index": prime_index,
        "prime": prime,
        "root_batch_size": ROOT_BATCH_SIZE,
        "root_count": 512,
        "task_count": len(ordered),
        "ordered_task_roster": [
            {
                "task_index": int(row["task_index"]),
                "root_start": int(row["root_start"]),
                "root_stop": int(row["root_stop"]),
                "node_id": row["node_id"],
                "scheduler_phase": row["scheduler_phase"],
                "record_sha256": row["record_sha256"],
            }
            for row in ordered
        ],
        "ordered_leaf_sha256": leaves,
        "balanced_levels": levels,
        "balanced_root_sha256": root,
    }
    return sealed(unsigned, "receipt_sha256")


def build_plan(
    engine: Any,
    instance: Mapping[str, Any],
    batch: Mapping[str, Any],
    scheduler: Mapping[str, Any],
    cpu_ids: list[int],
) -> dict[str, Any]:
    inherited = h14.build_plan(engine, instance, batch, scheduler, cpu_ids)
    unsigned = dict(inherited)
    unsigned.pop("plan_sha256")
    unsigned.update(
        {
            "schema": "SLCV05_N72_H14D_T18_EXECUTION_PLAN_V1",
            "campaign_id": CAMPAIGN_ID,
            "display_name": DISPLAY_NAME,
            "version_label": "SLCV0.5-CANDIDATE-H14D",
            "scheduler_profile_id": PROFILE_ID,
            "scheduler_dispatch": "SHARED_DYNAMIC_QUEUE",
            "worker_topology": "PINNED_H14_PHYSICAL_CORES",
            "calibration_tasks_per_prime": 0,
            "weighted_tasks_per_prime": 0,
            "dynamic_tasks_per_prime": 128,
            "total_calibration_task_count": 0,
            "total_weighted_task_count": 0,
            "total_dynamic_task_count": 384,
            "active_changes": [
                value
                for value in inherited["active_changes"]
                if value
                not in (
                    "PER_PRIME_NODE_CALIBRATION",
                    "INVERSE_CALIBRATION_WEIGHTED_STATIC_QUEUES",
                    "ACTIVE_FULL_Q_512_BY_512",
                )
            ]
            + [
                "SHARED_DYNAMIC_ROOT_BATCH_QUEUE",
                "TYPED_THETA18_OVER_ACTIVE_Z4_9",
            ],
            "tuning_authority": {
                "result_sha256": EXPECTED_TUNING_RESULT_SHA256,
                "validation_sha256": EXPECTED_TUNING_VALIDATION_SHA256,
                "selected_profile_id": PROFILE_ID,
            },
            "fiber_contract": {
                "public_name_component": "T18",
                "theta_arity": 18,
                "packet_count": 2,
                "theta_coordinates_per_packet": 9,
                "q_coordinate_count": 9,
                "coordinate_group": "Z4",
                "assignment_count": ASSIGNMENT_COUNT,
                "computational_factor_dimensions": [512, 512],
                "legacy_encoding": "ACTIVE_512_BY_512_Z4_9",
            },
        }
    )
    return sealed(unsigned, "plan_sha256")


def source_manifest() -> dict[str, Any]:
    paths = [
        HERE / "README.md",
        CONTRACT,
        HERE / "slcv05_h14d_worker.py",
        Path(__file__).resolve(),
        HERE / "validate_slcv05_h14d.py",
        TUNING_RESULT,
        TUNING_VALIDATION,
        V05_H14C_ROOT / "slcv05_ir.py",
        H14C_RESULT,
        PARENT_ROOT / "slcv40_hybrid_full_runner.py",
        PARENT_ROOT / "slcv40_hybrid_worker.py",
        h14.BATCH_RESULT,
        h14.SCHEDULER_RESULT,
        h14.ENGINE_PATH,
        h14.V31_ROOT / "slcv0031_w10.py",
        h14.V4_DEV_ROOT / "slcv004_fiber_probe.py",
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
            "schema": "SLCV05_N72_H14D_T18_SOURCE_MANIFEST_V1",
            "campaign_id": CAMPAIGN_ID,
            "display_name": DISPLAY_NAME,
            "sources": rows,
        },
        "manifest_sha256",
    )


def t18_compatibility() -> tuple[dict[str, Any], Any]:
    checks = dict(run_ir_self_checks())
    typed_maps, typed = build_t18_transition_maps()
    w10, _ = h14.fiber_engine.load_modules()
    legacy, legacy_maps = h14.fiber_engine.exercise_full_fiber(w10)
    checks.update(
        {
            "typed_map_hash_expected": typed["map_sha256"]
            == EXPECTED_T18_MAP_SHA256,
            "legacy_map_hash_expected": legacy["map_sha256"]
            == EXPECTED_T18_MAP_SHA256,
            "typed_maps_equal_legacy": np.array_equal(typed_maps, legacy_maps),
            "all_addresses_executed": typed["assignment_count"]
            == ASSIGNMENT_COUNT,
        }
    )
    if not all(checks.values()):
        raise RuntimeError("H14D T18 compatibility failed")
    receipt = sealed(
        {
            **typed,
            "campaign_id": CAMPAIGN_ID,
            "legacy_w10_receipt": legacy,
            "checks": checks,
            "all_checks_passed": True,
        },
        "receipt_sha256",
    )
    return receipt, w10


def write_heartbeat(payload: Mapping[str, Any]) -> None:
    unsigned = {
        "schema": "SLCV05_N72_H14D_T18_HEARTBEAT_V1",
        "campaign_id": CAMPAIGN_ID,
        "updated_unix": time.time(),
        **dict(payload),
    }
    atomic_json(HEARTBEAT, sealed(unsigned, "heartbeat_sha256"))


def execute_dynamic(
    engine: Any,
    instance: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    memory_before = h14.meminfo()
    if memory_before["MemAvailable"] < MINIMUM_AVAILABLE_MEMORY_BYTES:
        raise RuntimeError("8 GiB memory reserve unavailable")
    node_ids = [str(value) for value in plan["node_ids"]]
    cpu_ids = [int(value) for value in plan["requested_cpu_ids"]]
    cpu_by_node = dict(zip(node_ids, cpu_ids))
    context = mp.get_context("spawn")
    result_queue = context.Queue()
    task_queue = context.Queue()
    checkpoint_roots = {
        node_id: WORK / node_id / "checkpoints" for node_id in node_ids
    }
    for path in checkpoint_roots.values():
        path.mkdir(parents=True, exist_ok=True)
    processes = {
        node_id: context.Process(
            target=dynamic_worker.node_loop,
            args=(
                node_id,
                cpu_by_node[node_id],
                instance,
                plan,
                task_queue,
                result_queue,
                str(checkpoint_roots[node_id]),
                str(h14.ENGINE_PATH),
                PER_WORKER_ADDRESS_SPACE_BYTES,
            ),
            name=f"SLCV05-H14D-{node_id}",
        )
        for node_id in node_ids
    }
    started = time.perf_counter()
    for process in processes.values():
        process.start()
    pids = {}
    readiness = {}
    worker_peaks = {node_id: 0 for node_id in node_ids}
    worker_wall = {node_id: 0.0 for node_id in node_ids}
    worker_cpu = 0.0
    peak_aggregate_rss = 0
    minimum_available = memory_before["MemAvailable"]
    maximum_active_nodes = 0
    executed_tasks = 0
    checkpoint_roster = []
    prime_receipt_roster = []
    prime_metrics = []
    modular_coefficients = []
    structural_metrics: dict[str, int] = {}
    last_heartbeat = 0.0

    def sample_resources() -> None:
        nonlocal peak_aggregate_rss, minimum_available, maximum_active_nodes
        rss = {node_id: h14.pid_rss_bytes(pid) for node_id, pid in pids.items()}
        peak_aggregate_rss = max(peak_aggregate_rss, sum(rss.values()))
        maximum_active_nodes = max(
            maximum_active_nodes, sum(value > 0 for value in rss.values())
        )
        available = h14.meminfo()["MemAvailable"]
        minimum_available = min(minimum_available, available)
        if available < MINIMUM_AVAILABLE_MEMORY_BYTES:
            raise RuntimeError("H14D crossed the 8 GiB memory reserve")

    try:
        while len(pids) < len(node_ids):
            message = result_queue.get(timeout=120)
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')} startup error: "
                    f"{message.get('error')}\n{message.get('traceback')}"
                )
            if message.get("kind") != "READY":
                raise RuntimeError("unexpected H14D startup message")
            node_id = str(message["node_id"])
            if message["observed_affinity"] != [cpu_by_node[node_id]]:
                raise RuntimeError("H14D worker affinity changed")
            pids[node_id] = int(message["worker_pid"])
            readiness[node_id] = dict(message)
            worker_peaks[node_id] = int(message["maximum_rss_bytes"])
        startup_seconds = time.perf_counter() - started
        sample_resources()

        for prime_index, raw_prime in enumerate(plan["primes"]):
            prime = int(raw_prime)
            records: dict[int, dict[str, Any]] = {}
            tasks = {}
            for task_index, root_start in enumerate(range(0, 512, 4)):
                task_id = f"p{prime_index:02d}t{task_index:03d}"
                task = {
                    "task_id": task_id,
                    "prime_index": prime_index,
                    "prime": prime,
                    "task_index": task_index,
                    "root_start": root_start,
                    "root_stop": root_start + 4,
                    "checkpoint_name": (
                        f"prime_{prime_index:02d}_task_{task_index:03d}_"
                        f"roots_{root_start:04d}_{root_start + 4:04d}.json"
                    ),
                }
                tasks[task_id] = task
                task_queue.put(task)
            pending = set(tasks)
            prime_started = time.perf_counter()
            while pending:
                try:
                    message = result_queue.get(timeout=0.25)
                except queue.Empty:
                    sample_resources()
                    now = time.monotonic()
                    if now - last_heartbeat >= 15:
                        last_heartbeat = now
                        write_heartbeat(
                            {
                                "prime_index": prime_index,
                                "pending_task_count": len(pending),
                                "executed_task_count": executed_tasks,
                                "peak_aggregate_worker_rss_bytes": peak_aggregate_rss,
                                "minimum_available_memory_bytes": minimum_available,
                            }
                        )
                        print(
                            json.dumps(
                                {
                                    "prime": f"{prime_index + 1}/3",
                                    "pending": len(pending),
                                    "executed": executed_tasks,
                                    "peak_gib": round(
                                        peak_aggregate_rss / (1 << 30), 3
                                    ),
                                    "min_available_gib": round(
                                        minimum_available / (1 << 30), 3
                                    ),
                                },
                                sort_keys=True,
                            ),
                            flush=True,
                        )
                    if any(not process.is_alive() for process in processes.values()):
                        raise RuntimeError("H14D worker exited during execution")
                    continue
                if message.get("kind") == "ERROR":
                    raise RuntimeError(
                        f"{message.get('node_id')} error: {message.get('error')}\n"
                        f"{message.get('traceback')}"
                    )
                if message.get("kind") != "DONE":
                    raise RuntimeError("unexpected H14D worker message")
                task_id = str(message["task_id"])
                if task_id not in pending:
                    raise RuntimeError("duplicate H14D completion")
                task = tasks[task_id]
                node_id = str(message["node_id"])
                path = Path(str(message["checkpoint_path"]))
                relative = path.resolve().relative_to(WORK.resolve())
                checkpoint = load_json(path)
                dynamic_worker.validate_checkpoint(
                    checkpoint,
                    {
                        "domain": dynamic_worker.CHECKPOINT_DOMAIN,
                        "campaign_id": CAMPAIGN_ID,
                        "plan_sha256": plan["plan_sha256"],
                        "instance_sha256": instance["instance_sha256"],
                        "node_id": node_id,
                        "requested_cpu_id": cpu_by_node[node_id],
                        "observed_affinity": [cpu_by_node[node_id]],
                        "task_id": task_id,
                        "prime_index": prime_index,
                        "prime": prime,
                        "scheduler_phase": "DYNAMIC_SHARED_QUEUE",
                        "task_index": task["task_index"],
                        "root_start": task["root_start"],
                        "root_stop": task["root_stop"],
                    },
                )
                task_index = int(task["task_index"])
                records[task_index] = checkpoint
                pending.remove(task_id)
                executed_tasks += 1
                worker_cpu += float(message["process_cpu_seconds"])
                worker_wall[node_id] += float(message["wall_seconds"])
                worker_peaks[node_id] = max(
                    worker_peaks[node_id], int(message["maximum_rss_bytes"])
                )
                checkpoint_roster.append(
                    {
                        "path": str(relative),
                        "node_id": node_id,
                        "requested_cpu_id": cpu_by_node[node_id],
                        "prime_index": prime_index,
                        "scheduler_phase": "DYNAMIC_SHARED_QUEUE",
                        "task_index": task_index,
                        "root_start": task["root_start"],
                        "root_stop": task["root_stop"],
                        "record_sha256": checkpoint["record_sha256"],
                    }
                )
                for key, value in checkpoint["structural_metrics"].items():
                    if key.startswith("sum_"):
                        if key in structural_metrics and structural_metrics[key] != int(value):
                            raise RuntimeError("H14D structural metric changed")
                        structural_metrics[key] = int(value)
                    else:
                        structural_metrics[key] = max(
                            structural_metrics.get(key, 0), int(value)
                        )
                sample_resources()

            ordered = [records[index] for index in range(128)]
            prime_kernel_seconds = time.perf_counter() - prime_started
            evaluations = np.zeros((16, 512), dtype=np.int64)
            for checkpoint in ordered:
                start = int(checkpoint["root_start"])
                stop = int(checkpoint["root_stop"])
                evaluations[:, start:stop] = np.asarray(
                    checkpoint["evaluations"], dtype=np.int64
                )
            receipt = prime_receipt(
                plan=plan,
                instance=instance,
                prime_index=prime_index,
                prime=prime,
                ordered=ordered,
            )
            receipt_path = WORK / "prime_receipts" / f"prime_{prime_index:02d}.json"
            atomic_json(receipt_path, receipt)
            prime_receipt_roster.append(
                {
                    "path": str(receipt_path.relative_to(WORK)),
                    "prime_index": prime_index,
                    "prime": prime,
                    "receipt_sha256": receipt["receipt_sha256"],
                    "balanced_root_sha256": receipt["balanced_root_sha256"],
                }
            )
            exact = engine._modules()[1]
            inverse_started = time.perf_counter()
            modular_coefficients.append(
                [
                    [int(value) for value in exact._inverse_ntt(evaluations[state].tolist(), prime)]
                    for state in range(16)
                ]
            )
            inverse_seconds = time.perf_counter() - inverse_started
            task_count_by_node: dict[str, int] = defaultdict(int)
            task_wall_by_node: dict[str, float] = defaultdict(float)
            for checkpoint in ordered:
                node_id = str(checkpoint["node_id"])
                task_count_by_node[node_id] += 1
                task_wall_by_node[node_id] += float(checkpoint["wall_seconds"])
            prime_metrics.append(
                {
                    "prime_index": prime_index,
                    "prime": prime,
                    "kernel_wall_seconds": prime_kernel_seconds,
                    "inverse_ntt_seconds": inverse_seconds,
                    "task_count_by_node": dict(sorted(task_count_by_node.items())),
                    "task_wall_seconds_by_node": dict(sorted(task_wall_by_node.items())),
                    "sum_task_wall_seconds": sum(task_wall_by_node.values()),
                }
            )
            print(
                json.dumps(
                    {
                        "event": "PRIME_COMPLETE",
                        "prime": f"{prime_index + 1}/3",
                        "kernel_wall_seconds": prime_kernel_seconds,
                        "task_count_by_node": dict(sorted(task_count_by_node.items())),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    finally:
        for _ in node_ids:
            try:
                task_queue.put(None)
            except Exception:
                pass
        for process in processes.values():
            process.join(timeout=10)
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)

    exact = engine._modules()[1]
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
            for degree in range(512)
        ]
        if any(row[local_bound + 1 :]):
            raise RuntimeError("H14D operator support escaped local bound")
        active = row[: local_bound + 1]
        if any(value < 0 for value in active) or sum(active) != expected_row_sum:
            raise RuntimeError("H14D operator row invariant changed")
        w_coefficients.append(active)
    ownership = engine.factor_ownership(instance)
    glue = engine.glue_y_degrees(ownership["cut_edges"], plan["port_order"])
    operator = {
        "schema": "SLCX032_N72_OPERATOR_V1",
        "campaign_id": CAMPAIGN_ID,
        "source_validation": engine.validate_n72_instance(instance),
        "source_instance_id": instance["instance_id"],
        "source_instance_sha256": instance["instance_sha256"],
        "port_freeze_sha256": engine.load_port_freeze()["freeze_sha256"],
        "port_order": list(plan["port_order"]),
        "cut_edges": ownership["cut_edges"],
        "orientation": [list(edge) for edge in engine.CUT_ENDPOINTS],
        "factor_ownership": ownership,
        "w_coefficients": w_coefficients,
        "w_sha256": canonical_sha256(w_coefficients),
        "local_y_degree": local_bound,
        "expected_row_sum": expected_row_sum,
        "row_sums": [sum(row) for row in w_coefficients],
        "glue_y_degrees": glue,
        "glue_y_degrees_sha256": canonical_sha256(glue),
        "metrics": {
            "elapsed_seconds": time.perf_counter() - started,
            "y_ntt_length": 512,
            "selected_primes": primes,
            "root_batch_size": 4,
            "conditional_induced_width": plan["conditional_induced_width"],
            **structural_metrics,
        },
    }
    if operator["w_sha256"] != EXPECTED_OPERATOR_SHA256:
        raise RuntimeError("H14D operator differs from parent")
    recovery = engine.recover_n72_one_cell(operator)
    if recovery["fixed_coefficient_sha256"] != EXPECTED_FIXED_SHA256:
        raise RuntimeError("H14D scalar result differs from parent")
    checkpoint_roster.sort(
        key=lambda row: (int(row["prime_index"]), int(row["task_index"]))
    )
    memory_after = h14.meminfo()
    task_count_by_node: dict[str, int] = defaultdict(int)
    for row in checkpoint_roster:
        task_count_by_node[str(row["node_id"])] += 1
    return {
        "operator": operator,
        "recovery": recovery,
        "checkpoint_roster": checkpoint_roster,
        "checkpoint_roster_sha256": canonical_sha256(checkpoint_roster),
        "prime_receipt_roster": prime_receipt_roster,
        "prime_receipt_roster_sha256": canonical_sha256(prime_receipt_roster),
        "metrics": {
            "wall_seconds_this_invocation": time.perf_counter() - started,
            "startup_seconds": startup_seconds,
            "sum_prime_kernel_wall_seconds": sum(
                row["kernel_wall_seconds"] for row in prime_metrics
            ),
            "sum_worker_cpu_seconds": worker_cpu,
            "worker_wall_seconds_by_node": worker_wall,
            "task_count_by_node": dict(sorted(task_count_by_node.items())),
            "executed_task_count": executed_tasks,
            "reused_task_count": 0,
            "total_task_count": len(checkpoint_roster),
            "prime_completion_receipt_count": len(prime_receipt_roster),
            "worker_pids": pids,
            "worker_readiness": readiness,
            "worker_peak_rss_bytes_by_node": worker_peaks,
            "peak_sampled_aggregate_worker_rss_bytes": peak_aggregate_rss,
            "maximum_active_nodes": maximum_active_nodes,
            "available_memory_before_bytes": memory_before["MemAvailable"],
            "minimum_available_memory_bytes": minimum_available,
            "available_memory_after_bytes": memory_after["MemAvailable"],
            "prime_metrics": prime_metrics,
        },
    }


def ensure_fresh() -> None:
    occupied = [path for path in (WORK, RELEASE) if path.exists()]
    if occupied:
        raise RuntimeError("H14D campaign artifacts already exist")


def render(result: Mapping[str, Any]) -> str:
    metrics = result["metrics"]
    comparison = result["comparison"]
    return "\n".join(
        [
            f"# {DISPLAY_NAME} exact N72 result",
            "",
            f"**Status:** `{result['execution_status']}`  ",
            f"**Classification:** {result['result_classification']}",
            "",
            f"- Fresh tasks: **{metrics['executed_task_count']}/384**",
            "- Scheduler: **dynamic queue on 14 pinned physical cores**",
            f"- Dense wall: **{metrics['wall_seconds_this_invocation']:.6f} s**",
            (
                "- Change versus first v0.5 H14C candidate: "
                f"**{comparison['h14d_minus_h14c_seconds']:+.6f} s**"
            ),
            (
                "- Change versus frozen v0.4 H14C observation: "
                f"**{comparison['h14d_minus_v04_h14c_seconds']:+.6f} s**"
            ),
            "- Exact 871-coefficient equality: **True**",
            "- T18/legacy W10 map equality: **True**",
            "",
            "`H14D` is a provisional candidate profile label, not release promotion.",
            "",
            f"**Result SHA-256:** `{result['result_sha256']}`",
            "",
        ]
    )


def main() -> int:
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError(f"{key} must equal 1")
    ensure_fresh()
    h14.frozen_v4.check_locked_sources()
    batch, scheduler = h14.load_probe_results()
    tuning = load_json(TUNING_RESULT)
    tuning_validation = load_json(TUNING_VALIDATION)
    h14c = load_json(H14C_RESULT)
    validate_seal(tuning, "result_sha256")
    validate_seal(tuning_validation, "validation_sha256")
    validate_seal(h14c, "result_sha256")
    if (
        tuning["result_sha256"] != EXPECTED_TUNING_RESULT_SHA256
        or tuning_validation["validation_sha256"]
        != EXPECTED_TUNING_VALIDATION_SHA256
        or tuning["selected_profile_id"] != PROFILE_ID
    ):
        raise RuntimeError("H14D tuning authority changed")
    engine, instance, _, _, _, _ = h14.hot_runner.load_inputs()
    cpu_ids = h14.physical_cpu_ids()
    plan = build_plan(engine, instance, batch, scheduler, cpu_ids)
    manifest = source_manifest()
    t18, w10 = t18_compatibility()
    WORK.mkdir(parents=True, exist_ok=False)
    RELEASE.mkdir(parents=True, exist_ok=False)
    atomic_json(PLAN_PATH, plan)
    atomic_json(MANIFEST_PATH, manifest)
    atomic_json(T18_PATH, t18)
    total_started = time.perf_counter()
    cluster = execute_dynamic(engine, instance, plan)
    atomic_json(OPERATOR_PATH, cluster["operator"])
    fixed = [int(value) for value in cluster["recovery"]["fixed_coefficients"]]
    open_port, routing = h14.fiber_engine.build_open_port_attachment(w10)
    closed = h14.fiber_engine.build_closed_n72_attachment(
        cluster["operator"], fixed, routing
    )
    metrics = cluster["metrics"]
    wall = float(metrics["wall_seconds_this_invocation"])
    h14c_wall = float(h14c["metrics"]["wall_seconds_this_invocation"])
    v04_wall = float(h14c["comparison"]["parent_wall_seconds"])
    comparison = {
        "h14c_v05_seconds": h14c_wall,
        "v04_h14c_seconds": v04_wall,
        "h14d_seconds": wall,
        "h14d_minus_h14c_seconds": wall - h14c_wall,
        "h14c_over_h14d_speed_ratio": h14c_wall / wall,
        "h14d_minus_v04_h14c_seconds": wall - v04_wall,
        "v04_h14c_over_h14d_speed_ratio": v04_wall / wall,
        "under_400_seconds_observed": wall < 400.0,
        "runtime_is_observation": True,
    }
    checks = {
        "fresh_384_tasks_executed": metrics["executed_task_count"] == 384
        and metrics["reused_task_count"] == 0,
        "three_prime_receipts_written": metrics[
            "prime_completion_receipt_count"
        ]
        == 3,
        "all_fourteen_workers_pinned": all(
            metrics["worker_readiness"][node_id]["observed_affinity"]
            == [cpu_id]
            for node_id, cpu_id in zip(plan["node_ids"], cpu_ids)
        ),
        "all_fourteen_workers_active": metrics["maximum_active_nodes"] == 14,
        "dynamic_profile_matches_tuning_winner": plan[
            "scheduler_profile_id"
        ]
        == PROFILE_ID,
        "operator_equals_parent": cluster["operator"]["w_sha256"]
        == EXPECTED_OPERATOR_SHA256,
        "all_871_coefficients_equal_parent": cluster["recovery"][
            "fixed_coefficient_sha256"
        ]
        == EXPECTED_FIXED_SHA256,
        "configuration_count_is_2_pow_72": cluster["recovery"][
            "observed_configuration_count"
        ]
        == 1 << 72,
        "t18_compatibility_passed": t18["all_checks_passed"],
        "open_port_keeps_four_q_positions": open_port[
            "all_four_q_positions_distinct"
        ],
        "closed_scalar_marginals_equal": closed[
            "all_four_scalar_marginals_equal_hot_v0_2_2"
        ],
        "minimum_8_gib_reserve_kept": metrics[
            "minimum_available_memory_bytes"
        ]
        >= MINIMUM_AVAILABLE_MEMORY_BYTES,
        "dynamic_h14_improves_first_v05_full_run": wall < h14c_wall,
    }
    if not all(checks.values()):
        raise RuntimeError("H14D full N72 confirmation failed")
    classification = "The test result suggests strong contact with the concept."
    completion_unsigned = {
        "schema": "SLCV05_N72_H14D_T18_COMPLETION_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "execution_status": "COMPLETED",
        "result_classification": classification,
        "release_promoted": False,
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "N": 72,
        "plan": plan,
        "source_manifest": manifest,
        "operator_w_sha256": cluster["operator"]["w_sha256"],
        "linked_fixed_coefficient_sha256": cluster["recovery"][
            "fixed_coefficient_sha256"
        ],
        "configuration_count": str(
            cluster["recovery"]["observed_configuration_count"]
        ),
        "dos": cluster["recovery"]["dos_rows"],
        "dos_sha256": cluster["recovery"]["dos_sha256"],
        "t18_compatibility": t18,
        "open_port_attachment": open_port,
        "closed_n72_attachment": closed,
        "checkpoint_roster": cluster["checkpoint_roster"],
        "checkpoint_roster_sha256": cluster["checkpoint_roster_sha256"],
        "prime_receipt_roster": cluster["prime_receipt_roster"],
        "prime_receipt_roster_sha256": cluster[
            "prime_receipt_roster_sha256"
        ],
        "metrics": metrics,
        "comparison": comparison,
        "checks": checks,
        "total_runner_wall_seconds": time.perf_counter() - total_started,
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "platform": platform.platform(),
            "allowed_cpu_ids": sorted(os.sched_getaffinity(0)),
        },
    }
    completion = sealed(completion_unsigned, "completion_sha256")
    atomic_json(COMPLETION, completion)
    result_unsigned = {
        "schema": "SLCV05_N72_H14D_T18_RESULT_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "execution_status": "COMPLETED",
        "result_classification": classification,
        "release_promoted": False,
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "configuration_count": completion["configuration_count"],
        "operator_w_sha256": completion["operator_w_sha256"],
        "linked_fixed_coefficient_sha256": completion[
            "linked_fixed_coefficient_sha256"
        ],
        "plan": plan,
        "t18_compatibility": t18,
        "open_port_attachment": open_port,
        "closed_n72_attachment": closed,
        "metrics": metrics,
        "comparison": comparison,
        "checks": checks,
        "completion_path": str(COMPLETION.relative_to(REPO_ROOT)),
        "completion_file_sha256": sha256_file(COMPLETION),
        "completion_sha256": completion["completion_sha256"],
        "source_manifest_sha256": manifest["manifest_sha256"],
        "operator_path": str(OPERATOR_PATH.relative_to(REPO_ROOT)),
        "operator_file_sha256": sha256_file(OPERATOR_PATH),
        "total_runner_wall_seconds": completion["total_runner_wall_seconds"],
    }
    result = sealed(result_unsigned, "result_sha256")
    atomic_json(RESULT_JSON, result)
    RESULT_MD.write_text(render(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "COMPLETED",
                "wall_seconds": wall,
                "h14d_minus_h14c_seconds": wall - h14c_wall,
                "h14d_minus_v04_seconds": wall - v04_wall,
                "under_400_seconds": wall < 400,
                "result_sha256": result["result_sha256"],
            },
            indent=2,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
