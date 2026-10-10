import numpy as np
import sympy as sp
import pytest
from sve_lab.numerics import reference,integrated_reference,taylor
from sve_lab.trials import Trial,original_residual
from sve_lab.symbolic import reduced_residual,z,f,P,C,H
from sve_lab.jets import g,kappa
from sve_lab.tube import tube_certificate

@pytest.mark.parametrize('physical',[False,True])
def test_reference_family_uniform_bootstrap(physical):
    cert=tube_certificate(physical)
    assert sp.Rational(cert['barrier_slack'])>0
    assert sp.Rational(cert['leading_lower'])>0
    assert sp.Rational(cert['velocity_lower'])>0

@pytest.mark.parametrize('physical',[False,True])
@pytest.mark.parametrize('exponent',[1.,2.9,3.1,4.])
def test_third_order_and_first_integral_agree(physical,exponent):
    ref,guards=reference(exponent,physical)
    other,I0=integrated_reference(exponent,physical)
    grid=np.linspace(1,1.4,101)
    np.testing.assert_allclose(ref.sol(grid)[:2],other.sol(grid)[:2],rtol=1e-9,atol=1e-11)
    assert min(guards.values())>0

@pytest.mark.parametrize('kind',['reduced_tanh','direct_tanh','reduced_chebyshev'])
@pytest.mark.parametrize('order',[2,4])
def test_hard_data_exact(kind,order):
    prior=taylor(3.1,False,order)
    trial=Trial(prior,kind)
    weights=np.linspace(-.2,.3,12)
    ys=np.linspace(0,np.log(2),7)
    for j,value in enumerate([2.,.5,.1]):
        np.testing.assert_allclose(trial.derivative(ys,1.,weights,0,j),value,atol=1e-14)

@pytest.mark.parametrize('physical',[False,True])
def test_original_residual_against_ode(physical):
    xx=np.linspace(1,1.4,11)
    trial=Trial(taylor(2.9,physical,4))
    weights=np.linspace(-.001,.001,12)
    jets=trial.jets(0.,xx,weights)
    actual,_,_=original_residual(jets,xx,2.9,physical)
    R=sp.lambdify((z,f,P,C,H,g,kappa),reduced_residual(sp.Rational(29,10),physical),'numpy')
    expected=R(xx,*(jets[(0,j)] for j in range(4)),1.,1./30.)
    np.testing.assert_allclose(actual,expected,rtol=1e-12,atol=1e-12)

@pytest.mark.parametrize('physical',[False,True])
def test_direct_2d_residual_against_original_chain_rule(physical):
    tt,ss,yy,zz=sp.symbols('tt ss yy zz',positive=True)
    U=2+(zz-1)/2+(zz-1)**2/20+yy**2/1000+3*yy*(zz-1)**3/1000
    phi=tt*U.subs({yy:sp.log(tt),zz:ss/tt})
    A=sp.diff(phi,ss)*sp.diff(phi,tt,2)-sp.diff(phi,ss,2)/sp.diff(phi,ss)**2
    E=sp.diff(A,tt)-sp.Rational(1,10)*sp.diff(sp.diff(phi,tt)**2*sp.diff(phi,tt,ss)/sp.diff(phi,ss),ss)
    if physical:E-=sp.diff(sp.diff(phi,tt)*A/sp.diff(phi,ss),ss)
    y0,z0=.2,1.2
    jets={(i,j):float(sp.diff(U,yy,i,zz,j).subs({yy:y0,zz:z0}))
          for n in range(4) for i in range(n+1) for j in [n-i]}
    actual,_,_=original_residual(jets,z0,3,physical)
    expected=float((tt**2*E).subs({tt:np.exp(y0),ss:np.exp(y0)*z0}))
    np.testing.assert_allclose(actual,expected,rtol=1e-11,atol=1e-12)
