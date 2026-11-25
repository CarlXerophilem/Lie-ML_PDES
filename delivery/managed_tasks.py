"""Symbolic task export from checked reductions; no optimization or reference values."""
import hashlib
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parent


def export_tasks():
    from lie_pde_reducer import reduction
    from lie_reduce.benchmarks import export
    from lie_reduce.critical import certify
    from lie_reduce.identities import require_zero
    provenance=[reduction('E1',2,'bed_drift'),reduction('M',2,'tilted'),reduction('E2',3)]
    if any(v['verification']['status']!='verified_local_identities' for v in provenance):
        raise ArithmeticError('independent PDE verification failed')
    derived=export();certificate=certify();s,y,dy=sp.symbols('s y dy',real=True)
    tasks=[]
    for name,X,initial,expr in (
        ('N1',sp.Rational(4,5),sp.S.One,2*y*dy/sp.Rational(4,5)+1),
        ('N2',sp.Rational(1,64),sp.Rational(1,2),(10-y*y-12*y**3)*dy/sp.Rational(1,64)-20*y**3)):
        # Compare the exported first-order equation, up to its documented denominator.
        raw=derived[name]['residual'];function=next(iter(raw.atoms(sp.core.function.AppliedUndef)))
        z=function.args[0];raw=raw.subs({sp.diff(function,z):dy/X,function:y},simultaneous=True)
        require_zero(raw-expr if name=='N1' else raw-expr/(20*y**3),'task equation vs verified first integral')
        tasks.append({'id':name,'operator':'regular','residual':str(expr),'initial':str(initial),'interval':['0','1'],
                      'physical_scale':str(X),'scope':'N2 uses the local interface interval, not a fold-distance experiment' if name=='N2' else 'positive bed-drift profile',
                      'source_model':'E1' if name=='N1' else 'M','source_anchor':'eq:tilted' if name=='N2' else 'tab:reductions'})
    X=certificate['shared_halfwidth']
    for branch in certificate['branches']:
        rho,w=sp.symbols('rho w',real=True);b=branch['b']
        pn,pd=sp.fraction(branch['Psi'])
        A=sp.Poly(pn.subs({rho:X*s,w:X*y},simultaneous=True),s,y,dy,extension=sp.sqrt(141))
        B=sp.Poly(pd.subs({rho:X*s,w:X*y},simultaneous=True),s,y,dy,extension=sp.sqrt(141))
        numerator=(sp.Poly(X*(s*dy+b*y),s,y,dy,extension=sp.sqrt(141))*B-A).as_expr()
        denominator=(B*X).as_expr()
        expr=numerator/denominator
        tasks.append({'id':'N3plus' if sp.expand(branch['slope']).coeff(sp.sqrt(141))>0 else 'N3minus',
                      'operator':'BB','residual':str(expr),'residual_numerator':str(numerator),'residual_denominator':str(denominator),'initial':'0','interval':['-1','1'],'physical_scale':str(X),
                      'b':str(sp.N(b,17)),'slope':str(branch['slope']),'source_model':'E2','source_anchor':'eq:planar',
                      'scope':'scaled saddle remainder q; H=1+ell*X*s+X**2*s*q; no division by D at the critical point',
                      'certificate_radius':str(branch['disk']['R']),'remainder_radius':str(branch['disk']['R_w'])})
    source=(ROOT.parent/'draft'/'dissertation_wku_compact.tex').read_text()
    for task in tasks:
        anchor=source.index('\\label{'+task['source_anchor']+'}')
        if 'residual_numerator' not in task:
            numerator,denominator=sp.fraction(sp.together(sp.sympify(task['residual'],locals={'s':s,'y':y,'dy':dy})))
            task['residual_numerator']=str(numerator);task['residual_denominator']=str(denominator)
        task['paper_contract']={'residual_numerator':task['residual_numerator'],'residual_denominator':task['residual_denominator'],'schema':'paper-ode-v1','symbols':['s','y','dy'],'functions':[],
            'coordinate':'s','value_symbol':'y','derivative_symbol':'dy','residual':task['residual'],
            'trace_coordinate':'0','trace_value':task['initial'],'source_anchor':task['source_anchor'],
            'source_excerpt':source[max(0,anchor-80):anchor+650],
            'scope':'derived ODE contract after separate independent PDE pullback; not a direct LaTeX parser'}
        task['pde_verification_sha256']=hashlib.sha256(json.dumps(provenance,sort_keys=True).encode()).hexdigest()
    return {'schema':'verified-ode-tasks-v1','tasks':tasks,'PDE_provenance':provenance,'ML':False}
