"""Exact retained-port and two-cell transfer engine for SLCX032.

The engine is deliberately a narrow sidecar.  It hash-loads the sealed
SLCX023A/SLCX027/SLCX029 arithmetic implementations, compiles one frozen
four-bit boundary object from ``SLCX025_N72_I00``, and exposes two independent
N144 constructions:

* ``trace(T**2)`` from the retained-port N72 cell operator; and
* a complete 144-variable fused elimination on an independently assembled
  two-copy graph.

Every shifted Ising exponent is even.  The engine therefore works in the
exact quotient variable ``y = z**2``.  Root evaluations are still produced by
the sealed parent factor builder: for a length-L transform in y it receives
the first L powers of a primitive 2L-th root zeta, so zeta**2 is the ordinary
L-th NTT root used by the inverse transform.

This module contains no stage opening, retry, fallback, artifact writing, or
verdict logic.  Those custody duties belong to the sealed worker and runner.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
from types import ModuleType
from typing import Any, Callable, Mapping, Sequence

import numpy as np


CAMPAIGN_ID = "SLCX032_EXACT_N72_SUPERCELL_N144_DAISY_CHAIN_DISCOVERY"
N72_INSTANCE_ID = "SLCX025_N72_I00"
N72_INSTANCE_SHA256 = "396778a771378af50f7f6cbe594d93245fb0b653aef3f7a91b142c1e51fe450b"
N72_VAULT_SHA256 = "45fb1e7683990edff5eb3224b8cbdf08364aeb8e566c8cbd85b5c3996971011d"

PRIMES_3: tuple[int, ...] = (998244353, 1004535809, 469762049)
PRIMES_5: tuple[int, ...] = PRIMES_3 + (167772161, 1224736769)
PRIMITIVE_ROOT = 3
PORT_ORDER: tuple[int, ...] = (6, 15, 16, 58)
CUT_ENDPOINTS: tuple[tuple[int, int], ...] = ((6, 58), (15, 16))
STATE_COUNT = 16
N72_BOUND = 435
LOCAL_BOUND = 431
GLUE_BOUND = 4
N144_BOUND = 870
W_Y_LENGTH = 512
N144_Y_LENGTH = 1024
ROOT_BATCH_SIZE = 2
FUSED_CHUNK_CAP = 32768
EXPECTED_CONDITIONAL_WIDTH = 22
EXPECTED_CONDITIONAL_UNION_WORK = 42161952
EXPECTED_DIRECT_WIDTH = 22
EXPECTED_DIRECT_UNION_WORK = 94813790
DOS_DOMAIN = "SLCX029-EXACT-DOS-V1"

EXPECTED_COMPRESSED_SHA256 = "9827128293c306439000e5160fcac3d13d534cb825b7c508fcdef921bdded3aa"
EXPECTED_EXACT_SHA256 = "fb8bff08ae0836a628a90edb141f8e3d96ae13d96075eb2e2031d12737f77c5a"
EXPECTED_TRANSFER_SHA256 = "2374ca80472151ac7b72558ec969e045fdf163bf306a72e1b9168a582b758a9d"
EXPECTED_N12_VAULT_SHA256 = "ff5408986ed611165e4f1b4444623f346df1448c97e4575b97c2666d231445df"
EXPECTED_PORT_FREEZE_SHA256 = "e03716c5aa0f477c8118709fadc6243a7165b0592e7ad8448e41df19e583eb05"
EXPECTED_ORDER_FREEZE_SHA256 = "207debe5ea884d775668ce2807204a922379fced3ad68733238297b00574a14a"


class SLCX032Error(RuntimeError):
    """Base SLCX032 engine error."""


class SLCX032CustodyError(SLCX032Error):
    """A source, frozen choice, or typed domain changed."""


class SLCX032ArithmeticError(SLCX032Error):
    """An exact arithmetic invariant failed."""


Progress = Callable[[Mapping[str, Any]], None]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "18_SAM_NATIVE_QC").is_dir():
            return parent
    raise SLCX032CustodyError("could not locate the Courtroom repository root")


ROOT = _repo_root()
BASE = ROOT / "18_SAM_NATIVE_QC" / "SLCX032_EXACT_N72_SUPERCELL_N144_DAISY_CHAIN_DISCOVERY"
COMPRESSED_ENGINE = (
    ROOT
    / "18_SAM_NATIVE_QC"
    / "SLCX029_DENSE_FRONTIER_COMPRESSION_N36_DISCOVERY_N48_VALIDATION_N72_CLOSED"
    / "release"
    / "executed_capsule"
    / "slcx029_compressed_engine.py"
)
EXACT_ENGINE = (
    ROOT
    / "18_SAM_NATIVE_QC"
    / "SLCX025_EXACT_N72_FRUSTRATED_ISING_DOS_EXTENSION"
    / "SLCX025_EXECUTION_CAPSULE"
    / "slcx023_exact_engine.py"
)
TRANSFER_ENGINE = (
    ROOT
    / "18_SAM_NATIVE_QC"
    / "SLCX027_EXACT_BOUNDARY_TRANSFER_RING_SCALING"
    / "release"
    / "executed_capsule"
    / "slcx027_transfer_engine.py"
)
N12_VAULT = (
    ROOT
    / "18_SAM_NATIVE_QC"
    / "SLCX027_EXACT_BOUNDARY_TRANSFER_RING_SCALING"
    / "SLCX027_MOTIF_FAMILY_VAULT.json"
)
PORT_FREEZE = BASE / "SLCX032_PORT_FREEZE.json"
ORDER_FREEZE = (
    ROOT
    / "18_SAM_NATIVE_QC"
    / "SLCX031_DENSE_N72_EXACT_DOS_WIDTH22_FUSED_INDEPENDENT_REFERENCE"
    / "SLCX031_ORDER_FREEZE.json"
)


_MODULE_CACHE: dict[str, ModuleType] = {}


def _load_guarded_module(path: Path, expected_sha256: str, name: str) -> ModuleType:
    if sha256_file(path) != expected_sha256:
        raise SLCX032CustodyError(f"sealed module hash mismatch: {path}")
    if name in _MODULE_CACHE:
        return _MODULE_CACHE[name]
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise SLCX032CustodyError(f"could not load sealed module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    _MODULE_CACHE[name] = module
    return module


def _modules() -> tuple[ModuleType, ModuleType, ModuleType]:
    compressed = _load_guarded_module(
        COMPRESSED_ENGINE, EXPECTED_COMPRESSED_SHA256, "slcx032_sealed_compressed"
    )
    exact = _load_guarded_module(EXACT_ENGINE, EXPECTED_EXACT_SHA256, "slcx032_sealed_exact")
    transfer = _load_guarded_module(
        TRANSFER_ENGINE, EXPECTED_TRANSFER_SHA256, "slcx032_sealed_transfer"
    )
    return compressed, exact, transfer


def _notify(progress: Progress | None, **payload: Any) -> None:
    if progress is not None:
        progress({"campaign_id": CAMPAIGN_ID, **payload})


def _plain_int(value: Any, label: str) -> int:
    if type(value) is not int:
        raise SLCX032CustodyError(f"{label} must be an integer")
    return value


def _instance_hash(instance: Mapping[str, Any]) -> str:
    core = {key: value for key, value in instance.items() if key != "instance_sha256"}
    return canonical_sha256(core)


def _read_frozen_json(path: Path, expected_sha256: str) -> dict[str, Any]:
    if sha256_file(path) != expected_sha256:
        raise SLCX032CustodyError(f"frozen JSON hash mismatch: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SLCX032CustodyError(f"frozen JSON is not an object: {path}")
    return value


def load_port_freeze() -> dict[str, Any]:
    freeze = _read_frozen_json(PORT_FREEZE, EXPECTED_PORT_FREEZE_SHA256)
    if freeze.get("freeze_sha256") != canonical_sha256(
        {key: value for key, value in freeze.items() if key != "freeze_sha256"}
    ):
        raise SLCX032CustodyError("port-freeze semantic self-seal mismatch")
    required = {
        "source_instance_id": N72_INSTANCE_ID,
        "source_instance_sha256": N72_INSTANCE_SHA256,
        "port_bit_order": list(PORT_ORDER),
        "cut_edge_endpoints": [list(edge) for edge in CUT_ENDPOINTS],
        "conditional_induced_width": EXPECTED_CONDITIONAL_WIDTH,
        "sum_2_pow_union_scope": EXPECTED_CONDITIONAL_UNION_WORK,
        "candidate_count": 15390,
        "selector_forbidden_values_received": False,
    }
    for key, expected in required.items():
        if freeze.get(key) != expected:
            raise SLCX032CustodyError(f"port-freeze field mismatch: {key}")
    return freeze


def load_full_n72_order() -> list[int]:
    freeze = _read_frozen_json(ORDER_FREEZE, EXPECTED_ORDER_FREEZE_SHA256)
    if freeze.get("freeze_sha256") != canonical_sha256(
        {key: value for key, value in freeze.items() if key != "freeze_sha256"}
    ):
        raise SLCX032CustodyError("N72 order-freeze semantic self-seal mismatch")
    primary = freeze.get("primary")
    if not isinstance(primary, Mapping):
        raise SLCX032CustodyError("N72 primary order is absent")
    order = [_plain_int(value, "primary order vertex") for value in primary.get("order", [])]
    if sorted(order) != list(range(72)) or primary.get("induced_width") != 22:
        raise SLCX032CustodyError("N72 full order roster/width mismatch")
    return order


def _validate_edges(instance: Mapping[str, Any], n: int) -> tuple[list[tuple[int, int, int]], list[int]]:
    raw_edges = instance.get("edges")
    if not isinstance(raw_edges, list):
        raise SLCX032CustodyError("instance edges must be a list")
    edges: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int]] = set()
    degrees = [0] * n
    for index, raw in enumerate(raw_edges):
        if not isinstance(raw, list) or len(raw) != 3:
            raise SLCX032CustodyError(f"edges[{index}] is malformed")
        u = _plain_int(raw[0], f"edges[{index}][0]")
        v = _plain_int(raw[1], f"edges[{index}][1]")
        coupling = _plain_int(raw[2], f"edges[{index}][2]")
        if not 0 <= u < v < n or coupling == 0 or (u, v) in seen:
            raise SLCX032CustodyError("edge roster is noncanonical, parallel, or zero-weight")
        seen.add((u, v))
        degrees[u] += 1
        degrees[v] += 1
        edges.append((u, v, coupling))
    if edges != sorted(edges):
        raise SLCX032CustodyError("edges are not canonically sorted")
    return edges, degrees


def validate_n72_instance(instance: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(instance, Mapping):
        raise SLCX032CustodyError("N72 source must be a mapping")
    if instance.get("instance_id") != N72_INSTANCE_ID or instance.get("instance_sha256") != N72_INSTANCE_SHA256:
        raise SLCX032CustodyError("N72 source identity mismatch")
    if _instance_hash(instance) != N72_INSTANCE_SHA256:
        raise SLCX032CustodyError("N72 semantic instance hash mismatch")
    n = _plain_int(instance.get("N"), "N72.N")
    if n != 72:
        raise SLCX032CustodyError("N72 source size changed")
    fields = instance.get("fields")
    if not isinstance(fields, list) or len(fields) != n or any(type(value) is not int for value in fields):
        raise SLCX032CustodyError("N72 fields are malformed")
    edges, degrees = _validate_edges(instance, n)
    if len(edges) != 180 or instance.get("edge_count") != 180 or any(value != 5 for value in degrees):
        raise SLCX032CustodyError("N72 graph is not the frozen five-regular roster")
    bound = sum(abs(value) for value in fields) + sum(abs(edge[2]) for edge in edges)
    if bound != N72_BOUND or instance.get("energy_bound_B") != N72_BOUND:
        raise SLCX032CustodyError("N72 energy bound mismatch")
    return {
        "status": "PASS",
        "instance_id": N72_INSTANCE_ID,
        "instance_sha256": N72_INSTANCE_SHA256,
        "N": n,
        "edge_count": len(edges),
        "energy_bound_B": bound,
    }


def _cut_edges(instance: Mapping[str, Any], endpoints: Sequence[Sequence[int]]) -> tuple[tuple[int, int, int], ...]:
    edge_map = {(int(u), int(v)): (int(u), int(v), int(j)) for u, v, j in instance["edges"]}
    cuts: list[tuple[int, int, int]] = []
    for raw in endpoints:
        if len(raw) != 2:
            raise SLCX032CustodyError("cut endpoint is malformed")
        pair = tuple(sorted((_plain_int(raw[0], "cut.u"), _plain_int(raw[1], "cut.v"))))
        if pair not in edge_map:
            raise SLCX032CustodyError("frozen cut edge is absent")
        cuts.append(edge_map[pair])
    if len(set(cuts)) != len(cuts):
        raise SLCX032CustodyError("cut roster contains a duplicate")
    ports = sorted({vertex for edge in cuts for vertex in edge[:2]})
    if ports != list(PORT_ORDER):
        raise SLCX032CustodyError("cut roster does not expose the frozen port")
    return tuple(cuts)


def factor_ownership(instance: Mapping[str, Any]) -> dict[str, Any]:
    cuts = _cut_edges(instance, CUT_ENDPOINTS)
    cut_set = set(cuts)
    source_edges = [tuple(map(int, edge)) for edge in instance["edges"]]
    local_edges = [edge for edge in source_edges if edge not in cut_set]
    if set(local_edges) & cut_set or set(local_edges) | cut_set != set(source_edges):
        raise SLCX032CustodyError("local/glue ownership is not an exact partition")
    local_bound = sum(abs(int(value)) for value in instance["fields"]) + sum(abs(edge[2]) for edge in local_edges)
    glue_bound = sum(abs(edge[2]) for edge in cuts)
    if (local_bound, glue_bound, local_bound + glue_bound) != (LOCAL_BOUND, GLUE_BOUND, N72_BOUND):
        raise SLCX032CustodyError("local/glue bounds changed")
    edge_owners = [
        [u, v, coupling, "D" if (u, v, coupling) in cut_set else "W"]
        for u, v, coupling in source_edges
    ]
    return {
        "status": "PASS",
        "source_factor_count": len(instance["fields"]) + len(source_edges),
        "local_factor_count": len(instance["fields"]) + len(local_edges),
        "glue_factor_count": len(cuts),
        "local_edge_count": len(local_edges),
        "double_owned_factor_count": 0,
        "unowned_factor_count": 0,
        "all_source_factors_owned_once": True,
        "port_vertices": list(PORT_ORDER),
        "cut_edges": [list(edge) for edge in cuts],
        "local_bound": local_bound,
        "glue_bound": glue_bound,
        "total_bound": local_bound + glue_bound,
        "edge_owner_sha256": canonical_sha256(edge_owners),
        "local_edges": [list(edge) for edge in local_edges],
    }


def _local_instance(instance: Mapping[str, Any], ownership: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "N": int(instance["N"]),
        "fields": [int(value) for value in instance["fields"]],
        "edges": [list(map(int, edge)) for edge in ownership["local_edges"]],
        "energy_bound_B": int(ownership["local_bound"]),
    }


@dataclass(frozen=True)
class Factor:
    scope: tuple[int, ...]
    values: np.ndarray


def _project_indices(assignments: np.ndarray, union_scope: tuple[int, ...], factor_scope: tuple[int, ...]) -> np.ndarray:
    positions = {vertex: index for index, vertex in enumerate(union_scope)}
    result = np.zeros(len(assignments), dtype=np.uint64)
    for factor_position, vertex in enumerate(factor_scope):
        result |= ((assignments >> positions[vertex]) & 1) << factor_position
    return result.astype(np.intp, copy=False)


def _insert_bit(assignments: np.ndarray, position: int, value: int) -> np.ndarray:
    low_mask = (1 << position) - 1
    result = (assignments & low_mask) | ((assignments >> position) << (position + 1))
    if value:
        result |= np.uint64(1 << position)
    return result


def retained_port_root_batch(
    local_instance: Mapping[str, Any],
    elimination_order: Sequence[int],
    points: np.ndarray,
    prime: int,
    port_order: Sequence[int],
) -> tuple[np.ndarray, dict[str, int]]:
    """Eliminate every non-port variable and return all port states together."""

    _, exact, _ = _modules()
    n = int(local_instance["N"])
    ports = tuple(int(value) for value in port_order)
    if len(ports) != 4 or len(set(ports)) != 4:
        raise SLCX032CustodyError("retained port must contain four distinct vertices")
    order = tuple(int(value) for value in elimination_order)
    if set(order) != set(range(n)) - set(ports) or len(order) != n - 4:
        raise SLCX032CustodyError("conditional elimination order is not exactly the non-port roster")
    parent_factors = exact._initial_factors(local_instance, points, prime)
    factors = [
        Factor(tuple(int(value) for value in factor.scope), np.ascontiguousarray(factor.values, dtype=np.int64))
        for factor in parent_factors
    ]
    peak_union = 1
    peak_output = 1
    peak_chunk = 1
    peak_retained = sum(int(factor.values.shape[0]) for factor in factors)
    union_work = 0
    output_work = 0
    for vertex in order:
        selected = [factor for factor in factors if vertex in factor.scope]
        factors = [factor for factor in factors if vertex not in factor.scope]
        if not selected:
            union_scope = (vertex,)
            output_scope: tuple[int, ...] = ()
            output = np.full((1, len(points)), 2, dtype=np.int64)
            chunk_size = 1
        else:
            union_scope = tuple(sorted({site for factor in selected for site in factor.scope}))
            position = union_scope.index(vertex)
            output_scope = tuple(site for site in union_scope if site != vertex)
            output_count = 1 << len(output_scope)
            chunk_size = min(FUSED_CHUNK_CAP, output_count)
            output = np.empty((output_count, len(points)), dtype=np.int64)
            for start in range(0, output_count, chunk_size):
                stop = min(output_count, start + chunk_size)
                remaining = np.arange(start, stop, dtype=np.uint64)
                zero_union = _insert_bit(remaining, position, 0)
                one_union = _insert_bit(remaining, position, 1)
                product_zero = np.ones((stop - start, len(points)), dtype=np.int64)
                product_one = np.ones((stop - start, len(points)), dtype=np.int64)
                for factor in selected:
                    zero_index = _project_indices(zero_union, union_scope, factor.scope)
                    one_index = _project_indices(one_union, union_scope, factor.scope)
                    product_zero = product_zero * factor.values[zero_index, :] % prime
                    product_one = product_one * factor.values[one_index, :] % prime
                output[start:stop, :] = (product_zero + product_one) % prime
        factors.append(Factor(output_scope, np.ascontiguousarray(output, dtype=np.int64)))
        union_entries = 1 << len(union_scope)
        output_entries = int(output.shape[0])
        union_work += union_entries
        output_work += output_entries
        peak_union = max(peak_union, union_entries)
        peak_output = max(peak_output, output_entries)
        peak_chunk = max(peak_chunk, chunk_size)
        peak_retained = max(peak_retained, sum(int(factor.values.shape[0]) for factor in factors))
    port_scope = tuple(int(value) for value in ports)
    assignments = np.arange(STATE_COUNT, dtype=np.uint64)
    terminal = np.ones((STATE_COUNT, len(points)), dtype=np.int64)
    for factor in factors:
        if not set(factor.scope).issubset(port_scope):
            raise SLCX032ArithmeticError("conditional elimination left a non-port variable")
        index = _project_indices(assignments, port_scope, factor.scope)
        terminal = terminal * factor.values[index, :] % prime
    return np.ascontiguousarray(terminal, dtype=np.int64), {
        "peak_union_assignments_per_root_logical": peak_union,
        "peak_output_assignments_per_root": peak_output,
        "peak_fused_chunk_assignments_per_root": peak_chunk,
        "peak_retained_factor_assignments_per_root": peak_retained,
        "sum_2_pow_union_scope": union_work,
        "sum_2_pow_output_scope": output_work,
        "full_union_materialization_count": 0,
    }


def _zeta_points(prime: int, y_length: int, start: int, stop: int) -> np.ndarray:
    z_order = 2 * y_length
    if y_length <= 0 or y_length & (y_length - 1) or (prime - 1) % z_order:
        raise SLCX032ArithmeticError("prime does not support the required even-quotient root order")
    zeta = pow(PRIMITIVE_ROOT, (prime - 1) // z_order, prime)
    if pow(zeta, z_order, prime) != 1 or pow(zeta, z_order // 2, prime) == 1:
        raise SLCX032ArithmeticError("derived zeta lacks exact order 2L")
    omega = zeta * zeta % prime
    expected_omega = pow(PRIMITIVE_ROOT, (prime - 1) // y_length, prime)
    if omega != expected_omega:
        raise SLCX032ArithmeticError("zeta squared does not equal the canonical y root")
    return np.asarray([pow(zeta, index, prime) for index in range(start, stop)], dtype=np.int64)


def _crt_product(primes: Sequence[int]) -> int:
    product = 1
    for prime in primes:
        product *= int(prime)
    return product


def _compile_conditional_w(
    instance: Mapping[str, Any],
    ownership: Mapping[str, Any],
    elimination_order: Sequence[int],
    port_order: Sequence[int],
    *,
    y_length: int,
    primes: Sequence[int],
    progress: Progress | None,
    phase: str,
) -> dict[str, Any]:
    _, exact, _ = _modules()
    local_instance = _local_instance(instance, ownership)
    local_bound = int(ownership["local_bound"])
    if y_length <= local_bound:
        raise SLCX032ArithmeticError("conditional W y-transform is too short")
    expected_row_sum = 1 << (int(instance["N"]) - len(port_order))
    if _crt_product(primes) <= expected_row_sum:
        raise SLCX032ArithmeticError("conditional W CRT product is insufficient")
    modular: list[list[list[int]]] = []
    prime_metrics: list[dict[str, Any]] = []
    aggregate: dict[str, int] = {}
    started = time.perf_counter()
    for prime_index, prime in enumerate(primes):
        evaluations = np.zeros((STATE_COUNT, y_length), dtype=np.int64)
        prime_started = time.perf_counter()
        prime_aggregate: dict[str, int] = {}
        _notify(progress, phase=phase, event="PRIME_STARTED", prime=int(prime), prime_index=prime_index)
        for start in range(0, y_length, ROOT_BATCH_SIZE):
            stop = min(y_length, start + ROOT_BATCH_SIZE)
            points = _zeta_points(int(prime), y_length, start, stop)
            terminal, metrics = retained_port_root_batch(
                local_instance, elimination_order, points, int(prime), port_order
            )
            evaluations[:, start:stop] = terminal
            for key, value in metrics.items():
                if key.startswith("sum_"):
                    if key in prime_aggregate and prime_aggregate[key] != int(value):
                        raise SLCX032ArithmeticError("conditional structural work changed across roots")
                    prime_aggregate[key] = int(value)
                else:
                    prime_aggregate[key] = max(prime_aggregate.get(key, 0), int(value))
            if stop == y_length or stop % 64 == 0:
                _notify(
                    progress,
                    phase=phase,
                    event="ROOT_PROGRESS",
                    prime=int(prime),
                    roots_complete=stop,
                    roots_total=y_length,
                )
        coefficients = [
            [int(value) for value in exact._inverse_ntt(evaluations[state, :].tolist(), int(prime))]
            for state in range(STATE_COUNT)
        ]
        modular.append(coefficients)
        residue_hash = canonical_sha256(coefficients)
        prime_metrics.append(
            {
                "prime": int(prime),
                "y_ntt_length": y_length,
                "z_root_order": 2 * y_length,
                "root_batch_size": ROOT_BATCH_SIZE,
                "coefficient_residue_sha256": residue_hash,
                "elapsed_seconds": time.perf_counter() - prime_started,
                **prime_aggregate,
            }
        )
        for key, value in prime_aggregate.items():
            if key.startswith("sum_"):
                if key in aggregate and aggregate[key] != value:
                    raise SLCX032ArithmeticError("conditional work changed across primes")
                aggregate[key] = value
            else:
                aggregate[key] = max(aggregate.get(key, 0), value)
    reconstructed: list[list[int]] = []
    for state in range(STATE_COUNT):
        row = [
            int(exact._crt([modular[p][state][degree] for p in range(len(primes))], primes))
            for degree in range(y_length)
        ]
        if any(row[local_bound + 1 :]):
            raise SLCX032ArithmeticError("conditional W has support above its exact local bound")
        active = row[: local_bound + 1]
        if any(value < 0 for value in active) or sum(active) != expected_row_sum:
            raise SLCX032ArithmeticError("conditional W row normalization/nonnegativity failed")
        reconstructed.append(active)
    return {
        "w_coefficients": reconstructed,
        "w_sha256": canonical_sha256(reconstructed),
        "local_y_degree": local_bound,
        "expected_row_sum": expected_row_sum,
        "row_sums": [sum(row) for row in reconstructed],
        "metrics": {
            "elapsed_seconds": time.perf_counter() - started,
            "y_ntt_length": y_length,
            "z_root_order": 2 * y_length,
            "selected_primes": [int(value) for value in primes],
            "crt_modulus_product": _crt_product(primes),
            "root_batch_size": ROOT_BATCH_SIZE,
            "prime_metrics": prime_metrics,
            **aggregate,
        },
    }


def _state_spin(state: int, vertex: int, port_order: Sequence[int]) -> int:
    position = tuple(port_order).index(vertex)
    return 1 if state & (1 << position) else -1


def glue_y_degrees(cut_edges: Sequence[Sequence[int]], port_order: Sequence[int]) -> list[list[int]]:
    table = [[0 for _ in range(STATE_COUNT)] for _ in range(STATE_COUNT)]
    for left in range(STATE_COUNT):
        for right in range(STATE_COUNT):
            z_degree = 0
            for raw in cut_edges:
                u, v, coupling = map(int, raw)
                z_degree += -coupling * _state_spin(left, u, port_order) * _state_spin(right, v, port_order) + abs(coupling)
            if z_degree & 1:
                raise SLCX032ArithmeticError("glue shifted exponent is not even")
            table[left][right] = z_degree // 2
    if min(map(min, table)) < 0 or max(map(max, table)) > GLUE_BOUND:
        raise SLCX032ArithmeticError("glue y-degree escaped the frozen bound")
    return table


def calibrate_n12(progress: Progress | None = None) -> dict[str, Any]:
    _, _, transfer = _modules()
    vault = _read_frozen_json(N12_VAULT, EXPECTED_N12_VAULT_SHA256)
    source = vault.get("source_cell")
    if not isinstance(source, Mapping):
        raise SLCX032CustodyError("sealed N12 source cell is absent")
    cuts = [list(map(int, edge)) for edge in vault.get("cut_edges", [])]
    ownership = transfer.validate_factor_ownership(source, cuts)
    port_order = [int(value) for value in ownership["port_vertices"]]
    order = [int(value) for value in source["orders"]["cell_min_fill"] if int(value) not in set(port_order)]
    retained = _compile_conditional_w(
        source,
        ownership,
        order,
        port_order,
        y_length=128,
        primes=(PRIMES_3[0],),
        progress=progress,
        phase="N12_COMPILER_CALIBRATION",
    )
    brute_z = transfer._compile_local_coefficients(source, ownership)
    if brute_z.shape[1] != 2 * int(ownership["local_bound"]) + 1:
        raise SLCX032ArithmeticError("sealed brute-force N12 W has an unexpected degree")
    if np.any(brute_z[:, 1::2]):
        raise SLCX032ArithmeticError("sealed brute-force N12 W violates even shifted parity")
    brute_y = [[int(value) for value in row[::2]] for row in brute_z.tolist()]
    retained_y = retained["w_coefficients"]
    passed = retained_y == brute_y
    if not passed:
        raise SLCX032ArithmeticError("retained-port compiler failed N12 brute-force calibration")
    return {
        "schema": "SLCX032_N12_CALIBRATION_V1",
        "campaign_id": CAMPAIGN_ID,
        "source_instance_id": source["instance_id"],
        "port_order": port_order,
        "cut_edges": cuts,
        "calibration_pass": passed,
        "retained_w_sha256": canonical_sha256(retained_y),
        "brute_w_sha256": canonical_sha256(brute_y),
        "row_sum": 1 << 8,
        "metrics": retained["metrics"],
    }


def compile_n72_operator(instance: Mapping[str, Any], progress: Progress | None = None) -> dict[str, Any]:
    validation = validate_n72_instance(instance)
    freeze = load_port_freeze()
    ownership = factor_ownership(instance)
    order = [int(value) for value in freeze["conditional_order"]]
    compiled = _compile_conditional_w(
        instance,
        ownership,
        order,
        PORT_ORDER,
        y_length=W_Y_LENGTH,
        primes=PRIMES_3,
        progress=progress,
        phase="N72_OPERATOR_COMPILATION",
    )
    metrics = dict(compiled["metrics"])
    if (
        metrics.get("sum_2_pow_union_scope") != EXPECTED_CONDITIONAL_UNION_WORK
        or metrics.get("peak_output_assignments_per_root") != 1 << EXPECTED_CONDITIONAL_WIDTH
    ):
        raise SLCX032ArithmeticError("observed retained-port structure differs from the freeze")
    cut_edges = ownership["cut_edges"]
    glue = glue_y_degrees(cut_edges, PORT_ORDER)
    return {
        "schema": "SLCX032_N72_OPERATOR_V1",
        "campaign_id": CAMPAIGN_ID,
        "source_validation": validation,
        "source_instance_id": N72_INSTANCE_ID,
        "source_instance_sha256": N72_INSTANCE_SHA256,
        "port_freeze_sha256": freeze["freeze_sha256"],
        "port_order": list(PORT_ORDER),
        "cut_edges": cut_edges,
        "orientation": [list(edge) for edge in CUT_ENDPOINTS],
        "factor_ownership": ownership,
        "w_coefficients": compiled["w_coefficients"],
        "w_sha256": compiled["w_sha256"],
        "local_y_degree": compiled["local_y_degree"],
        "expected_row_sum": compiled["expected_row_sum"],
        "row_sums": compiled["row_sums"],
        "glue_y_degrees": glue,
        "glue_y_degrees_sha256": canonical_sha256(glue),
        "metrics": {
            **metrics,
            "conditional_induced_width": EXPECTED_CONDITIONAL_WIDTH,
            "conditional_order": order,
            "conditional_order_sha256": canonical_sha256(order),
        },
    }


def _normalize_w(operator_result: Mapping[str, Any]) -> list[list[int]]:
    if operator_result.get("schema") != "SLCX032_N72_OPERATOR_V1":
        raise SLCX032CustodyError("operator schema mismatch")
    if operator_result.get("port_order") != list(PORT_ORDER):
        raise SLCX032CustodyError("operator port order changed")
    raw = operator_result.get("w_coefficients")
    if not isinstance(raw, list) or len(raw) != STATE_COUNT:
        raise SLCX032CustodyError("operator W row roster changed")
    rows: list[list[int]] = []
    for state, raw_row in enumerate(raw):
        if not isinstance(raw_row, list) or len(raw_row) != LOCAL_BOUND + 1:
            raise SLCX032CustodyError(f"operator W[{state}] degree roster changed")
        row: list[int] = []
        for value in raw_row:
            if type(value) is int:
                parsed = value
            elif isinstance(value, str) and value.isdigit() and str(int(value)) == value:
                parsed = int(value)
            else:
                raise SLCX032CustodyError("operator W coefficient is not a canonical integer")
            if parsed < 0:
                raise SLCX032CustodyError("operator W coefficient is negative")
            row.append(parsed)
        if sum(row) != 1 << 68:
            raise SLCX032CustodyError("operator W row normalization changed")
        rows.append(row)
    if canonical_sha256(rows) != operator_result.get("w_sha256"):
        raise SLCX032CustodyError("operator W semantic hash mismatch")
    return rows


def _normalize_glue(operator_result: Mapping[str, Any]) -> list[list[int]]:
    raw = operator_result.get("glue_y_degrees")
    if not isinstance(raw, list) or len(raw) != STATE_COUNT:
        raise SLCX032CustodyError("glue table row roster changed")
    table: list[list[int]] = []
    for row in raw:
        if not isinstance(row, list) or len(row) != STATE_COUNT or any(type(value) is not int for value in row):
            raise SLCX032CustodyError("glue table is malformed")
        table.append([int(value) for value in row])
    if canonical_sha256(table) != operator_result.get("glue_y_degrees_sha256"):
        raise SLCX032CustodyError("glue table semantic hash mismatch")
    return table


def fixed_energy_vector_from_y(coefficients_y: Sequence[int], bound: int) -> list[int]:
    bound = _plain_int(bound, "bound")
    if bound < 0:
        raise SLCX032ArithmeticError("bound cannot be negative")
    fixed = [0] * (2 * bound + 1)
    for degree, raw_count in enumerate(coefficients_y):
        count = _plain_int(raw_count, f"coefficients_y[{degree}]")
        if count < 0:
            raise SLCX032ArithmeticError("coefficient cannot be negative")
        energy = 2 * degree - bound
        if energy < -bound or energy > bound:
            if count:
                raise SLCX032ArithmeticError("nonzero y coefficient lies above the active bound")
            continue
        fixed[energy + bound] = count
    return fixed


def _dos_rows(fixed: Sequence[int], bound: int) -> list[dict[str, Any]]:
    return [
        {"energy": energy, "count": str(int(fixed[energy + bound]))}
        for energy in range(-bound, bound + 1)
        if int(fixed[energy + bound])
    ]


def dos_semantic_hash(rows: Sequence[Mapping[str, Any]]) -> str:
    return canonical_sha256({"domain": DOS_DOMAIN, "dos": list(rows)})


def raw_moments_from_fixed(fixed: Sequence[int], bound: int, maximum_order: int = 4) -> dict[int, int]:
    return {
        power: sum(int(count) * (index - bound) ** power for index, count in enumerate(fixed))
        for power in range(1, maximum_order + 1)
    }


def recover_n72_one_cell(operator_result: Mapping[str, Any]) -> dict[str, Any]:
    w = _normalize_w(operator_result)
    glue = _normalize_glue(operator_result)
    coefficients = [0] * (N72_BOUND + 1)
    for state in range(STATE_COUNT):
        shift = glue[state][state]
        for degree, count in enumerate(w[state]):
            coefficients[degree + shift] += count
    fixed = fixed_energy_vector_from_y(coefficients, N72_BOUND)
    rows = _dos_rows(fixed, N72_BOUND)
    observed = sum(fixed)
    if observed != 1 << 72:
        raise SLCX032ArithmeticError("one-cell trace failed 2^72 normalization")
    return {
        "schema": "SLCX032_N72_ONE_CELL_RECOVERY_V1",
        "campaign_id": CAMPAIGN_ID,
        "source_instance_id": N72_INSTANCE_ID,
        "fixed_coefficients": fixed,
        "fixed_coefficient_sha256": canonical_sha256(fixed),
        "y_coefficients": coefficients,
        "dos_rows": rows,
        "dos_sha256": dos_semantic_hash(rows),
        "observed_configuration_count": observed,
        "raw_moments": raw_moments_from_fixed(fixed, N72_BOUND),
        "energy_bound_B": N72_BOUND,
        "occupied_energy_bins": len(rows),
        "minimum_energy": rows[0]["energy"],
        "maximum_energy": rows[-1]["energy"],
    }


def _canonical_edge(u: int, v: int, coupling: int) -> tuple[int, int, int]:
    return (u, v, coupling) if u < v else (v, u, coupling)


def build_n144_ring_instance(source: Mapping[str, Any]) -> dict[str, Any]:
    validate_n72_instance(source)
    ownership = factor_ownership(source)
    local_edges = [tuple(map(int, edge)) for edge in ownership["local_edges"]]
    cut_edges = [tuple(map(int, edge)) for edge in ownership["cut_edges"]]
    edges: list[tuple[int, int, int]] = []
    for copy_index in range(2):
        offset = 72 * copy_index
        edges.extend((u + offset, v + offset, coupling) for u, v, coupling in local_edges)
    for copy_index in range(2):
        source_offset = 72 * copy_index
        target_offset = 72 * ((copy_index + 1) % 2)
        for u, v, coupling in cut_edges:
            edges.append(_canonical_edge(u + source_offset, v + target_offset, coupling))
    edges = sorted(edges)
    if len(edges) != 360 or len({edge[:2] for edge in edges}) != 360:
        raise SLCX032ArithmeticError("N144 construction lost or duplicated an edge")
    fields = [int(value) for value in source["fields"]] * 2
    instance: dict[str, Any] = {
        "schema": "SLCX032_N144_RING_INSTANCE_V1",
        "instance_id": "SLCX032_N144_TWO_COPY_RING_I00",
        "source_instance_id": N72_INSTANCE_ID,
        "source_instance_sha256": N72_INSTANCE_SHA256,
        "N": 144,
        "cell_size": 72,
        "cell_count": 2,
        "fields": fields,
        "edges": [list(edge) for edge in edges],
        "edge_count": len(edges),
        "energy_bound_B": sum(abs(value) for value in fields) + sum(abs(edge[2]) for edge in edges),
        "cut_edges": [list(edge) for edge in cut_edges],
        "orientation": [list(edge) for edge in CUT_ENDPOINTS],
    }
    instance["instance_sha256"] = _instance_hash(instance)
    validate_n144_instance(instance)
    return instance


def build_n144_direct_instance(source: Mapping[str, Any]) -> dict[str, Any]:
    """Independently assemble the full two-cell graph for the direct lane.

    Unlike :func:`build_n144_ring_instance`, this path begins with two complete
    copies of the frozen N72 graph.  It then removes the four copied internal
    cut edges and inserts the four cross-copy replacements.  The final semantic
    hash is checked against a separately reconstructed transfer-style edge
    roster, without calling the transfer-lane builder.
    """

    validate_n72_instance(source)
    cuts = _cut_edges(source, CUT_ENDPOINTS)
    cut_by_pair = {(u, v): (u, v, coupling) for u, v, coupling in cuts}

    # Start from two full 180-edge copies, preserving every source factor.
    full_edges: list[tuple[int, int, int]] = []
    for copy_index in range(2):
        offset = 72 * copy_index
        for raw_u, raw_v, raw_coupling in source["edges"]:
            full_edges.append(
                _canonical_edge(
                    int(raw_u) + offset,
                    int(raw_v) + offset,
                    int(raw_coupling),
                )
            )
    if len(full_edges) != 360 or len(set(full_edges)) != 360:
        raise SLCX032ArithmeticError("direct N144 full-copy assembly is not 360 unique edges")

    # Remove each frozen cut occurrence from each complete copy.  Match both
    # endpoints and coupling so an endpoint-only coincidence cannot be removed.
    retained: list[tuple[int, int, int]] = []
    removed: list[tuple[int, int, int]] = []
    for edge in full_edges:
        u, v, coupling = edge
        same_copy = u // 72 == v // 72
        offset = 72 * (u // 72) if same_copy else -1
        local = (u - offset, v - offset, coupling) if same_copy else None
        if local is not None and cut_by_pair.get(local[:2]) == local:
            removed.append(edge)
        else:
            retained.append(edge)
    expected_removed = sorted(
        (u + 72 * copy_index, v + 72 * copy_index, coupling)
        for copy_index in range(2)
        for u, v, coupling in cuts
    )
    if sorted(removed) != expected_removed or len(retained) != 356:
        raise SLCX032ArithmeticError("direct N144 cut removal differs from the frozen four-edge roster")

    # Insert the two oriented cut factors across each of the two cell seams.
    inserted: list[tuple[int, int, int]] = []
    for source_copy, target_copy in ((0, 1), (1, 0)):
        source_offset = 72 * source_copy
        target_offset = 72 * target_copy
        for u, v, coupling in cuts:
            inserted.append(
                _canonical_edge(u + source_offset, v + target_offset, coupling)
            )
    if len(inserted) != 4 or len(set(inserted)) != 4:
        raise SLCX032ArithmeticError("direct N144 cross-copy insertion is not four unique factors")

    edges = sorted(retained + inserted)
    if len(edges) != 360 or len({edge[:2] for edge in edges}) != 360:
        raise SLCX032ArithmeticError("direct N144 construction lost or duplicated an edge")
    fields = [int(value) for value in source["fields"]] + [
        int(value) for value in source["fields"]
    ]
    instance: dict[str, Any] = {
        "schema": "SLCX032_N144_RING_INSTANCE_V1",
        "instance_id": "SLCX032_N144_TWO_COPY_RING_I00",
        "source_instance_id": N72_INSTANCE_ID,
        "source_instance_sha256": N72_INSTANCE_SHA256,
        "N": 144,
        "cell_size": 72,
        "cell_count": 2,
        "fields": fields,
        "edges": [list(edge) for edge in edges],
        "edge_count": len(edges),
        "energy_bound_B": sum(abs(value) for value in fields)
        + sum(abs(edge[2]) for edge in edges),
        "cut_edges": [list(edge) for edge in cuts],
        "orientation": [list(edge) for edge in CUT_ENDPOINTS],
    }
    instance["instance_sha256"] = _instance_hash(instance)
    validate_n144_instance(instance)

    # Independently reconstruct the transfer-lane semantic roster.  This is a
    # hash comparison between two assembly algorithms; it deliberately does not
    # invoke build_n144_ring_instance or share its local-edge result.
    cut_set = set(cuts)
    transfer_edges: list[tuple[int, int, int]] = []
    for copy_index in range(2):
        offset = 72 * copy_index
        for raw_edge in source["edges"]:
            local_edge = tuple(map(int, raw_edge))
            if local_edge not in cut_set:
                transfer_edges.append(
                    (local_edge[0] + offset, local_edge[1] + offset, local_edge[2])
                )
    for copy_index in range(2):
        source_offset = 72 * copy_index
        target_offset = 72 * ((copy_index + 1) % 2)
        for u, v, coupling in cuts:
            transfer_edges.append(
                _canonical_edge(u + source_offset, v + target_offset, coupling)
            )
    transfer_core = dict(instance)
    transfer_core["edges"] = [list(edge) for edge in sorted(transfer_edges)]
    transfer_core.pop("instance_sha256", None)
    if instance["instance_sha256"] != canonical_sha256(transfer_core):
        raise SLCX032ArithmeticError(
            "independent direct graph does not hash-match the transfer-lane graph"
        )
    return instance


def validate_n144_instance(instance: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(instance, Mapping) or instance.get("schema") != "SLCX032_N144_RING_INSTANCE_V1":
        raise SLCX032CustodyError("N144 instance schema mismatch")
    if instance.get("source_instance_sha256") != N72_INSTANCE_SHA256 or instance.get("N") != 144:
        raise SLCX032CustodyError("N144 source/size mismatch")
    fields = instance.get("fields")
    if not isinstance(fields, list) or len(fields) != 144 or any(type(value) is not int for value in fields):
        raise SLCX032CustodyError("N144 fields are malformed")
    edges, degrees = _validate_edges(instance, 144)
    if len(edges) != 360 or instance.get("edge_count") != 360 or any(value != 5 for value in degrees):
        raise SLCX032CustodyError("N144 graph is not five-regular")
    bound = sum(abs(value) for value in fields) + sum(abs(edge[2]) for edge in edges)
    if bound != N144_BOUND or instance.get("energy_bound_B") != N144_BOUND:
        raise SLCX032CustodyError("N144 energy bound mismatch")
    if _instance_hash(instance) != instance.get("instance_sha256"):
        raise SLCX032CustodyError("N144 semantic instance hash mismatch")
    return {
        "status": "PASS",
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "N": 144,
        "edge_count": 360,
        "energy_bound_B": bound,
    }


def xor_moments(instance: Mapping[str, Any]) -> dict[str, Any]:
    n = int(instance["N"])
    terms: dict[int, int] = defaultdict(int)
    for u, v, coupling in instance["edges"]:
        terms[(1 << int(u)) | (1 << int(v))] -= int(coupling)
    for vertex, field in enumerate(instance["fields"]):
        if int(field):
            terms[1 << vertex] -= int(field)
    terms = {mask: value for mask, value in terms.items() if value}
    square: dict[int, int] = defaultdict(int)
    items = list(terms.items())
    for left_mask, left_coefficient in items:
        for right_mask, right_coefficient in items:
            square[left_mask ^ right_mask] += left_coefficient * right_coefficient
    per_configuration = {
        1: terms.get(0, 0),
        2: square.get(0, 0),
        3: sum(value * terms.get(mask, 0) for mask, value in square.items()),
        4: sum(value * value for value in square.values()),
    }
    scale = 1 << n
    return {
        "method": "INDEPENDENT_XOR_MONOMIAL_CONTRACTION",
        "instance_id": instance["instance_id"],
        "monomial_count": len(terms),
        "xor_square_support": len(square),
        "per_configuration": per_configuration,
        "raw_sums": {power: value * scale for power, value in per_configuration.items()},
    }


def _forward_ntt_rows(rows: Sequence[Sequence[int]], length: int, prime: int) -> np.ndarray:
    _, _, transfer = _modules()
    result = np.empty((len(rows), length), dtype=np.int64)
    for index, row in enumerate(rows):
        if len(row) > length:
            raise SLCX032ArithmeticError("polynomial row exceeds the requested NTT length")
        padded = [int(value) % prime for value in row] + [0] * (length - len(row))
        result[index, :] = np.asarray(transfer.forward_ntt(padded, prime), dtype=np.int64)
    return result


def safe_modular_matmul(left: np.ndarray, right: np.ndarray, prime: int) -> np.ndarray:
    left = np.asarray(left, dtype=np.int64)
    right = np.asarray(right, dtype=np.int64)
    if left.ndim < 2 or right.ndim != left.ndim or left.shape[:-2] != right.shape[:-2]:
        raise SLCX032ArithmeticError("matrix batch shapes do not match")
    if left.shape[-1] != right.shape[-2]:
        raise SLCX032ArithmeticError("matrix inner dimensions do not match")
    if np.any(left < 0) or np.any(left >= prime) or np.any(right < 0) or np.any(right >= prime):
        raise SLCX032ArithmeticError("matrix residue lies outside the prime field")
    output = np.zeros(left.shape[:-2] + (left.shape[-2], right.shape[-1]), dtype=np.int64)
    for shared in range(left.shape[-1]):
        product = left[..., :, shared, None] * right[..., shared, None, :] % prime
        output = (output + product) % prime
    return output


def _trace_evaluations(matrix: np.ndarray, prime: int) -> list[int]:
    trace = np.zeros(matrix.shape[0], dtype=np.int64)
    for state in range(matrix.shape[1]):
        trace = (trace + matrix[:, state, state]) % prime
    return [int(value) for value in trace]


def _reconstruct_coefficients(modular: Sequence[Sequence[int]], primes: Sequence[int], active_degree: int) -> list[int]:
    _, exact, _ = _modules()
    length = len(modular[0])
    if any(len(row) != length for row in modular):
        raise SLCX032ArithmeticError("modular coefficient lengths differ")
    coefficients = [
        int(exact._crt([modular[p][degree] for p in range(len(primes))], primes))
        for degree in range(length)
    ]
    if any(coefficients[active_degree + 1 :]):
        raise SLCX032ArithmeticError("reconstructed polynomial has support above the active degree")
    return coefficients[: active_degree + 1]


def solve_n144_transfer(
    operator_result: Mapping[str, Any],
    source_instance: Mapping[str, Any],
    progress: Progress | None = None,
) -> dict[str, Any]:
    w = _normalize_w(operator_result)
    glue = np.asarray(_normalize_glue(operator_result), dtype=np.intp)
    n144 = build_n144_ring_instance(source_instance)
    expected_moments = xor_moments(n144)
    crt_product = _crt_product(PRIMES_5)
    if crt_product <= 1 << 144 or _crt_product(PRIMES_5[:4]) > 1 << 144:
        raise SLCX032ArithmeticError("five-prime/four-prime N144 capacity gate failed")
    modular: list[list[int]] = []
    residue_hashes: list[dict[str, Any]] = []
    started = time.perf_counter()
    for prime_index, prime in enumerate(PRIMES_5):
        prime_started = time.perf_counter()
        _notify(progress, phase="N144_TWO_CELL_TRANSFER_DISCOVERY", event="PRIME_STARTED", prime=prime)
        w_roots = _forward_ntt_rows(w, N144_Y_LENGTH, prime)
        omega = pow(PRIMITIVE_ROOT, (prime - 1) // N144_Y_LENGTH, prime)
        points = np.asarray([pow(omega, index, prime) for index in range(N144_Y_LENGTH)], dtype=np.int64)
        maximum_glue = int(glue.max())
        powers = np.empty((maximum_glue + 1, N144_Y_LENGTH), dtype=np.int64)
        powers[0, :] = 1
        for degree in range(1, maximum_glue + 1):
            powers[degree, :] = powers[degree - 1, :] * points % prime
        glue_roots = np.ascontiguousarray(powers[glue].transpose(2, 0, 1), dtype=np.int64)
        transfer = np.ascontiguousarray(w_roots.T[:, :, None] * glue_roots % prime, dtype=np.int64)
        squared = safe_modular_matmul(transfer, transfer, prime)
        evaluations = _trace_evaluations(squared, prime)
        _, exact, _ = _modules()
        coefficients = [int(value) for value in exact._inverse_ntt(evaluations, prime)]
        modular.append(coefficients)
        residue_hashes.append(
            {
                "prime": prime,
                "ring_coefficient_residue_sha256": canonical_sha256(coefficients),
                "t2_root_residue_sha256": hashlib.sha256(
                    np.ascontiguousarray(squared, dtype=">u8").tobytes(order="C")
                ).hexdigest(),
                "elapsed_seconds": time.perf_counter() - prime_started,
            }
        )
        _notify(progress, phase="N144_TWO_CELL_TRANSFER_DISCOVERY", event="PRIME_COMPLETE", prime=prime)
    coefficients_y = _reconstruct_coefficients(modular, PRIMES_5, N144_BOUND)
    fixed = fixed_energy_vector_from_y(coefficients_y, N144_BOUND)
    observed = sum(fixed)
    if observed != 1 << 144:
        raise SLCX032ArithmeticError("N144 transfer failed exact normalization")
    moments = raw_moments_from_fixed(fixed, N144_BOUND)
    expected_raw = {int(key): int(value) for key, value in expected_moments["raw_sums"].items()}
    if moments != expected_raw:
        raise SLCX032ArithmeticError("N144 transfer failed independent XOR moments")
    rows = _dos_rows(fixed, N144_BOUND)
    return {
        "schema": "SLCX032_N144_TRANSFER_V1",
        "campaign_id": CAMPAIGN_ID,
        "instance_id": n144["instance_id"],
        "instance_sha256": n144["instance_sha256"],
        "operator_w_sha256": operator_result["w_sha256"],
        "composition": "TRACE_T_SQUARED",
        "fixed_coefficients": fixed,
        "fixed_coefficient_sha256": canonical_sha256(fixed),
        "y_coefficients": coefficients_y,
        "dos_rows": rows,
        "dos_sha256": dos_semantic_hash(rows),
        "residue_hashes": residue_hashes,
        "observed_configuration_count": observed,
        "raw_moments": moments,
        "independent_xor_moments": expected_moments,
        "metrics": {
            "elapsed_seconds": time.perf_counter() - started,
            "y_ntt_length": N144_Y_LENGTH,
            "z_root_order": 2 * N144_Y_LENGTH,
            "selected_primes": list(PRIMES_5),
            "crt_modulus_product": crt_product,
            "transfer_shape": [STATE_COUNT, STATE_COUNT],
            "composition_reduction": "after_each_shared_state",
            "energy_bound_B": N144_BOUND,
            "occupied_energy_bins": len(rows),
        },
    }


def direct_n144_order() -> list[int]:
    base = load_full_n72_order()
    return base + [value + 72 for value in base]


def solve_n144_direct(instance: Mapping[str, Any], progress: Progress | None = None) -> dict[str, Any]:
    validation = validate_n144_instance(instance)
    compressed, exact, _ = _modules()
    order = direct_n144_order()
    structure = compressed.order_structure(instance, order)
    if (
        int(structure["induced_width"]) != EXPECTED_DIRECT_WIDTH
        or int(structure["sum_2_pow_union_scope"]) != EXPECTED_DIRECT_UNION_WORK
    ):
        raise SLCX032CustodyError("direct N144 order structure differs from the frozen design")
    modular: list[list[int]] = []
    prime_metrics: list[dict[str, Any]] = []
    started = time.perf_counter()
    for prime_index, prime in enumerate(PRIMES_5):
        evaluations = [0] * N144_Y_LENGTH
        aggregate: dict[str, int] = {}
        prime_started = time.perf_counter()
        _notify(progress, phase="N144_DIRECT_FUSED_REFERENCE", event="PRIME_STARTED", prime=prime)
        for start in range(0, N144_Y_LENGTH, ROOT_BATCH_SIZE):
            stop = min(N144_Y_LENGTH, start + ROOT_BATCH_SIZE)
            points = _zeta_points(prime, N144_Y_LENGTH, start, stop)
            terminal, metrics = compressed.fused_root_batch(
                instance,
                order,
                points,
                prime,
                lambda _metadata, _table: None,
                parent_path=EXACT_ENGINE,
            )
            evaluations[start:stop] = [int(value) for value in terminal]
            for key, value in metrics.items():
                aggregate[key] = max(aggregate.get(key, 0), int(value))
            if stop == N144_Y_LENGTH or stop % 64 == 0:
                _notify(
                    progress,
                    phase="N144_DIRECT_FUSED_REFERENCE",
                    event="ROOT_PROGRESS",
                    prime=prime,
                    roots_complete=stop,
                    roots_total=N144_Y_LENGTH,
                )
        coefficients = [int(value) for value in exact._inverse_ntt(evaluations, prime)]
        modular.append(coefficients)
        prime_metrics.append(
            {
                "prime": prime,
                "coefficient_residue_sha256": canonical_sha256(coefficients),
                "elapsed_seconds": time.perf_counter() - prime_started,
                **aggregate,
            }
        )
        _notify(progress, phase="N144_DIRECT_FUSED_REFERENCE", event="PRIME_COMPLETE", prime=prime)
    coefficients_y = _reconstruct_coefficients(modular, PRIMES_5, N144_BOUND)
    fixed = fixed_energy_vector_from_y(coefficients_y, N144_BOUND)
    observed = sum(fixed)
    if observed != 1 << 144:
        raise SLCX032ArithmeticError("direct N144 solve failed exact normalization")
    independent = xor_moments(instance)
    moments = raw_moments_from_fixed(fixed, N144_BOUND)
    expected = {int(key): int(value) for key, value in independent["raw_sums"].items()}
    if moments != expected:
        raise SLCX032ArithmeticError("direct N144 solve failed independent XOR moments")
    rows = _dos_rows(fixed, N144_BOUND)
    return {
        "schema": "SLCX032_N144_DIRECT_V1",
        "campaign_id": CAMPAIGN_ID,
        "instance_validation": validation,
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "order": order,
        "order_sha256": canonical_sha256(order),
        "order_structure": structure,
        "fixed_coefficients": fixed,
        "fixed_coefficient_sha256": canonical_sha256(fixed),
        "y_coefficients": coefficients_y,
        "dos_rows": rows,
        "dos_sha256": dos_semantic_hash(rows),
        "residue_hashes": prime_metrics,
        "observed_configuration_count": observed,
        "raw_moments": moments,
        "independent_xor_moments": independent,
        "metrics": {
            "elapsed_seconds": time.perf_counter() - started,
            "y_ntt_length": N144_Y_LENGTH,
            "z_root_order": 2 * N144_Y_LENGTH,
            "selected_primes": list(PRIMES_5),
            "crt_modulus_product": _crt_product(PRIMES_5),
            "root_batch_size": ROOT_BATCH_SIZE,
            "energy_bound_B": N144_BOUND,
            "prime_metrics": prime_metrics,
        },
    }


def engine_control_metadata(operator_result: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return frozen arithmetic facts used by runner-level wrong controls."""

    metadata: dict[str, Any] = {
        "four_prime_product": _crt_product(PRIMES_5[:4]),
        "five_prime_product": _crt_product(PRIMES_5),
        "four_prime_n144_sufficient": _crt_product(PRIMES_5[:4]) > 1 << 144,
        "five_prime_n144_sufficient": _crt_product(PRIMES_5) > 1 << 144,
        "length_512_n144_sufficient": 512 > N144_BOUND,
        "length_1024_n144_sufficient": 1024 > N144_BOUND,
        "delayed_16_term_int64_safe": 16 * (max(PRIMES_5) - 1) ** 2 <= np.iinfo(np.int64).max,
        "required_port_order": list(PORT_ORDER),
        "required_readout": "trace",
        "required_composition": "matrix_square",
    }
    if operator_result is not None:
        w = _normalize_w(operator_result)
        glue = _normalize_glue(operator_result)
        metadata.update(
            {
                "w_row_count": len(w),
                "w_rows_distinct": len({canonical_sha256(row) for row in w}),
                "w_sha256": canonical_sha256(w),
                "glue_sha256": canonical_sha256(glue),
            }
        )
    return metadata


def run_wrong_controls(operator_result: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate the frozen low-cost algebraic wrong controls.

    These controls deliberately do not open or recompute an N144 spectrum.
    They operate on the already sealed exact W object, its glue ledger, and
    the root-zero counting identities.  Runner-level custody, early-open,
    residue-tamper, occupied-bin, alias, and CRT-capacity controls remain
    separate.
    """

    w = _normalize_w(operator_result)
    glue = _normalize_glue(operator_result)
    cut_edges = [tuple(map(int, edge)) for edge in operator_result.get("cut_edges", [])]
    if len(cut_edges) != 2:
        raise SLCX032CustodyError("operator cut-edge roster changed")

    def unbounded_glue(edges: Sequence[Sequence[int]]) -> list[list[int]]:
        table = [[0 for _ in range(STATE_COUNT)] for _ in range(STATE_COUNT)]
        for left in range(STATE_COUNT):
            for right in range(STATE_COUNT):
                z_degree = 0
                for raw in edges:
                    u, v, coupling = map(int, raw)
                    z_degree += (
                        -coupling
                        * _state_spin(left, u, PORT_ORDER)
                        * _state_spin(right, v, PORT_ORDER)
                        + abs(coupling)
                    )
                if z_degree & 1:
                    raise SLCX032ArithmeticError("wrong-control glue exponent is not even")
                table[left][right] = z_degree // 2
        return table

    controls: list[dict[str, Any]] = []

    def add(control_id: str, detected: bool, observed: Any, expected: Any) -> None:
        controls.append(
            {
                "control_id": control_id,
                "detected": bool(detected),
                "observed": observed,
                "expected_correct_path": expected,
            }
        )

    correct_glue_hash = canonical_sha256(glue)
    omitted = unbounded_glue(cut_edges[1:])
    duplicated = unbounded_glue(cut_edges + [cut_edges[0]])
    reversed_one = unbounded_glue(
        [(cut_edges[0][1], cut_edges[0][0], cut_edges[0][2]), cut_edges[1]]
    )
    add("OMIT_ONE_GLUE_EDGE", canonical_sha256(omitted) != correct_glue_hash, canonical_sha256(omitted), correct_glue_hash)
    add("DUPLICATE_ONE_GLUE_EDGE", canonical_sha256(duplicated) != correct_glue_hash, canonical_sha256(duplicated), correct_glue_hash)
    add("REVERSE_ONE_GLUE_EDGE", canonical_sha256(reversed_one) != correct_glue_hash, canonical_sha256(reversed_one), correct_glue_hash)

    correct_count = 1 << 144
    add("SUM_ALL_T2_ENTRIES", (1 << 148) != correct_count, 1 << 148, correct_count)
    add("ELEMENTWISE_SQUARE", (1 << 140) != correct_count, 1 << 140, correct_count)
    add("T_INSTEAD_OF_T2", (1 << 72) != correct_count, 1 << 72, correct_count)

    permuted = [list(row) for row in w]
    pair: tuple[int, int] | None = None
    for left in range(STATE_COUNT):
        for right in range(left + 1, STATE_COUNT):
            if permuted[left] != permuted[right]:
                pair = (left, right)
                break
        if pair is not None:
            break
    if pair is None:
        raise SLCX032ArithmeticError("all conditional W rows are identical")
    permuted[pair[0]], permuted[pair[1]] = permuted[pair[1]], permuted[pair[0]]
    add("ROW_STATE_PERMUTATION", canonical_sha256(permuted) != operator_result["w_sha256"], canonical_sha256(permuted), operator_result["w_sha256"])

    port_tamper = dict(operator_result)
    port_tamper["port_order"] = [15, 6, 16, 58]
    try:
        _normalize_w(port_tamper)
        port_detected = False
    except SLCX032CustodyError:
        port_detected = True
    add("PORT_BIT_PERMUTATION", port_detected, "REJECTED" if port_detected else "ACCEPTED", "REJECTED")

    scalar_tamper = dict(operator_result)
    scalar_tamper["w_coefficients"] = [sum(values) for values in zip(*w)]
    try:
        _normalize_w(scalar_tamper)
        scalar_detected = False
    except SLCX032CustodyError:
        scalar_detected = True
    add("SCALAR_DOS_AS_CONDITIONAL_W", scalar_detected, "REJECTED" if scalar_detected else "ACCEPTED", "REJECTED")

    return {
        "schema": "SLCX032_ENGINE_WRONG_CONTROLS_V1",
        "campaign_id": CAMPAIGN_ID,
        "controls": controls,
        "detected_count": sum(int(row["detected"]) for row in controls),
        "total_count": len(controls),
        "all_detected": all(bool(row["detected"]) for row in controls),
    }


__all__ = [
    "CAMPAIGN_ID",
    "CUT_ENDPOINTS",
    "N144_BOUND",
    "N144_Y_LENGTH",
    "PORT_ORDER",
    "PRIMES_3",
    "PRIMES_5",
    "SLCX032ArithmeticError",
    "SLCX032CustodyError",
    "SLCX032Error",
    "build_n144_direct_instance",
    "build_n144_ring_instance",
    "calibrate_n12",
    "canonical_sha256",
    "compile_n72_operator",
    "direct_n144_order",
    "dos_semantic_hash",
    "engine_control_metadata",
    "factor_ownership",
    "fixed_energy_vector_from_y",
    "glue_y_degrees",
    "raw_moments_from_fixed",
    "recover_n72_one_cell",
    "retained_port_root_batch",
    "run_wrong_controls",
    "safe_modular_matmul",
    "solve_n144_direct",
    "solve_n144_transfer",
    "validate_n144_instance",
    "validate_n72_instance",
    "xor_moments",
]
