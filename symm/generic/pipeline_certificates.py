"""Inspectable exact certificates for the approved week-four scope."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import sympy as sp

from .boundary import restrict_to_constraints
from .core import JetSpace, PointGenerator
from .jets import prolonged_action
from .parameter_models import diffusion_search, reaction_search, heat_polynomial
from .reduction import check_lie_closure
from symm.solvers.problems import scalar_lab, expressions


def stringify(value: Any) -> Any:
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, sp.MatrixBase):
        return [[str(e) for e in row] for row in value.tolist()]
    if isinstance(value, dict):
        return {key: stringify(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [stringify(item) for item in value]
    return value


def exact_certificates() -> dict:
    records = []
    for case, values in ((diffusion_search(), (sp.Integer(2), -sp.Rational(4, 3), sp.Integer(0))),
                         (reaction_search(), (sp.Integer(1), sp.Integer(-2), sp.Integer(0)))):
        strata = case.strata
        branches = []
        for value in values:
            kernel = strata.matrix.subs(strata.parameter, value).nullspace()
            generators = []
            for vector in kernel:
                substitutions = {**dict(zip(strata.coefficients, vector)), strata.parameter: value}
                remainder = sp.simplify(case.shell_residual.subs(substitutions))
                if remainder != 0:
                    raise AssertionError("finite kernel failed direct original-PDE prolongation")
                generators.append(PointGenerator(tuple(e.subs(substitutions) for e in case.generator.xi),
                                                  tuple(e.subs(substitutions) for e in case.generator.phi)))
            closure = check_lie_closure(case.space, generators)
            branches.append({"parameter": value, "finite_nullity": len(kernel),
                             "generators": [gen.as_dict() for gen in generators],
                             "original_prolongation_remainders": [0]*len(kernel),
                             "closure": closure.as_dict(),
                             "full_algebra": "infinite heat superposition" if value == 0 else "not classified by this finite search"})
        records.append({"model": case.name, "scope": case.scope, "status": "exact-in-declared-ansatz",
                        "matrix": strata.matrix, "coefficient_count": strata.matrix.cols,
                        "generic_rank": strata.generic_rank, "maximal_minors": strata.maximal_minors,
                        "minor_gcd": strata.minor_gcd, "exceptional_values": strata.exceptional_values,
                        "branches": branches})
    t, x = sp.symbols("t x")
    heat_checks = [sp.expand(sp.diff(heat_polynomial(n,t,x),t)-sp.diff(heat_polynomial(n,t,x),x,2))
                   for n in range(15)]
    sy = scalar_lab()
    from sve_lab import jets
    scalar = []
    for physical in (False, True):
        equation = jets.model_residual(jets.m, physical)
        defect = jets.act(equation, jets.t, -2*jets.s, 0)+equation-(jets.m-3)*jets.g*jets.m*jets.kappa*jets.total(
            jets.p**(jets.m-1)*jets.b/jets.q, 1)
        integral = sy.first_integral(jets.m, physical)
        velocity, slope = sp.symbols("V_positive P_positive", positive=True)
        remainder = sp.simplify((sy.profile_total(integral)-sy.reduced_residual(jets.m, physical))
                                .subs(sy.f, velocity+sy.z*sy.P).subs(sy.P, slope))
        common = sp.simplify(jets.act(equation, jets.t, jets.s, jets.u)+2*equation)
        obstruction = sy.obstruction(physical)
        principal = sy.principal_symbol_obstruction(physical)
        checks = {"Xc_multiplier": common, "X5_defect": sp.simplify(defect),
                  "first_integral": remainder,
                  "obstruction_principal_symbol": sp.simplify(obstruction["highest_polynomial"]-principal["highest_polynomial"])}
        if any(e != 0 for e in checks.values()):
            raise AssertionError("exact scalar certificate failed")
        scalar.append({"model": "physical_corrected" if physical else "printed", "status": "exact",
                       "guards": ["t>0", "phi_s>0", "phi_t>0", "g,kappa>0", "beta_tr=m*kappa"],
                       "checks": checks, "first_integral": integral,
                       "leading_factor": sp.factor(integral/sy.C),
                       "first_order_obstruction_witness": obstruction["witness"],
                       "X5_only_cubic_condition": "nonzero transport; m=0 is degenerate on beta_tr=m*kappa",
                       "conservation_pullback": sy.conservation_pullback_certificate(jets.m, physical)})
    T,S,PHI,BED=sp.symbols("t s phi bed")
    G,BETA=sp.symbols("g beta",nonzero=True)
    M=sp.Symbol("m",real=True)
    space=JetSpace((T,S),(PHI,BED),3)
    p,q=space.jet_symbol(0,(1,0)),space.jet_symbol(0,(0,1))
    a=q*space.jet_symbol(0,(2,0))-G*space.jet_symbol(0,(0,2))/q**2
    transport_term=BETA*p**(M-1)*space.jet_symbol(0,(1,1))/q
    momentum=a+G*space.jet_symbol(1,(0,1))
    transport=space.jet_symbol(1,(1,0))-p*space.jet_symbol(1,(0,1))/q+transport_term
    xc=PointGenerator((T,S),(PHI,0))
    x5=PointGenerator((T,-2*S),(0,-2*BED))
    bed_shift=PointGenerator((0,0),(0,1))
    checks={"Xc_momentum":sp.simplify(prolonged_action(space,momentum,xc)+momentum),
            "Xc_transport":sp.simplify(prolonged_action(space,transport,xc)+transport),
            "X5_momentum":sp.simplify(prolonged_action(space,momentum,x5)),
            "X5_transport_defect":sp.simplify(prolonged_action(space,transport,x5)+3*transport-(3-M)*transport_term),
            "bed_shift_momentum":sp.simplify(prolonged_action(space,momentum,bed_shift)),
            "bed_shift_transport":sp.simplify(prolonged_action(space,transport,bed_shift))}
    if any(e != 0 for e in checks.values()):
        raise AssertionError("coupled generator certificate failed")
    z0,T0,S0=sp.symbols("z0 T0 S0",positive=True)
    surface_actions = []
    for name, surface, expected in (("moving-ray",S-z0*T,True),("fixed-time",T-T0,False),("fixed-wall",S-S0,False)):
        action=T*sp.diff(surface,T)+S*sp.diff(surface,S)
        restricted=restrict_to_constraints(action,(surface,))
        if restricted.verified != expected:
            raise AssertionError("boundary control failed")
        surface_actions.append({"name":name,"surface":surface,"action":action,
                                "restriction_remainder":restricted.remainder,"invariant":restricted.verified})
    args, cubic, _ = expressions("cubic_X5")
    z,f,p,c,h,m,g,kappa=args
    amplitude=sp.Symbol("K",positive=True)
    anchor=amplitude*z**sp.Rational(1,3)
    substituted=cubic.subs({p:sp.diff(anchor,z),c:sp.diff(anchor,z,2),h:sp.diff(anchor,z,3)})
    anchor_remainder=sp.simplify(substituted.subs(kappa,(1-27*g/amplitude**3)/(12*g)))
    if anchor_remainder != 0:
        raise AssertionError("cubic exact anchor failed")
    anchor_factor=sp.factor(substituted)
    return stringify({"status":"verified","scope":"selected finite searches, scalar equations and coupled generators; no maximal SVE classification",
        "rank_strata":records,"heat_superposition":{"status":"exact-infinite-family", "family":"sum_j n! t^j x^(n-2j)/(j! (n-2j)!), n>=0",
                "independence_witness":"f_n(0,x)=x**n", "operator_remainders":heat_checks,
                "general_criterion":"pr(f(t,x)*d_u)(u_t-u_xx)=f_t-f_xx"},
        "scalar_models":scalar,"common_chart":sy.common_scaling_certificate(),
        "coupled_corrected":{"status":"verified-generators", "checks":checks,
                "Xc":xc.as_dict(),"X5_bed_lift":x5.as_dict(),"cubic_subalgebra":check_lie_closure(space,(xc,x5,bed_shift)).as_dict(),
                "X5_bare_momentum_defect":2*G*space.jet_symbol(1,(0,1)),"maximal_classification":False},
        "boundary_controls":surface_actions,"cubic_anchor":{"residual_factor":anchor_factor,
                "constraint_substitution_remainder":anchor_remainder,
                "condition":"K**3=27*g/(1-12*g*kappa), positive K and denominator", "checked_by_numerical_exact_anchor":True},
        "weights":{"cubic_X5":"7/24","common_scaling":"3/8","time_window":"evaluation/quadrature only; not invariant time caps"}})
