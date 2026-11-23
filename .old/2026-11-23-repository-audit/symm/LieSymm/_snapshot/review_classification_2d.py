"""Independent exact-version review of the 17 declared two-dimensional cells.

The reviewer owns this file and CLASSIFICATION_2D_REVIEW.md. The independent
jet recursion below does not call either author's prolongation implementation.
Run one bounded phase at a time under the cpu-symbolic lease. A partial or
failed receipt never opens the classification gate.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time
from unittest.mock import patch

import sympy as s

HERE = Path(__file__).resolve().parent
INPUTS = (
    'main.py', 'models.py', 'models_2d.py', 'analyze_2d.py', 'classification_2d.py',
    'research_first_order_2d.py', 'research_slope_2d.py',
    'FIRST_ORDER_2D_DERIVATION.md', 'SLOPE_2D_DERIVATION.md',
    'reductions_2d.py', 'tests/test_models_2d.py', 'tests/test_reductions_2d.py',
    'radial_normal_form.py', 'general_sve.py', 'case_support_2d.py',
    'stage2_gate.py', 'stage2_runner.py', 'gatekeeper.py', 'run_all.py', 'validate_project.py',
    'review_classification_2d.py', 'CLASSIFICATION_2D_REVIEW.md', 'CONTRACT.md',
)
PHASES = ('raw', 'necessity', 'branches', 'reductions', 'adapter')


def hashes():
    return {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUTS}


# Snapshot before importing the reviewed implementations.
SNAPSHOT = hashes()
import models_2d as models
import research_first_order_2d as first_author
import research_slope_2d as slope_author
import analyze_2d as frontend
import classification_2d as classifier
import reductions_2d as reductions
from main import JetSpace as ParentJet, arbitrary_generator as parent_generator
from main import prolongation_coefficients as parent_prolong, point_action as parent_action

t, x, y, h, u, v, B = (*models.branch_model_2d('grass_generic_f0')['independent_variables'],
                         *models.branch_model_2d('grass_generic_f0')['dependent_fields'])
coords = (t, x, y, h, u, v, B)
fields = (h, u, v, B)
g, K, G, m, n, f = models.g, models.K, models.G, models.m, models.n, models.f
speed2 = u*u+v*v
ROT = s.Matrix([[0, -1], [1, 0]])


class ReviewJet:
    """Independent finite J2 coordinates, total derivatives and point action."""
    def __init__(self):
        self.base = (t, x, y)
        self.fields = fields
        self.symbols = {}
        for a, field in enumerate(fields):
            for degree in range(3):
                for index in itertools.product(range(degree+1), repeat=3):
                    if sum(index) == degree:
                        self.symbols[a, index] = field if degree == 0 else s.Symbol(
                            'review_'+str(field)+'_'+''.join(map(str,index)), real=True)
        self.reverse = {value:key for key,value in self.symbols.items()}

    def jet(self, a, *axes):
        index = tuple(axes.count(i) for i in range(3))
        return self.symbols[a, index]

    def D(self, expression, axis):
        expression = s.sympify(expression)
        result = s.diff(expression, self.base[axis])
        for symbol in expression.free_symbols & self.reverse.keys():
            a, index = self.reverse[symbol]
            if sum(index) == 2:
                raise ValueError('Independent J2 derivative would need order three')
            shifted = tuple(value+int(i==axis) for i,value in enumerate(index))
            result += s.diff(expression, symbol)*self.symbols[a, shifted]
        return s.expand(result)

    def action(self, equations, generator):
        base = tuple(map(s.sympify, generator[:3]))
        eta = tuple(map(s.sympify, generator[3:]))
        phi = {(a, (0,0,0)):eta[a] for a in range(4)}
        for degree in (1,2):
            for a,index in self.symbols:
                if sum(index) != degree:
                    continue
                axis = next(i for i,value in enumerate(index) if value)
                previous = tuple(value-int(i==axis) for i,value in enumerate(index))
                value = self.D(phi[a,previous], axis)
                for j in range(3):
                    shifted = tuple(q+int(i==j) for i,q in enumerate(previous))
                    value -= self.symbols[a,shifted]*self.D(base[j],axis)
                phi[a,index] = s.expand(value)
        result=[]
        for equation in equations:
            value=sum(base[i]*s.diff(equation,self.base[i]) for i in range(3))
            for symbol in equation.free_symbols & self.reverse.keys():
                value += phi[self.reverse[symbol]]*s.diff(equation,symbol)
            result.append(s.expand(value))
        return tuple(result)

    def equations(self, transport=True, diffusion=True, exponent=m, slope=n, coriolis=f,
                  abstract=False):
        if abstract:
            flux = s.Matrix([s.Function('RF1')(u,v),s.Function('RF2')(u,v)])
            diffusivity = s.Function('RD')(u,v)
        else:
            flux = K*speed2**((s.sympify(exponent)-1)/2)*s.Matrix([u,v]) if transport else s.zeros(2,1)
            diffusivity = G*speed2**(s.sympify(slope)/2) if diffusion else s.S.Zero
        mass=self.jet(0,0)+self.D(h*u,1)+self.D(h*v,2)
        momx=self.jet(1,0)+u*self.jet(1,1)+v*self.jet(1,2)+g*(self.jet(0,1)+self.jet(3,1))-coriolis*v
        momy=self.jet(2,0)+u*self.jet(2,1)+v*self.jet(2,2)+g*(self.jet(0,2)+self.jet(3,2))+coriolis*u
        bed=self.jet(3,0)+sum(self.D(flux[i]-diffusivity*self.jet(3,i+1),i+1) for i in range(2))
        return (mass,momx,momy,bed)

    def shell(self,equations):
        rules={self.jet(a,0):s.expand(self.jet(a,0)-equations[a]) for a in range(4)}
        order=max(sum(self.reverse[q][1]) for e in equations for q in e.free_symbols & self.reverse.keys())
        if order==2:
            for a in range(3):
                for axis in (1,2):
                    rules[self.jet(a,0,axis)]=self.D(rules[self.jet(a,0)],axis)
            for a in range(3):
                rules[self.jet(a,0,0)]=self.D(rules[self.jet(a,0)],0).xreplace(rules)
        return {key:s.expand(value) for key,value in rules.items()}

    def residual(self,equations,generator):
        rules=self.shell(equations)
        return tuple(s.expand(value.xreplace(rules)) for value in self.action(equations,generator))

    def parent_map(self,parent):
        return {parent.jet(a,index):value for (a,index),value in self.symbols.items()}


R=ReviewJet()


def clean(expression):
    """Exact simplification; radial fallback uses a positive rational chart.

    u=rho*(1-z^2)/(1+z^2), v=2*rho*z/(1+z^2), rho>0 covers a dense
    velocity chart. This preserves real powers and uses no forced power rule.
    Smoothness extends a zero identity to the omitted velocity ray.
    """
    value=s.expand(expression)
    if value==0:
        return s.S.Zero
    value=s.simplify(value)
    if value==0:
        return s.S.Zero
    if any(power.base==speed2 for power in value.atoms(s.Pow)):
        rho=s.Dummy('rho',positive=True)
        z=s.Dummy('z',real=True)
        chart=value.xreplace({speed2:rho*rho}).subs(
            {u:rho*(1-z*z)/(1+z*z),v:2*rho*z/(1+z*z)},simultaneous=True)
        chart=s.simplify(s.powdenest(chart,force=False))
        if chart==0:
            return s.S.Zero
    return value


class Checks:
    def __init__(self): self.records=[]
    def __call__(self,name,values):
        if not isinstance(values,(tuple,list,s.MatrixBase)):
            values=[values]
        residuals=[clean(q) for q in values]
        bad=[str(q) for q in residuals if q!=0]
        self.records.append({'name':name,'passed':not bad,'nonzero_residuals':bad})
        if bad: raise AssertionError(name+': '+str(bad)[:1500])
    def yes(self,name,condition): self(name,0 if condition else 1)


def arbitrary(args=coords):
    return tuple(s.Function('review_'+name)(*args) for name in ('tau','xi','chi','H','U','V','Z'))


def branch_equations(name):
    cell=models.BRANCHES_2D[name]
    return R.equations(cell['K'],cell['G'],cell.get('m',m),cell.get('n',n),
                       0 if cell['coriolis']=='f0' else f)


def check_raw(check):
    cases={}
    for name in models.BRANCHES_2D:
        model=models.branch_model_2d(name)
        parent=ParentJet(model['independent_variables'],model['dependent_fields'])
        eq=branch_equations(name)
        check('independent flux/model '+name,[a-b.xreplace(R.parent_map(parent)) for a,b in zip(eq,model['equations'])])
    gen=arbitrary()
    for name in ('grass_generic_f_nonzero','slope_source_generic_f_nonzero'):
        model=models.branch_model_2d(name)
        parent=ParentJet(model['independent_variables'],model['dependent_fields'])
        eq=branch_equations(name)
        independent=R.residual(eq,gen)
        shell=frontend.MixedShell(parent,model['equations'])
        phi=parent_prolong(parent,gen[:3],gen[3:],shell.order)
        root_original=[shell.reduce(parent_action(parent,e,gen[:3],gen[3:],shell.order,coefficients=phi)) for e in model['equations']]
        root=[value.xreplace(R.parent_map(parent)) for value in root_original]
        check('unrestricted root raw determining identity '+name,[a-b for a,b in zip(independent,root)])
        for row,expression in enumerate(root_original):
            split=frontend.split_free_jets(parent,expression,shell)
            reconstructed=sum(term['coefficient']*s.prod(jet**power for jet,power in zip(split['jets'],term['powers'])) for term in split['terms'])
            check('exact jet-polynomial reconstruction '+name+'/'+str(row),
                  (expression-reconstructed/split.get('denominator',1)).xreplace(R.parent_map(parent)))
        rules=R.shell(eq)
        check('independent shell equals root shell '+name,[value-shell.rules[next(k for k,vv in R.parent_map(parent).items() if vv==key)].xreplace(R.parent_map(parent)) for key,value in rules.items()])
        if shell.order==2:
            check.yes('thirteen mixed shell constraints',len(rules)==13)
            free=set(R.reverse)-set(fields)-set(rules)
            check.yes('twenty-three free J2 jets',len(free)==23)
            check.yes('all three bed mixed/time jets remain free',all(R.jet(3,0,i) in free for i in range(3)))
            for a in range(3):
                for axis in range(3):
                    check(f'independent hydro differential consequence {a}/{axis}',R.D(eq[a],axis).xreplace(rules))
            for axis in (1,2):
                check('root splitter retains bed mixed jet '+str(axis),
                      0 if parent.jet(3,tuple(int(i==0)+int(i==axis) for i in range(3))) in frontend.split_free_jets(parent,parent.jet(3,tuple(int(i==0)+int(i==axis) for i in range(3))),shell)['jets'] else 1)
        cases[name]={'raw_components_compared':4,'shell_constraints':len(rules)}
    # Compare the separately authored first-order calculation with the same
    # unrestricted coefficients, including the mixed x/y quadratic monomials.
    own=R.residual(R.equations(diffusion=False),gen)
    acoords=first_author.COORDINATES
    agen=arbitrary(acoords)
    amap=dict(zip(acoords,coords))
    amap.update({first_author.g:g,first_author.K:K,first_author.m:m,first_author.f:f})
    amap.update({first_author.px[a]:R.jet(a,1) for a in range(4)})
    amap.update({first_author.py[a]:R.jet(a,2) for a in range(4)})
    authored=first_author.direct_prolongation(agen,simplify=False)
    check('author first-order unrestricted raw identity',[own[a]-authored[a].xreplace(amap) for a in range(4)])
    # Arbitrary D,F comparison proves the whole slope operator equality, not
    # merely finitely many exponent substitutions.
    eq=R.equations(abstract=True)
    own=R.residual(eq,gen)
    amap=dict(zip(slope_author.coordinates,coords))
    amap.update({slope_author.g:g,slope_author.f:f})
    amap.update({slope_author.abstract_D:s.Function('RD')(u,v),
                 slope_author.abstract_F[0]:s.Function('RF1')(u,v),slope_author.abstract_F[1]:s.Function('RF2')(u,v)})
    for (a,i),symbol in slope_author.first.items(): amap[symbol]=R.jet(a,i)
    for (a,i,j),symbol in slope_author.second.items(): amap[symbol]=R.jet(a,i,j)
    authored=slope_author.residuals(arbitrary(slope_author.coordinates))
    check('author slope unrestricted raw identity for arbitrary diffusivity and flux',[own[a]-authored[a].xreplace(amap) for a in range(4)])
    return {'raw_cases':cases}


def check_necessity(check):
    eq=R.equations(abstract=True)
    D=s.Function('RD')(u,v)
    F=s.Matrix([s.Function('RF1')(u,v),s.Function('RF2')(u,v)])
    gen=list(arbitrary())
    raw=R.residual(eq,gen)
    for axis in (1,2):
        check('unrestricted mixed-bed coefficient '+str(axis),s.diff(raw[3],R.jet(3,0,axis))-2*D*R.D(gen[0],axis))
    gen[0]=s.Function('tau')(t)
    raw=R.residual(eq,gen)
    for a in range(3):
        check('fluid Hessian coefficient '+str(a),s.diff(raw[3],R.jet(a,1,1))+D*(s.diff(gen[6],fields[a])-sum(R.jet(3,i+1)*s.diff(gen[i+1],fields[a]) for i in range(2))))
    for i in (1,2,6): gen[i]=s.Function('restricted_'+str(i))(t,x,y,B)
    raw=R.residual(eq,gen)
    etaD=s.diff(D,u)*gen[4]+s.diff(D,v)*gen[5]
    for i in (1,2):
        check('diagonal bed Hessian '+str(i),s.diff(raw[3],R.jet(3,i,i))-D*(2*s.diff(gen[i],coords[i])-s.diff(gen[0],t)+2*R.jet(3,i)*s.diff(gen[i],B))+etaD)
    check('off-diagonal bed Hessian factor two',s.diff(raw[3],R.jet(3,1,2))-2*D*(s.diff(gen[1],y)+s.diff(gen[2],x)+R.jet(3,2)*s.diff(gen[1],B)+R.jet(3,1)*s.diff(gen[2],B)))
    # The entire arbitrary-time hydro family is checked independently.
    tau=s.Function('T')(t); k,omega0=s.symbols('k omega0',real=True)
    shift=s.Matrix([s.Function('p')(t),s.Function('q')(t)])
    pos=s.Matrix([x,y]); vel=s.Matrix([u,v])
    sigma=s.diff(tau,t)/2+k; omega=omega0-f*tau/2
    A=sigma*s.eye(2)+omega*ROT; alpha=sigma-s.diff(tau,t)
    spatial=A*pos+shift; b=spatial.diff(t)+(A-s.diff(tau,t)*s.eye(2))*vel
    psi=-(s.diff(tau,t,3)+f*f*s.diff(tau,t))*(x*x+y*y)/(4*g)
    psi-=((shift.diff(t,2)+f*ROT*shift.diff(t)).dot(pos))/g
    psi+=s.Function('S')(t)
    raw=R.residual(eq,(tau,*spatial,2*alpha*h,*b,2*alpha*B+psi))
    check('arbitrary-time hydro family, all components',raw[:3])
    gradB=s.Matrix([R.jet(3,1),R.jet(3,2)])
    gradpsi=s.Matrix([s.diff(psi,x),s.diff(psi,y)])
    def div(vector): return sum(R.D(vector[i],i+1) for i in range(2))
    chi=2*alpha; etaD=s.diff(D,u)*b[0]+s.diff(D,v)*b[1]
    expected=(chi-s.diff(tau,t))*R.shell(eq)[R.jet(3,0)]+s.diff(chi,t)*B+s.diff(psi,t)-spatial.diff(t).dot(gradB)
    expected+=div(F.jacobian((u,v))*b-A*F)
    expected-=div(((etaD+chi*D)*s.eye(2)-D*(A+A.T))*gradB+D*gradpsi)
    check('full bed divergence identity with arbitrary-time hydro coefficients',raw[3]-expected)
    # Homogeneity/nonvanishing identities with actual real powers.
    flux=K*speed2**((m-1)/2)*vel; diffusivity=G*speed2**(n/2)
    aa,ww=s.symbols('aa ww',real=True); M=aa*s.eye(2)+ww*ROT
    check('radial vector covariance',flux.jacobian((u,v))*M*vel-(m*aa*s.eye(2)+ww*ROT)*flux)
    check('radial scalar covariance',sum(s.diff(diffusivity,vel[i])*(M*vel)[i] for i in range(2))-n*aa*diffusivity)
    check('transport nonzero without dividing a velocity component',(vel.T*flux.jacobian((u,v))*vel)[0]-m*K*speed2**((m+1)/2))
    # Independent directional spectral identities; inequalities are adjudicated
    # analytically in the review report, never inferred from these identities.
    qa,qb=s.symbols('qa qb',real=True); lam=s.Symbol('lambda')
    core=s.Matrix([[u,h,0],[g,u,g],[0,qa,0]])
    sym=s.diag(g/h,1,g/qa)*core
    check('positive directional symmetrizer',sym-sym.T)
    check('transverse eigenvalue separates from core',core.charpoly(lam).as_expr().subs(lam,u)+g*h*u)
    full=s.Matrix([[u,h,0,0],[g,u,0,g],[0,0,u,0],[0,qa,qb,0]])
    check('zero-transport directional spectrum',full.subs({qa:0,qb:0}).charpoly(lam).as_expr()-lam*(lam-u)*((lam-u)**2-g*h))
    right=s.Matrix([-qb/u,0,1,qb/u]); left=s.Matrix([[0,0,1,0]])
    check('passive right eigenpair',full*right-u*right)
    check('passive left eigenpair',left*full-u*left)
    # Explicit failures that would otherwise reintroduce excluded families.
    boost=R.residual(R.equations(transport=False,diffusion=False,coriolis=0),(0,t,0,0,1,0,0))
    check('static full bed rejects boost with exact residual',s.Matrix(boost)-s.Matrix([0,0,0,-R.jet(3,1)]))
    nonlinear=(0,x*x-y*y,2*x*y,4*x*h,2*x*u-2*y*v,2*y*u+2*x*v,4*x*B)
    check('nonlinear conformal field rejected in mass row',R.residual(R.equations(transport=False,diffusion=False,coriolis=0),nonlinear)[0]-8*h*u)
    return {'necessity_review':'All arbitrary-function integrations reviewed in CLASSIFICATION_2D_REVIEW.md; finite checks substantiate the coefficient identities.'}


def check_branches(check):
    branches={}
    for name,cell in models.BRANCHES_2D.items():
        author=slope_author if cell['G'] else first_author
        solved=author.general_solution(name,coordinates=coords)
        integral=tuple(solved['coefficients'])
        check('independent original-PDE general integral '+name,R.residual(branch_equations(name),integral))
        basis=[s.Matrix(integral).diff(c) for c in solved['free_constants']]
        columns=[]
        for vector in basis:
            columns.append([s.expand(q).coeff(z) for q in vector for z in coords]+[q.subs(dict.fromkeys(coords,0)) for q in vector])
        rank=s.Matrix.hstack(*(s.Matrix(col) for col in columns)).rank()
        check('basis function independence '+name,rank-len(basis))
        rotating=cell['coriolis']!='f0'
        if cell['G']:
            expected=5+int((not cell['K'] or cell['m']==3) and (not rotating or cell['n']==2))
        else:
            expected=(5 if rotating else 6)+int(not cell['K'] or cell['m']==3)
        check('dimension and parameter rank '+name,len(basis)-expected)
        restriction=models.recover_one_dimension(name)
        check('one-dimensional longitudinal restriction '+name,restriction['one_dimensional_residuals'])
        from models import u as u1
        check('transverse Coriolis restriction '+name,restriction['transverse_residual']-(f*u1 if rotating else 0))
        branches[name]={'passed':True,'dimension':len(basis),'general_coefficients':[str(q) for q in integral],
                        'constant_equations':[str(q) for q in solved['constant_equations']],
                        'one_dimensional_restriction':not rotating}
    # Endpoints and changes in the geometry of D_n must not silently be lost.
    for exponent in (0,1,2,3,4,s.Rational(3,2)):
        solved=slope_author.general_solution('slope_only_f0',coordinates=coords,exponent=exponent)
        check('slope-only continuous-family specialization '+str(exponent),R.residual(R.equations(transport=False,slope=exponent,coriolis=0),tuple(solved['coefficients'])))
    for exponent in (1,4,s.Rational(3,2)):
        solved=first_author.general_solution('grass_generic_f0',coordinates=coords,exponent=exponent)
        check('first-order endpoint/noninteger specialization '+str(exponent),R.residual(R.equations(diffusion=False,exponent=exponent,coriolis=0),tuple(solved['coefficients'])))
    return {'branches':branches}


def direct_graph(equations,graph,base=(t,x,y)):
    substitution={}
    for symbol,(a,index) in R.reverse.items():
        value=graph[a]
        for axis,count in enumerate(index):
            for _ in range(count): value=s.diff(value,base[axis])
        substitution[symbol]=value
    return tuple(e.xreplace(substitution) for e in equations)


def check_reductions(check):
    records={}
    for name in ('grass_generic_f0','slope_source_generic_f_nonzero','slope_only_f0'):
        reduction=reductions.plane_wave(name)
        check.yes('plane wave API status '+name,reduction['status']=='verified_ode_reduction')
        pulled=direct_graph(branch_equations(name),reduction['graph'])
        z=reduction['reduced_independent_variables'][0]
        check('independent Cartesian plane-wave pullback '+name,[a-b.subs(z,reduction['invariant']) for a,b in zip(pulled,reduction['reduced_equations'])])
        check('plane-wave projection rank '+name,reduction['projection_rank']-2)
        records[name+'/plane_wave']={'passed':True,'projection_rank':2,'type':'ODE/DAE'}
    for name in ('zero_transport_f_nonzero','slope_attachment_cubic_f_nonzero','slope_only_n2_f_nonzero'):
        reduction=reductions.rotation_scaling_time_ode(name)
        check.yes('time ODE API status '+name,reduction['status']=='verified_ode_reduction')
        raw=direct_graph(branch_equations(name),reduction['graph'])
        rr=x*x+y*y; E=reduction['reduced_equations']
        check('independent Cartesian time-ODE pullback '+name,[raw[0]-rr*E[0],raw[1]-x*E[1]+y*E[2],raw[2]-y*E[1]-x*E[2],raw[3]-rr*E[3]])
        check('rotation-scaling base minor '+name,reduction['projection_minor']+rr)
        records[name+'/time_ode']={'passed':True,'projection_rank':2,'type':'ODE','chart':'x^2+y^2>0'}
    special=reductions.rotation_scaling_time_ode('slope_only_f0',diffusion_exponent=2)
    check.yes('nonrotating slope n=2 slice accessible',special['status']=='verified_ode_reduction')
    H,A,W,Z=special['profiles']; E=special['reduced_equations']
    check('nonrotating n=2 time ODE explicit formula',s.Matrix(E)-s.Matrix([s.diff(H,t)+4*A*H,s.diff(A,t)+A*A-W*W+2*g*(H+Z),s.diff(W,t)+2*A*W,s.diff(Z,t)-8*G*(A*A+W*W)*Z]))
    # Independently differentiate a Cartesian radial graph on x>0, then take
    # the y=0 cross-section. The verified joint rotation transports this local
    # identity to every r>0 orbit; no value at r=0 is inferred.
    name='slope_attachment_cubic_f_nonzero'
    reduction=reductions.rotating_radial(name)
    xp=s.Symbol('review_positive_x',positive=True); yp=s.Symbol('review_y',real=True)
    radius=s.sqrt(xp*xp+yp*yp)
    H,U,V,Z=reduction['profiles']; radial=reduction['reduced_independent_variables'][1]
    graph=(H.subs(radial,radius),(xp*U-yp*V).subs(radial,radius)/radius,
           (yp*U+xp*V).subs(radial,radius)/radius,Z.subs(radial,radius))
    raw=direct_graph(branch_equations(name),graph,base=(t,xp,yp))
    section=[s.simplify(q.subs(yp,0).doit()) for q in raw]
    check('independent Cartesian radial cross-section',[a-b.subs(radial,xp) for a,b in zip(section,reduction['reduced_equations'])])
    check('radial base rank is one',reduction['projection_rank']-1)
    check.yes('radial reduction explicitly retains PDE',reduction['ode_claim'] is False and len(reduction['reduced_independent_variables'])==2)
    check('polar inverse chart determinant',reduction['base_jacobian']-radial)
    records[name+'/radial']={'passed':True,'projection_rank':1,'type':'PDE in t,r','chart':'r>0, local angle'}
    # Negative controls and the earlier fixes.
    for invalid in (s.I,s.oo,s.nan):
        rejected=False
        try: reductions.plane_wave('grass_generic_f0',invalid)
        except ValueError: rejected=True
        check.yes('non-real/non-finite wave speed rejected '+str(invalid),rejected)
    bad=reductions.rotation_scaling_time_ode('slope_source_cubic_f_nonzero')
    check.yes('unsupported pure spatial scaling rejected',bad['status']=='generator_not_admitted')
    bad=R.residual(R.equations(),(0,-y,x,0,0,0,0))
    check.yes('spatial-only rotation fails the original equations',any(clean(q)!=0 for q in bad))
    z=s.Symbol('z',real=True); Hp,Up,Zp=(s.Function(q)(x-t) for q in ('Hp','Up','Zp'))
    bad=direct_graph(R.equations(diffusion=False),(Hp,Up,s.S.Zero,Zp))
    check('naive transverse-zero wave retains f U',bad[2]-f*Up)
    return {'reduction_cases':records}


def gate_controls(check):
    names=tuple(models.BRANCHES_2D)
    contents={'virtual/'+name:(HERE/name).read_bytes() for name in INPUTS}
    class MemoryPath:
        def __init__(self,value): self.value=value.value if isinstance(value,MemoryPath) else str(value)
        def __truediv__(self,value): return MemoryPath(self.value+'/'+str(value))
        def exists(self): return self.value in contents
        def is_file(self): return self.exists()
        def read_bytes(self): return contents[self.value]
        def read_text(self,encoding='utf-8'): return self.read_bytes().decode(encoding)
    good={'inputs_sha256':SNAPSHOT,'all_checks_passed':True,'branches':{name:{'passed':True} for name in names},
          'verdicts':{name:'accepted virtual test only' for name in ('first_order','slope','root_analyzer')}}
    def evaluate(record):
        contents['virtual/receipt.json']=json.dumps(record).encode()
        with patch.object(classifier,'Path',MemoryPath):
            return classifier.review_gate('virtual/receipt.json',root='virtual')
    check.yes('virtual exact review accepted',evaluate(good)['passed'])
    for label,mutate in (
        ('missing model dependency',lambda q:q['inputs_sha256'].pop('models.py')),
        ('missing branch',lambda q:q['branches'].pop(names[-1])),
        ('extra branch',lambda q:q['branches'].update({'invented':{'passed':True}})),
        ('failed branch',lambda q:q['branches'][names[0]].update(passed=False)),
        ('partial review',lambda q:q.update(all_checks_passed=False)),
        ('rejected necessity',lambda q:q['verdicts'].update(slope='rejected')),
    ):
        record=json.loads(json.dumps(good));mutate(record)
        check.yes('virtual gate rejects '+label,not evaluate(record)['passed'])
    original=contents['virtual/analyze_2d.py']; contents['virtual/analyze_2d.py']+=b'\n# changed'
    check.yes('virtual gate rejects changed source',not evaluate(good)['passed'])
    contents['virtual/analyze_2d.py']=original
    return {'virtual_gate_controls':8,'live_gate_created_by_fixture':False}


def stage_gate_controls(check):
    """Exercise release mutations entirely in memory; never create a live gate."""
    import stage2_gate as release
    import stage2_runner
    import run_all
    names=tuple(models.BRANCHES_2D)
    contents={}
    def put(path,value):
        contents[path]=json.dumps(value).encode() if isinstance(value,(dict,list)) else value
    def digest(path):return hashlib.sha256(contents[str(path)]).hexdigest()
    class MemoryPath:
        def __init__(self,value):self.value=value.value if isinstance(value,MemoryPath) else str(value)
        def __str__(self):return self.value
        def __truediv__(self,value):return MemoryPath(self.value+'/'+str(value))
        def __eq__(self,other):return self.value==str(other)
        def __hash__(self):return hash(self.value)
        def resolve(self):return self
        def is_relative_to(self,other):return self.value==str(other) or self.value.startswith(str(other)+'/')
        def relative_to(self,other):
            if not self.is_relative_to(other):raise ValueError('outside virtual cycle')
            return MemoryPath(self.value[len(str(other))+1:])
        def exists(self):return self.value in contents
        def is_file(self):return self.exists()
        def read_bytes(self):return contents[self.value]
        def read_text(self,encoding='utf-8'):return self.read_bytes().decode(encoding)
        def write_text(self,value,encoding='utf-8'):contents[self.value]=value.encode(encoding)
    source_names=list(INPUTS)+['data_experiments_2d.py','algebra_2d.py']+['cases_2d/'+name+'.py' for name in names]
    for name in source_names:put('cycle/'+name,('fixture source '+name).encode())
    snapshot={name:digest('cycle/'+name) for name in source_names}
    put('cycle/STAGE_1_GATE.json',{'passed':True})
    put('cycle/classification_2d_review.json',{'all_checks_passed':True})
    run={'execution_passed':True,'sources_unchanged_during_run':True,
         'source_hashes_before':snapshot,'source_hashes_after':snapshot,'receipts':[]}
    for name in names:
        log='cycle/branches/'+name+'.log';artifact='cycle/branches/'+name+'/derivation.json'
        put(log,b'completed child fixture')
        put(artifact,{'model_id':'2d__'+name,'classification_status':'proved_for_declared_regular_chart',
                      'generator_verification':'verified','reduction_status':'verified_specified_reductions',
                      'data_status':'verified_specified_data_controls'})
        run['receipts'].append({'branch':name,'exit_code':0,'process_status':'exited','log':log,
                                'log_sha256':digest(log),'derivation_sha256':digest(artifact),
                                'child_sha256':digest('cycle/cases_2d/'+name+'.py')})
    validation={'all_protected_inputs_unchanged':True,'sources_unchanged_during_run':True,
                'source_hashes_before':snapshot,'source_hashes_after':snapshot,'receipts':[]}
    for name in ('audit','data-flux','workflow','engine-chart','active-package','new-cycle'):
        log='cycle/validation/'+name+'.log';put(log,b'completed validation fixture')
        validation['receipts'].append({'name':name,'exit_code':0,'process_status':'exited','log':log,'log_sha256':digest(log)})
    additional=['cycle/data_2d_review.json','cycle/algebra_2d_review.json']
    notes=('DATA_CONTROLS_2D.md','ALGEBRA_2D.md')
    for path,implementation,note in zip(additional,('data_experiments_2d.py','algebra_2d.py'),notes):
        put('cycle/'+note,('reviewed note '+note).encode())
        put(path,{'all_checks_passed':True,'review_status':'accepted',
                  'inputs_sha256':{implementation:snapshot[implementation],note:digest('cycle/'+note)}})
    baseline_contents=dict(contents)
    def evaluate(mutate=None):
        contents.clear();contents.update(baseline_contents)
        rr=json.loads(json.dumps(run));vv=json.loads(json.dumps(validation));aa=list(additional)
        if mutate:mutate(rr,vv,aa)
        put('cycle/branches/receipts.json',rr);put('cycle/validation/receipts.json',vv)
        def compare(hashes):return [name for name,value in hashes.items() if digest('cycle/'+name)!=value]
        with (patch.object(release,'Path',MemoryPath),patch.object(release,'HERE',MemoryPath('cycle')),
             patch.object(release,'ROOT',MemoryPath('project')),patch.object(release,'digest',digest),
             patch.object(release,'check_hashes',compare),patch.object(release,'check_gate',lambda n:{'passed':True}),
             patch.object(classifier,'review_gate',lambda:{'passed':True}),
             patch.object(stage2_runner,'source_hashes',lambda:snapshot),patch.object(run_all,'source_hashes',lambda:snapshot)):
            return release.create_stage2('cycle/branches','cycle/validation',aa)
    accepted=evaluate()
    check.yes('virtual stage2 complete evidence accepted',accepted['passed'])
    check.yes('virtual stage2 binds all nested reviewed Markdown',all(note in accepted['evidence_sha256'] for note in notes))
    # Read the created virtual gate with the real gate-checking implementation.
    # Its nested note is absent from the Python source inventory, so only the
    # repaired evidence transitive closure can detect this post-release edit.
    import gatekeeper
    with (patch.object(gatekeeper,'Path',MemoryPath),patch.object(gatekeeper,'HERE',MemoryPath('cycle')),
          patch.object(classifier,'review_gate',lambda:{'passed':True})):
        check.yes('virtual completed stage2 passes actual checker',gatekeeper.check_gate(2)['passed'])
        contents['cycle/'+notes[0]]+=b'\npost-release edit'
        stale=gatekeeper.check_gate(2)
        check.yes('actual gate checker rejects changed nested Markdown',
                  not stale['passed'] and notes[0] in stale.get('changed',[]))
    mutations=(
        ('empty branch source set',lambda rr,vv,aa:rr.update(source_hashes_before={},source_hashes_after={})),
        ('empty validation source set',lambda rr,vv,aa:vv.update(source_hashes_before={},source_hashes_after={})),
        ('missing child',lambda rr,vv,aa:rr['receipts'].pop()),
        ('duplicate child',lambda rr,vv,aa:rr['receipts'].__setitem__(-1,rr['receipts'][0])),
        ('failed child exit',lambda rr,vv,aa:rr['receipts'][0].update(exit_code=1)),
        ('timed out child',lambda rr,vv,aa:rr['receipts'][0].update(process_status='timeout')),
        ('changed derivation',lambda rr,vv,aa:put('cycle/branches/'+names[0]+'/derivation.json',{'model_id':'tampered'})),
        ('missing derivation digest',lambda rr,vv,aa:rr['receipts'][0].pop('derivation_sha256')),
        ('timed out validation',lambda rr,vv,aa:vv['receipts'][0].update(process_status='timeout')),
        ('wrong canonical validation log',lambda rr,vv,aa:vv['receipts'][0].update(log=vv['receipts'][1]['log'])),
        ('failed non-audit validation',lambda rr,vv,aa:vv['receipts'][1].update(exit_code=1)),
        ('omitted additional reviews',lambda rr,vv,aa:aa.clear()),
        ('rejected additional review',lambda rr,vv,aa:put(aa[0],{'all_checks_passed':True,'review_status':'rejected','inputs_sha256':{'data_experiments_2d.py':snapshot['data_experiments_2d.py']}})),
        ('unbound additional review',lambda rr,vv,aa:put(aa[0],{'all_checks_passed':True,'review_status':'accepted','inputs_sha256':{'main.py':snapshot['main.py']}})),
    )
    for name,mutation in mutations:
        rejected=False
        try:evaluate(mutation)
        except (ValueError,KeyError):rejected=True
        check.yes('virtual stage2 rejects '+name,rejected)
    return {'virtual_stage2_controls':4+len(mutations),'live_stage2_gate_written':False}


def check_adapter(check):
    records={}
    from radial_normal_form import normalize
    exponent=s.Symbol('review_exponent',real=True)
    identity=u*u*speed2**exponent+v*v*speed2**exponent-speed2**(exponent+1)
    check('root radial normalizer exact same-base identity',normalize(identity,u,v))
    check('root radial normalizer retains a nonzero remainder',normalize(identity+1,u,v)-1)
    check('independent rational-chart validation of root normalization',clean(identity))
    for name in ('grass_generic_f_nonzero','slope_only_n2_f_nonzero'):
        report=frontend.analyze(**models.branch_model_2d(name))
        integration=report['integration']
        check.yes('actual frontend integrates '+name,integration['status'] in ('necessity_integrated_pending_review','proved_for_declared_regular_chart'))
        check('actual frontend general-integral raw DE remainders '+name,integration['raw_DE_remainders'])
        check.yes('actual frontend sufficient basis '+name,all(q['verified'] for q in integration['candidate_checks']))
        check('actual frontend shell count '+name,report['shell_constraint_count']-(13 if models.BRANCHES_2D[name]['G'] else 4))
        altered=dict(report,equations=tuple(report['equations'][:-1])+(report['equations'][-1]+1,))
        check.yes('model fingerprint refuses changed equation '+name,classifier.integrate_sve_2d(altered)['status']=='unresolved')
        altered=dict(report,branch_conditions=dict(report['branch_conditions'],unreviewed_guard=True))
        check.yes('model fingerprint refuses changed guards '+name,classifier.integrate_sve_2d(altered)['status']=='unresolved')
        records[name]={'determining_equations':len(report['determining_equations']),'dimension':integration['dimension'],
                       'elapsed_seconds':report['elapsed_seconds'],'shell_constraints':report['shell_constraint_count']}
    records.update(gate_controls(check))
    records.update(stage_gate_controls(check))
    return {'adapter_cases':records}


def run(phase):
    started=time.perf_counter(); path=HERE/'classification_2d_review.json'
    old=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    history=list(old.get('prior_attempts',[]))
    if old and old.get('inputs_sha256')!=SNAPSHOT:
        history.append({'status':'superseded_input_version','completed_phases':list(old.get('phases',{})),
                        'previous_all_checks_passed':old.get('all_checks_passed',False)})
        old={}
    result=old or {'reviewer_role':'fresh independent reviewer, not a derivation author',
                   'inputs_sha256':SNAPSHOT,'phases':{},'branches':{},'verdicts':{},'all_checks_passed':False}
    result['prior_attempts']=history
    result['all_checks_passed']=False
    check=Checks()
    try:
        if phase!='finalize':
            action=globals()['check_'+phase]
            data=action(check)
            result['phases'][phase]={'passed':True,'checks':check.records,
                                     'elapsed_seconds':time.perf_counter()-started,**data}
            if 'branches' in data:result['branches']=data['branches']
        changed=[name for name,digest in hashes().items() if digest!=SNAPSHOT[name]]
        if changed:raise AssertionError('review inputs changed during execution: '+str(changed))
        result['input_snapshot_unchanged_through_execution']=True
        if phase=='finalize':
            if set(result['phases'])!=set(PHASES) or not all(q['passed'] for q in result['phases'].values()):
                raise AssertionError('All five independent review phases must pass')
            if set(result['branches'])!=set(models.BRANCHES_2D):raise AssertionError('Incomplete branch coverage')
            result['verdicts']={
                'first_order':'accepted: unrestricted necessity and sufficiency on the declared open chart',
                'slope':'accepted: unrestricted mixed-order necessity and sufficiency on the declared open chart',
                'root_analyzer':'accepted: independently checked raw DEs, mixed J2 shell and exact model fingerprints',
                'reductions':'accepted: specified rank-one PDE and rank-two ODE/DAE charts, not an optimal system',
                'review_gate':'accepted: exact-version hash and branch coverage controls; virtual fixtures only',
            }
            result['all_checks_passed']=True
        result['check_count']=sum(len(q.get('checks',[])) for q in result['phases'].values())
        result['proof_review']='CLASSIFICATION_2D_REVIEW.md'
        result['limitations']=['No zero-speed/zero-depth classification','No full disconnected point-equivalence groupoid',
                              'No optimal-subalgebra completeness in 2D','No arbitrary-data or well-posedness theorem',
                              'No conditional/nonclassical or ML claim','Finite checks substantiate, not replace, the necessity proof']
        path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        if phase=='finalize' and not classifier.review_gate()['passed']:
            raise AssertionError('Live exact-version gate rejected the finalized review')
        print(json.dumps({'phase':phase,'phase_checks':len(check.records),'total_checks':result['check_count'],
                          'elapsed_seconds':time.perf_counter()-started,'all_checks_passed':result['all_checks_passed']},indent=2))
    except Exception as exc:
        result['all_checks_passed']=False
        result['prior_attempts'].append({'phase':phase,'status':'failed','error':repr(exc),
                                         'elapsed_seconds':time.perf_counter()-started,'checks':check.records})
        path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=PHASES+('finalize',),required=True)
    run(parser.parse_args().phase)
