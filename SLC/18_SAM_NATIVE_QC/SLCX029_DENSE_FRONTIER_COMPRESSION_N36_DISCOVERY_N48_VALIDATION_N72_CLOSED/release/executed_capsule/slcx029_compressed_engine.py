"""Exact dense-frontier compression engine for SLCX029.

The numerical authority remains the hash-locked SLCX023A exact NTT/VE engine.
This sidecar changes two things only:

* a finite graph-only order portfolio is scored without couplings, fields,
  spectra, timing, or target access; and
* elimination is evaluated as two fused products over the output boundary,
  in frozen chunks, so the full union-assignment product is never allocated.

The materialized parent kernel remains callable as an independent N36
step-table oracle.  Both kernels are wrapped by the same NTT, CRT, hashing and
DOS-verification path below.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
from types import ModuleType
from typing import Any, Callable, Mapping, Sequence

import numpy as np


CAMPAIGN_ID = "SLCX029_DENSE_FRONTIER_COMPRESSION_N36_DISCOVERY_N48_VALIDATION_N72_CLOSED"
SEALED_PARENT_ENGINE_SHA256 = "fb8bff08ae0836a628a90edb141f8e3d96ae13d96075eb2e2031d12737f77c5a"
PARENT_PRIMES = (998244353, 1004535809, 469762049)
PRIMITIVE_ROOT = 3
ALLOWED_SIZES = frozenset({36, 48})
FROZEN_CHUNK_CAP = 32768
ROOT_BATCH_ENTRY_CAP = 1 << 24
TABLE_DOMAIN = "SLCX029-EXACT-STEP-TABLE-V1"
DOS_DOMAIN = "SLCX029-EXACT-DOS-V1"

BASE = Path(__file__).resolve().parent
DEFAULT_PARENT_ENGINE = (
    BASE.parent
    / "SLCX023A_EXECUTABLE_CUSTODY_AND_RECEIPT_DOMAIN_APPEAL_RETEST"
    / "release"
    / "executed_capsule"
    / "slcx023_exact_engine.py"
)


class SLCX029Error(RuntimeError):
    """Raised for custody, policy, or exact-arithmetic failure."""


class PortfolioValidationError(SLCX029Error):
    """Raised when the frozen portfolio roster or order changes."""


class ExactComparisonError(SLCX029Error):
    """Raised when a step table or DOS differs from its exact authority."""


class RosterValidationError(SLCX029Error):
    """Raised when staged instances are missing, duplicated, or reused."""


class FrozenPolicyError(SLCX029Error):
    """Raised when validation attempts to refit the discovery policy."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@lru_cache(maxsize=None)
def _load_parent(resolved: str) -> ModuleType:
    path = Path(resolved)
    if path.is_symlink() or not path.is_file():
        raise SLCX029Error("parent engine must be a regular retained source file")
    observed = sha256_file(path)
    if observed != SEALED_PARENT_ENGINE_SHA256:
        raise SLCX029Error(f"parent engine hash mismatch: {observed}")
    name = f"_slcx029_parent_{observed[:16]}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SLCX029Error("could not construct parent engine import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    if tuple(module.NTT_PRIMES) != PARENT_PRIMES:
        raise SLCX029Error("parent prime roster changed")
    if int(module.MAX_NTT_LENGTH) != 2048:
        raise SLCX029Error("parent NTT cap changed")
    module.ALLOWED_SIZES = ALLOWED_SIZES
    return module


def load_parent(path: Path | None = None) -> ModuleType:
    return _load_parent(str((path or DEFAULT_PARENT_ENGINE).resolve()))


def validate_instance(instance: Mapping[str, Any], parent_path: Path | None = None) -> dict[str, Any]:
    parent = load_parent(parent_path)
    report = dict(parent.validate_instance(instance))
    if int(report["N"]) not in ALLOWED_SIZES:
        raise SLCX029Error("SLCX029 admits only frozen N36 and N48 instances")
    return report


def _base_adjacency(instance: Mapping[str, Any]) -> dict[int, set[int]]:
    n = int(instance["N"])
    adjacency = {vertex: set() for vertex in range(n)}
    for raw_u, raw_v, _ in instance["edges"]:
        u, v = int(raw_u), int(raw_v)
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def _fill_count(vertex: int, adjacency: Mapping[int, set[int]], remaining: set[int]) -> int:
    neighbors = sorted(adjacency[vertex] & remaining)
    return sum(
        right not in adjacency[left]
        for index, left in enumerate(neighbors)
        for right in neighbors[index + 1 :]
    )


def _eliminate_graph_vertex(
    vertex: int,
    adjacency: dict[int, set[int]],
    remaining: set[int],
) -> tuple[int, tuple[int, ...]]:
    if vertex not in remaining:
        raise SLCX029Error("order repeats an eliminated vertex")
    neighbors = tuple(sorted(adjacency[vertex] & remaining))
    for index, left in enumerate(neighbors):
        for right in neighbors[index + 1 :]:
            adjacency[left].add(right)
            adjacency[right].add(left)
    for neighbor in neighbors:
        adjacency[neighbor].discard(vertex)
    remaining.remove(vertex)
    return len(neighbors), neighbors


def order_structure(instance: Mapping[str, Any], order: Sequence[int]) -> dict[str, Any]:
    """Return the frozen graph-only score and per-step logical sizes."""

    n = int(instance["N"])
    canonical_order = tuple(int(vertex) for vertex in order)
    if len(canonical_order) != n or sorted(canonical_order) != list(range(n)):
        raise SLCX029Error("candidate order is not a vertex permutation")
    adjacency = _base_adjacency(instance)
    remaining = set(range(n))
    steps: list[dict[str, Any]] = []
    width = 0
    union_sum = 0
    output_sum = 0
    for step, vertex in enumerate(canonical_order, 1):
        degree, neighbors = _eliminate_graph_vertex(vertex, adjacency, remaining)
        union_entries = 1 << (degree + 1)
        output_entries = 1 << degree
        width = max(width, degree)
        union_sum += union_entries
        output_sum += output_entries
        steps.append(
            {
                "step": step,
                "vertex": vertex,
                "output_neighbors": list(neighbors),
                "induced_width": degree,
                "union_assignment_entries": union_entries,
                "output_assignment_entries": output_entries,
            }
        )
    return {
        "induced_width": width,
        "sum_2_pow_union_scope": union_sum,
        "sum_2_pow_output_scope": output_sum,
        "peak_union_assignment_entries": max(row["union_assignment_entries"] for row in steps),
        "peak_output_assignment_entries": max(row["output_assignment_entries"] for row in steps),
        "canonical_order": list(canonical_order),
        "score": [width, union_sum, list(canonical_order)],
        "steps": steps,
    }


def _greedy_order(instance: Mapping[str, Any], policy: str) -> list[int]:
    n = int(instance["N"])
    cell_size = int(instance.get("cell_size", 12))
    adjacency = _base_adjacency(instance)
    remaining = set(range(n))
    order: list[int] = []

    def simulate_next_min_fill(candidate: int) -> int:
        if len(remaining) <= 1:
            return 0
        trial_adj = {vertex: set(neighbors) for vertex, neighbors in adjacency.items()}
        trial_remaining = set(remaining)
        _eliminate_graph_vertex(candidate, trial_adj, trial_remaining)
        return min(_fill_count(v, trial_adj, trial_remaining) for v in trial_remaining)

    while remaining:
        rows: list[tuple[tuple[int, ...], int]] = []
        for vertex in sorted(remaining):
            degree = len(adjacency[vertex] & remaining)
            fill = _fill_count(vertex, adjacency, remaining)
            cross = sum(
                neighbor // cell_size != vertex // cell_size
                for neighbor in adjacency[vertex] & remaining
            )
            if policy == "deterministic_min_fill_degree_vertex":
                key = (fill, degree, vertex)
            elif policy == "deterministic_min_fill_cross_degree_vertex":
                key = (fill, cross, degree, vertex)
            elif policy == "deterministic_min_fill_degree_cross_vertex":
                key = (fill, degree, cross, vertex)
            elif policy == "one_step_lookahead_min_fill":
                key = (fill, simulate_next_min_fill(vertex), degree, cross, vertex)
            else:
                raise SLCX029Error(f"unknown greedy order policy: {policy}")
            rows.append((key, vertex))
        chosen = min(rows)[1]
        order.append(chosen)
        _eliminate_graph_vertex(chosen, adjacency, remaining)
    return order


def _adjacent_swap_refinement(instance: Mapping[str, Any], seed: Sequence[int]) -> list[int]:
    """One frozen left-to-right adjacent-swap refinement sweep."""

    current = list(int(value) for value in seed)
    current_score = tuple(order_structure(instance, current)["score"][:2]) + (tuple(current),)
    # Exactly one canonical sweep keeps the portfolio finite and cheap.  An
    # accepted swap must strictly improve the same graph-only objective used
    # to choose the portfolio winner.
    for index in range(len(current) - 1):
        trial = list(current)
        trial[index], trial[index + 1] = trial[index + 1], trial[index]
        structure = order_structure(instance, trial)
        trial_score = (
            int(structure["induced_width"]),
            int(structure["sum_2_pow_union_scope"]),
            tuple(trial),
        )
        if trial_score < current_score:
            current = trial
            current_score = trial_score
    return current


PORTFOLIO_IDS = (
    "historical_cell_min_fill",
    "historical_min_fill",
    "historical_min_degree",
    "deterministic_min_fill_degree_vertex",
    "deterministic_min_fill_cross_degree_vertex",
    "deterministic_min_fill_degree_cross_vertex",
    "one_step_lookahead_min_fill",
    "deterministic_adjacent_swap_refinement",
)

FROZEN_SELECTION_RULE = (
    "LEXICOGRAPHIC_MIN_INDUCED_WIDTH_THEN_SUM_2_POW_UNION_THEN_CANONICAL_ORDER"
)


def validate_portfolio_roster(portfolio: Sequence[Any]) -> None:
    ids = tuple(
        str(row["policy_id"]) if isinstance(row, Mapping) else str(row)
        for row in portfolio
    )
    if ids != PORTFOLIO_IDS:
        raise PortfolioValidationError(
            f"portfolio roster/order mismatch: observed={ids}, expected={PORTFOLIO_IDS}"
        )


def validate_frozen_policy(policy: Mapping[str, Any]) -> None:
    validate_portfolio_roster(policy.get("portfolio_ids", ()))
    if policy.get("selection_rule") != FROZEN_SELECTION_RULE:
        raise FrozenPolicyError("selection rule changed after discovery")
    if policy.get("chunk_cap") != FROZEN_CHUNK_CAP:
        raise FrozenPolicyError("chunk cap changed after discovery")
    if policy.get("refit") is not False or policy.get("repair") is not False:
        raise FrozenPolicyError("validation refit/repair is forbidden")


def validate_unique_staged_roster(
    discovery_instances: Sequence[Mapping[str, Any]],
    validation_instances: Sequence[Mapping[str, Any]],
) -> None:
    discovery_ids = tuple(str(row.get("instance_id", "")) for row in discovery_instances)
    validation_ids = tuple(str(row.get("instance_id", "")) for row in validation_instances)
    expected_discovery = ("SLCX023_N36_I00", "SLCX023_N36_I01")
    expected_validation = ("SLCX024_N48_I00", "SLCX024_N48_I01")
    combined = discovery_ids + validation_ids
    if discovery_ids != expected_discovery or validation_ids != expected_validation:
        raise RosterValidationError("staged instance roster mismatch")
    if len(combined) != len(set(combined)):
        raise RosterValidationError("instance reuse detected across staged roster")


def order_portfolio(instance: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Generate the exact finite portfolio; weights and fields are untouched."""

    historical = instance.get("orders")
    if not isinstance(historical, Mapping):
        raise SLCX029Error("frozen instance lacks historical orders")
    generated: dict[str, list[int]] = {
        "historical_cell_min_fill": [int(v) for v in historical["cell_min_fill"]],
        "historical_min_fill": [int(v) for v in historical["min_fill"]],
        "historical_min_degree": [int(v) for v in historical["min_degree"]],
    }
    for policy in (
        "deterministic_min_fill_degree_vertex",
        "deterministic_min_fill_cross_degree_vertex",
        "deterministic_min_fill_degree_cross_vertex",
        "one_step_lookahead_min_fill",
    ):
        generated[policy] = _greedy_order(instance, policy)
    generated["deterministic_adjacent_swap_refinement"] = _adjacent_swap_refinement(
        instance,
        generated["deterministic_min_fill_degree_vertex"],
    )
    if tuple(generated) != PORTFOLIO_IDS:
        raise SLCX029Error("portfolio identity/order drift")
    rows: list[dict[str, Any]] = []
    for policy_id in PORTFOLIO_IDS:
        structure = order_structure(instance, generated[policy_id])
        rows.append({"policy_id": policy_id, **structure})
    validate_portfolio_roster(rows)
    return rows


def select_graph_only_order(instance: Mapping[str, Any]) -> dict[str, Any]:
    portfolio = order_portfolio(instance)
    selected = min(
        portfolio,
        key=lambda row: (
            int(row["induced_width"]),
            int(row["sum_2_pow_union_scope"]),
            tuple(int(value) for value in row["canonical_order"]),
        ),
    )
    baseline = next(row for row in portfolio if row["policy_id"] == "historical_cell_min_fill")
    return {
        "selection_rule": FROZEN_SELECTION_RULE,
        "portfolio_ids": list(PORTFOLIO_IDS),
        "portfolio": portfolio,
        "selected_policy_id": selected["policy_id"],
        "selected_order": list(selected["canonical_order"]),
        "selected_structure": selected,
        "baseline_structure": baseline,
        "portfolio_sha256": canonical_sha256(portfolio),
    }


@dataclass(frozen=True)
class Factor:
    scope: tuple[int, ...]
    values: np.ndarray


def _project_indices(
    union_assignments: np.ndarray,
    union_scope: tuple[int, ...],
    factor_scope: tuple[int, ...],
) -> np.ndarray:
    positions = {vertex: index for index, vertex in enumerate(union_scope)}
    result = np.zeros(len(union_assignments), dtype=np.uint64)
    for factor_position, vertex in enumerate(factor_scope):
        result |= ((union_assignments >> positions[vertex]) & 1) << factor_position
    return result.astype(np.intp, copy=False)


def _insert_bit(assignments: np.ndarray, position: int, value: int) -> np.ndarray:
    low_mask = (1 << position) - 1
    low = assignments & low_mask
    high = assignments >> position
    result = low | (high << (position + 1))
    if value:
        result |= np.uint64(1 << position)
    return result


def _initial_factors(parent: ModuleType, instance: Mapping[str, Any], points: np.ndarray, prime: int) -> list[Factor]:
    parent_factors = parent._initial_factors(instance, points, prime)
    return [Factor(tuple(f.scope), np.ascontiguousarray(f.values, dtype=np.int64)) for f in parent_factors]


def fused_root_batch(
    instance: Mapping[str, Any],
    order: Sequence[int],
    points: np.ndarray,
    prime: int,
    on_step: Callable[[dict[str, Any], np.ndarray], None],
    *,
    chunk_cap: int = FROZEN_CHUNK_CAP,
    parent_path: Path | None = None,
) -> tuple[np.ndarray, dict[str, int]]:
    """Run exact fused paired elimination without a full union product table."""

    if type(chunk_cap) is not int or chunk_cap != FROZEN_CHUNK_CAP:
        raise SLCX029Error("chunk policy drift")
    parent = load_parent(parent_path)
    factors = _initial_factors(parent, instance, points, prime)
    peak_union = 1
    peak_output = 1
    peak_chunk = 1
    peak_retained = sum(int(f.values.shape[0]) for f in factors)
    for step_index, raw_vertex in enumerate(order):
        vertex = int(raw_vertex)
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
            chunk_size = min(FROZEN_CHUNK_CAP, output_count)
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
                    product_zero = (product_zero * factor.values[zero_index, :]) % prime
                    product_one = (product_one * factor.values[one_index, :]) % prime
                output[start:stop, :] = (product_zero + product_one) % prime
        output = np.ascontiguousarray(output, dtype=np.int64)
        factors.append(Factor(output_scope, output))
        peak_union = max(peak_union, 1 << len(union_scope))
        peak_output = max(peak_output, int(output.shape[0]))
        peak_chunk = max(peak_chunk, chunk_size)
        peak_retained = max(peak_retained, sum(int(f.values.shape[0]) for f in factors))
        on_step(
            {
                "step": step_index + 1,
                "eliminated_vertex": vertex,
                "input_factor_count": len(selected),
                "union_scope": list(union_scope),
                "output_scope": list(output_scope),
                "output_assignment_count": int(output.shape[0]),
                "fused_chunk_size": int(chunk_size),
                "full_union_materialized": False,
            },
            output,
        )
    if any(factor.scope for factor in factors):
        raise SLCX029Error("fused elimination left an unresolved boundary")
    terminal = np.ones(len(points), dtype=np.int64)
    for factor in factors:
        terminal = (terminal * factor.values[0, :]) % prime
    return terminal, {
        "peak_union_assignments_per_root_logical": peak_union,
        "peak_output_assignments_per_root": peak_output,
        "peak_fused_chunk_assignments_per_root": peak_chunk,
        "peak_retained_factor_assignments_per_root": peak_retained,
        "full_union_materialization_count": 0,
    }


def materialized_root_batch(
    instance: Mapping[str, Any],
    order: Sequence[int],
    points: np.ndarray,
    prime: int,
    on_step: Callable[[dict[str, Any], np.ndarray], None],
    *,
    parent_path: Path | None = None,
) -> tuple[np.ndarray, dict[str, int]]:
    parent = load_parent(parent_path)

    def adapter(metadata: dict[str, Any], table: np.ndarray) -> None:
        on_step(
            {
                **metadata,
                "fused_chunk_size": None,
                "full_union_materialized": True,
            },
            table,
        )

    terminal, metrics = parent._ve_root_batch(instance, order, points, prime, adapter)
    return terminal, {
        "peak_union_assignments_per_root_logical": int(metrics["peak_union_assignments_per_root"]),
        "peak_output_assignments_per_root": max(1, int(metrics["peak_union_assignments_per_root"]) // 2),
        "peak_fused_chunk_assignments_per_root": 0,
        "peak_retained_factor_assignments_per_root": 0,
        "full_union_materialization_count": len(order),
    }


def _ntt_length(bound: int) -> int:
    length = 1
    while length <= 2 * bound:
        length <<= 1
    if length > 2048:
        raise SLCX029Error("NTT length exceeds frozen cap")
    return length


def _selected_primes(n: int) -> tuple[int, ...]:
    product = 1
    selected: list[int] = []
    for prime in PARENT_PRIMES:
        selected.append(prime)
        product *= prime
        if product > (1 << n):
            return tuple(selected)
    raise SLCX029Error("parent CRT roster is insufficient")


def solve_exact(
    instance: Mapping[str, Any],
    order: Sequence[int],
    *,
    order_id: str,
    kernel: str,
    parent_path: Path | None = None,
) -> dict[str, Any]:
    """Execute one exact materialized or fused NTT/VE solve."""

    validation = validate_instance(instance, parent_path)
    parent = load_parent(parent_path)
    n = int(instance["N"])
    bound = int(instance["energy_bound_B"])
    structure = order_structure(instance, order)
    ntt_length = _ntt_length(bound)
    primes = _selected_primes(n)
    maximum_union = int(structure["peak_union_assignment_entries"])
    root_batch = min(8, ntt_length, max(1, ROOT_BATCH_ENTRY_CAP // maximum_union))
    if kernel == "fused":
        root_kernel = fused_root_batch
    elif kernel == "materialized":
        root_kernel = materialized_root_batch
    else:
        raise SLCX029Error("kernel must be fused or materialized")

    modular_coefficients: list[list[int]] = []
    step_tables: list[dict[str, Any]] = []
    prime_metrics: list[dict[str, Any]] = []
    started = time.perf_counter()
    for prime_index, prime in enumerate(primes):
        omega = pow(PRIMITIVE_ROOT, (prime - 1) // ntt_length, prime)
        evaluations = [0] * ntt_length
        hashers: list[Any] = []
        headers: list[dict[str, Any]] = []
        aggregate_metrics: dict[str, int] = {
            "peak_union_assignments_per_root_logical": 0,
            "peak_output_assignments_per_root": 0,
            "peak_fused_chunk_assignments_per_root": 0,
            "peak_retained_factor_assignments_per_root": 0,
            "full_union_materialization_count": 0,
        }
        for batch_start in range(0, ntt_length, root_batch):
            batch_stop = min(ntt_length, batch_start + root_batch)
            points = np.asarray(
                [pow(omega, root_index, prime) for root_index in range(batch_start, batch_stop)],
                dtype=np.int64,
            )

            def on_step(metadata: dict[str, Any], table: np.ndarray) -> None:
                step_index = int(metadata["step"]) - 1
                stable = {
                    key: value
                    for key, value in metadata.items()
                    if key not in {"fused_chunk_size", "full_union_materialized"}
                }
                if batch_start == 0:
                    header = {
                        "schema": TABLE_DOMAIN,
                        "instance_sha256": instance["instance_sha256"],
                        "order_id": order_id,
                        "prime": prime,
                        "ntt_length": ntt_length,
                        **stable,
                        "root_major_assignment_order": True,
                    }
                    hasher = hashlib.sha256()
                    hasher.update(TABLE_DOMAIN.encode("ascii") + b"\x00")
                    hasher.update(canonical_bytes(header) + b"\x00")
                    headers.append(header)
                    hashers.append(hasher)
                else:
                    expected = headers[step_index]
                    for key, value in stable.items():
                        if expected.get(key) != value:
                            raise SLCX029Error("boundary structure changed across root batches")
                root_major = np.ascontiguousarray(table.T, dtype=">u8")
                hashers[step_index].update(root_major.tobytes(order="C"))

            terminal, batch_metrics = root_kernel(
                instance,
                order,
                points,
                prime,
                on_step,
                parent_path=parent_path,
            )
            evaluations[batch_start:batch_stop] = [int(value) for value in terminal]
            for key in aggregate_metrics:
                aggregate_metrics[key] = max(aggregate_metrics[key], int(batch_metrics[key]))
        coefficients = parent._inverse_ntt(evaluations, prime)
        modular_coefficients.append([int(value) for value in coefficients])
        for header, hasher in zip(headers, hashers):
            step_tables.append(
                {
                    "prime_index": prime_index,
                    "prime": prime,
                    "step": header["step"],
                    "eliminated_vertex": header["eliminated_vertex"],
                    "union_scope": header["union_scope"],
                    "output_scope": header["output_scope"],
                    "output_assignment_count": header["output_assignment_count"],
                    "table_sha256": hasher.hexdigest(),
                }
            )
        prime_metrics.append(
            {
                "prime": prime,
                "ntt_length": ntt_length,
                "root_batch_size": root_batch,
                "coefficient_residue_sha256": canonical_sha256(coefficients),
                **aggregate_metrics,
            }
        )

    coefficients = [
        int(parent._crt([modular_coefficients[p][index] for p in range(len(primes))], primes))
        for index in range(ntt_length)
    ]
    if any(coefficients[index] for index in range(2 * bound + 1, ntt_length)):
        raise SLCX029Error("inverse NTT produced coefficients beyond 2B")
    dos = {
        shifted - bound: count
        for shifted, count in enumerate(coefficients[: 2 * bound + 1])
        if count
    }
    verification = dict(parent.verify_dos(instance, dos))
    if verification.get("status") != "PASS":
        raise SLCX029Error("exact DOS invariant failure")
    dos_rows = [{"energy": energy, "count": str(count)} for energy, count in sorted(dos.items())]
    elapsed = time.perf_counter() - started
    return {
        "schema": "SLCX029_EXACT_SOLVE_V1",
        "kernel": kernel,
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "order_id": order_id,
        "order": [int(value) for value in order],
        "order_structure": structure,
        "dos": dos_rows,
        "dos_sha256": canonical_sha256({"domain": DOS_DOMAIN, "dos": dos_rows}),
        "step_tables": step_tables,
        "step_table_roster_sha256": canonical_sha256(step_tables),
        "verification": verification,
        "metrics": {
            "elapsed_seconds": elapsed,
            "N": n,
            "energy_bound_B": bound,
            "ntt_length": ntt_length,
            "selected_primes": list(primes),
            "root_batch_size": root_batch,
            "prime_metrics": prime_metrics,
            "monolithic_full_union_table_cardinality_per_root_peak": int(
                structure["peak_union_assignment_entries"]
            ),
            "retained_separator_cardinality_per_root_peak": int(
                structure["peak_output_assignment_entries"]
            ),
            "fused_transient_chunk_workspace_cardinality_per_root_peak": int(
                2 * min(FROZEN_CHUNK_CAP, int(structure["peak_output_assignment_entries"]))
            ),
            "fused_transient_metric_scope": (
                "two paired-product accumulator tensors only; excludes retained factors, "
                "retained output, interpreter overhead, and total process memory"
            ),
            "assignment_branches_evaluated_per_root_sum": int(
                structure["sum_2_pow_union_scope"]
            ),
            "retained_separator_unchanged_at_fixed_order": True,
            "full_union_materialization_count": 0 if kernel == "fused" else n * len(primes) * ntt_length,
        },
    }


def dos_mapping(result: Mapping[str, Any]) -> dict[int, int]:
    rows = result.get("dos")
    if not isinstance(rows, list):
        raise SLCX029Error("result lacks DOS rows")
    return {int(row["energy"]): int(row["count"]) for row in rows}


def exact_step_table_match(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return left.get("step_tables") == right.get("step_tables")


def require_exact_step_table_match(left: Mapping[str, Any], right: Mapping[str, Any]) -> None:
    if not exact_step_table_match(left, right):
        raise ExactComparisonError("exact step-table roster mismatch")


def require_authority_dos_match(result: Mapping[str, Any], authority: Mapping[int, int]) -> None:
    if dos_mapping(result) != {int(energy): int(count) for energy, count in authority.items()}:
        raise ExactComparisonError("DOS coefficient vector differs from frozen authority")
    verification = result.get("verification")
    if not isinstance(verification, Mapping) or verification.get("status") != "PASS":
        raise ExactComparisonError("DOS invariant envelope did not pass")


__all__ = [
    "CAMPAIGN_ID",
    "FROZEN_CHUNK_CAP",
    "FROZEN_SELECTION_RULE",
    "PORTFOLIO_IDS",
    "SEALED_PARENT_ENGINE_SHA256",
    "SLCX029Error",
    "PortfolioValidationError",
    "ExactComparisonError",
    "RosterValidationError",
    "FrozenPolicyError",
    "canonical_sha256",
    "dos_mapping",
    "exact_step_table_match",
    "require_exact_step_table_match",
    "require_authority_dos_match",
    "fused_root_batch",
    "load_parent",
    "materialized_root_batch",
    "order_portfolio",
    "order_structure",
    "select_graph_only_order",
    "sha256_file",
    "solve_exact",
    "validate_instance",
    "validate_frozen_policy",
    "validate_portfolio_roster",
    "validate_unique_staged_roster",
]
