"""Verified one-generator graph reductions derived from equations and a basis.

The supported characteristic integrations are translations and homogeneous
diagonal fields. Unsupported generators/charts return an explicit unresolved
record. No literature ODE, nonsingularity assumption, or solved leading matrix
is substituted for the original equations.
"""
from __future__ import annotations

import sympy as sp

from main import JetSpace, graph_check, point_action, verify_generator


# 1. Model specialization and constant-coefficient membership in the solved algebra.
def _context(model, substitutions=None):
    subs = dict(model.get("branch_conditions", {}).get("substitutions", {}))
    subs.update(substitutions or {})
    xs = tuple(model["independent_variables"])
    fields = tuple(model["dependent_fields"])
    if len(xs) != 2 or len(fields) != 3:
        raise ValueError("This reduction adapter supports two base and three field coordinates")
    space = JetSpace(xs, fields)
    equations = tuple(sp.sympify(e).subs(subs, simultaneous=True) for e in model["equations"])
    return space, equations, subs


def _unresolved(reason, **details):
    return {"status": "unresolved", "reason": reason, **details}


def _constant_identities(expressions, coordinates):
    equations = []
    for expr in expressions:
        numerator = sp.fraction(sp.together(expr))[0]
        try:
            equations.extend(sp.Poly(numerator, *coordinates).coeffs())
        except sp.PolynomialError:
            return None
    return equations


def basis_combination(coordinates, basis, target):
    """Find constant weights, independently of basis ordering or normalization."""
    if not basis:
        return _unresolved("empty supplied basis")
    vectors = tuple(sp.Matrix(v) for v in basis)
    if any(v.shape != (len(coordinates), 1) for v in vectors):
        return _unresolved("basis coordinate dimension mismatch")
    weights = sp.symbols(f"basis_weight_0:{len(vectors)}")
    difference = sum((w*v for w,v in zip(weights,vectors)), sp.zeros(len(coordinates),1))-sp.Matrix(target)
    equations = _constant_identities(difference, coordinates)
    if equations is None:
        return _unresolved("nonpolynomial constant basis decomposition is unsupported")
    solutions = sp.linsolve(equations, weights)
    if solutions == sp.EmptySet:
        return _unresolved("requested generator is outside the supplied constant span")
    solution = next(iter(solutions))
    # Redundant bases may leave arbitrary weights. Choose zero only for those
    # decomposition parameters; physical/model parameters remain untouched.
    free_weights = set(weights) & set().union(*(v.free_symbols for v in solution))
    values = tuple(sp.simplify(v.subs(dict.fromkeys(free_weights, 0))) for v in solution)
    residual = difference.subs(dict(zip(weights, values)))
    if any(sp.simplify(v) != 0 for v in residual):
        return _unresolved("constant basis membership could not be certified")
    return {"status":"verified", "weights":values, "residual":tuple(residual)}


# 2. Exact chain pullback, invariant graph, and an undivided leading system.
def _positive_simplify(expr, positive_coordinates=()):
    replacements = {v:sp.Dummy(str(v)+"_positive", positive=True) for v in positive_coordinates}
    result = sp.sympify(expr).xreplace(replacements)
    result = sp.expand_power_base(result, force=True)
    result = sp.powsimp(sp.powdenest(result,force=True), force=True)
    result = sp.expand(result)
    # SymPy may leave t**(n/(n-2))/t and t**(2/(n-2)) structurally
    # different. Canonicalize actual powers of the positive orbit coordinate;
    # no independent placeholders for related powers are introduced.
    for orbit in replacements.values():
        grouped = {}
        for term in sp.Add.make_args(result):
            term = sp.factor_terms(term)
            exponent,coefficient = sp.S.Zero,sp.S.One
            # Remove factors structurally rather than dividing by a combined
            # symbolic power: generic polynomial cancel can leave reciprocal
            # powers with mathematically equal but different exponent forms.
            for factor in sp.Mul.make_args(term):
                if factor == orbit:
                    exponent += 1
                elif isinstance(factor,sp.Pow) and factor.base == orbit:
                    exponent += factor.exp
                else:
                    coefficient *= factor
            key = sp.cancel(exponent)
            grouped[key] = grouped.get(key,0)+coefficient
        result = sum(sp.factor(coefficient)*orbit**exponent
                     for exponent,coefficient in grouped.items())
        result = sp.expand(result)
    result = sp.factor(result)
    return result.xreplace({v:k for k,v in replacements.items()})


def _chain_jets(space, equations, amplitudes, z, invariant):
    profiles = (sp.Function("H",positive=True)(z),
                sp.Function("U",positive=True)(z),sp.Function("Z")(z))
    graph = tuple(a*f.subs(z,invariant) for a,f in zip(amplitudes,profiles))
    derivatives = tuple(sp.diff(invariant, coordinate) for coordinate in space.x)

    def chain(expr, axis):
        return sp.diff(expr,space.x[axis])+derivatives[axis]*sp.diff(expr,z)

    used = set().union(*(e.free_symbols for e in equations)) & space.reverse.keys()
    # First derivatives are also required for the characteristic identity.
    used |= {space.jet(a,space.unit(i)) for a in range(3) for i in range(2)}
    used |= set(space.u)
    mapping, chain_checks = {}, []
    for symbol in sorted(used,key=str):
        a,index = space.reverse[symbol]
        value = amplitudes[a]*profiles[a]
        direct = graph[a]
        for axis,count in enumerate(index):
            for _ in range(count):
                value = chain(value,axis)
                direct = sp.diff(direct,space.x[axis])
        mapping[symbol] = value
        chain_checks.append(value.subs(z,invariant)-direct)
    return profiles,graph,mapping,chain_checks


def _leading_system(equations, profiles, z):
    orders = []
    for field in profiles:
        found = [len(d.variables) for e in equations for d in e.atoms(sp.Derivative)
                 if d.expr == field and all(v == z for v in d.variables)]
        orders.append(max(found,default=0))
    leaders = tuple(sp.diff(f,z,k) if k else f for f,k in zip(profiles,orders))
    matrix = sp.Matrix(equations).jacobian(leaders)
    remainder = (sp.Matrix(equations)-matrix*sp.Matrix(leaders)).applyfunc(sp.simplify)
    affine = not any(v.has(*leaders) for v in matrix) and not any(v.has(*leaders) for v in remainder)
    determinant = sp.factor(matrix.det()) if matrix.rows == matrix.cols and affine else None
    return {"orders":tuple(orders),"leaders":leaders,"matrix":matrix,
            "remainder":remainder,"affine_in_leaders":affine,"determinant":determinant,
            "status":"implicit_ode_or_dae", "leading_matrix_inverted":False,
            "singular_locus_discarded":False}


def _certificate(space,equations,generator,amplitudes,z,invariant,orbit,
                 inverse_base,row_factors,positive_coordinates,guards,membership,kind):
    xi,eta = generator[:2],generator[2:]
    verified = verify_generator(space,equations,xi,eta)
    if not verified["verified"]:
        return _unresolved("supplied generator fails the original PDE symmetry test",generator_verification=verified)
    profiles,graph,jets,checks = _chain_jets(space,equations,amplitudes,z,invariant)
    simplify = lambda expr:_positive_simplify(expr,positive_coordinates)
    chain_residuals = tuple(simplify(v) for v in checks)
    raw = tuple(e.xreplace(jets) for e in equations)
    pulled = tuple(simplify(v.subs(inverse_base,simultaneous=True)) for v in raw)
    # The cross section orbit=0 has unit amplitude (t=1 or x=1 for dilation).
    orbit_coordinate = next(iter(positive_coordinates),None)
    reduced = tuple(simplify(v.subs(orbit_coordinate,1)) if orbit_coordinate is not None
                    else simplify(v) for v in pulled)
    reconstruction = tuple(simplify(v-factor*ode) for v,factor,ode in zip(pulled,row_factors,reduced))
    characteristic = []
    for a in range(3):
        expr = sp.sympify(eta[a]).xreplace(jets)
        for i in range(2):
            expr -= sp.sympify(xi[i]).xreplace(jets)*jets[space.jet(a,space.unit(i))]
        characteristic.append(simplify(expr.subs(inverse_base,simultaneous=True)))
    base_jacobian = simplify(sp.Matrix((orbit,invariant)).jacobian(space.x).det())
    # These first integrals are obtained from the characteristic ODEs, and the
    # complete point-field derivative proves their invariance independently.
    field_invariants = tuple(field/amp for field,amp in zip(space.u,amplitudes))
    point_coordinates = space.x+space.u
    invariant_checks = tuple(simplify(sum(generator[i]*sp.diff(expr,v)
                                         for i,v in enumerate(point_coordinates)))
                             for expr in (invariant,)+field_invariants)
    orbit_check = simplify(sum(xi[i]*sp.diff(orbit,v) for i,v in enumerate(space.x))-1)
    all_checks = chain_residuals+reconstruction+tuple(characteristic)+invariant_checks+(orbit_check,)
    if any(v != 0 for v in all_checks):
        return _unresolved("an exact characteristic/chain/reconstruction identity did not simplify to zero",
                           chain_residuals=chain_residuals,reconstruction_residuals=reconstruction,
                           characteristic_residuals=tuple(characteristic),invariant_residuals=invariant_checks,
                           orbit_residual=orbit_check)
    if any(e.has(*space.x) for e in reduced):
        return _unresolved("orbit dependence remains in reduced equations",reduced_equations=reduced)
    return {"status":"verified_reduction","kind":kind,"generator":tuple(generator),
            "basis_membership":membership,"generator_verification":verified,
            "profile_coordinate":z,"profiles":profiles,"base_invariant":invariant,
            "field_invariants":field_invariants,"orbit_coordinate":orbit,
            "chart_jacobian":base_jacobian,"chart_guards":tuple(guards),
            "chart_conditions":("H(z)>0","U(z)>0"),
            "graph":graph,"jet_substitution":jets,"chain_residuals":chain_residuals,
            "reduced_equations":reduced,"row_factors":tuple(row_factors),
            "reconstruction_residuals":reconstruction,
            "characteristic_residuals":tuple(characteristic),
            "invariant_residuals":invariant_checks,"orbit_residual":orbit_check,
            "leading_system":_leading_system(reduced,profiles,z),
            "graph_solution_claim":"original PDE iff these implicit reduced equations vanish on the guarded chart",
            "ode_order_reduction_claim":False,"optimal_subalgebra_claim":False}


# 3. Translation characteristics produce z=x-c*t without choosing a paper ODE.
def traveling_reduction(model,basis,speed=None,substitutions=None):
    space,equations,subs = _context(model,substitutions)
    t,x = space.x
    speed = sp.Symbol("c",real=True) if speed is None else sp.sympify(speed)
    if speed.has(*(space.x+space.u)):
        return _unresolved("traveling speed must be independent of point coordinates")
    vectors = tuple(sp.Matrix(v).subs(subs,simultaneous=True) for v in basis)
    generator = (sp.S.One,speed,sp.S.Zero,sp.S.Zero,sp.S.Zero)
    membership = basis_combination(space.x+space.u,vectors,generator)
    if membership["status"] != "verified":
        return membership
    # dt/ds=1, dx/ds=c and dy/ds=0 integrate to this full invariant set.
    z = sp.Symbol("z",real=True)
    return _certificate(space,equations,generator,(1,1,1),z,x-speed*t,t,
                        {x:z+speed*t},(1,1,1),(),(),membership,"traveling")


# 4. Homogeneous diagonal characteristics; chart branches are explicit.
def scaling_reduction(model,basis,generator,chart=None,substitutions=None):
    space,equations,subs = _context(model,substitutions)
    coordinates = space.x+space.u
    generator = tuple(sp.sympify(v).subs(subs,simultaneous=True) for v in generator)
    if len(generator) != len(coordinates):
        return _unresolved("generator coordinate dimension mismatch")
    vectors = tuple(sp.Matrix(v).subs(subs,simultaneous=True) for v in basis)
    membership = basis_combination(coordinates,vectors,generator)
    if membership["status"] != "verified":
        return membership
    weights = tuple(sp.simplify(sp.diff(v,coord)) for v,coord in zip(generator,coordinates))
    if any(sp.simplify(v-w*coord) != 0 or w.has(*coordinates)
           for v,w,coord in zip(generator,weights,coordinates)):
        return _unresolved("only diagonal homogeneous coefficients without additive terms are integrated")
    alpha,beta,*gamma = weights
    t,x = space.x
    if chart is None:
        if alpha.is_zero is False:
            chart = "time"
        elif alpha == 0 and beta.is_zero is False:
            chart = "space"
        elif alpha == 0 and beta == 0:
            return _unresolved("zero projected base rank cannot reduce the independent variables")
        else:
            return _unresolved("parameter-dependent base rank/chart requires a declared split",
                               required_split=(sp.Eq(alpha,0),sp.Ne(alpha,0)),
                               available_conditional_chart="time")
    z = sp.Symbol("z",real=True)
    if chart == "time":
        if alpha == 0:
            return _unresolved("time chart is singular because its generator coefficient is zero")
        invariant = x*t**(-beta/alpha)
        amplitudes = tuple(t**(w/alpha) for w in gamma)
        orbit = sp.log(t)/alpha
        inverse = {x:z*t**(beta/alpha)}
        positive = (t,)
        guards = (sp.Gt(t,0),sp.Ne(alpha,0,evaluate=False))
        divisor = alpha
        orbit_base = t
    elif chart == "space":
        if alpha != 0:
            return _unresolved("this spatial chart requires alpha=0 after parameter specialization")
        if beta == 0:
            return _unresolved("space chart is singular because its generator coefficient is zero")
        invariant = t
        amplitudes = tuple(x**(w/beta) for w in gamma)
        orbit = sp.log(x)/beta
        inverse = {t:z}
        positive = (x,)
        guards = (sp.Gt(x,0),sp.Ne(beta,0,evaluate=False))
        divisor = beta
        orbit_base = x
    else:
        return _unresolved("unknown chart; choose time or space")

    # Derive each row's actual weight by prolongation. This supports diagonal
    # semi-invariant rows; row-mixing symmetries are deliberately unresolved.
    row_weights = []
    for equation in equations:
        action = point_action(space,equation,generator[:2],generator[2:])
        ratio = sp.simplify(action/equation)
        if ratio.has(*coordinates) or ratio.free_symbols & space.reverse.keys():
            return _unresolved("PDE rows are not scalar semi-invariants under this diagonal generator")
        if sp.simplify(action-ratio*equation) != 0:
            return _unresolved("could not certify an equation scaling weight")
        row_weights.append(ratio)
    factors = tuple(orbit_base**(w/divisor) for w in row_weights)
    result = _certificate(space,equations,generator,amplitudes,z,invariant,orbit,
                          inverse,factors,positive,guards,membership,"diagonal_scaling")
    result.update({"diagonal_weights":weights,"row_weights":tuple(row_weights),"selected_chart":chart})
    return result


# 5. Constructed exact graphs and fixed initial-slice stabilizers are separate gates.
def constant_slope_graph(model,slope=None):
    space,equations,_ = _context(model)
    t,x = space.x
    h0,u0 = sp.symbols("h0 u0",positive=True)
    b0 = sp.Symbol("b0",real=True)
    slope = sp.Symbol("slope",real=True) if slope is None else sp.sympify(slope)
    gravities = [p for p in model["parameters"] if str(p)=="g"]
    if len(gravities)!=1:
        return _unresolved("constant-slope construction requires the declared gravity parameter g")
    graph = (h0,u0-gravities[0]*slope*t,slope*x+b0)
    checked = graph_check(space,equations,graph)
    return {"status":"verified_exact_graph" if checked["is_solution"] else "unresolved",
            "graph":graph,"guards":(sp.Gt(graph[1],0),sp.Gt(h0,0)),
            "check":checked,"scope":"constructed uniform-depth, constant-bed-slope solution"}


def initial_data_stabilizer(model,basis,initial_profiles,time0=0):
    """Tangent subalgebra of one fixed initial slice and its prescribed graph."""
    space,_,_ = _context(model)
    t,x = space.x
    if len(initial_profiles)!=3:
        return _unresolved("one initial profile per field is required")
    profiles = tuple(map(sp.sympify,initial_profiles))
    if any(v.has(t) for v in profiles):
        return _unresolved("initial profiles must be functions of x, not t")
    constants = sp.symbols(f"stabilizer_c0:{len(basis)}")
    generator = sum((v*sp.Matrix(b) for v,b in zip(constants,basis)),sp.zeros(5,1))
    substitution = dict(zip(space.u,profiles)) | {t:sp.sympify(time0)}
    tangent = [generator[0].subs(substitution,simultaneous=True)]
    tangent += [(generator[a+2]-generator[1]*sp.diff(profiles[a],x)).subs(substitution,simultaneous=True)
                for a in range(3)]
    equations = _constant_identities(tangent,(x,))
    if equations is None:
        return _unresolved("nonpolynomial initial-graph identities require further functional splitting",
                           tangent_identities=tuple(tangent))
    solution = sp.linsolve(equations,constants)
    if solution == sp.EmptySet:
        return _unresolved("unexpected inconsistent homogeneous stabilizer system")
    solved = next(iter(solution))
    tangent_residuals = tuple(sp.simplify(v.subs(dict(zip(constants,solved)),simultaneous=True)) for v in tangent)
    return {"status":"verified_initial_graph_stabilizer" if all(v==0 for v in tangent_residuals) else "unresolved",
            "coefficient_solution":solved,"constants":constants,
            "tangent_identities":tuple(tangent),"verification_residuals":tangent_residuals,
            "fixed_time":sp.sympify(time0),"scope":"fixed initial slice and initial graph only; no lateral boundary claim"}
