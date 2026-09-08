"""Binding-gated exact Q3 catalog construction and Q2 continuity replay."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys
from typing import Any, Mapping

from .binding import DEFAULT_BINDING_PATH, require_sealed_icf1_binding
from .canonical import canonical_sha256
from .comparator import load_q2_current_model, score_q2_current
from .evaluation import EvaluationResult, evaluate_complete_catalog
from .features import (
    FEATURE_SCHEMAS,
    FeatureReceipt,
    Representation,
    derive_all_representations,
)
from .foundation import BoundV6Foundation
from .source import (
    Q1_ROOT,
    SPLITS,
    Q3Group,
    Q3Inventory,
    SourceVisibleChoice,
    load_target_choices,
)
from .training import RankRow, selected_tiers


class CatalogError(RuntimeError):
    """The exact Q3 catalog roster, target tiers, or continuity replay differs."""


@dataclass(frozen=True, slots=True)
class Q3CatalogBundle:
    """One split-local, all-representation catalog with exact receipts."""

    split: str
    rows_by_representation: Mapping[Representation, Mapping[str, tuple[RankRow, ...]]]
    complete_rows_by_representation: Mapping[Representation, Mapping[str, tuple[RankRow, ...]]]
    visible_pairs: Mapping[tuple[str, str], tuple[SourceVisibleChoice, SourceVisibleChoice]]
    feature_receipt_semantic_sha256s: Mapping[Representation, tuple[str, ...]]
    zero_variance_receipts: Mapping[Representation, Mapping[str, object]]
    query_count: int
    group_reference_count: int
    exact_group_quality_checks: int
    semantic_sha256: str


@dataclass(slots=True)
class FeatureCensusAccumulator:
    """Streaming equivalent of retained receipt hashes and zero-variance census."""

    representation: Representation
    semantic_sha256s: list[str]
    first_values: tuple[Fraction, ...] | None
    varying_indexes: set[int]
    row_count: int

    @classmethod
    def create(cls, representation: Representation) -> "FeatureCensusAccumulator":
        return cls(representation, [], None, set(), 0)

    def observe(self, receipt: FeatureReceipt) -> None:
        if receipt.representation != self.representation:
            raise CatalogError("streamed feature census received another representation")
        self.semantic_sha256s.append(receipt.semantic_sha256)
        if self.first_values is None:
            self.first_values = receipt.values
        else:
            for index, (first, value) in enumerate(
                zip(self.first_values, receipt.values, strict=True)
            ):
                if first != value:
                    self.varying_indexes.add(index)
        self.row_count += 1

    def zero_variance_receipt(self) -> dict[str, object]:
        if self.row_count < 1 or self.first_values is None:
            raise CatalogError("streamed zero-variance census is empty")
        constant = tuple(
            name
            for index, name in enumerate(FEATURE_SCHEMAS[self.representation])
            if index not in self.varying_indexes
        )
        return {
            "representation": self.representation.value,
            "row_count": self.row_count,
            "zero_variance_feature_names": constant,
            "zero_variance_count": len(constant),
            "status": "PASS_RECORDED_NOT_CREDITED_WITH_SELECTOR_LEVERAGE",
        }


@dataclass(slots=True)
class ExactFeatureInterner:
    """Share equal exact values/vectors without changing tuple equality or order."""

    fractions: dict[Fraction, Fraction]
    vectors: dict[tuple[Fraction, ...], tuple[Fraction, ...]]

    @classmethod
    def create(cls) -> "ExactFeatureInterner":
        return cls({}, {})

    def intern(self, values: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        canonical = tuple(
            self.fractions.setdefault(value, value)
            for value in values
        )
        existing = self.vectors.get(canonical)
        if existing is not None:
            return existing
        self.vectors[canonical] = canonical
        return canonical


def _quality_tuple(value: Any) -> tuple[int, int, int, int]:
    quality = (
        value.direction_mismatch,
        value.input_residual,
        value.endpoint_residual,
        value.checkpoint_residual,
    )
    if any(isinstance(item, bool) or not isinstance(item, int) or item < 0 for item in quality):
        raise CatalogError("intrinsic target is not a nonnegative exact four-integer quality")
    return quality


def _visible_order(value: SourceVisibleChoice) -> tuple[object, ...]:
    return (
        value.left_shell,
        value.right_shell,
        value.left_direction,
        value.right_direction,
        value.route_domain,
        value.physical_relation_domain,
    )


def _representative_record(group: Q3Group):
    return min(group.records, key=lambda row: _visible_order(row.visible))


def _query_token(group: Q3Group, receipt_index: int) -> str:
    # Tokens are custody metadata only.  They are never passed to a feature
    # constructor or appended to a mathematical representation.
    return f"Q3Q:{group.q3_group_id}:{receipt_index:04d}"


def _bundle_semantic_body(
    *,
    split: str,
    rows: Mapping[Representation, Mapping[str, tuple[RankRow, ...]]],
    complete: Mapping[Representation, Mapping[str, tuple[RankRow, ...]]],
    feature_hashes: Mapping[Representation, tuple[str, ...]],
    zero_variance: Mapping[Representation, Mapping[str, object]],
    query_count: int,
    group_reference_count: int,
    exact_group_quality_checks: int,
) -> dict[str, object]:
    return {
        "schema": "SLCV33_RZ_Q3_EXACT_CATALOG_BUNDLE_V1",
        "split": split,
        "rows_by_representation": {key.value: value for key, value in rows.items()},
        "complete_rows_by_representation": {key.value: value for key, value in complete.items()},
        "feature_receipt_semantic_sha256s": {
            key.value: value for key, value in feature_hashes.items()
        },
        "zero_variance_receipts": {key.value: value for key, value in zero_variance.items()},
        "query_count": query_count,
        "group_reference_count": group_reference_count,
        "exact_group_quality_checks": exact_group_quality_checks,
    }


def build_q3_catalog_bundle(
    inventory: Q3Inventory,
    split: str,
    *,
    binding_path: str | Path = DEFAULT_BINDING_PATH,
    control_winner_lock: Mapping[str, Any] | None = None,
    foundation: BoundV6Foundation | None = None,
) -> Q3CatalogBundle:
    """Build a complete split catalog only after the sealed ICF1/V6 gate.

    The gate runs before the hidden target ledger is opened.  CONTROL remains
    additionally locked until a sealed HOLDOUT winner receipt is supplied.
    """

    if split not in SPLITS:
        raise CatalogError(f"unknown Q3 catalog split: {split}")
    binding = require_sealed_icf1_binding(binding_path)
    if foundation is None:
        with BoundV6Foundation(binding) as bound:
            return build_q3_catalog_bundle(
                inventory,
                split,
                binding_path=binding_path,
                control_winner_lock=control_winner_lock,
                foundation=bound,
            )
    if foundation.binding.snapshot_sha256 != binding.snapshot_sha256:
        raise CatalogError("catalog foundation differs from the sealed binding")
    groups = inventory.groups_for_split(split)
    expected_per_axis = 80 if split == "TRAIN" else 24
    if any(sum(group.axis == axis for group in groups) != expected_per_axis for axis in range(4)):
        raise CatalogError(f"{split} physical-group axis roster differs")

    target_by_index = load_target_choices(
        inventory,
        splits=(split,),
        control_winner_lock=control_winner_lock,
    )
    expected_targets = sum(group.multiplicity for group in groups)
    if len(target_by_index) != expected_targets:
        raise CatalogError(f"{split} target choice count differs")
    if str(Q1_ROOT) not in sys.path:
        sys.path.insert(0, str(Q1_ROOT))
    from slcv32_rz.source_quality import intrinsic_quality  # noqa: PLC0415

    complete_mutable: dict[Representation, dict[str, tuple[RankRow, ...]]] = {
        representation: {} for representation in Representation
    }
    selected_mutable: dict[Representation, dict[str, tuple[RankRow, ...]]] = {
        representation: {} for representation in Representation
    }
    feature_censuses = {
        representation: FeatureCensusAccumulator.create(representation)
        for representation in Representation
    }
    feature_interner = ExactFeatureInterner.create()
    visible_pairs: dict[
        tuple[str, str], tuple[SourceVisibleChoice, SourceVisibleChoice]
    ] = {}
    exact_group_quality_checks = 0
    group_reference_count = 0
    query_count = 0

    for query_group in groups:
        candidates = tuple(
            sorted(
                (group for group in groups if group.axis == query_group.axis),
                key=lambda group: group.q3_group_id,
            )
        )
        if len(candidates) != expected_per_axis:
            raise CatalogError("same-axis candidate roster differs")
        for query_record in query_group.canonical_records:
            query_count += 1
            query_token = _query_token(query_group, query_record.receipt_index)
            query_target = target_by_index[query_record.receipt_index]
            raw: list[
                tuple[
                    Q3Group,
                    tuple[int, int, int, int],
                    dict[Representation, FeatureReceipt],
                ]
            ] = []
            for candidate_group in candidates:
                representative_record = _representative_record(candidate_group)
                candidate_target = target_by_index[representative_record.receipt_index]
                quality = _quality_tuple(intrinsic_quality(query_target, candidate_target))
                for candidate_record in candidate_group.records:
                    observed = _quality_tuple(
                        intrinsic_quality(query_target, target_by_index[candidate_record.receipt_index])
                    )
                    if observed != quality:
                        raise CatalogError("one physical group crosses intrinsic target quality")
                    exact_group_quality_checks += 1
                receipts = derive_all_representations(
                    query_record.visible,
                    candidate_group,
                    foundation,
                )
                for representation, receipt in receipts.items():
                    feature_censuses[representation].observe(receipt)
                raw.append((candidate_group, quality, receipts))
                visible_pairs[(query_token, candidate_group.q3_group_id)] = (
                    query_record.visible,
                    representative_record.visible,
                )
                group_reference_count += 1

            qualities = tuple(sorted({quality for _group, quality, _receipts in raw}))
            if len(qualities) < 2:
                raise CatalogError("one Q3 query has fewer than two exact target tiers")
            tier_by_quality = {quality: tier for tier, quality in enumerate(qualities)}
            selected = set(selected_tiers(len(qualities))) if split == "TRAIN" else set(range(len(qualities)))
            for representation in Representation:
                rows = tuple(
                    RankRow(
                        query_token=query_token,
                        group_token=group.q3_group_id,
                        quality=quality,
                        tier=tier_by_quality[quality],
                        multiplicity=group.multiplicity,
                        query_multiplicity=query_group.multiplicity,
                        candidate_multiplicity=group.multiplicity,
                        features=feature_interner.intern(
                            receipts[representation].values
                        ),
                    )
                    for group, quality, receipts in raw
                )
                complete_mutable[representation][query_token] = rows
                selected_rows = tuple(row for row in rows if row.tier in selected)
                if {row.tier for row in selected_rows} != selected:
                    raise CatalogError("selected exact training tiers lost a complete tier")
                selected_mutable[representation][query_token] = selected_rows

    expected_queries = len(groups) * 2
    expected_references = expected_queries * expected_per_axis
    if query_count != expected_queries or group_reference_count != expected_references:
        raise CatalogError("Q3 query or candidate-reference count differs")

    complete = {
        representation: dict(rows) for representation, rows in complete_mutable.items()
    }
    selected_rows = {
        representation: dict(rows) for representation, rows in selected_mutable.items()
    }
    feature_hashes = {
        representation: tuple(census.semantic_sha256s)
        for representation, census in feature_censuses.items()
    }
    zero_variance = {
        representation: census.zero_variance_receipt()
        for representation, census in feature_censuses.items()
    }
    body = _bundle_semantic_body(
        split=split,
        rows=selected_rows,
        complete=complete,
        feature_hashes=feature_hashes,
        zero_variance=zero_variance,
        query_count=query_count,
        group_reference_count=group_reference_count,
        exact_group_quality_checks=exact_group_quality_checks,
    )
    return Q3CatalogBundle(
        split=split,
        rows_by_representation=selected_rows,
        complete_rows_by_representation=complete,
        visible_pairs=visible_pairs,
        feature_receipt_semantic_sha256s=feature_hashes,
        zero_variance_receipts=zero_variance,
        query_count=query_count,
        group_reference_count=group_reference_count,
        exact_group_quality_checks=exact_group_quality_checks,
        semantic_sha256=canonical_sha256(body),
    )


def evaluate_installed_q2_continuity(bundle: Q3CatalogBundle) -> EvaluationResult:
    """Evaluate the immutable installed Q2 selector on the complete R0 roster."""

    frozen_model = load_q2_current_model()

    def scorer(row: RankRow) -> tuple:
        pair = bundle.visible_pairs.get((row.query_token, row.group_token))
        if pair is None:
            raise CatalogError("Q2 continuity pair is absent from source-visible custody")
        return score_q2_current(pair[0], pair[1], model=frozen_model)

    return evaluate_complete_catalog(
        bundle.complete_rows_by_representation[Representation.R0],
        selector_id="Q2_CURRENT_FIXED",
        scorer=scorer,
    )
