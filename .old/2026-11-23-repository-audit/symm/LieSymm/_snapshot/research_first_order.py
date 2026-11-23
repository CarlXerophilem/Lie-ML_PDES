"""Unrestricted first-order SVE determining system and exact proof checks.

The proof of maximality is in FIRST_ORDER_DERIVATION.md. This module checks
its algebra and independently prolongs generators; a finite candidate test
is not the source of the completeness claim. All computations are exact.
"""
from __future__ import annotations

import json
from pathlib import Path
import time

import sympy as s

t, x, h, u, B = s.symbols("t x h u B", real=True)
g, K = s.symbols("g K", positive=True)
m = s.symbols("m", real=True)
COORDINATES = (t, x, h, u, B)
FIELDS = (h, u, B)
PARAMETERS = (g, K, m)
px = s.Matrix(s.symbols("h_x u_x B_x", real=True))


def flux_matrix(q=None):
    """A for w_t + A(w) w_x = 0; use q=0 for zero transport."""
    if q is None:
        q = m * K * u ** (m - 1)
    return s.Matrix([[u, h, 0], [g, u, g], [0, q, 0]])


def build_determining_system(q=None):
    """Return necessary and sufficient equations before projectability.

    tau, xi, and all three eta components initially depend on all five
    coordinates. The on-equation-manifold residual is C + M*px + Q2.
    Set every coefficient of this polynomial in the three free x jets
    to zero. This is an unrestricted determining system, not an ansatz.
    """
    A = flux_matrix(q)
    tau = s.Function("tau")(*COORDINATES)
    xi = s.Function("xi")(*COORDINATES)
    eta = s.Matrix([s.Function(n)(*COORDINATES) for n in ("H", "U", "Z")])
    J = eta.jacobian(FIELDS)
    ta = s.Matrix([[s.diff(tau, v) for v in FIELDS]])
    xb = s.Matrix([[s.diff(xi, v) for v in FIELDS]])
    Ap = A * px
    Q2 = (A * Ap) * (ta * px)[0] - Ap * (ta * Ap)[0]
    Q2 += px * (xb * Ap)[0] - Ap * (xb * px)[0]
    etaA = sum((eta[i] * A.diff(v) for i, v in enumerate(FIELDS)), s.zeros(3))
    M = A * J - J * A + etaA
    M += (s.diff(tau, t) - s.diff(xi, x)) * A
    M += s.diff(tau, x) * A * A - s.diff(xi, t) * s.eye(3)
    C = eta.diff(t) + A * eta.diff(x)
    return {"A": A, "tau": tau, "xi": xi, "eta": eta,
            "quadratic": Q2, "linear_matrix": M, "zero_order": C,
            "residual": C + M * px + Q2, "free_jets": px}


def direct_prolongation(generator, q=None):
    """Independent first-prolongation formula evaluated on w_t=-A*w_x."""
    A = flux_matrix(q)
    tau, xi, *components = map(s.sympify, generator)
    eta = s.Matrix(components)
    wt = -A * px

    def Dt(f):
        return s.diff(f, t) + sum(s.diff(f, w) * wt[i] for i, w in enumerate(FIELDS))

    def Dx(f):
        return s.diff(f, x) + sum(s.diff(f, w) * px[i] for i, w in enumerate(FIELDS))

    eta_t = eta.applyfunc(Dt) - wt * Dt(tau) - px * Dt(xi)
    eta_x = eta.applyfunc(Dx) - wt * Dx(tau) - px * Dx(xi)
    etaA = sum((eta[i] * A.diff(v) for i, v in enumerate(FIELDS)), s.zeros(3))
    return (eta_t + A * eta_x + etaA * px).applyfunc(s.simplify)


def _branch_name(branch):
    return {"grass_generic":"positive_generic", "grass_cubic":"positive_cubic"}.get(branch,branch)


def general_solution(branch="positive_generic", coordinates=None):
    """Integrated arbitrary coefficients with their surviving free constants.

    Coordinates may be supplied in the order (t,x,h,u,B), allowing a caller
    whose SymPy symbols carry different assumptions to substitute directly
    into its own raw determining equations. No basis is supplied as input.
    The necessity certificate is integration_certificate() and the proof.
    """
    branch = _branch_name(branch)
    if branch not in {"positive_generic", "positive_cubic", "zero_transport"}:
        raise ValueError("unknown first-order branch: " + branch)
    t0, x0, d0, beta, a0 = s.symbols("t0 x0 d0 beta a0",real=True)
    constants = (t0,x0,d0,beta)
    names = ("time_translation","space_translation","bed_translation","common_base_scaling")
    if branch == "positive_generic":
        a = s.S.Zero
    else:
        a = a0
        constants += (a0,)
        names += ("relative_scaling",)
    coefficients = s.Matrix([(beta+a)*t+t0,beta*x+x0,-2*a*h,-a*u,d0-2*a*B])
    if coordinates is not None:
        if len(coordinates) != 5:
            raise ValueError("coordinates must have length five")
        coefficients = coefficients.xreplace(dict(zip(COORDINATES,coordinates)))
    return {"branch":branch,"coefficients":coefficients,"free_constants":constants,
            "constant_names":names,"dimension":len(constants),
            "general_constraint_before_branching":K*(m-3)*a0,
            "proof_sections":list(range(2,8)),
            "necessity_status":"integrated_unrestricted_equations_pending_independent_review"}


def branch_generators(branch="positive_generic", coordinates=None):
    """Extract a basis by differentiating the solved general coefficients."""
    solved = general_solution(branch,coordinates)
    return {name:solved["coefficients"].diff(c)
            for name,c in zip(solved["constant_names"],solved["free_constants"])}


def integration_certificate():
    """Transparent algebraic elimination chain, before final integrations.

    Projectability and the integrations are proved in the accompanying
    readable derivation. Here U and H are actually solved from two invariant
    consequences of the arbitrary linear-jet determining matrix.
    """
    q = s.symbols("q",positive=True)
    a,b,c = s.symbols("a b c",real=True)
    H,U = s.symbols("H U")
    J = s.Matrix(3,3,lambda i,j:s.Symbol("HUZ"[i]+"_"+str(FIELDS[j])))
    A = flux_matrix(q)
    dA = s.Matrix([[U,H,0],[0,U,0],[0,(m-1)*q*U/u,0]])
    M = A*J-J*A+dA+a*A+b*A*A-c*s.eye(3)
    trace_equations = [s.trace(M),s.trace(A*M)]
    solved = s.solve(trace_equations,(H,U),dict=True)[0]
    determinant = s.factor(s.trace(A.adjugate()*M))
    D = s.expand(determinant.subs(solved))
    return {
        "projectability_quadratic_factor":"(lambda_i-lambda_j)*(lambda_i*tau_wj-xi_wj)",
        "linear_matrix":M,"trace_equations":trace_equations,
        "solved_H_U":solved,"determinant_equation":determinant,
        "determinant_after_trace":D,
        "h_coefficient":s.factor(s.diff(D,h)),
        "m_one_after_h_split":s.factor(D.subs({m:1,c:-g*q*b})),
        "positive_after_b_c_zero":s.factor(D.subs({b:0,c:0})),
        "zero_transport_determinant":s.factor(D.subs(q,0)),
        "remaining_field_equations":["Z_h=0","Z_u=0","Z_B=-2a"],
        "remaining_base_equations":["tau_x=0","xi_t=0","a_t=0","a_x=0","d_t=0","d_x=0"],
        "branch_divisors":["g>0","h>0","u>0","q>0 only on K>0", "m-1 only on m>1"],
        "exceptional_factors":["K", "m-1 handled separately", "m-3", "u^2-gh handled by dense smooth extension"],
    }


def verify_generator(generator, branch="positive_generic", m_value=None):
    branch = _branch_name(branch)
    q = 0 if branch == "zero_transport" else None
    residual = direct_prolongation(generator, q=q)
    if branch == "positive_cubic":
        residual = residual.subs(m, 3)
    if m_value is not None:
        residual = residual.subs(m, s.sympify(m_value))
    return residual.applyfunc(s.simplify)


def run_verification():
    """Check proof identities and controls; raise on a failed exact check."""
    start = time.perf_counter()
    checks = {}

    def check(name, expression):
        expressions = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
        residuals = [s.simplify(e) for e in expressions]
        ok = all(e == 0 for e in residuals)
        checks[name] = {"passed": ok, "nonzero_residuals": [str(e) for e in residuals if e != 0]}
        if not ok:
            raise AssertionError((name, residuals))

    system = build_determining_system()
    arbitrary = [system["tau"], system["xi"], *system["eta"]]
    check("unrestricted_split_equals_direct_prolongation",
          system["residual"] - direct_prolongation(arbitrary))

    # Eigenbasis coefficients of the quadratic determining equations.
    lam = s.symbols("lambda_0:3")
    aw = s.symbols("tau_w0:3")
    bw = s.symbols("xi_w0:3")
    L = s.diag(*lam)
    lp = L * px
    ta, xb = s.Matrix([aw]), s.Matrix([bw])
    qe = L*lp*(ta*px)[0] - lp*(ta*lp)[0] + px*(xb*lp)[0] - lp*(xb*px)[0]
    for i in range(3):
        for j in range(3):
            if i != j:
                coeff = s.Poly(s.expand(qe[i]), *px).coeff_monomial(px[i]*px[j])
                check(f"quadratic_eigenbasis_{i}_{j}", coeff - (lam[i]-lam[j])*(lam[i]*aw[j]-bw[j]))

    q, qp = s.symbols("q qp", real=True)
    aa, bb, cc = s.symbols("a b c", real=True)
    HH, UU, ZZ = s.symbols("H U Z")
    A = flux_matrix(q)
    J = s.Matrix(3, 3, lambda i,j:s.Symbol("HUZ"[i]+"_"+str(FIELDS[j])))
    dA = s.Matrix([[UU, HH, 0], [0, UU, 0], [0, qp*UU, 0]])
    M = A*J-J*A+dA+aa*A+bb*A*A-cc*s.eye(3)
    e2 = u*u-g*(h+q)
    determinant_identity = -g*(q+u*qp)*UU-3*aa*g*q*u-2*bb*g*q*u*u-cc*e2
    check("determinant_identity_without_invertibility",
          s.trace(A.adjugate()*M)-determinant_identity)
    check("trace_identity", s.trace(M)-(2*UU+2*aa*u+2*bb*(u*u+g*(h+q))-3*cc))
    check("K_positive_symmetrizer", s.diag(g/h,1,g/q)*A-(s.diag(g/h,1,g/q)*A).T)
    z = s.symbols("lambda")
    check("K_zero_characteristic", flux_matrix(0).charpoly(z).as_expr()-z*((z-u)**2-g*h))
    check("K_zero_discriminant", s.discriminant(z*((z-u)**2-g*h),z)-4*g*h*(u*u-g*h)**2)

    U0 = s.Rational(3,2)*cc-aa*u-bb*(u*u+g*(h+q))
    D = s.expand(determinant_identity.subs({UU:U0,qp:(m-1)*q/u}))
    expected = (aa*g*q*u*(m-3) + bb*g*q*u*u*(m-2)
                + bb*g*g*m*q*q + cc*g*q*(1-s.Rational(3,2)*m)-cc*u*u
                + h*(bb*g*g*m*q+cc*g))
    check("determinant_after_trace", D-expected)
    check("determinant_h_coefficient", s.diff(D,h)-g*(bb*g*m*q+cc))
    check("m_one_remaining_equation", D.subs({m:1,cc:-g*q*bb})-g*q*(-4*aa*u+3*bb*g*q)/2)
    check("generic_exceptional_factor", D.subs({bb:0,cc:0})-aa*g*q*u*(m-3))
    H0 = -2*aa*h+aa*(m-3)*q + bb*g*(m-1)*q*(h+q)/u
    H0 += -4*bb*h*u+bb*(m-2)*q*u-s.Rational(3,2)*cc*(m-1)*q/u-cc*u/g
    trace_AM = s.trace(A*M).subs({UU:U0,HH:H0,qp:(m-1)*q/u})
    check("trace_A_M_solves_H", trace_AM)

    # K=0 leaves b in invariant equations; an actual matrix equation removes it.
    e0 = s.Matrix([-2*aa*h-4*bb*h*u, -aa*u-bb*(u*u+g*h), s.Function("Z")(h,u,B)])
    A0 = flux_matrix(0)
    M0 = A0*e0.jacobian(FIELDS)-e0.jacobian(FIELDS)*A0
    M0 += sum((e0[i]*A0.diff(v) for i,v in enumerate(FIELDS)),s.zeros(3))
    M0 += aa*A0+bb*A0*A0
    check("K_zero_matrix_11_removes_tau_x", M0[0,0]-3*g*h*bb)

    at, ax, dt, dx = s.symbols("a_t a_x d_t d_x")
    eta_t = s.Matrix([-2*h*at,-u*at,-2*B*at+dt])
    eta_x = s.Matrix([-2*h*ax,-u*ax,-2*B*ax+dx])
    C = eta_t+A*eta_x
    check("remaining_zero_jet_equations", C-s.Matrix([
        -2*h*at-3*h*u*ax,
        -u*at-(2*g*h+u*u+2*g*B)*ax+g*dx,
        -2*B*at-q*u*ax+dt]))

    witnesses = {}
    for branch in ("positive_generic","positive_cubic","zero_transport"):
        witnesses[branch] = {}
        solved = general_solution(branch)
        check(branch+"_general_solution",verify_generator(solved["coefficients"],branch))
        for name, vector in branch_generators(branch).items():
            r = verify_generator(vector,branch)
            check(branch+"_"+name,r)
            witnesses[branch][name] = [str(v) for v in vector]

    S = s.Matrix([t,0,-2*h,-u,-2*B])
    rS = direct_prolongation(S)
    check("extra_scaling_exact_defect", rS-s.Matrix([0,0,(3-m)*m*K*u**(m-1)*px[1]]))
    boost = direct_prolongation([0,t,0,1,0])
    check("galilean_defect",boost-s.Matrix([0,0,m*K*(m-1)*u**(m-2)*px[1]-px[2]]))
    gauge = direct_prolongation([0,0,0,0,B*B],q=0)
    check("nonlinear_bed_relabeling_defect",gauge-s.Matrix([0,2*g*B*px[2],0]))
    nonprojectable = direct_prolongation([h,0,0,0,0],q=0)
    if all(v == 0 for v in nonprojectable):
        raise AssertionError("nonprojectable negative control unexpectedly passed")

    return {
        "model": "h_t+u*h_x+h*u_x=0; u_t+u*u_x+g*(h_x+B_x)=0; B_t+m*K*u^(m-1)*u_x=0",
        "assumptions": ["local smooth point symmetries", "open connected coordinate domain", "h>0", "u>0", "g>0", "K>=0", "1<=m<=4"],
        "claim_status": "complete_unrestricted_point_algebra_derived; independent_review_required",
        "proof": "FIRST_ORDER_DERIVATION.md",
        "dimensions": {"K>0,m!=3":4,"K>0,m=3":5,"K=0,m_removed":5},
        "checks": checks,
        "check_count": len(checks),
        "all_checks_passed": all(v["passed"] for v in checks.values()),
        "generators": witnesses,
        "general_solutions":{branch:{
            "coefficients":[str(v) for v in general_solution(branch)["coefficients"]],
            "free_constants":[str(v) for v in general_solution(branch)["free_constants"]]}
            for branch in witnesses},
        "integration_certificate":{key:str(value) for key,value in integration_certificate().items()},
        "negative_controls": {
            "extra_scaling_generic_defect": [str(v) for v in rS],
            "galilean_defect": [str(v) for v in boost],
            "nonlinear_bed_relabeling_defect_K_zero": [str(v) for v in gauge],
            "nonprojectable_trial_defect_K_zero": [str(v) for v in nonprojectable],
        },
        "elapsed_seconds": time.perf_counter()-start,
        "not_claimed": ["equivalence-group maximality", "optimal-system completeness", "generalized/contact/nonlocal symmetry classification", "arbitrary data compatibility", "well-posedness", "2D classification"],
    }


if __name__ == "__main__":
    receipt = run_verification()
    target = Path(__file__).with_name("first_order_results.json")
    target.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(target),"checks":receipt["check_count"],
                      "passed":receipt["all_checks_passed"],
                      "elapsed_seconds":receipt["elapsed_seconds"]},indent=2))
