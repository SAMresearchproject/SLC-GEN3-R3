"""Apply generated template vectors to the previously blocked isotope inventories."""
from .compiler import ROOT, HERE, sha
from .construction import read, save
from .template_generator import DEFAULT, readgz
from SAM_PROJECT.session import DomainSession


def run():
    out = ROOT/'SAM_REVIEW/campaigns/GEN3_TEMPLATE_INVENTORY_BRIDGE1'
    out.mkdir(exist_ok=False)
    targets_path = ROOT/'SAM_REVIEW/campaigns/GEN3_ISOTOPE_EXPANSION1/FRONTIER.json'
    library = readgz(DEFAULT/'TEMPLATES.json.gz')
    state = readgz(DEFAULT/'SEARCH.json.gz')
    candidates = list(state['nodes'].values())
    by_inventory = {}
    for n in sorted(candidates, key=lambda n: n['id']):
        by_inventory.setdefault((n['Z'], n['N']), n)
    binding = {'generator_contract': sha(DEFAULT/'CONTRACT.json'), 'generator_library': sha(DEFAULT/'TEMPLATES.json.gz'),
               'targets': sha(targets_path), 'adapter_source': sha(HERE/'template_bridge.py')}
    save(out/'CONTRACT.json', {'source_binding': binding, 'mapping': 'For target (Z,N), let q,r=divmod(N,Z). Combine Z-r retained (1,q) templates and r retained (1,q+1) templates. GEN3 exactly executes the source inventory matrix times this count vector.',
                               'stage': 'Inventory recipe; generated-template placement and assembly are separate next operations.'})
    rows = []
    with DomainSession.start('ATOM3D', objective='Apply the new source-template basis to the 68 inventory-blocked targets', output_root=out/'sessions', receipt_storage='gzip') as s:
        print(s.announcement(), s.directory, flush=True)
        for target in read(targets_path)['template_targets']:
            z, n = target['Z'], target['N']
            q, r = divmod(n, z)
            left, right = by_inventory[1, q], by_inventory[1, q+1]
            vectors = [[left['Z'], right['Z']], [left['N'], right['N']]]
            coefficients = [[z-r], [r]]
            context = {'basis': ['Z', 'N'], 'field': {'radicand': 0}, 'units': {'quantity': 'exact nuclear inventory'},
                       'history': {'source_templates': [left['id'], right['id']], 'target': target['key']}, 'spectral_coordinate': 'inventory'}
            result = s.execute('GEN3_SOURCE_OPERATOR_WORD', {'name': 'generated_template_'+target['key'], 'source_binding': binding,
                                                             'context': context, 'data': {'operators': {'T': vectors, 'c': coefficients},
                                                                                         'program': [{'name': 'inventory', 'op': 'multiply', 'inputs': ['T', 'c']}], 'output': 'inventory'}},
                               purpose='Execute exact generated-template inventory construction for '+target['label'])
            assert [int(v[0]) for v in result['matrix']] == [z, n]
            recipe = [{'template_id': t['id'], 'count': c, 'Z': t['Z'], 'N': t['N']} for t, c in [(left, z-r), (right, r)] if c]
            rows.append({**target, 'status': 'GENERATED_TEMPLATE_INVENTORY_RECIPE_READY', 'recipe': recipe,
                         'native_record_sha256': result['record_sha256'], 'next_step': 'INSTANCE_AND_CONNECT_GENERATED_TEMPLATE_INTERFACES'})
        checkpoint = s.execute('GEN3_CHECKPOINT', {}, purpose='Retain the 68 exact generated-template inventory constructions.')
        save(out/'RESULT.json', {'targets_with_new_basis_recipes': len(rows), 'new_assembled_roster_entries': 0,
                                 'rows': rows, 'session': str(s.directory), 'checkpoint': checkpoint,
                                 'source_binding': binding, 'classification': 'The test result suggests strong contact with the concept.'})
    print('New source basis supplies exact recipes for', len(rows), 'previously blocked target inventories.', flush=True)


if __name__ == '__main__':
    run()
