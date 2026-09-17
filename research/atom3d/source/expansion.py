"""Stable-first named construction expansion, using the completed source constructors.

The finite queue adds reference identities only after source placement and local
operator admission. Source-template synthesis is an explicit separate frontier.
"""
import argparse
import collections
import fcntl
import gzip
import json
import shutil
import subprocess
import time
from pathlib import Path

from .compiler import ROOT, HERE, sha
from .construction import read, save
from .catalog import SYMBOLS
from .roster_batch import A32, A33, independent
from SAM_PROJECT.session import DomainSession
from CURRENT_REVISION.runtime import current_generation

BASE = ROOT / 'SAM_REVIEW/campaigns'
DEFAULT = BASE / 'GEN3_ISOTOPE_EXPANSION1'
REFERENCE = BASE / 'GEN3_ISOTOPE_RESEARCH1/reference/nubase_4.mas20'
LAYERS = BASE / 'GEN3_ISOTOPE_LAYERS2/INPUT.json'
FAMILIES = BASE / 'GEN3_ROSTER_COVERAGE1'
BINARIES = {
    'ISOTOPE_COMPACT_CATALOG_V1': BASE / 'GEN3_ISOTOPE_CATALOG2/catalog-native',
    'ISOTOPE_SOURCE_LAYER_CONSTRUCT_V1': BASE / 'GEN3_ISOTOPE_LAYERS2/layers-native',
    'ISOTOPE_GENERAL_OCCUPANCY_CONSTRUCT_V1': FAMILIES / 'roster-batch-native',
}


def reference_rows():
    rows = {}
    for line in REFERENCE.read_text().splitlines():
        if len(line) < 80 or not line[:3].strip().isdigit() or not line[4:8].isdigit() or line[7] != '0':
            continue
        a, z = int(line[:3]), int(line[4:7])
        if not 1 <= z <= 118 or a < z:
            continue
        n = a - z
        if (z, n) in rows:
            raise ValueError('Duplicate reference ground state')
        rows[z, n] = {'Z': z, 'N': n, 'label': SYMBOLS[z-1]+str(a),
                      'reference_stable': line[69:78].strip() == 'stbl'}
    return rows


def prepare(out):
    out.mkdir(parents=True, exist_ok=True)
    if (out / 'CONTRACT.json').exists():
        return read(out / 'CONTRACT.json')
    prior = read(HERE / 'CURRENT.json')
    roster = read(ROOT / prior['roster']['path'])
    old = {(r['Z'], r['N']) for r in roster['rows']}
    refs = reference_rows()
    missing = sorted((r for k, r in refs.items() if k not in old),
                     key=lambda r: (not r['reference_stable'], r['Z']+r['N'], r['Z']))
    paths = [REFERENCE, LAYERS, FAMILIES/'INPUT.json', FAMILIES/'COVERAGE.json',
             A32, A33, ROOT/prior['roster']['path'], Path(__file__),
             HERE/'native/catalog.cpp', HERE/'native/layers.cpp', HERE/'native/roster_batch.cpp']
    files = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    # Carry the established source pins and exact receiver-prefix commitment.
    inherited = read(LAYERS)['source_binding']
    files.update(inherited['files'])
    contract = {
        'schema': 'GEN3_ISOTOPE_EXPANSION_V1', 'generation': current_generation(),
        'source_binding': {'files': files, 'receiver_prefix': inherited['receiver_prefix']},
        'binaries': {op: {'path': str(p.relative_to(ROOT)), 'sha256': sha(p)} for op, p in BINARIES.items()},
        'objective': 'Add named source constructions, prioritizing missing reference-stable targets, using the A3D38 constructor precedent.',
        'mapping': 'NUBASE ground-state identities and stable designation schedule work. Exact four-template recipes feed the established source-root allocation. Each retained occurrence is bound to a labelled local occupancy operator. Target mass, energy and lifetime values are not construction inputs.',
        'reference': {'path': str(REFERENCE.relative_to(ROOT)), 'sha256': sha(REFERENCE),
                      'source_url': 'https://amdc.impcas.ac.cn/masstables/Ame2020/nubase_4.mas20',
                      'consumed_fields': ['A', 'Z', 'ground_state_flag', 'stable_designation']},
        'prior_roster': prior['roster'], 'prior_targets': len(old),
        'reference_targets': len(refs), 'missing_targets': len(missing),
        'missing_stable': [r['label'] for r in missing if r['reference_stable']],
        'template_synthesis': 'NOT_IMPLEMENTED: source-history extension is a separate construction operation, not a combination of the four input templates.',
        'cleanup_trigger_bytes': 300*2**30, 'minimum_free_bytes': 20*2**30,
        'retention': 'Keep all unique constructions, source pins, sparse operators and receipts. At 300GiB delete only interrupted *.tmp writes in this campaign; stop with a notice if more space is needed.',
        'stop': 'Owner STOP, storage admission, generation change, or finite queue exhaustion. Exhaustion writes NOTICE.md and FRONTIER.json.',
    }
    save(out/'PRIOR_CURRENT.json', prior)
    save(out/'TARGETS.json', missing)
    save(out/'CONTRACT.json', contract)
    save(out/'STATUS.json', {'state': 'READY', 'new_named_constructions': 0, 'targets': len(missing)})
    return contract


class Consumer:
    def __init__(self, consumer, contract):
        self.consumer, self.contract = consumer, contract

    def __getattr__(self, name):
        return getattr(self.consumer, name)

    def execute(self, operation, payload):
        if operation not in self.contract['binaries']:
            return self.consumer.execute(operation, payload)
        spec = self.contract['binaries'][operation]
        binary = ROOT/spec['path']
        if sha(binary) != spec['sha256'] or payload['source_binding'] != self.contract['source_binding']:
            raise ValueError('Native worker/source binding changed')
        result = subprocess.run([str(binary)], input=json.dumps(payload), capture_output=True,
                                text=True, check=True, timeout=600)
        return json.loads(result.stdout)


def sites_for_frame(frame):
    bindings = {x['semantic_sha256']: x for x in read(A32)['compiled']['address_bindings']}
    sites = {}
    for r in read(A33)['compiled']['crosswalk_rows']:
        if r['execution_word'] == frame:
            x = bindings[r['a3d32_binding_ref']['semantic_sha256']]
            side = 0 if x['meaning']['generator_word'] == ['s1', 's2'] else 1
            sites[r['roster_index'], side] = r['frozen_action']['source_site']
    assert len(sites) == 8
    return sites


def admit(out, contract):
    if (out/'STOP').exists():
        raise InterruptedError('Owner STOP')
    if current_generation() != contract['generation']:
        raise ValueError('Generation changed')
    used = sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
    if used >= contract['cleanup_trigger_bytes']:
        removed = []
        for p in out.rglob('*.tmp'):
            removed.append(str(p.relative_to(out)))
            p.unlink()
        save(out/f'CLEANUP_{time.time_ns()}.json', {'removed_interrupted_writes': removed, 'bytes_before': used})
        if sum(p.stat().st_size for p in out.rglob('*') if p.is_file()) >= contract['cleanup_trigger_bytes']:
            raise InterruptedError('Storage trigger reached; retained unique evidence requires review')
    if shutil.disk_usage(out).free < contract['minimum_free_bytes']:
        raise InterruptedError('Free-space reserve reached')


def batch(out, name, targets, session, contract, operators):
    dest = out/name
    if (dest/'RESULT.json').exists():
        return read(dest/'RESULT.json')
    dest.mkdir(exist_ok=True)
    admit(out, contract)
    binding = contract['source_binding']
    catalog = session.execute('ISOTOPE_COMPACT_CATALOG_V1', {'isotopes': targets, 'source_binding': binding},
                              purpose='Construct all exact template recipes for previously absent reference targets.')
    shared = read(LAYERS)
    payload = {k: shared[k] for k in ('pairs', 'reference_words', 'local_recipes')}
    payload.update(targets=catalog['rows'], source_binding=binding)
    layers = session.execute('ISOTOPE_SOURCE_LAYER_CONSTRUCT_V1', payload,
                             purpose='Build minimum-cell source-owned placements for new target identities, retaining source roots, histories and local witnesses.')
    save(dest/'CATALOG.json', catalog)
    save(dest/'CONSTRUCTION.json', layers)
    bykey = {r['key']: r for r in catalog['rows']}
    occ = read(FAMILIES/'INPUT.json')
    sites = sites_for_frame(occ['frame'])
    accepted, blocked = [], []
    for layer in layers['rows']:
        row = bykey[layer['key']]
        if not layer.get('placements'):
            blocked.append({'key': layer['key'], 'label': row['label'], 'Z': row['Z'], 'N': row['N'], 'question': layer['coverage']})
            continue
        factors, owned, totals = [], set(), [0, 0, 0, 0]
        for p in layer['placements']:
            counts = p['counts']
            fid = '_'.join(map(str, counts))
            occurrences = sorted(p['occurrences'], key=lambda o: (o['type'], o['source_anchor']))
            code = 0
            observed = [0, 0, 0, 0]
            for o in occurrences:
                assert o['source_anchor'] not in owned
                owned.add(o['source_anchor'])
                observed[o['type']-1] += 1
                code = 8*code + sites[o['roster'], o['side']]
            assert observed == counts
            totals = [a+b for a, b in zip(totals, counts)]
            if fid not in operators:
                admit(out, contract)
                op_payload = {k: occ[k] for k in ('site_rosters', 'membership', 'edges')}
                op_payload.update(counts=counts, seed_codes=[{'id': row['key'], 'code': code}], source_binding=binding)
                result = session.execute('ISOTOPE_GENERAL_OCCUPANCY_CONSTRUCT_V1', op_payload,
                                         purpose='Construct a missing local occupancy family with all retained terminal channels.')
                validation = independent(result, op_payload)
                path = out/'operators'/f'{fid}.json.gz'
                path.parent.mkdir(exist_ok=True)
                with gzip.open(path, 'wt') as stream:
                    json.dump(result, stream, separators=(',', ':'))
                operators[fid] = {'path': str(path.relative_to(ROOT)), 'sha256': sha(path),
                                  'indices': {c: i for i, c in enumerate(result['state_codes'])}}
                save(out/'operators'/f'{fid}.validation.json', validation)
            op = operators[fid]
            assert code in op['indices'], (row['label'], fid, code)
            factors.append({'family': fid, 'cell': p['cell'], 'operators': op['path'],
                            'sha256': op['sha256'], 'seed_code': code, 'seed_index': op['indices'][code],
                            'source_anchors_by_slot': [o['source_anchor'] for o in occurrences]})
        assert totals == layer['selected_recipe']
        h1, h2, h3, he3 = totals
        assert (h1+h2+h3+2*he3, h2+2*h3+he3) == (row['Z'], row['N'])
        row.update(source_layer_construction=layer, local_operators=factors,
                   coverage={'inventory': 'COMPLETE_FOUR_TEMPLATE_ENUMERATION', 'source_layers': layer['coverage'],
                             'occupancy': 'COMPLETE_SINGLE_CELL_OCCUPANCY_OPERATOR' if layer['minimum_cells'] == 1 else 'LOCAL_OCCUPANCY_FACTORS_CONSTRUCTED',
                             'physical_energy_stability': 'UNASSIGNED'},
                   next_step='CONSTRUCT_ISOTOPE_SPECIFIC_INTERACTION')
        accepted.append(row)
    result = {'rows': accepted, 'blocked': blocked, 'session': str(session.directory),
              'new_named_constructions': len(accepted),
              'reference_stable_constructions': [r['label'] for r in accepted if r['reference_stable']],
              'independent_check': 'Every accepted inventory, unique custody allocation and local occupancy seed checked.'}
    save(dest/'RESULT.json', result)
    print(json.dumps({'batch': name, 'new_named_constructions': len(accepted), 'stable': result['reference_stable_constructions']}), flush=True)
    return result


def run(out):
    contract = prepare(out)
    with (out/'controller.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if (out/'STATUS.json').exists() and read(out/'STATUS.json')['state'] == 'COMPLETE_AWAITING_NEW_CONSTRUCTION_OPERATION':
            return read(out/'SUMMARY.json')
        for path, digest in contract['source_binding']['files'].items():
            if sha(ROOT/path) != digest:
                raise ValueError('Source changed: '+path)
        operators = {}
        for family in read(FAMILIES/'COVERAGE.json')['local_families']:
            p = ROOT/family['operators']
            if sha(p) != family['operators_sha256']:
                raise ValueError('Prior occupancy family changed')
            with gzip.open(p, 'rt') as stream:
                data = json.load(stream)
            operators[family['family']] = {'path': family['operators'], 'sha256': family['operators_sha256'],
                                            'indices': {c: i for i, c in enumerate(data['state_codes'])}}
        targets = read(out/'TARGETS.json')
        results = []
        started = time.time()
        with DomainSession.start('ATOM3D', objective=contract['objective'], output_root=out/'execution', receipt_storage='gzip') as session:
            print(session.announcement(), session.directory, flush=True)
            session.consumer = Consumer(session.consumer, contract)
            for name, todo in [('stable_first', [r for r in targets if r['reference_stable']]),
                               ('remaining_reference', [r for r in targets if not r['reference_stable']])]:
                result = batch(out, name, todo, session, contract, operators)
                results.append(result)
                save(out/'STATUS.json', {'state': 'RUNNING', 'batch': name,
                                         'new_named_constructions': sum(r['new_named_constructions'] for r in results)})
        new = [r for result in results for r in result['rows']]
        prior = read(ROOT/contract['prior_roster']['path'])
        oldkeys = {r['key'] for r in prior['rows']}
        assert len({r['key'] for r in new}) == len(new) and not oldkeys.intersection(r['key'] for r in new)
        blocked = [r for result in results for r in result['blocked']]
        oldblocked = [{'key': r['key'], 'label': r['label'], 'Z': r['Z'], 'N': r['N'],
                       'question': 'EXTEND_INVENTORY_TEMPLATE_BASIS'} for r in prior['rows'] if not r['decomposition_count']]
        summary = {'prior_roster_targets': len(prior['rows']), 'new_named_source_constructions': len(new),
                   'expanded_roster_targets': len(prior['rows'])+len(new),
                   'new_reference_stable': [r['label'] for r in new if r['reference_stable']],
                   'new_single_cell_operators': sum(r['source_layer_construction']['minimum_cells'] == 1 for r in new),
                   'new_connected_assemblies': sum(r['source_layer_construction']['receiver_components_used'] == 1 for r in new),
                   'new_multicomponent_assemblies': sum(r['source_layer_construction']['receiver_components_used'] > 1 for r in new),
                   'template_frontier_targets': len(blocked)+len(oldblocked),
                   'elapsed_seconds': time.time()-started, 'new_templates_constructed': 0}
        prior['rows'].extend(new)
        prior.update(schema='SAM_ISOTOPE_EXPANDED_CONSTRUCTION_ROSTER_V1', expansion_summary=summary,
                     expansion_contract=str((out/'CONTRACT.json').relative_to(ROOT)))
        prior['summary'].update(isotopes=len(prior['rows']),
                                constructed_targets=prior['summary']['constructed_targets']+len(new),
                                connected_targets=prior['summary']['connected_targets']+summary['new_connected_assemblies'])
        save(out/'ROSTER.json', prior)
        save(out/'SUMMARY.json', summary)
        save(out/'FRONTIER.json', {'template_targets': oldblocked+blocked,
                                  'operation_needed': 'Generate new source ledgers from N100 role assignments and reciprocal connector histories; derive identity and continuation template, then derive its occurrence membership/action interface.',
                                  'precedent': 'ATOM3D/campaigns/ATOM3D_A2_HYDROGEN_LADDER/stages/A2H3_A2HE3/freeze_a3_pair.py',
                                  'state': 'SOURCE_TEMPLATE_GENERATOR_NOT_IMPLEMENTED'})
        (out/'NOTICE.md').write_text('The finite established-constructor queue is complete. '+str(len(new))+
            ' new named source constructions are retained. Next work requires source-template generation and/or inter-cell interaction construction. No template search is currently running.\n')
        save(out/'STATUS.json', {'state': 'COMPLETE_AWAITING_NEW_CONSTRUCTION_OPERATION', **summary})
        print(json.dumps(summary), flush=True)
        return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run', 'status', 'stop'])
    parser.add_argument('--output', type=Path, default=DEFAULT)
    args = parser.parse_args()
    if args.action == 'prepare':
        print(json.dumps(prepare(args.output), indent=2))
    elif args.action == 'status':
        print(json.dumps(read(args.output/'STATUS.json'), indent=2))
    elif args.action == 'stop':
        (args.output/'STOP').touch()
    else:
        try:
            run(args.output)
        except BaseException as error:
            save(args.output/f'FAILURE_{time.time_ns()}.json', {'error': repr(error)})
            save(args.output/'STATUS.json', {'state': 'STOPPED' if isinstance(error, InterruptedError) else 'FAILED', 'error': repr(error)})
            (args.output/'NOTICE.md').write_text(str(error)+'\n')
            raise


if __name__ == '__main__':
    main()
