"""Independent checker. Imports only the standard library and SymPy.

No PDE reduction, reference-generation, optimization or ODE-solver modules may
be imported here. Input equations are separate, reviewed paper transcriptions.
"""
import hashlib
import json
import sympy as sp


from symbolic_input import Expressions

def _zero(expression):
    # Simplification is limited to local symbolic identities; branches are listed
    # separately. Failure to simplify is UNKNOWN, never a nonzero theorem.
    normalized=sp.cancel(sp.simplify(expression))
    if normalized==0:return {'status':'proved_zero','normal_form':'0'}
    return {'status':'not_proved','residual':str(normalized)}


def _check_reduction(output,paper):
    if output.get('model')!=paper.get('model'):raise ValueError('model identity differs from paper contract')
    symbols=set(paper['independent']+paper['dependent']+paper['parameters']+output.get('symbols',[])+['z','orbit'])
    functions=set(paper['dependent']+output['profile_functions'])
    reader=Expressions(symbols,functions,paper.get('positive_parameters',[]));read=reader.read
    base=tuple(read(n) for n in paper['independent']);z=read('z')
    fields=tuple(reader.functions[n](*base) for n in paper['dependent'])
    bindings={read(k):read(v) for k,v in output.get('parameter_bindings',{}).items()}
    originals=tuple(read(e).doit().subs(bindings,simultaneous=True) for e in paper['equations'])
    lifts=tuple(read(e) for e in output['lifts'])
    if len(lifts)!=len(fields):raise ValueError('lift has wrong number of components')
    substitution=dict(zip(fields,lifts));point_sub=dict(zip((read(n) for n in paper['dependent']),lifts))
    invariant=read(output['invariant']);equations=tuple(read(e) for e in output['equations'])
    orbit={read(k):read(v) for k,v in output.get('orbit_coordinates',{}).items()}
    if len(equations)!=len(originals):raise ValueError('one residual per original balance is required')
    checks=[];base_fields=[]
    for generator in output['generators']:
        X=tuple(read(v) for v in generator)
        if len(X)!=len(base)+len(fields):raise ValueError('generator dimension mismatch')
        if any(v.has(*(read(n) for n in paper['dependent'])) for v in X[:len(base)]):raise ValueError('nonprojectable generator in declared graph chart')
        base_fields.append(X[:len(base)])
        for eta,lift in zip(X[len(base):],lifts):
            checks.append(_zero(eta.subs(point_sub,simultaneous=True)-sum(
                xi.subs(point_sub,simultaneous=True)*sp.diff(lift,x) for xi,x in zip(X,base))))
        checks.append(_zero(sum(xi*sp.diff(invariant,x) for xi,x in zip(X,base))))
    base_rank=sp.Matrix(base_fields).rank()
    if base_rank!=len(base)-1:raise ValueError('base orbit rank does not give an ODE quotient')
    if all(sp.diff(invariant,x)==0 for x in base):raise ValueError('constant quotient coordinate is not an invariant coordinate chart')
    weights=tuple(read(v) for v in output.get('weights',['1']*len(originals)))
    if len(weights)!=len(originals):raise ValueError('weight count differs from balance count')
    weight_checks=[]
    for original,equation,weight in zip(originals,equations,weights):
        pull=original.subs(substitution,simultaneous=True).doit()
        if orbit:
            pull=sp.simplify(pull.subs(orbit,simultaneous=True).doit());lifted=equation
        else:lifted=equation.subs(z,invariant).doit()
        checks.append(_zero(pull-weight*lifted))
        if weight.is_zero is True:raise ValueError('zero pullback weight destroys reverse implication')
        weight_checks.append({'weight':str(weight),'nonzero':weight.is_zero is False or weight.func==sp.exp})
    ok=all(v['status']=='proved_zero' for v in checks)
    return {'status':'verified_local_identities' if ok else 'not_verified','checks':checks,'weights':weight_checks,'generic_base_orbit_rank':base_rank,
            'equivalence':'conditional on original denominators, chart, section rank and nonzero weights',
            'scope':'independent PDE-to-graph substitution and invariant-surface identities; not a classification-completeness proof'}


def _check_candidate(output,paper):
    reader=Expressions(paper['symbols'],paper.get('functions',[]),paper.get('positive_parameters',[]));read=reader.read
    s=read(paper['coordinate']);y=read(paper['value_symbol']);dy=read(paper['derivative_symbol'])
    residual=read(paper['residual'])
    if 'residual_numerator' in paper:
        numerator=read(paper['residual_numerator']);denominator=read(paper['residual_denominator'])
        if denominator==0:raise ValueError('zero residual denominator')
        quotient=numerator/denominator
        if residual!=quotient and _zero(residual-quotient)['status']!='proved_zero':
            raise ValueError('residual numerator/denominator disagree with the equation')
    if output['representation']=='polynomial':
        coeffs=[read(v) for v in output['coefficients']]
        candidate=sum(c*s**i for i,c in enumerate(coeffs));derivative=sp.diff(candidate,s)
        trace=_zero(candidate.subs(s,read(paper['trace_coordinate']))-read(paper['trace_value']))
        if 'residual_numerator' in paper:
            polynomial=sp.Poly(read(paper['residual_numerator']),s,y,dy,extension=sp.sqrt(141))
            curve=sp.Poly(candidate,s,extension=sp.sqrt(141));tangent=curve.diff()
            def substitute(poly):
                result=sp.Poly(0,s,extension=sp.sqrt(141))
                for (i,j,k),c in poly.terms():
                    result+=sp.Poly(c*s**i,s,extension=sp.sqrt(141))*curve**j*tangent**k
                return result
            result=substitute(polynomial)
            denominator=substitute(sp.Poly(read(paper['residual_denominator']),s,y,dy,extension=sp.sqrt(141)))
            if denominator.is_zero:return {'status':'inadmissible','reason':'candidate lies identically on the residual denominator zero set'}
            exact=result.is_zero
            defect_record={'numerator_coefficients_descending':list(map(str,result.all_coeffs())),
                           'denominator_definition':paper['residual_denominator'],
                           'domain':'where substituted denominator is nonzero'}
        else:
            defect=sp.cancel(residual.subs({y:candidate,dy:derivative},simultaneous=True))
            exact=_zero(defect)['status']=='proved_zero';defect_record=str(defect)
        return {'status':'exact_solution' if exact and trace['status']=='proved_zero' else 'approximation',
                'symbolic_substitution':True,'symbolic_trace':trace,'symbolic_residual':defect_record,
                'continuous_error_bound':None,'scope':'exact rational/algebraic interpretation of recorded polynomial coefficients'}
    if output['representation']=='analytic':
        candidate=read(output['expression']);derivative=sp.diff(candidate,s)
        defect=residual.subs({y:candidate,dy:derivative},simultaneous=True)
        check=_zero(defect);trace=_zero(candidate.subs(s,read(paper['trace_coordinate']))-read(paper['trace_value']))
        return {'status':'exact_solution' if check['status']=='proved_zero' and trace['status']=='proved_zero' else 'not_verified',
                'symbolic_substitution':check,'symbolic_trace':trace,'conditions':output.get('conditions',[])}
    if output['representation']=='implicit':
        relation=read(output['expression']);slope=-sp.diff(relation,s)/sp.diff(relation,y)
        check=_zero(residual.subs(dy,slope))
        trace=_zero(relation.subs({s:read(paper['trace_coordinate']),y:read(paper['trace_value'])},simultaneous=True))
        leading=sp.diff(relation,y).subs({s:read(paper['trace_coordinate']),y:read(paper['trace_value'])},simultaneous=True)
        if leading.is_zero is not False:return {'status':'not_verified','reason':'implicit function condition at trace is zero or unproved'}
        return {'status':'exact_implicit_solution' if check['status']=='proved_zero' and trace['status']=='proved_zero' else 'not_verified',
                'symbolic_substitution':check,'symbolic_trace':trace,'nonvanishing_required':str(sp.diff(relation,y)),
                'conditions':output.get('conditions',[])}
    if output['representation']=='network':
        points=output.get('verification_points',[]);expected_probes=output.get('autograd_probes',[])
        if not points or len(points)!=len(expected_probes):
            raise ValueError('one recorded autograd probe per verification coordinate is required')
        for point,probe in zip(points,expected_probes):
            if _zero(read(point)-read(str(probe['coordinate'])))['status']!='proved_zero':
                raise ValueError('autograd probe coordinates differ from verification coordinates')
        # Independent symbolic layer-derivative templates, not torch autograd.
        q,v,dv,a=sp.symbols('q v dv a',real=True)
        templates={'tanh_derivative':sp.diff(sp.tanh(q),q),
                   'residual_block_derivative':sp.diff(q+a*sp.tanh(v),q)+sp.diff(q+a*sp.tanh(v),v)*dv}
        # Weight values are exact decimal rationals. Probe evaluations are high
        # precision diagnostics and are explicitly not a continuous certificate.
        probes=[]
        for point in output.get('verification_points',['0','1/3','1']):
            x=read(point);value=[sp.N(x,40)];derivative=[sp.Integer(1)]
            for layer in output['layers']:
                W=[[sp.Rational(str(v)) for v in row] for row in layer['weight']]
                bias=[sp.Rational(str(v)) for v in layer['bias']]
                if len(bias)!=len(W) or any(len(row)!=len(value) for row in W):raise ValueError('network layer shape mismatch')
                if layer['kind']=='residual' and (len(W)!=len(value) or len(layer['alpha'])!=len(value)):raise ValueError('residual block shape mismatch')
                affine=[sum(w*v for w,v in zip(row,value))+b for row,b in zip(W,bias)]
                tangent=[sum(w*v for w,v in zip(row,derivative)) for row in W]
                if layer['kind']=='linear':value,derivative=affine,tangent
                elif layer['kind']=='tanh':
                    value=[sp.N(sp.tanh(v),40) for v in affine]
                    derivative=[sp.N(templates['tanh_derivative'].subs(q,v)*d,40) for v,d in zip(affine,tangent)]
                elif layer['kind']=='residual':
                    alpha=list(map(lambda v:sp.Rational(str(v)),layer['alpha']))
                    value=[sp.N(old+c*sp.tanh(v),40) for old,c,v in zip(value,alpha,affine)]
                    derivative=[sp.N(old+c*(1-sp.tanh(v)**2)*d,40) for old,c,v,d in zip(derivative,alpha,affine,tangent)]
                else:raise ValueError('unknown layer kind')
            if len(value)!=1:raise ValueError('scalar task requires exactly one output')
            yy,ddy=value[0],derivative[0]
            if output.get('prefix') is not None:
                prefix=sum(read(c)*s**i for i,c in enumerate(output['prefix']));power=len(output['prefix'])
                yy=prefix.subs(s,x)+x**power*value[0]
                ddy=sp.diff(prefix,s).subs(s,x)+power*x**(power-1)*value[0]+x**power*derivative[0]
            probes.append({'coordinate':str(x),'value':str(sp.N(yy,25)),'derivative':str(sp.N(ddy,25)),
                           'residual':str(sp.N(residual.subs({s:x,y:yy,dy:ddy},simultaneous=True),25))})
        agreement=[]
        for expected,observed in zip(output.get('autograd_probes',[]),probes):
            differences={key:abs(sp.N(sp.Rational(str(expected[key]))-sp.sympify(observed[key]),30)) for key in ('value','derivative')}
            agreement.append({'coordinate':observed['coordinate'],'absolute_differences':{k:str(v) for k,v in differences.items()},
                              'passed':all(v<sp.Rational(1,10**10) for v in differences.values())})
        status='derivative_mismatch' if any(not v['passed'] for v in agreement) else 'approximation'
        return {'status':status,'autograd_crosscheck':agreement,'symbolic_chain_rule_templates':{k:str(v) for k,v in templates.items()},
                'independent_probes':probes,'continuous_error_bound':None,
                'scope':'symbolic differentiation of layer maps followed by high-precision probes; no exact-solution assertion'}
    raise ValueError('unknown candidate representation')


def _verify(solver_output,paper_txt_respective):
    """Two-input isolated boundary. Paper text must be a reviewed equation contract."""
    try:
        paper=json.loads(paper_txt_respective) if isinstance(paper_txt_respective,str) else paper_txt_respective
        if paper.get('schema') not in ('paper-pde-v1','paper-ode-v1'):raise ValueError('reviewed equation contract required; arbitrary prose is not machine-verifiable')
        if not paper.get('source_excerpt') or not paper.get('source_anchor'):raise ValueError('paper anchor and excerpt required')
        if paper['schema']=='paper-pde-v1':
            result=_check_generators(solver_output,paper) if solver_output.get('kind')=='point_generators' else _check_reduction(solver_output,paper)
        else:result=_check_candidate(solver_output,paper)
        result.update(verifier='independent_verifier.v1',paper_sha256=hashlib.sha256(json.dumps(paper,sort_keys=True).encode()).hexdigest(),
                      paper_transcription='explicit input; semantic agreement of transcription with prose is not inferred')
        return result
    except Exception as exc:
        return {'status':'verification_timeout' if isinstance(exc,TimeoutError) else 'verification_error','reason':f'{type(exc).__name__}: {exc}'}


def verifier(solver_output,paper_txt_respective):
    import signal
    import time
    def expired(*_):raise TimeoutError('independent verification exceeded 30 seconds')
    previous=signal.getsignal(signal.SIGALRM);old_timer=signal.getitimer(signal.ITIMER_REAL)
    start=time.monotonic();signal.signal(signal.SIGALRM,expired)
    signal.setitimer(signal.ITIMER_REAL,min(30,old_timer[0]) if old_timer[0]>0 else 30)
    try:return _verify(solver_output,paper_txt_respective)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)
        if old_timer[0]>0:signal.setitimer(signal.ITIMER_REAL,max(.001,old_timer[0]-(time.monotonic()-start)),old_timer[1])


def _check_generators(output,paper):
    """Characteristic prolongation, independent of the reducer's recursive eta_J."""
    from itertools import product
    if output.get('model')!=paper.get('model'):raise ValueError('model identity differs from paper contract')
    if not output.get('generators'):raise ValueError('no generators supplied for verification')
    reader=Expressions(paper['independent']+paper['dependent']+paper['parameters'],paper['dependent'],paper.get('positive_parameters',[]))
    read=reader.read;base=tuple(read(v) for v in paper['independent']);n=len(base)
    fields=[reader.functions[v](*base) for v in paper['dependent']]
    bindings={read(k):read(v) for k,v in output.get('parameter_bindings',{}).items()}
    originals=[read(e).doit().subs(bindings,simultaneous=True) for e in paper['equations']]
    order=max(d.derivative_count for eq in originals for d in eq.atoms(sp.Derivative))
    indices=sorted((j for j in product(range(order+2),repeat=n) if sum(j)<=order+1),key=lambda j:(sum(j),j))
    zero=(0,)*n;jets={};mapping={}
    for a,f in enumerate(fields):
        for j in indices:
            v=read(paper['dependent'][a]) if j==zero else sp.Symbol('j'+str(a)+'_'+''.join(map(str,j)),real=True)
            jets[a,j]=v;mapping[sp.diff(f,*[(x,k) for x,k in zip(base,j) if k]) if any(j) else f]=v
    equations=[e.xreplace(mapping) for e in originals]
    principal=[read(e).doit().xreplace(mapping) for e in paper['principal']]
    solutions=sp.solve(equations,principal,dict=True,simplify=False)
    if len(solutions)!=1:raise ValueError('paper principal chart is not uniquely explicit')
    determinant=sp.factor(sp.Matrix(equations).jacobian(principal).det().subs(solutions[0],simultaneous=True))
    if determinant==0:raise ValueError('paper principal presentation is singular')
    def total(expr,axis):
        result=sp.diff(expr,base[axis])
        for (a,j),v in jets.items():
            derivative=sp.diff(expr,v)
            if derivative==0:continue
            nxt=tuple(k+int(i==axis) for i,k in enumerate(j))
            if (a,nxt) not in jets:raise ValueError('independent checker jet order exceeded')
            result+=derivative*jets[a,nxt]
        return sp.expand(result)
    checks=[]
    for generator in output['generators']:
        X=tuple(read(v).subs(bindings,simultaneous=True) for v in generator)
        if len(X)!=n+len(fields):raise ValueError('generator dimension mismatch')
        characteristic=[X[n+a]-sum(X[i]*jets[a,tuple(int(i==k) for k in range(n))] for i in range(n)) for a in range(len(fields))]
        coefficients={}
        for a,Q in enumerate(characteristic):
            for j in indices:
                if sum(j)>order:continue
                v=Q
                for i,k in enumerate(j):
                    for _ in range(k):v=total(v,i)
                coefficients[a,j]=sp.expand(v+sum(X[i]*jets[a,tuple(k+int(i==l) for l,k in enumerate(j))] for i in range(n)))
        for equation in equations:
            prolonged=sum(X[i]*sp.diff(equation,base[i]) for i in range(n))
            prolonged+=sum(c*sp.diff(equation,jets[key]) for key,c in coefficients.items())
            checks.append(_zero(sp.expand(prolonged).subs(solutions[0],simultaneous=True)))
    return {'status':'verified_generators_on_regular_chart' if all(v['status']=='proved_zero' for v in checks) else 'not_verified',
            'checks':checks,'principal_determinant_required_nonzero':str(determinant),
            'scope':'independent full characteristic prolongation sufficiency; does not prove basis completeness'}
