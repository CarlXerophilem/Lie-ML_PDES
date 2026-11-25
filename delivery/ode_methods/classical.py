"""Exact local recurrence and nonlinear Chebyshev collocation."""
import sympy as sp


def taylor(task,degree):
    s,y,dy=task.symbols
    from symbolic_input import Expressions
    numerator=Expressions(('s','y','dy')).read(task.data['residual_numerator']) if 'residual_numerator' in task.data else sp.cancel(task.expression).as_numer_denom()[0]
    poly=sp.Poly(numerator,s,y,dy,extension=sp.sqrt(141));domain=poly.domain
    terms=poly.terms();zero=domain.zero;one=domain.one
    if task.critical and (sp.Rational(task.data['initial'])!=0 or any(k and i<1 for (i,j,k),c in terms)):
        raise ValueError('BB recurrence requires zero remainder trace and a coordinate factor on every derivative term')
    coefficients=[domain.from_sympy(sp.Rational(task.data['initial']))]
    def mul(a,b,n):return [sum((a[j]*b[i-j] for j in range(max(0,i-len(b)+1),min(i+1,len(a)))),zero) for i in range(n+1)]
    def coefficient(values,n):
        yy=values+[zero]*max(0,n+1-len(values));dd=[domain.convert(i)*values[i] for i in range(1,len(values))]
        powers={0:[one]+[zero]*n,1:yy[:n+1]}
        for k in range(2,max(j for (i,j,k),c in terms)+1):powers[k]=mul(powers[k-1],yy,n)
        result=zero
        for (i,j,k),c in terms:
            if i>n:continue
            if k>1:raise ValueError('recurrence currently requires first-degree highest derivative')
            product=mul(powers[j],dd,n) if k else powers[j]
            result+=domain.from_sympy(c)*product[n-i]
        return result
    divisors=[]
    for j in range(1,degree+1):
        n=j if task.critical else j-1
        r0=coefficient(coefficients+[zero],n);r1=coefficient(coefficients+[one],n)
        divisor=r1-r0
        if not divisor:raise ArithmeticError('resonance or singular recurrence coefficient')
        if coefficient(coefficients+[domain.convert(2)],n)!=r0+2*divisor:raise ArithmeticError('coefficient equation is nonlinear')
        value=-r0/divisor;coefficients.append(value);divisors.append(str(domain.to_sympy(divisor)))
        if coefficient(coefficients,n)!=zero:raise ArithmeticError('recurrence substitution failed')
    return {'representation':'polynomial','coefficients':[str(domain.to_sympy(v)) for v in coefficients],
            'status':'exact_truncation','degree':degree,'recurrence_divisors':divisors,'termination':'requested_degree'}


def chebyshev(task,degree,tol=1e-12,maxiter=30):
    import numpy as np
    lo,hi=task.interval;n=degree
    nodes=(lo+hi)/2+(hi-lo)*np.cos(np.pi*np.arange(n+1)/n)/2
    trace=int(np.argmin(abs(nodes)))
    if abs(nodes[trace])>8*np.finfo(float).eps*max(abs(lo),abs(hi),1):
        raise ValueError('trace must be a Lobatto node; use even degree on the symmetric BB interval')
    nodes[trace]=0
    weights=(-1.)**np.arange(n+1);weights[[0,-1]]*=.5
    delta=nodes[:,None]-nodes[None,:];np.fill_diagonal(delta,1)
    D=(weights[None,:]/weights[:,None])/delta;np.fill_diagonal(D,0);np.fill_diagonal(D,-D.sum(axis=1))
    R,Ry,Rd=task.numpy_functions();y=np.full(n+1,task.trace);status='iteration_budget'
    def residual(v):
        value=np.asarray(R(nodes,v,D@v),dtype=float)+np.zeros(n+1);value[trace]=v[trace]-task.trace;return value
    for iteration in range(maxiter):
        rr=residual(y);norm=float(np.max(abs(rr)))
        if norm<tol:status='residual_tolerance';break
        a=np.asarray(Ry(nodes,y,D@y))+np.zeros(n+1);b=np.asarray(Rd(nodes,y,D@y))+np.zeros(n+1)
        jac=np.diag(a)+b[:,None]*D;jac[trace]=0;jac[trace,trace]=1
        try:step=np.linalg.solve(jac,-rr)
        except np.linalg.LinAlgError:status='singular_jacobian';break
        factor=1.
        for _ in range(20):
            candidate=y+factor*step
            if np.all(np.isfinite(candidate)) and np.max(abs(residual(candidate)))<norm:
                y=candidate;break
            factor/=2
        else:status='line_search_failed';break
    coeff=np.polynomial.Chebyshev.fit(nodes,y,n,domain=[lo,hi]).convert(kind=np.polynomial.Polynomial).coef
    return {'representation':'polynomial','coefficients':[repr(float(v)) for v in coeff],
            'status':status,'degree':degree,'iterations':iteration+1,'collocation_residual_max':float(np.max(abs(residual(y)))),
            'termination':'nonlinear Newton with residual test and backtracking','nodes':nodes.tolist()}


def analytic(task):
    s,y,dy=task.symbols
    initial=sp.Rational(task.data['initial'])
    if sp.cancel(task.expression.subs({y:initial,dy:0},simultaneous=True))==0:
        return {'representation':'analytic','expression':str(initial),'status':'symbolic_solution',
                'termination':'constant equilibrium; no ML call'}
    rhs=sp.solve(task.expression,dy)
    if len(rhs)!=1:return {'status':'unsupported','reason':'no unique explicit scalar RHS'}
    if rhs[0].has(s):
        function=sp.Function('Y')(s)
        equation=sp.Eq(sp.diff(function,s),rhs[0].subs(y,function))
        solution=sp.dsolve(equation,ics={function.subs(s,0):sp.Rational(task.data['initial'])})
        if isinstance(solution,list):return {'status':'unsupported','reason':'multiple symbolic solution branches require explicit selection'}
        if solution.lhs!=function or solution.rhs.has(function):
            return {'representation':'implicit','expression':str((solution.lhs-solution.rhs).subs(function,y)),
                    'status':'symbolic_solution','termination':'SymPy dsolve; implicit branch requires verifier check'}
        return {'representation':'analytic','expression':str(solution.rhs),'status':'symbolic_solution',
                'termination':'SymPy dsolve; no ML call'}
    primitive=sp.integrate(1/rhs[0],y)
    if primitive.has(sp.Integral):return {'status':'unsupported','reason':'symbolic primitive not found'}
    relation=sp.simplify(primitive-primitive.subs(y,sp.Rational(task.data['initial']))-s)
    return {'representation':'implicit','expression':str(relation),'status':'symbolic_quadrature',
            'conditions':['dG/dy != 0','declared positive solution branch'],'termination':'exact antiderivative'}
