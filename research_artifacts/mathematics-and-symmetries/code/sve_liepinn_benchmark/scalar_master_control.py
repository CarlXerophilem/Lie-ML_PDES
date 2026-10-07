#!/usr/bin/env python3
"""Separate 1+1 printed-master-equation control from the user's main.tex.

This is a literature scalar control, not a 2+1 SVE derivation. It rejects the
exceptional subgroup off m=3 and for time-dependent transport coefficients.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def symbolic_check():
    tic=time.perf_counter()
    t,s,p=sp.symbols('t s phi',positive=True)
    pt,ps=sp.symbols('pt ps',positive=True)
    ptt,pts,pss,pttt,ptts,ptss,psss=sp.symbols('ptt pts pss pttt ptts ptss psss',real=True)
    m,g,beta0,delta=sp.symbols('m g beta0 delta',real=True)
    z=(t,s,p,pt,ps,ptt,pts,pss,pttt,ptts,ptss,psss)
    transport=(m-1)*pt**(m-2)*pts**2/ps+pt**(m-1)*(ptss/ps-pts*pss/ps**2)
    water=pts*ptt+ps*pttt-g*ptss/ps**2+2*g*pss*pts/ps**3
    beta=beta0*m/3  # preserve beta_tr=m*A_g*xi with beta0 at m=3
    E=water-g*beta*transport
    coef=sp.Matrix([t,-2*s,0,-pt,2*ps,-2*ptt,pts,4*pss,-3*pttt,0,3*ptss,6*psss])
    prolong=(sp.Matrix([E]).jacobian(z)*coef)[0]
    defect=sp.factor(prolong+E)
    assert sp.simplify(defect.subs(m,3))==0
    assert sp.simplify(defect.subs(m,sp.Rational('3.1')))!=0
    Etime=E.subs(m,3).subs(beta0,beta0*(1+delta*t))
    time_defect=sp.factor((sp.Matrix([Etime]).jacobian(z)*coef)[0]+Etime)
    assert time_defect!=0
    sigma=sp.Symbol('sigma',positive=True);F=sp.Function('F')(sigma)
    fp,fpp=sp.diff(F,sigma),sp.diff(F,sigma,2)
    A=2*sigma*fp**2+4*sigma**2*fp*fpp-g*fpp/fp**2
    B=8*sigma**2*fp*(fp+sigma*fpp)
    R=sp.expand(2*sigma*sp.diff(A,sigma)-g*beta0*sp.diff(B,sigma))
    f3=sp.diff(F,sigma,3);coefficient=sp.diff(R,f3)
    remainder=sp.simplify(R-coefficient*f3)
    expr=sp.Function('F')(s*t*t)
    mapping={p:expr,pt:sp.diff(expr,t),ps:sp.diff(expr,s),ptt:sp.diff(expr,t,2),
             pts:sp.diff(expr,t,s),pss:sp.diff(expr,s,2),pttt:sp.diff(expr,t,3),
             ptts:sp.diff(expr,t,2,s),ptss:sp.diff(expr,t,s,2),psss:sp.diff(expr,s,3)}
    pulled=E.subs(m,3).subs(mapping,simultaneous=True)
    assert sp.simplify(pulled-R.subs(sigma,s*t*t)/t)==0
    K=sp.real_root(27*g/(1-4*g*beta0),3)
    # Verify exact profile on the explicitly positive denominator branch.
    F0=(sp.Rational(45))**sp.Rational(1,3)*sigma**sp.Rational(1,3)
    exact=R.subs({g:1,beta0:sp.Rational('.1')}).subs(F,F0).doit()
    assert sp.simplify(exact)==0
    report={'dimension':'1+1, scalar manuscript control; not the 2+1 neural task',
            'jet_dimension':12,'equation_ops':int(sp.count_ops(E)),
            'generator':'X5=t*d_t-2*s*d_s','finite_flow':'(t,s,phi)->(exp(epsilon)*t,exp(-2epsilon)*s,phi)',
            'invariant':'sigma=s*t^2','multiplier':-1,'generic_defect':str(defect),
            'cubic_verified':True,'near_cubic_rejected':True,'time_coefficient_defect':str(time_defect),
            'pullback_identity':'E3[F(s*t^2)] = R[F](s*t^2)/t','pullback_verified':True,
            'exact_cubic_profile_verified':True,'third_derivative_coefficient':str(coefficient),
            'excluded':'t=0, Fprime=0, third-derivative coefficient=0',
            'symbolic_seconds':time.perf_counter()-tic,'claim':'supplied subgroup and reduction only; printed equation physical interpretation remains a separate issue'}
    q1,q2=sp.symbols('q1 q2')
    a=coefficient.subs({fp:q1,g:1,beta0:sp.Rational('.1')})
    b=remainder.subs({fp:q1,fpp:q2,g:1,beta0:sp.Rational('.1')})
    return report,sp.lambdify((sigma,q1,q2),a,'numpy'),sp.lambdify((sigma,q1,q2),b,'numpy')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',default='results/scalar_master.json')
    args=parser.parse_args();report,a,b=symbolic_check()
    K=45**(1/3);eta=.01
    y0=[K,K/3,-2*K/9*(1+eta)];nodes=np.linspace(1,1.5,101)
    minimum={'a':np.inf,'fp':np.inf}
    def rhs(sigma,y):
        coefficient=a(sigma,y[1],y[2]);minimum['a']=min(minimum['a'],abs(coefficient));minimum['fp']=min(minimum['fp'],abs(y[1]))
        if abs(coefficient)<1e-8 or y[1]<=0:raise FloatingPointError('Left declared regular reduction branch')
        return [y[1],y[2],-b(sigma,y[1],y[2])/coefficient]
    records=[];solutions=[]
    for method,rtol,atol in [('DOP853',1e-7,1e-9),('DOP853',1e-9,1e-11),('DOP853',1e-11,1e-13),('Radau',1e-11,1e-13)]:
        tic=time.perf_counter();sol=solve_ivp(rhs,(1,1.5),y0,t_eval=nodes,method=method,rtol=rtol,atol=atol)
        if not sol.success:raise RuntimeError(sol.message)
        records.append({'method':method,'rtol':rtol,'atol':atol,'seconds':time.perf_counter()-tic,'nfev':sol.nfev})
        solutions.append(sol.y)
    for row,solution in zip(records,solutions):row['max_difference_from_fine_DOP853']=float(np.max(abs(solution-solutions[2])))
    report['numerical']={'initial_curvature_eta':eta,'solvers':records,'min_abs_coefficient_sampled':minimum['a'],
                         'min_Fprime_sampled':minimum['fp'],'domain':[1,1.5],'scope':'one compatible regular cubic profile IVP'}
    destination=Path(args.out);destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))


if __name__=='__main__':main()
