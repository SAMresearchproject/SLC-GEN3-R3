"""Verify byte identity of the copied public Courtroom artifacts; no test execution."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'maintenance/COURTROOM_MIRROR.json').read_text())
for row in d['files']:
 b=(R/row['destination']).read_bytes()
 assert len(b)==row['bytes'],row['destination']
 assert hashlib.sha256(b).hexdigest()==row['sha256'],row['destination']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['sha'],row['destination']
assert len(d['files'])==d['file_count']
assert sum(r['bytes'] for r in d['files'])==d['bytes']
print(json.dumps({'status':'PASS','files':d['file_count'],'bytes':d['bytes'],'source_commit':d['source_commit']}))
