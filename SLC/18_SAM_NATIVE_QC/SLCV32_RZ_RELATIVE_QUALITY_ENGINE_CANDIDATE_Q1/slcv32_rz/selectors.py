"""Deterministic exact baseline, pairwise, listwise and multi-head Q1 selectors."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Mapping, Sequence

from .canonical import canonical_sha256, fraction_dict, fraction_from_dict
from .source_quality import FEATURE_ORDER, QualityVector


class SelectorError(RuntimeError):
    """An exact selector contract, objective or model is invalid."""


REGULARIZATION = Fraction(1, 100)
SELECTOR_KINDS = (
    "DETERMINISTIC_EXACT_BASELINE",
    "PAIRWISE_EXACT_RANK_RIDGE",
    "LISTWISE_QUERY_CENTERED_BORDA_RIDGE",
    "MULTI_HEAD_EXACT_RESIDUAL_RIDGE",
)


@dataclass(frozen=True, slots=True)
class TrainingRow:
    query_id: str
    group_id: str
    features: tuple[int, ...]
    quality: QualityVector
    multiplicity: int

    def __post_init__(self) -> None:
        if not self.query_id or not self.group_id:
            raise SelectorError("training rows require query and group identities")
        if len(self.features) != len(FEATURE_ORDER):
            raise SelectorError("training feature width differs from frozen Q1 order")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in self.features):
            raise SelectorError("training features must be exact integers")
        if isinstance(self.multiplicity, bool) or not isinstance(self.multiplicity, int) or self.multiplicity < 1:
            raise SelectorError("training multiplicity must be a positive integer")


@dataclass(frozen=True, slots=True)
class ExactObservation:
    design: tuple[int, ...]
    target: Fraction
    weight: int


@dataclass(frozen=True, slots=True)
class ExactStatistics:
    objective: str
    feature_order: tuple[str, ...]
    gram: tuple[tuple[Fraction, ...], ...]
    rhs_by_head: tuple[tuple[str, tuple[Fraction, ...]], ...]
    observation_count: int
    weighted_observation_count: int
    regularization: Fraction

    @property
    def semantic_sha256(self) -> str:
        return canonical_sha256(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": "SLCV32-RZ-Q1-EXACT-SUFFICIENT-STATISTICS-V1",
            "feature_order": list(self.feature_order),
            "gram": [[fraction_dict(value) for value in row] for row in self.gram],
            "objective": self.objective,
            "observation_count": self.observation_count,
            "regularization": fraction_dict(self.regularization),
            "rhs_by_head": [
                {
                    "head": head,
                    "rhs": [fraction_dict(value) for value in rhs],
                }
                for head, rhs in self.rhs_by_head
            ],
            "weighted_observation_count": self.weighted_observation_count,
        }


@dataclass(frozen=True, slots=True)
class ExactSelectorModel:
    selector_id: str
    selector_kind: str
    feature_order: tuple[str, ...]
    parameters_by_head: tuple[tuple[str, tuple[Fraction, ...]], ...]
    statistics_semantic_sha256: str | None
    training_query_count: int
    training_group_count: int
    training_receipt_exposure_count: int
    regularization: Fraction | None

    def __post_init__(self) -> None:
        if self.selector_kind not in SELECTOR_KINDS:
            raise SelectorError("selector kind is outside the Q1 roster")
        if not self.selector_id:
            raise SelectorError("selector ID must not be empty")
        if self.selector_kind == "DETERMINISTIC_EXACT_BASELINE":
            if self.parameters_by_head or self.statistics_semantic_sha256 is not None:
                raise SelectorError("baseline cannot carry trained parameters")
        elif not self.parameters_by_head or self.regularization is None:
            raise SelectorError("learned selector has no exact parameters")
        for head, values in self.parameters_by_head:
            if not head or len(values) != len(self.feature_order):
                raise SelectorError("selector parameter width is invalid")

    @property
    def parameter_count(self) -> int:
        return sum(len(values) for _, values in self.parameters_by_head)

    @property
    def semantic_sha256(self) -> str:
        return canonical_sha256(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": "SLCV32-RZ-Q1-EXACT-SELECTOR-MODEL-V1",
            "feature_order": list(self.feature_order),
            "parameter_count": self.parameter_count,
            "parameters_by_head": [
                {
                    "head": head,
                    "parameters": [fraction_dict(value) for value in values],
                }
                for head, values in self.parameters_by_head
            ],
            "regularization": (
                fraction_dict(self.regularization)
                if self.regularization is not None
                else None
            ),
            "selector_id": self.selector_id,
            "selector_kind": self.selector_kind,
            "statistics_semantic_sha256": self.statistics_semantic_sha256,
            "training_group_count": self.training_group_count,
            "training_query_count": self.training_query_count,
            "training_receipt_exposure_count": self.training_receipt_exposure_count,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ExactSelectorModel":
        if value.get("contract") != "SLCV32-RZ-Q1-EXACT-SELECTOR-MODEL-V1":
            raise SelectorError("wrong exact selector model contract")
        heads = tuple(
            (
                row["head"],
                tuple(fraction_from_dict(item) for item in row["parameters"]),
            )
            for row in value["parameters_by_head"]
        )
        return cls(
            selector_id=value["selector_id"],
            selector_kind=value["selector_kind"],
            feature_order=tuple(value["feature_order"]),
            parameters_by_head=heads,
            statistics_semantic_sha256=value["statistics_semantic_sha256"],
            training_query_count=value["training_query_count"],
            training_group_count=value["training_group_count"],
            training_receipt_exposure_count=value["training_receipt_exposure_count"],
            regularization=(
                fraction_from_dict(value["regularization"])
                if value["regularization"] is not None
                else None
            ),
        )


def _solve(matrix: Sequence[Sequence[Fraction]], rhs: Sequence[Fraction]) -> tuple[Fraction, ...]:
    size = len(matrix)
    if size == 0 or len(rhs) != size or any(len(row) != size for row in matrix):
        raise SelectorError("exact system must be nonempty and square")
    augmented = [list(row) + [rhs[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column] != 0),
            None,
        )
        if pivot is None:
            raise SelectorError("regularized exact selector system is singular")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(
                        augmented[row], augmented[column], strict=True
                    )
                ]
    solution = tuple(row[-1] for row in augmented)
    for row, target in zip(matrix, rhs, strict=True):
        if sum((a * b for a, b in zip(row, solution, strict=True)), Fraction(0)) != target:
            raise SelectorError("exact selector solution failed reconstruction")
    return solution


def accumulate_statistics(
    *,
    objective: str,
    observations_by_head: Mapping[str, Sequence[ExactObservation]],
    regularization: Fraction = REGULARIZATION,
) -> ExactStatistics:
    if regularization <= 0 or not observations_by_head:
        raise SelectorError("exact selector regularization/heads are invalid")
    heads = sorted(observations_by_head)
    first = tuple(observations_by_head[heads[0]])
    if not first:
        raise SelectorError("exact selector objective has no observations")
    width = len(first[0].design)
    if width != len(FEATURE_ORDER):
        raise SelectorError("objective feature width differs from Q1")
    identities = [
        (row.design, row.weight) for row in first
    ]
    for head in heads[1:]:
        rows = tuple(observations_by_head[head])
        if [(row.design, row.weight) for row in rows] != identities:
            raise SelectorError("multi-head objectives must share rows and weights")

    gram_int = [[0] * width for _ in range(width)]
    for row in first:
        if row.weight < 1 or len(row.design) != width:
            raise SelectorError("objective observation is invalid")
        for left in range(width):
            weighted_left = row.weight * row.design[left]
            for right in range(left, width):
                gram_int[left][right] += weighted_left * row.design[right]
    for left in range(width):
        for right in range(left):
            gram_int[left][right] = gram_int[right][left]
    gram = [[Fraction(value) for value in row] for row in gram_int]
    for index in range(width):
        gram[index][index] += regularization

    rhs_by_head: list[tuple[str, tuple[Fraction, ...]]] = []
    for head in heads:
        rhs = [Fraction(0) for _ in range(width)]
        for row in observations_by_head[head]:
            for index, value in enumerate(row.design):
                rhs[index] += row.weight * value * row.target
        rhs_by_head.append((head, tuple(rhs)))
    return ExactStatistics(
        objective=objective,
        feature_order=FEATURE_ORDER,
        gram=tuple(tuple(row) for row in gram),
        rhs_by_head=tuple(rhs_by_head),
        observation_count=len(first),
        weighted_observation_count=sum(row.weight for row in first),
        regularization=regularization,
    )


def _model_from_statistics(
    *,
    selector_id: str,
    selector_kind: str,
    statistics: ExactStatistics,
    rows: Sequence[TrainingRow],
) -> ExactSelectorModel:
    parameters = tuple(
        (head, _solve(statistics.gram, rhs))
        for head, rhs in statistics.rhs_by_head
    )
    return ExactSelectorModel(
        selector_id=selector_id,
        selector_kind=selector_kind,
        feature_order=FEATURE_ORDER,
        parameters_by_head=parameters,
        statistics_semantic_sha256=statistics.semantic_sha256,
        training_query_count=len({row.query_id for row in rows}),
        training_group_count=len(rows),
        training_receipt_exposure_count=sum(row.multiplicity for row in rows),
        regularization=statistics.regularization,
    )


def baseline_model(rows: Sequence[TrainingRow]) -> ExactSelectorModel:
    return ExactSelectorModel(
        selector_id="Q1-BASELINE-RELATIONAL-LEXICOGRAPHIC",
        selector_kind="DETERMINISTIC_EXACT_BASELINE",
        feature_order=FEATURE_ORDER,
        parameters_by_head=(),
        statistics_semantic_sha256=None,
        training_query_count=len({row.query_id for row in rows}),
        training_group_count=len(rows),
        training_receipt_exposure_count=sum(row.multiplicity for row in rows),
        regularization=None,
    )


def fit_pairwise(rows: Sequence[TrainingRow]) -> tuple[ExactSelectorModel, ExactStatistics]:
    by_query: dict[str, list[TrainingRow]] = {}
    for row in rows:
        by_query.setdefault(row.query_id, []).append(row)
    observations: list[ExactObservation] = []
    for query_id in sorted(by_query):
        ordered = sorted(by_query[query_id], key=lambda row: (row.quality, row.group_id))
        strict = [
            (left, right)
            for left, right in zip(ordered, ordered[1:])
            if left.quality < right.quality
        ]
        for better, worse in strict:
            observations.append(
                ExactObservation(
                    design=tuple(
                        left - right
                        for left, right in zip(
                            better.features, worse.features, strict=True
                        )
                    ),
                    target=Fraction(1),
                    weight=better.multiplicity * worse.multiplicity,
                )
            )
    statistics = accumulate_statistics(
        objective="EXACT_SQUARED_MARGIN_ADJACENT_STRICT_TIER_RANK_RIDGE",
        observations_by_head={"pairwise_score": observations},
    )
    return (
        _model_from_statistics(
            selector_id="Q1-PAIRWISE-EXACT-RANK-RIDGE",
            selector_kind="PAIRWISE_EXACT_RANK_RIDGE",
            statistics=statistics,
            rows=rows,
        ),
        statistics,
    )


def fit_listwise(rows: Sequence[TrainingRow]) -> tuple[ExactSelectorModel, ExactStatistics]:
    by_query: dict[str, list[TrainingRow]] = {}
    for row in rows:
        by_query.setdefault(row.query_id, []).append(row)
    observations: list[ExactObservation] = []
    for query_id in sorted(by_query):
        query_rows = by_query[query_id]
        qualities = sorted({row.quality for row in query_rows})
        grade = {
            quality: Fraction(len(qualities) - 1 - index)
            for index, quality in enumerate(qualities)
        }
        weighted_mean = sum(
            (grade[row.quality] * row.multiplicity for row in query_rows),
            Fraction(0),
        ) / sum(row.multiplicity for row in query_rows)
        for row in sorted(query_rows, key=lambda value: value.group_id):
            observations.append(
                ExactObservation(
                    design=row.features,
                    target=grade[row.quality] - weighted_mean,
                    weight=row.multiplicity,
                )
            )
    statistics = accumulate_statistics(
        objective="EXACT_QUERY_CENTERED_DENSE_TIER_BORDA_RIDGE",
        observations_by_head={"listwise_score": observations},
    )
    return (
        _model_from_statistics(
            selector_id="Q1-LISTWISE-QUERY-CENTERED-BORDA-RIDGE",
            selector_kind="LISTWISE_QUERY_CENTERED_BORDA_RIDGE",
            statistics=statistics,
            rows=rows,
        ),
        statistics,
    )


def fit_multi_head(rows: Sequence[TrainingRow]) -> tuple[ExactSelectorModel, ExactStatistics]:
    head_targets = {
        "direction_head": lambda q: -q.direction_mismatch,
        "input_head": lambda q: -q.input_residual,
        "endpoint_head": lambda q: -q.endpoint_residual,
        "checkpoint_head": lambda q: -q.checkpoint_residual,
    }
    observations_by_head: dict[str, list[ExactObservation]] = {
        head: [] for head in head_targets
    }
    for row in sorted(rows, key=lambda value: (value.query_id, value.group_id)):
        for head, target in head_targets.items():
            observations_by_head[head].append(
                ExactObservation(
                    design=row.features,
                    target=Fraction(target(row.quality)),
                    weight=row.multiplicity,
                )
            )
    statistics = accumulate_statistics(
        objective="EXACT_SHARED_ROWS_FOUR_HEAD_ROUTE_FIDELITY_RIDGE",
        observations_by_head=observations_by_head,
    )
    return (
        _model_from_statistics(
            selector_id="Q1-MULTI-HEAD-EXACT-ROUTE-FIDELITY-RIDGE",
            selector_kind="MULTI_HEAD_EXACT_RESIDUAL_RIDGE",
            statistics=statistics,
            rows=rows,
        ),
        statistics,
    )


def linear_scores(model: ExactSelectorModel, features: Sequence[int]) -> dict[str, Fraction]:
    if len(features) != len(model.feature_order):
        raise SelectorError("selector score feature width differs")
    return {
        head: sum(
            (parameter * value for parameter, value in zip(parameters, features, strict=True)),
            Fraction(0),
        )
        for head, parameters in model.parameters_by_head
    }


def learned_score(model: ExactSelectorModel, features: Sequence[int]) -> tuple[Fraction, ...]:
    scores = linear_scores(model, features)
    if model.selector_kind == "PAIRWISE_EXACT_RANK_RIDGE":
        return (scores["pairwise_score"],)
    if model.selector_kind == "LISTWISE_QUERY_CENTERED_BORDA_RIDGE":
        return (scores["listwise_score"],)
    if model.selector_kind == "MULTI_HEAD_EXACT_RESIDUAL_RIDGE":
        return (
            scores["direction_head"],
            scores["input_head"],
            scores["endpoint_head"],
            scores["checkpoint_head"],
        )
    raise SelectorError("baseline scores require the deterministic baseline function")


__all__ = [
    "ExactObservation",
    "ExactSelectorModel",
    "ExactStatistics",
    "REGULARIZATION",
    "SELECTOR_KINDS",
    "SelectorError",
    "TrainingRow",
    "accumulate_statistics",
    "baseline_model",
    "fit_listwise",
    "fit_multi_head",
    "fit_pairwise",
    "learned_score",
    "linear_scores",
]
