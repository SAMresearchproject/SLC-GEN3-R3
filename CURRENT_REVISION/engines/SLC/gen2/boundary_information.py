"""Registered construction boundaries on complete source-bound history relations.

The original source roster and its statistical measure remain separate from
construction amounts. Reports condition linked records, never Cartesian
marginals. Native histories are validated/reused through compiled transitions;
append evaluates only the new endpoint and keeps original history identities.
"""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from inspect import getsourcefile
from itertools import product
from pathlib import Path

from .exact import canonical, canonical_bytes, digest, rational
from .exact_observation_information import score_observation
from .linked_relation import weights_for, restrict_weights, probabilities


SCHEMA = 'GEN2_BOUNDARY_CHECKPOINT_V1'
OPERATIONS = ('GEN2_BOUNDARY_OPEN', 'GEN2_BOUNDARY_INFORMATION',
              'GEN2_BOUNDARY_CONDITION', 'GEN2_BOUNDARY_APPEND', 'GEN2_BOUNDARY_RESUME')
_VERIFIED = {}
_ROWS = {}
_INFORMATION = {}
_STATS = {'source_relation_builds': 0, 'source_relation_cache_hits': 0,
          'semantic_checkpoint_rebuilds': 0, 'validated_checkpoint_cache_hits': 0,
          'partition_builds': 0, 'partition_cache_hits': 0,
          'conditioned_without_source_reexecution': 0, 'appended_transition_lookups': 0,
          'prior_native_transitions_reexecuted': 0}


def reuse_stats(reset=False):
    result = {**_STATS, 'source_relation_cache_entries': len(_ROWS),
              'validated_checkpoint_cache_entries': len(_VERIFIED), 'partition_cache_entries': len(_INFORMATION)}
    if reset:
        for key in _STATS:
            _STATS[key] = 0
    return result


def _remember(cache, key, value):
    if key not in cache and len(cache) >= 128:
        cache.pop(next(iter(cache)))
    cache[key] = value


def _fields(raw, allowed, required=()):
    if not isinstance(raw, dict) or set(raw) - set(allowed) or set(required) - set(raw):
        raise ValueError('Missing or undeclared boundary fields')


def _binding(log_class):
    from .quantities import bind_formal_log
    base = Path(__file__).resolve().parent
    names = ('boundary_information.py', 'linked_relation.py', 'quantities.py',
             'construction.py', 'readouts.py', 'encounters.py', 'exact_observation_information.py',
             'contracts.py', 'compiler.py', 'native.py', 'exact.py',
             'dependencies/native/t18.py', 'dependencies/native/exact.py', 'dependencies/native/quadratic.py',
             'dependencies/common_reception.py', 'dependencies/J4_RESPONSES.jsonl',
             'dependencies/LI6_GEOMETRY.json', 'dependencies/LI6_SELECTION_DERIVATION.json',
             'dependencies/LI6_TMR1.i64le')
    return {**{name: sha256((base / name).read_bytes()).hexdigest() for name in names},
            'formal_log_source': bind_formal_log(log_class)}


def _native_history(block, raw):
    _fields(raw, {'initial', 'program', 'states'}, ('initial', 'program'))
    initial = block.contract.admit_state(raw['initial'])
    if initial not in block.state_set or not isinstance(raw['program'], (list, tuple)):
        raise ValueError('History needs an admitted initial state and explicit ordered native program')
    states = [list(initial)]
    for label in raw['program']:
        matches = [row for row in block.outgoing.get(tuple(states[-1]), ()) if row[1] == label]
        if len(matches) != 1:
            raise ValueError('Source history contains an inadmissible native transition')
        states.append(list(matches[0][2]))
    if 'states' in raw and canonical(raw['states']) != states:
        raise ValueError('Supplied native history loses its source/event/state association')
    return {'initial': list(initial), 'program': list(raw['program']), 'states': states}


def _native_variables(block, native, original=None):
    original = native if original is None else original
    state = tuple(native['states'][-1])
    values = {'INTERIOR_HISTORY': original, 'CURRENT_HISTORY': native,
              'INTERIOR_STATE': list(state), 'SOURCE_ACTION': block.contacts[state]}
    signed = block.frames[state]['SIGNED_PHASE']
    occupancy = block.frames[state]['AXIS_OCCUPANCY']
    offset = 0
    ports = []
    for receiver in block.contract.receivers:
        width = len(receiver.matrix)
        values['COMPONENT:' + receiver.name + ':STATE'] = [state[block.contract.coordinates.index(c)] for c in receiver.coordinates]
        values['EXTERIOR:' + receiver.name + ':SIGNED'] = signed[offset:offset + width]
        values['EXTERIOR:' + receiver.name + ':OCCUPANCY'] = occupancy[offset:offset + width]
        ports.append(signed[offset:offset + width])
        offset += width
    if len(ports) > 1 and len({len(port) for port in ports}) == 1:
        values['EXTERIOR:SUM_SIGNED'] = [sum(lane) for lane in zip(*ports, strict=True)]
    return canonical(values)


def _row(source, original, current, values, associations=None):
    return canonical({'record_id': digest({'source': source, 'original': original}),
                      'original': original, 'current': current, 'variables': values,
                      'associations': {} if associations is None else associations})


def _construction_values(compiled, alternative):
    response = compiled.evaluate(alternative['values'])
    values = {'INTERIOR_CONFIGURATION': alternative,
              'SOURCE_INVENTORY': compiled.source_account_totals}
    values.update({'EXTERIOR:' + account: value for account, value in response['values'].items()})
    for instance in response['instances']:
        for account, value in instance['values'].items():
            values['COMPONENT:' + instance['instance_id'] + ':' + instance['action_id'] + ':' + account] = value
    return canonical(values)


def _source(raw, runtime):
    if not isinstance(raw, dict):
        raise ValueError('Boundary source must be a registered construction declaration')
    kind = raw.get('kind')
    if kind == 'NATIVE':
        _fields(raw, {'kind', 'contract', 'histories'}, ('kind', 'histories'))
        block = runtime.compile(raw.get('contract'))
        if not isinstance(raw['histories'], list) or not raw['histories']:
            raise ValueError('Declare the complete nonempty finite native history roster')
        return {'kind': kind, 'contract': block.contract.to_dict(),
                'histories': [_native_history(block, history) for history in raw['histories']]}
    if kind == 'NATIVE_JOIN':
        _fields(raw, {'kind', 'components', 'joins', 'composition'}, ('kind', 'components', 'joins'))
        if 'composition' in raw and raw['composition'] != 'EXPLICIT_COMPATIBILITY_JOIN_WITH_ONE_ASSEMBLY_MEASURE':
            raise ValueError('Unknown source assembly composition law')
        if not isinstance(raw['components'], list) or len(raw['components']) < 2 or not isinstance(raw['joins'], list):
            raise ValueError('Declare component rosters and every shared coordinate/clock join')
        components = []
        for component in raw['components']:
            _fields(component, {'component_id', 'source', 'ticks', 'clock_id', 'clock_unit'},
                    ('component_id', 'source', 'ticks', 'clock_id', 'clock_unit'))
            if any(type(component[name]) is not str or not component[name] for name in ('component_id', 'clock_id', 'clock_unit')):
                raise ValueError('Source component and clock identities must be explicit')
            source = _source(component['source'], runtime)
            if source['kind'] != 'NATIVE':
                raise ValueError('Native joins accept native component history rosters')
            ticks = component['ticks']
            if not isinstance(ticks, list) or any(type(tick) is not int for tick in ticks) or ticks != sorted(set(ticks)):
                raise ValueError('Component history ticks must be strictly increasing exact integers')
            if any(len(history['states']) != len(ticks) for history in source['histories']):
                raise ValueError('Every component state requires its declared source clock tick')
            components.append({**component, 'source': source})
        lookup = {c['component_id']: c for c in components}
        if len(lookup) != len(components):
            raise ValueError('Assembly component identities must be distinct')
        joins = []
        for join in raw['joins']:
            _fields(join, {'left', 'right'}, ('left', 'right'))
            for key in ('left', 'right'):
                endpoint = join[key]
                if not isinstance(endpoint, list) or len(endpoint) != 2 or endpoint[0] not in lookup:
                    raise ValueError('A source join endpoint names component and native coordinate')
                if type(endpoint[1]) is not int or endpoint[1] not in lookup[endpoint[0]]['source']['contract']['coordinates']:
                    raise ValueError('Shared boundary coordinate is not declared by its component')
            left, right = lookup[join['left'][0]], lookup[join['right'][0]]
            if left is right or (left['clock_id'], left['clock_unit'], left['ticks']) != (right['clock_id'], right['clock_unit'], right['ticks']):
                raise ValueError('A shared coordinate requires one declared aligned source clock and full common tick roster')
            joins.append(join)
        return canonical({'kind': kind, 'components': components, 'joins': joins,
                          'composition': 'EXPLICIT_COMPATIBILITY_JOIN_WITH_ONE_ASSEMBLY_MEASURE'})
    if kind == 'CONSTRUCTION':
        _fields(raw, {'kind', 'source', 'alternatives'}, ('kind', 'source', 'alternatives'))
        from .construction import ConstructionSpec
        spec = ConstructionSpec.from_dict(raw['source'])
        alternatives = []
        for row in raw['alternatives']:
            _fields(row, {'values', 'context'}, ('values',))
            alternative = {'values': [rational(v) for v in row['values']], 'context': row.get('context', {})}
            spec.compile(alternative['context']).evaluate(alternative['values'])
            alternatives.append(canonical(alternative))
        if not alternatives:
            raise ValueError('Declare the finite construction alternatives')
        return {'kind': kind, 'source': spec.to_dict(), 'alternatives': alternatives}
    if kind == 'LI6':
        _fields(raw, {'kind', 'alternatives'}, ('kind', 'alternatives'))
        from .construction import li6_edge_vectors
        allowed = {'state', 'phases', 'cover', 'assignment', 'rho', 'mask', 'hidden_loop', 'receiver'}
        alternatives = []
        for row in raw['alternatives']:
            _fields(row, allowed)
            if ('state' in row) == ('phases' in row):
                raise ValueError('Li6 alternative requires exactly one native state or phase vector')
            li6_edge_vectors(row.get('state'), phases=row.get('phases'))
            alternatives.append(canonical(row))
        if not alternatives:
            raise ValueError('Declare the finite Li6 alternatives')
        return {'kind': kind, 'alternatives': alternatives}
    if kind == 'ENCOUNTER':
        _fields(raw, {'kind', 'source', 'alternatives'}, ('kind', 'source', 'alternatives'))
        from .encounters import EncounterTransfer
        transfer = EncounterTransfer.from_dict(raw['source'])
        alternatives = []
        for row in raw['alternatives']:
            _fields(row, {'emissions'}, ('emissions',))
            transfer.source_vector(row['emissions'])
            alternatives.append(canonical(row))
        if not alternatives:
            raise ValueError('Declare complete finite source emission histories')
        return {'kind': kind, 'source': transfer.to_dict(), 'alternatives': alternatives}
    raise ValueError('Unregistered assembly source kind')


def _build(source, runtime):
    rows = []
    source_id = digest(source)
    if source['kind'] == 'NATIVE':
        block = runtime.compile(source['contract'])
        rows = [_row(source_id, native, native, _native_variables(block, native)) for native in source['histories']]
    elif source['kind'] == 'NATIVE_JOIN':
        components = source['components']
        blocks = {c['component_id']: runtime.compile(c['source']['contract']) for c in components}
        for combination in product(*(c['source']['histories'] for c in components)):
            histories = dict(zip((c['component_id'] for c in components), combination, strict=True))
            compatible = True
            for join in source['joins']:
                a, x = join['left']; b, y = join['right']
                i = blocks[a].contract.coordinates.index(x); j = blocks[b].contract.coordinates.index(y)
                if any(left[i] != right[j] for left, right in zip(histories[a]['states'], histories[b]['states'], strict=True)):
                    compatible = False
                    break
            if not compatible:
                continue
            variables = {'INTERIOR_HISTORY': histories}
            for name, history in histories.items():
                for variable, value in _native_variables(blocks[name], history).items():
                    variables[name + '/' + variable] = value
            rows.append(_row(source_id, histories, histories, variables,
                             {'shared_coordinates': source['joins'], 'clocks': [
                                 {k: c[k] for k in ('component_id', 'clock_id', 'clock_unit', 'ticks')} for c in components]}))
    elif source['kind'] == 'CONSTRUCTION':
        from .construction import ConstructionSpec
        spec = ConstructionSpec.from_dict(source['source'])
        compiled = {}
        for alternative in source['alternatives']:
            key = canonical_bytes(alternative['context'])
            if key not in compiled:
                compiled[key] = spec.compile(alternative['context'])
            rows.append(_row(source_id, alternative, alternative, _construction_values(compiled[key], alternative)))
    elif source['kind'] == 'LI6':
        from .construction import li6_construction, li6_edge_vectors, site_cycle_forward, li6_geometry
        compiled = {}
        for alternative in source['alternatives']:
            settings = {k: v for k, v in alternative.items() if k not in ('state', 'phases')}
            key = canonical_bytes(settings)
            if key not in compiled:
                compiled[key] = li6_construction(**settings).compile()
            real, imaginary = li6_edge_vectors(alternative.get('state'), phases=alternative.get('phases'))
            values = _construction_values(compiled[key], {'values': list(real + imaginary), 'context': settings})
            values['INTERIOR_CONFIGURATION'] = alternative
            mask = li6_geometry()['masks'][settings.get('mask', 3)]
            fields = [site_cycle_forward([v * flag for v, flag in zip(part, mask, strict=True)]) for part in (real, imaginary)]
            values['EXTERIOR:SITES'] = [part['sites'] for part in fields]
            values['EXTERIOR:CYCLES'] = [part['cycles'] for part in fields]
            rows.append(_row(source_id, alternative, alternative, values))
    else:
        from .encounters import EncounterTransfer
        transfer = EncounterTransfer.from_dict(source['source'])
        for alternative in source['alternatives']:
            result = transfer.forward(alternative['emissions'])
            values = {'INTERIOR_HISTORY': alternative['emissions']}
            values.update({'COMPONENT:' + name: values for name, values in alternative['emissions'].items()})
            values.update({'EXTERIOR:' + name: values for name, values in result['observations'].items()})
            rows.append(_row(source_id, alternative, alternative, values,
                             {'transfer_sha256': result['transfer_sha256'], 'maintained_state_transition': 'NONE'}))
    return canonical(rows)


def _descriptor(name, source):
    from .quantities import normalize_descriptor
    exterior = name.startswith('EXTERIOR:') or '/EXTERIOR:' in name
    local_name = name.split('/', 1)[-1]
    kind = ('SOURCE_HISTORY' if 'HISTORY' in name else 'SOURCE_ACCOUNT_INVENTORY' if local_name == 'SOURCE_INVENTORY'
            else 'SOURCE_CONFIGURATION' if 'CONFIGURATION' in name or name.endswith(':STATE') or local_name == 'INTERIOR_STATE'
            else 'EXACT_REGISTERED_READOUT')
    numerical = kind == 'EXACT_REGISTERED_READOUT'
    unit = None
    if numerical and source['kind'] in ('NATIVE', 'NATIVE_JOIN'):
        contract = (source['contract'] if source['kind'] == 'NATIVE' else next(
            c['source']['contract'] for c in source['components'] if c['component_id'] == name.split('/', 1)[0]))
        unit = 'native_source_action' if local_name == 'SOURCE_ACTION' else contract['units']
    elif numerical and source['kind'] == 'CONSTRUCTION':
        unit = source['source']['output_units'].get(name.split(':')[-1])
    elif numerical and source['kind'] == 'LI6':
        unit = 'native_edge_current' if name in ('EXTERIOR:SITES', 'EXTERIOR:CYCLES') else 'CANDIDATE_SOURCE_ACTION'
    elif numerical and source['kind'] == 'ENCOUNTER':
        unit = source['source']['source_unit']
    units = {} if unit is None else {unit: 1}
    if source['kind'] == 'ENCOUNTER' and exterior and source['source']['coefficient_unit'] != 'DIMENSIONLESS':
        units[source['source']['coefficient_unit']] = units.get(source['source']['coefficient_unit'], 0) + 1
    return {'variable': name, 'visibility': 'EXTERIOR' if exterior else 'INTERIOR',
            'quantity': normalize_descriptor({'kind': kind, 'source': digest(source),
                'component': name.split(':')[1] if ':' in name else None,
                'role': 'EXTERIOR_CHANNEL' if exterior else 'ASSEMBLY_INTERIOR',
                'units': units, 'normalization': None,
                'scope': 'HISTORY' if 'HISTORY' in name else 'ENDPOINT',
                'sign_convention': 'SIGNED_VALUE'})}


def _catalog(source, rows):
    names = sorted(set().union(*(row['variables'] for row in rows))) if rows else []
    return {name: _descriptor(name, source) for name in names}


def _seal(body):
    body = canonical(body)
    return {'body': body, 'sha256': digest(body)}


def _condition(body, reports):
    if not isinstance(reports, dict) or not reports:
        raise ValueError('Supply one or more observed exterior channel values')
    for variable in reports:
        if variable not in body['variables'] or body['variables'][variable]['visibility'] != 'EXTERIOR':
            raise ValueError('Conditioning requires a registered exterior observation channel')
    def exact_value(value):
        if isinstance(value, (list, tuple)):
            return [exact_value(v) for v in value]
        if isinstance(value, dict):
            return {k: exact_value(v) for k, v in value.items()}
        return canonical(rational(value))
    reports = {name: exact_value(value) for name, value in reports.items()}
    kept = []
    for row in body['rows']:
        if any(name not in row['variables'] or row['variables'][name] is None for name in reports):
            raise ValueError('Selected exterior reading is undefined on a retained source history')
        if all(exact_value(row['variables'][name]) == value for name, value in reports.items()):
            kept.append(row)
    body['rows'] = kept
    body['weights'] = restrict_weights(body['weights'], kept)
    body['journal'].append({'operation': 'CONDITION', 'reports': reports})
    _STATS['conditioned_without_source_reexecution'] += 1


def _append(body, event, runtime):
    if body['source']['kind'] == 'NATIVE_JOIN':
        return _append_join(body, event, runtime)
    if body['source']['kind'] != 'NATIVE' or type(event) is not str:
        raise ValueError('Native append requires one declared event on a native assembly relation')
    block = runtime.compile(body['source']['contract'])
    replacements = []
    for row in body['rows']:
        native = deepcopy(row['current'])
        admitted = [edge for edge in block.outgoing.get(tuple(native['states'][-1]), ()) if edge[1] == event]
        if len(admitted) != 1:
            raise ValueError('Append event must be admitted for every retained history')
        native['program'].append(event)
        native['states'].append(list(admitted[0][2]))
        replacements.append({**row, 'current': native,
                             'variables': _native_variables(block, native, row['original'])})
    body['rows'] = canonical(replacements)
    body['journal'].append({'operation': 'APPEND', 'event': event})
    _STATS['appended_transition_lookups'] += len(replacements)


def _append_join(body, event, runtime):
    _fields(event, {'events', 'tick'}, ('events', 'tick'))
    components = body['source']['components']
    names = {component['component_id'] for component in components}
    if not isinstance(event['events'], dict) or set(event['events']) != names or type(event['tick']) is not int:
        raise ValueError('Joined append requires one declared native event per component and a new exact clock tick')
    blocks = {component['component_id']: runtime.compile(component['source']['contract']) for component in components}
    replacements = []
    for row in body['rows']:
        histories = deepcopy(row['current'])
        clocks = deepcopy(row['associations']['clocks'])
        for clock in clocks:
            if event['tick'] <= clock['ticks'][-1]:
                raise ValueError('Joined append clock must advance every declared component clock')
            clock['ticks'].append(event['tick'])
        for name, history in histories.items():
            label = event['events'][name]
            edges = [edge for edge in blocks[name].outgoing.get(tuple(history['states'][-1]), ()) if edge[1] == label]
            if len(edges) != 1:
                raise ValueError('Joined append event is not admitted on every retained component history')
            history['program'].append(label)
            history['states'].append(list(edges[0][2]))
        for join in body['source']['joins']:
            a, x = join['left']; b, y = join['right']
            if histories[a]['states'][-1][blocks[a].contract.coordinates.index(x)] != histories[b]['states'][-1][blocks[b].contract.coordinates.index(y)]:
                raise ValueError('Appended component events disagree on their shared boundary coordinate')
        variables = {'INTERIOR_HISTORY': row['original']}
        for name, history in histories.items():
            for variable, value in _native_variables(blocks[name], history, row['original'][name]).items():
                variables[name + '/' + variable] = value
        replacements.append({**row, 'current': histories, 'variables': variables,
                             'associations': {**row['associations'], 'clocks': clocks}})
    body['rows'] = canonical(replacements)
    body['journal'].append({'operation': 'APPEND', 'event': event})
    _STATS['appended_transition_lookups'] += len(replacements) * len(components)


def _opened(source, measure, runtime, log_class):
    binding = _binding(log_class)
    key = canonical_bytes({'source': source, 'binding': binding})
    reused = key in _ROWS
    if not reused:
        _remember(_ROWS, key, _build(source, runtime))
        _STATS['source_relation_builds'] += 1
    else:
        _STATS['source_relation_cache_hits'] += 1
    rows = deepcopy(_ROWS[key])
    weights = weights_for(rows, measure)
    body = {'schema': SCHEMA, 'complete': True, 'source': source,
            'source_sha256': digest(source), 'implementation_binding': binding,
            'measure': measure, 'original_rows': rows, 'original_weights': weights,
            'rows': deepcopy(rows), 'weights': deepcopy(weights), 'variables': _catalog(source, rows),
            'journal': []}
    return body, reused


def _session(checkpoint, runtime, log_class):
    _fields(checkpoint, {'body', 'sha256'}, ('body', 'sha256'))
    body = checkpoint['body']
    if digest(body) != checkpoint['sha256'] or body.get('schema') != SCHEMA or body.get('complete') is not True:
        raise ValueError('Boundary checkpoint seal/schema/completeness differs')
    if body.get('implementation_binding') != _binding(log_class):
        raise ValueError('Boundary source, quantity, information or implementation binding differs')
    key = canonical_bytes(checkpoint)
    if key in _VERIFIED:
        _STATS['validated_checkpoint_cache_hits'] += 1
        return deepcopy(_VERIFIED[key]), True
    _STATS['semantic_checkpoint_rebuilds'] += 1
    source = _source(body['source'], runtime) if body['source']['kind'] != 'NATIVE_JOIN' else _source(
        {k: v for k, v in body['source'].items() if k != 'composition'}, runtime)
    rebuilt, _ = _opened(source, body['measure'], runtime, log_class)
    for event in body['journal']:
        if event.get('operation') == 'CONDITION':
            _fields(event, {'operation', 'reports'}, ('operation', 'reports'))
            _condition(rebuilt, event['reports'])
        elif event.get('operation') == 'APPEND':
            _fields(event, {'operation', 'event'}, ('operation', 'event'))
            _append(rebuilt, event['event'], runtime)
        else:
            raise ValueError('Unknown boundary checkpoint journal entry')
    if canonical(rebuilt) != body:
        raise ValueError('Boundary checkpoint loses source alternatives, measure or observation associations')
    _remember(_VERIFIED, key, deepcopy(rebuilt))
    return rebuilt, False


def _result(body, *, cache_reused=False):
    return {'schema': 'GEN2_BOUNDARY_RELATION_V1', 'complete': True,
            'status': 'EMPTY' if not body['rows'] else 'UNIQUE' if len(body['rows']) == 1 else 'MULTIPLE',
            'candidate_count': len(body['rows']), 'original_candidate_count': len(body['original_rows']),
            'members': deepcopy(body['rows']), 'weights': deepcopy(body['weights']),
            'probabilities': probabilities(body['weights']), 'variables': deepcopy(body['variables']),
            'source_account_amounts_used_as_weights': False,
            'checkpoint': _seal(body)}


def _variables(body, names):
    if not isinstance(names, list) or len(set(names)) != len(names) or any(name not in body['variables'] for name in names):
        raise ValueError('Information variables must be distinct registered names')
    if any(name not in row['variables'] or row['variables'][name] is None for row in body['rows'] for name in names):
        raise ValueError('Information variable is undefined on a retained assembly alternative')
    return names


def _information(body, left, right, given, log_class):
    left, right, given = (_variables(body, names) for names in (left, right, given))
    if not left or not right:
        raise ValueError('Declare nonempty left and right variable tuples')
    if not body['rows']:
        return {'schema': 'GEN2_BOUNDARY_INFORMATION_V1', 'status': 'EMPTY', 'candidate_count': 0}
    key = canonical_bytes({'rows': body['rows'], 'weights': body['weights'], 'left': left, 'right': right, 'given': given,
                           'binding': body['implementation_binding'], 'variables': body['variables']})
    if key in _INFORMATION:
        _STATS['partition_cache_hits'] += 1
        return deepcopy(_INFORMATION[key])
    _STATS['partition_builds'] += 1
    def value(row, name):
        raw = row['variables'][name]
        if body['variables'][name]['quantity']['kind'] != 'EXACT_REGISTERED_READOUT':
            return raw
        def exact(raw):
            if isinstance(raw, (tuple, list)):
                return [exact(item) for item in raw]
            if isinstance(raw, dict):
                return {key: exact(item) for key, item in raw.items()}
            return rational(raw)
        return exact(raw)
    def score(a, b):
        return score_observation([{'record_id': row['record_id'],
            'target': [value(row, name) for name in a],
            'observation': [value(row, name) for name in b]} for row in body['rows']],
            formal_log_cls=log_class, weights={k: rational(v) for k, v in body['weights'].items()})
    xy, yx = score(left, right), score(right, left)
    joint = score(left + right, []).target_entropy
    baseline = score(left, given)
    combined = score(left, given + [name for name in right if name not in given])
    gain = baseline.conditional_target_entropy - combined.conditional_target_entropy
    result = {'schema': 'GEN2_BOUNDARY_INFORMATION_V1', 'status': 'AVAILABLE',
              'log_unit': 'nats', 'candidate_count': len(body['rows']),
              'left': left, 'right': right, 'given': given,
              'H_left': xy.target_entropy.to_dict(), 'H_right': yx.target_entropy.to_dict(),
              'H_joint': joint.to_dict(), 'H_left_given_right': xy.conditional_target_entropy.to_dict(),
              'mutual_information': xy.mutual_information.to_dict(),
              'H_left_given_baseline': baseline.conditional_target_entropy.to_dict(),
              'H_left_given_baseline_and_right': combined.conditional_target_entropy.to_dict(),
              'conditional_information_gain': gain.to_dict(),
              'linked_partitions': xy.to_dict()}
    _remember(_INFORMATION, key, deepcopy(result))
    return result


def dispatch(operation, payload, runtime):
    log_class = runtime.exact_information().hd_module.FormalLogElement
    if operation == 'GEN2_BOUNDARY_OPEN':
        _fields(payload, {'source', 'measure'}, ('source', 'measure'))
        source = _source(payload['source'], runtime)
        body, reused = _opened(source, payload['measure'], runtime, log_class)
        checkpoint = _seal(body)
        _remember(_VERIFIED, canonical_bytes(checkpoint), deepcopy(body))
        return _result(body, cache_reused=reused)
    required = {'GEN2_BOUNDARY_INFORMATION': ('checkpoint', 'left', 'right'),
                'GEN2_BOUNDARY_CONDITION': ('checkpoint', 'reports'),
                'GEN2_BOUNDARY_APPEND': ('checkpoint', 'event'),
                'GEN2_BOUNDARY_RESUME': ('checkpoint',)}
    if operation not in required:
        raise ValueError('Unknown boundary operation')
    allowed = set(required[operation]) | ({'given'} if operation == 'GEN2_BOUNDARY_INFORMATION' else set())
    _fields(payload, allowed, required[operation])
    body, reused = _session(payload['checkpoint'], runtime, log_class)
    if operation == 'GEN2_BOUNDARY_INFORMATION':
        return _information(body, payload['left'], payload['right'], payload.get('given', []), log_class)
    if operation == 'GEN2_BOUNDARY_CONDITION':
        _condition(body, payload['reports'])
    elif operation == 'GEN2_BOUNDARY_APPEND':
        _append(body, payload['event'], runtime)
    _remember(_VERIFIED, canonical_bytes(_seal(body)), deepcopy(body))
    return _result(body, cache_reused=reused)


def register_ordinary(operation, payload, result):
    """Expose boundary meanings on ordinary calls without inventing a prior."""
    result = dict(result)
    if 'CONSTRUCTION' in operation:
        source = result.get('source', payload.get('source', {}))
        instances = source.get('instances', [])
        outputs = source.get('output_units', result.get('output_units', {}))
        registration = {'kind': 'TYPED_CONSTRUCTION',
            'interior_instances': [{'instance_id': row['instance_id'], 'kind': row['kind'],
                'accounts': [account['name'] for account in row.get('accounts', [])],
                'actions': [action.get('action_id', 'response') for action in row.get('actions', [])]}
                for row in instances], 'exterior_accounts': outputs}
    elif 'SITE_CYCLE' in operation:
        registration = {'kind': 'LI6_SITE_CYCLE', 'interior': 'MASKED_NATIVE_EDGE_CURRENTS',
                        'exterior': ['sites', 'cycles']}
    elif 'ENCOUNTER' in operation:
        registration = {'kind': 'SOURCE_ENCOUNTER', 'interior': 'DECLARED_SOURCE_PORT_EMISSION_HISTORIES',
                        'exterior': 'DECLARED_RECEIVER_PORT_AND_OBSERVATION_TICK_FRAMES',
                        'transfer_sha256': result.get('transfer_sha256')}
    else:
        registration = {'kind': 'REGISTERED_READOUT', 'interior': 'DECLARED_SOURCE_OPERANDS',
                        'exterior': payload.get('strategy', 'polynomial')}
    result['boundary'] = {'schema': 'GEN2_REGISTERED_BOUNDARY_V1', 'automatic': True,
                          'registration': registration,
                          'information_status': 'COMPLETE_RELATION_AND_MEASURE_REQUIRED',
                          'source_amounts_are_probability_weights': False,
                          'relation_entrypoint': 'GEN2_BOUNDARY_OPEN'}
    if 'exterior_accounts' in registration:
        from .quantities import normalize_descriptor
        result['boundary']['quantity_descriptors'] = {
            name: normalize_descriptor({'kind': 'CONSTRUCTION_RESPONSE', 'units': {unit: 1},
                'source': result.get('source_sha256', digest(source)), 'role': 'EXTERIOR_ACCOUNT',
                'component': name, 'scope': 'ENDPOINT', 'sign_convention': 'SIGNED_VALUE'})
            for name, unit in registration['exterior_accounts'].items()}
    return result
