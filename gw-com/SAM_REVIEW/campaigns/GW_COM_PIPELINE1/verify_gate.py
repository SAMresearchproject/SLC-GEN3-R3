"""Supplemental current-gate checks against the preserved run, without refitting."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from GW_COM.runtime.evidence import Store,encode
from GW_COM.runtime.decoder import admission,decode


def main():
    run=HERE/(sys.argv[1] if len(sys.argv)>1 else 'run001')
    target=run/'gate_verification'
    target.mkdir(exist_ok=False)
    refs=[]
    for path in [ROOT/'GW_COM/runtime/decoder.py',ROOT/'GW_COM/runtime/evidence.py',ROOT/'GW_COM/tests/test_decoder_gate.py']:
        dst=target/path.name;shutil.copyfile(path,dst)
        refs.append({'path':str(dst.relative_to(ROOT)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
    method=target/'METHOD.json';method.write_bytes(encode({'schema':'GW_COM_METHOD_V1','refs':refs}))
    store=Store(ROOT,target/'records',method)
    original=Store(ROOT,run/'records',run/'METHOD.json')
    result=json.loads((run/'records/RUN_RESULT.json').read_text())
    checked=[]
    for name,case in result['cases'].items():
        prior=original.payload(case['admission'])
        current=admission(store,name+'.admission',prior['lineage'],prior['controls'])
        assert store.payload(current)['eligible']==case['admitted']
        if case['admitted']:
            out=decode(store,name+'.decoded',current)
            assert store.payload(out)==original.payload(case['decoded_hypothesis'])
        else:
            try:decode(store,name+'.blocked',current)
            except ValueError:pass
            else:raise AssertionError('Gate bypass')
        checked.append(name)
    test=subprocess.run([sys.executable,'-m','unittest','discover','-s','GW_COM/tests','-v'],
                        cwd=ROOT,capture_output=True,text=True)
    (target/'TEST_OUTPUT.txt').write_text(test.stdout+test.stderr)
    if test.returncode:raise RuntimeError('Gate tests failed; see retained TEST_OUTPUT.txt')
    report={'status':'PASS','cases_rechecked':checked,'gate_tests':9,
            'change':'Explicit rejection of incomplete stage records and missing individual control evidence; saved numerical outcomes unchanged.',
            'new_native_computation':False}
    (target/'VALIDATION.json').write_bytes(encode(report))
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
