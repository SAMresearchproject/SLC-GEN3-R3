"""Exact boundary-transfer engine for the frozen SLCX027 motif ring.

The frozen twelve-site source cell has two directed edges removed from its
local factor set.  Four endpoint spins therefore form a 16-state boundary.
For a boundary state ``s`` this module constructs the exact shifted-energy
polynomial ``W[s]`` from every field and every uncut edge in the cell.  The
removed edges are owned exactly once by the inter-cell glue polynomial
``D[s,t]``.  At every NTT root the cell operator is

    T[s,t] = W[s] * D[s,t].

The ring partition polynomial is ``trace(T ** cell_count)``.  Matrix powers
are evaluated by binary exponentiation over each frozen prime field.  Modular
matrix multiplication reduces after *every* shared-state contribution, so no
sum of products is ever accumulated in an ``int64`` value.

This is a campaign sidecar.  It does not modify or relabel the sealed
SLCX023/SLCX024 predecessor engine and it does not treat the unrelated
480-state deterministic tape quotient as an Ising transfer object.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from time import perf_counter
from typing import Any, Mapping, Sequence

import numpy as np


FROZEN_NTT_PRIMES: tuple[int, ...] = (998244353, 1004535809, 469762049)
NTT_PRIMITIVE_ROOT = 3
CELL_SIZE = 12
PORT_BITS = 4
STATE_COUNT = 1 << PORT_BITS
MAX_NTT_LENGTH = 2048

EXPECTED_SOURCE_INSTANCE_ID = "SLCX023_N12_I00"
EXPECTED_SOURCE_SHA256 = "f2d5817bec5762381111d46b9bdf2e5a57fd691c8b135f2aee8851c74d3aa834"
EXPECTED_CUT_EDGES: tuple[tuple[int, int, int], ...] = ((0, 7, 2), (3, 9, -3))
EXPECTED_VAULT_SHA256 = "ff5408986ed611165e4f1b4444623f346df1448c97e4575b97c2666d231445df"
EXPECTED_VAULT_CONTENT_SHA256 = "b338fda8b82ebbe8233f875231d11a4eace6d3c1111461f2ba90504649feb62d"
EXPECTED_SEALED_ENGINE_SHA256 = "fb8bff08ae0836a628a90edb141f8e3d96ae13d96075eb2e2031d12737f77c5a"

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
DEFAULT_VAULT = BASE / "SLCX027_MOTIF_FAMILY_VAULT.json"
SEALED_PREDECESSOR_ENGINE = (
    ROOT
    / "18_SAM_NATIVE_QC"
    / "SLCX024_EXACT_N48_N60_FRUSTRATED_ISING_DOS_EXTENSION"
    / "release"
    / "executed_capsule"
    / "slcx023_exact_engine.py"
)


class TransferEngineError(RuntimeError):
    """Base class for SLCX027 transfer-engine failures."""


class TransferCustodyError(TransferEngineError):
    """Raised when a frozen input or ownership rule has changed."""


class TransferArithmeticError(TransferEngineError):
    """Raised when an exact arithmetic invariant fails."""


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _canonical_line_sha256(value: Any) -> str:
    """Match the precommit builder's canonical JSON plus trailing-LF hash."""

    return hashlib.sha256(_canonical_bytes(value) + b"\n").hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _plain_int(value: Any, label: str) -> int:
    if type(value) is not int:  # Deliberately reject bool.
        raise TransferCustodyError(f"{label} must be an integer")
    return value


def _instance_hash(instance: Mapping[str, Any]) -> str:
    core = {key: value for key, value in instance.items() if key != "instance_sha256"}
    return _canonical_sha256(core)


def _normalize_cut_edges(cut_edges: Sequence[Sequence[int]]) -> tuple[tuple[int, int, int], ...]:
    if isinstance(cut_edges, (str, bytes)) or len(cut_edges) != 2:
        raise TransferCustodyError("SLCX027 requires exactly two cut edges")
    normalized: list[tuple[int, int, int]] = []
    for index, raw in enumerate(cut_edges):
        if isinstance(raw, (str, bytes)) or len(raw) != 3:
            raise TransferCustodyError(f"cut_edges[{index}] must be [u,v,J]")
        u = _plain_int(raw[0], f"cut_edges[{index}][0]")
        v = _plain_int(raw[1], f"cut_edges[{index}][1]")
        coupling = _plain_int(raw[2], f"cut_edges[{index}][2]")
        normalized.append((u, v, coupling))
    return tuple(normalized)


def _validate_source_cell(source_cell: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(source_cell, Mapping):
        raise TransferCustodyError("source_cell must be a mapping")
    if source_cell.get("instance_id") != EXPECTED_SOURCE_INSTANCE_ID:
        raise TransferCustodyError("frozen source-cell identity changed")
    if _instance_hash(source_cell) != source_cell.get("instance_sha256"):
        raise TransferCustodyError("source-cell instance_sha256 mismatch")
    if source_cell.get("instance_sha256") != EXPECTED_SOURCE_SHA256:
        raise TransferCustodyError("source-cell hash differs from the SLCX027 precommit")

    n = _plain_int(source_cell.get("N"), "source_cell.N")
    if n != CELL_SIZE:
        raise TransferCustodyError("SLCX027 source cell must contain twelve sites")
    fields_raw = source_cell.get("fields")
    if not isinstance(fields_raw, list) or len(fields_raw) != CELL_SIZE:
        raise TransferCustodyError("source-cell fields must contain twelve entries")
    fields = tuple(_plain_int(value, f"source_cell.fields[{index}]") for index, value in enumerate(fields_raw))

    edges_raw = source_cell.get("edges")
    if not isinstance(edges_raw, list) or len(edges_raw) != 30:
        raise TransferCustodyError("source cell must contain the frozen thirty edges")
    edges: list[tuple[int, int, int]] = []
    seen_pairs: set[tuple[int, int]] = set()
    degrees = [0] * CELL_SIZE
    for index, raw in enumerate(edges_raw):
        if not isinstance(raw, list) or len(raw) != 3:
            raise TransferCustodyError(f"source_cell.edges[{index}] must be [u,v,J]")
        u = _plain_int(raw[0], f"source_cell.edges[{index}][0]")
        v = _plain_int(raw[1], f"source_cell.edges[{index}][1]")
        coupling = _plain_int(raw[2], f"source_cell.edges[{index}][2]")
        if not (0 <= u < v < CELL_SIZE):
            raise TransferCustodyError("source-cell edges must use canonical endpoints")
        if coupling == 0:
            raise TransferCustodyError("source-cell coupling cannot be zero")
        if (u, v) in seen_pairs:
            raise TransferCustodyError("source cell contains a parallel edge")
        seen_pairs.add((u, v))
        degrees[u] += 1
        degrees[v] += 1
        edges.append((u, v, coupling))
    if edges != sorted(edges):
        raise TransferCustodyError("source-cell edges are not canonically sorted")
    if any(degree != 5 for degree in degrees):
        raise TransferCustodyError("source-cell graph is not five-regular")

    bound = sum(abs(value) for value in fields) + sum(abs(edge[2]) for edge in edges)
    if source_cell.get("energy_bound_B") != bound:
        raise TransferCustodyError("source-cell energy bound mismatch")
    return {"fields": fields, "edges": tuple(edges), "bound": bound}


def _deterministic_cut_pair(source_cell: Mapping[str, Any]) -> tuple[tuple[int, int, int], ...]:
    witness_raw = source_cell.get("k33_witness_edges")
    if not isinstance(witness_raw, list):
        raise TransferCustodyError("source cell lacks its frozen K3,3 witness")
    witness = {tuple(map(int, edge)) for edge in witness_raw}
    eligible = [
        tuple(map(int, edge))
        for edge in source_cell["edges"]
        if (int(edge[0]), int(edge[1])) not in witness
    ]
    for left_index, left in enumerate(eligible):
        for right in eligible[left_index + 1 :]:
            if {left[0], left[1]}.isdisjoint({right[0], right[1]}) and left[2] * right[2] < 0:
                return left, right
    raise TransferCustodyError("source cell has no deterministic cut pair")


def validate_factor_ownership(
    source_cell: Mapping[str, Any],
    cut_edges: Sequence[Sequence[int]],
    *,
    omit_glue_index: int | None = None,
) -> dict[str, Any]:
    """Validate the frozen one-owner factor partition and return its ledger.

    Every field and every uncut edge belongs to ``W``.  Each cut edge belongs
    to ``D`` exactly once.  ``omit_glue_index`` is an explicit wrong control;
    it removes that glue factor only after the frozen ownership partition has
    passed.
    """

    source = _validate_source_cell(source_cell)
    cuts = _normalize_cut_edges(cut_edges)
    if cuts != EXPECTED_CUT_EDGES or cuts != _deterministic_cut_pair(source_cell):
        raise TransferCustodyError("cut edges differ from the frozen deterministic port rule")
    if not {cuts[0][0], cuts[0][1]}.isdisjoint({cuts[1][0], cuts[1][1]}):
        raise TransferCustodyError("cut edges are not vertex-disjoint")
    if cuts[0][2] * cuts[1][2] >= 0:
        raise TransferCustodyError("cut-edge coupling signs are not opposite")
    if omit_glue_index is not None:
        omit_glue_index = _plain_int(omit_glue_index, "omit_glue_index")
        if not 0 <= omit_glue_index < len(cuts):
            raise TransferCustodyError("omit_glue_index is outside the frozen glue list")

    source_edges = source["edges"]
    source_edge_set = set(source_edges)
    glue_edge_set = set(cuts)
    if len(glue_edge_set) != len(cuts) or not glue_edge_set.issubset(source_edge_set):
        raise TransferCustodyError("a cut edge is absent or duplicated in the source cell")
    local_edges = tuple(edge for edge in source_edges if edge not in glue_edge_set)
    if set(local_edges) & glue_edge_set or set(local_edges) | glue_edge_set != source_edge_set:
        raise TransferCustodyError("local/glue edge ownership is not a disjoint exact partition")

    port_vertices = tuple(sorted({endpoint for edge in cuts for endpoint in edge[:2]}))
    if len(port_vertices) != PORT_BITS:
        raise TransferCustodyError("the frozen cut does not expose four distinct port spins")
    local_bound = sum(abs(value) for value in source["fields"]) + sum(abs(edge[2]) for edge in local_edges)
    frozen_glue_bound = sum(abs(edge[2]) for edge in cuts)
    if local_bound + frozen_glue_bound != source["bound"]:
        raise TransferCustodyError("factor bounds do not reconstruct the source-cell bound")

    active_glue_edges = tuple(
        edge for index, edge in enumerate(cuts) if index != omit_glue_index
    )
    active_glue_bound = sum(abs(edge[2]) for edge in active_glue_edges)
    ownership_material = {
        "field_owners": [[vertex, "W"] for vertex in range(CELL_SIZE)],
        "edge_owners": [
            [edge[0], edge[1], edge[2], "D" if edge in glue_edge_set else "W"]
            for edge in source_edges
        ],
    }
    return {
        "status": "PASS",
        "source_factor_count": CELL_SIZE + len(source_edges),
        "local_field_factor_count": CELL_SIZE,
        "local_edge_factor_count": len(local_edges),
        "frozen_glue_factor_count": len(cuts),
        "active_glue_factor_count": len(active_glue_edges),
        "intentional_omitted_glue_factor_count": 0 if omit_glue_index is None else 1,
        "double_owned_factor_count": 0,
        "unowned_factor_count_before_wrong_control": 0,
        "all_source_factors_owned_once": True,
        "port_vertices": list(port_vertices),
        "local_edges": [list(edge) for edge in local_edges],
        "frozen_glue_edges": [list(edge) for edge in cuts],
        "active_glue_edges": [list(edge) for edge in active_glue_edges],
        "local_bound": local_bound,
        "frozen_glue_bound": frozen_glue_bound,
        "active_glue_bound": active_glue_bound,
        "frozen_per_cell_bound": local_bound + frozen_glue_bound,
        "active_per_cell_bound": local_bound + active_glue_bound,
        "ownership_sha256": _canonical_sha256(ownership_material),
    }


def load_frozen_vault(path: str | Path = DEFAULT_VAULT) -> dict[str, Any]:
    """Load and hash-check the frozen SLCX027 vault and predecessor custody."""

    vault_path = Path(path)
    if not vault_path.is_file():
        raise FileNotFoundError(vault_path)
    if _file_sha256(vault_path) != EXPECTED_VAULT_SHA256:
        raise TransferCustodyError("SLCX027 vault file hash mismatch")
    if not SEALED_PREDECESSOR_ENGINE.is_file():
        raise FileNotFoundError(SEALED_PREDECESSOR_ENGINE)
    if _file_sha256(SEALED_PREDECESSOR_ENGINE) != EXPECTED_SEALED_ENGINE_SHA256:
        raise TransferCustodyError("sealed predecessor engine hash mismatch")

    try:
        vault = json.loads(vault_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TransferCustodyError("SLCX027 vault is not valid JSON") from exc
    if not isinstance(vault, dict):
        raise TransferCustodyError("SLCX027 vault must be a JSON object")
    content_hash = vault.get("content_sha256")
    core = {key: value for key, value in vault.items() if key != "content_sha256"}
    if content_hash != EXPECTED_VAULT_CONTENT_SHA256 or _canonical_line_sha256(core) != content_hash:
        raise TransferCustodyError("SLCX027 vault content hash mismatch")
    if vault.get("schema") != "SLCX027_MOTIF_FAMILY_VAULT_V1":
        raise TransferCustodyError("unexpected SLCX027 vault schema")

    ownership = validate_factor_ownership(vault.get("source_cell"), vault.get("cut_edges"))
    if vault.get("port_vertices") != ownership["port_vertices"]:
        raise TransferCustodyError("vault port vertices differ from factor ownership")
    instances = vault.get("instances")
    if not isinstance(instances, list) or [row.get("cell_count") for row in instances] != [3, 4, 6]:
        raise TransferCustodyError("vault stage roster changed")
    for row in instances:
        if not isinstance(row, dict) or _instance_hash(row) != row.get("instance_sha256"):
            raise TransferCustodyError("vault ring-instance hash mismatch")
        cell_count = _plain_int(row.get("cell_count"), "vault cell_count")
        if row.get("N") != CELL_SIZE * cell_count:
            raise TransferCustodyError("vault ring size/cell-count mismatch")
        if row.get("energy_bound_B") != ownership["frozen_per_cell_bound"] * cell_count:
            raise TransferCustodyError("vault ring energy bound mismatch")
    return vault


def _ntt_length_for_bound(bound: int) -> int:
    if type(bound) is not int or bound < 0:
        raise TransferArithmeticError("energy bound must be a nonnegative integer")
    length = 1
    while length <= 2 * bound:
        length <<= 1
    if length > MAX_NTT_LENGTH:
        raise TransferArithmeticError("required NTT length exceeds the frozen campaign cap")
    return length


def _validate_primes(ntt_primes: Sequence[int], ntt_length: int) -> tuple[int, ...]:
    if isinstance(ntt_primes, (str, bytes)):
        raise TransferCustodyError("ntt_primes must be the frozen integer sequence")
    primes = tuple(_plain_int(value, "ntt prime") for value in ntt_primes)
    if primes != FROZEN_NTT_PRIMES:
        raise TransferCustodyError("all three frozen NTT primes are required in canonical order")
    for prime in primes:
        if (prime - 1) % ntt_length:
            raise TransferArithmeticError("required NTT length is unsupported by a frozen prime")
        if (prime - 1) * (prime - 1) + (prime - 1) > np.iinfo(np.int64).max:
            raise TransferArithmeticError("frozen prime is unsafe for reduced int64 products")
    return primes


def _ntt(values: Sequence[int], prime: int, *, inverse: bool) -> list[int]:
    length = len(values)
    if length == 0 or length & (length - 1):
        raise TransferArithmeticError("NTT vector length must be a nonzero power of two")
    if (prime - 1) % length:
        raise TransferArithmeticError("NTT length does not divide prime-1")
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
        if inverse:
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
    if inverse:
        inverse_length = pow(length, prime - 2, prime)
        result = [(value * inverse_length) % prime for value in result]
    return result


def forward_ntt(values: Sequence[int], prime: int) -> list[int]:
    """Return exact root evaluations in the predecessor engine's root order."""

    return _ntt(values, prime, inverse=False)


def inverse_ntt(values: Sequence[int], prime: int) -> list[int]:
    """Recover coefficient residues from exact root evaluations."""

    return _ntt(values, prime, inverse=True)


def _state_spin(state: int, vertex: int, port_positions: Mapping[int, int]) -> int:
    return 1 if state & (1 << port_positions[vertex]) else -1


def _compile_local_coefficients(
    source_cell: Mapping[str, Any],
    ownership: Mapping[str, Any],
) -> np.ndarray:
    fields = tuple(int(value) for value in source_cell["fields"])
    local_edges = tuple(tuple(map(int, edge)) for edge in ownership["local_edges"])
    port_vertices = tuple(int(value) for value in ownership["port_vertices"])
    port_positions = {vertex: position for position, vertex in enumerate(port_vertices)}
    local_bound = int(ownership["local_bound"])
    coefficients = np.zeros((STATE_COUNT, 2 * local_bound + 1), dtype=np.int64)

    for assignment in range(1 << CELL_SIZE):
        state = 0
        for position, vertex in enumerate(port_vertices):
            state |= ((assignment >> vertex) & 1) << position
        shifted_energy = 0
        for vertex, field in enumerate(fields):
            spin = 1 if assignment & (1 << vertex) else -1
            shifted_energy += -field * spin + abs(field)
        for u, v, coupling in local_edges:
            left_spin = 1 if assignment & (1 << u) else -1
            right_spin = 1 if assignment & (1 << v) else -1
            shifted_energy += -coupling * left_spin * right_spin + abs(coupling)
        if not 0 <= shifted_energy <= 2 * local_bound:
            raise TransferArithmeticError("local shifted energy escaped its owned bound")
        coefficients[state, shifted_energy] += 1

    expected_row_count = 1 << (CELL_SIZE - PORT_BITS)
    if any(int(total) != expected_row_count for total in coefficients.sum(axis=1)):
        raise TransferArithmeticError("a conditional cell polynomial has the wrong normalization")
    if int(coefficients.sum()) != 1 << CELL_SIZE:
        raise TransferArithmeticError("conditional cell polynomials lost source assignments")
    return coefficients


def _glue_degree_table(ownership: Mapping[str, Any]) -> np.ndarray:
    port_vertices = tuple(int(value) for value in ownership["port_vertices"])
    port_positions = {vertex: position for position, vertex in enumerate(port_vertices)}
    active_edges = tuple(tuple(map(int, edge)) for edge in ownership["active_glue_edges"])
    degrees = np.zeros((STATE_COUNT, STATE_COUNT), dtype=np.intp)
    for left_state in range(STATE_COUNT):
        for right_state in range(STATE_COUNT):
            degree = 0
            for source_vertex, target_vertex, coupling in active_edges:
                source_spin = _state_spin(left_state, source_vertex, port_positions)
                target_spin = _state_spin(right_state, target_vertex, port_positions)
                degree += -coupling * source_spin * target_spin + abs(coupling)
            degrees[left_state, right_state] = degree
    if int(degrees.min()) < 0 or int(degrees.max()) > 2 * int(ownership["active_glue_bound"]):
        raise TransferArithmeticError("glue shifted energy escaped its owned bound")
    return degrees


def _compile_transfer_at_roots(
    local_coefficients: np.ndarray,
    glue_degrees: np.ndarray,
    ntt_length: int,
    prime: int,
) -> np.ndarray:
    local_evaluations = np.empty((ntt_length, STATE_COUNT), dtype=np.int64)
    for state in range(STATE_COUNT):
        padded = [int(value) for value in local_coefficients[state, :]]
        padded.extend([0] * (ntt_length - len(padded)))
        local_evaluations[:, state] = np.asarray(forward_ntt(padded, prime), dtype=np.int64)

    omega = pow(NTT_PRIMITIVE_ROOT, (prime - 1) // ntt_length, prime)
    points = np.empty(ntt_length, dtype=np.int64)
    points[0] = 1
    for index in range(1, ntt_length):
        points[index] = points[index - 1] * omega % prime
    maximum_glue_degree = int(glue_degrees.max())
    root_powers = np.empty((maximum_glue_degree + 1, ntt_length), dtype=np.int64)
    root_powers[0, :] = 1
    for exponent in range(1, maximum_glue_degree + 1):
        root_powers[exponent, :] = root_powers[exponent - 1, :] * points % prime
    glue_evaluations = np.ascontiguousarray(root_powers[glue_degrees].transpose(2, 0, 1))
    transfer = local_evaluations[:, :, None] * glue_evaluations % prime
    return np.ascontiguousarray(transfer, dtype=np.int64)


def _residue_array(value: Any, prime: int, label: str) -> np.ndarray:
    array = np.asarray(value)
    if array.dtype.kind not in "iu" or array.ndim < 2:
        raise TransferArithmeticError(f"{label} must be an integer array with at least two axes")
    if np.any(array < 0) or np.any(array >= prime):
        raise TransferArithmeticError(f"{label} contains a value outside the prime field")
    return np.ascontiguousarray(array, dtype=np.int64)


def safe_modular_matmul(left: Any, right: Any, prime: int) -> np.ndarray:
    """Multiply residue matrices, reducing after every shared-state term.

    Leading batch dimensions must match.  Individual products of the frozen
    prime residues fit in signed ``int64``; the reduction inside the shared
    dimension prevents an unsafe accumulated dot product.
    """

    prime = _plain_int(prime, "prime")
    if prime not in FROZEN_NTT_PRIMES:
        raise TransferCustodyError("safe_modular_matmul requires a frozen prime")
    left_array = _residue_array(left, prime, "left")
    right_array = _residue_array(right, prime, "right")
    if left_array.shape[:-2] != right_array.shape[:-2]:
        raise TransferArithmeticError("matrix batch dimensions do not match")
    if left_array.shape[-1] != right_array.shape[-2]:
        raise TransferArithmeticError("matrix inner dimensions do not match")
    output_shape = left_array.shape[:-2] + (left_array.shape[-2], right_array.shape[-1])
    result = np.zeros(output_shape, dtype=np.int64)
    for shared in range(left_array.shape[-1]):
        product = (
            left_array[..., :, shared, None]
            * right_array[..., shared, None, :]
        ) % prime
        # This reduction is intentionally inside the shared-state loop.
        result = (result + product) % prime
    return np.ascontiguousarray(result)


def _matrix_power_with_metrics(matrix: Any, exponent: int, prime: int) -> tuple[np.ndarray, int]:
    exponent = _plain_int(exponent, "matrix exponent")
    if exponent <= 0:
        raise TransferArithmeticError("matrix exponent must be positive")
    base = _residue_array(matrix, prime, "matrix")
    if base.shape[-2] != base.shape[-1]:
        raise TransferArithmeticError("matrix power requires square matrices")
    identity = np.eye(base.shape[-1], dtype=np.int64)
    result = np.broadcast_to(identity, base.shape).copy()
    operations = 0
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = safe_modular_matmul(result, base, prime)
            operations += 1
        remaining >>= 1
        if remaining:
            base = safe_modular_matmul(base, base, prime)
            operations += 1
    return result, operations


def modular_matrix_power(matrix: Any, exponent: int, prime: int) -> np.ndarray:
    """Binary matrix power over one frozen prime field."""

    return _matrix_power_with_metrics(matrix, exponent, prime)[0]


def _elementwise_power_with_metrics(matrix: Any, exponent: int, prime: int) -> tuple[np.ndarray, int]:
    exponent = _plain_int(exponent, "elementwise exponent")
    if exponent <= 0:
        raise TransferArithmeticError("elementwise exponent must be positive")
    base = _residue_array(matrix, prime, "matrix")
    result = np.ones(base.shape, dtype=np.int64)
    operations = 0
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = result * base % prime
            operations += 1
        remaining >>= 1
        if remaining:
            base = base * base % prime
            operations += 1
    return np.ascontiguousarray(result), operations


def _readout(powered: np.ndarray, mode: str, prime: int) -> np.ndarray:
    if mode == "trace":
        return np.asarray(np.trace(powered, axis1=-2, axis2=-1) % prime, dtype=np.int64)
    if mode == "sum":
        return np.asarray(np.sum(powered, axis=(-2, -1), dtype=np.int64) % prime, dtype=np.int64)
    raise TransferCustodyError("readout must be 'trace' or 'sum'")


def _configuration_count(exponent: int, readout: str, composition: str) -> int:
    if composition == "matrix":
        extra_bits = 0 if readout == "trace" else PORT_BITS
        return 1 << (CELL_SIZE * exponent + extra_bits)
    if composition == "elementwise":
        extra_bits = PORT_BITS if readout == "trace" else 2 * PORT_BITS
        return 1 << ((CELL_SIZE - PORT_BITS) * exponent + extra_bits)
    raise TransferCustodyError("composition must be 'matrix' or 'elementwise'")


def _crt(residues: Sequence[int], primes: Sequence[int]) -> int:
    if not residues or len(residues) != len(primes):
        raise TransferArithmeticError("CRT residue/modulus arity mismatch")
    value = int(residues[0])
    modulus = int(primes[0])
    for residue, prime in zip(residues[1:], primes[1:]):
        correction = ((int(residue) - value) % prime) * pow(modulus, -1, prime) % prime
        value += modulus * correction
        modulus *= prime
    return value


def dos_raw_moments(dos: Mapping[int, int], maximum_order: int = 4) -> list[int]:
    """Return exact raw energy-moment sums from order one through ``maximum_order``."""

    maximum_order = _plain_int(maximum_order, "maximum_order")
    if maximum_order < 1:
        raise TransferArithmeticError("maximum_order must be positive")
    return [
        sum(int(count) * int(energy) ** order for energy, count in dos.items())
        for order in range(1, maximum_order + 1)
    ]


def solve_ring(
    source_cell: Mapping[str, Any],
    cut_edges: Sequence[Sequence[int]],
    cell_count: int,
    ntt_primes: Sequence[int] = FROZEN_NTT_PRIMES,
    *,
    omit_glue_index: int | None = None,
    exponent_override: int | None = None,
    readout: str = "trace",
    composition: str = "matrix",
) -> dict[str, Any]:
    """Solve one frozen repeated-motif ring exactly.

    The default controls implement ``trace(T ** cell_count)``.  The keyword
    switches are deliberately explicit wrong-control helpers:

    * ``omit_glue_index`` removes one of the two glue factors;
    * ``exponent_override`` changes the number of composed motif operators;
    * ``readout='sum'`` sums every final matrix entry;
    * ``composition='elementwise'`` uses Hadamard rather than matrix powers.

    The returned ``bound`` is the active shifted-energy bound, so wrong
    controls remain exact solutions of the altered algebra rather than being
    silently reindexed against the correct Hamiltonian.
    """

    started = perf_counter()
    validation_started = perf_counter()
    vault = load_frozen_vault()
    if _canonical_bytes(source_cell) != _canonical_bytes(vault["source_cell"]):
        raise TransferCustodyError("solve_ring source cell differs from the frozen vault")
    normalized_cuts = _normalize_cut_edges(cut_edges)
    if normalized_cuts != tuple(tuple(map(int, edge)) for edge in vault["cut_edges"]):
        raise TransferCustodyError("solve_ring cut edges differ from the frozen vault")
    cell_count = _plain_int(cell_count, "cell_count")
    if cell_count <= 0:
        raise TransferCustodyError("cell_count must be positive")
    frozen_cell_counts = tuple(int(row["cell_count"]) for row in vault["instances"])
    if cell_count not in frozen_cell_counts:
        raise TransferCustodyError("cell_count is outside the frozen SLCX027 stage roster")
    if exponent_override is None:
        exponent = cell_count
    else:
        exponent = _plain_int(exponent_override, "exponent_override")
        if exponent <= 0:
            raise TransferCustodyError("exponent_override must be positive")
    if readout not in {"trace", "sum"}:
        raise TransferCustodyError("readout must be 'trace' or 'sum'")
    if composition not in {"matrix", "elementwise"}:
        raise TransferCustodyError("composition must be 'matrix' or 'elementwise'")

    ownership = validate_factor_ownership(
        source_cell,
        normalized_cuts,
        omit_glue_index=omit_glue_index,
    )
    per_cell_bound = int(ownership["active_per_cell_bound"])
    bound = per_cell_bound * exponent
    ntt_length = _ntt_length_for_bound(bound)
    primes = _validate_primes(ntt_primes, ntt_length)
    expected_configuration_count = _configuration_count(exponent, readout, composition)
    crt_modulus = 1
    for prime in primes:
        crt_modulus *= prime
    if crt_modulus <= expected_configuration_count:
        raise TransferArithmeticError("frozen CRT modulus cannot reconstruct the requested exact count")
    validation_seconds = perf_counter() - validation_started

    local_started = perf_counter()
    local_coefficients = _compile_local_coefficients(source_cell, ownership)
    glue_degrees = _glue_degree_table(ownership)
    local_seconds = perf_counter() - local_started

    modular_coefficients: list[list[int]] = []
    prime_metrics: list[dict[str, Any]] = []
    root_zero_residues: list[int] = []
    for prime in primes:
        prime_started = perf_counter()
        compile_started = perf_counter()
        transfer = _compile_transfer_at_roots(
            local_coefficients,
            glue_degrees,
            ntt_length,
            prime,
        )
        transfer_compile_seconds = perf_counter() - compile_started

        composition_started = perf_counter()
        if composition == "matrix":
            powered, power_operations = _matrix_power_with_metrics(transfer, exponent, prime)
        else:
            powered, power_operations = _elementwise_power_with_metrics(transfer, exponent, prime)
        evaluations = _readout(powered, readout, prime)
        composition_seconds = perf_counter() - composition_started
        root_zero = int(evaluations[0])
        if root_zero != expected_configuration_count % prime:
            raise TransferArithmeticError("root-zero normalization failed")
        root_zero_residues.append(root_zero)

        inverse_started = perf_counter()
        coefficients = inverse_ntt([int(value) for value in evaluations], prime)
        inverse_seconds = perf_counter() - inverse_started
        if any(coefficients[index] for index in range(2 * bound + 1, ntt_length)):
            raise TransferArithmeticError("inverse NTT produced aliased coefficients above 2B")
        modular_coefficients.append(coefficients)
        prime_metrics.append(
            {
                "prime": prime,
                "ntt_length": ntt_length,
                "root_evaluations": ntt_length,
                "transfer_shape": [STATE_COUNT, STATE_COUNT],
                "binary_power_operations": power_operations,
                "transfer_compile_seconds": transfer_compile_seconds,
                "composition_seconds": composition_seconds,
                "inverse_ntt_seconds": inverse_seconds,
                "total_prime_seconds": perf_counter() - prime_started,
                "coefficient_residue_sha256": _canonical_sha256(coefficients),
            }
        )

    reconstruction_started = perf_counter()
    coefficient_vector = [
        _crt(
            [modular_coefficients[prime_index][coefficient] for prime_index in range(len(primes))],
            primes,
        )
        for coefficient in range(ntt_length)
    ]
    if any(coefficient_vector[index] for index in range(2 * bound + 1, ntt_length)):
        raise TransferArithmeticError("CRT reconstruction has support above the active bound")
    active_coefficients = coefficient_vector[: 2 * bound + 1]
    if any(value < 0 or value > expected_configuration_count for value in active_coefficients):
        raise TransferArithmeticError("CRT coefficient lies outside its exact counting range")
    if any(value for degree, value in enumerate(active_coefficients) if degree & 1):
        raise TransferArithmeticError("shifted Ising polynomial violated even-degree parity")
    dos = {
        degree - bound: int(count)
        for degree, count in enumerate(active_coefficients)
        if count
    }
    dos = dict(sorted(dos.items()))
    observed_configuration_count = sum(dos.values())
    if observed_configuration_count != expected_configuration_count:
        raise TransferArithmeticError("recovered DOS failed exact normalization")
    reconstruction_seconds = perf_counter() - reconstruction_started

    controls = {
        "omit_glue_index": omit_glue_index,
        "exponent_override": exponent_override,
        "readout": readout,
        "composition": composition,
    }
    is_correct_path = (
        omit_glue_index is None
        and exponent_override is None
        and readout == "trace"
        and composition == "matrix"
    )
    moments = dos_raw_moments(dos, 4)
    local_polynomial_sha256 = _canonical_sha256(local_coefficients.tolist())
    glue_degree_table_sha256 = _canonical_sha256(glue_degrees.tolist())
    dos_sha256 = _canonical_sha256([[energy, count] for energy, count in dos.items()])
    total_seconds = perf_counter() - started
    timing = {
        "validation_seconds": validation_seconds,
        "local_polynomial_compile_seconds": local_seconds,
        "prime_seconds": [row["total_prime_seconds"] for row in prime_metrics],
        "crt_and_dos_seconds": reconstruction_seconds,
        "total_seconds": total_seconds,
        "end_to_end_seconds": total_seconds,
        "scope": [
            "vault_and_predecessor_custody",
            "factor_ownership_validation",
            "conditional_W_and_glue_D_build",
            "all_frozen_primes_and_roots",
            "binary_power_and_readout",
            "inverse_NTT_and_CRT",
            "DOS_invariants_moments_and_hashes",
        ],
    }
    return {
        "schema": "SLCX027_EXACT_BOUNDARY_TRANSFER_RESULT_V1",
        "method": "EXACT_NTT_16_STATE_BOUNDARY_TRANSFER_RING",
        "source_cell_instance_id": source_cell["instance_id"],
        "source_cell_sha256": source_cell["instance_sha256"],
        "cut_edges": [list(edge) for edge in normalized_cuts],
        "cell_count": cell_count,
        "composition_exponent": exponent,
        "target_N": CELL_SIZE * cell_count,
        "composition_N": CELL_SIZE * exponent,
        "controls": controls,
        "is_correct_path": is_correct_path,
        "dos": dos,
        "ntt_length": ntt_length,
        "bound": bound,
        "ntt_primes": list(primes),
        "timing": timing,
        "metrics": {
            "state_count": STATE_COUNT,
            "transfer_shape": [STATE_COUNT, STATE_COUNT],
            "port_bit_order": ownership["port_vertices"],
            "state_bit_convention": "bit=0 spin=-1; bit=1 spin=+1",
            "active_per_cell_bound": per_cell_bound,
            "frozen_per_cell_bound": ownership["frozen_per_cell_bound"],
            "crt_modulus_product": crt_modulus,
            "expected_configuration_count": expected_configuration_count,
            "observed_configuration_count": observed_configuration_count,
            "occupied_energy_bins": len(dos),
            "minimum_energy": min(dos),
            "maximum_energy": max(dos),
            "ground_state_degeneracy": dos[min(dos)],
            "raw_moment_sums_1_through_4": moments,
            "raw_moment_sums": {str(order): value for order, value in enumerate(moments, 1)},
            "local_polynomial_sha256": local_polynomial_sha256,
            "glue_degree_table_sha256": glue_degree_table_sha256,
            "dos_sha256": dos_sha256,
            "modular_matmul_reduction": "after_each_shared_state",
            "prime_metrics": prime_metrics,
        },
        "factor_ownership": ownership,
        "verification": {
            "status": "PASS",
            "path_status": "CORRECT_PATH" if is_correct_path else "EXACT_WRONG_CONTROL_PATH",
            "vault_sha256": EXPECTED_VAULT_SHA256,
            "sealed_predecessor_engine_sha256": EXPECTED_SEALED_ENGINE_SHA256,
            "root_zero_residues": root_zero_residues,
            "configuration_count_pass": True,
            "coefficient_support_pass": True,
            "even_shifted_degree_parity_pass": True,
            "factor_ownership_pass": True,
        },
    }


__all__ = [
    "FROZEN_NTT_PRIMES",
    "TransferArithmeticError",
    "TransferCustodyError",
    "TransferEngineError",
    "dos_raw_moments",
    "forward_ntt",
    "inverse_ntt",
    "load_frozen_vault",
    "modular_matrix_power",
    "safe_modular_matmul",
    "solve_ring",
    "validate_factor_ownership",
]
