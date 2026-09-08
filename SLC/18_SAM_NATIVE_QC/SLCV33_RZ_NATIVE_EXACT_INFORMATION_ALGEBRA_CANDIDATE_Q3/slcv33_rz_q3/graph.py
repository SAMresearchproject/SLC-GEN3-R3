"""Equal-width typed receipt-graph encoder for R3_GRAPH."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from .custody import CustodyProfile
from .foundation import BoundV6Foundation
from .hd import HDSigma, sigma_hd, structured_node_block


NODE_TYPES = ("HD_VALUE", "ALGEBRA_RESULT", "PARTITION", "RECEIPT")
EDGE_TYPES = (
    "PRODUCT_LEFT",
    "PRODUCT_RIGHT",
    "QUOTIENT_NUMERATOR",
    "QUOTIENT_DENOMINATOR",
    "PARTITION_REFINES",
    "RECEIPT_SELECTS",
    "COMPOSES",
    "UNCOMPUTES",
)


class GraphEncodingError(ValueError):
    """The typed Q3 graph or its frozen width differs."""


@dataclass(frozen=True, slots=True)
class GraphNode:
    key: str
    node_type: str
    value: HDSigma


@dataclass(frozen=True, slots=True)
class GraphEdge:
    source: str
    target: str
    edge_type: str


def build_receipt_graph(
    hd_values: tuple[HDSigma, ...],
    products: tuple[HDSigma, ...],
    quotients: tuple[HDSigma, ...],
    custody: CustodyProfile,
    foundation: BoundV6Foundation,
) -> tuple[tuple[GraphNode, ...], tuple[GraphEdge, ...]]:
    if len(hd_values) != 6 or len(products) != 3 or len(quotients) != 3:
        raise GraphEncodingError("frozen graph algebra roster differs")
    nodes: list[GraphNode] = []
    for index, value in enumerate(hd_values):
        nodes.append(GraphNode(f"v{index}", "HD_VALUE", value))
    for index, value in enumerate(products):
        nodes.append(GraphNode(f"p{index}", "ALGEBRA_RESULT", value))
    for index, value in enumerate(quotients):
        nodes.append(GraphNode(f"q{index}", "ALGEBRA_RESULT", value))

    best = custody.best_orientation_multiplicity
    other = custody.other_orientation_multiplicity
    multiplicity = custody.direct_multiplicity
    partition_values = (multiplicity, 2, max(best, other))
    receipt_values = (multiplicity, 2, max(best, other))
    for index, value in enumerate(partition_values):
        nodes.append(GraphNode(
            f"partition{index}",
            "PARTITION",
            sigma_hd(
                value,
                foundation,
                source_provenance=f"Q3_SOURCE_VISIBLE_PARTITION_VALUE_{index}",
            ),
        ))
    for index, value in enumerate(receipt_values):
        nodes.append(GraphNode(
            f"receipt{index}",
            "RECEIPT",
            sigma_hd(
                value,
                foundation,
                source_provenance=f"Q3_SOURCE_VISIBLE_RECEIPT_VALUE_{index}",
            ),
        ))

    edges: list[GraphEdge] = []
    for index, (left, right) in enumerate(((0, 1), (2, 3), (4, 5))):
        edges.extend(
            (
                GraphEdge(f"v{left}", f"p{index}", "PRODUCT_LEFT"),
                GraphEdge(f"v{right}", f"p{index}", "PRODUCT_RIGHT"),
                GraphEdge(f"v{left}", f"q{index}", "QUOTIENT_NUMERATOR"),
                GraphEdge(f"v{right}", f"q{index}", "QUOTIENT_DENOMINATOR"),
            )
        )
    edges.extend(
        (
            GraphEdge("partition0", "partition1", "PARTITION_REFINES"),
            GraphEdge("partition1", "partition2", "PARTITION_REFINES"),
            GraphEdge("receipt1", "partition1", "RECEIPT_SELECTS"),
            GraphEdge("receipt2", "partition2", "RECEIPT_SELECTS"),
            GraphEdge("receipt1", "receipt0", "COMPOSES"),
            GraphEdge("receipt2", "receipt0", "COMPOSES"),
            GraphEdge("receipt0", "receipt1", "UNCOMPUTES"),
            GraphEdge("receipt0", "receipt2", "UNCOMPUTES"),
        )
    )
    return tuple(nodes), tuple(edges)


def _edge_moments(source: tuple[Fraction, ...], target: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    # Block order: undefined, zero, sign, v2, v3, u_num, u_den, closures...
    return (
        Fraction(1),
        source[3],
        source[4],
        target[3],
        target[4],
        source[2] * target[2],
        source[0] + source[1] + target[0] + target[1],
    )


def encode_graph(
    nodes: Iterable[GraphNode],
    edges: Iterable[GraphEdge],
    custody: CustodyProfile,
) -> tuple[Fraction, ...]:
    """Return 108 exact graph coordinates, independent of input ordering."""

    node_rows = tuple(nodes)
    edge_rows = tuple(edges)
    if any(node.node_type not in NODE_TYPES for node in node_rows):
        raise GraphEncodingError("graph node type differs")
    if any(edge.edge_type not in EDGE_TYPES for edge in edge_rows):
        raise GraphEncodingError("graph edge type differs")
    by_key = {node.key: node for node in node_rows}
    if len(by_key) != len(node_rows):
        raise GraphEncodingError("graph node keys are not unique")
    blocks = {key: structured_node_block(node.value) for key, node in by_key.items()}

    node_pool: list[Fraction] = []
    for node_type in NODE_TYPES:
        selected = [blocks[node.key] for node in node_rows if node.node_type == node_type]
        if not selected:
            raise GraphEncodingError(f"graph has no {node_type} node")
        node_pool.extend(sum((row[index] for row in selected), Fraction()) for index in range(12))

    edge_pool: list[Fraction] = []
    for edge_type in EDGE_TYPES:
        selected = [edge for edge in edge_rows if edge.edge_type == edge_type]
        totals = [Fraction(0)] * 7
        for edge in selected:
            if edge.source not in blocks or edge.target not in blocks:
                raise GraphEncodingError("graph edge references an unknown node")
            for index, value in enumerate(_edge_moments(blocks[edge.source], blocks[edge.target])):
                totals[index] += value
        edge_pool.extend(totals)

    signatures = {blocks[node.key] for node in node_rows}
    zero_count = sum(node.value.zero for node in node_rows)
    undefined_count = sum(node.value.undefined for node in node_rows)
    partition_second_moment = (
        custody.best_orientation_multiplicity ** 2
        + custody.other_orientation_multiplicity ** 2
    )
    invariants = (
        Fraction(len(signatures)),
        Fraction(zero_count),
        Fraction(undefined_count),
        Fraction(partition_second_moment),
    )
    result = tuple(node_pool) + tuple(edge_pool) + invariants
    if len(result) != 108:
        raise GraphEncodingError(f"graph augmentation width differs: {len(result)}")
    return result
