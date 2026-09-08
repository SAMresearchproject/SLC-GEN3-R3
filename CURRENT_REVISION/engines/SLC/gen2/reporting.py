"""Source-declared exact observation resolution, separate from native quantities."""
from fractions import Fraction
from .exact import canonical, canonical_bytes, rational

SCHEMA = 'GEN2_REPORTED_OBSERVATION_V1'
EXACT = {'kind': 'EXACT'}


def normalize_report(raw):
    if not isinstance(raw, dict) or raw.get('kind') not in ('EXACT', 'ABOVE_SAME_BELOW', 'BINS'):
        raise ValueError('Report rule must be EXACT, ABOVE_SAME_BELOW or complete exact BINS')
    kind = raw['kind']
    if kind == 'EXACT':
        if set(raw) != {'kind'}: raise ValueError('EXACT report takes no resolution parameters')
        return dict(EXACT)
    if kind == 'ABOVE_SAME_BELOW':
        if set(raw) != {'kind', 'reference'}: raise ValueError('Relative report needs its source reference')
        ref = raw['reference']
        if not isinstance(ref, dict): ref = rational(ref)
        elif ref.get('schema') != 'SLC_FORMAL_LOG_ELEMENT_V1': raise ValueError('Unknown logarithmic report reference')
        return canonical({'kind': kind, 'reference': ref})
    if set(raw) != {'kind', 'boundaries', 'closed'} or raw['closed'] not in ('LEFT', 'RIGHT'):
        raise ValueError('BINS needs increasing exact boundaries and LEFT/RIGHT endpoint inclusion')
    if not isinstance(raw['boundaries'], (list, tuple)) or not raw['boundaries']:
        raise ValueError('BINS requires at least one exact boundary')
    cuts = [rational(v) for v in raw['boundaries']]
    if any(a >= b for a,b in zip(cuts,cuts[1:])):
        raise ValueError('Bin boundaries must be strictly increasing')
    return canonical({'kind':kind,'boundaries':cuts,'closed':raw['closed']})


def _log(raw, cls):
    from .observation_motion import _exact_log
    value = _exact_log(raw, cls)
    return cls.from_terms([(r['prime'], Fraction(r['coefficient']['numerator'],r['coefficient']['denominator'])) for r in value['coefficients']])


def _compare(value, reference, cls):
    if isinstance(value, dict) and value.get('schema') == 'SLC_FORMAL_LOG_ELEMENT_V1':
        if isinstance(reference,dict): other = _log(reference,cls)
        elif rational(reference) == 0: other = cls.zero()
        else: raise ValueError('Log report reference must be an exact formal log or zero')
        return _log(value,cls).compare(other)
    a,b = rational(value),rational(reference)
    return (a>b)-(a<b)


def _scalar(observation):
    value = observation.get('value') if isinstance(observation,dict) and observation.get('schema') == 'GEN2_TYPED_MOTION_OBSERVATION_V1' else observation
    if isinstance(value,(list,tuple)):
        if len(value) != 1: raise ValueError('Coarse scalar report cannot silently project a vector or history')
        value=value[0]
    return value


def report_value(observation, report, cls):
    report=normalize_report(report)
    if report['kind']=='EXACT': return canonical(observation)
    value=_scalar(observation)
    if report['kind']=='ABOVE_SAME_BELOW':
        comparison=_compare(value,report['reference'],cls)
        return 'ABOVE' if comparison>0 else 'BELOW' if comparison<0 else 'SAME'
    return sum(_compare(value,boundary,cls)>=0 if report['closed']=='LEFT' else _compare(value,boundary,cls)>0 for boundary in report['boundaries'])


def channel(choice):
    if 'readout' in choice: return {'readout':choice['readout']}
    return {key:choice[key] for key in ('mode','view','components','projection')}


def wrap(value, choice):
    return canonical({'schema':SCHEMA,'channel':channel(choice),'report':choice['report'],'value':value})


def predict(observation, choice, cls):
    return wrap(report_value(observation,choice['report'],cls),choice)


def supplied(raw, choice, cls):
    report=choice['report']
    if isinstance(raw,dict) and raw.get('schema')==SCHEMA:
        if set(raw)!={'schema','channel','report','value'} or raw['channel']!=channel(choice) or raw['report']!=report:
            raise ValueError('Supplied report belongs to another source channel or resolution')
        raw=raw['value']
    kind=report['kind']
    if kind=='ABOVE_SAME_BELOW':
        if raw not in ('ABOVE','SAME','BELOW'): raise ValueError('Supply the actual ABOVE/SAME/BELOW report')
    elif kind=='BINS':
        if type(raw) is not int or not 0<=raw<=len(report['boundaries']): raise ValueError('Observed bin index is outside its complete report alphabet')
    else:
        # EXACT report values still undergo the native/typed validation in observation._condition.
        return wrap(raw,choice)
    return wrap(raw,choice)


def source_reports(block, readouts, whitelist=None):
    """EXACT plus registered source normalization comparisons or explicit bins."""
    from .observation_motion import descriptor
    from .observation_motion import profile as source_profile
    profile=source_profile(block)
    result=[]
    for readout in readouts:
        reports=[dict(EXACT)]
        if readout['scope']=='ENDPOINT' and readout['kind'] in ('SCALE','LOG_SCALE'):
            reports.append(normalize_report({'kind':'ABOVE_SAME_BELOW','reference':1 if readout['kind']=='SCALE' else 0}))
        for report in reports: result.append({'readout':readout,'report':report})
    for row in ([] if profile is None else profile.get('observation_reports',[])):
        if not isinstance(row,dict) or set(row)!={'readout','reports'} or not isinstance(row['reports'],list):
            raise ValueError('Source observation_reports requires readout and a complete report-rule list')
        readout=descriptor(row['readout'],block)
        if readout not in readouts: continue
        for raw in row['reports']:
            report=normalize_report(raw)
            if report['kind']!='EXACT' and (readout['scope']!='ENDPOINT' or readout['kind']=='SPHERE'):
                raise ValueError('Source coarse report requires an endpoint scalar channel')
            item={'readout':readout,'report':report}
            if item not in result:result.append(item)
    if whitelist is None:return canonical(result)
    if not isinstance(whitelist,(list,tuple)): raise ValueError('available_reports must restrict the declared source resolution roster')
    out=[]
    for row in whitelist:
        if not isinstance(row,dict) or set(row)!={'readout','report'}:raise ValueError('Report whitelist entry requires readout and report')
        item={'readout':descriptor(row['readout'],block),'report':normalize_report(row['report'])}
        if item not in result or item in out: raise ValueError('Unknown or repeated source report resolution')
        out.append(item)
    return canonical(out)


def allowed(choice, declared):
    if 'readout' not in choice:
        return 'report' not in choice or choice['report']==EXACT
    return {'readout':choice['readout'],'report':choice.get('report',EXACT)} in declared


def automatic_choices(base, declared):
    result=[]
    for choice in base:
        if allowed(choice,declared):result.append(choice)
        if 'readout' in choice:
            for entry in declared:
                if entry['readout']==choice['readout'] and entry['report']!=EXACT:
                    result.append({**choice,'label':choice['label']+':REPORT:'+str(len(result)), 'report':entry['report']})
    return result


def quantity_descriptor(block, choice):
    """Channel meaning metadata, kept outside the predictive report value."""
    from .quantities import normalize_descriptor, source_quantity
    if 'readout' in choice:
        readout = choice['readout']
        role = readout.get('role', readout.get('roles'))
        reference = {'kind': 'MEMBER_ORIGINAL_INITIAL_STATE'} if readout['kind'] in ('SCALE', 'LOG_SCALE', 'SPHERE') else None
        if readout['kind'] != 'SPHERE':
            return source_quantity(block, readout['kind'], role=role, reference_state=reference, scope=readout['scope'])
        return normalize_descriptor({'kind': 'UNIT_SPHERE_POINT', 'units': {}, 'scope': readout['scope'],
            'source': block.contract_id, 'role': role, 'frame': {'kind': 'FIXED_UNIT_SPHERE'},
            'normalization': {'kind': 'INITIAL_ACTION_STEREOGRAPHIC', 'source_account': block.contract_id, 'role': role},
            'reference_state': reference})
    return normalize_descriptor({'kind': 'NATIVE_RECEIVER_SIGN' if choice['projection'] == 'SIGN' else 'NATIVE_RECEIVER_VALUE',
        'units': {} if choice['projection'] == 'SIGN' else {block.contract.units: 1},
        'source': block.contract_id, 'component': choice['components'],
        'scope': 'EDGE' if choice['mode'] == 'DELTA' else 'ENDPOINT',
        'frame': {'view': choice['view'], 'mode': choice['mode']}})
