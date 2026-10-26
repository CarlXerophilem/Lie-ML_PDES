"""A guarded annular full-E example using the existing LieSymm/generic APIs.

This is a constructed smooth benchmark, not a maximal symmetry classification
or a physical validation. The supplied rotation chart is local (x>0); a
separate direct Cartesian pullback checks the reconstruction on r>0.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, is_dataclass
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import sympy as sp

from symm.generic import (
    DifferentialSystem, JetSpace, PDEProblem, PointGenerator, ReductionChart,
    bracket, characteristic, check_lie_closure, jet_coordinates, orbit_rank,
    prolong_characteristic, prolong_recursive, prolonged_action, prolonged_system,
    reduce_in_chart, total_derivative,
)

from . import models_2d as registry
from .core import JetSpace as PinnedJetSpace


@dataclass(frozen=True)
class AnnularCase:
    system: DifferentialSystem
    parameters: tuple[sp.Expr, ...]
    flux: tuple[sp.Expr, ...]
    generators: dict[str, PointGenerator]
    multipliers: dict[str, sp.Matrix]
    registry_residuals: tuple[sp.Expr, ...]


def build_case(coriolis=None) -> AnnularCase:
    """Build m=3,n=2 E; fixed Coriolis may be symbolic, nonzero, or zero."""
    t, y = sp.symbols("t y", real=True)
    x = sp.Symbol("x", positive=True)
    h = sp.Symbol("h", positive=True)
    u, v, B = sp.symbols("u v B", real=True)
    g, K, G = sp.symbols("g K G", positive=True)
    f = sp.Symbol("f", real=True, nonzero=True) if coriolis is None else sp.sympify(coriolis)
    if f.is_real is False or f.has(t, x, y, h, u, v, B):
        raise ValueError("Coriolis must be a fixed real parameter")
    c = sp.Symbol("c", real=True, nonzero=True)
    space = JetSpace((t,x,y), (h,u,v,B), 2)
    j = space.jet_symbol
    D = lambda e, i: total_derivative(space,e,i)
    speed2 = u*u+v*v
    flux = (speed2*(K*u-G*j(3,(0,1,0))), speed2*(K*v-G*j(3,(0,0,1))))
    equations = (
        j(0,(1,0,0))+D(h*u,1)+D(h*v,2),
        j(1,(1,0,0))+u*j(1,(0,1,0))+v*j(1,(0,0,1))+g*D(h+B,1)-f*v,
        j(2,(1,0,0))+u*j(2,(0,1,0))+v*j(2,(0,0,1))+g*D(h+B,2)+f*u,
        j(3,(1,0,0))+D(flux[0],1)+D(flux[1],2),
    )
    system = DifferentialSystem(space, equations, inequations=(speed2,),
        assumptions=(h>0,g>0,K>0,G>0), name="E-annular-m3-n2")
    generators = {
        "T": PointGenerator((1,0,0),(0,0,0,0)),
        "X": PointGenerator((0,1,0),(0,0,0,0)),
        "Y": PointGenerator((0,0,1),(0,0,0,0)),
        "A": PointGenerator((0,0,0),(0,0,0,1)),
        "J": PointGenerator((0,-y,x),(0,-v,u,0)),
        "D": PointGenerator((0,x,y),(2*h,u,v,2*B)),
    }
    multipliers = {name: sp.zeros(4) for name in generators}
    multipliers["J"][1,2] = -1
    multipliers["J"][2,1] = 1
    multipliers["D"] = sp.diag(2,1,1,2)
    cell = "slope_attachment_cubic_"+("f0" if f == 0 else "f_nonzero")
    pinned = registry.branch_model_2d(cell)
    old_space = PinnedJetSpace(pinned["independent_variables"],pinned["dependent_fields"],2)
    mapping = dict(zip(old_space.x, space.independent_variables))
    mapping.update({registry.g:g,registry.K:K,registry.G:G,registry.f:f})
    mapping.update({symbol:j(field,index) for (field,index),symbol in old_space.coordinates.items()})
    registry_residuals = tuple(sp.expand(a-b.xreplace(mapping))
        for a,b in zip(equations,pinned["equations"]))
    return AnnularCase(system,(g,K,G,f,c),flux,generators,multipliers,registry_residuals)


def certify_generator(case: AnnularCase, generator: PointGenerator, multipliers) -> dict:
    """Certify the off-shell covariance identity, not raw off-shell zero."""
    space = case.system.jet_space
    recursive = prolong_recursive(space,generator,2)
    other = prolong_characteristic(space,generator,2)
    lhs = prolonged_system(case.system,generator)
    residuals = tuple(sp.expand(a-b) for a,b in zip(lhs,sp.Matrix(multipliers)*sp.Matrix(case.system.equations)))
    agreement = all(sp.expand(recursive[key]-other[key]) == 0 for key in recursive)
    return dict(verified=agreement and all(e == 0 for e in residuals),
        generator=generator, characteristic=characteristic(space,generator),
        prolongation=recursive, two_prolongation_forms_agree=agreement,
        multipliers=sp.Matrix(multipliers), prolonged_equations=lhs,
        covariance_residuals=residuals, raw_off_shell_zero=all(e == 0 for e in lhs))


def _require_reduction(outcome, stage):
    if outcome.certificate.status != "verified":
        raise RuntimeError(f"{stage}: {outcome.certificate.message}; {outcome.certificate.checks}")
    return outcome.reduced_system


def radial_reduction(case: AnnularCase | None = None) -> dict:
    """Use two existing chart reductions and independently differentiate E."""
    case = build_case() if case is None else case
    source = case.system.jet_space
    t,x,y = source.independent_variables
    h,u,v,B = source.dependent_fields
    g,K,G,f,c = case.parameters
    a = sp.Symbol("a",positive=True)
    b = sp.Symbol("b",real=True)
    h0 = sp.Symbol("h0",positive=True)
    u0,v0,z0 = sp.symbols("u0 v0 z0",real=True)
    tau = sp.Symbol("tau",real=True)
    stationary = JetSpace((a,b),(h0,u0,v0,z0),2)
    time_generator = PointGenerator((1,0,0),(0,0,0,c))
    parameters = tuple(dict.fromkeys(s for e in case.parameters for s in e.free_symbols))
    time_chart = ReductionChart(stationary,(x,y),tau,t,(tau,a,b),
        (h0,u0,v0,z0+c*t),(1,1,1,1))
    time_outcome = reduce_in_chart(PDEProblem(case.system,parameters=parameters),time_generator,time_chart)
    time_system = _require_reduction(time_outcome,"time-plus-bed chart")

    radius = sp.sqrt(a*a+b*b)
    frame = sp.Matrix([[1,0,0,0],[0,a/radius,b/radius,0],
                       [0,-b/radius,a/radius,0],[0,0,0,1]])
    framed_equations = tuple(sp.expand(e) for e in frame*sp.Matrix(time_system.equations))
    framed = DifferentialSystem(stationary,framed_equations,
        inequations=(*time_system.inequations,radius),assumptions=time_system.assumptions,
        name="E-stationary-radial-momentum-frame")
    rotation = PointGenerator((-b,a),(0,-v0,u0,0))
    r = sp.Symbol("r",positive=True)
    H,V = sp.symbols("H V",positive=True)
    W,Z = sp.symbols("W Z",real=True)
    s = sp.Symbol("s",real=True)
    radial = JetSpace((r,),(H,V,W,Z),2)
    radial_chart = ReductionChart(radial,(radius,),s,b/a,
        (r/sp.sqrt(1+s*s),r*s/sp.sqrt(1+s*s)),
        (H,(a*V-b*W)/radius,(b*V+a*W)/radius,Z),(1,1,1,1))
    rotation_outcome = reduce_in_chart(PDEProblem(framed,parameters=parameters),rotation,radial_chart)
    reduced = _require_reduction(rotation_outcome,"radial chart")
    Hp,Vp,Wp,Zp = (radial.jet_symbol(i,(1,)) for i in range(4))
    Zpp = radial.jet_symbol(3,(2,))
    speed2 = V*V+W*W
    qr = speed2*(K*V-G*Zp)
    expected = (
        V*Hp+H*Vp+H*V/r,
        V*Vp-W*W/r-f*W+g*(Hp+Zp),
        V*(Wp+W/r+f),
        c+qr/r+2*(V*Vp+W*Wp)*(K*V-G*Zp)+speed2*(K*Vp-G*Zpp),
    )
    equation_residuals = tuple(sp.simplify(a-b) for a,b in zip(reduced.equations,expected))

    # This path uses SymPy's ordinary Cartesian differentiation, not chart jets.
    xx,yy,tt = sp.symbols("xx yy tt",real=True)
    R = sp.sqrt(xx*xx+yy*yy)
    HH,VV,WW,ZZ = (sp.Function(name)(R) for name in ("HH","VV","WW","ZZ"))
    UU,VY,BB = (xx*VV-yy*WW)/R,(yy*VV+xx*WW)/R,ZZ+c*tt
    SS = sp.factor(UU*UU+VY*VY)
    direct = (
        sp.diff(HH,tt)+sp.diff(HH*UU,xx)+sp.diff(HH*VY,yy),
        sp.diff(UU,tt)+UU*sp.diff(UU,xx)+VY*sp.diff(UU,yy)+g*sp.diff(HH+BB,xx)-f*VY,
        sp.diff(VY,tt)+UU*sp.diff(VY,xx)+VY*sp.diff(VY,yy)+g*sp.diff(HH+BB,yy)+f*UU,
        sp.diff(BB,tt)+sp.diff(SS*(K*UU-G*sp.diff(BB,xx)),xx)
        +sp.diff(SS*(K*VY-G*sp.diff(BB,yy)),yy),
    )
    rr = sp.Symbol("rr",positive=True)
    q_functions = tuple(sp.Function(name)(rr) for name in ("HH","VV","WW","ZZ"))
    profile_rules = dict(zip((H,V,W,Z),q_functions))
    profile_rules.update({radial.jet_symbol(i,(degree,)):sp.diff(fun,rr,degree)
        for i,fun in enumerate(q_functions) for degree in (1,2)})
    pull_expected = tuple(e.xreplace(profile_rules).subs({r:rr}).subs(rr,R) for e in expected)
    full_expected = (pull_expected[0],
        (xx*pull_expected[1]-yy*pull_expected[2])/R,
        (yy*pull_expected[1]+xx*pull_expected[2])/R,pull_expected[3])
    cartesian_residuals = tuple(sp.simplify(a-b) for a,b in zip(direct,full_expected))
    opposite_bed = ZZ-c*tt
    opposite_bed_equation = (sp.diff(opposite_bed,tt)
        +sp.diff(SS*(K*UU-G*sp.diff(opposite_bed,xx)),xx)
        +sp.diff(SS*(K*VY-G*sp.diff(opposite_bed,yy)),yy))
    opposite_bed_sign_residual = sp.simplify(opposite_bed_equation-full_expected[3])
    reconstructed = (HH,UU,VY,BB)
    function_rules = dict(zip(source.dependent_fields,reconstructed))
    function_rules.update({symbol:sp.diff(reconstructed[field],tt,index[0],xx,index[1],yy,index[2])
        for (field,index),symbol in jet_coordinates(source).items() if any(index)})
    function_rules.update({t:tt,x:xx,y:yy})
    surface_residuals = tuple(sp.simplify(e.xreplace(function_rules))
        for generator in (time_generator,case.generators["J"])
        for e in characteristic(source,generator))

    radial_velocity = (x*u+y*v)/sp.sqrt(x*x+y*y)
    angular_velocity = (-y*u+x*v)/sp.sqrt(x*x+y*y)
    invariants = (sp.sqrt(x*x+y*y),h,radial_velocity,angular_velocity,B-c*t)
    sediment_normal_flux = (x*case.flux[0]+y*case.flux[1])/sp.sqrt(x*x+y*y)
    boundary_quantities = (*invariants,h*radial_velocity,sediment_normal_flux)
    data_invariance_residuals = tuple(sp.simplify(prolonged_action(source,e,generator))
        for generator in (time_generator,case.generators["J"]) for e in boundary_quantities)
    Vnormal = V*(W*W/r+f*W+g*H/r-g*Zp)/(V*V-g*H)
    Hnormal = -H*Vnormal/V-H/r
    Wnormal = -W/r-f
    Znormal = (c+qr/r+2*(V*Vnormal+W*Wnormal)*(K*V-G*Zp)+speed2*K*Vnormal)/(G*speed2)
    normal_rules = {Hp:Hnormal,Vp:Vnormal,Wp:Wnormal,Zpp:Znormal}
    normal_residuals = tuple(sp.cancel(e.xreplace(normal_rules)) for e in expected)
    first_integrals = (r*H*V,r*W+f*r*r/2,r*qr+c*r*r/2)
    integral_residuals = tuple(sp.cancel(total_derivative(radial,e,0).xreplace(normal_rules))
        for e in first_integrals)
    integral_independence = sp.factor(sp.Matrix(first_integrals).jacobian((H,W,Zp)).det())
    leading_matrix,_ = sp.linear_eq_to_matrix(expected,(Hp,Vp,Wp,Zpp))
    commutator = bracket(source,time_generator,case.generators["J"])
    return dict(time_certificate=time_outcome.certificate,rotation_certificate=rotation_outcome.certificate,
        time_chart=time_chart,rotation_chart=radial_chart,projection_rank=orbit_rank(source,(time_generator,case.generators["J"])),
        commutator=commutator.xi+commutator.phi,symbols=(r,H,V,W,Z,g,K,G,f,c),
        derivatives=(Hp,Vp,Wp,Zp,Zpp),equations=reduced.equations,
        comparison_residuals=equation_residuals,cartesian_pullback_residuals=cartesian_residuals,
        cartesian_pullback=full_expected,invariant_surface_residuals=surface_residuals,
        opposite_bed_sign_residual=opposite_bed_sign_residual,
        invariants=invariants,characteristics={"T_c":characteristic(source,time_generator),
            "J":characteristic(source,case.generators["J"])},
        boundary_invariant_quantities=boundary_quantities,data_invariance_residuals=data_invariance_residuals,
        equation_frame_determinant=sp.simplify(frame.det()),
        leading_determinant=sp.factor(leading_matrix.det()),
        normal_form=(Hnormal,Vnormal,Wnormal,Zp,Znormal),normal_form_residuals=normal_residuals,
        first_integrals=first_integrals,first_integral_residuals=integral_residuals,
        first_integral_independence_determinant=integral_independence,
        first_integral_independence_columns=(H,W,Zp),
        guards=("r>0", "H>0", "V>0", "g,K,G>0", "c!=0", "V**2-g*H!=0", "G*(V**2+W**2)!=0"),
        excluded_branches=("V=0", "H=0", "r=0", "V**2=g*H", "G=0"),
        chart_scope="local x>0 rational angular chart; independent Cartesian pullback valid on r>0")


@lru_cache(maxsize=1)
def certify_case() -> dict:
    """Return concrete profiles, jets, covariance, brackets and reduced ODEs."""
    case = build_case()
    symmetries = {name:certify_generator(case,generator,case.multipliers[name])
        for name,generator in case.generators.items()}
    basis = tuple(case.generators.values())
    algebra = check_lie_closure(case.system.jet_space,basis)
    eps = sp.Symbol("epsilon",real=True)
    adjoints = {}
    for i,name in enumerate(case.generators):
        matrix = sp.Matrix(6,6,lambda k,j:algebra.structure_constants[i][j][k])
        adjoints[name] = (eps*matrix).exp().applyfunc(sp.simplify)
    reduction = radial_reduction(case)
    t,x,y = case.system.jet_space.independent_variables
    spatial_only_rotation = PointGenerator((0,-y,x),(0,0,0,0))
    negative_control = certify_generator(case,spatial_only_rotation,case.multipliers["J"])
    residual_sets = (case.registry_residuals,reduction["comparison_residuals"],
        reduction["cartesian_pullback_residuals"],reduction["invariant_surface_residuals"],
        reduction["data_invariance_residuals"],reduction["normal_form_residuals"],
        reduction["first_integral_residuals"])
    passed = (all(record["verified"] for record in symmetries.values())
        and algebra.closure_status == "closed" and all(e == 0 for row in residual_sets for e in row)
        and reduction["projection_rank"] == 2)
    return dict(status="verified-local-subalgebra-and-reduction" if passed else "failed",
        target="full Eulerian E, isotropic m=3,n=2 bed flux, fixed optional Coriolis",
        system=case.system,parameters=case.parameters,flux=case.flux,
        registry_residuals=case.registry_residuals,symmetries=symmetries,
        jet_coordinate_legend={str(symbol):str(case.system.jet_space.dependent_fields[field])+"__"
            +"".join(str(variable)*count for variable,count in zip(case.system.jet_space.independent_variables,index))
            for (field,index),symbol in jet_coordinates(case.system.jet_space).items() if any(index)},
        algebra=dict(basis_names=tuple(case.generators),closure_status=algebra.closure_status,
            structure_constants=algebra.structure_constants,adjoint_parameter=eps,adjoints=adjoints,
            adjoint_convention="Ad(exp(epsilon X))Y=exp(epsilon ad_X)Y; [X,Y]=X(Y)-Y(X)"),
        reduction=reduction,maximal_classification_claim=False,
        negative_controls=dict(spatial_only_rotation=negative_control,
            opposite_bed_sign_residual=reduction["opposite_bed_sign_residual"]),
        physical_validation_claim=False,arbitrary_IBVP_claim=False)


def profile_rhs(r, state, *, g, K, G, f, c):
    """Guarded normal form for (H,V,W,Z,P=Z'); no singular division."""
    import numpy as np
    values = np.asarray((r,*state,g,K,G,f,c),dtype=float)
    if len(state) != 5 or not np.all(np.isfinite(values)):
        raise ValueError("finite radius, five-state data, and parameters are required")
    H,V,W,Z,P = map(float,state)
    pivot = V*V-g*H
    if r <= 0 or H <= 0 or V <= 0 or min(g,K,G) <= 0 or c == 0:
        raise ValueError("outside the r,H,V,g,K,G positive evolving-bed chart")
    if abs(pivot) <= 1e-10*max(1.,V*V,abs(g*H)):
        raise ValueError("characteristic pivot V**2-g*H is singular or near singular")
    S = V*V+W*W
    if G*S <= 1e-14:
        raise ValueError("diffusive normal-form denominator is singular")
    Vp = V*(W*W/r+f*W+g*H/r-g*P)/pivot
    Hp = -H*Vp/V-H/r
    Wp = -W/r-f
    Pp = (c+S*(K*V-G*P)/r+2*(V*Vp+W*Wp)*(K*V-G*P)+S*K*Vp)/(G*S)
    return np.array((Hp,Vp,Wp,P,Pp),dtype=float)


def _rk4(rhs, interval, initial, steps):
    import numpy as np
    grid = np.linspace(*interval,steps+1)
    values = np.empty((steps+1,len(initial)))
    values[0] = initial
    for i,r in enumerate(grid[:-1]):
        h = grid[i+1]-r
        state = values[i]
        k1 = rhs(r,state)
        k2 = rhs(r+h/2,state+h*k1/2)
        k3 = rhs(r+h/2,state+h*k2/2)
        k4 = rhs(r+h,state+h*k3)
        values[i+1] = state+h*(k1+2*k2+2*k3+k4)/6
    return grid,values


def _cartesian_fd_checks(solution, parameters):
    """Differentiate reconstructed fields in x,y, separately from radial RHS."""
    import numpy as np
    g,K,G,f,c = (parameters[k] for k in ("g","K","G","f","c"))

    def fields(x,y,t):
        r = np.hypot(x,y)
        H,V,W,Z,P = solution(r)
        return np.array((H,(x*V-y*W)/r,(y*V+x*W)/r,Z+c*t))

    records = []
    for step in (2e-3,1e-3,5e-4):
        residuals = []
        for radius in np.linspace(1.02,1.23,9):
            for theta in (0.,.7,2.2,4.6):
                x,y = radius*np.cos(theta),radius*np.sin(theta)
                for t in (0.,.7):
                    center = fields(x,y,t)
                    derivatives = []
                    second_bed = []
                    for axis in (0,1):
                        shifts = []
                        for offset in (-2,-1,1,2):
                            shifts.append(fields(x+offset*step*(axis==0),y+offset*step*(axis==1),t))
                        mm,m,p,pp = shifts
                        derivatives.append((mm-8*m+8*p-pp)/(12*step))
                        second_bed.append((-pp[3]+16*p[3]-30*center[3]+16*m[3]-mm[3])/(12*step*step))
                    H,u,v,B = center
                    Hx,ux,vx,Bx = derivatives[0]
                    Hy,uy,vy,By = derivatives[1]
                    S = u*u+v*v
                    residuals.append((
                        u*Hx+v*Hy+H*(ux+vy),
                        u*ux+v*uy+g*(Hx+Bx)-f*v,
                        u*vx+v*vy+g*(Hy+By)+f*u,
                        c+K*((3*u*u+v*v)*ux+2*u*v*vx+2*u*v*uy+(u*u+3*v*v)*vy)
                        -G*((2*u*ux+2*v*vx)*Bx+(2*u*uy+2*v*vy)*By+S*sum(second_bed)),
                    ))
        errors = np.max(np.abs(np.asarray(residuals)),axis=0)
        records.append(dict(step=step,points=len(residuals),per_equation_max_abs_residual=errors.tolist(),
                            max_abs_residual=float(np.max(errors))))
    return records


def solve_profile() -> dict:
    """Construct one regular numerical profile, with independent RK/FD checks."""
    import numpy as np
    from scipy.integrate import solve_ivp
    parameters = dict(g=1.,K=.05,G=.1,f=.2,c=.02)
    interval = (1.,1.25)
    initial = np.array((1.,2.,.3,0.,.9))
    rhs = lambda r,state:profile_rhs(r,state,**parameters)
    started = time.perf_counter()
    solution = solve_ivp(rhs,interval,initial,method="DOP853",rtol=1e-12,atol=1e-14,
                         dense_output=True,max_step=.025)
    if not solution.success or solution.t[-1] != interval[-1]:
        raise RuntimeError(f"profile integration did not reach endpoint: {solution.message}")
    grid = np.linspace(*interval,257)
    values = solution.sol(grid)
    H,V,W,Z,P = values
    S = V*V+W*W
    q = S*(parameters["K"]*V-parameters["G"]*P)
    integrals = (grid*H*V,grid*W+parameters["f"]*grid*grid/2,
                 grid*q+parameters["c"]*grid*grid/2)
    drifts = {name:float(np.max(np.abs(e-e[0])))
        for name,e in zip(("mass","angular","sediment"),integrals)}
    rk_records = []
    for steps in (8,16,32,64):
        rk_grid,rk_values = _rk4(rhs,interval,initial,steps)
        error = float(np.max(np.abs(rk_values-solution.sol(rk_grid).T)))
        rk_records.append(dict(method="classical-fixed-step-RK4",steps=steps,max_abs_error=error))
    fd = _cartesian_fd_checks(solution.sol,parameters)
    checks = (min(H)>0,min(V)>0,min(abs(V*V-parameters["g"]*H))>1e-6,
              rk_records[-1]["max_abs_error"]<1e-8,max(drifts.values())<1e-9,
              fd[-1]["max_abs_residual"]<1e-6)
    return dict(status="verified-sampled-numerical-profile" if all(checks) else "failed-numerical-gate",
        parameters=parameters,interval=interval,initial_state=dict(zip(("H","V","W","Z","P"),initial.tolist())),
        boundary_surface="x**2+y**2=r0**2, r0=1; invariant under J and T+c*dB",
        boundary_data=dict(depth=1.,radial_velocity=2.,azimuthal_velocity=.3,
            bed="B=.02*t",normal_bed_slope=.9,water_normal_flux=2.,sediment_normal_flux=.0409,
            total_water_flux=4*float(np.pi),total_sediment_flux=.0818*float(np.pi),
            normal_convention="e_r points away from the origin; inner-annulus domain-outward normal is -e_r"),
        first_integral_initial_values={name:float(e[0])
            for name,e in zip(("mass","angular","sediment"),integrals)},
        first_integral_max_drifts=drifts,minimum_H=float(min(H)),minimum_V=float(min(V)),
        minimum_abs_characteristic_pivot=float(min(abs(V*V-parameters["g"]*H))),
        minimum_diffusion_denominator=float(min(parameters["G"]*S)),
        cross_solver_max_abs_error=rk_records[-1]["max_abs_error"],rk4_convergence=rk_records,
        cartesian_finite_difference_checks=fd,solver=dict(method="scipy-DOP853",rtol=1e-12,atol=1e-14,
            nfev=solution.nfev,accepted_nodes=len(solution.t),message=solution.message),
        samples=dict(r=grid.tolist(),H=H.tolist(),V=V.tolist(),W=W.tolist(),Z=Z.tolist(),P=P.tolist(),
                     bed_normal_flux=q.tolist()),elapsed_seconds=time.perf_counter()-started,
        continuous_error_bound_claim=False,physical_validation_claim=False,
        scope="constructed smooth annular profile; sampled guards and residuals, not a continuous error theorem")


def write_profile_plot(report: dict, destination: Path) -> tuple[Path, Path]:
    """Plot recorded numerical fields; no new integration or fitted profile."""
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    destination = Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    samples = {key:np.asarray(value) for key,value in report["samples"].items()}
    r = samples["r"]
    fig, axes = plt.subplots(2,2,figsize=(11.5,7),layout="constrained")
    axes[0,0].plot(r,samples["H"],color="#176f53",linewidth=2)
    axes[0,0].set(title="Positive water depth",ylabel="H")
    axes[0,1].plot(r,samples["V"],label="Radial V",color="#145ca6",linewidth=2)
    axes[0,1].plot(r,samples["W"],label="Azimuthal W",color="#b24b48",linewidth=2)
    axes[0,1].set(title="Velocity profiles",ylabel="Velocity")
    axes[0,1].legend()
    for t,style in ((0.,"-"),(5.,"--")):
        bed = samples["Z"]+report["parameters"]["c"]*t
        axes[1,0].plot(r,bed,style,label=f"Bed, t={t:g}",color="#6d508e")
        axes[1,0].plot(r,bed+samples["H"],style,label=f"Surface, t={t:g}",color="#145ca6")
    axes[1,0].set(title="Evolving bed and free surface",ylabel="Elevation")
    axes[1,0].legend(fontsize=8,ncol=2)
    axes[1,1].plot(r,samples["bed_normal_flux"],color="#b24b48",linewidth=2)
    axes[1,1].set(title="Radially outward sediment flux",ylabel="q_r")
    for ax in axes.flat:
        ax.set_xlabel("Radius r")
        ax.grid(alpha=.25)
        ax.set_xlim(r[0],r[-1])
    fig.suptitle("Constructed annular full-E profile: g=1, K=0.05, G=0.1, f=0.2, c=0.02",fontsize=12)
    paths = destination/"annular-profile.png",destination/"annular-profile.pdf"
    fig.savefig(paths[0],dpi=160)
    fig.savefig(paths[1])
    plt.close(fig)
    return paths


def _jsonable(value):
    if isinstance(value,sp.MatrixBase):
        return [[_jsonable(e) for e in row] for row in value.tolist()]
    if isinstance(value,sp.Basic):
        return sp.sstr(value)
    if hasattr(value,"as_dict"):
        return _jsonable(value.as_dict())
    if is_dataclass(value):
        return {key:_jsonable(getattr(value,key)) for key in value.__dataclass_fields__}
    if isinstance(value,dict):
        return {str(key):_jsonable(e) for key,e in value.items()}
    if isinstance(value,(tuple,list)):
        return [_jsonable(e) for e in value]
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args = parser.parse_args(argv)
    destination = args.out.resolve()
    repo = Path(__file__).resolve().parents[2]
    if destination.is_relative_to(Path(__file__).resolve().parent):
        parser.error("write generated receipts outside the library source directory")
    destination.mkdir(parents=True,exist_ok=True)
    started = time.perf_counter()
    exact = certify_case()
    numerical = solve_profile()
    for filename,payload in (("exact.json",exact),("numerical.json",numerical)):
        (destination/filename).write_text(json.dumps(_jsonable(payload),indent=2)+"\n",encoding="utf-8")
    plot_paths = write_profile_plot(numerical,destination)
    source_paths = [Path(__file__).resolve(),Path(__file__).parent/"tests/test_annular2d.py",
        repo/"symm/generic/core.py",repo/"symm/generic/jets.py",repo/"symm/generic/reduction.py",
        repo/"symm/generic/chart_reduction.py",repo/"symm/generic/problem.py",repo/"symm/generic/boundary.py",
        Path(__file__).parent/"core.py",Path(__file__).parent/"models_2d.py",Path(__file__).parent/"_loader.py",
        Path(__file__).parent/"_snapshot/models.py",Path(__file__).parent/"_snapshot/models_2d.py",
        Path(__file__).parent/"_snapshot/main.py"]
    source_hashes = {str(path.relative_to(repo)).replace("\\","/"):
        hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
    manifest = dict(command="python -B -X utf8 -m symm.LieSymm.annular2d --out "+str(args.out),
        python=sys.version,executable=sys.executable,platform=platform.platform(),sympy=sp.__version__,
        source_sha256=source_hashes,receipts_sha256={name:hashlib.sha256((destination/name).read_bytes()).hexdigest()
            for name in ("exact.json","numerical.json",*(path.name for path in plot_paths))},elapsed_seconds=time.perf_counter()-started,
        exact_status=exact["status"],numerical_status=numerical["status"],
        invariance_chart="x>0 sector; separate direct Cartesian pullback on r>0",
        limitations=["No maximal classification", "No physical validation", "No arbitrary IBVP existence",
                     "Finite numeric checks do not certify continuous PDE error"])
    (destination/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:manifest[key] for key in ("exact_status","numerical_status","elapsed_seconds")},indent=2))
    return 0 if exact["status"].startswith("verified") and numerical["status"].startswith("verified") else 1


if __name__ == "__main__":
    raise SystemExit(main())
