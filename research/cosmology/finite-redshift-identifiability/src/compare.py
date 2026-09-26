"""Compare independent results with the transcribed manuscript; retain discrepancies."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
import argparse,json
from pathlib import Path
import numpy as np
from scipy.stats import norm
from model import design,Likelihood

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);args=p.parse_args();run=args.run
    root=Path(__file__).resolve().parents[1];reported=json.loads((root/'paper/reported_results.json').read_text());table=json.loads((run/'results/table_i.json').read_text());ext=json.loads((run/'results/extended.json').read_text())
    s,z,mu,f,tail,core,cov=design();corr=.8*np.eye(24)+.2*np.exp(-abs(s[:,None]-s[None,:])/.12)
    variants={};h=np.minimum(.015+.22*(s/s[-1])**2,.8*s);yb=1.04*(.9+.1*np.exp(-3*s)*np.sinh(3*h)/(3*h))
    for name,S in [('declared_equations_69_to_72',cov),('diagnostic_f_in_correlated_core_without_separate_tail',np.outer(mu*f,mu*f)*corr)]:
        lk=Likelihood(s,S);_,_,V=lk.fit(mu);a=.936;C=1.04;k=norm.ppf(.975)
        roots=np.sort(np.roots([C*C-k*k*V.sum(),-2*a*C+2*k*k*(V[0,0]+V[0,1]),a*a-k*k*V[0,0]]))
        variants[name]=dict(sigma_C=float(np.sqrt(V.sum())),fieller_interval=roots.tolist(),binning_fit=lk.profile_mean(yb))
        np.savetxt(run/f'data/covariance_{name}.csv',S,delimiter=',')
    rows=[]
    for old,new in zip(reported['table_i']['rows'],table['rows']):
        row={'case':new['case'],'n_difference':new['noiseless_fit']['n']-old['n'],'xi_difference':new['noiseless_fit']['xi']-old['xi']}
        for key in ['fixed_rejection_rate','profile_rejection_rate']:
            p0=old[key];p1=new[key];se=np.sqrt((p0*(1-p0)+p1*(1-p1))/new['catalogs'])
            row[key]=dict(reported=p0,independent=p1,difference=p1-p0,conditional_two_sample_standard_error=float(se),note='Descriptive only: excludes finite calibration-threshold uncertainty; original draw ordering is unknown.')
        rows.append(row)
    out=dict(status='INDEPENDENT_REIMPLEMENTATION_WITH_UNRESOLVED_HISTORICAL_COVARIANCE_DISCREPANCY',table_i=rows,covariance_diagnostic=variants,interpretation='The alternative covariance matches the reported rounded deterministic Fieller and binning numbers. This is evidence of a specification/output discrepancy, not proof of which code the original author executed. Main outputs keep the explicitly declared covariance.',historical_hankel_comparison='Not directly comparable: original five-point grid not specified.',monte_carlo_note='A seed alone does not specify a random stream: generator, draw order, covariance, and implementation also matter. No original bitwise replication claim.',independent_fieller_coverage=ext['fieller']['coverage'])
    (run/'results/comparison.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out['covariance_diagnostic'],indent=2))
if __name__=='__main__':main()
