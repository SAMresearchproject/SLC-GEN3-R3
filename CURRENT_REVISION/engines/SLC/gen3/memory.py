"""Execute acquired observation/question branches inside the native machine.

The installed seed manifest is part of the authenticated release. An encounter
requires an actual supplied report and evidence on every traversed branch.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from ..gen2.exact import canonical_bytes, digest

SEEDS = Path(__file__).resolve().parent / 'seeds'


def load(name):
    manifest = json.loads((SEEDS/'MANIFEST.json').read_text())
    filename = name + '.json'
    if filename not in manifest['files']:
        raise ValueError('Unknown installed acquired memory')
    data = (SEEDS/filename).read_bytes()
    if hashlib.sha256(data).hexdigest() != manifest['files'][filename]['sha256']:
        raise ValueError('Installed acquired memory differs from its bound manifest')
    return json.loads(data)


def node_result(name, key, node):
    return {'memory': name, 'node': key, **{k: deepcopy(node[k]) for k in
        ('candidate_count','choice','selected_label','maximizing_labels','members',
         'target','target_resolved','transcript') if k in node}}


def dispatch(machine, operation, payload):
    if operation == 'GEN3_MEMORY_NODE':
        if set(payload) - {'memory','node'} or 'memory' not in payload:
            raise ValueError('Memory lookup needs its name and optional node identity')
        package = load(payload['memory']); memory = package.get('memory', package)
        key = payload.get('node', memory.get('root'))
        if key is None or key not in memory.get('nodes', {}):
            raise ValueError('Supply an acquired node in this scoped memory')
        return node_result(payload['memory'], key, memory['nodes'][key])
    if operation == 'GEN3_MEMORY_START':
        if set(payload) - {'memory','node','encounter'} or not {'memory','encounter'} <= set(payload):
            raise ValueError('Start needs an encounter identity and acquired memory')
        name = payload['encounter']
        if not isinstance(name, str) or not name or ('encounter:'+name) in machine.observations:
            raise ValueError('Use a new nonempty encounter identity')
        row = dispatch(machine, 'GEN3_MEMORY_NODE', {k:v for k,v in payload.items() if k!='encounter'})
        machine.observations['encounter:'+name] = {'memory':payload['memory'],'node':row['node'],'actual_reports':[]}
        machine.dirty['observations'].add('encounter:'+name)
        return {'encounter':name, **row}
    if operation == 'GEN3_MEMORY_APPLY':
        if set(payload) != {'encounter','observation','evidence'} or not payload['evidence']:
            raise ValueError('Every applied branch needs the actual observation and explicit source evidence')
        key = 'encounter:'+payload['encounter']
        encounter = machine.observations[key]
        package = load(encounter['memory']); memory = package.get('memory', package)
        node = memory['nodes'][encounter['node']]
        matches = [edge for edge in node['branches'].values()
                   if canonical_bytes(edge['observation']) == canonical_bytes(payload['observation'])]
        if len(matches) != 1:
            return {'status':'OUTSIDE_ACQUIRED_BRANCH_SUPPORT','encounter':payload['encounter'],
                **node_result(encounter['memory'], encounter['node'], node),
                'actual_observation':deepcopy(payload['observation']),
                'next_operation':'GEN2_OBSERVATION_APPLY with the complete current source checkpoint and plan'}
        target = matches[0]['target']
        if target not in memory['nodes']:
            raise ValueError('Acquired branch has no retained destination node')
        encounter['actual_reports'].append({'from':encounter['node'],'to':target,
            'choice':deepcopy(node.get('choice')),'observation':deepcopy(payload['observation']),
            'evidence':deepcopy(payload['evidence'])})
        encounter['node'] = target
        machine.dirty['observations'].add(key)
        machine.stats['learned_observation_branches_executed'] += 1
        return {'status':'APPLIED_ACTUAL_REPORT','encounter':payload['encounter'],
                **node_result(encounter['memory'], target, memory['nodes'][target])}
    raise ValueError('Unknown acquired memory operation')
