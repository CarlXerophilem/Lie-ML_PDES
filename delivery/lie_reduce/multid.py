"""PDE->ODE quotient for n independent variables by a rank n-1 subalgebra of affine point fields.

The ansatz is the orbit of a profile graph on a section line under the product of
flows, x = x(z, v), u = U(z, v). Jets are obtained by the chain rule through the
inverse Jacobian of (z, v) -> x, so the invariant z(x) is never inverted. The
reduction is accepted only after the identities

    Q_X[U] = 0 for every generator,      Delta(z, v) = M(z, v) E(z),

with M free of the profile and det M not identically zero, are proved exactly.
"""
from dataclasses import dataclass, field
from itertools import product
import sympy as sp
from sympy.core.function import AppliedUndef
from .algebra import bracket, coordinates_in_basis
from .identities import nonzero_record
from .reduce import ReducedODE


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
        raise NotImplementedError('field is not affine in (x, u); supply a section graph')
    return A, b


def flow(X, coords, v):
    """exp(v X) on (y, 1) for an affine field."""
    A, b = affine(X, coords)
    N = len(coords)
    M = sp.zeros(N + 1, N + 1)
    M[:N, :N], M[:N, N] = A, b
    E = (v*M).exp()
    return E.applyfunc(lambda e: sp.simplify(e.rewrite(sp.cos)) if e.has(sp.I) else sp.simplify(e))


def closed(fields, coords):
    if len(fields) < 2:
        return True
    for i, X in enumerate(fields):
        for Y in fields[i+1:]:
            Z = bracket(X, Y, coords)
            if all(sp.expand(v) == 0 for v in Z):
                continue
            try:
                c = coordinates_in_basis(Z, fields, coords)
            except (ValueError, sp.PolynomialError):
                return False
            if any(sp.sympify(k).has(*coords) for k in c):
                return False
    return True


def _section(base, n, z):
    for ones in range(n + 1):
        for x0 in product((0, 1), repeat=n):
            if sum(x0) != ones:
                continue
            for axis in range(n):
                point = [sp.Integer(c) for c in x0]
                point[axis] = z
                rows = [[sp.sympify(c).subs(dict(zip(base[0][1], point)), simultaneous=True) for c in X] for X, _ in base]
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
    point, axis, det = _section(base, n, z)
    profiles = tuple(sp.Function(f'F{i}')(z) for i in range(len(j.dependent)))
    state = sp.Matrix([*point, *profiles, 1])
    for X, s in reversed(list(zip(fields, v))):
        state = flow(X, coords, s)*state
    state = state.applyfunc(sp.simplify)
    xs, us = tuple(state[:n]), tuple(state[n:n+len(j.dependent)])
    orbit = (z, *v)
    J = sp.Matrix(xs).jacobian(orbit)
    detJ = sp.simplify(J.det())
    return OrbitGraph(z, orbit, xs, profiles, us, {x: p for x, p in zip(j.independent, point)}, detJ,
                      (f'section {dict(zip(map(str, j.independent), map(str, point)))} along {j.independent[axis]}',
                       f'orbit chart det {detJ} != 0'),
                      orbit_coordinates=dict(zip(j.independent, xs)))


def _jets(spec, graph):
    j = spec.jets
    n = len(j.independent)
    Jinv = sp.Matrix(graph.base).jacobian(graph.orbit).inv().applyfunc(sp.simplify)
    D = lambda e, i: sp.simplify(sum(Jinv[c, i]*sp.diff(e, w) for c, w in enumerate(graph.orbit)))
    out = {}
    for (a, idx), sym in j.jets.items():
        if not any(idx):
            out[sym] = graph.lifts[a]
            continue
        i = next(q for q, s in enumerate(idx) if s)
        prev = tuple(s - int(q == i) for q, s in enumerate(idx))
        out[sym] = D(out[j.jets[a, prev]], i)
    return out, D


def _profile_symbols(exprs, profiles, z):
    atoms = set()
    for e in exprs:
        atoms |= {d for d in e.atoms(sp.Derivative) if d.expr in profiles}
        atoms |= {f for f in e.atoms(AppliedUndef) if f in profiles}
    atoms = sorted(atoms, key=lambda d: (-getattr(d, 'derivative_count', 0), sp.default_sort_key(d)))
    return {d: sp.Dummy('J') for d in atoms}


def weight_matrix(raw, odes, profiles, z):
    """Find M(z, v), free of the profile, with raw = M odes."""
    m = len(raw)
    scalar = []
    for r, e in zip(raw, odes):
        if e == 0:
            scalar = None
            break
        ratio = sp.simplify(r/e)
        if ratio.atoms(AppliedUndef) or ratio.atoms(sp.Derivative):
            scalar = None
            break
        scalar.append(ratio)
    if scalar is not None:
        return sp.diag(*scalar), 'diagonal'
    W = sp.Matrix(m, m, lambda a, b: sp.Symbol(f'w_{a}_{b}'))
    rep = _profile_symbols((*raw, *odes), profiles, z)
    rows = []
    for a in range(m):
        num = sp.numer(sp.together(sp.expand(raw[a] - sum(W[a, b]*odes[b] for b in range(m))).xreplace(rep)))
        rows.extend(sp.Poly(sp.expand(num), *rep.values()).coeffs())
    sol = sp.solve(rows, list(W), dict=True)
    if not sol:
        raise ArithmeticError('pullback is not a profile-free combination of the section equations')
    M = W.subs(sol[0]).subs({w: 0 for w in W}).applyfunc(sp.simplify)
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
            if any(sp.simplify(j.act(eq, X).subs(shell, simultaneous=True)) != 0 for eq in spec.equations):
                return ReducedODE(spec.name, 'rejected', reason='generator fails on-shell symmetry identity')
    try:
        graph = orbit_graph(spec, fields)
    except (NotImplementedError, ValueError) as exc:
        return ReducedODE(spec.name, 'unsupported', reason=str(exc))
    chart = nonzero_record(graph.jacobian, spec.positive)
    if chart['status'] == 'zero':
        return ReducedODE(spec.name, 'rejected', reason='orbit chart is degenerate')
    jets, D = _jets(spec, graph)
    base_map = dict(zip(j.independent, graph.base))
    for X in fields:
        sub = {**base_map, **dict(zip(j.dependent, graph.lifts))}
        for a in range(len(j.dependent)):
            q = X[n+a].xreplace(sub) - sum(X[i].xreplace(sub)*jets[j.jets[a, tuple(int(q == i) for q in range(n))]]
                                           for i in range(n))
            if sp.simplify(q) != 0:
                return ReducedODE(spec.name, 'rejected', reason='invariant-surface condition Q_X = 0 fails')
    mapping = {**jets, **base_map}
    raw = tuple(sp.simplify(eq.xreplace(mapping)) for eq in spec.equations)
    zero = dict.fromkeys(graph.orbit[1:], 0)
    odes = tuple(sp.factor(sp.simplify(r.subs(zero))) for r in raw)
    try:
        M, kind = weight_matrix(raw, odes, graph.profiles, graph.z)
    except (ArithmeticError, sp.PolynomialError) as exc:
        return ReducedODE(spec.name, 'unsupported', reason=str(exc))
    residual = (sp.Matrix(raw) - M*sp.Matrix(odes)).applyfunc(sp.simplify)
    if any(v != 0 for v in residual):
        return ReducedODE(spec.name, 'rejected', reason='weight identity fails')
    det = nonzero_record(sp.simplify(M.det()), spec.positive)
    if det['status'] == 'zero':
        return ReducedODE(spec.name, 'rejected', reason='singular weight matrix loses the reverse implication')
    return ReducedODE(spec.name, 'verified', graph=graph, equations=odes,
                      weights=tuple(M) if kind == 'matrix' else tuple(M.diagonal()),
                      conditions=spec.conditions + graph.conditions,
                      checks={'base_orbit_rank': n - 1, 'subalgebra': True, 'on_shell': verify_symmetry,
                              'invariant_surface': True, 'chart_jacobian': chart, 'weight_kind': kind,
                              'weight_determinant': det, 'pullback_identity': 'Delta(z,v) = M(z,v) E(z) exactly'},
                      scope='local orbit chart of a rank n-1 affine subalgebra')
