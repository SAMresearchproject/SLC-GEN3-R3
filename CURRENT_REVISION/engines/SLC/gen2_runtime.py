"""One GEN2 native runtime with retained Q3 quality and exact-information components."""
from CURRENT_REVISION.engines.SLC.slcq3_rz_current import (
    CandidateGroupInput, FrozenSLCQ3RZModel, RankOutcome, SLCQ3RZError,
    SourceVisibleChoice, load_frozen_model,
)
from CURRENT_REVISION.engines.SLC.native.runtime import Q3Runtime

if __package__ and __package__.startswith('CURRENT_REVISION.'):
    from . import gen2
else:
    import gen2

VERSION = 'SLC-GEN2-R4'
BUILD = 'GEN2-REUSE-INFO1-20260907'
if __package__ and __package__.startswith('CURRENT_REVISION.'):
    from CURRENT_REVISION.runtime import current_generation
    __current_generation__ = current_generation()


class GEN2Runtime(Q3Runtime):
    def __init__(self, model=None, *, cache_size=128, installed=False):
        super().__init__(model, cache_size=cache_size)
        self.installed = installed
        self.generation = None
        if installed:
            from CURRENT_REVISION.runtime import current_generation, record
            self.generation = current_generation()
            if record('SLC')['version'] != VERSION:
                raise ValueError('GEN2 is not the selected global runtime')

    def _active(self):
        super()._active()
        if self.installed:
            from CURRENT_REVISION.runtime import require_generation
            require_generation(self.generation)

    def compile(self, contract=None, *, rho=1, blocks=None):
        self._active()
        from importlib import import_module
        compiler = import_module(gen2.__name__ + '.compiler')
        native = import_module(gen2.__name__ + '.native')
        spec = contract if contract is not None else native.native_contract(
            rho=rho, **({'blocks': blocks} if blocks is not None else {}))
        block = compiler.compile_block(spec)
        # Compiled blocks may be used directly within or after this runtime.
        # Register the already-bound log class without opening a second stack.
        import_module(gen2.__name__ + '.motion')._log_class(
            self.exact_information().hd_module.FormalLogElement)
        return block

    def direction_fiber(self, address, writes, **custody):
        native_word = super().direction_fiber(address, writes, **custody)
        from importlib import import_module
        return import_module(gen2.__name__ + '.native_phase').annotate_word(native_word)

    def execute(self, operation, payload):
        self._active()
        if not isinstance(payload, dict):
            raise ValueError('GEN2 operation payload must be an object')
        from importlib import import_module
        if operation == 'T18_WORD':
            return self.direction_fiber(**payload)
        if operation in {'GEN2_SIGNED_LOG', 'GEN2_SIGNED_LOG_RESUME'}:
            return import_module(gen2.__name__ + '.signed_log').dispatch(
                operation, payload, self.exact_information())
        if operation in {'GEN2_HISTORY_SUMMARY', 'GEN2_HISTORY_SUMMARY_APPEND'}:
            return import_module(gen2.__name__ + '.history_summary').dispatch(
                operation, payload, self.exact_information())
        if operation.startswith('GEN2_BOUNDARY_'):
            return import_module(gen2.__name__ + '.boundary_information').dispatch(
                operation, payload, self)
        if operation in {'GEN2_OBSERVATION_POLICY_PLAN', 'GEN2_OBSERVATION_POLICY_APPLY',
                         'GEN2_OBSERVATION_POLICY_RESUME'}:
            policy = import_module(gen2.__name__ + '.observation_policy')
            contract = policy.resolve_contract(operation, payload)
            block = self.compile(contract)
            return policy.dispatch(operation, payload, block,
                self.exact_information().hd_module.FormalLogElement)
        if operation == 'GEN2_DENSE_N72':
            return import_module(gen2.__name__ + '.dense_n72').dispatch(
                payload, generation=self.generation, foundation=self.exact_information())
        if operation == 'GEN2_REUSE_STATS':
            if set(payload) - {'reset'} or ('reset' in payload and type(payload['reset']) is not bool):
                raise ValueError('Reuse statistics accept only an optional boolean reset')
            rows = {}
            for name in ('signed_log', 'history_summary', 'motion', 'observation',
                         'observation_policy', 'boundary_information'):
                module = import_module(gen2.__name__ + '.' + name)
                method = getattr(module, 'reuse_stats', None)
                if method is not None:
                    rows[name] = method(reset=payload.get('reset', False))
            return {'schema': 'GEN2_REUSE_EXECUTION_TELEMETRY_V1',
                    'mathematical_identity': False, 'modules': rows}
        if operation in {'GEN2_INVERSE_OPEN', 'GEN2_OBSERVATION_PLAN',
                         'GEN2_OBSERVATION_APPLY', 'GEN2_INVERSE_RESUME'}:
            contract = (payload.get('contract') if operation == 'GEN2_INVERSE_OPEN'
                        else payload['checkpoint']['body']['contract'])
            block = self.compile(contract, rho=payload.get('rho', 1), blocks=payload.get('blocks'))
            observation_payload = dict(payload)
            if operation == 'GEN2_INVERSE_OPEN':
                observation_payload.pop('rho', None)
                observation_payload.pop('blocks', None)
            return import_module(gen2.__name__ + '.observation').dispatch(
                operation, observation_payload, block,
                self.exact_information().hd_module.FormalLogElement)
        if operation in ('GEN2_HD', 'GEN2_HD_PRIMITIVES', 'GEN2_FORMAL_LOG'):
            return import_module(gen2.__name__ + '.information').dispatch(
                operation, payload, self.exact_information())
        if operation.startswith('GEN2_TAU_'):
            return import_module(gen2.__name__ + '.applications').dispatch(operation, payload)
        groups = {
            'construction': {'GEN2_CONSTRUCTION_COMPILE', 'GEN2_CONSTRUCTION_CHANGE',
                             'GEN2_LI6_CONSTRUCTION', 'GEN2_LI6_SITE_CYCLE'},
            'readouts': {'GEN2_READOUT', 'GEN2_READOUT_INVERSE'},
            'encounters': {'GEN2_ENCOUNTER', 'GEN2_ENCOUNTER_INVERSE'},
        }
        for name, operations in groups.items():
            if operation in operations:
                module = import_module(gen2.__name__ + '.' + name)
                if name == 'encounters':
                    return module.dispatch(operation.removeprefix('GEN2_'), payload,
                        log_class=self.exact_information().hd_module.FormalLogElement)
                return module.dispatch(operation.removeprefix('GEN2_'), payload)
        if operation == 'GEN2_SOURCE_BATCH':
            return import_module(gen2.__name__ + '.fabric').execute(payload)
        if operation == 'GEN2_CUSTODY':
            custody = import_module(gen2.__name__ + '.custody').compile_custody(payload['contract'])
            action = payload.get('action', 'profile')
            if action == 'encode': return custody.encode(payload['source'])
            if action == 'decode': return custody.decode(payload['visible'], payload['receipt'])
            if action == 'fiber': return custody.fiber(payload['visible'])
            if action == 'profile': return custody.to_dict()
            raise ValueError('Unknown custody action')
        if operation == 'GEN2_MOTION_RESUME':
            block = self.compile(payload['checkpoint']['body']['contract'])
            return import_module(gen2.__name__ + '.motion').resume_motion(
                block, payload['checkpoint'], max_writes=payload.get('max_writes'),
                log_class=self.exact_information().hd_module.FormalLogElement)
        if operation == 'GEN2_RESUME':
            block = self.compile(payload['checkpoint']['body']['contract'])
            answer = block.resume(payload['checkpoint'], max_steps=payload.get('max_steps'))
            result = answer.to_dict(include_graph=True)
            if payload.get('include_checkpoint') or not answer.complete:
                result['checkpoint'] = answer.checkpoint()
            return result
        if operation in {'GEN2_COMPILE', 'GEN2_RUN', 'GEN2_DECODE'}:
            block = self.compile(payload.get('contract'), rho=payload.get('rho', 1), blocks=payload.get('blocks'))
            if operation == 'GEN2_COMPILE': return block.to_dict()
            if operation == 'GEN2_RUN':
                return block.run(payload['initial'], payload.get('program'),
                    view=payload.get('view', 'JOINT'), motion=payload.get('motion'),
                    max_writes=payload.get('max_writes'),
                    log_class=self.exact_information().hd_module.FormalLogElement)
            answer = block.decode(payload['observations'], directions=payload.get('directions'),
                                  initial_states=payload.get('initial_states'), view=payload.get('view', 'JOINT'),
                                  max_steps=payload.get('max_steps'))
            result = answer.to_dict(include_graph=True)
            if payload.get('include_checkpoint') or not answer.complete:
                result['checkpoint'] = answer.checkpoint()
            if payload.get('include_paths'):
                limit = payload.get('path_limit', 1000)
                result['requested_paths'] = list(answer.iter_paths(limit=limit))
                result['path_export_limit'] = limit
            return result
        raise ValueError('Unknown GEN2 operation: ' + operation)


SLCQ3RZRuntime = GEN2Runtime


def open_runtime(model=None, *, cache_size=128):
    return GEN2Runtime(model, cache_size=cache_size,
                       installed=bool(__package__ and __package__.startswith('CURRENT_REVISION.')))


def derive_r3_graph(query, candidate, *, model=None):
    with open_runtime(model) as runtime:
        return runtime.derive_r3_graph(query, candidate)


def score(query, candidate, *, model=None):
    with open_runtime(model) as runtime:
        return runtime.score(query, candidate)


def rank(query, candidates, *, model=None):
    with open_runtime(model) as runtime:
        return runtime.rank(query, candidates)
