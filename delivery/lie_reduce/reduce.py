"""Local invariant graph reduction, multi-profile first integrals, and deterministic ODE elimination."""
from dataclasses import dataclass, field
import sympy as sp
from sympy.core.function import AppliedUndef

from .identities import nonzero_record, zero_record


@dataclass
class Graph:
    z: sp.Symbol
    invariant: sp.Expr
    profiles: tuple
    lifts: tuple
    section: dict
    conditions: tuple = ()
    orbit_coordinates: dict = field(default_factory=dict)


@dataclass
class ReducedODE:
    model: str
    status: str
    reason: str = ''
    graph: object = None
    equations: tuple = ()
    reduced_equations: tuple = ()
    integrated_ode: sp.Expr | None = None
    target_profile: sp.Expr | None = None
    eliminated: dict = field(default_factory=dict)
    reconstructed_lifts: tuple = ()
    weights: tuple = ()
    first_integrals: tuple = ()
    leading_coefficients: tuple = ()
    preserved_parameters: tuple = ()
    conditions: tuple = ()
    checks: dict = field(default_factory=dict)
    scope: str = 'local invariant orbit chart'
    degree: int | None = None


def _drop_piecewise(expr):
    def _pick(*args):
        for val, cond in args:
            if isinstance(cond, sp.Ne) or cond is sp.S.true or cond is True:
                return val
        return args[0][0]
    return expr.replace(sp.Piecewise, _pick)


def multi_flux_check(expr, profiles, z):
    """Exact variational Euler-operator check and constructive first integral for multi-profile ODEs."""
    expr = sp.expand(expr)
    active = [F for F in profiles if expr.has(F)]
    if not active:
        return {'status': 'not_found', 'reason': 'no profile dependence'}
    orders = [d.derivative_count for d in expr.atoms(sp.Derivative) if d.expr in active]
    n = max(orders, default=0)
    if n < 1:
        return {'status': 'not_found', 'reason': 'no derivative'}

    Y = [[sp.Symbol(f'_J_{a}_{k}', real=True) for k in range(2 * n + 2)] for a in range(len(active))]
    mapping = {}
    for a, F in enumerate(active):
        for k in range(n, -1, -1):
            mapping[sp.diff(F, z, k) if k else F] = Y[a][k]
    r = expr.xreplace(mapping)

    def total_d(e):
        res = sp.diff(e, z)
        for a in range(len(active)):
            for k in range(len(Y[a]) - 1):
                de = sp.diff(e, Y[a][k])
                if de != 0:
                    res += Y[a][k + 1] * de
        return sp.expand(res)

    def iter_d(e, steps):
        for _ in range(steps):
            e = total_d(e)
        return e

    for a in range(len(active)):
        euler = sum((-1)**k * iter_d(sp.diff(r, Y[a][k]), k) for k in range(n + 1))
        ev = zero_record(euler)
        if ev['status'] != 'proved_zero':
            return {'status': 'not_total_derivative', 'euler_operator': euler, 'evidence': ev}

    remainder = r
    flux = sp.S.Zero
    for k in range(n, 0, -1):
        if zero_record(remainder)['status'] == 'proved_zero':
            remainder = sp.S.Zero
            break
        # Repeatedly peel elementary profile quadratures at jet order k (coupled potentials cancel across components)
        for _ in range(len(active) + 1):
            if zero_record(remainder)['status'] == 'proved_zero':
                remainder = sp.S.Zero
                break
            peeled = False
            for a in range(len(active)):
                coeff = sp.diff(remainder, Y[a][k])
                if zero_record(coeff)['status'] == 'proved_zero':
                    continue
                cand = _drop_piecewise(sp.integrate(coeff, Y[a][k - 1], manual=True))
                if cand.has(sp.Integral, sp.hyper, sp.meijerg) and not any(
                    p.is_Pow and not p.exp.is_Integer for p in coeff.atoms(sp.Pow)
                ):
                    cand = _drop_piecewise(sp.integrate(coeff, Y[a][k - 1], meijerg=False))
                if cand.has(sp.Integral, sp.hyper, sp.meijerg):
                    continue
                flux += cand
                remainder = sp.together(sp.powsimp(sp.expand(remainder - total_d(cand))))
                peeled = True
                break
            if not peeled:
                # Check if any unresolved derivative at order k remains
                if any(zero_record(sp.diff(remainder, Y[a][k]))['status'] != 'proved_zero' for a in range(len(active))):
                    return {'status': 'not_elementary', 'reason': 'non-elementary quadrature in flux reconstruction'}
                break
    if zero_record(remainder)['status'] != 'proved_zero':
        cand_z = _drop_piecewise(sp.integrate(remainder, z, manual=True))
        if cand_z.has(sp.Integral, sp.hyper, sp.meijerg) and not any(
            p.is_Pow and not p.exp.is_Integer for p in remainder.atoms(sp.Pow)
        ):
            cand_z = _drop_piecewise(sp.integrate(remainder, z, meijerg=False))
        if cand_z.has(sp.Integral, sp.hyper, sp.meijerg):
            return {'status': 'not_elementary', 'reason': 'non-elementary z-quadrature in flux reconstruction'}
        flux += cand_z
    defect = zero_record(r - total_d(flux))
    if defect['status'] != 'proved_zero':
        return {'status': 'not_found', 'reason': 'constructive flux identity failed'}

    inverse = {Y[a][k]: (sp.diff(F, z, k) if k else F) for a, F in enumerate(active) for k in range(n + 1)}
    return {'status': 'verified', 'flux': sp.simplify(flux.xreplace(inverse)), 'identity_remainder': 0}


def flux_check(expr, F, z):
    return multi_flux_check(expr, (F,), z)


def _strip_nonderiv_factors(expr, profiles):
    """Strip only z-free undifferentiated profile/parameter multipliers so radial 1/z weights stay intact."""
    num, den = sp.together(expr).as_numer_denom()
    if not any(e.is_Pow and not e.exp.is_Integer for e in num.atoms(sp.Pow)):
        factors = sp.Mul.make_args(sp.factor(num))
    else:
        factors = sp.Mul.make_args(num)
    core = sp.S.One
    has_deriv = False
    for f in factors:
        if any(d.expr in profiles for d in f.atoms(sp.Derivative)) or f.has(*[a for p in profiles for a in p.args]):
            if any(d.expr in profiles for d in f.atoms(sp.Derivative)) or not f.atoms(AppliedUndef):
                core *= f
            if any(d.expr in profiles for d in f.atoms(sp.Derivative)):
                has_deriv = True
    if not has_deriv:
        return expr
    den_core = sp.S.One
    for f in sp.Mul.make_args(den):
        if any(d.expr in profiles for d in f.atoms(sp.Derivative)) or any(f.has(P) for P in profiles) or f.free_symbols:
            den_core *= f
    return core / den_core


def _fast_clean(expr):
    if any(p.is_Pow and not p.exp.is_Integer for p in expr.atoms(sp.Pow)):
        return sp.together(sp.powsimp(sp.expand(expr)))
    return sp.cancel(expr)


def _clean_power_pullback(expr):
    expr = expr.replace(
        lambda e: e.is_Pow and not e.exp.is_Integer,
        lambda e: sp.trigsimp(sp.expand(e.base))**e.exp,
    )
    expr = sp.expand_power_base(expr, force=True)
    return _fast_clean(expr)


def _apply_eliminated(expr, eliminated, z):
    if not eliminated:
        return expr
    out = expr
    # First substitute cyclic derivatives (and higher derivatives thereof)
    deriv_subs = {}
    for k, v in eliminated.items():
        if isinstance(k, sp.Derivative):
            F_b = k.expr
            max_ord = max((d.derivative_count for d in out.atoms(sp.Derivative) if d.expr == F_b), default=0)
            for ord_k in range(max_ord, 0, -1):
                deriv_subs[sp.diff(F_b, z, ord_k)] = sp.diff(v, z, ord_k - 1)
    if deriv_subs:
        out = out.xreplace(deriv_subs).doit()
    alg_subs = {k: v for k, v in eliminated.items() if not isinstance(k, sp.Derivative)}
    if alg_subs:
        out = out.subs(alg_subs).doit()
    return _fast_clean(out)


def integrate_and_eliminate(equations, profiles, z, positive=(), lifts=()):
    """Deterministically integrate exact total-derivative balances and eliminate algebraic/cyclic profiles."""
    eq_list = list(equations)
    eliminated = {}
    integrals = []
    integrated_ode = None
    const_idx = 1

    # Pass 0: integrate all raw exact balances BEFORE substituting rational eliminations into symbolic powers
    pending_fluxes = []
    surviving_raw = []
    for eq in eq_list:
        core = _strip_nonderiv_factors(eq, profiles)
        found = None
        used_mu = sp.S.One
        for mu in (sp.S.One, z, 1 / z, z**2):
            fc = multi_flux_check(sp.together(mu * core), profiles, z)
            if fc['status'] == 'verified':
                found = fc
                used_mu = mu
                break
        if found is not None and len(equations) > 1:
            C_sym = sp.Symbol(f'C{const_idx}', real=True)
            const_idx += 1
            rec = {'constant': C_sym, 'flux': found['flux'], 'multiplier': used_mu, 'status': 'verified'}
            integrals.append(rec)
            pending_fluxes.append((C_sym, found['flux'], eq))
        else:
            surviving_raw.append(eq)

    # If all equations were exact (e.g. E1 has 3 exact equations), keep the last differential equation un-eliminated
    if pending_fluxes and not surviving_raw:
        last_C, last_flux, last_eq = pending_fluxes.pop()
        surviving_raw.append(last_eq)

    # Solve pending exact fluxes for algebraic profiles first, then cyclic derivatives
    for _ in range(len(pending_fluxes) + 1):
        progressed = False
        for p_idx, (C_sym, flux_expr, orig_eq) in enumerate(list(pending_fluxes)):
            cur_flux = _apply_eliminated(flux_expr, eliminated, z)
            deriv_profiles = {d.expr for d in cur_flux.atoms(sp.Derivative)}
            nonint_pows = [p for p in cur_flux.atoms(sp.Pow) if not p.exp.is_Integer]
            alg_candidates = [
                F for F in profiles
                if cur_flux.has(F) and F not in deriv_profiles
                and not any(p.base.has(F) for p in nonint_pows)
            ]
            alg_candidates.sort(key=lambda F: (
                sum(1 for e in surviving_raw if e.has(sp.diff(F, z))),
                -profiles.index(F),
            ))
            solved = False
            for F_a in alg_candidates:
                try:
                    sol = sp.solve(cur_flux - C_sym, F_a, simplify=False)
                except NotImplementedError:
                    sol = []
                if len(sol) == 1 and not sol[0].has(F_a):
                    eliminated[F_a] = _fast_clean(sol[0])
                    for k_prev in list(eliminated):
                        if k_prev != F_a:
                            eliminated[k_prev] = _apply_eliminated(eliminated[k_prev], {F_a: eliminated[F_a]}, z)
                    pending_fluxes.pop(p_idx)
                    progressed = True
                    solved = True
                    break
            if solved:
                break
            cyclic_candidates = [
                d.expr for d in cur_flux.atoms(sp.Derivative)
                if d.derivative_count == 1
                and not cur_flux.xreplace({d: sp.Dummy()}).has(d.expr)
                and not any(_apply_eliminated(other, eliminated, z).xreplace(
                    {sp.diff(d.expr, z, k): sp.Dummy() for k in range(1, 5)}).has(d.expr)
                    for other in surviving_raw)
            ]
            for F_b in cyclic_candidates:
                dF = sp.diff(F_b, z)
                try:
                    sol = sp.solve(cur_flux - C_sym, dF, simplify=False)
                except NotImplementedError:
                    sol = []
                if len(sol) == 1 and not sol[0].has(F_b):
                    eliminated[dF] = _fast_clean(sol[0])
                    pending_fluxes.pop(p_idx)
                    progressed = True
                    solved = True
                    break
            if solved:
                break
        if not progressed:
            break

    for _, _, leftover_eq in pending_fluxes:
        surviving_raw.append(leftover_eq)
    eq_list = [_apply_eliminated(e, eliminated, z) for e in surviving_raw]
    eq_list = [e for e in eq_list if zero_record(e)['status'] != 'proved_zero']

    for _ in range(len(eq_list) + 1):
        eq_list = [_apply_eliminated(e, eliminated, z) for e in eq_list]
        eq_list = [e for e in eq_list if zero_record(e)['status'] != 'proved_zero']
        if not eq_list:
            break
        if len(eq_list) == 1:
            max_ord_single = max((d.derivative_count for d in eq_list[0].atoms(sp.Derivative) if d.expr in profiles), default=0)
            if max_ord_single <= 1:
                break
        progressed = False
        for idx, eq in enumerate(eq_list):
            core = _strip_nonderiv_factors(eq, profiles)
            found = None
            used_mu = sp.S.One
            for mu in (sp.S.One, z, 1 / z, z**2):
                fc = multi_flux_check(sp.together(mu * core), profiles, z)
                if fc['status'] == 'verified':
                    found = fc
                    used_mu = mu
                    break
            if found is None:
                continue
            if any(zero_record(found['flux'] - _apply_eliminated(prev['flux'], eliminated, z))['status'] == 'proved_zero'
                   for prev in integrals):
                if len(eq_list) == 1:
                    max_ord = max((d.derivative_count for d in eq.atoms(sp.Derivative) if d.expr in profiles), default=0)
                    if max_ord >= 2 and integrated_ode is None:
                        integrated_ode = sp.simplify(found['flux'] - integrals[-1]['constant'])
                continue
            C_sym = sp.Symbol(f'C{const_idx}', real=True)
            const_idx += 1
            rec = {'constant': C_sym, 'flux': found['flux'], 'multiplier': used_mu, 'status': 'verified'}
            integrals.append(rec)

            if len(eq_list) > 1:
                deriv_profiles = {d.expr for d in found['flux'].atoms(sp.Derivative)}
                alg_candidates = [F for F in profiles if found['flux'].has(F) and F not in deriv_profiles]
                for F_a in alg_candidates:
                    try:
                        sol = sp.solve(found['flux'] - C_sym, F_a)
                    except NotImplementedError:
                        sol = []
                    if len(sol) == 1 and not sol[0].has(F_a):
                        eliminated[F_a] = sp.simplify(sol[0])
                        for k_prev in list(eliminated):
                            if k_prev != F_a:
                                eliminated[k_prev] = _apply_eliminated(eliminated[k_prev], {F_a: eliminated[F_a]}, z)
                        eq_list.pop(idx)
                        progressed = True
                        break
                if progressed:
                    break
            else:
                max_ord = max((d.derivative_count for d in eq.atoms(sp.Derivative) if d.expr in profiles), default=0)
                if max_ord >= 2:
                    integrated_ode = sp.simplify(found['flux'] - C_sym)
        if not progressed:
            break

    surviving_profiles = [F for F in profiles if any(e.has(F) for e in eq_list)]
    target_profile = surviving_profiles[0] if len(surviving_profiles) == 1 else None

    reconstructed = []
    for lift in lifts:
        expr_l = lift
        for k, v in eliminated.items():
            if not isinstance(k, sp.Derivative):
                # Map profile F(z) on section to F(inv) in spacetime lift
                for f_atom in list(expr_l.atoms(AppliedUndef)):
                    if f_atom.func == k.func:
                        arg = f_atom.args[0]
                        expr_l = expr_l.subs(f_atom, v.subs(z, arg))
        reconstructed.append(_fast_clean(expr_l))

    return {
        'reduced_equations': tuple(eq_list),
        'integrated_ode': integrated_ode,
        'target_profile': target_profile,
        'eliminated': eliminated,
        'first_integrals': tuple(integrals),
        'reconstructed_lifts': tuple(reconstructed),
    }


def automatic_graph(spec, X):
    j = spec.jets
    if len(j.independent) != 2:
        raise NotImplementedError('use orbit_graph for >2 independent variables')
    t, x = j.independent
    if X[0] == 0:
        if X[1] == 0:
            raise ValueError('no invariant graph')
        t, x = x, t
        base = (X[1], X[0])
    else:
        base = X[:2]
    a, b = sp.diff(base[0], t), base[0].subs(t, 0)
    c, d = sp.diff(base[1], x), base[1].subs(x, 0)
    if any(v.has(*j.independent, *j.dependent) for v in (a, b, c, d)):
        raise NotImplementedError('non-diagonal affine base flow delegates to matrix-exponential orbit_graph')
    z = sp.Symbol('z', real=True)
    t0 = sp.S.One if a != 0 and b == 0 else sp.S.Zero
    if sp.simplify(a * t0 + b) == 0:
        raise ValueError('section is not transverse')
    e = sp.log((a * t + b) / (a * t0 + b)) / a if a != 0 else (t - t0) / b
    inv = sp.exp(-c * e) * (x + d / c) - d / c if c != 0 else x - d * e
    inv = sp.simplify(sp.expand_power_base(inv))
    profiles = tuple(sp.Function('F' + str(i))(z) for i in range(len(j.dependent)))
    lifts = []
    v = sp.Symbol('orbit', real=True)
    tflow = (t0 + b / a) * sp.exp(a * v) - b / a if a != 0 else t0 + b * v
    for u, eta, F in zip(j.dependent, X[2:], profiles):
        rate = sp.diff(eta, u)
        forcing = sp.expand(eta - rate * u)
        if rate.has(*j.independent, *j.dependent) or forcing.has(*j.dependent):
            raise NotImplementedError('coupled vertical flow delegates to matrix-exponential orbit_graph')
        xflow = (inv + d / c) * sp.exp(c * v) - d / c if c != 0 else inv + d * v
        integral = sp.integrate(sp.exp(-rate * v) * forcing.subs({t: tflow, x: xflow}, simultaneous=True), (v, 0, e))
        lifts.append(sp.simplify(sp.exp(rate * e) * (F.subs(z, inv) + integral)))
    return Graph(
        z, inv, profiles, tuple(lifts), {t: t0, x: z},
        (f'{a*t+b} != 0', 'local flow chart; logarithm arguments positive when used'),
        {t: tflow, x: (z + d / c) * sp.exp(c * v) - d / c if c != 0 else z + d * v},
    )


def reduce(spec, X, section=None):
    """Deterministic reduction of a PDE system by a 1D generator or rank-(d-1) subalgebra."""
    j = spec.jets
    n = len(j.independent)
    # Allow passing a subalgebra list/tuple of generators directly
    if isinstance(X, (list, tuple)) and X and isinstance(X[0], (list, tuple)):
        if len(X) == 1 and n == 2 and section is None:
            X = X[0]
        else:
            from .multid import reduce_nd
            return reduce_nd(spec, X)

    X = tuple(map(sp.sympify, X))
    if len(X) != n + len(j.dependent):
        return ReducedODE(spec.name, 'rejected', reason='generator dimension mismatch')
    if all(v == 0 for v in X):
        return ReducedODE(spec.name, 'rejected', reason='zero generator does not define a subalgebra')
    if any(v.has(*j.dependent) for v in X[:n]):
        return ReducedODE(spec.name, 'unsupported', reason='base action is not projectable in this chart')
    if all(v == 0 for v in X[:n]):
        return ReducedODE(spec.name, 'no invariant graph',
                          reason='vertical generator has zero base projection; no quotient to fewer independent variables')

    if n != 2 and section is None:
        from .multid import reduce_nd
        return reduce_nd(spec, (X,))

    try:
        graph = section or automatic_graph(spec, X)
    except NotImplementedError:
        from .multid import reduce_nd
        return reduce_nd(spec, (X,))
    except ValueError as exc:
        return ReducedODE(spec.name, 'rejected', str(exc))

    if sp.simplify(graph.invariant.subs(graph.section, simultaneous=True) - graph.z) != 0:
        return ReducedODE(spec.name, 'rejected', reason='section does not invert the quotient coordinate')
    if any(sp.simplify(lift.subs(graph.section, simultaneous=True) - F) != 0
           for lift, F in zip(graph.lifts, graph.profiles)):
        return ReducedODE(spec.name, 'rejected', reason='section does not recover arbitrary profile data')

    section_curve = sp.Matrix([graph.section.get(x, x) for x in j.independent])
    transverse = sp.Matrix.hstack(sp.Matrix(X[:2]).subs(graph.section, simultaneous=True),
                                  section_curve.diff(graph.z)).det()
    transverse_record = nonzero_record(transverse, spec.positive)
    if transverse_record['status'] == 'zero':
        return ReducedODE(spec.name, 'rejected', reason='section is tangent to the orbit')

    shell, _ = spec.shell()
    if any(zero_record(j.act(eq, X).subs(shell, simultaneous=True))['status'] != 'proved_zero'
           for eq in spec.equations):
        return ReducedODE(spec.name, 'rejected', reason='generator fails full on-shell symmetry identity')

    mapping = dict(zip(j.dependent, graph.lifts))
    defects = tuple(sp.simplify(eta.subs(mapping, simultaneous=True) - sum(
        xi.subs(mapping, simultaneous=True) * sp.diff(lift, x) for xi, x in zip(X[:n], j.independent)))
        for eta, lift in zip(X[n:], graph.lifts))
    invariant_defect = sp.simplify(sum(v * sp.diff(graph.invariant, x) for v, x in zip(X[:n], j.independent)))
    if any(v != 0 for v in defects) or invariant_defect != 0:
        return ReducedODE(spec.name, 'rejected', reason='invariant surface or invariant coordinate identity fails')

    jet_map = j.pullback(graph.lifts)
    positive = tuple(sp.simplify(v.xreplace(jet_map)) for v in spec.positive)
    if any(v.is_nonpositive is True for v in positive):
        return ReducedODE(spec.name, 'chart-incompatible',
                          reason='a declared strictly positive quantity is identically nonpositive on this graph',
                          graph=graph)

    pulled = tuple(_clean_power_pullback(eq.xreplace(jet_map)) for eq in spec.equations)
    equations = tuple(_clean_power_pullback(v.subs(graph.section, simultaneous=True).doit()) for v in pulled)
    weights, weight_evidence = [], []
    for raw, red in zip(pulled, equations):
        if graph.orbit_coordinates:
            raw_orb = _clean_power_pullback(raw.subs(graph.orbit_coordinates, simultaneous=True).doit())
            lifted = red
        else:
            raw_orb = raw
            lifted = _clean_power_pullback(red.subs(graph.z, graph.invariant).doit())
        if zero_record(red)['status'] == 'proved_zero' and zero_record(raw_orb)['status'] != 'proved_zero':
            return ReducedODE(spec.name, 'rejected', reason='zero section equation does not extend off section')
        ratio = sp.powsimp(sp.cancel(sp.powsimp(raw_orb / lifted))) if zero_record(red)['status'] != 'proved_zero' else sp.S.One
        if ratio.has(*j.dependent) or ratio.atoms(AppliedUndef) or ratio.atoms(sp.Derivative):
            from .multid import reduce_nd
            return reduce_nd(spec, (X,))
        if zero_record(raw_orb - ratio * lifted)['status'] != 'proved_zero':
            return ReducedODE(spec.name, 'rejected', reason='pullback weight identity fails')
        ev = nonzero_record(ratio, spec.positive)
        if ev['status'] == 'zero':
            return ReducedODE(spec.name, 'rejected', reason='zero pullback weight destroys reverse implication')
        weight_evidence.append(ev)
        weights.append(ratio)

    elim = integrate_and_eliminate(equations, graph.profiles, graph.z, spec.positive, graph.lifts)
    preserved = tuple(sorted(
        {s for eq in (*equations, *elim['reduced_equations']) for s in eq.free_symbols if s != graph.z},
        key=sp.default_sort_key,
    ))
    leading = []
    for eq in elim['reduced_equations']:
        derivatives = eq.atoms(sp.Derivative)
        order = max((d.derivative_count for d in derivatives), default=0)
        leading.append({str(d): sp.simplify(eq.diff(d)) for d in derivatives if d.derivative_count == order})

    return ReducedODE(
        spec.name, 'verified',
        graph=graph,
        equations=equations,
        reduced_equations=elim['reduced_equations'],
        integrated_ode=elim['integrated_ode'],
        target_profile=elim['target_profile'],
        eliminated=elim['eliminated'],
        reconstructed_lifts=elim['reconstructed_lifts'],
        weights=tuple(weights),
        first_integrals=elim['first_integrals'],
        leading_coefficients=tuple(leading),
        preserved_parameters=preserved,
        conditions=spec.conditions + graph.conditions + tuple(str(v) + ' > 0' for v in positive),
        checks={
            'on_shell': True,
            'invariant_surface': True,
            'pullback': True,
            'base_orbit_rank': 1,
            'transversality': transverse_record,
            'weight_nonvanishing': weight_evidence,
            'section_inverse': True,
        },
    )
