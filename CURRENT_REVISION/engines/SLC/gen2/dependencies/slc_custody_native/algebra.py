"""Exact symbolic multiplicity and information-weight algebra."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log
from typing import Iterable, Mapping


def factor_positive_integer(value: int) -> tuple[tuple[int, int], ...]:
    """Return the exact prime factorization of a positive integer."""

    n = int(value)
    if n < 1:
        raise ValueError("multiplicity must be a positive integer")
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= n:
        exponent = 0
        while n % divisor == 0:
            n //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        factors.append((n, 1))
    return tuple(factors)


def _coefficient_text(value: Fraction, *, suppress_one: bool = False) -> str:
    if value == 1 and suppress_one:
        return ""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True, slots=True)
class PrimeLogWeight:
    """The exact additive information weight ``log(m)`` of multiplicity m."""

    multiplicity: int
    prime_exponents: tuple[tuple[int, int], ...]

    @classmethod
    def from_multiplicity(cls, multiplicity: int) -> "PrimeLogWeight":
        value = int(multiplicity)
        return cls(value, factor_positive_integer(value))

    @property
    def expression(self) -> str:
        if self.multiplicity == 1:
            return "0"
        terms: list[str] = []
        for prime, exponent in self.prime_exponents:
            if exponent == 1:
                terms.append(f"log({prime})")
            else:
                terms.append(f"{exponent}*log({prime})")
        return " + ".join(terms)

    @property
    def nats(self) -> float:
        return log(self.multiplicity)

    @property
    def bits(self) -> float:
        return self.nats / log(2)

    def compose(self, other: "PrimeLogWeight") -> "PrimeLogWeight":
        return PrimeLogWeight.from_multiplicity(self.multiplicity * other.multiplicity)

    def quotient(self, retained: "PrimeLogWeight") -> "PrimeLogWeight":
        if self.multiplicity % retained.multiplicity:
            raise ValueError("retained multiplicity must divide source multiplicity")
        return PrimeLogWeight.from_multiplicity(self.multiplicity // retained.multiplicity)

    def to_dict(self) -> dict[str, object]:
        return {
            "multiplicity": self.multiplicity,
            "prime_exponents": [
                {"prime": prime, "exponent": exponent}
                for prime, exponent in self.prime_exponents
            ],
            "exact_nats": self.expression,
            "evaluated_nats": self.nats,
            "evaluated_bits": self.bits,
        }


@dataclass(frozen=True, slots=True)
class SymbolicEntropy:
    """A rational linear combination of exact prime logarithms."""

    coefficients: tuple[tuple[int, Fraction], ...] = ()

    @classmethod
    def from_terms(cls, terms: Mapping[int, Fraction | int]) -> "SymbolicEntropy":
        normalized = tuple(
            sorted(
                (int(prime), Fraction(coefficient))
                for prime, coefficient in terms.items()
                if Fraction(coefficient) != 0
            )
        )
        return cls(normalized)

    @classmethod
    def weighted_log(
        cls,
        multiplicity: int,
        coefficient: Fraction | int = Fraction(1),
    ) -> "SymbolicEntropy":
        scalar = Fraction(coefficient)
        return cls.from_terms(
            {
                prime: scalar * exponent
                for prime, exponent in factor_positive_integer(multiplicity)
            }
        )

    @classmethod
    def sum(cls, values: Iterable["SymbolicEntropy"]) -> "SymbolicEntropy":
        accumulator: dict[int, Fraction] = {}
        for value in values:
            for prime, coefficient in value.coefficients:
                accumulator[prime] = accumulator.get(prime, Fraction()) + coefficient
        return cls.from_terms(accumulator)

    def __add__(self, other: "SymbolicEntropy") -> "SymbolicEntropy":
        return SymbolicEntropy.sum((self, other))

    def __sub__(self, other: "SymbolicEntropy") -> "SymbolicEntropy":
        return self + SymbolicEntropy.from_terms(
            {prime: -coefficient for prime, coefficient in other.coefficients}
        )

    @property
    def expression(self) -> str:
        if not self.coefficients:
            return "0"
        terms: list[str] = []
        for prime, coefficient in self.coefficients:
            if coefficient == 1:
                terms.append(f"log({prime})")
            elif coefficient == -1:
                terms.append(f"-log({prime})")
            else:
                terms.append(f"{_coefficient_text(coefficient)}*log({prime})")
        return " + ".join(terms).replace("+ -", "- ")

    @property
    def nats(self) -> float:
        return sum(float(coefficient) * log(prime) for prime, coefficient in self.coefficients)

    @property
    def bits(self) -> float:
        return self.nats / log(2)

    def to_dict(self) -> dict[str, object]:
        return {
            "prime_log_coefficients": [
                {
                    "prime": prime,
                    "coefficient": _coefficient_text(coefficient),
                }
                for prime, coefficient in self.coefficients
            ],
            "exact_nats": self.expression,
            "evaluated_nats": self.nats,
            "evaluated_bits": self.bits,
        }

