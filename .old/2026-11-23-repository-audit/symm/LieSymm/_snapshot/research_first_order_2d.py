"""Unrestricted 2+1 first-order SVE point algebra, G=0.

All stage-1 inputs are read-only. The necessary integration is documented in
FIRST_ORDER_2D_DERIVATION.md. Basis vectors are differentiated from the solved
arbitrary-coefficient integral, not supplied to a finite ansatz search.
"""
from __future__ import annotations

import json
from pathlib import Path
import time

import sympy as s

t,x,y,h,u,v,B=s.symbols('t x y h u v B',real=True)
g,K=s.symbols('g K',positive=True)
m,f=s.symbols('m f',real=True)
COORDINATES=(t,x,y,h,u,v,B)
FIELDS=(h,u,v,B)
px=s.Matrix(s.symbols('h_x u_x v_x B_x',real=True))
py=s.Matrix(s.symbols('h_y u_y v_y B_y',real=True))
R2=u*u+v*v


def positive_radius_normal_form(expression):
    """Combine only integer shifts of powers of the known positive radius.

    SymPy can leave S**(m/2-1/2)-S*S**(m/2-3/2) uncombined when S is
    represented by u**2+v**2. A positive temporary S permits exact exponent
    grouping; its defining polynomial is restored in the coefficients.
    Neither velocity component is assumed positive.
    """
    reduced=s.simplify(s.factor_terms(s.expand(expression)))
    if reduced==0:
        return reduced
    radius=s.Dummy('positive_speed_squared',positive=True)
    expanded=s.expand(reduced.xreplace({R2:radius}))
    grouped={}
    for term in s.Add.make_args(expanded):
        exponent,coefficient=s.S.Zero,s.S.One
        for factor in s.Mul.make_args(s.factor_terms(term)):
            if factor==radius:
                exponent+=1
            elif isinstance(factor,s.Pow) and factor.base==radius:
                exponent+=factor.exp
            else:
                coefficient*=factor
        constant,variable=s.expand(exponent).as_coeff_Add()
        integer=s.floor(constant)
        if integer.is_Integer:
            key=s.simplify(variable+constant-integer)
            coefficient*=radius**integer
        else:
            key=s.simplify(exponent)
        grouped[key]=grouped.get(key,0)+coefficient
    return s.factor_terms(sum(s.simplify(coefficient.subs(radius,R2))*R2**exponent
                             for exponent,coefficient in grouped.items()))


def flux_matrices(exponent=None,transport=None):
    mm=m if exponent is None else s.sympify(exponent)
    kk=K if transport is None else s.sympify(transport)
    if kk==0:
        Q=s.zeros(2)
    else:
        Q=kk*R2**((mm-3)/2)*s.Matrix([[mm*u*u+v*v,(mm-1)*u*v],
                                                   [(mm-1)*u*v,u*u+mm*v*v]])
    A=s.Matrix([[u,h,0,0],[g,u,0,g],[0,0,u,0],[0,Q[0,0],Q[0,1],0]])
    C=s.Matrix([[v,0,h,0],[0,v,0,0],[g,0,v,g],[0,Q[1,0],Q[1,1],0]])
    return A,C,Q


def direct_prolongation(coefficients,exponent=None,transport=None,coriolis=None,simplify=True):
    """First prolongation directly on the original four evolution rows."""
    tau,xi,chi,*vertical=map(s.sympify,coefficients)
    eta=s.Matrix(vertical)
    A,C,_=flux_matrices(exponent,transport)
    ff=f if coriolis is None else s.sympify(coriolis)
    F=s.Matrix([0,ff*v,-ff*u,0])
    wt=F-A*px-C*py

    def total(expression,base,jets):
        return s.diff(expression,base)+sum(s.diff(expression,w)*jets[i] for i,w in enumerate(FIELDS))

    Dt=lambda z:total(z,t,wt)
    Dx=lambda z:total(z,x,px)
    Dy=lambda z:total(z,y,py)
    et=eta.applyfunc(Dt)-wt*Dt(tau)-px*Dt(xi)-py*Dt(chi)
    ex=eta.applyfunc(Dx)-wt*Dx(tau)-px*Dx(xi)-py*Dx(chi)
    ey=eta.applyfunc(Dy)-wt*Dy(tau)-px*Dy(xi)-py*Dy(chi)
    dA=sum((eta[i]*A.diff(w) for i,w in enumerate(FIELDS)),s.zeros(4))
    dC=sum((eta[i]*C.diff(w) for i,w in enumerate(FIELDS)),s.zeros(4))
    residual=et+A*ex+C*ey+dA*px+dC*py-F.jacobian(FIELDS)*eta
    return residual.applyfunc(s.simplify if simplify else s.expand)


def build_determining_system(exponent=None,transport=None,coriolis=None):
    """All coefficients begin as arbitrary functions of all seven coordinates.

    The polynomial coefficients in the eight independent spatial jets are
    necessary and sufficient. Projectability is a derived theorem, not an
    input restriction. This callable is available to the parent engine.
    """
    generator=tuple(s.Function(name)(*COORDINATES) for name in ('tau','xi','chi','H','U','V','Z'))
    residual=direct_prolongation(generator,exponent,transport,coriolis,simplify=False)
    jets=tuple(px)+tuple(py)
    polynomial=[s.Poly(e,*jets) for e in residual]
    equations=tuple(dict.fromkeys(coefficient for poly in polynomial for coefficient in poly.coeffs()))
    return {'generator':generator,'on_shell_residual':residual,
            'free_jets':jets,'determining_equations':equations,
            'projectability_assumed':False,'proof':'FIRST_ORDER_2D_DERIVATION.md'}


def projectable_matrices(tau,xi,chi,eta,exponent=None,transport=None,coriolis=None):
    """Necessary/sufficient first-jet matrices after proven projectability."""
    A,C,_=flux_matrices(exponent,transport)
    ff=f if coriolis is None else s.sympify(coriolis)
    F=s.Matrix([0,ff*v,-ff*u,0])
    eta=s.Matrix(eta)
    J=eta.jacobian(FIELDS)
    dA=sum((eta[i]*A.diff(w) for i,w in enumerate(FIELDS)),s.zeros(4))
    dC=sum((eta[i]*C.diff(w) for i,w in enumerate(FIELDS)),s.zeros(4))
    Mx=A*J-J*A+dA+(s.diff(tau,t)-s.diff(xi,x))*A-s.diff(xi,y)*C
    Mx+=s.diff(tau,x)*A*A+s.diff(tau,y)*C*A-s.diff(xi,t)*s.eye(4)
    My=C*J-J*C+dC-s.diff(chi,x)*A+(s.diff(tau,t)-s.diff(chi,y))*C
    My+=s.diff(tau,x)*A*C+s.diff(tau,y)*C*C-s.diff(chi,t)*s.eye(4)
    C0=eta.diff(t)+A*eta.diff(x)+C*eta.diff(y)
    C0+=(J-s.diff(tau,t)*s.eye(4))*F-F.jacobian(FIELDS)*eta
    C0-=s.diff(tau,x)*A*F+s.diff(tau,y)*C*F
    return C0,Mx,My


def _branch(branch):
    branch=branch.removeprefix('2d__')
    if branch.endswith('_f_nonzero'):
        base=branch.removesuffix('_f_nonzero'); rotating=True
    elif branch.endswith('_f0'):
        base=branch.removesuffix('_f0'); rotating=False
    else:
        raise ValueError('Specify _f0 or _f_nonzero explicitly')
    if base not in ('grass_generic','grass_cubic','zero_transport'):
        raise ValueError('Not a G=0 first-order 2D branch: '+branch)
    return branch,base,rotating


def general_solution(branch,coordinates=None,exponent=None,f_value=None):
    """Solve the terminal constant equations of the unrestricted integration.

    Coordinate order is (t,x,y,h,u,v,B). f_value is optional because the
    explicit branch already records whether the fixed Coriolis constant is
    zero. No stage-1 module is imported or mutated.
    """
    branch,base,rotating=_branch(branch)
    coords=COORDINATES if coordinates is None else tuple(coordinates)
    if len(coords)!=7:
        raise ValueError('coordinates must be (t,x,y,h,u,v,B)')
    for value in (exponent,f_value):
        if value is None:
            continue
        value=s.sympify(value)
        if value.free_symbols.intersection(coords) or value.atoms(s.Function):
            raise ValueError('Model parameters must be constant in point coordinates')
        if value.is_real is False or value.is_finite is False or value in (s.nan,s.zoo):
            raise ValueError('Model parameters must be finite real constants')
    tt,xx,yy,hh,uu,vv,BB=coords
    if base=='zero_transport':
        mm=None;transport_factor=s.S.Zero
        guards=['K=0','G=0','m removed']
    else:
        mm=(s.Integer(3) if base=='grass_cubic' else m) if exponent is None else s.sympify(exponent)
        if base=='grass_cubic' and mm!=3:
            raise ValueError('Cubic branch requires m=3')
        if mm.is_number and (mm.is_real is not True or not 1<=mm<=4
                             or (base=='grass_generic' and mm==3)):
            raise ValueError('Exponent lies outside the stated branch')
        transport_factor=K*(mm-3)
        guards=['K>0','G=0',f'1<={mm}<=4',f'{mm}=3' if base=='grass_cubic' else f'{mm}!=3']
    ff=(f if rotating else s.S.Zero) if f_value is None else s.sympify(f_value)
    if ff.is_real is False or ff.is_finite is False or (rotating and ff==0) or (not rotating and ff!=0):
        raise ValueError('Coriolis constant contradicts the selected branch')
    guards+=[f'{ff}!=0' if rotating else 'f=0']
    for value in (mm,ff):
        if value is not None and value.is_real is None:
            guards.append(str(s.Contains(value,s.S.Reals,evaluate=False)))
        if value is not None and value.is_finite is None:
            guards.append(str(s.Q.finite(value)))
    t0,x0,y0,b0,omega,a0,p0=s.symbols('t0 x0 y0 b0 omega a0 p0',real=True)
    terminal=(transport_factor*(p0-a0),ff*a0)
    solved=list(s.linsolve(terminal,(a0,p0)))
    if len(solved)!=1:
        raise AssertionError('Unexpected terminal constant system')
    integral=s.Matrix([a0*tt+t0,p0*xx-omega*yy+x0,omega*xx+p0*yy+y0,
                       2*(p0-a0)*hh,(p0-a0)*uu-omega*vv,
                       omega*uu+(p0-a0)*vv,2*(p0-a0)*BB+b0])
    coefficients=integral.subs(dict(zip((a0,p0),solved[0])),simultaneous=True)
    constants=tuple(c for c in (t0,x0,y0,b0,omega,a0,p0) if coefficients.has(c))
    return {'branch':branch,'coefficients':coefficients,'free_constants':constants,
            'basis':tuple(coefficients.diff(c) for c in constants),'dimension':len(constants),
            'constant_equations':terminal,'constant_solution':solved[0],
            'coordinate_order':coords,'exponent':mm,'coriolis':ff,
            'guards':['h>0','u^2+v^2>0','g>0']+guards,
            'necessity_proof':'FIRST_ORDER_2D_DERIVATION.md',
            'review_status':'independent_review_required'}


def integration_certificate():
    """Symbolic elimination data before integrating spatial coefficients."""
    qa,qb,qc=s.symbols('qa qb qc',real=True)
    a,b,c,p,q,r,z,ex,ey=s.symbols('a b c p q r z ex ey',real=True)
    H,U,V,Z=s.symbols('H U V Z')
    J=s.Matrix(4,4,lambda i,j:s.Symbol('HUVZ'[i]+'_'+str(FIELDS[j])))
    A=s.Matrix([[u,h,0,0],[g,u,0,g],[0,0,u,0],[0,qa,qb,0]])
    C=s.Matrix([[v,0,h,0],[0,v,0,0],[g,0,v,g],[0,qb,qc,0]])
    dqa,dqb,dqc=s.symbols('delta_qa delta_qb delta_qc')
    dA=s.Matrix([[U,H,0,0],[0,U,0,0],[0,0,U,0],[0,dqa,dqb,0]])
    dC=s.Matrix([[V,0,H,0],[0,V,0,0],[0,0,V,0],[0,dqb,dqc,0]])
    Mx=A*J-J*A+dA+(a-p)*A-q*C+b*A*A+c*C*A-ex*s.eye(4)
    My=C*J-J*C+dC-r*A+(a-z)*C+b*A*C+c*C*C-ey*s.eye(4)
    rx=s.Matrix([-qb/u,0,1,qb/u]);ry=s.Matrix([-qb/v,1,0,qb/v])
    lx=s.Matrix([[0,0,1,0]]);ly=s.Matrix([[0,1,0,0]])
    passive=(s.expand((lx*Mx*rx)[0]),s.expand((ly*My*ry)[0]))
    velocity=s.solve(passive,(U,V),dict=True)[0]
    traces=(s.expand(s.trace(Mx).subs(velocity)),s.expand(s.trace(My).subs(velocity)))
    return {'matrices':(A,C),'linear_jet_matrices':(Mx,My),
            'passive_eigenvectors':(rx,ry),'passive_equations':passive,
            'solved_velocity':velocity,'trace_after_velocity':traces,
            'trace_h_coefficients':tuple(s.diff(e,h) for e in traces),
            'projectability':'pure-direction quadratic coefficients and dense simple spectrum',
            'remaining_spatial_equations':('xi_x=chi_y','xi_y=-chi_x','p_x=0','p_y=0'),
            'remaining_time_equations':('tau_x=0','tau_y=0','xi_t=0','chi_t=0','tau_tt=0'),
            'terminal_equations':('K*(m-3)*(p-tau_t)=0','f*tau_t=0','z_t=z_x=z_y=0')}


def run_verification():
    start=time.perf_counter();checks={}

    def check(name,expression):
        values=list(expression) if isinstance(expression,(list,tuple,s.MatrixBase)) else [expression]
        residual=[s.simplify(e) for e in values]
        ok=all(e==0 for e in residual)
        checks[name]={'passed':ok,'nonzero_residuals':[str(e) for e in residual if e!=0]}

    # The quadratic determining equations are unaffected by the zero-order
    # Coriolis source. Four distinct eigenvalues force both coefficient rows.
    eigenvalues=s.symbols('lambda0:4');ar=s.symbols('tau_w0:4');br=s.symbols('xi_w0:4')
    L=s.diag(*eigenvalues);pjet=px;Lp=L*pjet
    ar=s.Matrix([ar]);br=s.Matrix([br])
    Q2=L*Lp*(ar*pjet)[0]-Lp*(ar*Lp)[0]+pjet*(br*Lp)[0]-Lp*(br*pjet)[0]
    for i in range(4):
        for j in range(4):
            if i!=j:
                coefficient=s.Poly(s.expand(Q2[i]),*pjet).coeff_monomial(pjet[i]*pjet[j])
                check(f'quadratic_eigenbasis_{i}_{j}',coefficient-(eigenvalues[i]-eigenvalues[j])*(eigenvalues[i]*ar[j]-br[j]))

    cert=integration_certificate();A,C=cert['matrices'];rx,ry=cert['passive_eigenvectors']
    check('passive_x_eigenpair',A*rx-u*rx);check('passive_y_eigenpair',C*ry-v*ry)
    check('passive_x_left_eigenpair',s.Matrix([[0,0,1,0]])*A-u*s.Matrix([[0,0,1,0]]))
    check('passive_y_left_eigenpair',s.Matrix([[0,1,0,0]])*C-v*s.Matrix([[0,1,0,0]]))
    qa,qb,qc=s.symbols('qa qb qc',real=True)
    aa,bb,cc,ex,ey=s.symbols('a b c ex ey',real=True)
    check('trace_forces_time_projectability_x',cert['trace_after_velocity'][0]-(2*g*(bb*(h+qa)+cc*qb)-ex))
    check('trace_forces_time_projectability_y',cert['trace_after_velocity'][1]-(2*g*(bb*qb+cc*(h+qc))-ey))
    core=s.Matrix([[u,h,0],[g,u,g],[0,qa,0]])
    check('directional_core_symmetrizer',s.diag(g/h,1,g/qa)*core-(s.diag(g/h,1,g/qa)*core).T)
    spectral=s.symbols('lambda')
    check('passive_eigenvalue_distinct_from_core',core.charpoly(spectral).as_expr().subs(spectral,u)+g*h*u)
    check('K_zero_directional_characteristic',A.subs({qa:0,qb:0}).charpoly(spectral).as_expr()
          -(spectral-u)*spectral*((spectral-u)**2-g*h))

    # Projectable matrix formula compared with an independent prolongation.
    tau=s.Function('tau')(t,x,y);xi=s.Function('xi')(t,x,y);chi=s.Function('chi')(t,x,y)
    eta=s.Matrix([s.Function(name)(*COORDINATES) for name in ('H','U','V','Z')])
    C0,Mx,My=projectable_matrices(tau,xi,chi,eta,exponent=1)
    independent=direct_prolongation((tau,xi,chi,*eta),exponent=1,simplify=False)
    check('projectable_matrix_formula_equals_direct_prolongation',independent-C0-Mx*px-My*py)

    # The remaining velocity/spatial equations are verified for arbitrary H,Z.
    p,q,r,z,a=s.symbols('p q r z a',real=True)
    HH=s.Function('H')(t,x,y,h,u,v,B);ZZ=s.Function('Z')(t,x,y,h,u,v,B)
    vertical=s.Matrix([HH,(p-a)*u+q*v,r*u+(z-a)*v,ZZ])
    _,Wx,Wy=projectable_matrices(a*t,p*x+q*y,r*x+z*y,vertical,exponent=1)
    check('water_H_u_equation',Wx[0,0]+g*s.diff(HH,u))
    check('water_H_v_equation',Wy[0,0]+g*s.diff(HH,v))
    check('water_H_B_x_equation',Wx[0,3]-(u*s.diff(HH,B)-g*s.diff(HH,u)))
    check('water_H_B_y_equation',Wy[0,3]-(v*s.diff(HH,B)-g*s.diff(HH,v)))
    Hreduced=s.Function('Hred')(t,x,y,h)
    replacement={HH:Hreduced}
    Wx=Wx.subs(replacement).doit();Wy=Wy.subs(replacement).doit()
    check('water_H_homogeneity',Wx[0,1]-(Hreduced-h*s.diff(Hreduced,h)))
    check('water_conformal_off_diagonal',Wx[2,0]+g*(q+r))
    check('water_conformal_diagonal_difference',Wx[1,0]-Wy[2,0]-2*g*(z-p))
    check('water_Z_u',Wx[1,1]-g*s.diff(ZZ,u))
    check('water_Z_v',Wx[1,2]-g*s.diff(ZZ,v))

    # Radial transport homogeneity/equivariance justify every real m, not a grid.
    _,_,Q=flux_matrices()
    rot=s.Matrix([[0,-1],[1,0]])
    check('radial_tensor_homogeneity',(u*Q.diff(u)+v*Q.diff(v)-(m-1)*Q).applyfunc(positive_radius_normal_form))
    check('radial_tensor_rotational_equivariance',-v*Q.diff(u)+u*Q.diff(v)-(rot*Q-Q*rot))

    a0,p0,omega,b0,t0,x0,y0=s.symbols('a0 p0 omega b0 t0 x0 y0',real=True)
    lam=p0-a0
    full=s.Matrix([a0*t+t0,p0*x-omega*y+x0,omega*x+p0*y+y0,
                   2*lam*h,lam*u-omega*v,omega*u+lam*v,2*lam*B+b0])
    Ax,Ay,_=flux_matrices()
    sediment=(Ax*px+Ay*py)[3]
    expected=s.Matrix([0,-a0*f*v,a0*f*u,lam*(m-3)*sediment])
    check('general_integral_exact_residual',direct_prolongation(full)-expected)
    # Check the coefficient PDE which eliminates arbitrary conformal maps.
    ap,px0,py0,wx,wy=s.symbols('a_prime p_x p_y omega_x omega_y',real=True)
    et=s.Matrix([-2*ap*h,-ap*u,-ap*v,-2*ap*B])
    exv=s.Matrix([2*px0*h,px0*u-wx*v,wx*u+px0*v,2*px0*B])
    eyv=s.Matrix([2*py0*h,py0*u-wy*v,wy*u+py0*v,2*py0*B])
    continuity=(et+Ax*exv+Ay*eyv)[0].subs({wx:-py0,wy:px0})
    check('continuity_forces_affine_conformal_map',continuity-h*(-2*ap+4*px0*u+4*py0*v))

    branches={}
    for base in ('grass_generic','grass_cubic','zero_transport'):
        for rotating in (False,True):
            branch=base+('_f_nonzero' if rotating else '_f0')
            solved=general_solution(branch)
            residual=direct_prolongation(solved['coefficients'],
                exponent=3 if base=='grass_cubic' else None,
                transport=0 if base=='zero_transport' else None,
                coriolis=f if rotating else 0)
            check(branch+'_general_solution',residual)
            expected_dimension=(5 if rotating else 6)+(base!='grass_generic')
            check(branch+'_dimension',solved['dimension']-expected_dimension)
            branches[branch]={'dimension':solved['dimension'],
                'general_coefficients':[str(e) for e in solved['coefficients']],
                'free_constants':[str(e) for e in solved['free_constants']],
                'basis':[[str(e) for e in vector] for vector in solved['basis']],
                'constant_equations':[str(e) for e in solved['constant_equations']],
                'guards':solved['guards']}
    boost=direct_prolongation([0,t,0,0,1,0,0],transport=0,coriolis=0)
    check('Galilean_boost_negative_control_K_zero',boost-s.Matrix([0,0,0,-px[3]]))
    nonlinear_conformal=[0,x*x-y*y,2*x*y,4*x*h,2*x*u-2*y*v,2*y*u+2*x*v,4*x*B]
    conformal_defect=direct_prolongation(nonlinear_conformal,transport=0,coriolis=0)
    check('nonlinear_conformal_negative_control_mass',conformal_defect[0]-8*h*u)
    for label,branch,kwargs in (
        ('variable_exponent','grass_generic_f0',{'exponent':x}),
        ('variable_Coriolis','grass_cubic_f_nonzero',{'f_value':t}),
        ('nonreal_exponent','grass_generic_f0',{'exponent':s.I}),
        ('nonreal_Coriolis','grass_cubic_f_nonzero',{'f_value':s.I}),
        ('wrong_generic_stratum','grass_generic_f0',{'exponent':3}),
        ('wrong_Coriolis_stratum','grass_cubic_f_nonzero',{'f_value':0})):
        try:
            general_solution(branch,**kwargs)
        except ValueError:
            check('parameter_guard_'+label,0)
        else:
            check('parameter_guard_'+label,1)
    return {'model':'2+1 full SVE, G=0, radial signed Grass flux and constant Coriolis',
            'claim_status':'unrestricted_integration_complete_independent_review_required',
            'assumptions':['h>0','u^2+v^2>0','g>0','K>=0','1<=m<=4 if K>0',
                           'fixed real f; f=0 and f!=0 separate','open connected point-coordinate domain'],
            'checks':checks,'check_count':len(checks),'all_checks_passed':all(v['passed'] for v in checks.values()),
            'branches':branches,'integration_certificate':{k:str(value) for k,value in cert.items()},
            'negative_controls':{'K_zero_Galilean_boost':[str(e) for e in boost],
                                 'nonlinear_conformal_mass_defect':str(conformal_defect[0])},
            'elapsed_seconds':time.perf_counter()-start,'per_process_timeout_seconds':60,
            'not_claimed':['zero-speed maximal algebra','contact/generalized/nonlocal symmetries',
                           'full equivalence groupoid','optimal subalgebra system','data compatibility',
                           'conditional symmetries','ML results']}


if __name__=='__main__':
    result=run_verification()
    target=Path(__file__).with_name('first_order_2d_results.json')
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'output':str(target),'passed':result['all_checks_passed'],
                      'checks':result['check_count'],'elapsed_seconds':result['elapsed_seconds']},indent=2))
    raise SystemExit(0 if result['all_checks_passed'] else 1)
