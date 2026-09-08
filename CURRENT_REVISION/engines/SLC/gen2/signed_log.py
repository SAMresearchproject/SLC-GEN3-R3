"""Exact signed rational value arithmetic with preserved contribution graphs.

HDSignature is the represented value; FormalLogElement is its log magnitude.
The operation DAG preserves every input occurrence, including cancellation.
"""
from copy import deepcopy
from hashlib import sha256
from inspect import getsourcefile
from pathlib import Path

from .exact import canonical, canonical_bytes, digest, rational
from .quantities import normalize_descriptor, compatible_add, add_descriptor, product_descriptor, require_log_reference


SCHEMA = 'GEN2_SIGNED_LOG_CHECKPOINT_V1'
_VERIFIED = {}
_STATS = {'operations': 0, 'new_nodes_evaluated': 0, 'existing_nodes_reused': 0,
          'checkpoint_nodes_revalidated': 0}


def reuse_stats(reset=False):
    if type(reset) is not bool:
        raise ValueError('Counter reset must be boolean')
    result = dict(_STATS)
    if reset:
        _STATS.update(dict.fromkeys(_STATS, 0))
    return result


def _value_convention(value, quantity):
    convention = quantity['sign_convention']
    if convention not in ('SIGNED_VALUE', 'NONNEGATIVE_VALUE', 'POSITIVE_VALUE'):
        raise ValueError('Signed rational values cannot masquerade as logarithmic or phase quantities')
    if convention == 'POSITIVE_VALUE' and value <= 0 or convention == 'NONNEGATIVE_VALUE' and value < 0:
        raise ValueError('Exact operand violates its declared positive/nonnegative quantity convention')


def _result_convention(operation, left, right):
    a, b = left['sign_convention'], right['sign_convention']
    if operation == 'SUBTRACT' or 'SIGNED_VALUE' in (a, b):
        return 'SIGNED_VALUE'
    if operation == 'ADD':
        return 'POSITIVE_VALUE' if 'POSITIVE_VALUE' in (a, b) else 'NONNEGATIVE_VALUE'
    return 'POSITIVE_VALUE' if a == b == 'POSITIVE_VALUE' else 'NONNEGATIVE_VALUE'


def _binding(foundation):
    base = Path(__file__).resolve().parent
    names = ('signed_log.py', 'quantities.py', 'exact.py')
    result = {name: sha256((base / name).read_bytes()).hexdigest() for name in names}
    result['bound_hd_source'] = sha256(Path(getsourcefile(foundation.hd_module.HDSignature)).read_bytes()).hexdigest()
    return result


def _reference(raw, quantity):
    if raw is None:
        return None
    if not isinstance(raw, dict) or set(raw) != {'value', 'quantity'}:
        raise ValueError('Reference needs exact positive value and compatible quantity descriptor')
    value = rational(raw['value'])
    if value <= 0:
        raise ValueError('Log reference must be strictly positive')
    descriptor = require_log_reference(quantity, raw['quantity'])
    return {'value': canonical(value), 'quantity': descriptor}


def _signature(value, quantity, reference, foundation):
    hd = foundation.hd_module.HDSignature.from_rational(value)
    if value == 0:
        logarithm, log_status = None, 'ZERO_HAS_NO_FINITE_LOG'
    elif quantity['units'] and reference is None:
        logarithm, log_status = None, 'REFERENCE_REQUIRED'
    else:
        divisor = 1 if reference is None else rational(reference['value'])
        logarithm = foundation.hd_module.FormalLogElement.from_positive_rational(abs(value) / divisor).to_dict()
        log_status = 'DEFINED'
    return {'value': canonical(value), 'hd_signature': hd.to_dict(),
            'sign': 0 if value == 0 else 1 if value > 0 else -1,
            'variant': 'ZERO' if value == 0 else 'NONZERO',
            'log_magnitude': logarithm, 'log_status': log_status}


def _append(inputs, prior, foundation):
    if not isinstance(inputs, list):
        raise ValueError('Contribution nodes must be a complete ordered list')
    nodes = deepcopy(prior)
    lookup = {node['id']: node for node in nodes}
    normalized = []
    for raw in inputs:
        if not isinstance(raw, dict) or not {'id', 'op'} <= set(raw):
            raise ValueError('Every contribution needs an explicit id and native value operation')
        identifier, operation = raw['id'], raw['op']
        if type(identifier) is not str or not identifier or identifier in lookup:
            raise ValueError('Contribution IDs must be nonempty and new; repeated operands use repeated edges')
        if operation == 'VALUE':
            if set(raw) - {'id', 'op', 'value', 'quantity', 'reference', 'source'} or 'value' not in raw:
                raise ValueError('Unknown value contribution fields')
            value = rational(raw['value'])
            quantity = normalize_descriptor(raw.get('quantity'))
            _value_convention(value, quantity)
            reference = _reference(raw.get('reference'), quantity)
            item = {'id': identifier, 'op': operation, 'value': canonical(value),
                    'quantity': quantity, 'reference': reference, 'source': raw.get('source')}
            node = {'id': identifier, 'op': operation, 'operands': [], 'quantity': quantity,
                    'reference': reference, 'source': raw.get('source'), 'status': 'DEFINED',
                    **_signature(value, quantity, reference, foundation)}
        else:
            if operation not in ('ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE') or set(raw) != {'id', 'op', 'left', 'right'}:
                raise ValueError('Binary value operation needs known operation and two explicit prior node IDs')
            if any(type(raw[key]) is not str or raw[key] not in lookup for key in ('left', 'right')):
                raise ValueError('Every operand must refer to an earlier retained contribution')
            left, right = lookup[raw['left']], lookup[raw['right']]
            item = dict(raw)
            quantity = add_descriptor(left['quantity'], right['quantity']) if operation in ('ADD', 'SUBTRACT') else product_descriptor(
                left['quantity'], right['quantity'], division=operation == 'DIVIDE')
            quantity['sign_convention'] = _result_convention(operation, left['quantity'], right['quantity'])
            reference = None
            if operation in ('ADD', 'SUBTRACT'):
                references = left['reference'], right['reference']
                if ((references[0] is None) != (references[1] is None) or
                    references[0] is not None and (rational(references[0]['value']) != rational(references[1]['value']) or
                    not compatible_add(references[0]['quantity'], references[1]['quantity']))):
                    raise ValueError('Additive log quantities require a common explicit reference value')
                reference = None if references[0] is None else {'value': references[0]['value'], 'quantity': quantity}
            elif left['reference'] is not None or right['reference'] is not None:
                # Dimensionless values already use the exact implicit reference 1.
                # Preserve it when composing with an explicit reference, without
                # inventing a reference for an unreferenced dimensional operand.
                references = [rational(operand['reference']['value']) if operand['reference'] is not None
                              else rational(1) if not operand['quantity']['units'] else None
                              for operand in (left, right)]
                if all(value is not None for value in references):
                    a, b = references
                    reference = {'value': canonical(a / b if operation == 'DIVIDE' else a * b), 'quantity': quantity}
            node = {'id': identifier, 'op': operation, 'operands': [raw['left'], raw['right']],
                    'quantity': quantity, 'reference': reference, 'source': None}
            status = 'DEPENDENCY_UNDEFINED' if left['status'] != 'DEFINED' or right['status'] != 'DEFINED' else 'DEFINED'
            if status == 'DEFINED':
                a, b = rational(left['value']), rational(right['value'])
                if operation == 'DIVIDE' and b == 0:
                    status = 'DIVISION_BY_ZERO'
                else:
                    if operation == 'ADD':
                        value = a + b
                    elif operation == 'SUBTRACT':
                        value = a - b
                    else:
                        hda = foundation.hd_module.HDSignature.from_rational(a)
                        hdb = foundation.hd_module.HDSignature.from_rational(b)
                        value = (hda.divide(hdb) if operation == 'DIVIDE' else hda.multiply(hdb)).value
                    node.update(_signature(value, quantity, reference, foundation))
            node['status'] = status
            if status != 'DEFINED':
                node.update(value=None, hd_signature=None, sign=None, variant='UNDEFINED',
                            log_magnitude=None, log_status=status)
        node = canonical(node)
        normalized.append(canonical(item)); nodes.append(node); lookup[identifier] = node
    return normalized, nodes


def _seal(body):
    body = canonical(body)
    return {'body': body, 'sha256': digest(body)}


def _remember(body):
    if len(_VERIFIED) >= 32:
        _VERIFIED.pop(next(iter(_VERIFIED)))
    _VERIFIED[canonical_bytes(body)] = True


def _result(body, work):
    _remember(body)
    _STATS['operations'] += 1
    for key, count in work.items():
        _STATS[key] += count
    root = next((node for node in body['nodes'] if node['id'] == body['result_id']), None)
    if root is None:
        raise ValueError('Requested result ID is absent from the complete contribution graph')
    return {'schema': 'GEN2_SIGNED_LOG_RESULT_V1', 'complete': True, 'status': root['status'],
            'result': deepcopy(root), 'nodes': deepcopy(body['nodes']), 'checkpoint': _seal(body)}


def dispatch(operation, payload, foundation):
    """GEN2_SIGNED_LOG(nodes,result_id?) or RESUME(checkpoint,append_nodes,result_id?)."""
    if operation == 'GEN2_SIGNED_LOG':
        if not isinstance(payload, dict) or set(payload) - {'nodes', 'result_id'} or 'nodes' not in payload:
            raise ValueError('Signed arithmetic needs declared contribution nodes')
        inputs, nodes = _append(payload['nodes'], [], foundation)
        if not nodes:
            raise ValueError('A signed arithmetic graph requires at least one contribution')
        body = {'schema': SCHEMA, 'complete': True, 'implementation_binding': _binding(foundation),
                'inputs': inputs, 'nodes': nodes, 'result_id': payload.get('result_id', nodes[-1]['id'])}
        return _result(body, {'new_nodes_evaluated': len(nodes), 'existing_nodes_reused': 0,
                              'checkpoint_nodes_revalidated': 0})
    if operation != 'GEN2_SIGNED_LOG_RESUME':
        raise ValueError('Unknown signed arithmetic operation')
    if not isinstance(payload, dict) or set(payload) - {'checkpoint', 'append_nodes', 'result_id'} or 'checkpoint' not in payload:
        raise ValueError('Signed arithmetic resume requires its complete checkpoint')
    checkpoint = payload['checkpoint']
    if not isinstance(checkpoint, dict) or set(checkpoint) != {'body', 'sha256'}:
        raise ValueError('Malformed signed arithmetic checkpoint')
    body = deepcopy(checkpoint['body'])
    expected = {'schema', 'complete', 'implementation_binding', 'inputs', 'nodes', 'result_id'}
    if not isinstance(body, dict) or set(body) != expected or body['schema'] != SCHEMA or body['complete'] is not True or digest(body) != checkpoint['sha256'] or body['implementation_binding'] != _binding(foundation):
        raise ValueError('Signed arithmetic checkpoint is incomplete, altered or differently bound')
    validated = 0
    if canonical_bytes(body) not in _VERIFIED:
        inputs, nodes = _append(body['inputs'], [], foundation)
        if inputs != body['inputs'] or nodes != body['nodes']:
            raise ValueError('Contribution graph values, references or operation associations were altered')
        validated = len(nodes)
    prior = len(body['nodes'])
    inputs, nodes = _append(payload.get('append_nodes', []), body['nodes'], foundation)
    body['inputs'] += inputs; body['nodes'] = nodes
    body['result_id'] = payload.get('result_id', nodes[-1]['id'] if inputs else body['result_id'])
    return _result(body, {'new_nodes_evaluated': len(inputs), 'existing_nodes_reused': prior,
                          'checkpoint_nodes_revalidated': validated})
