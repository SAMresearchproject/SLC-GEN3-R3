"""Source-bound exact weighted cut-cell blocks for the installed RH fabric.

FLINT is the same integer/rational backend as RH native.block. No floats enter
source contractions. Workers have no authority to select research questions.
"""
from pathlib import Path
import concurrent.futures, gzip, hashlib, json, os, socket, sys, time
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
for p in (HERE/'vendor', HERE.parent/'native/vendor'):
    if p.is_dir():sys.path.insert(0,str(p))
from flint import fmpq as Q, ctx
ctx.threads=1

def encode(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def atomic(path,body):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    data=encode(body);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
    fd=os.open(path.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)

def cell_task(job):
    s,t=job['s'],job['t'];history=job.get('history',True);mu=[Q(str(x)) for x in job['source']]
    if len(mu)!=s:raise ValueError('Full source required')
    cpu=job['cpu'];os.sched_setaffinity(0,{cpu});start=time.monotonic()
    dsum=[Q(0) for _ in range(t if history else 0)];fsum=dsum.copy();esum=dsum.copy();cells=[];full=Q(0)
    M=sum(mu[:t],Q(0));prefix=[Q(0)]
    for a in mu[:t]:prefix.append(prefix[-1]+a)
    for c in job['cells']:
        cuts=c['cuts'];l,h=cuts[0],cuts[-1]
        w={r:Q(1,r*(s-r)) for r in cuts};W=sum(w.values(),Q(0));offset=sum((r*w[r] for r in cuts),Q(0))/s
        before=W-offset;after=-offset;suffix=Q(0);beta={}
        for r in reversed(cuts):beta[r]=suffix-offset;suffix+=w[r]
        Z=Q(0);D=Q(0)
        for i,a in enumerate(mu[:t]):
            b=before if i<l else after if i>=h else beta[i]
            d=a*a*b*b/W;f=2*a*Z*b/W;previous=Z*Z/W
            Z+=a*b;E=Z*Z/W;D+=d
            if E-previous != d+f:raise ArithmeticError('Cell signed accumulation identity')
            if history:dsum[i]+=d;fsum[i]+=f;esum[i]+=E
        trace=(l*before*before+(s-h)*after*after+sum((beta[i]*beta[i] for i in range(l,h)),Q(0)))/W
        direct=sum((w[r]*(prefix[min(r,t)]-Q(r,s)*M) for r in cuts),Q(0))
        if direct!=Z:raise ArithmeticError('Cut contraction differs from ordered source')
        full+=sum((w[r]*(prefix[min(r,t)]-Q(r,s)*M)**2 for r in cuts),Q(0))
        cells.append(dict(cell=c['cell'],l=l,h=h,region='POST_STOP' if l>=t else 'PRE_STOP' if h<t else 'STRADDLING',
            energy=str(Z*Z/W),diagonal=str(D),cross=str(Z*Z/W-D),trace=str(trace),W=str(W),Z=str(Z),tail_factor=str(before*before/W)))
    return dict(cells=cells,rows=[[str(d),str(f),str(e)] for d,f,e in zip(dsum,fsum,esum)],full=str(full),
        telemetry=dict(host=socket.gethostname(),pid=os.getpid(),cpu=cpu,seconds=time.monotonic()-start,cells=len(cells),admissions=t),
        worker_sha256=sha(Path(__file__).read_bytes()))

def batch(request):
    cpus=request['cpus'];groups=[[] for _ in cpus];loads=[0]*len(cpus)
    if not cpus:raise ValueError('No admitted CPU workers')
    for cell in sorted(request['cells'],key=lambda c:len(c['cuts']),reverse=True):
        i=min(range(len(cpus)),key=lambda k:loads[k]);groups[i].append(cell);loads[i]+=len(cell['cuts'])+request['t']
    jobs=[dict(s=request['s'],t=request['t'],source=request['source'],cells=g,cpu=cpu,history=request.get('history',True)) for cpu,g in zip(cpus,groups) if g]
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(jobs)) as pool:
        parts=list(pool.map(cell_task,jobs))
    return dict(status='PASS',request_sha256=sha(encode(request)),parts=parts)

def main():
    request=json.load(sys.stdin);result=batch(request)
    if request.get('output'):
        p=Path(request['output']);p.parent.mkdir(parents=True,exist_ok=True)
        import shutil
        if shutil.disk_usage(p.parent).free < 20*2**30+len(encode(result))*2:raise RuntimeError('T500 reserve reached')
        if p.exists():raise ValueError('Immutable worker output already exists')
        atomic(p,result)
        if sha(p.read_bytes())!=sha(encode(result)):raise ValueError('Worker durable readback differs')
        result['custody']={'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'fsync_and_readback':True}
    print(json.dumps(result,separators=(',',':')),flush=True)
if __name__=='__main__':main()
