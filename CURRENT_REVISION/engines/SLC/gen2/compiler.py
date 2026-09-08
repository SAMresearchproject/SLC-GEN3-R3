"""Generate complete finite transitions once; reuse them for every query."""
from collections import defaultdict
from time import perf_counter
from .contracts import SourceContract, Event
from .exact import canonical, canonical_bytes, rational
from .native import native_contract, transition, receive, contact


VIEWS = ('JOINT', 'SIGNED', 'OCCUPANCY', 'WRONG_POST_ABS')


def observation_key(value, view='JOINT'):
    if view not in VIEWS:
        raise ValueError('Unknown observation view')
    if value is None:
        return None
    if isinstance(value, dict):
        allowed = {'SIGNED_PHASE', 'AXIS_OCCUPANCY'}
        if set(value) - allowed:
            raise ValueError('Only declared measured lanes are accepted; provenance and targets are separate')
        if view in ('JOINT', 'SIGNED', 'WRONG_POST_ABS'):
            s = tuple(rational(v) for v in value['SIGNED_PHASE'])
        if view in ('JOINT', 'OCCUPANCY'):
            u = tuple(rational(v) for v in value['AXIS_OCCUPANCY'])
        return s + u if view == 'JOINT' else u if view == 'OCCUPANCY' else s + tuple(abs(v) for v in s) if view == 'WRONG_POST_ABS' else s
    if not isinstance(value, (list, tuple)):
        raise ValueError('Observation must be measured lanes, a projected vector, or None')
    return tuple(rational(v) for v in value)


class CompiledBlock:
    def __init__(self, contract):
        start = perf_counter()
        self.contract = contract
        self.contract_id = contract.contract_id
        self.states = tuple(contract.domain())
        self.state_set = frozenset(self.states)
        self.events = {e.label: e for e in contract.events}
        self.frames = {q: receive(q, contract) for q in self.states}
        self.contacts = {q: contact(q, contract) for q in self.states}
        self.transitions = []
        self.outgoing = defaultdict(list)
        for q in self.states:
            for event in contract.events:
                if event.admitted_states is not None and q not in event.admitted_states:
                    continue
                target = transition(q, event, contract.coordinates)
                if target not in self.state_set:
                    raise ValueError('Admitted event leaves the declared state domain; specify its state admission')
                row = (q, event.label, target, event.direction)
                self.transitions.append(row)
                self.outgoing[q].append(row)
        self.transitions = tuple(self.transitions)
        self._keys = {}
        self._indexes = {}
        self.compile_seconds = perf_counter() - start
        self.cache_hit = False

    def forward(self, q, event):
        q = self.contract.admit_state(q)
        if q not in self.state_set:
            raise ValueError('Initial state outside source domain')
        label = event.label if isinstance(event, Event) else event
        if label not in self.events:
            raise ValueError('Event is not in this source alphabet')
        declared = self.events[label]
        if isinstance(event, Event) and event != declared:
            raise ValueError('Event label has mismatched source action')
        if declared.admitted_states is not None and q not in declared.admitted_states:
            raise ValueError('Event is not admitted at this state')
        return transition(q, declared, self.contract.coordinates)

    def observe(self, q, view='JOINT'):
        q = self.contract.admit_state(q)
        if q not in self.frames:
            raise ValueError('Observed state outside source domain')
        if view == 'FRAME':
            return canonical(self.frames[q])
        return self.keys(view)[q]

    def keys(self, view):
        if view not in self._keys:
            self._keys[view] = {q: observation_key(f, view) for q, f in self.frames.items()}
        return self._keys[view]

    def transition_index(self, view='JOINT', directions_supplied=True):
        identity = (view, bool(directions_supplied))
        if identity not in self._indexes:
            index = defaultdict(list)
            keys = self.keys(view)
            for row in self.transitions:
                q, label, target, direction = row
                key = (direction if directions_supplied else None, keys[q], keys[target])
                index[key].append(row)
            self._indexes[identity] = {k: tuple(v) for k, v in index.items()}
        return self._indexes[identity]

    def run(self, initial, program=None, view='JOINT', *, motion=None, max_writes=None, log_class=None):
        from .motion import annotate_history, execute_motion
        if program is None:
            if motion is None:
                raise ValueError('Supply a native program or a source motion request')
            return execute_motion(self, initial, motion, view=view, max_writes=max_writes, log_class=log_class)
        if max_writes is not None:
            raise ValueError('Chunk max_writes applies to a generated motion request, not a prescribed program')
        q = self.contract.admit_state(initial)
        states = [q]
        labels = []
        for event in program:
            label = event.label if isinstance(event, Event) else event
            q = self.forward(q, event)
            labels.append(label)
            states.append(q)
        energies = [self.contacts[s] for s in states]
        result = canonical({'schema': 'SLC_GEN2_FORWARD_V1', 'contract_id': self.contract_id,
                          'initial': states[0], 'program': labels, 'states': states,
                          'observations': [self.observe(s, view) for s in states],
                          'directions': [self.events[e].direction for e in labels],
                          'contact_profile': energies,
                          'barrier': None if energies[0] is None else max(energies) - energies[0],
                          'view': view})
        result['motion'] = annotate_history(self, result, log_class)
        if motion is not None:
            result['motion']['prescribed_program_authority'] = True
            result['motion']['requested_intent'] = canonical(motion)
        return result

    def decode(self, observations, directions=None, initial_states=None,
               view='JOINT', max_steps=None):
        from .inverse import JointAnswer
        return JointAnswer.start(self, observations, directions, initial_states, view).advance(max_steps)

    def resume(self, checkpoint, max_steps=None):
        from .inverse import JointAnswer
        return JointAnswer.restore(self, checkpoint).advance(max_steps)

    def to_dict(self):
        index = self.transition_index()
        return {'schema': 'SLC_GEN2_COMPILED_BLOCK_V1', 'contract': self.contract.to_dict(),
                'contract_id': self.contract_id, 'states': len(self.states),
                'transitions': len(self.transitions), 'joint_direction_keys': len(index),
                'keys_with_single_event_label': sum(len({r[1] for r in rows}) == 1 for rows in index.values()),
                'compile_seconds': self.compile_seconds, 'cache_hit': self.cache_hit}


_BLOCKS = {}


def compile_block(spec=None, *, use_cache=True):
    if spec is None:
        spec = native_contract()
    if isinstance(spec, dict):
        spec = SourceContract.from_dict(spec)
    if not isinstance(spec, SourceContract):
        raise TypeError('Compilation requires a SourceContract or its declared JSON form')
    # Canonical object bytes, not hash equality, decide cache identity.
    identity = canonical_bytes(spec.to_dict())
    if use_cache and identity in _BLOCKS:
        block = _BLOCKS[identity]
        block.cache_hit = True
        return block
    block = CompiledBlock(spec)
    if use_cache:
        _BLOCKS[identity] = block
    return block


def clear_compile_cache():
    _BLOCKS.clear()


def compose_relations(left, right):
    """Compose triples (start,witness,end), keeping each shared intermediate."""
    by_start = defaultdict(list)
    for start, witness, end in right:
        by_start[start].append((witness, end))
    result = []
    for start, witness_left, middle in left:
        for witness_right, end in by_start.get(middle, ()):
            result.append((start, (witness_left, middle, witness_right), end))
    return tuple(result)
