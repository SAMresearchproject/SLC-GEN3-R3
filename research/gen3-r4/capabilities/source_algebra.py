"""Source-bound exact operator records in the common native worker/checkpoint."""
from copy import deepcopy
from CURRENT_REVISION.engines.SLC.gen2.exact import canonical_bytes, digest

SOURCE_OPERATIONS = (
    'GEN3_SOURCE_OPERATOR_WORD', 'GEN3_SOURCE_SUBSPACE', 'GEN3_NATIVE_PAIR_ROOTS',
    'GEN3_BLOCK_SOURCE_RECURRENCE', 'GEN3_SOURCE_SPECTRAL_CREATION',
    'GEN3_SOURCE_WORD_EXCHANGE', 'GEN3_SOURCE_TERMINAL_ACTION', 'GEN3_SOURCE_SPECTRAL_EXPORT',
)

FIELDS = {
    'GEN3_SOURCE_OPERATOR_WORD': ({'operators', 'program', 'output'}, set()),
    'GEN3_SOURCE_SUBSPACE': ({'H', 'seeds', 'mode'}, {'reference', 'reference_energy'}),
    'GEN3_NATIVE_PAIR_ROOTS': ({'H', 'frame', 'parameters'}, set()),
    'GEN3_BLOCK_SOURCE_RECURRENCE': ({'H', 'seeds'}, {'max_levels'}),
    'GEN3_SOURCE_SPECTRAL_CREATION': ({'recurrence'}, {'reference', 'reference_energy', 'x'}),
    'GEN3_SOURCE_WORD_EXCHANGE': ({'mode'}, {'lift', 'u', 'v', 'primes', 'include_terminal', 'on_reference', 'family', 'R'}),
    'GEN3_SOURCE_TERMINAL_ACTION': ({'lift', 'mode', 'frame'}, {'primes'}),
}


class SourceCapabilities:
    def source_record(self, name, source):
        key = 'capability:source_algebra:' + name
        if key not in self.machine.origins:
            raise ValueError('Unknown retained source operator record')
        value = self.machine.origins[key]
        if canonical_bytes(value['source_binding']) != canonical_bytes(source):
            raise ValueError('Source operator record binding differs')
        return value

    def source_execute(self, operation, payload):
        export = operation == 'GEN3_SOURCE_SPECTRAL_EXPORT'
        required = {'name', 'source_binding'} if export else {'name', 'source_binding', 'context', 'data'}
        if set(payload) != required:
            raise ValueError('Supply exactly the source operation fields')
        name, source = payload['name'], payload['source_binding']
        if not isinstance(name, str) or not name or len(name) > 128:
            raise ValueError('Source operation name must contain1..128 characters')
        if not isinstance(source, dict) or not source:
            raise ValueError('Explicit source binding required')
        if export:
            record = self.source_record(name, source)
            return {'record': deepcopy(record), 'sha256': digest(record), 'recomputed': False,
                    'checkpoint_schema': 'GEN3_UNIFIED_CHECKPOINT_V1'}
        key = 'capability:source_algebra:' + name
        if key in self.machine.origins:
            raise ValueError('Retain prior source operation; supply a successor identity')
        context = payload['context']
        if not isinstance(context, dict) or set(context) != {'basis', 'field', 'units', 'history', 'spectral_coordinate'}:
            raise ValueError('Explicit basis, field, units, history and spectral coordinate required')
        basis = context['basis']
        if (not isinstance(basis, list) or not 1 <= len(basis) <= 64 or
                any(type(v) not in (str, int) or v == '' for v in basis) or
                len({canonical_bytes(v) for v in basis}) != len(basis)):
            raise ValueError('Supply1..64 distinct scalar source basis identities')
        if any(not isinstance(context[k], dict) or not context[k] for k in ('field', 'units', 'history')):
            raise ValueError('Nonempty exact field, units and source history required')
        if not isinstance(context['spectral_coordinate'], str) or not context['spectral_coordinate']:
            raise ValueError('Explicit spectral coordinate convention required')
        data = deepcopy(payload['data'])
        need, optional = FIELDS[operation]
        if not isinstance(data, dict) or not need <= data.keys() or set(data) - need - optional:
            raise ValueError('Source operation data fields differ from contract')
        if operation == 'GEN3_SOURCE_WORD_EXCHANGE':
            mode = data['mode']
            fields = ({'mode', 'lift', 'u', 'v', 'primes'}, {'include_terminal', 'on_reference'}) if mode == 'LIFT_RANK' else ({'mode', 'family', 'R'}, set()) if mode == 'CONSTANT_EXCHANGE' else (set(), set())
            required_mode, optional_mode = fields
            if not required_mode or not required_mode <= data.keys() or set(data) - required_mode - optional_mode:
                raise ValueError('Exchange fields differ from selected mode')
            for flag in ('include_terminal', 'on_reference'):
                if flag in data and type(data[flag]) is not bool:
                    raise ValueError('Exchange flags must be Boolean')
        if operation == 'GEN3_SOURCE_TERMINAL_ACTION':
            needed = {'lift', 'mode', 'frame'} | ({'primes'} if data['mode'] == 'MODULAR_ACTION' else set())
            if data['mode'] not in ('MODULAR_ACTION', 'EXACT_ACTION') or set(data) != needed:
                raise ValueError('Terminal fields differ from selected mode')
        if 'primes' in data and (not isinstance(data['primes'], list) or not 1 <= len(data['primes']) <= 4 or any(type(p) is not int for p in data['primes'])):
            raise ValueError('One to four integer modular primes required')
        if 'max_levels' in data and type(data['max_levels']) is not int:
            raise ValueError('Integer recurrence budget required')
        if operation == 'GEN3_NATIVE_PAIR_ROOTS' and set(data['parameters']) != {'mu', 'a', 'b', 'c', 'g', 'offset'}:
            raise ValueError('Explicit native pair parameters required')
        if operation == 'GEN3_SOURCE_OPERATOR_WORD':
            for step in data['program']:
                op = step.get('op')
                needed = {'name', 'op'} | ({'dimension'} if op == 'identity' else {'inputs'}) | ({'factor'} if op == 'scale' else set())
                if set(step) != needed or (op == 'identity' and type(step['dimension']) is not int):
                    raise ValueError('Ordered word fields differ from selected step')
        dependencies = []

        def recurrence(value):
            if isinstance(value, dict) and set(value) == {'record'}:
                record = self.source_record(value['record'], source)
                if record['operation'] != 'GEN3_BLOCK_SOURCE_RECURRENCE':
                    raise ValueError('Dependency is not an admitted block recurrence')
                if canonical_bytes(record['context']['basis']) != canonical_bytes(basis) or record['context']['field'] != context['field']:
                    raise ValueError('Recurrence dependency basis/field differs')
                dependencies.append({'name': value['record'], 'sha256': digest(record)})
                return deepcopy(record['result'])
            if not isinstance(value, dict):
                raise ValueError('Explicit recurrence or retained record required')
            return value

        if 'recurrence' in data:
            data['recurrence'] = recurrence(data['recurrence'])
        if 'lift' in data:
            lift = data['lift']
            allowed = {'recurrence', 'seed_operators', 'reference', 'action', 'reference_energy'}
            if not isinstance(lift, dict) or not {'recurrence', 'seed_operators', 'reference', 'action'} <= lift.keys() or set(lift) - allowed:
                raise ValueError('Explicit operator lift contract required')
            lift['recurrence'] = recurrence(lift['recurrence'])
        matrices = []
        for matrix_key in ('H', 'seeds', 'frame', 'reference'):
            if matrix_key in data:
                matrices.append(data[matrix_key])
        if 'recurrence' in data:
            matrices.append(data['recurrence']['H'])
        if 'lift' in data:
            matrices += [data['lift']['recurrence']['H'], data['lift']['reference']]
        if operation == 'GEN3_SOURCE_OPERATOR_WORD':
            # Tensor construction may start in smaller local spaces; the selected
            # result is checked against the declared output basis after execution.
            pass
        elif operation == 'GEN3_SOURCE_WORD_EXCHANGE' and data['mode'] == 'CONSTANT_EXCHANGE':
            matrices.extend(coeff for poly in data.get('family', []) for coeff in poly)
        if any(not isinstance(m, list) or len(m) != len(basis) for m in matrices):
            raise ValueError('Declared source basis and matrix rows differ')
        if ('reference' in data) != ('reference_energy' in data):
            raise ValueError('Reference and eigenvalue must be supplied together')
        data['field'] = context['field']
        result = self.call(operation.removeprefix('GEN3_'), data)
        if operation == 'GEN3_SOURCE_OPERATOR_WORD' and len(result['matrix']) != len(basis):
            raise ValueError('Word output basis differs')
        record = {'schema': 'GEN3_SOURCE_OPERATOR_RECORD_V1', 'operation': operation,
                  'name': name, 'source_binding': deepcopy(source), 'context': deepcopy(context),
                  'input': deepcopy(payload['data']), 'dependencies': dependencies,
                  'result': deepcopy(result), 'native_manifest_sha256': digest(self.manifest)}
        self.remember(key, record)
        self.machine.stats['native_source_operator_calls'] += 1
        result['record_sha256'] = digest(record)
        result['execution'] = {'backend': 'NATIVE_CPP_GMP_CPU', 'exact_field': deepcopy(context['field']),
                               'native_source_manifest': digest(self.manifest), 'shared_checkpoint': True}
        return result
