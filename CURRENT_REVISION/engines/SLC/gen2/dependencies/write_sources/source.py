"""Source-bound quadratic compiler; all evaluations are installed R4 calls."""
from fractions import Fraction as F
from itertools import product

ROLES = ('a', 'b', 'p')
PHASES = ((1, 0), (0, 1), (-1, 0), (0, -1))
PAIRS = ('CA_re', 'CA_im', 'CB_re', 'CB_im')
PHASE_CHANNELS = tuple('phase_' + str(i) for i in range(6))

def frame(q):
    return [PHASES[x][0] for x in q] + [PHASES[x][1] for x in q] + [1]

def quadratic(entries, dimension=7):
    result = [[F(0) for _ in range(dimension)] for _ in range(dimension)]
    for i, j, coefficient in entries:
        coefficient = F(coefficient)
        if i == j:
            result[i][j] += coefficient
        else:
            result[i][j] += coefficient / 2
            result[j][i] += coefficient / 2
    return [[str(x) for x in row] for row in result]

def source():
    identity = [[int(i == j) for j in range(7)] for i in range(7)]
    def action(name, entries, coefficients):
        return {'action_id': name, 'pullback': identity,
                'form': quadratic(entries), 'coefficients': coefficients}
    outputs = {'E': 'NATIVE_SOURCE_ACTION'}
    outputs.update({k: 'SIGNED_INTERACTION_COMPONENT' for k in PAIRS})
    outputs.update({'dE_' + role: 'SOURCE_ACTION_PER_PHASE_RADIAN' for role in ROLES})
    outputs.update({k: 'DIMENSIONLESS_PHASE_COMPONENT' for k in PHASE_CHANNELS})
    shell = action('shell', [(i, i, 2) for i in range(6)], {'E': 1})
    phase_actions = [action(name, [(i, 6, 1)], {name: 1})
                     for i, name in enumerate(PHASE_CHANNELS)]
    interactions = [
        action('CA_re', [(0, 2, -2), (3, 5, -2)], {'CA_re': 1, 'E': 1}),
        action('CA_im', [(3, 2, -2), (0, 5, 2)],
               {'CA_im': 1, 'dE_a': -1, 'dE_p': 1}),
        action('CB_re', [(1, 2, 2), (4, 5, 2)], {'CB_re': 1, 'E': 1}),
        action('CB_im', [(4, 2, 2), (1, 5, -2)],
               {'CB_im': 1, 'dE_b': -1, 'dE_p': 1})]
    return {'construction_id': 'RH_J4_LOCAL_ACTION_X1_GATE_V1',
        'coordinates': ['a_re', 'b_re', 'p_re', 'a_im', 'b_im', 'p_im', 'compiler_anchor'],
        'instances': [
            {'instance_id': 'phase_frame', 'kind': 'SOURCE_PHASE_READOUT', 'actions': phase_actions},
            {'instance_id': 'shell', 'kind': 'NATIVE_J4_PHASE_NORMS', 'actions': [shell]},
            {'instance_id': 'exchange', 'kind': 'SIGNED_J4_X1_JOIN',
             'activation': {'flag': 'B'}, 'actions': interactions}],
        'output_units': outputs,
        'metadata': {
            'predecessor': 'H001081', 'reference_E': 6,
            'phase_extension': 'p_j=(cos(phi_j),sin(phi_j)); native restriction phi_j=pi*q_j/2',
            'gate_join': 'Codex source-bound identification of the paper X1 witness with signed J4 pair couplings',
            'compiler_anchor': '1 for linear phase readouts only; no new physical source account',
            'physical_spin_or_orbit_assigned': False}}

def alternatives():
    return [{'values': frame(q), 'context': {'B': active}}
            for q in product(range(4), repeat=3) for active in (False, True)]

def covering_word():
    return (['W1+']*4 + ['W4+'])*4 + ['W7+']

def gate_readout():
    return {'constant': 0, 'linear': [0]*4,
            'quadratic': [[('1/8' if i == j else '0') for j in range(4)] for i in range(4)],
            'input_unit': 'SIGNED_INTERACTION_COMPONENT', 'output_unit': 'BOOLEAN_X1_GATE',
            'normalization': 'ONE_COMMON_BOOLEAN_GATE; TWO_UNIT_PHASE_PAIRS_OF_MAGNITUDE_TWO'}
