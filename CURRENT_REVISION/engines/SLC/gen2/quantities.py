"""Shared exact quantity meanings, reference accounts and unit composition."""
from .exact import canonical, digest, rational
from hashlib import sha256
from inspect import getsourcefile
from pathlib import Path


SCHEMA = 'GEN2_QUANTITY_V1'
_SEMANTIC = ('kind', 'units', 'normalization', 'reference_state', 'frame', 'scope', 'sign_convention')
_FORMAL_LOG_SOURCES = {}


def bind_formal_log(log_class, source_sha256=None):
    if log_class not in _FORMAL_LOG_SOURCES:
        _FORMAL_LOG_SOURCES[log_class] = source_sha256 or sha256(Path(getsourcefile(log_class)).read_bytes()).hexdigest()
    elif source_sha256 is not None and source_sha256 != _FORMAL_LOG_SOURCES[log_class]:
        raise ValueError('Bound formal-log source identity changed')
    return _FORMAL_LOG_SOURCES[log_class]


def normalize_exact_value(value, kind='RATIONAL'):
    if kind != 'RATIONAL':
        raise ValueError('Exact rational normalization does not reinterpret labels or information logs')
    return canonical(rational(value))


def normalize_descriptor(raw=None):
    if raw is None:
        raw = {'kind': 'SIGNED_RATIONAL', 'units': {}, 'source': 'GEN2_EXACT_RATIONAL'}
    allowed = {'schema', 'kind', 'units', 'normalization', 'reference_state', 'frame',
               'scope', 'sign_convention', 'source', 'component', 'role'}
    if not isinstance(raw, dict) or set(raw) - allowed or not {'kind', 'units'} <= set(raw):
        raise ValueError('Quantity descriptor needs declared kind and units with known fields')
    if raw.get('schema', SCHEMA) != SCHEMA or type(raw['kind']) is not str or not raw['kind']:
        raise ValueError('Unknown quantity schema or kind')
    units = raw['units']
    if not isinstance(units, dict) or any(type(k) is not str or not k for k in units):
        raise ValueError('Units must be a named exact exponent map; dimensionless is {}')
    units = {name: rational(power) for name, power in units.items()}
    units = {name: power for name, power in units.items() if power}
    scope = raw.get('scope', 'SCALAR')
    if scope not in ('SCALAR', 'ENDPOINT', 'HISTORY', 'EDGE'):
        raise ValueError('Unknown quantity scope')
    convention = raw.get('sign_convention', 'SIGNED_VALUE')
    if convention not in ('SIGNED_VALUE', 'NONNEGATIVE_VALUE', 'POSITIVE_VALUE', 'SIGNED_LOG', 'WRAPPED_PHASE', 'LIFTED_PHASE'):
        raise ValueError('Unknown quantity sign/value convention')
    return canonical({'schema': SCHEMA, 'kind': raw['kind'], 'units': units,
                      'normalization': raw.get('normalization'), 'reference_state': raw.get('reference_state'),
                      'frame': raw.get('frame'), 'scope': scope, 'sign_convention': convention,
                      'source': raw.get('source', 'DECLARED_SOURCE'),
                      'component': raw.get('component'), 'role': raw.get('role')})


def compatible_add(left, right):
    left, right = normalize_descriptor(left), normalize_descriptor(right)
    value_conventions = {'SIGNED_VALUE', 'NONNEGATIVE_VALUE', 'POSITIVE_VALUE'}
    if not all(left[field] == right[field] or (field == 'sign_convention' and
               left[field] in value_conventions and right[field] in value_conventions) for field in _SEMANTIC):
        return False
    normalization = left['normalization']
    explicit_account = isinstance(normalization, dict) and any(k in normalization for k in ('account', 'source_account'))
    if normalization is not None and not explicit_account:
        return all(left[field] == right[field] for field in ('source', 'component', 'role'))
    return True


def add_descriptor(left, right):
    left, right = normalize_descriptor(left), normalize_descriptor(right)
    if not compatible_add(left, right):
        raise ValueError('Addition/subtraction needs compatible quantity kinds, units, frames and reference accounts')
    if left == right:
        return left
    result = dict(left)
    result.update(source={'composition': 'ADDITIVE', 'sources': [left['source'], right['source']]},
                  component=None, role=None)
    return canonical(result)


def product_descriptor(left, right, division=False):
    left, right = normalize_descriptor(left), normalize_descriptor(right)
    if type(division) is not bool:
        raise ValueError('Unit composition division flag must be boolean')
    units = {key: rational(value) for key, value in left['units'].items()}
    for key, value in right['units'].items():
        units[key] = units.get(key, 0) + (-1 if division else 1) * rational(value)
    units = {key: value for key, value in units.items() if value}
    default = normalize_descriptor()
    if left == default and right == default:
        return default
    return normalize_descriptor({'kind': 'RATIO_VALUE' if division else 'PRODUCT_VALUE', 'units': units,
        'source': {'operation': 'DIVIDE' if division else 'MULTIPLY', 'left': left, 'right': right},
        'normalization': None, 'reference_state': None,
        'frame': {'left': left['frame'], 'right': right['frame']}, 'scope': 'SCALAR'})


def require_log_reference(descriptor, reference_descriptor=None):
    descriptor = normalize_descriptor(descriptor)
    if reference_descriptor is None:
        if descriptor['units']:
            raise ValueError('A dimensional logarithm needs an explicit compatible positive reference')
        return descriptor
    reference = normalize_descriptor(reference_descriptor)
    if not compatible_add(descriptor, reference):
        raise ValueError('Log reference has incompatible quantity meaning, units, frame or normalization')
    return reference


def descriptor_binding(descriptor):
    return digest(normalize_descriptor(descriptor))


def source_quantity(block, kind, role=None, reference_state=None, scope='ENDPOINT'):
    known = {'SOURCE_ACTION', 'SCALE', 'LOG_SCALE', 'INFORMATION', 'ROLE_PHASE',
             'ROLE_LIFT', 'ROLE_WINDING', 'RELATIVE_PHASE', 'RELATIVE_LIFT'}
    if kind not in known:
        raise ValueError('Unknown registered native quantity kind')
    normalized = kind in ('SCALE', 'LOG_SCALE')
    units = {'native_source_action': 1} if kind == 'SOURCE_ACTION' else {}
    convention = ('SIGNED_LOG' if kind in ('LOG_SCALE', 'INFORMATION') else
                  'WRAPPED_PHASE' if kind in ('ROLE_PHASE', 'RELATIVE_PHASE') else
                  'LIFTED_PHASE' if kind in ('ROLE_LIFT', 'RELATIVE_LIFT', 'ROLE_WINDING') else
                  'POSITIVE_VALUE' if kind == 'SCALE' else 'SIGNED_VALUE')
    return normalize_descriptor({'kind': kind, 'units': units, 'source': block.contract_id,
        'role': role, 'scope': scope, 'sign_convention': convention,
        'normalization': {'kind': 'INITIAL_ACTION', 'source_account': block.contract_id, 'role': role,
                          'reference_state': reference_state} if normalized else None,
        'reference_state': reference_state,
        'frame': {'source_coordinates': list(block.contract.coordinates)}})
