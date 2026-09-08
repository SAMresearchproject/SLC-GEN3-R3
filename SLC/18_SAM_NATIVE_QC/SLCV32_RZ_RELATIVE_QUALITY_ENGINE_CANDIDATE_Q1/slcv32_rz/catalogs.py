"""Leakage-safe frozen catalogs for the SLCV32-RZ Q1 quality engine.

The source loader owns receipt admission, the fresh physical-group namespace,
and the intrinsic target.  This module turns those admitted choices into:

* one reciprocal/replicate-safe physical-group split manifest;
* bounded TRAIN catalogs mined solely by complete target tiers; and
* complete same-axis HOLDOUT and CONTROL catalogs.

Group identifiers are custody, never target tie-breakers.  Selection happens
on :class:`~slcv32_rz.source_quality.QualityVector` values only; group hashes
are used after selection solely to make serialization byte-stable.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .canonical import (
    canonical_bytes,
    canonical_sha256,
    load_exact_json,
    seal_dict,
    verify_seal,
    write_canonical_json,
)
from .source_quality import (
    CANONICAL_ROLE,
    CANDIDATE_ROOT,
    FEATURE_ORDER,
    Q1_GROUP_NAMESPACE,
    SPLITS,
    QualitySourceError,
    QualityVector,
    ReceiptChoice,
    canonical_queries,
    intrinsic_quality,
    load_receipt_choices,
    source_admission_receipt,
    visible_features,
)


DEFAULT_QUALITY_TARGET_CONTRACT = CANDIDATE_ROOT / "config/QUALITY_TARGET_CONTRACT.json"
DEFAULT_GROUPED_CATALOG_CONTRACT = CANDIDATE_ROOT / "config/GROUPED_CATALOG_CONTRACT.json"
QUALITY_TARGET_SCHEMA = "SLCV32_RZ_Q1_QUALITY_TARGET_CONTRACT_V1"
GROUPED_CATALOG_SCHEMA = "SLCV32_RZ_Q1_GROUPED_CATALOG_CONTRACT_V1"
ZERO_QUALITY = QualityVector(0, 0, 0, 0)


class CatalogError(QualitySourceError):
    """A Q1 split, exact-equality group, or frozen catalog is invalid."""


def _load_contract(path: str | Path, schema: str, label: str) -> dict[str, Any]:
    value = load_exact_json(path)
    if not isinstance(value, dict) or value.get("schema") != schema:
        raise CatalogError(f"{label} has the wrong schema")
    if not verify_seal(value):
        raise CatalogError(f"{label} semantic seal is invalid")
    return value


def load_quality_target_contract(
    path: str | Path = DEFAULT_QUALITY_TARGET_CONTRACT,
) -> dict[str, Any]:
    return _load_contract(path, QUALITY_TARGET_SCHEMA, "quality-target contract")


def load_grouped_catalog_contract(
    path: str | Path = DEFAULT_GROUPED_CATALOG_CONTRACT,
) -> dict[str, Any]:
    return _load_contract(path, GROUPED_CATALOG_SCHEMA, "grouped-catalog contract")


def _descriptor(choice: ReceiptChoice) -> dict[str, Any]:
    return {
        "axis": choice.axis,
        "endpoint_max": max(choice.left_shell, choice.right_shell),
        "endpoint_min": min(choice.left_shell, choice.right_shell),
        "modulus": choice.modulus,
        "namespace": Q1_GROUP_NAMESPACE,
        "physical_relation_domain": choice.physical_relation_domain,
        "route_domain": choice.route_domain,
    }


def _orientation_body(choice: ReceiptChoice, *, swap: bool) -> dict[str, Any]:
    """Return every candidate value consumed by target/features in one orientation."""

    lane_order = (1, 0) if swap else (0, 1)
    left_index, right_index = lane_order
    shells = (choice.left_shell, choice.right_shell)
    directions = (choice.left_direction, choice.right_direction)
    return {
        "axis": choice.axis,
        "checkpoint_lanes": [list(choice.checkpoint_lanes[index]) for index in lane_order],
        "endpoint_lanes": [list(choice.endpoint_lanes[index]) for index in lane_order],
        "event_input_lanes": [list(choice.event_input_lanes[index]) for index in lane_order],
        "inverse_directions": [choice.inverse_directions[index] for index in lane_order],
        "inverse_input_lanes": [list(choice.inverse_input_lanes[index]) for index in lane_order],
        "left_direction": directions[left_index],
        "left_shell": shells[left_index],
        "modulus": choice.modulus,
        "physical_relation_domain": choice.physical_relation_domain,
        "right_direction": directions[right_index],
        "right_shell": shells[right_index],
        "route_domain": choice.route_domain,
        "split": choice.split,
    }


def _normalized_function_body(choice: ReceiptChoice) -> dict[str, Any]:
    alternatives = [
        _orientation_body(choice, swap=False),
        _orientation_body(choice, swap=True),
    ]
    alternatives.sort(key=canonical_bytes)
    return {
        "namespace": "SLCV32_RZ_Q1_RECIPROCAL_FUNCTION_INPUT_V1",
        "orientations": alternatives,
    }


def _raw_function_sha256(choice: ReceiptChoice) -> str:
    return canonical_sha256(_orientation_body(choice, swap=False))


def _query_event_custody(query: ReceiptChoice) -> dict[str, Any]:
    return {
        "candidate_id": query.candidate_id,
        "custody": query.custody(),
        "event": query.visible_event(),
        "query_id": query.query_id,
        "sample_role": query.sample_role,
        "split": query.split,
    }


@dataclass(frozen=True, slots=True)
class CatalogGroup:
    """One query-relative physical group with all exact-equal receipts retained."""

    query_id: str
    query_receipt_index: int
    query_group_sha256: str
    query_pair_id: str
    split: str
    axis: int
    group_sha256: str
    representative_receipt_index: int
    features: tuple[int, ...]
    quality: QualityVector
    receipt_indices: tuple[int, ...]
    quality_tier_ordinal: int
    quality_tier_group_count: int
    mining_role: str

    @property
    def multiplicity(self) -> int:
        return len(self.receipt_indices)

    @property
    def target_is_uniquely_ordered(self) -> bool:
        return self.quality_tier_group_count == 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "ambiguity_handling": (
                "UNIQUE_TARGET_TIER"
                if self.target_is_uniquely_ordered
                else "COMPLETE_TARGET_TIE_RETAINED_NO_ID_TIEBREAK"
            ),
            "axis": self.axis,
            "features": list(self.features),
            "group_sha256": self.group_sha256,
            "mining_role": self.mining_role,
            "multiplicity": self.multiplicity,
            "quality": self.quality.to_dict(),
            "quality_tier_group_count": self.quality_tier_group_count,
            "quality_tier_ordinal": self.quality_tier_ordinal,
            "query_group_sha256": self.query_group_sha256,
            "query_id": self.query_id,
            "query_pair_id": self.query_pair_id,
            "query_receipt_index": self.query_receipt_index,
            "receipt_indices": list(self.receipt_indices),
            "representative_receipt_index": self.representative_receipt_index,
            "split": self.split,
        }


@dataclass(frozen=True, slots=True)
class QueryCatalog:
    query: ReceiptChoice
    groups: tuple[CatalogGroup, ...]

    @property
    def selected_training_groups(self) -> tuple[CatalogGroup, ...]:
        return tuple(
            group
            for group in self.groups
            if group.mining_role not in {"TRAIN_COMPLETE_UNMINED", "FULL_CATALOG_EVALUATION"}
        )


@dataclass(frozen=True, slots=True)
class CatalogBundle:
    """In-memory frozen catalog surface consumed by deterministic selectors."""

    choices: tuple[ReceiptChoice, ...]
    queries: tuple[ReceiptChoice, ...]
    catalogs: tuple[QueryCatalog, ...]
    split_manifest: dict[str, Any]
    training_manifest: dict[str, Any]
    full_catalog_manifest: dict[str, Any]
    statistics: dict[str, Any]

    def _catalog(self, query_id: str) -> QueryCatalog:
        for catalog in self.catalogs:
            if catalog.query.query_id == query_id:
                return catalog
        raise CatalogError(f"unknown Q1 query_id: {query_id}")

    def training_rows(self) -> tuple[CatalogGroup, ...]:
        return tuple(
            group
            for catalog in self.catalogs
            if catalog.query.split == "TRAIN"
            for group in catalog.selected_training_groups
        )

    def training_rows_for(self, query_id: str) -> tuple[CatalogGroup, ...]:
        catalog = self._catalog(query_id)
        if catalog.query.split != "TRAIN":
            raise CatalogError("training rows are defined only for TRAIN queries")
        return catalog.selected_training_groups

    def full_catalog_for(
        self, query_id: str, split: str | None = None
    ) -> tuple[CatalogGroup, ...]:
        catalog = self._catalog(query_id)
        if split is not None and catalog.query.split != split:
            raise CatalogError(
                f"query {query_id} belongs to {catalog.query.split}, not {split}"
            )
        return catalog.groups

    def write_manifests(self, directory: str | Path) -> tuple[Path, ...]:
        destination = Path(directory)
        artifacts = (
            ("GROUPED_SPLIT_MANIFEST.json", self.split_manifest),
            ("TRAINING_CATALOG_MANIFEST.json", self.training_manifest),
            ("FULL_EVALUATION_CATALOG_MANIFEST.json", self.full_catalog_manifest),
            ("CATALOG_STATISTICS.json", self.statistics),
        )
        paths = []
        for name, value in artifacts:
            path = destination / name
            write_canonical_json(path, value)
            paths.append(path)
        return tuple(paths)


def _build_physical_groups(
    choices: Sequence[ReceiptChoice],
) -> tuple[dict[str, tuple[ReceiptChoice, ...]], dict[str, str]]:
    grouped: dict[str, list[ReceiptChoice]] = defaultdict(list)
    for choice in choices:
        grouped[choice.group_sha256].append(choice)
    if len(grouped) != 512:
        raise CatalogError(f"Q1 requires 512 physical groups, observed {len(grouped)}")

    function_seals: dict[str, str] = {}
    for group_id, mutable_members in grouped.items():
        members = tuple(sorted(mutable_members, key=lambda item: item.receipt_index))
        descriptors = {_canonical_key(_descriptor(member)) for member in members}
        if len(descriptors) != 1 or canonical_sha256(_descriptor(members[0])) != group_id:
            raise CatalogError("Q1 physical group descriptor or identity differs")
        splits = {member.split for member in members}
        axes = {member.axis for member in members}
        if len(splits) != 1 or len(axes) != 1:
            raise CatalogError("reciprocal/replicate group crosses an axis or split")
        canonical_members = [member for member in members if member.sample_role == CANONICAL_ROLE]
        if len(canonical_members) != 2:
            raise CatalogError("each Q1 physical group requires two reciprocal canonical queries")
        normalized = {
            canonical_sha256(_normalized_function_body(member)) for member in members
        }
        if len(normalized) != 1:
            raise CatalogError("physical group receipts are not exact-equal modulo reciprocity")
        function_seals[group_id] = next(iter(normalized))
        grouped[group_id] = list(members)

    frozen = {group_id: tuple(members) for group_id, members in grouped.items()}
    return frozen, function_seals


def _canonical_key(value: Any) -> bytes:
    return canonical_bytes(value)


def _split_counts(
    groups: Mapping[str, Sequence[ReceiptChoice]], queries: Sequence[ReceiptChoice]
) -> dict[str, Any]:
    group_counts = Counter(members[0].split for members in groups.values())
    query_counts = Counter(query.split for query in queries)
    receipt_counts = Counter(
        choice.split for members in groups.values() for choice in members
    )
    per_axis_group_counts = {
        str(axis): {
            split: sum(
                members[0].axis == axis and members[0].split == split
                for members in groups.values()
            )
            for split in SPLITS
        }
        for axis in range(4)
    }
    expected_per_axis = {
        str(axis): {"CONTROL": 16, "HOLDOUT": 16, "TRAIN": 96}
        for axis in range(4)
    }
    if per_axis_group_counts != expected_per_axis:
        raise CatalogError(f"Q1 per-axis split cardinality differs: {per_axis_group_counts}")
    counts = {
        "canonical_query_counts": {split: query_counts[split] for split in SPLITS},
        "canonical_queries": len(queries),
        "group_counts": {split: group_counts[split] for split in SPLITS},
        "groups": len(groups),
        "per_axis_group_counts": per_axis_group_counts,
        "receipt_counts": {split: receipt_counts[split] for split in SPLITS},
        "receipts": sum(receipt_counts.values()),
    }
    if counts["group_counts"] != {"TRAIN": 384, "HOLDOUT": 64, "CONTROL": 64}:
        raise CatalogError("Q1 global group split must be 384/64/64")
    if counts["canonical_query_counts"] != {
        "TRAIN": 768,
        "HOLDOUT": 128,
        "CONTROL": 128,
    }:
        raise CatalogError("Q1 canonical query split must be 768/128/128")
    return counts


def _quality_tiers(
    rows: Sequence[tuple[str, tuple[ReceiptChoice, ...], tuple[int, ...], QualityVector]]
) -> tuple[QualityVector, ...]:
    return tuple(sorted({row[3] for row in rows}))


def _training_role_by_quality(
    qualities: Sequence[QualityVector], contract: Mapping[str, Any]
) -> dict[QualityVector, str]:
    if not qualities or qualities[0] != ZERO_QUALITY:
        raise CatalogError("each TRAIN query must contain an exact zero-quality group")
    strict = tuple(quality for quality in qualities if quality != ZERO_QUALITY)
    mining = contract["train_mining"]
    nearest_count = mining["nearest_strict_nonzero_target_tiers"]
    if nearest_count != 4 or len(strict) < nearest_count + 4:
        raise CatalogError("TRAIN target tier roster is too small for the frozen miner")
    first_middle = len(strict) // 3
    second_middle = (2 * len(strict)) // 3
    middle_indices = (first_middle, second_middle)
    if len(set(middle_indices)) != 2:
        raise CatalogError("TRAIN middle target tiers are not distinct")

    result = {ZERO_QUALITY: "BEST_COMPLETE_TIER"}
    for ordinal, quality in enumerate(strict[:nearest_count], start=1):
        result[quality] = f"NEAREST_STRICT_NONZERO_COMPLETE_TIER_{ordinal}"
    result[strict[middle_indices[0]]] = "DETERMINISTIC_LOWER_MIDDLE_COMPLETE_TIER"
    result[strict[middle_indices[1]]] = "DETERMINISTIC_UPPER_MIDDLE_COMPLETE_TIER"
    result[strict[-1]] = "FAR_COMPLETE_TIER"
    if len(result) != 8:
        raise CatalogError("frozen TRAIN tier roles overlap")
    return result


def _catalog_for_query(
    query: ReceiptChoice,
    physical_groups: Mapping[str, tuple[ReceiptChoice, ...]],
    grouped_contract: Mapping[str, Any],
) -> tuple[QueryCatalog, int]:
    raw_rows: list[tuple[str, tuple[ReceiptChoice, ...], tuple[int, ...], QualityVector]] = []
    exact_equality_checks = 0
    for group_id, members in physical_groups.items():
        representative = members[0]
        if representative.split != query.split or representative.axis != query.axis:
            continue
        raw_representatives: dict[str, ReceiptChoice] = {}
        for member in members:
            raw_representatives.setdefault(_raw_function_sha256(member), member)
        observed_features = {
            visible_features(query, member) for member in raw_representatives.values()
        }
        observed_quality = {
            intrinsic_quality(query, member) for member in raw_representatives.values()
        }
        exact_equality_checks += len(raw_representatives)
        if len(observed_features) != 1 or len(observed_quality) != 1:
            raise CatalogError(
                "reciprocal/replicate physical group differs in target or features"
            )
        raw_rows.append(
            (
                group_id,
                members,
                next(iter(observed_features)),
                next(iter(observed_quality)),
            )
        )

    expected_groups = 96 if query.split == "TRAIN" else 16
    if len(raw_rows) != expected_groups:
        raise CatalogError(
            f"{query.split} same-axis catalog has {len(raw_rows)} groups; expected {expected_groups}"
        )
    qualities = _quality_tiers(raw_rows)
    tier_ordinal = {quality: ordinal for ordinal, quality in enumerate(qualities)}
    tier_counts = Counter(row[3] for row in raw_rows)
    role_by_quality = (
        _training_role_by_quality(qualities, grouped_contract)
        if query.split == "TRAIN"
        else {}
    )

    groups: list[CatalogGroup] = []
    for group_id, members, features, quality in raw_rows:
        role = (
            role_by_quality.get(quality, "TRAIN_COMPLETE_UNMINED")
            if query.split == "TRAIN"
            else "FULL_CATALOG_EVALUATION"
        )
        groups.append(
            CatalogGroup(
                query_id=query.query_id,
                query_receipt_index=query.receipt_index,
                query_group_sha256=query.group_sha256,
                query_pair_id=query.pair_id,
                split=query.split,
                axis=query.axis,
                group_sha256=group_id,
                representative_receipt_index=members[0].receipt_index,
                features=features,
                quality=quality,
                receipt_indices=tuple(member.receipt_index for member in members),
                quality_tier_ordinal=tier_ordinal[quality],
                quality_tier_group_count=tier_counts[quality],
                mining_role=role,
            )
        )
    groups.sort(key=lambda row: (row.quality, row.group_sha256))
    return QueryCatalog(query=query, groups=tuple(groups)), exact_equality_checks


def _build_split_manifest(
    groups: Mapping[str, tuple[ReceiptChoice, ...]],
    function_seals: Mapping[str, str],
    queries: Sequence[ReceiptChoice],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    group_rows = []
    for group_id in sorted(groups):
        members = groups[group_id]
        canonical_members = [
            member.receipt_index for member in members if member.sample_role == CANONICAL_ROLE
        ]
        group_rows.append(
            {
                "axis": members[0].axis,
                "canonical_query_receipt_indices": canonical_members,
                "descriptor": _descriptor(members[0]),
                "exact_function_input_semantic_sha256": function_seals[group_id],
                "group_sha256": group_id,
                "receipt_count": len(members),
                "receipt_custody": [
                    {
                        "pair_id": member.pair_id,
                        "pair_receipt_semantic_sha256": member.pair_receipt_semantic_sha256,
                        "receipt_index": member.receipt_index,
                        "sample_role": member.sample_role,
                        "source_row_semantic_sha256": member.source_row_semantic_sha256,
                    }
                    for member in members
                ],
                "split": members[0].split,
            }
        )
    document = {
        "contract_semantic_sha256": contract["semantic_sha256"],
        "counts": _split_counts(groups, queries),
        "groups": group_rows,
        "leakage_checks": {
            "all_replicates_share_physical_group_and_split": True,
            "each_group_has_two_reciprocal_canonical_queries": True,
            "no_group_crosses_axis": True,
            "no_group_crosses_split": True,
            "q1_namespace_distinct_from_e1": True,
            "reciprocal_and_replicate_receipts_exact_equal_for_target_and_features": True,
        },
        "schema": "SLCV32_RZ_Q1_GROUPED_SPLIT_MANIFEST_V1",
        "status": "FROZEN_BEFORE_MODEL_EXECUTION",
    }
    return seal_dict(document)


def _query_manifest_row(
    catalog: QueryCatalog, groups: Sequence[CatalogGroup]
) -> dict[str, Any]:
    return {
        "candidate_group_count": len(groups),
        "candidate_receipt_count": sum(group.multiplicity for group in groups),
        "groups": [group.to_dict() for group in groups],
        "query": _query_event_custody(catalog.query),
    }


def _build_training_manifest(
    catalogs: Sequence[QueryCatalog],
    quality_contract: Mapping[str, Any],
    grouped_contract: Mapping[str, Any],
) -> dict[str, Any]:
    train = [catalog for catalog in catalogs if catalog.query.split == "TRAIN"]
    rows = [
        _query_manifest_row(catalog, catalog.selected_training_groups)
        for catalog in train
    ]
    selected = [group for catalog in train for group in catalog.selected_training_groups]
    roles = Counter(group.mining_role for group in selected)
    document = {
        "catalog_contract_semantic_sha256": grouped_contract["semantic_sha256"],
        "counts": {
            "complete_same_axis_groups_examined": sum(len(catalog.groups) for catalog in train),
            "query_count": len(train),
            "selected_group_references": len(selected),
            "selected_receipt_references": sum(group.multiplicity for group in selected),
            "selected_role_group_counts": dict(sorted(roles.items())),
            "target_tied_selected_group_references": sum(
                group.quality_tier_group_count > 1 for group in selected
            ),
        },
        "freeze_boundary": "FROZEN_BEFORE_ANY_SELECTOR_FIT_OR_COMPARISON",
        "queries": rows,
        "quality_target_contract_semantic_sha256": quality_contract["semantic_sha256"],
        "schema": "SLCV32_RZ_Q1_TRAINING_CATALOG_MANIFEST_V1",
        "selection_semantics": {
            "complete_target_ties_retained": True,
            "group_hash_or_identifier_used_as_target_tiebreak": False,
            "middle_target_tier_indices": "FLOOR(N_STRICT/3)_AND_FLOOR(2*N_STRICT/3)",
            "nearest_strict_nonzero_complete_target_tiers": 4,
            "selected_complete_target_tier_count_per_query": 8,
        },
        "status": "FROZEN_BOUNDED_TRAINING_CATALOG",
    }
    return seal_dict(document)


def _build_full_catalog_manifest(
    catalogs: Sequence[QueryCatalog],
    quality_contract: Mapping[str, Any],
    grouped_contract: Mapping[str, Any],
) -> dict[str, Any]:
    evaluation = [
        catalog for catalog in catalogs if catalog.query.split in {"HOLDOUT", "CONTROL"}
    ]
    rows = [_query_manifest_row(catalog, catalog.groups) for catalog in evaluation]
    by_split = Counter(catalog.query.split for catalog in evaluation)
    group_refs = Counter(
        catalog.query.split for catalog in evaluation for _ in catalog.groups
    )
    receipt_refs = Counter(
        catalog.query.split
        for catalog in evaluation
        for group in catalog.groups
        for _ in group.receipt_indices
    )
    document = {
        "catalog_contract_semantic_sha256": grouped_contract["semantic_sha256"],
        "complete_catalog_guards": {
            "all_split_local_same_axis_groups_exposed": True,
            "all_split_local_same_axis_receipts_exposed": True,
            "catalog_mining_or_sampling_applied": False,
            "group_hash_or_identifier_used_as_target_tiebreak": False,
        },
        "counts": {
            "group_references": {split: group_refs[split] for split in ("HOLDOUT", "CONTROL")},
            "query_counts": {split: by_split[split] for split in ("HOLDOUT", "CONTROL")},
            "receipt_references": {split: receipt_refs[split] for split in ("HOLDOUT", "CONTROL")},
        },
        "quality_target_contract_semantic_sha256": quality_contract["semantic_sha256"],
        "queries": rows,
        "schema": "SLCV32_RZ_Q1_FULL_EVALUATION_CATALOG_MANIFEST_V1",
        "splits": ["HOLDOUT", "CONTROL"],
        "status": "FROZEN_COMPLETE_CATALOG_EVALUATION",
    }
    return seal_dict(document)


def _build_statistics(
    choices: Sequence[ReceiptChoice],
    queries: Sequence[ReceiptChoice],
    catalogs: Sequence[QueryCatalog],
    groups: Mapping[str, tuple[ReceiptChoice, ...]],
    exact_equality_checks: int,
    split_manifest: Mapping[str, Any],
    training_manifest: Mapping[str, Any],
    full_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    tier_counts = [len({group.quality for group in catalog.groups}) for catalog in catalogs]
    group_multiplicities = Counter(len(members) for members in groups.values())
    target_tied_catalogs = sum(
        any(group.quality_tier_group_count > 1 for group in catalog.groups)
        for catalog in catalogs
    )
    document = {
        "catalogs": {
            "catalog_count": len(catalogs),
            "complete_evaluation_query_count": sum(
                catalog.query.split in {"HOLDOUT", "CONTROL"} for catalog in catalogs
            ),
            "maximum_quality_tier_count": max(tier_counts),
            "minimum_quality_tier_count": min(tier_counts),
            "target_tied_catalog_count": target_tied_catalogs,
            "train_query_count": sum(catalog.query.split == "TRAIN" for catalog in catalogs),
        },
        "cross_manifest_semantic_sha256": {
            "full_evaluation_catalog": full_manifest["semantic_sha256"],
            "grouped_split": split_manifest["semantic_sha256"],
            "training_catalog": training_manifest["semantic_sha256"],
        },
        "exact_equality_validation": {
            "query_group_orientation_checks": exact_equality_checks,
            "receipt_members_verified": len(choices),
            "target_and_feature_equality_per_physical_group": True,
        },
        "feature_count": len(FEATURE_ORDER),
        "group_receipt_multiplicity_counts": {
            str(key): value for key, value in sorted(group_multiplicities.items())
        },
        "physical_group_count": len(groups),
        "query_count": len(queries),
        "receipt_count": len(choices),
        "schema": "SLCV32_RZ_Q1_CATALOG_STATISTICS_V1",
        "status": "FROZEN_EXACT_CATALOG_STATISTICS",
    }
    return seal_dict(document)


def build_catalog_bundle(
    choices: Sequence[ReceiptChoice] | None = None,
    quality_target_contract_path: str | Path = DEFAULT_QUALITY_TARGET_CONTRACT,
    grouped_catalog_contract_path: str | Path = DEFAULT_GROUPED_CATALOG_CONTRACT,
) -> CatalogBundle:
    """Build and seal the complete Q1 split, TRAIN, HOLDOUT, and CONTROL surface."""

    quality_contract = load_quality_target_contract(quality_target_contract_path)
    grouped_contract = load_grouped_catalog_contract(grouped_catalog_contract_path)
    admitted = tuple(load_receipt_choices() if choices is None else choices)
    if len(admitted) != 5120:
        raise CatalogError("Q1 catalog builder requires all 5,120 admitted receipts")
    queries = canonical_queries(admitted)
    physical_groups, function_seals = _build_physical_groups(admitted)
    split_manifest = _build_split_manifest(
        physical_groups, function_seals, queries, grouped_contract
    )

    catalogs: list[QueryCatalog] = []
    exact_equality_checks = 0
    for query in queries:
        catalog, checks = _catalog_for_query(query, physical_groups, grouped_contract)
        catalogs.append(catalog)
        exact_equality_checks += checks
    frozen_catalogs = tuple(catalogs)
    training_manifest = _build_training_manifest(
        frozen_catalogs, quality_contract, grouped_contract
    )
    full_manifest = _build_full_catalog_manifest(
        frozen_catalogs, quality_contract, grouped_contract
    )
    statistics = _build_statistics(
        admitted,
        queries,
        frozen_catalogs,
        physical_groups,
        exact_equality_checks,
        split_manifest,
        training_manifest,
        full_manifest,
    )
    # Source admission is evaluated here even though its document is emitted by
    # the outer release builder.  This makes catalog construction fail closed on
    # a source-custody mismatch before any model sees a row.
    admission = source_admission_receipt(admitted)
    if admission["group_count"] != split_manifest["counts"]["groups"]:
        raise CatalogError("source admission and split manifest group counts differ")
    return CatalogBundle(
        choices=admitted,
        queries=queries,
        catalogs=frozen_catalogs,
        split_manifest=split_manifest,
        training_manifest=training_manifest,
        full_catalog_manifest=full_manifest,
        statistics=statistics,
    )


__all__ = [
    "CatalogBundle",
    "CatalogError",
    "CatalogGroup",
    "DEFAULT_GROUPED_CATALOG_CONTRACT",
    "DEFAULT_QUALITY_TARGET_CONTRACT",
    "GROUPED_CATALOG_SCHEMA",
    "QUALITY_TARGET_SCHEMA",
    "QueryCatalog",
    "build_catalog_bundle",
    "load_grouped_catalog_contract",
    "load_quality_target_contract",
]
