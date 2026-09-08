"""Typed observed motion channels over complete retained native histories.

Predicted chart values are candidate calculations. A channel declaration says
what can be measured; only a separately supplied measurement conditions a fiber.
"""
from fractions import Fraction
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from .exact import canonical, canonical_bytes, rational, digest


SCHEMA = 'GEN2_TYPED_MOTION_OBSERVATION_V1'
KINDS = ('SPHERE', 'SCALE', 'LOG_SCALE', 'ROLE_PHASE', 'ROLE_LIFT',
         'ROLE_WINDING', 'RELATIVE_PHASE', 'RELATIVE_LIFT')
PAIRS = ('RELATIVE_PHASE', 'RELATIVE_LIFT')
HISTORY_CHANNELS = ('ROLE_LIFT', 'ROLE_WINDING', 'RELATIVE_LIFT')


class UnavailableReadout(ValueError):
    """The native history exists, but its declared chart coordinate is undefined."""


_PROFILE_CACHE = {}
_PROFILE_IDENTITIES = {}
_PROFILE_STATS = {'profile_hits': 0, 'profile_misses': 0, 'profile_source_refreshes': 0}


def reuse_stats(reset=False):
    result = dict(_PROFILE_STATS)
    if reset:
        for key in _PROFILE_STATS: _PROFILE_STATS[key] = 0
    return result


def profile(block):
    from .motion import resolve_profile
    base = Path(__file__).resolve().parent
    names = ('observation_motion.py', 'motion.py', 'native.py', 'contracts.py',
             'motion_profiles.json', 'dependencies/common_reception.py', 'dependencies/J4_RESPONSES.jsonl')
    paths = [(name, base / name) for name in names]
    signature = tuple((name, path.stat().st_mtime_ns, path.stat().st_size) for name, path in paths)
    if signature not in _PROFILE_IDENTITIES:
        _PROFILE_IDENTITIES.clear()
        _PROFILE_IDENTITIES[signature] = {name: sha256(path.read_bytes()).hexdigest() for name, path in paths}
        _PROFILE_STATS['profile_source_refreshes'] += 1
    key = digest({'contract': block.contract.to_dict(), 'profile_sources': _PROFILE_IDENTITIES[signature]})
    if key not in _PROFILE_CACHE:
        _PROFILE_STATS['profile_misses'] += 1
        if len(_PROFILE_CACHE) >= 512: _PROFILE_CACHE.pop(next(iter(_PROFILE_CACHE)))
        _PROFILE_CACHE[key] = resolve_profile(block)
    else:
        _PROFILE_STATS['profile_hits'] += 1
    return deepcopy(_PROFILE_CACHE[key])


def descriptor(raw, block):
    if not isinstance(raw, dict) or set(raw) - {'kind', 'role', 'roles', 'scope'}:
        raise ValueError('Motion readout requires only kind, role/roles and scope')
    kind, scope = raw.get('kind'), raw.get('scope', 'ENDPOINT')
    if kind not in KINDS or scope not in ('ENDPOINT', 'HISTORY'):
        raise ValueError('Unknown motion readout kind or scope')
    source = profile(block)
    if source is None:
        raise ValueError('This source has no registered or declared motion profile')
    roles = {row['role_id'] for row in source['roles']}
    if scope == 'HISTORY' or kind in HISTORY_CHANNELS:
        if source.get('complete_history_readout') is not True:
            raise ValueError('A lift/winding/trace readout needs a declared complete-history measurement channel')
    result = {'kind': kind, 'scope': scope}
    if kind in PAIRS:
        pair = raw.get('roles')
        if 'role' in raw or not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError('Relative readout requires two ordered roles')
        if pair[0] == pair[1] or any(type(role) is not str or role not in roles for role in pair):
            raise ValueError('Relative readout roles must be distinct registered roles')
        result['roles'] = list(pair)
    else:
        role = raw.get('role')
        if 'roles' in raw or type(role) is not str or role not in roles:
            raise ValueError('Readout requires a registered role')
        result['role'] = role
    return result


def available_readouts(block, raw=None):
    """Resolve declared channels; an explicit list restricts that declaration."""
    source = profile(block)
    defaults = [] if source is None else source.get('available_readouts', [])
    if not isinstance(defaults, (list, tuple)):
        raise ValueError('Profile observation channels must be a descriptor list')
    declared = [descriptor(row, block) for row in defaults]
    keys = {canonical_bytes(row) for row in declared}
    if len(keys) != len(declared):
        raise ValueError('Motion profile repeats an observed readout channel')
    if raw is None:
        return declared
    if not isinstance(raw, (list, tuple)):
        raise ValueError('Available readouts must be an explicit descriptor whitelist')
    result = [descriptor(row, block) for row in raw]
    observed = [canonical_bytes(row) for row in result]
    if len(set(observed)) != len(observed) or any(key not in keys for key in observed):
        raise ValueError('Readout whitelist must contain distinct profile-declared measurement channels')
    return result


def automatic_choices(block, declared):
    """One deterministic native/declared-readout roster, independent of target answers."""
    result = []
    width = len(next(iter(block.keys('JOINT').values())))
    for event in (None, *sorted(block.events)):
        event_name = 'PASSIVE' if event is None else event
        mode = 'ABSOLUTE' if event is None else 'DELTA'
        result.append({'label': 'AUTO:NATIVE:' + event_name + ':JOINT', 'event': event,
                       'mode': mode, 'view': 'JOINT', 'components': list(range(width)),
                       'projection': 'IDENTITY'})
        for index in range(width):
            for projection in ('IDENTITY', 'SIGN'):
                result.append({'label': f'AUTO:NATIVE:{event_name}:{index}:{projection}',
                               'event': event, 'mode': mode, 'view': 'JOINT',
                               'components': [index], 'projection': projection})
        for index, readout in enumerate(declared):
            result.append({'label': f'AUTO:MOTION:{event_name}:{index}',
                           'event': event, 'readout': readout})
    return result


def _exact_log(raw, log_class):
    if not isinstance(raw, dict) or set(raw) - {'schema', 'expression', 'coefficients'}:
        raise ValueError('Log observation requires exact prime coefficients')
    if raw.get('schema') != 'SLC_FORMAL_LOG_ELEMENT_V1' or not isinstance(raw.get('coefficients'), list):
        raise ValueError('Unknown exact formal-log observation schema')
    terms = []
    for row in raw['coefficients']:
        if not isinstance(row, dict) or set(row) != {'prime', 'coefficient'}:
            raise ValueError('Malformed formal-log coefficient')
        coefficient = row['coefficient']
        if not isinstance(coefficient, dict) or set(coefficient) != {'numerator', 'denominator'}:
            raise ValueError('Formal-log coefficients require exact numerator/denominator')
        numerator, denominator = coefficient['numerator'], coefficient['denominator']
        if type(numerator) is not int or type(denominator) is not int or denominator <= 0:
            raise ValueError('Invalid exact formal-log coefficient')
        terms.append((row['prime'], Fraction(numerator, denominator)))
    result = log_class.from_terms(terms).to_dict()
    if 'expression' in raw and raw['expression'] != result['expression']:
        raise ValueError('Log display expression disagrees with exact coefficients')
    return result


def observed_value(raw, readout, log_class, *, history_length):
    """Canonicalize supplied values without adding any candidate information."""
    if isinstance(raw, dict) and raw.get('schema') == SCHEMA:
        if set(raw) != {'schema', 'readout', 'value'} or raw['readout'] != readout:
            raise ValueError('Typed observed value belongs to another readout')
        raw = raw['value']
    kind = readout['kind']

    def one(value):
        if kind == 'LOG_SCALE':
            return _exact_log(value, log_class)
        if kind == 'SPHERE':
            if not isinstance(value, (list, tuple)) or len(value) != 3:
                raise ValueError('Sphere observation needs three exact coordinates')
            coordinates = [rational(v) for v in value]
            if sum(v * v for v in coordinates) != 1:
                raise ValueError('Observed sphere coordinate must have exact unit norm')
            return canonical(coordinates)
        value = rational(value)
        if kind == 'SCALE' and value <= 0:
            raise ValueError('Observed normalized scale must be positive')
        if kind in ('ROLE_PHASE', 'RELATIVE_PHASE') and (value.denominator != 1 or not 0 <= value < 4):
            raise ValueError('Observed wrapped phase must be an exact Z4 value')
        if kind in HISTORY_CHANNELS and value.denominator != 1:
            raise ValueError('Observed lifted quartersteps/winding must be integral')
        return canonical(value)

    if readout['scope'] == 'HISTORY':
        if not isinstance(raw, (list, tuple)) or len(raw) != history_length:
            raise ValueError('History observation must cover every original and appended native state')
        value = [one(item) for item in raw]
    else:
        value = one(raw)
    return {'schema': SCHEMA, 'readout': readout, 'value': value}


def predicted_value(block, *, initial, program, states, readout, log_class, cache=None):
    """Calculate a candidate channel value; this function does not condition a fiber."""
    from .motion import motion_readout
    key = (tuple(initial), tuple(program), tuple(tuple(q) for q in states))
    if cache is not None and key in cache:
        annotation = cache[key]
    else:
        annotation = motion_readout(block, initial=initial, program=program, states=states,
                                    log_class=log_class)
        if cache is not None:
            cache[key] = annotation
    roles = {row['role_id']: row for row in annotation['roles']}
    kind = readout['kind']
    if kind in PAIRS:
        left, right = (roles[name] for name in readout['roles'])
        values = []
        for a, b in zip(left['records'], right['records'], strict=True):
            value = a['lifted_phase_quartersteps'] - b['lifted_phase_quartersteps']
            values.append(value % 4 if kind == 'RELATIVE_PHASE' else value)
    else:
        field = {'SPHERE': 'sphere_point', 'SCALE': 'scale', 'LOG_SCALE': 'log_scale',
                 'ROLE_PHASE': 'wrapped_quarter_phase', 'ROLE_LIFT': 'lifted_phase_quartersteps',
                 'ROLE_WINDING': 'winding'}[kind]
        values = [row.get(field) for row in roles[readout['role']]['records']]
    selected = values if readout['scope'] == 'HISTORY' else values[-1]
    if selected is None or (readout['scope'] == 'HISTORY' and any(value is None for value in selected)):
        raise UnavailableReadout('Declared chart coordinate is undefined on this retained history')
    return observed_value(selected, readout, log_class, history_length=len(states))


def scalar_count(readout, history_length):
    width = 3 if readout['kind'] == 'SPHERE' else 1
    return width * (history_length if readout['scope'] == 'HISTORY' else 1)
