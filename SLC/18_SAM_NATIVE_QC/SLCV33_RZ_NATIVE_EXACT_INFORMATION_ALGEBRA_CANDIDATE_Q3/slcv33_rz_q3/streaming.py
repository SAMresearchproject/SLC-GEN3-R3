"""Query-local exact Q3 catalog, training, and evaluation primitives.

The legacy materialized catalog remains available for bounded equivalence
tests.  Primary execution uses this module so its peak retained state is one
query plus compact exact accumulators rather than every feature row.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys
from typing import Any, Iterable, Iterator, Mapping, Sequence

from .binding import DEFAULT_BINDING_PATH, require_sealed_icf1_binding
from .canonical import OrderedSemanticDigest, seal
from .catalogs import (
    CatalogError,
    _quality_tuple,
    _query_token,
    _representative_record,
)
from .features import (
    FEATURE_SCHEMAS,
    REPRESENTATION_WIDTHS,
    FeatureReceipt,
    Representation,
    derive_all_representations,
)
from .foundation import BoundV6Foundation
from .source import (
    Q1_ROOT,
    SPLITS,
    Q3Inventory,
    SourceVisibleChoice,
    load_target_choices,
)
from .training import (
    ADJACENT_WEIGHT,
    RIDGES,
    ExactHybridModel,
    ExactStatisticsAccumulator,
    RankRow,
    selected_tiers,
    solve_exact_ridge,
    statistics_semantic_sha256,
)


STREAMING_CATALOG_SCHEMA = "SLCV33_RZ_Q3_STREAMING_EXACT_CATALOG_RECEIPT_V1"


@dataclass(frozen=True, slots=True)
class QueryCatalog:
    """One query's complete and selected exact rows for requested widths."""

    query_token: str
    complete_rows: Mapping[Representation, tuple[RankRow, ...]]
    selected_rows: Mapping[Representation, tuple[RankRow, ...]]
    feature_receipts: Mapping[Representation, tuple[FeatureReceipt, ...]]
    visible_pairs: tuple[
        tuple[str, SourceVisibleChoice, SourceVisibleChoice], ...
    ]
    exact_group_quality_checks: int


@dataclass(slots=True)
class CompactFeatureCensus:
    """Constant-memory feature-roster digest and zero-variance census."""

    representation: Representation
    receipt_digest: OrderedSemanticDigest
    value_digest: OrderedSemanticDigest
    first_values: tuple[Fraction, ...] | None
    varying_indexes: set[int]
    row_count: int

    @classmethod
    def create(cls, representation: Representation) -> "CompactFeatureCensus":
        return cls(
            representation,
            OrderedSemanticDigest.create(),
            OrderedSemanticDigest.create(),
            None,
            set(),
            0,
        )

    def observe(self, receipt: FeatureReceipt) -> None:
        if receipt.representation != self.representation:
            raise CatalogError("compact feature census received another representation")
        self.receipt_digest.observe_semantic_sha256(receipt.semantic_sha256)
        self.value_digest.observe(receipt.values)
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
            raise CatalogError("compact zero-variance census is empty")
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

    def receipt(self) -> dict[str, object]:
        return {
            "representation": self.representation.value,
            "width": REPRESENTATION_WIDTHS[self.representation],
            "feature_receipt_ordered_digest": self.receipt_digest.receipt(),
            "feature_values_ordered_digest": self.value_digest.receipt(),
            "zero_variance_receipt": self.zero_variance_receipt(),
        }


@dataclass(slots=True)
class StreamingCatalogAccumulator:
    """Compact split receipt assembled as query-local rows are consumed."""

    split: str
    representations: tuple[Representation, ...]
    complete_digests: dict[Representation, OrderedSemanticDigest]
    selected_digests: dict[Representation, OrderedSemanticDigest]
    feature_censuses: dict[Representation, CompactFeatureCensus]
    visible_pair_digest: OrderedSemanticDigest
    query_digest: OrderedSemanticDigest
    query_count: int = 0
    group_reference_count: int = 0
    exact_group_quality_checks: int = 0

    @classmethod
    def create(
        cls,
        split: str,
        representations: Iterable[Representation],
    ) -> "StreamingCatalogAccumulator":
        selected = tuple(Representation(value) for value in representations)
        if split not in SPLITS or not selected or len(set(selected)) != len(selected):
            raise CatalogError("streaming catalog accumulator configuration differs")
        return cls(
            split=split,
            representations=selected,
            complete_digests={
                value: OrderedSemanticDigest.create() for value in selected
            },
            selected_digests={
                value: OrderedSemanticDigest.create() for value in selected
            },
            feature_censuses={
                value: CompactFeatureCensus.create(value) for value in selected
            },
            visible_pair_digest=OrderedSemanticDigest.create(),
            query_digest=OrderedSemanticDigest.create(),
        )

    def observe(self, query: QueryCatalog) -> None:
        if set(query.complete_rows) != set(self.representations):
            raise CatalogError("streaming query representation roster differs")
        if set(query.selected_rows) != set(self.representations):
            raise CatalogError("streaming selected-row representation roster differs")
        if set(query.feature_receipts) != set(self.representations):
            raise CatalogError("streaming feature-receipt representation roster differs")
        self.query_digest.observe(query.query_token)
        self.query_count += 1
        reference_count = len(query.visible_pairs)
        self.group_reference_count += reference_count
        self.exact_group_quality_checks += query.exact_group_quality_checks
        for group_token, query_visible, candidate_visible in query.visible_pairs:
            self.visible_pair_digest.observe(
                {
                    "query_token": query.query_token,
                    "group_token": group_token,
                    "query": query_visible.to_dict(),
                    "candidate": candidate_visible.to_dict(),
                }
            )
        for representation in self.representations:
            complete = query.complete_rows[representation]
            selected = query.selected_rows[representation]
            receipts = query.feature_receipts[representation]
            if len(complete) != reference_count or len(receipts) != reference_count:
                raise CatalogError("streaming query row/reference count differs")
            self.complete_digests[representation].observe(
                {"query_token": query.query_token, "rows": complete}
            )
            self.selected_digests[representation].observe(
                {"query_token": query.query_token, "rows": selected}
            )
            for receipt in receipts:
                self.feature_censuses[representation].observe(receipt)

    def representation_receipts(self) -> dict[str, object]:
        return {
            representation.value: {
                **self.feature_censuses[representation].receipt(),
                "complete_query_rows_ordered_digest": self.complete_digests[
                    representation
                ].receipt(),
                "selected_query_rows_ordered_digest": self.selected_digests[
                    representation
                ].receipt(),
            }
            for representation in self.representations
        }

    def finalize(self) -> dict[str, Any]:
        if self.query_count < 1 or self.group_reference_count < 1:
            raise CatalogError("streaming catalog receipt is empty")
        return seal(
            {
                "schema": STREAMING_CATALOG_SCHEMA,
                "status": "PASS_QUERY_LOCAL_EXACT_CATALOG_DIGESTS",
                "split": self.split,
                "query_count": self.query_count,
                "group_reference_count": self.group_reference_count,
                "exact_group_quality_checks": self.exact_group_quality_checks,
                "query_token_ordered_digest": self.query_digest.receipt(),
                "source_visible_pair_ordered_digest": self.visible_pair_digest.receipt(),
                "representations": self.representation_receipts(),
            }
        )


class Q3SplitQuerySource:
    """Binding-gated, split-local query source with one target-ledger read."""

    def __init__(
        self,
        inventory: Q3Inventory,
        split: str,
        *,
        binding_path: str | Path = DEFAULT_BINDING_PATH,
        control_winner_lock: Mapping[str, Any] | None = None,
        foundation: BoundV6Foundation,
    ) -> None:
        if split not in SPLITS:
            raise CatalogError(f"unknown Q3 catalog split: {split}")
        binding = require_sealed_icf1_binding(binding_path)
        if foundation.binding.snapshot_sha256 != binding.snapshot_sha256:
            raise CatalogError("streaming catalog foundation differs from sealed binding")
        self.inventory = inventory
        self.split = split
        self.foundation = foundation
        self.groups = inventory.groups_for_split(split)
        self.expected_per_axis = 80 if split == "TRAIN" else 24
        if any(
            sum(group.axis == axis for group in self.groups) != self.expected_per_axis
            for axis in range(4)
        ):
            raise CatalogError(f"{split} physical-group axis roster differs")
        self.target_by_index = load_target_choices(
            inventory,
            splits=(split,),
            control_winner_lock=control_winner_lock,
        )
        expected_targets = sum(group.multiplicity for group in self.groups)
        if len(self.target_by_index) != expected_targets:
            raise CatalogError(f"{split} target choice count differs")
        if str(Q1_ROOT) not in sys.path:
            sys.path.insert(0, str(Q1_ROOT))
        from slcv32_rz.source_quality import intrinsic_quality  # noqa: PLC0415

        self.intrinsic_quality = intrinsic_quality

    @property
    def expected_query_count(self) -> int:
        return len(self.groups) * 2

    def iter_queries(
        self,
        representations: Sequence[Representation] = tuple(Representation),
        *,
        accumulator: StreamingCatalogAccumulator | None = None,
    ) -> Iterator[QueryCatalog]:
        selected_representations = tuple(
            Representation(value) for value in representations
        )
        if not selected_representations or len(set(selected_representations)) != len(
            selected_representations
        ):
            raise CatalogError("streaming representation request differs")
        if accumulator is not None and (
            accumulator.split != self.split
            or accumulator.representations != selected_representations
        ):
            raise CatalogError("streaming catalog accumulator/source differs")

        query_count = 0
        for query_group in self.groups:
            candidates = tuple(
                sorted(
                    (group for group in self.groups if group.axis == query_group.axis),
                    key=lambda group: group.q3_group_id,
                )
            )
            if len(candidates) != self.expected_per_axis:
                raise CatalogError("same-axis streaming candidate roster differs")
            for query_record in query_group.canonical_records:
                query_count += 1
                query_token = _query_token(query_group, query_record.receipt_index)
                query_target = self.target_by_index[query_record.receipt_index]
                raw: list[
                    tuple[
                        Any,
                        tuple[int, int, int, int],
                        Mapping[Representation, FeatureReceipt],
                        SourceVisibleChoice,
                    ]
                ] = []
                quality_checks = 0
                for candidate_group in candidates:
                    representative_record = _representative_record(candidate_group)
                    candidate_target = self.target_by_index[
                        representative_record.receipt_index
                    ]
                    quality = _quality_tuple(
                        self.intrinsic_quality(query_target, candidate_target)
                    )
                    for candidate_record in candidate_group.records:
                        observed = _quality_tuple(
                            self.intrinsic_quality(
                                query_target,
                                self.target_by_index[candidate_record.receipt_index],
                            )
                        )
                        if observed != quality:
                            raise CatalogError(
                                "one physical group crosses intrinsic target quality"
                            )
                        quality_checks += 1
                    all_receipts = derive_all_representations(
                        query_record.visible,
                        candidate_group,
                        self.foundation,
                    )
                    receipts = {
                        representation: all_receipts[representation]
                        for representation in selected_representations
                    }
                    raw.append(
                        (
                            candidate_group,
                            quality,
                            receipts,
                            representative_record.visible,
                        )
                    )

                qualities = tuple(
                    sorted({quality for _group, quality, _receipts, _visible in raw})
                )
                if len(qualities) < 2:
                    raise CatalogError("one streaming query has fewer than two target tiers")
                tier_by_quality = {
                    quality: tier for tier, quality in enumerate(qualities)
                }
                selected_tier_set = set(
                    selected_tiers(len(qualities))
                    if self.split == "TRAIN"
                    else range(len(qualities))
                )
                complete: dict[Representation, tuple[RankRow, ...]] = {}
                selected: dict[Representation, tuple[RankRow, ...]] = {}
                feature_receipts: dict[
                    Representation, tuple[FeatureReceipt, ...]
                ] = {}
                for representation in selected_representations:
                    rows = tuple(
                        RankRow(
                            query_token=query_token,
                            group_token=group.q3_group_id,
                            quality=quality,
                            tier=tier_by_quality[quality],
                            multiplicity=group.multiplicity,
                            query_multiplicity=query_group.multiplicity,
                            candidate_multiplicity=group.multiplicity,
                            features=receipts[representation].values,
                        )
                        for group, quality, receipts, _visible in raw
                    )
                    selected_rows = tuple(
                        row for row in rows if row.tier in selected_tier_set
                    )
                    if {row.tier for row in selected_rows} != selected_tier_set:
                        raise CatalogError(
                            "streaming selected training tiers lost a complete tier"
                        )
                    complete[representation] = rows
                    selected[representation] = selected_rows
                    feature_receipts[representation] = tuple(
                        receipts[representation]
                        for _group, _quality, receipts, _visible in raw
                    )
                query = QueryCatalog(
                    query_token=query_token,
                    complete_rows=complete,
                    selected_rows=selected,
                    feature_receipts=feature_receipts,
                    visible_pairs=tuple(
                        (
                            group.q3_group_id,
                            query_record.visible,
                            representative_visible,
                        )
                        for group, _quality, _receipts, representative_visible in raw
                    ),
                    exact_group_quality_checks=quality_checks,
                )
                if accumulator is not None:
                    accumulator.observe(query)
                yield query
        if query_count != self.expected_query_count:
            raise CatalogError("streaming query count differs")


def merge_representation_catalog_receipts(
    split: str,
    receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Combine one-representation passes after exact common-roster equality."""

    if len(receipts) != len(Representation):
        raise CatalogError("streaming merge requires five representation passes")
    common_keys = (
        "query_count",
        "group_reference_count",
        "exact_group_quality_checks",
        "query_token_ordered_digest",
        "source_visible_pair_ordered_digest",
    )
    first = receipts[0]
    if first.get("split") != split:
        raise CatalogError("streaming merge split differs")
    representations: dict[str, object] = {}
    for receipt in receipts:
        if receipt.get("split") != split or any(
            receipt.get(key) != first.get(key) for key in common_keys
        ):
            raise CatalogError("streaming representation passes have different common rosters")
        rows = receipt.get("representations")
        if not isinstance(rows, Mapping) or len(rows) != 1:
            raise CatalogError("streaming representation pass is not singular")
        name, row = next(iter(rows.items()))
        if name in representations:
            raise CatalogError("streaming representation pass repeats a width")
        representations[str(name)] = row
    if set(representations) != {value.value for value in Representation}:
        raise CatalogError("streaming merged representation roster differs")
    return seal(
        {
            "schema": STREAMING_CATALOG_SCHEMA,
            "status": "PASS_QUERY_LOCAL_EXACT_CATALOG_DIGESTS",
            "split": split,
            **{key: first[key] for key in common_keys},
            "representations": {
                key: representations[key] for key in sorted(representations)
            },
        }
    )


@dataclass(frozen=True, slots=True)
class StreamingFitResult:
    models: tuple[ExactHybridModel, ...]
    catalog_receipt: Mapping[str, Any]
    statistics_receipts: Mapping[str, Mapping[str, object]]


def fit_q3_budget_streaming(source: Q3SplitQuerySource) -> StreamingFitResult:
    """Fit each width from one query at a time and retain one Gram at a time."""

    if source.split != "TRAIN":
        raise CatalogError("streaming Q3 fit requires the TRAIN source")
    models: list[ExactHybridModel] = []
    catalog_passes: list[Mapping[str, Any]] = []
    statistics_receipts: dict[str, Mapping[str, object]] = {}
    for representation in Representation:
        catalog = StreamingCatalogAccumulator.create("TRAIN", (representation,))
        statistics_accumulator = ExactStatisticsAccumulator.create(
            REPRESENTATION_WIDTHS[representation]
        )
        for query in source.iter_queries((representation,), accumulator=catalog):
            statistics_accumulator.observe_query(
                query.query_token,
                query.selected_rows[representation],
                adjacent_weight=ADJACENT_WEIGHT,
            )
        statistics = statistics_accumulator.finalize()
        statistics_semantic = statistics_semantic_sha256(statistics)
        statistics_receipts[representation.value] = {
            "representation": representation.value,
            "width": REPRESENTATION_WIDTHS[representation],
            "observation_count": statistics.observation_count,
            "weighted_observation_count": statistics.weighted_observation_count,
            "statistics_semantic_sha256": statistics_semantic,
        }
        for ridge in RIDGES:
            parameters = solve_exact_ridge(statistics, ridge)
            models.append(
                ExactHybridModel(
                    representation=representation.value,
                    regularization=ridge,
                    parameters=parameters,
                    adjacent_weight=ADJACENT_WEIGHT,
                    statistics_semantic_sha256=statistics_semantic,
                )
            )
        catalog_passes.append(catalog.finalize())
        del statistics_accumulator
        del statistics
    if len(models) != 15:
        raise CatalogError("streaming exact fit count differs")
    return StreamingFitResult(
        models=tuple(models),
        catalog_receipt=merge_representation_catalog_receipts(
            "TRAIN", catalog_passes
        ),
        statistics_receipts=statistics_receipts,
    )
