"""Depth-averaged rotating exchange tank ML benchmark via direct unparsed symbolic ODE handoff."""
from types import SimpleNamespace
import sympy as sp

from _profile_learning import Case, cli
from symbolic_new_model2026 import discover_exchange_swirl_ode


def _build_case():
    _, b_fn, t_sym, r_sym, swirl_ode, lifts, pars = discover_exchange_swirl_ode()
    p_sym = sp.Symbol('p', real=True)
    # Nonzero physical fields (H, W, B, A) on the swirl invariant family
    physical_lifts = (lifts[0], lifts[2], lifts[3], lifts[4])
    red_stub = SimpleNamespace(
        graph=SimpleNamespace(z=t_sym, profiles=(b_fn,), lifts=physical_lifts),
        reduced_equations=(-swirl_ode,),
        equations=(-swirl_ode,),
        integrated_ode=None,
        target_profile=b_fn,
        reconstructed_lifts=physical_lifts,
    )
    return Case.from_reduction(
        '2026 rotating tank',
        red_stub,
        left=0.0,
        trace_interval=(0.08, 0.20),
        trace_exprs=(p_sym,),
        parameter_symbol=p_sym,
        parameter_values=pars,
        section_values={r_sym: sp.Rational(5, 4)},
        positive_jet_guards=(lifts[3], lifts[4]),
    )


CASE = _build_case()

if __name__ == '__main__':
    cli((CASE,))
