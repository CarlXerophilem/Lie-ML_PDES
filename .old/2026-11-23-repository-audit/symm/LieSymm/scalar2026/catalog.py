"""Executable invariant graphs of the already classified printed-P algebra.

This is a registry of known representatives, not a new classification engine.
Jet substitution differentiates graphs before dividing by any ODE coefficient.
"""
from functools import lru_cache
import sympy as sp

t, s, z = sp.symbols('t s z', real=True)
F, p, q, h = sp.symbols('F p q h', real=True)
J = (F, p, q, h)
g, kappa, m = sp.symbols('g kappa m', positive=True)
a, b, c, alpha, alpha3 = sp.symbols('a b c alpha alpha3', real=True)
sigma = sp.Symbol('sigma', nonzero=True, real=True)
PHI = sp.Symbol('phi', real=True)


def _row(name, generator, strata, aliases=(), parameters=None):
    return dict(id=name, model='P', generator=generator, algebra_strata=strata,
                aliases=list(aliases), parameter_defaults=parameters or {},
                parameter_domain='g>0, kappa>0, m>=1; real remaining parameters',
                chart='phi_s>0, phi_t>0; additional local chart conditions below')


def representatives():
    """Each old orbit family has a map here, including support/sign strata."""
    rows = [
        _row('paper-3.1', (1, 0, 0), ['generic','m1','m3'], ['3.1','X1']),
        _row('paper-3.2', (0, 1, 0), ['generic','m1','m3'], ['3.2','X2']),
        _row('paper-3.3', (0, 0, 1), ['generic','m1','m3'], ['3.3','X3']),
        _row('paper-3.4', (t,s,PHI), ['generic','m1','m3'], ['3.4','X4']),
        _row('paper-3.5', (t,-2*s,0), ['m3'], ['3.5','X5'], {'m':3}),
        _row('paper-3.6', (1,alpha,0), ['generic','m1','m3'], ['3.6','X1+aX2'], {'alpha':-1}),
        _row('paper-3.7', (1,0,alpha), ['generic','m1','m3'], ['3.7','X1+aX3'], {'alpha':1}),
        _row('paper-3.8', (0,1,alpha), ['generic','m1','m3'], ['3.8','X2+aX3'], {'alpha':1}),
        _row('paper-3.9', (1,alpha,alpha3), ['generic','m1','m3'], ['3.9','X1+aX2+bX3'], {'alpha':-1,'alpha3':1}),
        _row('m1-scale-boost', (t,s,PHI+alpha*t), ['m1'], ['X4+alphaX6'], {'m':1,'alpha':1}),
        _row('m1-boost', (0,0,t), ['m1'], ['X6'], {'m':1}),
        _row('m1-boost-travel', (sigma,a,t), ['m1'], ['X6+sigmaX1+aX2'], {'m':1,'sigma':1,'a':-1}),
        _row('m1-boost-space', (0,sigma,t), ['m1'], ['X6+sigmaX2'], {'m':1,'sigma':1}),
        _row('cubic-mixed', ((a+b)*t,(a-2*b)*s,a*PHI), ['m3'], ['aX4+bX5','Table 3 mixed'], {'m':3,'a':1,'b':sp.Rational(1,4)}),
        _row('cubic-space-scaling', (0,3*s,PHI), ['m3'], ['X4-X5','a+b=0'], {'m':3}),
        _row('cubic-resonant-vertical', (t,-2*s,c), ['m3'], ['X5+cX3'], {'m':3,'c':1}),
        _row('cubic-resonant-time', (c,3*s,PHI), ['m3'], ['X4-X5+cX1'], {'m':3,'c':1}),
        _row('cubic-resonant-space', (sp.Rational(3,2)*t,c,PHI), ['m3'], ['X4+X5/2+cX2'], {'m':3,'c':1}),
    ]
    # The extra cubic translation normalization is a map, not another solution count.
    mappings = {
        'paper-3.6': 'X1+sigma X2: alpha=sigma, sigma=+/-1',
        'paper-3.7': 'X3+sigma X1: alpha=1/sigma, sigma=+/-1',
        'paper-3.8': 'X3+sigma X2: alpha=1/sigma, sigma=+/-1',
        'paper-3.9': 'X3+sigma X1+K X2: alpha=K/sigma, alpha3=1/sigma, K!=0',
    }
    for row in rows:
        row['representative_mapping'] = mappings.get(row['id'], 'as displayed')
    return rows


def parameter_values(name, supplied):
    rows = {r['id']:r for r in representatives()}
    name = name if name in rows else 'paper-'+name
    if name not in rows:
        raise ValueError('Unknown reduction: '+name)
    values = dict(g=sp.Integer(1), kappa=sp.Rational(1,30), m=sp.Integer(3))
    values.update(rows[name]['parameter_defaults'])
    allowed = {'g','kappa','m','alpha','alpha3','a','b','c','sigma'}
    if set(supplied)-allowed:
        raise ValueError('Unknown parameters: '+str(sorted(set(supplied)-allowed)))
    values.update({key:sp.sympify(value) for key,value in supplied.items()})
    values = {key:sp.sympify(value) for key,value in values.items()}
    for key,value in values.items():
        if value.is_real is False or value.has(sp.nan,sp.zoo,sp.oo,-sp.oo):
            raise ValueError(key+' must be finite real')
    for key in ('g','kappa'):
        if values[key].is_positive is False or values[key].is_real is False:
            raise ValueError(key+' must be positive real')
    if (values['m']-1).is_negative is True or values['m'].is_real is False:
        raise ValueError('m must be real and >=1')
    if name.startswith('m1-') and values['m'] != 1:
        raise ValueError('This representative requires m=1')
    if (name.startswith('cubic-') or name=='paper-3.5') and values['m'] != 3:
        raise ValueError('This representative requires m=3')
    if 'sigma' in values and values['sigma'].is_number and values['sigma'] not in (-1,1):
        raise ValueError('sigma must be +1 or -1')
    return name, values


def graph(name, values):
    """Return the invariant graph and an explicit transversal inverse chart."""
    A=values.get('alpha',1); U=values.get('alpha3',1)
    av=values.get('a',-1); bv=values.get('b',0); cv=values.get('c',1); sig=values.get('sigma',1)
    domains=['phi_s>0','phi_t>0']
    if name in ('paper-3.3','m1-boost'):
        return dict(status='no_invariant_graph', graph=None, coordinate=None, guards=domains)
    if name=='paper-3.2':
        return dict(status='undefined_pde',graph=F,coordinate=t,guards=['phi_s=0'])
    if name=='paper-3.1':
        return dict(status='outside_positive_chart',graph=F,coordinate=s,guards=['phi_t=0'])
    if name in ('paper-3.6','paper-3.7','paper-3.9'):
        speed=0 if name=='paper-3.7' else A
        vertical=A if name=='paper-3.7' else (0 if name=='paper-3.6' else U)
        coord=s-speed*t; phi=vertical*t+F; inverse={s:z+speed*t}
        section={t:1,s:z+speed}; multiplier=sp.Integer(1)
    elif name=='paper-3.8':
        coord=t;phi=A*s+F;inverse={t:z};section={s:1,t:z};multiplier=sp.Integer(1)
    elif name=='m1-boost-travel':
        coord=s-av*t/sig;phi=t**2/(2*sig)+F
        inverse={s:z+av*t/sig};section={t:1,s:z+av/sig};multiplier=sp.Integer(1)
    elif name=='m1-boost-space':
        coord=t;phi=t*s/sig+F;inverse={t:z};section={s:1,t:z};multiplier=sp.Integer(1)
        domains+=['t/sigma>0']
    elif name in ('cubic-space-scaling','cubic-resonant-time') or (name=='cubic-mixed' and av+bv==0):
        if name=='cubic-mixed' and av==0:
            raise ValueError('(a,b) cannot both vanish')
        shift=cv if name=='cubic-resonant-time' else 0
        coord=t-shift*sp.log(s)/3;phi=s**sp.Rational(1,3)*F
        inverse={t:z+shift*sp.log(s)/3};section={s:1,t:z};multiplier=s**(-sp.Rational(1,3))
        domains+=['s>0; this fractional-power chart excludes s=0']
    else:
        offset=sp.Integer(0)
        if name in ('paper-3.4','m1-scale-boost'):
            power=sp.Integer(1);weight=sp.Integer(-1);coord=s/t
            if name=='m1-scale-boost':offset=A*t*sp.log(t)
        elif name in ('paper-3.5','cubic-resonant-vertical'):
            power=sp.Integer(0);weight=sp.Integer(2);coord=s*t**2
            if name=='cubic-resonant-vertical':offset=cv*sp.log(t)
        elif name=='cubic-resonant-space':
            power=sp.Rational(2,3);weight=0;coord=s-2*cv*sp.log(t)/3
        elif name=='cubic-mixed':
            power=sp.cancel(av/(av+bv));weight=sp.cancel((2*bv-av)/(av+bv));coord=s*t**weight
            domains+=['a+b!=0; a+b=0 is the separate space-scaling chart']
        else:raise ValueError(name)
        phi=t**power*F+offset
        inverse={s:z+2*cv*sp.log(t)/3} if name=='cubic-resonant-space' else {s:z*t**(-weight)}
        section={t:1,s:z};multiplier=t**(-power-1)
        domains+=['t>0; logarithmic/power chart excludes t=0']
    return dict(status='reduction',graph=phi,coordinate=coord,inverse_chart=inverse,
                section=section,multiplier=multiplier,guards=domains)


def total(expr, variable, coordinate):
    return sp.diff(expr,variable)+sp.diff(coordinate,variable)*sum(sp.diff(expr,J[i])*J[i+1] for i in range(3))


def original_from_jets(jets, values):
    """Expanded original P, with no ODE normal-form substitution."""
    v,Q=jets[1,0],jets[0,1];acc,mix,curv=jets[2,0],jets[1,1],jets[0,2]
    G,K,N=values['g'],values['kappa'],values['m']
    flux = v**(N-1)*(jets[1,2]/Q-mix*curv/Q**2)
    if N != 1:flux += (N-1)*v**(N-2)*mix**2/Q
    return Q*jets[3,0]+mix*acc-G*jets[1,2]/Q**2+2*G*curv*mix/Q**3-G*N*K*flux


def derive_entry(name, values):
    row=next(r for r in representatives() if r['id']==name).copy()
    replacements={g:values['g'],kappa:values['kappa'],m:values['m']}
    replacements.update({v:values[str(v)] for v in (a,b,c,alpha,alpha3,sigma) if str(v) in values})
    row['generator']=tuple(sp.sympify(v).subs(replacements) for v in row['generator'])
    row.update(graph(name,values));row['parameters']=values;row['variables']=(t,s)
    if row['status']!='reduction':
        row.update(residual=None,leading=None,Q=(t if name=='m1-boost' else 1) if row['status']=='no_invariant_graph' else 0)
        return row
    phi,coord=row['graph'],row['coordinate'];jets={(0,0):phi}
    for order in range(1,4):
        for it in range(order+1):
            ix=order-it
            jets[it,ix]=total(jets[it-1,ix],t,coord) if it else total(jets[it,ix-1],s,coord)
    tau,xi,eta=row['generator']
    row['Q']=sp.simplify(eta.subs(PHI,phi)-tau*jets[1,0]-xi*jets[0,1])
    row['jets']=jets
    sliced={ij:sp.simplify(v.subs(row['section'],simultaneous=True)) for ij,v in jets.items()}
    if sliced[0,1]==0:
        row.update(status='undefined_pde',residual=None,leading=None)
        return row
    residual=sp.factor(original_from_jets(sliced,values))
    order=next((i for i in (3,2,1,0) if residual.has(J[i])),0)
    row.update(residual=residual,leading=sp.factor(sp.diff(residual,J[order])) if order else sp.Integer(0),
               third_order_coefficient=sp.factor(sp.diff(residual,h)),
               velocity=sliced[1,0],gradient=sliced[0,1],profile_jets=J,
               ode_order=order,
               derivation=['PDE P','invariant graph from Q=0','all jets by total differentiation',
                           'original P on an explicit transversal','undivided reduced residual'])
    return row


@lru_cache(maxsize=1)
def _catalog():
    rows=[]
    for meta in representatives():
        values=dict(g=g,kappa=kappa,m=m)
        for key in meta['parameter_defaults']:
            values[key]={'a':a,'b':b,'c':c,'alpha':alpha,'alpha3':alpha3,'sigma':sigma,'m':meta['parameter_defaults'].get('m',m)}[key]
        row=derive_entry(meta['id'],values)
        row['solution_status']='registered; use solve_reduction for an instantiated result'
        rows.append(row)
    return rows


def solution_catalog():
    """Symbolic continuous families, with all original source aliases retained."""
    import copy
    return copy.deepcopy(_catalog())
