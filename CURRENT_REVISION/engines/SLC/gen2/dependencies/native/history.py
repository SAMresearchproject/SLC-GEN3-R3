"""Maintained W8 endpoint state, directed history and explicit action fibers.

The generic record checks caller-supplied before/after states. It does not
invent an exchange dynamics, conservation law or physical endpoint mapping.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Mapping

from .exact import ExactError, digest, fraction, seal, token, vector


@dataclass(frozen=True)
class DirectedWrite:
    source: str
    receiver: str
    source_before: tuple
    source_after: tuple
    receiver_before: tuple
    receiver_after: tuple
    retained_operands: tuple
    action: str

    def __post_init__(self):
        if token(self.source) == token(self.receiver):
            raise ExactError("directed Write endpoints must remain distinct")
        token(self.action)
        for name in ("source_before", "source_after", "receiver_before", "receiver_after",
                     "retained_operands"):
            object.__setattr__(self, name, vector(getattr(self, name)))
        if len(self.source_before) != len(self.source_after) or \
           len(self.receiver_before) != len(self.receiver_after):
            raise ExactError("maintained endpoint dimension changed")


@dataclass(frozen=True)
class RetainedHistory:
    initial_endpoints: tuple
    writes: tuple[DirectedWrite, ...]
    semantic_type: str

    def __post_init__(self):
        token(self.semantic_type)
        endpoints = tuple(sorted((token(name), vector(state))
                                 for name, state in self.initial_endpoints))
        if len(endpoints) < 2 or len({name for name, _ in endpoints}) != len(endpoints):
            raise ExactError("endpoint roster must contain distinct identities")
        object.__setattr__(self, "initial_endpoints", endpoints)
        object.__setattr__(self, "writes", tuple(self.writes))
        self.maintained_state()

    def maintained_state(self) -> tuple:
        states = dict(self.initial_endpoints)
        for write in self.writes:
            if not isinstance(write, DirectedWrite):
                raise ExactError("history contains an untyped Write")
            if states.get(write.source) != write.source_before or \
               states.get(write.receiver) != write.receiver_before:
                raise ExactError("Write does not join the maintained endpoint states")
            states[write.source] = write.source_after
            states[write.receiver] = write.receiver_after
        return tuple(sorted(states.items()))

    def receipt(self) -> dict:
        return seal("Q3_RETAINED_DIRECTED_HISTORY_V1", semantic_type=self.semantic_type,
                    initial_endpoints=self.initial_endpoints, maintained_W8=self.maintained_state(),
                    directed_history=self.writes,
                    maintained_state_sha256=digest(self.maintained_state()),
                    directed_history_sha256=digest(self.writes))


@dataclass(frozen=True)
class ConnectorHistory:
    operands: tuple

    def __post_init__(self):
        values = vector(self.operands)
        if any(value <= 0 for value in values):
            raise ExactError("connector operands must be positive")
        object.__setattr__(self, "operands", values)

    @property
    def terminal(self) -> Fraction:
        return sum(self.operands, Fraction())

    def first_prefix_lift(self) -> Fraction:
        first = self.operands[0]
        return first + first * first / 144

    def symmetric_contact(self) -> Fraction:
        return (self.terminal**2 - sum(value**2 for value in self.operands)) / 144

    def receipt(self) -> dict:
        return seal("Q3_CONNECTOR_HISTORY_V1", ordered_operands=self.operands,
                    terminal=self.terminal, first_prefix_lift=self.first_prefix_lift(),
                    symmetric_contact=self.symmetric_contact(),
                    output_type="CONNECTOR_LIFT_RESPONSE", units="DIMENSIONLESS")


def response_partition(histories, actions: Mapping[str, Callable]) -> dict:
    """Exact response equivalence on this finite roster and these named actions.

    Keys are canonical response bytes, not approximate embeddings. All original
    records and multiplicities are retained for reconstruction.
    """
    from .exact import canonical_bytes, plain
    histories = tuple(histories)
    if not histories or not actions:
        raise ExactError("history and action rosters must be nonempty")
    action_ids = tuple(sorted(token(name) for name in actions))
    members, groups = [], {}
    for ordinal, history in enumerate(histories):
        if not isinstance(history, (RetainedHistory, ConnectorHistory)):
            raise ExactError("partition requires native retained histories")
        responses = {name: plain(actions[name](history)) for name in action_ids}
        key = canonical_bytes(responses)
        members.append({"ordinal": ordinal, "history": history.receipt(), "responses": responses})
        groups.setdefault(key, []).append(ordinal)
    fibers = [{"member_ordinals": ordinals, "responses": members[ordinals[0]]["responses"]}
              for ordinals in groups.values()]
    return seal("Q3_FINITE_ACTION_RESPONSE_PARTITION_V1", action_ids=action_ids,
                members=members, fibers=fibers, member_count=len(members),
                response_class_count=len(fibers), retained_member_count=sum(len(x["member_ordinals"]) for x in fibers),
                scope="DECLARED_FINITE_ROSTER_AND_ACTIONS")
