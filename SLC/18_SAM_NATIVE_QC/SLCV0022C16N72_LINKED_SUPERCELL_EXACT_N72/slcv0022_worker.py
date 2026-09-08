"""Persistent linked-supercell worker for Dense Exact v0.2.2 C16."""

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


CAMPAIGN_ID = "SLCV0022C16N72_LINKED_SUPERCELL_EXACT_N72"
CHECKPOINT_DOMAIN = "SLCV0022-C16-LINKED-ROOT-BATCH-V1"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(canonical_bytes(value) + b"\n")
    os.replace(temporary, path)


def maximum_rss_bytes() -> int:
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def load_engine(engine_path: Path) -> Any:
    name = "slcv0022_sealed_slcx032_engine"
    if name in sys.modules:
        return sys.modules[name]
    specification = importlib.util.spec_from_file_location(name, engine_path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load linked-supercell engine: {engine_path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def validate_checkpoint(
    checkpoint: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> None:
    unsigned = dict(checkpoint)
    observed = unsigned.pop("record_sha256", None)
    if observed != canonical_sha256(unsigned):
        raise RuntimeError("root-batch checkpoint self-seal mismatch")
    for key, value in expected.items():
        if checkpoint.get(key) != value:
            raise RuntimeError(f"root-batch checkpoint mismatch for {key}")
    evaluations = checkpoint.get("evaluations")
    root_count = int(expected["root_stop"]) - int(expected["root_start"])
    if (
        not isinstance(evaluations, list)
        or len(evaluations) != 16
        or any(
            not isinstance(row, list) or len(row) != root_count
            for row in evaluations
        )
    ):
        raise RuntimeError("root-batch checkpoint evaluation shape mismatch")


def node_loop(
    node_id: str,
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
            terminal, metrics = engine.retained_port_root_batch(
                local_instance,
                elimination_order,
                points,
                prime,
                port_order,
            )
            unsigned = {
                "schema": "SLCV0022_C16_LINKED_ROOT_BATCH_CHECKPOINT_V1",
                "domain": CHECKPOINT_DOMAIN,
                "campaign_id": CAMPAIGN_ID,
                "plan_sha256": plan["plan_sha256"],
                "instance_sha256": instance["instance_sha256"],
                "node_id": node_id,
                "prime_index": int(task["prime_index"]),
                "prime": prime,
                "wave_index": int(task["wave_index"]),
                "root_start": root_start,
                "root_stop": root_stop,
                "evaluations": [
                    [int(value) for value in row]
                    for row in terminal.tolist()
                ],
                "structural_metrics": {
                    key: int(value) for key, value in metrics.items()
                },
                "wall_seconds": time.perf_counter() - started_wall,
                "process_cpu_seconds": time.process_time() - started_cpu,
                "maximum_rss_bytes": maximum_rss_bytes(),
            }
            checkpoint = {
                **unsigned,
                "record_sha256": canonical_sha256(unsigned),
            }
            checkpoint_path = checkpoint_dir / str(task["checkpoint_name"])
            if checkpoint_path.exists():
                existing = json.loads(
                    checkpoint_path.read_text(encoding="utf-8")
                )
                validate_checkpoint(
                    existing,
                    {
                        key: unsigned[key]
                        for key in (
                            "domain",
                            "campaign_id",
                            "plan_sha256",
                            "instance_sha256",
                            "node_id",
                            "prime_index",
                            "prime",
                            "wave_index",
                            "root_start",
                            "root_stop",
                        )
                    },
                )
                if existing["evaluations"] != checkpoint["evaluations"]:
                    raise RuntimeError("existing checkpoint evaluations differ")
                checkpoint = existing
            else:
                atomic_json(checkpoint_path, checkpoint)
            result_queue.put(
                {
                    "kind": "DONE",
                    "task_id": task["task_id"],
                    "node_id": node_id,
                    "checkpoint_path": str(checkpoint_path),
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
    "atomic_json",
    "canonical_bytes",
    "canonical_sha256",
    "load_engine",
    "maximum_rss_bytes",
    "node_loop",
    "validate_checkpoint",
]
