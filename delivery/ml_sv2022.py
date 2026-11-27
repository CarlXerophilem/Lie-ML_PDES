"""2022 Eulerian bed-drift ML benchmark via direct unparsed symbolic ReducedODE handoff."""
import sympy as sp

from _profile_learning import Case, cli
from symbolic_sv2022 import discover_reduction


def _build_case():
    spec, _, _, red = discover_reduction()
    z = red.graph.z
    F1 = red.target_profile
    m_sym = next(p for p in spec.parameters if str(p) == 'm')
    g_sym = next(p for p in spec.parameters if str(p) == 'g')
    K_sym = next(p for p in spec.parameters if str(p) == 'K')
    b_sym = sp.Symbol('b', real=True)
    C1_sym, C2_sym = sp.symbols('C1 C2', real=True)
    t_sym, x_sym = spec.jets.independent

    # Express reduced ODE and reconstructed lifts in flux-power profile Y(z) = F1(z)**m
    Y = sp.Function('Y')(z)
    f1_of_Y = Y ** (sp.S.One / m_sym)
    ode_Y = sp.powsimp(sp.expand(red.reduced_equations[0].subs(F1, f1_of_Y).doit()), force=True)
    lifts_Y = tuple(
        l_expr.subs(x_sym, z).subs(sp.Function(F1.func.__name__)(z), f1_of_Y)
        for l_expr in red.reconstructed_lifts
    )

    p_sym = sp.Symbol('p', real=True)
    param_vals = {
        g_sym: sp.Integer(1),
        K_sym: sp.Rational(1, 2),
        m_sym: sp.Integer(2),
        b_sym: sp.Rational(1, 4),
        C1_sym: sp.Integer(1),
        C2_sym: sp.Integer(2),
    }
    return Case.from_reduction(
        '2022 E1',
        red,
        left=0.0,
        trace_interval=(1.0, 1.4),
        trace_exprs=(p_sym,),
        parameter_symbol=p_sym,
        parameter_values=param_vals,
        ode_override_expr=(ode_Y, Y),
        lift_exprs=lifts_Y,
        section_values={t_sym: sp.Rational(1, 2), x_sym: z},
        positive_jet_guards=(Y,),
    )


CASE = _build_case()

if __name__ == '__main__':
    cli((CASE,))
