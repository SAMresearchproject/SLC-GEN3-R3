"""Exact formal state kernel for the twelve-lebit SLC C1 simulator.

The kernel deliberately implements only the real operator fragment frozen by
SLCX002/SLCX003:

* ``B`` is a one-site binary flip;
* ``PREPARE_REQUEST`` is the balanced real transform H;
* ``X1_RESPONSE`` is the ordered controlled binary response (CNOT).

An amplitude is represented as ``coefficient / sqrt(2) ** sqrt2_power``.
There are no floating-point state decisions in this module.  Physical
connectivity, complex phase, publication/Born readout, and hardware cost are
not silently supplied; their entry points raise typed boundary exceptions.

Site zero is the least-significant bit of a basis index.  Displayed bitstrings
use conventional high-to-low order (L11 ... L0).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from .errors import (
    SLCControlTargetAliasError,
    SLCRegisterArityError,
    SLCSiteRangeError,
    SLCStateCustodyError,
    SLCStateInvariantError,
    SLCUnsupportedConnectivityError,
    SLCUnsupportedPhaseError,
    SLCUnsupportedPublicationError,
)


REGISTER_SIZE = 12
DIMENSION = 1 << REGISTER_SIZE
STATE_SCHEMA = "SAM_LANGUAGE_SLC_C1_EXACT_STATE_V1"
HISTORY_SCHEMA = "SAM_LANGUAGE_SLC_C1_ROUTE_HISTORY_V1"
FORMAL_AUTHORITY = "FORMAL_CANDIDATE"

FROZEN_SOURCE_HASHES = MappingProxyType(
    {
        "SLCX002_OPERATOR_MATRICES.json": "3974aabdc8b9a4dd5edff8cf9030c59aeba641d222871c4e9498ba1b40ea052d",
        "SLCX003_OPERATOR_LIFT.json": "26029b0ed3ec02049a73c46215be726df9e698fc15209c823cf64280662444a6",
        "SLCX003_12_LEBIT_FORMAL_GRAMMAR.md": "34f549336a183b4bcc7a6ebe5f468207610b7ee6dd393015aff629590529fb61",
    }
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _domain_hash(domain: str, value: Any) -> str:
    material = domain.encode("ascii") + b"\x00" + _canonical_json(value).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def _canonical_hash(value: Any) -> str:
    """SHA-256 of canonical UTF-8 JSON, exactly as frozen by the contract."""

    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


_OPERATOR_CONTRACTS = MappingProxyType(
    {
        "SLC_ZERO_REGISTER": MappingProxyType(
            {
                "arity": 0,
                "map": "construct |0>^12",
                "predecessor_name": "SLCX003 12-lebit register origin",
                "phase_semantics": "none",
            }
        ),
        "SLC_BINARY_FLIP": MappingProxyType(
            {
                "arity": 1,
                "map": "|x> -> |x XOR 1> at the selected site",
                "predecessor_name": "SLC B",
                "phase_semantics": "none",
            }
        ),
        "SLC_PREPARE_REQUEST": MappingProxyType(
            {
                "arity": 1,
                "map": "|0> -> (|0>+|1>)/sqrt(2); |1> -> (|0>-|1>)/sqrt(2)",
                "predecessor_name": "SLCX002 PREPARE_REQUEST",
                "phase_semantics": "real_sign_only",
            }
        ),
        "SLC_X1_RESPONSE": MappingProxyType(
            {
                "arity": 2,
                "map": "|control,target> -> |control,target XOR control>",
                "predecessor_name": "SLCX002 X1_RESPONSE",
                "ordered_arguments": True,
                "physical_connectivity": "open",
            }
        ),
    }
)


def _plain_contract(operator: str) -> dict[str, Any]:
    try:
        contract = _OPERATOR_CONTRACTS[operator]
    except KeyError as exc:
        raise SLCStateCustodyError(f"unknown history operator: {operator!r}") from exc
    return {key: value for key, value in contract.items()}


def operator_contract_hash(operator: str) -> str:
    """Return the frozen, domain-separated hash of one operator contract."""

    return _domain_hash(
        "SLC-C1-OPERATOR-CONTRACT",
        {"schema": STATE_SCHEMA, "operator": operator, "contract": _plain_contract(operator)},
    )


OPERATOR_CONTRACT_HASHES = MappingProxyType(
    {name: operator_contract_hash(name) for name in _OPERATOR_CONTRACTS}
)


def engine_contract_hash() -> str:
    """Hash the complete executable fragment without claiming source custody."""

    return _domain_hash(
        "SLC-C1-ENGINE-CONTRACT",
        {
            "schema": STATE_SCHEMA,
            "register_size": REGISTER_SIZE,
            "dimension": DIMENSION,
            "amplitude_form": "integer/sqrt(2)^k",
            "operator_contract_hashes": dict(OPERATOR_CONTRACT_HASHES),
            "frozen_source_hashes": dict(FROZEN_SOURCE_HASHES),
            "open_boundaries": [
                "complex_phase",
                "publication_born_readout",
                "physical_connectivity",
                "hardware_cost",
            ],
        },
    )


ENGINE_CONTRACT_HASH = engine_contract_hash()


def _require_int(value: Any, label: str) -> int:
    if type(value) is not int:  # bool is intentionally rejected
        raise SLCStateInvariantError(f"{label} must be an integer, got {type(value).__name__}")
    return value


def _validate_site(site: Any) -> int:
    if type(site) is not int or not 0 <= site < REGISTER_SIZE:
        raise SLCSiteRangeError(
            f"site must be an integer from 0 through {REGISTER_SIZE - 1}; got {site!r}"
        )
    return site


def _validate_basis_index(index: Any) -> int:
    if type(index) is not int or not 0 <= index < DIMENSION:
        raise SLCStateInvariantError(
            f"basis index must be an integer from 0 through {DIMENSION - 1}; got {index!r}"
        )
    return index


def _canonicalize_sparse(
    coefficients: Mapping[int, int] | Iterable[tuple[int, int]],
    sqrt2_power: int,
) -> tuple[tuple[tuple[int, int], ...], int]:
    """Combine, prune, sort, and denominator-reduce a sparse exact state."""

    power = _require_int(sqrt2_power, "sqrt2_power")
    if power < 0:
        raise SLCStateInvariantError("sqrt2_power cannot be negative")

    items = coefficients.items() if isinstance(coefficients, Mapping) else coefficients
    combined: dict[int, int] = {}
    try:
        iterator = iter(items)
    except TypeError as exc:
        raise SLCStateInvariantError("coefficients must be a mapping or iterable of pairs") from exc

    for item in iterator:
        try:
            index, coefficient = item
        except (TypeError, ValueError) as exc:
            raise SLCStateInvariantError(
                "each sparse coefficient entry must be a (basis_index, integer) pair"
            ) from exc
        index = _validate_basis_index(index)
        coefficient = _require_int(coefficient, f"coefficient[{index}]")
        combined[index] = combined.get(index, 0) + coefficient

    combined = {index: coefficient for index, coefficient in combined.items() if coefficient != 0}
    if not combined:
        raise SLCStateInvariantError("an exact state cannot have empty support")

    # sqrt(2)^2 = 2.  Dividing every coefficient by two while reducing the
    # exponent by two is the only integer-preserving denominator reduction.
    while power >= 2 and all(coefficient % 2 == 0 for coefficient in combined.values()):
        combined = {index: coefficient // 2 for index, coefficient in combined.items()}
        power -= 2

    return tuple(sorted(combined.items())), power


def _state_hash(coefficients: Sequence[tuple[int, int]], sqrt2_power: int) -> str:
    return _canonical_hash(
        {
            "schema": STATE_SCHEMA,
            "register_size": REGISTER_SIZE,
            "sqrt2_power": sqrt2_power,
            "coefficients": [[index, coefficient] for index, coefficient in coefficients],
        }
    )


def _history_genesis_hash(state_hash: str) -> str:
    return _canonical_hash(
        {
            "schema": HISTORY_SCHEMA,
            "record_type": "GENESIS",
            "initial_state_hash": state_hash,
            "engine_contract_hash": ENGINE_CONTRACT_HASH,
            "frozen_source_hashes": dict(FROZEN_SOURCE_HASHES),
        }
    )


def _history_record_material(
    *,
    sequence: int,
    operator: str,
    arguments: Sequence[int],
    prior_state_hash: str,
    result_state_hash: str,
    prior_history_hash: str,
    contract_hash: str,
    authority: str,
) -> dict[str, Any]:
    return {
        "schema": HISTORY_SCHEMA,
        "sequence": sequence,
        "operator": operator,
        "arguments": list(arguments),
        "prior_state_hash": prior_state_hash,
        "result_state_hash": result_state_hash,
        "prior_history_hash": prior_history_hash,
        "operator_contract_hash": contract_hash,
        "engine_contract_hash": ENGINE_CONTRACT_HASH,
        "frozen_source_hashes": dict(FROZEN_SOURCE_HASHES),
        "authority": authority,
    }


@dataclass(frozen=True, slots=True)
class SLCHistoryRecord:
    """One immutable, hash-chained formal operator receipt."""

    sequence: int
    operator: str
    arguments: tuple[int, ...]
    prior_state_hash: str
    result_state_hash: str
    prior_history_hash: str
    operator_contract_hash: str
    authority: str
    receipt_hash: str

    @classmethod
    def build(
        cls,
        *,
        sequence: int,
        operator: str,
        arguments: Sequence[int],
        prior_state_hash: str,
        result_state_hash: str,
        prior_history_hash: str,
    ) -> "SLCHistoryRecord":
        arguments_tuple = tuple(arguments)
        contract_hash = operator_contract_hash(operator)
        material = _history_record_material(
            sequence=sequence,
            operator=operator,
            arguments=arguments_tuple,
            prior_state_hash=prior_state_hash,
            result_state_hash=result_state_hash,
            prior_history_hash=prior_history_hash,
            contract_hash=contract_hash,
            authority=FORMAL_AUTHORITY,
        )
        return cls(
            sequence=sequence,
            operator=operator,
            arguments=arguments_tuple,
            prior_state_hash=prior_state_hash,
            result_state_hash=result_state_hash,
            prior_history_hash=prior_history_hash,
            operator_contract_hash=contract_hash,
            authority=FORMAL_AUTHORITY,
            receipt_hash=_canonical_hash(material),
        )

    def __post_init__(self) -> None:
        if type(self.sequence) is not int or self.sequence < 1:
            raise SLCStateCustodyError("history sequence must be a positive integer")
        if not isinstance(self.operator, str) or not self.operator:
            raise SLCStateCustodyError("history operator must be a non-empty string")
        if not isinstance(self.arguments, tuple) or any(type(arg) is not int for arg in self.arguments):
            raise SLCStateCustodyError("history arguments must be an immutable tuple of integers")
        if self.authority != FORMAL_AUTHORITY:
            raise SLCStateCustodyError(
                f"history authority must remain {FORMAL_AUTHORITY!r}; got {self.authority!r}"
            )
        for label, digest in (
            ("prior_state_hash", self.prior_state_hash),
            ("result_state_hash", self.result_state_hash),
            ("prior_history_hash", self.prior_history_hash),
            ("operator_contract_hash", self.operator_contract_hash),
            ("receipt_hash", self.receipt_hash),
        ):
            if not isinstance(digest, str) or len(digest) != 64:
                raise SLCStateCustodyError(f"{label} must be a 64-character SHA-256 digest")
        self.verify()

    def verify(self) -> bool:
        expected_contract = operator_contract_hash(self.operator)
        if self.operator_contract_hash != expected_contract:
            raise SLCStateCustodyError(
                f"operator contract hash mismatch at history sequence {self.sequence}"
            )
        _validate_history_arguments(self.operator, self.arguments)
        material = _history_record_material(
            sequence=self.sequence,
            operator=self.operator,
            arguments=self.arguments,
            prior_state_hash=self.prior_state_hash,
            result_state_hash=self.result_state_hash,
            prior_history_hash=self.prior_history_hash,
            contract_hash=self.operator_contract_hash,
            authority=self.authority,
        )
        expected_receipt = _canonical_hash(material)
        if self.receipt_hash != expected_receipt:
            raise SLCStateCustodyError(
                f"history receipt hash mismatch at sequence {self.sequence}"
            )
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "operator": self.operator,
            "arguments": list(self.arguments),
            "prior_state_hash": self.prior_state_hash,
            "result_state_hash": self.result_state_hash,
            "prior_history_hash": self.prior_history_hash,
            "operator_contract_hash": self.operator_contract_hash,
            "frozen_source_hashes": dict(FROZEN_SOURCE_HASHES),
            "authority": self.authority,
            "receipt_hash": self.receipt_hash,
        }


def _validate_history_arguments(operator: str, arguments: Sequence[int]) -> None:
    contract = _plain_contract(operator)
    if len(arguments) != contract["arity"]:
        raise SLCStateCustodyError(
            f"{operator} history arity must be {contract['arity']}; got {len(arguments)}"
        )
    try:
        sites = tuple(_validate_site(site) for site in arguments)
    except SLCSiteRangeError as exc:
        raise SLCStateCustodyError(str(exc)) from exc
    if operator == "SLC_X1_RESPONSE" and sites[0] == sites[1]:
        raise SLCStateCustodyError("X1 response history aliases control and target")


def _replay_transition(
    coefficients: Sequence[tuple[int, int]],
    sqrt2_power: int,
    operator: str,
    arguments: Sequence[int],
) -> tuple[tuple[tuple[int, int], ...], int]:
    """Replay one receipt without consulting or constructing route history."""

    _validate_history_arguments(operator, arguments)
    if operator == "SLC_ZERO_REGISTER":
        return ((0, 1),), 0
    if operator == "SLC_BINARY_FLIP":
        mask = 1 << arguments[0]
        return _canonicalize_sparse(
            {index ^ mask: coefficient for index, coefficient in coefficients},
            sqrt2_power,
        )
    if operator == "SLC_PREPARE_REQUEST":
        mask = 1 << arguments[0]
        transformed: dict[int, int] = {}
        for index, coefficient in coefficients:
            if index & mask:
                zero_index = index & ~mask
                transformed[zero_index] = transformed.get(zero_index, 0) + coefficient
                transformed[index] = transformed.get(index, 0) - coefficient
            else:
                one_index = index | mask
                transformed[index] = transformed.get(index, 0) + coefficient
                transformed[one_index] = transformed.get(one_index, 0) + coefficient
        return _canonicalize_sparse(transformed, sqrt2_power + 1)
    if operator == "SLC_X1_RESPONSE":
        control, target = arguments
        control_mask = 1 << control
        target_mask = 1 << target
        return _canonicalize_sparse(
            {
                (index ^ target_mask) if index & control_mask else index: coefficient
                for index, coefficient in coefficients
            },
            sqrt2_power,
        )
    raise SLCStateCustodyError(f"cannot replay unknown operator {operator!r}")


@dataclass(frozen=True, slots=True)
class ExactSLCState:
    """A normalized, canonical, immutable twelve-lebit real state."""

    coefficients: tuple[tuple[int, int], ...]
    sqrt2_power: int
    history: tuple[SLCHistoryRecord, ...] = ()

    def __post_init__(self) -> None:
        canonical, power = _canonicalize_sparse(self.coefficients, self.sqrt2_power)
        object.__setattr__(self, "coefficients", canonical)
        object.__setattr__(self, "sqrt2_power", power)
        if not isinstance(self.history, tuple):
            raise SLCStateCustodyError("route history must be an immutable tuple")
        if any(not isinstance(record, SLCHistoryRecord) for record in self.history):
            raise SLCStateCustodyError("route history contains a non-SLCHistoryRecord value")
        self.assert_exact_normalization()
        self.verify_custody()

    @classmethod
    def from_sparse(
        cls,
        coefficients: Mapping[int, int] | Iterable[tuple[int, int]],
        sqrt2_power: int,
    ) -> "ExactSLCState":
        """Create a normalized root state with a fresh custody genesis."""

        canonical, power = _canonicalize_sparse(coefficients, sqrt2_power)
        return cls(canonical, power, ())

    @property
    def register_size(self) -> int:
        return REGISTER_SIZE

    @property
    def dimension(self) -> int:
        return DIMENSION

    @property
    def state_hash(self) -> str:
        """Hash canonical amplitudes only; route history is intentionally excluded."""

        return _state_hash(self.coefficients, self.sqrt2_power)

    @property
    def history_hash(self) -> str:
        """Hash the ordered route; equal terminal states may have different values."""

        if self.history:
            return self.history[-1].receipt_hash
        return _history_genesis_hash(self.state_hash)

    @property
    def support_size(self) -> int:
        return len(self.coefficients)

    @property
    def normalization_numerator(self) -> int:
        return sum(coefficient * coefficient for _, coefficient in self.coefficients)

    @property
    def normalization_denominator(self) -> int:
        return 1 << self.sqrt2_power

    def assert_exact_normalization(self) -> bool:
        numerator = self.normalization_numerator
        denominator = self.normalization_denominator
        if numerator != denominator:
            raise SLCStateInvariantError(
                "state is not exactly normalized: "
                f"sum(coeff^2)={numerator}, expected 2^{self.sqrt2_power}={denominator}"
            )
        return True

    def verify_custody(self) -> bool:
        if not self.history:
            return True

        previous: SLCHistoryRecord | None = None
        for expected_sequence, record in enumerate(self.history, start=1):
            record.verify()
            if record.sequence != expected_sequence:
                raise SLCStateCustodyError(
                    f"history sequence discontinuity: expected {expected_sequence}, got {record.sequence}"
                )
            if previous is None:
                expected_prior_history = _history_genesis_hash(record.prior_state_hash)
            else:
                if record.prior_state_hash != previous.result_state_hash:
                    raise SLCStateCustodyError(
                        f"state-hash chain break at history sequence {record.sequence}"
                    )
                expected_prior_history = previous.receipt_hash
            if record.prior_history_hash != expected_prior_history:
                raise SLCStateCustodyError(
                    f"history-hash chain break at history sequence {record.sequence}"
                )
            previous = record

        if self.history[-1].result_state_hash != self.state_hash:
            raise SLCStateCustodyError("terminal history receipt does not match the terminal state")

        # Language-produced states always begin with the deterministic zero
        # constructor. Replaying every later receipt turns the hash chain into
        # executable custody: a re-hashed but false transition still fails.
        if self.history[0].operator == "SLC_ZERO_REGISTER":
            replay_coefficients: tuple[tuple[int, int], ...] = ((0, 1),)
            replay_power = 0
            for record in self.history:
                replay_prior_hash = _state_hash(replay_coefficients, replay_power)
                if record.prior_state_hash != replay_prior_hash:
                    raise SLCStateCustodyError(
                        f"replayed prior state mismatch at history sequence {record.sequence}"
                    )
                replay_coefficients, replay_power = _replay_transition(
                    replay_coefficients,
                    replay_power,
                    record.operator,
                    record.arguments,
                )
                replay_result_hash = _state_hash(replay_coefficients, replay_power)
                if record.result_state_hash != replay_result_hash:
                    raise SLCStateCustodyError(
                        f"replayed result state mismatch at history sequence {record.sequence}"
                    )
            if replay_coefficients != self.coefficients or replay_power != self.sqrt2_power:
                raise SLCStateCustodyError("replayed route does not reproduce the terminal amplitudes")
        return True

    @property
    def has_replayable_zero_origin_custody(self) -> bool:
        return bool(self.history and self.history[0].operator == "SLC_ZERO_REGISTER")

    def require_replayable_zero_origin_custody(self) -> bool:
        self.verify_custody()
        if not self.has_replayable_zero_origin_custody:
            raise SLCStateCustodyError(
                "SAM Language states must descend from SLC_ZERO_REGISTER; "
                "historyless basis states are diagnostic-only"
            )
        return True

    def coefficient(self, basis_index: int) -> int:
        basis_index = _validate_basis_index(basis_index)
        return dict(self.coefficients).get(basis_index, 0)

    def inspect(self, *, include_coefficients: bool = True) -> dict[str, Any]:
        return inspect_state(self, include_coefficients=include_coefficients)


SLCState12 = ExactSLCState


def _require_state(state: Any) -> ExactSLCState:
    if not isinstance(state, ExactSLCState):
        raise SLCStateInvariantError(
            f"expected ExactSLCState, got {type(state).__name__}"
        )
    state.assert_exact_normalization()
    state.verify_custody()
    return state


def _append_result(
    prior: ExactSLCState,
    *,
    operator: str,
    arguments: Sequence[int],
    coefficients: Mapping[int, int] | Iterable[tuple[int, int]],
    sqrt2_power: int,
) -> ExactSLCState:
    canonical, power = _canonicalize_sparse(coefficients, sqrt2_power)
    normalization = sum(coefficient * coefficient for _, coefficient in canonical)
    if normalization != 1 << power:
        raise SLCStateInvariantError(
            f"{operator} produced a non-normalized state: {normalization} != {1 << power}"
        )
    result_hash = _state_hash(canonical, power)
    record = SLCHistoryRecord.build(
        sequence=len(prior.history) + 1,
        operator=operator,
        arguments=arguments,
        prior_state_hash=prior.state_hash,
        result_state_hash=result_hash,
        prior_history_hash=prior.history_hash,
    )
    return ExactSLCState(canonical, power, prior.history + (record,))


def zero_state(*, register_size: int = REGISTER_SIZE) -> ExactSLCState:
    """Return |0>^12.  Other arities are intentionally not inferred."""

    if type(register_size) is not int or register_size != REGISTER_SIZE:
        raise SLCRegisterArityError(
            f"the frozen C1 register has exactly {REGISTER_SIZE} sites; got {register_size!r}"
        )
    coefficients = ((0, 1),)
    state_hash = _state_hash(coefficients, 0)
    genesis_hash = _history_genesis_hash(state_hash)
    record = SLCHistoryRecord.build(
        sequence=1,
        operator="SLC_ZERO_REGISTER",
        arguments=(),
        prior_state_hash=state_hash,
        result_state_hash=state_hash,
        prior_history_hash=genesis_hash,
    )
    return ExactSLCState(coefficients, 0, (record,))


def basis_state(basis_index: int, *, register_size: int = REGISTER_SIZE) -> ExactSLCState:
    """Return one normalized computational basis state as an independent root."""

    if type(register_size) is not int or register_size != REGISTER_SIZE:
        raise SLCRegisterArityError(
            f"the frozen C1 register has exactly {REGISTER_SIZE} sites; got {register_size!r}"
        )
    basis_index = _validate_basis_index(basis_index)
    return ExactSLCState(((basis_index, 1),), 0, ())


def binary_flip(state: ExactSLCState, site: int) -> ExactSLCState:
    """Apply the SLC binary B transform (X) to one formal site."""

    state = _require_state(state)
    site = _validate_site(site)
    mask = 1 << site
    transformed = {index ^ mask: coefficient for index, coefficient in state.coefficients}
    return _append_result(
        state,
        operator="SLC_BINARY_FLIP",
        arguments=(site,),
        coefficients=transformed,
        sqrt2_power=state.sqrt2_power,
    )


def prepare_request(state: ExactSLCState, site: int) -> ExactSLCState:
    """Apply the exact real balanced PREPARE_REQUEST transform (H)."""

    state = _require_state(state)
    site = _validate_site(site)
    mask = 1 << site
    transformed: dict[int, int] = {}
    for index, coefficient in state.coefficients:
        if index & mask:
            zero_index = index & ~mask
            transformed[zero_index] = transformed.get(zero_index, 0) + coefficient
            transformed[index] = transformed.get(index, 0) - coefficient
        else:
            one_index = index | mask
            transformed[index] = transformed.get(index, 0) + coefficient
            transformed[one_index] = transformed.get(one_index, 0) + coefficient
    return _append_result(
        state,
        operator="SLC_PREPARE_REQUEST",
        arguments=(site,),
        coefficients=transformed,
        sqrt2_power=state.sqrt2_power + 1,
    )


def x1_response(state: ExactSLCState, control: int, target: int) -> ExactSLCState:
    """Apply ordered X1_RESPONSE without asserting a physical edge."""

    state = _require_state(state)
    control = _validate_site(control)
    target = _validate_site(target)
    if control == target:
        raise SLCControlTargetAliasError(
            f"X1 response control and target must be distinct; both were L{control}"
        )
    control_mask = 1 << control
    target_mask = 1 << target
    transformed = {
        (index ^ target_mask) if index & control_mask else index: coefficient
        for index, coefficient in state.coefficients
    }
    return _append_result(
        state,
        operator="SLC_X1_RESPONSE",
        arguments=(control, target),
        coefficients=transformed,
        sqrt2_power=state.sqrt2_power,
    )


def _fraction_payload(numerator: int, denominator: int) -> dict[str, int | str]:
    value = Fraction(numerator, denominator)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": f"{value.numerator}/{value.denominator}",
    }


def _basis_bits(index: int) -> str:
    return format(index, f"0{REGISTER_SIZE}b")


def _project_bits(index: int, sites: Sequence[int]) -> int:
    projected = 0
    for position, site in enumerate(sites):
        projected |= ((index >> site) & 1) << position
    return projected


def _project_display(pattern: int, sites: Sequence[int]) -> str:
    # The string order follows the listed ascending site order, not integer
    # display order; the explicit site list accompanies it in inspection data.
    return "".join(str((pattern >> position) & 1) for position in range(len(sites)))


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        return True

    def components(self) -> list[list[int]]:
        grouped: dict[int, list[int]] = {}
        for value in range(len(self.parent)):
            grouped.setdefault(self.find(value), []).append(value)
        return sorted((sorted(group) for group in grouped.values()), key=lambda group: group[0])


def _rank_one_across_partition(
    state: ExactSLCState,
    sites: Sequence[int],
) -> bool:
    site_set = set(sites)
    rest = [site for site in range(REGISTER_SIZE) if site not in site_set]
    matrix: dict[tuple[int, int], int] = {}
    row_values: set[int] = set()
    column_values: set[int] = set()
    for index, coefficient in state.coefficients:
        row = _project_bits(index, sites)
        column = _project_bits(index, rest)
        matrix[(row, column)] = coefficient
        row_values.add(row)
        column_values.add(column)

    pivot_key = next((key for key, coefficient in matrix.items() if coefficient), None)
    if pivot_key is None:
        return False
    pivot_row, pivot_column = pivot_key
    pivot = matrix[pivot_key]
    for row in row_values:
        for column in column_values:
            value = matrix.get((row, column), 0)
            row_pivot = matrix.get((row, pivot_column), 0)
            column_pivot = matrix.get((pivot_row, column), 0)
            if value * pivot != row_pivot * column_pivot:
                return False
    return True


def _component_relative_sign(state: ExactSLCState, sites: Sequence[int], patterns: Sequence[int]) -> str:
    if len(patterns) != 2:
        return "UNRESOLVED"
    site_set = set(sites)
    rest = [site for site in range(REGISTER_SIZE) if site not in site_set]
    rows: dict[int, dict[int, int]] = {patterns[0]: {}, patterns[1]: {}}
    for index, coefficient in state.coefficients:
        row = _project_bits(index, sites)
        if row in rows:
            rows[row][_project_bits(index, rest)] = coefficient
    for column in sorted(set(rows[patterns[0]]) | set(rows[patterns[1]])):
        left = rows[patterns[0]].get(column, 0)
        right = rows[patterns[1]].get(column, 0)
        if left and right:
            return "PLUS" if left * right > 0 else "MINUS"
    return "UNRESOLVED"


def _state_topology(state: ExactSLCState) -> dict[str, Any]:
    support_indices = [index for index, _ in state.coefficients]
    weights = {index: coefficient * coefficient for index, coefficient in state.coefficients}
    total_weight = state.normalization_denominator

    marginals: list[dict[str, Any]] = []
    varies: list[bool] = []
    for site in range(REGISTER_SIZE):
        weight_one = sum(weight for index, weight in weights.items() if index & (1 << site))
        weight_zero = total_weight - weight_one
        site_varies = weight_zero > 0 and weight_one > 0
        varies.append(site_varies)
        if weight_one == 0:
            status = "FIXED_0"
        elif weight_zero == 0:
            status = "FIXED_1"
        elif weight_zero == weight_one:
            status = "BALANCED"
        else:
            status = "UNBALANCED"
        marginals.append(
            {
                "site": site,
                "label": f"L{site}",
                "status": status,
                "p0": _fraction_payload(weight_zero, total_weight),
                "p1": _fraction_payload(weight_one, total_weight),
            }
        )

    relation_union = _UnionFind(REGISTER_SIZE)
    relations: list[dict[str, Any]] = []
    for left in range(REGISTER_SIZE):
        for right in range(left + 1, REGISTER_SIZE):
            if not (varies[left] and varies[right]):
                continue
            xor_values = {
                ((index >> left) & 1) ^ ((index >> right) & 1)
                for index in support_indices
            }
            if len(xor_values) == 1:
                xor_value = next(iter(xor_values))
                relation_union.union(left, right)
                relations.append(
                    {
                        "left": left,
                        "right": right,
                        "relation": "SAME" if xor_value == 0 else "OPPOSITE",
                        "exact": True,
                    }
                )

    components_payload: list[dict[str, Any]] = []
    ghz_like_count = 0
    for component in relation_union.components():
        pattern_weights: dict[int, int] = {}
        for index, weight in weights.items():
            pattern = _project_bits(index, component)
            pattern_weights[pattern] = pattern_weights.get(pattern, 0) + weight
        patterns = sorted(pattern_weights)
        complement_mask = (1 << len(component)) - 1
        complement_pair = (
            len(patterns) == 2 and (patterns[0] ^ complement_mask) == patterns[1]
        )
        equal_weight = (
            len(patterns) == 2 and pattern_weights[patterns[0]] == pattern_weights[patterns[1]]
        )
        separable = _rank_one_across_partition(state, component)
        ghz_like = len(component) >= 2 and complement_pair and equal_weight and separable
        if ghz_like:
            ghz_like_count += 1
            kind = "GHZ_LIKE_EXACT_REAL_COMPONENT"
        elif len(component) == 1:
            kind = marginals[component[0]]["status"] + "_SINGLE_SITE"
        else:
            kind = "EXACT_PARITY_RELATED_COMPONENT"
        components_payload.append(
            {
                "sites": component,
                "labels": [f"L{site}" for site in component],
                "kind": kind,
                "patterns": [
                    {
                        "site_order_bits": _project_display(pattern, component),
                        "weight": _fraction_payload(pattern_weights[pattern], total_weight),
                    }
                    for pattern in patterns
                ],
                "complement_pair": complement_pair,
                "equal_weight": equal_weight,
                "separable_from_rest": separable,
                "ghz_like": ghz_like,
                "relative_real_sign": (
                    _component_relative_sign(state, component, patterns)
                    if ghz_like
                    else "UNRESOLVED"
                ),
            }
        )

    return {
        "basis_marginals": marginals,
        "exact_pair_relations": relations,
        "component_partition": [component["sites"] for component in components_payload],
        "components": components_payload,
        "ghz_like_component_count": ghz_like_count,
        "classification_boundary": (
            "GHZ-like means an exact equal-weight complementary real component "
            "that factorizes from the rest; it is not a physical-connectivity claim."
        ),
    }


def _route_topology(state: ExactSLCState) -> dict[str, Any]:
    route_union = _UnionFind(REGISTER_SIZE)
    response_edges: list[dict[str, int]] = []
    cycle_receipts: list[int] = []
    invalid_forest_steps: list[dict[str, Any]] = []
    reached: set[int] = set()
    roots: list[int] = []
    for record in state.history:
        if record.operator == "SLC_ZERO_REGISTER":
            continue
        if record.operator == "SLC_PREPARE_REQUEST":
            site = record.arguments[0]
            if site in reached:
                invalid_forest_steps.append(
                    {
                        "sequence": record.sequence,
                        "reason": "PREPARE_ON_ALREADY_REACHED_SITE",
                        "site": site,
                    }
                )
            else:
                reached.add(site)
                roots.append(site)
            continue
        if record.operator == "SLC_BINARY_FLIP":
            invalid_forest_steps.append(
                {
                    "sequence": record.sequence,
                    "reason": "BINARY_FLIP_IS_NOT_A_ROOTED_FOREST_PRODUCTION",
                    "site": record.arguments[0],
                }
            )
            continue
        if record.operator != "SLC_X1_RESPONSE":
            invalid_forest_steps.append(
                {"sequence": record.sequence, "reason": "UNKNOWN_FOREST_OPERATOR"}
            )
            continue
        control, target = record.arguments
        response_edges.append(
            {"sequence": record.sequence, "control": control, "target": target}
        )
        step_valid = True
        if control not in reached:
            invalid_forest_steps.append(
                {
                    "sequence": record.sequence,
                    "reason": "CONTROL_NOT_REACHED_BEFORE_RESPONSE",
                    "control": control,
                    "target": target,
                }
            )
            step_valid = False
        if target in reached:
            invalid_forest_steps.append(
                {
                    "sequence": record.sequence,
                    "reason": "TARGET_ALREADY_REACHED_BEFORE_RESPONSE",
                    "control": control,
                    "target": target,
                }
            )
            step_valid = False
        if step_valid:
            reached.add(target)
        if not route_union.union(control, target):
            cycle_receipts.append(record.sequence)
    unique_undirected = {
        (min(edge["control"], edge["target"]), max(edge["control"], edge["target"]))
        for edge in response_edges
    }
    return {
        "ordered_response_edges": response_edges,
        "response_edge_count": len(response_edges),
        "unique_undirected_edge_count": len(unique_undirected),
        "components": route_union.components(),
        "root_sites": roots,
        "reached_sites": sorted(reached),
        "is_parent_before_child_forest_prefix": not invalid_forest_steps,
        "is_complete_rooted_forest_history": (
            not invalid_forest_steps and reached == set(range(REGISTER_SIZE))
        ),
        "is_rooted_forest_history": (
            not invalid_forest_steps and reached == set(range(REGISTER_SIZE))
        ),
        "invalid_forest_steps": invalid_forest_steps,
        "cycle_or_repeat_receipt_sequences": cycle_receipts,
        "boundary": (
            "forest status validates root preparation and parent-before-child reachability; "
            "route edges remain formal operator history, not physical connectivity"
        ),
    }


def inspect_state(
    state: ExactSLCState,
    *,
    include_coefficients: bool = True,
) -> dict[str, Any]:
    """Return an exact, deterministic, JSON-ready state and route dossier."""

    state = _require_state(state)
    payload: dict[str, Any] = {
        "schema": STATE_SCHEMA,
        "authority": FORMAL_AUTHORITY,
        "register_size": REGISTER_SIZE,
        "dimension": DIMENSION,
        "support_size": state.support_size,
        "sqrt2_power": state.sqrt2_power,
        "common_denominator": (
            "1" if state.sqrt2_power == 0 else f"sqrt(2)^{state.sqrt2_power}"
        ),
        "normalization": {
            "sum_coefficient_squares": state.normalization_numerator,
            "expected_power_of_two": state.normalization_denominator,
            "exact": True,
        },
        "state_hash": state.state_hash,
        "history_hash": state.history_hash,
        "state_and_history_hashes_are_separate": state.state_hash != state.history_hash,
        "history_length": len(state.history),
        "custody": {
            "hash_chain_verified": True,
            "zero_origin_transition_replay_verified": state.has_replayable_zero_origin_custody,
            "class": (
                "SEALED_ZERO_ORIGIN_REPLAYED"
                if state.has_replayable_zero_origin_custody
                else "DIAGNOSTIC_ROOT_HASH_CHAIN_ONLY"
            ),
        },
        "engine_contract_hash": ENGINE_CONTRACT_HASH,
        "operator_contract_hashes": dict(OPERATOR_CONTRACT_HASHES),
        "frozen_source_hashes": dict(FROZEN_SOURCE_HASHES),
        "history": [record.to_dict() for record in state.history],
        "state_topology": _state_topology(state),
        "route_topology": _route_topology(state),
        "open_boundaries": [
            "complex_phase",
            "publication_born_readout",
            "physical_connectivity",
            "hardware_cost",
        ],
    }
    if include_coefficients:
        payload["coefficients"] = [
            {
                "basis_index": index,
                "bits_L11_to_L0": _basis_bits(index),
                "coefficient": coefficient,
                "amplitude_exact": (
                    str(coefficient)
                    if state.sqrt2_power == 0
                    else f"{coefficient}/sqrt(2)^{state.sqrt2_power}"
                ),
                "probability": _fraction_payload(
                    coefficient * coefficient,
                    state.normalization_denominator,
                ),
            }
            for index, coefficient in state.coefficients
        ]
    return payload


def apply_complex_phase(*_args: Any, **_kwargs: Any) -> None:
    raise SLCUnsupportedPhaseError(
        "the frozen SLC C1 kernel is exact-real; no complex phase operator is registered"
    )


def publish(*_args: Any, **_kwargs: Any) -> None:
    raise SLCUnsupportedPublicationError(
        "publication/Born readout remains outside the frozen formal state kernel"
    )


def sample_measurement(*_args: Any, **_kwargs: Any) -> None:
    raise SLCUnsupportedPublicationError(
        "sampling would require an opened publication/Born rule and is not available"
    )


def assert_physical_connectivity(*_args: Any, **_kwargs: Any) -> None:
    raise SLCUnsupportedConnectivityError(
        "formal site pairs do not independently establish physical connectivity"
    )


# Stable functional names for the language registry and direct Python use.
SLC_ZERO_REGISTER = zero_state
SLC_REGISTER_ZERO = zero_state
SLC_BINARY_FLIP = binary_flip
SLC_PREPARE_REQUEST = prepare_request
SLC_X1_RESPONSE = x1_response
B = binary_flip
PREPARE_REQUEST = prepare_request
X1_RESPONSE = x1_response
ZERO = zero_state()


__all__ = [
    "REGISTER_SIZE",
    "DIMENSION",
    "STATE_SCHEMA",
    "HISTORY_SCHEMA",
    "FORMAL_AUTHORITY",
    "FROZEN_SOURCE_HASHES",
    "ENGINE_CONTRACT_HASH",
    "OPERATOR_CONTRACT_HASHES",
    "SLCRegisterArityError",
    "SLCSiteRangeError",
    "SLCControlTargetAliasError",
    "SLCStateInvariantError",
    "SLCStateCustodyError",
    "SLCUnsupportedPhaseError",
    "SLCUnsupportedPublicationError",
    "SLCUnsupportedConnectivityError",
    "SLCHistoryRecord",
    "ExactSLCState",
    "SLCState12",
    "zero_state",
    "basis_state",
    "binary_flip",
    "prepare_request",
    "x1_response",
    "inspect_state",
    "operator_contract_hash",
    "engine_contract_hash",
    "apply_complex_phase",
    "publish",
    "sample_measurement",
    "assert_physical_connectivity",
    "SLC_ZERO_REGISTER",
    "SLC_REGISTER_ZERO",
    "SLC_BINARY_FLIP",
    "SLC_PREPARE_REQUEST",
    "SLC_X1_RESPONSE",
    "B",
    "PREPARE_REQUEST",
    "X1_RESPONSE",
    "ZERO",
]
