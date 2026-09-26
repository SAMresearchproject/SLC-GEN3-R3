"""Run independent manuscript replication. Outputs never claim historical custody."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,time
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import numpy as np
import scipy,sympy,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import chi2,norm
from model import *
ROOT=Path(__file__).resolve().parents[1]
def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--quick',action='store_true');args=ap.parse_args();out=args.output
    if out.exists() and any(out.iterdir()):raise SystemExit('Choose an empty output directory; preserve completed records')
    for name in ['data','results','figures','records']:(out/name).mkdir(parents=True,exist_ok=True)
    started=time.monotonic();s,z,mu,frac,tail,core,cov=design();lk=Likelihood(s,cov)
    nc,nt,ne=(300,200,1000) if args.quick else (30000,20000,100000)
    nh=2000 if args.quick else 200000
    arrays=dict(s=s,z=z,fiducial_mean=mu,fractional_sigma=frac,lensing_rms=tail,covariance_core=core,covariance_total=cov,exponent_grid=lk.grid)
    np.savez_compressed(out/'data/design.npz',**arrays)
    np.savetxt(out/'data/design.csv',np.column_stack([z,s,mu,frac,tail]),delimiter=',',header='z,s,mean,fractional_sigma,lensing_rms',comments='')
    np.savetxt(out/'data/covariance_total.csv',cov,delimiter=',')
    rng=np.random.default_rng(20260927);Y0=mu+noise(rng,nc,mu,tail,core);f0,p0=lk.statistics(Y0);critical=[float(np.quantile(f0,.95)),float(np.quantile(p0,.95))]
    np.savez_compressed(out/'data/calibration_catalogs.npz',catalogs=Y0,fixed=f0,profile=p0)
    cases=[('single_power',mu),('constant_gain_096',curve(s,calibration=.96)),('second_power',1.04*(.9+.07*np.exp(-3*s)+.03*np.exp(-.5*s))),('calibration_drift',mu*np.exp(.01*s)),('localized_departure',mu+1.04*.015*np.exp(-(s-.60)**2/(2*.09**2)))]
    rows=[];residuals=[]
    for name,mean in cases:
        Y=mean+noise(rng,nt,mu,tail,core);fixed,prof=lk.statistics(Y);coef,_,_=lk.fit(Y);xi=coef[:,0]/coef.sum(axis=1);fit=lk.profile_mean(mean)
        rows.append(dict(case=name,catalogs=nt,fixed_rejections=int(sum(fixed>critical[0])),profile_rejections=int(sum(prof>critical[1])),fixed_rejection_rate=float(np.mean(fixed>critical[0])),profile_rejection_rate=float(np.mean(prof>critical[1])),fixed_xi_mean=float(np.mean(xi)),fixed_xi_sd=float(np.std(xi,ddof=1)),noiseless_fit=fit))
        np.savez_compressed(out/f'data/{name}_catalogs.npz',catalogs=Y,mean=mean,fixed=fixed,profile=prof,xi_fixed=xi)
        residuals.append((name,(mean-curve(s,fit['xi'],fit['n'],fit['calibration']))/np.sqrt(np.diag(cov))))
    # Declared fixed-n calibration constraint: C=1, n=3.
    t=np.exp(-3*s);v=lk.white(1-t);w=lk.white(mu-t);forced=float(v@w/(v@v));noncentral=float(np.sum((w-forced*v)**2))
    save(out/'results/table_i.json',dict(provenance='INDEPENDENT_REIMPLEMENTATION_NOT_ORIGINAL_RUN',seed=20260927,bit_generator='PCG64',draw_order='calibration then five cases in listed order; Gaussian matrix then lognormal matrix within each call',calibration_catalogs=nc,critical_values=critical,rows=rows,forced_C1_fixed_n3=dict(xi=forced,noncentrality=noncentral)))
    # Independent Gaussian checks, as required by the exact normal-theory pivots.
    rng=np.random.default_rng(20260926);Y=mu+rng.standard_normal((ne,24))@lk.L.T;coef,_,V=lk.fit(Y);C=coef.sum(axis=1);pivot_var=V[0,0]-2*.9*(V[0,0]+V[0,1])+.9**2*V.sum();pivot=(coef[:,0]-.9*C)/np.sqrt(pivot_var)
    alpha=1.04*.9;c=1.04;k=norm.ppf(.975);roots=np.sort(np.roots([c*c-k*k*V.sum(),-2*alpha*c+2*k*k*(V[0,0]+V[0,1]),alpha*alpha-k*k*V[0,0]]))
    fieller=dict(catalogs=ne,coverage=float(np.mean(abs(pivot)<=k)),noiseless_interval=roots.tolist(),sigma_C=float(np.sqrt(V.sum())))
    # Gaussian finite-grid search calibration; null location cancels analytically.
    ns=nt;wc=rng.standard_normal((ns,24));we=rng.standard_normal((ns,24));scan_c=np.max((wc@lk.Q)**2,axis=1);scan_e=np.max((we@lk.Q)**2,axis=1);cut=float(np.quantile(scan_c,.95));p_mc=(1+ns-np.searchsorted(np.sort(scan_c),scan_e,side='left'))/(ns+1)
    scan=dict(calibration_catalogs=ns,evaluation_catalogs=ns,threshold=cut,calibrated_rejection=float(np.mean(scan_e>cut)),rank_p_rejection=float(np.mean(p_mc<=.05)),single_exponent_threshold=float(chi2.ppf(.95,1)),incorrect_single_threshold_rejection=float(np.mean(scan_e>chi2.ppf(.95,1))))
    # Correlated held-out prediction, equations63--67.
    X=np.column_stack([np.ones(24),t]);TT=cov[:16,:16];HT=cov[16:,:16];K=np.linalg.solve(TT,HT.T).T;VT=np.linalg.inv(X[:16].T@np.linalg.solve(TT,X[:16]));BH=X[16:]-K@X[:16];VH=cov[16:,16:]-K@HT.T+BH@VT@BH.T
    Yh=mu+rng.standard_normal((ne,24))@lk.L.T;theta=Yh[:,:16]@np.linalg.solve(TT,X[:16])@VT;pred=Yh[:,:16]@K.T+theta@BH.T;err=Yh[:,16:]-pred;stats=np.sum(err*np.linalg.solve(VH,err.T).T,axis=1)
    heldout=dict(catalogs=ne,mean_statistic=float(np.mean(stats)),degrees_of_freedom=8,rejection=float(np.mean(stats>chi2.ppf(.95,8))))
    # Five equally spaced log-redshift points are an explicit independent choice;
    # the paper does not identify its historical Hankel grid.
    sh=np.linspace(s[0],s[-1],5);mh=curve(sh);Sig=.03**2*np.eye(5);D=np.diff(np.eye(5),axis=0);B=np.array([[0,0,.5],[0,-1,0],[.5,0,0]]);Qs=[D[i:i+3].T@B@D[i:i+3] for i in [0,1]]
    means=np.array([mh@Q@mh for Q in Qs]);bias=np.array([np.trace(Q@Sig) for Q in Qs]);Hcov=np.array([[2*np.trace(Q@Sig@R@Sig)+4*mh@Q@Sig@R@mh for R in Qs] for Q in Qs]);draw=mh+.03*rng.standard_normal((nh,5));raw=np.column_stack([np.einsum('ni,ij,nj->n',draw,Q,draw) for Q in Qs]);corrected=raw-bias
    hankel=dict(catalogs=nh,s=sh.tolist(),grid_provenance='Independent declared grid; historical grid unspecified in PDF',true_determinants=means.tolist(),raw_bias_theory=bias.tolist(),raw_bias_empirical=(raw.mean(axis=0)-means).tolist(),corrected_mean=corrected.mean(axis=0).tolist(),covariance_theory=Hcov.tolist(),covariance_empirical=np.cov(corrected,rowvar=False).tolist(),correlation_theory=float(Hcov[0,1]/np.sqrt(Hcov[0,0]*Hcov[1,1])),correlation_empirical=float(np.corrcoef(corrected,rowvar=False)[0,1]))
    np.savez_compressed(out/'data/extended_statistics.npz',fieller_pivot=pivot,scan_calibration=scan_c,scan_evaluation=scan_e,scan_rank_p=p_mc,heldout_statistic=stats,hankel_raw=raw,hankel_corrected=corrected)
    save(out/'results/extended.json',dict(provenance='INDEPENDENT_REIMPLEMENTATION_NOT_ORIGINAL_RUN',seed=20260926,Gaussian_assumption=True,fieller=fieller,constant_null_scan=scan,heldout=heldout,hankel=hankel))
    # Matched information designs, TableII.
    designs={'low_only':np.linspace(np.log1p(.03),np.log1p(.35),24),'broad':s,'high_only':np.linspace(np.log(2),np.log(4),24),'three_bands':np.concatenate([np.linspace(np.log1p(a),np.log1p(b),8) for a,b in [(.03,.12),(.3,.6),(1,2)]])}
    fish={name:fisher(ss) for name,ss in designs.items()};save(out/'results/table_ii.json',fish)
    h=np.minimum(.015+.22*(s/s[-1])**2,.8*s);tb=np.exp(-3*s)*np.sinh(3*h)/(3*h);binned=1.04*(.9+.1*tb);coefb,_,_=lk.fit(binned,t=tb)
    save(out/'results/binning.json',dict(halfwidth_s=h.tolist(),exact_bin_design=tb.tolist(),mean=binned.tolist(),point_center_fit=lk.profile_mean(binned),window_aware_xi=float(coefb[0]/sum(coefb)),window_aware_C=float(sum(coefb))))
    # Deterministic exact/near-exact mathematical checks.
    maxerr=0.;maxfour=0.;sr=np.log1p([.07,.47,1.83]);sf=np.log1p([.07,.47,1.1,1.83]);count=0
    for n in [.25,.5,1,2,3,5]:
      for xi in [.7,.9,1.1,1.3]:
       for cal in [.96,1,1.04]:
        got=recover(sr,curve(sr,xi,n,cal));maxerr=max(maxerr,float(np.max(abs(np.array(got)-[n,xi,cal]))));count+=1
        yy=curve(sf,xi,n,cal);maxfour=max(maxfour,abs(recover(sf[:3],yy[:3])[0]-recover(sf[1:],yy[1:])[0]))
    A=contrasts(s,3);sample=cases[-1][1];res=A@sample;Tcontrast=float(res@np.linalg.solve(A@cov@A.T,res));Tgls=float(lk.fit(sample)[1]);sys=.01**2*np.outer(mu,mu);sys_res=float(np.max(abs(A@sys@A.T)))
    a,b,l,r=sympy.symbols('a b l r');vals=[a*l**j+b*r**j for j in range(4)];ds=[vals[i+1]-vals[i] for i in range(3)];symbolic=sympy.expand(ds[0]*ds[2]-ds[1]**2-a*b*(l-1)*(r-1)*(l-r)**2)==0
    checks=dict(irregular_parameter_cases=count,parameter_grid_provenance='Independent72-case grid; original72 choices not specified',maximum_parameter_error=maxerr,maximum_shared_exponent_error=maxfour,contrast_GLS_difference=abs(Tcontrast-Tgls),common_gain_contrast_covariance_max=sys_res,two_power_Hankel_symbolic_identity=bool(symbolic))
    assert maxerr<1e-9 and maxfour<1e-9 and abs(Tcontrast-Tgls)<1e-9 and sys_res<1e-15 and symbolic
    save(out/'results/deterministic_checks.json',checks)
    # Figures are newly rendered; their original source files were not recovered.
    zz=np.linspace(0,2,500);ss=np.log1p(zz);fig,ax=plt.subplots(1,2,figsize=(9,3));q1=.9+.1*np.exp(-3*ss);q2=.85+.1*np.exp(-3*ss)+.05*np.exp(-.01*ss);ax[0].plot(zz,q1,label='Q1');ax[0].plot(zz,q2,label='Q2');zl=np.linspace(0,.2,500);base=curve(np.log1p(zl));ax[1].plot(zl,base,label='Y1');ax[1].plot(zl,base+.04*np.exp(-400*np.log1p(zl)),label='Y2');ax[1].axvline(.03,ls=':',color='k')
    for aa in ax:aa.set_xlabel('Redshift z');aa.legend()
    fig.tight_layout();fig.savefig(out/'figures/figure_1_endpoint_constructions.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots();
    for xi,n in [(.9,3),(.9,1),(1.1,3)]:ax.plot(zz,curve(ss,xi,n,1),label=f'Xi0={xi}, n={n}')
    ax.legend();ax.set(xlabel='Redshift z',ylabel='Distance ratio');fig.tight_layout();fig.savefig(out/'figures/figure_2_ratio_families.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots()
    for name,r in residuals[2:]:ax.plot(z,r,label=name)
    ax.legend();ax.set(xlabel='Redshift z',ylabel='Residual / marginal sigma');fig.tight_layout();fig.savefig(out/'figures/figure_3_residuals.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots();sx=np.sort(scan_c);ax.plot(sx,np.arange(1,ns+1)/ns,label='Independent finite-grid null');xx=np.linspace(0,12,500);ax.plot(xx,chi2.cdf(xx,1),label='One specified exponent');ax.axvline(cut,ls=':');ax.set(xlim=(0,12),xlabel='Improvement',ylabel='CDF');ax.legend();fig.tight_layout();fig.savefig(out/'figures/figure_4_scan_null.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots();ax.bar(list(fish),[fish[k]['sigma_n'] for k in fish]);ax.set_yscale('log');ax.set_ylabel('Marginal sigma_n');fig.tight_layout();fig.savefig(out/'figures/figure_5_fisher.png',dpi=180);plt.close(fig)
    src={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}
    save(out/'records/execution.json',dict(role='Independent manuscript replication, not an original SLC/GEN4 science receipt',started_and_completed='This process generated all files under its output directory',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=sympy.__version__,matplotlib=matplotlib.__version__,source_sha256=src,quick=args.quick,elapsed_seconds=time.monotonic()-started,command='python src/reproduce.py --output <empty-directory>'+(' --quick' if args.quick else ''),original_supplement_recovered=False))
    print(json.dumps(dict(output=str(out),critical_values=critical,checks=checks,seconds=time.monotonic()-started),indent=2))
if __name__=='__main__':main()
