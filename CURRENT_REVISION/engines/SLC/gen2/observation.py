"""Complete finite native inverse sessions and exact observation decisions.

DELTA matches actual declared receiver differences on linked transitions.
ABSOLUTE uses the existing JointAnswer DAG, then retains every matching path.
Targets always refer to the original history; probes append separate history.
Checkpoints are integrity seals with semantic replay, not authentication tokens.
No presentation limit or partially processed relation is accepted as a session.

Choices declare one native event (or a passive absolute observation), receiver
view, selected scalar components, and IDENTITY or SIGN projection. A choice is
available only if its event is admitted for every current member. Undefined
contact/action targets remain in the inverse relation and cannot be scored.
R3 additionally supports profile-declared exact motion readouts and automatic
choice rosters. Candidate chart predictions never substitute for supplied
measurements; every applied readout retains its original target and history.
"""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from inspect import getsourcefile
from pathlib import Path

from .compiler import observation_key
from .contracts import SourceContract
from .exact import canonical, canonical_bytes, digest, rational
from .exact_observation_information import score_observation, choose_max_information, report_detail
from . import observation_motion as motion_observation
from . import reporting


VIEWS = ('JOINT', 'SIGNED', 'OCCUPANCY')
SCHEMA = 'SLC_GEN2_OBSERVATION_CHECKPOINT_V1'
PLAN_SCHEMA = 'SLC_GEN2_OBSERVATION_PLAN_V1'
_PREDICTED = {}
_BINDING_CACHE = {}
_STATS = {'prediction_hits': 0, 'prediction_misses': 0, 'session_hits': 0}

def reuse_stats(reset=False):
    result = dict(_STATS)
    result.update(motion_observation.reuse_stats(reset=reset))
    if reset:
        for key in _STATS: _STATS[key] = 0
    return result

_VERIFIED = {}  # Exact canonical bytes; an exported or modified list never keys this cache.


def _fields(value, allowed, required=()):
    if not isinstance(value, dict) or set(value) - set(allowed) or set(required) - set(value):
        raise ValueError('Missing or undeclared fields: expected ' + ', '.join(sorted(allowed)))


def _binding(log_class):
    base = Path(__file__).resolve().parent
    names = ('observation.py', 'observation_motion.py', 'exact_observation_information.py',
             'observation_policy.py', 'reporting.py', 'quantities.py', 'contracts.py',
             'compiler.py', 'exact.py', 'native.py', 'inverse.py',
             'motion.py', 'golden.py', 'motion_profiles.json',
             'dependencies/native/t18.py', 'dependencies/native/exact.py',
             'dependencies/common_reception.py', 'dependencies/J4_RESPONSES.jsonl')
    paths = {name: base / name for name in names}
    source = getsourcefile(log_class)
    if source is None:
        raise ValueError('Exact formal-log implementation must have a bound source file')
    paths['formal_log_source'] = Path(source)
    signature = tuple((name, str(path), path.stat().st_mtime_ns, path.stat().st_size) for name, path in paths.items())
    if signature not in _BINDING_CACHE:
        _BINDING_CACHE.clear()
        _BINDING_CACHE[signature] = {name: sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
    return deepcopy(_BINDING_CACHE[signature])


def _phase_map(raw, block):
    if not isinstance(raw, dict):
        raise ValueError('Phase conditions must be a coordinate-to-phase map')
    out = {}
    for coordinate, phase in raw.items():
        if type(coordinate) is int:
            number = coordinate
        elif type(coordinate) is str and coordinate.isdigit() and str(int(coordinate)) == coordinate:
            number = int(coordinate)
        else:
            raise ValueError('Condition coordinate must be a declared integer coordinate')
        if number not in block.contract.coordinates or type(phase) is not int or phase not in range(4):
            raise ValueError('Unknown coordinate or invalid Z4 phase in condition')
        if str(number) in out:
            raise ValueError('Duplicate condition coordinate')
        out[str(number)] = phase
    return out


def _components(raw, width):
    if raw is None:
        return list(range(width))
    if not isinstance(raw, (tuple, list)) or not raw or len(set(raw)) != len(raw):
        raise ValueError('Components must be a nonempty list of distinct scalar indices')
    if any(type(i) is not int or not 0 <= i < width for i in raw):
        raise ValueError('Receiver component outside declared view')
    return list(raw)


def _vector(raw, width, *, scalar=False):
    if scalar and not isinstance(raw, (list, tuple)) and width == 1:
        raw = [raw]
    if not isinstance(raw, (list, tuple)) or len(raw) != width:
        raise ValueError('Observation length does not match declared receiver components')
    return tuple(rational(value) for value in raw)


def _question(payload, block):
    allowed = {'contract', 'mode', 'observations', 'deltas', 'view', 'components',
               'directions', 'event_labels', 'known_phases', 'conditions',
               'initial_states', 'target', 'available_readouts', 'available_reports'}
    _fields(payload, allowed, ('mode', 'target'))
    if 'contract' in payload and SourceContract.from_dict(payload['contract']).to_dict() != block.contract.to_dict():
        raise ValueError('Outer source contract does not match compiled source')
    mode = payload['mode']
    view = payload.get('view', 'JOINT')
    if mode not in ('ABSOLUTE', 'DELTA') or view not in VIEWS:
        raise ValueError('Unknown inverse mode or native receiver view')
    width = len(next(iter(block.keys(view).values())))
    components = _components(payload.get('components'), width)
    field = 'observations' if mode == 'ABSOLUTE' else 'deltas'
    other = 'deltas' if mode == 'ABSOLUTE' else 'observations'
    raw = payload.get(field)
    if other in payload or not isinstance(raw, (list, tuple)) or (mode == 'ABSOLUTE' and not raw):
        raise ValueError('Supply exactly the measurements for the declared inverse mode')
    measurements = []
    for value in raw:
        if isinstance(value, dict):
            if components != list(range(width)):
                raise ValueError('Lane dictionaries require the complete declared view')
            value = observation_key(value, view)
        measurements.append(None if value is None else _vector(value, len(components)))
    n = len(measurements) - (mode == 'ABSOLUTE')
    directions = payload.get('directions', [None] * n)
    labels = payload.get('event_labels', [None] * n)
    if not isinstance(directions, (list, tuple)) or len(directions) != n or any(
            d is not None and (type(d) is not int or d not in (-1, 1)) for d in directions):
        raise ValueError('One exact direction (+1, -1 or withheld) is required per original transition')
    if not isinstance(labels, (list, tuple)) or len(labels) != n or any(
            e is not None and (type(e) is not str or e not in block.events) for e in labels):
        raise ValueError('One declared event label or withheld value is required per original transition')
    if 'conditions' in payload and 'known_phases' in payload:
        raise ValueError('Use conditions or its initial-only known_phases shorthand, not both')
    raw_conditions = payload.get('conditions', {'initial': payload.get('known_phases', {})})
    if not isinstance(raw_conditions, dict):
        raise ValueError('Conditions must map history positions to coordinate phase maps')
    conditions = {}
    for position, phases in raw_conditions.items():
        if position == 'initial':
            index = 0
        elif position == 'final':
            index = n
        elif type(position) is int:
            index = position
        elif type(position) is str and position.isdigit() and str(int(position)) == position:
            index = int(position)
        else:
            raise ValueError('Unknown condition position')
        if not 0 <= index <= n or str(index) in conditions:
            raise ValueError('Condition position outside original history or repeated')
        conditions[str(index)] = _phase_map(phases, block)
    roots = payload.get('initial_states')
    if roots is not None:
        if not isinstance(roots, (tuple, list)):
            raise ValueError('Initial states must be an explicit state list')
        roots = [block.contract.admit_state(q) for q in roots]
        if len(set(roots)) != len(roots) or any(q not in block.state_set for q in roots):
            raise ValueError('Initial state list has duplicates or inadmissible states')
        roots = sorted(roots)
    target = payload['target']
    _fields(target, {'kind', 'position', 'coordinates'}, ('kind',))
    kind = target['kind']
    if kind not in ('STATE', 'BARRIER', 'ACTION_RATIO', 'HISTORY'):
        raise ValueError('Unknown original inverse target')
    if kind == 'STATE':
        position = target.get('position', 'final')
        coords = target.get('coordinates', list(block.contract.coordinates))
        if position not in ('initial', 'final') or not isinstance(coords, (tuple, list)) or not coords:
            raise ValueError('STATE target needs original initial/final and admitted coordinates')
        if len(set(coords)) != len(coords) or any(type(c) is not int or c not in block.contract.coordinates for c in coords):
            raise ValueError('STATE target has unknown or repeated coordinates')
        target = {'kind': kind, 'position': position, 'coordinates': list(coords)}
    elif set(target) != {'kind'}:
        raise ValueError('Contact targets do not take state projection fields')
    question = {'mode': mode, 'view': view, 'components': components,
                field: measurements, 'directions': directions, 'event_labels': labels,
                'conditions': conditions, 'initial_states': roots, 'target': target}
    if 'available_readouts' in payload and not isinstance(payload['available_readouts'], (list, tuple)):
        raise ValueError('Available readouts must be an explicit descriptor whitelist')
    declared = motion_observation.available_readouts(block, payload.get('available_readouts'))
    if declared or 'available_readouts' in payload:
        question['available_readouts'] = declared
    if declared or 'available_reports' in payload:
        question['available_reports'] = reporting.source_reports(block, declared, payload.get('available_reports'))
    return canonical(question)


def _matches_conditions(block, q, conditions):
    return all(q[block.contract.coordinates.index(int(c))] == phase for c, phase in conditions.items())


def _member(block, program, states, target, log_class):
    states = [tuple(q) for q in states]
    energies = [block.contacts[q] for q in states]
    barrier = None if any(e is None for e in energies) else max(energies) - energies[0]
    ratio = None if energies[0] in (None, 0) or energies[-1] is None else Fraction(energies[-1]) / Fraction(energies[0])
    positive_ratio = ratio is not None and energies[0] > 0 and energies[-1] > 0
    if target['kind'] == 'STATE':
        state = states[0 if target['position'] == 'initial' else -1]
        value = [state[block.contract.coordinates.index(c)] for c in target['coordinates']]
        defined = True
    elif target['kind'] == 'HISTORY':
        value, defined = {'contract': block.contract.to_dict(), 'program': list(program), 'states': states}, True
    elif target['kind'] == 'BARRIER':
        value, defined = barrier, barrier is not None
    else:
        value, defined = str(ratio) if positive_ratio else None, positive_ratio
    identity = {'contract_id': block.contract_id, 'program': program, 'states': states}
    return canonical({'record_id': digest(identity), 'initial': states[0],
                      'original_program': program, 'original_states': states,
                      'original_contact_profile': energies, 'original_barrier': barrier,
                      'original_action_ratio': None if ratio is None else str(ratio),
                      'original_log_action_ratio': log_class.from_positive_rational(ratio).to_dict() if positive_ratio else None,
                      'target': value, 'target_status': 'DEFINED' if defined else 'UNDEFINED',
                      'program': program, 'states': states, 'contact_profile': energies,
                      'barrier': barrier, 'probe_history': []})


def _original_members(block, question, log_class):
    view, components = question['view'], question['components']
    keys = {q: tuple(values[i] for i in components) for q, values in block.keys(view).items()}
    conditions = question['conditions']
    roots = block.states if question['initial_states'] is None else [tuple(q) for q in question['initial_states']]
    roots = [q for q in roots if _matches_conditions(block, q, conditions.get('0', {}))]
    labels, directions = question['event_labels'], question['directions']
    measurements = question['observations' if question['mode'] == 'ABSOLUTE' else 'deltas']
    measurements = [None if m is None else tuple(rational(v) for v in m) for m in measurements]
    paths = []
    if question['mode'] == 'ABSOLUTE':
        full = components == list(range(len(next(iter(block.keys(view).values())))))
        # A partial view is a declared constraint on actual paths, never a fabricated frame.
        answer = block.decode(measurements if full else [None] * len(measurements),
                              directions=directions, initial_states=roots, view=view)
        if not answer.complete:
            raise ValueError('Absolute reconstruction did not finish the original history')
        for path in answer.iter_paths():
            program, states = path['program'], path['states']
            if any(label is not None and label != program[i] for i, label in enumerate(labels)):
                continue
            if any(m is not None and keys[tuple(states[i])] != m for i, m in enumerate(measurements)):
                continue
            if any(not _matches_conditions(block, states[int(i)], condition) for i, condition in conditions.items()):
                continue
            paths.append((list(program), list(states)))
    else:
        frontier = [([], [q]) for q in roots]
        for i, measured in enumerate(measurements):
            following = []
            for program, states in frontier:
                q = states[-1]
                for _, label, after, direction in block.outgoing.get(q, ()):
                    if labels[i] is not None and labels[i] != label:
                        continue
                    if directions[i] is not None and directions[i] != direction:
                        continue
                    if not _matches_conditions(block, after, conditions.get(str(i + 1), {})):
                        continue
                    delta = tuple(b - a for a, b in zip(keys[q], keys[after]))
                    if measured is None or measured == delta:
                        following.append((program + [label], states + [after]))
            frontier = following
        paths = frontier
    members = [_member(block, program, states, question['target'], log_class) for program, states in paths]
    return sorted(members, key=lambda m: (m['initial'], m['original_program'], m['original_states']))


def _weights(raw, members):
    ids = {member['record_id'] for member in members}
    if not isinstance(raw, dict) or set(raw) != ids:
        raise ValueError('Weights must cover exactly the complete current member IDs')
    result = {identifier: rational(value) for identifier, value in raw.items()}
    if any(value <= 0 for value in result.values()):
        raise ValueError('Every record weight must be positive and exact')
    return canonical(result)


def _choice(raw, block):
    if isinstance(raw, dict) and 'readout' in raw:
        _fields(raw, {'label', 'event', 'readout', 'report'}, ('label', 'event', 'readout'))
        label, event = raw['label'], raw['event']
        if type(label) is not str or not label:
            raise ValueError('Every observation choice needs a nonempty distinct label')
        if event is not None and (type(event) is not str or event not in block.events):
            raise ValueError('Observation choice event must be a declared native label')
        result = {'label': label, 'event': event,
                  'readout': motion_observation.descriptor(raw['readout'], block)}
        if 'report' in raw: result['report'] = reporting.normalize_report(raw['report'])
        return result
    _fields(raw, {'label', 'event', 'mode', 'view', 'components', 'projection', 'report'}, ('label', 'event', 'mode'))
    label, event = raw['label'], raw['event']
    mode, view = raw['mode'], raw.get('view', 'JOINT')
    projection = raw.get('projection', 'IDENTITY')
    if type(label) is not str or not label:
        raise ValueError('Every observation choice needs a nonempty distinct label')
    if event is not None and (type(event) is not str or event not in block.events):
        raise ValueError('Observation choice event must be a declared native label')
    if mode not in ('ABSOLUTE', 'DELTA') or (event is None and mode != 'ABSOLUTE'):
        raise ValueError('Passive observations are absolute; native probes may observe a frame or difference')
    if view not in VIEWS or projection not in ('IDENTITY', 'SIGN'):
        raise ValueError('Unknown observation view or projection')
    width = len(next(iter(block.keys(view).values())))
    result = {'label': label, 'event': event, 'mode': mode, 'view': view,
              'components': _components(raw.get('components'), width), 'projection': projection}
    if 'report' in raw: result['report'] = reporting.normalize_report(raw['report'])
    return result


def _predictions_uncached(block, members, choice, log_class=None, available_readouts=(), annotation_cache=None):
    predictions, unavailable = [], []
    typed = 'readout' in choice
    if typed and choice['readout'] not in available_readouts:
        return [], [member['record_id'] for member in members]
    for member in members:
        before = tuple(member['states'][-1])
        event, after = choice['event'], before
        if event is not None:
            rows = [row for row in block.outgoing.get(before, ()) if row[1] == event]
            if not rows:
                unavailable.append(member['record_id'])
                continue
            after = rows[0][2]
        states = member['states'] + ([] if event is None else [list(after)])
        program = member['program'] + ([] if event is None else [event])
        if typed:
            try:
                values = motion_observation.predicted_value(
                    block, initial=member['initial'], program=program, states=states,
                    readout=choice['readout'], log_class=log_class, cache=annotation_cache)
            except motion_observation.UnavailableReadout:
                unavailable.append(member['record_id'])
                continue
        else:
            pre, post = block.observe(before, choice['view']), block.observe(after, choice['view'])
            values = post if choice['mode'] == 'ABSOLUTE' else tuple(b - a for a, b in zip(pre, post))
            values = [values[i] for i in choice['components']]
            if choice['projection'] == 'SIGN':
                values = [(value > 0) - (value < 0) for value in values]
        energies = [block.contacts[tuple(q)] for q in states]
        barrier = None if any(e is None for e in energies) else max(energies) - energies[0]
        if 'report' in choice:
            values = reporting.predict(values, choice, log_class)
        predictions.append(canonical({'record_id': member['record_id'], 'observation': values,
                                      'after': after, 'program': program, 'states': states,
                                      'contact_profile': energies, 'barrier': barrier}))
    return predictions, unavailable


def _predictions(block, members, choice, log_class=None, available_readouts=(), annotation_cache=None):
    # Complete current linked histories and source/code bytes key reuse. Labels
    # remain in the key: equal receiver partitions do not equate future actions.
    binding = annotation_cache.get('__implementation_binding__') if annotation_cache is not None else None
    if binding is None: binding = _binding(log_class)
    key = digest({'binding': binding, 'contract': block.contract.to_dict(),
                  'members': [{k: v for k, v in m.items() if k != 'probe_history'} for m in members],
                  'choice': {k: v for k, v in choice.items() if k != 'label'}, 'readouts': available_readouts})
    if key in _PREDICTED:
        _STATS['prediction_hits'] += 1
        return deepcopy(_PREDICTED[key])
    _STATS['prediction_misses'] += 1
    value = _predictions_uncached(block, members, choice, log_class, available_readouts, annotation_cache)
    if len(_PREDICTED) >= 8192: _PREDICTED.pop(next(iter(_PREDICTED)))
    _PREDICTED[key] = value
    return deepcopy(value)


def _observed(block, members, choice, observation, log_class):
    if 'report' in choice:
        observation = reporting.supplied(observation, choice, log_class)
        if choice['report']['kind'] != 'EXACT': return observation
        raw_choice = {k: v for k, v in choice.items() if k != 'report'}
        return reporting.wrap(_observed(block, members, raw_choice, observation['value'], log_class), choice)
    if 'readout' in choice:
        length = (len(members[0]['states']) + (choice['event'] is not None)) if members else 0
        return motion_observation.observed_value(observation, choice['readout'], log_class, history_length=length)
    observation = canonical(_vector(observation, len(choice['components']), scalar=True))
    if choice['projection'] == 'SIGN' and any(value not in (-1, 0, 1) for value in observation):
        raise ValueError('SIGN observation components must be -1, 0 or +1')
    return observation


def _condition_predictions(members, choice, observation, predictions, report_status='OBSERVED'):
    predictions = {row['record_id']: row for row in predictions}
    retained = []
    for member in members:
        prediction = predictions[member['record_id']]
        if report_status == 'OBSERVED' and prediction['observation'] != observation:
            continue
        result = deepcopy(member)
        for field in ('program', 'states', 'contact_profile', 'barrier'):
            result[field] = prediction[field]
        step = {'choice': choice, 'observation': observation,
                'before': member['states'][-1], 'after': prediction['after']}
        if report_status == 'MISSING': step['report_status'] = 'MISSING'
        result['probe_history'].append(step)
        retained.append(result)
    return retained


def _condition(block, members, choice, observation, log_class=None, available_readouts=(), report_status='OBSERVED'):
    predictions, unavailable = _predictions(block, members, choice, log_class, available_readouts)
    if unavailable:
        raise ValueError('Selected probe is not admitted for every surviving source history')
    if report_status not in ('OBSERVED', 'MISSING'):
        raise ValueError('Report status must be OBSERVED or MISSING')
    if report_status == 'MISSING':
        if observation is not None: raise ValueError('Missing report cannot also supply a measured value')
    else:
        observation = _observed(block, members, choice, observation, log_class)
    return _condition_predictions(members, choice, observation, predictions, report_status), observation


def _seal(body):
    body = canonical(body)
    return {'body': body, 'sha256': digest(body)}


def _checked_seal(value, schema):
    _fields(value, {'body', 'sha256'}, ('body', 'sha256'))
    body = value['body']
    if not isinstance(body, dict) or body.get('schema') != schema or digest(body) != value['sha256']:
        raise ValueError('Checkpoint/plan integrity or schema mismatch')
    return body


def _session(block, checkpoint, log_class):
    body = _checked_seal(checkpoint, SCHEMA)
    _fields(body, {'schema', 'complete', 'contract', 'implementation_binding', 'question',
                   'original_members', 'members', 'weights', 'probe_history'},
                  {'schema', 'complete', 'contract', 'implementation_binding', 'question',
                   'original_members', 'members', 'weights', 'probe_history'})
    binding = _binding(log_class)
    if body['complete'] is not True or body['contract'] != block.contract.to_dict() or body['implementation_binding'] != binding:
        raise ValueError('Session is unfinished or bound to another source/implementation')
    cache_key = canonical_bytes(body)
    if cache_key in _VERIFIED:
        _STATS['session_hits'] += 1
        return deepcopy(body)
    # Reconstruct the complete question so removing paths and re-sealing cannot
    # turn a truncated presentation into an observation-planning relation.
    question = _question(body['question'], block)
    if question != body['question']:
        raise ValueError('Session question is not the canonical original contract')
    originals = _original_members(block, question, log_class)
    if originals != body['original_members']:
        raise ValueError('Original relation is altered or incomplete')
    members = originals
    weights = {m['record_id']: 1 for m in members}
    replay = deepcopy(body)
    replay.update(members=members, weights=weights, probe_history=[])
    if not isinstance(body['probe_history'], list):
        raise ValueError('Probe history must be a complete ordered list')
    for step in body['probe_history']:
        _fields(step, {'choice', 'observation', 'weights', 'plan', 'report_status'},
                ('choice', 'observation', 'weights', 'plan'))
        choice = _choice(step['choice'], block)
        if choice != step['choice']:
            raise ValueError('Probe choice is not canonical')
        saved_plan = _checked_seal(step['plan'], PLAN_SCHEMA)
        previous = _seal(replay)
        if saved_plan.get('checkpoint_sha256') != previous['sha256']:
            raise ValueError('Saved decision plan is not linked to its preceding complete session')
        expected = _plan(block, previous, replay, _replay_choices(saved_plan),
                         saved_plan.get('weights'), log_class)
        choices = [row for row in expected['choices'] if row['choice'] == choice and row['available']]
        if expected['plan'] != step['plan'] or not choices or expected['status'] in ('EMPTY', 'UNDEFINED_TARGET'):
            raise ValueError('Saved probe plan, alternatives or exact selection record was altered')
        if step['weights'] != saved_plan['weights']:
            raise ValueError('Saved probe measure differs from its declared decision plan')
        weights = _weights(step['weights'], members)
        members, observation = _condition(block, members, choice, step['observation'], log_class,
                                          body['question'].get('available_readouts', ()), step.get('report_status', 'OBSERVED'))
        if observation != step['observation']:
            raise ValueError('Probe observation is not canonical')
        ids = {m['record_id'] for m in members}
        weights = {identifier: value for identifier, value in weights.items() if identifier in ids}
        replay.update(members=members, weights=weights)
        replay['probe_history'].append(step)
    if members != body['members'] or weights != body['weights']:
        raise ValueError('Conditioned linked relation or its exact measure is altered/incomplete')
    if len(_VERIFIED) >= 16:
        _VERIFIED.pop(next(iter(_VERIFIED)))
    _VERIFIED[cache_key] = True
    return deepcopy(body)


def _result(body):
    count = len(body['members'])
    return {'schema': 'SLC_GEN2_INVERSE_SESSION_V1', 'complete': True,
            'status': 'EMPTY' if count == 0 else 'UNIQUE' if count == 1 else 'MULTIPLE',
            'candidate_count': count, 'original_candidate_count': len(body['original_members']),
            'target': body['question']['target'], 'members': deepcopy(body['members']),
            'weights': deepcopy(body['weights']), 'checkpoint': _seal(body)}


def _evaluate(block, body, choices, raw_weights, log_class):
    automatic = choices is None
    declared = body['question'].get('available_readouts', ())
    reports = body['question'].get('available_reports', reporting.source_reports(block, declared))
    if automatic:
        choices = reporting.automatic_choices(motion_observation.automatic_choices(block, declared), reports)
    if not isinstance(choices, (tuple, list)) or not choices:
        raise ValueError('Declare a nonempty ordered observation-choice roster')
    choices = [_choice(choice, block) for choice in choices]
    if len({choice['label'] for choice in choices}) != len(choices):
        raise ValueError('Observation choice labels must be unique')
    refined = automatic or any('report' in choice for choice in choices)
    members = body['members']
    weights = _weights(body['weights'] if raw_weights is None else raw_weights, members)
    scores, details, results = {}, {}, []
    annotation_cache = {'__implementation_binding__': _binding(log_class)}
    defined = all(member['target_status'] == 'DEFINED' for member in members)
    for choice in choices:
        channel_declared = ('readout' not in choice or choice['readout'] in declared) and reporting.allowed(choice, reports)
        if 'report' in choice and not channel_declared:
            raise ValueError('Observation report resolution is not declared by this source or its whitelist')
        predictions, unavailable = _predictions(block, members, choice, log_class, declared, annotation_cache)
        history_length = (len(members[0]['states']) + (choice['event'] is not None)) if members else 0
        component_count = (motion_observation.scalar_count(choice['readout'], history_length)
                           if 'readout' in choice else len(choice['components']))
        if 'report' in choice and choice['report']['kind'] != 'EXACT': component_count = 1
        row = {'choice': choice, 'label': choice['label'], 'available': not unavailable and channel_declared,
               'returned_scalar_components': component_count,
               'predictions': predictions, 'unavailable_record_ids': unavailable, 'score': None}
        if refined: row['quantity'] = reporting.quantity_descriptor(block, choice)
        if members and defined and not unavailable and channel_declared:
            by_id = {m['record_id']: m for m in members}
            records = [{'record_id': p['record_id'], 'target': by_id[p['record_id']]['target'],
                        'observation': p['observation']} for p in predictions]
            score = score_observation(records, formal_log_cls=log_class,
                                      weights={identifier: rational(value) for identifier, value in weights.items()})
            scores[choice['label']] = score
            row['score'] = score.to_dict()
            details[choice['label']] = report_detail(score, log_class)
            if refined: row['report_detail'] = _detail_json(details[choice['label']])
        results.append(row)
    return choices, weights, results, scores, details, automatic, refined


def _detail_json(detail):
    return {'report_entropy': detail['report_entropy'].to_dict(), 'report_alphabet': detail['report_alphabet']}


def _plan(block, checkpoint, body, choices, raw_weights, log_class):
    choices, weights, results, scores, details, automatic, refined = _evaluate(block, body, choices, raw_weights, log_class)
    ties = choose_max_information(scores) if scores else []
    finalists = list(ties)
    if refined and finalists:
        best = details[finalists[0]]['report_entropy']
        for label in finalists[1:]:
            if details[label]['report_entropy'].compare(best) < 0: best = details[label]['report_entropy']
        finalists = [label for label in finalists if details[label]['report_entropy'].compare(best) == 0]
        alphabet = min(details[label]['report_alphabet'] for label in finalists)
        finalists = [label for label in finalists if details[label]['report_alphabet'] == alphabet]
    selected = min(finalists, key=lambda label: next(r['returned_scalar_components'] for r in results if r['label'] == label)) if finalists else None
    if not body['members']: status = 'EMPTY'
    elif any(m['target_status'] != 'DEFINED' for m in body['members']): status = 'UNDEFINED_TARGET'
    elif not scores: status = 'NO_AVAILABLE_CHOICES'
    elif scores[selected].mutual_information.compare(log_class.zero()) == 0: status = 'NO_GAIN'
    else: status = 'GAIN'
    plan_body = {'schema': PLAN_SCHEMA, 'checkpoint_sha256': checkpoint['sha256'],
                 'choices': choices, 'weights': weights, 'results': results,
                 'maximizing_labels': ties, 'selected_label': selected, 'status': status}
    if automatic: plan_body['automatic_choices'] = True
    if refined:
        plan_body['selection_rule'] = 'TARGET_INFORMATION_REPORT_ENTROPY_ALPHABET_SCALARS_ROSTER'
        plan_body['minimum_detail_labels'] = finalists
    return canonical({'schema': PLAN_SCHEMA, 'complete': True, 'status': status,
                      'candidate_count': len(body['members']), 'choices': results,
                      'maximizing_labels': ties, 'selected_label': selected,
                      'plan': _seal(plan_body), 'checkpoint': checkpoint})


def _replay_choices(plan):
    if 'automatic_choices' in plan:
        if plan['automatic_choices'] is not True:
            raise ValueError('Automatic roster marker must be exactly true')
        return None
    return plan.get('choices')


def dispatch(operation, payload, block, formal_log_cls):
    """Public, JSON-safe operations on a compiled native source and exact log class.

    OPEN: mode, measurements, original target, optional explicit phase conditions.
    PLAN: checkpoint, optional choices and complete ID-to-positive-rational weights.
    APPLY: checkpoint, sealed plan, choice_label, measured returned observation.
    RESUME: checkpoint. Resumption performs semantic completeness validation.
    """
    if operation == 'GEN2_INVERSE_OPEN':
        question = _question(payload, block)
        members = _original_members(block, question, formal_log_cls)
        body = {'schema': SCHEMA, 'complete': True, 'contract': block.contract.to_dict(),
                'implementation_binding': _binding(formal_log_cls), 'question': question,
                'original_members': members, 'members': deepcopy(members),
                'weights': {m['record_id']: 1 for m in members}, 'probe_history': []}
        return _result(body)
    if operation == 'GEN2_INVERSE_RESUME':
        _fields(payload, {'checkpoint'}, ('checkpoint',))
        return _result(_session(block, payload['checkpoint'], formal_log_cls))
    if operation == 'GEN2_OBSERVATION_PLAN':
        _fields(payload, {'checkpoint', 'choices', 'weights'}, ('checkpoint',))
        body = _session(block, payload['checkpoint'], formal_log_cls)
        return _plan(block, payload['checkpoint'], body, payload.get('choices'), payload.get('weights'), formal_log_cls)
    if operation == 'GEN2_OBSERVATION_APPLY':
        _fields(payload, {'checkpoint', 'plan', 'choice_label', 'observation', 'report_status'},
                ('checkpoint', 'plan', 'choice_label'))
        report_status = payload.get('report_status', 'OBSERVED')
        if report_status not in ('OBSERVED', 'MISSING') or (report_status == 'OBSERVED' and 'observation' not in payload) or (report_status == 'MISSING' and 'observation' in payload):
            raise ValueError('Supply an actual observation or explicitly report MISSING')
        body = _session(block, payload['checkpoint'], formal_log_cls)
        plan_body = _checked_seal(payload['plan'], PLAN_SCHEMA)
        if plan_body.get('checkpoint_sha256') != payload['checkpoint']['sha256']:
            raise ValueError('Observation plan belongs to another complete inverse session')
        expected = _plan(block, payload['checkpoint'], body, _replay_choices(plan_body),
                         plan_body.get('weights'), formal_log_cls)
        if expected['plan'] != payload['plan']:
            raise ValueError('Observation plan predictions, scoring or choice set were altered')
        rows = [row for row in expected['choices'] if row['label'] == payload['choice_label']]
        if not rows or not rows[0]['available']:
            raise ValueError('Selected observation is absent or unavailable for the full relation')
        if expected['status'] in ('EMPTY', 'UNDEFINED_TARGET'):
            raise ValueError('Cannot apply a target-scored plan to an empty or undefined-target relation')
        choice = rows[0]['choice']
        members, observation = _condition(block, body['members'], choice, payload.get('observation'), formal_log_cls,
                                          body['question'].get('available_readouts', ()), report_status)
        body['probe_history'].append({'choice': choice, 'observation': observation,
                                      'weights': plan_body['weights'], 'plan': deepcopy(payload['plan'])})
        if report_status == 'MISSING': body['probe_history'][-1]['report_status'] = 'MISSING'
        body['members'] = members
        ids = {m['record_id'] for m in members}
        body['weights'] = {identifier: weight for identifier, weight in plan_body['weights'].items() if identifier in ids}
        return _result(body)
    raise ValueError('Unknown GEN2 inverse observation operation')
