"""PDE->ODE quotient for n independent variables by a rank n-1 subalgebra of affine point fields.

Jets are computed on the complete JetSpace via the inverse Jacobian of the matrix-exponential
orbit chart (z, v) -> x, verified via Q_X[U] = 0 and Delta(z, v) = M(z, v) E(z) with det M != 0,
followed by deterministic multi-profile first-integral elimination preserving all parameters.
"""
from dataclasses import dataclass, field
from itertools import product
import sympy as sp
from sympy.core.function import AppliedUndef

from .algebra import closed
from .identities import nonzero_record, zero_record
from .reduce import ReducedODE, integrate_and_eliminate


@dataclass
class OrbitGraph:
    z: sp.Symbol
    orbit: tuple
    base: tuple
    profiles: tuple
    lifts: tuple
    section: dict
    jacobian: sp.Expr
    conditions: tuple = ()
    invariant: object = None
    orbit_coordinates: dict = field(default_factory=dict)


def affine(X, coords):
    X = sp.Matrix(X)
    A = X.jacobian(coords)
    b = X.subs(dict.fromkeys(coords, 0), simultaneous=True)
    if any(v.has(*coords) for v in (*A, *b)):
        raise NotImplementedError('field is not affine in (x, u)')
    return A, b


def flow(X, coords, v):
    """exp(v X) on (y, 1) for an affine field."""
    A, b = affine(X, coords)
    N = len(coords)
    M = sp.zeros(N + 1, N + 1)
    M[:N, :N], M[:N, N] = A, b
    E = (v * M).exp()
    return E.applyfunc(lambda e: sp.simplify(e.rewrite(sp.cos)) if e.has(sp.I) else sp.simplify(e))


def _section(base, n, z):
    for ones in range(n + 1):
        for x0 in product((0, 1), repeat=n):
            if sum(x0) != ones:
                continue
            for axis in range(n):
                point = [sp.Integer(c) for c in x0]
                point[axis] = z
                rows = [[sp.sympify(c).subs(dict(zip(base[0][1], point)), simultaneous=True) for c in X]
                        for X, _ in base]
                det = sp.simplify(sp.Matrix(rows + [[int(k == axis) for k in range(n)]]).det())
                if det != 0:
                    return point, axis, det
    raise ValueError('no transverse coordinate section found')


def orbit_graph(spec, fields):
    j = spec.jets
    n, coords = len(j.independent), j.independent + j.dependent
    k = len(fields)
    z = sp.Symbol('z', real=True)
    v = sp.symbols(f'v1:{k+1}', real=True)
    base = [(X[:n], j.independent) for X in fields]
    point, axis, _ = _section(base, n, z)
    profiles = tuple(sp.Function(f'F{i}')(z) for i in range(len(j.dependent)))
    state = sp.Matrix([*point, *profiles, 1])
    for X, s in reversed(list(zip(fields, v))):
        state = flow(X, coords, s) * state
    state = state.applyfunc(sp.simplify)
    xs, us = tuple(state[:n]), tuple(state[n:n + len(j.dependent)])
    orbit = (z, *v)
    J = sp.Matrix(xs).jacobian(orbit)
    detJ = sp.simplify(J.det())
    return OrbitGraph(
        z, orbit, xs, profiles, us,
        {x: p for x, p in zip(j.independent, point)},
        detJ,
        (f'section {dict(zip(map(str, j.independent), map(str, point)))} along {j.independent[axis]}',
         f'orbit chart det {detJ} != 0'),
        orbit_coordinates=dict(zip(j.independent, xs)),
    )


def _jets(spec, graph):
    j = spec.jets
    Jinv = sp.Matrix(graph.base).jacobian(graph.orbit).inv().applyfunc(sp.simplify)
    D = lambda e, i: sp.simplify(sum(Jinv[c, i] * sp.diff(e, w) for c, w in enumerate(graph.orbit)))
    out = {}
    for (a, idx), sym in j.jets.items():
        if not any(idx):
            out[sym] = graph.lifts[a]
            continue
        i = next(q for q, s in enumerate(idx) if s)
        prev = tuple(s - int(q == i) for q, s in enumerate(idx))
        out[sym] = D(out[j.jets[a, prev]], i)
    return out, D


def _profile_symbols(exprs, profiles):
    atoms = set()
    for e in exprs:
        atoms |= {d for d in e.atoms(sp.Derivative) if d.expr in profiles}
        atoms |= {f for f in e.atoms(AppliedUndef) if f in profiles}
        atoms |= {pw for pw in e.atoms(sp.Pow)
                  if not pw.exp.is_Integer and any(pw.base.has(p) for p in profiles)}
    ordered = sorted(atoms, key=lambda d: (-len(str(d)), sp.default_sort_key(d)))
    return {d: sp.Dummy('J') for d in ordered}


def weight_matrix(raw, odes, profiles):
    """Find M(z, v), free of the profile, with raw = M * odes."""
    m = len(raw)
    M = sp.zeros(m, m)
    coupled_rows = []
    for a, (r, e) in enumerate(zip(raw, odes)):
        if zero_record(e)['status'] != 'proved_zero':
            if zero_record(r - e)['status'] == 'proved_zero':
                M[a, a] = sp.S.One
                continue
            ratio = sp.trigsimp(sp.powsimp(sp.cancel(sp.powsimp(r / e))))
            if not ratio.atoms(AppliedUndef) and not ratio.atoms(sp.Derivative):
                M[a, a] = ratio
                continue
        coupled_rows.append(a)
    if not coupled_rows:
        return M, 'diagonal'

    from .hidden import normalize_powers
    for a in coupled_rows:
        # Candidate columns b: exclude odes[b] introducing symbolic powers absent from raw[a]
        raw_pows = {p.exp for p in raw[a].atoms(sp.Pow) if not p.exp.is_Integer}
        cand_cols = [
            b for b in range(m)
            if {p.exp for p in odes[b].atoms(sp.Pow) if not p.exp.is_Integer} <= raw_pows
        ] or list(range(m))
        w_syms = [sp.Symbol(f'w_{a}_{b}') for b in cand_cols]
        store, roots, seen = {}, {}, {}
        diff_expr = raw[a] - sum(w * odes[b] for w, b in zip(w_syms, cand_cols))
        num, _, _, _ = normalize_powers(diff_expr, None, store, roots, seen)
        rep = _profile_symbols((num,), profiles)
        extra_syms = [
            s for s in (*store.values(), *roots.values())
            if any(b_expr.has(p) for (b_expr, _), sym in (*store.items(), *roots.items()) if sym == s for p in profiles)
        ]
        num_rep = sp.expand(num.xreplace(rep))
        gens = (*rep.values(), *extra_syms)
        rows = sp.Poly(num_rep, *gens).coeffs() if gens else [num_rep]
        sol = sp.solve(rows, w_syms, dict=True)
        if not sol:
            raise ArithmeticError('pullback is not a profile-free combination of the section equations')
        for w, b in zip(w_syms, cand_cols):
            M[a, b] = sp.simplify(sol[0].get(w, sp.S.Zero).subs({u: 0 for u in w_syms}))
    return M, 'matrix'


def reduce_nd(spec, fields, verify_symmetry=True):
    j = spec.jets
    n, coords = len(j.independent), j.independent + j.dependent
    fields = [tuple(map(sp.sympify, X)) for X in fields]
    if len(fields) != n - 1:
        return ReducedODE(spec.name, 'rejected', reason=f'need {n-1} generators for an ODE quotient')
    if any(c.has(*j.dependent) for X in fields for c in X[:n]):
        return ReducedODE(spec.name, 'unsupported', reason='base action is not projectable')
    if sp.Matrix([X[:n] for X in fields]).rank() != n - 1:
        return ReducedODE(spec.name, 'rejected', reason='generic base orbit rank is not n-1')
    if not closed(fields, coords):
        return ReducedODE(spec.name, 'rejected', reason='generators do not span a Lie subalgebra')
    if verify_symmetry:
        shell, _ = spec.shell()
        for X in fields:
            if any(zero_record(j.act(eq, X).subs(shell, simultaneous=True))['status'] != 'proved_zero'
                   for eq in spec.equations):
                return ReducedODE(spec.name, 'rejected', reason='generator fails on-shell symmetry identity')
    try:
        graph = orbit_graph(spec, fields)
    except (NotImplementedError, ValueError) as exc:
        return ReducedODE(spec.name, 'unsupported', reason=str(exc))
    chart = nonzero_record(graph.jacobian, spec.positive)
    if chart['status'] == 'zero':
        return ReducedODE(spec.name, 'rejected', reason='orbit chart is degenerate')
    jets, _ = _jets(spec, graph)
    base_map = dict(zip(j.independent, graph.base))
    for X in fields:
        sub = {**base_map, **dict(zip(j.dependent, graph.lifts))}
        for a in range(len(j.dependent)):
            q = X[n + a].xreplace(sub) - sum(
                X[i].xreplace(sub) * jets[j.jets[a, tuple(int(q_i == i) for q_i in range(n))]]
                for i in range(n)
            )
            if zero_record(q)['status'] != 'proved_zero':
                return ReducedODE(spec.name, 'rejected', reason='invariant-surface condition Q_X = 0 fails')
    def _norm_orbit_expr(expr):
        expr = expr.replace(
            lambda e: e.is_Pow and not e.exp.is_Integer,
            lambda e: sp.trigsimp(sp.expand(e.base))**e.exp,
        )
        expr = sp.expand_power_base(expr, force=True)
        return sp.trigsimp(sp.powsimp(sp.expand(expr)))

    mapping = {**jets, **base_map}
    zero = dict.fromkeys(graph.orbit[1:], 0)
    raw = tuple(_norm_orbit_expr(eq.xreplace(mapping)) for eq in spec.equations)
    odes = tuple(_norm_orbit_expr(eq.xreplace(mapping).subs(zero)) for eq in spec.equations)
    try:
        M, kind = weight_matrix(raw, odes, graph.profiles)
    except (ArithmeticError, sp.PolynomialError) as exc:
        return ReducedODE(spec.name, 'unsupported', reason=str(exc))
    residual = sp.Matrix(raw) - M * sp.Matrix(odes)
    if any(zero_record(v)['status'] != 'proved_zero' for v in residual):
        return ReducedODE(spec.name, 'rejected', reason='weight identity fails')
    det = nonzero_record(sp.simplify(M.det()), spec.positive)
    if det['status'] == 'zero':
        return ReducedODE(spec.name, 'rejected', reason='singular weight matrix loses the reverse implication')

    elim = integrate_and_eliminate(odes, graph.profiles, graph.z, spec.positive, graph.lifts)
    preserved = tuple(sorted(
        {s for eq in (*odes, *elim['reduced_equations']) for s in eq.free_symbols if s != graph.z},
        key=sp.default_sort_key,
    ))

    return ReducedODE(
        spec.name, 'verified',
        graph=graph,
        equations=odes,
        reduced_equations=elim['reduced_equations'],
        integrated_ode=elim['integrated_ode'],
        target_profile=elim['target_profile'],
        eliminated=elim['eliminated'],
        reconstructed_lifts=elim['reconstructed_lifts'],
        weights=tuple(M) if kind == 'matrix' else tuple(M.diagonal()),
        first_integrals=elim['first_integrals'],
        preserved_parameters=preserved,
        conditions=spec.conditions + graph.conditions,
        checks={
            'base_orbit_rank': n - 1,
            'subalgebra': True,
            'on_shell': verify_symmetry,
            'invariant_surface': True,
            'chart_jacobian': chart,
            'weight_kind': kind,
            'weight_determinant': det,
            'pullback_identity': 'Delta(z,v) = M(z,v) E(z) exactly',
        },
        scope='local orbit chart of a rank n-1 affine subalgebra',
    )
