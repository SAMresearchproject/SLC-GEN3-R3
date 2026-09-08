#!/usr/bin/env python3
"""Pinned dynamic-queue worker for the SLC v0.5 H14D N72 candidate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import sys
import time
import traceback
from typing import Any, Mapping


CAMPAIGN_ID = "SLCV05_N72_H14D_T18_CANDIDATE"
CHECKPOINT_DOMAIN = "SLCV05-N72-H14D-T18-ROOT-BATCH-V1"
CHECKPOINT_SCHEMA = "SLCV05_N72_H14D_T18_ROOT_BATCH_CHECKPOINT_V1"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(canonical_bytes(value) + b"\n")
    os.replace(temporary, path)


def maximum_rss_bytes() -> int:
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def load_engine(engine_path: Path) -> Any:
    name = "slcv05_h14d_slcx032_engine"
    if name in sys.modules:
        return sys.modules[name]
    specification = importlib.util.spec_from_file_location(name, engine_path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load N72 engine: {engine_path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def validate_checkpoint(
    checkpoint: Mapping[str, Any], expected: Mapping[str, Any]
) -> None:
    unsigned = dict(checkpoint)
    observed = unsigned.pop("record_sha256", None)
    if observed != canonical_sha256(unsigned):
        raise RuntimeError("H14D checkpoint self-seal mismatch")
    if checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise RuntimeError("H14D checkpoint schema changed")
    for key, value in expected.items():
        if checkpoint.get(key) != value:
            raise RuntimeError(f"H14D checkpoint mismatch for {key}")
    root_count = int(checkpoint["root_stop"]) - int(checkpoint["root_start"])
    evaluations = checkpoint.get("evaluations")
    if (
        not isinstance(evaluations, list)
        or len(evaluations) != 16
        or any(
            not isinstance(row, list) or len(row) != root_count
            for row in evaluations
        )
    ):
        raise RuntimeError("H14D checkpoint evaluation shape changed")


def node_loop(
    node_id: str,
    cpu_id: int,
    instance: Mapping[str, Any],
    plan: Mapping[str, Any],
    task_queue: Any,
    result_queue: Any,
    checkpoint_root: str,
    engine_path: str,
    address_space_cap_bytes: int,
) -> None:
    try:
        resource.setrlimit(
            resource.RLIMIT_AS,
            (address_space_cap_bytes, address_space_cap_bytes),
        )
        os.sched_setaffinity(0, {cpu_id})
        engine = load_engine(Path(engine_path))
        ownership = engine.factor_ownership(instance)
        local_instance = engine._local_instance(instance, ownership)
        elimination_order = [int(value) for value in plan["conditional_order"]]
        port_order = [int(value) for value in plan["port_order"]]
        checkpoint_dir = Path(checkpoint_root)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        result_queue.put(
            {
                "kind": "READY",
                "node_id": node_id,
                "worker_pid": os.getpid(),
                "requested_cpu_id": cpu_id,
                "observed_affinity": sorted(os.sched_getaffinity(0)),
                "maximum_rss_bytes": maximum_rss_bytes(),
            }
        )
        while True:
            task = task_queue.get()
            if task is None:
                break
            started_wall = time.perf_counter()
            started_cpu = time.process_time()
            prime = int(task["prime"])
            root_start = int(task["root_start"])
            root_stop = int(task["root_stop"])
            points = engine._zeta_points(
                prime,
                int(plan["y_ntt_length"]),
                root_start,
                root_stop,
            )
            terminal, structural = engine.retained_port_root_batch(
                local_instance,
                elimination_order,
                points,
                prime,
                port_order,
            )
            unsigned = {
                "schema": CHECKPOINT_SCHEMA,
                "domain": CHECKPOINT_DOMAIN,
                "campaign_id": CAMPAIGN_ID,
                "plan_sha256": plan["plan_sha256"],
                "instance_sha256": instance["instance_sha256"],
                "node_id": node_id,
                "requested_cpu_id": cpu_id,
                "observed_affinity": sorted(os.sched_getaffinity(0)),
                "task_id": str(task["task_id"]),
                "prime_index": int(task["prime_index"]),
                "prime": prime,
                "scheduler_phase": "DYNAMIC_SHARED_QUEUE",
                "task_index": int(task["task_index"]),
                "root_start": root_start,
                "root_stop": root_stop,
                "evaluations": [
                    [int(value) for value in row] for row in terminal.tolist()
                ],
                "structural_metrics": {
                    key: int(value) for key, value in structural.items()
                },
                "wall_seconds": time.perf_counter() - started_wall,
                "process_cpu_seconds": time.process_time() - started_cpu,
                "maximum_rss_bytes": maximum_rss_bytes(),
            }
            checkpoint = {
                **unsigned,
                "record_sha256": canonical_sha256(unsigned),
            }
            path = checkpoint_dir / str(task["checkpoint_name"])
            if path.exists():
                raise RuntimeError("H14D checkpoint path already exists")
            atomic_json(path, checkpoint)
            result_queue.put(
                {
                    "kind": "DONE",
                    "task_id": task["task_id"],
                    "node_id": node_id,
                    "checkpoint_path": str(path),
                    "wall_seconds": checkpoint["wall_seconds"],
                    "process_cpu_seconds": checkpoint["process_cpu_seconds"],
                    "maximum_rss_bytes": checkpoint["maximum_rss_bytes"],
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


__all__ = [
    "CAMPAIGN_ID",
    "CHECKPOINT_DOMAIN",
    "CHECKPOINT_SCHEMA",
    "node_loop",
    "validate_checkpoint",
]
