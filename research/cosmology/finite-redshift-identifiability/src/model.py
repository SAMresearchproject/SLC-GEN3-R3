"""Independent implementation of the equations in Brady's 2026-09-25 manuscript."""
import numpy as np
from scipy.linalg import solve_triangular
from scipy.optimize import brentq, minimize_scalar

def curve(s, xi=.9, n=3., calibration=1.04):
    return calibration*(xi+(1-xi)*np.exp(-n*np.asarray(s)))

def design():
    s=np.linspace(np.log1p(.03),np.log(3),24); z=np.expm1(s); mean=curve(s)
    frac=np.sqrt(.02**2+(.0225*z)**2); tail=.004+.004*z
    core=np.sqrt(frac**2-tail**2)
    corr=.8*np.eye(24)+.2*np.exp(-np.abs(s[:,None]-s[None,:])/.12)
    covcore=np.outer(mean*core,mean*core)*corr
    cov=covcore+np.diag((mean*tail)**2)
    return s,z,mean,frac,tail,covcore,cov

def contrasts(s,n):
    t=np.exp(-n*s); r=np.diff(t)[1:]/np.diff(t)[:-1]; A=np.zeros((len(s)-2,len(s)))
    for i,a in enumerate(r):A[i,i:i+3]=[a,-1-a,1]
    return A

class Likelihood:
    def __init__(self,s,cov):
        self.s=s;self.cov=cov;self.L=np.linalg.cholesky(cov)
        self.ones=self.white(np.ones(len(s)));self.e0=self.ones/np.linalg.norm(self.ones)
        self.grid=np.linspace(.25,8,311)
        T=np.exp(-s[:,None]*self.grid);W=solve_triangular(self.L,T,lower=True)
        W-=self.e0[:,None]*(self.e0@W)[None,:];self.Q=W/np.linalg.norm(W,axis=0)
        self.fixed=int(np.argmin(abs(self.grid-3)))
    def white(self,Y):return solve_triangular(self.L,np.asarray(Y).T,lower=True).T
    def fit(self,Y,n=3,t=None):
        t=np.exp(-n*self.s) if t is None else t
        X=np.column_stack([np.ones(len(t)),t]);W=solve_triangular(self.L,X,lower=True)
        pinv=np.linalg.solve(W.T@W,W.T);coef=self.white(Y)@pinv.T
        residual=self.white(Y)-coef@W.T
        return coef,np.sum(residual**2,axis=-1),np.linalg.inv(W.T@W)
    def profile_mean(self,Y):
        f=lambda n:float(self.fit(Y,n)[1])
        opt=minimize_scalar(f,bounds=(.25,8),method='bounded',options={'xatol':1e-12})
        coef,T,V=self.fit(Y,opt.x);return dict(n=float(opt.x),xi=float(coef[0]/sum(coef)),calibration=float(sum(coef)),noncentrality=float(T))
    def statistics(self,Y):
        W=self.white(Y);const=np.sum(W*W,axis=1)-(W@self.e0)**2
        fixed=np.empty(len(Y));profile=np.empty(len(Y))
        for a in range(0,len(Y),2048):
            q=W[a:a+2048]@self.Q;fixed[a:a+2048]=const[a:a+2048]-q[:,self.fixed]**2
            profile[a:a+2048]=const[a:a+2048]-np.max(q*q,axis=1)
        return fixed,profile

def noise(rng,count,mean,tail,covcore):
    G=rng.standard_normal((count,len(mean)))@np.linalg.cholesky(covcore).T
    tau=.75;U=(np.exp(tau*rng.standard_normal(G.shape)-tau*tau/2)-1)/np.sqrt(np.expm1(tau*tau))
    return G+U*(mean*tail)

def recover(s,Y):
    h=np.diff(s);d=np.diff(Y);r=d[1]/d[0]
    if not 0<r<h[1]/h[0]:raise ValueError('Outside positive-exponent admission interval')
    F=lambda n:-np.expm1(-n*h[1])/np.expm1(n*h[0])-r
    n=brentq(F,1e-9,100,xtol=1e-13)
    t=np.exp(-n*s);beta=(Y[0]-Y[1])/(t[0]-t[1]);alpha=Y[0]-beta*t[0]
    return n,alpha/(alpha+beta),alpha+beta

def fisher(s):
    xi,n,C=.9,3.,1.04;t=np.exp(-n*s)
    J=np.column_stack([C*(1-t),-C*(1-xi)*s*t,xi+(1-xi)*t])/.03
    V=np.linalg.inv(J.T@J)
    return dict(sigma_n=float(np.sqrt(V[1,1])),sigma_xi=float(np.sqrt(V[0,0])),covariance=V.tolist())
