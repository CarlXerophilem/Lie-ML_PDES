"""Deterministic Lie algebra operations and subalgebra enumeration from generator combinations."""
from itertools import combinations
import sympy as sp


def bracket(X, Y, coordinates):
    X, Y = sp.Matrix(X), sp.Matrix(Y)
    return tuple(sp.expand(v) for v in (Y.jacobian(coordinates) * X - X.jacobian(coordinates) * Y))


def add(*weighted):
    return tuple(sp.expand(sum(c * X[i] for c, X in weighted)) for i in range(len(weighted[0][1])))


def coordinates_in_basis(X, basis, coordinates):
    if not basis:
        raise ValueError('empty basis')
    constants = sp.symbols(f'c_b0:{len(basis)}')
    residual = add((1, X), *[(-c, Y) for c, Y in zip(constants, basis)])
    monos = set()
    for e in residual:
        if e != 0:
            monos |= set(sp.Poly(sp.expand(e), *coordinates).monoms())
    if not monos:
        return (sp.S.Zero,) * len(basis)
    rows = [sp.Poly(sp.expand(e), *coordinates).coeff_monomial(m) for e in residual for m in sorted(monos)]
    M, rhs = sp.linear_eq_to_matrix(rows, constants)
    from sympy.polys.matrices import DomainMatrix
    dM = DomainMatrix.from_Matrix(M.row_join(-rhs))
    dM = dM.convert_to(dM.domain.get_field())
    rref, pivs = dM.rref()
    rmat = rref.to_Matrix()
    if pivs and pivs[-1] == len(constants):
        raise ValueError('generator not in span of supplied basis')
    if len(pivs) != len(constants):
        raise ValueError('supplied basis is linearly dependent')
    return tuple(sp.cancel(rmat[i, len(constants)]) for i in range(len(constants)))


def span_equal(left, right, coordinates):
    """Exact polynomial-vector-field span equality over the field of rational functions in parameters."""
    left = [tuple(map(sp.sympify, v)) for v in left]
    right = [tuple(map(sp.sympify, v)) for v in right]
    if len(left) != len(right):
        return False
    try:
        for v in left:
            coordinates_in_basis(v, right, coordinates)
        for v in right:
            coordinates_in_basis(v, left, coordinates)
    except (ValueError, sp.PolynomialError):
        return False
    return True


def closed(fields, coordinates):
    if len(fields) < 2:
        return True
    for i, X in enumerate(fields):
        for Y in fields[i + 1:]:
            Z = bracket(X, Y, coordinates)
            if all(sp.expand(v) == 0 for v in Z):
                continue
            try:
                coeffs = coordinates_in_basis(Z, fields, coordinates)
            except (ValueError, sp.PolynomialError):
                return False
            if any(sp.sympify(k).has(*coordinates) for k in coeffs):
                return False
    return True


def canonical_basis_dict(raw_basis, coordinates, prefix='G'):
    """Order and normalize any discovered basis deterministically without model-specific assumptions."""
    origin = dict.fromkeys(coordinates, 0)
    scored = []
    for X in raw_basis:
        X = tuple(sp.expand(v) for v in X)
        is_const = all(sp.diff(v, c) == 0 for v in X for c in coordinates)
        is_diag = (not is_const and all(v.subs(origin) == 0 for v in X)
                   and all(sp.diff(X[i], coordinates[j]) == 0
                           for i in range(len(coordinates)) for j in range(len(coordinates)) if i != j))
        first_nz = next((i for i, v in enumerate(X) if v != 0), len(coordinates))
        tier = 0 if is_const else (1 if is_diag else 2)
        scored.append((tier, first_nz, str(X), X))
    scored.sort(key=lambda item: item[:3])
    out = {}
    for idx, (_, first_nz, _, X) in enumerate(scored, 1):
        lead = sp.Poly(X[first_nz], *coordinates).coeffs()[0]
        normed = tuple(sp.factor(sp.cancel(v / lead)) for v in X)
        out[f'{prefix}{idx}'] = normed
    return out


def enumerate_subalgebras(basis, coordinates, n_indep, max_combo_terms=2):
    """Deterministically enumerate rank-(n_indep - 1) closed projectable subalgebras from combinations.

    Symbolic combination weights (alpha_1, alpha_2, ...) are preserved so no parameter is fixed.
    """
    if isinstance(basis, dict):
        items = list(basis.items())
    else:
        items = [(f'G{i+1}', tuple(X)) for i, X in enumerate(basis)]
    dep = coordinates[n_indep:]
    rank_target = n_indep - 1
    if rank_target < 1:
        return []

    a1, a2 = sp.symbols('alpha_1 alpha_2', real=True)
    pool = []
    # 1. Basis singletons
    for name, X in items:
        pool.append((name, tuple(X), {name}))
    # 2. Pairwise combinations from basis
    if max_combo_terms >= 2:
        for (n1, X1), (n2, X2) in combinations(items, 2):
            if rank_target == 1 or all(v == 0 for v in bracket(X1, X2, coordinates)):
                pool.append((f'{n1} + alpha_1*{n2}', add((1, X1), (a1, X2)), {n1, n2}))
    # 3. Three-term combinations for 1D subalgebras when requested
    if rank_target == 1 and max_combo_terms >= 3 and len(items) <= 6:
        for (n1, X1), (n2, X2), (n3, X3) in combinations(items, 3):
            pool.append((f'{n1} + alpha_1*{n2} + alpha_2*{n3}', add((1, X1), (a1, X2), (a2, X3)), {n1, n2, n3}))

    subalgebras = []
    for subset in combinations(pool, rank_target):
        # Skip redundant subsets where one element's basis support is a subset of another's
        supports = [sup for _, _, sup in subset]
        if any(i != k and supports[i] <= supports[k] for i in range(len(supports)) for k in range(len(supports))):
            continue
        labels = tuple(lbl for lbl, _, _ in subset)
        fields = tuple(X for _, X, _ in subset)
        if any(comp.has(*dep) for X in fields for comp in X[:n_indep]):
            continue
        base_mat = sp.Matrix([X[:n_indep] for X in fields])
        if base_mat.rank() != rank_target:
            continue
        if not closed(fields, coordinates):
            continue
        subalgebras.append({'id': ' ; '.join(labels), 'generators': fields})
    return subalgebras


def weights(spec, basis):
    coords = spec.jets.independent + spec.jets.dependent
    items = list(basis.items()) if isinstance(basis, dict) else [(f'G{i+1}', X) for i, X in enumerate(basis)]
    return {f'[{left},{right}]': bracket(X, Y, coords)
            for (left, X), (right, Y) in combinations(items, 2)
            if any(v != 0 for v in bracket(X, Y, coords))}


def verify_lie_algebra(spec, basis):
    """Verify closure and Jacobi identity in the discovered basis."""
    from .identities import require_zero
    coords = spec.jets.independent + spec.jets.dependent
    items = list(basis.items()) if isinstance(basis, dict) else [(f'G{i+1}', X) for i, X in enumerate(basis)]
    names = [k for k, _ in items]
    fields = [v for _, v in items]
    constants = {}
    for i, X in enumerate(fields):
        for k, Y in enumerate(fields):
            coeff = coordinates_in_basis(bracket(X, Y, coords), fields, coords)
            if any(v.has(*coords) for v in coeff):
                raise ArithmeticError('nonconstant structure coefficients')
            constants[i, k] = sp.Matrix(coeff)
    count = 0
    for i, j, k in combinations(range(len(fields)), 3):
        jac = sp.zeros(len(fields), 1)
        for a, b, c in ((i, j, k), (j, k, i), (k, i, j)):
            jac += sum((constants[b, c][d] * constants[a, d] for d in range(len(fields))), sp.zeros(len(fields), 1))
        for v in jac:
            require_zero(v, 'Jacobi')
        count += 1
    return {
        'status': 'verified',
        'dimension': len(fields),
        'structure_constants': {f'[{names[i]},{names[j]}]': tuple(c)
                                for (i, j), c in constants.items() if i < j and any(x != 0 for x in c)},
        'jacobi_triples': count,
    }
