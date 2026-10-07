"""Exact supplied-generator verification and a declared scaling ansatz."""
import json
import time
from pathlib import Path
import sympy as sp
from models import multiplier


def build(case):
    z = sp.symbols("t x y", real=True)
    h = sp.Symbol("h", positive=True)
    u, v, b = sp.symbols("u v b", real=True)
    fields = (h, u, v, b)
    d = [sp.symbols(n + "t " + n + "x " + n + "y", real=True)
         for n in ("h", "u", "v", "b")]
    ht, hx, hy = d[0]; ut, ux, uy = d[1]
    vt, vx, vy = d[2]; bt, bx, by = d[3]
    g, k, m, f, gamma = [sp.Rational(str(a)) for a in
                         (case.g, case.kappa, case.m, case.coriolis, case.drag)]
    r2 = u*u + v*v
    flux = k*(r2**((m-1)/2)*(ux+vy) + (m-1)*r2**((m-3)/2)*
              (u*u*ux + u*v*vx + u*v*uy + v*v*vy)) if k else sp.S.Zero
    eqs = sp.Matrix([ht+u*hx+v*hy+h*(ux+vy),
                     ut+u*ux+v*uy+g*(hx+bx)-f*v+gamma*u,
                     vt+u*vx+v*vy+g*(hy+by)+f*u+gamma*v,
                     bt+flux])
    return z, fields, d, eqs


def coefficients(z, fields, d, name):
    t, x, y = z; h, u, v, b = fields
    choices = {
        "Tt": ((1, 0, 0), (0, 0, 0, 0)),
        "Tx": ((0, 1, 0), (0, 0, 0, 0)),
        "Ty": ((0, 0, 1), (0, 0, 0, 0)),
        "D": (z, (0, 0, 0, 0)),
        "V": ((0, x, y), (2*h, u, v, 2*b)),
        "J": ((0, -y, x), (0, -v, u, 0)),
        "Gx": ((0, t, 0), (0, 1, 0, 0)),
    }
    xi, eta = [tuple(map(sp.sympify, a)) for a in choices[name]]
    def total(expr, i):
        return sp.diff(expr, z[i]) + sum(sp.diff(expr, fields[a])*d[a][i]
                                        for a in range(4))
    prolong = [total(eta[a], i) - sum(d[a][j]*total(xi[j], i) for j in range(3))
               for a in range(4) for i in range(3)]
    return sp.Matrix([*xi, *eta, *prolong])


def scaling_ansatz(case):
    # X=a*t*d_t+b*(x*d_x+y*d_y)+c*h*d_h+d*(u*d_u+v*d_v)+e*b*d_b.
    a, b, c, d, e = sp.symbols("a b c d e")
    constraints = [b-a-d, c-2*d, e-c]
    if case.kappa:
        constraints.append((sp.Rational(str(case.m))-1)*d-e)
    if case.coriolis or case.drag:
        constraints.append(a)
    mat, _ = sp.linear_eq_to_matrix(constraints, (a,b,c,d,e))
    return {"coefficient_names": ["a","b","c","d","e"],
            "constraints": list(map(str, constraints)),
            "matrix_shape": list(mat.shape), "rank": mat.rank(),
            "nullity": len(mat.nullspace()),
            "basis": [list(map(str, v)) for v in mat.nullspace()],
            "scope": "constant-coefficient isotropic scaling ansatz only"}


def audit(case):
    start = time.perf_counter()
    z, fields, d, eqs = build(case)
    jet = (*z, *fields, *(item for row in d for item in row))
    jac = eqs.jacobian(jet)
    build_seconds = time.perf_counter() - start
    rows = []
    for name in ("Tt", "Tx", "Ty", "D", "V", "J", "Gx"):
        tic = time.perf_counter()
        coef = coefficients(z, fields, d, name)
        prolonged = jac*coef
        matrix = sp.Matrix(multiplier(name).astype(int))
        defect = [sp.simplify(q) for q in prolonged-matrix*eqs]
        rows.append({"generator": name, "verified": all(q == 0 for q in defect),
                     "defect": list(map(str, defect)),
                     "verify_seconds": time.perf_counter()-tic,
                     "prolong_ops": sum(sp.count_ops(q) for q in prolonged),
                     "bulk_only": True,
                     "fixed_periodic_IC_compatible":
                         name in ("Tx", "Ty") and case.amplitude == 0 and case.bed_amplitude == 0})
    tic = time.perf_counter()
    ansatz = scaling_ansatz(case)
    ansatz_seconds = time.perf_counter()-tic
    useful = [r["generator"] for r in rows if r["verified"] and
              r["generator"] in ("D", "V", "J")]
    # Frozen-bed system permits arbitrary b(x,y); the truly flat-bed restriction
    # has additional symmetries, such as boosts, which that enlarged system loses.
    restricted_flat=None
    if case.kappa==0 and case.bed_amplitude==0 and not (case.coriolis or case.drag):
        boost=jac*coefficients(z,fields,d,'Gx')
        restricted_flat=all(sp.simplify(q.subs({a:0 for a in d[3]}))==0 for q in boost)
    return {"case": case.metadata(), "jet_dimension": len(jet),
            "equation_ops": sum(sp.count_ops(q) for q in eqs),
            "build_seconds": build_seconds, "scaling_seconds": ansatz_seconds,
            "total_seconds": time.perf_counter()-start,
            "generators": rows, "useful_generators": useful, "scaling_ansatz": ansatz,
            "assumptions": ["h>0", "u^2+v^2>0 for noninteger active flux", "g>0"],
            "claim": "supplied-generator identities; not a maximal Lie classification",
            "Galilean_Gx_valid_on_flat_bed_restriction": restricted_flat,
            "subgroups": {
                "D": "(t,x,y)->exp(eps)*(t,x,y); fields unchanged",
                "V": "(x,y)->exp(eps)*(x,y); (h,b)->exp(2eps)*(h,b); (u,v)->exp(eps)*(u,v)",
                "J": "rotate (x,y) and (u,v) through eps; h,b unchanged",
                "Tx_Ty": "commuting two-parameter translations; projected rank 2; nonuniform IC prevents hard reduction",
                "topology": "continuous rotations/scalings are bulk symmetries, not global actions of a fixed square torus"}}


def audit_suite(cases, output):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    results = {case.name: audit(case) for case in cases}
    (output/"symbolic.json").write_text(json.dumps(results, indent=2))
    return results
