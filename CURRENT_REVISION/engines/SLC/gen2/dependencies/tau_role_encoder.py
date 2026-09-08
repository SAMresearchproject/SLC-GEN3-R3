"""Round-one association recipes; native laws and banks are PILOT3 inputs.

The observed record, membership/role assignment, and native response are
separate values. Bookkeeping and targets are never accepted by this encoder.
"""
from itertools import product
import numpy as np
from CURRENT_REVISION.domains.ATOM3D.tau_pilot_v3 import encode_slc as base
from CURRENT_REVISION.domains.ATOM3D.tau_pilot_v3 import retained_features as native
from CURRENT_REVISION.domains.ATOM3D.tau_pilot_v3.legacy_features import A3D

S = 4096
ARMS = ('q3_ret', 'a3d41_ret', 'grammar_relative_ret')
COLUMNS = {ARMS[0]: np.r_[0:83, 99:139], ARMS[1]: np.arange(295),
           ARMS[2]: np.arange(365)}


def recipes():
    result = []
    for amount, group, direction in product(('energy', 'momentum', 'equal'),
                                           ('near', 'narrow', 'charge_mixed'),
                                           ('jet', 'centered')):
        result.append(dict(id=f'{amount}_{group}_{direction}', amount=amount,
                           group=group, direction=direction, shuffle_seed=None))
    for seed in (17, 29):
        result.append(dict(id=f'energy_shuffle_{seed}', amount='energy', group='near',
                           direction='jet', shuffle_seed=seed))
    return result


RECIPES = recipes()


def observe(record):
    """Original measurements stay at the caller; the current executor uses Q4096."""
    observed = base.encode(record, arm='q3_avg')
    order = observed['canonical_permutation']
    observed['momentum_fraction'] = np.array(
        [base.geometry(p)[1] for p in record['reco_cand_p4s']])[order] / observed['jet'][1]
    # PILOT3 ties have identical PILOT3 operands. A new momentum operand can
    # distinguish them, so that measurement resolves such ties here.
    q, u, valid, types = (observed[k] for k in ('q', 'u', 'valid', 'types'))
    order = np.array(sorted(range(len(q)), key=lambda i: (
        -int(q[i, 0]), int(types[i]), int(q[i, 3]), *u[i].tolist(),
        int(valid[i, 0]), int(q[i, 4]), int(valid[i, 1]), int(q[i, 5]),
        float(observed['momentum_fraction'][i]))), np.int64)
    for key in ('q', 'u', 'valid', 'types', 'momentum_fraction', 'canonical_permutation'):
        observed[key] = observed[key][order]
    return observed


def members(q, u, rule):
    n = len(q)
    distances = np.sum((u[:, None, :] - u[None, :, :])**2, axis=2)
    radius = 819 if rule == 'narrow' else 1638
    admitted = distances <= radius**2
    if rule == 'charge_mixed':
        admitted &= q[:, 3, None] * q[None, :, 3] <= 0
    np.fill_diagonal(admitted, False)
    pairs = np.column_stack(np.where(np.triu(admitted, 1))).astype(np.int64)
    triples = set()
    for anchor in range(n):
        neighbours = sorted(np.flatnonzero(admitted[anchor]),
                            key=lambda k: (int(distances[anchor, k]), int(k)))
        if len(neighbours) >= 2:
            triples.add(tuple(sorted((anchor, int(neighbours[0]), int(neighbours[1])))))
    return pairs.reshape(-1, 2), np.array(sorted(triples), np.int64).reshape(-1, 3)


def group_packet(q, u, indices, centered):
    arity = indices.shape[1]
    directions = u[indices].copy()
    if centered:
        # Exact arity * (u_i - mean_group(u)); no extra rounding step.
        directions = arity * directions - directions.sum(axis=1, keepdims=True)
    phase = np.argmax(np.stack((directions[:, :, 0], directions[:, :, 1],
                                -directions[:, :, 0], -directions[:, :, 1]), axis=2), axis=2)
    amount = q[indices, 0]
    divisor = np.maximum(amount.max(axis=1, initial=0), 1)[:, None]
    whole, rem = np.divmod(12 * amount, divisor)
    shape_components = whole + ((2*rem > divisor) | ((2*rem == divisor) & (whole % 2 == 1)))
    shape = shape_components @ (13**np.arange(arity-1, -1, -1, dtype=np.int64))
    state = phase @ (4**np.arange(arity-1, -1, -1, dtype=np.int64))
    return dict(indices=indices, directions=directions, shape_components=shape_components,
                shape=shape, phase=state, amount=amount,
                zero_transverse=int(np.sum(np.all(directions[:, :, :2] == 0, axis=2))))


def assign(observed, recipe):
    q = observed['q'].copy(); u = observed['u']
    if recipe['amount'] == 'momentum':
        q[:, 0] = np.rint(S*np.clip(observed['momentum_fraction'], 0, 2)).astype(np.int64)
    elif recipe['amount'] == 'equal':
        q[:, 0] = int(np.rint(S/len(q)))
    if recipe['shuffle_seed'] is not None:
        # The permutation depends on recipe and multiplicity, never row/file IDs.
        order = np.random.default_rng(recipe['shuffle_seed']+len(q)).permutation(len(q))
        q[:, 0] = q[order, 0]
    pairs, triples = members(q, u, recipe['group'])
    centered = recipe['direction'] == 'centered'
    return dict(q=q, u=u, pairs=group_packet(q, u, pairs, centered),
                triples=group_packet(q, u, triples, centered), centered=centered)


def execute(observed, assignment, trace=False):
    q, u = assignment['q'], assignment['u']
    valid, types = observed['valid'], observed['types']
    scalar, scalar_num, scalar_count = base.exact_features(q, u, valid, types, observed['jet'])
    pair, triad = assignment['pairs'], assignment['triples']
    ps, pq, ts, tq = pair['shape'], pair['phase'], triad['shape'], triad['phase']
    num = np.zeros(352, np.int64); counts = np.zeros(352, np.int64)
    if len(ts):
        num[:16] = native.checked_sum(A3D[ts, tq]); counts[:16] = len(ts)
    num[32:72], counts[32:72] = native.current_features(q, u, valid, types, scalar_count, len(ps), len(ts))
    if len(ts):
        tq_flat = q[triad['indices']].reshape(-1, 6)
        tu_flat = triad['directions'].reshape(-1, 3)
        ids = np.arange(len(tq_flat)).reshape(-1, 3)
        num[72:228] = native.continuous(tq_flat, tu_flat, ids); counts[72:228] = len(ts)
    for bank, addresses, phases, target in (
            (native.RP, ps, pq, slice(282, 288)), (native.RT, ts, tq, slice(288, 298)),
            (native.RPRET, ps, pq, slice(298, 316)), (native.RTRET, ts, tq, slice(316, 352))):
        if len(addresses):
            num[target] = native.checked_sum(bank[addresses, phases]); counts[target] = len(addresses)
    denominators = native.DENOMINATORS.copy()
    if assignment['centered']:
        denominators[72:228] *= 9  # quadratic response to a direction divided by 3
    values = (num.astype(np.float64)/denominators/np.maximum(counts, 1)).astype(np.float32)
    # Common observations retain their original measurement meaning across maps.
    x = np.r_[observed['x'][:47], scalar[47:83], values[:16], values[32:228], values[282:352]]
    assert x.shape == (365,) and np.all(np.isfinite(x))
    diagnostic = np.array([len(q), len(ps), len(ts), pair['zero_transverse'],
                           triad['zero_transverse'], np.sum(q[:, 0] == 0)], np.int64)
    result = {'x': x, 'diagnostic': diagnostic}
    if trace:
        result.update(native_num=scalar_num, native_count=scalar_count,
                      extra_num=num, extra_count=counts, denominators=denominators)
    return result


def encode(record, selected=None, trace=False):
    observed = observe(record)
    selected = RECIPES if selected is None else selected
    results = [execute(observed, assign(observed, recipe), trace) for recipe in selected]
    return observed, results


def encode_chunk(rows):
    result = []
    for record in rows:
        try:
            observed, maps = encode(record)
            result.append(dict(features=np.stack([m['x'] for m in maps]),
                               diagnostics=np.stack([m['diagnostic'] for m in maps]),
                               jet=observed['jet'], basis=observed['basis'],
                               stats=observed['stats']))
        except (base.InvalidRecord, OverflowError) as error:
            result.append({'invalid': str(error)})
    return result


def gpu_packet(observed, assignment):
    """Compile membership once; the 780M executes the original native kernel."""
    q, u = assignment['q'], assignment['u']; n = len(q)
    triad = assignment['triples']; pair = assignment['pairs']
    # Original constituents supply scalar/current readouts. Distinct group
    # records supply centered vectors to their native three-owner operation.
    q_extra = q[triad['indices']].reshape(-1, 6)
    u_extra = triad['directions'].reshape(-1, 3)
    operands = dict(offsets=np.array([0, n], np.int64), q=np.r_[q, q_extra],
                    u=np.r_[u, u_extra], valid=np.r_[observed['valid'], np.zeros((len(q_extra), 2), bool)],
                    types=np.r_[observed['types'], np.zeros(len(q_extra), np.int8)])
    triples = np.arange(n, n+len(q_extra)).reshape(-1, 3)
    groups = dict(pair_offsets=np.array([0, len(pair['indices'])], np.int64),
                  pairs=np.column_stack((pair['indices'], pair['shape'], pair['phase'])),
                  triad_offsets=np.array([0, len(triples)], np.int64),
                  triads=np.column_stack((triples, triad['shape'], triad['phase'])))
    return operands, groups
