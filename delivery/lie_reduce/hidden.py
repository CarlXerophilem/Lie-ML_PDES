"""Parameter strata of the degree-d determining system.

The general generator X has unknown polynomial coefficients of degree <= d. Its
prolonged action on the shell is split in the free jets; a symbolic exponent m is
split generically, b**(a*m + k) -> W_b**a * b**k. The determining matrix then has
entries polynomial in the parameters, and its kernel dimension jumps only on the
zero set of the pivot minor or where two split monomials of the same jet coincide
(the resonances). Every candidate is decided by exact specialization.
"""
from itertools import combinations
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from .spec import PDESpec


def _split(expr, parameter, store):
    def rule(e):
        base, ex = e.as_base_exp()
        poly = sp.Poly(sp.expand(ex), parameter)
        if poly.degree() != 1:
            raise ValueError(f'exponent {ex} is not affine in {parameter}')
        a, k = poly.all_coeffs()
        if not (a.is_Integer and a > 0):
            raise ValueError(f'exponent {ex} needs a positive integer multiple of {parameter}')
        W = store.setdefault(base, sp.Symbol(f'W_{base}', positive=True))
        return W**a*base**k
    return expr.replace(lambda e: e.is_Pow and e.exp.has(parameter), rule)


def _split_fraction(expr, store):
    """b**(n + i/q) -> R**i * b**n with R = b**(1/q), 0 < i < q; then reduce R**q = b."""
    def rule(e):
        base, ex = e.as_base_exp()
        n = sp.floor(ex)
        frac = ex - n
        R = store.setdefault((base, frac.q), sp.Symbol(f'R{frac.q}_{base}', positive=True))
        return R**frac.p*base**n
    expr = expr.replace(lambda e: e.is_Pow and e.exp.is_Rational and not e.exp.is_Integer and e.base.free_symbols, rule)
    for (base, q), R in store.items():
        expr = sp.expand(expr).replace(lambda e: e.is_Pow and e.base == R and e.exp.is_Integer and e.exp >= q,
                                       lambda e: R**(e.exp % q)*base**(e.exp//q))
    return expr


def determining(spec, parameters, degree=1, exponent=None):
    j = spec.jets
    base = j.independent + j.dependent
    monomials = sorted(sp.itermonomials(base, degree), key=sp.default_sort_key)
    constants = sp.symbols(f'a:{len(base)*len(monomials)}')
    field = tuple(sum(c*v for c, v in zip(constants[i*len(monomials):(i+1)*len(monomials)], monomials))
                  for i in range(len(base)))
    shell, _ = spec.shell()
    free = tuple(v for v in j.jets.values() if v not in shell and v not in j.dependent)
    store, roots, rows, resonant = {}, {}, [], set()
    for eq in spec.equations:
        tangent = sp.expand(j.act(eq, field).subs(shell, simultaneous=True))
        if exponent is not None:
            tangent = _split(tangent, exponent, store)
        numerator = _split_fraction(sp.numer(sp.together(tangent)), roots)
        gens = free + base + tuple(store.values()) + tuple(roots.values())
        poly = sp.Poly(sp.expand(numerator), *gens)
        rows.extend(poly.coeffs())
        index = {b: (gens.index(b), gens.index(W)) for b, W in store.items()}
        for b, (ib, iw) in index.items():
            groups = {}
            for mono in poly.monoms():
                rest = tuple(e for q, e in enumerate(mono) if q not in (ib, iw))
                groups.setdefault(rest, set()).add((mono[iw], mono[ib]))
            for pairs in groups.values():
                for (a1, k1), (a2, k2) in combinations(pairs, 2):
                    if a1 != a2:
                        resonant.add(sp.Rational(k2 - k1, a1 - a2))
    matrix, rhs = sp.linear_eq_to_matrix(rows, constants)
    if rhs != sp.zeros(matrix.rows, 1):
        raise ValueError('inhomogeneous determining equations')
    return matrix, field, constants, resonant


def _candidates(minor, parameters, positive):
    out = {}
    for factor, _ in sp.factor_list(minor)[1]:
        if not factor.free_symbols & set(parameters):
            continue
        for p in parameters:
            if factor.has(p):
                for root in sp.solve(factor, p):
                    if root.is_real is not False and not (root.is_Symbol and root in positive):
                        out.setdefault(p, set()).add(root)
                break
    return out


def special_kernel(spec, degree=1):
    """Exact kernel at a fixed parameter value; rational powers are split over b**(1/q)."""
    from .identities import require_zero
    matrix, field, constants, _ = determining(spec, (), degree)
    basis = [tuple(sp.expand(v.subs(dict(zip(constants, k)))) for v in field) for k in matrix.nullspace()]
    shell, _ = spec.shell()
    for X in basis:
        for eq in spec.equations:
            require_zero(spec.jets.act(eq, X).subs(shell, simultaneous=True), 'full prolongation sufficiency')
    return {'basis': basis}


def specialize(spec, values):
    eqs = tuple(sp.expand(sp.powsimp(e.subs(values))) for e in spec.equations)
    return PDESpec(f'{spec.name}{values}', spec.jets, eqs, spec.principal,
                   tuple(p for p in spec.parameters if p not in values), spec.conditions,
                   spec.positive, spec.domain_exclusions)


def strata(spec, parameter, degree=1, exponent=False):
    matrix, field, constants, resonant = determining(spec, (parameter,), degree, parameter if exponent else None)
    dM = DomainMatrix.from_Matrix(matrix)
    dM = dM.convert_to(dM.domain.get_field())
    _, cols = dM.rref()
    _, rows = dM.transpose().rref()
    rank = len(cols)
    minor = sp.factor(dM.extract(list(rows), list(cols)).to_Matrix().det(method='berkowitz'))
    kernel = dM.nullspace().to_Matrix() if rank < len(constants) else sp.zeros(0, len(constants))
    coords = spec.jets.independent + spec.jets.dependent
    generic = [_normalize(tuple(sp.expand(v.subs(dict(zip(constants, kernel.row(i))))) for v in field), coords)
               for i in range(kernel.rows)]
    found = _candidates(minor, (parameter,), spec.positive).get(parameter, set())
    out = {'parameter': str(parameter), 'generic_kernel_dimension': len(constants) - rank,
           'generic_basis': generic, 'pivot_minor_factors': [str(f) for f, _ in sp.factor_list(minor)[1]],
           'minor_roots': sorted(found, key=sp.default_sort_key),
           'resonances': sorted(resonant, key=sp.default_sort_key), 'strata': []}
    for value in sorted(found | resonant, key=sp.default_sort_key):
        try:
            special = special_kernel(specialize(spec, {parameter: value}), degree)
        except (ValueError, ArithmeticError) as exc:
            out['strata'].append({'value': value, 'status': 'undecided', 'reason': str(exc)})
            continue
        dim = len(special['basis'])
        limit = [_limit(X, parameter, value) for X in generic]
        extra = _complement(limit, special['basis'], coords)
        out['strata'].append({'value': value, 'status': 'decided', 'kernel_dimension': dim,
                              'jump': dim - out['generic_kernel_dimension'], 'extra': extra,
                              'basis': special['basis'],
                              'source': 'pivot minor' if value in found else 'power resonance'})
    return out


def _limit(X, parameter, value):
    """Leading nonzero term of the generic generator as the parameter tends to the stratum."""
    for k in (0, 1, 2, 3, -1, -2, -3):
        Y = tuple(sp.cancel(c*(parameter - value)**k).subs(parameter, value) for c in X)
        if not any(v.has(sp.zoo, sp.nan, sp.oo) for v in Y) and any(v != 0 for v in Y):
            return Y
    raise ArithmeticError('generic generator has no finite limit on the stratum')


def _normalize(X, coords):
    lead = next(sp.Poly(c, *coords).coeffs()[0] for c in X if c != 0)
    return tuple(sp.factor(sp.cancel(c/lead)) for c in X)


def _complement(generic, special, coords):
    """Special generators that enlarge the span of the specialized generic kernel."""
    span = list(generic)
    extra = []
    for X in special:
        if _rank(span + [X], coords) > _rank(span, coords):
            span.append(X)
            extra.append(X)
    return extra


def _rank(fields, coords):
    if not fields:
        return 0
    monos = set()
    for X in fields:
        for comp in X:
            monos |= set(sp.Poly(sp.expand(comp), *coords).monoms())
    monos = sorted(monos)
    M = sp.Matrix([[sp.Poly(sp.expand(comp), *coords).coeff_monomial(m) for comp in X for m in monos] for X in fields])
    return M.rank()
