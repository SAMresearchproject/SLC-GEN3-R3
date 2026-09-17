"""Use the installed generated-template library and its acquired search model."""
import argparse
import collections
import json
import time
from fractions import Fraction

from .compiler import ROOT, HERE, sha
from .construction import read, save
from .template_generator import readgz
from SAM_PROJECT.session import DomainSession


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['list', 'export', 'proposals'])
    parser.add_argument('--label')
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()
    current = read(HERE/'TEMPLATE_CURRENT.json')
    out = ROOT/current['campaign']
    library = ROOT/current['library']['path']
    if sha(library) != current['library']['sha256']:
        raise ValueError('Installed template library changed')
    asset_path = ROOT/current['assets']['path']
    if sha(asset_path) != current['assets']['sha256']:
        raise ValueError('Installed template asset manifest changed')
    assets = read(asset_path)['files']
    def artifact(relative):
        path = out/relative
        if sha(path) != assets[relative]:
            raise ValueError('Installed template artifact changed: '+relative)
        return read(path)
    index = artifact('INDEX.json')['templates']
    if args.action == 'list':
        print(json.dumps({'inventories': dict(sorted(collections.Counter(t['label'] for t in index).items())),
                          'templates': len(index), 'state': current['state'], 'model': current['model']['name']}, indent=2))
        return
    if not args.label:
        parser.error('--label is required')
    matches = [t for t in index if t['label'] == args.label.replace('-', '')]
    if not matches:
        parser.error('No generated source template for that inventory')
    if args.action == 'export':
        selected = min(matches, key=lambda t: t['id'])
        template = next(t for t in readgz(library) if t['id'] == selected['id'])
        print(json.dumps({'template': template, 'other_retained_history_ids': [t['id'] for t in matches if t['id'] != selected['id']],
                          'template_slot_map': template['ledger']['objects'],
                          'transport': 'The shared path prototype uses ordered slots; this template retains its own role, kind, site and full connector history through the slot map.',
                          'placement_interface': artifact(selected['placement_interface']), 'operator_family': artifact(selected['operator_family'])}, indent=2))
        return
    state = readgz(out/'SEARCH.json.gz')
    inventory = matches[0]['Z'], matches[0]['N']
    proposals = [q for q in state['deferred'] if (q['Z'], q['N']) == inventory]
    model = state['model']
    if not proposals:
        print(json.dumps({'label': args.label, 'deferred_proposals': 0}))
        return
    with DomainSession(read(out/'SESSION_PATH.json')['path']) as s:
        predictions = s.execute('GEN3_TREE_PREDICT', {'name': model['name'], 'source_binding': model['binding'],
                                                     'rows': [{'id': q['id'], 'features': q['features']} for q in proposals]},
                                purpose='Use installed continuation learning to rank owner-requested deferred source-template questions without fitting.')
        probabilities = {r['id']: Fraction(r['probability']) for r in predictions['predictions']}
        ordered = sorted(proposals, key=lambda q: (-probabilities[q['id']], q['id']))
        receipt = out/'queries'/f'{time.time_ns()}.json'
        save(receipt, {'label': args.label, 'session': str(s.directory), 'predictions': predictions, 'proposals': proposals})
    print(json.dumps({'label': args.label, 'deferred_proposals': len(proposals), 'model': model['name'],
                      'full_prediction_receipt': str(receipt), 'all_probability_ties_retained': True,
                      'first_proposals': [{'id': q['id'], 'probability': str(probabilities[q['id']]), 'parent': q['parent']} for q in ordered[:max(1, args.limit)]]}, indent=2))


if __name__ == '__main__':
    main()
