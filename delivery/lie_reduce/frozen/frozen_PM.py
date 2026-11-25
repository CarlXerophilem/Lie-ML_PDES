"""Discover scalar point generators on the frozen positive chart of P and M."""
import json
from itertools import combinations

from reproduce_sve2026 import (
    act, master, total, t, s, u, p, q, a, b, c, r, w, x, y, g, kappa, m,
    JETS, z, F, P, C, H, profile_total, sp,
)


def compatible(exponent=m):
    return sp.expand(master(exponent) - total(p*(q*a-g*c/q**2)/q, 1))


def _require(condition, stage):
    if not condition:
        raise ArithmeticError(stage)


def _normal_form(equation):
    leading = equation.diff(r)
    _require(leading.is_positive and not leading.has(r), "regular third-jet chart")
    return -equation.xreplace({r: sp.S.Zero})/leading


def _on_shell(equation, field):
    return act(equation, *field).xreplace({r: _normal_form(equation)})


def _coefficients(expr, *jets):
    return sp.Poly(sp.expand(expr), *jets).coeffs()


def _zero_solution(rows, unknowns, stage):
    """Solve an exact finite linear split and require that its kernel is zero."""
    matrix, rhs = sp.linear_eq_to_matrix(rows, unknowns)
    _require(rhs.is_zero_matrix and matrix.rank() == len(unknowns), stage)
    return dict.fromkeys(unknowns, sp.S.Zero)


def _positive_unit(expr):
    """Clear a positive multiplier on p,q,g,kappa>0, m>=1."""
    pos_m = sp.Dummy("positive_m", positive=True)
    _require(sp.factor(expr.subs(m, pos_m)).is_positive is True,
             "positive multiplier on the frozen chart")
    return expr


def material_slice(equation, field):
    """Evaluate the arbitrary prolongation at a=b=c=0 after solving for r."""
    zero_second = dict.fromkeys((a, b, c), sp.S.Zero)
    return _on_shell(equation, field).xreplace(zero_second)


def _material_rows(tau, xi, eta):
    """Derive the dependencies, then return equations for the affine slopes."""
    equation = compatible()
    tangent = material_slice(equation, (tau, xi, eta))
    dw = sp.Poly(sp.expand(q**4*tangent.diff(w)), q)

    projected = (xi.diff(t), xi.diff(u), tau.diff(s))
    rows = _coefficients(dw.nth(5), p) + _coefficients(dw.nth(2), p)
    substitutions = _zero_solution(rows, projected, "M: projected dependencies")

    vertical = (eta.diff(s), tau.diff(u))
    rows = _coefficients(dw.nth(3).xreplace(substitutions), p)
    substitutions.update(_zero_solution(rows, vertical, "M: remaining spatial derivatives"))
    rows = _coefficients(dw.nth(4).xreplace(substitutions), p)
    substitutions.update(_zero_solution(rows, (eta.diff(t),), "M: vertical time derivative"))
    _require(sp.expand(dw.as_expr().xreplace(substitutions)) == 0,
             "M: complete w coefficient")

    # These one-variable dependencies follow from the preceding exact splits.
    tau, xi, eta = sp.Function("tau")(t), sp.Function("xi")(s), sp.Function("eta")(u)
    tangent = material_slice(equation, (tau, xi, eta))
    dx = sp.Poly(sp.expand(q**4*tangent.diff(x)), q)
    _require(set(dx.monoms()) == {(2,), (3,)}, "M: x coefficient support")
    first = sp.cancel(dx.nth(2)/g)
    second = sp.expand(dx.nth(3)/_positive_unit(g*kappa*m*p**(m-1)))
    slopes = (tau.diff(t), xi.diff(s), eta.diff(u))
    curvature = (tau.diff(t, 2), xi.diff(s, 2), eta.diff(u, 2))
    _zero_solution([first.diff(v) for v in (t, s, u)], curvature,
                   "M: one-variable derivatives are constant")
    receipt = {
        "w_slice": str(dw.as_expr()),
        "zero_first_derivatives": list(map(str, substitutions)),
        "x_slice_after_dependency_split": str(dx.as_expr()),
    }
    return (first, second), slopes, receipt


def _printed_rows(tau, xi, eta):
    """Derive the dependencies for P, leaving the time shift free initially."""
    equation = master()
    tangent = _on_shell(equation, (tau, xi, eta))
    candidates = (xi.diff(t), xi.diff(u))
    coeff = tangent.diff(y)
    normalized = sp.cancel(coeff/_positive_unit(coeff.diff(candidates[0])))
    _zero_solution(_coefficients(normalized, p, q), candidates, "P: xi depends on s")
    receipt = {"free_y_normalized": str(normalized)}

    xi = sp.Function("xi")(s)
    tangent = _on_shell(equation, (tau, xi, eta))
    candidates = (tau.diff(s), tau.diff(u))
    coeff = tangent.diff(w)
    normalized = sp.cancel(coeff/_positive_unit(coeff.diff(candidates[0])))
    _zero_solution(_coefficients(normalized, p, q), candidates, "P: tau depends on t")
    receipt["free_w_after_xi_split"] = str(normalized)

    tau = sp.Function("tau")(t)
    tangent = _on_shell(equation, (tau, xi, eta))
    row = sp.expand(q*tangent.diff(a, b))
    _zero_solution([row], (eta.diff(s),), "P: eta depends on t and phi")
    receipt["free_ab_after_base_split"] = str(row)

    eta = sp.Function("eta")(t, u)
    tangent = _on_shell(equation, (tau, xi, eta))
    da = sp.Poly(sp.expand(tangent.diff(a)/q), p)
    _require(da.degree() == 1, "P: free p coefficient")
    _zero_solution([da.nth(1)], (eta.diff(u, 2),), "P: eta affine in phi")
    receipt["free_a_after_eta_s_split"] = str(da.as_expr())

    A, B = sp.Function("A")(t), sp.Function("B")(t)
    tangent = _on_shell(equation, (tau, xi, A*u+B))
    dx = sp.Poly(sp.expand(q**2*tangent.diff(x)), q)
    _require(set(dx.monoms()) == {(0,), (1,)}, "P: x coefficient support")
    first = sp.cancel(dx.nth(0)/g)
    second = sp.expand(dx.nth(1)/_positive_unit(g*kappa*m*p**(m-2)))
    curvature = (tau.diff(t, 2), xi.diff(s, 2), A.diff(t))
    dt = da.nth(0).subs(eta, A*u+B).doit()
    constants = _zero_solution([first.diff(t), first.diff(s), dt], curvature,
                               "P: independent slopes are constant")
    receipt["free_x_after_eta_affine"] = str(dx.as_expr())
    return [first, *_coefficients(second.xreplace(constants), p)], (
        tau.diff(t), xi.diff(s), A, B.diff(t),
    ), receipt


def _rank_strata(matrix):
    """Find the rank-drop locus by the gcd of the generic maximal minors."""
    _require(matrix.free_symbols <= {m}, "only the frozen exponent may vary")
    rank = matrix.rank()
    _require(rank > 0, "nontrivial determining matrix")
    minors = [matrix.extract(i, j).det()
              for i in combinations(range(matrix.rows), rank)
              for j in combinations(range(matrix.cols), rank)]
    divisor = sp.gcd_list(minors, m)
    roots = sp.solveset(divisor, m, domain=sp.Interval(1, sp.oo))
    _require(roots is sp.S.EmptySet or isinstance(roots, sp.FiniteSet),
             "finite rank strata on m>=1")
    for root in roots:
        _require(matrix.subs(m, root).rank() < rank, "exceptional rank certificate")
    return roots


def _printed_time_shift(equation, kernel):
    """When B'(t) is free, derive B''(t)=0 before using an affine generator."""
    B = sp.Function("B")(t)
    spatial = [v[:3] for v in kernel if v[3] == 0]
    time_shifts = [v for v in kernel if v[3] != 0]
    _require(len(time_shifts) == 1 and all(v == 0 for v in time_shifts[0][:3]),
             "P: split free field time shift from the other slopes")
    weights = sp.symbols(f"scale:{len(spatial)}")
    T, S, U = (sum(weight*row[j] for weight, row in zip(weights, spatial))
               for j in range(3))
    tangent = _on_shell(equation, (T*t, S*s, U*u+B))
    free_second = dict.fromkeys((a, b, c, w, x, y), sp.S.Zero)
    row = tangent.diff(b).xreplace(free_second)
    _zero_solution([sp.factor(row)], (B.diff(t, 2),), "P: time shift is affine")


def classify(model):
    """Run the frozen sequence from arbitrary smooth fields to a checked basis."""
    field = tuple(sp.Function(name)(t, s, u) for name in ("tau", "xi", "eta"))
    if model == "P":
        equation = master()
        rows, unknowns, receipt = _printed_rows(*field)
    elif model == "M":
        equation = compatible()
        rows, unknowns, receipt = _material_rows(*field)
    else:
        raise ValueError("model must be 'P' or 'M'")
    matrix, rhs = sp.linear_eq_to_matrix(rows, unknowns)
    _require(rhs.is_zero_matrix, "homogeneous affine determining equations")
    roots = _rank_strata(matrix)
    strata = {}
    translations = [tuple(row) for row in sp.eye(3).tolist()]
    for exponent in (m, *sorted(roots)):
        specialized = matrix.subs(m, exponent)
        on_branch = equation.subs(m, exponent)
        kernel = specialized.nullspace()
        if exponent == m:
            for generator in kernel:
                for value in generator:
                    denominator = sp.cancel(value).as_numer_denom()[1]
                    poles = sp.solveset(denominator, m, domain=sp.Interval(1, sp.oo))
                    _require(poles.is_subset(roots), "generic basis on all regular strata")
        if model == "P" and any(v[3] != 0 for v in kernel):
            _printed_time_shift(on_branch, kernel)
        basis = translations + [
            (sp.cancel(v[0])*t, sp.cancel(v[1])*s,
             sp.cancel(v[2])*u + (sp.cancel(v[3])*t if model == "P" else 0))
            for v in kernel
        ]
        for generator in basis:
            _require(sp.simplify(_on_shell(on_branch, generator)) == 0,
                     f"{model}: full unsliced prolongation at m={exponent}")
        strata[str(exponent)] = basis
    return {
        "exceptional_exponents": tuple(sorted(roots)),
        "affine_coordinates": tuple(map(str, unknowns)),
        "affine_matrix": matrix,
        "determining_splits": receipt,
        "bases": strata,
    }


def material_scaling(generator):
    """Use a verified generator, then extract the undivided first integral."""
    T = sp.Symbol("T", positive=True)
    profile = sp.Function("profile")
    graph = T*profile(s/T)
    tau, xi, eta = [v.subs({t: T, u: graph}, simultaneous=True) for v in generator]
    _require(sp.simplify(eta-tau*graph.diff(T)-xi*graph.diff(s)) == 0,
             "scaling graph satisfies the invariant-surface condition")
    substitutions = {sp.diff(profile(z), z, n): value
                     for n, value in enumerate((F, P, C, H))}
    jets = {v: sp.diff(graph, T, i, s, j).subs(s, z*T).doit().xreplace(substitutions)
            for (i, j), v in JETS.items()}
    pulled = T**2*compatible().xreplace(jets)
    leading = sp.diff(pulled, H)
    velocity = sp.Symbol("V", positive=True)
    hydro = sp.factor(leading.subs(kappa, 0))
    transport = sp.factor((leading-hydro).subs(F, velocity+z*P))
    _require(not (hydro+transport).has(T), "material scaling reduces the leading coefficient")
    flux = (hydro+transport.subs(velocity, F-z*P))*C
    difference = (pulled-profile_total(flux)).subs(F, velocity+z*P)
    _require(sp.factor(sp.expand(difference)) == 0, "full material first integral")
    return {"velocity": str(F-z*P), "bindings": {"V": str(F-z*P)}, "leading": str(hydro+transport),
            "first_integral": str(C*(hydro+transport))}


def run():
    models = {model: classify(model) for model in ("P", "M")}
    material_generator, = models["M"]["bases"]["m"][3:]
    return {
        "scope": "Local smooth point generators on p,q,g,kappa>0; real m>=1",
        "coordinates": ["t", "s", "phi"],
        "models": {
            name: {
                "exceptional_exponents": list(map(str, result["exceptional_exponents"])),
                "affine_coordinates": result["affine_coordinates"],
                "affine_matrix": [list(map(str, row)) for row in result["affine_matrix"].tolist()],
                "determining_splits": result["determining_splits"],
                "bases": {exponent: [list(map(str, v)) for v in basis]
                          for exponent, basis in result["bases"].items()},
            }
            for name, result in models.items()
        },
        "material_scaling": material_scaling(material_generator),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
