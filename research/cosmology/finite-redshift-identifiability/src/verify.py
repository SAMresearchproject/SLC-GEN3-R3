"""Verify archived bytes and optionally compare a fresh independent replay."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def compare(a,b,path=''):
    if isinstance(a,dict):
        if set(a)!=set(b):raise AssertionError(f'{path}: keys differ')
        for k in a:compare(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        if len(a)!=len(b):raise AssertionError(f'{path}: lengths differ')
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+f'/{i}')
    elif isinstance(a,(int,float)) and not isinstance(a,bool):
        np.testing.assert_allclose(a,b,rtol=1e-7,atol=1e-10,err_msg=path)
    elif a!=b:raise AssertionError(f'{path}: values differ')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--replay',type=Path);args=ap.parse_args();count=0
    for line in (ROOT/'HASHES.sha256').read_text().splitlines():
        expected,name=line.split('  ',1);p=ROOT/name
        if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise AssertionError(f'Hash mismatch: {name}')
        count+=1
    ex=json.loads((ROOT/'records/execution.json').read_text())
    for name,h in ex['source_sha256'].items():
        if hashlib.sha256((ROOT/'src'/name).read_bytes()).hexdigest()!=h:raise AssertionError(f'Execution source differs: {name}')
    files=arrays=0
    if args.replay:
        for p in sorted((ROOT/'data').glob('*.npz')):
            with np.load(p,allow_pickle=False) as a,np.load(args.replay/'data'/p.name,allow_pickle=False) as b:
                if set(a.files)!=set(b.files):raise AssertionError(f'Array keys differ: {p.name}')
                for k in a.files:
                    np.testing.assert_allclose(a[k],b[k],rtol=1e-7,atol=1e-10,err_msg=f'{p.name}/{k}');arrays+=1
            files+=1
        for p in sorted((ROOT/'results').glob('*.json')):
            compare(json.loads(p.read_text()),json.loads((args.replay/'results'/p.name).read_text()),p.name);files+=1
        for p in sorted((ROOT/'data').glob('*.csv')):
            skip=1 if p.name=='design.csv' else 0
            np.testing.assert_allclose(np.loadtxt(p,delimiter=',',skiprows=skip),np.loadtxt(args.replay/'data'/p.name,delimiter=',',skiprows=skip),rtol=1e-7,atol=1e-10);files+=1
    print(json.dumps(dict(status='PASS',manifest_files=count,replay_files=files,replay_npz_arrays=arrays,rtol=1e-7,atol=1e-10),indent=2))
if __name__=='__main__':main()
