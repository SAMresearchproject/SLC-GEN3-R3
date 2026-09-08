"""Finite custody-morphism compiler with exact receipt reconstruction."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import ceil, log2
from typing import Callable, Generic, Hashable, Iterable, TypeVar

from .algebra import PrimeLogWeight, SymbolicEntropy
from .events import ResetRecord, declare_reset


X = TypeVar("X", bound=Hashable)
Y = TypeVar("Y", bound=Hashable)
Z = TypeVar("Z", bound=Hashable)


def _stable_form(value: object) -> object:
    if isinstance(value, tuple):
        return {"tuple": [_stable_form(item) for item in value]}
    if isinstance(value, list):
        return {"list": [_stable_form(item) for item in value]}
    if isinstance(value, dict):
        return {
            "dict": [
                [_stable_form(key), _stable_form(item)]
                for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))
            ]
        }
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return {"type": type(value).__qualname__, "repr": repr(value)}


def _stable_bytes(value: object) -> bytes:
    return json.dumps(
        _stable_form(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def _stable_sort(values: Iterable[X]) -> tuple[X, ...]:
    return tuple(sorted(values, key=_stable_bytes))


def _container_bits(symbol_count: int) -> int:
    if symbol_count < 1:
        raise ValueError("symbol count must be positive")
    return 0 if symbol_count == 1 else ceil(log2(symbol_count))


@dataclass(frozen=True, slots=True)
class FiberReceipt:
    schema: str
    morphism_id: str
    fiber_multiplicity: int
    fiber_index: int
    container_bits: int
    exact_information_nats: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CustodyState(Generic[Y]):
    visible: Y
    receipt: FiberReceipt


@dataclass(frozen=True, slots=True)
class FiberProfile:
    schema: str
    morphism_id: str
    name: str
    input_count: int
    visible_output_count: int
    fiber_strata: tuple[tuple[int, int], ...]
    visible_map_injective: bool
    augmented_map_injective: bool
    expected_hidden_information: SymbolicEntropy
    worst_case_hidden_information: PrimeLogWeight
    expected_receipt_container_bits: float
    worst_case_receipt_container_bits: int

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "morphism_id": self.morphism_id,
            "name": self.name,
            "input_count": self.input_count,
            "visible_output_count": self.visible_output_count,
            "fiber_strata": [
                {
                    "fiber_multiplicity": multiplicity,
                    "visible_output_count": output_count,
                    "exact_information_weight": PrimeLogWeight.from_multiplicity(multiplicity).expression,
                    "receipt_container_bits": _container_bits(multiplicity),
                }
                for multiplicity, output_count in self.fiber_strata
            ],
            "visible_map_injective": self.visible_map_injective,
            "augmented_map_injective": self.augmented_map_injective,
            "expected_hidden_information": self.expected_hidden_information.to_dict(),
            "worst_case_hidden_information": self.worst_case_hidden_information.to_dict(),
            "expected_receipt_container_bits": self.expected_receipt_container_bits,
            "worst_case_receipt_container_bits": self.worst_case_receipt_container_bits,
        }


class CompiledCustodyMorphism(Generic[X, Y]):
    """A visible finite map plus its canonical minimal fiber-index receipt."""

    def __init__(
        self,
        name: str,
        domain: Iterable[X],
        visible_map: Callable[[X], Y],
        *,
        source_references: tuple[str, ...] = (),
    ) -> None:
        self.name = str(name)
        self.source_references = tuple(source_references)
        self.domain = _stable_sort(tuple(domain))
        if not self.domain:
            raise ValueError("morphism domain cannot be empty")
        if len(set(self.domain)) != len(self.domain):
            raise ValueError("morphism domain contains duplicates")

        output_by_input: dict[X, Y] = {}
        mutable_fibers: dict[Y, list[X]] = {}
        for item in self.domain:
            output = visible_map(item)
            try:
                hash(output)
            except TypeError as exc:
                raise TypeError("visible outputs must be hashable") from exc
            output_by_input[item] = output
            mutable_fibers.setdefault(output, []).append(item)
        self._output_by_input = output_by_input
        self._fibers = {
            output: _stable_sort(fiber)
            for output, fiber in mutable_fibers.items()
        }
        self._index_by_input = {
            item: index
            for fiber in self._fibers.values()
            for index, item in enumerate(fiber)
        }
        self.morphism_id = self._fingerprint()
        self.profile = self._build_profile()

    def _fingerprint(self) -> str:
        digest = hashlib.sha256()
        digest.update(self.name.encode("utf-8"))
        digest.update(b"\0")
        for item in self.domain:
            digest.update(_stable_bytes(item))
            digest.update(b"->")
            digest.update(_stable_bytes(self._output_by_input[item]))
            digest.update(b"\n")
        return digest.hexdigest()

    def _build_profile(self) -> FiberProfile:
        stratum_counts: dict[int, int] = {}
        entropy_terms: list[SymbolicEntropy] = []
        expected_container_bits = Fraction()
        total = len(self.domain)
        for fiber in self._fibers.values():
            multiplicity = len(fiber)
            stratum_counts[multiplicity] = stratum_counts.get(multiplicity, 0) + 1
            probability_mass = Fraction(multiplicity, total)
            entropy_terms.append(SymbolicEntropy.weighted_log(multiplicity, probability_mass))
            expected_container_bits += probability_mass * _container_bits(multiplicity)
        worst = max(stratum_counts)
        augmented_pairs = {
            (self._output_by_input[item], self._index_by_input[item])
            for item in self.domain
        }
        return FiberProfile(
            schema="SLC_CUSTODY_NATIVE_FIBER_PROFILE_V1",
            morphism_id=self.morphism_id,
            name=self.name,
            input_count=total,
            visible_output_count=len(self._fibers),
            fiber_strata=tuple(sorted(stratum_counts.items())),
            visible_map_injective=worst == 1,
            augmented_map_injective=len(augmented_pairs) == total,
            expected_hidden_information=SymbolicEntropy.sum(entropy_terms),
            worst_case_hidden_information=PrimeLogWeight.from_multiplicity(worst),
            expected_receipt_container_bits=float(expected_container_bits),
            worst_case_receipt_container_bits=_container_bits(worst),
        )

    @property
    def visible_outputs(self) -> tuple[Y, ...]:
        return _stable_sort(self._fibers)

    def visible(self, item: X) -> Y:
        return self._output_by_input[item]

    def fiber(self, visible: Y) -> tuple[X, ...]:
        return self._fibers[visible]

    def encode(self, item: X) -> CustodyState[Y]:
        visible = self.visible(item)
        multiplicity = len(self._fibers[visible])
        receipt = FiberReceipt(
            schema="SLC_CUSTODY_NATIVE_FIBER_RECEIPT_V1",
            morphism_id=self.morphism_id,
            fiber_multiplicity=multiplicity,
            fiber_index=self._index_by_input[item],
            container_bits=_container_bits(multiplicity),
            exact_information_nats=PrimeLogWeight.from_multiplicity(multiplicity).expression,
        )
        return CustodyState(visible=visible, receipt=receipt)

    def decode(self, visible: Y, receipt: FiberReceipt) -> X:
        if receipt.morphism_id != self.morphism_id:
            raise ValueError("receipt belongs to a different custody morphism")
        fiber = self._fibers[visible]
        if receipt.fiber_multiplicity != len(fiber):
            raise ValueError("receipt fiber multiplicity does not match visible output")
        if not 0 <= receipt.fiber_index < len(fiber):
            raise ValueError("receipt fiber index is outside the visible fiber")
        return fiber[receipt.fiber_index]

    def discard_receipt(
        self,
        state: CustodyState[Y],
        *,
        physical_reset_declared: bool = False,
        temperature_kelvin: int | str | None = None,
    ) -> ResetRecord:
        if state.receipt.morphism_id != self.morphism_id:
            raise ValueError("state receipt belongs to a different custody morphism")
        return declare_reset(
            self.morphism_id,
            state.receipt.fiber_multiplicity,
            physical_reset_declared=physical_reset_declared,
            temperature_kelvin=temperature_kelvin,
        )

    def audit(self) -> dict[str, object]:
        reconstruction_failures: list[str] = []
        augmented_keys: set[tuple[Y, int]] = set()
        receipt_alphabet_failures: list[str] = []
        for visible, fiber in self._fibers.items():
            observed_indices: set[int] = set()
            for item in fiber:
                state = self.encode(item)
                augmented_keys.add((state.visible, state.receipt.fiber_index))
                observed_indices.add(state.receipt.fiber_index)
                if self.decode(state.visible, state.receipt) != item:
                    reconstruction_failures.append(repr(item))
            if observed_indices != set(range(len(fiber))):
                receipt_alphabet_failures.append(repr(visible))
        return {
            "schema": "SLC_CUSTODY_NATIVE_MORPHISM_AUDIT_V1",
            "morphism_id": self.morphism_id,
            "input_count": len(self.domain),
            "augmented_key_count": len(augmented_keys),
            "augmented_map_injective": len(augmented_keys) == len(self.domain),
            "reconstruction_failures": reconstruction_failures,
            "receipt_alphabet_failures": receipt_alphabet_failures,
            "status": (
                "PASS"
                if not reconstruction_failures
                and not receipt_alphabet_failures
                and len(augmented_keys) == len(self.domain)
                else "FAIL"
            ),
        }

    def compose(
        self,
        after: "CompiledCustodyMorphism[Y, Z]",
        *,
        name: str | None = None,
    ) -> tuple["CompiledCustodyMorphism[X, Z]", dict[str, object]]:
        missing = [visible for visible in self.visible_outputs if visible not in after._output_by_input]
        if missing:
            raise ValueError("second morphism domain does not contain every first-stage output")
        composed = CompiledCustodyMorphism(
            name or f"{after.name}_AFTER_{self.name}",
            self.domain,
            lambda item: after.visible(self.visible(item)),
            source_references=(self.morphism_id, after.morphism_id),
        )

        total = len(self.domain)
        raw_weighted_bits = Fraction()
        minimized_weighted_bits = Fraction()
        strata: list[dict[str, object]] = []
        for final_visible, composite_fiber in composed._fibers.items():
            intermediate_values = {
                self.visible(item)
                for item in composite_fiber
            }
            second_fiber_size = len(after.fiber(final_visible))
            first_max_bits = max(
                _container_bits(len(self.fiber(intermediate)))
                for intermediate in intermediate_values
            )
            raw_bits = _container_bits(second_fiber_size) + first_max_bits
            minimized_bits = _container_bits(len(composite_fiber))
            probability_mass = Fraction(len(composite_fiber), total)
            raw_weighted_bits += probability_mass * raw_bits
            minimized_weighted_bits += probability_mass * minimized_bits
            strata.append(
                {
                    "final_visible": repr(final_visible),
                    "composed_fiber_multiplicity": len(composite_fiber),
                    "raw_pair_container_bits": raw_bits,
                    "direct_minimal_container_bits": minimized_bits,
                }
            )
        report = {
            "schema": "SLC_CUSTODY_NATIVE_COMPOSITION_REPORT_V1",
            "first_morphism_id": self.morphism_id,
            "second_morphism_id": after.morphism_id,
            "composed_morphism_id": composed.morphism_id,
            "raw_pair_expected_container_bits": float(raw_weighted_bits),
            "direct_minimal_expected_container_bits": float(minimized_weighted_bits),
            "expected_container_bit_savings": float(raw_weighted_bits - minimized_weighted_bits),
            "strata": strata,
            "composed_audit": composed.audit(),
        }
        return composed, report

