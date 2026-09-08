"""Exact hybrid listwise-plus-adjacent Q3 trainer."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import chain
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence

from .binding import DEFAULT_BINDING_PATH, require_sealed_icf1_binding
from .canonical import canonical_sha256
from .features import REPRESENTATION_WIDTHS, Representation


class TrainingError(RuntimeError):
    """The frozen exact training budget or catalog differs."""


@dataclass(frozen=True, slots=True)
class RankRow:
    query_token: str
    group_token: str
    quality: tuple[int, int, int, int]
    tier: int
    multiplicity: int
    query_multiplicity: int
    candidate_multiplicity: int
    features: tuple[Fraction, ...]


@dataclass(frozen=True, slots=True)
class Observation:
    design: tuple[Fraction, ...]
    target: Fraction
    weight: int


@dataclass(frozen=True, slots=True)
class ExactStatistics:
    gram: tuple[tuple[Fraction, ...], ...]
    rhs: tuple[Fraction, ...]
    observation_count: int
    weighted_observation_count: int


@dataclass(slots=True)
class ExactStatisticsAccumulator:
    """One-representation exact Gram/RHS accumulator for query-local rows."""

    width: int
    gram: list[list[Fraction]]
    rhs: list[Fraction]
    observation_count: int = 0
    weighted_observation_count: int = 0

    @classmethod
    def create(cls, width: int) -> "ExactStatisticsAccumulator":
        if isinstance(width, bool) or not isinstance(width, int) or width < 1:
            raise TrainingError("statistics accumulator width must be positive")
        return cls(
            width,
            [[Fraction() for _ in range(width)] for _ in range(width)],
            [Fraction() for _ in range(width)],
        )

    def observe(self, observation: Observation) -> None:
        if len(observation.design) != self.width or observation.weight < 1:
            raise TrainingError("exact streamed observation differs")
        weight = Fraction(observation.weight)
        self.observation_count += 1
        self.weighted_observation_count += observation.weight
        nonzero = tuple(
            (index, value)
            for index, value in enumerate(observation.design)
            if value
        )
        for position, (left, value) in enumerate(nonzero):
            weighted = weight * value
            self.rhs[left] += weighted * observation.target
            for right, right_value in nonzero[position:]:
                self.gram[left][right] += weighted * right_value

    def observe_query(
        self,
        query_token: str,
        rows: Sequence[RankRow],
        *,
        adjacent_weight: int = 4,
    ) -> None:
        for observation in iter_hybrid_observations(
            {query_token: tuple(rows)},
            adjacent_weight=adjacent_weight,
        ):
            self.observe(observation)

    def finalize(self) -> ExactStatistics:
        if self.observation_count < 1:
            raise TrainingError("statistics accumulator contains no observations")
        for left in range(self.width):
            for right in range(left):
                self.gram[left][right] = self.gram[right][left]
        return ExactStatistics(
            gram=tuple(tuple(row) for row in self.gram),
            rhs=tuple(self.rhs),
            observation_count=self.observation_count,
            weighted_observation_count=self.weighted_observation_count,
        )


@dataclass(frozen=True, slots=True)
class ExactHybridModel:
    representation: str
    regularization: Fraction
    parameters: tuple[Fraction, ...]
    adjacent_weight: int
    statistics_semantic_sha256: str

    @property
    def selector_id(self) -> str:
        return (
            f"Q3-{self.representation}-HYBRID-LISTWISE-ADJACENT-"
            f"RIDGE-{self.regularization.numerator}D{self.regularization.denominator}"
        )

    @property
    def semantic_sha256(self) -> str:
        return canonical_sha256(
            {
                "selector_id": self.selector_id,
                "representation": self.representation,
                "regularization": self.regularization,
                "parameters": self.parameters,
                "adjacent_weight": self.adjacent_weight,
                "statistics_semantic_sha256": self.statistics_semantic_sha256,
            }
        )

    def score(self, row: RankRow) -> tuple[Fraction, ...]:
        if len(row.features) != len(self.parameters):
            raise TrainingError("model and feature widths differ")
        return (
            sum(
                (parameter * feature for parameter, feature in zip(self.parameters, row.features, strict=True)),
                Fraction(),
            ),
        )


RIDGES = (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10))
ADJACENT_WEIGHT = 4


def selected_tiers(tier_count: int) -> tuple[int, ...]:
    if tier_count < 2:
        raise TrainingError("training catalog has fewer than two target tiers")
    selected = set(range(min(6, tier_count)))
    for quantile in range(1, 8):
        center = (quantile * (tier_count - 1)) // 8
        for delta in (-1, 0, 1):
            selected.add(max(0, min(tier_count - 1, center + delta)))
    selected.update(range(max(0, tier_count - 2), tier_count))
    return tuple(sorted(selected))


def hybrid_observations(
    rows_by_query: Mapping[str, Sequence[RankRow]],
    *,
    adjacent_weight: int = ADJACENT_WEIGHT,
) -> tuple[Observation, ...]:
    return tuple(
        iter_hybrid_observations(
            rows_by_query,
            adjacent_weight=adjacent_weight,
        )
    )


def iter_hybrid_observations(
    rows_by_query: Mapping[str, Sequence[RankRow]],
    *,
    adjacent_weight: int = ADJACENT_WEIGHT,
) -> Iterator[Observation]:
    """Yield the frozen objective without retaining its design vectors."""

    width: int | None = None
    observed = False
    for query_token in sorted(rows_by_query):
        rows = tuple(rows_by_query[query_token])
        if len(rows) < 2 or any(row.query_token != query_token for row in rows):
            raise TrainingError("training query catalog is invalid")
        widths = {len(row.features) for row in rows}
        if len(widths) != 1:
            raise TrainingError("one query contains mixed feature widths")
        row_width = next(iter(widths))
        width = row_width if width is None else width
        if row_width != width:
            raise TrainingError("training queries contain mixed feature widths")
        maximum = max(row.tier for row in rows)
        grades = {row.group_token: Fraction(maximum - row.tier) for row in rows}
        total_weight = sum(row.multiplicity for row in rows)
        mean = sum(
            (grades[row.group_token] * row.multiplicity for row in rows),
            Fraction(),
        ) / total_weight
        for row in rows:
            observed = True
            yield Observation(
                row.features,
                grades[row.group_token] - mean,
                row.multiplicity,
            )
        for left, right in combinations(rows, 2):
            if abs(left.tier - right.tier) != 1:
                continue
            better, worse = (left, right) if left.tier < right.tier else (right, left)
            observed = True
            yield Observation(
                tuple(
                    a - b
                    for a, b in zip(
                        better.features, worse.features, strict=True
                    )
                ),
                Fraction(1),
                adjacent_weight * better.multiplicity * worse.multiplicity,
            )
    if not observed:
        raise TrainingError("hybrid objective contains no observations")


def exact_statistics(observations: Iterable[Observation]) -> ExactStatistics:
    iterator = iter(observations)
    try:
        first = next(iterator)
    except StopIteration as exc:
        raise TrainingError("statistics require observations") from exc
    width = len(first.design)
    if width < 1:
        raise TrainingError("feature width must be positive")
    accumulator = ExactStatisticsAccumulator.create(width)
    for observation in chain((first,), iterator):
        accumulator.observe(observation)
    return accumulator.finalize()


def statistics_semantic_sha256(statistics: ExactStatistics) -> str:
    return canonical_sha256(
        {
            "gram": statistics.gram,
            "rhs": statistics.rhs,
            "observation_count": statistics.observation_count,
            "weighted_observation_count": statistics.weighted_observation_count,
        }
    )


def solve_exact_ridge(statistics: ExactStatistics, regularization: Fraction) -> tuple[Fraction, ...]:
    ridge = Fraction(regularization)
    if ridge <= 0:
        raise TrainingError("ridge regularization must be positive")
    size = len(statistics.gram)
    matrix = [
        [value + (ridge if row == column else 0) for column, value in enumerate(values)]
        + [statistics.rhs[row]]
        for row, values in enumerate(statistics.gram)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size) if matrix[row][column]), None)
        if pivot is None:
            raise TrainingError("regularized exact system is singular")
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
                    value - factor * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[column], strict=True)
                ]
    result = tuple(row[-1] for row in matrix)
    for index, (row, target) in enumerate(zip(statistics.gram, statistics.rhs, strict=True)):
        observed = sum(
            (value * parameter for value, parameter in zip(row, result, strict=True)),
            Fraction(),
        ) + ridge * result[index]
        if observed != target:
            raise TrainingError("exact ridge reconstruction differs")
    return result


def fit_exact_hybrid(
    representation: str,
    rows_by_query: Mapping[str, Sequence[RankRow]],
    regularization: Fraction,
    *,
    adjacent_weight: int = ADJACENT_WEIGHT,
) -> ExactHybridModel:
    statistics = exact_statistics(
        iter_hybrid_observations(
            rows_by_query,
            adjacent_weight=adjacent_weight,
        )
    )
    statistics_semantic = statistics_semantic_sha256(statistics)
    return ExactHybridModel(
        representation=representation,
        regularization=Fraction(regularization),
        parameters=solve_exact_ridge(statistics, Fraction(regularization)),
        adjacent_weight=adjacent_weight,
        statistics_semantic_sha256=statistics_semantic,
    )


def fit_q3_budget(
    catalogs: Mapping[Representation, Mapping[str, Sequence[RankRow]]],
    *,
    binding_path: str | Path = DEFAULT_BINDING_PATH,
) -> tuple[ExactHybridModel, ...]:
    """Fit the frozen 15-model budget only after the V6 foundation binds."""

    require_sealed_icf1_binding(binding_path)
    if set(catalogs) != set(Representation):
        raise TrainingError("Q3 fit requires all five frozen representations")
    models: list[ExactHybridModel] = []
    for representation in Representation:
        rows = catalogs[representation]
        widths = {len(row.features) for query_rows in rows.values() for row in query_rows}
        if widths != {REPRESENTATION_WIDTHS[representation]}:
            raise TrainingError(f"{representation.value} catalog width differs")
        statistics = exact_statistics(
            iter_hybrid_observations(rows, adjacent_weight=ADJACENT_WEIGHT)
        )
        statistics_semantic = statistics_semantic_sha256(statistics)
        models.extend(
            ExactHybridModel(
                representation=representation.value,
                regularization=ridge,
                parameters=solve_exact_ridge(statistics, ridge),
                adjacent_weight=ADJACENT_WEIGHT,
                statistics_semantic_sha256=statistics_semantic,
            )
            for ridge in RIDGES
        )
    if len(models) != 15:
        raise TrainingError("Q3 exact fit count differs")
    return tuple(models)
