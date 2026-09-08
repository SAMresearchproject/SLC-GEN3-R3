"""Exact native source motion, fixed-sphere annotation and golden execution.

Annotation reads an already executed complete native history and compiled
source tables. It never calls run/forward. Sphere scale is each role's source
contact action divided by its own initial action; phases and ordered signed
lifts remain available when a positive action chart is unavailable. Registered
roles are source endpoint roles. They do not assign physical spin or orbit.
"""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from inspect import getsourcefile
from itertools import combinations
import json
from pathlib import Path

from .exact import canonical, canonical_bytes, digest, rational
from .dependencies import common_reception as common
from . import golden


PHASE = ((1, 0), (0, 1), (-1, 0), (0, -1))
PROFILE_SCHEMA = 'GEN2_MOTION_PROFILE_V1'
CHECKPOINT_SCHEMA = 'GEN2_MOTION_CHECKPOINT_V1'
_LOG_CLASS = None
_LOG_SOURCE_HASHES = {}
_MOTION_VERIFIED = {}
_STATS = {'full_annotations': 0, 'incremental_appends': 0, 'new_states_annotated': 0,
          'boundary_states_revalidated': 0, 'prior_states_reused': 0,
          'checkpoint_states_revalidated': 0}


def reuse_stats(reset=False):
    if type(reset) is not bool:
        raise ValueError('Counter reset must be boolean')
    result = dict(_STATS)
    if reset:
        _STATS.update(dict.fromkeys(_STATS, 0))
    return result


def _log_class(supplied=None):
    global _LOG_CLASS
    if supplied is not None:
        if supplied not in _LOG_SOURCE_HASHES:
            _LOG_SOURCE_HASHES[supplied] = sha256(Path(getsourcefile(supplied)).read_bytes()).hexdigest()
        _LOG_CLASS = supplied
        from .quantities import bind_formal_log
        bind_formal_log(supplied, _LOG_SOURCE_HASHES[supplied])
        return supplied
    if _LOG_CLASS is None:
        # This is the installed retained exact-information component, not a
        # second logarithm implementation or a filesystem-selected substitute.
        from CURRENT_REVISION.engines.SLC.native.runtime import Q3Runtime
        with Q3Runtime() as runtime:
            _LOG_CLASS = runtime.exact_information().hd_module.FormalLogElement
            _LOG_SOURCE_HASHES[_LOG_CLASS] = sha256(Path(getsourcefile(_LOG_CLASS)).read_bytes()).hexdigest()
            from .quantities import bind_formal_log
            bind_formal_log(_LOG_CLASS, _LOG_SOURCE_HASHES[_LOG_CLASS])
    return _LOG_CLASS


def bind_log_class(log_class):
    """Register an active runtime's exact class for later pure helper calls."""
    return _log_class(log_class)


def _fields(raw, allowed, required=()):
    if not isinstance(raw, dict) or set(raw) - set(allowed) or set(required) - set(raw):
        raise ValueError('Missing or undeclared motion fields: ' + ', '.join(sorted(allowed)))


def _positive_label(block, coordinate):
    matches = [event.label for event in block.contract.events
               if event.coordinate == coordinate and event.direction == 1]
    conventional = 'W' + str(coordinate) + '+'
    return conventional if conventional in matches else matches[0] if len(matches) == 1 else None


def _default_readouts(roles):
    result = []
    for role in roles:
        kinds = ['ROLE_PHASE']
        if role['source_coordinates'] is not None:
            kinds = ['SPHERE', 'SCALE', 'LOG_SCALE'] + kinds
        result.extend({'kind': kind, 'role': role['role_id'], 'scope': 'ENDPOINT'} for kind in kinds)
    result.extend({'kind': 'RELATIVE_PHASE', 'roles': [a['role_id'], b['role_id']],
                   'scope': 'ENDPOINT'} for a, b in combinations(roles, 2))
    return result


def _normalize_profile(block, raw, *, registered=False):
    allowed = {'schema', 'profile_id', 'roles', 'aliases', 'available_readouts',
               'default_motion', 'readout_context', 'complete_history_readout', 'observation_reports'}
    _fields(raw, allowed, ('profile_id', 'roles'))
    if raw.get('schema', PROFILE_SCHEMA) != PROFILE_SCHEMA:
        raise ValueError('Unknown source motion profile schema')
    if type(raw['profile_id']) is not str or not raw['profile_id']:
        raise ValueError('Motion profile requires a nonempty source identity')
    if not isinstance(raw['roles'], (list, tuple)) or not raw['roles']:
        raise ValueError('A source motion profile requires explicit roles')
    roles = []
    for role in raw['roles']:
        _fields(role, {'role_id', 'sphere_id', 'azimuth_coordinate', 'source_coordinates', 'normalization'},
                ('role_id', 'sphere_id', 'azimuth_coordinate', 'source_coordinates'))
        if any(type(role[name]) is not str or not role[name] for name in ('role_id', 'sphere_id')):
            raise ValueError('Role and sphere IDs must be nonempty text')
        axis, source = role['azimuth_coordinate'], role['source_coordinates']
        if type(axis) is not int or axis not in block.contract.coordinates:
            raise ValueError('Role azimuth is not a declared native coordinate')
        if source is not None and (not isinstance(source, (list, tuple)) or len(source) != 3 or any(
                type(c) is not int or c not in block.contract.coordinates for c in source)):
            raise ValueError('Role action must name three admitted native contact coordinates or null')
        if role.get('normalization', 'INITIAL_ACTION') != 'INITIAL_ACTION':
            raise ValueError('The registered action chart uses each role\'s own INITIAL_ACTION normalization')
        roles.append({'role_id': role['role_id'], 'sphere_id': role['sphere_id'],
                      'azimuth_coordinate': axis, 'source_coordinates': None if source is None else list(source),
                      'normalization': 'INITIAL_ACTION'})
    ids = [role['role_id'] for role in roles]
    if len(set(ids)) != len(ids):
        raise ValueError('Motion role IDs must be distinct; shared coordinates retain distinct roles')
    aliases = raw.get('aliases', {})
    if not isinstance(aliases, dict) or any(type(k) is not str or not k or k in ids or v not in ids
                                            for k, v in aliases.items()):
        raise ValueError('Role aliases must uniquely name existing declared roles')
    readouts = raw.get('available_readouts', _default_readouts(roles) if registered else [])
    if not isinstance(readouts, list) or any(not isinstance(item, dict) for item in readouts):
        raise ValueError('Available readouts must be an explicit descriptor list')
    history = raw.get('complete_history_readout', False)
    if type(history) is not bool:
        raise ValueError('complete_history_readout must be an explicit boolean')
    result = {'schema': PROFILE_SCHEMA, 'profile_id': raw['profile_id'], 'roles': roles,
              'aliases': aliases, 'available_readouts': readouts,
              'complete_history_readout': history,
              'default_motion': raw.get('default_motion'),
              'readout_context': raw.get('readout_context', 'SOURCE_DECLARATION'),
              'resolution': 'REGISTERED_NATIVE_SOURCE' if registered else 'EXPLICIT_SOURCE_PROFILE',
              'source_binding': block.contract.source_binding,
              'physical_spin_or_orbit_assigned': False}
    if 'observation_reports' in raw:
        if not isinstance(raw['observation_reports'], list):
            raise ValueError('Declared observation_reports must be a source report descriptor list')
        result['observation_reports'] = canonical(raw['observation_reports'])
    return canonical(result)


def resolve_profile(block):
    """Resolve explicit roles or the exact registered H980 J4 source roster."""
    explicit = block.contract.motion_profile
    if explicit is not None:
        return _normalize_profile(block, explicit)
    base = Path(__file__).resolve().parent
    registry = json.loads((base / 'motion_profiles.json').read_text())
    row = registry['profiles'][0]
    calibration = sha256((base / row['calibration_file']).read_bytes()).hexdigest()
    prefix = row['source_binding_prefix'] + calibration + ':rho='
    binding = block.contract.source_binding
    if not binding.startswith(prefix):
        return None
    text = binding[len(prefix):]
    if not text.isdigit() or str(int(text)) != text or int(text) < 1:
        return None
    from .native import j4_matrix
    try:
        expected = j4_matrix(int(text))
    except ValueError:
        return None
    if any(len(receiver.coordinates) != 3 or receiver.matrix != expected for receiver in block.contract.receivers):
        return None
    if tuple(block.contract.contact_coordinates or ()) not in [receiver.coordinates for receiver in block.contract.receivers]:
        return None
    roles, defaults = [], []
    for receiver in block.contract.receivers:
        for declaration in row['roles']:
            roles.append({'role_id': receiver.name + '.' + declaration['name'],
                          'sphere_id': receiver.name,
                          'azimuth_coordinate': receiver.coordinates[declaration['azimuth_slot']],
                          'source_coordinates': list(receiver.coordinates),
                          'normalization': row['normalization']})
        turn = _positive_label(block, receiver.coordinates[0])
        partner = _positive_label(block, receiver.coordinates[2])
        if turn is not None and partner is not None:
            defaults.append({'role_id': receiver.name + '.endpoint_a', 'event': turn, 'after_packet': [partner]})
    default_motion = {'kind': 'GOLDEN', 'roles': defaults} if len(defaults) == len(block.contract.receivers) else None
    return _normalize_profile(block, {'profile_id': row['profile_id'], 'roles': roles,
                                     'default_motion': default_motion,
                                     'readout_context': row['readout_context']}, registered=True)


def _validated_history(block, native):
    if not isinstance(native, dict) or any(field not in native for field in ('initial', 'program', 'states')):
        raise ValueError('Motion annotation needs explicit complete initial/program/state associations')
    if not isinstance(native['program'], (list, tuple)) or not isinstance(native['states'], (list, tuple)):
        raise ValueError('Program and states must be complete ordered sequences')
    states = [block.contract.admit_state(q) for q in native['states']]
    program = list(native['program'])
    if len(states) != len(program) + 1 or not states or tuple(native['initial']) != states[0]:
        raise ValueError('Native state history is incomplete or has a different original initial state')
    if any(q not in block.state_set for q in states):
        raise ValueError('Motion state lies outside the declared source domain')
    for index, event in enumerate(program):
        if type(event) is not str or not any(row[1] == event and row[2] == states[index + 1]
                                            for row in block.outgoing.get(states[index], ())):
            raise ValueError('Motion history does not follow the admitted labelled native transitions')
    return program, states


def _action(state, coordinates, source):
    if source is None:
        return None
    values = dict(zip(coordinates, state, strict=True))
    return Fraction(common.contact(tuple(values[c] for c in source)))


def annotate_history(block, native, log_class=None, spec=None, *, _summaries=True, _validation=False, _telemetry=True):
    """Annotate actual complete native states without another native execution."""
    program, states = _validated_history(block, native)
    if _telemetry:
        if _validation:
            _STATS['checkpoint_states_revalidated'] += len(states)
        else:
            _STATS['full_annotations'] += 1; _STATS['new_states_annotated'] += len(states)
    profile = resolve_profile(block) if spec is None else _normalize_profile(block, spec)
    cls = _log_class(log_class)
    coordinates = block.contract.coordinates
    lifts = dict.fromkeys(coordinates, 0)
    coordinate_records = []
    for step, state in enumerate(states):
        if step:
            event = block.events[program[step - 1]]
            lifts[event.coordinate] += event.direction
        row = {}
        for index, coordinate in enumerate(coordinates):
            lifted = states[0][index] + lifts[coordinate]
            wrapped, winding = lifted % 4, lifted // 4
            if wrapped != state[index]:
                raise AssertionError('Native phase and ordered signed lift disagree')
            row[str(coordinate)] = {'wrapped_quarter_phase': wrapped,
                                    'lifted_quartersteps': lifts[coordinate],
                                    'lifted_phase_quartersteps': lifted, 'winding': winding,
                                    'phase_pair': list(PHASE[wrapped])}
        coordinate_records.append({'step': step, 'state': list(state), 'coordinates': row})
    result = {'schema': 'GEN2_NATIVE_MOTION_HISTORY_V1', 'complete': True,
              'profile': profile, 'profile_id': None if profile is None else profile['profile_id'],
              'status': 'UNAVAILABLE' if profile is None else 'AVAILABLE',
              'mapping': {'sphere_radius': '1', 'scale': 'E_role(q)/E_role(initial)',
                          'source_action': '6-2*dot(p0,p2)+2*dot(p1,p2)',
                          'physical_size_assigned': False, 'physical_spin_or_orbit_assigned': False},
              'coordinate_records': coordinate_records, 'roles': [], 'relative_records': []}
    if profile is None:
        result['unavailable_reason'] = 'NO_REGISTERED_OR_DECLARED_SOURCE_MOTION_PROFILE'
        return canonical(result)
    for role in profile['roles']:
        energies = [_action(q, coordinates, role['source_coordinates']) for q in states]
        baseline = energies[0]
        records, accumulated, telescopes = [], cls.zero(), True
        for step, (state, energy) in enumerate(zip(states, energies, strict=True)):
            phase = coordinate_records[step]['coordinates'][str(role['azimuth_coordinate'])]
            positive = baseline is not None and baseline > 0 and energy is not None and energy > 0
            edge_positive = energy is not None and energy > 0 and (step == 0 or (energies[step - 1] is not None and energies[step - 1] > 0))
            ratio = Fraction(1) if step == 0 and edge_positive else energy / energies[step - 1] if edge_positive else None
            delta = cls.from_positive_rational(ratio) if ratio is not None else None
            if delta is None:
                telescopes = False
            elif telescopes:
                accumulated = accumulated + delta
            scale = energy / baseline if positive else None
            logarithm = cls.from_positive_rational(scale) if positive else None
            if positive:
                cosine, sine = phase['phase_pair']
                denominator = 1 + scale * scale
                sphere = (2 * scale * cosine / denominator, 2 * scale * sine / denominator,
                          (1 - scale * scale) / denominator)
                norm = sum(value * value for value in sphere)
                if norm != 1:
                    raise AssertionError('Exact fixed-sphere point does not have unit norm')
                status = 'AVAILABLE'
            else:
                sphere, norm = None, None
                status = 'SOURCE_ACTION_UNAVAILABLE' if baseline is None or energy is None else 'NONPOSITIVE_SOURCE_ACTION'
            records.append({'step': step, 'event': None if step == 0 else program[step - 1],
                            'state': list(state), 'source_action': None if energy is None else str(energy),
                            'scale': None if scale is None else str(scale),
                            'log_scale': None if logarithm is None else logarithm.to_dict(),
                            'edge_action_ratio': None if ratio is None else str(ratio),
                            'delta_log_scale': None if delta is None else delta.to_dict(),
                            **phase, 'sphere_point': None if sphere is None else list(map(str, sphere)),
                            'sphere_norm_squared': None if norm is None else str(norm), 'status': status})
        if telescopes and accumulated.compare(cls.from_positive_rational(energies[-1] / baseline)) != 0:
            raise AssertionError('Source log increments do not telescope to original-normalized endpoint')
        result['roles'].append({**role, 'initial_source_action': None if baseline is None else str(baseline),
                                'records': records, 'status': 'AVAILABLE' if all(r['status'] == 'AVAILABLE' for r in records) else 'PARTIAL',
                                'endpoint_log_scale': records[-1]['log_scale'],
                                'accumulated_delta_log': accumulated.to_dict() if telescopes else None,
                                'log_ratios_telescope_exactly': telescopes})
    for step in range(len(states)):
        pairs = []
        for left, right in combinations(result['roles'], 2):
            a, b = left['records'][step], right['records'][step]
            relative = a['lifted_phase_quartersteps'] - b['lifted_phase_quartersteps']
            pairs.append({'left_role': left['role_id'], 'right_role': right['role_id'],
                          'lifted_relative_quartersteps': relative,
                          'relative_write_quartersteps': a['lifted_quartersteps'] - b['lifted_quartersteps'],
                          'wrapped_quarter_phase': relative % 4, 'phase_pair': list(PHASE[relative % 4])})
        result['relative_records'].append({'step': step, 'pairs': pairs})
    if any(role['status'] != 'AVAILABLE' for role in result['roles']):
        result['status'] = 'PARTIAL'
    if _summaries:
        from .history_summary import summarize
        from .quantities import source_quantity
        for role in result['roles']:
            points, edges = _summary_points(native, role['records'], 0)
            quantity = source_quantity(block, 'SOURCE_ACTION', role=role['role_id'],
                                       reference_state=native['initial'], scope='HISTORY')
            binding = {'contract_id': block.contract_id, 'role_id': role['role_id'],
                       'source_coordinates': role['source_coordinates'],
                       'profile_id': profile['profile_id'], 'original_state': native['initial']}
            role['history_summary'] = summarize(quantity, binding, points, edges, cls,
                                               _work='VALIDATION' if _validation else 'UPDATE')
    return canonical(result)


def _summary_points(native, records, start):
    points = [{'id': 'state:' + str(i), 'state': native['states'][i],
               'action': records[i - start]['source_action']} for i in range(start, start + len(records))]
    edges = [{'id': 'edge:' + str(i), 'before': 'state:' + str(i), 'after': 'state:' + str(i + 1),
              'event': native['program'][i]} for i in range(max(0, start - 1), start + len(records) - 1)]
    return points, edges


def _append_annotation(block, previous, native, cls):
    """Reuse all old source/role records; annotate only the new suffix and boundary."""
    count = len(previous['coordinate_records'])
    added = len(native['states']) - count
    if added < 0:
        raise ValueError('Motion append shortened its retained native history')
    if not added:
        return previous
    suffix = {'initial': native['states'][count - 1], 'states': native['states'][count - 1:],
              'program': native['program'][count - 1:]}
    fresh = annotate_history(block, suffix, cls, _summaries=False, _telemetry=False)
    result = deepcopy(previous)
    boundary = previous['coordinate_records'][-1]['coordinates']
    for offset, row in enumerate(fresh['coordinate_records'][1:], count):
        row['step'] = offset
        for coordinate, phase in row['coordinates'].items():
            old = boundary[coordinate]
            phase['lifted_quartersteps'] += old['lifted_quartersteps']
            phase['lifted_phase_quartersteps'] += old['lifted_phase_quartersteps'] - old['wrapped_quarter_phase']
            phase['winding'] = phase['lifted_phase_quartersteps'] // 4
        result['coordinate_records'].append(row)
    from .history_summary import append as append_summary
    for old_role, new_role in zip(result['roles'], fresh['roles'], strict=True):
        baseline = None if old_role['initial_source_action'] is None else Fraction(old_role['initial_source_action'])
        accumulated = None if old_role['accumulated_delta_log'] is None else cls.from_dict(old_role['accumulated_delta_log'])
        incoming = []
        for offset, row in enumerate(new_role['records'][1:], count):
            row['step'] = offset
            row.update(result['coordinate_records'][offset]['coordinates'][str(old_role['azimuth_coordinate'])])
            energy = None if row['source_action'] is None else Fraction(row['source_action'])
            positive = baseline is not None and baseline > 0 and energy is not None and energy > 0
            if positive:
                scale = energy / baseline
                log = cls.from_positive_rational(scale)
                cosine, sine = row['phase_pair']; denominator = 1 + scale * scale
                sphere = (2 * scale * cosine / denominator, 2 * scale * sine / denominator,
                          (1 - scale * scale) / denominator)
                if sum(x * x for x in sphere) != 1:
                    raise AssertionError('Incremental fixed-sphere norm differs')
                row.update(scale=str(scale), log_scale=log.to_dict(), sphere_point=list(map(str, sphere)),
                           sphere_norm_squared='1', status='AVAILABLE')
            else:
                row.update(scale=None, log_scale=None, sphere_point=None, sphere_norm_squared=None,
                           status='SOURCE_ACTION_UNAVAILABLE' if baseline is None or energy is None else 'NONPOSITIVE_SOURCE_ACTION')
            if row['delta_log_scale'] is None:
                accumulated = None
            elif accumulated is not None:
                accumulated = accumulated + cls.from_dict(row['delta_log_scale'])
            incoming.append(row)
        old_role['records'] += incoming
        old_role['endpoint_log_scale'] = incoming[-1]['log_scale']
        old_role['accumulated_delta_log'] = None if accumulated is None else accumulated.to_dict()
        old_role['log_ratios_telescope_exactly'] = accumulated is not None
        if old_role['status'] != 'AVAILABLE' or any(r['status'] != 'AVAILABLE' for r in incoming):
            old_role['status'] = 'PARTIAL'
        if accumulated is not None and accumulated.compare(cls.from_dict(incoming[-1]['log_scale'])) != 0:
            raise AssertionError('Incremental log telescope differs from original baseline')
        points, edges = _summary_points(native, incoming, count)
        old_role['history_summary'] = append_summary(old_role['history_summary']['checkpoint'], points, edges, cls)
    for step in range(count, len(native['states'])):
        pairs = []
        for left, right in combinations(result['roles'], 2):
            a, b = left['records'][step], right['records'][step]
            relative = a['lifted_phase_quartersteps'] - b['lifted_phase_quartersteps']
            pairs.append({'left_role': left['role_id'], 'right_role': right['role_id'],
                          'lifted_relative_quartersteps': relative,
                          'relative_write_quartersteps': a['lifted_quartersteps'] - b['lifted_quartersteps'],
                          'wrapped_quarter_phase': relative % 4, 'phase_pair': list(PHASE[relative % 4])})
        result['relative_records'].append({'step': step, 'pairs': pairs})
    if any(role['status'] != 'AVAILABLE' for role in result['roles']):
        result['status'] = 'PARTIAL'
    _STATS['incremental_appends'] += 1; _STATS['new_states_annotated'] += added
    _STATS['boundary_states_revalidated'] += 1; _STATS['prior_states_reused'] += count
    return canonical(result)


def motion_readout(block, *, initial, program, states, spec=None, log_class=None):
    return annotate_history(block, {'initial': initial, 'program': program, 'states': states}, log_class, spec)


def _intent(block, raw, profile):
    _fields(raw, {'kind', 'packets', 'roles'}, ('packets',))
    if profile is None:
        raise ValueError('Native motion intent requires a registered or explicitly declared role profile')
    defaults = profile.get('default_motion') or {}
    kind = raw.get('kind', defaults.get('kind', 'GOLDEN'))
    if kind != 'GOLDEN':
        raise ValueError('Unknown source motion scheduling policy')
    packets = raw['packets']
    if type(packets) is not int or packets < 0:
        raise ValueError('Motion packet count must be a nonnegative integer')
    requested = raw.get('roles', defaults.get('roles'))
    if not isinstance(requested, (list, tuple)) or not requested:
        raise ValueError('This profile requires an explicit nonempty motion role/event roster')
    lookup = {role['role_id']: role for role in profile['roles']}
    roles = []
    for row in requested:
        _fields(row, {'role_id', 'event', 'after_packet'}, ('role_id', 'event'))
        role_id = profile['aliases'].get(row['role_id'], row['role_id'])
        if role_id not in lookup or row['event'] not in block.events:
            raise ValueError('Motion intent has an unknown role or event label')
        if block.events[row['event']].coordinate != lookup[role_id]['azimuth_coordinate']:
            raise ValueError('Scheduled role Write does not act on that role\'s declared azimuth')
        partner = row.get('after_packet', [])
        if not isinstance(partner, (tuple, list)) or any(type(e) is not str or e not in block.events for e in partner):
            raise ValueError('After-packet interactions must be declared native event labels')
        roles.append({'role_id': role_id, 'event': row['event'], 'after_packet': list(partner)})
    if len({r['role_id'] for r in roles}) != len(roles):
        raise ValueError('Motion intent repeats a role; give each coupled role its own identity')
    return {'kind': kind, 'packets': packets, 'roles': roles}


def _binding(log_class):
    base = Path(__file__).resolve().parent
    names = ('motion.py', 'golden.py', 'motion_profiles.json', 'history_summary.py', 'quantities.py', 'contracts.py', 'compiler.py',
             'native.py', 'exact.py', 'dependencies/common_reception.py',
             'dependencies/native/t18.py', 'dependencies/J4_RESPONSES.jsonl')
    result = {name: sha256((base / name).read_bytes()).hexdigest() for name in names}
    result['formal_log_source'] = _LOG_SOURCE_HASHES[log_class]
    return result


def _native(block, initial, program, states, view):
    energies = [block.contacts[tuple(q)] for q in states]
    return canonical({'schema': 'SLC_GEN2_FORWARD_V1', 'contract_id': block.contract_id,
                      'initial': initial, 'program': program, 'states': states,
                      'observations': [block.observe(tuple(q), view) for q in states],
                      'directions': [block.events[event].direction for event in program],
                      'contact_profile': energies,
                      'barrier': None if any(e is None for e in energies) else max(energies) - energies[0],
                      'view': view})


def _seal(body):
    body = canonical(body)
    return {'body': body, 'sha256': digest(body)}


def _state(block, initial, intent, profile, view, log_class):
    q = block.contract.admit_state(initial)
    if q not in block.state_set:
        raise ValueError('Motion initial state is outside the native source domain')
    native = _native(block, list(q), [], [list(q)], view)
    return {'schema': CHECKPOINT_SCHEMA, 'contract': block.contract.to_dict(),
            'implementation_binding': _binding(log_class), 'profile': profile,
            'intent': intent, 'native': native, 'motion': annotate_history(block, native, log_class),
            'cursor': golden.initial_cursor(intent['packets']), 'schedule_records': []}


def _motion_result(block, body, *, blocked=None):
    if len(_MOTION_VERIFIED) >= 16:
        _MOTION_VERIFIED.pop(next(iter(_MOTION_VERIFIED)))
    _MOTION_VERIFIED[canonical_bytes(body)] = True
    result = deepcopy(body['native'])
    result['motion'] = deepcopy(body['motion'])
    result['motion']['execution'] = {'intent': body['intent'], 'cursor': body['cursor'],
                                    'schedule_records': body['schedule_records'],
                                    'rounding_law': 'K_n=floor(6*n-2*n*sqrt(5)+1/2)',
                                    'native_phase_resolution_turns': '1/4'}
    role_lookup = {role['role_id']: role for role in body['profile']['roles']}
    executed_counts = {}
    for record in body['schedule_records']:
        counts = executed_counts.setdefault((record['role_id'], record['packet']), [0, 0])
        counts[record['kind'] == 'AFTER_PACKET'] += 1
    scheduled = []
    for role in body['intent']['roles']:
        axis = role_lookup[role['role_id']]['azimuth_coordinate']
        phase = body['native']['initial'][block.contract.coordinates.index(axis)]
        direction = block.events[role['event']].direction
        rows = []
        for packet in range(1, body['intent']['packets'] + 1):
            row = golden.packet_target(packet, direction=direction, initial_phase=phase)
            turns, partners = executed_counts.get((role['role_id'], packet), (0, 0))
            row.update(executed_turn_writes=turns, executed_after_packet_writes=partners,
                       turn_packet_complete=turns == row['packet_quarters'],
                       whole_role_packet_complete=turns == row['packet_quarters'] and partners == len(role['after_packet']))
            rows.append(row)
        scheduled.append({'role_id': role['role_id'], 'event': role['event'], 'initial_phase': phase,
                          'account': 'DESIGNATED_ROLE_TURN_WRITES_WITH_SHARED_INTERACTIONS_SEPARATE', 'rows': rows})
    result['motion']['execution']['role_schedules'] = scheduled
    result['complete'] = body['cursor']['complete']
    result['motion_status'] = 'EVENT_UNAVAILABLE' if blocked else 'COMPLETE' if result['complete'] else 'PAUSED'
    if blocked:
        result['unavailable_event'] = blocked
    result['motion_checkpoint'] = _seal(body)
    return canonical(result)


def _advance(block, body, max_writes, log_class):
    if max_writes is not None and (type(max_writes) is not int or max_writes < 0):
        raise ValueError('Chunk max_writes must be a nonnegative exact integer or omitted')
    native, cursor = body['native'], body['cursor']
    count, blocked = 0, None
    while not cursor['complete'] and (max_writes is None or count < max_writes):
        planned = golden.peek_event(body['intent'], cursor)
        before = tuple(native['states'][-1])
        if not any(row[1] == planned['event'] for row in block.outgoing.get(before, ())):
            blocked = {'event': planned['event'], 'state': list(before), 'cursor': dict(cursor)}
            break
        after = block.forward(before, planned['event'])
        native['program'].append(planned['event'])
        native['states'].append(list(after))
        native['observations'].append(canonical(block.observe(after, native['view'])))
        native['directions'].append(block.events[planned['event']].direction)
        energy = block.contacts[after]
        native['contact_profile'].append(canonical(energy))
        if energy is None or native['barrier'] is None:
            native['barrier'] = None
        else:
            native['barrier'] = canonical(max(rational(native['barrier']), energy - rational(native['contact_profile'][0])))
        body['schedule_records'].append(planned)
        cursor = golden.advance_cursor(body['intent'], cursor)
        count += 1
    body['cursor'] = cursor
    body['native'] = canonical(native)
    body['motion'] = _append_annotation(block, body['motion'], body['native'], log_class)
    return _motion_result(block, body, blocked=blocked)


def execute_motion(block, initial, motion, view='JOINT', max_writes=None, log_class=None):
    cls = _log_class(log_class)
    profile = resolve_profile(block)
    intent = _intent(block, motion, profile)
    body = _state(block, initial, intent, profile, view, cls)
    return _advance(block, body, max_writes, cls)


def resume_motion(block, checkpoint, max_writes=None, log_class=None):
    """Restore original normalization, roles, word and midpacket cursor exactly.

    Validation uses compiled transition tables and source annotation; only new
    Writes after the checkpoint call the native forward executor.
    """
    _fields(checkpoint, {'body', 'sha256'}, ('body', 'sha256'))
    body = deepcopy(checkpoint['body'])
    required = {'schema', 'contract', 'implementation_binding', 'profile', 'intent',
                'native', 'motion', 'cursor', 'schedule_records'}
    _fields(body, required, required)
    cls = _log_class(log_class)
    if body['schema'] != CHECKPOINT_SCHEMA or digest(body) != checkpoint['sha256']:
        raise ValueError('Motion checkpoint schema or integrity mismatch')
    profile = resolve_profile(block)
    if body['contract'] != block.contract.to_dict() or body['implementation_binding'] != _binding(cls) or body['profile'] != profile:
        raise ValueError('Motion checkpoint source, role profile or implementation changed')
    if canonical_bytes(body) in _MOTION_VERIFIED:
        return _advance(block, body, max_writes, cls)
    intent = _intent(block, body['intent'], profile)
    if intent != body['intent']:
        raise ValueError('Motion checkpoint intent is not canonical')
    native = body['native']
    program, states = _validated_history(block, native)
    expected_native = _native(block, list(states[0]), program, [list(q) for q in states], native['view'])
    if expected_native != native or annotate_history(block, native, cls, _validation=True) != body['motion']:
        raise ValueError('Motion checkpoint history, source normalization or phase/sphere readouts changed')
    cursor, records = golden.initial_cursor(intent['packets']), []
    for label in program:
        planned = golden.peek_event(intent, cursor)
        if planned is None or planned['event'] != label:
            raise ValueError('Retained word does not match its declared signed golden role schedule')
        records.append(planned)
        cursor = golden.advance_cursor(intent, cursor)
    if cursor != body['cursor'] or records != body['schedule_records']:
        raise ValueError('Golden packet progress, signed role association or cursor was altered')
    return _advance(block, body, max_writes, cls)
