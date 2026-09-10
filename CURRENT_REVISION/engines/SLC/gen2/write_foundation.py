"""Automatic, source-bound AN0003/4/5 foundation for ordinary GEN2 execution.

Completed source tables are loaded once. History integration reuses those exact
tables and only appends new state/event references. No public operation or flag
is required. Existing native execution and source accounts supply the inputs.
"""
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

from .exact import canonical, digest, rational

SCHEMA = 'GEN2_AUTOMATIC_WRITE_FOUNDATION_V1'
BASE = Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def _data():
    raw = (BASE/'WRITE_FOUNDATION.json').read_bytes()
    data = json.loads(raw)
    if (data.get('schema') != 'SLC_GEN2_WRITE_FOUNDATION_V1'
            or data.get('version') != 'SLC-GEN2-R4.2' or data.get('automatic') is not True):
        raise ValueError('Installed Write foundation identity differs')
    for source in data['sources']:
        path = BASE/'dependencies/write_sources'/source['installed_file']
        if sha256(path.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Integrated Write foundation source differs: '+source['installed_file'])
    binding = {'schema': data['schema'], 'foundation_sha256': sha256(raw).hexdigest(),
               'source_authority': data['source_authority'], 'automatic': True}
    return data, binding


def foundation():
    """Runtime-owned foundation data, isolated from the shared immutable cache."""
    from .write_arithmetic import clocks
    result=deepcopy(_data()[0])
    result['arithmetic']=deepcopy(clocks())
    return result


def binding():
    return deepcopy(_data()[1])


def _phase_clock(count, net):
    from . import write_arithmetic
    arithmetic = write_arithmetic.phase(count, net)
    v = arithmetic['values']
    return {'completed_writes': int(rational(v['completed_writes'])),
            'minimum_retained_advance_turns': '1/4',
            'total_phase_variation_turns': str(rational(v['total_phase_variation_turns'])),
            'absolute_phase_action_over_hbar_pi': str(rational(v['absolute_phase_action_over_hbar_pi'])),
            'signed_net_quartersteps': {k: int(rational(v['net_quarters_'+k])) for k in net},
            'count_basis': 'RETAINED_COMPLETED_DIRECTED_EVENTS',
            'action_basis': 'IDENTIFIED_NATIVE_RECORD_AND_PHYSICAL_ROUTE_PHASE',
            'arithmetic': arithmetic}


def annotate_t18(body):
    net = dict.fromkeys(map(str, range(9)), 0)
    for event in body['directed_history']:
        net[str(event['record_index'])] += event['orientation']
    return canonical({'schema': SCHEMA, 'binding': binding(),
        'phase_clock': _phase_clock(len(body['directed_history']), net),
        'completion': {'X1_completion_custody': body['X1_completion_custody'],
                       'W8_shell_state': body['W8_shell_state'],
                       'source_endpoint': body['source_endpoint'],
                       'target_endpoint': body['target_endpoint']},
        'clock_relation': _data()[0]['effective_clock']['quarter_seconds']})


def _new_history(block, profile):
    data = _data()[0]
    groups = []
    # The completed AN0004 map is the registered native J4 restriction B=1.
    # A custom source retains its own declared construction and phase clock.
    if profile is not None and profile['resolution'] == 'REGISTERED_NATIVE_SOURCE':
        coordinates = sorted({tuple(role['source_coordinates']) for role in profile['roles']
                              if role['source_coordinates'] is not None})
        for source in coordinates:
            groups.append({'source_coordinates': list(source), 'B': 1, 'reference_E': 6,
                           'states': [], 'events': [], 'atlas_rows': {},
                           'equatorial_completed_steps': []})
    return {'schema': SCHEMA, 'binding': binding(),
            'phase_clock': _phase_clock(0, dict.fromkeys(map(str,block.contract.coordinates),0)),
            'local_sources': groups,
            'clock_relations': {k: data['effective_clock'][k] for k in
                ('c_eff','quarter_seconds','equatorial_quarter_seconds_per_radius_m',
                 'local_dt_dphi_squared_per_radius_squared','local_closure',
                 'same_transformed_event_identity','activation_waiting_time_seconds')},
            'clock_reference_levels': data['effective_clock']['levels'],
            'local_density_reference': 'E*=6 (AN0004)',
            'inherited_sphere_reference': 'E_initial (retained motion chart)'}


def _extend_history(block, native, output, start):
    data = _data()[0]
    atlas = data['local_action']['atlas']
    slots = {c: i for i,c in enumerate(block.contract.coordinates)}
    states, program = native['states'], native['program']
    clock = output['phase_clock']
    for label in program[max(start-1, 0):]:
        event = block.events[label]
        clock['signed_net_quartersteps'][str(event.coordinate)] += event.direction
    output['phase_clock'] = _phase_clock(len(program), clock['signed_net_quartersteps'])
    for group in output['local_sources']:
        source = group['source_coordinates']
        for step in range(start, len(states)):
            q = [states[step][slots[c]] for c in source]
            key = ''.join(map(str,q))+':1'
            group['states'].append({'step':step, 'atlas_id':key})
            if key not in group['atlas_rows']:
                group['atlas_rows'][key] = deepcopy(atlas[key])
                group['atlas_rows'][key]['computed'] = local_readout(atlas[key]['values'])
            if step:
                event = block.events[program[step-1]]
                if event.coordinate not in source:
                    continue
                role = ['a','b','p'][source.index(event.coordinate)]
                before = [states[step-1][slots[c]] for c in source]
                equatorial = role == 'p' and before[0] == before[1]
                group['events'].append({'step':step, 'native_event':event.label,
                    'role':role, 'orientation':event.direction,
                    'phase_advance_turns':str(Fraction(event.direction,4)),
                    'before_atlas_id':''.join(map(str,before))+':1', 'after_atlas_id':key,
                    'absolute_action_over_hbar_pi':'1/2',
                    'clock_path':'CONSTANT_D1_PARTNER_QUARTER' if equatorial else 'LOCAL_DENSITY_INTEGRAL'})
                if equatorial:
                    group['equatorial_completed_steps'].append(step)
    return canonical(output)


def annotate_history(block, native, profile):
    return _extend_history(block, native, _new_history(block, profile), 0)


def append_history(block, previous, native, old_state_count):
    if previous['binding'] != binding():
        raise ValueError('Retained history belongs to a different Write foundation')
    if previous['phase_clock']['completed_writes'] != old_state_count-1:
        raise ValueError('Write foundation append boundary differs from native history')
    return _extend_history(block, native, deepcopy(previous), old_state_count)


def annotate_golden(result, schedule_records):
    # Counts are from the actual native event schedule, including a partial packet.
    output = result['motion']['write_foundation']
    turns = sum(row['kind'] == 'TURN' for row in schedule_records)
    partners = sum(row['kind'] == 'AFTER_PACKET' for row in schedule_records)
    from . import write_arithmetic
    from .write_arithmetic import Graph
    graph=Graph('RETAINED_GOLDEN_EVENT_COUNTS')
    graph.value('designated',turns);graph.value('partner',partners)
    graph.binary('completed','ADD','designated','partner')
    arithmetic=graph.run({'designated':'designated','partner':'partner','completed':'completed'})
    output['golden_arithmetic']=arithmetic
    turns=int(rational(arithmetic['values']['designated']));partners=int(rational(arithmetic['values']['partner']))
    output['golden_clock'] = {'designated_completed_writes': turns,
                             'after_packet_completed_writes': partners,
                             'completed_writes': turns+partners,
                             'rounding_law': _data()[0]['golden']['quarter_count']}


def local_readout(values, log_class=None):
    """Ordinary readouts consume the native exact arithmetic graph outputs."""
    from . import write_arithmetic
    arithmetic = write_arithmetic.local(values)
    v = arithmetic['values']
    values = {k:rational(value) for k,value in values.items()}
    densities = {}
    for role in ('a','b','p'):
        d2 = rational(v['D2_'+role])
        densities[role] = {'dimensionless_squared': d2,
            'exact_log_magnitude': {'positive_rational_argument':str(d2),'multiplier':'1/2'},
            'arithmetic_node': arithmetic['outputs']['D2_'+role],
            'local_clock_squared_per_radius_squared_by_pi_endpoint': {
                endpoint:rational(v[endpoint+'_'+role])
                for endpoint in _data()[0]['effective_clock']['local_clock_squared']}}
    return canonical({'schema':SCHEMA,'binding':binding(),'B':int(rational(v['B'])),
        'activation_readout':'SIGNED_RECIPROCAL_PAIR_NORMS', 'E_B':rational(v['E']),
        'signed_witness':{'C_a':[values['CA_re'],values['CA_im']],
                          'C_b':[values['CB_re'],values['CB_im']]},
        'gradient':[rational(v['g'+role]) for role in ('a','b','p')], 'reference_E':6,
        'local_density':densities,'completed_write_count_from_state_alone':None,
        'quarter_clock_relation':_data()[0]['effective_clock']['quarter_seconds'],
        'arithmetic':arithmetic})


def annotate_construction(operation, payload, result):
    if operation.removeprefix('GEN2_') != 'CONSTRUCTION_COMPILE':
        return result
    data = _data()[0]
    if result.get('source_sha256') != data['local_action']['construction_sha256']:
        return result
    result['foundation_binding'] = binding()
    if 'response' not in result:
        return result
    x = [rational(v) for v in payload['values']]
    if len(x) != 7 or x[6] != 1 or any(x[j]*x[j]+x[j+3]*x[j+3] != 1 for j in range(3)):
        result['local_geometry_status'] = 'REQUIRES_SOURCE_UNIT_PHASE_FRAME'
        return result
    result['write_foundation'] = local_readout(result['response']['values'])
    return result
