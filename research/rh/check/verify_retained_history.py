"""Independent exact check of exported GEN3 results; Python is not the native producer."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import argparse, gzip, hashlib, json, sys
sys.set_int_max_str_digits(0)
class Kernel:
    def __init__(self,s):
        self.s=s; self.L=lcm(*range(1,s)); self.H=[0]*s
        for j in range(1,s):self.H[j]=self.H[j-1]+self.L//j
        self.den=self.L*s*s
    def add(self,z,j,a):
        M,W,Q=z; head=self.L+self.s*(2*self.H[-1]-self.H[j]); diag=head-self.s*self.H[self.s-j-1]
        return M+a,W+a*self.H[self.s-j-1],Q+2*a*(head*M-self.s*W)+a*a*diag

def squarefree_choices(n):
    d=2
    while d*d<=n:
        if n%(d*d)==0:return (0,)
        d+=1
    return (-1,1)

def certificate(p):
    s,t=p['s'],p['t']; a=p['parent_prefix'];g=p['odd_child_prefix']
    assert len(a)==len(g)==t and all(x in (-1,0,1) for x in a+g)
    k=Kernel(s);za=zv=(0,0,0)
    for j,(alpha,gamma) in enumerate(zip(a,g)):
        beta=(alpha if (s+j)%2==0 else 0)+gamma
        za=k.add(za,j,alpha);zv=k.add(zv,j,beta-alpha)
    start=zv[2]-2*za[2]; assert F(start,2*k.den)==F(p['expected_current_E'])
    horizon=min(4,s-t); upper=0;terminal=[];nodes=0
    def visit(za,zv,j):
        nonlocal upper,nodes
        change=zv[2]-2*za[2]-start;upper=max(upper,change)
        if j==t+horizon:terminal.append(change);return
        n=s+j
        for alpha in squarefree_choices(n):
            for gamma in squarefree_choices(2*n+1):
                nodes+=1;beta=(alpha if n%2==0 else 0)+gamma
                visit(k.add(za,j,alpha),k.add(zv,j,beta-alpha),j+1)
    visit(za,zv,t)
    result={'horizon':horizon,'support_branches':len(terminal),'nodes':nodes,'overshoot_bound':F(upper,2*k.den),'drift_lower':F(min(terminal),2*k.den),'drift_upper':F(max(terminal),2*k.den),'E_upper':F(start+upper,2*k.den)}
    expected=p['expected_certificate']
    for key,value in result.items():assert value==F(expected[key]),(t,key)
    return {'s':s,'t':t,'status':'PASS','branches':len(terminal),'E_upper':str(result['E_upper']),'future_sign_input_count':0}

def coverage(path):
    raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()=='4313557d89fa97e51d8c283fafa0f24eac5f81d11edbc28baddbf33944839ff5'
    with gzip.open(path,'rt') as f:data=json.load(f)
    assert data['s']==8192 and data['prefixes']==8193
    # Rebuild the complete scan in admission order. Evaluate signs only at
    # the current admission, never from a suffix table or future outcome.
    def mobius_at(n):
        sign=1;d=2
        while d*d<=n:
            if n%d==0:
                n//=d;sign=-sign
                if n%d==0:return 0
            d+=1
        return -sign if n>1 else sign
    scale=data['s']; k=Kernel(scale); fine=Kernel(2*scale)
    za=zb=zv=zf=(0,0,0); source_a=[0]*scale;source_b=[0]*scale;source_f=[0]*(2*scale)
    witnesses={w['t']:w for w in data['witnesses']};source_checks=0
    def equals_scaled(numerator,denominator,record):
        top,slash,bottom=str(record).partition('/')
        return numerator*int(bottom or '1')==int(top)*denominator
    for t,row in enumerate(data['compact_prefixes']):
        assert row['t']==t
        if t:
            j=t-1;n=scale+j;alpha=mobius_at(n);gamma=mobius_at(2*n+1)
            even=-alpha if n%2 else 0;beta=(alpha if n%2==0 else 0)+gamma
            source_a[j]=alpha;source_b[j]=beta;source_f[2*j]=even;source_f[2*j+1]=gamma
            za=k.add(za,j,alpha);zb=k.add(zb,j,beta);zv=k.add(zv,j,beta-alpha)
            zf=fine.add(fine.add(zf,2*j,even),2*j+1,gamma)
        assert equals_scaled(za[2],k.den,row['Q_a'])
        assert equals_scaled(zv[2]-za[2],2*k.den,row['A'])
        assert equals_scaled(zv[2]-2*za[2],2*k.den,row['excess'])
        source_checks+=3
        if t in witnesses:
            w=witnesses[t]
            assert equals_scaled(zf[2],fine.den,w['Q_fine'])
            assert equals_scaled(zb[2],k.den,w['Q_b'])
            assert equals_scaled(zv[2],k.den,w['Q_v'])
            for values,key in [(source_a,'a_sha256'),(source_b,'b_sha256'),(source_f,'fine_source_sha256')]:
                encoded=''.join(str(v)+',' for v in values).encode()
                assert hashlib.sha256(encoded).hexdigest()==w[key]
            source_checks+=6
    checks=0
    for w in data['witnesses']:
        q={key:F(w[key]) for key in ['Q_a','Q_b','inner_ab','A','S','S_sos','I','epsilon','R','Q_fine','excess','mean_forcing','cut_forcing']}
        assert q['A']==q['Q_b']/2-q['inner_ab']
        assert q['Q_fine']==q['Q_a']+q['excess']+q['R']
        assert q['R']==-q['S']+q['I']+q['epsilon']<=3
        assert q['S']==q['S_sos']>=0
        assert q['excess']==q['A']-q['Q_a']/2
        assert q['A']==q['mean_forcing']+q['cut_forcing']
        p=w['parity_causes'];assert q['A']==F(p['Q_even'])/2+F(p['Q_odd'])/2+F(p['even_odd_inner'])-F(p['a_even_inner'])-F(p['a_odd_inner'])
        checks+=7
    return {'status':'PASS','prefixes':data['prefixes'],'witnesses':len(data['witnesses']),'exact_transport_checks':checks,'source_reconstruction_checks':source_checks,'scope':'All 8193 original prefix energies and excesses rebuilt in admission order; fine energy and source hashes rebuilt at each witness; transport identities checked exactly'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--coverage',type=Path);args=parser.parse_args()
    packets=json.loads((Path(__file__).parent/'PREFIX_CERTIFICATES.json').read_text())['packets']
    results=[certificate(p) for p in packets]
    output={'role':'Independent exact public reconstruction','certificates':[{k:v for k,v in row.items() if k!='E_upper'} for row in results],'native_exact_bounds_matched':True}
    if args.coverage:output['scale8192']=coverage(args.coverage)
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
