"""Complete exact Q3 ranking metrics and changed-error receipts."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations
from typing import Callable, Mapping, Sequence

from .canonical import OrderedSemanticDigest, canonical_sha256, seal
from .training import RankRow


class EvaluationError(RuntimeError):
    """A complete-catalog evaluation or comparison differs."""


Score = tuple[Fraction, ...]


@dataclass(frozen=True, slots=True)
class PairOutcome:
    query_token: str
    better_group_token: str
    worse_group_token: str
    outcome: str
    weight: int
    multiplicity_stratum: tuple[int, int, int]

    @property
    def key(self) -> tuple[str, str, str]:
        return self.query_token, self.better_group_token, self.worse_group_token


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    selector_id: str
    query_count: int
    exact_best_set_recovery: Fraction
    best_tier_accuracy: Fraction
    strict_pair_correct: int
    strict_pair_tied: int
    strict_pair_wrong: int
    strict_pair_total: int
    strict_pair_accuracy: Fraction
    error_count: int
    score_tie_weight: int
    representation_collision_weight: int
    representation_collision_rate: Fraction
    abstention_rate: Fraction
    false_singleton_rate: Fraction
    mean_harmonic_tier_gain: Fraction
    mean_selected_tier: Fraction
    pair_outcomes: tuple[PairOutcome, ...]
    per_multiplicity: tuple[tuple[tuple[int, int, int], int, int, int, int], ...]
    query_receipt_semantic_sha256s: tuple[str, ...]
    streamed_pair_outcome_count: int | None = None
    streamed_pair_outcomes_semantic_sha256: str | None = None

    @property
    def pair_outcome_count(self) -> int:
        if self.streamed_pair_outcome_count is not None:
            return self.streamed_pair_outcome_count
        return len(self.pair_outcomes)

    @property
    def pair_outcomes_semantic_sha256(self) -> str:
        if self.streamed_pair_outcomes_semantic_sha256 is not None:
            return self.streamed_pair_outcomes_semantic_sha256
        return canonical_sha256(self.pair_outcomes)

    @property
    def semantic_sha256(self) -> str:
        return canonical_sha256(self.to_dict())

    def to_dict(self) -> dict[str, object]:
        body = {
            "selector_id": self.selector_id,
            "query_count": self.query_count,
            "exact_best_set_recovery": self.exact_best_set_recovery,
            "best_tier_accuracy": self.best_tier_accuracy,
            "strict_pair_counts": {
                "correct": self.strict_pair_correct,
                "tied": self.strict_pair_tied,
                "wrong": self.strict_pair_wrong,
                "total": self.strict_pair_total,
            },
            "strict_pair_accuracy": self.strict_pair_accuracy,
            "error_count": self.error_count,
            "score_tie_weight": self.score_tie_weight,
            "representation_collision_weight": self.representation_collision_weight,
            "representation_collision_rate": self.representation_collision_rate,
            "abstention_rate": self.abstention_rate,
            "false_singleton_rate": self.false_singleton_rate,
            "mean_harmonic_tier_gain": self.mean_harmonic_tier_gain,
            "mean_selected_tier": self.mean_selected_tier,
            "per_multiplicity": self.per_multiplicity,
            "query_receipt_semantic_sha256s": self.query_receipt_semantic_sha256s,
        }
        if self.streamed_pair_outcome_count is None:
            body["pair_outcomes"] = self.pair_outcomes
        else:
            body["pair_outcome_count"] = self.pair_outcome_count
            body["pair_outcomes_semantic_sha256"] = self.pair_outcomes_semantic_sha256
        return body


@dataclass(slots=True)
class StreamingEvaluationAccumulator:
    """Exact evaluation state retaining only one query's pair outcomes."""

    selector_id: str
    totals: defaultdict[str, int]
    harmonic_total: Fraction
    strata: dict[tuple[int, int, int], list[int]]
    receipt_hashes: list[str]
    pair_digest: OrderedSemanticDigest
    last_query_token: str | None = None

    @classmethod
    def create(cls, selector_id: str) -> "StreamingEvaluationAccumulator":
        return cls(
            selector_id=selector_id,
            totals=defaultdict(int),
            harmonic_total=Fraction(),
            strata=defaultdict(lambda: [0, 0, 0, 0]),
            receipt_hashes=[],
            pair_digest=OrderedSemanticDigest.create(),
        )

    def observe_query(
        self,
        rows: Sequence[RankRow],
        scores: Mapping[str, Score],
    ) -> tuple[PairOutcome, ...]:
        frozen = tuple(rows)
        if len(frozen) < 2:
            raise EvaluationError("streamed evaluation query has fewer than two rows")
        query_tokens = {row.query_token for row in frozen}
        if len(query_tokens) != 1:
            raise EvaluationError("streamed evaluation rows cross query tokens")
        query_token = next(iter(query_tokens))
        if self.last_query_token is not None and query_token <= self.last_query_token:
            raise EvaluationError("streamed evaluation query order differs")
        self.last_query_token = query_token
        if set(scores) != {row.group_token for row in frozen}:
            raise EvaluationError("streamed selector score roster differs")
        if any(not isinstance(score, tuple) or not score for score in scores.values()):
            raise EvaluationError("streamed selector score is not an exact tuple")
        if any(
            isinstance(value, float) or not isinstance(value, (int, Fraction))
            for score in scores.values()
            for value in score
        ):
            raise EvaluationError("streamed selector score contains a non-exact coordinate")

        best_score = max(scores.values())
        proposed = [row for row in frozen if scores[row.group_token] == best_score]
        proposed_qualities = {row.quality for row in proposed}
        selected_quality = (
            next(iter(proposed_qualities)) if len(proposed_qualities) == 1 else None
        )
        selected = [
            row
            for row in frozen
            if selected_quality is not None and row.quality == selected_quality
        ]
        best_quality = min(row.quality for row in frozen)
        best = [row for row in frozen if row.quality == best_quality]
        exact_best = {row.group_token for row in selected} == {
            row.group_token for row in best
        }
        abstained = selected_quality is None
        selected_tier = (
            1 + max(row.tier for row in frozen)
            if abstained
            else next(row.tier for row in frozen if row.quality == selected_quality)
        )
        query_counts = [0, 0, 0]
        query_outcomes: list[PairOutcome] = []
        for left, right in combinations(frozen, 2):
            if left.quality == right.quality:
                continue
            better, worse = (
                (left, right) if left.quality < right.quality else (right, left)
            )
            weight = better.multiplicity * worse.multiplicity
            collision = better.features == worse.features
            if scores[better.group_token] > scores[worse.group_token]:
                outcome = "CORRECT"
                index = 0
            elif scores[better.group_token] < scores[worse.group_token]:
                outcome = "WRONG"
                index = 2
            else:
                outcome = "TIED"
                index = 1
            query_counts[index] += weight
            self.totals[outcome.lower()] += weight
            self.totals["collision"] += int(collision) * weight
            stratum = (
                better.query_multiplicity,
                better.candidate_multiplicity,
                worse.candidate_multiplicity,
            )
            self.strata[stratum][index] += weight
            self.strata[stratum][3] += weight
            row = PairOutcome(
                query_token,
                better.group_token,
                worse.group_token,
                outcome,
                weight,
                stratum,
            )
            self.pair_digest.observe(row)
            query_outcomes.append(row)

        actual = _harmonic_gain(frozen, scores)
        ideal = _harmonic_gain(
            frozen,
            {row.group_token: (-Fraction(row.tier),) for row in frozen},
        )
        harmonic = actual / ideal
        self.totals["queries"] += 1
        self.totals["exact_best"] += int(exact_best)
        self.totals["best"] += int(selected_quality == best_quality)
        self.totals["abstained"] += int(abstained)
        self.totals["false_singleton"] += int(
            sum(row.multiplicity for row in best) > 1
            and sum(row.multiplicity for row in selected) == 1
        )
        self.totals["selected_tier"] += selected_tier
        self.harmonic_total += harmonic
        self.receipt_hashes.append(
            canonical_sha256(
                {
                    "query_token": query_token,
                    "exact_best_set_recovered": exact_best,
                    "selected_tier": None if abstained else selected_tier,
                    "strict_pair_correct": query_counts[0],
                    "strict_pair_tied": query_counts[1],
                    "strict_pair_wrong": query_counts[2],
                }
            )
        )
        return tuple(query_outcomes)

    def finalize(self) -> EvaluationResult:
        queries = self.totals["queries"]
        total = (
            self.totals["correct"]
            + self.totals["tied"]
            + self.totals["wrong"]
        )
        if queries < 1 or total < 1:
            raise EvaluationError("streamed evaluation contains no queries or strict pairs")
        per_multiplicity = tuple(
            (key, values[0], values[1], values[2], values[3])
            for key, values in sorted(self.strata.items())
        )
        return EvaluationResult(
            selector_id=self.selector_id,
            query_count=queries,
            exact_best_set_recovery=Fraction(self.totals["exact_best"], queries),
            best_tier_accuracy=Fraction(self.totals["best"], queries),
            strict_pair_correct=self.totals["correct"],
            strict_pair_tied=self.totals["tied"],
            strict_pair_wrong=self.totals["wrong"],
            strict_pair_total=total,
            strict_pair_accuracy=Fraction(self.totals["correct"], total),
            error_count=self.totals["tied"] + self.totals["wrong"],
            score_tie_weight=self.totals["tied"],
            representation_collision_weight=self.totals["collision"],
            representation_collision_rate=Fraction(self.totals["collision"], total),
            abstention_rate=Fraction(self.totals["abstained"], queries),
            false_singleton_rate=Fraction(self.totals["false_singleton"], queries),
            mean_harmonic_tier_gain=self.harmonic_total / queries,
            mean_selected_tier=Fraction(self.totals["selected_tier"], queries),
            pair_outcomes=(),
            per_multiplicity=per_multiplicity,
            query_receipt_semantic_sha256s=tuple(self.receipt_hashes),
            streamed_pair_outcome_count=self.pair_digest.count,
            streamed_pair_outcomes_semantic_sha256=self.pair_digest.hexdigest,
        )


_OUTCOME_TO_CODE = {"CORRECT": 0, "TIED": 1, "WRONG": 2}
_CODE_TO_OUTCOME = ("CORRECT", "TIED", "WRONG")


@dataclass(slots=True)
class CompactOutcomeStore:
    """Compact HOLDOUT-only pair identities and selector outcome bytes."""

    selector_ids: tuple[str, ...]
    pair_keys: list[tuple[str, str, str]]
    outcomes: dict[str, bytearray]
    pair_key_digest: OrderedSemanticDigest

    @classmethod
    def create(cls, selector_ids: Sequence[str]) -> "CompactOutcomeStore":
        selected = tuple(selector_ids)
        if not selected or len(set(selected)) != len(selected):
            raise EvaluationError("compact outcome selector roster differs")
        return cls(
            selector_ids=selected,
            pair_keys=[],
            outcomes={selector: bytearray() for selector in selected},
            pair_key_digest=OrderedSemanticDigest.create(),
        )

    def observe_query(
        self,
        outcomes_by_selector: Mapping[str, Sequence[PairOutcome]],
    ) -> None:
        if set(outcomes_by_selector) != set(self.selector_ids):
            raise EvaluationError("compact outcome query selector roster differs")
        by_selector = {
            selector: {row.key: row for row in outcomes_by_selector[selector]}
            for selector in self.selector_ids
        }
        first_keys = set(by_selector[self.selector_ids[0]])
        if any(set(rows) != first_keys for rows in by_selector.values()):
            raise EvaluationError("compact outcome strict-pair rosters differ")
        for key in sorted(first_keys):
            self.pair_keys.append(key)
            self.pair_key_digest.observe(key)
            for selector in self.selector_ids:
                outcome = by_selector[selector][key].outcome
                try:
                    code = _OUTCOME_TO_CODE[outcome]
                except KeyError as exc:
                    raise EvaluationError("compact outcome category differs") from exc
                self.outcomes[selector].append(code)

    @property
    def pair_count(self) -> int:
        return len(self.pair_keys)

    def roster_receipt(self) -> dict[str, object]:
        if any(len(values) != self.pair_count for values in self.outcomes.values()):
            raise EvaluationError("compact outcome selector lengths differ")
        return {
            "pair_key_ordered_digest": self.pair_key_digest.receipt(),
            "selector_ids": self.selector_ids,
            "selector_outcome_byte_sha256s": {
                selector: hashlib.sha256(values).hexdigest()
                for selector, values in self.outcomes.items()
            },
        }


@dataclass(slots=True)
class CompactChangedAccumulator:
    """Digest exact changed-error categories without retaining pair rows."""

    baseline_selector_id: str
    candidate_selector_id: str
    category_digests: dict[str, OrderedSemanticDigest]

    @classmethod
    def create(
        cls,
        baseline_selector_id: str,
        candidate_selector_id: str,
    ) -> "CompactChangedAccumulator":
        return cls(
            baseline_selector_id,
            candidate_selector_id,
            {
                category: OrderedSemanticDigest.create()
                for category in (
                    "fixed",
                    "introduced",
                    "unchanged_error",
                    "changed_correct",
                )
            },
        )

    def observe(
        self,
        pair_key: tuple[str, str, str],
        baseline_outcome: str,
        candidate_outcome: str,
    ) -> None:
        before_error = baseline_outcome != "CORRECT"
        after_error = candidate_outcome != "CORRECT"
        if before_error and not after_error:
            category = "fixed"
        elif not before_error and after_error:
            category = "introduced"
        elif before_error and after_error:
            category = "unchanged_error"
        elif baseline_outcome != candidate_outcome:
            category = "changed_correct"
        else:
            return
        self.category_digests[category].observe(
            {
                "pair": pair_key,
                "baseline": baseline_outcome,
                "candidate": candidate_outcome,
            }
        )

    def finalize(
        self,
        baseline: EvaluationResult,
        candidate: EvaluationResult,
    ) -> dict[str, object]:
        if baseline.selector_id != self.baseline_selector_id:
            raise EvaluationError("compact changed baseline selector differs")
        if candidate.selector_id != self.candidate_selector_id:
            raise EvaluationError("compact changed candidate selector differs")
        body = {
            "schema": "SLCV33_RZ_Q3_COMPACT_CHANGED_ERROR_RECEIPT_V1",
            "baseline_selector_id": baseline.selector_id,
            "candidate_selector_id": candidate.selector_id,
            "baseline_error_count": baseline.error_count,
            "candidate_error_count": candidate.error_count,
            "net_error_reduction": baseline.error_count - candidate.error_count,
            "categories": {
                category: digest.receipt()
                for category, digest in self.category_digests.items()
            },
        }
        return seal(body)


def compact_changed_from_store(
    store: CompactOutcomeStore,
    baseline: EvaluationResult,
    candidate: EvaluationResult,
) -> dict[str, object]:
    """Finalize one compact comparison from a bounded HOLDOUT outcome store."""

    try:
        baseline_codes = store.outcomes[baseline.selector_id]
        candidate_codes = store.outcomes[candidate.selector_id]
    except KeyError as exc:
        raise EvaluationError("compact changed selector is absent from outcome store") from exc
    accumulator = CompactChangedAccumulator.create(
        baseline.selector_id,
        candidate.selector_id,
    )
    for key, before, after in zip(
        store.pair_keys,
        baseline_codes,
        candidate_codes,
        strict=True,
    ):
        accumulator.observe(
            key,
            _CODE_TO_OUTCOME[before],
            _CODE_TO_OUTCOME[after],
        )
    return accumulator.finalize(baseline, candidate)


def _harmonic_gain(rows: Sequence[RankRow], scores: Mapping[str, Score]) -> Fraction:
    tier_count = 1 + max(row.tier for row in rows)
    ordered_scores = sorted({scores[row.group_token] for row in rows}, reverse=True)
    offset = 0
    total = Fraction()
    for score in ordered_scores:
        block = [row for row in rows if scores[row.group_token] == score]
        width = sum(row.multiplicity for row in block)
        mean_discount = sum(
            (Fraction(1, rank) for rank in range(offset + 1, offset + width + 1)),
            Fraction(),
        ) / width
        total += sum(
            (row.multiplicity * (tier_count - row.tier) * mean_discount for row in block),
            Fraction(),
        )
        offset += width
    return total


def evaluate_complete_catalog(
    rows_by_query: Mapping[str, Sequence[RankRow]],
    *,
    selector_id: str,
    scorer: Callable[[RankRow], Score],
) -> EvaluationResult:
    totals = defaultdict(int)
    harmonic_total = Fraction()
    outcomes: list[PairOutcome] = []
    receipt_hashes: list[str] = []
    strata: dict[tuple[int, int, int], list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for query_token in sorted(rows_by_query):
        rows = tuple(rows_by_query[query_token])
        if len(rows) < 2 or any(row.query_token != query_token for row in rows):
            raise EvaluationError("evaluation query catalog differs")
        scores = {row.group_token: scorer(row) for row in rows}
        if any(not isinstance(score, tuple) or not score for score in scores.values()):
            raise EvaluationError("selector score is not an exact tuple")
        if any(
            isinstance(value, float) or not isinstance(value, (int, Fraction))
            for score in scores.values()
            for value in score
        ):
            raise EvaluationError("selector score contains a non-exact coordinate")
        best_score = max(scores.values())
        proposed = [row for row in rows if scores[row.group_token] == best_score]
        proposed_qualities = {row.quality for row in proposed}
        selected_quality = next(iter(proposed_qualities)) if len(proposed_qualities) == 1 else None
        selected = [row for row in rows if selected_quality is not None and row.quality == selected_quality]
        best_quality = min(row.quality for row in rows)
        best = [row for row in rows if row.quality == best_quality]
        exact_best = {row.group_token for row in selected} == {row.group_token for row in best}
        abstained = selected_quality is None
        selected_tier = (1 + max(row.tier for row in rows)) if abstained else next(
            row.tier for row in rows if row.quality == selected_quality
        )
        query_counts = [0, 0, 0]
        for left, right in combinations(rows, 2):
            if left.quality == right.quality:
                continue
            better, worse = (left, right) if left.quality < right.quality else (right, left)
            weight = better.multiplicity * worse.multiplicity
            collision = better.features == worse.features
            if scores[better.group_token] > scores[worse.group_token]:
                outcome = "CORRECT"
                index = 0
            elif scores[better.group_token] < scores[worse.group_token]:
                outcome = "WRONG"
                index = 2
            else:
                outcome = "TIED"
                index = 1
            query_counts[index] += weight
            totals[outcome.lower()] += weight
            totals["collision"] += int(collision) * weight
            stratum = (
                better.query_multiplicity,
                better.candidate_multiplicity,
                worse.candidate_multiplicity,
            )
            strata[stratum][index] += weight
            strata[stratum][3] += weight
            outcomes.append(
                PairOutcome(
                    query_token,
                    better.group_token,
                    worse.group_token,
                    outcome,
                    weight,
                    stratum,
                )
            )
        actual = _harmonic_gain(rows, scores)
        ideal = _harmonic_gain(rows, {row.group_token: (-Fraction(row.tier),) for row in rows})
        harmonic = actual / ideal
        totals["queries"] += 1
        totals["exact_best"] += int(exact_best)
        totals["best"] += int(selected_quality == best_quality)
        totals["abstained"] += int(abstained)
        totals["false_singleton"] += int(
            sum(row.multiplicity for row in best) > 1
            and sum(row.multiplicity for row in selected) == 1
        )
        totals["selected_tier"] += selected_tier
        harmonic_total += harmonic
        receipt_hashes.append(
            canonical_sha256(
                {
                    "query_token": query_token,
                    "exact_best_set_recovered": exact_best,
                    "selected_tier": None if abstained else selected_tier,
                    "strict_pair_correct": query_counts[0],
                    "strict_pair_tied": query_counts[1],
                    "strict_pair_wrong": query_counts[2],
                }
            )
        )
    queries = totals["queries"]
    total = totals["correct"] + totals["tied"] + totals["wrong"]
    if queries < 1 or total < 1:
        raise EvaluationError("evaluation contains no queries or strict pairs")
    per_multiplicity = tuple(
        (key, values[0], values[1], values[2], values[3])
        for key, values in sorted(strata.items())
    )
    return EvaluationResult(
        selector_id=selector_id,
        query_count=queries,
        exact_best_set_recovery=Fraction(totals["exact_best"], queries),
        best_tier_accuracy=Fraction(totals["best"], queries),
        strict_pair_correct=totals["correct"],
        strict_pair_tied=totals["tied"],
        strict_pair_wrong=totals["wrong"],
        strict_pair_total=total,
        strict_pair_accuracy=Fraction(totals["correct"], total),
        error_count=totals["tied"] + totals["wrong"],
        score_tie_weight=totals["tied"],
        representation_collision_weight=totals["collision"],
        representation_collision_rate=Fraction(totals["collision"], total),
        abstention_rate=Fraction(totals["abstained"], queries),
        false_singleton_rate=Fraction(totals["false_singleton"], queries),
        mean_harmonic_tier_gain=harmonic_total / queries,
        mean_selected_tier=Fraction(totals["selected_tier"], queries),
        pair_outcomes=tuple(outcomes),
        per_multiplicity=per_multiplicity,
        query_receipt_semantic_sha256s=tuple(receipt_hashes),
    )


def changed_error_receipt(
    baseline: EvaluationResult,
    candidate: EvaluationResult,
) -> dict[str, object]:
    baseline_rows = {row.key: row for row in baseline.pair_outcomes}
    candidate_rows = {row.key: row for row in candidate.pair_outcomes}
    if baseline_rows.keys() != candidate_rows.keys():
        raise EvaluationError("changed-error comparisons require identical strict-pair rosters")
    fixed = []
    introduced = []
    unchanged_error = []
    changed_correct = []
    for key in sorted(baseline_rows):
        before = baseline_rows[key].outcome
        after = candidate_rows[key].outcome
        before_error = before != "CORRECT"
        after_error = after != "CORRECT"
        row = {"pair": key, "baseline": before, "candidate": after}
        if before_error and not after_error:
            fixed.append(row)
        elif not before_error and after_error:
            introduced.append(row)
        elif before_error and after_error:
            unchanged_error.append(row)
        elif before != after:
            changed_correct.append(row)
    body = {
        "baseline_selector_id": baseline.selector_id,
        "candidate_selector_id": candidate.selector_id,
        "fixed": fixed,
        "introduced": introduced,
        "unchanged_error": unchanged_error,
        "changed_correct": changed_correct,
        "baseline_error_count": baseline.error_count,
        "candidate_error_count": candidate.error_count,
        "net_error_reduction": baseline.error_count - candidate.error_count,
    }
    body["semantic_sha256"] = canonical_sha256(body)
    return body
