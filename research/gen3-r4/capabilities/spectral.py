"""R4 source-bound certified readouts. Arithmetic belongs to the native worker."""
from copy import deepcopy
from CURRENT_REVISION.engines.SLC.gen2.exact import canonical_bytes, digest

SPECTRAL_OPERATIONS = (
    'GEN3_SPECTRAL_ADMIT', 'GEN3_LOG1P_ENCLOSURE', 'GEN3_SPECTRAL_LOG_PROFILE',
    'GEN3_SPECTRAL_REFINE', 'GEN3_SIGNED_TRANSPORT_LOG', 'GEN3_SPECTRAL_EXPORT')


def bounded(value, lo, hi, name):
    if type(value) is not int or not lo <= value <= hi:
        raise ValueError(f'{name} must be an integer in {lo}..{hi}')
    return value


class SpectralCapabilities:
    def spectral_record(self, name, source):
        if not isinstance(name, str) or not name or len(name) > 128:
            raise ValueError('Record name must contain 1..128 characters')
        key = 'capability:spectral:' + name
        if key not in self.machine.origins:
            raise ValueError('Unknown retained spectral record')
        row = self.machine.origins[key]
        if canonical_bytes(source) != canonical_bytes(row['source_binding']):
            raise ValueError('Spectral source binding differs')
        return row

    def spectral_dependencies(self, record, source):
        root = record if record['kind'] == 'source' else self.spectral_record(record['source_record'], source)
        if root['kind'] != 'source':
            raise ValueError('Invalid spectral source dependency')
        state = record
        seen = set()
        while 'spectral_state' not in state:
            if state['name'] in seen or 'spectral_parent' not in state:
                raise ValueError('Invalid spectral-state dependency')
            seen.add(state['name'])
            state = self.spectral_record(state['spectral_parent'], source)
        return root, state

    def spectral_context(self, context, size=None):
        fields = {'basis', 'units', 'reference', 'history'}
        if not isinstance(context, dict) or set(context) != fields:
            raise ValueError('Explicit basis, units, reference and source history required')
        for key in ('units', 'history'):
            if not isinstance(context[key], dict) or not context[key]:
                raise ValueError('Nonempty ' + key + ' required')
        units = context['units']
        if (units.get('source', units.get('energy')) != 'dimensionless' or
                any(value != 'dimensionless' for value in units.values())):
            raise ValueError('This provider requires explicitly dimensionless normalized inputs')
        if context['reference'] != '1':
            raise ValueError('This provider requires dimensionless reference 1')
        basis = context['basis']
        if size is not None:
            indexed = basis == {'kind': 'ORDERED_INDEX', 'size': size}
            explicit = (isinstance(basis, list) and len(basis) == size and
                        all(type(x) in (str, int) and x != '' for x in basis) and
                        len({canonical_bytes(x) for x in basis}) == size)
            if not (indexed or explicit):
                raise ValueError('Basis must identify every ordered source coordinate')
        elif not basis:
            raise ValueError('Explicit transport basis required')

    def spectral_execute(self, operation, payload):
        common = {'name', 'source_binding'}
        required = {
            'GEN3_SPECTRAL_ADMIT': common | {'source', 'context'},
            'GEN3_LOG1P_ENCLOSURE': common | {'record'},
            'GEN3_SPECTRAL_LOG_PROFILE': common | {'record', 'tau'},
            'GEN3_SPECTRAL_REFINE': common | {'record'},
            'GEN3_SIGNED_TRANSPORT_LOG': common | {'context', 'initial_energy', 'increments'},
            'GEN3_SPECTRAL_EXPORT': common,
        }
        controls = {'max_degree', 'max_new_modes', 'max_terms', 'epsilon', 'rho',
                    'numerical', 'coefficient_order', 'tau', 'route'}
        allowed = {
            'GEN3_SPECTRAL_ADMIT': {'max_degree'},
            'GEN3_LOG1P_ENCLOSURE': controls - {'tau', 'coefficient_order'},
            'GEN3_SPECTRAL_LOG_PROFILE': controls - {'rho', 'route'},
            'GEN3_SPECTRAL_REFINE': controls,
            'GEN3_SIGNED_TRANSPORT_LOG': {'max_terms', 'numerical'},
            'GEN3_SPECTRAL_EXPORT': set(),
        }
        if not required[operation] <= set(payload) or set(payload) - required[operation] - allowed[operation]:
            raise ValueError('Supply exactly the declared spectral fields')
        name, source = payload['name'], payload['source_binding']
        if not isinstance(name, str) or not name or len(name) > 128:
            raise ValueError('Record name must contain 1..128 characters')
        if not isinstance(source, dict) or not source:
            raise ValueError('Explicit spectral source binding required')
        if operation == 'GEN3_SPECTRAL_EXPORT':
            row = self.spectral_record(name, source)
            out = {'record': deepcopy(row), 'sha256': digest(row), 'recomputed': False}
            if row['kind'] != 'transport':
                root, state = self.spectral_dependencies(row, source)
                out.update(source_record=deepcopy(root), spectral_record=deepcopy(state))
            return out
        key = 'capability:spectral:' + name
        if key in self.machine.origins:
            raise ValueError('Retain prior record; use a new successor identity')
        row = {'schema': 'GEN3_CERTIFIED_RECORD_V1', 'name': name, 'operation': operation,
               'source_binding': deepcopy(source), 'request': deepcopy(payload),
               'native_manifest_sha256': digest(self.manifest)}
        counters = {'native_calls': 0, 'new_modes': 0, 'reused_modes': 0}
        native_work = {}

        def native(op, data):
            result = self.call(op, data)
            counters['native_calls'] += 1
            for k, v in result.get('counters', {}).items():
                native_work[k] = native_work.get(k, 0) + v
            return result

        if operation == 'GEN3_SPECTRAL_ADMIT':
            vector = payload['source']
            if not isinstance(vector, list) or not 1 <= len(vector) <= 65536:
                raise ValueError('Source dimension must be in 1..65536')
            self.spectral_context(payload['context'], len(vector))
            degree = bounded(payload.get('max_degree', 0), 0, min(256, len(vector)-1), 'max_degree')
            out = native('SPECTRAL_ADMIT', {'source': vector, 'max_degree': degree, 'kernel': 'MEAN_CUT_V1'})
            state = out['record']
            # Source/context occur once in durable storage, under this source identity.
            row.pop('request')
            row.update(kind='source', source=deepcopy(vector), context=deepcopy(payload['context']),
                       kernel='MEAN_CUT_V1', spectral_state=state,
                       admission={'max_degree': degree})
            counters['new_modes'] = len(state['modes'])
            result = {'kind': 'SOURCE_SPECTRAL_CERTIFICATE', 'spectral': deepcopy(state),
                      'status': out['status'], 'requested_degree': degree}
        elif operation == 'GEN3_SIGNED_TRANSPORT_LOG':
            self.spectral_context(payload['context'])
            terms = bounded(payload.get('max_terms', 64), 1, 512, 'max_terms')
            numerical = payload.get('numerical', True)
            if type(numerical) is not bool:
                raise ValueError('numerical must be boolean')
            result = native('TRANSPORT_LOG', {k: deepcopy(payload[k]) for k in
                            ('initial_energy', 'increments')} | {'max_terms': terms,
                            'numerical': numerical, 'reference': '1'})
            row.update(kind='transport', context=deepcopy(payload['context']))
        else:
            parent = self.spectral_record(payload['record'], source)
            if parent['kind'] == 'transport':
                raise ValueError('Transport records are not spectral sources')
            root, previous_state = self.spectral_dependencies(parent, source)
            state = deepcopy(previous_state['spectral_state'])
            s = len(root['source'])
            inherited = parent.get('readout_controls', {}) if operation == 'GEN3_SPECTRAL_REFINE' else {}
            params = {**inherited, **{k: deepcopy(v) for k, v in payload.items() if k in controls}}
            if operation == 'GEN3_SPECTRAL_REFINE':
                kind = parent.get('readout_kind', 'spectral' if 'tau' in params else 'scalar')
            else:
                kind = 'scalar' if operation == 'GEN3_LOG1P_ENCLOSURE' else 'spectral'
            if operation == 'GEN3_SPECTRAL_REFINE':
                irrelevant = {'tau', 'coefficient_order'} if kind == 'scalar' else {'rho', 'route'}
                if irrelevant & set(payload):
                    raise ValueError('Refinement controls must apply to the retained readout kind')
            route = params.get('route', 'spectral')
            if route not in ('spectral', 'direct') or (route == 'direct' and kind != 'scalar'):
                raise ValueError('direct route is available only for scalar source energy')
            max_degree = bounded(params.get('max_degree', min(256, s-1)), 0, min(256, s-1), 'max_degree')
            if max_degree < state['m']:
                raise ValueError('Refinement cannot discard retained modes')
            budget = bounded(params.get('max_new_modes', 32), 0, 257, 'max_new_modes')
            terms = bounded(params.get('max_terms', 64), 1, 512, 'max_terms')
            numerical = params.get('numerical', True)
            if type(numerical) is not bool:
                raise ValueError('numerical must be boolean')
            args = {'max_terms': terms, 'numerical': numerical,
                    'epsilon': params.get('epsilon', '1/1000000')}
            if kind == 'scalar':
                args['rho'] = params.get('rho', '1000001/1000000')
                args['reference'] = '1'
            else:
                if 'tau' not in params:
                    raise ValueError('Spectral profile requires exact tau')
                args['tau'] = params['tau']
                args['coefficient_order'] = bounded(params.get('coefficient_order', 4), 1, 32, 'coefficient_order')
            counters['reused_modes'] = len(state['modes'])
            if route == 'direct':
                counters['reused_modes'] = 0
                result = native('DIRECT_SCALAR_LOG', {'source': root['source'], **args})
            else:
                op = 'SCALAR_LOG' if kind == 'scalar' else 'SPECTRAL_LOG'
                while True:
                    result = native(op, {'record': state, **args})
                    if result.get('status') in ('CERTIFIED_WITHIN_TOLERANCE', 'EXACT_SYMBOLIC') or state['m'] >= max_degree or counters['new_modes'] >= budget:
                        break
                    if result.get('numerical', {}).get('mode_tail_upper') == '0':
                        # Only numerical precision remains; further projections cannot help.
                        break
                    target = min(max_degree, state['m'] + budget - counters['new_modes'], max(1, 2*state['m']))
                    if target <= state['m']:
                        break
                    extended = native('SPECTRAL_EXTEND', {'source': root['source'], 'record': state,
                                      'max_degree': target, 'max_new_modes': target-state['m']})
                    if extended['record']['m'] == state['m']:
                        break
                    counters['new_modes'] += extended['record']['m'] - state['m']
                    state = extended['record']
            row.update(kind='readout', source_record=root['name'], parent=parent['name'],
                       readout_kind=kind, readout_controls={**params, **args, 'route': route})
            if counters['new_modes']:
                row['spectral_state'] = state
            else:
                row['spectral_parent'] = previous_state['name']
            result['retained_degree'] = state['m']
            result['route'] = route
        row['result'] = deepcopy(result)
        row['work'] = deepcopy(counters)
        row['native_work'] = deepcopy(native_work)
        self.remember(key, row)
        for field, value in counters.items():
            self.machine.stats['spectral_' + field] += value
        result.update(name=name, source_binding=deepcopy(source), record_sha256=digest(row),
                      work=counters, native_work=native_work, execution={'backend': 'NATIVE_CPP_GMP_CPU',
                      'shared_checkpoint': True, 'native_source_manifest': digest(self.manifest)})
        return result
