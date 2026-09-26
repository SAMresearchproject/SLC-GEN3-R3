"""Independent algebraic and numerical controls; no stochastic pass/fail gates."""
import sys,unittest
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import curve,design,contrasts,Likelihood,recover,fisher

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.s,self.z,self.mu,self.f,self.tail,self.core,self.cov=design()
        self.lk=Likelihood(self.s,self.cov)
    def test_declared_marginal_variance(self):
        np.testing.assert_allclose(np.diag(self.cov),(self.mu*self.f)**2,rtol=1e-14)
        self.assertGreater(np.linalg.eigvalsh(self.cov)[0],0)
    def test_design_endpoint_parameters(self):
        self.assertAlmostEqual(curve(0),1.04)
        self.assertAlmostEqual(curve(100),.936)
    def test_slow_mode_bound(self):
        s=np.linspace(0,4,301);a=.1;b=.05;eps=.003
        q1=1-a+a*np.exp(-3*s);q2=1-a-b+a*np.exp(-3*s)+b*np.exp(-eps*s)
        self.assertLessEqual(np.max(abs(q1-q2)),b*eps*max(s))
        self.assertAlmostEqual((1-a)-(1-a-b),b)
    def test_fast_mode_bound(self):
        s=np.linspace(.03,4,301);d=.04;N=400
        self.assertLessEqual(np.max(abs(d*np.exp(-N*s))),abs(d)*np.exp(-N*s[0]))
    def test_known_exponent_two_point_symbolic(self):
        a,b,x,y=sp.symbols('a b x y',nonzero=True);yi=a+b/x;yj=a+b/y
        self.assertEqual(sp.simplify((y*yj-x*yi)/(y-x)-a),0)
        self.assertEqual(sp.simplify(x*y*(yi-yj)/(y-x)-b),0)
    def test_equal_grid_inverse_symbolic(self):
        a,b,l=sp.symbols('a b l');y=[a+b*l**i for i in range(3)]
        self.assertEqual(sp.simplify((y[0]*y[2]-y[1]**2)/(y[0]-2*y[1]+y[2])-a),0)
        self.assertEqual(sp.simplify((y[2]-y[1])/(y[1]-y[0])-l),0)
    def test_irregular_inverse_both_signs(self):
        s=np.log1p([.07,.47,1.83])
        for xi in [.7,1.3]:
            np.testing.assert_allclose(recover(s,curve(s,xi,2.3,.96)),[2.3,xi,.96],rtol=1e-11)
    def test_irregular_rejects_invalid_ratio(self):
        with self.assertRaises(ValueError):recover(np.array([0.,1.,2.]),np.array([1.,2.,1.]))
    def test_contrast_annihilates_model(self):
        A=contrasts(self.s,3)
        np.testing.assert_allclose(A@np.column_stack([np.ones(24),np.exp(-3*self.s)]),0,atol=4e-16)
        self.assertEqual(np.linalg.matrix_rank(A),22)
    def test_contrast_gls_with_correlated_noise(self):
        A=contrasts(self.s,3);Y=self.mu+.02*np.sin(np.arange(24));r=A@Y
        self.assertAlmostEqual(float(r@np.linalg.solve(A@self.cov@A.T,r)),float(self.lk.fit(Y)[1]),places=10)
    def test_gain_covariance_annihilation(self):
        A=contrasts(self.s,3);S=.1*np.outer(self.mu,self.mu)
        np.testing.assert_allclose(A@S@A.T,0,atol=2e-16)
    def test_grid_profile_contains_fixed_fit(self):
        Y=np.stack([self.mu,self.mu+.02*np.sin(np.arange(24))]);f,p=self.lk.statistics(Y)
        self.assertTrue(np.all(p<=f+1e-10))
        np.testing.assert_allclose(f,self.lk.fit(Y)[1],atol=2e-10)
    def test_scan_q_orthonormal_to_constant(self):
        np.testing.assert_allclose(self.lk.Q.T@self.lk.e0,0,atol=1e-14)
        np.testing.assert_allclose(np.sum(self.lk.Q**2,axis=0),1,atol=1e-14)
    def test_bin_average_by_independent_quadrature(self):
        for s,h in [(.1,.03),(.6,.12),(1.1,.23)]:
            exact=np.exp(-3*s)*np.sinh(3*h)/(3*h)
            numeric=quad(lambda t:np.exp(-3*t),s-h,s+h)[0]/(2*h)
            self.assertAlmostEqual(exact,numeric,places=14)
    def test_heldout_covariance_by_full_linear_map(self):
        X=np.column_stack([np.ones(24),np.exp(-3*self.s)]);T=self.cov[:16,:16];HT=self.cov[16:,:16]
        K=np.linalg.solve(T,HT.T).T;V=np.linalg.inv(X[:16].T@np.linalg.solve(T,X[:16]));B=X[16:]-K@X[:16]
        prediction=K+B@V@np.linalg.solve(T,X[:16]).T
        R=np.column_stack([-prediction,np.eye(8)])
        np.testing.assert_allclose(R@X,0,atol=3e-15)
        np.testing.assert_allclose(R@self.cov@R.T,self.cov[16:,16:]-K@HT.T+B@V@B.T,atol=3e-18)
    def test_hankel_symbolic_factor_and_noise_bias(self):
        a,b,l,r=sp.symbols('a b l r');d=[a*(l-1)*l**i+b*(r-1)*r**i for i in range(3)]
        self.assertEqual(sp.expand(d[0]*d[2]-d[1]**2-a*b*(l-1)*(r-1)*(l-r)**2),0)
        D=np.diff(np.eye(4),axis=0);B=np.array([[0,0,.5],[0,-1,0],[.5,0,0]]);Q=D.T@B@D
        self.assertAlmostEqual(np.trace(Q*.03**2),-2*.03**2)
    def test_fisher_table_rounding(self):
        f=fisher(self.s)
        self.assertAlmostEqual(f['sigma_n'],2.0498,places=4)
        self.assertAlmostEqual(f['sigma_xi'],.02174,places=5)
    def test_matched_covariance_coordinate_invariance(self):
        r=np.array([.3,-.2]);C=np.array([[2.,1/3],[1/3,3.]]);S=np.diag([.75,.625])
        self.assertAlmostEqual(float(r@np.linalg.solve(C,r)),float((S@r)@np.linalg.solve(S@C@S.T,S@r)),places=15)

if __name__=='__main__':unittest.main(verbosity=2)
