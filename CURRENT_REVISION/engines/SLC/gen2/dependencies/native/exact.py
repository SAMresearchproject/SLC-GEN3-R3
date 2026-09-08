"""Exact values and canonical records shared by Q3 and CE."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from fractions import Fraction
import hashlib
import json
from typing import Any


class ExactError(ValueError):
    pass


def fraction(value: Any) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ExactError("expected an integer, rational string or Fraction")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ExactError("invalid exact rational") from exc
    if isinstance(value, str) and str(result) != value:
        raise ExactError("rational string is not canonical")
    return result


def integer(value: Any, *, minimum: int | None = None) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ExactError("integer outside the declared range")
    return value


def token(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExactError("empty type, endpoint, action or source identifier")
    return value


def plain(value: Any) -> Any:
    if isinstance(value, Fraction):
        return {"rational": [str(value.numerator), str(value.denominator)]}
    if is_dataclass(value):
        return plain(asdict(value))
    if value is None or type(value) in (str, int, bool):
        return value
    if isinstance(value, (tuple, list)):
        return [plain(item) for item in value]
    if isinstance(value, dict) and all(type(key) is str for key in value):
        return {key: plain(item) for key, item in value.items()}
    raise ExactError(f"nonexact or unsupported canonical value: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(plain(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode() + b"\n"


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def seal(schema: str, **body: Any) -> dict:
    if "schema" in body or "semantic_sha256" in body:
        raise ExactError("reserved receipt field")
    value = plain({"schema": token(schema), **body})
    return {**value, "semantic_sha256": digest(value)}


def verify(value: dict, schema: str | None = None) -> dict:
    if not isinstance(value, dict):
        raise ExactError("receipt is not an object")
    body = dict(value)
    expected = body.pop("semantic_sha256", None)
    if expected != digest(body) or (schema is not None and body.get("schema") != schema):
        raise ExactError("receipt identity or schema differs")
    return body


def vector(values) -> tuple[Fraction, ...]:
    result = tuple(fraction(value) for value in values)
    if not result:
        raise ExactError("empty vector")
    return result


def symmetric_matrix(values, dimension: int) -> tuple[tuple[Fraction, ...], ...]:
    rows = tuple(vector(row) for row in values)
    if len(rows) != dimension or any(len(row) != dimension for row in rows):
        raise ExactError("quadratic matrix dimension differs")
    if any(rows[i][j] != rows[j][i] for i in range(dimension) for j in range(i)):
        raise ExactError("quadratic matrix is not symmetric")
    return rows


def dot(a, b) -> Fraction:
    if len(a) != len(b):
        raise ExactError("vector dimensions differ")
    return sum((x * y for x, y in zip(a, b)), Fraction())


def bilinear(a, matrix, b) -> Fraction:
    return dot(a, tuple(dot(row, b) for row in matrix))
