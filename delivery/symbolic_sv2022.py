"""Deterministic complete-JetSpace Lie classification and quotient for 1+1 Eulerian Grass SVE E1."""
import json
import sympy as sp

from lie_reduce.algebra import bracket, canonical_basis_dict
from lie_reduce.determining import smooth_symmetries
from lie_reduce.models import discover_and_enumerate, euler_spec
from lie_reduce.reduce import reduce


def _require(condition, stage):
    if not condition:
        raise ArithmeticError(stage)


def discover_reduction(exponent=None):
    """Discover point algebra on complete JetSpace, enumerate combinations, and reduce bed-drift."""
    m = sp.Symbol('m', real=True) if exponent is None else sp.sympify(exponent)
    spec = euler_spec(m)
    exp_sym = m if isinstance(m, sp.Symbol) else None
    _, basis, subalgebras = discover_and_enumerate(spec, degree=1, exponent=exp_sym)
    slope = sp.Symbol('b', real=True)
    alpha_1 = sp.Symbol('alpha_1', real=True)
    target_sub = next(s for s in subalgebras if s['id'] == 'X1 + alpha_1*X3')
    gen = tuple(sp.sympify(c).subs(alpha_1, slope) for c in target_sub['generators'][0])
    red = reduce(spec, (gen,))
    _require(red.status == 'verified', 'E1 bed-drift reduction verified')
    _require(len(red.reduced_equations) == 1, 'E1 bed-drift reduces to a single scalar ODE')
    return spec, basis, subalgebras, red


def run():
    m = sp.Symbol('m', real=True)
    spec = euler_spec(m)
    smooth = smooth_symmetries(spec, exponent=m)
    _require(smooth['smooth_to_affine_proved'], 'unrestricted smooth-to-affine proof on E1')

    coords = spec.jets.independent + spec.jets.dependent
    strata_info = smooth['strata_classification']
    jumps = [row['value'] for row in strata_info['strata'] if row.get('jump') and row['value'] >= 1]
    _require(jumps == [sp.Integer(3)], 'cubic exceptional stratum m=3 on E1')

    generic_basis = canonical_basis_dict(strata_info['generic_basis'], coords, prefix='X')
    cubic_row = next(row for row in strata_info['strata'] if row['value'] == 3)
    cubic_basis = canonical_basis_dict(cubic_row['basis'], coords, prefix='X')

    results = {}
    for label, basis in (('positive_generic', generic_basis), ('positive_cubic', cubic_basis)):
        b_map = {}
        for left, v in basis.items():
            for right, w in basis.items():
                val = bracket(v, w, coords)
                if any(c != 0 for c in val):
                    b_map[f'[{left},{right}]'] = list(map(str, val))
        results[label] = {
            'basis': {k: list(map(str, vec)) for k, vec in basis.items()},
            'brackets': b_map,
        }

    _, _, _, red = discover_reduction(m)
    dep_names = tuple(map(str, spec.jets.dependent))
    lifted_profiles = {name: str(expr) for name, expr in zip(dep_names, red.reconstructed_lifts)}

    return {
        'scope': 'Local smooth point symmetries on complete JetSpace, all real m>=1, K,g,h,u>0',
        'smooth_to_affine_proved': smooth['smooth_to_affine_proved'],
        'stratum_hessian_checks': smooth['stratum_hessian_checks'],
        'coordinate_order': list(map(str, coords)),
        'strata': results,
        'bed_drift_reconstructed_lifts': lifted_profiles,
        'bed_drift_reduced_ode': str(red.reduced_equations[0]) + ' = 0',
        'preserved_parameters': [str(p) for p in red.preserved_parameters],
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
