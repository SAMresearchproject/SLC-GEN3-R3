"""Complete-catalog exact evaluation and ambiguity-safe Q1 admission."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Any, Mapping, Sequence

from .canonical import canonical_sha256, fraction_dict
from .selectors import ExactSelectorModel, SelectorError, learned_score
from .source_quality import FEATURE_ORDER, QualityVector


class EvaluationError(RuntimeError):
    """A complete-catalog evaluation or admission rule is invalid."""


@dataclass(frozen=True, slots=True)
class EvaluationRow:
    query_id: str
    group_id: str
    features: tuple[int, ...]
    quality: QualityVector
    multiplicity: int
    baseline_score: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.query_id or not self.group_id:
            raise EvaluationError("evaluation row lacks query/group identity")
        if len(self.features) != len(FEATURE_ORDER):
            raise EvaluationError("evaluation feature width differs from Q1")
        if self.multiplicity < 1:
            raise EvaluationError("evaluation multiplicity must be positive")
        if not self.baseline_score:
            raise EvaluationError("evaluation row lacks baseline score")


def _score(model: ExactSelectorModel, row: EvaluationRow) -> tuple[Any, ...]:
    if model.selector_kind == "DETERMINISTIC_EXACT_BASELINE":
        return row.baseline_score
    return learned_score(model, row.features)


def _fraction(value: Fraction) -> dict[str, str]:
    return fraction_dict(value)


def _query_evaluation(
    model: ExactSelectorModel, rows: Sequence[EvaluationRow]
) -> tuple[dict[str, Any], dict[str, int | Fraction]]:
    if not rows:
        raise EvaluationError("complete query catalog is empty")
    query_ids = {row.query_id for row in rows}
    if len(query_ids) != 1:
        raise EvaluationError("query evaluation mixes query identities")
    if len({row.group_id for row in rows}) != len(rows):
        raise EvaluationError("query evaluation repeats a physical group")
    qualities = sorted({row.quality for row in rows})
    if len(qualities) < 2:
        raise EvaluationError("complete query catalog has no strict quality order")
    tier_by_quality = {quality: index for index, quality in enumerate(qualities)}
    scores = {row.group_id: _score(model, row) for row in rows}
    best_score = max(scores.values())
    proposed = [row for row in rows if scores[row.group_id] == best_score]
    proposed_qualities = {row.quality for row in proposed}

    if len(proposed_qualities) != 1:
        status = "ABSTAIN"
        selected_quality = None
        selected = []
    else:
        selected_quality = next(iter(proposed_qualities))
        selected = [row for row in rows if row.quality == selected_quality]
        selected_receipts = sum(row.multiplicity for row in selected)
        status = "SELECTED_UNIQUE" if selected_receipts == 1 else "AMBIGUOUS_BEST_SET"

    best_quality = qualities[0]
    best = [row for row in rows if row.quality == best_quality]
    best_receipts = sum(row.multiplicity for row in best)
    selected_receipts = sum(row.multiplicity for row in selected)
    best_tier = (
        len(qualities)
        if selected_quality is None
        else tier_by_quality[selected_quality]
    )
    exact_best_set = (
        {row.group_id for row in selected} == {row.group_id for row in best}
        if selected
        else False
    )

    strict_correct = 0
    strict_wrong = 0
    strict_tied = 0
    for left, right in combinations(rows, 2):
        if left.quality == right.quality:
            continue
        better, worse = (left, right) if left.quality < right.quality else (right, left)
        weight = better.multiplicity * worse.multiplicity
        if scores[better.group_id] > scores[worse.group_id]:
            strict_correct += weight
        elif scores[better.group_id] < scores[worse.group_id]:
            strict_wrong += weight
        else:
            strict_tied += weight

    # Exact harmonic tier gain is a rational, log-free graded-list metric.
    # Every score-tied block receives the mean discount across the receipt
    # positions occupied by that block.  This makes the metric custody-free,
    # honors receipt multiplicity, and keeps the ideal target order at 1.
    def harmonic_gain(key: Any) -> Fraction:
        ordered_keys = sorted({key(row) for row in rows}, reverse=True)
        offset = 0
        total = Fraction(0)
        for block_key in ordered_keys:
            block = [row for row in rows if key(row) == block_key]
            width = sum(row.multiplicity for row in block)
            mean_discount = sum(
                (Fraction(1, rank) for rank in range(offset + 1, offset + width + 1)),
                Fraction(0),
            ) / width
            total += sum(
                row.multiplicity
                * (len(qualities) - tier_by_quality[row.quality])
                * mean_discount
                for row in block
            )
            offset += width
        return total

    actual_gain = harmonic_gain(lambda row: scores[row.group_id])
    ideal_gain = harmonic_gain(
        lambda row: len(qualities) - tier_by_quality[row.quality]
    )
    harmonic_ratio = actual_gain / ideal_gain
    if not Fraction(0) <= harmonic_ratio <= Fraction(1):
        raise EvaluationError("exact harmonic tier gain escaped [0,1]")

    receipt = {
        "query_id": next(iter(query_ids)),
        "catalog_group_count": len(rows),
        "catalog_receipt_count": sum(row.multiplicity for row in rows),
        "target_tier_count": len(qualities),
        "best_target_receipt_count": best_receipts,
        "proposed_group_count": len(proposed),
        "proposed_quality_count": len(proposed_qualities),
        "admission_status": status,
        "selected_target_tier": best_tier if selected_quality is not None else None,
        "selected_group_count": len(selected),
        "selected_receipt_count": selected_receipts,
        "best_target_tier_selected": selected_quality == best_quality,
        "exact_best_set_recovered": exact_best_set,
        "false_singleton": best_receipts > 1 and selected_receipts == 1,
        "strict_pair_correct": strict_correct,
        "strict_pair_wrong": strict_wrong,
        "strict_pair_tied": strict_tied,
        "harmonic_tier_gain_ratio": _fraction(harmonic_ratio),
        "selected_quality": selected_quality.to_dict() if selected_quality else None,
        "serialization_order_is_quality_order": False,
    }
    receipt["semantic_sha256"] = canonical_sha256(receipt)
    accumulators: dict[str, int | Fraction] = {
        "query_count": 1,
        "best_tier_selected": int(selected_quality == best_quality),
        "exact_best_set_recovered": int(exact_best_set),
        "false_singleton": int(receipt["false_singleton"]),
        "abstained": int(status == "ABSTAIN"),
        "selected_tier": best_tier,
        "strict_correct": strict_correct,
        "strict_wrong": strict_wrong,
        "strict_tied": strict_tied,
        "harmonic_ratio": harmonic_ratio,
        "receipt_count": receipt["catalog_receipt_count"],
    }
    return receipt, accumulators


def evaluate_complete_catalogs(
    model: ExactSelectorModel,
    rows_by_query: Mapping[str, Sequence[EvaluationRow]],
    *,
    split: str,
    retain_query_receipts: bool = False,
) -> dict[str, Any]:
    if split not in {"HOLDOUT", "CONTROL"}:
        raise EvaluationError("complete evaluation split must be HOLDOUT or CONTROL")
    if not rows_by_query:
        raise EvaluationError("complete evaluation has no queries")
    totals: dict[str, int | Fraction] = {
        "query_count": 0,
        "best_tier_selected": 0,
        "exact_best_set_recovered": 0,
        "false_singleton": 0,
        "abstained": 0,
        "selected_tier": 0,
        "strict_correct": 0,
        "strict_wrong": 0,
        "strict_tied": 0,
        "harmonic_ratio": Fraction(0),
        "receipt_count": 0,
    }
    query_receipts = []
    query_hashes = []
    for query_id in sorted(rows_by_query):
        receipt, accumulators = _query_evaluation(model, rows_by_query[query_id])
        query_hashes.append(receipt["semantic_sha256"])
        if retain_query_receipts:
            query_receipts.append(receipt)
        for name, value in accumulators.items():
            totals[name] += value
    queries = int(totals["query_count"])
    strict_total = int(totals["strict_correct"] + totals["strict_wrong"] + totals["strict_tied"])
    if queries < 1 or strict_total < 1:
        raise EvaluationError("complete evaluation produced no strict comparisons")
    result = {
        "schema": "SLCV32_RZ_Q1_COMPLETE_CATALOG_EVALUATION_V1",
        "status": "PASS",
        "split": split,
        "selector_id": model.selector_id,
        "selector_kind": model.selector_kind,
        "model_semantic_sha256": model.semantic_sha256,
        "query_count": queries,
        "complete_catalog_receipt_exposures": int(totals["receipt_count"]),
        "best_tier_accuracy": _fraction(Fraction(int(totals["best_tier_selected"]), queries)),
        "exact_best_set_recovery": _fraction(Fraction(int(totals["exact_best_set_recovered"]), queries)),
        "false_singleton_rate": _fraction(Fraction(int(totals["false_singleton"]), queries)),
        "abstention_rate": _fraction(Fraction(int(totals["abstained"]), queries)),
        "coverage": _fraction(Fraction(queries - int(totals["abstained"]), queries)),
        "mean_selected_target_tier": _fraction(Fraction(int(totals["selected_tier"]), queries)),
        "strict_pair_accuracy": _fraction(Fraction(int(totals["strict_correct"]), strict_total)),
        "strict_pair_counts": {
            "correct": int(totals["strict_correct"]),
            "tied": int(totals["strict_tied"]),
            "total": strict_total,
            "wrong": int(totals["strict_wrong"]),
        },
        "mean_harmonic_tier_gain_ratio": _fraction(totals["harmonic_ratio"] / queries),
        "query_receipt_semantic_sha256s": query_hashes,
        "query_receipts": query_receipts if retain_query_receipts else None,
        "all_receipts_in_complete_catalog_counted": True,
        "target_ties_never_broken_by_custody": True,
    }
    result["semantic_sha256"] = canonical_sha256(result)
    return result


def _ratio(value: Mapping[str, str]) -> Fraction:
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def winner_key(result: Mapping[str, Any], parameter_count: int, selector_id: str) -> tuple[Any, ...]:
    """Return the frozen HOLDOUT-only winner key; greater is better."""

    if result.get("schema") != "SLCV32_RZ_Q1_COMPLETE_CATALOG_EVALUATION_V1":
        raise EvaluationError("winner selection requires a complete-catalog evaluation")
    if result.get("split") != "HOLDOUT":
        raise EvaluationError("winner selection is restricted to HOLDOUT")
    if result.get("status") != "PASS":
        raise EvaluationError("winner selection requires a passing HOLDOUT result")

    return (
        _ratio(result["exact_best_set_recovery"]),
        _ratio(result["best_tier_accuracy"]),
        _ratio(result["strict_pair_accuracy"]),
        _ratio(result["mean_harmonic_tier_gain_ratio"]),
        -_ratio(result["mean_selected_target_tier"]),
        -_ratio(result["false_singleton_rate"]),
        -_ratio(result["abstention_rate"]),
        -parameter_count,
        tuple(-ord(character) for character in selector_id),
    )


__all__ = [
    "EvaluationError",
    "EvaluationRow",
    "evaluate_complete_catalogs",
    "winner_key",
]
