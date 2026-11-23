"""Independent unrestricted-point calculation for the slope-diffusion SVE family.

This is a staged exact algebra verifier, not a finite generator-ansatz search.
The integration of its necessary coefficient equations is in SLOPE_DERIVATION.md.
Run: python -B research_slope.py
Only research_slope_results.json in this script's directory is written.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import sympy as s

t, x = s.symbols("t x", real=True)
h, u = s.symbols("h u", positive=True)
B = s.Symbol("B", real=True)
g, G = s.symbols("g G", positive=True)
K = s.Symbol("K", nonnegative=True)
m, n = s.symbols("m n", real=True)
ht, ut, Bt, p, q, r = s.symbols("h_t u_t B_t h_x u_x B_x")
htt, utt, Btt, htx, utx, Btx, hxx, uxx, v = s.symbols(
    "h_tt u_tt B_tt h_tx u_tx B_tx h_xx u_xx B_xx"
)
coords = (t, x, h, u, B)
fields = (h, u, B)
tjets, xjets = (ht, ut, Bt), (p, q, r)
C, D = m*K*u**(m-1), G*u**n
f = (-u*p-h*q, -u*q-g*(p+r), D*v+s.diff(D,u)*q*r-C*q)
first_order_subs = dict(zip(tjets, f))


def dx(expr):
    """Total x derivative through order two, in the ambient jet space."""
    result = s.diff(expr, x)
    for var, jet in zip(fields, xjets):
        result += jet*s.diff(expr, var)
    for var, jet in zip(tjets+xjets, (htx,utx,Btx,hxx,uxx,v)):
        result += jet*s.diff(expr,var)
    return s.expand(result)


def dt(expr):
    """Total t derivative through order two, in the ambient jet space."""
    result = s.diff(expr, t)
    for var, jet in zip(fields, tjets):
        result += jet*s.diff(expr,var)
    for var, jet in zip(tjets+xjets, (htt,utt,Btt,htx,utx,Btx)):
        result += jet*s.diff(expr,var)
    return s.expand(result)


def clean(expr):
    return s.simplify(s.expand(expr))


def residuals(tau, xi, a, b, c):
    """Actual prolongation of all three equations from arbitrary point fields."""
    etas = (a,b,c)
    et = [dt(e)-yt*dt(tau)-yx*dt(xi)
          for e,yt,yx in zip(etas,tjets,xjets)]
    ex = [dx(e)-yt*dx(tau)-yx*dx(xi)
          for e,yt,yx in zip(etas,tjets,xjets)]
    cxx = dx(ex[2])-Btx*dx(tau)-v*dx(xi)
    out = (
        et[0]+b*p+u*ex[0]+a*q+h*ex[1],
        et[1]+b*q+u*ex[1]+g*(ex[0]+ex[2]),
        et[2]+s.diff(C,u)*b*q+C*ex[1]-s.diff(D,u)*b*v-D*cxx
        -s.diff(D,u,2)*b*q*r-s.diff(D,u)*(ex[1]*r+q*ex[2]),
    )
    return tuple(s.expand(z.subs(first_order_subs, simultaneous=True)) for z in out)


def arbitrary(name, variables=coords):
    return s.Function(name)(*variables)


def general_solution(branch, coordinates=None, exponent=None):
    """Solve the integrated necessary equations on an explicit model branch.

    ``coordinates`` is (t,x,h,u,B); ``exponent`` is m on positive-K branches
    and n on ``slope_only``. The basis is obtained by differentiation only
    AFTER linsolve solves equations (20),(21). Generic symbolic elimination
    is authorized by the recorded m!=3 and m>=1 guards, not by silent division.
    """
    selected = (t,x,h,u,B) if coordinates is None else tuple(coordinates)
    if len(selected) != 5:
        raise ValueError("coordinates must be (t,x,h,u,B)")
    tt,xx,hh,uu,BB = selected
    if branch in ("slope_attachment_generic", "slope_source_generic"):
        mm = m if exponent is None else s.sympify(exponent)
        if mm.is_number and (mm == 3 or not 1 <= mm <= 4):
            raise ValueError("generic positive-K branch requires 1<=m<=4 and m!=3")
        nn = mm-1 if branch == "slope_attachment_generic" else mm
        transport_factor = mm*K*(mm-3)
        guards = ["K>0","G>0","1<=m<=4","m!=3"]
    elif branch in ("slope_attachment_cubic", "slope_source_cubic"):
        if exponent is not None and s.sympify(exponent) != 3:
            raise ValueError("cubic positive-K branch requires m=3")
        mm = s.Integer(3)
        nn = s.Integer(2 if branch == "slope_attachment_cubic" else 3)
        transport_factor = mm*K*(mm-3)
        guards = ["K>0","G>0","m=3"]
    elif branch == "slope_only":
        mm = None
        nn = n if exponent is None else s.sympify(exponent)
        if nn.is_number and not 0 <= nn <= 4:
            raise ValueError("slope_only requires 0<=n<=4")
        transport_factor = s.S.Zero
        guards = ["K=0","G>0","0<=n<=4"]
    else:
        raise ValueError(f"not a G>0 slope branch: {branch}")
    t0,x0,b0,T,d = s.symbols("t0 x0 b0 T d",real=True)
    constant_equations = (T+(2-nn)*d, transport_factor*d)
    solution_set = s.linsolve(constant_equations,(T,d))
    solutions = list(solution_set)
    if len(solutions) != 1:
        raise AssertionError(f"unexpected constant system: {solution_set}")
    Tsol,dsol = solutions[0]
    unrestricted_integral = s.Matrix((T*tt+t0,(T+d)*xx+x0,2*d*hh,d*uu,b0+2*d*BB))
    coefficients = unrestricted_integral.subs({T:Tsol,d:dsol},simultaneous=True)
    free_constants = tuple(z for z in (t0,x0,b0,d) if coefficients.has(z))
    basis = tuple(coefficients.diff(z) for z in free_constants)
    return {
        "coefficients":coefficients,"free_constants":free_constants,"basis":basis,
        "constant_equations":constant_equations,"constant_solution":(Tsol,dsol),
        "branch":branch,"m":mm,"n":nn,"guards":guards,
        "coordinate_order":selected,
    }


def run():
    start = time.perf_counter()
    checks = []
    equations = {}

    def check(name, actual, expected=0):
        delta = clean(actual-expected)
        if delta != 0:
            raise AssertionError(f"{name}: {delta}")
        checks.append(name)

    # The J2 chart includes all order-two consequences of the first-order rows.
    # Its free jets include B_tx, h_xx, u_xx, B_xx and B_tt.
    mixed = {htx: dx(f[0]), utx: dx(f[1])}
    second_time = {
        htt: dt(f[0]).subs(first_order_subs, simultaneous=True).subs(mixed),
        utt: dt(f[1]).subs(first_order_subs, simultaneous=True).subs(mixed),
    }
    full_chart = {**first_order_subs, **mixed, **second_time}
    first_rows = (ht+u*p+h*q, ut+u*q+g*(p+r))
    for i, row in enumerate(first_rows):
        for label, deriv in (("t",dt),("x",dx)):
            check(f"J2 consequence F{i+1}_{label}",
                  deriv(row).subs(full_chart, simultaneous=True))

    tau,xi,a,b,c = [arbitrary(z) for z in ("tau","xi","a","b","c")]
    raw = residuals(tau,xi,a,b,c)
    check("B_tx coefficient forces D_x tau=0", s.diff(raw[2],Btx),2*D*dx(tau))
    equations["tau_projectability"] = str(2*D*dx(tau))

    tau = arbitrary("tau",(t,))
    raw = residuals(tau,xi,a,b,c)
    check("h_xx coefficient",s.diff(raw[2],hxx),-D*(s.diff(c,h)-r*s.diff(xi,h)))
    check("u_xx coefficient",s.diff(raw[2],uxx),-D*(s.diff(c,u)-r*s.diff(xi,u)))
    xi,c = arbitrary("xi",(t,x,B)),arbitrary("c",(t,x,B))
    raw = residuals(tau,xi,a,b,c)
    expected_v = D*(2*s.diff(xi,x)-s.diff(tau,t)+2*r*s.diff(xi,B))-s.diff(D,u)*b
    check("B_xx coefficient forces xi_B=0",s.diff(raw[2],v),expected_v)
    equations["xi_B_projectability"] = str(expected_v)

    xi = arbitrary("xi",(t,x))
    raw = residuals(tau,xi,a,b,c)
    check("water row gives a_B=0",s.diff(raw[0],v),D*s.diff(a,B))
    check("momentum row gives b_B=0",s.diff(raw[1],v),D*s.diff(b,B))
    a,b = arbitrary("a",(t,x,h,u)),arbitrary("b",(t,x,h,u))
    raw = residuals(tau,xi,a,b,c)
    check("water B_x coefficient gives a_u=0",s.diff(raw[0],r),-g*s.diff(a,u))
    a = arbitrary("a",(t,x,h))
    raw = residuals(tau,xi,a,b,c)
    tt,xx,xt = s.diff(tau,t),s.diff(xi,x),s.diff(xi,t)
    hydro = [
        h*s.diff(b,h)+b-xt+u*(tt-xx),
        a-h*s.diff(a,h)+h*s.diff(b,u)+h*(tt-xx),
        s.diff(a,t)+u*s.diff(a,x)+h*s.diff(b,x),
        g*(-s.diff(b,u)+s.diff(a,h)+tt-xx),
        -h*s.diff(b,h)+b-xt+u*(tt-xx),
        g*(-s.diff(b,u)+s.diff(c,B)+tt-xx),
        s.diff(b,t)+u*s.diff(b,x)+g*(s.diff(a,x)+s.diff(c,x)),
    ]
    check("water coefficient reconstruction",raw[0],hydro[0]*p+hydro[1]*q+hydro[2])
    check("momentum coefficient reconstruction",raw[1],hydro[3]*p+hydro[4]*q+hydro[5]*r+hydro[6])
    equations["hydrodynamic_necessary_and_sufficient"] = [str(z) for z in hydro]

    T,L,t0 = s.symbols("T L t0",real=True)
    d = L-T
    R,S = arbitrary("R",(t,)),arbitrary("S",(t,))
    integrated = (T*t+t0,L*x+R,2*d*h,d*u+s.diff(R,t),2*d*B-s.diff(R,t,2)*x/g+S)
    res = residuals(*integrated)
    check("integrated water identity",res[0])
    check("integrated momentum identity",res[1])
    expected_bed = (
        D*(T+(2-n)*d-n*s.diff(R,t)/u)*v
        +s.diff(D,u)*(T+(2-n)*d-(n-1)*s.diff(R,t)/u)*q*r
        +(C*((m-3)*d+(m-1)*s.diff(R,t)/u)+s.diff(D,u)*s.diff(R,t,2)/g)*q
        -s.diff(R,t)*r-s.diff(R,t,3)*x/g+s.diff(S,t)
    )
    check("complete remaining bed determining identity",res[2],expected_bed)
    equations["bed_after_hydrodynamic_integration"] = str(s.factor(expected_bed))

    # Exact family verification does not substitute finitely sampled exponents.
    integrated_solution = general_solution("slope_only")
    extracted_basis = tuple(tuple(gen) for gen in integrated_solution["basis"])
    translations, dilation = extracted_basis[:3], extracted_basis[3]
    for j,gen in enumerate(translations):
        for i,expr in enumerate(residuals(*gen)):
            check(f"translation {j} row {i}",expr)
    dil_res = residuals(*dilation)
    check("D_n water",dil_res[0])
    check("D_n momentum",dil_res[1])
    check("D_n exact obstruction",dil_res[2],K*m*(m-3)*u**(m-1)*q)
    for label,sub in (("K=0 symbolic n",{K:0}),("m=3 symbolic n",{m:3})):
        check(label,dil_res[2].subs(sub))

    # Broken-hypothesis controls: no acceptance merely from generator shape.
    controls = {}
    wrong_spatial = residuals(0,x,2*h,u,2*B)[2].subs({m:3,n:3})
    controls["spatial_only_m3_n3"] = str(clean(wrong_spatial))
    controls["Galilean_n0_K0"] = str(clean(residuals(0,t,0,1,0)[2].subs({n:0,K:0})))
    controls["time_dependent_bed_shift"] = str(clean(residuals(0,0,0,0,t)[2]))
    controls["dilation_m2_K1"] = str(clean(dil_res[2].subs({m:2,K:1})))
    for name,expr in controls.items():
        if expr == "0":
            raise AssertionError(f"broken hypothesis was not detected: {name}")

    branch_solutions = {}
    for branch in ("slope_attachment_generic","slope_source_generic",
                   "slope_attachment_cubic","slope_source_cubic","slope_only"):
        solved = general_solution(branch)
        st,sd = solved["constant_solution"]
        for j,eq in enumerate(solved["constant_equations"]):
            check(f"constant solve {branch} equation {j}",
                  eq.subs({s.Symbol("T",real=True):st,s.Symbol("d",real=True):sd},simultaneous=True))
        branch_solutions[branch] = {
            "coefficients":[str(z) for z in solved["coefficients"]],
            "free_constants":[str(z) for z in solved["free_constants"]],
            "basis":[[str(z) for z in gen] for gen in solved["basis"]],
            "constant_equations":[str(z) for z in solved["constant_equations"]],
            "constant_solution":[str(z) for z in solved["constant_solution"]],
            "guards":solved["guards"],
        }

    result = {
        "status":"all_exact_checks_passed; maximality_pending_fresh_review",
        "scope":"G>0,g>0,h>0,u>0; smooth local point fields; 1D full evolving-bed system",
        "independent_variables":["t","x"],"fields":["h","u","B"],
        "free_J2_jets":["h_x","u_x","B_x","h_xx","u_xx","B_xx","B_tx","B_tt"],
        "checked_identities":checks,"check_count":len(checks),
        "necessary_equations":equations,
        "basis_universal":["d_t","d_x","d_B"],
        "extra_generator":"(n-2)t*d_t+(n-1)x*d_x+2h*d_h+u*d_u+2B*d_B",
        "extra_generator_condition":"K=0 or m=3",
        "branch_solutions_from_linsolve":branch_solutions,
        "parameter_equations":["T+(2-n)d=0","K*m*(m-3)d=0"],
        "branch_divisions":["G*u**n != 0","g != 0","h != 0","u > 0"],
        "no_division_by":["n","n-1","n-2","m-3","K"],
        "broken_hypothesis_controls":controls,
        "elapsed_seconds":time.perf_counter()-start,
    }
    output = Path(__file__).with_name("research_slope_results.json")
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("status","check_count","elapsed_seconds")},indent=2))
    return result


if __name__ == "__main__":
    run()
