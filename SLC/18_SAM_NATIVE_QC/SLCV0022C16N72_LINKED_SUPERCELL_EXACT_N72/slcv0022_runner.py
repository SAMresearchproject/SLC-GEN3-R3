#!/usr/bin/env python3
"""Run exact dense N72 with 16 linked-supercell workers at capacity 2^24."""

from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import queue
import sys
import time
from typing import Any, Mapping

import numpy as np


BASE = Path(__file__).resolve().parent
NATIVE_ROOT = BASE.parent
SLC_ROOT = BASE.parents[1]
V21_ROOT = (
    NATIVE_ROOT / "SLCV0021C4N72_LINKED_SUPERCELL_EXACT_N72"
)
if str(V21_ROOT) not in sys.path:
    sys.path.insert(0, str(V21_ROOT))

import slcv0021_runner as v21  # noqa: E402
import slcv0022_worker as worker  # noqa: E402


CAMPAIGN_ID = worker.CAMPAIGN_ID
VERSION_LABEL = "SLC_DENSE_EXACT_V0_2_2_C16_CAP24"
NODE_IDS = tuple(f"SLC_{index:02d}" for index in range(16))
LINKAGE_DOMAIN = "SLCV0022-C16-BALANCED-LINKAGE-V1"
MINIMUM_AVAILABLE_MEMORY_BYTES = 8 * (1 << 30)
MAXIMUM_AGGREGATE_RSS_BYTES = 12 * (1 << 30)
PER_NODE_ADDRESS_SPACE_BYTES = 6 * (1 << 30)
ROOT_BATCH_SIZE = 4
CAPACITY_EXPONENT_PER_WORKER = 24
AGGREGATE_CAPACITY_EXPONENT = 28

WORK = BASE / "work" / "N72"
RELEASE = BASE / "release"
HEARTBEAT = WORK / "HEARTBEAT.json"
COMPLETION = WORK / "CANDIDATE_COMPLETION.json"
RESULT_JSON = RELEASE / "SLCV0022C16N72_RESULT.json"
RESULT_MD = RELEASE / "SLCV0022C16N72_RESULT.md"

ENGINE_PATH = v21.ENGINE_PATH
INSTANCE_PATH = v21.INSTANCE_PATH
BASELINE_COMPLETION = v21.BASELINE_COMPLETION
BASELINE_RESULT = v21.BASELINE_RESULT
V21_COMPLETION = V21_ROOT / "work" / "N72" / "CANDIDATE_COMPLETION.json"
V21_RESULT = V21_ROOT / "release" / "SLCV0021C4N72_RESULT.json"
SLCX032_OPERATOR = v21.SLCX032_OPERATOR


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def sealed(unsigned: Mapping[str, Any], key: str) -> dict[str, Any]:
    return {**unsigned, key: worker.canonical_sha256(unsigned)}


def validate_self_seal(value: Mapping[str, Any], key: str) -> None:
    unsigned = dict(value)
    observed = unsigned.pop(key, None)
    if observed != worker.canonical_sha256(unsigned):
        raise RuntimeError(f"self-seal mismatch: {key}")


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


def meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        key, raw = line.split(":", 1)
        values[key] = int(raw.split()[0]) * 1024
    return values


def source_manifest() -> dict[str, Any]:
    paths = [
        BASE / "README.md",
        BASE / "slcv0022_worker.py",
        BASE / "slcv0022_runner.py",
        V21_ROOT / "slcv0021_worker.py",
        V21_ROOT / "slcv0021_runner.py",
        ENGINE_PATH,
        INSTANCE_PATH,
        BASELINE_COMPLETION,
        BASELINE_RESULT,
        V21_COMPLETION,
        V21_RESULT,
        SLCX032_OPERATOR,
    ]
    rows = [
        {
            "path": str(path.relative_to(SLC_ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in paths
    ]
    return sealed(
        {
            "schema": "SLCV0022_SOURCE_MANIFEST_V1",
            "campaign_id": CAMPAIGN_ID,
            "sources": rows,
        },
        "manifest_sha256",
    )


def load_inputs() -> tuple[
    Any,
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    engine, instance, baseline_completion, baseline_result = v21.load_inputs()
    v21_completion = load_json(V21_COMPLETION)
    v21_result = load_json(V21_RESULT)
    if (
        v21_completion.get("instance_sha256")
        != v21.EXPECTED_INSTANCE_SHA256
        or v21_result.get("instance_sha256")
        != v21.EXPECTED_INSTANCE_SHA256
    ):
        raise RuntimeError("v0.2.1 comparison instance differs")
    if (
        v21_completion.get("operator_w_sha256") != v21.EXPECTED_W_SHA256
        or v21_result.get("operator_w_sha256") != v21.EXPECTED_W_SHA256
    ):
        raise RuntimeError("v0.2.1 linked operator identity differs")
    return (
        engine,
        instance,
        baseline_completion,
        baseline_result,
        v21_completion,
        v21_result,
    )


def build_plan(engine: Any, instance: Mapping[str, Any]) -> dict[str, Any]:
    freeze = engine.load_port_freeze()
    ownership = engine.factor_ownership(instance)
    tasks_per_prime = int(engine.W_Y_LENGTH // ROOT_BATCH_SIZE)
    waves_per_prime = tasks_per_prime // len(NODE_IDS)
    unsigned = {
        "schema": "SLCV0022_C16_LINKED_SUPERCELL_PLAN_V1",
        "campaign_id": CAMPAIGN_ID,
        "version_label": VERSION_LABEL,
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "cluster_size": len(NODE_IDS),
        "node_ids": list(NODE_IDS),
        "numerical_object": "SLCX032_FOUR_BIT_LINKED_SUPERCELL_OPERATOR",
        "scale_delta": "C4_BATCH2_TO_C16_BATCH4",
        "port_order": [int(value) for value in engine.PORT_ORDER],
        "cut_edges": ownership["cut_edges"],
        "conditional_order": [
            int(value) for value in freeze["conditional_order"]
        ],
        "conditional_induced_width": int(
            freeze["conditional_induced_width"]
        ),
        "y_ntt_length": int(engine.W_Y_LENGTH),
        "z_root_order": 2 * int(engine.W_Y_LENGTH),
        "root_batch_size": ROOT_BATCH_SIZE,
        "retained_capacity_exponent_per_worker": (
            CAPACITY_EXPONENT_PER_WORKER
        ),
        "aggregate_sharded_capacity_exponent": (
            AGGREGATE_CAPACITY_EXPONENT
        ),
        "primes": [int(value) for value in engine.PRIMES_3],
        "tasks_per_prime": tasks_per_prime,
        "waves_per_prime": waves_per_prime,
        "total_task_count": tasks_per_prime * len(engine.PRIMES_3),
        "total_wave_count": waves_per_prime * len(engine.PRIMES_3),
        "linkage_receipt_tree": "BALANCED_BINARY_16_TO_8_TO_4_TO_2_TO_1",
        "minimum_available_memory_bytes": (
            MINIMUM_AVAILABLE_MEMORY_BYTES
        ),
        "excluded_changes": [
            "W10",
            "FULL_Q_512_BY_512",
            "CUTSET_BRANCHING",
            "GLOBAL_SPIN_GAUGE",
            "FOURTH_CRT_PRIME",
            "CAPACITY29_PROFILE",
            "COMPACT_STAGE4C_GRAPH",
        ],
    }
    if (
        unsigned["conditional_induced_width"] != 22
        or unsigned["port_order"] != [6, 15, 16, 58]
        or unsigned["root_batch_size"] != 4
        or unsigned["cluster_size"] != 16
        or unsigned["tasks_per_prime"] != 128
        or unsigned["waves_per_prime"] != 8
        or unsigned["total_task_count"] != 384
        or unsigned["total_wave_count"] != 24
    ):
        raise RuntimeError("C16 capacity-24 plan differs")
    return sealed(unsigned, "plan_sha256")


def checkpoint_expected(
    *,
    plan: Mapping[str, Any],
    instance: Mapping[str, Any],
    node_id: str,
    prime_index: int,
    prime: int,
    wave_index: int,
    root_start: int,
    root_stop: int,
) -> dict[str, Any]:
    return {
        "domain": worker.CHECKPOINT_DOMAIN,
        "campaign_id": CAMPAIGN_ID,
        "plan_sha256": plan["plan_sha256"],
        "instance_sha256": instance["instance_sha256"],
        "node_id": node_id,
        "prime_index": prime_index,
        "prime": prime,
        "wave_index": wave_index,
        "root_start": root_start,
        "root_stop": root_stop,
    }


def balanced_tree(
    leaves: list[str],
    *,
    plan_sha256: str,
    instance_sha256: str,
    prime_index: int,
    wave_index: int,
) -> tuple[list[list[str]], str]:
    if len(leaves) != 16:
        raise RuntimeError("balanced linkage requires sixteen leaves")
    levels: list[list[str]] = []
    current = list(leaves)
    depth = 0
    while len(current) > 1:
        if len(current) & 1:
            raise RuntimeError("balanced linkage level has odd cardinality")
        following = [
            worker.canonical_sha256(
                {
                    "domain": LINKAGE_DOMAIN,
                    "plan_sha256": plan_sha256,
                    "instance_sha256": instance_sha256,
                    "prime_index": prime_index,
                    "wave_index": wave_index,
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


def balanced_linkage_receipt(
    *,
    plan: Mapping[str, Any],
    instance: Mapping[str, Any],
    prime_index: int,
    wave_index: int,
    checkpoints: list[Mapping[str, Any]],
) -> dict[str, Any]:
    by_node = {str(row["node_id"]): row for row in checkpoints}
    if set(by_node) != set(NODE_IDS):
        raise RuntimeError("balanced linkage wave lacks a worker")
    leaves = [
        str(by_node[node_id]["record_sha256"]) for node_id in NODE_IDS
    ]
    levels, root = balanced_tree(
        leaves,
        plan_sha256=str(plan["plan_sha256"]),
        instance_sha256=str(instance["instance_sha256"]),
        prime_index=prime_index,
        wave_index=wave_index,
    )
    return sealed(
        {
            "schema": "SLCV0022_BALANCED_C16_LINKAGE_V1",
            "domain": LINKAGE_DOMAIN,
            "campaign_id": CAMPAIGN_ID,
            "plan_sha256": plan["plan_sha256"],
            "instance_sha256": instance["instance_sha256"],
            "prime_index": prime_index,
            "wave_index": wave_index,
            "node_ids": list(NODE_IDS),
            "leaves": leaves,
            "levels": levels,
            "root_sha256": root,
        },
        "receipt_sha256",
    )


def validate_linkage_receipt(receipt: Mapping[str, Any]) -> None:
    validate_self_seal(receipt, "receipt_sha256")
    if receipt.get("node_ids") != list(NODE_IDS):
        raise RuntimeError("balanced linkage worker roster changed")
    leaves = receipt.get("leaves")
    if not isinstance(leaves, list) or len(leaves) != 16:
        raise RuntimeError("balanced linkage leaves changed")
    levels, root = balanced_tree(
        [str(value) for value in leaves],
        plan_sha256=str(receipt["plan_sha256"]),
        instance_sha256=str(receipt["instance_sha256"]),
        prime_index=int(receipt["prime_index"]),
        wave_index=int(receipt["wave_index"]),
    )
    if receipt.get("levels") != levels or receipt.get("root_sha256") != root:
        raise RuntimeError("balanced linkage receipt changed")


def write_heartbeat(payload: Mapping[str, Any]) -> None:
    unsigned = {
        "schema": "SLCV0022_HEARTBEAT_V1",
        "campaign_id": CAMPAIGN_ID,
        "updated_unix": time.time(),
        **dict(payload),
    }
    worker.atomic_json(HEARTBEAT, sealed(unsigned, "heartbeat_sha256"))


def fixed_from_dos(
    rows: list[Mapping[str, Any]],
    bound: int = 435,
) -> list[int]:
    fixed = [0] * (2 * bound + 1)
    for row in rows:
        fixed[int(row["energy"]) + bound] = int(row["count"])
    return fixed


def execute_cluster(
    engine: Any,
    instance: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    memory_before = meminfo()
    if memory_before["MemAvailable"] < MINIMUM_AVAILABLE_MEMORY_BYTES:
        raise RuntimeError("8 GiB system-memory reserve is unavailable")
    context = mp.get_context("spawn")
    result_queue = context.Queue()
    task_queues = {node_id: context.Queue() for node_id in NODE_IDS}
    checkpoint_roots = {
        node_id: WORK / node_id / "checkpoints" for node_id in NODE_IDS
    }
    for path in checkpoint_roots.values():
        path.mkdir(parents=True, exist_ok=True)
    processes = {
        node_id: context.Process(
            target=worker.node_loop,
            args=(
                node_id,
                instance,
                plan,
                task_queues[node_id],
                result_queue,
                str(checkpoint_roots[node_id]),
                str(ENGINE_PATH),
                PER_NODE_ADDRESS_SPACE_BYTES,
            ),
            name=f"SLCV0022-{node_id}",
        )
        for node_id in NODE_IDS
    }
    started = time.perf_counter()
    for process in processes.values():
        process.start()

    pids: dict[str, int] = {}
    peak_aggregate_rss = 0
    minimum_available = memory_before["MemAvailable"]
    maximum_active_nodes = 0
    worker_peaks = {node_id: 0 for node_id in NODE_IDS}
    worker_wall = {node_id: 0.0 for node_id in NODE_IDS}
    worker_cpu = 0.0
    executed_tasks = 0
    reused_tasks = 0
    checkpoint_roster: list[dict[str, Any]] = []
    linkage_roster: list[dict[str, Any]] = []
    modular_coefficients: list[list[list[int]]] = []
    structural_metrics: dict[str, int] = {}
    last_heartbeat = 0.0

    def sample_resources() -> None:
        nonlocal peak_aggregate_rss
        nonlocal minimum_available
        nonlocal maximum_active_nodes
        rss = {
            node_id: pid_rss_bytes(pid) for node_id, pid in pids.items()
        }
        peak_aggregate_rss = max(peak_aggregate_rss, sum(rss.values()))
        maximum_active_nodes = max(
            maximum_active_nodes,
            sum(value > 0 for value in rss.values()),
        )
        available = meminfo()["MemAvailable"]
        minimum_available = min(minimum_available, available)
        if peak_aggregate_rss > MAXIMUM_AGGREGATE_RSS_BYTES:
            raise RuntimeError("aggregate worker RSS crossed 12 GiB")
        if available < MINIMUM_AVAILABLE_MEMORY_BYTES:
            raise RuntimeError("run crossed the 8 GiB system-memory reserve")

    try:
        while len(pids) < len(NODE_IDS):
            message = result_queue.get(timeout=120)
            if message.get("kind") == "ERROR":
                raise RuntimeError(
                    f"{message.get('node_id')} startup error: "
                    f"{message.get('error')}\n{message.get('traceback')}"
                )
            if message.get("kind") != "READY":
                raise RuntimeError("unexpected message before readiness")
            node_id = str(message["node_id"])
            pids[node_id] = int(message["worker_pid"])
            worker_peaks[node_id] = int(message["maximum_rss_bytes"])
        sample_resources()

        y_length = int(plan["y_ntt_length"])
        root_batch = int(plan["root_batch_size"])
        for prime_index, prime in enumerate(plan["primes"]):
            evaluations = np.zeros((16, y_length), dtype=np.int64)
            roots = list(range(0, y_length, root_batch))
            for wave_index, offset in enumerate(
                range(0, len(roots), len(NODE_IDS))
            ):
                wave_roots = roots[offset : offset + len(NODE_IDS)]
                if len(wave_roots) != len(NODE_IDS):
                    raise RuntimeError("partial sixteen-worker wave")
                records: dict[str, dict[str, Any]] = {}
                pending: set[str] = set()
                for node_id, root_start in zip(NODE_IDS, wave_roots):
                    root_stop = root_start + root_batch
                    checkpoint_name = (
                        f"prime_{prime_index:02d}_wave_{wave_index:03d}_"
                        f"roots_{root_start:04d}_{root_stop:04d}.json"
                    )
                    checkpoint_path = (
                        checkpoint_roots[node_id] / checkpoint_name
                    )
                    expected = checkpoint_expected(
                        plan=plan,
                        instance=instance,
                        node_id=node_id,
                        prime_index=prime_index,
                        prime=int(prime),
                        wave_index=wave_index,
                        root_start=root_start,
                        root_stop=root_stop,
                    )
                    if checkpoint_path.exists():
                        checkpoint = load_json(checkpoint_path)
                        worker.validate_checkpoint(checkpoint, expected)
                        records[node_id] = checkpoint
                        reused_tasks += 1
                    else:
                        task_id = (
                            f"p{prime_index:02d}w{wave_index:03d}{node_id}"
                        )
                        task_queues[node_id].put(
                            {
                                "task_id": task_id,
                                "prime_index": prime_index,
                                "prime": int(prime),
                                "wave_index": wave_index,
                                "root_start": root_start,
                                "root_stop": root_stop,
                                "checkpoint_name": checkpoint_name,
                            }
                        )
                        pending.add(task_id)

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
                                    "phase": "C16_LINKED_OPERATOR",
                                    "prime_index": prime_index,
                                    "prime_count": len(plan["primes"]),
                                    "wave_index": wave_index,
                                    "waves_per_prime": plan[
                                        "waves_per_prime"
                                    ],
                                    "pending_nodes": len(pending),
                                    "executed_task_count": executed_tasks,
                                    "reused_task_count": reused_tasks,
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
                                        "wave": (
                                            f"{wave_index + 1}/"
                                            f"{plan['waves_per_prime']}"
                                        ),
                                        "pending": len(pending),
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
                                "worker exited during an active wave"
                            )
                        continue
                    if message.get("kind") == "ERROR":
                        raise RuntimeError(
                            f"{message.get('node_id')} error: "
                            f"{message.get('error')}\n"
                            f"{message.get('traceback')}"
                        )
                    if message.get("kind") != "DONE":
                        raise RuntimeError("unexpected worker message")
                    task_id = str(message["task_id"])
                    if task_id not in pending:
                        raise RuntimeError(
                            "unexpected or duplicate task completion"
                        )
                    pending.remove(task_id)
                    node_id = str(message["node_id"])
                    checkpoint = load_json(
                        Path(str(message["checkpoint_path"]))
                    )
                    expected = checkpoint_expected(
                        plan=plan,
                        instance=instance,
                        node_id=node_id,
                        prime_index=prime_index,
                        prime=int(prime),
                        wave_index=wave_index,
                        root_start=int(checkpoint["root_start"]),
                        root_stop=int(checkpoint["root_stop"]),
                    )
                    worker.validate_checkpoint(checkpoint, expected)
                    records[node_id] = checkpoint
                    executed_tasks += 1
                    worker_cpu += float(message["process_cpu_seconds"])
                    worker_wall[node_id] += float(message["wall_seconds"])
                    worker_peaks[node_id] = max(
                        worker_peaks[node_id],
                        int(message["maximum_rss_bytes"]),
                    )
                    sample_resources()

                ordered = [records[node_id] for node_id in NODE_IDS]
                covered = [
                    root
                    for checkpoint in ordered
                    for root in range(
                        int(checkpoint["root_start"]),
                        int(checkpoint["root_stop"]),
                    )
                ]
                expected_roots = list(
                    range(
                        wave_roots[0],
                        wave_roots[0]
                        + len(NODE_IDS) * root_batch,
                    )
                )
                if covered != expected_roots:
                    raise RuntimeError("wave root coverage changed")
                for checkpoint in ordered:
                    start = int(checkpoint["root_start"])
                    stop = int(checkpoint["root_stop"])
                    evaluations[:, start:stop] = np.asarray(
                        checkpoint["evaluations"],
                        dtype=np.int64,
                    )
                    checkpoint_roster.append(
                        {
                            "node_id": checkpoint["node_id"],
                            "prime_index": prime_index,
                            "wave_index": wave_index,
                            "root_start": start,
                            "root_stop": stop,
                            "record_sha256": checkpoint["record_sha256"],
                        }
                    )
                    for key, value in checkpoint[
                        "structural_metrics"
                    ].items():
                        if key.startswith("sum_"):
                            if (
                                key in structural_metrics
                                and structural_metrics[key] != int(value)
                            ):
                                raise RuntimeError(
                                    "structural work changed across tasks"
                                )
                            structural_metrics[key] = int(value)
                        else:
                            structural_metrics[key] = max(
                                structural_metrics.get(key, 0),
                                int(value),
                            )

                receipt = balanced_linkage_receipt(
                    plan=plan,
                    instance=instance,
                    prime_index=prime_index,
                    wave_index=wave_index,
                    checkpoints=ordered,
                )
                validate_linkage_receipt(receipt)
                receipt_path = (
                    WORK
                    / "linkage"
                    / f"prime_{prime_index:02d}_wave_{wave_index:03d}.json"
                )
                if receipt_path.exists():
                    existing = load_json(receipt_path)
                    validate_linkage_receipt(existing)
                    if existing != receipt:
                        raise RuntimeError(
                            "existing balanced linkage receipt differs"
                        )
                else:
                    worker.atomic_json(receipt_path, receipt)
                linkage_roster.append(
                    {
                        "prime_index": prime_index,
                        "wave_index": wave_index,
                        "receipt_sha256": receipt["receipt_sha256"],
                        "root_sha256": receipt["root_sha256"],
                    }
                )

            exact = engine._modules()[1]
            modular_coefficients.append(
                [
                    [
                        int(value)
                        for value in exact._inverse_ntt(
                            evaluations[state, :].tolist(),
                            int(prime),
                        )
                    ]
                    for state in range(16)
                ]
            )
    finally:
        for node_id in NODE_IDS:
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
    w_coefficients: list[list[int]] = []
    expected_row_sum = 1 << (
        int(instance["N"]) - len(plan["port_order"])
    )
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
            raise RuntimeError("linked operator has support above local bound")
        active = row[: local_bound + 1]
        if any(value < 0 for value in active):
            raise RuntimeError("linked operator has a negative coefficient")
        if sum(active) != expected_row_sum:
            raise RuntimeError("linked operator row normalization changed")
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
        "port_freeze_sha256": engine.load_port_freeze()["freeze_sha256"],
        "port_order": list(plan["port_order"]),
        "cut_edges": ownership["cut_edges"],
        "orientation": [list(edge) for edge in engine.CUT_ENDPOINTS],
        "factor_ownership": ownership,
        "w_coefficients": w_coefficients,
        "w_sha256": worker.canonical_sha256(w_coefficients),
        "local_y_degree": local_bound,
        "expected_row_sum": expected_row_sum,
        "row_sums": [sum(row) for row in w_coefficients],
        "glue_y_degrees": glue,
        "glue_y_degrees_sha256": worker.canonical_sha256(glue),
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
            "conditional_order_sha256": worker.canonical_sha256(
                plan["conditional_order"]
            ),
            **structural_metrics,
        },
    }
    if operator["w_sha256"] != v21.EXPECTED_W_SHA256:
        raise RuntimeError("compiled linked operator identity differs")
    recovery = engine.recover_n72_one_cell(operator)
    if recovery["fixed_coefficient_sha256"] != v21.EXPECTED_FIXED_SHA256:
        raise RuntimeError("linked one-cell closure identity differs")
    memory_after = meminfo()
    if maximum_active_nodes != len(NODE_IDS):
        raise RuntimeError("all sixteen workers were not observed")
    return {
        "operator": operator,
        "recovery": recovery,
        "checkpoint_roster": checkpoint_roster,
        "checkpoint_roster_sha256": worker.canonical_sha256(
            checkpoint_roster
        ),
        "linkage_roster": linkage_roster,
        "linkage_roster_sha256": worker.canonical_sha256(linkage_roster),
        "metrics": {
            "wall_seconds_this_invocation": time.perf_counter() - started,
            "sum_worker_cpu_seconds": worker_cpu,
            "worker_wall_seconds_by_node": worker_wall,
            "executed_task_count": executed_tasks,
            "reused_task_count": reused_tasks,
            "total_task_count": len(checkpoint_roster),
            "wave_count": len(linkage_roster),
            "worker_pids": pids,
            "worker_peak_rss_bytes_by_node": worker_peaks,
            "sum_node_peak_rss_bytes": sum(worker_peaks.values()),
            "peak_sampled_aggregate_worker_rss_bytes": peak_aggregate_rss,
            "maximum_active_nodes": maximum_active_nodes,
            "available_memory_before_bytes": memory_before["MemAvailable"],
            "minimum_available_memory_bytes": minimum_available,
            "available_memory_after_bytes": memory_after["MemAvailable"],
            "swap_free_before_bytes": memory_before["SwapFree"],
            "swap_free_after_bytes": memory_after["SwapFree"],
        },
    }


def markdown(result: Mapping[str, Any]) -> str:
    metrics = result["metrics"]
    comparison = result["comparison"]
    return "\n".join(
        [
            "# Dense Exact v0.2.2 C16 capacity-24 N72 result",
            "",
            (
                "Result classification: "
                f"**{result['result_classification']}**"
            ),
            "",
            f"- Exact dense instance: `{result['instance_id']}`",
            "- Linked numerical object: SLCX032 four-bit supercell",
            "- Worker group: **16**",
            "- Retained capacity per worker: **2^24**",
            "- Aggregate sharded capacity: **2^28**",
            "- Root batch: **4**",
            f"- Root checkpoints: **{metrics['total_task_count']}/384**",
            f"- Balanced C16 waves: **{metrics['wave_count']}/24**",
            (
                "- Full 871-position coefficient equality: "
                f"**{comparison['full_coefficient_equality']}**"
            ),
            f"- Configuration count: **{result['configuration_count']}**",
            f"- Wall time: **{metrics['wall_seconds_this_invocation']:.6f} s**",
            (
                "- Peak sampled aggregate worker RSS: "
                f"**{metrics['peak_sampled_aggregate_worker_rss_bytes']} bytes**"
            ),
            (
                "- Minimum available memory: "
                f"**{metrics['minimum_available_memory_bytes']} bytes**"
            ),
            (
                "- Speed relative to v0.2: "
                f"**{comparison['v0_2_over_v0_2_2_speed_ratio']:.6f}x**"
            ),
            (
                "- Speed relative to v0.2.1: "
                f"**{comparison['v0_2_1_over_v0_2_2_speed_ratio']:.6f}x**"
            ),
            (
                "- Memory relative to v0.2: "
                f"**{comparison['v0_2_2_over_v0_2_memory_ratio']:.6f}**"
            ),
            "",
            (
                "No W10, 512 fiber, cutset, gauge, fourth prime, "
                "capacity-29 profile, or compact Stage4C graph was active."
            ),
            "",
        ]
    )


def main() -> int:
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError(f"{key} must equal 1")
    (
        engine,
        instance,
        baseline_completion,
        baseline_result,
        v21_completion,
        v21_result,
    ) = load_inputs()
    plan = build_plan(engine, instance)
    manifest = source_manifest()
    WORK.mkdir(parents=True, exist_ok=True)
    RELEASE.mkdir(parents=True, exist_ok=True)
    worker.atomic_json(WORK / "SOURCE_MANIFEST.json", manifest)
    worker.atomic_json(WORK / "EXECUTION_PLAN.json", plan)

    cluster = execute_cluster(engine, instance, plan)
    recovery = cluster["recovery"]
    candidate_fixed = [
        int(value) for value in recovery["fixed_coefficients"]
    ]
    baseline_fixed = fixed_from_dos(baseline_completion["dos"])
    v21_fixed = fixed_from_dos(v21_completion["dos"])
    differences_v2 = [
        index - 435
        for index, (candidate, baseline) in enumerate(
            zip(candidate_fixed, baseline_fixed)
        )
        if candidate != baseline
    ]
    differences_v21 = [
        index - 435
        for index, (candidate, previous) in enumerate(
            zip(candidate_fixed, v21_fixed)
        )
        if candidate != previous
    ]
    if differences_v2 or differences_v21:
        raise RuntimeError("C16 linked N72 coefficient comparison differs")

    metrics = cluster["metrics"]
    v2_metrics = baseline_result["cluster_metrics"]
    v21_metrics = v21_result["metrics"]
    v2_wall = float(v2_metrics["wall_seconds_this_invocation"])
    v21_wall = float(v21_metrics["wall_seconds_this_invocation"])
    new_wall = float(metrics["wall_seconds_this_invocation"])
    v2_memory = int(
        v2_metrics["peak_sampled_aggregate_worker_rss_bytes"]
    )
    v21_memory = int(
        v21_metrics["peak_sampled_aggregate_worker_rss_bytes"]
    )
    new_memory = int(metrics["peak_sampled_aggregate_worker_rss_bytes"])
    comparison = {
        "fixed_domain": [-435, 435],
        "coefficient_count": 871,
        "difference_count_vs_v0_2": len(differences_v2),
        "difference_count_vs_v0_2_1": len(differences_v21),
        "full_coefficient_equality": (
            not differences_v2 and not differences_v21
        ),
        "v0_2_wall_seconds": v2_wall,
        "v0_2_1_wall_seconds": v21_wall,
        "v0_2_2_wall_seconds": new_wall,
        "v0_2_over_v0_2_2_speed_ratio": v2_wall / new_wall,
        "v0_2_1_over_v0_2_2_speed_ratio": v21_wall / new_wall,
        "v0_2_2_over_v0_2_wall_ratio": new_wall / v2_wall,
        "v0_2_2_over_v0_2_1_wall_ratio": new_wall / v21_wall,
        "v0_2_peak_sampled_aggregate_worker_rss_bytes": v2_memory,
        "v0_2_1_peak_sampled_aggregate_worker_rss_bytes": v21_memory,
        "v0_2_2_peak_sampled_aggregate_worker_rss_bytes": new_memory,
        "v0_2_2_over_v0_2_memory_ratio": new_memory / v2_memory,
        "v0_2_2_over_v0_2_1_memory_ratio": new_memory / v21_memory,
    }
    candidate = sealed(
        {
            "schema": "SLCV0022_C16_LINKED_N72_COMPLETION_V1",
            "campaign_id": CAMPAIGN_ID,
            "version_label": VERSION_LABEL,
            "status": "COMPLETED",
            "result_classification": (
                "The test result suggests strong contact with the concept."
            ),
            "instance_id": instance["instance_id"],
            "instance_sha256": instance["instance_sha256"],
            "N": int(instance["N"]),
            "plan": plan,
            "source_manifest": manifest,
            "operator_w_sha256": cluster["operator"]["w_sha256"],
            "linked_fixed_coefficient_sha256": recovery[
                "fixed_coefficient_sha256"
            ],
            "dos": recovery["dos_rows"],
            "dos_sha256": recovery["dos_sha256"],
            "configuration_count": str(
                recovery["observed_configuration_count"]
            ),
            "raw_moments": {
                str(key): str(value)
                for key, value in recovery["raw_moments"].items()
            },
            "checkpoint_roster": cluster["checkpoint_roster"],
            "checkpoint_roster_sha256": cluster[
                "checkpoint_roster_sha256"
            ],
            "linkage_roster": cluster["linkage_roster"],
            "linkage_roster_sha256": cluster["linkage_roster_sha256"],
            "metrics": metrics,
            "comparison": comparison,
            "environment": {
                "executable": sys.executable,
                "python": sys.version.split()[0],
                "numpy": np.__version__,
                "platform": platform.platform(),
                "logical_cpu_count": os.cpu_count(),
                "thread_environment": {
                    key: os.environ.get(key)
                    for key in (
                        "OPENBLAS_NUM_THREADS",
                        "OMP_NUM_THREADS",
                        "MKL_NUM_THREADS",
                    )
                },
            },
        },
        "candidate_completion_sha256",
    )
    worker.atomic_json(COMPLETION, candidate)
    result = sealed(
        {
            "schema": "SLCV0022C16N72_RESULT_V1",
            "campaign_id": CAMPAIGN_ID,
            "version_label": VERSION_LABEL,
            "execution_status": "COMPLETED",
            "result_classification": candidate["result_classification"],
            "instance_id": instance["instance_id"],
            "instance_sha256": instance["instance_sha256"],
            "configuration_count": candidate["configuration_count"],
            "operator_w_sha256": candidate["operator_w_sha256"],
            "linked_fixed_coefficient_sha256": candidate[
                "linked_fixed_coefficient_sha256"
            ],
            "plan": plan,
            "metrics": metrics,
            "comparison": comparison,
            "candidate_completion_path": str(
                COMPLETION.relative_to(SLC_ROOT)
            ),
            "candidate_completion_file_sha256": sha256_file(COMPLETION),
            "candidate_completion_sha256": candidate[
                "candidate_completion_sha256"
            ],
            "source_manifest_sha256": manifest["manifest_sha256"],
        },
        "result_sha256",
    )
    worker.atomic_json(RESULT_JSON, result)
    RESULT_MD.write_text(markdown(result), encoding="utf-8")
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
