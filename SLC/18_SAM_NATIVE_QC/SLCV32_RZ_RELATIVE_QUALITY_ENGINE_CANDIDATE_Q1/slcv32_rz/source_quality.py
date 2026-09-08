"""Source-bound receipt choices and intrinsic relative-quality targets for Q1.

Q1 deliberately separates the learned feature plane from the target oracle.
The feature plane sees only mathematical event descriptors already exposed by
E1.  The target oracle independently reads the frozen W9P execution ledger and
uses returned-W8 endpoint residues plus the two D81 checkpoint residue pairs.
Custody identifiers, hashes, sequence values, target tiers and hidden execution
coordinates never enter a learned feature vector.
"""

from __future__ import annotations

from dataclasses import dataclass
import gzip
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .canonical import canonical_sha256, file_sha256, load_exact_json


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
E1_ROOT = (
    REPOSITORY_ROOT
    / "SLC/18_SAM_NATIVE_QC/SLCV31_RZ_QUALITY_ENGINE_CANDIDATE_E1"
)
E1_SOURCE_INDEX = E1_ROOT / "preexecution/engine_data/SOURCE_INDEX.json"
E1_SPLIT_MANIFEST = E1_ROOT / "preexecution/engine_data/GROUPED_SPLIT_MANIFEST.json"
W9P_LEDGER = (
    REPOSITORY_ROOT
    / "SAM_REVIEW/campaigns/"
    "SLCV21R_FULL_INTERSECTION_STARBREAKER_BINDING_PROGRAM_V1/"
    "phase_b/release/SLCV21R_PHASE_B_D18_W9P_ROUTER_LEDGER.jsonl.gz"
)

EXPECTED_FILE_SHA256 = {
    "e1_source_index": "08f7aaf28a19534e9c9a9baeba521d0d32c7d7d9c2a2a9950ad5c3b12ffee034",
    "e1_split_manifest": "2613e10413a5ef6cc00c4c05a0eefd17d78b859bcffe85e08f854ccc85ba317b",
    "w9p_ledger": "91853c85bf44d3c86a74239176bd22ba42ee6c6d2d54e49cedcc51f3f1dd0add",
}
EXPECTED_SEMANTIC_SHA256 = {
    "e1_source_index": "88f57ad8ad0c8fb456a8327a1c8f49b395ea2333fae7a1280870d4184419edc5",
    "e1_split_manifest": "413586b277c3487b65ab19f6b5f1894eda6a76967d01c01d4c7bf9964b7ed67b",
}

SPLITS = ("TRAIN", "HOLDOUT", "CONTROL")
CANONICAL_ROLE = "CANONICAL_MODEL_EXAMPLE"
REPLICATE_ROLE = "REPLAY_REPLICATE"
Q1_GROUP_NAMESPACE = "SLCV32_RZ_Q1_RELATIVE_QUALITY_GROUP_V1"


class QualitySourceError(RuntimeError):
    """Frozen Q1 target source or target semantics are invalid."""


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise QualitySourceError(f"duplicate historical JSON key: {key}")
        value[key] = item
    return value


def _loads_historical(data: bytes) -> Any:
    """Load a hash-pinned legacy row without admitting timing floats to Q1.

    The frozen W9P ledger contains historical timing numbers.  They are parsed
    as inert strings and never cross into target, feature or receipt values.
    """

    return json.loads(
        data,
        object_pairs_hook=_reject_duplicate_pairs,
        parse_float=str,
        parse_constant=lambda token: (_ for _ in ()).throw(
            QualitySourceError(f"non-finite historical JSON token: {token}")
        ),
    )


def _strict_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise QualitySourceError(f"{label} must be an integer")
    return value


def _pair(value: Any, modulus: int, label: str) -> tuple[int, int]:
    if not isinstance(value, list) or len(value) != 4:
        raise QualitySourceError(f"{label} must be a four-integer state")
    state = tuple(_strict_int(item, f"{label}[{index}]") for index, item in enumerate(value))
    if state[0] != modulus:
        raise QualitySourceError(f"{label} modulus differs from event modulus")
    if not all(0 <= item < modulus for item in state[1:3]):
        raise QualitySourceError(f"{label} residues are outside the source modulus")
    # state[3] is an execution sequence/custody coordinate and is intentionally
    # validated but discarded before target construction.
    return state[1], state[2]


@dataclass(frozen=True, slots=True)
class ReceiptChoice:
    """One exact, source-admitted SLC receipt realization."""

    receipt_index: int
    split: str
    sample_role: str
    group_sha256: str
    pair_id: str
    axis: int
    modulus: int
    left_shell: int
    right_shell: int
    left_direction: int
    right_direction: int
    route_domain: str
    physical_relation_domain: str
    event_input_lanes: tuple[tuple[int, int], tuple[int, int]]
    inverse_input_lanes: tuple[tuple[int, int], tuple[int, int]]
    inverse_directions: tuple[int, int]
    endpoint_lanes: tuple[tuple[int, int], tuple[int, int]]
    checkpoint_lanes: tuple[tuple[int, int], tuple[int, int]]
    source_row_semantic_sha256: str
    pair_receipt_semantic_sha256: str

    @property
    def query_id(self) -> str:
        return f"Q1Q:{self.receipt_index:04d}"

    @property
    def candidate_id(self) -> str:
        return f"Q1R:{self.receipt_index:04d}"

    def visible_event(self) -> dict[str, Any]:
        """Return the exact mathematical fields admitted to feature extraction."""

        return {
            "axis": self.axis,
            "left_direction": self.left_direction,
            "left_shell": self.left_shell,
            "modulus": self.modulus,
            "physical_relation_domain": self.physical_relation_domain,
            "right_direction": self.right_direction,
            "right_shell": self.right_shell,
            "route_domain": self.route_domain,
        }

    def custody(self) -> dict[str, Any]:
        return {
            "group_sha256": self.group_sha256,
            "pair_id": self.pair_id,
            "pair_receipt_semantic_sha256": self.pair_receipt_semantic_sha256,
            "receipt_index": self.receipt_index,
            "source_row_semantic_sha256": self.source_row_semantic_sha256,
        }


@dataclass(frozen=True, order=True, slots=True)
class QualityVector:
    """Lower is better in exact direction/input/endpoint/checkpoint order."""

    direction_mismatch: int
    input_residual: int
    endpoint_residual: int
    checkpoint_residual: int

    def __post_init__(self) -> None:
        if any(
            value < 0
            for value in (
                self.direction_mismatch,
                self.input_residual,
                self.endpoint_residual,
                self.checkpoint_residual,
            )
        ):
            raise QualitySourceError("quality residuals must be nonnegative")

    def to_dict(self) -> dict[str, int]:
        return {
            "checkpoint_residual": self.checkpoint_residual,
            "direction_mismatch": self.direction_mismatch,
            "endpoint_residual": self.endpoint_residual,
            "input_residual": self.input_residual,
        }


def centered_modular_delta(left: int, right: int, modulus: int) -> int:
    """Return the nonnegative centered modular distance in ``Z/modulus``."""

    left = _strict_int(left, "left residue")
    right = _strict_int(right, "right residue")
    modulus = _strict_int(modulus, "modulus")
    if modulus < 3 or not 0 <= left < modulus or not 0 <= right < modulus:
        raise QualitySourceError("centered modular distance input is out of range")
    forward = (left - right) % modulus
    backward = (right - left) % modulus
    return min(forward, backward)


def _lane_residual(
    query_lanes: Sequence[Sequence[int]],
    candidate_lanes: Sequence[Sequence[int]],
    modulus: int,
    *,
    swap: bool,
) -> int:
    candidate_order = (candidate_lanes[1], candidate_lanes[0]) if swap else candidate_lanes
    total = 0
    for query_lane, candidate_lane in zip(query_lanes, candidate_order, strict=True):
        if len(query_lane) != 2 or len(candidate_lane) != 2:
            raise QualitySourceError("relative-quality lanes must contain two residues")
        for query_value, candidate_value in zip(query_lane, candidate_lane, strict=True):
            delta = centered_modular_delta(query_value, candidate_value, modulus)
            total += delta * delta
    return total


def intrinsic_quality(query: ReceiptChoice, candidate: ReceiptChoice) -> QualityVector:
    """Compute the reciprocal-quotiented hidden execution target.

    Identity and whole-lane swap are both evaluated.  The lower exact
    ``(direction mismatch, input residual, endpoint residual, checkpoint
    residual)`` vector is the source target.
    No learned value participates in this calculation.
    """

    if query.modulus != candidate.modulus:
        raise QualitySourceError("relative-quality choices must share a modulus")
    if query.axis != candidate.axis or query.split != candidate.split:
        raise QualitySourceError("relative-quality catalog must be same-axis and split-local")
    choices = []
    for swap in (False, True):
        candidate_directions = (
            (candidate.inverse_directions[1], candidate.inverse_directions[0])
            if swap
            else candidate.inverse_directions
        )
        choices.append(
            QualityVector(
                direction_mismatch=sum(
                    left != right
                    for left, right in zip(
                        (query.left_direction, query.right_direction),
                        candidate_directions,
                        strict=True,
                    )
                ),
                input_residual=_lane_residual(
                    query.event_input_lanes,
                    candidate.inverse_input_lanes,
                    query.modulus,
                    swap=swap,
                ),
                endpoint_residual=_lane_residual(
                    query.endpoint_lanes,
                    candidate.endpoint_lanes,
                    query.modulus,
                    swap=swap,
                ),
                checkpoint_residual=_lane_residual(
                    query.checkpoint_lanes,
                    candidate.checkpoint_lanes,
                    query.modulus,
                    swap=swap,
                ),
            )
        )
    return min(choices)


def visible_features(query: ReceiptChoice, candidate: ReceiptChoice) -> tuple[int, ...]:
    """Return target-blind exact integer features in the frozen Q1 order."""

    if query.modulus != candidate.modulus:
        raise QualitySourceError("feature choices must share a modulus")
    if query.axis != candidate.axis:
        raise QualitySourceError("Q1 catalogs admit only same-axis choices")

    shell_modulus = 256
    direct_left = centered_modular_delta(query.left_shell, candidate.left_shell, shell_modulus)
    direct_right = centered_modular_delta(query.right_shell, candidate.right_shell, shell_modulus)
    swapped_left = centered_modular_delta(query.left_shell, candidate.right_shell, shell_modulus)
    swapped_right = centered_modular_delta(query.right_shell, candidate.left_shell, shell_modulus)
    direct_squared = direct_left * direct_left + direct_right * direct_right
    swapped_squared = swapped_left * swapped_left + swapped_right * swapped_right
    q_delta = query.right_shell - query.left_shell
    c_delta = candidate.right_shell - candidate.left_shell
    direct_direction_mismatch = (
        int(query.left_direction != candidate.left_direction)
        + int(query.right_direction != candidate.right_direction)
    )
    swap_direction_mismatch = (
        int(query.left_direction != candidate.right_direction)
        + int(query.right_direction != candidate.left_direction)
    )
    direct_overlap = int(query.left_shell == candidate.left_shell) + int(
        query.right_shell == candidate.right_shell
    )
    swap_overlap = int(query.left_shell == candidate.right_shell) + int(
        query.right_shell == candidate.left_shell
    )

    def clipped_v2(value: int) -> int:
        if value == 0:
            return 8
        magnitude = abs(value)
        return min(8, (magnitude & -magnitude).bit_length() - 1)

    direct_v2 = sorted((clipped_v2(direct_left), clipped_v2(direct_right)))
    swapped_v2 = sorted((clipped_v2(swapped_left), clipped_v2(swapped_right)))
    best_v2 = max(direct_v2, swapped_v2)
    min_squared = min(direct_squared, swapped_squared)
    max_squared = max(direct_squared, swapped_squared)
    direction_matches = sorted(
        (
            int(query.left_direction == candidate.left_direction),
            int(query.left_direction == candidate.right_direction),
        ),
        reverse=True,
    )
    delta_v2 = sorted(
        (clipped_v2(q_delta - c_delta), clipped_v2(q_delta + c_delta)),
        reverse=True,
    )
    return (
        1,
        *(1 if query.axis == axis else 0 for axis in range(4)),
        min(direct_direction_mismatch, swap_direction_mismatch),
        max(direct_overlap, swap_overlap),
        int(
            sorted((query.left_shell, query.right_shell))
            == sorted((candidate.left_shell, candidate.right_shell))
        ),
        int(min(abs(q_delta - c_delta), abs(q_delta + c_delta)) == 0),
        min(31, abs((query.left_shell + query.right_shell) - (candidate.left_shell + candidate.right_shell)) // 8),
        min(31, abs(abs(q_delta) - abs(c_delta))),
        min(31, min_squared // 64),
        min(63, max_squared // 64),
        best_v2[0],
        best_v2[1],
        delta_v2[0],
        delta_v2[1],
        int(direct_squared == swapped_squared),
        direction_matches[0],
        direction_matches[1],
    )


FEATURE_ORDER = (
    "bias",
    "query_axis_0",
    "query_axis_1",
    "query_axis_2",
    "query_axis_3",
    "reciprocal_direction_mismatch_count",
    "reciprocal_endpoint_overlap_count",
    "unordered_edge_equality",
    "oriented_delta_agreement",
    "midpoint_difference_bin",
    "span_difference_bin",
    "best_shell_residual_bin",
    "other_shell_residual_bin",
    "best_endpoint_v2_low",
    "best_endpoint_v2_high",
    "best_oriented_delta_v2",
    "other_oriented_delta_v2",
    "direct_reciprocal_residual_tie",
    "best_direction_match",
    "other_direction_match",
)


def baseline_score(query: ReceiptChoice, candidate: ReceiptChoice) -> tuple[int, int, int]:
    """Deterministic exact visible-geometry baseline; higher is better."""

    features = visible_features(query, candidate)
    by_name = dict(zip(FEATURE_ORDER, features, strict=True))
    return (
        by_name["unordered_edge_equality"],
        by_name["reciprocal_endpoint_overlap_count"],
        -by_name["reciprocal_direction_mismatch_count"],
        -by_name["best_shell_residual_bin"],
        by_name["oriented_delta_agreement"],
    )


def _extract_choice(
    index_row: Mapping[str, Any],
    ledger_row: Mapping[str, Any],
    *,
    group_sha256: str,
    split: str,
) -> ReceiptChoice:
    event = index_row.get("event")
    provenance = index_row.get("provenance")
    if not isinstance(event, Mapping) or not isinstance(provenance, Mapping):
        raise QualitySourceError("E1 source-index row is missing event/provenance")
    attachment = ledger_row.get("attachment")
    if not isinstance(attachment, Mapping):
        raise QualitySourceError("W9P row is missing attachment")
    parent = attachment.get("parent_d162_receipt")
    if not isinstance(parent, Mapping):
        raise QualitySourceError("W9P row is missing parent D162 receipt")
    left_custody = parent.get("left_custody")
    right_custody = parent.get("right_custody")
    if not isinstance(left_custody, Mapping) or not isinstance(right_custody, Mapping):
        raise QualitySourceError("W9P row is missing two parent input-state lanes")
    theta = attachment.get("theta_completion_report")
    completed = theta.get("completed_w9_pair_receipt") if isinstance(theta, Mapping) else None
    left_delivery = completed.get("left_supported_delivery") if isinstance(completed, Mapping) else None
    right_delivery = completed.get("right_supported_delivery") if isinstance(completed, Mapping) else None
    left = left_delivery.get("W9", {}).get("execution_receipt") if isinstance(left_delivery, Mapping) else None
    right = right_delivery.get("W9", {}).get("execution_receipt") if isinstance(right_delivery, Mapping) else None
    if not isinstance(left, Mapping) or not isinstance(right, Mapping):
        raise QualitySourceError("W9P row is missing two exact W9 execution receipts")

    modulus = _strict_int(event.get("modulus"), "event modulus")
    pair_id = event.get("pair_id")
    if pair_id != ledger_row.get("pair_id") or pair_id != parent.get("pair_id"):
        raise QualitySourceError("source-index/W9P/parent pair identity differs")
    if event.get("legacy_partition") != ledger_row.get("partition"):
        raise QualitySourceError("source-index/W9P legacy partition differs")
    if provenance.get("parent_d162_receipt_semantic_sha256") != parent.get(
        "complete_bridge_receipt_semantic_sha256"
    ):
        raise QualitySourceError("source-index parent receipt hash differs")

    if split not in SPLITS:
        raise QualitySourceError("Q1 source row has an invalid Q1 grouped split")
    if not isinstance(group_sha256, str) or len(group_sha256) != 64:
        raise QualitySourceError("Q1 source row has an invalid group identity")
    replicate_index = _strict_int(event.get("replicate_index"), "replicate index")
    sample_role = CANONICAL_ROLE if replicate_index == 0 else REPLICATE_ROLE
    event_inputs = (
        _pair(left_custody.get("input_state"), modulus, "left parent input state"),
        _pair(right_custody.get("input_state"), modulus, "right parent input state"),
    )
    if event_inputs != (
        (event.get("left_shell"), event.get("right_shell")),
        (event.get("right_shell"), event.get("left_shell")),
    ):
        raise QualitySourceError("parent input-state lanes differ from the frozen event shell")

    inverse_inputs = []
    inverse_directions = []
    checkpoints = []
    endpoints = []
    for label, execution in (("left", left), ("right", right)):
        inverse = execution.get("inverse_readback")
        grouping = execution.get("foundation_grouping_custody")
        w9_state = execution.get("W9_interaction_state")
        if not isinstance(inverse, Mapping) or inverse.get("exact") is not True:
            raise QualitySourceError(f"{label} inverse readback is not exact")
        if not isinstance(grouping, Mapping) or not isinstance(w9_state, Mapping):
            raise QualitySourceError(f"{label} W9 execution custody is incomplete")
        inverse_inputs.append(
            _pair(
                inverse.get("foundation_reconstructed_input"),
                modulus,
                f"{label} inverse input",
            )
        )
        inverse_directions.append(
            _strict_int(inverse.get("signed_direction"), f"{label} inverse direction")
        )
        checkpoints.append(
            _pair(grouping.get("s81_checkpoint"), modulus, f"{label} D81 checkpoint")
        )
        endpoints.append(
            _pair(w9_state.get("foundation_final_state"), modulus, f"{label} returned W8 state")
        )

    return ReceiptChoice(
        receipt_index=_strict_int(index_row.get("pair_catalog_index"), "receipt index"),
        split=split,
        sample_role=sample_role,
        group_sha256=group_sha256,
        pair_id=pair_id,
        axis=_strict_int(event.get("axis"), "event axis"),
        modulus=modulus,
        left_shell=_strict_int(event.get("left_shell"), "left shell"),
        right_shell=_strict_int(event.get("right_shell"), "right shell"),
        left_direction=_strict_int(event.get("left_direction"), "left direction"),
        right_direction=_strict_int(event.get("right_direction"), "right direction"),
        route_domain=event.get("route_domain"),
        physical_relation_domain=event.get("physical_relation_domain"),
        event_input_lanes=event_inputs,
        inverse_input_lanes=(inverse_inputs[0], inverse_inputs[1]),
        inverse_directions=(inverse_directions[0], inverse_directions[1]),
        endpoint_lanes=(endpoints[0], endpoints[1]),
        checkpoint_lanes=(checkpoints[0], checkpoints[1]),
        source_row_semantic_sha256=provenance.get("source_row_semantic_sha256"),
        pair_receipt_semantic_sha256=provenance.get("pair_receipt_semantic_sha256"),
    )


def load_receipt_choices(
    source_index_path: str | Path = E1_SOURCE_INDEX,
    split_manifest_path: str | Path = E1_SPLIT_MANIFEST,
    ledger_path: str | Path = W9P_LEDGER,
) -> tuple[ReceiptChoice, ...]:
    """Verify the frozen source pins and load all 5,120 receipt realizations."""

    source_index_path = Path(source_index_path)
    split_manifest_path = Path(split_manifest_path)
    ledger_path = Path(ledger_path)
    observed_files = {
        "e1_source_index": file_sha256(source_index_path),
        "e1_split_manifest": file_sha256(split_manifest_path),
        "w9p_ledger": file_sha256(ledger_path),
    }
    if observed_files != EXPECTED_FILE_SHA256:
        raise QualitySourceError(
            f"frozen relative-quality source file differs: {observed_files}"
        )
    source_index = load_exact_json(source_index_path)
    split_manifest = load_exact_json(split_manifest_path)
    if source_index.get("semantic_sha256") != EXPECTED_SEMANTIC_SHA256["e1_source_index"]:
        raise QualitySourceError("E1 source-index semantic identity differs")
    if split_manifest.get("semantic_sha256") != EXPECTED_SEMANTIC_SHA256["e1_split_manifest"]:
        raise QualitySourceError("E1 grouped-split semantic identity differs")
    rows = source_index.get("rows")
    if not isinstance(rows, list) or len(rows) != 5120:
        raise QualitySourceError("E1 source index must contain exactly 5,120 rows")

    group_rows: dict[str, tuple[int, dict[str, Any]]] = {}
    row_group_ids: list[str] = []
    for index_row in rows:
        event = index_row.get("event")
        if not isinstance(event, Mapping):
            raise QualitySourceError("source-index row has no event for Q1 grouping")
        group_body = {
            "namespace": Q1_GROUP_NAMESPACE,
            "axis": event.get("axis"),
            "modulus": event.get("modulus"),
            "endpoint_min": min(event.get("left_shell"), event.get("right_shell")),
            "endpoint_max": max(event.get("left_shell"), event.get("right_shell")),
            "route_domain": event.get("route_domain"),
            "physical_relation_domain": event.get("physical_relation_domain"),
        }
        group_id = canonical_sha256(group_body)
        row_group_ids.append(group_id)
        previous = group_rows.setdefault(group_id, (event.get("axis"), group_body))
        if previous != (event.get("axis"), group_body):
            raise QualitySourceError("Q1 group identity collision")
    if len(group_rows) != 512:
        raise QualitySourceError("Q1 grouped split requires 512 physical groups")
    split_by_group: dict[str, str] = {}
    for axis in range(4):
        axis_groups = sorted(group_id for group_id, (value, _) in group_rows.items() if value == axis)
        if len(axis_groups) != 128:
            raise QualitySourceError("Q1 grouped split requires 128 groups per axis")
        for ordinal, group_id in enumerate(axis_groups):
            split_by_group[group_id] = "TRAIN" if ordinal < 96 else "HOLDOUT" if ordinal < 112 else "CONTROL"

    choices: list[ReceiptChoice] = []
    with gzip.open(ledger_path, "rb") as handle:
        for ordinal, (index_row, group_id, raw_line) in enumerate(
            zip(rows, row_group_ids, handle, strict=True)
        ):
            ledger_row = _loads_historical(raw_line)
            choice = _extract_choice(
                index_row,
                ledger_row,
                group_sha256=group_id,
                split=split_by_group[group_id],
            )
            if choice.receipt_index != ordinal:
                raise QualitySourceError("receipt index differs from lockstep ledger ordinal")
            choices.append(choice)
    if len(choices) != 5120:
        raise QualitySourceError("W9P ledger row count differs from 5,120")
    return tuple(choices)


def canonical_queries(choices: Iterable[ReceiptChoice]) -> tuple[ReceiptChoice, ...]:
    queries = tuple(choice for choice in choices if choice.sample_role == CANONICAL_ROLE)
    if len(queries) != 1024:
        raise QualitySourceError("Q1 requires 1,024 canonical directed queries")
    return queries


def full_catalog(
    query: ReceiptChoice, choices: Iterable[ReceiptChoice]
) -> tuple[ReceiptChoice, ...]:
    catalog = tuple(
        choice
        for choice in choices
        if choice.split == query.split and choice.axis == query.axis
    )
    if len(catalog) < 2:
        raise QualitySourceError("relative-quality catalog is not genuinely multiple")
    return tuple(sorted(catalog, key=lambda choice: choice.receipt_index))


def tiered_catalog(
    query: ReceiptChoice, choices: Iterable[ReceiptChoice]
) -> tuple[tuple[QualityVector, tuple[ReceiptChoice, ...]], ...]:
    tiers: dict[QualityVector, list[ReceiptChoice]] = {}
    for candidate in full_catalog(query, choices):
        tiers.setdefault(intrinsic_quality(query, candidate), []).append(candidate)
    return tuple(
        (quality, tuple(sorted(rows, key=lambda choice: choice.receipt_index)))
        for quality, rows in sorted(tiers.items())
    )


def source_admission_receipt(choices: Sequence[ReceiptChoice]) -> dict[str, Any]:
    queries = canonical_queries(choices)
    split_counts = {
        split: sum(choice.split == split for choice in choices) for split in SPLITS
    }
    query_split_counts = {
        split: sum(choice.split == split for choice in queries) for split in SPLITS
    }
    receipt = {
        "schema": "SLCV32_RZ_Q1_SOURCE_ADMISSION_RECEIPT_V1",
        "status": "EXACT_RECEIPT_CHOICES_ADMITTED",
        "choice_count": len(choices),
        "canonical_query_count": len(queries),
        "choice_split_counts": split_counts,
        "query_split_counts": query_split_counts,
        "group_count": len({choice.group_sha256 for choice in choices}),
        "axis_count": len({choice.axis for choice in choices}),
        "target_hidden_fields": [
            "exact_inverse_reconstructed_input_pairs",
            "returned_W8_final_residue_pairs",
            "D81_checkpoint_residue_pairs",
        ],
        "sequence_and_custody_stripped_before_target": True,
        "learned_features_exclude_hidden_target_fields": True,
        "reciprocal_lane_swap_quotient": True,
        "group_namespace": Q1_GROUP_NAMESPACE,
        "e1_split_reused": False,
        "source_files": {
            "e1_source_index_sha256": EXPECTED_FILE_SHA256["e1_source_index"],
            "e1_split_manifest_sha256": EXPECTED_FILE_SHA256["e1_split_manifest"],
            "w9p_ledger_sha256": EXPECTED_FILE_SHA256["w9p_ledger"],
        },
        "choice_custody_semantic_sha256": canonical_sha256(
            [choice.custody() for choice in choices]
        ),
    }
    receipt["semantic_sha256"] = canonical_sha256(receipt)
    return receipt


__all__ = [
    "CANONICAL_ROLE",
    "CANDIDATE_ROOT",
    "E1_SOURCE_INDEX",
    "E1_SPLIT_MANIFEST",
    "FEATURE_ORDER",
    "QualitySourceError",
    "QualityVector",
    "REPOSITORY_ROOT",
    "ReceiptChoice",
    "SPLITS",
    "W9P_LEDGER",
    "baseline_score",
    "canonical_queries",
    "centered_modular_delta",
    "full_catalog",
    "intrinsic_quality",
    "load_receipt_choices",
    "source_admission_receipt",
    "tiered_catalog",
    "visible_features",
]
