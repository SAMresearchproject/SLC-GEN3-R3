"""AN0003/4/5 executed by the retained native exact contribution DAG.

Every returned operand is a node of GEN2_SIGNED_LOG. Large rational clock
operands keep exact unfactored log arguments. Source pi endpoints are rational
substitutions into the retained symbolic formula, never identities for pi.
"""
from copy import deepcopy
from functools import lru_cache
from .exact import canonical, digest, rational
from . import signed_log

_FOUNDATION = None
_STATS = {'graphs_executed': 0, 'nodes_executed': 0, 'cached_graphs_reused': 0}


def bind(foundation):
    global _FOUNDATION
    _FOUNDATION = foundation


def _engine():
    if _FOUNDATION is None:
        from CURRENT_REVISION.engines.SLC.native.runtime import Q3Runtime
        with Q3Runtime() as runtime:
            bind(runtime.exact_information())
    return _FOUNDATION


def reuse_stats(reset=False):
    result = dict(_STATS)
    if reset:
        _STATS.update(dict.fromkeys(_STATS, 0))
    return result


def _source():
    from .write_foundation import _data
    return _data()


class Graph:
    def __init__(self, account):
        self.nodes = []
        self.account = account
        self.source = {'foundation': _source()[1], 'account': account}

    def value(self, name, value):
        self.nodes.append({'id': name, 'op': 'VALUE', 'value': canonical(rational(value)),
                           'source': self.source})
        return name

    def binary(self, name, op, a, b):
        self.nodes.append({'id': name, 'op': op, 'left': a, 'right': b})
        return name

    def square(self, name, a):
        return self.binary(name, 'MULTIPLY', a, a)

    def run(self, outputs):
        result = signed_log.dispatch('GEN2_SIGNED_LOG',
            {'nodes': self.nodes, 'representation': 'RATIONAL', 'result_id': next(reversed(outputs.values()))}, _engine())
        if any(n['status'] != 'DEFINED' for n in result['nodes']):
            raise ValueError('Foundation source produced an undefined arithmetic node')
        values = {n['id']: n['value'] for n in result['nodes']}
        _STATS['graphs_executed'] += 1
        _STATS['nodes_executed'] += len(self.nodes)
        return {'schema': 'GEN2_WRITE_ARITHMETIC_V1', 'account': self.account,
                'source': self.source, 'coordinate_model':'EXACT_NORMALIZED_SOURCE_COEFFICIENTS', 'outputs': outputs,
                'values': {k: values[v] for k,v in outputs.items()},
                'checkpoint': result['checkpoint']}


def phase(count, net):
    if type(count) is not int or count < 0 or any(type(v) is not int for v in net.values()):
        raise ValueError('Completed-event phase accounts require exact integer counts')
    if sum(abs(v) for v in net.values()) > count or (count-sum(net.values())) % 2:
        raise ValueError('Signed phase counts differ from completed directed events')
    key = (count, tuple(sorted(net.items())))
    before = _phase.cache_info().hits
    result = _phase(key)
    _STATS['cached_graphs_reused'] += _phase.cache_info().hits-before
    return deepcopy(result)


@lru_cache(maxsize=128)
def _phase(key):
    count, net = key
    g = Graph('COMPLETED_WRITE_PHASE_ACTION')
    g.value('writes', count);g.value('four',4);g.value('two',2)
    outputs = {'completed_writes':'writes',
        'total_phase_variation_turns':g.binary('turns','DIVIDE','writes','four'),
        'absolute_phase_action_over_hbar_pi':g.binary('action','DIVIDE','writes','two')}
    for coordinate, value in net:
        a=g.value('net_'+coordinate,value)
        outputs['net_quarters_'+coordinate]=a
        outputs['net_turns_'+coordinate]=g.binary('turns_'+coordinate,'DIVIDE',a,'four')
        outputs['net_action_over_hbar_pi_'+coordinate]=g.binary('action_'+coordinate,'DIVIDE',a,'two')
    return g.run(outputs)


@lru_cache(maxsize=1)
def clocks():
    data = _source()[0]; source = data['effective_clock']; g=Graph('CEFF_CLOCK_AND_CMB_REFERENCE')
    g.value('zero',0);g.value('one',1);g.value('two',2);g.value('c',299792458)
    g.value('G',data['cmb_scale']['constants']['G'])
    g.value('R_CMB',data['cmb_scale']['reference_values']['R_CMB_metres']['exact'])
    g.square('c2','c');g.binary('twoG','MULTIPLY','two','G')
    g.binary('radius_per_kg','DIVIDE','twoG','c2')
    outputs={'closure_radius_per_kg':'radius_per_kg','R_CMB_metres':'R_CMB',
             't_H_seconds':g.binary('t_H','DIVIDE','R_CMB','c')}
    for side in ('LO','HI'):
        p=g.value(side+'_pi',source['source_pi_enclosure']['lower' if side=='LO' else 'upper'])
        for name,b in (('ZERO','0'),('FLOOR','1/12'),('Z1','7/8'),('CEILING','1')):
            tag=side+'_'+name
            weight=g.value(tag+'_weight',b)
            a=g.binary(tag+'_A','DIVIDE',weight,p)
            f=g.binary(tag+'_f','SUBTRACT','one',a)
            speed=g.binary(tag+'_speed','MULTIPLY','c',f)
            inverse=g.binary(tag+'_inverse_speed','DIVIDE','one',speed)
            g.square(tag+'_speed2',speed)
            outputs[tag+'.local_clock_squared']=g.binary(tag+'_local_clock_squared','DIVIDE','one',tag+'_speed2')
            g.binary(tag+'_twospeed','MULTIPLY','two',speed)
            q=g.binary(tag+'_quarter_per_radius','DIVIDE',p,tag+'_twospeed')
            for key,node in (('A',a),('f',f),('ceff_m_per_s',speed),('seconds_per_native_m',inverse),
                             ('equatorial_quarter_s_per_radius_m',q)):
                outputs[tag+'.'+key]=node
            outputs[tag+'.period_multiplier']=g.binary(tag+'_period','DIVIDE','one',f)
            outputs[tag+'.equatorial_quarter_s_per_home_kg']=g.binary(tag+'_mass','MULTIPLY',q,'radius_per_kg')
            outputs[tag+'.conditional_CMB_quarter_s']=g.binary(tag+'_cmb','MULTIPLY',q,'R_CMB')
    result=g.run(outputs)
    result['symbolic_parameters']={'pi':{'constant':'PI','enclosure':source['source_pi_enclosure']}}
    result['symbolic_relations']={k:source[k] for k in ('A_los','c_eff','quarter_seconds',
        'local_dt_dphi_squared_per_radius_squared','equatorial_quarter_seconds_per_radius_m',
        'equatorial_mass_conversion_seconds_per_kg','same_transformed_event_identity')}
    result['endpoint_meaning']='EXACT_RATIONAL_SUBSTITUTIONS_AT_SOURCE_PI_ENCLOSURE_ENDPOINTS'
    result['units']={'ceff_m_per_s':'m/s','seconds_per_native_m':'s/m',
        'equatorial_quarter_s_per_radius_m':'s/m','equatorial_quarter_s_per_home_kg':'s/kg',
        'conditional_CMB_quarter_s':'s','local_clock_squared':'s^2/m^2'}
    return result


def local(values):
    keys=('CA_re','CA_im','CB_re','CB_im','E')
    key=tuple(str(rational(values[k])) for k in keys)
    before=_local.cache_info().hits;result=_local(key)
    _STATS['cached_graphs_reused']+=_local.cache_info().hits-before
    return deepcopy(result)


@lru_cache(maxsize=256)
def _local(values):
    g=Graph('SIGNED_ACTIVATION_LOCAL_DENSITY_CLOCK')
    for name,value in zip(('ar','ai','br','bi','E'),values):g.value(name,value)
    for name,value in (('zero',0),('four',4),('eight',8),('six',6),('thirtysix',36),('c144',144)):
        g.value(name,value)
    for name in ('ar','ai','br','bi','E'):g.square(name+'2',name)
    g.binary('ca2','ADD','ar2','ai2');g.binary('cb2','ADD','br2','bi2')
    g.binary('Ba','DIVIDE','ca2','four');g.binary('Bb','DIVIDE','cb2','four')
    g.binary('pair2','ADD','ca2','cb2');g.binary('B','DIVIDE','pair2','eight')
    g.binary('real','ADD','ar','br');g.binary('E_recovered','ADD','six','real')
    g.binary('ga','SUBTRACT','zero','ai');g.binary('gb','SUBTRACT','zero','bi');g.binary('gp','ADD','ai','bi')
    g.binary('Eplus36','ADD','E2','thirtysix');g.square('density_numerator','Eplus36')
    outputs={k:k for k in ('B','Ba','Bb','E','E_recovered','ga','gb','gp')}
    clock=clocks(); clock_ref=digest(clock['checkpoint'])
    for endpoint in _source()[0]['effective_clock']['local_clock_squared']:
        g.value(endpoint+'_clock_base',clock['values'][endpoint+'.local_clock_squared'])
        g.nodes[-1]['source']={'account':'NATIVE_CLOCK_GRAPH_OUTPUT','checkpoint_sha256':clock_ref,
                              'node':clock['outputs'][endpoint+'.local_clock_squared']}
    for role in ('a','b','p'):
        g.square('g'+role+'2','g'+role)
        g.binary(role+'_den0','ADD','E2','g'+role+'2')
        g.binary(role+'_den','MULTIPLY','c144',role+'_den0')
        d=g.binary('D2_'+role,'DIVIDE','density_numerator',role+'_den');outputs['D2_'+role]=d
        for endpoint in _source()[0]['effective_clock']['local_clock_squared']:
            name=endpoint+'_'+role
            outputs[name]=g.binary(name,'DIVIDE',endpoint+'_clock_base',d)
    result=g.run(outputs);v=result['values']
    if rational(v['Ba'])!=rational(v['Bb']) or rational(v['B']) not in (0,1) or rational(v['E'])<=0 or v['E']!=v['E_recovered']:
        raise ValueError('Signed witnesses do not satisfy the completed one-gate J4 source')
    result['clock_graph_reference']={'checkpoint_sha256':clock_ref,'account':clock['account']}
    return result


def dispatch(operation,payload):
    """Existing READOUT/INVERSE strategy; ordinary histories need no extra call."""
    account=payload.get('account','local')
    if operation=='READOUT':
        if account=='local':return local(payload['values'])
        if account=='phase':return phase(payload['completed_writes'],payload['signed_net_quartersteps'])
        if account=='clock':return deepcopy(clocks())
        if account=='golden':
            from .golden import quarter_count
            n=payload['packets'];k=quarter_count(n)
            g=Graph('GOLDEN_COMPLETED_PACKET_ACTION');g.value('packets',n);g.value('designated',k)
            g.binary('completed','ADD','packets','designated');g.value('four',4);g.value('two',2)
            g.binary('turns','DIVIDE','completed','four');g.binary('action','DIVIDE','completed','two')
            result=g.run({k:k for k in ('packets','designated','completed','turns','action')})
            result['golden_source']={'exact_floor':'floor(n*(6-2*sqrt(5))+1/2)','implementation':'gen2.golden.quarter_count'}
            return result
    if operation=='READOUT_INVERSE':
        if account=='local':
            observed={k:rational(v) for k,v in payload['observed'].items()}
            allowed={'B','E','D2_a','D2_b','D2_p','ga','gb','gp'}
            if not observed or set(observed)-allowed:raise ValueError('Unknown or empty foundation observation')
            atlas=_source()[0]['local_action']['atlas'];members=[]
            domain=payload.get('domain',list(atlas))
            if len(domain)!=len(set(domain)) or any(k not in atlas for k in domain):raise ValueError('Invalid native phase/gate domain')
            for key in domain:
                result=local(atlas[key]['values'])
                if all(rational(result['values'][k])==v for k,v in observed.items()):
                    members.append({'atlas_id':key,'q':atlas[key]['q'],'B':atlas[key]['B']})
            return {'schema':'GEN2_JOINT_ANSWER_V1','strategy':'WRITE_FOUNDATION','account':account,
                'complete':True,'unique':len(members)==1,'members':members,'member_count':len(members),
                'domain_count':len(domain),'observed':canonical(observed),'source':_source()[1]}
        if account=='phase':
            if not payload['observed']:raise ValueError('A phase inverse needs an observed account')
            from .readouts import linear_inverse
            # Exact joint count, variation, action in [N, turns, action/(hbar*pi)].
            names={'completed_writes':0,'total_phase_variation_turns':1,'absolute_phase_action_over_hbar_pi':2}
            rows=[[1,-4,0],[1,0,-2]];rhs=[0,0]
            for k,v in payload['observed'].items():
                if k not in names:raise ValueError('Unknown phase inverse observation')
                row=[0,0,0];row[names[k]]=1;rows.append(row);rhs.append(v)
            result=linear_inverse(rows,rhs)
            if result['unique']:
                n=rational(result['members'][0][0])
                if n<0 or n.denominator!=1:
                    result.update(unique=False,members=[],member_count=0)
            result['coordinate_names']=list(names);result['completed_write_domain']='NONNEGATIVE_INTEGER'
            return result
        if account=='clock':
            if not payload['observed']:raise ValueError('A clock inverse needs an observed account')
            # Solve t/R at an explicitly selected source pi endpoint.
            from .readouts import linear_inverse
            context=payload['context'];side=payload['pi_endpoint']
            if context not in ('ZERO','FLOOR','Z1','CEILING') or side not in ('LO','HI'):
                raise ValueError('Clock inversion needs a source context and pi endpoint')
            coefficient=clocks()['values'][side+'_'+context+'.equatorial_quarter_s_per_radius_m']
            rows=[[-rational(coefficient),1]];rhs=[0]
            names={'radius_m':0,'quarter_seconds':1}
            for k,v in payload['observed'].items():
                if k not in names:raise ValueError('Unknown clock inverse observation')
                row=[0,0];row[names[k]]=1;rows.append(row);rhs.append(v)
            result=linear_inverse(rows,rhs);result['coordinate_names']=list(names)
            if result['unique'] and any(rational(v)<=0 for v in result['members'][0]):
                result.update(unique=False,members=[],member_count=0)
            result['pi_endpoint_meaning']='EXACT_RATIONAL_ENDPOINT_SUBSTITUTION'
            result['context']=context;result['pi_endpoint']=side
            return result
    raise ValueError('Unknown source-defined Write foundation account')


def intern_history(foundation, catalog):
    """One complete exact graph per packet; every occurrence retains its reference."""
    def intern(arithmetic):
        key=arithmetic['checkpoint']['sha256']
        if key not in catalog:
            catalog[key]=arithmetic
        return {'schema':'GEN2_WRITE_ARITHMETIC_REFERENCE_V1', 'graph_sha256':key,
                'account':arithmetic['account'], 'values':arithmetic['values'],
                'outputs':arithmetic['outputs']}
    foundation['phase_clock']['arithmetic']=intern(foundation['phase_clock']['arithmetic'])
    for group in foundation.get('local_sources',[]):
        for row in group['atlas_rows'].values():
            row['computed']['arithmetic']=intern(row['computed']['arithmetic'])
    if 'golden_arithmetic' in foundation:
        foundation['golden_arithmetic']=intern(foundation['golden_arithmetic'])
    clock=clocks()
    catalog.setdefault(clock['checkpoint']['sha256'],clock)
