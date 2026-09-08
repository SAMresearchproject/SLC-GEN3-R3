"""Exact finite encounter transfers with explicit clocks and observation windows.

An arrival frame and maintained source state are separate objects. Empty
arrival ticks contain zero observations; no transition resets W8 here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from .exact import rational, canonical, digest
from .readouts import vec, matrix, matvec, linear_inverse


def _names(values, label):
    result = tuple(values)
    if not result or any(not isinstance(x, str) or not x for x in result) or len(result) != len(set(result)):
        raise ValueError(label + " must be nonempty unique names")
    return result


def _ticks(values):
    result = tuple(values)
    if not result or any(type(x) is not int for x in result) or len(set(result)) != len(result):
        raise ValueError("clock ticks must be distinct integers")
    return result


@dataclass(frozen=True)
class TransferTerm:
    source: str
    receiver: str
    emission_tick: int
    arrival_tick: int
    coefficient: Fraction
    orientation: tuple

    def to_dict(self):
        return canonical({"source": self.source, "receiver": self.receiver,
                          "emission_tick": self.emission_tick, "arrival_tick": self.arrival_tick,
                          "coefficient": self.coefficient, "orientation": self.orientation})


@dataclass(frozen=True)
class EncounterTransfer:
    sources: tuple
    receivers: tuple
    emission_ticks: tuple
    observation_ticks: tuple
    dimension: int
    terms: tuple
    source_unit: str
    coefficient_unit: str
    clock_unit: str
    causal: bool = True
    context: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, source):
        sources = _names(source["sources"], "source ports")
        receivers = _names(source["receivers"], "receiver ports")
        emit = _ticks(source["emission_ticks"])
        observe = _ticks(source["observation_ticks"])
        dimension = source["dimension"]
        if type(dimension) is not int or dimension < 1:
            raise ValueError("encounter dimension must be positive")
        identity = [[int(i == j) for j in range(dimension)] for i in range(dimension)]
        causal = source.get("causal", True)
        if type(causal) is not bool:
            raise ValueError("causal flag must be boolean")
        terms = []
        for term in source["terms"]:
            if term["source"] not in sources or term["receiver"] not in receivers:
                raise ValueError("transfer term uses an undeclared calibrated port")
            e, a = term["emission_tick"], term["arrival_tick"]
            if type(e) is not int or type(a) is not int or e not in emit:
                raise ValueError("transfer term uses an undeclared emission tick")
            if causal and a < e:
                raise ValueError("causal transfer arrives before emission")
            terms.append(TransferTerm(term["source"], term["receiver"], e, a,
                                      rational(term["coefficient"]), matrix(term.get("orientation", identity), dimension, dimension)))
        units = [source.get("source_unit", "NATIVE_RECEIVER_CURRENT"), source.get("coefficient_unit", "DIMENSIONLESS"),
                 source.get("clock_unit", "DECLARED_FIXTURE_TICK")]
        if any(not isinstance(unit, str) or not unit for unit in units):
            raise ValueError("source, coefficient and clock units must be explicit")
        return cls(sources, receivers, emit, observe, dimension, tuple(terms), *units, causal, source.get("context", {}))

    def to_dict(self):
        return canonical({"schema": "GEN2_ENCOUNTER_TRANSFER_V1", "sources": self.sources, "receivers": self.receivers,
                          "emission_ticks": self.emission_ticks, "observation_ticks": self.observation_ticks,
                          "dimension": self.dimension, "terms": [term.to_dict() for term in self.terms],
                          "source_unit": self.source_unit, "coefficient_unit": self.coefficient_unit,
                          "clock_unit": self.clock_unit, "causal": self.causal, "context": self.context})

    @property
    def source_coordinates(self):
        return tuple((source, tick, component) for source in self.sources for tick in self.emission_ticks for component in range(self.dimension))

    @property
    def observation_coordinates(self):
        return tuple((receiver, tick, component) for receiver in self.receivers for tick in self.observation_ticks for component in range(self.dimension))

    def source_vector(self, emissions):
        if set(emissions) != set(self.sources):
            raise ValueError("source emission ports differ from the contract")
        frames = {}
        for source in self.sources:
            ticks = emissions[source]
            if set(map(str, ticks)) != set(map(str, self.emission_ticks)):
                raise ValueError("every declared emission tick needs an explicit frame")
            for tick in self.emission_ticks:
                frame = vec(ticks[str(tick)] if str(tick) in ticks else ticks[tick])
                if len(frame) != self.dimension:
                    raise ValueError("emission frame dimension differs")
                frames[source, tick] = frame
        return tuple(frames[source, tick][component] for source, tick, component in self.source_coordinates)

    def observations_vector(self, observations):
        if set(observations) != set(self.receivers):
            raise ValueError("observed receiver ports differ from the contract")
        frames = {}
        for receiver in self.receivers:
            ticks = observations[receiver]
            if set(map(str, ticks)) != set(map(str, self.observation_ticks)):
                raise ValueError("observation window differs; create the declared reduced-window contract")
            for tick in self.observation_ticks:
                frame = vec(ticks[str(tick)] if str(tick) in ticks else ticks[tick])
                if len(frame) != self.dimension:
                    raise ValueError("observed frame dimension differs")
                frames[receiver, tick] = frame
        return tuple(frames[receiver, tick][component] for receiver, tick, component in self.observation_coordinates)

    def sparse_matrix(self):
        columns = {coordinate: i for i, coordinate in enumerate(self.source_coordinates)}
        rows = {coordinate: i for i, coordinate in enumerate(self.observation_coordinates)}
        entries = {}
        for term in self.terms:
            if term.arrival_tick not in self.observation_ticks:
                continue
            for i, vector in enumerate(term.orientation):
                for j, coefficient in enumerate(vector):
                    if coefficient:
                        key = (rows[term.receiver, term.arrival_tick, i], columns[term.source, term.emission_tick, j])
                        entries[key] = entries.get(key, Fraction()) + term.coefficient * coefficient
        return tuple((i, j, value) for (i, j), value in sorted(entries.items()) if value)

    def dense_matrix(self):
        result = [[Fraction() for _ in self.source_coordinates] for _ in self.observation_coordinates]
        for i, j, value in self.sparse_matrix():
            result[i][j] = value
        return tuple(tuple(row) for row in result)

    def forward(self, emissions):
        x = self.source_vector(emissions)
        y = [Fraction() for _ in self.observation_coordinates]
        for row, column, coefficient in self.sparse_matrix():
            y[row] += coefficient * x[column]
        frames = {receiver: {str(tick): [Fraction()] * self.dimension for tick in self.observation_ticks} for receiver in self.receivers}
        for (receiver, tick, component), value in zip(self.observation_coordinates, y):
            frames[receiver][str(tick)][component] = value
        return canonical({"schema": "GEN2_ENCOUNTER_RESPONSE_V1", "observations": frames,
                          "transfer_sha256": digest(self.to_dict()), "source_unit": self.source_unit,
                          "coefficient_unit": self.coefficient_unit, "clock_unit": self.clock_unit,
                          "maintained_state_transition": "NONE", "unobserved_arrivals":
                          [term.to_dict() for term in self.terms if term.arrival_tick not in self.observation_ticks]})

    def inverse(self, observations, *, domain=None):
        observed = self.observations_vector(observations)
        if domain is None:
            answer = linear_inverse(self.dense_matrix(), observed)
            return canonical({**answer, "source_coordinates": self.source_coordinates,
                              "transfer_sha256": digest(self.to_dict())})
        matches, count = [], 0
        sparse = self.sparse_matrix()
        for member in domain:
            emissions = member.get("emissions", member)
            x = self.source_vector(emissions)
            y = [Fraction() for _ in self.observation_coordinates]
            for row, column, coefficient in sparse:
                y[row] += coefficient * x[column]
            count += 1
            if tuple(y) == observed:
                matches.append(member)
        return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "FINITE_ENCOUNTER_TRANSFER",
                          "complete": True, "unique": len(matches) == 1, "members": matches,
                          "member_count": len(matches), "domain_count": count,
                          "transfer_sha256": digest(self.to_dict()),
                          "provenance_used_as_observation": False})


def tick_fixture(*, dimension=32, emission_ticks=(0, 1), observation_ticks=(0, 1, 2), clock_offset=0):
    """D1 F13c: Y1[t]=HA[t]+HB[t], Y2[t]=HA[t]+2 HB[t-1]."""
    if type(clock_offset) is not int:
        raise ValueError("clock alignment is an explicit integer fixture offset")
    terms = []
    for tick in emission_ticks:
        terms.extend([
            {"source": "A", "receiver": "R1", "emission_tick": tick, "arrival_tick": tick + clock_offset, "coefficient": 1},
            {"source": "B", "receiver": "R1", "emission_tick": tick, "arrival_tick": tick + clock_offset, "coefficient": 1},
            {"source": "A", "receiver": "R2", "emission_tick": tick, "arrival_tick": tick + clock_offset, "coefficient": 1},
            {"source": "B", "receiver": "R2", "emission_tick": tick, "arrival_tick": tick + 1 + clock_offset, "coefficient": 2}])
    return EncounterTransfer.from_dict({"sources": ["A", "B"], "receivers": ["R1", "R2"],
        "emission_ticks": emission_ticks, "observation_ticks": observation_ticks, "dimension": dimension,
        "terms": terms, "causal": clock_offset >= 0, "clock_unit": "DECLARED_FIXTURE_TICK",
        "context": {"law": "D1_F13C", "clock_alignment_offset": clock_offset, "zero_emissions_outside_declared_ticks": True,
                    "physical_propagation_assigned": False}})


def causal_tick_inverse(observations, *, emission_ticks=(0, 1), dimension=32):
    """Exact triangular inverse for the declared aligned, zero-prehistory fixture."""
    if set(observations) != {"R1", "R2"}:
        raise ValueError("causal fixture requires R1 and R2")
    if tuple(emission_ticks) != tuple(range(len(emission_ticks))):
        raise ValueError("causal fixture emission ticks start at zero and are contiguous")
    result = {"A": {}, "B": {}}
    previous_b = (Fraction(),) * dimension
    for tick in emission_ticks:
        if str(tick) not in observations["R1"] or str(tick) not in observations["R2"]:
            raise ValueError("causal inverse requires both receivers at every emission tick")
        y1, y2 = vec(observations["R1"][str(tick)]), vec(observations["R2"][str(tick)])
        if len(y1) != dimension or len(y2) != dimension:
            raise ValueError("causal frame dimension differs")
        a = tuple(y - 2 * old for y, old in zip(y2, previous_b))
        b = tuple(y - source for y, source in zip(y1, a))
        result["A"][str(tick)], result["B"][str(tick)] = a, b
        previous_b = b
    if set(observations["R1"]) != set(observations["R2"]):
        raise ValueError("receiver windows differ")
    observed_ticks = tuple(sorted(int(tick) for tick in observations["R1"]))
    contract = tick_fixture(dimension=dimension, emission_ticks=emission_ticks, observation_ticks=observed_ticks)
    replay = contract.forward(result)["observations"]
    if replay != canonical(observations):
        return {"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "CAUSAL_TICK_ANALYTIC", "complete": True,
                "unique": False, "member_count": 0, "members": []}
    return canonical({"schema": "GEN2_JOINT_ANSWER_V1", "strategy": "CAUSAL_TICK_ANALYTIC", "complete": True,
                      "unique": True, "member_count": 1, "members": [result], "all_supplied_ticks_checked": True})


def _dispatch_base(operation, payload):
    operation = operation.removeprefix("GEN2_")
    if operation not in ("ENCOUNTER", "ENCOUNTER_INVERSE"):
        raise ValueError("unsupported GEN2 encounter operation")
    source = payload.get("source")
    contract = EncounterTransfer.from_dict(source) if source is not None else tick_fixture(
        dimension=payload.get("dimension", 32), emission_ticks=tuple(payload.get("emission_ticks", (0, 1))),
        observation_ticks=tuple(payload.get("observation_ticks", (0, 1, 2))), clock_offset=payload.get("clock_offset", 0))
    if operation == "ENCOUNTER_INVERSE" or "observations" in payload:
        if payload.get("strategy") == "causal":
            if contract.context.get("law") != "D1_F13C" or contract.context.get("clock_alignment_offset") != 0:
                raise ValueError("causal inverse only applies to its bound aligned tick fixture")
            return causal_tick_inverse(payload["observations"], emission_ticks=contract.emission_ticks, dimension=contract.dimension)
        return contract.inverse(payload["observations"], domain=payload.get("domain"))
    return contract.forward(payload["emissions"])


def dispatch(operation, payload, *, log_class=None):
    from .motion_adapters import encounter_geometry
    from .boundary_information import register_ordinary
    return register_ordinary(operation, payload,
                             encounter_geometry(operation, payload, _dispatch_base(operation, payload), log_class=log_class))
