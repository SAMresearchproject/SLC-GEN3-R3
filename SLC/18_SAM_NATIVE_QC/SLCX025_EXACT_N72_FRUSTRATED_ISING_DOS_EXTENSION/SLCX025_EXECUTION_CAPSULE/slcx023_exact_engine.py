"""Deterministic exact engines for the SLCX023 weighted-Ising DOS ladder.

This module deliberately keeps two computational authorities separate:

* :func:`gray_code_dos` enumerates assignments in reflected Gray order and
  updates the integer Hamiltonian after the one changed spin.
* :func:`ntt_variable_elimination` evaluates the shifted DOS polynomial at
  exact NTT roots, performs scalar variable elimination at every root, applies
  an inverse NTT, and reconstructs the integer coefficients by CRT.

The variable-elimination implementation is a transparent development sidecar.
It is not an operator already installed in SAM Language v0.7.  Its boundary
tables are hashed at every elimination so a typed lane can retain the complete
message custody without pretending that a terminal digest proves the work.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import numpy as np


NTT_PRIMES: tuple[int, ...] = (998244353, 1004535809, 469762049)
NTT_PRIMITIVE_ROOT = 3
ALLOWED_SIZES = frozenset({12, 24, 36})
ALLOWED_COUPLINGS = frozenset({-3, -2, -1, 1, 2, 3})
ALLOWED_FIELDS = frozenset({-2, -1, 0, 1, 2})
CELL_SIZE = 12
MAX_GRAY_N = 24
MAX_NTT_LENGTH = 2048
DEFAULT_ROOT_BATCH_SIZE = 8

LEAF_DOMAIN = b"SLCX023-GROUND-STATE-LEAF-V1\x00"
NODE_DOMAIN = b"SLCX023-GROUND-STATE-NODE-V1\x00"
REFERENCE_RECEIPT_DOMAIN = "SLCX023-REFERENCE-VE-RECEIPT-V1"
TYPED_RECEIPT_DOMAIN = "SLCX023-TYPED-BOUNDARY-RECEIPT-V1"
BOUNDARY_TABLE_DOMAIN = "SLCX023-BOUNDARY-TABLE-V1"
PERMUTATION_DOMAIN = "SLCX023-VERTEX-PERMUTATION-V1"
GAUGE_DOMAIN = "SLCX023-ISING-GAUGE-V1"


class ExactEngineError(RuntimeError):
    """Base class for deterministic exact-engine failures."""


class InstanceValidationError(ExactEngineError):
    """Raised when a corpus or transformed instance violates its contract."""


class ExactArithmeticError(ExactEngineError):
    """Raised when an exact reconstruction or invariant fails."""


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _domain_hash(domain: str, value: Any) -> str:
    return hashlib.sha256(domain.encode("ascii") + b"\x00" + _canonical_bytes(value)).hexdigest()


def _require_plain_int(value: Any, label: str) -> int:
    if type(value) is not int:  # bool is intentionally not an integer here.
        raise InstanceValidationError(f"{label} must be an integer")
    return value


def _instance_core(instance: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in instance.items() if key != "instance_sha256"}


def _connected(n: int, edge_pairs: Iterable[tuple[int, int]]) -> bool:
    adjacency = [set() for _ in range(n)]
    for u, v in edge_pairs:
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = {0}
    queue: deque[int] = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == n


def _crossing_stats(n: int, edge_pairs: Iterable[tuple[int, int]]) -> tuple[int, list[list[int]]]:
    cell_count = n // CELL_SIZE
    pair_counts = [[0 for _ in range(cell_count)] for _ in range(cell_count)]
    cross = 0
    for u, v in edge_pairs:
        left, right = u // CELL_SIZE, v // CELL_SIZE
        if left != right:
            cross += 1
            pair_counts[left][right] += 1
            pair_counts[right][left] += 1
    return cross, pair_counts


def _induced_width(n: int, edge_pairs: Iterable[tuple[int, int]], order: Sequence[int]) -> int:
    adjacency = {vertex: set() for vertex in range(n)}
    for u, v in edge_pairs:
        adjacency[u].add(v)
        adjacency[v].add(u)
    remaining = set(range(n))
    width = 0
    for vertex in order:
        if vertex not in remaining:
            raise InstanceValidationError("elimination order is not a vertex permutation")
        neighbors = sorted(adjacency[vertex] & remaining)
        width = max(width, len(neighbors))
        for left_index, left in enumerate(neighbors):
            for right in neighbors[left_index + 1 :]:
                adjacency[left].add(right)
                adjacency[right].add(left)
        for neighbor in neighbors:
            adjacency[neighbor].discard(vertex)
        remaining.remove(vertex)
    if remaining:
        raise InstanceValidationError("elimination order omitted vertices")
    return width


def _validate_k33_witness(
    witness: Any,
    edge_pairs: set[tuple[int, int]],
    n: int,
) -> list[tuple[int, int]]:
    if not isinstance(witness, list) or len(witness) != 9:
        raise InstanceValidationError("k33_witness_edges must contain nine edges")
    witness_pairs: list[tuple[int, int]] = []
    for index, raw in enumerate(witness):
        if not isinstance(raw, list) or len(raw) != 2:
            raise InstanceValidationError(f"k33_witness_edges[{index}] is malformed")
        u = _require_plain_int(raw[0], f"k33_witness_edges[{index}][0]")
        v = _require_plain_int(raw[1], f"k33_witness_edges[{index}][1]")
        if not (0 <= u < n and 0 <= v < n and u != v):
            raise InstanceValidationError("K3,3 witness vertex is out of range")
        pair = (min(u, v), max(u, v))
        if pair not in edge_pairs:
            raise InstanceValidationError("K3,3 witness edge is absent from the graph")
        witness_pairs.append(pair)
    if len(set(witness_pairs)) != 9:
        raise InstanceValidationError("K3,3 witness contains duplicate edges")

    adjacency: dict[int, set[int]] = defaultdict(set)
    for u, v in witness_pairs:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if len(adjacency) != 6 or any(len(neighbors) != 3 for neighbors in adjacency.values()):
        raise InstanceValidationError("supplied witness is not a six-vertex cubic graph")
    colors: dict[int, int] = {}
    for root in adjacency:
        if root in colors:
            continue
        colors[root] = 0
        queue: deque[int] = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    raise InstanceValidationError("supplied K3,3 witness is not bipartite")
    if sorted(colors.values()).count(0) != 3 or sorted(colors.values()).count(1) != 3:
        raise InstanceValidationError("supplied witness does not have a 3+3 bipartition")
    return sorted(witness_pairs)


def _ntt_length_for_bound(bound: int) -> int:
    length = 1
    while length <= 2 * bound:
        length <<= 1
    return length


def validate_instance(instance: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one frozen or deterministic metamorphic instance.

    The function raises :class:`InstanceValidationError` on the first failure
    and otherwise returns a compact validation report.  It never mutates the
    supplied mapping.
    """

    if not isinstance(instance, Mapping):
        raise InstanceValidationError("instance must be a mapping")
    instance_id = instance.get("instance_id")
    if not isinstance(instance_id, str) or not instance_id:
        raise InstanceValidationError("instance_id must be a non-empty string")
    n = _require_plain_int(instance.get("N"), "N")
    if n not in ALLOWED_SIZES:
        raise InstanceValidationError(f"N must be one of {sorted(ALLOWED_SIZES)}")
    if instance.get("cell_size") != CELL_SIZE or instance.get("cell_count") != n // CELL_SIZE:
        raise InstanceValidationError("cell_size/cell_count mismatch")

    fields_raw = instance.get("fields")
    if not isinstance(fields_raw, list) or len(fields_raw) != n:
        raise InstanceValidationError("fields must contain exactly N entries")
    fields = [_require_plain_int(value, f"fields[{index}]") for index, value in enumerate(fields_raw)]
    if any(value not in ALLOWED_FIELDS for value in fields):
        raise InstanceValidationError("field lies outside the frozen alphabet")

    edges_raw = instance.get("edges")
    if not isinstance(edges_raw, list):
        raise InstanceValidationError("edges must be a list")
    weighted_edges: list[tuple[int, int, int]] = []
    edge_pairs: set[tuple[int, int]] = set()
    degrees = [0] * n
    for index, raw in enumerate(edges_raw):
        if not isinstance(raw, list) or len(raw) != 3:
            raise InstanceValidationError(f"edges[{index}] must be [u,v,J]")
        u = _require_plain_int(raw[0], f"edges[{index}][0]")
        v = _require_plain_int(raw[1], f"edges[{index}][1]")
        coupling = _require_plain_int(raw[2], f"edges[{index}][2]")
        if not (0 <= u < v < n):
            raise InstanceValidationError("edges must use canonical u<v endpoints")
        if coupling not in ALLOWED_COUPLINGS:
            raise InstanceValidationError("coupling lies outside the frozen alphabet")
        if (u, v) in edge_pairs:
            raise InstanceValidationError("parallel edge detected")
        edge_pairs.add((u, v))
        weighted_edges.append((u, v, coupling))
        degrees[u] += 1
        degrees[v] += 1
    if weighted_edges != sorted(weighted_edges):
        raise InstanceValidationError("weighted edges are not canonically sorted")
    expected_edge_count = 5 * n // 2
    if len(weighted_edges) != expected_edge_count or instance.get("edge_count") != expected_edge_count:
        raise InstanceValidationError("edge_count is not five-regular")
    if any(degree != 5 for degree in degrees):
        raise InstanceValidationError("graph is not five-regular")
    if not _connected(n, edge_pairs):
        raise InstanceValidationError("graph is disconnected")
    witness_pairs = _validate_k33_witness(instance.get("k33_witness_edges"), edge_pairs, n)

    bound = sum(abs(coupling) for _, _, coupling in weighted_edges) + sum(abs(value) for value in fields)
    if instance.get("energy_bound_B") != bound:
        raise InstanceValidationError("energy_bound_B mismatch")
    ntt_length = _ntt_length_for_bound(bound)
    if ntt_length > MAX_NTT_LENGTH:
        raise InstanceValidationError("frozen NTT length exceeds the campaign cap")
    for prime in NTT_PRIMES:
        if (prime - 1) % ntt_length:
            raise InstanceValidationError("NTT length is unsupported by a frozen prime")

    cross, pair_counts = _crossing_stats(n, edge_pairs)
    if instance.get("cross_cell_edge_count") != cross:
        raise InstanceValidationError("cross_cell_edge_count mismatch")
    if instance.get("cell_pair_edge_counts") != pair_counts:
        raise InstanceValidationError("cell_pair_edge_counts mismatch")

    orders = instance.get("orders")
    widths = instance.get("induced_widths")
    if not isinstance(orders, Mapping) or not isinstance(widths, Mapping):
        raise InstanceValidationError("orders and induced_widths must be mappings")
    required_orders = {"min_fill", "min_degree", "cell_min_fill"}
    if not required_orders.issubset(orders) or not required_orders.issubset(widths):
        raise InstanceValidationError("one or more frozen elimination orders are absent")
    observed_widths: dict[str, int] = {}
    for name in sorted(required_orders):
        raw_order = orders[name]
        if not isinstance(raw_order, list) or len(raw_order) != n:
            raise InstanceValidationError(f"orders[{name}] has the wrong length")
        order = [_require_plain_int(value, f"orders[{name}]") for value in raw_order]
        if sorted(order) != list(range(n)):
            raise InstanceValidationError(f"orders[{name}] is not a vertex permutation")
        width = _induced_width(n, edge_pairs, order)
        if widths[name] != width:
            raise InstanceValidationError(f"induced width mismatch for {name}")
        observed_widths[name] = width

    expected_hash = _canonical_sha256(_instance_core(instance))
    if instance.get("instance_sha256") != expected_hash:
        raise InstanceValidationError("instance_sha256 mismatch")

    return {
        "status": "PASS",
        "instance_id": instance_id,
        "instance_sha256": expected_hash,
        "N": n,
        "edge_count": len(weighted_edges),
        "energy_bound_B": bound,
        "ntt_length": ntt_length,
        "induced_widths": observed_widths,
        "k33_witness_sha256": _canonical_sha256([list(pair) for pair in witness_pairs]),
    }


def load_corpus(path: str | Path) -> list[dict[str, Any]]:
    """Load and validate the complete frozen six-instance JSONL corpus."""

    corpus_path = Path(path)
    if not corpus_path.is_file():
        raise FileNotFoundError(corpus_path)
    instances: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(corpus_path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise InstanceValidationError(f"invalid JSON on corpus line {line_number}") from exc
        if not isinstance(value, dict):
            raise InstanceValidationError(f"corpus line {line_number} is not an object")
        validate_instance(value)
        instances.append(value)
    ids = [row["instance_id"] for row in instances]
    hashes = [row["instance_sha256"] for row in instances]
    if len(ids) != len(set(ids)) or len(hashes) != len(set(hashes)):
        raise InstanceValidationError("corpus contains duplicate identities or hashes")
    roster = {n: sum(row["N"] == n for row in instances) for n in sorted(ALLOWED_SIZES)}
    if roster != {12: 2, 24: 2, 36: 2}:
        raise InstanceValidationError(f"frozen corpus roster mismatch: {roster}")
    return instances


def _weighted_edges(instance: Mapping[str, Any]) -> list[tuple[int, int, int]]:
    return [(int(u), int(v), int(coupling)) for u, v, coupling in instance["edges"]]


def _adjacency(instance: Mapping[str, Any]) -> list[list[tuple[int, int]]]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(int(instance["N"]))]
    for u, v, coupling in _weighted_edges(instance):
        adjacency[u].append((v, coupling))
        adjacency[v].append((u, coupling))
    for neighbors in adjacency:
        neighbors.sort()
    return adjacency


def _energy_for_basis(instance: Mapping[str, Any], basis: int) -> int:
    n = int(instance["N"])
    if type(basis) is not int or not 0 <= basis < (1 << n):
        raise ExactArithmeticError("basis index is out of range")
    spins = [1 if basis & (1 << vertex) else -1 for vertex in range(n)]
    energy = -sum(coupling * spins[u] * spins[v] for u, v, coupling in _weighted_edges(instance))
    energy -= sum(int(field) * spins[vertex] for vertex, field in enumerate(instance["fields"]))
    return energy


def merkle_root(states: Iterable[int], n: int) -> str:
    """Return the canonical custody root of an ordered ground-state set.

    The root is a commitment only; it is intentionally not described as a
    proof that the supplied list is complete.
    """

    n = _require_plain_int(n, "n")
    if n <= 0:
        raise ExactArithmeticError("n must be positive")
    ordered = sorted(_require_plain_int(value, "ground state") for value in states)
    if not ordered:
        raise ExactArithmeticError("a ground-state Merkle tree cannot be empty")
    if len(ordered) != len(set(ordered)):
        raise ExactArithmeticError("ground-state list contains duplicates")
    if ordered[0] < 0 or ordered[-1] >= (1 << n):
        raise ExactArithmeticError("ground-state basis index is out of range")
    width = (n + 7) // 8
    n_bytes = n.to_bytes(4, "big", signed=False)
    layer = [
        hashlib.sha256(LEAF_DOMAIN + n_bytes + state.to_bytes(width, "big", signed=False)).digest()
        for state in ordered
    ]
    while len(layer) > 1:
        if len(layer) & 1:
            layer.append(layer[-1])
        layer = [
            hashlib.sha256(NODE_DOMAIN + layer[index] + layer[index + 1]).digest()
            for index in range(0, len(layer), 2)
        ]
    return layer[0].hex()


def gray_code_dos(instance: Mapping[str, Any]) -> dict[str, Any]:
    """Compute the complete DOS by independent Gray-code enumeration."""

    report = validate_instance(instance)
    n = report["N"]
    if n > MAX_GRAY_N:
        raise ExactEngineError(f"Gray enumeration is frozen only through N={MAX_GRAY_N}")
    fields = [int(value) for value in instance["fields"]]
    adjacency = _adjacency(instance)
    spins = [-1] * n
    energy = _energy_for_basis(instance, 0)
    histogram: dict[int, int] = defaultdict(int)
    histogram[energy] = 1
    minimum = energy
    ground_states: list[int] = [0]
    prior_gray = 0
    state_count = 1 << n

    # Local bindings materially reduce the 2^24 Python-loop overhead while
    # preserving the plainly independent enumeration lane.
    local_spins = spins
    local_adjacency = adjacency
    local_fields = fields
    local_histogram = histogram
    for step in range(1, state_count):
        gray = step ^ (step >> 1)
        changed = gray ^ prior_gray
        vertex = changed.bit_length() - 1
        old_spin = local_spins[vertex]
        local_field = local_fields[vertex]
        for neighbor, coupling in local_adjacency[vertex]:
            local_field += coupling * local_spins[neighbor]
        energy += 2 * old_spin * local_field
        local_spins[vertex] = -old_spin
        local_histogram[energy] += 1
        if energy < minimum:
            minimum = energy
            ground_states = [gray]
        elif energy == minimum:
            ground_states.append(gray)
        prior_gray = gray

    ordered_dos = dict(sorted(local_histogram.items()))
    ground_states.sort()
    verification = verify_dos(instance, ordered_dos)
    if verification["status"] != "PASS":
        raise ExactArithmeticError("Gray-code DOS failed its exact invariants")
    if len(ground_states) != ordered_dos[minimum]:
        raise ExactArithmeticError("ground-state list does not match the minimum DOS coefficient")
    return {
        "method": "GRAY_EXHAUSTIVE_INCREMENTAL",
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "dos": ordered_dos,
        "ground_states": ground_states,
        "ground_state_merkle_root": merkle_root(ground_states, n),
        "metrics": {
            "N": n,
            "configurations": state_count,
            "incremental_updates": state_count - 1,
            "occupied_energy_bins": len(ordered_dos),
            "minimum_energy": minimum,
            "maximum_energy": max(ordered_dos),
            "ground_state_degeneracy": len(ground_states),
        },
        "verification": verification,
    }


def _hamiltonian_monomials(instance: Mapping[str, Any]) -> dict[int, int]:
    coefficients: dict[int, int] = defaultdict(int)
    for u, v, coupling in _weighted_edges(instance):
        coefficients[(1 << u) | (1 << v)] -= coupling
    for vertex, field in enumerate(instance["fields"]):
        if field:
            coefficients[1 << vertex] -= int(field)
    return {mask: value for mask, value in coefficients.items() if value}


def xor_moments(instance: Mapping[str, Any]) -> dict[str, Any]:
    """Compute raw energy moments one through four without using a DOS.

    Walsh monomials multiply by XOR of their vertex masks.  The calculation
    therefore depends only on the Hamiltonian term ledger and is independent
    of both exact DOS engines.
    """

    report = validate_instance(instance)
    n = report["N"]
    terms = _hamiltonian_monomials(instance)
    square: dict[int, int] = defaultdict(int)
    term_items = list(terms.items())
    for left_mask, left_coefficient in term_items:
        for right_mask, right_coefficient in term_items:
            square[left_mask ^ right_mask] += left_coefficient * right_coefficient
    per_configuration = {
        1: terms.get(0, 0),
        2: square.get(0, 0),
        3: sum(value * terms.get(mask, 0) for mask, value in square.items()),
        4: sum(value * value for value in square.values()),
    }
    scale = 1 << n
    raw_sums = {power: value * scale for power, value in per_configuration.items()}
    return {
        "method": "INDEPENDENT_XOR_MONOMIAL_CONTRACTION",
        "instance_id": instance["instance_id"],
        "monomial_count": len(terms),
        "xor_square_support": len(square),
        "per_configuration": per_configuration,
        "raw_sums": raw_sums,
    }


def _normalize_dos(dos: Mapping[Any, Any]) -> dict[int, int]:
    if not isinstance(dos, Mapping):
        raise ExactArithmeticError("DOS must be a mapping")
    normalized: dict[int, int] = {}
    for raw_energy, raw_count in dos.items():
        if type(raw_energy) is int:
            energy = raw_energy
        elif isinstance(raw_energy, str):
            try:
                energy = int(raw_energy)
            except ValueError as exc:
                raise ExactArithmeticError("DOS energy key is not an integer") from exc
            if str(energy) != raw_energy.strip():
                raise ExactArithmeticError("DOS energy key is not canonical")
        else:
            raise ExactArithmeticError("DOS energy key is not an integer")
        if type(raw_count) is not int:
            raise ExactArithmeticError("DOS count is not an exact integer")
        if energy in normalized:
            raise ExactArithmeticError("DOS contains duplicate canonical energies")
        normalized[energy] = raw_count
    if not normalized:
        raise ExactArithmeticError("DOS cannot be empty")
    return dict(sorted(normalized.items()))


def verify_dos(instance: Mapping[str, Any], dos: Mapping[Any, Any]) -> dict[str, Any]:
    """Return exact DOS invariant checks, including independent moments 1..4."""

    report = validate_instance(instance)
    n = report["N"]
    bound = report["energy_bound_B"]
    normalized = _normalize_dos(dos)
    counts = list(normalized.values())
    occupied = [energy for energy, count in normalized.items() if count]
    expected_parity = sum(_hamiltonian_monomials(instance).values()) & 1
    independent = xor_moments(instance)["raw_sums"]
    observed = {
        power: sum((energy**power) * count for energy, count in normalized.items())
        for power in range(1, 5)
    }
    checks = {
        "counts_nonnegative_exact_integers": all(type(count) is int and count >= 0 for count in counts),
        "total_configuration_count": sum(counts) == (1 << n),
        "occupied_support_nonempty": bool(occupied),
        "energy_bound": bool(occupied) and min(occupied) >= -bound and max(occupied) <= bound,
        "energy_parity": bool(occupied) and all((energy & 1) == expected_parity for energy in occupied),
        "first_moment": observed[1] == independent[1],
        "second_moment": observed[2] == independent[2],
        "third_moment": observed[3] == independent[3],
        "fourth_moment": observed[4] == independent[4],
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "status": status,
        "instance_id": instance["instance_id"],
        "checks": checks,
        "N": n,
        "energy_bound_B": bound,
        "expected_energy_parity": expected_parity,
        "minimum_energy": min(occupied) if occupied else None,
        "maximum_energy": max(occupied) if occupied else None,
        "ground_state_degeneracy": normalized[min(occupied)] if occupied else None,
        "occupied_energy_bins": len(occupied),
        "configuration_count": sum(counts),
        "observed_raw_moment_sums": observed,
        "independent_raw_moment_sums": independent,
    }


@dataclass(frozen=True)
class _Factor:
    scope: tuple[int, ...]
    values: np.ndarray


def _root_power_table(points: np.ndarray, maximum_power: int, prime: int) -> np.ndarray:
    table = np.empty((maximum_power + 1, len(points)), dtype=np.int64)
    table[0, :] = 1
    for exponent in range(1, maximum_power + 1):
        table[exponent, :] = (table[exponent - 1, :] * points) % prime
    return table


def _initial_factors(
    instance: Mapping[str, Any],
    points: np.ndarray,
    prime: int,
) -> list[_Factor]:
    maximum_power = max(
        [2 * abs(int(value)) for value in instance["fields"]]
        + [2 * abs(coupling) for _, _, coupling in _weighted_edges(instance)]
        + [0]
    )
    powers = _root_power_table(points, maximum_power, prime)
    factors: list[_Factor] = []
    for vertex, raw_field in enumerate(instance["fields"]):
        field = int(raw_field)
        exponents = []
        for bit in (0, 1):
            spin = 1 if bit else -1
            exponents.append(-field * spin + abs(field))
        values = np.stack([powers[exponent, :] for exponent in exponents], axis=0)
        factors.append(_Factor((vertex,), np.ascontiguousarray(values, dtype=np.int64)))
    for u, v, coupling in _weighted_edges(instance):
        exponents = []
        for assignment in range(4):
            left_spin = 1 if assignment & 1 else -1
            right_spin = 1 if assignment & 2 else -1
            exponents.append(-coupling * left_spin * right_spin + abs(coupling))
        values = np.stack([powers[exponent, :] for exponent in exponents], axis=0)
        factors.append(_Factor((u, v), np.ascontiguousarray(values, dtype=np.int64)))
    return factors


def _factor_index_map(union_scope: tuple[int, ...], factor_scope: tuple[int, ...]) -> np.ndarray:
    assignment_count = 1 << len(union_scope)
    assignments = np.arange(assignment_count, dtype=np.uint64)
    positions = {vertex: position for position, vertex in enumerate(union_scope)}
    indices = np.zeros(assignment_count, dtype=np.uint64)
    for factor_position, vertex in enumerate(factor_scope):
        indices |= ((assignments >> positions[vertex]) & 1) << factor_position
    return indices.astype(np.intp, copy=False)


def _remove_assignment_bit(remaining: np.ndarray, position: int) -> np.ndarray:
    low_mask = (1 << position) - 1
    low = remaining & low_mask
    high = remaining >> position
    return low | (high << (position + 1))


def _ve_root_batch(
    instance: Mapping[str, Any],
    order: Sequence[int],
    points: np.ndarray,
    prime: int,
    on_step: Callable[[dict[str, Any], np.ndarray], None],
) -> tuple[np.ndarray, dict[str, int]]:
    factors = _initial_factors(instance, points, prime)
    peak_assignments = 1
    peak_entries = len(points)
    for step_index, vertex in enumerate(order):
        selected = [factor for factor in factors if vertex in factor.scope]
        factors = [factor for factor in factors if vertex not in factor.scope]
        if not selected:
            # This generic case is not reached by the connected frozen corpus,
            # but summing a genuinely free spin must still contribute exactly 2.
            output = np.full((1, len(points)), 2, dtype=np.int64)
            output_scope: tuple[int, ...] = ()
            union_scope = (vertex,)
            input_factor_count = 0
        else:
            union_scope = tuple(sorted({site for factor in selected for site in factor.scope}))
            assignment_count = 1 << len(union_scope)
            peak_assignments = max(peak_assignments, assignment_count)
            peak_entries = max(peak_entries, assignment_count * len(points))
            product = np.ones((assignment_count, len(points)), dtype=np.int64)
            for factor in selected:
                indices = _factor_index_map(union_scope, factor.scope)
                selected_values = factor.values[indices, :]
                product = (product * selected_values) % prime
            position = union_scope.index(vertex)
            output_scope = tuple(site for site in union_scope if site != vertex)
            remaining = np.arange(1 << len(output_scope), dtype=np.uint64)
            zero_indices = _remove_assignment_bit(remaining, position).astype(np.intp, copy=False)
            one_indices = (zero_indices | (1 << position)).astype(np.intp, copy=False)
            output = (product[zero_indices, :] + product[one_indices, :]) % prime
        output = np.ascontiguousarray(output, dtype=np.int64)
        factors.append(_Factor(output_scope, output))
        on_step(
            {
                "step": step_index + 1,
                "eliminated_vertex": vertex,
                "input_factor_count": len(selected),
                "union_scope": list(union_scope),
                "output_scope": list(output_scope),
                "output_assignment_count": int(output.shape[0]),
            },
            output,
        )

    if any(factor.scope for factor in factors):
        raise ExactArithmeticError("variable elimination left an unresolved boundary")
    terminal = np.ones(len(points), dtype=np.int64)
    for factor in factors:
        terminal = (terminal * factor.values[0, :]) % prime
    return terminal, {
        "peak_union_assignments_per_root": peak_assignments,
        "peak_batch_table_entries": peak_entries,
    }


def _inverse_ntt(values: Sequence[int], prime: int) -> list[int]:
    length = len(values)
    if length == 0 or length & (length - 1):
        raise ExactArithmeticError("NTT vector length must be a nonzero power of two")
    if (prime - 1) % length:
        raise ExactArithmeticError("NTT length does not divide prime-1")
    result = [int(value) % prime for value in values]
    left = 0
    for right in range(1, length):
        bit = length >> 1
        while left & bit:
            left ^= bit
            bit >>= 1
        left ^= bit
        if right < left:
            result[right], result[left] = result[left], result[right]
    block = 2
    while block <= length:
        root = pow(NTT_PRIMITIVE_ROOT, (prime - 1) // block, prime)
        root = pow(root, prime - 2, prime)
        half = block >> 1
        for offset in range(0, length, block):
            multiplier = 1
            for index in range(offset, offset + half):
                even = result[index]
                odd = result[index + half] * multiplier % prime
                result[index] = (even + odd) % prime
                result[index + half] = (even - odd) % prime
                multiplier = multiplier * root % prime
        block <<= 1
    inverse_length = pow(length, prime - 2, prime)
    return [(value * inverse_length) % prime for value in result]


def _selected_primes(n: int) -> tuple[int, ...]:
    selected: list[int] = []
    product = 1
    for prime in NTT_PRIMES:
        selected.append(prime)
        product *= prime
        if product > (1 << n):
            return tuple(selected)
    raise ExactArithmeticError("frozen CRT modulus product is too small")


def _crt(residues: Sequence[int], primes: Sequence[int]) -> int:
    if len(residues) != len(primes) or not residues:
        raise ExactArithmeticError("CRT residue/modulus arity mismatch")
    value = int(residues[0])
    modulus = int(primes[0])
    for residue, prime in zip(residues[1:], primes[1:]):
        correction = ((int(residue) - value) % prime) * pow(modulus, -1, prime) % prime
        value += modulus * correction
        modulus *= prime
    return value


def ntt_variable_elimination(
    instance: Mapping[str, Any],
    order_name: str,
    typed: bool = False,
) -> dict[str, Any]:
    """Compute an exact DOS by NTT-root variable elimination and CRT.

    ``typed`` changes the custody domain, not the numerical recurrence.  The
    intended independent lanes use different frozen orders (``min_degree`` for
    reference and ``cell_min_fill`` for typed), while coefficient equality is
    the authority.
    """

    report = validate_instance(instance)
    n = report["N"]
    bound = report["energy_bound_B"]
    if order_name not in instance["orders"]:
        raise ExactEngineError(f"unknown frozen order {order_name!r}")
    order = [int(value) for value in instance["orders"][order_name]]
    if sorted(order) != list(range(n)):
        raise ExactEngineError("supplied order is not a vertex permutation")
    ntt_length = _ntt_length_for_bound(bound)
    primes = _selected_primes(n)
    root_batch_size = min(DEFAULT_ROOT_BATCH_SIZE, ntt_length)
    modular_coefficients: list[list[int]] = []
    receipts: list[dict[str, Any]] = []
    prime_metrics: list[dict[str, Any]] = []
    receipt_domain = TYPED_RECEIPT_DOMAIN if typed else REFERENCE_RECEIPT_DOMAIN
    prior_receipt_hash = "0" * 64

    for prime_index, prime in enumerate(primes):
        omega = pow(NTT_PRIMITIVE_ROOT, (prime - 1) // ntt_length, prime)
        evaluations = [0] * ntt_length
        step_hashers: list[hashlib._Hash] = []  # type: ignore[attr-defined]
        step_metadata: list[dict[str, Any]] = []
        peak_union_assignments = 0
        peak_batch_entries = 0

        for batch_start in range(0, ntt_length, root_batch_size):
            batch_stop = min(ntt_length, batch_start + root_batch_size)
            root_indices = range(batch_start, batch_stop)
            points = np.asarray([pow(omega, index, prime) for index in root_indices], dtype=np.int64)

            def on_step(metadata: dict[str, Any], table: np.ndarray) -> None:
                step_index = metadata["step"] - 1
                if batch_start == 0:
                    header = {
                        "schema": BOUNDARY_TABLE_DOMAIN,
                        "instance_sha256": instance["instance_sha256"],
                        "order_name": order_name,
                        "typed": bool(typed),
                        "prime": prime,
                        "ntt_length": ntt_length,
                        **metadata,
                        "root_major_assignment_order": True,
                    }
                    hasher = hashlib.sha256()
                    hasher.update(BOUNDARY_TABLE_DOMAIN.encode("ascii") + b"\x00")
                    hasher.update(_canonical_bytes(header) + b"\x00")
                    step_hashers.append(hasher)
                    step_metadata.append(header)
                else:
                    expected = step_metadata[step_index]
                    for key in (
                        "step",
                        "eliminated_vertex",
                        "input_factor_count",
                        "union_scope",
                        "output_scope",
                        "output_assignment_count",
                    ):
                        if expected[key] != metadata[key]:
                            raise ExactArithmeticError("boundary structure changed across NTT batches")
                # Canonical root-major order makes the table hash independent
                # of the private batching used to control peak memory.
                root_major = np.ascontiguousarray(table.T, dtype=">u8")
                step_hashers[step_index].update(root_major.tobytes(order="C"))

            terminal, batch_metrics = _ve_root_batch(instance, order, points, prime, on_step)
            evaluations[batch_start:batch_stop] = [int(value) for value in terminal]
            peak_union_assignments = max(
                peak_union_assignments,
                batch_metrics["peak_union_assignments_per_root"],
            )
            peak_batch_entries = max(peak_batch_entries, batch_metrics["peak_batch_table_entries"])

        coefficients = _inverse_ntt(evaluations, prime)
        modular_coefficients.append(coefficients)
        prime_metrics.append(
            {
                "prime": prime,
                "ntt_length": ntt_length,
                "root_evaluations": ntt_length,
                "root_batch_size": root_batch_size,
                "peak_union_assignments_per_root": peak_union_assignments,
                "peak_batch_table_entries": peak_batch_entries,
                "conceptual_peak_all_roots_entries": peak_union_assignments * ntt_length,
                "coefficient_residue_sha256": _canonical_sha256(coefficients),
            }
        )
        for metadata, hasher in zip(step_metadata, step_hashers):
            table_hash = hasher.hexdigest()
            receipt_material = {
                "schema": receipt_domain,
                "prior_receipt_hash": prior_receipt_hash,
                "table_hash": table_hash,
                "prime_index": prime_index,
                **metadata,
            }
            receipt_hash = _domain_hash(receipt_domain, receipt_material)
            receipts.append(
                {
                    **receipt_material,
                    "receipt_hash": receipt_hash,
                }
            )
            prior_receipt_hash = receipt_hash

    coefficient_vector = [
        _crt([modular_coefficients[index][coefficient] for index in range(len(primes))], primes)
        for coefficient in range(ntt_length)
    ]
    if any(coefficient_vector[index] for index in range(2 * bound + 1, ntt_length)):
        raise ExactArithmeticError("inverse NTT produced aliased coefficients above 2B")
    maximum_count = 1 << n
    if any(value < 0 or value > maximum_count for value in coefficient_vector[: 2 * bound + 1]):
        raise ExactArithmeticError("CRT coefficient lies outside the exact counting range")
    dos = {
        shifted_energy - bound: count
        for shifted_energy, count in enumerate(coefficient_vector[: 2 * bound + 1])
        if count
    }
    dos = dict(sorted(dos.items()))
    verification = verify_dos(instance, dos)
    if verification["status"] != "PASS":
        raise ExactArithmeticError("NTT/VE DOS failed its exact invariants")
    return {
        "method": "SLC_TYPED_NTT_ROOT_VARIABLE_ELIMINATION" if typed else "REFERENCE_NTT_ROOT_VARIABLE_ELIMINATION",
        "instance_id": instance["instance_id"],
        "instance_sha256": instance["instance_sha256"],
        "order_name": order_name,
        "order": order,
        "typed": bool(typed),
        "dos": dos,
        "receipts": receipts,
        "terminal_receipt_hash": prior_receipt_hash,
        "metrics": {
            "N": n,
            "energy_bound_B": bound,
            "ntt_length": ntt_length,
            "selected_primes": list(primes),
            "crt_modulus_product": int(np.prod(np.asarray(primes, dtype=object))),
            "frozen_induced_width": instance["induced_widths"][order_name],
            "elimination_steps_per_prime": n,
            "boundary_receipts": len(receipts),
            "occupied_energy_bins": len(dos),
            "minimum_energy": min(dos),
            "maximum_energy": max(dos),
            "ground_state_degeneracy": dos[min(dos)],
            "prime_metrics": prime_metrics,
        },
        "verification": verification,
    }


def _refresh_transformed_instance(instance: dict[str, Any]) -> dict[str, Any]:
    n = int(instance["N"])
    instance["edges"] = sorted([list(edge) for edge in instance["edges"]])
    instance["edge_count"] = len(instance["edges"])
    instance["cell_size"] = CELL_SIZE
    instance["cell_count"] = n // CELL_SIZE
    pairs = [(int(u), int(v)) for u, v, _ in instance["edges"]]
    cross, pair_counts = _crossing_stats(n, pairs)
    instance["cross_cell_edge_count"] = cross
    instance["cell_pair_edge_counts"] = pair_counts
    instance["energy_bound_B"] = sum(abs(int(edge[2])) for edge in instance["edges"]) + sum(
        abs(int(value)) for value in instance["fields"]
    )
    instance["induced_widths"] = {
        name: _induced_width(n, pairs, [int(value) for value in order])
        for name, order in instance["orders"].items()
    }
    instance.pop("instance_sha256", None)
    instance["instance_sha256"] = _canonical_sha256(instance)
    validate_instance(instance)
    return instance


def permute_instance(instance: Mapping[str, Any]) -> dict[str, Any]:
    """Return the frozen deterministic vertex-relabeling metamorphic control."""

    validate_instance(instance)
    n = int(instance["N"])
    base_hash = str(instance["instance_sha256"])
    old_vertices = list(range(n))
    new_to_old = sorted(
        old_vertices,
        key=lambda vertex: hashlib.sha256(
            f"{PERMUTATION_DOMAIN}|{base_hash}|{vertex}".encode("ascii")
        ).digest(),
    )
    if new_to_old == old_vertices:
        new_to_old = new_to_old[1:] + new_to_old[:1]
    old_to_new = [0] * n
    for new, old in enumerate(new_to_old):
        old_to_new[old] = new

    transformed = json.loads(json.dumps(instance))
    transformed["instance_id"] = f"{instance['instance_id']}__VERTEX_PERMUTED"
    transformed["fields"] = [int(instance["fields"][old]) for old in new_to_old]
    transformed_edges: list[list[int]] = []
    for u, v, coupling in _weighted_edges(instance):
        left, right = sorted((old_to_new[u], old_to_new[v]))
        transformed_edges.append([left, right, coupling])
    transformed["edges"] = sorted(transformed_edges)
    transformed["k33_witness_edges"] = sorted(
        [sorted((old_to_new[int(u)], old_to_new[int(v)])) for u, v in instance["k33_witness_edges"]]
    )
    transformed["orders"] = {
        name: [old_to_new[int(vertex)] for vertex in order]
        for name, order in instance["orders"].items()
    }
    transformed["transformation"] = {
        "kind": "VERTEX_PERMUTATION",
        "domain": PERMUTATION_DOMAIN,
        "base_instance_sha256": base_hash,
        "old_to_new": old_to_new,
        "new_to_old": new_to_old,
    }
    return _refresh_transformed_instance(transformed)


def gauge_transform(instance: Mapping[str, Any]) -> dict[str, Any]:
    """Return a deterministic local Ising gauge transformation of an instance."""

    validate_instance(instance)
    n = int(instance["N"])
    base_hash = str(instance["instance_sha256"])
    eta = [
        1
        if hashlib.sha256(f"{GAUGE_DOMAIN}|{base_hash}|{vertex}".encode("ascii")).digest()[0] & 1
        else -1
        for vertex in range(n)
    ]
    if all(value == eta[0] for value in eta):
        eta[0] *= -1

    transformed = json.loads(json.dumps(instance))
    transformed["instance_id"] = f"{instance['instance_id']}__GAUGE"
    transformed["fields"] = [eta[vertex] * int(field) for vertex, field in enumerate(instance["fields"])]
    transformed["edges"] = [
        [u, v, eta[u] * eta[v] * coupling]
        for u, v, coupling in _weighted_edges(instance)
    ]
    transformed["transformation"] = {
        "kind": "LOCAL_ISING_GAUGE",
        "domain": GAUGE_DOMAIN,
        "base_instance_sha256": base_hash,
        "eta": eta,
        "rule": "J_uv'=eta_u*eta_v*J_uv__h_u'=eta_u*h_u",
    }
    return _refresh_transformed_instance(transformed)


__all__ = [
    "ExactArithmeticError",
    "ExactEngineError",
    "InstanceValidationError",
    "NTT_PRIMES",
    "gauge_transform",
    "gray_code_dos",
    "load_corpus",
    "merkle_root",
    "ntt_variable_elimination",
    "permute_instance",
    "validate_instance",
    "verify_dos",
    "xor_moments",
]
