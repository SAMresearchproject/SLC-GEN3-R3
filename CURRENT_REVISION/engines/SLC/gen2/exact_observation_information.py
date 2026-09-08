"""Exact target information of an observation on full linked candidate records.

The caller supplies the installed runtime's bound ``FormalLogElement`` class.
This module provides the finite partition calculation, not another log algebra.
"""
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Mapping


def _key(value):
    """Preserve exact value types while accepting sequence and rational inputs."""
    if value is None:
        return ("none",)
    if type(value) is bool:
        return ("bool", value)
    if type(value) in (int, Fraction):
        number = Fraction(value)
        return ("rational", number.numerator, number.denominator)
    if type(value) is str:
        return ("text", value)
    if isinstance(value, (list, tuple)):
        return ("sequence", tuple(_key(item) for item in value))
    if isinstance(value, Mapping) and all(type(k) is str for k in value):
        return ("mapping", tuple((k, _key(value[k])) for k in sorted(value)))
    raise ValueError("Target and observation values must have exact, serializable types")


def _json(value):
    if type(value) is Fraction:
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, Mapping):
        return {key: _json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(item) for item in value]
    return value


def _entropy(masses, log_class):
    total = sum(masses, Fraction())
    result = log_class.zero()
    for mass in masses:
        probability = mass / total
        result = result - log_class.from_positive_rational(probability).scale(probability)
    return result


@dataclass(frozen=True)
class InformationScore:
    target_entropy: Any
    conditional_target_entropy: Any
    mutual_information: Any
    records: tuple
    target_partition: tuple
    observation_partition: tuple
    measure: str
    comparison_basis: tuple

    def to_dict(self):
        return {
            "schema": "GEN2_LINKED_TARGET_OBSERVATION_INFORMATION_V1",
            "measure": self.measure,
            "log_unit": "nats",
            "candidate_count": len(self.records),
            "target_entropy": self.target_entropy.to_dict(),
            "conditional_target_entropy": self.conditional_target_entropy.to_dict(),
            "mutual_information": self.mutual_information.to_dict(),
            "records": _json(self.records),
            "target_partition": _json(self.target_partition),
            "observation_partition": _json(self.observation_partition),
        }


def score_observation(records, *, formal_log_cls, weights=None):
    """Compute H(target), H(target|observation), and their exact difference.

    Each input record has exactly ``record_id``, ``target`` and ``observation``.
    Unique nonempty text identifiers label complete linked candidate histories;
    repeated target values stay associated with their individual records.
    ``weights`` is an optional complete ID-to-positive-int/Fraction map. Its
    masses are normalized exactly; omission declares uniform candidate weight.
    """
    records = tuple(records)
    if not records:
        raise ValueError("Information scoring requires a nonempty candidate fiber")
    ids = []
    for row in records:
        if not isinstance(row, Mapping) or set(row) != {"record_id", "target", "observation"}:
            raise ValueError("Each candidate needs record_id, target, and observation only")
        identifier = row["record_id"]
        if type(identifier) is not str or not identifier:
            raise ValueError("Candidate record IDs must be nonempty text")
        _key(row["target"])
        _key(row["observation"])
        ids.append(identifier)
    if len(set(ids)) != len(ids):
        raise ValueError("Candidate record IDs must be unique")
    if weights is None:
        weights = dict.fromkeys(ids, Fraction(1))
        measure = "UNIFORM_OVER_DECLARED_FULL_LINKED_CANDIDATE_RECORDS"
    else:
        if not isinstance(weights, Mapping) or set(weights) != set(ids):
            raise ValueError("Explicit weights must cover exactly the candidate IDs")
        measure = "DECLARED_POSITIVE_EXACT_RECORD_WEIGHTS_NORMALIZED_BY_TOTAL"
    for weight in weights.values():
        if type(weight) not in (int, Fraction) or weight <= 0:
            raise ValueError("Each weight must be a positive exact int or Fraction")
    total = sum((Fraction(weight) for weight in weights.values()), Fraction())
    probabilities = {identifier: Fraction(weights[identifier]) / total for identifier in ids}

    targets, observations = {}, {}
    for row in records:
        identifier = row["record_id"]
        target_key, observation_key = _key(row["target"]), _key(row["observation"])
        target = targets.setdefault(target_key, {
            "target": row["target"], "members": [], "mass": Fraction(),
        })
        target["members"].append(identifier)
        target["mass"] += probabilities[identifier]
        observation = observations.setdefault(observation_key, {
            "observation": row["observation"], "members": [], "mass": Fraction(), "targets": {},
        })
        observation["members"].append(identifier)
        observation["mass"] += probabilities[identifier]
        joint = observation["targets"].setdefault(target_key, {
            "target": row["target"], "members": [], "mass": Fraction(),
        })
        joint["members"].append(identifier)
        joint["mass"] += probabilities[identifier]

    entropy = _entropy([group["mass"] for group in targets.values()], formal_log_cls)
    conditional = formal_log_cls.zero()
    for group in observations.values():
        conditional = conditional + _entropy(
            [target["mass"] for target in group["targets"].values()], formal_log_cls,
        ).scale(group["mass"])
    target_partition = tuple({
        "target": group["target"], "members": tuple(group["members"]), "probability": group["mass"],
    } for group in targets.values())
    observation_partition = tuple({
        "observation": group["observation"], "members": tuple(group["members"]),
        "probability": group["mass"],
        "targets": tuple({
            "target": target["target"], "members": tuple(target["members"]),
            "joint_probability": target["mass"],
            "conditional_probability": target["mass"] / group["mass"],
        } for target in group["targets"].values()),
    } for group in observations.values())
    linked_records = tuple({
        "record_id": row["record_id"], "target": row["target"], "observation": row["observation"],
        "probability": probabilities[row["record_id"]],
    } for row in records)
    basis = tuple(sorted((row["record_id"], _key(row["target"]), probabilities[row["record_id"]])
                         for row in records))
    return InformationScore(entropy, conditional, entropy - conditional, linked_records,
                            target_partition, observation_partition, measure, basis)


def choose_max_information(scores):
    """Return every exact maximizing label for the same target and measure."""
    if not isinstance(scores, Mapping) or not scores:
        raise ValueError("Supply a nonempty label-to-InformationScore mapping")
    selected, best, basis = [], None, None
    for label, score in scores.items():
        if not isinstance(score, InformationScore):
            raise ValueError("Every observation choice must carry an InformationScore")
        if basis is None:
            basis = score.comparison_basis
        elif score.comparison_basis != basis:
            raise ValueError("Observation choices must use the same linked records, target, and measure")
        comparison = 1 if best is None else score.mutual_information.compare(best)
        if comparison > 0:
            selected, best = [label], score.mutual_information
        elif comparison == 0:
            selected.append(label)
    return selected


def report_detail(score, formal_log_cls):
    """Detail of the actual returned report on exactly the scored measure."""
    return {'report_entropy': _entropy([row['probability'] for row in score.observation_partition], formal_log_cls),
            'report_alphabet': len(score.observation_partition)}
