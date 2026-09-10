"""One runtime-owned state and executable, explicitly source-scoped knowledge."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import hashlib
import json
from ..gen2.compiler import CompiledBlock
from ..gen2.contracts import Event
from ..gen2.exact import canonical, canonical_bytes, digest
from .logs import LogAccount
from .store import Store
from . import VERSION, GENERATION


class LearnedBlock(CompiledBlock):
    """A runtime view; the shared compiled source object is never mutated."""
    def __init__(self, source, machine):
        self.source, self.machine = source, machine

    def __getattr__(self, name):
        return getattr(self.source, name)

    def forward(self, state, event):
        state = self.contract.admit_state(state)
        label = event.label if isinstance(event, Event) else event
        declared = self.events.get(label)
        if declared is None or (isinstance(event, Event) and event != declared):
            raise ValueError('Event is outside the bound source alphabet')
        if state not in self.state_set or (declared.admitted_states is not None and state not in declared.admitted_states):
            raise ValueError('Event is outside its bound source-state admission')
        key = digest({'contract': self.contract_id, 'state': state, 'event': label})
        known = self.machine.relations.get(key)
        if known is None:
            target = self.source.forward(state, event)
            known = canonical({'contract_id': self.contract_id, 'contract': self.contract.to_dict(),
                'from': state, 'event': label, 'to': target,
                'action_before': self.contacts[state], 'action_after': self.contacts[target],
                'direction': declared.direction,
                'admission': 'EXECUTED_EXACT_NATIVE_SOURCE_EVENT'})
            self.machine.relations[key] = known
            self.machine.new_relations.add(key)
            self.machine.stats['native_events_acquired'] += 1
        else:
            target = tuple(known['to'])
            self.machine.stats['learned_events_executed'] += 1
        self.machine.support.append(key)
        return target


def implementation_binding():
    base = Path(__file__).resolve().parent.parent
    names = ['gen3_runtime.py', 'gen2_runtime.py']
    names += [str(p.relative_to(base)) for p in sorted((base/'gen3').rglob('*.py'))]
    names += [str(p.relative_to(base)) for p in sorted((base/'gen3/seeds').glob('*.json'))]
    # Include exact primitives, their source calibration and all declared schemas.
    names += [str(p.relative_to(base)) for p in sorted((base/'gen2').rglob('*'))
              if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.py','.json','.jsonl')]
    return {'version': VERSION, 'generation': GENERATION,
            'implementation_sha256': digest({n: hashlib.sha256((base/n).read_bytes()).hexdigest() for n in names})}


class Machine:
    def __init__(self):
        self.relations, self.compositions, self.observations, self.accounts = {}, {}, {}, {}
        self.origins = {}
        self.state = None
        self.sequence = 0
        self.stats = Counter()
        self.support = []
        self.store = None
        self.refs = {k: {} for k in ('relations','compositions','observations','accounts','origins')}
        self.new_relations = set()
        self.dirty = {k: set() for k in ('compositions','observations','accounts','origins')}
        self.journal, self.journal_refs = [], []
        self.last_checkpoint = None

    def attach(self, directory):
        if self.store is not None:
            if self.store.root != Path(directory).resolve():
                raise ValueError('A warm machine cannot silently change its durable store')
            return
        store = Store(directory, implementation_binding())
        try:
            if (store.root/'HEAD.json').exists():
                if self.sequence or self.accounts:
                    raise ValueError('Attach recovery storage before executing source work')
                self._restore(store, store.restore())
            self.store = store
        except BaseException:
            store.close(); raise

    def _restore(self, store, snapshot):
        refs = snapshot['refs']
        for group in ('relations','compositions','observations','origins'):
            setattr(self, group, {key: store.get(ref) for key, ref in refs[group].items()})
        self.accounts = {key: LogAccount.restore(store, ref) for key, ref in refs['accounts'].items()}
        self.refs = deepcopy(refs)
        self.state, self.sequence = snapshot['state'], snapshot['sequence']
        self.journal_refs = snapshot['journal']
        self.stats.update(snapshot['stats']); self.stats['trusted_snapshot_restores'] += 1
        self.new_relations.clear()
        for changed in self.dirty.values():
            changed.clear()

    def checkpoint(self):
        if self.store is None:
            raise ValueError('Attach a durable store before requesting a checkpoint')
        for key in self.new_relations:
            self.refs['relations'][key] = self.store.put(self.relations[key])
        self.new_relations.clear()
        for group, keys in self.dirty.items():
            for key in keys:
                obj = getattr(self, group)[key]
                self.refs[group][key] = obj.persist(self.store) if group == 'accounts' else self.store.put(obj)
            keys.clear()
        for row in self.journal:
            self.journal_refs.append(self.store.put(row))
        self.journal.clear()
        closure = list(self.journal_refs)
        for group in self.refs.values():
            closure.extend(group.values())
        for account in self.accounts.values():
            closure.extend(account.chunks)
        snapshot = {'refs': self.refs, 'state': self.state, 'sequence': self.sequence,
                    'journal': self.journal_refs, 'stats': dict(self.stats)}
        self.last_checkpoint = self.store.commit(snapshot, closure)
        return deepcopy(self.last_checkpoint)

    def account(self, name, payload):
        if not isinstance(name, str) or not name or name in self.accounts:
            raise ValueError('A new log account needs an unused nonempty identity')
        account = LogAccount(payload['quantity'], payload['source_binding'])
        count = account.append(payload['points'], payload['edges'])
        self.accounts[name] = account
        self.dirty['accounts'].add(name)
        self.stats['new_log_edges'] += count
        return account.readout()

    def append(self, name, points, edges):
        account = self.accounts[name]
        self.stats['new_log_edges'] += account.append(points, edges)
        self.dirty['accounts'].add(name)
        return account.readout()

    def record_run(self, result):
        self.sequence += 1
        name = 'execution:' + str(self.sequence)
        points = [{'id': name + ':p' + str(i), 'state': q, 'action': action}
                  for i, (q, action) in enumerate(zip(result['states'], result['contact_profile'], strict=True))]
        edges = [{'id': name + ':e' + str(i), 'before': points[i]['id'], 'after': points[i+1]['id'],
                  'event': {'label': event, 'direction': result['directions'][i]}}
                 for i, event in enumerate(result['program'])]
        readout = self.account(name, {'quantity': {'kind': 'SOURCE_ACTION',
            'units': {'native_source_action': 1}, 'scope': 'HISTORY',
            'source': result['contract_id']}, 'source_binding': result['contract_id'],
            'points': points, 'edges': edges})
        key = digest({'contract': result['contract_id'], 'initial': result['initial'],
                      'program': result['program'], 'view': result['view']})
        composition = {'contract_id': result['contract_id'], 'initial': result['initial'],
            'program': result['program'], 'final': result['states'][-1], 'support': list(self.support),
            'history_account': name, 'execution': 'ORDERED_SOURCE_RELATION_COMPOSITION'}
        if key in self.compositions:
            self.stats['known_compositions_executed'] += 1
        else:
            self.stats['new_compositions_acquired'] += 1
            self.compositions[key] = composition
            self.dirty['compositions'].add(key)
        self.state = {'contract_id': result['contract_id'], 'state': result['states'][-1],
            'contract': deepcopy(self.active_contract),
            'history_account': name, 'composition': key, 'sequence': self.sequence,
            'phase': deepcopy(result.get('motion', {}).get('coordinate_records', [])[-1:]),
            'barrier': result['barrier']}
        self.journal.append({'type': 'native_execution', **composition, 'sequence': self.sequence})
        return {'machine': VERSION, 'history_account': name, 'logarithmic_accumulation': readout,
                'composition': key, 'support_occurrences': len(self.support),
                'knowledge': self.status()['knowledge']}

    def status(self):
        return {'schema': 'GEN3_UNIFIED_MACHINE_STATUS_V1', 'version': VERSION,
            'sequence': self.sequence, 'state': deepcopy(self.state),
            'knowledge': {k: len(getattr(self, k)) for k in ('relations','compositions','observations','origins')},
            'log_accounts': len(self.accounts), 'execution_counters': dict(self.stats),
            'durable_store': None if self.store is None else str(self.store.root),
            'checkpoint': deepcopy(self.last_checkpoint)}

    def import_relations(self, package, compile_source):
        # A source hash alone is insufficient: every imported relation is checked
        # against the current exact primitive and complete source scope.
        knowledge = package['knowledge']
        original = hashlib.sha256((json.dumps(knowledge, sort_keys=True, indent=2,
                    allow_nan=False)+'\n').encode()).hexdigest()
        if original != package['sha256']:
            raise ValueError('Imported acquired knowledge seal differs')
        source = compile_source(rho=1, blocks=[[1,4,7]]).source
        admitted = {}
        for row in knowledge['transitions'].values():
            state = source.contract.admit_state(row['from'])
            event = row['event']
            target = source.forward(state, event)
            if (row['contract_id'] != source.contract_id or list(target) != row['to']
                or source.contacts[state] != row['action_before'] or source.contacts[target] != row['action_after']):
                raise ValueError('Imported relation differs from current source semantics')
            key = digest({'contract': source.contract_id, 'state': state, 'event': event})
            admitted[key] = canonical({'contract_id': source.contract_id, 'contract': source.contract.to_dict(),
                'from': state, 'event': event, 'to': target, 'action_before': row['action_before'],
                'action_after': row['action_after'], 'direction': source.events[event].direction,
                'admission': 'EXECUTED_EXACT_NATIVE_SOURCE_EVENT'})
        for key, row in admitted.items():
            if key in self.relations and self.relations[key] != row:
                raise ValueError('Imported relation conflicts with admitted support')
        self.relations.update(admitted); self.new_relations.update(admitted)
        self.origins[original] = deepcopy(package); self.dirty['origins'].add(original)
        self.stats['imported_relations_semantically_validated'] += len(admitted)
        return {'status': 'ADMITTED', 'original_sha256': original, 'relations': len(admitted),
                'source_contract_id': source.contract_id, 'original_package_preserved': True}

    def close(self):
        if self.store is not None:
            self.store.close(); self.store = None
