"""Complete-JetSpace infinitesimal determining solvers (polynomial and smooth-to-affine)."""
import sympy as sp
from sympy.core.function import AppliedUndef
from sympy.polys.matrices import DomainMatrix

from .hidden import determining as _poly_determining, normalize_powers, special_kernel, specialize, strata
from .identities import require_zero
from .strata import rank_locus


def symmetries(spec, degree=1, exponent=None):
    """Exact polynomial-class point symmetries on the complete JetSpace, preserving all parameters."""
    matrix, field, constants, _ = _poly_determining(spec, spec.parameters, degree, exponent=exponent)
    dM = DomainMatrix.from_Matrix(matrix)
    dM = dM.convert_to(dM.domain.get_field())
    rank = len(dM.rref()[1])
    kernel = dM.nullspace().to_Matrix() if rank < len(constants) else sp.zeros(0, len(constants))
    coords = spec.jets.independent + spec.jets.dependent
    basis = []
    for i in range(kernel.rows):
        vec = tuple(sp.expand(v.subs(dict(zip(constants, kernel.row(i))))) for v in field)
        lead = next(sp.Poly(c, *coords).coeffs()[0] for c in vec if c != 0)
        basis.append(tuple(sp.factor(sp.cancel(c / lead)) for c in vec))
    shell, denominators = spec.shell()
    for generator in basis:
        for equation in spec.equations:
            require_zero(spec.jets.act(equation, generator).subs(shell, simultaneous=True),
                         'full prolongation sufficiency')
    return {
        'full_prolongation_verified': True,
        'symmetry_type': 'point',
        'scope': f'polynomial point coefficients of degree <= {degree} on principal chart',
        'degree': degree,
        'preserved_parameters': [str(p) for p in spec.parameters],
        'basis': basis,
        'matrix': matrix,
        'rank': rank,
        'denominators': denominators,
        'strata': rank_locus(matrix, tuple(p for p in spec.parameters if p != exponent)),
    }


def _row_atoms(rows, known_syms=()):
    found = set()
    known = set(known_syms)
    for r in rows:
        ds = r.atoms(sp.Derivative)
        found |= ds
        found |= sp.sympify(r.xreplace({d: sp.S.Zero for d in ds})).atoms(AppliedUndef)
        found |= (r.free_symbols - known)
    return sorted(found, key=lambda a: (-getattr(a, 'derivative_count', 0), sp.default_sort_key(a)))


def _forced_zero_atoms(rows, atoms):
    """Return subset of ``atoms`` uniquely forced to zero by homogeneous linear ``rows``."""
    if not rows or not atoms:
        return set()
    M, rhs = sp.linear_eq_to_matrix(rows, atoms)
    if rhs != sp.zeros(M.rows, 1):
        return set()
    dM = DomainMatrix.from_Matrix(M)
    dM = dM.convert_to(dM.domain.get_field())
    rref, pivots = dM.rref()
    rmat = rref.to_Matrix()
    forced = set()
    for r_idx, c_idx in enumerate(pivots):
        if all(rmat[r_idx, j] == 0 for j in range(len(atoms)) if j != c_idx):
            forced.add(atoms[c_idx])
    return forced


def _split_independent_coords(rows, candidate_vars):
    """Split each row as a polynomial in variables on which no undefined function in that row depends."""
    out = []
    for row in rows:
        row = sp.expand(row)
        if row == 0:
            continue
        atoms = row.atoms(AppliedUndef, sp.Derivative)
        indep = [v for v in candidate_vars if v.is_Symbol and not any(a.has(v) for a in atoms)]
        if indep:
            out.extend(sp.Poly(row, *indep).coeffs())
        else:
            out.append(row)
    return [sp.expand(r) for r in out if r != 0]


def _diff_power_safe(expr, var, exponent=None):
    """Differentiate a determining row wrt ``var``, keeping symbolic power bases polynomial."""
    d = sp.diff(expr, var)
    if d == 0:
        return sp.S.Zero
    num, _, _, _ = normalize_powers(sp.expand(d), exponent)
    return num


def _prove_hessian_zero(spec, exponent=None):
    """Generic Spencer/prolongation elimination on unrestricted smooth coefficients Xi_k(coords).

    Iteratively drops zero first-partials, substitutes vanishing higher partials, and prolongs
    surviving determining equations wrt coordinates to test whether D^2 Xi_k == 0 everywhere.
    """
    j = spec.jets
    coords = j.independent + j.dependent
    dep = j.dependent
    shell, _ = spec.shell()
    free_jets = tuple(v for v in j.jets.values() if v not in shell and v not in dep)
    funcs = [sp.Function(f'Xi_{k}')(*coords) for k in range(len(coords))]
    current_field = list(funcs)
    zero_derivs = {}

    for _ in range(16):
        store, roots, seen = {}, {}, {}
        raw_rows = []
        for eq in spec.equations:
            tangent = sp.expand(j.act(eq, current_field).subs(shell, simultaneous=True))
            if zero_derivs:
                tangent = sp.expand(tangent.xreplace(zero_derivs))
            if tangent == 0:
                continue
            num, _, _, _ = normalize_powers(tangent, exponent, store, roots, seen)
            jet_vars = (free_jets
                        + tuple(W for (b, _), W in store.items() if b.free_symbols & set(free_jets))
                        + tuple(R for (b, _), R in roots.items() if b.free_symbols & set(free_jets)))
            if jet_vars:
                raw_rows.extend(sp.Poly(num, *jet_vars).coeffs())
            else:
                raw_rows.append(num)
        all_sym_vars = (*coords, *store.values(), *roots.values())
        rows = _split_independent_coords(raw_rows, all_sym_vars)

        known = (*all_sym_vars, *spec.parameters)
        atoms = _row_atoms(rows, known)
        forced = _forced_zero_atoms(rows, atoms)
        changed = False
        for d in forced:
            if isinstance(d, (AppliedUndef, sp.Symbol)):
                current_field = [sp.expand(e.subs(d, sp.S.Zero).doit()) for e in current_field]
                zero_derivs = {}
                changed = True
            elif isinstance(d, sp.Derivative) and d.derivative_count == 1 and isinstance(d.expr, AppliedUndef):
                f_old = d.expr
                var_drop = d.variables[0]
                if var_drop in f_old.args:
                    new_args = tuple(a for a in f_old.args if a != var_drop)
                    f_new = sp.Function(f_old.func.__name__)(*new_args) if new_args else sp.Symbol(f_old.func.__name__ + '_c')
                    current_field = [sp.expand(e.subs(f_old, f_new).doit()) for e in current_field]
                    zero_derivs = {}
                    changed = True
            elif isinstance(d, sp.Derivative) and d.derivative_count == 2 and isinstance(d.expr, AppliedUndef) and len(set(d.variables)) == 1:
                # d^2 f / dv^2 == 0 => f is affine in v
                f_old = d.expr
                v_lin = d.variables[0]
                if v_lin in f_old.args:
                    other = tuple(a for a in f_old.args if a != v_lin)
                    nm = f_old.func.__name__
                    f0 = sp.Function(nm + '_0')(*other) if other else sp.Symbol(nm + '_0')
                    f1 = sp.Function(nm + '_1')(*other) if other else sp.Symbol(nm + '_1')
                    current_field = [sp.expand(e.subs(f_old, f0 + v_lin * f1).doit()) for e in current_field]
                    zero_derivs = {}
                    changed = True
        if changed:
            continue

        surviving_funcs = sorted({f for e in current_field for f in e.atoms(AppliedUndef)}, key=sp.default_sort_key)
        if not surviving_funcs:
            return {'proved': True, 'surviving_functions': []}

        # Prolong surviving PDE rows up to 2 differentiation steps wrt coordinates
        prolonged = list(rows)
        for _step in range(2):
            extra = []
            for r in prolonged:
                max_ord = max((d.derivative_count for d in r.atoms(sp.Derivative)), default=0)
                if max_ord <= 2:
                    for v in coords:
                        dr = _diff_power_safe(r, v, exponent=exponent)
                        if dr != 0:
                            extra.append(dr)
            prolonged = _split_independent_coords(list(dict.fromkeys(prolonged + extra)), all_sym_vars)

        p_atoms = _row_atoms(prolonged, known)
        p_forced = _forced_zero_atoms(prolonged, p_atoms)

        # Check if any 1st or unmixed 2nd derivative became forced zero after prolongation
        progressed_prolong = False
        for d in p_forced:
            if isinstance(d, (AppliedUndef, sp.Symbol)):
                current_field = [sp.expand(e.subs(d, sp.S.Zero).doit()) for e in current_field]
                progressed_prolong = True
            elif isinstance(d, sp.Derivative) and d.derivative_count == 1 and isinstance(d.expr, AppliedUndef):
                f_old = d.expr
                var_drop = d.variables[0]
                if var_drop in f_old.args:
                    new_args = tuple(a for a in f_old.args if a != var_drop)
                    f_new = sp.Function(f_old.func.__name__)(*new_args) if new_args else sp.Symbol(f_old.func.__name__ + '_c')
                    current_field = [sp.expand(e.subs(f_old, f_new).doit()) for e in current_field]
                    progressed_prolong = True
            elif isinstance(d, sp.Derivative) and d.derivative_count == 2 and isinstance(d.expr, AppliedUndef) and len(set(d.variables)) == 1:
                f_old = d.expr
                v_lin = d.variables[0]
                if v_lin in f_old.args:
                    other = tuple(a for a in f_old.args if a != v_lin)
                    nm = f_old.func.__name__
                    f0 = sp.Function(nm + '_0')(*other) if other else sp.Symbol(nm + '_0')
                    f1 = sp.Function(nm + '_1')(*other) if other else sp.Symbol(nm + '_1')
                    current_field = [sp.expand(e.subs(f_old, f0 + v_lin * f1).doit()) for e in current_field]
                    progressed_prolong = True
        if progressed_prolong:
            continue

        hessian = {sp.diff(f, v1, v2) for f in surviving_funcs for v1 in f.args for v2 in f.args}
        if hessian <= p_forced:
            return {'proved': True, 'surviving_functions': [str(f) for f in surviving_funcs]}
        break

    surviving_funcs = sorted({f for e in current_field for f in e.atoms(AppliedUndef)}, key=sp.default_sort_key)
    return {'proved': False, 'surviving_functions': [str(f) for f in surviving_funcs]}


def smooth_symmetries(spec, exponent=None):
    """Derive point symmetries starting from unrestricted smooth coefficient functions on JetSpace."""
    generic_hess = _prove_hessian_zero(spec, exponent=exponent)
    if exponent is not None:
        strata_result = strata(spec, exponent, degree=1, exponent=True)
        stratum_hess = {}
        for s_row in strata_result['strata']:
            val = s_row['value']
            if val.is_number and val >= 1:
                stratum_hess[str(val)] = _prove_hessian_zero(specialize(spec, {exponent: val}), exponent=None)['proved']
        smooth_proved = bool(generic_hess['proved'] and all(stratum_hess.values()))
        return {
            'smooth_to_affine_proved': smooth_proved,
            'stratum_hessian_checks': stratum_hess,
            'strata_classification': strata_result,
        }
    poly_result = special_kernel(spec, degree=1)
    return {
        'smooth_to_affine_proved': bool(generic_hess['proved']),
        'basis': poly_result['basis'],
        'dimension': poly_result['dimension'],
    }
