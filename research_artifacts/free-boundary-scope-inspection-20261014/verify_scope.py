"""Bounded inspection checks; not a general free-boundary solver.

Run from the repository root with Python. The gas exponent is gamma=1+k>1.
The affine solution is checked on a>0, C-D*(x*x+y*y)/a**2>0.
Vacuum boundary traces are separate from the positive-density interior.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys

for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import sympy as sp
from symm.generic import DataCondition, DifferentialSystem, JetSpace, PDEProblem
from symm.generic.core import GenericValidationError


def run() -> dict:
    t, x, y = sp.symbols("t x y", real=True)
    a = sp.Function("a", positive=True)(t)
    C, D, K, k, g = sp.symbols("C D K k g", positive=True)
    gamma = 1 + k
    r2 = x*x + y*y
    q = C - D*r2/a**2
    rho = a**-2 * q**(1/k)
    velocity = (sp.diff(a, t)*x/a, sp.diff(a, t)*y/a)
    base = (x, y)
    checks: dict[str, str] = {}

    def zero(name: str, expression) -> None:
        value = sp.factor(sp.simplify(expression))
        if value != 0:
            raise AssertionError((name, value))
        checks[name] = "0"

    continuity = sp.diff(rho, t) + sum(sp.diff(rho*u, z) for u,z in zip(velocity, base))
    # Division by rho is valid only in the positive-density interior.
    zero("Euler_continuity_interior", continuity/rho)
    # On a>0,q>0, H = K gamma rho^(gamma-1)/(gamma-1).
    enthalpy = K*gamma/k * a**(-2*k)*q
    acceleration = 2*K*gamma*D/k * a**(-2*k-1)
    for i,z in enumerate(base):
        material = sp.diff(velocity[i], t) + sum(
            u*sp.diff(velocity[i], v) for u,v in zip(velocity,base))
        zero(f"Euler_momentum_{z}_interior", (
            material + sp.diff(enthalpy,z)).subs(sp.diff(a,t,2), acceleration))

    # The unknown boundary is r=a(t)*sqrt(C/D). Phi is a smooth level set.
    Phi = r2 - C*a*a/D
    level_transport = sp.diff(Phi,t) + sum(u*sp.diff(Phi,z) for u,z in zip(velocity,base))
    zero("boundary_transport_multiplier", level_transport - 2*sp.diff(a,t)*Phi/a)
    zero("enthalpy_vanishes_on_vacuum_boundary", enthalpy.subs(y*y, C*a*a/D-x*x))
    R = a*sp.sqrt(C/D)
    zero("radial_boundary_speed", sp.diff(R,t) - sp.diff(a,t)*R/a)

    # A material reference map X(t,alpha)=a(t)*alpha has J=a**2.
    alpha, beta = sp.symbols("alpha beta", real=True)
    X = sp.Matrix((a*alpha, a*beta))
    J = X.jacobian((alpha,beta)).det()
    rho0 = (C-D*(alpha*alpha+beta*beta))**(1/k)
    pulled_rho = rho.subs({x:a*alpha,y:a*beta}, simultaneous=True)
    zero("Lagrangian_mass_conservation", pulled_rho*J-rho0)
    zero("material_map_kinematics_x", sp.diff(X[0],t)-velocity[0].subs(x,X[0]))
    zero("material_map_kinematics_y", sp.diff(X[1],t)-velocity[1].subs(y,X[1]))

    # Flat-bed nondispersive shallow water: rho=h, gamma=2, K=g/2.
    depth = (C-D*r2/a**2)/a**2
    sw_acceleration = 2*g*D/a**3
    zero("shallow_water_parameter_specialization", acceleration.subs({k:1,K:g/2})-sw_acceleration)
    zero("shallow_water_continuity", sp.diff(depth,t)+sum(sp.diff(depth*u,z) for u,z in zip(velocity,base)))
    for i,z in enumerate(base):
        material = sp.diff(velocity[i],t)+sum(u*sp.diff(velocity[i],v) for u,v in zip(velocity,base))
        zero(f"shallow_water_momentum_{z}", (material+g*sp.diff(depth,z)).subs(sp.diff(a,t,2),sw_acceleration))

    # Scaling candidates for fixed K: weights(t,x,u,rho)=(T,L,L-T,H).
    T,L,H = sp.symbols("T L H", real=True)
    pressure_balance = k*H - 2*(L-T)
    zero("generic_gamma_scaling_balance", pressure_balance.subs(H,2*(L-T)/k))
    # This is a weight condition, not a maximal symmetry classification.
    # A translation remains an equation symmetry but moves a fixed circular footprint.
    fixed_R = sp.symbols("R0", positive=True)
    fixed_circle = r2-fixed_R**2
    bad_translation = sp.diff(fixed_circle,x).subs({x:fixed_R,y:0})
    assert bad_translation == 2*fixed_R
    # Common space-time scaling also moves an initial slice t=t0>0.
    t0 = sp.symbols("t0", positive=True)
    bad_initial_slice = (t*sp.diff(t-t0,t)).subs(t,t0)
    assert bad_initial_slice == t0

    # Field-dependent free boundaries cannot be supplied to the present API.
    U,F = sp.symbols("U F")
    space = JetSpace((t,x,y),(U,F),1)
    system = DifferentialSystem(space,(space.jet_symbol(0,(1,0,0)),))
    PDEProblem(system, data=(DataCondition("prescribed",x,(U,)),))
    api_rejection = None
    try:
        PDEProblem(system,data=(DataCondition("unknown_interface",F,(U,)),))
    except GenericValidationError as exc:
        api_rejection = str(exc)
    assert api_rejection == "data surfaces must depend only on base coordinates and parameters"

    # A field-coordinate chart also cannot silently replace a solution-dependent
    # material map; no claim about such automation is made by these checks.
    return {
        "status": "passed",
        "sympy_version": sp.__version__,
        "zero_identity_count": len(checks),
        "zero_identities": checks,
        "parameters": "gamma=1+k>1; K,C,D>0; a(t)>0",
        "interior": "x*x+y*y < a(t)**2*C/D",
        "scale_ODE": str(sp.Eq(sp.diff(a,t,2),acceleration)),
        "boundary": "r=a(t)*sqrt(C/D); p=0 by rho->0 for gamma>1",
        "negative_controls": {
            "translation_fails_fixed_circle_at_R0_0": str(bad_translation),
            "common_scaling_fails_positive_initial_time": str(bad_initial_slice),
            "unknown_boundary_rejected_by_current_API": api_rejection,
        },
        "qualifications": [
            "Explicit affine ansatz, not a certified Lie-group reduction or new solution claim.",
            "Interior identities and explicit boundary traces; no arbitrary-data existence theorem.",
            "No assertion of uniform smoothness across the vacuum boundary for general gamma.",
            "Lagrangian J=a**2 stays positive; rho0=0 at the boundary is permitted.",
            "Scaling-weight balance is not an exhaustive Lie classification.",
        ],
    }


if __name__ == "__main__":
    result = run()
    output = Path(__file__).with_name("symbolic_checks.json")
    output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result,indent=2))
