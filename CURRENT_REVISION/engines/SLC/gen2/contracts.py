"""Finite source declarations for the reusable T18 construction compiler."""
from dataclasses import dataclass
from itertools import product
from .exact import canonical, digest, rational


@dataclass(frozen=True)
class Event:
    label: str
    coordinate: int
    direction: int
    admitted_states: tuple | None = None

    def to_dict(self):
        out = {'label': self.label, 'coordinate': self.coordinate,
               'direction': self.direction}
        if self.admitted_states is not None:
            out['admitted_states'] = [list(q) for q in self.admitted_states]
        return out


@dataclass(frozen=True)
class Receiver:
    name: str
    coordinates: tuple
    matrix: tuple

    def to_dict(self):
        return canonical({'name': self.name, 'coordinates': self.coordinates,
                          'matrix': self.matrix})


@dataclass(frozen=True)
class SourceContract:
    name: str
    coordinates: tuple
    events: tuple
    receivers: tuple
    states: tuple | None = None
    contact_coordinates: tuple | None = None
    source_binding: str = 'NATIVE_T18_J4_H980'
    units: str = 'native_receiver_integer'
    motion_profile: dict | None = None

    def __post_init__(self):
        object.__setattr__(self, 'events', tuple(sorted(self.events, key=lambda e: e.label)))
        if self.states is not None:
            object.__setattr__(self, 'states', tuple(sorted(self.states)))
        if not self.coordinates or len(set(self.coordinates)) != len(self.coordinates):
            raise ValueError('Coordinates must be nonempty and unique')
        if any(type(c) is not int or not 0 <= c < 9 for c in self.coordinates):
            raise ValueError('T18 coordinates must be record indices 0 through 8')
        if len({e.label for e in self.events}) != len(self.events):
            raise ValueError('Event labels must be unique; equal actions may have distinct labels')
        for event in self.events:
            if type(event.label) is not str or not event.label or type(event.coordinate) is not int or event.coordinate not in self.coordinates or type(event.direction) is not int or event.direction not in (-1, 1):
                raise ValueError('Invalid declared event')
            if event.admitted_states is not None:
                for q in event.admitted_states:
                    self.admit_state(q)
        if not self.receivers or len({r.name for r in self.receivers}) != len(self.receivers):
            raise ValueError('Receivers must be nonempty with distinct names')
        for rec in self.receivers:
            if not rec.coordinates or len(set(rec.coordinates)) != len(rec.coordinates):
                raise ValueError('Receiver coordinate list must be nonempty and unique')
            if any(c not in self.coordinates for c in rec.coordinates):
                raise ValueError('Receiver reads an undeclared coordinate')
            if not rec.matrix or any(len(row) != 2 * len(rec.coordinates) for row in rec.matrix):
                raise ValueError('Receiver matrix must read real and imaginary source coordinates')
        if self.states is not None:
            if not self.states or len(set(self.states)) != len(self.states):
                raise ValueError('Declared state domain must be nonempty and unique')
            for q in self.states:
                self.admit_state(q)
        if self.contact_coordinates is not None:
            if len(self.contact_coordinates) != 3 or any(c not in self.coordinates for c in self.contact_coordinates):
                raise ValueError('Contact needs three admitted coordinates')
        if self.motion_profile is not None:
            if not isinstance(self.motion_profile, dict):
                raise ValueError('Optional motion profile must be a source declaration object')
            object.__setattr__(self, 'motion_profile', canonical(self.motion_profile))

    def admit_state(self, q):
        q = tuple(q)
        if len(q) != len(self.coordinates) or any(type(v) is not int or not 0 <= v < 4 for v in q):
            raise ValueError('State must contain one Z4 value per declared coordinate')
        return q

    def domain(self):
        return self.states if self.states is not None else product(range(4), repeat=len(self.coordinates))

    @property
    def contract_id(self):
        return digest(self.to_dict())

    def to_dict(self):
        result = canonical({'schema': 'SLC_GEN2_SOURCE_V1', 'name': self.name,
                          'coordinates': self.coordinates,
                          'events': [e.to_dict() for e in self.events],
                          'receivers': [r.to_dict() for r in self.receivers],
                          'states': self.states,
                          'contact_coordinates': self.contact_coordinates,
                          'source_binding': self.source_binding, 'units': self.units})
        if self.motion_profile is not None:
            result['motion_profile'] = canonical(self.motion_profile)
        return result

    @classmethod
    def from_dict(cls, spec):
        allowed = {'schema', 'name', 'coordinates', 'events', 'receivers', 'states',
                   'contact_coordinates', 'source_binding', 'units', 'motion_profile'}
        if set(spec) - allowed:
            raise ValueError('Undeclared source fields: ' + str(sorted(set(spec) - allowed)))
        if spec.get('schema', 'SLC_GEN2_SOURCE_V1') != 'SLC_GEN2_SOURCE_V1':
            raise ValueError('Unsupported source schema')
        coords = tuple(spec['coordinates'])
        events = []
        for e in spec['events']:
            if set(e) - {'label', 'coordinate', 'direction', 'admitted_states'}:
                raise ValueError('Undeclared event fields')
            admitted = e.get('admitted_states')
            events.append(Event(e['label'], e['coordinate'], e['direction'],
                                None if admitted is None else tuple(sorted(tuple(q) for q in admitted))))
        receivers = []
        for r in spec['receivers']:
            if set(r) != {'name', 'coordinates', 'matrix'}:
                raise ValueError('Receiver fields must be name, coordinates, matrix')
            receivers.append(Receiver(r['name'], tuple(r['coordinates']),
                                      tuple(tuple(rational(x) for x in row) for row in r['matrix'])))
        states = spec.get('states')
        contact = spec.get('contact_coordinates')
        return cls(spec.get('name', 'declared-native-source'), coords,
                   tuple(sorted(events, key=lambda e: e.label)), tuple(receivers),
                   None if states is None else tuple(sorted(tuple(q) for q in states)),
                   None if contact is None else tuple(contact),
                   spec.get('source_binding', 'DECLARED_NATIVE_T18'),
                   spec.get('units', 'native_receiver_integer'), spec.get('motion_profile'))
