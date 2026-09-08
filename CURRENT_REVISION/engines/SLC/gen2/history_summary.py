"""Exact owner-defined U/D/V/maximum history summaries with append and merge.

Every edge is explicitly linked to adjacent source points. Incremental append
updates only the new edges; summaries remain linked to the complete history.
"""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from .exact import canonical, canonical_bytes, digest, rational
from .quantities import normalize_descriptor, bind_formal_log


SCHEMA = 'GEN2_LOG_HISTORY_CHECKPOINT_V1'
_VERIFIED = {}
_STATS = {'operations': 0, 'new_edges_summarized': 0, 'existing_edges_reused': 0,
          'checkpoint_edges_revalidated': 0, 'chunk_compositions': 0}


def reuse_stats(reset=False):
    if type(reset) is not bool:
        raise ValueError('Counter reset must be boolean')
    result = dict(_STATS)
    if reset:
        _STATS.update(dict.fromkeys(_STATS, 0))
    return result


def _binding(cls):
    base = Path(__file__).resolve().parent
    return {**{name: sha256((base / name).read_bytes()).hexdigest() for name in
                ('history_summary.py', 'quantities.py', 'exact.py')},
            'formal_log_source': bind_formal_log(cls)}


def _point(raw):
    if not isinstance(raw, dict) or set(raw) - {'id', 'state', 'action', 'status'} or not {'id', 'state', 'action'} <= set(raw):
        raise ValueError('A history point needs explicit id, full source state and exact action')
    if type(raw['id']) is not str or not raw['id']:
        raise ValueError('Source point IDs must be nonempty text')
    status = raw.get('status', 'MISSING' if raw['action'] is None else 'OBSERVED')
    if status not in ('OBSERVED', 'MISSING', 'UNAVAILABLE', 'UNDEFINED'):
        raise ValueError('Unknown source point availability status')
    action = None if raw['action'] is None else rational(raw['action'])
    if (status == 'OBSERVED') != (action is not None):
        raise ValueError('Observed action and missing/unavailable/undefined status differ')
    return canonical({'id': raw['id'], 'state': raw['state'], 'action': action, 'status': status})


def _edge(raw, before, after):
    if not isinstance(raw, dict) or set(raw) != {'id', 'before', 'after', 'event'}:
        raise ValueError('A history edge needs id, adjacent point IDs and its explicit source event')
    if type(raw['id']) is not str or not raw['id'] or raw['event'] is None:
        raise ValueError('A history edge requires source identity and an explicit directed event')
    if raw['before'] != before['id'] or raw['after'] != after['id']:
        raise ValueError('History edge does not connect the declared adjacent source points')
    return canonical(raw)


def _positive(point):
    return point['status'] == 'OBSERVED' and rational(point['action']) > 0


def _zero_summary(point, cls):
    zero = cls.zero().to_dict()
    return {'first_point': point['id'], 'last_point': point['id'],
            'initial_action': point['action'], 'final_action': point['action'],
            'U': zero, 'D': zero, 'V': zero, 'net': zero, 'M': zero,
            'maximizing_points': [point['id']], 'contributing_edges': [], 'edge_increments': []}


def _extend_summary(summary, before, after, edge, cls):
    delta = cls.from_positive_rational(rational(after['action']) / rational(before['action']))
    up, down = cls.from_dict(summary['U']), cls.from_dict(summary['D'])
    sign = delta.sign
    if sign > 0:
        up = up + delta
    elif sign < 0:
        down = down - delta
    net = cls.from_positive_rational(rational(after['action']) / rational(summary['initial_action']))
    maximum = cls.from_dict(summary['M'])
    comparison = net.compare(maximum)
    if comparison > 0:
        maximum, ties = net, [after['id']]
    elif comparison == 0:
        ties = summary['maximizing_points'] + [after['id']]
    else:
        ties = summary['maximizing_points']
    if (up - down).compare(net) != 0:
        raise AssertionError('Exact rise/fall balance differs from endpoint source ratio')
    summary.update(last_point=after['id'], final_action=after['action'], U=up.to_dict(), D=down.to_dict(),
                   V=(up + down).to_dict(), net=net.to_dict(), M=maximum.to_dict(), maximizing_points=ties)
    summary['contributing_edges'].append(edge['id'])
    summary['edge_increments'].append({'edge_id': edge['id'], 'delta_log': delta.to_dict(), 'direction': sign})


def _summary(body):
    valid = (len(body['segments']) == 1 and
             len(body['segments'][0]['contributing_edges']) == len(body['edges']) and
             body['segments'][0]['first_point'] == body['points'][0]['id'] and
             body['segments'][0]['last_point'] == body['points'][-1]['id'])
    if valid:
        return {'status': 'DEFINED', **deepcopy(body['segments'][0]),
                'identities': {'U_minus_D_equals_net': True, 'U_plus_D_equals_V': True}}
    return {'status': 'UNDEFINED_GAPS', 'U': None, 'D': None, 'V': None, 'net': None, 'M': None,
            'initial_action': body['points'][0]['action'], 'final_action': body['points'][-1]['action'],
            'first_point': body['points'][0]['id'], 'last_point': body['points'][-1]['id'],
            'maximizing_points': [], 'contributing_edges': [], 'edge_increments': [],
            'unavailable_points': [p['id'] for p in body['points'] if not _positive(p)],
            'segments': deepcopy(body['segments'])}


def _append(body, raw_points, raw_edges, cls):
    if not isinstance(raw_points, list) or not isinstance(raw_edges, list):
        raise ValueError('History append requires explicit ordered points and edges')
    points = [_point(p) for p in raw_points]
    needed = len(points) if body['points'] else max(0, len(points) - 1)
    if len(raw_edges) != needed:
        raise ValueError('Supply exactly one connecting source edge for each appended point')
    ids = {p['id'] for p in body['points']}
    edge_ids = {e['id'] for e in body['edges']}
    offset = 0
    for point in points:
        if point['id'] in ids:
            raise ValueError('Each retained point occurrence needs a distinct ID')
        ids.add(point['id'])
        if not body['points']:
            if _positive(point):
                body['segments'].append(_zero_summary(point, cls))
        else:
            before = body['points'][-1]
            edge = _edge(raw_edges[offset], before, point); offset += 1
            if edge['id'] in edge_ids:
                raise ValueError('Each retained source edge occurrence needs a distinct ID')
            edge_ids.add(edge['id']); body['edges'].append(edge)
            if _positive(before) and _positive(point):
                _extend_summary(body['segments'][-1], before, point, edge, cls)
            elif _positive(point):
                body['segments'].append(_zero_summary(point, cls))
        body['points'].append(point)
    if not body['points']:
        raise ValueError('A history summary needs its original reference source point')
    body['summary'] = _summary(body)
    return needed


def _seal(body):
    body = canonical(body)
    return {'body': body, 'sha256': digest(body)}


def _remember(body):
    if len(_VERIFIED) >= 64:
        _VERIFIED.pop(next(iter(_VERIFIED)))
    _VERIFIED[canonical_bytes(body)] = True


def _result(body):
    _remember(body)
    log_quantity = normalize_descriptor({'kind': 'LOG_ACTION_CHANGE', 'units': {},
        'source': body['source_binding'], 'scope': 'HISTORY', 'sign_convention': 'SIGNED_LOG',
        'normalization': {'kind': 'ORIGINAL_POSITIVE_ACTION', 'source_account': body['source_binding'],
                          'reference_point': body['points'][0]['id']},
        'reference_state': body['points'][0]['state'], 'frame': body['quantity']['frame']})
    return {'schema': 'GEN2_LOG_HISTORY_SUMMARY_V1', 'complete': True,
            'quantity': deepcopy(body['quantity']), 'source_binding': deepcopy(body['source_binding']),
            'summary_quantity': log_quantity, 'summary': deepcopy(body['summary']), 'checkpoint': _seal(body)}


def _admit_source(quantity, source_binding):
    if source_binding is None or source_binding == '' or source_binding == {}:
        raise ValueError('Declared source-action trace requires an explicit source/input binding')
    quantity = normalize_descriptor(quantity)
    if quantity['sign_convention'] not in ('SIGNED_VALUE', 'NONNEGATIVE_VALUE', 'POSITIVE_VALUE'):
        raise ValueError('Source-action history cannot reinterpret logarithms, information or phase coordinates as action values')
    return quantity


def summarize(quantity, source_binding, points, edges, log_class, *, _work='UPDATE'):
    quantity = _admit_source(quantity, source_binding)
    body = {'schema': SCHEMA, 'complete': True, 'implementation_binding': _binding(log_class),
            'quantity': quantity, 'source_binding': canonical(source_binding),
            'points': [], 'edges': [], 'segments': [], 'summary': None}
    count = _append(body, points, edges, log_class)
    if _work == 'VALIDATION':
        _STATS['checkpoint_edges_revalidated'] += count
    else:
        _STATS['operations'] += 1; _STATS['new_edges_summarized'] += count
    return _result(body)


def _restore(checkpoint, cls):
    if not isinstance(checkpoint, dict) or set(checkpoint) != {'body', 'sha256'}:
        raise ValueError('History summary requires its complete sealed checkpoint')
    body = deepcopy(checkpoint['body'])
    required = {'schema', 'complete', 'implementation_binding', 'quantity', 'source_binding',
                'points', 'edges', 'segments', 'summary'}
    if not isinstance(body, dict) or set(body) != required or body['schema'] != SCHEMA or body['complete'] is not True or digest(body) != checkpoint['sha256'] or body['implementation_binding'] != _binding(cls):
        raise ValueError('History checkpoint is incomplete, altered or bound to another implementation')
    if _admit_source(body['quantity'], body['source_binding']) != body['quantity']:
        raise ValueError('History checkpoint quantity is not its canonical source declaration')
    if canonical_bytes(body) not in _VERIFIED:
        reconstructed = deepcopy(body)
        reconstructed.update(points=[], edges=[], segments=[], summary=None)
        _append(reconstructed, body['points'], body['edges'], cls)
        if reconstructed != body or normalize_descriptor(body['quantity']) != body['quantity']:
            raise ValueError('History checkpoint source associations, normalization, increments or summary changed')
        _STATS['checkpoint_edges_revalidated'] += len(body['edges'])
    return body


def append(checkpoint, points, edges, log_class):
    body = _restore(checkpoint, log_class)
    prior = len(body['edges'])
    count = _append(body, points, edges, log_class)
    _STATS['operations'] += 1; _STATS['new_edges_summarized'] += count; _STATS['existing_edges_reused'] += prior
    return _result(body)


def compose(left_checkpoint, right_checkpoint, foundation=None, *, log_class=None):
    cls = log_class or foundation.hd_module.FormalLogElement
    left, right = _restore(left_checkpoint, cls), _restore(right_checkpoint, cls)
    if left['quantity'] != right['quantity'] or left['source_binding'] != right['source_binding']:
        raise ValueError('Chunk composition requires one declared source account, frame and quantity')
    if left['points'][-1] != right['points'][0]:
        raise ValueError('Chunks must share the identical boundary occurrence, source state and action')
    if left['summary']['status'] != 'DEFINED' or right['summary']['status'] != 'DEFINED':
        raise ValueError('Compose positive source segments explicitly when a chunk contains unavailable points')
    if {p['id'] for p in left['points'][:-1]} & {p['id'] for p in right['points'][1:]} or {e['id'] for e in left['edges']} & {e['id'] for e in right['edges']}:
        raise ValueError('Chunk occurrences overlap beyond their shared boundary')
    a, b = left['summary'], right['summary']
    up = cls.from_dict(a['U']) + cls.from_dict(b['U'])
    down = cls.from_dict(a['D']) + cls.from_dict(b['D'])
    net_a = cls.from_dict(a['net']); net = net_a + cls.from_dict(b['net'])
    maximum_a = cls.from_dict(a['M']); shifted_b = net_a + cls.from_dict(b['M'])
    compare = shifted_b.compare(maximum_a)
    ties = b['maximizing_points'] if compare > 0 else a['maximizing_points'] if compare < 0 else list(dict.fromkeys(a['maximizing_points'] + b['maximizing_points']))
    segment = {'first_point': a['first_point'], 'last_point': b['last_point'],
               'initial_action': a['initial_action'], 'final_action': b['final_action'],
               'U': up.to_dict(), 'D': down.to_dict(), 'V': (up + down).to_dict(),
               'net': net.to_dict(), 'M': (shifted_b if compare > 0 else maximum_a).to_dict(),
               'maximizing_points': ties,
               'contributing_edges': a['contributing_edges'] + b['contributing_edges'],
               'edge_increments': a['edge_increments'] + b['edge_increments']}
    left['points'] += right['points'][1:]; left['edges'] += right['edges']; left['segments'] = [segment]
    left['summary'] = _summary(left)
    _STATS['operations'] += 1; _STATS['chunk_compositions'] += 1
    _STATS['existing_edges_reused'] += len(left['edges'])
    return _result(left)


def dispatch(operation, payload, foundation):
    cls = foundation.hd_module.FormalLogElement
    bind_formal_log(cls)
    if operation == 'GEN2_HISTORY_SUMMARY':
        if not isinstance(payload, dict) or set(payload) != {'quantity', 'source_binding', 'points', 'edges'}:
            raise ValueError('History summary needs quantity, source binding, points and explicit edges')
        return summarize(payload['quantity'], payload['source_binding'], payload['points'], payload['edges'], cls)
    if operation == 'GEN2_HISTORY_SUMMARY_APPEND':
        if not isinstance(payload, dict) or set(payload) != {'checkpoint', 'points', 'edges'}:
            raise ValueError('History append needs checkpoint and new ordered points/edges only')
        return append(payload['checkpoint'], payload['points'], payload['edges'], cls)
    raise ValueError('Unknown logarithmic history summary operation')
