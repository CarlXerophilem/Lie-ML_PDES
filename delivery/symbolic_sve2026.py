"""Deterministic complete-JetSpace Lie classification and scaling integral for scalar P and M."""
import json
import sympy as sp

from lie_reduce.algebra import canonical_basis_dict
from lie_reduce.determining import smooth_symmetries
from lie_reduce.models import discover_and_enumerate, scalar_spec
from lie_reduce.reduce import reduce


def _require(condition, stage):
    if not condition:
        raise ArithmeticError(stage)


def classify(model):
    """Derive unrestricted smooth point symmetries and exponent strata on complete JetSpace."""
    m = sp.Symbol('m', real=True)
    spec = scalar_spec(model, m)
    smooth = smooth_symmetries(spec, exponent=m)
    _require(smooth['smooth_to_affine_proved'], f'{model}: smooth-to-affine Hessian elimination')

    strata_data = smooth['strata_classification']
    coords = spec.jets.independent + spec.jets.dependent
    # Rename dependent coordinate phi -> u only for compatibility with reproduce_sve2026 symbol u
    u_legacy = sp.Symbol('u', real=True)
    phi_sym = spec.jets.dependent[0]

    def _norm_basis(raw_basis):
        canon = canonical_basis_dict(raw_basis, coords, prefix='Y')
        return [tuple(c.subs(phi_sym, u_legacy) for c in vec) for vec in canon.values()]

    roots = tuple(sorted(
        int(row['value']) for row in strata_data['strata']
        if row.get('jump') and row['value'].is_Integer and int(row['value']) >= 1
    ))
    bases = {'m': _norm_basis(strata_data['generic_basis'])}
    for r_val in roots:
        row = next(r for r in strata_data['strata'] if r['value'] == r_val)
        bases[str(r_val)] = _norm_basis(row['basis'])

    return {
        'exceptional_exponents': roots,
        'smooth_to_affine_proved': smooth['smooth_to_affine_proved'],
        'stratum_hessian_checks': smooth['stratum_hessian_checks'],
        'preserved_parameters': [str(p) for p in spec.parameters],
        'bases': bases,
    }


def material_scaling(generator=None):
    """Derive the scaling quotient and exact first integral of M purely via lie_reduce."""
    m = sp.Symbol('m', real=True)
    spec, basis, subalgebras = discover_and_enumerate(scalar_spec('M', m), degree=1, exponent=m)
    phi_sym = spec.jets.dependent[0]
    u_legacy = sp.Symbol('u', real=True)
    if generator is None:
        sub = next(s for s in subalgebras if s['id'] == 'Y4')
        gen = sub['generators'][0]
    else:
        gen = tuple(sp.sympify(c).subs(u_legacy, phi_sym) for c in generator)
    red = reduce(spec, (gen,))
    _require(red.status == 'verified', 'M scaling reduction verified on complete JetSpace')
    _require(len(red.first_integrals) >= 1 and red.integrated_ode is not None,
             'M scaling constructive variational first integral')
    flux = red.first_integrals[0]['flux']
    z = red.graph.z
    F0 = red.graph.profiles[0]
    F_s, P_s, C_s = sp.symbols('F P C', real=True)
    jet_display = {sp.diff(F0, z, 2): C_s, sp.diff(F0, z): P_s, F0: F_s}
    flux_disp = sp.simplify(-flux.xreplace(jet_display))
    leading_disp = sp.simplify(sp.diff(flux_disp, C_s))
    return {
        'velocity': str(F_s - z * P_s),
        'bindings': {'V': str(F_s - z * P_s)},
        'leading': str(leading_disp),
        'first_integral': str(flux_disp),
        'integrated_ode': str(red.integrated_ode) + ' = 0',
        'preserved_parameters': [str(p) for p in red.preserved_parameters],
    }


def run():
    models = {name: classify(name) for name in ('P', 'M')}
    return {
        'scope': 'Local smooth point generators on complete JetSpace (phi_t,phi_s,g,kappa>0; real m>=1)',
        'coordinates': ['t', 's', 'phi'],
        'models': {
            name: {
                'exceptional_exponents': list(map(str, res['exceptional_exponents'])),
                'smooth_to_affine_proved': res['smooth_to_affine_proved'],
                'stratum_hessian_checks': res['stratum_hessian_checks'],
                'preserved_parameters': res['preserved_parameters'],
                'bases': {
                    exp_key: [list(map(str, vec)) for vec in basis]
                    for exp_key, basis in res['bases'].items()
                },
            }
            for name, res in models.items()
        },
        'material_scaling': material_scaling(),
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
