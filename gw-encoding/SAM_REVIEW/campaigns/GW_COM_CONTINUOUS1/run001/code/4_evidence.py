"""Immutable evidence records with readable, hash-checked ancestry."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def encode(value):
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


class Store:
    def __init__(self, root, directory, method, units=None):
        self.root = Path(root).resolve()
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True,exist_ok=True)
        self.method = self.ref(method)
        self.units = units or {'time':'discrete ticks','amplitude':'dimensionless signed Qxx-Qyy second difference',
                              'channel':'single C4 projected channel; not calibrated detector strain'}

    def ref(self, path):
        path = Path(path).resolve()
        return {'path':str(path.relative_to(self.root)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

    def write(self, name, value):
        path = self.directory/(name+'.json')
        with path.open('xb') as f:
            f.write(encode(value))
        return self.ref(path)

    def record(self, name, kind, payload, parents=(), execution=(), status='COMPLETE'):
        artifact = self.write(name+'.data',payload)
        return self.write(name, {'schema':'GW_COM_EVIDENCE_V1','schema_version':1,
            'record_id':name,'kind':kind,'created_utc':datetime.now(timezone.utc).isoformat(),
            'campaign_id':str(self.directory.parent.relative_to(self.root)),
            'parent_refs':list(parents),'artifact_refs':[artifact], 'method_ref':self.method,
            'parameters':{'configuration_in_payload':True},
            'units_and_conventions':self.units,
            'execution_refs':[self.ref(p) for p in execution], 'status':status})

    def read(self, ref):
        path = (self.root/ref['path']).resolve()
        path.relative_to(self.root)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=ref['sha256']:
            raise ValueError('Evidence hash mismatch: '+ref['path'])
        return json.loads(raw)

    def payload(self, ref):
        record = self.read(ref)
        return self.read(record['artifact_refs'][0])

    def verify(self, ref, seen=None):
        seen = set() if seen is None else seen
        key = (ref['path'],ref['sha256'])
        if key in seen:
            return
        seen.add(key)
        path = (self.root/ref['path']).resolve()
        path.relative_to(self.root)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=ref['sha256']:
            raise ValueError('Evidence hash mismatch: '+ref['path'])
        if path.suffix!='.json':
            return
        record = json.loads(raw)
        if not isinstance(record,dict):
            return
        if record.get('schema')=='GW_COM_EVIDENCE_V1':
            for link in record['parent_refs']+record['artifact_refs']+record['execution_refs']+[record['method_ref']]:
                self.verify(link,seen)
        elif record.get('schema')=='GW_COM_METHOD_V1':
            for link in record['refs']:
                self.verify(link,seen)
        elif record.get('status')=='RETURNED' and 'input_sha256' in record:
            for name,key in [('INPUT.json','input_sha256'),('OUTPUT.json','output_sha256')]:
                p=path.parent/name
                if hashlib.sha256(p.read_bytes()).hexdigest()!=record[key]:
                    raise ValueError('Native call record differs')
