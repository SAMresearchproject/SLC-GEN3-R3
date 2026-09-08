"""Exact bounded Q2 full-ranking engine.

Q2 is a new successor directory.  It treats frozen Q1 as an immutable source
dependency and never writes inside Q1.  All learned features are reconstructed
from source-visible event fields; the hidden inverse input, returned endpoint,
and checkpoint lanes are used only by the inherited exact target oracle.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, replace
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping, Sequence


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
Q1_ROOT = (
    REPOSITORY_ROOT
    / "SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q1"
)
CURRENT_POINTER = REPOSITORY_ROOT / "SLC/18_SAM_NATIVE_QC/CURRENT_SLC_REVISION.json"
Q2_NAMESPACE = "SLCV32_RZ_Q2_FULL_RANKING_GROUP_V1"
QUADRATIC_CLIP_MAX = 16_777_215

if str(Q1_ROOT) not in sys.path:
    sys.path.insert(0, str(Q1_ROOT))

from slcv32_rz.canonical import canonical_sha256 as q1_canonical_sha256  # noqa: E402
from slcv32_rz.selectors import (  # noqa: E402
    ExactSelectorModel as Q1SelectorModel,
    learned_score as q1_learned_score,
)
from slcv32_rz.source_quality import (  # noqa: E402
    ReceiptChoice,
    canonical_queries,
    intrinsic_quality,
    load_receipt_choices,
    visible_features as q1_visible_features,
)


class Q2Error(RuntimeError):
    """A frozen Q2 contract, source, model, or evaluation is invalid."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def fraction_dict(value: Fraction) -> dict[str, str]:
    return {"denominator": str(value.denominator), "numerator": str(value.numerator)}


def fraction_from_dict(value: Mapping[str, Any]) -> Fraction:
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("semantic_sha256", None)
    body["semantic_sha256"] = canonical_sha256(body)
    return body


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def _config(name: str, schema: str) -> dict[str, Any]:
    path = CANDIDATE_ROOT / "config" / name
    value = read_json(path)
    if value.get("schema") != schema or value.get("status") != "FROZEN_BEFORE_Q2_EXECUTION":
        raise Q2Error(f"Q2 frozen contract is invalid: {name}")
    return value


def load_contracts() -> dict[str, dict[str, Any]]:
    return {
        "campaign": _config("Q2_CAMPAIGN_CONTRACT.json", "SLCV32_RZ_Q2_CAMPAIGN_CONTRACT_V1"),
        "features": _config("FEATURE_MAP_CONTRACT.json", "SLCV32_RZ_Q2_FEATURE_MAP_CONTRACT_V1"),
        "catalog": _config("GROUPED_CATALOG_CONTRACT.json", "SLCV32_RZ_Q2_GROUPED_CATALOG_CONTRACT_V1"),
        "budget": _config("SELECTOR_BUDGET_CONTRACT.json", "SLCV32_RZ_Q2_SELECTOR_BUDGET_CONTRACT_V1"),
        "preservation": _config("PRESERVATION_CONTRACT.json", "SLCV32_RZ_Q2_PRESERVATION_CONTRACT_V1"),
    }


def tree_receipt(root: Path) -> dict[str, Any]:
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rows.append(
            {
                "bytes": path.stat().st_size,
                "path": path.relative_to(root).as_posix(),
                "sha256": file_sha256(path),
            }
        )
    return seal({"file_count": len(rows), "files": rows, "root": root.relative_to(REPOSITORY_ROOT).as_posix()})


def preservation_receipt(contracts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    frozen = contracts["preservation"]
    observed = {
        "current_pointer_file_sha256": file_sha256(CURRENT_POINTER),
        "q1_final_freeze_file_sha256": file_sha256(Q1_ROOT / "release/FINAL_FREEZE_RECEIPT.json"),
        "q1_release_manifest_file_sha256": file_sha256(Q1_ROOT / "release/RELEASE_MANIFEST.json"),
        "q1_selector_comparison_file_sha256": file_sha256(
            Q1_ROOT / "release/execution/SELECTOR_COMPARISON_PRIMARY.json"
        ),
    }
    for key, value in observed.items():
        if value != frozen[key]:
            raise Q2Error(f"frozen Q1/pointer preservation pin differs: {key}")
    pointer = read_json(CURRENT_POINTER)
    if pointer.get("current_revision_name") != "SLCV21R":
        raise Q2Error("current SLC pointer differs from SLCV21R")
    return seal(
        {
            "current_pointer": "SLCV21R",
            "observed": observed,
            "q1_tree": tree_receipt(Q1_ROOT),
            "schema": "SLCV32_RZ_Q2_PREDECESSOR_PRESERVATION_RECEIPT_V1",
            "status": "PASS_Q1_AND_POINTER_IMMUTABLE",
        }
    )


def _strict_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise Q2Error(f"{label} must be an exact integer")
    return value


def signed_centered_delta(left: int, right: int, modulus: int = 256) -> int:
    left = _strict_int(left, "left delta input")
    right = _strict_int(right, "right delta input")
    residue = (left - right) % modulus
    return residue - modulus if residue > modulus // 2 else residue


def full_v2(value: int) -> int:
    value = abs(_strict_int(value, "v2 input"))
    if value == 0:
        return 8
    return min(8, (value & -value).bit_length() - 1)


FEATURE_ORDER = (
    "bias",
    "axis_0", "axis_1", "axis_2", "axis_3",
    "frozen_modulus_match", "route_domain_match", "physical_relation_domain_match",
    "best_left_signed", "best_right_signed", "other_left_signed", "other_right_signed",
    "best_left_abs", "best_right_abs", "other_left_abs", "other_right_abs",
    "best_left_sq", "best_right_sq", "other_left_sq", "other_right_sq",
    "best_sum_sq", "other_sum_sq", "minimum_sum_sq", "maximum_sum_sq",
    "best_abs_sum", "other_abs_sum", "minimum_abs_sum", "maximum_abs_sum",
    "midpoint_delta", "midpoint_abs", "query_span", "candidate_span_abs",
    "best_span_relation", "best_span_relation_abs", "other_span_relation", "other_span_relation_abs",
    "best_direction_mismatch", "other_direction_mismatch", "minimum_direction_mismatch",
    "best_left_direction_match", "best_right_direction_match",
    "other_left_direction_match", "other_right_direction_match",
    "query_left_parity", "query_right_parity", "candidate_parity_low", "candidate_parity_high",
    "best_parity_match_count", "other_parity_match_count", "unordered_parity_match",
    "best_left_v2", "best_right_v2", "other_left_v2", "other_right_v2",
    "best_span_relation_v2", "other_span_relation_v2",
    "quadratic_best_sum_sq_x_direction", "quadratic_best_abs_x_span_abs",
    "quadratic_midpoint_abs_x_span_abs", "quadratic_best_sum_sq_x_midpoint_abs",
    "quadratic_best_x_other", "quadratic_span_relation", "quadratic_midpoint",
    "quadratic_best_abs", "quadratic_other_abs",
    "quadratic_best_direction", "quadratic_other_direction",
    "quadratic_parity_x_best_abs", "route_x_best_sum_sq", "relation_x_span_abs",
)


def visible_features(query: ReceiptChoice, candidate: ReceiptChoice) -> tuple[int, ...]:
    if query.axis != candidate.axis or query.modulus != candidate.modulus:
        raise Q2Error("Q2 feature rows require same-axis, same-modulus choices")
    def alignment(
        candidate_left: int,
        candidate_right: int,
        direction_left: int,
        direction_right: int,
    ) -> dict[str, Any]:
        signed = (
            signed_centered_delta(query.left_shell, candidate_left),
            signed_centered_delta(query.right_shell, candidate_right),
        )
        absolute = tuple(abs(value) for value in signed)
        squared = tuple(value * value for value in signed)
        direction_matches = (
            int(query.left_direction == direction_left),
            int(query.right_direction == direction_right),
        )
        return {
            "signed": signed,
            "absolute": absolute,
            "squared": squared,
            "sum_sq": sum(squared),
            "abs_sum": sum(absolute),
            "direction_mismatch": 2 - sum(direction_matches),
            "direction_matches": direction_matches,
            "parity_match": int((query.left_shell - candidate_left) % 2 == 0)
            + int((query.right_shell - candidate_right) % 2 == 0),
            "candidate_span": candidate_right - candidate_left,
        }

    alignments = [
        alignment(
            candidate.left_shell,
            candidate.right_shell,
            candidate.left_direction,
            candidate.right_direction,
        ),
        alignment(
            candidate.right_shell,
            candidate.left_shell,
            candidate.right_direction,
            candidate.left_direction,
        ),
    ]
    alignments.sort(
        key=lambda row: (
            row["sum_sq"],
            row["abs_sum"],
            row["direction_mismatch"],
            -row["parity_match"],
            row["signed"],
            row["direction_matches"],
        )
    )
    best, other = alignments
    signed = (*best["signed"], *other["signed"])
    absolute = (*best["absolute"], *other["absolute"])
    squared = (*best["squared"], *other["squared"])
    best_sum_sq, other_sum_sq = best["sum_sq"], other["sum_sq"]
    minimum_sum_sq, maximum_sum_sq = sorted((best_sum_sq, other_sum_sq))
    best_abs_sum, other_abs_sum = best["abs_sum"], other["abs_sum"]
    minimum_abs_sum, maximum_abs_sum = sorted((best_abs_sum, other_abs_sum))
    midpoint_delta = (query.left_shell + query.right_shell) - (
        candidate.left_shell + candidate.right_shell
    )
    query_span = query.right_shell - query.left_shell
    candidate_span_abs = abs(candidate.right_shell - candidate.left_shell)
    best_span_relation = query_span - best["candidate_span"]
    other_span_relation = query_span - other["candidate_span"]
    unordered_parity = int(
        sorted((query.left_shell % 2, query.right_shell % 2))
        == sorted((candidate.left_shell % 2, candidate.right_shell % 2))
    )
    route_match = int(query.route_domain == candidate.route_domain)
    relation_match = int(query.physical_relation_domain == candidate.physical_relation_domain)

    def clip(value: int) -> int:
        return max(-QUADRATIC_CLIP_MAX, min(QUADRATIC_CLIP_MAX, value))

    values = (
        1,
        *(int(query.axis == axis) for axis in range(4)),
        int(query.modulus == 524287), route_match, relation_match,
        *signed, *absolute, *squared,
        best_sum_sq, other_sum_sq, minimum_sum_sq, maximum_sum_sq,
        best_abs_sum, other_abs_sum, minimum_abs_sum, maximum_abs_sum,
        midpoint_delta, abs(midpoint_delta), query_span, candidate_span_abs,
        best_span_relation, abs(best_span_relation), other_span_relation, abs(other_span_relation),
        best["direction_mismatch"], other["direction_mismatch"],
        min(best["direction_mismatch"], other["direction_mismatch"]),
        *best["direction_matches"], *other["direction_matches"],
        query.left_shell % 2, query.right_shell % 2,
        *sorted((candidate.left_shell % 2, candidate.right_shell % 2)),
        best["parity_match"], other["parity_match"], unordered_parity,
        *(full_v2(value) for value in signed),
        full_v2(best_span_relation), full_v2(other_span_relation),
        clip(minimum_sum_sq * min(best["direction_mismatch"], other["direction_mismatch"])),
        clip(minimum_abs_sum * abs(best_span_relation)),
        clip(abs(midpoint_delta) * abs(best_span_relation)),
        clip(best_sum_sq * abs(midpoint_delta)),
        clip(best_sum_sq * other_sum_sq),
        clip(best_span_relation * best_span_relation),
        clip(midpoint_delta * midpoint_delta),
        clip(minimum_abs_sum * minimum_abs_sum),
        clip(other_abs_sum * other_abs_sum),
        clip(best["direction_mismatch"] * best_sum_sq),
        clip(other["direction_mismatch"] * other_sum_sq),
        clip((2 - max(best["parity_match"], other["parity_match"])) * minimum_abs_sum),
        clip(route_match * minimum_sum_sq),
        clip(relation_match * abs(best_span_relation)),
    )
    if len(values) != len(FEATURE_ORDER):
        raise Q2Error(f"Q2 feature width differs: {len(values)} != {len(FEATURE_ORDER)}")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
        raise Q2Error("Q2 feature vector is not exact integer data")
    return values


@dataclass(frozen=True, slots=True)
class CatalogRow:
    query_id: str
    query_receipt_index: int
    axis: int
    split: str
    group_id: str
    representative_receipt_index: int
    multiplicity: int
    quality: tuple[int, int, int, int]
    tier: int
    features: tuple[int, ...]
    q1_features: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CatalogBundle:
    choices: tuple[ReceiptChoice, ...]
    queries: tuple[ReceiptChoice, ...]
    members_by_group: Mapping[str, tuple[ReceiptChoice, ...]]
    rows_by_query: Mapping[str, tuple[CatalogRow, ...]]
    training_rows_by_query: Mapping[str, tuple[CatalogRow, ...]]
    split_manifest: dict[str, Any]
    training_manifest: dict[str, Any]
    evaluation_manifest: dict[str, Any]
    source_receipt: dict[str, Any]


def _new_group_id(choice: ReceiptChoice) -> str:
    return canonical_sha256(
        {
            "axis": choice.axis,
            "endpoint_max": max(choice.left_shell, choice.right_shell),
            "endpoint_min": min(choice.left_shell, choice.right_shell),
            "modulus": choice.modulus,
            "namespace": Q2_NAMESPACE,
            "physical_relation_domain": choice.physical_relation_domain,
            "route_domain": choice.route_domain,
        }
    )


def _fresh_choices() -> tuple[ReceiptChoice, ...]:
    inherited = load_receipt_choices()
    group_axis: dict[str, int] = {}
    provisional = []
    for choice in inherited:
        group_id = _new_group_id(choice)
        previous = group_axis.setdefault(group_id, choice.axis)
        if previous != choice.axis:
            raise Q2Error("fresh Q2 group identity collision")
        provisional.append((choice, group_id))
    if len(group_axis) != 512:
        raise Q2Error("fresh Q2 namespace does not contain 512 groups")
    split_by_group: dict[str, str] = {}
    for axis in range(4):
        groups = sorted(group for group, value in group_axis.items() if value == axis)
        if len(groups) != 128:
            raise Q2Error("fresh Q2 split requires 128 groups per axis")
        for ordinal, group_id in enumerate(groups):
            split_by_group[group_id] = "TRAIN" if ordinal < 80 else "HOLDOUT" if ordinal < 104 else "CONTROL"
    return tuple(
        replace(choice, group_sha256=group_id, split=split_by_group[group_id])
        for choice, group_id in provisional
    )


def _selected_tiers(tier_count: int) -> tuple[int, ...]:
    if tier_count < 2:
        raise Q2Error("Q2 training catalog has fewer than two target tiers")
    selected = set(range(min(6, tier_count)))
    for quantile in range(1, 8):
        center = (quantile * (tier_count - 1)) // 8
        for delta in (-1, 0, 1):
            selected.add(max(0, min(tier_count - 1, center + delta)))
    selected.update(range(max(0, tier_count - 2), tier_count))
    return tuple(sorted(selected))


def build_catalogs() -> CatalogBundle:
    choices = _fresh_choices()
    queries = canonical_queries(choices)
    choice_by_index = {choice.receipt_index: choice for choice in choices}
    grouped: dict[str, list[ReceiptChoice]] = defaultdict(list)
    for choice in choices:
        grouped[choice.group_sha256].append(choice)
    members_by_group = {
        group: tuple(sorted(members, key=lambda item: item.receipt_index))
        for group, members in grouped.items()
    }
    multiplicities = {len(members) for members in members_by_group.values()}
    canonical_counts = {
        sum(member.sample_role == "CANONICAL_MODEL_EXAMPLE" for member in members)
        for members in members_by_group.values()
    }
    if multiplicities != {4, 10, 16} or canonical_counts != {2}:
        raise Q2Error("Q2 inherited group multiplicity/canonical roster differs")
    split_rows = []
    for group_id, members in sorted(members_by_group.items()):
        if len({member.split for member in members}) != 1 or len({member.axis for member in members}) != 1:
            raise Q2Error("Q2 group crosses split or axis")
        split_rows.append(
            {
                "axis": members[0].axis,
                "group_sha256": group_id,
                "member_receipt_indices": [member.receipt_index for member in members],
                "split": members[0].split,
            }
        )
    split_manifest = seal(
        {
            "counts": {
                split: {
                    str(axis): sum(
                        row["split"] == split and row["axis"] == axis for row in split_rows
                    )
                    for axis in range(4)
                }
                for split in ("TRAIN", "HOLDOUT", "CONTROL")
            },
            "group_rows": split_rows,
            "namespace": Q2_NAMESPACE,
            "q1_split_membership_reused": False,
            "schema": "SLCV32_RZ_Q2_FRESH_GROUP_SPLIT_MANIFEST_V1",
            "status": "FROZEN_DERIVED_BEFORE_MODEL_FIT",
        }
    )
    rows_by_query: dict[str, tuple[CatalogRow, ...]] = {}
    training_rows_by_query: dict[str, tuple[CatalogRow, ...]] = {}
    training_receipts = []
    evaluation_receipts = []
    exact_equality_checks = 0
    for query in queries:
        eligible = [
            (group_id, members)
            for group_id, members in members_by_group.items()
            if members[0].split == query.split and members[0].axis == query.axis
        ]
        raw = []
        for group_id, members in sorted(eligible):
            representative = members[0]
            quality_object = intrinsic_quality(query, representative)
            quality = (
                quality_object.direction_mismatch,
                quality_object.input_residual,
                quality_object.endpoint_residual,
                quality_object.checkpoint_residual,
            )
            features = visible_features(query, representative)
            old_features = q1_visible_features(query, representative)
            for member in members[1:]:
                member_quality = intrinsic_quality(query, member)
                observed = (
                    member_quality.direction_mismatch,
                    member_quality.input_residual,
                    member_quality.endpoint_residual,
                    member_quality.checkpoint_residual,
                )
                if observed != quality or visible_features(query, member) != features:
                    raise Q2Error("Q2 exact-equality physical group differs")
                if q1_visible_features(query, member) != old_features:
                    raise Q2Error("Q1 comparator features differ inside Q2 group")
                exact_equality_checks += 1
            raw.append((group_id, representative, quality, features, old_features, len(members)))
        qualities = sorted({row[2] for row in raw})
        tier_by_quality = {quality: ordinal for ordinal, quality in enumerate(qualities)}
        rows = tuple(
            CatalogRow(
                query_id=query.query_id,
                query_receipt_index=query.receipt_index,
                axis=query.axis,
                split=query.split,
                group_id=group_id,
                representative_receipt_index=representative.receipt_index,
                multiplicity=multiplicity,
                quality=quality,
                tier=tier_by_quality[quality],
                features=features,
                q1_features=old_features,
            )
            for group_id, representative, quality, features, old_features, multiplicity in raw
        )
        rows_by_query[query.query_id] = rows
        if query.split == "TRAIN":
            selected = set(_selected_tiers(len(qualities)))
            train_rows = tuple(row for row in rows if row.tier in selected)
            if {row.tier for row in train_rows} != selected:
                raise Q2Error("Q2 harder training tiers lost a complete tier")
            training_rows_by_query[query.query_id] = train_rows
            training_receipts.append(
                {
                    "query_id": query.query_id,
                    "selected_group_ids": [row.group_id for row in train_rows],
                    "selected_tiers": sorted(selected),
                    "target_tier_count": len(qualities),
                }
            )
        else:
            evaluation_receipts.append(
                {
                    "catalog_group_count": len(rows),
                    "catalog_receipt_count": sum(row.multiplicity for row in rows),
                    "query_id": query.query_id,
                    "split": query.split,
                    "target_tier_count": len(qualities),
                }
            )
    source_receipt = seal(
        {
            "choice_count": len(choices),
            "exact_equality_checks": exact_equality_checks,
            "feature_count": len(FEATURE_ORDER),
            "physical_group_count": len(members_by_group),
            "q1_final_freeze_semantic_sha256": read_json(
                Q1_ROOT / "release/FINAL_FREEZE_RECEIPT.json"
            )["semantic_sha256"],
            "query_count": len(queries),
            "schema": "SLCV32_RZ_Q2_SOURCE_ADMISSION_V1",
            "status": "PASS_FRESH_DERIVED_RECEIPTS_SOURCE_BOUND_TO_FROZEN_Q1",
        }
    )
    training_manifest = seal(
        {
            "complete_target_ties_retained": True,
            "query_count": len(training_rows_by_query),
            "query_receipts": training_receipts,
            "schema": "SLCV32_RZ_Q2_HARDER_TRAIN_CATALOG_V1",
            "status": "FROZEN_BEFORE_MODEL_FIT",
            "training_group_references": sum(len(rows) for rows in training_rows_by_query.values()),
            "training_receipt_exposures": sum(
                row.multiplicity for rows in training_rows_by_query.values() for row in rows
            ),
        }
    )
    evaluation_manifest = seal(
        {
            "complete_unmined": True,
            "query_receipts": evaluation_receipts,
            "schema": "SLCV32_RZ_Q2_COMPLETE_EVALUATION_CATALOGS_V1",
            "status": "FROZEN_BEFORE_MODEL_FIT_CONTROL_CLOSED",
        }
    )
    if len(choice_by_index) != len(choices):
        raise Q2Error("Q2 source receipt indices are not unique")
    return CatalogBundle(
        choices=choices,
        queries=queries,
        members_by_group=members_by_group,
        rows_by_query=rows_by_query,
        training_rows_by_query=training_rows_by_query,
        split_manifest=split_manifest,
        training_manifest=training_manifest,
        evaluation_manifest=evaluation_manifest,
        source_receipt=source_receipt,
    )


@dataclass(frozen=True, slots=True)
class Observation:
    design: tuple[int, ...]
    target: Fraction
    weight: int


@dataclass(frozen=True, slots=True)
class StatisticsBase:
    objective: str
    gram: tuple[tuple[int, ...], ...]
    rhs: tuple[Fraction, ...]
    observation_count: int
    weighted_observation_count: int


@dataclass(frozen=True, slots=True)
class Q2Model:
    selector_id: str
    architecture: str
    regularization: Fraction
    heads: tuple[tuple[str, tuple[Fraction, ...]], ...]
    statistics_receipts: tuple[dict[str, Any], ...]

    @property
    def parameter_count(self) -> int:
        return sum(len(values) for _, values in self.heads)

    @property
    def semantic_sha256(self) -> str:
        return canonical_sha256(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "architecture": self.architecture,
            "feature_order": list(FEATURE_ORDER),
            "heads": [
                {"head": head, "parameters": [fraction_dict(value) for value in values]}
                for head, values in self.heads
            ],
            "parameter_count": self.parameter_count,
            "regularization": fraction_dict(self.regularization),
            "selector_id": self.selector_id,
            "statistics_receipts": list(self.statistics_receipts),
        }


def _statistics(objective: str, observations: Sequence[Observation]) -> StatisticsBase:
    if not observations:
        raise Q2Error(f"Q2 objective has no observations: {objective}")
    width = len(FEATURE_ORDER)
    gram = [[0] * width for _ in range(width)]
    rhs = [Fraction(0) for _ in range(width)]
    for observation in observations:
        if len(observation.design) != width or observation.weight < 1:
            raise Q2Error("Q2 exact observation is invalid")
        for left, value in enumerate(observation.design):
            weighted = observation.weight * value
            rhs[left] += weighted * observation.target
            for right in range(left, width):
                gram[left][right] += weighted * observation.design[right]
    for left in range(width):
        for right in range(left):
            gram[left][right] = gram[right][left]
    return StatisticsBase(
        objective=objective,
        gram=tuple(tuple(row) for row in gram),
        rhs=tuple(rhs),
        observation_count=len(observations),
        weighted_observation_count=sum(row.weight for row in observations),
    )


def _solve(base: StatisticsBase, regularization: Fraction) -> tuple[Fraction, ...]:
    size = len(base.gram)
    matrix = [
        [Fraction(value) + (regularization if row == column else 0) for column, value in enumerate(values)]
        + [base.rhs[row]]
        for row, values in enumerate(base.gram)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size) if matrix[row][column]), None)
        if pivot is None:
            raise Q2Error("regularized Q2 exact system is singular")
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        pivot_value = matrix[column][column]
        matrix[column] = [value / pivot_value for value in matrix[column]]
        for row in range(size):
            if row == column:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    value - factor * pivot_row
                    for value, pivot_row in zip(matrix[row], matrix[column], strict=True)
                ]
    solution = tuple(row[-1] for row in matrix)
    # Full reconstruction, including the diagonal ridge term.
    for index, (row, target) in enumerate(zip(base.gram, base.rhs, strict=True)):
        observed = sum((Fraction(value) * parameter for value, parameter in zip(row, solution, strict=True)), Fraction(0))
        observed += regularization * solution[index]
        if observed != target:
            raise Q2Error("Q2 exact ridge solution failed reconstruction")
    return solution


def _listwise_observations(bundle: CatalogBundle) -> list[Observation]:
    observations = []
    for query_id in sorted(bundle.training_rows_by_query):
        rows = bundle.training_rows_by_query[query_id]
        maximum = max(row.tier for row in bundle.rows_by_query[query_id])
        grades = {row.group_id: Fraction(maximum - row.tier) for row in rows}
        total_weight = sum(row.multiplicity for row in rows)
        mean = sum((grades[row.group_id] * row.multiplicity for row in rows), Fraction(0)) / total_weight
        for row in rows:
            observations.append(
                Observation(row.features, grades[row.group_id] - mean, row.multiplicity)
            )
    return observations


def _hybrid_observations(bundle: CatalogBundle, adjacent_weight: int) -> list[Observation]:
    observations = _listwise_observations(bundle)
    for query_id in sorted(bundle.training_rows_by_query):
        rows = bundle.training_rows_by_query[query_id]
        for left, right in combinations(rows, 2):
            if abs(left.tier - right.tier) != 1:
                continue
            better, worse = (left, right) if left.tier < right.tier else (right, left)
            observations.append(
                Observation(
                    tuple(a - b for a, b in zip(better.features, worse.features, strict=True)),
                    Fraction(1),
                    adjacent_weight * better.multiplicity * worse.multiplicity,
                )
            )
    return observations


def _conditional_pair_observations(
    bundle: CatalogBundle, component: int
) -> list[Observation]:
    observations = []
    for query_id in sorted(bundle.training_rows_by_query):
        rows = bundle.training_rows_by_query[query_id]
        prefixes: dict[tuple[int, ...], list[CatalogRow]] = defaultdict(list)
        for row in rows:
            prefixes[row.quality[:component]].append(row)
        for prefix_rows in prefixes.values():
            component_values = sorted({row.quality[component] for row in prefix_rows})
            adjacent = {(left, right) for left, right in zip(component_values, component_values[1:])}
            for left, right in combinations(prefix_rows, 2):
                if left.quality[component] == right.quality[component]:
                    continue
                low, high = sorted((left.quality[component], right.quality[component]))
                if (low, high) not in adjacent:
                    continue
                better, worse = (left, right) if left.quality[component] < right.quality[component] else (right, left)
                observations.append(
                    Observation(
                        tuple(a - b for a, b in zip(better.features, worse.features, strict=True)),
                        Fraction(1),
                        better.multiplicity * worse.multiplicity,
                    )
                )
    return observations


def _stats_receipt(base: StatisticsBase) -> dict[str, Any]:
    return seal(
        {
            "gram_sha256": canonical_sha256([list(row) for row in base.gram]),
            "objective": base.objective,
            "observation_count": base.observation_count,
            "rhs_sha256": canonical_sha256([fraction_dict(value) for value in base.rhs]),
            "weighted_observation_count": base.weighted_observation_count,
        }
    )


def fit_q2_models(bundle: CatalogBundle, contracts: Mapping[str, Mapping[str, Any]]) -> tuple[Q2Model, ...]:
    adjacent_weight = int(contracts["budget"]["adjacent_pair_weight"])
    bases: dict[str, tuple[tuple[str, StatisticsBase], ...]] = {
        "EXPANDED_QUERY_CENTERED_LISTWISE_RIDGE": (
            ("listwise_score", _statistics("EXPANDED_QUERY_CENTERED_LISTWISE", _listwise_observations(bundle))),
        ),
        "HYBRID_LISTWISE_ADJACENT_ORDINAL_RIDGE": (
            ("hybrid_score", _statistics("LISTWISE_PLUS_ADJACENT_STRICT_PAIRS", _hybrid_observations(bundle, adjacent_weight))),
        ),
        "LEXICOGRAPHIC_CONDITIONAL_MULTI_HEAD_RIDGE": tuple(
            (
                head,
                _statistics(
                    f"CONDITIONAL_ADJACENT_{head.upper()}",
                    _conditional_pair_observations(bundle, component),
                ),
            )
            for head, component in (("input_score", 1), ("endpoint_score", 2), ("checkpoint_score", 3))
        ),
    }
    regularizations = [fraction_from_dict(value) for value in contracts["budget"]["regularization_roster"]]
    models = []
    for architecture in contracts["budget"]["q2_architectures"]:
        for regularization in regularizations:
            heads = tuple(
                (head, _solve(base, regularization)) for head, base in bases[architecture]
            )
            selector_id = f"Q2-{architecture}-RIDGE-{regularization.numerator}D{regularization.denominator}"
            models.append(
                Q2Model(
                    selector_id=selector_id,
                    architecture=architecture,
                    regularization=regularization,
                    heads=heads,
                    statistics_receipts=tuple(_stats_receipt(base) for _, base in bases[architecture]),
                )
            )
    return tuple(models)


def q2_score(model: Q2Model, row: CatalogRow) -> tuple[Fraction, ...]:
    return tuple(
        sum((parameter * feature for parameter, feature in zip(parameters, row.features, strict=True)), Fraction(0))
        for _, parameters in model.heads
    )


def load_q1_winner() -> Q1SelectorModel:
    comparison = read_json(Q1_ROOT / "release/execution/SELECTOR_COMPARISON_PRIMARY.json")
    if comparison.get("semantic_sha256") != "534610abb78e0b229f29988214bc5546d23a8654854f1aa1cfb6cda220721d85":
        raise Q2Error("frozen Q1 selector comparison semantic identity differs")
    selected = next(
        row for row in comparison["selectors"]
        if row["selector_id"] == "Q1-LISTWISE-QUERY-CENTERED-BORDA-RIDGE"
    )
    return Q1SelectorModel.from_dict(selected["model"])


def _harmonic_gain(rows: Sequence[CatalogRow], scores: Mapping[str, tuple[Any, ...]]) -> Fraction:
    tier_count = 1 + max(row.tier for row in rows)
    ordered_scores = sorted({scores[row.group_id] for row in rows}, reverse=True)
    offset = 0
    total = Fraction(0)
    for score in ordered_scores:
        block = [row for row in rows if scores[row.group_id] == score]
        width = sum(row.multiplicity for row in block)
        mean_discount = sum((Fraction(1, rank) for rank in range(offset + 1, offset + width + 1)), Fraction(0)) / width
        total += sum(row.multiplicity * (tier_count - row.tier) * mean_discount for row in block)
        offset += width
    return total


def evaluate(
    bundle: CatalogBundle,
    *,
    split: str,
    selector_id: str,
    selector_kind: str,
    parameter_count: int,
    scorer: Any,
    collision_feature_getter: Any,
) -> dict[str, Any]:
    totals = defaultdict(int)
    harmonic_total = Fraction(0)
    query_receipts = []
    feature_collision_pairs = 0
    strict_pairs = 0
    for query_id in sorted(bundle.rows_by_query):
        rows = bundle.rows_by_query[query_id]
        if rows[0].split != split:
            continue
        scores = {row.group_id: scorer(row) for row in rows}
        best_score = max(scores.values())
        proposed = [row for row in rows if scores[row.group_id] == best_score]
        proposed_qualities = {row.quality for row in proposed}
        selected_quality = next(iter(proposed_qualities)) if len(proposed_qualities) == 1 else None
        selected = [row for row in rows if selected_quality is not None and row.quality == selected_quality]
        best_quality = min(row.quality for row in rows)
        best = [row for row in rows if row.quality == best_quality]
        exact_best = {row.group_id for row in selected} == {row.group_id for row in best}
        status = "ABSTAIN" if selected_quality is None else (
            "AMBIGUOUS_BEST_SET" if sum(row.multiplicity for row in selected) > 1 else "SELECTED_UNIQUE"
        )
        correct = wrong = tied = 0
        for left, right in combinations(rows, 2):
            if left.quality == right.quality:
                continue
            better, worse = (left, right) if left.quality < right.quality else (right, left)
            weight = better.multiplicity * worse.multiplicity
            strict_pairs += weight
            if collision_feature_getter(better) == collision_feature_getter(worse):
                feature_collision_pairs += weight
            if scores[better.group_id] > scores[worse.group_id]:
                correct += weight
            elif scores[better.group_id] < scores[worse.group_id]:
                wrong += weight
            else:
                tied += weight
        actual = _harmonic_gain(rows, scores)
        ideal_scores = {row.group_id: (-row.tier,) for row in rows}
        ideal = _harmonic_gain(rows, ideal_scores)
        harmonic = actual / ideal
        selected_tier = (1 + max(row.tier for row in rows)) if selected_quality is None else next(
            row.tier for row in rows if row.quality == selected_quality
        )
        totals["queries"] += 1
        totals["best"] += int(selected_quality == best_quality)
        totals["exact_best"] += int(exact_best)
        totals["abstained"] += int(status == "ABSTAIN")
        totals["false_singleton"] += int(sum(row.multiplicity for row in best) > 1 and sum(row.multiplicity for row in selected) == 1)
        totals["selected_tier"] += selected_tier
        totals["correct"] += correct
        totals["wrong"] += wrong
        totals["tied"] += tied
        totals["receipt_exposures"] += sum(row.multiplicity for row in rows)
        harmonic_total += harmonic
        query_receipts.append(
            seal(
                {
                    "admission_status": status,
                    "best_target_tier_selected": selected_quality == best_quality,
                    "catalog_group_count": len(rows),
                    "exact_best_set_recovered": exact_best,
                    "harmonic_tier_gain_ratio": fraction_dict(harmonic),
                    "query_id": query_id,
                    "selected_target_tier": selected_tier if selected_quality is not None else None,
                    "strict_pair_correct": correct,
                    "strict_pair_tied": tied,
                    "strict_pair_wrong": wrong,
                }
            )
        )
    queries = totals["queries"]
    strict_total = totals["correct"] + totals["wrong"] + totals["tied"]
    if queries < 1 or strict_total < 1:
        raise Q2Error(f"Q2 evaluation split is empty: {split}")
    result = seal(
        {
            "abstention_rate": fraction_dict(Fraction(totals["abstained"], queries)),
            "best_tier_accuracy": fraction_dict(Fraction(totals["best"], queries)),
            "complete_catalog_receipt_exposures": totals["receipt_exposures"],
            "exact_best_set_recovery": fraction_dict(Fraction(totals["exact_best"], queries)),
            "false_singleton_rate": fraction_dict(Fraction(totals["false_singleton"], queries)),
            "feature_collision_strict_pair_rate": fraction_dict(Fraction(feature_collision_pairs, strict_pairs)),
            "mean_harmonic_tier_gain_ratio": fraction_dict(harmonic_total / queries),
            "mean_selected_target_tier": fraction_dict(Fraction(totals["selected_tier"], queries)),
            "parameter_count": parameter_count,
            "query_count": queries,
            "query_receipt_semantic_sha256s": [row["semantic_sha256"] for row in query_receipts],
            "selector_id": selector_id,
            "selector_kind": selector_kind,
            "split": split,
            "status": "PASS_COMPLETE_CATALOG",
            "strict_pair_accuracy": fraction_dict(Fraction(totals["correct"], strict_total)),
            "strict_pair_counts": {
                "correct": totals["correct"], "tied": totals["tied"],
                "total": strict_total, "wrong": totals["wrong"],
            },
        }
    )
    return result


def _ratio(value: Mapping[str, Any]) -> Fraction:
    return fraction_from_dict(value)


def _winner_key(evaluation: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        _ratio(evaluation["exact_best_set_recovery"]),
        _ratio(evaluation["best_tier_accuracy"]),
        _ratio(evaluation["strict_pair_accuracy"]),
        _ratio(evaluation["mean_harmonic_tier_gain_ratio"]),
        -evaluation["parameter_count"],
        tuple(-ord(character) for character in evaluation["selector_id"]),
    )


def _contract_manifest(contracts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    rows = []
    for name in sorted(path.name for path in (CANDIDATE_ROOT / "config").glob("*.json")):
        path = CANDIDATE_ROOT / "config" / name
        rows.append({"bytes": path.stat().st_size, "path": f"config/{name}", "sha256": file_sha256(path)})
    return seal({"contracts": rows, "schema": "SLCV32_RZ_Q2_FROZEN_CONTRACT_MANIFEST_V1"})


def build_and_evaluate(*, write_artifacts: bool = True) -> dict[str, Any]:
    contracts = load_contracts()
    before = preservation_receipt(contracts)
    bundle = build_catalogs()
    models = fit_q2_models(bundle, contracts)
    q1_model = load_q1_winner()
    holdout = []
    q1_holdout = evaluate(
        bundle,
        split="HOLDOUT",
        selector_id=q1_model.selector_id,
        selector_kind="FROZEN_Q1_LISTWISE_COMPARATOR",
        parameter_count=q1_model.parameter_count,
        scorer=lambda row: q1_learned_score(q1_model, row.q1_features),
        collision_feature_getter=lambda row: row.q1_features,
    )
    holdout.append(q1_holdout)
    model_by_id = {model.selector_id: model for model in models}
    for model in models:
        holdout.append(
            evaluate(
                bundle,
                split="HOLDOUT",
                selector_id=model.selector_id,
                selector_kind=model.architecture,
                parameter_count=model.parameter_count,
                scorer=lambda row, selected=model: q2_score(selected, row),
                collision_feature_getter=lambda row: row.features,
            )
        )
    winner_eval = max(holdout, key=_winner_key)
    winner_id = winner_eval["selector_id"]
    if winner_id == q1_model.selector_id:
        winner_scorer = lambda row: q1_learned_score(q1_model, row.q1_features)
        winner_kind = "FROZEN_Q1_LISTWISE_COMPARATOR"
        winner_parameters = q1_model.parameter_count
    else:
        winner_model = model_by_id[winner_id]
        winner_scorer = lambda row: q2_score(winner_model, row)
        winner_kind = winner_model.architecture
        winner_parameters = winner_model.parameter_count
    q1_control = evaluate(
        bundle,
        split="CONTROL",
        selector_id=q1_model.selector_id,
        selector_kind="FROZEN_Q1_LISTWISE_COMPARATOR",
        parameter_count=q1_model.parameter_count,
        scorer=lambda row: q1_learned_score(q1_model, row.q1_features),
        collision_feature_getter=lambda row: row.q1_features,
    )
    winner_control = evaluate(
        bundle,
        split="CONTROL",
        selector_id=winner_id,
        selector_kind=winner_kind,
        parameter_count=winner_parameters,
        scorer=winner_scorer,
        collision_feature_getter=(
            (lambda row: row.q1_features)
            if winner_id == q1_model.selector_id
            else (lambda row: row.features)
        ),
    )
    holdout_delta = _ratio(winner_eval["strict_pair_accuracy"]) - _ratio(q1_holdout["strict_pair_accuracy"])
    control_delta = _ratio(winner_control["strict_pair_accuracy"]) - _ratio(q1_control["strict_pair_accuracy"])
    required = fraction_from_dict(contracts["campaign"]["material_improvement"]["holdout_strict_pair_delta_minimum"])
    best_preserved = _ratio(winner_eval["exact_best_set_recovery"]) == 1 and _ratio(winner_control["exact_best_set_recovery"]) == 1
    material = winner_id != q1_model.selector_id and holdout_delta >= required and control_delta > 0 and best_preserved
    positive = winner_id != q1_model.selector_id and holdout_delta > 0 and control_delta > 0 and best_preserved
    classification = (
        "The test result suggests strong contact with the concept."
        if material
        else "The test result suggests the concept is possible."
        if positive
        else "The test falsifies the concept."
    )
    after = preservation_receipt(contracts)
    if before["q1_tree"]["semantic_sha256"] != after["q1_tree"]["semantic_sha256"]:
        raise Q2Error("Q1 tree changed during Q2 execution")
    checkpoint_values = [
        ("FROZEN_CONTRACTS", _contract_manifest(contracts)["semantic_sha256"]),
        ("Q1_PRESERVATION", before["semantic_sha256"]),
        ("FRESH_GROUP_SPLIT", bundle.split_manifest["semantic_sha256"]),
        ("HARDER_TRAIN_CATALOG", bundle.training_manifest["semantic_sha256"]),
        ("FEATURE_MAP", canonical_sha256(list(FEATURE_ORDER))),
        ("MODEL_ROSTER", canonical_sha256([model.to_dict() for model in models])),
        ("HOLDOUT_WINNER_LOCK", winner_eval["semantic_sha256"]),
        ("POSTSELECTION_CONTROL", winner_control["semantic_sha256"]),
    ]
    chain = []
    predecessor = None
    for stage, value in checkpoint_values:
        row = seal({"predecessor_semantic_sha256": predecessor, "stage": stage, "value_semantic_sha256": value})
        chain.append(row)
        predecessor = row["semantic_sha256"]
    result = seal(
        {
            "candidate": "SLCV32-RZ RELATIVE QUALITY ENGINE CANDIDATE Q2",
            "checkpoint_chain": chain,
            "classification": classification,
            "control_comparator": q1_control,
            "control_delta": fraction_dict(control_delta),
            "control_read_after_winner_lock": True,
            "current_pointer": "SLCV21R",
            "current_pointer_changed": False,
            "feature_count": len(FEATURE_ORDER),
            "feature_order": list(FEATURE_ORDER),
            "full_scale_tuning_started": False,
            "holdout_comparisons": holdout,
            "holdout_delta": fraction_dict(holdout_delta),
            "material_improvement": material,
            "models": [seal(model.to_dict()) for model in models],
            "physical_calibration_started": False,
            "promoted": False,
            "q1_byte_identical_after_execution": True,
            "q1_comparator": q1_holdout,
            "schema": "SLCV32_RZ_Q2_QUALITY_ENGINE_RESULT_V1",
            "status": "PASS_MATERIAL_FULL_RANKING_SUCCESSOR" if material else "COMPLETE_BOUNDED_NO_MATERIAL_SUCCESSOR",
            "winner": {
                "control_evaluation_semantic_sha256": winner_control["semantic_sha256"],
                "holdout_evaluation_semantic_sha256": winner_eval["semantic_sha256"],
                "selector_id": winner_id,
                "selector_kind": winner_kind,
            },
            "winner_control": winner_control,
        }
    )
    if write_artifacts:
        pre = CANDIDATE_ROOT / "preexecution"
        release = CANDIDATE_ROOT / "release"
        write_json(pre / "FROZEN_CONTRACT_MANIFEST.json", _contract_manifest(contracts))
        write_json(pre / "SOURCE_ADMISSION.json", bundle.source_receipt)
        write_json(pre / "Q2_GROUP_SPLIT_MANIFEST.json", bundle.split_manifest)
        write_json(pre / "HARDER_TRAIN_CATALOG.json", bundle.training_manifest)
        write_json(pre / "COMPLETE_EVALUATION_CATALOGS.json", bundle.evaluation_manifest)
        write_json(
            pre / "SELECTOR_BUDGET.json",
            seal(
                {
                    "architecture_count": 3,
                    "feature_count": len(FEATURE_ORDER),
                    "fit_count": len(models),
                    "q1_frozen_comparator_count": 1,
                    "regularization_candidate_count": 3,
                    "schema": "SLCV32_RZ_Q2_EXECUTED_SELECTOR_BUDGET_V1",
                    "training_group_references": bundle.training_manifest["training_group_references"],
                    "training_query_count": bundle.training_manifest["query_count"],
                    "training_receipt_exposures": bundle.training_manifest["training_receipt_exposures"],
                }
            ),
        )
        write_json(release / "PREDECESSOR_PRESERVATION.json", after)
        write_json(release / "DEPENDENCY_SOURCE_MANIFEST.json", seal({
            "contracts_semantic_sha256": _contract_manifest(contracts)["semantic_sha256"],
            "q1_final_freeze_file_sha256": contracts["preservation"]["q1_final_freeze_file_sha256"],
            "q1_release_manifest_file_sha256": contracts["preservation"]["q1_release_manifest_file_sha256"],
            "q1_selector_comparison_file_sha256": contracts["preservation"]["q1_selector_comparison_file_sha256"],
            "schema": "SLCV32_RZ_Q2_DEPENDENCY_SOURCE_MANIFEST_V1",
            "source_admission_semantic_sha256": bundle.source_receipt["semantic_sha256"],
        }))
        write_json(release / "QUALITY_ENGINE_RESULT.json", result)
    return result


__all__ = [
    "CANDIDATE_ROOT", "FEATURE_ORDER", "Q2Error", "build_and_evaluate",
    "build_catalogs", "canonical_sha256", "file_sha256", "fit_q2_models",
    "fraction_from_dict", "load_contracts", "preservation_receipt", "q2_score",
    "read_json", "seal", "tree_receipt", "visible_features", "write_json",
]
