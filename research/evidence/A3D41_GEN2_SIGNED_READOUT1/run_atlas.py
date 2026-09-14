"""Orchestrate actual GEN2 T18 transitions and exact Li6 construction algorithms.

Python enumerates source requests and serializes returned values. It does not
evaluate the transition law, construction forms, inverses or information scores.
"""
from pathlib import Path
import json
import time
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from SAM_PROJECT.session import DomainSession

HERE = Path(__file__).resolve().parent
SESSION = ROOT / 'SAM_REVIEW/campaigns/PROJECT_DOMAIN_SESSIONS1/sessions/ATOM3D_c51c939ff7ce489196cfb2aa0bcbfc43'

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def main():
    started = time.perf_counter()
    selection = json.loads((ROOT / 'CURRENT_REVISION/domains/ATOM3D/li6_grammar_source/SELECTION_DERIVATION.json').read_text())['states']
    save('PLAN.json', {
        'objective': 'Determine whether native single-Write responses distinguish the tied Li6 source constructions and selected histories.',
        'direction': 'Sean Brady; utilize genuine GEN2 algorithmic computation whenever possible',
        'technical_mapping': 'Codex: eighteen signed quarter Writes on each selected state, followed by native isotope construction response and exact finite inverse/information algorithms.',
        'source_history': 'H000976', 'states': selection, 'covers': [3, 4], 'assignments': list(range(6)), 'rho': 1,
        'controls': ['Unperturbed selected states', 'Both Write orientations', 'All retained covers and placements'],
        'source_to_operation': {'transitions': 'T18_WORD', 'construction_forms_and_responses': 'GEN2_BOUNDARY_OPEN kind LI6', 'inverse_and_information': 'GEN2_CUSTODY / GEN2_BOUNDARY_INFORMATION', 'signed_arithmetic': 'GEN2_SIGNED_LOG'},
        'interpretation': 'Candidate source-action response and distinguishability; phase coordinates retain their source meaning. Physical spin, magnetic/quadrupole coefficients and MeV conversion remain unassigned.',
        'prior': 'Uniform finite source roster for information accounting only; no physical population distribution assigned.',
        'session': str(SESSION),
    })
    session = DomainSession(SESSION)
    calls = []
    known = set((SESSION / 'calls').iterdir())
    def execute(operation, payload, purpose):
        nonlocal known
        answer = session.execute(operation, payload, purpose=purpose)
        current = set((SESSION / 'calls').iterdir())
        added = current - known
        assert len(added) == 1
        calls.append({'operation': operation, 'purpose': purpose, 'directory': str(added.pop().relative_to(ROOT))})
        known = current
        save('ATLAS_CALLS.json', calls)
        return answer
    words = []
    for item in selection:
        for edge in range(9):
            for sign in (1, -1):
                result = execute('T18_WORD', {'address': item['state'], 'writes': [[edge, sign]], 'source_endpoint': 'LI6_SOURCE', 'target_endpoint': 'LI6_RESPONSE', 'shell_state': 0},
                    f"Native one-Write Li6 response source: state {item['state']}, edge index {edge}, sign {sign}.")
                words.append({'before': item['state'], 'edge': edge, 'sign': sign, 'after': result['address_after'],
                              'phases_before': result['motion']['initial_phases'], 'phases_after': result['motion']['final_phases'],
                              'receipt': calls[-1]['directory'], 'semantic_sha256': result['semantic_sha256']})
        print(f"Native Writes complete for {item['state']}: {len(words)}/288", flush=True)
    save('WORDS.json', words)
    states = sorted({x['state'] for x in selection} | {x['after'] for x in words})
    atlas = []
    for cover in (3, 4):
        for assignment in range(6):
            alternatives = [{'state': state, 'cover': cover, 'assignment': assignment, 'rho': 1} for state in states]
            result = execute('GEN2_BOUNDARY_OPEN', {'source': {'kind': 'LI6', 'alternatives': alternatives}, 'measure': {'kind': 'UNIFORM'}},
                f'Compute exact Li6 construction forms, source responses and signed site/cycle currents on {len(states)} distinct native one-Write/base states: cover {cover}, placement {assignment}, rho 1.')
            for member in result['members']:
                variables = member['variables']
                atlas.append({'configuration': variables['INTERIOR_CONFIGURATION'], 'native': variables['EXTERIOR:native'],
                              'observed': variables['EXTERIOR:observed'], 'sites': variables['EXTERIOR:SITES'],
                              'cycles': variables['EXTERIOR:CYCLES'],
                              'components': {k:v for k,v in variables.items() if k.startswith('COMPONENT:')},
                              'receipt': calls[-1]['directory']})
            save('ATLAS.json', atlas)
            print(f"Native construction batch cover={cover} placement={assignment}: {len(result['members'])} rows, cumulative {len(atlas)}", flush=True)
    save('ATLAS_RUN.json', {'status': 'RETURNED', 'native_write_calls': len(words), 'distinct_source_states': len(states),
                          'native_construction_evaluations': len(atlas), 'calls': len(calls), 'seconds': time.perf_counter()-started})
    session.close()

if __name__ == '__main__':
    main()
