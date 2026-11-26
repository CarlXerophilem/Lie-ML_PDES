"""Independent references; exact recurrences and verified local analytic disks."""
import json
from fractions import Fraction
import math
import time
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp
from flint import arb, fmpq, fmpq_series, ctx
from .algebra import (Series,annular,pair,ball_pair,polynomial_record,majorant,
                      lower_denominator,outward,ROOT141)
from .record import save,run_record,Timer


def n1_coefficients(order):
    values=[fmpq(1)]
    for n in range(1,order+1):values.append(values[-1]*fmpq(2*n-3,2*n))
    return values


def n2_coefficients(initial,order):
    values=[fmpq(initial)]
    for n in range(order):
        p=fmpq_series(values,prec=order+1)
        rhs=20*p**3/(10-p*p-12*p**3)
        values.append(rhs[n]/(n+1))
    return values


def saddle_geometry(sign):
    x,w,r,h=sp.symbols('rho w r h')
    ell=(-21+sign*ROOT141)/30
    b=(141+sign*ROOT141)/70
    D,N,_=annular(r,h)
    dn,dd=map(sp.expand,sp.fraction(sp.cancel(D.subs({r:1+x,h:1+x*(ell+w)}))))
    nn,nd=map(sp.expand,sp.fraction(sp.cancel(N.subs({r:1+x,h:1+x*(ell+w)}))))
    # Remove rho from numerator polynomials, not by evaluation at a small rho.
    dn=sp.cancel(dn/x,extension=ROOT141);nn=sp.cancel(nn/x,extension=ROOT141)
    psi=sp.cancel(nn*dd/(nd*dn)-ell+(b-1)*w,extension=ROOT141)
    pn,pd=sp.fraction(psi)
    assert sp.simplify(pn.subs({x:0,w:0}))==0
    assert sp.simplify(sp.diff(pn,w).subs({x:0,w:0}))==0
    assert sp.simplify(pd.subs({x:0,w:0}))!=0
    numerator=polynomial_record(pn,x,w);denominator=polynomial_record(pd,x,w)
    bv=ball_pair(pair(b));ev=ball_pair(pair(ell))
    accepted=None
    for kr in range(4,25):
        R=arb(f'1/{2**kr}')
        for kw in range(4,13):
            W=arb(f'1/{2**kw}')
            den=lower_denominator(denominator,R,W)
            if not den>0:continue
            pnorm=majorant(numerator,R,W)
            lips=(majorant(numerator,R,W,dw=1)/den+
                  pnorm*majorant(denominator,R,W,dw=1)/den**2)
            # Psi(rho,0)/rho is analytic because its constant term is zero.
            pzero=[[i-1,0,a,c] for i,j,a,c in numerator if j==0 and i>=1]
            K=majorant(pzero,R,arb(0))/lower_denominator(denominator,R,arb(0))
            lam=lips/bv
            image=K*R/(bv+1)+lam*W
            h_lower=1-R*(abs(ev)+W)
            if lam<arb('1/2') and image<W and h_lower>0:
                accepted={'R':f'1/{2**kr}','R_w':f'1/{2**kw}',
                          'denominator_lower':outward(den),'H_modulus_lower':outward(h_lower),
                          'K_Psi':outward(K),'L_Psi':outward(lips),'Lambda':outward(lam),
                          'image_upper':outward(image),'status':'verified',
                          'method':'complex polydisk coefficient majorants, exact Q(sqrt(141)) coefficients and arb rounding'}
                break
        if accepted:break
    if accepted is None:raise ArithmeticError('No verified saddle disk on the predetermined grid')
    return {'slope_exact':pair(ell),'slope':str(sp.N(ell,40)),
            'b_exact':pair(b),'b':str(sp.N(b,40)),
            'psi_numerator':numerator,'psi_denominator':denominator,'disk':accepted}


def saddle_coefficients(sign,degree):
    ctx.cap=degree+4
    a=[fmpq(1),fmpq(-7,10)]; b=[fmpq(0),fmpq(sign,30)]
    for n in range(2,degree+1):
        order=n+2
        r=Series([1,1],order=order);h=Series(a,b,order=order)
        D,N,_=annular(r,h)
        residual=D*h.diff()-N
        ra,rb=residual.coefficient(n)
        divisor=Series(fmpq(1-n,10),fmpq(sign*(n+1),10),order=order)
        value=-Series(ra,rb,order=order)/divisor
        ca,cb=value.coefficient(0)
        a.append(ca);b.append(cb)
    profile=Series(a,b,order=degree+2)
    D,N,_=annular(Series([1,1],order=degree+2),profile)
    residual=D*profile.diff()-N
    assert all(residual.coefficient(n)==(0,0) for n in range(degree+1))
    return profile.pairs(degree+1)


def evaluate_pairs(coefficients,x):
    root=mp.sqrt(141);result=mp.mpf(0)
    for a,b in reversed(coefficients):result=result*x+mp.mpf(a)+mp.mpf(b)*root
    return result


def build(out):
    out.mkdir(parents=True,exist_ok=True)
    gate=json.loads((out/'m0'/'audit'/'ODE_INVENTORY.json').read_text())
    assert gate['status']=='passed'
    assert json.loads((out/'m0'/'REGRESSION.json').read_text())['status']=='passed'
    ctx.prec=256;ctx.cap=128;mp.mp.dps=80
    total=Timer();problems={};references={}
    grid=np.linspace(0,1,1025)
    timer=Timer();coeff=n1_coefficients(64)
    X=fmpq(4,5)
    values=[float((arb(1)-arb(X)*arb(fmpq(i,1024))).sqrt().mid()) for i in range(1025)]
    independent=solve_ivp(lambda x,y:-1/(2*y),[0,float(X)],[1.],method='DOP853',rtol=2.3e-14,atol=1e-15,dense_output=True)
    disagreement=float(np.max(abs(np.array(values)-independent.sol(grid*float(X))[0])))
    assert disagreement<1e-11
    problems['N1']={'id':'N1','model':'E1','generator':'dt+dB','chart':'h,u>0; rank 1',
                    'half_width':str(X),'initial':'1','branch':'positive square root',
                    'parameters':{'m':2,'g':1,'kappa':1,'alpha':1,'mass_flux':1},
                    'prefix':[str(coeff[i]*X**i) for i in range(4)],'guards':['U>0'],
                    'lift':'h=1/U; u=U; B=t+3/2-U^2/2-1/U'}
    references['N1']={'coefficients_physical':list(map(str,coeff)),'values':values,'grid_scaled':grid.tolist(),
                       'kind':'closed form sqrt(1-x), arb evaluation','reference_error_upper':1e-60,
                       'DOP853_disagreement':disagreement,'resources':timer.result()}
    timer=Timer()
    def G(p):return -1/(4*p*p)-3*p/5-mp.log(p)/20
    fold=mp.findroot(lambda p:12*p**3+p**2-10,mp.mpf('.9'))
    zfold=G(fold)-G(mp.mpf('.5'))
    fold_ball=arb(str(fold),'1e-60')
    assert 12*fold_ball.lower()**3+fold_ball.lower()**2-10<0
    assert 12*fold_ball.upper()**3+fold_ball.upper()**2-10>0
    def Ga(p):return -1/(4*p*p)-3*p/5-p.log()/20
    zfold_ball=Ga(fold_ball)-Ga(arb('1/2'))
    # Use a rational endpoint safely inside 4/5 of the enclosed fold distance.
    endpoint=int(mp.floor(mp.mpf(str(zfold_ball.mid()).split(' ')[0].strip('[]'))*mp.mpf('.8')*2**40))-1
    X=fmpq(endpoint,2**40)
    assert arb(X)<arb('4/5')*zfold_ball
    ps=[];previous=mp.mpf('.5');p0=previous
    for i in range(1025):
        z=mp.mpf(str(X))*i/1024
        root=p0 if i==0 else mp.findroot(lambda p:G(p)-G(p0)-z,(previous,previous+mp.mpf('.001')))
        ball=arb(str(root),'1e-50');target=arb(X)*arb(fmpq(i,1024))
        assert Ga(ball.lower())-Ga(arb('1/2'))<target
        assert Ga(ball.upper())-Ga(arb('1/2'))>target
        ps.append(float(root));previous=root
    independent=solve_ivp(lambda z,p:20*p**3/(10-p*p-12*p**3),[0,float(X)],[.5],
                          method='DOP853',rtol=2.3e-14,atol=1e-15,dense_output=True)
    disagreement=float(np.max(abs(np.array(ps)-independent.sol(grid*float(X))[0])))
    assert disagreement<1e-11
    ode=mp.odefun(lambda z,p:20*p**3/(10-p*p-12*p**3),0,mp.mpf('.5'),tol=mp.mpf('1e-45'),degree=30)
    high_precision_check=abs(ode(mp.mpf(str(X)))-previous)
    assert high_precision_check<mp.mpf('1e-30')
    coeff=n2_coefficients(fmpq(1,2),40)
    problems['N2']={'id':'N2','model':'M -> E1','generator':'dt-ds+(1/2)dphi','chart':'p>0,u=1/2+p>0; rank 1',
                    'half_width':str(X),'initial':'1/2','branch':'p<p_fold',
                    'parameters':{'m':2,'g':1,'beta':'1/10','c':-1,'gamma':'1/2','I':1,'F0':0,'bed_gauge':'17/8'},
                    'prefix':[str(coeff[i]*X**i) for i in range(4)],'guards':['p>0','1/2+p>0','L(p)>0'],
                    'lift':'F(z)=integral_0^z p; x=t/2+F; h=1/p; u=1/2+p; B=17/8-1/p-p^2/2+t'}
    references['N2']={'kind':'monotone implicit quadrature with arb root brackets','p_fold':str(fold),
                       'z_fold':outward(zfold_ball),'coefficients_physical':list(map(str,coeff)),
                       'values':ps,'grid_scaled':grid.tolist(),'reference_error_upper':1e-49,
                       'mpmath_ODE_disagreement':str(high_precision_check),'DOP853_disagreement':disagreement,
                       'L_min_lower':str((1/(2*arb(str(previous),'1e-50')**3)-arb('3/5')-1/(20*arb(str(previous),'1e-50'))).lower()),
                       'resources':timer.result()}
    geometries={sign:saddle_geometry(sign) for sign in (1,-1)}
    X=min(Fraction(g['disk']['R']) for g in geometries.values())/2
    for sign,id in ((1,'N3+'),(-1,'N3-')):
        timer=Timer();geo=geometries[sign];disk=geo['disk']
        R=arb(disk['R']);W=arb(disk['R_w']);theta=arb(str(X))/R
        degree=40
        while not W*R*theta**(degree+1)/(1-theta)<arb('1e-24'):degree+=1
        if degree>100:raise ArithmeticError('Reference order cap exceeded')
        coefficients=saddle_coefficients(sign,degree)
        xn=mp.mpf(str(X));scaled=np.linspace(-1,1,1025)
        # q=(H-1-ell*rho)/(X*rho), evaluated without subtractive cancellation.
        qcoeff=[['0','0']]+[[str(fmpq(a)*fmpq(str(X))**(n-2)),str(fmpq(b)*fmpq(str(X))**(n-2))]
                            for n,(a,b) in enumerate(coefficients[2:],2)]
        values=[float(evaluate_pairs(qcoeff,mp.mpf(float(s)))) for s in scaled]
        physical=[float(evaluate_pairs(coefficients,xn*mp.mpf(float(s)))) for s in scaled]
        dis=0.
        for side in (-1,1):
            start=side*float(X)/32;end=side*float(X)
            h0=float(evaluate_pairs(coefficients,mp.mpf(start)))
            sol=solve_ivp(lambda rho,h:np.array(annular(1+rho,h)[1])/np.array(annular(1+rho,h)[0]),
                          [start,end],[h0],method='DOP853',rtol=2.3e-14,atol=1e-15)
            dis=max(dis,abs(sol.y[0,-1]-float(evaluate_pairs(coefficients,mp.mpf(end)))))
        assert dis<1e-10
        tail=W*R*theta**(degree+1)/(1-theta)
        qtail=W/arb(str(X))*theta**degree/(1-theta)
        prefix=[str(mp.mpf(a)+mp.mpf(b)*mp.sqrt(141)) for a,b in qcoeff[:4]]
        problems[id]={'id':id,'model':'E2','generator':'<R,dt-7dB>','chart':'r,H>0; rank 2',
                      'half_width':str(X),'initial':'0','branch':id[-1],
                      'parameters':{'g':1,'K':1,'G':1,'f':1,'C1':1,'C2':1,'C3':'-71/16','c':-7,'Z0':0},
                      **{k:v for k,v in geo.items() if k!='disk'},'reference_radius':disk['R'],
                      'remainder_radius':disk['R_w'],'prefix':prefix,'guards':['H>0','r>0','d!=0'],
                      'lift':'H=1+ell*rho+X*rho*q; V=1/(rH); W=1/r-r/2; Z=integral_1^r P_Z; B=Z-7t'}
        references[id]={'kind':'Q(sqrt(141)) Briot–Bouquet series with complex-disk majorants',
                        'disk':disk,'coefficients_physical':coefficients,'coefficients_q':qcoeff,
                        'degree':degree,'recurrence_residual_coefficients_exactly_zero':True,
                        'value_tail':outward(tail),'derivative_tail':outward(W*theta**degree*((degree+1)/(1-theta)+theta/(1-theta)**2)),
                        'reference_error_upper':float(qtail.upper()),'values':values,'physical_values':physical,
                        'grid_scaled':scaled.tolist(),'DOP853_disagreement':dis,'resources':timer.result()}
        print(id,'R',disk['R'],'R_w',disk['R_w'],'degree',degree,flush=True)
    save(out/'problems.json',problems)
    report=run_record('references',{'no_ML':True,'arb_precision_bits':ctx.prec})
    report.update(status='passed',tasks=references,resources=total.result())
    save(out/'REFERENCES.json',report)
    print('References verified',flush=True)
