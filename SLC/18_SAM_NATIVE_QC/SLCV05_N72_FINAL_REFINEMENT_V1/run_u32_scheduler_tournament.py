#!/usr/bin/env python3
"""Complete-prime tournament for exact uint32 reduced-value storage."""

from __future__ import annotations

import json
import os
from pathlib import Path
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
import run_p1_packet_tournament as packet  # noqa: E402
from native_arithmetic_u32 import NativeArithmeticU32P1  # noqa: E402
from refined_kernel_u32 import retained_port_root_p1_u32  # noqa: E402


SCHEMA = "SLCV05_N72_FINAL_REFINEMENT_U32_SCHEDULER_TOURNAMENT_V1"
WORK = HERE / "work" / "U32_SCHEDULER_TOURNAMENT"
TRIAL_ROOT = WORK / "trials"
NATIVE_ROOT = WORK / "native"
MANIFEST_PATH = WORK / "SOURCE_MANIFEST.json"
BUILD_RECEIPT = WORK / "NATIVE_BUILD_RECEIPT.json"
RESULT_PATH = HERE / "release" / "U32_SCHEDULER_TOURNAMENT_RESULT.json"
RESULT_MD = HERE / "release" / "U32_SCHEDULER_TOURNAMENT_RESULT.md"
P1_RESULT = HERE / "release" / "P1_PACKET_TOURNAMENT_RESULT.json"

CONFIGS = [
    {"config_id": "O3_C65536", "flags": [], "chunk_cap": 65536},
    {"config_id": "O3_C262144", "flags": [], "chunk_cap": 262144},
    {
        "config_id": "UNROLL_C65536",
        "flags": ["-funroll-loops"],
        "chunk_cap": 65536,
    },
    {
        "config_id": "UNROLL_C131072",
        "flags": ["-funroll-loops"],
        "chunk_cap": 131072,
    },
]


def library_path(config: Mapping[str, Any]) -> Path:
    return NATIVE_ROOT / f"libslcv05_u32_{config['config_id']}.so"


def build_libraries() -> dict[str, Any]:
    NATIVE_ROOT.mkdir(parents=True, exist_ok=False)
    rows = []
    for config in CONFIGS:
        destination = library_path(config)
        command = [
            "gcc",
            "-O3",
            "-march=native",
            *[str(value) for value in config["flags"]],
            "-std=c11",
            "-fPIC",
            "-shared",
            str(HERE / "refined_native_u32_p1.c"),
            "-o",
            str(destination),
        ]
        started = time.perf_counter()
        completed = subprocess.run(
            command, check=True, capture_output=True, text=True
        )
        rows.append(
            {
                "config_id": config["config_id"],
                "chunk_cap": config["chunk_cap"],
                "command": command,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "build_seconds": time.perf_counter() - started,
                "library_bytes": destination.stat().st_size,
                "library_sha256": base.sha256_file(destination),
            }
        )
    receipt = base.sealed(
        {
            "schema": "SLCV05_N72_U32_NATIVE_BUILD_ROSTER_V1",
            "campaign_id": base.CAMPAIGN_ID,
            "compiler": subprocess.run(
                ["gcc", "--version"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()[0],
            "source_sha256": base.sha256_file(
                HERE / "refined_native_u32_p1.c"
            ),
            "builds": rows,
        },
        "receipt_sha256",
    )
    base.atomic_json(BUILD_RECEIPT, receipt)
    return receipt


def source_manifest() -> dict[str, Any]:
    paths = [
        Path(__file__).resolve(),
        HERE / "refined_native_u32_p1.c",
        HERE / "native_arithmetic_u32.py",
        HERE / "refined_kernel_u32.py",
        HERE / "run_p1_packet_tournament.py",
        HERE / "run_scheduler_tournament.py",
        P1_RESULT,
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
            "schema": "SLCV05_N72_U32_SCHEDULER_SOURCE_MANIFEST_V1",
            "campaign_id": base.CAMPAIGN_ID,
            "sources": rows,
        },
        "manifest_sha256",
    )


def parse_chunk(native_library: str) -> int:
    marker = Path(native_library).stem.rsplit("_C", 1)
    if len(marker) != 2 or not marker[1].isdigit():
        raise RuntimeError("uint32 library name lacks its chunk cap")
    return int(marker[1])


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
            base.ENGINE_PATH, f"u32_engine_{node_id}_{os.getpid()}"
        )
        local_instance = engine._local_instance(
            instance, engine.factor_ownership(instance)
        )
        cache = base.open_cache_file(Path(cache_path), cache_descriptor)
        native = NativeArithmeticU32P1(Path(native_library))
        native.self_test([int(value) for value in plan["primes"]])
        chunk_cap = parse_chunk(native_library)
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
            if packet_stop - packet_start != 1:
                raise RuntimeError("uint32 scheduler requires singleton packets")
            points = engine._zeta_points(
                prime,
                int(plan["y_ntt_length"]),
                packet_start,
                packet_stop,
            )
            started_wall = time.perf_counter()
            started_cpu = time.process_time()
            terminal, structural = retained_port_root_p1_u32(
                engine,
                local_instance,
                order,
                points,
                prime,
                ports,
                cache,
                native,
                chunk_cap,
            )
            evaluations = [
                [int(terminal[state, 0])] for state in range(16)
            ]
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


def render(result: Mapping[str, Any]) -> str:
    selection = result["selection"]
    return "\n".join(
        [
            "# N72 exact uint32-storage scheduler tournament",
            "",
            f"- Status: `{result['execution_status']}`",
            f"- Classification: **{result['result_classification']}**",
            f"- Complete-prime trials: `{result['trial_count']}`",
            f"- Selected configuration: `{selection['config_id']}`",
            f"- Selected median wall: `{selection['median_wall_seconds']:.9f}` seconds",
            f"- H14E/selected ratio: `{result['comparison']['h14e_over_selected_ratio']:.6f}`",
            f"- Int64 P1/selected ratio: `{result['comparison']['int64_p1_over_selected_ratio']:.6f}`",
            f"- Result SHA-256: `{result['result_sha256']}`",
            "",
        ]
    )


def main() -> int:
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(key) != "1":
            raise RuntimeError(f"{key} must equal 1")
    if WORK.exists() or RESULT_PATH.exists() or RESULT_MD.exists():
        raise RuntimeError("uint32 scheduler artifacts already exist")
    WORK.mkdir(parents=True, exist_ok=False)
    TRIAL_ROOT.mkdir(parents=True, exist_ok=False)
    packet.TRIAL_ROOT = TRIAL_ROOT
    packet.worker_loop = worker_loop
    manifest = source_manifest()
    base.atomic_json(MANIFEST_PATH, manifest)
    build_receipt = build_libraries()
    p1_result = base.load_json(P1_RESULT)
    base.validate_seal(p1_result, "result_sha256")
    if p1_result.get("execution_status") != "COMPLETED":
        raise RuntimeError("int64 P1 authority changed")
    plan = base.load_json(base.H14D_PLAN)
    instance = base.load_json(base.INSTANCE_PATH)
    base.validate_seal(plan, "plan_sha256")
    engine = base.load_engine(base.ENGINE_PATH, "u32_parent_engine")
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
        tempfile.mkdtemp(prefix="slcv05_u32_cache_", dir="/tmp")
    )
    cache_path = temporary_root / "projection_cache.bin"
    cache_removed = False
    trials: list[tuple[str, dict[str, Any]]] = []
    try:
        cache_receipt = base.build_cache_file(cache_path, descriptor)
        if base.sha256_file(cache_path) != cache_receipt["cache_sha256"]:
            raise RuntimeError("uint32 cache hash changed")
        os.chmod(cache_path, 0o444)

        def execute(trial_id: str, config: Mapping[str, Any]) -> None:
            packet.NATIVE_LIBRARY = library_path(config)
            trial = packet.run_trial(
                trial_id=trial_id,
                packet_size=1,
                instance=instance,
                plan=plan,
                prime=prime,
                cache_path=cache_path,
                descriptor=descriptor,
                expected_sha256=expected_sha256,
            )
            trials.append((str(config["config_id"]), trial))

        for index, config in enumerate(CONFIGS):
            execute(f"U32_INITIAL_{index:02d}_{config['config_id']}", config)
        ranked = sorted(trials, key=lambda row: float(row[1]["kernel_wall_seconds"]))
        finalist_ids = [ranked[0][0], ranked[1][0]]
        config_by_id = {
            str(config["config_id"]): config for config in CONFIGS
        }
        for index, config_id in enumerate(
            [finalist_ids[0], finalist_ids[1], finalist_ids[1], finalist_ids[0]]
        ):
            execute(
                f"U32_CONFIRM_{index:02d}_{config_id}",
                config_by_id[config_id],
            )
    finally:
        if cache_path.exists():
            cache_path.chmod(0o644)
            cache_path.unlink()
        if temporary_root.exists():
            shutil.rmtree(temporary_root)
        cache_removed = not cache_path.exists() and not temporary_root.exists()
    observations: dict[str, list[float]] = {}
    for config_id, trial in trials:
        observations.setdefault(config_id, []).append(
            float(trial["kernel_wall_seconds"])
        )
    finalist_statistics = []
    for config_id in finalist_ids:
        values = observations[config_id]
        finalist_statistics.append(
            {
                "config_id": config_id,
                "wall_seconds": values,
                "median_wall_seconds": sorted(values)[1],
            }
        )
    finalist_statistics.sort(key=lambda row: row["median_wall_seconds"])
    winner = finalist_statistics[0]
    winner_config = next(
        config for config in CONFIGS if config["config_id"] == winner["config_id"]
    )
    selected_wall = float(winner["median_wall_seconds"])
    int64_wall = float(p1_result["selection"]["median_wall_seconds"])
    h14e_wall = float(
        p1_result["comparison"]["h14e_complete_prime_wall_seconds"]
    )
    selected_build = next(
        row
        for row in build_receipt["builds"]
        if row["config_id"] == winner["config_id"]
    )
    selection = {
        "profile_id": "H14_U32_P1_PACKET1",
        "config_id": winner["config_id"],
        "cpu_ids": packet.CPU_IDS,
        "worker_count": len(packet.CPU_IDS),
        "singleton_root_batch_size": 1,
        "queue_packet_size": 1,
        "chunk_cap": int(winner_config["chunk_cap"]),
        "compiler_flags": winner_config["flags"],
        "native_policy_id": "NATIVE_EXACT_U32_STORAGE_U64_MULTIPLY_P1",
        "library_sha256": selected_build["library_sha256"],
        "median_wall_seconds": selected_wall,
        "observed_wall_seconds": winner["wall_seconds"],
        "selection_rule": "LOWER_MEDIAN_OF_THREE_EXACT_U32_COMPLETE_PRIME_TRIALS",
    }
    checks = {
        "all_trials_exact": all(
            trial["exact_equality_with_h14e"] for _, trial in trials
        ),
        "all_workers_active": all(trial["all_workers_active"] for _, trial in trials),
        "all_reserves_maintained": all(
            trial["system_reserve_maintained"] for _, trial in trials
        ),
        "eight_complete_prime_trials": len(trials) == 8,
        "two_finalists_repeated_three_times": all(
            len(observations[config_id]) == 3 for config_id in finalist_ids
        ),
        "u32_selected_below_int64_p1": selected_wall < int64_wall,
        "cache_removed": cache_removed,
    }
    if not all(checks.values()):
        failures = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"uint32 scheduler checks failed: {failures}")
    result = base.sealed(
        {
            "schema": SCHEMA,
            "campaign_id": base.CAMPAIGN_ID,
            "execution_status": "COMPLETED",
            "result_classification": "The test result suggests strong contact with the concept.",
            "release_promoted": False,
            "p1_result_sha256": p1_result["result_sha256"],
            "manifest": manifest,
            "native_build": build_receipt,
            "initial_configs": CONFIGS,
            "finalist_ids": finalist_ids,
            "finalist_statistics": finalist_statistics,
            "selection": selection,
            "trial_count": len(trials),
            "comparison": {
                "h14e_complete_prime_wall_seconds": h14e_wall,
                "int64_p1_median_wall_seconds": int64_wall,
                "selected_median_wall_seconds": selected_wall,
                "h14e_over_selected_ratio": h14e_wall / selected_wall,
                "int64_p1_over_selected_ratio": int64_wall / selected_wall,
                "wall_reduction_from_h14e_percent": 100.0
                * (h14e_wall - selected_wall)
                / h14e_wall,
            },
            "trial_roster": [
                {
                    "config_id": config_id,
                    "trial_id": trial["trial_id"],
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
                for config_id, trial in trials
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
                "event": "U32_SCHEDULER_TOURNAMENT_COMPLETE",
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
