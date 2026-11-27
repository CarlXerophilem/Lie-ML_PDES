"""Parameter strata of the degree-d determining system on a complete JetSpace.

Symbolic exponents (including half-integer/rational multiples on composite bases such as
(u**2 + v**2)**((m - 1)/2)) and all other symbolic PDE parameters are preserved exactly.
"""
from itertools import combinations
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from .spec import PDESpec


def normalize_powers(expr, parameter=None, store=None, roots=None, seen=None):
    """Replace symbolic-exponent and fractional powers by independent positive symbols times integer powers."""
    if store is None:
        store = {}
    if roots is None:
        roots = {}
    if seen is None:
        seen = {}

    if parameter is None:
        exp_syms = sorted(
            {s for p in expr.atoms(sp.Pow) if p.base.free_symbols and not p.exp.is_Integer for s in p.exp.free_symbols},
            key=sp.default_sort_key,
        )
        if len(exp_syms) == 1:
            parameter = exp_syms[0]

    def match(e):
        if not (e.is_Pow and e.base.free_symbols):
            return False
        if parameter is not None and e.exp.has(parameter):
            return True
        return e.exp.is_Rational and not e.exp.is_Integer

    def rule(e):
        base, ex = e.as_base_exp()
        if parameter is not None and ex.has(parameter):
            poly = sp.Poly(sp.expand(ex), parameter)
            if poly.degree() != 1:
                raise ValueError(f'exponent {ex} is not affine in {parameter}')
            a, k = poly.all_coeffs()
            a, k = sp.sympify(a), sp.sympify(k)
            if not (a.is_Rational and a != 0 and k.is_Rational):
                raise ValueError(f'exponent {ex} needs nonzero rational slope and rational offset')
        else:
            a, k = sp.Integer(0), sp.sympify(ex)
        seen.setdefault(base, set()).add((a, k))
        n = sp.floor(k)
        frac = k - n
        factor = sp.S.One
        if a != 0:
            qa = a.q
            pa = a.p
            W = store.setdefault((base, qa), sp.Symbol(f'W{qa}_{len(store)}', positive=True))
            factor *= W**pa
        if frac != 0:
            R = roots.setdefault((base, frac.q), sp.Symbol(f'R{frac.q}_{len(roots)}', positive=True))
            factor *= R**frac.p
        return factor * base**n

    replaced = expr.replace(match, rule)
    numerator = sp.expand(sp.numer(sp.together(replaced)))
    for (base, q), R in roots.items():
        numerator = sp.expand(numerator).replace(
            lambda e, R=R, q=q: e.is_Pow and e.base == R and e.exp.is_Integer and e.exp >= q,
            lambda e, base=base, R=R, q=q: R**(e.exp % q) * base**(e.exp // q),
        )
    return numerator, store, roots, seen


def determining(spec, parameters=(), degree=1, exponent=None):
    j = spec.jets
    base = j.independent + j.dependent
    monomials = sorted(sp.itermonomials(base, degree), key=sp.default_sort_key)
    constants = sp.symbols(f'a:{len(base)*len(monomials)}')
    field = tuple(sum(c*v for c, v in zip(constants[i*len(monomials):(i+1)*len(monomials)], monomials))
                  for i in range(len(base)))
    shell, _ = spec.shell()
    free = tuple(v for v in j.jets.values() if v not in shell and v not in j.dependent)
    store, roots, seen, rows, resonant = {}, {}, {}, [], set()
    for eq in spec.equations:
        tangent = sp.expand(j.act(eq, field).subs(shell, simultaneous=True))
        numerator, _, _, _ = normalize_powers(tangent, exponent, store, roots, seen)
        gens = free + base + tuple(store.values()) + tuple(roots.values())
        poly = sp.Poly(sp.expand(numerator), *gens)
        rows.extend(poly.coeffs())
        if exponent is not None:
            for b, qa in list(store):
                W = store[b, qa]
                if b in gens:
                    ib, iw = gens.index(b), gens.index(W)
                    groups = {}
                    for mono in poly.monoms():
                        rest = tuple(e for q, e in enumerate(mono) if q not in (ib, iw))
                        groups.setdefault(rest, set()).add((sp.Rational(mono[iw], qa), mono[ib]))
                    for pairs in groups.values():
                        for (a1, k1), (a2, k2) in combinations(pairs, 2):
                            if a1 != a2:
                                resonant.add(sp.Rational(k2 - k1, a1 - a2))
                else:
                    for a1, k1 in seen.get(b, ()):
                        if a1 != 0:
                            for shift in range(4):
                                resonant.add(sp.Rational(shift - k1, a1))
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


def special_kernel(spec, degree=1, exponent=None):
    """Exact kernel on complete JetSpace, preserving symbolic parameters."""
    from .identities import require_zero
    matrix, field, constants, _ = determining(spec, spec.parameters, degree, exponent=exponent)
    dM = DomainMatrix.from_Matrix(matrix)
    dM = dM.convert_to(dM.domain.get_field())
    rank = len(dM.rref()[1])
    kernel = dM.nullspace().to_Matrix() if rank < len(constants) else sp.zeros(0, len(constants))
    coords = spec.jets.independent + spec.jets.dependent
    basis = [_normalize(tuple(sp.expand(v.subs(dict(zip(constants, kernel.row(i))))) for v in field), coords)
             for i in range(kernel.rows)]
    shell, _ = spec.shell()
    for X in basis:
        for eq in spec.equations:
            require_zero(spec.jets.act(eq, X).subs(shell, simultaneous=True), 'full prolongation sufficiency')
    return {'basis': basis, 'rank': rank, 'dimension': len(basis)}


def specialize(spec, values):
    eqs = tuple(sp.expand(sp.powsimp(e.subs(values))) for e in spec.equations)
    return PDESpec(f'{spec.name}{values}', spec.jets, eqs, spec.principal,
                   tuple(p for p in spec.parameters if p not in values), spec.conditions,
                   spec.positive, spec.domain_exclusions)


def strata(spec, parameter, degree=1, exponent=False):
    matrix, field, constants, resonant = determining(spec, spec.parameters or (parameter,), degree,
                                                     parameter if exponent else None)
    dM = DomainMatrix.from_Matrix(matrix)
    dM = dM.convert_to(dM.domain.get_field())
    _, cols = dM.rref()
    _, rows = dM.transpose().rref()
    rank = len(cols)
    minor = sp.factor(dM.extract(list(rows), list(cols)).to_Matrix().det(method='berkowitz')) if rank else sp.S.One
    kernel = dM.nullspace().to_Matrix() if rank < len(constants) else sp.zeros(0, len(constants))
    coords = spec.jets.independent + spec.jets.dependent
    generic = [_normalize(tuple(sp.expand(v.subs(dict(zip(constants, kernel.row(i))))) for v in field), coords)
               for i in range(kernel.rows)]
    found = _candidates(minor, (parameter,), spec.positive).get(parameter, set())
    out = {
        'parameter': str(parameter),
        'preserved_parameters': [str(p) for p in spec.parameters],
        'generic_kernel_dimension': len(constants) - rank,
        'generic_basis': generic,
        'pivot_minor_factors': [str(f) for f, _ in sp.factor_list(minor)[1]],
        'minor_roots': sorted(found, key=sp.default_sort_key),
        'resonances': sorted(resonant, key=sp.default_sort_key),
        'strata': [],
    }
    for value in sorted(found | resonant, key=sp.default_sort_key):
        try:
            special = special_kernel(specialize(spec, {parameter: value}), degree)
        except (ValueError, ArithmeticError) as exc:
            out['strata'].append({'value': value, 'status': 'undecided', 'reason': str(exc)})
            continue
        dim = len(special['basis'])
        limit = [_limit(X, parameter, value) for X in generic]
        extra = _complement(limit, special['basis'], coords)
        out['strata'].append({
            'value': value,
            'status': 'decided',
            'kernel_dimension': dim,
            'jump': dim - out['generic_kernel_dimension'],
            'extra': extra,
            'basis': special['basis'],
            'source': 'pivot minor' if value in found else 'power resonance',
        })
    return out


def _limit(X, parameter, value):
    for k in (0, 1, 2, 3, -1, -2, -3):
        Y = tuple(sp.cancel(c*(parameter - value)**k).subs(parameter, value) for c in X)
        if not any(v.has(sp.zoo, sp.nan, sp.oo) for v in Y) and any(v != 0 for v in Y):
            return Y
    raise ArithmeticError('generic generator has no finite limit on the stratum')


def _normalize(X, coords):
    lead = next(sp.Poly(c, *coords).coeffs()[0] for c in X if c != 0)
    return tuple(sp.factor(sp.cancel(c/lead)) for c in X)


def _complement(generic, special, coords):
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
