#!/usr/bin/env python3
"""Exact policy-driven retained-port kernel for the N72 final refinement."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence

import numpy as np


@dataclass(frozen=True)
class KernelPolicy:
    policy_id: str
    chunk_cap: int
    inplace_products: bool
    reusable_product_buffers: bool
    reusable_one_index: bool
    reusable_take_buffer: bool
    take_mode: str = "raise"
    native_fused: bool = False

    def validate(self) -> None:
        if self.chunk_cap <= 0 or self.chunk_cap & (self.chunk_cap - 1):
            raise RuntimeError("refined chunk cap must be a positive power of two")
        if self.reusable_take_buffer and not self.inplace_products:
            raise RuntimeError("reusable take buffer requires in-place products")
        if self.take_mode not in ("raise", "clip"):
            raise RuntimeError("refined take mode is not admitted")
        if self.take_mode != "raise" and not self.reusable_take_buffer:
            raise RuntimeError("non-default take mode requires the sealed take lane")
        if self.native_fused and self.reusable_take_buffer:
            raise RuntimeError("native fused and NumPy take lanes are exclusive")


def retained_port_root_batch_refined(
    engine: Any,
    local_instance: Mapping[str, Any],
    elimination_order: Sequence[int],
    points: np.ndarray,
    prime: int,
    port_order: Sequence[int],
    cache: Any,
    policy: KernelPolicy,
    native_arithmetic: Any | None = None,
) -> tuple[np.ndarray, dict[str, int]]:
    """Run the exact cached kernel under one explicit allocation/chunk policy."""

    policy.validate()
    if policy.native_fused != (native_arithmetic is not None):
        raise RuntimeError("native arithmetic presence differs from policy")
    descriptor = cache.descriptor
    if list(map(int, elimination_order)) != descriptor["elimination_order"]:
        raise RuntimeError("refined kernel elimination order differs from cache")
    if list(map(int, port_order)) != descriptor["port_order"]:
        raise RuntimeError("refined kernel port order differs from cache")
    _, exact, _ = engine._modules()
    parent_factors = exact._initial_factors(local_instance, points, prime)
    factors = [
        engine.Factor(
            tuple(int(value) for value in factor.scope),
            np.ascontiguousarray(factor.values, dtype=np.int64),
        )
        for factor in parent_factors
    ]
    initial_scope_sha256 = hashlib.sha256(
        json.dumps(
            [list(factor.scope) for factor in factors],
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    if initial_scope_sha256 != descriptor["initial_factor_scope_sha256"]:
        raise RuntimeError("refined kernel initial factor topology changed")

    point_count = len(points)
    product_zero_storage = (
        np.empty((policy.chunk_cap, point_count), dtype=np.int64)
        if policy.reusable_product_buffers
        else None
    )
    product_one_storage = (
        np.empty((policy.chunk_cap, point_count), dtype=np.int64)
        if policy.reusable_product_buffers
        else None
    )
    one_index_storage = (
        np.empty(policy.chunk_cap, dtype=np.uint32)
        if policy.reusable_one_index
        else None
    )
    take_storage = (
        np.empty((policy.chunk_cap, point_count), dtype=np.int64)
        if policy.reusable_take_buffer
        else None
    )

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
            raise RuntimeError("refined selected-factor topology changed")
        union_scope = tuple(int(value) for value in raw_step["union_scope"])
        output_scope = tuple(int(value) for value in raw_step["output_scope"])
        if not selected:
            output = np.full((1, point_count), 2, dtype=np.int64)
            chunk_size = 1
        else:
            observed_union = tuple(
                sorted({site for factor in selected for site in factor.scope})
            )
            if observed_union != union_scope:
                raise RuntimeError("refined union topology changed")
            output_count = int(raw_step["output_count"])
            if output_count != 1 << len(output_scope):
                raise RuntimeError("refined output extent changed")
            chunk_size = min(policy.chunk_cap, output_count)
            output = np.empty((output_count, point_count), dtype=np.int64)
            for start in range(0, output_count, chunk_size):
                stop = min(output_count, start + chunk_size)
                count = stop - start
                if policy.reusable_product_buffers:
                    product_zero = product_zero_storage[:count]
                    product_one = product_one_storage[:count]
                    product_zero.fill(1)
                    product_one.fill(1)
                else:
                    product_zero = np.ones(
                        (count, point_count), dtype=np.int64
                    )
                    product_one = np.ones(
                        (count, point_count), dtype=np.int64
                    )
                for factor, row, projection in zip(
                    selected,
                    raw_step["maps"],
                    cache.maps[step_index],
                ):
                    zero_index = projection[start:stop]
                    if policy.native_fused:
                        native_arithmetic.update(
                            product_zero,
                            product_one,
                            factor.values,
                            zero_index,
                            int(row["eliminated_factor_bit"]),
                            prime,
                        )
                        cache_entry_reads += count
                        selected_value_gathers += 2 * count * point_count
                        continue
                    if policy.reusable_one_index:
                        one_index = one_index_storage[:count]
                        np.bitwise_or(
                            zero_index,
                            int(row["eliminated_factor_bit"]),
                            out=one_index,
                            casting="unsafe",
                        )
                    else:
                        one_index = np.bitwise_or(
                            zero_index,
                            int(row["eliminated_factor_bit"]),
                        )
                    if policy.reusable_take_buffer:
                        gathered = take_storage[:count]
                        np.take(
                            factor.values,
                            zero_index,
                            axis=0,
                            out=gathered,
                            mode=policy.take_mode,
                        )
                        np.multiply(product_zero, gathered, out=product_zero)
                        np.remainder(product_zero, prime, out=product_zero)
                        np.take(
                            factor.values,
                            one_index,
                            axis=0,
                            out=gathered,
                            mode=policy.take_mode,
                        )
                        np.multiply(product_one, gathered, out=product_one)
                        np.remainder(product_one, prime, out=product_one)
                    elif policy.inplace_products:
                        np.multiply(
                            product_zero,
                            factor.values[zero_index, :],
                            out=product_zero,
                        )
                        np.remainder(product_zero, prime, out=product_zero)
                        np.multiply(
                            product_one,
                            factor.values[one_index, :],
                            out=product_one,
                        )
                        np.remainder(product_one, prime, out=product_one)
                    else:
                        product_zero = (
                            product_zero * factor.values[zero_index, :]
                        ) % prime
                        product_one = (
                            product_one * factor.values[one_index, :]
                        ) % prime
                    cache_entry_reads += count
                    selected_value_gathers += 2 * count * point_count
                target = output[start:stop, :]
                if policy.native_fused:
                    native_arithmetic.finish(
                        target,
                        product_zero,
                        product_one,
                        prime,
                    )
                elif policy.inplace_products:
                    np.add(product_zero, product_one, out=target)
                    np.remainder(target, prime, out=target)
                else:
                    target[:] = (product_zero + product_one) % prime
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
        (int(engine.STATE_COUNT), point_count), dtype=np.int64
    )
    for factor in factors:
        if not set(factor.scope).issubset(ports):
            raise RuntimeError("refined kernel left a non-port variable")
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
        "selected_value_gather_count": selected_value_gathers,
        "policy_chunk_cap": policy.chunk_cap,
        "policy_inplace_products": int(policy.inplace_products),
        "policy_reusable_product_buffers": int(
            policy.reusable_product_buffers
        ),
        "policy_reusable_one_index": int(policy.reusable_one_index),
        "policy_reusable_take_buffer": int(policy.reusable_take_buffer),
        "policy_take_mode_clip": int(policy.take_mode == "clip"),
        "policy_native_fused": int(policy.native_fused),
    }


__all__ = ["KernelPolicy", "retained_port_root_batch_refined"]
