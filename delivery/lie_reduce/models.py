"""PDE definitions from balances; independent of frozen prolongation implementation."""
from functools import lru_cache
import sympy as sp
from .spec import PDESpec
from .jets import JetSpace


def _project(basis, coords, conditions):
    """Coefficient vectors in ``basis`` whose combination satisfies ``conditions``."""
    count = len(basis)
    if count == 0:
        return []
    unknowns = sp.symbols(f"a0:{count}")
    combined = [sum((unknowns[j] * basis[j][i] for j in range(count)), sp.Integer(0))
                for i in range(len(basis[0]))]
    rows = [sp.expand(value) for value in conditions(combined, coords)]
    matrix, rhs = sp.linear_eq_to_matrix(rows, unknowns)
    if rhs != sp.zeros(len(rows), 1):
        raise ArithmeticError("generator projection was inhomogeneous")
    projected = []
    for column in matrix.nullspace():
        projected.append(tuple(sp.expand(sum(column[j] * basis[j][i] for j in range(count)))
                               for i in range(len(basis[0]))))
    return projected


def _constant_rows(vector, coords):
    return [sp.diff(component, coordinate) for component in vector for coordinate in coords]


def _vanishing_at_origin(vector, coords):
    origin = dict.fromkeys(coords, 0)
    return [component.subs(origin) for component in vector]


def _diagonal_rows(vector, coords):
    return [sp.diff(vector[i], coords[j]) for i in range(len(coords)) for j in range(len(coords)) if i != j]


def _off_diagonal_rows(vector, coords):
    return [sp.diff(vector[i], coords[i]) for i in range(len(coords))]


def _weights(vector, coords):
    return [sp.diff(vector[i], coords[i]) for i in range(len(coords))]


def _unique(space, equations):
    count = len(space)
    if count == 0:
        raise ArithmeticError("empty symmetry subspace")
    unknowns = sp.symbols(f"c0:{count}")
    combined = [sum((unknowns[j] * space[j][i] for j in range(count)), sp.Integer(0))
                for i in range(len(space[0]))]
    rows = [sp.expand(value) for value in equations(combined)]
    solution = sp.solve(rows, unknowns, dict=True)
    if len(solution) != 1 or set(solution[0]) != set(unknowns):
        raise ArithmeticError("canonical generator is not unique")
    return tuple(sp.expand(component.subs(solution[0], simultaneous=True)) for component in combined)


def _span_equal(left, right, coords):
    monomials = set()
    for vector in (*left, *right):
        for component in vector:
            monomials.update(exponents for exponents, _ in sp.Poly(sp.expand(component), *coords).terms())
    ordered = sorted(monomials)

    def column(vector):
        values = []
        for component in vector:
            polynomial = sp.Poly(sp.expand(component), *coords)
            values.extend(polynomial.coeff_monomial(exponents) for exponents in ordered)
        return sp.Matrix(values)

    left_matrix = sp.Matrix.hstack(*(column(vector) for vector in left))
    right_matrix = sp.Matrix.hstack(*(column(vector) for vector in right))
    return left_matrix.rank() == right_matrix.rank() == left_matrix.row_join(right_matrix).rank()


def _split_linear(raw, coords):
    translations = _project(raw, coords, _constant_rows)
    linear = _project(raw, coords, _vanishing_at_origin)
    if len(translations) + len(linear) != len(raw) or len(translations) != 3:
        raise ArithmeticError("translation/linear split does not match the determining kernel")
    diagonal = _project(linear, coords, _diagonal_rows)
    off = _project(linear, coords, _off_diagonal_rows)
    if len(diagonal) + len(off) != len(linear):
        raise ArithmeticError("diagonal split does not match the linear kernel")
    return translations, diagonal, off


def _axis(space, index, width):
    return _unique(space, lambda vector, index=index, width=width: [
        vector[i] - (1 if i == index else 0) for i in range(width)])


def _label_scalar(raw, coords, model):
    translations, diagonal, off = _split_linear(raw, coords)
    fields = {
        "Y1": _axis(translations, 0, 3),
        "Y2": _axis(translations, 2, 3),
        "Y3": _axis(translations, 1, 3),
        "Y4": _unique(diagonal, lambda vector: [_weights(vector, coords)[0] - _weights(vector, coords)[1],
                                                _weights(vector, coords)[0] - 1]),
    }
    if len(diagonal) == 2:
        fields["Y5"] = _unique(diagonal, lambda vector: [_weights(vector, coords)[2],
                                                         _weights(vector, coords)[0] - 1])
    elif len(diagonal) != 1:
        raise ArithmeticError("unexpected scalar scaling dimension")
    if len(off) == 1:
        if model != "P":
            raise ArithmeticError("material kernel contains an off-diagonal linear field")
        fields["Y6"] = _unique(off, lambda vector: [sp.diff(vector[2], coords[0]) - 1])
    elif len(off) != 0:
        raise ArithmeticError("unexpected off-diagonal dimension")
    if not _span_equal(list(fields.values()), raw, coords):
        raise ArithmeticError("canonical labels do not span the determining kernel")
    return fields


def _label_euler(raw, coords):
    translations, diagonal, off = _split_linear(raw, coords)
    if off:
        raise ArithmeticError("Euler kernel contains an off-diagonal linear field")
    fields = {
        "X1": _axis(translations, 0, 5),
        "X2": _axis(translations, 1, 5),
        "X3": _axis(translations, 4, 5),
        "X4": _unique(diagonal, lambda vector: [_weights(vector, coords)[0] - _weights(vector, coords)[1],
                                                _weights(vector, coords)[0] - 1]),
    }
    if len(diagonal) == 2:
        fields["X5"] = _unique(diagonal, lambda vector: [_weights(vector, coords)[1],
                                                         _weights(vector, coords)[0] - 1])
    elif len(diagonal) != 1:
        raise ArithmeticError("unexpected Euler scaling dimension")
    if not _span_equal(list(fields.values()), raw, coords):
        raise ArithmeticError("canonical labels do not span the determining kernel")
    return fields


def _scalar_spec(model, exponent):
    t, s, u = sp.symbols("t s phi", real=True)
    g, k = sp.symbols("g kappa", positive=True)
    jets = JetSpace((t, s), (u,), 3)
    p, q = jets.jet(0, 1, 0), jets.jet(0, 0, 1)
    a, b, c = jets.jet(0, 2, 0), jets.jet(0, 1, 1), jets.jet(0, 0, 2)
    amplitude = q * a - g * c / q**2
    equation = jets.D(amplitude, 0) - g * jets.D(exponent * k * p**(exponent - 1) * b / q, 1)
    if model == "M":
        equation -= jets.D(p * amplitude / q, 1)
    elif model != "P":
        raise ValueError(model)
    return PDESpec(model, jets, (sp.expand(equation),), (jets.jet(0, 3, 0),), (),
                   ("phi_t>0", "phi_s>0", "g,kappa>0", f"m={exponent}"), positive=(p, q, g, k))


def _euler_spec(exponent):
    t, x, h, u, bed = sp.symbols("t x h u B", real=True)
    g, k = sp.symbols("g kappa", positive=True)
    jets = JetSpace((t, x), (h, u, bed), 1)
    equations = (jets.D(h, 0) + jets.D(h * u, 1),
                 jets.D(u, 0) + u * jets.D(u, 1) + g * jets.D(h + bed, 1),
                 jets.D(bed, 0) + k * jets.D(u**exponent, 1))
    return PDESpec("E1", jets, equations, tuple(jets.jet(i, 1, 0) for i in range(3)), (),
                   ("h,u,g,kappa>0", f"m={exponent}"), positive=(h, u, g, k))


@lru_cache(maxsize=None)
def _scalar_basis(model, exponent):
    from .determining import symmetries
    spec = _scalar_spec(model, exponent)
    coords = spec.jets.independent + spec.jets.dependent
    raw = symmetries(spec, 1)["basis"]
    labeled = _label_scalar(raw, coords, model)
    return tuple(labeled.items())


@lru_cache(maxsize=None)
def _euler_basis(exponent):
    from .determining import symmetries
    spec = _euler_spec(exponent)
    coords = spec.jets.independent + spec.jets.dependent
    raw = symmetries(spec, 1)["basis"]
    labeled = _label_euler(raw, coords)
    return tuple(labeled.items())


def scalar(model, exponent=2):
    exponent = int(exponent)
    spec = _scalar_spec(model, exponent)
    return spec, dict(_scalar_basis(model, exponent))


def euler(exponent=2):
    exponent = int(exponent)
    spec = _euler_spec(exponent)
    return spec, dict(_euler_basis(exponent))


def annular():
    """Selected rank-2 subalgebra on polar E2, not a solved X_i/Y_i basis.

    The pair is rotation together with bed drift. It is not a maximal planar
    classification and it is not the five-balance rotating-exchange model.
    Sufficiency is the independent pullback of this declared quotient.
    """
    t,r,theta=sp.symbols('t r theta',real=True)
    h,V,W,B=sp.symbols('h V W B',real=True)
    g,K,G=sp.symbols('g K G',positive=True);f,c=sp.symbols('f c',real=True)
    j=JetSpace((t,r,theta),(h,V,W,B),2)
    S=V**2+W**2;Dr=lambda e:j.D(e,1);Dt=lambda e:j.D(e,0);Da=lambda e:j.D(e,2)
    equations=(Dt(h)+Dr(r*h*V)/r+Da(h*W)/r,
               Dt(V)+V*Dr(V)+W*Da(V)/r-W**2/r+g*Dr(h+B)-f*W,
               Dt(W)+V*Dr(W)+W*Da(W)/r+V*W/r+g*Da(h+B)/r+f*V,
               Dt(B)+Dr(r*S*(K*V-G*Dr(B)))/r+Da(S*(K*W-G*Da(B)/r))/r)
    spec=PDESpec('E2',j,equations,tuple(j.jet(a,1,0,0) for a in range(4)),(),('r>0','h>0','g,K,G>0'),positive=(r,h,g,K,G))
    from .reduce import Graph
    z=sp.Symbol('z',real=True);profiles=tuple(sp.Function(n)(z) for n in ('H','V','W','Z'))
    lifts=tuple(F.subs(z,r) for F in profiles[:3])+(profiles[3].subs(z,r)+c*t,)
    return spec,((0,0,1,0,0,0,0),(1,0,0,0,0,0,c)),Graph(z,r,profiles,lifts,{t:0,theta:0,r:z}),c
