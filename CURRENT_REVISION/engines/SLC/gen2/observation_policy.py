"""Exact two-step adaptive observation policies over complete linked histories.

Planning computes declared candidate consequences; APPLY always requires an
actual report (or explicit MISSING). STOP preserves the complete inverse fiber.
The reusable DAG keys full native histories, original targets, exact conditional
weights, source/code bindings and remaining roster/horizon. Equivalent reports
may reuse calculations; their labels, programs and decision branches remain.
"""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from .exact import canonical, digest, rational
from . import observation as obs

SCHEMA = 'GEN2_OBSERVATION_POLICY_CHECKPOINT_V1'
POLICY_SCHEMA = 'GEN2_OBSERVATION_POLICY_V1'
_NODES = {}
_TREE_BYTES = {}
_VERIFIED = {}
_STATS = {'node_hits': 0, 'node_misses': 0, 'policy_resume_hits': 0, 'target_determined_bounds': 0, 'sealed_tree_hits': 0, 'sealed_tree_misses': 0}


def reuse_stats(reset=False):
    result = dict(_STATS)
    if reset:
        for key in _STATS: _STATS[key] = 0
    return result


def resolve_contract(operation, payload):
    try:
        checkpoint = payload['checkpoint'] if operation == 'GEN2_OBSERVATION_POLICY_PLAN' else payload['policy_checkpoint']['body']['session_checkpoint']
        return checkpoint['body']['contract']
    except (TypeError, KeyError) as error:
        raise ValueError('Policy requires a complete source-bound inverse/session checkpoint') from error


def _log(value, cls):
    return cls.from_terms([(row['prime'], Fraction(row['coefficient']['numerator'], row['coefficient']['denominator'])) for row in value['coefficients']])


def _zero(cls):
    return {'target_information': cls.zero().to_dict(), 'transcript_entropy': cls.zero().to_dict(),
            'transcript_alphabet': 1, 'expected_reads': 0, 'expected_writes': 0, 'expected_scalar_payload': 0}


def _context(block, body, choices, horizon, log_class):
    # Probe report bookkeeping is retained by the session/tree. Future native
    # consequences depend on complete original/current native histories below,
    # not on the spelling of a prior report or its sealed plan envelope.
    members = [{k: v for k, v in m.items() if k != 'probe_history'} for m in body['members']]
    return canonical({'contract': block.contract.to_dict(), 'implementation_binding': body['implementation_binding'],
                      'question': body['question'], 'members': members, 'weights': body['weights'],
                      'choices': choices, 'remaining_horizon': horizon})


def _minimum(options, cls):
    """All target-information ties survive; detail/cost then stable roster."""
    best = None
    ties = []
    for option in options:
        value = _log(option['metrics']['target_information'], cls)
        comparison = 1 if best is None else value.compare(best)
        if comparison > 0: best, ties = value, [option['label']]
        elif comparison == 0: ties.append(option['label'])
    finalists = [option for option in options if option['label'] in ties]
    smallest = _log(finalists[0]['metrics']['transcript_entropy'], cls)
    for option in finalists[1:]:
        value = _log(option['metrics']['transcript_entropy'], cls)
        if value.compare(smallest) < 0: smallest = value
    finalists = [option for option in finalists if _log(option['metrics']['transcript_entropy'], cls).compare(smallest) == 0]
    for field in ('transcript_alphabet', 'expected_reads', 'expected_writes', 'expected_scalar_payload'):
        smallest = min(rational(option['metrics'][field]) for option in finalists)
        finalists = [option for option in finalists if rational(option['metrics'][field]) == smallest]
    return ties, [option['label'] for option in finalists], finalists[0]


def _target_determined_options(block, body, choices, cls):
    """Exact dominance bound without enumerating irrelevant second reports.

    For a single original target class every complete report has I(T;R)=0.
    H(R)>=0 and its alphabet>=1; every non-STOP action consumes one read.
    Thus STOP wins even when a future report is constant. Available labels stay
    information-tied and manually applying any of them remains supported.
    """
    declared = body['question'].get('available_readouts', ())
    reports = body['question'].get('available_reports', obs.reporting.source_reports(block, declared))
    if choices is None:
        choices = obs.reporting.automatic_choices(obs.motion_observation.automatic_choices(block, declared), reports)
    choices = [obs._choice(choice, block) for choice in choices]
    cache = {'__implementation_binding__': body['implementation_binding']}
    options = []
    for choice in choices:
        allowed = ('readout' not in choice or choice['readout'] in declared) and obs.reporting.allowed(choice, reports)
        if 'report' in choice and not allowed:
            raise ValueError('Observation report resolution is not declared by this source or its whitelist')
        if 'readout' in choice:
            predictions, unavailable = obs._predictions(block, body['members'], choice, cls, declared, cache)
        else:
            unavailable = [m['record_id'] for m in body['members'] if choice['event'] is not None and
                           not any(row[1] == choice['event'] for row in block.outgoing.get(tuple(m['states'][-1]), ()))]
        available = allowed and not unavailable
        row = {'label': choice['label'], 'choice': choice, 'available': available,
               'unavailable_record_ids': unavailable, 'branches': [], 'metrics': None}
        if available:
            row.update(metrics={'target_information': cls.zero().to_dict()},
                       immediate_information=cls.zero().to_dict(),
                       dominance_certificate={'kind': 'ORIGINAL_TARGET_ALREADY_DETERMINED',
                            'target_class_count': 1, 'target_information': cls.zero().to_dict(),
                            'transcript_entropy_lower_bound': cls.zero().to_dict(),
                            'transcript_alphabet_lower_bound': 1, 'expected_reads_lower_bound': 1,
                            'stop_expected_reads': 0, 'branch_enumeration': 'UNNEEDED_FOR_EXACT_DOMINANCE'})
        options.append(row)
    return options


def _solve(block, body, choices, horizon, cls):
    context = _context(block, body, choices, horizon, cls)
    identifier = digest(context)
    if identifier in _NODES:
        _STATS['node_hits'] += 1
        return identifier
    _STATS['node_misses'] += 1
    options = [{'label': 'STOP', 'choice': None, 'available': True, 'metrics': _zero(cls), 'branches': []}]
    evaluated = []
    determined = bool(body['members']) and all(m['target_status'] == 'DEFINED' for m in body['members']) and len({digest(m['target']) for m in body['members']}) == 1
    if horizon and determined:
        _STATS['target_determined_bounds'] += 1
        options.extend(_target_determined_options(block, body, choices, cls))
    elif horizon and body['members'] and all(m['target_status'] == 'DEFINED' for m in body['members']):
        roster, weights, evaluated, scores, details, automatic, refined = obs._evaluate(block, body, choices, None, cls)
        for row in evaluated:
            choice = row['choice']
            if choice['label'] == 'STOP': raise ValueError('STOP is the reserved policy terminal action')
            option = {'label': choice['label'], 'choice': choice, 'available': row['available'],
                      'unavailable_record_ids': row['unavailable_record_ids'], 'metrics': None, 'branches': []}
            if row['score'] is None:
                options.append(option)
                continue
            score = scores[choice['label']]
            information = score.mutual_information
            entropy = details[choice['label']]['report_entropy']
            alphabet = 0
            reads, writes = Fraction(1), Fraction(choice['event'] is not None)
            scalars = Fraction(row['returned_scalar_components'])
            for group in score.observation_partition:
                members = obs._condition_predictions(body['members'], choice, canonical(group['observation']), row['predictions'])
                child_body = dict(body, members=members, weights={m['record_id']: weights[m['record_id']] for m in members})
                child_id = _solve(block, child_body, choices, horizon - 1, cls)
                child = _NODES[child_id]
                mass = group['probability']
                metrics = child['selected_metrics']
                information = information + _log(metrics['target_information'], cls).scale(mass)
                entropy = entropy + _log(metrics['transcript_entropy'], cls).scale(mass)
                alphabet += metrics['transcript_alphabet']
                reads += mass * rational(metrics['expected_reads'])
                writes += mass * rational(metrics['expected_writes'])
                scalars += mass * rational(metrics['expected_scalar_payload'])
                option['branches'].append({'observation': canonical(group['observation']), 'probability': str(mass),
                                           'members': list(group['members']), 'node': child_id})
            option['immediate_information'] = score.mutual_information.to_dict()
            option['immediate_report_entropy'] = details[choice['label']]['report_entropy'].to_dict()
            option['metrics'] = canonical({'target_information': information.to_dict(), 'transcript_entropy': entropy.to_dict(),
                                           'transcript_alphabet': alphabet, 'expected_reads': reads, 'expected_writes': writes,
                                           'expected_scalar_payload': scalars})
            options.append(option)
    available = [option for option in options if option['available'] and option['metrics'] is not None]
    if horizon and determined:
        ties, finalists, selected = [option['label'] for option in available], ['STOP'], options[0]
    else:
        ties, finalists, selected = _minimum(available, cls)
    node = canonical({'node_id': identifier, 'context': context, 'candidate_count': len(body['members']),
                      'options': options, 'maximizing_labels': ties, 'minimum_detail_cost_labels': finalists,
                      'selected_label': selected['label'], 'selected_metrics': selected['metrics']})
    _NODES[identifier] = node
    return identifier


def _seal_json(body):
    # All fields are constructed from already canonical validated session,
    # choice, exact metric and report records. Serialize once and return an
    # isolated decoded copy; bytes match exact.canonical_bytes identically.
    encoded = json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()
    return {'body': json.loads(encoded), 'sha256': sha256(encoded).hexdigest()}


def _tree(block, body, choices, horizon, cls):
    root = digest(_context(block, body, choices, horizon, cls))
    if root in _TREE_BYTES:
        _STATS['sealed_tree_hits'] += 1
        encoded = _TREE_BYTES[root]
        return {'body': json.loads(encoded), 'sha256': sha256(encoded).hexdigest()}
    _STATS['sealed_tree_misses'] += 1
    # Eviction occurs between complete tree builds, never while child links
    # are being assembled. Cached trees own immutable exact serialized bytes.
    if len(_NODES) > 8192: _NODES.clear()
    root = _solve(block, body, choices, horizon, cls)
    nodes = {}
    def include(identifier):
        if identifier in nodes: return
        node = _NODES[identifier]
        nodes[identifier] = node
        for option in node['options']:
            for branch in option['branches']: include(branch['node'])
    include(root)
    value = {'schema': POLICY_SCHEMA, 'root_node': root, 'nodes': nodes,
             'selection_rule': 'TARGET_INFORMATION_TRANSCRIPT_ENTROPY_ALPHABET_EXPECTED_READS_WRITES_SCALARS_ROSTER'}
    encoded = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()
    if len(_TREE_BYTES) >= 8: _TREE_BYTES.pop(next(iter(_TREE_BYTES)))
    _TREE_BYTES[root] = encoded
    return {'body': json.loads(encoded), 'sha256': sha256(encoded).hexdigest()}


def _checkpoint(block, session_checkpoint, choices, horizon, cls, *, weights=None, previous=None, step=None):
    body = obs._session(block, session_checkpoint, cls)
    weights = obs._weights(body['weights'] if weights is None else weights, body['members'])
    policy = _tree(block, dict(body, weights=weights), choices, horizon, cls)
    return _seal_json({'schema': SCHEMA, 'session_checkpoint': session_checkpoint,
                      'choices': choices, 'remaining_horizon': horizon, 'policy': policy, 'weights': weights,
                      'previous': previous, 'step': step})


def _result(checkpoint):
    body = checkpoint['body']
    policy = body['policy']['body']
    node = policy['nodes'][policy['root_node']]
    session = obs._result(body['session_checkpoint']['body'])
    kinds = {digest(m['target']) for m in session['members'] if m['target_status'] == 'DEFINED'}
    return {'schema': POLICY_SCHEMA, 'complete': True,
                      'status': 'STOP' if node['selected_label'] == 'STOP' else 'READY',
                      'remaining_horizon': body['remaining_horizon'], 'candidate_count': session['candidate_count'],
                      'target_resolved': bool(session['members']) and len(kinds) == 1 and all(m['target_status'] == 'DEFINED' for m in session['members']),
                      'target_class_count': len(kinds), 'weights': body['weights'], 'selected_label': node['selected_label'],
                      'maximizing_labels': node['maximizing_labels'], 'selected_metrics': node['selected_metrics'],
                      'session': session, 'policy_checkpoint': checkpoint}


def _validate(block, checkpoint, cls):
    body = obs._checked_seal(checkpoint, SCHEMA)
    obs._fields(body, {'schema', 'session_checkpoint', 'choices', 'remaining_horizon', 'policy', 'weights', 'previous', 'step'},
                {'schema', 'session_checkpoint', 'choices', 'remaining_horizon', 'policy', 'weights', 'previous', 'step'})
    session = obs._session(block, body['session_checkpoint'], cls)
    if obs._weights(body['weights'], session['members']) != body['weights']:
        raise ValueError('Policy measure must be canonical complete positive weights')
    if digest(body) in _VERIFIED:
        _STATS['policy_resume_hits'] += 1
        return body
    if type(body['remaining_horizon']) is not int or body['remaining_horizon'] not in range(3):
        raise ValueError('R4 policy horizon is exactly zero, one or two observations')
    if (body['previous'] is None) != (body['step'] is None):
        raise ValueError('Policy continuation needs its complete previous policy and actual report')
    if body['previous'] is not None:
        previous = _validate(block, body['previous'], cls)
        expected = _apply(block, body['previous'], body['step'], cls, verified=True)
        if expected != checkpoint: raise ValueError('Policy continuation or original session was altered')
    expected_policy = _tree(block, dict(body['session_checkpoint']['body'], weights=body['weights']), body['choices'], body['remaining_horizon'], cls)
    if expected_policy != body['policy']: raise ValueError('Policy alternatives, chain rule, costs or selected tree were altered')
    _VERIFIED[digest(body)] = True
    return body


def _apply(block, checkpoint, request, cls, verified=False):
    body = checkpoint['body'] if verified else _validate(block, checkpoint, cls)
    obs._fields(request, {'choice_label', 'observation', 'report_status'}, ())
    tree = body['policy']['body']
    node = tree['nodes'][tree['root_node']]
    label = request.get('choice_label', node['selected_label'])
    if label == 'STOP':
        if set(request) - {'choice_label'}: raise ValueError('STOP receives no report and performs no native event')
        return _checkpoint(block, body['session_checkpoint'], body['choices'], 0, cls,
                           weights=body['weights'], previous=checkpoint, step={'choice_label': 'STOP'})
    if not body['remaining_horizon']: raise ValueError('Policy has no remaining observation budget')
    rows = [row for row in node['options'] if row['label'] == label and row['available'] and row['metrics'] is not None]
    if not rows: raise ValueError('Policy choice is absent or unavailable for the complete conditional relation')
    session = body['session_checkpoint']
    plan = obs.dispatch('GEN2_OBSERVATION_PLAN', {'checkpoint': session, 'weights': body['weights'], **({} if body['choices'] is None else {'choices': body['choices']})}, block, cls)
    payload = {'checkpoint': session, 'plan': plan['plan'], 'choice_label': label}
    for field in ('observation', 'report_status'):
        if field in request: payload[field] = request[field]
    result = obs.dispatch('GEN2_OBSERVATION_APPLY', payload, block, cls)
    step = {'choice_label': label}
    step.update({k: v for k, v in request.items() if k != 'choice_label'})
    return _checkpoint(block, result['checkpoint'], body['choices'], body['remaining_horizon'] - 1, cls,
                       previous=checkpoint, step=canonical(step))


def dispatch(operation, payload, block, formal_log_cls):
    if operation == 'GEN2_OBSERVATION_POLICY_PLAN':
        obs._fields(payload, {'checkpoint', 'horizon', 'choices', 'weights'}, ('checkpoint',))
        horizon = payload.get('horizon', 2)
        if type(horizon) is not int or horizon not in range(3): raise ValueError('R4 policy horizon must be zero, one or two')
        body = obs._session(block, payload['checkpoint'], formal_log_cls)
        weights = obs._weights(payload.get('weights', body['weights']), body['members'])
        choices = payload.get('choices')
        if choices is not None:
            if not isinstance(choices, (list, tuple)) or not choices: raise ValueError('Policy roster must be nonempty')
            choices = [obs._choice(c, block) for c in choices]
            if len({c['label'] for c in choices}) != len(choices) or any(c['label'] == 'STOP' for c in choices):
                raise ValueError('Policy labels must be distinct and reserve STOP')
        return _result(_checkpoint(block, payload['checkpoint'], choices, horizon, formal_log_cls, weights=weights))
    if operation == 'GEN2_OBSERVATION_POLICY_RESUME':
        obs._fields(payload, {'policy_checkpoint'}, ('policy_checkpoint',))
        _validate(block, payload['policy_checkpoint'], formal_log_cls)
        return _result(payload['policy_checkpoint'])
    if operation == 'GEN2_OBSERVATION_POLICY_APPLY':
        obs._fields(payload, {'policy_checkpoint', 'choice_label', 'observation', 'report_status'}, ('policy_checkpoint',))
        request = {k: v for k, v in payload.items() if k != 'policy_checkpoint'}
        return _result(_apply(block, payload['policy_checkpoint'], request, formal_log_cls))
    raise ValueError('Unknown adaptive observation policy operation')
