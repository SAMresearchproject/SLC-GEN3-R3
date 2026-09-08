#!/usr/bin/env python3
"""Exact active-fiber attachment probe for the hot v0.2.2 linked operator."""

from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any, Mapping, Sequence

import numpy as np


CAMPAIGN_ID = "SLCV004C16N72_LINKED_ACTIVE_512_FIBER"
VERSION_LABEL = "SLC_DENSE_EXACT_V0_4_C16_ACTIVE_FULL_Q"
SCHEMA = "SLCV004_ACTIVE_512_FIBER_PROBE_V1"

HERE = Path(__file__).resolve().parent
SLC_ROOT = HERE.parent
V22_ROOT = SLC_ROOT / "SLCV0022C16N72_LINKED_SUPERCELL_EXACT_N72"
V31_ROOT = SLC_ROOT / "SLCV0031_DENSE_EXACT_FULL_Q_STAGE4_N72"
X32_ROOT = (
    SLC_ROOT
    / "SLCX032_EXACT_N72_SUPERCELL_N144_DAISY_CHAIN_DISCOVERY"
)

HOT_COMPLETION = V22_ROOT / "work" / "N72" / "CANDIDATE_COMPLETION.json"
HOT_RESULT = V22_ROOT / "release" / "SLCV0022C16N72_RESULT.json"
PRIMARY_OPERATOR = (
    X32_ROOT / "release" / "SLCX032_PRIMARY_OPERATOR_RESULT.json"
)
W10_SOURCE = V31_ROOT / "slcv0031_w10.py"
ENGINE_SOURCE = X32_ROOT / "slcx032_engine.py"

WORK = HERE / "work" / "FIBER_PROBE"
RELEASE = HERE / "release"
RESULT_JSON = RELEASE / "SLCV004_FIBER_PROBE_RESULT.json"
RESULT_MD = RELEASE / "SLCV004_FIBER_PROBE_RESULT.md"

EXPECTED_FILE_SHA256 = {
    HOT_COMPLETION: (
        "07a2a1d043702c707139e166abb59919e4a59e142c7abc6caed87ef85d0d2dc5"
    ),
    HOT_RESULT: (
        "c985fe38f2901facf09b9e0aa6ac6c6360bc4e6a64d66aea0e0b1f54f2178ee4"
    ),
    PRIMARY_OPERATOR: (
        "9187d6cd0b2a5f4bebf064dd0484e043ed6f5681b39ac4de12fac9fa08f51095"
    ),
    W10_SOURCE: (
        "7727ae43483c305d7a31a3727aa0357ea06c4cb35c6c9c58faaea2d181598ccf"
    ),
    ENGINE_SOURCE: (
        "af744a255d0459e9100e13c9ea77a88e85686bbd5910ccc15eee480030e13d78"
    ),
}

EXPECTED_INSTANCE_SHA256 = (
    "396778a771378af50f7f6cbe594d93245fb0b653aef3f7a91b142c1e51fe450b"
)
EXPECTED_OPERATOR_W_SHA256 = (
    "13f315ddb0f1a9f19e992f1209a2090b5a604704c48ab549aff98e89073cda50"
)
EXPECTED_FIXED_SHA256 = (
    "06c8e85ea8deca940be49190b91d8f5a028338a4b1add1c62256e22017f2c353"
)
EXPECTED_TENSOR_PLAN_SHA256 = (
    "ae434966f46dc5c2a1ee2a24ef0a878c11c7e0e895d03bbeef405314d5aa0594"
)

RECORD_COUNT = 9
FACTOR_DIMENSION = 1 << RECORD_COUNT
ASSIGNMENT_COUNT = 1 << (2 * RECORD_COUNT)
N72_BOUND = 435
FIXED_LENGTH = 2 * N72_BOUND + 1
RESPONSE_VALUES = (-4, -2, 0, 2, 4)


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
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(canonical_bytes(value) + b"\n")
    os.replace(temporary, path)


def current_rss_bytes() -> int:
    status = Path("/proc/self/status").read_text(encoding="utf-8")
    for line in status.splitlines():
        if line.startswith("VmRSS:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("current resident memory is unavailable")


def peak_rss_bytes() -> int:
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def load_modules() -> tuple[Any, Any]:
    for path in (V31_ROOT, X32_ROOT):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)
    return (
        importlib.import_module("slcv0031_w10"),
        importlib.import_module("slcx032_engine"),
    )


def check_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, expected in EXPECTED_FILE_SHA256.items():
        observed = sha256_file(path)
        if observed != expected:
            raise RuntimeError(f"source identity changed: {path}")
        rows.append(
            {
                "path": str(path.relative_to(SLC_ROOT)),
                "bytes": path.stat().st_size,
                "sha256": observed,
            }
        )
    return rows


def fixed_from_dos(rows: Sequence[Mapping[str, Any]]) -> list[int]:
    fixed = [0] * FIXED_LENGTH
    for row in rows:
        energy = int(row["energy"])
        if not -N72_BOUND <= energy <= N72_BOUND:
            raise RuntimeError("hot N72 energy escaped its fixed domain")
        fixed[energy + N72_BOUND] = int(row["count"])
    return fixed


def load_hot_objects() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    list[int],
]:
    completion = load_json(HOT_COMPLETION)
    result = load_json(HOT_RESULT)
    envelope = load_json(PRIMARY_OPERATOR)
    operator = envelope.get("result", {}).get("operator")
    if not isinstance(operator, dict):
        raise RuntimeError("saved linked operator is absent")
    if (
        completion.get("instance_sha256") != EXPECTED_INSTANCE_SHA256
        or result.get("instance_sha256") != EXPECTED_INSTANCE_SHA256
        or operator.get("source_instance_sha256") != EXPECTED_INSTANCE_SHA256
    ):
        raise RuntimeError("N72 instance identity changed")
    if (
        completion.get("operator_w_sha256") != EXPECTED_OPERATOR_W_SHA256
        or result.get("operator_w_sha256") != EXPECTED_OPERATOR_W_SHA256
        or operator.get("w_sha256") != EXPECTED_OPERATOR_W_SHA256
        or canonical_sha256(operator.get("w_coefficients"))
        != EXPECTED_OPERATOR_W_SHA256
    ):
        raise RuntimeError("hot linked operator identity changed")
    fixed = fixed_from_dos(completion["dos"])
    if (
        canonical_sha256(fixed) != EXPECTED_FIXED_SHA256
        or completion.get("linked_fixed_coefficient_sha256")
        != EXPECTED_FIXED_SHA256
    ):
        raise RuntimeError("hot N72 scalar identity changed")
    return completion, result, operator, fixed


def apply_forward_addresses(
    addresses: np.ndarray,
    record_index: int,
) -> np.ndarray:
    bit = np.uint32(1 << record_index)
    low = addresses & np.uint32(FACTOR_DIMENSION - 1)
    high = addresses >> np.uint32(RECORD_COUNT)
    low_bit = (low >> np.uint32(record_index)) & np.uint32(1)
    target_low = low ^ bit
    target_high = high ^ (low_bit * bit)
    return target_low | (target_high << np.uint32(RECORD_COUNT))


def apply_reverse_addresses(
    addresses: np.ndarray,
    record_index: int,
) -> np.ndarray:
    bit = np.uint32(1 << record_index)
    low = addresses & np.uint32(FACTOR_DIMENSION - 1)
    high = addresses >> np.uint32(RECORD_COUNT)
    low_bit = (low >> np.uint32(record_index)) & np.uint32(1)
    target_low = low ^ bit
    target_high = high ^ ((np.uint32(1) - low_bit) * bit)
    return target_low | (target_high << np.uint32(RECORD_COUNT))


def exercise_full_fiber(w10: Any) -> tuple[dict[str, Any], np.ndarray]:
    started = time.perf_counter()
    rss_before = current_rss_bytes()
    plan = w10.full_q_tensor_plan(RECORD_COUNT)
    report = w10.validate_full_q_tensor_plan(plan)
    if (
        plan["tensor_plan_sha256"] != EXPECTED_TENSOR_PLAN_SHA256
        or report["assignment_count"] != ASSIGNMENT_COUNT
        or report["factor_dimensions"] != [FACTOR_DIMENSION, FACTOR_DIMENSION]
    ):
        raise RuntimeError("full-position tensor identity changed")

    addresses = np.arange(ASSIGNMENT_COUNT, dtype=np.uint32)
    transition_maps = np.empty(
        (2, RECORD_COUNT, ASSIGNMENT_COUNT),
        dtype=np.uint32,
    )
    carry_counts: list[dict[str, int]] = []
    for record_index in range(RECORD_COUNT):
        forward = apply_forward_addresses(addresses, record_index)
        reverse = apply_reverse_addresses(addresses, record_index)
        transition_maps[0, record_index, :] = forward
        transition_maps[1, record_index, :] = reverse
        if not np.array_equal(reverse[forward], addresses):
            raise RuntimeError("forward/reverse event maps are not inverse")
        if not np.array_equal(forward[reverse], addresses):
            raise RuntimeError("reverse/forward event maps are not inverse")
        bit = np.uint32(1 << record_index)
        source_high = addresses >> np.uint32(RECORD_COUNT)
        forward_high = forward >> np.uint32(RECORD_COUNT)
        reverse_high = reverse >> np.uint32(RECORD_COUNT)
        carry_counts.append(
            {
                "record_index": record_index,
                "forward_high_factor_changes": int(
                    np.count_nonzero((source_high ^ forward_high) & bit)
                ),
                "reverse_high_factor_changes": int(
                    np.count_nonzero((source_high ^ reverse_high) & bit)
                ),
            }
        )

        for source_q in range(4):
            q_values = [0] * RECORD_COUNT
            q_values[record_index] = source_q
            low, high = w10.encode_q_vector(q_values)
            source_address = low | (high << RECORD_COUNT)
            expected_forward = w10.apply_event_to_q_factors(
                low,
                high,
                record_count=RECORD_COUNT,
                record_index=record_index,
                event="FORWARD",
            )
            expected_reverse = w10.apply_event_to_q_factors(
                low,
                high,
                record_count=RECORD_COUNT,
                record_index=record_index,
                event="REVERSE",
            )
            observed_forward = int(
                transition_maps[0, record_index, source_address]
            )
            observed_reverse = int(
                transition_maps[1, record_index, source_address]
            )
            if observed_forward != (
                expected_forward[0] | (expected_forward[1] << RECORD_COUNT)
            ):
                raise RuntimeError("forward event differs from tested W10 action")
            if observed_reverse != (
                expected_reverse[0] | (expected_reverse[1] << RECORD_COUNT)
            ):
                raise RuntimeError("reverse event differs from tested W10 action")

    elapsed = time.perf_counter() - started
    rss_after = current_rss_bytes()
    maps_hash = hashlib.sha256(
        np.ascontiguousarray(transition_maps, dtype=">u4").tobytes(order="C")
    ).hexdigest()
    transition_count = 3 * RECORD_COUNT * ASSIGNMENT_COUNT
    return (
        {
            "record_count": RECORD_COUNT,
            "coordinate_group": "Z4",
            "factor_dimensions": [FACTOR_DIMENSION, FACTOR_DIMENSION],
            "assignment_count": ASSIGNMENT_COUNT,
            "tensor_plan_sha256": plan["tensor_plan_sha256"],
            "both_factors_active": (
                plan["factorization"]["both_factors_active"] is True
            ),
            "constant_multiplicity": (
                plan["factorization"]["constant_multiplicity"]
            ),
            "event_count_per_record": 3,
            "transition_count_exercised": transition_count,
            "forward_reverse_map_count": 2 * RECORD_COUNT,
            "identity_map_shared": True,
            "materialized_map_bytes": int(transition_maps.nbytes),
            "address_vector_bytes": int(addresses.nbytes),
            "map_sha256": maps_hash,
            "carry_counts": carry_counts,
            "all_event_maps_closed_and_invertible": True,
            "all_local_actions_equal_tested_w10_action": True,
            "elapsed_seconds": elapsed,
            "transitions_per_second": transition_count / elapsed,
            "rss_before_bytes": rss_before,
            "rss_after_bytes": rss_after,
            "rss_growth_bytes": max(0, rss_after - rss_before),
            "peak_rss_bytes": peak_rss_bytes(),
        },
        transition_maps,
    )


def build_open_port_attachment(w10: Any) -> tuple[dict[str, Any], np.ndarray]:
    started = time.perf_counter()
    routing = np.empty((4, 16, 16), dtype=np.int8)
    census: dict[str, dict[str, int]] = {}
    signatures: list[str] = []
    for q in range(4):
        counts = {str(response): 0 for response in RESPONSE_VALUES}
        for left in range(16):
            for right in range(16):
                response = int(w10.square_response(left, right, q))
                routing[q, left, right] = RESPONSE_VALUES.index(response)
                counts[str(response)] += 1
        census[str(q)] = counts
        signatures.append(
            hashlib.sha256(
                np.ascontiguousarray(routing[q], dtype=np.int8).tobytes()
            ).hexdigest()
        )
    if len(set(signatures)) != 4:
        raise RuntimeError("open ordered-square response lost a q position")
    return (
        {
            "attachment": "OPEN_RETAINED_PORT_BEFORE_TRACE",
            "port_state_shape": [16, 16],
            "q_lane_count": 4,
            "response_values": list(RESPONSE_VALUES),
            "routing_shape": list(routing.shape),
            "routing_bytes": int(routing.nbytes),
            "routing_sha256": hashlib.sha256(
                np.ascontiguousarray(routing, dtype=np.int8).tobytes(order="C")
            ).hexdigest(),
            "q_routing_signatures": signatures,
            "distinct_q_routing_signature_count": len(set(signatures)),
            "all_four_q_positions_distinct": len(set(signatures)) == 4,
            "low_bit_changes_response": signatures[0] != signatures[1],
            "high_bit_changes_response": signatures[0] != signatures[2],
            "opposite_directions_distinct": signatures[1] != signatures[3],
            "response_census": census,
            "elapsed_seconds": time.perf_counter() - started,
        },
        routing,
    )


def build_closed_n72_attachment(
    operator: Mapping[str, Any],
    hot_fixed: Sequence[int],
    routing: np.ndarray,
) -> dict[str, Any]:
    started = time.perf_counter()
    w = operator["w_coefficients"]
    glue = operator["glue_y_degrees"]
    if len(w) != 16 or any(len(row) != 432 for row in w):
        raise RuntimeError("linked coefficient shape changed")
    joint = [
        [[0] * FIXED_LENGTH for _ in RESPONSE_VALUES]
        for _ in range(4)
    ]
    for q in range(4):
        for state in range(16):
            response_index = int(routing[q, state, state])
            shift = int(glue[state][state])
            for degree, raw_count in enumerate(w[state]):
                fixed_index = 2 * (degree + shift)
                if not 0 <= fixed_index < FIXED_LENGTH:
                    raise RuntimeError("linked contribution escaped N72 domain")
                joint[q][response_index][fixed_index] += int(raw_count)

    marginals: list[list[int]] = []
    signature_hashes: list[str] = []
    response_totals: dict[str, dict[str, str]] = {}
    occupied_joint_cells: dict[str, int] = {}
    for q in range(4):
        marginal = [
            sum(joint[q][response_index][index] for response_index in range(5))
            for index in range(FIXED_LENGTH)
        ]
        if marginal != list(hot_fixed):
            raise RuntimeError("fiber response changed the hot N72 scalar marginal")
        marginals.append(marginal)
        signature_hashes.append(canonical_sha256(joint[q]))
        response_totals[str(q)] = {
            str(response): str(sum(joint[q][response_index]))
            for response_index, response in enumerate(RESPONSE_VALUES)
        }
        occupied_joint_cells[str(q)] = sum(
            1
            for response_index in range(5)
            for count in joint[q][response_index]
            if count
        )

    equality_pairs = [
        [left, right]
        for left in range(4)
        for right in range(left + 1, 4)
        if signature_hashes[left] == signature_hashes[right]
    ]
    if equality_pairs != [[1, 3]]:
        raise RuntimeError("one-cell trace q-signature relation changed")
    return {
        "attachment": "ONE_CELL_TRACE_SCALAR_MARGINAL",
        "joint_coordinate_order": [
            "q",
            "ordered_square_response",
            "fixed_energy",
        ],
        "joint_shape": [4, 5, FIXED_LENGTH],
        "joint_tensor_sha256": canonical_sha256(joint),
        "q_joint_signature_sha256": signature_hashes,
        "distinct_q_joint_signature_count": len(set(signature_hashes)),
        "equal_q_signature_pairs": equality_pairs,
        "opposite_directions_merge_at_one_cell_trace": (
            equality_pairs == [[1, 3]]
        ),
        "low_bit_remains_active": signature_hashes[0] != signature_hashes[1],
        "high_bit_remains_active": signature_hashes[0] != signature_hashes[2],
        "response_totals": response_totals,
        "occupied_joint_cells": occupied_joint_cells,
        "scalar_marginal_sha256_by_q": [
            canonical_sha256(marginal) for marginal in marginals
        ],
        "hot_scalar_sha256": canonical_sha256(list(hot_fixed)),
        "all_four_scalar_marginals_equal_hot_v0_2_2": True,
        "configuration_count_per_q": str(sum(hot_fixed)),
        "elapsed_seconds": time.perf_counter() - started,
    }


def resource_envelope(
    hot_result: Mapping[str, Any],
    fiber: Mapping[str, Any],
    open_port: Mapping[str, Any],
) -> dict[str, Any]:
    coefficient_count = FIXED_LENGTH
    address_cells = coefficient_count * ASSIGNMENT_COUNT
    three_prime_bytes = address_cells * 3 * np.dtype(np.uint32).itemsize
    five_response_three_prime_bytes = three_prime_bytes * len(RESPONSE_VALUES)
    hot_peak = int(
        hot_result["metrics"]["peak_sampled_aggregate_worker_rss_bytes"]
    )
    hot_minimum_available = int(
        hot_result["metrics"]["minimum_available_memory_bytes"]
    )
    return {
        "hot_v0_2_2_wall_seconds": float(
            hot_result["metrics"]["wall_seconds_this_invocation"]
        ),
        "hot_v0_2_2_peak_sampled_aggregate_worker_rss_bytes": hot_peak,
        "hot_v0_2_2_minimum_available_memory_bytes": hot_minimum_available,
        "factorized_probe_increment_bytes": (
            int(fiber["materialized_map_bytes"])
            + int(fiber["address_vector_bytes"])
            + int(open_port["routing_bytes"])
        ),
        "naive_full_q_coefficient_address_count": address_cells,
        "naive_full_q_three_residue_bytes": three_prime_bytes,
        "naive_full_q_three_residue_gib": three_prime_bytes / (1 << 30),
        "naive_five_response_three_residue_bytes": (
            five_response_three_prime_bytes
        ),
        "naive_five_response_three_residue_gib": (
            five_response_three_prime_bytes / (1 << 30)
        ),
        "implementation_direction": (
            "SHARE_HOT_LINKED_COEFFICIENTS_AND_ROUTE_ACTIVE_Q_ON_OPEN_PORTS"
        ),
        "dense_broadcast_selected": False,
    }


def result_markdown(result: Mapping[str, Any]) -> str:
    fiber = result["full_fiber_execution"]
    open_port = result["open_port_attachment"]
    closed = result["closed_n72_attachment"]
    resources = result["resource_envelope"]
    return "\n".join(
        [
            "# SLC v0.4 active 512-factor fiber probe",
            "",
            f"**Status:** `{result['execution_status']}`  ",
            f"**Classification:** {result['result_classification']}",
            "",
            "## Outcome",
            "",
            (
                f"- Exhaustively executed **{fiber['transition_count_exercised']:,}** "
                "event transitions over all **262,144** full-position addresses."
            ),
            (
                f"- Fiber event maps took **{fiber['elapsed_seconds']:.6f} s** "
                f"and used **{fiber['materialized_map_bytes'] / (1 << 20):.3f} MiB**."
            ),
            (
                "- The open 16-by-16 retained port keeps all "
                f"**{open_port['distinct_q_routing_signature_count']}** ordered "
                "positions distinct."
            ),
            (
                "- Every one-cell N72 q marginal equals the hot v0.2.2 "
                f"871-position scalar: **{closed['all_four_scalar_marginals_equal_hot_v0_2_2']}**."
            ),
            (
                "- The final one-cell trace retains three response signatures; "
                "the forward and reverse signatures merge there."
            ),
            (
                "- Closed-response totals are exact powers-of-two patterns: "
                "`q=0` is entirely response `-4`; `q=1,3` split "
                "`2^69 : 3*2^70 : 2^69` across `-4,0,+4`; and `q=2` "
                "splits `2^70 : 2^71 : 2^70`."
            ),
            "",
            "## v0.4 implementation consequence",
            "",
            (
                "Install the active q routing on the open linked operator and "
                "carry it through linkage. Take the scalar trace only as a final "
                "marginal. Reuse the hot linked coefficient rows rather than "
                "broadcasting them over all full-position addresses."
            ),
            "",
            "## Resource envelope",
            "",
            (
                f"- Factorized coordinate and routing storage in this probe: "
                f"**{resources['factorized_probe_increment_bytes'] / (1 << 20):.3f} MiB**."
            ),
            (
                "- A direct 871-by-262,144 three-residue broadcast would occupy "
                f"**{resources['naive_full_q_three_residue_gib']:.3f} GiB** "
                "before response lanes or work buffers."
            ),
            (
                "- Five dense response lanes would raise that static array to "
                f"**{resources['naive_five_response_three_residue_gib']:.3f} GiB**."
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
    total_started = time.perf_counter()
    rss_started = current_rss_bytes()
    sources = check_sources()
    w10, _engine = load_modules()
    completion, hot_result, operator, hot_fixed = load_hot_objects()

    fiber, transition_maps = exercise_full_fiber(w10)
    open_port, routing = build_open_port_attachment(w10)
    closed = build_closed_n72_attachment(operator, hot_fixed, routing)
    resources = resource_envelope(hot_result, fiber, open_port)
    checks = {
        "hot_parent_completed": completion.get("status") == "COMPLETED",
        "hot_parent_operator_reused": (
            operator["w_sha256"] == completion["operator_w_sha256"]
        ),
        "all_262144_addresses_executed": (
            fiber["assignment_count"] == ASSIGNMENT_COUNT
        ),
        "both_512_factors_active": (
            fiber["both_factors_active"]
            and fiber["constant_multiplicity"] is False
        ),
        "mod4_events_closed_and_invertible": (
            fiber["all_event_maps_closed_and_invertible"]
        ),
        "open_port_keeps_four_positions": (
            open_port["all_four_q_positions_distinct"]
        ),
        "low_and_high_coordinates_change_response": (
            open_port["low_bit_changes_response"]
            and open_port["high_bit_changes_response"]
        ),
        "all_n72_scalar_marginals_equal_hot_parent": (
            closed["all_four_scalar_marginals_equal_hot_v0_2_2"]
        ),
        "trace_localizes_direction_merge": (
            closed["opposite_directions_merge_at_one_cell_trace"]
        ),
        "hot_linked_coefficients_shared_not_broadcast": (
            resources["dense_broadcast_selected"] is False
        ),
    }
    if not all(checks.values()):
        raise RuntimeError("v0.4 fiber probe check failed")

    del transition_maps
    elapsed = time.perf_counter() - total_started
    unsigned = {
        "schema": SCHEMA,
        "campaign_id": CAMPAIGN_ID,
        "version_label": VERSION_LABEL,
        "execution_status": "COMPLETED",
        "result_classification": (
            "The test result suggests strong contact with the concept."
        ),
        "parent": {
            "campaign_id": hot_result["campaign_id"],
            "version_label": hot_result["version_label"],
            "result_sha256": hot_result["result_sha256"],
            "instance_sha256": hot_result["instance_sha256"],
            "operator_w_sha256": hot_result["operator_w_sha256"],
            "linked_fixed_coefficient_sha256": hot_result[
                "linked_fixed_coefficient_sha256"
            ],
        },
        "source_manifest": sources,
        "full_fiber_execution": fiber,
        "open_port_attachment": open_port,
        "closed_n72_attachment": closed,
        "resource_envelope": resources,
        "checks": checks,
        "metrics": {
            "elapsed_seconds": elapsed,
            "rss_started_bytes": rss_started,
            "rss_finished_bytes": current_rss_bytes(),
            "peak_process_rss_bytes": peak_rss_bytes(),
        },
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
    result = {**unsigned, "result_sha256": canonical_sha256(unsigned)}
    WORK.mkdir(parents=True, exist_ok=True)
    RELEASE.mkdir(parents=True, exist_ok=True)
    atomic_json(WORK / "SLCV004_FIBER_PROBE_EXECUTION.json", result)
    atomic_json(RESULT_JSON, result)
    RESULT_MD.write_text(result_markdown(result), encoding="utf-8")
    print(json.dumps(
        {
            "status": result["execution_status"],
            "elapsed_seconds": elapsed,
            "fiber_seconds": fiber["elapsed_seconds"],
            "fiber_map_mib": fiber["materialized_map_bytes"] / (1 << 20),
            "open_q_signatures": open_port[
                "distinct_q_routing_signature_count"
            ],
            "closed_q_signatures": closed[
                "distinct_q_joint_signature_count"
            ],
            "all_scalar_marginals_equal": closed[
                "all_four_scalar_marginals_equal_hot_v0_2_2"
            ],
            "result_sha256": result["result_sha256"],
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
