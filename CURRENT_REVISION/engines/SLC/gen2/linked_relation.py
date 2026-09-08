"""One explicit rational measure on complete, linked native history records."""
from fractions import Fraction
from .exact import canonical, rational


def weights_for(rows, measure):
    if not isinstance(measure, dict) or measure.get('kind') not in ('UNIFORM', 'WEIGHTS'):
        raise ValueError('Declare UNIFORM or explicit positive rational record WEIGHTS')
    allowed = {'kind'} if measure['kind'] == 'UNIFORM' else {'kind', 'values'}
    if set(measure) != allowed:
        raise ValueError('Unknown measure fields; construction amounts are not probabilities')
    values = [1] * len(rows) if measure['kind'] == 'UNIFORM' else measure['values']
    if not isinstance(values, (list, tuple)) or len(values) != len(rows):
        raise ValueError('Measure must cover the complete declared relation in roster order')
    values = [rational(value) for value in values]
    if any(value <= 0 for value in values):
        raise ValueError('History weights must be positive exact rationals')
    ids = [row['record_id'] for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError('A complete source history appears twice in the declared relation')
    return canonical(dict(zip(ids, values, strict=True)))


def restrict_weights(weights, rows):
    return {row['record_id']: weights[row['record_id']] for row in rows}


def probabilities(weights):
    total = sum((rational(value) for value in weights.values()), Fraction())
    return canonical({key: rational(value) / total for key, value in weights.items()}) if total else {}
