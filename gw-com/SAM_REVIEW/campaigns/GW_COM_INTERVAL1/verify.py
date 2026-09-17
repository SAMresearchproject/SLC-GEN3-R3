"""Independent saved-artifact and isolated-receiver verification."""
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
release = HERE/'release'
manifest = json.loads((release/'MANIFEST.json').read_text())
for name, expected in manifest.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name

with tempfile.TemporaryDirectory() as folder:
    temp = Path(folder)
    (temp/'receiver.py').write_bytes((HERE/'receiver.py').read_bytes())
    # Fresh subprocess receives only receiver source and the wave JSON on stdin.
    command = [sys.executable, '-c',
               'import json,sys; from receiver import decode; print(json.dumps(decode(json.load(sys.stdin)["wave_samples"])))']
    actual = {}
    for name in ('prime', 'unmodulated', 'alternate'):
        p = subprocess.run(command, cwd=temp, input=(release/(name+'_receiver_input.json')).read_text(),
                           text=True, capture_output=True, check=True, env={'PATH': '/usr/bin:/bin'})
        actual[name] = json.loads(p.stdout)
    assert [p['intervals'] for p in actual['prime']['packets']] == [[2,5,7,11,13,17]]*2
    assert actual['unmodulated']['packets'] == []
    assert [p['intervals'] for p in actual['alternate']['packets']] == [[4,6,8,10,12,14]]*2

rows = list(csv.DictReader((release/'source_wave.csv').open()))
q = [2*(F(row['x_plus'])**2-F(row['y_plus'])**2) for row in rows]
for i in range(1, len(rows)-1):
    assert q[i-1]-2*q[i]+q[i+1] == F(rows[i]['signed_quadrupole_second_difference'])
result = json.loads((release/'RESULT.json').read_text())
assert actual == result['decoded']
assert result['noise_trials_recovered'] == 20
receipt_paths = sorted((ROOT/result['session']/'calls').glob('*/RECEIPT.json'))
assert len(receipt_paths) == 1
receipt = json.loads(receipt_paths[0].read_text())
assert receipt['status']=='RETURNED' and receipt['operation']=='GEN2_SIGNED_LOG'
report = {'status':'PASS', 'manifest_hashes_checked':len(manifest),
          'independent_saved_wave_stencils_checked':len(rows)-2,
          'isolated_receiver_cases':3, 'native_receipt':str(receipt_paths[0].relative_to(ROOT)),
          'scope':'Exact saved waveform reconstruction, custody hashes, and fresh-process receiver isolation.'}
folder = HERE/'verification'
folder.mkdir(exist_ok=True)
with (folder/'VALIDATION.json').open('x') as f:
    json.dump(report,f,indent=2); f.write('\n')
print(json.dumps(report,indent=2))
