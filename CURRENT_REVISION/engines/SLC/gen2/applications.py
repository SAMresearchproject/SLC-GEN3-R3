"""Typed observation, assignment, native response and task readout interfaces.

The H986 tau mapping is an adapter. Original detector measurements and tracing
information survive independently of its numerical lowering. Source IDs and
targets never enter the learned input. Detector charge is not a native Write
sign, and the directional/amount views do not assign GEN2 reception lanes.
"""
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DEPENDENCIES = HERE / 'dependencies'
OPERATIONS = ('GEN2_TAU_ASSIGNMENT', 'GEN2_TAU_REPLAY', 'GEN2_TAU_FEATURE_CATALOG')


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _json(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(item) for item in value]
    return value


def _rational(numerator, denominator=1):
    f = Fraction(int(numerator), int(denominator))
    return f'{f.numerator}/{f.denominator}'


@lru_cache(maxsize=1)
def _source():
    # Import installed arithmetic and data only after authenticating their
    # current application bundle and the precise H986 dependency binding.
    from CURRENT_REVISION.domains.ATOM3D.tau_reco import current
    pointer, bundle = current()
    binding = json.loads((DEPENDENCIES / 'TAU_ROLE_SOURCE_BINDING.json').read_text())
    if _sha(bundle / 'MODEL_BINDING.json') != binding['installed_model_binding']['sha256']:
        raise ValueError('GEN2 tau application requires its declared PILOT3 component binding')
    if _sha(DEPENDENCIES / 'tau_role_encoder.py') != binding['adapted_encoder']['sha256']:
        raise ValueError('GEN2 tau role encoder source differs')
    if _sha(DEPENDENCIES / 'TAU_FEATURE_CATALOG.json') != binding['feature_catalog']['sha256']:
        raise ValueError('GEN2 tau feature meanings differ')
    from .dependencies import tau_role_encoder as encoder
    with np.load(bundle / 'CANDIDATE_ASSIGNMENTS.npz', allow_pickle=False) as data:
        parameters = {kind: data[kind + '_parameters'].copy() for kind in ('pair', 'triad')}
    return encoder, parameters, binding


def feature_catalog():
    _source()
    catalog = json.loads((DEPENDENCIES / 'TAU_FEATURE_CATALOG.json').read_text())
    return {'schema': 'GEN2_TAU_FEATURE_CATALOG_V1', 'source': 'H000986',
            'catalog_sha256': _sha(DEPENDENCIES / 'TAU_FEATURE_CATALOG.json'),
            'rules': catalog, 'architecture_feature_width_fixed': False}


def _recipe(encoder, selected):
    candidates = {row['id']: row for row in encoder.RECIPES}
    if isinstance(selected, str) and selected in candidates:
        return candidates[selected]
    if isinstance(selected, dict) and selected.get('id') in candidates and selected == candidates[selected['id']]:
        return selected
    raise ValueError('Unknown or changed H986 assignment recipe; use a versioned successor adapter')


def tau_assignment(payload):
    allowed = {'reconstructed', 'recipe', 'arm', 'provenance'}
    if not isinstance(payload, dict) or set(payload) - allowed:
        raise ValueError('Unknown tau assignment fields; targets and bookkeeping belong outside reconstructed inputs')
    encoder, parameters, binding = _source()
    raw = payload['reconstructed']
    if not isinstance(raw, dict) or set(raw) != set(encoder.base.INPUTS):
        raise ValueError('Reconstructed input must contain exactly the declared detector whitelist')
    # Nested p4 objects are measurements too, not an avenue for provenance.
    for p4 in [raw['reco_jet_p4'], *(raw['reco_cand_p4s'] or [])]:
        if not isinstance(p4, dict) or set(p4) != {'rho', 'eta', 'phi', 't'}:
            raise ValueError('Four-vector input must contain rho, eta, phi and t only')
    recipe = _recipe(encoder, payload.get('recipe', 'energy_near_jet'))
    arm = payload.get('arm', 'grammar_relative_ret')
    if arm not in encoder.ARMS:
        raise ValueError('Unknown retained tau representation')
    observed = encoder.observe(raw)
    assigned = encoder.assign(observed, recipe)
    response = encoder.execute(observed, assigned, trace=True)
    order = observed['canonical_permutation']
    groups, tracing = [], []
    for kind, parameter_name in (('pairs', 'pair'), ('triples', 'triad')):
        packet, params = assigned[kind], parameters[parameter_name]
        arity = packet['indices'].shape[1]
        for number, indices in enumerate(packet['indices']):
            shape = packet['shape_components'][number]
            distance = np.sum((6 * shape - (72 // params.max(axis=1))[:, None] * params) ** 2, axis=1)
            matches = np.arange(len(params)) if not np.any(shape) else np.flatnonzero(distance == distance.min())
            original_directions = observed['u'][indices]
            centroid = [_rational(int(v), 4096 * arity) for v in original_directions.sum(axis=0)]
            group = {'arity': arity, 'kind': kind, 'operand_slots': indices.tolist(),
                     'assigned_amount_Q4096': packet['amount'][number].tolist(),
                     'measured_energy_fraction_Q4096': observed['q'][indices, 0].tolist(),
                     'measured_momentum_fraction': observed['momentum_fraction'][indices].tolist(),
                     'shape': shape.tolist(), 'group_centroid_jet_frame': centroid,
                     'direction_integer_numerator': packet['directions'][number].tolist(),
                     'direction_denominator': 4096 * (arity if assigned['centered'] else 1),
                     'direction_frame': 'group_centered_in_jet_basis' if assigned['centered'] else 'jet_basis',
                     'nearest_transverse_phase_address': int(packet['phase'][number]),
                     'compatible_catalog_parameters': params[matches].tolist(),
                     'compatible_count': len(matches), 'all_minimum_ties_retained': True,
                     'absolute_scale_selected': False}
            groups.append(group)
            tracing.append({'group_index': len(groups) - 1,
                            'original_constituent_indices': order[indices].tolist(),
                            'catalog_assignment_indices': matches.tolist()})
    n = len(order)
    directional_amounts = [_rational(1, n)] * n
    columns = encoder.COLUMNS[arm]
    return _json({
        'schema': 'GEN2_TAU_APPLICATION_ENVELOPE_V1',
        'observation': {'reconstructed': deepcopy(raw), 'units': {'p4_rho_t': 'GeV', 'angles': 'radian'},
                        'jet_basis': observed['basis'], 'track_validity': observed['valid'],
                        'missingness_and_clipping': observed['stats'],
                        'quantization': {'scale': 4096, 'rounding': 'nearest_ties_even',
                                         'maximum_error': observed['maximum_quantization_error']}},
        'assignment': {'adapter': 'H986_ROLE_ASSOCIATION_R01', 'recipe': deepcopy(recipe),
                       'constituent_count': n, 'arity_counts': {'one_body': n, 'pair': len(assigned['pairs']['indices']),
                                                              'three_owner': len(assigned['triples']['indices'])},
                       'directional_view': {'contribution': directional_amounts,
                                            'jet_direction_Q4096': observed['u'],
                                            'meaning': 'equal contribution per constituent, associated by canonical operand slot'},
                       'measured_amount_view': {'energy_fraction_Q4096': observed['q'][:, 0],
                                                'momentum_fraction': observed['momentum_fraction'],
                                                'meaning': 'original measured amounts retained beside directional contributions'},
                       'executed_amount_Q4096': assigned['q'][:, 0], 'groups': groups,
                       'native_receiver_lane_assignment': 'UNASSIGNED',
                       'detector_charge_is_native_write_sign': False,
                       'detector_list_order_is_encounter_time': False},
        'native_response': {'full_feature_vector': response['x'],
                            'scalar_numerators': response['native_num'], 'scalar_counts': response['native_count'],
                            'scalar_quantization_denominator': 4096 ** 2,
                            'scalar_exact_aggregates': [[[_rational(v, 4096 ** 2 * max(int(response['native_count'][g, c]), 1))
                                                          for v in response['native_num'][g, c]] for c in range(6)] for g in range(3)],
                            'extra_numerators': response['extra_num'], 'extra_counts': response['extra_count'],
                            'extra_denominators': [int(v) for v in response['denominators']],
                            'extra_exact_aggregates': [_rational(v, int(d) * max(int(c), 1)) for v, d, c in
                                                       zip(response['extra_num'], response['denominators'], response['extra_count'])],
                            'feature_catalog_sha256': binding['feature_catalog']['sha256']},
        'predictive_input': {'arm': arm, 'column_indices': columns.tolist(), 'values': response['x'][columns]},
        'task_readout': {'status': 'NO_LEARNED_READOUT_REQUESTED', 'ranking_changes_exact_ties': False},
        'provenance': deepcopy(payload.get('provenance', {})),
        'trace': {'canonical_to_original_constituent_index': order, 'groups': tracing},
    })


def tau_replay(payload):
    """Apply explicitly supplied readout parameters; never open caller paths.

    This serves serialized research replay. No checkpoint or learned head is
    selected or installed by the operation. IDs, targets and provenance remain
    outside the numerical vector accepted by the readout.
    """
    if not isinstance(payload, dict) or set(payload) != {'assignment', 'readout'}:
        raise ValueError('Tau replay requires assignment inputs and an explicit readout')
    envelope = tau_assignment(payload['assignment'])
    readout = payload['readout']
    if not isinstance(readout, dict) or set(readout) != {'parameters', 'mean', 'std', 'provenance'}:
        raise ValueError('Readout requires parameters, mean, std and separate provenance')
    p = {key: np.asarray(value, np.float32) for key, value in readout['parameters'].items()}
    if set(p) != {'w0', 'b0', 'w1', 'b1', 'w2', 'b2'}:
        raise ValueError('Readout parameter roster differs')
    width = len(envelope['predictive_input']['values'])
    # H986 normalization is float64; convert its result to the float32 model
    # input only after subtraction, division and clipping.
    mean, std = np.asarray(readout['mean'], np.float64), np.asarray(readout['std'], np.float64)
    if mean.shape != (width,) or std.shape != (width,) or np.any(std <= 0):
        raise ValueError('Readout normalization shape or scale differs')
    if any(not np.all(np.isfinite(value)) for value in [*p.values(), mean, std]):
        raise ValueError('Readout contains nonfinite values')
    if p['w0'].ndim != 2 or p['w0'].shape[0] != width:
        raise ValueError('Readout input width differs')
    h = p['w0'].shape[1]
    if p['b0'].shape != (h,) or p['w1'].shape != (h, 64) or p['b1'].shape != (64,) or p['w2'].shape != (64, 11) or p['b2'].shape != (11,):
        raise ValueError('Readout architecture differs from H986')
    x = np.asarray(envelope['predictive_input']['values'], np.float32)[None, :]
    x = np.clip((x - mean) / std, -10, 10).astype(np.float32)
    for layer in range(3):
        x = x @ p[f'w{layer}'] + p[f'b{layer}']
        if layer < 2:
            x = np.maximum(x, 0)
    if not np.all(np.isfinite(x)):
        raise ValueError('Readout produced nonfinite values')
    envelope['task_readout'] = {'status': 'EXPLICIT_RESEARCH_READOUT_EXECUTED', 'logits': x[0].tolist(),
                                'provenance': deepcopy(readout['provenance']), 'ranking_changes_exact_ties': False,
                                'new_learned_model_selected': False}
    return envelope


def dispatch(operation, payload):
    if operation == 'GEN2_TAU_ASSIGNMENT':
        return tau_assignment(payload)
    if operation == 'GEN2_TAU_REPLAY':
        return tau_replay(payload)
    if operation == 'GEN2_TAU_FEATURE_CATALOG':
        if payload:
            raise ValueError('Feature catalogue operation takes an empty payload')
        return feature_catalog()
    raise ValueError('Unknown GEN2 tau application operation: ' + operation)
