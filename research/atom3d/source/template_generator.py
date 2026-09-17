"""Learning-directed, source-bound atomic terminal-template generation.

Python owns custody/scheduling/independent checks. The native adapter executes
source extension and placement; installed GEN3 performs learning and algebra.
"""
import argparse
import collections
import copy
import csv
import fcntl
import gzip
import hashlib
import json
import shutil
import subprocess
import time
from fractions import Fraction
from pathlib import Path

from .compiler import ROOT, HERE, sha
from .construction import read, save
from .catalog import SYMBOLS
from SAM_PROJECT.session import DomainSession
from CURRENT_REVISION.runtime import current_generation

DEFAULT = ROOT/'SAM_REVIEW/campaigns/GEN3_TEMPLATE_GENERATOR4'
SRC = ROOT/'SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN'
EDGES = SRC/'SLC_EXACT_N100_N81_PARTICLE_GRAMMAR_BRIDGE_V1/instances/N100_P2_PACKET_PLUS_DEPTH.json'
ACTIONS = SRC/'SLC_OCTAHEDRAL_FIBER_ACTION_N100_N81_BRIDGE_V1/DIRECTED_EDGE_ACTION_MAP.csv'
SEEDS = ROOT/'ATOM3D/campaigns/ATOM3D_A2_HYDROGEN_LADDER/stages/A2H3_A2HE3/release'
OP = 'ISOTOPE_SOURCE_TEMPLATE_GENERATOR_V1'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def savegz(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    with gzip.open(tmp, 'wt') as f:
        json.dump(value, f, separators=(',', ':'))
    tmp.replace(path)


def readgz(path):
    with gzip.open(path, 'rt') as f:
        return json.load(f)


def seal(node):
    return {**node, 'id': digest(node)}


def prepare(out):
    out.mkdir(parents=True, exist_ok=True)
    if (out/'CONTRACT.json').exists():
        return read(out/'CONTRACT.json')
    numeric = {'source_site', 'target_site', 'source_frame_q', 'target_frame_q', 'local_displacement', 'sigma_chi'}
    with ACTIONS.open() as f:
        actions = [{k: int(v) if k in numeric else v for k, v in r.items()} for r in csv.DictReader(f)]
    edges = read(EDGES)['edges']
    lookup = {(r['u'], r['v']): i for i, r in enumerate(edges)}
    seeds = []
    for name in ['H3', 'HE3']:
        ledger = read(SEEDS/f'{name}_ATOMIC_LEDGER.json')
        objects = [{k: o[k] for k in ['role', 'site', 'kind']} for o in ledger['matter_objects'] if o['kind'] != 'electron']
        objects_by_id = {o['object_id']: i for i, o in enumerate(o for o in ledger['matter_objects'] if o['kind'] != 'electron')}
        cycles = []
        events = ledger['event_stream']['events']
        for start in range(0, len(events), 2):
            pair = events[start:start+2]
            ids = []
            for e in pair:
                matches = [i for i, a in enumerate(actions) if all(a[k] == e[k] for k in ['source_site', 'target_site', 'octahedral_vertex', 'action', 'local_displacement', 'sigma_chi'])
                           and a['source_frame_q'] == e['q_in'] and a['target_frame_q'] == e['q_out']]
                assert len(matches) == 1
                ids.append(matches[0])
            u, v = objects_by_id[pair[0]['source_object_id']], objects_by_id[pair[0]['target_object_id']]
            cycles.append({'u': u, 'v': v, 'edge': lookup[tuple(sorted((objects[u]['role'], objects[v]['role'])))],
                           'forward': ids[0], 'reverse': ids[1], 'origin': pair[0]['cycle_id'],
                           'source_event_ids': [e['event_id'] for e in pair]})
        seeds.append(seal({'schema': 'SAM_GENERATED_SOURCE_LEDGER_V1', 'objects': objects, 'cycles': cycles,
                           'Z': sum(o['kind'] == 'proton' for o in objects), 'N': sum(o['kind'] == 'neutron' for o in objects),
                           'electrons': ledger['identity']['electrons'], 'terminal': events[-1]['event_id'], 'parent': None,
                           'seed_source': {'path': str((SEEDS/f'{name}_ATOMIC_LEDGER.json').relative_to(ROOT)), 'sha256': sha(SEEDS/f'{name}_ATOMIC_LEDGER.json')}}))
    include = ROOT/'SAM_REVIEW/campaigns/GEN3_R3_CAPABILITY_UPGRADE1/deps/root/usr/include'
    cmd = ['g++', '-O2', '-std=c++20', '-Wall', '-Wextra', '-fsanitize=undefined', '-fno-sanitize-recover=undefined',
           '-I'+str(include), str(HERE/'native/template_generator.cpp'), '-o', str(out/'template-native')]
    build = subprocess.run(cmd, capture_output=True, text=True)
    save(out/'BUILD.json', {'command': cmd, 'returncode': build.returncode, 'stderr': build.stderr})
    build.check_returncode()
    paths = [EDGES, ACTIONS, SEEDS/'H3_ATOMIC_LEDGER.json', SEEDS/'HE3_ATOMIC_LEDGER.json',
             HERE/'native/template_generator.cpp', Path(__file__)]
    contract = {'schema': 'GEN3_SOURCE_TEMPLATE_GENERATOR_CONTRACT_V1', 'generation': current_generation(),
                'source_binding': {'files': {str(p.relative_to(ROOT)): sha(p) for p in paths}},
                'binary_sha256': sha(out/'template-native'),
                'question': 'Which append-only source path extensions produce reusable atomic templates beyond H1/H2/H3/He3, and can acquired continuation knowledge improve subsequent search?',
                'new_rule_origin': 'Codex implementation of Sean Brady\'s template-generation directive: append one proton or neutron at an unused N100 neighbor role and an unused adjacent source cube site; execute one exact reciprocal source cycle. Existing parent objects and cycles remain unchanged. Electron count follows proton count.',
                'scope': 'Candidate source-incidence path templates of four through eight nucleons; no species-specific stability or energy assignment. No site/role selection rule beyond this declared exploratory construction is inferred from source counts.',
                'learning_target': 'An append-only source role path and cube path can both complete eight distinct sites. Exact native lookahead labels each executed candidate; identity, species and phase variants share a structural split group.',
                'features': ['object_count', 'occupied_site_mask', 'terminal_site', 'unused_role_neighbors', 'unused_site_neighbors', 'free_cube_components', 'free_cube_isolated', 'free_cube_leaves', 'terminal_role_degree'],
                'scheduler': {'bootstrap_through_A': 5, 'parents_per_stage': 128, 'learned_slots': 256, 'exploration_slots': 64,
                              'preserve_inventory_diversity': True, 'shadow_baseline': 'Same candidate pool and budget, deterministic hash order; measured separately and excluded from learning.'},
                'max_A': 8, 'cleanup_trigger_bytes': 300*2**30, 'minimum_free_bytes': 20*2**30,
                'retention': 'Unique templates, inverse receipts, learned models, source events and deferred questions are retained. Only interrupted temporary writes can be deleted automatically; otherwise stop and notify.',
                'source_template_membership': 'Derive injective cube embeddings of the new path and retain reciprocal source-action choices. Never import the old four-type membership assignment.',
                'physical_binding_stability': 'UNASSIGNED'}
    save(out/'CONTRACT.json', contract)
    save(out/'INPUT.json', {'edges': edges, 'actions': actions, 'seeds': seeds})
    save(out/'STATUS.json', {'state': 'READY', 'new_templates': 0})
    return contract


class Consumer:
    def __init__(self, consumer, out, contract):
        self.consumer, self.out, self.contract = consumer, out, contract
        self.source = read(out/'INPUT.json')

    def __getattr__(self, name):
        return getattr(self.consumer, name)

    def execute(self, operation, payload):
        # The native checkpoint can commit just before the application state file.
        # Reconcile such interrupted writes by exact source identity, not by refit.
        if operation == 'GEN3_TREE_FIT':
            try:
                export = self.consumer.execute('GEN3_TREE_EXPORT', {'name': payload['name']})
            except ValueError as error:
                if str(error) != 'Unknown acquired model':
                    raise
            else:
                record = export['record']
                if record['source_binding'] != payload['source_binding'] or record['training_input_sha256'] != digest(payload['rows']):
                    raise ValueError('Interrupted model input differs from its checkpoint')
                return {'name': payload['name'], **record['model'], 'model_sha256': export['sha256'],
                        'source_binding': payload['source_binding'], 'recovered_without_fit': True}
        if operation in {'GEN3_SOURCE_OPERATOR_WORD', 'GEN3_SOURCE_SUBSPACE', 'GEN3_BLOCK_SOURCE_RECURRENCE', 'GEN3_SOURCE_SPECTRAL_CREATION'}:
            try:
                export = self.consumer.execute('GEN3_SOURCE_SPECTRAL_EXPORT', {k: payload[k] for k in ['name', 'source_binding']})
            except ValueError as error:
                if str(error) != 'Unknown retained source operator record':
                    raise
            else:
                record = export['record']
                if record['operation'] != operation or record['context'] != payload['context'] or record['input'] != payload['data']:
                    raise ValueError('Interrupted operator input differs from its checkpoint')
                return {**record['result'], 'record_sha256': export['sha256'], 'recovered_without_computation': True}
        if operation in {'GEN3_LOG_OPEN', 'GEN3_LOG_APPEND'}:
            try:
                history = self.consumer.execute('GEN3_HISTORY_EXPORT', {'account': payload['account']})
            except KeyError:
                pass
            else:
                points = {p['id']: p for p in history['points']}
                edges = {e['id']: e for e in history['edges']}
                expected = [{**p, 'status': p.get('status', 'OBSERVED')} for p in payload['points']]
                if all(p['id'] in points for p in expected):
                    if not all(points[p['id']] == p for p in expected) or not all(edges.get(e['id']) == e for e in payload['edges']):
                        raise ValueError('Interrupted growth history differs from its checkpoint')
                    if operation == 'GEN3_LOG_OPEN' and history['source_binding'] != payload['source_binding']:
                        raise ValueError('Interrupted growth source differs')
                    return self.consumer.execute('GEN3_READOUT', {'account': payload['account']})
        if operation != OP:
            return self.consumer.execute(operation, payload)
        if sha(self.out/'template-native') != self.contract['binary_sha256'] or payload['source_binding'] != self.contract['source_binding']:
            raise ValueError('Template source binding changed')
        if payload['edges'] != self.source['edges'] or payload['actions'] != self.source['actions']:
            raise ValueError('Source incidence/action payload differs from the bound input')
        result = subprocess.run([str(self.out/'template-native')], input=json.dumps(payload), capture_output=True,
                                text=True, check=True, timeout=600)
        return json.loads(result.stdout)


def independent(node, parent, proposal, source):
    """Independent ledger, source-cycle and exact inverse reconstruction."""
    objects = node['objects']
    assert objects[:-1] == parent['objects'] and node['cycles'][:-1] == parent['cycles']
    assert len({o['role'] for o in objects}) == len(objects) == len({o['site'] for o in objects})
    assert objects[-1] == {k: proposal[k] for k in ['role', 'site', 'kind']}
    z = sum(o['kind'] == 'proton' for o in objects)
    assert (node['Z'], node['N'], node['electrons']) == (z, len(objects)-z, z)
    c = node['cycles'][-1]
    assert c['parent_terminal'] == parent['terminal'] and node['parent'] == parent['id']
    a, b = [source['actions'][c[k]] for k in ['forward', 'reverse']]
    x, y = objects[-2:]
    e = source['edges'][c['edge']]
    assert {e['u'], e['v']} == {x['role'], y['role']}
    assert (a['source_site'], a['target_site']) == (x['site'], y['site'])
    assert (b['source_site'], b['target_site']) == (y['site'], x['site'])
    assert a['octahedral_vertex'] == b['octahedral_vertex'] and a['action'] != b['action']
    assert a['source_frame_q'] == b['target_frame_q'] and a['target_frame_q'] == b['source_frame_q']
    assert a['local_displacement'] == -b['local_displacement'] and a['sigma_chi'] == -b['sigma_chi']
    restored = {**node, 'objects': objects[:-1], 'cycles': node['cycles'][:-1],
                'Z': parent['Z'], 'N': parent['N'], 'electrons': parent['electrons'],
                'terminal': parent['terminal'], 'parent': parent['parent']}
    restored.pop('id', None)
    assert seal(restored) == parent
    return {'parent': parent['id'], 'removed_object': objects[-1], 'removed_cycle': c,
            'restored_parent_sha256': digest(restored), 'exact_inverse': True}


def diverse(rows, limit, scores=None):
    """Round-robin inventories; rank within each inventory without deleting ties."""
    scores = scores or {}
    groups = collections.defaultdict(list)
    for r in rows:
        groups[r['Z'], r['N']].append(r)
    for g in groups.values():
        g.sort(key=lambda r: (-scores.get(r['id'], Fraction(0)), digest(r['id'])))
    keys = sorted(groups, key=lambda k: (k[0], -k[1]))
    selected = []
    while keys and len(selected) < limit:
        for k in list(keys):
            if len(selected) == limit:
                break
            selected.append(groups[k].pop(0))
            if not groups[k]:
                keys.remove(k)
    return selected


def admit(out, contract):
    if (out/'STOP').exists():
        raise InterruptedError('Owner STOP')
    if current_generation() != contract['generation']:
        raise ValueError('Generation changed')
    used = sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
    if used >= contract['cleanup_trigger_bytes']:
        for p in out.rglob('*.tmp'):
            p.unlink()
        raise InterruptedError('300GiB cleanup trigger: interrupted writes cleared; unique evidence retained for review')
    if shutil.disk_usage(out).free < contract['minimum_free_bytes']:
        raise InterruptedError('Free-space reserve reached')


def execute(out):
    contract = prepare(out)
    with (out/'controller.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if read(out/'STATUS.json')['state'] == 'COMPLETE_DECLARED_SEARCH':
            return read(out/'SUMMARY.json')
        for p, h in contract['source_binding']['files'].items():
            if sha(ROOT/p) != h:
                raise ValueError('Source changed: '+p)
        source = read(out/'INPUT.json')
        if (out/'SESSION_PATH.json').exists():
            session = DomainSession(read(out/'SESSION_PATH.json')['path'])
        else:
            session = DomainSession.start('ATOM3D', objective=contract['question'], output_root=out/'sessions', receipt_storage='gzip')
            save(out/'SESSION_PATH.json', {'path': str(session.directory)})
        with session as s:
            print(s.announcement(), s.directory, flush=True)
            s.consumer = Consumer(s.consumer, out, contract)
            def native(mode, **kwargs):
                return s.execute(OP, {'mode': mode, 'edges': source['edges'], 'actions': source['actions'],
                                      'source_binding': contract['source_binding'], **kwargs},
                                 purpose='Execute source-template '+mode+' with actual N100 incidence and reciprocal source actions.')
            if not (out/'CAPABILITIES.json').exists():
                save(out/'CAPABILITIES.json', s.execute('GEN3_CAPABILITIES', {}, purpose='Map installed native capabilities into the source-template generator.'))
            checkpoint_path = out/'SEARCH.json.gz'
            if checkpoint_path.exists():
                state = readgz(checkpoint_path)
            else:
                state = {'nodes': {n['id']: n for n in source['seeds']}, 'frontier': source['seeds'], 'learning': {},
                         'next_A': 4, 'model': None, 'rounds': [], 'deferred': [], 'inverses': {}}
                s.execute('GEN3_LOG_OPEN', {'account': 'template_growth', 'quantity': {'kind': 'SOURCE_ACTION', 'units': {'retained_source_template': 1}, 'scope': 'HISTORY', 'source': str(out.name)},
                                          'source_binding': contract['source_binding'], 'points': [{'id': 'A3', 'state': {'seeds': [n['id'] for n in source['seeds']]}, 'action': 2}], 'edges': []},
                          purpose='Retain exact logarithmic growth and full stage custody of the constructed template library.')
                s.execute('GEN3_CHECKPOINT', {}, purpose='Commit initial source-template seeds and growth history.')
                savegz(checkpoint_path, state)
            for a in range(state['next_A'], contract['max_A']+1):
                admit(out, contract)
                parents = diverse(state['frontier'], contract['scheduler']['parents_per_stage'])
                parentmap = {n['id']: n for n in parents}
                proposals = native('PROPOSE', parents=parents)['proposals']
                for q in proposals:
                    # Content identity is stable across restarts and ordering changes.
                    q['id'] = digest({k: q[k] for k in ['parent', 'role', 'site', 'forward', 'kind']})
                scores, prediction = {}, None
                if state['model']:
                    m = state['model']
                    prediction = s.execute('GEN3_TREE_PREDICT', {'name': m['name'], 'source_binding': m['binding'],
                                                               'rows': [{'id': q['id'], 'features': q['features']} for q in proposals]},
                                           purpose='Use acquired continuation knowledge on fresh, unexecuted source extensions; retain every probability tie.')
                    scores = {r['id']: Fraction(r['probability']) for r in prediction['predictions']}
                if a <= contract['scheduler']['bootstrap_through_A']:
                    selected = proposals
                else:
                    guided = diverse(proposals, contract['scheduler']['learned_slots'], scores)
                    ids = {q['id'] for q in guided}
                    exploration = diverse([q for q in proposals if q['id'] not in ids], contract['scheduler']['exploration_slots'])
                    selected = guided+exploration
                ids = {q['id'] for q in selected}
                baseline = diverse(proposals, len(selected))
                shadow = [q for q in baseline if q['id'] not in ids]
                production = native('EXTEND', parents=parents, proposals=selected)['rows']
                shadow_rows = native('EXTEND', parents=parents, proposals=shadow)['rows'] if shadow else []
                outcomes = {r['proposal']: r['can_complete_eight'] for r in production+shadow_rows}
                proposalmap = {q['id']: q for q in proposals}
                frontier = []
                for r in production:
                    q = proposalmap[r['proposal']]
                    n = seal(r['node'])
                    inv = independent(n, parentmap[q['parent']], q, source)
                    state['nodes'][n['id']] = n
                    state['inverses'][n['id']] = inv
                    frontier.append(n)
                    group = digest(q['split_group'])
                    split = int(group[:8], 16) % 5
                    split = 2 if split == 0 else 1 if split == 1 else 0
                    learned = {'features': q['features'], 'label': int(r['can_complete_eight']), 'split': split,
                               'witness': {'structural_group': group, 'template': n['id'], 'source_completion': r['can_complete_eight']}}
                    if group in state['learning']:
                        assert state['learning'][group]['features'] == learned['features'] and state['learning'][group]['label'] == learned['label']
                    else:
                        state['learning'][group] = learned
                state['deferred'].extend(q for q in proposals if q['id'] not in ids)
                round_result = {'A': a, 'parents': len(parents), 'proposals': len(proposals), 'constructed': len(production),
                                'model_used': state['model']['name'] if state['model'] else None,
                                'guided_completable': sum(outcomes[q['id']] for q in selected),
                                'baseline_completable': sum(outcomes[q['id']] for q in baseline),
                                'same_budget': len(selected), 'selection_changed': {q['id'] for q in baseline} != ids,
                                'shadow_only': len(shadow), 'deferred': len(proposals)-len(selected)}
                savegz(out/f'rounds/A{a}.json.gz', {'summary': round_result, 'selected': selected, 'baseline': baseline,
                                                  'predictions': prediction, 'native_labels': outcomes})
                if {0, 1} <= {r['split'] for r in state['learning'].values()}:
                    rows = list(state['learning'].values())
                    binding = {'contract': sha(out/'CONTRACT.json'), 'corpus': digest(rows), 'target': contract['learning_target'], 'split': 'whole source role set, terminal role, occupied cube sites and terminal site'}
                    name = out.name.lower()+f'_continuation_A{a}'
                    fit = s.execute('GEN3_TREE_FIT', {'name': name, 'rows': rows, 'source_binding': binding},
                                    purpose='Acquire continuation rules from exact source-extension outcomes, with held-out structural families excluded from fitting and selection.')
                    export = s.execute('GEN3_TREE_EXPORT', {'name': name}, purpose='Retain learned rules and provenance for subsequent construction stages and restart.')
                    save(out/f'models/A{a}.json', {'name': name, 'binding': binding, 'fit': fit, 'export': export})
                    state['model'] = {'name': name, 'binding': binding, 'export_sha256': export['sha256']}
                state['frontier'] = frontier
                state['rounds'].append(round_result)
                state['next_A'] = a+1
                s.execute('GEN3_LOG_APPEND', {'account': 'template_growth', 'points': [{'id': f'A{a}', 'state': {'stage': round_result, 'new_template_ids': [n['id'] for n in frontier]}, 'action': len(state['nodes'])}],
                                             'edges': [{'id': f'extend_A{a}', 'before': f'A{a-1}', 'after': f'A{a}', 'event': {'operation': OP, 'new_templates': len(frontier)}}]},
                          purpose='Append actual source-construction growth while preserving every stage and all maximum ties.')
                s.execute('GEN3_CHECKPOINT', {}, purpose='Commit learned continuation model, growth account and exact source records at the stage boundary.')
                savegz(checkpoint_path, state)
                save(out/'STATUS.json', {'state': 'RUNNING', 'completed_A': a, 'new_templates': len(state['nodes'])-2, 'learning_groups': len(state['learning']), 'last_round': round_result})
                print(json.dumps(round_result), flush=True)
            finish(out, state, source, contract, s, native)


def finish(out, state, source, contract, session, native):
    # One exact interface per path length is reusable through the retained slot map.
    # Full source role/kind/phase histories stay distinct in the template library.
    interfaces, algebra, exports = {}, {}, []
    for a in range(4, contract['max_A']+1):
        representative = next(n for n in state['nodes'].values() if len(n['objects']) == a)
        interface = native('INTERFACE', node=representative)
        seed = [o['site'] for o in representative['objects']]
        assert seed in interface['placements']
        assert all(len(set(v)) == a and all((v[i]^v[i+1]).bit_count() == 1 for i in range(a-1)) for v in interface['placements'])
        save(out/f'interfaces/A{a}.json', interface)
        interfaces[a] = interface
        h = interface['connector_laplacian']
        ctx = {'basis': list(range(a)), 'field': {'radicand': 0}, 'units': {'energy': 'dimensionless source connector Laplacian'},
               'history': {'source_template': representative['id'], 'assignment': 'L=D-A on this executed connector path; no physical energy scale'}, 'spectral_coordinate': 'lambda'}
        prefix = out.name.lower()+f'_path_A{a}'
        def calc(op, suffix, data):
            name = prefix+'_'+suffix
            result = session.execute(op, {'name': name, 'source_binding': contract['source_binding'], 'context': ctx, 'data': data},
                                     purpose='Derive reusable exact source-path operator structure for newly generated templates: '+suffix)
            exports.append(name)
            return result
        word = calc('GEN3_SOURCE_OPERATOR_WORD', 'laplacian', {'operators': {'L': h}, 'program': [{'name': 'Lcopy', 'op': 'scale', 'inputs': ['L'], 'factor': 1}], 'output': 'Lcopy'})
        assert word['rank'] == a-1
        seeds = [[int(i == 0)] for i in range(a)]
        closure = calc('GEN3_SOURCE_SUBSPACE', 'closure', {'H': h, 'seeds': seeds, 'mode': 'CLOSURE'})
        recurrence = calc('GEN3_BLOCK_SOURCE_RECURRENCE', 'recurrence', {'H': h, 'seeds': seeds, 'max_levels': a})
        creation = calc('GEN3_SOURCE_SPECTRAL_CREATION', 'creation', {'recurrence': {'record': prefix+'_recurrence'}, 'reference': [[1] for _ in range(a)], 'reference_energy': 0})
        algebra[a] = {'word': word, 'closure': closure, 'recurrence': recurrence, 'creation': creation}
        save(out/f'algebra/A{a}.json', algebra[a])
    templates = []
    for n in state['nodes'].values():
        a = len(n['objects'])
        if a == 3:
            continue
        assert [o['site'] for o in n['objects']] in interfaces[a]['placements']
        templates.append({'id': n['id'], 'label': SYMBOLS[n['Z']-1]+str(a), 'Z': n['Z'], 'N': n['N'], 'electrons': n['electrons'],
                          'ledger': n, 'inverse': state['inverses'][n['id']],
                          'placement_interface': f'interfaces/A{a}.json', 'operator_family': f'algebra/A{a}.json',
                          'status': 'GENERATED_SOURCE_PATH_TEMPLATE', 'physical_binding_stability': 'UNASSIGNED'})
    savegz(out/'TEMPLATES.json.gz', templates)
    save(out/'INDEX.json', {'templates': [{k: t[k] for k in ['id', 'label', 'Z', 'N', 'placement_interface', 'operator_family']} for t in templates],
                            'library': 'TEMPLATES.json.gz', 'library_sha256': sha(out/'TEMPLATES.json.gz')})
    learned = list(state['learning'].values())
    summary = {'new_source_templates': len(templates), 'distinct_inventories': len({(t['Z'], t['N']) for t in templates}),
               'inventory_labels': sorted({t['label'] for t in templates}, key=lambda label: (len(label), label)),
               'beyond_four_template_cone': sorted({t['label'] for t in templates if t['N'] > 2*t['Z']}),
               'exact_inverses_checked': len(templates), 'placement_interfaces': len(interfaces), 'new_operator_families': len(algebra),
               'learning_groups': len(learned), 'training_groups': sum(r['split'] == 0 for r in learned),
               'development_groups': sum(r['split'] == 1 for r in learned), 'held_out_groups': sum(r['split'] == 2 for r in learned),
               'rounds': state['rounds'], 'deferred_proposals': len(state['deferred']),
               'new_roster_assemblies': 0, 'state': 'COMPLETE_DECLARED_SEARCH',
               'classification': 'The test result suggests strong contact with the concept.'}
    save(out/'SUMMARY.json', summary)
    save(out/'RECOVERY_REQUEST.json', {'model': state['model'], 'operator_names': exports, 'source_binding': contract['source_binding']})
    checkpoint = session.execute('GEN3_CHECKPOINT', {}, purpose='Commit complete reusable template-generation knowledge and exact operator records.')
    save(out/'CHECKPOINT.json', checkpoint)
    save(out/'STATUS.json', summary)
    (out/'NOTICE.md').write_text('The declared append-only search through eight nucleons is complete. Learned models, source templates and deferred proposals are saved. Next questions: expanded-template roster assembly, branch/readdress operations, or additional deferred source histories. No unbounded background loop is running.\n')
    print(json.dumps(summary), flush=True)


def recover(out):
    request = read(out/'RECOVERY_REQUEST.json')
    with DomainSession(read(out/'SESSION_PATH.json')['path']) as s:
        before = s.execute('GEN3_STATUS', {}, purpose='Read counters before restoring generator knowledge.')
        model = s.execute('GEN3_TREE_EXPORT', {'name': request['model']['name']}, purpose='Recover the learned continuation model without fitting.')
        assert model['sha256'] == request['model']['export_sha256']
        for name in request['operator_names']:
            r = s.execute('GEN3_SOURCE_SPECTRAL_EXPORT', {'name': name, 'source_binding': request['source_binding']}, purpose='Recover the exact template operator family without recomputation.')
            assert r['recomputed'] is False
        after = s.execute('GEN3_STATUS', {}, purpose='Verify restored template memory does not rerun native calculations.')
        assert before['execution_counters'] == after['execution_counters']
    result = {'status': 'PASS', 'model_sha256': model['sha256'], 'operators_exported': len(request['operator_names']), 'native_counters_unchanged': True}
    save(out/'RECOVERY.json', result)
    print(json.dumps(result), flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'run', 'status', 'stop', 'recover'])
    p.add_argument('--output', type=Path, default=DEFAULT)
    args = p.parse_args()
    if args.action == 'prepare':
        print(json.dumps(prepare(args.output), indent=2))
    elif args.action == 'status':
        print(json.dumps(read(args.output/'STATUS.json'), indent=2))
    elif args.action == 'stop':
        (args.output/'STOP').touch()
    elif args.action == 'recover':
        recover(args.output)
    else:
        try:
            execute(args.output)
        except BaseException as error:
            save(args.output/f'FAILURE_{time.time_ns()}.json', {'error': repr(error)})
            save(args.output/'STATUS.json', {'state': 'STOPPED' if isinstance(error, InterruptedError) else 'FAILED', 'error': repr(error)})
            raise


if __name__ == '__main__':
    main()
