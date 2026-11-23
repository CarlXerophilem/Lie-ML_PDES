"""Exact 1D flow controls and stabilizers of explicitly specified initial data.

These experiments use the original equations and the already integrated
general point coefficients. They do not infer a solution from an initial
profile, an equivalence map, or a vanishing invariant-surface condition.
Zero-speed examples are separately labelled polynomial-closure extensions.
Run this module to print its JSON report; it never overwrites evidence.
"""
from __future__ import annotations

from collections.abc import Mapping
import json

import sympy as sp

from main import JetSpace, graph_check, json_ready, point_action, prolongation_coefficients
from models import BRANCHES, branch_model, t, x, h, u, B, g, K, G, m, n


def _context(branch, substitutions=None):
    model = branch_model(branch)
    substitutions = {sp.sympify(k):sp.sympify(v) for k,v in (substitutions or {}).items()}
    if not set(substitutions).issubset(set(model['parameters'])):
        raise ValueError('Specialize only parameters actually present in this branch')
    point_coordinates=set(model['independent_variables']+model['dependent_fields'])
    for value in substitutions.values():
        if value.free_symbols & point_coordinates or value.atoms(sp.Function):
            raise ValueError('Physical parameter substitutions must be constant in point coordinates')
        if value.is_real is False or value.is_finite is False or value in (sp.nan,sp.zoo):
            raise ValueError('Physical parameter substitutions must be finite real constants')
    cell = BRANCHES[branch]
    for parameter, active in ((g,True),(K,cell['K']),(G,cell['G'])):
        if active and parameter in substitutions and substitutions[parameter].is_nonpositive is True:
            raise ValueError(f'{parameter}>0 is required; select the appropriate zero branch instead')
    if cell['K']:
        exponent = sp.sympify(cell['m']).subs(substitutions)
        if exponent.is_number and (not 1 <= exponent <= 4 or
                ('generic' in branch and exponent == 3)):
            raise ValueError('Exponent specialization leaves the registered m stratum')
    if branch == 'slope_only':
        exponent = n.subs(substitutions)
        if exponent.is_number and not 0 <= exponent <= 4:
            raise ValueError('The slope-only branch requires 0<=n<=4')
    conditions=[sp.Gt(g,0,evaluate=False)]
    if cell['K']:
        conditions += [sp.Gt(K,0,evaluate=False),sp.Ge(sp.sympify(cell['m']),1,evaluate=False),
                       sp.Le(sp.sympify(cell['m']),4,evaluate=False)]
        if 'generic' in branch:
            conditions.append(sp.Ne(sp.sympify(cell['m']),3,evaluate=False))
    if cell['G']:
        conditions.append(sp.Gt(G,0,evaluate=False))
    if branch=='slope_only':
        conditions += [sp.Ge(n,0,evaluate=False),sp.Le(n,4,evaluate=False)]
    specialized=[condition.subs(substitutions,simultaneous=True) for condition in conditions]
    if any(value is sp.S.false for value in specialized):
        raise ValueError('Parameter specialization contradicts the registered branch')
    specialized=[value for value in specialized if value is not sp.S.true]
    for value in substitutions.values():
        if value.is_real is None:
            specialized.append(sp.Contains(value,sp.S.Reals,evaluate=False))
        if value.is_finite is None:
            specialized.append(sp.Q.finite(value))
    model['branch_conditions']['original_guards']=model['branch_conditions']['guards']
    model['branch_conditions']['guards']=['h>0','u>0']+list(map(str,specialized))
    model['branch_conditions']['substitutions']=substitutions
    space = JetSpace(model['independent_variables'],model['dependent_fields'])
    equations = tuple(e.subs(substitutions,simultaneous=True) for e in model['equations'])
    return model, space, equations, substitutions


def _solved_coefficients(branch, substitutions):
    """Import solved arbitrary coefficients, without rediscovering an ansatz."""
    coordinates = (t,x,h,u,B)
    cell = BRANCHES[branch]
    if cell['G']:
        from research_slope import general_solution
        exponent = sp.sympify(cell['m'] if cell['K'] else cell['n']).subs(substitutions)
        solved = general_solution(branch,coordinates=coordinates,exponent=exponent)
    else:
        from research_first_order import general_solution
        solved = general_solution(branch,coordinates=coordinates)
    old_constants = tuple(solved['free_constants'])
    constants = tuple(sp.Dummy('c_'+str(c),real=True) for c in old_constants)
    rename = dict(zip(old_constants,constants))
    coefficients = tuple(sp.sympify(v).xreplace(rename).subs(substitutions,simultaneous=True)
                         for v in solved['coefficients'])
    return coefficients, constants, tuple(map(str,old_constants))


def _flow_result(branch, graph, substitutions):
    model, space, equations, substitutions = _context(branch,substitutions)
    graph = tuple(sp.sympify(v).subs(substitutions,simultaneous=True) for v in graph)
    checked = graph_check(space,equations,graph)
    chart_guards = (sp.Gt(graph[0],0,evaluate=False),sp.Gt(graph[1],0,evaluate=False))
    outside = graph[0].is_nonpositive is True or graph[1].is_nonpositive is True
    return {'branch':branch,'graph':graph,'check':checked,
            'status':('outside_declared_chart' if outside else
                      'verified_exact_solution' if checked['is_solution'] else 'negative_pde_control'),
            'chart_guards':chart_guards,'parameter_guards':model['branch_conditions']['guards'],
            'parameter_substitutions':substitutions,
            'scope':'constructed smooth solution on recorded chart',
            'arbitrary_data_claim':False}


def uniform_flow(branch, *, depth=2, velocity=3, datum=1, substitutions=None):
    """h=H0>0, u=U0>0, B=B0; all spatial/time derivatives vanish."""
    return _flow_result(branch,(depth,velocity,datum),substitutions)


def constant_slope_flow(branch, *, depth=2, velocity=3, slope=sp.Rational(1,5),
                        datum=1, time0=0, substitutions=None):
    """h=H0, u=U0-g*slope*(t-time0), B=slope*x+B0.

    The nonzero sediment flux can depend on time, while its x derivative
    vanishes. The velocity positivity guard restricts the time interval.
    """
    depth,velocity,slope,datum,time0 = map(sp.sympify,(depth,velocity,slope,datum,time0))
    return _flow_result(branch,(depth,velocity-g*slope*(t-time0),slope*x+datum),substitutions)


def sediment_flux_variation(branch, coefficients, substitutions=None):
    """Return the actual first prolongation of J, including the bed gradient."""
    model,space,_,substitutions = _context(branch,substitutions)
    coefficients = tuple(sp.sympify(v).subs(substitutions,simultaneous=True) for v in coefficients)
    if len(coefficients) != 5:
        raise ValueError('Expected coefficients (tau,xi,eta_h,eta_u,eta_B)')
    cell = BRANCHES[branch]
    Bx = space.jet(B,(0,1))
    flux = K*u**cell['m'] if cell['K'] else sp.S.Zero
    if cell['G']:
        flux -= G*u**cell['n']*Bx
    flux = flux.subs(substitutions,simultaneous=True)
    prolonged = prolongation_coefficients(space,coefficients[:2],coefficients[2:],1,'recursive')
    variation = point_action(space,flux,coefficients[:2],coefficients[2:],order=1,
                             method='recursive',coefficients=prolonged)
    return {'flux':flux,'variation':sp.simplify(variation),'bed_slope_jet':Bx,
            'parameter_guards':model['branch_conditions']['guards'],
            'parameter_substitutions':substitutions,
            'slope_variation':sp.simplify(prolonged[(2,(0,1))]),
            'formula':'eta_Bx = D_x eta_B - B_t D_x tau - B_x D_x xi'}


def _zero_state(expr, branch, substitutions):
    """Use the declared positive active coefficients, retaining other strata."""
    positive = {}
    for parameter,active in ((g,True),(K,BRANCHES[branch]['K']),(G,BRANCHES[branch]['G'])):
        if active and parameter not in substitutions:
            positive[parameter] = sp.Dummy('positive_'+str(parameter),positive=True)
    return sp.simplify(expr.xreplace(positive)).is_zero


def _split_polynomial_identities(identities):
    equations, guards = [], []
    for identity in identities:
        numerator,denominator = sp.fraction(sp.cancel(sp.sympify(identity)))
        if denominator != 1:
            guards.append(sp.Ne(denominator,0,evaluate=False))
        try:
            equations.extend(sp.Poly(numerator,x).coeffs())
        except sp.PolynomialError:
            return None, guards
    return tuple(dict.fromkeys(sp.simplify(v) for v in equations if v != 0)),guards


def _guarded_homogeneous_solve(equations, constants, branch, substitutions):
    """Exact linear elimination that records every unproved nonzero pivot.

    A generic linsolve result can silently lose a profile-parameter rank-drop
    branch. Prefer provably nonzero pivots, and expose the other branches.
    """
    if not equations:
        return constants, (), (), tuple(constants)
    matrix,rhs = sp.linear_eq_to_matrix(equations,constants)
    if any(v != 0 for v in rhs):
        raise ValueError('A stabilizer determining system must be homogeneous')
    row, pivots, guards, zero_branches = 0, [], [], []
    for column in range(matrix.cols):
        candidates = [(i,_zero_state(matrix[i,column],branch,substitutions))
                      for i in range(row,matrix.rows)]
        nonzero = [i for i,state in candidates if state is False]
        undecided = [i for i,state in candidates if state is None]
        if not nonzero and not undecided:
            continue
        selected = (nonzero or undecided)[0]
        matrix.row_swap(row,selected)
        pivot = sp.factor(matrix[row,column])
        if not nonzero:
            guards.append(sp.Ne(pivot,0,evaluate=False))
            zero_branches.append(sp.Eq(pivot,0,evaluate=False))
        matrix.row_op(row,lambda value,j:sp.cancel(value/pivot))
        for i in range(matrix.rows):
            if i == row:
                continue
            factor = matrix[i,column]
            if factor != 0:
                matrix.row_op(i,lambda value,j:sp.cancel(value-factor*matrix[row,j]))
        pivots.append(column)
        row += 1
        if row == matrix.rows:
            break
    free = [j for j in range(len(constants)) if j not in pivots]
    solution = list(constants)
    for i,column in enumerate(pivots):
        solution[column] = sp.simplify(-sum(matrix[i,j]*constants[j] for j in free))
    return tuple(solution),tuple(guards),tuple(zero_branches),tuple(constants[j] for j in free)


def initial_data_stabilizer(branch, initial_profiles, *, time0=0, endpoints=None,
                            sediment_flux=None, substitutions=None):
    """Stabilize one fixed t=time0 initial graph using the solved coefficients.

    The equations are tau|initial=0 and eta_i-xi*U0_i'=0. Optional endpoints
    are fixed spatial boundaries (xi=0). A scalar sediment_flux prescribes a
    profile on the initial slice; a mapping {endpoint: Q(t)} prescribes its
    value at fixed endpoints on that slice. No future boundary trace is
    inferred from initial data, and compatibility is checked independently.
    """
    model,space,equations,substitutions = _context(branch,substitutions)
    if len(initial_profiles) != 3:
        raise ValueError('Provide one initial profile for each of (h,u,B)')
    profiles = tuple(sp.sympify(v).subs(substitutions,simultaneous=True) for v in initial_profiles)
    if any(v.has(t,h,u,B) for v in profiles):
        raise ValueError('Initial profiles must depend on x and data parameters only')
    time0 = sp.sympify(time0)
    if time0.has(t,x,h,u,B):
        raise ValueError('The initial time must be a constant')
    coefficients,constants,constant_names = _solved_coefficients(branch,substitutions)
    tau,xi,*etas = coefficients
    initial_subs = dict(zip((h,u,B),profiles)) | {t:time0}
    identities = [tau.subs(initial_subs,simultaneous=True)]
    identities += [(eta-xi*sp.diff(profile,x)).subs(initial_subs,simultaneous=True)
                   for eta,profile in zip(etas,profiles)]
    fixed_endpoints = [sp.sympify(v) for v in (endpoints or ())]
    if isinstance(sediment_flux,Mapping):
        fixed_endpoints.extend(sp.sympify(v) for v in sediment_flux)
    fixed_endpoints = list(dict.fromkeys(fixed_endpoints))
    if any(v.has(t,x,h,u,B) for v in fixed_endpoints):
        raise ValueError('Endpoints must be constant positions')
    for location in fixed_endpoints:
        identities.append(xi.subs(initial_subs,simultaneous=True).subs(x,location))

    flux_data = {'compatibility_residuals':(),'variation_identities':(),
                 'compatible':True,'scope':'no sediment flux specified'}
    if sediment_flux is not None:
        variation = sediment_flux_variation(branch,coefficients,substitutions)
        # The integrated coefficients have D_x tau=0. If an adapter ever
        # changes this, initial data alone cannot supply the missing B_t.
        if sp.simplify(space.D(tau,1)) != 0:
            raise ValueError('Flux trace needs time jets when D_x tau is not zero')
        jet_subs = dict(initial_subs)
        for field,profile in zip((h,u,B),profiles):
            jet_subs[space.jet(field,(0,1))] = sp.diff(profile,x)
            jet_subs[space.jet(field,(1,0))] = 0
        actual_flux = sp.simplify(variation['flux'].xreplace(jet_subs))
        compatibility,flux_identities = [],[]
        traces = tuple(sediment_flux.items()) if isinstance(sediment_flux,Mapping) else ((None,sediment_flux),)
        for location,prescribed in traces:
            prescribed = sp.sympify(prescribed).subs(substitutions,simultaneous=True)
            if prescribed.has(h,u,B):
                raise ValueError('Prescribed flux may depend on t,x and parameters, not fields')
            defect = actual_flux-prescribed.subs(t,time0)
            transformed = (variation['variation']-tau*sp.diff(prescribed,t)-xi*sp.diff(prescribed,x))
            transformed = transformed.xreplace(jet_subs)
            if location is not None:
                defect = defect.subs(x,sp.sympify(location))
                transformed = transformed.subs(x,sp.sympify(location))
            compatibility.append(sp.simplify(defect))
            flux_identities.append(sp.simplify(transformed))
        compatible_states = [_zero_state(v,branch,substitutions) for v in compatibility]
        compatible = False if False in compatible_states else (True if all(s is True for s in compatible_states) else None)
        identities.extend(flux_identities)
        flux_data = {**variation,'initial_flux':actual_flux,
                     'compatibility_residuals':tuple(compatibility),
                     'compatibility_conditions':tuple(sp.Eq(v,0,evaluate=False) for v in compatibility if v!=0),
                     'variation_identities':tuple(flux_identities),'compatible':compatible,
                     'scope':'prescribed sediment flux on the initial slice only'}

    identities = tuple(sp.simplify(v) for v in identities)
    frozen = graph_check(space,equations,profiles)
    report = {'branch':branch,'profiles':profiles,'fixed_time':time0,
              'general_coefficients':coefficients,'constants':constants,
              'source_constant_names':constant_names,'tangency_identities':identities,
              'flux_data':flux_data,'fixed_endpoints':tuple(fixed_endpoints),
              'boundary_scope':'fixed endpoint tangency; flux values only on the initial slice',
              'chart_guards':(sp.Gt(profiles[0],0,evaluate=False),sp.Gt(profiles[1],0,evaluate=False)),
              'parameter_guards':model['branch_conditions']['guards'],
              'parameter_substitutions':substitutions,
              'frozen_profile_diagnostic':frozen,'pde_solution_claim':False,
              'scope':'stabilizer of specified initial graph; no existence or later boundary-data theorem'}
    split,denominator_guards = _split_polynomial_identities(identities)
    if split is None:
        return {**report,'status':'unresolved_functional_splitting',
                'reason':'Functional identities were retained; no finite x samples were used',
                'denominator_guards':tuple(denominator_guards)}
    solved,rank_guards,zero_branches,free = _guarded_homogeneous_solve(split,constants,branch,substitutions)
    replacement = dict(zip(constants,solved))
    remainders = tuple(sp.simplify(v.subs(replacement,simultaneous=True)) for v in identities)
    stabilized = tuple(sp.simplify(v.subs(replacement,simultaneous=True)) for v in coefficients)
    if profiles[0].is_nonpositive is True or profiles[1].is_nonpositive is True:
        status = 'outside_declared_chart'
    elif flux_data['compatible'] is False:
        status = 'incompatible_prescribed_flux'
    elif any(v != 0 for v in remainders):
        status = 'unresolved_tangency_verification'
    elif rank_guards or flux_data['compatible'] is None:
        status = 'conditional_initial_data_stabilizer'
    else:
        status = 'verified_initial_data_stabilizer'
    return {**report,'status':status,'constant_constraints':split,'coefficient_solution':solved,
            'free_constants':free,'dimension':len(free),'stabilized_coefficients':stabilized,
            'verification_residuals':remainders,'rank_guards':rank_guards,
            'unresolved_zero_pivot_branches':zero_branches,'denominator_guards':tuple(denominator_guards)}


def lake_control(branch, *, bed, level, substitutions=None):
    """Check u=0 only where the signed closure has a smooth polynomial extension.

    Active transport allows m=1 or 3; active abs(u)**n diffusivity allows
    n=0,2,4. Generic real exponents and odd absolute-value diffusivities are
    not evaluated at zero. Level and bed may both depend on time: the PDE
    decides whether their motion is compatible, not a static-bed assumption.
    """
    model,space,equations,substitutions = _context(branch,substitutions)
    cell = BRANCHES[branch]
    effective_m = sp.sympify(cell['m']).subs(substitutions) if cell['K'] else None
    effective_n = sp.sympify(cell['n']).subs(substitutions) if cell['G'] else None
    allowed = ((not cell['K'] or effective_m in (sp.Integer(1),sp.Integer(3)))
               and (not cell['G'] or effective_n in (sp.Integer(0),sp.Integer(2),sp.Integer(4))))
    bed,level = (sp.sympify(v).subs(substitutions,simultaneous=True) for v in (bed,level))
    graph = (sp.simplify(level-bed),sp.S.Zero,bed)
    base = {'branch':branch,'graph':graph,'effective_exponents':(effective_m,effective_n),
            'parameter_guards':model['branch_conditions']['guards'],
            'parameter_substitutions':substitutions,
            'inside_classified_positive_speed_chart':False,
            'scope':'explicit polynomial-closure extension; no zero-speed maximal-algebra claim',
            'chart_guards':(sp.Gt(graph[0],0,evaluate=False),)}
    if not allowed:
        return {**base,'status':'outside_declared_chart','check':None,
                'reason':'u=0 requires the separately declared signed polynomial closure'}
    # Specialize and simplify the polynomial equations before inserting u=0;
    # never interpret 0**(n-1)*0 as a generic-real-exponent certificate.
    checked = graph_check(space,tuple(sp.expand(e) for e in equations),graph)
    outside = graph[0].is_nonpositive is True
    return {**base,'check':checked,'status':('outside_declared_chart' if outside else
            'verified_polynomial_zero_speed_solution' if checked['is_solution'] else 'negative_pde_control')}


def run_data_experiments():
    """All eight registry cells, concrete initial profiles, and chart controls."""
    branches = {}
    for branch in BRANCHES:
        initial = {name:initial_data_stabilizer(branch,(2,3,bed)) for name,bed in
                   (('flat',sp.S.One),('linear',1+x),('quadratic',1+x**2))}
        branches[branch] = {
            'uniform_flow':uniform_flow(branch),
            'constant_slope_accelerating_flow':constant_slope_flow(branch),
            'initial_data':initial,
            'fixed_endpoints_uniform':initial_data_stabilizer(branch,(2,3,1),endpoints=(0,1)),
        }
    lakes = {
        'static_quadratic_constant_diffusion':lake_control('slope_only',bed=x**2,level=3,substitutions={n:0}),
        'moving_quadratic_constant_diffusion':lake_control('slope_only',bed=x**2+2*G*t,
                                                           level=3+2*G*t,substitutions={n:0}),
        'static_quadratic_vanishing_at_zero_diffusion':lake_control('slope_attachment_cubic',bed=x**2,level=3),
        'generic_exponent_zero_speed':lake_control('grass_generic',bed=1,level=3),
    }
    return {'branches':branches,'zero_speed_extension_controls':lakes,
            'all_exact_flow_controls_passed':all(
                value[key]['status']=='verified_exact_solution' for value in branches.values()
                for key in ('uniform_flow','constant_slope_accelerating_flow')),
            'all_concrete_initial_stabilizers_verified':all(
                result['status']=='verified_initial_data_stabilizer' for value in branches.values()
                for result in value['initial_data'].values()),
            'claim_scope':'constructed controls and specified initial-data stabilizers only'}


if __name__ == '__main__':
    report = run_data_experiments()
    print(json.dumps(json_ready(report),ensure_ascii=False,indent=2))
    raise SystemExit(0 if report['all_exact_flow_controls_passed']
                     and report['all_concrete_initial_stabilizers_verified'] else 1)
