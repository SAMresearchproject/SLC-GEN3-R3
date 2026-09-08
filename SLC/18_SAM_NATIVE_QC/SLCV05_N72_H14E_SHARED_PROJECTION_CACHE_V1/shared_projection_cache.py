#!/usr/bin/env python3
"""Deterministic shared projection cache for the exact N72 retained-port kernel."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import mmap
from pathlib import Path
import time
from typing import Any, Mapping, Sequence

import numpy as np


DESCRIPTOR_SCHEMA = "SLCV05_N72_H14E_PROJECTION_CACHE_DESCRIPTOR_V1"
CACHE_LAYOUT = "ALIGNED_MIXED_UINT_READ_ONLY_FILE_MMAP"
ALIGNMENT_BYTES = 64


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


def _align(value: int) -> int:
    return (value + ALIGNMENT_BYTES - 1) // ALIGNMENT_BYTES * ALIGNMENT_BYTES


def _dtype_name(scope_width: int) -> str:
    if scope_width <= 8:
        return "uint8"
    if scope_width <= 16:
        return "uint16"
    if scope_width <= 32:
        return "uint32"
    raise RuntimeError("projection factor scope exceeds the uint32 cache contract")


def _unsigned_descriptor(value: Mapping[str, Any]) -> dict[str, Any]:
    unsigned = dict(value)
    unsigned.pop("descriptor_sha256", None)
    return unsigned


def validate_descriptor(descriptor: Mapping[str, Any]) -> None:
    if descriptor.get("schema") != DESCRIPTOR_SCHEMA:
        raise RuntimeError("projection-cache descriptor schema changed")
    if descriptor.get("layout") != CACHE_LAYOUT:
        raise RuntimeError("projection-cache layout changed")
    if descriptor.get("descriptor_sha256") != canonical_sha256(
        _unsigned_descriptor(descriptor)
    ):
        raise RuntimeError("projection-cache descriptor self-seal mismatch")
    if int(descriptor.get("alignment_bytes", -1)) != ALIGNMENT_BYTES:
        raise RuntimeError("projection-cache alignment changed")
    total_bytes = int(descriptor.get("total_bytes", -1))
    steps = descriptor.get("steps")
    if total_bytes <= 0 or not isinstance(steps, list) or len(steps) != 68:
        raise RuntimeError("projection-cache descriptor dimensions changed")
    previous_stop = 0
    entry_count = 0
    for step_index, step in enumerate(steps):
        if int(step.get("step_index", -1)) != step_index:
            raise RuntimeError("projection-cache step roster changed")
        maps = step.get("maps")
        if not isinstance(maps, list):
            raise RuntimeError("projection-cache map roster is malformed")
        for map_index, row in enumerate(maps):
            if int(row.get("map_index", -1)) != map_index:
                raise RuntimeError("projection-cache map order changed")
            dtype = np.dtype(str(row.get("dtype")))
            if dtype.name not in ("uint8", "uint16", "uint32"):
                raise RuntimeError("projection-cache dtype escaped the contract")
            offset = int(row.get("offset_bytes", -1))
            count = int(row.get("entry_count", -1))
            if offset < previous_stop or offset % ALIGNMENT_BYTES or count <= 0:
                raise RuntimeError("projection-cache extent is malformed")
            previous_stop = offset + count * dtype.itemsize
            if previous_stop > total_bytes:
                raise RuntimeError("projection-cache extent exceeds its file")
            entry_count += count
    if previous_stop > total_bytes or entry_count != int(
        descriptor.get("entry_count", -1)
    ):
        raise RuntimeError("projection-cache aggregate extent changed")


def compile_descriptor(
    engine: Any,
    local_instance: Mapping[str, Any],
    elimination_order: Sequence[int],
    port_order: Sequence[int],
) -> dict[str, Any]:
    """Compile the topology-only schedule without constructing any cache values."""

    _, exact, _ = engine._modules()
    n = int(local_instance["N"])
    ports = tuple(int(value) for value in port_order)
    order = tuple(int(value) for value in elimination_order)
    if len(ports) != 4 or len(set(ports)) != 4:
        raise RuntimeError("shared-cache retained port is malformed")
    if len(order) != n - 4 or set(order) != set(range(n)) - set(ports):
        raise RuntimeError("shared-cache elimination order changed")
    seed_points = np.asarray([1], dtype=np.int64)
    parent_factors = exact._initial_factors(
        local_instance,
        seed_points,
        int(engine.PRIMES_3[0]),
    )
    factor_scopes = [
        tuple(int(vertex) for vertex in factor.scope) for factor in parent_factors
    ]
    initial_scope_sha256 = canonical_sha256([list(scope) for scope in factor_scopes])
    offset = 0
    entry_count = 0
    dtype_entry_counts = {"uint8": 0, "uint16": 0, "uint32": 0}
    steps: list[dict[str, Any]] = []
    for step_index, vertex in enumerate(order):
        selected = [scope for scope in factor_scopes if vertex in scope]
        factor_scopes = [scope for scope in factor_scopes if vertex not in scope]
        if selected:
            union_scope = tuple(
                sorted({site for scope in selected for site in scope})
            )
            output_scope = tuple(site for site in union_scope if site != vertex)
            output_count = 1 << len(output_scope)
            maps = []
            for map_index, factor_scope in enumerate(selected):
                dtype_name = _dtype_name(len(factor_scope))
                dtype = np.dtype(dtype_name)
                offset = _align(offset)
                eliminated_position = factor_scope.index(vertex)
                maps.append(
                    {
                        "map_index": map_index,
                        "factor_scope": list(factor_scope),
                        "factor_scope_width": len(factor_scope),
                        "dtype": dtype_name,
                        "offset_bytes": offset,
                        "entry_count": output_count,
                        "eliminated_factor_position": eliminated_position,
                        "eliminated_factor_bit": 1 << eliminated_position,
                    }
                )
                offset += output_count * dtype.itemsize
                entry_count += output_count
                dtype_entry_counts[dtype_name] += output_count
        else:
            union_scope = (vertex,)
            output_scope = ()
            output_count = 1
            maps = []
        factor_scopes.append(output_scope)
        steps.append(
            {
                "step_index": step_index,
                "vertex": vertex,
                "union_scope": list(union_scope),
                "output_scope": list(output_scope),
                "output_count": output_count,
                "maps": maps,
            }
        )
    if any(not set(scope).issubset(ports) for scope in factor_scopes):
        raise RuntimeError("compiled shared-cache schedule left a non-port scope")
    total_bytes = _align(offset)
    unsigned = {
        "schema": DESCRIPTOR_SCHEMA,
        "layout": CACHE_LAYOUT,
        "alignment_bytes": ALIGNMENT_BYTES,
        "source_instance_n": n,
        "port_order": list(ports),
        "elimination_order": list(order),
        "elimination_order_sha256": canonical_sha256(list(order)),
        "initial_factor_scope_sha256": initial_scope_sha256,
        "entry_count": entry_count,
        "dtype_entry_counts": dtype_entry_counts,
        "total_bytes": total_bytes,
        "steps": steps,
    }
    descriptor = {
        **unsigned,
        "descriptor_sha256": canonical_sha256(unsigned),
    }
    validate_descriptor(descriptor)
    return descriptor


def build_cache_file(
    path: Path,
    descriptor: Mapping[str, Any],
) -> dict[str, Any]:
    """Materialize every deterministic projection map into one aligned byte file."""

    validate_descriptor(descriptor)
    if path.exists():
        raise RuntimeError("projection-cache target already exists")
    started = time.perf_counter()
    raw = np.memmap(
        path,
        mode="w+",
        dtype=np.uint8,
        shape=(int(descriptor["total_bytes"]),),
    )
    raw[:] = 0
    for step in descriptor["steps"]:
        output_scope = tuple(int(value) for value in step["output_scope"])
        output_count = int(step["output_count"])
        if not step["maps"]:
            continue
        positions = {vertex: index for index, vertex in enumerate(output_scope)}
        assignments = np.arange(output_count, dtype=np.uint32)
        vertex = int(step["vertex"])
        for row in step["maps"]:
            dtype = np.dtype(str(row["dtype"]))
            projection = np.ndarray(
                shape=(output_count,),
                dtype=dtype,
                buffer=raw,
                offset=int(row["offset_bytes"]),
            )
            projection[:] = 0
            factor_scope = tuple(int(value) for value in row["factor_scope"])
            for factor_position, factor_vertex in enumerate(factor_scope):
                if factor_vertex == vertex:
                    continue
                contribution = (
                    ((assignments >> positions[factor_vertex]) & 1)
                    << factor_position
                ).astype(dtype, copy=False)
                projection |= contribution
            maximum = int(projection.max(initial=0))
            if maximum | int(row["eliminated_factor_bit"]) >= 1 << len(
                factor_scope
            ):
                raise RuntimeError("projection-cache index escaped its factor")
    raw.flush()
    del raw
    cache_sha256 = sha256_file(path)
    build_seconds = time.perf_counter() - started
    return {
        "cache_sha256": cache_sha256,
        "cache_bytes": path.stat().st_size,
        "build_seconds": build_seconds,
        "descriptor_sha256": descriptor["descriptor_sha256"],
    }


@dataclass
class ProjectionCache:
    path: Path
    descriptor: Mapping[str, Any]
    raw: np.memmap
    maps: list[list[np.ndarray]]

    def close(self) -> None:
        mapping = getattr(self.raw, "_mmap", None)
        if mapping is not None:
            mapping.close()


def open_cache_file(
    path: Path,
    descriptor: Mapping[str, Any],
) -> ProjectionCache:
    validate_descriptor(descriptor)
    if path.stat().st_size != int(descriptor["total_bytes"]):
        raise RuntimeError("projection-cache file size changed")
    raw = np.memmap(path, mode="r", dtype=np.uint8)
    mapping = getattr(raw, "_mmap", None)
    if mapping is not None and hasattr(mapping, "madvise"):
        mapping.madvise(mmap.MADV_WILLNEED)
    maps: list[list[np.ndarray]] = []
    for step in descriptor["steps"]:
        step_maps = []
        for row in step["maps"]:
            step_maps.append(
                np.ndarray(
                    shape=(int(row["entry_count"]),),
                    dtype=np.dtype(str(row["dtype"])),
                    buffer=raw,
                    offset=int(row["offset_bytes"]),
                )
            )
        maps.append(step_maps)
    return ProjectionCache(path=path, descriptor=descriptor, raw=raw, maps=maps)


def retained_port_root_batch_cached(
    engine: Any,
    local_instance: Mapping[str, Any],
    elimination_order: Sequence[int],
    points: np.ndarray,
    prime: int,
    port_order: Sequence[int],
    cache: ProjectionCache,
) -> tuple[np.ndarray, dict[str, int]]:
    """Run the exact retained-port kernel with topology projections read from cache."""

    descriptor = cache.descriptor
    if list(map(int, elimination_order)) != descriptor["elimination_order"]:
        raise RuntimeError("cached kernel elimination order differs from cache")
    if list(map(int, port_order)) != descriptor["port_order"]:
        raise RuntimeError("cached kernel port order differs from cache")
    _, exact, _ = engine._modules()
    parent_factors = exact._initial_factors(local_instance, points, prime)
    factors = [
        engine.Factor(
            tuple(int(value) for value in factor.scope),
            np.ascontiguousarray(factor.values, dtype=np.int64),
        )
        for factor in parent_factors
    ]
    observed_initial_sha256 = canonical_sha256(
        [list(factor.scope) for factor in factors]
    )
    if observed_initial_sha256 != descriptor["initial_factor_scope_sha256"]:
        raise RuntimeError("cached kernel initial factor topology changed")
    peak_union = 1
    peak_output = 1
    peak_chunk = 1
    peak_retained = sum(int(factor.values.shape[0]) for factor in factors)
    union_work = 0
    output_work = 0
    cache_entry_reads = 0
    for step_index, raw_step in enumerate(descriptor["steps"]):
        vertex = int(raw_step["vertex"])
        selected = [factor for factor in factors if vertex in factor.scope]
        factors = [factor for factor in factors if vertex not in factor.scope]
        expected_scopes = [
            tuple(int(value) for value in row["factor_scope"])
            for row in raw_step["maps"]
        ]
        if [factor.scope for factor in selected] != expected_scopes:
            raise RuntimeError("cached kernel selected-factor topology changed")
        union_scope = tuple(int(value) for value in raw_step["union_scope"])
        output_scope = tuple(int(value) for value in raw_step["output_scope"])
        if not selected:
            output = np.full((1, len(points)), 2, dtype=np.int64)
            chunk_size = 1
        else:
            observed_union = tuple(
                sorted({site for factor in selected for site in factor.scope})
            )
            if observed_union != union_scope:
                raise RuntimeError("cached kernel union topology changed")
            output_count = int(raw_step["output_count"])
            if output_count != 1 << len(output_scope):
                raise RuntimeError("cached kernel output extent changed")
            chunk_size = min(int(engine.FUSED_CHUNK_CAP), output_count)
            output = np.empty((output_count, len(points)), dtype=np.int64)
            for start in range(0, output_count, chunk_size):
                stop = min(output_count, start + chunk_size)
                product_zero = np.ones(
                    (stop - start, len(points)), dtype=np.int64
                )
                product_one = np.ones(
                    (stop - start, len(points)), dtype=np.int64
                )
                for factor, row, projection in zip(
                    selected,
                    raw_step["maps"],
                    cache.maps[step_index],
                ):
                    zero_index = projection[start:stop]
                    one_index = np.bitwise_or(
                        zero_index,
                        int(row["eliminated_factor_bit"]),
                    )
                    product_zero = (
                        product_zero * factor.values[zero_index, :]
                    ) % prime
                    product_one = (
                        product_one * factor.values[one_index, :]
                    ) % prime
                    cache_entry_reads += stop - start
                output[start:stop, :] = (product_zero + product_one) % prime
        factors.append(
            engine.Factor(
                output_scope,
                np.ascontiguousarray(output, dtype=np.int64),
            )
        )
        union_entries = 1 << len(union_scope)
        output_entries = int(output.shape[0])
        union_work += union_entries
        output_work += output_entries
        peak_union = max(peak_union, union_entries)
        peak_output = max(peak_output, output_entries)
        peak_chunk = max(peak_chunk, chunk_size)
        peak_retained = max(
            peak_retained,
            sum(int(factor.values.shape[0]) for factor in factors),
        )
    ports = tuple(int(value) for value in port_order)
    assignments = np.arange(int(engine.STATE_COUNT), dtype=np.uint64)
    terminal = np.ones(
        (int(engine.STATE_COUNT), len(points)), dtype=np.int64
    )
    for factor in factors:
        if not set(factor.scope).issubset(ports):
            raise RuntimeError("cached kernel left a non-port variable")
        index = engine._project_indices(assignments, ports, factor.scope)
        terminal = terminal * factor.values[index, :] % prime
    return np.ascontiguousarray(terminal, dtype=np.int64), {
        "peak_union_assignments_per_root_logical": peak_union,
        "peak_output_assignments_per_root": peak_output,
        "peak_fused_chunk_assignments_per_root": peak_chunk,
        "peak_retained_factor_assignments_per_root": peak_retained,
        "sum_2_pow_union_scope": union_work,
        "sum_2_pow_output_scope": output_work,
        "full_union_materialization_count": 0,
        "topology_projection_cache_entry_reads": cache_entry_reads,
        "topology_projection_rebuild_count": 0,
        "one_branch_index_rule_count": cache_entry_reads,
    }


__all__ = [
    "CACHE_LAYOUT",
    "DESCRIPTOR_SCHEMA",
    "ProjectionCache",
    "build_cache_file",
    "canonical_bytes",
    "canonical_sha256",
    "compile_descriptor",
    "open_cache_file",
    "retained_port_root_batch_cached",
    "sha256_file",
    "validate_descriptor",
]

