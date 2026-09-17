"""Source-bound RXT capabilities executed by a warm exact C++/GMP consumer.

Python validates, routes and persists; the native worker computes exact results.
All acquired models and call origins share the existing R3 machine/checkpoint.
"""
from .source_algebra import SourceCapabilities, SOURCE_OPERATIONS
from .spectral import SpectralCapabilities, SPECTRAL_OPERATIONS
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import selectors
import subprocess
import threading
from CURRENT_REVISION.engines.SLC.gen2.exact import canonical_bytes, digest

HERE = Path(__file__).resolve().parent
OPERATIONS = ('GEN3_CAPABILITIES', 'GEN3_SIGNED_ENERGY', 'GEN3_COMMON_MINIMA',
              'GEN3_TREE_FIT', 'GEN3_TREE_PREDICT', 'GEN3_TREE_EXPORT', 'GEN3_CONSTRUCTION_PLAN',
              'GEN3_OPERATOR_OBSTRUCTION', 'GEN3_COMMUTING_LOG', 'GEN3_OPERATOR_EXPORT') + SPECTRAL_OPERATIONS + SOURCE_OPERATIONS


class Capabilities(SpectralCapabilities, SourceCapabilities):
    def __init__(self, machine):
        self.machine = machine
        self.manifest = json.loads((HERE/'MANIFEST.json').read_text())
        for name, sha in self.manifest['files'].items():
            if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != sha:
                raise ValueError('Installed capability source differs: '+name)
        self.package = json.loads((HERE/'MODELS.json').read_text())
        self.worker = None
        self.lock = threading.RLock()

    def close(self):
        with self.lock:
            if self.worker is not None:
                self.worker.stdin.close()
                try: self.worker.wait(timeout=3)
                except subprocess.TimeoutExpired: self.worker.kill(); self.worker.wait()
                self.worker.stdout.close()
                self.worker = None

    def call(self, op, payload):
        raw = canonical_bytes({'op':op, 'payload':payload})
        if len(raw) > 64*1024*1024:
            raise ValueError('Capability input exceeds 64 MiB admission')
        with self.lock:
            if self.worker is None:
                self.worker = subprocess.Popen([str(HERE/'capability-native')],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                self.worker.stdin.write(raw+b'\n'); self.worker.stdin.flush()
                with selectors.DefaultSelector() as ready:
                    ready.register(self.worker.stdout, selectors.EVENT_READ)
                    if not ready.select(120):
                        self.worker.kill(); raise ValueError('Native capability execution exceeded its bounded call time')
                line = self.worker.stdout.readline()
                if not line: raise ValueError('Native capability worker exited before returning a result')
                result = json.loads(line)
            except BaseException:
                self.close(); raise
        if not result['ok']: raise ValueError(result['error'])
        return result['result']

    def remember(self, key, value):
        self.machine.origins[key] = deepcopy(value)
        self.machine.dirty['origins'].add(key)

    def model(self, name):
        key='capability:model:'+name
        if key in self.machine.origins: return self.machine.origins[key]
        if name not in self.package['models']: raise ValueError('Unknown acquired model')
        return {'model':deepcopy(self.package['models'][name]),
                'source_binding':deepcopy(self.package['source_binding'][name]),
                'origin':self.package['origin'], 'name':name}

    def operator_execute(self, operation, payload):
        common = {'name', 'source_binding'}
        fields = {
            'GEN3_OPERATOR_OBSTRUCTION': common | {'context', 'P', 'Q', 'phase_generator'},
            'GEN3_COMMUTING_LOG': common | {'context', 'moments', 'order'},
            'GEN3_OPERATOR_EXPORT': common,
        }
        if set(payload) != fields[operation]:
            raise ValueError('Supply exactly the declared operator fields')
        name, source = payload['name'], payload['source_binding']
        if not isinstance(name, str) or not name or len(name)>128:
            raise ValueError('Operator name must be a nonempty string of at most 128 characters')
        if not isinstance(source, dict) or not source:
            raise ValueError('Explicit operator source binding required')
        key = 'capability:operator:'+name
        if operation == 'GEN3_OPERATOR_EXPORT':
            if key not in self.machine.origins:
                raise ValueError('Unknown retained operator')
            record = self.machine.origins[key]
            if canonical_bytes(source) != canonical_bytes(record['source_binding']):
                raise ValueError('Operator source binding differs')
            return {'record':deepcopy(record), 'sha256':digest(record),
                    'recomputed':False, 'checkpoint_schema':'GEN3_UNIFIED_CHECKPOINT_V1'}
        if key in self.machine.origins:
            raise ValueError('Retain prior operator; use a new successor identity')
        context = payload['context']
        required = {'basis','coefficient_parameter','expansion_variables','normalization','units','history'}
        if not isinstance(context, dict) or set(context)!=required:
            raise ValueError('Explicit basis, parameters, reference, units and source history required')
        basis=context['basis']
        if (not isinstance(basis,list) or not 1<=len(basis)<=16 or
                any(type(x) not in (str,int) or x=='' for x in basis) or
                len({canonical_bytes(x) for x in basis})!=len(basis)):
            raise ValueError('Supply 1..16 distinct scalar basis identities')
        variables=['u','v'] if operation=='GEN3_OPERATOR_OBSTRUCTION' else ['s']
        if context['expansion_variables'] != variables:
            raise ValueError('Expansion variables differ from the operation convention')
        parameter=context['coefficient_parameter']
        if not isinstance(parameter,str) or not parameter or parameter in variables:
            raise ValueError('Distinct explicit coefficient parameter required')
        if context['normalization']!='IDENTITY_AT_ZERO':
            raise ValueError('This formal expansion requires identity normalization at zero')
        if not isinstance(context['units'],dict) or not context['units']:
            raise ValueError('Explicit coefficient and coordinate units required')
        if not isinstance(context['history'],dict) or not context['history']:
            raise ValueError('Retain an explicit source history or source-history reference')
        data={k:v for k,v in payload.items() if k not in common|{'context'}}
        data['dimension']=len(basis)
        native='OPERATOR_OBSTRUCTION' if operation=='GEN3_OPERATOR_OBSTRUCTION' else 'COMMUTING_LOG'
        result=self.call(native,data)
        result['context']=deepcopy(context)
        result['source_binding']=deepcopy(source)
        result['name']=name
        record={'operation':operation,'name':name,'source_binding':deepcopy(source),
                'payload':deepcopy(payload),'result':deepcopy(result),
                'native_manifest_sha256':digest(self.manifest)}
        self.remember(key,record)
        self.machine.stats['native_operator_calls']+=1
        result['record_sha256']=digest(record)
        result['execution']={'backend':'NATIVE_CPP_GMP_CPU','shared_R3_checkpoint':True,
                             'native_source_manifest':digest(self.manifest)}
        return result

    def execute(self, operation, payload):
        canonical_bytes(payload)  # Reject floats before native execution or persistence.
        if operation in SOURCE_OPERATIONS:
            return self.source_execute(operation, payload)
        if operation in SPECTRAL_OPERATIONS:
            return self.spectral_execute(operation, payload)
        if operation in ('GEN3_OPERATOR_OBSTRUCTION','GEN3_COMMUTING_LOG','GEN3_OPERATOR_EXPORT'):
            return self.operator_execute(operation,payload)
        if operation == 'GEN3_CAPABILITIES':
            if payload: raise ValueError('Capabilities status takes no fields')
            return {'version':self.manifest['version'], 'operations':list(OPERATIONS),
                    'certified_spectral':{'provider':'MEAN_CUT_V1','dimension':[1,65536],'max_degree':256,'coefficient_order':[1,32],'record_schema':'GEN3_CERTIFIED_RECORD_V1','source_required':True,'backend':'NATIVE_CPP_GMP_CPU'},
                    'source_operator_algebra':{'dimension':[1,64],'field':'Q or real quadratic','operations':list(SOURCE_OPERATIONS),'records':'GEN3_SOURCE_OPERATOR_RECORD_V1'},
                    'backend':'NATIVE_CPP_GMP_CPU', 'installed_models':list(self.package['models']),
                    'source_binding':self.package['source_binding'],
                    'acquired_models':[k.removeprefix('capability:model:') for k in self.machine.origins if k.startswith('capability:model:')],
                    'original_core_memories_preserved':True,
                    'retained_operators':[k.removeprefix('capability:operator:') for k in self.machine.origins if k.startswith('capability:operator:')]}
        allowed = {
            'GEN3_SIGNED_ENERGY':{'left','right','a','b','source_binding'},
            'GEN3_COMMON_MINIMA':{'states','left','right','source_binding'},
            'GEN3_TREE_FIT':{'name','rows','source_binding'},
            'GEN3_TREE_PREDICT':{'name','rows','source_binding'},
            'GEN3_TREE_EXPORT':{'name'},
            'GEN3_CONSTRUCTION_PLAN':{'family_ids','source_contract'},
        }
        if operation not in allowed or set(payload)!=allowed[operation]:
            raise ValueError('Supply exactly the declared capability fields')
        if operation == 'GEN3_CONSTRUCTION_PLAN':
            construction=json.loads((HERE/'CONSTRUCTION.json').read_text())
            if payload['source_contract']!=construction['source_contract']:
                raise ValueError('Construction source contract differs')
            rows=self.call('CONSTRUCTION_FEATURES',{'family_ids':payload['family_ids'],
                'feature_table':construction['feature_table'], 'inventory_counts':construction['inventory_counts']})
            name='A3D41_COMMON_MINIMUM'
            result=self.execute('GEN3_TREE_PREDICT',{'name':name,'rows':rows,
                'source_binding':self.package['source_binding'][name]})
            result['family_features']=rows
            result['target']='Common minimum of original contexts 3 and 11'
            return result
        if operation == 'GEN3_TREE_EXPORT':
            row=deepcopy(self.model(payload['name']))
            return {'record':row,'sha256':digest(row)}
        source=payload['source_binding']
        if not isinstance(source,dict) or not source:
            raise ValueError('Explicit source binding required')
        if operation == 'GEN3_TREE_FIT':
            name=payload['name']
            if not isinstance(name,str) or not name or len(name)>128:
                raise ValueError('Nonempty model identity of at most 128 characters required')
            if name in self.package['models'] or 'capability:model:'+name in self.machine.origins:
                raise ValueError('Retain prior model; use a new successor identity')
            for row in payload['rows']:
                if not isinstance(row,dict) or set(row)!={'features','label','split','witness'} or not row['witness']:
                    raise ValueError('Each learning row needs features, label, split and witness')
            result=self.call('TREE_FIT',{'rows':payload['rows']})
            record={'name':name,'source_binding':source,'model':result,
                    'training_input_sha256':digest(payload['rows']),
                    'origin':'NATIVE_CLASS_BALANCED_CART_SUCCESSOR'}
            self.remember('capability:model:'+name,record)
            result={'name':name,**result,'model_sha256':digest(record)}
        elif operation == 'GEN3_TREE_PREDICT':
            record=self.model(payload['name'])
            if canonical_bytes(source)!=canonical_bytes(record['source_binding']):
                raise ValueError('Candidate/model source binding differs')
            result=self.call('TREE_PREDICT',{'model':record['model'],'rows':payload['rows']})
            result.update(name=payload['name'],model_sha256=digest(record))
            self.remember('capability:model:'+payload['name'],record)
        else:
            op='SIGNED_ENERGY' if operation=='GEN3_SIGNED_ENERGY' else 'COMMON_MINIMA'
            result=self.call(op,{k:v for k,v in payload.items() if k!='source_binding'})
        record={'operation':operation,'source_binding':source,'payload':deepcopy(payload),
                'result':deepcopy(result),'native_manifest_sha256':digest(self.manifest)}
        self.remember('capability:call:'+digest(record),record)
        self.machine.stats['native_capability_calls']+=1
        result['source_binding']=deepcopy(source)
        result['execution']={'backend':'NATIVE_CPP_GMP_CPU','native_source_manifest':digest(self.manifest),
                             'shared_R3_checkpoint':True}
        return result
