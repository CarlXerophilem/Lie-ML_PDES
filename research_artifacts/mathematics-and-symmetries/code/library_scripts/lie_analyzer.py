#!/usr/bin/env python3
"""ML-free seven-step Lie analysis for local 1D/2D PDE systems.

Only SymPy and the Python standard library are required. Classification is
within an explicitly bounded polynomial point-generator ansatz. Supported
reductions have explicit charts; a missing chart is reported, never guessed.
"""
import argparse
import ast
import itertools
import json
import math
import time
from pathlib import Path
import sympy as sp


def safe_expr(text,names):
    """Small arithmetic DSL; no eval, attributes, imports, or Python calls."""
    functions={'sin':sp.sin,'cos':sp.cos,'exp':sp.exp,'log':sp.log,'sqrt':sp.sqrt,'tanh':sp.tanh}
    def walk(n):
        if isinstance(n,ast.Constant) and type(n.value) in (int,float):return sp.Rational(str(n.value))
        if isinstance(n,ast.Name) and n.id in names:return names[n.id]
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            return walk(n.operand) if isinstance(n.op,ast.UAdd) else -walk(n.operand)
        if isinstance(n,ast.BinOp):
            a,b=walk(n.left),walk(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
            if isinstance(n.op,ast.Pow):return a**b
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in functions and len(n.args)==1 and not n.keywords:
            return functions[n.func.id](walk(n.args[0]))
        raise ValueError(f'Unsupported expression syntax: {ast.dump(n)}')
    return walk(ast.parse(str(text),mode='eval').body)


def multiindices(n,order):
    return sorted((a for a in itertools.product(range(order+1),repeat=n) if sum(a)<=order),key=lambda a:(sum(a),a))


class System:
    def __init__(self,config):
        self.config=config;self.dim=config['spatial_dimension']
        if type(self.dim) is not int or self.dim not in (1,2):raise ValueError('Spatial dimension must be integer 1 or 2')
        self.x=(sp.Symbol('t',positive=True),*sp.symbols('x y' if self.dim==2 else 'x',real=True,seq=True))
        self.fields=tuple(sp.Symbol(n,positive=True) if n in config.get('positive_fields',[]) else sp.Symbol(n,real=True)
                          for n in config['fields'])
        if len(set(config['fields']))!=len(self.fields):raise ValueError('Duplicate field names')
        if any(not n.isidentifier() or n in ['t','x','y','sin','cos','exp','log','sqrt','tanh'] for n in config['fields']):
            raise ValueError('Fields must have distinct nonreserved identifier names')
        self.order=config.get('order',1)
        if type(self.order) is not int or self.order not in (1,2,3):raise ValueError('Jet order must be integer 1, 2, or 3')
        self.indices=multiindices(len(self.x),self.order)
        self.jets={}
        for field in self.fields:
            for index in self.indices:
                suffix=''.join(str(x)*n for x,n in zip(self.x,index))
                self.jets[(field,index)]=field if not suffix else sp.Symbol(str(field)+'_'+suffix,real=True)
        self.names={str(v):v for v in (*self.x,*self.jets.values())}
        self.parameters=[];self.parameter_values={}
        for name,spec in config.get('parameters',{}).items():
            if name in self.names:raise ValueError('Parameter name collides with a coordinate or jet')
            spec=spec if isinstance(spec,dict) else {'value':spec}
            symbol=sp.Symbol(name,**{a:True for a in spec.get('assumptions',['real'])})
            self.names[name]=symbol;self.parameters.append(symbol)
            if spec.get('value') is not None:self.parameter_values[symbol]=safe_expr(spec['value'],self.names)
        self.equations=sp.Matrix([safe_expr(e,self.names).subs(self.parameter_values) for e in config['equations']])
        if len(self.equations)!=3 and not config.get('allow_other_equation_count',False):
            raise ValueError('Main contract requires 3 equations: one constraint/conservation plus two main equations')
        roles=config.get('roles',['constraint/conservation','main','main'])
        if len(roles)!=len(self.equations):raise ValueError('Equation roles must match equation count')
        self.leaders=tuple(self.names[n] for n in config['leaders'])
        if len(set(self.leaders))!=len(self.equations):raise ValueError('One distinct declared leader per equation required')
        if any(l not in self.jets.values() or l in self.fields for l in self.leaders):raise ValueError('Leaders must be derivative jets')
        # Prolong lower-order equations to the common jet order before restricting.
        # This is especially important for divergence constraints beside momentum.
        chart_equations=list(self.equations);chart_leaders=list(self.leaders)
        lookup={jet:(field,index) for (field,index),jet in self.jets.items()}
        for equation,leader in zip(self.equations,self.leaders):
            used_order=max((sum(index) for (field,index),jet in self.jets.items() if jet in equation.free_symbols),default=0)
            for alpha in multiindices(len(self.x),self.order-used_order)[1:]:
                derived=equation
                for i,k in enumerate(alpha):
                    for _ in range(k):derived=self.total(derived,i)
                field,index=lookup[leader];following=tuple(a+b for a,b in zip(index,alpha))
                derived_leader=self.jets[(field,following)]
                if derived_leader in chart_leaders:continue
                chart_equations.append(derived);chart_leaders.append(derived_leader)
        self.chart_equations=sp.Matrix(chart_equations);self.chart_leaders=tuple(chart_leaders)
        jac=self.chart_equations.jacobian(self.chart_leaders);self.leader_determinant=sp.factor(jac.det())
        if self.leader_determinant==0:raise ValueError('Singular declared leading-jet chart')
        solutions=sp.solve(chart_equations,self.chart_leaders,dict=True)
        if len(solutions)!=1:raise ValueError('A unique leading-jet chart is required; split branches explicitly')
        self.rules=solutions[0]
        if any(v.free_symbols & set(self.chart_leaders) for v in self.rules.values()):raise ValueError('Nontriangular leading-jet solution')
        self.zero=(0,)*len(self.x)

    def total(self,expr,i):
        result=sp.diff(expr,self.x[i])
        for (field,index),jet in self.jets.items():
            if sum(index)>=self.order:continue
            following=list(index);following[i]+=1
            result+=sp.diff(expr,jet)*self.jets[(field,tuple(following))]
        return sp.expand(result)

    def prolong(self,vector):
        xi=vector[:len(self.x)];eta=vector[len(self.x):]
        coefficients=dict(zip(self.x,xi))
        for field,base in zip(self.fields,eta):
            calculated={self.zero:base}
            for index in self.indices[1:]:
                i=next(i for i,n in enumerate(index) if n)
                previous=list(index);previous[i]-=1;previous=tuple(previous)
                value=self.total(calculated[previous],i)
                for j in range(len(self.x)):
                    following=list(previous);following[j]+=1
                    value-=self.jets[(field,tuple(following))]*self.total(xi[j],i)
                calculated[index]=sp.expand(value)
            coefficients.update({self.jets[(field,index)]:value for index,value in calculated.items()})
        return coefficients

    def action(self,expressions,vector):
        coef=self.prolong(vector)
        return sp.Matrix([sum(sp.diff(e,z)*v for z,v in coef.items()) for e in expressions])

    def restrict(self,expr):
        return sp.factor(sp.cancel(expr.subs(self.rules,simultaneous=True)))

    def verify(self,vector):
        defects=[sp.simplify(self.restrict(e)) for e in self.action(self.equations,vector)]
        return {'verified':all(e==0 for e in defects),'on_shell_defects':list(map(str,defects))}

    def affine_ansatz(self,degree=1):
        base=(*self.x,*self.fields)
        monomials=[sp.prod(z**p for z,p in zip(base,a)) for a in multiindices(len(base),degree)]
        coefficients=sp.symbols(f'c0:{len(base)*len(monomials)}')
        vector=sp.Matrix([sum(c*m for c,m in zip(coefficients[i*len(monomials):(i+1)*len(monomials)],monomials))
                          for i in range(len(base))])
        return vector,coefficients

    def classify(self,degree=1):
        tic=time.perf_counter();vector,unknowns=self.affine_ansatz(degree)
        determining=[self.restrict(e) for e in self.action(self.equations,vector)]
        equations=[];denominators=[]
        splitting=(*self.x,*self.jets.values())
        for expression in determining:
            numerator,denominator=sp.together(expression).as_numer_denom();denominators.append(str(denominator))
            try:poly=sp.Poly(sp.expand(numerator),*splitting)
            except sp.PolynomialError:
                return {'status':'nonpolynomial-split-unsupported','degree':degree,'unknowns':len(unknowns),
                        'seconds':time.perf_counter()-tic,'basis':[],
                        'reason':'Use exact candidate verification or declare an independent nonpolynomial splitting basis; no numerical rank classification substituted.'}
            equations.extend(poly.coeffs())
        matrix,rhs=sp.linear_eq_to_matrix(equations,unknowns)
        if any(rhs):raise ValueError('Determining system unexpectedly inhomogeneous')
        # Exact sparse row deduplication reduces the solve without changing its kernel.
        unique={tuple(row) for row in matrix.tolist() if any(row)}
        matrix=sp.Matrix(sorted(unique,key=str)) if unique else sp.zeros(0,len(unknowns))
        nullspace=matrix.nullspace();basis=[vector.subs(dict(zip(unknowns,v))) for v in nullspace]
        verification=[self.verify(v) for v in basis]
        if not all(v['verified'] for v in verification):raise AssertionError('Computed basis failed independent substitution')
        _,pivots=matrix.rref()
        return {'status':'exact-within-polynomial-ansatz','degree':degree,'unknowns':len(unknowns),
                'split_matrix_shape':list(matrix.shape),'rank':len(pivots),'nullity':len(basis),
                'basis':[list(map(str,v)) for v in basis],'verified_basis':verification,
                'split_denominators':denominators,'seconds':time.perf_counter()-tic,
                'parameter_scope':'Specified strata only. Symbolic nullspace is generic; recompute exceptional parameter values.',
                'completeness':'Exact kernel on the declared algebraic jet chart within the finite ansatz. Constrained non-involutive systems may require additional compatibility equations; no maximal point-algebra claim.'}


def builtin(name='swe2d'):
    d=1 if name=='swe1d' else 2
    if name=='navier2d':
        return {'name':name,'spatial_dimension':2,'fields':['u','v','p'],'order':2,
                'parameters':{'nu':{'value':'1','assumptions':['positive']}},
                'equations':['u_x+v_y','u_t+u*u_x+v*u_y+p_x-nu*(u_xx+u_yy)',
                             'v_t+u*v_x+v*v_y+p_y-nu*(v_xx+v_yy)'],
                'leaders':['v_y','u_t','v_t'],'roles':['constraint','main','main'],
                'domains':['t>0','nu>0'],'note':'second-order constrained bulk equations; verification is a sufficient algebraic-chart check, not differential-involutive completeness'}
    source='-f*v+gamma*u';sourcev='+f*u+gamma*v'
    config={'name':name,'spatial_dimension':d,'fields':['h','u','v'],'order':1,'positive_fields':['h'],
            'parameters':{'g':{'value':'1','assumptions':['positive']},'f':'0','gamma':'0'},
            'equations':['h_t+u*h_x+h*u_x'+('+v*h_y+h*v_y' if d==2 else ''),
                         'u_t+u*u_x+g*h_x'+('+v*u_y' if d==2 else '')+source,
                         'v_t+u*v_x'+('+v*v_y+g*h_y' if d==2 else '')+sourcev],
            'leaders':['h_t','u_t','v_t'],'roles':['conservation','main','main'],'domains':['t>0','h>0','g>0']}
    if name=='sve2d':
        config['fields'].append('b');config['parameters'].update({'kappa':'0.01','m':'3'})
        config['equations'][1]+='+g*b_x';config['equations'][2]+='+g*b_y'
        config['equations'].append('b_t+kappa*((u**2+v**2)**((m-1)/2)*(u_x+v_y)+(m-1)*(u**2+v**2)**((m-3)/2)*(u**2*u_x+u*v*v_x+u*v*u_y+v**2*v_y))')
        config['leaders'].append('b_t');config['roles'].append('additional sediment conservation')
        config['allow_other_equation_count']=True;config['domains'].append('u**2+v**2>0 for noninteger active flux')
    return config


def named_generators(system):
    x=system.x;t=x[0];fields=system.fields;n=len(x);size=n+len(fields)
    result={}
    for name,components in system.config.get('generators',{}).items():
        if len(components)!=size:raise ValueError('Supplied generator vector has wrong length')
        result[name]=sp.Matrix([safe_expr(q,system.names).subs(system.parameter_values) for q in components])
    for i,z in enumerate(x):
        v=sp.zeros(size,1);v[i]=1;result['T'+str(z)]=v
    D=sp.zeros(size,1);D[:n,0]=sp.Matrix(x);result['D']=D
    if tuple(map(str,fields))[:3] not in [('h','u','v'),('u','v','p')]:return result
    if str(fields[0])=='h':
        h,u,v=fields[:3];V=sp.zeros(size,1)
        for i in range(1,n):V[i]=x[i]
        V[n:n+3,0]=sp.Matrix([2*h,u,v])
        if len(fields)==4:V[n+3]=2*fields[3]
        result['V']=V
        for i,vel in [(1,u)]+([(2,v)] if system.dim==2 else []):
            G=sp.zeros(size,1);G[i]=t;G[n+fields.index(vel)]=1;result['G'+str(x[i])]=G
        if system.dim==2:
            P=sp.Matrix([t*t,t*x[1],t*x[2],-2*t*h,x[1]-t*u,x[2]-t*v]+([0] if len(fields)==4 else []));result['P']=P
            result['J']=sp.Matrix([0,-x[2],x[1],0,-v,u]+([0] if len(fields)==4 else []))
    else:
        u,v,p=fields
        result['Gx']=sp.Matrix([0,t,0,1,0,0]);result['Gy']=sp.Matrix([0,0,t,0,1,0])
        result['J']=sp.Matrix([0,-x[2],x[1],-v,u,0]);result['pressure_shift']=sp.Matrix([0,0,0,0,0,1])
    return result


def bracket(a,b,base):
    return sp.simplify(b.jacobian(base)*a-a.jacobian(base)*b)


def algebra_table(vectors,base):
    table={}
    for i,a in enumerate(vectors):
        for j in range(i+1,len(vectors)):
            b=bracket(a,vectors[j],base)
            if any(b):table[f'{i},{j}']=list(map(str,b))
    return table


def affine_flow(vector,base):
    matrix=vector.jacobian(base);offset=sp.simplify(vector-matrix*sp.Matrix(base))
    if any(z in matrix.free_symbols|offset.free_symbols for z in base):
        return {'status':'nonaffine-flow-not-integrated','characteristic_system':list(map(str,vector))}
    augmented=matrix.row_join(offset).col_join(sp.zeros(1,len(base)+1))
    return {'status':'exact-matrix-exponential','base':list(map(str,base)),
            'augmented_matrix':[[str(a) for a in row] for row in augmented.tolist()],
            'flow':'(z(epsilon),1)=exp(epsilon*A)*(z(0),1)',
            'domain_note':'local flow only; t>0 and all chart/data restrictions must remain valid'}


def expansion_reduction(system):
    function_start=time.perf_counter()
    if tuple(map(str,system.fields))!=('h','u','v') or system.order!=1:
        return {'status':'unsupported','reason':'Expansion chart is supplied for the three-field flat SWE only.'}
    if any(k not in system.names for k in ['f','gamma']):
        return {'status':'unsupported','reason':'The supplied SWE chart requires explicitly declared f and gamma parameters; use reduction none for a general model.'}
    if any(sp.simplify(system.names[k].subs(system.parameter_values))!=0 for k in ['f','gamma']):
        return {'status':'unsupported','reason':'Source terms break the supplied boost-based chart.'}
    t=system.x[0];a,H0,U0,V0=sp.symbols('a H0 U0 V0',real=True)
    rho=1+a*t;n=len(system.x);generators=named_generators(system)
    selected=[generators['Tx']+a*generators['Gx']]
    if system.dim==2:selected.append(generators['Ty']+a*generators['Gy'])
    verification=[system.verify(v) for v in selected]
    if not all(v['verified'] for v in verification):return {'status':'unsupported','verification':verification}
    h,u,v=system.fields
    invariants=[t,h,u-a*system.x[1]/rho,v-a*system.x[2]/rho if system.dim==2 else v]
    for inv in invariants:
        assert all(sp.simplify(sum(sp.diff(inv,z)*c for z,c in zip((*system.x,*system.fields),X)))==0 for X in selected)
    H,U,V=[sp.Function(k)(t) for k in ('H','U','V')]
    ansatz={h:H,u:a*system.x[1]/rho+U,v:a*system.x[2]/rho+V if system.dim==2 else V}
    chart_seconds=time.perf_counter()-function_start;reduction_start=time.perf_counter();actual={}
    for (field,index),symbol in system.jets.items():
        expression=ansatz[field]
        for z,k in zip(system.x,index):expression=sp.diff(expression,z,k)
        actual[symbol]=expression
    reduced=[sp.simplify(e.subs(actual,simultaneous=True)) for e in system.equations]
    reduction_seconds=time.perf_counter()-reduction_start;reconstruct_start=time.perf_counter()
    solution={H:H0/rho**system.dim,U:U0/rho,V:V0/rho if system.dim==2 else V0}
    profile_defects=[sp.simplify(e.subs(solution).doit()) for e in reduced]
    if any(e!=0 for e in profile_defects):
        return {'status':'reduced-profile-not-supplied','reduced_equations':list(map(str,reduced)),
                'projected_rank':system.dim,'independent_invariant':'t',
                'dependent_invariants':list(map(str,invariants[1:])),
                'reason':'The verified chart reduces this custom model, but the supplied SWE profile does not solve its reduced equations.',
                'trial_profile_defects':list(map(str,profile_defects)),'solution_status':'pending'}
    lifted={h:solution[H],u:ansatz[u].subs(solution),v:ansatz[v].subs(solution)}
    for (field,index),symbol in system.jets.items():
        e=lifted[field]
        for z,k in zip(system.x,index):e=sp.diff(e,z,k)
        actual[symbol]=e
    residuals=[sp.simplify(e.subs(actual,simultaneous=True)) for e in system.equations]
    assert all(r==0 for r in residuals)
    z=a*t;P2=H0*sum((-1)**k*sp.binomial(system.dim+k-1,k)*z**k for k in range(3))
    depth_series_error=sp.factor(lifted[h]-P2)
    # A concrete function-iteration certificate for the reduced linear ODE.
    # On C([0,T]) with sup norm, the Volterra map has Lipschitz bound
    # kappa=d*log(1+a*T) for a>=0. This does not transfer to the full PDE.
    a_control,T_control=.5,.25;L=math.log(1+a_control*T_control);kappa=system.dim*L
    picard=[]
    for k in range(7):
        approximation=sum((-system.dim*L)**n/math.factorial(n) for n in range(k+1))
        picard.append({'iteration':k,'depth_error_at_T':abs(approximation-math.exp(-system.dim*L)),
                       'sup_norm_error_bound_H0_1':kappa**(k+1)/(1-kappa)})
    assert kappa<1 and all(r['depth_error_at_T']<=r['sup_norm_error_bound_H0_1'] for r in picard)
    return {'status':'verified-reduced-and-reconstructed','selected_generators':[list(map(str,X)) for X in selected],
            'commuting':all(not any(bracket(A,B,(*system.x,*system.fields))) for A,B in itertools.combinations(selected,2)),
            'projected_rank':system.dim,'required_rank_for_ODE':len(system.x)-1,
            'independent_invariant':'t','dependent_invariants':list(map(str,invariants[1:])),
            'orbit_coordinates':[str(z/rho) for z in system.x[1:]],'chart_determinant':str(rho**(-system.dim)),
            'reduced_equations':list(map(str,reduced)),'solution':{str(k):str(e) for k,e in lifted.items()},
            'original_residuals':list(map(str,residuals)),
            'data':'at t=0: h=H0, u=a*x+U0, v=a*y+V0 (2D) or V0 (1D)',
            'data_compatibility':'both boost/translation combinations preserve this supplied data',
            'domain':'t>0, a>=0, H0>0, g>0; nonperiodic full-plane/local chart',
            'periodic_square_compatible':False,
            'series_control':{'P2_depth':str(P2),'exact_depth_error':str(depth_series_error),'series_domain':'|a*t|<1'},
            'picard_certificate':{'function_space':'C([0,T];R^3), sup norm for reduced profiles only',
                 'map':'Y_next(t)=Y0+integral_0^t diag(-d*a/rho,-a/rho,-a/rho)*Y(s) ds (2D); last entry zero in 1D',
                 'contraction_bound':'kappa=d*log(1+a*T)<1, a>=0',
                 'control_a':a_control,'control_T':T_control,'control_kappa':kappa,'iterations':picard,
                 'scope':'sufficient local contraction certificate for this explicitly reduced linear system; not general SWE or KAN convergence'},
            'internal_timings':{'chart_seconds':chart_seconds,'reduction_seconds':reduction_seconds,
                                'solution_reconstruction_seconds':time.perf_counter()-reconstruct_start}}


def translation_reduction(system):
    generator=named_generators(system)['Tx'];check=system.verify(generator)
    if not check['verified']:return {'status':'unsupported','reason':'x translation is not a verified PDE symmetry'}
    reduced=[sp.simplify(e.subs({jet:0 for (field,index),jet in system.jets.items() if index[1]>0})) for e in system.equations]
    return {'status':'exact-reduction-conditional-on-data','independent_invariants':list(map(str,(system.x[0],*system.x[2:]))),
            'invariant_fields':'all fields independent of x','equations':list(map(str,reduced)),
            'projected_rank':1,'result_dimension':'1+1' if system.dim==2 else 'ODE',
            'data_certificate':'not supplied; requires initial/boundary data independent of x',
            'solution_status':'not solved; reduced PDE/ODE is returned without a fabricated profile'}


def analyze(config,degree=1,search=True,reduction='expansion'):
    start=time.perf_counter();timings={};tic=time.perf_counter();system=System(config)
    timings['1_model_and_chart']=time.perf_counter()-tic
    tic=time.perf_counter();named=named_generators(system)
    candidate_checks={k:{'vector':list(map(str,v)),**system.verify(v)} for k,v in named.items()}
    timings['2_prolong_and_determine']=time.perf_counter()-tic
    classification=system.classify(degree) if search else {'status':'candidate-verification-only','basis':[]}
    timings['3_exact_split_and_solve']=classification.get('seconds',0.)
    tic=time.perf_counter();basis=[sp.Matrix([safe_expr(a,system.names) for a in row]) for row in classification['basis']]
    algebra=algebra_table(basis,(*system.x,*system.fields)) if basis else {}
    timings['4_verify_and_bracket']=time.perf_counter()-tic
    tic=time.perf_counter();flows={name:affine_flow(v,(*system.x,*system.fields)) for name,v in named.items() if candidate_checks[name]['verified']}
    basis_flows={str(i):affine_flow(v,(*system.x,*system.fields)) for i,v in enumerate(basis)}
    timings['5_flows_invariants_admissibility']=time.perf_counter()-tic
    tic=time.perf_counter()
    reduced=expansion_reduction(system) if reduction=='expansion' else translation_reduction(system) if reduction=='translation-x' else {'status':'not-requested'}
    timings['6_reduce']=time.perf_counter()-tic
    verification_status=reduced.get('status')=='verified-reduced-and-reconstructed'
    if 'internal_timings' in reduced:
        durations=reduced['internal_timings']
        timings['5_flows_invariants_admissibility']+=durations['chart_seconds']
        timings['6_reduce']=durations['reduction_seconds']
        timings['7_reconstruct_and_check']=durations['solution_reconstruction_seconds']
    else:timings['7_reconstruct_and_check']=0.
    return {'schema':'lie-seven-step-v1','model':config,'independent_variables':list(map(str,system.x)),
            'step_1':{'jet_dimension':len(system.jets)+len(system.x),'order':system.order,
                      'differential_consequences_added':len(system.chart_equations)-len(system.equations),
                      'leading_chart':{str(k):str(v) for k,v in system.rules.items()},
                      'leading_determinant':str(system.leader_determinant),
                      'regular_chart_condition':str(system.leader_determinant)+' != 0',
                      'singular_strata_analyzed':not bool(system.leader_determinant.free_symbols),
                      'domain_restrictions':config.get('domains',[])},
            'step_2':{'candidate_checks':candidate_checks},'step_3':classification,
            'step_4':{'nonzero_brackets_of_classified_basis':algebra,'basis_indices':'zero-based'},
            'step_5':{'one_parameter_flows':flows,'classified_basis_flows':basis_flows,
                 'admissibility':'PDE symmetry, initial data, boundary data, and global domain are separate tests'},
            'step_6':reduced,'step_7':{'exact_reconstruction_passed':verification_status,
                 'scope':'verified supplied chart/data only' if verification_status else 'a solved compatible reduced problem is not supplied'},
            'timings':timings,'total_seconds':time.perf_counter()-start,'ml_imports':False,
            'limitations':['finite polynomial ansatz is not maximal classification','nonpolynomial split is explicitly unsupported',
                           'arbitrary constrained higher-order systems require differential-involutive completion for completeness',
                           'no fractional spatial dimensions, shocks, or dry-bed charts']}


def self_test():
    checks={}
    for name in ['swe1d','swe2d']:
        result=analyze(builtin(name));assert result['step_7']['exact_reconstruction_passed']
        assert result['step_3']['nullity']>0
        if name=='swe2d':assert result['step_2']['candidate_checks']['P']['verified']
        checks[name]={'nullity':result['step_3']['nullity'],'seconds':result['total_seconds'],'reconstruction':True}
    cubic=analyze(builtin('sve2d'),search=False,reduction='none')
    assert cubic['step_2']['candidate_checks']['V']['verified']
    near=builtin('sve2d');near['parameters']['m']='3.1'
    near=analyze(near,search=False,reduction='none');assert not near['step_2']['candidate_checks']['V']['verified']
    source=builtin();source['parameters'].update({'f':'.2','gamma':'.05'})
    source=analyze(source,search=False);assert not source['step_2']['candidate_checks']['D']['verified']
    assert source['step_6']['status']=='unsupported'
    malformed=builtin();malformed['spatial_dimension']=1.5
    try:System(malformed);raise AssertionError('Fractional dimension accepted')
    except ValueError:pass
    try:safe_expr("__import__('os').system('id')",{});raise AssertionError('Unsafe expression accepted')
    except ValueError:pass
    assert analyze(builtin(),search=False,reduction='translation-x')['step_6']['result_dimension']=='1+1'
    checks.update({'near_cubic_V_rejected':True,'source_breaks_D_and_expansion':True,
                   'fractional_dimension_rejected':True,'unsafe_expression_rejected':True,'2D_translation_reduces_to_1plus1':True})
    third={'name':'third-order linear transport control','spatial_dimension':1,
           'fields':['h','u','v'],'order':3,'equations':['h_t+h_xxx','u_t+u_xxx','v_t+v_xxx'],
           'leaders':['h_t','u_t','v_t'],'roles':['conservation','main','main']}
    third=analyze(third,search=False,reduction='none')
    assert third['step_2']['candidate_checks']['Tx']['verified']
    assert third['step_2']['candidate_checks']['Tt']['verified']
    checks['third_order_translation_candidates_verified']=True
    missing=builtin();missing['parameters'].pop('f');missing['parameters'].pop('gamma')
    missing['equations']=[e.replace('-f*v+gamma*u','').replace('+f*u+gamma*v','') for e in missing['equations']]
    assert analyze(missing,search=False)['step_6']['status']=='unsupported'
    checks['missing_named_chart_parameters_reported_unsupported']=True
    custom=builtin();custom['equations']=['h_t+u*h_x+v*h_y','u_t+u*u_x+v*u_y','v_t+u*v_x+v*v_y']
    assert analyze(custom,search=False)['step_6']['status']=='reduced-profile-not-supplied'
    checks['custom_reduced_system_does_not_inherit_wrong_SWE_profile']=True
    nonautonomous=builtin();nonautonomous['parameters']['f']='0.1*t'
    assert not analyze(nonautonomous,search=False,reduction='none')['step_2']['candidate_checks']['Tt']['verified']
    checks['time_dependent_coefficient_breaks_time_translation']=True
    navier=analyze(builtin('navier2d'),search=False,reduction='none')
    assert navier['step_1']['differential_consequences_added']==3
    assert navier['step_2']['candidate_checks']['Gx']['verified']
    checks['mixed_order_constraint_prolongation_verified']=True
    return {'status':'passed','checks':checks}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--builtin',choices=['swe1d','swe2d','sve2d','navier2d'],default='swe2d')
    p.add_argument('--input',help='JSON PDE specification; overrides builtin')
    p.add_argument('--parameter',action='append',default=[],help='name=exact-value; repeat for explicit parameter strata')
    p.add_argument('--degree',type=int,choices=[0,1,2],default=1)
    p.add_argument('--verify-only',action='store_true')
    p.add_argument('--reduction',choices=['expansion','translation-x','none'],default='expansion')
    p.add_argument('--self-test',action='store_true')
    p.add_argument('--write-example',help='write builtin as editable JSON and exit')
    p.add_argument('--out',default='results/lie_analysis.json');args=p.parse_args()
    config=json.loads(Path(args.input).read_text()) if args.input else builtin(args.builtin)
    for item in args.parameter:
        name,value=item.split('=',1)
        if name not in config.get('parameters',{}):p.error('Unknown parameter '+name)
        original=config['parameters'][name]
        config['parameters'][name]={**original,'value':value} if isinstance(original,dict) else value
    if args.write_example:
        target=Path(args.write_example);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(config,indent=2));return
    result=self_test() if args.self_test else analyze(config,args.degree,not args.verify_only,args.reduction)
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2))
    print(json.dumps({'output':str(out),'status':result.get('status',result.get('step_3',{}).get('status')),
                      'seconds':result.get('total_seconds'),'tests':result.get('checks')},indent=2))


if __name__=='__main__':main()
