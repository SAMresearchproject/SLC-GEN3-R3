"""Independent source-template checks and real installed-learning confirmation."""
import argparse
import collections
import copy
import itertools
import json
import subprocess
from functools import lru_cache

from .compiler import sha
from .construction import read, save
from .template_generator import DEFAULT, OP, Consumer, digest, readgz, recover
from SAM_PROJECT.session import DomainSession


def check(out):
    source = read(out/'INPUT.json')
    contract = read(out/'CONTRACT.json')
    state = readgz(out/'SEARCH.json.gz')
    templates = readgz(out/'TEMPLATES.json.gz')
    adjacency = collections.defaultdict(set)
    for e in source['edges']:
        adjacency[e['u']].add(e['v'])
        adjacency[e['v']].add(e['u'])

    @lru_cache(None)
    def role_completion(last, used, count):
        if not count:
            return True
        return any(role_completion(v, used | (1 << v), count-1) for v in adjacency[last] if not used & (1 << v))

    @lru_cache(None)
    def cube_completion(last, used):
        # Enumerate remaining site orders independently of the native recursive walk.
        remaining = [s for s in range(8) if not used & (1 << s)]
        return any(all((a ^ b).bit_count() == 1 for a, b in zip((last,)+order, order)) for order in itertools.permutations(remaining))

    labels_checked = 0
    for row in state['learning'].values():
        n = state['nodes'][row['witness']['template']]
        roles = [o['role'] for o in n['objects']]
        sites = [o['site'] for o in n['objects']]
        expected = cube_completion(sites[-1], sum(1 << s for s in sites)) and role_completion(roles[-1], sum(1 << r for r in roles), 8-len(roles))
        assert row['label'] == int(expected)
        labels_checked += 1
    interface_states = 0
    for a in range(4, 9):
        interface = read(out/f'interfaces/A{a}.json')
        expected = {v for v in itertools.permutations(range(8), a) if all((x ^ y).bit_count() == 1 for x, y in zip(v, v[1:]))}
        actual = {tuple(v) for v in interface['placements']}
        assert actual == expected and len(actual) == len(interface['placements'])
        interface_states += len(actual)
        algebra = read(out/f'algebra/A{a}.json')
        assert algebra['word']['rank'] == a-1 and algebra['closure']['rank'] == a
        assert algebra['closure']['invariant'] and algebra['recurrence']['closed']
        assert algebra['creation']['reference_eigenstate_verified']
    for t in templates:
        node = dict(t['ledger'])
        identity = node.pop('id')
        assert identity == digest(node) == t['id']
        parent = state['nodes'][node['parent']]
        assert node['objects'][:-1] == parent['objects'] and node['cycles'][:-1] == parent['cycles']
        assert t['inverse']['restored_parent_sha256'] == parent['id']
    with DomainSession(read(out/'SESSION_PATH.json')['path']) as session:
        session.consumer = Consumer(session.consumer, out, contract)
        parent = source['seeds'][0]
        payload = {'mode': 'PROPOSE', 'parents': [parent], 'edges': source['edges'], 'actions': source['actions'], 'source_binding': contract['source_binding']}
        proposals = session.execute(OP, payload, purpose='Recover one valid source proposal for targeted admission controls.')['proposals']
        base = {**payload, 'mode': 'EXTEND', 'proposals': [proposals[0]]}
        controls = {}
        for name in ['duplicate_role', 'duplicate_site', 'wrong_inventory', 'wrong_reciprocal', 'wrong_source_action', 'floating_address']:
            altered = copy.deepcopy(base)
            if name == 'duplicate_role':
                altered['proposals'][0]['role'] = parent['objects'][0]['role']
            elif name == 'duplicate_site':
                altered['proposals'][0]['site'] = parent['objects'][0]['site']
            elif name == 'wrong_inventory':
                altered['parents'][0]['N'] += 1
            elif name == 'wrong_reciprocal':
                altered['parents'][0]['cycles'][0]['reverse'] = altered['parents'][0]['cycles'][0]['forward']
            elif name == 'wrong_source_action':
                altered['actions'][0]['sigma_chi'] *= -1
            else:
                altered['proposals'][0]['role'] += 0.5
            try:
                session.execute(OP, altered, purpose='Check that the template constructor rejects '+name.replace('_', ' ')+'.')
            except (ValueError, subprocess.CalledProcessError) as error:
                controls[name] = {'rejected': True, 'reason': (getattr(error, 'stderr', '') or str(error))[:180]}
            else:
                raise AssertionError('Admission control accepted: '+name)
        model = state['model']
        held = {r['witness']['structural_group']: r for r in state['learning'].values() if r['split'] == 2}
        predictions = session.execute('GEN3_TREE_PREDICT', {'name': model['name'], 'source_binding': model['binding'],
                                                         'rows': [{'id': k, 'features': r['features']} for k, r in held.items()]},
                                      purpose='Apply the final acquired model to reserved whole structural families; no fitting or selection uses these labels.')
        correct = sum(int(p['positive']) == held[p['id']]['label'] for p in predictions['predictions'])
        confirmations = {'correct': correct, 'total': len(held), 'predictions': predictions}
        growth = session.execute('GEN3_READOUT', {'account': 'template_growth'}, purpose='Read exact retained source-template growth after restoring the generator checkpoint.')
        assert growth['point_count'] == 6 and growth['full_history_retained']
        before = session.execute('GEN3_STATUS', {}, purpose='Check counters before reconciling an interrupted application commit.')
        reused = session.execute('GEN3_TREE_FIT', {'name': model['name'], 'rows': list(state['learning'].values()), 'source_binding': model['binding']},
                                 purpose='Replay the exact final fit request after restart; recover its committed model without refitting.')
        assert reused['recovered_without_fit']
        request = read(out/'RECOVERY_REQUEST.json')
        retained = session.execute('GEN3_SOURCE_SPECTRAL_EXPORT', {'name': request['operator_names'][0], 'source_binding': contract['source_binding']},
                                   purpose='Recover an exact operator request for interrupted-commit reconciliation.')['record']
        reused_op = session.execute(retained['operation'], {'name': retained['name'], 'source_binding': retained['source_binding'],
                                                            'context': retained['context'], 'data': retained['input']},
                                    purpose='Replay the identical operator request without recalculation.')
        assert reused_op['recovered_without_computation']
        history = session.execute('GEN3_HISTORY_EXPORT', {'account': 'template_growth'}, purpose='Recover the final append event for an exact replay check.')
        session.execute('GEN3_LOG_APPEND', {'account': 'template_growth', 'points': history['points'][-1:], 'edges': history['edges'][-1:]},
                        purpose='Replay the final committed growth append without duplicating source events.')
        after = session.execute('GEN3_STATUS', {}, purpose='Confirm interrupted-commit recovery performed no new native computations or history appends.')
        assert before['execution_counters'] == after['execution_counters']
        save(out/'LEARNING_CONFIRMATION.json', confirmations)
        save(out/'GROWTH.json', growth)
    result = {'status': 'PASS', 'source_templates': len(templates), 'exact_parent_inverses_checked': len(templates),
              'completion_labels_independently_checked': labels_checked, 'complete_interface_embeddings_checked': interface_states,
              'source_operator_families': 5, 'admission_controls': controls, 'held_out_correct': correct, 'held_out_total': len(held),
              'guided_selection_changed_in_rounds': [r['A'] for r in state['rounds'] if r['selection_changed']],
              'interrupted_commit_reconciliation': 'Model, operator and history replay preserve native counters',
              'retained_library_sha256': sha(out/'TEMPLATES.json.gz')}
    save(out/'VALIDATION.json', result)
    recover(out)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=type(DEFAULT), default=DEFAULT)
    check(p.parse_args().output)
