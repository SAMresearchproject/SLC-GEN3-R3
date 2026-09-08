#!/usr/bin/env python3
"""Exact singleton-root retained-port kernel with uint32 reduced storage."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

import numpy as np


def retained_port_root_p1_u32(
    engine: Any,
    local_instance: Mapping[str, Any],
    elimination_order: Sequence[int],
    points: np.ndarray,
    prime: int,
    port_order: Sequence[int],
    cache: Any,
    native_arithmetic: Any,
    chunk_cap: int,
) -> tuple[np.ndarray, dict[str, int]]:
    if len(points) != 1:
        raise RuntimeError("uint32 refinement admits one root per kernel call")
    if chunk_cap <= 0 or chunk_cap & (chunk_cap - 1):
        raise RuntimeError("uint32 chunk cap must be a positive power of two")
    if not 0 < prime <= np.iinfo(np.uint32).max:
        raise RuntimeError("prime does not fit uint32 reduced storage")
    descriptor = cache.descriptor
    if list(map(int, elimination_order)) != descriptor["elimination_order"]:
        raise RuntimeError("uint32 elimination order differs from cache")
    if list(map(int, port_order)) != descriptor["port_order"]:
        raise RuntimeError("uint32 port order differs from cache")
    _, exact, _ = engine._modules()
    parent_factors = exact._initial_factors(local_instance, points, prime)
    factors = []
    for factor in parent_factors:
        values = np.asarray(factor.values)
        if values.size and (
            int(values.min()) < 0 or int(values.max()) >= prime
        ):
            raise RuntimeError("initial modular factor escaped uint32 residue range")
        factors.append(
            engine.Factor(
                tuple(int(value) for value in factor.scope),
                np.ascontiguousarray(values, dtype=np.uint32),
            )
        )
    initial_scope_sha256 = hashlib.sha256(
        json.dumps(
            [list(factor.scope) for factor in factors],
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    if initial_scope_sha256 != descriptor["initial_factor_scope_sha256"]:
        raise RuntimeError("uint32 initial factor topology changed")

    product_zero_storage = np.empty(chunk_cap, dtype=np.uint32)
    product_one_storage = np.empty(chunk_cap, dtype=np.uint32)
    peak_union = 1
    peak_output = 1
    peak_chunk = 1
    peak_retained = sum(int(factor.values.shape[0]) for factor in factors)
    union_work = 0
    output_work = 0
    cache_entry_reads = 0
    selected_value_gathers = 0
    for step_index, raw_step in enumerate(descriptor["steps"]):
        vertex = int(raw_step["vertex"])
        selected = [factor for factor in factors if vertex in factor.scope]
        factors = [factor for factor in factors if vertex not in factor.scope]
        expected_scopes = [
            tuple(int(value) for value in row["factor_scope"])
            for row in raw_step["maps"]
        ]
        if [factor.scope for factor in selected] != expected_scopes:
            raise RuntimeError("uint32 selected-factor topology changed")
        union_scope = tuple(int(value) for value in raw_step["union_scope"])
        output_scope = tuple(int(value) for value in raw_step["output_scope"])
        if not selected:
            output = np.full((1, 1), 2, dtype=np.uint32)
            chunk_size = 1
        else:
            observed_union = tuple(
                sorted({site for factor in selected for site in factor.scope})
            )
            if observed_union != union_scope:
                raise RuntimeError("uint32 union topology changed")
            output_count = int(raw_step["output_count"])
            if output_count != 1 << len(output_scope):
                raise RuntimeError("uint32 output extent changed")
            chunk_size = min(chunk_cap, output_count)
            output = np.empty((output_count, 1), dtype=np.uint32)
            for start in range(0, output_count, chunk_size):
                stop = min(output_count, start + chunk_size)
                count = stop - start
                product_zero = product_zero_storage[:count].reshape(count, 1)
                product_one = product_one_storage[:count].reshape(count, 1)
                product_zero.fill(1)
                product_one.fill(1)
                for factor, row, projection in zip(
                    selected,
                    raw_step["maps"],
                    cache.maps[step_index],
                ):
                    zero_index = projection[start:stop]
                    native_arithmetic.update(
                        product_zero,
                        product_one,
                        factor.values,
                        zero_index,
                        int(row["eliminated_factor_bit"]),
                        prime,
                    )
                    cache_entry_reads += count
                    selected_value_gathers += 2 * count
                target = output[start:stop, :]
                native_arithmetic.finish(
                    target,
                    product_zero,
                    product_one,
                    prime,
                )
        factors.append(engine.Factor(output_scope, output))
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
    terminal = np.ones((int(engine.STATE_COUNT), 1), dtype=np.uint64)
    for factor in factors:
        if not set(factor.scope).issubset(ports):
            raise RuntimeError("uint32 kernel left a non-port variable")
        index = engine._project_indices(assignments, ports, factor.scope)
        gathered = factor.values[index, :].astype(np.uint64, copy=False)
        terminal = terminal * gathered % prime
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
        "selected_value_gather_count": selected_value_gathers,
        "policy_chunk_cap": chunk_cap,
        "policy_native_fused": 1,
        "policy_reduced_storage_bits": 32,
        "policy_multiplication_bits": 64,
    }


__all__ = ["retained_port_root_p1_u32"]
