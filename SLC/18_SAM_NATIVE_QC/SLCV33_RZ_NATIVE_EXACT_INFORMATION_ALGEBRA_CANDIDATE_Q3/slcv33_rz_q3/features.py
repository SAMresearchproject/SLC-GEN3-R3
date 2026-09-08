"""Frozen-width Q3 representation derivation and feature receipts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from pathlib import Path
import sys
from typing import Iterable, Mapping

from .canonical import canonical_sha256
from .custody import CUSTODY_FEATURE_NAMES, CustodyProfile, build_custody_profile
from .foundation import BoundV6Foundation
from .geometry import HD_OBJECT_NAMES, build_visible_geometry, q2_compat_features70
from .graph import build_receipt_graph, encode_graph
from .hd import (
    HDSigma,
    base_feature_block,
    closure_feature_block,
    divide_hd,
    law_receipt,
    multiply_hd,
    relation_feature_block,
    sigma_hd,
)
from .source import Q2_ROOT, Q3Group, SourceVisibleChoice


class FeatureError(ValueError):
    """A Q3 feature schema, width, or source firewall differs."""


class Representation(str, Enum):
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3_FLAT = "R3_FLAT"
    R3_GRAPH = "R3_GRAPH"


REPRESENTATION_WIDTHS = {
    Representation.R0: 70,
    Representation.R1: 82,
    Representation.R2: 178,
    Representation.R3_FLAT: 200,
    Representation.R3_GRAPH: 200,
}

BASE_BLOCK_NAMES = ("zero", "sign", "v2", "v3", "u_numerator", "u_denominator")
RELATION_BLOCK_NAMES = (
    "undefined_quotient", "zero", "sign", "v2", "v3", "u_numerator", "u_denominator",
)
CLOSURE_NAMES = ("h4", "h12", "h18", "d18_12", "d9_8")
RELATION_PAIRS = ((0, 1), (2, 3), (4, 5))


def _q2_feature_names() -> tuple[str, ...]:
    if str(Q2_ROOT) not in sys.path:
        sys.path.insert(0, str(Q2_ROOT))
    from slcv32_rz_q2.engine import FEATURE_ORDER  # noqa: PLC0415

    if len(FEATURE_ORDER) != 70:
        raise FeatureError("frozen Q2 feature-order width differs")
    return tuple(f"q2.{name}" for name in FEATURE_ORDER)


def _r1_names() -> tuple[str, ...]:
    return _q2_feature_names() + tuple(
        f"hd.{name}.{coordinate}"
        for name in HD_OBJECT_NAMES
        for coordinate in ("zero", "v3")
    )


def _r2_names() -> tuple[str, ...]:
    names = list(_q2_feature_names())
    names.extend(
        f"hd.{name}.{coordinate}"
        for name in HD_OBJECT_NAMES
        for coordinate in BASE_BLOCK_NAMES
    )
    names.extend(
        f"hd.{name}.{coordinate}"
        for name in HD_OBJECT_NAMES
        for coordinate in CLOSURE_NAMES
    )
    for relation_index in range(3):
        for operation in ("product", "quotient"):
            names.extend(
                f"hd.relation{relation_index}.{operation}.{coordinate}"
                for coordinate in RELATION_BLOCK_NAMES
            )
    return tuple(names)


def _graph_names() -> tuple[str, ...]:
    return (
        _q2_feature_names()
        + tuple(f"graph.node_pool.{index:02d}" for index in range(48))
        + tuple(f"graph.edge_pool.{index:02d}" for index in range(56))
        + tuple(f"custody.{name}" for name in CUSTODY_FEATURE_NAMES)
        + (
            "graph.distinct_node_signature_count",
            "graph.zero_node_count",
            "graph.undefined_quotient_count",
            "graph.partition_block_second_moment",
        )
    )


FEATURE_SCHEMAS: dict[Representation, tuple[str, ...]] = {
    Representation.R0: _q2_feature_names(),
    Representation.R1: _r1_names(),
    Representation.R2: _r2_names(),
    Representation.R3_FLAT: _r2_names() + tuple(f"custody.{name}" for name in CUSTODY_FEATURE_NAMES),
    Representation.R3_GRAPH: _graph_names(),
}
for _representation, _names in FEATURE_SCHEMAS.items():
    if len(_names) != REPRESENTATION_WIDTHS[_representation] or len(set(_names)) != len(_names):
        raise FeatureError(f"frozen {_representation.value} schema width or uniqueness differs")


@dataclass(frozen=True, slots=True)
class FeatureReceipt:
    representation: Representation
    feature_names: tuple[str, ...]
    values: tuple[Fraction, ...]
    source_field_names: tuple[str, ...]
    hd_semantic_sha256s: tuple[str, ...]
    law_receipts: tuple[Mapping[str, object], ...]
    custody_audit_passed: bool | None
    foundation_import_semantic_sha256: str

    @property
    def semantic_sha256(self) -> str:
        return canonical_sha256(
            {
                "representation": self.representation.value,
                "feature_names": self.feature_names,
                "values": self.values,
                "source_field_names": self.source_field_names,
                "hd_semantic_sha256s": self.hd_semantic_sha256s,
                "law_receipts": self.law_receipts,
                "custody_audit_passed": self.custody_audit_passed,
                "foundation_import_semantic_sha256": self.foundation_import_semantic_sha256,
            }
        )


def _hd_roster(
    query: SourceVisibleChoice,
    candidate: SourceVisibleChoice,
    foundation: BoundV6Foundation,
) -> tuple[HDSigma, ...]:
    geometry = build_visible_geometry(query, candidate)
    return tuple(
        sigma_hd(
            value,
            foundation,
            source_provenance=f"Q3_SOURCE_VISIBLE_HD_OBJECT_{HD_OBJECT_NAMES[index]}",
        )
        for index, value in enumerate(geometry.hd_objects)
    )


def _relations(
    values: tuple[HDSigma, ...],
    foundation: BoundV6Foundation,
) -> tuple[tuple[HDSigma, ...], tuple[HDSigma, ...]]:
    products = tuple(
        multiply_hd(
            values[left],
            values[right],
            foundation,
            source_provenance=f"Q3_SOURCE_VISIBLE_RELATION_{index}_PRODUCT",
        )
        for index, (left, right) in enumerate(RELATION_PAIRS)
    )
    quotients = tuple(
        divide_hd(
            values[left],
            values[right],
            foundation,
            source_provenance=f"Q3_SOURCE_VISIBLE_RELATION_{index}_QUOTIENT",
        )
        for index, (left, right) in enumerate(RELATION_PAIRS)
    )
    return products, quotients


def derive_representation(
    representation: Representation | str,
    query: SourceVisibleChoice,
    candidate_group: Q3Group,
    foundation: BoundV6Foundation,
) -> FeatureReceipt:
    """Derive one target-blind representation from visible fields and roster counts."""

    selected = Representation(representation)
    return derive_all_representations(query, candidate_group, foundation)[selected]


def derive_all_representations(
    query: SourceVisibleChoice,
    candidate_group: Q3Group,
    foundation: BoundV6Foundation,
) -> dict[Representation, FeatureReceipt]:
    """Derive all five widths from one shared bound-V6 canonical object graph."""

    representative = min(
        (record.visible for record in candidate_group.records),
        key=lambda value: (
            value.left_shell,
            value.right_shell,
            value.left_direction,
            value.right_direction,
            value.route_domain,
            value.physical_relation_domain,
        ),
    )
    q2 = tuple(Fraction(value) for value in q2_compat_features70(query, representative))
    values = _hd_roster(query, representative, foundation)
    products, quotients = _relations(values, foundation)
    laws = tuple(
        law_receipt(values[left], values[right], foundation)
        for left, right in RELATION_PAIRS
    )
    if not all(row["product_direct_equality"] and row["quotient_direct_equality"] for row in laws):
        raise FeatureError("HD factor/product/quotient law audit differs")

    r1_values: list[Fraction] = []
    for value in values:
        r1_values.extend((Fraction(value.zero), Fraction(0 if value.zero else value.v3)))
    hd_flat = tuple(item for value in values for item in base_feature_block(value))
    closures = tuple(item for value in values for item in closure_feature_block(value))
    relation_values: list[Fraction] = []
    for product, quotient in zip(products, quotients, strict=True):
        relation_values.extend(relation_feature_block(product))
        relation_values.extend(relation_feature_block(quotient))
    r2 = q2 + hd_flat + closures + tuple(relation_values)
    custody = build_custody_profile(query, candidate_group, foundation)
    custody_block = custody.feature_block()
    graph_nodes, graph_edges = build_receipt_graph(
        values, products, quotients, custody, foundation
    )
    graph_augmentation = encode_graph(graph_nodes, graph_edges, custody)
    results = {
        Representation.R0: q2,
        Representation.R1: q2 + tuple(r1_values),
        Representation.R2: r2,
        Representation.R3_FLAT: r2 + custody_block,
        Representation.R3_GRAPH: (
            q2 + graph_augmentation[:104] + custody_block + graph_augmentation[104:]
        ),
    }
    foundation_semantic = str(foundation.import_receipt["semantic_sha256"])
    hd_semantics = tuple(
        value.semantic_sha256 for value in values + products + quotients
    )
    receipts: dict[Representation, FeatureReceipt] = {}
    for selected, result in results.items():
        expected = REPRESENTATION_WIDTHS[selected]
        if len(result) != expected:
            raise FeatureError(
                f"{selected.value} feature width differs: {len(result)} != {expected}"
            )
        if any(not isinstance(value, Fraction) for value in result):
            raise FeatureError("Q3 mathematical feature identity is not exact Fraction data")
        receipts[selected] = FeatureReceipt(
            representation=selected,
            feature_names=FEATURE_SCHEMAS[selected],
            values=result,
            source_field_names=tuple(SourceVisibleChoice.__dataclass_fields__),
            hd_semantic_sha256s=hd_semantics,
            law_receipts=laws,
            custody_audit_passed=(
                custody.audit.passed
                if selected in (Representation.R3_FLAT, Representation.R3_GRAPH)
                else None
            ),
            foundation_import_semantic_sha256=foundation_semantic,
        )
    return receipts


def zero_variance_receipt(
    representation: Representation | str,
    rows: Iterable[FeatureReceipt],
) -> dict[str, object]:
    selected = Representation(representation)
    frozen = tuple(rows)
    if not frozen or any(row.representation != selected for row in frozen):
        raise FeatureError("zero-variance census has no homogeneous feature rows")
    constant = tuple(
        FEATURE_SCHEMAS[selected][index]
        for index in range(REPRESENTATION_WIDTHS[selected])
        if len({row.values[index] for row in frozen}) == 1
    )
    return {
        "representation": selected.value,
        "row_count": len(frozen),
        "zero_variance_feature_names": constant,
        "zero_variance_count": len(constant),
        "status": "PASS_RECORDED_NOT_CREDITED_WITH_SELECTOR_LEVERAGE",
    }
