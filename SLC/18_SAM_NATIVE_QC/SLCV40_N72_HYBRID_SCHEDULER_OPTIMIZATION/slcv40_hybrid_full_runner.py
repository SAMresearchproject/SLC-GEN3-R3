#!/usr/bin/env python3
"""Run fresh exact N72 with the calibrated pinned H14 scheduler."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import queue
import sys
import time
from typing import Any, Mapping, Sequence

import numpy as np


CAMPAIGN_ID = "SLCV40_N72_HYBRID_SCHEDULER_OPTIMIZATION"
DISPLAY_NAME = "SLCV4.0-24-H14C-512"
VERSION_LABEL = "SLCV4.0-24-H14C-512"
PROFILE_ID = "CALIBRATED_F14_PINNED_PHYSICAL_CORES"
PRIME_RECEIPT_DOMAIN = "SLCV40-H14C-PRIME-COMPLETION-V1"
ROOT_BATCH_SIZE = 4
WORKER_COUNT = 14
MINIMUM_AVAILABLE_MEMORY_BYTES = 8 * (1 << 30)
PER_WORKER_ADDRESS_SPACE_BYTES = 6 * (1 << 30)

EXPECTED_BATCH_RESULT_SHA256 = (
    "0a59fb51b32f1d11e9738fb2b267dfda67abdf97bfaf85dd69590924ca0ca45c"
)
EXPECTED_SCHEDULER_RESULT_SHA256 = (
    "ba66ed9ad56d8d1e566f97ee6110831d810faff353ccc9cd84910d5b18b02ed7"
)
EXPECTED_FROZEN_RESULT_SHA256 = (
    "a64fdfb7e264a06a7c5f599b4b2892a0bdf5d410af6e8946dfbd44fcd0c606f3"
)
EXPECTED_SMART_RESULT_SHA256 = (
    "914a29ea6791af2482933921b3c5620b3c91694fe528c57f34d529d0b9995fd9"
)

HERE = Path(__file__).resolve().parent
QC_ROOT = HERE.parent
V4_ROOT = QC_ROOT / "SLCV40_24_F16_512_EXACT_N72"
SMART_ROOT = QC_ROOT / "SLCV40_SMART_CONFIG_EXACT_N72"
V22_ROOT = QC_ROOT / "SLCV0022C16N72_LINKED_SUPERCELL_EXACT_N72"
V21_ROOT = QC_ROOT / "SLCV0021C4N72_LINKED_SUPERCELL_EXACT_N72"
V4_DEV_ROOT = QC_ROOT / "SLCV004C16N72_LINKED_ACTIVE_512_FIBER"
V31_ROOT = QC_ROOT / "SLCV0031_DENSE_EXACT_FULL_Q_STAGE4_N72"

CONTRACT = HERE / "SLCV40_HYBRID_OPTIMIZATION_CONTRACT.json"
BATCH_RESULT = (
    HERE
    / "work"
    / "BATCH_FINE_PROBE"
    / "SLCV40_BATCH_FINE_RESULT.json"
)
SCHEDULER_RESULT = (
    HERE
    / "work"
    / "SCHEDULER_PRIME_PROBE"
    / "SLCV40_SCHEDULER_PRIME_RESULT.json"
)
FROZEN_RESULT = (
    V4_ROOT
    / "release"
    / "SLCV4.0-24-F16-512_RESULT.json"
)
SMART_RESULT = (
    SMART_ROOT / "release" / "SLCV40_SMART_N72_RESULT.json"
)
WORK = HERE / "work" / "N72_H14C"
RELEASE = HERE / "release"
HEARTBEAT = WORK / "HEARTBEAT.json"
COMPLETION = WORK / "CANDIDATE_COMPLETION.json"
OPERATOR_RESULT = WORK / "LINKED_OPERATOR.json"
RESULT_JSON = RELEASE / "SLCV40_24_H14C_512_N72_RESULT.json"
RESULT_MD = RELEASE / "SLCV40_24_H14C_512_N72_RESULT.md"
ENGINE_PATH = (
    QC_ROOT
    / "SLCX032_EXACT_N72_SUPERCELL_N144_DAISY_CHAIN_DISCOVERY"
    / "slcx032_engine.py"
)

for module_root in (
    HERE,
    V4_ROOT,
    V22_ROOT,
    V21_ROOT,
    V4_DEV_ROOT,
    V31_ROOT,
):
    module_text = str(module_root)
    if module_text not in sys.path:
        sys.path.insert(0, module_text)

import slcv40_hybrid_worker as worker  # noqa: E402
import slcv40_runner as frozen_v4  # noqa: E402


hot_runner = frozen_v4.hot_runner
fiber_engine = frozen_v4.fiber_engine


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
        raise RuntimeError(f"expected one JSON object at {path}")
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


def sealed(
    unsigned: Mapping[str, Any],
    key: str,
) -> dict[str, Any]:
    return {**unsigned, key: canonical_sha256(unsigned)}


def meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(
        encoding="utf-8"
    ).splitlines():
        key, raw = line.split(":", 1)
        values[key] = int(raw.split()[0]) * 1024
    return values


def pid_rss_bytes(pid: int) -> int:
    try:
        for line in Path(f"/proc/{pid}/status").read_text(
            encoding="utf-8"
        ).splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024
    except (FileNotFoundError, ProcessLookupError):
        return 0
    return 0


def physical_cpu_ids() -> list[int]:
    allowed = sorted(os.sched_getaffinity(0))
    by_core: dict[tuple[int, int], list[int]] = defaultdict(list)
    for cpu_id in allowed:
        topology = Path(
            f"/sys/devices/system/cpu/cpu{cpu_id}/topology"
        )
        package_id = int(
            (topology / "physical_package_id").read_text().strip()
        )
        core_id = int((topology / "core_id").read_text().strip())
        by_core[(package_id, core_id)].append(cpu_id)
    selected = [
        min(cpu_ids)
        for _, cpu_ids in sorted(by_core.items())
    ]
    if len(selected) != WORKER_COUNT:
        raise RuntimeError(
            f"expected fourteen physical cores, found {len(selected)}"
        )
    return selected


def cpu_record(cpu_id: int) -> dict[str, Any]:
    topology = Path(f"/sys/devices/system/cpu/cpu{cpu_id}/topology")
    frequency = Path(
        f"/sys/devices/system/cpu/cpu{cpu_id}/cpufreq/cpuinfo_max_freq"
    )
    siblings_text = (
        topology / "thread_siblings_list"
    ).read_text().strip()
    sibling_ids: list[int] = []
    for component in siblings_text.split(","):
        if "-" in component:
            first, last = (int(value) for value in component.split("-"))
            sibling_ids.extend(range(first, last + 1))
        else:
            sibling_ids.append(int(component))
    return {
        "cpu_id": cpu_id,
        "core_id": int((topology / "core_id").read_text().strip()),
        "thread_siblings": sibling_ids,
        "maximum_frequency_khz": (
            int(frequency.read_text().strip())
            if frequency.exists()
            else None
        ),
    }


def weighted_quotas(
    calibration_seconds: Mapping[str, float],
    remaining_task_count: int,
) -> dict[str, int]:
    if any(seconds <= 0 for seconds in calibration_seconds.values()):
        raise RuntimeError("calibration duration must be positive")
    weights = {
        node_id: 1.0 / seconds
        for node_id, seconds in calibration_seconds.items()
    }
    total_weight = sum(weights.values())
    raw = {
        node_id: remaining_task_count * weight / total_weight
        for node_id, weight in weights.items()
    }
    quotas = {
        node_id: int(math.floor(value))
        for node_id, value in raw.items()
    }
    left = remaining_task_count - sum(quotas.values())
    order = sorted(
        raw,
        key=lambda node_id: (
            -(raw[node_id] - quotas[node_id]),
            node_id,
        ),
    )
    for node_id in order[:left]:
        quotas[node_id] += 1
    if sum(quotas.values()) != remaining_task_count:
        raise RuntimeError("weighted task quotas do not close")
    return quotas


def fixed_from_dos(rows: list[Mapping[str, Any]]) -> list[int]:
    fixed = [0] * 871
    for row in rows:
        fixed[int(row["energy"]) + 435] = int(row["count"])
    return fixed


def load_probe_results() -> tuple[dict[str, Any], dict[str, Any]]:
    batch = load_json(BATCH_RESULT)
    scheduler = load_json(SCHEDULER_RESULT)
    validate_seal(batch, "result_sha256")
    validate_seal(scheduler, "result_sha256")
    if (
        batch.get("result_sha256") != EXPECTED_BATCH_RESULT_SHA256
        or scheduler.get("result_sha256")
        != EXPECTED_SCHEDULER_RESULT_SHA256
        or batch.get("campaign_id") != CAMPAIGN_ID
        or scheduler.get("campaign_id") != CAMPAIGN_ID
        or int(batch.get("selected_root_batch_size", 0))
        != ROOT_BATCH_SIZE
        or int(scheduler.get("root_batch_size", 0))
        != ROOT_BATCH_SIZE
        or scheduler.get("selected_profile_id") != PROFILE_ID
        or not bool(scheduler.get("selected_is_new_scheduler"))
    ):
        raise RuntimeError("hybrid probe selection identity changed")
    return batch, scheduler


def selected_scheduler_profile(
    scheduler: Mapping[str, Any],
) -> dict[str, Any]:
    selected = [
        dict(profile)
        for profile in scheduler["profiles"]
        if profile.get("profile_id") == PROFILE_ID
    ]
    if len(selected) != 1:
        raise RuntimeError("selected scheduler profile is not unique")
    profile = selected[0]
    if (
        not bool(profile.get("full_prime_exact_equality"))
        or not bool(profile.get("system_reserve_maintained"))
        or int(profile.get("worker_count", 0)) != WORKER_COUNT
    ):
        raise RuntimeError("selected scheduler profile is not admissible")
    return profile


def build_plan(
    engine: Any,
    instance: Mapping[str, Any],
    batch: Mapping[str, Any],
    scheduler: Mapping[str, Any],
    cpu_ids: Sequence[int],
) -> dict[str, Any]:
    smart_result = load_json(SMART_RESULT)
    validate_seal(smart_result, "result_sha256")
    if smart_result.get("result_sha256") != EXPECTED_SMART_RESULT_SHA256:
        raise RuntimeError("smart V4.0 result identity changed")
    smart_plan = dict(smart_result["plan"])
    selected = selected_scheduler_profile(scheduler)
    if list(selected["requested_cpu_ids"]) != list(cpu_ids):
        raise RuntimeError("current physical-core roster differs from probe")

    freeze = engine.load_port_freeze()
    ownership = engine.factor_ownership(instance)
    y_length = int(engine.W_Y_LENGTH)
    tasks_per_prime = y_length // ROOT_BATCH_SIZE
    retained_width = int(freeze["conditional_induced_width"])
    retained_entries_per_worker = ROOT_BATCH_SIZE << retained_width
    aggregate_entries = WORKER_COUNT * retained_entries_per_worker
    node_ids = [f"SLC_{index:02d}" for index in range(WORKER_COUNT)]
    unsigned = {
        "schema": "SLCV40_24_H14C_512_EXECUTION_PLAN_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "version_label": VERSION_LABEL,
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "numerical_object": "SLCX032_FOUR_BIT_LINKED_SUPERCELL_OPERATOR",
        "scale_delta": (
            "SMART_BATCH4_PLUS_CALIBRATED_PINNED_PHYSICAL_CORE_SCHEDULER"
        ),
        "scheduler_profile_id": PROFILE_ID,
        "worker_topology": "PINNED_H14_PHYSICAL_CORES",
        "cluster_size": WORKER_COUNT,
        "node_ids": node_ids,
        "requested_cpu_ids": list(cpu_ids),
        "cpu_topology": [cpu_record(cpu_id) for cpu_id in cpu_ids],
        "active_changes": [
            "SMART_CAPACITY_SELECTION",
            "PER_PRIME_NODE_CALIBRATION",
            "INVERSE_CALIBRATION_WEIGHTED_STATIC_QUEUES",
            "PHYSICAL_CORE_AFFINITY",
            "BALANCED_ORDERED_PRIME_COMPLETION_RECEIPTS",
            "W10_ORDERED_SQUARE_RESPONSE",
            "ACTIVE_FULL_Q_512_BY_512",
            "OPEN_PORT_POSITION_ROUTING",
        ],
        "port_order": [int(value) for value in engine.PORT_ORDER],
        "cut_edges": ownership["cut_edges"],
        "conditional_order": [
            int(value) for value in freeze["conditional_order"]
        ],
        "conditional_induced_width": retained_width,
        "y_ntt_length": y_length,
        "z_root_order": 2 * y_length,
        "root_batch_size": ROOT_BATCH_SIZE,
        "retained_capacity_exponent_per_worker": 24,
        "retained_batch_entries_per_worker": retained_entries_per_worker,
        "logical_union_batch_entries_per_worker": (
            ROOT_BATCH_SIZE << (retained_width + 1)
        ),
        "retained_batch_entry_ceiling_exponent": 26,
        "logical_union_batch_entry_ceiling_exponent": 27,
        "aggregate_sharded_retained_entries": aggregate_entries,
        "aggregate_sharded_capacity_equivalent_log2": math.log2(
            aggregate_entries
        ),
        "primes": [int(value) for value in engine.PRIMES_3],
        "tasks_per_prime": tasks_per_prime,
        "calibration_tasks_per_prime": WORKER_COUNT,
        "weighted_tasks_per_prime": tasks_per_prime - WORKER_COUNT,
        "total_task_count": tasks_per_prime * len(engine.PRIMES_3),
        "total_calibration_task_count": (
            WORKER_COUNT * len(engine.PRIMES_3)
        ),
        "total_weighted_task_count": (
            (tasks_per_prime - WORKER_COUNT) * len(engine.PRIMES_3)
        ),
        "prime_completion_receipt_count": len(engine.PRIMES_3),
        "prime_completion_receipt_tree": (
            "BALANCED_ORDERED_128_TO_64_TO_32_TO_16_TO_8_TO_4_TO_2_TO_1"
        ),
        "minimum_available_memory_bytes": (
            MINIMUM_AVAILABLE_MEMORY_BYTES
        ),
        "per_worker_address_space_cap_bytes": (
            PER_WORKER_ADDRESS_SPACE_BYTES
        ),
        "probe_dependencies": {
            "batch_result_sha256": batch["result_sha256"],
            "batch_result_file_sha256": sha256_file(BATCH_RESULT),
            "scheduler_result_sha256": scheduler["result_sha256"],
            "scheduler_result_file_sha256": sha256_file(
                SCHEDULER_RESULT
            ),
            "selected_prime_wall_seconds": scheduler[
                "selected_kernel_wall_seconds"
            ],
            "fresh_fixed_prime_wall_seconds": scheduler[
                "fixed_kernel_wall_seconds"
            ],
            "selected_over_fixed_prime_wall_ratio": scheduler[
                "selected_over_fixed_wall_ratio"
            ],
        },
        "fiber_contract": smart_plan["fiber_contract"],
        "excluded_changes": [
            "CUTSET_BRANCHING",
            "GLOBAL_SPIN_GAUGE",
            "FOURTH_CRT_PRIME",
            "CAPACITY29_PROFILE",
            "COMPACT_STAGE4C_GRAPH",
            "SAME_HOST_SUB_SLC_EXECUTION_QUEUES",
        ],
    }
    if (
        unsigned["conditional_induced_width"] != 22
        or unsigned["port_order"] != [6, 15, 16, 58]
        or unsigned["root_batch_size"] != 4
        or unsigned["retained_batch_entries_per_worker"] != 1 << 24
        or unsigned["logical_union_batch_entries_per_worker"] != 1 << 25
        or unsigned["tasks_per_prime"] != 128
        or unsigned["total_task_count"] != 384
        or unsigned["aggregate_sharded_retained_entries"]
        != 14 * (1 << 24)
    ):
        raise RuntimeError("hybrid full-run plan differs")
    return sealed(unsigned, "plan_sha256")


def source_manifest() -> dict[str, Any]:
    paths = [
        HERE / "README.md",
        CONTRACT,
        HERE / "slcv40_batch_fine_probe.py",
        HERE / "slcv40_scheduler_prime_probe.py",
        HERE / "slcv40_hybrid_worker.py",
        Path(__file__).resolve(),
        HERE / "slcv40_hybrid_validate.py",
        BATCH_RESULT,
        BATCH_RESULT.with_suffix(".md"),
        SCHEDULER_RESULT,
        SCHEDULER_RESULT.with_suffix(".md"),
        V4_ROOT / "README.md",
        V4_ROOT / "SLCV4.0-24-F16-512_CONTRACT.json",
        V4_ROOT / "slcv40_runner.py",
        FROZEN_RESULT,
        SMART_ROOT / "README.md",
        SMART_ROOT / "SLCV40_SMART_CONFIG_CONTRACT.json",
        SMART_ROOT / "slcv40_smart_runner.py",
        SMART_RESULT,
        V22_ROOT / "slcv0022_runner.py",
        V22_ROOT / "slcv0022_worker.py",
        V21_ROOT / "slcv0021_runner.py",
        V21_ROOT / "slcv0021_worker.py",
        hot_runner.ENGINE_PATH,
        hot_runner.INSTANCE_PATH,
        frozen_v4.HOT_COMPLETION,
        frozen_v4.HOT_RESULT,
        V31_ROOT / "slcv0031_w10.py",
        V4_DEV_ROOT / "slcv004_fiber_probe.py",
        frozen_v4.FIBER_PROBE_RESULT,
    ]
    rows = [
        {
            "path": str(path.relative_to(QC_ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in paths
    ]
    return sealed(
        {
            "schema": "SLCV40_24_H14C_512_SOURCE_MANIFEST_V1",
            "campaign_id": CAMPAIGN_ID,
            "display_name": DISPLAY_NAME,
            "sources": rows,
        },
        "manifest_sha256",
    )


def checkpoint_expected(
    *,
    plan: Mapping[str, Any],
    instance: Mapping[str, Any],
    task: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "domain": worker.CHECKPOINT_DOMAIN,
        "campaign_id": CAMPAIGN_ID,
        "plan_sha256": plan["plan_sha256"],
        "instance_sha256": instance["instance_sha256"],
        "node_id": task["node_id"],
        "requested_cpu_id": int(task["cpu_id"]),
        "observed_affinity": [int(task["cpu_id"])],
        "task_id": task["task_id"],
        "prime_index": int(task["prime_index"]),
        "prime": int(task["prime"]),
        "scheduler_phase": task["scheduler_phase"],
        "task_index": int(task["task_index"]),
        "root_start": int(task["root_start"]),
        "root_stop": int(task["root_stop"]),
    }


def balanced_tree(
    leaves: Sequence[str],
    *,
    plan_sha256: str,
    instance_sha256: str,
    prime_index: int,
) -> tuple[list[list[str]], str]:
    if not leaves or len(leaves) & (len(leaves) - 1):
        raise RuntimeError(
            "prime completion receipt requires a power-of-two roster"
        )
    levels: list[list[str]] = []
    current = list(leaves)
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


def prime_completion_receipt(
    *,
    plan: Mapping[str, Any],
    instance: Mapping[str, Any],
    prime_index: int,
    prime: int,
    ordered_checkpoints: Sequence[Mapping[str, Any]],
    calibration_seconds: Mapping[str, float],
    quotas: Mapping[str, int],
    assignments: Mapping[str, Sequence[int]],
) -> dict[str, Any]:
    leaves = [
        str(checkpoint["record_sha256"])
        for checkpoint in ordered_checkpoints
    ]
    levels, root = balanced_tree(
        leaves,
        plan_sha256=str(plan["plan_sha256"]),
        instance_sha256=str(instance["instance_sha256"]),
        prime_index=prime_index,
    )
    unsigned = {
        "schema": "SLCV40_H14C_PRIME_COMPLETION_RECEIPT_V1",
        "domain": PRIME_RECEIPT_DOMAIN,
        "campaign_id": CAMPAIGN_ID,
        "plan_sha256": plan["plan_sha256"],
        "instance_sha256": instance["instance_sha256"],
        "prime_index": prime_index,
        "prime": prime,
        "root_batch_size": ROOT_BATCH_SIZE,
        "root_count": int(plan["y_ntt_length"]),
        "task_count": len(ordered_checkpoints),
        "ordered_task_roster": [
            {
                "task_index": int(checkpoint["task_index"]),
                "root_start": int(checkpoint["root_start"]),
                "root_stop": int(checkpoint["root_stop"]),
                "node_id": checkpoint["node_id"],
                "scheduler_phase": checkpoint["scheduler_phase"],
                "record_sha256": checkpoint["record_sha256"],
            }
            for checkpoint in ordered_checkpoints
        ],
        "ordered_leaf_sha256": leaves,
        "balanced_levels": levels,
        "balanced_root_sha256": root,
        "calibration_seconds_by_node": dict(calibration_seconds),
        "remaining_task_quotas": dict(quotas),
        "remaining_root_assignments": {
            node_id: list(root_starts)
            for node_id, root_starts in assignments.items()
        },
    }
    return sealed(unsigned, "receipt_sha256")


def validate_prime_receipt(receipt: Mapping[str, Any]) -> None:
    validate_seal(receipt, "receipt_sha256")
    leaves = [str(value) for value in receipt["ordered_leaf_sha256"]]
    levels, root = balanced_tree(
        leaves,
        plan_sha256=str(receipt["plan_sha256"]),
        instance_sha256=str(receipt["instance_sha256"]),
        prime_index=int(receipt["prime_index"]),
    )
    if (
        len(leaves) != 128
        or receipt.get("balanced_levels") != levels
        or receipt.get("balanced_root_sha256") != root
    ):
        raise RuntimeError("prime completion receipt tree changed")


def write_heartbeat(payload: Mapping[str, Any]) -> None:
    unsigned = {
        "schema": "SLCV40_H14C_HEARTBEAT_V1",
        "campaign_id": CAMPAIGN_ID,
        "updated_unix": time.time(),
        **dict(payload),
    }
    atomic_json(
        HEARTBEAT,
        sealed(unsigned, "heartbeat_sha256"),
    )


def ensure_fresh_run() -> None:
    occupied = [
        path
        for path in (
            COMPLETION,
            OPERATOR_RESULT,
            RESULT_JSON,
            RESULT_MD,
            WORK / "prime_receipts",
        )
        if path.exists()
    ]
    if WORK.exists():
        occupied.extend(WORK.glob("SLC_*/checkpoints/*.json"))
    if occupied:
        raise RuntimeError(
            "hybrid full-run artifacts already exist: "
            + ", ".join(str(path) for path in occupied[:5])
        )


def execute_cluster(
    engine: Any,
    instance: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    memory_before = meminfo()
    if memory_before["MemAvailable"] < MINIMUM_AVAILABLE_MEMORY_BYTES:
        raise RuntimeError("8 GiB system-memory reserve is unavailable")

    node_ids = [str(value) for value in plan["node_ids"]]
    cpu_ids = [int(value) for value in plan["requested_cpu_ids"]]
    cpu_by_node = dict(zip(node_ids, cpu_ids))
    context = mp.get_context("spawn")
    result_queue = context.Queue()
    task_queues = {
        node_id: context.Queue() for node_id in node_ids
    }
    checkpoint_roots = {
        node_id: WORK / node_id / "checkpoints"
        for node_id in node_ids
    }
    for path in checkpoint_roots.values():
        path.mkdir(parents=True, exist_ok=True)
    processes = {
        node_id: context.Process(
            target=worker.node_loop,
            args=(
                node_id,
                cpu_by_node[node_id],
                instance,
                plan,
                task_queues[node_id],
                result_queue,
                str(checkpoint_roots[node_id]),
                str(ENGINE_PATH),
                PER_WORKER_ADDRESS_SPACE_BYTES,
            ),
            name=f"SLCV40-H14C-{node_id}",
        )
        for node_id in node_ids
    }

    started = time.perf_counter()
    for process in processes.values():
        process.start()

    pids: dict[str, int] = {}
    readiness: dict[str, dict[str, Any]] = {}
    peak_aggregate_rss = 0
    minimum_available = memory_before["MemAvailable"]
    maximum_active_nodes = 0
    worker_peaks = {node_id: 0 for node_id in node_ids}
    worker_wall = {node_id: 0.0 for node_id in node_ids}
    worker_cpu = 0.0
    executed_tasks = 0
    checkpoint_roster: list[dict[str, Any]] = []
    prime_receipt_roster: list[dict[str, Any]] = []
    prime_metrics: list[dict[str, Any]] = []
    modular_coefficients: list[list[list[int]]] = []
    structural_metrics: dict[str, int] = {}
    last_heartbeat = 0.0
    startup_seconds = 0.0

    def sample_resources() -> None:
        nonlocal peak_aggregate_rss
        nonlocal minimum_available
        nonlocal maximum_active_nodes
        rss = {
            node_id: pid_rss_bytes(pid)
            for node_id, pid in pids.items()
        }
        peak_aggregate_rss = max(
            peak_aggregate_rss,
            sum(rss.values()),
        )
        maximum_active_nodes = max(
            maximum_active_nodes,
            sum(value > 0 for value in rss.values()),
        )
        available = meminfo()["MemAvailable"]
        minimum_available = min(minimum_available, available)
        if available < MINIMUM_AVAILABLE_MEMORY_BYTES:
            raise RuntimeError(
                "hybrid run crossed the 8 GiB system-memory reserve"
            )

    def collect(
        *,
        pending_tasks: Mapping[str, Mapping[str, Any]],
        records: dict[int, dict[str, Any]],
        prime_index: int,
        phase: str,
    ) -> None:
        nonlocal worker_cpu
        nonlocal executed_tasks
        nonlocal last_heartbeat
        pending = set(pending_tasks)
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
                            "phase": phase,
                            "prime_index": prime_index,
                            "prime_count": len(plan["primes"]),
                            "pending_task_count": len(pending),
                            "executed_task_count": executed_tasks,
                            "peak_aggregate_worker_rss_bytes": (
                                peak_aggregate_rss
                            ),
                            "minimum_available_memory_bytes": (
                                minimum_available
                            ),
                            "worker_pids": pids,
                        }
                    )
                    print(
                        json.dumps(
                            {
                                "prime": (
                                    f"{prime_index + 1}/"
                                    f"{len(plan['primes'])}"
                                ),
                                "phase": phase,
                                "pending": len(pending),
                                "executed": executed_tasks,
                                "peak_gib": round(
                                    peak_aggregate_rss / (1 << 30),
                                    3,
                                ),
                                "min_available_gib": round(
                                    minimum_available / (1 << 30),
                                    3,
                                ),
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
                if any(
                    not process.is_alive()
                    for process in processes.values()
                ):
                    raise RuntimeError(
                        "hybrid worker exited during execution"
                    )
                continue
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')} error: "
                    f"{message.get('error')}\n"
                    f"{message.get('traceback')}"
                )
            if message.get("kind") != "DONE":
                raise RuntimeError("unexpected hybrid worker message")
            task_id = str(message["task_id"])
            if task_id not in pending:
                raise RuntimeError(
                    "unexpected or duplicate hybrid task completion"
                )
            task = pending_tasks[task_id]
            checkpoint_path = Path(str(message["checkpoint_path"]))
            try:
                relative_path = checkpoint_path.resolve().relative_to(
                    WORK.resolve()
                )
            except ValueError as error:
                raise RuntimeError(
                    "hybrid checkpoint escaped the work directory"
                ) from error
            checkpoint = load_json(checkpoint_path)
            worker.validate_checkpoint(
                checkpoint,
                checkpoint_expected(
                    plan=plan,
                    instance=instance,
                    task=task,
                ),
            )
            task_index = int(task["task_index"])
            if task_index in records:
                raise RuntimeError("hybrid task index completed twice")
            records[task_index] = checkpoint
            pending.remove(task_id)
            executed_tasks += 1
            worker_cpu += float(message["process_cpu_seconds"])
            node_id = str(message["node_id"])
            worker_wall[node_id] += float(message["wall_seconds"])
            worker_peaks[node_id] = max(
                worker_peaks[node_id],
                int(message["maximum_rss_bytes"]),
            )
            checkpoint_roster.append(
                {
                    "path": str(relative_path),
                    "node_id": node_id,
                    "requested_cpu_id": int(task["cpu_id"]),
                    "prime_index": int(task["prime_index"]),
                    "scheduler_phase": task["scheduler_phase"],
                    "task_index": task_index,
                    "root_start": int(task["root_start"]),
                    "root_stop": int(task["root_stop"]),
                    "record_sha256": checkpoint["record_sha256"],
                }
            )
            for key, value in checkpoint["structural_metrics"].items():
                if key.startswith("sum_"):
                    if (
                        key in structural_metrics
                        and structural_metrics[key] != int(value)
                    ):
                        raise RuntimeError(
                            "structural work changed across hybrid tasks"
                        )
                    structural_metrics[key] = int(value)
                else:
                    structural_metrics[key] = max(
                        structural_metrics.get(key, 0),
                        int(value),
                    )
            sample_resources()

    try:
        while len(pids) < len(node_ids):
            message = result_queue.get(timeout=120)
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')} startup error: "
                    f"{message.get('error')}\n"
                    f"{message.get('traceback')}"
                )
            if message.get("kind") != "READY":
                raise RuntimeError(
                    "unexpected message before hybrid readiness"
                )
            node_id = str(message["node_id"])
            if (
                node_id not in cpu_by_node
                or message.get("observed_affinity")
                != [cpu_by_node[node_id]]
                or int(message.get("requested_cpu_id", -1))
                != cpu_by_node[node_id]
            ):
                raise RuntimeError("hybrid worker affinity differs")
            pids[node_id] = int(message["worker_pid"])
            readiness[node_id] = dict(message)
            worker_peaks[node_id] = int(
                message["maximum_rss_bytes"]
            )
        startup_seconds = time.perf_counter() - started
        sample_resources()

        y_length = int(plan["y_ntt_length"])
        starts = list(range(0, y_length, ROOT_BATCH_SIZE))
        for prime_index, prime_value in enumerate(plan["primes"]):
            prime = int(prime_value)
            evaluations = np.zeros((16, y_length), dtype=np.int64)
            records: dict[int, dict[str, Any]] = {}
            prime_started = time.perf_counter()

            calibration_tasks: dict[str, dict[str, Any]] = {}
            for task_index, (node_id, root_start) in enumerate(
                zip(node_ids, starts)
            ):
                root_stop = root_start + ROOT_BATCH_SIZE
                task_id = f"p{prime_index:02d}t{task_index:03d}"
                task = {
                    "task_id": task_id,
                    "node_id": node_id,
                    "cpu_id": cpu_by_node[node_id],
                    "prime_index": prime_index,
                    "prime": prime,
                    "scheduler_phase": "CALIBRATION",
                    "task_index": task_index,
                    "root_start": root_start,
                    "root_stop": root_stop,
                    "checkpoint_name": (
                        f"prime_{prime_index:02d}_task_{task_index:03d}_"
                        f"roots_{root_start:04d}_{root_stop:04d}.json"
                    ),
                }
                calibration_tasks[task_id] = task
                task_queues[node_id].put(task)
            collect(
                pending_tasks=calibration_tasks,
                records=records,
                prime_index=prime_index,
                phase="CALIBRATION",
            )
            calibration_phase_seconds = (
                time.perf_counter() - prime_started
            )
            calibration_seconds = {
                node_id: float(records[index]["wall_seconds"])
                for index, node_id in enumerate(node_ids)
            }
            remaining_starts = starts[WORKER_COUNT:]
            quotas = weighted_quotas(
                calibration_seconds,
                len(remaining_starts),
            )
            assignments: dict[str, list[int]] = {
                node_id: [] for node_id in node_ids
            }
            cursor = 0
            for node_id in node_ids:
                count = quotas[node_id]
                assignments[node_id] = remaining_starts[
                    cursor : cursor + count
                ]
                cursor += count
            if cursor != len(remaining_starts):
                raise RuntimeError(
                    "hybrid weighted assignment does not cover roots"
                )

            weighted_started = time.perf_counter()
            weighted_tasks: dict[str, dict[str, Any]] = {}
            for node_id in node_ids:
                for root_start in assignments[node_id]:
                    task_index = root_start // ROOT_BATCH_SIZE
                    root_stop = root_start + ROOT_BATCH_SIZE
                    task_id = f"p{prime_index:02d}t{task_index:03d}"
                    task = {
                        "task_id": task_id,
                        "node_id": node_id,
                        "cpu_id": cpu_by_node[node_id],
                        "prime_index": prime_index,
                        "prime": prime,
                        "scheduler_phase": "WEIGHTED_EXECUTION",
                        "task_index": task_index,
                        "root_start": root_start,
                        "root_stop": root_stop,
                        "checkpoint_name": (
                            f"prime_{prime_index:02d}_"
                            f"task_{task_index:03d}_"
                            f"roots_{root_start:04d}_{root_stop:04d}.json"
                        ),
                    }
                    weighted_tasks[task_id] = task
                    task_queues[node_id].put(task)
            collect(
                pending_tasks=weighted_tasks,
                records=records,
                prime_index=prime_index,
                phase="WEIGHTED_EXECUTION",
            )
            weighted_phase_seconds = (
                time.perf_counter() - weighted_started
            )
            prime_kernel_seconds = time.perf_counter() - prime_started

            if len(records) != 128:
                raise RuntimeError("hybrid prime task count changed")
            ordered = [records[index] for index in range(128)]
            covered = [
                root
                for checkpoint in ordered
                for root in range(
                    int(checkpoint["root_start"]),
                    int(checkpoint["root_stop"]),
                )
            ]
            if covered != list(range(y_length)):
                raise RuntimeError("hybrid prime root coverage changed")
            for checkpoint in ordered:
                start = int(checkpoint["root_start"])
                stop = int(checkpoint["root_stop"])
                evaluations[:, start:stop] = np.asarray(
                    checkpoint["evaluations"],
                    dtype=np.int64,
                )

            receipt = prime_completion_receipt(
                plan=plan,
                instance=instance,
                prime_index=prime_index,
                prime=prime,
                ordered_checkpoints=ordered,
                calibration_seconds=calibration_seconds,
                quotas=quotas,
                assignments=assignments,
            )
            validate_prime_receipt(receipt)
            receipt_path = (
                WORK
                / "prime_receipts"
                / f"prime_{prime_index:02d}.json"
            )
            atomic_json(receipt_path, receipt)
            prime_receipt_roster.append(
                {
                    "path": str(receipt_path.relative_to(WORK)),
                    "prime_index": prime_index,
                    "prime": prime,
                    "receipt_sha256": receipt["receipt_sha256"],
                    "balanced_root_sha256": receipt[
                        "balanced_root_sha256"
                    ],
                }
            )

            exact = engine._modules()[1]
            inverse_started = time.perf_counter()
            modular_coefficients.append(
                [
                    [
                        int(value)
                        for value in exact._inverse_ntt(
                            evaluations[state, :].tolist(),
                            prime,
                        )
                    ]
                    for state in range(16)
                ]
            )
            inverse_ntt_seconds = time.perf_counter() - inverse_started
            task_count_by_node: dict[str, int] = defaultdict(int)
            task_wall_by_node: dict[str, float] = defaultdict(float)
            for checkpoint in ordered:
                node_id = str(checkpoint["node_id"])
                task_count_by_node[node_id] += 1
                task_wall_by_node[node_id] += float(
                    checkpoint["wall_seconds"]
                )
            prime_metrics.append(
                {
                    "prime_index": prime_index,
                    "prime": prime,
                    "calibration_phase_seconds": (
                        calibration_phase_seconds
                    ),
                    "weighted_phase_seconds": weighted_phase_seconds,
                    "kernel_wall_seconds": prime_kernel_seconds,
                    "inverse_ntt_seconds": inverse_ntt_seconds,
                    "calibration_seconds_by_node": calibration_seconds,
                    "remaining_task_quotas": quotas,
                    "remaining_root_assignments": assignments,
                    "task_count_by_node": dict(
                        sorted(task_count_by_node.items())
                    ),
                    "task_wall_seconds_by_node": dict(
                        sorted(task_wall_by_node.items())
                    ),
                    "sum_task_wall_seconds": sum(
                        task_wall_by_node.values()
                    ),
                }
            )
            print(
                json.dumps(
                    {
                        "event": "PRIME_COMPLETE",
                        "prime": f"{prime_index + 1}/{len(plan['primes'])}",
                        "kernel_wall_seconds": prime_kernel_seconds,
                        "inverse_ntt_seconds": inverse_ntt_seconds,
                        "task_count_by_node": dict(
                            sorted(task_count_by_node.items())
                        ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    finally:
        for node_id in node_ids:
            try:
                task_queues[node_id].put(None)
            except Exception:
                pass
        for process in processes.values():
            process.join(timeout=10)
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)

    exact = engine._modules()[1]
    local_bound = int(engine.LOCAL_BOUND)
    primes = [int(value) for value in plan["primes"]]
    expected_row_sum = 1 << (
        int(instance["N"]) - len(plan["port_order"])
    )
    w_coefficients: list[list[int]] = []
    for state in range(16):
        row = [
            int(
                exact._crt(
                    [
                        modular_coefficients[prime_index][state][degree]
                        for prime_index in range(len(primes))
                    ],
                    primes,
                )
            )
            for degree in range(int(plan["y_ntt_length"]))
        ]
        if any(row[local_bound + 1 :]):
            raise RuntimeError(
                "hybrid linked operator has support above local bound"
            )
        active = row[: local_bound + 1]
        if any(value < 0 for value in active):
            raise RuntimeError(
                "hybrid linked operator has a negative coefficient"
            )
        if sum(active) != expected_row_sum:
            raise RuntimeError(
                "hybrid linked operator row normalization changed"
            )
        w_coefficients.append(active)

    ownership = engine.factor_ownership(instance)
    glue = engine.glue_y_degrees(
        ownership["cut_edges"],
        plan["port_order"],
    )
    operator = {
        "schema": "SLCX032_N72_OPERATOR_V1",
        "campaign_id": CAMPAIGN_ID,
        "source_validation": engine.validate_n72_instance(instance),
        "source_instance_id": instance["instance_id"],
        "source_instance_sha256": instance["instance_sha256"],
        "port_freeze_sha256": engine.load_port_freeze()[
            "freeze_sha256"
        ],
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
            "y_ntt_length": plan["y_ntt_length"],
            "z_root_order": plan["z_root_order"],
            "selected_primes": primes,
            "root_batch_size": plan["root_batch_size"],
            "conditional_induced_width": plan[
                "conditional_induced_width"
            ],
            "conditional_order": plan["conditional_order"],
            "conditional_order_sha256": canonical_sha256(
                plan["conditional_order"]
            ),
            **structural_metrics,
        },
    }
    if operator["w_sha256"] != frozen_v4.EXPECTED_OPERATOR_SHA256:
        raise RuntimeError("hybrid compiled linked operator differs")
    recovery = engine.recover_n72_one_cell(operator)
    if (
        recovery["fixed_coefficient_sha256"]
        != frozen_v4.EXPECTED_FIXED_SHA256
    ):
        raise RuntimeError("hybrid one-cell closure identity differs")
    memory_after = meminfo()
    if maximum_active_nodes != WORKER_COUNT:
        raise RuntimeError("all fourteen hybrid workers were not observed")

    checkpoint_roster.sort(
        key=lambda row: (
            int(row["prime_index"]),
            int(row["task_index"]),
        )
    )
    task_count_by_node: dict[str, int] = defaultdict(int)
    for row in checkpoint_roster:
        task_count_by_node[str(row["node_id"])] += 1
    return {
        "operator": operator,
        "recovery": recovery,
        "checkpoint_roster": checkpoint_roster,
        "checkpoint_roster_sha256": canonical_sha256(
            checkpoint_roster
        ),
        "prime_receipt_roster": prime_receipt_roster,
        "prime_receipt_roster_sha256": canonical_sha256(
            prime_receipt_roster
        ),
        "metrics": {
            "wall_seconds_this_invocation": time.perf_counter() - started,
            "startup_seconds": startup_seconds,
            "sum_prime_kernel_wall_seconds": sum(
                float(row["kernel_wall_seconds"])
                for row in prime_metrics
            ),
            "sum_worker_cpu_seconds": worker_cpu,
            "worker_wall_seconds_by_node": worker_wall,
            "task_count_by_node": dict(sorted(task_count_by_node.items())),
            "executed_task_count": executed_tasks,
            "reused_task_count": 0,
            "total_task_count": len(checkpoint_roster),
            "prime_completion_receipt_count": len(
                prime_receipt_roster
            ),
            "worker_pids": pids,
            "worker_readiness": readiness,
            "worker_peak_rss_bytes_by_node": worker_peaks,
            "sum_node_peak_rss_bytes": sum(worker_peaks.values()),
            "peak_sampled_aggregate_worker_rss_bytes": (
                peak_aggregate_rss
            ),
            "maximum_active_nodes": maximum_active_nodes,
            "available_memory_before_bytes": memory_before["MemAvailable"],
            "minimum_available_memory_bytes": minimum_available,
            "available_memory_after_bytes": memory_after["MemAvailable"],
            "swap_free_before_bytes": memory_before["SwapFree"],
            "swap_free_after_bytes": memory_after["SwapFree"],
            "prime_metrics": prime_metrics,
        },
    }


def render_markdown(result: Mapping[str, Any]) -> str:
    metrics = result["metrics"]
    comparison = result["comparison"]
    return "\n".join(
        [
            f"# {DISPLAY_NAME} exact N72 result",
            "",
            f"**Status:** `{result['execution_status']}`  ",
            f"**Classification:** {result['result_classification']}",
            "",
            "## Selected execution profile",
            "",
            "- Retained capacity per worker: **2^24**",
            "- Kernel root batch: **4**",
            "- Scheduler: **calibrated pinned H14 physical cores**",
            "- Active semantic fiber: **512 x 512**",
            (
                "- Aggregate sharded retained entries: "
                f"**{result['plan']['aggregate_sharded_retained_entries']:,}**"
            ),
            "",
            "## Fresh N72 execution",
            "",
            (
                f"- Fresh tasks: **{metrics['executed_task_count']}/"
                f"{result['plan']['total_task_count']}**"
            ),
            (
                "- Prime completion receipts: "
                f"**{metrics['prime_completion_receipt_count']}/3**"
            ),
            (
                "- Dense wall time: "
                f"**{metrics['wall_seconds_this_invocation']:.6f} s**"
            ),
            (
                "- Peak sampled aggregate worker RSS: "
                f"**{metrics['peak_sampled_aggregate_worker_rss_bytes'] / (1 << 30):.6f} GiB**"
            ),
            (
                "- Minimum available memory: "
                f"**{metrics['minimum_available_memory_bytes'] / (1 << 30):.6f} GiB**"
            ),
            (
                "- Full 871-coefficient equality: "
                f"**{comparison['full_coefficient_equality']}**"
            ),
            f"- Configuration count: **{result['configuration_count']}**",
            "",
            "## Scheduler comparison",
            "",
            (
                "- Full wall change versus the smart fixed-F16 run: "
                f"**{comparison['hybrid_minus_smart_wall_seconds']:+.6f} s**"
            ),
            (
                "- Smart fixed-F16 / hybrid wall ratio: "
                f"**{comparison['smart_v4_over_hybrid_speed_ratio']:.6f}x**"
            ),
            (
                "- Full-run scheduler classification: "
                f"**{result['scheduler_optimization_result_classification']}**"
            ),
            "",
            "## Active fiber",
            "",
            (
                "- Event transitions executed: "
                f"**{result['fiber_execution']['transition_count_exercised']:,}**"
            ),
            (
                "- Full-position assignments: "
                f"**{result['fiber_execution']['assignment_count']:,}**"
            ),
            "",
            f"**Result SHA-256:** `{result['result_sha256']}`",
            "",
        ]
    )


def main() -> int:
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError(f"{key} must equal 1")
    ensure_fresh_run()
    frozen_v4.check_locked_sources()
    batch, scheduler = load_probe_results()
    frozen_result = load_json(FROZEN_RESULT)
    smart_result = load_json(SMART_RESULT)
    validate_seal(frozen_result, "result_sha256")
    validate_seal(smart_result, "result_sha256")
    if (
        frozen_result.get("result_sha256")
        != EXPECTED_FROZEN_RESULT_SHA256
        or smart_result.get("result_sha256")
        != EXPECTED_SMART_RESULT_SHA256
    ):
        raise RuntimeError("full-run comparison identity changed")

    total_started = time.perf_counter()
    (
        engine,
        instance,
        baseline_completion,
        baseline_result,
        v21_completion,
        v21_result,
    ) = hot_runner.load_inputs()
    hot_completion = load_json(frozen_v4.HOT_COMPLETION)
    hot_result = load_json(frozen_v4.HOT_RESULT)
    if (
        instance.get("instance_sha256")
        != frozen_v4.EXPECTED_INSTANCE_SHA256
        or hot_completion.get("operator_w_sha256")
        != frozen_v4.EXPECTED_OPERATOR_SHA256
        or hot_result.get("operator_w_sha256")
        != frozen_v4.EXPECTED_OPERATOR_SHA256
    ):
        raise RuntimeError("frozen numerical parent identity changed")

    cpu_ids = physical_cpu_ids()
    plan = build_plan(
        engine,
        instance,
        batch,
        scheduler,
        cpu_ids,
    )
    manifest = source_manifest()
    WORK.mkdir(parents=True, exist_ok=True)
    RELEASE.mkdir(parents=True, exist_ok=True)
    atomic_json(WORK / "EXECUTION_PLAN.json", plan)
    atomic_json(WORK / "SOURCE_MANIFEST.json", manifest)

    cluster = execute_cluster(engine, instance, plan)
    recovery = cluster["recovery"]
    candidate_fixed = [
        int(value) for value in recovery["fixed_coefficients"]
    ]
    comparison_vectors = {
        "v0_2": fixed_from_dos(baseline_completion["dos"]),
        "v0_2_1": fixed_from_dos(v21_completion["dos"]),
        "v0_2_2": fixed_from_dos(hot_completion["dos"]),
    }
    difference_positions = {
        name: [
            index - 435
            for index, (candidate, reference) in enumerate(
                zip(candidate_fixed, vector)
            )
            if candidate != reference
        ]
        for name, vector in comparison_vectors.items()
    }
    if any(difference_positions.values()):
        raise RuntimeError("hybrid N72 coefficient vector differs")
    if (
        canonical_sha256(candidate_fixed)
        != frozen_v4.EXPECTED_FIXED_SHA256
    ):
        raise RuntimeError(
            "hybrid N72 fixed-coefficient identity changed"
        )

    w10, _engine = fiber_engine.load_modules()
    fiber_receipt, transition_maps = fiber_engine.exercise_full_fiber(w10)
    open_port, routing = fiber_engine.build_open_port_attachment(w10)
    closed = fiber_engine.build_closed_n72_attachment(
        cluster["operator"],
        candidate_fixed,
        routing,
    )
    del transition_maps
    atomic_json(OPERATOR_RESULT, cluster["operator"])

    metrics = cluster["metrics"]
    hybrid_wall = float(metrics["wall_seconds_this_invocation"])
    frozen_wall = float(
        frozen_result["metrics"]["wall_seconds_this_invocation"]
    )
    smart_wall = float(
        smart_result["metrics"]["wall_seconds_this_invocation"]
    )
    full_equal = all(
        not values for values in difference_positions.values()
    )
    optimization_persisted = hybrid_wall < smart_wall
    scheduler_classification = (
        "The test result suggests strong contact with the concept."
        if optimization_persisted
        else "The test falsifies the concept."
    )
    semantic_classification = (
        "The test result suggests strong contact with the concept."
    )
    comparison = {
        "fixed_domain": [-435, 435],
        "coefficient_count": 871,
        "difference_positions": difference_positions,
        "full_coefficient_equality": full_equal,
        "v0_2_wall_seconds": float(
            baseline_result["cluster_metrics"][
                "wall_seconds_this_invocation"
            ]
        ),
        "v0_2_1_wall_seconds": float(
            v21_result["metrics"]["wall_seconds_this_invocation"]
        ),
        "v0_2_2_wall_seconds": float(
            hot_result["metrics"]["wall_seconds_this_invocation"]
        ),
        "frozen_v4_wall_seconds": frozen_wall,
        "smart_v4_wall_seconds": smart_wall,
        "hybrid_h14c_wall_seconds": hybrid_wall,
        "hybrid_minus_frozen_wall_seconds": hybrid_wall - frozen_wall,
        "hybrid_minus_smart_wall_seconds": hybrid_wall - smart_wall,
        "frozen_v4_over_hybrid_speed_ratio": frozen_wall / hybrid_wall,
        "smart_v4_over_hybrid_speed_ratio": smart_wall / hybrid_wall,
        "hybrid_faster_than_frozen_v4": hybrid_wall < frozen_wall,
        "hybrid_faster_than_smart_v4": hybrid_wall < smart_wall,
        "optimization_persisted_across_full_n72": (
            optimization_persisted
        ),
    }
    checks = {
        "fresh_384_tasks_executed": (
            metrics["executed_task_count"] == 384
            and metrics["reused_task_count"] == 0
        ),
        "all_three_prime_completion_receipts_written": (
            metrics["prime_completion_receipt_count"] == 3
        ),
        "all_fourteen_workers_pinned": all(
            row["observed_affinity"] == [cpu_id]
            for row, cpu_id in zip(
                (
                    metrics["worker_readiness"][node_id]
                    for node_id in plan["node_ids"]
                ),
                plan["requested_cpu_ids"],
            )
        ),
        "selected_batch_and_scheduler_match_probes": (
            plan["root_batch_size"]
            == batch["selected_root_batch_size"]
            and plan["scheduler_profile_id"]
            == scheduler["selected_profile_id"]
        ),
        "retained_batch_under_2_pow_26_ceiling": (
            plan["retained_batch_entries_per_worker"] <= 1 << 26
        ),
        "logical_union_batch_under_2_pow_27_ceiling": (
            plan["logical_union_batch_entries_per_worker"] <= 1 << 27
        ),
        "all_871_coefficients_equal": full_equal,
        "exact_configuration_count_2_pow_72": (
            recovery["observed_configuration_count"] == 1 << 72
        ),
        "both_512_factors_active": (
            fiber_receipt["both_factors_active"]
            and fiber_receipt["constant_multiplicity"] is False
        ),
        "all_262144_fiber_addresses_executed": (
            fiber_receipt["assignment_count"] == 262144
        ),
        "open_port_keeps_four_positions": (
            open_port["all_four_q_positions_distinct"]
        ),
        "all_four_scalar_marginals_equal_fresh_n72": (
            closed["all_four_scalar_marginals_equal_hot_v0_2_2"]
        ),
        "minimum_8_gib_system_reserve_kept": (
            metrics["minimum_available_memory_bytes"]
            >= MINIMUM_AVAILABLE_MEMORY_BYTES
        ),
    }
    if not all(checks.values()):
        raise RuntimeError("hybrid SLC V4.0 execution check failed")

    unsigned = {
        "schema": "SLCV40_24_H14C_512_N72_COMPLETION_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "version_label": VERSION_LABEL,
        "execution_status": "COMPLETED",
        "result_classification": scheduler_classification,
        "scheduler_optimization_result_classification": (
            scheduler_classification
        ),
        "semantic_continuity_result_classification": (
            semantic_classification
        ),
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "N": int(instance["N"]),
        "plan": plan,
        "batch_probe_result": batch,
        "scheduler_probe_result": scheduler,
        "source_manifest": manifest,
        "operator_w_sha256": cluster["operator"]["w_sha256"],
        "linked_fixed_coefficient_sha256": recovery[
            "fixed_coefficient_sha256"
        ],
        "configuration_count": str(
            recovery["observed_configuration_count"]
        ),
        "dos": recovery["dos_rows"],
        "dos_sha256": recovery["dos_sha256"],
        "raw_moments": {
            str(key): str(value)
            for key, value in recovery["raw_moments"].items()
        },
        "fiber_execution": fiber_receipt,
        "open_port_attachment": open_port,
        "closed_n72_attachment": closed,
        "checkpoint_roster": cluster["checkpoint_roster"],
        "checkpoint_roster_sha256": cluster[
            "checkpoint_roster_sha256"
        ],
        "prime_receipt_roster": cluster["prime_receipt_roster"],
        "prime_receipt_roster_sha256": cluster[
            "prime_receipt_roster_sha256"
        ],
        "metrics": metrics,
        "comparison": comparison,
        "checks": checks,
        "total_runner_wall_seconds": time.perf_counter() - total_started,
        "environment": {
            "executable": sys.executable,
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "platform": platform.platform(),
            "logical_cpu_count": os.cpu_count(),
            "allowed_cpu_ids": sorted(os.sched_getaffinity(0)),
            "thread_environment": {
                key: os.environ.get(key)
                for key in (
                    "OPENBLAS_NUM_THREADS",
                    "OMP_NUM_THREADS",
                    "MKL_NUM_THREADS",
                )
            },
        },
    }
    completion = sealed(unsigned, "completion_sha256")
    atomic_json(COMPLETION, completion)
    result_unsigned = {
        "schema": "SLCV40_24_H14C_512_N72_RESULT_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "version_label": VERSION_LABEL,
        "execution_status": "COMPLETED",
        "result_classification": completion["result_classification"],
        "scheduler_optimization_result_classification": completion[
            "scheduler_optimization_result_classification"
        ],
        "semantic_continuity_result_classification": completion[
            "semantic_continuity_result_classification"
        ],
        "instance_id": completion["instance_id"],
        "instance_sha256": completion["instance_sha256"],
        "configuration_count": completion["configuration_count"],
        "operator_w_sha256": completion["operator_w_sha256"],
        "linked_fixed_coefficient_sha256": completion[
            "linked_fixed_coefficient_sha256"
        ],
        "plan": plan,
        "batch_probe_result_sha256": batch["result_sha256"],
        "scheduler_probe_result_sha256": scheduler["result_sha256"],
        "fiber_execution": fiber_receipt,
        "open_port_attachment": open_port,
        "closed_n72_attachment": closed,
        "metrics": metrics,
        "comparison": comparison,
        "checks": checks,
        "candidate_completion_path": str(
            COMPLETION.relative_to(QC_ROOT)
        ),
        "candidate_completion_file_sha256": sha256_file(COMPLETION),
        "candidate_completion_sha256": completion[
            "completion_sha256"
        ],
        "source_manifest_sha256": manifest["manifest_sha256"],
        "operator_result_path": str(
            OPERATOR_RESULT.relative_to(QC_ROOT)
        ),
        "operator_result_file_sha256": sha256_file(OPERATOR_RESULT),
        "total_runner_wall_seconds": completion[
            "total_runner_wall_seconds"
        ],
    }
    result = sealed(result_unsigned, "result_sha256")
    atomic_json(RESULT_JSON, result)
    RESULT_MD.write_text(render_markdown(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["execution_status"],
                "display_name": DISPLAY_NAME,
                "wall_seconds": hybrid_wall,
                "smart_wall_seconds": smart_wall,
                "hybrid_minus_smart_seconds": hybrid_wall - smart_wall,
                "peak_gib": (
                    metrics["peak_sampled_aggregate_worker_rss_bytes"]
                    / (1 << 30)
                ),
                "minimum_available_gib": (
                    metrics["minimum_available_memory_bytes"] / (1 << 30)
                ),
                "all_coefficients_equal": full_equal,
                "fiber_assignments": fiber_receipt["assignment_count"],
                "result_classification": result[
                    "result_classification"
                ],
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
