"""2026 scalar P (m=1) and compatible M->E1 (m=2) ML benchmarks via direct unparsed ReducedODE handoff."""
import numpy as np
import sympy as sp

from _profile_learning import Case, cli
from lie_reduce.models import discover_and_enumerate, scalar_spec
from lie_reduce.reduce import reduce


def _build_printed_case():
    spec_p, _, subs_p = discover_and_enumerate(scalar_spec('P', 1), degree=1)
    sub_p = next(s for s in subs_p if s['id'] == 'Y2 + alpha_1*Y5')
    red_p = reduce(spec_p, sub_p['generators'])
    t_sym, s_sym = spec_p.jets.independent
    g_sym, k_sym = spec_p.parameters[:2]
    alpha_1 = sp.Symbol('alpha_1', real=True)
    C1_sym = sp.Symbol('C1', real=True)
    z_sym = red_p.graph.z
    F0 = red_p.graph.profiles[0]
    lift_phi = red_p.graph.lifts[0].subs(t_sym, z_sym)

    return Case.from_reduction(
        '2026 P at m=1',
        red_p,
        left=1.0,
        trace_interval=(0.6, 1.0),
        trace_exprs=(sp.Integer(0), sp.Rational(1, 2)),
        parameter_symbol=C1_sym,
        parameter_values={g_sym: sp.Integer(1), k_sym: sp.Rational(1, 10), alpha_1: sp.Integer(1)},
        use_integrated_ode=True,
        lift_exprs=(lift_phi,),
        section_values={s_sym: sp.Rational(5, 4)},
    )


def _build_material_case():
    m_sym = sp.Symbol('m', real=True)
    spec_m, _, subs_m = discover_and_enumerate(scalar_spec('M', m_sym), degree=1, exponent=m_sym)
    sub_m = next(s for s in subs_m if s['id'] == 'Y1 + alpha_1*Y2')
    red_m = reduce(spec_m, sub_m['generators'])
    t_sym, _ = spec_m.jets.independent
    g_sym, k_sym = spec_m.parameters[:2]
    alpha_1 = sp.Symbol('alpha_1', real=True)
    C1_sym = sp.Symbol('C1', real=True)
    b0_sym = sp.Symbol('b_0', real=True)
    p_sym = sp.Symbol('p', real=True)
    z_sym = red_m.graph.z
    F0 = red_m.graph.profiles[0]

    # Express order-reduced M traveling ODE in material gradient Y(z) = F0'(z)
    Y = sp.Function('Y')(z_sym)
    grad_sub = {sp.diff(F0, z_sym, 2): sp.diff(Y, z_sym), sp.diff(F0, z_sym): Y}
    ode_Y = sp.simplify(-red_m.integrated_ode.xreplace(grad_sub))
    diag_Y = m_sym * k_sym * ode_Y
    lifts_e1 = (
        1 / Y,
        Y,
        b0_sym - 1 / Y - Y ** 2 / (2 * g_sym) + m_sym * k_sym * C1_sym * t_sym,
    )
    param_vals = {
        g_sym: sp.Integer(1),
        k_sym: sp.Rational(1, 20),
        m_sym: sp.Integer(2),
        alpha_1: sp.Integer(-1),
        C1_sym: -sp.Rational(1, 5),
        b0_sym: sp.Integer(3),
    }
    return Case.from_reduction(
        '2026 M to E1 at m=2',
        red_m,
        left=0.0,
        trace_interval=(1.0, 1.4),
        trace_exprs=(p_sym,),
        parameter_symbol=p_sym,
        parameter_values=param_vals,
        ode_override_expr=(ode_Y, Y),
        diagnostic_expr=diag_Y,
        lift_exprs=lifts_e1,
        section_values={t_sym: sp.Rational(1, 2)},
        positive_jet_guards=(Y,),
    )


PRINTED = _build_printed_case()
MATERIAL = _build_material_case()


def material_laurent_profile(sigma, w0, g, offset=0., degree=6):
    """Evaluate the proven m=3, g*beta=3/4 branch and its analytic tail."""
    from reproduce_sve2026 import cubic_material_laurent
    from numpy.polynomial.polynomial import polyval

    sigma = np.asarray(sigma, dtype=float)
    if not (np.all(np.isfinite(sigma)) and np.all(sigma > 0) and
            np.isfinite(w0) and w0 > 0 and np.isfinite(g) and g > 0 and
            np.isfinite(offset) and type(degree) is int and 1 <= degree <= 8):
        raise ValueError('Require a positive finite chart and 1<=degree<=8')
    xi = g * sigma ** 4 / w0 ** 3
    q = 4 * xi
    if np.any(q >= 1):
        raise ValueError('No convergence certificate on this chart')
    coeff = cubic_material_laurent(degree)
    position = polyval(xi, np.array(coeff['F_coefficients_in_w_over_sigma'], float))
    gradient = polyval(xi, np.array(coeff['Y'], float))
    magnitude = 17 * q ** (degree + 1) / (16 * (1 - q))
    return {
        'position': offset + w0 * position / sigma,
        'gradient': w0 * gradient / sigma ** 2,
        'position_tail': w0 * magnitude / (sigma * (4 * degree + 3)),
        'gradient_tail': w0 * magnitude / sigma ** 2,
    }


if __name__ == '__main__':
    cli((PRINTED, MATERIAL))
