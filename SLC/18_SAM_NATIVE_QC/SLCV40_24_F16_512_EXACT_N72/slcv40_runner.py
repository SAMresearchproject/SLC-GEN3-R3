#!/usr/bin/env python3
"""Frozen SLCV4.0-24-F16-512 exact N72 execution."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
from typing import Any, Mapping

import numpy as np


CAMPAIGN_ID = "SLCV40_24_F16_512_EXACT_N72"
DISPLAY_NAME = "SLCV4.0-24-F16-512"
VERSION_LABEL = "SLCV4.0-24-F16-512"
LINKAGE_DOMAIN = "SLCV40-24-F16-512-BALANCED-LINKAGE-V1"

HERE = Path(__file__).resolve().parent
QC_ROOT = HERE.parent
V22_ROOT = QC_ROOT / "SLCV0022C16N72_LINKED_SUPERCELL_EXACT_N72"
V21_ROOT = QC_ROOT / "SLCV0021C4N72_LINKED_SUPERCELL_EXACT_N72"
V4_DEV_ROOT = QC_ROOT / "SLCV004C16N72_LINKED_ACTIVE_512_FIBER"
V31_ROOT = QC_ROOT / "SLCV0031_DENSE_EXACT_FULL_Q_STAGE4_N72"
X32_ROOT = (
    QC_ROOT
    / "SLCX032_EXACT_N72_SUPERCELL_N144_DAISY_CHAIN_DISCOVERY"
)

CONTRACT = HERE / "SLCV4.0-24-F16-512_CONTRACT.json"
WORK = HERE / "work" / "N72"
RELEASE = HERE / "release"
HEARTBEAT = WORK / "HEARTBEAT.json"
COMPLETION = WORK / "CANDIDATE_COMPLETION.json"
OPERATOR_RESULT = WORK / "LINKED_OPERATOR.json"
RESULT_JSON = RELEASE / "SLCV4.0-24-F16-512_RESULT.json"
RESULT_MD = RELEASE / "SLCV4.0-24-F16-512_RESULT.md"

HOT_COMPLETION = V22_ROOT / "work" / "N72" / "CANDIDATE_COMPLETION.json"
HOT_RESULT = V22_ROOT / "release" / "SLCV0022C16N72_RESULT.json"
FIBER_PROBE_RESULT = (
    V4_DEV_ROOT / "release" / "SLCV004_FIBER_PROBE_RESULT.json"
)
TOPOLOGY_DECISION = (
    V4_DEV_ROOT / "release" / "SLCV004_CLUSTER_TOPOLOGY_DECISION.md"
)
TOPOLOGY_R1_RESULT = (
    V4_DEV_ROOT / "release" / "SLCV004_CLUSTER_TOPOLOGY_PROBE_RESULT.json"
)
TOPOLOGY_R2_RESULT = (
    V4_DEV_ROOT
    / "release"
    / "SLCV004_CLUSTER_TOPOLOGY_CONFIRMATION_R2_RESULT.json"
)

EXPECTED_FILE_SHA256 = {
    V22_ROOT / "slcv0022_runner.py": (
        "9fd41c9f960d4e18544e687fb3debe8c043f88f1cd4ceba3ac7227469383c495"
    ),
    V22_ROOT / "slcv0022_worker.py": (
        "f64b560512ff3b71cd3808c3fa07849cf8ad7514f152c00add13e40c6fa4fa75"
    ),
    X32_ROOT / "slcx032_engine.py": (
        "af744a255d0459e9100e13c9ea77a88e85686bbd5910ccc15eee480030e13d78"
    ),
    V31_ROOT / "slcv0031_w10.py": (
        "7727ae43483c305d7a31a3727aa0357ea06c4cb35c6c9c58faaea2d181598ccf"
    ),
    V4_DEV_ROOT / "slcv004_fiber_probe.py": (
        "658af6a7f7b68588c194530c922b0b1f798c3aac5398cb027e6d59b9aa2e1cf8"
    ),
    HOT_COMPLETION: (
        "07a2a1d043702c707139e166abb59919e4a59e142c7abc6caed87ef85d0d2dc5"
    ),
    HOT_RESULT: (
        "c985fe38f2901facf09b9e0aa6ac6c6360bc4e6a64d66aea0e0b1f54f2178ee4"
    ),
    FIBER_PROBE_RESULT: (
        "204165c28ef2bbc58bb5406147ee28f07c703530d6cee8cc4c520c711a072f22"
    ),
    TOPOLOGY_DECISION: (
        "445d960e90f6898d90f95c2215773dc8a9ccea1ef547eaee03f3f11fab58caaa"
    ),
    TOPOLOGY_R1_RESULT: (
        "0472530c5e0540860973f806821d66937ffaa71ab0d8d0248b72394fd4a52571"
    ),
    TOPOLOGY_R2_RESULT: (
        "0c1b88d629f3a27efb59ded0f95ee08ca96004cfa2bffb4e9657c8ed0dd06503"
    ),
}

EXPECTED_INSTANCE_SHA256 = (
    "396778a771378af50f7f6cbe594d93245fb0b653aef3f7a91b142c1e51fe450b"
)
EXPECTED_OPERATOR_SHA256 = (
    "13f315ddb0f1a9f19e992f1209a2090b5a604704c48ab549aff98e89073cda50"
)
EXPECTED_FIXED_SHA256 = (
    "06c8e85ea8deca940be49190b91d8f5a028338a4b1add1c62256e22017f2c353"
)
EXPECTED_FIBER_RESULT_SHA256 = (
    "71b3ab762cae692607843ce7eff75d4e6e9a07da385314face861128e55c7ab4"
)
EXPECTED_TOPOLOGY_R1_SHA256 = (
    "3075f4be1a71a34ebc50c93ee133a3b35ad18e68fc667ed1f1932d2e27ce4bfb"
)
EXPECTED_TOPOLOGY_R2_SHA256 = (
    "bc53c3e5962b0db57ef360c3fbbcbf89390861e475615cffe0180571860a86cd"
)

for module_path in (V22_ROOT, V21_ROOT, V4_DEV_ROOT, V31_ROOT):
    text = str(module_path)
    if text not in sys.path:
        sys.path.insert(0, text)

import slcv0022_runner as hot_runner  # noqa: E402
import slcv0022_worker as hot_worker  # noqa: E402
import slcv004_fiber_probe as fiber_engine  # noqa: E402


def configure_hot_spine() -> None:
    hot_runner.CAMPAIGN_ID = CAMPAIGN_ID
    hot_runner.VERSION_LABEL = VERSION_LABEL
    hot_runner.BASE = HERE
    hot_runner.WORK = WORK
    hot_runner.RELEASE = RELEASE
    hot_runner.HEARTBEAT = HEARTBEAT
    hot_runner.COMPLETION = COMPLETION
    hot_runner.RESULT_JSON = RESULT_JSON
    hot_runner.RESULT_MD = RESULT_MD
    hot_runner.LINKAGE_DOMAIN = LINKAGE_DOMAIN
    hot_runner.NODE_IDS = tuple(f"SLC_{index:02d}" for index in range(16))
    hot_runner.worker.CAMPAIGN_ID = CAMPAIGN_ID
    hot_runner.worker.CHECKPOINT_DOMAIN = (
        "SLCV40-24-F16-512-LINKED-ROOT-BATCH-V1"
    )
    hot_worker.CAMPAIGN_ID = CAMPAIGN_ID
    hot_worker.CHECKPOINT_DOMAIN = (
        "SLCV40-24-F16-512-LINKED-ROOT-BATCH-V1"
    )


configure_hot_spine()


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


def check_locked_sources() -> None:
    for path, expected in EXPECTED_FILE_SHA256.items():
        if sha256_file(path) != expected:
            raise RuntimeError(f"locked source identity changed: {path}")
    if (
        load_json(FIBER_PROBE_RESULT).get("result_sha256")
        != EXPECTED_FIBER_RESULT_SHA256
        or load_json(TOPOLOGY_R1_RESULT).get("result_sha256")
        != EXPECTED_TOPOLOGY_R1_SHA256
        or load_json(TOPOLOGY_R2_RESULT).get("result_sha256")
        != EXPECTED_TOPOLOGY_R2_SHA256
    ):
        raise RuntimeError("v0.4 selection-result identity changed")


def source_manifest() -> dict[str, Any]:
    paths = [
        HERE / "README.md",
        CONTRACT,
        Path(__file__).resolve(),
        V22_ROOT / "slcv0022_runner.py",
        V22_ROOT / "slcv0022_worker.py",
        V21_ROOT / "slcv0021_runner.py",
        V21_ROOT / "slcv0021_worker.py",
        hot_runner.ENGINE_PATH,
        hot_runner.INSTANCE_PATH,
        HOT_COMPLETION,
        HOT_RESULT,
        V31_ROOT / "slcv0031_w10.py",
        V4_DEV_ROOT / "slcv004_fiber_probe.py",
        FIBER_PROBE_RESULT,
        TOPOLOGY_DECISION,
        TOPOLOGY_R1_RESULT,
        TOPOLOGY_R2_RESULT,
    ]
    rows = [
        {
            "path": str(path.relative_to(QC_ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in paths
    ]
    unsigned = {
        "schema": "SLCV40_24_F16_512_SOURCE_MANIFEST_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "sources": rows,
    }
    return {**unsigned, "manifest_sha256": canonical_sha256(unsigned)}


def build_frozen_plan(
    engine: Any,
    instance: Mapping[str, Any],
) -> dict[str, Any]:
    inherited = hot_runner.build_plan(engine, instance)
    unsigned = dict(inherited)
    unsigned.pop("plan_sha256")
    unsigned.update(
        {
            "schema": "SLCV40_24_F16_512_EXECUTION_PLAN_V1",
            "campaign_id": CAMPAIGN_ID,
            "display_name": DISPLAY_NAME,
            "version_label": VERSION_LABEL,
            "scale_delta": "HOT_V0_2_2_PLUS_ACTIVE_FACTORED_W10_FIBER",
            "worker_topology": "FLAT_F16_FIXED_NODE_COMPLETE_WAVES",
            "active_changes": [
                "W10_ORDERED_SQUARE_RESPONSE",
                "ACTIVE_FULL_Q_512_BY_512",
                "OPEN_PORT_POSITION_ROUTING",
            ],
            "fiber_contract": {
                "name_component": 512,
                "coordinate_group": "Z4",
                "record_count": 9,
                "assignment_count": 262144,
                "storage_factor_dimensions": [512, 512],
                "both_factors_active": True,
                "constant_multiplicity": False,
                "attachment": "OPEN_RETAINED_PORT_BEFORE_FINAL_SCALAR_TRACE",
            },
            "excluded_changes": [
                "CUTSET_BRANCHING",
                "GLOBAL_SPIN_GAUGE",
                "FOURTH_CRT_PRIME",
                "CAPACITY29_PROFILE",
                "COMPACT_STAGE4C_GRAPH",
                "SAME_HOST_SUB_SLC_EXECUTION_QUEUES",
            ],
        }
    )
    if (
        unsigned["cluster_size"] != 16
        or unsigned["root_batch_size"] != 4
        or unsigned["retained_capacity_exponent_per_worker"] != 24
        or unsigned["aggregate_sharded_capacity_exponent"] != 28
        or unsigned["total_task_count"] != 384
        or unsigned["total_wave_count"] != 24
    ):
        raise RuntimeError("frozen 24-F16 execution profile changed")
    return {**unsigned, "plan_sha256": canonical_sha256(unsigned)}


def fixed_from_dos(rows: list[Mapping[str, Any]]) -> list[int]:
    fixed = [0] * 871
    for row in rows:
        fixed[int(row["energy"]) + 435] = int(row["count"])
    return fixed


def render_markdown(result: Mapping[str, Any]) -> str:
    metrics = result["metrics"]
    comparison = result["comparison"]
    fiber = result["fiber_execution"]
    closed = result["closed_n72_attachment"]
    return "\n".join(
        [
            f"# {DISPLAY_NAME} exact N72 result",
            "",
            f"**Status:** `{result['execution_status']}`  ",
            f"**Classification:** {result['result_classification']}",
            "",
            "## Frozen implementation",
            "",
            "- Per-worker retained capacity: **2^24**",
            "- Worker topology: **flat F16**",
            "- Root batch: **4**",
            "- Active fiber storage: **512 x 512**",
            "- Full-position assignments: **262,144**",
            "",
            "## N72 execution",
            "",
            f"- Fresh tasks: **{metrics['executed_task_count']}/384**",
            f"- Balanced waves: **{metrics['wave_count']}/24**",
            f"- Dense wall time: **{metrics['wall_seconds_this_invocation']:.6f} s**",
            (
                "- Peak sampled aggregate worker RSS: "
                f"**{metrics['peak_sampled_aggregate_worker_rss_bytes'] / (1 << 30):.6f} GiB**"
            ),
            (
                "- Minimum available memory: "
                f"**{metrics['minimum_available_memory_bytes'] / (1 << 30):.6f} GiB**"
            ),
            (
                "- Full 871-coefficient equality with v0.2, v0.2.1, and "
                f"v0.2.2: **{comparison['full_coefficient_equality']}**"
            ),
            f"- Configuration count: **{result['configuration_count']}**",
            "",
            "## Active fiber execution",
            "",
            (
                f"- Event transitions executed: "
                f"**{fiber['transition_count_exercised']:,}**"
            ),
            (
                f"- Event execution time: "
                f"**{fiber['elapsed_seconds']:.6f} s**"
            ),
            (
                "- Open-port ordered-position signatures: "
                f"**{result['open_port_attachment']['distinct_q_routing_signature_count']}**"
            ),
            (
                "- Closed response signatures: "
                f"**{closed['distinct_q_joint_signature_count']}**"
            ),
            (
                "- All four scalar marginals equal the fresh N72 result: "
                f"**{closed['all_four_scalar_marginals_equal_hot_v0_2_2']}**"
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
    if RESULT_JSON.exists():
        raise RuntimeError("frozen N72 result already exists")
    check_locked_sources()
    total_started = time.perf_counter()
    (
        engine,
        instance,
        baseline_completion,
        baseline_result,
        v21_completion,
        v21_result,
    ) = hot_runner.load_inputs()
    hot_completion = load_json(HOT_COMPLETION)
    hot_result = load_json(HOT_RESULT)
    if (
        instance.get("instance_sha256") != EXPECTED_INSTANCE_SHA256
        or hot_completion.get("operator_w_sha256")
        != EXPECTED_OPERATOR_SHA256
        or hot_result.get("operator_w_sha256")
        != EXPECTED_OPERATOR_SHA256
    ):
        raise RuntimeError("frozen parent identity changed")

    plan = build_frozen_plan(engine, instance)
    manifest = source_manifest()
    WORK.mkdir(parents=True, exist_ok=True)
    RELEASE.mkdir(parents=True, exist_ok=True)
    atomic_json(WORK / "EXECUTION_PLAN.json", plan)
    atomic_json(WORK / "SOURCE_MANIFEST.json", manifest)

    cluster = hot_runner.execute_cluster(engine, instance, plan)
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
        raise RuntimeError("frozen N72 coefficient vector differs")
    if canonical_sha256(candidate_fixed) != EXPECTED_FIXED_SHA256:
        raise RuntimeError("frozen N72 fixed-coefficient identity changed")

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
    full_equal = all(not values for values in difference_positions.values())
    comparison = {
        "fixed_domain": [-435, 435],
        "coefficient_count": 871,
        "difference_positions": difference_positions,
        "full_coefficient_equality": full_equal,
        "v0_2_wall_seconds": float(
            baseline_result["cluster_metrics"]["wall_seconds_this_invocation"]
        ),
        "v0_2_1_wall_seconds": float(
            v21_result["metrics"]["wall_seconds_this_invocation"]
        ),
        "v0_2_2_wall_seconds": float(
            hot_result["metrics"]["wall_seconds_this_invocation"]
        ),
        "slcv40_wall_seconds": float(
            metrics["wall_seconds_this_invocation"]
        ),
    }
    comparison.update(
        {
            "v0_2_over_slcv40_speed_ratio": (
                comparison["v0_2_wall_seconds"]
                / comparison["slcv40_wall_seconds"]
            ),
            "v0_2_1_over_slcv40_speed_ratio": (
                comparison["v0_2_1_wall_seconds"]
                / comparison["slcv40_wall_seconds"]
            ),
            "v0_2_2_over_slcv40_speed_ratio": (
                comparison["v0_2_2_wall_seconds"]
                / comparison["slcv40_wall_seconds"]
            ),
        }
    )
    checks = {
        "fresh_384_tasks_executed": (
            metrics["executed_task_count"] == 384
            and metrics["reused_task_count"] == 0
        ),
        "all_24_balanced_waves_completed": metrics["wave_count"] == 24,
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
            metrics["minimum_available_memory_bytes"] >= 8 * (1 << 30)
        ),
    }
    if not all(checks.values()):
        raise RuntimeError("frozen SLCV4.0 execution check failed")

    unsigned = {
        "schema": "SLCV40_24_F16_512_N72_COMPLETION_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "version_label": VERSION_LABEL,
        "execution_status": "COMPLETED",
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
        "linkage_roster": cluster["linkage_roster"],
        "linkage_roster_sha256": cluster["linkage_roster_sha256"],
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
    completion = {
        **unsigned,
        "completion_sha256": canonical_sha256(unsigned),
    }
    atomic_json(COMPLETION, completion)
    result_unsigned = {
        "schema": "SLCV40_24_F16_512_RESULT_V1",
        "campaign_id": CAMPAIGN_ID,
        "display_name": DISPLAY_NAME,
        "version_label": VERSION_LABEL,
        "execution_status": "COMPLETED",
        "result_classification": completion["result_classification"],
        "instance_id": completion["instance_id"],
        "instance_sha256": completion["instance_sha256"],
        "configuration_count": completion["configuration_count"],
        "operator_w_sha256": completion["operator_w_sha256"],
        "linked_fixed_coefficient_sha256": completion[
            "linked_fixed_coefficient_sha256"
        ],
        "plan": plan,
        "fiber_execution": fiber_receipt,
        "open_port_attachment": open_port,
        "closed_n72_attachment": closed,
        "metrics": metrics,
        "comparison": comparison,
        "checks": checks,
        "candidate_completion_path": str(COMPLETION.relative_to(QC_ROOT)),
        "candidate_completion_file_sha256": sha256_file(COMPLETION),
        "candidate_completion_sha256": completion["completion_sha256"],
        "source_manifest_sha256": manifest["manifest_sha256"],
        "operator_result_path": str(OPERATOR_RESULT.relative_to(QC_ROOT)),
        "operator_result_file_sha256": sha256_file(OPERATOR_RESULT),
        "total_runner_wall_seconds": completion[
            "total_runner_wall_seconds"
        ],
    }
    result = {
        **result_unsigned,
        "result_sha256": canonical_sha256(result_unsigned),
    }
    atomic_json(RESULT_JSON, result)
    RESULT_MD.write_text(render_markdown(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["execution_status"],
                "display_name": DISPLAY_NAME,
                "wall_seconds": metrics["wall_seconds_this_invocation"],
                "peak_gib": (
                    metrics["peak_sampled_aggregate_worker_rss_bytes"]
                    / (1 << 30)
                ),
                "minimum_available_gib": (
                    metrics["minimum_available_memory_bytes"] / (1 << 30)
                ),
                "all_coefficients_equal": full_equal,
                "fiber_assignments": fiber_receipt["assignment_count"],
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
